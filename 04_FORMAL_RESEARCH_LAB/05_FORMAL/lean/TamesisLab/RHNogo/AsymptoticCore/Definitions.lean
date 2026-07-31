import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# ASYM-NOGO-001 — Definitions

Normalizações usadas no núcleo assintótico abstrato.

Nada aqui menciona a função zeta, seus zeros, operadores, PDE ou a lei de
Weyl. O objeto é uma função real arbitrária `N : ℝ → ℝ`.

As definições são `noncomputable` por dependerem de `Real.log` e da divisão
real; isso é herdado da Mathlib e não introduz axioma algum.

scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE
-/

namespace TamesisLab.RHNogo.AsymptoticCore

/-- Escala `T ↦ T · log T`. -/
noncomputable def tLogScale (T : ℝ) : ℝ := T * Real.log T

/-- Normalização de `N` pela escala `T log T`. -/
noncomputable def normalizeTLog (N : ℝ → ℝ) (T : ℝ) : ℝ := N T / tLogScale T

/-- Normalização de `N` pela potência `T ^ α`. -/
noncomputable def normalizeRpow (N : ℝ → ℝ) (α T : ℝ) : ℝ := N T / T ^ α

/-- Fator de comparação entre as duas escalas: `log T · T ^ (1 - α)`. -/
noncomputable def powerLogFactor (α T : ℝ) : ℝ := Real.log T * T ^ (1 - α)

@[simp]
theorem tLogScale_eq (T : ℝ) : tLogScale T = T * Real.log T := rfl

@[simp]
theorem normalizeTLog_eq (N : ℝ → ℝ) (T : ℝ) :
    normalizeTLog N T = N T / (T * Real.log T) := rfl

@[simp]
theorem normalizeRpow_eq (N : ℝ → ℝ) (α T : ℝ) :
    normalizeRpow N α T = N T / T ^ α := rfl

@[simp]
theorem powerLogFactor_eq (α T : ℝ) :
    powerLogFactor α T = Real.log T * T ^ (1 - α) := rfl

end TamesisLab.RHNogo.AsymptoticCore
