import TamesisLab.RHNogo.Composition.Corollaries

set_option autoImplicit false

/-!
# ABSTRACT-NOGO-001 — Audit

Registro de assinaturas. Nenhum resultado novo.

Confirma também, por typecheck, que os dois componentes reutilizados são os
já verificados — `counting_law_bridge` e `asym_nogo_001` — e que nada da
pasta `Geometry/` entra na cadeia.
-/

namespace TamesisLab.RHNogo.Composition.Audit

section Local

#check @TamesisLab.RHNogo.Composition.abstract_power_tlog_incompatibility
#check @TamesisLab.RHNogo.Composition.AbstractCountingNogoData
#check @TamesisLab.RHNogo.Composition.AbstractCountingNogoData.false
#check @TamesisLab.RHNogo.Composition.AbstractNogoStatement
#check @TamesisLab.RHNogo.Composition.abstractNogoStatement_holds
#check @TamesisLab.RHNogo.Composition.abstract_nogo_of_eventuallyEq
#check @TamesisLab.RHNogo.Composition.abstract_nogo_of_boundedDifference

end Local

section Reused

-- COUNTING-LAW-BRIDGE (verificado no gate anterior).
#check @TamesisLab.RHNogo.Bridge.counting_law_bridge
#check @TamesisLab.RHNogo.Bridge.TLogCountingLaw.transfer
#check @TamesisLab.RHNogo.Bridge.TLogCountingLaw.transfer_constant
#check @TamesisLab.RHNogo.Bridge.subdominantTLog_of_eventualEquality
#check @TamesisLab.RHNogo.Bridge.subdominantTLog_of_boundedDifference

-- ASYM-NOGO-001 (verificado dois gates atrás).
#check @TamesisLab.RHNogo.AsymptoticCore.asym_nogo_001

end Reused

end TamesisLab.RHNogo.Composition.Audit
