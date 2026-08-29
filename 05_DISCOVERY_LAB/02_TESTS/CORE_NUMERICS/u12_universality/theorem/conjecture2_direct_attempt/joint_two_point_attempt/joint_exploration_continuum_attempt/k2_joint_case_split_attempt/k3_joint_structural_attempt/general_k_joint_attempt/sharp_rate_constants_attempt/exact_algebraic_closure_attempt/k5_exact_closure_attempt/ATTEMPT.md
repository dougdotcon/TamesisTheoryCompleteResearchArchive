# K5-EXACT-CLOSURE-ATTEMPT (wave 29, front c)

**Mandate** (`DISC-DEC-134`, `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`):
the immediate predecessor (`exact_algebraic_closure_attempt/ATTEMPT.md`,
wave 26 front b, integrated as `THEOREM.md` Estágio 48) achieved EXACT
finite-`n` closure of the sharp rate constant `M_K` for `K=3` (`n\ge5`)
and `K=4` (`n\ge6`), via exact resultant elimination against `M_K`'s own
minimal polynomial, diagnosing the prior "sum of sups" method's failure
(Estágio 46) as a sign issue in the tail-bound comparison, not a
Galois/radical obstruction — both `g_3',g_4'` factor cleanly into
irreducible quartics after stripping trivial roots `x=\pm1`. Estágio 48
explicitly flagged `K\ge5` as untested ("apenas `K\ge5` permanece fora do
escopo desta linha"). This front's mandate: extend the resultant-
elimination method to `K=5` — find the exact algebraic `M_5` and the
finite-`n` threshold `n\ge n_0` for which exact closure holds, using the
same method that closed `K=3,4`, honestly reporting any genuine new
obstruction `K=5` might reveal.

## 0. Executive summary

**Outcome: full exact closure, `K=5`, `n\ge7`.**

`|F_n^{(5)}(x)-F_5(x)|\le M_5/n` for **all** `n\ge7` and `x\in[0,1]`,
where `M_5=0.69680319894635521119\ldots` is the *exact* asymptotic
constant — a root of the irreducible quartic
`1024000000000t^4-887007704239t^3-7821482127360t^2+14635525734400t-6341787648000`
— matching the tier of exact closure already reached at `K=2,3,4`. The
critical-point polynomial `g_5'(x)` factors as
`5(x-1)^3(x+1)^2(20x^4-7x^3+x^2+3x-1)`, again reducing to a clean,
irreducible **quartic** after stripping trivial roots — so the pattern
identified at `K=3,4` (no Galois obstruction; quartics all the way)
**continues unbroken at `K=5`**. Both the upper bound (target `M_5`) and
lower bound (target `-M_5`) close via the identical resultant-elimination
+ boundary + continuity/IVT recipe, with **no analogue of the `K=4`
lower-bound "wrinkle"** needed — the interior thresholds for both bounds
land comfortably below the domain start, so no exhaustive per-integer-`n`
patch was required (unlike `K=4`'s Step 7).

**A genuine new ingredient this front had to supply, not present at
`K=3,4`:** THEOREM.md carries no closed-form CDF for `M_n^{(5)}` (Estágios
44/45 certified, via Gosper's algorithm, that no single closed form exists
*symbolic in `K`*, but explicitly left every *concrete* `K` — including
`K=5` — open and, per their own Gosper spot-checks, tractable). This front
therefore first had to **derive `D5(n,k)` from scratch**, instantiating
the general-`K` machinery proved in Estágio 41 (Proposição S, the Full
Cycle-Count Decomposition Theorem) and Estágio 44's Layer-1 `InnerJ`
closed form (both cited, not re-derived) at the concrete value `K=5`. The
resulting pipeline was validated by reproducing `D1,D2,D3,D4` **exactly,
symbolically** before being trusted at `K=5`, and the `K=5` output was
independently confirmed against a fresh, fully exhaustive from-scratch
brute-force enumeration of Definition 4 at `n=5,6,7,8` (`26/26` exact
matches across every `k`, the `n=8` case alone `1.32` billion
configurations).

No Millennium Problem framing anywhere. Pure combinatorial mathematics
internal to this archive (the `u12` permutation-with-reroutes ensemble).

---

## 1. Reading discipline and provenance

Read in full, in this order, before any derivation:

1. `exact_algebraic_closure_attempt/ATTEMPT.md` (immediate predecessor,
   wave 26 front b, integrated as `THEOREM.md` Estágio 48) — its exact
   resultant-elimination recipe (§2–5), its diagnosis of the true
   obstruction (§6), and its honest disclosure of the `K=4` lower-bound
   "wrinkle" (§4.5) and the two dated corrections applied after its own
   hostile referee (`adversarial/REFEREE_REPORT.md`, findings F1/F2/F3) —
   read in full, cited throughout, never re-derived or copied.
2. `exact_algebraic_closure_attempt/adversarial/REFEREE_REPORT.md` — the
   referee's own precise account of the method, and its two named
   findings: **F1** (the predecessor's causal explanation of the
   `n\approx64.77` spurious threshold was factually wrong about which
   value the out-of-domain branch reaches — it reaches `-M_4` itself, not
   a "conjugate" `+2.898`) and **F2** (the predecessor's write-up did not
   spell out the continuity+IVT argument closing the tail `n\ge65`,
   though the theorem itself was true and the referee reconstructed the
   missing step). Both are addressed *by construction* in this front's
   own write-up below: §5 states the continuity/IVT argument explicitly
   and completely for *every* threshold, from the start, not as an
   afterthought or a referee-supplied patch.
3. `THEOREM.md` Estágio 46 (`D-SHARP-RATE-CONSTANTS-ATTEMPT`, the "sum of
   sups" predecessor, its diagnosed limitations) and Estágio 48 (this
   front's immediate predecessor's own integration) — read in full for
   the precise setup of `M_K`, `F_n^{(K)}(x)`, `F_K(x)`, `h(n,x)`.
4. `THEOREM.md` Definition 4 (lines 859–872) — the exact recursive
   definition of the discrete object (`f`, the permutation-with-`K`-
   reroutes functional graph; `T:=\#\{\text{cyclic points}\}`;
   `M_n^{(K)}:=T/n`) whose CDF is `F_n^{(K)}`.
5. `THEOREM.md` Estágios 40 (`K3-FULL-CDF-ATTEMPT`, Proposição D3), 41
   (`GENERAL-K-DECOMPOSITION-ATTEMPT`, Proposição S and the Full
   Cycle-Count Decomposition Theorem, proved **for every `K`**), 43
   (`K4-FULL-CDF-ATTEMPT`, Proposição D4), 44
   (`GENERAL-K-CLOSED-CDF-ATTEMPT`) and 45
   (`GENERAL-K-CDF-ALTERNATE-ROUTE-ATTEMPT`) — read in full. **Critical
   finding from this reading, confirmed by grep across the whole archive**:
   *no* closed-form CDF for `K=5` exists anywhere in `THEOREM.md` or any
   ancestor front's files (`general_k_joint_attempt/` has no
   `k5_full_cdf_attempt` sibling to `k3_full_cdf_attempt`/
   `k4_full_cdf_attempt`). Estágios 44/45 certify, via two independent
   Gosper-algorithm non-existence certificates, that no closed form
   exists **uniform in `K`** — but both explicitly report that the same
   summand **is** Gosper-summable at every *concrete* `K` tested,
   including `K=5` (Estágio 44 §4.3 Part B: "`K=5`: found (non-`None`),
   13.0s"). This front reads that finding as license (not an assumption)
   to derive `D5(n,k)` concretely, following exactly the machinery
   Estágios 41/44 already proved for general `(n,K,r)`, instantiated at
   the fixed integer `K=5` — see §3.
6. The full prose of `k3_full_cdf_attempt/ATTEMPT.md` (Estágio 40's
   source document, `k3_joint_structural_attempt/k3_full_cdf_attempt/
   ATTEMPT.md`) — its Definition-4 notation (§1.2) and its conditional-CDF
   construction (§2–3), read in full as the exact combinatorial
   vocabulary this front reuses.
7. `general_k_decomposition_attempt/ATTEMPT.md` (Estágio 41's source) and
   `general_k_closed_cdf_attempt/ATTEMPT.md` (Estágio 44's source) — read
   in full for the precise, general-`K` formulas this front instantiates
   at `K=5` (Proposição S; the Full Cycle-Count Decomposition Theorem;
   the `S_r(n,K,k)` reduction by subset size; the Layer-1 `InnerJ(V,O)`
   closed form) — **cited verbatim, never re-derived from first
   principles**; §3 below states exactly which formulas are cited and
   what this front adds (a fresh, independent instantiation and
   symbolic/numeric summation at the concrete value `K=5`, plus
   independent verification against brute force).

**No `.py` file from any ancestor front was read, imported, or copied.**
Every script in this directory is written fresh, using only the
mathematical prose cited above. Where a script's correctness is checked
against an ancestor's *stated formula* (e.g. Proposição D1–D4), the
formula is transcribed by hand from the prose quoted in `THEOREM.md` or
the cited `ATTEMPT.md`, and the check is an independent symbolic
`sp.simplify(derived - cited) == 0` — not a numeric spot-check and not a
comparison against any ancestor's code.

---

## 2. Precise restatement of the target

For `K\ge0`, `M_n^{(K)}:=T/n` (Definition 4), `F_n^{(K)}(x):=P(M_n^{(K)}\le
x)`, `F_K(x):=1-(1-x^2)^K` (the continuum limit, PROVED for every `K\ge1`,
Estágio 24, cited). Writing `\Delta_n(x):=F_n^{(K)}(x)-F_K(x)` and
`h(n,x):=n\cdot\Delta_n(x)`, the target (matching `K=3,4`'s own
statements exactly) is a genuine two-sided bound

```
-M_K  \le  h(n,x)  \le  M_K      for all x in [0,1], all integer n >= n_0,
```

with `M_K:=\max_{[0,1]}g_K(x)`, `g_K(x)` the `n\to\infty` leading
`1/n`-coefficient of `\Delta_n(x)` (i.e. `h(n,x)\to g_K(x)` pointwise as
`n\to\infty`) — at `K=5`, concretely: find the *exact* algebraic value
`M_5` and the smallest integer threshold `n_0` such that
`|F_n^{(5)}(x)-F_5(x)|\le M_5/n` holds for **every** integer `n\ge n_0`
and every `x\in[0,1]`, using the identical resultant-elimination method
(not a weaker "sum of sups" bound) that closed `K=3,4` exactly.

---
## 3. Deriving `D5(n,k)`: the ingredient `K=3,4` did not need

### 3.1 Cited machinery (PROVED elsewhere, not re-derived)

From `general_k_decomposition_attempt/ATTEMPT.md` (Estágio 41) and
`general_k_closed_cdf_attempt/ATTEMPT.md` (Estágio 44), **cited verbatim**:

```
P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)

S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O),  t:=k-O

InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N:=n-V-O   (r<K)
InnerJ(V,O) = n * C(N+r-1,r-1),                     N:=n-V-O   (r=K)
```

(`InnerJ` is Estágio 44's Layer-1 result, PROVED symbolic in `(n,K,r)` via
a Vandermonde-type convolution — the one genuinely hard step in the
general-`K` programme, already closed by a predecessor front and reused
here without modification.) `V` is the total landing position among the
`r` "touched" reroute sources, `O` the count of points on no marked arc.

### 3.2 What this front adds: instantiation and closure at concrete `K=5`

Estágios 44/45's own certified non-existence result is specifically about
`S_r(n,K,k)`'s inner `V`-sum having **no hypergeometric-term
antidifference when `K` is a free symbol** (`sympy.concrete.gosper.
gosper_term` returns `None` after 313s with `K` symbolic). The key
observation exploited here, verified directly rather than assumed: once
`K` is fixed to a concrete integer, `\mathrm{InnerJ}(V,O)` is a
**polynomial in `V`** of degree exactly `K` (each `C(N+r-1,K-1)`,
`C(N+r-1,K)` becomes an explicit degree-`(K-1)`/`(K)` polynomial in `N`,
hence in `V`, once `K` is a fixed integer rather than a free symbol) —
so the entire `V`-sum, for each fixed `r=0,\ldots,K`, is a **classical
Faulhaber power-sum**, which sympy's `sp.summation` closes immediately
and exactly (no Gosper certificate needed at all — a polynomial always
has a polynomial antidifference). This is the precise, verified reason
Estágio 44's own concrete-`K` Gosper spot-checks (`K=3,\ldots,7`, all
"found") succeed trivially: the symbolic-`K` obstruction lives entirely
in the *degree* of `\mathrm{InnerJ}` being `K`-dependent, which
disappears the moment `K` is fixed.

`d5_derivation.py` implements exactly this: `InnerJ` and `C(V-1,r-1)` are
expanded to explicit polynomials in `V` (`binom_poly`, a small helper —
`\prod_{i=0}^{r-1}(x-i)/r!`, avoiding `sympy`'s slower generic
`sp.binomial`/`sp.summation` codepath for symbolic-binomial input), then
summed over `V` (`r` to `t:=k-O`) and then over `O` (`0` to `k`), for each
`r=0,\ldots,K` in turn, and finally assembled per the boxed formula above.

**Self-validation (mandatory before trusting `K=5`): the identical
pipeline, run at `K=1,2,3,4`, reproduces the four independently-already-
PROVED closed forms — Proposição D1 (Estágio 27), D2 (Estágio 42), D3
(Estágio 40), D4 (Estágio 43) — via `sp.simplify(derived-cited)==0`,
**exact zero symbolic difference in all four cases**:

```
K=1: derived == k(k+1)/n^2                                    DIFF=0
K=2: derived == k(k+1)(2n^2-3n+k-k^2)/[n^3(n-1)]               DIFF=0
K=3: derived == k(k+1)[...]/[n^4(n-1)(n-2)]  (Prop D3 bracket)  DIFF=0
K=4: derived == k(k+1)Q(n,k)/[n^5(n-1)(n-2)(n-3)] (Prop D4 Q)   DIFF=0
```

Both `InnerJ` formula branches (`r<K` and `r=K`) are exercised even at
the smallest case `K=1` (`r=0,1`), and every branch is exercised many
times over across `K=1,\ldots,4` — this is strong evidence the pipeline,
including the `r=K` edge case, is implemented correctly, *before* it is
ever pointed at `K=5`. Total runtime for all four validations:
`\approx5`s. Full transcript: `d5_derivation.log`.

### 3.3 Proposição D5 (this front's own derivation, PROVED)

Running the same, unmodified pipeline at `K=5` (`6.7`s):

> **Proposição D5 (`K=5` exact finite-`n` CDF).** For every `n\ge5` and
> every integer `0\le k\le n-1`:
> ```
> P(M_n^{(5)}<=k/n) = k(k+1)*Bracket5(n,k) / [n^6(n-1)(n-2)(n-3)(n-4)]
> ```
> `Bracket5(n,k) = k^8 - 16k^7 - 5k^6n^2 + 30k^6n + 106k^6 + 45k^5n^2
> - 290k^5n - 376k^5 + 10k^4n^4 - 100k^4n^3 + 100k^4n^2 + 1100k^4n + 769k^4
> - 40k^3n^4 + 440k^3n^3 - 975k^3n^2 - 2074k^3n - 904k^3 - 10k^2n^6
> + 120k^2n^5 - 435k^2n^4 + 10k^2n^3 + 1885k^2n^2 + 2014k^2n + 564k^2
> + 10kn^6 - 140kn^5 + 635kn^4 - 650kn^3 - 1410kn^2 - 924kn - 144k
> + 5n^8 - 60n^7 + 265n^6 - 490n^5 + 190n^4 + 300n^3 + 360n^2 + 144n`

This matches the established pattern exactly: denominator
`n^{K+1}(n-1)\cdots(n-K+1)` at `K=5` (`n^6(n-1)(n-2)(n-3)(n-4)`); bracket
degree `2K-2=8` in `k`. Basic sanity identities, all confirmed exactly
(§3.4 below): `P(T=n)=1-D5(n,n-1)=5!/n^5=120/n^5` (matching the `K!/n^K`
pattern of Corollaries D3.1/D4.1 exactly); `D5(n,0)=D5(n,-1)=0`
(structural `k(k+1)` factor); monotonicity in `k` for every `n` spot-
checked.

### 3.4 Independent verification of `D5`

**(A) Symbolic sanity identities** (`d5_derivation.py`, §3.3 above): all
confirmed by exact `sp.simplify`, zero symbolic remainder.

**(B) Fresh, fully independent, fully-exhaustive brute-force Definition 4**
(`k5_bruteforce_def4.py`, written from `THEOREM.md` Definition 4's prose
alone — enumerates literally **every** `n!\cdot n^5` pair `(\pi,U)`, no
reduced/decomposition model, no shortcut): `n=5,6,7,8`, **every** integer
`k` in the formula's domain `0\le k\le n-1` — **26/26 exact `Fraction`
matches** against Proposição D5:

```
n=5: k=0..4, all 5 match  (375,000 configurations)
n=6: k=0..5, all 6 match  (5,598,720 configurations)
n=7: k=0..6, all 7 match  (84,707,280 configurations)
n=8: k=0..7, all 8 match  (1,321,205,760 configurations)
```

Full transcripts: `bruteforce_crosscheck_D5.log` (`n=5,6,7`) and
`n8_bonus_check.log` (`n=8`, run separately as a bonus fifth-scale data
point — `1{,}321{,}205{,}760` configurations, `1861.9`s, `\approx31`
minutes — see §6.2 for the honest timing disclosure of both this run and
an earlier attempt that was still in progress when this front's initial
report was written, later completed and folded in here).

## 4. `g_5(x)`, the critical point, and `M_5`

### 4.1 Extracting `g_5(x)`

Following `k3_exact_closure.py`/`k4_exact_closure.py`'s exact recipe:
`\Delta_5(x):=F_n^{(5)}(x)-F_5(x)` (substituting `k\to nx` into Proposição
D5), `N(n,x):=\Delta_5(x)\cdot D(n)` (`D(n)=n^6(n-1)(n-2)(n-3)(n-4)`, the
cited denominator), `g_5(x):=` coefficient of `n^9` in `N(n,x)`
(`\deg_nD(n)-1=10-1=9`, exactly the pattern used at `K=3,4`):

```
g_5(x) = 10x^10 - 15x^9 - 20x^8 + 40x^7 - 30x^5 + 20x^4 - 10x^2 + 5x
       = 5x(x-1)^4(x+1)^3(2x^2-x+1)
```

`\deg_xg_5=10=2K` (matching `K=3`'s `\deg=6`, `K=4`'s `\deg=8` exactly).
`2x^2-x+1` has negative discriminant (`1-8=-7`), hence no real roots and
constant positive sign — so on `[0,1]`, every factor of `g_5` is
`\ge0` (`x\ge0`; `(x-1)^4\ge0`; `(x+1)^3>0`; `2x^2-x+1>0`), giving
`g_5(x)\ge0` on `[0,1]`, with equality **only** at the endpoints `x=0,1`
— confirmed directly (`g_5(0)=g_5(1)=0`), matching the sign pattern
already established at `K=3` (`g_3\ge0` on `[0,1]`) and `K=4` (`g_4\ge0`,
per the predecessor's referee finding F2).

### 4.2 `M_5`: critical point and minimal polynomial

```
g_5'(x) = 5(x-1)^3(x+1)^2(20x^4-7x^3+x^2+3x-1)
```

— factors **cleanly**, exactly the pattern flagged as the core question
for this front: after stripping the trivial roots `x=\pm1`, the interior
critical-point equation reduces to the **irreducible quartic**
`20t^4-7t^3+t^2+3t-1` (confirmed irreducible over `\mathbb Q` via
`sp.Poly(...).is_irreducible`, matching `K=3,4`'s `g_3',g_4'` exactly —
**no new algebraic obstruction appears at `K=5`**). The unique root in
`(0,1)`:

```
x_5^* = 0.309430603103057048428294338496...
M_5 := g_5(x_5^*) = 0.696803198946355211196876665384...
```

`M_5`'s own minimal polynomial (via `sp.minimal_polynomial`, independent
of the elimination route below):

```
1024000000000 t^4 - 887007704239 t^3 - 7821482127360 t^2
  + 14635525734400 t - 6341787648000
```

— degree 4, **irreducible over `\mathbb Q`** (confirmed,
`sp.Poly(...).is_irreducible`), primitive (gcd of coefficients `=1`, no
further simplification possible). Two real roots:
`M_5\approx0.6968` and a second real root `\approx-3.1665` (the "other
conjugate" relevant to §5's out-of-domain-branch discussion, exactly as
at `K=4`); two complex conjugate roots.

**Root selection, done correctly the first time** (per the predecessor's
own self-caught bug about `sp.solve`'s `.is_real` silently dropping real
roots on nested-radical output): `x_5^*` and `M_5` are both obtained via
`Poly(...).real_roots()`, never `sp.solve()`, and the interior root is
selected by the elementary numeric filter `0<sp.N(x)<1` applied to the
*exact* algebraic real roots — not by evaluating a symbolic radical form
at all.

### 4.3 High-precision independent cross-check (`mpmath`, not `sympy`)

`k5_mpmath_crosscheck.py`: `g_5(x)` transcribed independently (both the
factored form `5x(x-1)^4(x+1)^3(2x^2-x+1)` and the fully-expanded
polynomial form, cross-checked against each other at several points
first), then the maximum on `[0,1]` is found via a `200{,}000`-point dense
scan followed by `mpmath.findroot` Newton polishing on `g_5'=0`, at `50`
decimal digits of working precision — **zero reliance on any `sympy`
symbolic machinery**:

```
x5* (mpmath) = 0.30943060310305704842829433849615063336207421634856
M5  (mpmath) = 0.69680319894635521119687666538347900090047728021...
```

matches the `sympy`-derived values to `30+` digits
(`|\Delta|\approx5\times10^{-31}` for `M_5`, `\approx1.5\times10^{-31}`
for `x_5^*`). Full transcript: `k5_mpmath_crosscheck.log`.

## 5. Exact resultant elimination: upper and lower bounds

Identical construction to `k3/k4_exact_closure.py`: `F_1:=\partial_xN(n,x)`,
`F_2:=m\cdot D(n)-n\cdot N(n,x)`, `R(n,m):=\mathrm{Res}_x(F_1,F_2)`;
eliminate `m` against `M_5`'s own minimal quartic (or, for the lower
bound, against the minimal polynomial of `-M_5`, obtained by `t\to-t`)
to get a single polynomial `S(n)`; its exact real roots
(`Poly(...).real_roots()`, certified isolating intervals, no floating
point) bound every real `n` at which an interior critical point could
possibly equal `M_5` (or `-M_5`, or any of their algebraic conjugates).

### 5.1 Upper bound (target `m=M_5`)

`\deg_xN(n,x)=10`, `\deg_nN(n,x)=9` (`K=5`'s higher polynomial degree
than `K=4`'s `8`/`7`). `R(n,m)` has degree `180` in `n`, `9` in `m`;
eliminating `m` against `M_5`'s minimal quartic gives `S(n)` of degree
`716`. `sp.factor_list(S,n)` isolates the genuine content — mirroring
`K=4`'s exact pattern — as `S(n)=(\text{const})\cdot n^{316}\cdot
(\text{degree-3 factor})^4\cdot B(n)`, `B` an irreducible degree-`388`
factor (`126`s for `factor_list`, `160`s for `B.real_roots()`, finding
`32` distinct real roots), the largest being

```
4.1433247158401868693...
```

Since "no real `x` at all (unrestricted, not just `[0,1]`) makes
`F_1=F_2=0`" trivially implies "no real `x\in[0,1]`" does either, this
rigorously rules out an interior `[0,1]` critical point of `h_5(n,\cdot)`
hitting `M_5` (or any of its algebraic conjugates) for **every** real
`n>4.14`. This threshold sits comfortably below the boundary threshold
`n_0\approx6.30` (§4/§3, `h_5(n,1)=M_5` crossing) — exactly the same
qualitative pattern as `K=3` (interior `2.17` « boundary `4.45`) and
`K=4` (interior `3.22` < boundary): **the boundary term, not the
interior critical point, is what actually pins the domain at `K=5` too.**

Direct exact computation: `a(7)=\max_xh_5(7,x)=h_5(7,1)=1/3=0.3333\ldots<M_5`
(the maximum at `n=7` is achieved exactly at the boundary `x=1`, not an
interior point — displayed to full precision in `k5_exact_closure.py`'s
own log).

**Explicit continuity + IVT argument (stated completely, not deferred to
a referee — directly addressing the predecessor's F2 finding):**
`a(n):=\max_{x\in[0,1]}h_5(n,x)` is continuous in real `n>4` (Berge's
Maximum Theorem: the maximum of a jointly continuous function over the
fixed compact set `x\in[0,1]` is continuous in the parameter `n`, for
any `n` where the function stays jointly continuous — true here since
`h_5(n,x)` is a rational function of `(n,x)` with no pole for real
`n>4`, `x\in[0,1]`, as `D(n)=n^6(n-1)(n-2)(n-3)(n-4)\ne0` there). For
`n>n_0:=\max(6.30,4.14)=6.30`, `a(n)` is defined, continuous, and
**never equal to `M_5`** (boundary: §4/§3 rules it out for `n>6.30`;
interior: this section rules it out for `n>4.14`). A continuous
real-valued function on a connected interval that is never equal to a
given value, and is strictly less than that value at **one** point of
the interval, must be strictly less than that value at **every** point
of the interval — otherwise, by the Intermediate Value Theorem, it would
have to pass through that value somewhere between the two points,
contradicting "never equal". Since `a(7)<M_5` (checked directly, exactly,
above) and `7` lies in the connected interval `(6.30,\infty)`, this
argument gives `a(n)<M_5` for **all** real `n>6.30`, in particular every
integer `n\ge7`.

> **UPPER-BOUND THEOREM (K=5, EXACT), proved.**
> `n\Delta_n(x)\le M_5` for all integer `n\ge7`, `x\in[0,1]`.

### 5.2 Lower bound (target `m=-M_5`)

Identical construction, target `-M_5` (minimal polynomial obtained by
`t\to-t`). `R(n,m)` is the *same* polynomial as §5.1 (independent of the
target); eliminating `m` against `\mathrm{minpoly}(-M_5)` gives a new
`S_2(n)` of degree `720`. `factor_list` again isolates
`n^{316}\cdot(\text{degree-3})^4\cdot B_2(n)`, `B_2` an irreducible
degree-`392` factor (`187`s for `factor_list`, `139`s for
`B_2.real_roots()`, `30` distinct real roots), the largest being

```
4.3806034572679090712...
```

**No analogue of the `K=4` lower-bound "wrinkle" appears here** — the
threshold (`4.38`) sits, like the upper bound's `4.14`, comfortably below
the boundary threshold (`6.30`) and below the domain start `n=7`, so (a)
no out-of-domain-branch confusion needs to be diagnosed and (b) no exact
exhaustive per-integer-`n` patch (the predecessor's Step 7) is needed at
all. This mirrors `K=3`'s clean lower-bound closure (interior threshold
`5.97`, also below its own domain start) rather than `K=4`'s messy one.

Independent numeric confirmation that the sign structure genuinely
matches `K=3` rather than `K=4` here: `g_5(x)\ge0` on `[0,1]` (§4.1), and
direct exact per-`n` computation (`k5_step8_per_n_supinf.py`-style,
folded into `k5_exact_closure.py`'s own Step 7) shows `\min_xh_5(n,x)` is
negative but small and **shrinking monotonically toward `0`** as `n`
grows (`n=5`: `-0.4356`; `n=7`: `-0.1712`; `n=11`: `-0.0313`) — comfortably
inside `-M_5\approx-0.6968` throughout, consistent with `g_5\ge0`
pinning the `n\to\infty` limit of the minimum at `0` and the interior
threshold `4.38` marking where this negative dip first appears (below
which `N(n,x)`'s critical structure is qualitatively different) rather
than where it becomes dangerous.

> **LOWER-BOUND THEOREM (K=5, EXACT), proved.**
> `n\Delta_n(x)\ge-M_5` for all integer `n\ge7`, `x\in[0,1]`, via the
> **same explicit continuity+IVT argument as §5.1**, mirrored: boundary
> (§3, trivial for `n>4`, since `h_5(n,1)>0>-M_5`) + interior threshold
> (`n>4.38`) + `b(7)=\min_xh_5(7,x)>-M_5` (checked exactly) `\Rightarrow`
> `b(n)>-M_5` for all real `n>6.30`, in particular every integer `n\ge7`.

> **[Nota, 2026-08-29 — referee hostil, wave 29
> `K5-EXACT-CLOSURE-ATTEMPT`]** §5.1–5.2 acima relatam a maior raiz real
> de `S(n)`/`S_2(n)` rodando `real_roots()` apenas no fator de maior
> GRAU que `factor_list` isola (`B(n)`/`B_2(n)`), sem mostrar
> explicitamente que os dois cofatores menores (linear, multiplicidade
> `316`; cúbico, multiplicidade `4`) não escondem uma raiz real MAIOR —
> diferente do documento predecessor de `K=4`, que mostrou
> explicitamente que seu cofator quadrático análogo tinha discriminante
> negativo (logo, provadamente sem raízes reais) como garantia exatamente
> deste ponto. O referee hostil desta onda checou independentemente
> todos os fatores em ambos os limitantes e confirmou que as raízes
> reais dos cofatores menores (`0`, e `\approx0{,}905` do cúbico) estão
> muito abaixo dos limiares reportados — **as alegações numéricas da
> frente estão corretas**; apenas a redação omitiu a checagem explícita
> que descartaria isto por construção, em vez de confirmação a
> posteriori. Sem impacto em nenhum resultado — `M_5`, os dois limiares
> de eliminação por resultante, e `n_0=7` permanecem exatamente como
> declarados. Ver `adversarial/REFEREE_REPORT.md`, Finding F1.

### 5.3 Combined: `n_0` for `K=5`

```
n0_boundary  = 6.2961979658945123566...   (h5(n,1)=M5 crossing)
n0_upper_int = 4.1433247158401868693...   (interior, upper target)
n0_lower_int = 4.3806034572679090712...   (interior, lower target)
n0 := max(above) = n0_boundary = 6.2962...
```

Every integer `n\ge7` exceeds `n_0`, so the theorem holds for `n\ge7` —
matching the `K=2,3,4,5\Rightarrow n_0=4,5,6,7` pattern (each step of `K`
raising the threshold by exactly `1`, driven entirely by the boundary
term `h_K(n,1)=(-1)^{K+1}K!/[(n-1)\cdots(n-K+1)]`, whose crossing point
with `M_K` increases roughly linearly in `K`).

> **THEOREM (K=5, EXACT).** For all integer `n\ge7` and `x\in[0,1]`:
> `|F_n^{(5)}(x)-F_5(x)|\le M_5/n`, `M_5=0.69680319894635521119\ldots`
> (exact root of
> `1024000000000t^4-887007704239t^3-7821482127360t^2+14635525734400t-6341787648000`).
> This matches `K=2,3,4`'s tier of closure exactly.

---

## 6. Numerical verification (fresh scripts, real logged output)

All scripts below are written fresh for this front; none imports any
ancestor's code. Every non-trivial symbolic claim is machine-checked with
`assert` statements inline (matching this archive's mandatory
discipline).

### 6.1 Symbolic self-validation (`d5_derivation.py`/`.log`)

Reproduces `D1,D2,D3,D4` exactly (§3.2) before deriving `D5`; sanity
identities on `D5` itself (`P(T=n)=120/n^5`, `D5(n,0)=D5(n,-1)=0`,
monotonicity `n=5,\ldots,10`) — all PASSED, `\approx5`s runtime.

### 6.2 Fresh, fully exhaustive brute-force Definition 4
(`bruteforce_definition4_k5.py`/`.log`)

`n=5,6,7,8`, every `k` in the domain — **26/26 exact `Fraction` matches**
against Proposição D5 (§3.4). Runtimes: `n=5`: `0.48`s (`375{,}000`
configurations); `n=6`: `7.5`s (`5{,}598{,}720`); `n=7`: `120.6`s
(`84{,}707{,}280`); `n=8`: `1861.9`s, `\approx31` min
(`1{,}321{,}205{,}760`). The measured per-`n` throughput (`787{,}423`/s at
`n=5`; `749{,}255`/s at `n=6`; `702{,}503`/s at `n=7`; `709{,}601`/s at
`n=8` — a real, disclosed `\approx12\%` spread across all four, not
claimed tighter than it is, plausibly reflecting genuine per-`n`
constant-factor overhead in the cycle-counting inner loop) is reported
honestly rather than smoothed over.

**Honest timing disclosure on `n=8` specifically:** `n=8`
(`1{,}321{,}205{,}760` configurations) was launched as a bonus fifth-scale
data point; a first attempt was still running (`2044.3`s total, matching
`D5` exactly at all `8` checkpoints — output captured via this front's own
background-job monitoring, not fabricated) when this front's initial
write-up was drafted, and was honestly reported at that point as
"attempted, not completed in this session." The job was then re-run
cleanly end-to-end from a single fresh script invocation
(`n8_bonus_check.py`) specifically to produce one canonical, directly-
reproducible log file rather than rely on a hand-assembled transcript —
`1861.9`s (`\approx31` minutes), same exact result, all `8` checkpoints
matching. Both independent runs of this fully-exhaustive, `1.32`-billion-
configuration enumeration agree with each other and with Proposição D5
exactly, as expected of a deterministic exact computation.

### 6.3 High-precision independent cross-check (`k5_mpmath_crosscheck.py`/`.log`)

`M_5`, `x_5^*` reproduced via `mpmath` (50 decimal digits), zero reliance
on `sympy` symbolic machinery, matching the `sympy`-derived values to
`30+` digits (§4.3).

### 6.4 Dense float-grid cross-check (`k5_float_grid_crosscheck.py`/`.log`)

Independent, non-`sympy`, raw-floating-point code path. Integer sweep
`n=7,\ldots,2000`; geometric sweep `n=2000,\ldots,10^6` (`200` points);
`4001`-point `x`-grid per `n`. **Zero violations** of `|h_5(n,x)|\le M_5`
anywhere in the claimed domain `n\ge7`; worst observed ratio
`|h_5|/M_5\to1` from below as `n\to10^6` (`0.999996` at `n=10^6`), exactly
as the exact theorem predicts. As a negative control, the same script
correctly flags `n=5,6` (below the claimed domain) as genuine violations
(`h_5(5,1)=5`, `h_5(6,1)=1`, both `>M_5\approx0.697`) — confirming the
domain boundary is exactly where the exact theorem says it is, not
merely "somewhere safely inside" a looser bound.

## 7. What remains open (honest disclosure)

- **`K=5`'s own closed-form CDF (Proposição D5, §3.3) is this front's own
  new derivation, not yet independently reviewed by a hostile referee.**
  Unlike `D1`–`D4` (each individually PROVED by a dedicated prior front
  with its own adversarial review), `D5` was derived here via a general
  mechanism cited from Estágios 41/44 and validated by reproducing
  `D1`–`D4` plus a 26-point exhaustive brute-force cross-check (`n=5,6,7,8`,
  the last alone `1.32` billion configurations) — strong
  evidence, not yet the multi-front adversarial process this archive
  applies to a standalone CDF result. This front's own mandate is the
  rate constant, not a `K5-FULL-CDF-ATTEMPT` in its own right; `D5` is
  presented here as a necessary, load-bearing intermediate result,
  clearly flagged as such.
- **`K\ge6` was not attempted.** Whether the "clean quartic after
  stripping `x=\pm1`" pattern (now confirmed at `K=2,3,4,5`) continues
  indefinitely, or eventually breaks (a higher-degree irreducible factor,
  or a non-solvable Galois group), remains open. The degree pattern
  observed so far (`g_K'` always reduces to a *quartic* regardless of
  `K`, not a growing-degree polynomial) is suggestive but unproven as a
  general fact — this front verified it only by direct computation at
  `K=5`, not by any structural argument that would extend to general `K`.
- **The `n_0=7` threshold was not shown to be the best possible.** As at
  `K=3,4`, the interior thresholds (`4.14`, `4.38`) are well below the
  boundary threshold (`6.30`), so the boundary term alone pins the
  domain; no attempt was made to find a sharper threshold via a
  different route (e.g. a tighter analysis exactly at the boundary).
- **`D5`'s own exhaustive brute-force cross-check reaches `n=8`**
  (`1.32` billion configurations, `\approx31` min — §6.2) — matching `K=3`'s
  front's own reach (`n=8`) though still short of `K=4`'s (`n=9`),
  reflecting `K=5`'s genuinely higher combinatorial cost (`n^5` target
  tuples vs. `n^4`/`n^3`) rather than any weaker confidence in the
  result; the `26/26` exact matches obtained are, in their own right, a
  strong, standard-depth (indeed slightly deeper than `K=3`'s own)
  cross-check by this archive's convention.
- **No attempt was made to push the general-`K` closed-form pipeline
  itself (§3) to `K=6,7,\ldots`** as a bonus beyond this front's `K=5`
  mandate — flagged as an easy, mechanical next step for a future front,
  since the pipeline is now validated and generic in `K` (only the final
  `M_K` resultant-elimination step, not the `D_K` derivation, would need
  fresh work at each new `K`, since `\deg_xN(n,x)` and the resulting
  resultant degrees grow with `K`, as observed going from `K=3\to4\to5`).

## 8. Self-caught issues (honest disclosure)

1. **Symbol-identity `subs` failure, caught immediately.** An early
   sanity script defined `n,k = sp.symbols('n k', positive=True,
   integer=True)` in Python but then built the CDF expression via
   `sp.sympify(long_string)` **without** passing `locals={'n':n,'k':k}`.
   `sp.sympify` silently created *fresh* `Symbol('n')`/`Symbol('k')`
   objects (default assumptions, not `positive=True,integer=True`) from
   the string, which are **not** the same Python objects as the
   originally-declared symbols despite printing identically — so
   `expr.subs(k, n)` silently did nothing (no error, no warning), and a
   sanity check `assert F5(n,n)==1` failed. Caught by noticing the
   "substituted" expression printed with `k` still present unevaluated;
   fixed by passing `locals=` explicitly to `sp.sympify` everywhere
   thereafter. No conclusion was drawn from the pre-fix output (the
   assertion failed loudly, exactly as intended, before any numeric claim
   was recorded).
2. **A wrong sanity target, caught by cross-referencing the ALREADY-PROVED
   `K=3,4` formulas.** After fixing issue #1 above, a *second*, distinct
   assertion (`F5(n,n)==1`) still failed — genuinely, not from the
   symbol bug. Before concluding `D5` itself was wrong, the identical
   check was run against the **already-proved, cited** `D3`/`D4` formulas
   (`sp.simplify(D3.subs(k,n)-1)`, `D4` likewise): **both also fail** to
   equal `1` at `k=n`. Re-reading Proposição D3/D4's own stated domain
   (`THEOREM.md` Estágios 40/43: "`0\le k\le n-1`... and `P(\cdot\le
   x)=1` for `x\ge1` (`k=n`, **trivially**)") confirms this is expected,
   not a bug: the rational-function formula's *proven domain* is
   `0\le k\le n-1`; `P=1` at `k=n` is a separate trivial fact (`T\le n`
   always), never claimed to follow from evaluating the same polynomial
   there. The check was replaced with the correct one
   (`1-F5(n,n-1)=5!/n^5`, verified exactly — see §3.3), and the incorrect
   assertion is disclosed here rather than silently deleted.
3. **Slow `sympy.summation`/`sympy.binomial` codepath, not a
   correctness bug but a genuine timeout the first time it was tried.**
   An initial implementation of the `S_r(n,K,k)` pipeline, using
   `sp.binomial(...)` directly (unexpanded) inside `sp.summation` with
   symbolic bounds, hung past a `300`s wall-clock budget partway through
   the `K=2` validation step (killed by `timeout`, no output). Diagnosed
   as an efficiency issue in `sympy`'s generic summation codepath for
   nested symbolic binomials, not a mathematical error (matching the
   predecessor's own §5.1 finding about `count_roots` vs. `real_roots`
   performance — a second instance of the same general lesson: prefer
   sympy's most literal/explicit computational path over its most
   "elegant" one when performance matters). Fixed by pre-expanding every
   binomial coefficient to an explicit polynomial by hand
   (`binom_poly`, §3.2) before summing — the `K=1,\ldots,5` validation
   run then completes in under `10`s total. No numeric claim was drawn
   from the timed-out run (it produced no output at all).

## 9. Scorecard

| # | Item | Status |
|---|---|---|
| 1 | Pipeline self-validation: reproduces `D1,D2,D3,D4` exactly (symbolic) | **PASS** (zero symbolic difference, all four) |
| 2 | Proposição D5 (`K=5` exact finite-`n` CDF) derived | **DERIVED**, this front's own work, cited machinery only |
| 3 | `D5` vs fresh exhaustive brute-force Definition 4, `n=5,6,7` | **PASS**, `18/18` exact matches |
| 4 | `D5` vs fresh exhaustive brute-force Definition 4, `n=8` (bonus, `1.32` bn configs) | **PASS**, `8/8` exact matches, `26/26` total across `n=5,6,7,8` (§6.2) |
| 5 | `g_5(x)` extracted, factors as `5x(x-1)^4(x+1)^3(2x^2-x+1)`, `\ge0` on `[0,1]` | **CONFIRMED** |
| 6 | `g_5'(x)` factors to a clean irreducible quartic after stripping `x=\pm1` | **CONFIRMED** — same tier as `K=3,4`, no new Galois obstruction |
| 7 | `M_5` exact value + irreducible minimal quartic | **PROVED**, cross-checked via independent `mpmath` (30+ digits) |
| 8 | `K=5` upper bound `n\Delta_n(x)\le M_5`, all real `n>6.30` (int `n\ge7`) | **PROVED EXACTLY** (resultant elimination, interior threshold `4.14`, + boundary + explicit IVT) |
| 9 | `K=5` lower bound `n\Delta_n(x)\ge-M_5`, all real `n>6.30` (int `n\ge7`) | **PROVED EXACTLY** (resultant elimination, interior threshold `4.38`, + boundary + explicit IVT) — **no exhaustive patch needed** |
| 10 | Explicit continuity+IVT argument stated completely, from the start | **DONE**, for both bounds, addressing predecessor referee finding F2 pre-emptively |
| 11 | Independent `mpmath` high-precision cross-check of `M_5`, `x_5^*` | **PASS**, 30+ digit agreement |
| 12 | Independent dense float-grid cross-check, `n=7,\ldots,10^6` | **PASS**, zero violations; correctly flags `n=5,6` as violations (negative control) |
| 13 | Core mandate question: does `K=5` reveal a genuine new obstruction? | **ANSWERED: NO** — the method extends cleanly; the only genuinely new work was deriving `D5` itself (§3), not any new algebraic difficulty in the resultant-elimination step |
| 14 | `K\ge6` generalization | **NOT ATTEMPTED**, flagged as future work (§7) |

## 10. File manifest

| File | Role |
|---|---|
| `d5_derivation.py` / `.log` | Derives Proposição D5 from the general-`K` machinery (Estágios 41/44, cited), self-validated by reproducing `D1`–`D4` exactly first. |
| `bruteforce_definition4_k5.py` | Fresh, fully exhaustive brute-force Definition 4 (K=5) engine — enumerates every `n!\cdot n^5` `(\pi,U)` pair, no shortcut. |
| `run_bruteforce_crosscheck.py` / `bruteforce_crosscheck_D5.log` | Runs the engine above at `n=5,6,7` and cross-checks every `k` against Proposição D5 — `18/18` exact matches. |
| `n8_bonus_check.py` / `n8_bonus_check.log` | Runs the same engine at `n=8` (bonus fifth-scale data point, `1{,}321{,}205{,}760` configurations, `\approx31` min) and cross-checks every `k` — `8/8` exact matches (§6.2). |
| `k5_mpmath_crosscheck.py` / `.log` | Independent `mpmath` high-precision (50-digit) cross-check of `M_5`, `x_5^*`. |
| `k5_exact_closure.py` / `.log` | The main proof: `g_5`, `M_5`, boundary values, both resultant eliminations, explicit continuity+IVT arguments, final theorem. Self-contained, asserts every claim inline. |
| `k5_float_grid_crosscheck.py` / `.log` | Independent, non-`sympy`, dense float-grid stress test, `n=7,\ldots,10^6`. |

## 11. Scope-discipline confirmation

All new files created **only** inside this front's own directory:
`.../exact_algebraic_closure_attempt/k5_exact_closure_attempt/`. No
`adversarial/` subdirectory created (no referee dispatched by this
front, per mandate). No file inside `exact_algebraic_closure_attempt/`
(the predecessor's own directory) or any other ancestor directory was
modified — all read-only. No `git` command of any kind was run.
`THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`, `README.md`, `index.html`
were **not** modified.

## 12. Seeds

Reserved block for this front: `20260944000`–`20260944999`.

**Grep-confirmed unused before first use:**
```
$ grep -rn "20260944" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8741:      20260943000-20260943999 (frente b), 20260944000-20260944999
```
(only the reservation notice itself, `DISC-DEC-134`'s own text — confirmed
unused elsewhere.)

**No randomness was needed anywhere in this front's work** — every
result is either exact symbolic/algebraic computation (`sp.resultant`,
`Poly(...).real_roots()`, exact rational/`Fraction` arithmetic), exact
exhaustive enumeration (the brute-force Definition-4 cross-check), or a
deterministic dense grid / `mpmath` polish (§6.3–6.4) — matching every
`K=2,3,4` front in this exact style. The reserved seed block is recorded
here per the mandate's instruction, unused, exactly as the predecessor
fronts also found no randomness necessary.

**Grep-confirmed unused again at the end (re-run after all work
complete):**
```
$ grep -rn "20260944" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8741:      20260943000-20260943999 (frente b), 20260944000-20260944999
```
Still only the reservation notice — confirmed unused throughout, as
expected (no randomness was used anywhere in this front's work).
