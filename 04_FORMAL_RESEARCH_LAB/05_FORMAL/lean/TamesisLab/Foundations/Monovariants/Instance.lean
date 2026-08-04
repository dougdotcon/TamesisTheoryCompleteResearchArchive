import TamesisLab.Foundations.Monovariants.Definitions

set_option autoImplicit false

/-!
# FOUND-MONOVARIANT-DESCENT-001 — instâncias, TEST_ONLY

Duas definições que existem para sustentar **negações**. Elas impedem que
a ferramenta seja lida como universal.
-/

namespace TamesisLab.Foundations.Monovariants

/-- Passo estritamente crescente sobre um tipo infinito. -/
def downStep (p : Nat × Nat) : Nat × Nat := (p.1 + 1, p.2 + 1)

/-- Subtração truncada. A função óbvia que **parece** decrescer. -/
def strictDown (k : Nat) : Nat := k - 1

end TamesisLab.Foundations.Monovariants
