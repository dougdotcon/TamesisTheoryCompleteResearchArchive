---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T16:30:00-03:00
canonical_commit: "3f72ad0cf19e523f5b714d2d078cd71f3e44c46f"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-FUNCTIONAL-GRAPH-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "portfolio-review-result.json"
current_blocker: null
next_single_action: >
  Preparar a especificação formal da decomposição de grafos
  funcionais finitos, sem executar provas.
authorized_action: "FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED"
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
  - "Não formalizar FOUND-FUNCTIONAL-GRAPH-001 antes de sua especificação estar pronta"
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
FOUND-FUNCTIONAL-GRAPH-001   SCOPED      ativo; so especificacao autorizada
FOUND-SEMIGROUP-002          VERIFIED    encerrado, APPROVED, sem extensao
RH-NOGO-001                  FROZEN_PARTIAL_RESULT
```

## Frente selecionada

**Grafos funcionais finitos**: `X` finito, `f : X → X`, cada estado com
exatamente uma transição seguinte. A pergunta muda de escala em relação a
`FOUND-SEMIGROUP-002` — lá era **uma trajetória**, aqui é a **estrutura
global** do grafo.

Resultado estrutural candidato:

> Cada componente contém um ciclo dirigido, e todo estado do componente
> alcança esse ciclo após um número finito de iterações.

Consequência direta de `exists_eventual_period`, já verificado.

O resultado **mais forte** — unicidade do ciclo por componente conexa —
**não está autorizado** antes da especificação, porque depende de qual
noção de "componente" for adotada (`FFG-GAP-002`, `FFG-GAP-004`).

## Trava renomeada

`NO_ACTION_AUTHORIZED` → `PORTFOLIO_REVIEW_REQUIRED`, atomicamente, nos
pontos acoplados: allowlist do `labctl.py`, `LAB_STATE`, `RESEARCH_QUEUE`,
`STATUS.yaml` e `CLOSURE_RECORD.md` de `FOUND-SEMIGROUP-002`.

Registros históricos — o JSON de resultado da revisão anterior, as sessões
e o changelog — **não** foram reescritos: eles documentam o que o gate
daquele momento decidiu, com o nome que a trava tinha então.

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

Decomposição de grafos funcionais em ciclos com árvores de entrada é
material padrão. O valor é formal e de reutilização.

## Próxima ação

Preparar a especificação. **Nenhuma prova. Nenhum arquivo Lean.**
