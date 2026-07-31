import TamesisLab.RHNogo.Bridge.Definitions

set_option autoImplicit false

/-!
# COUNTING-LAW-BRIDGE — TLogScale

Propriedades elementares da escala `T log T`.

Nenhuma afirmação global sobre `Real.log` é feita: tudo é enunciado
eventualmente em `atTop`, sob `1 < T`.
-/

namespace TamesisLab.RHNogo.Bridge

open Filter

/-- CLB-SCALE-001 — `T · log T` é eventualmente não nulo em `atTop`. -/
theorem eventually_tLogScale_ne_zero :
    ∀ᶠ T : ℝ in atTop, T * Real.log T ≠ 0 := by
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with T hT
  have hT0 : (0 : ℝ) < T := lt_trans zero_lt_one hT
  exact mul_ne_zero (ne_of_gt hT0) (ne_of_gt (Real.log_pos hT))

/-- CLB-SCALE-002 — `T · log T → +∞`. Usado apenas pelo corolário do
nível E1. -/
theorem tendsto_tLogScale_atTop :
    Tendsto (fun T : ℝ => T * Real.log T) atTop atTop :=
  Filter.Tendsto.atTop_mul_atTop₀ tendsto_id Real.tendsto_log_atTop

/-- CLB-SCALE-003 — a normalização de `c · (T log T)` pela própria escala
tende a `c`. -/
theorem tendsto_const_mul_tLogScale_div (c : ℝ) :
    Tendsto (fun T : ℝ => c * (T * Real.log T) / (T * Real.log T))
      atTop (nhds c) := by
  refine tendsto_const_nhds.congr' ?_
  filter_upwards [eventually_tLogScale_ne_zero] with T hT
  rw [mul_div_assoc, div_self hT, mul_one]

end TamesisLab.RHNogo.Bridge
