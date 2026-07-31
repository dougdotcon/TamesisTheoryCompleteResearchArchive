---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T11:50:00-03:00
canonical_commit: "b4ce2551cd9f3588030fc7281d7f8c7aa624bac3"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-SEMIGROUP-002"
work_status: "VERIFIED"
result_review: "APPROVED"
extension_status: "NOT_AUTHORIZED"
evidence_level: "F"
last_verified_artifact: "found-semigroup-002-result-review.json"
current_blocker: null
next_single_action: >
  Aguardar um gate separado de revisão de portfólio para selecionar
  o próximo work item. Nenhuma extensão de FOUND-SEMIGROUP-002
  está autorizada.
authorized_action: "NO_ACTION_AUTHORIZED"
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
  - "NO_ACTION_AUTHORIZED é trava, não autorização: nenhum gate pode agir sob ela"
  - "Não estender FOUND-SEMIGROUP-002 nem abrir FOUND-SEMIGROUP-003 sem gate próprio"
  - "Não formalizar decomposição canônica de órbitas sem gate próprio (FSG2-GAP-004b)"
  - "Não afirmar que as quatro propriedades de C3 falham simultaneamente em toda ação"
  - "Não afirmar que IsInvariantUnder é universalmente mais fraca que IsInvariant"
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
FOUND-SEMIGROUP-002   VERIFIED / result_review APPROVED   ENCERRADO
RH-NOGO-001           FROZEN_PARTIAL_RESULT               congelado

authorized_action: NO_ACTION_AUTHORIZED   (trava, nao execucao)
```

**Nenhuma frente tem autorização ativa.** A escolha do próximo trabalho
exige um gate separado de revisão de portfólio.

## FOUND-SEMIGROUP-002 — encerrado como fundação reutilizável

```text
17 declaracoes publicas, 1 auxiliar private, 11 instancias
0 instancias no nucleo matematico
0 conflitos de instancia; umbrella nao ambiguo
casa dos pombos usada 1 vez; minimalPeriod usado 0 vezes
sem DecidableEq X, Fintype M, Group M
FRR-001..FRR-007 todos CONFIRMADOS
```

Gaps: **nove resolvidos, três abertos** (`FSG2-GAP-004b`, `FSG2-GAP-007`,
`FSG2-GAP-009`). Encerrar a frente **não fecha** nenhum deles.

## Limites vinculantes

```yaml
mathematical_novelty: NONE
```

`RESULT_BOUNDARY.md`, `C3_BOUNDARY.md` e `NOVELTY_BOUNDARY.md` permanecem
vinculantes. A leitura correta de "propriedades de C3 falham em geral" é
que **para cada uma existe um contraexemplo** — não que todas falhem
simultaneamente em toda ação.

## RH-NOGO-001

`FROZEN_PARTIAL_RESULT` / `NOT_AUTHORIZED` / `NO_EXECUTION` / `DEFERRED`.
Reativação apenas por `REACT-001..005`.

## Próxima ação

Aguardar gate de revisão de portfólio. Nada mais está autorizado.
