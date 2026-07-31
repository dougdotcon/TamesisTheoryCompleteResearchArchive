import TamesisLab.RHNogo.AsymptoticCore

/-!
# ASYM-NOGO-001 — teste isolado

Importa o núcleo e referencia cada teorema rastreável por nome, com as
assinaturas originais. Sem hipóteses ocultas: a auditoria dos axiomas do
kernel está registrada em
`03_MILLENNIUM/01_RIEMANN/ASYM_NOGO_001_PROOF_AUDIT.md`.
-/

namespace TamesisLab.Tests.RHNogoAsymptotic001

open Filter TamesisLab.RHNogo.AsymptoticCore

-- ASYM-NOGO-ALG-001 — identidade eventual das normalizações.
example (N : ℝ → ℝ) (α : ℝ) :
    ∀ᶠ T : ℝ in atTop,
      N T / T ^ α =
        (N T / (T * Real.log T)) * (Real.log T * T ^ (1 - α)) :=
  eventually_normalization_identity N α

-- ASYM-NOGO-PL-001 — caso α < 1.
example {α : ℝ} (hα : α < 1) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop atTop :=
  tendsto_powerLogFactor_atTop_of_lt_one hα

-- ASYM-NOGO-PL-002 — caso α = 1 (redução exata e divergência).
example {α : ℝ} (hα : α = 1) (T : ℝ) :
    Real.log T * T ^ (1 - α) = Real.log T :=
  powerLogFactor_eq_log_of_eq_one hα T

example {α : ℝ} (hα : α = 1) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop atTop :=
  tendsto_powerLogFactor_atTop_of_eq_one hα

-- ASYM-NOGO-PL-003 — caso α > 1.
example {α : ℝ} (hα : 1 < α) :
    Tendsto (fun T : ℝ => Real.log T * T ^ (1 - α)) atTop (nhds 0) :=
  tendsto_powerLogFactor_nhds_zero_of_one_lt hα

-- ASYM-NOGO-001 — teorema principal.
example (N : ℝ → ℝ) (α c C : ℝ) (hα : 0 < α) (hc : 0 < c) (hC : 0 < C)
    (hTLog : Tendsto (fun T : ℝ => N T / (T * Real.log T)) atTop (nhds c))
    (hPower : Tendsto (fun T : ℝ => N T / T ^ α) atTop (nhds C)) :
    False :=
  asym_nogo_001 N α c C hα hc hC hTLog hPower

-- O enunciado do probe está provado.
example : TamesisLab.RHNogo.AsymNogoStatement :=
  TamesisLab.RHNogo.asymNogoStatement_holds

end TamesisLab.Tests.RHNogoAsymptotic001
