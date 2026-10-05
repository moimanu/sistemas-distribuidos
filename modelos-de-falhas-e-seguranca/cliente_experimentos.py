import time
import random
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN_VALIDO = "secret-token-123"

def executar_requisicao_com_retry(url, headers=None, json_data=None, metodo="GET", tentativas=4, timeout=0.5):
    """Executa requisições HTTP aplicando Retry com Backoff Exponencial + Jitter."""
    headers = headers or {}
    
    for tentativa in range(tentativas):
        inicio = time.time()
        try:
            if metodo == "GET":
                r = requests.get(url, headers=headers, timeout=timeout)
            elif metodo == "POST":
                r = requests.post(url, headers=headers, json=json_data, timeout=timeout)
            
            duracao = (time.time() - inicio) * 1000
            
            if r.status_code >= 400:
                print(f"  [Tentativa {tentativa+1}/{tentativas}] Status {r.status_code} ({duracao:.1f}ms) -> {r.json().get('detail')}")
                if 400 <= r.status_code < 500:
                    return r
                r.raise_for_status()
            
            print(f"  [Tentativa {tentativa+1}/{tentativas}] SUCESSO (200 OK) em {duracao:.1f}ms")
            return r

        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as exc:
            duracao = (time.time() - inicio) * 1000
            tipo_erro = type(exc).__name__
            
            if tentativa == tentativas - 1:
                print(f"  [Tentativa {tentativa+1}/{tentativas}] FALHA FINAL após {duracao:.1f}ms: {tipo_erro}")
                return None
            
            espera = (2 ** tentativa) * 0.2 + random.uniform(0.0, 0.1)
            print(f"  [Tentativa {tentativa+1}/{tentativas}] Falha ({tipo_erro} em {duracao:.1f}ms). Reenviando em {espera:.2f}s...")
            time.sleep(espera)


def executar_bateria_de_testes():
    print("="*70)
    print("🚀 INICIANDO BATERIA DE EXPERIMENTOS DE FALHAS E SEGURANÇA")
    print("="*70)

    #--------------------------------------------------------------
    print("\nCENÁRIO 1: Referência Sem Falha")
    executar_requisicao_com_retry(f"{BASE_URL}/experimento/instavel?atraso_ms=0&prob_falha=0.0")

    #--------------------------------------------------------------
    print("\nCENÁRIO 2: Timeout (Modelo de Interação & Detector Imperfeito)")
    print("Injetando atraso de 1000ms com timeout limite de 0.3s...")
    executar_requisicao_com_retry(f"{BASE_URL}/experimento/instavel?atraso_ms=1000", tentativas=1, timeout=0.3)

    #--------------------------------------------------------------
    print("\nCENÁRIO 3: Falha Transitória com Retry + Backoff Exponencial")
    print("Injetando 70% de probabilidade de erro 503 com 4 tentativas de retry...")
    executar_requisicao_com_retry(f"{BASE_URL}/experimento/instavel?prob_falha=0.7", tentativas=4, timeout=0.5)

    #--------------------------------------------------------------
    print("\nCENÁRIO 4: Segurança (Autenticidade & Autenticação por Token)")
    payload_jogador = {"nickname": "Hacker_123", "plataforma": "PC", "rank": "Bronze"}
    
    print("a) Tentativa de escrita SEM token (Esperado 401 Unauthorized):")
    executar_requisicao_com_retry(f"{BASE_URL}/jogadores", json_data=payload_jogador, metodo="POST", tentativas=1)

    print("\nb) Tentativa de escrita COM token válido:")
    headers = {"X-API-Token": TOKEN_VALIDO}
    executar_requisicao_com_retry(f"{BASE_URL}/jogadores", headers=headers, json_data=payload_jogador, metodo="POST", tentativas=1)

    #--------------------------------------------------------------
    print("\nCENÁRIO 5: Efeito Adverso de Retry em Operação Não Idempotente")
    payload_partida = {"gols": 2, "assistencias": 1, "defesas": 0, "resultado": "vitoria"}
    
    print("a) Registrando partida sem Idempotency Key (Retries duplicated result):")
    for i in range(2):
        print(f" Envios repetidos {i+1}:")
        executar_requisicao_com_retry(f"{BASE_URL}/jogadores/1/partidas", headers=headers, json_data=payload_partida, metodo="POST", tentativas=1)

    print("\nb) Registrando partida COM Idempotency Key (Proteção contra duplicatas):")
    headers_idempotente = {"X-API-Token": TOKEN_VALIDO, "X-Idempotency-Key": "req-uuid-9999"}
    for i in range(2):
        print(f" Envios repetidos {i+1}:")
        executar_requisicao_com_retry(f"{BASE_URL}/jogadores/1/partidas", headers=headers_idempotente, json_data=payload_partida, metodo="POST", tentativas=1)

    print("\n" + "="*70)
    print("✅ EXPERIMENTOS CONCLUÍDOS COM SUCESSO!")
    print("="*70)

if __name__ == "__main__":
    executar_bateria_de_testes()