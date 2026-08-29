# REFEREE REPORT — `GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`

**Target:** `.../diagonal_2f0_sum_attempt/route2_bypass_attempt/joint_saddle_point_attempt/ATTEMPT.md`
(Wave 31, front (b), `GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`, authorized by
`DISC-DEC-142`)

**Referee:** hostile, independent adversarial session. Read, in full and in
prose, in the order specified by the dispatch mandate, before opening any
script belonging to the target: `gamma_scaling_attempt/ATTEMPT.md` (592
lines, wave 17, ultimate ancestor); `gamma_second_order_attempt/ATTEMPT.md`
(632 lines, wave 18, Lemma E / Lemma D0); `gamma_c_gamma_construction_
attempt/ATTEMPT.md` (642 lines, wave 28 front b); `diagonal_2f0_sum_
attempt/ATTEMPT.md` (500 lines, wave 29 front b, §3/§4 for the local rate
`c(γ)=2(1-γ)/γ`); `route2_bypass_attempt/ATTEMPT.md` (593 lines, wave 30
front a, immediate predecessor, in full, esp. §2/§3/§4/§5/§8) and its
`adversarial/REFEREE_REPORT.md` (367 lines, esp. item (d), the Beta-integral
Pfaff derivation); `THEOREM.md` Estágios 26, 51, 52, 54 in full. Only after
all of that was the target's own `ATTEMPT.md` and its five scripts
(`01`–`05`) read.

Pure combinatorial/asymptotic mathematics internal to this archive, about a
specific random-permutation-with-reroutes ensemble — no Millennium Prize
Problem, no physics claim, anywhere in this document, its target, or any of
its ancestors.

---

## VERDICT: **SOUND WITH ISSUES — ACCEPT for catalogue, with two named
## corrections.** Claims 1–3 (the exact `t*` quadratic, the mesoscale
## profile `T_prof`, and its non-circular reproduction of `G_n`'s
## coefficient) are genuinely sound and were independently re-derived here
## via routes stronger than, and largely disjoint from, the target's own.
## Claim 4 (the `c(γ)/2`-to-`A(γ)` "crossover") contains a real, checkable
## error: the claimed near-origin value is wrong, both as an arithmetic
## illustration and as a description of the target's own printed data. A
## second, independent quantitative claim (`<0.7%` agreement for `λ≤1.0`)
## is also contradicted by the target's own log. `C(γ)` remains, correctly,
## entirely OPEN.

The mathematical core of this front — clearing denominators to get an exact
quadratic for the inner Beta-integral saddle `t*`, and a genuine two-level
Laplace-on-`t` + Stirling-on-`m` derivation of the mesoscale limit profile
`T_prof(λ,γ)` — was re-derived here **completely independently**, using a
methodologically *stronger* route than the target's own (an exact `lgamma`
difference throughout, rather than the target's leading-order `(2m+1)ln n`
shortcut for the binomial-shift term) and landed on the **identical** closed
forms. This is a substantive, non-trivial confirmation, not a restatement.
Two real issues were found in the document's own descriptive/summary prose,
both traceable directly to the front's own disclosed logs — neither
threatens the core results, but both need correction before this document
is treated as a clean record.

---

## Independent verification, item by item

### (a) Claim 1 — the exact quadratic and closed form for `t*(n,m,γ)` (§3, script `02`)

Re-derived fully symbolically from scratch (own `sympy` code, `ref01` Part
1): `g'(t)`'s numerator, cleared of denominators, gives the identical
quadratic `γ(m+n)t² − (2m+γn)t + m = 0` and the identical closed-form root.
**Beyond** the target's own verification (numerical golden-section
cross-check at 18 points), this review supplies a genuine **non-numerical
proof of global optimality**: each of `g(t)`'s three additive terms
(`m ln t`, `m ln(1−t)`, `(n−m)ln(1−γt)`) is individually strictly concave on
`(0,1)` for `γ∈(0,1)`, `0≤m≤n` (confirmed symbolically, `ref01`), so `g` is
globally concave, `g'` is strictly decreasing, and the unique critical point
found is automatically the *global* maximizer — not merely a point
satisfying `g''(t*)<0`, which only certifies a local max. **PROVED,
independently reconfirmed and strengthened.**

### (b) Claim 2 — the mesoscale profile `T_prof(λ,γ)` (§4, script `03`) — deepest-scrutiny item

Re-derived the full `ln(term_m)` combination from scratch (`ref01` Part 2),
using the **exact** `lgamma` difference `ln[(n+m+1)!]−ln[(n−m)!]` throughout
instead of the target's own leading-order `(2m+1)ln(n)` approximation for
this piece — a strictly more rigorous route, since it removes one possible
(if ultimately harmless, see below) source of hidden error from the
target's own derivation. Substituting `n=m²/λ²` and taking the `m→∞` limit
(`sympy.series`, independently written) gives, symbolically, **exact zero
difference** from the target's claimed closed form
`T_prof(λ,γ)=(1/γ)exp[−(2−γ)λ²/(2γ)]`.

Independently confirmed this is not a `sympy`-series artifact via a
**second, direct high-precision numeric route** (`ref01` Part 3, `mpmath`
`mp.loggamma`, no series machinery at all): the exact asymptotic combination
converges **cleanly and monotonically** to the closed form as `m→∞`, checked
at `m` up to `10^{10}` (and, in preliminary exploration, up to `10^{14}`) at
six `(λ,γ)` points **including `λ=2.0`, wider than anything the target
itself tested** (target's own grid stops at `λ=1.5`). Convergence is
clean `O(1/m)`-looking at every point, no anomalies.

**This independently confirms claim 2 is genuinely correct** as an
asymptotic statement — not merely "the target's `sympy.series` call did
what the document says" (which was this review's explicit mandate to
check), but "the claimed limit is the actual, correct `m→∞` limit of the
Laplace/Stirling combination, confirmed via a materially different and more
rigorous computational route landing on the identical answer."

**However**, a genuine issue was found in the *numerical validation* of
this claim (not in the closed form itself — see item (c) below).

### (c) The `<0.7%`-for-`λ≤1.0` numerical claim (§4) — CONTRADICTED by the target's own log — **correção**

ATTEMPT.md §4 states: *"the general closed form matches the
Richardson-extrapolated value to `<0.7%` for `λ≤1.0`, `<1.6%` at `λ=1.5`."*
The target's own `03_saddle_value_expansion.log` contains the line:

```
lambda=0.6 gamma=0.3: predicted=1.201983134  numeric(Richardson)=1.214728583  rel.err=0.0104924
```

**`1.05%`, which exceeds the claimed `<0.7%` bound for `λ≤1.0`.** This is
not a subtle misreading: `λ=0.6 < 1.0`, and `0.0104924 > 0.007`. Confirmed
by direct re-parsing of the log (`ref04` Part 1).

Independently re-implemented the target's exact `term_m` evaluator and its
own repeated (2×, squared) Richardson procedure from scratch (`ref04` Part
2, own code): **reproduces the target's residual almost exactly**
(`1.046%` here vs. `1.049%` reported — the small difference is quadrature
window-width tuning, not a different fact). This is not a transcription
error in the log; it is a real, reproducible feature of the target's own
extrapolation pipeline at this specific point.

**Diagnosis (this review, not attempted by the target for this point).**
The *raw*, non-extrapolated relative error at `(λ,γ)=(0.6,0.3)` shrinks
cleanly from `2.1%` (`n=4000`) to `0.074%` (`n=1{,}024{,}000`) — and a
*simple* single-stage 2-point Richardson using the two largest available
`n` already achieves `0.13%` agreement, an order of magnitude tighter than
the target's own repeated-Richardson estimate. This is consistent with the
`1.05%` discrepancy being an artifact of the *specific* repeated/
second-order Richardson procedure used (noise-amplifying at this
particular point) — **the same kind of diagnosis the target itself
reached, independently, for its own `λ=1.5` discrepancy** (via a direct
high-`n` push, its own self-caught issue §8 item 2) — **but this
due-diligence was not extended to the comparably-anomalous `λ=0.6` case**,
and the summary claim in §4/VERDICT was not corrected to reflect it.

**Severity: correção.** The specific quantitative claim needs correction
(e.g. to something like *"`<1.1%` for `λ≤1.0`, with `λ=0.6` the
worst-behaved point in the Richardson grid, plausibly extrapolation
artifact rather than closed-form error given the clean raw-error trend at
that point — not separately investigated with a direct high-`n` push the
way `λ=1.5` was"*). It does **not**, on the evidence gathered here (item
(b) above), indicate any flaw in the `T_prof` closed form itself.

### (d) Claim 3 — the `G_n`-coefficient reproduction is genuinely non-circular (§5, script `04`) — **CONFIRMED, both the identity and the "not circular" claim**

Re-derived `∫_0^∞ T_prof(λ,γ)dλ = ½√(π/β)` independently two ways
(`ref02` Part A): a by-hand Gaussian-integral substitution, and a
fresh `sympy.integrate` call — both give exact symbolic zero difference
from `G_n`'s coefficient (using a squared-both-sides argument to route
around a `sympy` branch-cut presentation artifact on `√(2−γ)` vs.
`√(−1/(γ−2))` — the same *class* of harmless `sympy` simplification
limitation the target's own script 04 self-caught and disclosed for the
identical integral). Confirmed at 5 fresh rational `γ` disjoint from the
target's own 6-point grid.

**The "not circular" claim was independently verified by direct file
inspection** (`ref02` Part B): grepped the target's own scripts `02`
(inner saddle) and `03` (`T_prof` derivation) for any occurrence of `G_n`,
`β`, or `T(γ)` — **zero occurrences in either file**. The derivation of
`T_prof` genuinely never references the object it is later shown to be
consistent with. This is a real, falsifiable, unforced consistency check
of the whole pipeline (Beta-integral → inner saddle → Stirling → outer
continuum limit), and it succeeds exactly. **This is independently
confirmed sound, and is fairly the front's strongest single result**, as
the target's own §11 scorecard already characterizes it.

### (e) Claim 4 — the `c(γ)/2`-to-`A(γ)` "local-rate crossover" (§6, script `05`) — **CONTAINS A REAL ERROR — correção**

This is the item this review scrutinized hardest, per the dispatch's
explicit instruction to check whether the reconciliation is "a genuine
resolution... not hand-waving." It is **not** hand-waving — but the
specific claimed near-origin value is **wrong**, in two compounding ways:

**(i) The illustrative arithmetic itself is wrong.** ATTEMPT.md §6 states:
*"e.g. `γ=1/3`: `c(γ)/2=1`, `A(γ)=2.5`."* Direct computation
(`ref03` Part 1): `c(1/3) = 2(1−1/3)/(1/3) = 4`, so `c(1/3)/2 = 2`, **not
`1`**. `A(1/3)=2.5` is correctly stated. This is a simple, checkable
arithmetic slip.

**(ii) More substantively: the target's own printed data does not show the
crossover "starting at `c(γ)/2`" at all.** The `05_local_rate_crossover.log`
(target's own file, quoted verbatim) shows, at `γ=1/3`, `n=4×10⁶`:

```
m=1 (lambda=0.0005): local curvature over [prev_m,m] = 4.000002
```

**This is `c(γ)=4.0`, not `c(γ)/2=2.0`.** Independently reproduced
(`ref03` Part 2, own code): the "local curvature" formula used in script
`05` Part B, `−n·log(term_m/term_{m−1})/(m²−prev_m²)`, reduces **by direct
algebraic construction** to exactly the Part A rate formula (`c(n,γ)`
itself) at the very first step, since `m²−prev_m² = 1²−0² = 1` there — this
is not a numerical coincidence, it is forced by the definition. No
subsequent value in the printed 11-point grid passes through or near
`c(γ)/2=2.0` either: the sequence at `γ=1/3` reads `4.0, 3.0, 2.75, 2.625,
2.51, 2.996(↑), 2.55, 2.502, 2.501, 2.501, 2.500` — starting at `c(γ)`,
decreasing (with one undisclosed non-monotonic bump at `m=32`, both `γ`
tested) toward `A(γ)=2.5`, never toward or through `2.0`.

Checked whether `c(γ)/2` corresponds to *any* other quantity computed
anywhere in the document (e.g. the self-caught planning note of §8 item 4,
which correctly diagnoses that naively substituting `m=1` into the
mesoscale Laplace formula predicts a rate of `A(γ)`, not `c(γ)`) — neither
the true exact near-origin value (`c(γ)`) nor the invalid-naive-substitution
value (`A(γ)`, per the target's own §8 item 4) equals `c(γ)/2` in general.
**No valid derivation or numerical demonstration of `c(γ)/2` as a
meaningful near-origin endpoint exists anywhere in this document.**

**What survives.** The genuinely solid content of claim 4 — that the local
curvature is *not* constant across the `m`-range, and that it converges
cleanly (`<0.1%` by `m∼500`–`3000`) to `A(γ)`, not to any extrapolation of
`c(γ)` — is real and independently reconfirmed here (item (b)/(d) above
independently establish `A(γ)` is exactly `T_prof`'s curvature). The error
is specifically in the claimed **near-origin endpoint label**
(`"c(γ)/2"`), which appears in the VERDICT (item 4), in §6's main prose,
and in script `05`'s own inline print statement/expectation comment — the
same wrong label in three places, none cross-checked against the script's
own printed output before finalizing the document.

**A smaller, undisclosed wrinkle noted in passing**: the crossover data
shows a non-monotonic bump at `m=32` (both `γ=1/3` and `γ=1/2`: the
curvature rises above its `m=16` and `m=64` neighbors) that is not
mentioned anywhere in the document, unlike the comparable `λ=1.5`/`m=0.9`
anomalies elsewhere in the front, which *are* disclosed and investigated.
Severity: **nota** — plausibly quadrature-window noise at that specific
`m`, does not affect the converged large-`m` conclusion, but the
document's "confirmed cleanly" framing (§6, VERDICT) slightly overstates
the grid's actual smoothness.

**Severity: correção** for (i) and (ii) together — a real, checkable
error in a claim that appears prominently in the VERDICT (one of the
front's four headline findings). Recommended correction: replace
`"starts at c(γ)/2 (m=O(1))"` throughout with something like `"starts at
c(γ) itself at the very first step (by construction), decreases through
several intermediate values, and settles onto A(γ) by m∼500–3000"`, and
fix the `γ=1/3` illustrative numbers.

### (f) Self-caught issues (§8) — accurately described, and fixes genuinely present

Checked each against the actual code, not merely re-read:
- Item 1 (golden-section threshold loosened `1e-30→1e-20`): confirmed
  present in `02_inner_saddle_exact.py` (assert `< mp.mpf('1e-20')`), with
  the disclosed reasoning consistent with the actual observed max error
  (`1.6×10⁻²⁶`).
- Item 2 (`λ=1.5` Richardson residual, resolved via direct high-`n` push):
  confirmed via direct log inspection (`03_saddle_value_expansion.log`),
  the disclosed numbers (`6.2%→4.1%→0.33%→0.73%→0.41%→0.25%→0.17%`) match
  the actual printed sequence to the precision quoted.
- Item 3 (quadrature failure fixed by seeding interior points at `t*±k·
  width`): confirmed present in both `03` and `05`'s `term_m_beta_robust`
  functions — the described mechanism (peak too narrow/off-center for
  default `mp.quad` node placement) is textbook-accurate for a Beta-type
  integral with `t*→0`.
- Item 4 (the `A(γ)`-vs-`c(γ)` "planning-stage concern," resolved by
  recognizing the Laplace/Watson formula is asymptotic *in* `m`): the
  *reasoning* in this item is independently confirmed correct by this
  review (item (e) above) — but see (e): the *resolution* as stated
  (invoking `c(γ)/2`) does not actually match what the "exact,
  non-asymptotic `term_m` formula" (script `05`) shows, which is the
  substance of the correção above.
- Item 5 (Laurent expansion of `g(t*)` alone diverges): the mechanism
  described (`t*∼m/(γn)→0` makes `m ln t*` contain an unbounded `m ln m`
  piece) is mathematically correct, consistent with this review's own
  derivation (item (b)).

**No other computational bugs found** in scripts `01`–`05` beyond the two
correções above.

---

## Overclaim/underclaim check

The VERDICT, §7, §10, and §11 (scorecard) were checked against each other
and against the independent re-derivations above.

- Claims 1–3 are labeled at the correct tier ("PROVED" for the quadratic/
  root, appropriately hedged "derived + independently numerically
  CONFIRMED — not a fully rigorous uniform bound" for `T_prof`, "PROVED"
  for the exact `G_n`-coefficient integral) — **accurate, not overclaimed**,
  and if anything item (a) above shows claim 1 is *stronger* than
  presented (global, not just local, optimality — an underclaim the front
  did not need to make but could have).
- Claim 4 ("numerically DEMONSTRATED at 2 γ, not proved uniformly," §11
  scorecard) is technically hedged correctly as a status *label*, but the
  accompanying *prose description* of what was demonstrated (§6, VERDICT
  item 4) is the locus of the correção in item (e) above — a genuine
  overclaim in the specific numeric characterization, not in the
  claimed proof tier.
- §7's itemized diagnosis of what remains (uniform Watson's-lemma
  remainder; next-order Stirling/Euler-Maclaurin corrections; Poisson-
  summation treatment of the outer sum; their combination) was checked
  against this review's own independent understanding of the mathematics
  after re-deriving claims 1–3 from scratch: it is **accurate and
  reasonably complete**. One implicit point worth making explicit for a
  future front: the `n=m²/λ²` substitution used throughout (both by the
  target and by this review, independently) is a *formal* device for
  extracting the `m→∞`-at-fixed-`λ` limit: item 1's "uniform... over
  `m=O(√n)`" already covers making this rigorous for the actual discrete
  sum over integer `m`, so nothing is missing, but it is worth being
  explicit that this is exactly what item 1 must supply.
- The mandate's own risk disclosure ("may return another honest
  non-closure with a sharper diagnosis, not necessarily `C(γ)`
  constructed," per `DISC-DEC-142`, confirmed by direct reading of the
  ledger entry) is exactly what happened, and the document does not
  claim otherwise anywhere. **No instance of overclaiming `C(γ)`'s
  status was found** — every scorecard row and the VERDICT itself
  correctly and consistently states `C(γ)` remains entirely open.

---

## Scope, seed, and governance discipline

- **File-scope discipline.** `git status --porcelain` (read-only) at the
  repository root shows the target's own new `joint_saddle_point_attempt/`
  directory plus two pre-existing, unrelated, already-known stalled
  directories from other sub-lineages (a `boundary_layer_selfheal_attempt`
  chain and a `k3_full_cdf_attempt_ABANDONED_STALLED` directory) as the
  only untracked entries. **Zero modified (tracked) files** anywhere in
  the repository. No `adversarial/` directory existed inside the target's
  own directory prior to this review (confirmed by direct `ls` before
  creating one).
- **Seed range.** `grep -rn "20260949" 05_DISCOVERY_LAB/` finds exactly one
  match outside this review's own new files: the `DECISION_LEDGER.yaml`
  reservation line itself (`20260949000–20260949999`, "frente b"). No
  `random`/`numpy.random`/`seed` call appears in any of the target's five
  scripts (direct grep; the one textual match, "points *seeded* at the
  analytic saddle," is a quadrature-node-placement comment, not RNG usage).
- **No `git` command** appears in any of the target's five scripts
  (`grep -n "subprocess\|os\.system\|git "` — zero matches); no `git`
  command other than the read-only `git status --porcelain` above was run
  by this referee.
- `DECISION_LEDGER.yaml`'s `DISC-DEC-142` entry (read-only) confirms the
  mandate wording quoted in the target's own header matches the ledger
  verbatim, including the specific starting point named ("a forma fechada
  Beta(m+1,m+1) verificada pelo próprio referee") and the explicitly
  disclosed risk (depth comparable to Gap 1, may not construct `C(γ)`).

---

## Summary assessment

This front's central mathematical machinery — the exact quadratic and
closed form for the inner saddle `t*` (§3), and the mesoscale limit profile
`T_prof(λ,γ)` derived via a genuine two-level Laplace/Stirling computation
(§4) — was independently re-derived from primary definitions in this
review, via a route that is methodologically *more* rigorous than the
target's own at one specific step (using the exact `lgamma` difference
rather than a leading-order shortcut for the binomial-shift term), and
lands on **exactly** the same closed forms, confirmed further by a direct
high-precision numeric check reaching beyond the target's own tested range
(`λ=2.0`, `m` up to `10^{10}`+). The central positive deliverable — that
`∫_0^∞T_prof\,dλ` exactly and non-circularly reproduces the already-PROVED
coefficient of `G_n` — is independently confirmed both as an exact identity
and, by direct file inspection, as genuinely non-circular. **These three
claims are sound; say so plainly: the joint saddle-point machinery, when
actually carried out, is mathematically correct at leading order, and this
review's own independent, structurally different re-derivation is strong
evidence of that, not merely a re-confirmation of the target's own
computation.**

Two real, checkable issues were found, both in descriptive/summary claims
rather than in the underlying mathematics: (1) the specific numerical bound
`"<0.7% for λ≤1.0"` (§4) is contradicted by the target's own log at
`λ=0.6` (`1.05%`), most likely a Richardson-extrapolation-procedure
artifact rather than a closed-form flaw, but uninvestigated and
mischaracterized as-is; (2) the "local-rate crossover" claim's near-origin
endpoint (`"c(γ)/2"`, VERDICT item 4 and §6) is both arithmetically wrong
in its own illustrative example and directly contradicted by the target's
own printed crossover data, which shows the near-origin value is `c(γ)`
itself, not half of it — while the genuinely solid part of that claim (a
non-constant curvature converging to `A(γ)`) survives. Neither issue
threatens `C(γ)`'s status (correctly reported as entirely open throughout)
or the front's other three findings.

**Verdict: SOUND WITH ISSUES — ACCEPT for catalogue**, conditional on
correcting (e) and (c) above in `ATTEMPT.md` (a dated addendum, per this
lineage's convention, is sufficient — no numerical result needs
recomputation, only the two summary claims need restating against the
data already on disk).

---

## Files

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref01_saddle_and_tprof_independent.py`/`.log` | independent symbolic + numeric re-derivation of the exact `t*` quadratic (with a stronger, non-numerical global-optimality proof via concavity) and of `T_prof(λ,γ)`, via the exact `lgamma` difference route (methodologically stronger than the target's own leading-order shortcut) |
| `ref02_gn_integral_and_circularity_check.py`/`.log` | independent confirmation of `∫T_prof\,dλ=½√(π/β)` (by-hand + fresh `sympy.integrate` + numeric spot-check on a disjoint γ-grid) and a direct file-inspection confirmation that scripts `02`/`03` never reference `G_n`/`β`/`T(γ)`, substantiating the "not circular" claim |
| `ref03_crossover_c_half_check.py`/`.log` | the claim-4 investigation: confirms the `γ=1/3` illustrative arithmetic is wrong, and independently reproduces the target's own `m=1` crossover data point, showing it equals `c(γ)`, not `c(γ)/2` |
| `ref04_lambda06_richardson_discrepancy.py`/`.log` | the claim-2-numerics investigation: reproduces the target's own `λ=0.6,γ=0.3` Richardson residual (`~1.05%`) from scratch, and shows the raw (non-extrapolated) error trend is clean, diagnosing the discrepancy as a Richardson-procedure artifact rather than a closed-form flaw |

No Millennium Problem claims anywhere in the target or this report; pure
combinatorial/asymptotic mathematics internal to this archive. No file
outside this front's own `joint_saddle_point_attempt/adversarial/`
directory was created or modified by this review. No `git` command was run
by this referee beyond the read-only `git status --porcelain` reported
above.
