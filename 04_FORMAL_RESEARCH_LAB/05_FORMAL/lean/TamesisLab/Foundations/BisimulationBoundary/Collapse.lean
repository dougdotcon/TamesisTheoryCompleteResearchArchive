import TamesisLab.Foundations.BisimulationBoundary.Definitions

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — o colapso

Em sistemas determinísticos **totais**, o zag é consequência do zig, e a
bissimulação funcional não é uma condição mais forte que a
semiconjugação.

```text
zag:  dado c, exibir c' com stepC c = c' e abstract c' = stepA (abstract c)

stepC e funcao TOTAL, entao a testemunha esta imposta: c' = stepC c

o que sobra e exatamente o zig
```

É a **ausência de escolha** que produz o colapso. Qualquer relaxamento
que devolva escolha — não determinismo, relações de transição gerais,
bissimulação relacional, rótulos, funções parciais — destrói o
argumento. Ver `SCOPE_BOUNDARY.md`.
-/

namespace TamesisLab.Foundations.BisimulationBoundary

variable {C A : Type*}

/-- O zig **é** a semiconjugação, por definição. -/
theorem simulates_iff_semiconj (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Simulates abstract stepC stepA ↔ Function.Semiconj abstract stepC stepA :=
  Iff.rfl

/-- O zag **não** é o zig por definição, mas é equivalente a ele.

O contraste com `simulates_iff_semiconj`, que é `Iff.rfl`, é a evidência
de que a existencial do zag não foi trivializada: aqui a prova precisa
das duas direções. -/
theorem reflects_iff_simulates (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Reflects abstract stepC stepA ↔ Simulates abstract stepC stepA := by
  constructor
  · intro h c
    obtain ⟨c', hstep, hobs⟩ := h c
    exact hstep ▸ hobs
  · intro h c
    exact ⟨stepC c, rfl, h c⟩

/-- **O colapso.**

Para sistemas determinísticos totais, a bissimulação funcional coincide
com a semiconjugação.

Enunciar isto sem o qualificador — "bissimulação é semiconjugação" — é
**falso**, e falso exatamente na teoria de concorrência onde a palavra
nasceu, que é não determinística e rotulada. -/
theorem bisimulation_iff_semiconj (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Bisimulation abstract stepC stepA ↔ Function.Semiconj abstract stepC stepA := by
  constructor
  · intro h
    exact (simulates_iff_semiconj abstract stepC stepA).mp h.1
  · intro h
    exact ⟨h, (reflects_iff_simulates abstract stepC stepA).mpr h⟩

end TamesisLab.Foundations.BisimulationBoundary
