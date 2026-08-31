import requests

BASE_URL = "http://127.0.0.1:8000"

print("=== INICIANDO ROTEIRO AUTOMATIZADO DE TESTES ===")

payload_jogador = {
    "nickname": "Octane",
    "plataforma": "Steam",
    "rank": "Champion II"
}

jogador_id = None

# TESTE 1: Listar Jogadores Iniciais (Seed)
print("\n[TESTE 1: GET /jogadores - Seed Inicial]")
try:
    resposta = requests.get(f"{BASE_URL}/jogadores", timeout=3.0)
    
    assert resposta.status_code == 200, f"Esperado 200, obtido {resposta.status_code}"
    
    dados = resposta.json()
    assert len(dados) >= 2, "Seed deve conter pelo menos 2 jogadores"
    
    print(f" -> SUCESSO! Total de jogadores no banco: {len(dados)}")
except Exception as erro:
    print(f" -> FALHA: {erro}")

# TESTE 2: Criar Jogador
print("\n[TESTE 2: POST /jogadores - Criar Jogador]")
try:
    resposta = requests.post(f"{BASE_URL}/jogadores", json=payload_jogador, timeout=3.0)
    
    assert resposta.status_code == 201, f"Esperado 201, obtido {resposta.status_code}"
    assert "Location" in resposta.headers, "Header Location ausente"
    
    dados = resposta.json()
    assert dados["nickname"] == payload_jogador["nickname"], "Nickname divergente"
    
    jogador_id = dados["id"]
    print(f" -> SUCESSO! Criado ID {jogador_id}. Location: {resposta.headers['Location']}")
except Exception as erro:
    print(f" -> FALHA: {erro}")

# TESTE 3: ERRO DE APLICAÇÃO 1 - Nickname Duplicado (409 Conflict)
print("\n[TESTE 3 (ERRO DE APLICAÇÃO 1): POST /jogadores - Nickname Duplicado (409)]")
try:
    resposta = requests.post(f"{BASE_URL}/jogadores", json=payload_jogador, timeout=3.0)
    
    assert resposta.status_code == 409, f"Esperado 409, obtido {resposta.status_code}"
    
    dados = resposta.json()
    print(f" -> SUCESSO! Erro 409 capturado: {dados['detail']}")
except Exception as erro:
    print(f" -> FALHA: {erro}")

# TESTE 4: Registrar Partida
if jogador_id is not None:
    print(f"\n[TESTE 4: POST /jogadores/{jogador_id}/partidas - Registrar Partida]")
    try:
        dados_partida = {
            "gols": 4,
            "assistencias": 1,
            "defesas": 2,
            "resultado": "vitoria"
        }
        resposta = requests.post(
            f"{BASE_URL}/jogadores/{jogador_id}/partidas", 
            json=dados_partida, 
            timeout=3.0
        )
        
        assert resposta.status_code == 201, f"Esperado 201, obtido {resposta.status_code}"
        
        dados = resposta.json()
        print(f" -> SUCESSO! Partida cadastrada com ID {dados['id']}")
    except Exception as erro:
        print(f" -> FALHA: {erro}")

# TESTE 5: Atualizar Jogador
if jogador_id is not None:
    print(f"\n[TESTE 5: PUT /jogadores/{jogador_id} - Atualizar Jogador]")
    try:
        dados_atualizados = {
            "nickname": "Octane_PRO",
            "plataforma": "Steam",
            "rank": "Grand Champion"
        }
        resposta = requests.put(
            f"{BASE_URL}/jogadores/{jogador_id}", 
            json=dados_atualizados, 
            timeout=3.0
        )
        
        assert resposta.status_code == 200, f"Esperado 200, obtido {resposta.status_code}"
        
        dados = resposta.json()
        assert dados["nickname"] == "Octane_PRO", "Update falhou"
        
        print(" -> SUCESSO! Dados do jogador atualizados.")
    except Exception as erro:
        print(f" -> FALHA: {erro}")

# TESTE 6: ERRO DE APLICAÇÃO 2 - Recurso Inexistente (404 Not Found)
print("\n[TESTE 6 (ERRO DE APLICAÇÃO 2): GET /jogadores/9999 - Recurso Inexistente (404)]")
try:
    resposta = requests.get(f"{BASE_URL}/jogadores/9999", timeout=3.0)
    
    assert resposta.status_code == 404, f"Esperado 404, obtido {resposta.status_code}"
    
    dados = resposta.json()
    print(f" -> SUCESSO! Erro 404 capturado: {dados['detail']}")
except Exception as erro:
    print(f" -> FALHA: {erro}")

# TESTE 7: Remover Jogador
if jogador_id is not None:
    print(f"\n[TESTE 7: DELETE /jogadores/{jogador_id} - Remover Jogador]")
    try:
        resposta = requests.delete(f"{BASE_URL}/jogadores/{jogador_id}", timeout=3.0)
        
        assert resposta.status_code == 204, f"Esperado 204, obtido {resposta.status_code}"
        
        print(" -> SUCESSO! Jogador e sub-recursos removidos com sucesso.")
    except Exception as erro:
        print(f" -> FALHA: {erro}")

# TESTE 8: FALHA DE CONECTIVIDADE (Interativo)
print("\n" + "="*60)
print("[PAUSA PARA O TESTE 8 - FALHA DE CONECTIVIDADE]")
print("Por favor, acesse o terminal onde a API está executando e")
print("DESLIGUE O SERVIDOR (pressione Ctrl+C) para testar a queda de conexão.")
print("="*60)

input("\n>> Pressione ENTER após desligar o servidor para executar o Teste 8... ")

print(f"\n[TESTE 8 (FALHA DE CONECTIVIDADE): GET {BASE_URL}/jogadores]")
try:
    resposta = requests.get(f"{BASE_URL}/jogadores", timeout=3.0)
    print(" -> FALHA: A requisição respondeu, o servidor ainda está ligado!")
except requests.exceptions.ConnectionError:
    print(" -> SUCESSO! Falha de conectividade capturada com êxito (ConnectionError).")
    print("    O cliente tentou conectar na porta 8000, mas a conexão foi recusada.")
except Exception as erro:
    print(f" -> FALHA INESPERADA: {erro}")

print("\n=== FINAL DO ROTEIRO DE TESTES ===")