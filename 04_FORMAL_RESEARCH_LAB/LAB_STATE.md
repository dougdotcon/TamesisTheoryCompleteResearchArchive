---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T16:30:00-03:00
canonical_commit: "90fb4e26da33cebed2ba414ee5aeb663647de149"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-FUNCTIONAL-GRAPH-001"
work_status: "READY"
specification_status: "APPROVED"
evidence_level: "F"
last_verified_artifact: "found-functional-graph-001-specification-review-result.json"
current_blocker: null
next_single_action: >
  Formalizar o núcleo aprovado de alcance por iteração,
  encontro eventual, existência limitada de ponto cíclico e
  unicidade da órbita periódica do componente funcional.
authorized_action: "FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_AUTHORIZED"
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
  - "Não publicar IsRecurrent — usar x ∈ Function.periodicPts f"
  - "Não publicar SameFunctionalComponent nem componentSet sem uso na API pública"
  - "Não usar ∃! p : X no teorema principal"
  - "Não usar decide sobre igualdade de periodicOrbit (noncomputável)"
  - "Não desviar das assinaturas congeladas em FINAL_SIGNATURES.md sem gate próprio"
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
FOUND-FUNCTIONAL-GRAPH-001   READY / especificacao APPROVED
                             formalizacao AUTORIZADA
FOUND-SEMIGROUP-002          VERIFIED / APPROVED / sem extensao
RH-NOGO-001                  FROZEN_PARTIAL_RESULT
```

## Núcleo congelado

Três definições — `IterReachable`, `MutuallyReachable`, `EventuallyMeets` —
e **nove** teoremas, terminando em

```lean
exists_component_cycle_with_entry_bound
```

Assinaturas em `FINAL_SIGNATURES.md`; definições em
`FINAL_DEFINITIONS.md`. Desviar delas exige gate próprio.

## Três correções da revisão

```text
1. MutuallyReachable: semantica precisa por classes.
   "Classe unitaria" NAO distingue transitorio de ponto fixo — um ponto
   fixo tambem tem classe unitaria.

2. IsRecurrent RETIRADO. "Recorrencia" tem significados mais amplos em
   dinamica. Publico usa x ∈ Function.periodicPts f.

3. Testemunhas corrigidas: iterate_add_apply poe a contagem EXTERNA a
   esquerda, entao as testemunhas naturais sao d + mx e d + nz.
```

## Hipóteses congeladas

```text
relacoes e igualdade de orbitas    nenhuma finitude
existencia e teorema principal     [Fintype X]
DecidableEq X                      AUSENTE do nucleo
```

## Diferidos

```text
componentSet, Setoid, SimpleGraph, arvores, distancia minima,
representante canonico, classificacao completa.
```

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Próxima ação

Formalizar o núcleo aprovado. **Somente ele.**
