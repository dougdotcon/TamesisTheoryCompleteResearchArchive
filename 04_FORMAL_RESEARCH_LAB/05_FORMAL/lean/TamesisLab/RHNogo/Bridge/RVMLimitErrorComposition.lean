import TamesisLab.RHNogo.Bridge.RVMLimit

set_option autoImplicit false

/-!
# RVM-LIMIT-ERROR — composição de dois termos `o(T log T)`

Fecha, como item de Onda 2 (`WAVE2-RH-1`, plano `RH-1`), o gap
`RVM-LIMIT-ERROR` registrado no planejamento (`PLANO_DE_ATAQUE_ONDA_2`):
compor **dois** termos `o(T log T)` — um vindo de um erro genérico
`e = O(log T)` (via `IsBigO.trans_isLittleO`, composto com
`log T = o(T log T)`), o outro vindo da fórmula simbólica de
Riemann–von Mangoldt já fechada em `RVMLimit.lean`
(`tendsto_rvmLimitFormula_div_tLogScale`) — e invocar
`tendsto_tLog_of_eq_main_add_littleO` (`SB-GAP-010A`, já fechado em
`StrongAsymptoticCorollary.lean`) para concluir que a soma continua a
satisfazer a mesma lei `T log T` com a mesma constante `1/(2π)`.

Interpretação: o teorema principal desta arquivo mostra que anexar à
fórmula simbólica de von Mangoldt um erro **genérico** qualquer que seja
apenas `O(log T)` — a ordem de grandeza do termo de erro real `RVM-STRONG`,
que `RVMLimit.lean` omite explicitamente — **não muda** o limite
`N(T)/(T log T) → 1/(2π)`. Isto é aritmética de `little-o`/`big-O` pura;
`e` é uma função `ℝ → ℝ` arbitrária satisfazendo a hipótese, não a
função de contagem de zeros de zeta nem qualquer objeto analítico
específico.

**O que isto NÃO estabelece:** nada sobre `ζ`, seus zeros, ou se o termo
de erro real de Riemann–von Mangoldt (`O(log T)` de fato, com constante
explícita) satisfaz a hipótese `e =O[atTop] log` — isso continua sendo
`SB-GAP-010B`, fora do alcance atual, exatamente como em `RVMLimit.lean`.

Independente de: função zeta, zeros, Riemann–von Mangoldt, operadores, lei
de Weyl, PDE, Hilbert–Pólya e da classe `W-ELLIPTIC`.

scientific_novelty: STANDARD_ASYMPTOTIC_COMPOSITION_FORMALIZED_FOR_LOCAL_USE
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

/-- Passo (a), parte fixa: `log T = o(T log T)`. Provado via
`isLittleO_iff_tendsto'`, reduzindo a `(log T)/(T log T) → 0`, que é
`T⁻¹ → 0` fora de um conjunto onde `log T = 0` (i.e. `T ≤ 1`), tratado
eventualmente via `eventually_tLogScale_ne_zero`. -/
theorem log_isLittleO_tLogScale :
    (fun T : ℝ => Real.log T) =o[atTop] fun T => T * Real.log T := by
  have hg0 : ∀ᶠ T : ℝ in atTop, T * Real.log T = 0 → Real.log T = 0 := by
    filter_upwards [eventually_tLogScale_ne_zero] with T hT h
    exact absurd h hT
  refine (isLittleO_iff_tendsto' hg0).mpr ?_
  refine Tendsto.congr' ?_ (tendsto_inv_atTop_zero (𝕜 := ℝ))
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with T hT
  have hT0 : T ≠ 0 := ne_of_gt (lt_trans zero_lt_one hT)
  have hlogT : Real.log T ≠ 0 := ne_of_gt (Real.log_pos hT)
  field_simp

/-- Passo (a): qualquer erro `e = O(log T)` já é `o(T log T)`. Composição
direta via `IsBigO.trans_isLittleO`, exatamente como pedido pelo teste:
`e =O[atTop] log T` seguido de `log T =o[atTop] (T log T)`. -/
theorem littleO_tLogScale_of_isBigO_log
    {e : ℝ → ℝ} (he : e =O[atTop] fun T => Real.log T) :
    e =o[atTop] fun T => T * Real.log T :=
  he.trans_isLittleO log_isLittleO_tLogScale

/-- Passo (b): a diferença entre a fórmula simbólica de von Mangoldt e seu
termo principal `(1/2π)·(T log T)` é `o(T log T)`. Extraído de
`tendsto_rvmLimitFormula_div_tLogScale` via `isLittleO_iff_tendsto'`, o
inverso do que `subdominantDifference_tendsto_zero` faz (little-o ⟹
tendsto 0); aqui vamos de tendsto (a um `c` genérico) até little-o. -/
theorem rvmLimitFormula_subdominant :
    (fun T : ℝ =>
        ((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
              - T / (2 * Real.pi) + 7 / 8)
          - (1 / (2 * Real.pi)) * (T * Real.log T))
      =o[atTop] fun T : ℝ => T * Real.log T := by
  have hg0 : ∀ᶠ T : ℝ in atTop, T * Real.log T = 0 →
      ((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
            - T / (2 * Real.pi) + 7 / 8)
        - (1 / (2 * Real.pi)) * (T * Real.log T) = 0 := by
    filter_upwards [eventually_tLogScale_ne_zero] with T hT h
    exact absurd h hT
  refine (isLittleO_iff_tendsto' hg0).mpr ?_
  have hsub :=
    tendsto_rvmLimitFormula_div_tLogScale.sub_const (1 / (2 * Real.pi))
  rw [sub_self] at hsub
  refine Tendsto.congr' ?_ hsub
  filter_upwards [eventually_tLogScale_ne_zero] with T hT
  rw [sub_div, mul_div_assoc, div_self hT, mul_one]

/-- **RVM-LIMIT-ERROR (`WAVE2-RH-1`).** Se `e` é um erro genérico
`O(log T)` — a ordem de grandeza do termo de erro real de
Riemann–von Mangoldt, aqui tratado apenas como hipótese abstrata, sem
`ζ` — então a fórmula simbólica de von Mangoldt **mais** `e` ainda
satisfaz `N(T)/(T log T) → 1/(2π)`, a mesma constante de
`tendsto_rvmLimitFormula_div_tLogScale`. Composição de dois termos
`o(T log T)` (passo (a) + passo (b)) seguida por
`tendsto_tLog_of_eq_main_add_littleO` (`SB-GAP-010A`), exatamente como
especificado pelo teste falsificável `RH-1`. -/
theorem tendsto_rvmLimitFormula_add_error_div_tLogScale
    {e : ℝ → ℝ} (he : e =O[atTop] fun T => Real.log T) :
    Tendsto
      (fun T : ℝ =>
        (((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
              - T / (2 * Real.pi) + 7 / 8) + e T) / (T * Real.log T))
      atTop (nhds (1 / (2 * Real.pi))) := by
  have hN : ∀ T : ℝ,
      (((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
              - T / (2 * Real.pi) + 7 / 8) + e T)
        = (1 / (2 * Real.pi)) * (T * Real.log T) +
          ((((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
                    - T / (2 * Real.pi) + 7 / 8)
                - (1 / (2 * Real.pi)) * (T * Real.log T)) + e T) := by
    intro T; ring
  have hr :
      (fun T : ℝ =>
          (((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
                    - T / (2 * Real.pi) + 7 / 8)
                - (1 / (2 * Real.pi)) * (T * Real.log T)) + e T)
        =o[atTop] fun T : ℝ => T * Real.log T :=
    rvmLimitFormula_subdominant.add (littleO_tLogScale_of_isBigO_log he)
  exact tendsto_tLog_of_eq_main_add_littleO hN hr

end TamesisLab.RHNogo.Bridge

#print axioms TamesisLab.RHNogo.Bridge.log_isLittleO_tLogScale
#print axioms TamesisLab.RHNogo.Bridge.littleO_tLogScale_of_isBigO_log
#print axioms TamesisLab.RHNogo.Bridge.rvmLimitFormula_subdominant
#print axioms TamesisLab.RHNogo.Bridge.tendsto_rvmLimitFormula_add_error_div_tLogScale
