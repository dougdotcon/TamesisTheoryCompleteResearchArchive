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

**The exact open gap.** For `K ≥ 2`, `φ_n^{(K)} → φ_K` (the "fixed-`K`
bridge") is **neither proved nor disproved**. A single reroute disturbs
exactly one background cycle (tractable, §K=1 above); `K ≥ 2` reroutes
can strike the same cycle in either order or strike different cycles
whose severed pieces later re-link — a combinatorial explosion not
resolved here. Exact enumeration at `K=2` (`simulations/finite_n.py`,
`n` up to 7-8) shows `φ_n^{(2)}` decreasing monotonically toward `φ_2`,
but the rescaled deviation `n²(φ_n^{(2)}-φ_2)` is *not* settling to a
constant over the tested range — so, unlike `K=1`'s clean `O(1/n²)`
rate, **no specific convergence rate for `K≥2` should be assumed**.

Consequently: the full statement "`φ(n,c) → φ_∞(c)` for every `c`" is a
**conditional proposition** — it follows from the (unconditionally
proved) mixing reduction *given* the open `K≥2` bridge lemma, which
remains open. It is not a theorem in its own right. The empirical
control that exists (exact enumeration to small `n`, Monte Carlo to
large `n`, both reproduced in `simulations/`) is evidence for this
conditional statement, not a proof of it.

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

Neither conjecture is used anywhere above as though it were proved; both
are numerically supported (Kolmogorov–Smirnov tests, no rejection) and
neither is claimed as established. The `K≥2` fixed-`K` bridge (§6) is a
distinct, third kind of open item — a convergence statement between
two well-defined finite/infinite objects, not a guessed closed form —
and is not counted as a "Conjecture 3" for that reason.

