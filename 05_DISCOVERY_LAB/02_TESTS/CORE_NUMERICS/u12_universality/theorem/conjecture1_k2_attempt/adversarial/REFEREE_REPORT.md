# Adversarial Referee Report — `CONJECTURE-1-K2-ATTEMPT`

> Target: `ATTEMPT.md` (this directory's parent), claiming `f_{M_2}(x) =
> 4x(1-x^2)` on `(0,1)`, exactly — a proof of `THEOREM.md` §8 Conjecture 1
> at `K=2`, "PROVED, modulo one classical citation."
>
> Referee scope note: this report covers the parts of the claim not
> already independently re-derived by the orchestrating session (the
> symbolic/algebraic chain from Lemma 1's premise to `f_{M_2}=4x(1-x^2)`,
> which the orchestrator re-derived from scratch and confirmed exactly).
> This report focuses on: (1) Lemma 1 itself — the joint-uniformity claim
> for `(m_1,m_2)`; (2) the 9-cell mechanism table (§3); (3) the "same
> citation as Proposition 2.4" framing and the §2.3 finite-`n` argument;
> (4) a general search for errors/overclaims, including a larger-scale
> independent re-run of the aggregate density check.
>
> All checks below were built entirely from scratch in this session —
> none of the front's own scripts (`derive_density_symbolic.py`,
> `derive_density_full.py`, `r2_k1_sanity.py`, `mc_step_a_check.py`,
> `discrete_k2_full_distribution_mc.py`, `mc_recipe_check.py`,
> `bonus_limitsim_crosscheck.py`) were read or imported. Seeds used:
> `20260836001`–`20260836021`, confirmed unused in the archive before
> first use (only the two reservation lines in `ATTEMPT.md` /
> `DERIVATION_PREREG.md` / `DECISION_LEDGER.yaml` mentioned the range).

## Verdict

**SOUND WITH NAMED ISSUES (one, minor, non-substantive) — ACCEPT for
catalogue.**

The mathematics is correct. Lemma 1 (the load-bearing, highest-risk step,
explicitly flagged as such in `DERIVATION_PREREG.md` before any
computation) holds up under an independent discrete-permutation
simulation that does not presuppose the continuum PD(1)/stick-breaking
machinery at all. The 9-cell mechanism table in §3 — the one part of the
document neither the front's own R4 nor the orchestrator's symbolic
re-derivation tested at the granular, per-configuration level — passed a
260,000-trial, all-9-cells, exact-match test with **zero** mismatches,
including boundary/collision edge cases. The "same citation as
Proposition 2.4" framing is accurate in substance, and is in fact the
*same methodological move* `THEOREM.md`'s own already-accepted §5.3
(K=1) proof makes, not a new or riskier one. The §2.3 finite-`n`
combinatorial argument does **not** smuggle in the harder, still-partial
`M_n(c)→L(c)` bridge (Stage 2, §7); it is a self-contained, exact,
elementary discrete fact with a genuinely trivial `n→∞` step, correctly
characterized as such. The one named issue is a citation-label
imprecision inside Lemma 1's own proof text that does not affect the
proof's validity.

---

## 1. Lemma 1 (§2.2) — independent verification

### 1.1 What was checked and how

Lemma 1 claims `(m_1,m_2)` — background-cycle-membership masses of two
independent uniform reroute sources on an independent `PD(1)` partition
— is **exactly uniform** (density 2) on the triangle `T={m_1,m_2>0,
m_1+m_2<1}`. Its proof rests on one classical citation (the `PD(1)`
residual/size-biased-sampling property) plus otherwise-elementary steps.

Rather than re-verify the *algebra* (already done by the orchestrator),
this referee built a **genuinely different generative model** —
`adv_lemma1_discrete_check.py` — that does not touch stick-breaking or
`PD(1)` machinery at all: draw a uniform random permutation `π` of
`[n]`, pick two random distinct labels `x_1,x_2`, trace the actual
cycle(s), and compute `(m_1,m_2)` from raw permutation combinatorics
exactly per Lemma 1's own case definitions (same-cycle: arc split;
different-cycles: two whole cycle lengths). This is the discrete
ensemble underlying `THEOREM.md`'s Definition 1/4, not a re-run of the
continuum citation being scrutinized — a genuinely independent route.

### 1.2 Results

Three scales (`n=300,1000,3000`; seeds `20260836001–003`; full output in
`adv_lemma1_discrete_check.log`/`.json`):

| `n` | trials | `P(same block)` | KS(`m_1` vs `2x-x^2`) | KS(`m_1+m_2` vs `x^2`) | exchangeability KS(`m_1` vs `m_2`) |
|---|---|---|---|---|---|
| 300 | 60,000 | 0.5011 (z=0.51) | D=0.0074, **p=0.0029** | D=0.0070, **p=0.0055** | D=0.0099, **p=0.0057** |
| 1000 | 40,000 | 0.4968 (z=−1.29) | D=0.0044, p=0.41 | D=0.0043, p=0.45 | D=0.0049, p=0.72 |
| 3000 | 20,000 | 0.4998 (z=−0.06) | D=0.0046, p=0.80 | D=0.0060, p=0.48 | D=0.0069, p=0.73 |

All first and second moments (`E[m_1],E[m_2],E[m_1^2],E[m_1 m_2],
\mathrm{Cov}(m_1,m_2)`) matched the exact `\mathrm{Dirichlet}(1,1,1)`
targets (`1/3,1/3,1/6,1/12,-1/36`) to within `z<1.6` at every scale.

**Interpretation.** At `n=300` the KS tests reject at the `p<0.01`
level — but this is *exactly the expected signature of a genuine
`n→∞` limit claim*, not evidence against Lemma 1: a discrete finite-`n`
permutation model has an `O(1/n)`-type discretization bias relative to
its continuum limit (the same kind of bias `THEOREM.md` Proposition 4
computes *exactly* for the related `K=1` finite-`n` bridge:
`\varphi_n^{(1)}-\varphi_1=1/(3n^2)`). As `n` grows tenfold (300→3000),
the KS `p`-values climb cleanly from `0.003–0.006` to `0.48–0.80`, and
the `z`-scores fall below 1.3 at every scale beyond `n=300` — a clean
convergence trend, not noise. This is *stronger* evidence for Lemma 1
than a continuum-only check could give: it confirms the claimed
continuum law is genuinely compatible with being the correct limit of
the actual combinatorial ensemble, not merely internally consistent
with itself.

**Conclusion on Lemma 1: independently corroborated, no error found.**

---

## 2. The 9-cell mechanism table (§3) — independent per-cell check

### 2.1 Why this was the priority

Neither the orchestrator's symbolic re-derivation nor the front's own R4
(`discrete_k2_full_distribution_mc.py`) tests the **mechanism** at the
per-configuration level: R4 only compares the *aggregate* empirical
density of `M_2/n` to `4x(1-x^2)` via a KS test, which could in
principle pass even if individual cell formulas in §3's table were
subtly wrong but compensated on average. This referee built
`adv_mechanism_check.py` to close exactly that gap.

### 2.2 Method

For each trial: draw a fresh permutation `π` of `[n]`, random distinct
`x_1,x_2`; compute region1/region2 as explicit ordered lists (far-edge
→ source) directly from Lemma 1's own definitions; draw `u_1,u_2`
uniform on `[n]`; classify each as landing in `R1`/`R2`/`OUT` with its
0-indexed position; **build the actual mapping `f`** (background `π`
except `f(x_1)=u_1,f(x_2)=u_2`) and find its **true** cyclic set by a
from-scratch color-marking orbit trace (ground truth — no formula
assumed). Independently, compute the **claimed** `M_2` from the 9-cell
table (hand-transcribed from `ATTEMPT.md` §3 for comparison only) using
the measured region masses and positions, and compare exactly.

### 2.3 Results

Two scales (`n=30`, 200,000 trials; `n=200`, 60,000 trials; seeds
`20260836011/012`; full output in `adv_mechanism_check.log`/`.json`):

```
n=30,  trials=200000: exact match rate = 1.00000000 (200000/200000)
n=200, trials=60000:  exact match rate = 1.00000000 (60000/60000)
```

All 9 raw cells (`u1∈{R1,R2,OUT} × u2∈{R2,R1,OUT}`, using the doc's own
row/column semantics) were hit with substantial counts (16,000–34,500
at `n=30`; 4,900–10,100 at `n=200`) and **every single cell matched
exactly, 100%** — including 6,728 (`n=30`) and 313 (`n=200`) trials
where `u_1=u_2` (destination collision) and 13,109 / 564 trials where a
destination landed exactly on its own source point (`u_i=x_i`, the
degenerate fixed-point case). These are precisely the edge cases a
purely symbolic/continuum treatment cannot see (probability zero in the
continuum), and the mechanism held exactly through all of them.

**Conclusion on the mechanism table: independently confirmed at the
most granular level available — no error found, and this is the
strongest new evidence this report adds beyond what was already
checked.**

---

## 3. The citation framing and the §2.3 finite-`n` argument

### 3.1 Is it really "the same" citation as Proposition 2.4?

`THEOREM.md` Proposition 2.4 (§2.3) cites Kingman 1975 / Arratia–Barbour–
Tavaré 2003 for the "Feller coupling" representation of `PD(1)`/`GEM(1)`
under simultaneous multi-arc-head exploration, and is explicitly labeled
"CITED, not re-derived here" (`THEOREM.md` §6 item 8) — the *only*
non-self-contained structural input to Stage 1's entire proved core.
`ATTEMPT.md` §2.2's residual-property citation (McCloskey 1965;
Patil–Taillie 1977; Pitman St-Flour 2002 Ch. 3) is the textbook
size-biased-deletion/residual-allocation property that is, in substance,
immediate from the very recursive definition of `GEM(1)` stick-breaking
— arguably *more* elementary than Proposition 2.4's full multi-arc-head
independence claim, not less. Checked directly: `THEOREM.md` §5.3 (the
already-accepted, "PROVED" `K=1` result this document generalizes) uses
the *identical* move — "let `L~Unif(0,1)` be the (size-biased,
`PD(1)`-typical) length of the cycle struck by the reroute" — sourced to
`DERIVATION.md §5`, with no more ceremony than `ATTEMPT.md` gives its
own `L_1`. So the "not a new or weaker link" framing is accurate: it is
the same methodological choice already baked into the archive's accepted
Stage-1 core, at the same rigor level, not a new exposure.

### 3.2 Does §2.3's finite-`n` argument secretly need the (still-partial)
`M_n(c)→L(c)` bridge?

This was the sharpest risk to check: `THEOREM.md` §6 item 9 explicitly
states that no result in Stage 1 "proves or assumes" `M_n(c)→L(c)`
convergence, and Stage 2 (§7) only closes this bridge for the *mean*
(`φ_n^{(K)}→φ_K`), progressively, `K` by `K` (fully unconditional through
`K=10` as of the latest "Estágio" extension read in `THEOREM.md`, `K≥11`
still open in general). If §2.3's argument silently depended on this
bridge for a *distributional* (not just mean) statement, that would be a
real, hidden escalation of risk.

On close reading, it does **not**. §2.3's argument is: (i) an **exact**,
non-asymptotic, finite-`n` combinatorial fact — given `L_1=\ell` and
`2\notin C_1`, the permutation restricted to the complementary `n-\ell`
labels is *itself* an exactly uniform random permutation (a one-line
exchangeability fact for `S_n`, standard and correct), so `L_2` (label
`2`'s cycle length) is *exactly* `\mathrm{Unif}\{1,\dots,n-\ell\}` for
**every finite `n`** — no limit needed for this part at all; (ii) the
only actual `n\to\infty` step is the elementary, fully rigorous fact
that discrete uniform on `\{1/m,\dots,1\}` converges weakly to
`\mathrm{Unif}(0,1)` as `m\to\infty` — a one-paragraph fact, structurally
the *same kind* of convergence already implicit in Fact A's own remark
that Definition 3's `T_0` "matches the classical fact... in the `n\to\infty`
limit" (`THEOREM.md` §2.3). This is a fact about a single point's cycle
length in a plain uniform permutation, not about the harder rerouted-
mapping-with-Poisson-marks object Stage 2's bridge is proving convergence
for. The document's own framing ("not a new gap... the same
already-flagged, already-accepted limit passage") is accurate, not an
overclaim.

The specific numeric fact §2.3 cross-references — `E[(L-1)/(n-1)]=1/2`
for `L\sim\mathrm{Unif}\{1,\dots,n\}`, attributed to `THEOREM.md`'s
"Lema do co-ciclo" (Estágio 3, Resultado 3) — was checked directly
against `THEOREM.md`'s own text (line ~1369–1372): *"a probabilidade
`P=1/2` exata... foi re-derivada do zero pelo referee
(`E[(L-1)/(m-1)]=1/2`) e confirmada por força bruta para `m=2..8`"* —
confirms `ATTEMPT.md`'s citation is accurate, correctly scoped ("a
different sub-problem," "corroborating evidence" not independent proof),
not fabricated or inflated. (The fact itself is also trivially
verifiable by hand: `\frac1{n(n-1)}\sum_{\ell=1}^n(\ell-1) =
\frac1{n(n-1)}\cdot\frac{n(n-1)}2=\frac12` for every `n\ge2`.)

### 3.3 One named issue

Lemma 1's proof (§2.2) opens: *"By Fact A (`THEOREM.md` §2.3, PROVED),
`L_1\sim\mathrm{Unif}(0,1)`."* This is imprecise. `Fact A`, as literally
proved in `THEOREM.md`, establishes `T_0=1-e^{-E_0}\sim\mathrm{Unif}(0,1)`
for a specific auxiliary variable inside **Definition 3**'s explicit
hazard-clock construction — not, by itself, "the length of a size-biased
block in **Definition 2**'s canonical `PD(1)` partition" (which is the
object `ATTEMPT.md` §1 actually declares its model on). The bridge
between the two is exactly Proposition 2.4's role, and `THEOREM.md`
itself is careful to say Fact A only gives "an elementary,
self-contained *partial check*" of Proposition 2.4 (§6, item 8) — not a
proof that supersedes it. So the precise citation for `L_1\sim
\mathrm{Unif}(0,1)` on Definition 2's object should be the classical
size-biased-sampling fact (McCloskey/Patil–Taillie/Pitman) directly —
exactly as `ATTEMPT.md`'s own very next paragraph correctly does for the
residual property — rather than "Fact A, PROVED." This is a labeling
inconsistency **within `ATTEMPT.md` itself** (one invocation of
essentially the same underlying fact is marked PROVED via Fact A, the
other correctly marked CITED), not a new mathematical gap: the
underlying claim (`L_1\sim\mathrm{Unif}(0,1)`) is exactly what
`THEOREM.md` §5.3's own already-accepted proof uses without comment, and
substance-wise this referee found it to be correct (§1 above,
independently, numerically). **Recommended fix (non-blocking):** reword
to "by the same classical size-biased-sampling fact `§5.3`'s own proof
relies on (McCloskey 1965; Patil–Taillie 1977; Pitman 2002 Ch. 3) —
Fact A independently confirms this marginal within Definition 3's own
construction, as a partial check, not a full derivation for Definition
2's object."

---

## 4. General error/overclaim search, and a larger-scale independent R4

### 4.1 Independent larger-scale aggregate density check

Using the same from-scratch orbit-tracer as §2, this referee ran an
independent full-density check at **`n=20000`** (2× the front's own R4,
which used `n=10000`) with `12000` trials (seed `20260836021`; full
output in `adv_aggregate_r4_scaleup.log`/`.json`):

```
KS D=0.00545, p=0.866   (front's own R4: D=0.00799, p=0.542, n=10000/trials=10000)
mean(M2/n)=0.53361, z=+0.14 vs phi_2=8/15=0.53333
E[x^2]=0.33401 vs target 1/3=0.33333
```

This independently confirms the aggregate claim at larger scale than the
front's own check, with an even cleaner `p`-value, using code that
shares no lines with either the front's scripts or this referee's own
§1–2 Lemma-1/mechanism checks (only the orbit-tracer routine is reused
between §2 and this section, and that routine was itself validated
line-by-line by the 100%-exact-match result in §2).

### 4.2 Fidelity check — does `ATTEMPT.md` accurately report its own logs?

Every numeric value `ATTEMPT.md` §6 quotes from its own scripts was
checked against the corresponding `.log` file in the parent directory
(`mc_step_a_check.log`, `discrete_k2_full_distribution_mc.log`,
`mc_recipe_check.log`, `bonus_limitsim_crosscheck.log`,
`derive_density_full.log`, `r2_k1_sanity.log`, and the preserved
`mc_step_a_check_BUGGY_FIRST_ATTEMPT.log`) — every number matches
exactly, including the extreme z-scores (200–536) and `p<10^{-4}` KS
results in the deliberately-preserved buggy first attempt, confirming
the "honest bug report, not silently patched" claim (§6.2) is genuine
and the log was not sanitized after the fact. File timestamps
(`ls -la --time-style=full-iso`) confirm `DERIVATION_PREREG.md`
(21:38:32) predates every script/log (21:49:07+) and `ATTEMPT.md` itself
(21:51:42), matching the provenance claim in §0.

### 4.3 Scope/honesty claims (§7)

`ATTEMPT.md` §7 states plainly that `K\ge3` was not attempted and makes
no claim about it, citing the same combinatorial-explosion diagnosis
`../k2_open_lemma/ATTEMPT.md` gives for a *different* problem (the
`n\to\infty` mean-bridge, not the density conjecture) exploding past
`K=2`. This is an honest, non-overclaiming statement of scope; no
attempt was found anywhere in the document to extend, hint at, or
informally claim progress on `K\ge3` beyond this acknowledgment. The
scorecard (§8) is consistent with the body text throughout — no item is
marked more strongly than its proof section supports.

### 4.4 Governance

`DISC-DEC-057` (`DECISION_LEDGER.yaml`, line 3606) authorizes front (c)
`CONJECTURE-1-K2-ATTEMPT` exactly as described in `ATTEMPT.md`'s
governance banner. No irregularity found.

### 4.5 No other error found

No other computational, logical, or citation error was found anywhere
in `ATTEMPT.md` in the course of this review (which additionally
included a full read of `THEOREM.md` §0–§7 and the Estágio 3 extension
for citation-context verification).

---

## 5. Scorecard (referee's own, independent of `ATTEMPT.md` §8)

| Item | Referee verdict |
|---|---|
| Lemma 1 (`(m_1,m_2)` uniform on `T`, density 2) | **CONFIRMED** — independent discrete-permutation MC at 3 scales, convergence trend as `n→∞` matches theory (§1) |
| 9-cell mechanism table (§3) | **CONFIRMED** — 260,000-trial exact-match test, all 9 cells, incl. edge cases, 0 mismatches (§2) |
| "Same citation as Proposition 2.4" framing | **ACCURATE** — same methodological move as `THEOREM.md` §5.3's already-accepted proof (§3.1) |
| §2.3 finite-`n` argument (no bridge-gap smuggling) | **CONFIRMED clean** — self-contained, exact at finite `n`, only a trivial discrete→continuous limit (§3.2) |
| Cross-reference to "Lema do co-ciclo" Estágio 3 | **VERIFIED accurate**, correctly scoped (§3.2) |
| Aggregate density `f_{M_2}(x)=4x(1-x^2)` | **RE-CONFIRMED** at 2× the front's own R4 scale, cleaner `p`-value (§4.1) |
| Self-reported numerics fidelity | **VERIFIED** — every quoted number matches its source log exactly (§4.2) |
| `K\ge3` "not attempted" honesty | **VERIFIED**, no overclaim found (§4.3) |
| Citation label in Lemma 1's proof ("Fact A... PROVED") | **NAMED ISSUE** — imprecise label, substance unaffected (§3.3) |

## Files produced by this referee (`adversarial/`)

- `adv_lemma1_discrete_check.py` / `.log` / `.json` — §1
- `adv_mechanism_check.py` / `.log` / `.json` — §2
- `adv_aggregate_r4_scaleup.py` / `.log` / `.json` — §4.1
- `REFEREE_REPORT.md` — this document

**Recommendation: ACCEPT for catalogue**, with the single suggested
(non-blocking) wording fix in §3.3 above. No git command was run; no
file outside this `adversarial/` subdirectory was created or modified.
