---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-ORBIT-SEPARATION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
primary_public_contract: OrbitSeparating
set_injon_equivalence: DEFERRED_OPTIONAL
non_tautological: true
---

# `OrbitSeparating`

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

## Propriedades exigidas, e verificadas

```text
quantifica sobre toda a orbita alcancada         SIM
assume apenas a igualdade do witness atual       NAO
exige injetividade global                        NAO
exige C finito                                   NAO
exige DecidableEq C                              NAO
verificavel pelo consumidor como obrigacao separada SIM
```

## Por que ela não é tautológica

A hipótese quantifica sobre **todos** os pares `i, j`; a conclusão da
reflexão compara **um** par específico, `baseIndex + period` e
`baseIndex`. A implicação é estrita.

A prova de que ela não é consequência da semiconjugação é positiva e
compilada:

```lean
theorem boolToUnit_not_orbitSeparating :
    ¬ OrbitSeparating forgetBool concreteStep false
```

Se `OrbitSeparating` decorresse da semiconjugação, valeria em
`BOOL_TO_UNIT` — onde a semiconjugação vale. Ela falha ali. Logo não
decorre.

Uma definição equivalente a "a igualdade concreta desejada para o
witness atual" seria tautológica e dispararia `STOP-ABS-006`.

## Satisfazibilidade

```lean
theorem orbitSeparating_of_injective
    {abstract : C → A} (hinj : Function.Injective abstract)
    (stepC : C → C) (start : C) :
    OrbitSeparating abstract stepC start
```

Sem axiomas. A condição é satisfeita por toda abstração injetiva — mas
exige **muito menos** do que injetividade global: apenas separação sobre
a órbita alcançada a partir de `start`.

## Comparação com `Set.InjOn`

A equivalência foi **provada em probe, sem axiomas**:

```lean
theorem orbitSeparating_iff_injOn
    (abstract : C → A) (stepC : C → C) (start : C) :
    OrbitSeparating abstract stepC start
      ↔ Set.InjOn abstract
          (Set.range fun k : Nat => (stepC^[k]) start)
```

| Critério | `OrbitSeparating` | `Set.InjOn` sobre `Set.range` |
|---|---|---|
| prova de reflexão | `hsep (b+p) b h`, direto | dois `Set.mem_range_self` |
| verificação pelo consumidor | quantificador sobre `Nat` | pertinência a `Set.range` |
| reutilização Mathlib | nenhuma herdada | herda o ferramental de `Set.InjOn` |
| dependência | só `Nat.iterate` | `Set`, `Set.range`, `Set.InjOn` |

### Decisão

```yaml
primary_public_contract: OrbitSeparating
Set.InjOn_equivalence: DEFERRED_OPTIONAL
```

Compilar não é motivo suficiente para publicar. Nenhum resultado central
consome a equivalência, e a regra da frente é escolher a API menor. Ela
fica registrada aqui, com evidência de que é barata, e pode ser
promovida por gate próprio se algum consumidor aparecer.
