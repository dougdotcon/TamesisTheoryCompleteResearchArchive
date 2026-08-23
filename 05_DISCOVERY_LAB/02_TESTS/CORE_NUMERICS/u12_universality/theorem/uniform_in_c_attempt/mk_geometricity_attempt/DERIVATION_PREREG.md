# Pre-registration — `MK-QUALITATIVE-GEOMETRICITY-ATTEMPT`

> Governance. Wave 12, front (a), authorized by `DISC-DEC-051` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Written and saved
> **before** any script is run or any numeric value is computed. Nothing
> outside this directory (`uniform_in_c_attempt/mk_geometricity_attempt/`)
> will be created, modified, or deleted. No git command will be run.

## 1. Target claim

`uniform_in_c_attempt/ATTEMPT.md` §5.6 (Teorema E) is
`PROVED-MODULO-[K-uniform domination]`. The missing ingredient, precisely
named by `uniform_in_c_attempt/adversarial/REFEREE_REPORT.md` §6.2 (F-1),
is:

> a bound `M_K` with `|n(φ_n^{(K)}-φ_K)| ≤ M_K` for every valid `n`, and
> `M_K = O(λ^K)` for **some** finite `λ` (the value of `λ` is irrelevant —
> `Σ_K c^Kλ^K/K! = e^{cλ} < ∞` for every `c`, which is all Teorema E needs).

**Target of this document:** prove such an `M_K` exists, or determine
precisely why it does not / why the route(s) attempted do not close.

## 2. Planned proof strategy

Two routes will be attempted, in this order.

**Route A (primary, new — not the referee's sketch).** Bypass the
`D_r(b)`/`A_r(b)`/`B_r(b)`/Proposição-6 apparatus entirely, using instead
Estágio 9's exact all-orders closed form (`all_orders_closed_form_attempt/ATTEMPT.md`
Corolário A1, `THEOREM.md` Estágio 9, PROVED unconditionally, adversarially
verified with 0 open findings against it):

`ψ_n^{(K)} = (φ_K/4^K) Σ_{j=0}^K C(2K+1,K-j)·(n+j)!/(n!·n^j)`, valid for
every `n ≥ K+1`.

Plan:
1. Write `n(ψ_n^{(K)}-φ_K) = (φ_K/4^K) Σ_{j=0}^K C(2K+1,K-j)·f_j(n)`, where
   `f_j(n) := n[Π_{i=1}^j(1+i/n) - 1] = Σ_{k=1}^j e_k(1,…,j)/n^{k-1}` (`e_k`
   the elementary symmetric polynomials of `{1,…,j}`).
2. Since every `e_k(1,…,j) > 0`, each `f_j(n)` is **strictly decreasing** in
   `n` for `j ≥ 2` (constant in `n` for `j ≤ 1`). All weights
   `C(2K+1,K-j) ≥ 0`. Hence `n(ψ_n^{(K)}-φ_K)` is a nonincreasing function of
   `n`, so its supremum over the valid range `n ≥ K+1` is attained exactly at
   `n = K+1`.
3. Bound `f_j(K+1) = (K+1)[Π_{i=1}^j(1+i/(K+1))-1] ≤ (K+1)[e^{j(j+1)/(2(K+1))}-1]
   ≤ (K+1)e^{K/2}` (using `1+x ≤ e^x` termwise, and `j(j+1)/(2(K+1)) ≤ K/2` for
   `j ≤ K`), giving `M_K^ψ := sup_n n(ψ_n^{(K)}-φ_K) ≤ φ_K(K+1)e^{K/2}` (using
   `Σ_j C(2K+1,K-j) = 2^{2K}` exactly, and `φ_K ≤ 1`).
4. Combine with the already-PROVED Reduction Lemma A (`THEOREM.md` line
   ~1355, `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §0/§2, both
   `ψ_n^{(K)}, ψ_n^{(K),R} ∈ [0,1]` **by definition** — they are literally
   named as probabilities, `P(K+1 cyclic)` and `P(1 cyclic)`):
   `n(φ_n^{(K)}-φ_K) = n(ψ_n^{(K)}-φ_K) + K[ψ_n^{(K),R}-ψ_n^{(K)}]`, hence
   `|n(φ_n^{(K)}-φ_K)| ≤ M_K^ψ + K` (using `|ψ_n^{(K),R}-ψ_n^{(K)}| ≤ 1`).
5. Conclude `M_K ≤ φ_K(K+1)e^{K/2} + K = O(K·(√e)^K)`, i.e. `λ = √e` (any
   larger `λ` works too) — **qualitative geometric growth, PROVED**, if every
   step above survives independent verification.

**Route B (the referee's sketch, attempted for completeness / to honor the
explicit instruction, and to verify its arithmetic claims independently):**
(a) verify `F_r(2,0) = (φ_r/4^r)Σ_{i=0}^r 2^{r-i}C(2r+1,i) ≤ 2φ_r·2^r = O(2^r)`
by hand from Lemma 7 of `error_constant_growth_attempt/ATTEMPT.md` §6.2; (b)
verify the unrolled Proposição 6 recursion
`C'_r(b) ≤ (B_r(b)+A_r(b+1)) + 2C'_{r-1}(b+1)` follows algebraically from the
boxed recursion in `error_constant_growth_attempt/ATTEMPT.md` §6.1; (c)
attempt to bound `A_r(b), B_r(b)` **for general `b`** (not just `b=0`)
geometrically, which is needed because unrolling `C'_K(0)` down to the base
case forces `b` to range over `0,…,K-1` while `r` ranges over `K,…,1`
(invariant `r+b=K`) — this is explicitly *not* established anywhere in the
archive (`error_constant_growth_attempt/ATTEMPT.md` scorecard row 7: "closed
form for `D_r(b),C_r(b),A_r(b)` general `r`: NOT ATTEMPTED"). Route B will be
reported as far as it goes; if Route A succeeds, Route B is not required to
close and will be reported as an open/unattempted secondary route with the
verified arithmetic pieces (a)/(b) recorded honestly.

## 3. Refutation criteria (stated before any computation)

Route A is considered **refuted / not closed** if any of the following is
found:

- R1. Corolário A1's closed form for `ψ_n^{(K)}` fails to reproduce the
  independently-PROVED closed forms `ψ_n^{(1)}=(4n+1)/(6n)`,
  `ψ_n^{(2)}=(8n^2+4n+1)/(15n^2)`, or the `K=3,4,5` forms tabulated in
  `error_constant_growth_attempt/ATTEMPT.md` §7.1 — checked here by
  independent re-derivation (own `sympy`/`Fraction` code, not copied from any
  sibling script), symbolically in `n` where feasible.
- R2. The monotonicity claim ("`f_j(n)` nonincreasing in `n`", hence
  "`n(ψ_n^{(K)}-φ_K)` maximized at `n=K+1`") is contradicted by exact
  evaluation at any `(K,n)` pair in an exhaustive small grid (`K ≤ 40`,
  `n` from `K+1` to `K+200`) or by the elementary-symmetric-function argument
  itself failing symbolic re-derivation.
- R3. The resulting numeric sequence `M_K^ψ` (or the exact quantity
  `(K+1)(ψ_{K+1}^{(K)}-φ_K)`), computed exactly for `K` up to at least `300`,
  fails to satisfy `M_K^ψ ≤ φ_K(K+1)e^{K/2}` for any `K` in range (this would
  mean an algebra error in step 3 above, not a failure of geometricity per
  se, but must be caught and fixed or reported).
- R4. `ψ_n^{(K),R}` turns out **not** to be genuinely bounded in `[0,1]` (this
  would contradict its definition as a probability in
  `k2_open_lemma/k3_attempt_2/ATTEMPT.md` §0 — checked here only by rereading
  the definition again for exact wording, not by new computation, since it is
  a definitional fact, not a numerical one).
- R5. If, after R1–R4 all pass, the *actual* growth rate of `M_K^ψ` computed
  exactly for `K` up to the feasible range turns out, on inspection, to be
  faster than geometric after all (i.e. `log M_K^ψ / K` does not stabilize
  but keeps growing without bound as `K` increases in the tested range) —
  this would not contradict the PROVED upper bound (an upper bound is still a
  valid bound even if not tight) but would be reported as a surprising
  finding requiring a second look at whether the upper-bound derivation
  itself is sound.

If Route A survives R1–R4, the qualitative-geometricity claim is **PROVED**
(modulo the standing archive-wide requirement of independent adversarial
verification before integration) regardless of what R5 shows, since R5 only
concerns tightness, not correctness, of the bound. Route A does **not**
depend on Route B in any way; Route B's closure/non-closure will be reported
honestly as a separate, secondary finding, not used to inflate or deflate
the verdict on Route A.

## 4. What "success" requires, concretely

- Every algebraic step in Route A re-derivable by hand from already-PROVED
  archive facts (Corolário A1, Reduction Lemma A, `ψ_n^{(K)},ψ_n^{(K),R}∈[0,1]`,
  `φ_K ≤ 1`) plus elementary calculus/combinatorics (`1+x≤e^x`, positivity of
  elementary symmetric polynomials of positive reals) — no new unproved
  machinery.
- Independent numeric verification of R1–R4's negations, exact rational
  arithmetic (`fractions.Fraction`) throughout, no floating point except for
  display and for extending the range of the log-ratio sanity check in §3
  (R5), which is explicitly informational, not part of the proof.
- Honest labeling: PROVED steps stay PROVED, anything checked only
  numerically for a finite range is labeled NUMERICALLY VERIFIED, and Route
  B's status (verified sub-arithmetic vs. genuinely open general-`b` bound)
  is reported precisely, not glossed over.

## 5. Randomness / seeds

No Monte Carlo or randomized simulation is planned — every check is exact
combinatorial/symbolic arithmetic or high-precision deterministic evaluation
(`mpmath`, fixed precision, no randomness). If any randomized check becomes
useful during execution, seeds will be drawn from `numpy.random.SeedSequence`
starting at `20260825800` (per the wave-12 governance instruction) and every
seed used will be recorded in a table in `ATTEMPT.md`. As planned, this
section is expected to remain empty of actual seeds.

## 6. Files this document commits to producing

- `verify_corollary_a1.py` / `.log` — R1.
- `verify_monotonicity.py` / `.log` — R2.
- `compute_MK.py` / `.log` — R3, and the exact sequence `M_K^ψ`,
  `K=1,…,300` (or as far as exact arithmetic remains fast), plus a
  higher-`K` `mpmath` extension for the R5 sanity context.
- `route_b_arithmetic.py` / `.log` — Route B's step (a)/(b) verification.
- `ATTEMPT.md` — the final write-up, structured like
  `error_constant_growth_attempt/ATTEMPT.md` (§0 discipline, derivation,
  verification, scorecard, honest verdict).

Timestamp of this pre-registration: recorded by the filesystem at write
time, preceding every script/log file above (all of which will postdate
this file — checked in `ATTEMPT.md` §0 by `ls -la --time-style=full-iso`).
