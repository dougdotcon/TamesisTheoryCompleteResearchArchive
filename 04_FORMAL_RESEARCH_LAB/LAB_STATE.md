---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T11:50:00-03:00
canonical_commit: "39e3d95925a7038da307017216dd4cb8e49c572a"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-SEMIGROUP-002"
work_status: "READY"
evidence_level: "F"
last_verified_artifact: "found-semigroup-002-specification-result.json"
current_blocker: null
next_single_action: >
  Formalizar o núcleo aprovado de alcançabilidade, invariantes e
  periodicidade eventual para funções em tipos finitos, sem executar
  extensões físicas ou alegações Tamesis.
authorized_action: "FOUND_SEMIGROUP_002_FORMALIZATION_AUTHORIZED"
frozen_work_items:
  RH-NOGO-001: "FROZEN_PARTIAL_RESULT desde 2026-07-31, commit c186ab59; ver 03_MILLENNIUM/01_RIEMANN/RH_NOGO_FREEZE_RECORD.md"
prohibited_actions:
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md tenha ocorrido e sido verificada"
  - "Não tratar mais capacidade computacional ou um modelo de IA mais forte como critério de reativação"
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não instanciar PowerCountingLaw com um operador"
  - "Não instanciar TLogCountingLaw com a função zeta"
  - "Não formalizar teoria pseudodiferencial, lei de Weyl ou Riemann–von Mangoldt concreto"
  - "Não apresentar ABSTRACT-NOGO-001 como no-go espectral, como refutação de Hilbert–Pólya ou como progresso sobre RH"
  - "Não apresentar ABSTRACT-NOGO-001 como novidade matemática"
  - "Não apresentar W-ELLIPTIC-SCALAR-BRIDGE como classe copiada da literatura — seis das doze condições são deste laboratório"
  - "Não incluir decomposição única de órbitas na primeira formalização (FSG2-GAP-004b)"
  - "Não usar Function.minimalPeriod nem MulAction.period como período eventual (FSG2-GAP-002b)"
  - "Não criar instância global Preorder para alcançabilidade (FSG2-GAP-006)"
  - "Não afirmar negativa sem contraexemplo planejado"
  - "Não apresentar periodicidade eventual como novidade matemática"
  - "Não confundir o modelo finito de FOUND-SEMIGROUP-002 com teoria geral de semigrupos"
  - "Não reutilizar o modelo finito como suporte de alegação física ou espectral"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "03_MILLENNIUM/01_RIEMANN/RH_NOGO_FREEZE_RECORD.md"
  - "03_MILLENNIUM/01_RIEMANN/RH_NOGO_RESULT_BOUNDARY.md"
  - "03_MILLENNIUM/01_RIEMANN/RH_NOGO_REACTIVATION_CRITERIA.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/README.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/THEOREM_CANDIDATES.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/NOVELTY_BOUNDARY.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/DECISION_LEDGER.yaml"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

```text
FOUND-SEMIGROUP-002   READY    especificacao pronta; formalizacao autorizada
RH-NOGO-001           FROZEN_PARTIAL_RESULT   congelado, NAO descartado
```

## O que a especificação fixou

Três camadas separadas por construção, com a regra de que **todo teorema
vai para a camada mais fraca em que ainda faz sentido**:

```text
CAMADA A   acao completa de M      alcancabilidade, orbita, invariantes
CAMADA B   um gerador a fixo       corolario DERIVADO
CAMADA C   funcao finita (X, f)    periodicidade eventual vive AQUI
```

Alvo: `C. CORE_BOUNDS_AND_PROPAGATION` — existência da colisão, limitantes
em `Fintype.card X` e propagação. **Decomposição única em cauda + ciclo
fica fora**, com custo analisado (`FSG2-GAP-004b`).

Onze teoremas candidatos, cinco contraexemplos planejados, doze gaps
registrados.

## Achados da auditoria da Mathlib

```text
smul_iterate_apply      EXISTE  -> FSG2-GAP-003 resolvido pela API
mem_orbit_iff           Iff.rfl -> ponte alcancabilidade/orbita custa zero
pigeonhole              EXISTE  -> Fintype.exists_ne_map_eq_of_card_lt
periodicidade eventual  AUSENTE -> enunciado sera local
minimalPeriod           ARMADILHA: devolve 0 fora de periodicPts
```

## Preflight desta sessão

`canonical_commit` atualizado de `c186ab59` para `39e3d95` **antes** de
qualquer trabalho, e a política textual corrigida. A validação de
ancestralidade passou a ser executada por `labctl validate` como **erro**,
com distinção entre exit `1` (não ancestral) e outros códigos (erro do
git). Sete testes cobrem a tabela de decisão sem tocar no histórico.

## Novidade

**Zero.** Periodicidade eventual em conjunto finito é o princípio da casa
dos pombos. `NOVELTY_BOUNDARY.md` é vinculante. Bibliografia primária
`NOT_AUDITED`, logo nenhuma afirmação de prioridade histórica é permitida.

## Próxima ação

Formalizar o núcleo aprovado. **Somente ele.**
