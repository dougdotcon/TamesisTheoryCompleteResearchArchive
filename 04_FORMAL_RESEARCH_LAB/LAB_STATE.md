---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T16:30:00-03:00
canonical_commit: "3f6d7e785ba8bd90a35f33f7dc889f1234a7b650"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-FUNCTIONAL-GRAPH-001"
work_status: "VERIFIED"
formalization_status: "VERIFIED"
result_review: "APPROVED"
extension_status: "NOT_AUTHORIZED"
specification_status: "APPROVED"
evidence_level: "F"
last_verified_artifact: "found-functional-graph-001-result-review.json"
current_blocker: null
next_single_action: >
  Aguardar um gate explícito de revisão de portfólio.
  Nenhuma extensão de FOUND-FUNCTIONAL-GRAPH-001 está autorizada.
authorized_action: "PORTFOLIO_REVIEW_REQUIRED"
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
  - "Não afirmar unicidade de ponto periódico, de representante, de μ ou de período"
  - "Não afirmar ponte com SimpleGraph, árvores ou distância mínima"
  - "PORTFOLIO_REVIEW_REQUIRED é trava, não autorização: nenhum gate pode agir sob ela"
  - "Não aplicar a recíproca de periodicOrbit a pontos não periódicos — órbitas vazias são iguais sem encontro"
  - "Não apresentar periodicOrbit como algoritmo executável — é noncomputável"
  - "Não estender FOUND-FUNCTIONAL-GRAPH-001 nem abrir FOUND-FUNCTIONAL-GRAPH-002 sem gate próprio"
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
FOUND-FUNCTIONAL-GRAPH-001   VERIFIED / result_review APPROVED   ENCERRADO
FOUND-SEMIGROUP-002          VERIFIED / APPROVED                 ENCERRADO
RH-NOGO-001                  FROZEN_PARTIAL_RESULT               congelado

authorized_action: PORTFOLIO_REVIEW_REQUIRED   (trava, nao execucao)
```

**Nenhuma frente ativa.** A escolha do próximo trabalho exige um gate
explícito de revisão de portfólio.

## Força exata do resultado encerrado

```text
Para cada estado inicial x, existe entrada limitada numa orbita periodica.

Todos os pontos periodicos do componente de x, definido por
EventuallyMeets, pertencem a MESMA orbita periodica.
```

**Não** provado: componente como conjunto ou quociente, representante
canônico, menor `μ`, enumeração da bacia, grafo subjacente, conexidade em
`SimpleGraph`, decomposição em árvores, unicidade global de ciclo.

## A ressalva que precisa sobreviver

```text
A reciproca EXIGE ambos os pontos periodicos.

Dois pontos NAO periodicos tem ambos periodicOrbit = Cycle.nil. As orbitas
vazias sao iguais SEM que as trajetorias se encontrem.
```

## Limite computacional

`periodicOrbit` é **noncomputável**. O resultado não fornece algoritmo de
enumeração de componentes, cálculo de `μ` ou detecção de ciclo.

## Auditoria da revisão

```text
16 declaracoes publicas, 1 auxiliar private
5 instancias, todas em contraexemplos; ZERO no nucleo
0 conflitos; umbrella nao ambiguo
DecidableEq ausente de todos; Fintype so na existencia
zero Setoid, zero SimpleGraph, zero Quotient
pigeonhole nao reaplicado; ∃! ausente
FGR-001..008 todos CONFIRMADOS
```

Gaps: **onze resolvidos, quatro abertos** (`006`, `007`, `012`, `014`).

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Próxima ação

Aguardar gate de revisão de portfólio. Nada mais está autorizado.
