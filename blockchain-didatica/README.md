# Blockchain Didática Distribuída

Esta é uma implementação minimalista de uma blockchain para fins acadêmicos, focada em demonstrar conceitos de hashing, encadeamento, Proof of Work (PoW) e consenso distribuído (resolução de forks).

## Pré-requisitos e Instalação

Certifique-se de ter o Python instalado. Instale as dependências:
```bash
pip install fastapi uvicorn requests pydantic
```

## Como Executar e Testar o Roteiro

Abra dois terminais para simular dois nós independentes.

**Terminal 1 (Nó 8001):**
```bash
python -m uvicorn node:app --port 8001
```

**Terminal 2 (Nó 8002):**
```bash
python -m uvicorn node:app --port 8002
```

### Passo a Passo (Demonstração e Logs)

**1. Minerar blocos no Nó 8001**
```bash
curl -X POST http://127.0.0.1:8001/mine -H "Content-Type: application/json" -d '{"origem":"Alice", "destino":"Bob", "valor":50.0}'
# Retorna o bloco minerado (com nonce e hash iniciando com 000)
```

**2. Adulteração Proposital (Nó 8001)**
```bash
curl -X POST http://127.0.0.1:8001/tamper
# Resposta: {"message": "Cadeia adulterada propositalmente..."}
curl -X GET http://127.0.0.1:8001/chain
# Resposta mostrará "is_valid": false
```

**3. Criando a Rede (Conectando 8001 e 8002)**
Reinicie o Nó 8001 para limpar a adulteração e minere um bloco nele. No Nó 8002, adicione o 8001 como peer:
```bash
curl -X POST http://127.0.0.1:8002/peers -H "Content-Type: application/json" -d '{"url":"http://127.0.0.1:8001"}'
```

**4. Fork Controlado e Reconciliação**
Minere **2 blocos** no Nó 8001. O Nó 8001 agora tem tamanho 3 (1 Gênese + 2 Minerados).
O Nó 8002 tem tamanho 1 (apenas Gênese). Existe um Fork!
Execute a reconciliação no Nó 8002:
```bash
curl -X GET http://127.0.0.1:8002/resolve
# Resposta esperada: {"message": "Cadeia substituída por uma válida e mais longa da rede.", "length": 3}
```
Se você desligar o Nó 8001 e rodar `/resolve` no 8002, o sistema não cai (ignora peer indisponível).

---

## Tabela de Limitações (Protótipo vs Blockchain Real)

| Funcionalidade | Este Protótipo (Didático) | Blockchain Real (Ex: Bitcoin/Ethereum) |
| :--- | :--- | :--- |
| **Identificação/Peers** | Descoberta manual via API (`POST /peers`). | Descoberta P2P automática (Gossip protocol). |
| **Transações** | JSON simples, sem autenticação. | Assinaturas digitais (ECDSA), validação estrita. |
| **Mempool** | Inexistente (perde transações em forks). | Fila de espera de transações, reprocessadas em reorg. |
| **Dificuldade PoW** | Fixa e estática (ex: 3 zeros). | Dinâmica, ajustada a cada X blocos baseada no tempo real de mineração. |
| **Segurança Sybil** | Nenhuma. API vulnerável a flood. | Custo econômico real de mineração inibe maioria dos ataques. |
| **Persistência** | Memória RAM (perde dados ao reiniciar). | Bancos de dados otimizados (LevelDB) em disco rígido. |