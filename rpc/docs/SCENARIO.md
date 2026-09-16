# Tabela de Latência e Status por Experimento

| Experimento / Cenário | Operação RPC | Status gRPC Observado | Latência (ms) | Observação de Comportamento |
| :--- | :--- | :--- | :--- | :--- |
| **1. Fluxo Normal (Sucesso)** | RegistrarJogador | OK (0) | 5.62 ms | Cadastro com payload válido ("moimanu"). |
| **1. Fluxo Normal (Sucesso)** | EnviarEstatisticaPartida | OK (0) | 0.64 ms | Vínculo de estatísticas de partida executado. |
| **2. Validação de Domínio (Erro)** | RegistrarJogador | INVALID_ARGUMENT (3) | 0.59 ms | Nickname vazio bloqueado pela validação do servidor. |
| **2. Entidade Inexistente (Erro)** | EnviarEstatisticaPartida | NOT_FOUND (5) | 0.61 ms | Tentativa de atualizar ID 9999 não existente no repositório. |
| **3. Server Streaming** | AcompanharPartidaAoVivo | OK (0) | 2504.33 ms | Transmissão contínua de 5 pacotes com intervalo nominal (0.5s). |
| **4. Teste Concorrente (10 reqs)** | RegistrarJogador | OK (0) | 0.86 ms a 1.51 ms | Executado via ThreadPoolExecutor (4 workers concorrentes). |
| **5. Servidor Offline / Timeout** | RegistrarJogador | DEADLINE_EXCEEDED (4) / UNAVAILABLE (14) | 1004.02 ms | Timeout do cliente atingido em porta sem serviço ativo (50099). |