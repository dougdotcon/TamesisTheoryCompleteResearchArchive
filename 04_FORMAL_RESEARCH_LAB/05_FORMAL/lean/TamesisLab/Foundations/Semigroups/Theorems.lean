import TamesisLab.Foundations.Semigroups.Regime3
import Mathlib.Data.Fintype.Card

/-!
# FOUND-SEMIGROUP-001 — Theorems: leis do modelo cíclico

Todos os teoremas são propriedades de um modelo finito explícito, provadas
antes de qualquer instância estrutural (a ordem exigida pelo gate: definir
operação → provar leis → instanciar). As provas por `decide` são análises
finitas exaustivas verificadas pelo kernel; as provas por `rfl`/`cases` são
computação definicional.

novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
-/

namespace TamesisLab.Foundations.Semigroups

/-- FOUND-SG-002 — associatividade da composição (27 casos). -/
theorem comp_assoc (a b c : Shift3) :
    Shift3.comp (Shift3.comp a b) c = Shift3.comp a (Shift3.comp b c) := by
  revert a b c; decide

/-- FOUND-SG-003 — identidade à esquerda. -/
theorem identity_comp (a : Shift3) : Shift3.comp .identity a = a := rfl

/-- FOUND-SG-004 — identidade à direita. -/
theorem comp_identity (a : Shift3) : Shift3.comp a .identity = a := by
  cases a <;> rfl

/-- FOUND-SG-005 — compatibilidade da ação com a composição, na convenção
adotada (`comp a b` aplica `b` primeiro): 9 transições × 3 regimes. -/
theorem apply_comp (a b : Shift3) (r : Regime3) :
    (Shift3.comp a b).apply r = a.apply (b.apply r) := by
  revert a b r; decide

/-- FOUND-SG-006 — `forward` aplicada três vezes retorna ao regime inicial. -/
theorem forward_cycle (r : Regime3) :
    Shift3.forward.apply (Shift3.forward.apply (Shift3.forward.apply r)) = r := by
  cases r <;> rfl

/-- FOUND-SG-007 — `Regime3` possui exatamente três elementos. -/
theorem card_regime3 : Fintype.card Regime3 = 3 := by decide

/-- FOUND-SG-008 — `Shift3` possui exatamente três elementos. -/
theorem card_shift3 : Fintype.card Shift3 = 3 := by decide

/-- FOUND-SG-009 — `identity ≠ forward`. Decorre da igualdade decidível. -/
theorem identity_ne_forward : Shift3.identity ≠ Shift3.forward := by decide

/-- FOUND-SG-010 — `identity ≠ forward2`. Decorre da igualdade decidível. -/
theorem identity_ne_forward2 : Shift3.identity ≠ Shift3.forward2 := by decide

/-- FOUND-SG-011 — `forward ≠ forward2`. Decorre da igualdade decidível. -/
theorem forward_ne_forward2 : Shift3.forward ≠ Shift3.forward2 := by decide

/-- FOUND-SG-012 — fidelidade: transições com a mesma ação em todos os
regimes são iguais. Análise finita exaustiva. -/
theorem apply_faithful (a b : Shift3)
    (h : ∀ r, Shift3.apply a r = Shift3.apply b r) : a = b := by
  revert a b; decide

/-- FOUND-SG-013 — transitividade do modelo: para quaisquer regimes `x` e
`y` existe uma transição levando `x` a `y`. Propriedade do modelo cíclico de
três elementos, não de semigrupos em geral. -/
theorem apply_transitive (x y : Regime3) :
    ∃ s : Shift3, s.apply x = y := by
  revert x y; decide

end TamesisLab.Foundations.Semigroups
