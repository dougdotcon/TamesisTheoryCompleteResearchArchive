---
document_id: FOUND-BISIMULATION-BOUNDARY-001-PUBLIC-API-SPECIFICATION
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
public_definitions: 3
public_theorems: 5
public_total: 8
typeclasses_required: 0
---

# API pública candidata

## Definições — 3

```text
Simulates
Reflects
Bisimulation
```

## Teoremas — 5

```text
simulates_iff_semiconj
reflects_iff_simulates
bisimulation_iff_semiconj
bisimulation_does_not_reflect_cycles
surjective_bisimulation_does_not_reflect_cycles
```

## Contagem derivada

```text
definicoes  3
teoremas    5
------------
total       8
```

Derivada das listas; será conferida por script contra as declarações
reais no gate de formalização.

## `TEST_ONLY`

```text
boolToUnit_bisimulation
forgetBool_surjective
```

Estes dois instanciam o resultado no contraexemplo. Eles são o
**material de evidência** das duas negações, e vivem com os testes, não
na API pública — a frente anterior tratou `BOOL_TO_UNIT` do mesmo modo.

## `DEFERRED_OPTIONAL`

```text
injective_bisimulation_reflects
```

Reconstruível em uma linha a partir de `OrbitSeparating`. Já existe
equivalente na frente anterior (`orbitSeparating_of_injective`),
igualmente diferido. Duplicá-lo aqui não acrescenta.

## Hipóteses do contrato público

```text
typeclasses   0
finitude      nao exigida
DecidableEq   nao exigida
sobrejetividade  exigida SOMENTE no enunciado que a menciona
```
