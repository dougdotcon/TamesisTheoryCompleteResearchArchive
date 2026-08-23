# DERIVATION_PREREG — Hypothesis (U') via the exact all-orders closed form

**Wave 13, `DISC-DEC-054`, front (a) `U-PRIME-HYPOTHESIS-ATTEMPT`.** Written
after a small amount of *throwaway* float/mpmath exploration (not reported as
final numbers below) established that the route sketched in §1 is promising,
and BEFORE any of the exact-arithmetic verification runs that produce the
numbers reported in `ATTEMPT.md` are executed. Pure combinatorics/asymptotics
on the `u12` recursion; no external data, no randomness needed (the object is
entirely deterministic/combinatorial), no governance edits.

---

## 1. The route, derived from the prose sources

Read in full, as required: `uniform_in_c_attempt/ATTEMPT.md` §6 (all of it,
plus the `[Correção pós-adversarial, 2026-08-23]` block); `THEOREM.md`
Estágio 7 (`c_K` exact, `= [(K+2)φ_K-2]/4`), Estágio 9 (all-orders closed form
`ψ_n^{(K)}`, Corolário A1, and Teorema B for `h_r(a,b)`), Estágio 11 (`M_K`
qualitative geometricity, Route A, and its explicit statement that Route A's
`M_K ≤ φ_K(K+1)e^{K/2}+K` bound is a **different, strictly weaker** fact than
(U') and does not close it); `mk_geometricity_attempt/ATTEMPT.md` §2 (Route A
in full: Step 2's elementary-symmetric-polynomial monotonicity proof that
`n(ψ_n^{(K)}-φ_K)` is nonincreasing in `n` with sup at `n=K+1`; Step 4's
Reduction Lemma A step, `n(φ_n^{(K)}-φ_K) = n(ψ_n^{(K)}-φ_K) +
K(ψ_n^{(K),R}-ψ_n^{(K)})`, with the crude bound `|ψ^{(K),R}-ψ^{(K)}|≤1`
flagged as the loose step); `k2_open_lemma/ATTEMPT.md` §2 (Reduction Lemma A
itself, and the exact definitions `ψ_n^{(K)}:=P(K{+}1\text{ cyclic})`,
`ψ_n^{(K),R}:=P(1\text{ cyclic})`); `k2_open_lemma/k3_attempt_2/ATTEMPT.md`
§2 (the `(a,b,r)` Markov chain, and the identification `ψ_n^{(K)}=g(0,0,K)`,
`ψ_n^{(K),R}=h(0,0,K{-}1)`); `.../all_orders_closed_form_attempt/ATTEMPT.md`
§1 and §4 (Theorem A's closed form for `g_r(m,b)`, Theorem B's reduction
`h_r(a,b)=\frac{n-a+1}n\hat g_r(n{-}a{+}1,b{+}1)`, including the explicit
domain caveat that `a=0` evaluates `\hat g` **out of its ordinary
probabilistic domain**, which is exactly the case needed here).

**The gap identified.** Route A of `mk_geometricity_attempt` bounds the
correction term `K|ψ_n^{(K),R}-ψ_n^{(K)}|` crudely by `K` (using only that
both quantities are probabilities in `[0,1]`), which is why it proves
geometric growth of `M_K`, not `O(√K)`. But `ψ_n^{(K),R}=h(0,0,K{-}1)`, and
Theorem B of the all-orders document gives `h_r(a,b)` in closed form too
(`a=0`, `r=K{-}1`, `b=0`) — this closed form was derived by wave 11 for a
different purpose (the general-`r` residual constants) and has, as far as
this front's review of the archive shows, never been specialized to
`ψ_n^{(K),R}` or combined with Corolário A1's `ψ_n^{(K)}` formula to get an
**exact, closed-form expression for `φ_n^{(K)}-φ_K` itself** (not just its
`n→∞` limit or a crude geometric bound). That combination is this front's
target.

**Throwaway probe finding (informational, not final, not cited as a proof
below).** A first hand derivation of `ψ_n^{(K),R}` from Theorem B, cross-
checked against `chain.py`'s independent exact recursion for `K=0..7`,
`n=K+1..K+8` (64/64 exact `Fraction` matches — `chain.py` is wave 11's
from-scratch engine, never touched by the derivation being checked), gives

`ψ_n^{(K),R} = κ Σ_{i=1}^K C(2K,K-i) g(i;n)`, `κ:=(K-1)!K!/(2K)!`, `g(i;n):=(n+i)!/(n!n^i)`,

and combining with Corolário A1 via Lemma A and simplifying (Pascal's rule
`C(2K+1,K-j)=C(2K,K-j)+C(2K,K-j-1)` plus the binomial-ratio identity
`C(2K,K-j-1)/C(2K,K-j)=(K-j)/(K+j+1)`) collapses `T(n,K):=n(φ_n^{(K)}-φ_K)`
into a sum of **manifestly nonnegative, nonincreasing-in-`n`** pieces —
suggesting fact (i) of §6.3 (sup over `n` at `n=K+1`) may be provable for
`φ_n^{(K)}` itself, not just for `ψ_n^{(K)}` (which `mk_geometricity` already
proved). This is the target below; it is stated here as a *candidate*, to be
either confirmed by the pre-registered checks or abandoned honestly.

---

## 2. Target claims (to prove, not assume)

> **Claim 1 (exact decomposition).** For every `K≥0` there is an identity
> `T(n,K)/A = \mathrm{CONST}(K) + Σ_{j=1}^K\big[C(2K{+}1,K{-}j)f_j(n) +
> B_j(K)(g(j;n){-}1)\big]`, `A:=φ_K/4^K`, `f_j(n):=n(g(j;n){-}1)`,
> `\mathrm{CONST}(K):=2^{2K-1}-\tfrac{2K+1}2C(2K,K)`,
> `B_j(K):=\tfrac{(2K+1)(j+1)}{K+j+1}C(2K,K{-}j)`, with every coefficient
> `≥0` and every `f_j(n),(g(j;n){-}1)` nonnegative and nonincreasing in `n`
> (the latter two already essentially proved by `mk_geometricity_attempt`
> §2.2's elementary-symmetric-polynomial argument, reused not re-derived).

> **Claim 2 (fact (i), closed).** Consequently `T(n,K)` is nonnegative and
> nonincreasing in `n` for `n≥K+1`, for **every** `K` (not a numerical
> observation up to `K=16384` — a proof for all `K`). Hence
> `M_K:=\sup_{n≥K+1}|T(n,K)| = T(K{+}1,K)`.

> **Claim 3 (exact value of `M_K`).** `M_K = Q(K{+}1)-(K{+}1)φ_K` exactly,
> where `Q` is the Ramanujan `Q`-function of Proposição 7.1 — via the
> `[Correção pós-adversarial]` fact `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n` applied at
> `n=K{+}1`, plus the derivation that `ψ_{K+1}^{(K),R}=ψ_{K+1}^{(K)}` exactly
> (both sources of the Lemma-A average collapse to the same value at the
> `K=n-1` endpoint), which forces `φ_{K+1}^{(K)}=ψ_{K+1}^{(K)}` there too.

> **Claim 4 ((U'), PROVED with an explicit, non-sharp constant).** Using two
> elementary sandwich bounds — `\sqrt{π/2}/\sqrt{K+1} < φ_K <
> \sqrt{π/2}/\sqrt K` for `K≥1` (proved from the exact ratio
> `φ_{K+1}/φ_K=(2K{+}2)/(2K{+}3)` plus monotonicity of `Kφ_K^2` and
> `(K{+}1)φ_K^2`, citing only the classical Wallis limit
> `Kφ_K^2\to π/4`) and `Q(n) ≤ 1+\sqrt{πn/2}` for `n≥1` (proved elementarily
> from `1-x≤e^{-x}` plus a Gaussian-integral comparison) — combined with the
> `K=n` boundary case via the *same* two bounds:
>
> `\displaystyle |φ_n^{(K)}-φ_K| ≤ \big(1+\sqrt{π/2}\big)\frac{\sqrt K}n`
> for **every** integer `n≥1` and `0≤K≤n`.

**If Claim 1 fails the symbolic check below:** fall back to reporting
whatever weaker/partial fact survives (e.g. Claim 2 alone if provable by a
different route, or nothing beyond what Estágio 11 already has) — this is a
fully acceptable outcome per the task's discipline, and will be written up
honestly as such, not forced.

---

## 3. Planned tests, in order, with pass/fail criteria fixed now

1. **T1 — symbolic identity check (sympy, `K=0..8`, symbolic in `n`).**
   Verify Claim 1's identity as an exact rational-function identity in `n`
   (clear denominators or `sympy.simplify(LHS-RHS)`). **Pass:** `0` for
   every `K` tested. **Fail:** any nonzero residual — Claim 1 is then false
   as stated and must be re-derived or abandoned.
2. **T2 — the coefficient sub-identity, exact integer check, `K≤300`, all
   `j≤K`.** `(K{+}1)C(2K,K{-}j)-K\,C(2K,K{-}j{-}1) =
   C(2K,K{-}j)\frac{(2K+1)(j+1)}{K+j+1}` in exact `Fraction`/`int`
   arithmetic — this is the algebraic fact `B_j(K)`'s derivation rests on.
   **Pass:** `0` mismatches. This plus the two cited elementary facts
   (Pascal's rule, the binomial-ratio identity) constitutes a **general-`K`
   proof**, not just a large-`K` numerical check — the check is run to
   catch any transcription error in the hand derivation, not as the proof
   itself.
3. **T3 — closed form vs. the independent `chain.py` recursion, exact
   `Fraction`, `K=0..9`, `n=K+1..K+30`.** Cross-checks `φ_n^{(K)}` computed
   via the Corolário-A1 + Theorem-B route against `chain.py`'s from-scratch
   `(j,R)`-recursion (never touched by this derivation). **Pass:** every
   value matches exactly. Also checks `T(n,K)` is nonincreasing and
   `T(K+1,K)=\max_n T(n,K)` on this exact grid (Claim 2, direct evidence).
4. **T4 — exact value of `M_K` vs. `Q(K{+}1)-(K{+}1)φ_K`, `Fraction`,
   `K=0..40`.** Via `chain.py`'s recursion at `n=K{+}1` (not the closed
   form, for independence) compared to an independently-coded exact `Q(n)`.
   **Pass:** exact equality every time (Claim 3).
5. **T5 — the four elementary inequalities behind Claim 4, `mpmath` 40-digit
   precision, wide `K`/`n` grids up to `K,n\sim10^5`.** (a) `φ_K` sandwich;
   (b) `Q(n)≤1+\sqrt{πn/2}`; (c) `n/\sqrt{n{+}1}≥\sqrt n - 1`; (d) the
   assembled bound `|φ_n^{(K)}-φ_K|≤(1{+}\sqrt{π/2})\sqrt K/n` itself,
   sampled at `n=K{+}1`, `n=K` (the two binding cases identified by the
   hand proof) and several interior `n`. **Pass:** zero violations anywhere
   on the grid — this is a *sanity check* on an already-elementary, already
   hand-verified proof, not the proof itself; a violation here means the
   hand algebra has an error and Claim 4 must be re-derived, not patched.

No claim is reported as PROVED in `ATTEMPT.md` on the basis of T1/T3/T4/T5
alone (numerical/symbolic-at-fixed-K checks) unless the general-`K` hand
proof is also written out in full and holds up on its own; the tests exist to
catch transcription errors in that hand proof, exactly per the archive's
"exact arithmetic for anything PROVED" rule.

---

## 4. Seeds

None used. This front is entirely deterministic (exact rational/integer
arithmetic and elementary real analysis) — no Monte Carlo, no random search.

---

## 5. Files planned

`verify_decomposition.py` (T1, T2), `verify_closed_form.py` (T3, T4),
`verify_inequalities.py` (T5), each with a matching `.log`; `ATTEMPT.md`
written last, after all logs exist.
