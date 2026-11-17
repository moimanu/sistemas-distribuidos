# Contratos Inteligentes - Torneio Rocket League

Contrato inteligente em Solidity (`RocketLeagueTorneio`) para registro e finalização de partidas em rede EVM local (`Anvil`), com controle de acesso (`onlyOwner`), validação de estado e emissão de eventos.

---

## Documentação do Projeto

A documentação está organizada na pasta `docs/`:

* **[SCENARIO.md](docs/SCENARIO.md)**: Tabela consolidada dos testes automatizados e cenários de execução.
* **[LOGS.md](docs/LOGS.md)**: Evidências reais de compilação, testes, implantação local (`Anvil`), eventos e `revert`.
* **[ANALYSIS.md](docs/ANALYSIS.md)**: Riscos de segurança, comparação On-chain vs REST e respostas às questões de análise da AP8.

---

## Estrutura

* `src/RocketLeagueTorneio.sol`: Contrato com estado (`owner`, `totalPartidas`, `partidas`), duas funções de escrita (`criarPartida`, `finalizarPartida`), uma função `view` (`consultarPartida`) e dois eventos (`PartidaCriada`, `PartidaFinalizada`).
* `test/RocketLeagueTorneio.t.sol`: 5 testes automatizados cobrindo fluxo feliz, eventos e `revert`s esperados.
* `foundry.toml`: Configuração mínima do Foundry.

---

## Como Executar

Pré-requisito: [Foundry](https://getfoundry.sh/) (`forge`, `anvil`, `cast`).

```bash
cd contratos-inteligentes

# 1. Compilar e rodar testes automatizados
forge test -vvv

# 2. Subir nó local sem valor real (em outro terminal)
anvil

# 3. Implantar no nó local (conta padrão #0 do Anvil)
forge create src/RocketLeagueTorneio.sol:RocketLeagueTorneio \
  --rpc-url http://127.0.0.1:8545 \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
  --broadcast

# 4. Criar partida, finalizar, consultar estado e observar eventos
cast send <CONTRATO> "criarPartida(string)" "DFH Stadium" --rpc-url http://127.0.0.1:8545 --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
cast send <CONTRATO> "finalizarPartida(uint256,address)" 1 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 --rpc-url http://127.0.0.1:8545 --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
cast call <CONTRATO> "consultarPartida(uint256)(string,address,bool)" 1 --rpc-url http://127.0.0.1:8545
cast logs --address <CONTRATO> --from-block 0 --rpc-url http://127.0.0.1:8545
```

