# Ledger Distribuído em Blockchain - Rocket League

Este projeto implementa uma estrutura de encadeamento criptográfico de blocos (*blockchain*) para auditoria e registro imutável de trocas de itens inspiradas em Rocket League. A solução contempla a criação de blocos encadeados por hashes SHA-256, validação de integridade da cadeia e simulações de adulteração de dados, falsificação (*forge*) e bifurcações (*fork*).

---

## Documentação do Projeto

A documentação detalhada da aplicação está organizada na pasta `docs/`:

* **[DIAGRAM.md](docs/DIAGRAM.md)**: Representação visual em Mermaid da divergência de réplicas e bifurcação (*fork*).
* **[LOGS.md](docs/LOGS.md)**: Saídas completas capturadas do terminal durante a execução dos experimentos de validação e adulteração.
* **[SCENARIO.md](docs/SCENARIO.md)**: Tabela consolidada dos cenários de teste executados, detalhando as ações, resultados observados e estados de validação da cadeia.

---

## Componentes Principais

* `main.py`: Contém a definição das estruturas de dados (`TradeEvent`, `Block`), o gerenciador da cadeia (`RocketLeagueLedger`) com métodos para criação de bloco gênesis, adição de transações e validação de consistência, além dos experimentos práticos simulados no terminal.

---

## Como Executar

O projeto utiliza exclusivamente a biblioteca padrão do Python (Python 3.10+):

```bash
# Acessar a pasta do projeto
cd blockchain

# Executar a simulação
python main.py
```
