# Diagrama da Arquitetura MQTT

Este documento descreve a topologia de comunicação distribuída do projeto utilizando o protocolo MQTT (Eclipse Mosquitto). A arquitetura foi desenhada para suportar comunicação em tempo real entre clientes jogadores, serviços de backend e ferramentas de auditoria através do padrão Pub/Sub.

---

## Visão Geral do Sistema

```mermaid
graph TD
    %% Nós de Agentes/Serviços
    subgraph Clients["Clientes"]
        P1["Jogador 1 (player.py)"]
        P2["Jogador 2 (player.py)"]
    end

    subgraph Infrastructure["Infraestrutura de Mensageria"]
        Broker[("Broker MQTT\n(Mosquitto)")]
    end

    subgraph Backend["Serviços de Backend"]
        MM["Matchmaker (matchmaker.py)"]
        SRV["Juiz / Servidor (server.py)"]
        DASH["Dashboard / Audit (dashboard.py)"]
    end

    %% Fluxo de Matchmaking e Entrada
    P1 -->|"Fila / Matchmaking"| Broker
    P2 -->|"Fila / Matchmaking"| Broker
    Broker <-->|"Lê Fila / Cria Sala"| MM

    %% Fluxo de Partida e Telemetria
    P1 -->|"Telemetria / LWT"| Broker
    P2 -->|"Telemetria / LWT"| Broker
    Broker <-->|"Placar / Gols / Eventos"| SRV

    %% Observabilidade / Auditoria
    Broker -->|"Tópicos Wildcard (#)"| DASH

    %% Estilização
    style Broker fill:#1f2937,stroke:#60a5fa,stroke-width:2px,color:#fff
    style DASH fill:#111827,stroke:#9ca3af,stroke-width:1px,color:#fff