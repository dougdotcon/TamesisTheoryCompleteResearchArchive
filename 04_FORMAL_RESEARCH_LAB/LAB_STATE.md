---
schema: tamesis-formal-lab-state/1
updated_at: 2026-08-01T05:40:00-03:00
canonical_commit: "a4907b7cb2b421ccb52fc0262bf276ef2d94f8a9"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "engineering_foundation"
active_work_item: "ENG-FINITE-STATE-RUNTIME-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "portfolio-review-finite-state-runtime-result.json"
current_blocker: null
next_single_action: >
  Preparar a especificação de um adaptador executável que valide
  uma tabela dinâmica de transições, construa uma função total
  sobre Fin n e aplique o detector certificado de ciclos.
authorized_action: "ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_PREPARATION_AUTHORIZED"
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
  FOUND-CYCLE-DETECTION-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    totalization_status: DEFERRED
    extraction_status: NOT_AUTHORIZED
    optimization_status: NOT_AUTHORIZED
    minimality_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
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
governance_rules:
  post_commit_validation: >
    Quando uma auditoria obrigatória falhar depois do primeiro commit e
    amend e commit corretivo estiverem ambos proibidos, parar com
    GATE_POST_COMMIT_VALIDATION_FAILED e aguardar gate corretivo explícito.
  truncated_output: >
    Não assumir sucesso a partir de saída truncada. Toda etapa de patch
    termina com verificação independente do efeito.
prohibited_actions:
  - "Não criar arquivos Lean sob a autorização atual"
  - "Não implementar o adaptador antes de sua especificação estar pronta"
  - "Não corrigir destinos inválidos por módulo, clamp ou fallback silencioso"
  - "Não converter estado inicial inválido por módulo"
  - "Não permitir que a tabela validada aponte para fora do domínio"
  - "Não usar Classical.choose para produzir dados"
  - "Não depender de Function.periodicOrbit na execução"
  - "Não reimplementar o detector nem a casa dos pombos"
  - "Não misturar parsing JSON, CSV, arquivo ou rede com o núcleo formal"
  - "Não incluir servidor, banco de dados ou interface web na primeira versão"
  - "Não tornar Floyd, Brent ou a totalização dependências obrigatórias"
  - "Não declarar automaticamente correta a abstração de um sistema real em estados finitos"
  - "Não afirmar complexidade sem modelo de custo"
  - "Não formalizar Floyd, Brent ou tabela visitada — todos NOT_AUTHORIZED"
  - "Não estender FOUND-CYCLE-DETECTION-001 nem abrir FOUND-CYCLE-DETECTION-002 sem gate próprio"
  - "Não estender FOUND-FUNCTIONAL-GRAPH-001 nem FOUND-SEMIGROUP-002 sem gate próprio"
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md ocorra e seja verificada"
  - "Não registrar testes que importam TamesisLab dentro de TamesisLab.lean — import circular"
  - "Não conectar a nova frente a TRI, TDTR, teoria de tudo, física, Hipótese de Riemann ou conjectura Clay"
  - "Não afirmar novo modelo de computação, novo algoritmo, nova teoria de autômatos ou descoberta"
  - "Não tratar reutilização em software como descoberta científica"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "01_PORTFOLIO/NEXT_WORK_ITEM_FINITE_STATE_RUNTIME.md"
  - "01_PORTFOLIO/PORTFOLIO_REVIEW_FINITE_STATE_RUNTIME.md"
  - "02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/PUBLIC_API.md"
  - "02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/RESULT_BOUNDARY.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "último relatório em 09_SESSIONS/"
---# Estado atual

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
