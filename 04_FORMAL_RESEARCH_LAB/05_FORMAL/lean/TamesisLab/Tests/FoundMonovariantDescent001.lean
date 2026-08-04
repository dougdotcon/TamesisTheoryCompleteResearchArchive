import TamesisLab.Foundations.Monovariants

set_option autoImplicit false

/-!
# Testes de FOUND-MONOVARIANT-DESCENT-001

Duas negações. Ambas existem para impedir leituras erradas da ferramenta.
-/

namespace TamesisLab.Tests.FoundMonovariantDescent001

open TamesisLab.Foundations.Monovariants

/-- Um sistema estritamente crescente não tem a primeira coordenada como
monovariante. A ferramenta **não** é universal. -/
theorem downStep_not_monovariant :
    ¬ Monovariant (fun p : Nat × Nat => p.1) downStep := by
  intro h
  have := h (0, 0)
  simp [downStep] at this

/-- **O registro que importa.**

`Nat` é bem fundado, e ainda assim `k - 1` **não** é monovariante:
falha em zero, onde a subtração trunca.

Boa fundação do contradomínio **não substitui** decrescimento estrito. -/
theorem strictDown_not_monovariant :
    ¬ Monovariant (fun k : Nat => k) strictDown := by
  intro h
  have := h 0
  simp [strictDown] at this

end TamesisLab.Tests.FoundMonovariantDescent001
