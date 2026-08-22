# Derivation: cycle survival under Poisson perturbation of random permutations

Self-contained restatement of the mathematical content of this package.
Source of record for the proofs is the archive's internal theorem
document (see `README.md` for the pointer); this file reproduces the
argument in full so the package does not depend on the archive to be
read. Status labels (PROVED / CONJECTURED / CITED / OPEN) are preserved
exactly as in the source — nothing here is upgraded or softened.

## Contents

1. The model
2. The limit object
3. Theorem 1 (closed form) and proof
4. Corollaries: series, tail asymptotic
5. The conditional-K law and the Hansen–Jaworski connection
6. The n→∞ bridge: what is proved, what is open
7. Conjectures, stated separately from proofs

---

## 1. The model

Fix `n ∈ ℕ` and `c ≥ 0`. Let `π` be a uniformly random permutation of
`[n] = {1,…,n}`. Independently, for each `i ∈ [n]` let `ξ_i` be i.i.d.
Bernoulli with `P(ξ_i=1) = c/n`, and let `U_i` be i.i.d. uniform on `[n]`,
independent of `π` and of the `ξ`'s. Define the random mapping

```
f(i) = U_i   if ξ_i = 1  ("i is rerouted")
f(i) = π(i)  if ξ_i = 0
```

A point `i` is **cyclic** for `f` iff `f^t(i) = i` for some `t ≥ 1`,
equivalently iff `i` lies on a directed cycle of the functional digraph
`i → f(i)`. The observable is

```
φ(n,c) := E[ #{i : i cyclic for f} ] / n = P(1 is cyclic for f)
```

(the second equality by exchangeability of the construction in `i`).
`c` is the expected number of rerouted points; `c=0` recovers a plain
uniform permutation (`φ(n,0)≡1`, every point of a bijection is cyclic).

**Terminology note.** No name for this ensemble appears in the random-
mapping literature under this exact construction — the literature's
"random mappings with exchangeable in-degrees" family (Jaworski 1984
through Hansen–Jaworski 2014, §5 below) is parametrized by in-degree
sequence, not by a background permutation independently corrupted by
per-point rerouting. See `README.md` for the exact scope of that claim.

---

## 2. The limit object `L(c)`

The `n → ∞` scaling limit of the cycle structure of a uniform random
permutation is the standard Poisson–Dirichlet object: normalized cycle
lengths converge to `PD(1)` (Kingman 1975), with the size-biased
("stick-breaking") representation `GEM(1)` (McCloskey 1965;
Patil–Taillie 1977; see Pitman, *Combinatorial Stochastic Processes*,
St-Flour 2002, Springer LNM 1875, Ch. 3). `L(c)` is this object equipped
with an independent Poisson process of rate `c` on `[0,1]` ("marks"),
each mark carrying an independent uniform destination: an unmarked point
moves to the next point on its cycle; a marked point moves instead to
its destination.

This can be built explicitly from elementary primitives (independent
`Exp(1)` "closure clocks" per arc-head, raced against the Poisson mark
process) without importing exchangeable-partition machinery beyond one
citation (that the resulting exploration process is the standard `PD(1)`
representation under lazy revelation — Kingman 1975; Arratia–Barbour–
Tavaré, *Logarithmic Combinatorial Structures*, EMS 2003, Chs. 4–5, "the
Feller coupling"). Every computation below is self-contained given that
one citation.

`φ_∞(c) := P(x_0 \text{ cyclic in } L(c))` for a uniform reference point
`x_0`; by Fubini and exchangeability of the construction in `x_0`, this
equals `E[\text{Lebesgue measure of the cyclic set}]` — the natural
`n→∞` analogue of `φ(n,c)`.

---

## 3. Theorem 1 (PROVED) and proof

> **Theorem 1.** For every `c ≥ 0`,
> `φ_∞(c) = ∫₀¹ e^{-c t²} dt = (1/2)√(π/c) · erf(√c)` (value `1` at
> `c=0` by continuity / direct check).

### Proof sketch (exploration process)

Reveal the forward orbit of `x_0` step by step. Let `t ∈ [0,1)` be the
traversed (visited) fraction of mass so far. The orbit decomposes into
**arcs** — maximal runs traversed without a mark — separated by marks
that survive (do not land on already-visited territory). At traversal
level `t`, with `m` currently-open "arc-heads" (including `x_0`'s own):

- **π-closure hazard**: the walk closes onto a specific arc-head at rate
  `1/(1−t)` per unit traversed mass (this is exactly the classical fact
  that the size-biased cycle length of a uniform permutation is uniform
  on `(0,1)` — the `m=1`, `c=0` case reduces to this).
- **Mark hazard**: rate `c dt`; a mark at position `s` "kills" (lands on
  already-visited territory, terminal, non-cyclic) with probability `s`,
  or survives (opens a new arc-head) with probability `1−s`.

`x_0` is cyclic iff the *first* terminal event is a π-closure back onto
`x_0` itself, not onto some other, later-born arc-head, and not a mark
kill. Writing `T_0 ~ Unif(0,1)` for `x_0`'s own closure clock (an
elementary fact, proved by direct computation on `Exp(1)` primitives)
and conditioning on `T_0 = t`:

`P(x_0 \text{ cyclic} \mid T_0=t) = P(\text{no mark before } t \text{ kills, and no surviving mark before } t \text{ produces a sibling arc-head that closes before } t)`.

**The key computation.** For a single mark at position `s < t`, compute
the joint probability (over its independent survival-Bernoulli and its
independent closure-clock) that it neither kills nor produces a sibling
closing before `t`:

```
P(survives) · P(sibling closes after t | survives) = (1−s) · (1−t)/(1−s) = 1−t
```

— **independent of `s`.** This exact cancellation (the survival
probability `1−s` cancels against the competing-clock tail
`(1−t)/(1−s)`) is the entire reason a closed form exists. By the
Poisson marking/thinning theorem, the number of "failing" marks in
`[0,t)` is then `Poisson(c·t·t) = Poisson(c t²)` (rate `c` on an
interval of length `t`, each mark failing with probability `t`,
independent of position), so

```
P(x_0 cyclic | T_0=t) = P(Poisson(c t²) = 0) = e^{-c t²}.
```

Integrating over `T_0 ~ Unif(0,1)`:

```
φ_∞(c) = ∫₀¹ e^{-c t²} dt.
```

The closed form follows by the substitution `u = √c · t`:
`∫₀¹ e^{-ct²}dt = (1/√c)∫₀^{√c} e^{-u²}du = (1/√c)·(√π/2)·erf(√c)`. ∎

### A specific numerical pitfall this proof avoids

A *heuristic* tail computation that forgets to size-bias "the arc
currently being traversed" lands on `√(π/2)·c^{-1/2}` instead of the
correct `(√π/2)·c^{-1/2}` — off by a factor `√2` (an
inspection/waiting-time-paradox error: the arc containing a uniformly
chosen reference time has mean `2/c`, not the unconditional `1/c`). The
proof above never forms this quantity: Step 4's per-mark probability is
computed jointly over the pair (survival Bernoulli, closure-clock
exponential), not as an averaged arc length, so there is no
size-biased object anywhere in the chain to get wrong. `simulations/asymptotics.py`
verifies the *correct* coefficient `√π/2 ≈ 0.8862269255` numerically.

---

## 4. Corollaries (PROVED)

**Corollary 4.1 (series).** `φ_∞(c) = Σ_{k≥0} (-c)^k / (k!(2k+1))` for
every real `c`; entire function (infinite radius of convergence — proved
by the Weierstrass M-test justifying term-by-term integration of the
Taylor series of `e^{-ct²}` on `[0,1]`). First terms:
`1 − c/3 + c²/10 − c³/42 + c⁴/216 − …`. In particular `a_1 = 1/3`
(coefficient of `−c`) — see `README.md` for why this single number
already discriminates against a specific refuted candidate closed form.

**Corollary 4.2 (tail, with a rigorous error bound).** As `c → ∞`,

```
φ_∞(c) = (√π/2)·c^{-1/2} − R(c),    0 < R(c) < e^{-c}/(2c) for all c > 0.
```

So `φ_∞(c) = (√π/2)c^{-1/2}(1 + O(e^{-c}))` — a *pure* power-law tail up
to exponentially small corrections, not the polynomial corrections
typical of more general asymptotic expansions. Proved by one integration
by parts on the erf tail integral (`README.md`/`simulations/asymptotics.py`
verify the bound numerically, including the regime where `R(c)` itself
underflows double precision).

**Sanity check.** `φ_∞(0) = ∫₀¹ 1 dt = 1`: with no reroutes, every point
of a permutation is cyclic.

---

## 5. The conditional-K law and the Hansen–Jaworski connection

Condition on exactly `K` marks (rather than `Poisson(c)` many).

> **Lemma 2 (mean, PROVED for every `K`).**
> `φ_K = ∫₀¹ (1−t²)^K dt = 4^K (K!)² / (2K+1)!` (a Wallis integral).
>
> Checks: `φ_0=1`, `φ_1=2/3`, `φ_2=8/15`, `φ_3=16/35`, … Mixing over
> `K ~ Poisson(c)` exactly reproduces Theorem 1:
> `Σ_K e^{-c} c^K/K! · φ_K = ∫₀¹ e^{-c} e^{c(1-t²)} dt = ∫₀¹ e^{-ct²}dt`.

> **Lemma 2 (density at `K=1`, PROVED).** The cyclic-mass random variable
> `M_1 := Leb(cyclic set)` has density `f_{M_1}(x) = 2x` on `(0,1)`.
> Proved by a direct whole-space computation (splitting on whether the
> single reroute's destination lands inside or outside the struck
> background cycle) — genuinely different from, and stronger than, the
> single-point-exploration technique used for Theorem 1's mean.

**Conjecture (general `K`, NOT proved here).**
`f_{M_K}(x) = 2Kx(1-x^2)^{K-1}` for `K ≥ 2`. Reduces to `2x` at `K=1`;
its mean matches `φ_K` exactly by a proved integration-by-parts identity
(necessary, not sufficient, for the density itself to be correct);
supported by Kolmogorov–Smirnov tests at `K=1,2,3` (no rejection, two
independent implementations) and — most substantively — by an *external*
theorem for a *different* microscopic model with the same conditional-`K`
limit:

> **Hansen & Jaworski, "Structural transition in random mappings,"
> *Electronic Journal of Combinatorics* 21(1) (2014), #P1.18, Theorem
> 7(ii).** For their model `T̂ⁿᵣ` (a uniform random mapping with `r`
> vertices constrained to in-degree ≤ 1 and `a = n−r` vertices allowed
> in-degree ≤ 2), fixed `a` and `k = ⌊xn⌋`:
> `Pr{X̂ⁿᵣ = k} ∼ (1/n)·2ax(1-x²)^{a-1}` — the *same* functional form,
> with `a ↔ K`.

The two microscopic models are structurally different (Hansen–Jaworski's
is a uniform draw under an in-degree constraint, no permutation-plus-
reroute mechanism at all); the coincidence of their conditional-`K`
limit law is exactly the kind of universality fact that is flagged, not
assumed. Theorem 7(ii) does **not**, by itself, prove the conjecture
above for this ensemble — it is independent supporting evidence for a
claim that remains a conjecture on this side. See `README.md` for the
literature-priority verdict on this connection (component 3: **already
known**, this exact citation).

---

## 6. The n→∞ bridge: what is proved, what is open

Theorem 1 (§3) and Lemma 2 (§5) are statements **about `L(c)` itself**,
taken as given. The separate question is whether the *finite* model
`φ(n,c)` (§1) actually converges to `φ_∞(c)` as `n → ∞`. This is
**not** fully closed. What is proved:

- **Exact mixture identity (no approximation).** For every finite `n`,
  `φ(n,c) = Σ_{K=0}^n C(n,K)(c/n)^K(1-c/n)^{n-K} φ_n^{(K)}`, where
  `φ_n^{(K)} := φ(n,c)` conditioned on exactly `K` rerouted points — a
  purely combinatorial quantity independent of `c`. (`simulations/finite_n.py`
  implements and verifies this identity by brute force.)
- **Mixing reduction (PROVED, unconditionally).** *If* `φ_n^{(K)} → φ_K`
  for every fixed `K`, *then* `φ(n,c) → φ_∞(c)`. Proved via the Poisson
  limit theorem (Scheffé's lemma for the `d_TV → 0` part) plus a
  Chernoff-type uniform-in-`n` tail bound on `Binomial(n,c/n)`, both
  derived from scratch, not merely cited.
- **`K=0` (trivial, exact for every `n`).** `φ_n^{(0)} = 1` — no reroutes
  means `f=π`, a bijection, every point cyclic.
- **`K=1` (PROVED exactly, with an explicit rate).**
  `φ_n^{(1)} = 2/3 + 1/(3n²)`, exactly, for every `n`. Proved by a
  case-split on the uniform cycle length `L` containing the rerouted
  point and the uniform destination `U`. `simulations/finite_n.py`
  brute-force-verifies this identity exactly (rational arithmetic) for
  `n` up to 9.
- **`K=2` (PROVED exactly, with an explicit rate — resolved after the
  package's initial release).**
  `φ_n^{(2)} = 8/15 + 1/(30n) + 7/(10n²) + 1/(5n³)`, exactly, for every
  `n ≥ 3`. Proved by a reduction lemma — valid for every fixed `K` —
  splitting `φ_n^{(K)}` into a weighted average of a "generic point"
  quantity `ψ_n^{(K)}` and a "rerouted point itself" quantity
  `ψ_n^{(K),R}`, whose weight `K/n → 0` for fixed `K`; at `K=2` an
  explicit discrete exploration/case-analysis argument (case-splitting
  on whether each of the two reroutes lies on the reference point's own
  `π`-cycle, using the elementary fact that two fixed points of a
  uniform permutation of size `m` share a cycle with probability
  exactly `1/2`, independent of `m`) computes both `ψ_n^{(2)} = 8/15 +
  4/(15n) + 1/(15n²)` and `ψ_n^{(2),R} = (5n+2)(n+1)/(12n²)` in closed
  form. Both this method and the final closed form were verified by
  exact rational brute-force enumeration (`n` up to 9) and, separately,
  by an independent adversarial referee who re-derived every piece from
  scratch and found no error (archive record:
  `.../u12_universality/theorem/k2_open_lemma/ATTEMPT.md` and
  `adversarial/REFEREE_REPORT.md`). **The rate is `Θ(1/n)` (leading
  term `1/(30n)`), not `Θ(1/n²)`** — this is the correct resolution of
  what looked, in this package's original `n²`-rescaled table
  (`simulations/finite_n.py`, `n` up to 7-8), like a rate that simply
  never settled: it was never going to settle under that rescaling,
  because the true leading correction is order `1/n`, not `1/n²`. The
  `K=1 → K=2` jump from a clean `Θ(1/n²)` to `Θ(1/n)` reflects a genuine
  structural difference, not an error: at `K=1`, `ψ_n^{(1)}`'s and
  `ψ_n^{(1),R}`'s own `Θ(1/n)` corrections cancel *exactly* when
  recombined; at `K=2` they very nearly, but not exactly, cancel,
  leaving a small residual `Θ(1/n)` term.

- **`K=3` (PROVED exactly, with an explicit rate — resolved by a
  genuinely different technique from `K=1,2`).**
  `ψ_n^{(3)} = 16/35 + 12/(35n) + 5/(28n²) + 3/(70n³)` and
  `φ_n^{(3)} = 16/35 + 1/(14n) + 11/(10n²) + 23/(35n³) + 6/(35n⁴)`,
  both exactly, for every `n ≥ 4`. The `K=1,2` proofs above work by hand
  case-analysis (splitting on where the reroute source(s) land relative
  to the reference point's own cycle), a method that grows
  combinatorially with `K` and was explicitly diagnosed, at the end of
  the `K=2` result, as not extending to `K=3` by more of the same
  casework. `K=3` is instead proved by a *structurally different*
  method: the discrete exploration walk underlying the `K=1,2` reduction
  is reformulated as an explicit, exact **`K`-uniform Markov chain** on
  a 3-integer state `(a,b,r)` — `a` = points already queried as
  `π`-images, `b` = points reached by a reroute jump into unexplored
  territory, `r` = number of the `K` reroute sources not yet reached —
  whose transition rule is derived once, for general `K`, from the same
  permutation-exchangeability fact the `K=1,2` proofs already used.
  Solving the resulting linear recursion level by level in `r` (a
  standard falling-factorial/hockey-stick telescoping-sum identity,
  executed symbolically once per level, `r=0,1,2,3`) is a *mechanical*
  procedure, not a fresh hand argument — and it first reproduces the
  already-proved `K=1,2` closed forms exactly, as an internal check,
  before being pushed one level further to close `K=3`. Verified six
  independent ways (method reproduces `K=1,2`; matches the `K=2`
  proof's own brute-force log at `n=4..8`; matches a fresh brute-force
  run at `n=9`, never computed before; matches an independently-coded,
  non-symbolic direct recursion; the recombined `φ_n^{(3)}` matches a
  third, independent brute-force enumeration of the raw Definition-4
  average; 20/20 automated checks pass) and then independently
  re-derived from scratch by a separate adversarial referee, who solved
  the same recursion by a different technique (an integrating-factor
  method instead of the symbolic telescoping sum), substituted every
  closed form back into the recursion symbolically, re-ran every script
  including the ~7.5-minute `n=9` brute force, and reported **no error
  at any layer** (archive record:
  `.../u12_universality/theorem/k2_open_lemma/k3_attempt_2/ATTEMPT.md`
  and `adversarial/REFEREE_REPORT.md`). The rate is again `Θ(1/n)`
  (leading term `1/(14n)`) — the same order as `K=2`, confirming that
  `K=2`'s jump away from `K=1`'s clean `Θ(1/n²)` was not a fluke.
- **`K=4`, `K=5` (PROVED exactly, bonus results, same mechanical
  method).** Because the `K=3` procedure above is uniform in `K`,
  climbing two further levels of the same recursion costs no new idea,
  only more arithmetic:
  `ψ_n^{(4)} = 128/315 + 128/(315n) + 103/(315n²) + 52/(315n³) + 4/(105n⁴)`
  and `ψ_n^{(5)} = (1024n⁵+1280n⁴+1405n³+1105n²+538n+120)/(2772n⁵)`, both
  exact and both verified against fresh brute-force enumeration, proving
  `φ_n^{(K)} → φ_K` unconditionally at `K=4,5` too, via the same
  reduction identity used at `K=2,3`. Both were also confirmed by the
  same adversarial referee pass described above.
- **`K=6,…,10` (PROVED exactly, same mechanical method run five further
  levels).** Running the identical `K`-uniform transfer-matrix procedure
  five more rungs, past `K=5`, costs no new idea, only more arithmetic:
  `ψ_n^{(6)} = (2048n⁶+3072n⁵+4293n⁴+4638n³+3529n²+1662n+360)/(6006n⁶)`,
  proving `φ_n^{(6)} → φ_6 = 1024/3003` unconditionally, via the same
  reduction identity, for every `n ≥ 7`. The analogous exact closed forms
  for `K=7,8,9,10` exist by the identical procedure and are each
  independently verified to have `n→∞` limit exactly `φ_K` (full
  formulas: archive record
  `.../u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/ATTEMPT.md`
  §1.1), extending the fixed-`K` bridge's unconditional resolution
  through `K=10`. The `K=6` closed form was independently re-verified by
  a separate hostile adversarial referee, who substituted every one of
  its 13 constituent closed forms (and, at `K=7`, all 16 of that level's)
  back into the exact defining recursion with zero symbolic discrepancy
  in any case, and who matched the formula bit-for-bit against a fresh,
  independently-coded brute-force enumeration at `K=6,n=7`
  (`355081/823543`, out of `7!×7^6=592,950,960` exhaustively enumerated
  combinations) and, as a second held-out point, at `K=6,n=8`
  (`191647/458752`, out of `8!×8^6=10,569,646,080` combinations).
- **The general-`K` rate — CONFIRMED unconditionally for `K=0,…,10`;
  PROVED for every `K`, conditional on one precisely-named regularity
  hypothesis.** Across all eleven now-proved closed forms,
  `lim_{n→∞} n(ψ_n^{(K)} − φ_K) = (K/4)·φ_K` holds *exactly*, for every
  one of `K=0,1,…,10` individually (eleven independently-derived closed
  forms, not a fit to data) — this part is **PROVED, unconditionally**,
  with no hypothesis. Separately, a genuinely new technique proves the
  identity for **every** `K` at once: take the `n→∞` scaling limit of the
  same `(a,b,r)` Markov chain *before* solving it in `r` (rather than
  after, as the concrete ladder above does), turning the exact discrete
  recursion into a linear ODE in the scaling variable `t=m/n`, with `r`
  now an ordinary symbolic parameter. Solving this ODE by diagonal
  coefficient matching gives closed forms, symbolic in `r`, for the
  leading order `F_r(t,b) := lim_n g_r(nt,b)` and the `O(1/n)` correction
  `G_r(t,b) := lim_n n[g_r(nt,b)-F_r(t,b)]`; `F_r(1,0)=φ_r` re-derives the
  Wallis-integral mean by a new route, and `G_r(1,0)=rφ_r/4` — proved by
  an elementary binomial-sum symmetry identity — is exactly the rate
  conjecture, for every `K`. **The one honest caveat:** this derivation
  establishes what `F_r,G_r` *must* equal *if* `g_r(m,b)` admits a
  regular two-term asymptotic expansion of the specific polynomial-in-`t`
  shape used throughout, for every `r`; the *existence* of that expansion
  for `r` beyond the eleven concretely-verified values (`K=0,…,10`) is
  not independently re-derived here from first principles (e.g. by a
  discrete-Gronwall-type error bound). Wherever this hypothesis can be
  checked against an independent, unconditionally proved computation, it
  holds exactly, with zero exceptions, across all eleven checkable
  values. An independent hostile adversarial referee re-derived both
  ODEs by hand, the `F_r`/`G_r` closed forms symbolically for general
  `r,k,b`, and the binomial-sum identity, finding zero errors, and
  additionally tested `F_r,G_r` against exact ground truth at `t≠1` (45
  new data points, `r=0,…,5`, symbolic `b`) — zero discrepancies. Asked
  explicitly whether the caveat is correctly scoped, too conservative, or
  too optimistic, the referee's verdict, adopted in full: **it is
  correctly scoped — neither too optimistic nor too conservative**
  (archive record: same `k6_attempt/ATTEMPT.md` §2–§4, and
  `k6_attempt/adversarial/REFEREE_REPORT.md`).

**The exact open gap, narrowed further.** For `K ≥ 11`, `φ_n^{(K)} → φ_K`
(the "fixed-`K` bridge," i.e. the Open Lemma itself) is **neither proved
nor disproved unconditionally**. A finite limit `lim_n n(ψ_n^{(K)}-φ_K)`
forces `ψ_n^{(K)}-φ_K→0` as an elementary consequence (if the difference
did not vanish, multiplying by `n→∞` could not converge to a finite
value) — so the continuum-scaling-limit technique's conditional proof of
the associated **rate** for every `K` already conditionally discharges
the Open Lemma itself too, as an immediate corollary, on the identical
regularity hypothesis. That hypothesis — existence of the two-term
asymptotic expansion, for `K` beyond the eleven concretely checked
values — is not independently established from first principles, so
nothing here closes the Open Lemma *unconditionally* for `K≥11`; it
remains open exactly as the rate does (proved conditionally, open
unconditionally), not resolved by any weaker or stronger margin. The
exact, all-orders, general-`K` finite-`n` closed form for `ψ_n^{(K)}`
(of which the two-order continuum expansion is only a truncation) is
not attempted at all.

Consequently: the full statement "`φ(n,c) → φ_∞(c)` for every `c`" is a
**conditional proposition** — it follows from the (unconditionally
proved) mixing reduction *given* the open `K≥11` bridge lemma (narrowed
from `K≥6`, now that `K=6,…,10` are proved), which remains open. It is not
a theorem in its own right. The empirical control that exists (exact
enumeration to small `n`, Monte Carlo to large `n`, both reproduced in
`simulations/`) is evidence for this conditional statement, not a proof
of it.

---

## 7. Conjectures (stated separately from proofs)

1. **General-`K` density** `f_{M_K}(x) = 2Kx(1-x^2)^{K-1}` for `K ≥ 2`
   (§5). Proved only at `K=1`.
2. **Full unconditional distributional law**
   `M(c) \stackrel{d}{=} \min(1, \sqrt{E/c})`, `E ~ Exp(1)`, i.e.
   `P(M(c) ≤ x) = 1 - e^{-cx^2}` for `x<1` with an atom `e^{-c}` at
   `x=1` — the Poisson(`c`)-mixture of Conjecture 1. Its *mean* is
   `φ_∞(c)`, proved (Theorem 1); only the full distribution around that
   mean is conjectural.

3. ~~General-`K` rate of the fixed-`K` bridge~~ — **no longer a
   conjecture.** `lim_{n→∞} n(ψ_n^{(K)} − φ_K) = (K/4)·φ_K` (§6) is
   **PROVED, unconditionally**, for `K=0,…,10` (eleven independently
   derived closed forms), and **PROVED for every `K`, conditional on** the
   regularity hypothesis named in §6 (existence of a two-term asymptotic
   expansion, for `K` beyond those eleven values). It is retained here
   only to record that it is *not* fully unconditional for general `K` —
   the caveat is real, precisely named, and adversarially judged
   correctly scoped, but it is a hypothesis, not a proof from first
   principles, so this item is not promoted to §§1–6's PROVED tier
   without qualification.

Neither density conjecture above (1–2) is used anywhere above as though
it were proved; both are numerically supported (Kolmogorov–Smirnov
tests, no rejection) and neither is claimed as established. The general
rate conjecture (3) is likewise never treated as fully unconditional
beyond the eleven values it was actually verified at without hypothesis.
The `K≥11` fixed-`K` bridge (§6, the Open Lemma itself) is a distinct,
fourth kind of open item — a convergence statement between two
well-defined finite/infinite objects, not a guessed closed form or a
guessed asymptotic coefficient — and is not counted among Conjectures
1–3 for that reason; it shares item 3's conditional proof route in
full, not just for the rate: a finite limit of `n(ψ_n^{(K)}-φ_K)`
elementarily forces `ψ_n^{(K)}→φ_K`, so item 3's conditional rate proof
already conditionally discharges the bare convergence too, on the
identical hypothesis — it is only the *unconditional* resolution that
remains missing, for the bridge exactly as much as for the rate. (Note: this is
unrelated to the general-`K` density Conjecture 1 above, which remains
open for every `K≥2` — the `K=2,…,10` results resolved in §6 are about
the *mean* `φ_n^{(K)}→φ_K`, not about the full distributional law
`f_{M_K}(x)`.)

