# FOUND-SEMIGROUP-001 — Hipóteses

## Hipóteses do modelo

1. Os regimes formam um tipo finito com igualdade decidível (`Regime3`,
   três construtores).
2. As transições formam um tipo finito com igualdade decidível (`Shift3`,
   três construtores).
3. A ação `Shift3.apply` é uma função total e determinística; não há
   não determinismo, probabilidade ou dinâmica contínua.
4. A composição `Shift3.comp` é dada por tabela finita explícita, com a
   convenção "aplicar o segundo argumento primeiro" (alinhada a `mul_smul`
   da Mathlib).

## O que não é assumido

- Nenhuma claim histórica do arquivo (TRI, TDTR, TOE, Omega, Braid, massa
  crítica) é usada como hipótese.
- Nenhuma correspondência entre este modelo e sistemas físicos é assumida.
- Nenhuma propriedade é herdada do benchmark LAB-BENCH-001: os tipos são
  redefinições independentes.
- Nenhum axioma local é introduzido; todas as leis são provadas por
  computação finita verificada pelo kernel.

## Fronteira de validade

Todos os teoremas valem para o modelo C3 concreto. FOUND-SG-013
(transitividade) e FOUND-SG-012 (fidelidade) são propriedades **deste**
modelo; os contraexemplos registrados no `README.md` mostram que não são
propriedades de sistemas de transição em geral.
