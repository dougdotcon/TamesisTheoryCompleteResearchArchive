import TamesisLab.Foundations.ComputabilityBridge.Encoding

set_option autoImplicit false

/-!
# FOUND-COMPUTABILITY-BRIDGE-001 — a cota do certificado

```text
w.baseIndex + w.period <= n     o TESTEMUNHO cabe em n     PROVADO
a computacao custa n passos     AFIRMACAO DE CUSTO         PROIBIDA
```

A primeira é teorema. A segunda exigiria um modelo de máquina que o
laboratório não tem — ver `CB-GAP-002`.

## A duplicação, declarada

Esta frente mantinha a **terceira** ocorrência da mesma redução do bloco
`do`: a original é privada em `FiniteStateRuntime/DynamicAnalysis.lean`,
a segunda é privada em `Monovariants/WitnessBounds.lean`.

Reproduzir uma redução curta a partir de API exclusivamente pública é
permitido; reimplementar o detector não é, e não é feito aqui. A correção
própria — alargar `analyzeTransitionTable_sound` para devolver o contrato
`Valid` inteiro — toca frente encerrada e exige gate próprio:
`CB-GAP-004`.
-/

namespace TamesisLab.Foundations.ComputabilityBridge

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

variable {S : Type*} {n : Nat}

/-- **A cota, no nível da tabela.**

O certificado cabe no tamanho da tabela. Recuperada da terceira cláusula
de `CycleWitness.Valid`, que `analyzeTransitionTable_sound` perde. -/
theorem analyzeTransitionTable_bound {raw : RawTransitionTable} {start : Nat}
    {w : CycleWitness} (h : analyzeTransitionTable raw start = .ok w) :
    w.baseIndex + w.period ≤ raw.next.size :=
  (analyzeTransitionTable_rawValid h).2.2.1

/-- **A cota tipada**: o certificado cabe em `n`.

Cota do **certificado**, não de recursos. -/
theorem analyzeEncodedSystem_bound {e : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {w : CycleWitness}
    (h : analyzeEncodedSystem e stepS start = .ok w) :
    w.baseIndex + w.period ≤ n := by
  have hb : w.baseIndex + w.period ≤ (buildTransitionTable e stepS).next.size :=
    analyzeTransitionTable_bound h
  simpa using hb

end TamesisLab.Foundations.ComputabilityBridge
