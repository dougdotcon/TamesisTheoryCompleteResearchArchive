---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-OBSERVATIONAL-SOUNDNESS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
category: PUBLIC_SPECIFICATION_CORE
semantic_strength: OBSERVATIONAL_RECURRENCE
concludes_in: A
---

# Soundness observacional — final

## Assinatura medida por `#check`

```text
@analyzeAbstractSystem_observational_sound :
  ∀ {C : Type u_3} {A : Type u_4} {stepC : C → C} {stepA : A → A} {n : ℕ}
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C}
    {witness : CycleWitness},
  analyzeAbstractSystem abstraction encoding start = Except.ok witness →
    abstraction.abstract (stepC^[witness.baseIndex + witness.period] start) =
      abstraction.abstract (stepC^[witness.baseIndex] start)
```

## A verificação decisiva

A conclusão é

```text
abstraction.abstract (…) = abstraction.abstract (…)
```

Ambos os lados estão **sob `abstract`**. A igualdade vive em `A`. Não há
nenhuma leitura em que este teorema afirme igualdade entre os estados
concretos.

```text
STOP-ABS-004 disparada   NAO
```

## Hipóteses

```text
h : analyzeAbstractSystem … = .ok witness    unica
OrbitSeparating                              AUSENTE, corretamente
typeclasses                                  nenhuma
finitude de C                                nenhuma
```

A ausência de `OrbitSeparating` aqui é uma **propriedade**, não uma
omissão: o resultado observacional é gratuito, e é isso que o torna o
teorema central.

## DAG confirmado

```text
analyzeEncodedSystem_sound
  → igualdade entre iteradas de stepA
    → iterate_commutes, duas vezes
      → igualdade entre observacoes
```

Prova: duas reescritas e um `exact`. A casa dos pombos não é reaplicada;
o detector não é copiado; a tabela não é reaberta.

## Pegada

```text
[propext, Classical.choice, Quot.sound]
```

Herdada de `analyzeEncodedSystem`, em proposições apagadas na execução.
Nenhuma escolha clássica produz dado.
