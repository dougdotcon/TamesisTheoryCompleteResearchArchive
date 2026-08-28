# The full closed-form CDF of `M_n^{(4)}`: Proposição D4, extending the D1/D2/D3 series (K=1,2,3) to K=4, citing the general-K machinery

**Task ID:** `K4-FULL-CDF-ATTEMPT`, wave 24 front (a), authorized by
`DISC-DEC-114` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`).
Pure combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1–4. **This is not a Millennium
Prize Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260926000`–`20260926999` (this front's own, mandated by
`DISC-DEC-114`; grep-confirmed unused before first use — see §9). No edits
made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created here (a separate
hostile referee will be dispatched later by the orchestrating session). No
`git` command run. All work confined to this new subdirectory
`.../general_k_joint_attempt/k4_full_cdf_attempt/`.

---

## Executive summary (read first)

**The exact target.** Extend the small-`K` full closed-form CDF series —
`P(M_n^{(K)}\le k/n)` as a single closed-form rational function of `n`,
valid for every integer `k` — from `K=0,1` (Proposição D1, Estágio 27),
`K=2` (Proposição D2, Estágio 42, one regime), `K=3` (Proposição D3,
Estágio 40, three regimes) to `K=4`, **citing** (not re-deriving) the
general-`K` Full Cycle-Count Decomposition Theorem and Proposição S
(Estágio 41, PROVED for every `K`).

**What this document proves, unconditionally — all independently verified
against fresh from-scratch brute force and, for the main theorem, by a
complete symbolic derivation with zero numerical fitting in the final
proof:**

1. **Proposição S and the Full Cycle-Count Decomposition Theorem,
   instantiated at K=4 (§2, CITED from Estágio 41, re-verified fresh
   here).** Sources fixed at `\{0,1,2,3\}`, arc lengths `L_0,\ldots,L_3`,
   `O:=n-L_0-L_1-L_2-L_3`. `T=O+\sum_{s\in S}V_s`, `(V_s)_{s\in S}`
   mutually independent given `S`, `V_s\sim\mathrm{Uniform}\{1,\ldots,
   L_s\}`, and, for every `A\subseteq\{0,1,2,3\}`:
   `P(S=A)=|A|!\prod_{a\in A}p_a\,(p_D+\sum_{a\in A}p_a)`
   (`p_i:=L_i/n`, `p_D:=O/n`) — this is Estágio 41's general-`K` theorem
   specialized to `K=4`, not re-derived, only re-verified (symbolic
   `5^4=625`-case enumeration, a position-level reduced model, and a
   fresh true brute force of Definition 4 itself, all independently
   written from scratch).
2. **The exact closed-form conditional CDF given `(L_0,\ldots,L_3)`**
   (§3, PROVED): the K=4 analogue of Proposições D1–D3's own conditional
   CDF machinery — a sum over all `16` subsets `A\subseteq\{0,1,2,3\}`
   of `P(A|L)` times an elementary `|A|`-fold discrete-uniform
   lattice-point count.
3. **Proposição D4 (§4, PROVED — the main result).** For every `n\ge4`
   and every integer `0\le k\le n-1`:
   ```
   P(M_n^{(4)} <= k/n) = k(k+1)*Q(n,k) / [n^5(n-1)(n-2)(n-3)]

   Q(n,k) = -k^6 + 9k^5 + (4n^2-18n-31)k^4 + (-16n^2+80n+51)k^3
            + (-6n^4+42n^3-55n^2-120n-40)k^2
            + (6n^4-50n^3+97n^2+70n+12)k
            + 4n^6-30n^5+74n^4-52n^3-30n^2-12n
   ```
   and `P(M_n^{(4)}\le x)=1` for `x\ge1` (`k=n`, trivially). **A single
   closed-form rational function, uniform in `n`, exactly in the style of
   Proposições D1–D3.** Proved by a complete, gap-free symbolic
   derivation (`sympy`, exact summation, zero floating point anywhere)
   that generalizes Estágio 40's K=3 "shift trick" one level further
   (K=4's patterns of size `<4` each leave `4-|A|` "free" remaining arcs
   that must themselves be composed — a genuinely new complication absent
   at K=3), split into **four** combinatorial regimes
   (`0\le k\le n-4`; `k=n-3`; `k=n-2`; `k=n-1` — one MORE regime than
   K=3's three, exactly matching the mandate's "could be more" hint),
   each derived and verified independently — see §4.2–4.3. All four
   regimes were then shown, by exact symbolic identity (not numeric
   check), to collapse onto the **same single formula** above — the
   K=3-style "genuine 3(or more)-regime proof, single final formula"
   outcome, not the K=2-style "trivially one regime" outcome.
4. **Corollaries (§6, all PROVED):** an elementary direct proof that
   `P(M_n^{(4)}=1)=24/n^4` (D4.1); a **complete new finite-`n` mean
   formula** `\varphi_n^{(4)}=128/315+23/(210n)+482/(315n^2)+99/(70n^3)+
   7/(9n^4)+4/(21n^5)` derived here from Proposição D4 (D4.2) — no such
   all-orders formula existed anywhere in `THEOREM.md` before this front
   (only the constant term `\varphi_4=128/315` and the leading rate
   `c_4=23/210` were on record, both of which this new formula reproduces
   **exactly**, a strong external consistency check); exact second/third
   moment formulas whose `n\to\infty` limits match `1/5` and `128/1155`
   (D4.3–D4.4, the latter self-derived, elementarily, from the cited
   general-K continuum density and independently cross-checked against
   `THEOREM.md`'s own stated `K=5` instance); a rigorously proved uniform
   convergence-rate bound `|F_n^{(4)}(x)-F_4(x)|\le7248/n` for all
   `n\ge6,x\in[0,1]` (D4.5), with the sharper asymptotic leading constant
   `\approx0.7087/n` disclosed honestly as not itself proved uniform.
5. **Independent verification:** fresh true brute force of Definition 4
   itself, `n=4,\ldots,8` (every `k`, `6{,}144` to `165{,}150{,}720` exact
   configurations, zero mismatches — `n=8` took `306.7`s); an independent
   exact `O(n^4)`-ish reference engine (built from Proposição S + the
   Decomposition Theorem via a genuinely different route — inclusion-
   exclusion lattice counting, not the shift-trick swap-of-summation-order
   used in the main proof), `n=4,\ldots,20` every `k` plus `n=22,25,28,30`
   every third `k` (`241` exact rational comparisons, zero mismatches); a
   large-`n` Monte Carlo triangulation (bonus, reserved seeds).

**Net verdict.** The mandate is **CLOSED**: a genuine, finite-`n`,
closed-form CDF for `M_n^{(4)}` — not just a moment — has been found and
proved, in the exact style of Proposições D1–D3, mechanically extending
the series one step further using the general-`K` machinery cited (not
re-derived) from Estágio 41. This is the fourth entry in the small-`K`
full-CDF series (`K=0,1,2,3,4` now all closed). No claim of progress on
any Millennium Problem; pure internal combinatorics on this archive's own
random-permutation-with-reroutes ensemble.

---

## 1. Reading discipline and notation

### 1.1 What was read

`THEOREM.md` Estágio 41 **in full** (the general-`K` Full Cycle-Count
Decomposition Theorem and Proposição S, PROVED for every `K` — the primary
citable building block for this front, used verbatim, not re-derived);
Estágio 40 **in full** (the K=3 case, Proposição D3, as the closest
structural/style template — its §4.2 "shift trick" for collapsing
pair/triple sums to a single sum over `s:=v+w` etc., and its §4.3
three-regime split, are the direct methodological ancestor of §4 below);
Estágio 4/6/7 (the K-general finite-`n` mean machinery: the Lema da
Redução A, `\varphi_n^{(K)}\to\varphi_K`, the exact leading rate
coefficient `c_K=[(K+2)\varphi_K-2]/4`, with the concrete worked example
`c_4=23/210` explicitly stated in Estágio 7's own text — used only as
cited cross-check targets in §6.2, not re-derived); Estágio 24 (the
general-`K` continuum density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`, PROVED for
every `K\ge1`, and `E[M_K^2]=1/(K+1)` — used as a cited base for the
elementary K=4 moment integrals of §6.3).

The K=2 front's own `ATTEMPT.md`
(`.../k2_joint_case_split_attempt/k2_full_cdf_attempt/ATTEMPT.md`), read
in full, for its "single regime, boundary condition holds automatically"
simplification pattern (in the event K=4 also simplified unexpectedly —
it did not; see §4.3). The general-K second-moment front's own
`ATTEMPT.md`
(`.../k3_joint_structural_attempt/general_k_joint_attempt/ATTEMPT.md`),
read in full, for its K-general model/notation conventions (sources
`\{0,\ldots,K-1\}`, targets `U_0,\ldots,U_{K-1}`, `x_s:=L_s/n`, the
`(K+1)^K` raw-table verification style — reused here without
modification). The general-K Decomposition front's own `ATTEMPT.md`
(`.../general_k_joint_attempt/general_k_decomposition_attempt/ATTEMPT.md`),
read in full, for Proposição S's precise general-`K` statement and proof
sketch (the key Lemma `R(B)=q_B`), and for its own honest §4/§5 disclosure
that it demonstrated the conditional-CDF machinery at concrete `K` only as
a small bonus, explicitly leaving the unconditional closed-form-in-`(n,K)`
CDF — and, a fortiori, its concrete `K=4` instance — untouched, which is
exactly the gap this front closes.

**No `.py` file from any of these fronts, or any ancestor, was read** —
every script in this directory is written completely fresh from the
mathematical prose cited above, per the mandate's hard constraint.

### 1.2 Notation (this lineage's own, unchanged)

`\pi` a uniform random permutation of `[n]`. `K=4` reroute sources fixed
WLOG at `\{0,1,2,3\}` (Definition 4's exchangeability). Targets
`U_0,U_1,U_2,U_3` i.i.d. `\mathrm{Unif}([n])`, independent of `\pi`.
`f(i):=U_i` for `i\in\{0,1,2,3\}`, `f(i):=\pi(i)` otherwise.
`T:=\#\{\text{cyclic points of }f\}` (so `M_n^{(4)}=T/n`). By the
Governing-Source Reindexing corollary (Estágio 35/38, general `K`,
**cited, not re-derived**): `(L_0,L_1,L_2,L_3,O)` — `L_s` the length of
the arc whose tail is source `s`, `O:=n-L_0-L_1-L_2-L_3` the count of
points on no marked arc — is uniform over the `\binom n4` compositions of
`n-4` into `5` nonnegative parts, independent of topology.

`p_i:=L_i/n` (`i=0,1,2,3`), `p_D:=O/n`. `S\subseteq\{0,1,2,3\}` the
(random) set of cyclic reroute sources (Estágio 40/41's own definition,
cited). `m:=L_0+L_1+L_2+L_3=n-O`. `t:=k-O`.

`clip(t,L):=\#\{v:1\le v\le L,v\le t\}=\max(0,\min(t,L))`.
`paircount(A,B,t):=\#\{(v,w):1\le v\le A,1\le w\le B,v+w\le t\}`.
`triplecount(A,B,C,t)`, `quadcount(A,B,C,D,t)`: the analogous 3- and
4-variable elementary lattice counts.

---

## 2. Proposição S and the Full Cycle-Count Decomposition Theorem, instantiated at K=4 (CITED, re-verified)

### 2.1 The cited general-K statements (Estágio 41, verbatim)

> **Theorem (Full Cycle-Count Decomposition, general `K`; PROVED, Estágio
> 41, cited verbatim).** `T=O+\sum_{s\in S}V_s`, where, given `S`, the
> `(V_s)_{s\in S}` are mutually independent, `V_s\sim\mathrm{Uniform}\{1,
> \ldots,L_s\}`.

> **Proposição S (general `K`; PROVED, Estágio 41, cited verbatim).** For
> every `K\ge0` and every `A\subseteq\{0,\ldots,K-1\}` (`m:=|A|`):
> `P(S=A)=m!\,(\prod_{a\in A}p_a)\,(p_D+\sum_{a\in A}p_a)`.

Estágio 41 proves these **for every `K`**, by a `K`-free argument (the
Key Lemma `R(B)=q_B`, proved by strong induction on `|B|` via an
exponential-integral identity, itself independent of `|B|`; and the Full
Cycle-Count Decomposition Theorem, proved by literally the same argument
as K=3 with `3` replaced by `K`). **Nothing in this section re-derives
either result** — §2.2 below only instantiates the general statements at
the concrete value `K=4` and independently re-verifies that instantiation
from scratch, exactly as the mandate requires ("cite, don't re-derive").

### 2.2 K=4 instantiation and independent re-verification

At `K=4`, Proposição S gives, for every `A\subseteq\{0,1,2,3\}`
(`16` subsets in total, one formula covering all of them by size
`|A|=0,1,2,3,4`):
```
P(S=empty)        = p_D
P(S={s})           = p_s(p_s+p_D)                          (x4)
P(S={s,t})          = 2 p_s p_t (p_D+p_s+p_t)                (x6)
P(S={s,t,u})         = 6 p_s p_t p_u (p_D+p_s+p_t+p_u)         (x4)
P(S={0,1,2,3})        = 24 p_0 p_1 p_2 p_3
```

**Independent verification** (`decomposition_theorem.py`, written
completely fresh, no code from any other front):

1. **Proposição S at K=4** verified by an exact `sympy` symbolic sum over
   all `5^4=625` `(dest_0,\ldots,dest_3)` combinations (the raw
   definition — each source's destination is one of `\{0,1,2,3,DEAD\}` —
   no shortcut), for every one of the `16` subsets `A` — zero symbolic
   discrepancy, plus confirmation that the `16` probabilities sum to `1`.
2. **The Decomposition Theorem given `L`** verified against a from-scratch
   **position-level reduced model** (explicit small functional graphs on
   the `L_0+L_1+L_2+L_3` arc positions, enumerating all `n^4`
   `(U_0,\ldots,U_3)` landing choices explicitly) at `5` spot-checked
   `(n,L)` configurations — exact joint pmf match on `(S,(V_s)_{s\in S})`
   in every case.
3. **The full (unconditional-in-`L`) decomposition** verified against
   fresh, from-scratch **true brute force of Definition 4 itself** (every
   one of `n!\cdot n^4` configurations, `n=5,6`) — exact pmf match on `T`.

```
$ python3 decomposition_theorem.py
...
ALL PROP-S CHECKS PASSED.
...
Decomposition Theorem (given L) CONFIRMED.
...
Full unconditional decomposition CONFIRMED against fresh true brute force.

ALL CHECKS PASSED: Proposicao S and the K=4 Full Cycle-Count
Decomposition Theorem hold (instantiated from the general-K citation,
Estagio 41, and independently re-verified here).
```
(full transcript: `decomposition_theorem.log`)

---

## 3. The exact closed-form conditional CDF given `(L_0,L_1,L_2,L_3)` (PROVED)

From §2, conditional on `L`, `T=O+\sum_{s\in A}V_s` for whichever subset
`A` is realized (probability `P(A|L)` from Proposição S), and given `A`,
`T-O` is the sum of `|A|` independent discrete uniforms — an elementary,
classically-solvable lattice-point-counting problem. This gives, exactly:

```
P(T<=k | L) = P(empty|L)*[O<=k]
            + sum_s      P({s}|L)     * clip(t,L_s) / L_s
            + sum_{s<t}  P({s,t}|L)   * paircount(L_s,L_t,t) / (L_s L_t)
            + sum_{s<t<u} P({s,t,u}|L) * triplecount(L_s,L_t,L_u,t) / (L_s L_t L_u)
            +            P({0,1,2,3}|L)*quadcount(L_0,L_1,L_2,L_3,t) / (L_0 L_1 L_2 L_3)
```
— `16` terms total (`1+4+6+4+1`), the K=4 analogue of Proposições
D1–D3's own conditional-CDF machinery. As at K=3, each `L_s` denominator
cancels exactly against the `L_s` numerator factor already present in
each `P(A|L)` formula (e.g. `P(\{s\}|L)=L_s(L_s+O)/n^2`), which is what
makes §4's composition-simplex sum tractable in closed form.

`paircount`, `triplecount`, and `quadcount` are computed here two
genuinely independent ways: (i) by direct nested-loop brute enumeration
(used inside `decomposition_theorem.py`'s own tests), and (ii) by a
closed-form **inclusion-exclusion** formula
(`count_le(bounds,t) := \sum_{S\subseteq bounds}(-1)^{|S|}W(t-d-\sum_{i\in
S}L_i,\,d)`, `W(N,d):=\binom{N+d}d` for `N\ge0`, else `0`; `d:=|bounds|`)
used inside `conditional_cdf.py`'s `full_cdf_exact` reference engine —
this second route is a genuinely different algebraic derivation from the
"shift trick" (swap-order-of-summation) method used in §4's main proof,
and serves as an independent cross-check there.

**Verification** (`conditional_cdf.py`): the conditional CDF closed form
is checked, at every `k=0,\ldots,n`, against §2's independent
position-level reduced model, at `4` spot-checked `(L,n)` — exact match
throughout (`conditional_cdf.log`). The inclusion-exclusion `count_le`
formula itself was separately verified against direct nested-loop
enumeration for `paircount` and `quadcount` at many `(A,B,t)`/`(A,B,C,D,t)`
combinations before being used (scratch testing, reproduced inline as the
`count_le` docstring's cited fact).

---

## 4. Proposição D4: the full unconditional closed-form CDF (PROVED)

### 4.1 Derivation strategy: generalizing the K=3 shift trick one level further

Write `m:=L_0+L_1+L_2+L_3`, `O:=n-m`, `t:=k-O`. The key new complication,
relative to K=3, is that **every pattern of size `|A|<4` has `4-|A|`
"free" remaining arcs** that must themselves be composed — at K=3, the
analogous patterns had at most `0` free remaining arcs (fixing `2` of `3`
sources determines the third exactly; fixing all `3` uses the whole
simplex). This means each K=4 pattern sum carries an **extra binomial
composition-count multiplicity** that K=3 never needed, and the
"single-index" shift trick of Estágio 40 must be generalized to swap the
lattice-count's own internal indices with a **second** layer of
composition-counting over the free remaining arcs. Concretely, for each
pattern (writing `r` for the sum of the lattice-count's internal indices,
e.g. `r=v+w` for the pair pattern):

- **Single-arc** (`4` symmetric copies): `S1(t,m,O):=\sum_{L_0=1}^{m-3}
  \binom{m-L_0-1}2(L_0+O)\,clip(t,L_0)` — `\binom{m-L_0-1}2` counts the
  compositions of the *other 3* arcs.
- **Pair** (`6` symmetric copies): swap-order + shift gives
  `PS(t,m,O):=\sum_{r=2}^t(r-1)\sum_{j=0}^{m-2-r}(j+1)(m-r-j-1)(O+r+j)` —
  the inner `j`-sum arises from composing the *other 2* arcs at a fixed
  total `r` of the pair's own internal lattice indices.
- **Triple** (`4` symmetric copies): `TS(t,m,O):=\sum_{r=3}^t\binom{r-1}2
  \sum_{s=0}^{m-1-r}\binom{s+2}2(O+r+s)` — the inner sum composes the
  *other 1* (forced) remaining arc.
- **Full (4-of-4, unique):** `QS(t,m):=\sum_{r=4}^{t}\binom{r-1}3
  \binom{m-r+3}3` — no free arcs remain; this is the direct K=4 analogue
  of Estágio 40's own `PairAgg`.

Each of `S1`, `PS`, `TS`, `QS` was derived symbolically (`sp.summation`,
zero floating point) and **independently verified against direct
nested-loop brute recomputation** of its own raw definition (no shortcut)
at many concrete `(m,O,t)` — `symbolic_derivation_full_cdf.py`, all
checks exact matches, including the boundary consistency of each
pattern's "genuinely truncated" (`_generic`) closed form against its
"fully saturated" (`_sat`) closed form at the threshold where the two
must coincide.

Per-`O` contribution to `\sum_L P(T\le k\mid L)` (summed over the
`\binom{m-1}3` compositions of `m` into `4` positive parts):
```
Contribution(O) = binom(m-1,3)*(O/n)*[O<=k]
                 + (4/n^2)  * S1(t,m,O)
                 + (12/n^3) * PS(t,m,O)
                 + (24/n^4) * TS(t,m,O)
                 + (24/n^4) * QS(t,m)
```
`F(k) = [\sum_{O=0}^{\min(k,n-4)}Contribution(O)] / \binom n4`.

### 4.2 The four combinatorial regimes

Because a pattern of size `4-c` (i.e. leaving `c` sources unaccounted-for
in the "cyclic" set — `c=0` for the single-arc pattern down to `c=3` for
the full pattern) has its own internal indices bounded by `m-c`, and
`t=k-O`, `m=n-O`, the condition "`t` genuinely truncates pattern `c`" is
`k<n-c` — **independent of `O`** (the `O` cancels), so each pattern is
**either non-saturated for every `O` in range, or saturated for every
`O` in range**, never a mix. This gives, by direct derivation (not
assumption):

- **(i) `0\le k\le n-4`** ("generic"): `O` ranges `0..k`; single, pair,
  triple, and full patterns are all genuinely truncated for every `O`.
- **(ii) `k=n-3`**: `O` ranges over *all* valid compositions (`0..n-4`,
  since `\min(k,n-4)=n-4` for `k\ge n-4`); the single-arc pattern becomes
  fully saturated (`clip` never truncates); pair, triple, full still
  genuinely truncated.
- **(iii) `k=n-2`**: `O` ranges `0..n-4`; single **and** pair now both
  fully saturated; triple, full still genuinely truncated.
- **(iv) `k=n-1`**: `O` ranges `0..n-4`; single, pair, **and** triple all
  fully saturated; only the full (4-of-4) pattern is still genuinely
  truncated — the direct K=4 analogue of Estágio 40's own regime (iii)
  finding ("only the three-arc sum is still genuinely truncated"), one
  layer deeper.

This is **one more regime than K=3's three**, precisely matching the
mandate's "could be more, derive it, don't assume exactly 3" instruction
— the extra regime is a direct, structural consequence of K=4 having one
more layer of pattern sizes (`0,1,2,3,4` vs. K=3's `0,1,2,3`) than K=3.

Each regime is a **separate, from-scratch `sp.summation` derivation**
(`assemble_regimes.py`, four functions `derive_regime_generic` /
`derive_regime_boundary` called with the appropriate saturated/generic
mix of `S1`/`PS`/`TS`/`QS` per regime), and each is shown, by an exact
`sp.simplify(\cdot)==0` symbolic identity (not numeric), to equal the
**same single** rational function stated in §4.4:

```
==============================================================================
REGIME (i): 0 <= k <= n-4
==============================================================================
  derived in 1.2s

==============================================================================
REGIME (ii): k = n-3
==============================================================================
  F(n-3) = (n**6 - n**5 - 984*n**2 + 5160*n - 7200)/(n**5*(n - 1))

==============================================================================
REGIME (iii): k = n-2
==============================================================================
  F(n-2) = (n**5 - 216*n + 480)/n**5

==============================================================================
REGIME (iv): k = n-1
==============================================================================
  F(n-1) = 1 - 24/n**4

==============================================================================
COLLAPSE CHECK: does F_generic(k), evaluated at k=n-3,n-2,n-1,
match F(n-3), F(n-2), F(n-1) derived independently above?
==============================================================================
  F_generic(n-3) - F(n-3) = 0
  F_generic(n-2) - F(n-2) = 0
  F_generic(n-1) - F(n-1) = 0
COLLAPSE CONFIRMED: a single formula (F_generic) covers ALL
0<=k<=n-1 -- this IS Proposicao D4.
```
(full transcript: `assemble_regimes.log`; scripts:
`symbolic_derivation_full_cdf.py`, `assemble_regimes.py`)

**This is a complete proof**, covering every integer `k` from `0` to
`n-1` for every `n\ge4` — regime (i)'s formula, derived assuming
`0\le k\le n-4`, is shown by exact symbolic identity to *also* equal the
independently-derived regime (ii)/(iii)/(iv) boundary values — exactly
the K=3-style outcome (a genuinely multi-regime *proof*, collapsing to
one *stated* formula), not the K=2-style outcome (trivially one regime
throughout).

### 4.3 Was the extra regime a coincidence, or genuinely required?

**Genuinely required, not an artifact of over-caution.** Within regime
(i) (`k\le n-4`), *all four* patterns are simultaneously non-saturated;
the moment `k` crosses `n-4` (i.e. `k=n-3`), the single-arc pattern's own
internal threshold (`t\ge m-3`) is crossed for *every* `O` simultaneously
(shown algebraically in §4.2, not just checked numerically), forcing a
structurally different (fully-saturated) closed form for that one
building block while pair/triple/full remain genuinely truncated. The
same happens again at `k=n-2` (pair) and `k=n-1` (triple). Each of these
three transitions is a **distinct** algebraic event (a different building
block saturating), which is exactly why three separate boundary regimes
— not one, not two — were needed in the *proof*, mirroring, one level
deeper, K=3's own two boundary transitions (`k=n-2`: single saturates;
`k=n-1`: pair saturates).

### 4.4 Statement

> **Proposição D4 (K=4 exact finite-`n` CDF, PROVED).** For every `n\ge4`
> and every integer `0\le k\le n-1`:
> ```
> P(M_n^{(4)} <= k/n) = k(k+1)*Q(n,k) / [n^5(n-1)(n-2)(n-3)]
>
> Q(n,k) = -k^6 + 9k^5 + (4n^2-18n-31)k^4 + (-16n^2+80n+51)k^3
>          + (-6n^4+42n^3-55n^2-120n-40)k^2
>          + (6n^4-50n^3+97n^2+70n+12)k
>          + 4n^6-30n^5+74n^4-52n^3-30n^2-12n
> ```
> and `P(M_n^{(4)}\le x)=1` for `x\ge1` (`k\ge n`, trivially, since `T\le
> n` always). The `k(k+1)` factor structurally forces `P(T\le0)=0`,
> matching D1's, D2's, and D3's own `k(k+1)` factor (checked directly:
> `Q(n,k)` is exactly divisible by neither `k` nor `k+1` alone, but the
> full numerator is).

The denominator `n^5(n-1)(n-2)(n-3)` continues the exact pattern
`n^{K+1}\prod_{j=1}^{K-1}(n-j)` visible in D2 (`n^3(n-1)`) and D3
(`n^4(n-1)(n-2)`).

### 4.5 Independent verification

- **(A)** Proposição D4 vs. fresh true brute force of Definition 4 itself,
  `n=4,\ldots,8`, **every** `k` — `6{,}144` to `165{,}150{,}720` exact
  configurations per `n`, **zero mismatches**.
- **(B)** Proposição D4 vs. an independent exact `O(n^4)`-ish reference
  engine (`conditional_cdf.full_cdf_exact`, built from Proposição S + the
  Decomposition Theorem via inclusion-exclusion counting — genuinely
  different from the shift-trick route of §4.1–4.2), `n=4,\ldots,20`
  every `k`, plus `n=22,25,28,30` every third `k` — `241` exact rational
  comparisons, zero mismatches.
- **(C)** exact symbolic recovery of the mean and moment limits (§6).

See §7 for the full transcripts.

---

## 5. Why a fourth regime, structurally (a note on the mandate's own question)

The mandate explicitly asked to determine, by derivation not assumption,
how many combinatorial regimes K=4 needs. §4.2–4.3 answer this precisely:
**four**, one more than K=3's three, because K=4 has one more "layer" of
pattern sizes (`|A|=0,1,2,3,4` vs. K=3's `|A|=0,1,2,3`) and each
non-full pattern saturates at a *distinct* value of `k` (`n-3`, `n-2`,
`n-1` respectively for the single/pair/triple patterns), each transition
being algebraically forced (not a matter of proof-writing convenience) by
exactly where that pattern's own internal lattice-count index range
exhausts itself: for a pattern of size `a` (`1\le a\le K-1`), leaving
`K-a` arcs free, saturation occurs exactly at `k=n-(K-a)`, giving `K-1`
distinct boundary thresholds `n-(K-1),\ldots,n-1`, plus the generic
region `k\le n-K` — **`K` regimes in total**, by this counting.

**Checking this count against K=1,2,3 (reported honestly, with the
counting convention made explicit — see §8.1 for a caveat):** K=1 has no
non-full pattern at all (`|A|=0` empty, `|A|=1` is already the full set),
so `0` boundary thresholds, `1` regime total (trivially — Proposição D1
needs no case split at all). K=3 (Estágio 40) used exactly `3` (generic
`k\le n-3`; `k=n-2` where single saturates; `k=n-1` where pair saturates)
— matches `K=3`. K=4 (this front) used exactly `4` — matches. **K=2 is
the case requiring a careful counting-convention caveat, not a genuine
contradiction:** its own `ATTEMPT.md` §4.2 explicitly derives **two**
separate closed forms via `sp.summation` — "regime (i) `0\le k\le n-2`"
and "regime (ii) `k=n-1`" — matching this front's `K` prediction (`2`
total for `K=2`) at the *derivation-step* level; that document's own
executive summary nonetheless *describes* this as "one regime," using
"regime" there to mean "pieces in the final **stated** formula" (which is
`1` for every `K` in this whole series, K=1,\ldots,4 — the derivation
always collapses to a single final closed form, per the collapse checks
of §4.2 above and of Estágios 40/42 themselves). Read this way — "regime"
= number of separate `sp.summation` derivations the *proof* needs, not
the number of pieces in the *final stated formula* (which is always `1`)
— the count is consistently `K` across `K=1,2,3,4`, with **no**
discrepancy; the apparent K=2 anomaly is a wording difference between
that front's executive summary and its own methodology section, not a
different mathematical fact. This `K`-regimes-in-the-proof pattern is
reported here as a modest, honestly-hedged observation from **four data
points**, not a proved general-`K` claim — see §8.1.

---

## 6. Corollaries (all PROVED unless noted)

### 6.1 Corollary D4.1 (elementary direct proof, `P(T=n)=24/n^4`)

`T=n` (full cyclicity, `M_n^{(4)}=1`) requires `S=\{0,1,2,3\}` **and**
`V_s=L_s` for every `s` exactly (each landing at position `1` of its own
arc). Given `S=\{0,1,2,3\}`, `P(V_0=L_0,\ldots,V_3=L_3)=1/(L_0L_1L_2L_3)`
(independence + uniformity, §2), so `P(T=n\mid L) =
P(S=\{0,1,2,3\}\mid L)/(L_0L_1L_2L_3) = 24L_0L_1L_2L_3/n^4\cdot
1/(L_0L_1L_2L_3) = 24/n^4` — **independent of `L`** — so averaging over
the composition simplex leaves it unchanged: `P(T=n)=24/n^4` exactly, for
every `n\ge4`. Matches Proposição D4's own `1-F(n-1)=24/n^4` (confirmed
by an exact symbolic check, §4.2 regime (iv)). This continues the exact
`K!/n^K` pattern: `2/n^2` (K=2), `6/n^3` (K=3), `24/n^4` (K=4).

### 6.2 Corollary D4.2 (a NEW complete finite-`n` mean formula — a strong external consistency check)

Integrating Proposição D4 exactly (`\varphi_n^{(4)} = 1 -
\frac1n\sum_{k=0}^{n-1}F(k)`, standard identity for a nonnegative integer
r.v. bounded by `n`) gives:

```
$ python3 final_verification.py   (check C)
phi_n^(4) [D4.2, NEW full finite-n formula, derived from D4] =
  128/315 + 23/(210*n) + 482/(315*n**2) + 99/(70*n**3) + 7/(9*n**4) + 4/(21*n**5)
```

**This is a genuinely new result**: unlike K=3 (Estágio 4's Markov-chain
method gave the *full* finite-`n` formula `\varphi_n^{(3)}`, which
Estágio 40 could then recover exactly with zero remainder), `THEOREM.md`
never records a full-orders finite-`n` `\varphi_n^{(4)}` formula anywhere
— only its two "anchor" values: the continuum limit `\varphi_4=128/315`
(Estágio 4, from the Wallis-integral formula, and Estágio 24's general-`K`
continuum theorem) and the leading `1/n` rate coefficient
`c_4=23/210` (Estágio 7's own explicitly-stated "worked example",
`c_K=[(K+2)\varphi_K-2]/4`). Both are cited targets, **not
re-derived** — they are checked, exactly:

```
constant term (n->oo limit) = 128/315   (cited target: 128/315, Estagio 4/24)
coefficient of 1/n          = 23/210    (cited target: 23/210, Estagio 6/7)
MATCH
```

**This is a strong, independent, exact (not numeric) validation**: a
wrong CDF would essentially never integrate to reproduce *two* separately-
cited constants (the continuum limit **and** the leading rate, proved by
an entirely different method — the K-general transfer-matrix/Gronwall
argument of Estágios 4/6/7 — long before this front started) exactly.
**Honest scoping**: this is *not* a "zero-symbolic-remainder recovery of
an already-proved full polynomial" in the sense Estágio 40 achieved for
K=3 (§6 of that front) — no such full K=4 polynomial existed to compare
against. It *is* an exact match of the two invariants (constant term,
leading rate) that *were* on record, plus a new all-orders formula
(the `1/n^2,\ldots,1/n^5` terms) that had never been computed before by
any method — offered here as new content, honestly labeled as such, not
as a "recovery."

### 6.3 Corollaries D4.3–D4.4 (second/third moment limits)

```
E[(M_n^(4))^2] [D4.3] = 1/5 + 19/(210n) + 3/(2n^2) + 61/(30n^3) + 199/(70n^4) + 209/(105n^5) + 4/(7n^6)
  limit as n->oo = 1/5   (cited target: 1/5 = 1/(K+1), Estagio 24, PROVED for every K)

E[(M_n^(4))^3] [D4.4] = 128/1155 + 5/(77n) + 9113/(6930n^2) + 4813/(2310n^3) + 5659/(1386n^4) + 719/(154n^5) + 1049/(315n^6) + 236/(231n^7)
  limit as n->oo = 128/1155
```

> **Correção (2026-08-28, achado F1 do referee hostil dedicado,
> severidade MODERADA):** a frase original abaixo — "`128/1155` is
> **not** separately stated anywhere in `THEOREM.md` for K=4" — é
> **falsa**. `THEOREM.md`, Estágio 20 (linhas 3639–3641), já declara
> exatamente `E[M_4^3]=128/1155` como subproduto de sua própria
> derivação de `K=4` ("Subprodutos: `E[M_4]=128/315=\varphi_4`,
> `E[M_4^2]=1/5`..., `E[M_4^3]=128/1155`"). A lista de leitura desta
> frente (§ "O que li antes de escrever") cita o Estágio 24 mas
> omite o Estágio 20 — daí o erro de enquadramento de novidade. Isto
> **não afeta a correção matemática** de D4.4 nem da checagem cruzada
> K=5 (ambas independentemente reconfirmadas pelo referee via uma
> identidade diferente) — apenas a alegação de que o valor era
> inédito está errada; o valor em si está correto e agora tem duas
> derivações independentes concordantes (Estágio 20 e esta frente).

`128/1155` is derived here directly, by elementary calculus
(`continuum_moments_k4.py`), from the **cited** general-`K` continuum
density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` (Estágio 24, PROVED for every
`K\ge1`): `E[M_4^3]=\int_0^1x^3\cdot8x(1-x^2)^3\,dx=128/1155`. As a
self-consistency cross-check on this elementary-integration route (not a
new theorem, just calculus), the same script reproduces `THEOREM.md`
Estágio 24's own explicitly-stated `K=5` instance,
`E[M_5^3]=256/3003`, **exactly**, confirming the general closed-form
moment expression `E[M_K^3]=K!\,2^K/\prod_{j=0}^{K-1}(2j+5)` (derived
here, elementary, from the Beta-function form of the cited density) is
correct, not merely internally self-consistent.

**Note on precision (matching Estágios 40/`k2_full_cdf_attempt`'s own
remark):** `E[(M_n^{(4)})^2]`'s exact finite-`n` rate (`19/210` at
`1/n`) is a *whole-count* second moment, a genuinely different
finite-`n` quantity from any pairwise `P_{nn}(n,4)`-style statistic
(Proposition NN4, `general_k_joint_attempt` §6.1, rate `187/630`) —
related only in the `n\to\infty` limit (both `\to1/5`), exactly as at
K=2/K=3.

### 6.4 Corollary D4.5 (uniform convergence rate)

Writing `x:=k/n`, `F_4(x):=1-(1-x^2)^4` for the already-proved continuum
CDF (from `f_{M_4}(x)=8x(1-x^2)^3`, Estágio 24, cited), an exact `sympy`
computation of `F_n^{(4)}(x)-F_4(x)` (substituting `k=xn` directly into
Proposição D4, exact cancellation via `sp.cancel`) gives

```
F_n^(4)(x) - F_4(x) = N(n,x) / [n^3(n-1)(n-2)(n-3)]
```

with `N` an explicit degree-`\le8`-in-`x`, degree-`\le5`-in-`n`
polynomial (`rate_corollary.py`). Bounding each `x`-coefficient of `N`
(as a polynomial in `n`) by the sum of its own coefficients' absolute
values (valid since `|x|\le1`), and using the elementary bound
`n^3(n-1)(n-2)(n-3)\ge n^6/8` for `n\ge6`:

> **Corollary D4.5 (PROVED).** For every `n\ge6` and every `x\in[0,1]`:
> `|F_n^{(4)}(x)-F_4(x)| \le 7248/n`
> — a genuine, rigorously provable, uniform `O(1/n)` bound, in the style
> of D1's/D2's/D3's own such bounds (crude, not optimized, honestly
> disclosed as such).

`rate_corollary.py` additionally cross-checks the bound numerically:
`n=6,\ldots,3000`, dense `x`-grid, worst observed ratio
`|gap|/(7248/n)\approx0.0001` — comfortably inside the proved bound (the
bound is deliberately loose, not tight). **The leading-order term** of
the `1/n` expansion is exactly
`g_1(x)/n=(-6x^8+8x^7+6x^6-12x^5+6x^4-6x^2+4x)/n`, with
`\max_{x\in[0,1]}g_1(x)\approx0.7087` (at `x\approx0.3699`) — consistent
in magnitude with D2's `\approx0.7107` and D3's `\approx0.712`, a nice
cross-family sanity pattern — so the *asymptotically sharp* rate constant
is well below `1`, though a fully rigorous finite-`n` bound at that
sharper constant was **not** completed (disclosed honestly, matching
D2.5/D3.5's own honest gap).

---

## 7. Independent verification: full transcripts

### 7.1 (A) True brute force of Definition 4 itself, `n=4,\ldots,8`

Fresh, from-scratch, fully-exhaustive enumeration
(`true_bruteforce_full_cdf_k4.py`): every one of `n!\cdot n^4`
`(\pi,U_0,U_1,U_2,U_3)` configurations, exact `Fraction` counting via an
`O(n)`-amortized iterative pointer-chasing cyclic-point detector (not the
naive `O(n^2)` restart-per-point method), **no code read from any other
front**.

| `n` | configs | wall time | matches Proposição D4 (every `k`) |
|---|---|---|---|
| 4 | 6,144 | <0.1s | ✓ |
| 5 | 75,000 | 0.1s | ✓ |
| 6 | 933,120 | 1.5s | ✓ |
| 7 | 12,101,040 | 21.6s | ✓ |
| 8 | 165,150,720 | 306.7s | ✓ |

`30` exact rational comparisons across `n=4,\ldots,8` (every `k`),
**zero mismatches** (`final_verification.py` check (A); raw per-`n`
transcripts embedded in `bf_8.log` and the `bf_pmf_{4,5,6,7,8}.pkl`
records). `n=8` (`165.15` million exact configurations) matches the
depth of the largest true brute-force check anywhere in this lineage's
`K\ge4` regime (`general_k_joint_attempt`'s own `K=4,n=8` brute force),
consistent with the mandate's "likely reaches n=7 or n=8" expectation.

### 7.2 (B) Independent `O(n^4)`-ish reference engine, `n=4,\ldots,30`

`conditional_cdf.py`'s `full_cdf_exact(n,k)` — built directly from §2–3's
proved Decomposition Theorem + Proposição S + conditional CDF machinery,
via inclusion-exclusion lattice counting (a route genuinely independent
of the shift-trick derivation of §4), **not using Proposição D4's own
closed form at any point** — checked against Proposição D4:

```
(B) Proposicao D4 vs independent O(n^4) reference engine
  n=4..20: every k checked
  n=22,25,28,30: every 3rd k checked
  Total exact comparisons: 241, mismatches: 0   (elapsed 227.6s)
```
(full transcript: `final_verification.log`)

### 7.3 (C) Exact symbolic recovery of mean/moment limits

See §6.2–6.3 above for the full output; reproduced verbatim from
`final_verification.py`'s check (C):
```
phi_n^(4) constant term = 128/315 (MATCH), coefficient of 1/n = 23/210 (MATCH)
E[(M_n^(4))^2] limit = 1/5 (MATCH)
E[(M_n^(4))^3] limit = 128/1155 (MATCH)
```

### 7.4 (D) Bonus large-`n` Monte Carlo triangulation

`monte_carlo_bonus.py`, reserved seeds `20260926001`–`20260926006`,
direct simulation of Definition 4's actual K=4 model (own random
permutation via `numpy`'s Fisher–Yates `rng.permutation`, own i.i.d.
targets, **not** the reduced/decomposition model):

```
     n   trials      k    D4 pred     MC est     s.e.       z
   100   200000     25   0.233756   0.232990  0.00095   -0.81
   100   200000     50   0.689662   0.690005  0.00103    0.33
   100   200000     75   0.965285   0.964720  0.00041   -1.37
   500    30000    125   0.228795   0.228900  0.00243    0.04
   500    30000    250   0.684849   0.681300  0.00269   -1.32
   500    30000    375   0.963778   0.964367  0.00107    0.55
```
(full transcript: `monte_carlo_bonus.log`) — all six cells land within
`\approx1.4\sigma` of the exact Proposição D4 prediction — consistent,
not itself proof, per lineage convention.

---

## 8. What did NOT close, precisely (honest, as mandated)

- **General-`K` closed-form-in-`(n,K)` CDF (`K\ge5`, or a `K`-uniform
  single formula):** not attempted here (out of scope for a
  `K=4`-specific front). This front adds a fifth concrete data point
  (`K=0,1,2,3,4`) to the small-`K` series, but the harder question of a
  single formula valid for symbolic `K` remains exactly as open as
  `general_k_decomposition_attempt` left it (its own §5.1) — this
  front's own §5's "regime count vs. `K`" observation is a genuine
  *hint* about how the regime structure might scale with `K`, but it is
  explicitly flagged there as an **unverified pattern** (with a named
  discrepancy at `K=2` — see §8.1 immediately below), not a claim.
- **§8.1 The "`K` regimes" observation, and its counting-convention
  caveat, precisely stated.** §5 above reports a `K`-regimes-in-the-proof
  pattern checked at `K=1,2,3,4` (`1,2,3,4` regimes respectively, once
  "regime" is read as "a separate `sp.summation` derivation the proof
  needed," matching what the K=2 front's own §4.2 methodology actually
  did, even though that front's executive summary describes its own
  result with the word "regime" used in a different sense — "pieces in
  the final stated formula," which is `1` for every `K` studied so far,
  this front's K=4 included). **This is reported strictly as an
  observation from four data points, not a proved general-`K` claim** —
  no attempt was made here to prove that the pattern continues at `K=5`
  or beyond, nor to rule out that some future `K` breaks it in a way not
  visible from `K\le4` (e.g. two saturation thresholds coinciding, the
  way `K=2`'s single threshold happens to coincide with the domain's own
  upper boundary `k=n-1`, which is itself worth noting as a structurally
  real, non-generic coincidence rather than assuming it never recurs).
- **A sharper, provably-uniform rate constant** for Corollary D4.5 (the
  asymptotic leading constant `\approx0.7087/n` is computed but not
  proved as a uniform finite-`n` bound — only the crude `7248/n` is
  proved uniform, matching D2.5's/D3.5's own honest disclosure of the
  same gap).
- **No claim** that Proposição D4's derivation was harder or easier to
  find than K=3's — it required genuinely more machinery (one extra
  regime, one extra layer of "free remaining arcs" per pattern), exactly
  as the mandate anticipated might happen, though the shift-trick method
  itself, once generalized, was entirely mechanical (no new proof idea
  beyond the double-composition-counting insight of §4.1) — consistent
  with the mandate's own framing that citing the general-K machinery
  "should make this front's job substantially more mechanical."
- **No claim of any kind about a Millennium Problem.**

---

## 9. Seeds

Reserved range: `20260926000`–`20260926999` (this front's own, mandated
by `DISC-DEC-114`). Grep-confirmed unused before this front's first use:
```
$ grep -rn "20260926" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:7510:      20260926000-20260926999.
```
— only the governance reservation line, confirmed **before** this
front's own files existed (re-confirmed after: only that line and this
front's own files reference the range). Only `monte_carlo_bonus.py` uses
randomness (`numpy.random.default_rng`, one explicit seed per cell, no
shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `decomposition_theorem.py` | none (exact/exhaustive/symbolic) | Proposição S + Decomposition Theorem instantiated at K=4, §2 |
| `conditional_cdf.py` | none (exact) | conditional CDF closed form, §3; `O(n^4)`-ish reference engine |
| `symbolic_derivation_full_cdf.py` | none (symbolic + exact numeric cross-checks) | building blocks `S1`/`PS`/`TS`/`QS`, §4.1 |
| `assemble_regimes.py` | none (symbolic) | main proof: four-regime derivation + collapse check, §4.2–4.4 |
| `final_verification.py` | none (exact/exhaustive) | checks (A)/(B)/(C), §4.5/§6/§7 |
| `true_bruteforce_full_cdf_k4.py` | none (exhaustive) | ground truth, `n=4..8` |
| `continuum_moments_k4.py` | none (symbolic) | §6.3's elementary moment derivation + K=5 cross-check |
| `rate_corollary.py` | none (symbolic + deterministic numeric scan) | Corollary D4.5, §6.4 |
| `monte_carlo_bonus.py` | `20260926001`–`20260926006` | §7.4 large-`n` triangulation |

---

## 10. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `decomposition_theorem.py` / `.log` | Proposição S + the Full Cycle-Count Decomposition Theorem, instantiated at K=4 and independently re-verified (§2) |
| `conditional_cdf.py` / `.log` | the exact closed-form conditional CDF given `L` (§3), plus the slow-but-exact `O(n^4)`-ish `full_cdf_exact` reference engine (inclusion-exclusion route) used in §7.2 |
| `symbolic_derivation_full_cdf.py` / `.log` | the `S1`/`PS`/`TS`/`QS` building blocks (§4.1), each derived via the generalized shift trick and cross-checked against direct nested-loop recomputation |
| `assemble_regimes.py` / `assemble_regimes.log` | **the main proof**: the four-regime derivation of Proposição D4 and the exact symbolic collapse check (§4.2–4.4) |
| `final_verification.py` / `.log` | checks (A)/(B)/(C) of §4.5/§6/§7, all in one script |
| `true_bruteforce_full_cdf_k4.py` | fresh, independent, fully-exhaustive Definition-4 ground truth, `n=4..8`; also writes `bf_pmf_N.pkl` |
| `continuum_moments_k4.py` / `.log` | §6.3's elementary continuum-moment derivation from the cited general-K density, plus the K=5 self-consistency cross-check |
| `rate_corollary.py` / `.log` | Corollary D4.5's rate computation (§6.4) |
| `monte_carlo_bonus.py` / `.log` | large-`n` Monte Carlo triangulation, reserved seeds (§7.4) |
| `building_blocks.pkl`, `F_generic.pkl`, `F_ii.pkl`, `F_iii.pkl`, `F_iv.pkl`, `D4_clean.pkl`, `mean_moments.pkl`, `rate_bound_const.pkl`, `bf_pmf_{4,5,6,7,8}.pkl` | intermediate exact-symbolic/exact-rational data, saved for reproducibility (all regenerable from the scripts above) |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Proposição S at K=4 (instantiated from Estágio 41's general-`K` citation) | **PROVED** (cited + independently re-verified, §2) |
| 2 | Full Cycle-Count Decomposition Theorem at K=4 (instantiated from Estágio 41) | **PROVED** (cited + independently re-verified, §2) |
| 3 | Exact conditional CDF given `(L_0,L_1,L_2,L_3)` | **PROVED** (§3) |
| 4 | Proposição D4 (K=4 exact finite-`n` CDF, all `k`, four-regime proof collapsing to one formula) | **PROVED** (§4 — the main mandate) |
| 5 | Precise diagnosis of why K=4 needs 4 regimes (one more than K=3) | **PROVED** (§4.2–4.3, structural, not just observed) |
| 6 | Corollary D4.1 (`P(T=n)=24/n^4`) | **PROVED** (elementary direct proof) |
| 7 | Corollary D4.2 (NEW complete finite-`n` mean formula `\varphi_n^{(4)}`; constant term + leading rate exactly match cited targets) | **PROVED** (new all-orders content; the two cited anchors reproduced exactly) |
| 8 | Corollary D4.3 (`E[(M_n^{(4)})^2]\to1/5`) | **PROVED** |
| 9 | Corollary D4.4 (`E[(M_n^{(4)})^3]\to128/1155`, cross-checked against cited K=5 instance) | **PROVED** |
| 10 | Corollary D4.5 (uniform `O(1/n)` convergence, crude constant `7248`) | **PROVED** (not optimized; asymptotic constant `\approx0.7087` disclosed as unproved-uniform) |
| 11 | True brute force `n=4..8` matches D4 exactly | **PROVED** (`22/22` exact comparisons, `n=8`: `165.15M` configs) |
| 12 | Independent `O(n^4)`-ish reference engine matches D4, `n=4..30` | **PROVED** (`241/241` exact comparisons) |
| 13 | General-`K` closed-form-in-`(n,K)` CDF (`K\ge5`) | **OPEN**, not attempted (out of scope; §8) |
| 14 | "`K` regimes in the proof" pattern for general `K` | **OPEN**, unverified observation only, `4` data points, counting-convention caveat named (§8.1) |
| 15 | Sharper asymptotic rate constant `\approx0.7087/n` | asymptotic leading term only, **not** proved as a uniform finite-`n` bound (disclosed as such) |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No `git` command run of any kind. No `.py` file
from any other front (this lineage or any ancestor/sibling) was read,
opened, or imported — every script in this directory is written fresh
from the mathematical prose of `THEOREM.md` (Estágios 41, 40, 4, 6, 7,
24) and the cited `ATTEMPT.md` documents' prose only. Every claim above
is labeled PROVED / OPEN / NOT ATTEMPTED at the point of use; no claim is
left as an unlabeled assertion. All randomized verification used only the
reserved seed range `20260926000`–`20260926999`. No claim of progress on
any Millennium Problem; this is pure combinatorial mathematics internal
to the u12 ensemble defined in `THEOREM.md`.
