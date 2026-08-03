---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-THEOREM-IMPLEMENTATION-MAP
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Mapa especificação → implementação

Cada linha liga uma assinatura congelada ao arquivo que a realiza.

| Especificado em | Declaração | Implementado em |
|---|---|---|
| `FINAL_DATA_MODEL.md` | `CertifiedFiniteAbstraction` | `FiniteStateAbstraction/Abstraction.lean` |
| `ITERATION_CORRESPONDENCE.md` | `CertifiedFiniteAbstraction.iterate_commutes` | `FiniteStateAbstraction/Abstraction.lean` |
| `ABSTRACT_ANALYSIS_BRIDGE.md` | `analyzeAbstractSystem` | `FiniteStateAbstraction/AbstractAnalysis.lean` |
| `FINAL_ABSTRACT_COMPLETENESS.md` | `analyzeAbstractSystem_complete` | `FiniteStateAbstraction/AbstractAnalysis.lean` |
| `FINAL_OBSERVATIONAL_SOUNDNESS.md` | `analyzeAbstractSystem_observational_sound` | `FiniteStateAbstraction/Observation.lean` |
| `FINAL_ORBIT_SEPARATION.md` | `OrbitSeparating` | `FiniteStateAbstraction/OrbitSeparation.lean` |
| `FINAL_REFLECTED_SOUNDNESS.md` | `analyzeAbstractSystem_reflected_sound` | `FiniteStateAbstraction/OrbitSeparation.lean` |
| `COUNTEREXAMPLE_REVIEW.md` | `BOOL_TO_UNIT` inteiro | `FiniteStateAbstraction/Counterexample.lean` |

## Desvios em relação à especificação

```text
nenhum
```

As sete assinaturas públicas foram implementadas **letra por letra** como
congeladas nos documentos `FINAL_*`.

## Decisão de organização, dentro da liberdade autorizada

`orbitSeparating_of_injective` era `DEFERRED_OPTIONAL`. Ele foi
reconstruído dentro de `Tests/FoundFiniteStateAbstraction001.lean`,
único lugar que o consome, em vez de entrar na API pública. Isso mantém
`PUBLIC_TOTAL = 7`.

`naive_cycle_reflection_is_false` era `TEST_ONLY` na especificação e foi
implementado em `Counterexample.lean`, junto do restante do
contraexemplo, por coesão. Ele **não** é contado como declaração
pública: o módulo do contraexemplo inteiro é material de teste, e o
`Audit.lean` o expõe apenas para leitura.

## Ordem de imports

```text
Abstraction        → Engineering.FiniteStateEncoding
AbstractAnalysis   → Abstraction
Observation        → AbstractAnalysis
OrbitSeparation    → Observation
Counterexample     → OrbitSeparation
Audit              → Counterexample
```

Linear. Nenhum ciclo. `Foundations.lean` importa o agregador e o
`Audit`; `Engineering` nunca importa `Foundations.lean`, apenas
`Foundations.CycleDetection`, de modo que a inclusão não fecha ciclo.
