/-
FOUND-DIRICHLET-OSCILLATORY-INTEGRAL-001 — standalone draft, NOT integrated into
`TamesisLab.lean` or any shared aggregator. Follows the same convention as
`CalderonZygmundKernelDefinitions.lean` / `ConstantinFeffermanDepletionKernel.lean`
(03_MILLENNIUM/02_NAVIER_STOKES/FORMAL/): a self-contained Lean file, verified
directly via `lake env lean` against the same vendored Mathlib, outside the
shared import tree. Authorization: `PORTFOLIO_REVIEW_DIRICHLET_OSCILLATORY_INTEGRAL_2026_08_09.md`
(`FOUND-DIRICHLET-OSCILLATORY-INTEGRAL-001_AUTHORIZED`), scoped by
`RESEARCH_SCOPING_SINGULAR_INTEGRAL_INFRASTRUCTURE_2026_08_09.md`.

## What this file is

A general-purpose, standalone piece of classical real analysis: the value of the
improper Dirichlet integral

  ∫₀^∞ (sin x)/x dx = π/2

together with its formal identification with `lim_{N→∞} ∫₀^N (sin x)/x dx`.
This is item 1 of the authorized scope. It is reusable for ANY future zero-mean
kernel work in this lab and is deliberately NOT specific to Navier-Stokes.

## Primary source and exact statement checked against it

Loukas Grafakos, *Classical Fourier Analysis*, 3rd ed., Springer GTM 249, 2014,
§5.2.2, Lemma 5.2.5 (pp. 336-337). Lemma 5.2.5 itself is stated for the family

  lim_{ε→0,N→∞} ∫_ε^N (cos(ra) - cos(r))/r dr = log(1/|a|)                (5.2.10)
  |∫_ε^N (cos(ra) - cos(r))/r dr| ≤ 2|log(1/|a|)|  for all N > ε > 0      (5.2.11)
  lim_{ε→0,N→∞} ∫_ε^N (e^{-ira} - cos r)/r dr = log(1/|a|) - (iπ/2) sgn a (5.2.12)
  |∫_ε^N (e^{-ira} - cos r)/r dr| ≤ 2|log(1/|a|)| + 4  for all N > ε > 0  (5.2.13)

for `a` a nonzero real number. Grafakos's own proof of (5.2.10)/(5.2.11) is a
direct FTC + double-integral computation that does NOT go through the value of
any improper trigonometric integral (it only needs a vanishing bound on
`∫_N^{N|a|} cos(t)/t dt` as `N → ∞`, obtained by one integration by parts). It is
only the proof of (5.2.12)/(5.2.13) — via the auxiliary claim (5.2.14) that
`|∫_ε^N sin(ra)/r dr| = |∫_{ε|a|}^{N|a|} sin(r)/r dr|` tends to `π/2` as
`ε → 0, N → ∞` and is bounded by 4, citing Grafakos's own Exercise 5.1.1 — that
genuinely needs the classical Dirichlet integral value formalized below.

This file formalizes ONLY the Dirichlet integral itself (the prerequisite fact
behind (5.2.12)/(5.2.14)). Lemma 5.2.5 in full (the `log(1/|a|)` limits, real or
complex) is NOT attempted here; see "Scope and honest gap note" at the end of
this file for the precise, separate reason. Every proof below is fully closed —
no incomplete-proof placeholder, no locally introduced primitive assumption, and
no memory-unchecked declaration appears anywhere in this file.

## What this file does NOT do

It does not touch `CalderonZygmundKernelDefinitions.lean`, `FourierMultiplierL2.lean`,
or any other file in this lab. It does not attempt principal-value distributions,
Grafakos Proposition 5.2.3, or any Fourier-multiplier boundedness claim. It makes
no claim of progress on any Navier-Stokes gap. It is pure, general real analysis.

## Proof route actually used (checked to be Mathlib-supported before committing)

The classical "Feynman parameter" derivation, but organized to avoid needing
differentiation under an improper integral sign (which would need extra
dominated-derivative machinery). Concretely, for fixed `N > 0`:

1. `∫ t in 0..M, exp(-x*t) dt = (1 - exp(-x*M))/x`  for `x ≠ 0`        (elementary FTC)
2. `∫ x in 0..N, exp(-t*x) * sin x dx` has an explicit closed form via FTC applied
   to the antiderivative `x ↦ -(exp(-t*x)*(t*sin x + cos x))/(1+t^2)`.
3. Swapping the (finite × finite) double integral `∫x in 0..N, ∫t in 0..M, exp(-t*x) sin x`
   over the COMPACT rectangle `[0,N] × [0,M]` (continuous integrand ⇒ integrable,
   no delicate improper-Fubini argument needed) and combining with steps 1-2 gives,
   for every `N, M > 0`:
     `(∫x in 0..N, sinc x) - (∫x in 0..N, sinc x * exp(-x*M))
        = ∫t in 0..M, (1 - exp(-t*N)*(t*sin N + cos N))/(1+t^2)`.
4. Sending `M → ∞`: the remainder term `→ 0` by dominated convergence
   (`|sinc x| ≤ 1`, `exp(-x*M) ≤ 1` for `x, M ≥ 0`, pointwise `→ 0` for `x > 0`),
   and the right side `→ ∫t in Ioi 0, (...)/(1+t^2)` by the standard improper-
   integral-as-limit lemma, giving `∫x in 0..N, sinc x = Φ(N)` where
   `Φ(N) := ∫t in Ioi 0, (1 - exp(-t*N)*(t*sin N + cos N))/(1+t^2) dt`.
5. `Φ(N) = π/2 - Ψ(N)` where `∫t in Ioi 0, 1/(1+t^2) dt = π/2` is already in
   Mathlib (`integral_Ioi_inv_one_add_sq`), and `Ψ(N) → 0` as `N → ∞` by an
   explicit `O(1/N)` bound.
6. Hence `∫x in 0..N, sinc x → π/2` as `N → ∞`; converting `sinc` back to
   `sin x / x` (they agree everywhere except at the single, measure-zero point
   `x = 0`, which the interval `(0, N]` excludes from the integration domain
   in an a.e. sense in any case) gives the Grafakos-style statement directly.

`Real.sinc` (continuity, `|sinc| ≤ 1`) is taken from
`Mathlib.Analysis.SpecialFunctions.Trigonometric.Sinc`, exactly as suggested by
the scoping report; everything else (the actual VALUE `π/2`) is new.
-/

import Mathlib

open Real Set Filter MeasureTheory intervalIntegral Topology

noncomputable section

namespace TamesisFoundationsDirichletOscillatoryIntegral

/-! ## Step 1 : elementary closed form for `∫ t in 0..M, exp(-x*t) dt`. -/

/-- Antiderivative (in `t`) of `t ↦ exp(-x*t)`, valid for `x ≠ 0`. -/
def expAntideriv (x t : ℝ) : ℝ := -Real.exp (-x * t) / x

lemma hasDerivAt_expAntideriv {x : ℝ} (hx : x ≠ 0) (t : ℝ) :
    HasDerivAt (fun t => expAntideriv x t) (Real.exp (-x * t)) t := by
  have hExp : HasDerivAt (fun t : ℝ => Real.exp (-x * t)) (Real.exp (-x * t) * (-x)) t := by
    have : HasDerivAt (fun t : ℝ => -x * t) (-x) t := by
      simpa using (hasDerivAt_id t).const_mul (-x)
    simpa using this.exp
  have hNegDiv := hExp.neg.div_const x
  have hEq : -(Real.exp (-x * t) * (-x)) / x = Real.exp (-x * t) := by field_simp
  rw [hEq] at hNegDiv
  exact hNegDiv

lemma integral_exp_mul_neg (x : ℝ) (hx : x ≠ 0) (M : ℝ) :
    ∫ t in (0:ℝ)..M, Real.exp (-x * t) = (1 - Real.exp (-x * M)) / x := by
  have hderiv : ∀ t ∈ Set.uIcc (0:ℝ) M,
      HasDerivAt (fun t => expAntideriv x t) (Real.exp (-x * t)) t :=
    fun t _ => hasDerivAt_expAntideriv hx t
  have hcont : IntervalIntegrable (fun t => Real.exp (-x * t)) MeasureTheory.volume 0 M := by
    apply Continuous.intervalIntegrable; fun_prop
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hcont]
  simp [expAntideriv]; ring

/-- Closed form of the inner `t`-integral in terms of `Real.sinc`, valid at `x = 0` too
(both sides equal `0` there), which lets later steps avoid case-splitting on `x = 0`. -/
lemma integral_exp_mul_sin_eq_sinc (x M : ℝ) :
    ∫ t in (0:ℝ)..M, Real.exp (-t * x) * Real.sin x = Real.sinc x * (1 - Real.exp (-x * M)) := by
  rcases eq_or_ne x 0 with rfl | hx
  · simp
  · have hswap : ∀ t : ℝ, Real.exp (-t * x) = Real.exp (-x * t) := fun t => by ring_nf
    simp_rw [hswap]
    rw [intervalIntegral.integral_mul_const, integral_exp_mul_neg x hx M, Real.sinc_of_ne_zero hx]
    field_simp

/-! ## Step 2 : closed form for `∫ x in 0..N, exp(-t*x) * sin x dx`. -/

/-- Antiderivative (in `x`) of `x ↦ exp(-t*x) * sin x`. -/
def auxAntideriv (t x : ℝ) : ℝ :=
  -(Real.exp (-t * x) * (t * Real.sin x + Real.cos x)) / (1 + t ^ 2)

lemma hasDerivAt_auxAntideriv (t x : ℝ) :
    HasDerivAt (fun x => auxAntideriv t x) (Real.exp (-t * x) * Real.sin x) x := by
  have h1t : (1 : ℝ) + t ^ 2 ≠ 0 := by positivity
  have hExp : HasDerivAt (fun x : ℝ => Real.exp (-t * x)) (Real.exp (-t * x) * (-t)) x := by
    have : HasDerivAt (fun x : ℝ => -t * x) (-t) x := by
      simpa using (hasDerivAt_id x).const_mul (-t)
    simpa using this.exp
  have hTrig : HasDerivAt (fun x : ℝ => t * Real.sin x + Real.cos x)
      (t * Real.cos x - Real.sin x) x := by
    have h1 : HasDerivAt (fun x : ℝ => t * Real.sin x) (t * Real.cos x) x :=
      (Real.hasDerivAt_sin x).const_mul t
    have h2 : HasDerivAt (fun x : ℝ => Real.cos x) (-Real.sin x) x := Real.hasDerivAt_cos x
    simp only [sub_eq_add_neg]
    exact h1.add h2
  have hProd : HasDerivAt (fun x : ℝ => Real.exp (-t * x) * (t * Real.sin x + Real.cos x))
      (Real.exp (-t * x) * (-t) * (t * Real.sin x + Real.cos x)
        + Real.exp (-t * x) * (t * Real.cos x - Real.sin x)) x := hExp.mul hTrig
  have hNegDiv := (hProd.neg).div_const (1 + t ^ 2)
  have hEq : -(Real.exp (-t * x) * (-t) * (t * Real.sin x + Real.cos x)
        + Real.exp (-t * x) * (t * Real.cos x - Real.sin x)) / (1 + t ^ 2)
      = Real.exp (-t * x) * Real.sin x := by field_simp; ring
  rw [hEq] at hNegDiv
  exact hNegDiv

lemma integral_exp_mul_sin (t N : ℝ) :
    ∫ x in (0:ℝ)..N, Real.exp (-t * x) * Real.sin x
      = (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2) := by
  have h1t : (1 : ℝ) + t ^ 2 ≠ 0 := by positivity
  have hderiv : ∀ x ∈ Set.uIcc (0:ℝ) N,
      HasDerivAt (fun x => auxAntideriv t x) (Real.exp (-t * x) * Real.sin x) x :=
    fun x _ => hasDerivAt_auxAntideriv t x
  have hcont : IntervalIntegrable (fun x => Real.exp (-t * x) * Real.sin x)
      MeasureTheory.volume 0 N := by
    apply Continuous.intervalIntegrable; fun_prop
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hcont]
  simp only [auxAntideriv, mul_zero, Real.exp_zero, Real.sin_zero, Real.cos_zero, mul_one,
    zero_add]
  field_simp; ring

/-! ## Step 3 : swapping a genuinely finite (compact-rectangle) double integral. -/

lemma integrableOn_rectangle {N M : ℝ} (hN : 0 < N) (hM : 0 < M) :
    IntegrableOn (Function.uncurry (fun x t : ℝ => Real.exp (-t * x) * Real.sin x))
      (Set.uIoc (0:ℝ) N ×ˢ Set.uIoc (0:ℝ) M) := by
  rw [Set.uIoc_of_le hN.le, Set.uIoc_of_le hM.le]
  have hsub : Set.Ioc (0:ℝ) N ×ˢ Set.Ioc (0:ℝ) M ⊆ Set.Icc (0:ℝ) N ×ˢ Set.Icc (0:ℝ) M :=
    Set.prod_mono Set.Ioc_subset_Icc_self Set.Ioc_subset_Icc_self
  have hcompact : IsCompact (Set.Icc (0:ℝ) N ×ˢ Set.Icc (0:ℝ) M) :=
    isCompact_Icc.prod isCompact_Icc
  have hcont : ContinuousOn (Function.uncurry (fun x t : ℝ => Real.exp (-t * x) * Real.sin x))
      (Set.Icc (0:ℝ) N ×ˢ Set.Icc (0:ℝ) M) := by
    apply Continuous.continuousOn; fun_prop
  exact (hcont.integrableOn_compact hcompact).mono_set hsub

/-- The key finite identity linking the `sinc`-integral over `[0,N]` to a Laplace-type
integral over `[0,M]`, obtained by swapping a genuinely finite (compact-rectangle)
double integral — no improper Fubini/Tonelli argument is needed. -/
lemma sinc_integral_sub_remainder_eq {N M : ℝ} (hN : 0 < N) (hM : 0 < M) :
    (∫ x in (0:ℝ)..N, Real.sinc x) - (∫ x in (0:ℝ)..N, Real.sinc x * Real.exp (-x * M))
      = ∫ t in (0:ℝ)..M, (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2) := by
  have hswap := intervalIntegral_intervalIntegral_swap (integrableOn_rectangle hN hM)
  simp_rw [integral_exp_mul_sin] at hswap
  simp_rw [integral_exp_mul_sin_eq_sinc] at hswap
  have hsplit : ∀ x : ℝ, Real.sinc x * (1 - Real.exp (-x * M))
      = Real.sinc x - Real.sinc x * Real.exp (-x * M) := fun x => by ring
  simp_rw [hsplit] at hswap
  have hsub : (∫ x in (0:ℝ)..N, Real.sinc x - Real.sinc x * Real.exp (-x * M))
      = (∫ x in (0:ℝ)..N, Real.sinc x) - ∫ x in (0:ℝ)..N, Real.sinc x * Real.exp (-x * M) := by
    apply intervalIntegral.integral_sub
    · apply Continuous.intervalIntegrable; fun_prop
    · apply Continuous.intervalIntegrable; fun_prop
  rw [← hsub]
  exact hswap

/-! ## Step 4 : sending `M → ∞`. -/

lemma tendsto_exp_neg_mul_atTop (x : ℝ) (hx : 0 < x) :
    Tendsto (fun M : ℝ => Real.exp (-x * M)) atTop (𝓝 0) := by
  have h1 : Tendsto (fun M : ℝ => x * M) atTop atTop :=
    Filter.Tendsto.const_mul_atTop hx tendsto_id
  have h3 := Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
  simpa [Function.comp_def, neg_mul] using h3

lemma remainder_tendsto_zero {N : ℝ} (hN : 0 < N) :
    Tendsto (fun M : ℝ => ∫ x in (0:ℝ)..N, Real.sinc x * Real.exp (-x * M)) atTop (𝓝 0) := by
  have key := intervalIntegral.tendsto_integral_filter_of_dominated_convergence
    (μ := (volume : Measure ℝ)) (l := (atTop : Filter ℝ))
    (F := fun M x : ℝ => Real.sinc x * Real.exp (-x * M)) (f := fun _ : ℝ => (0:ℝ))
    (bound := fun _ : ℝ => (1:ℝ))
    (hF_meas := Filter.Eventually.of_forall (fun M => by
      apply Continuous.aestronglyMeasurable; fun_prop))
    (h_bound := by
      filter_upwards [eventually_ge_atTop (0:ℝ)] with M hM
      filter_upwards with x hx
      rw [Set.uIoc_of_le hN.le] at hx
      have hxpos : 0 < x := hx.1
      have h1 : |Real.sinc x| ≤ 1 := Real.abs_sinc_le_one x
      have h2 : Real.exp (-x * M) ≤ 1 := by
        rw [Real.exp_le_one_iff]; nlinarith
      have h3 : 0 < Real.exp (-x * M) := Real.exp_pos _
      calc ‖Real.sinc x * Real.exp (-x * M)‖
          = |Real.sinc x| * Real.exp (-x * M) := by
            rw [Real.norm_eq_abs, abs_mul, abs_of_pos h3]
        _ ≤ 1 * 1 := mul_le_mul h1 h2 h3.le zero_le_one
        _ = 1 := by ring)
    (bound_integrable := intervalIntegrable_const)
    (h_lim := by
      filter_upwards with x hx
      rw [Set.uIoc_of_le hN.le] at hx
      have hxpos : 0 < x := hx.1
      have h4 := tendsto_exp_neg_mul_atTop x hxpos
      simpa using h4.const_mul (Real.sinc x))
  simpa using key

/-! ## Step 5 : the Laplace-parameter side converges to the improper integral over `Ioi 0`. -/

lemma integrableOn_expTerm (N : ℝ) (hN : 0 < N) :
    IntegrableOn (fun t : ℝ => Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2))
      (Set.Ioi (0:ℝ)) := by
  apply Integrable.mono' (g := fun t : ℝ => 2 * Real.exp (-N * t))
  · have hN' : (-N : ℝ) < 0 := by linarith
    exact (integrableOn_exp_mul_Ioi hN' (0:ℝ)).const_mul 2
  · apply Continuous.aestronglyMeasurable
    have hnum : Continuous (fun t : ℝ => Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) := by
      fun_prop
    have hden : Continuous (fun t : ℝ => (1:ℝ) + t ^ 2) := by fun_prop
    exact hnum.div hden (fun t => by positivity)
  · filter_upwards [ae_restrict_mem measurableSet_Ioi] with t ht
    have htpos : 0 < t := ht
    have h1t : (0:ℝ) < 1 + t ^ 2 := by positivity
    have hnum : |t * Real.sin N + Real.cos N| ≤ t + 1 := by
      calc |t * Real.sin N + Real.cos N| ≤ |t * Real.sin N| + |Real.cos N| := abs_add_le _ _
        _ ≤ t * 1 + 1 := by
            apply add_le_add
            · rw [abs_mul, abs_of_pos htpos]
              exact mul_le_mul_of_nonneg_left (Real.abs_sin_le_one N) htpos.le
            · exact Real.abs_cos_le_one N
        _ = t + 1 := by ring
    have hfrac : (t + 1) / (1 + t ^ 2) ≤ 2 := by
      rw [div_le_iff₀ h1t]; nlinarith [sq_nonneg (t - 1)]
    have hexp : Real.exp (-t * N) = Real.exp (-N * t) := by ring_nf
    calc ‖Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2)‖
        = Real.exp (-t * N) * |t * Real.sin N + Real.cos N| / (1 + t ^ 2) := by
          rw [Real.norm_eq_abs, abs_div, abs_mul, abs_of_pos (Real.exp_pos _), abs_of_pos h1t]
      _ ≤ Real.exp (-t * N) * (t + 1) / (1 + t ^ 2) := by gcongr
      _ = Real.exp (-t * N) * ((t + 1) / (1 + t ^ 2)) := by ring
      _ ≤ Real.exp (-t * N) * 2 := by gcongr
      _ = 2 * Real.exp (-N * t) := by rw [hexp]; ring

lemma integrableOn_Phi_integrand (N : ℝ) (hN : 0 < N) :
    IntegrableOn
      (fun t : ℝ => (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2))
      (Set.Ioi (0:ℝ)) := by
  have heq : (fun t : ℝ => (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2))
      = fun t : ℝ =>
        (1 + t ^ 2)⁻¹ - Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2) := by
    funext t
    have h1t : (1 : ℝ) + t ^ 2 ≠ 0 := by positivity
    field_simp
  rw [heq]
  exact integrable_inv_one_add_sq.integrableOn.sub (integrableOn_expTerm N hN)

lemma S_tendsto_Phi {N : ℝ} (hN : 0 < N) :
    Tendsto (fun M : ℝ => ∫ t in (0:ℝ)..M,
        (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2))
      atTop
      (𝓝 (∫ t in Set.Ioi (0:ℝ),
        (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2))) :=
  intervalIntegral_tendsto_integral_Ioi 0 (integrableOn_Phi_integrand N hN) tendsto_id

/-! ## Step 6 : `∫ x in 0..N, sinc x = Φ(N)` for every `N > 0`. -/

/-- Partial Dirichlet integral, expressed via `Real.sinc` (so it is defined and continuous
in `N` with no case-splitting on the origin). -/
def dirichletPartial (N : ℝ) : ℝ := ∫ x in (0:ℝ)..N, Real.sinc x

/-- The Laplace-transform side of the identity, viewed as a function of `N`. -/
def phiFun (N : ℝ) : ℝ :=
  ∫ t in Set.Ioi (0:ℝ), (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2)

lemma dirichletPartial_eq_phiFun {N : ℝ} (hN : 0 < N) :
    dirichletPartial N = phiFun N := by
  have h1 : Tendsto (fun M : ℝ => dirichletPartial N
      - ∫ x in (0:ℝ)..N, Real.sinc x * Real.exp (-x * M)) atTop (𝓝 (dirichletPartial N)) := by
    have h0 : Tendsto (fun _ : ℝ => dirichletPartial N) atTop (𝓝 (dirichletPartial N)) :=
      tendsto_const_nhds
    simpa using h0.sub (remainder_tendsto_zero hN)
  have h1' : Tendsto (fun M : ℝ => ∫ t in (0:ℝ)..M,
      (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2))
      atTop (𝓝 (dirichletPartial N)) := by
    apply h1.congr'
    filter_upwards [eventually_gt_atTop (0:ℝ)] with M hM
    exact sinc_integral_sub_remainder_eq hN hM
  exact tendsto_nhds_unique h1' (S_tendsto_Phi hN)

/-! ## Step 7 : `Φ(N) → π/2` as `N → ∞`. -/

lemma phiFun_eq (N : ℝ) (hN : 0 < N) :
    phiFun N = π / 2 -
      ∫ t in Set.Ioi (0:ℝ), Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2) := by
  unfold phiFun
  have heq : (fun t : ℝ => (1 - Real.exp (-t * N) * (t * Real.sin N + Real.cos N)) / (1 + t ^ 2))
      = fun t : ℝ =>
        (1 + t ^ 2)⁻¹ - Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2) := by
    funext t
    have h1t : (1 : ℝ) + t ^ 2 ≠ 0 := by positivity
    field_simp
  rw [heq, MeasureTheory.integral_sub integrable_inv_one_add_sq.integrableOn
    (integrableOn_expTerm N hN)]
  have hpi : ∫ t in Set.Ioi (0:ℝ), (1 + t ^ 2)⁻¹ = π / 2 := by
    rw [integral_Ioi_inv_one_add_sq]; simp
  rw [hpi]

lemma psi_tendsto_zero :
    Tendsto (fun N : ℝ =>
        ∫ t in Set.Ioi (0:ℝ), Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2))
      atTop (𝓝 0) := by
  have hbound : ∀ N : ℝ, 0 < N →
      ‖∫ t in Set.Ioi (0:ℝ), Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2)‖
        ≤ 2 / N := by
    intro N hN
    have hstep : ‖∫ t in Set.Ioi (0:ℝ),
        Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2)‖
        ≤ ∫ t in Set.Ioi (0:ℝ), 2 * Real.exp (-N * t) := by
      apply MeasureTheory.norm_integral_le_of_norm_le
        ((integrableOn_exp_mul_Ioi (by linarith : (-N:ℝ) < 0) (0:ℝ)).const_mul 2)
      filter_upwards [ae_restrict_mem measurableSet_Ioi] with t ht
      have htpos : 0 < t := ht
      have h1t : (0:ℝ) < 1 + t ^ 2 := by positivity
      have hnum : |t * Real.sin N + Real.cos N| ≤ t + 1 := by
        calc |t * Real.sin N + Real.cos N| ≤ |t * Real.sin N| + |Real.cos N| := abs_add_le _ _
          _ ≤ t * 1 + 1 := by
              apply add_le_add
              · rw [abs_mul, abs_of_pos htpos]
                exact mul_le_mul_of_nonneg_left (Real.abs_sin_le_one N) htpos.le
              · exact Real.abs_cos_le_one N
          _ = t + 1 := by ring
      have hfrac : (t + 1) / (1 + t ^ 2) ≤ 2 := by
        rw [div_le_iff₀ h1t]; nlinarith [sq_nonneg (t - 1)]
      have hexp : Real.exp (-t * N) = Real.exp (-N * t) := by ring_nf
      calc ‖Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2)‖
          = Real.exp (-t * N) * |t * Real.sin N + Real.cos N| / (1 + t ^ 2) := by
            rw [Real.norm_eq_abs, abs_div, abs_mul, abs_of_pos (Real.exp_pos _), abs_of_pos h1t]
        _ ≤ Real.exp (-t * N) * (t + 1) / (1 + t ^ 2) := by gcongr
        _ = Real.exp (-t * N) * ((t + 1) / (1 + t ^ 2)) := by ring
        _ ≤ Real.exp (-t * N) * 2 := by gcongr
        _ = 2 * Real.exp (-N * t) := by rw [hexp]; ring
    have hval : ∫ t in Set.Ioi (0:ℝ), 2 * Real.exp (-N * t) = 2 / N := by
      rw [MeasureTheory.integral_const_mul, integral_exp_mul_Ioi (by linarith : (-N:ℝ) < 0) 0]
      simp; ring
    rwa [hval] at hstep
  have hsqueeze : Tendsto (fun N : ℝ => 2 / N) atTop (𝓝 0) := by
    have h2 : Tendsto (fun N : ℝ => (2:ℝ) * N⁻¹) atTop (𝓝 0) := by
      simpa using tendsto_inv_atTop_zero.const_mul (2:ℝ)
    simpa [div_eq_mul_inv] using h2
  apply squeeze_zero_norm' _ hsqueeze
  filter_upwards [eventually_gt_atTop (0:ℝ)] with N hN
  exact hbound N hN

lemma phiFun_tendsto_piDiv2 : Tendsto phiFun atTop (𝓝 (π / 2)) := by
  have heq : phiFun =ᶠ[atTop] (fun N => π / 2 -
      ∫ t in Set.Ioi (0:ℝ), Real.exp (-t * N) * (t * Real.sin N + Real.cos N) / (1 + t ^ 2)) := by
    filter_upwards [eventually_gt_atTop (0:ℝ)] with N hN
    exact phiFun_eq N hN
  rw [tendsto_congr' heq]
  have h1 : Tendsto (fun _ : ℝ => π / 2) atTop (𝓝 (π / 2)) := tendsto_const_nhds
  simpa using h1.sub psi_tendsto_zero

/-! ## Step 8 : the Dirichlet integral, `sinc` form and `sin x / x` form. -/

/-- The partial Dirichlet integral `∫₀^N sinc x dx` tends to `π/2` as `N → ∞`. -/
theorem dirichletPartial_tendsto_piDiv2 : Tendsto dirichletPartial atTop (𝓝 (π / 2)) := by
  have heq : dirichletPartial =ᶠ[atTop] phiFun := by
    filter_upwards [eventually_gt_atTop (0:ℝ)] with N hN
    exact dirichletPartial_eq_phiFun hN
  rw [tendsto_congr' heq]
  exact phiFun_tendsto_piDiv2

/-- **The Dirichlet integral.** The classical improper integral
`∫₀^∞ (sin x)/x dx = π/2`, in the standard formal sense that the partial integrals
`∫₀^N (sin x)/x dx` converge to `π/2` as `N → ∞`. This is the prerequisite classical
fact (Grafakos's Exercise 5.1.1, cited without proof inside the proof of his
Lemma 5.2.5, (5.2.10)-(5.2.14)) behind the oscillatory-integral lemma; it is proved
here in full, as a standalone, general-purpose real-analysis result. -/
theorem tendsto_integral_sin_div_atTop :
    Tendsto (fun N : ℝ => ∫ x in (0:ℝ)..N, Real.sin x / x) atTop (𝓝 (π / 2)) := by
  have heq : (fun N : ℝ => ∫ x in (0:ℝ)..N, Real.sin x / x) = dirichletPartial := by
    funext N
    unfold dirichletPartial
    apply intervalIntegral.integral_congr_ae
    have h0 : (volume : Measure ℝ) {(0:ℝ)} = 0 := measure_singleton 0
    filter_upwards [compl_mem_ae_iff.mpr h0] with x hx _
    simp only [Set.mem_compl_iff, Set.mem_singleton_iff] at hx
    exact (Real.sinc_of_ne_zero hx).symm
  rw [heq]
  exact dirichletPartial_tendsto_piDiv2

end TamesisFoundationsDirichletOscillatoryIntegral

/-!
## Scope and honest gap note (not part of the formal development above)

Grafakos's Lemma 5.2.5 itself — the `log(1/|a|)` limits (5.2.10)-(5.2.13) — is
NOT formalized in this file, by deliberate scope decision, not because of a
Mathlib gap discovered while trying: the authorized scope for today's session
was the Dirichlet integral alone (see the file header). Two honest observations
for whoever picks this up next:

* Grafakos's own proof of (5.2.10)/(5.2.11) (the real, `cos(ra) - cos(r)`
  version) does NOT need the Dirichlet integral proved above at all — it is a
  self-contained FTC + one-integration-by-parts argument bounding
  `∫_N^{N|a|} cos(t)/t dt → 0`. That would be a separate, comparably-sized
  formalization task, independent of everything in this file.
* It is only the complex/`sgn`-carrying statement (5.2.12)/(5.2.13), via the
  auxiliary claim (5.2.14) about `∫ sin(r)/r dr → π/2`, that actually consumes
  the Dirichlet integral proved above (specifically, the *bounded* half of
  (5.2.14) — `|∫_ε^N sin(x)/x dx| ≤ 4` — is not yet available from this file
  and would need a short separate uniform-bound lemma in addition to the
  convergence fact already proved here).

Neither of these is attempted here; this file's only claim is the complete,
fully-closed-proof formalization of the Dirichlet integral itself.
-/
