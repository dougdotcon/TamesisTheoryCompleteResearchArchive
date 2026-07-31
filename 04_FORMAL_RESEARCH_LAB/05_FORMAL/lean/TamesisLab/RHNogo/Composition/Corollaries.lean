import TamesisLab.RHNogo.Composition.AbstractNogo

set_option autoImplicit false

/-!
# ABSTRACT-NOGO-001 — corolários E0 e E1

Reutilizam as conversões **já verificadas** em
`Bridge/StrongAsymptoticCorollary.lean`:

```text
E0 => E2   subdominantTLog_of_eventualEquality
E1 => E2   subdominantTLog_of_boundedDifference
```

Nenhum crescimento de `T log T` é reprovado aqui: o lema auxiliar
`tendsto_norm_tLogScale_atTop` já existe e é usado indiretamente.

O nível **E3** (equivalência por razão, `RatioEquivalence`) **não é
formalizado**: sua ligação a E2 exige positividade e controle eventual do
denominador (`SB-GAP-011`, aberto por desenho).
-/

namespace TamesisLab.RHNogo.Composition

open Filter TamesisLab.RHNogo.Bridge

/-- **ABSTRACT-NOGO-E0-001** — o mesmo resultado sob igualdade eventual.

Se `NTarget` obedece a uma lei de potência positiva, `NBase` obedece a uma
lei `T log T` positiva, e as duas coincidem eventualmente, obtém-se `False`. -/
theorem abstract_nogo_of_eventuallyEq
    {NTarget NBase : ℝ → ℝ}
    (hPower : PowerCountingLaw NTarget)
    (hTLog : TLogCountingLaw NBase)
    (hEq : NTarget =ᶠ[Filter.atTop] NBase) :
    False :=
  abstract_power_tlog_incompatibility hPower hTLog
    (subdominantTLog_of_eventualEquality hEq)

/-- **ABSTRACT-NOGO-E1-001** — o mesmo resultado sob diferença limitada.

Autorizado porque a conversão `BoundedDifference ⟹ SubdominantTLog` já
está verificada (`subdominantTLog_of_boundedDifference`). -/
theorem abstract_nogo_of_boundedDifference
    {NTarget NBase : ℝ → ℝ}
    (hPower : PowerCountingLaw NTarget)
    (hTLog : TLogCountingLaw NBase)
    (hBounded : BoundedDifference NTarget NBase) :
    False :=
  abstract_power_tlog_incompatibility hPower hTLog
    (subdominantTLog_of_boundedDifference hBounded)

end TamesisLab.RHNogo.Composition
