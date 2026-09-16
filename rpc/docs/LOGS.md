# Logs Completos do Terminal

### servidor.py
```cmd
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\rpc>python servidor.py
🚀 Servidor rodando na porta 50051...
[SERVIDOR] Reg. OK -> ID 1 | Nick: moimanu
[SERVIDOR] Stats salvos -> ID 1 | Gols: 3
[SERVIDOR - ERRO] Nickname inválido (vazio).
[SERVIDOR - ERRO] ID 9999 não encontrado.
[SERVIDOR - STREAM] Transmitindo partida ID 101...
[SERVIDOR] Reg. OK -> ID 2 | Nick: Bot_1
[SERVIDOR] Reg. OK -> ID 3 | Nick: Bot_2
[SERVIDOR] Reg. OK -> ID 4 | Nick: Bot_3
[SERVIDOR] Reg. OK -> ID 5 | Nick: Bot_4
[SERVIDOR] Reg. OK -> ID 6 | Nick: Bot_5
[SERVIDOR] Reg. OK -> ID 7 | Nick: Bot_6
[SERVIDOR] Reg. OK -> ID 8 | Nick: Bot_7
[SERVIDOR] Reg. OK -> ID 9 | Nick: Bot_8
[SERVIDOR] Reg. OK -> ID 10 | Nick: Bot_9
[SERVIDOR] Reg. OK -> ID 11 | Nick: Bot_10
```

### cliente.py

```cmd
C:\Users\moise\Documents\GitHub\sistemas-distribuidos\rpc>python cliente.py

--- Cadastrar Jogador (moimanu) ---
Sucesso! ID: 1 | Retorno: Jogador 'moimanu' (XP: 150) registrado com sucesso! [5.62ms]

--- Enviar Stats (ID: 1) ---
Sucesso! Estatísticas vinculadas à temporada com sucesso. [0.64ms]

--- Cadastrar Jogador () ---
Erro RPC [StatusCode.INVALID_ARGUMENT]: O nickname do jogador não pode ser vazio. [0.59ms]

--- Enviar Stats (ID: 9999) ---
Erro [StatusCode.NOT_FOUND]: Jogador ID 9999 não localizado. [0.61ms]

--- Telemetria da Partida #101 ---
[10s] Azul 0 x 0 Laranja | Evento: [Partida #101] Kickoff inicial executado.
[45s] Azul 1 x 0 Laranja | Evento: [Partida #101] Gol de Kickoff! Marca Time Azul.
[120s] Azul 1 x 1 Laranja | Evento: [Partida #101] Gol de Chute Aéreo! Marca Time Laranja.
[240s] Azul 2 x 1 Laranja | Evento: [Partida #101] Defesa Épica e Gol do Time Azul!
[300s] Azul 2 x 1 Laranja | Evento: [Partida #101] Fim de jogo! Vitória do Time Azul.
Transmissão encerrada. [2504.33ms]

--- Teste Concorrente (10 reqs / 4 workers) ---
[Thread #01] Sucesso -> ID: 2 [1.51ms]
[Thread #02] Sucesso -> ID: 3 [1.54ms]
[Thread #03] Sucesso -> ID: 4 [1.42ms]
[Thread #04] Sucesso -> ID: 5 [1.37ms]
[Thread #05] Sucesso -> ID: 6 [1.16ms]
[Thread #06] Sucesso -> ID: 7 [1.12ms]
[Thread #07] Sucesso -> ID: 8 [1.09ms]
[Thread #08] Sucesso -> ID: 9 [0.92ms]
[Thread #09] Sucesso -> ID: 10 [0.92ms]
[Thread #10] Sucesso -> ID: 11 [0.86ms]

--- Teste Servidor Offline (localhost:50099) ---
Capturado com sucesso: Status StatusCode.DEADLINE_EXCEEDED [1004.02ms]

C:\Users\moise\Documents\GitHub\sistemas-distribuidos\rpc>
```