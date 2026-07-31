import TamesisLab.Engineering.FiniteStateRuntime.RawTable
import TamesisLab.Engineering.FiniteStateRuntime.Validation
import TamesisLab.Engineering.FiniteStateRuntime.Execution
import TamesisLab.Engineering.FiniteStateRuntime.DetectorAdapter
import TamesisLab.Engineering.FiniteStateRuntime.DynamicAnalysis

/-!
# ENG-FINITE-STATE-RUNTIME-001 — agregador

Ponte executável e certificada entre dados dinâmicos e o detector de
ciclos já verificado.

```text
RawTable.lean          RawTransitionTable, Valid, ValidatedTransitionTable
Validation.lean        RuntimeCycleError e as duas validacoes
Execution.lean         step, step?, run? e a ponte de iteracoes
DetectorAdapter.lean   reutilizacao do detector, sem copia
DynamicAnalysis.lean   analyzeTransitionTable, soundness e completeness
```

O consumidor fornece `Array Nat` e `Nat`. Nenhuma typeclass é exigida
dele.

Destinos inválidos são **rejeitados**, nunca corrigidos. Não há módulo,
clamp nem valor padrão em ponto algum desta frente.

scientific_value: FORMAL_SOFTWARE_BRIDGE
mathematical_novelty: NONE
algorithmic_novelty: NONE
-/
