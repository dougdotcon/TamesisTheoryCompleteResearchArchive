# REFEREE REPORT — `GAMMA-CROSSOVER-MATCHED-ASYMPTOTICS-ATTEMPT` (wave 34, `DISC-DEC-151`)

**Scope of this review.** Hostile, adversarial review of
`gamma_crossover_matched_asymptotics_attempt/ATTEMPT.md` (695 lines) and
its scripts `01`–`05`, per the dispatching mandate. Every central claim
was independently re-derived from scratch — fresh symbolic derivations,
fresh numerical evaluators (different implementations from the front's
own), and a fresh from-primary-definitions check of the one cited
identity (`S_n'=1+S_n`) the front's central §6 argument leans on hardest
— not merely re-run or eyeballed. Scripts and logs are in this
directory (`01`–`04`, `.py`/`.log`).

---

## VERDICT: **SOUND WITH ISSUES, both LOW severity — ACCEPT for catalogue**

After genuine, sustained adversarial effort — independently re-deriving
the central Watson's-lemma closed form via a structurally different
symbolic route, independently confirming it against two numerical
evaluators neither copied from the front (an *exact* terminating-2F1
evaluator with zero quadrature error, and a differently-structured plain
quadrature), independently re-deriving both §4 matching claims via a
different bivariate-expansion technique, independently re-verifying the
critical cited identity `S_n'(γ)=1+S_n(γ)` from PRIMARY combinatorial
definitions (not merely citing it), and independently spelling out and
checking BOTH directions of the §6 "logical equivalence" argument — **no
mathematical, logical, or code-correctness error was found anywhere in
this front.** Every central claim survives independent reconstruction
exactly as stated. Two minor issues were found, both LOW severity,
neither touching the mathematical substance:

| # | Issue | Severity | Location |
|---|---|---|---|
| 1 | A numeric transcription slip in the VERDICT prose: the quoted "ratios `99.97,100.0,100.0,1000.0`" for the `m=3,γ=0.5` example do not match the front's own `03_numerical_verification_inner.log`, which shows `99.7333, 99.9973, 100.0, 1000.0`. | LOW | `ATTEMPT.md` lines 298–300 (VERDICT §, point labeled "Confirmed numerically") |
| 2 | The §6 "logical equivalence" (Reason 2) is framed as "the front's sharpest, most load-bearing finding" and a genuinely new diagnosis; its correctness is fully confirmed (both directions, independently re-derived below), but its *novelty* is somewhat overstated — the target `D(γ)+1-1/(2γ)` was already constructed, by the immediate predecessor, via exactly this same Lemma-E-plus-decomposition route (that is how the predecessor arrived at "the conjectural target" in the first place). Making the equivalence fully explicit as a two-directional statement is a legitimate and useful contribution, but it is closer to "unpacking what the predecessor's own target construction already implied" than to an independent new discovery. | LOW | `ATTEMPT.md` VERDICT point 3, §6 Reason 2 |

Neither issue affects any proved claim, any numerical result, or the
front's own honest bottom line (`C(γ)` remains entirely open; nothing
here constructs, bounds, or resolves it).

---

## §A. Independent re-derivation of the central Watson's-lemma result (task item 1)

**Script:** `01_watson_rederivation.py` / `.log`.

Re-derived `A_m(γ) = m(m+3)/(2γ) - m(m+1)/γ²` from scratch via a
**structurally different symbolic path** than the front's own script 02:

- Combined the two log-expansions (`ln(1-t)^m` and `(n-m)ln(1-γt)`) into
  a **single** exponent and exponentiated once (the front expands them
  as two separate factors and multiplies), then integrated the
  resulting polynomial-in-`s` correction term-by-term against the exact
  Gamma moments `∫s^p e^{-γs}ds=p!/γ^{p+1}`.
- Independently re-derived the prefactor expansion
  `(n+m+1)!/(n-m)! ~ n^{2m+1}[1+(2m+1)/n+O(1/n²)]` via a **different
  sympy code path**: expressing the ratio as `RisingFactorial(n-m+1,
  2m+1)` (an explicit polynomial in `n` for each fixed `m`), substituting
  `n=1/ε`, and Taylor-expanding — not the front's by-hand
  arithmetic-series-sum argument (`Σk=2m+1`).
- Assembled both pieces independently and confirmed, **symbolically,
  exact difference `0`**, that this reproduces
  `A_m(γ)=m(m+3)/(2γ)-m(m+1)/γ²` for general `m`, and matches the
  front's own printed table at `m=2,3,4` exactly
  (`A_2=(5γ-6)/γ²`, `A_3=3(3γ-4)/γ²`, `A_4=2(7γ-10)/γ²`).
- Independently re-confirmed both validation checks: `A_0(γ)=0` exactly,
  and `-γA_1(γ)=c(γ)=2(1-γ)/γ` exactly.

**Also verified by hand** (shown in the report body during review, not
just by sympy): expanding `A_m(γ)/n` at `m=λ√n` reduces algebraically to
`λ²[1/(2γ)-1/γ²] + (λ/√n)[3/(2γ)-1/γ²]`, matching script 02's own claimed
decomposition.

**Conclusion: the central closed form is correct.** Independently
re-derived via a different method, not merely re-checked.

---

## §B. Independent numerical verification (task item 1, continued)

**Script:** `02_numeric_check.py` / `.log`.

Two evaluators, **neither structurally similar to the front's own**
(which substitutes `t=s/n` and seeds quadrature nodes near the expected
peak `s*~m/γ`):

1. **An EXACT route** (zero quadrature error): Euler's classical
   integral representation of `₂F₁` gives
   `I(n,m,γ)=B(m+1,m+1)·₂F₁(m-n,m+1;2m+2;γ)`, a **terminating** series
   (since `m-n` is a negative integer) summed exactly via `mpmath.hyp2f1`
   — no numerical integration at all. Used at `n` up to `3200`.
2. **A plain, differently-structured quadrature** directly on `t∈[0,1]`
   with no substitution and no node seeding, pushed to `n` up to `10^9`.

Both agree with the front's `A_m(γ)` prediction to the expected `O(1/n)`
rate at every point tested, and agree with **each other** (routes 1 and
2, computed completely independently) to `<10^{-59}` at shared test
points. The `O(1/n)→O(1/n²)` rate-doubling structure (successive
relative-error ratios `≈100`, then `≈10` at the final `10×`-in-`n` jump)
is reproduced cleanly at `m=2,3`, `γ=0.5`, `n` up to `10^9`.

**Conclusion: independently confirmed, both the limit and the claimed
rate.**

**Separately, reading the front's own final committed scripts** (not
just the narrative in §7): the two disclosed precision bugs in
`03_numerical_verification_inner.py` (insufficient `+40`-only guard
digits independent of `m`; the stale-`mpf`-at-old-precision caching bug)
are **genuinely absent from the committed script** — `dps` is computed
as `max(80, log10(n)+40+10*m)` and `g`/`Am_pred` are recomputed fresh,
at the current high `dps`, immediately before every comparison, exactly
as claimed. The disclosed unit-mismatch bug in `04_matching_verification.py`
(comparing a `λ`-carrying expression against a bare stripped coefficient)
is also genuinely absent from the committed script — both `CLAIM 1` and
`CLAIM 2` correctly strip the matching power of `λ` via `.coeff(...)` /
explicit division before comparing. **All four self-caught issues are
genuinely fixed in the final committed code, not merely narrated as
fixed** (task item 5, confirmed).

**A minor, LOW-severity finding on the numbers quoted in the VERDICT**
(see table above, issue 1): the specific ratio figures quoted for the
`m=3,γ=0.5` example do not match the front's own log. Every *other*
number checked in `ATTEMPT.md` against its cited log (§3's `6.5×10^{-k}`
sequence, §5 Part A's four crossover values, §5 Part B's entire table)
matches its log exactly to the precision quoted — this appears to be an
isolated transcription slip, not a pattern.

---

## §C. Independent re-derivation of the §4 matching claims (task item 2)

**Script:** `03_matching_and_equivalence.py` / `.log`, Part (a).

Re-derived both CLAIM 1 and CLAIM 2 via a genuinely different technique
than the front's own script 04 (which introduces a formal symbol
`sqrtn:=√n` and uses `sp.limit(...,sqrtn,oo)` to peel off the
`sqrtn`-independent piece): here, `A_m(γ)/n` at `m=λ√n` is substituted
with `√n=1/u` (`u:=1/√n`) directly, turning it into an ordinary
polynomial in `u`, and the `u⁰`/`u¹` coefficients are extracted via
`.coeff(u,0)`/`.coeff(u,1)` — a different sympy code path entirely.

- **CLAIM 1** (leading `O(λ²)` piece `= T_prof`'s own `λ²` Taylor
  coefficient): independently confirmed, exact symbolic difference `0`.
- **CLAIM 2** (subleading `O(λ/√n)` piece `= T_prof(0,γ)×Δ_total`'s own
  linear-in-`λ` coefficient): independently confirmed, exact symbolic
  difference `0`.

Both were also confirmed by direct hand algebra during this review
(shown in §A above). **Conclusion: both matching claims are correct,
confirmed via an independently-implemented route.**

---

## §D. The §6 "logical equivalence" — the front's central claim (task item 3)

### D.1 Tracing "Lemma E" to its source

Grepped the full record (`05_DISCOVERY_LAB/`) for "Lemma E" outside this
front's own directory. **Original source located:**
`.../gamma_scaling_attempt/gamma_second_order_attempt/ATTEMPT.md`
(wave 18, `DISC-DEC-078`), §2, lines ~138–163:

> **Lemma E.** Fix `γ∈(0,1]`. ... Suppose `S_n = G_n + D + o(1)` as
> `n→∞`, for a constant `D=D(γ)` not depending on `n`. Then
> `√n(R_n−T(γ)) → C(γ) := (2/√π)√γ D(γ)`. Conversely, if
> `√n(R_n−T(γ))→C` for some constant `C`, then `S_n = G_n + D + o(1)`
> with `D=(√π/(2√γ))C`.

This is a genuine, general, **both-directions** biconditional between
"`S_n` has a limit `D` relative to `G_n`" and "the scaling-law's
second-order term has a limit `C`" — for ANY constant `D`, not just the
specific conjectured closed form. It was independently confirmed
**PROVED** by an earlier, dedicated referee
(`gamma_second_order_attempt/adversarial/REFEREE_REPORT.md`: "Lemma E
(equivalence, §2): CONFIRMED PROVED, both directions... via two
independent algebraic routes"). The crossover front's §6 citation of
"Lemma E's cited equivalence `C(γ)⟺S_n=G_n+D(γ)+o(1)`" **matches this
original statement exactly** — no drift, no misquotation, correctly
substituting the specific `D(γ):=D_0(γ)+E_heuristic(γ)` closed form
(traced through `gamma_c_gamma_construction_attempt/ATTEMPT.md` §1, and
consistent throughout the whole sub-lineage from Estágio 26 onward).

### D.2 Independent re-derivation of both directions of the equivalence

**Script:** `03_matching_and_equivalence.py` / `.log`, Part (b).

The front's own script 05 Part C only writes out the **forward**
substitution (assume `C(γ)` holds, derive the crossover target). This
review wrote out and checked **both directions independently**:

- **Forward:** assuming `S_n=G_n+D+o(1)` (Lemma E's hypothesis) and
  `S_n'=1+S_n`, the predecessor's decomposition
  `S_n'-G_n-1/(2γ)=crossover(n,γ)+o(1)` forces
  `crossover(n,γ)→D+1-1/(2γ)` — confirmed exactly, symbolically.
- **Backward:** assuming `crossover(n,γ)→D+1-1/(2γ)`, the SAME
  decomposition, solved the other way, forces `S_n'→D+G_n+1`, hence
  `S_n=S_n'-1→G_n+D` — exactly Lemma E's hypothesis — confirmed exactly,
  symbolically.

Both directions are genuine algebraic consequences (not merely
one-directional as the front's own script literally demonstrates,
though its prose does correctly claim both directions).

### D.3 Independent re-verification of the one non-trivial cited fact this argument leans on: `S_n'(γ)=1+S_n(γ)`

**Script:** `03_matching_and_equivalence.py` / `.log`, Part (c).

This identity — cited, not re-derived, by every front in this
sub-lineage since Estágio 52 — is the one place the §6 argument could
silently fail if it were wrong. Independently implemented **both sides
from PRIMARY combinatorial definitions** (not from any cited closed
form): `A_k(n,γ):=Σ_{m=0}^kC(k,m)γ^m(1-γ)^{k-m}P_{k,m}`,
`P_{k,m}:=∏_{i=1}^m(1-(k-i)/n)`, `S_n(γ):=Σ_{k=1}^nA_k(n,γ)`, against
`term_m(n,γ):=(γ/n)^m m! T(n,m)`, `T(n,m):=Σ_jC(j+m,m)C(n-j,m)(1-γ)^j`,
`S_n'(γ):=Σ_{m=0}^nterm_m(n,γ)`. Checked at `n=3,4,5,6`, `γ∈{1/3,2/5,3/7}`
in **exact rational arithmetic**: **12/12 exact matches, `S_n'=1+S_n`
holds identically at every point.**

### D.4 Verdict on the §6 argument

**The equivalence claimed — `crossover(n,γ)→D(γ)+1-1/(2γ)` is logically
equivalent to `C(γ)` itself holding — is mathematically CORRECT, in
both directions, and not overstated as a matter of validity.** It relies
on three ingredients, all independently confirmed here: (1) `S_n'=1+S_n`
(re-verified from primary definitions above), (2) the predecessor's
decomposition with a rigorously (not just numerically) vanishing tail
(re-read in full; the tail is bounded via the same Poisson-summation
machinery that gives the front's own §2 exponential rate — genuinely
`o(1)`, not merely observed to shrink), and (3) Lemma E itself (traced
to its exact original source and independently confirmed sound above).

**However** (issue 2 in the table above): the framing of this as the
front's "sharpest, most load-bearing finding," discovered here for the
first time, somewhat overstates its novelty. The predecessor
(`gamma_outer_sum_poisson_attempt/ATTEMPT.md` §4 Part B) had *already*
named `D(γ)+1-1/(2γ)` as "the conjectural target" — and the only way to
arrive at that specific number, rather than any other, is by running
exactly the Lemma-E-plus-decomposition substitution this front performs
explicitly in §6. In that sense the front's contribution is making
fully explicit, in both directions, a fact that was already implicit in
*how the predecessor's own target was constructed* — a legitimate and
useful clarification (it is the first place this equivalence is stated
as an explicit theorem-like claim rather than left implicit), but
closer to "unpacking an implicit consequence" than "a new, independent
diagnosis." This does not affect the correctness of the claim, only its
billing.

---

## §E. Independent reproduction of §5 (task item 4)

**Script:** `04_crossover_mass.py` / `.log`.

Reproduced the partial-sum-by-cutoff exploration at **two fresh
`(n,γ)` points** the front never tested (`n=500,γ=0.3` and
`n=1200,γ=0.7`), using a differently-implemented evaluator (plain
`t∈[0,1]` quadrature, no substitution). Findings:

- At `θ=0.5` (`M≈√n`): `γ=0.3` captures `94.8%` of the total;
  `γ=0.7` captures only `36.5%` — **very different fractions from the
  front's own `73.3%` at `γ=0.5`**, confirming substantial `γ`-dependence
  in where the crossover mass accumulates.
- In both fresh cases, essentially all the mass is captured by
  `θ≈0.625`–`0.75`, qualitatively matching the front's own
  "builds up through, not before, the mesoscale" picture.

**This directly corroborates, rather than undermines, the front's own
explicit disclosure** (§8 item 6: "a single `(n,γ)` point... not
elevated to a proved or even confidently-general claim across all
`γ`") — the fresh points show real quantitative variation with `γ`
(`36.5%`–`94.8%` at the same `θ=0.5`, versus the front's single `73.3%`
data point), so the front's own caution against over-generalizing this
section was well-placed and is not a place where the front overclaimed.

**Independently re-ran the front's own §5 Part A/B numbers directly
against its log**: all match exactly (Part A's four crossover values;
Part B's entire 8-row table) — no discrepancy found there.

---

## §F. Self-caught issues (task item 5) — all confirmed genuinely fixed

Read the FINAL committed `.py` files directly (not the narrative) for
all four disclosed issues:

1. **Watson-coefficient hand-algebra slip** (pre-code, in early hand
   derivation): confirmed the committed `02_inner_expansion_derivation.py`
   derives `B1`/`I_correction` via symbolic Gamma-moment substitution,
   never via the buggy hand formula — consistent with the front's claim
   this specific slip "cannot recur in the committed derivation."
2. **`dps`-vs-`m` precision-scaling bug**: confirmed FIXED — committed
   `dps = max(80, log10(n)+40+10*m)`.
3. **Stale-`mpf`-caching bug**: confirmed FIXED — `g` and `Am_pred` are
   recomputed fresh, at the current `dps`, immediately before every
   comparison (line 99–100 of the committed script).
4. **Unit-mismatch in script 04's matching comparisons**: confirmed
   FIXED — both `CLAIM 1` and `CLAIM 2` correctly factor out the
   matching power of `λ` (`term_lambda2/lam**2`, `term_lambda1_over_sqrtn/lam`)
   before comparing bare coefficients.

**All four confirmed genuinely fixed in the code actually shipped, not
merely narrated as fixed.**

---

## §G. Governance / scope discipline (task item 6)

- **Seed block `20260954000–20260954999`**: `grep -rn "20260954"
  05_DISCOVERY_LAB/` (run fresh by this review) finds it ONLY in
  `DECISION_LEDGER.yaml`'s reservation line, `DISCOVERY_LAB_STATE.md`'s
  mirror, and this front's own `ATTEMPT.md`'s self-report — **confirmed
  unused elsewhere**, and `grep -rn "random" *.py` in the front's own
  directory finds no `random`/`numpy.random`/`seed` calls anywhere
  (only a comment stating "no randomness"). **The front's claim of zero
  randomness is accurate.**
- **`git status`** (run fresh by this review, read-only): shows only two
  untracked directories — this front's own new subdirectory (expected)
  and one unrelated pre-existing untracked directory belonging to a
  different, abandoned front (`k3_full_cdf_attempt_ABANDONED_STALLED`,
  not created or touched by this front). No modified, staged, or deleted
  files anywhere in the repository. **Consistent with** the front's
  claim of zero git commands of any kind — though, as with any such
  claim, this review can confirm the *repository state* shows no
  git-affecting side effect, not literally that no read-only `git`
  command (e.g. a `git status`) was ever typed; that part of the claim
  rests on the front's own self-report, per this lineage's established
  practice (cf. Estágio 58, where an analogous claim was checked the
  same way).
- **Scope discipline**: own new subdirectory only; no ancestor
  `ATTEMPT.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/etc. modified
  (confirmed via `git status`/`git diff`, read-only, no changes found).

---

## §H. Overclaim/underclaim check (task item 7)

The VERDICT UP FRONT is, with the two LOW-severity exceptions already
named, an accurate reflection of what was established:

- The claim that the inner-region closed form is "genuinely NEW" and
  "derived here from scratch" is accurate — independently re-derived via
  a different method in §A above, and no ancestor front had previously
  characterized the `m=O(1)`-fixed regime.
- The claim that the two validation checks are "non-circular" is
  accurate: `A_0(γ)=0` is a structural consequence of the new formula
  that happens to match an independently-known exact fact, and
  `-γA_1(γ)=c(γ)` reproduces an independently-proved constant via a
  route (fixed-`m` Watson's lemma) that shares no machinery with `c(γ)`'s
  own original derivation (a direct `term_1/term_0` ratio limit,
  Estágio 52) — confirmed by tracing both derivations.
- The claim that §4's matching "succeeds cleanly at two orders" is
  accurate — independently reconfirmed via a different technique (§C).
- The claim that §6 gives "a precise, non-hand-wavy reason... not a
  restatement of 'this is hard'" is **substantively accurate** (the
  equivalence is a real, checkable, both-directions logical fact, not
  hand-waving) but its framing as the front's most novel/sharpest
  contribution is somewhat oversold relative to how directly it follows
  from how the predecessor's own conjectural target was constructed —
  see §D.4 (issue 2).
- The claim "`C(γ)` for `γ∈(0,1)` remains entirely OPEN... this front
  does not construct, bound, or newly characterize `crossover(n,γ)`'s
  limit or `C(γ)`" is accurate and appropriately modest — no
  underclaiming found either.
- §5's exploratory findings are correctly and explicitly hedged as
  informal/single-point, confirmed appropriate by §E above (the fresh
  points show real point-to-point variability the front's own caveats
  already anticipate).

**No place was found where confidence language exceeds what was shown**,
beyond the one specific "sharpest finding" framing nuance (issue 2,
LOW), and no place was found where the front understates a genuine
result.

---

## Summary for the orchestrating session

| Item | Status |
|---|---|
| §2 Watson's-lemma closed form `A_m(γ)` | Independently re-derived via a different symbolic route — **CONFIRMED CORRECT** |
| §3 numerics (`O(1/n)` rate, `O(1/n²)` next order) | Independently confirmed via two evaluators neither copied from the front (exact terminating-2F1 + fresh plain quadrature) — **CONFIRMED CORRECT** |
| §4 matching CLAIM 1/CLAIM 2 | Independently re-derived via a different bivariate-expansion technique — **CONFIRMED CORRECT, both claims** |
| §5 exploratory mass-accumulation numerics | Reproduced at 2 fresh `(n,γ)` points with a fresh evaluator — **qualitatively consistent**, front's own hedging about `γ`-dependence corroborated |
| §6 logical equivalence (crossover-limit `⟺` `C(γ)`) | "Lemma E" traced to its exact original source and confirmed unmisquoted; both directions of the equivalence independently re-derived; the one load-bearing cited identity (`S_n'=1+S_n`) independently re-verified from PRIMARY definitions (12/12 exact matches) — **CONFIRMED CORRECT**, novelty framing slightly overstated (LOW) |
| §7 self-caught issues (4 disclosed) | All confirmed genuinely fixed in the FINAL committed scripts, verified by reading the code directly — **CONFIRMED** |
| Governance (seed block, randomness, git, scope) | **CONFIRMED CLEAN** |
| VERDICT overclaim/underclaim check | Accurate throughout except one numeric transcription slip (LOW) and one novelty-framing nuance (LOW) |

**Two issues, both LOW severity, suggested as dated correção/nota
footnotes:**

1. **(correção, LOW)** `ATTEMPT.md` lines 298–300: the quoted ratio
   sequence "`99.97,100.0,100.0,1000.0`" for the `m=3,γ=0.5` example does
   not match `03_numerical_verification_inner.log`'s actual values
   (`99.7333, 99.9973, 100.0, 1000.0`). Correct the quoted figures; the
   underlying claim (clean `O(1/n²)` rate confirmation) is unaffected
   and remains true.
2. **(nota, LOW)** VERDICT point 3 / §6: the characterization of the
   logical-equivalence finding as the front's "sharpest, most
   load-bearing finding," discovered fresh here, could be softened to
   acknowledge that the specific target `D(γ)+1-1/(2γ)` was already
   named as "the conjectural target" by the immediate predecessor via
   exactly this same Lemma-E route — this front's genuine contribution
   is making the two-directional equivalence fully explicit and
   rigorous, which is worth having, but is closer to "unpacking an
   already-implicit consequence" than an independently new diagnosis.

No other errors, of any severity, were found after genuine, sustained
adversarial effort across every major claim in the document.
