# Tabela de Resultados por Cenário de Teste

---

## 1. Resumo dos Cenários

| ID | Cenário / Casos de Teste | Tópico MQTT | QoS Utilizado | Retained Flag | Comportamento Esperado | Resultado Observado | Status |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- | :---: |
| **CEN-01** | Inicialização e Monitoramento Global | `rocketleague/#` | QoS 2 | N/A | Captura completa de todo o tráfego do ecossistema via tópicos coringa (wildcard). | Dashboard conectou e interceptou todas as mensagens publicadas na hierarquia sem perda. | **APROVADO** |
| **CEN-02** | Registro e Presença de Jogadores | `rocketleague/jogadores/+/status` | QoS 1 | `True` | Publicação do status do jogador. Garantia de entrega e persistência da mensagem mais recente no broker. | Status `online` mantido pelo broker; leitores subsequentes leram imediatamente a presença do jogador. | **APROVADO** |
| **CEN-03** | Fila de Matchmaking | `rocketleague/matchmaking/fila` | QoS 1 | `False` | Recepção ordenada de solicitações de entrada em fila (`busca_partida`) para pareamento 1v1. | `p1` e `p2` deram *match* instantâneo assim que o 2º jogador enviou a solicitação à fila. | **APROVADO** |
| **CEN-04** | Alocação de Sala / Partida Criada | `rocketleague/partida/{id}/info` | QoS 1 | `True` | Notificação de sala criada. Retenção permite que jogadores que conectem em seguida recebam os dados da sala. | Sala `#101` foi criada com `[p1, p2]` e entregue aos clientes interessados. | **APROVADO** |
| **CEN-05** | Eventos Críticos de Jogo (Gols / Fim) | `rocketleague/partida/{id}/eventos` | QoS 2 | `False` | Garantia rigorosa de entrega *Exactly Once* (sem duplicações e sem perdas) para atualização do placar. | Gol do `p1` e encerramento da partida foram processados sem duplicatas ou falhas na transmissão. | **APROVADO** |
| **CEN-06** | Streaming de Telemetria de Alta Frequência | `rocketleague/partida/{id}/telemetria` | QoS 0 | `False` | Envio em alta velocidade (*At Most Once*) com baixo *overhead*. Tolerância a pequenas divergências de ordem/perda. | Transmissão contínua de pacotes (1 a 10) para `p1` e `p2` realizada com latência mínima. | **APROVADO** |
| **CEN-07** | Detecção de Queda Abrupta (LWT) | `rocketleague/jogadores/{id}/status` | QoS 1 | `True` | Publicação automática do testamento (*Last Will and Testament*) pelo broker ao detectar desconexão sem `DISCONNECT`. | Ao encerrar `p3` via `Ctrl+C`, o broker publicou `status: offline` com `reason: LWT_DISCONNECT`. | **APROVADO** |
| **CEN-08** | Auditoria e Detecção de Sequência / Duplicatas | Todos | N/A | N/A | Identificação de pacotes antigos ou reinjetados por meio da validação de número de sequência (`seq`). | Dashboard detectou reinjeção de sequência no evento LWT (`seq 1 <= último 2`) marcando alerta de duplicata. | **APROVADO** |