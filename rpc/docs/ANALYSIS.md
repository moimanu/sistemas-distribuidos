# Tabela Comparativa entre Protocolos

| Critério | gRPC (AP4) | REST / HTTP (AP2) | MQTT (AP3) |
| --- | --- | --- | --- |
| **Modelo de Comunicação** | Requisição/Resposta e Streaming (Unidirecional e Bidirecional). | Requisição/Resposta síncrono clássico (Cliente-Servidor). | Publish/Subscribe assíncrono mediado por Broker. |
| **Protocolo de Transporte** | HTTP/2 (Multiplexado, conexões persistentes). | HTTP/1.1 ou HTTP/2. | TCP ou WebSockets. |
| **Formato de Payload** | Protocol Buffers (Binário de alto desempenho e ultra compacto). | JSON ou XML (Texto plano, mais verboso). | Binário livre / JSON. |
| **Acoplamento de Contrato** | **Forte**: Exige arquivo .proto compartilhado e compilação de Stubs. | **Fraco**: Esquema implícito ou documentação OpenAPI. | **Fraco**: Acoplamento apenas pelos tópicos de dados. |
| **Tratamento de Erros** | Status codes nativos e tipados (StatusCode). | Status HTTP padrão (2xx, 4xx, 5xx). | Controle por Níveis de QoS (0, 1, 2); sem erro de aplicação nativo. |
| **Caso de Uso Ideal** | Comunicação interna de alta velocidade entre microserviços e streaming em tempo real. | APIs públicas para navegadores e integrações web gerais. | Dispositivos IoT, conexões com restrição de banda e sensores instáveis. |