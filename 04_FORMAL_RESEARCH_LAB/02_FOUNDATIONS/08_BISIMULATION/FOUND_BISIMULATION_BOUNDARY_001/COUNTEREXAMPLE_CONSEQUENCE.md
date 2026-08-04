---
document_id: FOUND-BISIMULATION-BOUNDARY-001-COUNTEREXAMPLE-CONSEQUENCE
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
bisimulation_reflects_cycles: FALSE
surjective_bisimulation_reflects_cycles: FALSE
---

# A consequência: o contraexemplo já era uma bissimulação

## O que se descobre sobre `BOOL_TO_UNIT`

O contraexemplo formalizado na frente anterior não precisa ser
modificado nem estendido. Basta aplicar o colapso a ele:

```lean
theorem boolToUnit_bisimulation :
    Bisimulation forgetBool concreteStep abstractStep :=
  (bisimulation_iff_semiconj forgetBool concreteStep abstractStep).mpr
    boolToUnit_semiconj
```

Ele **sempre foi** uma bissimulação. Ninguém tinha olhado.

## E a abstração é sobrejetiva

```lean
theorem forgetBool_surjective : Function.Surjective forgetBool
```

`Unit` tem um habitante, e `forgetBool false = ()`. Portanto nem a
sobrejetividade — a hipótese que costuma acompanhar bissimulação
funcional — resgata a reflexão.

## As duas negações

```lean
theorem bisimulation_does_not_reflect_cycles :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Bisimulation abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start)

theorem surjective_bisimulation_does_not_reflect_cycles :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Function.Surjective abstract →
        Bisimulation abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start)
```

Ambos como **teoremas de negação que compilam**, sem pegada axiomática.
Nenhum arquivo deliberadamente inválido.

## O quadro completo, agora

```text
semiconjugacao                 NAO reflete ciclos
bissimulacao funcional         NAO reflete ciclos   (e a mesma coisa)
bissimulacao sobrejetiva       NAO reflete ciclos
OrbitSeparating                REFLETE
injetividade global            REFLETE  (mais forte que o necessario)
```

A tabela é o produto real da frente: ela mostra que a fronteira entre
observar e refletir **não** é atravessada por nenhum reforço estrutural
da relação de simulação, e sim por uma condição de **separação de
estados**.

## O que continua não provado

```text
que abstracoes injetivas sejam desejaveis      nao e afirmado
que sistemas nao deterministicos se comportem assim   nao e afirmado
que exista construcao canonica que force separacao    nao e afirmado
```
