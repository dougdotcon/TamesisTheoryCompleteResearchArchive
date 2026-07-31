# RH-NOGO-001 — Mapa Lean

| Módulo | Conteúdo | Estado |
|---|---|---|
| `TamesisLab/RHNogo/SignatureProbe.lean` | `AsymNogoStatement` (registro histórico) | provado em `AsymptoticCore/Audit.lean` |
| `TamesisLab/RHNogo/AsymptoticCore/` | `ASYM-NOGO-001`: 4 definições, 12 teoremas | **VERIFIED** |
| `TamesisLab/Tests/RHNogoAsymptotic001.lean` | teste do núcleo | PASS |
| `TamesisLab/RHNogo/Bridge/Definitions.lean` | interfaces `PowerCountingLaw`, `TLogCountingLaw`, níveis E0–E3, `CountingLawBridgeStatement` | **VERIFIED** |
| `TamesisLab/RHNogo/Bridge/TLogScale.lean` | CLB-SCALE-001/002/003 | **VERIFIED** |
| `TamesisLab/RHNogo/Bridge/LittleOTransfer.lean` | CLB-LO-001, CLB-ALG-001a/001 | **VERIFIED** |
| `TamesisLab/RHNogo/Bridge/CountingLawBridge.lean` | `counting_law_bridge`, versão estrutural, preservação da constante | **VERIFIED** |
| `TamesisLab/RHNogo/Bridge/StrongAsymptoticCorollary.lean` | `STRONG-TLOG-COROLLARY` (SB-GAP-010A), E0⟹E1⟹E2 | **VERIFIED** |
| `TamesisLab/RHNogo/Bridge/Audit.lean` | verificações de escopo | **VERIFIED** |
| `TamesisLab/RHNogo/Bridge/SignatureProbe.lean` | registro histórico; não redefine nada | — |
| `TamesisLab/Tests/RHNogoCountingBridge.lean` | teste da ponte | PASS |
| (não previsto) operadores, lei de Weyl, `ζ` | — | fora de qualquer autorização |

Regra: nenhum arquivo desta frente pode aplicar `ASYM-NOGO-001`, formalizar
operadores, a lei de Weyl ou Riemann–von Mangoldt concreto.

`set_option autoImplicit false` está ativo em toda a pasta `Bridge/`.

## Componentes analíticos abstratos verificados

```text
COUNTING-LAW-BRIDGE   (VERIFIED)
          ↓
ASYM-NOGO-001         (VERIFIED)
```

Falta demonstrar que os objetos concretos satisfazem as interfaces.

## RHNogo/Geometry — núcleo de positividade (GWB-008A / GWB-008B)

| Arquivo | Conteúdo |
|---|---|
| `Geometry/PositiveCoefficient.lean` | `PositiveWeylCoefficient`, `ofFactors`, `dimension_div_order_pos`, `measure_pos_of_isOpen_subset`, `coefficient_pos_of_factors`, `integral_pos_of_nonneg_of_support_measure_pos` |
| `Geometry/Audit.lean` | `#check` do núcleo local e dos cinco lemas Mathlib reutilizados |
| `Geometry.lean` | agregador com o aviso de escopo |
| `Tests/RHNogoPositiveCoefficient.lean` | teste isolado, instâncias concretas em `ℝ` |

**Escopo, vinculante:** teoria da medida elementar. **Não** define
variedade, fibrado cotangente, operador pseudodiferencial, símbolo
principal, medida de Liouville nem coeficiente de Weyl concreto. Cobre o
passo 5 de seis do argumento de `GWB-008A` e a aritmética de `GWB-008B`.
**Não prova a lei de Weyl.** Ver `GEOMETRIC_LEAN_SCOPE.md`.
