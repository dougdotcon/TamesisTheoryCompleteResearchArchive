import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.Analysis.PSeries

set_option autoImplicit false

/-!
# RH-5 — Trivial half-plane growth bound for `riemannZeta`

This file is a narrow, self-contained reconnaissance result. It is the
single-session probe proposed for the "Nevanlinna/Jensen-formula route to an
unconditional crude zero-counting bound" line of inquiry, after that inquiry
was narrowed by adversarial review.

## Background / motivation (recorded for continuity, not re-litigated here)

The original angle asked whether Mathlib's general Nevanlinna/value-distribution
machinery (`Mathlib.Analysis.Complex.ValueDistribution.LogCounting.Asymptotic`,
in particular `logCounting_isBigO_one_iff_analyticOnNhd`) could be instantiated
on `riemannZeta` to get an unconditional crude `N(T) = O(T log T)` bound,
entirely bypassing spectral/operator machinery. Doing so requires a
growth/convexity bound for `riemannZeta` **inside the critical strip**
(`0 < re s < 1`), of the classical form `|ζ(σ + it)| = O(|t|^c)`. An
exhaustive search of `Mathlib.NumberTheory.LSeries.RiemannZeta` (independently
re-run twice, by the recon pass and by adversarial review) confirms **no such
critical-strip bound exists** in the pinned Mathlib revision.

Because that search was already exhaustively completed (twice), the
adversarial review narrowed the single-session test to something sharper and
non-redundant: attempt the much weaker, classically trivial bound
`|ζ(σ + it)| = O(1)` for a **fixed** `σ > 1` (i.e. strictly to the right of
the critical strip, where the Dirichlet series `∑ 1/n^s` converges
absolutely), using only the Euler-product/Dirichlet-series machinery Mathlib
already has for `re s > 1`. The question posed: is even this trivial
half-plane bound already packaged as a reusable `IsBigO` lemma, or does it
require hand-assembly from the raw series?

## What is proved here

`riemannZeta_norm_le_of_one_lt_re`: for fixed `σ > 1`, `‖ζ(σ + it)‖` is
bounded, **uniformly in `t : ℝ`** (not merely eventually as `t → ∞`), by the
real constant `∑' n, 1 / n ^ σ` — the value of the convergent real `p`-series
at `σ`. This is in fact a *stronger* statement than the requested `IsBigO`:
the bound holds on the whole vertical line, not just eventually.

`riemannZeta_isBigO_one_of_one_lt_re`: the requested restatement of the above
as `(fun t => ζ(σ + it)) =O[atTop] (fun _ => (1:ℝ))`, obtained as an
immediate corollary.

## Method (answering the falsifiable question)

**No pre-packaged `IsBigO`/growth-rate lemma for `riemannZeta` on a vertical
line exists anywhere in Mathlib** (confirmed by grep across all files
importing `RiemannZeta.lean`, matching the recon's and the adversarial
review's independent findings). The bound above had to be hand-assembled
from three independent, pre-existing pieces of infrastructure, none of which
mention `riemannZeta` on a vertical line at all:

1. `zeta_eq_tsum_one_div_nat_cpow` (`Mathlib.NumberTheory.LSeries.RiemannZeta`)
   — the Dirichlet series identity for `re s > 1`;
2. `Complex.norm_natCast_cpow_of_re_ne_zero` (`Mathlib.Analysis.SpecialFunctions.Pow.Real`)
   — a *uniform-in-`n`* norm formula `‖(n:ℂ)^s‖ = n ^ s.re`, valid for every
   `n : ℕ` (including `n = 0`) as long as `s.re ≠ 0`, which is what lets the
   pointwise term bound below skip an `n = 0` case split entirely;
3. `norm_tsum_le_tsum_norm` (`Mathlib.Analysis.Normed.Group.InfiniteSum`) and
   `Real.summable_one_div_nat_rpow` (`Mathlib.Analysis.PSeries`) — the tsum
   triangle inequality and real `p`-series convergence test.

Assembly was mechanical and required no new mathematics: the term-by-term
norm identity is exact and `t`-independent (`‖1/(n:ℂ)^(σ+it)‖ = 1/n^σ` for
every `t`), so the triangle-inequality bound on the tsum inherits that
`t`-independence for free. This confirms the adversarial review's prediction
precisely: the trivial half-plane bound is **not** pre-packaged, and **does**
require hand-assembly from raw summability facts — but that assembly is
low-cost (three composed lemmas, no case analysis, no new estimates) given
that `re s > 1` is exactly the region where Mathlib already has full
absolute-convergence infrastructure for the Dirichlet series.

## What this explicitly does NOT show

* **Nothing about the critical strip.** The method here is entirely specific
  to `re s > 1`, where `∑ 1/n^s` converges absolutely; the bound obtained
  (`t`-independent!) is a degenerate/trivial case that says nothing about
  growth *inside* `0 < re s < 1`, which is where the Jensen-formula route
  actually needs input. The critical-strip convexity bound remains
  classical-but-unformalized: it needs the functional equation plus Stirling
  estimates for `Gamma`, genuinely different (and substantially harder)
  infrastructure than what is assembled here.
* **Not a step toward `N(T) = O(T log T)`.** No zero-counting, no Jensen
  formula, no `logCounting` instantiation is attempted here.
* **Not a proof or approximation of RH**, and not connected to
  `TamesisLab.RHNogo` (`ASYM-NOGO-001` and its descendants): nothing here is
  imported by, or imports, that chain. This file stands alone, matching the
  standalone-file convention already used for other one-off Millennium-line
  reconnaissance results in this lab (e.g.
  `TamesisLab.Riemann.ZetaZerosCountingFiniteness`, RH-2).

## Verdict for the parent line of inquiry

The half-plane case (this file) is cheap; the critical-strip case (what the
Jensen/Nevanlinna route actually needs) is not. This is consistent with, and
adds one concrete data point to, the recon's original deprioritization
recommendation: the low-cost part of the growth-bound question is answered
(assembling `O(1)` on a fixed half-plane line is a routine exercise), while
the genuinely load-bearing part (a strip-interior convexity bound) remains
unformalized and outside single-session scope.

scientific_novelty: NONE_CLAIMED_MATHLIB_WIRING_ONLY
-/

namespace TamesisLab.Riemann

open Complex Filter

/-- **Main result.** For fixed `σ > 1`, `riemannZeta` is bounded on the
vertical line `re s = σ`, *uniformly* in `t = im s` (for every `t : ℝ`, not
merely eventually), by the real constant `∑' n, 1 / n ^ σ`. This is the
"trivial half-plane" growth bound: it holds strictly to the right of the
critical strip, where the Dirichlet series for `ζ` converges absolutely, and
says nothing about growth inside `0 < re s < 1`. -/
theorem riemannZeta_norm_le_of_one_lt_re {σ : ℝ} (hσ : 1 < σ) (t : ℝ) :
    ‖riemannZeta (σ + t * Complex.I)‖ ≤ ∑' n : ℕ, 1 / (n : ℝ) ^ σ := by
  set s : ℂ := σ + t * Complex.I with hs_def
  have hs_re : s.re = σ := by simp [hs_def]
  have hs_re_ne : s.re ≠ 0 := by rw [hs_re]; linarith
  have hs_gt : 1 < s.re := by rw [hs_re]; exact hσ
  -- Term-by-term norm identity, uniform in `n` (no `n = 0` case split needed)
  -- and `t`-independent: only `s.re = σ` matters, not `s.im = t`.
  have hterm_eq : ∀ n : ℕ, ‖(1 : ℂ) / (n : ℂ) ^ s‖ = 1 / (n : ℝ) ^ σ := by
    intro n
    rw [norm_div, norm_one, Complex.norm_natCast_cpow_of_re_ne_zero n hs_re_ne, hs_re]
  have hsummable_real : Summable (fun n : ℕ => 1 / (n : ℝ) ^ σ) :=
    Real.summable_one_div_nat_rpow.mpr hσ
  have hsummable_norm : Summable (fun n : ℕ => ‖(1 : ℂ) / (n : ℂ) ^ s‖) :=
    hsummable_real.congr (fun n => (hterm_eq n).symm)
  calc ‖riemannZeta s‖
      = ‖∑' n : ℕ, (1 : ℂ) / (n : ℂ) ^ s‖ := by rw [zeta_eq_tsum_one_div_nat_cpow hs_gt]
    _ ≤ ∑' n : ℕ, ‖(1 : ℂ) / (n : ℂ) ^ s‖ := norm_tsum_le_tsum_norm hsummable_norm
    _ = ∑' n : ℕ, 1 / (n : ℝ) ^ σ := tsum_congr hterm_eq

/-- Restatement of `riemannZeta_norm_le_of_one_lt_re` in `IsBigO` form, as
literally requested by the falsifiable test: for fixed `σ > 1`,
`t ↦ ζ(σ + it) = O(1)` as `t → ∞`. (The proof above in fact gives the
stronger uniform-in-`t` bound; this corollary only restates it in the
requested asymptotic vocabulary.) -/
theorem riemannZeta_isBigO_one_of_one_lt_re {σ : ℝ} (hσ : 1 < σ) :
    (fun t : ℝ => riemannZeta (σ + t * Complex.I)) =O[atTop] (fun _ : ℝ => (1 : ℝ)) := by
  refine Asymptotics.IsBigO.of_bound (∑' n : ℕ, 1 / (n : ℝ) ^ σ) ?_
  filter_upwards with t
  simpa using riemannZeta_norm_le_of_one_lt_re hσ t

/-! ## Axiom audit

Expected for every declaration below: only `propext`, `Classical.choice`,
`Quot.sound` (inherited from Mathlib's own use of classical logic and
quotients) -- nothing locally declared, nothing incomplete. -/

#print axioms riemannZeta_norm_le_of_one_lt_re
#print axioms riemannZeta_isBigO_one_of_one_lt_re

end TamesisLab.Riemann
