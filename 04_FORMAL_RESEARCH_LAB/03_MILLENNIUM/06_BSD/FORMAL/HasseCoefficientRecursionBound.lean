/-
BSD-3 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`CalderonZygmundKernelDefinitions.lean`, `02_NAVIER_STOKES/FORMAL/`,
`03_MILLENNIUM/06_BSD/FORMAL/LFunctionMultiplicativity.lean`).

## What this file is

This is the adversarial reviewer's *narrowed* test for candidate
BSD-HASSE-CONDITIONAL-CONV-001, attempted in isolation and independent of
`WeierstrassCurve`/`LSeries`/`HeightOneSpectrum` machinery.

The local Euler factor of an elliptic-curve L-function at a good prime has
the shape `1 / (1 - a T + q T^2)` (`a` the trace of Frobenius, `q` the
residue-field size). Writing this as a power series `∑ c_n T^n`, the
coefficients satisfy the two-term linear recursion
`c_0 = 1`, `c_1 = a`, `c_{n+1} = a * c_n - q * c_{n-1}`.
Hasse's theorem (NOT proved or assumed true anywhere in this file, only
ever used as an explicit *hypothesis* on real numbers `a`, `q`) says
`|a| ≤ 2 * sqrt q`. The question tested here: does that hypothesis alone
force `|c_n| ≤ (n+1) * q^(n/2)`, the growth rate needed to eventually
invoke `LSeriesSummable_of_le_const_mul_rpow`
(`Mathlib/NumberTheory/LSeries/Basic.lean:341`) once/if such a bound is
ever assembled into a genuine global Dirichlet-coefficient estimate?

This file answers that question: **yes, unconditionally, with a complete
proof** -- but the naive proof strategy the recon suggested (direct
two-step induction using only the triangle inequality on the numeric
recursion) provably does NOT work, and a materially different route
(trigonometric parametrisation via Mathlib's Chebyshev-polynomial-of-the-
-second-kind machinery) was required. Both facts are recorded here
honestly, per the reviewer's own prediction that this "is real,
self-contained combinatorial/analytic work, not a routine estimate."

## Why the naive triangle-inequality induction fails (checked by hand
before writing any Lean, and left here as documentation since it explains
why this file's proof looks the way it does)

Assume only `|c_n| ≤ (n+1) q^{n/2}` and `|c_{n-1}| ≤ n q^{(n-1)/2}` and try
to bound `|c_{n+1}| = |a c_n - q c_{n-1}| ≤ |a| |c_n| + q |c_{n-1}|` using
`|a| ≤ 2√q`. This gives `|c_{n+1}| ≤ (3n+2) q^{(n+1)/2}`, and
`3n + 2 > n + 2` for every `n ≥ 1` -- so the crude bound is too weak to
sustain the induction past the second step. Concretely, at the extremal
case `a = -2√q` (where the true bound is tight for *every* n), the actual
recursion produces massive sign cancellation between the `a c_n` and
`-q c_{n-1}` terms (e.g. `c_3 = -4 q^{3/2}` while the triangle-inequality
bound only gives `8 q^{3/2}`) that a bound on absolute values alone cannot
see. The linear-in-`n` growth rate is a genuine "resonance" phenomenon
(only saturated in the limit `a → ±2√q`) that requires tracking the
*angle*, not just the magnitude, of the recursion's state.

## The proof that does work: identify `c_n` with a Chebyshev polynomial

Writing `a = 2√q cos θ` (possible exactly because `|a| ≤ 2√q`), the
substitution `c_n = q^{n/2} · U_n(cos θ)` turns the numeric recursion into
exactly the recursion defining Mathlib's Chebyshev polynomials of the
second kind, `Polynomial.Chebyshev.U` (`Mathlib/RingTheory/Polynomial/
Chebyshev.lean:265`, recursion at `U_add_two`, evaluated at `cos θ` via
`U_real_cos` in `Mathlib/Analysis/SpecialFunctions/Trigonometric/
Chebyshev/Basic.lean:155`). The needed bound `|U_n(cos θ)| ≤ n+1` is
*not* already in Mathlib as a stated lemma (checked: no `abs_eval_U`-style
bound exists anywhere in `Mathlib/Analysis/SpecialFunctions/Trigonometric/
Chebyshev/` or `Mathlib/RingTheory/Polynomial/Chebyshev.lean`), so it is
proved here from three ingredients that ARE in Mathlib:
* `U_real_cos`, reducing the generic case (`sin θ ≠ 0`) to the classical
  fact `|sin((n+1)θ)| ≤ (n+1)|sin θ|` (itself proved here from scratch by
  a one-line induction on `Real.sin_add`, since no packaged form of this
  fact was found in Mathlib either);
* `Polynomial.Chebyshev.U_eval_one` and `U_eval_neg_one`
  (`Mathlib/RingTheory/Polynomial/Chebyshev.lean:327,342`), which handle
  the degenerate case `sin θ = 0` (i.e. `cos θ = ±1`, i.e. `a = ±2√q`
  exactly) where the `sin`-ratio argument divides by zero and a separate
  closed form is needed;
* `Real.rpow_add`/`Real.sqrt_eq_rpow`/`Real.mul_self_sqrt`, to manage the
  half-integer exponents `q^(n/2)` algebraically across the induction
  step (this is where the bulk of the fiddly, non-conceptual Lean work
  actually was).

The `q = 0` case is handled separately and trivially (`|a| ≤ 2√0 = 0`
forces `a = 0`, and then the recursion collapses to `c_n = 0` for `n ≥ 1`
regardless of the values being multiplied, since both coefficients in the
recursion are literally `0`).

## What this file does NOT prove (honest scope, matching BSD-1's note)

This is a self-contained fact about a real-coefficient two-term linear
recursion. It says nothing about `WeierstrassCurve.LFunction`, does not
invoke `LSeriesSummable_of_le_const_mul_rpow` (that step would still need
turning this *local* coefficient bound into a *global* Dirichlet-series
coefficient bound via multiplicativity, i.e. candidate BSD-1's diagnosed
gap, plus an actual sum-over-primes argument -- neither attempted here).
It does NOT prove Hasse's theorem (`|a_p| ≤ 2√p` for actual traces of
Frobenius on actual elliptic curves is assumed as an explicit, named
hypothesis of every theorem below, never derived). It makes zero claim of
novelty (the bound `|U_n(cos θ)| ≤ n+1` is completely classical) and zero
claim of progress toward the Birch and Swinnerton-Dyer conjecture (a Clay
Millennium Problem) or toward any convergence statement about a genuine
elliptic-curve L-function.
-/

import Mathlib.RingTheory.Polynomial.Chebyshev
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Real Polynomial.Chebyshev

namespace TamesisLab.BSD3

/-- `cPair a q n = (c n, c (n+1))` for the recursion `c 0 = 1`, `c 1 = a`,
`c (n+2) = a * c (n+1) - q * c n`, packaged as a pair so the two-term
recursion becomes ordinary structural recursion on `ℕ`. -/
noncomputable def cPair (a q : ℝ) : ℕ → ℝ × ℝ
  | 0 => (1, a)
  | n + 1 => let p := cPair a q n; (p.2, a * p.2 - q * p.1)

/-- The Dirichlet coefficients of the formal power series `1 / (1 - a T + q T^2)`:
`c 0 = 1`, `c 1 = a`, `c (n+2) = a * c (n+1) - q * c n`. This is exactly the
recursion satisfied by the coefficients of the reciprocal of a Hasse-bound-shaped
local Euler factor `1 - a T + q T^2` (`a` = trace of Frobenius, `q` = residue
field size), see the file docstring. -/
noncomputable def cSeq (a q : ℝ) (n : ℕ) : ℝ := (cPair a q n).1

theorem cSeq_zero (a q : ℝ) : cSeq a q 0 = 1 := rfl

theorem cSeq_one (a q : ℝ) : cSeq a q 1 = a := rfl

theorem cSeq_succ_succ (a q : ℝ) (n : ℕ) :
    cSeq a q (n + 2) = a * cSeq a q (n + 1) - q * cSeq a q n := rfl

/-- Classical fact (not found packaged in Mathlib): `|sin((n+1)x)| ≤ (n+1)|sin x|`
for every real `x` and every `n : ℕ`, proved by induction on `Real.sin_add`. -/
theorem abs_sin_nat_succ_mul_le (x : ℝ) :
    ∀ n : ℕ, |Real.sin ((n + 1) * x)| ≤ (n + 1) * |Real.sin x| := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
    push_cast
    have hcast : ((n : ℝ) + 1 + 1) * x = (n + 1) * x + x := by ring
    rw [hcast, Real.sin_add]
    calc |Real.sin ((n + 1) * x) * Real.cos x + Real.cos ((n + 1) * x) * Real.sin x|
        ≤ |Real.sin ((n + 1) * x) * Real.cos x| + |Real.cos ((n + 1) * x) * Real.sin x| :=
          abs_add_le _ _
      _ = |Real.sin ((n + 1) * x)| * |Real.cos x| + |Real.cos ((n + 1) * x)| * |Real.sin x| := by
          rw [abs_mul, abs_mul]
      _ ≤ ((n : ℝ) + 1) * |Real.sin x| * 1 + 1 * |Real.sin x| := by
          gcongr
          · exact Real.abs_cos_le_one x
          · exact Real.abs_cos_le_one _
      _ = ((n : ℝ) + 1 + 1) * |Real.sin x| := by ring

/-- The classical extremal bound `|U_n(cos θ)| ≤ n + 1` for Chebyshev polynomials
of the second kind. Not found stated in Mathlib (checked
`Mathlib/RingTheory/Polynomial/Chebyshev.lean` and
`Mathlib/Analysis/SpecialFunctions/Trigonometric/Chebyshev/*`); proved here from
`U_real_cos` (generic case) plus `U_eval_one`/`U_eval_neg_one` (the degenerate
`sin θ = 0` case, where the `sin`-ratio argument divides by zero). -/
theorem abs_eval_U_real_cos_le (θ : ℝ) (n : ℕ) :
    |(U ℝ (n : ℤ)).eval (Real.cos θ)| ≤ (n : ℝ) + 1 := by
  rcases eq_or_ne (Real.sin θ) 0 with hs | hs
  · have hc2 : Real.cos θ ^ 2 = 1 := by
      have := Real.sin_sq_add_cos_sq θ
      rw [hs] at this; linarith [this]
    have hc : Real.cos θ = 1 ∨ Real.cos θ = -1 := by
      have h0 : (Real.cos θ - 1) * (Real.cos θ + 1) = 0 := by nlinarith [hc2]
      rcases mul_eq_zero.mp h0 with h | h
      · left; linarith
      · right; linarith
    rcases hc with hc | hc
    · rw [hc, U_eval_one]
      push_cast
      rw [abs_of_nonneg (by positivity)]
    · rw [hc, U_eval_neg_one]
      rw [abs_mul]
      have habsnop : |((n : ℤ).negOnePow : ℤ)| = 1 := Int.abs_negOnePow n
      have habsnop' : |(((n : ℤ).negOnePow : ℤ) : ℝ)| = 1 := by
        rw [← Int.cast_abs, habsnop]; norm_num
      rw [habsnop']
      push_cast
      rw [abs_of_nonneg (by positivity : (0 : ℝ) ≤ (n : ℝ) + 1)]
      linarith
  · have hrel := U_real_cos θ (n : ℤ)
    have habs := congrArg abs hrel
    rw [abs_mul] at habs
    have hbound := abs_sin_nat_succ_mul_le θ n
    have hcasteq : ((n : ℤ) + 1 : ℝ) * θ = ((n : ℝ) + 1) * θ := by push_cast; ring
    rw [hcasteq] at habs
    rw [← habs] at hbound
    have hsinpos : 0 < |Real.sin θ| := abs_pos.mpr hs
    have hfinal : |(U ℝ (n : ℤ)).eval (Real.cos θ)| * |Real.sin θ| ≤
        ((n : ℝ) + 1) * |Real.sin θ| := hbound
    exact le_of_mul_le_mul_right (by linarith [hfinal]) hsinpos

/-- Core identification (`q > 0` case): the coefficient recursion `cSeq a q` agrees
with `q^(n/2) * U_n(cos θ)` for the angle `θ` with `cos θ = a / (2√q)` (which exists
exactly because `|a| ≤ 2√q`, the Hasse-bound hypothesis, is what makes `a / (2√q)`
land in `[-1, 1]`; note `θ` itself is NOT assumed to exist here, it is a hypothesis
of this lemma supplied by the caller via `Real.arccos`). Proved by a paired
one-step induction (carrying both `cSeq n` and `cSeq (n+1)` simultaneously, the
standard trick for two-term recurrences), matching `cSeq`'s recursion against
`Polynomial.Chebyshev.U_add_two` term by term. -/
theorem cSeq_eq_rpow_mul_U (a q : ℝ) (hq : 0 < q) (θ : ℝ)
    (hcos : Real.cos θ = a / (2 * Real.sqrt q)) :
    ∀ n : ℕ, cSeq a q n = q ^ ((n : ℝ) / 2) * (U ℝ (n : ℤ)).eval (Real.cos θ) := by
  have hsqrt : Real.sqrt q > 0 := Real.sqrt_pos.mpr hq
  have hss : Real.sqrt q * Real.sqrt q = q := Real.mul_self_sqrt hq.le
  have ha_eq : a = 2 * Real.sqrt q * Real.cos θ := by
    rw [hcos]; field_simp
  have haq : a * Real.sqrt q = 2 * Real.cos θ * q := by
    have h1 : a * Real.sqrt q = 2 * Real.cos θ * (Real.sqrt q * Real.sqrt q) := by
      rw [ha_eq]; ring
    rw [h1, hss]
  have hhalf : q ^ ((1 : ℝ) / 2) = Real.sqrt q := (Real.sqrt_eq_rpow q).symm
  have key : ∀ n : ℕ, cSeq a q n = q ^ ((n : ℝ) / 2) * (U ℝ (n : ℤ)).eval (Real.cos θ) ∧
      cSeq a q (n + 1) = q ^ (((n : ℝ) + 1) / 2) * (U ℝ ((n : ℤ) + 1)).eval (Real.cos θ) := by
    intro n
    induction n with
    | zero =>
      refine ⟨by simp [cSeq_zero], ?_⟩
      simp only [Nat.cast_zero, zero_add, cSeq_one, U_one, Polynomial.eval_mul,
        Polynomial.eval_ofNat, Polynomial.eval_X]
      rw [hhalf, ha_eq]; ring
    | succ n ih =>
      obtain ⟨ih0, ih1⟩ := ih
      push_cast
      refine ⟨ih1, ?_⟩
      have hUstep : (U ℝ ((n : ℤ) + 1 + 1)).eval (Real.cos θ) =
          2 * Real.cos θ * (U ℝ ((n : ℤ) + 1)).eval (Real.cos θ) -
            (U ℝ (n : ℤ)).eval (Real.cos θ) := by
        have h := U_add_two (R := ℝ) (n : ℤ)
        have heq2 : (n : ℤ) + 1 + 1 = (n : ℤ) + 2 := by ring
        rw [heq2, h]
        simp
      rw [cSeq_succ_succ, ih1, ih0, hUstep]
      have hpow_half : q ^ (((n : ℝ) + 1) / 2) = Real.sqrt q * q ^ ((n : ℝ) / 2) := by
        rw [show ((n : ℝ) + 1) / 2 = (n : ℝ) / 2 + 1 / 2 by ring, Real.rpow_add hq, hhalf]; ring
      have hpow_full : q ^ (((n : ℝ) + 1 + 1) / 2) = q * q ^ ((n : ℝ) / 2) := by
        rw [show ((n : ℝ) + 1 + 1) / 2 = (n : ℝ) / 2 + 1 by ring, Real.rpow_add hq,
          Real.rpow_one]; ring
      rw [hpow_full, hpow_half]
      linear_combination (q ^ ((n : ℝ) / 2) * (U ℝ ((n : ℤ) + 1)).eval (Real.cos θ)) * haq
  exact fun n => (key n).1

/-- **Main result attempted for BSD-3.** Given the explicit, honestly-flagged
Hasse-bound-shaped hypothesis `|a| ≤ 2√q` (this is a hypothesis on arbitrary
reals `a q`, NOT a proof of Hasse's theorem for actual elliptic curves), the
coefficients of `1/(1 - a T + q T²)` satisfy `|c_n| ≤ (n+1) q^(n/2)`. This is
the exact statement the reviewer's narrowed test asked for, fully proved with
no forbidden placeholder tokens of any kind (see the repository's governance
policy). See the file docstring for what this does and does not establish
about actual L-functions. -/
theorem cSeq_abs_le (a q : ℝ) (hq : 0 ≤ q) (ha : |a| ≤ 2 * Real.sqrt q) :
    ∀ n : ℕ, |cSeq a q n| ≤ ((n : ℝ) + 1) * q ^ ((n : ℝ) / 2) := by
  rcases hq.lt_or_eq with hqpos | hq0
  swap
  · -- q = 0: the Hasse-bound hypothesis forces a = 0, collapsing the recursion.
    subst hq0
    have ha0 : a = 0 := by
      have : |a| ≤ 0 := by simpa using ha
      exact abs_eq_zero.mp (le_antisymm this (abs_nonneg a))
    subst ha0
    have hzero2 : ∀ k : ℕ, cSeq (0 : ℝ) 0 (k + 2) = 0 := by intro k; rw [cSeq_succ_succ]; ring
    have hzero1 : cSeq (0 : ℝ) 0 1 = 0 := cSeq_one 0 0
    intro n
    rcases n with _ | _ | k
    · simp [cSeq_zero]
    · simp [hzero1]
    · have hz : cSeq (0 : ℝ) (0 : ℝ) (k + 2) = 0 := hzero2 k
      rw [hz, abs_zero]
      positivity
  · -- q > 0: identify cSeq with q^(n/2) * U_n(cos θ) and bound via
    -- abs_eval_U_real_cos_le.
    have hbound_cos : |a / (2 * Real.sqrt q)| ≤ 1 := by
      rw [abs_div, abs_of_pos (by positivity : (0 : ℝ) < 2 * Real.sqrt q)]
      rw [div_le_one (by positivity)]
      exact ha
    obtain ⟨hlo, hhi⟩ := abs_le.mp hbound_cos
    set θ := Real.arccos (a / (2 * Real.sqrt q)) with hθdef
    have hcos : Real.cos θ = a / (2 * Real.sqrt q) := Real.cos_arccos hlo hhi
    intro n
    have hident := cSeq_eq_rpow_mul_U a q hqpos θ hcos n
    rw [hident, abs_mul, abs_of_nonneg (by positivity : (0 : ℝ) ≤ q ^ ((n : ℝ) / 2))]
    have hUbound := abs_eval_U_real_cos_le θ n
    have hmul : q ^ ((n : ℝ) / 2) * |(U ℝ (n : ℤ)).eval (Real.cos θ)| ≤
        q ^ ((n : ℝ) / 2) * ((n : ℝ) + 1) := by gcongr
    calc q ^ ((n : ℝ) / 2) * |(U ℝ (n : ℤ)).eval (Real.cos θ)|
        ≤ q ^ ((n : ℝ) / 2) * ((n : ℝ) + 1) := hmul
      _ = ((n : ℝ) + 1) * q ^ ((n : ℝ) / 2) := by ring

#print axioms cSeq_zero
#print axioms cSeq_one
#print axioms cSeq_succ_succ
#print axioms abs_sin_nat_succ_mul_le
#print axioms abs_eval_U_real_cos_le
#print axioms cSeq_eq_rpow_mul_U
#print axioms cSeq_abs_le

end TamesisLab.BSD3
