# Cliente e Servidor Socket de Serialização

Este projeto demonstra a comunicação via Sockets TCP entre um cliente e um servidor em Python, enviando o mesmo conjunto de dados em 5 formatos de serialização diferentes: **CSV**, **JSON**, **XML**, **YAML** e **TOML**.

---

## Estrutura do Projeto

* `cliente.py`: Coleta os dados do usuário no terminal, serializa as informações nos 5 formatos e envia ao servidor via socket.

* `servidor.py`: Escuta conexões na porta local `5000`, recebe as mensagens em sequência, desserializa cada formato e exibe os dados organizados.

---

## Requisitos

Antes de executar o projeto, instale as dependências externas para suporte a YAML e TOML:

```bash
pip install pyyaml toml

```

(As bibliotecas `csv`, `io`, `json`, `socket`, `time` e `xml.etree.ElementTree` já fazem parte da biblioteca padrão do Python).

---

## Como Executar

Para rodar o projeto, abra **dois terminais distintos**.

### 1. Iniciar o Servidor

No primeiro terminal, execute o script do servidor para aguardar conexões:

```bash
python servidor.py

```

### 2. Iniciar o Cliente

No segundo terminal, execute o script do cliente:

```bash
python cliente.py

```

---

## Fluxo de Funcionamento

1. O cliente solicita os seguintes dados no terminal: Nome, CPF, Idade e Mensagem.

2. O cliente conecta ao endereço `127.0.0.1` na porta `5000`.

3. Em seguida, os dados são convertidos e enviados sequencialmente nos formatos:

* CSV
* JSON
* XML
* YAML
* TOML

4. O servidor recebe cada pacote de texto, aplica a função correspondente de desserialização e imprime o resultado na tela.