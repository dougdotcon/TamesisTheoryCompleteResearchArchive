---
schema: tamesis-theorem-map/1
work_item_id: RH-NOGO-001
subartifact: ASYM-NOGO-001
scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE
lean_root: "05_FORMAL/lean/TamesisLab/RHNogo/AsymptoticCore"
namespace: TamesisLab.RHNogo.AsymptoticCore
toolchain: "leanprover/lean4:v4.33.0-rc1"
mathlib_revision: "79d0395a1825a6264ad5d269e35e60537518955e"
build_status: PASS
---

# ASYM-NOGO-001 — Mapa de teoremas

Todos os itens são análise real elementar. Nenhum menciona a função zeta,
seus zeros, a Hipótese de Riemann, operadores, PDE, a lei de Weyl ou a
Classe W.

---

```yaml
- theorem_id: ASYM-NOGO-ALG-001
  human_statement: >
    Para T suficientemente grande, N(T)/T^α é igual ao produto de
    N(T)/(T log T) pelo fator log T · T^(1-α).
  lean_signature: >
    theorem eventually_normalization_identity (N : ℝ → ℝ) (α : ℝ) :
      ∀ᶠ T : ℝ in atTop,
        N T / T ^ α = (N T / (T * Real.log T)) * (Real.log T * T ^ (1 - α))
  file: Normalization.lean
  dependencies: []
  mathlib_lemmas: [eventually_gt_atTop, Real.log_pos, Real.rpow_pos_of_pos, Real.rpow_sub, Real.rpow_one, field_simp]
  proof_method: >
    filter_upwards com T > 1; positividade de T, log T e T^α; reescrita
    T^(1-α) = T / T^α; field_simp. Nenhuma divisão por N(T); nenhuma
    hipótese sobre o sinal de N(T).
  assumptions: ["T > 1 eventualmente"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-ALG-002
  human_statement: >
    Reorientação da identidade como igualdade eventual de funções, na forma
    consumida pelas transferências de limite.
  lean_signature: >
    theorem eventually_product_eq_normalizeRpow (N : ℝ → ℝ) (α : ℝ) :
      (fun T => (N T / (T * Real.log T)) * (Real.log T * T ^ (1 - α)))
        =ᶠ[atTop] fun T => N T / T ^ α
  file: Normalization.lean
  dependencies: [ASYM-NOGO-ALG-001]
  mathlib_lemmas: [Filter.Eventually.mono]
  proof_method: "simetria pontual da identidade eventual"
  assumptions: []
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-PL-000
  human_statement: "Para α ≤ 1, o fator log T · T^(1-α) diverge para +∞."
  lean_signature: >
    theorem tendsto_powerLogFactor_atTop_of_le_one {α : ℝ} (hα : α ≤ 1) :
      Tendsto (fun T => Real.log T * T ^ (1 - α)) atTop atTop
  file: PowerLog.lean
  dependencies: []
  mathlib_lemmas: [tendsto_atTop_mono', Real.tendsto_log_atTop, Real.log_nonneg, Real.one_le_rpow, eventually_ge_atTop, nlinarith]
  proof_method: >
    Minoração: para T ≥ 1 tem-se T^(1-α) ≥ 1 e log T ≥ 0, logo o fator
    domina log T, que diverge. Auxiliar comum aos casos α < 1 e α = 1.
  assumptions: ["α ≤ 1"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-PL-001
  human_statement: "Caso α < 1: log T · T^(1-α) → +∞."
  lean_signature: >
    theorem tendsto_powerLogFactor_atTop_of_lt_one {α : ℝ} (hα : α < 1) :
      Tendsto (fun T => Real.log T * T ^ (1 - α)) atTop atTop
  file: PowerLog.lean
  dependencies: [ASYM-NOGO-PL-000]
  mathlib_lemmas: [le_of_lt]
  proof_method: "especialização do auxiliar α ≤ 1"
  assumptions: ["α < 1"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-PL-002a
  human_statement: "Caso α = 1: o fator reduz-se exatamente a log T."
  lean_signature: >
    theorem powerLogFactor_eq_log_of_eq_one {α : ℝ} (hα : α = 1) (T : ℝ) :
      Real.log T * T ^ (1 - α) = Real.log T
  file: PowerLog.lean
  dependencies: []
  mathlib_lemmas: [Real.rpow_zero, mul_one]
  proof_method: "simp com α = 1 (1 - 1 = 0, T^0 = 1); vale para todo T"
  assumptions: ["α = 1"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-PL-002
  human_statement: "Caso α = 1: log T · T^(1-α) → +∞."
  lean_signature: >
    theorem tendsto_powerLogFactor_atTop_of_eq_one {α : ℝ} (hα : α = 1) :
      Tendsto (fun T => Real.log T * T ^ (1 - α)) atTop atTop
  file: PowerLog.lean
  dependencies: [ASYM-NOGO-PL-000]
  mathlib_lemmas: [le_of_eq]
  proof_method: "especialização do auxiliar α ≤ 1"
  assumptions: ["α = 1"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-PL-003
  human_statement: "Caso α > 1: log T · T^(1-α) → 0."
  lean_signature: >
    theorem tendsto_powerLogFactor_nhds_zero_of_one_lt {α : ℝ} (hα : 1 < α) :
      Tendsto (fun T => Real.log T * T ^ (1 - α)) atTop (nhds 0)
  file: PowerLog.lean
  dependencies: []
  mathlib_lemmas: [isLittleO_log_rpow_atTop, Asymptotics.IsLittleO.tendsto_div_nhds_zero, Filter.Tendsto.congr', Real.rpow_neg, neg_sub, div_eq_mul_inv]
  proof_method: >
    Reutiliza isLittleO_log_rpow_atTop (namespace raiz) com expoente
    r = α - 1 > 0, obtendo log T / T^(α-1) → 0; transfere por congruência
    eventual usando T^(1-α) = (T^(α-1))⁻¹ para T > 0. Nenhum resultado da
    Mathlib é recriado.
  assumptions: ["α > 1"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-AUX-001
  human_statement: >
    Se a normalização por T log T tende a c > 0 e o fator diverge, então a
    normalização por T^α diverge.
  lean_signature: >
    theorem tendsto_normalizeRpow_atTop_of_factor_atTop
      {N : ℝ → ℝ} {α c : ℝ} (hc : 0 < c) (hTLog) (hfac) :
      Tendsto (fun T => N T / T ^ α) atTop atTop
  file: Incompatibility.lean
  dependencies: [ASYM-NOGO-ALG-002]
  mathlib_lemmas: [Filter.Tendsto.pos_mul_atTop, Filter.Tendsto.congr']
  proof_method: "produto de limite positivo por divergência, transferido pela identidade eventual"
  assumptions: ["c > 0"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-AUX-002
  human_statement: >
    Se a normalização por T log T converge e o fator tende a zero, então a
    normalização por T^α tende a zero.
  lean_signature: >
    theorem tendsto_normalizeRpow_nhds_zero_of_factor_nhds_zero
      {N : ℝ → ℝ} {α c : ℝ} (hTLog) (hfac) :
      Tendsto (fun T => N T / T ^ α) atTop (nhds 0)
  file: Incompatibility.lean
  dependencies: [ASYM-NOGO-ALG-002]
  mathlib_lemmas: [Filter.Tendsto.mul, mul_zero, Filter.Tendsto.congr']
  proof_method: "produto de limites (c · 0 = 0), transferido pela identidade eventual"
  assumptions: []
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-001
  human_statement: >
    Não existe N : ℝ → ℝ com N(T)/(T log T) → c > 0 e, simultaneamente,
    N(T)/T^α → C > 0 para algum α > 0.
  lean_signature: >
    theorem asym_nogo_001 (N : ℝ → ℝ) (α c C : ℝ)
      (hα : 0 < α) (hc : 0 < c) (hC : 0 < C)
      (hTLog : Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c))
      (hPower : Tendsto (fun T => N T / T ^ α) atTop (nhds C)) : False
  file: Incompatibility.lean
  dependencies: [ASYM-NOGO-PL-001, ASYM-NOGO-PL-002, ASYM-NOGO-PL-003, ASYM-NOGO-AUX-001, ASYM-NOGO-AUX-002]
  mathlib_lemmas: [lt_trichotomy, not_tendsto_nhds_of_tendsto_atTop, tendsto_nhds_unique, ne_of_gt]
  proof_method: >
    Tricotomia em α versus 1. Casos α < 1 e α = 1: a normalização por T^α
    diverge, contradizendo o limite finito C. Caso α > 1: a normalização
    tende a 0 e a unicidade de limites força C = 0, contra C > 0.
  assumptions: ["α > 0", "c > 0", "C > 0"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-CONTRA-001
  human_statement: >
    Forma contrapositiva: dada a normalização por T log T com c > 0, nenhuma
    normalização por potência positiva converge para um valor positivo.
  lean_signature: >
    theorem not_tendsto_normalizeRpow_of_tendsto_normalizeTLog
      (N : ℝ → ℝ) (α c C : ℝ) (hα) (hc) (hC) (hTLog) :
      ¬ Tendsto (fun T => N T / T ^ α) atTop (nhds C)
  file: Audit.lean
  dependencies: [ASYM-NOGO-001]
  mathlib_lemmas: []
  proof_method: "reformulação direta do teorema principal"
  assumptions: ["α > 0", "c > 0", "C > 0"]
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE

- theorem_id: ASYM-NOGO-PROBE-001
  human_statement: >
    O enunciado registrado sem prova no gate de especificação
    (AsymNogoStatement) está agora provado.
  lean_signature: "theorem asymNogoStatement_holds : AsymNogoStatement"
  file: Audit.lean
  dependencies: [ASYM-NOGO-CONTRA-001]
  mathlib_lemmas: []
  proof_method: "aplicação da forma contrapositiva ao enunciado do probe"
  assumptions: []
  scope: REAL_ANALYSIS
  scientific_novelty: STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE
```

## Definições

| Nome | Tipo | Arquivo |
|---|---|---|
| `tLogScale` | `ℝ → ℝ`, `T ↦ T · log T` | `Definitions.lean` |
| `normalizeTLog` | `(ℝ → ℝ) → ℝ → ℝ` | `Definitions.lean` |
| `normalizeRpow` | `(ℝ → ℝ) → ℝ → ℝ → ℝ` | `Definitions.lean` |
| `powerLogFactor` | `ℝ → ℝ → ℝ`, `(α, T) ↦ log T · T^(1-α)` | `Definitions.lean` |

Todas `noncomputable` (dependem de `Real.log` e da divisão real), com lemas
`@[simp]` de desdobramento. Os teoremas são enunciados nas expressões
explícitas, não nas abreviações, para não esconder a matemática.

## Totais

| Métrica | Valor |
|---|---|
| definições | 4 (+ 4 lemas de desdobramento) |
| teoremas rastreáveis | 12 |
| teorema principal | `asym_nogo_001` |
| `sorry` / `admit` / `axiom` / `unsafe` | 0 / 0 / 0 / 0 |
| axiomas do kernel | `propext`, `Classical.choice`, `Quot.sound` (padrão da Mathlib) |
| `lake build` | PASS (8.691 jobs) |
| teste isolado | PASS |
