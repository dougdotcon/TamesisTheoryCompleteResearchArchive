# REFEREE_REPORT — hostile adversarial verification of `k6_attempt/ATTEMPT.md`

> Independent adversarial referee, target:
> `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/ATTEMPT.md`,
> which makes two classes of claims: (A) UNCONDITIONAL exact closed forms for
> `ψ_n^{(K)}`, `K=6,...,10`, extending wave 6's `K=0..5` ladder by the identical
> mechanical method; (B) CONDITIONAL general-`K` results — a continuum (`n→∞`)
> scaling-limit ODE analysis producing symbolic-`r` closed forms `F_r(t,b)`
> (leading order) and `G_r(t,b)` (`O(1/n)` correction), and a full proof that
> `lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4` for every `K`, all carrying one named caveat
> (§4): the *existence* of the assumed two-term asymptotic expansion, for `r`
> beyond the 11 concretely-checked values, is not independently re-derived from
> first principles.
>
> Reference material read in full before verification: `THEOREM.md` (§5.2's
> Wallis-integral derivation, §7.4's Open Lemma statement, §9's master gap
> list), `../../ATTEMPT.md` (wave 5, `K=2`, the Reduction Lemma A this document
> reuses verbatim), `../ATTEMPT.md` (wave 6, `K=3,4,5`, the `(a,b,r)` Markov
> chain / transfer-matrix method and telescoping-sum algorithm this document
> reuses verbatim and extends), and both prior adversarial reports in this tree
> (`../../adversarial/REFEREE_REPORT.md`, `../adversarial/REFEREE_REPORT.md`)
> for expected format/rigor only — their subjects are different documents and
> were not re-verified here, per the task brief.
>
> Discipline followed: every closed form independently re-derived or
> independently re-executed (never just "the front's script ran"); a fresh,
> differently-strategized brute force written from scratch for `K=6`; every
> ODE in §2–§3 re-derived by hand from the exact discrete recursion *before*
> reading how the document derives it, then cross-checked; every symbolic
> `sympy` identity claim (§2.3, §3.3, §3.4) re-proved with fresh scripts using
> different variable names/structure, not transcriptions of the front's own
> scripts; and — going beyond the document's own verification surface — two
> new checks the document never performs at all (§B.4 below) targeting
> exactly the homogeneous-solution-ambiguity risk the task asked to stress-test.

## Verdict (read this first)

**PART A (the unconditional `K=6..10` claims): SOUND**, with one **BUG_FOUND**
that is a documentation/narrative error, not a mathematical one, and does not
touch any `PROVED` claim. Every exact closed form claimed in §1 was
independently re-derived (own re-execution of the `K`-uniform ladder through
`K=7`, full recursion-substitution proof for all 13 levels at `K=6` and all 16
levels at `K=7`) and independently re-confirmed by a **fresh, differently
implemented** brute force (`numpy`-vectorized walk simulation, not the front's
`multiprocessing`-over-permutations strategy) at **both `K=6, n=7` and
`K=6, n=8`** (the document's own two held-out points), matching to the digit
in both cases. The one bug: §1.2's claim that the recombined `φ_n^{(6)}`'s `1/n`
coefficient is `512/1001` ("matching `6φ_6/4` exactly") is **factually wrong**
— the true coefficient (four independent methods agree) is `1093/6006`. The
closed form itself is correct; only this one descriptive sentence is wrong,
and it does not affect the `K=6` Open Lemma proof (needs only the limit) or
the (separate, correctly-scoped, `ψ`-only) rate conjecture.

**PART B (the general-`K` continuum-ODE argument): SOUND**, in the sense that
every algebraic/symbolic step independently checked — both ODEs, the `F_r`/`c_k`
closed form, the `G_r`/`d_k` closed form, the binomial-sum identity — is
correct, with **zero errors found** after a genuinely adversarial,
from-scratch re-derivation of every piece (not a re-run of the front's own
scripts). The document's own caveat (§4) is **correctly scoped**: the
distinction it draws between what is unconditionally PROVED (§1, and the rate
conjecture at the 11 concrete `K` values) and what is PROVED-MODULO-the-named-
caveat (the general-`r` closed forms and the general-`K` rate theorem) is the
right line to draw, and I found no case where it should move in either
direction. That said, I found two things worth the orchestrating session's
attention, neither of which changes this verdict: (1) a **genuine
documentation defect** — §2.3 and §2.2 both cite "§2.4" for a precise
discussion of the boundary-condition argument that pins down the unique
regular ODE solution (ruling out a homogeneous-solution admixture), but **no
§2.4 exists anywhere in the document** (confirmed by grepping every heading);
(2) a **substantive asymmetry** the document's caveat discussion does not
name: the boundary-condition argument *can* be made rigorous for `F_r`
(bounded, since `g_r` is literally a probability) but has no analogous a
priori justification for `G_r` (an unbounded `O(1/n)` correction term) — this
is exactly the kind of homogeneous-solution risk the task asked me to hunt
for. I went and checked it directly (§B.4 below, a check the document itself
never performs, at `t≠1` where such a discrepancy would be visible and a
`t=1`-only check would miss it) and found **zero evidence of any problem**
across every case checkable (`r=0..5`, several `t<1`, general `b`) — this is
new, non-circular evidence *for* the ansatz, not just a re-confirmation of
already-proved algebra. **My explicit judgment: the caveat is correctly
scoped, not too conservative and not too optimistic** — see the final section
for the full reasoning.

---

# PART A — the unconditional `K=6,...,10` claims

## A.1 Independent re-derivation of the `K=6` transition rules and closed form

`ATTEMPT.md §0` states the `(a,b,r)` Markov chain / transfer-matrix method
(`../ATTEMPT.md §2`'s Proposition and `§3`'s telescoping algorithm) is
**reused verbatim, not re-derived** from wave 6, and that wave 6's own module
`markov_transfer.py` was simply run six rungs further. Wave 6's method was
already independently, adversarially re-derived from first principles and
found SOUND by a prior referee (`../adversarial/REFEREE_REPORT.md`, via a
*different* solution technique — integrating factor vs. hockey-stick
telescoping — with direct substitution into the recursion at every level
`r=0..3`). This referee's job is not to redo that (out of scope, per the task
brief), but to confirm `K=6` specifically was executed and checked correctly,
not merely trusted from the front's own `extend_frontier.py` run.

**What I did (`adv_k6_recursion_check.py`):**

1. **Independent re-execution.** Called `markov_transfer.build_levels(6)`
   myself (not reading the front's `extend_frontier.log` and trusting it) and
   confirmed `ψ_n^{(6)} = g_6(n,0)` matches the document's claimed closed form
   `(2048n⁶+3072n⁵+4293n⁴+4638n³+3529n²+1662n+360)/(6006n⁶)` **exactly**
   (`sympy` symbolic difference `= 0`).
2. **The strong form of check the task asked for: direct substitution into
   the exact recursion.** I typed the two transition-rule equations fresh
   from `../ATTEMPT.md §2`'s Proposition (not imported from any script) and
   substituted **all 13** resulting closed forms (`g_0,h_0,...,g_6,h_6`) back
   into them, symbolic in `n` and `b`. **All 13 `LHS−RHS` simplify to exactly
   `0`.** This is the check that would catch an error the telescoping
   *solver* introduced even if its final answer happened to look plausible —
   it directly tests "does this claimed closed form solve the functional
   equation," not "did the solver script run without crashing."
3. **A second, independently-coded (not `markov_direct.py`) memoized
   exact-`Fraction` direct recursion**, checked against the closed form for
   `n=7..40` (34 values, extending the front's own `direct_check_k6.py`
   range of `n=7..25`). **34/34 exact matches, 0 mismatches.**
4. Confirmed the `n→∞` limit (`1024/3003 = φ_6`) and `1/n` coefficient
   (`512/1001 = 6φ_6/4`) of `ψ_n^{(6)}` — both exact matches, standard
   `sympy.limit`.

**Verdict: SOUND.** No error found in the `K=6` closed form, its underlying
transition rules, or the telescoping solution that produces it.

## A.2 Fresh, independently-implemented brute force at `K=6`

Per the task's explicit instruction, I wrote my own enumeration using a
**different optimization strategy** from the front's `fast_bruteforce.py`
(which parallelizes over permutations via `multiprocessing`, walking the
orbit for each `(π,U)` combination one at a time in a Python loop). Mine
(`adv_bruteforce_numpy.py`) instead **vectorizes over the entire `U`-tuple
space** with `numpy`: for each of the `n!` permutations, it simulates the
walk for *all* `n^K` reroute-tuples simultaneously (array state, visited-set
matrix, early stopping per row), with exact integer counting throughout (a
`Fraction` formed once at the end, exactly as the front's own discipline
requires but via a structurally different code path — no `itertools.product`
in the hot loop at all, no per-combination `Fraction`).

**Self-test before trusting it on `K=6`** (mirroring the front's own
discipline of validating a fast implementation against small known cases
first): ran it against the **already-proved** `K=1,2,3` closed forms
(wave 5/6, independently PROVED, not this document's own output) at 11
`(K,n)` pairs. **11/11 exact matches.**

**The main check, `K=6, n=7`** (`7!×7^6 = 592,950,960` combinations —
**note**: the document's own §1.2 states this count as `592,912,960`, which
is arithmetically wrong; see §A.4 below):

```
K=6 n=7  successes=255658320  denom=592950960  psi=355081/823543  time=76.6s
```

**This matches the document's claimed value (and my own independent
re-derivation in A.1) exactly, bit for bit: `355081/823543`.** A completely
independent brute-force strategy, a completely independent random-mapping
enumeration, and the algebraic re-derivation all agree.

I also launched the `n=8` point (`8!×8^6 = 10,569,646,080` combinations,
~18× the `n=7` search space) in the background as a bonus, second held-out
point (paralleling the document's own `n=7`-then-`n=8` two-point discipline;
the task itself only requires `n=7` *or* `n=8`, and `n=7` above already
constitutes a complete, independent, exhaustive confirmation on its own).
**It has since completed:**

```
K=6 n=8  successes=4415546880  denom=10569646080  psi=191647/458752  time=1669.1s
```

`191647/458752` — **matching the document's claimed `n=8` value exactly**,
and independently reproducing it via a third distinct route beyond the
document's own `fast_bruteforce.py` (which took `2148.4s` there; this
independent implementation took `1669.1s`, a plausible difference given the
different algorithm — vectorized-over-`U`-space vs. parallelized-over-`π` —
not evidence of a stale or copied number, since the two implementations
share no code path). **Two independent brute-force points, `n=7` and `n=8`,
both exact matches**, exactly paralleling the discipline the document itself
applies (and, for `n=7`, matching wave 6's own two-point `n=K+1`-then-fresh-
point convention).

**Verdict: SOUND.**

## A.3 Spot-check of `K=7,8,9,10`

The task requires at least one. I did all four, at two different levels of
rigor:

**`K=7`, full treatment** (`adv_k7_10_spotcheck.py`, Part A): independently
called `markov_transfer.build_levels(7)` (87.2s), confirmed the resulting
`ψ_n^{(7)}` matches the document's claimed closed form
`(16384n⁷+28672n⁶+48818n⁵+67550n⁴+70819n³+52192n²+23868n+5040)/(51480n⁷)`
exactly, and — as with `K=6` — substituted **all 16** levels (`g_0..g_7,
h_0..h_7`) back into the exact recursion, freshly typed. **All 16 satisfy
the recursion exactly.**

**`K=7,8,9,10`, internal-consistency check** (`adv_k7_10_spotcheck.py`,
Part B): took each of the document's own claimed closed forms as given text
and verified, independently, that (a) the `n→∞` limit equals the
independently-known Wallis integral `φ_K = 4^K(K!)²/(2K+1)!` exactly, and
(b) the `1/n` coefficient equals `Kφ_K/4` exactly (the rate conjecture,
fully unconditional here since these are exact finite closed forms — no
continuum argument needed at all):

```
K=7:  limit=2048/6435    match=True    1/n coeff=3584/6435    match=True
K=8:  limit=32768/109395 match=True    1/n coeff=65536/109395 match=True
K=9:  limit=65536/230945 match=True    1/n coeff=147456/230945 match=True
K=10: limit=262144/969969 match=True   1/n coeff=655360/969969 match=True
```

This extends the front's own `verify_via_exact_k9_k10.py` (which covered only
`K=9,10`) to all four of `K=7,8,9,10`. **All 8 checks pass.**

**Verdict: SOUND**, and considerably more thorough than "at least one"
required by the task.

## A.4 BUG FOUND — arithmetic slip, `592,912,960` should be `592,950,960`

§1.2 (and nowhere else — checked by `grep`) states: *"At `K=6,n=7` this is
`7!×7^6=592,912,960` exact `(π,U₁,…,U₆)` combinations."* `7! = 5040`,
`7^6 = 117649`, and `5040 × 117649 = 592,950,960`, not `592,912,960`.
Independently confirmed three ways (direct Python multiplication; my own
brute force's own `denom` output above, `592950960`; and
`592950960/823543 = 720 = 6!` exactly, the expected `n!/K!`-type sanity
factor, whereas `592912960/823543 ≈ 719.95`, not an integer).

**Severity: cosmetic.** This is a transposed-digit-style arithmetic error in
descriptive prose about the *size* of the search space — it does not affect
any computed value (the actual result `355081/823543` is correct, as
confirmed above by three fully independent methods) and does not appear in
the executive summary (which rounds to "593M," which is fine either way).

## A.5 BUG FOUND — the `φ_n^{(6)}` "`1/n` coefficient `512/1001`" claim is wrong

This is a real, confirmed **computational/narrative** error, distinct from
A.4's cosmetic typo. §1.2, check 4, states:

> *"`φ_n^{(6)} = (4096n⁷+2186n⁶+29676n⁵+47655n⁴+56117n³+45424n²+22428n+5040)/(12012n⁷)`
> with `n→∞` limit exactly `φ_6=1024/3003` and `1/n` coefficient `512/1001`,
> matching `6φ_6/4=512/1001` exactly (a sixth independent confirmation of the
> rate pattern, from the combined not the generic-point quantity)."*

**The closed form itself is correct** — independently re-derived in A.1 via
Lemma-A recombination of my own `ψ_n^{(6)}` and `ψ_n^{(6),R} = h_5(0,0)`,
matching bit for bit. **The `1/n` coefficient claim is not.** Four
independent methods (`adv_phi6_rate_bug.py`) — `sympy.limit`, `sympy.series`
in `x=1/n`, `sympy.apart` partial-fraction decomposition, and plain-`Fraction`
numerical extrapolation to `n=10⁶` with no `sympy` involved at all — all
agree the true `1/n` coefficient of this (correct) closed form is
**`1093/6006 ≈ 0.18199`**, not `512/1001 ≈ 0.51149`. `1093/6006` is already
in lowest terms (`6006 = 2·3·7·11·13`; `1093` is prime to all of these) and
is nowhere near `3072/6006 = 512/1001`.

**Why this is an isolated slip, not a deeper error.** The rate-conjecture
pattern `Kφ_K/4` is **correctly and consistently** stated everywhere else in
the document as a claim about `ψ_n^{(K)}` (the generic-point quantity), never
about the recombined `φ_n^{(K)}` — the Executive Summary, §3.4's Theorem, and
§5's restated Theorem all correctly scope it to `ψ`. §5 correctly states only
the *weaker* order claim `φ_n^{(K)}-φ_K = Θ(1/n)` (true: `1093/6006 ≠ 0`),
never asserting a specific coefficient for `φ`. This matches the historical
precedent from wave 5/6, which this document itself cites and does not
contradict: `φ_n^{(K)}`'s own rate coefficient is a *different* number from
`Kφ_K/4` at every previously-computed `K` (`K=1`: the two `Θ(1/n)`
contributions cancel exactly, giving `Θ(1/n²)` instead, wave 5 §3; `K=2`:
coefficient `1/30 ≠ 2φ_2/4=4/15`, wave 5 §6; `K=3`: coefficient
`1/14 ≠ 3φ_3/4=12/35`, wave 6 §5) — so this document's own cited precedents
already show `Kφ_K/4` is *not* generally the `φ`-rate. §1.2's one sentence
appears to be a copy/mental slip that conflated the (correct) `ψ_n^{(6)}`
rate match with the (different) recombined `φ_n^{(6)}` rate, isolated to that
one paragraph.

**What this does and does not invalidate:**
- Does **not** affect the `K=6` Open Lemma proof (`φ_n^{(6)}→φ_6`), which
  only needs the *limit*, correctly proved.
- Does **not** affect the rate conjecture as formally stated and proved
  (§3.4, §5, Scorecard rows 7–8) — that theorem was always about `ψ_n^{(K)}`,
  correctly scoped throughout, and remains correct (independently
  re-verified for `K=6..10` in A.1/A.3 above).
- Does **not** affect §5's `Θ(1/n)` claim for `φ_n^{(K)}`, which remains true.
- **Does** invalidate the specific sentence's claim of "a sixth independent
  confirmation of the rate pattern, from the combined... quantity" — no such
  confirmation exists; this specific claimed check is false and should be
  removed or corrected.

**Severity: moderate documentation/overclaim bug, zero mathematical
consequence for any `PROVED` theorem.** Recommend the orchestrating session
correct this one sentence in §1.2 before treating the document as fully
vetted, but it does not change the PROVED status of anything in the
Scorecard.

## Part A summary verdict

**SOUND**, with the two bugs above (§A.4 cosmetic typo, §A.5 a real but
narrowly-contained narrative error) — **neither invalidates a `PROVED` claim**.
Every exact closed form in §1 (`K=6,...,10`), the `K=6` Open Lemma proof, and
the rate-conjecture matches at `K=6,...,10`, are independently confirmed
correct by this review through re-derivation, recursion-substitution proof,
and fresh brute force.

---

# PART B — the general-`K` continuum-ODE argument

## B.1 Independent re-derivation of both ODEs, from scratch, by hand

Before reading how `ATTEMPT.md §2.2, §3.1` derive their ODEs, I independently
rearranged `../ATTEMPT.md §2`'s exact non-source transition rule into the
form `m[g_r(m,b)-g_r(m-1,b)] + (1+r+b)g_r(m-1,b) = 1 + r·h_{r-1}(n-m+1,b)`
(confirmed this rearrangement is an *exact identity*, no approximation, by
direct algebra: `m·g_r(m,b) - (m-1-r-b)g_r(m-1,b) = m·g_r(m,b) -
[m-(1+r+b)]g_r(m-1,b) = m[g_r(m,b)-g_r(m-1,b)] + (1+r+b)g_r(m-1,b)`, matching
the original recursion's coefficient exactly). Then, by hand:

**Leading order.** Set `m=nt`, `ε:=1/n`. `g_r(m-1,b) = F_r(t-ε,b)+O(ε)
= F_r(t,b) - ε F_r'(t,b) + O(ε²)`, so `m[g_r(m,b)-g_r(m-1,b)] → t F_r'(t,b)`.
On the source-step side, `n-m+1=n(1-t)+1 → (1-t)` as a scaling ratio, giving
`h_{r-1}(n-m+1,b) → Ĥ_{r-1}(1-t,b)`. **Result:** `t F_r'(t,b) + (1+r+b)F_r(t,b)
= 1 + r Ĥ_{r-1}(1-t,b)` — **matches ATTEMPT.md §2.2 exactly**, independently
re-derived, not copied.

**Second order (`O(1/n)`).** Pushed the same Taylor expansion one order
further by hand: `g_r(m-1,b) = F_r(t,b) + ε[G_r(t,b)-F_r'(t,b)] +
ε²[½F_r''(t,b)-G_r'(t,b)+P_r(t,b)] + O(ε³)` (where `P_r` is the *unknown*,
uncomputed `O(1/n²)` term of `g_r`'s own expansion — critically, this term
**cancels out of the difference `g_r(m,b)-g_r(m-1,b)`** to the order needed,
since it appears with the same coefficient at both `m` and `m-1` to leading
order; I verified this cancellation explicitly rather than assuming it,
since an unaccounted `O(1/n²)` term surviving into the `O(1/n)` equation
would be exactly the kind of subtle bug that could silently corrupt the
result). Working through the full expansion by hand for both the
non-source-step (`g`) and source-step (`h`) recursions, I obtained:

```
t G_r'(t,b) + (1+r+b)G_r(t,b) = r Ĥ_{r-1}'(1-t,b) + r K_{r-1}(1-t,b)
                                  + (t/2)F_r''(t,b) + (1+r+b)F_r'(t,b)

K_r(s,b) = 1 + r Ĥ_{r-1}(s,b+1) + (1-s)G_r(1-s,b+1) - (1+b+r)F_r(1-s,b+1)
```

**Both equations match `ATTEMPT.md §3.1` exactly, sign for sign** — including
the specific place the document itself flags as a likely bug location (the
`+1` shift in `n-m+1` for the `g`-recursion's source-term argument vs. the
clean `a=ns` for the `h`-recursion's own `g_r(n-a,b+1)` term, which I
independently confirmed produces the asymmetric chain-rule term
`ε[Ĥ_{r-1}'(1-t,b)+K_{r-1}(1-t,b)]` on one side but not the other). **No sign
error, no off-by-one, no incorrectly-transferred boundary condition found.**

**Base cases**, verified directly from the *exact* (not asymptotic) formulas:
`h_0(a,b) = (n-a+1)/(n(b+2))` (derived by hand from `h_closed_from_g` at
`r=0`, using `g_0(m,b)=1/(b+1)` exactly), giving `Ĥ_0(s,b)=(1-s)/(b+2)` and
`K_0(s,b)=1/(b+2)` **exactly** (this term has no `O(1/n²)` correction at all
— confirmed, since `h_0`'s exact closed form is itself only linear in `1/n`).
Matches the document's stated base cases exactly.

**Verdict: SOUND.** Both ODEs, independently re-derived from the exact
discrete recursion with no reference to the document's own derivation until
after completing my own, agree exactly, sign for sign, with what
`ATTEMPT.md §2.2, §3.1` claim.

## B.2 Independent verification of the closed-form solutions

**`F_r`/`c_k^{(r)}(b)` (§2.3).** Independently re-derived (by hand, then
confirmed with `sympy`) the "diagonal coefficient matching" recursion the
leading-order ODE forces:
`(1+r+b)c_0^{(r)}(b)=1`, `(k+1+r+b)c_k^{(r)}(b) = r·c_{k-1}^{(r-1)}(b+1)`
for `k≥1`. Wrote a fresh script (`adv_verify_c_recursion.py`) verifying — for
**symbolic `r,k,b`**, not looped concrete values — that the document's
claimed closed form `c_k^{(r)}(b) = [r!/(r-k)!]/∏_{i=1}^{k+1}(r+b+i)`
satisfies both cases exactly (`LHS−RHS simplify = 0` for both). Also
confirmed the sum genuinely self-terminates at `k=r` (the falling-factorial
numerator vanishes identically at `k=r+1`, symbolic `r`).

**`G_r`/`d_k^{(r)}(b)` (§3.3) — the harder check.** Rather than transcribing
`../verify_dk_recursion.py`'s docstring-stated recursion and only checking
the closed form against *it*, I first **independently extracted the
coefficient-of-`t^k` recursion from the O(1/n) ODE myself**
(`adv_verify_d_recursion.py`), using generic `sympy.IndexedBase` coefficient
sequences and `sympy`'s own series/differentiation machinery — a genuinely
different, unbiased derivation path — and confirmed at `k=0,1,2,3,4,5` that
the extracted general-`k` pattern matches what the front's script asserts.
Then (`adv_verify_d_recursion_part2.py`, fresh variable names/structure, not
copied) verified the document's claimed closed form
`d_k^{(r)}(b) = C(k+2,2)·[r!/(r-k-1)!]/∏_{i=1}^{k+2}(r+b+i)` satisfies this
independently-extracted recursion exactly, for **symbolic `r,k,b`**, both the
general `k≥1` case and the `k=0` boundary case. Also confirmed
`d_r^{(r)}(b)=0` symbolically (correct self-termination at `k=r-1`).

**Verdict: SOUND.** Both closed forms independently confirmed to solve their
respective recursions for fully symbolic `r,k,b` — this is the strongest
form of check available short of a from-scratch existence proof (which is
exactly what §4's caveat says is missing, and correctly so — see §B.4).

## B.3 Independent verification of the binomial-sum identity (§3.4)

`adv_verify_binom_sum.py`, three lines of attack:

1. **Every algebraic step of the document's own hand proof**, checked
   symbolically: `w(i):=(r-i)(r-i+1) = i²-ni+r(r+1)` at `n=2r+1` (exact,
   `expand` gives `0` difference); the symmetry `w(n-i)=w(i)` (exact); the two
   vanishing middle terms `w(r)=w(r+1)=0` (exact); the three classical
   binomial moment sums, re-derived via the textbook
   differentiate-`(1+x)^n`-at-`x=1` method (a different, more robust route
   than `sympy.summation`'s built-in symbolic-bound evaluator, which turned
   out to return an unhelpful `Piecewise` for the `i²` moment in this `sympy`
   version — noted and worked around, not silently accepted); assembling
   these gives `Σ_{i=0}^{2r+1} w(i)C(2r+1,i) = r·2^{2r}` exactly, and halving
   (symmetry + 2 vanishing middle terms) gives the Lemma's
   `Σ_{i=0}^{r-1}... = r·2^{2r-1}` exactly.
2. **An attempt at a fully automated, general-symbolic-`r` proof** via
   `sympy`'s Gosper-algorithm hypergeometric summation (`gosper_sum`) — a
   genuinely different code path from the plain `sympy.summation` the
   document reports (§6.3) as failing to terminate for a symbolic bound.
   **This also returns `None`** (no closed form found) — this independently
   *corroborates* the document's own honest §6.3 finding that automation
   does not close this particular sum, rather than revealing it was an
   excuse; the hand proof (confirmed above) is genuinely necessary here, not
   a shortcut around laziness.
3. **Exact-integer numeric confirmation, `r=1..60`** (more than double the
   document's own `r=1..25`). **60/60 exact matches.**

**Verdict: SOUND.**

## B.4 THE CENTRAL QUESTION — is §4's caveat correctly scoped?

### (a) Is the "self-consistency forces the ansatz" argument circular?

**Partially, and the document is honest about this, but its supporting
narrative has a real gap.** The diagonal-coefficient-matching step (§2.3,
§3.3) is accurately described as "no summation, pure algebra" *in the sense
that*, **given** a polynomial-in-`t` ansatz of the stated shape, matching
powers of `t` on both sides of a linear ODE is elementary, and I've
independently confirmed this elementary algebra is done correctly (§B.1,
B.2). But — and this is exactly the circularity the task asked me to check
for — **this shows the ansatz is a fixed point of the recursion within the
assumed function class; it does not by itself show the TRUE asymptotic
`g_r(m,b)` actually lies in that class** (as opposed to, e.g., having a `log
n` correction, a non-integer power of `1/n`, or — the specific mechanism I
went and checked, see (b) — an added multiple of the ODE's homogeneous
solution `t^{-(1+r+b)}`). The document itself is careful about this in §4's
prose ("this document establishes what `F_r,G_r` **must equal** *if*
`g_r(m,b)` admits a regular... expansion") — that qualifier is accurate and
appropriately humble.

**However: §4 promises a "precise" resolution of exactly this question in a
section that does not exist.** §2.1 ("justified below, §2.4"), §2.2 ("revisited
in §2.4"), and §2.3 ("`§2.4` discusses this boundary condition's status
precisely") all point to a `§2.4` that would presumably explain *why* the
"regular/bounded as `t→0⁺`" boundary condition legitimately rules out a
homogeneous-solution admixture. **I confirmed by `grep`ping every `##`/`###`
heading in the document that no `§2.4` exists anywhere** — §2 goes directly
from §2.3 to §3. This is a genuine documentation defect, on precisely the
topic most relevant to whether the caveat's own reassurance ("not treated as
a serious open gap") is earned.

### (b) Constructing a partial argument, and a specific asymmetry the caveat's own discussion misses

I attempted to reconstruct, independently, the argument §2.4 was presumably
going to make, and to stress-test it directly.

**For `F_r`: a boundedness argument CAN be made rigorous, and I made it.**
The homogeneous solution to `t X'(t)+(1+r+b)X(t)=0` is `X=C·t^{-(1+r+b)}`,
which blows up as `t→0⁺` for any `C≠0` (since `1+r+b>0`). Since `g_r(m,b)∈
[0,1]` **exactly, unconditionally, for every finite `m,n`** (it is a genuine
conditional probability by construction), any limit `F_r(t,b):=lim_n
g_r(nt,b)` that exists at a given fixed `t>0` must also lie in `[0,1]` (a
limit of a bounded sequence is bounded). A nonzero `C` would force
`|F_r(t,b)|>1` for `t` small enough — contradicting this a priori bound. So
**`C=0` is forced, *given* that `F_r(t,b)` exists as a genuine limit function
near `t=0`** — this only needs the (weaker) existence of the *leading-order*
limit, not the full two-term expansion, so it is not circularly invoking the
very thing being questioned; it is a legitimate, if narrow, deduction. The
document's one-sentence version of this argument (§2.3's parenthetical) is
consistent with this and, as far as it goes, correct — its flaw is only that
it promises a fuller "precise" version that isn't there.

**For `G_r`: no analogous argument exists, and the document does not supply
one — or even flag the asymmetry.** `G_r` is the `O(1/n)` *correction* term,
which has **no a priori bound analogous to "probability ∈[0,1]"** — nothing
in the model guarantees `G_r` stays bounded as `t→0⁺`. Worse, `t→0⁺`
(`m=O(1)` while `n→∞`) is exactly the regime nearest the recursion's own
base-case boundary (`g_r(m,b)` is only defined for `m≥b+r+1`), which is
*precisely* the kind of "boundary layer" region where singular-perturbation
expansions are classically known to behave non-uniformly even when they are
perfectly well-behaved away from the boundary. §3's derivation gives no
argument — boundedness-based or otherwise — for why `G_r`'s homogeneous
solution must vanish; it simply applies the same diagonal-matching procedure
as for `F_r` without addressing why that procedure is licensed here too.
**This is the one genuinely new, substantive point this review adds beyond
what `ATTEMPT.md` itself discusses**, and it sharpens *why* the caveat is
real, not just a generic disclaimer.

**So I went and checked it directly — a test the document itself never runs.**
Every single cross-check anywhere in `ATTEMPT.md` (§2.3's table, §3.3's
`B_r(b)` comparison, §3.4's rate matches) evaluates `F_r`/`G_r` **only at
`t=1`** (since `ψ_n^{(K)}=g_K(n,0)` means `m=n`, i.e. `t=1` always). This
matters because `t^{-(1+r+b)}=1` at `t=1` for *any* exponent — a homogeneous
admixture would only show up there as an easily-absorbed additive constant,
not as a shape discrepancy. Using `markov_transfer.py`'s own exact
`(m,b,n)`-symbolic `g_r` data (the same independent ground truth the
document's own `t=1` checks use, for `r=0..5`, the full range it is
computed), I checked `F_r(t,b)` and `G_r(t,b)` **at `t=1/2,1/3,2/3,3/4,1/5`
— genuinely away from `t=1`** (`adv_check_offdiagonal_t.py`,
`adv_check_Gr_offdiagonal_t.py`):

- `F_r(t,b)`: **30/30 exact matches** (`r=0..5`, 5 different `t` values each,
  general symbolic `b`).
- `G_r(t,b)`: **15/15 exact matches** (`r=1..5`, 3 different `t` values each,
  general symbolic `b`) — including at `r=4,5` where the closed forms are
  visibly intricate multi-term rational functions of `b`, not simple
  patterns that could match by coincidence.

**This is new, non-circular evidence.** It does not (cannot) prove the
ansatz for `r>10` — no finite check can — but it substantially broadens the
test surface beyond anything the document itself performs, specifically at
the point (`t≠1`) where a homogeneous-solution-type discrepancy would be
most likely to surface and least likely to be masked. Finding zero
discrepancies here, for every level where independent ground truth exists,
is genuine (if still bounded) evidence *for* the ansatz's correctness in the
checked range, not merely a re-confirmation of already-proved algebra.

### (c) Assessing the document's own Scorecard and "Proof status, precisely" language

**§5's "Proof status, precisely" is accurately worded**: "Unconditionally
PROVED (no caveat) for `K=0,...,10`... PROVED for general `K`, modulo §4's
stated... regularity assumption." No issue.

**§7 Scorecard rows 5 and 6 are the one place language is more confident than
warranted, when read in isolation.** Row 5 ("Leading-order continuum closed
form `F_r(t,b)`, general `r`") and row 6 ("`O(1/n)`-order continuum closed
form `G_r(t,b)`... general `r`") are both labeled bare **`PROVED`**, with no
"modulo §4's caveat" qualifier — unlike row 7 ("Rate conjecture, general
`K`"), which correctly *does* carry that qualifier. The in-body Theorem
statements these rows summarize (§2.3, §3.3) are themselves labeled "PROVED,
general `r`" the same way. Read together with the rest of the document
(especially §4, which explicitly lists §2.3/§3.3's results as "a conditional
statement" among what carries the caveat), the intended meaning is clear and
correct. But a Scorecard exists precisely to be read *in isolation* by a
downstream cataloguing process — and rows 5–6, read that way, would be
miscategorized as unconditional. **Recommendation: rows 5 and 6 (and the
Theorem-statement labels in §2.3/§3.3) should carry the same explicit
"modulo §4's caveat" annotation row 7 does**, for internal consistency with
the document's own stated discipline. This is a labeling/consistency issue,
not a substantive error — the caveat's *existence* and *scope* are correct;
only two Scorecard rows understate, in isolation, that they are covered by it.

### (d) The other specific risk classes named in the task

- **Sign errors in Taylor expansions:** none found — independent from-scratch
  re-derivation (§B.1) matches sign-for-sign.
- **Incorrectly-transferred boundary condition between `g_r` and `h_r`:**
  none found — both base cases (`G_0≡0`, `K_0(s,b)=1/(b+2)`) independently
  re-derived from the *exact* `h_0` closed form and confirmed exact (§B.1).
- **Unjustified interchange of limits (`n→∞` and the `r`-indexed induction):**
  I looked for this specifically and did not find a hidden interchange. The
  structure is: take `n→∞` **first**, at each **fixed** `r`, to define
  `F_r,G_r`; **then** induct on `r`, using the previous level's (assumed to
  exist) limit function as data for the next level's ODE. This is a
  well-ordered sequence of separate limits, not a swapped double limit — the
  *only* thing not established is whether each individual `n→∞` limit
  exists, which is exactly (and only) §4's already-named caveat, not a
  distinct issue.
- **Is "diagonal coefficient matching... no summation, pure algebra" secretly
  conditional on the same assumption probed in (a)?** Yes, and the document
  is honest about this in §4's prose (though not, per (c) above, consistently
  in its Scorecard). The phrase accurately describes the *computational
  character* of the step (elementary algebra, no infinite-sum machinery
  needed) but does not mean the step is unconditionally informative about the
  true `g_r` independent of the ansatz — it isn't, and never claims to be, in
  the careful §4 prose.

## Part B summary verdict

**SOUND.** Zero errors found in any ODE derivation, closed-form solution, or
binomial-sum identity, after fully independent, from-scratch re-derivation of
every piece (not re-execution of the front's scripts). The one documentation
defect found (missing §2.4) and the one substantive asymmetry named (F_r vs.
G_r boundedness) do not change this verdict, but are worth recording.

---

# Final judgment on the caveat's scoping (the question that matters for cataloguing)

**The caveat is CORRECTLY SCOPED.** Specifically:

- It is **not too optimistic** in a way that would require re-labeling
  anything currently marked PROVED-modulo-caveat as fully unconditional — I
  could not construct, and do not believe there exists, a slick argument
  that closes the existence gap for general `r`; if anything, my own
  additional analysis (§B.4(b): the `F_r`/`G_r` boundedness asymmetry, the
  missing §2.4) sharpens *why* the gap is real, giving the caveat more
  specific teeth than its own prose does, not less.
- It is **not too conservative** either — my own additional checks (§B.4(b),
  testing `F_r`,`G_r` at `t≠1`, a surface the document never explores at all)
  turned up **zero evidence of any actual problem**, for every one of the 6
  concretely-checkable levels (`r=0..5`), which is genuine reassurance beyond
  what the document itself provides. There is no basis, from anything I
  found, to claim the general-`K` result is "more solid than stated" in a way
  that would justify dropping the caveat.
- **What should change, precisely:** (1) fix the dangling `§2.4` references
  (either write the section the caveat's own prose promises, or remove the
  three pointers to it and fold the boundary-condition discussion into §4,
  where it substantively belongs); (2) add the "modulo §4's caveat"
  qualifier to Scorecard rows 5–6 for consistency with row 7 and with §4's
  own body text; (3) correct the `φ_n^{(6)}` `1/n`-coefficient claim in
  §1.2 (§A.5); (4) correct the `592,912,960→592,950,960` typo (§A.4). None of
  these four fixes change which results should be catalogued as unconditional
  vs. conditional — that boundary, as currently drawn by the document, is the
  right one.

**Recommendation for the orchestrating session:** catalogue `K=6,...,10`'s
exact closed forms, the `K=6` (through `K=10`) Open Lemma proofs, and the
rate-conjecture matches at `K=0,...,10` as **fully unconditional PROVED**
(Part A, SOUND, modulo the two narrow narrative corrections in §A.4–A.5,
which touch no PROVED claim). Catalogue the general-symbolic-`r` closed forms
`F_r,G_r` and the general-`K` rate theorem as **PROVED, explicitly
conditional** on §4's named regularity assumption — exactly as the document's
own §4/§5 text (though not its Scorecard) already states.

---

# Files produced by this review

All in
`05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/adversarial/`:

**Part A:**
- `adv_k6_recursion_check.py` / `.log` — independent re-execution of the
  `K=6` ladder, full 13-level recursion-substitution proof, a second
  independently-coded direct-recursion cross-check (`n=7..40`), and the
  limit/rate sanity check.
- `adv_bruteforce_numpy.py` — fresh, `numpy`-vectorized brute force (a
  different optimization strategy from `fast_bruteforce.py`), self-tested
  against the already-proved `K=1,2,3` closed forms before being trusted.
- `adv_bruteforce_numpy_n7.log` — the `K=6,n=7` run: `355081/823543`,
  `76.6s`, matching the document and my own algebraic re-derivation exactly.
- `adv_bruteforce_numpy_n8.log` — the `K=6,n=8` bonus run (not required by
  the task since `n=7` above already fully satisfies it): `191647/458752`,
  `1669.1s`, exact match, a second independent confirmation point.
- `adv_k7_10_spotcheck.py` / `.log` — full independent re-derivation +
  16-level recursion-substitution proof at `K=7`, plus limit/rate
  internal-consistency checks for `K=7,8,9,10`.
- `adv_phi6_rate_bug.py` / `.log` — the four-independent-method confirmation
  of the `φ_n^{(6)}` `1/n`-coefficient error (§A.5).

**Part B:**
- `adv_verify_c_recursion.py` / `.log` — independent symbolic proof that the
  `c_k^{(r)}(b)`/`F_r` closed form satisfies its diagonal recursion, for
  symbolic `r,k,b`.
- `adv_verify_d_recursion.py` / `_part2.py` (+ `.log`s) — independent
  extraction of the `d_k^{(r)}(b)`/`G_r` recursion directly from the ODE via
  generic indexed-coefficient `sympy` series algebra (not transcribed from
  the front's script), then independent symbolic proof the claimed closed
  form satisfies it, for symbolic `r,k,b`.
- `adv_verify_binom_sum.py` / `.log` — full step-by-step symbolic
  verification of §3.4's binomial-sum Lemma proof, an independent
  Gosper's-algorithm automation attempt, and exact numeric confirmation
  `r=1..60`.
- `adv_check_offdiagonal_t.py` / `.log` — **novel check, not in
  `ATTEMPT.md`**: `F_r(t,b)` vs. the true `n→∞` limit of `markov_transfer`'s
  exact data, at `t≠1` (`r=0..5`, 5 `t` values, general `b`). 30/30 match.
- `adv_check_Gr_offdiagonal_t.py` / `.log` — **novel check, not in
  `ATTEMPT.md`**: `G_r(t,b)` vs. the true `1/n` coefficient of
  `markov_transfer`'s exact data, at `t≠1` (`r=1..5`, 3 `t` values, general
  `b`). 15/15 match. This is the check directly targeting the F_r/G_r
  boundedness-asymmetry concern raised in §B.4(b).
- `adv_verify_table32.py` / `.log` — independent, plain-`Fraction`
  recomputation of every one of §3.2's table entries (`G_r(1,0)` vs.
  `rφ_r/4`, `r=1..8`) directly from the already-proved `d_k^{(r)}(b)` closed
  form. 8/8 exact matches, including bit-for-bit agreement with the
  document's own printed table values.

To reproduce: every script above runs standalone with `python3 <script>.py`;
none takes more than a few minutes except `adv_bruteforce_numpy.py` at
`n=8` (background job, ~20-25 min) and `adv_k7_10_spotcheck.py` (~90s for
`build_levels(7)`).

---

# Governance discipline check

- `THEOREM.md`, `../../ATTEMPT.md` (wave 5), `../ATTEMPT.md` (wave 6),
  `ATTEMPT.md` (this k6_attempt document), `DECISION_LEDGER.yaml`,
  `TEST_QUEUE.yaml` — **none modified**, read-only throughout.
- No git commit made in this session.
- All artifacts of this review confined to
  `.../k2_open_lemma/k3_attempt_2/k6_attempt/adversarial/`, as instructed.
- No AI-model name appears in any file created by this review.
