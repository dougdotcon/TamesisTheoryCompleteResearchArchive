---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T16:30:00-03:00
canonical_commit: "df6adb93a3bf8c5570954c5a94b0701896be4877"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-FUNCTIONAL-GRAPH-001"
work_status: "READY"
specification_status: "READY_FOR_REVIEW"
evidence_level: "F"
last_verified_artifact: "found-functional-graph-001-specification-result.json"
current_blocker: null
next_single_action: >
  Revisar as definições de componente funcional, a unicidade
  por periodicOrbit e a viabilidade das assinaturas antes de
  autorizar formalização Lean.
authorized_action: "FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_AUTHORIZED"
closed_work_items:
  FOUND-SEMIGROUP-002:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
frozen_work_items:
  RH-NOGO-001:
    work_status: FROZEN_PARTIAL_RESULT
    authorization_state: NOT_AUTHORIZED
    execution_state: NO_EXECUTION
    concrete_layer_status: DEFERRED
governance_lock_renamed:
  from: NO_ACTION_AUTHORIZED
  to: PORTFOLIO_REVIEW_REQUIRED
  reason: "o sufixo _AUTHORIZED convidava a ler a trava como autorização"
  satisfied_by: PORTFOLIO_REVIEW
prohibited_actions:
  - "Não formalizar FOUND-FUNCTIONAL-GRAPH-001 antes da REVISÃO da especificação"
  - "Não definir componente funcional como MutuallyReachable (FFG-CE-004 refuta)"
  - "Não formular unicidade como existência de um único ponto periódico (FFG-CE-005 refuta)"
  - "Não importar SimpleGraph no núcleo (FFG-GAP-012 diferido)"
  - "Não acrescentar DecidableEq X sem necessidade verificada — a auditoria mostrou que não é necessária"
  - "Não criar instância global de Setoid, Preorder ou equivalência para EventuallyMeets"
  - "Não criar arquivos Lean sob a autorização atual"
  - "Não afirmar unicidade do ciclo por componente antes de FFG-GAP-002 e FFG-GAP-004"
  - "Não tratar FOUND-FUNCTIONAL-GRAPH-001 como extensão de FOUND-SEMIGROUP-002"
  - "Não estender FOUND-SEMIGROUP-002 nem abrir FOUND-SEMIGROUP-003 sem gate próprio"
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md ocorra e seja verificada"
  - "Não conectar a nova frente a TRI, TDTR, teoria de tudo, tempo físico, entropia, mecânica quântica ou cosmologia"
  - "Não conectar a nova frente à Hipótese de Riemann, Hilbert–Pólya ou qualquer conjectura Clay"
  - "Não afirmar nova lei universal, nova teoria de dinâmica, descoberta matemática ou descoberta física"
  - "Não apresentar decomposição de grafo funcional como novidade — é material padrão"
  - "Não tratar reutilização em software como descoberta científica"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "01_PORTFOLIO/NEXT_WORK_ITEM_DECISION.md"
  - "01_PORTFOLIO/PORTFOLIO_REVIEW_2026_07_31.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/PUBLIC_API.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/RESULT_BOUNDARY.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

```text
FOUND-FUNCTIONAL-GRAPH-001   READY / especificacao READY_FOR_REVIEW
FOUND-SEMIGROUP-002          VERIFIED / APPROVED / sem extensao
RH-NOGO-001                  FROZEN_PARTIAL_RESULT
```

**Formalização NÃO autorizada.** A próxima etapa é a **revisão** da
especificação — precisamente para que uma definição inadequada de
componente não seja congelada em Lean.

## A decisão que a especificação travou

```text
COMPONENTE FUNCIONAL := classe de EventuallyMeets
                        (exists m n, f^[m] x = f^[n] y)

NAO eh MutuallyReachable.
```

Contraexemplo decisivo `FFG-CE-004`:

```text
a → c
b → c
c → c
```

`a` e `b` estão no mesmo componente; nenhum alcança o outro.

## Unicidade — leitura vinculante

```text
"um ciclo por componente" significa que todos os pontos periodicos do
componente produzem a MESMA Function.periodicOrbit.

NAO significa um unico ponto periodico  (FFG-CE-005 refuta).
NAO significa representante canonico.
NAO significa ponto fixo               (FFG-CE-003 refuta).
```

## Achados da auditoria da Mathlib

```text
periodicPts                 exige periodo positivo POR DEFINICAO
periodicOrbit               Cycle a, SEM DecidableEq
periodicOrbit               NONCOMPUTAVEL: decide indisponivel para orbitas
periodicOrbit_apply_iterate_eq   da FFG-CYCLE-001 em tres passos
mk_mem_periodicPts          adaptador exato de exists_eventual_period
NOT_FOUND                   zero — toda a maquinaria de ciclos ja existe
```

Uma previsão do gate anterior foi **refutada**: `DecidableEq X` **não** é
necessária no núcleo.

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

Decomposição "forma rho" da iteração finita é material padrão.

## Próxima ação

Revisar a especificação. **Nenhuma prova. Nenhum arquivo Lean.**
