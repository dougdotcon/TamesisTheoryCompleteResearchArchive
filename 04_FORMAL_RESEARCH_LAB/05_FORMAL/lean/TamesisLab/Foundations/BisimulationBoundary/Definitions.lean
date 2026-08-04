import TamesisLab.Foundations.FiniteStateAbstraction

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — as duas metades

Bissimulação funcional, escrita como a conjunção honesta das suas duas
obrigações.

```text
zig   Simulates   todo passo concreto e acompanhado no abstrato
zag   Reflects    todo passo abstrato observado e acompanhado no concreto
```

`Reflects` conserva a quantificação existencial **de propósito**. Ela
parece redundante justamente porque o teorema de colapso é verdadeiro;
escrevê-la já resolvida tornaria esse teorema uma tautologia disfarçada.

O recorte é essencial e vive em `SCOPE_BOUNDARY.md`: sistemas
determinísticos **totais**, bissimulação **funcional**, sem rótulos.
-/

namespace TamesisLab.Foundations.BisimulationBoundary

variable {C A : Type*}

/-- **Zig.** Todo passo concreto é acompanhado por um passo abstrato.

Definicionalmente igual a `Function.Semiconj abstract stepC stepA`; o
nome existe para dar identidade à metade. -/
def Simulates (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, abstract (stepC c) = stepA (abstract c)

/-- **Zag.** Todo passo abstrato a partir de um estado observado é
acompanhado por algum passo concreto.

A existencial é a transcrição fiel da condição de bissimulação. Sob
determinismo e totalidade ela não oferece escolha — e é exatamente esse
o conteúdo de `reflects_iff_simulates`. Simplificá-la aqui destruiria o
resultado. -/
def Reflects (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, ∃ c' : C, stepC c = c' ∧ abstract c' = stepA (abstract c)

/-- **Bissimulação funcional**: as duas metades.

Não é uma definição coindutiva. Não é o maior ponto fixo de funtor
algum. É a conjunção de duas proposições quantificadas, e só se aplica
ao gráfico de uma função. -/
def Bisimulation (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  Simulates abstract stepC stepA ∧ Reflects abstract stepC stepA

end TamesisLab.Foundations.BisimulationBoundary
