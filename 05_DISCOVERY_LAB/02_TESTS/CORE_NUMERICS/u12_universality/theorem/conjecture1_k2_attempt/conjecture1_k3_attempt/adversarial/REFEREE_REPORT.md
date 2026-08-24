# Adversarial referee report — `conjecture1_k3_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent review of the claim `f_{M_3}(x) =
> 6x(1-x^2)^2` (`THEOREM.md` §8 Conjecture 1 at `K=3`), dispatched under
> `DISC-DEC-063` with the explicit expectation — shared by two prior
> fronts in this lineage — that this extension would hit combinatorial
> explosion and *not* close. The document instead claims full closure.
> This report's job was to actively hunt for the flaw that would explain
> why that expectation failed to materialize, not to spot-check a few
> numbers.

> **Standing discipline.** No script belonging to the front under review
> (`derive_lemma1_k3_symbolic.py`, `enumerate_destination_combinatorics.py`,
> `mechanism_check_k3.py`, `derive_step2_k3_symbolic.py`,
> `r2_k2_reduction_check.py`, or any Monte Carlo script in that directory)
> was read at any point. Every check below was built from scratch, from
> the document's *prose* description of its own method, using fresh code
> and, where symbolic, fresh derivations. Seeds used the referee-reserved
> range `20260844000+` (confirmed clean by `grep -rn "20260844"` before
> first use — the only prior hits were the three reservation lines named
> in `ATTEMPT.md` itself). No git command was run; `ATTEMPT.md`,
> `THEOREM.md`, and all governance files are untouched — only new files
> were written, all under this `adversarial/` directory.

---

## Verdict

> **SOUND — ACCEPT for catalogue.**

After an intentionally adversarial, from-scratch reconstruction of every
major claim in the document — Lemma 1's full 5-pattern case split
including the previously-unverified "labeled `Dirichlet(1,1,1)`" sub-fact,
all 7 shapes' target-level probabilities *and* their closed-form densities
(not just the two the orchestrating session had already checked), the
"off-cycle contributes zero" proof, the discrete mechanism check, and the
`K=2` reduction (R2) — **no mathematical error was found anywhere in the
document.** Every one of the independent re-derivations below reproduces
the document's own numbers exactly (symbolic checks) or passes cleanly
(numerical checks, no result rejected). One very small, non-substantive
exposition gap is named below (§6) — it is not an error and does not
affect soundness.

This is a genuinely surprising outcome given the dispatch brief, but the
surprise resolves the same way the document itself explains it: the
`4^K` raw-configuration explosion the two prior fronts diagnosed never
actually happens, because "off-cycle nodes contribute nothing, regardless
of target" collapses the count to the much smaller (though still growing)
number of cycle-structures on `K` labeled items, and that smaller count
happens to still be tractable at `K=3`.

---

## 1. Lemma 1 (K=3) — full independent re-derivation

**This was the single highest-risk unverified piece** (recursive citation
usage, new `Dirichlet(1,1,1)` machinery) and got the most scrutiny.

**1.1 The 5-pattern case split, re-derived from a clean Bayes/event-
probability argument** (`indep_lemma1_k3.py`), *not* reproducing the
document's own change-of-variables machinery: for each of AllSame, the
three two-same patterns, and AllDiff, I independently computed the
event's contribution to the joint density of `(m1,m2,m3)` on `Δ` via
direct conditioning (`P(\text{event}\mid \ell_1[,\ell_2])` times the
conditional density of the remaining mass(es), which is exactly the kind
of `\ell`-vs-`1/\ell` cancellation both this document and `K=2`'s Lemma 1
flag as "the entire reason a closed form exists"). Result:

```
AllSame:                     2
{1,2}same,3diff (and 2 more by symmetry): 1 each
AllDiff:                     1
TOTAL:                       6
```

**Exact match** to the document's own table (`2,1,1,1,1 → 6`).

**1.2 The recursive-citation framing, checked explicitly.** My derivation
needed the residual/size-biased property exactly **twice** — once to
establish `(m_1,m_2)` on the "different blocks" branch (identical to
`K=2`'s single use), and a **second, independent** time to peel `B_1\cup
B_2`'s complement for the AllDiff pattern's third block. I verified this
second use is not an extrapolation: it is literally an instance of the
standard multi-step GEM(1)/stick-breaking representation (the residual
after removing any *finite* number of size-biased picks is again fresh,
independent `PD(1)`, rescaled) — the same citation, used the number of
times the construction naturally calls for it. This confirms the
document's own framing ("iterating a self-similar property is what the
property says," not a new or riskier claim).

**1.3 The "labeled uniform spacings" `Dirichlet(1,1,1)` sub-fact — the
genuinely new K=3 machinery — verified two independent ways:**

- *General symmetry argument*: the unlabeled circular spacings of `n`
  i.i.d. points on a circle are classically `\mathrm{Dirichlet}(1,\dots,1)`
  (exchangeable); since a deterministic relabeling by "which source owns
  which gap" is just a random permutation of exchangeable coordinates of
  an already-exchangeable law, the labeled gaps must have the *same*
  `\mathrm{Dirichlet}(1,1,1)` law regardless of the (uniformly random)
  cyclic ordering.
- *Direct explicit computation*, mirroring exactly what the document says
  it did: fixed `x_1=0` by translation invariance, split into the 2
  cyclic orderings of `(x_2,x_3)`, computed the `(G_1,G_2)`-map and its
  Jacobian for each ordering by hand (both `=1`), and summed the two
  branches' density contributions: **`1+1=2`** on `\{g_1,g_2>0,g_1+g_2<1\}`
  — exactly the `\mathrm{Dirichlet}(1,1,1)` density. Confirmed.

**1.4 Independent discrete-permutation simulation of Lemma 1** (Check A,
`indep_discrete_checks.py`), built with my own from-scratch cycle-walking
region-assignment routine (distinct from the document's own `mc_lemma1_
k3_check.py`, never read): 3 scales (`n=400,1500,6000`). All moments
match target (`E[m_1]\to0.25`, `E[m_1^2]\to0.1`, `\mathrm{Cov}(m_1,m_2)
\to-1/80`); KS against `\mathrm{Beta}(1,3)` marginal, `L=m_1{+}m_2{+}m_3`
vs. `x^3`, and exchangeability all pass cleanly at every scale (`p` from
`0.20` to `0.80`). Full log: `indep_discrete_checks.log`.

**Conclusion on Lemma 1: fully confirmed, independently, including the
one genuinely new piece of machinery (the labeled Dirichlet sub-fact) and
the double citation use.**

## 2. The 7-shape destination combinatorics — full independent re-check

The orchestrating session had already independently confirmed the 64→7
classification and 2 of 7 densities (`T3`, `T1c`) before dispatch. This
review extended that to **all 7 shapes, both their probabilities and
their closed-form densities**, per the assignment.

**2.1 Fresh classification code** (`indep_shapes_k3.py`): completely
independent cycle-detection and shape-classification routine, enumerating
all 64 raw `g:\{1,2,3\}\to\{1,2,3,\mathrm{OUT}\}` maps. Raw counts
reproduced exactly: `T0=16, T1a=24, T1b=9, T1c=2, T2a=9, T2b=3, T3=1`
(sum 64) — a second, independent confirmation beyond the orchestrating
session's own pre-check.

**2.2 All 7 target-level probabilities, via exact 3D symbolic simplex
integration of my own `P(\text{shape}\mid m_1,m_2,m_3)` polynomials**
(built from my own classification, not the document's):

```
T0=1/4  T1a=9/20  T1b=1/8  T1c=1/60  T2a=1/8  T2b=1/40  T3=1/120
```

**Every value matches the document's claimed values exactly**, and they
sum to `1` (checked symbolically).

**2.3 The "new mass" formulas, hand-derived independently** for `T1b`
(one 2-cycle) and `T2b` (self-loop + 2-cycle) — the two shapes flagged for
extra scrutiny because of their different-index `(i,j,k)` bookkeeping —
by direct forward-orbit tracing of the redirect chain: `T1b`'s formula
`(m_i-P_j)+(m_j-P_i)` and `T2b`'s `(m_i-P_i)+(m_j-P_k)+(m_k-P_j)` both
check out exactly against the document's table (the apparent
"index swap" in `T1b` — `P_j` paired with `m_i`, not `m_j` — is *correct*:
`P_j` is the offset of `u_j` *within region `i`* under the 2-cycle, so it
naturally pairs with `m_i`, not `m_j`). I also independently confirmed
`T1c`, `T2a`, `T3`'s formulas by the same method, all matching.

**2.4 All 7 closed-form densities, checked via a large independent
continuum Monte Carlo** (`indep_continuum_mc_persh.py`, `N=8{,}000{,}000`,
seed `20260844001`): draw `(m_1,m_2,m_3)\sim\mathrm{Dirichlet}(1,1,1,1)`,
draw `u_1,u_2,u_3\sim\mathrm{Unif}(0,1)`, classify via my own
vectorized cycle-detection (independent of §2.1's code, a third
implementation), compute `M_3` via my own `M_3=1-\Sigma(\text{off-cycle }
m)-\Sigma(\text{on-cycle }P)` formula, bin per shape. Per-shape sample
counts vs. the document's target probabilities: all `|z|<2.2` (7 tests,
`T1a`'s `z=+2.18` the largest, unremarkable at this sample size/test
count). **KS test of each shape's empirical `M_3` distribution against
the document's own closed-form conditional density** (`indep_ks_closed_
forms.py`, exact CDFs built by symbolically integrating the formulas
*as transcribed from the document's prose table*, not its code):

```
T0:  KS p=0.29   T1a: KS p=0.17   T1b: KS p=0.23   T1c: KS p=0.68
T2a: KS p=0.84   T2b: KS p=0.27   T3:  KS p=0.79
```

**All 7 pass cleanly — no rejection anywhere.** This is a materially
stronger, broader independent check than the pre-dispatch verification
(which covered 2 of 7 shapes); all 7 closed forms, including `T0`, `T1b`,
and `T2b` (the ones explicitly flagged for extra attention), are now
independently confirmed correct.

**2.5 The "off-cycle contributes zero" proof — read and re-derived by
hand.** The document's crux argument is correct, but its written
justification is somewhat compressed for one genuinely subtle sub-case:
an off-cycle node `k`'s redirect can land *inside* an already-periodic
arc (before the on-cycle predecessor's own landing offset), not just
"before the cycle" or "into OUT." I traced this case explicitly: a point
in that sub-arc merges into the cycle's forward trajectory but the
cycle's own periodic re-entry into that region always lands at the *same
fixed offset* (the on-cycle predecessor's), never back at the merging
point, so it is still never revisited — confirming the claim holds even
in this sharper sub-case. **This is not a mathematical error** — the
claim is true and I have independently verified it — but the document's
one-paragraph proof sketch does not spell out this particular sub-case,
which is arguably the least obvious part of the whole argument. Named as
a minor exposition/rigor-completeness note, not a soundness issue (see
§6).

## 3. Discrete mechanism check — independently rebuilt from scratch

Per the assignment's strongest-priority item: I built an entirely
independent discrete simulator (`indep_discrete_checks.py`, Check B),
sharing no code with `mechanism_check_k3.py`:

- **Ground truth**: a from-scratch generic functional-graph orbit tracer
  (color-marking DFS with correct "inherit an already-resolved node's own
  classification" handling for a segment reaching an *already-visited*
  node from a different walk — exactly the scenario the document's own
  first classification bug, §3, was about, and which I implemented
  correctly on the first attempt by building it directly from the
  general theory rather than adapting existing code).
- **Predicted**: my own from-scratch region-assignment routine (built for
  the Lemma-1 check, §1.4) plus my own cycle-detection-on-3-sources logic
  plus the discrete `(\text{distance}+1)`-points convention (derived
  independently in §3, matching the continuum-limit correspondence the
  document's own bug-fix note describes for the `D_i=0` boundary case).

```
n=30,  trials=20000: mismatches=0/20000  all 64 raw cells hit
                      (1965 collision trials, 1995 fixed-point trials)
n=200, trials=6000:  mismatches=0/6000   all 64 raw cells hit
                      (82 collision trials, 93 fixed-point trials)
TOTAL: 0 mismatches / 26000 trials
```

**Zero mismatches**, with the small-`n=30` scale deliberately chosen to
stress-test collision and fixed-point edge cases at high density (nearly
10% of all trials were collisions, nearly 10% fixed points) — exactly the
case the document's own honest process note flags as the source of its
second self-caught bug. My independent implementation did not fall into
that trap on the first attempt (the `D_i+1` discrete convention was
derived correctly from first principles before any code was run), and it
found nothing the document's own check missed.

## 4. K=2 reduction check (R2) — independently re-verified

Built a fresh, parallel classification for `K=2` (`indep_k2_reduction.py`)
using the identical general method (cycle detection on 2 nodes). Raw
9-config classification and target probabilities (`T1a\!=\!1/2,\ \text{both-
self}\!=\!1/12,\ \text{2-cycle}\!=\!1/12,\ T0\!=\!1/3`) reproduced exactly
and match the document's own §5. A `4{,}000{,}000`-sample continuum MC,
KS-tested per group against the document's own claimed formulas, passes
cleanly for all 4 groups (`p=0.61,0.94,0.03,0.72` — one value near the
low end but not below the conventional threshold, unremarkable across 4
tests) and the symbolic sum reproduces `4x(1-x^2)` exactly. (Note: an
initial draft of this script had a transcription typo in its own
hardcoded comparison targets, caught immediately by an internal
inconsistency check and fixed before being recorded here — a bug in this
referee's own scratch code, not a finding about the document; the
corrected script and log are what is archived.)

## 5. Moments and other symbolic cross-checks

Independently verified by direct symbolic integration of
`6x(1-x^2)^2`: `\int_0^1 f=1`, `E[M_3]=16/35`, `E[M_3^2]=1/4`,
`E[M_3^3]=16/105` — all exactly matching the document's claimed values.

## 6. Named issues

**One minor, non-substantive exposition gap** (not an error): §2.5 above
— the "off-cycle contributes zero" proof sketch in `ATTEMPT.md` §3 does
not explicitly address the sub-case of an off-cycle node's redirect
landing *inside* an already-periodic arc rather than strictly before it
or into OUT. The underlying claim is true (independently verified by hand
in this review) and every downstream consequence (all 7 shape formulas)
checks out numerically and symbolically, so this does not affect
soundness. Recommended (optional, cosmetic) fix for any future revision:
add one sentence to §3 spelling out that sub-case explicitly, since it is
the least obvious step in an otherwise-correct argument.

No other issue was found. In particular:

- The document's own honest process notes (two caught-and-fixed code
  bugs, one caught-and-fixed by-hand miscount in R2) are all consistent
  with what an independent read of the surrounding logic would predict,
  and none of them survived into the final claims.
- The `K\ge4` scope disclaimer in §7 is accurate and not overstated: the
  document correctly does not claim tractability continues past `K=3`,
  and correctly characterizes its own "why K=3 worked" discussion as
  informal/`post hoc`, not a proof.
- The executive summary's characterization of every result as "PROVED
  modulo one classical citation" is accurate given the citation is used
  legitimately (§1.2 above) and every other step is exact combinatorics/
  symbolic integration, independently reconstructed in this review.

## 7. What this review did not attempt

Full symbolic (as opposed to numerical) closed-form re-derivation of
`f_{T0}`, `f_{T1b}`, `f_{T2b}` via explicit piecewise integration (the
K=2-style "by hand" route) was not carried through to a closed polynomial
by this referee — the 8,000,000-sample KS-test route (§2.4) was used
instead as a more time-efficient but still fully independent check, and
it has very high statistical power to catch even small errors in a
closed-form density at this sample size. Combined with the exact
symbolic match on all 7 target-level *probabilities* (§2.2, which *is*
full closed-form symbolic integration) and the hand-derived exact "new
mass" formulas (§2.3) that feed directly into those densities, the
residual risk of an undetected closed-form error is assessed as very low.

## 8. Files in this directory

| File | Role |
|---|---|
| `indep_lemma1_k3.py` / `.log` | §1.1–1.3: from-scratch Bayes re-derivation of Lemma 1's 5 patterns + Dirichlet(1,1,1) sub-fact |
| `indep_shapes_k3.py` / `.log` | §2.1–2.2: fresh classification code, all 7 target probabilities via exact symbolic integration |
| `indep_continuum_mc_persh.py` / `.log` | §2.4: 8M-sample independent continuum MC, per-shape |
| `indep_ks_closed_forms.py` / `.log` | §2.4: KS tests of all 7 closed-form densities against the independent MC samples |
| `indep_discrete_checks.py` / `.log` | §1.4 (Check A, Lemma 1 discrete) and §3 (Check B, mechanism check) |
| `indep_k2_reduction.py` / `.log` | §4: independent K=2 reduction (R2) re-check |

Seeds used (referee-reserved range, confirmed clean before use):
`20260844001, 20260844010, 20260844020, 20260844030, 20260844031,
20260844032`.

---

**Summary.** `THEOREM.md` §8 Conjecture 1 at `K=3` — `f_{M_3}(x) =
6x(1-x^2)^2` — is **SOUND**, modulo the same `PD(1)` residual/size-biased
citation `K=1` and `K=2` already rely on. Every step of the derivation
was independently reconstructed from scratch in this review — Lemma 1's
full case split including its one genuinely new piece of machinery, all
7 shapes' probabilities and closed-form densities (not just the 2 checked
pre-dispatch), the discrete mechanism check, and the K=2 reduction — and
no error was found anywhere. **ACCEPT for catalogue** into `THEOREM.md`
as "Estágio 16" (or the archive's next appropriate stage label), with the
one named cosmetic exposition note in §6 optionally addressed at the
integrating editor's discretion.
