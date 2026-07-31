import TamesisLab.RHNogo.Bridge.LittleOTransfer

set_option autoImplicit false

/-!
# COUNTING-LAW-BRIDGE — teorema principal

Transferência da lei `T log T` entre duas funções cuja diferença é
`o(T log T)`.

Nota sobre hipóteses ociosas: a positividade `0 < c` **não é necessária**
para a transferência do limite e foi **removida** do teorema técnico. Ela
permanece apenas em `TLogCountingLaw`, onde é parte da interface.
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

/-- **COUNTING-LAW-BRIDGE.** Se `NBase` normalizada por `T log T` tende a
`c`, e `NTarget − NBase = o(T log T)`, então `NTarget` normalizada pela
mesma escala tende ao **mesmo** `c`. -/
theorem counting_law_bridge
    {NTarget NBase : ℝ → ℝ} {c : ℝ}
    (hbase : Tendsto (fun T => NBase T / (T * Real.log T)) atTop (nhds c))
    (hsmall : SubdominantTLog NTarget NBase) :
    Tendsto (fun T => NTarget T / (T * Real.log T)) atTop (nhds c) := by
  have hsum := hbase.add (subdominantDifference_tendsto_zero hsmall)
  rw [add_zero] at hsum
  exact hsum.congr fun T => (target_normalization_eq NTarget NBase T).symm

/-- COUNTING-LAW-BRIDGE-STRUCT — versão estrutural: a interface
`TLogCountingLaw` transfere-se, **com a mesma constante**.

É `def`, e não `theorem`, porque `TLogCountingLaw` vive em `Type`: ela
carrega o dado `constant` além das hipóteses. -/
def TLogCountingLaw.transfer
    {NTarget NBase : ℝ → ℝ}
    (hbase : TLogCountingLaw NBase)
    (hsmall : SubdominantTLog NTarget NBase) :
    TLogCountingLaw NTarget where
  constant := hbase.constant
  constant_pos := hbase.constant_pos
  tendsto_normalized :=
    counting_law_bridge hbase.tendsto_normalized hsmall

/-- A constante é literalmente preservada pela transferência. -/
@[simp]
theorem TLogCountingLaw.transfer_constant
    {NTarget NBase : ℝ → ℝ}
    (hbase : TLogCountingLaw NBase)
    (hsmall : SubdominantTLog NTarget NBase) :
    (TLogCountingLaw.transfer hbase hsmall).constant = hbase.constant := rfl

/-- O enunciado registrado em `Definitions.lean` está provado. -/
theorem countingLawBridgeStatement_holds : CountingLawBridgeStatement :=
  fun _ _ _ hbase hsmall => counting_law_bridge hbase hsmall

end TamesisLab.RHNogo.Bridge
