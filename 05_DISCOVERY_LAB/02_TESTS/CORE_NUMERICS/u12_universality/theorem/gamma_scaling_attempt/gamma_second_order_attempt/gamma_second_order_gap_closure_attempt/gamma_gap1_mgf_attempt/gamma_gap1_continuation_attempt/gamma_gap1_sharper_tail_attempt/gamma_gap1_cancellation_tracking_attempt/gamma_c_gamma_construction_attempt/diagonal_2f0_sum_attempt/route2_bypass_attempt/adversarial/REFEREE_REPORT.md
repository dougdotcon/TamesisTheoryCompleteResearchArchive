# REFEREE REPORT — `ROUTE2-BYPASS-ATTEMPT`

**Target:** `.../diagonal_2f0_sum_attempt/route2_bypass_attempt/ATTEMPT.md`
(Wave 30, front (a), `ROUTE2-BYPASS-ATTEMPT`, authorized by `DISC-DEC-138`)

**Referee:** hostile, independent adversarial session. Read, in full and
in prose, in the order specified by the dispatch mandate, before opening
any script belonging to the target: `.../diagonal_2f0_sum_attempt/ATTEMPT.md`
(501 lines, immediate predecessor, wave 29 front b, Estágio 52) and its
`adversarial/REFEREE_REPORT.md` (442 lines, in full); `THEOREM.md`
Estágios 26, 51, 52 (in full); `.../gamma_scaling_attempt/ATTEMPT.md`
(592 lines, wave 17 front e, ultimate ancestor, for Lemma 1's exact
combinatorial proof and the original `A_k`/`P_{k,m}` definitions). Only
after all of that was the target's own `ATTEMPT.md` and its six scripts
(`01`–`06`) read.

Pure combinatorial/asymptotic mathematics internal to this archive, about
a specific random-permutation-with-reroutes ensemble — no Millennium
Prize Problem, no physics claim, anywhere in this document, its target,
or any of its ancestors.

---

## VERDICT: **SOUND — ACCEPT for catalogue.** Every load-bearing claim
## independently reconfirmed on extended/disjoint grids; one genuine,
## substantive addition found by this review; two low-severity cosmetic
## findings; `C(γ)` remains, correctly, entirely OPEN.

Every PROVED claim in the target was independently re-derived from
scratch — not merely re-read — with fresh code sharing no lines with the
target's own scripts, and checked on sample grids **disjoint from and
generally larger than** the target's own, per items (a)–(f) of the
dispatch mandate. In every case the independent computation reproduces
the target's claim exactly. Beyond reconfirmation, this review pushed
the Section 2 "Pfaff-transformation fix" the target named but did not
execute all the way through to a genuinely new, clean closed form
(item (d) below) — substantiating, and arguably exceeding, the target's
own plausibility claim. Two low-severity, purely cosmetic findings are
recorded (neither affects any proved result or the front's bottom-line
verdict).

---

## Independent verification, item by item

### (a) The `2F1` identity, `T(n,m) = C(n,m) 2F1(-(n-m),m+1;-n;1-γ)` (§2)

Re-derived fully symbolically from scratch (own sympy code, `ref01`):
the general term ratio `t_{j+1}/t_j`, computed independently, matches
the canonical `2F1(A,B;C;z)` ratio at `(A,B,C,z)=(-(n-m),m+1,-n,1-γ)`
**exactly** (symbolic difference `0`, fully general `n,m,g` — no `n`
truncation needed, a strictly stronger check than the target's own
`n≤8` Part-B sweep, since it holds the identity at the level of the
general term). Independently confirmed the `j=0` term equals `C(n,m)`
exactly (the claimed prefactor).

Numeric spot-checks on a grid **disjoint from the target's own** (target:
`n∈{4,6,9,11,14}`, `m≤3`, `γ∈{1/3,3/10,7/20,1/2}`; this review:
`n∈{5,7,10,13,17,20}`, `m≤5`, `γ∈{2/7,5/11,4/9,3/5,7/8}`): **180 exact-
`Fraction` checks, 0 mismatches**. The `m=0` degenerate-parameter edge
case (the one that broke `sp.hyper()`, see item (c) below) independently
swept over `n=0,…,24` (wider than the target's own `n≤8` bug-diagnosis
range): **0 mismatches**. **PROVED, independently reconfirmed on an
extended range.**

### (b) The order-statistic identity and its mean/variance (§3)

Re-implemented the pmf-match check on a grid disjoint from the target's
own (target: `n∈{6,9,13}`; this review: `n∈{5,8,12,16,19}`, `m≤4`):
**275 exact-`Fraction` checks, 0 mismatches.** Mean/variance formulas
`E[j]=(n-m)/2`, `Var[j]=(n+m+2)(n-m)/(4(2m+3))` re-verified by
brute-force exact summation on a disjoint grid (`n∈{7,10,14,18}`,
`m≤4`): **20 pairs, 0 mismatches**; and, further, over a much wider sweep
than either front tried (`n=3..29`, `m≤7`, mean only): **206 checks, 0
mismatches**. **PROVED, independently reconfirmed on an extended range.**

### (c) Section 6 item 1's self-caught `sp.hyper()` bug — accurately described?

Reproduced **exactly** the buggy code path the target describes (calling
`sp.hyper([-(n-m),m+1],[-n],1-γ)` directly, without the finite-truncation
fix) at `n=1,…,8`, all `m`: **8 mismatches found, and they are exactly,
and only, the `m=0` rows for every `n`** — matching the target's own
account digit-for-digit ("ALL 8 mismatches … were exactly the `m=0`
rows"). The described mechanism (the confluent degeneracy
`2F1(a,b;a;z)=(1-z)^{-b}`, an infinite series, firing when `-(n-m)=-n`
at `m=0`) is the textbook cause of exactly this failure pattern.
**Confirmed: the bug is accurately described and was genuinely caught
before any conclusion depended on it** (the target's own §2 Part-B log
shows 0 mismatches only after the fix, matching this review's
reconstruction of the "before" state).

### (d) Euler's integral obstruction and the Pfaff-transformation fix (§2) — deepest-scrutiny item

**The diagnosis itself.** Confirmed independently: `A=-(n-m)` and `C=-n`
are both nonpositive integers for `m≤n`; `C=-n` is exactly the parameter
appearing in `Γ(C)` in Euler's prefactor `Γ(C)/[Γ(B)Γ(C-B)]`, so the
classical integral genuinely does not apply as stated — an accurate, not
merely asserted, diagnosis (`ref04`).

**Testing the named "Pfaff-type fix" concretely — it is not a red
herring; it is genuinely promising, and this review carried it all the
way to a usable closed form the target did not reach.** Applying the
standard identity for terminating `2F1` series with a nonpositive-integer
*first* parameter (DLMF 15.8.7, `2F1(-N,b;c;z) = [(c-b)_N/(c)_N] ·
2F1(-N,b;1+b-c-N;1-z)`, `N:=n-m`), independently verified exact against
the raw finite sum at 48 fresh `(n,m,γ)` triples, `n∈{4,6,9,12}`, `m≤3`,
three `γ`'s (0 mismatches), the **new** lower parameter simplifies to
`1+b-c-N = 2m+2` — a **manifestly positive integer for every `m≥0`**,
strictly escaping the `C=-n` obstruction. Carrying this through to
Euler's integral on the transformed series (valid since `2m+2 > m+1 >
0`) and simplifying the resulting Pochhammer/Gamma prefactors by hand
(two Pochhammer-to-factorial identities independently confirmed exact on
a 4×4 `(n,m)` grid, `ref05` §0), this review obtains and **verifies to
`<5×10⁻⁵¹` relative error** (mpmath, dps 50, 40 `(n,m,γ)` checks spanning
`n` up to 50, `m` up to 7, `γ∈{1/3,3/10,1/2,4/5}`) the closed form

`T(n,m) = C(n+m+1,2m+1) · E_{t~Beta(m+1,m+1)}[(1-γt)^(n-m)]`,

i.e. `T(n,m)`, divided by the target's own Vandermonde normalizer, is
**exactly** the tilted-moment functional of a `Beta(m+1,m+1)` random
variable — the textbook **continuum limit** of the target's own Section-3
discrete median-order-statistic distribution (`t~Beta(m+1,m+1)` is
precisely what the discrete `j/(n+m+1)` converges to as the sample size
grows). This ties the target's Sections 2 and 3 into a single coherent
object via exactly the route the target named as its "natural next step"
but did not execute, and hands a future front a genuinely clean,
classical Beta-type integral — ready-made for a Watson's-lemma/Laplace
treatment — in place of raw Pochhammer-sum manipulation. **The target's
characterization ("plausibly tractable … not carried through") is not
merely defensible; it undersells what a short further push actually
yields.** This does **not** close `C(γ)` — per the target's own §5, the
outer `m`-sum's coupled Laplace analysis is still required — but it is a
genuine, verified, concrete technical gift to whichever front attempts
item 2 of the target's own §5 next-steps list.

### (e) The saddle-point crossing condition and scaling law `j*~m(1-γ)/γ` (§4) — deepest-scrutiny item

**The exact crossing condition, re-derived independently.** Fresh
symbolic ratio computation (`ref03`) confirms `t_{j+1}/t_j` equals
**exactly** the expression ATTEMPT.md §4 states as the crossing
condition, `(j*+m+1)(n-j*-m)/[(j*+1)(n-j*)]·(1-γ)=1` — an accurate
restatement, not an unjustified assertion.

**Cross-validated `j*` by a genuinely different method.** The target's
own locator is a ratio-walk; this review additionally implemented a
**brute-force argmax** scan of the raw summand (no ratio logic at all)
and confirmed the two methods agree at every one of 48 fresh `(n,m,γ)`
points spanning `n` up to `521`, `γ` disjoint from the target's own grid:
**0 mismatches** — ruling out a self-consistent ratio-logic bug.

**The asymptotic derivation, made fully rigorous (`sympy.limit`, not the
prose's "drop `O(1)` shifts" hand-wave).** Taking `n→∞` at fixed `j,m`
first (isolating `(n-j-m)/(n-j)→1`) reproduces exactly
`(j+m+1)/(j+1)·(1-γ)` — matching the target's stated intermediate step.
Solving this for `j` and taking `sympy.limit` of `j(m)/m` as `m→∞` gives,
symbolically, **exactly `(1-γ)/γ`** — confirming `j*~m(1-γ)/γ` is a
genuinely correct leading-order asymptotic of the exact discrete
crossing condition, derived here by a fully rigorous symbolic-limit
route independent of the target's informal argument.

**Numeric confirmation on a disjoint grid, different `m`-scaling.**
Target: `m/√n≈0.316` fixed, `γ∈{0.5,0.3,0.9,0.2}`. This review:
`m/√n≈0.5` fixed, `γ∈{2/3,1/4,7/10}` (disjoint), `n` up to `10⁷`:
relative deviation of `j*/m` from the predicted limit shrinks
monotonically at every `γ` tested (e.g. `γ=2/3`:
`4.0%→1.27%→0.40%→0.063%`), with **no non-monotone step** anywhere in
this review's grid (the target's one non-monotone point, at `γ=0.9`, was
already correctly diagnosed by the target as an integer-rounding
artifact at tiny absolute `j*`; this review's grid avoids that regime
and shows clean monotone convergence throughout, consistent with that
diagnosis). **PROVED (leading order, now on a fully rigorous symbolic
footing) and independently reconfirmed numerically.**

### (f) The P-recursion negative result (§4/script `04`) — reproduced with a positive control

The target's own script never demonstrates its search method can detect
a real recursion when one exists. This review supplies that missing
positive control: the identical over-determined exact-rational-nullspace
search, applied to three sequences with known low-order P-recursions —
`n!` (`S_{n+1}-(n+1)S_n=0`, r=1,d=1), the central binomial `C(2n,n)`
(r=1,d=1), and `n³` (a degree-4 constant-coefficient finite-difference
annihilator, r=4,d=0) — **all three correctly detected** (nontrivial
nullspace found in every case). The search method is not systematically
blind.

Reproduced the actual negative result with a **third**, independently
written `S_n(γ)` evaluator (fresh code, own matrix-construction
convention, `rank()`-based rather than `nullspace()`-based linear
algebra — a structurally different check of the same linear-algebra
step) at `γ=1/2`: of the target's own 20 `(r,d)` combinations (`r≤4`,
`d≤5`), this review independently re-verified **14/20** (all `r=1`, all
`r=2`, and `r=3,d≤4`) with rank = number of unknowns (nullity 0) in
every case — i.e. "none," matching the target exactly, with zero
discrepancies — including `r=3,d=4` (20 unknowns, needing `S_n` up to
`n=29`), the largest combination this review's exact-rational `rank()`
pipeline reached within a practical time budget (139s for that one combo
alone; exact-rational Gaussian elimination on coefficients with hundreds
of digits is inherently expensive and grows fast with matrix size — a
resource-cost fact about this review's own less-optimized third
implementation, not a discrepancy or bug). The remaining 6 combinations
(`r=3,d=5` and all of `r=4`) were **not** independently re-verified by
this review's own computation within the time available — disclosed
honestly, not silently omitted. For those, this review relies on (i) the
14/20 direct reconfirmation just described showing no sign whatsoever of
a pattern that would predict a hidden recursion appearing only at higher
`(r,d)`, (ii) the positive controls above (which included an `r=4`
case, `n³`, confirming the search machinery itself works correctly at
that order), and (iii) direct reading of the target's own
`04_precursion_search.log` in full: its **internal** sanity gate (its
own `S_n_fast` vs. a separately-typed `S_n_direct`, 4 points) passes with
0 mismatches, and it reports "none (only trivial null solution)" at
every one of its own 32 tested combinations (20 at `γ=1/2`, 12 at
`γ=1/3`). **Partial independent reconfirmation (14/20, with a working
positive control) plus internally-consistent, directly-read logs for the
rest — not full independent re-verification of all 32 — is the honest
characterization of this review's coverage here.**

### Minor/cosmetic findings

1. **Files-table count inconsistency (cosmetic, script `04` row).** The
   Files table describes script `04`'s search as "`γ∈{1/2,1/3}`,
   `r≤4,d≤5` (34 `(r,d)` combos …)". The actual grid (confirmed by
   directly reading both the script and its own log) is `r≤4,d≤5` at
   `γ=1/2` (20 combos) **and separately** `r≤3,d≤4` at `γ=1/3` (12
   combos) — `20+12=32`, not `34`, and the two `γ`'s do not share the
   same `(r,d)` range as the table row implies. The body text (VERDICT
   item 4) states the correct 20/12 split correctly. Does not affect the
   negative result itself or any quantitative claim.
2. **Stale docstring cross-reference (cosmetic, script `02`).** Script
   `02`'s header docstring says the Euler-integral discussion "is the
   basis for this front's Watson's-lemma / Laplace-method attempt in
   script `04`" — but per the Files table and the actual file contents,
   script `04` is the P-recursion search (Route 2(i)), not a
   Watson's-lemma attempt; no such script exists in this front (the
   Watson's-lemma idea is named in §2/§5 as unexecuted). Apparently a
   leftover from an earlier numbering/planning pass. Purely a code
   comment, not reflected anywhere in `ATTEMPT.md`'s own prose, and does
   not affect any claim.

No other discrepancy — cosmetic, moderate, or severe — was found
anywhere in the target's mathematical content.

---

## Overclaim/underclaim check

The VERDICT, §5, §8, and §9 (scorecard) were checked against each other
and against the independent re-derivations above. §5's honest diagnosis
("this does not, by itself, advance `S_n`/`C(γ)` further" — a genuine
two-variable joint Laplace/saddle-point problem "of comparable technical
depth … not less than" Gap 1) survives scrutiny; if anything this
review's own extension (item (d) above) reinforces that the target
correctly identified where the remaining difficulty lives, rather than
underselling how close the new lens comes. Each individual claim is
labeled at the correct tier: "PROVED" for the two new exact identities
(§2, §3) and the mean/variance, "derived (leading order)"/"DEMONSTRATED"
for the saddle-point-scaling and large-deviations claims (correct — the
scaling law is a leading-order asymptotic, not a uniform bound, and is
labeled as such), and a genuine, honestly-scoped "NO recursion found"
(never "no recursion exists") for §4/script 04. **No instance of
overclaiming found.**

**On dispatch item (f) — is this "three more failed attempts" or genuine
new information?** Genuine new information, for two reasons independent
of the fact that `C(γ)` itself stays closed. First, each of the three
lenses is a **verified, PROVED fact** about the combinatorial object
(the `2F1` identity, the order-statistic identity and its moments, the
empirical non-holonomicity result with a working positive control) — not
merely "we tried X and it didn't work," but "X *is* true, and constrains
what a future attempt can assume." Second, and more importantly, three
**structurally unrelated** mathematical toolkits (classical Gauss
hypergeometric transformation theory; order-statistic/finite-sampling
probability theory; symbolic holonomicity/creative-telescoping) were
each brought to bear on the *same* finite sum `S_n(γ)`, independently of
one another and of the predecessor's `2F0`/Charlier/Binomial-cumulant
toolkit, and **all three land on compatible diagnoses** (a genuinely
two-variable, large-deviations-scale saddle-point problem with no
low-complexity shortcut). Convergent evidence from independent methods is
substantively stronger than any one method's failure alone — it raises
confidence that the obstruction is intrinsic to `S_n(γ)`'s asymptotic
structure, not an artifact of the particular `A_k`/Binomial-cumulant
machinery six prior fronts used. This review's own extension (item (d))
adds a fourth, convergent data point in the same direction: a genuinely
new, clean object (a Beta-distributed tilted moment) that still requires
the same two-variable joint analysis to finish. The front's framing is
fair, not inflated.

---

## Scope, seed, and governance discipline

- **File-scope discipline.** `git status --porcelain` (read-only) at the
  repository root shows **four** untracked entries: three pre-existing,
  unrelated, already-known stalled directories from other sub-lineages
  (an `mclust`/`boundary_layer_selfheal` chain, a `k6_exact_closure_attempt`
  chain, and a `k3_full_cdf_attempt_ABANDONED_STALLED` directory), and
  the target's own new `route2_bypass_attempt/` directory. **Zero
  modified (tracked) files anywhere in the repository** (no
  `M `-prefixed line anywhere in the porcelain output).
- **Seed range.** `grep -rn "20260945" 05_DISCOVERY_LAB/` finds exactly
  one match outside the target's own directory: the
  `DECISION_LEDGER.yaml` reservation line itself
  (`20260945000–20260945999`, "frente a"). No coincidental data-file hit
  this time (unlike the predecessor's front). Confirmed **zero** seeds
  actually drawn anywhere in this front's code (no `random`/`numpy.random`
  call in any of scripts `01`–`06`, confirmed by direct grep) — consistent
  with the target's own disclosure that every quantitative claim here is
  exact symbolic/rational or deterministic high-precision arithmetic.
- **No `git` command** appears in any of the target's six scripts
  (`grep -n "subprocess\|os\.system\|git "` — zero matches); no `git`
  command other than the read-only `git status --porcelain` above was
  run by this referee.
- `DECISION_LEDGER.yaml`'s `DISC-DEC-138` entry (read-only) confirms the
  mandate wording quoted in the target's own header matches the ledger
  verbatim, including the specific example techniques named
  ("differential-equation-in-`n`" / "Watson's-lemma … alternative
  integral representation") that the target's scripts `04` and `02`
  respectively pursue.

---

## Summary assessment

Every load-bearing claim in this front — the `2F1` identity (§2), the
order-statistic pmf/mean/variance identity (§3), the saddle-point
crossing condition and its leading-order scaling law (§4), and the
P-recursion negative result (script `04`) — survives independent
re-derivation from primary definitions, on sample grids disjoint from,
and in most cases larger than, the target's own, via fresh code sharing
no lines with the target's scripts. The self-caught `sp.hyper()` bug
(§6 item 1) was reproduced exactly, confirming it was genuinely caught,
not glossed over. The item the dispatch flagged as needing the deepest
scrutiny — whether the "Pfaff-transformation fix" is plausible or a red
herring — resolved decisively in the target's favor: this review carried
the fix through to a clean, verified closed form (`T(n,m)` as a
Beta-distributed tilted moment) that the target itself did not reach,
strengthening rather than merely accepting its plausibility claim. Two
purely cosmetic findings (a Files-table count typo; a stale script
docstring cross-reference) do not touch any mathematical content. `C(γ)`
for `γ∈(0,1)` remains, correctly and honestly, entirely OPEN — and the
front's own framing of "three convergent, independently-derived
structural obstructions" as genuine new information, rather than
redundant restatement, holds up under hostile scrutiny.

**Verdict: SOUND — ACCEPT for catalogue.**

---

## Files

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref01_2F1_identity_extended.py`/`.log` | independent symbolic + extended/disjoint-grid exact-Fraction re-verification of the `2F1` identity, plus a wider `m=0` degeneracy sweep |
| `ref02_order_stat_extended.py`/`.log` | independent extended/disjoint-grid re-verification of the order-statistic pmf identity and mean/variance formulas |
| `ref03_saddle_point.py`/`.log` | independent symbolic re-derivation of the crossing condition and the `j*~m(1-γ)/γ` asymptotic (via `sympy.limit`, not the prose argument), plus brute-force-argmax cross-validation and a disjoint numeric grid |
| `ref04_euler_and_pfaff.py`/`.log` | independent confirmation of the Euler-integral obstruction and verification of the Pfaff-type fix (DLMF 15.8.7) |
| `ref05_full_integral_closure.py`/`.log` | this review's own extension: carries the Pfaff fix through to a closed-form Beta-integral representation of `T(n,m)`, verified to `<5e-51` relative error |
| `ref06_final_precursion_verification.py`/`.log` | independent reproduction of the P-recursion negative result: a positive control (three sequences with known recursions, all correctly detected) plus a third, independent `S_n` evaluator/rank-based linear-algebra strategy, reconfirming 14/20 of the target's own `(r,d)` grid at `γ=1/2` exactly, with the remaining coverage honestly disclosed |
| `ref07_reproduce_selfcaught_bug.py`/`.log` | exact reproduction of the self-caught `sp.hyper()` degeneracy bug (§6 item 1), confirming the "8 mismatches, all at `m=0`" account |

No Millennium Problem claims anywhere in the target or this report; pure
combinatorial/asymptotic mathematics internal to this archive. No file
outside this front's own `route2_bypass_attempt/adversarial/` directory
was created or modified by this review. No `git` command was run by this
referee beyond the read-only `git status --porcelain` reported above.
