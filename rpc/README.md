# Sistema de Distribuição de Eventos RPC - Rocket League

Este projeto implementa uma arquitetura para um ambiente de jogos multiplayer inspirado em Rocket League, utilizando o protocolo gRPC.

---

## Documentação do Projeto

A documentação detalhada da aplicação está organizada na pasta `docs/`:

* **[RUNNING.md](docs/RUNNING.md)**: Instruções passo a passo para execução dos scripts Python.
* **[LOGS.md](docs/LOGS.md)**: Saídas completas extraídas dos terminais durante os testes de execução.
* **[SCENARIO.md](docs/SCENARIO.md)**: Tabela consolidada com todos os cenários de teste executados, detalhando o comportamento esperado e os resultados observados.
* **[ANALYSIS.md](docs/ANALYSIS.md)**: Análise comparativa entre arquitetura distribuída com MQTT, REST e gRPC.

---

## Componentes Principais

* `server.py`: Servidor.
* `player.py`: Cliente, contendo o fluxo de execução dos testes.
* `rocket_league.proto`: Contrato do gRPC.