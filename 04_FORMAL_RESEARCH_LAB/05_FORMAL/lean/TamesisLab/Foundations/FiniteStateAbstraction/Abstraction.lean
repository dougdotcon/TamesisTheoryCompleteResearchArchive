import TamesisLab.Engineering.FiniteStateEncoding

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — a abstração certificada

Dois campos: um dado e uma lei.

```text
abstract    C → A                            dado
commutes    Function.Semiconj abstract stepC stepA   lei
```

A estrutura **não** armazena a codificação, o estado inicial, o
certificado, o resultado da análise, a tabela nem a condição de
reflexão. Ela descreve a abstração, e só ela.

`stepC` e `stepA` são parâmetros, não campos: pertencem aos sistemas.

## O que "certificada" significa, exatamente

```text
a comutacao entre stepC, abstract e stepA possui prova formal.
```

Não significa que um sistema externo real tenha sido corretamente
traduzido para `C`, nem que `abstract` seja injetiva, nem que
recorrências abstratas sejam concretas.
-/

namespace TamesisLab.Foundations.FiniteStateAbstraction

/-- Abstração determinística **certificada** entre dois sistemas.

O campo `commutes` é a certificação: a semiconjugação está orientada
como `abstract (stepC c) = stepA (abstract c)`, isto é, a trajetória
concreta é observada corretamente pela abstrata.

Nenhuma typeclass é exigida de `C` nem de `A`. Em particular `C` pode
ser infinito: a finitude executável entra depois, e só sobre `A`, por
`CertifiedFiniteEncoding`. -/
structure CertifiedFiniteAbstraction (C A : Type*) (stepC : C → C) (stepA : A → A) where
  /-- A observação de um estado concreto. Pode ser muitos-para-um. -/
  abstract : C → A
  /-- A certificação: um passo concreto, observado, é um passo abstrato. -/
  commutes : Function.Semiconj abstract stepC stepA

variable {C A : Type*} {stepC : C → C} {stepA : A → A}

/-- **Correspondência de iteradas.**

Observar a trajetória concreta após `k` passos é o mesmo que iterar `k`
vezes no sistema abstrato a observação inicial.

A rota é a API oficial de Mathlib, `Function.Semiconj.iterate_right`, e
não uma indução manual — este é o terceiro consumo consecutivo desse
lema no laboratório.

Nenhuma finitude, nenhuma igualdade decidível, nenhuma hipótese sobre a
codificação: o resultado pertence somente à abstração. -/
theorem CertifiedFiniteAbstraction.iterate_commutes
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA) (k : Nat) (start : C) :
    abstraction.abstract ((stepC^[k]) start) = (stepA^[k]) (abstraction.abstract start) :=
  abstraction.commutes.iterate_right k start

end TamesisLab.Foundations.FiniteStateAbstraction
