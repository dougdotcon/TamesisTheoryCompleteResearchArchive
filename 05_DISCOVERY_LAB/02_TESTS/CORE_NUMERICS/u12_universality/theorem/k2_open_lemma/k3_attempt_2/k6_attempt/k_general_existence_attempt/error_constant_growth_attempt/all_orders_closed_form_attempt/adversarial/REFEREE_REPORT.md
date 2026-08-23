# Hostile-referee report on `all_orders_closed_form_attempt/ATTEMPT.md`

> **Mandate.** Independent adversarial re-verification of the wave-11 front-(b)
> document claiming an exact, finite, all-orders, general-`K`, general-`b` closed
> form (Theorem A) for the discrete `(a,b,r)` recursion, together with Theorem B,
> Theorem M, Corollaries A1–A3, the mandated `(I_r,M_r)` rung, and the `D^{*(p)}`
> sharp constants. Scope discipline: everything below was produced inside this
> `adversarial/` directory. **No file outside it was created, modified or read
> for anything but ground truth.** No git commit was made. No governance file was
> touched. Pure combinatorics on a discrete recursion; no external data.

> **Reuse discipline.** Not one of the target's scripts (`core.py`,
> `explore_multipliers.py`, `verify_closed_form.py`, `verify_symbolic.py`,
> `order_ladder.py`, `cross_checks.py`, `corollaries.py`, `dstar_orders.py`) was
> read, imported or executed at any point — before, during or after my own work.
> The transition rules were re-transcribed **from `k3_attempt_2/ATTEMPT.md` §2's
> own prose in their original `(a,b,r)` form**, deliberately *not* from the
> target's rewritten `(*)`/`(**)`, so that the target's own transcription is an
> object under test rather than an input. Everything else — the elementary proof,
> the order-`p` `ε`-matching, the ladder, the Stirling identification — was
> re-derived by hand first (recorded in Parts 1–3 below) and only then coded.

---

## Executive summary

**Theorem A survives.** I re-derived its §4.1 proof from scratch, by hand, before
looking at how the document does it; my derivation is line-for-line the same
argument, and every step of it checks out. The four facts (P1)–(P4) are correct
as stated. I then verified the assembled identities two further ways: symbolically
(including a **per-term identity at symbolic `r` *and* symbolic `j`**, which is
strictly stronger than the document's own per-`r` `r=0..9` checks), and
numerically against a from-scratch exact-`Fraction` simulator of the raw
recursion — **215 070 exact checks, 0 mismatches**. The document's central claim
is sound, and with it Theorem B, Theorem M, and Corollaries A1/A2/A3.

**The `ε`-machinery survives too, including the flagged sign.** I re-derived the
order-`p` receiver ODE and source relation independently. **The signs in the
document's two boxed relations are correct**, including the `d/ds=-d/dt`
substitution the author flags as the place he had previously erred. Its `p=0,1,2`
instances do reproduce the four published statements **character-for-character** —
I checked against the actual predecessor texts, not the document's rendering of
them. The `p=3` rung `(I_r,M_r)` is correct and `M_2(0,0)=1/10`, the one place an
independent already-PROVED fact pins the new order.

**Theorem M holds at every order I could reach** (`p=0..8`, beyond the `p=4,5,6`
I was asked to reach), and the §3.2 resummation argument is airtight: the
`(j,k)↔(p,k)` reindexing is a clean bijection with nothing double-counted or
dropped, and **the claimed `g`/`h` termination asymmetry (`p=r` vs `p=r+1`) is
real, not a typo** — I derived its cause independently.

**One claim is FLAWED, and it is a *negative* claim.** §6.3 item 3 and scorecard
row 13 assert that a `{r^q\varphi_r\}\cup\{r^q\}` basis fails out of sample for
`D^{*(p)}_r(b)` at **`b=1,2,3`**. It does not fail at `b=1`. At `b=1` the basis
represents the answer **exactly**, for `p=1,2,3,4`, with `0` failures over
`r=0..400`; I supply the four closed forms, and the `p=2` one is not merely fitted
but **already PROVED** — it is the wave-10 referee's Theorem 3′ specialised to
`b=1`. The correct statement is "fails for `b\ge2`", and there is a clean
structural reason (Part 5.2). I also reproduce the document's own reported
"54–56 failures out of 61" **exactly** — as the `b=2` and `b=3` numbers, which
strongly indicates `b=1` was swept into a summary range it does not belong to.

**Two things the document correctly declines to claim, I was able to upgrade.**
I carried out the proof route the document names in §6.3 item 4 but explicitly
does not execute, and thereby moved `D^{*(p)}_r(0)` at `p=3,4,5` from NUMERICALLY
VERIFIED to **PROVED** (Part 6), and row 12's `(2p{-}1)!!/(4^pp!)` leading
coefficient from NUMERICALLY CHARACTERIZED to **PROVED** (Part 7). I also give
new `p=6,7` forms.

**Honesty audit: clean.** I looked specifically for the wave-10 failure mode
(conditional "PROVED given claim X" in the scorecard silently becoming flat
"PROVED" in the body). **I did not find it here.** Rows 4, 5, 8, 9, 10 carry
"PROVED given claim 6" and the body never upgrades them. Rows 11 and 12 are
labelled honestly and conservatively — indeed *too* conservatively, per Parts 6–7.
Three minor labelling nits are recorded in Part 8; none is substantive.

### Verdict, split by sub-claim

| sub-claim | verdict |
|---|---|
| **Theorem A** (§4.1 proof, facts P1–P4, assembled `(*)`) | **SOUND** — independently re-derived and re-proved |
| **Theorem B** and its domain caveat | **SOUND** — caveat verified as a strict biconditional |
| **§2.1 order-`p` ODE / source relation, incl. the flagged signs** | **SOUND** — independently re-derived |
| **§2.2 `p=0,1,2` reproduce the published statements** | **SOUND** — character-for-character, checked against the source texts |
| **§2.3 `(I_r,M_r)`, the mandated rung; `M_2(0,0)=1/10`** | **SOUND** |
| **Theorem M**, all orders; §3.2 resummation; `h`-side asymmetry | **SOUND** |
| **Corollaries A1 / A2 / A3**; `\psi_n^{(6,7,8)}` | **SOUND** — reproduced from my own brute force |
| **`D^{*(p)}_r(0)`, `p=3,4,5`** (labelled NUMERICALLY VERIFIED) | **SOUND, and now UPGRADED to PROVED** by this report |
| leading coefficient `(2p{-}1)!!/(4^pp!)` (row 12) | **SOUND, and now UPGRADED to PROVED** |
| **§6.3 item 3 / row 13, the `b\ge1` negative claim** | **FLAWED** — false at `b=1`; corrected statement + 4 closed forms supplied |
| scope/honesty discipline of §6 and §7 | **SOUND** (3 minor nits) |

**Recommendation.** Theorem A, Theorem B, Theorem M and Corollaries A1–A3 are
correct and may be catalogued. Row 13 must be restated as `b\ge2` and the `b=1`
closed forms added. Rows 11 and 12 may be promoted to PROVED with Parts 6–7 as
the argument.

---

## Part 0. What I treated as ground truth, and whether the document cites it accurately

I re-verified only that the citations are faithful; the internal correctness of
these predecessor results was settled by their own adversarial passes.

| cited as | source, verbatim | accurate? |
|---|---|---|
| transition rules `(*)`, `(**)` | `k3_attempt_2/ATTEMPT.md` §2 Proposition, in `(a,b,r)` form | **YES** — I re-derived the rewrite (below) and it is exact |
| `c_k^{(r)}(b)=\frac{r!}{(r-k)!}\prod_{i=1}^{k+1}(r{+}b{+}i)^{-1}` | `k6_attempt/ATTEMPT.md` §2.3, "PROVED, general `r`" | **YES** |
| `d_k^{(r)}(b)=\binom{k+2}2\frac{r!}{(r-k-1)!}\prod_{i=1}^{k+2}(\cdot)^{-1}` | `k6_attempt/ATTEMPT.md` line 575 | **YES** |
| `e_k^{(r)}(b)=\frac{(3k+8)(k+1)(k+2)(k+3)}{24}\cdots` | `error_constant_growth_attempt/ATTEMPT.md` Theorem 1 | **YES** |
| Fact 2 (`F_r` ODE) | `k6_attempt` line 344 | **YES**, character-for-character |
| Fact 3 (`G_r` ODE) | `k6_attempt` line 517 | **YES**, character-for-character |
| `H_r` ODE | `error_constant_growth_attempt` line 224 | **YES**, character-for-character |
| `L_r` relation | `error_constant_growth_attempt` line 232 | **YES**, character-for-character |
| `\psi_n^{(3),R}=\frac{11}{30}+\frac{13}{20n}+\frac{23}{60n^2}+\frac1{10n^3}` | `k3_attempt_2/ATTEMPT.md` line 341, PROVED (its row 7) | **YES** |
| `g_6(7,0)=355081/823543` (brute force) | reproduced by my own simulator | **YES** |
| Estágio 8's `1431/2002`, `2219/2340` | `error_constant_growth_attempt` line 429 | **YES** |
| Theorem 3′ (wave-10 referee) | `error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3 | **YES** — I transcribed and confirmed it exactly (Part 5.1) |

**The rewrite `(a,b,r)\to(m,b)` is exact.** With `m:=n-a`, `g_r(m,b):=g(n{-}m,b,r)`,
`h_r(a,b):=h(a,b,r)`: the non-source rule `g=\frac1m+\frac rm h(a{+}1,b,r{-}1)+\frac{m-1-r-b}m g(a{+}1,b,r)`
multiplied by `m` and rearranged is exactly `(*)`; the source rule is `(**)` with
`\frac{n-1-a-b-r}n=(1{-}s)-\frac{1+b+r}n`. I did not take this on trust — my
simulator implements the **original** rules and the rewritten pair was checked
against it at 25 871 states per rule (Part 1.4).

---

## Part 1. Theorem A — the elementary proof, re-derived from scratch

This is the check the document itself says matters most, and I gave it the most
weight. I worked the proof out on my own before comparing.

### 1.1 The four facts

Write `A_j:=A^{(r)}_j(b)=\frac{r!}{(r-j)!}\Big/\prod_{i=1}^{j+1}(r{+}b{+}i)` and
`P_j(m):=(m{+}j)!/m!=\prod_{i=1}^{j}(m{+}i)`, `P_0\equiv1`.

**(P1)** `A_j\,(j{+}1{+}r{+}b)=r\,A^{(r-1)}_{j-1}(b{+}1)`, for `j\ge1`.

*My derivation.* The denominator `\prod_{i=1}^{j+1}(r{+}b{+}i)` has last factor
`(r{+}b{+}j{+}1)=(j{+}1{+}r{+}b)`, so multiplying by it simply deletes that factor:
`A_j(j{+}1{+}r{+}b)=\frac{r!}{(r-j)!}\big/\prod_{i=1}^{j}(r{+}b{+}i)`.
On the other side, `A^{(r-1)}_{j-1}(b{+}1)=\frac{(r-1)!}{(r-j)!}\big/\prod_{i=1}^{j}\big((r{-}1)+(b{+}1)+i\big)=\frac{(r-1)!}{(r-j)!}\big/\prod_{i=1}^{j}(r{+}b{+}i)`,
and the level shift `r\to r{-}1` together with `b\to b{+}1` leaves `r+b` invariant —
*that* is the mechanism. Multiplying by `r` turns `(r{-}1)!` into `r!`. The two
sides coincide. `\square`

The invariance of `r+b` under the simultaneous shift is the whole content of the
identity, and it is exactly the invariance `k6_attempt` §2.3 already exploited to
unroll `c_k^{(r)}(b)` (its base case is "independent of `k`, since
`1+(r{-}k)+(b{+}k)=1+r+b`"). So (P1) is not a new coincidence; it is the same
structural fact one level up. **Confirmed symbolically in `r,j,b`** (Gamma form,
`\mathrm{simplify}(\mathrm{LHS}-\mathrm{RHS})=0`) and again as honest finite
products for `r\le12`, `j\le r`, `b\le5`.

**(P2)** `(1{+}r{+}b)A_0=(1{+}r{+}b)\cdot\frac{1}{r{+}b{+}1}=1`. Immediate.

**(P3)** For `j\ge1`, with `P_j(m)=(m{+}1)\cdots(m{+}j)` and
`P_j(m{-}1)=m(m{+}1)\cdots(m{+}j{-}1)`:
`P_j(m{-}1)=m\,P_{j-1}(m)` by inspection, and
`P_j(m)-P_j(m{-}1)=(m{+}1)\cdots(m{+}j{-}1)\big[(m{+}j)-m\big]=j\,P_{j-1}(m)`.
Both correct. Confirmed symbolically (Gamma form, symbolic `j`) and as expanded
polynomials in `m` for `j=1..14`.

**(P4)** Well-foundedness. I checked this in the **original** `(a,b,r)`
coordinates, where the claim is cleanest. Every recursive call increases `a+b` by
exactly `1`:

| rule | call | effect on `(a,b,r)` |
|---|---|---|
| `(*)` | `g_r(m{-}1,b)` | `a\to a{+}1`, `b` same, `r` same |
| `(*)` | `h_{r-1}(n{-}m{+}1,b)` | `a\to a{+}1`, `b` same, `r\to r{-}1` |
| `(**)` | `h_{r-1}(a,b{+}1)` | `a` same, `b\to b{+}1`, `r\to r{-}1` |
| `(**)` | `g_r(n{-}a,b{+}1)` | `a` same, `b\to b{+}1`, `r` same |

and `a{+}b\le n{-}1{-}r` is bounded above, so the induction (on `r`, and within
each `r` downward on `a{+}b`) terminates. At the top `a{+}b{+}r=n{-}1` both
"same-`r`" coefficients `\frac{m-1-r-b}m` and `\frac{n-1-a-b-r}n` are exactly `0`
(Part 1.3), so no boundary condition is needed. **(P4) is correct as stated.**

I also confirmed the ladder is genuinely self-starting: at `r=0`, `(*)` reads
`m[g_0(m,b)-g_0(m{-}1,b)]+(1{+}b)g_0(m{-}1,b)=1`; at the minimum `m=b{+}1` the
coefficient `\frac{m-1-b}m` vanishes, giving `g_0(b{+}1,b)=\frac1{b+1}`, and the
induction `g_0(m,b)=\frac{m-1-b}{m}\cdot\frac1{b+1}+\frac1m=\frac1{b+1}` holds.
So `g_0\equiv1/(b{+}1)` is a **consequence**, not an input.

### 1.2 The assembled identity

Define `\hat g_r(m,b):=\sum_{j=0}^rA_jP_j(m)/n^j` and
`\hat h_r(a,b):=\frac{n-a+1}n\hat g_r(n{-}a{+}1,b{+}1)`. Then by (P3), for `j\ge1`,

`m[P_j(m)-P_j(m{-}1)]+(1{+}r{+}b)P_j(m{-}1)=j\,m\,P_{j-1}(m)+(1{+}r{+}b)m\,P_{j-1}(m)=(j{+}1{+}r{+}b)\,m\,P_{j-1}(m)`,

while the `j=0` term contributes `(1{+}r{+}b)A_0=1` by (P2). Applying (P1),

`\displaystyle\sum_{j=1}^{r}A_j(j{+}1{+}r{+}b)\frac{mP_{j-1}(m)}{n^j}=\frac{rm}{n}\sum_{l=0}^{r-1}A^{(r-1)}_l(b{+}1)\frac{P_l(m)}{n^l}=\frac{rm}{n}\hat g_{r-1}(m,b{+}1)`,

and by definition `\hat h_{r-1}(n{-}m{+}1,b)=\frac mn\hat g_{r-1}(m,b{+}1)` — the
arguments match because `n-(n{-}m{+}1)+1=m`. Hence `(*)` holds. **This is a
polynomial identity in `m`, valid at every integer `m`**, which matters in 1.3.

For `(**)`: apply the display at `(r,\,m'=n{-}a{+}1,\,b{+}1)`. Then `m'-1=n-a` and
`n-m'+1=a`, so

`(n{-}a{+}1)[\hat g_r(n{-}a{+}1,b{+}1)-\hat g_r(n{-}a,b{+}1)]+(2{+}r{+}b)\hat g_r(n{-}a,b{+}1)=1+r\hat h_{r-1}(a,b{+}1)`.

Dividing by `n` and recognising the first term as `\hat h_r(a,b)`:

`\displaystyle\hat h_r(a,b)=\frac1n+\frac rn\hat h_{r-1}(a,b{+}1)+\Big[\frac{n-a+1}{n}-\frac{2+r+b}{n}\Big]\hat g_r(n{-}a,b{+}1)`,

and `\frac{n-a+1-2-r-b}{n}=\frac{n-1-a-b-r}{n}=(1{-}s)-\frac{1+b+r}{n}`. That is
exactly `(**)`. **The document's "`(\ast\ast)` is the same identity re-indexed"
is correct**, and I reproduce its stated coefficient `\frac{n-1-a-b-r}n` exactly.

By (P4) the system has a unique solution, so `\hat g=g`, `\hat h=h`. `\blacksquare`

### 1.3 The domain caveat — verified as a strict biconditional

This was flagged to me as the subtle point, and it is genuinely two distinct
facts, not one:

- **(D1)** in `(*)`, `g_r(m,b)` refers to `g_r(m{-}1,b)`; at the minimum
  `m=b{+}r{+}1` the reference `m{-}1=b{+}r` is one below `g_r(\cdot,b)`'s domain;
- **(D2)** in `(**)`, `h_r(a,b)` refers to `g_r(n{-}a,b{+}1)`, whose domain is
  `m\ge(b{+}1){+}r{+}1=b{+}r{+}2`; at the maximum `a=n{-}b{-}r{-}1` the reference
  is `m=b{+}r{+}1`, one below **that** domain.

Both are "one below the minimum", but *for different `b`*, which is precisely why
an implementation that guards only `(*)` still diverges on `(**)`. I tested the
biconditional over `n=2..29`, all `r`, all `b`, every valid state:

```
(D1)  4494 out-of-domain references, ALL with coefficient exactly 0
     31465 in-domain references,     NONE with coefficient 0
(D2)  4494 out-of-domain references, ALL with coefficient exactly 0
     31465 in-domain references,     NONE with coefficient 0
VIOLATIONS: 0
```

So the zero coefficient and the out-of-domain reference coincide **exactly** — it
is not a numerical accident that happens to wash out, it is an identity:
`\frac{n-1-a-b-r}{n}=0\iff a{+}b{+}r=n{-}1\iff n{-}a=b{+}r{+}1`. Independently,
`k3_attempt_2/ATTEMPT.md` §2 itself adopts the convention `g(b{+}r,b,r):=0` for
exactly this state and notes it "is not an extra assumption, it is exactly what
the recursion's own coefficient forces". Both routes agree. **The caveat's
reasoning is sound.**

- **(D3)** Theorem B at `a=0` evaluates `\hat g_r(n{+}1,b{+}1)`, outside the
  probabilistic domain. **This is not a defect.** `\hat g` is a polynomial
  expression; the §4.1 identity is a polynomial identity in `m` (Part 1.2), so it
  holds at `m=n{+}1`; and the raw recursion itself never evaluates `g_r` out of
  domain. I confirmed `h_r(0,b)` (true probability, from the raw recursion)
  `=\frac{n+1}{n}\hat g_r(n{+}1,b{+}1)` at 556 exact points, 0 mismatches. The
  document's handling of this is correct and its cross-reference to the wave-8
  I-2 precedent is apt.

### 1.4 Numerical confirmation, from a from-scratch simulator

My simulator implements the **original** `(a,b,r)` rules with exact `Fraction`
arithmetic, iteratively (fill by decreasing `a{+}b`), and **asserts** at every
step that a zero coefficient coincides with an absent (out-of-domain) state.

| check | scope | count | mismatches |
|---|---|---|---|
| Theorem A vs raw simulator | `n\le31, r\le10, b\le8`, every valid `m` | 25 871 | **0** |
| Theorem B vs raw simulator | same, every valid `a` | 25 871 | **0** |
| Theorem A binomial form | same | 25 871 | **0** |
| Theorem B binomial form | same | 25 871 | **0** |
| rewritten `(*)` vs original rules | same | 25 871 | **0** |
| rewritten `(**)` vs original rules | same | 25 871 | **0** |
| *(second, overlapping sweep `n\le24,r\le8,b\le6`)* | | 59 844 | **0** |
| **total** | | **215 070** | **0** |

### 1.5 Symbolic confirmation — and a strengthening

`ref_symbolic.log`:

| check | result |
|---|---|
| (P1) symbolic in `r,j,b` (Gamma form) | `0` |
| (P1) as honest finite products, `r\le12,j\le r,b\le5` | `0` failures |
| (P2) | `0` |
| (P3a), (P3b) symbolic in `m,j` | `0` |
| (P3) as expanded polynomials in `m`, `j=1..14` | `0` failures |
| **the per-term `j\ge1` identity at symbolic `r,j,b,m,n` simultaneously** | **`0`** |
| assembled `(*)`, symbolic `m,n,b`, `r=0..9` | `0` failures |
| assembled `(**)`, symbolic `a,n,b`, `r=0..9` | `0` failures |

The bolded row is a **strengthening of the document's own verification**. The
document checks `(*)` per-`r` for `r=0..9` (its S5). Because the proof of Part 1.2
reduces `(*)` to a single per-term identity, and that identity holds with `r` and
`j` both symbolic, the proof is verified **at all `r` simultaneously**, not merely
for ten of them. The document's Theorem A does not depend on this, but its
verification record is strictly weaker than it needed to be.

---

## Part 2. §2.1 — the general-order `ε`-matching, re-derived from scratch

I derived the two boxed relations myself before reading the document's derivation,
precisely because §6.4 warns that a sign is easy to get wrong there.

### 2.1 The receiver ODE

`\varepsilon=1/n`, `t=m/n`, so `(m{-}1)/n=t-\varepsilon` **exactly**; and for
`h_{r-1}(n{-}m{+}1,b)` the argument is `s'=(n{-}m{+}1)/n=(1{-}t)+\varepsilon`,
also exact. Each `\Phi^{[p]}_r(\cdot,b)` is a polynomial of bounded degree, so
every Taylor expansion below is a **finite identity with zero remainder**.

*Term 1.* `m[g_r(m,b)-g_r(m{-}1,b)]=\frac t\varepsilon\sum_p\varepsilon^p[\Phi^{[p]}(t)-\Phi^{[p]}(t{-}\varepsilon)]`
and `\Phi^{[p]}(t)-\Phi^{[p]}(t{-}\varepsilon)=\sum_{i\ge1}\frac{(-1)^{i+1}}{i!}\varepsilon^i(\Phi^{[p]})^{(i)}(t)`,
so the `\varepsilon^p` coefficient is `t\sum_{i=1}^{p+1}\frac{(-1)^{i+1}}{i!}(\Phi^{[p+1-i]})^{(i)}(t)`.
Its `i=1` piece is `t(\Phi^{[p]})'(t)` — the term that stays on the left. Moving
the rest to the right **flips the sign**, giving
`+\,t\sum_{i=2}^{p+1}\frac{(-1)^{i}}{i!}(\Phi^{[p+1-i]})^{(i)}`. ✔ matches the box.

*Term 2.* `(1{+}r{+}b)g_r(m{-}1,b)` has `\varepsilon^p` coefficient
`(1{+}r{+}b)\sum_{i=0}^{p}\frac{(-1)^i}{i!}(\Phi^{[p-i]})^{(i)}`. Its `i=0` piece
is `(1{+}r{+}b)\Phi^{[p]}`, which stays left; moving the rest right flips the sign
to `+(1{+}r{+}b)\sum_{i=1}^{p}\frac{(-1)^{i+1}}{i!}(\Phi^{[p-i]})^{(i)}`. ✔

*Term 3 — the sign the author flags.* With `\eta^{[p]}_r(t,b):=\Psi^{[p]}_r(1{-}t,b)`,
differentiating w.r.t. `t` gives `\frac{d}{dt}\eta^{[p]}(t)=-\Psi^{[p]\prime}(1{-}t)`
and hence, by induction,
`\;(\Psi^{[p]})^{(i)}(1{-}t)=(-1)^i(\eta^{[p]})^{(i)}(t)`.
Expanding `\Psi^{[p]}_{r-1}((1{-}t){+}\varepsilon)=\sum_i\frac{\varepsilon^i}{i!}(\Psi^{[p]}_{r-1})^{(i)}(1{-}t)`
and substituting gives `\varepsilon^p` coefficient
`r\sum_{i=0}^{p}\frac{(-1)^i}{i!}(\eta^{[p-i]}_{r-1})^{(i)}(t,b)`. ✔ matches.

**So the document's boxed order-`p` receiver ODE is correct, signs included.**

A useful cross-check on exactly that sign: substituting back
`(\eta^{[q]})^{(i)}(t)=(-1)^i(\Psi^{[q]})^{(i)}(1{-}t)` turns the `r`-block into
`\;r\sum_{i=0}^{p}\frac{1}{i!}(\Psi^{[p-i]}_{r-1})^{(i)}(1{-}t,b)` — **all signs
positive**. This is the form in which the published `p=1,2` instances are written
(`+r\hat H'_{r-1}`, `+r[\tfrac12\hat H''_{r-1}{+}K'_{r-1}{+}L_{r-1}]`), and it
agrees. Had the `d/ds=-d/dt` sign been wrong, this block would have alternated.

### 2.2 The source relation

`(**)` needs no expansion: `a=ns` and `(n{-}a)/n=1{-}s` are exact. Matching
`\varepsilon^p` in
`h_r=\varepsilon+\varepsilon r\,h_{r-1}(a,b{+}1)+[(1{-}s)-(1{+}b{+}r)\varepsilon]g_r(n{-}a,b{+}1)`
gives directly

`\Psi^{[p]}_r(s,b)=[p{=}1]+r\Psi^{[p-1]}_{r-1}(s,b{+}1)+(1{-}s)\Phi^{[p]}_r(1{-}s,b{+}1)-(1{+}b{+}r)\Phi^{[p-1]}_r(1{-}s,b{+}1)`,

and setting `s=1{-}t` yields the `\eta` form. ✔ Both match the document exactly.

### 2.3 The `p=0,1,2` instances, against the source texts

I instantiated my own boxed relations and compared with the **predecessor
documents themselves**, not the target's table:

| `p` | my instantiation | source | verdict |
|---|---|---|---|
| 0 | `tF_r'+(1{+}r{+}b)F_r=1+r\hat H_{r-1}(1{-}t,b)` | `k6_attempt` line 344 (Fact 2) | **identical** |
| 1 | `tG_r'+(1{+}r{+}b)G_r=r\hat H_{r-1}'+rK_{r-1}+\tfrac t2F_r''+(1{+}r{+}b)F_r'` | `k6_attempt` line 517 (Fact 3) | **identical** |
| 2 | `tH_r'+(1{+}r{+}b)H_r=r[\tfrac12\hat H_{r-1}''{+}K_{r-1}'{+}L_{r-1}]+\tfrac t2G_r''-\tfrac t6F_r'''+(1{+}r{+}b)[G_r'{-}\tfrac12F_r'']` | `error_constant_growth_attempt` line 224 | **identical** |
| 2 (src) | `L_r(s,b)=rK_{r-1}(s,b{+}1)+(1{-}s)H_r(1{-}s,b{+}1)-(1{+}b{+}r)G_r(1{-}s,b{+}1)` | ibid. line 232 | **identical** |

The document's "character-for-character" claim is accurate.

### 2.4 The `p=3` rung, and the one independent constraint

Instantiating at `p=3` I get, independently:

`t I_r'+(1{+}r{+}b)I_r=r\big[\tfrac16\hat H_{r-1}'''+\tfrac12K_{r-1}''+L_{r-1}'+M_{r-1}\big]+t\big[\tfrac12H_r''-\tfrac16G_r'''+\tfrac1{24}F_r''''\big]+(1{+}r{+}b)\big[H_r'-\tfrac12G_r''+\tfrac16F_r'''\big]`

`M_r(s,b)=rL_{r-1}(s,b{+}1)+(1{-}s)I_r(1{-}s,b{+}1)-(1{+}b{+}r)H_r(1{-}s,b{+}1)`

— **identical to the document's two NEW boxes.** (Note the `r`-block signs are
all `+` after the `\eta\to\Psi` conversion, as in 2.1.)

I then built my own ladder (Part 3) and evaluated the source side at `r=2`, `b=0`:

| object | my ladder | required by PROVED `\psi_n^{(3),R}` |
|---|---|---|
| `\hat H_2(0,0)` | `11/30` | `11/30` ✔ |
| `K_2(0,0)` | `13/20` | `13/20` ✔ |
| `L_2(0,0)` | `23/60` | `23/60` ✔ |
| **`M_2(0,0)`** | **`1/10`** | **`1/10`** ✔ |

I also confirmed `M_2(0,0)=1/10` **by hand**, without the ladder, from Theorem M's
`h`-side form: at `p=3,r=2,b=0` the only surviving term is `k=0`, giving
`A^{(2)}_2(1)\,c(4,1)=\frac{2}{4\cdot5\cdot6}\cdot 6=\frac1{60}\cdot6=\frac1{10}`.
This is the single place where a fact established independently of this entire
line of work pins the new order, and it lands exactly.

My ladder also reproduces the document's printed low `I_r`:
`I_0=I_1=I_2=0`, `I_3(t,0)=3/70`, `I_4(t,0)=3/35+\tfrac5{63}t`,
`I_5(t,0)=5/42+\tfrac{25}{126}t+\tfrac{25}{308}t^2`. ✔

---

## Part 3. My independent ladder, and Theorem M

`ref_ladder.py` solves the order-`p` ODE ladder I derived in Part 2, with my own
polynomial type over `Fraction`. Solving is coefficient-wise: if the RHS is
`\sum_k\rho_kt^k` then `\Phi^{[p]}_r=\sum_k\frac{\rho_k}{k+1+r+b}t^k`, and
`k{+}1{+}r{+}b>0` always, so the solution is unique. **Nothing is hard-coded**:
at `r=0` the `\eta`-block carries the prefactor `r=0`, and the ladder returns
`\Phi^{[0]}_0=1/(b{+}1)`, `\Phi^{[p\ge1]}_0=0`, `\Psi^{[0]}_0=(1{-}s)/(b{+}2)`,
`\Psi^{[1]}_0=1/(b{+}2)`, `\Psi^{[p\ge2]}_0=0` — i.e. exactly
`g_0=1/(b{+}1)` and `h_0(a,b)=(n{-}a{+}1)/(n(b{+}2))`, as the document says.

| check | scope | count | mismatches |
|---|---|---|---|
| ladder order 0/1/2 vs **PROVED** `c_k,d_k,e_k` | `r\le12,b\le4`, all `k` | 1 755 | **0** |
| `I_r` closed form vs ladder | `r\le21,b\le6`, all `k` | 2 079 | **0** |
| `M_r` closed form vs ladder | same | 2 079 | **0** |
| **Theorem M** vs ladder | **`p=0..8`**, `r\le16`, `b\le5`, all `k` | 10 098 | **0** |
| `\deg\Phi^{[p]}_r=r{-}p`; `\Phi^{[p]}_r\equiv0` for `p>r` | same | — | **0** violations |
| `h`-side closed form vs ladder | `p\le9`, `r\le10`, `b\le3` | 3 960 | **0** |
| multiplier table `p\le7,k\le6` | each entry read from 20 distinct `(r,b)` | 56 entries | **0** disagreements |

The §3.1 multiplier table is reproduced **entry for entry**, all 56 entries, and
the `r,b`-independence holds at every `(r,b)` I tried. Column `k=0` is `p!=c(p{+}1,1)`
and column `k=1` is `(p{+}1)!H_{p+1}=c(p{+}2,2)`, both confirmed.

### 3.1 The four Stirling identifications

Verified exactly for `N\le29` with my own `c(N,M)=c(N{-}1,M{-}1)+(N{-}1)c(N{-}1,M)`
implementation (itself cross-checked against `sympy` for `N\le17`):

`c(N,N)=1`, `c(N,N{-}1)=\binom N2`, `c(N,N{-}2)=\tfrac{3N-1}4\binom N3`,
`c(N,N{-}3)=\binom N2\binom N4`.

And the two that matter for consistency with published work:
`c(k{+}2,k{+}1)=\binom{k+2}2` **is** the published `d_k` multiplier, and
`c(k{+}3,k{+}1)=\tfrac{(3k+8)(k+1)(k+2)(k+3)}{24}` **is** the published `e_k`
multiplier. Also `\binom{k+4}2\binom{k+4}4=\tfrac{(k{+}1)(k{+}2)(k{+}3)^2(k{+}4)^2}{48}`,
the document's stated equivalent form for `I_r`. All `0` failures.

### 3.2 The resummation argument — is it airtight?

Yes. My independent derivation:

Theorem A says `g_r(m,b)=\sum_{j=0}^rA_j\prod_{i=1}^{j}(t{+}i\varepsilon)`, since
`P_j(m)/n^j=\prod_{i=1}^j(m{+}i)/n=\prod_{i=1}^j(t{+}i\varepsilon)`. The classical
identity `x(x{+}1)\cdots(x{+}N{-}1)=\sum_Mc(N,M)x^M` at `N=j{+}1`, divided by `x`,
gives `\prod_{i=1}^{j}(x{+}i)=\sum_{k=0}^{j}c(j{+}1,k{+}1)x^k`; homogenising with
`x=t/\varepsilon` and multiplying by `\varepsilon^j`:

`\displaystyle\prod_{i=1}^{j}(t{+}i\varepsilon)=\sum_{k=0}^{j}c(j{+}1,k{+}1)\,t^k\varepsilon^{j-k}`.

**Verified directly as a two-variable polynomial expansion for `j\le14`, `0`
failures** — I checked the homogenised form itself, not just the classical
identity, because the homogenisation is where an off-by-one would hide.

Now the reindexing. The double sum is over `\{(j,k):0\le k\le j\le r\}`, and the
substitution `p:=j-k` is a **bijection** onto `\{(p,k):p,k\ge0,\;k{+}p\le r\}`,
with inverse `j=k{+}p`. Nothing is double-counted and nothing is dropped, because
the map is a bijection between two finite index sets. Collecting `\varepsilon^p`:

`\displaystyle\Phi^{[p]}_r(t,b)=\sum_{k=0}^{r-p}c(k{+}p{+}1,k{+}1)\,A^{(r)}_{k+p}(b)\,t^k`,

which is Theorem M, with `\deg=r{-}p` and `\equiv0` for `p>r` because the range
`0..r{-}p` is then empty. **The `g`-side termination at `p=r` is correct.**

### 3.3 The `g`/`h` termination asymmetry is real

The document claims the `h`-side terminates one order later, at `p=r{+}1`. **This
is correct, and I derived why.** By Theorem B,
`h_r(a,b)=\big[(1{-}s)+\varepsilon\big]\hat g_r(n{-}a{+}1,b{+}1)`, and with
`t'=(n{-}a{+}1)/n=(1{-}s)+\varepsilon` one has `t'{+}i\varepsilon=(1{-}s)+(i{+}1)\varepsilon`,
so writing `u:=1{-}s`,

`\displaystyle h_r(a,b)=\sum_{j=0}^{r}A^{(r)}_j(b{+}1)\prod_{i=1}^{j+1}(u{+}i\varepsilon)`.

The product has **`j+1` factors, not `j`** — the leading `(1{-}s)+\varepsilon` is
absorbed as the `i=1` factor. Expanding by the same identity at `N=j{+}2` gives
`\varepsilon`-degrees up to `j{+}1`, i.e. up to `r{+}1`. Hence

`\displaystyle\Psi^{[p]}_r(s,b)=\sum_k c(k{+}p{+}1,k{+}1)\,A^{(r)}_{k+p-1}(b{+}1)\,(1{-}s)^k`,

exactly the document's §4.2 `h`-side statement. **The asymmetry is structural, not
a typo**: it is the one extra factor that Theorem B's prefactor contributes.
Confirmed numerically at 3 960 checks, and specifically:

| `r` | `\Psi^{[r+1]}_r(s,0)` | `\Psi^{[r+2]}_r(s,0)` |
|---|---|---|
| 0 | `1/2` | `0` |
| 1 | `1/6` | `0` |
| 2 | `1/10` | `0` |
| 3 | `3/35` | `0` |
| 4 | `2/21` | `0` |

i.e. `\Psi^{[r+1]}_r` is **nonzero** and `\Psi^{[r+2]}_r` vanishes — the asymmetry
holds in both directions, which is the stronger check. (Note the `r=2` entry is
`M_2(0,0)=1/10` again: it is the *last* nonvanishing order of `h_2`, which is why
no prior document had an object for it.)

---

## Part 4. Corollaries A1–A3 and the `\psi_n^{(K)}` formulas

| check | scope | count | mismatches |
|---|---|---|---|
| **Corollary A2**: `g_r=\sum_{p=0}^r\varepsilon^p\Phi^{[p]}_r` and `h_r=\sum_{p=0}^{r+1}\varepsilon^p\Psi^{[p]}_r`, both exact, vs raw simulator | `n\le20,r\le7,b\le4`, all `m`, all `a` | 9 270 | **0** |
| residual `=` exactly its own tail; `\equiv0` for `p>r` | same, all `p\le r{+}2` | 9 270 | **0** |
| **Corollary A1** `\psi_n^{(K)}=g_K(n,0)` vs raw simulator | `K=0..8`, `n=K{+}1..22` | 162 | **0** |
| `g_6(7,0)` vs published brute force `355081/823543` | — | 1 | **0** |
| **Corollary A3** `D^{*(p)}_r(b)=\Phi^{[p]}_r(1,b)=\sum_{j\ge p}c^{(r)}_j(b)c(j{+}1,j{+}1{-}p)` | `p\le5,r\le24,b\le3` | 600 | **0** |
| `D^{*(0,1,2)}_r(0)=\varphi_r,\ \tfrac r4\varphi_r,\ \tfrac{r(3r+1)}{32}\varphi_r-\tfrac r{12}` | `r=0..60` | 183 | **0** |

**The three new `\psi_n^{(K)}` formulas are correct.** I computed `g_K(n,0)`
independently with my raw simulator (exact fractions) and compared against
Corollary A1 symbolically:

- `\psi_n^{(6)}=\frac{2048n^6+3072n^5+4293n^4+4638n^3+3529n^2+1662n+360}{6006n^6}` — **IDENTICAL** to the document's printed formula, and matches my brute force at `n=7..22` (16 points).
- `\psi_n^{(7)}`, `\psi_n^{(8)}` — likewise **IDENTICAL**, 15 and 14 brute-force points.
- `K=0..5` reproduce the five published PROVED formulas.
- The two `1/n^2` coefficients Estágio 8 flagged as "not in any prior document",
  `1431/2002` and `2219/2340`, come out exactly.

**On Corollary A3's justification.** All `c(k{+}p{+}1,k{+}1)>0`, so `\Phi^{[p]}_r`
has non-negative coefficients, is non-decreasing on `[0,1]`, and attains its
maximum at `t=1`, which corresponds to `m=n` — a valid state whenever
`n\ge b{+}r{+}1`. Since the residual is exactly the tail (Corollary A2),
`n^p\max_m|R^{(p)}|=\Phi^{[p]}_r(1,b)+O(1/n)`, giving the stated limit. The
argument is correct. (Minor: "increasing" should read "non-decreasing" — for
`r=p` the polynomial is a positive constant. This does not affect the conclusion,
since the maximum is still attained at `t=1`.)

---

## Part 5. **FINDING: the `b\ge1` negative claim is false at `b=1`**

### 5.1 The claim, and what is actually true

> §6.3 item 3: *"Fitting the same `\{r^q\varphi_r\}\cup\{r^q\}` basis at
> `b=1,2,3` **fails** out of sample (54–56 failures out of 61 tested `r`), at
> `p=2` as well as `p=3`."*
> Scorecard row 13: *"**REFUTED for that basis** (54–56 out-of-sample failures out
> of 61, at `p=2` and `p=3` alike) — hence **OPEN** in general, exactly as the
> predecessor left it."*

**At `b=1` the basis does not fail. It represents `D^{*(p)}_r(1)` exactly.**
Fitting on the minimum `2p{+}1` points and then testing exactly out of sample to
`r=400`:

| `p` | `D^{*(p)}_r(1)` | out-of-sample failures, `r=0..400` |
|---|---|---|
| 1 | `\tfrac{r+1}{4}\varphi_r-\tfrac14` | **0** |
| 2 | `\tfrac{(r+1)(3r+8)}{32}\varphi_r-\tfrac{5r+6}{24}` | **0** |
| 3 | `\tfrac{(r+1)(5r^2+39r+32)}{128}\varphi_r-\tfrac{(r+1)(7r+12)}{48}` | **0** |
| 4 | `\tfrac{(r+1)(105r^3+1765r^2+3314r+1536)}{6144}\varphi_r-\tfrac{45r^3+229r^2+306r+120}{480}` | **0** |

**The `p=2` row is not merely fitted — it is PROVED.** It is the wave-10 referee's
Theorem 3′ specialised to `b=1`. I transcribed Theorem 3′ from
`error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3 and confirmed
it against my own `D^{*(2)}_r(b)` at **205 exact checks** (`r\le40`, `b\le4`),
`0` mismatches; at `b=1` it reduces, after the strip term vanishes
(`E(1{-}\tfrac\beta2)=E(0)=0` at `\beta=2`) and `\Phi_1(r)=2\varphi_r`, to exactly
`\tfrac{(r+1)(3r+8)}{32}\varphi_r-\tfrac{5r}{24}-\tfrac14`. So the document
declares OPEN, "exactly as the predecessor left it", a case its own cited
predecessor **had already closed**.

### 5.2 Why `b=1` works and `b\ge2` genuinely does not

Theorem 3′'s prefactor is `\Phi_b(r)=2\varphi_r\prod_{j=1}^{b}\frac{2r+2j}{2r+j+1}`.
Evaluating the product:

| `b` | `\Phi_b(r)/\varphi_r` | consequence |
|---|---|---|
| 0 | `2` | constant → polynomial-in-`r` times `\varphi_r` suffices |
| **1** | `\frac{2r+2}{2r+2}\cdot2=2` | **constant → the basis works** |
| 2 | `\frac{4r+8}{2r+3}` | not polynomial → basis cannot work |
| 3 | `\frac{4r+12}{2r+3}` | not polynomial → basis cannot work |
| 4 | `\frac{8r^2+56r+96}{4r^2+16r+15}` | not polynomial → basis cannot work |

The single `b=1` factor is `\frac{2r+2}{2r+2}=1` **identically**. That is the whole
explanation: `b=1` is the last value for which the prefactor collapse leaves a
constant multiple of `\varphi_r`, so `b\in\{0,1\}` are in the basis's span and
`b\ge2` are structurally excluded. I confirmed the exclusion is not a
basis-size artefact: enlarging to `\deg_\varphi\le p{+}6`, `\deg_{\text{poly}}\le p{+}5`
finds **no** fit at `p=2,3` and `b=2,3`.

### 5.3 How the error most likely arose

The document's reported failure counts are reproduced **exactly** — by `b=2` and
`b=3`, not by `b=1`. Fitting on `2p{+}1` points and counting failures over
`r=0..60` (61 values, in-sample points passing trivially):

| `p` | `b=0` | `b=1` | `b=2` | `b=3` |
|---|---|---|---|---|
| 2 | 0/61 | **0/61** | **56**/61 | **56**/61 |
| 3 | 0/61 | **0/61** | **54**/61 | **54**/61 |

`61-5=56` and `61-7=54`: every out-of-sample point failed and only the fit points
passed — the signature of a basis that cannot represent the answer at all. The
document's "54–56" is precisely the `b\in\{2,3\}` pair of numbers. The most
economical reading is that `b=1` was run, returned `0` failures, and was
nonetheless folded into a summary range describing `b=2,3`.

### 5.4 Corrected statement

> **Row 13, corrected.** A closed form for `D^{*(p)}_r(b)` in the
> `\{r^q\varphi_r\}\cup\{r^q\}` basis **exists for `b=0` and `b=1`** and is
> **REFUTED for `b\ge2`** (56/61 and 54/61 out-of-sample failures at `p=2,3`;
> no fit up to `\deg_\varphi\le p{+}6`). The `b=1` forms are tabulated in §5.1;
> the `p=2` one is **PROVED** (wave-10 Theorem 3′ at `b=1`), the `p=1,3,4` ones
> are **NUMERICALLY VERIFIED** exactly to `r=400`. The structural reason is that
> `\Phi_b(r)/\varphi_r` is constant exactly for `b\le1`. **`b\ge2` remains OPEN**,
> and for it the document's recommended route (Theorem 3′-style prefactor
> collapse, not a naive fit) is the right one.

This is a **strengthening** of the document, not a weakening: it converts one
overstated negative into four new closed forms.

---

## Part 6. **UPGRADE: `D^{*(p)}_r(0)` at `p=3,4,5` from NUMERICALLY VERIFIED to PROVED**

§6.3 item 4 names the proof route and says "Not carried out here". I carried it
out. The document's labelling was honest; it was simply conservative.

### 6.1 Structure theorem

Let `N=2r{+}1` and let `S` be a sum of `N` i.i.d. `\pm1` (so `S=N-2X`,
`X\sim\mathrm{Bin}(N,\tfrac12)`). Since `A^{(r)}_j(0)=\frac{\varphi_r}{4^r}\binom{2r+1}{r-j}`
and `c(j{+}1,j{+}1{-}p)=e_p(1,\dots,j)=:Q_p(j)`, a polynomial in `j` of degree `2p`,
substituting `i:=r-j` and `v:=\frac{N-2i}2=r{+}\tfrac12-i` gives

`\displaystyle D^{*(p)}_r(0)=\frac{\varphi_r}{4^r}\sum_{i=0}^{r}\binom Ni R_p(v)`, `\quad R_p(v):=Q_p(v-\tfrac12)`, `\deg R_p=2p`.

Split `R_p=E_p+O_p` into even and odd parts.

**Even block.** Because `N` is **odd** there is no middle term, so `i\mapsto N-i`
is a bijection of `\{i\le r\}` onto `\{i\ge r{+}1\}` sending `v\mapsto-v`. Hence
`\sum_{i\le r}\binom NiE_p(v)=\tfrac12\sum_{i=0}^{N}\binom NiE_p(v)=2^{N-1}\mathbb E[E_p(S/2)]`.
`\mathbb E[S^{2k}]` is a polynomial in `N` of degree `k` (a sum of `N` i.i.d.
mean-zero `\pm1`), so `\mathbb E[E_p(S/2)]` is a polynomial in `r` of degree `\le p`.
With `2^{N-1}=4^r`, this block contributes `\varphi_r\,U_p(r)`, `\deg U_p\le p`.

**Odd block.** `i\le r\iff S=N-2i\ge1\iff S>0`, and `S\ne0` since `N` is odd, so
`\sum_{i\le r}\binom NiO_p(v)=2^{N-1}\mathbb E[O_p(|S|/2)]`. Now
`\mathbb E|S|^{2k+1}=\frac{\binom{2r}r}{4^r}W_k(r)` with `W_k` a **polynomial**
divisible by `(2r{+}1)`; and `\frac{\varphi_r}{4^r}\binom{2r}r=\frac1{2r+1}`
exactly. So this block is `\varphi_r`-**free**, contributing a polynomial
`V_p(r)` with `\deg V_p\le p-1`.

`W_k` is a classical object; it follows by two applications of the telescoping
identity `(N{-}2i)\binom Ni=N\big[\binom{N-1}i-\binom{N-1}{i-1}\big]` plus Abel
summation and induction on `k` (`W_0=2r{+}1` directly). I verified it exactly:

| `k` | `W_k(r)` | degree | `(2r{+}1)\mid W_k` |
|---|---|---|---|
| 0 | `2r{+}1` | 1 | yes |
| 1 | `(2r{+}1)(4r{+}1)` | 2 | yes |
| 2 | `(2r{+}1)(32r^2{+}8r{+}1)` | 3 | yes |
| 3 | `(2r{+}1)(384r^3{-}32r^2{+}12r{+}1)` | 4 | yes |
| 4 | `(2r{+}1)(6144r^4{-}4608r^3{+}1728r^2{+}16r{+}1)` | 5 | yes |
| 5 | `(2r{+}1)(122880r^5{-}215040r^4{+}169728r^3{-}48064r^2{+}20r{+}1)` | 6 | yes |
| 6 | `(2r{+}1)(2949120r^6{-}\cdots{+}24r{+}1)` | 7 | yes |

and `\mathbb E[S^{2k}]` polynomial of degree `k` in `N` for `k\le8`, `0` failures.

> **Structure theorem.** `D^{*(p)}_r(0)=U_p(r)\varphi_r+V_p(r)` with
> `U_p,V_p\in\mathbb Q[r]`, `\deg U_p\le p`, `\deg V_p\le p{-}1`.

### 6.2 The upgrade

Once the *form* is known, matching `2p{+}1` points is a **proof**, provided the
interpolation matrix `\big[\varphi_{r}r^q\ \big|\ r^q\big]_{r=0..2p}` is
non-singular — which I checked exactly (determinant `\ne0` at `p=3,4,5`). The
unique solution is therefore *the* answer:

| `p` | recovered `U_p` | recovered `V_p` | vs the document |
|---|---|---|---|
| 3 | `\tfrac{r(5r^2+9r+2)}{128}` | `-\tfrac{r^2}{12}` | **IDENTICAL** |
| 4 | `\tfrac{r(105r^3+610r^2+123r-70)}{6144}` | `-\tfrac{r(3r+2)(5r-1)}{240}` | **IDENTICAL** |
| 5 | `\tfrac{r(189r^4+2590r^3+855r^2-490r-72)}{24576}` | `-\tfrac{r^2(5r^2+9r-4)}{120}` | **IDENTICAL** |

(the `V_4`, `V_5` factorisations expand to the document's
`-\tfrac{r^3}{16}-\tfrac{7r^2}{240}+\tfrac r{120}` and
`-\tfrac{r^4}{24}-\tfrac{3r^3}{40}+\tfrac{r^2}{30}`.) Belt-and-braces: `0`
failures over `r=0..400` for each. **Scorecard row 11 may be promoted to PROVED.**

Two further forms, never stated by the document:

`D^{*(6)}_r(0)=\tfrac{r(693r^5+18585r^4+16177r^3-9913r^2-2830r+1864)}{196608}\varphi_r-\tfrac{r(1575r^4+6986r^3-3639r^2-122r+240)}{60480}`

`D^{*(7)}_r(0)=\tfrac{r(429r^6+19943r^5+40971r^4-31899r^3-4368r^2+8764r-1072)}{262144}\varphi_r-\tfrac{r^2(945r^4+8330r^3-2973r^2-3086r+1824)}{60480}`

both `0` failures to `r=250`.

---

## Part 7. **UPGRADE: the `(2p{-}1)!!/(4^pp!)` leading coefficient (row 12) is PROVABLE**

Row 12 is labelled NUMERICALLY CHARACTERIZED, "a pattern in `p` over six points,
deliberately **not** promoted". It follows in two lines from Part 6:

- `e_p(1,\dots,j)` has leading term `\frac{(1{+}\cdots{+}j)^p}{p!}=\frac{(j^2/2)^p}{p!}=\frac{j^{2p}}{2^pp!}`,
  so `R_p(v)` has leading term `\frac{v^{2p}}{2^pp!}`, carried entirely by its
  **even** part;
- `\mathbb E[S^{2p}]` is a degree-`p` polynomial in `N` with leading coefficient
  `(2p{-}1)!!` (the `2p`-th Gaussian moment);
- the odd block contributes **no** `\varphi_r` at all (Part 6.1), so it cannot
  touch `U_p`'s leading coefficient. Hence, with `N\sim2r`,

`\displaystyle[\,r^p\,]U_p=\frac{1}{2^pp!}\cdot\frac{1}{2^{2p}}\cdot(2p{-}1)!!\cdot2^p=\frac{(2p{-}1)!!}{4^p\,p!}`. `\blacksquare`

Both ingredients verified exactly (`p\le7`, `k\le8`, `0` failures), and the
assembled constant matches `1,\tfrac14,\tfrac3{32},\tfrac5{128},\tfrac{35}{2048},\tfrac{63}{8192},\tfrac{231}{65536},\tfrac{429}{262144}`
for `p=0..7` — the document's six values plus my two new ones.
**Row 12 may be promoted to PROVED.**

---

## Part 8. Scope and honesty audit (§6, §7)

I looked specifically for the wave-10 failure mode: a scorecard row carrying
"PROVED given claim X" while the body states the same thing flatly.

**Not found.** The conditional structure is coherent and consistently maintained:
claim 6 is Theorem A (flat PROVED, correctly — I re-proved it); rows 4, 5, 8, 9
say "PROVED given claim 6"; row 10 says "PROVED given claims 5, 6, 9"; row 3 says
NUMERICALLY VERIFIED "and a corollary of claim 6 once that is granted". I checked
the body text of §3, §4.2, §4.3 and §5 for upgrades of these and found none. §6.3
items 1–6 and §6.4 are accurate and appropriately self-critical; the statement
"No independent adversarial re-verification has been performed" was true when
written.

Three minor nits, none substantive:

| # | location | issue | severity |
|---|---|---|---|
| N-1 | scorecard row 1 | The order-`p` ODE is marked flat **PROVED**. As a formal ladder it is definitionally fine, but as a statement *about `g_r`* it needs the expansion to exist and terminate — which is Corollary A2, itself "PROVED given claim 6". §2.1 does flag the ansatz status ("*an ansatz to be validated*"), so nothing is smuggled; the row should read "PROVED given claim 6" for consistency with rows 4/5/9. | cosmetic |
| N-2 | scorecard row 13 | "exactly as the predecessor left it" mis-states the predecessor's final state: the wave-10 referee's Theorem 3′ closed `p=2` for **every** `b`, and the predecessor `ATTEMPT.md` carries the post-adversarial correction saying so. | minor, factual |
| N-3 | Corollary A3 | "`\Phi^{[p]}_r(\cdot,b)` is **increasing** on `[0,1]`" — should be *non-decreasing* (at `r=p` it is a positive constant). Conclusion unaffected. | cosmetic |

No circularity: §4.1 proves Theorem A with no ansatz and no `\varepsilon`-expansion,
so §2/§3 may then be justified *a posteriori* by Corollary A2. The document states
this relationship correctly ("the `\varepsilon`-ladder … is not load-bearing for
the proof"), and my two derivations — the elementary proof (Part 1) and the
independent ladder (Part 3) — agree everywhere they overlap, which is the check
§6.4 asks for.

---

## Part 9. Scorecard (mirroring the target's §7)

| # | target's claim | target's label | **my verdict** |
|---|---|---|---|
| 1 | order-`p` receiver ODE + source relation (§2.1) | PROVED | **SOUND** — re-derived from scratch, signs included. Label should be "PROVED given claim 6" (N-1) |
| 2 | `I_r` ODE + `M_r` relation, the mandated rung | PROVED given 1 | **SOUND** — my instantiation is identical; `M_2(0,0)=1/10` confirmed two ways |
| 3 | multiplier is `r,b`-independent | NUM. VERIFIED | **SOUND** — reproduced at every `(r,b)` tried; all 56 table entries match |
| 4 | `\deg\Phi^{[p]}_r=r{-}p`; `\equiv0` for `p>r` | PROVED given 6 | **SOUND** |
| 5 | **Theorem M** | PROVED given 6 | **SOUND** — verified `p=0..8` (10 098 checks); resummation airtight |
| 6 | **Theorem A** | **PROVED** | **SOUND — the central claim survives.** Re-derived by hand; 215 070 exact checks; per-term identity verified at symbolic `r,j` (stronger than the document's own check) |
| 7 | **Theorem B** | PROVED | **SOUND**; domain caveat verified as a strict biconditional |
| 8 | **Corollary A1** (item (i)) | PROVED given 6 | **SOUND**; `\psi_n^{(6,7,8)}` reproduced from my own brute force |
| 9 | **Corollary A2** (termination, residual = tail) | PROVED given 6 | **SOUND**, 9 270 exact points |
| 10 | **Corollary A3** (`D^{*(p)}_r(b)=\Phi^{[p]}_r(1,b)`) | PROVED given 5,6,9 | **SOUND** (nit N-3) |
| 11 | `D^{*(3,4,5)}_r(0)` closed forms | NUM. VERIFIED | **SOUND, and UPGRADED to PROVED** (Part 6). Honestly labelled by the document |
| 12 | leading coefficient `(2p{-}1)!!/(4^pp!)` | NUM. CHARACTERIZED | **SOUND, and UPGRADED to PROVED** (Part 7) |
| 13 | `b\ge1` closed form in that basis | REFUTED / OPEN | **FLAWED.** False at `b=1`: the basis is exact there for `p=1,2,3,4`, and the `p=2` case is already PROVED by wave-10 Theorem 3′. Correct at `b\ge2`. Corrected statement + 4 closed forms in Part 5.4 |
| 14 | anything uniform in `K` | NOT CLAIMED | **correctly labelled** |
| 15 | re-derivation of the transition rules | NOT ATTEMPTED | **correctly labelled**; transcription verified faithful (Part 0) |
| 16 | independent adversarial re-verification | NOT PERFORMED | **now performed** — this report |

### Totals of my own independent verification

| script | what | exact checks | failures |
|---|---|---|---|
| `ref_sim.py` | raw `(a,b,r)` simulator vs Theorems A/B + both binomial forms + the `(*)`/`(**)` rewrite | **215 070** | **0** |
| `ref_symbolic.py` | (P1)–(P3) symbolic; per-term identity at symbolic `r,j,b,m,n`; assembled `(*)`,`(**)` symbolic `r=0..9`; Stirling identities | all symbolic | **0** |
| `ref_ladder.py` | independent order-`p` ladder; `c_k,d_k,e_k`; `I_r,M_r`; Theorem M `p\le8`; `h`-side; `D^*` | **20 754** | **0** |
| `ref_checks.py` | multiplier table; Corollary A2; `\psi_n^{(0..8)}`; `D^{*(p)}` fits; the `b\ge1` claim | **10 552** | **0** |
| `ref_bge1.py` | the `b\ge1` question in detail | — | see Part 5 |
| `ref_dstar_proof.py` | Theorem 3′ transcription (205); `b=1` forms to `r=400`; structure theorem; the upgrade | **3 012** | **0** |
| `ref_leading.py` | the `(2p{-}1)!!/(4^pp!)` upgrade | — | **0** |
| `ref_domain.py` | domain caveat as a biconditional | **72 474** | **0** |

---

## Part 10. Final verdicts

> **VERDICT 1 — Theorem A: SOUND.** The central claim survives a hostile,
> from-scratch re-derivation. Facts (P1)–(P4) are correct; the assembled
> identities `(*)` and `(**)` hold; (P4) gives uniqueness; the domain caveat is a
> genuine resolution, verified as a strict biconditional, not a coincidence. The
> proof is short, elementary, and — this is the load-bearing point — **correct**.
> With it, Theorem B, Theorem M and Corollaries A1/A2/A3 all follow, exactly as
> §6.4 says they do.

> **VERDICT 2 — the `\varepsilon`-machinery (§2.1–§2.3): SOUND.** The order-`p`
> receiver ODE and source relation are correct, **including the `d/ds=-d/dt`
> sign the author flags**. Their `p=0,1,2` instances reproduce the four published
> statements character-for-character, checked against the source texts. The `p=3`
> rung is correct and lands exactly on the one independent constraint available
> (`M_2(0,0)=1/10`). §2 and §4 are logically independent and agree everywhere.

> **VERDICT 3 — Theorem M and the resummation: SOUND.** Verified to `p=8`. The
> `(j,k)\leftrightarrow(p,k)` reindexing is a bijection; the `g`-side terminates
> at `p=r` and the `h`-side at `p=r{+}1`, and **that asymmetry is real** — it is
> the extra factor contributed by Theorem B's prefactor, which I derived
> independently and confirmed in both directions.

> **VERDICT 4 — the `p\ge3` sharp constants: SOUND, correctly labelled, and now
> STRENGTHENED.** The document's NUMERICALLY VERIFIED label was honest and
> conservative. I carried out the proof route it names but declines to execute,
> and rows 11 and 12 may both be promoted to **PROVED**.

> **VERDICT 5 — the `b\ge1` negative claim: FLAWED.** §6.3 item 3 and row 13 are
> **false at `b=1`** and correct only at `b\ge2`. The error's direction matters:
> the document declares OPEN a case that is not open — its own cited predecessor's
> Theorem 3′ already closes `p=2` at every `b`, and I supply exact forms at
> `p=1,2,3,4`. Corrected statement in Part 5.4. The structural reason
> (`\Phi_b(r)/\varphi_r` is constant exactly for `b\le1`) also explains why the
> document's negative finding is right for `b\ge2`.

> **OVERALL.** The headline result stands. The document is careful, its
> conditional labelling is consistent, it does not repeat the wave-10 pattern of
> silently dropping conditionals, and it correctly identifies what a referee
> should attack first. One negative side-claim is overstated and must be
> corrected before cataloguing; two conservative labels can be upgraded. Nothing
> found weakens Theorem A, Theorem B, Theorem M, or Corollaries A1–A3.

### Required edits before cataloguing

1. **Row 13 / §6.3 item 3** — restate as `b\ge2`; add the four `b=1` closed forms
   (Part 5.4); remove "exactly as the predecessor left it" (N-2).
2. **Row 11, Row 12** — may be promoted to PROVED, citing Parts 6 and 7.
3. **Row 1** — for consistency, "PROVED given claim 6" (N-1). Cosmetic.
4. **Corollary A3** — "non-decreasing" (N-3). Cosmetic.

### Files in this directory

| file | contents |
|---|---|
| `ref_sim.py` / `ref_sim_big.log` | from-scratch exact `(a,b,r)` simulator (original rules) + Theorem A/B closed forms + both binomial forms; 215 070 checks |
| `ref_symbolic.py` / `.log` | (P1)–(P3), the per-term identity at symbolic `r,j,b,m,n`, assembled `(*)`/`(**)`, Stirling identities |
| `ref_ladder.py` / `.log` | independent order-`p` `\varepsilon`-ladder; Theorem M to `p=8`; `I_r`/`M_r`; `h`-side asymmetry; `D^{*(p)}` |
| `ref_checks.py` / `.log` | multiplier table; Corollary A2; `\psi_n^{(0..8)}` vs brute force; `D^{*(p)}` fits; the `b\ge1` claim |
| `ref_bge1.py` / `.log` | the `b\ge1` question in detail; larger-basis search; structural explanation |
| `ref_dstar_proof.py` / `.log` | Theorem 3′ confirmation; `b=1` forms; structure theorem; the `p=3,4,5` upgrade; new `p=6,7` |
| `ref_leading.py` / `.log` | the `(2p{-}1)!!/(4^pp!)` upgrade |
| `ref_domain.py` / `.log` | the domain caveat as a strict biconditional |
| `ref_diagnosis.log` | reproduction of the target's "54–56 of 61" as the `b=2,3` numbers |

All exact (`fractions.Fraction` / `sympy.Rational` / `sympy.Symbol`). No
randomisation; every sweep is exhaustive over a stated finite range. Reproduce
with: `python3 ref_sim.py 31 10 8`; `python3 ref_symbolic.py`;
`python3 ref_ladder.py 8 16 5`; `python3 ref_checks.py`; `python3 ref_bge1.py`;
`python3 ref_dstar_proof.py`; `python3 ref_leading.py`; `python3 ref_domain.py`.
