# Adversarial referee report — `u_prime_hypothesis_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent re-verification of `ATTEMPT.md`'s claim to
> PROVE Hypothesis (U') — `|φ_n^{(K)}-φ_K| ≤ a√K/n` for **all** `n≥1`,
> `0≤K≤n`, with explicit constant `a = 1+√(π/2) ≈ 2.253314` — before
> catalogue. This closes the "single obstruction between Teorema A/C and a
> fully explicit rate" named at the end of
> `uniform_in_c_attempt/ATTEMPT.md` §6.3. Pure combinatorics/asymptotics; no
> physics claim, no Millennium Problem relevance.
>
> **Discipline.** None of this front's own scripts
> (`verify_decomposition.py`, `verify_closed_form.py`,
> `verify_inequalities.py`) or their `.log` files were opened at any point,
> before or after — every claim below was re-derived and re-checked from the
> **primary sources** the target cites, read directly: `THEOREM.md`
> (Definition 4, Estágio 7, Proposição 7.1, the `[Correção
> pós-adversarial, 2026-08-23]` block); `uniform_in_c_attempt/ATTEMPT.md` §6
> in full; `.../error_constant_growth_attempt/all_orders_closed_form_attempt/ATTEMPT.md`
> §4 (Theorem A/B, the primary source for "Estágio 9," including its own
> "Domain caveat"); `k2_open_lemma/ATTEMPT.md` §2–3 (Reduction Lemma A, the
> hand-derived `K=1` case); `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §2 (the
> `(a,b,r)` Markov-chain transition rules, used to build an independent
> ground-truth engine, `mychain.py`, below); and `mk_geometricity_attempt/ATTEMPT.md`
> §2.2 (the elementary-symmetric-polynomial technique Theorem 2 reuses).
> `fractions.Fraction`/`sympy` for everything labelled PROVED or an exact
> identity; `mpmath` (50–60 dps) and `numpy` (double precision) only for
> wide-range numerical stress-testing, never as the basis of a PROVED claim.
> No randomness used or needed. Nothing outside this `adversarial/` directory
> was created, modified, or touched; no git command was run.

---

## 0. Executive summary

**Verdict: SOUND. ACCEPT for catalogue.**

I independently re-derived Proposição 2.1 from Theorem A/B of the primary
Estágio-9 source (not from the target's own §2 transcription of it) and
found it correct; re-verified Theorem 1's exact decomposition identity
symbolically to `K=25` (target: `K≤8`) and exactly (Fraction) to `K=300`
(target's own algebra-only check went to `K=300` but only for a *sub*-identity,
never the full decomposition beyond `K=8`); re-verified Theorem 2's
monotonicity/argmax claim on grids totalling **9,960** `(K,n)` pairs (target:
~300); re-verified Theorem 3's `M_K` identity exactly to `K=1000` (target:
`K≤40`); and gave **Lemma 4.1's algebra — flagged by the orchestrating
session as not yet hand-verified — the most scrutiny of anything in this
report**: both cubic-sign identities were checked symbolically as identically
zero polynomials, the full ratio-to-sign chain was re-derived (catching and
fixing a false alarm in my *own* first-draft script, not in the target — see
§4), and `v_K`/`z_K` monotonicity was confirmed exactly to `K=20{,}000` and
via `mpmath` to `K=10^6`. Lemma 4.2 was checked exactly to `n=1200` and via
`numpy` double precision to `n=10^7`. **Theorem 4's fully assembled
inequality — the target claim itself — was checked with zero violations** at
both binding cases (`n=K+1`, `n=K`) exactly to `K=60`, densely via `mpmath`
to `K=3000`, sparsely to `K=10^5`, and at genuinely interior `n` (not just
the two endpoints) up to `n=100K`. Worst observed ratio (deviation/claimed
bound) across every stage: **0.1624**, consistent with — and independently
reproducing — the orchestrating session's reported 0.148 and the parent
document's own reported approach of the raw ratio toward `a*≈0.367` (my
worst-ratio figures are `a*`-type ratios rescaled by `1/a≈0.4438`, and
`0.1624×2.2533≈0.366`, matching the parent document's own `K=16384` figure of
`0.3645` as a continuation of the same slow convergence — an unplanned
cross-check that the whole apparatus, four documents deep, is internally
consistent).

**Citations audited against their primary sources, not trusted from the
target's paraphrase, and found accurate:**
Estágio 7's `c_K=[(K+2)φ_K-2]/4`, cited by Theorem 2's proof for `c_K≥0`
(equality only `K=0,1`), matches `THEOREM.md`'s own "Estágio 7" section
verbatim and was independently re-confirmed by sign for `K=0..2000`. The
`[Correção pós-adversarial, 2026-08-23]` identity `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n`,
cited by Theorem 3's proof, was read directly in
`uniform_in_c_attempt/ATTEMPT.md` §6.3 and matches the target's use of it
exactly; independently re-confirmed by a from-scratch brute-force enumeration
of the raw uniform-random-mapping model (`n=1..5`, exhaustive over all `n^n`
mappings) and via an independent Markov-chain engine (`n=2..30`).

**The document's own honesty section is accurate, neither over- nor
under-claiming.** The sharp constant `a*=√π(1/√2-1/2)=0.3670872…` is
genuinely not established by this document's proof — my own Theorem-4 sweep
confirms the assembled bound is loose by a factor of roughly `1/0.1624≈6.16`
at `K=10^5`, matching the target's own "roughly a factor of 6" claim almost
exactly — and the named missing ingredient (a matching *lower* bound on
`Q(n)`) is correctly identified as the precise gap, not a vague placeholder.

**No error was found in the mathematics.** One presentational nit is worth
recording (§7).

---

## 1. What I tried to break, and what happened

- **Lemma 4.1's algebra** (explicitly flagged by the orchestrating session as
  not yet hand-verified) — attacked hardest, symbolically and numerically at
  the largest scale in this report (`K` to `10^6`). Held.
- **The two cubic-sign identities** in isolation, and the full ratio chain
  connecting them to `v_K`/`z_K` monotonicity — checked both as raw,
  unreduced polynomial identities (to defend against sympy silently
  cancelling a shared factor and masking a real error — see §4) and via
  direct exact/high-precision monotonicity scans. Held.
- **Theorem 4's inequality chaining**, specifically the `n/√(n+1)≥√n-1`
  elementary step and the `K=n` boundary-case algebra (also flagged as
  unverified upstream) — re-derived by hand (§8) and checked numerically to
  `n=2×10^5`. Held.
- **Edge cases**: `K=0` (Theorem 1 gives `T(n,0)≡0` identically — checked),
  `K=1` (the historically delicate cancellation case, matches `THEOREM.md`
  Proposition 4 exactly), `K=n` exactly (a genuinely different code path —
  `ψ_n^{(K)}`'s own defining "generic non-source point" does not exist at
  `K=n`, so Lemma A's decomposition (2.1) does not apply there at all; I
  confirmed this is a real domain boundary, not a target oversight — see
  §2 and §9), `n=K+1` exactly (the claimed argmax, and where `M_K`'s formula
  is defined).
- **A direct hunt for a counterexample** to the assembled bound itself, over
  four independent computational routes (exact-Fraction at `K≤60`, dense
  `mpmath` to `K=3000`, sparse `mpmath`/`numpy` to `K=10^5`, and interior-`n`
  spot checks up to `n=100K`) — **zero found**.
- **An independent ground-truth engine** (`mychain.py`), built from the raw
  `(a,b,r)` exploration-walk transition rules stated in
  `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §2 — not from any closed form this
  front or its cited sources derive — used to cross-validate Proposição 2.1
  and Theorem 1 independently of every closed-form algebra step. Agreed
  everywhere tested.

I could not break any of it.

---

## 2. Re-deriving Proposição 2.1 from the primary Estágio-9 source

`check01_prop21_theorem1.py` Part A transcribes Theorem A and Theorem B
**directly from `all_orders_closed_form_attempt/ATTEMPT.md` §4** (its own
line range, not the target's §2), independently of the target's own
restatement:

```
g_r(m,b) = r!(r+b)!/(2r+b+1)! · Σ_{j=0}^r C(2r+b+1,r-j) (m+j)!/(m! n^j)      [Theorem A]
h_r(a,b) = (n-a+1)/n · ĝ_r(n-a+1, b+1)                                        [Theorem B]
```

Specializing at `r=K-1, a=0, b=0` and comparing, symbolically in `n`
(`sympy.simplify`), against the target's boxed Proposição 2.1 formula
`ψ_n^{(K),R} = κ Σ_{i=1}^K C(2K,K-i) g(i;n)`, `κ=(K-1)!K!/(2K)!` gives an
**exact symbolic match for `K=1..14`** — the target's own derivation text
only carries out this substitution by hand once, generically in `K`; I
re-did it independently, transcribing the primary source's formula fresh
rather than trusting the target's copy of it, and additionally machine-
checked the resulting algebra at 14 concrete `K`.

**The "Domain caveat."** The primary source flags that Theorem B at `a=0`
evaluates `g`'s closed-form *polynomial expression* outside `g`'s own
probabilistic domain (`m'=n+1>n`), but states this is "perfectly well
defined" as a formula. My symbolic check does exactly what the caveat
licenses — literal algebraic substitution into the closed-form polynomial,
no probabilistic reinterpretation — so it exercises the caveat correctly
rather than sidestepping it.

**Independent numerical cross-check.** `psi_R` computed via Proposição 2.1's
closed form was compared against `mychain.py` — an independent
from-scratch reimplementation of the `(a,b,r)` Markov chain, built only from
the transition-rule *statements* in `k2_open_lemma/k3_attempt_2/ATTEMPT.md`
§2, never from this front's or any sibling's code — for `K=1..12`,
`n=K+1..K+15` (180 pairs, exact `Fraction`): **0 mismatches**. `mychain.py`
was itself first sanity-checked against two independently-published,
differently-derived closed forms before being trusted as ground truth: the
`K=1` hand-derivation of `k2_open_lemma/ATTEMPT.md` §3
(`ψ_n^{(1)}=2/3+1/(6n)`, `ψ_n^{(1),R}=1/2+1/(2n)`, `φ_n^{(1)}=2/3+1/(3n²)`)
and the `K=2` table of `THEOREM.md` §7.4 (`n=3..8`) — both matched exactly.

---

## 3. Theorem 1: the exact decomposition

`check01_prop21_theorem1.py` Part B re-implements Theorem 1's boxed RHS
(`CONST(K)`, `B_j(K)`, `f_j(n)`) independently and its LHS via (2.1) +
Corolário A1 + the re-derived Proposição 2.1 (i.e. via Part A's formulas,
not the target's own collect-and-simplify), and checks
`sympy.simplify(LHS−RHS)==0` for **`K=0..25`** — the target's own T1 test
only reached `K=0..8`. **26/26 exact symbolic matches.**

`check01c_theorem1_highK.py` extends this numerically (exact `Fraction`, no
`sympy`, so much cheaper per `K`) to **`K=0..300`, `n=K+1..K+8`** (2,408
pairs): **0 mismatches** — this checks the *full* decomposition identity, not
merely the coefficient sub-identity the target's own T2 test pushed to
`K=300`. A second pass cross-validates the closed-form `T(n,K)` directly
against `mychain.py`'s independent recursion for `K=1..40`, `n=K+1..K+6`
(240 pairs): **0 mismatches**.

By hand: the two elementary algebraic facts the proof leans on —
`(K+1)(K+j+1)-K(K-j)=(2K+1)(j+1)` (giving `B_j(K)`) and the half-sum
identities `Σ_{j=0}^KC(2K+1,K-j)=2^{2K}`, `Σ_{j=1}^KC(2K,K-j)=2^{2K-1}-\frac12C(2K,K)`
(giving `CONST(K)`) — both expand out correctly by direct polynomial algebra
(re-derived independently on paper before writing any code); the end-to-end
symbolic/exact checks above subsume and confirm this.

---

## 4. Theorem 2: fact (i), the argmax at `n=K+1`

**The load-bearing step, attacked hardest after Lemma 4.1.**
`check02_theorem2.py` Part A re-derives, from scratch (a plain `O(j²)`
polynomial-coefficient DP, not `sympy`'s symmetric-function machinery),
`e_k(1,...,j)` for `j=0..400` and confirms every `e_k>0`, `1≤k≤j` — the
elementary fact underlying both `f_j(n)` and `g(j;n)-1`'s nonincreasing,
nonnegative structure, correctly identified by the target as reused from
`mk_geometricity_attempt/ATTEMPT.md` §2.2 (confirmed by reading that
document directly: its own §2.2 phrase "applied one order more simply for
`g(j;n)-1`" accurately describes what Theorem 2 does with it).

Part B runs three staged exact-`Fraction` grids on `T(n,K)` (nonnegativity,
nonincreasing-in-`n`, argmax at `n=K+1`), well beyond the orchestrating
session's `K=0..9, n≤K+24`:

| stage | range | pairs | violations |
|---|---|---|---|
| B1 (dense) | `K=0..80`, `n=K+1..K+40` | 3,240 | 0 |
| B2 (long tail) | `K=0..15`, `n=K+1..K+400` | 6,400 | 0 |
| B3 (large `K`, sparse) | `K∈{90,100,125,150,175,200,250,300}`, `n=K+1..K+40` | 320 | 0 |

**9,960 pairs total, zero negativity/monotonicity/argmax violations.**

---

## 5. Theorem 3: `M_K = Q(K+1) - (K+1)φ_K`

`check03_theorem3.py` Part A computes `T(K+1,K)` directly (independent of
Theorem 2's argmax claim — evaluated at the concrete point `n=K+1`, not via
"take the sup") and compares against `Q(K+1)-(K+1)φ_K` (`Q` via an
independent exact product-sum, not the closed form of §2–3 at all), exactly,
for **`K=0..1000`** (target's own T4: `K≤40`): **0 mismatches**.

Part C re-confirms the citation Theorem 3's proof leans on — the `[Correção
pós-adversarial, 2026-08-23]` identity `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n` — by
reading `uniform_in_c_attempt/ATTEMPT.md` §6.3 directly (the exact block is
quoted and matches the target's use of it verbatim), and independently
re-derives it two ways: a **from-scratch brute-force enumeration of the raw
uniform-random-mapping model** (`n=1..5`, exhaustive over all `n^n` mappings,
comparing `P(1\text{ cyclic})` against `Q(n)/n`) and `mychain.py`'s
`φ_n^{(n-1)}` (valid there since `n>K=n-1` is within the chain's domain)
against `Q(n)/n` for `n=2..30`. **All match exactly.**

Part B re-confirms the second citation (Estágio 7's `c_K` formula and its
sign, used by Theorem 2's proof) directly against `THEOREM.md`'s own
"Estágio 7" section: `c_K=[(K+2)φ_K-2]/4`, sign-checked `K=0..2000`
(`c_0=c_1=0` exactly, `c_K>0` for `K≥2`): confirmed.

---

## 6. Lemma 4.1 — full detail, the step given the most scrutiny

`check04_lemma41.py`, four independent parts:

**(1) The two boxed cubic identities**, `4(K+1)^3-K(2K+3)^2-(3K+4)` and
`4(K+1)^2(K+2)-(K+1)(2K+3)^2-(-(K+1))`, checked with `sympy.expand`: both
**identically zero polynomials in `K`**.

**(2) The full ratio-to-sign chain** — not just the isolated identities —
`(K+1)/K · (φ_{K+1}/φ_K)^2 - 1` and `(K+2)/(K+1) · (φ_{K+1}/φ_K)^2 - 1`,
built symbolically from the cited exact ratio `φ_{K+1}/φ_K=(2K+2)/(2K+3)` and
checked, over the **raw, unreduced common denominator** (`K(2K+3)^2` and
`(K+1)(2K+3)^2` respectively — deliberately not simplified first), against
the target's claimed raw numerators `3K+4` and `-(K+1)`. Both matched
exactly.

*A note on a false alarm caught and fixed in my own script, not the target's
math*: my first draft called `sympy.simplify` before extracting the
numerator, which silently cancelled a shared `(K+1)` factor between
numerator and denominator (turning `-(K+1)/[(K+1)(2K+3)^2]` into the
equivalent but differently-shaped `-1/(2K+3)^2`), producing a spurious
"mismatch" against the target's stated *pre-cancellation* numerator. This
was a bug in my verification harness (comparing a reduced expression against
an unreduced target), not in the target document — fixed by working over
the explicit unreduced denominator throughout, confirmed correct, and
recorded here in the interest of this archive's culture of naming every
imprecision found, including one's own.

**(3) Exact `Fraction`**: `v_K:=Kφ_K^2` strictly increasing and
`z_K:=(K+1)φ_K^2` strictly decreasing, `K=1..20000` (orchestrating session:
not checked exactly at all). **Confirmed, zero violations.**

**(4) `mpmath` (60 dps, log-gamma so no huge factorials are ever formed)**:
dense `K=1..2000`, then sparse spot checks to **`K=10^6`**, confirming both
sequences sandwich `π/4` and the gap `z_K-v_K` shrinks correctly (from
`2.6×10^{-4}` at `K=3000` to `7.9×10^{-7}` at `K=10^6`, consistent with the
`O(1/K)` rate implicit in the algebra). **Zero violations.**

---

## 7. Lemma 4.2: `Q(n) ≤ 1+√(πn/2)`

`check05_lemma42.py`: exact `Fraction` `Q(n)` (RHS evaluated at 60 dps,
sufficient to resolve the sign at the observed margins) for `n=1..1200`:
**0 violations**, worst observed ratio `0.9700` at `n=1200` (approaching but
never reaching 1 — matches the classical asymptotic `Q(n)=√(πn/2)-1/3+O(n^{-1/2})`
this bound is meant to majorize, not vacuous). Sanity checks on the two
elementary sub-facts (`1-x≤e^{-x}`; `j(j+1)≥j^2`) both hold as expected.
`numpy` double-precision spot checks from `n=1` to `n=10^7` (vectorized,
stress-test only, not load-bearing): **0 violations**, ratio climbing
smoothly toward 1 as `n→∞` (0.9987 at `n=10^7`), exactly the expected
approach to the classical leading-order asymptotic.

**Presentational nit (N-1, not an error):** the target's own §6 says
"target's own check: `n=1..199` exact-ish + a 'wide grid to `n=10^5`' without
stating exactness there" — this is my own script's commentary describing the
target, not a claim about the target that needs correcting; recorded here
only because I want the report's own phrasing distinguished from the
target's. No action needed.

---

## 8. Theorem 4 — the assembled inequality (the actual target claim)

`check06_theorem4.py`, six stages:

**(0) The elementary fact** `n/√(n+1)≥√n-1`, re-derived by hand (squaring
both nonnegative sides of the equivalent `n+√(n+1)≥√(n(n+1))`, reducing to
the always-true `2n√(n+1)+1≥0`) and checked, `n=1..200{,}000`: **0
violations**.

**(1) Exact `Fraction` baseline, `K=1..60`, both binding cases** (`n=K+1` via
`M_K`, `n=K` via the boundary formula): **0 violations**, worst
deviation/bound ratio `0.14793` — closely matching the orchestrating
session's independently reported `≈0.148`, an unplanned but reassuring
agreement between two independent implementations. Cross-checked against
`mpmath` at the same `K` (`|diff|<10^{-58}`): no drift.

**(2) `mpmath` (60 dps), dense, `K=1..3000`, both binding cases** (6,000
checks): **0 violations**, worst ratio `0.16027`.

**(3) Sparse spot checks to `K=10^5`**, both binding cases, using a fast
vectorized `numpy` double-precision `Q(n)` (cross-checked against exact
`Fraction` `Q(5000)` — exact agreement to double precision): **0
violations**, worst ratio `0.16244` at `K=10^5`. (Sanity: `0.16244×2.253314
≈0.3661`, matching the parent document's own convergent-from-below sequence
toward `a*=0.36709…`, e.g. its reported `0.3645` at `K=16384` — an
independent numerical continuation of the same slowly-converging sequence,
four documents removed from where it was first reported.)

**(4) Interior `n`** (not the two binding endpoints), via the closed forms
directly (`mpmath`), `K∈{1,5,20,100,500,2000}`, `n` including `10K` and
`100K`: **0 violations**, worst ratio `0.15964` at `(K,n)=(2000,2001)` —
consistent with Theorem 2's monotonicity (the bound is tightest just past
`n=K+1` and loosens further out, exactly as the nonincreasing-`T(n,K)`
structure predicts).

**By hand**, both binding-case algebra chains in the target's proof were
re-derived independently on paper before any code was written: the generic
case's `M_K<1+a*√(K+1)` substitution and the "maximized at `K=1`, value
`1+a*√2≈1.51914<1+√(π/2)≈2.25331`" claim (confirmed: `1/√K+a*√((K+1)/K)` is a
sum of two functions each strictly decreasing in `K≥1`); and the `K=n`
boundary case's chain, including the identity `1+√(π/2)-a*=1+√π/2` (exact,
since `a*=√(π/2)-√π/2`) and the final factorization
`(1+√π/2)(√n-1)≥0`. Both check out exactly as claimed.

---

## 9. A domain subtlety worth naming explicitly (not an error)

Building `mychain.py` surfaced a genuine boundary that the target document
handles correctly but does not spell out at length: the `(a,b,r)`
transition-rule proposition of `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §2 is
only stated for states with `a+b+r<n`. At `K=n` (every point rerouted), the
starting state `(0,0,K)` has `a+b+r=n`, **outside** that domain — there is no
"generic non-source reference point" for `ψ_n^{(K)}` to even be defined
against. This is exactly why Theorem 4's proof treats `K=n` as a genuinely
separate "boundary case," routed through Proposição 7.1's direct formula
`φ_n^{(n)}=Q(n)/n` rather than through Reduction Lemma A / (2.1) at all — the
target gets this right (it never applies (2.1) at `K=n`), and my own
`phi()` function in `mychain.py` had to add an explicit `assert n>K` after
first crashing on `n=K=2`, confirming the boundary is real and not a
oversight on either side.

---

## 10. Scorecard

| # | Claim | Target status | **Referee verdict, independent scale** |
|---|---|---|---|
| 1 | Proposição 2.1, re-derived from Theorem A/B | PROVED | **CONFIRMED**, symbolic `K=1..14` from primary-source formulas transcribed fresh; cross-checked vs. independent chain, 180 exact pairs |
| 2 | Theorem 1, exact decomposition of `T(n,K)` | PROVED | **CONFIRMED**, symbolic `K=0..25` (target: `≤8`); exact `K=0..300`×8, 2,408 pairs (target's own full-identity check: `≤8`); cross-checked vs. independent chain, 240 pairs |
| 3 | Theorem 2, argmax at `n=K+1` for every `K` | PROVED | **CONFIRMED**, `e_k` positivity `j≤400`; 9,960 `(K,n)` pairs across 3 staged grids, 0 violations (target/orchestrator: ~300 pairs) |
| 4 | Theorem 3, `M_K=Q(K+1)-(K+1)φ_K` | PROVED | **CONFIRMED**, exact `K=0..1000` (target: `≤40`) |
| 5 | Lemma 4.1, cubic identities + `v_K`/`z_K` monotonicity | PROVED | **CONFIRMED**, symbolic (raw + full ratio chain); exact `K≤20{,}000`; `mpmath` to `K=10^6` |
| 6 | Lemma 4.2, `Q(n)≤1+√(πn/2)` | PROVED | **CONFIRMED**, exact `n≤1200`; `numpy` double to `n=10^7` |
| 7 | Theorem 4 / Hypothesis (U'), `a=1+√(π/2)` | PROVED | **CONFIRMED**, 0 violations across exact (`K≤60`), dense `mpmath` (`K≤3000`), sparse (`K≤10^5`), and interior-`n` (`n≤100K`) sweeps |
| 8 | Citation: Estágio 7's `c_K` formula and sign | cited, PROVED elsewhere | **CONFIRMED** against `THEOREM.md` directly, `K=0..2000` |
| 9 | Citation: `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n` | cited, PROVED elsewhere | **CONFIRMED** against `uniform_in_c_attempt/ATTEMPT.md` §6.3 directly; independently re-derived by brute force (`n≤5`) and chain (`n≤30`) |
| 10 | Honesty section: `a*` NOT established; missing ingredient = lower bound on `Q(n)` | stated OPEN | **CONFIRMED accurate** — not overclaimed, not underclaimed; my own worst-ratio figures reproduce the target's "factor of ~6" looseness claim almost exactly |
| 11 | Independent adversarial re-verification | NOT PERFORMED | **NOW PERFORMED — this report** |

---

## 11. Findings

| id | severity | finding |
|---|---|---|
| N-1 | nit, not an error | None found in the target document itself. The one presentational note in this report (§6) concerns a bug in my *own* first-draft verification script (premature `sympy.simplify` masking a raw-numerator comparison), not the target — recorded per this archive's discipline of naming every imprecision, including a referee's own. |

**No mathematical error, gap, citation misuse, or overclaim was found
anywhere in `ATTEMPT.md`.**

---

## 12. Final verdict

**SOUND. ACCEPT for catalogue.** Hypothesis (U') is proved, with the
explicit constant `a=1+√(π/2)=2.253314…`, exactly as claimed. Every one of
the document's four numbered theorems and two lemmas was independently
re-derived and/or re-checked at a scale exceeding what the target itself
tested, using ground truth built fresh from the cited primary sources (never
from this front's own scripts), including a completely independent
`(a,b,r)`-Markov-chain engine used nowhere else in this lineage's adversarial
history. Lemma 4.1's algebra and Theorem 4's inequality-chaining — the two
steps explicitly flagged as not yet hand-verified upstream — received the
most scrutiny in this report and held up completely, including a symbolic
check of both cubic identities as raw (unreduced) polynomials, a
`K`-up-to-`10^6` high-precision monotonicity sweep, and a from-scratch
re-derivation on paper of every algebraic step in Theorem 4's two binding-case
proofs. The document's own honesty section — naming the sharp constant
`a*=0.367…` as open and the missing lower bound on `Q(n)` as the precise next
step — was checked against my own independent numerics and found accurate,
neither overclaiming nor underclaiming what was proved.

---

## 13. Files in this directory

| file | what it does |
|---|---|
| `mychain.py` | independent, from-scratch reimplementation of the `(a,b,r)` exploration-walk Markov chain (transition rules read directly from `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §2), used as ground truth for `ψ_n^{(K)}`, `ψ_n^{(K),R}`, `φ_n^{(K)}` throughout |
| `closed_forms.py` | shared exact (`Fraction`) and high-precision (`mpmath`, log-gamma) implementations of the target's own stated closed forms, used to stress-test the claimed identities/inequalities at scale |
| `check01_prop21_theorem1.py` / `.log` | §2–3: Proposição 2.1 re-derived symbolically from Theorem A/B (`K=1..14`) + 180-pair cross-check vs. `mychain.py`; Theorem 1 symbolic `K=0..25` |
| `check01c_theorem1_highK.py` / `.log` | §3: Theorem 1 exact `K=0..300`×8 (2,408 pairs) + 240-pair cross-check vs. `mychain.py` |
| `check02_theorem2.py` / `.log` | §4: `e_k` positivity `j=0..400`; 3 staged exact grids, 9,960 `(K,n)` pairs |
| `check03_theorem3.py` / `.log` | §5: `M_K` identity exact `K=0..1000`; `c_K` sign `K=0..2000`; `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n` via brute force (`n≤5`) and chain (`n≤30`) |
| `check04_lemma41.py` / `.log` | §6: cubic identities symbolic (raw + full ratio chain); `v_K`/`z_K` exact `K≤20{,}000`; `mpmath` to `K=10^6` |
| `check05_lemma42.py` / `.log` | §7: `Q(n)` bound exact `n≤1200`; sanity checks; `numpy` double to `n=10^7` |
| `check06_theorem4.py` / `.log` | §8: assembled (U') bound — exact `K≤60`, dense `mpmath` `K≤3000`, sparse to `K=10^5`, interior-`n` to `n=100K` |

Reproduce in this order: `python3 check01_prop21_theorem1.py`;
`check01c_theorem1_highK.py`; `check02_theorem2.py`; `check03_theorem3.py`;
`check04_lemma41.py`; `check05_lemma42.py`; `check06_theorem4.py`. All
scripts are self-contained (`sympy`/`fractions`/`mpmath`/`numpy`/stdlib
only) and were written without reading any `.py` file from the parent
`u_prime_hypothesis_attempt/` directory.
