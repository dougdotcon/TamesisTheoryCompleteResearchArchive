---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-REFLECTED-SOUNDNESS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
category: PUBLIC_SPECIFICATION_CORE
concludes_in: C
requires_hypothesis: OrbitSeparating
---

# Soundness concreta refletida — final

## Assinatura medida por `#check`

```text
@analyzeAbstractSystem_reflected_sound :
  ∀ {C : Type u_3} {A : Type u_4} {stepC : C → C} {stepA : A → A} {n : ℕ}
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C}
    {witness : CycleWitness},
  OrbitSeparating abstraction.abstract stepC start →
    analyzeAbstractSystem abstraction encoding start = Except.ok witness →
      stepC^[witness.baseIndex + witness.period] start =
        stepC^[witness.baseIndex] start
```

## A verificação decisiva

`OrbitSeparating abstraction.abstract stepC start` aparece **na
assinatura**, como hipótese explícita, antes da hipótese de execução.

```text
escondida na estrutura   NAO
instancia                NAO
autoParam                NAO
derivada                 NAO

STOP-ABS-005 disparada   NAO
```

## Conclusão

```text
stepC^[…] start = stepC^[…] start
```

Sem `abstract`. A igualdade vive em `C`. Esta é a **única** declaração
pública da frente que conclui em `C`, e ela paga com a hipótese.

## DAG confirmado

```text
analyzeAbstractSystem_observational_sound
  → hSeparating (baseIndex + period) baseIndex
    → igualdade concreta
```

Um termo. Nenhuma tática.

## Força da hipótese

```text
exigida       separacao sobre a orbita alcancada a partir de start
NAO exigida   injetividade global
NAO exigida   finitude de C
NAO exigida   DecidableEq C
```

`orbitSeparating_of_injective` mostra que injetividade global seria
suficiente — e, portanto, que exigi-la seria escolher a hipótese mais
forte quando a mais fraca basta.

## Pegada

```text
[propext, Classical.choice, Quot.sound]
```

Toda herdada da cadeia anterior.
