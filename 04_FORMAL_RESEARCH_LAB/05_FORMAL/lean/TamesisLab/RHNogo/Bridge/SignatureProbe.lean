import TamesisLab.RHNogo.Bridge.Definitions

set_option autoImplicit false

/-!
# RH-NOGO-001 — Bridge / SignatureProbe (registro histórico)

Este arquivo foi criado no gate `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION` para
registrar as **assinaturas** da ponte antes de qualquer prova.

Atualização (gate `COUNTING-LAW-BRIDGE`, 2026-07-31): as definições foram
**promovidas** para `Bridge/Definitions.lean`, onde passaram a ser a fonte
canônica, e a ponte foi provada em `Bridge/CountingLawBridge.lean`. Este
arquivo permanece apenas como registro das ferramentas verificadas antes da
formalização; não redefine nada.
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

#check @PowerCountingLaw
#check @TLogCountingLaw
#check @SubdominantDifference
#check @SubdominantTLog
#check @EventualEquality
#check @BoundedDifference
#check @RatioEquivalence
#check @CountingLawBridgeStatement

-- Ferramentas Mathlib previstas no gate de especificação e efetivamente
-- usadas na prova.
#check @Asymptotics.IsLittleO.tendsto_div_nhds_zero
#check @Filter.Tendsto.add
#check @Filter.Tendsto.congr

end TamesisLab.RHNogo.Bridge
