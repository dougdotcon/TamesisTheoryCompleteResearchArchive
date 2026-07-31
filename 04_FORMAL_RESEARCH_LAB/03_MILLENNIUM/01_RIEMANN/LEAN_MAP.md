# RH-NOGO-001 — Mapa Lean

| Módulo | Conteúdo | Estado |
|---|---|---|
| `TamesisLab/RHNogo/SignatureProbe.lean` | enunciado `AsymNogoStatement` (registro histórico) | provado em `AsymptoticCore/Audit.lean` |
| `TamesisLab/RHNogo/AsymptoticCore/` | `ASYM-NOGO-001`: 4 definições, 12 teoremas | **VERIFIED** |
| `TamesisLab/Tests/RHNogoAsymptotic001.lean` | teste de referência do núcleo | PASS |
| `TamesisLab/RHNogo/Bridge/SignatureProbe.lean` | interfaces `PowerCountingLaw`, `TLogCountingLaw`, `SubdominantDifference`, `EventualEquality`, `BoundedDifference`, `RatioEquivalence`, `CountingLawBridgeStatement`, `NarrowSpectralNogoStatement` | **assinaturas elaboradas, SEM provas** |
| (futuro) `TamesisLab/RHNogo/Bridge/CountingLawBridge.lean` | prova do `COUNTING-LAW-BRIDGE` | autorizado pelo próximo gate, não criado |
| (não previsto) operadores, lei de Weyl, `ζ` | — | fora de qualquer autorização |

Regra: nenhum arquivo desta frente pode conter prova da ponte, aplicação de
`ASYM-NOGO-001` ou formalização de operadores enquanto a autorização for de
especificação ou de formalização apenas das interfaces.

`set_option autoImplicit false` está ativo no probe da ponte, para impedir
captura silenciosa de identificadores desconhecidos.
