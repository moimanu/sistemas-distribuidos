# Modelos de Falhas e Segurança em Sistemas Distribuídos

Este projeto implementa um laboratório prático para testes de resiliência, injeção de falhas controladas e mecanismos de segurança em serviços REST. A solução contempla a simulação de atrasos de rede, falhas transitórias, mecanismos de tratamento com retry e backoff exponencial, autenticação por token e controle de idempotência para chamadas de escrita.

---

## Documentação do Projeto

A documentação detalhada da aplicação está organizada na pasta `docs/`:

* **[LOGS.md](docs/LOGS.md)**: Saídas completas extraídas do terminal durante a execução da bateria de testes e experimentos de falhas e segurança.
* **[SCENARIO.md](docs/SCENARIO.md)**: Relatório experimental consolidado contendo os cenários de teste executados, detalhando as hipóteses, as falhas injetadas, os erros medidos, a classificação das falhas e o comportamento observado do cliente.
* **[RUNNING.md](docs/RUNNING.md)**: Documento que descreve como executar o projeto.

---

## Componentes Principais

* `main.py`: API desenvolvida em FastAPI que disponibiliza endpoints de negócios (gerenciamento de jogadores e partidas) e rotas para injeção controlada de falhas (atrasos artificiais e erros transitórios HTTP 503), além de controle de autenticação e suporte a chaves de idempotência.
* `cliente_experimentos.py`: Script cliente automatizado que executa a bateria de experimentos, implementando lógicas de *retry* com *backoff* exponencial e *jitter*, além de validar o comportamento da API sob cenários de timeout, falhas de segurança e envios duplicados.