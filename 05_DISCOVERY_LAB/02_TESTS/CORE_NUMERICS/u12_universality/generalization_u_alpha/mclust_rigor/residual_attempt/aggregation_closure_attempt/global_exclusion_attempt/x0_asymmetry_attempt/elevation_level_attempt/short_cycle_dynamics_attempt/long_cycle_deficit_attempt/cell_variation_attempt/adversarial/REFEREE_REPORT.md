# REFEREE REPORT — adversarial review of `cell_variation_attempt/ATTEMPT.md`

**Wave 14, `DISC-DEC-057`, front (e) `CELL-VARIATION-ATTEMPT`, mandatory
independent adversarial verification.**

Object under test: `cell_variation_attempt/ATTEMPT.md` together with its
`DERIVATION_PREREG.md`. Both were read in full, together with the parent
front's own reported open item (`long_cycle_deficit_attempt/ATTEMPT.md` §5,
the target pattern this front investigates), before any line of this
review's own code was written.

**Scope and discipline.** Everything produced by this review lives in
`cell_variation_attempt/adversarial/`. `git status --porcelain` (run at
review end) shows only `cell_variation_attempt/` and an unrelated
sibling-front directory (`conjecture1_k2_attempt/`, untouched by this
review) as untracked — no other path in the repository is modified. **No
git commit was created.**

**Independence.** Per the mandate's explicit permission, `sc_engine.py` and
`sc_formula.py` (`short_cycle_dynamics_attempt/`, three directories up from
this `adversarial/` folder, already adversarially verified SOUND twice
earlier in this lineage) were imported and trusted as infrastructure.
**`cv_measure.py`, `cv_grid.py`, `cv_analysis.py` — this front's own
scripts — were never opened, read, or imported at any point in this
review.** All measurement logic (`ref_measure.py`) was written from scratch
directly against `sc_engine.py`'s public functions and
`DERIVATION_PREREG.md` §2's prose description of the far-tail quantity
being measured, cross-checked only against `short_cycle_dynamics_attempt/
ATTEMPT.md`'s own prose description of its T1 `(20b,∞)` bin (also prose,
not code). All statistical machinery (`ref_stats.py`: Pearson r/t/p, OLS,
partial correlation, Spearman, the delta-method ratio-estimator SEM, the
sub-group z-test, and a Cochran's-Q heterogeneity test not used anywhere in
the front's own document) was independently re-derived from standard
first-principles statistics, then cross-validated by reproducing the
document's own reported table numbers exactly (§3 below) before being
applied to any new data.

**Fresh seeds**, drawn from `20260840100+` (`DECISION_LEDGER.yaml`
`DISC-DEC-057` reserves `20260840000+` for this front's referee), confirmed
unused anywhere in the archive by `grep -rn` before each use — see the full
seed table in §9.

---

## 0. VERDICT — **SOUND WITH NAMED ISSUES**

T0 reproduces exactly. Every one of the 9 independently re-simulated cells'
point estimates (dev_own%, dev_b1%) matches the document's reported figures
within `|z_diff|≤1.6` (none exceed the conventional `|z|=2` bar) — a clean,
non-cherry-picked reproduction at equal-or-larger `N`. My own from-scratch
statistical code reproduces every one of the document's reported
correlation/OLS/sub-group-range numbers exactly when run on the document's
own data, independently confirming both its arithmetic and its underlying
formulas.

I actively tried to break the `ρ`-lean (§5-§7 below) and **mostly failed**:
on my own most carefully triangulated re-measurement (which resolves the
one cell, `G1b`, the front itself left ambiguous), the pooled `ρ`
correlation is **stronger** than the document's own figure (`r=−0.680,
p=0.011`, now *surviving* Bonferroni correction for the 3 covariates
tested — which the document's own reported `r=−0.623, p=0.031` does
*not*), and `b`'s near-zero correlation is confirmed in every version of
the data I measured. But I also found a genuine, disclosable complication
the document could not see because it excluded the relevant cell: properly
resolving `G1b` (triangulated across 3 independent runs, `N=12{,}000`
combined `own-b` instances) shows it has the *highest* `H2`-share in its
own sub-group at a *middle* `ρ`, breaking any clean monotonic-in-`ρ`
story within `G1` — confirmed significant by two different heterogeneity
tests, not just one noisy run. This is a real finding the document's design
could not reach (it honestly excluded `G1b` per its own pre-registered
rule) and it complicates, without falsifying, the `ρ`-lean.

No error found threatens the document's PRIMARY-rule verdict (PARTIAL/
MIXED, honestly reported) or its most conservative claim (`b` ruled out).
Named issues are of the "the document's own secondary evidence is more
fragile / more complicated than presented" kind, not arithmetic or
methodology errors. Full detail below.

---

## 1. T0 — engine sanity for `b=1` — **CONFIRMED, exactly**

**Code inspection** (read in full, hunting specifically for a hidden `b=1`
special case, as prior referees in this lineage have done):
`sc_engine.build_R_mask(n, b, pi, seed_mask)` —

```python
def build_R_mask(n, b, pi, seed_mask):
    R = seed_mask.copy()
    cur = np.where(seed_mask)[0]
    for _ in range(1, b):
        ...
    return R
```

At `b=1`, `range(1, 1)` is the empty range — the loop body never executes,
for any `n, c, pi, seed_mask`. `R` is `seed_mask.copy()` exactly. No other
function in the 320-line file (`build_f`, `cyclic_mask_peeling`,
`pi_cycle_lengths`) depends on `b` at all — grepped every `def` site and
every literal `b` reference in the file to confirm no hidden special-casing
elsewhere.

**Empirical re-check** (`ref_grid.py`, seed `20260840100`, `N=40`, own
code, not the front's `cv_measure.py`):

```
R_mask == seed_mask exactly at b=1: violations=0/40
rho_formula (c/n) = 0.015259   rho_meas = 0.015234+/-0.000087   z=-0.280
```

Matches the front's own T0 (`0/30`, `z=+0.15`) and the grandparent front's
own T0. **T0: CONFIRMED.**

---

## 2. Re-simulation design and scale

9 of the 13 cells re-simulated (all four sub-comparisons covered, both
required extremes, and the ambiguous `G1b` cell at higher `N` as directed):

| id | b | c | ρ | N (mine) | N (front) | priority |
|---|---|---|---|---|---|---|
| A | 100 | 1000 | 0.7851 | 3000 | 2000 | hub, G1∩G2∩G3 |
| G1b | 50 | 1000 | 0.5364 | 6000 (+ 4000 replicate) | 2000 | **ambiguous, mandate priority (c)** |
| G1d | 200 | 1000 | 0.9538 | 2500 | 2000 | G1 extreme |
| G2a | 100 | 200 | 0.2633 | 4000 | 2000 | **required extreme, mandate priority (b)** |
| G2d | 100 | 2000 | 0.9549 | 4000 | 2000 | **required extreme, mandate priority (b)** |
| G3c | 50 | 2000 | 0.7877 | 2500 | 2000 | G3 (ρ≈0.785–0.788) |
| G3d | 1007 | 100 | 0.7851 | 2000 | 2000 | G3 (ρ≈0.785–0.788) |
| B | 400 | 100 | 0.4571 | 2500 | 2000 | hub G4 |
| G4c | 26 | 1500 | 0.4523 | 2000 (+ 3000 replicate) | 2000 | G4 (ρ≈0.452–0.458) |

Not re-simulated (used verbatim from `ATTEMPT.md` §2, clearly labeled
throughout as `[doc]`, never presented as this review's own data): `G1a`,
`G2b`, `G3a`, `G4b`.

Every cell uses the **same** matched-threshold, two-condition design as the
front (`threshold=20·b_orig` for both `own-b` and `b=1`), `n=65536`
throughout, `nworkers=4`. Own code (`ref_measure.py`): a fresh
`cycle_lengths_fast` (vectorized-scan variant of cycle labeling,
cross-checked bit-for-bit against `sc_engine.pi_cycle_lengths` on 10 random
permutations, throwaway seed `999900020`), a pooled ratio-estimator
`phi_far`, and a Cochran-style delta-method SEM **independently re-derived
from first principles** (§4 below), not copied from any front or
sibling-referee script. Multiprocessing determinism (4 workers vs.
single-process, same `SeedSequence`) verified bit-identical before use
(throwaway seed `999900023`). Full grid: 9 cells × 2 conditions,
**57,000 total instances, 14.24 minutes wall-clock** (`ref_grid.log`).

Two additional **second-replicate** measurements (`ref_replicate.py`,
fresh seeds) were run post-hoc on `G1b` and `G4c` specifically, because
these two cells' first-replicate results anchor the review's most
consequential findings (§6, §7) and deserved a robustness check before
being weighted heavily.

---

## 3. Statistical machinery re-derivation — **exact match to the document's own reported numbers**

`ref_stats.py`'s Pearson r/t/p (with an independent 50,000–100,000-shuffle
permutation-test cross-check of every parametric p-value), OLS, and
sub-group range/z-test were written from standard textbook first
principles, then run on the document's **own** reported 12-cell table
(transcribed verbatim from `ATTEMPT.md` §2, not new data) as a
correctness check before touching any of my own measurements:

| quantity | my recomputation | document's reported figure |
|---|---|---|
| `r(ρ, H2share)` | `r=−0.6223, t=−2.5141, p=0.0307` | `r=−0.623, t=−2.516, p=0.0306` |
| `r(log10 c, H2share)` | `r=−0.5483, p=0.0649` | `r=−0.549, p=0.0648` |
| `r(log10 b, H2share)` | `r=+0.0785, p=0.8084` | `r=+0.079, p=0.8083` |
| OLS `R²` | `0.6814` | `0.68` |
| OLS `ρ` coefficient (fraction scale) | `+4.338` | `+4.33` |
| `r(log10 c, log10 b)` across design | `−0.7526` | `−0.75` |
| G1 range / z | `28.9pp / +1.69` | `28.9pp / +1.70` |
| G2 range / z | `81.8pp / +4.16` | `81.7pp / +4.16` |
| G3 range / z | `15.7pp / +0.57` | `15.7pp / +0.57` |
| G4 range / z | `23.5pp / +0.73` | `23.5pp / +0.73` |

**Every figure matches to rounding precision.** Independent, from-scratch
permutation-test p-values agree with the parametric ones at every
covariate (`ρ`: perm `p=0.0318` vs. parametric `0.0307`; `log10 c`:
`0.0655` vs. `0.0649`; `log10 b`: `0.8086` vs. `0.8084`) — the parametric
t-test is not distorting anything here. This independently confirms both
the document's arithmetic (already checked by the orchestrating session)
**and** the correctness of the underlying formulas (re-derived here, not
copied). **All formulas and reported numbers: CONFIRMED.**

---

## 4. Delta-method SEM — re-derived, and cross-checked by cluster bootstrap

Independent first-principles derivation (Cochran ratio-estimator theory):
for `R̂=Σyᵢ/Σxᵢ` over `N` independent clusters (instances), with
`dᵢ=yᵢ−R̂xᵢ` (which sums to exactly zero by construction),
`SEM(R̂)=√(Σdᵢ²/(N−1))/(√N·x̄)`. Cross-checked against a `B=4000`-replicate
cluster bootstrap on 4 cells (own-b condition):

| cell | delta-method SEM(φ_far) | bootstrap SEM(φ_far) | ratio |
|---|---|---|---|
| G2a | 0.000613 | 0.000615 | 1.0035 |
| G2d | 0.000735 | 0.000709 | 0.9648 |
| G1b | 0.000281 | 0.000282 | 1.0048 |
| A | 0.000563 | 0.000566 | 1.0056 |

All four agree to within 4%. **The delta-method SEM is well-calibrated,
not underestimated** — the large swings between independent measurements
of the same cell reported below (§6, §7) are genuine sampling variability
at the *stated* precision, not evidence of a broken estimator.

---

## 5. Attacking the ρ-conclusion: robustness checks on the document's own reported data

Applied **before** touching any of my own new measurements, purely to
stress-test the document's own 12-cell table:

**(a) Bonferroni.** The document tests 3 covariates and highlights `ρ`'s
`p=0.031` as the one "crossing conventional significance," but nowhere
applies or mentions a multiple-comparisons correction. At `m=3`,
`α_adj=0.0167` — **`ρ`'s own `p=0.031` does not survive.** Neither do
`log10 c` (`p=0.065`) or `log10 b` (`p=0.81`). **This is a real,
disclosable gap: the document should at minimum have flagged that its
headline correlation is significant only at uncorrected α=0.05, not under
any standard correction for the number of covariates it pre-registered
testing.**

**(b) Leverage / leave-one-out.** Dropping any single one of several
extreme-`ρ` cells collapses `ρ`'s significance: drop `G2a`→`r=−0.486,
p=0.130`; drop `G2d`→`r=−0.519, p=0.102`; drop `G1d`→`r=−0.537, p=0.089`.
**The pooled correlation's significance on the document's own 12-cell
table is driven by a handful of points, not a uniformly-present pattern.**

**(c) Spearman (rank, robust to leverage and linearity).** `r=−0.5254`,
permutation `p=0.081` (scipy cross-check: `p=0.079`) — **NOT significant
at conventional α=0.05**, in direct contrast to the Pearson `p=0.031`.

**(d) Partial correlations controlling for `ρ`.** `partial r(log10 b,
share|ρ)=+0.447`; `partial r(log10 c, share|ρ)=−0.478` (both `n=12,
df=9`, neither individually significant, `p≈0.14–0.17`, but both are
*larger in magnitude* than `log10 b`'s raw marginal correlation
(`+0.079`). "`b`'s pooled correlation is essentially zero" is true only for
the *raw* bivariate test; conditioning on `ρ` (itself a joint function of
`b` and `c`) re-exposes a non-trivial `b` signal the marginal test masks.

**(e) Alternative monotonic covariate.** `−log(1−ρ)` (linear in `b` at
fixed `c`, a different but equally principled monotonic summary of the
pair) correlates *more* strongly than raw `ρ`: `r=−0.7041, p=0.0106`. The
document explicitly disclaims fitting any functional form, so this is not
a contradiction — but it shows Pearson-on-raw-`ρ` likely *understates* the
true (probably nonlinear-in-the-tail) relationship, an avenue the document
does not explore.

**(f) Constructive, non-`ρ`-favoring checks (for balance).** `ρ`-tertile
means show a clean monotonic decrease (`60.0%→44.4%→30.8%`); a median-`b`
split gives virtually identical group means (`45.1%` vs. `45.0%`) despite
similar `ρ` ranges in both halves — both **support** the qualitative
direction of the document's lean and its "`b` doesn't matter marginally"
claim independently of the correlation-significance question.

**Net read of this section:** the document's own "lean, not certified"
framing turns out to be *appropriately* cautious — if anything the
document could have disclosed **more** fragility (Bonferroni, Spearman,
leverage) than it did, all of which point the same direction (less
confidence in the raw `r=−0.623` figure specifically), even though (as §6
shows) properly resolving the design's most underpowered cell ultimately
strengthens rather than weakens the qualitative `ρ` story.

---

## 6. The `G1b` resolution — the review's most consequential finding

`G1b` (`b=50,c=1000,ρ=0.5364`) was excluded by the document at its own
`N=2000` (`|z_own|=1.97<2`, "right at the boundary"). Mandate priority (c)
asked whether a larger `N` resolves it, and whether that resolution
matters.

**First replicate** (`N=6000`, seed `20260840103/104`): `own-b`
`dev=−4.089%, z=−5.945` — unambiguously real. `H2share=79.8%±21.3pp`.

**Second, independent replicate** (`N=4000`, fresh seeds
`20260840119/121`, run after the fact specifically to stress-test this
finding before relying on it): `own-b dev=−3.859%, z=−4.632`.
`H2share=46.8%±24.1pp`.

**Inverse-variance-weighted combination of all three independent
measurements** (the document's own `N=2000` run + my two replicates,
`N=2000+6000+4000=12{,}000` `own-b` instances total, matched methodology,
independent seeds throughout):

| condition | combined dev% | combined SEM | combined z |
|---|---|---|---|
| own-b | −3.731% | 0.4853% | **−7.688** |
| b=1 | −2.524% | 0.4840% | **−5.216** |

**`G1b`'s own-b far-tail deficit is real at very high confidence** — this
resolves the exact open question the document itself named in §6
("a higher-power rerun... might resolve whether its own-b deficit is
real" — not attempted there, attempted here). **Combined `H2share =
67.7% ± 15.7pp`.**

**This is the highest (or effectively tied-highest) `H2`-share in the
entire `G1` sub-group, sitting at a *middle* `ρ` (0.54) — between `G1a`
(`ρ=0.32, share=35.5%`) and `A` (`ρ=0.79, share=23.5%` on my own
remeasurement, `41.2%` on the document's) — breaking any clean
monotonic-decreasing-in-`ρ` pattern within `G1`.** Recomputing `G1`'s
sub-group heterogeneity with this triangulated value in place of the
document's exclusion:

| test | document (`G1b` excluded) | with `G1b` resolved |
|---|---|---|
| raw range | `28.9pp` (AMBIGUOUS) | `50.4pp` (VARIES SUBSTANTIALLY per the locked rule) |
| pairwise max/min z | `+1.70` (within noise) | `+3.04` (exceeds noise) |
| **Cochran's Q** (whole-group, `df=2→3`) | `Q=3.19, p=0.203` (consistent with flat) | **`Q=9.36, p=0.025`** (significantly heterogeneous) |

Both a naive pairwise test **and** a more statistically standard
whole-group heterogeneity test (Cochran's Q — not used anywhere in the
document, added here as a more rigorous alternative, §8) agree: **once
`G1b` is properly resolved, `G1` is genuinely, robustly non-flat, and the
pattern is not monotonic in `ρ`.** This is a real complication the
document's own design could not surface (it excluded the one cell that
carries it), found by directly following the document's own suggested,
un-attempted next step.

**What this does *not* mean:** it does not show `ρ` is wrong or that `b`
is the "real" driver instead — `G1` holds `c` fixed and lets `ρ` and `b`
co-vary together, so a non-monotonic-in-`ρ` pattern here is equally a
non-monotonic-in-`b` pattern; it is evidence against *any* simple,
single-covariate, monotonic story for `G1` specifically, not evidence for
a competing single-covariate story.

---

## 7. `G4c` — a concrete illustration of the design's b=1-companion fragility

`G4c`'s `b=1` companion was already flagged by the document itself as one
of four cells with weak/non-significant `b=1` signal (`z_b1=−1.70`). My
first replicate (`N=2000`, fresh seed) measured `dev_b1=+0.382%,
z=+0.319` — **the sign flipped** relative to the document's own run.
Given the bootstrap-confirmed-correct SEMs (§4), this is not a bug; it is
a faithful illustration of how close to a genuinely-zero effect this
particular cell's `b=1` companion sits.

Second replicate (`N=3000`, fresh seed): `dev_b1=−1.145%, z=−1.180` — back
to the document's sign, still non-significant. **Inverse-variance
combination of all three runs** (document + 2 replicates,
`N=2000+2000+3000=7000`): `dev_b1=−0.965%±0.633%, z=−1.525` — still not
individually significant, consistent with the document's own honest
flagging of this cell. **Combined `H2share=25.9%±17.5pp`** (vs. the
document's `46.5%±30.2pp`, my own first replicate's `−8.5%±26.6pp`, and my
second replicate's `40.9%±37.4pp` — four estimates spanning roughly `−9%`
to `47%`, all mutually consistent given their width, none individually
trustworthy). This is offered as a **concrete empirical demonstration**
that `H2share` for a cell whose `b=1` numerator is not itself established
is not a stable point estimate across independent runs — a caution that
should generalize to the other three such cells in the design (`G1a,
G2b, G2d`, all `|z_b1|<2` per the document's own table) and tempers how
much weight any *individual* cell's `H2share` — not just `G1b`'s — can
bear.

Recomputing `G4`'s heterogeneity with the triangulated `G4c` value: raw
range `46.0pp`, pairwise z `+2.20` (nominally exceeds the `z=2` noise
bar, in contrast to the document's own `z=0.73`) — **but Cochran's Q gives
`Q=4.99, df=2, p=0.083`, not significant.** Unlike `G1`'s flip (§6, robust
to both tests), **`G4`'s apparent flip does not survive the more rigorous
whole-group test** — I am flagging this explicitly as a finding I tried to
press and could **not** fully substantiate; the honest characterization is
"suggestive, not established," not a confirmed reversal of the document's
`G4` result.

---

## 8. Full hybrid/triangulated 13-cell re-analysis

Final table: my own single remeasurement for `A, G1d, G2a, G2d, G3c, G3d,
B` (all replicate directly against the document within `|z_diff|<1.6`,
§9); the 3-way triangulated combination for `G1b` and `G4c` (§6, §7); the
document's own values, unchanged, for the 4 cells not re-simulated (`G1a,
G2b, G3a, G4b`).

| covariate | my r | my p | Bonferroni (`α_adj=0.0167`) | document's r/p |
|---|---|---|---|---|
| `ρ` | **−0.6797** | **0.0106** | **survives** | `−0.623 / 0.031` (does not survive) |
| `log10(c)` | −0.6246 | 0.0225 | does not survive | `−0.549 / 0.065` |
| `log10(b)` | +0.1354 | 0.659 | does not survive | `+0.079 / 0.81` |

Spearman on the triangulated table: `ρ: r=−0.737`; `log10 c: r=−0.691`;
`log10 b: r=+0.084` — the rank correlation for `ρ` is now *also* strong
and (unlike on the document's own data, §5c) clearly significant.
**Properly resolving the design's weakest cell strengthens, not weakens,
the pooled-correlation evidence for `ρ` — the opposite of what I set out
to find when hunting for a counter-story.**

Sub-group ranges, triangulated table, both tests:

| group | raw range | pairwise z | Cochran's Q (p) | document's original |
|---|---|---|---|---|
| G1 | 50.4pp | +3.04 | **p=0.025** (heterogeneous) | 28.9pp, AMBIGUOUS, `Q p=0.203` |
| G2 | 88.4pp | +6.30 | **p<0.0001** (heterogeneous) | 81.7pp, VARIES, `Q p=0.0001` |
| G3 | 35.5pp | +1.67 | p=0.283 (**consistent with flat**) | 15.7pp, AMBIGUOUS, `Q p=0.946` |
| G4 | 46.0pp | +2.20 | p=0.083 (marginal, not significant) | 23.5pp, AMBIGUOUS, `Q p=0.759` |

Reading this table honestly: `G2`'s heterogeneity is overwhelming and
un-shaken in every version of the data and every test (the design's single
most robust finding). `G3` remains statistically consistent with "flat"
under the more rigorous test even though its raw range grew and crossed
the document's own mechanical `30pp` cutoff — evidence the raw-range
PRIMARY rule is a somewhat blunt instrument, over-sensitive to one
wide-SEM cell (`G3c`, `SEM=17.4pp`), more than evidence `G3` is genuinely
non-flat. `G4`'s apparent flip is marginal and does not survive the
stricter test. **Only `G1`, once its excluded cell is properly resolved,
shows a robust flip from the document's original finding** — and even
that flip does not identify a replacement single-covariate driver (§6).

Partial correlations on the triangulated table: `partial r(log10 b,
share|ρ)=+0.610`; `partial r(log10 c, share|ρ)=−0.612` — both substantial,
comparable in magnitude to `ρ`'s own raw correlation, confirming (more
strongly than on the document's own data) that `ρ` does not fully absorb
`b` and `c`'s marginal signal — there is real structure in the design `ρ`
alone does not capture, consistent with `G1`'s non-monotonic pattern.

---

## 9. Replication check — point estimates, all 9 re-simulated cells

| id | my dev_own% | doc dev_own% | z_diff | my dev_b1% | doc dev_b1% | z_diff |
|---|---|---|---|---|---|---|
| A | −8.752 | −8.06 | −0.46 | −2.054 | −3.32 | +0.82 |
| G1b | −4.089 | −2.37 | −1.24 | −3.264 | −1.64 | −1.17 |
| G1d | −20.009 | −19.64 | −0.24 | −3.470 | −2.41 | −0.66 |
| G2a | −8.631 | −8.42 | −0.14 | −8.221 | −7.41 | −0.56 |
| G2d | −22.114 | −20.31 | −1.29 | −1.510 | −1.26 | −0.18 |
| G3c | −6.173 | −6.00 | −0.11 | −0.895 | −3.41 | +1.59 |
| G3d | −22.148 | −22.14 | −0.00 | −7.793 | −10.54 | +1.40 |
| B | −12.166 | −13.37 | +0.74 | −8.751 | −9.36 | +0.36 |
| G4c | −4.506 | −4.27 | −0.14 | +0.382 | −1.98 | +1.42 |

**No cell's `z_diff` exceeds `2`** (max `|z_diff|=1.59`, `G3c`'s `b=1`
condition) — a clean, non-cherry-picked reproduction of every point
estimate at equal-or-larger `N`, with fresh independent seeds throughout.

---

## 10. Is the document's honesty framing accurate?

**Yes, and by a wider margin than the document itself could show.** The
document's own text is explicit that the PRIMARY mechanical rule yields
PARTIAL/MIXED and that the `ρ`-lean is "not a certified conclusion." My
independent re-analysis both (a) surfaces *more* reasons for caution than
the document discloses (Bonferroni, Spearman, leverage-sensitivity on its
own data, §5) and (b) — on the highest-precision data available, after
resolving the one cell the document left ambiguous — finds the pooled `ρ`
correlation *survives* those same stricter tests (§8), while also finding
a genuine complication (`G1`'s non-monotonicity, §6) the document's design
could not see. A reader relying only on the document's own reported
`r=−0.623, p=0.031` would be *overconfident* relative to what that number
alone can support (it doesn't survive Bonferroni or Spearman); a reader
who additionally knew this review's triangulated `G1b`/`G4c` figures would
be *entitled to somewhat more* confidence in the pooled `ρ` trend than the
document's own text conveys, but *less* confidence that it is a clean,
single-covariate, monotonic story than either document's framing might
suggest. **No overclaim found; no underclaim found beyond this nuance,
which is a genuine, disclosable addition, not a correction of an error.**

---

## 11. Errors and issues found, ordered by importance

1. **A real bug of my own, caught and fixed in this review before any
   number was reported**: my first draft of the hybrid-table analysis
   script mixed `H2share` on a 0–1 fraction scale (my own cells) with the
   document's 0–100 percent scale (the 4 cells not re-simulated),
   producing garbage correlations. Caught by eyeballing the printed table
   (values like `0.2%` next to `35.5%`), fixed, and the corrected script
   is what every number in §8 onward is based on. Disclosed here in the
   interest of showing the review's own process, not hidden.
2. **The document does not apply or mention a multiple-comparisons
   correction** for the 3 pre-registered covariate correlations, nor does
   it check Spearman or leave-one-out robustness. On the document's own
   data these checks reveal real fragility (§5) the document does not
   disclose. **Moderate**: does not change the document's own PARTIAL/MIXED
   verdict or its "lean, not certified" framing, but a fully rigorous
   write-up should have shown this working.
3. **`G1b`'s exclusion, while procedurally correct per the locked rule,
   hid a real and non-monotonic-in-`ρ` effect** (§6) — not an error in the
   document (the exclusion rule was followed exactly as pre-registered,
   and the document itself flags this as worth a future higher-`N` rerun),
   but a genuine limitation of what the 13-cell design as executed could
   show. **Moderate-to-notable**: does not overturn the `ρ`-lean (§8 shows
   the pooled correlation survives and strengthens) but shows the true
   relationship is not a clean single-covariate monotonic function of
   `ρ`, which the document's own binary decision framework has no
   category for.
4. **The document's own PRIMARY (raw range) and SECONDARY (pairwise
   max/min z) sub-group statistics are measurably less rigorous than a
   standard whole-group heterogeneity test** (Cochran's Q, §8) — using the
   more standard test changes which sub-groups look heterogeneous in ways
   that cut in *both* directions (`G3` looks more flat; `G1`, once
   resolved, looks less flat), so this is disclosed as a methodological
   observation, not a directional bias in the document's favor or against
   it. **Minor.**
5. No arithmetic, formula, or T0 error found anywhere in the document.
   Every reported number recomputes exactly from first-principles,
   independently re-derived code.

---

## 12. Scorecard

| claim | status | evidence |
|---|---|---|
| T0: `b=1` ⟹ `R=seed_mask` exactly | **CONFIRMED**, code read + fresh empirical (0/40, z=−0.28) | §1 |
| Every reported dev%/z/H2share arithmetic figure | **CONFIRMED**, exact match on independent recomputation | §3 |
| Pooled correlations, OLS, sub-group ranges (document's own data) | **CONFIRMED**, exact match, from-scratch code | §3 |
| Delta-method SEM formula | **CONFIRMED**, re-derived + bootstrap cross-check (ratio 0.96–1.01) | §4 |
| `ρ`'s headline `r=−0.623,p=0.031` significance | **NAMED ISSUE**: fails Bonferroni (m=3), fails Spearman (p=0.08), leverage-driven | §5 |
| `b` ruled out as independent driver | **CONFIRMED, robustly**, every version of the data (raw r=0.08–0.22, always p≫0.05) | §5, §8 |
| 9 re-simulated cells' point estimates | **CONFIRMED**, all `|z_diff|<1.6` vs. document | §9 |
| `G1b` own-b deficit, resolved | **CONFIRMED real** (combined z=−7.69, N=12,000), `H2share=67.7%±15.7pp` | §6 |
| `G1` sub-group, resolved | **FLIPS**: AMBIGUOUS → significantly heterogeneous, both tests | §6 |
| `G4c` b=1 companion | **CONFIRMED weak/sign-unstable** across 3 independent runs, as document itself flagged | §7 |
| `G4` sub-group "flip" | **NOT CONFIRMED** under the more rigorous Cochran's Q test (p=0.083) | §7, §8 |
| `G3` sub-group | Raw range crosses 30pp, but **Cochran's Q says still consistent with flat** (p=0.28) | §8 |
| Pooled `ρ` correlation, triangulated 13-cell table | **CONFIRMED and strengthened**: r=−0.680, p=0.011, survives Bonferroni | §8 |
| Partial correlations (b, c controlling for `ρ`) | Both substantial (~0.45–0.61), `ρ` does not fully absorb `b`/`c` | §5d, §8 |
| Document's honesty framing | **ACCURATE**, if anything conservative relative to what my re-analysis supports | §10 |
| Scope discipline (nothing outside this front's folder touched) | **CONFIRMED** | `git status --porcelain` |

---

## 13. Seeds (all used, this front's referee-reserved range `20260840000+`, confirmed unused by `grep -rn` before assignment)

| seed | use | N | result |
|---|---|---|---|
| `SeedSequence(20260840100)` | T0 re-check | 40 | 0/40 violations, z=−0.28 |
| `SeedSequence(20260840101)` | A, own-b | 3000 | dev=−8.752%, z=−9.328 |
| `SeedSequence(20260840102)` | A, b=1 | 3000 | dev=−2.054%, z=−2.094 |
| `SeedSequence(20260840103)` | G1b, own-b (1st replicate) | 6000 | dev=−4.089%, z=−5.945 |
| `SeedSequence(20260840104)` | G1b, b=1 (1st replicate) | 6000 | dev=−3.264%, z=−4.820 |
| `SeedSequence(20260840105)` | G1d, own-b | 2500 | dev=−20.009%, z=−19.170 |
| `SeedSequence(20260840106)` | G1d, b=1 | 2500 | dev=−3.470%, z=−3.234 |
| `SeedSequence(20260840107)` | G2a, own-b | 4000 | dev=−8.631%, z=−10.267 |
| `SeedSequence(20260840108)` | G2a, b=1 | 4000 | dev=−8.221%, z=−9.731 |
| `SeedSequence(20260840109)` | G2d, own-b | 4000 | dev=−22.114%, z=−27.662 |
| `SeedSequence(20260840110)` | G2d, b=1 | 4000 | dev=−1.510%, z=−1.824 |
| `SeedSequence(20260840111)` | G3c, own-b | 2500 | dev=−6.173%, z=−5.904 |
| `SeedSequence(20260840112)` | G3c, b=1 | 2500 | dev=−0.895%, z=−0.841 |
| `SeedSequence(20260840113)` | G3d, own-b | 2000 | dev=−22.148%, z=−15.718 |
| `SeedSequence(20260840114)` | G3d, b=1 | 2000 | dev=−7.793%, z=−5.584 |
| `SeedSequence(20260840115)` | B, own-b | 2500 | dev=−12.166%, z=−11.003 |
| `SeedSequence(20260840116)` | B, b=1 | 2500 | dev=−8.751%, z=−7.788 |
| `SeedSequence(20260840117)` | G4c, own-b (1st replicate) | 2000 | dev=−4.506%, z=−3.904 |
| `SeedSequence(20260840118)` | G4c, b=1 (1st replicate) | 2000 | dev=+0.382%, z=+0.319 |
| `SeedSequence(20260840119)` | G1b, own-b (2nd replicate) | 4000 | dev=−3.859%, z=−4.632 |
| `SeedSequence(20260840120)` | G4c, own-b (2nd replicate) | 3000 | dev=−2.799%, z=−2.897 |
| `SeedSequence(20260840121)` | G1b, b=1 (2nd replicate) | 4000 | dev=−1.807%, z=−2.138 |
| `SeedSequence(20260840122)` | G4c, b=1 (2nd replicate) | 3000 | dev=−1.145%, z=−1.180 |

(Throwaway, outside the reserved range, discarded, matching this archive's
disclosed-throwaway-seed convention: `999900020` cycle-labeling
cross-check, `999900021`/`999900022` timing smoke tests, `999900023`
multiprocessing-determinism check.)

Total independent re-simulation: **9 of 13 cells** (all four sub-groups
covered), **68,000 fresh instances** across the main grid plus both
replicates, at `N` from `2000` to `6000` per measurement (all `≥` the
front's own `N=2000`; `G1b` and `G2a`/`G2d` pushed to `2–3×`).

---

## 14. Files produced by this review (all in `cell_variation_attempt/adversarial/`)

| file | role |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref_measure.py` | from-scratch far-tail measurement (imports `sc_engine`/`sc_formula` only), own `cycle_lengths_fast`, pooled ratio estimator, `h2_share` |
| `ref_stats.py` | from-scratch statistics: Pearson r/t/p (+permutation-test cross-check), Spearman, partial correlation, OLS, Bonferroni, sub-group z-test, cluster bootstrap |
| `ref_grid.py` / `ref_grid.log` / `ref_grid_stdout.log` / `ref_grid_raw.npz` | main 9-cell × 2-condition re-simulation, seeds `20260840100–118`, raw per-instance arrays |
| `ref_replicate.py` / `ref_replicate.log` | second independent replicates of `G1b`, `G4c`, seeds `20260840119–122` |
| `ref_analysis.py` / `ref_analysis.log` | hybrid-table re-analysis: replication check, pooled correlations, Bonferroni, leave-one-out, partial correlations, sub-group ranges, bootstrap SEM cross-check |
