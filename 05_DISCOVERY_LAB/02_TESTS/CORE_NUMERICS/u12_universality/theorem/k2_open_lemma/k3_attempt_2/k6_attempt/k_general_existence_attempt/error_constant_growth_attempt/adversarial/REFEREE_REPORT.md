# Hostile adversarial referee report — `error_constant_growth_attempt/ATTEMPT.md`

> **Mandate.** Independent hostile re-verification of the wave-10 front-(b) document
> (`DISC-DEC-045`, `K-GENERAL-ERROR-CONSTANT-GROWTH-ATTEMPT`), which is a *positive*
> result and therefore cannot be catalogued without this pass. The target's own §8.4
> names the `ε²` Taylor-matching of §3.1 as the load-bearing derivation; that is where
> this report starts and where most of its weight sits.
>
> **Discipline.** Everything computational in this directory was written from scratch
> **before** any of the target's own `.py` files was opened. I read only the target's
> `ATTEMPT.md` prose (the object under test) and the predecessors' `ATTEMPT.md`
> statements of already-PROVED inputs. My `ref_core.py` header records exactly the
> three things transcribed from prose (the exact `(a,b,r)` transition rules; the base
> facts `g_0,h_0`; and the already-PROVED `c_k^{(r)}(b)`, `d_k^{(r)}(b)` closed forms —
> the last used **only as comparison targets**, never as ladder inputs). My ladder
> solves *my own* `ε⁰`/`ε¹`/`ε²` ODEs. Exact `fractions.Fraction` / `sympy` arithmetic
> throughout; floats only in display columns; `mpmath` at dps 60 for the large-`r`
> asymptotics, cross-checked against exact rationals to `2.2×10⁻⁶⁰`.
> Nothing outside this `adversarial/` directory was created or modified. No git commit.

---

## 0. Executive summary — SPLIT VERDICT

**The mathematical core of the document is SOUND.** I re-derived the `ε²` matching by
hand from the exact discrete recursion, solved the resulting ODE with my own code, and
obtained the target's `H_r` ODE, its `L_r` relation, and its Theorem 1 closed form
exactly. The strongest available internal check passes for me too: my `ε⁰` and `ε¹`
orders reproduce the already-PROVED `c_k^{(r)}(b)` and `d_k^{(r)}(b)` at **5022** index
triples each, with `0` mismatches — so the machinery is validated one order down before
it is used. Theorems 1, 2, 3, Corollaries 1a/2a/3a, Lemma 7 and Proposition 6 all
survive.

**But Theorem 4 — the growth-rate theorem — carries two stated formulas that are
FALSE, and I can correct both exactly.**

| # | finding | severity |
|---|---|---|
| **F-1** | Theorem 4's third term is stated as `+\frac{\sqrt\pi}{128}r^{1/2}`. The correct coefficient is `-\frac{\sqrt\pi}{512}` — **wrong sign and wrong magnitude (factor 4)**. The document's *own* numerics in §5.2 (the ratio row `0.99954, 0.999957, …` approaching `1` from **below**) already contradict its own printed *positive* term. The term originates in a hard-coded print string (`asymptotics.py:173`); it was never computed. | **FLAWED** — but harmless to `Θ(r^{3/2})` and to the leading constant |
| **F-2** | The executive summary's displayed formula `D^*_r(b)=\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}+O(\sqrt r)` is **false for every `b\ge1`**. The linear coefficient is **exactly** `-(3b+2)/24`, not `-1/12`; the stated formula's error is `Θ(br)`, not `O(\sqrt r)`. (§5.2's body text, which only claims `D^*_r(b)\sim\frac{3\sqrt\pi}{64}r^{3/2}`, is correct — the flaw is confined to the summary display.) | **FLAWED** |
| **F-3** | §5.2's *mechanism* for `b`-independence — "the factor `2^{b+1}` in `2^N` exactly cancels the `2^{-(b+1)}` in the prefactor `r!(r{+}b)!/(2r{+}b{+}1)!`" — is wrong as written: **that prefactor contains no power of 2 at all**. Scorecard row 9 honestly flags this step as "PROVED-MODULO the Stirling step being written out in full", so the gap is disclosed; but the sketch offered is not merely incomplete, it is incorrect. | **SOUND WITH NAMED ISSUE** (correctly flagged, wrongly sketched) |

**F-3 is now closed, in the affirmative.** Rather than patch the Stirling sketch I
derived an **exact closed form for `D^*_r(b)` at every `b`** (Part 3.1 below), verified
exactly at 287 `(r,b)` pairs against the direct half-sum and at 217 against my ODE
ladder. From it the `b`-independence of `3\sqrt\pi/64` follows rigorously with **no
Stirling estimate needed for the odd part at all**, and the exact linear term
`-(3b{+}2)r/24` drops out algebraically. This also answers the document's own open item
§8.3(2) ("a closed form for `D^*_r(b)` at `b\ge1`") in the affirmative.

**Corrected Theorem 4** (mine, verified to 10 significant figures out to `r=10^8`):

> `\displaystyle D^*_r(b)=\frac{3\sqrt\pi}{64}r^{3/2}\;-\;\frac{(3b{+}2)r}{24}\;+\;\frac{\sqrt\pi}{48}\Big[\tfrac{45}{16}\beta^2-\tfrac{15}{16}\beta-\tfrac{63}{32}\Big]r^{1/2}\;+\;O(1)`, `\quad\beta:=b{+}1`,
>
> which at `b=0` reads `\;\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}-\frac{\sqrt\pi}{512}r^{1/2}+O(1)`.

Additionally, eight **overclaim / bookkeeping** defects are listed in Part 6. None
changes a truth value; two of them (O-1, O-2) are the kind the archive's discipline
exists to catch — prose asserting flatly what the scorecard marks conditional.

**Bottom line.** The document's headline claims stand: the true residual constant is
`Θ(r^{3/2})` with leading constant `3\sqrt\pi/64`, `b`-independent, and at `b=0`
exactly `\frac{r(3r+1)}{32}\varphi_r-\frac r{12}`; the published bound is factorial;
the two looseness mechanisms are correctly located and Proposition 6 is rigorous. The
document should **not** be catalogued as-is: F-1 and F-2 are stated theorems that are
wrong, and must be replaced by the corrected statement above before integration.

---

## Part 1. The `ε²` matching of §3.1, re-derived from scratch

*(the derivation §8.4 asks a referee to attack first — done here entirely by hand,
before any code was written)*

### 1.1 The exact recursion, taken from the predecessors, not from the target

From `k3_attempt_2/ATTEMPT.md` §2 (PROVED), with `m:=n-a`:

`g(a,b,r)=\frac1m+\frac rm h(a{+}1,b,r{-}1)+\frac{m-1-r-b}{m}g(a{+}1,b,r)`,
`\qquad h(a,b,r)=\frac1n+\frac rn h(a,b{+}1,r{-}1)+\frac{n-1-a-b-r}{n}g(a,b{+}1,r)`.

In `(m,b)` coordinates, `g_r(m,b):=g(n{-}m,b,r)`, `h_r(a,b):=h(a,b,r)`:

`g_r(m,b)=\frac1m+\frac rm h_{r-1}(n{-}m{+}1,b)+\frac{m-1-r-b}{m}g_r(m{-}1,b)`

which rearranges (multiply by `m`, add and subtract `m\,g_r(m{-}1,b)`) to

`(*)\quad m[g_r(m,b)-g_r(m{-}1,b)]+(1{+}r{+}b)g_r(m{-}1,b)=1+r\,h_{r-1}(n{-}m{+}1,b)`,

and the source step becomes

`(**)\quad h_r(a,b)=\tfrac1n+\tfrac rn h_{r-1}(a,b{+}1)+\big[(1{-}s)-\tfrac{1+b+r}{n}\big]g_r(n{-}a,b{+}1)`, `s=a/n`.

**Both agree verbatim with the target's §3.1 restatement.** ✔ (The target's restatement
of `(*)` and `(**)` is accurate; I checked it against the predecessor, not against the
target's own paraphrase.)

### 1.2 My own substitution

Write `\varepsilon:=1/n`, `t=m/n`, and carry one extra unknown order so that nothing is
lost when multiplying by `m=t/\varepsilon`:

`g_r(m,b)=F+\varepsilon G+\varepsilon^2H+\varepsilon^3M+O(\varepsilon^4)`.

Since `(m{-}1)/n=t-\varepsilon`:

`g_r(m{-}1,b)=F(t{-}\varepsilon)+\varepsilon G(t{-}\varepsilon)+\varepsilon^2H(t{-}\varepsilon)+\varepsilon^3M(t{-}\varepsilon)+O(\varepsilon^4)`
`\;=F+\varepsilon(G-F')+\varepsilon^2(H-G'+\tfrac12F'')+\varepsilon^3(M-H'+\tfrac12G''-\tfrac16F''')+O(\varepsilon^4)`.

Subtracting and multiplying by `m=t/\varepsilon` — the `M` terms cancel:

`m[g_r(m)-g_r(m{-}1)]=tF'+\varepsilon\,t(G'-\tfrac12F'')+\varepsilon^2\,t(H'-\tfrac12G''+\tfrac16F''')+O(\varepsilon^3)`.

For the source, `n{-}m{+}1=n(1{-}t)+1`, so `s=(1{-}t)+\varepsilon` **exactly** (this is
the one place a shift enters, and the target handles it correctly). Expanding about
`s_0=1{-}t`:

`h_{r-1}(n{-}m{+}1,b)=\hat H_{r-1}+\varepsilon[\hat H_{r-1}'+K_{r-1}]+\varepsilon^2[\tfrac12\hat H_{r-1}''+K_{r-1}'+L_{r-1}]+O(\varepsilon^3)`.

Matching orders in `(*)`:

| order | result |
|---|---|
| `\varepsilon^0` | `tF_r'+(1{+}r{+}b)F_r=1+r\hat H_{r-1}(1{-}t,b)` — **exactly Fact 2** ✔ |
| `\varepsilon^1` | `t(G'-\tfrac12F'')+(1{+}r{+}b)(G-F')=r[\hat H_{r-1}'+K_{r-1}]`, i.e. `tG_r'+(1{+}r{+}b)G_r=r\hat H_{r-1}'+rK_{r-1}+\tfrac t2F_r''+(1{+}r{+}b)F_r'` — **exactly Fact 3** ✔ |
| `\varepsilon^2` | `t(H'-\tfrac12G''+\tfrac16F''')+(1{+}r{+}b)(H-G'+\tfrac12F'')=r[\tfrac12\hat H_{r-1}''+K_{r-1}'+L_{r-1}]` |

Rearranging the last line:

> **`H_r` ODE (mine).**
> `t H_r'+(1{+}r{+}b)H_r=r\big[\tfrac12\hat H_{r-1}''(1{-}t,b)+K_{r-1}'(1{-}t,b)+L_{r-1}(1{-}t,b)\big]+\tfrac t2G_r''-\tfrac t6F_r'''+(1{+}r{+}b)\big[G_r'-\tfrac12F_r''\big]`

**Character-for-character the target's boxed statement.** ✔

For `(**)`: `a=ns` exactly, no shift, and `(n{-}a)/n=1{-}s` exactly, so no Taylor
expansion is needed — pure algebra. Matching:

| order | result |
|---|---|
| `\varepsilon^0` | `\hat H_r(s,b)=(1{-}s)F_r(1{-}s,b{+}1)` — the definition ✔ |
| `\varepsilon^1` | `K_r(s,b)=1+r\hat H_{r-1}(s,b{+}1)+(1{-}s)G_r(1{-}s,b{+}1)-(1{+}b{+}r)F_r(1{-}s,b{+}1)` — the definition ✔ |
| `\varepsilon^2` | `L_r(s,b)=r\,K_{r-1}(s,b{+}1)+(1{-}s)H_r(1{-}s,b{+}1)-(1{+}b{+}r)G_r(1{-}s,b{+}1)` |

**Again character-for-character the target's boxed `L_r` relation.** ✔

**Base cases.** `g_0(m,b)=1/(b{+}1)` exactly ⟹ `H_0\equiv0`. `h_0(a,b)=(n{-}a{+}1)/(n(b{+}2))=(1{-}s)/(b{+}2)+\varepsilon/(b{+}2)` has **no** `\varepsilon^2` term ⟹ `L_0\equiv0`; and the `L_r` relation at `r=0` returns `0\cdot K_{-1}+(1{-}s)H_0-(1{+}b)G_0=0` ✔ consistent.

### 1.3 The coefficient recursion (§3.2), derived independently

Using `\hat H_{r-1}(1{-}t,b)=tF_{r-1}(t,b{+}1)` and, for `\phi(s)=\hat H_{r-1}(s,b)`,
`\psi(t)=\phi(1{-}t)` ⟹ `\phi''(1{-}t)=\psi''(t)` and `\phi'(1{-}t)=-\psi'(t)`, I
extracted the `t^k` coefficient of each RHS piece by hand. My result:

```
(k+1+r+b) e_k^(r)(b) = r*T + U
T = (1/2)(k+1)(k+2) c_{k+1}^(r-1)(b+1)                 <- (1/2)Hhat''_{r-1}(1-t,b)
  - (k+1)(r-1)      c_k^(r-2)(b+2)      \
  - (k+1)           d_k^(r-1)(b+1)       >- K'_{r-1}(1-t,b)
  + (k+1)(b+r)      c_{k+1}^(r-1)(b+1)  /
  + (r-1)[k==0] + (r-1)(r-2) c_{k-1}^(r-3)(b+3) + (r-1) d_{k-1}^(r-2)(b+2)
  - (r-1)(b+r) c_k^(r-2)(b+2) + e_{k-1}^(r-1)(b+1) - (b+r) d_k^(r-1)(b+1)
                                                       <- L_{r-1}(1-t,b)
U = (1/2)k(k+1) d_{k+1}^(r)(b) - (1/6)k(k+1)(k+2) c_{k+2}^(r)(b)
  + (1+r+b)(k+1) d_{k+1}^(r)(b) - (1/2)(1+r+b)(k+1)(k+2) c_{k+2}^(r)(b)
```

Comparing afterwards to the target's §3.2 block: **every term and every multiplier
agrees.** The only difference is a cosmetic mislabel — the target annotates the three
`K'`-lines as `-K'_{r-1}` when their values are `+[K'_{r-1}(1{-}t,b)]_k` (defect O-8).

### 1.4 Verdict on §3.1

> **SOUND.** The `ε²` matching is correct: the `H_r` ODE and the `L_r` relation are
> exactly what the exact discrete recursion forces, the `ε⁰`/`ε¹` orders reproduce the
> already-PROVED Facts 2 and 3, the shift `s=(1{-}t)+\varepsilon` is handled exactly,
> the base cases are right and self-consistent. The §3.2 coefficient recursion is
> correct. The "no circularity" paragraph is accurate: `H_r,L_r` are *defined* as the
> unique polynomial solutions of two explicit relations, and their approximating
> property is *derived* in §4, not posited.

Machine record (`ref_step1_eps2.log`, `ref_step1b_symbolic.log`):

| check | scope | result |
|---|---|---|
| my `ε⁰` ODE solution vs PROVED `c_k^{(r)}(b)` | `r=0..30`, `b=0..8`, all `k` incl. out-of-range | **5022** checks, **0** mismatches |
| my `ε¹` ODE solution vs PROVED `d_k^{(r)}(b)` | idem | **5022** checks, **0** mismatches |
| same, symbolic `b` | `r=0..8` | all `simplify(...)=0` |
| `H_0=H_1\equiv0`, `H_2(t,0)\equiv1/15`, `H_2(t,1)\equiv1/30`, `L_0\equiv0` | — | all confirmed |
| `\hat H_2(0,0)=11/30`, `K_2(0,0)=13/20`, `L_2(0,0)=23/60` vs PROVED `ψ_n^{(3),R}` | — | all exact, `L_2` from my own `L_r` relation |

---

## Part 2. Theorem 1 — the `e_k^{(r)}(b)` closed form

I solved **my own** `H_r` ODE and compared coefficient-by-coefficient with the target's
claimed
`e_k^{(r)}(b)=\frac{(3k{+}8)(k{+}1)(k{+}2)(k{+}3)}{24}\cdot\frac{r!}{(r{-}k{-}2)!}\cdot\frac1{\prod_{i=1}^{k+3}(r{+}b{+}i)}`.

| check | scope | result |
|---|---|---|
| my ODE solution vs the claimed closed form | `r=0..30`, `b=0..8`, every `k` incl. `k=r{-}1,r` | **5022** checks, **0** mismatches |
| symbolic-`b` ladder vs closed form | `r=0..8`, `b` a `Symbol` | all `simplify(...)=0` |
| my §1.3 recursion, symbolic `r,k,b`, general `k\ge1` branch | Gamma-function form | `LHS-RHS = 0` |
| my §1.3 recursion, symbolic `r,b`, `k=0` boundary branch | idem | `LHS-RHS = 0` |
| `\deg H_r=r{-}2` (with `H_0=H_1\equiv0`) | `r=0..30`, `b=0..8` | 0 violations |
| `e_k^{(r)}(b)>0` for `0\le k\le r{-}2` | idem | 0 violations |

The `k=0` branch genuinely differs (the `(r{-}1)\cdot[k{=}0]` constant from `K_{r-2}`'s
own constant term fires there, and every index-`(k{-}1)` object vanishes) — I split it
as the target does, and both branches simplify to `0` symbolically. With `H_0\equiv0`
this is a **complete induction on `r`**.

> **Theorem 1: SOUND — PROVED.** Now unconditional relative to §3.1, since §3.1 is
> independently confirmed in Part 1.

**Corollary 1a: SOUND**, with one cosmetic defect (O-4): the document says
`H_r(\cdot,b)` is "**strictly** increasing on `[0,1]`". That is false for `r\le2`
(`H_0=H_1\equiv0` and `H_2(t,b)=e_0^{(2)}(b)` is a *constant*). The conclusion
`\max_{[0,1]}|H_r|=H_r(1,b)` is nevertheless correct in every case (non-negative
coefficients suffice), and the "`t=1` is in the grid for every `n`" observation is
right.

---

## Part 3. Theorem 3, and my exact general-`b` extension

### 3.0 The half-sum, re-derived

At `t=1`, `b=0`, `\prod_{i=1}^{k+3}(r{+}i)=(r{+}k{+}3)!/r!`, so
`e_k^{(r)}(0)=\frac{(3k{+}8)(k{+}1)(k{+}2)(k{+}3)}{24}\cdot\frac{(r!)^2}{(r{-}k{-}2)!(r{+}k{+}3)!}`.
Put `i:=r{-}k{-}2`, `u:=r{-}i=k{+}2`. Then `(r{-}k{-}2)+(r{+}k{+}3)=2r{+}1=:N`, so
`(r{-}k{-}2)!(r{+}k{+}3)!=N!/\binom Ni`; and
`(3k{+}8)(k{+}1)(k{+}2)(k{+}3)=(3u{+}2)(u{-}1)u(u{+}1)=:24w(i)`. Hence

`\displaystyle H_r(1,0)=\frac{(r!)^2}{(2r{+}1)!}\sum_{i=0}^{r-2}w(i)\binom{2r{+}1}i`,

and the range extends to `i\le r` free of charge (`w` has the factors `u` and `u{-}1`,
vanishing at `i=r` and `i=r{-}1`). ✔ Exactly the target's §5.1 step.

### 3.1 My two boundary identities — stronger than the target's, and proved

The target uses two identities "verified exactly for `r=1..119`", the second "found
from exact data". I prove **general** versions by hand, from which the target's two are
immediate specialisations.

> **I1.** `\displaystyle\sum_{i=0}^{m}(n{-}2i)\binom ni=(m{+}1)\binom n{m+1}`.
>
> *Proof.* Induction on `m`. `m=0`: `n=1\cdot\binom n1`. Step: `(m{+}2)\binom n{m+2}=(n{-}m{-}1)\binom n{m+1}`, so the increment is `(n{-}m{-}1{-}m{-}1)\binom n{m+1}=(n{-}2(m{+}1))\binom n{m+1}`. `\square`

> **I3.** `\displaystyle\sum_{i=0}^{m}(n{-}2i)^3\binom ni=(n{-}2m)^2(m{+}1)\binom n{m+1}+4nm\binom{n-1}m`.
>
> *Proof.* Abel summation against `A(i):=\sum_{j\le i}(n{-}2j)\binom nj=(i{+}1)\binom n{i+1}` (I1):
> `\sum_{i\le m}(n{-}2i)^2[A(i){-}A(i{-}1)]=(n{-}2m)^2A(m)+\sum_{i\le m-1}[(n{-}2i)^2-(n{-}2i{-}2)^2]A(i)`.
> The difference is `4(n{-}2i{-}1)`, and `A(i)=(i{+}1)\binom n{i+1}`, so with `j=i{+}1`
> the tail is `4\sum_{j=1}^m(n{-}2j{+}1)j\binom nj=4n\sum_{l=0}^{m-1}[(n{-}1){-}2l]\binom{n-1}l=4nm\binom{n-1}m` by I1 again. `\square`

At `n=N=2r{+}1`, `m=r` (so `n{-}2m=1`): I1 gives `(r{+}1)\binom{2r+1}{r+1}=(2r{+}1)\binom{2r}r`
and I3 gives `(2r{+}1)\binom{2r}r+4(2r{+}1)r\binom{2r}r=(2r{+}1)(4r{+}1)\binom{2r}r`.
**Both target identities recovered.** ✔ Exhaustive exact confirmation:
`7260` checks each over `n\le120`, all `m<n`, `0` failures; and the two specialisations
for `r=1..159`, `0` failures (`ref_step2_thm3.log`).

### 3.2 The even/odd split and Theorem 3

With `v:=i-N/2`, `c:=(b{+}1)/2`, one has `u=r{-}i=-(v{+}c)`, hence
`24w=3(v{+}c)^4-2(v{+}c)^3-3(v{+}c)^2+2(v{+}c)`. At `b=0` (`c=1/2`) this is
`\underbrace{3v^4-\tfrac32v^2+\tfrac3{16}}_{\text{even}}+\underbrace{4v^3-v}_{\text{odd}}` ✔
(1830 exact checks, 0 failures).

`N` odd makes `i\le r` an exact half-range, so the even part contributes exactly half
its full binomial sum; with `\mu_2=N/4`, `\mu_4=N(3N{-}2)/16` for `\mathrm{Bin}(N,\tfrac12)`
the full sum is `2^N\cdot3(3N{-}1)(N{-}1)/16` and the half is `4^r\cdot3r(3r{+}1)/4` ✔
(120 exact checks, 0 failures). The odd part is
`\tfrac12[A_1^{(N-2i)}-A_3^{(N-2i)}]=-2r(2r{+}1)\binom{2r}r`, and since
`(r!)^2\binom{2r}r=(2r)!`, its contribution is exactly `-r/12`.

> **Theorem 3: SOUND — PROVED.** `D^*_r(0)=\frac{r(3r{+}1)}{32}\varphi_r-\frac r{12}`.

| check | scope | result |
|---|---|---|
| half-sum representation vs my ODE-solved `H_r(1,0)` | `r=0..45` | 0 mismatches |
| Theorem 3 vs my ODE-solved `H_r(1,0)` | `r=0..45` | 0 mismatches |
| Theorem 3 vs my half-sum | `r=0..80` | 0 mismatches |
| the `r=0..7` table | — | `0,0,\frac1{15},\frac5{28},\frac{103}{315},\frac{1405}{2772},\frac{1431}{2002},\frac{2219}{2340}` — identical to the target's |

**Corollary 3a: SOUND.** `3\varphi_1=2` gives `\frac{1\cdot4}{32}\cdot\frac23=\frac1{12}=\frac r{12}`, an exact cancellation. The document's own writing caution ("never write `D^*_r(0)>0` for all `r\ge0`") is correct and worth keeping.

### 3.3 NEW: an exact closed form for `D^*_r(b)` at every `b`

The target says (§8.3 item 2) that "no clean closed form was found at `b\ge1`" and
(row 9) that the `b\ge1` asymptotic is "PROVED-MODULO the Stirling step". **Both can be
resolved exactly.** Two prefactor collapses do the work; with `P_b:=r!(r{+}b)!/N!`,
`N=2r{+}b{+}1`, `\beta:=b{+}1`, and `N{-}1{-}r=r{+}b`:

`\displaystyle P_b\binom{N-1}r=\frac{(r{+}b)!}{N\,(r{+}b)!}=\frac1N`, `\qquad P_b\,(r{+}1)\binom N{r+1}=\frac{r!(r{+}b)!\,(r{+}1)}{(r{+}1)!(r{+}b)!}=1`.

Both are **exact identities, no asymptotics**. Feeding I1 and I3 at `(n,m)=(N,r)` into
the odd part `O(v)=(6b{+}4)v^3+A_1v`, `A_1=\tfrac32\beta^3-\tfrac32\beta^2-3\beta+2`,
using `v=-(N{-}2i)/2`, the whole odd contribution collapses to a **linear polynomial in
`r` with no binomials left**:

> `\displaystyle P_b\cdot\tfrac1{24}\sum_{i=0}^{r}O(v)\binom Ni \;=\; -\frac{(3b{+}2)\,r}{24}\;-\;\frac{b(3b{+}1)(b{+}2)}{48}` (exact, every `r,b`).

For the even part, the reflection `i\mapsto N{-}i` maps `\{i\ge r{+}1\}` onto
`\{i\le r{+}b\}`, so `\sum_{i\le r}E=\tfrac12[\sum_{i\le N}E-\sum_{i=r+1}^{r+b}E]`: the
full sum is `2^N` times an explicit polynomial in `N` (via `\mu_2,\mu_4`), and the strip
is exactly `b` terms whose prefactors `P_b\binom N{r+j}=\frac{r!(r{+}b)!}{(r{+}j)!(r{+}b{+}1{-}j)!}` are explicit rationals of size `O(1/r)`. Hence:

> **Theorem 3′ (mine; exact, every `r\ge0`, `b\ge0`).** With `\Phi_b(r):=P_b2^N=2\varphi_r\prod_{j=1}^b\frac{2r+2j}{2r+j+1}` and `E(v):=3v^4+(\tfrac92\beta^2-3\beta-3)v^2+(\tfrac3{16}\beta^4-\tfrac14\beta^3-\tfrac34\beta^2+\beta)`,
>
> `\displaystyle D^*_r(b)=\frac{\Phi_b(r)}{48}\Big[\frac{3N(3N{-}2)}{16}+\big(\tfrac92\beta^2-3\beta-3\big)\frac N4+\tfrac3{16}\beta^4-\tfrac14\beta^3-\tfrac34\beta^2+\beta\Big]`
> `\displaystyle\qquad\qquad-\;\frac1{48}\sum_{j=1}^{b}E\big(j-\tfrac\beta2\big)\frac{r!(r{+}b)!}{(r{+}j)!(r{+}b{+}1{-}j)!}\;-\;\frac{(3b{+}2)r}{24}\;-\;\frac{b(3b{+}1)(b{+}2)}{48}`.

At `b=0` the strip is empty, `\Phi_0=2\varphi_r`, `\beta=1`, `N=2r{+}1`, and the bracket
collapses to `\frac{12r(3r{+}1)}{16}`, giving exactly `\frac{r(3r{+}1)}{32}\varphi_r-\frac r{12}` — **Theorem 3 recovered**. ✔

| check | scope | result |
|---|---|---|
| Theorem 3′ vs the direct half-sum | `r=0..40`, `b=0..6` | **287** checks, **0** mismatches |
| the half-sum vs my ODE ladder | `r=0..30`, `b=0..6` | **217** checks, **0** mismatches |
| Theorem 3′ at `b=0` vs Theorem 3 | `r=0..40` | identical |

---

## Part 4. Theorem 4 — the two errors, and the corrected statement

### 4.1 The Wallis–Stirling step (`b=0`), re-derived

`\varphi_r=4^r(r!)^2/(2r{+}1)!=4^r/[(2r{+}1)\binom{2r}r]`. With
`\binom{2r}r=\frac{4^r}{\sqrt{\pi r}}\big(1-\frac1{8r}+O(r^{-2})\big)`,

`\varphi_r=\frac{\sqrt{\pi r}}{2r{+}1}\Big(1+\frac1{8r}+O(r^{-2})\Big)=\tfrac12\sqrt{\pi/r}\Big(1-\frac1{2r}+\frac1{8r}+O(r^{-2})\Big)=\tfrac12\sqrt{\pi/r}\Big(1-\frac3{8r}+O(r^{-2})\Big)` ✔

— the target's stated expansion, confirmed. Then

`\frac{r(3r{+}1)}{32}\varphi_r=\frac{\sqrt\pi}{64}\big(3r^{3/2}+r^{1/2}\big)\Big(1-\frac3{8r}+\cdots\Big)=\frac{3\sqrt\pi}{64}r^{3/2}+\frac{\sqrt\pi}{64}\Big(1-\frac98\Big)r^{1/2}+O(r^{-1/2})`,

and `1-\tfrac98=-\tfrac18`, so the `r^{1/2}` coefficient is
`\;\frac{\sqrt\pi}{64}\cdot\big(-\tfrac18\big)=-\frac{\sqrt\pi}{512}`.

### 4.2 F-1 — the third term is wrong

> **Document (Theorem 4):** `D^*_r(0)=\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}+\frac{\sqrt\pi}{128}r^{1/2}+O(1)`.
> **Correct:** `D^*_r(0)=\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}-\frac{\sqrt\pi}{512}r^{1/2}+O(1)`.

Measured `\big[D^*_r(0)-\frac{3\sqrt\pi}{64}r^{3/2}+\frac r{12}\big]/r^{1/2}`
(`mpmath` dps 60, my exact closed form):

| `r` | `10^2` | `10^3` | `10^4` | `10^5` | `10^6` | `10^7` | `10^8` |
|---|---|---|---|---|---|---|---|
| measured | `-0.0034037` | `-0.0034560` | `-0.0034612` | `-0.00346177` | `-0.00346182` | `-0.003461823` | `-0.0034618239` |

against `-\sqrt\pi/512=-0.0034618239` (**agreement to 10 significant figures**) and the
document's `+\sqrt\pi/128=+0.0138472957` (wrong sign, magnitude off by `4\times`).

**The document's own numerics already refute its own printed term.** §5.2 reports
`D^*_r(0)\big/\big[\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}\big]=0.99954,\,0.999957,\,0.9999958,\,0.99999958`
— approaching `1` strictly **from below**, which forces a *negative* next term. A
`+\sqrt\pi/128\,r^{1/2}` term would push that ratio above `1`. I reproduced all four of
those ratios and the whole §5.2 table exactly, so the numerics are right; only the
displayed asymptotic is wrong. Provenance: the string is hard-coded at
`asymptotics.py:173` and is never computed or tested anywhere in the directory.

**Severity: contained.** `Θ(r^{3/2})`, the leading constant `3\sqrt\pi/64`, Theorem 3
and the whole of §§3–5.1 are untouched. But it is a *stated theorem* that is false and
must be corrected before cataloguing.

### 4.3 F-2 — the general-`b` formula is wrong

The executive summary displays, for general `b`:
`D^*_r(b)=\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}+O(\sqrt r)`.

Theorem 3′ gives the linear term **exactly**, with no asymptotics: it is
`-\frac{(3b{+}2)r}{24}`, i.e.

| `b` | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| exact linear coefficient | `-1/12` | `-5/24` | `-1/3` | `-11/24` |

So for `b\ge1` the stated formula is off by `\frac{3b}{24}r=\frac{br}8`, which is
`Θ(br)` — not `O(\sqrt r)`. Measured `[D^*_r(b)-\frac{3\sqrt\pi}{64}r^{3/2}]/r`:

| `b` | `r=10^4` | `r=10^6` | `r=10^8` | `r=10^{10}` | `-(3b{+}2)/24` |
|---|---|---|---|---|---|
| 0 | `-0.083368` | `-0.0833368` | `-0.0833337` | `-0.08333337` | `-0.0833333` |
| 1 | `-0.205623` | `-0.2080601` | `-0.2083060` | `-0.20833060` | `-0.2083333` |
| 2 | `-0.325867` | `-0.3325764` | `-0.3332575` | `-0.33332575` | `-0.3333333` |
| 3 | `-0.444136` | `-0.4568860` | `-0.4581883` | `-0.45831883` | `-0.4583333` |

and `[D^*_r(0)-D^*_r(b)]/r\to b/8` (`0.12491,\,0.24976,\,0.37454` at `r=10^7` for `b=1,2,3`).

The document's §5.2 body text is *not* wrong — it only asserts
`D^*_r(b)\sim\frac{3\sqrt\pi}{64}r^{3/2}`. The flaw is entirely in the executive
summary's display, and in reading `-r/12` as `b`-independent.

### 4.4 F-3 — the `b\ge1` Stirling step, completed

The document's stated mechanism ("the factor `2^{b+1}` in `2^N` exactly cancels the
`2^{-(b+1)}` in the prefactor `r!(r{+}b)!/(2r{+}b{+}1)!`") is wrong as written: **that
prefactor has no power of 2 in it**. The real, exact cancellation is

`\displaystyle\rho_b(r):=2^b\frac{(r{+}b)!}{r!}\cdot\frac{(2r{+}1)!}{(2r{+}b{+}1)!}=\prod_{j=1}^b\frac{2r{+}2j}{2r{+}j{+}1}=1+\frac{b(b{-}1)}{4r}+O(r^{-2})\longrightarrow1`,

i.e. `2^b\cdot r^b/(2r)^b=1` to leading order. With Theorem 3′, `\Phi_b=2\varphi_r\rho_b=\sqrt{\pi/r}\big(1+\kappa/r+\cdots\big)`, `\kappa:=\frac{b(b{-}1)}4-\frac38`, and the even bracket expands to `\tfrac94r^2+c_1r+c_0` with `c_1=\tfrac94\beta^2+\tfrac34\beta-\tfrac94`. The leading term is `\frac{\sqrt\pi}{48}\cdot\frac94\,r^{3/2}=\frac{3\sqrt\pi}{64}r^{3/2}`, **independent of `b`** — and the strip contributes only `O(1/r)`, the odd part only the exact linear-plus-constant term. No hand-waving anywhere.

> **Corrected Theorem 4 (mine).**
> `\displaystyle D^*_r(b)=\frac{3\sqrt\pi}{64}r^{3/2}-\frac{(3b{+}2)r}{24}+\frac{\sqrt\pi}{48}\Big[\tfrac{45}{16}\beta^2-\tfrac{15}{16}\beta-\tfrac{63}{32}\Big]r^{1/2}+O(1)`, `\beta=b{+}1`.
> In particular `D^*_r(b)=Θ(r^{3/2})` with leading constant `\frac{3\sqrt\pi}{64}=0.0830837742611961\ldots` for **every** fixed `b` — now **PROVED, not PROVED-MODULO**.

Verification of the `r^{1/2}` coefficient (predicted vs measured at `r=10^8`):

| `b` | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| predicted | `-0.0034618239` | `+0.2734840903` | `+0.7581394401` | `+1.4505042256` |
| measured | `-0.00346182` | `+0.27345909` | `+0.75802278` | `+1.45019177` |

Log–log slopes: I reproduce the document's `1.5022 / 1.5054 / 1.5087 / 1.5119` on
`r=3\times10^4..10^5` exactly, and pushing to `r=10^9..10^{10}` gives
`1.500009 / 1.500024 / 1.500038 / 1.500052` — converging to `3/2` as claimed.

I also reproduce the document's entire §5.2 `D^*_r(b)` table exactly
(`1.78481, 1.19694, 0.830373, 0.593132` at `r=10`; `2619005, 2606593, 2594245, 2581962`
at `r=10^5`).

---

## Part 5. Theorem 2, Lemma 7, Proposition 6, `S_r`

### 5.1 Theorem 2 — the reduction is what is claimed

I re-derived the exact substitution myself. Writing
`R^{(3)}_r:=g_r-F_r-\frac1nG_r-\frac1{n^2}H_r`, `\varepsilon^{(3)}_r:=h_r-\hat H_r-\frac1nK_r-\frac1{n^2}L_r`,
substituting into `(*)` with **exact finite** Taylor expansions (all objects are
polynomials, so zero remainder), the `h^2` bracket comes out as
`t(H'-\tfrac12G''+\tfrac16F''')+(1{+}r{+}b)(H-G'+\tfrac12F'')-r[\tfrac12\hat H_{r-1}''+K_{r-1}'+L_{r-1}]`
— **which vanishes iff the `H_r` ODE holds.** So the target's statement that "item 1
becomes 'the `h^0`, `h^1` and `h^2` brackets vanish' — and the `h^2` bracket vanishing
*is* the `H_r` ODE" is exactly right, and it is the only new input. Items 2–4 of §4
(bounded degree; the exactly-zero contraction coefficient at `m=b{+}r{+}1`; the
falling-factorial/hockey-stick telescoping) carry over untouched, giving
`|R^{(3)}_r|\le[rC^{(3)}_{r-1}(b)+A^{(3)}_r(b)]/[(r{+}b{+}1)n^3]`.

On the `h`-side I get, from `(**)` and pure algebra,
`\varepsilon^{(3)}_r=h^3[rL_{r-1}(s,b{+}1)-(1{+}b{+}r)H_r(1{-}s,b{+}1)]+rh\,\varepsilon^{(3)}_{r-1}(a,b{+}1,n)+\big[(1{-}s)-h(1{+}b{+}r)\big]R^{(3)}_r(n{-}a,b{+}1,n)`,
the exact analogue of the predecessor's §6 identity.

**Machine confirmation, all from my own bivariate `Δ` construction:**

| check | scope | result |
|---|---|---|
| `h^0,h^1` brackets of `Δ_r` vanish identically in `t` | `r=0..16`, `b=0..4` | 85/85 |
| `h^0,h^1,h^2` brackets of `Δ^{(3)}_r` vanish identically in `t` | idem | 85/85 |
| lowest surviving `h`-power of `Δ^{(3)}_r` | `r=3..8` | exactly `3` |
| highest `h`-power of `Δ^{(3)}_r` | `r=3..8` | exactly `r` |
| `|R^{(3)}_r|\le D^{(3)}_r(b)/n^3`, every valid `m` | `n\le80`, `(r,b)` in 7 pairs | **0 violations** |
| `|\varepsilon^{(3)}_r|\le C^{(3)}_r(b)/n^3`, every valid `a` | idem | **0 violations** |
| `n^2\max_m|R_r|\to H_r(1,b)` | `(r,b)=(2,0),(3,0),(4,0),(5,0),(3,1),(4,1),(2,2)` | converges, monotonically, to the exact value |
| `n^3\max_m|R^{(3)}_r|` stabilises | `r=5,b=0`: `0.403508, 0.401062` at `n=40,80` | matches the document's `0.40351, 0.40106` |
| `R_1\equiv0`; `R_2\equiv1/(15n^2)`; `ψ_n^{(1)},ψ_n^{(2)}` | `n=6,7,9,11,15` | all exact |

> **Theorem 2: SOUND.** Two bookkeeping defects (O-5, O-6): §4 says "the identical
> algebra gives the identical recursion", but the stated `C^{(3)}_r(b)=B^{(3)}_r(b)+rC^{(3)}_{r-1}(b{+}1)+D^{(3)}_r(b{+}1)`
> has coefficient `1` on `D^{(3)}_r(b{+}1)` where the predecessor's §6 had `2`. The `1`
> *is* justified — by the target's own §6.1 `[0,1]` observation, in a later section —
> but the recursion is then not "identical". I computed both variants; both give finite
> constants and 0 violations, so nothing depends on it. Likewise §4's item 2 lists only
> `F_r,G_r,\hat H_r,K_r` as the bounded-degree polynomials; the three-term argument also
> needs `H_r` (degree `r{-}2`) and `L_r` (degree `r{-}1`), both trivially bounded.

### 5.2 Lemma 7 — SOUND

My own proof reproduces the target's. Coefficient of `s^j` in `p(1{-}s)` is
`(-1)^j\sum_{k\ge j}c_k\binom kj`; with `c_k\ge0` every contribution shares the sign
`(-1)^j`, so `\|p(1{-}\cdot)\|=\sum_k c_k\sum_j\binom kj=\sum_kc_k2^k=p(2)`. For the
second half, the `s^j` coefficient of `(1{-}s)q(s)` is `q_j-q_{j-1}`; if
`\mathrm{sign}(q_j)=(-1)^j` then `\mathrm{sign}(-q_{j-1})=(-1)^j` too, so
`\|(1{-}s)q\|=2\|q\|`. Both steps are correct. `\|\hat H_r(\cdot,b)\|=2F_r(2,b{+}1)`
follows.

**496 exact checks** (`r=0..30`, `b=0..3`), **0 failures**, covering
`\|F_r(1{-}\cdot,b)\|=F_r(2,b)`, `\|G_r(1{-}\cdot,b)\|=G_r(2,b)`,
`\|\hat H_r(\cdot,b)\|=2F_r(2,b{+}1)`, and my own extension
`\|H_r(1{-}\cdot,b)\|=H_r(2,b)` (`H_r` also has non-negative coefficients).

**The `(9/8)^r` mechanism — SOUND.** I re-derived
`F_r(2,0)=\frac{\varphi_r}{4^r}\sum_{i=0}^r2^{r-i}\binom{2r+1}i` (exact, `r=0..25`); the
summand ratio is `\tfrac12\frac{N-i}{i+1}=1` at `i=(N{-}2)/3=(2r{-}1)/3`, strictly
inside `[0,r]` for every `r\ge1`, and `Θ(\sqrt r)` standard deviations below the cut, so
the truncated sum captures all but an exponentially small share of `(3/2)^{2r+1}`,
giving `F_r(2,0)\sim\tfrac32\varphi_r(9/8)^r`. My measured
`F_r(2,0)/F_r(1,0)` ratios `1.135878, 1.127264, 1.125564` at `r=10,20,30` and
`/(9/8)^r` values `1.4164, 1.4797, 1.4947` **reproduce the document's table exactly**.

*Defect O-3:* the executive summary states `F_r(2,b)/F_r(1,b)=Θ((9/8)^r)` for general
`b`; §6.2 and scorecard row 14 derive it only at `b=0`. My numerics at `b=1,2,3`
(ratios `1.1239, 1.1224, 1.1208` at `r=40`) are consistent with `9/8` but converge more
slowly; the general-`b` claim is plausible and unproved.

### 5.3 Proposition 6 — SOUND, rigorous

Checked line by line, including the edge cases the brief flags:

- **`r/n\le r/(b{+}r{+}1)`.** Immediate from `n\ge b{+}r{+}1`. At `r=0` both sides are
  `0` (no division-by-zero issue: `b{+}r{+}1\ge1` always). ✔
- **Range compatibility.** The term being bounded is `\frac rn\varepsilon^h_{r-1}(a,b{+}1,n)`;
  the level-`(r{-}1)`, `b{+}1` inductive hypothesis is valid for `n\ge(b{+}1)+(r{-}1)+1=b{+}r{+}1`
  — **exactly the same range** on which `C'_r(b)` is asserted. No gap. ✔
- **`(1{-}s)-\frac{1{+}b{+}r}n=\frac{n-a-1-b-r}n\in[0,1]`.** Verified over *every* valid
  tuple `(n,a,b,r)` with `n\ge b{+}r{+}1`, `n\le39`, `b\le4`, `r\le5`: always in `[0,1]`.
  At the top boundary `a=n{-}b{-}r{-}1` it is **exactly `0`**, which is precisely what
  makes the out-of-domain reference `g_r(b{+}r{+}1,b{+}1)` harmless (the predecessor's
  post-adversarial note I-2). The same zero also covers the `n=b{+}r{+}1` corner, where
  `a=0` is the only valid `a` and coincides with the top boundary. ✔

So `C'_r(b)=B_r(b)+\frac r{b+r+1}C'_{r-1}(b{+}1)+D'_r(b{+}1)`,
`D'_r(b)=\frac{rC'_{r-1}(b)+A_r(b)}{r+b+1}` is a valid, strictly tighter recursion
proving the same Target Theorem. My values, from my own `Δ_r`:

| `r` | 6 | 10 | 16 | 20 | 30 | 45 |
|---|---|---|---|---|---|---|
| `D^*_r(0)` true | `0.7148` | `1.785` | `3.972` | `5.750` | `11.13` | `21.31` |
| `D'_r(0)` improved | `8.977` | `47.46` | `305.9` | `889.3` | `9895` | `2.73\times10^5` |
| `D_r(0)` original | `174.1` | `5.048\times10^5` | `1.529\times10^{12}` | `1.264\times10^{17}` | `7.086\times10^{30}` | — |

**Every entry reproduces the document's §6.1 table.** Ratios: `D_r/D_{r-1}=5.199,\,8.799,\,14.554,\,18.459,\,28.322` at `r=6,10,16,20,30` and `C_r/C_{r-1}=29.282` at `r=30` — matching the document's `14.55 / 18.46 / 28.32 / 29.28`. The improved ratio is `1.240059` at `r=45` — matching the document's `1.240`, and still decreasing.

### 5.4 §6.4 — the wave-8 referee's table, reproduced a third time

My independent bivariate `Δ_r`, `A_r`, `B_r`, `D_r`, `C_r` reproduce
`REFEREE_REPORT.md` §A.5 **exactly**: all six `A_r(0)/D_r(0)/C_r(0)` rows
(`0.133333/0.377778/2.233333` at `r=2` … `3.594572/174.072200/1200.680035` at `r=6`),
plus `D_2(2)=0.140952`, `D_3(1)=1.087000`, `D_3(5)=0.303012`, `D_4(3)=2.376231`,
`C_2(2)=1.406746`, `C_3(1)=6.955026`. The target's §6.4 claim is confirmed.

### 5.5 `S_r(b)` — the claims are correctly labelled

`S_r(b)` attained at the minimal state `n=m=b{+}r{+}1`: verified **exhaustively** over
every valid `m` and every `n\le40`, for `r=2..8`, `b=0,1` — 14/14, no exception. Ratios
`S_r(0)/D^*_r(0)=1.1056` at `r=4` and `1.3634` at `r=20`, and `S_r(0)/r^{3/2}=0.0452`
and `0.0877` — **all four reproduce the document's §5.3 table exactly**. The document's
Claim 5 is correctly marked NUMERICALLY CHARACTERIZED, and the honest caveat that
`S_r/D^*_r` is *not* proved bounded is appropriate — I confirm it is increasing
throughout my range too (`1.1056, 1.2199, 1.2857, 1.3634, 1.4194` at `r=4,8,12,20,30`).

### 5.6 §7.1 — independent reproduction of the cross-checks

I did the "seventh, self-contained" check my own way: exact Lagrange interpolation of
`ψ_n^{(K)}=g_K(n,0)` in `1/n` from `K{+}1` fitted `n`, then **out-of-sample validation
on five fresh `n`** (a wrong degree would fail there). All `K=1..7` pass, and every
`1/n^2` coefficient equals my `H_K(1,0)`:

| `K` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| `1/n^2` coeff | `0` | `1/15` | `5/28` | `103/315` | `1405/2772` | `1431/2002` | `2219/2340` |

My `K=3,4,5` full expansions equal the archive's PROVED `ψ_n^{(3)},ψ_n^{(4)},ψ_n^{(5)}`
term by term. On the `h`-side, my own simulator gives
`h_2(0,0)=\frac{11}{30}+\frac{13}{20n}+\frac{23}{60n^2}+\frac1{10n^3}` exactly at
`n=5,6,8,11,17`, and my ladder's `\hat H_2(0,0),K_2(0,0),L_2(0,0)` are `11/30, 13/20,
23/60` — the last from my own `L_r` relation.

---

## Part 6. Overclaim / bookkeeping audit (§9 Scorecard vs prose)

| id | where | issue | affects a truth value? |
|---|---|---|---|
| **O-1** | Executive summary item 2; §8.1 | The `b`-independence of `3\sqrt\pi/64` is asserted **flatly** ("the leading constant being the same for every fixed `b`", "plus `b`-independence of the leading constant") with no modulo, while scorecard row 9 marks the `b\ge1` case "PROVED-MODULO the Stirling step". Prose is unconditional where the scorecard is conditional — exactly the pattern this archive's discipline forbids. | no (and the claim is now **PROVED** by Part 3.3/4.4) |
| **O-2** | §6.3 summary table, row 1 | Marks "`D^*_r(b)` … `b`-independent" as "**PROVED** (mod. §8.4)". §8.4 is *only* about re-deriving §3.1; it does not cover row 9's Stirling modulo, which is silently dropped. | no |
| **O-3** | Executive summary item 4 | `F_r(2,b)/F_r(1,b)=Θ((9/8)^r)` stated for general `b`; derived only at `b=0` (row 14 is correctly scoped). | no |
| **O-4** | Corollary 1a | "`H_r(\cdot,b)` is **strictly** increasing on `[0,1]`" — false for `r\le2` (`H_0=H_1\equiv0`, `H_2` constant). Conclusion `\max|H_r|=H_r(1,b)` unaffected. | no |
| **O-5** | §4 | "the identical algebra gives the identical recursion" — the `C^{(3)}` recursion has coefficient `1` on `D^{(3)}_r(b{+}1)` vs the predecessor's `2` (justified, but elsewhere and unremarked). | no |
| **O-6** | §4 item 2 | The bounded-degree polynomial list omits `H_r` and `L_r`, which the three-term argument also needs. | no |
| **O-7** | §5.1 | "Combining, `4A_3-A_1=-2r(2r{+}1)\binom{2r}r`" is **false** under the `A_p:=\sum(N{-}2i)^p\binom Ni` convention the two preceding lines establish (I get `(2r{+}1)(16r{+}3)\binom{2r}r`); it is true only under an unstated `A_p:=\sum v^p\binom Ni` convention. Verified both readings numerically. Final `-r/12` is correct. | no |
| **O-8** | §3.2 | The three `K'` lines are annotated `-K'_{r-1}`; their values are `+[K'_{r-1}(1{-}t,b)]_k`. Also an unbalanced `]`. | no |

Everything else in the scorecard I judge **accurately labelled**. In particular rows 10,
11, 12, 14, 16 are correctly marked NUMERICALLY CHARACTERIZED / VERIFIED rather than
PROVED; rows 17–19 correctly OPEN / NOT CLOSED; row 20 correctly states that adversarial
verification had not been performed. §8.3's four open items do **not** overclaim — and
item 2 of that list is now *closed* by my Theorem 3′, which is a strengthening, not a
correction.

---

## Part 7. Scorecard (this referee's)

| # | Claim as stated in the target | My verdict |
|---|---|---|
| 1 | §3.1: the `ε²` matching — `H_r` ODE and `L_r` relation | **SOUND — CONFIRMED.** Re-derived from scratch by hand from the exact recursion; character-for-character identical. `ε⁰`/`ε¹` reproduce Facts 2/3 (5022+5022 exact checks, 0 mismatches; symbolic-`b` `r=0..8`). Base cases correct. |
| 2 | §3.2: the coefficient recursion **is** the ODE | **SOUND.** Independently hand-derived; every term agrees. Cosmetic mislabel O-8. |
| 3 | Theorem 1: `e_k^{(r)}(b)` closed form | **SOUND — PROVED.** 5022 exact checks (`r=0..30`, `b=0..8`); symbolic-`b` `r=0..8`; symbolic `r,k,b` both branches `=0` against **my own** recursion. Unconditional now that claim 1 is confirmed. |
| 4 | Corollary 1a: positivity, `\max=H_r(1,b)` | **SOUND**, with defect O-4 ("strictly increasing" false for `r\le2`). |
| 5 | Theorem 2: three-term existence, `O(1/n^3)` uniform | **SOUND.** The reduction is exactly as claimed (`h^2` bracket ⟺ `H_r` ODE, re-derived). Brackets vanish 85/85; 0 violations of both bounds over all `m`, all `a`, `n\le80`. Defects O-5, O-6. |
| 6 | Corollary 2a: `D^*_r(b)=H_r(1,b)` | **SOUND.** `n^2\max_m|R_r|\to H_r(1,b)` confirmed at 7 `(r,b)` pairs; `n^3\max|R^{(3)}|` stabilises (`0.403508, 0.401062` at `n=40,80`, `r=5,b=0`). |
| 7 | Theorem 3: `D^*_r(0)=\frac{r(3r{+}1)}{32}\varphi_r-\frac r{12}` | **SOUND — PROVED.** Own half-sum derivation; own **general** boundary identities I1/I3 proved by hand (7260+7260 exact checks) of which the target's two are specialisations; exact `r=0..80`. Notational defect O-7. |
| 8 | Corollary 3a: `D^*_0(0)=D^*_1(0)=0` | **SOUND.** |
| 9 | Theorem 4: `Θ(r^{3/2})`, constant `\frac{3\sqrt\pi}{64}`, `b`-independent, third term `+\frac{\sqrt\pi}{128}r^{1/2}` | **SPLIT.** `Θ(r^{3/2})` and the `b`-independent leading constant: **SOUND, and now PROVED outright** (Part 3.3/4.4 removes the Stirling modulo). Third term `+\frac{\sqrt\pi}{128}r^{1/2}`: **FLAWED (F-1)** — correct value `-\frac{\sqrt\pi}{512}r^{1/2}`. The `b\ge1` mechanism sketch: **FLAWED as written (F-3)**, though honestly flagged. |
| 9b | Exec. summary: `D^*_r(b)=\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}+O(\sqrt r)` for every `b` | **FLAWED (F-2).** Linear coefficient is exactly `-(3b{+}2)/24`; error is `Θ(br)`. |
| 10 | `S_r(b)` attained at `n=m=b{+}r{+}1` | **CONFIRMED numerically**, exhaustive `n\le40`, `r=2..8`, `b=0,1`. Correctly labelled "not proved". |
| 11 | Claim 5: `S_r=Θ(r^{3/2})`, `\approx1.7\times` constant | **CORRECTLY LABELLED** NUMERICALLY CHARACTERIZED. Two table entries reproduced exactly. |
| 12 | `D_r,C_r` factorial, `D_r/D_{r-1}\approx r` | **CONFIRMED.** My independent implementation reproduces the wave-8 §A.5 table exactly, and all quoted ratios. |
| 13 | Lemma 7 | **SOUND — PROVED.** 496 exact checks, 0 failures; own proof. |
| 14 | `(9/8)^r` cost; `F_r(2,0)\sim\frac32\varphi_r(9/8)^r` | **SOUND** at `b=0`, mechanism re-derived; measured table reproduced exactly. Defect O-3 for general `b`. |
| 15 | Proposition 6 rigorous | **SOUND.** All three inequality steps and every edge case checked, including `n=b{+}r{+}1` and `a=n{-}b{-}r{-}1`. Table reproduced exactly. |
| 16 | Improved bound geometric, ratio `\approx1.24` at `r=45` | **CONFIRMED**: `1.240059`. Correctly labelled. |
| 17–19 | open items | **CORRECTLY LABELLED**; item 18 (`b\ge1` closed form) is now **closed in the affirmative** by my Theorem 3′. |
| 20 | adversarial verification not performed | **NOW PERFORMED** — this report. |
| — | §6.4 reproduction of the wave-8 table | **CONFIRMED** by a third independent implementation. |
| — | §7.1 six/seven cross-checks | **CONFIRMED**, `K=1..7`, out-of-sample validated. |

---

## Part 8. Final verdicts

> **VERDICT A — §3.1 (the `ε²` matching), §3.2, Theorem 1, Corollary 1a, Theorem 2,
> Corollary 2a, Theorem 3, Corollary 3a, Lemma 7, Proposition 6, §6.4: SOUND.**
> Independently re-derived and independently re-implemented; every exact claim
> reproduced. The one derivation the document itself nominated for attack survives
> intact, and its own strongest internal check (the `ε⁰`/`ε¹` orders reproducing the
> already-PROVED `F_r`, `G_r`) reproduces for me as well. These may be catalogued.

> **VERDICT B — Theorem 4: FLAWED IN ITS STATED SUB-LEADING TERMS, SOUND IN ITS
> HEADLINE.** `D^*_r(b)=Θ(r^{3/2})` with leading constant `3\sqrt\pi/64`, the same for
> every fixed `b`, is correct — and is now **PROVED outright**, the "PROVED-MODULO the
> Stirling step" caveat of row 9 being removable via my exact Theorem 3′. But two
> displayed formulas are false and must be replaced before cataloguing:
> * the `r^{1/2}` coefficient at `b=0` is `-\sqrt\pi/512`, **not** `+\sqrt\pi/128`;
> * the linear coefficient at general `b` is `-(3b{+}2)/24`, **not** `-1/12`.
> Corrected statement: Part 4.4. Both corrections are exact, hand-derived, and confirmed
> numerically to 10 significant figures.

> **VERDICT C — §5.2's `b\ge1` Stirling sketch: SOUND WITH NAMED ISSUE.** The step was
> honestly flagged as incomplete (row 9), but the sketch given is *incorrect*, not
> merely abbreviated: the prefactor `r!(r{+}b)!/(2r{+}b{+}1)!` contains no `2^{-(b+1)}`.
> The correct cancellation is `\prod_{j=1}^b\frac{2r+2j}{2r+j+1}\to1`. Supplied and
> completed in Part 4.4.

> **VERDICT D — overclaiming: TWO REAL INSTANCES (O-1, O-2), six cosmetic.** The
> executive summary and §8.1 assert the `b`-independence flatly where row 9 marks it
> conditional, and §6.3's table marks it "PROVED (mod. §8.4)" while silently dropping
> row 9's separate modulo. Since the claim is now unconditionally proved, the remedy is
> to *upgrade row 9* rather than to weaken the prose — but the inconsistency was real
> at the time of writing and is exactly what this pass exists to catch.

> **RECOMMENDATION.** Adopt the corrected Theorem 4 and Theorem 3′ directly, fix F-1,
> F-2, F-3 and O-1…O-8, and then catalogue. No further adversarial round is needed on
> §§3–5.1, §6 or §7: those were re-derived from scratch here and are correct. A short
> confirmation round on the two *corrected* formulas would be prudent, since the
> correction is this referee's own work and has not itself been adversarially checked —
> though both are pinned by exact algebra (Theorem 3′, verified at 287+217 exact points)
> as well as by 10-significant-figure numerics.

---

## Part 9. Files in this directory

All written from scratch; all exact arithmetic except where flagged.

| file | contents | runtime |
|---|---|---|
| `ref_core.py` | own dense `Q[t]` polynomial type; the `(F,G,H,\hat H,K,L)` ladder built by solving **my own** `ε⁰/ε¹/ε²` ODEs; own exact `(a,b,r)` `Chain` simulator; the PROVED `c_k,d_k` and the claimed `e_k` as *comparison targets only* | — |
| `ref_bivar.py` | own bivariate `Q[t,h]` arithmetic; `Δ_r`, `Δ^{(3)}_r`; `A_r,B_r,D_r,C_r` at both orders, with switches for the `κ\in\{1,2\}` and (G1) variants | — |
| `ref_step4_helpers.py` | my exact general-`b` closed form `D^*_r(b)` (Theorem 3′) | — |
| `ref_step1_eps2.py` / `.log` | Part 1/2: `ε⁰`/`ε¹` validation (5022+5022), `ε²` vs Theorem 1 (5022), degrees, positivity, base cases, `h`-side cross-check | 8 s |
| `ref_step1b_symbolic.py` / `.log` | Part 2: symbolic-`b` ladder `r=0..8`; symbolic `r,k,b` recursion, both branches `=0` | 23 s |
| `ref_step2_thm3.py` / `.log` | Part 3: identities I1/I3 (7260+7260), even/odd split, even half-sum, Theorem 3 exact `r\le80` | 23 s |
| `ref_step3_thm2.py` / `.log` | Part 5.1/5.4: bracket vanishing, wave-8 table reproduction, `D^{(3)},C^{(3)}`, own finite-`n` simulator sweep | 9 s |
| `ref_step4_asympt.py` / `.log` | Part 3.3/4: Theorem 3′ verification (287+217), F-1, F-2, corrected Theorem 4, `mpmath` to `r=10^{10}` | 7 s |
| `ref_step5_bounds.py` / `.log` | Part 5.2/5.3/5.5: Lemma 7 (496), `(9/8)^r`, Proposition 6 edge cases and tables, exhaustive `S_r` scan | 45 s |
| `ref_step6_psi.py` / `.log` | Part 5.6: out-of-sample-validated `ψ_n^{(K)}` interpolation `K=1..7`; improved bound to `r=45` | 3 min |
| `ref_step7_misc.py` / `.log` | Part 6: O-3, O-4, O-7, O-8 and the `ρ_b(r)` correction to O/F-3 | 18 s |

Reproduce in this order: `python3 ref_step1_eps2.py 30 8`; `python3 ref_step1b_symbolic.py 8`;
`python3 ref_step2_thm3.py 80`; `python3 ref_step3_thm2.py 16 4`;
`python3 ref_step4_asympt.py 40`; `python3 ref_step5_bounds.py 30 40`;
`python3 ref_step6_psi.py 7 45`; `python3 ref_step7_misc.py`.
