import TamesisLab.Foundations.UniformPrimrec.Analysis

set_option autoImplicit false

/-!
# FOUND-UNIFORM-PRIMREC-001 — instancia positiva, TEST_ONLY

Tabela habitada de dois estados, `0 -> 1 -> 0`. Os dois lados do
casamento sao avaliados concretamente nos testes.
-/

namespace TamesisLab.Foundations.UniformPrimrec

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.ComputabilityBridge

def twoCycle : RawTransitionTable := ⟨#[1, 0]⟩

end TamesisLab.Foundations.UniformPrimrec
