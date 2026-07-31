---
schema: tamesis-theorem-map/1
work_item_id: RH-NOGO-001
subartifact: COUNTING-LAW-BRIDGE
scientific_novelty: STANDARD_ASYMPTOTIC_TRANSFER_FORMALIZED_FOR_LOCAL_USE
lean_root: "05_FORMAL/lean/TamesisLab/RHNogo/Bridge"
namespace: TamesisLab.RHNogo.Bridge
toolchain: "leanprover/lean4:v4.33.0-rc1"
mathlib_revision: "79d0395a1825a6264ad5d269e35e60537518955e"
build_status: PASS
---

# COUNTING-LAW-BRIDGE — mapa de teoremas

Todos os itens são análise real abstrata sobre funções `ℝ → ℝ`. Nenhum
menciona a função zeta, seus zeros, Riemann–von Mangoldt, operadores, a lei
de Weyl, PDE, Hilbert–Pólya ou a classe `W-ELLIPTIC`.

## Definições (`Definitions.lean`)

| Nome | Tipo |
|---|---|
| `tLogScale` | `ℝ → ℝ`, `T ↦ T·log T` (`noncomputable`) |
| `PowerCountingLaw` | `(ℝ → ℝ) → Type` — interface `W-POWER` (não usada na prova da ponte) |
| `TLogCountingLaw` | `(ℝ → ℝ) → Type` — interface `T log T` |
| `SubdominantDifference` | `(ℝ → ℝ) → (ℝ → ℝ) → (ℝ → ℝ) → Prop` — escala arbitrária |
| `SubdominantTLog` | `(ℝ → ℝ) → (ℝ → ℝ) → Prop` — nível E2 |
| `EventualEquality` | nível E0 |
| `BoundedDifference` | nível E1 |
| `RatioEquivalence` | nível E3 — **definida, não usada** |
| `CountingLawBridgeStatement` | `Prop` |

`PowerCountingLaw` e `TLogCountingLaw` vivem em `Type`, não `Prop`, porque
carregam dados (`exponent`, `constant`) além das hipóteses.

---

```yaml
- theorem_id: CLB-SCALE-001
  human_statement: "T · log T eh eventualmente nao nulo em atTop."
  lean_signature: "theorem eventually_tLogScale_ne_zero : ∀ᶠ T : ℝ in atTop, T * Real.log T ≠ 0"
  file: TLogScale.lean
  dependencies: []
  mathlib_lemmas: [eventually_gt_atTop, Real.log_pos, mul_ne_zero]
  proof_method: "filter_upwards com 1 < T; positividade de T e de log T"
  scope: REAL_ANALYSIS
  note: "Nenhuma afirmacao global sobre Real.log para valores <= 1."

- theorem_id: CLB-SCALE-002
  human_statement: "T · log T diverge para +infinito."
  lean_signature: "theorem tendsto_tLogScale_atTop : Tendsto (fun T : ℝ => T * Real.log T) atTop atTop"
  file: TLogScale.lean
  dependencies: []
  mathlib_lemmas: [Filter.Tendsto.atTop_mul_atTop₀, tendsto_id, Real.tendsto_log_atTop]
  proof_method: "produto de duas divergencias"
  scope: REAL_ANALYSIS
  note: "Usado apenas pelo corolario do nivel E1."

- theorem_id: CLB-SCALE-003
  human_statement: "A normalizacao de c·(T log T) pela propria escala tende a c."
  lean_signature: "theorem tendsto_const_mul_tLogScale_div (c : ℝ) : Tendsto (fun T => c * (T * Real.log T) / (T * Real.log T)) atTop (nhds c)"
  file: TLogScale.lean
  dependencies: [CLB-SCALE-001]
  mathlib_lemmas: [tendsto_const_nhds, Filter.Tendsto.congr', mul_div_assoc, div_self, mul_one]
  proof_method: "congruencia eventual com a constante, sob nao nulidade da escala"
  scope: REAL_ANALYSIS

- theorem_id: CLB-LO-001
  human_statement: "Uma diferenca o(T log T), normalizada pela escala, tende a zero."
  lean_signature: "theorem subdominantDifference_tendsto_zero {NTarget NBase} (hsmall : SubdominantTLog NTarget NBase) : Tendsto (fun T => (NTarget T - NBase T) / (T * Real.log T)) atTop (nhds 0)"
  file: LittleOTransfer.lean
  dependencies: []
  mathlib_lemmas: [Asymptotics.IsLittleO.tendsto_div_nhds_zero]
  proof_method: "aplicacao direta do lema da Mathlib; a definicao de little-o NAO eh reprovada a mao"
  scope: REAL_ANALYSIS

- theorem_id: CLB-ALG-001a
  human_statement: "Identidade PONTUAL das normalizacoes."
  lean_signature: "theorem target_normalization_eq (NTarget NBase : ℝ → ℝ) (T : ℝ) : NTarget T / (T * Real.log T) = NBase T / (T * Real.log T) + (NTarget T - NBase T) / (T * Real.log T)"
  file: LittleOTransfer.lean
  dependencies: []
  mathlib_lemmas: [div_eq_mul_inv, ring]
  proof_method: "reescrita em multiplicacao pelo inverso e ring"
  scope: REAL_ANALYSIS
  note: >
    A nao nulidade do denominador NAO eh necessaria: em um corpo,
    a/s + b/s = (a+b)/s vale inclusive para s = 0. Hipotese ociosa evitada.

- theorem_id: CLB-ALG-001
  human_statement: "Versao eventual da identidade das normalizacoes."
  lean_signature: "theorem eventually_target_normalization_eq (NTarget NBase : ℝ → ℝ) : ∀ᶠ T : ℝ in atTop, ..."
  file: LittleOTransfer.lean
  dependencies: [CLB-ALG-001a]
  mathlib_lemmas: [Filter.Eventually.of_forall]
  proof_method: "consequencia imediata da versao pontual"
  scope: REAL_ANALYSIS
  note: "O qualificador eventual eh conveniencia de interface, nao necessidade."

- theorem_id: COUNTING-LAW-BRIDGE
  human_statement: >
    Se NBase normalizada por T log T tende a c, e NTarget - NBase = o(T log T),
    entao NTarget normalizada pela mesma escala tende ao MESMO c.
  lean_signature: >
    theorem counting_law_bridge {NTarget NBase : ℝ → ℝ} {c : ℝ}
      (hbase : Tendsto (fun T => NBase T / (T * Real.log T)) atTop (nhds c))
      (hsmall : SubdominantTLog NTarget NBase) :
      Tendsto (fun T => NTarget T / (T * Real.log T)) atTop (nhds c)
  file: CountingLawBridge.lean
  dependencies: [CLB-LO-001, CLB-ALG-001a]
  mathlib_lemmas: [Filter.Tendsto.add, add_zero, Filter.Tendsto.congr]
  proof_method: "soma dos limites (c + 0) transportada pela identidade pontual"
  scope: REAL_ANALYSIS
  hypothesis_removed: >
    A positividade 0 < c NAO eh necessaria e foi REMOVIDA do teorema tecnico.
    Lean confirmou a desnecessidade. A positividade permanece apenas em
    TLogCountingLaw, onde eh parte da interface.

- theorem_id: COUNTING-LAW-BRIDGE-STRUCT
  human_statement: "A interface TLogCountingLaw transfere-se, com a mesma constante."
  lean_signature: >
    def TLogCountingLaw.transfer {NTarget NBase : ℝ → ℝ}
      (hbase : TLogCountingLaw NBase) (hsmall : SubdominantTLog NTarget NBase) :
      TLogCountingLaw NTarget
  file: CountingLawBridge.lean
  dependencies: [COUNTING-LAW-BRIDGE]
  proof_method: "construcao da estrutura reutilizando constante e positividade da base"
  scope: REAL_ANALYSIS
  note: "eh 'def' e nao 'theorem' porque TLogCountingLaw vive em Type (carrega dado)."

- theorem_id: COUNTING-LAW-BRIDGE-CONST
  human_statement: "A constante eh literalmente preservada pela transferencia."
  lean_signature: "theorem TLogCountingLaw.transfer_constant ... : (TLogCountingLaw.transfer hbase hsmall).constant = hbase.constant"
  file: CountingLawBridge.lean
  dependencies: [COUNTING-LAW-BRIDGE-STRUCT]
  proof_method: "rfl"
  scope: REAL_ANALYSIS

- theorem_id: COUNTING-LAW-BRIDGE-STATEMENT
  human_statement: "O enunciado registrado no gate de especificacao esta provado."
  lean_signature: "theorem countingLawBridgeStatement_holds : CountingLawBridgeStatement"
  file: CountingLawBridge.lean
  dependencies: [COUNTING-LAW-BRIDGE]
  proof_method: "aplicacao direta"
  scope: REAL_ANALYSIS

- theorem_id: STRONG-TLOG-COROLLARY
  human_statement: >
    Se N(T) = c*(T log T) + r(T) com r = o(T log T), entao N(T)/(T log T) -> c.
  lean_signature: >
    theorem tendsto_tLog_of_eq_main_add_littleO {N r : ℝ → ℝ} {c : ℝ}
      (hN : ∀ T, N T = c * (T * Real.log T) + r T)
      (hr : r =o[atTop] fun T => T * Real.log T) :
      Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c)
  file: StrongAsymptoticCorollary.lean
  dependencies: [COUNTING-LAW-BRIDGE, CLB-SCALE-003]
  mathlib_lemmas: [funext, ring]
  proof_method: "instancia a ponte com NBase := c*(T log T); a diferenca eh exatamente r"
  scope: REAL_ANALYSIS
  gap_closed: SB-GAP-010A
  note: >
    Formalizacao GENERICA de "formula assintotica forte implica limite".
    NAO menciona zeta. Instancia-la com Riemann-von Mangoldt eh SB-GAP-010B,
    fora do alcance atual.

- theorem_id: CLB-E0-E2
  human_statement: "Igualdade eventual implica diferenca o(T log T)."
  lean_signature: "theorem subdominantTLog_of_eventualEquality {NTarget NBase} (h : EventualEquality NTarget NBase) : SubdominantTLog NTarget NBase"
  file: StrongAsymptoticCorollary.lean
  dependencies: []
  mathlib_lemmas: [Asymptotics.isLittleO_zero, Asymptotics.IsLittleO.congr', sub_self]
  proof_method: "congruencia eventual com a funcao nula"
  scope: REAL_ANALYSIS

- theorem_id: CLB-E0-E1
  human_statement: "Igualdade eventual implica diferenca O(1)."
  lean_signature: "theorem boundedDifference_of_eventualEquality {NTarget NBase} (h : EventualEquality NTarget NBase) : BoundedDifference NTarget NBase"
  file: StrongAsymptoticCorollary.lean
  dependencies: []
  mathlib_lemmas: [Asymptotics.isBigO_zero, Asymptotics.IsBigO.congr', sub_self]
  proof_method: "congruencia eventual com a funcao nula"
  scope: REAL_ANALYSIS

- theorem_id: CLB-NORM-001
  human_statement: "A norma da escala T log T diverge."
  lean_signature: "theorem tendsto_norm_tLogScale_atTop : Tendsto (fun T : ℝ => ‖T * Real.log T‖) atTop atTop"
  file: StrongAsymptoticCorollary.lean
  dependencies: [CLB-SCALE-002]
  mathlib_lemmas: [Real.norm_eq_abs, tendsto_abs_atTop_atTop]
  proof_method: "composicao com o valor absoluto"
  scope: REAL_ANALYSIS

- theorem_id: CLB-E1-E2
  human_statement: "Diferenca O(1) implica diferenca o(T log T)."
  lean_signature: "theorem subdominantTLog_of_boundedDifference {NTarget NBase} (h : BoundedDifference NTarget NBase) : SubdominantTLog NTarget NBase"
  file: StrongAsymptoticCorollary.lean
  dependencies: [CLB-NORM-001]
  mathlib_lemmas: [Asymptotics.IsBigO.trans_isLittleO, Asymptotics.isLittleO_const_left]
  proof_method: "O(1) =o(T log T) porque a norma da escala diverge"
  scope: REAL_ANALYSIS
  note: >
    Os lemas Mathlib necessarios eram diretos; nenhuma teoria adicional de
    crescimento de T log T precisou ser desenvolvida. E1 FOI formalizado.
```

## Nível E3

**Não formalizado neste gate**, conforme instrução. `RatioEquivalence` está
apenas **definida**. Sua ligação a E2 exige positividade e controle eventual
do denominador (`N_base ≠ 0` eventualmente), hipóteses que não pertencem à
interface atual.

## Totais

| Métrica | Valor |
|---|---|
| definições | 9 (+1 lema `@[simp]` de desdobramento) |
| teoremas rastreáveis | 13 (12 `theorem` + 1 `def` estrutural) |
| teorema principal | `counting_law_bridge` |
| hipóteses removidas por serem ociosas | 1 (`0 < c`) |
| `sorry` / `admit` / `axiom` / `unsafe` | 0 / 0 / 0 / 0 |
| axiomas do kernel | `propext`, `Classical.choice`, `Quot.sound` |
| `lake build` | PASS (8.699 jobs) |
| teste isolado | PASS |
