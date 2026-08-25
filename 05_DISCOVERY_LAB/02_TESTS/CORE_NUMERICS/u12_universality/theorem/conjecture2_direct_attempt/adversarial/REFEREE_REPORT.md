# Adversarial referee report — `conjecture2_direct_attempt/ATTEMPT.md`

> **Governance.** Independent hostile review of wave 16 front (e)
> (`CONJECTURE-2-DIRECT-ATTEMPT`, `DISC-DEC-066`), performed 2026-08-25.
> Discipline followed: **none of the front's `.py` scripts was read or
> reused** — every check below was rebuilt from `ATTEMPT.md`'s prose
> alone; the front's `.log` files were read only as claimed outputs to
> compare against. Accepted context read: `THEOREM.md` (§§1–5, 7.3, 8),
> `conjecture1_k2_attempt/ATTEMPT.md` (+ its referee report, accepted),
> `conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md` (+ its
> referee report, accepted), and the front's `DERIVATION_PREREG.md`.
> Referee seeds: `20260859000`, `20260859001` (reserved referee block
> `20260859000+`, confirmed unused before first use — the only prior
> `grep -rn "20260859"` hits were the expected reservation lines in
> `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
> the K4 front's prereg quote, and the target front's own two
> reservation notices). Files created: this report plus 4 scripts and
> 4 logs, all inside this new `adversarial/` directory. Nothing else
> in the archive was created, modified, or deleted; git used read-only
> (`git status`).

## Verdict

> **SOUND WITH NAMED ISSUES (four, all minor, none affecting any
> exact/PROVED computation) — ACCEPT for catalogue, at its claimed
> tier: honest non-closure with named partial results.**

Every exact claim the document labels PROVED was independently
re-derived or re-executed by this referee and is correct: both new
closed forms (two independent symbolic routes each), Lemmas B1–B3
(continuum derivations re-checked; discrete cross-checks re-enumerated
from scratch and **extended to `n=8` with a stronger cell-level closed
form**), Lemma B4 (logic airtight; fresh-seed simulation, zero
violations), and the §4.2 counterexample (verified by hand and by two
independent algorithms; exact). The honesty framing is genuinely
maintained where it matters most: the second-moment closed form is
consistently presented as a *target computed from the conjectured
law*, not as evidence or as an independent derivation, and the §3.3
obstruction is presented as a located open problem, not an
impossibility theorem. The four named issues are: two shorthand-label
wording slips (Issues 1, 4) and two small, fully repairable proof-level
gaps in §4's scope (Issues 2, 3 — the referee supplies both repairs
below, one of them using the document's own configuration). None
changes the net verdict the document itself reports. An honest
non-closure that survives hostile re-derivation of everything it does
claim is exactly what the catalogue tier requires.

---

## 1. The moment-method architecture (§2) — VERIFIED

**Hausdorff determinacy (CITED).** Correct as stated: a `[0,1]`-valued
random variable's law is uniquely determined by its moment sequence
(Hausdorff moment problem on a compact interval is determinate; the
Stone–Weierstrass argument sketched in §2 is the standard one, and the
document is right that no MGF-convergence subtlety arises on compact
support). The citation is used at exactly the rigor level `THEOREM.md`
itself uses for CITED facts.

**Fubini reduction.** `E[M(c)^p] = ∫_{[0,1]^p} P(x_1,…,x_p all
cyclic) dx` is a correct Fubini–Tonelli application (non-negative,
jointly measurable integrand), and the invoked `p=1` precedent is
accurately described: `THEOREM.md` §2.4 performs exactly this reduction
for the mean, and §3 Steps 3–5 compute the one-point marginal by
marking/thinning without ever conditioning on `K`. The
"correct-if-completed" framing is accurate: if all `p`-point joint
cyclic probabilities were computed `K`-free and the resulting moments
matched `min(1,√(E/c))`'s (both laws live on `[0,1]`), Conjecture 2
would follow. As a bonus record, the referee computed the conjectured
law's general-`p` moment: `E[min(1,√(E/c))^p] = e^{-c} +
γ(p/2+1,c)/c^{p/2}` (lower incomplete gamma), which reduces at `p=2`
to `(1-e^{-c})/c` exactly (`ref_symbolic_targets.log`, S9b).

## 2. The new closed forms (§3.1) — VERIFIED, framing honest (see Issue 1)

Re-derived independently, exact sympy arithmetic
(`ref_symbolic_targets.py`):

- **Route A**: `M(c)^2 = min(1,E/c)`, so `E[M(c)^2] = ∫_0^c (e/c)e^{-e}de
  + e^{-c} = (1-e^{-c})/c`. Exact match (S1).
- **Route B**: `∫_0^1 x^2·2Kx(1-x^2)^{K-1}dx = 1/(K+1)` symbolically in
  `K`, by two referee routes (direct, and `u=x^2` → `K·B(2,K)`); the
  Poisson(`c`) mixture with the `K=0` term `1` sums in closed form to
  the same `(1-e^{-c})/c` (S2–S3).
- **`p=1` consistency (referee-added)**: `E[min(1,√(E/c))] = ∫_0^1
  e^{-ct^2}dt` exactly (S5) — the conjectured law's mean equals the
  PROVED `φ_∞(c)`, as it must.
- **Necessary-condition sandwich (referee-added)**: `φ_∞(c)^2 ≤
  (1-e^{-c})/c ≤ φ_∞(c)` on a grid `c ∈ [0.01,100]` (S6) — conditions
  the *true* `E[M(c)^2]` must satisfy; the conjectured target passes,
  so the target is not refutable by the proved mean alone.

**Cross-check against proved instances.** `1/(K+1)` gives `1/2, 1/3,
1/4` at `K=1,2,3`; the referee re-integrated the archive's *proved*
densities `2x`, `4x(1-x^2)`, `6x(1-x^2)^2` and got exactly `1/2`,
`1/3`, `1/4` (S4) — matching `THEOREM.md` §5.3 (K=1, implicit) and the
K=2/K=3 documents' reported `E[M_2^2]=1/3`, `E[M_3^2]=1/4`. So the
general-`K` formula is anchored unconditionally at `K ≤ 3` (and
trivially at `K=0`).

**Framing check.** §3.1 states explicitly that Route A/Route B
agreement "is **not** new evidence for Conjecture 2 (routes A and B are
two ways of unpacking the *same* conjectured object)", and §8 repeats
that `E[M(c)^2]` "was **not** independently re-derived … only computed
*from the conjectured law itself* … a target, not a derivation of that
target." That is the correct framing and it is genuinely maintained —
no passage offers the closed forms as evidence. See Issue 1 for the one
shorthand-labeling nit.

## 3. Lemmas B1–B3 (§3.2) — VERIFIED and strengthened

**Continuum derivations.** B1 (`P(same)=E[L]=1/2`, `L~Unif(0,1)` by
Fact A): correct. B2 (sub-density `ℓ·dℓ` normalized by `1/2` → `2ℓ`;
offset `Unif(0,ℓ)` given uniformity within the block's cyclic order):
correct, with the offset step resting on the same
exchangeability/rotational-order reading of Definition 2 that the rest
of the archive already uses — and nailed exactly by its discrete
analogue below. B3 (sub-density `1·dℓ_1·(1-ℓ_1)·dℓ_2/(1-ℓ_1) =
dℓ_1dℓ_2` on the simplex): correct, using the same `PD(1)`
residual/size-biased citation as `THEOREM.md` Prop. 2.4 and the
accepted K=2/K=3 documents; the referee additionally checked the
simplex mass integrates to `1/2 = P(different)`, consistent with B1
(S7).

**Discrete cross-checks, re-enumerated from scratch**
(`ref_discrete_enum.py`, exact integer counts, `n=2,…,8` — one order
beyond the front's `n≤7`):

- `P(1,2 same cycle) = 1/2` exactly, every `n=2..8`.
- Same cycle of length `ℓ`: forward-distance counts uniform across `d`
  for every `ℓ`, every `n=3..8`.
- Different cycles: a single count value across all `(ℓ_1,ℓ_2)` cells,
  every `n=3..8`.

**Referee strengthening**: every cell in *both* the B2 and B3 tables
carries count exactly `(n-2)!` (referee-derived closed form; the
telescoping `C(n-2,ℓ-2)(ℓ-2)!(n-ℓ)! = (n-2)!` and
`C(n-2,ℓ_1-1)(ℓ_1-1)!·C(n-1-ℓ_1,ℓ_2-1)(ℓ_2-1)!·(n-ℓ_1-ℓ_2)! =
(n-2)!`), verified in every cell with cell-total completeness checks —
a stronger statement than the front's "uniform within ℓ" / "single
distinct value", and it confirms the front's printed log values (`1,
2, 6, 24, 120` at `n=3..7` are exactly `(n-2)!`). Zero deviations
anywhere.

## 4. Lemma B4 (§3.4) — VERIFIED

**Logic.** Airtight. A point's cyclic status depends only on the
out-edges along its own forward orbit. If no member of the shared
`π`-cycle is rerouted, every member's `f`-image equals its `π`-image,
so the cycle survives verbatim and all `ℓ` members (both query points
included) are cyclic. External points rerouted *onto* the cycle add
in-edges only — they cannot change any member's out-edge, hence cannot
break the cycle. The probability `(1-c/n)^ℓ` is exact (the `ξ_i` are
i.i.d. Bernoulli(`c/n`), independent of `π`, so conditioning on the
cycle and the query points does not disturb it), and `→ e^{-ct}` at
fixed `t=ℓ/n`. The strictness claim `e^{-ct} < e^{-ct^2}` for
`t∈(0,1)` is correct (`t > t^2`; S8).

**Fresh-seed simulation** (`ref_mc_checks.py`, seeds `20260859000`
c=1 and `20260859001` c=4, `n=2000`, 20,000 trials each, cyclic set by
pointer-doubling cross-validated against an independent in-degree
peeling implementation): **zero** violations of `{intact} ⊆ {both
cyclic}` in 5,326 (c=1) + 1,193 (c=4) intact trials, and empirical
`P(both) ≥ P(intact)` in every populated bucket at both `c` values.
The front's own within-one-run, empirical-vs-empirical comparison
design is the *right* one: the referee notes that comparing a
bucket-averaged `g` against the bound evaluated at the bucket midpoint
can produce spurious ~1–2σ dips (the `ℓ`-density within a bucket is
tilted), which is precisely the class of artifact the front's design
avoids.

## 5. The counterexample (§4.2) — VERIFIED EXACTLY; scope framing: two repairable gaps (Issues 2, 3)

**Hand check.** `π=(1 2 3)(4 5 6)`. Reroute `1→5`: orbit of 2 is
`2→3→1→5→6→4→5→…` (never returns), `{4,5,6}` intact → cyclic set
`{4,5,6}`, count 3. Add `3→2`: since `f(2)=3`, the pair closes
`3→2→3` → cyclic set `{2,3,4,5,6}`, count 5. Strict increase `3→5`.

**Code check** (`ref_counterexample.py`): two independent cyclic-set
algorithms (orbit-following; in-degree peeling), asserted equal on
every evaluation. All claimed sets and counts reproduce exactly,
including the document's quoted trajectory.

**Does it rule out what §4.3 says it rules out?** The *conclusions* of
§4.3 are all true, and the "What this does NOT show" paragraph is
correctly scoped (it concedes that richer-state Markovianity and
cleverer PDE routes remain open — the counterexample indeed does not
touch those). But two steps between the exhibited certificate and the
stated PROVED claims are not in the document (both easy; both verified
by the referee):

- *Finite→continuum* (Issue 2): §4.3's first PROVED sentence is about
  the continuum coupling of §4.1; the certificate is an `n=6`
  finite-model computation. The bridge is a five-line
  positive-probability event, supplied in Issue 2 below.
- *Deterministic-direction-in-`M`* (Issue 3): the document exhibits a
  down-move from `M=1` (first reroute) and an up-move from `M=1/2`
  (second reroute). Those two transitions alone are *consistent* with
  a direction function of `M` ("down at 1, up at 1/2"). The refutation
  needs both directions from a *single* state; the referee's
  exhaustive scan of all 30 possible second reroutes from the
  document's own K=1 configuration shows 9 increase the count, 7
  decrease it (e.g. `5→4` gives count 2), 14 leave it unchanged — both
  directions from one configuration, hence from one `M` value. Claim
  repaired with the document's own example.

## 6. The obstruction analysis (§3.3, §6) — honest, with one over-assertive sentence (Issue 4)

§3.3 is exemplary: "**This is stated as a located, honest gap, not a
proof of impossibility**… It is entirely possible a cleverer joint
construction exists; this document did not find one." That is exactly
the located-open-problem register. The technical observation it rests
on is accurate: Definition 3's `(Θ_j,E_j)` device is certified
(Prop. 2.4) only to reproduce the *one-point marginal*; nothing in
`THEOREM.md` supplies a joint two-reference-point version, and the
document correctly declines to invent one without proof.

§6's *comparison* with Conjecture 1's obstruction accurately reflects
the K=3 document's own §7: shapes growing with
set-partitions-into-cycles of `K` labels, "faster than `K!`" — the
quoted characterization matches the source. The distinction drawn
(count-growth in a solvable setup vs. no correct joint setup yet at
`p=2`) is fair and, if anything, understates the document's own
progress. One sentence overshoots — see Issue 4.

## 7. The exploratory numerics (§3.5) — labeling discipline VERIFIED

Every number in §3.5 is framed as exploratory or harness-sanity;
nowhere is any of it offered as evidence for Conjecture 2 — the
section says so twice, and §8/§9 repeat it. The harness-sanity values
quoted are the right targets: referee computes `φ_∞(1)=0.7468241`,
`(1-e^{-1})=0.6321206`, `φ_∞(4)=0.4410407`, `(1-e^{-4})/4=0.2454211`
(S9) — the document's `0.74682 / 0.63212 / 0.44104 / 0.24542` are all
correct to the quoted precision, and the front's log values
(`0.74635`, `0.63164` at c=1; `0.44128`, `0.24559` at c=4) match its
ATTEMPT quotes verbatim. The referee's own fresh-seed MC reproduces
the qualitative claims independently: `g(ℓ)` matches *neither*
`e^{-cℓ^2}` (max |z| = 15.3 / 18.9 at c=1/4) nor `e^{-2cℓ^2}` (39.1 /
22.4), and `ρ(ℓ)` (computed against the empirical finite-`n`
marginal, per the front's stated design) is high at small/mid `ℓ` and
decreases toward `ℓ→1` at both `c` values (c=1: ~0.92→0.60; c=4:
~0.87→0.29) — the same reproducible pattern the front reports.

One observational note (not a violation): the second-moment
harness-sanity comparison is against the *conjectured* `(1-e^{-c})/c`,
so the actual harness-validation load is carried by the mean
comparison against the PROVED `φ_∞(c)` (which passes at both `c` in
both the front's runs and the referee's). The document claims nothing
evidential from the second-moment agreement, so discipline is intact;
a maximally clean phrasing would call the mean check the sanity check
and the second-moment line an observation.

## 8. The self-disclosed docstring mislabel (§3.5 honest process note) — corrected framing VERIFIED

The corrected statement is right on all three counts: (i) `e^{-cℓ^2}`
is `THEOREM.md` §3's *marginal* `P(x cyclic | own block length = ℓ)`
(Theorem 1 Step 5, eq. 3.4, with `T_0 = ℓ` the size-biased block
length); (ii) the intact-block probability is `e^{-cℓ}` (Lemma B4);
(iii) `e^{-cℓ^2} > e^{-cℓ}` strictly on `ℓ∈(0,1)` (S8), so the
mislabeled candidate was a strictly *larger* quantity and never a
valid lower bound. The narrative of how the mislabel was caught (an
apparent dip of `g` below the mistaken "bound" at the smallest bucket)
is consistent with the front's own printed table (`g=0.90378` vs
`e^{-cℓ^2}=0.99610` at bucket 0 of the c=1 run) and with the referee's
midpoint-vs-bucket-average observation in §4 above. The disclosure
affects a docstring only; no numeric output is implicated, and the
front's timeline (`.py` mtime 17:43:40, after the intact-block check,
matching §0's stated fix time) checks out.

## Provenance / governance checks

- `DERIVATION_PREREG.md` mtime (17:32:40) predates every script and
  log in the directory; `ATTEMPT.md` (17:48) postdates all of them;
  the §0 timeline matches the on-disk mtimes at every entry, including
  the docstring-fix entry.
- Seeds: `grep -rn "20260858"` hits only the front's own directory
  plus the two reservation lines — matching the front's claim; the
  front's Seeds table matches the three logs' printed seeds exactly.
  The referee range was untouched by the front, as claimed.
- The front created no `adversarial/` directory and dispatched no
  referee, as required; `THEOREM.md` and governance files unmodified.
- The claim that neither closed form appears in `THEOREM.md` was
  grep-verified (the `K=2,3` *instances* appear in the two attempt
  documents, correctly attributed there; the general-`K` form and the
  mixture form are new).

## Named issues

**Issue 1 (labeling shorthand; minor, wording only).** The executive
summary calls `E[M_K^2]=1/(K+1)` "a bonus exact fact … for every `K`",
and the §7/§9 tables label both closed forms "PROVED (symbolic, new)".
As statements *about the model*, these are unconditional only for
`K∈{0,1,2,3}` (via the proved densities — referee-verified anchors);
for `K≥4`, and for `E[M(c)^2]=(1-e^{-c})/c` as a statement about the
true `M(c)`, they are exactly as conjectural as Conjectures 1/2. The
document *does* state this correctly and explicitly where it matters
(§3.1's "not new evidence… two ways of unpacking the same conjectured
object"; §8's "a target, not a derivation of that target"), so nothing
is smuggled — but the table rows should read "PROVED as computations
on the conjectured law (target)", and the executive summary's "exact
fact for every `K`" should carry the same qualifier. A future
integration step must not lift the table rows without the §8 caveat.

**Issue 2 (proof-level gap, repaired; minor).** §4.3 states the
non-monotonicity PROVED claim for the *continuum* coupling of §4.1,
while §4.2's certificate is the exact `n=6` finite-model computation;
the bridge is asserted only as "the mechanism … is general". The
bridge is true and short — for the record: under the §4.1 coupling,
with positive probability exactly one mark arrives by `c_1`, at a
point `x` of a block `C` of length `L>0` with destination outside `C`
(so `M(c_1)=1-L`, all of `C` dead), and exactly one further mark
arrives in `(c_1,c_2]` at a point `y∈C` with destination `z` in the
forward arc strictly between `x` and `y` (an event of positive
probability given the first, since that arc has positive length a.s.);
then `z`'s forward path reaches `y` before `x`, so `y→z→…→y` closes a
new cycle of positive mass while destroying nothing previously cyclic
(only `y`'s out-edge changed, and `y` was dead), whence
`M(c_2)>M(c_1)` with positive probability. The document should either
include this paragraph or restate §4.3's first PROVED claim at the
finite-model level with the continuum transfer flagged as the same
mechanism.

**Issue 3 (proof-level gap, repaired with the document's own example;
minor).** §4.3's consequence "cannot be Markov … in any way that would
make 'does `M` go up or down at the next mark' a deterministic-in-
`M(c)` question" does not follow from the document's two exhibited
transitions alone (down from `M=1`, up from `M=1/2` — jointly
consistent with a direction *function* of `M`). It does follow from
the referee's exhaustive scan (`ref_counterexample.log`): from the
document's own K=1 configuration (one positive-probability state, one
`M` value), 9 of the 30 possible second reroutes increase the cyclic
count and 7 decrease it (e.g. `5→4` → count 2, vs. the exhibited
`3→2` → count 5). One sentence citing a single down-move from the
same configuration would close the gap.

**Issue 4 (over-assertive sentence in §6; minor, wording only).**
§6's bolded "Both are instances of one fact: … **no proper summary of
it smaller than 'the whole configuration' … carries enough information
to predict its own future evolution or its own multi-point
correlations**" is a universal negative stated as fact, carrying none
of the governance header's four labels, and it is not established —
what is actually demonstrated is that three *specific* summaries (the
scalar `M`, the pair status, the count `K`) fail for the *specific*
purposes examined (and for `M`, strictly only via Issues 2–3's
repaired forms). The surrounding text is honest (§3.3's explicit
"not a proof of impossibility"; §8's "the obstruction is 'no correct
joint construction was found'"), so this is one sentence to downgrade
to diagnosis/heuristic phrasing, not a systemic overclaim.

**Nano-nits (no action required).** (a) `same_cycle_exact_check.log`
cites "ATTEMPT.md Section 3.3" for the continuum `1/2` fact that lives
in §3.2. (b) §3.4's "`→ e^{-cℓ/n}`" momentarily uses `ℓ` for the
member count where the displayed limit needs `t=ℓ/n`; the intended
`e^{-ct}` appears correctly in the next sentence. (c) §3.2's
parenthetical that the K=2/K=3 Bell-number machinery is "directly
reusable here without re-derivation" for `p≥3` query points is an
unproved plausibility aside sitting inside a PROVED-labeled section;
it is clearly an aside, but a "(plausible, unproved)" tag would match
house style. (d) A cross-reference to the K=2/K=3 documents' proved
`E[M_2^2]=1/3`, `E[M_3^2]=1/4` at the point where `1/(K+1)` is
announced would let §3.1 claim its unconditional anchors explicitly.

## Referee verification summary

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | Hausdorff determinacy + Fubini architecture | prose re-derivation vs THEOREM.md §2.4/§3 | correct as stated |
| 2 | `E[M(c)^2]=(1-e^{-c})/c` | 2 symbolic routes, exact | exact match |
| 2 | `E[M_K^2]=1/(K+1)` | 2 symbolic routes, exact, symbolic in `K` | exact match |
| 2 | anchors `K=1,2,3` → `1/2,1/3,1/4` | integrate proved densities | exact match |
| 2 | mean of conjectured law `= φ_∞(c)` | symbolic (referee-added) | exact |
| 2 | `φ_∞^2 ≤ target ≤ φ_∞` | numeric grid (referee-added) | holds |
| 3 | B1 `=1/2`; B2 uniform; B3 constant | from-scratch enumeration `n=2..8` | 0 deviations; every cell `=(n-2)!` (strengthened) |
| 4 | B4 logic + inclusion | re-derivation + fresh-seed MC ×2 | 0 violations / 6,519 intact trials |
| 5 | counterexample `3→5` | hand + 2 independent algorithms | exact |
| 5 | both jump directions from one state | exhaustive 30-case scan (referee-added) | 9 up / 7 down / 14 flat |
| 7 | harness targets `0.74682/0.63212/0.44104/0.24542` | mpmath | all correct |
| 7 | `g` ≠ both candidates; `ρ` decreasing | fresh-seed MC ×2 | reproduced |
| 8 | corrected mislabel framing | symbolic + THEOREM.md §3 | correct |

## Files

| File | Role |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `ref_symbolic_targets.py` / `.log` | items 1–2, 8: all symbolic re-derivations (S1–S9b) |
| `ref_discrete_enum.py` / `.log` | item 3: from-scratch exact enumeration, `n=2..8` |
| `ref_counterexample.py` / `.log` | item 5: exact counterexample + 30-case direction scan |
| `ref_mc_checks.py` / `.log` | items 4, 7: fresh-seed MC (seeds `20260859000`, `20260859001`) |

**Final verdict: SOUND WITH NAMED ISSUES — ACCEPT for catalogue** at
the claimed tier (honest non-closure with named partial results).
Conditions attached to any future integration: carry Issue 1's
qualifier wherever the closed forms are restated; incorporate the
Issue 2/Issue 3 repair paragraphs (or equivalent) if §4's negative
finding is ever cited as PROVED for the continuum coupling; rephrase
§6's bolded sentence per Issue 4.
