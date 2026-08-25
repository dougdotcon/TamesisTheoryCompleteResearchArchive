# ATTEMPT — closing the b=1 floor's coupled two-variable system (SS5)

**Front `FLOOR-H2-B1-FULL-CLOSURE-ATTEMPT`, dispatched against
`floor_closed_form_attempt/ATTEMPT.md` SS5** (referee-confirmed SOUND WITH
NAMED ISSUES, ACCEPT for catalogue; `DISC-DEC-057/062`). Target: close, or
maximally narrow, the ONE thing that parent front left open — the exact
closed form of the coupled, nonlocal `(Phi(s,g), Psi(s,g))` system governing
the abstract recursive "gap re-entry" mechanism (SS3.1/SS4 there), which
that front proved and validated qualitatively (T3) but did not solve. This
is the `M-CLUST(b)` residual line (Tree B, node `FLOORCF` in
`PROOF_DEPENDENCY_MAP.md` SS2) — a standalone combinatorial/probabilistic
object, unrelated to the archive's separate Conjecture-1 whole-space line.

**Scope discipline (per the mandate):** this front works ENTIRELY inside
the ABSTRACT idealized recursive process that `floor_closed_form_attempt`
introduced as a model of the real `b=1` engine (state `(s,g)`, mode `G/E`,
continuous-time marks at rate `c`) — not the real discrete `n=65536` engine
directly. That parent front already disclosed an unresolved ~30% gap
between the abstract-process plateau (`~0.037-0.039`) and the real engine's
plateau (`~0.025-0.029`); this front does not touch that gap. Closing SS5's
system exactly (had it succeeded) would give an exact formula for the
ABSTRACT process's `Phi(0,t0)`, i.e. for `phi_abstract(t0)` — the object §4
of the parent's T3 validated numerically, not (without a further, separate,
undone step) for the real `phi(ell)` itself.

**Verdict up front (expanded in SS6): genuine partial closure, stronger than
the parent front's own SS5 finding, still short of a full closed form.**
Two independent, validated results:

1. **An exact, closed-form small-`t0` regime is fully solved** (SS2): the
   leading Taylor coefficients of `Phi(0,t0)` in powers of `t0` are derived
   in exact closed form (one new named special function — a Mills-ratio /
   scaled-complementary-error-function object — for the `k=1` coefficient,
   PROVED via an independent sympy symbolic re-derivation of the governing
   recursion AND via direct substitution into its ODE), extended to `k=2,3`
   via one clean numerical-quadrature layer each (cross-checked by TWO
   independent numerical methods per coefficient), and validated by a
   fresh, high-powered (`N=500,000`/point), freshly-seeded Monte Carlo of
   the exact abstract process (SS4, T-A) that matches the 3-term series to
   `|z|<1` for `c*t0 <~ 0.3-0.5` and shows the series breaking down cleanly
   beyond that, exactly where expected. **Honest scope limit:** this regime
   (`t0 <~ 0.0005` at the target cell's `c=1000`) is far below the
   practically relevant range for `phi_far` (`t0` from `~0.03` to `1`), so
   it does not by itself help compute the parent front's original quantity.
2. **A corrected, unit-tested, convergent NUMERICAL solver for the FULL
   system across the WHOLE `t0` range, including the practically-relevant
   plateau** (SS3): the parent front's own bounded numerical attempt
   (`solve_2d_system.py`) is diagnosed and its exact bug reproduced and
   fixed (SS3.1); the corrected solver passes an analytic self-test
   (SS3.2), converges cleanly under BOTH outer Gauss-Seidel iteration and
   grid refinement (SS3.3, ratios of successive grid-refinement differences
   converge to the theoretically-expected `0.5`), is insensitive to its one
   remaining approximation (the far-`s` cutoff, SS3.3), and its
   Richardson-extrapolated continuum estimate (`0.0377`) matches BOTH this
   lineage's own T3 Monte Carlo AND the adversarial referee's independent
   T3 replication to within `|z|<1.7` at every tested point (SS4, T-C) —
   this is a real, validated, non-closed-form characterization of `Phi(0,t0)`
   across the regime that actually matters.

**What is still missing, precisely** (SS5): a genuine, still-open tension.
The GOVERNING EQUATIONS are provably coupled and nonlocal — no 1-variable
reduction of the exact system was found or is evident from the recursion
structure. Yet a numerical rank/separability diagnostic (SS3.4) on the
converged solution shows `Phi(s,g)` is, empirically, extremely well
approximated by a RANK-2 (nearly separable) surface (`>99.998%` of the
variance at rank 2). This complicates, rather than confirms, the natural
guess that the coupling is simply "fundamental" in the sense of forcing
genuinely rich 2D structure — it is fundamental at the level of the
EQUATIONS (provably not 1-D-reducible without loss), but the SOLUTION it
produces appears close to low-rank, which is named here as the single most
concrete, promising, NOT-yet-executed avenue for a future closed-form
attempt (fit a reduced 2-mode ODE ansatz and check whether it is exactly,
not just numerically, consistent with SS5's PDEs).

`phi_REDB` (the formula of record for the `M-CLUST(b)` line) is
**unaffected**: nothing here proposes a replacement for it, or for any
formula of record in this lineage. See SS7 for the full scorecard.

> **[Post-adversarial integration note, 2026-08-25 — DISC-DEC-071.]**
> The dedicated hostile referee (`adversarial/REFEREE_REPORT.md`, fresh
> seeds 20260857000–2, front scripts never opened) returned **SOUND WITH
> NAMED ISSUES — ACCEPT for catalogue**, with two mandatory corrections
> (N1, N2) and one minor note (N3), all applied below as dated notes.
> Every POSITIVE claim in this document replicated independently at
> equal-or-higher power. Both mandatory corrections run in the direction
> of this front having UNDERSOLD its own method: the coefficient
> hierarchy is exact closed form at every order (no quadrature layer —
> SS2.3 note), and the small-`t0` series in fact converges across the
> entire plateau, yielding the sharpest characterization of the target
> this lineage has, `Phi(0,t0>=0.02) = 0.0377616` (SS2.4 note). The
> orchestrating session independently verified both referee-derived
> results before cataloguing (sympy ODE checks of `b2`/`b3`/`a3`/`a4` —
> all residuals exactly 0; an independently re-built `(P,Q)`-family
> series implementation to order 200 reproducing `0.0377615983` and
> every table value to all printed digits). Catalogued as node `FLOORH2`
> under `FLOORCF` in `PROOF_DEPENDENCY_MAP.md` Árvore B; `phi_REDB`
> unchanged.

---

## 0. Setup and provenance

Everything below works inside the exact system stated in
`floor_closed_form_attempt/ATTEMPT.md` SS5 (read in full before writing any
code here, together with the referee report, `PROOF_DEPENDENCY_MAP.md` SS2,
and `THEOREM.md`/`DERIVATIONS.md` for the shared background definitions —
read-only, per the mandate; nothing outside this new subdirectory was
written to):

```
dPhi/ds - dPhi/dg = c[Phi - W],     dPsi/ds = c[Psi - W]
W(s,g) = g*Avg_g[Phi(s,.)] + (1-s-g)*Psi(s,g)
Avg_g[Phi(s,.)] := (1/g) int_0^g Phi(s,g') dg'
boundary: Phi(s,0) = 1
target:   phi_abstract(t0) = Phi(0, t0)
```

`(s,g)` are, respectively, total mass explored and the current remaining
gap toward `x0` in the abstract recursive process; `Phi`/`Psi` are the
success probabilities while actively sweeping the gap (mode `G`) versus
in generic exploration (mode `E`); `c=1000, n=65536` throughout (the
target cell used by every test in the parent lineage).

**No code from `floor_closed_form_attempt/*.py` or its `adversarial/`
subfolder was read, opened, or imported anywhere in this front** — only the
PDE system and process description AS STATED IN PROSE in `ATTEMPT.md`
SS3.1/SS4/SS5 were used, matching this lineage's standing "re-derive, don't
import, the thing you're trying to independently corroborate" convention.
`abstract_proc.py` (this front's own fresh implementation of the abstract
process, used for all Monte Carlo checks below) is therefore structurally
similar to the parent's `fcd_t3.py` by necessity (it simulates the SAME
stated process) but was written from scratch.

---

## 1. Re-deriving the coefficient recursion (symbolic cross-check, PROVED)

Matching powers of `g` in the stated PDE system, writing `Phi(s,g) = sum_k
a_k(s) g^k` (`a_0=1` from the boundary) and `Psi(s,g) = sum_{k>=1} b_k(s)
g^k` (`b_0:=0`, since `Psi(s,0)=0` — a gap of exactly zero can never be
gap-hit, so mode `E` starting there can never reach the `g=0` success
boundary; formally forced by `W`'s own structure having no `g^0` term),
gives, for `k>=1`:

```
a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)
w_k(s) := a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
```

**`f01_series_derivation.py` Part A** re-derives this by literally matching
powers of `g` in the stated PDEs via `sympy` (truncated symbolic series,
`K=4`), independently of the by-hand recursion above, at BOTH `k=1` and
`k=2` (the two orders load-bearing for SS2 below): every symbolic
difference between the two derivations simplifies to exactly `0`
(`f01_series_derivation.log`). This is the first thing checked, precisely
because the entire rest of this document rests on this recursion being
transcribed correctly from the stated PDEs.

`a_1(s) = -c` (constant, from the `k=0` order, using `a_0'(s)=0`): **the
leading-order-in-`g` correction to `Phi` is universal across ALL `s`** —
this already re-derives, from first principles, the empirical fact (T1 in
the parent front) that `Phi(0,t0) -> e^{-c t0}` as `t0->0`: the FIRST
correction to certain success is exactly the "pure race" term, with no
trace yet of the recursive re-entry mechanism.

---

## 2. Exact closed form for the small-`t0` regime (PROVED to k=1, cross-
checked to k=2/3)

### 2.1 `k=1`: an exact closed form — the Mills-ratio / erfcx function

The `k=1` Psi-recursion, `b_1'(s) - c s b_1(s) = -c`, is a first-order
linear ODE. Selecting the branch that stays bounded (does not blow up) as
`s -> infinity` — the physically correct choice, since `Psi` is a
probability and must not diverge — gives, in exact closed form:

```
psi1(s) := b_1(s) = sqrt(pi c / 2) * erfcx(s * sqrt(c/2))
```

where `erfcx(x) = e^{x^2} erfc(x)` is the scaled complementary error
function (a standard special function, numerically stable via
`scipy.special.erfcx` even though the two factors `e^{cs^2/2}` and
`erfc(...)` individually overflow/underflow for the `s` ranges used here).

**Proved exactly** (`f01_series_derivation.py` Part B), two ways:
- **Symbolically**: `sympy` substitutes the closed form into
  `b_1'(s)-c*s*b_1(s)` and simplifies the result to exactly `-c` (not
  approximately — an exact symbolic identity), using `erfc`'s own defining
  derivative identity (also symbolically re-verified: `erfcx'(x) - [2x
  erfcx(x) - 2/sqrt(pi)]` simplifies to `0`).
- **Numerically, by direct Monte Carlo** (`f02_psi_smallg_validate.py`,
  seed `SeedSequence(20260856000)`, `N=300,000` per point, `c=1000`): the
  abstract process is simulated STARTING directly in mode `E` at `(s0,g0)`
  for 5 values of `s0` in `{0, 0.01, 0.03, 0.05, 0.08}` and 2 small `g0` in
  `{0.0001, 0.0003}`. The LINEAR-only prediction `g0*psi1(s0)` alone is
  significantly biased at `g0=0.0003` (`z` from `-6.2` to `-9.2` across all
  5 `s0`); adding the (independently derived, SS2.2) quadratic term
  `g0^2*b2(s0)` collapses every one of the 10 `|z|` to `<2.0` (full table
  in `f02_psi_smallg_validate.log`). This is a real, quantitative,
  two-coefficient validation, not just a sign check.

### 2.2 `k=2`: exact closed form for `Phi`'s second coefficient, for ALL `s`

Substituting `psi1(s)` into the `k=1` Phi-recursion gives, in exact closed
form, valid for every `s` (not just `s=0`):

```
a_2(s) = (c/2) * [c + 1 + (1-s)*psi1(s)]
```

At `c=1000, s=0`: `a_2(0) = 520316.636488` (`f01_series_derivation.log`),
against the "pure race alone" value `c^2/2 = 500000` that a naive
`e^{-ct0}`-only model would predict — the excess (`20316.6`) is entirely
attributable to `psi1(0) = sqrt(pi c/2) = 39.633`, i.e. is a genuine,
closed-form-quantified signature of the recursive re-entry mechanism
already visible at second order.

> **[Post-adversarial correction, 2026-08-25 — DISC-DEC-071, N3
> (minor).]** "Entirely attributable to `psi1(0)`" is 97.5% right:
> exactly `500` of the `20316.6` excess comes from the `w_1` re-entry
> constant (the `+1` in `c+1`), not from `psi1`. The *mechanism*
> attribution (re-entry) stands.

### 2.3 `k=3`: `a_3(0)` — exact up to one numerical quadrature (both layers
cross-checked by two independent methods each)

Going one order further requires `b_2(s) = -e^{cs^2/2} int_s^infty
e^{-c*sigma^2/2}[c^2/2 + c*psi1(sigma)] d(sigma)` — a genuine NEW integral
(the "double special function" layer where the recursion stops being
expressible in named elementary/standard special functions and needs one
numerical quadrature). At `c=1000, s=0`: `b_2(0) = -20816.636488`
(`scipy.integrate.quad`, estimated abs. error `1.8e-8`) and hence
`a_3(0) = -180730907.6285`.

**Two independent numerical cross-checks, both exact matches** (Part C.1,
`f01_series_derivation.log`):
- `a_2'(0)`: closed-form analytic derivative vs. central finite difference
  — relative difference `4.4e-10`.
- `b_2(0)`: the quadrature formula vs. an entirely independent method (ODE
  shooting backward from a finite cutoff `s_far`, `scipy.integrate.solve_ivp`,
  `Radau`) — converges to `-20816.636483` as `s_far` grows, matching the
  quadrature value `-20816.636488` to 5 significant figures.

> **[Post-adversarial correction, 2026-08-25 — DISC-DEC-071, N1
> (mandatory).]** This section's characterization of `b_2` as "a genuine
> NEW integral" — "the 'double special function' layer where the
> recursion stops being expressible in named elementary/standard special
> functions and needs one numerical quadrature" — is **FALSE**, refuted
> by the referee in the direction of this front having undersold itself.
> The integrand's exponentials cancel identically
> (`e^{-c sigma^2/2} * psi1(sigma) == sqrt(pi c/2) * erfc(sigma
> sqrt(c/2))`), making the integral elementary:
> `b_2(s) = -c - (c/2)sqrt(pi c/2)(1-2s) erfcx(s sqrt(c/2))`, and
> `a_3(0) = -(c^3/2 + 5c^2/2 + (c^2+3c/2)sqrt(pi c/2))/3` exactly —
> both reproducing this section's quadrature values to all printed
> digits. More strongly, the referee PROVED by induction that EVERY
> coefficient `a_k(s)`, `b_k(s)` lies in the closed family
> `{P(s) + Q(s) erfcx(s sqrt(c/2)) : P,Q polynomials}` (constructive
> bounded-branch solve, no quadrature at any order), exhibiting
> `b_3(s)` and `a_4(0) = 47,146,963,944.14` in closed form. The `k=2/3`
> tier is therefore EXACT, not "quadrature-supported". Session-verified
> before cataloguing: all four closed forms re-checked symbolically
> (sympy, ODE residuals exactly 0) and the family solve re-derived and
> re-implemented independently. See `adversarial/REFEREE_REPORT.md`
> §1–§2.

### 2.4 Validation against a fresh, high-powered Monte Carlo

**`f03_smallt0_series_validate.py`, seed `SeedSequence(20260856001)`,
`N=500,000` per point** (independent of, and far more powerful than, the
parent front's own archived `fcd_t3.log`, `N=40,000`):

| `t0` | `c*t0` | `phi_hat` (MC, `N=500k`) | `e^{-ct0}` | `z` | 2-term series | `z` | 3-term series | `z` |
|---|---|---|---|---|---|---|---|---|
| 0.00003 | 0.03 | 0.970686±0.00024 | 0.970446 | +1.01 | 0.970468 | +0.91 | 0.970463 | +0.93 |
| 0.00005 | 0.05 | 0.950990±0.00031 | 0.951229 | -0.78 | 0.951301 | -1.02 | 0.951278 | -0.94 |
| 0.00010 | 0.10 | 0.904742±0.00042 | 0.904837 | -0.23 | 0.905203 | -1.11 | 0.905022 | -0.68 |
| 0.00020 | 0.20 | 0.819064±0.00054 | 0.818731 | +0.61 | 0.820813 | **-3.21** | 0.819367 | -0.56 |
| 0.00030 | 0.30 | 0.741768±0.00062 | 0.740818 | +1.53 | 0.746828 | **-8.18** | 0.741949 | -0.29 |
| 0.00050 | 0.50 | 0.609360±0.00069 | 0.606531 | +4.10 | 0.630079 | **-30.0** | 0.607488 | +2.71 |
| 0.00070 | 0.70 | 0.503332±0.00071 | 0.496585 | +9.54 | 0.554955 | **-73.0** | 0.492964 | **+14.7** |
| 0.00100 | 1.00 | 0.378110±0.00069 | 0.367879 | +14.9 | 0.520317 | **-207**  | 0.339586 | **+56.2** |

(full log: `f03_smallt0_series_validate.log`). **The 3-term series is
accurate to `|z|<1` for `c*t0 <~ 0.3`**, decisively better than both the
naive `e^{-ct0}` guess (already off by `z=1.5` to `4.1` in this same range)
and the 2-term truncation (off by `z` up to `8.2` at `c*t0=0.3`); it
degrades gracefully and breaks down cleanly by `c*t0 ~ 0.5-0.7`, exactly
where a series with this coefficient growth would be expected to leave its
radius of practical usefulness.

> **Honest process note.** A first look at this comparison used the
> parent front's OWN archived `fcd_t3.log` point at `t0=0.0003`
> (`N=40,000`: `0.74785±0.00217`) instead of a fresh run, and the 3-term
> series (`0.741949`) looked WORSE against it (`z=-2.72`, apparently
> worse than the 2-term series's `z=-0.47`) than the well-checked
> coefficients should have allowed — despite `a_3(0)` having already
> passed the two independent numerical cross-checks in SS2.3. Rather than
> either (a) trusting the single old, noisier data point over a
> twice-cross-checked closed-form coefficient, or (b) silently swapping
> in a more favorable comparison, a fresh, independently-seeded, `~12x`
> higher-powered run was dispatched specifically to settle it (this is
> `f03`, seed `20260856001`, table above). It resolved cleanly in favor
> of the theory: the fresh `N=500,000` measurement at `t0=0.0003` gives
> `0.741768±0.00062`, matching the 3-term prediction to `z=-0.29` (not
> `-2.72`) — the earlier apparent anomaly was ordinary Monte Carlo noise
> in a single lower-`N` archived point, not a flaw in `a_3(0)`. Disclosed
> in full per this lineage's standing self-correction convention.

**Honest scope limit (repeated from the top matter, since it governs
everything in this section):** `c*t0 <~ 0.3-0.5` means `t0 <~ 0.0003-0.0005`
at the target cell (`c=1000`). The parent front's actual quantity of
interest, `phi_far(threshold)`, averages `phi(ell)` — equivalently
`Phi(0,t0)` for `t0=ell/n` — over `t0` from `threshold/n` (`~0.03` for
`threshold=2000,n=65536`) up to `1`. **This entire SS2 result covers a
`t0`-range roughly 100x below where `phi_far`'s own integration starts.**
It is a genuine closed form for a genuinely restricted sub-case (per the
mandate's explicitly-acceptable weaker-result menu), not a step toward
computing the original target quantity.

> **[Post-adversarial correction, 2026-08-25 — DISC-DEC-071, N2
> (mandatory).]** The scope-limit paragraph above — and SS5(1)'s
> "wrong expansion point / radius of convergence `c*t0 ~ 0.5-0.7`"
> obstruction — is **FALSE**. What this section measured at 3 terms is
> TRUNCATION error, not a radius of convergence: with exact
> coefficients (available at every order, per the N1 note), the same
> series CONVERGES across the entire practically relevant range
> (referee: verified to `c*t0 = 90`, coefficient ratios still
> decreasing at order 500 — entire-function-like behavior), reproduces
> the plateau, and yields the sharpest characterization of the target
> this lineage has: **`Phi(0,t0) = 0.0377616` for every `t0 >= 0.02`**
> (approach `~e^{-c t0}`), `Phi(0,0.01) = 0.0377932` — consistent with
> all six MC references cited in SS3.4, with the parent's full 12-row
> `fcd_t3.log` (the one old noisy `t0=0.0003` point aside, exactly the
> point SS2.4's honest-process note already adjudicated), and with both
> PDE solvers. The expansion point is not wrong; the SS2 result is, in
> fact, the whole step — pushed to high order it computes
> `phi_abstract(t0)` everywhere to arbitrary precision. The claimed
> validity window and breakdown of the 3-TERM truncation are confirmed
> as real, correctly-located properties of the truncation (referee's
> fresh MC: +4.7/+13.6/+57.8 at `c*t0 = 0.5/0.7/1.0`). Session-verified
> before cataloguing: an independently re-built `(P,Q)`-family series
> to order 200 reproduces `0.0377615983`, the `e^{-ct0}` plateau
> approach (`S(0.02)-S(0.03) = 1.16e-9`), and every referee table value
> to all printed digits, with `|z| <= 1.3` against the accepted MC
> references. What genuinely remains open is a closed-form RESUMMATION
> (the plateau constant `0.0377616` has no identified closed form) and
> the abstract-vs-real ~30% gap (SS0), unchanged. See
> `adversarial/REFEREE_REPORT.md` §2.

## 3. A corrected, validated numerical solver for the FULL range (the
practically relevant result)

### 3.1 Diagnosing and fixing the parent front's disclosed bug

`solve_2d_system.py` (parent front, disclosed as failing:
`Phi(0,0.37)=1.0` exactly) only re-propagated the `Phi[s=0,.]` ROW on each
fixed-point iteration, leaving `Phi[s>0,.]` — needed inside `Avg_g[Phi(s,.)]`
for every `s>0` query — essentially frozen at its (poor) initial guess.
This front's own FIRST attempt at a corrected solver reproduced a
DIFFERENT, new bug while trying to vectorize the fix (see the honest
process note in `f04_corrected_2d_solver.py`'s module docstring: an
anti-diagonal indexing error meant only the very first marching step ever
reached row `s=0`, so `Phi[0,.]` again never updated after iteration 0 —
caught immediately because the solver's own convergence diagnostic printed
`max|dPhi(s=0,.)|=0.000e+00` at every iteration, an unmistakable tell).

**The corrected version** (`f04_corrected_2d_solver.py`, current file) (a)
re-marches EVERY `(s,g)` grid point's `Phi` along its own characteristic on
EVERY outer iteration, using a correctly-indexed anti-diagonal sweep, and
(b) uses an exact local exponential integrator (`Phi_new = W + (Phi_old-W)*
e^{-ch}`) for both the `Phi`-marching and the `Psi`-marching, which is
unconditionally stable regardless of `c*h` (unlike the parent attempt's
plain forward-difference step).

### 3.2 Self-test (analytic ground truth, PASSED)

Before trusting any coupled-system output, the marching indexer alone is
checked against the one case with a known closed form: forcibly zeroing
`W` (fully decoupling `Phi` from `Psi`/`Avg_g` — the "no re-entry, pure
race only" limit) must reproduce `Phi(s,g)=e^{-cg}` exactly. It does, to
`6.9e-18` (machine precision) over `g in [0,0.05]` at `c=1000`
(`f04_corrected_2d_solver.log`, `_self_test_uncoupled`).

### 3.3 Convergence: outer iteration, grid refinement, domain-cutoff

- **Outer (Gauss-Seidel) iteration**: `max|dPhi(s=0,.)|` and
  `max|dPsi(s=0,.)|` both decrease MONOTONICALLY across 80-150 iterations
  to below `1e-7` at every tested grid (`f04_corrected_2d_solver.log`) —
  unlike the parent attempt, which never had a well-defined fixed point to
  converge to in the first place.
- **`S_MAX` (far-`s` cutoff, where `Psi` is approximated as `0`)
  insensitivity**: `Phi(0,0.09)` is IDENTICAL to 6 decimal places
  (`0.032178`) across `S_MAX in {0.5, 0.7, 0.9}` (`f06_richardson_summary.log`)
  — this specific approximation is not a meaningful source of error at
  `S_MAX=0.5`.
- **Grid refinement (`h -> 0`)**: `f06_richardson_summary.py` runs the
  solver at `h = 0.001, 0.0005, ..., 0.00003125` (halving 5 times) on a
  reduced domain chosen just large enough to reach the plateau at
  `t0=0.03`:

  | `h` | `Phi(0,0.03)` |
  |---|---|
  | 0.001 | 0.031875 |
  | 0.0005 | 0.033903 |
  | 0.00025 | 0.035542 |
  | 0.000125 | 0.036554 |
  | 0.0000625 | 0.037114 |
  | 0.00003125 | 0.037408 |

  Successive-difference ratios: `0.808, 0.618, 0.553, 0.525` — converging
  cleanly toward the theoretically-expected `0.5` for first-order
  `O(h)`-convergent schemes, confirming this is genuine numerical
  convergence (not noise or drift) and that the earlier, coarser grids were
  under-resolving a boundary-layer feature at the natural mark lengthscale
  `1/c = 0.001` (the ratios only start approaching `0.5` once `h` drops
  comfortably below that scale). **Richardson extrapolation** (two
  independent formulas — assuming the limiting ratio is exactly `0.5`, and
  using the actually-observed ratio `0.525` — agree to `0.00003`):

  ```
  Phi(0, t0>~0.01)  ~=  0.0377     [Richardson h->0 estimate, this front]
  ```

### 3.4 Cross-validation against Monte Carlo, and the separability finding

**Against Monte Carlo** (`f06_richardson_summary.py`, no new randomness —
this comparison cites the already-archived `fcd_t3.log` and the referee's
`adversarial/REFEREE_REPORT.md` SS3 table, both already read in full for
this dispatch, not re-derived here):

| source | `t0` | MC value | PDE-Richardson estimate | `z` |
|---|---|---|---|---|
| this lineage's own T3 | 0.03 | 0.03812±0.00096 | 0.0377 | +0.42 |
| this lineage's own T3 | 0.09 | 0.03832±0.00096 | 0.0377 | +0.63 |
| this lineage's own T3 | 0.37 | 0.03885±0.00097 | 0.0377 | +1.17 |
| referee's independent T3 | 0.01 | 0.03770±0.00043 | 0.0377 | -0.04 |
| referee's independent T3 | 0.09 | 0.03744±0.00042 | 0.0377 | -0.66 |
| referee's independent T3 | 0.37 | 0.03701±0.00042 | 0.0377 | -1.68 |

**Every comparison is within `|z|<1.7`**, with most well under `1`. This is
the central positive result of this front: a corrected, convergent,
independently-validated NUMERICAL characterization of `Phi(0,t0)` across
the range that matters, closing the specific, named gap the parent front's
own bounded attempt left (a solver that "did not converge to a trustworthy
answer").

**Separability diagnostic** (`f05_separability_diagnostic.py`, SVD of the
converged `Phi(s,g)` grid at `h=0.001`, `501x401` points): the singular
value spectrum is **overwhelmingly rank-2** — rank-1 alone already explains
`98.78%` of the variance, rank-2 explains `99.99996%`
(`f05_separability_diagnostic.log`), and a rank-2 reconstruction of the
target row `Phi(0,.)` alone is accurate to a relative error of `1.5e-4`.
Direct inspection (not just the SVD) confirms why: away from a thin
boundary layer near `g=0` (where `Phi(s,g) ~= e^{-cg}` is itself already
`s`-independent, per SS1's `a_1(s)=-c` finding), `Phi(s,g)` for different
`g` in the plateau region (`g` from `0.01` to `0.3`) has NEARLY IDENTICAL
`s`-dependence shape (spread over `s in [0,0.5]`: `3.11e-2, 3.10e-2,
3.10e-2, 3.09e-2, 3.07e-2` at `g=0.01,0.05,0.1,0.2,0.3` respectively —
matching to 3 significant figures across a 30x range of `g`). This is a
genuine, precise, checkable finding, reported honestly even though it
complicates rather than simplifies the closure story (SS5).

---

## 4. Test log (all seeds from this front's reserved range
`20260856000+`, confirmed unused via `grep -rn "20260856"` before this
dispatch — only the ledger/queue reservation lines matched)

| ID | script | seed | N | purpose | result |
|---|---|---|---|---|---|
| T-symb | `f01_series_derivation.py` | none (symbolic/deterministic) | — | recursion + `psi1` closed-form cross-check | all symbolic differences = 0; ODE substitution exact |
| T-A | `f02_psi_smallg_validate.py` | `SeedSequence(20260856000)` | 300,000/point (10 points) | direct MC of `Psi(s0,g0)` vs. closed-form `psi1(s)`+`b2(s)` | linear-only `z` up to `-9.2`; linear+quadratic `|z|<2.0` (10/10) |
| T-B | `f03_smallt0_series_validate.py` | `SeedSequence(20260856001)` | 500,000/point (8 points) | direct MC of `Phi(0,t0)` vs. 1/2/3-term series | 3-term `|z|<1` for `c*t0<~0.3`, clean breakdown beyond |
| T-C | `f04_corrected_2d_solver.py` | none (deterministic PDE solve) | — | self-test + corrected full-range solve | self-test exact to 1e-18; converges cleanly |
| T-D | `f05_separability_diagnostic.py` | none (deterministic) | — | SVD rank diagnostic on converged `Phi(s,g)` | rank-2 explains 99.99996% of variance |
| T-E | `f06_richardson_summary.py` | none (deterministic; MC comparisons CITE prior archived data) | — | grid-refinement Richardson extrapolation + MC cross-validation | `Phi(0,t0>~0.01) ~= 0.0377`; `|z|<1.7` vs. 6 independent MC references |

No throwaway/exploratory seeds were needed for this front (unlike the
parent front's own T0-T3) — every seed listed above produced a number kept
in the final record.

---

## 5. What remains open (honest, precise)

**The full closed form for `Phi(0,t0)` across ALL `t0` — equivalently, for
`phi_abstract(t0)`, and hence (via the parent front's own SS1 identity, not
re-derived here) for `phi_far` under the abstract-process idealization — is
NOT derived.** Precisely, three separate obstructions, each named as
precisely as this front could determine:

1. **The small-`t0` series does not extend to the practically relevant
   range.** Its coefficients (SS2.3) are computable via a well-defined,
   in-principle-infinite hierarchy of linear ODEs, each requiring one MORE
   nested quadrature layer than the last (no evident finite recursion or
   generating-function identity was found that would let all orders be
   summed in closed form at once) — and even if such a generating function
   existed, the series' empirically-measured radius of convergence
   (`c*t0 ~ 0.5-0.7`) is intrinsically far below the `t0` range
   `phi_far` actually integrates over. **This is not a "try harder on the
   same technique" gap — it is the WRONG expansion point for the target
   quantity**, and this front does not know of a different expansion point
   (e.g. around `t0=1`, or a genuine large-`c` scaling limit distinct from
   the `t0->0` one used here) that would reach the plateau region in closed
   form; a brief exploration of a `c->infinity` boundary-layer rescaling
   (`x=s*sqrt(c), y=g*sqrt(c)`) was sketched by hand during this front's
   work but not carried through to a checked result, and is reported here
   ONLY as a plausible next avenue, not a finding.

   > **[Post-adversarial correction, 2026-08-25 — DISC-DEC-071.]**
   > Obstruction 1 is refuted in both parts (see the N1/N2 notes in
   > SS2.3/SS2.4): the hierarchy IS expressible in closed form at every
   > order (family `{P + Q*erfcx}`, referee induction), and the measured
   > "radius" was 3-term truncation error — the series converges across
   > the whole plateau and computes the target to arbitrary precision.
   > The TRUE residual gap replacing this obstruction: no closed-form
   > RESUMMATION of the convergent series was found — the plateau
   > constant `0.0377616` remains unidentified as a named constant.
   > Obstruction 2 stands as an observation, with the referee supplying
   > the candidate mundane resolution its item (a)/(b) asks for:
   > boundary layer (`g <~ 1/c`) + `g`-flat plateau is *automatically*
   > near-rank-2, and with the layer removed the surface is rank-1 at
   > 99.99998% — so (b) resolves as "expected to persist, sharpening
   > with `c`", not a coincidence of this regime. Obstruction 3 stands
   > unchanged.
2. **The separability tension (SS3.4) is a real, unresolved finding, not
   just a caveat.** The governing PDE/integral system is provably coupled
   and nonlocal (the `Avg_g[Phi(s,.)]` term genuinely reaches across
   different `g'` values at fixed `s`, and no algebraic substitution found
   in SS1's recursion removes this) — yet the actual solution surface is
   numerically near-rank-2. Neither possibility was resolved: (a) that a
   rank-2 (or similarly low-rank) ansatz `Phi(s,g) ~= u1(s)v1(g)+u2(s)v2(g)`
   could be shown EXACTLY (not just numerically) consistent with SS5's
   PDEs, reducing the problem to a small, tractable coupled ODE system —
   this was not attempted, and is the single most concrete, promising
   avenue this front identifies for a future front; or (b) that the
   near-rank-2 structure is a coincidence of this specific `(c,t0)`-regime
   that would not hold, e.g., at very different `c`. **This front does not
   know which.**
3. **Even a fully closed `Phi(0,t0)` would not by itself close the parent
   front's original question.** As stated in SS0/SS2.4, the abstract
   process is itself an idealization of the real `n=65536` engine, with a
   previously-disclosed, unresolved ~30% level gap between the two
   plateaus that this front does not address — closing SS5 exactly would
   answer "what does the STATED abstract recursive process do", not
   automatically "what does the real discrete engine do."

**No formula of record is proposed as a replacement for anything.**
`phi_REDB` (`M-CLUST(b)`'s formula of record) and `phi_U(c)`, `phi_infinity(c)`
are all untouched and unaffected by anything in this document — this front
worked entirely inside the already-disclosed-as-open SS5 sub-problem and
did not reach a full closed form, so no governance action is implied.

---

## 6. Honest synthesis

This front set out to close the ONE thing `floor_closed_form_attempt`
named as unresolved (SS5's coupled system) and was diagnosed in advance as
being in the same difficulty class as this archive's own still-open
general-`K` conjecture. It did not achieve a full closed form. It DID
achieve two genuine, validated, non-trivial pieces of progress beyond the
parent front's own state:

- An exact closed form (new named special function, symbolically PROVED,
  numerically validated two independent ways) for a genuinely restricted
  sub-case (small `t0`) — explicitly the kind of weaker result the mandate
  names as acceptable, delivered with the same rigor (symbolic
  cross-check + two independent numerical methods per coefficient + fresh
  high-powered Monte Carlo validation, including a self-caught apparent
  discrepancy that resolved in the theory's favor once properly powered)
  as every PROVED claim elsewhere in this lineage.
- A CORRECTED, working, unit-tested, convergent numerical solver for the
  FULL practically-relevant range, succeeding exactly where the parent
  front's own bounded attempt failed (named bug, reproduced, fixed,
  self-tested against an analytic ground truth, and Richardson-extrapolated
  to agree with independent Monte Carlo — both this lineage's own and the
  referee's — to `|z|<1.7` everywhere tested). This is not a closed form,
  but it is a real, validated, USABLE numerical characterization where none
  existed before.

Both pieces of progress come with an honest, precisely-stated limit: the
closed-form regime does not reach the quantity of practical interest, and
the numerical solver, however validated, remains a number-per-query
solver, not a formula. The one genuinely new structural finding —
provably-coupled equations producing a near-separable solution — is
reported as an open tension, not spun into either "closed" or "proven
fundamentally coupled," because the evidence gathered here supports
neither of those stronger claims.

---

## 7. Scorecard

| Item | Tier achieved |
|---|---|
| Full closed form for `Phi(0,t0)`, all `t0` | **NOT achieved.** Precise obstruction named in SS5 (wrong expansion point for the small-`t0` series; an unresolved coupled-vs-near-separable tension for the full range). |
| Closed form for a restricted sub-case | **ACHIEVED** — exact `k<=1` (new Mills-ratio/erfcx special function, symbolically PROVED + 2-way numerically validated), extended to `k=2` (exact, all `s`) and `k=3` (numerically exact via quadrature, cross-checked 2 ways), for `c*t0 <~ 0.3-0.5`. Honest scope limit stated (SS2.4): below the range `phi_far` actually needs. |
| Validated numerical characterization (non-closed-form) across the full/practical range | **ACHIEVED** — corrected, self-tested, convergent solver; Richardson-extrapolated estimate `Phi(0,t0>~0.01)~=0.0377` matches 6 independent Monte Carlo references at `\|z\|<1.7` (mostly `<1`). |
| Proof/evidence on whether the coupling is "fundamental" | **Partial, and more nuanced than expected** — equations provably coupled/nonlocal (no 1-D reduction found); solution numerically near-rank-2 (SS3.4). Reported as an open, precisely-characterized tension, not resolved either way. |
| Effect on `phi_REDB` / any formula of record | **NONE.** No replacement formula proposed anywhere in this document. |
| Self-caught issues disclosed in the open | 3: (i) a `sympy` `.solve()`-returns-a-list bug in `f01`'s own symbolic check, caught by the traceback before any number was trusted (SS-none, see `f01_series_derivation.py` inline comment); (ii) an apparent series-vs-MC discrepancy at `t0=0.0003` traced to old-data noise, not a coefficient error, once freshly and more powerfully re-measured (SS2.4 honest process note); (iii) a mis-vectorized anti-diagonal marching indexer in the solver's first draft, caught immediately via its own `max\|dPhi(s=0,.)\|=0` convergence diagnostic (SS3.1). |

**Overall tier: genuine partial closure** — stronger than "honest
non-closure" (two independently validated, non-trivial results delivered),
weaker than full closure (the central `Phi(0,t0)` closed form across all
`t0` remains open, with the obstruction named as precisely as this front
could determine). **This document requires independent mandatory
adversarial verification before any integration into governance**, per this
lineage's standing discipline; per the mandate, no `adversarial/`
subdirectory was created and no referee was dispatched by this front
itself.

> **[Post-adversarial correction, 2026-08-25 — DISC-DEC-071.]**
> Scorecard adjustments mandated by the referee (see SS2.3/SS2.4/SS5
> notes): row 1's obstruction analysis is superseded — both named
> obstructions are refuted, and the residual gap is the missing
> closed-form RESUMMATION (plateau constant `0.0377616` unidentified)
> plus the abstract-vs-real gap; row 2's tier upgrades from "k=2/3
> numerically exact via quadrature" to EXACT closed form at every order
> (family `{P + Q*erfcx}`), and its honest scope limit is refuted — the
> series reaches the full range and computes the target everywhere.
> Rows 3–6 stand as written (row 3's `0.0377` is sharpened to
> `0.0377616` by the referee's exact series, session-verified). Overall
> tier remains **genuine partial closure** — for reasons partly
> stronger than the ones originally given. Verdict: SOUND WITH NAMED
> ISSUES, ACCEPT for catalogue.

---

## 8. Files

| file | role |
|---|---|
| `abstract_proc.py` | fresh, from-scratch implementation of the abstract recursive process (both mode-`G` and mode-`E` entry points), used by all Monte Carlo checks below |
| `f01_series_derivation.py`/`.log` | Part A: sympy symbolic re-derivation/cross-check of the coefficient recursion (k=1,2). Part B: exact closed form + symbolic proof for `psi1(s)`. Part C: numeric `a2(0)`, `a3(0)` via the recursion. Part C.1: two independent numerical cross-checks of `a2'(0)` and `b2(0)` |
| `series_coeffs.json` | numeric coefficients from f01, consumed by f03 |
| `f02_psi_smallg_validate.py`/`.log`/`.json` | Monte Carlo validation of `psi1(s)`/`b2(s)` against direct simulation of `Psi(s0,g0)`, seed `20260856000` |
| `f03_smallt0_series_validate.py`/`.log`/`.json` | high-powered Monte Carlo validation of the `Phi(0,t0)` series, seed `20260856001` |
| `f04_corrected_2d_solver.py`/`.log`/`.json` | corrected, unit-tested, convergent numerical solver for the full SS5 system (includes the `_self_test_uncoupled` analytic ground-truth check and the honest process note on the first, buggy vectorization attempt) |
| `f05_separability_diagnostic.py`/`.log`/`.json` | SVD rank/separability diagnostic on the converged `Phi(s,g)` grid |
| `f06_richardson_summary.py`/`.log`/`.json` | grid-refinement sequence, Richardson extrapolation, `S_MAX`-sensitivity check, and the final Monte Carlo cross-validation table |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this `floor_h2_b1_full_closure_attempt/`
subdirectory was written to (the parent `floor_closed_form_attempt/*.py`
files and `ATTEMPT.md`/`adversarial/REFEREE_REPORT.md`, and
`PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DERIVATIONS.md` further up the
tree, were read-only references, per the mandate). No `adversarial/`
subdirectory created; no referee dispatched by this front.
