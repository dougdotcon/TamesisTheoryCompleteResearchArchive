import TamesisLab.RHNogo.AsymptoticCore.Definitions
import Mathlib.Order.Filter.AtTopBot.Basic

/-!
# ASYM-NOGO-001 — Normalization

ASYM-NOGO-ALG-001: identidade algébrica eventual entre as duas
normalizações.

A identidade vale eventualmente (para `T > 1`), onde `T ≠ 0`, `log T ≠ 0`
e `T ^ α ≠ 0`. Nenhuma divisão por `N T` é usada e nada é assumido sobre o
sinal de `N T`.
-/

namespace TamesisLab.RHNogo.AsymptoticCore

open Filter

/-- ASYM-NOGO-ALG-001 — para `T` suficientemente grande,
`N T / T ^ α = (N T / (T log T)) · (log T · T ^ (1 - α))`. -/
theorem eventually_normalization_identity (N : ℝ → ℝ) (α : ℝ) :
    ∀ᶠ T : ℝ in atTop,
      N T / T ^ α =
        (N T / (T * Real.log T)) * (Real.log T * T ^ (1 - α)) := by
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with T hT
  have hT0 : (0 : ℝ) < T := lt_trans zero_lt_one hT
  have hTne : T ≠ 0 := ne_of_gt hT0
  have hlog : Real.log T ≠ 0 := ne_of_gt (Real.log_pos hT)
  have hpow : T ^ α ≠ 0 := ne_of_gt (Real.rpow_pos_of_pos hT0 α)
  have hrpow : T ^ (1 - α) = T / T ^ α := by
    rw [Real.rpow_sub hT0, Real.rpow_one]
  rw [hrpow]
  field_simp

/-- Versão da identidade com a orientação usada pelas transferências de
limite: o produto coincide eventualmente com `N T / T ^ α`. -/
theorem eventually_product_eq_normalizeRpow (N : ℝ → ℝ) (α : ℝ) :
    (fun T : ℝ => (N T / (T * Real.log T)) * (Real.log T * T ^ (1 - α)))
      =ᶠ[atTop] fun T : ℝ => N T / T ^ α :=
  (eventually_normalization_identity N α).mono fun _ h => h.symm

end TamesisLab.RHNogo.AsymptoticCore
