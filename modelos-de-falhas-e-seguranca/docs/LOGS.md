## Logs Completos do Terminal

```bash
PS C:\Users\moise\Documents\GitHub\sistemas-distribuidos\modelos-de-falhas-e-seguranca> python cliente_experimentos.py
>> 
======================================================================
🚀 INICIANDO BATERIA DE EXPERIMENTOS DE FALHAS E SEGURANÇA
======================================================================

CENÁRIO 1: Referência Sem Falha
  [Tentativa 1/4] SUCESSO (200 OK) em 25.9ms

CENÁRIO 2: Timeout (Modelo de Interação & Detector Imperfeito)
Injetando atraso de 1000ms com timeout limite de 0.3s...
  [Tentativa 1/1] FALHA FINAL após 334.4ms: ReadTimeout

CENÁRIO 3: Falha Transitória com Retry + Backoff Exponencial
Injetando 70% de probabilidade de erro 503 com 4 tentativas de retry...
  [Tentativa 1/4] Status 503 (17.3ms) -> Falha transitória injetada (Servidor Indisponível)
  [Tentativa 1/4] Falha (HTTPError em 17.5ms). Reenviando em 0.29s...
  [Tentativa 2/4] SUCESSO (200 OK) em 24.3ms

CENÁRIO 4: Segurança (Autenticidade & Autenticação por Token)
a) Tentativa de escrita SEM token (Esperado 401 Unauthorized):
  [Tentativa 1/1] Status 401 (15.9ms) -> Não autorizado: Token de API inválido ou ausente.

b) Tentativa de escrita COM token válido:
  [Tentativa 1/1] Status 409 (16.7ms) -> Nickname 'Hacker_123' já existe.

CENÁRIO 5: Efeito Adverso de Retry em Operação Não Idempotente
a) Registrando partida sem Idempotency Key (Retries duplicated result):
 Envios repetidos 1:
  [Tentativa 1/1] SUCESSO (200 OK) em 6.0ms
 Envios repetidos 2:
  [Tentativa 1/1] SUCESSO (200 OK) em 24.2ms

b) Registrando partida COM Idempotency Key (Proteção contra duplicatas):
 Envios repetidos 1:
  [Tentativa 1/1] SUCESSO (200 OK) em 14.7ms
 Envios repetidos 2:
  [Tentativa 1/1] SUCESSO (200 OK) em 15.0ms

======================================================================
✅ EXPERIMENTOS CONCLUÍDOS COM SUCESSO!
======================================================================
```