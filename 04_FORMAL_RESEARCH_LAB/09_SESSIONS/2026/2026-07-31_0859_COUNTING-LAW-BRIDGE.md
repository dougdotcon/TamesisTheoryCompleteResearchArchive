---
session_id: 2026-07-31_0859_COUNTING-LAW-BRIDGE
started_at: 2026-07-31T08:30:00-03:00
ended_at: 2026-07-31T08:59:57-03:00
agent: claude-opus-5
git_commit_before: 331c0880e8278c1ba3b7cecade180b3e92c383a4
git_commit_after: null
active_work_item: RH-NOGO-001
authorized_action: RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED
result_status: RH_NOGO_COUNTING_BRIDGE_VERIFIED
files_created:
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/Definitions.lean"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/TLogScale.lean"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/LittleOTransfer.lean"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/CountingLawBridge.lean"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/StrongAsymptoticCorollary.lean"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/Audit.lean"
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge.lean"
  - "05_FORMAL/lean/TamesisLab/Tests/RHNogoCountingBridge.lean"
  - "03_MILLENNIUM/01_RIEMANN/COUNTING_BRIDGE_THEOREM_MAP.md"
  - "03_MILLENNIUM/01_RIEMANN/COUNTING_BRIDGE_PROOF_AUDIT.md"
  - "counting-law-bridge-result.json"
  - "09_SESSIONS/2026/2026-07-31_0859_COUNTING-LAW-BRIDGE.md"
files_modified:
  - "05_FORMAL/lean/TamesisLab/RHNogo/Bridge/SignatureProbe.lean"
  - "05_FORMAL/lean/TamesisLab.lean"
  - "03_MILLENNIUM/01_RIEMANN/STATUS.yaml"
  - "03_MILLENNIUM/01_RIEMANN/LEAN_MAP.md"
  - "03_MILLENNIUM/01_RIEMANN/SOURCE_BRIDGE_GAP_REGISTER.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/CLAIM_LEDGER.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
tests_executed:
  - "lake env lean Tests/RHNogoCountingBridge.lean: exit 0, 43.6s"
  - "lake build: PASS, 8699 jobs, 2m05s"
  - "tokens proibidos: 0/0/0/0"
  - "#print axioms (13 objetos): [propext, Classical.choice, Quot.sound]"
  - "auditoria de imports e mencoes proibidas na pasta Bridge/: 0 ocorrencias"
  - "pytest: 2 passed"
  - "labctl validate: PASS, errors []"
claims_changed:
  - "COUNTING-BRIDGE-FORMAL-001 adicionada (F, formal_asymptotics, VERIFIED)"
gaps_closed:
  - "SB-GAP-010A — CLOSED_BY_FORMALIZATION"
gaps_opened:
  - "SB-GAP-010B — OUT_OF_CURRENT_SCOPE"
  - "SB-GAP-011 — nivel E3 nao formalizado"
gaps_superseded:
  - "SB-GAP-010"
next_single_action: "Resolver documentalmente e, quando elementar, formalizar isoladamente GWB-008 (positividade da constante de Weyl) e as hipóteses mínimas para W-ELLIPTIC-SCALAR, sem aplicar o no-go espectral."
---

## Objetivo autorizado

Formalizar em Lean a transferência abstrata da lei `T log T` sob diferença
`o(T log T)`, mantendo o gate independente de `ζ`, zeros,
Riemann–von Mangoldt, operadores, lei de Weyl, PDE, Hilbert–Pólya e da
classe `W-ELLIPTIC`.

## Correção de `SB-GAP-010`

Você tinha razão: a afirmação anterior — de que formalizar `RVM-LIMIT`
exigiria definir a função zeta — estava **errada para a parte genérica**.
Dividi o gap e **fechei a metade genérica por formalização**:

| Gap | Título | Estado |
|---|---|---|
| `SB-GAP-010A` | Generic strong-asymptotic-to-limit corollary | **CLOSED_BY_FORMALIZATION** |
| `SB-GAP-010B` | Lean proof of the actual Riemann–von Mangoldt theorem | `OUT_OF_CURRENT_SCOPE` |
| `SB-GAP-010` | — | `SUPERSEDED` |

`tendsto_tLog_of_eq_main_add_littleO` prova que
`N(T) = c·(T log T) + r(T)` com `r = o(T log T)` implica
`N(T)/(T log T) → c`, **sem uma única menção a zeta**.

## Teorema principal

```lean
theorem counting_law_bridge
    {NTarget NBase : ℝ → ℝ} {c : ℝ}
    (hbase : Tendsto (fun T => NBase T / (T * Real.log T)) atTop (nhds c))
    (hsmall : SubdominantTLog NTarget NBase) :
    Tendsto (fun T => NTarget T / (T * Real.log T)) atTop (nhds c)
```

**A hipótese `0 < c` foi removida.** Lean mostrou que não é necessária para
a transferência do limite. Segui sua instrução de não manter hipóteses
matematicamente ociosas: a positividade permanece apenas em
`TLogCountingLaw`, onde é parte da interface.

Evitei uma segunda hipótese ociosa: a identidade
`a/s + (b−a)/s = b/s` vale **pontualmente**, inclusive com `s = 0`, num
corpo. Registrei a versão eventual como conveniência de interface, não como
necessidade.

## Versão estrutural

`TLogCountingLaw.transfer` é `def`, não `theorem` — `TLogCountingLaw` vive
em `Type` porque carrega o dado `constant`. A preservação da constante é
provada por `rfl` (`transfer_constant`) e verificada no teste isolado.

## Níveis E0, E1, E3

- **E0 formalizado**: igualdade eventual ⟹ `o(T log T)`, e também ⟹ `O(1)`.
- **E1 formalizado**: `O(1)` ⟹ `o(T log T)`. Os lemas Mathlib necessários
  eram diretos (`IsBigO.trans_isLittleO`, `isLittleO_const_left`,
  `tendsto_abs_atTop_atTop`); **não** foi preciso desenvolver teoria de
  crescimento de `T log T` além de um lema auxiliar de três linhas.
- **E3 não formalizado**, conforme instrução. `RatioEquivalence` está apenas
  definida; sua ligação a E2 exige positividade e controle eventual do
  denominador (`SB-GAP-011`).

## Auditoria

`#print axioms` nos treze objetos rastreáveis devolve
`[propext, Classical.choice, Quot.sound]` em todos — sem `sorryAx`, sem
axioma local. Tokens proibidos: zero.

Auditoria de escopo: os únicos imports externos da pasta são
`Log.Basic`, `Pow.Real` (só para `rpow` na interface `PowerCountingLaw`,
que **não é usada** na prova) e `Asymptotics.Lemmas`. Busca por `zeta`,
`Riemann`, `Weyl`, `Complex`, `spectral`, `operator`, `Polya` na pasta:
**nenhuma ocorrência**.

## Falhas

Quatro, todas corrigidas sem token proibido:

1. `Definitions.lean` — falha de instância em `T ^ exponent`: faltava
   `Mathlib.Analysis.SpecialFunctions.Pow.Real`.
2. `LittleOTransfer.lean` — `Unknown identifier div_add_div_same`. Trocado
   por `simp only [div_eq_mul_inv]; ring`, que não depende do nome de um
   lema específico.
3. `CountingLawBridge.lean` — *"type of theorem is not a proposition"*:
   `TLogCountingLaw` está em `Type`, logo a transferência é `def`.
4. `StrongAsymptoticCorollary.lean` — `rewrite` falhou porque
   `SubdominantTLog` é `def` não redutível e o alvo não se desdobrava em
   `refine`. Corrigido com `show` explícito.

## O que foi e o que não foi provado

```text
Foi provado:
uma lei de normalização T log T pode ser transferida entre duas
funções cuja diferença seja o(T log T).

Não foi provado:
que N_ζ satisfaz Riemann–von Mangoldt;
que uma função espectral satisfaz Weyl;
que algum operador pertence a W-ELLIPTIC-SCALAR;
que N_P e N_ζ possuem diferença subdominante;
RH-NOGO-001;
qualquer afirmação sobre Hilbert–Pólya ou RH.
```

## Decisão sobre GWB-008

Conforme você indicou, `GWB-008` (`C_P > 0`) **não bloqueou este gate**: é
obrigação da futura inclusão `W-ELLIPTIC-SCALAR ⊆ W-POWER`, e ficou
registrada como obrigação **geométrica** separada em `STATUS.yaml` e no
registro de gaps.

## Handoff

Os dois componentes analíticos abstratos estão verificados:
`COUNTING-LAW-BRIDGE → ASYM-NOGO-001`. O que falta é inteiramente do lado
concreto — mostrar que objetos reais satisfazem as interfaces —, e é
exatamente onde a auditoria já havia localizado as lacunas geométricas
(`GWB-008`, discretude, fibrados) e bibliográficas.
