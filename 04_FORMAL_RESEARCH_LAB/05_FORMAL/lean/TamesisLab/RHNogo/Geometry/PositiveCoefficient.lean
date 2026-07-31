import Mathlib.MeasureTheory.Measure.OpenPos
import Mathlib.MeasureTheory.Integral.Bochner.Basic

set_option autoImplicit false

/-!
# RH-NOGO-001 — Geometry / PositiveCoefficient

Núcleo **abstrato e elementar** por trás das obrigações GWB-008A e GWB-008B.

Aviso de escopo, explícito e vinculante: este módulo é teoria da medida
pura. Ele **não** define variedade, fibrado cotangente, operador
pseudodiferencial, símbolo principal, medida de Liouville nem coeficiente
de Weyl concreto. Esses objetos permanecem **documentais**
(`WEYL_COEFFICIENT_POSITIVITY.md`). Nada aqui prova a lei de Weyl.

O que este módulo fornece é somente o invólucro que converte
"o conjunto contém um aberto não vazio" em "sua medida é positiva", e daí
em "o coeficiente é positivo".
-/

namespace TamesisLab.RHNogo.Geometry

open MeasureTheory

/-- Interface de saída: um coeficiente real positivo.

**Não** está associada a operador algum. Representa apenas o dado que
`PowerCountingLaw` exige. -/
structure PositiveWeylCoefficient where
  coefficient : ℝ
  coefficient_pos : 0 < coefficient

/-- ELEMENTARY_INTERFACE_LEMMA — o expoente `d/m` é positivo quando `d ≥ 1`
(logo `d > 0`) e `m > 0`.

Não é um resultado espectral: é aritmética de reais positivos. Justifica a
exigência `d ≥ 1` acrescentada à classe, sem a qual `PowerCountingLaw` não
poderia ser satisfeita. -/
theorem dimension_div_order_pos {d m : ℝ} (hd : 0 < d) (hm : 0 < m) :
    0 < d / m :=
  div_pos hd hm

/-- GWB-008A-CORE — se um conjunto contém um aberto não vazio e a medida é
positiva em abertos não vazios, então o conjunto tem medida positiva.

Este é o **único** conteúdo formalizado de GWB-008A. A parte geométrica —
que `{p_m < 1}` de fato contém tal aberto — é documental. -/
theorem measure_pos_of_isOpen_subset {X : Type*} [TopologicalSpace X]
    {_ : MeasurableSpace X} (μ : Measure X) [μ.IsOpenPosMeasure]
    {U S : Set X} (hU : IsOpen U) (hne : U.Nonempty) (hsub : U ⊆ S) :
    0 < μ S :=
  lt_of_lt_of_le (hU.measure_pos μ hne) (measure_mono hsub)

/-- GWB-008B-CORE — o produto de uma normalização positiva por um volume
positivo é positivo. -/
theorem coefficient_pos_of_factors {normalization volume : ℝ}
    (hn : 0 < normalization) (hv : 0 < volume) :
    0 < normalization * volume :=
  mul_pos hn hv

/-- Construtor da interface a partir de dois fatores positivos. -/
def PositiveWeylCoefficient.ofFactors {normalization volume : ℝ}
    (hn : 0 < normalization) (hv : 0 < volume) : PositiveWeylCoefficient where
  coefficient := normalization * volume
  coefficient_pos := coefficient_pos_of_factors hn hv

@[simp]
theorem PositiveWeylCoefficient.ofFactors_coefficient
    {normalization volume : ℝ} (hn : 0 < normalization) (hv : 0 < volume) :
    (PositiveWeylCoefficient.ofFactors hn hv).coefficient =
      normalization * volume := rfl

/-- Variante integral do núcleo: a integral de uma função não negativa é
positiva exatamente quando seu suporte tem medida positiva. Reutiliza
diretamente `MeasureTheory.integral_pos_iff_support_of_nonneg`. -/
theorem integral_pos_of_nonneg_of_support_measure_pos {X : Type*}
    {_ : MeasurableSpace X} (μ : Measure X) (f : X → ℝ)
    (hf : 0 ≤ f) (hfi : Integrable f μ)
    (hsupport : 0 < μ (Function.support f)) :
    0 < ∫ x, f x ∂μ :=
  (integral_pos_iff_support_of_nonneg hf hfi).mpr hsupport

end TamesisLab.RHNogo.Geometry
