import TamesisLab.RHNogo.Bridge.TLogScale

set_option autoImplicit false

/-!
# COUNTING-LAW-BRIDGE — LittleOTransfer

Os dois ingredientes da ponte: conversão de `little-o` em limite zero, e a
identidade algébrica das normalizações.
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

/-- CLB-LO-001 — uma diferença `o(T log T)`, normalizada pela escala, tende
a zero. Reutiliza `IsLittleO.tendsto_div_nhds_zero` da Mathlib; nada da
definição de `little-o` é reprovado à mão. -/
theorem subdominantDifference_tendsto_zero
    {NTarget NBase : ℝ → ℝ} (hsmall : SubdominantTLog NTarget NBase) :
    Tendsto (fun T => (NTarget T - NBase T) / (T * Real.log T))
      atTop (nhds 0) :=
  hsmall.tendsto_div_nhds_zero

/-- CLB-ALG-001a — identidade **pontual** das normalizações.

A não nulidade do denominador **não é necessária**: em um corpo,
`a / s + b / s = (a + b) / s` vale inclusive para `s = 0`. -/
theorem target_normalization_eq (NTarget NBase : ℝ → ℝ) (T : ℝ) :
    NTarget T / (T * Real.log T) =
      NBase T / (T * Real.log T) +
        (NTarget T - NBase T) / (T * Real.log T) := by
  simp only [div_eq_mul_inv]
  ring

/-- CLB-ALG-001 — versão eventual, na forma consumida pelas transferências
de limite. Segue da versão pontual; o qualificador eventual é conveniência,
não necessidade. -/
theorem eventually_target_normalization_eq (NTarget NBase : ℝ → ℝ) :
    ∀ᶠ T : ℝ in atTop,
      NTarget T / (T * Real.log T) =
        NBase T / (T * Real.log T) +
          (NTarget T - NBase T) / (T * Real.log T) :=
  Eventually.of_forall (target_normalization_eq NTarget NBase)

end TamesisLab.RHNogo.Bridge
