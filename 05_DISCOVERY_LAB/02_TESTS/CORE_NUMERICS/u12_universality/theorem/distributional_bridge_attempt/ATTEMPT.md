# The distributional bridge `M_n(c) →_d M(c)` — a bounded attempt

**Front:** wave 18, front (d), `DISTRIBUTIONAL-BRIDGE-ATTEMPT`, authorized
by `DISC-DEC-078` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`).
Pure combinatorial mathematics about the u12 random-permutation-with-
reroutes ensemble defined in `THEOREM.md` Definitions 1–4. **This is not
a Millennium Problem and no claim of that kind is made anywhere below.**

See `PREREG.md` (same directory) for the plan committed to before the
main proof work below.

---

## Executive summary

`THEOREM.md`'s Teorema 3 (mean convergence `φ(n,c)→φ_∞(c)`, unconditional
since Estágio 6, sharp rate uniform-in-`c` since Estágio 22) and its
general-`K` Conjectures 1–2 (now PROVED for the continuum object `L(c)`,
Estágio 24) leave one question explicitly untouched, and named as such
(`THEOREM.md` §8, Estágio 24's closing paragraph): does the actual
finite-`n` random variable `M_n(c) := \#\{\text{cyclic points}\}/n`
converge **in distribution** to `M(c)\overset d=\min(1,\sqrt{E/c})`, not
just in mean? No prior front attacked this directly. This one does.

**What closed (PROVED, unconditional).**

1. An exact, finite-`n` distributional mixture identity (Proposition
   D0) upgrading `THEOREM.md` Fact 4.1 from expectations to full CDFs.
2. **Lemma R**, a full re-derivation of `THEOREM.md` Proposition 3's
   mixing-convergence argument (Scheffé + a from-scratch Chernoff tail
   bound) at the level of CDFs rather than means: *if* `F_n^{(K)}(x) →
   F_K(x)` for every fixed integer `K\ge0` and every `x\in(0,1)`, *then*
   `M_n(c)\to_d M(c)`. This reduces the Target statement, rigorously and
   unconditionally, to the single remaining hypothesis of fixed-`K`
   distributional convergence — the exact one-level-up analogue of how
   `THEOREM.md` reduced the mean bridge to its own fixed-`K` Open Lemma
   between Estágio 2 and Estágio 6.
3. **`K=0`**: exact identity `M_n^{(0)}\equiv1` for every `n` — the
   fixed-`K` bridge here never needed proving.
4. **`K=1`** (Proposition D1, the front's central positive result): the
   **exact finite-`n` CDF** of `M_n^{(1)}`, in closed form —
   `P(M_n^{(1)}\le k/n) = k(k+1)/n^2` for `k=0,\dots,n-1` — derived by
   extending `THEOREM.md` Proposition 4's own case-split (already
   proved there for the *mean*) to the *whole* conditional law, with no
   new probabilistic input. Corollaries: `F_n^{(1)}(x)\to x^2=F_1(x)`
   with an explicit **uniform** rate `O(1/n)` (Corollary D1.1); the
   exact second moment `E[(M_n^{(1)})^2] = \tfrac12+\tfrac1{2n^2} \to
   \tfrac12 = E[M_1^2]` at rate exactly `O(1/n^2)` (Corollary D1.2),
   the *first* second-moment (fluctuation) result of any kind proved
   anywhere in this line — `THEOREM.md` §9 item 10 flags "any second-
   moment / fluctuation result" as entirely untouched; this front
   closes it at `K=1`.
5. **Lemma P2** (general `K`, PROVED): an exact exchangeability
   identity reducing `E[(M_n^{(K)})^2]`'s convergence to that of a
   single **generic-pair** quantity `P_{nn}(n,K):=P(\text{two specific
   non-rerouted points both cyclic})`, with the "at least one of the
   pair is itself rerouted" correction terms proved `O(K/n)\to0` — the
   exact 2-point analogue of `THEOREM.md` Estágio 3's Reduction Lemma A
   for the mean.

**What did NOT close (honest, pre-declared acceptable).** The fixed-`K`
distributional bridge for `K\ge2` — i.e. `F_n^{(K)}(x)\to F_K(x)` — is
**OPEN**, and, more specifically, even the *narrower*, second-moment-only
question `P_{nn}(n,K)\to1/(K+1)` (needed by Lemma P2) is open for
`K\ge2`. Diagnosis, precisely: the entire existing `K\ge2` machinery in
`THEOREM.md` (Estágios 3–7, `ψ_n^{(K)}`) is a **single-point marginal**
device by construction — it computes `P(x_0\text{ cyclic})`, which
recovers the mean by exchangeability but carries zero information about
any two-point joint quantity. The genuinely new combinatorics needed
(either a full whole-space `K=2` case analysis in the style of
Proposition D1, or a joint two-point exploration) is exactly what
`THEOREM.md`'s own joint-two-point front (Estágio 18/25) already
diagnosed as the hard residual obstruction in this whole research line
— for a related but *different* quantity (the continuum `E[M_K^2]`,
now closed by an unrelated route, Estágio 24) — and this front finds
the analogous finite-`n\to\infty` quantity equally unresolved. This is
reported as open, not solved by implication.

**Numerical exploration (never a substitute for the above).** Exact
enumeration (`K=1,2,3`, `n` up to `8`–`9`) and Monte Carlo (`n` up to
`2000`, reserved seeds `20260876000`–`20260877000`) both show
`P_{nn}(n,K)` and the full empirical CDF discrepancy `D(n,K):=
\sup_x|F_n^{(K)}(x)-F_K(x)|` trending toward the conjectured limits
(`1/(K+1)` and `0` respectively) for `K=2,3`, monotonically over the
whole exact-enumeration range — genuine supporting evidence, explicitly
not a proof, for the general-`K` case left open above.

**Verdict, honestly.** The Target statement `M_n(c)\to_d M(c)` is
reduced, unconditionally, to a single precisely-named hypothesis (Lemma
R + fixed-`K` bridge for every `K`); that hypothesis is fully closed at
`K=0,1` with new exact closed forms and rates, and reduced further (via
Lemma P2) at general `K` to a single scalar quantity `P_{nn}(n,K)`, not
itself resolved. No claim of a complete proof of the Target statement is
made. Nothing in `THEOREM.md` is edited, weakened, or contradicted.

---

## 1. The precise target

Fix `c\ge0`. Under `THEOREM.md` Definition 1, let

`M_n(c) := \#\{i : i \text{ cyclic for } f\} / n`

be the **random variable** whose expectation `φ(n,c):=E[M_n(c)]` is the
object Teorema 3 already controls. Write `F_n(x):=P(M_n(c)\le x)`. The
continuum target is `M(c)\overset d=\min(1,\sqrt{E/c})`, `E\sim
\mathrm{Exp}(1)`, with `F(x):=P(M(c)\le x) = 1-e^{-cx^2}` for
`x\in[0,1)` and an atom `P(M(c)=1)=e^{-c}`.

> **Target statement.** For every fixed `c\ge0`, `M_n(c)\to_d M(c)` as
> `n\to\infty`.

**Reduction to CDF convergence (elementary, PROVED, standard Portmanteau
argument — CITED for the theorem itself, applied here).** Both `M_n(c)`
and `M(c)` are supported in `[0,1]`, so `F_n(x)=F(x)=1` for every `x\ge1`
and `F_n(x)=F(x)=0` for `x<0`, trivially, for every `n` — this range
needs no argument at all. `F` is continuous on `(-\infty,1)` (smooth on
`(0,1)`, constant `0` below); its only discontinuity is the jump *at*
`x=1` itself, from `1-e^{-c}` to `1` (size `e^{-c}>0`, present for every
fixed `c\ge0`, including the degenerate `K=0`-only case `c=0`, where the
"jump" is the entire mass). By the classical Portmanteau theorem (weak
convergence of laws on `\mathbb R` `\iff` convergence of CDFs at every
continuity point of the limit — e.g. Billingsley, *Convergence of
Probability Measures*, 2nd ed., Wiley 1999, Thm 2.1; CITED, standard,
not re-derived), only continuity points of `F` need checking — i.e.
every real `x\ne1` — and of these only `x\in[0,1)` carries any content,
since `x<0` and `x\ge1` are already trivial by the previous sentence.
So the Target statement holds **iff** `F_n(x)\to F(x)` for every
`x\in[0,1)`.

This is the reduction attacked below.

---

## 2. Exact mixture identities, both sides

### 2.1 Finite-`n` side (Proposition D0, PROVED)

For `0\le K\le n`, let `M_n^{(K)}` be the cyclic-fraction random
variable under `THEOREM.md` Definition 4 (`K` reroutes fixed WLOG at a
specific `K`-subset of `[n]`, well-defined independent of which subset
by the exchangeability argument Definition 4 itself gives — this is
already used, for the mean only, throughout `THEOREM.md` §7). Write
`F_n^{(K)}(x):=P(M_n^{(K)}\le x)`.

> **Proposition D0.** For every `n`, `c\ge0`, `x\in\mathbb R`:
>
> `F_n(x) = \displaystyle\sum_{K=0}^n P(\mathrm{Bin}(n,c/n)=K)\, F_n^{(K)}(x)`.

*Proof.* Total probability over `K_n:=\#\{i:\xi_i=1\}`:
`F_n(x)=\sum_K P(K_n=K)\,P(M_n(c)\le x\mid K_n=K)`. Fix `K`. Conditional
on `\{K_n=K\}`, Definition 1's `\pi` remains a uniform random permutation
of `[n]`, independent of `\{K_n=K\}` (since `\pi\perp\xi`); the set of
rerouted indices, conditional on `K_n=K`, is a uniform random `K`-subset
of `[n]` (a standard fact about i.i.d. Bernoulli's conditioned on their
count — the same fact `THEOREM.md` Definition 4 invokes for the mean);
and the reroute targets `\{U_i\}_{i\in R}` remain i.i.d. `\mathrm{Unif}([n])`,
independent of `\pi` and of `R`. This is **exactly** Definition 4's model
(which fixes a specific `K`-subset WLOG, by the same exchangeability
argument). Hence, as *random variables*, `M_n(c)` conditional on
`\{K_n=K\}` has the same law as `M_n^{(K)}` — not merely the same mean —
so `P(M_n(c)\le x\mid K_n=K) = F_n^{(K)}(x)`. `\square`

This is a straightforward but genuinely new upgrade of Fact 4.1 (which
only ever tracked expectations) to full conditional laws; no new
probabilistic content beyond what Definition 4 already licenses.

### 2.2 Continuum side (CITED from Estágio 24, restated)

`THEOREM.md` Estágio 24 already proves, as a corollary of the general-`K`
Conjecture 1 (now a theorem, modulo the single `PD(1)` size-biasing
citation used throughout that line) plus the Kingman conditioning fact
already cited in §5.1:

`F(x) = P(M(c)\le x) = \sum_{K\ge0} e^{-c}\dfrac{c^K}{K!}\,F_K(x)`,
`F_K(x) := 1-(1-x^2)^K` for `x\in[0,1)` (`F_K(x)=1` for `x\ge1`).

Not re-derived here — imported verbatim, at the same modulo-citation
tier `THEOREM.md` itself carries it at.

---

## 3. Lemma R: the reduction (PROVED, unconditional)

> **Lemma R.** Fix `c\ge0` and `x\in[0,1)`. If `F_n^{(K)}(x) \to F_K(x)`
> as `n\to\infty`, for **every** fixed integer `K\ge0`, then
> `F_n(x) \to F(x)`.

*Proof.* This is `THEOREM.md` Proposition 3's proof (§7.2), re-executed
with `F_n^{(K)}(x)` in place of `\varphi_n^{(K)}` and `F_K(x)` in place
of `\varphi_K` throughout — every step used only that the summands lie
in `[0,1]`, which holds for CDFs exactly as it held for the means; the
proof is given here in full rather than merely asserted to transplant,
since it is the actual deliverable of this section.

Write `p:=c/n`, `\mathrm{Bin}:=\mathrm{Binomial}(n,p)`,
`\mathrm{Poi}:=\mathrm{Poisson}(c)`. By Proposition D0 (§2.1) and the
continuum mixture identity (§2.2),

`F_n(x)-F(x) = \underbrace{\sum_K P(\mathrm{Bin}=K)\big(F_n^{(K)}(x)-F_K(x)\big)}_{=:A_n(x)} + \underbrace{\sum_K\big(P(\mathrm{Bin}=K)-P(\mathrm{Poi}=K)\big)F_K(x)}_{=:B_n(x)}`,

using `0\le F_K(x)\le1` (a CDF) to insert and subtract the cross term,
exactly as Proposition 3's proof does for `\varphi_K\in[0,1]`.

**Bounding `B_n(x)`.** `|B_n(x)| \le \sum_K|P(\mathrm{Bin}=K)-P(\mathrm{Poi}=K)|\cdot1
= 2\,d_{TV}(\mathrm{Bin},\mathrm{Poi})`, which `\to0` by the *same*
elementary pointwise-in-`K` Poisson-limit computation plus Scheffé's
lemma that Proposition 3's proof establishes (§7.2, unchanged — this
step does not reference `x` at all, so it is imported without
modification, not merely re-typed).

**Bounding `A_n(x)`.** Fix `\varepsilon>0`. Choose `M` with
`P(\mathrm{Poi}>M)<\varepsilon/4` and, using the *same* from-scratch
Chernoff bound `P(\mathrm{Bin}(n,c/n)\ge M)\le \delta(c,M):=
e^{-c}(ec/M)^M` (Proposition 3's (7.3), uniform in `n`, depending only
on `c,M`), enlarge `M` so also `\delta(c,M)<\varepsilon/4`. Then, for
**every** `n`, splitting `A_n(x)` at `K=M`:

`|A_n(x)| \le \underbrace{\Big|\sum_{K\le M}P(\mathrm{Bin}=K)\big(F_n^{(K)}(x)-F_K(x)\big)\Big|}_{\text{finite sum}} + \underbrace{P(\mathrm{Bin}>M)}_{\le\,\delta(c,M)<\varepsilon/4}\cdot 1`

(using `|F_n^{(K)}(x)-F_K(x)|\le1` for the tail, exactly as `|\varphi_n^{(K)}-\varphi_K|\le1`
was used). By the Lemma's hypothesis, `F_n^{(K)}(x)\to F_K(x)` for each
of the finitely many `K\in\{0,\dots,M\}` (note: `M` was fixed, depending
on `\varepsilon` and `c` only, *before* invoking the hypothesis, exactly
as in Proposition 3), so the finite sum `\to0` as `n\to\infty`; hence it
is `<\varepsilon/4` for `n` large. For such `n`, `|A_n(x)|<\varepsilon/2`.

Combining, `|F_n(x)-F(x)|\le|A_n(x)|+|B_n(x)|<\varepsilon` for `n` large
enough. `\varepsilon>0` arbitrary, so `F_n(x)\to F(x)`. `\blacksquare`

**What this does and does not establish.** Exactly as `THEOREM.md`
Proposition 3 did for the mean: an unconditional, self-contained proof
of *one* implication (fixed-`K` CDF convergence, for every `K`
`\Rightarrow` the Target statement, at the given `x`). It uses no
unproved input beyond the same two named classical facts already
accepted throughout `THEOREM.md` (Scheffé's lemma; the elementary
Poisson-limit computation), reused verbatim. Combined with the
Portmanteau reduction (§1), applying Lemma R at every `x\in[0,1)` gives:

> **Corollary R.1.** If `F_n^{(K)}(x)\to F_K(x)` for every fixed integer
> `K\ge0` and every `x\in[0,1)`, then `M_n(c)\to_d M(c)`, for every fixed
> `c\ge0`.

This is the exact structural analogue, one level up, of how
`THEOREM.md` related Proposition 3 to Proposição Condicional 5 before
Estágio 6 closed the mean bridge unconditionally. What remains is
exactly: does `F_n^{(K)}(x)\to F_K(x)` for every `K`? §§4–6 attack this
case by case, mirroring `THEOREM.md` §7.3–§7.4's own strategy for the
mean bridge (`K=0,1` first, general `K` last).

---

## 4. `K=0`: the fixed-`K` bridge never needed proving (PROVED, exact)

With `K=0`, `f=\pi`, a permutation; every point of a permutation lies on
a cycle (elementary structure theory of bijections of a finite set,
already used at `THEOREM.md` (7.4)). So `M_n^{(0)}\equiv1` **exactly**,
for every `n\ge1`: `F_n^{(0)}(x) = \mathbf 1\{x\ge1\}`. On the continuum
side, `M_0\equiv1` a.s. too (Lemma 2's `K=0` case, `\varphi_0=1`, and no
reroutes to disturb any cycle), so `F_0(x)=\mathbf1\{x\ge1\}` identically.
`F_n^{(0)}=F_0` **exactly**, for every `n` — not merely a limit.

---

## 5. `K=1`: the exact finite-`n` CDF (PROVED — the front's central result)

### 5.1 Setup (recap of `THEOREM.md` Proposition 4's proof, unchanged)

Fix the rerouted index at `i^*:=1` WLOG (Definition 4's exchangeability).
`\pi` is an unconditioned uniform random permutation of `[n]`, `U:=U_1
\sim\mathrm{Unif}([n])` independent of `\pi`. Let `C` be the `\pi`-cycle
containing `1`, of length `L`. `THEOREM.md` §7.3 Step 1 proves (exactly,
for every `n`, not asymptotically): **`L\sim\mathrm{Unif}\{1,\dots,n\}`**.
Step 2 proves: every point outside `C` is cyclic under `f`, regardless of
`U` — contributing `n-L` cyclic points unconditionally. Step 3 gives the
exact case split, for `T:=\#\{\text{cyclic points of }f\}` (so
`M_n^{(1)}=T/n`), on where `U` lands, labeling `C`'s points
`c_0=1,c_1=\pi(1),\dots,c_{L-1}`:

- `U\notin C` (prob. `(n-L)/n` given `L`): `T = n-L`.
- `U=c_0` (prob. `1/n`): `T = n-L+1`.
- `U=c_d`, `d=1,\dots,L-1` (prob. `1/n` each): `T = n-d+1`.

`THEOREM.md` stops here and averages to get `E[T\mid L=\ell]`
(Proposition 4's Step 4), proving only the mean. Nothing below
introduces new probabilistic machinery — it is the *same* case split,
carried through to the full conditional **law** of `T`, not just its
mean.

### 5.2 The exact conditional CDF of `T` given `L=\ell`

> **Lemma D1.0.** For every `1\le\ell\le n` and every integer
> `0\le k\le n`: `P(T\le k \mid L=\ell) = \dfrac kn\cdot\mathbf1\{k\ge n-\ell\}`.

*Proof.* From §5.1's case split, given `L=\ell`, `T`'s conditional law
puts mass `(n-\ell)/n` on `T=n-\ell`, mass `1/n` on `T=n-\ell+1`
(`U=c_0`), and mass `1/n` on each of `T=n-d+1` for `d=1,\dots,\ell-1`
(`U=c_d`) — as `d` ranges over `1,\dots,\ell-1`, `n-d+1` ranges over the
`\ell-1` distinct integers `n-\ell+2,\dots,n`. So `T`'s support given
`L=\ell` is exactly `\{n-\ell,n-\ell+1,\dots,n\}`, with mass `(n-\ell)/n`
at the left endpoint and `1/n` at each of the remaining `\ell` points.

- If `k<n-\ell`: no mass is `\le k`, so `P(T\le k\mid\ell)=0`, matching
  `(k/n)\cdot0`.
- If `k=n-\ell`: `P(T\le k\mid\ell) = (n-\ell)/n = k/n`. ✓.
- If `k=n-\ell+1`: add the mass `1/n` at `T=n-\ell+1`:
  `(n-\ell+1)/n=k/n`. ✓.
- If `n-\ell+2\le k\le n`: add, for each integer value
  `v=n-\ell+2,\dots,k`, one more mass `1/n` (there are `k-(n-\ell+2)+1
  =k-n+\ell-1` such values): total `(n-\ell+1)/n + (k-n+\ell-1)/n =
  k/n`. ✓ (and at `k=n` this gives `n/n=1`, correct trivially).

So `P(T\le k\mid L=\ell)=k/n` for every `k\ge n-\ell`, and `0` otherwise
— the single formula claimed. `\square`

### 5.3 The exact unconditional CDF

> **Proposition D1 (`K=1` exact finite-`n` CDF, PROVED).** For every
> `n\ge1` and every integer `0\le k\le n-1`:
>
> `\displaystyle P(M_n^{(1)} \le k/n) = \frac{k(k+1)}{n^2}`
>
> (and `P(M_n^{(1)}\le x)=1` for `x\ge1`, trivially).

*Proof.* Averaging Lemma D1.0 over `L\sim\mathrm{Unif}\{1,\dots,n\}`:

`P(T\le k) = \dfrac1n\displaystyle\sum_{\ell=1}^n \dfrac kn\,\mathbf1\{\ell\ge n-k\}
= \dfrac k{n^2}\cdot\#\{\ell\in\{1,\dots,n\}:\ell\ge n-k\}`.

For `0\le k\le n-1`: `n-k\ge1`, and `\#\{\ell\in\{1,\dots,n\}:\ell\ge n-k\}
= n-(n-k)+1 = k+1`. So `P(T\le k)=k(k+1)/n^2`. (At `k=n`: `n-k=0`, every
`\ell\ge1>0` qualifies, count `=n`, giving `P(T\le n)=(n/n^2)\cdot n=1`,
consistent trivially.) `\blacksquare`

### 5.4 Consequences

> **Corollary D1.1 (`K=1` distributional convergence, with an explicit
> uniform rate; PROVED).** For every `x\in[0,1]` and every `n\ge1`,
>
> `\big|F_n^{(1)}(x) - x^2\big| \;\le\; \dfrac{5}{4n}`.
>
> In particular `F_n^{(1)}(x)\to x^2 = F_1(x)` (matching `f_{M_1}(x)=2x`,
> `THEOREM.md` §5.3, PROVED there), **uniformly** in `x\in[0,1]`.

*Proof.* Fix `x\in[0,1)`, `k:=\lfloor xn\rfloor\in\{0,\dots,n-1\}`,
`\theta:=xn-k\in[0,1)`. By Proposition D1,

`F_n^{(1)}(x) = \dfrac{k(k+1)}{n^2} = \dfrac{(xn-\theta)(xn-\theta+1)}{n^2}
= x^2 - \dfrac{(2\theta-1)x}{n} - \dfrac{\theta(1-\theta)}{n^2}`

(direct expansion of `(xn-\theta)(xn-\theta+1)=x^2n^2-2\theta xn+\theta^2+xn-\theta`,
divided by `n^2`). Since `x\le1`, `|2\theta-1|\le1`, and
`\theta(1-\theta)\le1/4` on `[0,1)`:

`\big|F_n^{(1)}(x)-x^2\big| \le \dfrac1n + \dfrac1{4n^2} \le \dfrac1n+\dfrac1{4n} = \dfrac5{4n}`

(using `1/(4n^2)\le1/(4n)` for `n\ge1`). At `x=1`, both sides equal `1`
trivially (`\le5/(4n)` holds vacuously). `\square`

> **Corollary D1.2 (`K=1` exact second moment; PROVED — the first
> second-moment / fluctuation result in this line, cf. `THEOREM.md` §9
> item 10).** For every `n\ge1`:
>
> `E\big[(M_n^{(1)})^2\big] = \dfrac12 + \dfrac1{2n^2}`,
>
> converging to `E[M_1^2]=1/2` (Estágio 24) at rate **exactly**
> `1/(2n^2)`.

*Proof.* From Proposition D1's CDF, the pmf of `T` is `P(T=k) =
F_n^{(1)}(k/n)-F_n^{(1)}((k-1)/n) = [k(k+1)-(k-1)k]/n^2 = 2k/n^2` for
`k=1,\dots,n-1`; `P(T=0)=0`; `P(T=n)=1-\tfrac{(n-1)n}{n^2}=\tfrac1n`
(sanity: `\sum_{k=1}^{n-1}2k/n^2 + 1/n = (n-1)/n+1/n=1`. ✓). Then

`E[T^2] = \sum_{k=1}^{n-1}k^2\cdot\dfrac{2k}{n^2} + n^2\cdot\dfrac1n
= \dfrac2{n^2}\sum_{k=1}^{n-1}k^3 + n = \dfrac2{n^2}\Big[\dfrac{(n-1)n}2\Big]^2+n
= \dfrac{(n-1)^2}2+n`,

so `E[(M_n^{(1)})^2]=E[T^2]/n^2 = \dfrac{(n-1)^2}{2n^2}+\dfrac1n
= \dfrac{n^2-2n+1}{2n^2}+\dfrac1n = \Big(\dfrac12-\dfrac1n+\dfrac1{2n^2}\Big)+\dfrac1n
= \dfrac12+\dfrac1{2n^2}`. `\square`

(Consistency check, also PROVED: the same pmf reproduces `E[T]=
\tfrac{2n}3+\tfrac1{3n}`, i.e. `\varphi_n^{(1)}=\tfrac23+\tfrac1{3n^2}`,
`THEOREM.md` Proposition 4, exactly — see §7 "Verification" below for
the independent exact-enumeration check of both.)

> **Corollary D1.3 (variance, PROVED).** `\mathrm{Var}(M_n^{(1)}) \to
> \mathrm{Var}(M_1) = \tfrac12-\big(\tfrac23\big)^2=\tfrac1{18}` as
> `n\to\infty` (immediate from Corollaries D1.1's mean formula and
> D1.2). The first fluctuation-level convergence result proved for any
> `K` anywhere in this research line.

---

## 6. General `K\ge2`: a proved reduction, and honest non-closure

### 6.1 Why the existing `K\ge2` machinery does not transfer

`THEOREM.md` Estágios 3–7 (`\psi_n^{(K)}`, the generic-point reduction,
the transfer-matrix and Gronwall arguments closing the mean bridge for
every `K`) compute, by construction, only the **marginal** probability
`P(x_0\text{ cyclic})` — which recovers `\varphi_n^{(K)}=E[M_n^{(K)}]`
by exchangeability (linearity of expectation over single-point
indicators) but is structurally incapable of saying anything about a
*joint* two-point (or whole-space) quantity: the entire apparatus never
once looks at whether a *second*, distinguished point is cyclic. This is
not a gap in that machinery — it was never asked to do more, and closes
its own (mean) question completely and unconditionally. It is simply the
wrong tool for a variance or CDF statement, exactly as `THEOREM.md`
Estágio 18/25 (§6.2 of `joint_two_point_attempt/ATTEMPT.md`) already
found for the analogous continuum question.

### 6.2 Lemma P2: the second-moment reduces to a generic pair (PROVED)

For `K\ge0` and `n>K+1`, fix the rerouted set WLOG at `\{1,\dots,K\}`
(Definition 4's convention). Define, for `n` large enough that the
relevant index pairs exist:

`P_{nn}(n,K) := P(n,n{-}1\text{ both cyclic})` (`K\le n-2`, a pair of
non-rerouted points),
`P_{nr}(n,K) := P(n,1\text{ both cyclic})` (`K\ge1`, one non-rerouted,
one rerouted),
`P_{rr}(n,K) := P(1,2\text{ both cyclic})` (`K\ge2`, both rerouted).

> **Lemma P2.** For `K\ge2`, `n>K+1`:
>
> `E\big[(M_n^{(K)})^2\big] = \dfrac{\varphi_n^{(K)}}n
> + \dfrac{(n-K)(n-K-1)}{n^2}P_{nn}(n,K)
> + \dfrac{2K(n-K)}{n^2}P_{nr}(n,K)
> + \dfrac{K(K-1)}{n^2}P_{rr}(n,K)`,
>
> **exactly**, for every such `n`. Consequently, since `P_{nr},P_{rr}
> \in[0,1]` and `\varphi_n^{(K)}\in[0,1]`, and `K` is fixed as
> `n\to\infty`: `\lim_n E[(M_n^{(K)})^2]` exists **iff** `\lim_n
> P_{nn}(n,K)` exists, and then the two limits coincide.

*Proof.* Write `C:=\#\{\text{cyclic points}\}=nM_n^{(K)}`. By linearity
of expectation over the `n(n-1)` ordered pairs of distinct points,
`E[C^2] = E[C] + \sum_{i\ne j}P(i,j\text{ both cyclic})`. Definition 4's
model is exchangeable *within* the non-rerouted points `\{K{+}1,\dots,n\}`
(all are treated symmetrically: `\pi` is a uniform random permutation,
and no non-rerouted index is distinguished by the construction) and
*within* the rerouted points `\{1,\dots,K\}` (the `U_i`, `i\le K`, are
i.i.d., and `\pi`'s marginal law does not distinguish which labels are
in `\{1,\dots,K\}` versus not — this is the same exchangeability fact
Definition 4 already invokes to declare `\varphi_n^{(K)}` well-defined).
Hence `P(i,j\text{ both cyclic})` takes only the three values
`P_{nn},P_{nr}(=P_{rn})`, `P_{rr}` according to how many of `i,j` are in
`\{1,\dots,K\}`, and there are exactly `(n-K)(n-K-1)` ordered
non-rerouted/non-rerouted pairs, `2K(n-K)` ordered mixed pairs, and
`K(K-1)` ordered rerouted/rerouted pairs (elementary count, partitioning
the `n(n-1)` ordered pairs by type). Substituting and dividing by `n^2`
(`E[C]/n^2 = \varphi_n^{(K)}/n`) gives the stated identity. The limit
claim follows since the coefficients of `P_{nr},P_{rr}` are `O(K/n)\to0`
(K fixed) and `\varphi_n^{(K)}/n\to0` (bounded numerator over `n`), while
the coefficient of `P_{nn}` `\to1`. `\square`

This is the exact 2-point generalization of `THEOREM.md` Estágio 3's
**Reduction Lemma A** for the mean (`\varphi_n^{(K)} = (K/n)\psi_n^{(K),R}
+(1-K/n)\psi_n^{(K)}`) — the "at least one point of interest is itself
rerouted" contribution vanishes in the limit either way, leaving only
the fully generic quantity.

### 6.3 What is genuinely missing

Lemma P2 reduces "does `E[(M_n^{(K)})^2]\to1/(K+1)`?" (itself only a
*necessary*, not sufficient, condition for the full CDF bridge
`F_n^{(K)}\to F_K`) to a single scalar question: does `P_{nn}(n,K)\to
1/(K+1)`? This is **not resolved** in this document. A first attempt at
a closed form via `K=1`'s case-split method (§5) does not obviously
generalize: `THEOREM.md`'s own `k2_open_lemma/ATTEMPT.md` §7 already
documents, for the strictly *easier* single-point marginal problem, that
the cost of an explicit case analysis grows combinatorially with `K`
(number of reroute sources on the reference cycle × their relative order
× the order in which the rest of the exploration resolves); the
*joint*-pair version attempted here inherits at least that same growth,
plus the additional bookkeeping of tracking a **second** reference
point's cyclic status through the same case tree — exactly the
"destination information a genuine joint construction needs," per
Estágio 18/25's diagnosis of the structurally analogous continuum
problem. No closed form for `P_{nn}(n,K)`, `K\ge2`, was found in the
time budget of this front. This is reported as the precise open item,
not folded into a vague "K≥2 is hard."

**What §7 below reports instead:** the numerical trend of `P_{nn}(n,K)`
and of the full-CDF discrepancy `D(n,K)`, for `K=2,3`, as evidence — not
proof — that the reduction targets of Lemma R and Lemma P2 are plausibly
both true at `K\ge2`, exactly mirroring the epistemic status
`THEOREM.md` §7.4 itself assigned to the `K=2` *mean*-bridge question
before Estágio 3 closed it.

---

## 7. Numerical exploration (NUMERICALLY EXPLORED throughout — not proof)

All scripts in this directory. No claim below is upgraded past
"numerically explored" by anything in this section.

### 7.1 Exact enumeration (`exact_enumeration.py`, deterministic, no
randomness — all `n!\cdot n^K` configurations enumerated exactly, exact
`Fraction` arithmetic throughout)

Cells: `K=0` (`n=1,2`), `K=1` (`n=2,\dots,9`), `K=2` (`n=3,\dots,9`),
`K=3` (`n=4,\dots,8`). For every cell, the script records the **full**
exact distribution of `T=\#\text{cyclic}` (not just its mean), plus the
exact values of `P_{nn},P_{nr},P_{rr}` where the relevant index pairs
exist. Raw output: `exact_enumeration_results.json`.

**(a) Proposition D1 (`K=1` CDF), independently checked.** For every
`n=2,\dots,9` and every `k=0,\dots,n`, the enumerated exact CDF matches
`k(k+1)/n^2` (`k<n`) / `1` (`k=n`) **exactly** (rational equality, not
floating point) — `analyze_cdf.py` part (a), `8/8` cells, `0`
mismatches.

**(b) Corollary D1.2 (`K=1` second moment) and Lemma P2's identity,
independently checked.** For every enumerated cell with `K\ge0`,
`E[(M_n^{(K)})^2]` computed directly from the exact `T`-distribution
matches Lemma P2's formula (§6.2) to the last digit of exact rational
arithmetic — `18/18` cells, `0` mismatches. The `K=1` closed form
`E[(M_n^{(1)})^2]=\tfrac12+\tfrac1{2n^2}` matches the direct computation
exactly for all `n=2,\dots,9`.

**(c) `P_{nn}(n,K)` trend toward `1/(K+1)`, `K=1,2,3` (evidence only).**

| `K` | target `1/(K+1)` | `P_{nn}(n,K)`, `n=` smallest `\to` largest tested | monotone? |
|---|---|---|---|
| 1 | 0.500000 | `n=3`: 0.55556 → `n=9`: 0.51852 | yes, every step |
| 2 | 0.333333 | `n=4`: 0.39583 → `n=9`: 0.36008 | yes, every step |
| 3 | 0.250000 | `n=5`: 0.31120 → `n=8`: 0.28658 | yes, every step |

`K=1` is in fact **exact**, `P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` for
`n=3,\dots,9` (rational equality, `7/7`, `analyze_cdf.py` part (d)) —
this closed form is reported as an **exact-verified pattern from finite
instances**, not a proof for general `n` (no derivation of it is given
in this document, unlike Proposition D1, which *is* a real proof); it
is consistent with, and gives an independent finite-`n` cross-check of,
Corollary D1.2 (though not needed for that Corollary's own proof, which
uses the full `T`-distribution directly).

For `K=2,3`, fitting `n\cdot(P_{nn}(n,K)-\tfrac1{K+1}) \approx a+b/n` to
the largest few data points suggests `a\approx7/30\approx0.2333` at
`K=2` — a numerical curiosity, **not** claimed as an exact rate; no
formula is asserted for `K\ge2`, exactly the caution `THEOREM.md` §7.4
itself already models for the analogous mean-bridge rate question at
`K=2` (do not extrapolate a clean rate from a handful of points).

**(d) Full-CDF discrepancy `D(n,K):=\max_{k=0,\dots,n}|F_n^{(K)}(k/n)-F_K(k/n)|`,
`K=2,3` (evidence only, `analyze_cdf.py` part (b)).**

| `n` | `D(n,2)` | `n\cdot D(n,2)` | `D(n,3)` | `n\cdot D(n,3)` |
|---|---|---|---|---|
| 3 | 0.1235 | 0.370 | — | — |
| 4 | 0.1250 | 0.500 | 0.0740 | 0.296 |
| 5 | 0.1056 | 0.528 | 0.0767 | 0.384 |
| 6 | 0.0958 | 0.575 | 0.0746 | 0.447 |
| 7 | 0.0852 | 0.597 | 0.0696 | 0.487 |
| 8 | 0.0759 | 0.607 | 0.0652 | 0.522 |
| 9 | 0.0695 | 0.626 | — | — |

`D(n,K)` itself decreases monotonically (up to one blip at the very
smallest `n`) over the whole tested range for both `K=2,3` — consistent
with `F_n^{(K)}\to F_K`. `n\cdot D(n,K)` is *not* leveling off over this
range (still slowly climbing at the largest `n` tested), so — exactly
as `THEOREM.md` §7.4 flagged for the mean bridge at `K=2` — **no rate is
claimed**; this data supports convergence, not any particular speed of
convergence.

### 7.2 Monte Carlo at larger `n` (`monte_carlo.py`, reserved seeds)

Exact enumeration is infeasible much past `n\approx9`
(`n!\cdot n^K` growth). To check the trend persists at much larger `n`,
Monte Carlo was run for `K=2,3` at `n\in\{50,150,500,2000\}` (fixed-`K`
model, `40320+`-trial budget adaptively scaled so `n\cdot\text{trials}
\approx1.5\times10^7` per cell — trial counts shown per row) and for the
**actual mixed-`c` model** `M_n(c)` directly (Definition 1, no
conditioning on `K` at all) at `c=1,4`, same `n` grid, against
`F(x)=1-e^{-cx^2}`.

| setting | `n` | trials | `D_{KS}` | `2^{\text{nd}}` moment (target) |
|---|---|---|---|---|
| `K=2` | 50 | 250000 | 0.0158 | 0.3348 (0.3333) |
| `K=2` | 2000 | 7500 | 0.0107 | 0.3291 (0.3333) |
| `K=3` | 50 | 250000 | 0.0182 | 0.2519 (0.2500) |
| `K=3` | 2000 | 7500 | 0.0067 | 0.2515 (0.2500) |
| mixed `c=1` | 50 | 250000 | 0.0079 | mean 0.7465 (target `\varphi_\infty(1)\approx0.7468`) |
| mixed `c=1` | 2000 | 7500 | 0.0078 | mean 0.7494 |
| mixed `c=4` | 50 | 250000 | 0.0139 | mean 0.4411 (target `\varphi_\infty(4)\approx0.4410`) |
| mixed `c=4` | 2000 | 7500 | 0.0053 | mean 0.4405 |

(Full table, all `16` cells, in `monte_carlo_results.json`.) All means
and second moments track their targets within a few times the Monte
Carlo standard error (`\approx0.5/\sqrt{\text{trials}}`, e.g. `\approx
0.006` at `n=2000`'s `7500` trials) at every `n` tested, for both the
fixed-`K` models and the actual mixed-`c` model directly. **Important
caveat, disclosed rather than glossed over:** because the trial budget
was deliberately *shrunk* as `n` grows (to keep `n\cdot\text{trials}`,
hence total runtime, roughly constant), the Kolmogorov statistic
`D_{KS}` at the largest `n` is dominated by its own sampling noise floor
(`\sim1/\sqrt{\text{trials}}`), not by the true bias `F_n^{(K)}-F_K`; the
apparent growth in `n\cdot D_{KS}` at large `n` in the raw table is
**not** evidence of a diverging discrepancy — it is an artifact of this
front's constant-work-budget design, and is explicitly not read as such
anywhere above. The exact-enumeration data of §7.1 (noise-free, exact
rational arithmetic) is the only numerical evidence in this document
given any weight toward a *trend* claim; the Monte Carlo data's role is
only to confirm the same qualitative picture (means, second moments,
and `D_{KS}` all small and stable) persists at `n` two to three orders
of magnitude beyond exact enumeration's reach.

---

## 8. Self-caught issues (disclosed per archive convention)

1. **`exact_enumeration.py`, first version — a real bug, caught before
   any downstream claim used the affected numbers.** The script's
   `summarize()` function initially reported `P_{nn}=0.0` (rather than
   "not applicable") whenever the required index pair `(n{-}1,n{-}2)`
   included a rerouted point (e.g. `n=4,K=3`, where indices `0,1,2` are
   rerouted and only index `3` is free, so no valid non-rerouted *pair*
   exists) — the gating check tested whether the raw *counter* variable
   was `None` (it never is; counters start at `0`) rather than whether
   the *index tuple* itself was `None`. Caught by inspecting the printed
   table (`n=4,K=3` showing a suspicious exact `0.0` inconsistent with
   neighboring cells) before any number from that row was used anywhere
   in this document. Fixed by gating on the index tuples directly; the
   corrected run (used throughout §7) reports `P_{nn}=\text{N/A}` for
   `n=4,K=3`, and every other previously-reported value was
   double-checked unaffected by the bug (all other cells had valid index
   tuples in both the buggy and fixed runs; the fix changed no other
   number, only added correct `None`/absent handling).
2. **First Monte Carlo design used `numpy` scalar indexing inside the
   per-sample cycle-detection loop** (arrays for `f`/`color`), which is
   known to be far slower than plain Python lists for this access
   pattern; an early back-of-envelope runtime estimate (before writing
   the final version) suggested part of the planned `n=5000` cell would
   take on the order of hours. Caught before running anything at that
   scale, by estimating total elementary operations (`n\times\text{trials}`)
   against a conservative Python-loop throughput, not by an actual
   failed run. Fixed by converting to plain Python lists inside the hot
   loop and adopting an explicit, disclosed constant-work-budget
   (`n\times\text{trials}\approx1.5\times10^7` per cell) instead of a
   fixed large `n` and fixed large trial count — see §7.2's caveat about
   what this design choice does and does not let the Monte Carlo data
   support.
3. **No bug found in the core mathematics (Propositions D0/D1, Lemma R,
   Lemma P2)** during self-review; all closed-form claims in §§5–6 were
   cross-checked against the independent exact-enumeration data (§7.1
   (a)–(b)) with exact rational arithmetic before being written up as
   PROVED, and every reported "EXACT MATCH" in this document reflects an
   actual `Fraction`-equality check in `analyze_cdf.py`'s output, not an
   eyeballed floating-point comparison.

---

## 9. What remains open (precise)

1. **The fixed-`K` distributional bridge, `K\ge2`**: `F_n^{(K)}(x)\to
   F_K(x)` for `x\in(0,1)`. Unproved. By Corollary R.1, this — for
   *every* `K\ge2` simultaneously, together with the already-closed
   `K=0,1` cases — is exactly what is needed to promote the Target
   statement (`M_n(c)\to_d M(c)`) from "reduced to a named hypothesis"
   to "theorem." A proof strategy is not even sketched here (unlike
   `THEOREM.md` §7.4's Open Lemma for the mean, which at least had a
   coupling sketch); this document's contribution at `K\ge2` is the
   reduction (Lemma P2) and numerical evidence (§7), not a strategy.
2. **`P_{nn}(n,K)\to1/(K+1)`, `K\ge2`** (needed by Lemma P2 for even the
   *second moment* alone, a strictly weaker target than item 1). Open.
   Diagnosed precisely in §6.3: needs either a whole-space `K=2` case
   analysis (cost growth documented in `k2_open_lemma/ATTEMPT.md` §7 for
   the easier marginal problem) or a genuine joint two-point exploration
   (the exact obstruction Estágio 18/25 already named, for a related but
   distinct continuum quantity).
3. **Any moment beyond the second**, for any `K\ge1` including `K=1`
   itself (only the second moment is closed here, Corollary D1.2) — not
   attempted; would need the same case-split method pushed further (for
   `K=1` this looks mechanical, since Proposition D1 already gives the
   *entire* law, from which every moment is a finite sum — not executed
   here purely for scope/time, flagged as low-hanging fruit for a
   follow-up).
4. **A locally-uniform-in-`x`, uniform-in-`c`** version combining this
   front's Corollary D1.1-style rate with `THEOREM.md` Estágio 22's
   uniform-in-`c` mean rate — not formulated.
5. **The rate of `D(n,K)\to0`**, `K\ge2`, given item 1 is eventually
   resolved — explicitly not estimated (§7.1(d)'s caution).

Nothing above was left vague to save effort: each names the precise
missing statement and what partial progress (if any) exists toward it.

---

## 10. Seeds

Reserved range: `20260876000`–`20260877000` (this front's own; the
referee range `20260877000+` untouched). All Monte Carlo in
`monte_carlo.py` draws from a single `numpy.random.SeedSequence(20260876000)`
rooted at the base seed, via `.spawn(1)` called once per cell, in
sequence order — so every cell gets a distinct, deterministically
reproducible child seed. Full mapping (cell → spawn index) is written to
`monte_carlo_results.json`'s per-row `seed_child_index` field; no seed
(root or any spawned child) was reused across cells or scripts, and
`exact_enumeration.py`/`analyze_cdf.py` use no randomness at all
(exhaustive/deterministic throughout).

| script | seed source | cells |
|---|---|---|
| `exact_enumeration.py` | none (exhaustive) | `K=0,1,2,3`, `n` up to `8`–`9` |
| `monte_carlo.py` | `SeedSequence(20260876000)`, `16` spawned children, indices `1`–`16` | `K=2,3` × `n\in\{50,150,500,2000\}`; `c=1,4` × same `n` grid |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Proposition D0 (exact finite-`n` CDF mixture identity) | **PROVED** |
| 2 | Continuum mixture `F(x)=\sum_K e^{-c}c^K/K!\,F_K(x)` | **CITED** (Estágio 24) |
| 3 | Lemma R (fixed-`K` CDF convergence, every `K` `\Rightarrow` Target statement) | **PROVED** |
| 4 | Corollary R.1 (Target statement, conditional on the fixed-`K` hypothesis) | **PROVED** (conditional — see item 11 below for status of the hypothesis) |
| 5 | `K=0` exact bridge | **PROVED** (exact identity, every `n`) |
| 6 | Proposition D1 (`K=1` exact finite-`n` CDF) | **PROVED** |
| 7 | Corollary D1.1 (`K=1` distributional convergence, uniform `O(1/n)` rate) | **PROVED** |
| 8 | Corollary D1.2 (`K=1` exact second moment, rate `O(1/n^2)`) | **PROVED** |
| 9 | Corollary D1.3 (`K=1` variance convergence) | **PROVED** |
| 10 | Lemma P2 (general-`K` second-moment reduction to `P_{nn}(n,K)`) | **PROVED** |
| 11 | `F_n^{(K)}(x)\to F_K(x)`, `K\ge2` | **OPEN** |
| 12 | `P_{nn}(n,K)\to1/(K+1)`, `K\ge2` | **OPEN**; NUMERICALLY EXPLORED (monotone trend, `K=2,3`, exact enumeration `n\le9`) |
| 13 | `P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` | exact-verified pattern (`n=3,\dots,9`, rational arithmetic), **not proved** for general `n` in this document |
| 14 | `D(n,K)\to0`, `K=2,3` | NUMERICALLY EXPLORED (monotone decrease over full tested range); **no rate claimed** |
| 15 | Full Target statement `M_n(c)\to_d M(c)` | **NOT established**; reduced unconditionally to item 11 (equivalently, given Lemma R, to items 5–6 which are closed, plus item 11 for `K\ge2` which is open) |

---

## 12. Files

| file | contents |
|---|---|
| `PREREG.md` | pre-registration, written before the numerical work |
| `ATTEMPT.md` | this document |
| `exact_enumeration.py` | exhaustive exact enumeration (no randomness), `K=0,1,2,3`, `n` up to `8`–`9`; full `T`-distribution + `P_{nn},P_{nr},P_{rr}` per cell |
| `exact_enumeration_results.json` | raw output of the above |
| `analyze_cdf.py` | checks Proposition D1's closed form, Lemma P2's identity, and the `P_{nn}(n,1)` exact pattern against `exact_enumeration_results.json`; computes `D(n,K)` |
| `monte_carlo.py` | Monte Carlo, reserved seeds `20260876000`–`20260877000`, fixed-`K` and mixed-`c` models, `n` up to `2000` |
| `monte_carlo_results.json` | raw output of the above |

---

## 13. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
or `DISCOVERY_LAB_STATE.md`. No `adversarial/` subdirectory created, no
referee dispatched by this front. No git commands run. Every claim above
is labeled PROVED / CITED / NUMERICALLY EXPLORED / OPEN at the point of
use; nothing is asserted as CONJECTURE without also being explicitly
so-labeled (none of this front's own new claims reached "conjecture"
status — each is either proved outright or left fully open, with the
sole intermediate case being the `P_{nn}(n,1)` exact-verified-pattern of
item 13, which is flagged as such rather than silently promoted). No
claim of progress on any Millennium Problem; this is pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.
