---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T11:50:00-03:00
canonical_commit: "c186ab593e8371098964533237f4a4bb8c85247c"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-SEMIGROUP-002"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "rh-nogo-research-review-result.json"
current_blocker: "FOUND-SEMIGROUP-002 ainda não foi especificado; execução não autorizada."
next_single_action: "Especificar FOUND-SEMIGROUP-002: definições, enunciados decidíveis e contraexemplos alvo para o monoide finito de transições já formalizado, sem executar formalização."
authorized_action: "FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED"
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
  - "Não executar FOUND-SEMIGROUP-002 antes de sua especificação estar pronta"
  - "Não confundir o modelo finito de FOUND-SEMIGROUP-002 com teoria geral de semigrupos"
  - "Não reutilizar o modelo finito como suporte de alegação física ou espectral"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "03_MILLENNIUM/01_RIEMANN/RH_NOGO_FREEZE_RECORD.md"
  - "03_MILLENNIUM/01_RIEMANN/RH_NOGO_RESULT_BOUNDARY.md"
  - "03_MILLENNIUM/01_RIEMANN/RH_NOGO_REACTIVATION_CRITERIA.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/DECISION_LEDGER.yaml"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

```text
RH-NOGO-001   FROZEN_PARTIAL_RESULT   (congelado, NAO descartado)
FOUND-SEMIGROUP-002   SCOPED          (ativo, apenas especificacao autorizada)
```

## RH-NOGO-001 — o que ficou pronto

```text
CAMADA ANALITICA ABSTRATA — COMPLETA
  ASYM-NOGO-001          VERIFIED
  COUNTING-LAW-BRIDGE    VERIFIED
  ABSTRACT-NOGO-001      VERIFIED
  WEYL-COEFFICIENT-CORE  VERIFIED  (interface, nao geometria)

CAMADA CONCRETA — DEFERIDA
  GLOBAL-WEYL-BRIDGE-SCALAR   NOT_PROVED       (9 obrigacoes, 0 provadas)
  Riemann-von Mangoldt        NOT_FORMALIZED
  exclusao de operadores      NOT_PROVED
```

Descrição canônica, vinculante:

> Teorema abstrato formal completo, com uma aplicação espectral candidata
> rigorosamente delimitada, mas ainda não instanciada.

## RH-NOGO-001 — conclusões científicas

```yaml
spectral_nogo: NOT_ESTABLISHED
hilbert_polya: NOT_EXCLUDED
riemann_hypothesis: NO_RESULT
```

Claims permitidas e proibidas estão fixadas em
`03_MILLENNIUM/01_RIEMANN/RH_NOGO_RESULT_BOUNDARY.md`, documento
vinculante.

## Por que congelar

Continuar exigiria construir, em Lean, infraestrutura para operadores
auto-adjuntos não limitados, resolvente compacto, projetores espectrais,
cálculo pseudodiferencial, lei global de Weyl e Riemann–von Mangoldt. Isso
é um projeto de formalização de grande porte, não o próximo gate — e o
resultado final excluiria apenas uma classe estreita, metade de cujas
condições é hipótese deste próprio laboratório, sem resolver RH.

Congelar preserva o que é válido e reutilizável. As pastas
`AsymptoticCore/`, `Bridge/` e `Composition/` são análise real abstrata
sobre funções `ℝ → ℝ` e podem ser usadas fora desta frente.

## Próxima frente

`FOUND-SEMIGROUP-002` — dinâmica discreta de monoides de transição
finitos. Escolhido porque usa infraestrutura Mathlib já disponível e já
exercitada aqui (`Fintype`, `Decidable`, `decide`), tem acesso alto a
contraexemplos por ser finito e decidível, e reutiliza diretamente
`FOUND-SEMIGROUP-001`, que está `VERIFIED`.

**Apenas a especificação está autorizada.** Nenhuma formalização foi
executada neste gate.
