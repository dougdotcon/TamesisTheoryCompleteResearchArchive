import TamesisLab.RHNogo.Bridge.StrongAsymptoticCorollary

set_option autoImplicit false

/-!
# RVM-LIMIT — instância simbólica da fórmula de von Mangoldt

Fecha, como um lema autônomo de análise real, o passo listado em
`03_MILLENNIUM/01_RIEMANN/RVM_LIMIT_BRIDGE.md` como `RVM-LIMIT`
(`evidence_status: ELEMENTARY_COROLLARY_REQUIRING_FORMALIZATION`,
`steps_sketched_not_proved`). O enunciado abaixo trata a forma simbólica
do termo principal de von Mangoldt

```text
N(T) = (T/2π)·log(T/2π) − T/2π + 7/8
```

como uma função `ℝ → ℝ` qualquer — **sem** `ζ`, sem zeros, sem a função
de contagem `N_ζ` de fato — e prova que `N(T)/(T log T) → 1/(2π)`. O termo
de erro `O(log T)` de `RVM-STRONG` é **omitido**, exatamente como o
enunciado do teste original permite como primeira passagem ("abstracted...
or omitted entirely").

**O que isto NÃO estabelece:** que a função de contagem de zeros de zeta
`N_ζ(T)` satisfaz esta fórmula — isso é `SB-GAP-010B`
(`OUT_OF_CURRENT_SCOPE`, exige a fórmula de Riemann–von Mangoldt em si,
com a função `ζ` e a definição de `N_ζ` via von Mangoldt 1905). Este
arquivo apenas move, no diagrama de `RVM_LIMIT_BRIDGE.md`, a seta
"`RVM-STRONG` (forma simbólica) → `RVM-LIMIT`" de "não formalizado" para
"formalizado". Nada sobre `ζ`, seus zeros, ou a lei de Weyl muda.

Independente de: função zeta, zeros, Riemann–von Mangoldt, operadores, lei
de Weyl, PDE, Hilbert–Pólya e da classe `W-ELLIPTIC`.

scientific_novelty: STANDARD_ASYMPTOTIC_INSTANTIATION_FORMALIZED_FOR_LOCAL_USE
-/

namespace TamesisLab.RHNogo.Bridge

open Filter Asymptotics

/-- Passo isolado de `RVM-LIMIT`
(`steps_sketched_not_proved[0]` em `RVM_LIMIT_BRIDGE.md`):
`log(T/2π)/log T → 1`. Provado escrevendo `log(T/2π) = log T - log(2π)`
(válido para `T ≠ 0`, via `Real.log_div`) e usando `log T → +∞`. Isola o
único passo genuinamente novo, separado da aritmética de limites em torno
dele. -/
theorem tendsto_log_div_two_pi_div_log_atTop :
    Tendsto (fun T : ℝ => Real.log (T / (2 * Real.pi)) / Real.log T)
      atTop (nhds 1) := by
  have hinv : Tendsto (fun T : ℝ => (Real.log T)⁻¹) atTop (nhds 0) :=
    Real.tendsto_log_atTop.inv_tendsto_atTop
  have hstep :
      Tendsto (fun T : ℝ => 1 - Real.log (2 * Real.pi) * (Real.log T)⁻¹)
        atTop (nhds 1) := by
    have h2 := hinv.const_mul (Real.log (2 * Real.pi))
    simpa using tendsto_const_nhds.sub h2
  refine Tendsto.congr' ?_ hstep
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with T hT
  have hT0 : T ≠ 0 := ne_of_gt (lt_trans zero_lt_one hT)
  have hpi0 : (2 * Real.pi) ≠ 0 := ne_of_gt Real.two_pi_pos
  have hlogT : Real.log T ≠ 0 := ne_of_gt (Real.log_pos hT)
  rw [Real.log_div hT0 hpi0]
  field_simp

/-- **RVM-LIMIT (forma simbólica).** A fórmula principal de von Mangoldt
`N(T) = (T/2π)·log(T/2π) − T/2π + 7/8`, tratada como função real qualquer
(sem `ζ`, sem zeros), satisfaz `N(T)/(T log T) → 1/(2π)`. Reduz o gap
`RVM-LIMIT` de `RVM_LIMIT_BRIDGE.md` (status `SPECIFIED_NOT_FORMALIZED`)
a uma instância explícita e verificada, mantendo `N_ζ(T) = N(T)` como
obrigação separada e não coberta aqui (`SB-GAP-010B`). -/
theorem tendsto_rvmLimitFormula_div_tLogScale :
    Tendsto (fun T : ℝ =>
        ((T / (2 * Real.pi)) * Real.log (T / (2 * Real.pi))
          - T / (2 * Real.pi) + 7 / 8) / (T * Real.log T))
      atTop (nhds (1 / (2 * Real.pi))) := by
  have hinv : Tendsto (fun T : ℝ => (Real.log T)⁻¹) atTop (nhds 0) :=
    Real.tendsto_log_atTop.inv_tendsto_atTop
  have hTlogInv : Tendsto (fun T : ℝ => (T * Real.log T)⁻¹) atTop (nhds 0) :=
    tendsto_tLogScale_atTop.inv_tendsto_atTop
  have ha :
      Tendsto
        (fun T : ℝ =>
          (-(Real.log (2 * Real.pi) + 1) / (2 * Real.pi)) * (Real.log T)⁻¹)
        atTop (nhds 0) := by
    have := hinv.const_mul (-(Real.log (2 * Real.pi) + 1) / (2 * Real.pi))
    simpa using this
  have hb :
      Tendsto (fun T : ℝ => (7 / 8 : ℝ) * (T * Real.log T)⁻¹)
        atTop (nhds 0) := by
    have := hTlogInv.const_mul (7 / 8 : ℝ)
    simpa using this
  have hsum :
      Tendsto
        (fun T : ℝ =>
          1 / (2 * Real.pi) +
            ((-(Real.log (2 * Real.pi) + 1) / (2 * Real.pi)) * (Real.log T)⁻¹
              + (7 / 8 : ℝ) * (T * Real.log T)⁻¹))
        atTop (nhds (1 / (2 * Real.pi) + (0 + 0))) :=
    tendsto_const_nhds.add (ha.add hb)
  simp only [add_zero] at hsum
  refine Tendsto.congr' ?_ hsum
  filter_upwards [eventually_gt_atTop (1 : ℝ)] with T hT
  have hT0 : T ≠ 0 := ne_of_gt (lt_trans zero_lt_one hT)
  have hpi0 : (2 * Real.pi) ≠ 0 := ne_of_gt Real.two_pi_pos
  have hlogT : Real.log T ≠ 0 := ne_of_gt (Real.log_pos hT)
  rw [Real.log_div hT0 hpi0]
  field_simp
  ring

end TamesisLab.RHNogo.Bridge

#print axioms TamesisLab.RHNogo.Bridge.tendsto_log_div_two_pi_div_log_atTop
#print axioms TamesisLab.RHNogo.Bridge.tendsto_rvmLimitFormula_div_tLogScale
