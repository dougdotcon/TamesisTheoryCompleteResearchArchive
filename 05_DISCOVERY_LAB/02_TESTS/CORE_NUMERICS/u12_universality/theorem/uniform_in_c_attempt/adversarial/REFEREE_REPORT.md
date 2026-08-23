# Adversarial referee report — `uniform_in_c_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent re-verification of Wave 11 front (a),
> `UNIFORM-IN-C-TEOREMA-3-ATTEMPT`, before catalogue. Priority order set by the
> orchestrating session: (1) Lema 3.1, (2) Teorema A, (3) Lema 4.1 / Corolário
> 4.2 / Teorema C — the two genuinely new analytic inputs and the two headline
> unconditional theorems — then §§5–7 and the honesty audit.
>
> **Discipline.** Everything below was derived by hand first and then coded from
> scratch. No `.py` file in the parent directory was read at any point, before
> or after. `ATTEMPT.md`'s prose (the object under test), `THEOREM.md`, and
> `error_constant_growth_attempt/ATTEMPT.md` §6 were read (read-only, cited,
> never edited). Everything reported as exact uses `fractions.Fraction` or
> `sympy.Rational`; `mpmath` at 30–40 dps for quadrature; `numpy.float64` only
> for the large-`n` sweeps, with a precision audit (§0.1 below). Nothing outside
> this `adversarial/` directory was created, modified or touched. No git commit
> was made.
>
> **Randomness.** One use only (the raw-model Monte Carlo of §7.4). Fresh
> `numpy.random.SeedSequence()`:
> ```
> SeedSequence entropy = 141469625505148724570726930541814868012
> ```

---

## 0. Executive summary

**Verdict: SPLIT, overwhelmingly positive on the load-bearing claims.**

The two headline unconditional theorems survive a deliberate attempt to break
them. I re-derived Lema 3.1, Teorema A, Lema 4.1, Corolário 4.2 and Teorema C
from scratch, checked every inequality in each chain separately rather than only
the end-to-end bound, and found **no error of any kind**. The same holds for
Lema 5.1, Lema 6.1, Corolário 6.2, Teorema B's Jensen step, Teorema D,
Proposição 5.2 and Proposição 7.1. The `e_j` closed form, which I re-derived by
an independent route (resumming Teorema D's finite alternating sum in closed
form, never using Proposição 5.2 as input), came out *exactly* right, including
the cancellation `1 - j(2j-1) = -(2j+1)(j-1)` that produces the `(j-1)²`.

**One substantive finding (F-1), and it points the other way from the usual
failure mode: the document is internally inconsistent about *why* Teorema E is
conditional, in a way that makes its own gap look better-founded than it is.**
§5.6 asserts (i) "*any* geometric growth `D_K(0)=O(λ^K)` suffices", (ii)
"Estágio 8's Proposição 6 *does prove* the improved constants `D'_r(b)` are
geometric", and then (iii) declares Teorema E conditional because the *rate* of
that geometric bound is only numerically characterized. (i)+(ii) contradict
(iii): if the sufficiency criterion is qualitative geometricity and that is
proved, the explicit constant is irrelevant and Teorema E would be
unconditional. Having read the cited source, the correct resolution is that
**(ii) overstates Estágio 8** — its own §6.3 status table downgrades `D'_r(b)`
to "PROVED bound; rate NUMERICALLY CHARACTERIZED", §6.1 supplies no proof of
geometricity, and the geometricity of the inputs `A_r(b),B_r(b)` is itself only
"NUMERICALLY CHARACTERIZED, mechanism proved". So the **label PROVED-MODULO on
Teorema E is correct**, but the stated reason for it is a non-sequitur, and the
gap it names ("an explicit-constant geometric bound") is *not* the gap that is
actually open (a written-down proof of *qualitative* geometric growth of `M_K`).
This needs a one-paragraph rewrite, not a retraction.

**Two genuine, minor overclaims in the Executive Summary (F-2, F-3)** — exactly
the pattern prior referees in this lineage were told to hunt: qualifiers present
in §7 and in the Scorecard are dropped in the summary prose. Neither touches
Teorema A or Teorema C.

**Teorema A and Teorema C are never anywhere claimed to carry an explicit rate.**
I checked every occurrence of "rate" in the document. §3.3, §8 item 1 and §10
bullet 1 each disclaim it explicitly and correctly. On this specific point the
document is scrupulous.

Every numerical table I could reach — §2.3's validation rows, §4.1's `C_0`-tail
values, §5.4's finite-`n` Taylor convergence, §5.5's landmarks, §5.6's
`sup|e|` column, §7.1's `√n φ(n,n)`, §7.2's six-row `γ` table, §7.3's global-sup
table — reproduces on my own independent engine, to every digit printed.

I also found a small **strengthening** the document leaves on the table (S-1):
its §6.3 mechanism for `a*` is exact, not approximate.

---

## 0.1 Independent engine, and its validation

`ref_engine.py` implements, from Definition 1 and from the *prose* of
`ATTEMPT.md` §2.1 only:

* `raw_phi(n,q)` — brute-force enumeration of the **raw** Definition-1 model:
  every permutation `π` of `[n]` (`n!` terms), every mark subset `S` (`2^n`
  terms) weighted `q^{|S|}(1-q)^{n-|S|}`, every reroute-target tuple (`n^{|S|}`
  terms) weighted `n^{-|S|}`, then a direct cycle test on the resulting `f`.
* `chain_phi(n,q)` — the `(j,R)` backward recursion (2.1).
* `chain_phiK(n,K)` / `phiK_fast(n,K)` — the conditional-`K` version.

| check | result |
|---|---|
| `raw_phi == chain_phi`, exact `Fraction`, `n=2,3,4` × `q∈{0,¼,⅓,½,⅔,1}` | **18/18 exact** |
| `φ_n^{(0)}=1`, `φ_n^{(1)}=2/3+1/(3n²)`, `n=1..10` | exact |
| `φ_n^{(2)}` table `n=2..8` (`3/4,17/27,113/192,356/625,151/270,569/1029,281/512`) | exact 7/7 |
| `φ_7^{(6)}=355081/823543` | exact |
| mixture identity (7.1), `n=2..7` × 4 values of `q` | exact 24/24 |
| `φ(n,n)=Q(n)/n`, `n=1..11` | exact 11/11 |
| raw-model Monte Carlo, 5 cells × `2·10⁵` reps | all within 3 s.e. |
| float64 vs exact `Fraction`, `n≤80` | max discrepancy `2.2·10⁻¹⁶` |

The `(j,R)` representation is therefore faithful to the raw model on my own
evidence, independently of the orchestrating session's check and of the
document's derivation. The backward recursion has all-positive coefficients and
values in `[0,1]`, so it is forward-stable; float64 at `n=4000` is safe.

*Files: `ref_engine.py` / `.log`.*

---

## 1. Lema 3.1 (equi-Lipschitz) — **SOUND**

### 1.1 The coupling, rebuilt

Take `0 ≤ c < c' ≤ n`. On one probability space put `V_1,…,V_n` i.i.d.
`Unif(0,1)`, `ξ_i := 1{V_i < c/n}`, `ξ'_i := 1{V_i < c'/n}`, and share **one**
uniform permutation `π` and **one** family `U_1,…,U_n` of i.i.d. `Unif[n]`.

*Marginals.* `(π,ξ,U)` has exactly the Definition-1 law at `c`; `(π,ξ',U)`
exactly the law at `c'`. Both hold because `ξ_i` are i.i.d. `Bern(c/n)`, `ξ'_i`
are i.i.d. `Bern(c'/n)`, and `π,U` are independent of the `V`'s in both. ✔

*The event.* On `E := {ξ_i = ξ'_i ∀i}`, `f(x) = U_x1{ξ_x=1} + π(x)1{ξ_x=0}`
agrees with `f'(x)` **term by term at every `x`** — the shared `π` and shared
`U` are what make this work, and both are genuinely needed. So `f = f'` as maps
and the indicator `1{1 cyclic}` agrees pointwise on `E`. ✔

*The bound.* `|φ(n,c)-φ(n,c')| = |E[1_A - 1_{A'}]| ≤ E|1_A - 1_{A'}| = P(A △ A')
≤ P(E^c) ≤ Σ_i P(ξ_i≠ξ'_i) = n·(c'-c)/n = c'-c`. ✔

*The reduction to `c' ≤ n`.* The document says "by the convention of §1 it
suffices to treat `0≤c<c'≤n`" and leaves it there; I checked it. Under
`q = min(c/n,1)`, `φ(n,·)` is constant on `[n,∞)`, so for `c ≤ n < c'` the LHS
is `|φ(n,c)-φ(n,n)| ≤ n-c ≤ c'-c`, and for `n ≤ c < c'` it is `0`. Valid, and
necessary — without it the coupling has no meaning for `c' > n`. ✔

The constant `1` is uniform in `n` because the union bound over `n` terms
cancels the `1/n` in each. That is the whole point and it is correct.

### 1.2 Stress test

All `624` pairs on a 13-point `q`-grid, `n=1..8`, exact `Fraction`: **0
violations**, worst ratio `|Δφ|/|Δc| = 0.287054` (`= 5812841/20250000`),
comfortably below `1` and below the sharp `1/3` of §3.2.

### 1.3 The non-monotonicity remark (F-8, nit)

The `n=3` example reproduces exactly: `π=(1 2 3)`, reroute `{1}` with `U_1=1`
gives `f = [1,3,1]`, cyclic points `{1}`, count 1; reroute `{1,2}` with
`U_1=1,U_2=2` gives `f = [1,2,1]`, cyclic points `{1,2}`, count 2. Adding a
reroute increased the cyclic **count**. ✔

But note what it does *not* show: `1` is cyclic in **both** configurations, so
this example does not by itself establish that the *event* `{1 cyclic}` — the
only functional `φ(n,·)` depends on — is non-monotone. Here is a counterexample
that does, and that lives inside Lema 3.1's own shared-`(π,U)` coupling:

> `n=2`, `π = id`, `U_1 = 2`, `U_2 = 1`.
> `ξ = (1,0)`: `f = [2,2]` → `1` **not** cyclic.
> `ξ' = (1,1)`: `f' = [2,1]` → `1` **is** cyclic.
> Same `π`, same `U`, `ξ ≤ ξ'` pointwise, indicator goes `0 → 1`.

So the document's *conclusion* ("no coupling proof of monotonicity is
available") is right; its stated example is weaker than its conclusion. Nothing
downstream depends on either — Lema 3.1 does not use monotonicity, and neither
does anything built on it.

### 1.4 A wording inconsistency (F-5, nit)

Scorecard row 2 calls it a "one-line **monotone** coupling", and §10 repeats
"Lema 3.1's monotone coupling". The coupling **of the marks** is indeed monotone
(`ξ_i ≤ ξ'_i` pointwise), so the term is defensible; but placed next to §3.1
remark (ii)'s "it is not pointwise-monotone" it reads as a contradiction. Either
drop "monotone" or say "monotone in the marks".

*Files: `ref_lipschitz.py` / `.log`.*

---

## 2. Teorema A — **SOUND, unconditional**

### 2.1 The `φ_∞` Lipschitz sub-bound

`|d/dc e^{-ct²}| = t²e^{-ct²} ≤ t²`, integrable and uniform in `c ≥ 0`, so
differentiation under the integral is legitimate and
`φ_∞'(c) = -∫₀¹t²e^{-ct²}dt`. Hence for every `c ≥ 0`

`|φ_∞'(c)| = ∫₀¹t²e^{-ct²}dt ≤ ∫₀¹t²dt = 1/3`,

with the sup `1/3` attained only at `c=0`. Verified numerically (`c=0`:
`0.333333`; `c=1`: `0.189472`; `c=5`: `0.038897`; `c=50`: `0.001253`). ✔ So
`φ_∞` is `1/3`-Lipschitz on all of `[0,∞)`, not merely on compacts.

### 2.2 The constant `4/3` and the grid inequality

`Δ_n = φ(n,·) - φ_∞` is therefore Lipschitz with constant `1 + 1/3 = 4/3`,
**uniformly in `n`** — the `1` from Lema 3.1 (uniform in `n`) and the `1/3` from
`φ_∞` (no `n` in it at all). With `c_i := iC/M`, every `c ∈ [0,C]` lies in some
`[c_i,c_{i+1}]` of width `C/M`, so

`|Δ_n(c)| ≤ |Δ_n(c_i)| + (4/3)(C/M)`,  hence  `ω_n(C) ≤ max_i|Δ_n(iC/M)| + 4C/(3M)`. ✔

Audited directly at six `(n,C,M)` cells against `ω_n(C)` computed on a
2001-point grid: holds in every cell. (Taking the *nearest* grid point rather
than the left endpoint would give `2C/(3M)`; the stated `4C/(3M)` is valid but a
factor 2 loose. Harmless.)

### 2.3 The `ε`-argument

Fix `ε>0`; choose `M` with `4C/(3M) < ε/2`; apply Teorema 3 (Estágio 6,
unconditional — confirmed as such in `THEOREM.md`) at each of the **finitely
many** points `c_0,…,c_M` to get `N` with `max_i|Δ_n(c_i)| < ε/2` for `n ≥ N`;
conclude `ω_n(C) < ε`. Standard, correctly executed, and genuinely unconditional
— it consumes only Teorema 3 and Lema 3.1. ✔

**No rate is produced and none is claimed.** `N` inherits Teorema 3's
unquantified convergence. §3.3 says so explicitly ("the *qualitative* part").

---

## 3. Lema 4.1 and Corolário 4.2 — **SOUND**; Teorema C — **SOUND, unconditional**

This is the item I attacked hardest, and the one the brief flagged for the
first-return/double-counting risk. I audited **each of the six steps
separately** using an exact forward pass on the chain, not just the end-to-end
inequality (a loose final bound would hide an error in any single step).

### 3.1 The forward pass

With `μ_j(R) = P(alive at step j, R reroutes so far)`, `μ_0(0)=1`:

```
return hazard  r(j,R) = q/n + (1-q)/(n-j+R)
fatal  hazard  F(j,R) = q·j/n + (1-q)·R/(n-j+R)
fresh -> (j+1,R+1)    q(n-j-1)/n
fresh -> (j+1,R)      (1-q)(n-j-1)/(n-j+R)
```

I asserted `r + F + fresh = 1` **identically** at every reachable state
(`assert` in the loop; it never fired) — which also re-confirms the `(j,R)`
branch table of §2.1 as a genuine probability decomposition.

### 3.2 The decomposition — is it legitimate? **Yes, and the worry is vacuous**

The brief warns against conflating "return at step `j`" with "*first* return at
step `j`". In this process the distinction **does not exist**: the exploration is
absorbed the first time it returns to `x_0` and absorbed the first time it lands
on `x_1,…,x_j`, so with `A_j = {alive at j}`, `Rt_j = A_j ∩ {step j returns}`,
`Ft_j = A_j ∩ {step j fatal}` one has `A_{j+1} = A_j \ (Rt_j ⊔ Ft_j)`. The
`Rt_j` are pairwise disjoint **by construction** (each sits inside `A_j`, which
is decreasing and already excludes every earlier return). A state cannot return
twice. And at `j = n-1` there is no fresh branch (`n-j-1 = 0`), so the
decomposition is exhaustive.

Confirmed exactly: over `n ∈ {2,3,5,8,12}` × 6 values of `q`,
`Σ_j Rt_j == φ(n,c)` **exactly** and `Σ_j (Rt_j + Ft_j) == 1` **exactly** in all
30 cells. **No missing mass, no double counting.** ✔

### 3.3 The two conditional facts, audited cellwise

* **(a)** `r(j,R) = q/n + (1-q)/(n-j+R) ≤ q/(n-j) + (1-q)/(n-j) = 1/(n-j)`,
  using `n-j ≤ n` and `R ≥ 0`. Both unconditional. ✔
* **(b)** `F(j,R) = q·j/n + (1-q)·R/(n-j+R) ≥ q·j/n`, dropping a nonnegative
  term. ✔

Audited at **1875 reachable states** (`n∈{5,9,14,20}` × 5 values of `q` × all
`(j,R)`): **0 violations**. Worst tightness of (a) is exactly `1.000000`
(attained at `j=0`, where `r = q/n+(1-q)/n = 1/n` exactly), worst tightness of
(b) exactly `1.000000` (attained at `q=1`, where the permutation branch has zero
weight). Both bounds are therefore tight somewhere — they are not slack
mis-statements.

### 3.4 The tower-property product — the step the brief singled out

The concern is that (b) is a **conditional** lower bound given the history, not
an unconditional one. The document's argument is correct precisely because the
bound `q·j/n` is **deterministic**:

`P(A_{j+1}) = E[1_{A_j}(1 - r - F)] ≤ E[1_{A_j}(1 - F)] ≤ E[1_{A_j}(1 - qj/n)]
= P(A_j)(1 - qj/n)`,

the last equality because `qj/n` is a constant that pulls out of the
expectation. Nonnegativity of the factor needs `qj/n ≤ 1`, true since `q ≤ 1`
and `j < J ≤ n/2 < n`. Iterating and using `1-u ≤ e^{-u}`:

`P(A_J) ≤ Π_{j<J}(1-qj/n) ≤ exp(-(q/n)Σ_{j<J}j) = exp(-qJ(J-1)/(2n))`. ✔

Had (b) been a bound on an *unconditional* probability the product would have
been illegitimate. It is not, and the document uses it correctly.

### 3.5 The remaining steps

* `Σ_{j<J} Rt_j ≤ Σ_{j<J} P(A_j)/(n-j) ≤ Σ_{j<J} 1/(n-j) ≤ J/(n-J+1) ≤ J/(n-J)`
  (largest of `J` terms is `1/(n-J+1)`). ✔
* `Σ_{j≥J} Rt_j ≤ P(A_J)`: those events are disjoint and all contained in
  `A_J`. ✔ This is the step that replaces the tail of the return series, and it
  is exact bookkeeping, not an estimate.
* `J/(n-J) ≤ 2J/n` for `J ≤ n/2`. ✔

Every one of these was verified numerically cell-by-cell (64 `(n,q,J)` cells,
table in `ref_tail.log` §C): **all six inequalities hold in every cell.**

### 3.6 Adversarial sweep for a counterexample to Lema 4.1

Exhaustive over `n = 2..40`, `q ∈ {0,1/100,1/10,1/4,1/2,3/4,1}`, and **every**
admissible `J` from `1` to `⌊n/2⌋` — **2800 cells, 0 violations**. Worst ratio
`φ/bound = 0.975000`, at the degenerate corner `(n,q,J) = (40,0,1)` where
`φ(n,0)=1` and the bound is `1/39 + 1 = 1.0256`. (The document reports a
looseness factor `2.5–4.2` over its own grid, which starts at `c=5`; no conflict.)

### 3.7 Corolário 4.2 — the algebra, re-derived

* Monotonicity in `c`: the RHS of Lema 4.1 depends on `c` only through
  `q = min(c/n,1)` and is non-increasing in `q`; for `c ≥ C_0` and `n ≥ C_0` we
  have `q ≥ C_0/n`, so evaluating at `q = C_0/n` suffices. ✔
* `J := ⌈n√(2L/C_0)⌉ + 1` depends only on `(n,C_0,L)`. Then `J-1 ≥ n√(2L/C_0)`
  and `J ≥ J-1`, so `qJ(J-1)/(2n) ≥ (C_0/n)·n²(2L/C_0)/(2n) = L`. ✔
* Admissibility `J ≤ n/2`: `C_0 ≥ 16L` gives `√(2L/C_0) ≤ 1/√8 = 0.353553`, so
  `J ≤ 0.353553n + 2 ≤ n/2` iff `n ≥ 13.66`; `n ≥ C_0 ≥ 80` supplies it. ✔
* `J/(n-J) ≤ 2J/n ≤ 2√(2L/C_0) + 4/n`. ✔

The "in particular" with `L = log C_0`: `e^{-L} = 1/C_0` ✔, `L ≥ 1` needs
`C_0 ≥ e` ✔, and `C_0 ≥ 16 log C_0` first holds at `C_0 = 67.36` (computed), so
the stated threshold `C_0 ≥ 80` is safe and is doing real work. ✔ Audited
directly at 9 `(C_0,n)` cells against the exact chain: holds everywhere with
margin.

### 3.8 Teorema C

`φ_∞(C_0) ≤ ∫₀^∞e^{-C_0t²}dt = √π/(2√C_0) → 0` ✔ and `ω(C_0) → 0` ✔, so
`C_0 ≥ 80` with `ω(C_0)+φ_∞(C_0) < ε/2` exists. For `c ≥ C_0`,
`|Δ_n(c)| ≤ φ(n,c)+φ_∞(c) ≤ ω(C_0)+4/n+φ_∞(C_0)` (Corolário 4.2 plus
monotonicity of `φ_∞`), so `sup_{c≥C_0}|Δ_n| < ε/2 + 4/n`. Teorema A gives
`sup_{[0,C_0]}|Δ_n| < ε/4` for `n` large. With `n ≥ max(C_0,16/ε)`, `4/n ≤ ε/4`,
so `sup_{c≥C_0}|Δ_n| < 3ε/4` and `sup_{[0,C_0]}|Δ_n| < ε/4`; combining,
`sup_{c≥0}|Δ_n| < ε`. ✔ The `ε`-bookkeeping is slightly generous but correct.

**Teorema C is sound, unconditional, and correctly flagged as depending on
Definition 1's own `q = min(c/n,1)` convention** — which I confirmed is quoted
verbatim from `THEOREM.md` line 111.

### 3.9 §4.1's "`C_0`-tail values" (F-10, nit)

The five figures `0.531, 0.259, 0.116, 0.053, 0.025` at
`C_0 = 50,200,10³,5·10³,2.5·10⁴` are **not** `ω(C_0)` of Corolário 4.2 (which
is `0.811, 0.465, 0.236, 0.117, 0.057` — 1.5–2× larger) and **not** the actual
`sup_{c≥C_0}φ(n,c)` (which at `C_0=10³` is `0.029–0.039`, 3–4× smaller). They
are the **`J`-optimised Lema 4.1 bound** at `q = C_0/n`, i.e.
`min_{x∈(0,½)} [x/(1-x) + exp(-C_0x²/2)]` in the large-`n` limit. I reproduced
all five independently: `0.5297, 0.2586, 0.1158, 0.0533, 0.0248`. ✔ Correct
numbers, and consistent with "essentially identical at `n=10³,10⁴,10⁵`" since
the limit is `n`-free — but the sentence is ambiguous enough that a reader could
take them for `ω(C_0)`. Worth one clarifying clause.

### 3.10 "uniformly in `n`" (F-11, nit)

Executive summary point 2 says Lema 4.1 "forces `sup_{c≥C_0}φ(n,c)→0` as
`C_0→∞` uniformly in `n`". Strictly it is uniform in `n ≥ C_0`: at `n=4`,
`C_0=80`, `sup_{c≥80}φ(4,c) = φ(4,4) = 71/128 = 0.555`. Corolário 4.2 itself
states "for every `n ≥ C_0`" correctly, and Teorema C's proof correctly takes
`n ≥ max(C_0,16/ε)`, so **nothing is broken** — only the compressed summary
phrase is loose.

*Files: `ref_tail.py` / `.log`.*

---

## 4. Lema 5.1, Lema 6.1, Corolário 6.2, Teorema B — all **SOUND**

### 4.1 Lema 5.1

`B_n(c) = Σ_K(b_K-p_K)φ_K` with `φ_K = ∫₀¹(1-t²)^K dt` (Lemma 2). Putting
`z := 1-t² ∈ [0,1]`, the binomial pgf gives `Σ_K b_K z^K = (1-(c/n)(1-z))^n =
(1-ct²/n)^n` (a **finite** sum, interchange free) and the Poisson pgf gives
`Σ_K p_K z^K = e^{-c(1-z)} = e^{-ct²}` (all terms nonnegative, Tonelli). Hence
`B_n(c) = ∫₀¹[(1-ct²/n)^n - e^{-ct²}]dt`, and for `c ≤ n` we have
`0 ≤ ct²/n ≤ 1`, so `1-u ≤ e^{-u}` gives `(1-ct²/n)^n ≤ e^{-ct²}` pointwise and
`B_n ≤ 0`. ✔ Verified sum-vs-integral at 6 values of `n` × up to 4 values of
`c`, worst discrepancy `1.3·10⁻⁴⁰` (mpmath 40 dps), and `B_n ≤ 0` in every cell.

### 4.2 Lema 6.1 — both branches of the case split

* **Left.** `1-u ≤ e^{-u}` with `u = x/n ∈ [0,1]`; both sides nonnegative so the
  `n`-th power preserves it. Needs only `x ≤ n`. ✔
* **Right, `x ≥ √n`.** Then `x²/n ≥ 1`, so `(x²/n)e^{-x} ≥ e^{-x} ≥ e^{-x} -
  (1-x/n)^n`, using `(1-x/n)^n ≥ 0` (again `x ≤ n`). ✔
* **Right, `x < √n`.** `u = x/n < 1/√n ≤ 1/2` for `n ≥ 4`. Then
  `(1-u)^n = e^{-n Σ_{k≥1}u^k/k} = e^{-x}e^{-y}` with `y = nΣ_{k≥2}u^k/k`
  (using `nu = x`), so `e^{-x}-(1-u)^n = e^{-x}(1-e^{-y}) ≤ e^{-x}y`
  (`1-e^{-y} ≤ y`), and `y ≤ (n/2)Σ_{k≥2}u^k = (n/2)u²/(1-u) ≤ nu² = x²/n`
  (`1-u ≥ 1/2`). ✔

The split is exhaustive, the boundary `x = √n` is covered by the first branch,
and each branch's hypotheses are met. Scanned at `4001` points for
`n ∈ {2,3,4,5,7,10,30,100,1000}`: left side never negative, max ratio to the
bound `0.563967` at `n=4` (matching the document's `0.564`), decreasing to
`0.500221` at `n=1000`. **F-13 (nit):** `n ≥ 4` is used *only* for
`1-u ≥ 1/2`; `n=2,3` also pass numerically (`0.652`, `0.590`), so the threshold
is an artefact of the proof, not of the statement. Harmless — the lemma is only
ever applied with `n` large.

### 4.3 Corolário 6.2 and `κ_B`

Applying Lema 6.1 at `x = ct² ∈ [0,c] ⊆ [0,n]`:
`|B_n(c)| ≤ ∫₀¹(c²t⁴/n)e^{-ct²}dt = c²I_2(c)/n ≤ κ_B/n`. ✔

My own computation: `argmax c* = 4.08675454645` (document: `4.086754546` ✔),
`κ_B = 0.280480169024586` (document: `0.280480169025` ✔). Agreement to `10⁻¹¹`.
Verified `|B_n(c)| ≤ c²I_2(c)/n ≤ κ_B/n` at 13 `(n,c)` cells. ✔

**F-9 (nit):** Executive summary point 4 says `κ_B` is "computed **exactly**
here". It is a high-precision *numerical* value of a transcendental supremum,
not a closed form. §6.1 itself writes it with a trailing ellipsis and is fine;
only the summary word "exactly" is loose.

### 4.4 Teorema B's Jensen step

`|A_n(c)| ≤ (a/n)E[√Bin(n,c/n)] ≤ (a/n)√(E Bin) = a√c/n` — `√` is concave so
Jensen runs the right way. ✔ Verified numerically at 4 `(n,c)` cells. Combined
with Corolário 6.2 this gives `|Δ_n(c)| ≤ (a√c + κ_B)/n` for `n ≥ 4`, `c ≤ n`.
**Correct given (U'ₐ)**, and correctly labelled as such everywhere.

*Files: `ref_lemmas.py` / `.log`.*

---

## 5. Teorema D — **SOUND, and the reasoning is airtight**

This is the document's key unconditional claim about the error profile, so I
tested the exact identity against an object that shares no machinery with it.

### 5.1 The exact finite formula, tested independently

The claim is that

`[c^j]φ(n,·) = (-1)^j (C(n,j)/n^j) Σ_{K=0}^{j} (-1)^K C(j,K) φ_n^{(K)}`

is **exact**, not asymptotic. I tested it against `φ(n,c)` built as an exact
**symbolic sympy polynomial** by running the `(j,R)` chain with `q = c/n` as a
symbol — a route that never uses the binomial identity, the mixture identity, or
`φ_n^{(K)}` at all. Result: for `n = 2,…,12`, **all `n+1` Taylor coefficients
match exactly, in every case** (91 coefficients total, `sympy.simplify(LHS-RHS)
== 0`). ✔

The underlying identity `C(n,K)C(n-K,j-K) = C(n,j)C(j,K)` is the "choose `j` of
`n`, then `K` of those `j`" double count; verified exhaustively for
`0 ≤ K ≤ j ≤ n ≤ 25`, 0 failures. ✔

The Poisson side, `[c^j]φ_∞ = ((-1)^j/j!)Σ_K(-1)^K C(j,K)φ_K = (-1)^j/(j!(2j+1))`,
follows from `Σ_K(-1)^K C(j,K)∫₀¹(1-t²)^K dt = ∫₀¹t^{2j}dt = 1/(2j+1)`; verified
exactly for `j=0..8`. ✔

### 5.2 Why no interchange of limits occurs — confirmed

For each fixed `j`, the sum has exactly `j+1` terms, all with `K ≤ j`. Inserting
`φ_n^{(K)} = φ_K + c_K/n + o(1/n)` for each of those finitely many `K`, and
`C(n,j)/n^j = (1/j!)Π_{i<j}(1-i/n) = (1/j!)(1 - C(j,2)/n + O(n^{-2}))`, and
multiplying out:

`[c^j]φ(n,·) = ((-1)^j/j!)[S + (T - C(j,2)S)/n] + o(1/n)`, `S = Σ(-1)^K C(j,K)φ_K`, `T = Σ(-1)^K C(j,K)c_K`,

so `n([c^j]φ(n,·) - [c^j]φ_∞) → ((-1)^j/j!)[T - C(j,2)S] = e_j`. ✔ **The
reasoning is airtight.** A finite sum of finitely many convergent sequences,
each with a known first-order expansion, times a scalar with a known
expansion — there is genuinely nothing to interchange.

*Minor note:* the document inserts `φ_n^{(K)} = φ_K + c_K/n + O_K(n^{-2})`,
citing Estágio 6/7. Estágio 7 as written states the **limit**
`lim n(φ_n^{(K)}-φ_K) = c_K`, i.e. an `o(1/n)` remainder. That weaker form
already suffices for Teorema D (shown above), so the argument is safe either
way; the stronger `O_K(n^{-2})` is available from Estágio 6's `D_K(0)/n²` bound
plus Reduction Lemma A, but the document does not need it here and might as well
not claim it.

### 5.3 `c_K` — the citation is accurate

`THEOREM.md` Estágio 7 Teorema A states `c_K = [(K+2)φ_K - 2]/4` exactly as
quoted. Confirmed numerically with my own `φ_n^{(K)}`: `n(φ_n^{(K)}-φ_K)` at
`n = 20,…,320` with two-point Richardson gives `0.000000, 0.000000, 0.033329,
0.071416, 0.181906` for `K = 0,1,2,3,6` against `c_K = 0, 0, 0.033333, 0.071429,
0.181985`. ✔ (`c_1 = 0` exactly, consistent with the `Θ(1/n²)` rate at `K=1`.)

### 5.4 Proposição 5.2 — re-derived independently

I derived the closed form **from Teorema D's finite sum**, without using
Proposição 5.2 as input. Using `φ_K = ∫₀¹(1-t²)^K dt`:

* `S_j = Σ_K(-1)^K C(j,K)φ_K = ∫₀¹t^{2j}dt = 1/(2j+1)`;
* `Σ_K(-1)^K C(j,K)Kφ_K = ∫₀¹ -j(1-t²)t^{2j-2}dt = -2j/((2j-1)(2j+1))`
  (from `Σ_K C(j,K)Kz^K = jz(1+z)^{j-1}` at `z = -(1-t²)`);
* hence `T_j = Σ_K(-1)^K C(j,K)c_K = (j-1)/(2(2j+1)(2j-1))` for `j ≥ 1`;
* hence `e_j = ((-1)^j/j!)[(j-1)/(2(2j+1)(2j-1)) - j(j-1)/(2(2j+1))]
  = ((-1)^j/j!)·(j-1)(1-j(2j-1))/(2(2j+1)(2j-1))`, and
  **`1 - j(2j-1) = -(2j+1)(j-1)`**, giving

  `e_j = (-1)^{j+1}(j-1)²/(2(2j-1)j!)`,  `e_0 = 0`. ∎

Exactly the document's closed form, obtained by a route it does not use. Both
auxiliary sums verified symbolically for `j = 1..10`, and the two `e_j`
expressions agree exactly for `j = 0..12`
(`0, 0, -1/12, 1/15, -3/112, 1/135, -5/3168, 1/3640, -7/172800, 1/192780,
-1/1702400, 1/16765056, -11/2003097600`). ✔

The resummation to the integral form, the substitution `u = t√c`, and the tail
analysis all check:
`Σ_{j≥0}(j-1)²z^j/j! = e^z(z²-z+1)` so at `z=-x` the inner sum is
`1-e^{-x}(1+x+x²)`; and
`∫₀^∞[1-(1+u²+u⁴)e^{-u²}]/u²du = √π - √π/2 - √π/4 = √π/4` (first term by one
integration by parts). ✔ Computed: `0.44311346272637900682` vs `√π/4 =
0.44311346272637900682`, agreeing to `1.1·10⁻²⁴`.

Landmarks all reproduce: minimiser `c = 2.28378152499` with
`e = -0.0669614288696` (document `2.283781525`, `-0.06696142887` ✔); sign change
`c_× = 4.83904605495` (✔ to all digits); `√π/8 = 0.221556731363` ✔; and
`e(c) = √(πc)/8 - 1/2` reproduces `0.607784 / 1.715567 / 3.931135` at
`C = 25/100/400` — the exact entries of the §5.6 table's last column. ✔

Finite-`n` convergence also reproduces the document's own numbers: for `j=2`,
`-0.0831375` at `n=20` → `-0.0833331` at `n=640`, target `-1/12`. ✔

*Files: `ref_profile.py` / `.log`.*

---

## 6. Teorema E and the honesty of the gap — **the one substantive finding**

### 6.1 What Teorema E actually needs — confirmed

`nΔ_n(c) = nA_n(c) + nB_n(c)`. The `B_n` half is unconditional (Lema 5.1 plus
dominated convergence on a *fixed* `[0,1]` integral, with Lema 6.1 as the
dominating estimate) — confirmed. The `A_n` half is
`Σ_{K=0}^{n} b_K(c)·n(φ_n^{(K)}-φ_K)`, a sum whose **number of terms grows with
`n`** while each term's limit is known. Moving the limit inside genuinely
requires a domination `|n(φ_n^{(K)}-φ_K)| ≤ M_K` with `Σ_K c^K M_K/K! < ∞`.
The document's justification that `b_K(c) ≤ c^K/K!` is correct
(`C(n,K)(c/n)^K(1-c/n)^{n-K} ≤ (n^K/K!)(c/n)^K`). ✔ **So yes, Teorema E really
does need what the document says it needs.**

Note also that this gap applies to the **pointwise** statement `nΔ_n(c) → e(c)`,
not only to the uniform one — see F-3 below.

### 6.2 F-1 — the stated reason for the gap is a non-sequitur

§5.6 makes three assertions that cannot all stand:

1. "**Any geometric growth `D_K(0)=O(λ^K)` suffices** (`Σc^Kλ^K/K! = e^{cλ} <
   ∞`)." — Correct, and note it needs no knowledge of `λ`.
2. "Estágio 8's Proposição 6 **does prove** the improved constants `D'_r(b)` are
   geometric."
3. Teorema E is nevertheless conditional, "because Estágio 8 itself labels the
   **rate** of that geometric bound NUMERICALLY CHARACTERIZED (`≈1.24` at
   `r=45`), with no published closed constant".

If 1 and 2 both hold, 3 does not follow: by criterion 1 the *value* of `λ` is
irrelevant, so Teorema E would be **unconditional**. The document's own
sufficiency criterion defeats its own stated obstruction.

Having read the cited source, the resolution is that **assertion 2 overstates
Estágio 8**:

* `error_constant_growth_attempt/ATTEMPT.md` §6.1's boxed Proposition 6 states
  the improved recursion "yields constants that still satisfy the Target
  Theorem's conclusions, and that are geometric rather than factorial in `r`" —
  but §6.1 supplies **no proof of the geometricity**, only the mechanism (the
  discarded `1/n` restored via `r/(b+r+1) < 1`) and a numerical table, followed
  by "The improved bound's ratio is `1.240` at `r=45` and slowly decreasing".
* That same document's own §6.3 status table lists `D'_r(b), C'_r(b)` as
  "**PROVED bound; rate NUMERICALLY CHARACTERIZED**" — i.e. the *bound* is
  rigorous, the *geometricity* is not separately certified.
* The geometricity of the inputs `A_r(b), B_r(b)` that would drive it is itself
  listed as "**NUMERICALLY CHARACTERIZED**, mechanism proved (Lemma 7)".
* `THEOREM.md`'s Estágio 8 open list keeps "a taxa exata do limitante melhorado
  `D'_r(b)` … convergência para `9/8` plausível não provada".

So: **the PROVED-MODULO label on Teorema E is correct** and should stay. But the
gap that is actually open is *a written-down proof of **qualitative** geometric
growth of `M_K`*, not "an explicit-constant geometric bound". Scorecard row 12
and §8 item 2 both name the wrong gap (they say "explicit-constant"), and §5.6's
sentence "Estágio 8's Proposição 6 does prove … are geometric" should be
softened to match Estágio 8's own status table.

*Direction of the error:* this makes the document's obstruction sound
**better-founded than it is**, while simultaneously making the result sound
**weaker than it might be**. It is not an overclaim of a result. But it is a
misstatement about a predecessor document's proof status, which in this archive
matters.

*Constructive note:* qualitative geometricity looks close at hand from Estágio
8's **proved** ingredients. Lemma 7 (PROVED, exact) gives the closed form
`F_r(2,0) = (φ_r/4^r)Σ_{i=0}^{r}2^{r-i}C(2r+1,i)`, and the crude bound
`Σ_{i≤r}C(2r+1,i) ≤ 2^{2r+1}` already yields `F_r(2,0) ≤ 2φ_r·2^r = O(2^r)` —
geometric, with an explicit (if far from sharp) constant. Unrolling Proposição
6's recursion, `C'_r(b) ≤ (B_r(b)+A_r(b+1)) + 2C'_{r-1}(b+1)` (the two
multipliers `r/(b+r+1)` and `r/(r+b+2)` each being `< 1`), which propagates
geometricity with an extra factor `2`. I have **not** carried this out and do
not claim it; I record it because if it goes through, Teorema E becomes
unconditional and the document's §5.6 is simply too pessimistic.

### 6.3 F-12 (nit) — the `K = n` term

The reduction `M_K ≤ 5K/4 + D_K(0)` is stated "on the theorem's own hypothesis
`n ≥ K+1`", which excludes `K = n` — a term that is present in the sum
`Σ_{K=0}^{n}`. It is harmless: `b_n(c)·n|φ_n^{(n)}-φ_n| ≤ (c/n)^n·n → 0`
super-exponentially. Worth one clause.

### 6.4 Hypothesis (U') is correctly identified — **citation accurate**

The document says (U') "is exactly 'Estágio 7's `1/n` rate, uniform in `K`'" and
that "the archive is explicit (Estágio 7, *Cautelas de redação*) that no
uniformity in `K` is proved or claimed there". `THEOREM.md` Estágio 7 reads,
verbatim:

> "manter sempre 'para todo `K` **fixo**, `K≥2`' na afirmação `Θ(1/n)` —
> **nenhuma uniformidade em `K` é provada ou alegada**."

**Citation accurate, word for word.** ✔ (U') is correctly labelled NUMERICALLY
CHARACTERIZED / OPEN, and the identification of it as the single obstruction to
an explicit rate is correct.

I also confirmed that `THEOREM.md` Estágio 7's open list still carries item (iv),
"versão localmente-uniforme-em-`c` do Teorema 3", so the target of this front is
correctly identified as genuinely open.

### 6.5 S-1 — a strengthening the document leaves on the table

§6.3 explains the sharp constant `a* = √π(1/√2 - 1/2)` via "at `n=K+1` all but
one point is rerouted, so `f` is a uniform random mapping in all but one
coordinate, and the Ramanujan-`Q` value of Prop. 7.1 applies **up to an `O(1/n)`
relative correction**".

The correction is unnecessary — the identity is **exact**:

> **Observation.** `φ_n^{(n-1)} = φ_n^{(n)} = Q(n)/n` for every `n ≥ 1`.
>
> *Proof.* With `K = n-1` reroutes, the single un-rerouted point `x` has
> `f(x) = π(x)`, and only that one value of `π` is ever consulted. For a uniform
> random permutation the **marginal** law of `π(x)` is `Uniform[n]`, independent
> of the `U_i`. So `f` is exactly a uniform random mapping, and Prop. 7.1
> applies verbatim. ∎

Verified exactly (`Fraction`) for `n = 2,…,10`: `3/4, 17/27, 71/128, 1569/3125,
899/1944, 355081/823543, 425331/1048576, 16541017/43046721, 5719087/15625000` —
identical in all three columns. (This also retro-explains why the document's own
§2.3 lists `φ_7^{(6)} = 355081/823543`, the same rational as `φ(7,7)`.)

This makes the `a*` mechanism exact at the endpoint rather than heuristic. It
does **not** prove (U'), which additionally needs that the max over `n` is
attained at `n = K+1` — still numerical.

---

## 7. §7 — the `c = γn` regime

### 7.1 Proposição 7.1 — **SOUND**

At `c = n`, Definition 1's convention gives `q = 1`, so every point is rerouted
and `f(i) = U_i` with `U` i.i.d. `Uniform[n]` — a uniform random mapping. The
orbit of `1` returns at step `j` iff `f(1),…,f^{j-1}(1)` are `j-1` distinct
points other than `1` and `f^j(1) = 1`, of probability
`[Π_{i=1}^{j-1}(n-i)/n]·(1/n)`. The return time is unique so the events are
disjoint; summing over `j ≥ 1` gives `(1/n)Σ_{m≥0}Π_{i=1}^{m}(1-i/n) = Q(n)/n`. ✔
Verified exactly for `n = 1..11` (11/11).

Numerically `√n φ(n,n) = 1.220996, 1.236905, 1.245046, 1.249164` at
`n = 100,400,1600,6400` — **identical to the document's figures**, and matching
`√(π/2) - 1/(3√n)` to six digits. ✔ `a* = 0.3670872119` confirmed.

The `Q(n) = √(πn/2) - 1/3 + O(n^{-1/2})` asymptotic is properly labelled
**CITED** (Knuth TAOCP I §1.2.11.3; Flajolet–Odlyzko), not proved here. Correct
practice.

### 7.2 The heuristic — coherent, and honestly labelled

I re-derived it. With `q = γ` fixed and `j` on scale `√n` (so `R ≈ γj`,
`n-j+R ≈ n`), the §4.1 hazards read `return ≈ 1/n` and
`fatal ≈ γj/n + (1-γ)γj/n = γ(2-γ)j/n`, giving

`φ(n,γn) ≈ (1/n)∫₀^∞e^{-γ(2-γ)J²/(2n)}dJ = n^{-1/2}√(π/(2γ(2-γ)))`,

against `φ_∞(γn) ≈ n^{-1/2}√(π/(4γ))`, ratio `√(2/(2-γ))`. ✔ Both endpoints
reduce correctly (`γ→0` → 1; `γ=1` → `√2` and `√(π/2)n^{-1/2}`, reproducing the
proved Prop 7.1). The `c_eff = c(1-c/2n)` restatement is equivalent
(`φ_∞(c_eff)/φ_∞(c) ≈ (1-γ/2)^{-1/2}`), and the small-`γ` expansion
`1 + γ/4` matches §5's `e(c)/φ_∞(c) ≈ c/4` independently. **Two routes, same
`c/(4n)`** — confirmed.

**What is missing is exactly what the document says is missing:** concentration
of `R` around `γj`, and a uniform Riemann-sum control of `(1/n)Σ_J Π(·)`. The
status line "**NUMERICALLY CHARACTERIZED** with a derived mechanism … not
carried out here, and **not claimed**" is accurate. **HONEST.**

### 7.3 The tables — reproduced to every printed digit

My own float64 engine at `n = 4000`:

| `γ` | `√n φ(n,γn)` | doc | ratio `φ/φ_∞` | doc |
|---|---|---|---|---|
| 0.05 | 4.006055 | 4.006055 | 1.010781 | 1.010781 |
| 0.10 | 2.867677 | 2.867677 | 1.023258 | 1.023258 |
| 0.25 | 1.887647 | 1.887647 | 1.064991 | 1.064991 |
| 0.50 | 1.440789 | 1.440789 | 1.149583 | 1.149583 |
| 0.75 | 1.288754 | 1.288754 | 1.259377 | 1.259377 |
| 1.00 | 1.248070 | 1.248070 | 1.408296 | 1.408296 |

§7.3's global-sup table likewise: `0.030239, 0.021909, 0.015759, 0.011278,
0.008043, 0.005721` at `n = 125..4000`, argmax `c*/n = 1.000` throughout,
`√n·sup = 0.338088 … 0.361843`. **Every entry reproduces exactly.** ✔

I also confirmed the §7.3 claim about the sup over *all* `c ≥ 0`: since
`φ(n,·)` is constant on `[n,∞)` and `φ_∞ ↓ 0`, that sup is `φ(n,n) = Q(n)/n`,
numerically `√n·φ(n,n) = 1.238613, 1.245912, 1.248070` at `n = 500,2000,4000`
→ `√(π/2)`. So the **global** sup is `≈1.2533/√n`, about `3.4×` larger than the
sup over `[0,n]` (`a*/√n`). Both → 0, so Teorema C is untouched — and the
document says precisely this. ✔

### 7.4 Raw-model Monte Carlo

`2·10⁵` mappings per cell, simulating `π`, `ξ`, `U` directly and following the
orbit of `1`:

| `n` | `c` | MC | ±2 s.e. | exact chain |
|---|---|---|---|---|
| 6 | 2 | 0.608220 | 0.002183 | 0.607563 |
| 10 | 3 | 0.512280 | 0.002235 | 0.510313 |
| 12 | 12 | 0.336490 | 0.002113 | 0.336339 |
| 20 | 5 | 0.399705 | 0.002191 | 0.401613 |
| 30 | 30 | 0.218200 | 0.001847 | 0.218315 |

All within 3 s.e. ✔

*Files: `ref_scaling.py` / `.log`.*

---

## 8. Honesty audit of the Scorecard (§9) and Verdict (§10)

### 8.1 The main question: is a rate ever attached to Teorema A or C? **No.**

I checked every occurrence of "rate" and "`Θ(n^…)`" in the document. Teorema A
and Teorema C are consistently presented as *qualitative*:

* §3.3: "Answer to Question 1, **qualitative part**: YES … The quantitative part
  … is §§5–6."
* §3.3: "Note what is *not* needed: no `F_r/G_r/H_r`, no error constants, **no
  rate**, no monotonicity."
* §8 item 1: "**An explicit rate for Teorema A.** Available only modulo (U')."
* §10 bullet 1: "**No explicit rate is proved.** Teorema A gives uniformity with
  no bound in `n`."
* Scorecard rows 5 and 7: "PROVED, unconditional", with no rate mentioned.

**On this specific point the document is scrupulous, including in the Executive
Summary** (points 1 and 2 claim uniformity only; point 4 presents the explicit
bound as conditional on (U')).

### 8.2 F-2 — Executive summary point 5 drops a qualifier (real, minor)

> Line 55: "In **absolute** terms nothing breaks — even the global sup tends to
> `0`, **at rate `Θ(n^{-1/2})`**."

No qualifier. Compare:

* §7's own summary (line 709): "the convergence is uniform on `[0,∞)` (Teorema
  C), at rate `Θ(n^{-1/2})` **(numerically characterized)**".
* Scorecard row 20: "`sup_{c≥0}|Δ_n| = φ(n,n) = Θ(n^{-1/2})` — **NUMERICALLY
  CHARACTERIZED** … the `→0` part is item 7 (PROVED)".

And the qualifier is needed. The `Ω(n^{-1/2})` half *is* essentially proved
(`sup_{c≥0}|Δ_n| ≥ φ(n,n) = Q(n)/n`, Prop 7.1 plus the cited `Q` asymptotics).
The `O(n^{-1/2})` half is **not**: it needs `sup_{[0,n]}|Δ_n| = O(n^{-1/2})`,
which follows from Teorema B at `C = n` — i.e. **only under (U')**, which is
unproved. So `Θ` is not available unconditionally, and the Executive Summary
states it as if it were. **This is the flagged pattern: a qualifier present in
§7 and in the Scorecard, absent in the summary prose.** Fix: add "(numerically
characterized)" to line 55.

### 8.3 F-3 — Executive summary point 3 mislocates the Teorema E gap (real, minor)

> Lines 31–39: "`n[φ(n,c)-φ_∞(c)] → e(c)` with … The **coefficient-wise**
> version … is **PROVED** unconditionally (§5.4); the **uniform** version needs
> one named interchange-of-limits step (§5.6) and is **PROVED-MODULO** that."

This presents the dichotomy as *coefficient-wise = proved / uniform = modulo*,
implying the **pointwise** statement `nΔ_n(c) → e(c)` is proved. It is not.
Teorema E (§5.6) reads, in full: "For every `c ≥ 0`, `nΔ_n(c) → e(c)`, **and**
`n sup_{[0,C]}|Δ_n| → sup_{[0,C]}|e|`" — and the whole of Teorema E carries the
`PROVED-MODULO` label. §5.6's own discussion confirms it: "The `A_n` half needs
to move the limit inside the `K`-sum", which is required for the *pointwise*
statement. And it genuinely cannot be avoided: the `K`-sum has a growing number
of terms, and coefficient-wise convergence (Teorema D) does not imply pointwise
convergence of `nΔ_n` without a domination.

Meanwhile the bullet's **opening sentence** asserts `n[φ(n,c)-φ_∞(c)] → e(c)`
flatly. So the summary asserts a conditional statement unconditionally, then
qualifies only a *different* statement. Fix: "everything except the
coefficient-wise version needs one named interchange-of-limits step".
Scorecard row 12 is correct as written and should be the governing text.

### 8.4 F-4 — "the error constant grows exactly like `√C`" (minor)

Executive summary point 3 and §5.6's bold "Consequence" both say "**The
uniform-on-`[0,C]` error constant grows exactly like `√C`**". As a statement
about `sup_{[0,C]}|e|` this is PROVED (given Prop 5.2). But calling it "*the*
uniform-on-`[0,C]` **error constant**" presupposes
`lim n·sup_{[0,C]}|Δ_n| = sup_{[0,C]}|e|` — which is Teorema E, conditional.
Scorecard row 13 gets this exactly right ("PROVED given item 11 (a statement
about `e` alone); its identification *as* the limiting error constant inherits
item 12's status"). The summary and §5.6 drop that distinction. Same pattern as
F-2/F-3, same fix: one clause.

### 8.5 Nits

* **F-6.** "§9.3" is cited twice (lines 68 and 142) for the scope note about
  Definition 1's `q = min(c/n,1)` convention. §9 is the Scorecard, a table with
  no subsections; the scope note is in **§8** under "Prior-document review".
  Broken cross-reference, twice.
* **F-7.** §2.3's validation table row "mixture identity (7.1), `n=2..7`, 4
  values of `c` each | exact, **28/28**". `n = 2..7` is 6 values; `6 × 4 = 24`,
  not 28. (My own run: 24/24 exact.) Either the row should read `n=2..8`, or the
  count should read 24/24. Every other count in that table is internally
  consistent (12/12, 7/7, 5/5, 11/11, 7/7).
* **F-5, F-8, F-9, F-10, F-11, F-12, F-13** as recorded in §§1.3, 1.4, 3.9,
  3.10, 4.2, 4.3, 6.3 above.

### 8.6 What the honesty audit did **not** find

* No case of a conditional result being restated as unconditional in §8 or §10.
  §10's three bullets ("No explicit rate is proved"; "Teorema E carries one named
  interchange-of-limits gap"; "The `γ∈(0,1)` scaling law is not proved") are
  accurate and, if anything, understate the document's positive results.
* No case of Teorema A or Teorema C being credited with a rate.
* No misquotation of any predecessor document. I checked verbatim: Definition
  1's convention (`THEOREM.md` line 111), §7.1's "a natural strengthening, not
  attempted here and flagged as its own gap" (line 851), Corolário 4.3's
  `a_1(n) = 1/3 - 1/(3n²)` (line 1081), Estágio 7's `c_K` and its *Cautelas de
  redação*, and Estágio 8's Proposição 6. All accurate **except** the
  characterisation of Proposição 6's proof status (F-1).
* The `e_0 = e_1 = 0` cross-check against `THEOREM.md` Corolário 4.3 is correct:
  `a_1(n) := -∂_cφ|_0 = 1/3 - 1/(3n²)`, so
  `n([c^1]φ(n,·) - [c^1]φ_∞) = n·(1/(3n²)) = 1/(3n) → 0 = e_1`. ✔
* §8's "Prior-document review … No error, gap, or overclaim was found in any
  catalogued document" is consistent with my own findings; I found none either.
* The scope note in §8 about the `q = min(c/n,1)` convention being *material*
  for Teorema C (as opposed to "immaterial in the limit" for Teorema 3) is
  **correct and well taken** — it is exactly what makes `φ(n,·)` constant on
  `[n,∞)` and hence what makes the global sup finite and equal to `φ(n,n)`.

---

## 9. Scorecard (this referee's, mirroring the target's §9)

| # | Target claim | Target status | **Referee verdict** |
|---|---|---|---|
| 1 | `(j,R)` chain computes `φ(n,c)`, `φ_n^{(K)}` | PROVED + NUM VERIFIED | **CONFIRMED** — my own raw-model enumeration matches exactly, 18/18, plus 5 archive families |
| 2 | **Lema 3.1** equi-Lipschitz, constant 1, uniform in `n` | PROVED | **SOUND** — coupling rebuilt, marginals/event/union bound all correct; 624 exact pairs, 0 violations. Wording nit F-5 |
| 3 | **Lema 3.2** derivative identity | PROVED | **SOUND** (re-derived; `dP(Bin=K)/dp = n[…]` standard) |
| 4 | Sharp Lipschitz constant `1/3-1/(3n²)` | NUM VERIFIED | **CONFIRMED as numerical**; correctly not used |
| 5 | **Teorema A** locally uniform | PROVED, unconditional | **SOUND, unconditional.** Grid inequality audited; `1/3` sub-bound confirmed; `4/3` correct (a factor-2-loose but valid `4C/(3M)`) |
| 6 | **Lema 4.1** + **Corolário 4.2** | PROVED | **SOUND.** All six steps audited separately; 1875 states for (a)/(b), 2800 cells for the lemma, 0 violations. Decomposition legitimate — "first return" worry is vacuous, the process cannot return twice. Nits F-10, F-11 |
| 7 | **Teorema C** globally uniform | PROVED, unconditional | **SOUND, unconditional**, under the correctly-named convention |
| 8 | **Lema 5.1** `B_n ≤ 0`, exact integral | PROVED | **SOUND** (both pgf interchanges legitimate; agreement `1.3·10⁻⁴⁰`) |
| 9 | **Teorema D** coefficient-wise | PROVED, unconditional | **SOUND, and airtight.** Exactness confirmed against a symbolic chain that never uses the binomial identity, `n=2..12`, 91/91 coefficients. No interchange occurs. Minor: cites `O_K(n^{-2})` where `o(1/n)` suffices |
| 10 | `e_j = [c^j]e(c)`, `j=0..8` | PROVED for those `j` | **CONFIRMED exactly, `j=0..12`** |
| 11 | **Prop 5.2** closed forms + large-`c` | PROVED | **SOUND** — re-derived independently from Teorema D's sum, including the `1-j(2j-1) = -(2j+1)(j-1)` cancellation; all landmarks reproduce |
| 12 | **Teorema E** | PROVED-MODULO-[explicit-constant geometric bound] | **LABEL CORRECT, REASON WRONG (F-1).** The gap is real; but it is *qualitative* geometricity of `M_K`, not an explicit constant, and §5.6 overstates Estágio 8's Prop 6 as proving geometricity |
| 13 | `sup_{[0,C]}|e| ~ √(πC)/8` | PROVED given 11 | **CONFIRMED**; row 13's own caveat about inheriting row 12's status is correct — but is dropped in the summary (F-4) |
| 14 | **Lema 6.1**, `κ_B` | PROVED | **SOUND.** Both branches correct; `κ_B = 0.280480169024586` reproduced. `n≥4` is a proof artefact (F-13); "computed exactly" is loose (F-9) |
| 15 | **Teorema B** given (U'ₐ) | PROVED given (U'ₐ) | **SOUND** (Jensen direction correct) |
| 16 | **(U')**, sharp `a*` | NUM CHARACTERIZED / OPEN | **CONFIRMED as open.** Citation of Estágio 7's *Cautelas de redação* is verbatim accurate. Endpoint mechanism is exactly right and in fact **exact**, not `O(1/n)` (S-1) |
| 17 | `K ↦ φ_n^{(K)}` non-increasing | NUM VERIFIED, not used | **CONFIRMED not used anywhere** |
| 18 | **Prop 7.1** `φ(n,n)=Q(n)/n` | PROVED (+ CITED `Q`) | **SOUND**, 11/11 exact; `Q` asymptotics properly labelled CITED |
| 19 | **(7.1)** `γ`-scaling | NUM CHARACTERIZED | **HONESTLY LABELLED.** Heuristic re-derived and internally coherent; the two named missing ingredients are exactly the ones missing |
| 20 | global sup at `c=n`, `√n sup → a*` | NUM CHARACTERIZED | **CONFIRMED as numerical**; but the summary drops the qualifier (F-2) |
| 21 | Independent adversarial review | NOT PERFORMED | **NOW PERFORMED — this report** |

---

## 10. Findings, in priority order

| id | severity | finding |
|---|---|---|
| **F-1** | **substantive (presentational/logical)** | §5.6 asserts "any geometric growth suffices" *and* "Estágio 8's Prop 6 does prove `D'_r(b)` geometric" *and* that Teorema E is nevertheless conditional for lack of an explicit constant. The first two contradict the third. Estágio 8's own §6.3 table says "PROVED bound; **rate** NUMERICALLY CHARACTERIZED" and gives no proof of geometricity, so the correct statement is that **qualitative** geometricity of `M_K` is what is missing. Teorema E's PROVED-MODULO label stands; the named gap must be renamed (§5.6, Scorecard row 12, §8 item 2, §10 bullet 2) |
| **F-2** | minor overclaim | Exec summary line 55: "the global sup tends to `0`, at rate `Θ(n^{-1/2})`" — qualifier "(numerically characterized)", present in §7 and Scorecard row 20, is dropped. The `O` half needs (U'), unproved |
| **F-3** | minor overclaim | Exec summary point 3 attributes the interchange gap to "the **uniform** version" only. The **pointwise** `nΔ_n(c) → e(c)` is equally inside Teorema E and equally conditional. Only the coefficient-wise Teorema D escapes |
| **F-4** | minor | "the uniform-on-`[0,C]` error constant grows exactly like `√C`" stated without Teorema E's caveat in the exec summary and in §5.6's bold "Consequence". Scorecard row 13 has it right |
| F-5 | nit | Scorecard row 2 / §10 say "monotone coupling"; §3.1(ii) says "not pointwise-monotone". Defensible (the *marks* are monotonically coupled) but reads as a contradiction |
| F-6 | nit | "§9.3" cited twice (lines 68, 142); the scope note is in **§8** |
| F-7 | nit | §2.3 mixture row says "28/28" for `n=2..7` × 4 values; that is 24 cells (I get 24/24 exact) |
| F-8 | nit | §3.1(ii)'s counterexample shows the cyclic **count** is non-monotone, not the event `{1 cyclic}`. Sharper counterexample supplied in §1.3 above |
| F-9 | nit | `κ_B` "computed exactly here" — it is a high-precision numerical value of a transcendental sup |
| F-10 | nit | §4.1's "`C_0`-tail values" are the `J`-optimised Lema 4.1 bound (I reproduced all five); the sentence could be read as `ω(C_0)` or as the true sup, both of which differ by 1.5–4× |
| F-11 | nit | Exec summary point 2's "uniformly in `n`" should be "uniformly in `n ≥ C_0`"; Cor 4.2 and Teorema C themselves are correct |
| F-12 | nit | Teorema E's domination `M_K ≤ 5K/4 + D_K(0)` requires `n ≥ K+1`, excluding the `K=n` term of the sum. Negligible (`≤ n(c/n)^n`) but should be dispatched in one clause |
| F-13 | nit | Lema 6.1's `n ≥ 4` is a proof artefact (from `1-u ≥ 1/2`); `n=2,3` also hold numerically |
| **S-1** | strengthening | §6.3's `φ_{K+1}^{(K)} ≈ Q(K+1)/(K+1)` "up to an `O(1/n)` relative correction" is in fact **exact**: `φ_n^{(n-1)} = φ_n^{(n)} = Q(n)/n`, because the single un-rerouted point's `π(x)` is marginally `Uniform[n]`. Verified exactly `n=2..10` |

**None of F-1 … F-13 touches Lema 3.1, Teorema A, Lema 4.1, Corolário 4.2 or
Teorema C.** F-1 is a mis-description of a gap, not a defect in a proof; F-2,
F-3, F-4 are summary-prose fixes of one clause each; the rest are nits.

---

## 11. Final verdicts

* **Lema 3.1 (equi-Lipschitz): SOUND.** The coupling is correct, the marginals
  are right, the shared `π` and shared `U` are both genuinely needed, the union
  bound is uniform in `n`, and the reduction to `c' ≤ n` is valid.
* **Teorema A (locally uniform, unconditional): SOUND.** The `1/3` sub-bound,
  the `4/3` constant, the grid inequality and the `ε`-argument are all correct.
  No rate is proved and none is claimed.
* **Lema 4.1 + Corolário 4.2: SOUND.** Every one of the six steps holds
  separately; the first-return decomposition is legitimate (the process cannot
  return twice, so "return at `j`" *is* "first return at `j`"); the tower-property
  product is legitimate precisely because the conditional lower bound `qj/n` is
  deterministic. 2800-cell exhaustive sweep, 0 violations.
* **Teorema C (globally uniform, unconditional): SOUND**, under Definition 1's
  own convention, which the document names explicitly and correctly.
* **Lema 5.1, Lema 6.1, Corolário 6.2, Teorema B, Teorema D, Proposição 5.2,
  Proposição 7.1: SOUND**, each re-derived from scratch.
* **Teorema E: correctly labelled conditional; the gap is real — but the
  document names the wrong gap (F-1).** Requires a targeted rewrite of §5.6,
  Scorecard row 12, §8 item 2 and §10 bullet 2.
* **§7's `γ∈(0,1)` scaling law: honestly labelled.** The mechanism is coherent
  and reproduces both endpoints and §5's independent `c/(4n)`; the two missing
  ingredients are named accurately and not glossed.
* **Honesty audit: substantially clean, with three summary-prose fixes
  (F-2, F-3, F-4).** Teorema A and Teorema C are never anywhere credited with an
  explicit rate — the specific failure mode the brief asked about does not
  occur.

**Recommendation: ACCEPT for catalogue, conditional on the F-1 rewrite and the
three one-clause fixes F-2/F-3/F-4.** The two headline unconditional theorems
(Teorema A, Teorema C) and the unconditional coefficient-wise Teorema D, plus
the closed forms of `e(c)`, stand as proved and should be catalogued as such.
This is a strong document; I attacked the load-bearing arguments from several
directions and could not break any of them.

---

## 12. Files in this directory

| file | what it does |
|---|---|
| `ref_engine.py` / `.log` | independent raw-model enumerator + `(j,R)` chain + conditional-`K` chain; validation against the raw model and 5 archive families |
| `ref_lipschitz.py` / `.log` | Lema 3.1 coupling audit, 624-pair exact stress test, both non-monotonicity counterexamples, `φ_∞` Lipschitz sub-bound, Teorema A grid inequality |
| `ref_tail.py` / `.log` | exact forward pass; decomposition audit; cellwise (a)/(b); all six Lema 4.1 steps; 2800-cell adversarial sweep; Corolário 4.2 algebra + numerical audit |
| `ref_lemmas.py` / `.log` | §4.1 `C_0`-tail reproduction; Lema 5.1; Lema 6.1 both branches + scan; `κ_B`; Corolário 6.2; Teorema B's Jensen step |
| `ref_profile.py` / `.log` | binomial identity; Teorema D vs symbolic chain (`n=2..12`); `c_K` citation check; independent re-derivation of Prop 5.2's `e_j`; three representations of `e(c)`; landmarks |
| `ref_scaling.py` / `.log` | float64 precision audit; Prop 7.1; §7.2 and §7.3 tables recomputed; heuristic re-derivation; raw-model Monte Carlo (the one use of randomness) |
| `ref_astar_note.log` | the S-1 observation `φ_n^{(n-1)} = φ_n^{(n)} = Q(n)/n`, exact `n=2..10` |

Reproduce with `python3 ref_engine.py`, then `ref_lipschitz.py`, `ref_tail.py`,
`ref_lemmas.py`, `ref_profile.py`, `ref_scaling.py` (the last is the only one
using randomness; its seed entropy is recorded at the top of this report and in
its own log).
