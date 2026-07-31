import TamesisLab.RHNogo.Geometry
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

set_option autoImplicit false

/-!
# Teste isolado — núcleo de positividade (GWB-008A / GWB-008B)

Verifica o núcleo de teoria da medida em instâncias concretas, sem
mencionar operador, variedade ou lei de Weyl.
-/

namespace TamesisLab.Tests.RHNogoPositiveCoefficient

open MeasureTheory TamesisLab.RHNogo.Geometry

/-- O expoente `α = d/m` é positivo para `d ≥ 1` e `m > 0`.
Instância numérica: `d = 3`, `m = 2`. -/
example : (0 : ℝ) < 3 / 2 :=
  dimension_div_order_pos (by norm_num) (by norm_num)

/-- Forma geral com `d ≥ 1` explícito, como exigido pela classe refinada. -/
example (d m : ℝ) (hd : 1 ≤ d) (hm : 0 < m) : 0 < d / m :=
  dimension_div_order_pos (lt_of_lt_of_le zero_lt_one hd) hm

/-- GWB-008A-CORE numa instância concreta: a medida de Lebesgue da bola
unitária aberta de `ℝ` é positiva, pois a bola contém um aberto não vazio
(ela própria). -/
example : 0 < volume (Set.Ioo (-1 : ℝ) 1) :=
  measure_pos_of_isOpen_subset volume isOpen_Ioo
    ⟨0, by norm_num⟩ (subset_refl _)

/-- Monotonicidade explícita: um superconjunto de um aberto não vazio
também tem medida positiva. -/
example : 0 < volume (Set.Icc (-2 : ℝ) 2) :=
  measure_pos_of_isOpen_subset volume isOpen_Ioo (U := Set.Ioo (-1 : ℝ) 1)
    ⟨0, by norm_num⟩ (fun x hx => ⟨by linarith [hx.1], by linarith [hx.2]⟩)

/-- GWB-008B-CORE: normalização positiva vezes volume positivo. -/
example : 0 < (2 : ℝ) * 5 :=
  coefficient_pos_of_factors (by norm_num) (by norm_num)

/-- A interface produz de fato um `PositiveWeylCoefficient`. -/
example : PositiveWeylCoefficient :=
  PositiveWeylCoefficient.ofFactors (normalization := 2) (volume := 5)
    (by norm_num) (by norm_num)

/-- E o coeficiente produzido é o produto, por `rfl`. -/
example :
    (PositiveWeylCoefficient.ofFactors (normalization := (2 : ℝ))
      (volume := (5 : ℝ)) (by norm_num) (by norm_num)).coefficient
      = 2 * 5 := rfl

/-- Todo `PositiveWeylCoefficient` tem coeficiente positivo — é o único
dado que a interface `PowerCountingLaw` consome. -/
example (C : PositiveWeylCoefficient) : 0 < C.coefficient :=
  C.coefficient_pos

end TamesisLab.Tests.RHNogoPositiveCoefficient
