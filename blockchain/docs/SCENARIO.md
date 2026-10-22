## Tabela de Experimentos

| Experimento | Ação Realizada | Resultado Observado | Status de Validação |
| --- | --- | --- | --- |
| **Geração de Blocos** | Inserção de 19 transações (trade) + Bloco Gênesis (20 blocos totais). | Encadeamento progressivo validado através da relação `previous_hash`. | Válido |
| **Adulteração Simples** | Modificação do item `"Batmobile"` para `"Fake Alpha Boost"` no Bloco 5. | Quebra da integridade detectada na verificação de avalanche. O hash recalculado diferiu do hash armazenado.| Inválido (Hash incorreto) |
| **Falsificação (Forge)** | Recálculo de todos os hashes e `previous_hashes` do Bloco 5 até o 19. | A cadeia assumiu os dados fraudulentos de forma íntegra localmente, reestabelecendo as ligações criptográficas. | Válido (Local) |
| **Bifurcação (Fork)** | Clona-se a cadeia em duas réplicas (A e B). Cada uma processa um bloco 20 diferente simultaneamente. | Ambas as cadeias são validadas internamente com perfeição. Hashes de topo divergiram (`da24...` vs `4efc...`). | Válido (Local em ambas) |
