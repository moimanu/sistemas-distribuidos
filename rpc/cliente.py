from concurrent.futures import ThreadPoolExecutor
import time
import grpc

import rocket_league_pb2
import rocket_league_pb2_grpc

# FUNÇÕES DE CLIENTE (Simples, curtas e sem tipagem ruidosa)

def cadastrar_jogador(stub, nickname, carro, plataforma, nivel_xp=0, timeout=2.0):
    print(f"\n--- Cadastrar Jogador ({nickname}) ---")
    req = rocket_league_pb2.JogadorRequest(
        nickname=nickname, carro=carro, plataforma=plataforma, nivel_xp=nivel_xp
    )
    t0 = time.perf_counter()
    try:
        res = stub.RegistrarJogador(req, timeout=timeout)
        lat = (time.perf_counter() - t0) * 1000
        print(f"Sucesso! ID: {res.jogador_id} | Retorno: {res.mensagem} [{lat:.2f}ms]")
        return res.jogador_id
    except grpc.RpcError as e:
        lat = (time.perf_counter() - t0) * 1000
        print(f"Erro RPC [{e.code()}]: {e.details()} [{lat:.2f}ms]")
        return None

def enviar_estatisticas(stub, jogador_id, gols, resultado, temporada="Season 14", timeout=2.0):
    print(f"\n--- Enviar Stats (ID: {jogador_id}) ---")
    req = rocket_league_pb2.PartidaStatsRequest(
        jogador_id=jogador_id, gols=gols, assistencias=1, defesas=2,
        resultado=resultado, temporada=temporada
    )
    t0 = time.perf_counter()
    try:
        res = stub.EnviarEstatisticaPartida(req, timeout=timeout)
        lat = (time.perf_counter() - t0) * 1000
        print(f"Sucesso! {res.detalhe} [{lat:.2f}ms]")
        return res.sucesso
    except grpc.RpcError as e:
        lat = (time.perf_counter() - t0) * 1000
        print(f"Erro [{e.code()}]: {e.details()} [{lat:.2f}ms]")
        return False

def consumir_stream_telemetria(stub, partida_id, timeout=10.0):
    print(f"\n--- Telemetria da Partida #{partida_id} ---")
    req = rocket_league_pb2.PartidaStreamRequest(partida_id=partida_id)
    t0 = time.perf_counter()
    try:
        stream = stub.AcompanharPartidaAoVivo(req, timeout=timeout)
        for p in stream:
            print(f"[{p.segundo}s] Azul {p.placar_azul} x {p.placar_laranja} Laranja | Evento: {p.ultimo_evento}")
        lat = (time.perf_counter() - t0) * 1000
        print(f"Transmissão encerrada. [{lat:.2f}ms]")
    except grpc.RpcError as e:
        lat = (time.perf_counter() - t0) * 1000
        print(f"Erro Stream [{e.code()}]: {e.details()} [{lat:.2f}ms]")

# EXPERIMENTOS E TESTES

def worker_concorrente(id_thread, endereco):
    with grpc.insecure_channel(endereco) as channel:
        stub = rocket_league_pb2_grpc.RocketLeagueServiceStub(channel)
        req = rocket_league_pb2.JogadorRequest(
            nickname=f"Bot_{id_thread}", carro="Dominus", plataforma="Epic", nivel_xp=10 * id_thread
        )
        t0 = time.perf_counter()
        try:
            res = stub.RegistrarJogador(req, timeout=3.0)
            lat = (time.perf_counter() - t0) * 1000
            print(f"[Thread #{id_thread:02d}] Sucesso -> ID: {res.jogador_id} [{lat:.2f}ms]")
        except grpc.RpcError as e:
            lat = (time.perf_counter() - t0) * 1000
            print(f"[Thread #{id_thread:02d}] Falha: {e.code()} [{lat:.2f}ms]")

def testar_concorrencia(endereco="localhost:50051", total=10, workers=4):
    print(f"\n--- Teste Concorrente ({total} reqs / {workers} workers) ---")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        for i in range(total):
            executor.submit(worker_concorrente, i + 1, endereco)

def testar_servidor_offline(endereco="localhost:50099"):
    print(f"\n--- Teste Servidor Offline ({endereco}) ---")
    with grpc.insecure_channel(endereco) as channel:
        stub = rocket_league_pb2_grpc.RocketLeagueServiceStub(channel)
        req = rocket_league_pb2.JogadorRequest(nickname="Ghost", carro="Merc", plataforma="PC")
        t0 = time.perf_counter()
        try:
            stub.RegistrarJogador(req, timeout=1.0)
        except grpc.RpcError as e:
            lat = (time.perf_counter() - t0) * 1000
            print(f"Capturado com sucesso: Status {e.code()} [{lat:.2f}ms]")

# EXECUÇÃO PRINCIPAL

def main():
    endereco = "localhost:50051"
    
    with grpc.insecure_channel(endereco) as channel:
        stub = rocket_league_pb2_grpc.RocketLeagueServiceStub(channel)

        # 1. Fluxo normal
        j_id = cadastrar_jogador(stub, "moimanu", "Fennec", "Steam", nivel_xp=150)
        if j_id:
            enviar_estatisticas(stub, j_id, gols=3, resultado="vitoria")

        # 2. Erros de negócio
        cadastrar_jogador(stub, "", "Octane", "Steam") # (nickname vazio)
        enviar_estatisticas(stub, jogador_id=9999, gols=0, resultado="derrota") # (ID inexistente)

        # 3. Stream
        consumir_stream_telemetria(stub, partida_id=101)

        # 4. Concorrência
        testar_concorrencia(endereco)

    # 5. Offline
    testar_servidor_offline()

if __name__ == '__main__':
    main()