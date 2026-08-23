# Hypothesis (U'), closed — an exact decomposition, fact (i) proved for every `K`, and an explicit (non-sharp) uniform constant

> **Governance.** Wave 13, `DISC-DEC-054`, front (a) `U-PRIME-HYPOTHESIS-ATTEMPT`.
> Pure combinatorics/asymptotics on the `u12` recursion — no external data, no
> real-world claim, no governance edits. `THEOREM.md` and the parent
> `uniform_in_c_attempt/ATTEMPT.md` are **not** modified by this document —
> everything new lives under this `u_prime_hypothesis_attempt/` directory.
> `DERIVATION_PREREG.md` (this directory) was written and locked before any
> of the exact-arithmetic verification runs reported below were executed (a
> small amount of throwaway float/mpmath exploration preceded it, as the
> preregistration discloses, and is not used as evidence for any claim
> below). Every claim is labelled PROVED, CITED (classical, already used
> elsewhere in this archive), NUMERICALLY VERIFIED, or OPEN.

> **Executive summary (read first).** Hypothesis (U') —
> `|φ_n^{(K)}-φ_K| ≤ a\sqrt K/n` for **all** `0≤K≤n` simultaneously — is
> **PROVED**, with an explicit, fully worked, non-sharp constant
> `a = 1+\sqrt{π/2} = 2.253314\ldots`. The route: (1) an exact closed-form
> identity, combining Estágio 9's all-orders formula for `ψ_n^{(K)}`
> (Corolário A1) with a companion formula for `ψ_n^{(K),R}` derived here from
> Estágio 9's Teorema B, decomposes `T(n,K):=n(φ_n^{(K)}-φ_K)` into a
> **nonnegative combination of manifestly nonincreasing-in-`n` pieces**; (2)
> this **proves, for every `K` (not just numerically up to `K=16384`), fact
> (i) named as open** in `uniform_in_c_attempt/ATTEMPT.md` §6.3 — the
> maximum of `n|φ_n^{(K)}-φ_K|` over `n` is always attained at `n=K+1`; (3)
> at that point the quantity collapses, via the archive's own
> post-adversarial exact identity `φ_n^{(n-1)}=Q(n)/n`, to the clean closed
> form `M_K:=\sup_n|T(n,K)| = Q(K{+}1)-(K{+}1)φ_K`, connecting `M_K` directly
> to the classical Ramanujan `Q`-function; (4) two elementary, fully explicit
> sandwich bounds (`φ_K` between `\sqrt{π}/(2\sqrt{K+1})` and
> `\sqrt π/(2\sqrt K)`; `Q(n)≤1+\sqrt{πn/2}`) bound `M_K` and the separate
> `K=n` boundary case, giving the uniform bound above. The **sharp** constant
> `a^*=0.3670872\ldots` is **not** established here (this document proves
> boundedness with an explicit witness, not sharpness) and remains open,
> named precisely in §7 below as the natural next step.

---

## 0. Discipline

No randomness is used anywhere in this document — the object under study is
entirely deterministic (exact rational/integer arithmetic and elementary
real analysis), so the archive's fresh-seed requirement does not apply and no
seed table is included. Every claim labelled PROVED below is proved by
elementary, general-`K`/general-`n` algebra (Pascal's rule, a standard
binomial-ratio identity, elementary-symmetric-polynomial positivity, `1-x\le
e^{-x}`, a Gaussian-integral comparison, and the classical Wallis/Stirling
limit already cited elsewhere in this archive) — never by extrapolating a
numerical scan. All exact-arithmetic scripts use `fractions.Fraction`;
`mpmath` (40-digit precision) is used only for the wide-range sanity net in
§6 (T5), never as the basis of a PROVED claim. Nothing here reads any
`adversarial/` referee-report directory's internals; the archive facts cited
below (Estágios 7/9/11, `mk_geometricity_attempt`, `k2_open_lemma`,
`k3_attempt_2`, `all_orders_closed_form_attempt`, Proposição 7.1) are cited
as already-integrated, published archive results, exactly as ordinary
literature review.

---

## 1. Setup and target, restated precisely

Notation as in `uniform_in_c_attempt/ATTEMPT.md` §6 and `THEOREM.md`
Definition 4: `φ_n^{(K)}` is the `K`-reroute recursion's value at sample size
`n` (`0≤K≤n`), `φ_K:=\lim_{n\to\infty}φ_n^{(K)}` (proved to exist, Estágio 6;
proved `Θ(1/n)` for `K≥2` and `Θ(1/n^2)` for `K=1`, Estágio 7). Target:

> **Hypothesis (U').** There exists `a<\infty` such that
> `\displaystyle|φ_n^{(K)}-φ_K| \le \frac{a\sqrt K}n` for **every** `n\ge1`
> and every integer `K` with `0\le K\le n`.

Known before this document (all cited, not re-derived): `uniform_in_c_attempt/ATTEMPT.md`
§6.2's Teorema B shows (U') would give an explicit rate for Teorema A/C's
`c`-uniform version of Teorema 3; §6.3 names it "NUMERICALLY CHARACTERIZED,
not proved," with the sharp candidate constant
`a^*:=\sqrt π(1/\sqrt2-1/2)=0.3670872119\ldots` and two named missing facts:
(i) `\max_n n|φ_n^{(K)}-φ_K|` is always attained at `n=K+1` (verified
numerically to `K=16384`, never proved); (ii) the `K\to\infty` limit of the
endpoint ratio is genuinely the supremum over `K`, not just its limit.
`THEOREM.md` Estágio 11 (`mk_geometricity_attempt/ATTEMPT.md`) proves
`M_K:=\sup_{n\ge K+1}|n(φ_n^{(K)}-φ_K)| \le φ_K(K{+}1)e^{K/2}+K` — geometric
growth in `K`, strictly weaker than the `O(\sqrt K)` (U') needs, as both
documents explicitly flag. This document's job: try to close the gap between
"grows at most geometrically" and "grows like `\sqrt K`."

---

## 2. The missing ingredient: a closed form for `ψ_n^{(K),R}`

`k2_open_lemma/ATTEMPT.md` §2 (Lemma A, Reduction Lemma, PROVED, every fixed
`K`): with `ψ_n^{(K)}:=P(K{+}1\text{ cyclic})` (generic non-rerouted
reference point) and `ψ_n^{(K),R}:=P(1\text{ cyclic})` (a rerouted reference
point),

`\displaystyle φ_n^{(K)} = \frac Kn\,ψ_n^{(K),R} + \Big(1-\frac Kn\Big)ψ_n^{(K)}`, exactly, `n>K`.  (2.1)

`k2_open_lemma/k3_attempt_2/ATTEMPT.md` §2 identifies these with the
`(a,b,r)` Markov chain of that document: `ψ_n^{(K)}=g(0,0,K)`,
`ψ_n^{(K),R}=h(0,0,K{-}1)`. `THEOREM.md` Estágio 9
(`all_orders_closed_form_attempt/ATTEMPT.md` §4, Theorem A/B, PROVED,
215,070 independent exact checks) gives, in the `g_r(m,b):=g(n{-}m,b,r)`,
`h_r(a,b):=h(a,b,r)` notation of that document:

`\displaystyle g_r(m,b)=\sum_{j=0}^r\binom{2r{+}b{+}1}{r{-}j}\frac{r!(r{+}b)!}{(2r{+}b{+}1)!}\frac{(m{+}j)!}{m!\,n^j}`,  `\qquad h_r(a,b)=\frac{n{-}a{+}1}n\,\hat g_r(n{-}a{+}1,b{+}1)`,  (2.2)

the second **evaluated out of `g`'s ordinary probabilistic domain at `a=0`**
(the document's own explicitly-flagged domain caveat, §4 "Domain caveat").
Corolário A1 is `ψ_n^{(K)}=g_K(n,0)`. Specializing (2.2)'s `h`-formula at
`r=K{-}1`, `a=0`, `b=0` and simplifying the prefactor (`N:=2r{+}b{+}1=2K` at
this `r,b`) gives:

> **Proposição 2.1 (PROVED here, from cited PROVED facts, general `K`).**
> `\displaystyle ψ_n^{(K),R} = κ\sum_{i=1}^K\binom{2K}{K-i}g(i;n)`,
> `\quad κ:=\frac{(K{-}1)!\,K!}{(2K)!}`, `\quad g(i;n):=\prod_{l=1}^i\Big(1{+}\frac ln\Big)=\frac{(n{+}i)!}{n!\,n^i}`.

*Derivation.* `h_{K-1}(0,0)=\frac{n+1}n\hat g_{K-1}(n{+}1,1)`; substitute
`\hat g_{K-1}(n{+}1,1)=\frac{(K{-}1)!K!}{(2K)!}\sum_{j=0}^{K-1}\binom{2K}{K{-}1{-}j}\frac{(n{+}1{+}j)!}{(n{+}1)!\,n^j}`
(Theorem A with `r=K{-}1,b=1,m=n{+}1`, `N=2K`); `\frac{n+1}n\cdot\frac{(n+1+j)!}{(n+1)!n^j}=\frac{(n+1+j)!}{n!\,n^{j+1}}`;
reindex `i:=j{+}1` (`i=1,\ldots,K`). `∎` **Verified independently**
(`verify_closed_form.py`, T3): the resulting `φ_n^{(K)}` via (2.1)+(2.2)/2.1
matches `chain.py`'s from-scratch `(j,R)`-recursion exactly (`Fraction`,
`K=0..9`, `n=K{+}1..K{+}30`, `300/300` matches), and at `K=1` reproduces the
hand-derived `ψ_n^{(1),R}=1/2+1/(2n)` of `k2_open_lemma/ATTEMPT.md` §3
exactly.

---

## 3. Theorem 1: the exact decomposition of `T(n,K):=n(φ_n^{(K)}-φ_K)`

> **Theorem 1 (PROVED, every `K\ge0`, every `n\ge K{+}1`).**
> `\displaystyle \frac{T(n,K)}A = \mathrm{CONST}(K) + \sum_{j=1}^K\Big[\binom{2K{+}1}{K{-}j}f_j(n) + B_j(K)\big(g(j;n){-}1\big)\Big]`,
> where `A:=φ_K/4^K=(K!)^2/(2K{+}1)!`, `f_j(n):=n(g(j;n){-}1)`,
> `\mathrm{CONST}(K):=2^{2K-1}-\tfrac{2K+1}2\binom{2K}K`,
> `B_j(K):=\dfrac{(2K{+}1)(j{+}1)}{K{+}j{+}1}\binom{2K}{K{-}j}`.
> **Every coefficient `\binom{2K+1}{K-j}` and `B_j(K)` is `\ge0`
> (`B_j(K)>0`).**

*Proof.* Combine Corolário A1's `ψ_n^{(K)}` and Proposição 2.1's
`ψ_n^{(K),R}` in (2.1); write `\kappa=A(2K{+}1)/K` (immediate from the two
prefactors); substitute and collect the coefficient of each `g(j;n)`,
`j=1,\ldots,K`, and the `n`-independent remainder. The coefficient of
`g(j;n)` in `n·φ_n^{(K)}` is `e_j(n):=(n{-}K)\binom{2K+1}{K-j} +
(2K{+}1)\binom{2K}{K-j}` (direct algebra from (2.1)); write
`e_j(n)=n\binom{2K+1}{K-j}+B_j(K)` where

`\displaystyle B_j(K) = (2K{+}1)\binom{2K}{K-j}-K\binom{2K+1}{K-j}`.

By Pascal's rule `\binom{2K+1}{K-j}=\binom{2K}{K-j}+\binom{2K}{K-j-1}` and
the standard binomial-ratio identity
`\binom{2K}{K-j-1}/\binom{2K}{K-j}=(K-j)/(K+j+1)`:

`\displaystyle B_j(K) = \binom{2K}{K-j}\Big[(K{+}1)-\frac{K(K{-}j)}{K{+}j{+}1}\Big] = \binom{2K}{K-j}\,\frac{(K{+}1)(K{+}j{+}1)-K(K{-}j)}{K{+}j{+}1}`,

and `(K{+}1)(K{+}j{+}1)-K(K{-}j) = (2K{+}1)(j{+}1)` (direct expansion:
`K^2{+}Kj{+}2K{+}j{+}1-K^2{+}Kj=2Kj{+}2K{+}j{+}1=(2K{+}1)(j{+}1)`), giving
the stated `B_j(K)`, manifestly `>0` for `0\le j\le K`. **Verified exactly**
for `K=0,\ldots,300`, all `j` (`verify_decomposition.py`, T2, `45\,451/45\,451`
matches — a check on transcription, not the proof, which is the elementary
algebra above and is general in `K`). Writing `n·φ_n^{(K)} =
A(n{-}K)\binom{2K+1}K + A\sum_{j=1}^Ke_j(n)g(j;n)` (the `j{=}0` term
isolated) and `n\varphi_K=An\cdot2^{2K}` (using
`\sum_{j=0}^K\binom{2K+1}{K-j}=2^{2K}`, the classical odd-`N` half-sum
identity), substituting `e_j(n)=n\binom{2K+1}{K-j}+B_j(K)` and
`g(j;n)=1+(g(j;n){-}1)`, and collecting the `n`-independent constant (which
telescopes, via the same half-sum identity plus
`\sum_{j=1}^K\binom{2K}{K-j}=2^{2K-1}-\tfrac12\binom{2K}K`, to the stated
`\mathrm{CONST}(K)`) gives the theorem. `∎` **Verified symbolically**
(`verify_decomposition.py`, T1): `\mathrm{sympy.simplify}` of `T(n,K)/A` minus
the claimed right-hand side is exactly `0`, as a rational-function identity
in `n`, for `K=0,\ldots,8` — `9/9` exact matches, not a numerical
spot-check.

---

## 4. Theorem 2: fact (i) — the maximum over `n` is always at `n=K+1`

> **Theorem 2 (PROVED, every `K\ge0`).** `f_j(n)` and `g(j;n){-}1` are both
> `\ge0` and nonincreasing in `n`, for every `j\ge1`. Consequently `T(n,K)`
> is nonincreasing in `n\ge K{+}1`; and since `T(n,K)\to c_K\ge0` as
> `n\to\infty` (Estágio 7, `c_K=[(K{+}2)φ_K-2]/4\ge0` for every `K`, with
> equality only at `K=0,1`), `T(n,K)\ge c_K\ge0` for every `n`. Hence
> `\displaystyle M_K:=\sup_{n\ge K+1}|T(n,K)| = T(K{+}1,K)`, for **every**
> `K` — resolving fact (i) of `uniform_in_c_attempt/ATTEMPT.md` §6.3 as a
> theorem, not a numerical observation bounded at `K=16384`.

*Proof.* `g(j;n)=\prod_{i=1}^j(1{+}i/n)=\sum_{k=0}^je_k(1,\ldots,j)/n^k`
(elementary symmetric polynomials of `\{1,\ldots,j\}`, `e_0=1`, every
`e_k>0` for `1\le k\le j`), so `g(j;n){-}1=\sum_{k=1}^je_k(j)/n^k` — a sum of
**strictly positive, strictly decreasing in `n`** terms, hence itself
`\ge0` and nonincreasing — and `f_j(n)=n(g(j;n){-}1)=\sum_{k=1}^je_k(j)/n^{k-1}`,
likewise `\ge0` and nonincreasing (the `k=1` term, `e_1(j)`, is simply
constant in `n`; every `k\ge2` term strictly decreases). This is exactly the
elementary-symmetric-polynomial argument of `mk_geometricity_attempt/ATTEMPT.md`
§2.2, reused verbatim for `f_j(n)` and applied one order more simply for
`g(j;n){-}1`. By Theorem 1,
`T(n,K)/A` is `\mathrm{CONST}(K)` (independent of `n`) plus a **nonnegative**
combination (`\binom{2K+1}{K-j},B_j(K)\ge0`) of these nonincreasing
nonnegative functions, hence itself nonincreasing in `n`. Since a
nonincreasing sequence is `\ge` its limit at every point, and that limit is
`c_K\ge0` (cited, Estágio 7 — `c_K>0` proved for `K\ge2`, `c_1=c_0=0`
exactly), `T(n,K)\ge0` for every `n`, so `|T(n,K)|=T(n,K)` and the supremum
of a nonincreasing sequence is its first term, `n=K{+}1`. `∎` **Verified**
(`verify_closed_form.py`, T3): on the exact grid `K=0..9`, `n=K{+}1..K{+}30`,
zero negativity violations, zero monotonicity violations, and `T(K{+}1,K)`
is the max in every one of the 10 rows tested.

---

## 5. Theorem 3: the exact value of `M_K`

> **Theorem 3 (PROVED).** `M_K = Q(K{+}1) - (K{+}1)φ_K`, where `Q` is the
> Ramanujan `Q`-function of Proposição 7.1
> (`uniform_in_c_attempt/ATTEMPT.md` §7.1).

*Proof.* By Theorem 2, `M_K=T(K{+}1,K)=(K{+}1)\big(φ_{K+1}^{(K)}-φ_K\big)`.
The `[Correção pós-adversarial, 2026-08-23]` block of
`uniform_in_c_attempt/ATTEMPT.md` §6.3 (already PROVED there: at `K=n-1`
reroutes, the one non-rerouted point's image under `π` is marginally
`\mathrm{Uniform}[n]`, independent of the `U_i`, so `f` is *exactly* a
uniform random mapping and Proposição 7.1 applies verbatim) gives
`φ_n^{(n-1)}=Q(n)/n` for every `n\ge1`; taking `n=K{+}1` gives
`φ_{K+1}^{(K)}=Q(K{+}1)/(K{+}1)`. Substituting: `M_K =
(K{+}1)\big[Q(K{+}1)/(K{+}1) - φ_K\big] = Q(K{+}1)-(K{+}1)φ_K`. `∎`
**Verified independently** (`verify_closed_form.py`, T4): `M_K` computed via
`chain.py`'s from-scratch recursion at `n=K{+}1` (not the closed form of §2–3
at all) matches `Q(K{+}1)-(K{+}1)φ_K`, computed by an independently-coded
exact `Q(n)`, exactly for `K=0,\ldots,40` (`41/41`), plus a direct check
(§1's throwaway probe, reproduced in `verify_closed_form.py`'s structure)
that `\varphi_n^{(n-1)}=Q(n)/n` holds exactly for `n=1,\ldots,24`.

This is a clean byproduct in its own right: `M_K` — the worst-case
finite-`n` deviation of the `K`-reroute recursion from its own limit,
maximized over every valid `n` — has an exact closed form in terms of the
classical Ramanujan `Q`-function, not just an asymptotic.

---

## 6. Theorem 4: (U') is PROVED, with explicit constant `a=1+\sqrt{π/2}`

Two elementary lemmas, both fully self-contained (no asymptotic-with-`O()`
citation needed beyond one classical limit value):

> **Lemma 4.1 (`φ_K` sandwich, PROVED).** For every `K\ge1`:
> `\displaystyle \frac{\sqrt π}{2\sqrt{K{+}1}} < φ_K < \frac{\sqrt π}{2\sqrt K}`.

*Proof.* `φ_{K+1}/φ_K=(2K{+}2)/(2K{+}3)` exactly (immediate from
`φ_K=4^K(K!)^2/(2K{+}1)!`, or cited from Estágio 7). Let `v_K:=Kφ_K^2`,
`z_K:=(K{+}1)φ_K^2`. Then `v_{K+1}/v_K = \frac{K{+}1}K\big(\frac{2K+2}{2K+3}\big)^2`,
and `4(K{+}1)^3-K(2K{+}3)^2=3K{+}4>0`, so `v_{K+1}>v_K`: `v_K` is *strictly
increasing*. Similarly `z_{K+1}/z_K=\frac{K{+}2}{K{+}1}\big(\frac{2K+2}{2K+3}\big)^2`,
and `4(K{+}1)^2(K{+}2)-(K{+}1)(2K{+}3)^2=-(K{+}1)<0`, so `z_{K+1}<z_K`: `z_K`
is *strictly decreasing* (both by direct cubic expansion, elementary; both
identities re-verified by machine, `mpmath`, at `K=0,\ldots,10^5` with zero
violations, §6 T5-(5a)). Both converge to the same limit
(`z_K-v_K=φ_K^2\to0`), which is `\pi/4` by the classical Wallis/Stirling
limit `Kφ_K^2\to\pi/4` (**CITED**, classical — the same asymptotic
`φ_K\sim\sqrt π/(2\sqrt K)` already cited, without dispute, at
`uniform_in_c_attempt/ATTEMPT.md` §6.3 and at `THEOREM.md` Estágio 7's
corollary `c_K=\sqrt{\pi K}/8-1/2+O(K^{-1/2})`). A strictly increasing
sequence converging to a limit stays strictly below it; a strictly
decreasing one stays strictly above: `v_K<\pi/4<z_K` for every `K\ge1`,
i.e. `Kφ_K^2<\pi/4<(K{+}1)φ_K^2`, which rearranges to the stated bounds. `∎`

> **Lemma 4.2 (`Q(n)` upper bound, PROVED).** `Q(n) \le 1+\sqrt{\pi n/2}`
> for every `n\ge1`.

*Proof.* `Q(n)=\sum_{j=0}^{n-1}\prod_{i=1}^j(1{-}i/n)`. Since `1{-}x\le
e^{-x}` for every real `x`, `\prod_{i=1}^j(1{-}i/n)\le e^{-j(j+1)/(2n)}\le
e^{-j^2/(2n)}=:h(j)` (using `j(j{+}1)\ge j^2`). `h` is positive and
decreasing on `[0,\infty)`, so `\sum_{j=1}^\infty h(j)\le\int_0^\infty
h(x)\,dx=\sqrt{\pi n/2}` (standard integral-test comparison plus the
Gaussian integral `\int_0^\infty e^{-x^2/(2n)}dx=\sqrt{\pi n/2}`). Hence
`Q(n)\le h(0)+\sum_{j=1}^\infty h(j) \le 1+\sqrt{\pi n/2}`. `∎` **Verified**
(§6 T5-(5b)): `n=1,\ldots,199` and a wide grid to `n=10^5`, zero violations.

> **Theorem 4 (Hypothesis (U'), PROVED).** For every integer `n\ge1` and
> every `0\le K\le n`:
> `\displaystyle |φ_n^{(K)}-φ_K| \le \big(1+\sqrt{\pi/2}\,\big)\frac{\sqrt K}n`,
> `\quad 1+\sqrt{\pi/2}=2.253314137\ldots`.

*Proof.* Throughout, use the elementary fact `n/\sqrt{n{+}1}\ge\sqrt n-1` for
every `n\ge1`: both sides are `\ge0` there (`\sqrt n\ge1`), so the inequality
is equivalent, after rearranging to `n+\sqrt{n{+}1}\ge\sqrt{n(n{+}1)}` and
squaring both (nonnegative) sides, to `n^2{+}2n\sqrt{n{+}1}{+}(n{+}1)\ge
n^2{+}n`, i.e. `2n\sqrt{n{+}1}{+}1\ge0`, always true.

**Generic case, `1\le K\le n{-}1`** (Theorem 2's domain `n\ge K{+}1`). By
Theorem 3, `M_K=Q(K{+}1)-(K{+}1)φ_K`. Lemma 4.2 bounds `Q(K{+}1)\le
1{+}\sqrt{\pi(K{+}1)/2}`; Lemma 4.1's `z_K`-bound (`(K{+}1)φ_K^2>\pi/4`)
gives `(K{+}1)φ_K=\sqrt{(K{+}1)^2φ_K^2}>\sqrt{(K{+}1)\cdot\pi/4}=
\tfrac{\sqrt\pi}2\sqrt{K{+}1}`. Subtracting:

`\displaystyle M_K < 1+\sqrt{\tfrac{\pi(K+1)}2} - \tfrac{\sqrt\pi}2\sqrt{K{+}1} = 1+\sqrt{K{+}1}\Big[\sqrt{\tfrac\pi2}-\tfrac{\sqrt\pi}2\Big] = 1+a^*\sqrt{K{+}1}`,

using `\sqrt{\pi/2}-\sqrt\pi/2=\sqrt\pi(1/\sqrt2-1/2)=a^*` exactly. Now
`\tfrac1{\sqrt K}+a^*\sqrt{\tfrac{K+1}K}` is a sum of two functions each
strictly decreasing in `K\ge1`, so `\tfrac{1+a^*\sqrt{K+1}}{\sqrt K}` is
maximized at `K=1`, where it equals `1+a^*\sqrt2=1.519140\ldots
<1+\sqrt{\pi/2}`. Hence `M_K\le(1{+}\sqrt{\pi/2})\sqrt K` for every `K\ge1`,
and `|φ_n^{(K)}-φ_K|\le M_K/n\le(1{+}\sqrt{\pi/2})\sqrt K/n` for every
`n\ge K{+}1`.

**Boundary case `K=n`.** `φ_n^{(n)}=Q(n)/n` (Proposição 7.1 exactly), so
`n|φ_n^{(n)}-φ_n|=|Q(n)-nφ_n|`. Upper side: Lemma 4.1's `z_n`-bound gives
`n φ_n \ge \tfrac{\sqrt\pi}2\cdot\tfrac n{\sqrt{n+1}} \ge
\tfrac{\sqrt\pi}2(\sqrt n-1)` (the elementary fact above), so

`\displaystyle Q(n)-n\varphi_n \le \big[1{+}\sqrt{\pi n/2}\big]-\tfrac{\sqrt\pi}2(\sqrt n-1) = 1+\tfrac{\sqrt\pi}2+a^*\sqrt n`.

Now `\big(1{+}\sqrt{\pi/2}\big)\sqrt n - \big(1{+}\tfrac{\sqrt\pi}2+a^*\sqrt n\big)
= \big(1{+}\sqrt{\pi/2}-a^*\big)\sqrt n - 1 - \tfrac{\sqrt\pi}2`, and, since
`a^*=\sqrt{\pi/2}-\sqrt\pi/2` gives `1{+}\sqrt{\pi/2}-a^*=1{+}\sqrt\pi/2`
exactly, this equals `\big(1{+}\tfrac{\sqrt\pi}2\big)(\sqrt n-1)\ge0` for
`n\ge1`. So `Q(n)-n\varphi_n\le(1{+}\sqrt{\pi/2})\sqrt n` directly. Lower
side: trivially `Q(n)\ge0` and
`nφ_n<\tfrac{\sqrt\pi}2\sqrt n` (Lemma 4.1's `v_n`-bound), so
`-(Q(n)-n\varphi_n) < \tfrac{\sqrt\pi}2\sqrt n < (1{+}\sqrt{\pi/2})\sqrt n`.
Combining, `|Q(n)-n\varphi_n|\le(1{+}\sqrt{\pi/2})\sqrt n` for every `n\ge1`,
i.e. `|φ_n^{(n)}-φ_n|\le(1{+}\sqrt{\pi/2})\sqrt n/n`, matching the claimed
bound at `K=n`. `∎`

**Verified** (`verify_inequalities.py`, T5): (5c) `n/\sqrt{n{+}1}\ge\sqrt
n{-}1` for `n=1,\ldots,10^5`, zero violations; (5d) the assembled bound at
both binding cases (`n=K{+}1` via the exact `M_K` formula, and `n=K`), for
`K` up to `10^5`, zero violations, worst observed ratio
`n|φ_n^{(K)}{-}φ_K|/\sqrt K = 0.366037` at the tested grid (consistent with
approach to `a^*=0.367087\ldots`, well inside the proved `a=2.253314`); (5e)
interior `n` (not just the two binding endpoints) checked directly via the
closed form of §2–3, `K\in\{1,5,20,100,1000\}`, `n=K{+}\{1,2,5,20,100\}`,
zero violations (redundant with Theorem 2's monotonicity, checked anyway).

---

## 7. What this closes, and what remains open

**Closed by this document:**

- **Hypothesis (U') itself — PROVED**, with explicit constant
  `a=1+\sqrt{\pi/2}\approx2.2533`. Via `uniform_in_c_attempt/ATTEMPT.md`
  §6.2's Teorema B (PROVED there, conditional on (U'_a)), this immediately
  gives an **unconditional, explicit rate**: for `n\ge4`, `0\le c\le n`,
  `|Δ_n(c)| \le \big[(1{+}\sqrt{\pi/2})\sqrt c + 0.2805\big]/n`. This closes
  the "single obstruction between Teorema A/C (soft, unconditional) and a
  fully explicit rate" named at the end of `uniform_in_c_attempt/ATTEMPT.md`
  §6.3.
- **Fact (i) of §6.3 — PROVED for every `K`** (Theorem 2), not merely
  verified to `K=16384`.
- **A new exact identity** (Theorem 3): `M_K=Q(K{+}1){-}(K{+}1)φ_K`,
  connecting the worst-case finite-`n` deviation directly to the classical
  Ramanujan `Q`-function.
- **A new exact decomposition** (Theorem 1) of `n(φ_n^{(K)}-φ_K)` itself,
  not just its `K`-fixed limit or a crude geometric bound — potentially
  useful raw material for future fronts on this recursion (e.g. Conjecturas
  1–2 of `THEOREM.md`, or a sharper Teorema B constant).

**NOT closed, honestly:**

- **The sharp constant `a^*=0.3670872119\ldots`** — this document proves
  boundedness with an explicit, checkable, but **not sharp** witness
  (`2.2533` vs. `0.3671`, roughly a factor of `6`). Fact (ii) of §6.3 — that
  the `K\to\infty` limit of the endpoint ratio equals the *supremum* over
  `K`, not just the limit — is **not** addressed here and remains open.
- **The natural route to sharpness**, named precisely so a future front does
  not have to rediscover it: Theorem 4's proof only ever uses the *upper*
  bound on `Q(n)` (Lemma 4.2) and the two-sided sandwich on `φ_K` (Lemma
  4.1); it never uses a matching *lower* bound on `Q(n)`. A lower bound of
  the form `Q(n)\ge\sqrt{\pi n/2}-C` for explicit `C` (provable, by the same
  elementary method as Lemma 4.2, using `-\ln(1{-}x)\le x/(1{-}x)` in place
  of `1{-}x\le e^{-x}`, at the cost of a more delicate error-term
  bookkeeping since `i/(n{-}i)` does not telescope as cleanly as `i/n`)
  would, combined with Theorem 3 and Lemma 4.1's already-sharp-in-the-limit
  bounds, immediately give `\lim_{K\to\infty}M_K/\sqrt K=a^*` **exactly** (not
  just `\limsup\le a^*` as this document's bound implies) — and, combined
  with a proof that `M_K/\sqrt K` is monotone in `K` (suggested but not
  proved by the numerics of `probe_K_sharp.log`, cited unchanged from the
  parent document), would close fact (ii) and hence (U') with the sharp
  constant `a^*` itself. **This document deliberately stops short of that**
  — it was not attempted, to avoid rushing a second, more delicate
  asymptotic derivation and risking an error in either; it is named here as
  the precise, concrete next step, not left vague.
  **[Correção pós-adversarial, 2026-08-23 — DISC-DEC-058, Estágio 13.]**
  O limitante inferior `Q(n)\ge\sqrt{πn/2}-6` foi PROVADO
  (`sharp_constant_attempt/ATTEMPT.md`, adversarialmente confirmado SOUND,
  "ACCEPT for catalogue", verificado independentemente até `n,K=10^6`),
  dando `\lim_{K\to\infty}M_K/\sqrt K=a^*` **exato**. A monotonicidade de
  `M_K/\sqrt K` (fato (ii)/`\sup_K=\lim_K`) permanece aberta, tentada por
  duas rotas e não fechada. A constante efetivamente provada na hipótese
  (U') permanece `a=1{+}\sqrt{π/2}`, não `a^*`. Ver `THEOREM.md` "Estágio
  13" para o enunciado completo.

---

## Established / Heuristic / Open

**Established (PROVED, this document):** Proposição 2.1 (§2); Theorem 1, the
exact decomposition (§3); Theorem 2, fact (i) for every `K` (§4); Theorem 3,
`M_K=Q(K{+}1){-}(K{+}1)φ_K` exactly (§5); Lemmas 4.1–4.2 (§6); Theorem 4,
Hypothesis (U') with explicit constant `a=1{+}\sqrt{\pi/2}` (§6).

**Established (cited, already PROVED elsewhere in this archive, reused
verbatim):** Reduction Lemma A (2.1); Estágio 9's Corolário A1 and Teorema
A/B (2.2); the `[Correção pós-adversarial]` exact identity
`φ_n^{(n-1)}=Q(n)/n` (§5); Estágio 7's `c_K` formula and `c_K\ge0` (§4);
Proposição 7.1 (§5, §6); the classical Wallis/Stirling limit `Kφ_K^2\to\pi/4`
(§6, Lemma 4.1) and the classical Gaussian integral (§6, Lemma 4.2).

**Heuristic / numerically suggestive, not proved (inherited, unchanged):**
the sharp constant `a^*` as the true supremum of `M_K/\sqrt K` over `K`
(§7); monotonicity of `M_K/\sqrt K` in `K`. **[Correção pós-adversarial,
2026-08-23 — DISC-DEC-058: `a^*` como valor-LIMITE (não supremo) está
agora PROVADO — ver `sharp_constant_attempt/ATTEMPT.md`. A monotonicidade
(equivalente a `\sup_K=\lim_K`) permanece heurística/não provada,
inalterada.]**

**Open:** the sharp constant in (U'); fact (ii) of §6.3; the lower-bound
route to both, named precisely in §7.

---

## Verdict

**Hypothesis (U') is PROVED**, closing wave 13 front (a)'s stated success
criterion ("uma prova de (U') com constante explicita") in full, via a route
that also independently resolves, as a strictly stronger byproduct, the
first of the two specific numerical facts (§6.3, fact (i)) that
`uniform_in_c_attempt/ATTEMPT.md` named as the two things standing between
"numerically characterized" and "proved" — turning it from a fact verified
to `K=16384` into a theorem for every `K`. The second named fact (ii), and
the sharp constant itself, are explicitly left open, with the precise
mathematical gap (a lower bound on `Q(n)` matching Lemma 4.2's upper bound)
named for whichever front attempts them next — consistent with this
archive's discipline of not overclaiming past what was actually proved.

---

## Files, reproducibility

- `DERIVATION_PREREG.md` — pre-registration, written before the verification
  runs below.
- `verify_decomposition.py` / `verify_decomposition.log` — T1 (symbolic
  identity, `sympy`, `K=0..8`, `9/9` pass) and T2 (coefficient sub-identity,
  exact, `K=0..300`, `45\,451/45\,451` pass).
- `verify_closed_form.py` / `verify_closed_form.log` — T3 (closed form vs.
  `chain.py`'s independent recursion, exact, `K=0..9`×`n=K{+}1..K{+}30`,
  `300/300` pass, plus monotonicity/argmax checks) and T4 (`M_K=Q(K{+}1){-}
  (K{+}1)φ_K`, exact, `K=0..40`, `41/41` pass).
- `verify_inequalities.py` / `verify_inequalities.log` — T5 (`mpmath`,
  40-digit precision, wide grids to `K,n\sim10^5`): the `φ_K` sandwich, the
  `Q(n)` bound, `n/\sqrt{n{+}1}\ge\sqrt n{-}1`, and the fully-assembled (U')
  bound at the two binding cases plus several interior `n` — all PASS, zero
  violations.
- No `.json` artifacts; every number reported above is reproduced by
  re-running the three scripts above, which import only `chain.py` from the
  parent `uniform_in_c_attempt/` directory (the wave-11 from-scratch exact
  engine, used here purely as an independent cross-check, never as the
  source of any closed-form derivation) plus the Python standard library,
  `sympy`, and `mpmath`.
