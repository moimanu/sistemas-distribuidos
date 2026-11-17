## Análise Técnica e Segurança (AP8)

### 1. Riscos de Segurança Analisados

1. **Quebra de Controle de Acesso (`onlyOwner`)**: Sem a verificação `msg.sender == owner`, qualquer endereço poderia criar partidas fictícias ou declarar a si mesmo como vencedor. **Mitigação**: modificador `onlyOwner` aplicado em `criarPartida` e `finalizarPartida`.
2. **Alteração Indevida ou Dupla Finalização de Estado**: Sem checar `!partida.finalizada` e `vencedor != address(0)`, um resultado já consolidado poderia ser sobrescrito ou anulado após o término da partida. **Mitigação**: `require` garantindo transição única (`criada -> finalizada`) e endereço válido.
3. **Crescimento Ilimitado / DoS por Gas**: Iterar sobre arrays crescentes on-chain pode ultrapassar o limite de gas do bloco (*block gas limit*). **Mitigação**: uso de `mapping(uint256 => Partida)` com acesso `O(1)` por `id`, sem loops.
4. **Centralização no `owner` (Risco de Confiança)**: Um único endereço `owner` pode falhar ou agir de forma maliciosa. Em produção, seria mitigado com multisig ou governança.

---

### 2. Comparação: Lógica On-Chain vs Serviço REST Tradicional

| Critério | Contrato Inteligente (On-Chain) | Serviço REST + Banco Tradicional |
| --- | --- | --- |
| **Confiança** | Regras auditáveis e executadas de forma determinística pela rede. | Depende integralmente do operador do servidor/banco. |
| **Custo por Escrita** | Consome gas por transação (ex.: `74.652` gas em `criarPartida`). | Custo fixo de infraestrutura, sem taxa por escrita. |
| **Latência e Throughput** | Limitado pelo tempo de bloco e consenso. | Baixa latência (milissegundos) e alta vazão. |
| **Privacidade** | Estado e histórico públicos no ledger. | Controle granular de acesso e sigilo de dados. |
| **Mutabilidade** | Código imutável após deploy; histórico verificável. | Fácil atualização de regras e correção de dados. |