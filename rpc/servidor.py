import time
from concurrent import futures
import grpc

import rocket_league_pb2
import rocket_league_pb2_grpc

# CAMADA DE REGRAS DE NEGÓCIO (Single Responsibility Principle)

class GerenciadorJogadores:
    def __init__(self):
        self._jogadores = {}
        self._proximo_id = 1

    def cadastrar(self, nickname: str, carro: str, plataforma: str, nivel_xp: int = 0):
        jogador_id = self._proximo_id
        self._jogadores[jogador_id] = {
            "nickname": nickname,
            "carro": carro,
            "plataforma": plataforma,
            "nivel_xp": nivel_xp
        }
        self._proximo_id += 1
        msg = f"Jogador '{nickname}' (XP: {nivel_xp}) registrado com sucesso!"
        return jogador_id, msg

    def existe(self, jogador_id: int) -> bool:
        return jogador_id in self._jogadores

def gerar_telemetria(partida_id: int):
    eventos = [
        (10, 0, 0, f"[Partida #{partida_id}] Kickoff inicial executado."),
        (45, 1, 0, f"[Partida #{partida_id}] Gol de Kickoff! Marca Time Azul."),
        (120, 1, 1, f"[Partida #{partida_id}] Gol de Chute Aéreo! Marca Time Laranja."),
        (240, 2, 1, f"[Partida #{partida_id}] Defesa Épica e Gol do Time Azul!"),
        (300, 2, 1, f"[Partida #{partida_id}] Fim de jogo! Vitória do Time Azul.")
    ]
    for seg, azul, laranja, evt in eventos:
        time.sleep(0.5)
        yield seg, azul, laranja, evt

# CAMADA gRPC

class RocketLeagueServicer(rocket_league_pb2_grpc.RocketLeagueServiceServicer):
    def __init__(self, gerenciador: GerenciadorJogadores = None):
        self.gerenciador = gerenciador or GerenciadorJogadores()

    def RegistrarJogador(self, request, context):
        if not request.nickname or not request.nickname.strip():
            print("[SERVIDOR - ERRO] Nickname inválido (vazio).")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("O nickname do jogador não pode ser vazio.")
            return rocket_league_pb2.JogadorResponse()

        j_id, msg = self.gerenciador.cadastrar(
            request.nickname, request.carro, request.plataforma, request.nivel_xp
        )
        print(f"[SERVIDOR] Reg. OK -> ID {j_id} | Nick: {request.nickname}")
        return rocket_league_pb2.JogadorResponse(jogador_id=j_id, mensagem=msg)

    def EnviarEstatisticaPartida(self, request, context):
        if not self.gerenciador.existe(request.jogador_id):
            print(f"[SERVIDOR - ERRO] ID {request.jogador_id} não encontrado.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Jogador ID {request.jogador_id} não localizado.")
            return rocket_league_pb2.ConfirmacaoResponse(sucesso=False, detalhe="Jogador inexistente")

        print(f"[SERVIDOR] Stats salvos -> ID {request.jogador_id} | Gols: {request.gols}")
        return rocket_league_pb2.ConfirmacaoResponse(
            sucesso=True, 
            detalhe="Estatísticas vinculadas à temporada com sucesso."
        )

    def AcompanharPartidaAoVivo(self, request, context):
        print(f"[SERVIDOR - STREAM] Transmitindo partida ID {request.partida_id}...")
        for seg, azul, laranja, evt in gerar_telemetria(request.partida_id):
            yield rocket_league_pb2.TelemetriaPartida(
                segundo=seg,
                placar_azul=azul,
                placar_laranja=laranja,
                ultimo_evento=evt
            )

# INICIALIZAÇÃO

def iniciar_servidor(porta="50051", max_workers=10):
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    rocket_league_pb2_grpc.add_RocketLeagueServiceServicer_to_server(
        RocketLeagueServicer(), servidor
    )
    servidor.add_insecure_port(f"[::]:{porta}")
    print(f"🚀 Servidor rodando na porta {porta}...")
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()