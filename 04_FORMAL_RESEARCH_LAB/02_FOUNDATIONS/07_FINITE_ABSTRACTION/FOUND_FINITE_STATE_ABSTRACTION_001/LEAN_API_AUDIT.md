---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-LEAN-API-AUDIT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Auditoria das APIs reutilizadas

Todas as assinaturas abaixo foram lidas por `lake env lean` contra o
repositório real, não citadas de memória.

## Mathlib

```text
@Function.Semiconj :
  {α : Type u_1} → {β : Type u_2} →
  (α → β) → (α → α) → (β → β) → Prop

@Function.Semiconj.iterate_right :
  ∀ {α β} {f : α → β} {ga : α → α} {gb : β → β},
    Function.Semiconj f ga gb →
      ∀ (n : ℕ), Function.Semiconj f ga^[n] gb^[n]

Function.Injective
Set.InjOn
Set.range
Set.mem_range_self
Nat.iterate                notacao f^[n]
```

## `TamesisLab.Engineering.FiniteStateEncoding`

```lean
structure CertifiedFiniteEncoding (S : Type*) (n : Nat) where
  encode : S → Fin n
  decode : Fin n → S
  decode_encode : ∀ s : S, decode (encode s) = s
  encode_decode : ∀ i : Fin n, encode (decode i) = i

def analyzeEncodedSystem (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) :
    Except RuntimeCycleError CycleWitness

theorem analyzeEncodedSystem_sound
    {encoding : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {witness : CycleWitness}
    (h : analyzeEncodedSystem encoding stepS start = .ok witness) :
    stepS^[witness.baseIndex + witness.period] start
      = stepS^[witness.baseIndex] start

theorem analyzeEncodedSystem_complete
    (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) :
    ∃ witness, analyzeEncodedSystem encoding stepS start = .ok witness

theorem analyzeEncodedSystem_ne_error
    (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) (err : RuntimeCycleError) :
    analyzeEncodedSystem encoding stepS start ≠ .error err
```

## `TamesisLab.Foundations.CycleDetection`

```lean
structure CycleWitness where
  baseIndex : ℕ
  period : ℕ
deriving DecidableEq, Repr, BEq
```

## `TamesisLab.Engineering.FiniteStateRuntime`

```lean
inductive RuntimeCycleError
deriving DecidableEq, Repr, BEq
```

Consumido apenas como tipo de erro do `Except`. Nenhum construtor é
criado, removido ou reinterpretado.

## Frentes que NÃO podem ser modificadas

```text
TamesisLab/Engineering/FiniteStateEncoding/
TamesisLab/Engineering/FiniteStateRuntime/
TamesisLab/Foundations/CycleDetection/
TamesisLab/Foundations/FunctionalGraphs/
TamesisLab/Foundations/Semigroups/
TamesisLab/RHNogo/
```

Esta frente **consome** essas APIs. Qualquer alteração nelas dispararia
`STOP-ABS-009`, `STOP-ABS-010` ou `STOP-ABS-011`.

## APIs deliberadamente NÃO usadas

```text
Fintype.equivFin        noncomputable, ja rejeitada na frente anterior
Function.periodicOrbit  noncomputable
Classical.choose        proibido para produzir dado
Setoid, Quotient        quocientes fora de escopo
SimpleGraph             fora de escopo
```
