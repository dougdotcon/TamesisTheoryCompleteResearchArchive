---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T11:50:00-03:00
canonical_commit: "2b86a8809776774e4caf3a54d1469d240ecdaf1d"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-SEMIGROUP-002"
work_status: "VERIFIED"
evidence_level: "F"
last_verified_artifact: "found-semigroup-002-formalization-result.json"
current_blocker: null
next_single_action: >
  Revisar o resultado formal, os limites de escopo e o potencial
  de reutilização antes de autorizar qualquer extensão.
authorized_action: "FOUND_SEMIGROUP_002_RESULT_REVIEW_AUTHORIZED"
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
FOUND-SEMIGROUP-002   VERIFIED   nucleo formal de dinamica finita
RH-NOGO-001           FROZEN_PARTIAL_RESULT   congelado, NAO descartado
```

## O que foi provado

```text
alcancabilidade eh reflexiva e transitiva;
invariantes completos sao preservados por alcancabilidade;
toda trajetoria de uma funcao em tipo finito eh eventualmente periodica,
  com mu < card X, 0 < lam, mu + lam <= card X, ponto periodico na cauda
  e propagacao a todos os indices posteriores;
a iteracao de um elemento de monoide em tipo finito eh eventualmente
  periodica, DERIVADA do resultado funcional;
propriedades especiais de C3 falham em acoes finitas gerais — no sentido
  de que para CADA UMA existe um contraexemplo, e nao no sentido de que
  todas falhem simultaneamente em toda acao.
```

## O que **não** foi provado

```text
unicidade da cauda;
minimalidade do periodo;
decomposicao canonica completa;
classificacao de todas as acoes finitas;
qualquer resultado sobre sistemas infinitos;
qualquer resultado fisico;
TRI ou TDTR;
novidade matematica.
```

## Disciplina verificada

```text
casa dos pombos usada UMA unica vez;
minimalPeriod NAO usado (armadilha do ponto pre-periodico);
nenhuma instancia global de Preorder;
CE-001 usa acao genuina de monoide, nao o grafo de uma funcao;
hipoteses ociosas removidas: DecidableEq X, Fintype M, Group M ausentes.
```

## Novidade

**Zero.** Periodicidade eventual em conjunto finito é o princípio da casa
dos pombos. `RESULT_BOUNDARY.md` e `C3_BOUNDARY.md` são vinculantes.

## Próxima ação

Revisão do resultado. **Nenhuma extensão autorizada.**
