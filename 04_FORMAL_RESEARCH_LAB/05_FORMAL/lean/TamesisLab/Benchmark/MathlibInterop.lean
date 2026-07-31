import Mathlib.Data.Finset.Insert
import TamesisLab.Benchmark.Structures

/-!
# LAB-BENCH-001 — MathlibInterop: uso mínimo e controlado de Mathlib

Benchmark de infraestrutura. Este arquivo importa um único módulo da Mathlib
(`Mathlib.Data.Finset.Insert`) e verifica pertencimento a um singleton de
`Finset` sobre o tipo enumerado do benchmark, que possui igualdade decidível
derivada. Resultado elementar e conhecido. Valor científico:
NONE — INFRASTRUCTURE BENCHMARK.

Rastreabilidade: 05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md
(BENCH-MATHLIB-001).
-/

namespace TamesisLab.Benchmark

/-- `alpha` pertence ao singleton `{alpha}` como `Finset`. Teste controlado
de interoperabilidade com Mathlib. Resultado conhecido. -/
theorem alpha_mem_singleton :
    Regime.alpha ∈ ({Regime.alpha} : Finset Regime) :=
  Finset.mem_singleton_self Regime.alpha

/-- `beta` não pertence ao singleton `{alpha}` como `Finset`. Resultado
conhecido. -/
theorem beta_not_mem_singleton :
    Regime.beta ∉ ({Regime.alpha} : Finset Regime) := by
  simp

end TamesisLab.Benchmark
