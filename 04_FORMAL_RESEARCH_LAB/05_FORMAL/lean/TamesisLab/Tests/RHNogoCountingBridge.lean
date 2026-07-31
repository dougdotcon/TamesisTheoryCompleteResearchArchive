import TamesisLab.RHNogo.Bridge

set_option autoImplicit false

/-!
# COUNTING-LAW-BRIDGE — teste isolado

Importa a ponte e referencia cada definição e cada teorema rastreável, com
as assinaturas originais. Verifica que a constante é preservada.

`ASYM-NOGO-001` **não** é aplicado em lugar algum deste arquivo.
-/

namespace TamesisLab.Tests.RHNogoCountingBridge

open Filter Asymptotics TamesisLab.RHNogo.Bridge

-- Definições.
example (T : ℝ) : tLogScale T = T * Real.log T := tLogScale_eq T
example : (ℝ → ℝ) → Type := PowerCountingLaw
example : (ℝ → ℝ) → Type := TLogCountingLaw
example : (ℝ → ℝ) → (ℝ → ℝ) → (ℝ → ℝ) → Prop := SubdominantDifference
example : (ℝ → ℝ) → (ℝ → ℝ) → Prop := SubdominantTLog
example : (ℝ → ℝ) → (ℝ → ℝ) → Prop := EventualEquality
example : (ℝ → ℝ) → (ℝ → ℝ) → Prop := BoundedDifference
example : (ℝ → ℝ) → (ℝ → ℝ) → Prop := RatioEquivalence

-- CLB-SCALE-001.
example : ∀ᶠ T : ℝ in atTop, T * Real.log T ≠ 0 :=
  eventually_tLogScale_ne_zero

-- CLB-SCALE-002.
example : Tendsto (fun T : ℝ => T * Real.log T) atTop atTop :=
  tendsto_tLogScale_atTop

-- CLB-SCALE-003.
example (c : ℝ) :
    Tendsto (fun T : ℝ => c * (T * Real.log T) / (T * Real.log T))
      atTop (nhds c) :=
  tendsto_const_mul_tLogScale_div c

-- CLB-LO-001.
example (NTarget NBase : ℝ → ℝ) (h : SubdominantTLog NTarget NBase) :
    Tendsto (fun T => (NTarget T - NBase T) / (T * Real.log T))
      atTop (nhds 0) :=
  subdominantDifference_tendsto_zero h

-- CLB-ALG-001a e CLB-ALG-001.
example (NTarget NBase : ℝ → ℝ) (T : ℝ) :
    NTarget T / (T * Real.log T) =
      NBase T / (T * Real.log T) +
        (NTarget T - NBase T) / (T * Real.log T) :=
  target_normalization_eq NTarget NBase T

example (NTarget NBase : ℝ → ℝ) :
    ∀ᶠ T : ℝ in atTop,
      NTarget T / (T * Real.log T) =
        NBase T / (T * Real.log T) +
          (NTarget T - NBase T) / (T * Real.log T) :=
  eventually_target_normalization_eq NTarget NBase

-- COUNTING-LAW-BRIDGE.
example (NTarget NBase : ℝ → ℝ) (c : ℝ)
    (hbase : Tendsto (fun T => NBase T / (T * Real.log T)) atTop (nhds c))
    (hsmall : SubdominantTLog NTarget NBase) :
    Tendsto (fun T => NTarget T / (T * Real.log T)) atTop (nhds c) :=
  counting_law_bridge hbase hsmall

-- COUNTING-LAW-BRIDGE-STRUCT, com preservação da constante.
example (NTarget NBase : ℝ → ℝ) (hbase : TLogCountingLaw NBase)
    (hsmall : SubdominantTLog NTarget NBase) : TLogCountingLaw NTarget :=
  TLogCountingLaw.transfer hbase hsmall

example (NTarget NBase : ℝ → ℝ) (hbase : TLogCountingLaw NBase)
    (hsmall : SubdominantTLog NTarget NBase) :
    (TLogCountingLaw.transfer hbase hsmall).constant = hbase.constant :=
  TLogCountingLaw.transfer_constant hbase hsmall

-- Enunciado registrado, provado.
example : CountingLawBridgeStatement := countingLawBridgeStatement_holds

-- STRONG-TLOG-COROLLARY.
example (N r : ℝ → ℝ) (c : ℝ)
    (hN : ∀ T, N T = c * (T * Real.log T) + r T)
    (hr : r =o[atTop] fun T => T * Real.log T) :
    Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c) :=
  tendsto_tLog_of_eq_main_add_littleO hN hr

-- Hierarquia E0 ⟹ E1 ⟹ E2.
example (NTarget NBase : ℝ → ℝ) (h : EventualEquality NTarget NBase) :
    SubdominantTLog NTarget NBase :=
  subdominantTLog_of_eventualEquality h

example (NTarget NBase : ℝ → ℝ) (h : BoundedDifference NTarget NBase) :
    SubdominantTLog NTarget NBase :=
  subdominantTLog_of_boundedDifference h

example (NTarget NBase : ℝ → ℝ) (h : EventualEquality NTarget NBase) :
    BoundedDifference NTarget NBase :=
  boundedDifference_of_eventualEquality h

end TamesisLab.Tests.RHNogoCountingBridge
