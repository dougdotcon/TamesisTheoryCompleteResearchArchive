---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T08:59:57-03:00
canonical_commit: "331c0880e8278c1ba3b7cecade180b3e92c383a4"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "counting-law-bridge-result.json"
current_blocker: "Faltam as obrigações geométricas: positividade da constante de Weyl (GWB-008) e as hipóteses mínimas de W-ELLIPTIC-SCALAR."
next_single_action: "Resolver documentalmente e, quando elementar, formalizar isoladamente GWB-008 (positividade da constante de Weyl) e as hipóteses mínimas para W-ELLIPTIC-SCALAR, sem aplicar o no-go espectral."
authorized_action: "RH_NOGO_GEOMETRIC_GAP_RESOLUTION_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova do no-go completo (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não aplicar ASYM-NOGO-001 a nenhum operador"
  - "Não formalizar operadores pseudodiferenciais, lei de Weyl ou Riemann–von Mangoldt concreto"
  - "Não quantificar sobre todas as realizações auto-adjuntas de uma expressão formal"
  - "Não estender do caso escalar para sistemas ou fibrados"
  - "Não estender do caso sem bordo para problemas de bordo"
  - "Não citar Hörmander 1968 pela lei de Weyl global — apenas pelo resultado local"
  - "Não declarar que Hilbert–Pólya foi refutado"
  - "Não declarar progresso sobre a verdade ou falsidade da Hipótese de Riemann"
  - "Não modificar legado nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "03_MILLENNIUM/01_RIEMANN/COUNTING_BRIDGE_THEOREM_MAP.md"
  - "03_MILLENNIUM/01_RIEMANN/GLOBAL_WEYL_BRIDGE_OBLIGATIONS.md"
  - "03_MILLENNIUM/01_RIEMANN/W_ELLIPTIC_SCALAR_V2.md"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_GAP_REGISTER.yaml"
  - "03_MILLENNIUM/01_RIEMANN/STOP_CONDITIONS.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

Os **dois componentes analíticos abstratos** da frente estão verificados em
Lean:

```text
COUNTING-LAW-BRIDGE   VERIFIED
          ↓
ASYM-NOGO-001         VERIFIED
```

`RH-NOGO-001` permanece `SCOPED`. `ASYM-NOGO-001` **não** foi aplicado,
nenhum operador foi construído e nada foi afirmado sobre a Hipótese de
Riemann.

## O que foi provado neste gate

```text
Se  N_base(T)/(T log T) → c
e   N_target(T) − N_base(T) = o(T log T),
então N_target(T)/(T log T) → c.
```

Quinze teoremas em `05_FORMAL/lean/TamesisLab/RHNogo/Bridge/`, incluindo a
versão estrutural (que **preserva a constante**), o corolário genérico
"fórmula forte ⟹ limite" e a hierarquia `E0 ⟹ E1 ⟹ E2`.

Auditoria de escopo: os únicos imports da pasta são `Log.Basic`,
`Pow.Real` e `Asymptotics.Lemmas`; busca por `zeta`, `Riemann`, `Weyl`,
`Complex`, `spectral`, `operator`, `Polya` na pasta: **nenhuma ocorrência**.

## Correção de `SB-GAP-010`

A afirmação anterior — de que formalizar `RVM-LIMIT` exigiria definir a
função zeta — estava **errada para a parte genérica**. Dividido em:

| Gap | Estado |
|---|---|
| `SB-GAP-010A` — corolário genérico "fórmula forte ⟹ limite" | **CLOSED_BY_FORMALIZATION** (sem mencionar zeta) |
| `SB-GAP-010B` — provar que a `N_ζ` concreta satisfaz Riemann–von Mangoldt | `OUT_OF_CURRENT_SCOPE` |

## O que falta

Demonstrar que os **objetos concretos** satisfazem as interfaces — exatamente
onde a auditoria encontrou as lacunas:

- **`GWB-008` (`C_P > 0`)**: obrigação **geométrica**, não bloqueou este
  gate; nenhuma fonte obtida a afirma.
- **`GAP-RH-012`**: discretude é hipótese incorporada, não derivada.
- **`GAP-RH-009`**: sistemas e fibrados adiados, **não fechado**.
- **`SB-GAP-010B`**: ramo aritmético concreto fora de alcance.
- **`SB-GAP-011`**: nível E3 não formalizado.

## Work items

| Item | Estado |
|---|---|
| LAB-ARCH-001 | VERIFIED |
| LAB-BENCH-001 | VERIFIED |
| FOUND-SEMIGROUP-001 | VERIFIED |
| RH-NOGO-001 | SCOPED; `ASYM-NOGO-001` e `COUNTING-LAW-BRIDGE` VERIFIED |

## Próxima ação única

Resolver documentalmente e, quando elementar, formalizar isoladamente
GWB-008 (positividade da constante de Weyl) e as hipóteses mínimas para
W-ELLIPTIC-SCALAR, sem aplicar o no-go espectral.

## Histórico recente

- 2026-07-31: migração WSL2; LAB-BENCH-001; FOUND-SEMIGROUP-001.
- 2026-07-31: `ASYM-NOGO-001` verificado em Lean.
- 2026-07-31: auditoria de fontes primárias — Hörmander 1968 não enuncia a
  lei global.
- 2026-07-31: classes separadas; ponte local→global documentada.
- 2026-07-31: ponte especificada; alvo migrado para `o(T log T)`.
- 2026-07-31: `COUNTING-LAW-BRIDGE` **verificado**
  (`RH_NOGO_COUNTING_BRIDGE_VERIFIED`); `SB-GAP-010` dividido e a parte
  genérica fechada por formalização; nenhuma claim sobre a RH.
