## Resumo dos Logs por Timestamp

A tabela abaixo resume os principais eventos registrados pelo dashboard de auditoria, organizados em ordem cronológica de acordo com o *timestamp* da mensagem:

| Timestamp | Tópico | Produtor | Sequência (`seq`) | QoS | Evento / Descrição Resumida |
| --- | --- | --- | --- | --- | --- |
| **22:44:25.822** | `rocketleague/partida/101/estado` | `server` | 1 | 1 | Publicação do estado inicial da partida (`EM_ANDAMENTO`, placar 0x0, 300s). |
| **22:44:27.824** | `rocketleague/partida/101/eventos` | `server` | 2 | 2 | Disparo de evento crítico: `GOL!` marcado pelo jogador `p1`. |
| **22:44:28.823** | `rocketleague/partida/101/estado` | `server` | 3 | 1 | Atualização de estado da partida após o gol (placar 1x0, 210s). |
| **22:44:30.825** | `rocketleague/partida/101/eventos` | `server` | 4 | 2 | Evento de encerramento da partida: `FIM_DE_JOGO` com vitória do `time_azul`. |
| **22:44:33.825** | `rocketleague/jogadores/p1/status` | `p1` | 1 | 1 | Jogador `p1` conecta e publica status `online`. |
| **22:44:33.826** | `rocketleague/matchmaking/fila` | `p1` | 2 | 1 | Jogador `p1` solicita entrada na fila de matchmaking (`busca_partida`). |
| **22:44:37.591** | `rocketleague/jogadores/p2/status` | `p2` | 1 | 1 | Jogador `p2` conecta e publica status `online`. |
| **22:44:37.592** | `rocketleague/matchmaking/fila` | `p2` | 2 | 1 | Jogador `p2` solicita entrada na fila de matchmaking (`busca_partida`). |
| **22:44:37.593** | `rocketleague/partida/101/info` | `matchmaker` | 1 | 1 | Matchmaker identifica 2 jogadores na fila (`p1`, `p2`) e cria a Sala #101. |
| **22:44:41.479** | `rocketleague/jogadores/p3/status` | `p3` | 1 | 1 | Jogador `p3` conecta e publica status `online`. |
| **22:44:41.479** | `rocketleague/matchmaking/fila` | `p3` | 2 | 1 | Jogador `p3` entra na fila de espera por novos jogadores. |
| **22:44:42.600** | `rocketleague/partida/101/telemetria` | `p1` | 3 | 0 | Início do streaming de telemetria de `p1` (Pacote 1). |
| **22:44:42.641** | `rocketleague/partida/101/telemetria` | `p2` | 3 | 0 | Início do streaming de telemetria de `p2` (Pacote 1). |
| **22:44:42.641** a **22:44:42.725** | `rocketleague/partida/101/telemetria` | `p1` / `p2` | 4–12 | 0 | Envio contínuo de dados de telemetria via QoS 0 (Pacotes 2 ao 10). |
| **22:44:43.948** | `rocketleague/jogadores/p3/status` | `p3` | 1 | 1 | **Detecção de Queda (LWT):** Broker dispara mensagem `offline` registrada como duplicada/desordenada (`seq 1 <= último 2`). |

---

## Logs Completos do Terminal

```text
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>docker compose up -d
[+] up 2/2
 ✔ Network mqtt_default       Created                                                                                                     0.0s
 ✔ Container mosquitto_broker Started                                                                                                     0.3s

C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>python dashboard.py

======================================================================
🖥️  DASHBOARD & AUDITORIA DE PROTOCOLO MQTT - ROCKET LEAGUE
======================================================================
⚡ [DASHBOARD] Conectado ao Broker MQTT.
📌 [DASHBOARD] Assinado no tópico wildcard 'rocketleague/#' com QoS 2.

[22:44:25.822] Tópico: rocketleague/partida/101/estado | QoS: 1
         Produtor: server | seq: 1
         Dados: {'id_partida': '101', 'status': 'EM_ANDAMENTO', 'placar': {'time_azul': 0, 'time_laranja': 0}, 'tempo_restante_seg': 300, 'producer': 'server', 'seq': 1}
----------------------------------------------------------------------
[22:44:27.824] Tópico: rocketleague/partida/101/eventos | QoS: 2
         Produtor: server | seq: 2
         Dados: {'id_partida': '101', 'evento': 'GOL!', 'autor': 'p1', 'time': 'time_azul', 'descricao': 'Golaço de bicicleta no ângulo!', 'producer': 'server', 'seq': 2}
----------------------------------------------------------------------
[22:44:28.823] Tópico: rocketleague/partida/101/estado | QoS: 1
         Produtor: server | seq: 3
         Dados: {'id_partida': '101', 'status': 'EM_ANDAMENTO', 'placar': {'time_azul': 1, 'time_laranja': 0}, 'tempo_restante_seg': 210, 'producer': 'server', 'seq': 3}
----------------------------------------------------------------------
[22:44:30.825] Tópico: rocketleague/partida/101/eventos | QoS: 2
         Produtor: server | seq: 4
         Dados: {'id_partida': '101', 'evento': 'FIM_DE_JOGO', 'vencedor': 'time_azul', 'placar_final': {'time_azul': 1, 'time_laranja': 0}, 'producer': 'server', 'seq': 4}
----------------------------------------------------------------------
[22:44:33.825] Tópico: rocketleague/jogadores/p1/status | QoS: 1
         Produtor: p1 | seq: 1
         Dados: {'player_id': 'p1', 'status': 'online', 'producer': 'p1', 'seq': 1}
----------------------------------------------------------------------
[22:44:33.826] Tópico: rocketleague/matchmaking/fila | QoS: 1
         Produtor: p1 | seq: 2
         Dados: {'player_id': 'p1', 'action': 'busca_partida', 'producer': 'p1', 'seq': 2}
----------------------------------------------------------------------
[22:44:37.591] Tópico: rocketleague/jogadores/p2/status | QoS: 1
         Produtor: p2 | seq: 1
         Dados: {'player_id': 'p2', 'status': 'online', 'producer': 'p2', 'seq': 1}
----------------------------------------------------------------------
[22:44:37.592] Tópico: rocketleague/matchmaking/fila | QoS: 1
         Produtor: p2 | seq: 2
         Dados: {'player_id': 'p2', 'action': 'busca_partida', 'producer': 'p2', 'seq': 2}
----------------------------------------------------------------------
[22:44:37.593] Tópico: rocketleague/partida/101/info | QoS: 1
         Produtor: matchmaker | seq: 1
         Dados: {'id_partida': '101', 'jogadores': ['p1', 'p2'], 'status': 'criada', 'producer': 'matchmaker', 'seq': 1}
----------------------------------------------------------------------
[22:44:41.479] Tópico: rocketleague/jogadores/p3/status | QoS: 1
         Produtor: p3 | seq: 1
         Dados: {'player_id': 'p3', 'status': 'online', 'producer': 'p3', 'seq': 1}
----------------------------------------------------------------------
[22:44:41.479] Tópico: rocketleague/matchmaking/fila | QoS: 1
         Produtor: p3 | seq: 2
         Dados: {'player_id': 'p3', 'action': 'busca_partida', 'producer': 'p3', 'seq': 2}
----------------------------------------------------------------------
[22:44:42.600] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 3
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 1, 'velocidade_kmh': 58.9, 'boost_pct': 36, 'producer': 'p1', 'seq': 3}    
----------------------------------------------------------------------
[22:44:42.641] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 3
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 1, 'velocidade_kmh': 52.0, 'boost_pct': 76, 'producer': 'p2', 'seq': 3}    
----------------------------------------------------------------------
[22:44:42.641] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 4
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 2, 'velocidade_kmh': 61.0, 'boost_pct': 9, 'producer': 'p1', 'seq': 4}     
----------------------------------------------------------------------
[22:44:42.642] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 5
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 3, 'velocidade_kmh': 98.5, 'boost_pct': 90, 'producer': 'p1', 'seq': 5}    
----------------------------------------------------------------------
[22:44:42.642] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 6
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 4, 'velocidade_kmh': 68.5, 'boost_pct': 49, 'producer': 'p1', 'seq': 6}    
----------------------------------------------------------------------
[22:44:42.642] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 7
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 5, 'velocidade_kmh': 113.6, 'boost_pct': 65, 'producer': 'p1', 'seq': 7}   
----------------------------------------------------------------------
[22:44:42.642] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 8
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 6, 'velocidade_kmh': 81.6, 'boost_pct': 98, 'producer': 'p1', 'seq': 8}    
----------------------------------------------------------------------
[22:44:42.643] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 9
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 7, 'velocidade_kmh': 108.5, 'boost_pct': 62, 'producer': 'p1', 'seq': 9}   
----------------------------------------------------------------------
[22:44:42.643] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 10
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 8, 'velocidade_kmh': 93.8, 'boost_pct': 35, 'producer': 'p1', 'seq': 10}   
----------------------------------------------------------------------
[22:44:42.643] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 11
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 9, 'velocidade_kmh': 42.7, 'boost_pct': 92, 'producer': 'p1', 'seq': 11}   
----------------------------------------------------------------------
[22:44:42.681] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p1 | seq: 12
         Dados: {'player_id': 'p1', 'id_partida': '101', 'pacote': 10, 'velocidade_kmh': 71.5, 'boost_pct': 31, 'producer': 'p1', 'seq': 12}  
----------------------------------------------------------------------
[22:44:42.682] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 4
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 2, 'velocidade_kmh': 85.2, 'boost_pct': 99, 'producer': 'p2', 'seq': 4}    
----------------------------------------------------------------------
[22:44:42.682] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 5
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 3, 'velocidade_kmh': 46.4, 'boost_pct': 85, 'producer': 'p2', 'seq': 5}    
----------------------------------------------------------------------
[22:44:42.682] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 6
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 4, 'velocidade_kmh': 90.2, 'boost_pct': 73, 'producer': 'p2', 'seq': 6}    
----------------------------------------------------------------------
[22:44:42.683] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 7
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 5, 'velocidade_kmh': 60.9, 'boost_pct': 48, 'producer': 'p2', 'seq': 7}    
----------------------------------------------------------------------
[22:44:42.683] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 8
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 6, 'velocidade_kmh': 77.5, 'boost_pct': 46, 'producer': 'p2', 'seq': 8}    
----------------------------------------------------------------------
[22:44:42.683] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 9
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 7, 'velocidade_kmh': 49.9, 'boost_pct': 37, 'producer': 'p2', 'seq': 9}    
----------------------------------------------------------------------
[22:44:42.683] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 10
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 8, 'velocidade_kmh': 106.6, 'boost_pct': 46, 'producer': 'p2', 'seq': 10}  
----------------------------------------------------------------------
[22:44:42.683] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 11
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 9, 'velocidade_kmh': 108.6, 'boost_pct': 16, 'producer': 'p2', 'seq': 11}  
----------------------------------------------------------------------
[22:44:42.725] Tópico: rocketleague/partida/101/telemetria | QoS: 0
         Produtor: p2 | seq: 12
         Dados: {'player_id': 'p2', 'id_partida': '101', 'pacote': 10, 'velocidade_kmh': 59.1, 'boost_pct': 74, 'producer': 'p2', 'seq': 12}  
----------------------------------------------------------------------
[22:44:43.948] Tópico: rocketleague/jogadores/p3/status | QoS: 1 [💀 LAST WILL] [⚠️ DUPLICADA: seq 1 <= último 2]
         Produtor: p3 | seq: 1
         Dados: {'player_id': 'p3', 'status': 'offline', 'reason': 'LWT_DISCONNECT', 'producer': 'p3', 'seq': 1}
----------------------------------------------------------------------

```

```text
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>python matchmaker.py 
🔄 [MATCHMAKER] Iniciando loop do Matchmaker...
⚡ [MATCHMAKER] Conectado ao Broker MQTT com sucesso.
📌 [MATCHMAKER] Inscrito nos tópicos: 'rocketleague/matchmaking/fila' (QoS 1) e 'rocketleague/jogadores/+/status' (QoS 1)
🟢 [MATCHMAKER] Jogador 'p1' está online.
🎮 [MATCHMAKER] Jogador 'p1' entrou na fila. Fila atual: ['p1']
🟢 [MATCHMAKER] Jogador 'p2' está online.
🎮 [MATCHMAKER] Jogador 'p2' entrou na fila. Fila atual: ['p1', 'p2']
🚀 [MATCHMAKER] PARTIDA CRIADA! Sala #101 -> Jogadores: [p1, p2] | Tópico: 'rocketleague/partida/101/info' (Retained=True, QoS 1)
🟢 [MATCHMAKER] Jogador 'p3' está online.
🎮 [MATCHMAKER] Jogador 'p3' entrou na fila. Fila atual: ['p3']
💀 [MATCHMAKER] Jogador 'p3' ficou offline/desconectou! Removido da fila. Fila atual: []

```

```text
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>python server.py
⚡ [SERVER/JUIZ] Conectado ao Broker. Gerenciando Partida #101...
📌 [SERVER/JUIZ] Estado inicial publicado em 'rocketleague/partida/101/estado' (Retained=True, QoS 1): Placar 0x0
⚽ [SERVER/JUIZ] EVENTO DE GOL publicado em 'rocketleague/partida/101/eventos' com QoS 2 (Garantia de entrega sem perda/duplicação)!
📌 [SERVER/JUIZ] Estado do placar atualizado em 'rocketleague/partida/101/estado' (Retained=True, QoS 1): Placar 1x0
🏁 [SERVER/JUIZ] Evento de FIM DE JOGO publicado em 'rocketleague/partida/101/eventos' com QoS 2!
✅ [SERVER/JUIZ] Execução encerrada com sucesso.

```

```text
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>python player.py p1
⚡ [PLAYER: p1] Conectado ao Broker MQTT.
🟢 [PLAYER: p1] Status 'online' publicado (Retained=True, QoS 1).
🎯 [PLAYER: p1] Pedido de busca de partida enviado para a fila (QoS 1).
📌 [PLAYER: p1] Aguardando confirmação de partida em 'rocketleague/partida/+/info'...
🎉 [PLAYER: p1] PARTIDA ENCONTRADA! Alocado na Sala #101 com ['p1', 'p2']
🏎️ [PLAYER: p1] Iniciando streaming de telemetria (QoS 0) em 'rocketleague/partida/101/telemetria'...
📊 [PLAYER: p1] Telemetria #1/10 enviada | Vel: 58.9km/h | Boost: 36% (QoS 0)
📊 [PLAYER: p1] Telemetria #2/10 enviada | Vel: 61.0km/h | Boost: 9% (QoS 0)
📊 [PLAYER: p1] Telemetria #3/10 enviada | Vel: 98.5km/h | Boost: 90% (QoS 0)
📊 [PLAYER: p1] Telemetria #4/10 enviada | Vel: 68.5km/h | Boost: 49% (QoS 0)
📊 [PLAYER: p1] Telemetria #5/10 enviada | Vel: 113.6km/h | Boost: 65% (QoS 0)
📊 [PLAYER: p1] Telemetria #6/10 enviada | Vel: 81.6km/h | Boost: 98% (QoS 0)
📊 [PLAYER: p1] Telemetria #7/10 enviada | Vel: 108.5km/h | Boost: 62% (QoS 0)
📊 [PLAYER: p1] Telemetria #8/10 enviada | Vel: 93.8km/h | Boost: 35% (QoS 0)
📊 [PLAYER: p1] Telemetria #9/10 enviada | Vel: 42.7km/h | Boost: 92% (QoS 0)
📊 [PLAYER: p1] Telemetria #10/10 enviada | Vel: 71.5km/h | Boost: 31% (QoS 0)
✅ [PLAYER: p1] Streaming de telemetria concluído com sucesso!

```

```text
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>python player.py p2
⚡ [PLAYER: p2] Conectado ao Broker MQTT.
🟢 [PLAYER: p2] Status 'online' publicado (Retained=True, QoS 1).
🎯 [PLAYER: p2] Pedido de busca de partida enviado para a fila (QoS 1).
📌 [PLAYER: p2] Aguardando confirmação de partida em 'rocketleague/partida/+/info'...
🎉 [PLAYER: p2] PARTIDA ENCONTRADA! Alocado na Sala #101 com ['p1', 'p2']
🏎️ [PLAYER: p2] Iniciando streaming de telemetria (QoS 0) em 'rocketleague/partida/101/telemetria'...
📊 [PLAYER: p2] Telemetria #1/10 enviada | Vel: 52.0km/h | Boost: 76% (QoS 0)
📊 [PLAYER: p2] Telemetria #2/10 enviada | Vel: 85.2km/h | Boost: 99% (QoS 0)
📊 [PLAYER: p2] Telemetria #3/10 enviada | Vel: 46.4km/h | Boost: 85% (QoS 0)
📊 [PLAYER: p2] Telemetria #4/10 enviada | Vel: 90.2km/h | Boost: 73% (QoS 0)
📊 [PLAYER: p2] Telemetria #5/10 enviada | Vel: 60.9km/h | Boost: 48% (QoS 0)
📊 [PLAYER: p2] Telemetria #6/10 enviada | Vel: 77.5km/h | Boost: 46% (QoS 0)
📊 [PLAYER: p2] Telemetria #7/10 enviada | Vel: 49.9km/h | Boost: 37% (QoS 0)
📊 [PLAYER: p2] Telemetria #8/10 enviada | Vel: 106.6km/h | Boost: 46% (QoS 0)
📊 [PLAYER: p2] Telemetria #9/10 enviada | Vel: 108.6km/h | Boost: 16% (QoS 0)
📊 [PLAYER: p2] Telemetria #10/10 enviada | Vel: 59.1km/h | Boost: 74% (QoS 0)
✅ [PLAYER: p2] Streaming de telemetria concluído com sucesso!

```

```text
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\mqtt>python player.py p3
⚡ [PLAYER: p3] Conectado ao Broker MQTT.
🟢 [PLAYER: p3] Status 'online' publicado (Retained=True, QoS 1).
🎯 [PLAYER: p3] Pedido de busca de partida enviado para a fila (QoS 1).
📌 [PLAYER: p3] Aguardando confirmação de partida em 'rocketleague/partida/+/info'...

💥 [PLAYER: p3] Queda simulada por Ctrl+C! Encerrando processo abruptamente para acionar LWT no Broker...

```