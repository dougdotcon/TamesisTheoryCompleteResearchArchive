---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-IDENTIFIER-CANONICALIZATION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
previous_candidate_id: FOUND-FINITE-ABSTRACTION-001
canonical_work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
aliases_active: 0
duplicate_work_items: 0
---

# Canonicalização do identificador

## O conflito real

O gate de revisão de portfólio que selecionou esta frente registrou o
identificador `FOUND-FINITE-ABSTRACTION-001`. Os gates de especificação
e de revisão exigiram `FOUND-FINITE-STATE-ABSTRACTION-001`. As duas
formas circularam simultaneamente, e `PROGRAM_STATE_AND_ROADMAP.md`
chegou a recomendar a resolução na direção oposta à adotada aqui.

Duas formas ativas para o mesmo item disparariam `STOP-ABS-017`.

## Decisão

```yaml
canonical_work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
authorization_prefix: FOUND_FINITE_STATE_ABSTRACTION_001_
previous_candidate_id: FOUND-FINITE-ABSTRACTION-001
aliases_active: 0
duplicate_work_items: 0
```

A forma canônica é `FOUND-FINITE-STATE-ABSTRACTION-001`. Ela nomeia o
objeto que a frente realmente estuda: a abstração de **estados finitos**,
consumindo `CertifiedFiniteEncoding A n`, e não uma noção genérica de
abstração finita.

## Superfície operacional migrada

```text
LAB_STATE.md                      active_work_item, authorized_action
01_PORTFOLIO/RESEARCH_QUEUE.yaml  work_item_id, authorized_next_gate
10_TOOLS/labctl.py                gate de sequencia e allowlist
PROGRAM_STATE_AND_ROADMAP.md      recomendacao anterior revertida
01_PORTFOLIO/FINITE_ABSTRACTION_CANDIDATE.md  work_item_id
CHANGELOG.md                      entrada nova
```

## Referências históricas preservadas

Os artefatos abaixo são registros imutáveis de gates encerrados e
**permanecem** com o nome candidato anterior. Eles não constituem um
segundo work item ativo:

```text
portfolio-review-after-certified-encoding-result.json
portfolio-review-after-runtime-adapter-result.json
01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_CERTIFIED_ENCODING.md
01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_RUNTIME_ADAPTER.md
01_PORTFOLIO/NEXT_TARGET_COMPARISON_MATRIX.md
01_PORTFOLIO/NEXT_TARGET_COMPARISON_AFTER_ENCODING.md
09_SESSIONS/2026/2026-08-01_2359_PORTFOLIO-REVIEW-AFTER-CERTIFIED-ENCODING.md
CHANGELOG.md (entradas anteriores)
```

Critério de conformidade: nenhum arquivo **operacional** — estado, fila,
ferramenta de validação — pode conter a forma anterior; a fila não pode
conter dois itens; a allowlist não pode conter dois prefixos.

## Verificação

```text
um unico work_item_id na fila                    SIM
um unico active_work_item                        SIM
um unico prefixo de autorizacao na allowlist     SIM
aliases operacionais ativos                      0
work items duplicados                            0
```
