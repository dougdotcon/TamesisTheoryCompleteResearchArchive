# The full closed-form CDF of `M_n^{(3)}`: Proposição D3, extending Proposição D1 (K=1) to K=3

**Task ID:** `K3-FULL-CDF-ATTEMPT` (`DISC-DEC-106`, a redispatch of `DISC-DEC-093` —
the first attempt at this exact task, `k3_full_cdf_attempt_ABANDONED_STALLED/`
in this same parent directory, was abandoned mid-work by the orchestrating
session and never adversarially reviewed; this is a fresh attempt, not a
continuation — see §10 for what was and was not reused from it).

Pure combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1–4. **This is not a Millennium
Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260920000`–`20260920999` (this front's own, mandated by
the dispatch; grep-confirmed unused before first use — see §9). No edits
made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, or `PROOF_DEPENDENCY_MAP.md`. No `adversarial/`
subdirectory created here, no referee dispatched by this front (a separate
hostile referee is dispatched by the orchestrating session per the
mandate). No git command run. All work confined to the new subdirectory
`.../k3_joint_structural_attempt/k3_full_cdf_attempt/`.

---

## Executive summary (read first)

**The exact target, restated precisely (verbatim from the mandate).**
Extend Estágio 35's K=3 closure (which closed only the second moment,
`E[(M_n^{(3)})^2] \to 1/4`, via Proposição NN3) to the **full CDF** of
`M_n^{(3)}` — i.e. `P(M_n^{(3)} \le k/n)` in exact closed form for finite
`n` — in the style of Proposição D1 (Estágio 27, K=1:
`P(M_n^{(1)}\le k/n) = k(k+1)/n^2`), building on (not re-deriving) Estágio
35's Lemma 4 (Cycle-Predecessor Uniqueness) and its governing-source
reindexing corollary.

**What this document proves, unconditionally — all independently verified
against fresh from-scratch brute force and, for the main theorem, by a
complete symbolic derivation with zero numerical fitting in the final
proof:**

1. **The Full Cycle-Count Decomposition Theorem (§2, PROVED, new).** A
   genuine strengthening of Estágio 35's Lemma 4/5 from a *pairwise*
   statement (only `P(\text{two specific points both cyclic})`) to the
   **entire joint law** of `T := \#\{\text{cyclic points of }f\}` (so
   `M_n^{(3)}=T/n`):
   `\displaystyle T = O + \sum_{s\in S} V_s`,
   where `S\subseteq\{0,1,2\}` is the random set of "cyclic" reroute
   sources and, given `S`, the `V_s` (`s\in S`) are **mutually
   independent**, `V_s\sim\mathrm{Uniform}\{1,\dots,L_s\}`. `S`'s law is
   given by four exact closed-form formulas (Proposição S, §2.2) in terms
   of `p_i:=L_i/n`, `p_D:=O/n` alone.
2. **The exact closed-form conditional CDF (§3, PROVED).**
   `P(T\le k\mid L_0,L_1,L_2)` in fully explicit closed form (piecewise via
   elementary `min`/lattice-count formulas) — the K=3 analogue of
   Proposição D1's Lemma D1.0.
3. **Proposição D3 (§4, PROVED — the main result).** For every `n\ge3`
   and every integer `0\le k\le n-1`:
   ```
   P(M_n^{(3)} <= k/n) =
       k(k+1) [k^4 - 4k^3 - (3n^2-9n-5)k^2 + (3n^2-11n-2)k + (3n^4-12n^3+12n^2+2n)]
       -----------------------------------------------------------------------------
                              n^4 (n-1)(n-2)
   ```
   and `P(M_n^{(3)}\le x)=1` for `x\ge1` (`k=n`, trivially). Proved by a
   **complete, gap-free symbolic derivation** (`sympy`, exact summation,
   zero floating point anywhere) that sums the proved conditional CDF over
   the entire composition simplex, split into exactly three combinatorial
   regimes (`0\le k\le n-3`; `k=n-2`; `k=n-1`), each derived and verified
   independently — see `symbolic_derivation_full_cdf.py`, §4.2–4.4. **This
   is a genuine closed-form, uniform-in-`n`, single-formula CDF, matching
   Proposição D1's ambition exactly**, not merely a per-`n` numeric table.
4. **Corollaries (§5, all PROVED):** an elementary direct proof that
   `P(M_n^{(3)}=1)=6/n^3` (D3.1); exact symbolic recovery of the
   **already-proved** finite-`n` mean formula `\varphi_n^{(3)}` (Estágio 4,
   `THEOREM.md`) with **zero symbolic remainder** (D3.2) — a nontrivial
   identity a wrong CDF would essentially never pass; exact second- and
   third-moment formulas whose `n\to\infty` limits match the already-proved
   continuum values `1/4` and `16/105` (Estágio 18/17, D3.3–D3.4); a
   uniform convergence-rate bound `F_n^{(3)}(x)\to F_3(x)=1-(1-x^2)^3`
   (D3.5).
5. Independent verification: fresh true brute force of Definition 4 itself
   at `n=3,\ldots,8` (every `k`, `162` to `20{,}643{,}840` exact
   configurations, zero mismatches); an independent exact `O(n^3)`
   reference engine at `n=6,\ldots,40` (every `k`, `805` exact rational
   comparisons, zero mismatches); a large-`n` Monte Carlo triangulation
   (bonus, reserved seeds).

**Net verdict.** The mandate is **CLOSED**: a genuine, finite-`n`,
closed-form CDF for `M_n^{(3)}` — not just its second moment — has been
found and proved, in the exact style requested (matching Proposição D1's
single-formula ambition). No claim of progress on any Millennium Problem;
pure internal combinatorics on this archive's own random-permutation-with-
reroutes ensemble.

---

## 1. Reading discipline and setup

### 1.1 What was read

`THEOREM.md` §7.2 (Definition 4, the K=3 conditional model); the
Estágio 27 block (Proposição D0, Lemma R, **Proposição D1 and its full
proof** — read in full, its exact style is what this document reproduces
at K=3 — Lemma P2); the Estágio 35 block **in full** (the Reindexação por
Fonte-Governante, Lemma 4 "Cycle-Predecessor Uniqueness", Lemma 5,
Proposição NN3, Corollaries NN3.1–NN3.2, and its own honest §8 scoping out
the full CDF as future work); the Estágio 4 block (the already-proved
exact finite-`n` mean `\varphi_n^{(3)}`, used only as a cited consistency
target in §5.2, not re-derived); the Estágio 17 block (the already-proved
continuum density `f_{M_3}(x)=6x(1-x^2)^2` and its moments
`E[M_3]=16/35`, `E[M_3^2]=1/4`, `E[M_3^3]=16/105`, used only as cited
consistency targets in §5.3–5.4).

The **full prose** (not scripts, until noted in §10) of the predecessor
K=3 front's own `ATTEMPT.md` (`k3_joint_structural_attempt/ATTEMPT.md`) —
its notation, Lemma 4's statement and proof, Lemma 5's formulas, and its
own §8 diagnosis of exactly what the full CDF would need — was read in
full and is the direct starting point for §2 below, as the mandate
requires ("cite them and build on top", not rediscover from zero).

### 1.2 Notation (Estágio 35's, unchanged)

`\pi` a uniform random permutation of `[n]`. `K=3` reroute sources fixed
WLOG at `\{0,1,2\}` (Definition 4's exchangeability). Targets
`U_0,U_1,U_2` i.i.d. `\mathrm{Unif}([n])`, independent of `\pi`.
`f(i):=U_i` for `i\in\{0,1,2\}`, `f(i):=\pi(i)` otherwise.
`T:=\#\{\text{cyclic points of }f\}` (so `M_n^{(3)}=T/n`). By Lemma 1 /
the Governing-Source Reindexing corollary (Estágio 35 §2, **cited, not
re-derived**), `(L_0,L_1,L_2,O)` — `L_s` the length of the arc whose tail
is source `s`, `O:=n-L_0-L_1-L_2` the count of points on no marked arc —
is uniform over the `\binom n3` compositions of `n-3` into 4 nonnegative
parts, independent of topology `\sigma`.

---

## 2. The Full Cycle-Count Decomposition Theorem (PROVED, new)

### 2.1 Recap of Estágio 35's Lemma 4 (cited, not re-derived)

> **Lemma 4 (Cycle-Predecessor Uniqueness; Estágio 35, PROVED, cited
> verbatim).** Fix a destination assignment
> `\mathrm{dest}:\{0,1,2\}\to\{0,1,2,\mathrm{DEAD}\}` (which arc, or
> "outside", each `U_s` lands in). Say source `s` is **cyclic** iff
> iterating `\mathrm{dest}` from `s` returns to `s` before hitting DEAD.
> If `s` is cyclic, there is a **unique** `t` with `\mathrm{dest}(t)=s`
> and `t` itself cyclic — `\mathrm{pred}(s)` — and `ARC(s)`'s cyclic
> point-set is exactly `\{k,\dots,L_s\}`, `k` the landing position of
> `U_{\mathrm{pred}(s)}` within `ARC(s)`, independent of any other
> (necessarily inert) source also targeting `ARC(s)`.

Estágio 35 used this only to compute the pairwise quantity
`P_{nn}(n,3)=P(\text{two specific non-source points both cyclic})`
(Lemma 5, its Proposição NN3). It explicitly scoped the full count
distribution as future work (its §8.1: *"Lemma 4/Lemma 5 aqui... dão
apenas a lei conjunta par-a-par, não a distribuição de contagem
completa"*).

### 2.2 What is new here: the entire joint law, not a pair

If `s` is **not** cyclic, then (by the same argument used to prove Lemma
4: a genuine returning cycle through any position in `ARC(s)` would have
to pass through `s`'s own tail to continue, forcing `s` itself onto the
cycle) `ARC(s)` contributes **zero** cyclic points — the whole arc is a
non-cyclic tail. Combined with Lemma 4's positive case, and writing
`S\subseteq\{0,1,2\}` for the (random) set of cyclic sources:

> **Theorem (Full Cycle-Count Decomposition, PROVED, new).**
> `\displaystyle T = O + \sum_{s\in S} V_s`,
> where, given `S`, `V_s := L_s - k_s + 1` (`k_s` as in Lemma 4) for
> `s\in S`, and the `(V_s)_{s\in S}` are **mutually independent**,
> `V_s \sim \mathrm{Uniform}\{1,\dots,L_s\}`.

*Proof.* `V_s` is uniform on `\{1,\dots,L_s\}` because `k_s` is the
position, within `ARC(s)`, of `U_{\mathrm{pred}(s)}` conditioned on
landing there — and a coordinate uniform on `[n]`, conditioned on which
of 4 fixed regions it lands in, is uniform *within* that region,
independent of which region it was (standard fact about uniform random
variables). For `s\ne s'` both in `S`, `\mathrm{pred}(s)\ne\mathrm{pred}
(s')` (distinct arcs have distinct incoming cycle-edges, since
`\mathrm{pred}` is the inverse of `\mathrm{dest}` restricted to the
cyclic subset — a bijection there, Lemma 4's own proof), so `V_s,V_{s'}`
are determined by the landing positions of two *different* `U_t`'s, hence
independent (the `U_t` are i.i.d.). This joint-independence claim is
genuinely stronger than anything Lemma 4/5 asserted (they only ever
examined one or two positions at a time); it is what makes the *entire*
count `T`, not just a pairwise indicator, tractable. `\blacksquare`

> **Proposição S (the law of `S`; PROVED, new).** Write `p_i:=L_i/n`
> (`i=0,1,2`), `p_D:=O/n`. Then, for `u` the index not in `\{s,t\}`:
> ```
> P(S=empty)     = p_D
> P(S={s})       = p_s (p_s + p_D)                    (x3, symmetric)
> P(S={s,t})     = 2 p_s p_t (1 - p_u)                 (x3, symmetric)
> P(S={0,1,2})   = 6 p_0 p_1 p_2
> ```

*Proof.* Since `U_0,U_1,U_2` are i.i.d. `\mathrm{Unif}([n])` and the `n`
slots partition into `ARC(0),ARC(1),ARC(2)`, "outside" of sizes
`L_0,L_1,L_2,O`, the destinations `\mathrm{dest}(0),\mathrm{dest}(1),
\mathrm{dest}(2)` are **i.i.d.** categorical on `\{0,1,2,\mathrm{DEAD}\}`
with weights `(p_0,p_1,p_2,p_D)` (this is itself a new, elementary
observation not made explicit at K=2/K=3 before: `\mathrm{dest}(s)=t`
has probability `p_t` for **every** `s`, since it depends only on which
region `U_s` lands in). `S=\{0,1,2\}` (all cyclic) happens iff `\mathrm
{dest}` restricted to `\{0,1,2\}` is a bijection of `\{0,1,2\}` to
itself (a standard functional-graph fact: every node cyclic `\iff` the
map is a permutation) — summing the product `p_{\sigma(0)}p_{\sigma(1)}
p_{\sigma(2)}=p_0p_1p_2` over the `3!=6` permutations `\sigma` gives
`6p_0p_1p_2`. `S=\{s,t\}` (exactly two cyclic) arises from either a
2-cycle (`\mathrm{dest}(s)=t,\mathrm{dest}(t)=s`) or two independent
1-cycles/"homes" (`\mathrm{dest}(s)=s,\mathrm{dest}(t)=t`), in *both*
cases requiring the third node `u` to avoid `\mathrm{dest}(u)=u`
(probability `1-p_u`) — giving `p_sp_t(1-p_u)` twice, `2p_sp_t(1-p_u)`.
`S=\{s\}` requires `\mathrm{dest}(s)=s` **and** neither `t` nor `u`
cyclic; a short elementary computation (`P(d_t\ne t,d_u\ne u) -
P(d_t=u,d_u=t)` — excluding the 2-cycle case, which would make `S=\{s,t,
u\}` instead — simplifies to `1-p_t-p_u=p_s+p_D`) gives
`p_s(p_s+p_D)`. `S=\emptyset` is the complement, which a direct symbolic
sum over all `64` cases confirms equals exactly `p_D` (see script §2.3).
`\blacksquare`

### 2.3 Independent verification

`decomposition_theorem.py`:
1. **`P(S=A)` formulas** verified by an exact `sympy` symbolic sum over
   all `4^3=64` `(d_0,d_1,d_2)` combinations (the raw definition, no
   shortcut), for every subset `A` — zero symbolic discrepancy (all `8`
   cases, including a sanity check that the 8 probabilities sum to 1).
2. **The Decomposition Theorem given `(L_0,L_1,L_2)`** verified against a
   *position-level* reduced model built directly from Definition 4's
   prose (enumerating all `n^3` `(U_0,U_1,U_2)` choices explicitly, no
   shortcut of any kind) — exact pmf match at 6 spot-checked
   `(L_0,L_1,L_2,n)` configurations.
3. **The full (unconditional-in-`L`) decomposition** verified against
   fresh, from-scratch true brute force of Definition 4 itself (every one
   of `n!\cdot n^3` configurations, `n=6,7`) — exact pmf match.

```
$ python3 decomposition_theorem.py
...
ALL P(S=A) FORMULAS PROVED (exact symbolic match to raw 64-case definition).
...
Decomposition theorem CONFIRMED given L (exact match on every pmf value).
...
Full decomposition CONFIRMED against independent true brute force.

ALL CHECKS PASSED: the Full Cycle-Count Decomposition Theorem holds.
```
(full transcript: `decomposition_theorem.log`)

---

## 3. The exact closed-form conditional CDF (PROVED)

From §2, conditional on `(L_0,L_1,L_2)`, `T=O+\sum_{s\in A}V_s` for
whichever subset `A` is realized (probability `P(A|L)` from Proposição
S), and given `A`, `T-O` is the sum of `|A|` **independent** discrete
uniforms — an elementary, classically-solvable lattice-point-counting
problem. This gives, exactly:

```
P(T<=k | L) = P(empty|L)*[O<=k]
            + sum_s      P({s}|L)   * clip(k-O,0,L_s) / L_s
            + sum_{s<t}  P({s,t}|L) * paircount(L_s,L_t,k-O) / (L_s L_t)
            +            P({0,1,2}|L)*triplecount(L0,L1,L2,k-O) / (L0 L1 L2)
```
where `paircount(A,B,m):=\#\{(v,w):1\le v\le A,1\le w\le B,v+w\le m\}`,
`triplecount` the analogous 3-variable count — both standard, elementary,
proved-by-direct-summation lattice counts (`conditional_cdf.py`,
`pair_count_le`/`triple_count_le`, with proofs in their docstrings).

This is the K=3 analogue of Proposição D1's Lemma D1.0. Note the `L_s`
denominators cancel exactly against the `L_s` numerator factor already
present in each `P(A|L)` formula (e.g. `P(\{s\}|L)=L_s(L_s+O)/n^2`) — a
fact exploited heavily in §4 to make the final composition-simplex sum
tractable in closed form.

**Verification** (`conditional_cdf.py`): the conditional CDF closed form
is checked, at every `k=0,\dots,n`, against the position-level reduced
model of §2.3, at 4 spot-checked `(L,n)` — exact match throughout.

---

## 4. Proposição D3: the full unconditional closed-form CDF (PROVED)

### 4.1 Statement

> **Proposição D3 (K=3 exact finite-`n` CDF, PROVED).** For every `n\ge3`
> and every integer `0\le k\le n-1`:
> ```
> P(M_n^{(3)} <= k/n) =
>     k(k+1) [k^4 - 4k^3 - (3n^2-9n-5)k^2 + (3n^2-11n-2)k + (3n^4-12n^3+12n^2+2n)]
>     -----------------------------------------------------------------------------
>                            n^4 (n-1)(n-2)
> ```
> and `P(M_n^{(3)}\le x)=1` for `x\ge1` (`k\ge n`, trivially, since `T\le
> n` always). The `k(k+1)` factor structurally forces `P(T\le0)=0` and
> generalizes D1's own `k(k+1)/n^2` factor.

### 4.2 Derivation strategy

Write `O` (rather than `L_0,L_1,L_2` directly) as the outer summation
index, `m:=n-O=L_0+L_1+L_2`, `t:=k-O`. For fixed `O`, the number of
`(L_1,L_2)` pairs given `L_0` is `m-L_0-1` (a composition-counting fact),
which turns each of §3's 4 patterns' contributions, summed over the
entire composition simplex, into a **single or double** finite sum:

- **Empty pattern:** `S_0=\sum_{m=\max(3,n-k)}^n \frac{n-m}n\binom{m-1}2`
  (number of compositions of `m` into 3 positive parts is `\binom{m-1}2`).
- **Single-arc pattern:** using the multiplicity `(m-L_0-1)` and splitting
  the `\mathrm{clip}(t,0,L_0)` at `L_0=t`, a sum in `L_0` alone (then `O`).
- **Two-/three-arc patterns:** a "shift trick" — substitute
  `L_0'=L_0-v\ge0` etc. and use that the number of nonnegative solutions
  of `L_0'+L_1'+L_2'=m'` summing a fixed coordinate is a standard
  triangular-number identity — collapses `paircount`/`triplecount`,
  summed over the *entire* composition simplex, to a **single** sum over
  `s:=v+w` (resp. `v+w+u`), of `(s-1)\binom{m-s+1}2\cdot(\text{weight})`
  (resp. `\binom{s-1}2\binom{m-s+2}2`) — genuinely new identities, proved
  by direct `sympy` summation and cross-checked against independent
  direct numeric (`Fraction`) evaluation of the raw combinatorial sums at
  several `(n,k)` (§4.2 of `symbolic_derivation_full_cdf.py`; every check
  passes exactly).

This reduces the entire composition-simplex sum, for each pattern, to a
finite, exactly-summable 1- or 2-variable sum — done by `sp.summation`,
not curve-fitting, at every step.

### 4.3 The three combinatorial regimes

Because the `O`-sum's valid range is `0\le O\le\min(k,n-3)` (a composition
of `m=n-O` into 3 positive parts needs `m\ge3`), the derivation of §4.2
splits into exactly three regimes, **each derived and verified
independently** — not one derived and the others assumed by
extrapolation:

- **(i) `0\le k\le n-3`** ("generic"): `O` ranges `0..k`; the inner
  clip/pair/triple counts are genuinely truncated for every `O` in range.
- **(ii) `k=n-2`**: `O` ranges over *all* valid compositions (`0..n-3`,
  since `n-3\le n-2=k` always); substituting `k=n-2` makes `t=m-2`
  exactly, so the single-arc clip *never* truncates (saturates), while
  the pair/triple sums still do.
- **(iii) `k=n-1`**: same `O`-range; `t=m-1` now also saturates the
  two-arc case; only the three-arc sum is still genuinely truncated.

Each regime is a **separate, from-scratch `sp.summation` derivation**
(`symbolic_derivation_full_cdf.py`, three functions
`derive_regime_generic`/`_nm2`/`_nm1`), and each is shown, by an exact
`sp.simplify(derived - conjectured) == 0` symbolic identity (not a
numeric or floating-point check), to equal the **same single** rational
function stated in §4.1:

```
==============================================================================
REGIME (i): 0 <= k <= n-3
==============================================================================
Derived F(k) [regime i] = k*(k + 1)*(k**4 - 4*k**3 - 3*k**2*n**2 + 9*k**2*n
+ 5*k**2 + 3*k*n**2 - 11*k*n - 2*k + 3*n**4 - 12*n**3 + 12*n**2 + 2*n)/
(n**4*(n - 2)*(n - 1))
  Cross-checking S0..S3 (regime i) against direct numeric sums:
    n=10 k=3: S1 OK, S2 OK, S3 OK
    n=12 k=5: S1 OK, S2 OK, S3 OK
    n=9 k=2: S1 OK, S2 OK, S3 OK
    n=15 k=7: S1 OK, S2 OK, S3 OK
  All S0..S3 pieces independently confirmed.

F_derived(regime i) - F_conjectured = 0
REGIME (i): PROVED -- exact symbolic match.

==============================================================================
REGIME (ii): k = n-2
==============================================================================
Derived F(n-2) = (n**4 - 42*n + 72)/n**4
F_conjectured(n-2) = (n**4 - 42*n + 72)/n**4
difference = 0
REGIME (ii): PROVED -- exact symbolic match.

==============================================================================
REGIME (iii): k = n-1
==============================================================================
Derived F(n-1) = 1 - 6/n**3
F_conjectured(n-1) = 1 - 6/n**3
difference = 0
REGIME (iii): PROVED -- exact symbolic match.
(cross-check: 1-F(n-1) = 6/n^3, matching the elementary direct proof
 of Corollary D3.1.)

==============================================================================
ALL THREE REGIMES PROVED. Proposicao D3 holds for every n>=3,
0<=k<=n-1 -- a complete, gap-free symbolic derivation.
==============================================================================
```
(full transcript: `symbolic_derivation_full_cdf.log`; script:
`symbolic_derivation_full_cdf.py`)

**This is a complete proof**, covering every integer `k` from `0` to
`n-1` for every `n\ge3` — not an extrapolation from a few fitted points
and not a numerically-verified conjecture. (How the closed-form *target*
itself was first *found*, before this proof was written, is disclosed in
full honesty in §8 — exact-rational fitting from the proved conditional
CDF, exactly per this archive's established practice — but the content of
this section is the independent proof that the found formula is correct,
not a repetition of the fitting.)

### 4.4 Independent verification

`final_verification.py` runs three further, fully independent checks
(§5–7 below give the exact transcripts):

- **(A)** Proposição D3 vs. fresh true brute force of Definition 4 itself,
  `n=3,\ldots,8`, **every** `k` — `162` to `20{,}643{,}840` exact
  configurations per `n`, **zero mismatches**.
- **(B)** Proposição D3 vs. an independent exact `O(n^3)` reference engine
  (`conditional_cdf.full_cdf_exact`, itself built from the proved
  Decomposition Theorem, *not* from Proposição D3's own formula),
  `n=6,\ldots,40`, **every** `k` — `805` exact rational comparisons, zero
  mismatches.
- **(C)** exact symbolic recovery of the mean and moment limits (§5.2–5.4).

---

## 5. Corollaries (all PROVED)

### 5.1 Corollary D3.1 (elementary direct proof, `P(T=n)=6/n^3`)

`T=n` (full cyclicity, `M_n^{(3)}=1`) requires `S=\{0,1,2\}` **and**
`V_0=L_0,V_1=L_1,V_2=L_2` exactly (each landing at position 1 of its
arc). Given `S=\{0,1,2\}`, `P(V_0=L_0,V_1=L_1,V_2=L_2)=1/(L_0L_1L_2)`
(independence + uniformity, §2), so
`P(T=n\mid L) = P(S=\{0,1,2\}\mid L)/(L_0L_1L_2) = 6L_0L_1L_2/n^3 \cdot
1/(L_0L_1L_2) = 6/n^3` — **independent of `L`** — so averaging over the
composition simplex leaves it unchanged: `P(T=n)=6/n^3` exactly, for
every `n\ge3`. This matches Proposição D3's own `1-F(n-1)=6/n^3`
(confirmed by an independent `sympy` symbolic check, §4.3 regime (iii)).

### 5.2 Corollary D3.2 (mean recovery — a strong external consistency check)

Integrating Proposição D3 exactly (`\varphi_n^{(3)} = 1 -
\frac1n\sum_{k=0}^{n-1}F(k)`, standard identity for a nonnegative integer
r.v. bounded by `n`) reproduces, with **zero symbolic remainder**, the
mean formula already proved unconditionally in `THEOREM.md` Estágio 4
(2026-08-22, `ψ_n^{(3)}`/`φ_n^{(3)}` via the K-general transfer-matrix
method, cited here, **not** re-derived):

```
phi_n^(3) derived from D3    = 16/35 + 1/(14*n) + 11/(10*n**2) + 23/(35*n**3) + 6/(35*n**4)
phi_n^(3) cited (THEOREM.md) = 16/35 + 1/(14*n) + 11/(10*n**2) + 23/(35*n**3) + 6/(35*n**4)
difference = 0
```

This is a strong, independent, exact (not numeric) validation: a CDF that
was *not* exactly Proposição D3 would essentially never integrate to
reproduce a 5-term rational-in-`n` formula that was proved by an entirely
different method (the K-general transfer-matrix telescoping of Estágio
3–4) years (in-archive-time) before this front started.

### 5.3–5.4 Corollaries D3.3–D3.4 (second/third moment limits)

```
E[(M_n^(3))^2] derived from D3 = 1/4 + 9/(140n) + 167/(140n^2) + 21/(20n^3) + 71/(70n^4) + 12/(35n^5)
  limit as n->oo = 1/4   (matches Corollary NN3.1 / Estagio 18's continuum anchor E[M_3^2]=1/4)

E[(M_n^(3))^3] derived from D3 = 16/105 + 1/(20n) + 487/(420n^2) + 33/(28n^3) + 97/(60n^4) + 73/(70n^5) + 12/(35n^6)
  limit as n->oo = 16/105   (matches the already-proved continuum third moment, Estagio 17)
```

**Note on precision:** `E[(M_n^{(3)})^2]`'s exact finite-`n` rate here
(`9/140n+...`) is *not* identical to Estágio 35's `P_{nn}(n,3)` rate
(`19/70n`) — this is expected, not a discrepancy: `E[(M_n^{(3)})^2]` and
`P_{nn}(n,3)` are genuinely different quantities related by Lemma P2
(`\varphi_n^{(3)}/n` plus a `P_{nn}`-weighted term plus smaller
`P_{nr},P_{rr}`-weighted terms), and only their `n\to\infty` limits
(both `1/4`) are asserted to coincide.

### 5.5 Corollary D3.5 (uniform convergence rate)

Writing `x:=k/n`, `F_3(x):=1-(1-x^2)^3=3x^2-3x^4+x^6` for the already-
proved continuum CDF (from `f_{M_3}(x)=6x(1-x^2)^2`, Estágio 17, cited),
an exact `sympy` computation of `F_n^{(3)}(x)-F_3(x)` (substituting
`k=xn` directly into Proposição D3, exact cancellation, `sp.cancel`)
gives

```
F_n^{(3)}(x) - F_3(x) = N(n,x) / [n^2(n-1)(n-2)]
```

with `N` an explicit degree-`\le6`-in-`x`, degree-`\le3`-in-`n`
polynomial (`rate_corollary.py`). Each coefficient of `N(n,x)` (as a
polynomial in `n`) has a fixed sign for every `n\ge3` (checked, not
assumed); summing `|c_i(n)|` gives, exactly,
`|N(n,x)|\le 12n^3-14n^2+18n+4` for every `n\ge3,x\in[0,1]`. Combined
with the elementary bound `D(n)=n^2(n-1)(n-2)\ge5n^4/9` for `n\ge6`
(`(n-1)\ge5n/6`, `(n-2)\ge2n/3`), this gives, for every `n\ge6` and every
`x\in[0,1]`: `|F_n^{(3)}(x)-F_3(x)| \le 22/n` (not tight — a genuine,
rigorously provable, uniform `O(1/n)` bound, in the qualitative style of
D1's own Corollary D1.1, though with a cruder constant than D1's tight
`5/(4n)`; `rate_corollary.py` cross-checks the bound numerically at
`n=6,\ldots,2000`, worst observed `n\cdot|F_n^{(3)}-F_3|\approx0.71`, well
inside `22`).
The **leading-order** term of the `1/n` expansion is exactly
`g_1(x)/n=3x(x-1)^2(x+1)(x^2+1)/n`, with `\max_{x\in[0,1]}g_1(x)\approx
0.712` (`x\approx0.452`) — so the *asymptotically sharp* rate constant is
well below `1`, though a fully rigorous finite-`n` bound at that sharper
constant was not completed (the crude `62/n` bound is what is proved for
all `n`; the `0.712/n` figure is the honest asymptotic leading term,
disclosed as such, not proved as a uniform-in-`n` bound).

---

## 6. Numerical exploration (bonus, not a substitute for §2–5)

`monte_carlo_bonus.py`, reserved seeds `20260920001`–`20260920003`, direct
simulation of Definition 4's K=3 model (own random permutations and
reroute targets, **not** the reduced/decomposition model):

```
     n   trials      k     D3 pred     MC est     s.e.      z
   200   200000     50    0.178808   0.178850  0.00086   0.05
   200   200000    100    0.581603   0.580385  0.00110  -1.10
   200   200000    150    0.918138   0.917875  0.00061  -0.43
  2000    30000    500    0.176305   0.173733  0.00219  -1.18
  2000    30000   1000    0.578476   0.574633  0.00285  -1.35
  2000    30000   1500    0.916452   0.916633  0.00160   0.11
  5000    10000   1250    0.176137   0.175300  0.00380  -0.22
  5000    10000   2500    0.578266   0.578700  0.00494   0.09
  5000    10000   3750    0.916337   0.916400  0.00277   0.02
```
(full transcript: `monte_carlo_bonus.log`)
— all triangulation cells land within a couple of standard errors of the
exact Proposição D3 prediction, consistent, not itself proof (§2–5 are
the actual evidence; this is triangulation only, per lineage convention).

---

## 7. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `decomposition_theorem.py` / `.log` | the Full Cycle-Count Decomposition Theorem: `P(S=A)` formulas (symbolic proof, §2.2), the theorem itself, verified against a position-level reduced model and fresh true brute force |
| `conditional_cdf.py` / `.log` | the exact closed-form conditional CDF given `(L_0,L_1,L_2)` (§3), plus the slow-but-exact `O(n^3)` reference engine used in §4.4 check (B) |
| `symbolic_derivation_full_cdf.py` / `.log` | **the main proof**: the complete, three-regime symbolic derivation of Proposição D3 (§4.2–4.3) |
| `final_verification.py` / `.log` | checks (A)/(B)/(C) of §4.4/§5.2–5.4, all in one script |
| `true_bruteforce_full_cdf_k3.py` / `.log` | fresh, independent, fully-exhaustive Definition-4 ground truth, `n=3..8` |
| `rate_corollary.py` | Corollary D3.5's rate computation (§5.5) |
| `monte_carlo_bonus.py` / `.log` | large-`n` Monte Carlo triangulation, reserved seeds (§6) |

---

## 8. Honest disclosure: how the closed-form target was found

Per this archive's established practice (cf. Estágio 35's own §4.5), the
closed-form *statement* of Proposição D3 was first **found**, before
§4.2–4.3's proof was written, by exact (never floating-point) rational
curve-fitting from the already-*proved* conditional CDF of §3, as
follows: (1) compute `P(T\le k)` exactly (`Fraction`, `O(n^3)` exact
averaging over the composition simplex — §3's closed form, not raw
enumeration) for many `n` and *every* `k`; (2) observe, via exact
finite-difference computation, that the 6th finite difference in `k` is
constant for `k=0,\dots,n-2` and only breaks at the single point `k=n`
(consistent with `F` being a degree-`\le6` polynomial in `k` for
`0\le k\le n-1`); (3) Lagrange-interpolate that degree-6 polynomial
exactly from 7 points (`k=0,\dots,6`) at many `n=8,\dots,25`, and confirm
it predicts **every** held-out `k=7,\dots,n-1` exactly, for every `n`
tested; (4) factor out the `k(k+1)` common factor (found empirically,
`sympy.factor`); (5) fit the remaining coefficients (themselves clean
integers/polynomials in `n`) exactly from enough `n` and confirm on many
held-out `n`.

**This fitting step is explicitly NOT the proof.** §4.2–4.3 above is a
complete, independent, from-scratch symbolic *derivation* of the same
formula (three regimes, each summed by `sp.summation`, each cross-checked
against direct numeric evaluation of its own intermediate pieces before
being combined) — the derivation was carried out and verified to match
the fitted target with **zero symbolic remainder** in all three regimes,
which is what elevates this from "conjectured, matching an exact fit" to
"PROVED". The fitting-discovery process itself is disclosed here purely
for narrative honesty, exactly as this archive's convention requires
(Estágio 35 §4.5's own precedent).

---

## 9. Seeds

Reserved range: `20260920000`–`20260920999` (this front's own, mandated).
Grep-confirmed unused before this front's first use:
```
$ grep -rn "20260920001\|20260920002\|20260920003" 05_DISCOVERY_LAB/
```
returns only this front's own files. Only `monte_carlo_bonus.py` uses
randomness (`numpy.random.default_rng` via `numpy.random.SeedSequence`,
one explicit seed per cell, no shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `decomposition_theorem.py` | none (exact/exhaustive) | Decomposition Theorem + verification |
| `conditional_cdf.py` | none (exact) | conditional CDF closed form |
| `symbolic_derivation_full_cdf.py` | none (symbolic + exact numeric cross-checks) | main proof |
| `final_verification.py` | none (exact/exhaustive) | checks (A)/(B)/(C) |
| `true_bruteforce_full_cdf_k3.py` | none (exhaustive) | ground truth, `n=3..8` |
| `rate_corollary.py` | none (symbolic) | Corollary D3.5 |
| `monte_carlo_bonus.py` | `20260920001`, `20260920002`, `20260920003` | §6 large-`n` triangulation |

---

## 10. Relationship to the abandoned first attempt (`..._ABANDONED_STALLED/`)

The mandate permits reading the abandoned first attempt
(`k3_full_cdf_attempt_ABANDONED_STALLED/`, same parent directory) for
context, without assuming any of its content correct without independent
re-verification. It was read for orientation only, **after** this
front's own Decomposition Theorem (§2) and Proposição D3 (§4) had
already been independently derived and proved — no code, formula, or
intermediate result from it was copied into any script in this
directory. What it contains, for the record: a probability-generating-
function (PGF) approach (`pgf_attempt_k3*.py`, multi-stage, `sympy`),
which — per its own logs — did reach a final combined PGF expression
(`pgf_final_result_cancel.txt`, `pgf_final_result_raw.txt`) that
correctly reproduced `E[T],E[T^2],E[T^3]` against independent numeric
checks at `n=4,\ldots,20` (`crosscheck_moments_formula_vs_numeric.log`,
all `True`), but the attempt stopped there — no closed-form CDF (i.e. no
extraction of `P(T\le k)` from the PGF, and no proof of a `D1`-style
single formula) is present in its files, consistent with it having been
abandoned mid-work rather than deliberately concluded. This front took a
structurally different route (the Full Cycle-Count Decomposition of §2,
reducing the whole problem to closed-form CDF's of sums of independent
discrete uniforms, rather than manipulating a raw PGF in `z`), which
proved directly tractable for the CDF itself, as §4 shows.

> **Nota (2026-08-28, sessão orquestradora, pós-adversarial).** O
> referee hostil desta frente (`adversarial/REFEREE_REPORT.md`, achado
> #2, MODERADO) sinalizou, por metadados de arquivo apenas (sem ler
> conteúdo, por mandato), que o diretório abandonado contém
> `symbolic_D3_derivation.py`/`.log` e `P_D3_closed_form.txt`, cujos
> nomes pareciam contradizer esta seção. A sessão orquestradora leu
> esses arquivos diretamente: eles contêm **fórmulas de ponto único**
> `P(D=2)=P(T=n{-}2)` e `P(D=3)=P(T=n{-}3)`, derivadas por
> decomposição de casos à mão (não uma fórmula fechada em `k`, não o
> estilo D1) — confirmando que a §10 original permanece precisa (nenhum
> `P(T\le k)` genérico está presente). Adicionalmente, a sessão
> verificou ambas as fórmulas de ponto contra brute force fresco: a
> fórmula `P(D=2)` da tentativa abandonada está **correta** (`n=5,6,7`,
> correspondência exata com brute force e com a Proposição D3 desta
> frente); a fórmula `P(D=3)` está **incorreta**
> (`19n^2{-}105n{+}160` impresso, valor verdadeiro
> `19n^2{-}108n{+}160`, confirmado por brute force em `n=6,7,8` e pela
> própria Proposição D3 desta frente) — consistente com a tentativa
> anterior ter sido corretamente abandonada em meio ao trabalho, não
> silenciosamente completa e descartada. Isto não afeta nenhuma
> alegação desta `ATTEMPT.md`: nenhum arquivo da tentativa abandonada
> foi lido antes da derivação independente da Proposição D3 (§4), como
> já disclosurado acima.

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `P(S=A)` formulas (Proposição S) | **PROVED** (new) |
| 2 | Full Cycle-Count Decomposition Theorem | **PROVED** (new) |
| 3 | Exact conditional CDF given `(L_0,L_1,L_2)` | **PROVED** (new) |
| 4 | Proposição D3 (`K=3` exact finite-`n` CDF, all `k`) | **PROVED** (new — the main mandate) |
| 5 | Corollary D3.1 (`P(T=n)=6/n^3`) | **PROVED** (elementary direct proof) |
| 6 | Corollary D3.2 (exact mean recovery, `\varphi_n^{(3)}`) | **PROVED** (exact symbolic identity vs. cited Estágio 4 result) |
| 7 | Corollary D3.3 (`E[(M_n^{(3)})^2]\to1/4`) | **PROVED** |
| 8 | Corollary D3.4 (`E[(M_n^{(3)})^3]\to16/105`) | **PROVED** |
| 9 | Corollary D3.5 (uniform `O(1/n)` convergence, crude constant) | **PROVED** (bound not optimized) |
| 10 | Sharper asymptotic rate constant `\approx0.712/n` | asymptotic leading term only, **not** proved as a uniform finite-`n` bound (disclosed as such) |
| 11 | General-`K` full CDF | **OPEN**, not attempted (out of scope for this front; the Decomposition Theorem's method — governing-source i.i.d. destinations, cyclic/non-cyclic dichotomy — looks structurally generalizable, per the same kind of flag Estágio 35 left for K=3 itself, but this is an unverified hint, not a claim) |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No git command run. No file in the sibling
`general_k_joint_attempt/` directory (a different front) was touched.
All randomized verification used only the reserved seed range
`20260920000`–`20260920999`. Every claim above is labeled PROVED / OPEN
at the point of use; no claim is left as an unlabeled assertion. No claim
of progress on any Millennium Problem; this is pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.
