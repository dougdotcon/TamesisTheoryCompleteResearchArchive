# REFEREE REPORT — `MCLUST-H1-POST-CORRECTION-ATTEMPT`

**Target:** `.../mclust_h1_validity_attempt/h1_post_correction_attempt/ATTEMPT.md`
(wave 24, front (c), `DISC-DEC-114`). **Role:** hostile, adversarial referee
— the mandate was to try to break this document, not confirm it.

**Verdict: SOUND — ACCEPT for catalogue.**

No error was found that changes the validity of any headline claim. Three
LOW-severity issues are named below (a genuine internal counting slip in
the target's own Sec 5.3/Sec 10, and two instances of imprecise-but-harmless
prose characterization). No MODERATE or HIGH finding. Every substantive
mathematical claim this review re-derived independently — the elementary
two-case bound, the n_cross_rigorous formula, the translation-invariance
failure of `K(y,t)`, and the numerical reproduction — checked out exactly.
The Banach-space extension of the classical Volterra quasi-nilpotency
argument (the front's central new content, Sec 3) is correctly and
explicitly handled, not silently assumed from the scalar case.

---

## 0. Reading and provenance

Read in full, in prose, before any derivation or code, exactly per the
mandate: the target `ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md`'s full
`PLATRESUM` node history including the `DISC-DEC-113` addendum (the
correction this front builds on); `mclust_h1_validity_attempt/ATTEMPT.md`
(establishes `(U1)`/`(U2)`); `h1_energy_estimate_attempt/ATTEMPT.md`
(establishes `(E1)`, `(KEY)`, `(BB-Psi')`, the Lipschitz-`<=1` finding, all
post-`DISC-DEC-100`-correction); `h1_volterra_attempt/ATTEMPT.md` in full,
including its dated correction blockquotes (VERDICT UP FRONT, Sec 4.4, 4.6,
Sec 10) and its Sec 3/5/6 (confirmed correct by the prior referee,
unaffected by the correction); and `h1_volterra_attempt/adversarial/
REFEREE_REPORT.md` in full (the original derivation of the corrected bound).

**No `.py` file from any front or referee in this lineage was opened at any
point.** Every script below (`a01`–`a05`) was written fresh from the
mathematical content of the prose cited above, re-deriving every fact used
before relying on it, exactly as the target front itself claims to do for
its own inputs.

**Safety rule compliance (`PROOF_DEPENDENCY_MAP.md` Sec 3):** the target
document was checked line-by-line for any citation of Tree A (`u1/2`)
content; none found, anywhere, hedged or otherwise. This report likewise
cites nothing from Tree A.

**Seed range:** `grep -rn "20260928" 05_DISCOVERY_LAB/` was re-run by this
review before any use; the range `20260928000-20260928799` reserved for
this referee (and the target's own `20260928000-20260928999`) appear only
in the target's own `ATTEMPT.md`, `DECISION_LEDGER.yaml`'s `DISC-DEC-114`
line, and `DISCOVERY_LAB_STATE.md`'s summary — confirmed unused elsewhere.
**This review needed no randomness anywhere** — every check is exact
symbolic/high-precision arithmetic (`mpmath`) or deterministic grid
computation (`numpy`, float64, fixed grids, no sampling) — so the reserved
range remains entirely unused here too, exactly as the target itself
reports for its own reservation.

---

## 1. Claim 1 — the elementary two-case bound `h_eps(z) <= sqrt(pi/2)`

**Re-derived from scratch** (`a01_hepsbound_check.py`/`.log`). Findings:

- `R(0)=sqrt(pi/2)` confirmed two independent ways (erfcx closed form vs.
  raw Gaussian tail integral, `mpmath dps=50`) to 45+ digits; `R` confirmed
  strictly decreasing on `[0,50]`; `R(z)<=1/z` confirmed at 11 points from
  `z=0.01` to `z=10000`. All three facts the proof leans on are genuinely
  correct, not merely asserted.
- **The case split at `z0=1/eps` is exactly where `|1-eps*z|` changes
  sign** — trivial but confirmed: `1-eps*z=0 <=> z=1/eps`; positive below,
  negative above.
- **The boundary point `z=z0` has no gap or double-counting problem**:
  `h_eps(z0)=0` exactly (confirmed to `<1e-40`, `mpmath`), and both case
  bounds hold (trivially, with slack) exactly at the boundary — the proof's
  case split is a harmless closed/closed cover of `[0,inf)` meeting at one
  point, not an open gap.
- **The hypothesis `eps<=sqrt(pi/2)` is genuinely load-bearing, not
  decorative** — this review scanned `h_eps` over `eps` values both inside
  and outside `(0,sqrt(pi/2)]`. For every `eps<=sqrt(pi/2)` tested (`0.01`
  through `sqrt(pi/2)` itself, the boundary case), the global max is
  exactly `sqrt(pi/2)`, attained at `z=0`. For `eps>sqrt(pi/2)` (`1.5, 2, 5,
  10` — deliberately outside the archive's regime), the bound **fails**:
  `max h_eps` exceeds `sqrt(pi/2)` (e.g. `eps=1.5` gives `max h_eps~1.50` on
  the tested range, growing toward `eps` itself as `z->infinity`), because
  Case 2's final step `eps<=sqrt(pi/2)` is exactly where the slack runs out.
  This confirms the proof is tight to its stated hypothesis, not
  over-cautious.
- **Every archive-relevant `eps=1/sqrt(c)`, `c>=1`, satisfies `eps<1<sqrt(
  pi/2)=1.2533...` strictly** — the stated hypothesis range is safe with
  margin, not fragile at `c=1`.

**No gap found in Claim 1.** The proof is elementary, correct, and its case
split, boundary, and hypothesis range are all exactly as tight as claimed
and no tighter than needed.

---

## 2. Claim 2 — the convergence-upgrade theorem (central new content)

This is where the mandate asked for the most scrutiny. Findings, walked
through step by step:

### 2.1 Does the corrected constant bound + classical quasi-nilpotency
actually give rigorous convergence at every finite `y`?

**Yes.** The logical chain is sound: `DISC-DEC-113` (independently
re-derived by this front's own Sec 2, and independently re-verified again
by this review in Sec 1 above) establishes `||K(y,t)|| <= M :=
sqrt(pi/2)+eps` **uniformly over ALL `(x,y,t)` with `0<=t<=y`** — not merely
for `y` in some fixed `[0,Y]`, but for every `y>=0` with a single
`y`-independent constant. This is *stronger* than what the classical
theorem's hypothesis (`M` finite on the compact simplex `0<=t<=y<=Y`, for
each fixed `Y`) actually requires — so the hypothesis is satisfied
unconditionally, for every `Y`, with the same `M`. Given that, the standard
simplex-volume argument (`||K_n(y,t)||<=M^n(y-t)^{n-1}/(n-1)!`, giving
`||L^n||<=(MY)^n/n!->0`) is completely standard and was already correctly
stated by the immediate predecessor (`h1_volterra_attempt` Sec 3.4) — this
front's Sec 3.2 re-derives the same classical fact, not a new one, and
correctly says so ("classical fact ... re-derived from scratch"). What
*is* new is the tail-sum rate bound in Sec 3.3
(`||Phi^(n)-Phi||<=||g||*(MY)^n e^{MY}/n!`). This review independently
re-derived that inequality: writing `(n+1)(n+2)...(n+j) > j!` for `n>=1`
(each factor `n+i>i`), one gets `(MY)^{n+j}/(n+j)! <= (MY)^n/n! *
(MY)^j/j!`; summing over `j>=0` gives exactly the claimed bound. **Correct,
standard, and checks out.**

### 2.2 Is there an operator-valued (Banach-space) subtlety the front
silently glosses over?

**No — and this is explicitly, not silently, handled.** The target's Sec
3.2 states the space `Z_Y := C([0,Y];X)`, `X=C_b([0,infinity))`, and works
throughout with **operator norms** on `X`, not scalar magnitudes — matching
exactly how the classical fact was already correctly framed by the
predecessor (`h1_volterra_attempt` Sec 3.4, itself reviewed and found sound
by a prior referee, unaffected by the `DISC-DEC-113` correction). The
simplex-volume argument's only ingredient beyond finiteness of `M` is
submultiplicativity of operator norms (`||AB||<=||A||*||B||`), which holds
in *any* normed space, not merely finite-dimensional or Hilbert ones — so
no scalar-specific step is silently transplanted. This review additionally
checked, independently, that `K(y,t)` is actually a well-defined *bounded*
operator `X->X` (not merely norm-bounded on paper) — i.e. that
`M_y∘K_A^raw(y,t)` genuinely maps `C_b([0,infinity))` into itself, since
`M_y` alone does not (it is literally unbounded as a standalone operator on
`X`). Tracing the large-`x` behavior: `|(K_A^raw(y,t)f)(x)| ~ eps/(x+y)`
for large `x` (from `R(z)~1/z`), and `M_y`'s coefficient `~x/eps`, so the
product `~x/(x+y) -> 1` (a *finite*, nonzero limit) as `x->infinity` —
consistent with `h_eps(z)->eps` as `z->infinity`. **The composite operator
is genuinely, not just formally, bounded on `X`** — the correction is
mathematically real, not an artifact of dropping to a bound that happens to
be finite without the underlying operator actually mapping `X` into
itself. No gap found.

### 2.3 Is "locally uniform in `y` on every compact `[0,Y]`" an accurate,
non-overclaiming description of what was proved?

**Yes.** `Z_Y`-norm convergence is, by definition, `sup_{y in [0,Y]}
sup_{x>=0} |Phi^(n)(x,y)-Phi(x,y)| -> 0` — i.e. genuinely *uniform* (not
merely "locally uniform") in `y` on the compact `[0,Y]`, **and** uniform in
`x` over the *entire* unrestricted half-line simultaneously (a stronger
statement, in the `x`-direction, than `(U1)` even requires locally). The
document's own wording ("locally uniformly in `y` on `[0,Y]`") is correctly
hedged by "for every finite `Y`" — i.e. uniform on each compact interval,
not (and not claimed to be) uniform on `[0,infinity)` itself. This is
exactly right and matches standard usage.

### 2.4 Does the theorem overclaim progress toward `(U1)`/`(U2)`?

**No — checked explicitly and found accurate.** Sec 3.3's own "What this
theorem does NOT say" paragraph and Sec 6.1–6.2 correctly and precisely
identify that convergence *in the Picard order `n`, at each fixed `y`* is a
different axis from the *`y->infinity` behavior of the resummed limit*
that `(U1)`/`(U2)` actually need, and correctly note that for any FIXED
truncation order `n`, `(My)^n/n!` is an unbounded polynomial in `y` — so no
finite-order truncation gives a `y`-uniform error bound by this route. This
review found this diagnosis accurate and not overstated; it matches, and
does not exceed, what `h1_energy_estimate_attempt`'s own predecessor
diagnosis (Sec 6.2 of that document, cited correctly here) already
established for the closely related fixed-order-truncation obstruction.

### 2.5 Minor framing note (not a mathematical error)

The "genuinely new theorem, previously unreachable" framing partially
re-derives content (the classical quasi-nilpotency fact itself) already
stated, under the identical label, by the immediate predecessor — the
front is transparent about this ("classical fact ... re-derived from
scratch," matching this lineage's own convention of re-deriving cited
facts before use), so this is not a hidden gap, just a point where the
"genuinely new" framing applies more precisely to the Sec 3.3 rate bound
and the overall "upgrade to PROVED" bookkeeping than to the engine itself.
**Severity: LOW** (rhetorical emphasis only; every number and every logical
step is correct).

**Overall verdict on Claim 2: sound.** No gap, no silent scalar-to-Banach
transplant, no overclaim relative to `(U1)`/`(U2)`.

---

## 3. Claim 3 — the rigorous `n_cross(y)` bound

Re-derived from scratch (`a04_ncross_formula_and_translation_invariance.py`
/`.log`, Parts A–B):

- `n! >= (n/e)^n`: re-derived via `e^n = sum_k n^k/k! >= n^n/n!` (single
  positive term), confirmed numerically `n=1..500` (`mpmath`, exact
  factorials). **Correct.**
- `n_cross_rigorous(y) := ceil(M*e*y)+1`: re-derived from `(My)^n/n! <=
  (My*e/n)^n < 1 <=> n > M*y*e`. **The algebra works out to exactly the
  claimed formula.**
- **This review reproduced the target's own Sec 4.3 table exactly, 14/14
  points, independently computed from the formula** (both `c=100` and
  `c=1000`, `y=0.5` through `6.0`).
- The claimed post-crossing strict-decrease property (`term(n+1)/term(n) =
  My/(n+1)`, itself decreasing) was independently re-verified numerically
  at two `(y,M)` pairs — confirmed strictly decreasing for 6 further terms
  past the crossing point in both cases.
- **Dominance check, independently, at a FINER grid than the target's own**
  (`y=0.5` to `6.0`, step `0.5`, 12 points × 2 values of `c` = **24 fresh
  points**, via this review's own from-scratch grid Neumann solver, Sec 4
  below): the rigorous bound dominates the measured `n_cross(y)` at
  **every single one of the 24 points**, both `c` values — see
  `a03_ratio_and_ncross.py`/`.log`, Part B.
- Minor prose-precision note (Sec 5 below, finding L2): the target's
  characterization "rigorous slope `~3.4-3.5`... roughly `5-7x`" the
  empirical slope is slightly imprecise for `c=100` specifically (this
  review's least-squares fit of the front's own table gives `~3.77`, not
  `~3.4-3.5`, and the ratio spread is closer to `~4.6x`–`7.7x`). This does
  not affect any tabulated value or the domination check itself, which was
  independently re-verified point-by-point above. **LOW severity.**

**Overall verdict on Claim 3: sound**, with one LOW-severity descriptive
imprecision noted.

---

## 4. Claim 4 — `K(y,t)` is not translation-invariant in `(y,t)`

Verified by direct, independent computation, not by restating the target's
own structural argument (`a04...py` Part C). Deriving the action of
`M_y∘K_A^raw(y,t)` on the test function `f(x)=1` from scratch:

```
(M_y K_A^raw(y,t)[1])(x) = (1-eps(x+y)) * R(x+y) * (1-e^{-(y-t)/eps})
```

This factors as `[function of (x,y) only] * [function of h:=y-t only]`. The
second factor is genuinely translation-invariant (`h`-only); the **first
factor depends on `y` directly** (through `x+y`), not merely on `h`. At
fixed `x=0`, `h=y-t=1.0` fixed, this review evaluated the operator's action
at `y=1,2,5,10,50` and found the value changes substantially and
non-monotonically (`0.590 -> 0.337 -> 0.096 -> 0.000 -> -0.080`) — direct,
concrete confirmation that `K(y,t)` genuinely depends on `y` and `t`
separately, not merely on `y-t`.

This review also checked whether an "obvious" reparametrization could
restore translation invariance (mandate's own request) — e.g. absorbing the
`y`-dependence via the `x+y`-conservation structural fact already
established elsewhere in the lineage. It cannot: `x` is an independently-
varying Banach-space index (the function-space coordinate), not free to
co-vary with `y` while `y` plays the role of Volterra "time" — fixing `x`
and varying `y` necessarily moves `x+y`, so no change of variables at fixed
`x` removes the dependence. **The target's Claim 4 is correct, and this
review found no missed reformulation that would resolve it.**

---

## 5. Claim 5 — numerical reproduction

A **third**, independent, from-scratch, interpolation-free grid
Neumann/Picard solver was built (`a02_grid_neumann_solver.py`), coded
directly from the prose equations `(I)`, `(BB-Psi')`, `(NEW-W)`, `(E2)` in
the required reading — no `.py` file from any front or the earlier referee
was read. Results:

- **The solver's raw Picard iterates at `(x=0,y=0.2/0.5/1.0)`, `c=100`,
  `h=0.1` reproduce `h1_volterra_attempt`'s own published Sec 5.3 table
  digit-for-digit** (`0.1353, 0.2184, 0.2224, 0.2225, 0.2225` etc.) — a
  strong sanity check that this review's independent implementation of the
  closed system is correct before trusting anything downstream.
- **Successive-difference ratio spot-check** (`a03...py` Part A) at
  `c=100, y=0.5/1.0/2.0` and `c=1000, y=1.0` (4 points, exceeding the
  mandate's "2-3" minimum): matches the predecessor's published Sec
  6.2/6.3 values to 3-4 significant digits at every point — e.g.
  `c=100,y=1.0`: this review `[0.5516, 0.1970, 0.1052, 0.0678, 0.0490]` vs.
  published `[0.552, 0.197, 0.105, 0.068, 0.049]`.
- **`n_cross(y)` fine-grid reproduction** (`a03...py` Part B/C): this
  review's independently-measured sequences match the target's own Sec 5.4
  sequences **exactly**: `c=100: [2,3,3,3,4,4,4,4,4,5,5,5]`, `c=1000:
  [3,3,4,4,5,5,6,6,6,6,7,7]` (both `y=0.5..6.0`, step `0.5`) — and the
  resulting least-squares slope/intercept fits match the target's reported
  `0.4895*y+2.2424` (`c=100`) and `0.7552*y+2.7121` (`c=1000`) to 4 decimal
  places.

**Overall verdict on Claim 5: sound, strongly reproduced.**

---

## 6. Claim 6 — overclaiming / honesty check, and one genuine finding

### Finding L1 (LOW) — internal counting inconsistency in Sec 5.3/Sec 10

The target's own Sec 5.3 text states: *"5 of 7 points at c=100 and 6 of 7
points at c=1000 match EXACTLY; **two** points differ by 1"* — but "5 of 7"
+ "6 of 7" arithmetically implies **3** differing points (2 at `c=100`, 1
at `c=1000`), not the "two points" the very next sentence states, and only
**two** rows are shown in the table that follows (`c=100,y=1.0` and
`c=1000,y=0.5`). The Sec 10 scorecard repeats the inconsistent tally:
*"11/14 points exact, 3/14 off by 1."*

This review recomputed the correct count **three independent ways**: (a)
extracting the integer-`y` values directly from the target's own Sec 5.4
finer-grid data (`c=100: [2,3,3,3,4,4,4,4,4,5,5,5]` at `y=0.5..6.0` step
`0.5` gives, at `y=0.5,1,2,3,4,5,6`: `[2,3,3,4,4,5,5]`, differing from the
predecessor's published `[2,2,3,4,4,5,5]` at **exactly one** point,
`y=1.0`; similarly for `c=1000`, exactly one point, `y=0.5`); (b) this
review's own fresh grid solver (`a03...py` Part C), computed independently
of the target's numbers, gives the **identical** result — `6/7` exact at
`c=100` (only `y=1.0` differs), `6/7` exact at `c=1000` (only `y=0.5`
differs); (c) both agree with the two rows the target's own table
*already shows*. **The correct tally is 12/14 exact, 2/14 off by 1 — not
11/14 and 3/14.**

This is a pure counting/arithmetic slip in the target's own prose and
scorecard (the "5 of 7" fraction for `c=100` should read "6 of 7"), not an
error in the underlying computation or in the substantive finding itself:
the front's identification of a genuine labeling slip in the
*predecessor's* Sec 6.4 footnote table (the `(already <0.5 at n=2)`
annotations at `c=100,y=1.0` and `c=1000,y=0.5` should read `n=3`, since
the predecessor's own Sec 6.2 first ratio value at those points, `0.552`
and `1.112` respectively, is not itself `<0.5`) **is correct and is
independently reconfirmed by this review's own from-scratch solver**, which
lands on `n_cross=3` at both points, matching the target's own corrected
values, not the predecessor's stale footnote. **Severity: LOW** — affects
only a tally description in the target's own prose/scorecard, changes no
individual number, and does not touch the correctness of the substantive
labeling-slip finding it accompanies.

### Finding L2 (LOW) — see Sec 3 above (slope characterization imprecision).

### Finding L3 (LOW) — see Sec 2.5 above (rhetorical framing of "genuinely
new" for the classical-theorem restatement).

### General overclaiming check

Every PROVED/CONFIRMED/OPEN label in the target's Sec 10 scorecard was
checked against what Sec 2–6 actually demonstrate. All are accurate:
`(U1)`, `(U2)`, `H1` are correctly kept OPEN; the "PROVED, for every finite
`y`" label for the convergence theorem is earned (Sec 2 above); the
"CONFIRMED numerically"/"MEASURED numerically" labels for the empirical
`n_cross(y)` content are not inflated to "PROVED"; the explicit "What this
theorem does NOT say" paragraph (Sec 3.3) and Sec 6.1–6.2's diagnosis
correctly scope "converges at every finite `y`" as a *different, weaker*
statement than the `y->infinity` uniformity `(U1)`/`(U2)` require, and this
review found no place where the document blurs that distinction elsewhere.
No claim of progress on `(U1)`/`(U2)` beyond what is proved was found
anywhere in the document.

---

## 7. Files in this review

| file | role |
|---|---|
| `a01_hepsbound_check.py`/`.log` | Independent re-derivation and stress-test of the elementary two-case `h_eps(z)<=sqrt(pi/2)` bound: `R` facts, case-split correctness, boundary check, `eps` hypothesis necessity, high-precision sup confirmation (Sec 1 above) |
| `a02_grid_neumann_solver.py`/`.log` | Third independent, from-scratch, interpolation-free grid Neumann/Picard solver, built only from the prose equations `(I)`,`(BB-Psi')`,`(NEW-W)`,`(E2)`; reproduces `h1_volterra_attempt`'s own Sec 5.3 table digit-for-digit as a sanity check |
| `a03_ratio_and_ncross.py`/`.log` | Uses `a02`'s solver to reproduce Sec 6.2/6.3 ratio tables (Part A), measure `n_cross(y)` on a fine grid and check rigorous-bound domination at 24 points (Part B), and cross-check against the predecessor's/target's published integer-`y` `n_cross` tables (Part C, Finding L1) |
| `a04_ncross_formula_and_translation_invariance.py`/`.log` | Re-derivation of `n!>=(n/e)^n` and `n_cross_rigorous(y)`, exact reproduction of the target's Sec 4.3 table (Part A/B); direct computational test of `K(y,t)`'s translation-invariance failure (Part C) |
| `a05_sec25_table_and_slope_precision_checks.py`/`.log` | Spot-check of the (non-load-bearing) Sec 2.5 illustrative table; precision check of the Sec 4.3 slope/ratio prose characterization (Finding L2) |
| `REFEREE_REPORT.md` | this document |

No `.py` file from any front or referee in this lineage was read at any
point. No `git` command of any kind run. No file outside this
`h1_post_correction_attempt/adversarial/` directory was written to.

---

## 8. Final verdict

**SOUND — ACCEPT for catalogue.**

The target's headline claims all check out under independent re-derivation:
the elementary two-case bound proof (Claim 1) is correct with no gap at the
case boundary and a genuinely load-bearing, archive-safe hypothesis range;
the convergence-upgrade theorem (Claim 2) correctly and explicitly extends
the classical Volterra quasi-nilpotency argument to the Banach-space-valued
setting, with no silent scalar-case transplant, and does not overclaim
progress toward `(U1)`/`(U2)`; the rigorous `n_cross_rigorous(y)` bound
(Claim 3) is correctly derived and was found to dominate the true measured
value at every one of 24 independently-computed points, on a grid finer
than the target's own; the translation-invariance failure of `K(y,t)`
(Claim 4) is genuine, confirmed by direct computation, and not resolvable
by an obvious missed reparametrization; and the numerical reproduction
(Claim 5) was independently confirmed by a third, freshly-built solver.

Three LOW-severity issues are named (Sec 6, Findings L1–L3): a genuine
internal counting inconsistency between the target's own Sec 5.3 prose
("5 of 7... two points differ") and Sec 10 scorecard ("11/14... 3/14") —
the correct, independently-triple-confirmed tally is 12/14 exact, 2/14 off
by one, at exactly the two points the target's own table already shows;
and two instances of mildly imprecise (not incorrect) prose
characterization of slope/ratio magnitudes and of the "genuinely new"
framing for content that partially restates an already-established
classical fact. None of the three affects any tabulated value, any proof
step, or the document's own honest "`H1` remains OPEN" bottom line.

`H1`, `(U1)`, `(U2)` remain correctly labeled OPEN throughout. No claim of
progress on any Millennium Prize Problem appears anywhere in the target
document or in this review. No result from the archive's separate Tree A
(`u1/2`) line was cited anywhere in the target document or in this review,
per `PROOF_DEPENDENCY_MAP.md` Sec 3.
