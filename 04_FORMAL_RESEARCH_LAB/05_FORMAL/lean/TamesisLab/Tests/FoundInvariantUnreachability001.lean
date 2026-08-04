import TamesisLab.Foundations.Invariants

set_option autoImplicit false

/-!
# Testes de FOUND-INVARIANT-UNREACHABILITY-001

Dois testes. O primeiro mostra a ferramenta **mordendo** num sistema
concreto infinito. O segundo impede a leitura ao contrário.
-/

namespace TamesisLab.Tests.FoundInvariantUnreachability001

open TamesisLab.Foundations.Invariants

/-- **Impossibilidade provada pela ferramenta.**

`(1, 0)` não é alcançável a partir de `(0, 0)` sob `diagStep`, por
nenhum número de passos. A diferença das coordenadas vale `0` na origem
e `1` no alvo, e ela é invariante.

`Int × Int` é infinito. Nenhuma enumeração, nenhuma busca, nenhuma
finitude. -/
theorem diag_unreachable : ¬ Reachable diagStep (0, 0) (1, 0) := by
  refine unreachable_of_invariant_ne diagStep_invariant ?_
  decide

/-- **O limite da ferramenta, escrito em Lean e não só em prosa.**

O invariante constante é um invariante legítimo e não prova nada: ele
não separa par nenhum. A ferramenta é **suficiente**, nunca
**necessária**, e esta declaração existe para que ninguém leia o teorema
ao contrário. Ver `INV-GAP-001`. -/
theorem constant_invariant_proves_nothing {C : Type*} (stepC : C → C) :
    Invariant (fun _ : C => ()) stepC := fun _ => rfl

end TamesisLab.Tests.FoundInvariantUnreachability001
