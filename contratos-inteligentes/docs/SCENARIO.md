## Tabela de Cenários e Testes

| Cenário / Teste | Ação Realizada | Resultado Observado | Status |
| --- | --- | --- | --- |
| **Criar e Consultar** | `owner` chama `criarPartida("DFH Stadium")` e `consultarPartida(1)`. | Partida criada com `id = 1`, evento `PartidaCriada` emitido e leitura `view` consistente (`94038` gas). | Passou |
| **Finalizar Partida** | `owner` chama `finalizarPartida(1, JOGADOR)`. | Vencedor registrado, `finalizada = true` e evento `PartidaFinalizada` emitido (`144881` gas). | Passou |
| **Controle de Acesso** | `INTRUSO` tenta chamar `criarPartida("Utopia Coliseum")`. | Transação revertida com `"Apenas owner"` (`33909` gas). | Passou (Revert) |
| **Validação de Entrada** | `owner` tenta chamar `criarPartida("")`. | Transação revertida com `"Arena vazia"` (`33114` gas). | Passou (Revert) |
| **Dupla Finalização** | `owner` tenta finalizar partida já finalizada. | Transação revertida com `"Partida ja finalizada"` (`164848` gas). | Passou (Revert) |

