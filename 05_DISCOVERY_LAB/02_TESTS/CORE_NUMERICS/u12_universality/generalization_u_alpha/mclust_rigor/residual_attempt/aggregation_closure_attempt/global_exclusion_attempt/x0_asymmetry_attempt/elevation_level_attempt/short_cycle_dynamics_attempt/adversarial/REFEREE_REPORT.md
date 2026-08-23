# REFEREE REPORT — adversarial review of `short_cycle_dynamics_attempt/ATTEMPT.md`

**Wave 12, `DISC-DEC-051`, front (b) `MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT`,
mandatory independent adversarial verification.**

Object under test: `short_cycle_dynamics_attempt/ATTEMPT.md` (§0–11) together
with its pre-registration `short_cycle_dynamics_attempt/DERIVATION_PREREG.md`.
Both were read in full, together with `elevation_level_attempt/ATTEMPT.md`
and `elevation_level_attempt/adversarial/REFEREE_REPORT.md` (all sections,
§3.2/§5/§11 read closely as instructed), before any line of code in this
folder was written.

**Scope and discipline.** Everything produced by this review lives in
`short_cycle_dynamics_attempt/adversarial/`. No file outside it was created,
modified, or touched — confirmed by `git status --porcelain` at the end of
this review, which shows exactly one untracked path relative to HEAD
(`7a9636e`): the `short_cycle_dynamics_attempt/` folder itself (this review's
own subfolder is inside it). Not `ATTEMPT.md`, not `DERIVATION_PREREG.md`,
not any ancestor `ATTEMPT.md`/`REFEREE_REPORT.md`, not `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, any `README*`, or
`PROOF_DEPENDENCY_MAP.md`. **No git commit was created.**

**Independence.** Every script here (`adv_*.py`) was written from scratch
from the mechanism as stated in the prose of `ATTEMPT.md` and
`DERIVATION_PREREG.md` (and, for φ_U/T_U/φ_REDB, from the printed closed
forms in `generalization_u_alpha/DERIVATIONS.md` line 170 and
`elevation_level_attempt/adversarial/REFEREE_REPORT.md` §11). **No `.py`
file under `short_cycle_dynamics_attempt/` itself, `elevation_level_attempt/`,
or `elevation_level_attempt/adversarial/` was read or imported at any
point** — not `sc_engine.py`, `sc_formula.py`, `sc_diagnostic.py`,
`sc_reduction.py`, `sc_batch.py`, nor `elev_*.py`, nor `ref2_*.py`. Every
`adv_*.py` script imports only other `adv_*.py` scripts in this same
subfolder.

**Fresh seeds**, confirmed unused anywhere in the archive by
`grep -r "20260826"` over the repository (filtered to `.py/.md/.log/.json/.yaml`,
0 hits) before use — this review's own seed block, `20260826000`–`20260826032`:

| seed | use |
|---|---|
| `SeedSequence(20260826000)` | `adv_engine.py selftest` (own T0) |
| `SeedSequence(20260826001)` | `adv_mechanism.py` — large-scale mechanism stress test (Claim 1) |
| `SeedSequence(20260826010)` | `adv_diagnostic.py` T1, target cell (100,1000,65536), N=2500 |
| `SeedSequence(20260826011)` | `adv_diagnostic.py` T1, cell (400,100,65536), N=2000 |
| `SeedSequence(20260826012)` | `adv_diagnostic.py` T1, cell (200,150,65536), N=2000 |
| `SeedSequence(20260826020–025)` | `adv_reduction.py` T2, 6-cell grid (target cell gets 025, N=2000; others N=1500) |
| `SeedSequence(20260826030)` | `adv_diag_bootstrap.py` — fresh independent re-run, target cell, N=4000 |
| `SeedSequence(20260826031)` | bootstrap resampling RNG (3000 replicates/bin) |
| `SeedSequence(20260826032)` | `adv_diag_decompose.py` — untouched/touched decomposition, target cell, N=3000 |

No seed above was reused for a second purpose. No `.json`/`.log`/`.npz` file
existed in this subfolder before the first script ran (confirmed by directory
listing at review start: empty).

---

## 0. VERDICT — **SOUND WITH NAMED ISSUES**

### Claim 1 (the mechanism, §1) → **CONFIRMED, exactly, at larger scale than the target**

Own from-scratch stress test (`adv_mechanism.py`), 5 cells including two
deliberately engineered edge cases (p up to 0.40, up to 30 seeds landing on
one short cycle), **2,653,644 total short-cycle points examined (2.2× the
target's stated >1.2M), zero violations** of either half of the claim: an
untouched π-cycle of length ≤b is never touched by R; a touched one is
*entirely* absorbed into R with zero run-starts anywhere on it (tested
directly, not just inferred). A second, independent from-scratch selftest
(`adv_engine.py`, its own T0) reproduces the same 0-violation result at
smaller scale plus four other structural checks (ρ, `R^c⊆U_rem`, peeling
vs. brute force). This is the strongest and least ambiguous result in the
review, and the document's claim here is, if anything, understated: it holds
under harder stress than the document tried.

### Claim 2 (T1 diagnostic split, §3) → **CONFIRMED**

Own engine (`adv_diagnostic.py`), 3 cells, N=2000–2500. The su-bucket sanity
check reproduces **exactly 1.000000000 ± 0** at all three cells (0
violations, 125,644–612,832 points per cell) — a genuine tautological
consequence of Claim 1, correctly reported as such. The long-cycle
population deviates from φ_U(c'') in the same direction as the document at
all three cells, with comparable order of magnitude (my dev/z: −4.87%/−4.33,
−4.40%/−3.61, −7.09%/−6.61 vs. the document's −8.40%/−8.25, −7.56%/−7.22,
−4.75%/−4.43) — smaller in magnitude at two of three cells and larger at the
third, consistent with ordinary between-seed scatter at N≈2000–2500 for an
effect this size (the referee report for the predecessor front records the
same kind of gap between low-N and high-N runs of a similarly-sized effect).
The measured `w_short` (0.356%, 0.858%, 0.394%) matches the document's own
figures (0.365%, 0.844%, 0.379%) closely at all three cells, cross-validating
that the R-construction and su/long split are implemented correctly.

### Claim 3 (L-binned non-monotonic structure, §3.1) → **QUALITATIVE SHAPE CONFIRMED, ROBUSTLY; QUANTITATIVE MAGNITUDES IN THE NEAR-b BINS ARE A NAMED ISSUE**

The headline qualitative claim — large positive excess for L just above b,
settling to a persistent negative plateau for large L — reproduces
independently, and *more* strongly than the document's own figures at the
near-b peak. The far-tail plateau ((20b,∞) bin) is well matched in sign and
rough size across all three cells. But the specific point estimates and
z-scores the document reports for the (b,2b] and (2b,5b] bins do not
reproduce under independent replication: two fresh independent seeds at the
target cell (N=2500 and N=4000) give (b,2b]-bin excess of +874% and +796%
respectively — both **roughly 3× the document's own reported +267.7%** for
the identical cell/bin — and this same directional gap (mine consistently
1.3×–3.3× higher) appears at all three tested cells. A decomposition
(`adv_diag_decompose.py`) traces this to the R^c-conditioning itself:
within the (b,2b] bin, untouched cycles (exactly-1, confirmed again here)
supply 54.6% of the target cell's R^c-conditional population — far more
than a naive *unconditional* weighting would suggest — which alone, plugged
into the document's own two-state model, predicts ≈+855%, close to what I
measured (+796–874%) and not close to what the document reports (+267.7%).
See §4 below. This is a real, named precision issue in one specific table,
not a refutation of the underlying phenomenon — which the document itself
already declines to promote to a formula (§3.1: "illustrative … not
adopted").

### Claim 4 (φ_REDC refutation, §2/§6/§7) → **CONFIRMED**

Own formula module (`adv_formula.py`) and own formula-free 6-cell reduction
test (`adv_reduction.py`, N=1500–2000/cell). φ_REDC is uniformly above
φ_REDB at every grid cell (my range +1.05%…+6.23%, vs. the document's
+1.6%…+6.4% — same direction, close magnitude), the wrong sign relative to
the residual. On the formula-free test, pooled χ² degrades from 20.32
(φ_REDB, full φ) to 97.70 (φ_REDC) — a 4.81× worsening (document: 8.6×; same
direction, smaller at my lower N). The pre-registered T2 success criterion
fails decisively and independently: on the target cell, |z| goes from 0.41
to 3.04 (a −647% "reduction", i.e. a dramatic worsening, not the required
+30% improvement), and 2 of the other 5 cells exceed their allowed bound.
φ_REDC moves the wrong direction on essentially every cell, exactly as the
document reports.

### Claim 5 (scope/honesty audit) → **CONFIRMED, no overclaim found**

`git status` shows only the front's own new subfolder as changed relative to
HEAD. File mtimes inside `short_cycle_dynamics_attempt/` confirm
`DERIVATION_PREREG.md` (13:35:50) predates every simulation output
(`sc_engine_selftest.log` 13:38:34 onward) and `ATTEMPT.md` itself
(14:01:09, written last). I read §8/§9/§10 against the body with my own
numbers in hand and found no place where the executive summary or verdict
claims more than the body supports — if anything my own Claim 3 finding
(§4 below) modestly *vindicates* the document's own hedging, since it
explicitly declined to adopt the near-b figures as a formula.

---

## 1. Claim 1 — the mechanism, re-verified from scratch (`adv_mechanism.py`, `adv_engine.py`)

`ATTEMPT.md` §1 / `DERIVATION_PREREG.md` §1.3 claim: for a π-cycle of length
L≤b, (a) untouched by every seed (prob (1−c/n)^L) ⇒ deterministically an
f-cycle, every point cyclic w.p. exactly 1; (b) touched by ≥1 seed ⇒ the
*entire* cycle is pulled into R and becomes permanently unreachable by any
normal π-step (zero run-starts anywhere on it).

I wrote this test purely from the prose (never reading `sc_engine.py`),
using `scipy.sparse.csgraph.connected_components` (weak) on the directed
graph `i → π(i)` to get exact π-cycle lengths — validated on a hand-built
5-point permutation before use (`[1,2,0,4,3]` → lengths `[3,3,3,2,2]`,
exact match) — and fully vectorized per-instance checks (grouping cycles by
label, no Python-level per-cycle loop needed for the main stress test).

**Stress cells** (`adv_mechanism.py`, seed `20260826001`):

| cell | instances | total short pts | untouched | touched | claim(a) viol. | claim(b) viol. | claim(b)-strong viol.¹ | max seeds/short-cycle |
|---|---|---|---|---|---|---|---|---|
| target b=100,c=1000,n=65536 | 6000 | 603,273 | 305,414 | 297,859 | 0 | 0 | 0 | 6 |
| b=400,c=100,n=65536 | 3000 | 1,189,775 | 875,524 | 314,251 | 0 | 0 | 0 | 5 |
| b=200,c=150,n=65536 | 3000 | 590,610 | 475,799 | 114,811 | 0 | 0 | 0 | 3 |
| edge: n=2000,b=50,c=800 (p=0.40) | 3000 | 149,299 | 4,572 | 144,727 | 0 | 0 | 0 | **30** |
| edge: n=16384,b=30,c=300 | 4000 | 120,687 | 91,403 | 29,284 | 0 | 0 | 0 | 4 |
| **combined** | | **2,653,644** | **1,752,712** | **900,932** | **0** | **0** | **0** | |

¹ "claim(b)-strong": for every *touched* short cycle, additionally checked
that **no point on it is a run-start** (`p∈R` with `π⁻¹(p)∉R`) — the
sharper "permanently unreachable by any normal step" form of claim (b), not
just "in R".

Elapsed 117.7s. **0/2,653,644 violations**, including the deliberately
adversarial edge cell (p=0.40, up to 30 seeds sharing one short cycle) — the
scenario most likely to expose an off-by-one or overlap bug in the
union-of-runs bookkeeping. A second, independent from-scratch T0-style
selftest (`adv_engine.py`, seed `20260826000`) reproduces the same 0/2389
result at smaller scale plus: ρ vs. `1−(1−c/n)^b` (8 cells, max|z|=2.13);
`R^c⊆U_rem` (40 instances, 0 violations); `cyclic_mask_peeling` vs. literal
brute-force orbit-following (200 random small graphs, 0 mismatches).

**Conclusion: Claim 1 is CONFIRMED exactly**, at a combined scale 2.2× the
document's own, including edge cases the document's own selftest (2389
points, ≤38 touched cycles) did not specifically target.

---

## 2. Claim 2 — T1 diagnostic split (`adv_diagnostic.py`)

Own engine, three cells, own peeling-based cyclic-set computation (in-degree
peeling with a per-instance stack, matching the document's own stated
choice to reject batched peeling for the same long-tail reason it names).
Errors: delta-method ratio-of-sums estimator across instances (treating each
instance as one i.i.d. cluster), matching the practice already established
in this lineage (`elevation_level_attempt/adversarial/REFEREE_REPORT.md`
§5.2: "errors are delta-method, instances are i.i.d.").

| cell | su bucket (n, φ) | long bucket (n, φ, dev%, z) | overall Rc (n, φ, dev%, z) | w_short measured |
|---|---|---|---|---|
| target (100,1000,65536) | 125,644, **1.000000000±0**, 0 viol. | 35,181,172, 0.057070±0.000674, **−4.87%**, z=−4.33 | 35,306,816, 0.060425±0.000672, +0.72%, z=+0.64 | 0.356% |
| (400,100,65536) | 612,832, **1.000000000±0**, 0 viol. | 70,845,640, 0.114897±0.001463, **−4.40%**, z=−3.61 | 71,458,472, 0.122488±0.001449, +1.92%, z=+1.59 | 0.858% |
| (200,150,65536) | 326,284, **1.000000000±0**, 0 viol. | 82,531,588, 0.084448±0.000974, **−7.09%**, z=−6.61 | 82,857,872, 0.088054±0.000975, −3.12%, z=−2.91 | 0.394% |

Document's own figures for comparison (long bucket): target −8.40%/z=−8.25,
(400,100) −7.56%/z=−7.22, (200,150) −4.75%/z=−4.43. **Direction matches at
all three cells; magnitude is the same order but not identical** — my
target-cell and (400,100)-cell deviations run smaller than the document's,
my (200,150)-cell deviation runs larger. Given the effect is genuinely small
(4–8%) and both runs use N≈2000–2500 (an order of magnitude below the
≥300,000-instance runs this lineage uses when it wants ≤1% precision on an
effect this size — see the predecessor referee report §5.2), this spread is
consistent with ordinary sampling variation, not a sign of an error in
either measurement. The "overall Rc" row shows the same expected
small-effect noise (my signs even flip relative to the document's at two of
three cells, both around |z|≈1, i.e. both consistent with an aggregate
residual too small for either run's N to pin down confidently) — the T2
reduction test below (§5), which is what actually validates the aggregate
number at reasonable precision, agrees well with φ_REDB.

**Conclusion: Claim 2 is CONFIRMED.** The su-bucket tautology is exact, as
required. The long-bucket deviation from φ_U(c'') is real, in the document's
claimed direction, at a comparable order of magnitude, at all three cells.

---

## 3. Claim 4 — φ_REDC refutation (`adv_formula.py`, `adv_reduction.py`)

### 3.1 Formula self-check

`adv_formula.py`, built only from the printed closed forms (φ_U from
`DERIVATIONS.md` line 170, φ_REDB from the referee report §11, φ_cond_C/φ_REDC
re-derived from `ATTEMPT.md` §2's own stated formula, not from any `.py`).
φ_U closed form checked against independent `scipy.integrate.quad` at 8
values of c: max relative error 3.9×10⁻¹⁶. `w_short` at the target cell:
**0.3590%** (document: "≈0.359%" — exact match). `φ_cond_C` vs. φ_U(c'') at
the target cell: **+5.63%** (document: "+5.6%" — exact match). `φ_REDC` vs.
`φ_REDB` across the 6-cell grid: my range **+1.05%…+6.23%** (document:
+1.6%…+6.4% — same direction and rough range; small numeric gap, noted but
immaterial to the conclusion — all 6 cells positive either way). `n→∞`
convergence of both φ_REDB and φ_REDC to φ_U(c) confirmed at fixed (b,c) for
n=2¹⁶…2²⁴.

### 3.2 Formula-free 6-cell reduction test

`adv_reduction.py`, own engine (same as §1–2), N=1500/cell (2000 at the
target cell), no formula on the measurement side.

| cell (b,c,ρ) | φ_Rc measured | vs φ_REDB_cond | vs φ_REDC_cond | full φ measured | vs φ_REDB_full | vs φ_REDC_full |
|---|---|---|---|---|---|---|
| 50,400,0.264 | 0.049689±0.000679 | −4.05% z=−3.09 | −5.04% z=−3.89 | 0.036891±0.000504 | −3.47% z=−2.63 | −4.47% z=−3.43 |
| 100,400,0.457 | 0.058673±0.000810 | −2.78% z=−2.07 | −5.32% z=−4.07 | 0.032189±0.000445 | −2.14% z=−1.58 | −4.74% z=−3.60 |
| 100,600,0.601 | 0.057171±0.000765 | −0.65% z=−0.49 | −3.73% z=−2.90 | 0.023342±0.000315 | +0.32% z=+0.24 | −2.84% z=−2.16 |
| 200,150,0.368 | 0.092556±0.001185 | +1.61% z=+1.24 | −1.96% z=−1.56 | 0.058721±0.000759 | +1.80% z=+1.37 | −1.85% z=−1.46 |
| 400,100,0.457 | 0.115019±0.001624 | −4.43% z=−3.28 | −9.83% z=−7.72 | 0.062791±0.000889 | −4.04% z=−2.97 | −9.66% z=−7.55 |
| **100,1000,0.785 (target)** | 0.060353±0.000717 | −0.86% z=−0.73 | −4.76% z=−4.21 | 0.013905±0.000164 | +0.48% z=+0.41 | −3.45% z=−3.04 |
| **pooled χ²** | | **26.93** | **119.85** (4.45×) | | **20.32** | **97.70** (4.81×) |

**Pre-registered T2 success criterion (§7 of `DERIVATION_PREREG.md`)**: on
the target cell, |z| goes from **0.41 (φ_REDB) to 3.04 (φ_REDC)** — a
**−647%** change, i.e. a dramatic worsening, nowhere near the required +30%
reduction. Two of the other five cells (100,400 and 400,100) additionally
exceed `max(2×φ_REDB|z|, 2.5)`. **The criterion fails on both independent
conditions**, exactly as `ATTEMPT.md` §7 reports for its own run.

The magnitude of the pooled-χ² degradation (4.45×/4.81× here vs. the
document's 8.6×) differs, entirely attributable to the ~30–40% lower
instance counts used here relative to `sc_reduction.py`'s N=2000–3000, and
does not change the qualitative verdict: φ_REDC moves the wrong way, at
every cell, on both formula-level and formula-free grounds.

**Conclusion: Claim 4 is CONFIRMED independently.**

---

## 4. Claim 3 — the L-binned structure: what holds and the named issue

### 4.1 Qualitative shape — CONFIRMED, and stronger than reported

L-bins (b,2b], (2b,5b], (5b,20b], (20b,∞), fixed before looking at data,
matching the document's own choice exactly.

| cell | (b,2b] | (2b,5b] | (5b,20b] | (20b,∞) |
|---|---|---|---|---|
| target, my run (N=2500) | +874.3% z=+27.2 | +23.2% z=+1.7 | −9.1% z=−1.9 | **−6.4% z=−5.6** |
| target, `ATTEMPT.md` | +267.7% z=+11.7 | −11.0% z=−1.4 | −23.5% z=−5.5 | **−9.7% z=−9.4** |
| 400,100, my run | +521.2% z=+54.0 | +154.2% z=+14.5 | −11.0% z=−3.0 | **−10.6% z=−8.3** |
| 400,100, `ATTEMPT.md` | +328.2% z=+28.0 | +71.5% z=+9.8 | −11.9% z=−3.6 | **−14.7% z=−13.3** |
| 200,150, my run | +757.5% z=+60.9 | +316.5% z=+23.0 | −7.4% z=−1.6 | **−12.5% z=−11.6** |
| 200,150, `ATTEMPT.md` | +569.7% z=+39.0 | +203.4% z=+18.4 | −3.7% z=−0.9 | **−10.7% z=−9.7** |

The qualitative shape — huge, overwhelmingly significant positive excess
right above L=b, settling to a persistent negative plateau in the (20b,∞)
tail — replicates independently at **every** cell, with the far-tail plateau
(bold column) matching the document's reported magnitude reasonably well in
sign and rough size at all three cells (my figures run somewhat smaller at
the target cell, close at the other two). This is the strongest single piece
of evidence for the document's most novel claim, and it holds up.

### 4.2 The named issue: near-b magnitudes are not reproducible, and I can explain why

The (b,2b] and (2b,5b] bins show a **large, consistent, one-directional**
gap: my measurement runs 1.3×–3.3× the document's reported figure at every
one of the three cells' (b,2b] bin, and even flips sign at the target cell's
(2b,5b] bin (mine: +23% then +50% across two independent re-runs; document:
−11%, not itself significant). This is too large and too consistently
one-directional to be ordinary noise around a shared true value, so I
investigated further with two follow-ups (both fresh seeds, both target
cell):

**(a) Stability check** (`adv_diag_bootstrap.py`, seed `20260826030`,
N=4000, independent of the N=2500 run above): (b,2b] bin gives +795.8%
(z=+29.4 delta-method, z=+29.3 cluster-bootstrap with 3000 replicates — the
two error estimators agree to 3 significant figures, ruling out a
naive-SE-too-small artifact on my side). This lands close to my *first*
run's +874.3%, not to the document's +267.7%. Both of my independent seeds
agree with each other; neither agrees with the document.

**(b) Decomposition** (`adv_diag_decompose.py`, seed `20260826032`, N=3000):
split the (b,2b] bin's R^c population by whether its cycle is untouched or
touched. Result:

| bin | untouched sub-pop (n, φ) | touched sub-pop (n, φ, dev%, z) | untouched weight | reconstructed dev% |
|---|---|---|---|---|
| (b,2b] | 35,912, **1.000000000±0** | 29,860, 0.013262±0.003657, −77.89%, z=−12.78 | **54.60%** | +820.15% |
| (2b,5b] | 9,816, **1.000000000±0** | 209,864, 0.061869±0.005438, +3.13%, z=+0.34 | 4.47% | +73.00% |
| (5b,20b] | 2,104, **1.000000000±0** | 1,043,032, 0.051001±0.002576, −14.99%, z=−3.49 | 0.20% | −11.80% |

This confirms the extended Claim 1 fact yet again — the untouched
sub-population is exactly 1.0 in every bin, as it must be, mechanically. The
key finding is the **weight**: 54.6% of the target cell's (b,2b]-bin R^c
population comes from fully-untouched cycles. This is far larger than an
*unconditional* cycle-length-weighted estimate would suggest (a direct
calculation of `mean_{L=101}^{200}(1−p)^L` gives ≈11%, which is what the
document's own §3.1 back-of-envelope model implicitly uses, predicting only
+159%) — because conditioning on `x0∈R^c` is itself a strong selection
effect: an untouched cycle contributes *all* its points to R^c, while a
touched cycle near this L range contributes only its shrinking residual
arc, so R^c over-represents untouched cycles relative to their raw
probability. Plugging the *correct* conditional weight (54.6%) into the
document's own simple two-state model (untouched→1, touched→φ_U(c'')) gives
a predicted dev% of **≈+855%** — close to what I actually measured
(+796–874% across two independent runs), not close to the document's
reported +267.7%.

I also find that the **touched** sub-population itself sits well *below*
φ_U(c'') in the (b,2b] bin (−77.89%, z=−12.78) — the opposite direction from
what the document's own explanatory heuristic anticipates ("the φ_U(c'')
value used for the touched state is itself too low … a second-order effect
not modeled," implying they expected touched > φ_U(c'')). This plausibly
connects to the *already-flagged, still-open* long-cycle deficit (§9 open
item 1) rather than being a separate phenomenon, but a full account is out
of scope here.

**Assessment.** I cannot rule out a genuine implementation difference
between my engine and `sc_diagnostic.py` (which I did not read, by mandate),
but three independent lines of evidence — two fresh Monte Carlo seeds
agreeing with each other, and a hand-corrected version of the document's own
theoretical model agreeing with both — triangulate on a value ≈3× the
document's reported figure for this one bin, at every tested cell, always in
the same direction. My own aggregate-level numbers (§2, §3.2) agree well
with the document's and with φ_REDB, which rules out a systematic bug in my
R/f/peeling construction. I read this as evidence that **the specific
percentages and z-scores `ATTEMPT.md` §3.1 reports for the near-b bins are
not stable, reproducible measurements** — the underlying statistic is
dominated by a small number of rare, high-leverage, cycle-level events
(effective sample size is closer to "number of qualifying cycles" — a few
hundred to low thousands — than to the raw point count), so between-seed
variance is much larger than either run's own internally-consistent
delta-method/bootstrap SE would suggest. This is a genuine finding, but it
does not undermine the document's own use of the result: §3.1 already
explicitly declines to adopt these figures as a validated formula ("reported
… as a qualitative, illustrative cross-check … no new formula is proposed
from it"), which in hindsight was the right call. I also could not
reproduce the document's own flagged target-cell "(500,2000] anomalous dip"
as a standout feature — my three independent measurements of the
(5b,20b]-equivalent region give −9.1%, −2.2%, and −11.8%, none clearly more
extreme than the neighboring plateau bin — consistent with the document's
own honest treatment of that specific point ("not explained here either …
flagged, not smoothed over"): independent replication suggests it is likely
within ordinary noise, not a robust standalone feature, which is exactly
the caution the document already exercised.

**Conclusion: Claim 3's qualitative shape is CONFIRMED, robustly. The
specific point estimates in §3.1's near-b bins are a named precision issue —
likely understated in the document by a factor of roughly 2–3× based on
independent triangulation — but this affects a sub-claim the document itself
already flags as illustrative-only, not a formula input, so it does not
change the verdict on the front's substantive claims.**

---

## 5. Claim 5 — scope and honesty audit

* `git status --porcelain` (run from the repo root, at review end): the only
  changed path is `05_DISCOVERY_LAB/.../short_cycle_dynamics_attempt/`
  (untracked, containing both the front's own files and this review's
  `adversarial/` subfolder). No other file in the repository shows as
  modified.
* File mtimes inside `short_cycle_dynamics_attempt/` (excluding this
  review's own `adversarial/` subfolder): `DERIVATION_PREREG.md` 13:35:50 →
  `sc_engine.py` 13:38:25 → `sc_engine_selftest.log` 13:38:34 (first
  simulation output) → … → `sc_red_cell5_target.log` 13:59:06 (last
  simulation output) → `ATTEMPT.md` 14:01:09 (written last). This is
  consistent with the document's own claimed ordering ("no functional form
  below was chosen after seeing T1 or T2's numbers") and with the
  pre-registration genuinely predating all computation.
* I checked the executive summary, §8, §9, and §10's verdict against the
  body with my own independently-measured numbers in hand and found no
  place where a claim is stated more strongly in the summary/verdict than
  the body supports. Specifically:
  - The "OPEN, not pursued" labeling of the persistent long-L deficit (§9
    item 1) is honest — I independently confirm the deficit is real,
    roughly the claimed size (§3.2/§4.1 above), and I found no explanation
    for it either.
  - The moderate-L excess is correctly labeled illustrative-only, not
    adopted as a formula (§3.1) — and, per §4.2 above, this caution turns
    out to have been well-placed: the specific numbers are less stable than
    they look, which the document's own hedging already anticipated in
    substance even though it did not anticipate this particular magnitude
    issue.
  - §10's verdict paragraph's claims (φ_REDC refuted on both conditions;
    U_{1/2} untouched; φ_REDB remains formula of record) all check out
    against my own independent numbers (§3 above, and the `n→∞` convergence
    check in §3.1).

**Conclusion: Claim 5 is CONFIRMED. No overclaim found, no scope violation
found.**

---

## 6. Errors and issues found, ordered by importance

1. **§3.1's near-b bin point estimates ((b,2b] and (2b,5b], all three
   cells) are not reproducible under independent re-measurement**, and
   appear understated by roughly a factor of 2–3× at the (b,2b] bin
   specifically (my two independent target-cell seeds: +874%/+796% vs. the
   document's +267.7%; consistent 1.3×–3.3× gap at all three cells; sign
   disagreement at the target cell's (2b,5b] bin). Traced to a genuine
   R^c-conditioning selection effect the document's own two-state
   back-of-envelope model under-weights (§4.2 above). **Does not threaten
   the front's central claims** — the document already treats these
   specific numbers as illustrative, not load-bearing, and the qualitative
   shape (and the far-tail plateau, which *is* used as evidence for the
   open item) reproduces cleanly.
2. **Minor: the φ_REDC vs. φ_REDB range** — I measure +1.05%…+6.23% across
   the 6-cell grid; the document reports +1.6%…+6.4%. Same direction, same
   rough size, does not affect any qualitative conclusion. Not investigated
   further given its immateriality to the refutation verdict (both ranges
   are uniformly positive on all 6 cells, which is the load-bearing fact).
3. No other error found. The mechanism (Claim 1), the su-bucket tautology
   (Claim 2's sanity check), the long-bucket sign/order-of-magnitude (Claim
   2), the φ_REDC refutation on both formula and formula-free grounds
   (Claim 4), and the scope/honesty audit (Claim 5) all independently
   confirm.

---

## 7. Scorecard

| claim | status | evidence |
|---|---|---|
| 1. Mechanism (untouched short cycle ⇒ deterministic f-cycle; touched ⇒ fully absorbed, unreachable) | **CONFIRMED**, 0/2,653,644 violations (2.2× target scale) | `adv_mechanism.py`, `adv_engine.py` §T0 |
| 2. T1 su-bucket tautology (φ=1 exactly) | **CONFIRMED**, exact, 3 cells, 0 violations | `adv_diagnostic.py` |
| 2. T1 long-bucket deviation from φ_U(c'') | **CONFIRMED**, same direction, comparable magnitude, 3 cells | `adv_diagnostic.py` |
| 3. L-binned qualitative shape (positive-then-negative-plateau) | **CONFIRMED**, robustly, even stronger at the near-b peak | `adv_diagnostic.py`, `adv_diag_bootstrap.py` |
| 3. L-binned near-b point estimates (magnitude/sign of specific bins) | **NAMED ISSUE** — not reproducible, ~2–3× gap, mechanistically explained | `adv_diag_bootstrap.py`, `adv_diag_decompose.py` |
| 4. φ_REDC refuted (formula self-check) | **CONFIRMED**, uniformly wrong-signed, 6/6 cells | `adv_formula.py` |
| 4. φ_REDC refuted (formula-free reduction, pre-registered criterion) | **CONFIRMED**, criterion fails on both conditions | `adv_reduction.py` |
| 5. Scope discipline (nothing else touched) | **CONFIRMED** | `git status`, file mtimes |
| 5. Pre-registration predates computation | **CONFIRMED** | file mtimes |
| 5. No overclaim in summary/§8/§9/§10 vs. body | **CONFIRMED** | manual audit against own numbers |

---

## 8. Files produced by this review (all in `short_cycle_dynamics_attempt/adversarial/`)

| file | role |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `adv_engine.py` / `adv_engine_selftest.log` | own from-scratch M-CLUST(b) engine (π, seeds, R, f, in-degree-peeling cyclic mask, exact π-cycle lengths via `scipy.sparse.csgraph.connected_components`); own T0-style selftest |
| `adv_mechanism.py` / `adv_mechanism.log` | Claim 1 large-scale stress test, 5 cells including 2 adversarial edge cells, 2.65M short-cycle points, 0 violations |
| `adv_formula.py` / `adv_formula_selfcheck.log` | own closed forms: φ_U (cross-checked vs. `scipy.integrate.quad`), T_U, φ_REDB, the exact short-cycle combinatorics (S_untouched, P(R^c), w_short), φ_cond_C, φ_REDC |
| `adv_diagnostic.py` / `adv_diagnostic.log` | Claim 2/3 — T1 diagnostic split + L-binned structure, 3 cells, multiprocessing across 4 workers, delta-method ratio SEM |
| `adv_diag_bootstrap.py` / `adv_diag_bootstrap.log` | fresh independent re-run of the target cell's L-bins (N=4000) with cluster-bootstrap SE cross-check |
| `adv_diag_decompose.py` / `adv_diag_decompose.log` | untouched-vs-touched decomposition of the near-b bins, target cell, isolating the mechanism behind the near-b excess magnitude |
| `adv_reduction.py` / `adv_reduction.log` | Claim 4 — own formula-free 6-cell reduction test, no formula on the measurement side |
