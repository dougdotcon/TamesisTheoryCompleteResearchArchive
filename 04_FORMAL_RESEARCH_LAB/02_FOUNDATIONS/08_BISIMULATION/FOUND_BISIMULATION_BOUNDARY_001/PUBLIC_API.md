---
document_id: FOUND-BISIMULATION-BOUNDARY-001-PUBLIC-API
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
status: IMPLEMENTED
public_total: 8
counts_derived_by_script: true
typeclasses_required: 0
axiom_footprint: NONE
---

# API pública implementada

## Definições — 3

```lean
def Simulates    (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop
def Reflects     (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop
def Bisimulation (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop
```

## Teoremas — 5

```lean
theorem simulates_iff_semiconj
theorem reflects_iff_simulates
theorem bisimulation_iff_semiconj
theorem bisimulation_does_not_reflect_cycles
theorem surjective_bisimulation_does_not_reflect_cycles
```

## Contagem

```text
declarada   8
derivada    8
divergencia 0
```

## Onde cada uma vive

```text
Definitions.lean      Simulates, Reflects, Bisimulation
Collapse.lean         simulates_iff_semiconj, reflects_iff_simulates,
                      bisimulation_iff_semiconj
CycleReflection.lean  as duas negacoes
```

## Fora da API

```text
CounterexampleInstance.lean   2 declaracoes, TEST_ONLY
  boolToUnit_bisimulation
  forgetBool_surjective
```

Residentes na biblioteca porque as negações públicas as consomem. Mesmo
tratamento que `FiniteStateAbstraction/Counterexample.lean` recebeu.

## Contrato

```text
typeclasses exigidas   0
finitude               nao exigida
DecidableEq            nao exigida
sobrejetividade        exigida SOMENTE no enunciado que a menciona
pegada axiomatica      NENHUMA, 10 de 10
```

## Como consumir

Quem já tem `Function.Semiconj abstract stepC stepA` obtém a
bissimulação de graça:

```lean
(bisimulation_iff_semiconj abstract stepC stepA).mpr h
```

E não deve esperar nada disso em troca: as duas negações registram que
a bissimulação assim obtida **não** reflete ciclos.
