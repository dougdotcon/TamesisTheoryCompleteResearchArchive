import TamesisLab.RHNogo.AsymptoticCore.Definitions
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics

/-!
# ASYM-NOGO-001 — PowerLog

Tricotomia do fator de comparação `log T · T ^ (1 - α)`:

* `α < 1` (ASYM-NOGO-PL-001): tende a `+∞`;
* `α = 1` (ASYM-NOGO-PL-002): reduz-se a `log T` e tende a `+∞`;
* `α > 1` (ASYM-NOGO-PL-003): tende a `0`.

O caso `α > 1` reutiliza `isLittleO_log_rpow_atTop` da Mathlib (namespace
raiz), sem recriar o resultado.
-/

namespace TamesisLab.RHNogo.AsymptoticCore

open Filter

/-- Auxiliar comum a `α < 1` e `α = 1`: para `α ≤ 1` o fator domina
`log T`, logo diverge. -/
theorem tendsto_powerLogFactor_atTop_of_le_one {α : ℝ} (hα : α ≤ 1) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop atTop := by
  refine tendsto_atTop_mono' atTop ?_ Real.tendsto_log_atTop
  filter_upwards [eventually_ge_atTop (1 : ℝ)] with T hT
  have hlog : 0 ≤ Real.log T := Real.log_nonneg hT
  have hone : (1 : ℝ) ≤ T ^ (1 - α) := Real.one_le_rpow hT (by linarith)
  nlinarith

/-- ASYM-NOGO-PL-001 — caso `α < 1`: `log T · T ^ (1 - α) → +∞`. -/
theorem tendsto_powerLogFactor_atTop_of_lt_one {α : ℝ} (hα : α < 1) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop atTop :=
  tendsto_powerLogFactor_atTop_of_le_one (le_of_lt hα)

/-- ASYM-NOGO-PL-002a — caso `α = 1`: o fator reduz-se exatamente a
`log T`. -/
theorem powerLogFactor_eq_log_of_eq_one {α : ℝ} (hα : α = 1) (T : ℝ) :
    Real.log T * T ^ (1 - α) = Real.log T := by
  simp [hα]

/-- ASYM-NOGO-PL-002 — caso `α = 1`: `log T · T ^ (1 - α) → +∞`. -/
theorem tendsto_powerLogFactor_atTop_of_eq_one {α : ℝ} (hα : α = 1) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop atTop :=
  tendsto_powerLogFactor_atTop_of_le_one (le_of_eq hα)

/-- ASYM-NOGO-PL-003 — caso `α > 1`: `log T · T ^ (1 - α) → 0`,
equivalentemente `log T / T ^ (α - 1) → 0`. -/
theorem tendsto_powerLogFactor_nhds_zero_of_one_lt {α : ℝ} (hα : 1 < α) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop (nhds 0) := by
  have hr : 0 < α - 1 := sub_pos.mpr hα
  have h := (isLittleO_log_rpow_atTop hr).tendsto_div_nhds_zero
  refine h.congr' ?_
  filter_upwards [eventually_gt_atTop (0 : ℝ)] with T hT
  rw [div_eq_mul_inv, ← Real.rpow_neg (le_of_lt hT), neg_sub]

end TamesisLab.RHNogo.AsymptoticCore
