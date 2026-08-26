# PREREG — the distributional bridge `M_n(c) →_d M(c)`

**Front:** wave 18, front (d), `DISTRIBUTIONAL-BRIDGE-ATTEMPT`, authorized
by `DISC-DEC-078`. Pure combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble. Not a Millennium Problem, and
no claim of the kind is made anywhere in this front's output.

## 1. Exact target

Fix `c ≥ 0`. Under `THEOREM.md` Definition 1, let

`M_n(c) := #{i : i cyclic for f} / n`

be the **random variable** (not its expectation `φ(n,c)=E[M_n(c)]`,
already handled by Teorema 3 / Estágio 22's `Δ_n` bound) giving the
observed cyclic-mass fraction in one draw of the finite model. The
target continuum object is `M(c) =_d min(1,√(E/c))`, `E~Exp(1)`, i.e.

`F(x) := P(M(c) ≤ x) = 1 - e^{-cx²}` for `x∈[0,1)`, atom `P(M(c)=1)=e^{-c}`.

**Target statement (the one this front attacks).** For every fixed
`c≥0`, `M_n(c) →_d M(c)` as `n→∞` — equivalently (Portmanteau, since
both laws are supported on the bounded set `[0,1]` and `F` is continuous
on `(0,1)`), `F_n(x) := P(M_n(c)≤x) → F(x)` for every `x∈(0,1)`.

This is explicitly **not** Teorema 3 (mean convergence, closed
unconditionally since Estágio 6, sharp-rate uniform-in-`c` since Estágio
22) and **not** Conjecture 1/2 (the exact laws of `M_K`/`M(c)` on the
continuum object `L(c)`, both now PROVED for every `K`, Estágio 24). It
is the third, structurally different question `THEOREM.md` §8/Estágio 24
names explicitly and leaves untouched: does the actual finite-`n` random
variable converge, as a distribution, to the continuum one. No front has
directly attacked it before this one.

## 2. Planned strategy

**S1 (exact mixture identity, both sides — expected easy).** Definition
4's conditioning argument (already used for the mean, `THEOREM.md`
Fact 4.1/§7.2) extends verbatim from expectations to full conditional
laws: conditional on `K_n=K`, `M_n(c)` is distributed exactly as the
random variable `M_n^{(K)} := #cyclic(f)/n` under the `K`-conditional
model of Definition 4. Hence, for every `n,x`:

`F_n(x) = Σ_{K=0}^n P(Bin(n,c/n)=K) F_n^{(K)}(x)`, `F_n^{(K)}(x):=P(M_n^{(K)}≤x)`.

On the continuum side, Estágio 24 already gives (Kingman conditioning +
countable additivity, cited) `F(x) = Σ_K e^{-c}c^K/K! · F_K(x)`, `F_K(x)
=1-(1-x²)^K` (from Conjecture 1's now-proved density).

**S2 (the reduction lemma — expected achievable, genuinely new).**
Adapt Proposition 3's mixing-convergence proof (`THEOREM.md` §7.2) from
scalars (`φ_n^{(K)}→φ_K`) to a fixed real `x`
(`F_n^{(K)}(x)→F_K(x)`). The proof machinery (Scheffé for the
Binomial→Poisson part `B_n`, the from-scratch Chernoff tail bound
`δ(c,M)` for the truncation part of `A_n`) uses only that the summands
are bounded in `[0,1]` — true of `F_n^{(K)}(x),F_K(x)` exactly as it was
of `φ_n^{(K)},φ_K` — so the proof should transplant essentially
verbatim, with `x` carried as a fixed parameter throughout. Expected
output: **Lemma R**, "fixed-`K` CDF convergence for every `K`
`⟹` the Target statement," fully proved, unconditionally.

**S3 (attack the fixed-`K` hypothesis, case by case, exactly as
`THEOREM.md` §7.3–§7.4 did for the mean, but now for the FULL law).**

- `K=0`: expected trivial exact identity (`M_n^{(0)}≡1`).
- `K=1`: Proposition 4's proof (`THEOREM.md` §7.3) already derives the
  *joint* law of `(L,U)` — the length of the struck cycle and the
  reroute target — and a case split for the exact cyclic count `T` as a
  function of `(L,U)`, not just its mean. Plan: extract the full
  conditional law of `T` given `L=ℓ` from that same case split (already
  proved, no new probabilistic input needed), sum over `L~Unif{1,…,n}`
  to get an exact finite-`n` CDF, and take `n→∞`. This is the highest-
  confidence target of the whole front.
- `K≥2`: the mean-bridge machinery of Estágios 3–7 (`ψ_n^{(K)}`, the
  generic-point reduction) is a **single-point marginal** device — by
  construction it only ever computes `P(x_0 cyclic)`, which recovers
  the mean by exchangeability but carries no information about the
  *joint* behavior of two or more points, hence nothing about the
  variance or CDF of `M_n^{(K)}`. The natural lever for a *second*
  moment is the exchangeability identity `E[(M_n^{(K)})^2] =
  φ_n^{(K)}/n + (1-1/n)P_both(n,K)`, `P_both(n,K):=P(1,2\text{ both
  cyclic})`. `THEOREM.md`'s own joint-two-point front (Estágio 18/25)
  diagnosed the *analogous* continuum quantity as the hard obstruction
  in this whole line, and Estágio 25's Theorem J gives the exact
  50/50 same/different-cycle split at every finite `n,K` but explicitly
  states this does **not** give the value of `P_both` itself. Plan:
  attempt a 2-point generalization of Estágio 3's Reduction Lemma A
  (showing the "at least one of the pair is itself rerouted" correction
  is `O(K/n)→0`, leaving only the generic-untouched-pair term), which
  is expected tractable; attempt an exact K=2 case analysis for the
  surviving term by hand, expected **hard** (the archive's own
  `k2_open_lemma/ATTEMPT.md` §7 already documents the combinatorial
  blow-up of case analysis with `K`, for the *marginal* problem, which
  is strictly easier than the joint one attempted here). Honest
  non-closure at `K≥2` is the single most likely outcome of this whole
  front and is pre-declared fully acceptable.

**S4 (numerical exploration, exact enumeration + Monte Carlo).** For
`K=1,2,3` and a handful of `n`, exact enumeration of the *full*
distribution of `#cyclic(f)` under Definition 4 (not just its mean),
comparing the empirical CDF to `F_K`. For larger `n`, Monte Carlo
(reserved seeds `20260876000`–`20260877000`) of the same, plus of the
mixed-`c` model `M_n(c)` directly against `F(x)=1-e^{-cx^2}`. This is
evidence, never a substitute for S2/S3's proofs, and is labeled as such
throughout.

## 3. What counts as honest non-closure

- If S2 (Lemma R) closes but S3 only closes `K=0,1`: the deliverable is
  a **conditional** distributional bridge — full weak convergence
  `M_n(c)→_d M(c)` reduced, rigorously and unconditionally, to the
  single remaining hypothesis "`F_n^{(K)}→F_K` pointwise, for every
  `K≥2`" — structurally the same honest shape `THEOREM.md` itself used
  for the mean bridge between Estágio 2 and Estágio 6, now transplanted
  one level up (full laws instead of means). This is the expected,
  fully acceptable outcome.
- If the `K=2` case analysis in S3 also fails to close (the likely
  outcome, given `k2_open_lemma`'s own account of the cost growth), the
  gap is reported precisely: not "the bridge is hard" in general terms,
  but the specific missing fact (`P_both(n,2)`'s exact or asymptotic
  value, or the full conditional law of `T` given the two-reroute
  configuration) with whatever partial reduction was achieved (e.g. the
  `O(K/n)` correction-vanishes lemma) clearly separated from what
  wasn't.
- Numerical exploration (S4) will be reported with explicit sample
  sizes / enumeration bounds and is never used to upgrade a conjecture
  to a claim of proof.
- Any bug or false start is disclosed in `ATTEMPT.md` §"Self-caught
  issues," per archive convention, whether or not it affected a
  reported number.

## 4. Seeds

Reserved range `20260876000`–`20260877000`. All Monte Carlo in this
front uses `numpy.random.Generator(numpy.random.PCG64(SeedSequence(s)))`
for `s` in this range, tabulated in `ATTEMPT.md`'s seeds table. No use
of the referee range `20260877000+`.

## 5. Scope discipline

No edits to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`. No `adversarial/` subdirectory, no self-
dispatched referee. No git commands. All claims in the final `ATTEMPT.md`
labeled PROVED / CITED / NUMERICALLY EXPLORED / CONJECTURE / OPEN,
individually, at the point of use.
