# Guia de Execução - Sistema de Distribuição de Eventos MQTT

## 1. Pré-requisitos

Para executar a aplicação, certifique-se de possuir instalado no ambiente:

* Docker e Docker Compose
* Python 3.10 ou superior
* Biblioteca `paho-mqtt`

Caso precise instalar a biblioteca `paho-mqtt`, execute:

```bash
pip install paho-mqtt
```

---

## 2. Inicialização do Broker MQTT

A infraestrutura do Broker Mosquitto é gerenciada via Docker Compose.

1. Abra o terminal na raiz do projeto.
2. Inicie o container do Mosquitto em segundo plano:

```bash
docker compose up -d
```

3. Para verificar se o serviço está ativo e ouvindo na porta 1883, execute:

```bash
docker compose ps
```

---

## 3. Ordem Recomendada de Execução dos Processos

Para visualizar o fluxo completo de mensagens, retenção de estado e gerenciamento de filas, abra terminais distintos e execute os scripts na ordem abaixo:

### Passo 1: Dashboard e Auditoria

O dashboard monitora o ecossistema via tópicos coringa (`#`). Mantenha este terminal visível.

```bash
python dashboard.py
```

### Passo 2: Servidor do Matchmaker

O serviço de matchmaking intercepta os pedidos de entrada e aloca salas quando houver dois jogadores ativos.

```bash
python matchmaker.py
```

### Passo 3: Juiz/Servidor da Partida

Simula o gerenciamento da partida (placar, eventos críticos de gol e encerramento).

```bash
python server.py
```

### Passo 4: Clientes Jogadores (Publishers / Subscribers)

Abra terminais adicionais para simular os jogadores no sistema.

* Terminal 4 (Jogador 1):
```bash
python player.py p1
```

* Terminal 5 (Jogador 2):
```bash
python player.py p2
```

---

## 4. Teste do Cenário de Indisponibilidade (LWT)

Para testar a resiliência e o disparo do recurso *Last Will and Testament* (LWT) pelo Broker:

1. Em um novo terminal, inicie o Jogador 3:
```bash
python player.py p3
```

2. Observe que o Jogador 3 entra na fila de espera do matchmaking.
3. No terminal do `p3`, pressione `Ctrl+C` para encerrar o processo de forma abrupta.
4. Verifique nos logs do `dashboard.py` a recepção do evento de LWT com o status `offline`.
5. Verifique nos logs do `matchmaker.py` a remoção automática do `p3` da fila após a detecção da perda de conexão.

---

## 5. Encerramento do Ambiente

Após a realização dos testes, encerre os scripts Python nos seus respectivos terminais e execute o comando abaixo para interromper o Broker MQTT:

```bash
docker compose down
```