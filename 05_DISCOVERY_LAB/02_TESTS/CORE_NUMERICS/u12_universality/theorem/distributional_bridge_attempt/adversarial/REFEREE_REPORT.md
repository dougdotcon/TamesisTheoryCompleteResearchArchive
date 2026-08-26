# Adversarial referee report — `distributional_bridge_attempt/ATTEMPT.md`

**Target document:** `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/distributional_bridge_attempt/ATTEMPT.md`
(wave 18, front (d), `DISTRIBUTIONAL-BRIDGE-ATTEMPT`).

**Method.** Every claim below was checked by (a) re-deriving the mathematics
by hand from `THEOREM.md`'s Definitions 1–4, Proposition 3, Proposition 4,
and the Estágio 24 continuum result — never by reading the front's own
proofs and nodding along — and (b) independent from-scratch brute-force /
exact-rational-arithmetic code, written without opening
`exact_enumeration.py`, `analyze_cdf.py`, `monte_carlo.py`, or their
`.json` outputs, and without opening any `.py` script from
`k2_open_lemma/` or any other prior front. All numerical checks here use
exact `Fraction` arithmetic (no floating point, no rounding) and no
randomness at all — every claim tested is a finite, deterministic
enumeration, so the reserved seed range `20260876000`–`20260877000` and
this referee's own range `20260877000+` were not needed and were not used.

**Verdict up front: SOUND — ACCEPT for catalogue**, at exactly the tier
claimed: Proposition D0, Lemma R, the `K=0,1` fixed-`K` closure
(Proposition D1 and Corollaries D1.1–D1.3), and Lemma P2 are all **PROVED**;
the `K≥2` fixed-`K` bridge and `P_nn(n,K)→1/(K+1)`, `K≥2`, are honestly and
accurately reported as **OPEN**. No bug was found anywhere in this
document's mathematics. No overclaim and no unnecessary underclaim was
found either.

---

## 1. Proposition D0 (exact finite-`n` CDF mixture identity)

**Re-derivation.** Total probability over `K_n`, plus the standard fact
that i.i.d. Bernoulli's conditioned on their count give a uniform random
subset of that size, plus independence of `π` and the `U_i`'s from `ξ`
(all exactly as stated) gives `P(M_n(c)≤x | K_n=K) = F_n^{(K)}(x)` — agreed,
this is routine given Definition 1/4.

**One place I pushed harder than the document does, and confirmed it holds.**
The proof needs, implicitly, that `M_n^{(K)}`'s *entire law* (not just its
mean) is independent of *which* `K`-subset is fixed as "rerouted" in
Definition 4 — Definition 4 itself only argues this for the mean
(`φ_n^{(K)}`, via exchangeability of a scalar). I checked the stronger,
full-law statement directly: for two `K`-subsets `S,S'` with a bijection
`σ:[n]→[n]`, `σ(S)=S'`, conjugating the whole construction
(`π':=σπσ⁻¹`, `U'_{σ(i)}:=σ(U_i)`) is measure-preserving (conjugation of a
uniform permutation is uniform; a bijective image of i.i.d. uniforms is
i.i.d. uniform) and satisfies `σ∘f∘σ⁻¹ = f'` where `f'` is *literally* the
`S'`-model's random mapping — and cyclic-point count is conjugation-invariant,
so `#cyclic(f) = #cyclic(f')` identically, not just in distribution. This
closes the one implicit gap between "Definition 4 licenses this for means"
and "Proposition D0 needs it for full laws" — no gap found, once checked.

**Status: PROVED**, agrees with the document's own tier.

## 2. Lemma R (CDF-level mixing reduction)

Re-executed the entire proof by hand, `φ_n^{(K)}↦F_n^{(K)}(x)`,
`φ_K↦F_K(x)`, for `x` held fixed throughout. Checked explicitly for the
trap named in the task brief — *does anything implicitly need
monotonicity-in-`x` or some other CDF-specific property not actually
available?* **No.** At every step, `F_n^{(K)}(x)` and `F_K(x)` are used
purely as **numbers in `[0,1]`** at the one fixed `x` under
consideration — the `B_n` bound (`Scheffé` + elementary Poisson-limit
computation, imported unchanged, correctly noted as not referencing `x`
at all), the Chernoff tail bound `δ(c,M)` (depends only on `c,M`, still
correctly independent of `x` and of `K`-content), and the finite-sum
bound (`|F_n^{(K)}(x)-F_K(x)|≤1`, using only that both are CDFs valued in
`[0,1]`, not that they are monotone or right-continuous in `x`). The
`x`-dependence only enters through *which* real number `F_n^{(K)}(x)`,
`F_K(x)` are — never through any structural property of the CDF as a
function. So the proof genuinely does transplant verbatim, exactly as
claimed, and the one place a CDF-specific fact (right-continuity /
monotonicity, hence the Portmanteau theorem itself) *is* actually needed
is correctly kept **outside** Lemma R, in the separate, correctly-cited
Portmanteau reduction of §1 — no property is smuggled into Lemma R that
it doesn't legitimately have available.

Also checked the outer reduction (§1): `F` is `1-e^{-cx^2}` on `[0,1)`,
`0` for `x<0`, `1` for `x≥1`, with its only discontinuity at `x=1`
(jump size `e^{-c}>0` for every `c≥0`, including the degenerate `c=0`
case where the jump is the entire mass) — continuity elsewhere, including
at `x=0`, confirmed directly (`F(0)=1-e^0=0=\lim_{x\to0^-}F(x)`). The
claim "only `x∈[0,1)` carries content" is correct: `x<0` and `x≥1` are
trivial for every `n` since `M_n(c),M(c)∈[0,1]` a.s. (`x=1` itself is not
needed by Portmanteau since it is `F`'s one discontinuity point, though
incidentally `F_n(1)=F(1)=1` trivially too, so nothing is lost either way).

**Status: PROVED**, agrees with the document's own tier. Corollary R.1's
combination step (apply Lemma R pointwise at every `x∈[0,1)`, invoke
Portmanteau) is a correct, direct assembly of already-checked pieces.

## 3. `K=0`

Trivial and exact (`f=π` a bijection, every point of a finite bijection is
cyclic) — agreed, nothing to add.

## 4. Proposition D1 (`K=1` exact finite-`n` CDF) — the centerpiece

### 4.1 From-scratch re-derivation

I redid the case-split independently before reading the document's own
Lemma D1.0/Proposition D1 write-up closely, to avoid anchoring:

- Fix reroute source at index `1`. `π` uniform, `U:=U_1` uniform on `[n]`,
  independent. `L:=` length of `π`-cycle `C` through `1`. `L\sim
  \mathrm{Unif}\{1,\dots,n\}` exactly (`THEOREM.md` §7.3 Step 1, standard
  cycle-length fact, re-checked by the same count-`(n-1)!` argument).
- All `n-L` points outside `C` are cyclic under `f` regardless of `U`
  (§7.3 Step 2 — unaffected forward orbits).
- Inside `C` (label `c_0=1,\dots,c_{L-1}`), only `f(c_0)=U` differs from
  `π`. Case split on `U`: `U\notin C` (prob `(n-L)/n`) → `0` cyclic points
  in `C`, `T=n-L`. `U=c_0` (prob `1/n`) → `1` cyclic point (`c_0`
  self-loops), `T=n-L+1`. `U=c_d`, `d=1,\dots,L-1` (prob `1/n` each) →
  `L-d+1` cyclic points in `C` (the cycle `c_d\to\cdots\to c_0\to c_d`),
  `T=n-d+1`.
- **Conditional law of `T` given `L=\ell`:** as `d` ranges `1,\dots,\ell-1`,
  `n-d+1` ranges bijectively over `\{n-\ell+2,\dots,n\}`. So `T`'s support
  given `L=\ell` is the **contiguous** integer range `\{n-\ell,\dots,n\}`
  — mass `(n-\ell)/n` at the left endpoint, mass `1/n` at each of the
  remaining `\ell` points. Because the support is contiguous with uniform
  `1/n` steps above the left endpoint, the CDF collapses to the single
  clean formula `P(T\le k\mid L=\ell) = k/n` for `k\ge n-\ell` (`0`
  otherwise) — I derived this the same way as the document's Lemma D1.0,
  independently, and it matches exactly.
- **Averaging over `L`:** `P(T\le k) = \frac1n\sum_{\ell=1}^n \frac kn
  \mathbf1\{\ell\ge n-k\}`. For `0\le k\le n-1`: `n-k\ge1`, so the count of
  qualifying `\ell\in\{1,\dots,n\}` is exactly `k+1`, giving `P(T\le k) =
  k(k+1)/n^2`. **Matches Proposition D1 exactly**, derived independently
  from the primitives, not merely re-typed from the document.

### 4.2 Brute-force exhaustive verification

Script `brute_k1.py` (this directory), using an independently-written
`cyclic.py` cycle-detector (`O(n)` per configuration, correctness
sanity-checked on 7 hand-built functional digraphs before use — see
`cyclic.py` and the interactive check in this session's transcript).
Model: enumerate **all** `n!\cdot n` configurations `(\pi,U)` exactly
(`π` ranges over `itertools.permutations`, `U` over `range(n)`), each
equally likely; build `f`, count cyclic points `T`, accumulate the exact
pmf as a `Fraction`-based CDF.

**Result: `n=2,\dots,9` (task asked for `n=2..8` at least — pushed one
further), every `k=0,\dots,n`: exact rational agreement between the
brute-force CDF and `k(k+1)/n^2` (`k\le n-1`) / `1` (`k=n`). Zero
mismatches**, `9-2+1=8` values of `n`, `\sum(n+1)=63` individual `k`-cells
checked. Full log: `brute_k1.log`.

**Status: PROVED.** Proposition D1 is correct — independently re-derived
from Definition 1/4's primitives and independently verified by exhaustive
enumeration with exact arithmetic, no discrepancy at any tested `n`.

## 5. Corollaries D1.1–D1.3

Redid all the algebra independently (not just re-read it):

- **D1.1 (uniform `O(1/n)` rate).** With `k=\lfloor xn\rfloor`,
  `\theta=xn-k\in[0,1)`: `k(k+1)=a(a+1)`, `a=xn-\theta`, expands to
  `x^2n^2 - 2\theta xn+\theta^2+xn-\theta`; dividing by `n^2` gives
  `F_n^{(1)}(x)=x^2+\frac{x(1-2\theta)}n-\frac{\theta(1-\theta)}{n^2}`,
  matching the document's expansion term-for-term. Bounding
  `|x(1-2\theta)|\le1` (`x\le1`, `|1-2\theta|\le1`) and
  `\theta(1-\theta)\le\frac14`: `|F_n^{(1)}(x)-x^2|\le\frac1n+\frac1{4n^2}
  \le\frac5{4n}`. **Confirmed correct**, and the `x=1` boundary case is
  handled correctly by hand-off to the trivial `P(\cdot\le1)=1` identity
  (Proposition D1's own scope is `k\le n-1`; no silent gap at `x=1`).
- **D1.2 (second moment).** From the CDF, `P(T=k)=[k(k+1)-(k-1)k]/n^2=2k/n^2`
  for `k=1,\dots,n-1`; `P(T=0)=0`; `P(T=n)=1/n`
  (`\sum_{k=1}^{n-1}2k/n^2+1/n=(n-1)/n+1/n=1`, checked). `E[T^2]=
  \frac2{n^2}\sum_{k=1}^{n-1}k^3+n = \frac2{n^2}\left[\frac{(n-1)n}2\right]^2
  +n = \frac{(n-1)^2}2+n`. Dividing by `n^2` and simplifying
  `\frac{(n-1)^2}{2n^2}+\frac1n = \left(\frac12-\frac1n+\frac1{2n^2}\right)
  +\frac1n = \frac12+\frac1{2n^2}`. **Matches exactly, redone independently.**
  Cross-checked by brute force (§4.2's script, extended): `E[T]` and
  `E[T^2]` computed directly from the brute pmf match `THEOREM.md`
  Proposition 4's `\varphi_n^{(1)}=\frac23+\frac1{3n^2}` (as `E[T]/n`) and
  Corollary D1.2's `\frac{(n-1)^2}2+n` **exactly**, for every
  `n=2,\dots,9` — zero mismatches (`brute_k1.log`).
- **D1.3 (variance).** `\mathrm{Var}(M_n^{(1)})\to\frac12-\left(\frac23
  \right)^2=\frac12-\frac49=\frac{9-8}{18}=\frac1{18}`. **Arithmetic
  confirmed correct.**

**Status: all three PROVED**, agreeing with the document.

## 6. Lemma P2 (general-`K` second-moment reduction)

**Re-derivation.** `C:=nM_n^{(K)}`. `C^2=\sum_i\mathbf1_i+\sum_{i\ne j}
\mathbf1_i\mathbf1_j`, so `E[C^2]=E[C]+\sum_{i\ne j}P(i,j\text{ both
cyclic})` — linearity of expectation, no probabilistic content beyond
that. Pair-type counting: I independently verified the ordered-pair
counts sum correctly, `(n-K)(n-K-1)+K(K-1)+2K(n-K) = n^2-n=n(n-1)`
(direct algebraic expansion, checked by hand — see working above), so the
partition of all `n(n-1)` ordered pairs by type (`nn`,`rr`,`nr`/`rn`) is
exhaustive and non-overlapping, exactly as claimed. The joint (not just
marginal) exchangeability needed — that `P(i,j\text{ both cyclic})`
depends only on the pair's *type*, not on the specific labels — follows
by the same conjugation argument I used to close the Proposition D0 gap
in §1 above (relabeling within the non-rerouted set, or within the
rerouted set, is measure-preserving and conjugation-invariant on the
cyclic-point set), so this is legitimate, not merely asserted.

**Limit claim.** Coefficients: `(n-K)(n-K-1)/n^2\to1`, `2K(n-K)/n^2\to0`,
`K(K-1)/n^2\to0` (`K` fixed, `n\to\infty`), `\varphi_n^{(K)}/n\to0`
(bounded numerator). Since `P_{nr},P_{rr}\in[0,1]` are bounded, the two
vanishing-coefficient terms `\to0` regardless of the (unknown) limiting
behavior of `P_{nr},P_{rr}` — **correct**, and this is exactly why the
reduction to the single scalar `P_{nn}(n,K)` is legitimate.

**Numerical cross-check.** `brute_generalK.py` (this directory):
independent brute-force enumeration of Definition 4's model at general
`K` (rerouted set `\{0,\dots,K-1\}`, `n!\cdot n^K` configurations,
0-indexed), computing `T`'s full pmf directly (hence `\varphi_n^{(K)}`
and `E[(M_n^{(K)})^2]` directly, with no use of Lemma P2's formula) plus
the three pair-probabilities `P_{nn},P_{nr},P_{rr}` by direct counting
over the indices `(n{-}1,n{-}2)`, `(n{-}1,0)`, `(0,1)` respectively.
Lemma P2's formula was then evaluated from `\varphi_n^{(K)}, P_{nn},
P_{nr}, P_{rr}` and compared against the **directly**-computed
`E[(M_n^{(K)})^2]`.

**Result: `K=1` (`n=3,\dots,7`), `K=2` (`n=4,\dots,7`), `K=3`
(`n=5,6`) — 11 cells, exact rational agreement in every cell, zero
mismatches.** Full log: `brute_generalK.log`.

**Status: PROVED.** Lemma P2's exact identity is correct — re-derived
independently and confirmed numerically, exact arithmetic, across `K=1,2,3`.

## 7. `K≥2` non-closure — honesty check

This document reports `F_n^{(K)}(x)\to F_K(x)` (`K\ge2`) and even
`P_{nn}(n,K)\to1/(K+1)` (`K\ge2`) as **OPEN**, with a stated diagnosis
(§6.1, §6.3): `THEOREM.md`'s Estágios 3–7 machinery (`ψ_n^{(K)}`) is a
single-point marginal device that "carries zero information about any
two-point joint quantity," and the genuinely missing ingredient is either
a whole-space `K=2` case analysis in Proposition D1's style, or a joint
two-point exploration — which `THEOREM.md`'s own Estágio 18/25 already
diagnosed as the hard residual obstruction, **for a related but
different quantity** (the continuum `E[M_K^2]`, since closed by an
unrelated route in Estágio 24).

I checked this diagnosis against `THEOREM.md` directly (§7.4, and
Estágios 18/24/25): §7.4's Open Lemma for `K\ge2` is indeed still open
at the *mean* level for the fixed-`K` bridge as a strategy question
(only proved for `K=0,1`, matching what this front reuses); Estágio 24
closes the *continuum-only* `E[M_K^2]=1/(K+1)` for every `K`, via
general-`K` Conjecture 1, **not** via any joint two-point machinery;
Estágio 25's Theorem J (uniform cyclic restriction, exact `1/2`
same/different-cycle split) is explicitly noted **in `THEOREM.md`
itself** as *not* yielding the value of the relevant "both cyclic"
probability by itself — that front's own §6.2 states resolving the
second moment target requires the general-`K` Conjecture 1 machinery,
which is precisely what actually closed it (by an unrelated route). This
document's careful separation of "the continuum `E[M_K^2]`, now closed"
from "the analogous finite-`n\to\infty` quantity `P_{nn}(n,K)`, not
closed by this route" (Executive Summary, item 5) is an accurate reading
of the archive's own state, not a conflation and not an overclaim of
transferred progress. **The diagnosis is accurate, neither overstated
nor understated.**

## 8. Numerical exploration spot-checks (§7)

Independently computed (not read from the front's own
`exact_enumeration_results.json`):

- `P_{nn}(n,K)`, `K=2`, `n=4,\dots,9`: `19/48, 287/750, 101/270,
  541/1470, 349/960, 175/486` → decimals `0.39583, 0.38267, 0.37407,
  0.36803, 0.36354, 0.36008`. **Matches the document's Sec 7.1(c) table
  to all reported digits**, every value.
- `P_{nn}(n,K)`, `K=3`, `n=5,\dots,8`: decimals `0.31120, 0.30000,
  0.29225, 0.28658`. **Matches** the document's table exactly.
- `P_{nn}(n,1)=\frac12+\frac1{6n}` exact pattern, `n=3,\dots,7`: exact
  rational equality confirmed in every case (`5/9, 13/24, 8/15, 19/36,
  11/21`). **Matches.** (Correctly labeled by the document as an
  exact-verified pattern, *not* a proof for general `n` — agreed, no
  derivation of this closed form is attempted or needed for anything else
  in the document.)
- `D(n,K):=\max_k|F_n^{(K)}(k/n)-F_K(k/n)|`: `D(6,2)=23/240=0.0958` and
  `D(4,3)=303/4096=0.0740`, both **exact matches** to the document's Sec
  7.1(d) table (`dnk_spotcheck.py`, `dnk_spotcheck.log`).

No discrepancy found in any spot-checked numerical claim.

## 9. Self-disclosed issues (§8 of the target document)

The document discloses two process bugs (a `None`-vs-index-tuple gating
bug in `exact_enumeration.py`'s `summarize()`, caught before any
downstream number was affected; a slow numpy-scalar-indexing Monte Carlo
draft, caught by back-of-envelope estimation before running). I did not
open or execute the front's own scripts (per the referee mandate), so I
cannot independently confirm the *bug narrative* itself — but this is
immaterial to the verdict: my own from-scratch enumeration (§4, §6, §8
above) reproduces every final reported number in the document **exactly**
(the `K=1` CDF, the `K=1` second moment, Lemma P2's identity at `K=1,2,3`,
and the `P_{nn}(n,K)` / `D(n,K)` tables at `K=2,3`), which is strong
independent evidence that whatever the bug was, it was genuinely caught
and fixed before any number in the current document was affected, exactly
as claimed.

## 10. Referee's own bugs, disclosed

One minor slip during development, self-corrected before any number was
reported: `check_lemma_P2` in an early draft of `brute_generalK.py`
computed `Prr` unconditionally even when `K<2` — harmless in practice
(the coefficient `K(K-1)/n^2` is exactly `0` at `K\le1` so it never
affected any printed comparison), but the code was left explicit about
gating `Prr`'s meaning on `have_rr` to avoid any doubt; verified by
inspection, not by a failed run — no output was ever generated or
inspected before this was in place. No other bug found in this session's
own verification code (independently sanity-checked the cycle-detector
`cyclic.py` on 7 hand-built digraphs before first use, and cross-checked
`brute_k1.py`'s `n=9` cell — the largest and slowest tested — end-to-end
before trusting the smaller `n`'s built on the same code path).

## 11. Verdict

| # | Claim | This referee's finding |
|---|---|---|
| 1 | Proposition D0 | **PROVED** — confirmed, plus the implicit full-law (not just mean) well-definedness gap independently closed |
| 2 | Lemma R | **PROVED** — re-derived in full; no CDF-specific property (monotonicity etc.) smuggled in or missing |
| 3 | Corollary R.1 | **PROVED** (conditional on the fixed-`K` hypothesis, as stated) |
| 4 | `K=0` bridge | **PROVED** — trivial, exact |
| 5 | Proposition D1 (`K=1` exact CDF) | **PROVED** — independently re-derived from scratch and exhaustively verified, exact arithmetic, `n=2,\dots,9`, 0/63 mismatches |
| 6 | Corollary D1.1 (rate) | **PROVED** — algebra redone, correct |
| 7 | Corollary D1.2 (2nd moment) | **PROVED** — algebra redone and brute-force verified, `n=2,\dots,9`, 0 mismatches |
| 8 | Corollary D1.3 (variance) | **PROVED** — arithmetic confirmed |
| 9 | Lemma P2 | **PROVED** — re-derived and brute-force verified at `K=1,2,3`, 11 cells, 0 mismatches |
| 10 | `K\ge2` bridge / `P_{nn}(n,K)\to1/(K+1)` | **OPEN**, accurately and precisely diagnosed — not overstated, not understated |
| 11 | Numerical tables (§7) | Spot-checked (`P_{nn}`, `K=2,3`; `D(n,K)`, two cells) — **all match exactly** |

**Overall: SOUND. ACCEPT for catalogue**, at exactly the tier the document
itself claims — PROVED for Proposition D0, Lemma R, the `K=0,1` fixed-`K`
closure (Proposition D1 and its three corollaries), and Lemma P2; honestly
OPEN for the `K\ge2` fixed-`K` bridge and `P_{nn}(n,K)\to1/(K+1)`. No bug
was found in the document's mathematics. The document's own self-caught
issues (§8) are process bugs, fully disclosed, and immaterial to every
final claim (independently re-derived and re-verified here). No claim of
progress on any Millennium Problem is made anywhere in the target document
or in this report; this is pure combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble.

---

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `cyclic.py` | independent `O(n)` cyclic-point detector for a functional digraph, sanity-checked on hand-built examples before use |
| `brute_k1.py` | exhaustive brute-force check of Proposition D1 (`K=1` CDF) and Corollary D1.2 (2nd moment), `n=2,\dots,9`, exact `Fraction` arithmetic; no randomness |
| `brute_k1.log` | its output — 0 mismatches |
| `brute_generalK.py` | exhaustive brute-force check of Lemma P2's identity (`K=1,2,3`) and of the `P_{nn}(n,K)`, `K=2,3` table, and the `P_{nn}(n,1)=\frac12+\frac1{6n}` pattern; exact arithmetic; no randomness |
| `brute_generalK.log` | its output — 0 mismatches, all table values match |
| `dnk_spotcheck.py` | independent spot-check of two `D(n,K)` table entries (Sec 7.1(d)) |
| `dnk_spotcheck.log` | its output — both match exactly |

No `.py` script from `distributional_bridge_attempt/` (the target front's
own directory) or from `k2_open_lemma/` (or any other prior front) was
opened, read, or imported at any point in this review, per the referee
mandate. No Monte Carlo / randomized code was used — every check above is
a finite, deterministic, exact-rational enumeration — so no seed from the
reserved range `20260876000`–`20260877000`, nor from this referee's own
range `20260877000+`, was needed or drawn.

No edits were made to `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, or `DISCOVERY_LAB_STATE.md`. No git commands were run.
