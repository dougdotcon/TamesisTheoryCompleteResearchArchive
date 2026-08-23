# The multiplier ladder is the unsigned Stirling numbers of the first kind — and the `ε`-series therefore resums to an exact, finite, all-orders closed form

> **Governance.** Wave 11, front (b), authorized by `DISC-DEC-047`
> (`ALL-ORDERS-CLOSED-FORM-ATTEMPT`). Target: item **(i)** of the "what remains
> open" list of `THEOREM.md` Estágio 6 / 7 / 8 — *"a forma fechada exata,
> todas-as-ordens, geral-`K`"* — approached, as the mandate directs, by
> extending the `ε`-matching ladder of `error_constant_growth_attempt/ATTEMPT.md`
> §3.1 **one more order** (from `(H_r,L_r)` at `1/n²` to a new pair at `1/n³`)
> and looking for a fourth term in the multiplier sequence
> `1,\ \binom{k+2}2,\ \tfrac{3k+8}4\binom{k+3}3`. Pure combinatorial /
> asymptotic mathematics — no external data, no holdout, no real-world claim,
> no governance edits. **Nothing outside this directory was created, modified
> or deleted.** No git commit was made. Every claim below is labeled PROVED,
> PROVED-MODULO-[X] (X named precisely), NUMERICALLY VERIFIED, NUMERICALLY
> CHARACTERIZED, or OPEN.

> **Executive summary (read first).**
>
> 1. **The mandated rung was derived.** Carrying the `ε`-matching to order
>    `ε³` gives the pair `(I_r, M_r)` (my naming; §2.3), with
>    `\displaystyle I_r(t,b)=\sum_{k=0}^{r-3}\binom{k{+}4}2\binom{k{+}4}4
>    \cdot\frac{r!}{(r{-}k{-}3)!}\cdot\frac{t^k}{\prod_{i=1}^{k+4}(r{+}b{+}i)}`.
>    Its `ε⁰,ε¹,ε²` orders reproduce the already-PROVED `F_r`, `G_r`, `H_r`
>    closed forms exactly, and its `M_2(0,0)=1/10` matches the `1/n³`
>    coefficient of the already-PROVED `ψ_n^{(3),R}`.
>
> 2. **The pattern search did not fail — it closed.** The fourth multiplier is
>    `\binom{k+4}2\binom{k+4}4`, and together with `1`, `\binom{k+2}2`,
>    `\tfrac{3k+8}4\binom{k+3}3` this is not four fitted points but the four
>    lowest instances of one classical sequence: the **unsigned Stirling
>    numbers of the first kind**,
>    `\;M_p(k)=c(k{+}p{+}1,\,k{+}1)=|s(k{+}p{+}1,k{+}1)|`, uniform in the order
>    index `p`. Read off *independently* from the ladder at orders
>    `p=0,\dots,8` before any fitting (§3.1).
>
> 3. **Because the multipliers are Stirling numbers, the whole series resums.**
>    `\sum_k c(j{+}1,k{+}1)t^k\varepsilon^{j-k}=\prod_{i=1}^{j}(t{+}i\varepsilon)`
>    is the homogenised rising-factorial generating identity; and
>    `\prod_{i=1}^{j}(t{+}i/n)=(m{+}j)!/(m!\,n^j)` exactly. Since
>    `\deg\Phi^{[p]}_r=r{-}p` the series **terminates at `p=r`**, so the
>    resummation is not asymptotic but exact:
>
>    > **Theorem A.** For every valid state (`b{+}r{+}1\le m\le n`),
>    > `\displaystyle g_r(m,b)=\sum_{j=0}^{r}c_j^{(r)}(b)\cdot\frac{(m{+}j)!}{m!\,n^{j}}`,
>    > with `c_j^{(r)}(b)` **exactly the already-PROVED leading-order
>    > coefficients** of `F_r`. In words: *the exact finite-`n` answer is
>    > `F_r(t,b)` with each monomial `t^j` replaced by the grid product
>    > `\prod_{i=1}^{j}(t+i/n)`.*
>
>    Equivalently, in binomial form and at `t=1,b=0`:
>    `\displaystyle \psi_n^{(K)}=\frac{\varphi_K}{4^K}\sum_{j=0}^{K}
>    \binom{2K{+}1}{K{-}j}\frac{(n{+}j)!}{n!\,n^{j}}`.
>
> 4. **Theorem A has an elementary proof** (§4) that does not use the
>    `ε`-machinery at all: two one-line product identities for
>    `(m{+}j)!/m!`, one coefficient identity
>    (`A_j\,(j{+}1{+}r{+}b)=r\,A_{j-1}^{(r-1)}(b{+}1)`, verified symbolically in
>    `r,j,b`) plus its trivial `j{=}0` companion, and the observation that the transition
>    system is a well-founded finite recursion with a unique solution. The
>    `ε`-ladder is what *found* the formula and what ties it to the published
>    `F_r,G_r,H_r`; it is not load-bearing for the proof.
>
> 5. **Verification.** My from-scratch ladder reproduces the PROVED
>    `c_k^{(r)}(b), d_k^{(r)}(b), e_k^{(r)}(b)` exactly; the closed form
>    reproduces **every** published exact fact of this lineage (17/17
>    cross-checks: `ψ_n^{(1..5)}`, `ψ_n^{(3),R}`, the brute-force-confirmed
>    `g_6(7,0)=355081/823543`, `\varphi_K`, `K\varphi_K/4`, Estágio 7's `c_K`
>    including `c_6=1093/6006`, Estágio 8's Theorem 3 to `r=89` and its
>    general-`b` table); and it agrees with my own exact discrete simulator on
>    two exhaustive sweeps (**61 048** and **22 216** exact checks, overlapping
>    in range by design), `0` mismatches.
>
> **This is a positive result of substantial size and it is therefore NOT
> catalogued by this document.** Per the archive's standing discipline it
> requires a dedicated hostile-referee pass — re-deriving §2 and §4 from
> scratch — before any integration into `THEOREM.md` may be considered. I do
> not claim item (i) is closed or integrated; I claim it is **answered and
> ready for review**. §6.4 names exactly what a referee should attack first.
> Nothing here weakens any existing result: Teorema 3, the Estágio 6 existence
> theorem, the Estágio 7 rate coefficient and the Estágio 8 growth rate are all
> untouched and all remain true — this document only supplies a sharper object
> that has them as corollaries.

---

## 0. Disciplina

**Sources read, in the order the task mandated, before any derivation or code:**

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entry `DISC-DEC-047`
   (mandate and scope for wave 11 front (b), including its explicit statement
   that concluding "there is no closed pattern beyond the current order" would
   be a complete and accepted outcome).
2. `.../u12_universality/theorem/THEOREM.md`, the complete Estágio 6, Estágio 7
   and Estágio 8 sections. Item **(i)** of all three open lists is the target.
3. `.../k_general_existence_attempt/ATTEMPT.md` in full — §1 (the definitions
   of `R_r`, `\varepsilon^h_r`), §2 (Facts 1–4), §3 (the exact residual
   recursion and the exact-finite-Taylor mechanism), §4 (including the I-1
   `h^{j-1}\to h^k` correction), §5 (the falling-factorial / hockey-stick
   telescoping), §6 (including the I-2 addendum), §§7–9.
4. `.../error_constant_growth_attempt/ATTEMPT.md` in full, with particular care
   on §3.1 (the `ε²` matching), §3.2 (the coefficient recursion), §3.3
   (Theorem 1 and the three-row multiplier table), §4 (Theorem 2), §5
   (Theorems 3 / 4 and their post-adversarial corrections), §8.2 (*"the
   multiplier sequence `1, \binom{k+2}2, \frac{3k+8}4\binom{k+3}3` is
   suggestive but three terms is not a pattern"*) and §8.4.
5. `.../error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` — Part 1
   (the independent re-derivation of the `ε²` matching), Part 2, Part 3.3
   (Theorem 3′), Part 4.
6. `.../k6_attempt/ATTEMPT.md` §2.3 (`c_k^{(r)}(b)`, PROVED), §3.1, §3.3
   (`d_k^{(r)}(b)`, PROVED), §3.4, and **§6.2** — which states precisely what
   item (i) asks for: *"The exact finite-`n` closed form for general `K` —
   which would need all `K+1` orders resummed, not just the first two — was not
   attempted… Whether the pattern found for `c_k^{(r)}(b)` and `d_k^{(r)}(b)`
   itself continues in a similarly closed-form-guessable way at every order is
   an open question this document does not address."*
7. `.../k3_attempt_2/ATTEMPT.md` §2 (the exact `(a,b,r)` transition rules,
   PROVED, with their own brute-force validation), §3 (the per-`K` telescoping
   **algorithm** — explicitly a `K`-uniform *procedure*, not a general-`K`
   closed form), §5 and §7.1 (`ψ_n^{(3)},ψ_n^{(3),R},ψ_n^{(4)},ψ_n^{(5)}`).

**Reuse policy (same convention as every predecessor in this lineage).** Every
script in this directory was written **from scratch**. Nothing was imported,
copied, or adapted from `k6_attempt/`, `k_general_existence_attempt/`,
`error_constant_growth_attempt/`, its `adversarial/`, or any other sibling. Two
classes of already-established *statements* (not code) were re-transcribed from
their prose, and both are labeled as such in `core.py`'s header:

- **Used as fixed, already-PROVED input:** the exact `(a,b,r)` transition rules
  of `k3_attempt_2/ATTEMPT.md` §2. This document takes the discrete recursion as
  given and is about its combinatorics; it does **not** re-derive the transition
  rules from the underlying probabilistic model. (My independent implementation
  of them reproduces `ψ_n^{(1)},\dots,ψ_n^{(5)}` and the
  brute-force-confirmed `g_6(7,0)=355081/823543`, which is the standing check
  that the transcription is faithful.)
- **Used only as CROSS-CHECK TARGETS, never as inputs:** the PROVED closed forms
  `c_k^{(r)}(b)`, `d_k^{(r)}(b)`, `e_k^{(r)}(b)`, the values `\varphi_r`,
  `K\varphi_K/4`, `\frac{K(3K+1)}{32}\varphi_K-\frac K{12}`, `c_K`, and the five
  exact `ψ_n^{(K)}` formulas. My ladder is built from the recursion alone and is
  *compared* against them afterwards.

**Exactness policy.** `fractions.Fraction` / `sympy.Rational` / `sympy.Symbol`
throughout. Every claim labeled PROVED, "exact", or "identity" rests on exact
rational or symbolic arithmetic. Floating point appears in exactly two places,
both flagged in situ: human-readable display columns, and the tolerance
comparison in `cross_checks.py` X8 against a predecessor's *printed* 6-figure
table (the only place where the target itself is not available exactly).

**No seeds.** Nothing in this directory is randomised; every sweep is
exhaustive over a stated finite range.

---

## 1. The target, restated precisely

Fix integers `r,b\ge0` and `n`. Write `h:=\varepsilon:=1/n`, `t:=m/n`, `s:=a/n`.
`g_r(m,b):=g(n{-}m,b,r)` and `h_r(a,b):=h(a,b,r)` are the exact conditional
probabilities of `k3_attempt_2/ATTEMPT.md` §2, defined on
`b{+}r{+}1\le m\le n` and `0\le a\le n{-}b{-}r{-}1`, and satisfying (PROVED
there, reused verbatim, not re-derived):

`(\ast)\qquad m\big[g_r(m,b)-g_r(m{-}1,b)\big]+(1{+}r{+}b)\,g_r(m{-}1,b)=1+r\,h_{r-1}(n{-}m{+}1,b)`

`(\ast\ast)\qquad h_r(a,b)=\tfrac1n+\tfrac rn\,h_{r-1}(a,b{+}1)+\Big[(1{-}s)-\tfrac{1{+}b{+}r}n\Big]g_r(n{-}a,b{+}1)`

Item (i) asks for the exact, all-orders, general-`K` closed form of
`\psi_n^{(K)}=g_K(n,0)`. The mandate's concrete instruction is narrower: push
the `\varepsilon`-matching one order past `H_r` and see whether the multiplier
sequence `1,\ \binom{k+2}2,\ \tfrac{3k+8}4\binom{k+3}3` acquires a recognisable
fourth term.

**Naming convention adopted here.** The lineage uses `F_r,G_r,H_r` on the
receiver (`g_r`) side and `\hat H_r,K_r,L_r` on the source (`h_r`) side. I
continue both alphabets by one letter — `I_r` (receiver, order `1/n^3`) and
`M_r` (source, order `1/n^3`) — and, because the derivation is done at a
symbolic order index, I also write

`\Phi^{[p]}_r(t,b)` for the order-`\varepsilon^p` receiver term
  (`\Phi^{[0]}=F_r,\ \Phi^{[1]}=G_r,\ \Phi^{[2]}=H_r,\ \Phi^{[3]}=I_r`),

`\Psi^{[p]}_r(s,b)` for the order-`\varepsilon^p` source term
  (`\Psi^{[0]}=\hat H_r,\ \Psi^{[1]}=K_r,\ \Psi^{[2]}=L_r,\ \Psi^{[3]}=M_r`),

and, since every source object enters the receiver equation reflected, the
reflected shorthand `\eta^{[p]}_r(t,b):=\Psi^{[p]}_r(1{-}t,b)`.

---

## 2. The `\varepsilon`-matching at a symbolic order index

### 2.1 The substitution

This is the predecessor's §3.1 mechanism carried at general `p` rather than at
`p=2`. Write, as an *ansatz to be validated* (§4 replaces it by a proof that
needs no ansatz at all):

`g_r(m,b)=\sum_{p\ge0}\varepsilon^p\Phi^{[p]}_r(t,b)`, `\qquad
h_r(a,b)=\sum_{p\ge0}\varepsilon^p\Psi^{[p]}_r(s,b)`.

Because `(m{-}1)/n=t-\varepsilon` **exactly** and each `\Phi^{[p]}_r(\cdot,b)`
is a polynomial of bounded degree, Taylor's theorem is an exact finite identity
with zero remainder — the same structural fact
`k_general_existence_attempt/ATTEMPT.md` §3 relies on. Collecting the
`\varepsilon^p` coefficient of each side of `(\ast)`:

- from `g_r(m{-}1,b)`: `\;\sum_{i\ge0}\frac{(-1)^i}{i!}(\Phi^{[p-i]}_r)^{(i)}(t,b)`;
- from `m[g_r(m,b)-g_r(m{-}1,b)]=\frac t\varepsilon[\cdots]`:
  `\;t\sum_{i\ge1}\frac{(-1)^{i+1}}{i!}(\Phi^{[p+1-i]}_r)^{(i)}(t,b)`;
- from `h_{r-1}(n{-}m{+}1,b)`, using `s=(1{-}t)+\varepsilon` **exactly** and
  `(\Psi^{[j]})^{(i)}(1{-}t)=(-1)^i(\eta^{[j]})^{(i)}(t)`:
  `\;\sum_{i\ge0}\frac{(-1)^i}{i!}(\eta^{[p-i]}_{r-1})^{(i)}(t,b)`.

Isolating the two terms that carry `\Phi^{[p]}_r` itself gives:

> **The order-`p` receiver ODE (general `p\ge0`).**
> `\displaystyle t\,(\Phi^{[p]}_r)'(t,b)+(1{+}r{+}b)\,\Phi^{[p]}_r(t,b)
> \;=\;[p{=}0]
> \;+\;r\!\!\sum_{i=0}^{p}\frac{(-1)^i}{i!}\big(\eta^{[p-i]}_{r-1}\big)^{(i)}(t,b)
> \;+\;t\!\!\sum_{i=2}^{p+1}\frac{(-1)^i}{i!}\big(\Phi^{[p+1-i]}_r\big)^{(i)}(t,b)
> \;+\;(1{+}r{+}b)\!\!\sum_{i=1}^{p}\frac{(-1)^{i+1}}{i!}\big(\Phi^{[p-i]}_r\big)^{(i)}(t,b)`

The source step `(\ast\ast)` needs no Taylor expansion at all (`a=ns` and
`(n{-}a)/n=1{-}s` are exact), so matching `\varepsilon^p` there is pure algebra:

> **The order-`p` source relation (general `p\ge0`).**
> `\displaystyle \Psi^{[p]}_r(s,b)=[p{=}1]+r\,\Psi^{[p-1]}_{r-1}(s,b{+}1)
> +(1{-}s)\Phi^{[p]}_r(1{-}s,b{+}1)-(1{+}b{+}r)\Phi^{[p-1]}_r(1{-}s,b{+}1)`,
>
> equivalently `\;\eta^{[p]}_r(t,b)=[p{=}1]+r\,\eta^{[p-1]}_{r-1}(t,b{+}1)
> +t\,\Phi^{[p]}_r(t,b{+}1)-(1{+}b{+}r)\Phi^{[p-1]}_r(t,b{+}1)`.

Since the ODE's left side contributes `(k{+}1{+}r{+}b)` to the coefficient of
`t^k`, and `k{+}1{+}r{+}b>0` always, each `\Phi^{[p]}_r` is determined uniquely
as a polynomial once the lower orders and level `r{-}1` are known.

**The ladder is self-starting.** At `r=0` the `\eta`-sum carries the prefactor
`r=0`, so the ODE reads `t(\Phi^{[p]}_0)'+(1{+}b)\Phi^{[p]}_0=[p{=}0]+\cdots`
with only `\Phi^{[j]}_0`, `j<p`, on the right; it gives
`\Phi^{[0]}_0=1/(b{+}1)` and `\Phi^{[p]}_0\equiv0` for `p\ge1` — exactly the
already-known `g_0(m,b)=1/(b{+}1)` — with **nothing hard-coded**. The source
relation then returns `\eta^{[0]}_0=t/(b{+}2)`, `\eta^{[1]}_0=1/(b{+}2)`,
`\eta^{[p]}_0=0` for `p\ge2`, i.e. exactly
`h_0(a,b)=(n{-}a{+}1)/(n(b{+}2))`.

### 2.2 Validation of the scheme one, two and three orders down

The scheme is only worth using if its low orders reproduce what is already
proved. They do:

| `p` | what the general-`p` ODE / relation reduces to | status of that object |
|---|---|---|
| `0` | `tF_r'+(1{+}r{+}b)F_r=1+r\hat H_{r-1}(1{-}t,b)` | **Fact 2**, PROVED, `k6` §2.3 |
| `1` | `tG_r'+(1{+}r{+}b)G_r=r\hat H_{r-1}'+rK_{r-1}+\tfrac t2F_r''+(1{+}r{+}b)F_r'` | **Fact 3**, PROVED, `k6` §3.3 |
| `2` | `tH_r'+(1{+}r{+}b)H_r=r[\tfrac12\hat H_{r-1}''{+}K_{r-1}'{+}L_{r-1}]+\tfrac t2G_r''-\tfrac t6F_r'''+(1{+}r{+}b)[G_r'{-}\tfrac12F_r'']` | Estágio 8 §3.1, PROVED, independently re-derived by its referee (Part 1.2) |
| `2` (source) | `L_r(s,b)=rK_{r-1}(s,b{+}1)+(1{-}s)H_r(1{-}s,b{+}1)-(1{+}b{+}r)G_r(1{-}s,b{+}1)` | idem |

All four come out **character-for-character** identical to the published
statements. Computationally, `core.py`'s smoke test confirms that the
ODE-solved `\Phi^{[0]},\Phi^{[1]},\Phi^{[2]}` equal the PROVED
`c_k^{(r)}(b),d_k^{(r)}(b),e_k^{(r)}(b)` at every `k`, for `r=0,\dots,12`,
`b=0,\dots,4` — `0` mismatches — and that
`F_r(1,0)=\varphi_r`, `G_r(1,0)=r\varphi_r/4`,
`H_r(1,0)=\frac{r(3r+1)}{32}\varphi_r-\frac r{12}` all hold.

### 2.3 The mandated fourth rung `(I_r, M_r)`

Instantiating the two boxed relations at `p=3` (`'` = `d/ds` on the source side):

> **The `I_r` ODE (NEW).**
> `\displaystyle t\,I_r'(t,b)+(1{+}r{+}b)\,I_r(t,b)
> = r\Big[\tfrac16\hat H_{r-1}'''(1{-}t,b)+\tfrac12K_{r-1}''(1{-}t,b)
>       +L_{r-1}'(1{-}t,b)+M_{r-1}(1{-}t,b)\Big]`
> `\displaystyle\qquad\qquad
> +\;t\Big[\tfrac12H_r''(t,b)-\tfrac16G_r'''(t,b)+\tfrac1{24}F_r''''(t,b)\Big]
> \;+\;(1{+}r{+}b)\Big[H_r'(t,b)-\tfrac12G_r''(t,b)+\tfrac16F_r'''(t,b)\Big]`

> **The `M_r` relation (NEW).**
> `\displaystyle M_r(s,b)=r\,L_{r-1}(s,b{+}1)+(1{-}s)\,I_r(1{-}s,b{+}1)-(1{+}b{+}r)\,H_r(1{-}s,b{+}1)`

**Base cases (exact, not asymptotic).** `g_0(m,b)=1/(b{+}1)` exactly, so
`I_0\equiv0`; `h_0(a,b)=(1{-}s)/(b{+}2)+\varepsilon/(b{+}2)` has no
`\varepsilon^3` term at all, so `M_0\equiv0`; and the `M_r` relation reproduces
this (`0\cdot L_{-1}+(1{-}s)I_0-(1{+}b)H_0=0`).

**The first independent confirmation of the new rung, before any pattern
search.** `k3_attempt_2/ATTEMPT.md` §5 proves
`\psi_n^{(3),R}=h_2(0,0)=\frac{11}{30}+\frac{13}{20n}+\frac{23}{60n^2}+\frac1{10n^3}`.
The predecessor used its first three coefficients as its own sixth cross-check
(`\hat H_2(0,0)=11/30`, `K_2(0,0)=13/20`, `L_2(0,0)=23/60`). The fourth
coefficient, `1/10`, had no object to compare against until now. My ladder gives

`M_2(0,0)=\tfrac1{10}` — **exactly**, `core.py` smoke test (g).

---

## 3. The multiplier: it is the unsigned Stirling numbers of the first kind

### 3.1 Reading the multipliers off, before any fitting

All three published orders share one shape — a `k`-dependent multiplier, a
falling factorial, and a denominator product. Assuming only that shape,

`\displaystyle [t^k]\Phi^{[p]}_r(t,b)\;=\;M_p(k)\cdot\frac{r!}{(r{-}k{-}p)!}\cdot\frac1{\prod_{i=1}^{k+p+1}(r{+}b{+}i)}`,

the quantity `M_p(k)` is *over-determined*: it is computed from the ladder at
every `(r,b)` and must come out the same. It does — **6264 `(p,k,r,b)`
instances, `p\le7`, `r\le18`, `b\le5`, `0` inconsistencies**
(`explore_multipliers.log` STAGE 1), together with `\deg\Phi^{[p]}_r=r{-}p`
exactly and `\Phi^{[p]}_r\equiv0` once `p>r` (STAGE 2, `0` violations). The
resulting table:

| `p\backslash k` | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **0** | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **1** | 1 | 3 | 6 | 10 | 15 | 21 | 28 |
| **2** | 2 | 11 | 35 | 85 | 175 | 322 | 546 |
| **3** | 6 | 50 | 225 | 735 | 1960 | 4536 | 9450 |
| **4** | 24 | 274 | 1624 | 6769 | 22449 | 63273 | 157773 |
| **5** | 120 | 1764 | 13132 | 67284 | 269325 | 902055 | 2637558 |
| **6** | 720 | 13068 | 118124 | 723680 | 3416930 | 13339535 | 44990231 |
| **7** | 5040 | 109584 | 1172700 | 8409500 | 45995730 | 206070150 | 790943153 |

Two columns identify the whole table at sight. Column `k=0` is
`1,1,2,6,24,120,720,5040=p!`. Column `k=1` is
`1,3,11,50,274,1764,13068,109584=(p{+}1)!\,H_{p+1}`. Those are `c(p{+}1,1)` and
`c(p{+}2,2)`, the **unsigned Stirling numbers of the first kind**
`c(N,M):=|s(N,M)|` — the number of permutations of `N` letters with `M` cycles.

> **Theorem M (the all-orders multiplier).**
> `\displaystyle [t^k]\Phi^{[p]}_r(t,b)\;=\;c(k{+}p{+}1,\;k{+}1)\cdot\frac{r!}{(r{-}k{-}p)!}\cdot\frac1{\prod_{i=1}^{k+p+1}(r{+}b{+}i)}`,
> `\;0\le k\le r{-}p`, and `0` otherwise.

This is **not four fitted points**. The three already-PROVED multipliers are its
three lowest instances, via three classical identities:

| order | published multiplier | Stirling identification | identity used |
|---|---|---|---|
| `1` | `1` | `c(k{+}1,k{+}1)` | `c(N,N)=1` |
| `1/n` | `\binom{k+2}2` | `c(k{+}2,k{+}1)` | `c(N,N{-}1)=\binom N2` |
| `1/n^2` | `\tfrac{3k+8}4\binom{k+3}3` | `c(k{+}3,k{+}1)` | `c(N,N{-}2)=\tfrac{3N-1}4\binom N3` |
| **`1/n^3`** | **`\binom{k+4}2\binom{k+4}4`** | `c(k{+}4,k{+}1)` | `c(N,N{-}3)=\binom N2\binom N4` |
| `1/n^p` | `c(k{+}p{+}1,k{+}1)` | — | — |

(the `N=k{+}3` and `N=k{+}4` specialisations were verified exactly for
`k=0,\dots,29`, `order_ladder.log` PART 1).

**The mandated fourth rung in closed form:**

> **`\displaystyle I_r(t,b)=\sum_{k=0}^{r-3}\binom{k{+}4}2\binom{k{+}4}4\cdot\frac{r!}{(r{-}k{-}3)!}\cdot\frac{t^k}{\prod_{i=1}^{k+4}(r{+}b{+}i)}`**,
> equivalently multiplier `\frac{(k{+}1)(k{+}2)(k{+}3)^2(k{+}4)^2}{48}`;
>
> **`\displaystyle M_r(s,b)=\sum_{k=0}^{r-2}\binom{k{+}4}2\binom{k{+}4}4\cdot\frac{r!}{(r{-}k{-}2)!}\cdot\frac{(1{-}s)^k}{\prod_{i=1}^{k+3}(r{+}b{+}1{+}i)}`**.

Both verified against the ODE-solved ladder exhaustively: `I_r` at **2233**
`(r,b,k)` triples (`r\le21`, `b\le6`, all `k` including out-of-range), `M_r` at
**920** — `0` mismatches (`order_ladder.log` PART 1). First few:
`I_0=I_1=I_2=0`, `I_3(t,0)=3/70`, `I_4(t,0)=3/35+\tfrac5{63}t`,
`I_5(t,0)=5/42+\tfrac{25}{126}t+\tfrac{25}{308}t^2`.

### 3.2 The resummation — why Stirling numbers are the *right* answer

The Stirling identification is not merely a labelling convenience. Set
`j:=k{+}p`. Then the falling factorial `r!/(r{-}j)!` and the denominator
`\prod_{i=1}^{j+1}(r{+}b{+}i)` depend on `j` alone; only the multiplier
`c(j{+}1,k{+}1)` sees `k` and `p` separately. Writing

`\displaystyle A^{(r)}_j(b):=\frac{r!}{(r{-}j)!}\cdot\frac1{\prod_{i=1}^{j+1}(r{+}b{+}i)}\;=\;c^{(r)}_j(b)`

— i.e. exactly the already-PROVED order-`1` coefficients — the whole double sum
factors:

`\displaystyle \sum_{p\ge0}\varepsilon^p\Phi^{[p]}_r(t,b)
=\sum_{j\ge0}A^{(r)}_j(b)\underbrace{\sum_{k=0}^{j}c(j{+}1,k{+}1)\,t^k\varepsilon^{j-k}}_{(\dagger)}`.

And `(\dagger)` is the classical rising-factorial generating identity
`\sum_M c(N,M)x^M=x(x{+}1)\cdots(x{+}N{-}1)`, homogenised at `N=j{+}1`,
`x=t/\varepsilon`:

`\displaystyle (\dagger)=\frac1t\sum_{M}c(j{+}1,M)t^M\varepsilon^{j+1-M}
=\frac1t\cdot t(t{+}\varepsilon)\cdots(t{+}j\varepsilon)=\prod_{i=1}^{j}(t{+}i\varepsilon)`.

Finally `t{+}i\varepsilon=(m{+}i)/n`, so
`\prod_{i=1}^{j}(t{+}i\varepsilon)=(m{+}j)!/(m!\,n^j)`. Because
`\Phi^{[p]}_r\equiv0` for `p>r`, the `p`-sum is finite and the `j`-sum stops at
`j=r`; the resummation is therefore not a formal manipulation of a divergent
series but a **finite rearrangement**. That gives Theorem A.

---

## 4. Theorem A and Theorem B, with an elementary proof

> **Theorem A (exact, all-orders, general-`r`, general-`b`, finite-`n`).** For
> every `n`, every `r,b\ge0` and every valid `m` (`b{+}r{+}1\le m\le n`),
>
> `\displaystyle g_r(m,b)\;=\;\sum_{j=0}^{r}\frac{r!}{(r{-}j)!}\cdot\frac1{\prod_{i=1}^{j+1}(r{+}b{+}i)}\cdot\frac{(m{+}j)!}{m!\;n^{j}}
> \;=\;\sum_{j=0}^{r}c^{(r)}_j(b)\prod_{i=1}^{j}\Big(t+\frac in\Big)`.
>
> **Theorem B.** For every valid `a` (`0\le a\le n{-}b{-}r{-}1`),
> `\displaystyle h_r(a,b)\;=\;\frac{n{-}a{+}1}{n}\;\hat g_r(n{-}a{+}1,\;b{+}1)`,
> where `\hat g_r(\cdot,b)` denotes the **closed-form expression** of Theorem A.

> **Domain caveat, stated explicitly because a referee will hit it first.** For
> `a\ge1` the argument `m'=n{-}a{+}1` satisfies `b{+}r{+}2\le m'\le n`, so it is
> a genuine state of `g_r(\cdot,b{+}1)` and Theorem B reads as an identity
> between two probabilities. At `a=0` alone, `m'=n{+}1>n` is **outside** the
> probabilistic domain; there Theorem B is an identity between `h_r(0,b)` and
> the closed-form polynomial expression evaluated at `m'=n{+}1`, which is
> perfectly well defined but is not "a value of `g_r`". Nothing in the proof of
> §4.1 evaluates `\hat g` out of domain: there `\hat h_{r-1}(n{-}m{+}1,b)`
> appears only for `b{+}r{+}1\le m\le n`, i.e. `\hat g_{r-1}(\cdot,b{+}1)` is
> evaluated at `m\le n` and `m\ge b{+}r{+}1=(b{+}1)+(r{-}1)+1`, in domain. The
> lineage has met the mirror image of this before — the wave-8 referee's issue
> I-2, where the out-of-domain reference was killed by a coefficient that is
> exactly `0`.

**Binomial form.** With `N:=2r{+}b{+}1`, `\;\frac{r!}{(r-j)!\prod_{i=1}^{j+1}(r+b+i)}=\frac{r!\,(r{+}b)!}{N!}\binom N{r-j}`, so

`\displaystyle g_r(m,b)=\frac{r!\,(r{+}b)!}{(2r{+}b{+}1)!}\sum_{j=0}^{r}\binom{2r{+}b{+}1}{r{-}j}\frac{(m{+}j)!}{m!\,n^{j}}`,
`\qquad
h_r(a,b)=\frac{r!\,(r{+}b{+}1)!}{(2r{+}b{+}2)!}\sum_{j=0}^{r}\binom{2r{+}b{+}2}{r{-}j}\frac{(n{-}a{+}j{+}1)!}{(n{-}a)!\,n^{j+1}}`.

> **Corollary A1 (item (i), the headline instance).**
> `\displaystyle \psi_n^{(K)}=g_K(n,0)=\sum_{j=0}^{K}\frac{(K!)^2}{(K{-}j)!\,(K{+}j{+}1)!}\cdot\frac{(n{+}j)!}{n!\,n^{j}}
> \;=\;\frac{\varphi_K}{4^{K}}\sum_{j=0}^{K}\binom{2K{+}1}{K{-}j}\frac{(n{+}j)!}{n!\,n^{j}}`,
> `\varphi_K=\dfrac{4^K(K!)^2}{(2K{+}1)!}` — a **finite, `K{+}1`-term, fully
> explicit** expression, valid for every `n\ge K{+}1`.

### 4.1 The proof

The proof uses no asymptotics, no ansatz, and no `\varepsilon`-expansion. Write
`A_j:=A^{(r)}_j(b)`, `P_j(m):=(m{+}j)!/m!=\prod_{i=1}^{j}(m{+}i)` (`P_0=1`), and
*define* `\hat g_r(m,b):=\sum_{j=0}^rA_jP_j(m)/n^j` and
`\hat h_r(a,b):=\frac{n-a+1}n\hat g_r(n{-}a{+}1,b{+}1)`. Four elementary facts:

**(P1)** `\;A_j\,(j{+}1{+}r{+}b)=r\,A^{(r-1)}_{j-1}(b{+}1)`. *Proof:* the last
factor of `\prod_{i=1}^{j+1}(r{+}b{+}i)` is `(r{+}b{+}j{+}1)`, so the left side
is `\frac{r!}{(r-j)!}\big/\prod_{i=1}^{j}(r{+}b{+}i)`; and
`r\,A^{(r-1)}_{j-1}(b{+}1)=r\cdot\frac{(r-1)!}{(r-j)!}\big/\prod_{i=1}^{j}(r{+}b{+}i)`
— the same. `\square` **Verified symbolically in `r,j,b`** (Gamma form,
`verify_symbolic.log` S1: `\mathrm{simplify}(\text{LHS}-\text{RHS})=0`).

**(P2)** `\;(1{+}r{+}b)A_0=1`. Immediate; symbolic check S2.

**(P3)** For `j\ge1`: `\;P_j(m)-P_j(m{-}1)=j\,P_{j-1}(m)` and
`\;P_j(m{-}1)=m\,P_{j-1}(m)`. *Proof:* `P_j(m)=(m{+}1)\cdots(m{+}j)` and
`P_j(m{-}1)=m(m{+}1)\cdots(m{+}j{-}1)`; both follow by inspection. `\square`
Symbolic check S3 (Gamma form, symbolic `j`; plus expanded polynomials in `m`
for `j=1,\dots,12`).

**(P4)** The transition system has a **unique** solution on its finite domain
`\{a{+}b{+}r<n\}`, with no boundary condition needed. *Proof:* every recursive
call on either rule increases `a{+}b` by exactly `1` and leaves the state valid,
and `a{+}b\le n{-}1{-}r`; at the top, `a{+}b{+}r=n{-}1`, the "same-`r`"
coefficients `\frac{m-1-r-b}m` and `\frac{n-1-a-b-r}n` are **exactly `0`**, so
the recursion terminates. Induct on `r`, and within each `r` downward on
`a{+}b`. `\square`

Now the computation. By (P3), for `j\ge1`,
`m[P_j(m)-P_j(m{-}1)]=j\,m\,P_{j-1}(m)` and `P_j(m{-}1)=m\,P_{j-1}(m)`, while the
`j=0` term contributes `0` and `A_0` respectively. Hence

`\displaystyle m\big[\hat g_r(m,b)-\hat g_r(m{-}1,b)\big]+(1{+}r{+}b)\hat g_r(m{-}1,b)
=\underbrace{(1{+}r{+}b)A_0}_{=1\ \text{by (P2)}}+\sum_{j=1}^{r}A_j\,(j{+}1{+}r{+}b)\,\frac{m\,P_{j-1}(m)}{n^{j}}`

and by (P1) the sum is
`\displaystyle \sum_{j=1}^{r}r\,A^{(r-1)}_{j-1}(b{+}1)\frac{m\,P_{j-1}(m)}{n^{j}}
=\frac{r\,m}{n}\sum_{l=0}^{r-1}A^{(r-1)}_{l}(b{+}1)\frac{P_l(m)}{n^{l}}
=\frac{r\,m}{n}\,\hat g_{r-1}(m,b{+}1)`.

Since `\hat h_{r-1}(n{-}m{+}1,b)=\frac mn\hat g_{r-1}(m,b{+}1)` by definition,
this is precisely

`\displaystyle m\big[\hat g_r(m,b)-\hat g_r(m{-}1,b)\big]+(1{+}r{+}b)\hat g_r(m{-}1,b)=1+r\,\hat h_{r-1}(n{-}m{+}1,b)`,

i.e. `(\ast)`. And `(\ast\ast)` is the **same identity re-indexed**: applying the
display above at `(r,\,m{=}n{-}a{+}1,\,b{+}1)` and dividing by `n` gives exactly
`\hat h_r(a,b)=\frac1n+\frac rn\hat h_{r-1}(a,b{+}1)+\frac{n-1-a-b-r}n\hat g_r(n{-}a,b{+}1)`.
So `\hat g,\hat h` satisfy both transition rules at every valid state; by (P4)
they *are* `g,h`. `\blacksquare`

**Machine confirmation of the assembled identity, not just its pieces.**
`verify_symbolic.log` S5 and S6 check `(\ast)` and `(\ast\ast)` for the closed
forms with **symbolic `m`, `a`, `n`, `b`** at `r=0,\dots,9`:
`\mathrm{simplify}(\text{LHS}-\text{RHS})=0` in all 20 cases.

### 4.2 Theorem M is now a corollary, not a conjecture

Expanding `\prod_{i=1}^{j}(t{+}i\varepsilon)` by §3.2 and reading off the
`t^k\varepsilon^{j-k}` coefficient turns Theorem A into Theorem M; the
coefficient is the elementary symmetric polynomial `e_{j-k}(1,2,\dots,j)`, which
is `c(j{+}1,k{+}1)`. Checked as a two-variable polynomial expansion for
`j=0,\dots,13`, all `k`, `0` failures (S7); the analogous statement on the
`h`-side (`\Psi^{[p]}_r(s,b)=\sum_k c(k{+}p{+}1,k{+}1)A^{(r)}_{k+p-1}(b{+}1)(1{-}s)^k`)
at **328** symbolic checks, `0` failures (S8).

### 4.3 Corollaries about the expansion itself

> **Corollary A2 (the expansion terminates; there is no error term).** For every
> `r,b,n` and every valid `m`,
> `\;g_r(m,b)=\sum_{p=0}^{r}\varepsilon^p\Phi^{[p]}_r(t,b)` **exactly**, and
> `\;h_r(a,b)=\sum_{p=0}^{r+1}\varepsilon^p\Psi^{[p]}_r(s,b)` exactly. Hence the
> `p`-term truncation residual is *exactly* its own tail,
> `\;R^{(p)}_r(m,b,n)=\sum_{q=p}^{r}\varepsilon^q\Phi^{[q]}_r(t,b)`, and is
> **identically zero once `p>r`**.
>
> Verified at **34 907** exact points (`n\le22`, `r\le7`, `b\le4`, every valid
> `m`, every `p\le r{+}2`), `0` mismatches and `0` cases where a `p>r` residual
> was nonzero (`order_ladder.log` PART 3).

This subsumes, and is strictly sharper than, the existence statements the
lineage has been proving: Estágio 6's Target Theorem (`|R_r|\le D_r(b)/n^2`
uniformly) and Estágio 8's Theorem 2 (`|R^{(3)}_r|\le D^{(3)}_r(b)/n^3`) are
both immediate, with the *sharp* constants below. **Neither is contradicted** —
they are true bounds; they were simply not tight, which is exactly what Estágio
8 measured.

> **Corollary A3 (the sharp residual constants, all orders).** Every
> coefficient `c(k{+}p{+}1,k{+}1)>0`, so `\Phi^{[p]}_r(\cdot,b)` is increasing
> on `[0,1]` and its maximum sits at `t=1`, which is on the grid for every `n`.
>
> > **[Correção pós-adversarial, 2026-08-23, N-3 de `adversarial/REFEREE_REPORT.md`
> > Parte 4.]** "Increasing" deveria ler **"non-decreasing"** — em `r=p` o
> > polinômio `\Phi^{[p]}_r` é uma constante positiva, não estritamente
> > crescente. A conclusão (máximo em `t=1`) é inafetada, já que uma constante
> > também atinge seu máximo ali.
>
> Hence
> `\displaystyle D^{*(p)}_r(b):=\lim_{n\to\infty}\max_m n^p\big|R^{(p)}_r(m,b,n)\big|=\Phi^{[p]}_r(1,b)=\sum_{j=p}^{r}c^{(r)}_j(b)\,c(j{+}1,\,j{+}1{-}p)`,
> the inner factor being `e_p(1,2,\dots,j)`.
>
> `p=0,1,2` recover `\varphi_r`, `\frac r4\varphi_r`, and Estágio 8's
> Theorem 3 `\frac{r(3r+1)}{32}\varphi_r-\frac r{12}` — each verified exactly
> for `r=0,\dots,60` (`corollaries.log` C3), and the `p=2` case additionally for
> `r=0,\dots,89` and against the predecessor's general-`b` table
> (`cross_checks.log` X6, X8).

---

## 5. Numerical corroboration, consolidated

All exact unless stated. Logs retained.

| check | scope | result |
|---|---|---|
| my ladder's order 0/1/2 vs the **PROVED** `c_k,d_k,e_k` | `r\le12`, `b\le4`, all `k` | `0` mismatches (`core.py`) |
| my simulator vs **PROVED** `\psi_n^{(1)},\psi_n^{(2)}`; `g_6(7,0)=355081/823543` | `n\le9`; the brute-forced value | exact (`core.py`) |
| `\hat H_2(0,0),K_2(0,0),L_2(0,0)` **and the new** `M_2(0,0)=1/10` vs **PROVED** `\psi_n^{(3),R}` | — | all four exact |
| multiplier `M_p(k)` is `r,b`-independent | `p\le7,r\le18,b\le5` | **6264** instances, `0` inconsistencies |
| `\deg\Phi^{[p]}_r=r{-}p`; `\Phi^{[p]}_r\equiv0` for `p>r` | idem | `0` violations |
| **Theorem M** vs the ODE ladder | `p\le8`, `r\le20`, `b\le6`, all `k` incl. out-of-range | **18 522** exact checks, `0` mismatches |
| `I_r`, `M_r` (the mandated rung) vs the ladder | `r\le21,b\le6` / `r\le15,b\le4` | **2233** + **920**, `0` mismatches |
| **Theorem A** vs my exact simulator | every valid `m`, `n\le26`, `r\le8`, `b\le6` | **12 305**, `0` |
| **Theorem B** vs my exact simulator | every valid `a`, same range | **12 305**, `0` |
| both, larger sweep | `n\le33`, `r\le10`, `b\le8` | **61 048**, `0` |
| both binomial forms vs simulator | `n\le25`, `r\le8`, `b\le6` | **22 216**, `0` |
| (P1) symbolic in `r,j,b`; (P2); (P3) symbolic in `m,j` | — | all `=0` (S1–S3) |
| Stirling generating identity, own implementation | `j\le15`; vs `sympy.stirling`, `N\le17` | `0` failures (S4) |
| `(\ast)` for the closed form, **symbolic `m,n,b`** | `r=0..9` | `0` failures (S5) |
| `(\ast\ast)` for the closed form, **symbolic `a,n,b`** | `r=0..9` | `0` failures (S6) |
| Theorem A `\Rightarrow` Theorem M (2-variable expansion) | `j\le13`, all `k` | `0` failures (S7) |
| `h`-side all-orders closed form, symbolic | `r\le7` | **328**, `0` failures (S8) |
| residual `=` exactly its tail; `\equiv0` for `p>r` | `n\le22,r\le7,b\le4`, all `m`, all `p` | **34 907**, `0` |
| `h`-side termination: `\Psi^{[p]}_r\equiv0` for `p>r{+}1`, and `h_r=\sum_{p=0}^{r+1}\varepsilon^p\Psi^{[p]}_r` exactly | `r\le9,b\le3`; then `n\le19,r\le6,b\le3`, all `a` | `0` violations; **3215**, `0` |
| `\psi_n^{(1)},\dots,\psi_n^{(5)}` (**PROVED** elsewhere, different method) | `n\le39` | all exact |
| `\psi_n^{(3),R}` (**PROVED** elsewhere) | `n\le39` | exact |
| `\varphi_K`; `K\varphi_K/4`; Estágio 8 Thm 3 | `K\le39`; `K\le39`; `K\le89` | all exact |
| Estágio 7's `c_K=((K{+}2)\varphi_K-2)/4` via Reduction Lemma A | `K\le29`, incl. `c_1{=}0,c_2{=}\tfrac1{30},c_3{=}\tfrac1{14},c_6{=}\tfrac{1093}{6006}` | all exact |
| Estágio 8's general-`b` `D^*_r(b)` printed table | 8 entries, `r=10,10^2`, `b\le3` | reproduced to printed precision |
| `D^{*(p)}_r(0)` closed forms (fitted, then tested out of sample) | `p\le5`, `r\le300` | `0` failures |

**New exact outputs of Corollary A1** (`corollaries.log` C2). `K=1,\dots,5`
reproduce the published PROVED formulas verbatim; `K=6,7,8` are new:

`\psi_n^{(6)}=\dfrac{2048n^6+3072n^5+4293n^4+4638n^3+3529n^2+1662n+360}{6006\,n^6}`

`\psi_n^{(7)}=\dfrac{16384n^7+28672n^6+48818n^5+67550n^4+70819n^3+52192n^2+23868n+5040}{51480\,n^7}`

`\psi_n^{(8)}=\dfrac{32768n^8+65536n^7+131870n^6+223472n^5+300913n^4+306016n^3+219100n^2+97632n+20160}{109395\,n^8}`

(their `1/n^2` coefficients `1431/2002` and `2219/2340` are exactly the two
values Estágio 8 §7.1 reported as *"not in any prior document"* — a seventh
independent agreement with that document, by a different route).

**The sharp constants at the new order** (`dstar_orders.log`), each fitted on the
minimum number of points and then confirmed exactly out to `r=300`:

| `p` | `D^{*(p)}_r(0)` | status |
|---|---|---|
| `0` | `\varphi_r` | PROVED (this document + already known) |
| `1` | `\tfrac r4\varphi_r` | PROVED |
| `2` | `\tfrac{r(3r+1)}{32}\varphi_r-\tfrac r{12}` | PROVED (Estágio 8 Thm 3) |
| **`3`** | `\tfrac{5r^3+9r^2+2r}{128}\varphi_r-\tfrac{r^2}{12}` | **NUMERICALLY VERIFIED**, `r\le300` |
| **`4`** | `\tfrac{105r^4+610r^3+123r^2-70r}{6144}\varphi_r-\tfrac{r^3}{16}-\tfrac{7r^2}{240}+\tfrac r{120}` | **NUMERICALLY VERIFIED**, `r\le300` |
| **`5`** | `\tfrac{189r^5+2590r^4+855r^3-490r^2-72r}{24576}\varphi_r-\tfrac{r^4}{24}-\tfrac{3r^3}{40}+\tfrac{r^2}{30}` | **NUMERICALLY VERIFIED**, `r\le300` |

with the leading coefficients `1,\ \tfrac14,\ \tfrac3{32},\ \tfrac5{128},\
\tfrac{35}{2048},\ \tfrac{63}{8192}` matching `\dfrac{(2p{-}1)!!}{4^p\,p!}`
(NUMERICALLY CHARACTERIZED, `p\le5`).

---

## 6. What this resolves, precisely, and what it does not

### 6.1 Relative to the mandate

The mandate asked for a fourth data point in the multiplier sequence, and
explicitly pre-authorised the outcome *"no discernible pattern; the item remains
genuinely open."* That is not what happened: the fourth multiplier is
`\binom{k+4}2\binom{k+4}4`, and the *identification* `M_p(k)=c(k{+}p{+}1,k{+}1)`
is confirmed at orders `p=0,\dots,8` — nine orders, not four — and then proved.
The distinction matters and I want it on the record: this is **not** a curve fit
to four points. The claim rests on (a) `18\,522` exact ladder checks across nine
orders, and (b) an independent proof (§4) that never touches the multipliers.

### 6.2 Relative to open item (i)

`k6_attempt/ATTEMPT.md` §6.2 defines item (i) as *"the exact finite-`n` closed
form for general `K`, which would need all `K{+}1` orders resummed"*, and asks
whether the `c_k`/`d_k` pattern *"continues in a similarly closed-form-guessable
way at every order."* Corollary A1 is the first; Theorem M is the second. What
this document supplies that the lineage did not previously have:

- a **closed form**, not an algorithm. `k3_attempt_2/ATTEMPT.md` §3's
  telescoping ladder is `K`-uniform as a *procedure* (one `sympy.summation` per
  rung), which is why the archive has `\psi_n^{(1)},\dots,\psi_n^{(5)}` as five
  separate outputs rather than one formula. Corollary A1 is a single expression
  in `K` and `n`;
- a general-`b`, general-`m` statement (Theorem A), not only `t=1,b=0`;
- the source side too (Theorem B), which is a *simplification* — `h_r` is a
  single rescaled evaluation of `g_r`, with no separate ladder at all;
- the all-orders multiplier (Theorem M), which is what item (i)'s second half
  literally asked about.

### 6.3 What this does **not** do

1. **It does not re-derive the transition rules** from the probabilistic model.
   Those are taken as PROVED input from `k3_attempt_2/ATTEMPT.md` §2 (which
   validated them by exhaustive brute force against the raw definition). Every
   statement here is a statement about *that recursion*.
2. **It proves nothing uniform in `K`.** Corollary A1 is an identity at each
   fixed `K`; no bound uniform in `K`, no interchange of `K\to\infty` with
   `n\to\infty`, is claimed or used anywhere.
3. **It does not close the `b\ge1` closed form for `D^{*(p)}_r(b)`.** Fitting
   the same `\{r^q\varphi_r\}\cup\{r^q\}` basis at `b=1,2,3` **fails** out of
   sample (54–56 failures out of 61 tested `r`), at `p=2` as well as `p=3` —
   the same phenomenon the predecessor reported (§8.3 item 2 there), so the
   route to `b\ge1` remains the referee's Theorem 3′-style prefactor collapse,
   not a naive fit. Reported as OPEN, not forced.

   > **[Correção pós-adversarial, 2026-08-23,
   > `adversarial/REFEREE_REPORT.md` Parte 5.]** **Este item está errado em
   > `b=1`.** A basis NÃO falha em `b=1` — ela representa `D^{*(p)}_r(1)`
   > **exatamente**, para `p=1,2,3,4`, com `0` falhas fora-da-amostra até
   > `r=400`. O caso `p=2` não é sequer um ajuste — é o Teorema 3′ do referee
   > da onda 10 (`error_constant_growth_attempt/adversarial/REFEREE_REPORT.md`
   > §3.3) especializado em `b=1`, já **PROVADO**. As "54–56 falhas de 61"
   > reportadas acima são exatamente os números de `b=2` e `b=3`, não de
   > `b=1` — o referee reproduziu-as textualmente sob esses dois valores. A
   > razão estrutural: o prefator de Teorema 3′,
   > `\Phi_b(r)=2\varphi_r\prod_{j=1}^b\frac{2r+2j}{2r+j+1}`, colapsa para uma
   > constante `2\varphi_r` exatamente em `b\in\{0,1\}` (o fator único de
   > `b=1` é `\frac{2r+2}{2r+2}=1` identicamente) e deixa de ser polinomial a
   > partir de `b=2` — daí a basis funcionar em `b\le1` e falhar
   > estruturalmente (não por tamanho de basis insuficiente, confirmado até
   > `\deg_\varphi\le p{+}6`) em `b\ge2`. **Enunciado corrigido: a basis
   > existe para `b=0` e `b=1`, e é REFUTADA para `b\ge2`.** Formas fechadas
   > exatas em `b=1` (`p=2` PROVADA via Teorema 3′; `p=1,3,4` NUMERICALMENTE
   > VERIFICADAS a `r=400`):
   > `D^{*(1)}_r(1)=\frac{r+1}4\varphi_r-\frac14`,
   > `D^{*(2)}_r(1)=\frac{(r+1)(3r+8)}{32}\varphi_r-\frac{5r+6}{24}`,
   > `D^{*(3)}_r(1)=\frac{(r+1)(5r^2+39r+32)}{128}\varphi_r-\frac{(r+1)(7r+12)}{48}`,
   > `D^{*(4)}_r(1)=\frac{(r+1)(105r^3+1765r^2+3314r+1536)}{6144}\varphi_r-\frac{45r^3+229r^2+306r+120}{480}`.
   > `b\ge2` permanece OPEN, e para ele a rota recomendada acima (colapso de
   > prefator estilo Teorema 3′, não ajuste ingênuo) continua correta.
4. **The `p\ge3` forms of `D^{*(p)}_r(0)` are fits**, not proofs. They are
   verified exactly out to `r=300` (fitted on `2p{+}1` points), which is strong
   evidence, but the honest label is NUMERICALLY VERIFIED. The proof route is
   known and mechanical — `D^{*(p)}_r(0)=\frac{\varphi_r}{4^r}\sum_j\binom{2r+1}{r-j}Q_p(j)`
   with `Q_p(j)=e_p(1..j)` a degree-`2p` polynomial, so Estágio 8 §5.1's
   odd/even half-range split applies, needing binomial central moments up to
   order `2p`. Not carried out here.
5. **It does not change the status of anything already catalogued.** Teorema 3,
   the Estágio 6 existence theorem, the Estágio 7 rate coefficient and the
   Estágio 8 growth rate are all untouched and all remain true; this document
   only makes them corollaries of a sharper object. In particular the
   `\Theta(r^{3/2})` growth of Estágio 8 is unaffected (it is a statement about
   `D^{*(2)}_r(b)`, which is reproduced here exactly).
6. **No independent adversarial re-verification has been performed** (§6.4).

### 6.4 The one thing a hostile referee should attack first

Everything in §3 and §5 is downstream of two things, and both are short enough
to be re-derived from scratch:

- **§4.1, the proof of Theorem A.** It is four elementary facts and one page of
  algebra. A referee should re-derive (P1)–(P4) independently, and independently
  re-check that `\hat g,\hat h` satisfy `(\ast)` and `(\ast\ast)` — ideally with
  a from-scratch simulator, since that check is a pure identity and needs no
  cleverness at all. **If Theorem A survives, everything else in this document
  follows mechanically**, including Theorem M (§4.2) and the mandated `I_r`.
- **§2.1, the general-`p` `\varepsilon`-matching.** This is the object the
  mandate actually commissioned. Three things make it checkable: its `p=0,1,2`
  instances must reproduce Facts 2 and 3 and Estágio 8's boxed `H_r` ODE /`L_r`
  relation character-for-character (they do); its `p=3` instance must produce an
  `M_2(0,0)` equal to `1/10`, the `1/n^3` coefficient of the already-PROVED
  `\psi_n^{(3),R}` (it does); and it is *logically independent* of §4 — if §2
  and §4 disagree anywhere, one of them is wrong, and they agree at 18 522
  points.

A specific place to be suspicious, which I flag rather than hide: **the sign
handling in §2.1**. Under `s=1{-}t` one has `d/ds=-d/dt`, and my first draft of
the order-`p` ODE had this wrong; it was caught only because the `p=1` instance
failed to reproduce Fact 3 (recorded in `PROGRESS.log` [8]). A referee should
re-derive those signs independently rather than reading mine.

**No independent adversarial re-verification of this document has been
performed.** Per the archive's standing discipline a positive result of this
size requires a dedicated hostile referee who re-derives §2.1 and §4.1 from
scratch — own `\varepsilon`-expansion, own simulator, own closed form — *before*
reading how this document derives them, and only then may integration into
`THEOREM.md` be considered. **I do not claim item (i) is closed, catalogued, or
integrated. I claim it is answered and ready for review.**

### 6.5 Scope discipline

No file outside this directory was created, modified, or deleted. `THEOREM.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
`README*.md`, `PROOF_DEPENDENCY_MAP.md`, `tamesis-cycle-survival/`, my parent
`error_constant_growth_attempt/ATTEMPT.md` and its `adversarial/` subfolder, and
every other predecessor `ATTEMPT.md`/`REFEREE_REPORT.md` are untouched (read
only). No git commit was made. No code was imported or copied from any sibling
or predecessor directory.

---

## 7. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | The general-order `\varepsilon`-matching: the order-`p` receiver ODE and source relation (§2.1) | **PROVED** by the same exact-finite-Taylor mechanism as the orders below it (every Taylor expansion terminates; the shift `s=(1{-}t){+}\varepsilon` is exact). Its `p=0,1,2` instances reproduce PROVED Facts 2/3 and Estágio 8's `H_r` ODE / `L_r` relation character-for-character. Not independently re-derived by a second party (§6.4) — **[Correção pós-adversarial, 2026-08-23, N-1]: para consistência com as linhas 4/5/9, mais preciso ler "PROVED given claim 6" — como ladder formal está bem definido, mas como afirmação *sobre* `g_r` precisa que a expansão exista e termine (Corolário A2), o que por sua vez depende do Teorema A. Ver Parte 8 do referee report; não afeta nenhuma conclusão.** |
| 2 | The `I_r` ODE and the `M_r` relation — **the mandated fourth rung** (§2.3) | **PROVED given claim 1** (its `p=3` instance). Independently corroborated by `M_2(0,0)=1/10`, the `1/n^3` coefficient of the already-PROVED `\psi_n^{(3),R}`, which no prior document had an object for |
| 3 | The multiplier `M_p(k)` is independent of `r` and `b` (§3.1) | **NUMERICALLY VERIFIED**, exact — 6264 `(p,k,r,b)` instances, `p\le7,r\le18,b\le5`, `0` inconsistencies; and a corollary of claim 6 once that is granted |
| 4 | `\deg\Phi^{[p]}_r=r{-}p`, and `\Phi^{[p]}_r\equiv0` for `p>r` (the series terminates) | **PROVED given claim 6**; independently NUMERICALLY VERIFIED, `0` violations over the same sweep |
| 5 | **Theorem M**: `[t^k]\Phi^{[p]}_r(t,b)=c(k{+}p{+}1,k{+}1)\frac{r!}{(r-k-p)!}\prod_{i=1}^{k+p+1}(r{+}b{+}i)^{-1}` | **PROVED given claim 6** (§4.2, via the homogenised rising-factorial identity, symbolic check S7). Independently verified against the ODE ladder at **18 522** exact `(p,r,b,k)` checks, `p\le8`, `0` mismatches. Its `p=0,1,2` slices **are** the three already-PROVED multipliers, via `c(N,N)=1`, `c(N,N{-}1)=\binom N2`, `c(N,N{-}2)=\frac{3N-1}4\binom N3` |
| 6 | **Theorem A**: `g_r(m,b)=\sum_{j=0}^{r}c^{(r)}_j(b)\,(m{+}j)!/(m!\,n^{j})`, exact, every valid `m,b,r,n` | **PROVED** (§4.1) — elementary: (P1) verified symbolically in `r,j,b`, (P2)–(P3) elementary and symbolically checked, (P4) well-foundedness. The assembled identity `(\ast)` verified with **symbolic `m,n,b`** for `r=0..9`. Exhaustively confirmed against a from-scratch exact simulator at **61 048** points |
| 7 | **Theorem B**: `h_r(a,b)=\frac{n-a+1}{n}g_r(n{-}a{+}1,b{+}1)` | **PROVED** (§4.1; `(\ast\ast)` is `(\ast)` re-indexed), symbolic check S6, same exhaustive simulator confirmation |
| 8 | **Corollary A1** (item (i)): `\psi_n^{(K)}=\frac{\varphi_K}{4^K}\sum_{j=0}^{K}\binom{2K+1}{K-j}\frac{(n+j)!}{n!\,n^{j}}` | **PROVED given claim 6.** Reproduces the five independently-derived PROVED `\psi_n^{(K)}` formulas exactly (`K\le5`, `n\le39`), the brute-force-confirmed `g_6(7,0)`, and Estágio 8's two "not in any prior document" values `1431/2002`, `2219/2340` |
| 9 | **Corollary A2**: the `1/n` expansion terminates at order `r`; the `p`-term residual is exactly its own tail and `\equiv0` for `p>r` | **PROVED given claim 6**; NUMERICALLY VERIFIED at **34 907** exact points, `0` mismatches. Strictly sharper than — and consistent with — Estágio 6's Target Theorem and Estágio 8's Theorem 2, neither of which is contradicted |
| 10 | **Corollary A3**: `D^{*(p)}_r(b)=\Phi^{[p]}_r(1,b)` for every `p` (all coefficients positive, `t=1` on the grid at every `n`) | **PROVED given claims 5, 6, 9**. Recovers `\varphi_r`, `\frac r4\varphi_r` and Estágio 8's Theorem 3 exactly (`r\le89`) and its general-`b` table |
| 11 | `D^{*(3)}_r(0)=\frac{5r^3+9r^2+2r}{128}\varphi_r-\frac{r^2}{12}`, and the analogous `p=4,5` forms | **NUMERICALLY VERIFIED** — exact rational, fitted on `2p{+}1` points and confirmed exactly for `r=0,\dots,300`. **Not proved**; the proof route is named (§6.3 item 4) but not carried out — **[Correção pós-adversarial, 2026-08-23]: agora PROVADO.** O referee executou a rota nomeada (teorema de estrutura `D^{*(p)}_r(0)=U_p(r)\varphi_r+V_p(r)` via a mesma técnica de momentos binomiais par/ímpar de Estágio 8, mais interpolação em `2p{+}1` pontos com matriz não-singular verificada) e confirma exatamente os `p=3,4,5` publicados, mais novas formas `p=6,7`. Ver `adversarial/REFEREE_REPORT.md` Parte 6. |
| 12 | The leading-in-`r` coefficient of `D^{*(p)}_r(0)` is `\frac{(2p-1)!!}{4^p p!}` | **NUMERICALLY CHARACTERIZED**, `p\le5` — a pattern in `p` over six points, deliberately **not** promoted — **[Correção pós-adversarial, 2026-08-23]: agora PROVADO** em duas linhas a partir do teorema de estrutura da linha 11 (o bloco par carrega o termo líder via o `2p`-ésimo momento gaussiano `(2p{-}1)!!`; o bloco ímpar é livre de `\varphi_r` e não pode tocar o coeficiente líder). Ver `adversarial/REFEREE_REPORT.md` Parte 7. |
| 13 | A closed form for `D^{*(p)}_r(b)` at `b\ge1` in the `\{r^q\varphi_r\}\cup\{r^q\}` basis | **REFUTED for that basis** (54–56 out-of-sample failures out of 61, at `p=2` and `p=3` alike) — hence **OPEN** in general, exactly as the predecessor left it — **[Correção pós-adversarial, 2026-08-23]: ERRADO em `b=1`.** As "54–56 falhas" reportadas são exatamente os números de `b=2` e `b=3`; em `b=1` a basis é **exata** para `p=1,2,3,4` (`0` falhas a `r=400`), e o caso `p=2` já era **PROVADO** pelo Teorema 3′ do referee da onda 10, especializado em `b=1` — a frase "exactly as the predecessor left it" está errada, pois o próprio predecessor já havia fechado esse caso. Enunciado correto: a basis existe em `b\in\{0,1\}` e é REFUTADA para `b\ge2`. Ver §6.3 item 3 acima (correção completa com as quatro formas fechadas de `b=1`) e `adversarial/REFEREE_REPORT.md` Parte 5. |
| 14 | Anything uniform in `K` | **NOT CLAIMED** — every statement is at fixed `K` (equivalently fixed `r`) |
| 15 | Re-derivation of the `(a,b,r)` transition rules from the probabilistic model | **NOT ATTEMPTED** — taken as PROVED input (§0, §6.3 item 1) |
| 16 | Independent adversarial re-verification of this document | **NOT PERFORMED** — required before any integration (§6.4) |

**Net honest verdict.** The mandate's narrow question — *is there a fourth term
in the multiplier sequence, or is the item genuinely open beyond the current
order?* — is answered decisively in the first sense: the multiplier at order
`1/n^p` is the unsigned Stirling number of the first kind `c(k{+}p{+}1,k{+}1)`,
whose `p=0,1,2` instances are precisely the three multipliers already proved,
and whose `p=3` instance `\binom{k+4}2\binom{k+4}4` gives the mandated `I_r`.
Because those multipliers are exactly the coefficients of a rising factorial,
the `\varepsilon`-series resums to `\prod_{i=1}^{j}(t{+}i/n)` and — since it
terminates at order `r` — the resummation is an **exact, finite, general-`K`,
general-`b`, general-`m` closed form** (Theorem A), which is what open item (i)
asks for. Theorem A additionally admits a short elementary proof that bypasses
the `\varepsilon`-machinery entirely, so the two derivations are independent
confirmations of each other. This is a **positive** result and is therefore
**not** catalogued here: it requires the archive's mandatory hostile-referee
pass first, focused on §4.1 and §2.1 (§6.4). Nothing in this document weakens
any existing result; several of them become corollaries.

---

## 8. Files, reproducibility

All scripts were written from scratch in this directory; nothing is imported
from any sibling or predecessor directory. All use exact
`fractions.Fraction` / `sympy.Rational` / `sympy.Symbol` arithmetic; floating
point appears only in display columns and in one tolerance comparison against a
predecessor's *printed* table (`cross_checks.py` X8).

| file | contents | runtime |
|---|---|---|
| `core.py` / `.log` | own `Poly` type; the **general-order** `Ladder` (§2.1, self-starting, nothing hard-coded); own exact `(a,b,r)` `Chain` simulator; the re-transcribed PROVED `c_k,d_k,e_k` closed forms used **only** as ground-truth checks; smoke tests | ~1 s |
| `explore_multipliers.py` / `.log` | §3.1: `r,b`-independence of `M_p(k)`, degree/vanishing checks, the multiplier table, the `(2p{-}1)!!` normalisation | ~1 s |
| `verify_closed_form.py` / `.log` | §3, §4: own Stirling implementation + its sanity checks; Theorem M vs the ladder (18 522); Theorems A/B vs the simulator (12 305 + 12 305); `\psi_n^{(1..4)}`, `\psi_n^{(3),R}`; `\varphi_K` | ~4 s |
| `verify_symbolic.py` / `.log` | §4: S1 (the pivot identity, **symbolic `r,j,b`**), S2, S3, S4 (Stirling generating identity), S5/S6 (the assembled `(\ast)`/`(\ast\ast)`, **symbolic `m,a,n,b`**, `r=0..9`), S7, S8 | ~5 min |
| `order_ladder.py` / `.log` | §2.3, §3.1, §4.3: the mandated `I_r`/`M_r` rung (2233 + 920); the multiplier ladder table; residual-is-exactly-the-tail (34 907); `D^{*(p)}_r(b)`; the `h`-side termination (3215) | ~4 s |
| `cross_checks.py` / `.log` | §5: 17/17 confrontations with every published exact fact of this lineage, plus a 61 048-point exhaustive simulator sweep | ~3 s |
| `corollaries.py` / `.log` | §4: the binomial forms; `\psi_n^{(K)}` written out for `K=0..8`; the `D^{*(p)}` identities | ~2 s |
| `dstar_orders.py` / `.log` | §5: `D^{*(p)}_r(0)` closed forms `p\le5`, fitted then tested exactly to `r=300`; the `b\ge1` failure | ~8 s |
| `PROGRESS.log` | chronological checkpoint trail, with the by-hand derivations recorded *before* the corresponding code, and a self-caught sign error | — |

Reproduce in this order: `python3 core.py`; `python3 explore_multipliers.py 7 18 5`;
`python3 verify_closed_form.py 8 20 6 26`; `python3 order_ladder.py 22`;
`python3 cross_checks.py`; `python3 corollaries.py`; `python3 dstar_orders.py 5 300`;
`python3 verify_symbolic.py 9 12` (slowest, ~5 min).
