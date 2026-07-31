import TamesisLab.RHNogo.AsymptoticCore.Normalization
import TamesisLab.RHNogo.AsymptoticCore.PowerLog
import Mathlib.Topology.Algebra.Order.Field

/-!
# ASYM-NOGO-001 — Incompatibility

Teorema principal: nenhuma função real admite simultaneamente uma
normalização assintótica positiva finita por `T log T` e uma normalização
assintótica positiva finita por `T ^ α`, com `α > 0`.

O enunciado é puramente de análise real. Não menciona a função zeta, seus
zeros, a Hipótese de Riemann, operadores, PDE, a lei de Weyl ou a Classe W.
-/

namespace TamesisLab.RHNogo.AsymptoticCore

open Filter

/-- Auxiliar: quando o fator de comparação diverge, a normalização por
`T ^ α` também diverge. -/
theorem tendsto_normalizeRpow_atTop_of_factor_atTop
    {N : ℝ → ℝ} {α c : ℝ} (hc : 0 < c)
    (hTLog : Tendsto (fun T : ℝ => N T / (T * Real.log T)) atTop (nhds c))
    (hfac : Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop atTop) :
    Tendsto (fun T : ℝ => N T / T ^ α) atTop atTop :=
  (Filter.Tendsto.pos_mul_atTop hc hTLog hfac).congr'
    (eventually_product_eq_normalizeRpow N α)

/-- Auxiliar: quando o fator de comparação tende a zero, a normalização por
`T ^ α` tende a zero. -/
theorem tendsto_normalizeRpow_nhds_zero_of_factor_nhds_zero
    {N : ℝ → ℝ} {α c : ℝ}
    (hTLog : Tendsto (fun T : ℝ => N T / (T * Real.log T)) atTop (nhds c))
    (hfac : Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop (nhds 0)) :
    Tendsto (fun T : ℝ => N T / T ^ α) atTop (nhds 0) := by
  have h := hTLog.mul hfac
  rw [mul_zero] at h
  exact h.congr' (eventually_product_eq_normalizeRpow N α)

/-- **ASYM-NOGO-001.** Não existe `N : ℝ → ℝ` que satisfaça
simultaneamente `N T / (T log T) → c > 0` e `N T / T ^ α → C > 0` com
`α > 0`.

Resultado de análise real elementar; sem qualquer conteúdo aritmético,
espectral ou geométrico. -/
theorem asym_nogo_001
    (N : ℝ → ℝ) (α c C : ℝ)
    (hα : 0 < α) (hc : 0 < c) (hC : 0 < C)
    (hTLog : Tendsto (fun T : ℝ => N T / (T * Real.log T)) atTop (nhds c))
    (hPower : Tendsto (fun T : ℝ => N T / T ^ α) atTop (nhds C)) :
    False := by
  rcases lt_trichotomy α 1 with h | h | h
  · -- α < 1: o fator diverge, logo N/T^α diverge, contradizendo o limite C.
    exact not_tendsto_nhds_of_tendsto_atTop
      (tendsto_normalizeRpow_atTop_of_factor_atTop hc hTLog
        (tendsto_powerLogFactor_atTop_of_lt_one h)) C hPower
  · -- α = 1: o fator é log T, que diverge; mesma contradição.
    exact not_tendsto_nhds_of_tendsto_atTop
      (tendsto_normalizeRpow_atTop_of_factor_atTop hc hTLog
        (tendsto_powerLogFactor_atTop_of_eq_one h)) C hPower
  · -- α > 1: o fator tende a 0, logo N/T^α → 0; por unicidade, C = 0.
    have hzero := tendsto_normalizeRpow_nhds_zero_of_factor_nhds_zero hTLog
      (tendsto_powerLogFactor_nhds_zero_of_one_lt h)
    have hCzero : C = 0 := tendsto_nhds_unique hPower hzero
    exact absurd hCzero (ne_of_gt hC)

end TamesisLab.RHNogo.AsymptoticCore
