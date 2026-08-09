# Mapa Lean

Medida de rede real, Hamiltoniano de transferência, e reconstrução OS
seguem `NOT_FORMALIZED` — a frente exige infraestrutura de
probabilidade/análise que não foi construída nesta rodada.

Um esboço abstrato, autocontido, foi escrito nesta rodada (auditoria
`YM-LIMIT-001`, 2026-08-09):

- `FORMAL/InsufficiencyToyModel.lean` — dois contraexemplos de análise
  real elementar (`toyGap`, `toyFiniteVolumeGap`) que formalizam a
  estrutura lógica dos gaps `YM-GAP-001` e `YM-GAP-002`
  (`GAP_REGISTER.yaml`). **Não** registrado em `TamesisLab.lean`, **não**
  compilado nesta sessão (regra de isolamento da onda paralela — ver
  `PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`). Nomes de lema conferidos por
  grep contra o snapshot de Mathlib vendorizado, não por `lake build`.
  Sem `sorry`/`admit`/axioma local.
- O terceiro contraexemplo (operador de multiplicação, espectral) descrito
  em `COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md#contraexemplo-3` **não**
  foi formalizado — registrado como não tentado, motivo: infraestrutura de
  operadores/espectro em `L^2` fora do orçamento desta frente.

