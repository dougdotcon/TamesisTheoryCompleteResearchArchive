# Mapa Lean

Máquina de Turing, P/NP clássicos, e qualquer ponte de simulação
universal seguem `NOT_FORMALIZED` — deliberadamente fora do escopo desta
auditoria (ver `PNP-GAP-001`).

Um rascunho autocontido foi escrito e compilado nesta rodada (auditoria
`PVSNP-PHYS-001`, 2026-08-09):

- `FORMAL/PvsNPPhys.lean` — as definições internas `AffineBounded` e
  `SimEquivalent`, e duas propriedades estruturais triviais
  (reflexividade, simetria), sem dependência de Mathlib. Compilado
  (`lake env lean`, `exit 0`) na integração serial. **Não** registrado
  em `TamesisLab.lean`. Nada aqui decide, aproxima ou sugere resposta a
  P vs NP clássico.
