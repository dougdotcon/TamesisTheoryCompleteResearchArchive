---
document_id: ENC-IMPORT-PLAN
---

# Plano de imports

## Mínimo confirmado pelo probe

```lean
import TamesisLab.Engineering.FiniteStateRuntime
```

**Um único import** foi suficiente para os treze resultados. Ele já traz
transitivamente `Mathlib.Data.Fintype.Card`,
`Mathlib.Logic.Function.Iterate` e `TamesisLab.Foundations.CycleDetection`.

`Array.ofFn`, `Array.size_ofFn`, `Array.getElem_ofFn`, `Fin.cast`,
`Fin.isLt`, `Fin.ext`, `Option.some.inj`, `Function.LeftInverse.injective`
e `Function.Semiconj.iterate_right` estavam todos disponíveis sem import
adicional.

## Namespace obrigatório

```lean
open TamesisLab.Engineering.FiniteStateRuntime
```

Achado do probe, e não trivial: sem esta linha, **toda** referência a
`ValidatedTransitionTable.step`, `.next`, `.toRaw` e
`analyzeTransitionTable` falha com *"Invalid field notation"*. Custou a
primeira execução inteira do probe.

O namespace próprio da frente será
`TamesisLab.Engineering.FiniteStateEncoding`.

## Não importar

```text
Mathlib               (o guarda-chuva inteiro)
Mathlib.Tactic
Mathlib.Data.Fintype.EquivFin
SimpleGraph, Topology, MeasureTheory, Analysis, PDE
JSON, Parser, IO, Network
```

`Mathlib.Data.Fintype.EquivFin` merece menção explícita: ele **não** é
necessário, e importá-lo tornaria `Fintype.equivFin` acessível — a única
API que esta frente rejeitou por ser `noncomputable`. Mantê-lo fora é uma
barreira, não uma economia.

## Módulos planejados

```text
TamesisLab/Engineering/FiniteStateEncoding/Encoding.lean
TamesisLab/Engineering/FiniteStateEncoding/TableConstruction.lean
TamesisLab/Engineering/FiniteStateEncoding/TableIndex.lean
TamesisLab/Engineering/FiniteStateEncoding/Commutation.lean
TamesisLab/Engineering/FiniteStateEncoding/RawCorrespondence.lean
TamesisLab/Engineering/FiniteStateEncoding/TypedAnalysis.lean
TamesisLab/Engineering/FiniteStateEncoding.lean          (agregador)
TamesisLab/Engineering/FiniteStateEncoding/Audit.lean
```

Nomes **não** congelados: pertencem ao gate de especificação-review e ao
de formalização. Registrados aqui apenas como plano.

Lição herdada de `CD-GAP-018` e `RT-GAP-018`: um teste que importa a raiz
`TamesisLab` **não** pode ser registrado em `TamesisLab.lean` — o import
seria circular.
