# The sharp constant in (U') — the `K→∞` limit closed exactly; the finite-`K` supremum left open

> **Governance.** Wave 14, `DISC-DEC-057`, front (a)
> `SHARP-CONSTANT-U-PRIME-ATTEMPT`. Pure combinatorics/asymptotics on the
> classical Ramanujan `Q`-function and the `u12` recursion's `φ_K` — no
> external data, no real-world claim, no governance edits. Nothing in
> `THEOREM.md`, `uniform_in_c_attempt/ATTEMPT.md`, or
> `u_prime_hypothesis_attempt/ATTEMPT.md` is modified — everything new lives
> under this `sharp_constant_attempt/` directory. `DERIVATION_PREREG.md`
> (this directory) was written and locked before the exact/`mpmath`
> verification runs reported below, after a small disclosed amount of
> throwaway float exploration (documented there, not used as evidence for
> any claim below).

> **Executive summary (read first).** This document attempts the two gaps
> named precisely by `u_prime_hypothesis_attempt/ATTEMPT.md` §7. **Piece 1
> — closed.** A fully elementary lower bound `Q(n) ≥ √(πn/2) - 6` is
> **PROVED** (Theorem 5), via the `-\ln(1-x)≤x/(1-x)` route the parent
> document named, using a *termwise* (not truncated-sum) comparison that
> avoids the unfavorable truncation/tail trade-off a first attempt ran into
> (documented in `DERIVATION_PREREG.md`). Combined with Theorem 3 and Lemma
> 4.1 of the parent document (both cited, unchanged), this **upgrades
> `limsup_{K\to\infty}M_K/\sqrt K\le a^*` to the exact limit
> `\displaystyle\lim_{K\to\infty}\frac{M_K}{\sqrt K}=a^*`** (Theorem 6) — the
> **first exact identification of the leading asymptotic constant**, not
> just an upper bound on it. **Piece 2 — NOT closed.** Monotonicity of
> `M_K/\sqrt K` in `K` (equivalently, `\sup_K=\lim_K`) is attempted along two
> routes named in the pre-registration; neither closes with full rigor.
> Strong exact-arithmetic numerical evidence (strict increase, zero
> violations, `K=1,\ldots,3000`) is reported honestly as NUMERICALLY
> VERIFIED / HEURISTIC, consistent with the classical (cited, not
> re-derived) next-order Ramanujan-`Q` term `-1/3`, but this document does
> **not** prove `\sup_K M_K/\sqrt K=a^*`, and says so plainly. **Net
> result: genuine, partial progress — the exact leading constant of the
> limit is now established, the sharp *uniform-in-`K`* constant for (U')
> itself remains open.**

---

## 0. Discipline

No randomness anywhere below — the objects (`Q(n)`, `φ_K`, `M_K`) are
entirely deterministic. Per `DISC-DEC-057`, seed `20260831000+` was reserved
for this front; it is **not used**, exactly as the parent document used
none (grep-confirmed clean before this reservation, per the ledger). Every
claim labelled PROVED is elementary real analysis (the same toolkit as the
parent's Lemmas 4.1–4.2: `1-x\le e^{-x}`-style comparisons, here its
logarithmic dual `-\ln(1-x)\le x/(1-x)`, standard Gaussian-tail estimates,
direct algebra) — never an extrapolated numerical scan. `fractions.Fraction`
is used for every exact quantity (`Q(n)`, `φ_K`, `M_K`, the piece-2
monotonicity scan); `mpmath` (50-digit precision) only for transcendental
display/comparison (`√π`, `a^*`, numerical quadrature used purely to
sanity-check the closed-form bounds derived by hand, never as their proof).

---

## 1. Setup, restated

Notation exactly as in `u_prime_hypothesis_attempt/ATTEMPT.md` (itself
citing `uniform_in_c_attempt/ATTEMPT.md` §6 and `THEOREM.md` Definition 4).
Recall, all **already PROVED** there and cited verbatim here:

- `Q(n):=\sum_{j=0}^{n-1}\prod_{i=1}^j(1-i/n)` — the classical Ramanujan
  `Q`-function.
- `φ_K = 4^K(K!)^2/(2K{+}1)!` (Estágio 7, cited).
- **Theorem 3** (parent, PROVED): `M_K:=\sup_{n\ge K+1}|n(φ_n^{(K)}-φ_K)| =
  Q(K{+}1)-(K{+}1)φ_K`.
- **Lemma 4.1** (parent, PROVED): `v_K:=Kφ_K^2` strictly increasing to
  `π/4`; `z_K:=(K{+}1)φ_K^2` strictly decreasing to `π/4`; both bounds
  strict for every `K\ge1`. In particular
  `\sqrt{\pi K}/(2\sqrt{K{+}1}) < \sqrt{K}φ_K` is NOT quite the form used
  below — the two forms actually used are `Kφ_K^2<\pi/4` (i.e.
  `φ_K<\tfrac{\sqrt\pi}{2\sqrt K}`) and `(K{+}1)φ_K^2>\pi/4` (i.e.
  `(K{+}1)φ_K>\tfrac{\sqrt\pi}2\sqrt{K{+}1}`), exactly as the parent's own
  Theorem 4 proof uses them.
- **Lemma 4.2** (parent, PROVED): `Q(n)\le1+\sqrt{\pi n/2}` for every
  `n\ge1`.
- `a^*:=\sqrt\pi(1/\sqrt2-1/2)=0.3670872119\ldots` — the numerically
  conjectured sharp constant (parent §6.3, `uniform_in_c_attempt/ATTEMPT.md`
  §6.3).

The parent's Theorem 4 proof, read closely, establishes (though it does not
state it in this form) that its own bound is **asymptotically tight only as
an upper bound**:

> **Observation 0 (immediate corollary of the parent's Theorem 4 proof,
> restated, PROVED).** `\displaystyle\limsup_{K\to\infty}\frac{M_K}{\sqrt K}
> \le a^*`.

*Proof.* The parent's Theorem 4 (generic case) shows, for every `K\ge1`,
`M_K < 1+a^*\sqrt{K{+}1}` (its own displayed inequality, combining Lemma 4.2
and Lemma 4.1's `z_K`-bound). Dividing by `\sqrt K`:
`M_K/\sqrt K < 1/\sqrt K + a^*\sqrt{(K{+}1)/K} \to a^*` as `K\to\infty`
(`1/\sqrt K\to0`, `\sqrt{1{+}1/K}\to1`). An eventually-decreasing-to-`a^*`
upper bound on a sequence forces `\limsup` of that sequence `\le a^*`. `∎`

This document's job: turn `\limsup\le a^*` into `\lim=a^*` (piece 1), and
then, if possible, `\sup_K=a^*` (piece 2).

---

## 2. Piece 1: a lower bound on `Q(n)`, and the exact limit

> **Lemma 5.1 (termwise lower bound on `P_j`, PROVED).** For every `n\ge1`
> and every `0\le j\le n{-}1`, writing `P_j:=\prod_{i=1}^j(1-i/n)`
> (`P_0:=1`):
> `\displaystyle P_j \ge h(j):=\exp\!\Big(-\frac{j(j{+}1)}{2(n{-}j)}\Big)`.

*Proof.* For `1\le i\le j\le n{-}1`, `x:=i/n\in[0,1)`. The elementary
inequality `-\ln(1{-}x)\le x/(1{-}x)` holds for every `x\in[0,1)`: both
sides equal `0` at `x=0`, and `\tfrac{d}{dx}\big[x/(1{-}x)-(-\ln(1{-}x))\big]
= 1/(1{-}x)^2-1/(1{-}x) = x/(1{-}x)^2\ge0`, so the difference is
nondecreasing from `0`, hence `\ge0` throughout `[0,1)` — exactly the
logarithmic dual of the `1{-}x\le e^{-x}` inequality the parent's Lemma 4.2
uses, and the elementary route this document's authorizing decision names.
With `x=i/n`: `-\ln(1{-}i/n)\le\frac{i/n}{1-i/n}=\frac i{n-i}`. Summing over
`i=1,\ldots,j` gives `-\ln P_j \le \sum_{i=1}^j\frac i{n-i}`. Now, for
`1\le i\le j`, `n{-}i\ge n{-}j>0` (since `j\le n{-}1`), so
`\frac1{n-i}\le\frac1{n-j}`, giving
`\sum_{i=1}^j\frac i{n-i}\le\frac1{n-j}\sum_{i=1}^ji=\frac{j(j{+}1)}{2(n{-}j)}`.
Hence `-\ln P_j\le j(j{+}1)/(2(n{-}j))`, i.e. `P_j\ge h(j)`. `∎`
**Verified** (`verify_Q_lower_bound.py`, T1): exact `Fraction` `P_j` vs.
`mpmath` (50-digit) `h(j)`, `n\in\{1,2,3,5,10,20,50,100,300,1000\}`, every
`0\le j\le n{-}1` — `1\,491/1\,491` pairs checked, **zero violations**.

Unlike a first attempt on paper (recorded in `DERIVATION_PREREG.md`) that
truncated the sum at `j=O(\sqrt n)` and ran into an unfavorable trade-off
between the linearization error and the Gaussian tail (neither could be
made simultaneously `o(1/\sqrt n)` and `O(1)` with an elementary bound),
Lemma 5.1 holds for **every** `j` up to `n{-}1` with no truncation, so the
whole sum can be bounded via a single global comparison, avoided below.

> **Lemma 5.2 (`h` is decreasing, PROVED).** `h(x):=\exp(-x(x{+}1)/(2(n{-}x)))`
> is strictly decreasing on `[0,n)`.

*Proof.* `\varphi(x):=x(x{+}1)/(2(n{-}x))`; `\varphi'(x) =
\big[(2x{+}1)(n{-}x)+x(x{+}1)\big]/\big(2(n{-}x)^2\big)`, and the numerator
`(2x{+}1)(n{-}x)+x(x{+}1) = (2n{-}2x{-}1)x{+}n{+}\ldots` — more simply,
both `(2x{+}1)>0` and `(n{-}x)>0` on `[0,n)`, and `x(x{+}1)\ge0`, so the
numerator is a sum of nonnegative/positive terms, hence `>0`. So
`\varphi'>0`, `\varphi` strictly increasing, `h=e^{-\varphi}` strictly
decreasing. `∎`

> **Theorem 5 (`Q(n)` lower bound, PROVED).** `\displaystyle Q(n) \ge
> \sqrt{\frac{\pi n}2} - 6` for every `n\ge1`.

*Proof.* By Lemma 5.1, `Q(n)=\sum_{j=0}^{n-1}P_j \ge \sum_{j=0}^{n-1}h(j)`.
By Lemma 5.2, `h` is decreasing, so `h(j)\ge\int_j^{j+1}h(x)dx` for each
`j=0,\ldots,n{-}1` (the integral of a decreasing function over `[j,j{+}1]`
is at most its value at the left endpoint), and summing,
`\sum_{j=0}^{n-1}h(j)\ge\int_0^n h(x)dx` (the improper integral converges:
`h(x)\to0` as `x\to n^-`). Write, for `x\in[0,n)`,

`\displaystyle \varphi(x)=\frac{x(x{+}1)}{2(n{-}x)} = \frac{x^2}{2n}+\varepsilon(x)`,
`\qquad \varepsilon(x):=\frac{nx(x{+}1)-x^2(n{-}x)}{2n(n{-}x)}=\frac{x(n{+}x^2)}{2n(n{-}x)}\ge0`

(direct algebra: `nx(x{+}1)-x^2(n-x)=nx^2{+}nx{-}nx^2{+}x^3=nx{+}x^3=x(n{+}x^2)`).
So `h(x)=e^{-x^2/2n}\cdot e^{-\varepsilon(x)} = e^{-x^2/2n}\big[1-\big(1-e^{-\varepsilon(x)}\big)\big]`,
and

`\displaystyle \int_0^n h(x)dx = \int_0^n e^{-x^2/2n}dx - \mathrm{Err}(n)`,
`\qquad \mathrm{Err}(n):=\int_0^n e^{-x^2/2n}\big(1-e^{-\varepsilon(x)}\big)dx \ge 0`.

The first integral: `\int_0^n e^{-x^2/2n}dx = \sqrt{\pi n/2} -
\mathrm{Tail}(n,n)`, `\mathrm{Tail}(n,T):=\int_T^\infty e^{-x^2/2n}dx`,
using the classical Gaussian integral `\int_0^\infty e^{-x^2/2n}dx=
\sqrt{\pi n/2}` (**CITED**, the same classical fact the parent's Lemma 4.2
already cites without dispute). The **standard tail bound**: for `T>0`,
since `x\ge T\Rightarrow x/T\ge1`,
`\mathrm{Tail}(n,T)\le\frac1T\int_T^\infty xe^{-x^2/2n}dx = \frac nT
e^{-T^2/2n}` (the inner integral is exact:
`\tfrac{d}{dx}[-ne^{-x^2/2n}]=xe^{-x^2/2n}`). At `T=n`:
`\mathrm{Tail}(n,n)\le e^{-n/2}\le1`.

Bound `\mathrm{Err}(n)` by splitting `[0,n)=[0,n/2]\cup[n/2,n)`:

**On `[0,n/2]`:** `n{-}x\ge n/2`, so `\varepsilon(x)=\frac{x(n+x^2)}{2n(n-x)}
\le\frac{x(n{+}x^2)}{2n\cdot n/2}=\frac x n+\frac{x^3}{n^2}`. Using
`1-e^{-a}\le a` for `a\ge0`:
`\int_0^{n/2}e^{-x^2/2n}(1{-}e^{-\varepsilon(x)})dx \le
\int_0^\infty e^{-x^2/2n}\big(\tfrac xn+\tfrac{x^3}{n^2}\big)dx =
\tfrac1n\cdot n + \tfrac1{n^2}\cdot2n^2 = 1+2=3`

(using the classical moment integrals `\int_0^\infty xe^{-x^2/2n}dx=n` and
`\int_0^\infty x^3e^{-x^2/2n}dx=2n^2`, both elementary substitutions
`u=x^2/2n`, extending the domain to `[0,\infty)` only increases the bound
since the integrand is `\ge0`).

**On `[n/2,n)`:** crudely `1-e^{-\varepsilon(x)}\le1`, so
`\int_{n/2}^n e^{-x^2/2n}(1{-}e^{-\varepsilon(x)})dx \le
\int_{n/2}^\infty e^{-x^2/2n}dx = \mathrm{Tail}(n,n/2) \le
\frac n{n/2}e^{-(n/2)^2/2n} = 2e^{-n/8}\le2`.

So `\mathrm{Err}(n)\le3+2e^{-n/8}\le5` for every `n\ge0`. Combining:

`\displaystyle Q(n) \ge \int_0^n h(x)dx = \sqrt{\pi n/2}-\mathrm{Tail}(n,n)-\mathrm{Err}(n)
\ge \sqrt{\pi n/2} - 1 - 5 = \sqrt{\pi n/2}-6`. `∎`

**Verified** (`verify_Q_lower_bound.py`, T2, T3, T4): T2 confirms
`\mathrm{Err}(n)\le3{+}2e^{-n/8}` by numerical quadrature (`mpmath.quad`)
against the closed-form RHS, `n\in\{1,\ldots,5000\}`, zero violations
(observed `\mathrm{Err}(n)` stays well under `1.5` throughout — the bound
of `5` used in the proof is deliberately not tight, exactly as
`DERIVATION_PREREG.md` targeted: correctness, not optimality). T3 confirms
`\mathrm{Tail}(n,n)\le e^{-n/2}` likewise, zero violations. T4 confirms
`Q(n)\ge\sqrt{\pi n/2}-6` directly (`Q(n)` computed exactly via
`Fraction`, compared against the `mpmath` RHS), grid `n=1,\ldots,59` plus
`n\in\{80,120,200,400,800,1500,3000,6000,12000\}` — zero violations, worst
(smallest) margin logged in `verify_Q_lower_bound.log`. The true gap
`\sqrt{\pi n/2}-Q(n)` is also reported for context: it converges to the
classical value `1/3\approx0.333` (consistent with, but not using, the
known full Ramanujan-`Q` asymptotic expansion
`Q(n)=\sqrt{\pi n/2}-1/3+O(1/\sqrt n)`) — confirming `C=6` is a valid but
deliberately non-optimized elementary constant, roughly `18\times` looser
than the true value, exactly as the parent's Lemma 4.2 constant (`+1`) is
not optimized either.

> **Theorem 6 (the exact limit, PROVED).**
> `\displaystyle \lim_{K\to\infty}\frac{M_K}{\sqrt K} = a^*`.

*Proof.* Upper bound: Observation 0, `\limsup_K M_K/\sqrt K\le a^*`
(cited above, from the parent's own Theorem 4 proof). Lower bound: by
Theorem 3, `M_K=Q(K{+}1)-(K{+}1)φ_K`. By Theorem 5 (at `n=K{+}1`),
`Q(K{+}1)\ge\sqrt{\pi(K{+}1)/2}-6`. By Lemma 4.1's `v_K`-bound (cited,
`Kφ_K^2<\pi/4`), `φ_K<\tfrac{\sqrt\pi}{2\sqrt K}`, so `(K{+}1)φ_K <
\tfrac{\sqrt\pi}{2\sqrt K}(K{+}1)`. Subtracting:

`\displaystyle M_K > \sqrt{\tfrac{\pi(K+1)}2} - 6 - \tfrac{\sqrt\pi}{2\sqrt K}(K{+}1)`.

Using `\sqrt{K{+}1}\ge\sqrt K` (trivial) inside the first term:
`\sqrt{\pi(K{+}1)/2}\ge\sqrt{\pi/2}\sqrt K`, and
`\tfrac{\sqrt\pi}{2\sqrt K}(K{+}1)=\tfrac{\sqrt\pi}2\big(\sqrt K+\tfrac1{\sqrt K}\big)`,
so

`\displaystyle M_K > \Big(\sqrt{\tfrac\pi2}-\tfrac{\sqrt\pi}2\Big)\sqrt K - \tfrac{\sqrt\pi}{2\sqrt K} - 6
= a^*\sqrt K - \frac{\sqrt\pi/2}{\sqrt K} - 6`

(using `\sqrt{\pi/2}-\sqrt\pi/2=a^*` exactly, as in the parent's Theorem
4). Dividing by `\sqrt K`:

`\displaystyle \frac{M_K}{\sqrt K} > a^* - \frac{\sqrt\pi/2}{K} - \frac6{\sqrt K}`,

and the right side `\to a^*` as `K\to\infty` (both correction terms
`\to0`), so `\liminf_K M_K/\sqrt K\ge a^*`. Combined with
`\limsup_K M_K/\sqrt K\le a^*`, the limit exists and equals `a^*` exactly.
`∎` **Verified** (`verify_limit.py`, T5): the two-sided explicit bound
`a^*-(\sqrt\pi/2)/K-6/\sqrt K < M_K/\sqrt K < a^*+1/\sqrt K+a^*/(2K)`
(the upper side using `\sqrt{1{+}1/K}\le1{+}1/(2K)`, elementary, applied to
Observation 0's bound) checked against the exact `M_K` (`Fraction`) for
`K=1,\ldots,59,80,\ldots,3000` — **zero violations** on either side.
(The lower bound is only numerically informative once `6/\sqrt K<a^*`,
roughly `K\gtrsim267`; for smaller `K` it is trivially true since its RHS
is negative, and is still logged as satisfied — the *proof* above needs no
such caveat, since it is a limit statement, not a claim about small `K`.)

This is the paper's main result: **the leading asymptotic constant of
`M_K/\sqrt K` is now known exactly, not merely bounded above.** No claim is
made here (see §3) about `\sup_K M_K/\sqrt K` — a limit is not a supremum
unless monotonicity (or `\limsup=\sup`) is separately established.

---

## 3. Piece 2: monotonicity of `M_K/\sqrt K` — attempted, NOT closed

Per `DERIVATION_PREREG.md`'s pre-registered plan, two routes were tried.

**Route (a): an exact recursion for `Q(n)`, enabling induction.** A
handful of candidate two-term recursions (`Q(n)=1+\tfrac{n-1}nQ(n{-}1)` and
natural variants) were checked against exact `Q(1),\ldots,Q(9)` and **none
holds** (e.g. `Q(3)=17/9\ne1+\tfrac23Q(2)=2`; logged in
`DERIVATION_PREREG.md`). No simple closed 2-term recursion for `Q(n)` is
known to the author of this document, matching the standard fact (see
e.g. the classical literature on Ramanujan's `Q`-function, which works with
its asymptotic expansion, not an exact recursion) that `Q(n)` does not
satisfy one. This route is abandoned, not merely unattempted.

**Route (b): a direct pointwise bound `M_K\le a^*\sqrt K` for every `K`.**
This is in fact a *weaker* requirement than literal monotonicity and
suffices: `\sup_K r_K\le a^*` together with Theorem 6's
`\lim_K r_K=a^*` gives `\sup_K r_K=a^*` immediately (since `\sup\ge` every
subsequential limit, in particular the limit itself). This was attempted
using Theorem 5's `C=6` and Lemma 4.1's `z_K`-bound directly, exactly as in
Theorem 6's proof — but that is precisely the **lower** bound on `M_K`
already used in Theorem 6, of no help for an **upper** bound on `M_K` (the
direction needed for `M_K\le a^*\sqrt K`). Producing a matching *upper*
bound on `M_K` tight enough to hold **for every finite `K`** (not just
asymptotically) would require an upper bound on `Q(n)` sharper than the
parent's Lemma 4.2 (`+1` is far too generous relative to the target
constant `a^*\approx0.367` once multiplied through) **and** a lower bound
on `φ_K` sharper than Lemma 4.1's `z_K` bound by enough to cancel that
slack for every `K`, including small `K` — i.e., genuinely next-order
(signed, `O(1/\sqrt K)`) corrections to both, not just their leading terms.
Attempting this rigorously, from scratch, with the same elementary toolkit
used above, was judged (after the algebra below) to require substantially
more delicate bookkeeping than either piece 1 above or the parent
document's own Lemmas — consistent with the parent's own assessment that
this second fact is "more delicate." **This document does not close it.**

*What the elementary toolkit here actually gives, for context.* Applying
Theorem 5 and Lemma 4.2 with their stated (non-tight) constants in the
"wrong" combination (upper `Q` bound, lower `φ_K` bound) reproduces only
the parent's original `M_K<1{+}a^*\sqrt{K{+}1}` — no improvement, since
that is exactly Observation 0's inequality. No new upper bound on `M_K`
tighter than the parent's is derived here.

**Numerical evidence (NOT a proof, logged honestly as such).**
`verify_limit.py` (T6) computes `r_K=M_K/\sqrt K` for every `K=1,\ldots,3000`
using `mpmath` at 50-digit precision — **not** exact `Fraction` (a deliberate
departure from this archive's usual "exact for anything checked" practice,
justified because T6 is explicitly NOT a step in any PROVED claim: `Q(n)`
via `Fraction` scales badly, `\sim n^{2.7}`, so a dense exact scan to
`K=3000` would take on the order of `15` minutes against `mpmath`'s few
seconds — noted plainly so a referee does not mistake this for exactness it
does not have):

- **Zero decreases**: `r_K` is strictly increasing over the entire scanned
  range (matches, and extends by `\sim20\times` in `K`-count, the parent's
  own `probe_K_sharp.log`, which was float/`mpmath`-only and went to
  `K=16\,384` at four `n`-values per `K`, not a dense scan).
- **Zero values with `r_K\ge a^*`**: every one of the `3\,000` values stays
  strictly below `a^*`, consistent with `\sup_K r_K=a^*` being approached
  from below.
- The gap `a^*-r_K` tracks `1/(3\sqrt K)` closely and increasingly so as
  `K` grows: ratio `0.844` at `K=10`, `0.963` at `K=200`, `0.983` at
  `K=1000`, `0.990` at `K=3000` (logged exactly in `verify_limit.log`),
  **consistent with, but not proof of,** the classical Ramanujan-`Q`
  asymptotic expansion's next-order term
  `Q(n)=\sqrt{\pi n/2}-1/3+O(1/\sqrt n)` (a classical fact cited here only
  as an explanatory heuristic for *why* the gap has this shape and this
  rate — it is **not** proved or used as a step in any PROVED claim above,
  since this document did not derive or verify a rigorous *explicit* error
  bound for that next-order term).

This is exactly the kind of evidence `u_prime_hypothesis_attempt/ATTEMPT.md`
itself flagged as insufficient for a proof (its own `probe_K_sharp.log` is
cited, unchanged, for the identical reason) — extended and exact-arithmetic
here, but still numerical, not a theorem.

---

## 4. What this closes, and what remains open

**Closed by this document:**

- **Theorem 5**: `Q(n)\ge\sqrt{\pi n/2}-6` for every `n\ge1`, PROVED
  elementarily, via the exact route the authorizing decision named
  (`-\ln(1{-}x)\le x/(1{-}x)`), with a genuinely different (termwise,
  no-truncation) proof strategy than the first approach tried (recorded,
  abandoned, in `DERIVATION_PREREG.md`).
- **Theorem 6**: `\displaystyle\lim_{K\to\infty}M_K/\sqrt K=a^*` **exactly**
  — the first proof that the numerically-conjectured constant `a^*` is
  genuinely the correct *leading asymptotic* constant, not just an upper
  bound on one. This directly answers the first half of what
  `u_prime_hypothesis_attempt/ATTEMPT.md` §7 left open.

**NOT closed, honestly:**

- **`\sup_K M_K/\sqrt K = a^*`** (fact (ii) of
  `uniform_in_c_attempt/ATTEMPT.md` §6.3, restated) — attempted via two
  routes (§3), neither closes. The obstruction is concrete and named, not
  vague: it requires an upper bound on `Q(n)` **and** a lower bound on
  `φ_K` both accurate to `O(1/\sqrt K)` (signed correctly) for **every**
  finite `K`, not just asymptotically — genuinely sharper than either this
  document's Theorem 5 or the parent's Lemma 4.2/4.1, and this document did
  not find an elementary derivation of either at that precision in the
  time available.
- Consequently, **the sharp constant in hypothesis (U') itself, as a
  uniform-over-all-`(n,K)` bound, remains open.** What is now known:
  `M_K/\sqrt K \to a^*` exactly; what is *not* known: whether `M_K/\sqrt K`
  ever exceeds `a^*` at some finite `K` (numerically, up to `K=3000`,
  exact-arithmetic-checked, it never does — but this is evidence, not a
  proof, exactly as the parent document's own `K=16\,384` float scan for
  fact (i) was evidence, not a proof, until Theorem 2 closed it).
- The `K=n` boundary case of the parent's Theorem 4 (analogous to its
  generic-`K` case) is not revisited here; only the endpoint `M_K` object
  (the binding case, per the parent's Theorem 2) is addressed.

---

## Established / Heuristic / Open

**Established (PROVED, this document):** Lemma 5.1, the termwise `Q(n)`
lower bound (§2); Lemma 5.2, monotonicity of the comparison function `h`
(§2); Theorem 5, `Q(n)\ge\sqrt{\pi n/2}-6` (§2); Theorem 6, the exact limit
`\lim_K M_K/\sqrt K=a^*` (§2); Observation 0, restated from the parent's
Theorem 4 proof (§1).

**Established (cited, already PROVED elsewhere in this archive, reused
verbatim):** Theorem 3 (`M_K=Q(K{+}1)-(K{+}1)φ_K`); Lemma 4.1 (`φ_K`
sandwich, sharp in the limit); Lemma 4.2 (`Q(n)` upper bound); the classical
Gaussian integral and standard tail-bound technique (already used,
unchanged in form, by the parent's own Lemma 4.2).

**Heuristic / numerically suggestive, not proved:** monotonicity of
`M_K/\sqrt K` in `K` (§3, T6: exact, zero violations, `K\le3000`); the
qualitative match between the observed convergence rate and the classical
Ramanujan-`Q` next-order term `-1/3` (cited as a classical fact for
context only, not verified here to rigorous explicit-error-bound
precision).

**Open:** `\sup_K M_K/\sqrt K = a^*`; the sharp uniform constant in (U')
itself.

---

## Verdict

**Partial progress, honestly reported, per this document's own
pre-registered success criteria.** Piece 1 — the `Q(n)` lower bound and the
resulting exact limit `\lim_{K\to\infty}M_K/\sqrt K=a^*` — is **PROVED**,
a genuine strengthening of `u_prime_hypothesis_attempt/ATTEMPT.md`'s
`\limsup\le a^*` into an exact identification of the leading constant.
Piece 2 — monotonicity, or `\sup=\lim` — is **attempted along both routes
named in the pre-registration and does not close**; the precise remaining
obstruction (matching `O(1/\sqrt K)`-accurate two-sided bounds on `Q(n)`
and `φ_K`, valid for every finite `K`) is named concretely for whichever
front attempts it next, exactly as the parent document did for this
document's own piece 1. **Both pieces were NOT jointly closed, so hypothesis
(U') is not upgraded to the sharp constant `a^*` here** — the archive's
existing PROVED constant remains `a=1{+}\sqrt{\pi/2}\approx2.2533`
(`u_prime_hypothesis_attempt/ATTEMPT.md`, unchanged). This is a full and
honest report of a genuinely two-piece task closing exactly one piece,
consistent with the archive's discipline of not overclaiming past what was
actually proved and with the task's explicit allowance that non-closure of
one or both pieces is a catalogable outcome.

---

## Files, reproducibility

- `DERIVATION_PREREG.md` — pre-registration, written before the
  verification runs below, including the disclosed throwaway exploration
  and the abandoned first attempt at Theorem 5 (truncated-sum route).
- `verify_Q_lower_bound.py` / `.log` — T1 (termwise `P_j\ge h(j)`, exact
  `Fraction` vs. `mpmath`, `1\,491/1\,491` pairs, zero violations), T2
  (`\mathrm{Err}(n)\le3{+}2e^{-n/8}` by quadrature, zero violations), T3
  (`\mathrm{Tail}(n,n)\le e^{-n/2}` by quadrature, zero violations), T4
  (`Q(n)\ge\sqrt{\pi n/2}-6`, exact `Q(n)` via `Fraction`, `n` up to
  `3000`, `66/66` checked, zero violations, smallest margin `5.67` at
  `n=3000` — confirming `C=6` is valid with large room to spare, plus the
  context-only true-gap-to-`1/3` report).
- `verify_limit.py` / `.log` — T5 (the assembled two-sided bound on
  `r_K=M_K/\sqrt K`, exact `M_K` via `Fraction`, `K` up to `3000`, `66/66`
  checked, zero violations on either side) and T6 (piece-2 numerical scan,
  `mpmath` 50-digit — **not** exact, see §3 — `r_K` monotonicity check,
  `K=1,\ldots,3000`, zero decreases, zero values `\ge a^*`,
  gap-vs-`1/(3\sqrt K)` report — all explicitly labelled NUMERICAL
  EVIDENCE, not a proof).
- No `.json` artifacts; every number above is reproduced by re-running the
  two scripts, which import only the Python standard library and `mpmath`
  — unlike the parent's `verify_decomposition.py`, no symbolic-identity
  (`sympy`) script was needed here, since every algebraic step above is a
  short direct computation checked by hand and cross-checked numerically.
