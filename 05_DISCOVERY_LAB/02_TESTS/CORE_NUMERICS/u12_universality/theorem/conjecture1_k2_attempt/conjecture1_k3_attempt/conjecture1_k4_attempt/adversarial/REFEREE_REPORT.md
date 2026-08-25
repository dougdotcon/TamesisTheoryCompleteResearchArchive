# Adversarial referee report — `conjecture1_k4_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent review of the claim `f_{M_4}(x) =
> 8x(1-x^2)^3` (`THEOREM.md` §8 Conjecture 1 at `K=4`). This is the
> **second consecutive surprising closure in this exact lineage**: `K=3`
> closed against an explicit combinatorial-explosion prediction (wave 15,
> verdict SOUND), and now `K=4` claims full closure against the `K=3`
> document's own explicit "genuinely open question, not attempted"
> framing. This report's job was therefore not to spot-check numbers but
> to actively hunt for the flaw that would explain why this "shouldn't"
> have worked twice — including a deliberate search for a **systematic
> error inherited across the lineage** (something subtly wrong in the
> shared method that would produce self-consistent but wrong answers at
> every `K`), attacked via surfaces that share none of the lineage's
> continuum machinery.

> **Standing discipline.** No script belonging to the front under review
> (`derive_lemma1_k4_symbolic.py`, `enumerate_destination_combinatorics_k4.py`,
> `mechanism_check_k4.py`, `derive_step2_k4_symbolic.py`,
> `r3_k3_reduction_check.py`, `discrete_k4_full_distribution_mc.py`, or
> any `mc_*.py` in that directory) was read at any point — nor were the
> front's `.log`/`.json` outputs (the only exception: a mechanical,
> content-blind extraction of seed *tokens* for the governance check in
> §8 below). Every check was built from scratch, from the documents'
> *prose* only, with fresh code and fresh derivations. The `K=2`/`K=3`
> documents and their referee reports were read for context, as the
> dispatch permits. Seeds used the referee-reserved range `20260851000+`
> (confirmed clean by `grep -rn "20260851"` before first use — the only
> prior hits were the two reservation lines in `DECISION_LEDGER.yaml`
> and `TEST_QUEUE.yaml`). No git command beyond read-only `git status`
> was run; `ATTEMPT.md`, `THEOREM.md`, and all governance files are
> untouched — only new files were written, all under this `adversarial/`
> directory.

---

## Verdict

> **SOUND — ACCEPT for catalogue.**

After an intentionally adversarial, from-scratch reconstruction of every
major claim — Lemma 1's full `Bell(4)=15`-pattern case split (all 15
patterns derived individually by a different method, not just the 5
grouped shapes), the `n=4` labeled-spacings Dirichlet fact by two
independent routes, the three-peel residual usage, the 625→12
classification, the off-cycle weight `W_C(Q)=1-Q` by my own enumeration
for every `n_off≤4`, the per-`r` density formula re-derived by hand and
symbolically evaluated, a **new raw-625 exact-moment surface** that uses
none of the document's collapse machinery, a from-scratch discrete
mechanism check with an added `n=12` stress scale (0 mismatches in
110,000 trials, all 625 cells hit at all three scales), an 8,000,000-
sample continuum Monte Carlo with per-group *and* per-cycle-type KS
tests, a raw large-`n` discrete simulation including a scale the front
never ran (`n=40000`), and the `K=3`/`K=2` reduction checks —
**no mathematical error was found anywhere in the document.** Every
independent re-derivation reproduces the document's numbers exactly
(symbolic) or passes cleanly (statistical, no rejection anywhere). One
carried-over cosmetic exposition note is named in §9; it is not an
error and does not affect soundness.

On the specific "two consecutive surprises" concern: the surprise
dissolves under scrutiny for an identifiable structural reason, which
the document itself now names precisely and which this review confirmed
independently at each joint — (a) the per-shape Lemma-1 constants are
`∏(b_j−1)!`, whose sum over set partitions is *forced* to be `K!` by the
permutation/cycle-decomposition bijection (verified here for `K=2..6`);
(b) the density formula for an on-cycle set depends only on `r_on`,
never on the internal cycle structure (verified here not only
symbolically but *distributionally*, per cycle type — a test no prior
front ran); (c) the off-cycle weight collapses to `1−Q` because the
weighted-forest closed form `E(E+Q)^{n_off−1}` degenerates at `E+Q=1`
(verified here by my own brute-force enumeration through `n_off=4`, one
case beyond what `K=4` needs). None of these three joints has any
`K`-specific content up to the verified ranges, which is *why* two
consecutive closures happened without anything being wrong.

---

## 1. Lemma 1 (K=4) — full independent re-derivation

**The single highest-risk piece** (three sequential residual peels — one
more than `K=3`'s maximum, and exactly where the document caught its own
Route-B scale-confusion bug) got the most scrutiny.
Script: `indep_lemma1_k4.py` / `.log`.

**1.1 All 15 co-block patterns, derived individually** by a clean
sequential Bayes/event-probability route (the `K=3` referee's style —
*not* the document's change-of-variables machinery), with the peeling
bookkeeping made explicit: block anchors contribute
`R·(1/R)=1` (landing-outside probability × residual length density —
the residual/size-biased citation, used once per new block, so **three
peels** for `1+1+1+1`); each non-anchor member contributes the
**absolute** membership probability `ℓ_j`; each block's labeled gaps
contribute `(b_j−1)!/ℓ_j^{b_j−1}`. Every one of the 15 patterns comes
out a **constant** on `Δ_4` (all `ℓ`-dependence cancels symbolically),
equal to `∏(b_j−1)!`, grouped `6+8+3+6+1 = 24` — the document's table
exactly. Because all 15 were computed individually, the document's
exchangeability grouping (one representative per shape) is confirmed
*concretely for every pattern*, strictly more than the document's own
two-route spot check.

**1.2 The Route-B bug, reproduced.** Substituting the erroneous
rescaled-residual probability `ℓ_2/(1−ℓ_1)` into my own route yields
exactly the `ℓ_1`-dependent `2/(1−ℓ_1)^2` the document reports its
first Route B produced, and the correct absolute probability `ℓ_2`
yields the constant `2`. The document's diagnosis of its own bug is
accurate, and the fix is the mathematically correct one — the absolute
vs. rescaled distinction is forced by `x_3,x_4 ~ Unif(0,1)` on the
whole interval.

**1.3 The `n=4` labeled circular spacings fact — the genuinely new K=4
machinery — verified two independent ways:** (a) the direct 6-ordering
construction: for each cyclic ordering of the three free points the gap
map is triangular with unit Jacobian onto the *full* open simplex, so
the labeled-gap density is `6/ℓ^3 = 3!/ℓ^3`, i.e. `ℓ·Dirichlet(1,1,1,1)`;
(b) an ordering-free brute-force check: all 35 mixed moments
`E[g_2^a g_3^b g_4^c]`, `a+b+c ≤ 4`, computed by direct symbolic
integration over the free points' uniform positions, match the
`Dirichlet(1,1,1,1)` moments exactly (with the `n=2`/`n=3` cases — the
`K=2`/`K=3` facts — re-checked as regressions).

**1.4 The three-peel citation usage, checked explicitly.** My
derivation needed the residual property exactly three times for the
`1+1+1+1` pattern (`ℓ_1→ℓ_2→ℓ_3→ℓ_4`) and fewer for every other
pattern — literally the multi-step GEM(1)/stick-breaking representation
(the residual after removing finitely many size-biased picks is again
fresh rescaled `PD(1)`). The same citation `K=2` used once and `K=3`
twice, used the number of times the construction calls for; not a new
or weaker link.

**1.5 The `∏(b_j−1)!` / `K!` identity**, checked by my own enumeration
for `K=2,…,6` (`2, 6, 24, 120, 720`) — two values beyond the document's
own range. The identity is exactly the permutation ↔ (set partition +
per-block cyclic order) bijection, as claimed.

**1.6 Per-pattern probabilities, independent route.** Each of the 15
patterns' probabilities computed by iterated symbolic integration over
the peeling variables (never touching the density claim): each equals
`∏(b_j−1)!/24` and all 15 sum to exactly `1` — the self-consistency
check that would catch a wrong constant even if it canceled in the
density total.

**1.7 Independent discrete-permutation simulation of Lemma 1**
(`indep_discrete_checks_k4.py` Check A, my own region-assignment
routine, seeds `20260851020/021/022`, scales `n=300/1000/5000`): all
moments match (`E[m_i]→1/5`, `E[m_1^2]→1/15`, `Cov→−1/150`, worst
`|z|=1.96` across 12 moment tests); KS of `L=Σm_i` vs `t^4`, pooled
`m_i` vs `Beta(1,4)`, `m_1+m_2` vs `Beta(2,3)`, and exchangeability all
pass at `n=1000, 5000` (`p` from `0.12` to `0.80`). At `n=300` the KS
tests on `L` and the pooled marginal reject (`p=0.003, 0.000`) — the
**identical small-`n` discretization-bias signature** the document
reports at its own `n=300` and that both prior referees confirmed and
explained; converging cleanly with `n` exactly as a genuine continuum
limit must.

**Conclusion: Lemma 1 (K=4) fully confirmed — joint density exactly
`24` on `Δ_4` — including the one genuinely new fact (`n=4` spacings),
the third peel, and the per-pattern constants, by methods sharing
nothing with the document's own derivation.**

## 2. The 625→12 destination combinatorics and the assembly — full independent re-check

Script: `indep_shapes_k4.py` / `.log`. The orchestrating session had
already independently verified the classification, `W_C`, the
`Σ∏(b_j−1)!` identity, the five per-`r` densities via its own
marginalization, the group probabilities, and the final sum. This
review re-did all of that by *different* routes and extended it to
surfaces nobody had checked:

**2.1 Fresh classification** (third implementation): all 625 raw
`g:{1,2,3,4}→{1,2,3,4,OUT}` maps classified with my own cycle
detection. Per-`r_on` raw counts `125/200/180/96/24` (sum 625), exactly
**12 shape types** with per-`r_on` counts `1,1,2,3,5` (the partition
numbers — the document's pre-registered prediction), and per-type raw
counts (`90+90` at `r=2`; `16+48+32` at `r=3`; `1+6+3+8+6` at `r=4`)
all reproduced. `N(r_on,n_off)` constancy across every specific subset
and cycle-permutation choice confirmed (`125,50,15,4,1` — singleton
value sets), **plus an analytic cross-check the document doesn't state:
`N = (r+1)(r+1+n_off)^{n_off−1}`, the labeled-forest count, matches all
five.**

**2.2 Off-cycle weight `W_C`, my own enumeration.** For
`n_off=1,2,3,4`: summing the product of target masses over all
off-target assignments that create no cycle inside the off-set (my own
cycle rejection, `1/3/16/125` valid assignments) gives **exactly**
`e·(e+Q)^{n_off−1}` as a polynomial identity in the symbolic masses,
hence `1−Q` at `e=1−Q`. This covers `n_off=3` (the case exceeding
`K=3`'s maximum — the crux new ingredient) *and* `n_off=4`.

**2.3 The per-`r` density formula, re-derived by hand.** I re-derived
the document's §4 display from first principles by a route I built
myself: fix `C` and a cycle permutation `σ`; the change of variables
`m_j = D_j + P_{σ^{-1}(j)}` (unit Jacobian) makes the joint density of
`({P},{D},\text{off})` equal `24(1−Q)` on a domain **independent of
`σ`** — which is the precise reason the `r!` collapse and the
"depends only on `r_on`" phenomenon are correct — and marginalizing
(`D`-simplex volume `x^r/r!`, `s=ΣP` surface `s^{r-1}/(r-1)!`, `Q`
surface `Q^{n_off-1}/(n_off-1)!`) reproduces the document's integral
formula term for term. Evaluating it exactly reproduces all four
claimed polynomials `r=1..4`; `r=0` reproduced via **two** routes
(forest weight × `OUT ~ Beta(1,4)` density, and a literal brute-force
sum over the 125 no-cycle configs — which also confirmed
`P_{T0}(m) = 1−Σm` identically as a polynomial). Group integrals
`1/5, 2/5, 2/7, 1/10, 1/70` (sum `1`); total **exactly**
`8x−24x^3+24x^5−8x^7 = 8x(1−x^2)^3`; `∫f=1`, `E[M_4]=128/315` (equal to
the §5.2 Wallis value `4^K(K!)^2/(2K+1)!` at `K=4`), `E[M_4^2]=1/5`,
`E[M_4^3]=128/1155` — all exact matches.

**2.4 Per-`r` probabilities via a second independent route** — direct
symbolic simplex integration of my own `P(r_on=r \mid m)` polynomials
(built from my own classification, weight `m_{g(i)}` per on-cycle node,
raw off weights, Dirichlet monomial formula): `1/5, 2/5, 2/7, 1/10,
1/70` again, sum `1`.

**2.5 Sub-shape (cycle-type) probabilities — a check no prior front
ran.** The theory forces, within each `r_on`, every specific cycle
permutation `σ` to carry equal probability, so each cycle type's
probability must be `P(r_on)·(\#\text{perms of that type})/r_on!`. All
11 non-trivial `(r_on, \text{cycle type})` probabilities, computed by
exact symbolic integration, match this prediction exactly (e.g.
`(4,(3,1)) = 1/210`, `(4,(1^4)) = 1/1680`).

## 3. The raw-625 exact-moment surface — a new, machinery-free symbolic check

Script: `indep_raw625_moments_k4.py` / `.log`. To attack the
possibility that the *collapse machinery itself* (shape grouping,
`σ`-independence, `W=1−Q`, the change of variables, the per-`r`
formula) harbors a self-consistent systematic error, I computed the
exact per-group moments `E[M^p \, 1\{r_{on}=r\}]` for `p=0..8` **from
the raw 625 configurations directly** — for each of the 65 `(C,σ)`
classes, raw off-target weight sums (no closed form assumed), exact
nested `P`-integrals, exact Dirichlet-formula simplex integration —
using none of the machinery listed above. All `5×9 = 45` per-group
moments and all 9 totals match the claimed five polynomials and
`8x(1−x^2)^3` exactly (`E[M]=128/315`, `E[M^2]=1/5`, `E[M^3]=128/1155`).
Since each claimed `f_r` has degree ≤ 7, matching moments `p=0..8`
leaves no room for any competing polynomial density — combined with §5's
KS tests, no room for any competing density at all.

## 4. Discrete mechanism check — independently rebuilt from scratch

Script: `indep_discrete_checks_k4.py` Check B (seeds
`20260851001/002/003`). Entirely independent simulator: my own
ground-truth color-marking orbit tracer (**cross-validated against a
naive `f^t`-iteration oracle on 3,000 trials at `n=12`** — zero
disagreements), my own region/distance assignment, my own prediction
derived from first principles (`M_{pred} = \#\text{OUT} + Σ_{i\in
\text{cyc}(g)}(D_i+1)`, with the `(D+1)`-points convention derived
before any code ran — the arc from `u_i` to `x_{g(i)}` inclusive at
both ends):

```
n=12,  trials=30000: mismatches=0  cells hit=625/625  collisions=12861  fixed-points=8871
n=25,  trials=60000: mismatches=0  cells hit=625/625  collisions=13184  fixed-points=9112
n=150, trials=20000: mismatches=0  cells hit=625/625  collisions=785    fixed-points=525
TOTAL: 0 mismatches / 110,000 trials
```

The added `n=12` scale (not run by the front) stresses collisions
(43% of trials) and fixed points (30%) far past the document's own
densities, and hits all 625 raw cells at *every* scale, not just
overall. The mechanism — off-cycle contributes zero regardless of
target; on-cycle members contribute exactly their `(D_i+1)`-point arcs;
sourceless `π`-cycles stay cyclic — is exact per configuration.

## 5. Per-group conditional densities — large independent continuum MC

Script: `indep_continuum_mc_perr_k4.py` / `.log` (seed `20260851030`,
`N=8{,}000{,}000`, vectorized, a fourth classification implementation).
Per-`r_on` group fractions: all `|z| ≤ 2.07` (5 tests, unremarkable).
**KS of each group's empirical `M_4` against the document's claimed
conditional closed form** (exact CDFs built by `Fraction` integration
of the polynomials as transcribed from the document's §4 table):

```
r=0: n=1,598,667  KS p=0.80      r=1: n=3,198,545  KS p=0.97
r=2: n=2,288,324  KS p=0.86      r=3: n=  799,484  KS p=0.35
r=4: n=  114,980  KS p=0.34
overall: KS p=0.45   mean=0.406393±0.000066 vs 128/315 (z=+0.67)
```

**All five pass cleanly.** Additionally — the distributional version of
the `σ`-independence claim, never tested by any front: within each
group, every cycle type's sample was KS-tested against the *group* law
(10 tests: e.g. `(2,2)` vs `(4,)` at `r=4` must be indistinguishable in
law). All pass (worst `p=0.065` across 10 tests, unremarkable), and all
cycle-type fractions match the `\#\text{perms}/r!` prediction
(`|z| ≤ 0.81`).

## 6. Raw large-`n` discrete simulation — the anti-lineage-systematic-error surface

Script: `indep_full_discrete_mc_k4.py` / `.log` (seeds
`20260851010/011/012`). The strongest independent surface: genuine
uniform permutations, 4 reroutes, true cyclic count via **pointer
doubling** (a fourth cyclic-set algorithm, itself self-tested against a
naive oracle on 200 random functional graphs) — no `PD(1)`, no
Lemma 1, no regions, no shapes, no formulas anywhere in the pipeline:

```
n=10000, trials=4000: KS D=0.01011 p=0.8040  mean=0.406888±0.002984 (z=+0.18)
n=20000, trials=2000: KS D=0.01684 p=0.6156  mean=0.401919±0.004158 (z=-1.07)
n=40000, trials=1200: KS D=0.01401 p=0.9700  mean=0.405662±0.005301 (z=-0.13)
```

All three scales pass KS against `F(x)=1−(1−x^2)^4` with no rejection;
`n=40000` is a scale the front never ran — a genuinely new point on the
convergence curve, and it is the *cleanest* of the three. If the
lineage's shared continuum machinery had a self-consistent systematic
error, this surface is where it would have surfaced; it did not.

## 7. Reduction checks (R2) and the two disclosed bugs

Script: `indep_reduction_checks.py` / `.log`.

**7.1 K=3 reduction, group by group.** My own general `K`-parametrized
formula at `K=3` reproduces the `K=3` document's already-reviewed
per-group densities exactly (`r=0..3`), agrees row-for-row with the
`K=4` document's §5 comparison table, and sums to `6x(1−x^2)^2`. My
classification also reproduces `K=3`'s 64→7 collapse and raw counts.
**K=2 reduction:** same, reproducing `4x(1−x^2)` group by group.

**7.2 §2's scale-confusion bug (Route B):** verified fixed — see §1.2;
the erroneous form provably fails the constant-density requirement and
the corrected form is what my independent route derives. Nothing of the
bug survives in any final claim (the final constants are confirmed by
my all-15-pattern derivation and by the discrete Lemma-1 MC).

**7.3 §5's `sympify` fresh-symbol bug:** the pitfall is real and
behaves exactly as the document describes — I reproduced it
(`sympify("...")` yields `Symbol('x')` with no assumptions, distinct
from `Symbol('x', positive=True)`; the difference does not cancel and
`srepr` shows two distinct symbols). It was a bug in the front's
*comparison harness*, not in any mathematical claim, and the corrected
group-by-group comparison is independently confirmed by §7.1 (my
comparison never uses string `sympify`). Nothing survives into final
claims.

## 8. Governance spot-checks

- **Seed discipline:** a content-blind token extraction over the
  front's files finds only `20260850000–20260850030` seed tokens
  (matching its declared seeds table) plus range-boundary mentions;
  **no referee-range (`20260851xxx`) token appears in any front file.**
  My own seeds used only the referee range.
- **Timestamps:** `DERIVATION_PREREG.md` (17:14Z) predates every
  script/log (17:18Z–17:28Z) and `ATTEMPT.md` (17:32Z), consistent with
  §0's pre-registration claim; the 12-shape/`Σp(s)` prediction indeed
  appears in the prereg.
- **`git status` (read-only):** only untracked `adversarial/`
  directories; no tracked file modified by this review or by the front.

## 9. Named issues

**One carried-over, non-substantive exposition note** (not an error):
the `K=4` document's §3 restates the "off-cycle contributes zero" proof
in the same compressed form the `K=3` referee flagged (`K=3` report §6)
— the sub-case of an off-cycle redirect landing *inside* an
already-periodic arc is again not spelled out, the document instead
deferring to the `K`-independence of the lineage argument. The parent
`K=3` document now carries the post-adversarial correction note tracing
that sub-case explicitly, the claim is `K`-independent and true, and
this review's 110,000-trial per-configuration mechanism check (with a
collision/fixed-point-saturated `n=12` scale) confirms it exhaustively
at `K=4`. Optional cosmetic fix: one sentence in §3 pointing at the
`K=3` document's post-adversarial note. Does not affect soundness.

No other issue was found. In particular:

- Both self-disclosed bugs (§7.2, §7.3 above) are accurately described,
  genuinely fixed, and leave no trace in final claims.
- The `K≥5` scope disclaimer is accurate and not overstated; the
  weighted-forest explanation is correctly labeled informal/OPEN. (As a
  referee-side probe, not part of this verdict: my general formula at
  `K=5` sums to `10x(1−x^2)^4`, and my own enumeration already verifies
  `W=1−Q` at `n_off=4` — so the document's proposed future-front lead
  is well-posed; what would remain for `K=5` is Lemma 1 at `K=5` and
  `W` at `n_off=5`.)
- The executive summary's "PROVED modulo one classical citation"
  framing is accurate: the citation is used legitimately (three peels
  are literally the multi-step stick-breaking representation, §1.4),
  and every other step is exact combinatorics/symbolic integration,
  independently reconstructed here.
- Every headline number in the document that this review could test
  independently (constants, counts, polynomials, probabilities,
  moments, and the qualitative small-`n` KS signature) reproduced
  exactly or within ordinary statistical fluctuation; ~34 statistical
  tests were run in this review and none rejected at scale (the only
  sub-0.01 p-values are the two *expected* `n=300` discretization-bias
  signatures, which converge away by `n=1000`).

## 10. What this review did not attempt

A fully symbolic piecewise re-derivation of each per-`r` closed form by
direct `x`-space integration (the `K=2`-style by-hand route) was not
carried through; instead the raw-625 exact-moment route (§3) was used —
it is *stronger* than a piecewise re-derivation for error-detection
purposes (it is exact, exhaustive over configurations, and
machinery-free) and, combined with the 8M-sample per-group KS tests
(§5), leaves no residual polynomial or non-polynomial alternative
consistent with the data. Lemma 1 at `K≥5` and `W(n_off≥5)` were not
examined beyond the probe noted in §9, since the document claims
nothing there.

## 11. Files in this directory

| File | Role |
|---|---|
| `indep_lemma1_k4.py` / `.log` | §1: all-15-pattern Bayes re-derivation of Lemma 1, Route-B bug reproduction, `n=4` Dirichlet fact (2 routes), per-pattern probabilities, `∏(b_j−1)!/K!` identity `K=2..6` |
| `indep_shapes_k4.py` / `.log` | §2: fresh 625-classification, `N(r,n_off)` + forest-count cross-check, `W_C` enumeration `n_off=1..4`, per-`r` formula evaluation, `T0` two routes, probabilities two routes, sub-shape probabilities, final sum + moments |
| `indep_raw625_moments_k4.py` / `.log` | §3: machinery-free raw-625 exact per-group moments `p=0..8` |
| `indep_discrete_checks_k4.py` / `.log` / `_results.json` | §1.7 (Check A: Lemma 1 discrete MC) and §4 (Check B: mechanism check, 3 scales incl. `n=12` stress, oracle-validated tracer) |
| `indep_continuum_mc_perr_k4.py` / `.log` / `_results.json` | §5: 8M-sample continuum MC, per-group KS + sub-shape law tests |
| `indep_full_discrete_mc_k4.py` / `.log` / `_results.json` | §6: raw large-`n` discrete simulation, pointer-doubling ground truth, incl. new `n=40000` scale |
| `indep_reduction_checks.py` / `.log` | §7: K=3/K=2 reductions, K=5 probe, `sympify` pitfall confirmation |
| `REFEREE_REPORT.md` | this report |

Seeds used (referee-reserved range `20260851000+`, confirmed clean
before use): `20260851001, 20260851002, 20260851003, 20260851010,
20260851011, 20260851012, 20260851013` (oracle self-test),
`20260851020, 20260851021, 20260851022, 20260851030`.

---

**Summary.** `THEOREM.md` §8 Conjecture 1 at `K=4` — `f_{M_4}(x) =
8x(1−x^2)^3` — is **SOUND**, modulo the same `PD(1)` residual/
size-biased citation the already-accepted `K=1,2,3` line relies on
(here used three times, a use this review verified is the standard
multi-step stick-breaking representation, not an extrapolation). Every
step was independently reconstructed from scratch: Lemma 1 at full
15-pattern granularity including its two genuinely new ingredients (the
`n=4` labeled-spacings fact and the third peel), the 625→12 collapse,
the off-cycle weight through `n_off=4`, the per-`r` densities by two
independent exact routes (one of which uses none of the lineage's
collapse machinery), the discrete mechanism at per-configuration
exactness, the continuum recipe distributionally at per-group and
per-cycle-type granularity, the raw discrete model at three large
scales including one the front never ran, and both reduction checks.
The hunted-for inherited systematic error does not exist on any surface
this review could reach. **ACCEPT for catalogue** into `THEOREM.md` at
the archive's next appropriate stage label, with the one named cosmetic
exposition note (§9) optionally addressed at the integrating editor's
discretion.
