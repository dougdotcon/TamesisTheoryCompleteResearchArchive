# REFEREE REPORT — `GAMMA-C-GAMMA-CONSTRUCTION-ATTEMPT`

**Target:** `.../gamma_gap1_cancellation_tracking_attempt/gamma_c_gamma_construction_attempt/ATTEMPT.md`
(Wave 28, front (b), authorized by `DISC-DEC-131`)

**Referee:** hostile, independent adversarial session. Read, in full and in
prose, before opening any script belonging to the target: `THEOREM.md`'s
γ-scaling-law section (Estágios 26, 33, 36, 49, plus surrounding context);
`.../gamma_gap1_cancellation_tracking_attempt/ATTEMPT.md` (684 lines, the
immediate predecessor) and its own `adversarial/REFEREE_REPORT.md` (370
lines); `.../gamma_second_order_attempt/ATTEMPT.md` (633 lines, for Lemma
E, `D_0(γ)`, and the order-2 cumulant heuristic `E_heuristic(γ)`);
`.../gamma_gap1_mgf_attempt/ATTEMPT.md` (608 lines, for the original
Bulk/Tail Lemma and `x(D)`'s exact cubic form); `.../gamma_scaling_attempt/ATTEMPT.md`
(592 lines, wave-17 ultimate ancestor, for Lemma 1 and the `A_k=E_M[P_{k,M}]`
definition). Only after all of that was the target's own `ATTEMPT.md` and
its nine scripts (`01`–`09`) read.

This is pure combinatorial/asymptotic mathematics internal to this
archive, about a specific random-permutation-with-reroutes ensemble — no
Millennium Prize Problem, no physics claim, anywhere in this document or
its target.

---

## VERDICT: **SOUND WITH NAMED ISSUES — ACCEPT for catalogue**

Every load-bearing mathematical claim independently checked below — the
`2F0` identity (matching the orchestrating session's own pre-dispatch
spot-check exactly), the cumulant/central-moment machinery, the exact
`x(D)` cubic, the exact `E[x(D)^4]`, the validity of the Lyapunov-based
bulk and small-`k` bounds, the unbounded `(ln n)^{1.5}` growth of the
improvement ratio, the final `n_0(γ)` table, and the honesty of the
Charlier non-identification disclosure — reproduces correctly, in every
case either exactly (zero symbolic difference / exact rational agreement)
or to bisection precision. **One real, verifiable, MODERATE-severity
issue was found**: a headline interpretive claim in §5 ("the shift...
[is] comparable to, or smaller than, the residual gap already present at
order 2") is contradicted by the front's own reported numbers at all
three tested `γ`, and is repeated in three prominent locations (VERDICT,
§5, Scorecard) — structurally the same pattern (a claim mis-stated in
exactly the VERDICT/body/Scorecard triad) as the one finding this
front's own predecessor's referee caught. It does not affect any proved
result, the `n_0(γ)` table, or the non-closure conclusion. **One
trivial/cosmetic finding** (a numeric "exceeds" that is technically
"approaches") is also noted. The front's own self-critical framing of
item 2 ("the SAME KIND of contribution Estágio 49 said a ninth front
should move past") is **assessed as accurate** — see the dedicated
section below.

---

## Independent verification, item by item

### (a) §3's cumulant machinery and the two classical Binomial
central-moment formulas

Re-derived `μ_3=kγ(1-γ)(1-2γ)` and `μ_4=kγ(1-γ)[1+3(k-2)γ(1-γ)]`
independently, via a **different algebraic route** than the target's
cumulant recursion: the elementary "sum of `k` i.i.d. mean-zero
variables" identities `E[D^3]=k·E[Y^3]`, `E[D^4]=k·E[Y^4]+3k(k-1)(E[Y^2])^2`
(`adv01_moments_iid_route.py`). **Exact zero symbolic difference** against
both cited classical formulas — independently confirming both the
ancestor's citation (`gamma_second_order_attempt/ATTEMPT.md` §5) and the
target's own script `02` cross-check.

Re-derived `x(D)`'s exact cubic coefficients `c_0,\ldots,c_3` a **third**
independent way (`sympy.diff`-based Taylor coefficients at `D=0`, rather
than the target's `Poly.coeff_monomial` route) — exact zero difference
against the referee-corrected cited forms (`adv02_Ex4_sympy_stats_route.py`).

Re-derived `E[x(D)^4]` two more independent ways: (i) `sympy.stats.Binomial`'s
own moment engine (a **fourth**, fully independent computational route,
built from the raw pmf, not moments/cumulants at all) at 24 fresh
`(k,n,γ)` points (`adv02...py`); (ii) direct `sympy.summation` over the
exact pmf plus brute-force exact-`Fraction` summation, at 5 **fresh**
`(k,n,γ)` triples not used anywhere in the target's own scripts
(`adv03_Ex4_freshpoints_crosscheck.py`) — **0/5 mismatches**. Together
with the target's own script `02`/`03` checks (48 brute-force pmf checks,
5-point brute-force `E[x(D)^4]` cross-check, `γ=1` degenerate sanity),
the exact-moment machinery feeding §4 is now confirmed **five
independent ways**, not just the two the target itself ran.

### (b)/(c) The Lyapunov step and the three validity checks

**Mathematical validity, checked by hand.** The chain
`E[|x(D)|^3e^{|x(D)|}\mathbb 1_{\text{bulk}}] \le e^{H_\Theta}E[|x(D)|^3\mathbb 1_{\text{bulk}}]
\le e^{H_\Theta}E[|x(D)|^3] \le e^{H_\Theta}(E[x(D)^4])^{3/4}` is valid at
every step: the first inequality holds because `H_\Theta` is *defined* as
`\max_{|D|\le\Theta_k}|x_k(D)|`, so `e^{|x(D)|}\le e^{H_\Theta}`
pointwise on the bulk event, and the deterministic factor pulls out of
the expectation legitimately; the second drops a `\{0,1\}`-indicator
against a non-negative integrand (trivially valid); the third is
**Lyapunov's inequality** for power means of a non-negative random
variable (`(E[Y^3])^{1/3}\le(E[Y^4])^{1/4}`, standard, elementary,
correctly applied — not misused or mis-stated in any way). No gap found
in either the `e^{H_\Theta}`-factoring step or the Lyapunov/Hölder step
itself.

**Re-running the three validity checks at points the target did not
test.** Built the pointwise (unrestricted) Lyapunov bound
`R_k^{\text{bound}}:=\tfrac16e^{H_{\text{full}}}(E[x(D)^4])^{3/4}` fully
independently (own `c_i`, own moment recursion, own exact-cubic-max
routine) and checked it against `R_k^{\text{exact}}` (direct exact
Binomial-pmf summation) at **10 fresh `(k,n,γ)` points**, deliberately
chosen outside the target's own script `06` grid (`k\in\{10,30,80\}`,
`n\in\{1000,20000\}`, `γ\in\{0.2,0.5,0.8\}`) — including small `k=2`,
large `k=100`, extreme `γ=0.03,0.95,0.99`, and `n` up to `50000`
(`adv06_lyapunov_bound_freshpoints.py`). **0/10 violations**, bound/exact
ratios `1.27\times`–`3.22\times` (modest, not suspiciously loose or
suspiciously tight) — the bound is genuinely valid, not merely valid on
the target's own chosen grid.

**The `(\ln n)^{1.5}`-growth claim.** The target's own script `04` fits
the growth exponent from only the **first and last** of 8 tested `n`-scales
per `γ` (a 2-point fit) — a legitimate concern that this could
understate real curvature. Re-fit **all 8 points** by ordinary
least-squares for `γ=0.5` (the target's own full-table row, `n=10^{10}`
through `10^{100}`): slope `1.4990`, versus the target's 2-point value
`1.499` — **the two agree to four significant figures**, meaning the
`\log(\text{ratio})` vs. `\log\ln n` relationship is genuinely
log-log-linear across the whole tested range, not an artifact of
endpoint selection. This *strengthens* confidence in the `\approx1.5`
exponent claim rather than weakening it. The disclosed `γ=0.99` anomaly
(fitted exponent `5.065` over the same range) was not independently
re-investigated — the target discloses it honestly as unresolved, and
nothing in its own construction depends on resolving it (the final
`n_0(γ)` table for `γ=0.99` is separately verified below via direct
bisection, not via the exponent fit).

### (d) Small-`k` residual fix at `γ=0.99, 0.90`

Genuinely handled, not merely asserted. Script `06`'s own term-by-term
breakdown (re-read, not re-run, since it is a direct diagnostic printout)
shows the small-`k` residual dominating the *pre-fix* (v1, bulk-only)
assembly's total budget at exactly `γ=0.99` (`81.8\%` of the total) and
`γ=0.90` (`99.7\%`) — nowhere else in the 8-point grid. Script `09` then
applies the identical Lyapunov/exact-4th-moment mechanism to this term
(self-derived, since the predecessor's own small-`k` formula carried an
un-derivable `e^{1/2}` factor the target's required reading did not
source precisely enough to reuse — an honest, disclosed choice, not a
shortcut). The resulting v2 table shows exactly `γ=0.99,0.90,0.70`
improving over v1 (the three points where the fix could matter), while
`γ=0.50,0.30,0.10,0.05,0.01` are unchanged to the digits shown (bulk was
always binding there, as expected). Independently re-bisected
`γ=0.9`'s v2 value from scratch (own `c_i`, own `E[x^4]`, own bisection —
see (e) below): `10^{10.153568}`, matching the target's own
`10^{10.1536}` to `3\times10^{-5}` decades.

### (e) The final `n_0(γ)` table (8 rows)

Reassembled the **entire** hybrid construction (`K_{\text{real}}`,
`\lambda_{\text{tight}}`, `C0_{\text{tight\_Bernstein}}`, the Lyapunov
bulk term, the Bernstein-with-slack tail term, the Lyapunov small-`k`
term, the margin search, log-domain bisection) fresh, from the formulas
quoted in the target's own §1–§4 prose, and independently bisected 3 of
the 8 rows — `γ=0.5` (bulk-binding), `γ=0.9` (small-`k`-binding
pre-fix), `γ=0.01` (extreme small-`γ`) — deliberately spanning both
regimes (`adv05_n0_reassembly.py`):

| `γ` | target's `log₁₀n₀` | this referee's `log₁₀n₀` | `|`diff`|` (decades) |
|---|---|---|---|
| 0.5  | 16.4628  | 16.462757 | `4.3×10⁻⁵` |
| 0.9  | 10.1536  | 10.153568 | `3.2×10⁻⁵` |
| 0.01 | 31.4117  | 31.411661 | `3.9×10⁻⁵` |

All three match to within bisection precision. Also independently
verified, by direct subtraction, that the "decades saved" column against
Estágio 49's cited table (`15.42,19.09,30.45,35.49,39.30,47.72,52.08,61.17`)
is arithmetically correct at **all 8 rows** (`3.46, 8.94, 19.18, 19.03,
18.91, 22.72, 24.96, 29.76` — every value matches the published table
exactly) — unlike the predecessor front, whose analogous "decades saved"
summary contained a genuine three-place mislabeling error that its own
referee had to catch. This front's arithmetic here is clean.

### (f) §5's higher-order Taylor/cumulant evidence for `E_heuristic(γ)`

**Numerics independently reproduced.** Built the full order-6 exact
Taylor/cumulant machinery fresh (own moment recursion to order 18, own
`E[x(D)^j]` for `j=0,\ldots,6`, own summation and 2-point Richardson
extrapolation) and re-ran the `γ=0.5` case at `n=4096` and `n=16384`
(`adv04_order6_taylor_recheck.py`). Result: `E_n^{(2)}=-0.2287073976`
and `-0.2347117482`; `E_n^{(6)}=-0.2306615245` and `-0.2356654573`;
Richardson-extrapolated order-2 `\to-0.2407160987`, order-6
`\to-0.2406693901` — **matching the target's own log
(`08_higher_order_taylor_check.log`) to every digit shown.** The raw
computation is correct.

**A real interpretive overstatement, however.** The target's §5 (echoed
in the up-front VERDICT and the §9 Scorecard — three places) states:
*"the four extra exact orders shift the extrapolated limit by only
`4$–`8\times10^{-5}$` — comparable to, or smaller than, the residual gap
already present at order 2."* Checking this claim by pure arithmetic
against the target's own three-row table (`γ=0.3,0.5,0.7`):

| `γ` | order-2 residual `|`o2`-`E_h`|` | shift `|`o6`-`o2`|` | ratio shift/residual |
|---|---|---|---|
| 0.3 | `6.41\times10^{-5}` | `8.41\times10^{-5}` | `1.31\times` |
| 0.5 | `2.46\times10^{-5}` | `4.67\times10^{-5}` | `1.90\times` |
| 0.7 | `0.98\times10^{-5}` | `3.61\times10^{-5}` | `3.68\times` |

**At all three tested `γ`, the order-2→order-6 shift *exceeds* the
order-2 residual gap — by `1.3\times` to `3.7\times` — the opposite of
"comparable to, or smaller than."** Equivalently: at every tested `γ`,
the order-6 extrapolated value sits *farther* from `E_{\text{heuristic}}(γ)`
than the order-2 value does (`|`o6`-`E_h`|` exceeds `|`o2`-`E_h`|` by a
factor of `2.3\times$–`4.7\times$` in the table itself). This does not
mean the evidence is worthless — a `\lesssim10^{-4}`-scale shift from
only two extra orders, extrapolated from a fairly modest `n`-range
(`n\le2^{14}=16384`, a 2-point Richardson fit) is still small in
absolute terms, and could easily be dominated by extrapolation-model
mismatch (the order-6 series need not obey the same `1/\sqrt n`
correction-rate assumption as order-2) rather than a genuine surviving
`\Theta(1)` term — but the specific comparative language used ("comparable
to, or smaller than, the residual gap") is not what the front's own
numbers, taken at face value, show. This is a **MODERATE**-severity
presentational finding, structurally the same class of issue (a
mis-stated summary comparison, repeated in the VERDICT/body/Scorecard
triad) as the one finding the *predecessor* front's own referee caught
— worth a dated correction, but affecting neither the correctness of the
underlying computation nor the front's honest bottom line that this is
"evidence, not proof."

### (g) The Charlier-polynomial non-identification (§2)

Correctly characterized as a genuine, honestly-disclosed near-miss, not
an error being hidden. Re-read script `01`'s own log: the naive parameter
match (`x=k-n-1`, `a=(1-γ)n/γ`) reproduces `A_k` at `k=0` only; `k=1`
leaves an **exact, `n`-independent residual `-2γ`** (not an artifact of
rounding or a near-zero numerical coincidence), and `k=2,\ldots,6` leave
increasingly complex nonzero polynomial residuals — a real, structural
mismatch, not a sign flip away from working. The `2F0` identity itself
(Part B) — the only claim actually used downstream — was independently
verified by the orchestrating session's own pre-dispatch `sympy` spot-
check (`k=0,\ldots,6`, `n,γ` fully symbolic, zero discrepancy) and is
re-confirmed here by direct reading of `01_exact_hypergeometric_structure.log`
(the same `k=0,\ldots,6` symbolic zero-difference result, plus `539`
Pochhammer-form checks and `40` numeric spot checks, `0` mismatches
overall) — matching the orchestrator's own verification range exactly.

---

## Assessment of the self-critical framing (item 2 vs. Estágio 49's warning)

The mandate's dispatching text asks whether "the SAME KIND of
contribution Estágio 49 explicitly said a ninth front should move past"
is an accurate characterization, or needs correction in either direction.
**Assessed: accurate, and appropriately nuanced — no correction needed.**

Two things are simultaneously true, and the front says both, correctly:

1. **The mechanism is genuinely different in kind**, not just a tighter
   constant on the same kind of bound. The four prior `n_0(γ)`-tightening
   fronts (Estágios 33, 36, 37, 49) each sharpened a *tail-probability*
   or *coefficient-cancellation* step, each time removing a **fixed**
   multiplicative constant (`4\times$` here, `14\times$` there). This
   front instead diagnosed that the predecessor's **bulk** term bounded
   an *expectation* (dominated by typical `D`, scale `\sqrt k`) by a
   *deterministic worst case* evaluated at the bulk radius (scale
   `\sqrt{k\ln n}$`, growing relative to typical scale as `n\to\infty$) —
   a **structural** mismatch between the quantity being bounded and where
   the bound is evaluated, not a loose constant. Independently confirmed
   above: the resulting improvement ratio genuinely grows without bound
   (`\sim(\ln n)^{1.5}$`, confirmed via full 8-point regression, not just
   the target's 2-point fit) — this is not spin.
2. **The outcome is nonetheless still "more `n_0(γ)`-tightening, `C(γ)`
   still untouched"** — exactly the category Estágio 49's closing
   paragraph said a ninth front should move past. `n_0(γ)` remains
   `10^{10.2}$`–`10^{31.4}$`, astronomically large by this lineage's own
   established convention since Estágio 36, and none of this front's three
   contributions (the `2F0` fact, the Lyapunov refinement, the order-6
   Taylor evidence) narrows, bounds, or characterizes `C(γ)` itself in any
   way — confirmed by direct reading of §7 ("`C(γ)` for `γ\in(0,1)` itself
   is NOT constructed... this front's contributions are entirely on the
   *supporting* side").

These two facts do not contradict each other, and the front's own prose
holds them apart correctly rather than blurring them to sound better. If
anything the front is mildly conservative here, not inflated: it could
have leaned harder on point 1 (a genuinely new proof *technique* in this
sub-lineage) to soften point 2, but instead leads with point 2's
self-criticism in the VERDICT's own words. No overclaiming or
underclaiming found on this specific question.

## Overclaim/underclaim check on the document as a whole

No instance of overclaiming was found beyond the one MODERATE §5 finding
above (which itself inflates confidence in supporting *evidence*, not any
proved claim). Two very minor, cosmetic points, not raised to Finding
status: (i) §4's prose states "at `n=10^{60}`, the ratio already exceeds
`6{,}600`" for `γ=0.5`; the script `04` log's actual value is `6597.317`,
technically *below*, not above, `6{,}600` (a `0.04\%$` discrepancy — better
phrased "approaches" or "reaches about"); (ii) the `2F0`/hypergeometric
fact (§2) is, if anything, slightly undersold relative to its genuine
novelty — no ancestor `ATTEMPT.md` in this entire lineage (checked by
`grep` across all five required-reading documents) mentions
hypergeometric functions, Pochhammer ratios, or orthogonal polynomials at
all, so this is a real "nobody looked at it this way before" observation,
correctly flagged as new but appropriately not oversold given it does not
yet lead anywhere toward `C(γ)`.

---

## Scope, seed, and governance discipline

- **File-scope discipline.** `git status --porcelain` (read-only) at the
  repository root shows exactly two untracked entries: the target's own
  new `gamma_c_gamma_construction_attempt/` directory, and an unrelated
  abandoned/stalled directory from a completely different sub-lineage
  (`conjecture2_direct_attempt/.../k3_full_cdf_attempt_ABANDONED_STALLED/`,
  pre-existing, untouched by this front). **No modified (tracked) file
  anywhere in the repository** — `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
  `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
  every ancestor `ATTEMPT.md`/`adversarial/` file, and every sibling
  directory are all untouched.
- **Seed range.** `grep -rn "20260941" 05_DISCOVERY_LAB/` (run
  independently by this referee) finds only `DECISION_LEDGER.yaml`'s own
  reservation line (`20260941000-20260941999 (frente b)`) — confirmed
  **unused**, matching the front's own before/after disclosure exactly.
- **`random`/seed usage.** `grep -n "random\.\|seed("` across the target's
  nine scripts finds exactly one use: `random.seed(1)` in script `01`
  (a disclosed, fixed, 40-point deterministic sanity check) — matches the
  front's own characterization; not drawn from the reserved block.
- **No `git` command** of any kind appears in any of the target's nine
  scripts (checked via `grep` for `subprocess`, `os.system`, and literal
  `git ` invocations — none found); no git command was run by this
  referee either beyond the read-only `git status` above.
- `DECISION_LEDGER.yaml` was grepped (read-only) and confirms the
  `DISC-DEC-131` authorization entry exists at the cited location.

---

## Summary assessment

This front honestly does not achieve its mandate — `C(γ)` for `γ\in(0,1)`
remains exactly as open after this front as before it, and the document
says so plainly, repeatedly, and in the first sentence of its own
VERDICT. What it does deliver is real and independently verified: a
genuinely new (if not yet fruitful) exact structural fact about `A_k`;
a substantively different, correctly-derived, and independently
re-confirmed refinement mechanism for the Bulk/Tail Lemma's bulk and
small-`k` pieces, producing the largest single `n_0(γ)`-reduction this
sub-lineage has recorded (`3.46$–`29.76$` decades, arithmetic verified
exactly at all 8 rows, and independently re-bisected exactly at 3 of
them); and new — though, per the one real finding above, somewhat
over-characterized — supporting evidence for the standing `E_{\text{heuristic}}(γ)`
conjecture. The self-critical framing that item 2 is "the same kind of
contribution Estágio 49 said to move past" holds up under scrutiny as an
accurate, well-calibrated piece of self-assessment, not spin in either
direction.

**Verdict: SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**

---

## Files

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `adv01_moments_iid_route.py`/`.log` | independent re-derivation of `μ_3,μ_4` via the elementary i.i.d.-sum route (not cumulant recursion) |
| `adv02_Ex4_sympy_stats_route.py`/`.log` | independent re-derivation of `x(D)`'s coefficients via `sympy.diff`; `E[x(D)^4]` via `sympy.stats.Binomial`'s own moment engine, 24 points |
| `adv03_Ex4_freshpoints_crosscheck.py`/`.log` | `E[x(D)^4]` via direct `sympy.summation` + brute-force exact `Fraction` pmf, at 5 fresh `(k,n,γ)` points |
| `adv04_order6_taylor_recheck.py`/`.log` | independent re-derivation of the order-2/order-6 Taylor truncation and Richardson extrapolation at `γ=0.5` (exact match to target's log), plus the arithmetic check underlying Finding 1 |
| `adv05_n0_reassembly.py`/`.log` | full independent reassembly of the hybrid `n_0(γ)` construction, bisected fresh at `γ=0.5,0.9,0.01` |
| `adv06_lyapunov_bound_freshpoints.py`/`.log` | independent Lyapunov-bound validity check at 10 fresh `(k,n,γ)` points outside the target's own grid |

No Millennium Problem claims anywhere in the target or this report; pure
combinatorial/asymptotic mathematics internal to this archive. No file
outside this front's own `gamma_c_gamma_construction_attempt/adversarial/`
directory was created or modified by this review. No `git` command was
run by this referee beyond the read-only `git status` reported above.
