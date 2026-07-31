---
document_id: FFG-FINAL-GAP-STATUS
---

# FOUND-FUNCTIONAL-GRAPH-001 — Estado final dos gaps

```yaml
FFG-GAP-001:
  title: Representacao do componente funcional
  status: RESOLVED_BY_DESIGN
  evidence: "EventuallyMeets adotada; MutuallyReachable refutada por CE-004"

FFG-GAP-002:
  title: Prova de transitividade de EventuallyMeets
  status: RESOLVED_FORMALLY
  evidence: "eventuallyMeets_trans, dois casos por Nat.le_total, revisado linha a linha"

FFG-GAP-003:
  title: Diferenca entre alcance mutuo e componente
  status: RESOLVED_BY_COUNTEREXAMPLE
  evidence: "CE-004: EventuallyMeets f a b sem MutuallyReachable f a b"

FFG-GAP-004:
  title: Unicidade do ciclo como igualdade de periodicOrbit
  status: RESOLVED_FORMALLY
  evidence: "periodicOrbit_eq_of_eventuallyMeets; CE-005 refuta a leitura por ponto"

FFG-GAP-005:
  title: Recorrencia via periodicPts
  status: RESOLVED_BY_API_REUSE
  evidence: "periodicPts usada diretamente; nenhum alias IsRecurrent publicado"

FFG-GAP-006:
  title: Distancia minima ate o ciclo
  status: OPEN_DEFERRED

FFG-GAP-007:
  title: Representacao de arvores de entrada
  status: OPEN_DEFERRED

FFG-GAP-008:
  title: Necessidade real de DecidableEq
  status: RESOLVED_FORMALLY
  evidence: "assinaturas impressas: DecidableEq ausente de TODOS os teoremas"

FFG-GAP-009:
  title: Reutilizacao de exists_eventual_period
  status: RESOLVED_BY_DEPENDENCY_REUSE
  evidence: "exists_cyclePoint_reachable_with_bound; pigeonhole nao reaplicado"

FFG-GAP-010:
  title: Fronteira entre teorema padrao e aplicacoes de software
  status: RESOLVED_BY_BOUNDARY
  evidence: "RESULT_BOUNDARY.md e REUSE_MATRIX.md, vinculantes"

FFG-GAP-011:
  title: periodicOrbit API suitability
  status: RESOLVED_FORMALLY
  evidence: "CE003.orbit_eq por periodicOrbit_apply_iterate_eq, sem decide"

FFG-GAP-012:
  title: Equivalencia com conectividade fraca de SimpleGraph
  status: OPEN_DEFERRED

FFG-GAP-013:
  title: Representante unico versus objeto ciclo unico
  status: RESOLVED_BY_DESIGN
  evidence: "o objeto unico eh a orbita; CE-005 exibe dois representantes"

FFG-GAP-014:
  title: Bibliografia primaria nao auditada
  status: OPEN_BIBLIOGRAPHIC

FFG-GAP-015:
  title: Orientacao de iterate_add_apply nas testemunhas
  status: RESOLVED_FORMALLY
  evidence: "testemunhas d + mx, d + nz e b + a; chamadas com f explicito"
```

## Resumo

| Classificação | Gaps |
|---|---|
| `RESOLVED_FORMALLY` | `002`, `004`, `008`, `011`, `015` — **5** |
| `RESOLVED_BY_DESIGN` | `001`, `013` — **2** |
| `RESOLVED_BY_COUNTEREXAMPLE` | `003` — **1** |
| `RESOLVED_BY_API_REUSE` | `005` — **1** |
| `RESOLVED_BY_DEPENDENCY_REUSE` | `009` — **1** |
| `RESOLVED_BY_BOUNDARY` | `010` — **1** |
| `OPEN_DEFERRED` | `006`, `007`, `012` — **3** |
| `OPEN_BIBLIOGRAPHIC` | `014` — **1** |

**Quinze gaps, onze resolvidos, quatro abertos.** Os quatro abertos
**não** foram fechados: três por decisão de escopo, um por falta de fontes.

## Observação estrutural sem gap próprio

A ausência de contraexemplo para "dois pontos não periódicos com órbitas
vazias iguais que não se encontram" está registrada em `RESULT_REVIEW.md`
e `COUNTEREXAMPLE_REVIEW.md`. Não recebeu identificador de gap porque não
é uma lacuna do resultado — é uma limitação **da cobertura dos
contraexemplos**, e a limitação real (que o inverso exige periodicidade)
está corretamente expressa nas hipóteses do teorema.
