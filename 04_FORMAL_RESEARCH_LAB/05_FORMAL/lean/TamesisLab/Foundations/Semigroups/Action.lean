import TamesisLab.Foundations.Semigroups.Basic
import TamesisLab.Foundations.Semigroups.Theorems

/-!
# FOUND-SEMIGROUP-001 — Action: instâncias estruturais

As instâncias são criadas somente aqui, depois das leis provadas em
`Theorems.lean`, na ordem exigida pelo gate: operação → leis → instâncias.
Nenhuma instância é usada para provar retroativamente as próprias leis.

`Monoid Shift3` fornece `Semigroup Shift3` por herança;
`MulAction Shift3 Regime3` fornece `SemigroupAction Shift3 Regime3` por
herança — ambas as projeções são verificadas em `Audit.lean`.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
-/

namespace TamesisLab.Foundations.Semigroups

/-- Monoide das transições: `*` é `Shift3.comp`, `1` é `Shift3.identity`.
Leis: FOUND-SG-002/003/004. -/
instance : Monoid Shift3 where
  mul := Shift3.comp
  mul_assoc := comp_assoc
  one := Shift3.identity
  one_mul := identity_comp
  mul_one := comp_identity

/-- Ação de monoide das transições sobre os regimes: `•` é `Shift3.apply`.
Leis: FOUND-SG-005 e a aplicação definicional da identidade. -/
instance : MulAction Shift3 Regime3 where
  smul := Shift3.apply
  mul_smul := apply_comp
  one_smul := fun _ => rfl

end TamesisLab.Foundations.Semigroups
