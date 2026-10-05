# Laboratório de Falhas e Segurança em Sistemas Distribuídos

Esta pasta contém o laboratório prático para testes de resiliência, injeção de falhas controladas e segurança em serviços REST.

## Como Executar

### 1. Iniciar o Servidor da API com Injeção de Falhas
```bash
python -m uvicorn main:app --reload
```

### 2. Executar a Bateria Automatizada de Experimentos

Em outro terminal, execute:

```bash
python cliente_experimentos.py
```