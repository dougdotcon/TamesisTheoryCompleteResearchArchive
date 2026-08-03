---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-ORBIT-SEPARATION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
primary_public_contract: OrbitSeparating
set_injon_equivalence: DEFERRED_OPTIONAL
non_tautological: true
---

# `OrbitSeparating` — final

## Definição congelada

```lean
def OrbitSeparating
    (abstract : C → A)
    (stepC : C → C)
    (start : C) : Prop :=
  ∀ i j : Nat,
    abstract ((stepC^[i]) start) =
      abstract ((stepC^[j]) start) →
    (stepC^[i]) start =
      (stepC^[j]) start
```

Tipo medido:

```text
@OrbitSeparating :
  {C : Type u_3} → {A : Type u_4} →
  (C → A) → (C → C) → C → Prop
```

Zero typeclasses. Zero axiomas.

## Não tautologicidade — prova positiva

```lean
theorem boolToUnit_not_orbitSeparating :
    ¬ OrbitSeparating forgetBool concreteStep false
```

`does not depend on any axioms`.

O argumento é conclusivo: a semiconjugação **vale** em `BOOL_TO_UNIT`.
Se `OrbitSeparating` decorresse da semiconjugação, valeria ali. Ela
falha ali. Logo é uma hipótese genuinamente adicional.

```text
STOP-ABS-006 disparada   NAO
```

## Quantificação — verificada

```text
sobre TODOS os pares i, j          SIM
sobre apenas baseIndex e period    NAO
```

A conclusão da reflexão usa **um** par. A hipótese fornece **todos**. A
implicação é estrita, não uma reescrita da conclusão.

## Satisfazibilidade

```lean
theorem orbitSeparating_of_injective
    {abstract : C → A} (hinj : Function.Injective abstract)
    (stepC : C → C) (start : C) :
    OrbitSeparating abstract stepC start
```

Sem axiomas. A condição não é vazia.

## `Set.InjOn` — decisão final

```lean
theorem orbitSeparating_iff_injOn (abstract) (stepC) (start) :
    OrbitSeparating abstract stepC start
      ↔ Set.InjOn abstract (Set.range fun k : Nat => (stepC^[k]) start)
```

Compila. Sem axiomas.

```yaml
primary_public_contract: OrbitSeparating
Set.InjOn_equivalence: DEFERRED_OPTIONAL
```

Razão da recusa apesar da evidência favorável: nenhum resultado central
a consome, e a regra da frente é escolher a API menor. Publicá-la
obrigaria o núcleo a carregar `Set`, `Set.range` e `Set.InjOn` para
servir a nenhum consumidor.

Ela é reconstruível em três linhas por qualquer gate futuro que a
precise.
