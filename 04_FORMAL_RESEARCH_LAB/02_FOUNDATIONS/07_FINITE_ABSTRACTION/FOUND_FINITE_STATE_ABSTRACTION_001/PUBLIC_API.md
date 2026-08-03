---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-PUBLIC-API
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: IMPLEMENTED
public_total: 7
counts_derived_by_script: true
typeclasses_required: 0
---

# API pública implementada

Sete declarações, contadas por script sobre os quatro módulos do núcleo.

## Executáveis — 2

```lean
structure CertifiedFiniteAbstraction (C A : Type*) (stepC : C → C) (stepA : A → A) where
  abstract : C → A
  commutes : Function.Semiconj abstract stepC stepA

def analyzeAbstractSystem
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C) :
    Except RuntimeCycleError CycleWitness
```

## Especificação — 5

```lean
theorem CertifiedFiniteAbstraction.iterate_commutes
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA) (k : Nat) (start : C) :
    abstraction.abstract ((stepC^[k]) start) = (stepA^[k]) (abstraction.abstract start)

theorem analyzeAbstractSystem_observational_sound
    {abstraction : …} {encoding : …} {start : C} {witness : CycleWitness}
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    abstraction.abstract ((stepC^[witness.baseIndex + witness.period]) start)
      = abstraction.abstract ((stepC^[witness.baseIndex]) start)

def OrbitSeparating (abstract : C → A) (stepC : C → C) (start : C) : Prop

theorem analyzeAbstractSystem_reflected_sound
    {…} (hSeparating : OrbitSeparating abstraction.abstract stepC start)
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    (stepC^[witness.baseIndex + witness.period]) start = (stepC^[witness.baseIndex]) start

theorem analyzeAbstractSystem_complete
    (abstraction : …) (encoding : …) (start : C) :
    ∃ witness, analyzeAbstractSystem abstraction encoding start = .ok witness
```

## Contagem

```text
declarada em FINAL_PUBLIC_API.md   7
derivada por script do codigo      7
divergencia                        0
```

## Onde cada uma vive

```text
Abstraction.lean       CertifiedFiniteAbstraction, iterate_commutes
AbstractAnalysis.lean  analyzeAbstractSystem, analyzeAbstractSystem_complete
Observation.lean       analyzeAbstractSystem_observational_sound
OrbitSeparation.lean   OrbitSeparating, analyzeAbstractSystem_reflected_sound
```

## Fora da API pública

```text
Counterexample.lean    10 declaracoes, TEST_ONLY
orbitSeparating_of_injective   reconstruido nos testes, DEFERRED_OPTIONAL
orbitSeparating_iff_injOn      nao implementado, DEFERRED_OPTIONAL
```

## Contrato

```text
typeclasses exigidas   0
finitude de C          nao exigida
DecidableEq            nao exigida
```

Verificado por varredura: nenhum `[Fintype`, `[Finite`, `[DecidableEq`,
`[Nonempty` ou `[Inhabited` nos módulos centrais.
