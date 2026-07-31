import TamesisLab.Foundations.FunctionalGraphs.Relations
import Mathlib.Dynamics.PeriodicPts.Defs

set_option autoImplicit false

/-!
# FOUND-FUNCTIONAL-GRAPH-001 — Órbitas periódicas

Pontos periódicos que se encontram eventualmente determinam **a mesma
órbita periódica**.

O objeto único é `Function.periodicOrbit f p`, um `Cycle X` — quociente por
rotação —, e **não** um representante escolhido.

## Fontes reutilizadas

```text
Function.periodicPts f = { x | ∃ n > 0, IsPeriodicPt f n x }
Function.periodicOrbit f x : Cycle X
Function.periodicOrbit_apply_iterate_eq (hx) (n) :
  periodicOrbit f (f^[n] x) = periodicOrbit f x
```

`Function.IsPeriodicPt f 0 x` é **sempre verdadeiro**; por isso a fonte de
"ponto do ciclo" é `periodicPts`, que exige `∃ n > 0`, e nunca
`IsPeriodicPt` isolada.

**Nenhuma hipótese de finitude neste arquivo.** Nem `DecidableEq`, nem
`minimalPeriod`, nem aritmética modular.
-/

namespace TamesisLab.Foundations.FunctionalGraphs

/-- FFG-CYCLE-001 — pontos periódicos que se encontram eventualmente
determinam a mesma órbita periódica.

Orientação congelada: o **primeiro** argumento de `EventuallyMeets` fica à
esquerda da igualdade. -/
theorem periodicOrbit_eq_of_eventuallyMeets {X : Type*} {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f)
    (hq : q ∈ Function.periodicPts f)
    (hpq : EventuallyMeets f p q) :
    Function.periodicOrbit f p = Function.periodicOrbit f q := by
  obtain ⟨m, n, hmn⟩ := hpq
  calc Function.periodicOrbit f p
      = Function.periodicOrbit f (f^[m] p) :=
        (Function.periodicOrbit_apply_iterate_eq hp m).symm
    _ = Function.periodicOrbit f (f^[n] q) := by rw [hmn]
    _ = Function.periodicOrbit f q :=
        Function.periodicOrbit_apply_iterate_eq hq n

/-- FFG-CYCLE-002 — recíproca. `OPTIONAL_COROLLARY`.

Composição curta de `self_mem_periodicOrbit` e `mem_periodicOrbit_iff`.
**Não** é dependência do teorema principal. -/
theorem eventuallyMeets_of_periodicOrbit_eq {X : Type*} {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f)
    (hq : q ∈ Function.periodicPts f)
    (hOrbit : Function.periodicOrbit f p = Function.periodicOrbit f q) :
    EventuallyMeets f p q := by
  have hmem : p ∈ Function.periodicOrbit f q := by
    rw [← hOrbit]
    exact Function.self_mem_periodicOrbit hp
  obtain ⟨n, hn⟩ := (Function.mem_periodicOrbit_iff hq).mp hmem
  exact ⟨0, n, hn.symm⟩

end TamesisLab.Foundations.FunctionalGraphs
