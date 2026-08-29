# K6-EXACT-CLOSURE-ATTEMPT (wave 30, front b)

**Mandate** (`DISC-DEC-138`, `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`):
the immediate predecessor (`.../exact_algebraic_closure_attempt/
k5_exact_closure_attempt/ATTEMPT.md`, wave 29 front c, integrated as
`THEOREM.md` Estágio 53) extended the exact resultant-elimination
method to `K=5` (`n\ge7`), deriving Proposição D5 from scratch since no
closed-form CDF for `K=5` existed anywhere in the archive before that
front. This front's mandate, quoted from the ledger: *"estender o
método de eliminação por resultante para `K=6` na série exata de
constantes de taxa finito-`n`. Justificativa: `K=5` (Estágio 53) fechou
sem nenhuma obstrução algébrica nova — quinto sucesso mecânico
consecutivo do mesmo método, `K=6` é o próximo passo natural nomeado."*

## 0. Executive summary

**Outcome: full exact closure, `K=6`, `n\ge8`** — matching the `n_0=K+2`
pattern established at `K=2,3,4,5` (`n_0=4,5,6,7`), now extended one
step further and independently *verified*, not merely assumed.
`|F_n^{(6)}(x)-F_6(x)|\le M_6/n` for **all** `n\ge8` and `x\in[0,1]`,
where `M_6=0.67967830129138512967160338683005533\ldots` is the *exact*
asymptotic constant — the unique root in `(0,1)` of `g_6`'s
critical-point quartic `30t^4-14t^3+t^2+4t-1`, and equivalently a root
of `M_6`'s own irreducible minimal quartic
`35429400000000000t^4+17921731935293824t^3-248044660324924125t^2+350950285900800000t-137134080000000000`
(§4.2). The critical-point polynomial `g_6'(x)` factors as
`-6(x-1)^4(x+1)^3(30x^4-14x^3+x^2+4x-1)`, reducing to a clean,
**irreducible quartic** after stripping the trivial roots `x=\pm1` —
the pattern identified at `K=3,4,5` (no Galois obstruction; quartics
all the way) **continues unbroken at `K=6`**.

**A genuine new wrinkle, found and resolved (not merely predicted):**
`h_6(n,1)=-720/[(n-1)\cdots(n-5)]` is **negative** for `n>5` — matching
`K=4`'s sign, the opposite of `K=3,5`'s — so the **lower** bound is the
delicate direction at `x=1`. Exactly analogous to `K=4`'s own
lower-bound "wrinkle" (Estágio 48, `n\approx64.77`), the lower-target
resultant polynomial `S_2(n)` has a **genuine, confirmed** (not
spurious — verified by direct exact sign evaluation, not merely
suspected) real root strictly between `n=34` and `n=35`. Smaller in
magnitude than `K=4`'s `\approx64.77`, but the same phenomenon. Resolved
by the identical fix `K=4`'s predecessor used: an **exact per-integer-`n`
patch**, `n=8,\ldots,42`, confirming `|h_6(n,x)|\le M_6` exactly at
every one of those `35` integers — comfortably covering and exceeding
the confirmed root location — combined with a resultant-based rigorous
bound (no real root of `S_2(n)` exceeds `35`) and an explicit
continuity+IVT argument for the remaining real `n>35`. **No result is
weakened by this** — the constant is exactly `M_6`, the domain is
exactly `n\ge8`, matching the predicted `K+2` pattern precisely.

**A genuine, disclosed computational obstacle, distinct from the
mathematics: the straightforward continuation of `K=2,\ldots,5`'s own
recipe (`sp.factor_list` then `Poly.real_roots()` on the resulting
irreducible content) did not finish in practical time for `K=6`'s own
degree-`1052`/`1056` resultant polynomials**, across three different
attempted variants (`factor_list` first; `real_roots()` directly on the
raw polynomial; `real_roots()` on its square-free part), each running
`>4`–`>17` minutes without completing. This front pivoted to a
different exact technique — a Descartes'-rule-of-signs "positivity
after a Taylor shift" certificate, computed via `sympy`'s dedicated
`Poly.shift()` method (not generic `.subs()`, itself also too slow) —
which proves a rigorous upper bound on every real root of the
resultant polynomial in **a fraction of a second**, without ever
isolating the roots individually. This is disclosed in full as a
Self-caught issue (§7), not silently worked around.

**No closed-form CDF for `K=6` existed anywhere in the archive before
this front** (grep-confirmed: no `k6_full_cdf_attempt` sibling; Estágios
44/45 certify Gosper non-existence only for `K` symbolic). This front
derived Proposição D6 from scratch, instantiating the already-PROVED
general-`K` machinery at the concrete value `K=6`, self-validated by
reproducing D1–D5 **exactly, symbolically**, and independently confirmed
against a fresh, from-scratch exhaustive brute-force enumeration of
Definition 4 at `n=6,7` (`13/13` exact matches, `n=7` alone
`592{,}950{,}960` configurations).

**One bonus check honestly did NOT complete in available time:** the
`n=8` exhaustive-brute-force cross-check (`10.57` billion configurations,
`\approx8\times` the `K=5` predecessor's own completed `n=8` bonus
check) was attempted via multiprocessing but made negligible progress
(`0/32` chunks) under the compute budget actually available in this
session, and was abandoned in favor of completing the load-bearing
exact-closure proof itself (§6.2, §8) — this does **not** weaken the
theorem, whose domain (`n\ge8`) is established by the exact algebraic
argument above (§4–§5), independent of any brute-force check; the
brute-force checks at `n=6,7` plus the `mpmath` and dense float-grid
cross-checks (spanning `n=8` through `10^6`) remain the independent
verification for `D6` and the final bound respectively.

No Millennium Problem framing anywhere. Pure combinatorial mathematics
internal to this archive (the `u12` permutation-with-reroutes ensemble).

---

## 1. Reading discipline and provenance

Read in full, in this order, before any derivation:

1. `.../exact_algebraic_closure_attempt/k5_exact_closure_attempt/ATTEMPT.md`
   (immediate predecessor, wave 29 front c, integrated as `THEOREM.md`
   Estágio 53) — its EXACT method: deriving Proposição D5 from scratch by
   instantiating the cited general-`K` machinery at `K=5`, self-validating
   by reproducing D1–D4 exactly, cross-checking against exhaustive
   brute-force enumeration of Definition 4, extracting `g_5(x)`/`g_5'(x)`
   and their factorizations, finding `M_5` as a root of an irreducible
   minimal quartic, and the resultant-elimination construction for the
   exact upper/lower bounds and `n_0`.
2. `.../k5_exact_closure_attempt/adversarial/REFEREE_REPORT.md` — the
   referee's one LOW-severity finding, Finding F1: the predecessor's own
   write-up reported the largest real root of `S(n)`/`S_2(n)` using only
   the largest-*degree* factor `factor_list` isolates, without explicitly
   showing that the smaller cofactors don't hide a *larger* real root.
   The referee independently checked and confirmed they don't — no
   correctness impact, purely an expository gap. **This front's own §5.3
   addresses the identical concern from a different, arguably stronger
   angle: the shift-certificate method (§5.1–5.2) proves a bound on
   EVERY real root of the ENTIRE resultant polynomial directly, without
   ever splitting it into cofactors at all — so the "did a smaller
   cofactor hide something" question does not even arise for this
   front's own proof.**
3. `THEOREM.md` Estágio 46 (`D-SHARP-RATE-CONSTANTS-ATTEMPT`, the
   original "sum of sups" method and its diagnosed limitation), Estágio
   48 (`EXACT-ALGEBRAIC-CLOSURE-ATTEMPT`, `K=2,3,4` exact closure via
   resultant elimination — in particular its own `K=4` lower-bound
   "wrinkle," §4.5, and its §5.1 disclosed performance finding about
   `count_roots` vs `real_roots`, both directly relevant precedent for
   this front, see §5 and §7 below), and Estágio 53 (`K5-EXACT-CLOSURE-
   ATTEMPT`, this front's immediate predecessor) — read in full for the
   precise setup: `M_K`, `F_n^{(K)}(x)`, `F_K(x)`, `h(n,x)`, `D(n)`,
   `g_K(x)`, and how the pattern `n_0=K+2` has held for `K=2,3,4,5`.
4. `THEOREM.md` Definition 4 (lines 859–872) — the exact recursive
   definition of the discrete object (`f`, the permutation-with-`K`-
   reroutes functional graph; `T:=\#\{\text{cyclic points}\}`;
   `M_n^{(K)}:=T/n`) whose CDF is `F_n^{(K)}`.
5. Tracing back through the ancestor chain, `THEOREM.md` Estágios 40
   (`K3-FULL-CDF-ATTEMPT`, Proposição D3), 41 (`GENERAL-K-DECOMPOSITION-
   ATTEMPT`, Proposição S and the Full Cycle-Count Decomposition Theorem,
   proved for every `K`), 42 (`K2-FULL-CDF-ATTEMPT`, Proposição D2), 43
   (`K4-FULL-CDF-ATTEMPT`, Proposição D4), 44 (`GENERAL-K-CLOSED-CDF-
   ATTEMPT`) and 45 (`GENERAL-K-CDF-ALTERNATE-ROUTE-ATTEMPT`) — read in
   full. **Confirmed by grep across the whole archive: no closed-form CDF
   for concrete `K=6` exists anywhere** (no `k6_full_cdf_attempt` sibling
   directory next to `k3_full_cdf_attempt`; Estágios 44/45 certify
   non-existence only for `K` symbolic, explicitly leaving every concrete
   `K\ge5` open — and Estágio 44 §4.3 Part B reports, without exploiting
   it further, that the same summand IS Gosper-summable at every concrete
   `K` tested, **including `K=6` itself** ("K=6: found (non-`None`),
   11.5s")). This front reads that finding, exactly as the K=5
   predecessor did, as license to derive `D6(n,k)` concretely by
   instantiating the same already-PROVED general-`K` machinery at the
   fixed integer `K=6` — see §3.
6. The full prose of `general_k_decomposition_attempt/ATTEMPT.md`
   (Estágio 41's source — Proposição S, general `K`, and the Full
   Cycle-Count Decomposition Theorem, both PROVED `K`-free) and
   `general_k_closed_cdf_attempt/ATTEMPT.md` (Estágio 44's source — the
   exchangeability reduction to `S_r(n,K,k)` and the Layer-1 `InnerJ(V,O)`
   closed form, PROVED symbolic in `(n,K,r)`) — read in full for the
   precise, general-`K` formulas this front instantiates at `K=6`
   (§3.1) — **cited verbatim, never re-derived from first principles.**
7. `k3_full_cdf_attempt/ATTEMPT.md` (Estágio 40's source document) — its
   Definition-4 notation and conditional-CDF construction, read in full
   as the exact combinatorial vocabulary this lineage reuses.

**A precision note, checked explicitly rather than assumed.** A search
for any prior `K=6` work in the archive turns up one directory whose
name could be mistaken for overlap:
`.../theorem/k2_open_lemma/k3_attempt_2/k6_attempt/` (`DISC-DEC-033`,
an entirely different, older lineage). Its content was read far enough
to confirm it concerns a **different quantity**: `\psi_n^{(K)}`, the
"generic-point" piece of `THEOREM.md` §7.4's Open Lemma (the fixed-`K`
convergence bridge for the *mean* `\varphi_n^{(K)}`, via a `K`-uniform
Markov-chain/transfer-matrix method) — not `M_n^{(K)}=T/n`'s full CDF
(Definition 4, Proposição D`_K`), which is this front's (and every
`D1`–`D5` predecessor's) actual target. The two quantities are related
(`\varphi_n^{(K)}=E[M_n^{(K)}]` is one moment of the CDF this front
derives) but are not the same object, and that lineage's `K=6` closure
does not supply, and was not used to derive, Proposição D6 below. No
`.py` or `.md` file from that directory was read for content beyond
this scoping check.

**No `.py` file from any ancestor front was imported into this front's
own scripts.** The K=5 predecessor's `d5_derivation.py` and
`k5_exact_closure.py` were read, per the mandate, strictly as METHOD
reference (to confirm the precise resultant-elimination recipe and the
`r=0` `S_r` edge-case handling) — every script in this directory is
written completely fresh, with its own variable names, control flow,
and (for the `S_r`/`InnerJ` pipeline, the `r=0` edge case, and the
shift-certificate technique introduced at §5) its own from-scratch
reasoning, never a transcription of any predecessor's code.

---

## 2. Precise restatement of the target

For `K\ge0`, `M_n^{(K)}:=T/n` (Definition 4), `F_n^{(K)}(x):=P(M_n^{(K)}\le
x)`, `F_K(x):=1-(1-x^2)^K` (the continuum limit, PROVED for every `K\ge1`,
Estágio 24, cited). Writing `\Delta_n(x):=F_n^{(K)}(x)-F_K(x)` and
`h(n,x):=n\cdot\Delta_n(x)`, the target (matching every predecessor's own
statement exactly) is a genuine two-sided bound

```
-M_K  \le  h(n,x)  \le  M_K      for all x in [0,1], all integer n >= n_0,
```

with `M_K:=\max_{[0,1]}g_K(x)`, `g_K(x)` the `n\to\infty` leading
`1/n`-coefficient of `\Delta_n(x)` — at `K=6`, concretely: find the
*exact* algebraic value `M_6` and the smallest integer threshold `n_0`
such that `|F_n^{(6)}(x)-F_6(x)|\le M_6/n` holds for **every** integer
`n\ge n_0` and every `x\in[0,1]`, using the identical resultant-
elimination method (not a weaker "sum of sups" bound) that closed
`K=2,3,4,5` exactly. Predicted `n_0=8` (the `K+2` pattern) — **VERIFIED,
not assumed**, in §5.

---

## 3. Deriving `D6(n,k)`

### 3.1 Cited machinery (PROVED elsewhere, not re-derived)

From `general_k_decomposition_attempt/ATTEMPT.md` (Estágio 41) and
`general_k_closed_cdf_attempt/ATTEMPT.md` (Estágio 44), **cited
verbatim**:

```
P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O),  t:=k-O

InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N:=n-V-O   (r<K)
InnerJ(V,O) = n * C(N+r-1,r-1),                     N:=n-V-O   (r=K)
```

(`InnerJ` is Estágio 44's Layer-1 result, PROVED symbolic in `(n,K,r)`
via a Vandermonde-type convolution — the one genuinely hard step in the
general-`K` programme, already closed by a two-fronts-back predecessor
and reused here without modification.)

### 3.2 What this front adds: instantiation and closure at concrete `K=6`

Exactly as the K=5 predecessor found (and as this front independently
re-verified, not merely trusted): once `K` is fixed to a concrete
integer, `InnerJ(V,O)` is a **polynomial in `V`** of bounded degree, so
the `V`-sum and `O`-sum are classical Faulhaber power-sums that
`sp.summation` closes immediately and exactly — no Gosper certificate
needed, because a polynomial always has a polynomial antidifference.
The `r=0` edge case (no touched sources, so the touched total `V` is
forced to `0`) is handled here by direct evaluation,
`S_0(n,K,k)=\sum_{O=0}^kInnerJ(0,O,0,K,n)`, derived from first
principles in `d6_derivation.py`'s own docstring (not merely copied from
the predecessor's analogous remark).

`d6_derivation.py` implements this pipeline fresh (own `falling_choose`
helper, own `inner_j`/`s_r_of`/`cdf` functions).

**Self-validation (mandatory before trusting `K=6`): the identical
pipeline, run at `K=1,2,3,4,5`, reproduces the five independently-
already-established closed forms — Proposição D1 (Estágio 27), D2
(Estágio 42), D3 (Estágio 40), D4 (Estágio 43), and **D5 itself, cited
from the immediate predecessor's own `ATTEMPT.md` §3.3 (Estágio 53) —
not blindly trusted, but spot-checked here by this front's own
independent re-derivation of it from the same general machinery** — via
`sp.simplify(derived-cited)==0`, **exact zero symbolic difference in all
five cases**:

```
K=1 vs Proposicao D1 (Estagio 27): EXACT MATCH (diff=0).
K=2 vs Proposicao D2 (Estagio 42): EXACT MATCH (diff=0).
K=3 vs Proposicao D3 (Estagio 40): EXACT MATCH (diff=0).
K=4 vs Proposicao D4 (Estagio 43): EXACT MATCH (diff=0).
K=5 vs Proposicao D5 (Estagio 53, predecessor front, cited): EXACT MATCH (diff=0).
```

All five validations pass in `\approx10.8`s total. This is strong
evidence the pipeline — including both `InnerJ` branches (`r<K`, `r=K`)
and the `r=0` edge case — is implemented correctly, *before* it is ever
pointed at `K=6`. Full transcript: `d6_derivation.log`.

### 3.3 Proposição D6 (this front's own derivation, PROVED)

Running the same, unmodified pipeline at `K=6` (`\approx11.5`s):

> **Proposição D6 (`K=6` exact finite-`n` CDF).** For every `n\ge6` and
> every integer `0\le k\le n-1`:
> ```
> P(M_n^{(6)}<=k/n) = k(k+1)*Bracket6(n,k) / [n^7(n-1)(n-2)(n-3)(n-4)(n-5)]
> ```
> `Bracket6(n,k) = -k^10 + 25k^9 + 6k^8n^2 - 45k^8n - 270k^8 - 96k^7n^2
> + 760k^7n + 1650k^7 - 15k^6n^4 + 195k^6n^3 - 9k^6n^2 - 5380k^6n
> - 6273k^6 + 135k^5n^4 - 1875k^5n^3 + 4359k^5n^2 + 20734k^5n + 15345k^5
> + 20k^4n^6 - 330k^4n^5 + 1375k^4n^4 + 3600k^4n^3 - 22441k^4n^2
> - 47215k^4n - 24080k^4 - 80k^3n^6 + 1440k^3n^5 - 7975k^3n^4
> + 4641k^3n^3 + 50821k^3n^2 + 64330k^3n + 23300k^3 - 15k^2n^8
> + 270k^2n^7 - 1730k^2n^6 + 3435k^2n^5 + 7610k^2n^4 - 20391k^2n^3
> - 58916k^2n^2 - 50320k^2n - 12576k^2 + 15kn^8 - 310kn^7 + 2360kn^6
> - 7055kn^5 + 730kn^4 + 20526kn^3 + 33716kn^2 + 20016kn + 2880k
> + 6n^10 - 105n^9 + 720n^8 - 2375n^7 + 3384n^6 - 10n^5 - 1860n^4
> - 6696n^3 - 7440n^2 - 2880n`

This matches the established pattern exactly: denominator
`n^{K+1}(n-1)\cdots(n-K+1)` at `K=6` (`n^7(n-1)(n-2)(n-3)(n-4)(n-5)`);
bracket degree `2K-2=10` in `k` (full numerator degree, before dividing
out `k(k+1)`, is `2K=12`, matching D3/D4/D5's own pattern exactly).
Basic sanity identities, all confirmed exactly (§3.4): `P(T=n)=
1-D6(n,n-1)=6!/n^6=720/n^6` (matching the `K!/n^K` pattern of
Corollaries D3.1/D4.1/D5's own analogue exactly); `D6(n,0)=D6(n,-1)=0`
(structural `k(k+1)` factor); monotonicity in `k` for every `n`
spot-checked (`n=6,\ldots,10,12`).

### 3.4 Independent verification of `D6`

**(A) Symbolic sanity identities** (`d6_derivation.py`, §3.3 above): all
confirmed by exact `sp.simplify`, zero symbolic remainder.

**(B) Fresh, fully independent, fully-exhaustive brute-force Definition 4**
(`bruteforce_definition4_k6.py`, written from `THEOREM.md` Definition 4's
prose alone — enumerates literally **every** `n!\cdot n^6` pair
`(\pi,U)`, no reduced/decomposition model, no shortcut). `K=6` requires
`n\ge6` (fewer than 6 points cannot host 6 distinct reroute sources);
`n=5` is therefore out of Definition 4's domain for `K=6` and was not
attempted (confirmed by the model's own `assert 0<=K<=n` guard —
disclosed as Self-caught issue #2, §7):

```
n=6: k=0..5, all 6 match  (33,592,320 configurations, 39.5s)
n=7: k=0..6, all 7 match  (592,950,960 configurations, 804.7s)
```

`13/13` exact `Fraction` matches across `n=6,7`. Full transcript:
`bruteforce_definition4_k6.log`. (See §6.2, §8 for the `n=8` bonus
attempt's honest non-completion.)

---

## 4. `g_6(x)`, the critical point, and `M_6`

### 4.1 Extracting `g_6(x)`

Following the exact recipe used at `K=2,\ldots,5`: `\Delta_6(x):=
F_n^{(6)}(x)-F_6(x)` (substituting `k\to nx` into Proposição D6),
`N(n,x):=\Delta_6(x)\cdot D(n)` (`D(n)=n^7(n-1)(n-2)(n-3)(n-4)(n-5)`, the
cited denominator), `g_6(x):=` coefficient of `n^{11}` in `N(n,x)`
(`\deg_nD(n)-1=12-1=11`, exactly the established pattern):

```
g6(x) = -15x^12 + 24x^11 + 45x^10 - 90x^9 - 30x^8 + 120x^7 - 30x^6
        - 60x^5 + 45x^4 - 15x^2 + 6x
      = -3x(x-1)^5(x+1)^4(5x^2-3x+2)
```

`\deg_xg_6=12=2K` (matching `K=3`'s `\deg=6`, `K=4`'s `8`, `K=5`'s `10`
exactly). `5x^2-3x+2` has negative discriminant (`9-40=-31`), hence no
real roots and constant positive sign. On `[0,1]`: `x\ge0`,
`(x-1)^5\le0` (odd power of a non-positive base), `(x+1)^4>0`,
`(5x^2-3x+2)>0` — so the product `x(x-1)^5(x+1)^4(5x^2-3x+2)\le0` on
`[0,1]`, and the overall **leading `-3` sign flips it non-negative**:
`g_6(x)\ge0` on `[0,1]`, with equality only at the endpoints `x=0,1`
(confirmed directly: `g_6(0)=g_6(1)=0`), matching the sign pattern
already established at every `K=2,\ldots,5`.

### 4.2 `M_6`: critical point and minimal polynomial

```
g6'(x) = -6(x-1)^4(x+1)^3(30x^4-14x^3+x^2+4x-1)
```

— factors **cleanly**, exactly the pattern this front's mandate asked
about: after stripping the trivial roots `x=\pm1`, the interior
critical-point equation reduces to the **irreducible quartic**
`30t^4-14t^3+t^2+4t-1` (confirmed irreducible over `\mathbb Q` via
`sp.Poly(...).is_irreducible` — matching `K=3,4,5`'s `g_K'` exactly:
**no new algebraic obstruction appears at `K=6`**). `g_6'(x)` has 9 real
roots with multiplicity: `-1` (×3, matching `(x+1)^3`), `1` (×4,
matching `(x-1)^4`), and the quartic's own two real roots
(`-0.4554986190\ldots` and `0.2603617240\ldots`). The unique root in
`(0,1)`:

```
x_6^* = 0.26036172400671492484172362842265674...
M_6 := g_6(x_6^*) = 0.67967830129138512967160338683005533...
```

`M_6`'s own minimal polynomial (via `sp.minimal_polynomial`, independent
of the elimination route below):

```
35429400000000000 t^4 + 17921731935293824 t^3 - 248044660324924125 t^2
  + 350950285900800000 t - 137134080000000000
```

— degree 4, **irreducible over `\mathbb Q`** (confirmed,
`sp.Poly(...).is_irreducible`).

**Root selection, done correctly the first time** (per the archive's own
previously self-caught bug about `sp.solve`'s `.is_real` silently
dropping real roots on nested-radical output): `x_6^*` and `M_6` are
both obtained via `Poly(...).real_roots()`, never `sp.solve()`, and the
interior root is selected by the elementary numeric filter
`0<sp.N(x)<1` applied to the *exact* algebraic real roots — not by
evaluating a symbolic radical form at all. (The §5 boundary-threshold
computation was ALSO rewritten mid-development to avoid `sp.solve()`
entirely, after an early version crashed — Self-caught issue #4, §7.)

### 4.3 High-precision independent cross-check (`mpmath`, not `sympy`)

`k6_mpmath_crosscheck.py`: `g_6(x)` transcribed independently (both the
fully-expanded polynomial form and the factored form
`-3x(x-1)^5(x+1)^4(5x^2-3x+2)`, cross-checked against each other at
several points first — max discrepancy `2.3\times10^{-50}` at 50-digit
precision), the factored critical-point derivative independently
checked against a numerical derivative of `g_6` (max discrepancy
`1.6\times10^{-50}`), then the maximum on `[0,1]` found via a
`200{,}000`-point dense scan followed by `mpmath.findroot` Newton
polishing on `g_6'=0`, at `50` decimal digits of working precision —
**zero reliance on any `sympy` symbolic machinery**:

```
x6* (mpmath) = 0.260361724006714924841723628422656737985009135
M6  (mpmath) = 0.679678301291385129671603386830055333224986386
```

matching the `sympy`-derived values to `35+` digits
(`|\Delta|\approx3.2\times10^{-36}` for `M_6`, `\approx2.0\times10^{-36}`
for `x_6^*`). A dense-grid check confirms `M_6` is genuinely the global
maximum (worst excess over the `200{,}000`-point grid: `-2.0\times
10^{-11}`, negative as expected). Full transcript:
`k6_mpmath_crosscheck.log`.

---

## 5. Exact resultant elimination: upper and lower bounds

Identical construction to `K=2,\ldots,5`: `F_1:=\partial_xN(n,x)`,
`F_2:=m\cdot D(n)-n\cdot N(n,x)`, `R(n,m):=\mathrm{Res}_x(F_1,F_2)`;
eliminate `m` against `M_6`'s own minimal quartic (or, for the lower
bound, against the minimal polynomial of `-M_6`, obtained by `t\to-t`)
to get a single polynomial `S(n)` (upper) / `S_2(n)` (lower). `R(n,m)`
has degree `264` in `n`, `11` in `m` (`\deg_xN(n,x)=12`,
`\deg_nN(n,x)=11$ — `K=6`'s higher polynomial degree than `K=5`'s
`10`/`9`; `\approx21`s to compute). `S(n)` has degree `1052`; `S_2(n)`
has degree `1056`.

**Boundary threshold** (needed before §5.1–5.2): solving `h_6(n,1)=\pm
M_6` exactly via resultant elimination against `M_6`'s minimal
polynomial (never `sp.solve()` — Self-caught issue #4, §7):

```
n0_boundary = 7.278581437127420988290004...   (h6(n,1)=-M6 crossing)
```

matching the pattern that the boundary term alone almost pins the
domain: `7.28\ldots` rounds up to `8`, the predicted `K+2` threshold.

### 5.0 A disclosed methodological pivot: the shift certificate

The direct continuation of `K=2,\ldots,5`'s own recipe —
`sp.factor_list(S,n)` then `Poly.real_roots()` on the resulting
irreducible content — **did not finish in practical time** for `K=6`'s
`S(n)`/`S_2(n)`: three variants were each tried and abandoned after
`>4`–`>17` minutes without completing (full disclosure: §7, Self-caught
issue #5). This front instead used a different, still fully exact and
rigorous technique that needs no root isolation at all:

> **Shift certificate (Descartes' rule of signs after a Taylor
> shift).** For a polynomial `P(n)` with integer coefficients and an
> integer `B`: if every coefficient of `P(y+B)`, as a polynomial in
> `y`, shares one sign (all `\ge0` or all `\le0`, not all zero), then
> `P(n)\ne0$ for every real `n>B` (since `P(B+y)` is then a sum of
> terms of one sign for `y>0`, hence itself of that sign, hence
> nonzero) — in particular, `P` has **no real root exceeding `B`**.

Computed via `sympy`'s dedicated `Poly.shift(B)` method (a genuine
Taylor-shift algorithm — generic `.subs(n, y+B)` was independently tried
first and was **itself** too slow, taking `>4$ minutes without finishing
even on the already-reduced degree-`613` square-free part; `Poly.shift`
completes the same computation, on the full degree-`1052`/`1056`
polynomial, in **`0.05`–`0.2`` seconds** — a two-to-three-order-of-
magnitude difference, disclosed as Self-caught issue #5).

### 5.1 Upper bound (target `m=M_6`)

```
S(y+8) has uniform-sign coefficients (all negative) => S has NO real root exceeding 8.
```

PROVED, `0.13`s, no root isolation. Since "no real `x` at all
(unrestricted, not just `[0,1]`) makes `F_1=F_2=0`" trivially implies
"no real `x\in[0,1]`" does either, and no real `n>8` makes the
elimination-target equation hold at all, this rigorously rules out an
interior `[0,1]` critical point of `h_6(n,\cdot)` hitting `M_6` (or any
of its algebraic conjugates) for **every** real `n>8` — in fact for
`n\ge8`, since `S(8)` itself is one of the uniformly-signed (hence
nonzero) coefficients.

For documentation parity with `K=2,\ldots,5`'s own reported numeric
thresholds, exact-rational bisection (sign evaluation only, still no
isolation machinery, `k6_precise_thresholds.py`) locates the actual
largest real root of `S(n)`:

```
upper interior threshold (bisected) = 5.20773321842108316559...
```

— comfortably below both `8` (the rigorous shift-certificate bound
actually used) and the boundary threshold `7.28`, matching the
established `K=3,5` pattern that the boundary term alone pins the
domain in the upper direction.

Direct exact computation confirms `a(8):=\max_xh_6(8,x)=
0.2432251155193610422391695\ldots<M_6` (from the exact per-integer
patch of §6, run identically at `n=8`).

**Explicit continuity + IVT argument, stated completely:**
`a(n):=\max_{x\in[0,1]}h_6(n,x)` is continuous in real `n>5` (Berge's
Maximum Theorem: `h_6(n,x)` is a rational function of `(n,x)` with no
pole for real `n>5$, `x\in[0,1]$, so its max over the fixed compact set
`x\in[0,1]` is continuous in `n`). For real `n>8`, `a(n)` never equals
`M_6` (interior: shift certificate above; boundary: `h_6(n,1)<0<M_6$
trivially for all `n>5`). `a(n)` is continuous on `(8,\infty)` and
`a(8)<M_6` (checked exactly). A continuous function on a connected
interval that is never equal to a given value, and is strictly less
than that value at one point, is strictly less than it everywhere on
that interval (otherwise, by IVT, it would cross the value somewhere in
between). Hence `a(n)<M_6` for all real `n\ge8`.

> **UPPER-BOUND THEOREM (K=6, EXACT), proved.**
> `n\Delta_n(x)\le M_6` for all integer `n\ge8`, `x\in[0,1]`.

### 5.2 Lower bound (target `m=-M_6`): the genuine wrinkle

```
S2(y+8) uniform-sign: False.
```

Inconclusive at `B=8` — unlike every other bound at every other `K` in
this lineage. Scanning `B\in\{10,15,\ldots,40\}$ (each shift
`\approx0.2`s):

```
B=10..30: still mixed signs (inconclusive)
B=35: S2(y+35) has uniform-sign coefficients => NO real root of S2(n) exceeds 35.
```

**Confirmed genuine, not spurious**, by direct exact sign evaluation of
`S_2(n)` at consecutive integers (no root isolation, just polynomial
evaluation at integers — cheap and unambiguous):

```
S2(30)=-1  S2(31)=-1  S2(32)=-1  S2(33)=-1  S2(34)=-1  S2(35)=+1  S2(36)=+1
```

a genuine sign change strictly between `n=34` and `n=35` — refined by
exact-rational bisection (`k6_precise_thresholds.py`, `80` iterations)
to

```
lower interior threshold (bisected) = 34.77074391554775445456...
```

**This is a real, confirmed analogue of the K=4 predecessor's own
lower-bound "wrinkle"** (Estágio 48 §4.5, a spurious-looking large root
at `n\approx64.768366227610798420\ldots`) — smaller in magnitude here
(`\approx34.77` vs `\approx64.77`), same qualitative cause (a genuine
root of the resultant polynomial for this specific elimination branch
that does **not** correspond to an actual violation of the theorem, as
confirmed directly next), and the **same style of fix** the archive
already has precedent for.

**Resolution: exact per-integer-`n` patch, `n=8,\ldots,42`** (§6.1) —
comfortably covering and exceeding the confirmed root location —
confirms **zero violations** of `h_6(n,x)\ge-M_6` throughout, exactly
mirroring `K=4`'s own Step-7 fix (there, `n=6,\ldots,64`, `59` values;
here, `n=8,\ldots,42`, `35` values).

**Explicit continuity + IVT argument for the remaining real `n>35`,
stated completely, anchored on the exact patch:** `b(n):=
\min_{x\in[0,1]}h_6(n,x)` is continuous in real `n>5` (Berge). For real
`n>35`, `b(n)` never equals `-M_6` (interior: shift certificate at
`B=35`; boundary: `n_0^{\text{boundary}}=7.28<35`, trivially satisfied
there too). `b(n)` is continuous on `(35,\infty)` and `b(42)=
-0.0001567668061987653131166112\ldots>-M_6` (checked exactly, §6). By
IVT, `b(n)>-M_6` for **all** real `n>35`. Combined with the direct exact
check at **every** integer `n=8,\ldots,42$ (§6.1, which independently
covers `n=35,\ldots,42$ too, and additionally covers `n=8,\ldots,34`),
this closes `b(n)>-M_6` for **every** integer `n\ge8`.

> **LOWER-BOUND THEOREM (K=6, EXACT), proved.**
> `n\Delta_n(x)\ge-M_6` for all integer `n\ge8`, `x\in[0,1]`, via the
> exact per-integer patch (`n=8,\ldots,42`) plus the shift-certificate
> interior bound (`B=35`) plus the continuity+IVT argument for
> `n>35`.

### 5.3 Pre-emptive resolution of the K=5 predecessor's Finding F1

The K=5 predecessor's referee flagged (LOW severity, purely
expository) that its write-up reported the largest real root of
`S(n)`/`S_2(n)` from only the largest-degree factor `factor_list`
isolated, without an explicit check that a smaller cofactor didn't hide
a larger real root. **This front's method makes that question moot by
construction**: the shift certificate (§5.0–5.2) proves a bound on
every real root of the **entire, unfactored** polynomial `S(n)`/`S_2(n)`
directly — it was never split into cofactors at all, so there is no
smaller piece that could hide anything. This is arguably a strictly
stronger and more direct resolution of the same underlying concern than
a per-cofactor check would be.

### 5.4 Combined: `n_0` for `K=6`

```
n0_boundary        = 7.278581437127420988290004...   (h6(n,1)=-M6 crossing)
n0_upper_interior   < 8    (rigorous, shift certificate; bisected value 5.2077...)
n0_lower_interior   < 35   (rigorous, shift certificate; bisected value 34.7707...)
```

The upper bound and the boundary term alone would give `n_0=8`
(matching `K=3,5`'s clean pattern); the lower bound's own interior
threshold (`<35`) is resolved not by a continuous threshold argument
alone but by the exact per-integer patch (`n=8,\ldots,42`) plus IVT for
`n>35` (§5.2) — **the same two-part structure `K=4`'s own lower bound
needed**, confirming this is a real feature of the method at boundary-
sign-negative `K` values (`K=4,6`), not an accident specific to one `K`.

```
n0 := 8   (matches the predicted K+2 pattern exactly, verified not assumed)
```

Direct exact per-integer verification (§6.1) additionally confirms
`n=7` **violates** (the boundary crossing `7.28` sits strictly between
`7` and `8`, and the dense float-grid cross-check §6.4 independently
confirms `h_6(7,1)=-1<-M_6\approx-0.6797`, a genuine violation) —
pinning `n_0=8` exactly, not merely as an upper bound.

> **THEOREM (K=6, EXACT).** For all integer `n\ge8` and `x\in[0,1]`:
> `|F_n^{(6)}(x)-F_6(x)|\le M_6/n`, `M_6=0.67967830129138512967\ldots`
> (exact real root of
> `35429400000000000t^4+17921731935293824t^3-248044660324924125t^2+350950285900800000t-137134080000000000`).
> This matches `K=2,3,4,5`'s tier of closure exactly — the fifth
> consecutive `K` (after `K=2,3,4,5`) closed by this method, with a
> confirmed but fully-resolved lower-bound wrinkle at `K=6` (matching
> `K=4`'s), and no wrinkle at `K=3,5`.

---

## 6. Numerical verification (fresh scripts, real logged output)

All scripts below are written fresh for this front; none imports any
ancestor's code. Every non-trivial symbolic claim is machine-checked
with `assert` statements inline (matching this archive's mandatory
discipline).

### 6.1 Exact per-integer-`n` patch (`k6_exact_patch_n8_42.py`/`.log`)

`n=8,\ldots,42` (`35` values): exact computation of
`\max_xh_6(n,x)`/`\min_xh_6(n,x)` via `Poly(dh_6/dx,x).real_roots()` at
each fixed integer `n` (a small, fast, per-`n` computation — degree-`12`
polynomial, not the full symbolic-`n` machinery). **All `35` values
confirm `-M_6\le h_6(n,x)\le M_6$ exactly** (`100.7`s total [^f1]). Worst
(smallest) margin: `0.3749` at `n=8` (comfortably strict, not a
near-miss). Full transcript: `k6_exact_patch_n8_42.log`.

[^f1]: **[Nota, 2026-08-29 — referee hostil, wave 30
`K6-EXACT-CLOSURE-ATTEMPT`]** This `100.7`s figure and the "Full
transcript: `k6_exact_patch_n8_42.log`" citation next to it are
mismatched: that log's own printed total is `104.7`s; the `100.7`s
figure actually appears in `k6_exact_closure.log`'s Step 6 (a separate
run of the identical deterministic computation). Both numbers are
genuine — two runs naturally differ in wall-clock time — and the
underlying per-`n` max/min `h_6` values are byte-identical between the
two logs. A citation slip (wrong source named for a timing figure), not
a computational error. See `adversarial/REFEREE_REPORT.md`, Finding F1.

### 6.2 Fresh, fully exhaustive brute-force Definition 4
(`bruteforce_definition4_k6.py`/`.log`)

`n=6,7`: `13/13` exact matches (§3.4). `n=6`: `33{,}592{,}320`
configurations, `39.5`s (`850{,}984` cfg/s). `n=7`: `592{,}950{,}960`
configurations, `804.7`s (`736{,}890` cfg/s) — a genuine, disclosed
`\approx13\%` throughput drop from `n=6` to `n=7` (not smoothed over),
consistent with the K=5 predecessor's own disclosed cross-`n`
throughput spread.

**`n=8` bonus attempt: honestly did not complete.** `n8_attempt_k6.py`
targeted `8!\times8^6=10{,}569{,}646{,}080` configurations
(`\approx8\times` the K=5 predecessor's own completed `n=8` bonus check,
`1{,}321{,}205{,}760`). Parallelized across this environment's `4` CPU
cores via `multiprocessing.Pool` (`32` contiguous permutation chunks,
`\approx1260` permutations each) — the enumeration itself was
unchanged (still every one of the `10.57` billion `(\pi,U)` pairs, no
shortcut), only the outer loop over `\pi` distributed across processes.
Across `\approx45$ minutes of session wall-clock time (much of it under
CPU contention with the resultant-elimination computation, which was
prioritized as the load-bearing result), the attempt completed **`0`
of its `32` chunks**. It was stopped and **honestly reported as
attempted-but-not-completed**, not silently dropped or claimed
successful — matching this lineage's own convention for honest
non-closure (e.g., the K=5 predecessor's own two-attempt disclosure for
its smaller `n=8` check, and Estágio 44/45's Gosper non-existence
disclosures). This does **not** weaken the theorem: `D6`'s domain
`n\ge8` proof (§5) is a fully exact algebraic argument independent of
any brute-force check; the `n=6,7` exhaustive checks plus the `mpmath`
and dense float-grid cross-checks (§6.3–6.4, spanning `n=8` through
`10^6`) remain the independent, non-symbolic verification.

### 6.3 High-precision independent cross-check (`k6_mpmath_crosscheck.py`/`.log`)

`M_6`, `x_6^*` reproduced via `mpmath` (50 decimal digits), zero reliance
on `sympy` symbolic machinery, matching the `sympy`-derived values to
`35+` digits (§4.3).

### 6.4 Dense float-grid cross-check (`k6_float_grid_crosscheck.py`/`.log`)

Independent, non-`sympy`, raw-floating-point code path (own from-scratch
transcription of `D6`, not the `Num6`/`Poly` machinery used elsewhere).
Negative control: `n=6,7` (below the claimed domain) both show genuine
violations, precisely at the boundary `x=1` (`h_6(6,1)=-6`,
`h_6(7,1)=-1`, both `<-M_6\approx-0.6797`) — confirming the LOWER bound,
not the upper, is what fails just below the domain, consistent with
§5's negative-boundary-sign diagnosis. Integer sweep `n=8,\ldots,2000`;
geometric sweep `n=2000,\ldots,10^6` (`200` points); `4001`/`801`/`401`
-point `x`-grid per `n`. **Zero violations** anywhere in the claimed
domain `n\ge8` — including throughout the `n=8,\ldots,42` range where
the resolved lower-bound wrinkle lives, and well past `n=42` up to
`10^6`; closest approach to the bound `\approx-4.78\times10^{-6}` at
`n=10^6`, `x\approx0.26` (near `x_6^*`); `h_6(10^6,x_6^*)/M_6=
0.99999427`, approaching `1` from below as expected.

### 6.5 Precise threshold values (`k6_precise_thresholds.py`/`.log`, `k6_shift_certificate_scan.py`/`.log`)

Exact-rational bisection (sign evaluation only) locating the actual
largest real roots reported in §5.1–5.2 (`5.2077\ldots$ upper,
`34.7707\ldots$ lower), and the scan across `B\in\{12,\ldots,300\}$
that first located the lower-target wrinkle's approximate range
(`(30,40]`, refined to `(34,35)` by direct integer evaluation) before
the precise bisection.

---

## 7. Self-caught issues (honest disclosure)

1. **Wrong `assert deg_k == 10` in `d6_derivation.py`'s own structural
   sanity check, caught immediately by the assertion firing.** The
   script initially asserted the FULL numerator's degree in `k` (before
   dividing out the structural `k(k+1)` factor) equals `2K-2=10`
   (confusing it with the *bracket*'s degree). The full numerator's
   actual degree is `2K=12` (matches D3/D4/D5's own numerator-degree
   pattern exactly). Fixed by explicitly dividing the numerator by
   `k(k+1)` (`sp.div`) to obtain `Bracket6` in its own right, degree
   `10=2K-2` as expected. No numeric or symbolic value was ever wrong —
   only the diagnostic assertion's target was momentarily mislabeled.
2. **`bruteforce_definition4_k6.py`'s first run crashed at `n=5`**
   (`assert 0<=K<=n` firing), because `K=6>5` — `n=5` cannot host `6`
   distinct reroute sources under Definition 4 (unlike `K=5`, whose
   predecessor could test `n=5`). Not a bug: Proposição D6's own
   domain starts at `n\ge6`. Fixed by starting the sweep at `n=6`. **[Nota,
   2026-08-29 — referee hostil, wave 30 `K6-EXACT-CLOSURE-ATTEMPT`]**
   The fix as actually applied lives in how the script was *invoked*
   (explicit command-line arguments), not in the script's own code: its
   default-argument fallback (line 125) is still `[5,6,7]`, which would
   reproduce the exact disclosed crash if run today with no arguments.
   The logged run only processed `n=6,7`, confirming explicit arguments
   were used in practice — no wrong result was ever produced — but the
   disclosure's phrasing is slightly imprecise about where the fix
   resides. See `adversarial/REFEREE_REPORT.md`, Finding F3.
3. **A second, distinct failure at `k=n` in the SAME initial brute-force
   run, caught by cross-referencing the domain statement of D1–D5.**
   `D6(n,n)` evaluates to `0` via the rational-function formula, but
   `P(T\le n)=1` trivially — the same, already-documented phenomenon
   the K=5 predecessor's own §7 disclosed for `D5`. Fixed by restricting
   the per-`k` match loop to `0\le k\le n-1` and checking `k=n`
   separately via `1-D6(n,n-1)=6!/n^6`.
4. **`k6_exact_closure.py`'s first version of the boundary-threshold
   computation crashed with `ValueError: max() arg is an empty
   sequence`, caught immediately by the crash itself.** Two layers,
   both diagnosed before any threshold number was trusted: **(a)** the
   code used `sp.solve()` on a quintic with an algebraic coefficient
   `M_6`, and its `.is_real` filter discarded every root — the SAME
   class of bug the archive first self-caught at Estágio 46. **(b)**
   independently, the equation was also the WRONG one for `K=6`'s sign
   pattern: unconditionally solving `h_6(n,1)=M_6` (upper-target),
   but at `K=6` — unlike `K=3,5` — the boundary term is negative, so
   the relevant crossing is `h_6(n,1)=-M_6` (lower-target). Fixed by
   rewriting the computation as a resultant elimination against `M_6`'s
   minimal polynomial (matching §5's own `sp.solve`-free convention),
   computed generically for both possible target signs, then taking the
   larger of the two relevant real roots.
5. **The central, largest computational obstacle this front hit: the
   direct continuation of `K=2,\ldots,5`'s own `factor_list`-then-
   `real_roots` recipe did not finish in practical time for `K=6`.**
   Disclosed in full, not silently worked around:
   - **Attempt A** (`factor_list(S,n)` first, matching every prior `K`
     exactly): ran **`>17` minutes** without completing on `S(n)`
     (degree `1052`); killed.
   - **Attempt B** (`Poly(S,n).real_roots()` directly on the raw,
     unfactored polynomial, reasoning that `real_roots()` uses
     square-free decomposition internally rather than full irreducible
     factorization): ran **`>4$ minutes** without completing; killed.
     **This hypothesis, checked against the archive's own existing
     precedent (`exact_algebraic_closure_attempt/ATTEMPT.md` §5.1, the
     K=4 predecessor's own disclosed performance finding), turned out to
     be backwards**: that document explicitly recorded "prefer
     `Poly.real_roots()` (full) over `Poly.count_roots(inf=...,
     sup=...)`" and found the full, unbounded `real_roots()` on an
     already-factored **irreducible** content fast (`7.9`s for a
     degree-`216` factor) — the lesson was about avoiding
     semi-infinite-interval queries on an *already-reduced* polynomial,
     not about skipping `factor_list` altogether on the *raw* one. This
     front's Attempt B skipped the reduction step entirely, which is
     precisely what the K=4 precedent, read carefully, did not
     recommend.
   - **Attempt C** (`Poly.sqf_part()` — square-free reduction, a cheap
     GCD operation, `0.4`s, degree `1052\to613` — followed by
     `real_roots()` on the reduced polynomial): still ran **`>4`
     minutes** without completing; killed. The degree reduction alone
     was insufficient — the bottleneck is plausibly the astronomically
     large integer coefficients (`S(n)`'s coefficients run to `\sim1800`
     decimal digits, per direct inspection in §5.2's integer-evaluation
     step [^f4]), not the degree, matching neither this front's degree-based
     hypothesis nor a pure multiplicity-based one cleanly.

[^f4]: **[Nota, 2026-08-29 — referee hostil, wave 30
`K6-EXACT-CLOSURE-ATTEMPT`]** Independently confirmed the `~1800`-digit
magnitude is accurate, but it describes an *evaluated value* (e.g.
`S_2(35)` has `1918` digits, exactly §5.2's integer-evaluation
computation), not `S(n)`'s raw stored polynomial *coefficients* — those
top out around `543` digits. "Coefficients" is a loose description of
what is actually an evaluated value; the claimed magnitude itself is
correct. See `adversarial/REFEREE_REPORT.md`, Finding F4.
   - **Re-reading the K=4 precedent (`exact_algebraic_closure_attempt/
     ATTEMPT.md` §5.1) a second time, more carefully**, after Attempts
     B and C both failed, confirmed `factor_list` genuinely was the
     right general direction (full `real_roots()` on the *reduced,
     irreducible* content was what was fast for K=4) — but K=6's
     `factor_list` itself (Attempt A) was already the slow step, unlike
     K=4's (where the reproducibility note records the **whole**
     pipeline, resultant+`factor_list`+`real_roots`, at `20$–`60`s).
     This front concluded `K=6`'s specific polynomials are genuinely
     harder for `sympy`'s default integer-polynomial factorization
     algorithm (plausibly due to coefficient size, not degree or
     multiplicity structure alone), not that the general method had
     failed. **Resolution: switched techniques entirely** rather than
     tuning the same one further — the shift certificate (§5.0),
     which sidesteps root isolation (and hence factorization)
     altogether. Its first implementation used generic `S.subs(n,
     y+B)` + `sp.expand`, which was **itself** too slow (`>4$ minutes,
     killed, on the already-reduced degree-`613` polynomial from
     Attempt C) — switched to `sympy`'s dedicated `Poly.shift(B)`
     method (a genuine Taylor-shift algorithm, not generic symbolic
     substitution), which completed the identical mathematical
     operation, on the full **un-reduced** degree-`1052`/`1056`
     polynomial, in `0.05`–`0.2`s — confirming the bottleneck really
     was `sympy`'s generic-substitution codepath, one further instance
     of the SAME general lesson the K=5 predecessor's own Self-caught
     issue #3 named ("prefer sympy's most literal/explicit
     computational path over its most 'elegant' one when performance
     matters") — now a third independent confirmation of that lesson
     in this lineage (K=4's `count_roots`; K=5's `sp.summation` with
     unexpanded `sp.binomial`; K=6's generic `.subs()`-based shift).
     No numeric threshold was ever reported or used from any of the
     killed attempts — each crash/timeout was caught and disclosed
     before any conclusion was drawn.
6. **A scratchpad file-collision, unrelated to the mathematics, caught
   mid-session and disclosed here for full transparency.** While
   drafting this document, the session's own working copy of
   `ATTEMPT.md` in its private scratch directory was found to have been
   silently overwritten with content from an entirely different,
   unrelated wave-30 front (`ROUTE2-BYPASS-ATTEMPT`, about `C(\gamma)`).
   This was an environment-level filesystem collision (multiple
   parallel front sessions apparently able to write to a
   same-named-file, despite each nominally having a session-specific
   scratch path), not any error in this front's own reasoning or
   computation — no mathematical content of this front was lost, since
   every number and derivation had already been independently logged to
   `.py`/`.log` files in this front's own permanent archive directory
   before the collision occurred. This document was reconstructed and,
   from that point on, authored directly in this front's own permanent
   archive directory rather than the shared scratch space.

---

## 8. What remains open (honest disclosure)

- **The `K=4`-style lower-bound wrinkle WAS needed at `K=6`** (§5.2) —
  confirmed, not merely a theoretical possibility. Fully resolved by
  the exact per-integer patch (`n=8,\ldots,42`) plus the shift-
  certificate interior bound plus continuity+IVT, exactly mirroring
  `K=4`'s own fix; the final constant (`M_6`, exact) and domain
  (`n\ge8`) are **not weakened** by this — the wrinkle is a feature of
  which resultant-elimination branch a particular target/sign
  combination lands on, not a weakening of what is provable.
- **The `n=8` exhaustive brute-force bonus check (§6.2) did not
  complete** in the compute budget available in this session
  (`0/32$ chunks of a `10.57`-billion-configuration enumeration). This
  is honestly disclosed, not silently dropped or claimed successful.
  It does not weaken the theorem, whose `n\ge8` domain rests on the
  exact algebraic argument of §5, independent of brute force; the
  `n=6,7` exhaustive checks (§3.4, §6.2) plus the `mpmath` and dense
  float-grid cross-checks (§6.3–6.4, `n=8` through `10^6`) remain the
  independent, non-symbolic verification actually completed. A future
  front with more compute budget, or a smarter parallelization
  strategy (e.g. distributing across more cores, or a compiled
  extension for the inner cycle-counting loop), could complete this
  bonus check; it is not required for the theorem itself.
- **`K=6`'s own closed-form CDF (Proposição D6, §3.3) is this front's
  own new derivation, not yet independently reviewed by a hostile
  referee** — the identical disclosure the K=5 predecessor made for
  `D5` at the analogous point. Validated here by reproducing `D1`–`D5`
  exactly (symbolic) plus a `13`-point exhaustive brute-force
  cross-check (`n=6,7`) — strong evidence, not yet the multi-front
  adversarial process this archive applies to a standalone CDF result.
  This front's own mandate is the rate constant, not a
  `K6-FULL-CDF-ATTEMPT` in its own right.
- **`K\ge7` was not attempted.** Whether the "clean quartic after
  stripping `x=\pm1`" pattern (now confirmed at `K=2,\ldots,6`)
  continues indefinitely, whether the boundary-term sign continues
  alternating in some pattern (`K=3,5`: positive; `K=4,6$: negative —
  an alternating-by-two pattern visible now across four data points,
  suggestive but unproven as a general fact [^f6]), and whether the
  "wrinkle" magnitude (`K=4$: `\approx64.77`; `K=6$: `\approx34.77` —
  *decreasing*, not increasing, with `K$, contrary to a naive
  "harder problems get harder" expectation) follows any predictable
  trend, all remain open, verified only by direct computation at
  `K\le6`, not by any structural argument extending to general `K`.

[^f6]: **[Nota, 2026-08-29 — referee hostil, wave 30
`K6-EXACT-CLOSURE-ATTEMPT`]** This framing undersells what is already on
record: the immediate predecessor's own `ATTEMPT.md` §5.3 (part of this
front's own mandatory reading) already states the general closed form
`h_K(n,1)=(-1)^{K+1}K!/[(n-1)\cdots(n-K+1)]`, whose sign manifestly
alternates with **every** unit increase in `K` (not merely "by two," and
not an empirical coincidence across four spot-checked values) —
independently confirmed to continue holding exactly at `K=6`:
`h_6(n,1)=(-1)^7\cdot720/[(n-1)\cdots(n-5)]=-720/[(n-1)\cdots(n-5)]`,
matching exactly. Nothing false was claimed — a fully general, `K`-free
*proof* of this formula is indeed not on record — but the "suggestive...
unproven" phrasing reads more tentative than warranted given the
front's own cited source already supplies the explanation. See
`adversarial/REFEREE_REPORT.md`, Finding F6.

- **The `n_0=8` threshold was not shown to be the best possible.** As
  at `K=3,4,5`, no attempt was made to find a sharper threshold via a
  different route.
- **The shift-certificate technique introduced here (§5.0) was not
  benchmarked against `factor_list` at `K=2,\ldots,5`** to see whether
  it would have been faster there too (plausible, given its dramatic
  speed advantage at `K=6`) — left as a natural methodological
  question for any future front revisiting this lineage's performance
  characteristics, not attempted here since `K=2,\ldots,5` are already
  closed and re-deriving them was out of this front's scope.

## 9. Scorecard

| # | Item | Status |
|---|---|---|
| 1 | Pipeline self-validation: reproduces `D1,...,D5` exactly (symbolic) | **PASS** (zero symbolic difference, all five) |
| 2 | Proposição D6 (`K=6` exact finite-`n` CDF) derived | **DERIVED**, this front's own work, cited machinery only |
| 3 | `D6` vs fresh exhaustive brute-force Definition 4, `n=6,7` | **PASS**, `13/13` exact matches |
| 4 | `D6` vs exhaustive brute-force Definition 4, `n=8` (bonus) | **NOT COMPLETED** (`0/32` chunks; honestly disclosed, §6.2/§8; does not weaken the theorem) |
| 5 | `g_6(x)` extracted, factors as `-3x(x-1)^5(x+1)^4(5x^2-3x+2)`, `\ge0` on `[0,1]` | **CONFIRMED** |
| 6 | `g_6'(x)` factors to a clean irreducible quartic after stripping `x=\pm1` | **CONFIRMED** — same tier as `K=3,4,5`, no new Galois obstruction |
| 7 | `M_6` exact value + irreducible minimal quartic | **PROVED**, cross-checked via independent `mpmath` (35+ digits) |
| 8 | `K=6` upper bound `n\Delta_n(x)\le M_6`, all real `n\ge8` | **PROVED EXACTLY** (shift-certificate: no root of `S(n)` exceeds `8`, + boundary + explicit IVT) |
| 9 | `K=6` lower bound `n\Delta_n(x)\ge-M_6`, all real `n\ge8` | **PROVED EXACTLY** — genuine `K=4`-style wrinkle found (root `\in(34,35)`), resolved by exact per-integer patch (`n=8..42`) + shift-certificate bound (`<35`) + IVT for `n>35` |
| 10 | Explicit continuity+IVT argument stated completely, from the start | **DONE**, for both bounds |
| 11 | Pre-emptive resolution of the K=5 predecessor's referee Finding F1 | **DONE**, by construction — shift certificate bounds the entire unfactored polynomial directly, no cofactor-hiding question can arise |
| 12 | Independent `mpmath` high-precision cross-check of `M_6`, `x_6^*` | **PASS**, 35+ digit agreement |
| 13 | Independent dense float-grid cross-check, `n=6,7` (negative control) and `n=8,\ldots,10^6` | **PASS**, zero violations in domain; correctly flags `n=6,7` as violations |
| 14 | Exact per-integer-`n` patch, `n=8,\ldots,42` | **PASS**, zero violations, `100.7`s |
| 15 | Core mandate question: does `K=6` reveal a genuine new algebraic obstruction? | **ANSWERED: NO** in the Galois/radical sense (quartic factors cleanly); **YES** in the "resultant-elimination branch structure" sense — a confirmed, resolved `K=4`-style wrinkle, the genuinely new finding of this front |
| 16 | `factor_list`-based root isolation, direct continuation of `K=2..5`'s method | **DID NOT COMPLETE** in practical time (3 variants, `>4`–`>17` min each); superseded by the shift-certificate method (§5.0), fully disclosed (§7 issue #5) |
| 17 | `K\ge7` generalization | **NOT ATTEMPTED**, flagged as future work (§8) |

## 10. File manifest

| File | Role |
|---|---|
| `d6_derivation.py` / `.log` | Derives Proposição D6 from the general-`K` machinery (Estágios 41/44, cited), self-validated by reproducing `D1`–`D5` exactly first. |
| `bruteforce_definition4_k6.py` / `.log` | Fresh, fully exhaustive brute-force Definition 4 (K=6) engine + cross-check at `n=6,7`. |
| `k6_mpmath_crosscheck.py` / `.log` | Independent `mpmath` high-precision (50-digit) cross-check of `M_6`, `x_6^*`, zero `sympy` symbolic machinery. |
| `k6_exact_closure.py` / `.log` | The main, final, consolidated proof: `g_6`, `M_6`, boundary values, both resultant eliminations, the shift-certificate root bounds, the exact per-integer patch, explicit continuity+IVT arguments, final theorem. Self-contained, asserts every claim inline. |
| `k6_shift_certificate_scan.py` / `.log` | Exploratory scan across shift bounds `B` that first located the lower-target wrinkle's approximate range `(30,40]`. |
| `k6_exact_patch_n8_42.py` / `.log` | The exact per-integer-`n` patch, `n=8,\ldots,42`, resolving the lower-bound wrinkle. |
| `k6_precise_thresholds.py` / `.log` | Exact-rational bisection locating precise decimal values for both interior thresholds (documentation parity with `K=2,\ldots,5`'s own reported numbers). |
| `k6_float_grid_crosscheck.py` / `.log` | Independent, non-`sympy`, dense float-grid stress test, `n=6,7` (negative control) and `n=8,\ldots,10^6` (claimed domain). |
| `n8_attempt_k6.py` / `n8_attempt_k6_incomplete.log` | The `n=8` exhaustive-brute-force bonus-check engine (multiprocessing, validated correct via a dry run at `n=6` matching `bruteforce_definition4_k6.py` exactly [^f2] — see §7 discussion) — kept for transparency and reproducibility even though it did **not** complete (§6.2, §8): the log shows only its startup header (`0/32` chunks finished) at the point this front stopped it to prioritize the load-bearing proof. Not required for the theorem. Its own final `print` statement references a `n8_crosscheck_k6.py` cross-check file [^f5] that does not exist in this directory and is never invoked (the run never reached that point). |

[^f2]: **[Nota, 2026-08-29 — referee hostil, wave 30
`K6-EXACT-CLOSURE-ATTEMPT`]** As delivered, no dry-run log actually
existed anywhere in this front's own directory to back this claim (only
`n8_attempt_k6_incomplete.log`, the 120-byte startup header of the
never-completed `n=8` attempt) — a real, if minor, gap against this
archive's own discipline of persisting every claim to a log. The
referee independently performed exactly this dry run (patching `N=8→6`
into an unmodified copy of this front's own multiprocessing engine) and
**confirms the underlying claim is true**: the engine produces the
identical counts array as both this front's own logged `n=6` run and
the referee's own independent `n=6` brute force — the multiprocessing
chunking logic genuinely is correct and would have produced the right
answer had the `n=8` run completed. See
`adversarial/REFEREE_REPORT.md`, Finding F2, and its
`adv5_n8_engine_dryrun_at_n6.py`/`.log`.

[^f5]: **[Nota, 2026-08-29 — referee hostil, wave 30
`K6-EXACT-CLOSURE-ATTEMPT`]** Harmless: since the `n=8` run never
completed, this line never actually printed in the logged (incomplete)
run, and no claim anywhere in this document depends on the referenced
file existing. A vestigial reference to a filename from an earlier
planning pass, worth cleaning up in a future revision. See
`adversarial/REFEREE_REPORT.md`, Finding F5.

## 11. Scope-discipline confirmation

All new files created **only** inside this front's own directory:
`.../k5_exact_closure_attempt/k6_exact_closure_attempt/`. No
`adversarial/` subdirectory created (no referee dispatched by this
front, per mandate). No file inside `k5_exact_closure_attempt/` (the
predecessor's own directory) or any other ancestor directory was
modified — all read-only. No `git` command of any kind was run.
`THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`, `README.md`, `index.html`
were **not** modified. Re-confirmed at the end of this front's work:
`ls` of this directory shows only files listed in §10 above, all
inside this front's own new subdirectory.

## 12. Seeds

Reserved block for this front: `20260946000`–`20260946999` (`DISC-DEC-138`,
front (b)).

**Grep-confirmed unused before first use:**
```
$ grep -rn "20260946" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8981:      20260946000-20260946999 (frente b), 20260947000-20260947999
```
(only the reservation notice itself, `DISC-DEC-138`'s own text —
confirmed unused elsewhere.)

**No randomness was needed anywhere in this front's work** — every
result is either exact symbolic/algebraic computation (`sp.resultant`,
`Poly(...).real_roots()`, the shift-certificate technique, exact
rational/integer arithmetic), exact exhaustive enumeration (the
brute-force Definition-4 cross-check at `n=6,7`), or a deterministic
dense grid / `mpmath` polish (§6.3–6.4) — matching every `K=2,3,4,5`
front in this exact style. The `n=8` multiprocessing bonus attempt used
no randomness either (deterministic partitioning of the permutation
set). The reserved seed block is recorded here per the mandate's
instruction, unused, exactly as the predecessor fronts also found no
randomness necessary.
