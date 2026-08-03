---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-IMPORT-PLAN
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Plano de imports

## Import único do núcleo

```lean
import TamesisLab.Engineering.FiniteStateEncoding
```

Ele já traz, transitivamente:

```text
CertifiedFiniteEncoding
analyzeEncodedSystem e seus teoremas
CycleWitness
RuntimeCycleError
Function.Semiconj e iterate_right
```

O probe confirmou que **nenhum** import adicional é necessário para a
cadeia central.

## Proibidos

```text
Mathlib          (import total)
Mathlib.Tactic
SimpleGraph
Topology
MeasureTheory
Analysis
PDE
JSON
Parser
IO
Network
```

## Sobre `Set.InjOn`

A equivalência com `Set.InjOn` é `DEFERRED_OPTIONAL`, logo a API central
**não** importa infraestrutura de `Set` por causa dela. Caso um gate
futuro a promova, o import entra no módulo dela, nunca no núcleo.

## Organização modular planejada

```text
TamesisLab/Foundations/FiniteStateAbstraction/
  Abstraction.lean        estrutura e iterate_commutes
  AbstractAnalysis.lean   analyzeAbstractSystem e completeness
  Observation.lean        soundness observacional
  OrbitSeparation.lean    OrbitSeparating e reflexao
  Counterexample.lean     BOOL_TO_UNIT
  Audit.lean              #check das declaracoes publicas

TamesisLab/Foundations/FiniteStateAbstraction.lean   agregador
```

O agregador entra em `TamesisLab/Foundations.lean`. Os testes entram em
`TamesisLab.lean`, exceto a auditoria umbrella.
