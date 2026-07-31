import TamesisLab.RHNogo.AsymptoticCore.Incompatibility
import TamesisLab.RHNogo.SignatureProbe

set_option autoImplicit false

/-!
# ASYM-NOGO-001 — Audit

Verificações de escopo por typecheck. Confirma que o teorema principal fecha
com a assinatura pretendida e que o enunciado registrado em
`TamesisLab/RHNogo/SignatureProbe.lean` (`AsymNogoStatement`) é agora um
teorema, e não apenas uma `Prop`.

Nenhum resultado novo é introduzido aqui.
-/

namespace TamesisLab.RHNogo.AsymptoticCore

open Filter

-- Assinatura final do teorema principal.
example : ∀ (N : ℝ → ℝ) (α c C : ℝ), 0 < α → 0 < c → 0 < C →
    Tendsto (fun T : ℝ => N T / (T * Real.log T)) atTop (nhds c) →
    Tendsto (fun T : ℝ => N T / T ^ α) atTop (nhds C) → False :=
  fun N α c C hα hc hC h₁ h₂ => asym_nogo_001 N α c C hα hc hC h₁ h₂

-- Forma contrapositiva usada na aplicação futura: dada a normalização por
-- `T log T`, nenhuma normalização por potência positiva é possível.
theorem not_tendsto_normalizeRpow_of_tendsto_normalizeTLog
    (N : ℝ → ℝ) (α c C : ℝ) (hα : 0 < α) (hc : 0 < c) (hC : 0 < C)
    (hTLog : Tendsto (fun T : ℝ => N T / (T * Real.log T)) atTop (nhds c)) :
    ¬ Tendsto (fun T : ℝ => N T / T ^ α) atTop (nhds C) :=
  fun hPower => asym_nogo_001 N α c C hα hc hC hTLog hPower

end TamesisLab.RHNogo.AsymptoticCore

namespace TamesisLab.RHNogo

/-- O enunciado registrado em `SignatureProbe.lean` está agora provado. -/
theorem asymNogoStatement_holds : AsymNogoStatement :=
  fun N c C α hc hC hα hTLog =>
    AsymptoticCore.not_tendsto_normalizeRpow_of_tendsto_normalizeTLog
      N α c C hα hc hC hTLog

end TamesisLab.RHNogo
