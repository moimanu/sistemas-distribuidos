# Guia de Execução - Sistema de Distribuição de Eventos gRPC

Este guia traz o passo a passo completo para configurar o ambiente, compilar os stubs do Protocol Buffers e executar a demonstração do sistema RPC em Python.

---

### Estrutura dos Arquivos do Projeto

Certifique-se de que todos os arquivos estejam no mesmo diretório:

```text
sistemas-distribuidos/rpc/
│
├── rocket_league.proto    # Definição das mensagens e serviços gRPC
├── servidor.py            # Implementação do servidor gRPC
└── cliente.py             # Script cliente e execução dos experimentos

```

---

1. **Instalar as dependências do gRPC:** Requer Python 3.8 ou superior.
Execute o comando abaixo no terminal para instalar a biblioteca de runtime do gRPC e a ferramenta de compilação de arquivos `.proto`:

```bash
pip install grpcio grpcio-tools

```

2. **Gerar os Stubs do gRPC:** Executar antes de iniciar servidor ou cliente.
Gere os arquivos Python a partir do contrato `rocket_league.proto`. Esse comando cria os módulos `rocket_league_pb2.py` (mensagens) e `rocket_league_pb2_grpc.py` (stubs de serviço):

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. rocket_league.proto

```

> **Verificação:** Certifique-se de que os dois arquivos gerados (`rocket_league_pb2.py` e `rocket_league_pb2_grpc.py`) apareceram na pasta do projeto.


3. **Inicializar o Servidor gRPC:** Manter este terminal aberto.
Abra um terminal e execute o servidor:

```bash
python servidor.py

```

**Saída esperada no terminal:**

```cmd
🚀 Servidor rodando na porta 50051...

```

4. **Executar o Cliente e os Experimentos:** Abrir um segundo terminal.
Com o servidor rodando, abra uma **nova janela do terminal**, navegue até a mesma pasta e execute o script do cliente:

```bash
python cliente.py

```

**O cliente executará sequencialmente:**

1. **Fluxo Normal:** Cadastro de jogador e envio de estatísticas (`OK`).
2. **Tratamento de Erros:** Validação de nickname vazio (`INVALID_ARGUMENT`) e ID inexistente (`NOT_FOUND`).
3. **Server Streaming:** Recepção contínua da telemetria da partida em tempo real.
4. **Teste Concorrente:** Chamadas simultâneas via `ThreadPoolExecutor`.
5. **Servidor Offline:** Tentativa de conexão na porta `50099` com estouro de prazo (`DEADLINE_EXCEEDED`).

---

### Resolução de Problemas Comuns

| Erro Observado | Causa Provável | Solução |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'rocket_league_pb2'` | Os stubs não foram gerados antes da execução. | Execute o passo 2 (`grpc_tools.protoc`) novamente. |
| `StatusCode.UNAVAILABLE` nas chamadas normais | O servidor não foi iniciado ou a porta está bloqueada. | Verifique se o `servidor.py` está rodando no terminal principal. |
| `AttributeError: module 'rocket_league_pb2' has no attribute...` | O arquivo `.proto` foi modificado mas não recompilado. | Re-execute o comando de compilação do Passo 2. |