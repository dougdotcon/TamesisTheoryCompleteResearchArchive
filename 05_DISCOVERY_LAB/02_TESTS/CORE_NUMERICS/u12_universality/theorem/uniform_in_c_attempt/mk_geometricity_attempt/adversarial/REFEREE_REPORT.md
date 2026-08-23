# Adversarial referee report — `mk_geometricity_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent re-verification of `mk_geometricity_attempt/ATTEMPT.md`
> ("Qualitative geometric growth of `M_K`, proved"), before catalogue. Target
> claim: `M_K := sup_{n≥K+1}|n(φ_n^{(K)}-φ_K)| ≤ φ_K(K+1)e^{K/2}+K = O(K(√e)^K)`,
> the single named obstruction to dropping Teorema E's `PROVED-MODULO` label in
> `uniform_in_c_attempt/ATTEMPT.md` §5.6.
>
> **Discipline.** Everything below was re-derived from the mathematical
> statements in the target document's prose and cross-checked against the
> **primary sources** it cites (`THEOREM.md` Estágio 9; `k2_open_lemma/ATTEMPT.md`;
> `k2_open_lemma/k3_attempt_2/ATTEMPT.md`; `error_constant_growth_attempt/ATTEMPT.md`;
> `k_general_existence_attempt/ATTEMPT.md`) — read directly, not through the
> target's transcription. **No `.py` file in `mk_geometricity_attempt/` was
> read at any point**, before or after; every script here is written from
> scratch. `fractions.Fraction` / exact integer arithmetic is used for every
> claim labelled PROVED or "exact"; `mpmath` (50–80 dps) only for the
> irrational quantity `e^{K/2}` and for series-convergence sanity checks.
> Nothing outside this `adversarial/` directory was created, modified, or
> touched. No git command was run. No randomness was used or needed —
> everything below is exact combinatorial/symbolic arithmetic or deterministic
> high-precision evaluation.

---

## 0. Executive summary

**Verdict: SOUND.**

I independently re-derived and stress-tested every step of Route A (§2 of
the target document) from the mathematical statements alone, without reading
any of the target's own code, and found **no error of any kind** — not in the
central closed form (Corolário A1), not in the load-bearing monotonicity
argument (§2.2, the step the target document itself flags as the place a
referee should attack first), not in the crude geometric bound (§2.3), not in
the Reduction Lemma A algebra (§2.4), and not in the final assembly (§2.5).
Every numeric range I tested was pushed strictly beyond what the target
document itself tested (see §2 below for exact counts), specifically hunting
for a violation, and found none.

I also independently confirmed, against the **primary sources** rather than
the target's citations of them, that: (a) Corolário A1's closed form
genuinely matches five independently-derived `ψ_n^{(K)}` formulas from three
different predecessor documents (`K=1,2` from `k2_open_lemma/ATTEMPT.md`,
`K=3,4` from `k2_open_lemma/k3_attempt_2/ATTEMPT.md`); (b) Reduction Lemma A's
exact statement and the fact that `ψ_n^{(K)}`, `ψ_n^{(K),R}` are *literally*
defined as probabilities (hence trivially in `[0,1]`) is exactly as the
primary source (`k2_open_lemma/ATTEMPT.md` §2, "Lemma A") states it, not an
unjustified assumption by the target document; (c) the target's
characterization of Route B's archive state — that a general-`b` geometric
bound on `A_r(b),B_r(b)` is genuinely `NUMERICALLY CHARACTERIZED, mechanism
proved` and not established as a closed form anywhere in the archive — is
accurate against `error_constant_growth_attempt/ATTEMPT.md` §6.3's own status
table and `k_general_existence_attempt/ATTEMPT.md`'s own scorecard row 7, both
read directly.

**One minor citation-accuracy nit (not a mathematical error), noted for
completeness:** the target's own §0 (source-reading list, item 3) paraphrases
`error_constant_growth_attempt/ATTEMPT.md` §8.3 item 1 as literally reading
"closed-form for `A_r(b), B_r(b)` … not attempted." The actual text of that
item is about needing "a polynomial-in-`r` rigorous bound" via a `sup_{[0,1]}`
norm, not a verbatim statement about closed forms for `A_r(b),B_r(b)`. The
*substance* of the target's claim is fully supported elsewhere in the same
primary source (§6.3's status-table row, quoted verbatim by the target
correctly in its own §4), so this is a paraphrase-looseness nit, not a
misrepresentation of archive state. See §5 below.

**No overclaim found.** Route B step (c) is labelled OPEN in the scorecard
(item 10) and treated as OPEN consistently everywhere else in the document —
the executive summary, §4's diagnosis, and the scorecard all agree; nowhere is
Route B quietly treated as more resolved than "algebra of (a)/(b) verified,
(c) not established." See §6.

**Scope discipline: confirmed.** `git status` shows the *only* change in the
repository is the new, previously-untracked `mk_geometricity_attempt/`
directory itself; nothing outside it (not `THEOREM.md`, not any sibling
`ATTEMPT.md`, not `DECISION_LEDGER.yaml`) was touched. File mtimes confirm
`DERIVATION_PREREG.md` (13:19:42Z) genuinely predates every `.py`/`.log` file
in the directory (earliest computational file 13:20:05Z, `ATTEMPT.md` itself
written last at 13:29:36Z, after all logs existed) — no curve-fitting. See §7.

---

## 1. Step 1 (Corolário A1's closed form) — **SOUND**

`referee_check_corollary_a1.py` re-implements Corolário A1's stated closed
form,

```
ψ_n^{(K)} = (φ_K/4^K) Σ_{j=0}^K C(2K+1,K-j) (n+j)!/(n! n^j)
```

from scratch (fresh `sympy`, symbolic in `n`), and checks it against **four
independently, first-principles-derived closed forms read directly from their
primary sources** — not the target document's transcription of them:

| `K` | primary source | closed form | match |
|---|---|---|---|
| 1 | `k2_open_lemma/ATTEMPT.md` §3 | `2/3 + 1/(6n)` | exact (`sympy.simplify` diff `=0`) |
| 2 | `k2_open_lemma/ATTEMPT.md` §4.4 | `8/15 + 4/(15n) + 1/(15n²)` | exact |
| 3 | `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §5 | `16/35 + 12/(35n) + 5/(28n²) + 3/(70n³)` | exact |
| 4 | `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §7.1 | `128/315 + 128/(315n) + 103/(315n²) + 52/(315n³) + 4/(105n⁴)` | exact |

All four match bit-for-bit as symbolic rational-function identities (`K=1,2`
were derived in wave 5 by a hand case-analysis on the exploration walk;
`K=3,4` were derived independently again, by a completely different
Markov-chain/telescoping method — a genuinely independent cross-family
confirmation, not a self-consistency check within one derivation route). The
`n→∞` limit of Corolário A1's formula was additionally checked against
`φ_K = 4^K(K!)²/(2K+1)!` for `K=0,…,12` (target tested `K=0,…,8`) — all match
exactly — and `ψ_n^{(0)}≡1` identically, as required. **0 mismatches.**
(`referee_check_corollary_a1.log`.)

---

## 2. Step 2 (the monotonicity argument, §2.2) — **SOUND**, the single most
load-bearing step, attacked hardest

`referee_check_monotonicity.py`, three independent parts, all exact:

**(A) The elementary-symmetric decomposition and positivity.** `g(j;n) :=
Π_{i=1}^j(1+i/n) = Σ_{k=0}^j e_k(1,…,j) n^{-k}` and every `e_k(1,…,j)>0` for
`1≤k≤j`. Re-derived `e_k` from scratch via a from-scratch `O(j²)` dynamic
program (multiplying out `(x+1)(x+2)⋯(x+j)`, tracking exact integer
coefficients — an independent computation from `sympy`'s built-in symmetric-
polynomial machinery, which I initially tried and abandoned as too slow past
`j≈10`), and certified the rational-function identity by evaluating both sides
at more exact rational sample points than the number of unknown coefficients
(a nonzero polynomial of degree `≤j` cannot vanish at more than `j` points, so
`j+6` matching sample points *proves* the identity, not merely suggests it).
Checked `j=0,…,200` (target checked positivity/decomposition only
symbolically for `j=0,…,14`) — **all pass, e_k>0 confirmed for every
`k=1,…,j` at every tested `j`.**

**(B) `f_j(n)` nonincreasing in `n`, `f_j(n)≥0`.** Exhaustive exact
(`Fraction`) grid, `j=0,…,80`, `n=j+1,…,j+500` — **50,399 consecutive pairs
checked (target: 18,299, `j` up to 60, `n` up to `j+300`), 0 monotonicity
violations, 0 negative values.**

**(C) `n(ψ_n^{(K)}-φ_K)` nonincreasing in `n`, `≥0`, argmax at `n=K+1`.**
Exhaustive exact grid, `K=1,…,70`, `n=K+1,…,K+350` (target: `K` up to 40, `n`
up to `K+200`) — **24,430 consecutive pairs checked (target: 7,960), 0
monotonicity violations, 0 negative values, argmax at `n=K+1` in all 70 of 70
tested `K` (target: 40/40).** This part was computed via Corolário A1's
closed form directly, an end-to-end route independent of part (B)'s
product-form computation of `f_j(n)` — the two routes agreeing everywhere
tested is itself a cross-check.

**Assessment.** The argument is, as the target document says, a genuinely
short and clean one: it reduces to `e_k(1,…,j)>0`, a textbook fact about
elementary symmetric polynomials of positive reals (sums of positive
products), applied termwise to a nonnegative-weighted sum. I could not find,
and did not expect to find, a counterexample — the algebra has no hidden
assumption and no edge case at `n=K+1` (the only boundary point, and the sup
is *attained* there, not approached). (`referee_check_monotonicity.log`.)

---

## 3. Step 3 (the crude geometric bound, §2.3) — **SOUND**

`referee_check_crude_bound.py`:

**(i) The half-sum identity** `Σ_{i=0}^K C(2K+1,i) = 2^{2K}` — verified two
independent ways: (a) direct exact computation, `K=0,…,400` (target: `r` up to
59), 0 violations; (b) an independent structural proof from scratch: the
binomial theorem at `x=1` gives `Σ_{i=0}^{2K+1}C(2K+1,i)=2^{2K+1}`; the map
`i↦2K+1-i` on `{0,…,2K+1}` has no fixed point (`i=2K+1-i` would force
`2K+1` even, contradiction), is a bijection `{0,…,K}↔{K+1,…,2K+1}`, and
`C(2K+1,i)=C(2K+1,2K+1-i)` — so the two halves are equal and each is `2^{2K}`.
Verified this bijection/no-fixed-point/symmetry structure directly,
`K=0,…,59`, 0 failures.

**(ii) `M_K^ψ ≤ φ_K(K+1)e^{K/2}`** — `M_K^ψ` was computed **exactly**
(`Fraction`, via an independent re-implementation of Corolário A1 at
`n=K+1`, not reused from Step 2's code), then compared (at 80 `mpmath` dps) to
the irrational bound, for `K=1,…,400` (target: `K` up to 300). **0
violations.** The bound is, as expected, extremely crude (ratio to the exact
value as small as `0.076` already at `K=1`, and shrinking further — consistent
with, not contradicting, the target's own §5 "bonus finding" that the true
rate is far smaller).

**(iii) Sanity checks on the two textbook inputs**: `1+x≤e^x` (2000 random
spot-checks, `x∈[0,50]`, 0 violations) and `j(j+1)≤K(K+1)` for `0≤j≤K`
(`K=0,…,199`, 0 violations). (`referee_check_crude_bound.log`.)

---

## 4. Step 4 (Reduction Lemma A, §2.4) — **SOUND**, and the `[0,1]`
definitional claim confirmed against the primary source, not assumed

`k2_open_lemma/ATTEMPT.md` §2 was read directly (the actual proof of Lemma A,
not `k2_open_lemma/k3_attempt_2/ATTEMPT.md`'s citation of it, which the target
cites). Confirmed exactly as the target states:

- **Lemma A's statement**, `φ_n^{(K)} = (K/n)ψ_n^{(K),R} + (1-K/n)ψ_n^{(K)}`,
  proved there via an exchangeability/symmetry argument (conjugation by a
  within-block transposition), for every fixed `K≥1`, `n>K` — matches the
  target's citation exactly, word for word in substance.
- **`ψ_n^{(K)} := P(K{+}1 \text{ cyclic under } f)`, `ψ_n^{(K),R} := P(1
  \text{ cyclic under } f)`** — these are stated as literal probabilities *by
  definition*, in the same section that proves Lemma A. The follow-up document
  `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §0/§2 restates this identically via
  `ψ_n^{(K)}=g(0,0,K)`, `ψ_n^{(K),R}=h(0,0,K-1)`, both explicitly `P(x^*
  \text{ eventually cyclic})` for two starting states of the same Markov
  chain. **This is genuinely definitional** — the target document's treatment
  of `ψ_n^{(K)},ψ_n^{(K),R}\in[0,1]` as needing no further argument is
  correct, not a gap it is glossing over (as its own §6 flags for a referee to
  check — checked, and it holds up).

`referee_check_reduction_lemma.py` then verifies the target's algebra:

**(A)** `n(φ_n^{(K)}-φ_K) = n(ψ_n^{(K)}-φ_K) + K[ψ_n^{(K),R}-ψ_n^{(K)}]`
follows purely algebraically from Lemma A — verified symbolically with `K`
left as a free parameter, diff `=0`.

**(B)** `|ψ_n^{(K),R}-ψ_n^{(K)}|≤1` given both `∈[0,1]` — trivial; confirmed
by a `201×201` exhaustive grid over `[0,1]²`, 0 violations.

**(C)** An end-to-end sanity check using the **actual** exact closed forms for
`ψ_n^{(K)}` and `ψ_n^{(K),R}` at `K=1` and `K=3` (both read from primary
sources — `k2_open_lemma/ATTEMPT.md` §2/§3 and
`k2_open_lemma/k3_attempt_2/ATTEMPT.md` §5, not fitted): recombining via
Lemma A reproduces the primary sources' own independently-derived `φ_n^{(1)} =
2/3+1/(3n²)` and `φ_n^{(3)} = 16/35+1/(14n)+11/(10n²)+23/(35n³)+6/(35n⁴)`
exactly, and the target's algebraic identity holds exactly for both concrete
cases. (`referee_check_reduction_lemma.log`.)

---

## 5. Step 5 (final assembly, §2.5) and the match to Teorema E — **SOUND**

`referee_check_final_assembly.py`: (i) the bound `B(K):=φ_K(K+1)e^{K/2}+K`'s
consecutive ratio `B(K)/B(K-1)` converges to `√e≈1.64872` (checked `K` up to
300; last-10 ratios agree to `3×10^{-3}`, the expected `O(1/K)` residual from
the polynomial prefactor) — confirming the `O(K(√e)^K)` growth claim is
correctly characterized, not merely asserted. (ii) A ratio test on
`c^K B(K)/K!` confirms eventual geometric decay for every tested `c∈
{0.5,1,2,5,10,50}`, and direct partial summation confirms numerical
convergence (terms become negligible, `<10^{-34}`, well before `K=100` even at
`c=10`). (iii) **Textual match check**: `uniform_in_c_attempt/ATTEMPT.md` §5.6
was re-read directly and its stated requirement — `|n(φ_n^{(K)}-φ_K)|≤M_K`
with `Σ_K c^K M_K/K! <∞` — is a **definitional identity**, not merely a
resemblance, with the target document's own definition of `M_K` (§1) and its
proved consequence (§2.5). No reinterpretation or loosening occurs anywhere in
the chain from Steps 1–4 to this conclusion. (`referee_check_final_assembly.log`.)

---

## 6. Route B (§4) diagnosis — sanity-checked against primary sources, and
found accurate

`referee_check_route_b.py`:

**Step (a)**, the sharper bound `F_r(2,0)≤φ_r·2^r`, was re-derived from
scratch starting from the primary-source closed form
`F_r(2,0)=(φ_r/4^r)Σ_{i=0}^r2^{r-i}C(2r+1,i)`
(`error_constant_growth_attempt/ATTEMPT.md` §6.2), using `2^{r-i}≤2^r` plus
the half-sum identity of §3 above — confirmed exactly, `r=0,…,99`, 0
violations, both for the sharp bound and the ledger's own cruder `2φ_r·2^r`.

**Step (b)**, the algebraic unrolling of Proposição 6's boxed recursion —
`D'_r(b):=[rC'_{r-1}(b)+A_r(b)]/(r+b+1)`,
`C'_r(b):=B_r(b)+[r/(b+r+1)]C'_{r-1}(b+1)+D'_r(b+1)` (read directly from
`error_constant_growth_attempt/ATTEMPT.md` §6.1, not the target's citation) —
was substituted symbolically from scratch (`sympy`, free symbols) and produces
exactly the target's claimed intermediate form, and — since `r/(b+r+1)<1` and
`r/(r+b+2)<1` for all `r>0,b≥0` (confirmed on a `59×30` grid) — exactly the
ledger's crude bound `C'_r(b)≤(B_r(b)+A_r(b+1))+2C'_{r-1}(b+1)` after dropping
one denominator. **Diff `=0` symbolically; the algebra is correct.**

**Step (c) diagnosis (the "is this really open" question).** I read
`error_constant_growth_attempt/ATTEMPT.md` §6.3's status table and §8.3's
open-items list, and `k_general_existence_attempt/ATTEMPT.md` §9's scorecard
row 7, directly. The status table's own words: `A_r(b), B_r(b) —
… geometric, ratio →9/8 — NUMERICALLY CHARACTERIZED, mechanism proved (Lemma
7)`; `D'_r(b), C'_r(b) — improved rigorous bound — geometric, measured ratio
`1.240` at `r=45` — PROVED bound; rate NUMERICALLY CHARACTERIZED`; and
`k_general_existence_attempt/ATTEMPT.md`'s scorecard row 7 verbatim: `Closed-
form expressions for D_r(b),C_r(b),A_r(b) for general r — NOT ATTEMPTED`.
**This confirms the target's diagnosis is accurate**: no general-`b` rigorous
geometric closed-form bound on `A_r(b),B_r(b)` exists anywhere in the archive
as consulted — only a numerically-characterized rate with a proved mechanism
at `b=0`. It is plausible, given this, that the target's assessment ("a
substantial separate undertaking, not a short unrolling exercise") is correct,
though I did not attempt to close Route B myself (out of scope for this
review, and unnecessary since Route A stands independently).

**One nit** (already flagged in §0 above): the target's own source-reading
list (§0, item 3) paraphrases §8.3 item 1 with wording ("closed-form for
`A_r(b), B_r(b)`… not attempted") that is not a verbatim quote of that item
(which is about a polynomial-in-`r` bound via a `sup_{[0,1]}` norm). The
*substance* is still accurate, confirmed via the status-table line quoted
above, which the target also cites correctly and separately in its own §4.
(`referee_check_route_b.log`.)

---

## 7. Scope discipline and honesty checks

- `git status` (repository root): the **only** change is the new, previously
  untracked directory `.../mk_geometricity_attempt/` itself. No file outside
  it — not `THEOREM.md`, not `error_constant_growth_attempt/ATTEMPT.md`, not
  `uniform_in_c_attempt/ATTEMPT.md`, not `DECISION_LEDGER.yaml`,
  `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, or any predecessor
  `ATTEMPT.md`/`REFEREE_REPORT.md` — appears as modified, staged, or deleted.
- `ls -la --time-style=full-iso` on `mk_geometricity_attempt/`: `DERIVATION_PREREG.md`
  is timestamped `2026-08-23T13:19:42Z`; every `.py`/`.log` file in the
  directory has a strictly later mtime (earliest: `verify_corollary_a1.py` at
  `13:20:05Z`); `ATTEMPT.md` itself has the latest mtime of all
  (`13:29:36Z`, after every log file existed) — consistent with the document
  being written to summarize already-completed computation, not the other way
  around. **No evidence of curve-fitting or post-hoc pre-registration.**
- **Overclaim scan**: the executive summary, scorecard (item 10), and §4's
  prose all agree that Route B step (c) is OPEN and not established. I found
  no place where Route B is described more favorably than "steps (a)/(b)
  verified, (c) open" — including the scorecard, which is the place such
  drift most often shows up in this archive's failure pattern. The one
  citation-accuracy nit noted in §0/§6 is about a paraphrase of a primary
  source's wording, not an overstatement of what Route B itself achieves.

---

## 8. Scorecard (this referee's, mirroring the target's own §6)

| # | Target claim | Target status | **Referee verdict** |
|---|---|---|---|
| 1 | Corolário A1 reproduces `ψ_n^{(1)},…,ψ_n^{(4)}`, `n→∞→φ_K` limit, `ψ_n^{(0)}≡1` | PROVED | **CONFIRMED**, exact symbolic match against 4 independently-derived primary-source closed forms (`K=1,2` and `K=3,4` from two different derivation methods), limit checked `K=0..12` |
| 2 | `f_j(n)=Σ_k e_k(1,…,j)n^{1-k}`, every `e_k(1,…,j)>0` | PROVED, elementary | **CONFIRMED**, from-scratch `O(j²)` computation + exact rational-point certification, `j=0..200` |
| 3 | `f_j(n)` nonincreasing; `n(ψ_n^{(K)}-φ_K)` nonincreasing, `≥0`, sup at `n=K+1` | PROVED | **CONFIRMED**, exhaustive exact grids exceeding target's own range in both dimensions (50,399 + 24,430 pairs vs target's 18,299 + 7,960); argmax correct 70/70 |
| 4 | `M_K^ψ≤φ_K(K+1)e^{K/2}` | PROVED, elementary | **CONFIRMED**, exact `K=1..400` (target: 300), 0 violations |
| 5 | `n(φ_n^{(K)}-φ_K)=n(ψ_n^{(K)}-φ_K)+K[ψ^{(K),R}-ψ^{(K)}]`; `ψ,ψ^R∈[0,1]` | PROVED | **CONFIRMED**, symbolic algebra + verified against primary source that `[0,1]` is genuinely definitional |
| 6 | `M_K≤φ_K(K+1)e^{K/2}+K=O(K(√e)^K)` | PROVED | **CONFIRMED**, given 1–5 |
| 7 | `Σ_K c^K M_K/K!<∞` for every `c≥0` | PROVED | **CONFIRMED**, ratio test + direct partial-sum convergence, several `c` |
| 8 | Route B (a): `F_r(2,0)≤φ_r2^r` | PROVED | **CONFIRMED**, `r=0..99` |
| 9 | Route B (b): unrolled Prop. 6 inequality | PROVED, one-line algebra | **CONFIRMED**, symbolic, from scratch |
| 10 | Route B (c): general-`b` geometric bound on `A_r(b),B_r(b)` | OPEN | **CONFIRMED OPEN**, diagnosis matches primary-source status tables/scorecards exactly |
| 11 | (Informational) `M_K^ψ=Θ(√K)` | NUM. CHARACTERIZED, not claimed | Not independently re-verified (informational only, explicitly not load-bearing); no objection |
| 12 | Independent adversarial re-verification | NOT PERFORMED | **NOW PERFORMED — this report** |

---

## 9. Findings, in priority order

| id | severity | finding |
|---|---|---|
| F-1 | nit (citation accuracy) | §0 item 3's paraphrase of `error_constant_growth_attempt/ATTEMPT.md` §8.3 item 1 ("closed-form for `A_r(b), B_r(b)`… not attempted") is not a verbatim quote of that item, which is actually about a polynomial-in-`r` `sup_{[0,1]}`-norm bound. The substantive claim (no general-`b` closed-form geometric bound exists) is independently confirmed accurate via §6.3's status table, quoted correctly elsewhere in the target document (§4). No action required beyond noting it. |

**No other findings.** Every mathematical step in Route A (§2, the actual
proof) was independently re-derived from the stated formulas — not read from
the target's own code — and every inequality checked separately as well as
end-to-end. No error, gap, or unjustified step was found anywhere in Steps
1–5, in the Reduction Lemma A citation, or in the definitional `[0,1]` claim
the target's own §6 flagged for scrutiny.

---

## 10. Final verdicts

* **Corolário A1's closed form (Step 1): SOUND.** Matches four independently
  derived primary-source formulas exactly, plus the `n→∞` limit for `K=0..12`.
* **The monotonicity argument (Step 2, the load-bearing step): SOUND.** The
  elementary-symmetric-polynomial decomposition, positivity, and the resulting
  monotonicity/argmax claim all hold, checked well beyond the target's own
  tested range with zero violations found.
* **The crude geometric bound (Step 3): SOUND.** Both the half-sum identity
  and the final inequality hold exactly, `K` up to 400.
* **Reduction Lemma A and its use (Step 4): SOUND.** The lemma's statement and
  the definitional-probability claim were verified against the actual primary
  source (not merely trusted from the target's citation), and the algebra
  connecting it to `M_K` is a correct symbolic identity, confirmed also with
  two concrete known closed forms.
* **The final assembly (Step 5) and its match to Teorema E: SOUND.** The
  growth rate, the series convergence, and the definitional match to what
  `uniform_in_c_attempt/ATTEMPT.md` §5.6 actually requires were all
  independently confirmed.
* **Route B's diagnosis (§4): SOUND as a characterization of archive state.**
  Steps (a)/(b)'s algebra is correct; step (c)'s "OPEN" label is accurate
  against the primary sources' own status tables and scorecards.
* **Honesty audit: clean.** No overclaim found; scope discipline and
  pre-registration timing both confirmed via `git status` and file mtimes.

**Recommendation: ACCEPT for catalogue.** The theorem `M_K =
O(K(√e)^K)` is correctly proved, and Teorema E's named gap (a written-down
proof of qualitative geometric growth of `M_K`) is genuinely closed by this
document. I attacked the single step the document itself named as most
load-bearing (§2.2's monotonicity argument) with an independent, from-scratch
re-derivation and an exhaustive grid well beyond the target's own tested
range, and could not break it.

---

## 11. Files in this directory

| file | what it does |
|---|---|
| `referee_check_corollary_a1.py` / `.log` | §1: Corolário A1 vs 4 independently-derived primary-source closed forms, symbolic; `n→∞` limit `K=0..12`; `ψ_n^{(0)}≡1` |
| `referee_check_monotonicity.py` / `.log` | §2: from-scratch elementary-symmetric decomposition + positivity (`j=0..200`); exhaustive exact `f_j(n)` monotonicity grid (`j=0..80,n=j+1..j+500`); exhaustive exact `n(ψ_n^{(K)}-φ_K)` monotonicity + argmax grid (`K=1..70,n=K+1..K+350`) |
| `referee_check_crude_bound.py` / `.log` | §3: half-sum identity (direct + structural proof, `K=0..400`/`0..59`); `M_K^ψ≤φ_K(K+1)e^{K/2}` exact vs `mpmath`, `K=1..400`; `1+x≤e^x` and `j(j+1)≤K(K+1)` sanity checks |
| `referee_check_reduction_lemma.py` / `.log` | §4: symbolic algebra of the `n(φ_n^{(K)}-φ_K)` decomposition; `[0,1]`-boundedness sweep; end-to-end check with real `K=1,3` closed forms from primary sources |
| `referee_check_final_assembly.py` / `.log` | §5: ratio test confirming `O((√e)^K)` growth; ratio test + partial sums confirming `Σc^KM_K/K!<∞`; textual match to Teorema E's §5.6 requirement |
| `referee_check_route_b.py` / `.log` | §6: from-scratch re-derivation of Route B step (a)'s sharper bound; symbolic re-derivation of step (b)'s unrolled inequality; primary-source spot-check of step (c)'s "OPEN" diagnosis |

Reproduce in this order: `python3 referee_check_corollary_a1.py`;
`referee_check_monotonicity.py`; `referee_check_crude_bound.py`;
`referee_check_reduction_lemma.py`; `referee_check_final_assembly.py`;
`referee_check_route_b.py`. All scripts are self-contained, use only
`sympy`/`fractions`/`mpmath`/stdlib, and were written without reading any
`.py` file from the parent `mk_geometricity_attempt/` directory.
