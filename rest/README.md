## Como Executar a API

### Pré-requisitos
- Python 3.10 ou superior instalado na máquina.

---

### 1. Clonar ou Acessar a Pasta do Projeto
Navegue até o diretório onde o código está localizado no seu terminal:
```bash
cd caminho/para/rest

```

---

### 2. Configurar o Ambiente Virtual (.venv)

O ambiente virtual é utilizado para isolar as dependências do projeto e evitar conflitos com outros pacotes do sistema.

#### No Windows (PowerShell):

```powershell
# 1. Permite a execução de scripts no PowerShell para a sessão atual
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 2. Cria o ambiente virtual na pasta .venv
python -m venv .venv

# 3. Ativa o ambiente virtual
.\.venv\Scripts\Activate.ps1

```

#### No Linux / macOS:

```bash
# 1. Cria o ambiente virtual
python3 -m venv .venv

# 2. Ativa o ambiente virtual
source .venv/bin/activate

```

> **Nota:** Ao ativar o ambiente, o prefixo `(.venv)` passará a ser exibido no seu terminal.

---

### 3. Instalar as Dependências

Com o ambiente virtual ativado `(.venv)`, instale o FastAPI e o cliente HTTP Requests:

```bash
pip install "fastapi[standard]" requests

```

---

### 4. Executar o Servidor da API

Inicie o servidor de desenvolvimento com o FastApi CLI:

```bash
fastapi dev main.py

```

Ou utilizando diretamente o Uvicorn:

```bash
python -m uvicorn main:app --reload

```

A API estará acessível em: `http://127.0.0.1:8000`

A documentação interativa (Swagger) estará disponível em: `http://127.0.0.1:8000/docs`

---

## Mapeamento de Endpoints e Semântica HTTP

| Método | Caminho (URI) | Descrição da Operação | Status Esperado | Status de Erro | Idempotente? |
| --- | --- | --- | --- | --- | --- |
| **GET** | `/jogadores` | Listar todos os jogadores | 200 OK | — | Sim |
| **POST** | `/jogadores` | Cadastrar novo jogador | 201 Created (+ Header Location) | 409 Conflict (nickname duplicado), 422 Unprocessable | Não |
| **GET** | `/jogadores/{jogador_id}` | Buscar detalhes do jogador | 200 OK | 404 Not Found | Sim |
| **PUT** | `/jogadores/{jogador_id}` | Atualizar dados do jogador | 200 OK | 404 Not Found, 409 Conflict | Sim |
| **DELETE** | `/jogadores/{jogador_id}` | Remover jogador e seu histórico | 204 No Content | 404 Not Found | Sim |
| **POST** | `/jogadores/{jogador_id}/partidas` | Registrar partida do jogador | 201 Created | 404 Not Found (jogador inexistente), 422 Unprocessable | Não |
| **GET** | `/jogadores/{jogador_id}/partidas` | Listar partidas do jogador | 200 OK | 404 Not Found | Sim |

```