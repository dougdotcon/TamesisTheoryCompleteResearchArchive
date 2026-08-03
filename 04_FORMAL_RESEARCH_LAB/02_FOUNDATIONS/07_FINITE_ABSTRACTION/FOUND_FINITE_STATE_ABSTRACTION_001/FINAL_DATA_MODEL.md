---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-DATA-MODEL
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
---

# Modelo de dados — final

Congelado pela revisão. Divergir desta assinatura na formalização exige
gate próprio.

```lean
structure CertifiedFiniteAbstraction
    (C A : Type*)
    (stepC : C → C)
    (stepA : A → A) where
  abstract : C → A
  commutes :
    Function.Semiconj abstract stepC stepA
```

## Tipo medido

```text
CertifiedFiniteAbstraction :
  (C : Type u_3) → (A : Type u_4) →
  (C → C) → (A → A) → Type (max u_3 u_4)
```

Lido por `#check`. Zero typeclasses no tipo.

## Campos

```text
abstract    dado        C → A
commutes    proposicao  Function.Semiconj abstract stepC stepA
```

Total: **dois**. Nenhum campo adicional é autorizado.

## Ausências verificadas

```text
CertifiedFiniteEncoding   ausente
estado inicial            ausente
CycleWitness              ausente
resultado da analise      ausente
Array                     ausente
tabela                    ausente
prova de OrbitSeparating  ausente
concretizacao A → C       ausente
```

## Separação abstração/codificação — confirmada

```text
abstracao      C → A       campo da estrutura
codificacao    A ≃ Fin n   argumento de analyzeAbstractSystem
```

A codificação **nunca** entra na estrutura. `#check @analyzeAbstractSystem`
confirma que `CertifiedFiniteEncoding A n` aparece como argumento
independente.

## Typeclasses — ausência confirmada por elaboração

```text
Fintype C, Finite C, DecidableEq C, Nonempty C, Inhabited C   ausentes
Fintype A, DecidableEq A                                       ausentes
```
