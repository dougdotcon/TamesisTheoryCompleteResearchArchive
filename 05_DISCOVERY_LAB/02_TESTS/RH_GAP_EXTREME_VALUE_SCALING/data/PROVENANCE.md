# Proveniência de dados — DISC-RH-GAP-EXTREME-VALUE-SCALING-001

## Dataset primário

Reaproveitado sem modificação de `../../RH_ZETA_ZEROS/data/zeros1.txt`
(100.000 primeiros zeros reais de ζ(s), Odlyzko) — mesma proveniência já
documentada em `../../RH_ZETA_ZEROS/data/PROVENANCE.md` (URL, checksum,
verificação de conteúdo). Nenhum novo download necessário.

## Dataset reservado para o Gate de Replicação

`zeros5.txt` (Odlyzko, zeros próximos de #10²², mesma fonte
`https://www-users.cse.umn.edu/~odlyzko/zeta_tables/`) — **explicitamente
NÃO baixado nem inspecionado nesta sessão**. Reservado para checagem de
robustez fora-do-regime no Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`
Seção 3, cláusula de fallback — este pré-registro não declara holdout
selado sobre `zeros1.txt`, então o Gate exige checagem contra fonte de
dado adicional). Mesmo padrão que funcionou em `DISC-RH-ZERO-GAP-RUNS-001`
(que usou `zeros4.txt`, regime #10²¹, ~15 ordens de magnitude acima do
primário).
