# ATTEMPT — the γ-scaling law: `φ(n,γn)/φ_∞(γn) → √(2/(2−γ))` for every fixed `γ ∈ (0,1]`

**Wave 17 front (e), `DISC-DEC-072` (`GAMMA-SCALING-LAW-ATTEMPT`).**
First dedicated attack on the scaling law open since Estágios 10–13 of
`theorem/THEOREM.md` ("a lei de escala `γ∈(0,1)` — caracterizada, não
provada, sem frente ativa").

---

## VERDICT (up front)

> **PROVED, for every fixed `γ ∈ (0,1]`** — the full mandate interval
> `(0,1)` plus the endpoint `γ=1`, which the proof re-derives rather
> than imports:
>
> `φ(n,γn) / φ_∞(γn) → √(2/(2−γ))` as `n→∞`,
>
> with an **explicit, finite-`n`, two-sided envelope** (Theorem 1′
> below, numerically certified at 30 grid points) whose asymptotic
> width is `Θ_n(γ) = (Γ(5/4)/√(2π))·β^{−3/4}n^{−1/4}(1+o(1))`,
> `β := γ(2−γ)/2`. Both stretch goals are also reached:
>
> - **Uniformity (stretch 1): PROVED** on every compact `[γ₀,1] ⊂ (0,1]`
>   (Corollary 1).
> - **`γ→0` endpoint (stretch 2): PROVED** in the moving-parameter
>   sense: if `γ_n → 0` with `γ_n n^{1/3}/\ln n → ∞`, the ratio → 1
>   (Corollary 2) — the scaling law degrades continuously to "no
>   degradation" exactly as `√(2/(2−γ)) → 1` predicts.
>
> **Bonus (beyond mandate): the second-order term.** Numerics +
> a heuristic expansion of this front's own proof identify the exact
> second-order constant in closed form,
> `√n·(ratio − √(2/(2−γ))) → C(γ) = −(2/(3√π))·√γ·(6−8γ+3γ²)/(2−γ)²`,
> **PROVED at `γ=1`** (where it reduces to `−2/(3√π)`, a consequence of
> Robbins 1955 + FGKP95 already in the Estágio 19 lineage) and
> **CONJECTURED for `γ∈(0,1)`** — Richardson-extrapolated numerics
> match the closed form to 7 significant digits at all 11 grid values
> of `γ` (§7.3). Not claimed as proved.

The engine of the proof is **not** the Estágio 9/12 machinery (whose
rate `|Δ_n(c)| ≤ [a√c+0.2805]/n` is, as the dispatch pre-diagnosed,
structurally too weak here: at `c=γn` it gives `O(1)` *relative* error
against `φ_∞(γn) = Θ(n^{-1/2})`). Instead, §1 derives — from scratch,
directly from Definition 1 of THEOREM.md — a new **exact finite-`n`
double-sum formula** for `φ(n,c)` (Lemma 1), of which the archive's
`φ(n,n)=Q(n)/n` identity (Estágio 10, post-adversarial correction) is
the one-line `q=1` special case, and then performs a Laplace/Gaussian
analysis of that formula in the `c=γn` regime with all error terms
explicit. Every analytic ingredient is elementary (Chernoff, Hoeffding,
Jensen, sum–integral comparison); the only citations are classical
(Hoeffding's lemma) or already-proved archive results (Theorem 1 /
Corollary 4.2 of THEOREM.md for `φ_∞`).

---

## §0 Object, target, and provenance of every borrowed ingredient

**The object** (Definition 1, THEOREM.md §1, quoted): `π` a uniform
permutation of `[n]`; `ξ_i` i.i.d. Bernoulli(`q`), `q = c/n` (with
`q = min(c/n,1)`); `U_i` i.i.d. uniform on `[n]`; all independent;
`f(i) = U_i` if `ξ_i=1`, else `f(i) = π(i)`;
`φ(n,c) := E[#\{i \text{ cyclic}\}]/n`. At `c = γn` with `γ ∈ (0,1]`
this means exactly `q = γ`.

**The target** (THEOREM.md, Estágio 10, "Sobre `c` crescendo com `n`"):
for `c=γn`, `φ(n,c)/φ_∞(c) → √(2/(2−γ))`, "**provado** no extremo
`γ=1` (`φ(n,n)=Q(n)/n` exatamente, função `Q` de Ramanujan) e
caracterizado numericamente para `γ∈(0,1)`."

**Borrowed ingredients (each cited to its source; everything else is
derived from scratch in this document):**

| Ingredient | Source | How used |
|---|---|---|
| Definition 1 of the model | THEOREM.md §1 | the object itself |
| `φ_∞(c) = ∫_0^1 e^{-ct^2}dt = (√π/2)c^{-1/2}\mathrm{erf}(√c)` | THEOREM.md Theorem 1 (PROVED there) | denominator of the ratio |
| `φ_∞(c) = (√π/2)c^{-1/2} − R(c)`, `0<R(c)<e^{-c}/(2c)` | THEOREM.md Corollary 4.2 (PROVED there) | final ratio step (§5) |
| Mixture identity (7.1), `φ(n,c)=E_{K∼\mathrm{Bin}(n,c/n)}[φ_n^{(K)}]` | THEOREM.md §7.2 Fact 4.1 | **validation only** (test V3), not used in the proof |
| Closed forms `φ_n^{(1)},φ_n^{(2)},φ_n^{(3)}`; `φ(n,n)=Q(n)/n` | THEOREM.md Estágios 3–4; Estágio 10 correction | **validation only** (tests V2, V3); `Q(n)/n` is independently re-derived in Remark 1.2 |
| Hoeffding's lemma (`E e^{λ(X-EX)} ≤ e^{λ^2/8}`, `X∈[0,1]`) | Hoeffding 1963, classical — CITED | Lemma 4 upper bound; the scalar inequality additionally checked on a 6·10⁶-point grid (04, [S]) |
| `Q(n) = √(πn/2) − 1/3 + O(n^{-1/2})` | Robbins 1955 + FGKP95 Thm 7 (`θ(n)→1/3`), both verified in the Estágio 19 lineage | **only** for the `γ=1` case of the second-order *remark* (§7.3); not used in Theorems 1′/2 |

Not used anywhere: the Estágio 9 all-orders closed form, the Estágio
12 rate, the Estágio 13/19 sharp-constant results, any prior front's
`.py` script (none opened, per mandate).

**Discipline notes.** No randomness anywhere — the object is a finite
deterministic double sum, evaluated exactly (Fractions), in high
precision (mpmath dps=40), or in float64 with roundoff bounded against
the exact values (test V4). The seed block `20260868000+` was reserved
but never drawn from; `grep -rn "20260868"` over the repo returns only
coincidental digit substrings inside unrelated CSV/JSONL data files of
`01_TAMESIS_CORE` (checked before starting; no reservation conflict,
no seeds consumed). No git commits. No adversarial/ directory created,
no referee dispatched (per mandate).

---

## §1 The exact finite-`n` formula

> **Lemma 1 (exact formula; NEW, PROVED).** For every integer `n ≥ 1`
> and every `q ∈ [0,1]`,
>
> `φ(n, qn) = (1/n) \sum_{k=1}^{n} A_k(n,q)`,   where
> `A_k(n,q) := E\big[\,P_{k,M_k}\,\big]`,  `M_k ∼ \mathrm{Binomial}(k,q)`,
> `P_{k,m} := \prod_{i=1}^{m}\Big(1 − \frac{k−i}{n}\Big)`
> (empty product = 1). Equivalently,
> `A_k(n,q) = \sum_{m=0}^{k}\binom{k}{m}q^m(1−q)^{k−m}\prod_{i=1}^{m}\frac{n−k+i}{n}`.

*Proof.* A point is cyclic for `f` iff it lies on a directed cycle of
the functional digraph. Since every vertex has out-degree exactly 1,
the cycles of `f` are vertex-disjoint and every cyclic point lies on
exactly one of them; hence, pointwise in `ω`,

`#\{\text{cyclic points}\} = \sum_{C} |C|\; \mathbf 1\{C \subseteq f\}`,

the sum running over all *possible* directed cycles
`C = (i_1 → i_2 → \cdots → i_k → i_1)` on distinct vertices of `[n]`,
and `\{C ⊆ f\} := \{f(i_j)=i_{j+1 \bmod k}\ \forall j\}`. The number of
directed `k`-cycles is `\binom nk (k−1)! = (n)_k/k`, where
`(n)_k := n(n−1)\cdots(n−k+1)`.

Fix one such `C` and compute `P(C ⊆ f)`. Condition on the restriction
of `ξ` to `C`'s vertex set: for each subset `S` of the `k` vertices,
`P(ξ|_C = \mathbf 1_S) = q^{|S|}(1−q)^{k−|S|}`. Given `S` with
`|S|=m`: the required events split into `\{U_{i_j} = i_{j+1}\}` for
the `m` rerouted vertices — independent, probability `1/n` each,
independent of `π` — and `\{π(i_j)=i_{j+1}\ \forall\, i_j \notin S\}`
— a prescription of `π` at `k−m` distinct points with distinct images,
probability `(n−(k−m))!/n! = 1/(n)_{k−m}` under the uniform
permutation. Hence

`P(C ⊆ f) = \sum_{m=0}^{k}\binom km q^m (1−q)^{k−m}\, n^{−m} / (n)_{k−m}`.

Summing over cycles and lengths, with
`(n)_k/(n)_{k−m} = \prod_{i=1}^{m}(n−k+i)`:

`E[\#\text{cyclic}] = \sum_{k=1}^{n} \frac{(n)_k}{k}\cdot k \cdot P(C⊆f) = \sum_{k=1}^n \sum_{m=0}^k \binom km q^m(1−q)^{k−m}\prod_{i=1}^m\frac{n−k+i}{n}`,

and `\prod_{i=1}^m \frac{n-k+i}{n} = \prod_{i=1}^m (1-\frac{k-i}{n}) = P_{k,m}`. Divide by `n`. `∎`

**Remark 1.1 (sanity, `q=0`).** `A_k(n,0)=1` for every `k`, so
`φ(n,0) = n/n = 1` — every point of a permutation is cyclic. ✓

**Remark 1.2 (the `γ=1` endpoint falls out).** At `q=1`, `M_k = k`
a.s., so `A_k = P_{k,k} = (n)_k/n^k` and
`φ(n,n) = (1/n)\sum_{k=1}^n (n)_k/n^k = Q(n)/n` — a self-contained
one-paragraph re-derivation of the exact identity recorded in Estágio
10 (post-adversarial correction), obtained here without the `(a,b,r)`
chain machinery. Verified exactly for `n=1..400` (test V2).

**Remark 1.3 (independent validation).** Lemma 1 was validated four
independent ways (script `01`, all exact rational arithmetic):
**(V1)** against a from-scratch brute-force enumeration of Definition
1 (all `π`, all reroute subsets, all `U`-assignments) at `n=3,4,5`, as
polynomials in `q` — coefficient-by-coefficient agreement;
**(V2)** the `q=1` endpoint vs `Q(n)/n`, `n=1..400`, exact;
**(V3)** inverting the exact mixture identity (7.1) (Fact 4.1 of
THEOREM.md) on Lemma 1's `q`-polynomial recovers `φ_n^{(K)}`, which
matches the archive's independently proved closed forms
(`φ_n^{(1)}=2/3+1/(3n^2)`, Estágio-3 `φ_n^{(2)}`, Estágio-4
`φ_n^{(3)}`, and `φ_n^{(n)}=Q(n)/n`) exactly for `n=6..10` — tying
Lemma 1 to the Estágio 3/4/9 lineage without importing it;
**(V4)** float64-evaluator roundoff vs exact Fractions at
`(n,γ)=(50,1/2),(200,3/10)`: relative error `< 5·10^{-16}`.

---

## §2 Notation and elementary bounds

Throughout, fix `γ ∈ (0,1]` and set `q=γ`, `c=γn`. Write:

- `β := γ(2−γ)/2 ∈ (0, 1/2]`  (note `γ/2 ≤ β ≤ γ`);
- `σ_k(x) := \dfrac{x(2k−x−1)}{2n}` for real `x∈[0,k]`, so that for
  integer `m`, `\sum_{i=1}^m \frac{k−i}{n} = σ_k(m)`;
- `s(k) := σ_k(γk) = \dfrac{β k^2}{n} − \dfrac{γk}{2n}`, so
  `e^{−s(k)} = e^{−βk^2/n}\,e^{γk/(2n)}` exactly;
- `a_γ := γ(1−\ln 2)/2`;
- `G_n := \tfrac12\sqrt{πn/β}`  (the Gaussian integral
  `\int_0^\infty e^{−βx^2/n}dx`);
- `D := M_k − γk` (so `E D = 0`, `E D^2 = kγ(1−γ) ≤ k/4`).

Each factor of `P_{k,m}` lies in `(0,1]` (since `0 ≤ k−i ≤ n−1`), so
`P_{k,m} ∈ (0,1]` and `A_k ∈ (0,1]` always.

> **Lemma 2 (product sandwich; PROVED).** For `1 ≤ m ≤ k ≤ n`:
> **(a)** `P_{k,m} ≤ e^{−σ_k(m)}`;
> **(b)** if moreover `k ≤ n/2`, then
> `P_{k,m} ≥ e^{−σ_k(m) − k^3/n^2}`.

*Proof.* (a) `1−x ≤ e^{−x}` on each factor. (b) For `x ∈ [0,1/2]`:
`−\ln(1−x) − x = \sum_{j≥2} x^j/j ≤ \frac{x^2}{2(1−x)} ≤ x^2`, i.e.
`1−x ≥ e^{−x−x^2}`. Apply with `x_i=(k−i)/n ≤ k/n ≤ 1/2` and
`\sum_{i=1}^m x_i^2 ≤ m(k/n)^2 ≤ k^3/n^2`. `∎`

> **Lemma 3 (a priori decay; PROVED).** For all `1 ≤ k ≤ n` and
> `γ∈(0,1]`:
> `A_k ≤ e^{−a_γ k} + e^{−γk(k−1)/(4n)}`.

*Proof.* Split on `\{M_k < γk/2\}` and its complement, using
`P_{k,m} ≤ 1`:
`A_k ≤ P(M_k ≤ γk/2) + \max_{m ≥ γk/2} P_{k,m}`.
Chernoff for the first term: for `t>0`,
`P(M_k ≤ γk/2) ≤ e^{tγk/2}\,E[e^{−tM_k}] = e^{tγk/2}\big(1−γ+γe^{−t}\big)^k ≤ \exp\big(tγk/2 + γk(e^{−t}−1)\big)`
(using `1+x ≤ e^x`); at `t=\ln 2` the exponent is
`γk(\ln 2/2 − 1/2) = −a_γ k`. For the second term, by Lemma 2(a) and
`m ≤ k ⇒ 2k−m−1 ≥ k−1`:
`σ_k(m) = \frac{m(2k−m−1)}{2n} ≥ \frac{m(k−1)}{2n} ≥ \frac{γk(k−1)}{4n}` for `m ≥ γk/2`. `∎`

This bound is verified numerically with **zero violations** for
`k = 1..K_n` at `(n,γ)=(65536, 0.3)` and `(65536, 0.8)` (script `02`,
audit (T)), and it powers the *certified truncation* used by every
high-`n` evaluation in §7: for any cutoff `K`,

`\sum_{k>K}^{n} A_k ≤ \dfrac{e^{−a_γ(K+1)}}{1−e^{−a_γ}} + e^{−γK^2/(4n)}\Big(1+\dfrac{2n}{γK}\Big) =: ρ(K)`   (2.1)

(geometric sum for the first part; for the second,
`\sum_{k>K} e^{−γk(k−1)/(4n)} ≤ \sum_{j≥K} e^{−γj^2/(4n)} ≤ e^{−γK^2/(4n)} + \int_K^\infty e^{−γx^2/(4n)}dx`
and `\int_K^\infty e^{−ux^2}dx ≤ \frac{1}{2uK}e^{−uK^2}` with `u=γ/(4n)`).

---

## §3 Fluctuation control on the main range

> **Lemma 4 (Gaussian replacement; PROVED).** For `1 ≤ k ≤ n`:
> **(upper)** `A_k ≤ \big(1+ε_k\big)e^{−s(k)}`, with
> `ε_k := \dfrac{k}{n}\sqrt{\dfrac k2}\;e^{k^3/(4n^2)}`;
> **(lower)** if `k ≤ n/2`,
> `A_k ≥ \big(1 − k^3/n^2\big)\,e^{−s(k)}`.

*Proof.* The identity
`σ_k(m) − σ_k(x) = \frac{(m−x)\,(2k−m−x−1)}{2n}` (both sides are the
same quadratic) with `x=γk` gives, since `m, γk ∈ [0,k]` implies
`|2k−m−γk−1| ≤ 2k`,

`|σ_k(M_k) − s(k)| ≤ |D|\,k/n`.   (3.1)

**Upper.** By Lemma 2(a), `A_k ≤ E[e^{−σ_k(M_k)}] ≤ e^{−s(k)}E[e^{u|D|}]`
with `u := k/n`, by (3.1). Now `e^{u|D|} − 1 ≤ u|D|e^{u|D|}`, so by
Cauchy–Schwarz,

`E[e^{u|D|}] ≤ 1 + u\,\big(E D^2\big)^{1/2}\big(E e^{2u|D|}\big)^{1/2}`.

`D` is a sum of `k` independent centered variables supported in
intervals of length 1, so Hoeffding's lemma (CITED, classical; the
underlying scalar inequality
`γe^{λ(1−γ)}+(1−γ)e^{−λγ} ≤ e^{λ^2/8}` is additionally verified on a
`999×6001` grid with zero violations, script `04` [S]) gives
`E[e^{λD}] ≤ e^{λ^2 k/8}`; hence
`E[e^{2u|D|}] ≤ E[e^{2uD}]+E[e^{−2uD}] ≤ 2e^{u^2k/2}`. With
`E D^2 ≤ k/4`:

`E[e^{u|D|}] ≤ 1 + u\sqrt{k/4}\cdot\sqrt2\,e^{u^2k/4} = 1 + \frac kn\sqrt{\frac k2}\,e^{k^3/(4n^2)} = 1+ε_k`.

**Lower.** By Lemma 2(b) (using `k ≤ n/2`), and since
`\sum_{i≤M_k} x_i^2 ≤ k^3/n^2` deterministically,
`A_k ≥ e^{−k^3/n^2} E[e^{−σ_k(M_k)}]`. By Jensen (convexity of `exp`)
and `E[σ_k(M_k)] = s(k) − \frac{γ(1−γ)k}{2n} ≤ s(k)` (direct
computation from `E M = γk`, `E M^2 = γ^2k^2+γ(1−γ)k`),
`E[e^{−σ_k(M_k)}] ≥ e^{−E σ_k(M_k)} ≥ e^{−s(k)}`. Finally
`e^{−k^3/n^2} ≥ 1−k^3/n^2`. `∎`

Both inequalities verified numerically with **zero violations** over
`k=1..K_n` at `(65536,0.3)` and `(65536,0.8)` (script `02`, audits
(I−)/(I+)).

---

## §4 Sum–integral comparisons

> **Lemma 5 (PROVED).** Let `g:[0,∞)→[0,∞)`.
> **(a)** If `g` is nonincreasing, then
> `\int_0^\infty g − g(0) − \int_K^\infty g \;≤\; \sum_{k=1}^{K} g(k) \;≤\; \int_0^\infty g`.
> **(b)** If `g` is unimodal (nondecreasing then nonincreasing), then
> `\sum_{k=1}^{\infty} g(k) ≤ \int_0^\infty g + 2\sup g`.
> **(c)** Gaussian integrals (`b>0`):
> `\int_0^\infty e^{−bx^2}dx = \tfrac12\sqrt{π/b}`;
> `\int_0^\infty x^{3/2}e^{−bx^2}dx = \tfrac12 Γ(5/4)\,b^{−5/4}`;
> `\int_0^\infty x^{3}e^{−bx^2}dx = \tfrac1{2}b^{−2}`;
> `\int_K^\infty e^{−bx^2}dx ≤ \tfrac1{2bK}e^{−bK^2}`;
> and `\max_x x^{3/2}e^{−bx^2} = (3/(4b))^{3/4}e^{−3/4}`,
> `\max_x x^{3}e^{−bx^2} = (3/(2b))^{3/2}e^{−3/2}`.

*Proof.* (a) `g(k) ≤ \int_{k−1}^{k} g` termwise gives the upper bound
`\int_0^K g ≤ \int_0^\infty g`; `g(k) ≥ \int_k^{k+1} g` gives
`\sum_1^K ≥ \int_1^{K+1} g ≥ \int_0^\infty g − \int_0^1 g − \int_{K+1}^\infty g`,
and `\int_0^1 g ≤ g(0)`, `\int_{K+1}^\infty ≤ \int_K^\infty`.
(b) Let `x^*` be a mode. For integers `k ≤ x^*−1`, `g(k) ≤ \int_k^{k+1}g`
(nondecreasing side needs `k` to the *left*: on `[k,k+1] ⊆ [0,x^*]`,
`g(k) ≤ g(x)`); for `k ≥ x^*+1`, `g(k) ≤ \int_{k−1}^{k}g`. The used
intervals are disjoint (all on the respective sides of `x^*`), and at
most two integers `k ∈ (x^*−1, x^*+1)` are covered by neither case;
each of those terms is `≤ \sup g`. (c) Substitute `u=bx^2`
(`\int_0^\infty x^{s−1}e^{−bx^2}dx = \tfrac12 b^{−s/2}Γ(s/2)`); the
tail bound via `\int_K^\infty e^{−bx^2}dx ≤ \int_K^\infty \frac xK e^{−bx^2}dx`;
maxima by differentiating the log. `∎`

Sanity checks: (a) verified at 8 `(γ,n)` pairs, `|Σ − G_n| ≤ 1` with
the actual defect ≈ `0.5` every time (script `03`, [H3]).

---

## §5 The theorem

Define, for `γ ∈ (0,1]` and `n ≥ 3` (so `\ln n > 1`):

- `K := \big\lceil \sqrt{(4/β)\,n \ln n} \big\rceil` (truncation);
- `ω := K^3/(4n^2)`;  `δ := e^{γK/(2n)} − 1`;
- `J_{3/2} := \tfrac12Γ(5/4)(n/β)^{5/4} + 2\,(3n/(4β))^{3/4}e^{−3/4}`;
- `J_{3} := n^2/(2β^2) + 2\,(3n/(2β))^{3/2}e^{−3/2}`;
- `ρ := ρ(K)` as in (2.1);  `T := \dfrac{n}{2βK}e^{−βK^2/n}`;
- `U := (1+δ)\Big[G_n + \dfrac{e^{ω}}{\sqrt2\,n}J_{3/2}\Big] + ρ`;
- `\mathrm{Lo} := G_n − 1 − T − (1+δ)\,J_3/n^2`.

> **Theorem 1′ (finite-`n` sandwich; PROVED).** For every `γ ∈ (0,1]`
> and every `n` with `K ≤ n/2`:
>
> `\mathrm{Lo} \;≤\; n\,φ(n,γn) \;≤\; U.`

*Proof.* By Lemma 1, `nφ(n,γn) = \sum_{k=1}^n A_k`.

**Upper.** Split at `K`. For `k ≤ K`, Lemma 4 (upper) with
`ε_k ≤ e^{ω}\,k^{3/2}/(\sqrt2\,n)` (since `k^3/(4n^2) ≤ ω` for
`k ≤ K`) gives

`\sum_{k≤K} A_k ≤ \sum_{k≤K} e^{−s(k)} + \frac{e^{ω}}{\sqrt2\,n}\sum_{k≤K} k^{3/2}e^{−s(k)}.`

Since `e^{−s(k)} = e^{−βk^2/n}e^{γk/(2n)} ≤ (1+δ)e^{−βk^2/n}` on
`k ≤ K`, Lemma 5(a) bounds the first sum by `(1+δ)G_n`, and Lemma
5(b),(c) with the unimodal `g(x)=x^{3/2}e^{−βx^2/n}` bounds the second
by `(1+δ)J_{3/2}`. The `k > K` part is `≤ ρ` by (2.1). Total: `U`.

**Lower.** Drop the `k>K` part (`A_k ≥ 0`). For `k ≤ K ≤ n/2`, Lemma 4
(lower) and `e^{−s(k)} ≥ e^{−βk^2/n}` (as `s(k) ≤ βk^2/n`) give

`\sum_{k≤K}A_k ≥ \sum_{k≤K} e^{−βk^2/n} − \frac{1}{n^2}\sum_{k≤K}k^3 e^{−s(k)} ≥ \big(G_n − 1 − T\big) − \frac{1+δ}{n^2}J_3,`

using Lemma 5(a) (with `g(0)=1` and `\int_K^\infty e^{−βx^2/n}dx ≤ T`)
for the first sum and Lemma 5(b),(c) (unimodal `x^3e^{−βx^2/n}`, and
`e^{−s(k)} ≤ (1+δ)e^{−βk^2/n}`) for the second. `∎`

**Numerical certificate.** Script `04` checks Theorem 1′ *verbatim*
(the definitions above are mirrored line-by-line) at all 30 points of
`γ ∈ \{0.1,0.3,0.5,0.7,0.9,1.0\} × n ∈ \{2^{10},2^{12},2^{14},2^{16},2^{18}\}`,
against a certified-truncation evaluation of `nφ`: **the sandwich
holds at every point** — including the single point
(`γ=0.1, n=1024`) where the side condition `K ≤ n/2` fails and the
theorem makes no claim.

> **Theorem 2 (the γ-scaling law; PROVED).** For every fixed
> `γ ∈ (0,1]`,
>
> `\displaystyle \lim_{n→∞} \frac{φ(n,γn)}{φ_∞(γn)} = \sqrt{\frac{2}{2−γ}}.`
>
> Quantitatively: with
> `Θ_n(γ) := \max\big(U/G_n − 1,\; 1 − \mathrm{Lo}/G_n\big)` and
> `\hat r_n := e^{−γn}/\sqrt{πγn}`, for all `n` with `K ≤ n/2` and
> `\hat r_n ≤ 1/2`:
>
> `\sqrt{\tfrac{2}{2−γ}}\,(1−Θ_n) \;≤\; \frac{φ(n,γn)}{φ_∞(γn)} \;≤\; \sqrt{\tfrac{2}{2−γ}}\,(1+Θ_n)(1+2\hat r_n),`
>
> and `Θ_n(γ) = \dfrac{Γ(5/4)}{\sqrt{2π}}\,β^{−3/4}\,n^{−1/4}\,(1+o(1)) → 0`
> (the constant is `Γ(5/4)/\sqrt{2π} = 0.36158…`).

*Proof.* By Theorem 1′, `φ(n,γn) = (G_n/n)(1+θ_n)` with
`|θ_n| ≤ Θ_n`. By Corollary 4.2 of THEOREM.md (PROVED there),
`φ_∞(γn) = L_n − R(γn)` with `L_n := (√π/2)(γn)^{−1/2}` and
`0 < R(γn) < e^{−γn}/(2γn)`; hence
`L_n(1−\hat r_n) ≤ φ_∞(γn) ≤ L_n` with
`\hat r_n = R/L_n ≤ e^{−γn}/\sqrt{πγn}`. Since
`(G_n/n)/L_n = \sqrt{γ/β} = \sqrt{2/(2−γ)}` **exactly**, the sandwich
follows, using `1/(1−\hat r_n) ≤ 1+2\hat r_n` for `\hat r_n ≤ 1/2`.

It remains to check `Θ_n(γ) → 0` with the stated asymptotics; each
piece is explicit: `δ = e^{γK/(2n)}−1 = O(\sqrt{γ\ln n/n})`;
`ω = K^3/(4n^2) = O_γ((\ln n)^{3/2}n^{−1/2}) → 0`;
`\frac{e^{ω}}{\sqrt2\,n}\,\frac{J_{3/2}}{G_n} = \frac{Γ(5/4)}{\sqrt{2π}}β^{−3/4}n^{−1/4}(1+o(1))`
(the dominant term; the `2\max` part of `J_{3/2}` is `O(n^{3/4})/n`
against `G_n = Θ(\sqrt n)`, i.e. `O(n^{−3/4})` relative);
`ρ/G_n`: the Chernoff part is `e^{−Ω(\sqrt{γ n\ln n})}`, and since
`γK^2/(4n) ≥ (γ/β)\ln n ≥ \ln n`, the Gaussian part of `ρ` is
`≤ \frac1n(1+\frac{2n}{γK}) = O_γ(n^{−1/2}(\ln n)^{−1/2})`, so
`ρ/G_n = O_γ(n^{−1})`; `(1+T)/G_n = O_γ(n^{−1/2})` (as
`βK^2/n ≥ 4\ln n` makes `T = O(n^{−7/2})`);
`(1+δ)J_3/(n^2 G_n) = \frac{1}{\sqrt π}β^{−3/2}n^{−1/2}(1+o(1))`.
The `n^{−1/4}` term dominates. `∎`

---

## §6 Corollaries: uniformity, moving `γ`, endpoint

> **Corollary 1 (uniform on compacts of `(0,1]`; PROVED — stretch
> goal 1).** For every `γ_0 ∈ (0,1]`,
> `\displaystyle \sup_{γ∈[γ_0,1]}\Big|\frac{φ(n,γn)}{φ_∞(γn)} − \sqrt{\tfrac{2}{2−γ}}\Big| \xrightarrow[n→∞]{} 0.`

*Proof.* Every envelope term in Theorem 2 is an explicit elementary
function of `(γ,n)`, and on `[γ_0,1]` each is dominated by its value
with the worst constant: `β ∈ [β_0, 1/2]` with `β_0 := γ_0(2−γ_0)/2`,
so `K(γ) ≤ \lceil\sqrt{(4/β_0)n\ln n}\rceil`, `ω`, `δ`, `J_{3/2}/G_n`,
`J_3/(n^2G_n)`, `T/G_n`, `1/G_n` are all uniformly `O_{γ_0}(n^{−1/4})`
or smaller by the displayed formulas (each is monotone in `β` in the
direction controlled by `β_0`, and `G_n ≥ \tfrac12\sqrt{2πn}` uniformly
since `β ≤ 1/2`); in `ρ`, `a_γ ≥ a_{γ_0}` and
`γK^2/(4n) ≥ \ln n` *independently of `γ`*; and
`\hat r_n ≤ e^{−γ_0 n}/\sqrt{πγ_0 n}` (the function `e^{−c}/\sqrt{πc}`
is decreasing). The side conditions `K ≤ n/2`, `\hat r_n ≤ 1/2` hold
for all `γ∈[γ_0,1]` once `n ≥ n_1(γ_0)`. Hence the two-sided bound of
Theorem 2 holds with a single `γ`-free envelope `\bar Θ_n(γ_0) → 0`,
and `\sqrt{2/(2−γ)} ≤ \sqrt2` is bounded. `∎`

> **Corollary 2 (moving `γ_n`, including `γ_n → 0`; PROVED — stretch
> goal 2).** Let `γ_n ∈ (0,1]` satisfy `γ_n\,n^{1/3}/\ln n → ∞`. Then
> `\dfrac{φ(n,γ_n n)}{φ_∞(γ_n n)} − \sqrt{\dfrac{2}{2−γ_n}} \xrightarrow[n→∞]{} 0.`
> In particular, if additionally `γ_n → 0`, the ratio `→ 1`: the
> `γ`-law connects continuously to the fixed-`c` regime (where the
> ratio is identically `1` in the limit, THEOREM.md Teorema 3/A/C), and
> if `γ_n → γ^* ∈ (0,1]`, the ratio `→ \sqrt{2/(2−γ^*)}`.

*Proof.* Nothing in Theorems 1′/2 used that `γ` is constant in `n`;
it suffices that every envelope term → 0 when `γ=γ_n`. Using
`γ/2 ≤ β ≤ γ`: the dominant terms are
`β^{−3/4}n^{−1/4} ≤ (γ/2)^{−3/4}n^{−1/4} → 0` iff `γ_n ≫ n^{−1/3}`;
`ω = K^3/(4n^2) ≤ (8/γ)^{3/2}(\ln n)^{3/2}/(4\sqrt n) → 0` iff
`γ_n ≫ \ln n\, n^{−1/3}`;
`β^{−3/2}n^{−1/2} → 0` iff `γ_n ≫ n^{−1/3}`;
`δ ≤ e^{\sqrt{2γ\ln n/n}}−1 → 0` always;
in `ρ/G_n`, `γK^2/(4n) ≥ \ln n` always, and
`a_γ(K+1) ≥ 0.15\sqrt{4γ n\ln n} → ∞` with
`1/(1−e^{−a_γ}) ≤ 1+1/a_γ = O(1/γ)` still killed by the exponential;
`K ≤ n/2` and `\hat r_n → 0` need only `γ_n n/\ln n → ∞`. All are
implied by `γ_n n^{1/3}/\ln n → ∞`. The hypotheses of Theorem 1′/2
hold for large `n` and the envelope → 0. `∎`

**Remark (what Corollary 2 does *not* claim).** For `γ_n` decaying
*faster* than `n^{−1/3}\ln n` (e.g. `γ_n = n^{−1/2}`, i.e.
`c = √n`), this front proves nothing; the fixed-`c` results of
Estágio 10 (Teorema C: absolute uniform convergence on all of
`[0,∞)`) still apply in absolute terms, but the *relative* statement
in the window `n^{ε} ≪ c ≪ n^{2/3}/\log` is left open — named here as
the natural residual gap.

> **Corollary 3 (endpoint `γ=1`; re-proved).** Theorem 2 at `γ=1`
> gives `φ(n,n)/φ_∞(n) → √2`, and — via Remark 1.2 and Theorem 1′ —
> reproves `Q(n) = \sqrt{πn/2}\,(1+O(n^{−1/4}))` without Stirling,
> Robbins, or FGKP95. This is consistent with (and strictly weaker in
> rate than) the Estágio 19 lineage's `Q(n)` bounds; it is recorded
> only as a consistency anchor, not as an improvement.

---

## §7 Numerics (all deterministic; no seeds consumed)

### 7.1 γ-grid convergence table (mandated deliverable)

`R(n,γ) := φ(n,γn)/φ_∞(γn)` computed by the float64 evaluator
(roundoff `< 10^{−15}` relative, V4/H1) with **certified truncation**
(tail bound (2.1) `< 10^{−13}` relative at every printed point —
column `tailbnd/phi` of the log). Excerpt at `n = 2^{18} = 262144`
(full 11×11 table in `02_gamma_grid_convergence.log`):

| γ | target `√(2/(2−γ))` | `R(262144, γ)` | `R − target` | `√n·(R−target)` |
|------|---------------|---------------|------------|-----------|
| 0.1 | 1.025978352085 | 1.0256418673 | −3.365e−04 | −0.172280 |
| 0.2 | 1.054092553389 | 1.0536343736 | −4.582e−04 | −0.234588 |
| 0.3 | 1.084652289093 | 1.0841136908 | −5.386e−04 | −0.275762 |
| 0.4 | 1.118033988750 | 1.1174389803 | −5.950e−04 | −0.304644 |
| 0.5 | 1.154700538379 | 1.1540659874 | −6.346e−04 | −0.324890 |
| 0.6 | 1.195228609334 | 1.1945670586 | −6.616e−04 | −0.338714 |
| 0.7 | 1.240347345892 | 1.2396676769 | −6.797e−04 | −0.347991 |
| 0.8 | 1.290994448736 | 1.2903013199 | −6.931e−04 | −0.354882 |
| 0.9 | 1.348399724926 | 1.3476917252 | −7.080e−04 | −0.362496 |
| 0.99 | 1.407195089461 | 1.4064644540 | −7.306e−04 | −0.374085 |
| 1.0 | 1.414213562373 | 1.4134793898 | −7.342e−04 | −0.375896 |

**Convergence diagnostics** (per γ, over `n = 2^8 … 2^{18}`):
`err(n/2)/err(n)` climbs monotonically to `1.414 = √2` at every γ
(final column of the log; e.g. `1.411 → 1.414` for γ=0.5), i.e. the
empirical error is `Θ(n^{−1/2})` — strictly better than the proved
`O(n^{−1/4})` envelope; and `√n·(R−target)` stabilizes to a
γ-dependent constant (see §7.3). The approach to the limit is from
**below** at every γ (`R < target`), consistent with `C(γ) < 0`.

### 7.2 Proof-inequality audits and high-precision cross-checks

- Lemma 3 (T), Lemma 4 upper (I+) and lower (I−): **0 violations**
  over `k=1..K_n` at `(n,γ)=(65536,0.3)` and `(65536,0.8)` (script 02).
- Theorem 1′ sandwich: holds at **30/30** grid points (script 04),
  checked against certified-interval values of `nφ`.
- mpmath dps=40 full-sum evaluation at `n=4096, γ∈\{0.3,0.7\}` agrees
  with the float64 pipeline to `1.4·10^{−15}` relative (script 03, H1).
- `φ_∞` two ways (closed form vs direct quadrature of
  `\int_0^1 e^{−ct^2}dt`): agreement to 40+ digits; Corollary 4.2's
  envelope `|φ_∞ − (√π/2)c^{−1/2}| ≤ e^{−c}/(2c)` confirmed (03, H2).
- Gaussian sum-vs-integral defect: `|Σ−G_n| ≈ 0.5 ≤ 1` at 8 points
  (03, H3). γ=1 anchor `R(n,1) → √2` via exact `Q(n)` recursion up to
  `n=2·10^5` (03, H4), matching the γ=1.0 column of 02 computed by the
  completely different `A_k` route.

### 7.3 Second-order term (bonus; PROVED at γ=1, CONJECTURED else)

Pushing the expansion of §3–§5 one order deeper (heuristically —
second-order Taylor of `E[e^{−(σ_k(M)−s(k))}]` using `E D = 0`,
`E D^2 = γ(1−γ)k`; the `x^2/2` term of `−\ln(1−x)`; the `e^{γk/(2n)}`
factor; Euler–Maclaurin `−\tfrac12`; then Gaussian moments
`\sum k\,e^{−βk^2/n} ≈ n/(2β)`, `\sum k^3 e^{−βk^2/n} ≈ n^2/(2β^2)`)
yields, after exact cancellation of all `O(k/n)`-level terms
(`−\tfrac12 + \frac{γ(2−γ)}{4β} = 0`),

`\sqrt n\,\Big(\frac{φ(n,γn)}{φ_∞(γn)} − \sqrt{\tfrac{2}{2−γ}}\Big) \;\longrightarrow\; C(γ) := −\frac{2}{3\sqrt π}\,\sqrt γ\;\frac{6−8γ+3γ^2}{(2−γ)^2}.`

**Status: CONJECTURED for `γ∈(0,1)`** (the interchange of expansion
and summation and the error accounting are not done rigorously);
**PROVED at `γ=1`**, where `C(1) = −2/(3\sqrt π)` follows from
`Q(n) = \sqrt{πn/2} − \tfrac13 + O(n^{−1/2})` (Robbins 1955 +
FGKP95 `θ(n) → 1/3`, both independently verified in the Estágio 19
lineage) via `R(n,1) = (Q(n)/n)/φ_∞(n)`.

**Numerical test** (script 05): Richardson extrapolation of
`x_n := \sqrt n(R_n − \text{target})` from `n = 131072, 262144`
(model `x_n = C + b/\sqrt n`) against the closed form, at 11 values
of γ: worst relative deviation **5.1·10⁻⁷**. Sample:

| γ | `C_est` (extrapolated) | `C(γ)` (closed form) |
|------|------------|------------|
| 0.1 | −0.172317 | −0.172317 |
| 0.5 | −0.325064 | −0.325064 |
| 0.9 | −0.362723 | −0.362723 |
| 1.0 | −0.376126 | −0.376126 = `−2/(3√π)` |

---

## §8 Scorecard, honesty, files

### Scorecard

| Claim | Status |
|---|---|
| Lemma 1 (exact double-sum formula for `φ(n,c)`, all `n`, all `q∈[0,1]`) | **PROVED** (+4-way exact validation) |
| Lemma 2 (product sandwich), Lemma 3 (a priori decay + certified truncation), Lemma 5 (sum–integral) | **PROVED** (elementary, self-contained) |
| Lemma 4 (Gaussian replacement) | **PROVED** (modulo Hoeffding's lemma, CITED classical; scalar form grid-checked) |
| Theorem 1′ (explicit finite-`n` sandwich for `nφ(n,γn)`) | **PROVED**; numerically certified 30/30 |
| **Theorem 2: `φ(n,γn)/φ_∞(γn) → √(2/(2−γ))`, every fixed `γ∈(0,1]`** | **PROVED** — the mandate's target, with rate `O_γ(n^{−1/4})` |
| Corollary 1 (uniform in `γ` on `[γ_0,1]`) | **PROVED** (stretch goal 1) |
| Corollary 2 (moving `γ_n`; `γ_n→0` recovers ratio → 1 when `γ_n n^{1/3}/\ln n→∞`) | **PROVED** (stretch goal 2, with an explicitly named residual window) |
| Endpoint `γ=1` (`√2`; `φ(n,n)=Q(n)/n`) | **re-PROVED** independently (Remark 1.2, Corollary 3) |
| True rate `Θ(n^{−1/2})` of the ratio error | **characterized numerically** (diagnostic `err(n/2)/err(n) → √2`), NOT proved (proved rate is `n^{−1/4}`) |
| Second-order constant `C(γ) = −\frac{2}{3\sqrt π}\sqrt γ\,(6−8γ+3γ^2)/(2−γ)^2` | **PROVED at `γ=1`; CONJECTURED for `γ∈(0,1)`** (7-digit numerical match at 11 γ's) |

### What remains open (named precisely)

1. A *proved* `n^{−1/2}` rate and a *proved* second-order term for
   `γ∈(0,1)` (would need a rigorous Edgeworth-level version of §7.3's
   expansion — the natural next front).
2. The relative scaling law in the intermediate window
   `c = c_n` with `n^{ε} ≤ c_n ≤ n^{2/3}/\log` (between Estágio 10's
   fixed-`c` regime and Corollary 2's `γ_n ≥ n^{−1/3}\ln n` regime).

### Self-caught issues (disclosed)

1. **Vacuous first-draft envelope (mathematical, caught by own
   audit).** The first assembly used sup-form error factors
   `(1±τ_n)`, `τ_n = K^3/n^2` and `(1+ε_{K})` — asymptotically valid
   but numerically vacuous at practical `n` (script 02's audit showed
   the allowed slack reaching `10^{18}` at `n=65536`). Restructured to
   integral-weighted error sums (`J_{3/2}`, `J_3`), giving the
   non-vacuous Theorem 1′. No claim was ever based on the discarded
   draft.
2. **Impractical side condition (mathematical, caught before
   publication).** An intermediate version bounded `e^{k^3/(4n^2)} ≤
   e^{1/4}` under the side condition `K ≤ n^{2/3}`, which fails at all
   practically testable `n`; replaced by the explicit factor `e^{ω}`,
   leaving only `K ≤ n/2`. (The numerical certificate had held even
   beyond the old condition, but the statement now matches what is
   actually provable and testable.)
3. **Performance bug (computational only).** Script 04 originally
   evaluated `nφ` by the full `k=1..n` sum (`O(n^2)` work), timing out
   at `n=65536`; switched to certified truncation via (2.1). No
   numerical value changed (interval semantics reported).

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_validate_exact_formula.py` / `.log` | Lemma 1 validation V1–V4 (exact rational; brute force `n=3,4,5`; `Q(n)/n` `n≤400`; mixture inversion vs Estágio 3/4 forms; roundoff control) |
| `02_gamma_grid_convergence.py` / `.log` | γ-grid `γ∈\{0.1..0.9,0.99,1.0\} × n∈\{2^8..2^{18}\}` with certified truncation; convergence diagnostics; proof-inequality audits (I−)/(I+)/(T) |
| `03_highprec_spotcheck.py` / `.log` | mpmath dps=40 cross-checks H1–H4 (independent arithmetic path; `φ_∞` two ways; Gaussian-sum defect; exact-`Q` γ=1 anchor) |
| `04_assembly_envelope_check.py` / `.log` | Theorem 1′ sandwich certified verbatim at 30 grid points; scalar Hoeffding grid check |
| `05_second_order_conjecture.py` / `.log` | Richardson-extrapolation test of the conjectured `C(γ)` (worst deviation 5.1·10⁻⁷) |

No Millennium Problem claims; pure combinatorial mathematics internal
to this archive. No git commits made by this front.
