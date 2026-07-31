---
document_id: FCD-SPECIFICATION-DECISION
decision: A_FOUND_CYCLE_DETECTION_001_SPECIFICATION_READY
---

# Decisão da especificação

```text
A. FOUND_CYCLE_DETECTION_001_SPECIFICATION_READY
```

## Critérios de `READY`

| Critério | Estado |
|---|---|
| algoritmo primário congelado | `BOUNDED_CERTIFICATE_SEARCH`, em `ALGORITHM_SELECTION.md` |
| estrutura de saída congelada | `CycleWitness` com dois naturais |
| semântica não mínima explicitada | `baseIndex` = índice-base de colisão; `period` = período testemunhado |
| domínio de candidatos completo | `μ < n`, `0 < λ`, `μ + λ ≤ n`; fronteira verificada por avaliação |
| terminação clara | estrutural, `List.find?` sobre lista finita |
| soundness planejada | `List.find?_some` + `decide_eq_true_eq` |
| completeness planejada | transporte de `exists_bounded_iterate_collision` |
| reutilização do collision theorem | termo a termo — o contrato **é** a conclusão do teorema |
| `DecidableEq` justificada | necessária na comparação executável; verificada na sonda; confinada à camada 2 |
| totalização avaliada | avaliada e **`DEFERRED`**; API v1 baseada em `Option` |
| `periodicPts` conectada | `periodic_tail_of_collision` + `mk_mem_periodicPts` |
| `periodicOrbit` mantida proposicional | nunca comparada computacionalmente |
| extração auditada | `EXTRACTION_FEASIBILITY.md`, `READY_FOR_FEASIBILITY_AUDIT` |
| Floyd e Brent diferidos | `DEFERRED_OPTIMIZATION` |
| gaps registrados | 19 |
| novidade zero preservada | `NONE` / `NONE` |
| nenhuma implementação executada | 0 arquivos Lean permanentes, 0 provas |

## Desvios deliberados em relação ao gate

Três, todos registrados e justificados:

1. **`mem_cycleCandidates_iff` não é dependência da soundness.** As cotas
   vivem dentro de `Valid`. Fortificação, não lacuna. Ver
   `CORRECTNESS_PLAN.md` e a correção do DAG em
   `THEOREM_DEPENDENCY_MAP.md`.
2. **Totalização `DEFERRED`**, não aprovada. Quatro das cinco condições
   têm argumento favorável; a quinta — `#eval` funcionar — só é
   verificável implementando, o que este gate proíbe.
3. **Dois nomes de API do gate divergem do checkout** e foram corrigidos
   contra o Lean real: `List.find?_eq_some` →
   `List.find?_eq_some_iff_append`; `Function.iterate` → `Nat.iterate`.

## Renomeações em relação ao gate de portfólio

| Antes | Agora | Motivo |
|---|---|---|
| `CycleDetectionResult` | `CycleWitness` | é um certificado, não uma resposta final |
| `entryIndex` | `prefixIndex` | `entry` sugere minimalidade não provada |
| `prefixIndex` | `baseIndex` | **superado na revisão** — `prefix` também podia ser lido como minimalidade |
| três campos | dois campos | `entryPoint` é derivável |

O gate de portfólio registrou explicitamente que a estrutura **não estava
congelada** e que a escolha caberia à especificação.

## Próximo passo

```yaml
authorized_action: FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED
```

Revisar a enumeração de certificados, a executabilidade do detector
parcial, a completude por reutilização da colisão limitada e a viabilidade
de totalização sem escolha clássica.

**Nenhuma formalização autorizada. Nenhum arquivo Lean. Floyd, Brent,
extração e integração permanecem não autorizados.**
