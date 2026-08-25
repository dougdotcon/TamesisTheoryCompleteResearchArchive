# REFEREE REPORT — adversarial review of `floor_h2_b1_full_closure_attempt/ATTEMPT.md`

**Wave 16, front (d) `FLOOR-H2-B1-FULL-CLOSURE-ATTEMPT`, mandatory
independent adversarial verification.**

Object under test: `floor_h2_b1_full_closure_attempt/ATTEMPT.md` (the
wave-16 attempt at the full closed form of the b=1 floor's coupled
two-variable `(Phi, Psi)` system, claiming PARTIAL closure). Read in full
before any code was written, together with the parent
`floor_closed_form_attempt/ATTEMPT.md` (accepted, `DISC-DEC-057/062`), the
parent's `adversarial/REFEREE_REPORT.md`, and the parent's archived
`fcd_t3.log` (accepted MC reference data that the front's SS3.4 table
cites).

**Independence / discipline.** None of the front's own scripts
(`abstract_proc.py`, `f01`–`f06`) — and none of the parent front's scripts
— were read, opened, or imported at any point in this review. Everything
below was rebuilt from the prose of record: the PDE system and process
description as stated in the parent's SS3.1/SS4/SS5 and restated in the
front's SS0, plus the parent referee's independently-validated process
reading (accepted input). `git status --porcelain` at review end shows
EXACTLY ONE path: this new untracked `adversarial/` subdirectory — no
tracked file anywhere in the repository is modified. (Transient tracked
modifications observed mid-review belonged to other, concurrent wave-16
fronts and were committed by their own sessions before review end;
checked while present: zero mentions of this lineage or of `phi_REDB` in
those diffs.) **No git commit was made.**

**Fresh seeds**, all from `SeedSequence(20260857000)`–`(20260857002)`, the
range `DECISION_LEDGER.yaml` reserves for this front's referee — confirmed
before use via `grep -rn "20260857"` over `05_DISCOVERY_LAB/` (only the
ledger's and `TEST_QUEUE.yaml`'s reservation lines matched):

| seed | use | N | script | log |
|---|---|---|---|---|
| `SeedSequence(20260857000)` | R-A: fresh MC of `Phi(0,t0)`, small-`t0` series window + breakdown | 500,000 per point (8 points) | `ref_a03_mc_smallt0.py` | `ref_a03_mc_smallt0.log` |
| `SeedSequence(20260857001)` | R-B: fresh MC of `Psi(s0,g0)` vs closed-form `psi1`/`b2`/`b3` | 300,000 per point (10 points) | `ref_a04_mc_psi.py` | `ref_a04_mc_psi.log` |
| `SeedSequence(20260857002)` | R-C: fresh high-power MC of the plateau (`t0=0.01..0.37`) | 1,000,000 per point (4 points) | `ref_a07_mc_plateau.py` | `ref_a07_mc_plateau.log` |

Deterministic (seedless) referee artifacts: `ref_a01_symbolic.py`
(independent sympy re-derivation), `ref_a02_series_extend.py` (exact
coefficient hierarchy to order 500), `ref_a05_pde_solver.py` (independent
PDE solver, different discretization family), `ref_a06_svd.py`
(separability diagnostics). MC powers: R-A matches the front's own
`N=500k`; R-B matches its `N=300k`; R-C (`N=1M`) is 5× the strongest MC
reference the front cites (the parent referee's `N=200k` T3) and 25× the
parent's own T3.

---

## 0. VERDICT — **SOUND WITH NAMED ISSUES**. **ACCEPT for catalogue**, with two mandatory corrections.

Judged at its claimed tier (partial closure), the front's every POSITIVE
claim independently replicates, from scratch, at equal-or-higher power,
with fresh seeds:

- the coefficient recursion, `psi1` closed form, `a2(0)`, `b2(0)`,
  `a3(0)` — all exactly reproduced by an independent symbolic derivation
  (§1);
- the claimed small-`t0` validity window AND the claimed breakdown
  boundary — both replicate in a fresh MC (§3);
- the corrected-solver claim `Phi(0, t0>~0.01) ~= 0.0377` — reproduced by
  an independent PDE solver of a different discretization family, by a
  fresh 1M-walker MC, and (decisively) by an exact high-order series (§2,
  §4);
- the SVD near-separability observation — replicates on this review's own
  solver output (§5);
- `phi_REDB` and every formula of record — genuinely untouched (§6);
- all three self-disclosed bugs — none survives into any final claim (§6).

**However, the review REFUTES the front's two central NEGATIVE
(limits-of-scope) claims** — refutes them in the direction of the front
having *undersold its own method*:

1. **(MAJOR, named issue N1)** SS2.3/SS5(1)'s claim that the coefficient
   hierarchy "stops being expressible in named elementary/standard special
   functions and needs one numerical quadrature [layer per order]" is
   **false**: every `a_k(s)`, `b_k(s)` lies in the closed family
   `P(s) + Q(s)*erfcx(s*sqrt(c/2))` (`P,Q` polynomials), proved by an
   explicit induction and verified symbolically to `k=4` and numerically
   to `k=500` (§1–§2). In particular `b2`, claimed to need quadrature, is
   simply `b2(s) = -c - (c/2)sqrt(pi c/2)(1-2s) erfcx(s sqrt(c/2))`, and
   `a3(0) = -(c^3/2 + 5c^2/2 + (c^2+3c/2)sqrt(pi c/2))/3` exactly.
2. **(MAJOR, named issue N2)** SS2.4/SS5(1)'s scope-limit claim — that the
   small-`t0` series is "the WRONG expansion point", has an
   "empirically-measured radius of convergence `c*t0 ~ 0.5-0.7`", and
   "covers a `t0`-range roughly 100x below where `phi_far`'s own
   integration starts ... not a step toward computing the original target
   quantity" — is **false**. What the front measured at 3 terms is
   TRUNCATION error, not a radius of convergence. Summed with exact
   coefficients, the same series CONVERGES across the entire practically
   relevant range (verified to `c*t0 = 90`, with coefficient ratios still
   falling at order 500 — entire-function-like behavior), reproduces the
   plateau, and yields the sharpest characterization of the target this
   lineage has: `Phi(0,t0) = 0.03776160` for every `t0 >= 0.02` (approach
   `~e^{-c t0}`), `Phi(0,0.01) = 0.03779315` — consistent with all six of
   the front's cited MC references, with the parent's full 12-point
   `fcd_t3.log` (one already-adjudicated noisy point aside, §2), with
   this review's fresh MCs, and with both PDE solvers (§2, §4).

Because N1/N2 are claims about what was NOT achieved, their refutation
*strengthens* the record's mathematics while contradicting the document's
own obstruction analysis and parts of its SS7 scorecard. The right
governance outcome is ACCEPT with mandatory corrections to
SS2.3/SS2.4/SS5(1)/SS7 (specified in §7), not a rejection: nothing the
front asserts as ESTABLISHED is wrong, its honesty discipline held
everywhere it made positive claims, and the two refuted statements are
hedged in places ("no evident ... was found") though flatly asserted in
others ("it is the WRONG expansion point"). An accepted catalogue entry
must not leave those flat assertions standing, since this review
demonstrates they are not merely unproven but false.

---

## 1. Independent symbolic re-derivation (`ref_a01_symbolic.py`, deterministic)

Working only from the stated PDEs, powers of `g` were matched by sympy
independently of the front's by-hand recursion (my own extraction of the
order-`g^k` equations, then a symbolic comparison against the SS1
recursion as transcribed from the front's prose):

- **Recursion**: at every order checked (`a`-side `k=0..3`, `Psi`-side
  `k=1..3`), the difference between my derived relations and the front's
  stated `a_{k+1} = [a_k' - c a_k + c w_k]/(k+1)`,
  `b_k' - c s b_k = -c a_{k-1}/k + c b_{k-1}`,
  `w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}` simplifies to exactly 0.
  **SS1 CONFIRMED** (including `a_1 = -c` and the `b_0 = 0` boundary
  reasoning — the `g=0` Psi ODE forces `Psi(s,0) = Psi(0,0)e^{c s^2/2}`,
  and boundedness forces 0).
- **`psi1`**: `sqrt(pi c/2)*erfcx(s*sqrt(c/2))` satisfies
  `b1' - c s b1 = -c` exactly (symbolic identity) and `-> 0` as
  `s -> oo` (bounded branch). `psi1(0) = 39.6332729761`, `a2(0) =
  520316.636488` — **both match the front to all printed digits**.
  (Branch-selection caveat, minor: the physically exact domain ends at
  `s = 1-g`, not `s = oo`; the difference is a homogeneous term of
  relative weight `~e^{-c/2} ~ 1e-218` at the target cell — negligible,
  and the front's choice is validated by MC anyway. Not an issue.)
- **REFEREE FINDING (basis of N1)**: the front's `b2` integral is
  elementary. The integrand it calls "a genuine NEW integral" contains
  `e^{-c sigma^2/2} * psi1(sigma)`, which is *identically*
  `sqrt(pi c/2) * erfc(sigma sqrt(c/2))` — the exponentials cancel — and
  `int erfc` is closed-form. Hence
  `b2(s) = -c - (c/2)sqrt(pi c/2)(1-2s)erfcx(s sqrt(c/2))`, verified (i)
  symbolically against its ODE, (ii) numerically against the front's own
  integral representation at `s = 0, 0.01, 0.03, 0.05, 0.08` (agreement
  ~1e-16), reproducing the front's quadrature value `b2(0) =
  -20816.636488` exactly; and `a3(0)` follows in exact closed form,
  `-180730907.6285`, matching the front's quadrature-supported value.
- **Induction (all orders)**: the family
  `F = {P(s) + Q(s) erfcx(s sqrt(c/2)) : P,Q polynomials}` is closed
  under every operation the recursion uses: `d/ds` (since `erfcx' =
  c s erfcx - sqrt(2c/pi)` inside `F`), polynomial multiplication, and
  the bounded-branch solve of `b' - c s b = A + B erfcx` (solved
  constructively inside `F` by undetermined coefficients — unique, no
  quadrature). Demonstrated concretely:
  `b3(s) = c^2(8-7s)/12 + sqrt(2 pi) c^{3/2} (7cs^2-8cs+2c+7)/24 *
  erfcx(s sqrt(c/2))` (verified against its ODE symbolically and against
  an independent quadrature at `1.3e-16` relative), and `a4(0) =
  47,146,963,944.14` in closed form. **Every coefficient of the SS2
  hierarchy is exact closed form; no "quadrature layer" ever appears.**

## 2. The decisive check: exact coefficients to order 500 (`ref_a02_series_extend.py`)

Implementing the recursion inside the family `F` (mpmath, 300 digits,
polynomial pairs; validated against §1's sympy values at `k = 2,3,4` to
1e-10 relative and against the front's three claimed coefficient values):

- **Coefficient growth**: `|a_{k+1}(0)/a_k(0)|` = 520, 347, 261, 209
  ... 11.5 (k=100) ... 6.1 (k=200) ... 2.8 (k=500) — monotonically
  DECREASING through order 500, the signature of an entire-function-like
  series (a finite radius of convergence would force the ratios to level
  off at `1/R`; they don't). At the very least the empirical radius
  exceeds `~1/2.8 = 0.35`, i.e. `c*t0 > 350` — some three orders of
  magnitude beyond the front's claimed "radius" of `c*t0 ~ 0.5-0.7`.
- **Summation across the claimed-unreachable range** (partial sums
  `S_K`, exact coefficients):

  | `t0` | `c*t0` | `S_500` | converged by | reference (accepted MC) | `z` |
  |---|---|---|---|---|---|
  | 0.0003 | 0.3 | 0.74230791 | K~10 | parent log 0.74785±0.00217 (N=40k) | +2.55 |
  | 0.001 | 1 | 0.37837102 | K~20 | parent log 0.37585±0.00242 | −1.04 |
  | 0.003 | 3 | 0.08062020 | K~30 | parent log 0.08240±0.00137 | +1.30 |
  | 0.01 | 10 | 0.03779315 | K~50 | parent referee 0.03770±0.00043 | −0.22 |
  | 0.03 | 30 | 0.03776160 | K~150 | parent log 0.03812±0.00096 | +0.37 |
  | 0.05 | 50 | 0.03776160 | K~250 | parent log 0.03667±0.00094 | −1.16 |
  | 0.09 | 90 | 0.03776160 | K~400 | parent referee 0.03744±0.00042 | −0.77 |

  ALL 12 rows of the parent's `fcd_t3.log` (t0 from 0.0001 to 0.90) fit
  the exact-series values at `|z| <= 1.30` — except the single old
  `t0=0.0003` point (`+2.55`), which is precisely the point the front's
  SS2.4 honest-process note already re-measured and found high; the
  front's own fresh `N=500k` re-measurement (0.741768±0.00062) sits at
  `z = -0.87` of the exact value, and this review's fresh point (§3) at
  `z = -0.50`.
- **Plateau structure, exact**: `S(t0) - S(0.09)` = 3.16e-5, 1.16e-9,
  4.6e-14, 8.2e-23 at `t0` = 0.01, 0.02, 0.03, 0.05 — the plateau is
  approached like `~e^{-c t0}`, and the plateau constant is
  **`Phi(0, t0) = 0.0377615983` for all `t0 >= 0.02`** (this review's
  sharpest value; the front's Richardson `0.0377` is this to its stated
  precision).
- **What the front actually measured as a "radius"**: the exact 3-term
  truncation error is 3.6e-4 at `c*t0 = 0.3` (0.5–0.6 of the front's MC
  SEM — hence its `|z|<1` window), 2.7e-3 at 0.5, 9.8e-3 at 0.7 — i.e.
  the claimed "clean breakdown at `c*t0 ~ 0.5-0.7`" is a real and
  correctly-located property OF THE 3-TERM TRUNCATION (§3 confirms it by
  fresh MC), but it is not a radius of convergence, and nothing about the
  expansion point is "wrong".

This section — obtained by combining the front's OWN recursion with the
closed form the front's OWN SS2 was one cancellation away from noticing —
is the basis of named issues N1/N2, and simultaneously the strongest
possible confirmation of the front's positive numerics: three
independent routes (exact series | both PDE solvers | four independent
MCs) now agree on `Phi(0,t0)` across the entire range.

## 3. MC replication of the small-`t0` claims (fresh implementation, fresh seeds)

`ref_mc_lib.py` implements the abstract process from the prose spec alone
(state `(s,g)`, mode G/E, `Exp(c)` inter-mark mass increments, kill `s` /
gap `g` with new gap `~Unif(0,g)` / generic else; mode-G success when `g`
closes before the next mark).

**R-A (`ref_a03`, seed 20260857000, N=500k/point) — `Phi(0,t0)` small-`t0`
table, z-scores against each prediction tier:**

| `t0` | `c*t0` | `phat` | `z` vs `e^{-ct0}` | `z` vs 2-term | `z` vs 3-term | `z` vs exact series |
|---|---|---|---|---|---|---|
| 0.00003 | 0.03 | 0.970616 | +0.71 | +0.62 | +0.64 | +0.64 |
| 0.00005 | 0.05 | 0.950756 | −1.55 | −1.78 | −1.71 | −1.71 |
| 0.0001 | 0.10 | 0.904454 | −0.92 | −1.80 | −1.37 | −1.38 |
| 0.0002 | 0.20 | 0.818610 | −0.22 | −4.04 | −1.39 | −1.52 |
| 0.0003 | 0.30 | 0.741998 | +1.91 | −7.81 | +0.08 | −0.50 |
| 0.0005 | 0.50 | 0.610724 | +6.08 | −28.1 | +4.69 | +0.83 |
| 0.0007 | 0.70 | 0.502604 | +8.51 | −74.0 | +13.6 | −0.29 |
| 0.001 | 1.00 | 0.379278 | +16.6 | −206 | +57.8 | +1.32 |

- **Claimed validity window CONFIRMED**: 3-term `|z| <= 1.7` through
  `c*t0 = 0.3` (front claimed `|z|<1` on its own draw; the true 3-term
  bias at the window edge is ~0.6 SEM, so `|z|` slightly above 1 on a
  fresh draw is exactly as expected).
- **Claimed breakdown CONFIRMED and correctly located**: +4.7 / +13.6 /
  +57.8 at `c*t0` = 0.5 / 0.7 / 1.0 (front: +2.71 / +14.7 / +56.2).
- **Exact-series column**: all 8 points `|z| <= 1.71` (chi^2 = 10.3 on 8
  dof) — my MC and the §2 series validate each other; the residual
  misfits of the truncations are truncation error, not process error.
- The `t0=0.0003` adjudication (front's SS2.4 honest-process note): my
  fresh 0.741998±0.00062 agrees with the front's fresh 0.741768 (z_diff ~
  0.3) and with the exact value 0.742308 (z = −0.50); the parent's old
  N=40k point is the outlier (+2.55). **The front's resolution of its
  self-caught discrepancy was correct.**

**R-B (`ref_a04`, seed 20260857001, N=300k/point) — `Psi(s0,g0)`,
mode-E start, 5 values of `s0` x 2 values of `g0`:**

- linear-only prediction `g0*psi1(s0)`: `z` from −4.0 to −9.4 at
  `g0=3e-4` (front claimed −6.2 to −9.2) — same significant bias,
  same sign, same order;
- linear+quadratic (with the REFEREE's closed-form `b2`, not a
  quadrature): all 10 points `|z| <= 2.08` (chi^2 = 11.1 on 10 dof;
  front claimed `|z|<2.0` on its own draw) — **T-A's two-coefficient
  validation CONFIRMED**, and with it the closed forms themselves;
- adding the referee's closed-form `g0^3 b3(s0)` stays consistent
  (`|z| <= 2.13`), as expected at these tiny `g0`.

## 4. The corrected-solver claims (independent PDE solve + fresh plateau MC)

**R-D (`ref_a05_pde_solver.py`, deterministic).** An independent solver
was built from the stated system in a deliberately different
discretization family from the front's described scheme: renewal/integral
form with an exact exponential-weight, linearly-interpolated-`W` step
quadrature (locally third-order), cumulative-trapezoid `Avg_g`, Jacobi
outer iteration (the front describes a piecewise-constant-`W` exponential
integrator with Gauss-Seidel), and cutoff closures whose error carries
weight `e^{-c s^2/2} < 1e-30`. Self-tests, all PASSED: (i) `W==0` forced ⇒ `Phi = e^{-cg}` to machine
precision (max error 1.1e-16); (ii) `Psi(0,h)/h` converges to
`psi1(0) = 39.633` (39.12 at `h=2.5e-5`, gap halving per refinement);
(iii) `Phi(0, 0.002)` converges to the exact series value 0.15850015
(diff +1.7e-4 → +6.9e-7 across the ladder, ratio ~1/4 per halving).

Refinement ladder (`G=0.031`, margin `M=0.30`; Jacobi converged to
`<1e-11` in ~191 iterations at every grid — corroborating the
plausibility of the front's reported clean outer-iteration convergence):

| `h` | `Phi(0,0.01)` | `Phi(0,0.02)` | `Phi(0,0.03)` |
|---|---|---|---|
| 4e-4 | 0.038291 | 0.038260 | 0.038260 |
| 2e-4 | 0.037918 | 0.037886 | 0.037886 |
| 1e-4 | 0.037824 | 0.037793 | 0.037793 |
| 5e-5 | 0.037801 | 0.037769 | 0.037769 |
| 2.5e-5 | 0.037795 | 0.037764 | 0.037764 |

Successive-difference ratios: 0.251, 0.250, 0.250 at every `t0` — clean
SECOND-order convergence (my scheme family; the front's 0.5 ratios are
the correct first-order signature of its own scheme — the two families
disagree at coarse `h`, mine overshooting where theirs undershoots, and
meet in the limit). Richardson (`h->0`):

```
Phi(0,0.01) = 0.037793      [exact series: 0.03779315]
Phi(0,0.02) = 0.037762      [exact series: 0.03776160]
Phi(0,0.03) = 0.037762      [exact series: 0.03776160]
Phi(0,0.09) = 0.037762      [second ladder, G=0.093; exact: 0.03776160]
```

— the independent solver reproduces the exact-series values to all
printed digits, and hence confirms the front's `0.0377` at its stated
precision. Cutoff-margin insensitivity: `Phi(0,0.01)` and `Phi(0,0.03)`
IDENTICAL to 9 decimals across margins `M in {0.20, 0.25, 0.30, 0.35}`
(the analogue of the front's `S_MAX in {0.5,0.7,0.9}` check — its
far-`s`-cutoff-insensitivity claim is confirmed in my family too).

**R-C (`ref_a07`, seed 20260857002, N=1M/point) — fresh plateau MC:**

| `t0` | `phat` | SEM | `z` vs front's 0.0377 | `z` vs exact series |
|---|---|---|---|---|
| 0.01 | 0.037476 | 0.000190 | −1.18 | −1.67 |
| 0.03 | 0.037824 | 0.000191 | +0.65 | +0.33 |
| 0.09 | 0.038118 | 0.000191 | +2.18 | +1.86 |
| 0.37 | 0.037749 | 0.000191 | +0.26 | −0.07 |

chi^2 vs the exact-series values: 6.4 on 4 dof (p ~ 0.17) — consistent;
no point contradicts `0.0377` beyond the resolution the front claimed
(their two-significant-figure Richardson value). The front's SS3.4 table
arithmetic was also independently recomputed: their quoted `z`'s
correspond to comparing against ~0.03772 (their observed-ratio Richardson
variant) and are correct as printed; their grid-table ratios (0.808,
0.617, 0.553, 0.525) and both extrapolations (0.037702 / 0.037733,
agreeing to 3e-5) reproduce exactly from their own printed numbers.
**Claim (2) — the corrected, validated solver and
`Phi(0, t0>~0.01) ~= 0.0377` — is CONFIRMED** (and sharpened by §2 to
0.0377616 with an `e^{-ct0}` approach; the front's two Richardson
variants, 0.037702/0.037733, sit only 0.08–0.16% under the sharp value —
consistent with an honest extrapolation of a first-order scheme, and
right at the two-significant-figure precision the front actually
claimed).

## 5. The SVD near-separability finding (`ref_a06_svd.py`)

On this review's OWN solver output (a different discretization family
from the front's — an important artifact check), three grids were
SVD-analyzed: the front's f05 region (`s<=0.5 x g<=0.4`) at `h=1e-3`
(matched 501x401 shape) and `h=5e-4`, plus the fine ladder grid
(`h=2.5e-5`, `s<=0.362 x g<=0.031`):

| grid | rank-1 energy | rank-2 energy | rank-2 recon. of `Phi(0,.)`, max rel err |
|---|---|---|---|
| h=1e-3, front's region | 98.27167% | 99.99999982% | 1.64e-4 |
| h=5e-4, same region | 97.81233% | 99.99999980% | 1.45e-4 |
| h=2.5e-5, fine region | 99.72048% | 99.99999960% | 1.26e-4 |

**The front's SS3.4 observation REPLICATES on an independent solver
family** (front: rank-1 98.78%, rank-2 99.99996%, row-reconstruction
1.5e-4 — same structure, same order everywhere; the small quantitative
differences are the two families' different coarse-`h` biases, note both
coarse solutions are ~8% off the continuum in opposite directions:
mine 0.0408, theirs 0.0319, at `h=1e-3`). The near-rank-2 structure is
NOT a numerical artifact of their solver family, and NOT a coarse-grid
artifact (it persists at `h=2.5e-5` on a different region).

Two further diagnostics the front did not run:

- **Removing the `g <~ 1/c` boundary layer** (`g >= 0.01` sub-grid): the
  remaining surface is essentially RANK-1 (rank-1 energy 99.99998%–100%
  on all three grids; `sigma2/sigma1 ~ 2e-4`). The entire second mode is
  the boundary layer.
- **An explicit, no-fit rank-2 ansatz** `e^{-cg} + (1-e^{-cg})F(s)`
  (with `F` read off at the largest grid `g` — zero fitted parameters)
  already captures 99.9946%–99.9977% of the energy.

The front's "direct inspection" claim (near-identical `s`-shape across a
30x range of `g`, spreads matching to ~3 significant figures) also
replicates: my spreads are 3.8672e-2 at `g=0.01` vs 3.8687e-2 at
`g=0.03..0.3` (`h=1e-3` grid; the absolute values differ from the
front's 3.1e-2 for the coarse-`h` bias reason above).

**Assessment.** The observation itself is genuine and solver-independent
(it replicates on a different discretization family). But its "tension"
framing deserves one deflating remark the front did not make: a surface of
the form `Phi ~= e^{-cg}*1 + (1-e^{-cg})*F(s)` — i.e. a `1/c`-thick
boundary layer at `g=0` glued to a `g`-flat plateau profile in `s` — is
*automatically* near-rank-2, and §2's exact solution shows precisely this
structure in the `t0`-direction at `s=0` (plateau approach `~e^{-ct0}`).
The explicit no-fit ansatz above already captures 99.995%–99.998% of the
energy on my grids; the provable coupling lives in the small residual. So
the finding is real but partially mundane; the front reports it neutrally
as "unresolved", which is acceptable — this review simply supplies the
candidate resolution its SS5(2)(a) asks for: the near-rank-2 structure is
a boundary-layer/plateau effect and would NOT be expected to fail at
other `c` (it should sharpen as `c` grows). The document does not spin
the finding beyond "unresolved"; no overclaim found in SS3.4/SS5(2).

## 6. Honesty-framing audit

Tier-by-tier against the SS7 scorecard, in light of §§1–5:

| SS7 row | referee finding |
|---|---|
| Full closed form, all `t0`: NOT achieved | As a statement of what the DOCUMENT contains: accurate. As an obstruction analysis: **both named obstructions are wrong** (N1, N2). What genuinely remains open after this review: a closed-form resummation of the (now exactly-coefficiented, convergent) series into a named function — e.g. the plateau constant 0.0377616 has no identified closed form — and the separately-disclosed abstract-vs-real-engine ~30% gap, which the front correctly scoped out. |
| Restricted sub-case closed form (k<=3, `c*t0 <~ 0.3-0.5`) | CONFIRMED, but UNDERSTATED: the closed form is not restricted to `k<=3` (N1), and its claimed tier "k=2/3 via quadrature" is actually "exact" — values correct, characterization wrong. The "honest scope limit" (100x below `phi_far`) is refuted (N2). |
| Validated numerical characterization, full range | CONFIRMED at claimed tier (my solver, MC, and exact series all agree with 0.0377 at its stated precision). |
| Coupling "fundamental": open tension | Observation CONFIRMED; neutral framing appropriate; candidate mundane resolution supplied here (§5). |
| Effect on `phi_REDB`: NONE | CONFIRMED — no replacement formula is proposed anywhere in the document; `phi_REDB` appears only in "unaffected" statements; no tracked file in this lineage was modified; the concurrent tracked changes elsewhere in the repo contain zero references to this lineage or `phi_REDB`. |
| 3 self-caught bugs disclosed | None survives into final claims: (i) the `f01` sympy bug — not directly inspectable under the no-scripts discipline, but everything `f01` is cited for was re-derived independently here and is correct, so nothing downstream of that bug is wrong; (ii) the `t0=0.0003` apparent anomaly — the front's noise diagnosis is CONFIRMED by exact value + two fresh MCs (§3); (iii) the first-draft solver indexing bug — the fixed solver's outputs are confirmed by two independent routes (§4). |

Also verified: the SS3.4 table's "own T3, t0=0.03/0.09/0.37" rows match
the parent's archived `fcd_t3.log` exactly (the parent ATTEMPT's summary
table shows only 6 of the log's 12 rows, so the citations are to the log,
correctly); the honest-process note's `z=-2.72`, `-0.47`, `-0.29`
arithmetic reproduces; the SS2.4 table's `z` columns reproduce; no
cherry-picking — the log rows the front did NOT cite agree with the
plateau value at least as well as the cited ones.

Minor wording notes (below the named-issue bar): SS2.2 attributes the
`a2(0)` excess over `c^2/2` "entirely" to `psi1(0)`; exactly 500 of the
20316.6 comes from the `w_1` re-entry constant (the `+1` in `c+1`), not
from `psi1` — the *mechanism* attribution (re-entry) is right, the
*function* attribution is 97.5% right. SS3.4's "spread ~3.1e-2" figures
are h=1e-3-resolution artifacts of the correct qualitative claim (the
continuum spread is ~0.0378); the front does not rely on their absolute
values.

## 7. Named issues and mandatory corrections (for the front's authors / governance)

- **N1 (major, SS2.3 + SS5(1) + SS7).** "Needs one numerical quadrature /
  one more nested quadrature layer per order; the recursion stops being
  expressible in named special functions" — FALSE. Correction: state that
  every coefficient lies in `{P + Q*erfcx}` (induction in §1/§2 of this
  report; constructive solve, no quadrature), upgrade the k=2/3 tier from
  "quadrature-supported" to "exact", and delete the "double special
  function layer" obstruction.
- **N2 (major, SS2.4 + SS5(1) + SS7).** "Wrong expansion point;
  empirically-measured radius of convergence `c*t0 ~ 0.5-0.7`; covers a
  range 100x below `phi_far`; not a step toward the target quantity" —
  FALSE. What was measured is 3-term truncation error. The same series,
  summed with exact coefficients, converges through the entire plateau
  (verified to `c*t0=90`; ratio diagnostics to order 500) and yields
  `Phi(0,t0>=0.02) = 0.0377616`, `Phi(0,0.01) = 0.0377932`, agreeing
  with every accepted MC reference and both PDE solvers. Correction:
  replace the obstruction with the true residual gap — no closed-form
  RESUMMATION of the convergent series was found (the plateau constant
  remains unidentified), and the abstract-vs-real-engine gap is still
  untouched.
- **N3 (minor, SS2.2).** The "entirely attributable to `psi1(0)`"
  attribution — 97.5% attributable; the remaining 500 is the `w_1`
  re-entry constant. One-line fix.

None of N1–N3 invalidates a single number the front reports; N1/N2
invalidate its account of WHY it stopped where it did. Under this
lineage's convention (the parent front's referee likewise accepted with a
named synthesis-wording issue), and because the mandate explicitly judges
a partial result at its claimed tier, the correct disposition is the one
in §0.

## 8. Files (this review)

| file | role |
|---|---|
| `ref_a01_symbolic.py`/`.log` | independent sympy re-derivation of the recursion; `psi1` verification; closed forms for `b2`, `a3(0)`, `b3`, `a4(0)`; family-closure induction machinery |
| `ref_series_coeffs.json` | exact low-order coefficient values (consumed by R-A/R-B) |
| `ref_a02_series_extend.py`/`.log`, `ref_a02_series.json` | exact coefficient hierarchy to order 500 (mpmath, 300 digits); convergence/radius diagnostics; series values across the full range |
| `ref_mc_lib.py` | fresh, from-scratch vectorized MC of the abstract process (prose spec only) |
| `ref_a03_mc_smallt0.py`/`.log`, `ref_a03_results.json` | R-A: small-`t0` window + breakdown replication, seed 20260857000 |
| `ref_a04_mc_psi.py`/`.log`, `ref_a04_results.json` | R-B: `Psi` small-`g` closed-form validation, seed 20260857001 |
| `ref_a05_pde_solver.py`/`.log`, `ref_a05_results.json`, `ref_a05_grid_h0.001.npz`, `ref_a05_grid_h0.0005.npz` | R-D: independent PDE solver (different scheme family), refinement ladder, Richardson, cutoff-insensitivity, SVD input grids (the third, 104MB fine-grid `.npz` used by `ref_a06` was deleted after use to keep the archive light — it is deterministically regenerated by re-running `ref_a05_pde_solver.py`) |
| `ref_a06_svd.py`/`.log`, `ref_a06_results.json` | R-E: separability/SVD diagnostics + explicit boundary-layer ansatz assessment |
| `ref_a07_mc_plateau.py`/`.log`, `ref_a07_results.json` | R-C: fresh 1M-walker plateau MC, seed 20260857002 |
| `REFEREE_REPORT.md` | this document |

No file outside `floor_h2_b1_full_closure_attempt/adversarial/` was
written or modified. No git commit made.

---

> **VERDICT: SOUND WITH NAMED ISSUES — ACCEPT for catalogue, with
> mandatory corrections N1/N2 (and optional N3).** Every positive claim
> replicates independently at its claimed tier or above: the k<=3 closed
> forms are exact (indeed more exact than claimed), the claimed validity
> window and breakdown of the 3-term series both reproduce under fresh
> seeds, the corrected solver's `0.0377` is confirmed by an independent
> solver family, fresh 1M-walker MC, and an exact 500-order series
> (sharp value 0.0377616, with the front's Richardson variants sitting
> 0.08–0.16% under it — inside its own implied error), the SVD
> observation replicates and is not
> overclaimed, `phi_REDB` is untouched, and all three self-disclosed
> bugs are genuinely dead. The two major named issues are refuted
> NEGATIVE claims: the front's obstruction analysis (quadrature-layer
> hierarchy; wrong-expansion-point/radius) is demonstrably false, and
> with it the assertion that the SS2 result is "not a step toward
> computing the original target quantity" — it is, in fact, the whole
> step: pushed to high order it computes `phi_abstract(t0)` everywhere
> to arbitrary precision. The document's tier self-assessment ("genuine
> partial closure") therefore survives — but for reasons partly
> different from, and stronger than, the ones it gives, and its "what
> remains open" section must be corrected before integration so that the
> catalogue does not preserve a false obstruction. An honest partial
> closure whose only substantive errors are in underclaiming is still an
> honest partial closure.
