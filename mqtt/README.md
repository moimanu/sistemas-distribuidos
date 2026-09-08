# Sistema de Distribuição de Eventos MQTT - Rocket League

Este projeto implementa uma arquitetura orientada a eventos para um ambiente de jogos multiplayer inspirado em Rocket League, utilizando o protocolo MQTT (Eclipse Mosquitto). A solução contempla gerenciamento de estado de jogadores, fila de matchmaking, arbitragem de partidas, streaming de telemetria e auditoria de tráfego.

---

## Documentação do Projeto

A documentação detalhada da aplicação está organizada na pasta `docs/`:

* **[RUNNING.md](docs/RUNNING.md)**: Instruções passo a passo para subida da infraestrutura com Docker e ordem recomendada de execução dos scripts Python.
* **[DIAGRAM.md](docs/DIAGRAM.md)**: Representação visual da arquitetura em sintaxe Mermaid, ilustrando componentes, fluxos de dados, níveis de QoS e mensagens retidas.
* **[LOGS.md](docs/LOGS.md)**: Tabela cronológica dos eventos capturados pelo dashboard e saídas completas extraídas dos terminais durante os testes de execução e resiliência (LWT).
* **[SCENARIO.md](docs/SCENARIO.md)**: Tabela consolidada com todos os cenários de teste executados, detalhando o comportamento esperado, os níveis de Qualidade de Serviço (QoS) empregados, o mecanismo de retenção de estado e os resultados observados.

---

## Componentes Principais

* `dashboard.py`: Serviço de auditoria que assina todos os tópicos (`#`) para monitoramento centralizado.
* `matchmaker.py`: Serviço responsável pelo pareamento de jogadores e criação de salas de partida.
* `server.py`: Simula o juiz da partida, publicando eventos críticos (gols, encerramento) e atualizações de placar.
* `player.py`: Script do cliente jogador que simula entrada na fila, recepção de partida e streaming de telemetria.