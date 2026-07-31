---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T23:20:00-03:00
canonical_commit: "ab79032062cddf195671208058820993cfaabe76"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-CYCLE-DETECTION-001"
work_status: "READY"
evidence_level: "F"
last_verified_artifact: "found-cycle-detection-001-specification-result.json"
current_blocker: null
specification_status: "READY_FOR_REVIEW"
next_single_action: >
  Revisar a enumeração de certificados, a executabilidade do
  detector parcial, a completude por reutilização da colisão
  limitada e a viabilidade de totalização sem escolha clássica.
authorized_action: "FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED"
closed_work_items:
  FOUND-SEMIGROUP-002:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
  FOUND-FUNCTIONAL-GRAPH-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
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
  - "Não formalizar FOUND-CYCLE-DETECTION-001 antes de sua especificação ser revista"
  - "Não criar arquivos Lean sob a autorização atual"
  - "Não implementar Floyd, Brent ou tabela visitada — ambos DEFERRED_OPTIMIZATION"
  - "Não desviar do algoritmo congelado BOUNDED_CERTIFICATE_SEARCH sem gate próprio"
  - "Não acrescentar campos a CycleWitness — entryPoint é derivável e foi rejeitado"
  - "Não chamar prefixIndex de entryIndex nem de comprimento exato da cauda"
  - "Não chamar period de minimalPeriod"
  - "Não usar Classical.choose na função executável"
  - "Não marcar o detector como noncomputable"
  - "Não autorizar o wrapper total antes de checar #eval — CD-GAP-017"
  - "Não decidir igualdade de Function.periodicOrbit — é noncomputável"
  - "Não afirmar minimalidade de μ ou de λ sem prova e sem gate próprio"
  - "Não autorizar extração de código nem integração com sistemas reais"
  - "Não repetir a casa dos pombos: ela foi consumida uma única vez em FOUND-SEMIGROUP-002"
  - "Não enumerar todos os componentes na primeira versão"
  - "Não acrescentar DecidableEq X sem necessidade verificada na especificação (CD-GAP-004)"
  - "Não tratar FOUND-CYCLE-DETECTION-001 como extensão de FOUND-FUNCTIONAL-GRAPH-001"
  - "Não estender FOUND-FUNCTIONAL-GRAPH-001 nem abrir FOUND-FUNCTIONAL-GRAPH-002 sem gate próprio"
  - "Não estender FOUND-SEMIGROUP-002 nem abrir FOUND-SEMIGROUP-003 sem gate próprio"
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md ocorra e seja verificada"
  - "Não conectar a nova frente a TRI, TDTR, teoria de tudo, tempo físico, entropia, mecânica quântica ou cosmologia"
  - "Não conectar a nova frente à Hipótese de Riemann, Hilbert–Pólya ou qualquer conjectura Clay"
  - "Não afirmar novo algoritmo, nova teoria de grafos, nova lei de dinâmica ou descoberta matemática"
  - "Não tratar reutilização em software como descoberta científica"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/README.md"
  - "02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/SPECIFICATION_DECISION.md"
  - "01_PORTFOLIO/NEXT_WORK_ITEM_CYCLE_DETECTION.md"
  - "02_FOUNDATIONS/04_FUNCTIONAL_GRAPHS/FOUND_FUNCTIONAL_GRAPH_001/PUBLIC_API.md"
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
