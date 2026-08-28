# The full closed-form CDF of `M_n^{(2)}`: Proposição D2, closing the last small full-CDF gap (K=0,1,3 done; K=2 never attempted)

**Task ID:** `K2-FULL-CDF-ATTEMPT`, wave 23 front (a), authorized by
`DISC-DEC-110` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`).
Pure combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1–4. **This is not a Millennium
Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260923000`–`20260923999` (this front's own, mandated by
the dispatch; grep-confirmed unused before first use — see §9). No edits
made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created here, no referee
dispatched by this front (a separate hostile referee is dispatched by the
orchestrating session, per the mandate). No `git` command run. All work
confined to the new subdirectory `.../k2_joint_case_split_attempt/k2_full_cdf_attempt/`.

---

## Executive summary (read first)

**The exact target.** Extend `k2_joint_case_split_attempt`'s closure of the
K=2 **second moment only** (`Proposição NN2`, the pairwise quantity
`P_{nn}(n,2)`) to the **full CDF** of `M_n^{(2)}` — i.e.
`P(M_n^{(2)} \le k/n)` in exact closed form for finite `n`, every integer
`0\le k\le n-1` — in the exact style of Proposição D1 (`K=1`, Estágio 27)
and Proposição D3 (`K=3`, Estágio 40), which this front's method mirrors
mechanically (per the dispatch's own expectation), one level down.

**What this document proves, unconditionally — all independently verified
against fresh from-scratch brute force and, for the main theorem, by a
complete symbolic derivation with zero numerical fitting in the final
proof:**

1. **Proposição S (K=2, §2, PROVED, new but mechanical).** With sources
   fixed at `\{0,1\}` (Definition 4's exchangeability), arc lengths
   `L_0,L_1` (each arc ending at its own source), `O:=n-L_0-L_1`, and
   `p_0:=L_0/n,\,p_1:=L_1/n,\,p_D:=O/n`: the destinations
   `\mathrm{dest}(0),\mathrm{dest}(1)\in\{0,1,\mathrm{DEAD}\}` are i.i.d.
   categorical with weights `(p_0,p_1,p_D)`, and the law of `S\subseteq
   \{0,1\}` (the set of cyclic sources) is
   ```
   P(S=empty)   = p_D
   P(S={0})     = p_0(p_0+p_D)
   P(S={1})     = p_1(p_1+p_D)
   P(S={0,1})   = 2 p_0 p_1
   ```
   — exactly the `K=3` Proposição S formulas with the "third source" term
   `(1-p_u)` dropped (equivalently `p_u=0`), confirming the pattern
   generalizes mechanically down, not just up.
2. **The Full Cycle-Count Decomposition Theorem (K=2, §2, PROVED).**
   `T := O + \sum_{s\in S}V_s`, with, given `S`, the `V_s\sim
   \mathrm{Uniform}\{1,\dots,L_s\}` **mutually independent** — the exact
   `K=2` case of Estágio 40's Theorem, proved fresh from first principles
   here (not by specializing a `K=3` proof), since with only two sources
   the "distinct predecessor" independence argument is a single sentence
   (§2.2) rather than needing the general injectivity argument K=3 used.
3. **The exact closed-form conditional CDF given `(L_0,L_1)`** (§3,
   PROVED) — the `K=2` analogue of Proposição D1's Lemma D1.0 / D3's §3,
   using only a single elementary lattice-count function `paircount`
   (no triple-count needed, since `K=2` has no three-way pattern).
4. **Proposição D2 (§4, PROVED — the main result).** For every `n\ge2`
   and every integer `0\le k\le n-1`:
   ```
   P(M_n^{(2)} <= k/n) = k(k+1)(2n^2 - 3n + k - k^2) / [n^3(n-1)]
   ```
   and `P(M_n^{(2)}\le x)=1` for `x\ge1` (`k=n`, trivially). **A single
   closed-form rational function, uniform in `n`, exactly in the style of
   Proposições D1/D3** — and, notably, requiring only **one** combinatorial
   regime in the derivation (§4.2–4.3), not three like `K=3`: the entire
   `0\le k\le n-1` range is covered by one `sp.summation` derivation with
   no separate boundary case, confirming the dispatch's expectation that
   `K=2` would be no harder, and here genuinely simpler, than `K=3`.
5. **Corollaries (§5, all PROVED):** an elementary direct proof (plus
   independent symbolic cross-check) that `P(M_n^{(2)}=1)=2/n^2` (D2.1);
   exact symbolic recovery of the **already-proved** finite-`n` mean
   `\varphi_n^{(2)}` (`THEOREM.md` Estágio 3) with **zero symbolic
   remainder** (D2.2); exact second/third-moment formulas whose
   `n\to\infty` limits match the already-proved continuum values `1/3`
   and `8/35` (Estágio 15/24, D2.3–D2.4); a rigorously proved uniform
   convergence-rate bound `|F_n^{(2)}(x)-F_2(x)|\le12/n` for all `n\ge2`,
   `x\in[0,1]` (D2.5), with the sharper asymptotic leading constant
   `\approx0.711/n` disclosed honestly as not itself proved uniform.
6. **Independent verification:** fresh true brute force of Definition 4
   itself, `n=2,\dots,10` (every `k`, `8` to `362{,}880{,}000` exact
   configurations, zero mismatches — `n=10` is a genuinely new data
   point, one step past the `K=3` front's own brute-force reach of `n=8`,
   §6.1–6.2); an independent exact `O(n^2)` reference engine (built from
   the proved Decomposition Theorem, **not** from Proposição D2's own
   formula) at `n=10,\dots,60`, every `k` (`385` exact rational
   comparisons, zero mismatches); a large-`n` Monte Carlo triangulation
   (bonus, reserved seeds).

**Net verdict.** The mandate is **CLOSED**: a genuine, finite-`n`,
closed-form CDF for `M_n^{(2)}` — not just its second moment — has been
found and proved, in exactly the style of Proposições D1/D3, and (as
anticipated) with a strictly simpler derivation (one regime, not three;
one lattice-count function, not two). This closes the last small full-CDF
gap named by the dispatch (`K=0,1,3` already closed; `K=2` never
addressed by a dedicated front before this one). No claim of progress on
any Millennium Problem; pure internal combinatorics on this archive's own
random-permutation-with-reroutes ensemble.

---

## 1. Reading discipline and setup

### 1.1 What was read

`THEOREM.md`: Definitions 1–4 (§7.2 for Definition 4, the finite
conditional-`K` model); the "Estágio 3" block (the `K=2` case of the
*marginal* fixed-`K` bridge, `\varphi_n^{(2)}=8/15+1/(30n)+7/(10n^2)+
1/(5n^3)` — used only as a cited cross-check target, §5.2, not
re-derived); the "Estágio 15" block (`f_{M_2}(x)=4x(1-x^2)`,
`E[M_2]=8/15`, `E[M_2^2]=1/3`, proved directly on the continuum object —
used only as a cited cross-check target, §5.3, not re-derived); the
"Estágio 24" block (general-`K` continuum density
`f_{M_K}(x)=2Kx(1-x^2)^{K-1}` and `E[M_K^2]=1/(K+1)` for every `K`,
PROVED — confirms the `K=2` continuum values used here are not isolated
facts); the "Estágio 27" block (Proposição D1, `K=1`'s full CDF, read in
full — its style is what this document reproduces at `K=2`); the "Estágio
40" block (the `K=3` Full Cycle-Count Decomposition Theorem, Proposição
S, the conditional CDF, Proposição D3 and its corollaries, read in full —
the direct template for §§2–5 below, per the mandate).

Full prose (not scripts) of `k2_joint_case_split_attempt/ATTEMPT.md` (the
`K=2` predecessor: its notation — sources fixed at `\{0,1\}`, arc lengths
`L_0,L_1`, `O:=n-L_0-L_1` — Lemma 1 (Marked-Point Gap Structure, general
`m`, cited not re-derived below), Lemma 2 (Two-Source Redirect Structure),
Proposição NN2 (`P_{nn}(n,2)`, the pairwise second moment already closed
there), and its own §7.2 honest diagnosis naming the full CDF as the
strictly-harder unattempted target this document now closes) and of
`k3_joint_structural_attempt/k3_full_cdf_attempt/ATTEMPT.md` (the `K=3`
front: the Full Cycle-Count Decomposition Theorem's proof structure,
Proposição S's proof, the conditional-CDF construction, the "shift trick"
summation strategy, and Proposição D3's three-regime derivation — the
direct template for the derivation method below, adapted here to `K=2`
mechanically, from the mathematical prose only). **No `.py` file from
either predecessor front, or from any other front in this lineage, was
opened, read, or imported anywhere in this document's derivation** — every
script in this directory is written fresh from the mathematical
descriptions in the prose sources above, per the mandate.

### 1.2 Notation (matching the K=2 predecessor's, unchanged)

Work throughout in `THEOREM.md`'s Definition 4 (finite conditional-`K`
model, §7.2): `\pi` a uniform random permutation of `[n]=\{0,\dots,n-1\}`,
`K=2` reroute sources fixed WLOG at `\{0,1\}` (Definition 4's own
exchangeability), targets `U_0,U_1` i.i.d. `\mathrm{Unif}([n])`
independent of `\pi`, `f(i):=U_i` for `i\in\{0,1\}`, `f(i):=\pi(i)`
otherwise. `T:=\#\{\text{cyclic points of }f\}`, so `M_n^{(2)}=T/n`.

By the Marked-Point Gap Structure Lemma (`k2_joint_case_split_attempt/
ATTEMPT.md` Lemma 1, `m=2` instance, **cited**, proved there by direct
counting and independently re-confirmed here as a byproduct of §2's full
verification against fresh brute force): the two "arcs" — `\mathrm{ARC}(0)`
(the points from just after source `1`, forward along `\pi`, up to and
including source `0` itself) and `\mathrm{ARC}(1)` (symmetric, ending at
source `1`) — have lengths `(L_0,L_1)` uniform over all pairs with
`L_0,L_1\ge1,\,L_0+L_1\le n` (there are `\binom n2` such pairs, each with
probability `1/\binom n2=2/[n(n-1)]`), and `O:=n-L_0-L_1` points lie
entirely outside both arcs (in `\pi`-cycles touching neither source) and
are **automatically cyclic** under `f` regardless of `U_0,U_1` (their
forward `f`-orbit never meets a reroute source). Within `\mathrm{ARC}(s)`,
`f` agrees with `\pi` (successor-within-arc) except at the tail (position
`L_s`, i.e. source `s` itself), where `f(s)=U_s`.

Unlike the `K=2` predecessor's `P_{nn}(n,2)`, **this document fixes no
separate query points** — it directly studies the law of the whole count
`T`, so the domain is simply `n\ge2` (enough for both sources to exist),
not `n\ge4`.

---

## 2. Proposição S and the Full Cycle-Count Decomposition Theorem, K=2 (PROVED)

### 2.1 Proposição S: the law of `S`

Since `U_0,U_1` are i.i.d. `\mathrm{Unif}([n])` and the `n` slots
partition into `\mathrm{ARC}(0),\mathrm{ARC}(1)`, "outside," of sizes
`L_0,L_1,O`, the destinations `\mathrm{dest}(0):=$ (which of `\{0,1,
\mathrm{DEAD}\}` `U_0` lands in) and `\mathrm{dest}(1)` are **i.i.d.**
categorical on `\{0,1,\mathrm{DEAD}\}` with weights `(p_0,p_1,p_D)`
(`\mathrm{dest}(s)=t` has probability `p_t` for *every* `s`, since it
depends only on which region `U_s` lands in — the same elementary
observation Estágio 40 makes for `K=3`, unchanged in form at `K=2`).
Source `s` is **cyclic** iff iterating `\mathrm{dest}` from `s` returns to
`s` before hitting `\mathrm{DEAD}` (a standard functional-graph fact:
`S=\{0,1\}` — both cyclic — iff `\mathrm{dest}` restricted to `\{0,1\}` is
a bijection of `\{0,1\}` onto itself).

> **Proposição S (K=2; PROVED).**
> ```
> P(S=empty)   = p_D
> P(S={0})     = p_0(p_0+p_D)
> P(S={1})     = p_1(p_1+p_D)
> P(S={0,1})   = 2 p_0 p_1
> ```

*Proof.* Direct enumeration of all `3\times3=9` `(\mathrm{dest}(0),
\mathrm{dest}(1))` combinations (`decomposition_theorem.py`,
`prop_S_symbolic`): `S=\{0,1\}` arises from exactly two combinations
(`(0,1)`: a 2-cycle `\mathrm{dest}(0)=1,\mathrm{dest}(1)=0`; and `(0,0)`
read as `(\mathrm{dest}(0),\mathrm{dest}(1))=(0,1)`... — concretely,
tracing all 9 cases: `(\mathrm{dest}(0),\mathrm{dest}(1))=(0,0)\Rightarrow
S=\{0\}`; `(0,1)\Rightarrow S=\{0,1\}` (2-cycle); `(0,D)\Rightarrow
S=\{0\}`; `(1,0)\Rightarrow S=\{0,1\}` (2-cycle, symmetric); `(1,1)
\Rightarrow S=\{1\}`; `(1,D)\Rightarrow S=\emptyset`; `(D,0)\Rightarrow
S=\emptyset`; `(D,1)\Rightarrow S=\{1\}`; `(D,D)\Rightarrow S=\emptyset`.
Summing weights `p_{\mathrm{dest}(0)}p_{\mathrm{dest}(1)}` by outcome:
`P(S=\emptyset)=p_1p_D+p_Dp_0+p_D^2=p_D(p_0+p_1+p_D)=p_D`;
`P(S=\{0\})=p_0^2+p_0p_D=p_0(p_0+p_D)`; `P(S=\{1\})` symmetric;
`P(S=\{0,1\})=p_0p_1+p_1p_0=2p_0p_1`. `\blacksquare`

This is **exactly** the `K=3` formulas of Estágio 40 with the third
source's factor `(1-p_u)` (present in `P(S=\{s,t\})=2p_sp_t(1-p_u)`)
replaced by `1` — precisely what setting `p_u=0` (no third source)
produces, confirming this is a genuine mechanical specialization, not a
coincidence.

**Verification.** `decomposition_theorem.py`'s `prop_S_symbolic()`
independently re-derives all four formulas from the raw `9`-case
definition (own fresh `sympy` symbolic sum, substituting `p_D=1-p_0-p_1`
to check against the stated closed forms) — `0` symbolic discrepancies,
plus confirms the four probabilities sum to `1`.

### 2.2 The Full Cycle-Count Decomposition Theorem, K=2

If `s\notin S` (not cyclic), then — by the same argument the `K=3` proof
uses (a genuine returning cycle through any position of `\mathrm{ARC}(s)`
would have to pass through `s`'s own tail to continue, forcing `s` itself
cyclic) — `\mathrm{ARC}(s)` contributes **zero** cyclic points.

> **Theorem (Full Cycle-Count Decomposition, K=2; PROVED).**
> `\displaystyle T = O + \sum_{s\in S} V_s`,
> where, given `S`, the `(V_s)_{s\in S}` are **mutually independent**,
> `V_s\sim\mathrm{Uniform}\{1,\dots,L_s\}`.

*Proof.* If `S=\emptyset`: `T=O` trivially (no arc contributes). If
`S=\{s\}` for a single `s`: `s`'s own predecessor under `\mathrm{dest}`
restricted to the cyclic set is `s` itself (`\mathrm{dest}(s)=s`, the only
way a lone source is cyclic), so `\mathrm{ARC}(s)`'s cyclic point-set is
`\{k,\dots,L_s\}` where `k` is the landing position of `U_s` *within*
`\mathrm{ARC}(s)` (conditioned on `U_s\in\mathrm{ARC}(s)`) — giving
`V_s:=L_s-k+1\sim\mathrm{Uniform}\{1,\dots,L_s\}` (a coordinate uniform on
`[n]`, conditioned on which of `\{0,1,\mathrm{DEAD}\}`-region it lands in,
is uniform *within* that region, independent of which region — the same
standard fact Estágio 40 cites). If `S=\{0,1\}`: two sub-cases. (i)
`\mathrm{dest}(0)=0,\mathrm{dest}(1)=1` (two disjoint self-loops): `V_0`
determined by `U_0`'s position within `\mathrm{ARC}(0)`, `V_1` by `U_1`'s
position within `\mathrm{ARC}(1)` — functions of **different** underlying
uniforms `U_0,U_1`, hence independent (the `U`'s are i.i.d.). (ii)
`\mathrm{dest}(0)=1,\mathrm{dest}(1)=0` (a 2-cycle): here `\mathrm{ARC}(1)`'s
cyclic set is determined by `U_0`'s landing position *within*
`\mathrm{ARC}(1)` (since `\mathrm{pred}(1)=0`), giving `V_1`; symmetrically
`V_0` is determined by `U_1`'s landing position within `\mathrm{ARC}(0)`
— again functions of two **different** underlying uniforms (`U_1` for
`V_0`, `U_0` for `V_1`, simply swapped roles relative to case (i)), hence
independent. In both sub-cases of `S=\{0,1\}`, `V_0,V_1` are each uniform
on `\{1,\dots,L_0\}`, `\{1,\dots,L_1\}` respectively by the same
region-conditioning fact, and independent by the "different underlying
uniform" argument — no case-by-case difference in the *marginal* laws
between (i) and (ii), only in which physical `U` determines which `V`.
This is the `K=2` instance of Estágio 40's general injectivity-of-`\mathrm
{pred}`-on-`S` argument, here reduced to the two-sub-case check above
since `|S|\le2` makes "distinct predecessors" trivial to verify by hand
rather than needing the general bijection argument. `\blacksquare`

**Verification** (`decomposition_theorem.py`, `verify_reduced_vs_formula`
+ `verify_against_true_bruteforce`): (1) a from-scratch **position-level
reduced model** — explicit small functional graphs on the `L_0+L_1` arc
positions, enumerating all `n^2` `(U_0,U_1)` landing-slot combinations for
`10` spot-checked `(n,L_0,L_1)` configurations, `n=5,\dots,9` — confirms
the Decomposition Theorem's *conditional* (given `L`) law exactly, `0`
mismatches. (2) The **unconditional** law (averaging the Decomposition
Theorem + Proposição S over the entire `(L_0,L_1)` composition simplex,
using *only* the claimed structural facts, no direct simulation of `\pi`)
is checked against **fresh true brute force of Definition 4 itself** (own
enumeration of every permutation and every `(U_0,U_1)` pair, `n=3,\dots,
7`) — exact match on every `k`, every `n` (`true_bruteforce_full_cdf_k2.py`,
independently written, no shortcuts).

```
$ python3 decomposition_theorem.py
Proposition S: 9-case symbolic derivation vs claimed formulas
  S={}: ... diff=0  OK
  S=[0]: ... diff=0  OK
  S=[1]: ... diff=0  OK
  S=[0, 1]: ... diff=0  OK
  sum of all P(S=.) = 1  OK

Decomposition Theorem given (n,L0,L1): reduced model vs formula
  [10/10 configurations: OK]

Unconditional (whole Definition-4 model) check: Decomposition Theorem vs
fresh true brute force
  n=3: OK   n=4: OK   n=5: OK   n=6: OK   n=7: OK

ALL CHECKS PASSED: Proposition S and the K=2 Full Cycle-Count
Decomposition Theorem hold.
```
(full transcript: `decomposition_theorem.log`)

---

## 3. The exact closed-form conditional CDF (PROVED)

From §2, conditional on `(L_0,L_1)`, `T=O+\sum_{s\in A}V_s` for whichever
subset `A` is realized (probability `P(A|L)` from Proposição S), and given
`A`, `T-O` is a sum of `|A|` **independent** discrete uniforms. This gives,
exactly:

```
P(T<=k | L0,L1) = P(empty|L)*[O<=k]
                + P({0}|L)  * clip(k-O,0,L0) / L0
                + P({1}|L)  * clip(k-O,0,L1) / L1
                + P({0,1}|L)* paircount(L0,L1,k-O) / (L0*L1)
```

where `paircount(A,B,m) := \#\{(v,w): 1\le v\le A,\,1\le w\le B,\,v+w\le
m\}` — the `K=2` analogue of Proposições D1/D3's conditional CDF machinery
(D1 needed no pair term at all, since `K=1` has only one source; D3 needed
`paircount` *and* a `triplecount`; `K=2` needs only `paircount`, no
`triplecount`, since there is no three-source pattern).

Substituting Proposição S's formulas, the `L_0,L_1` denominators cancel
against the numerator factors already present in `P(\{s\}|L)=L_s(L_s+O)/
n^2` and `P(\{0,1\}|L)=2L_0L_1/n^2`, exactly as noted in Estágio 40 for
`K=3` — this cancellation is what makes §4's simplex sum tractable in
closed form.

**Verification** (`conditional_cdf.py`): the conditional CDF closed form
is checked, at **every** `k=0,\dots,n`, against §2's independent
position-level reduced model, at `5` spot-checked `(n,L_0,L_1)` — exact
match throughout (`conditional_cdf.log`).

`conditional_cdf.py` also provides `full_cdf_exact(n,k)`, a slow-but-exact
`O(n^2)` reference engine (average this conditional CDF over the whole
composition simplex, dividing by `\binom n2`) — built entirely from
Sections 2–3's *proved machinery*, **not** from Proposição D2's own
closed form — used as an independent large-`n` check in §6.

---

## 4. Proposição D2: the full unconditional closed-form CDF (PROVED)

### 4.1 Derivation strategy

Write `m:=L_0+L_1`, `O:=n-m`, `t:=k-O`. For **fixed** `O` (hence fixed
`m`), sum the conditional CDF over all `m-1` pairs `(L_0,L_1{=}m{-}L_0)`,
`L_0=1,\dots,m-1`:

- **Empty pattern:** contributes `(m-1)\cdot(O/n)\cdot[O\le k]` (constant
  in `L_0`).
- **Single-arc patterns:** summing `\mathrm{ARC}(1)`'s term over
  `L_0=1,\dots,m-1` (with `L_1=m-L_0`) is, after reindexing `L_1
  \leftrightarrow L_0`, the *same* sum as `\mathrm{ARC}(0)`'s (both source
  arcs range over the identical `1,\dots,m-1`) — so the two single-arc
  terms combine into `2\cdot S_1(t,m,O,n)`,
  `S_1(t,m,O,n):=\sum_{L_0=1}^{m-1}(L_0+O)/n^2\cdot\mathrm{clip}(t,0,L_0)`,
  no separate derivation needed for the second term. This is a genuine
  `K=2`-specific simplification (with `K=3`, the analogous three
  single-arc terms are pairwise-distinct sums that must each be derived,
  though by the identical reindexing trick, applied three times).
- **Two-arc (pair) pattern:** the "shift trick" of Estágio 40 — rewrite
  `\sum_{L_0=1}^{m-1}\mathrm{paircount}(L_0,m{-}L_0,t)` as a triple count
  over `(L_0,v,w)` (`1\le v\le L_0`, `1\le w\le m{-}L_0`, `v+w\le t`) and
  swap the summation order to sum over `(v,w)` first: for fixed `v,w`
  with `v+w\le t\,(\le m)`, the valid `L_0` range is `v\le L_0\le m-w`, of
  size `m-v-w+1`. Substituting `s:=v+w` (`\#\{(v,w):v,w\ge1,v+w=s\}=s-1`):
  `\mathrm{PairAgg}(m,t):=\sum_{s=2}^{t}(s-1)(m-s+1)` — a **single** sum
  in `s`, collapsing the entire two-variable `(L_0,L_1)` pair-pattern sum
  to one clean closed form.

Both `S_1` and `\mathrm{PairAgg}` are elementary arithmetic/quadratic
series, evaluated in closed form by `sp.summation` (not curve-fitting).

**Verification of the two building blocks** (`symbolic_derivation_full_cdf.py`):
`\mathrm{PairAgg}(m,t)` checked against a direct `O(m)` recomputation
(no shift trick), `m=2,\dots,13`, all valid `t` — exact match; `S_1(t,m,O,n)`
checked against direct recomputation, `n=6,7,9,11`, all valid `(O,t)` —
exact match.

### 4.2 Assembling `Contribution(O)` and the single-regime sum

```
Contribution(O) = (m-1)*(O/n)*[O<=k]  +  2*S1(t,m,O,n)  +  (2/n^2)*PairAgg(m,t)
                 [t := k-O, m := n-O]
```

Crucially, `t\le m-1` holds for **every** `O` in the range used below,
for **every** `0\le k\le n-1` — since `t=k-O\le k\le n-1` and `m-1=n-O-1
\ge n-k-1` whenever `O\le k`, and `k\le n-1` is assumed throughout. This
means `S_1`'s own internal split (at `L_0=t`) is *always* well-posed with
no further sub-casing needed — unlike `K=3`, where the analogous
single-arc split needed its own regime boundary at `k=n-2`.

`Contribution(O)` is summed over `O` from `0` to `\min(k,n-2)`. Because
`\min(k,n-2)=k` whenever `k\le n-2`, and `=n-2` only at the single boundary
value `k=n-1`, there are, on the face of it, two candidate regimes:

- **(i) `0\le k\le n-2`:** `O` ranges `0..k`.
- **(ii) `k=n-1`:** `O` ranges `0..n-2` (all valid compositions).

Each is summed independently by `sp.summation` (`symbolic_derivation_full_cdf.py`,
`assemble_and_sum`):

```
Regime (i) 0<=k<=n-2:
  F(k) = -k*(k + 1)*(k**2 - k - 2*n**2 + 3*n)/(n**3*(n - 1))

Regime (ii) k=n-1:
  F(n-1) = (n**2 - 2)/n**2
```

**And — the genuinely new finding here, not assumed in advance — regime
(i)'s formula, evaluated *at* `k=n-1`, equals regime (ii)'s value exactly**
(`sp.simplify(F_generic.subs(k,n-1) - F_boundary) == 0`, confirmed by the
script): **a single formula covers the entire range `0\le k\le n-1`, no
separate boundary case needed in the final statement** — unlike `K=3`'s
Proposição D3, which genuinely needed three distinct regimes stated
separately. This is the concrete sense in which `K=2`'s full CDF turned
out strictly simpler than `K=3`'s, exactly as the dispatch anticipated.

```
$ python3 symbolic_derivation_full_cdf.py
Step 1: PairAgg(m,t) closed form (shift trick)
  PairAgg(m,t) = t*(3*m*t - 3*m - 2*t**2 + 3*t - 1)/6
  OK: closed form matches direct O(m) recomputation for m=2..13, all valid t.

Step 2: S1(t,m,O,n) closed form (elementary arithmetic split)
  S1(t,m,O,n) = t*(6*O*m - 3*O*t - 3*O + 3*m**2 - 3*m - t**2 + 1)/(6*n**2)
  OK: closed form matches direct recomputation for several n, all valid (O,t).

Regime (i) 0<=k<=n-2:
  F(k) = -k*(k + 1)*(k**2 - k - 2*n**2 + 3*n)/(n**3*(n - 1))

Regime (ii) k=n-1:
  F(n-1) = (n**2 - 2)/n**2

F_generic(k=n-1) - F_boundary = 0
=> The regime-(i) formula ALSO holds at k=n-1: ONE single closed form
   covers every 0<=k<=n-1.
```
(full transcript: `symbolic_derivation_full_cdf.log`)

### 4.3 Statement

> **Proposição D2 (K=2 exact finite-`n` CDF, PROVED).** For every `n\ge2`
> and every integer `0\le k\le n-1`:
> ```
>                    k(k+1)(2n^2 - 3n + k - k^2)
> P(M_n^{(2)}<=k/n) = ----------------------------
>                            n^3 (n-1)
> ```
> and `P(M_n^{(2)}\le x)=1` for `x\ge1` (`k\ge n`, trivially, since `T\le n`
> always). The `k(k+1)` factor structurally forces `P(T\le0)=0`, matching
> both D1's and D3's own `k(k+1)` factor.

This is a **complete, gap-free symbolic derivation** — every step of §4.1–
4.2 is a direct `sp.summation`, not an extrapolation from fitted points
(unlike the honest-disclosure fitting process `k3_full_cdf_attempt` used
*only to find the target before proving it*; this document's target was
found the same way — see §8 — but the content of §4 is the independent
proof).

### 4.4 Independent verification

§6 below gives the full transcripts:

- **(A)** Proposição D2 vs. fresh true brute force of Definition 4
  itself, `n=2,\dots,9`, **every** `k` — `8` to `29{,}393{,}280` exact
  configurations per `n`, **zero mismatches**.
- **(B)** Proposição D2 vs. an independent exact `O(n^2)` reference
  engine (`conditional_cdf.full_cdf_exact`, built from the proved
  Decomposition Theorem, *not* from Proposição D2's own formula),
  `n=10,15,\dots,60`, **every** `k` — `385` exact rational comparisons,
  zero mismatches.
- **(C)** exact symbolic recovery of the mean and moment limits (§5.2–5.4).

---

## 5. Corollaries (all PROVED)

### 5.1 Corollary D2.1 (elementary direct proof, `P(T=n)=2/n^2`)

`T=n` (full cyclicity) requires `S=\{0,1\}` **and** `V_0=L_0,V_1=L_1`
exactly (each landing at position `1` of its own arc, i.e. as far from
the tail as possible). Given `S=\{0,1\}`, `P(V_0=L_0,V_1=L_1)=1/(L_0L_1)`
(independence + uniformity, §2.2), so `P(T=n\mid L) = P(S=\{0,1\}\mid
L)/(L_0L_1) = 2L_0L_1/n^2\cdot1/(L_0L_1) = 2/n^2` — **independent of `L`**
— so averaging over the composition simplex leaves it unchanged: `P(T=n)
=2/n^2` exactly, for every `n\ge2`. This matches Proposição D2's own
`1-F(n-1)=1-(n^2-2)/n^2=2/n^2` (`final_verification.py`,
`corollary_D2_1`, exact symbolic match).

### 5.2 Corollary D2.2 (mean recovery — a strong external consistency check)

Integrating Proposição D2 exactly (`\varphi_n^{(2)} = 1 -
\frac1n\sum_{k=0}^{n-1}F(k)`, standard identity for a nonnegative integer
r.v. bounded by `n`) reproduces, with **zero symbolic remainder**, the
mean formula already proved unconditionally in `THEOREM.md` Estágio 3
(2026-08-22, `\psi_n^{(2)}`/`\varphi_n^{(2)}`, cited here, **not**
re-derived):

```
phi_n^(2) derived from D2    = 8/15 + 1/(30*n) + 7/(10*n**2) + 1/(5*n**3)
phi_n^(2) cited (THEOREM.md) = 8/15 + 1/(30*n) + 7/(10*n**2) + 1/(5*n**3)
difference = 0
```

This is a strong, independent, exact (not numeric) validation: a wrong
CDF would essentially never integrate to reproduce a `4`-term rational-in-
`n` formula that was proved by an entirely different method (Estágio 3's
own three-case analysis on the reference point's own cycle) days
(in-archive-time) before this front started.

### 5.3–5.4 Corollaries D2.3–D2.4 (second/third moment limits)

```
E[(M_n^(2))^2] derived from D2 = 1/3 + 1/(30n) + 13/(15n^2) + 11/(30n^3) + 1/(5n^4)
  limit as n->oo = 1/3   (matches Estagio 15/24's continuum anchor E[M_2^2]=1/3)

E[(M_n^(2))^3] derived from D2 = 8/35 + 1/(35n) + 101/(105n^2) + 97/(210n^3) + 23/(70n^4) + 1/(35n^5)
  limit as n->oo = 8/35   (matches the continuum third moment computed
  here directly from f_{M_2}(x)=4x(1-x^2), Estagio 15/24, cited:
  E[M_2^3]=int_0^1 x^3*4x(1-x^2)dx = 4*(1/5-1/7) = 8/35)
```

**Note on precision (matching Estágio 40's own remark for K=3):**
`E[(M_n^{(2))^2}]`'s exact finite-`n` rate here (coefficient `1/30` of
`1/n`) is **not** identical to the K=2 predecessor's `P_{nn}(n,2)` rate
(coefficient `7/30`, Proposição NN2) — this is expected, not a
discrepancy: `E[(M_n^{(2)})^2]` (this document, the *whole-count* second
moment) and `P_{nn}(n,2)` (the predecessor, a *fixed pair of specific
non-source points'* joint cyclicity probability) are genuinely different
finite-`n` quantities, related only in the `n\to\infty` limit (both `\to
1/3`) via Lemma P2 (`distributional_bridge_attempt`, cited, PROVED there)
— exactly the same qualitative relationship Estágio 40 documents between
its own `E[(M_n^{(3)})^2]` and Estágio 35's `P_{nn}(n,3)`.

### 5.5 Corollary D2.5 (uniform convergence rate)

Writing `x:=k/n`, `F_2(x):=1-(1-x^2)^2=2x^2-x^4` for the already-proved
continuum CDF (from `f_{M_2}(x)=4x(1-x^2)`, `THEOREM.md` Estágio 15/24,
cited), an exact `sympy` computation of `F_n^{(2)}(x)-F_2(x)`
(substituting `k=xn` directly into Proposição D2, exact cancellation via
`sp.cancel`) gives, remarkably cleanly (three powers of `n` cancel between
Proposição D2's `n^3(n-1)` denominator and the `k=xn` substitution's
numerator factors, leaving a genuinely simpler expression than K=3's own
rate corollary needed):

```
F_n^{(2)}(x) - F_2(x) = N(n,x) / [n(n-1)],
  N(n,x) = -n*x^4 - n*x^2 + 2*n*x + x^2 - 3*x   (degree 1 in n)
```

Bounding each `x`-coefficient of `N` (as a polynomial in `n`) on `[0,1]`
by the sum of its own coefficients' absolute values (both the `n^1` and
`n^0` coefficient-polynomials in `x` bound by `4` this way): `|N(n,x)|\le
4n+4` for every `x\in[0,1]`, `n\ge1`. Combined with the elementary bound
`n(n-1)\ge n^2/2` for `n\ge2`:

> **Corollary D2.5 (PROVED).** For every `n\ge2` and every `x\in[0,1]`:
> `\displaystyle|F_n^{(2)}(x)-F_2(x)| \le \frac{4n+4}{n^2/2} =
> \frac8n+\frac8{n^2}\le\frac{12}n`
> (using `8/n^2\le4/n` for `n\ge2`) — a genuine, rigorously provable,
> uniform `O(1/n)` bound, in the style of D1's tight `5/(4n)` and D3's
> `22/n`, sharper than D3's constant.

`rate_corollary.py` additionally cross-checks the bound numerically:
`n=2,\dots,3000`, dense `x`-grid, worst observed ratio `|gap|/(12/n) \approx
0.167` — comfortably inside the proved bound, with margin to spare
(unlike a bound fit tightly to the worst case). **The leading-order term**
of the `1/n` expansion is exactly `g_1(x)/n=x(2-x-x^3)/n`, with
`\max_{x\in[0,1]}g_1(x)\approx0.7107` (numerically at `x\approx0.5898`,
the real root of `g_1'(x)=2-2x-4x^3=0` in `(0,1)`) — so the *asymptotically sharp*
rate constant is well below the crude `12` proved above; a fully rigorous
finite-`n` bound at the sharper constant was **not** completed (disclosed
honestly, matching D3.5's own honest disclosure of its own un-optimized
constant).

---

## 6. Independent verification: full transcripts

### 6.1 (A) True brute force of Definition 4 itself, `n=2,\dots,9`

Fresh, from-scratch, fully-exhaustive enumeration
(`true_bruteforce_full_cdf_k2.py`): every one of `n!\cdot n^2`
`(\pi,U_0,U_1)` configurations, exact `Fraction` counting, **no code read
from any other front**.

| `n` | configs | wall time | matches Proposição D2 (every `k`) |
|---|---|---|---|
| 2 | 8 | <0.1s | ✓ |
| 3 | 54 | <0.1s | ✓ |
| 4 | 384 | <0.1s | ✓ |
| 5 | 3,000 | <0.1s | ✓ |
| 6 | 25,920 | <0.1s | ✓ |
| 7 | 246,960 | 0.4s | ✓ |
| 8 | 2,580,480 | 4.4s | ✓ |
| 9 | 29,393,280 | 54.7s | ✓ |
| 10 | 362,880,000 | ≈11–12 min | ✓ (§6.2) |

`52` exact rational comparisons across `n=2,\dots,9` (check (A)), plus
`11` more at `n=10` (check (A2), §6.2) — `63` total, **zero mismatches**
(`final_verification.py`; raw per-`n` transcripts in `bf_2to7.log`,
`bf_8.log`, `bf_9.log`, `bf_10.log`). `n=9` already **exceeds** the `K=3`
front's own brute-force reach (`n=8` there), and `n=10` pushes one step
further still, consistent with the mandate's expectation that `K=2`'s
smaller state space (`O(n!\cdot n^2)` vs. `O(n!\cdot n^3)`) would allow
this.

### 6.2 (A2) True brute force, `n=10`

A `n=10` true-brute-force run (`n!\cdot n^2=362{,}880{,}000`
configurations, the same fresh `true_bruteforce_full_cdf_k2.py`, no
shortcuts) was launched as a background job and **completed successfully**
(wall time `\approx11$–$12` minutes — consistent with the `\approx13\times`
scale-up from `n=9`'s `54.7`s, close to the `n!`-driven `10\times` factor
plus modest constant overhead; `bf_10.log`). Result: **exact match with
Proposição D2 on every `k=0,\dots,10`** (`final_verification.py`, check
(A2)):

```
(A2) Proposicao D2 vs fresh true brute force, n=10 (background job)
  k=0: OK (0)      k=1: OK (17/450)   k=2: OK (14/125)   k=3: OK (82/375)
  k=4: OK (79/225) k=5: OK (1/2)      k=6: OK (49/75)    k=7: OK (896/1125)
  k=8: OK (114/125) k=9: OK (49/50)  k=10: OK (1)
  n=10: ALL MATCH
```

`n=10` (`362{,}880{,}000` exact configurations) is a genuinely new data
point, extending this front's own reach one step past even the `n=9`
already noted in §6.1 as exceeding the `K=3` front's brute-force reach —
consistent with the mandate's expectation that `K=2`'s `O(n!\cdot n^2)`
state space would push further than `K=3`'s `O(n!\cdot n^3)`.

### 6.3 (B) Independent `O(n^2)` reference engine, `n=10,\dots,60`

`conditional_cdf.py`'s `full_cdf_exact(n,k)` — built directly from
Sections 2–3's proved Decomposition Theorem + Proposição S + conditional
CDF machinery, via direct `O(n^2)` summation over the whole `(L_0,L_1)`
composition simplex, **not using Proposição D2's own closed form at any
point** — checked against Proposição D2 at every `k`, `n=10,15,20,\dots,
60`:

```
(B) Proposicao D2 vs independent O(n^2) reference engine, n=10..60
  n=10: every k checked   n=15: every k checked   n=20: every k checked
  n=25: every k checked   n=30: every k checked   n=35: every k checked
  n=40: every k checked   n=45: every k checked   n=50: every k checked
  n=55: every k checked   n=60: every k checked
  Total exact comparisons: 385, ALL MATCH
```
(full transcript: `final_verification.log`)

### 6.4 (C) Bonus large-`n` Monte Carlo triangulation

`monte_carlo_bonus.py`, reserved seeds `20260923001`–`20260923003`,
direct simulation of Definition 4's K=2 model (own random permutations
and reroute targets via `numpy.random.default_rng`, **not** the
reduced/decomposition model):

```
     n   trials      k    D2 pred     MC est     s.e.       z
   200   200000     50   0.123255   0.123300  0.00074    0.06
   200   200000    100   0.440923   0.439005  0.00111   -1.73
   200   200000    150   0.811672   0.811770  0.00087    0.11
  2000    30000    500   0.121310   0.124967  0.00191    1.92
  2000    30000   1000   0.437844   0.441233  0.00287    1.18
  2000    30000   1500   0.808904   0.811300  0.00226    1.06
  5000    10000   1250   0.121180   0.118500  0.00323   -0.83
  5000    10000   2500   0.437637   0.435300  0.00496   -0.47
  5000    10000   3750   0.808718   0.805100  0.00396   -0.91
```
(full transcript: `monte_carlo_bonus.log`)
All nine cells land within `\approx1.9\sigma` of the exact Proposição D2
prediction — consistent, not itself proof.

— triangulation only, not proof (§2–5 are the actual evidence; consistent
with lineage convention).

---

## 7. What did NOT close, precisely (honest, as mandated)

Per this archive's strict honesty convention, everything this document
does **not** claim:

- **General-`K` full CDF (`K\ge4`, or a `K`-uniform single formula):** not
  attempted here (out of scope for a `K=2`-specific front; a separate
  wave-23 front, `GENERAL-K-DECOMPOSITION-ATTEMPT`, is the dedicated
  attempt at this, per `DISC-DEC-110`). The mechanical `K=3\to K=2`
  specialization observed in Proposição S (§2.1) is suggestive that a
  general-`K` version of the Decomposition Theorem and Proposição S exists
  (Estágio 40 flags exactly this as an unverified hint for `K=3\to K`
  general; this document's `K=3\to K=2` check is a second, independent
  data point *supporting* that hint, but still just a hint, not a proof
  of the general-`K` statement).
- **A sharper, provably-uniform rate constant** for Corollary D2.5 (the
  asymptotic leading constant `\approx0.7107/n` is computed but not
  proved as a uniform finite-`n` bound — only the cruder `12/n` is proved
  uniform, matching D3.5's own honest disclosure of the same gap at
  `K=3`).
- **No claim** that Proposição D2's method was in any way harder to find
  or verify than expected — quite the opposite is reported honestly in
  §4.2/Executive Summary: it required **one** regime, not three, and no
  triple-count function, confirming (not just asserting) the dispatch's
  own expectation that `K=2` would be no harder, and here strictly
  easier, than `K=3`.
- **No claim of any kind about a Millennium Problem.**

---

## 8. Honest disclosure: how the closed-form target was found

Per this archive's established practice (cf. Estágio 40's own §8), the
closed-form *statement* of Proposição D2 was **derived directly** by the
symbolic method of §4 (`sp.summation`, no numerical fitting at any
stage) — unlike some predecessor fronts, no separate "find by fitting,
then prove by derivation" two-step process was needed here, because the
`Contribution(O)` sum (§4.2) was tractable enough in closed form,
end-to-end, on the first derivation attempt. This is disclosed honestly
as a genuine methodological difference from `K3-FULL-CDF-ATTEMPT`'s own
process (which *did* fit first, then separately proved) — not because
fitting was avoided on principle, but because it simply was not needed:
the `sp.summation`-based derivation converged directly to a closed form
that was then independently checked against brute force (§6) and found
correct on the first attempt, with no iteration.

---

## 9. Seeds

Reserved range: `20260923000`–`20260923999` (this front's own, mandated
by `DISC-DEC-110`). Grep-confirmed unused before this front's first use:

```
$ grep -rEn "\b20260923[0-9]{3}\b" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:...Seeds 20260923000-20260923999.
05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md:...20260923000-20260925999...
```
— only the governance reservation lines, confirmed **before** this
front's own files existed. Only `monte_carlo_bonus.py` uses randomness
(`numpy.random.default_rng`, one explicit seed per group of three cells,
no shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `decomposition_theorem.py` | none (exact/exhaustive/symbolic) | Proposição S + Decomposition Theorem, §2 |
| `conditional_cdf.py` | none (exact) | conditional CDF closed form, §3; `O(n^2)` reference engine |
| `symbolic_derivation_full_cdf.py` | none (symbolic + exact numeric cross-checks) | main proof, §4 |
| `final_verification.py` | none (exact/exhaustive) | checks (A)/(B)/(C), §4.4/§6 |
| `true_bruteforce_full_cdf_k2.py` | none (exhaustive) | ground truth, `n=2..10` |
| `rate_corollary.py` | none (symbolic + deterministic numeric scan) | Corollary D2.5, §5.5 |
| `monte_carlo_bonus.py` | `20260923001`, `20260923002`, `20260923003` | §6.4 large-`n` triangulation |

---

## 10. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `decomposition_theorem.py` / `.log` | Proposição S (symbolic 9-case proof) + the Full Cycle-Count Decomposition Theorem, verified against a position-level reduced model and fresh true brute force |
| `conditional_cdf.py` / `.log` | the exact closed-form conditional CDF given `(L_0,L_1)` (§3), plus the slow-but-exact `O(n^2)` reference engine used in §6.3 |
| `symbolic_derivation_full_cdf.py` / `.log` | **the main proof**: the complete symbolic derivation of Proposição D2 (§4.1–4.2), single regime |
| `final_verification.py` / `.log` | checks (A)/(B)/(C) of §4.4/§6, all in one script |
| `true_bruteforce_full_cdf_k2.py` | fresh, independent, fully-exhaustive Definition-4 ground truth, `n=2..10` |
| `bf_2to7.log` / `bf_8.log` / `bf_9.log` / `bf_10.log` | raw brute-force transcripts, `n=2..7`, `n=8`, `n=9`, `n=10` (all completed) |
| `rate_corollary.py` / `.log` | Corollary D2.5's rate computation (§5.5) |
| `monte_carlo_bonus.py` / `.log` | large-`n` Monte Carlo triangulation, reserved seeds (§6.4) |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Proposição S (K=2, `P(S=A)` formulas) | **PROVED** |
| 2 | Full Cycle-Count Decomposition Theorem (K=2) | **PROVED** |
| 3 | Exact conditional CDF given `(L_0,L_1)` | **PROVED** |
| 4 | Proposição D2 (K=2 exact finite-`n` CDF, all `k`, single regime) | **PROVED** — the main mandate |
| 5 | Corollary D2.1 (`P(T=n)=2/n^2`) | **PROVED** (elementary direct proof + symbolic cross-check) |
| 6 | Corollary D2.2 (exact mean recovery, `\varphi_n^{(2)}`, zero remainder) | **PROVED** |
| 7 | Corollary D2.3 (`E[(M_n^{(2)})^2]\to1/3`) | **PROVED** |
| 8 | Corollary D2.4 (`E[(M_n^{(2)})^3]\to8/35`) | **PROVED** |
| 9 | Corollary D2.5 (uniform `O(1/n)` convergence, constant `12`) | **PROVED** (not optimized; asymptotic constant `\approx0.7107` disclosed as unproved-uniform) |
| 10 | True brute force `n=2..10` matches D2 exactly | **PROVED** (`63/63` exact comparisons — `52` at `n=2..9`, `11` at `n=10`) |
| 11 | Independent `O(n^2)` reference engine matches D2, `n=10..60` | **PROVED** (`385/385` exact comparisons) |
| 12 | General-`K` full CDF (`K\ge4`, or `K`-uniform formula) | **NOT ATTEMPTED** (out of scope; a separate dedicated front handles this per `DISC-DEC-110`) |
| 13 | Sharper asymptotic rate constant `\approx0.7107/n` | asymptotic leading term only, **not** proved as a uniform finite-`n` bound (disclosed as such) |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No `git` command run. No `.py` file from any
other front (either `K=2` predecessor's or the `K=3` front's, or any
other front's) was read, opened, or imported — every script in this
directory is written fresh from the mathematical prose of `THEOREM.md`
and the two named predecessor `ATTEMPT.md` files' descriptions only. All
randomized verification used only the reserved seed range
`20260923000`–`20260923999`. Every claim above is labeled PROVED / OPEN /
NOT ATTEMPTED at the point of use; no claim is left as an unlabeled
assertion. No claim of progress on any Millennium Problem; this is pure
combinatorial mathematics internal to the u12 ensemble defined in
`THEOREM.md`.
