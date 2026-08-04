---
document_id: FOUND-BISIMULATION-BOUNDARY-001-FINAL-DEFINITIONS
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
status: FROZEN
---

# Definições e assinaturas — finais

Congeladas pela revisão. Divergir exige gate próprio.

```lean
def Simulates (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, abstract (stepC c) = stepA (abstract c)

def Reflects (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, ∃ c' : C, stepC c = c' ∧ abstract c' = stepA (abstract c)

def Bisimulation (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  Simulates abstract stepC stepA ∧ Reflects abstract stepC stepA
```

## Tipos medidos por `#check`

```text
@Simulates    : {C : Type u} → {A : Type v} → (C → A) → (C → C) → (A → A) → Prop
@Reflects     : {C : Type u} → {A : Type v} → (C → A) → (C → C) → (A → A) → Prop
@Bisimulation : {C : Type u} → {A : Type v} → (C → A) → (C → C) → (A → A) → Prop
```

Zero typeclasses nos três.

## Os cinco teoremas

```lean
theorem simulates_iff_semiconj (abstract) (stepC) (stepA) :
    Simulates abstract stepC stepA ↔ Function.Semiconj abstract stepC stepA

theorem reflects_iff_simulates (abstract) (stepC) (stepA) :
    Reflects abstract stepC stepA ↔ Simulates abstract stepC stepA

theorem bisimulation_iff_semiconj (abstract) (stepC) (stepA) :
    Bisimulation abstract stepC stepA ↔ Function.Semiconj abstract stepC stepA

theorem bisimulation_does_not_reflect_cycles : ¬ (…)

theorem surjective_bisimulation_does_not_reflect_cycles : ¬ (…)
```

## A assinatura que carrega o conteúdo

```text
Reflects usa  ∃ c', stepC c = c' ∧ …
```

Verificado por `Iff.rfl` contra a forma existencial explícita. **Não**
pode ser simplificado para `∀ c, abstract (stepC c) = stepA (abstract c)`
sem destruir o resultado — `STOP-BIS-002`.

## Contagem congelada

```text
definicoes  3
teoremas    5
------------
total       8
```

## Fora da API

```text
boolToUnit_bisimulation           TEST_ONLY
forgetBool_surjective             TEST_ONLY
injective_bisimulation_reflects   DEFERRED_OPTIONAL, nao implementado
```
