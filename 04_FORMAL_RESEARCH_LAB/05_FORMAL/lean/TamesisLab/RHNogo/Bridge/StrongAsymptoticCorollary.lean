import TamesisLab.RHNogo.Bridge.CountingLawBridge

set_option autoImplicit false

/-!
# COUNTING-LAW-BRIDGE — corolários

1. `STRONG-TLOG-COROLLARY` (SB-GAP-010A): termo principal `c·T log T` mais
   erro `o(T log T)` implica a lei `T log T`. **Genérico**: nenhuma menção a
   `ζ`, a zeros ou a Riemann–von Mangoldt.
2. Níveis E0 e E1 da hierarquia de relações entre contagens.

O nível E3 (equivalência por razão) **não é formalizado neste gate**: exige
positividade e controle eventual do denominador.
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

/-- STRONG-TLOG-COROLLARY (SB-GAP-010A) — se `N(T) = c·T log T + r(T)` com
`r = o(T log T)`, então `N(T)/(T log T) → c`.

Formalização **genérica** da passagem "fórmula assintótica forte ⟹ limite".
Não menciona a função zeta nem seus zeros; instanciá-la com a fórmula de
Riemann–von Mangoldt é SB-GAP-010B, fora do alcance atual. -/
theorem tendsto_tLog_of_eq_main_add_littleO
    {N r : ℝ → ℝ} {c : ℝ}
    (hN : ∀ T, N T = c * (T * Real.log T) + r T)
    (hr : r =o[atTop] fun T => T * Real.log T) :
    Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c) := by
  have hsmall : SubdominantTLog N (fun T => c * (T * Real.log T)) := by
    show (fun T => N T - c * (T * Real.log T)) =o[atTop]
      fun T => T * Real.log T
    have h : (fun T => N T - c * (T * Real.log T)) = r := by
      funext T
      rw [hN T]
      ring
    rw [h]
    exact hr
  exact counting_law_bridge (tendsto_const_mul_tLogScale_div c) hsmall

/-- E0 ⟹ E2 — igualdade eventual implica diferença `o(T log T)`. -/
theorem subdominantTLog_of_eventualEquality
    {NTarget NBase : ℝ → ℝ} (h : EventualEquality NTarget NBase) :
    SubdominantTLog NTarget NBase := by
  show (fun T => NTarget T - NBase T) =o[atTop] fun T => T * Real.log T
  refine (isLittleO_zero (fun T : ℝ => T * Real.log T) atTop).congr' ?_
    (EventuallyEq.refl _ _)
  filter_upwards [h] with T hT
  rw [hT, sub_self]

/-- E0 ⟹ E1 — igualdade eventual implica diferença `O(1)`. -/
theorem boundedDifference_of_eventualEquality
    {NTarget NBase : ℝ → ℝ} (h : EventualEquality NTarget NBase) :
    BoundedDifference NTarget NBase := by
  show (fun T => NTarget T - NBase T) =O[atTop] fun _ => (1 : ℝ)
  refine (isBigO_zero (fun _ : ℝ => (1 : ℝ)) atTop).congr' ?_
    (EventuallyEq.refl _ _)
  filter_upwards [h] with T hT
  rw [hT, sub_self]

/-- Auxiliar: a norma da escala `T log T` diverge. -/
theorem tendsto_norm_tLogScale_atTop :
    Tendsto (fun T : ℝ => ‖T * Real.log T‖) atTop atTop := by
  simp only [Real.norm_eq_abs]
  exact tendsto_abs_atTop_atTop.comp tendsto_tLogScale_atTop

/-- E1 ⟹ E2 — diferença `O(1)` implica diferença `o(T log T)`, porque
`T log T → +∞`. -/
theorem subdominantTLog_of_boundedDifference
    {NTarget NBase : ℝ → ℝ} (h : BoundedDifference NTarget NBase) :
    SubdominantTLog NTarget NBase := by
  show (fun T => NTarget T - NBase T) =o[atTop] fun T => T * Real.log T
  refine (show (fun T => NTarget T - NBase T) =O[atTop] fun _ => (1 : ℝ)
    from h).trans_isLittleO ?_
  rw [isLittleO_const_left]
  exact Or.inr tendsto_norm_tLogScale_atTop

end TamesisLab.RHNogo.Bridge
