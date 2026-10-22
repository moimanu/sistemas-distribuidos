## Logs Completos do Terminal

```bash
[moises@archlinux sistemas-distribuidos]$ python blockchain/main.py 
=== ESTADO INICIAL ===
Cadeia válida
Total de blocos: 20
Hash Bloco 5 Original: 475ee36a12f3049fe1cc5f9fb493e973c17f257c7235e97834f3cf310c7ac3d1

=== ADULTERAÇÃO SEM RECÁLCULO ===
Validação: Hash inválido no bloco 5
Hash Bloco 5 atual: 475ee36a12f3049fe1cc5f9fb493e973c17f257c7235e97834f3cf310c7ac3d1

=== ADULTERAÇÃO COM RECÁLCULO (FORGE) ===
Validação após recalcular tudo: Cadeia válida
Novo Hash Bloco 5: b06b8ac8f84052b071da188c54a6285f9f6473c62c246d002624986e4e498d51
Novo Hash Bloco 6 (afetado em cascata): 7271b88c0bb1ff9dcd8a17acd3989c17ee4e301bebedc39426021d853f77dbcf

=== RÉPLICAS DIVERGENTES ===
Hash topo Réplica A (Bloco 20): da241bd106f8641cef21fdb894092b38b2033627bb8bd60454e5b4e509c2d2d6
Hash topo Réplica B (Bloco 20): 4efc6e09c8e8ad92e32b7e3864fbabed17cf00149948a412a2dc57bb41c07489
```