---
document_id: FSG2-FINAL-GAP-STATUS
work_item_id: FOUND-SEMIGROUP-002
---

# FOUND-SEMIGROUP-002 — Estado final dos gaps

Classificações: `RESOLVED_FORMALLY`, `RESOLVED_BY_API_AUDIT`,
`RESOLVED_BY_DESIGN`, `OPEN_DEFERRED`, `OPEN_BIBLIOGRAPHIC`, `SUPERSEDED`.

```yaml
- gap_id: FSG2-GAP-001
  title: Mathlib orbit API suitability
  final_status: RESOLVED_BY_API_AUDIT
  evidence: >
    MulAction.orbit reutilizada; reachable_iff_mem_orbit eh Iff.rfl.
    Auditoria confirmou que NAO existe segunda definicao publica de
    orbita na frente.

- gap_id: FSG2-GAP-002
  title: Exact pigeonhole lemma for bounded repetition
  final_status: RESOLVED_FORMALLY
  evidence: >
    Fintype.exists_ne_map_eq_of_card_lt aplicado a
    g : Fin (card X + 1) -> X em exists_bounded_iterate_collision.
    Uso unico confirmado por busca textual.

- gap_id: FSG2-GAP-002b
  title: minimalPeriod nao captura periodicidade eventual
  final_status: RESOLVED_BY_DESIGN
  evidence: >
    minimalPeriod NAO eh usado (4 mencoes, todas em comentarios; 0 usos).
    MulAction.period: 0 ocorrencias. A ponte com a API oficial eh
    periodic_tail_of_collision, aplicada ao ponto f^[mu] x. CE-003 torna a
    armadilha detectavel: s0_not_periodic prova que o estado inicial nao
    eh periodico para periodo positivo algum.

- gap_id: FSG2-GAP-003
  title: Iterate-action identity
  final_status: RESOLVED_FORMALLY
  evidence: >
    smul_iterate_apply usado em monoid_element_eventually_periodic e em
    ..._propagates. Nenhum lema local foi criado.

- gap_id: FSG2-GAP-004
  title: Sharp cardinal bounds for mu and lambda
  final_status: RESOLVED_FORMALLY
  evidence: >
    mu < card X, 0 < lam, mu + lam <= card X estao na conclusao de
    exists_bounded_iterate_collision e de exists_eventual_period.
  residual: >
    Os limitantes sao SUFICIENTES, nao afirmados como OTIMOS. A
    otimalidade exigiria minimalidade — ver FSG2-GAP-004b.

- gap_id: FSG2-GAP-004b
  title: Decomposicao unica em cauda e ciclo
  final_status: OPEN_DEFERRED
  reason: >
    Excluida da meta C apos analise de custo: cinco obrigacoes novas
    (minimalidade de mu, minimalidade de lam, unicidade do par,
    injetividade no segmento inicial, estrutura ciclica), com a parte de
    divisibilidade dependendo de lemas de Dynamics/PeriodicPts nao
    auditados. NAO fechado.

- gap_id: FSG2-GAP-004c
  title: DecidableEq X eh hipotese ociosa?
  final_status: RESOLVED_FORMALLY
  evidence: >
    Confirmado pela assinatura impressa:
    @exists_eventual_period : forall {X} [inst : Fintype X] ...
    A hipotese foi OMITIDA e o teorema compila.

- gap_id: FSG2-GAP-005
  title: Propagation from one collision to full eventual periodicity
  final_status: RESOLVED_FORMALLY
  evidence: >
    collision_propagates formalizado. Function.iterate_add_apply
    localizado na fonte (Mathlib/Logic/Function/Iterate.lean:76),
    resolvendo tambem o NAME_UNCERTAIN da viabilidade.

- gap_id: FSG2-GAP-006
  title: Preorder representation without unsafe global instance
  final_status: RESOLVED_BY_DESIGN
  evidence: >
    Nenhuma instance Preorder criada — confirmado por busca: 1 ocorrencia
    de "Preorder", num comentario que declara a exclusao. Registrados
    apenas reachable_isRefl (Std.Refl) e reachable_isTrans (IsTrans),
    ambos theorem.

- gap_id: FSG2-GAP-007
  title: Counterexample encoding strategy
  final_status: OPEN_DEFERRED
  partially_resolved: >
    A estrategia de codificacao FOI decidida: tipos indutivos proprios com
    Fintype manual, provas por decide sobre no maximo 8 casos, sem
    native_decide.
  residual: >
    A negativa "o periodo pode depender do estado inicial" continua SEM
    contraexemplo e NAO eh afirmada em documento algum. NAO fechado, por
    exigencia explicita do gate.

- gap_id: FSG2-GAP-008
  title: Boundary between standard result and future Tamesis modelling
  final_status: RESOLVED_BY_DESIGN
  evidence: >
    NOVELTY_BOUNDARY.md, RESULT_BOUNDARY.md e C3_BOUNDARY.md sao
    vinculantes e trazem tabelas de "nao escrever / escrever". Nenhuma
    ponte com TRI/TDTR foi construida.

- gap_id: FSG2-GAP-009
  title: Bibliografia primaria nao auditada
  final_status: OPEN_BIBLIOGRAPHIC
  reason: >
    Nenhuma fonte primaria de teoria de semigrupos ou de dinamica discreta
    foi obtida ou auditada. NAO fechado, por exigencia explicita do gate.
  binding_consequence: >
    Nenhuma afirmacao de prioridade historica ou atribuicao a autor eh
    permitida.
```

## Resumo

| Classificação | Gaps |
|---|---|
| `RESOLVED_FORMALLY` | `002`, `003`, `004`, `004c`, `005` — **5** |
| `RESOLVED_BY_API_AUDIT` | `001` — **1** |
| `RESOLVED_BY_DESIGN` | `002b`, `006`, `008` — **3** |
| `OPEN_DEFERRED` | `004b`, `007` — **2** |
| `OPEN_BIBLIOGRAPHIC` | `009` — **1** |
| `SUPERSEDED` | — **0** |

**Doze gaps, nove resolvidos, três abertos.** Nenhum foi fechado sem
evidência: `FSG2-GAP-007` continua aberto por falta de contraexemplo, e
`FSG2-GAP-009` por falta de auditoria bibliográfica — exatamente como o
gate exigiu.
