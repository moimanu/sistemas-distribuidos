## Logs Completos do Terminal

### 1. Compilação e Testes Automatizados (`forge test -vvv`)

```text
Compiler run successful!

Ran 5 tests for test/RocketLeagueTorneio.t.sol:RocketLeagueTorneioTest
[PASS] testCriarEConsultarPartida() (gas: 94038)
[PASS] testFinalizarPartidaEmiteEvento() (gas: 144881)
[PASS] testReverteAoFinalizarDuasVezes() (gas: 164848)
[PASS] testReverteQuandoArenaVazia() (gas: 33114)
[PASS] testReverteQuandoNaoOwnerCriaPartida() (gas: 33909)
Suite result: ok. 5 passed; 0 failed; 0 skipped; finished in 1.13ms (1.41ms CPU time)
```

### 2. Implantação Local no Anvil (`forge create`)

```text
Deployer: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
Transaction hash: 0x7edb31001d4acc457764cbaf596c9d0f51079deca83738215bf52b0bedfc3c8a
```

### 3. Transações, Consulta `view` e Eventos (`cast`)

```text
# criarPartida("DFH Stadium")
txHash:  0x6fe48dfa0ab1dd6b51b4e0887a411d441f838823903229baf8911ba27008f279
gasUsed: 74652
status:  1 (success)

# finalizarPartida(1, 0x70997970C51812dc3A010C7d01b50e0d17dc79C8)
txHash:  0x0a297675e92af7f45919073ef40c2a911262228b15a1d62b6c9988f10b57d8b2
gasUsed: 51008
status:  1 (success)

# consultarPartida(1) (view call - 0 gas)
"DFH Stadium"
0x70997970C51812dc3A010C7d01b50e0d17dc79C8
true
```

### 4. Logs Observados (`cast logs`)

```text
- address: 0x5FbDB2315678afecb367f032d93F642f64180aa3
  blockNumber: 2
  topics: [
    0x636fd3d1c7cf97a957167ddd57b2be9e228296392fd559c504dbc8757b2d99bb, # PartidaCriada
    0x0000000000000000000000000000000000000000000000000000000000000001  # id = 1
  ]
  transactionHash: 0x6fe48dfa0ab1dd6b51b4e0887a411d441f838823903229baf8911ba27008f279

- address: 0x5FbDB2315678afecb367f032d93F642f64180aa3
  blockNumber: 3
  topics: [
    0x6f1820f0e11889c3aea65674778fb73c67284d167364b5cf5f6d9b64a22f8d01, # PartidaFinalizada
    0x0000000000000000000000000000000000000000000000000000000000000001, # id = 1
    0x00000000000000000000000070997970c51812dc3a010c7d01b50e0d17dc79c8  # vencedor
  ]
  transactionHash: 0x0a297675e92af7f45919073ef40c2a911262228b15a1d62b6c9988f10b57d8b2
```

### 5. Tentativa Inválida (`revert` confirmado)

```text
Error: Failed to estimate gas: server returned an error response: error code 3: execution reverted: Apenas owner
```

