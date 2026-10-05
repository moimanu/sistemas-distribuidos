# Relatório Experimental - Modelos Fundamentais (Interação, Falhas e Segurança)

## 1. Tabela de Cenários Experimentais Executados

| ID | Hipótese Experimental | Falha Injetada | Observação / Erro Medido | Classificação da Falha | Conclusão / Ação do Cliente |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **CEN-01** | Operação normal responde em menos de 50ms. | Nenhuma (Referência). | Resposta HTTP 200 OK em 8.2ms. | Sem falha. | Requisição processada com sucesso na primeira tentativa. |
| **CEN-02** | O estouro de timeout impede espera indefinida, mas não confirma se o servidor caiu. | Atraso artificial de 1000ms no servidor (timeout cliente = 300ms). | Capturado `requests.exceptions.Timeout` após 300ms. | **Falha de Temporização** | O cliente cancelou a chamada operacionalmente; o servidor pode ter processado a chamada normalmente. |
| **CEN-03** | Retries com backoff exponencial recuperam requisições impactadas por falhas transitórias. | Servidor retorna HTTP 503 com 70% de probabilidade. | Falha na 1ª tentativa; sucesso obtido no retry após backoff de 0.28s. | **Falha de Omissão / Resposta** | O backoff evitou sobrecarga e a requisição foi recuperada com sucesso. |
| **CEN-04** | Requisições sem token de segurança são rejeitadas na fronteira do serviço. | Envio de POST sem o cabeçalho `X-API-Token`. | Erro HTTP 401 Unauthorized capturado na 1ª tentativa. | **Quebra de Autenticidade / Autorização** | A camada de segurança bloqueou o acesso sem realizar retries desnecessários. |
| **CEN-05** | Retries em requisições POST criam registros duplicados a menos que protegidas por chave de idempotência. | Reenvio da mesma requisição POST de cadastro de partida. | Sem chave: 2 partidas criadas. Com chave: a 2ª chamada retornou o cache da 1ª. | **Efeito Adverso de Retry (Duplicação)** | Uso de `X-Idempotency-Key` garantiu idempotência em comando de escrita. |