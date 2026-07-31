import TamesisLab.Foundations.Semigroups.Action

/-!
# FOUND-SEMIGROUP-001 — Audit: verificações de interface

Confirma, por typecheck, que as instâncias criadas em `Action.lean` fecham a
camada abstrata da Mathlib (Camada A do gate) e que as notações `*`, `1` e
`•` correspondem exatamente às operações locais. Nenhum resultado novo é
introduzido.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
-/

namespace TamesisLab.Foundations.Semigroups

-- Camada A fechada pela interface oficial da Mathlib, sem duplicata local.
example : Semigroup Shift3 := inferInstance
example : Monoid Shift3 := inferInstance
example : SemigroupAction Shift3 Regime3 := inferInstance
example : MulAction Shift3 Regime3 := inferInstance

-- As notações estruturais coincidem definicionalmente com as operações
-- locais provadas em `Theorems.lean`.
example (a b : Shift3) : a * b = Shift3.comp a b := rfl
example : (1 : Shift3) = Shift3.identity := rfl
example (s : Shift3) (r : Regime3) : s • r = s.apply r := rfl

-- Leis reexpressas na linguagem estrutural (mesmos teoremas, sem provas
-- novas).
example (a b c : Shift3) : a * b * c = a * (b * c) := comp_assoc a b c
example (a : Shift3) : 1 * a = a := identity_comp a
example (a : Shift3) : a * 1 = a := comp_identity a
example (a b : Shift3) (r : Regime3) : (a * b) • r = a • b • r :=
  apply_comp a b r
example (r : Regime3) : (1 : Shift3) • r = r := rfl

end TamesisLab.Foundations.Semigroups
