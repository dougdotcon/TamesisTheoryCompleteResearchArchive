import TamesisLab.RHNogo.Geometry.PositiveCoefficient

set_option autoImplicit false

/-!
# RH-NOGO-001 — Geometry / Audit

Registro de assinaturas do núcleo de teoria da medida e dos lemas Mathlib
efetivamente reutilizados.

Nada aqui aplica `ASYM-NOGO-001`, nada constrói um operador, nada afirma a
lei de Weyl.
-/

namespace TamesisLab.RHNogo.Geometry.Audit

open MeasureTheory

section LocalCore

-- Núcleo local (este gate).
#check @TamesisLab.RHNogo.Geometry.PositiveWeylCoefficient
#check @TamesisLab.RHNogo.Geometry.dimension_div_order_pos
#check @TamesisLab.RHNogo.Geometry.measure_pos_of_isOpen_subset
#check @TamesisLab.RHNogo.Geometry.coefficient_pos_of_factors
#check @TamesisLab.RHNogo.Geometry.PositiveWeylCoefficient.ofFactors
#check @TamesisLab.RHNogo.Geometry.integral_pos_of_nonneg_of_support_measure_pos

end LocalCore

section MathlibReuse

-- Lemas Mathlib reutilizados, inspecionados na revisão fixada
-- (v4.33.0-rc1, rev 79d0395a1825a6264ad5d269e35e60537518955e).
#check @IsOpen.measure_pos
#check @MeasureTheory.measure_mono
#check @MeasureTheory.Measure.IsOpenPosMeasure
#check @MeasureTheory.integral_pos_iff_support_of_nonneg
#check @MeasureTheory.Measure.measure_pos_of_nonempty_interior

end MathlibReuse

end TamesisLab.RHNogo.Geometry.Audit
