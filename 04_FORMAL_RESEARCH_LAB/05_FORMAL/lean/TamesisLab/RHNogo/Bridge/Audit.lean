import TamesisLab.RHNogo.Bridge.StrongAsymptoticCorollary

set_option autoImplicit false

/-!
# COUNTING-LAW-BRIDGE — Audit

Verificações de escopo por typecheck.

Confirma o que **não** é usado: nenhum objeto desta pasta menciona `ζ`,
zeros, operadores, a lei de Weyl ou `ASYM-NOGO-001`.
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

-- Assinatura final do teorema principal, sem hipótese de positividade.
example : ∀ (NTarget NBase : ℝ → ℝ) (c : ℝ),
    Tendsto (fun T => NBase T / (T * Real.log T)) atTop (nhds c) →
    SubdominantTLog NTarget NBase →
    Tendsto (fun T => NTarget T / (T * Real.log T)) atTop (nhds c) :=
  fun _ _ _ hbase hsmall => counting_law_bridge hbase hsmall

-- A transferência estrutural preserva a constante.
example (NTarget NBase : ℝ → ℝ) (hbase : TLogCountingLaw NBase)
    (hsmall : SubdominantTLog NTarget NBase) :
    (TLogCountingLaw.transfer hbase hsmall).constant = hbase.constant := rfl

-- Hierarquia E0 ⟹ E1 ⟹ E2.
example (NTarget NBase : ℝ → ℝ) (h : EventualEquality NTarget NBase) :
    SubdominantTLog NTarget NBase :=
  subdominantTLog_of_boundedDifference
    (boundedDifference_of_eventualEquality h)

end TamesisLab.RHNogo.Bridge
