# The growth rate in `r` of the residual error constants: the true constant is `Θ(r^{3/2})`, with an exact closed form at `b=0`

> **Governance.** Wave 10, front (b), authorized by `DISC-DEC-045`
> (`K-GENERAL-ERROR-CONSTANT-GROWTH-ATTEMPT`). Target: item **(ii)** of the "what
> remains open" list of `THEOREM.md` Estágio 6 / Estágio 7 — *"a taxa de
> crescimento em `r` das constantes de erro `D_r(b),C_r(b)` do novo documento
> (nomeada, não perseguida — os números observados são muito menores que os
> limitantes, ex. `0,78` observado contra `174` de limitante em `r=6`, mas nenhuma
> forma fechada para o crescimento foi buscada)"*. Pure combinatorial /
> asymptotic mathematics — no external data, no holdout, no real-world claim, no
> governance edits. **Nothing outside this directory was modified.** No git commit
> was made. Every claim below is labeled PROVED, PROVED-MODULO-[X] (X named
> precisely), NUMERICALLY CHARACTERIZED, NUMERICALLY VERIFIED, or OPEN.

> **Executive summary (read first).** The attempt succeeds, on both sub-goals, and
> further than the brief anticipated.
>
> 1. **The true constant has an exact closed form.** Pushing the same `ε`-matching
>    that produced `F_r` (order `1`) and `G_r` (order `1/n`) one order further
>    produces a third-order pair `(H_r, L_r)`; `H_r(t,b)` has the closed form
>    `e_k^{(r)}(b) = \tfrac{(3k+8)(k+1)(k+2)(k+3)}{24}\cdot\frac{r!}{(r-k-2)!}\cdot
>    \frac1{\prod_{i=1}^{k+3}(r+b+i)}`, which slots exactly into the already-proved
>    `c_k^{(r)}(b)`, `d_k^{(r)}(b)` family and is verified here to the same standard
>    (`sympy`, symbolic `r,k,b`, `0`). Every coefficient is positive, so
>    `\max_{t\in[0,1]}|H_r(t,b)| = H_r(1,b)`, and at `b=0`
>
>    > `\displaystyle D^*_r(0)\;=\;H_r(1,0)\;=\;\frac{r(3r+1)}{32}\,\varphi_r\;-\;\frac r{12}`
>
>    exactly, `\varphi_r` the same Wallis mean as everywhere else in this lineage.
>    This is verified against **six independent** already-proved exact facts
>    (`ψ_n^{(1)},\dots,ψ_n^{(5)}` and `ψ_n^{(3),R}`), each derived elsewhere by a
>    completely different method.
> 2. **The growth rate is therefore exactly `Θ(r^{3/2})`**, with explicit constant:
>    `D^*_r(b) = \frac{3\sqrt\pi}{64}r^{3/2} - \frac r{12} + O(\sqrt r)`, **the
>    leading constant being the same for every fixed `b`** (`3\sqrt\pi/64 =
>    0.0830838\ldots`). Confirmed numerically to `r=10^5` (log-log slope `1.5022`
>    at `b=0`; `D^*_r(0)` agreeing with the two-term asymptote to `7` figures).
>    `r=0` and `r=1` give **exactly `0`** — the structural explanation of the
>    target document's observed "`R_1\equiv0` identically".
>
>    > **[Correção pós-adversarial, 2026-08-23, F-1/F-2 de
>    > `adversarial/REFEREE_REPORT.md` Parte 4.]** Este parágrafo, como
>    > escrito, está **errado em dois pontos específicos** (não na conclusão
>    > `Θ(r^{3/2})`, constante `3\sqrt\pi/64`, que sobrevive intacta e agora é
>    > **PROVADA incondicionalmente para todo `b`**, não apenas
>    > "PROVED-MODULO"). (i) O termo `O(\sqrt r)` escondia um coeficiente
>    > **errado** publicado no Teorema 4 abaixo (ver correção lá: o sinal e a
>    > magnitude do termo `r^{1/2}` estavam errados — os próprios números do
>    > §5.2 deste documento, a razão aproximando `1` **por baixo**, já
>    > refutavam o termo publicado, positivo). (ii) A frase "a mesma para todo
>    > `b` fixo" aplica-se apenas à constante líder `3\sqrt\pi/64`; o
>    > coeficiente do termo *linear* em `r`, aqui escrito como `-r/12` sem
>    > qualificação, é **exatamente `-(3b+2)/24`** e portanto depende de `b`
>    > (`-1/12` apenas em `b=0`) — o erro de tratar `-r/12` como válido para
>    > todo `b` é `Θ(br)`, não `O(\sqrt r)`. O referee derivou a forma fechada
>    > exata `D^*_r(b)` para todo `b` (o próprio item aberto §8.3(2) abaixo,
>    > agora fechado) e a partir dela ambas as correções seguem
>    > algebricamente, sem estimativa assintótica. A sessão orquestradora
>    > verificou independentemente as duas correções por conta própria (soma
>    > direta de `H_r(1,b)` via a fórmula fechada do Teorema 1, ponto flutuante
>    > vetorizado, `r` até `2\times10^7`): a razão `[D^*_r(b)-\text{termo
>    > líder}]/r` converge para `-(3b+2)/24` em `b=0,1,2,3` (ex. `-0.08333,
>    > -0.20825, -0.33316, -0.45800` em `r=2\times10^7`, contra previstos
>    > `-0.08333, -0.20833, -0.33333, -0.45833`), e o termo `r^{1/2}` em `b=0`
>    > converge para `-\sqrt\pi/512=-0.0034618239\ldots` (não
>    > `+\sqrt\pi/128`). Ver Teorema 4 corrigido, abaixo.
> 3. **The proved bound `D_r(b)`, by contrast, is FACTORIAL** — `D_r/D_{r-1}\approx
>    r` (measured `28.32` at `r=30`; `C_r/C_{r-1}=29.28` there). The referee's
>    "`174` vs `0.78` at `r=6`" is not
>    a constant-factor looseness: at `r=30` the bound is `7.1\times10^{30}` against a
>    true value of `11.13`.
> 4. **The looseness decomposes into exactly two independent, separately-fixable
>    mechanisms**, both located precisely. **(G1)** §6 of the target document bounds
>    `\frac rn\varepsilon^h_{r-1}` by `rC_{r-1}(b{+}1)/n^2`, *discarding the explicit
>    `1/n`*; since the theorem's own standing hypothesis is `n\ge b{+}r{+}1`, that
>    factor is worth `r/n\le r/(b{+}r{+}1)<1`. Keeping it is a **one-line, fully
>    rigorous change** that turns the factorial recursion into a geometric one
>    (`D'_{30}(0)=9.9\times10^3` instead of `7.1\times10^{30}`). **(G2)** §4's
>    coefficient-sum norm costs a factor `(9/8)^r`: it is proved here that
>    `\|F_r(1-\cdot,b)\| = F_r(2,b)` **exactly** (the reflection `s\mapsto1{-}s`
>    aligns all signs within each coefficient), and `F_r(2,b)/F_r(1,b)=Θ((9/8)^r)`.
> 5. **What is not closed:** a bound that is *polynomial* in `r`. Even after the
>    (G1) fix the proved bound stays geometric, because (G2) is not removable by a
>    one-liner. The gap between a rigorous `O(1.24^r)` and the true `Θ(r^{3/2})`
>    remains open, now with both obstructions named and measured rather than merely
>    noticed.
>
> **This is a positive result and therefore requires the archive's mandatory
> adversarial reproduction before being catalogued.** I do not claim victory: §9's
> scorecard states exactly what rests on what, and §8.4 names the one derivation
> (the `ε^2` matching of §3.1) that a hostile referee should re-derive from scratch
> first, since everything else follows from it mechanically.

---

## 0. Disciplina

**Sources read, in the order the task mandated, before any code was written:**

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entry `DISC-DEC-045`
   (mandate and scope for wave 10 front (b)).
2. `.../u12_universality/theorem/THEOREM.md` — the complete
   `[Extensão, Estágio 6 — 2026-08-22]` and `[Extensão, Estágio 7 — 2026-08-22]`
   sections. Item (ii) of both open lists is the target of this document.
3. `.../k_general_existence_attempt/ATTEMPT.md` — in full, with particular care on
   §3 (the exact residual recursion), §4 (`A_r(b)`, including the post-adversarial
   `h^{j-1}\to h^k` correction), §5 (`D_r(b):=E_r(b)/(r{+}b{+}1)`,
   `E_r(b):=rC_{r-1}(b)+A_r(b)`), §6 (`C_r(b):=B_r(b)+rC_{r-1}(b{+}1)+2D_r(b{+}1)`,
   including the I-2 addendum), §7 (numerics), §8 item 1 ("no growth rate
   established"), §9 (scorecard).
4. `.../k_general_existence_attempt/adversarial/REFEREE_REPORT.md` — §A.5, the
   referee's independently-computed `A_r(b)/D_r(b)/C_r(b)` table and the explicit
   remark *"`D_r(b)` is very loose at larger `r` (`174` vs an observed `0.78` at
   `r=6`); the document is honest that it makes no claim about the growth rate of
   the constants (§8 item 1), and I confirm none is established."*
5. `.../k6_attempt/ATTEMPT.md` — §2.2/§2.3 (leading ODE, `F_r(t,b)` closed form,
   PROVED), §3.1 (the `G_r` ODE and the `K_r` relation), §3.3 (the `d_k^{(r)}(b)`
   closed form, conjectured-then-PROVED by symbolic substitution — the
   methodological template this document follows at the next order), §3.4.
6. `.../k3_attempt_2/ATTEMPT.md` — §2 (the exact `(a,b,r)` transition rules,
   PROVED), §3 (the telescoping ladder), §5 and §7.1 (the exact `ψ_n^{(3)}`,
   `ψ_n^{(3),R}`, `ψ_n^{(4)}`, `ψ_n^{(5)}` closed forms used here as independent
   cross-checks).

**Reuse policy (same convention as every predecessor in this lineage).** Every
script in this directory was written **from scratch**; nothing was imported or
copied from any sibling or predecessor directory. Four already-proved objects were
**re-transcribed from their stated formulas** and are labeled as reuse in
`core.py`'s header: the exact `(a,b,r)` transition rules; the `F_r(t,b)` closed
form; the `G_r(t,b)` closed form; and the *definitions* of `\hat H_r(s,b)` and
`K_r(s,b)`. The wave-8 referee's `A/D/C` table (§A.5) was transcribed only as a
**target to reproduce**, and `loose_bound.py` reproduces all ten of its entries
exactly from an independent implementation (§6.4). The five exact `ψ_n^{(K)}`
closed forms were transcribed only as **cross-check targets** (§7.1).

**Exactness policy.** `fractions.Fraction` / `sympy.Rational` / `sympy.Symbol`
throughout. Every claim labeled PROVED, "exact", or "identity" rests on exact
rational or symbolic arithmetic. Floating point appears in exactly two places,
both flagged in situ: (a) human-readable display columns; (b) `asymptotics.py`
PART 3, which uses `mpmath` at 60 decimal digits to evaluate `D^*_r(b)` for
`r` up to `10^5`, where exact rationals become prohibitive. (b) is safe because
**every term of the sum defining `H_r(1,b)` is strictly positive** (§3.3), so no
cancellation occurs; it is cross-checked against the exact rationals at 24 `(r,b)`
pairs, worst relative discrepancy `7.6\times10^{-61}`.

---

## 1. The target, restated precisely — three different constants

The open item says "the growth rate in `r` of the error constants `D_r(b),C_r(b)`".
Three distinct quantities hide behind that phrase and this document separates them,
because they behave completely differently:

| symbol | definition | what it is |
|---|---|---|
| `D_r(b)`, `C_r(b)` | the explicit recursion of `../ATTEMPT.md` §5/§6 | the constants the **existing proof actually produces** |
| `S_r(b)` | `\sup_{m,n} n^2|R_r(m,b,n)|`, sup over **all** valid `m` and all `n\ge b{+}r{+}1` | the **smallest constant the Target Theorem's statement admits** |
| `D^*_r(b)` | `\lim_{n\to\infty}\max_m n^2|R_r(m,b,n)|` | the **asymptotically sharp** constant |

Trivially `D^*_r(b)\le S_r(b)\le D_r(b)`. The referee's remark ("`174` versus an
observed `0.78`") compares `D_6(0)` with a finite-`n` sample of `S_6(0)`. This
document determines `D^*_r(b)` exactly, measures `S_r(b)` exhaustively, and
determines the growth of `D_r(b)`, `C_r(b)`.

Notation is that of the predecessors: `h:=1/n`, `t:=m/n`, `s:=a/n`;
`R_r(m,b,n):=g_r(m,b)-F_r(t,b)-\frac1nG_r(t,b)`;
`\varepsilon^h_r(a,b,n):=h_r(a,b)-\hat H_r(s,b)-\frac1nK_r(s,b)`; valid domains
`b{+}r{+}1\le m\le n` and `0\le a\le n{-}b{-}r{-}1`, i.e. `a{+}b{+}r<n` throughout.

---

## 2. The mechanism: reduce the constant to a *known-shape* object

The predecessor's own numerics, and the wave-8 referee's exhaustive re-run, both
report that the worst case of `n^2|R_r(m,b,n)|` sits at `t=m/n=1` ("nenhum pico
interior, o pior caso sempre em `t=1`"). At `t=1,b=0`, `g_r(n,0)=\psi_n^{(r)}`, and
the two exactly-known cases are decisive:

- `\psi_n^{(1)}=(4n{+}1)/(6n)` ⟹ `R_1\equiv0`, so the true constant is `0` at `r=1`;
- `\psi_n^{(2)}=(8n^2{+}4n{+}1)/(15n^2)` ⟹ `R_2=1/(15n^2)`, constant in `m`.

Both facts say the same thing: **`n^2R_r` is converging to the third term of the
asymptotic expansion of `g_r`.** So the tight constant is not an inaccessible
supremum — it is `\max_{t}|H_r(t,b)|` where `H_r` is the `1/n^2` coefficient
function, an object of exactly the same kind as `F_r` and `G_r`, obtainable by the
same machinery one order further. That reduction is the whole strategy of this
document, and it is what makes large `r` reachable at all: the `H_r` ladder is a
single chain `H_r(\cdot,b)\leftarrow H_{r-1}(\cdot,b{+}1)\leftarrow\cdots\leftarrow
H_0(\cdot,b{+}r)=0`, not a search over `m,n`.

---

## 3. The third-order pair `(H_r, L_r)`

### 3.1 The `ε^2` matching (NEW; the one place a referee should start)

Write, as an *ansatz to be validated* (its validity is established in §4, not
assumed here):

`g_r(m,b)=F_r(t,b)+\varepsilon G_r(t,b)+\varepsilon^2H_r(t,b)+O(\varepsilon^3)`,
`\quad h_r(a,b)=\hat H_r(s,b)+\varepsilon K_r(s,b)+\varepsilon^2L_r(s,b)+O(\varepsilon^3)`,
`\quad\varepsilon:=1/n`.

Substituting into the exact rearranged non-source recursion
`m[g_r(m,b)-g_r(m-1,b)]+(1{+}r{+}b)g_r(m{-}1,b)=1+r\,h_{r-1}(n{-}m{+}1,b)`
(`../../ATTEMPT.md` §2, PROVED, reused verbatim) with `m=t/\varepsilon` exactly:

`g_r(m{-}1,b)=F+\varepsilon(G-F')+\varepsilon^2(H-G'+\tfrac12F'')+O(\varepsilon^3)`,

`m[g_r(m)-g_r(m{-}1)] = tF' + \varepsilon\,t(G'-\tfrac12F'') + \varepsilon^2\,t(H'-\tfrac12G''+\tfrac16F''') + O(\varepsilon^3)`,

and, since `n{-}m{+}1=n(1{-}t)+1` gives `s=(1{-}t)+\varepsilon` **exactly**,

`h_{r-1}(n{-}m{+}1,b) = \hat H_{r-1} + \varepsilon[\hat H_{r-1}'+K_{r-1}] + \varepsilon^2[\tfrac12\hat H_{r-1}''+K_{r-1}'+L_{r-1}] + O(\varepsilon^3)`

(all evaluated at `s=1{-}t`, `'` denoting `d/ds`). Matching orders:

- `\varepsilon^0` reproduces **Fact 2** (the leading ODE, PROVED, `k6` §2.3);
- `\varepsilon^1` reproduces **Fact 3** (the `G_r` ODE, PROVED, `k6` §3.3) exactly
  after rearrangement — *a free validation of the scheme one order down*;
- `\varepsilon^2` gives the **new** ODE:

> **The `H_r` ODE.**
> `\;t\,H_r'(t,b)+(1{+}r{+}b)H_r(t,b) = r\big[\tfrac12\hat H_{r-1}''(1{-}t,b)+K_{r-1}'(1{-}t,b)+L_{r-1}(1{-}t,b)\big] + \tfrac t2G_r''(t,b)-\tfrac t6F_r'''(t,b)+(1{+}r{+}b)\big[G_r'(t,b)-\tfrac12F_r''(t,b)\big]`

The source step `h_r(a,b)=\frac1n+\frac rn h_{r-1}(a,b{+}1)+[(1{-}s)-\frac{1{+}b{+}r}n]g_r(n{-}a,b{+}1)`
is again purely algebraic (`a=ns` exactly, no shift, no Taylor expansion): its
`\varepsilon^0` and `\varepsilon^1` orders reproduce the *definitions* of `\hat H_r`
and `K_r`, and its `\varepsilon^2` order gives the **new** relation:

> **The `L_r` relation.**
> `\;L_r(s,b) = r\,K_{r-1}(s,b{+}1) + (1{-}s)H_r(1{-}s,b{+}1) - (1{+}b{+}r)G_r(1{-}s,b{+}1)`

**Base cases (exact, not asymptotic).** `g_0(m,b)=1/(b{+}1)` exactly, so
`H_0\equiv0`; `h_0(a,b)=(n{-}a{+}1)/(n(b{+}2))` has **no** `1/n^2` term at all, so
`L_0\equiv0` (and the `L_r` relation reproduces this: at `r=0` it reads
`0\cdot K_{-1}+(1{-}s)H_0-(1{+}b)G_0=0`).

Since the RHS of the `H_r` ODE is a polynomial in `t`, matching the coefficient of
`t^k` (the LHS contributes `(k{+}1{+}r{+}b)e_k^{(r)}(b)`, never zero for
`r,b\ge0,k\ge0`) determines `H_r(t,b)=\sum_ke_k^{(r)}(b)t^k` uniquely as a
polynomial, with `\deg H_r=r{-}2`.

> **No circularity — the same non-circular structure the predecessor uses.** The
> ansatz above is a *device for finding candidates*, not a premise. What is
> actually used downstream is only this: `H_r` and `L_r` are **defined** to be the
> unique polynomial solutions of the two displayed relations (with `H_0=L_0=0`) —
> explicit, finite, already-computable objects, defined without reference to any
> limit. Nothing about `g_r,h_r` is assumed in defining them. §4 then *derives*,
> from the exact discrete recursion alone, that the difference between `g_r` and
> `F_r+\frac1nG_r+\frac1{n^2}H_r` is `O(1/n^3)`. This is exactly the
> assumption-free structure `../ATTEMPT.md` §1 insists on for `R_r`, one order up:
> the residual is a *defined* difference of two already-well-defined quantities,
> and its smallness is derived, not posited.

### 3.2 The defining coefficient recursion, written out

Expanding every piece of the ODE in coefficients (`\hat H_{r-1}(1{-}t,b)=t
F_{r-1}(t,b{+}1)` and the analogous reflections; full derivation in
`verify_ek_recursion.py`'s header):

`\;(k{+}1{+}r{+}b)\,e_k^{(r)}(b) = r\,T + U`, where

```
T =  (1/2)(k+1)(k+2) c_{k+1}^{(r-1)}(b+1)                    [ (1/2) Hhat''_{r-1} ]
   - (k+1)(r-1)      c_k^{(r-2)}(b+2)   ]
   - (k+1)           d_k^{(r-1)}(b+1)   ]  -K'_{r-1}
   + (k+1)(b+r)      c_{k+1}^{(r-1)}(b+1) ]
   + (r-1)·[k==0]        ]
   + (r-1)(r-2)      c_{k-1}^{(r-3)}(b+3) ]
   + (r-1)           d_{k-1}^{(r-2)}(b+2) ]  L_{r-1}
   - (r-1)(b+r)      c_k^{(r-2)}(b+2)     ]
   + e_{k-1}^{(r-1)}(b+1)                 ]
   - (b+r)           d_k^{(r-1)}(b+1)     ]
U =  (1/2)k(k+1)            d_{k+1}^{(r)}(b)      [ (t/2)G_r''       ]
   - (1/6)k(k+1)(k+2)       c_{k+2}^{(r)}(b)      [ -(t/6)F_r'''     ]
   + (1+r+b)(k+1)           d_{k+1}^{(r)}(b)      [ (1+r+b)G_r'      ]
   - (1/2)(1+r+b)(k+1)(k+2) c_{k+2}^{(r)}(b)      [ -(1+r+b)F_r''/2  ]
```

**This hand-derived recursion is itself verified, not assumed**: fed the
ODE-solved coefficients on both sides it reproduces them exactly at **6601**
index triples (`r=0..40`, `b=0..6`, every `k` including all out-of-range ones),
`0` mismatches (`verify_ek_recursion.log` STAGE A).

### 3.3 The closed form: conjectured from the data, then verified symbolically

Reading the exact `e_k^{(r)}(b)` off the ODE solution for `r=2,\dots,6`,
`b=0,\dots,4` gives `e_k^{(r)}(b) = P(k)\cdot\frac{r!}{(r-k-2)!}\cdot
\frac1{\prod_{i=1}^{k+3}(r+b+i)}` with `P(k)=2,11,35,85,175` at `k=0,\dots,4`.
Dividing by `\binom{k+4}4` gives `2,\ \tfrac{11}5,\ \tfrac73,\ \tfrac{17}7,\
\tfrac52`, i.e. exactly `3-\frac4{k+4}`. Hence:

> **Theorem 1 (third-order closed form).**
> `\displaystyle H_r(t,b) = \sum_{k=0}^{r-2}\frac{(3k{+}8)(k{+}1)(k{+}2)(k{+}3)}{24}\cdot\frac{r!}{(r{-}k{-}2)!}\cdot\frac{t^k}{\prod_{i=1}^{k+3}(r{+}b{+}i)}`.

It slots exactly into the already-proved family, one rung further:

| order | coefficient | multiplier | falling factorial | denominator |
|---|---|---|---|---|
| `1` | `c_k^{(r)}(b)` | `1` | `r!/(r{-}k)!` | `\prod_{i=1}^{k+1}(r{+}b{+}i)` |
| `1/n` | `d_k^{(r)}(b)` | `\binom{k+2}2` | `r!/(r{-}k{-}1)!` | `\prod_{i=1}^{k+2}(r{+}b{+}i)` |
| `1/n^2` | `e_k^{(r)}(b)` | `\tfrac{3k+8}4\binom{k+3}3` | `r!/(r{-}k{-}2)!` | `\prod_{i=1}^{k+3}(r{+}b{+}i)` |

**This is not left as a fit** — the same three-layer standard `k6_attempt` used to
promote its own `d_k^{(r)}(b)` conjecture to a theorem is applied here:

- **exhaustive exact:** the closed form equals the ODE solution at **10143**
  `(r,k,b)` triples (`r=0..45`, `b=0..8`, every `k`, including `k=r{-}1,r` where
  both must vanish), `0` mismatches (`verify_closed_form.log` V1); degrees all
  `r{-}2` (V1b);
- **symbolic in `b`:** the entire `(F,G,\hat H,K,H,L)` ladder rerun in `sympy`
  with `b` a `Symbol`, and `\text{simplify}(H_r(t,b)-\text{closed form})=0` for
  `r=0,\dots,11` (V2);
- **symbolic in `r,k,b`:** the closed forms written with gamma functions and
  substituted into the §3.2 recursion, *without looping over values* — the general
  `k\ge1` case and the `k=0` boundary case (which draws its `K_{r-2}` piece from a
  constant-only branch, exactly as `k6` §3.3 had to split) **both simplify to
  `0`** (`verify_ek_recursion.log` STAGE B1); and the closed form satisfies the
  recursion at all **6601** integer index triples including every degenerate
  boundary (STAGE B2).

With the base case `H_0\equiv0` this is a complete induction on `r`, conditional
only on the `H_r` ODE of §3.1.

> **Corollary 1a (PROVED, immediate).** Every coefficient `e_k^{(r)}(b)>0` for
> `0\le k\le r{-}2`. Hence `H_r(\cdot,b)` is strictly increasing on `[0,1]` and
> `\max_{t\in[0,1]}|H_r(t,b)| = H_r(1,b)`. Moreover `t=1` (i.e. `m=n`) is in the
> grid for *every* `n`, so `\max_m|H_r(m/n,b)| = H_r(1,b)` exactly at every `n` —
> no density argument is needed.

---

## 4. The three-term expansion exists: the same discrete-Gronwall argument, one order up

Theorem 1 is a statement about a polynomial. To make `D^*_r(b)` *the* residual
constant, one needs `n^2R_r\to H_r` uniformly. The predecessor's argument
(`../ATTEMPT.md` §§3–6) applies **verbatim** one order up: its only inputs are

1. that the `h^0` and `h^1` brackets of the substitution vanish identically in `t`;
2. that `F_r,G_r,\hat H_r,K_r` are polynomials of bounded degree, so every Taylor
   expansion involved is an exact finite identity with zero remainder;
3. that the contraction coefficient `(m{-}1{-}r{-}b)/m` is exactly `0` at the base
   case `m=b{+}r{+}1`, which subsumes the boundary with no separate treatment;
4. the falling-factorial/hockey-stick telescoping `\prod_{i=k+1}^m\frac{i-j}i=
   \binom kj/\binom mj` and `\sum_{k=j}^m\frac1k\binom kj=\binom mj/j`, which is
   what removes the spurious `\log n`.

Items 2–4 are untouched by adding a term. Item 1 becomes "the `h^0`, `h^1` **and
`h^2`** brackets vanish" — and the `h^2` bracket vanishing *is* the `H_r` ODE of
§3.1. Writing `R^{(3)}_r := g_r-F_r-\frac1nG_r-\frac1{n^2}H_r` and
`\varepsilon^{(3)}_r := h_r-\hat H_r-\frac1nK_r-\frac1{n^2}L_r`, the identical
algebra gives the identical recursion with `\Delta^{(3)}_r=\sum_{k\ge3}h^kq^{(3)}_k(t,b)`,
hence:

> **Theorem 2 (three-term existence).** For every `r\ge0,b\ge0` there are finite
> constants `D^{(3)}_r(b), C^{(3)}_r(b)` — given by the same recursion,
> `D^{(3)}_r(b)=[rC^{(3)}_{r-1}(b)+A^{(3)}_r(b)]/(r{+}b{+}1)`,
> `C^{(3)}_r(b)=B^{(3)}_r(b)+rC^{(3)}_{r-1}(b{+}1)+D^{(3)}_r(b{+}1)`,
> `D^{(3)}_0=C^{(3)}_0=0` — such that `|R^{(3)}_r(m,b,n)|\le D^{(3)}_r(b)/n^3` for
> every valid `m` and `|\varepsilon^{(3)}_r(a,b,n)|\le C^{(3)}_r(b)/n^3` for every
> valid `a`, uniformly, `n\ge b{+}r{+}1`.

Computational corroboration, all exact (`third_order_existence.log`):

- the `h^0`, `h^1` **and `h^2`** coefficients of `\Delta^{(3)}_r(t,b,h)` all vanish
  identically in `t`, for `r=0..24`, `b=0..4` — so `\Delta^{(3)}_r=O(h^3)` and the
  §4 coefficient-sum lemma applies unchanged;
- the constants come out finite and are tabulated;
- both bounds hold with **zero violations** over every valid `m`, every valid `a`,
  and every `n\le90`, for `r=1,\dots,6`, `b=0,1`.

> **Corollary 2a.** `\big|n^2R_r(m,b,n)-H_r(t,b)\big|\le D^{(3)}_r(b)/n` uniformly in
> `m`. Combining with Corollary 1a:
> `\displaystyle D^*_r(b) \;=\; \lim_{n\to\infty}\max_m n^2|R_r(m,b,n)| \;=\; H_r(1,b)`.

Independent numerical confirmation *before* the closed form was found
(`validate_third_order.log`): `n^3\max_m|R^{(3)}_r|` **stabilises** rather than
growing (`r{=}5,b{=}0`: `0.40351,\,0.40106,\,0.39984,\,0.39924,\,0.39893` at
`n=40,80,160,320,640`), same for the `h`-side; and the exact identity
`R_2(m,b,n)=H_2(t,b)/n^2` holds at **966/966** checked points for `b=0,\dots,3`.

---

## 5. The tight constant, exactly, and its growth

### 5.1 An exact closed form at `b=0`

At `b=0`, `\prod_{i=1}^{k+3}(r{+}i)=(r{+}k{+}3)!/r!`, so writing `i:=r{-}k{-}2`
(so `(r{-}k{-}2)+(r{+}k{+}3)=2r{+}1`) turns Theorem 1 at `t=1` into a **binomial
half-sum**, exactly as `k6` §3.4 did one order down:

`\displaystyle H_r(1,0) = \frac{(r!)^2}{(2r{+}1)!}\sum_{i=0}^{r}w(i)\binom{2r{+}1}i`,
`\qquad w(i):=\frac{u(u{+}1)(u{-}1)(3u{+}2)}{24},\ u:=r{-}i`

(the sum may be extended from `i\le r{-}2` to `i\le r` free of charge: `w` vanishes
at `u=0` and `u=1`). With `N:=2r{+}1`, `v:=i{-}N/2`, an elementary rewrite gives

`24\,w(i) = \underbrace{3v^4-\tfrac32v^2+\tfrac3{16}}_{\text{even in }v} + \underbrace{4v^3-v}_{\text{odd in }v}`

— verified exactly for `r=2..39`, all `i`. Because `N` is **odd**, `i\le r` is
*exactly half* the range, so the even part contributes exactly half its full sum,
computable from the central moments of `\mathrm{Bin}(N,\tfrac12)`
(`\mu_2=N/4`, `\mu_4=N(3N{-}2)/16`):

`\displaystyle\sum_{i=0}^{N}\Big[3v^4-\tfrac32v^2+\tfrac3{16}\Big]\binom Ni = 2^N\frac{3(3N{-}1)(N{-}1)}{16}`,
so the half-sum is `4^r\cdot\frac{3r(3r{+}1)}4`

(verified exactly, `r=1..59`). The odd part needs two boundary identities, both
verified exactly for `r=1..119`:

`\displaystyle\sum_{i=0}^{r}(N{-}2i)\binom Ni=(2r{+}1)\binom{2r}r`, `\qquad
\sum_{i=0}^{r}(N{-}2i)^3\binom Ni=(2r{+}1)(4r{+}1)\binom{2r}r`

(the first is the classical `nC(n{-}1,m)` telescoping; the second was found from
exact data — `D_3/\binom{2r}r = 15,45,91,153,231,\ldots`, second differences
constant `16`, hence `8r^2{+}6r{+}1`). Combining, `4A_3-A_1=-2r(2r{+}1)\binom{2r}r`,
and using `\binom{2r}r/4^r = 1/[(2r{+}1)\varphi_r]` the whole odd contribution
collapses to exactly `-r/12`:

> **Theorem 3 (the tight residual constant at `b=0`, exact).**
> `\displaystyle D^*_r(0)\;=\;H_r(1,0)\;=\;\frac{r(3r{+}1)}{32}\,\varphi_r\;-\;\frac r{12}`,
> `\qquad\varphi_r=\frac{4^r(r!)^2}{(2r{+}1)!}`.

Verified exactly against the ODE-solved `H_r(1,0)` for `r=0,\dots,80`.

| `r` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| `D^*_r(0)` | `0` | `0` | `1/15` | `5/28` | `103/315` | `1405/2772` | `1431/2002` | `2219/2340` |
| decimal | `0` | `0` | `0.0667` | `0.1786` | `0.3270` | `0.5069` | `0.7148` | `0.9483` |

> **Corollary 3a (why `R_1\equiv0`).** `D^*_1(0)= \frac{1\cdot4}{32}\cdot\frac23-\frac1{12}
> = \frac1{12}-\frac1{12}=0` — an **exact cancellation**, not an approximation.
> `D^*_0(0)=0` likewise. This is the structural explanation of the fact the target
> document found empirically and the wave-8 referee independently re-predicted
> (`R_1\equiv0`, 485 evaluations). It is the same *flavour* of exact degeneracy at
> the bottom of the ladder that Estágio 7 found for `c_K` (`c_1=0` exactly, from
> `3\varphi_1=2`) — and it carries the same writing caution: **never write
> "`D^*_r(0)>0` for all `r\ge0`"; `r=0` and `r=1` are exact-zero cases.**

### 5.2 The growth rate

`\varphi_r=\tfrac12\sqrt{\pi/r}\,[1-\tfrac3{8r}+O(r^{-2})]`, so Theorem 3 gives
immediately:

> **Theorem 4 (growth rate, `b=0`).**
> `\displaystyle D^*_r(0) \;=\; \frac{3\sqrt\pi}{64}\,r^{3/2}\;-\;\frac r{12}\;+\;\frac{\sqrt\pi}{128}\,r^{1/2}\;+\;O(1)`,
> in particular `D^*_r(0)=\Theta(r^{3/2})` with leading constant
> `\tfrac{3\sqrt\pi}{64}=0.0830837742611961\ldots`

> **[Correção pós-adversarial, 2026-08-23, F-1 de `adversarial/REFEREE_REPORT.md`
> Parte 4.2.]** O terceiro termo acima, `+\frac{\sqrt\pi}{128}r^{1/2}`, está
> **errado em sinal e em magnitude** (fator `4`). O valor correto, re-derivado
> pelo referee a partir da mesma expansão de Wallis–Stirling deste documento
> (`\varphi_r=\tfrac12\sqrt{\pi/r}[1-\tfrac3{8r}+O(r^{-2})]`, já confirmada
> acima) é:
> `\displaystyle D^*_r(0) \;=\; \frac{3\sqrt\pi}{64}\,r^{3/2}\;-\;\frac r{12}\;-\;\frac{\sqrt\pi}{512}\,r^{1/2}\;+\;O(1)`.
> Os próprios números deste documento em §5.2 (a razão `D^*_r(0)/[\frac{3\sqrt\pi}{64}r^{3/2}-\frac r{12}]` aproximando `1` **por baixo** —
> `0.99954,\,0.999957,\,0.9999958,\,0.99999958`) já refutavam o termo positivo
> publicado, que exigiria aproximação por cima; a string do termo estava
> codificada diretamente em `asymptotics.py:173`, nunca computada. A sessão
> orquestradora confirmou independentemente `-\sqrt\pi/512=-0.0034618239\ldots`
> via `mpmath` a `r=10^3,10^5,10^7,10^9` (convergência a `10` algarismos
> significativos), usando apenas a fórmula fechada do Teorema 3 acima (sem
> reusar nenhum script do referee). `\Theta(r^{3/2})` e a constante líder
> `3\sqrt\pi/64` são intocados por esta correção.

For general fixed `b`, the same computation with `N=2r{+}b{+}1` no longer has
`i\le r` as an exact half-range (which is why no equally clean closed form exists
at `b\ge1` — the residual `\frac{r(3r+1)}{32}F_r(1,b)-H_r(1,b)` is `r/12` at `b=0`
but not a clean rational at `b=1`: `5/96,\,61/480,\,963/4480,\dots`). The Stirling
estimate, however, is `b`-**independent**: the factor `2^{b+1}` in `2^N` exactly
cancels the `2^{-(b+1)}` in the prefactor `r!(r{+}b)!/(2r{+}b{+}1)!`, giving
`D^*_r(b)\sim\frac{3\sqrt\pi}{64}r^{3/2}` for every fixed `b`.

> **[Correção pós-adversarial, 2026-08-23, F-2/F-3 de
> `adversarial/REFEREE_REPORT.md` Partes 3.3/4.3/4.4.]** Dois erros neste
> parágrafo. **(F-3)** O mecanismo declarado de cancelamento — "o fator
> `2^{b+1}` em `2^N` cancela exatamente o `2^{-(b+1)}` no prefator
> `r!(r{+}b)!/(2r{+}b{+}1)!`" — está **errado como escrito**: esse prefator não
> contém potência de `2` alguma. O cancelamento real e exato é
> `\displaystyle\rho_b(r):=2^b\frac{(r{+}b)!}{r!}\cdot\frac{(2r{+}1)!}{(2r{+}b{+}1)!}=\prod_{j=1}^b\frac{2r+2j}{2r+j+1}\;\longrightarrow\;1`.
> **(F-2)** A frase "no clean closed form exists at `b\ge1`" acima estava
> correta apenas para o *valor exato* de `D^*_r(b)`, não para sua expansão
> assintótica: o referee derivou uma forma fechada exata **para todo `b`**
> (Teorema 3′, ver `adversarial/REFEREE_REPORT.md` Parte 3.3, verificada em
> `287+217` pontos exatos), que fecha o item aberto §8.3(2) abaixo na
> afirmativa e da qual segue, sem qualquer estimativa assintótica, que o
> coeficiente do termo linear em `D^*_r(b)` é **exatamente `-(3b{+}2)/24`**
> (não `-1/12`, válido só em `b=0`). O termo constante do próprio Teorema 4
> (abaixo) já assumia implicitamente `-r/12` como válido para todo `b`; ver
> correção lá. A sessão orquestradora confirmou independentemente, por soma
> direta e vetorizada em ponto flutuante da fórmula fechada do Teorema 1 (não
> reusando nenhum script do referee), que `[D^*_r(b)-\text{termo
> líder}]/r\to-(3b{+}2)/24` em `b=0,1,2,3`, com convergência limpa até
> `r=2\times10^7`.

**Numerical corroboration** (`asymptotics.log` PART 3; `mpmath` dps 60,
cross-checked against exact rationals to `7.6\times10^{-61}`):

| `r` | `D^*_r(0)` | `D^*_r(1)` | `D^*_r(2)` | `D^*_r(3)` |
|---|---|---|---|---|
| `10` | `1.78481` | `1.19694` | `0.83037` | `0.59313` |
| `10^2` | `74.7164` | `64.7476` | `56.2739` | `49.0490` |
| `10^3` | `2543.90` | `2427.41` | `2316.85` | `2211.89` |
| `10^4` | `82250.1` | `81027.5` | `79825.1` | `78642.4` |
| `10^5` | `2619005` | `2606593` | `2594245` | `2581962` |

local log-log slope `d\log D^*_r/d\log r` on `r=3\times10^4..10^5`:
`1.5022` (`b{=}0`), `1.5054` (`b{=}1`), `1.5087` (`b{=}2`), `1.5119` (`b{=}3`) — all
converging to `3/2`;
`D^*_r(b)/D^*_r(0)` at `r=10^5`: `0.99526,\,0.99055,\,0.98586` — converging to `1`;
`D^*_r(0)\big/\big[\tfrac{3\sqrt\pi}{64}r^{3/2}-\tfrac r{12}\big]`:
`0.99954` (`r{=}10^2`), `0.999957` (`10^3`), `0.9999958` (`10^4`), `0.99999958` (`10^5`).

### 5.3 The finite-`n` supremum `S_r(b)`

`S_r(b)` is attained at the **minimal state** `n=m=b{+}r{+}1` — verified by
exhaustive scan over every valid `m` and every `n\le70` for `r=2,\dots,22`,
`b=0,1` (`finite_n_sup.log`, `cross_checks.log` X2), with no exception. Being one
exact number per `r`, it can be pushed far:

| `r` | 4 | 20 | 60 | 100 | 130 | 150 |
|---|---|---|---|---|---|---|
| `S_r(0)/D^*_r(0)` | `1.1056` | `1.3634` | `1.5017` | `1.5513` | `1.5734` | `1.5845` |
| `S_r(0)/r^{3/2}` | `0.0452` | `0.0877` | `0.1085` | `0.1159` | `0.1192` | `0.1208` |

`S_r(0)/D^*_r(0)` increases but with increments decaying like `r^{-1/2}`; the fit
`S/D^*=a-c/\sqrt r` on the `r=60,130` pair gives `a\approx1.725` and then *predicts*
`1.5521` at `r=100` against the actual `1.55133`. Its log-log slope is `1.594` at
`r=150` and still falling (`D^*`'s own slope is `1.58` at comparable `r`).

> **Claim 5 (NUMERICALLY CHARACTERIZED, not proved).** `S_r(b)=\Theta(r^{3/2})`
> too, with a leading constant roughly `1.7\times` that of `D^*_r(b)`
> (`\approx0.142` at `b=0`). What is **not** proved is that `S_r/D^*_r` stays
> bounded: it is measured increasing throughout `r\le150`, and no argument here
> forbids an unbounded but very slowly growing factor.

---

## 6. Why the proved bound is so much bigger — two mechanisms, both located

### 6.1 (G1) The discarded `1/n` in the `h`-step: the factorial amplifier

`../ATTEMPT.md` §6's exact identity contains the term `\frac rn\varepsilon^h_{r-1}(a,b{+}1,n)`.
The document bounds it by `r\,C_{r-1}(b{+}1)/n^2`, i.e. it uses
`|\varepsilon^h_{r-1}|\le C_{r-1}(b{+}1)/n^2` and then **discards the explicit
factor `1/n`**. That is where the factorial comes from: with no compensating
division, `C_r\gtrsim rC_{r-1}`, hence `C_r,D_r=\tilde\Theta(r!)`.

But the Target Theorem's own standing hypothesis is `n\ge b{+}r{+}1` (it must be,
for `m=b{+}r{+}1` to be a valid state — and the level-`(r{-}1)`, `b{+}1` inductive
hypothesis is valid on exactly the same range, `n\ge(b{+}1)+(r{-}1)+1=b{+}r{+}1`).
So `\frac rn\le\frac r{b+r+1}<1` on the whole range where the theorem is asserted.
A second, smaller free gain: `(1{-}s)-\frac{1{+}b{+}r}n = \frac{n-a-1-b-r}n\in[0,1]`
on the valid domain (`a\le n{-}b{-}r{-}1` and `a\ge0`), so §6's `\le2` can be `\le1`.

> **Proposition 6 (a strictly tighter, still rigorous, bound).** Replacing §6's
> recursion by
> `\;C'_r(b) := B_r(b) + \frac r{b{+}r{+}1}C'_{r-1}(b{+}1) + D'_r(b{+}1)`,
> `\;D'_r(b) := \frac{rC'_{r-1}(b)+A_r(b)}{r{+}b{+}1}`, `\;C'_0=D'_0=0`,
> yields constants that still satisfy the Target Theorem's conclusions, and that
> are **geometric rather than factorial** in `r`.

| `r` | `D^*_r(0)` true | `D'_r(0)` improved | `D_r(0)` original | improved/true | original/improved |
|---|---|---|---|---|---|
| `6` | `0.715` | `8.98` | `174.1` | `12.6` | `19.4` |
| `10` | `1.785` | `47.5` | `5.05\times10^5` | `26.6` | `1.06\times10^4` |
| `16` | `3.972` | `306` | `1.53\times10^{12}` | `77.0` | `5.00\times10^9` |
| `20` | `5.750` | `889` | `1.26\times10^{17}` | `155` | `1.42\times10^{14}` |
| `30` | `11.13` | `9.90\times10^3` | `7.09\times10^{30}` | `889` | `7.16\times10^{26}` |

The original bound's ratio `D_r/D_{r-1}` grows linearly (`4.74,4.15,4.51,5.20,
6.04,\dots,14.55` at `r{=}16`, `18.46` at `r{=}20`, `28.32` at `r{=}30`; the
`C_r/C_{r-1}` ratios run one higher, `15.47`/`19.40`/`29.28`) — factorial. The improved
bound's ratio is `1.240` at `r=45` and slowly decreasing.

### 6.2 (G2) The coefficient-sum norm: a factor `(9/8)^r`

§4's Lemma bounds `|p(x)|` on `[0,1]` by `\|p\|:=\sum_k|a_k|`. For the polynomials
that actually occur this is not a mild overestimate:

> **Lemma 7 (PROVED, exact).** For any polynomial `p` with **non-negative**
> coefficients, `\|p(1-\cdot)\| = p(2)`, and `\|(1{-}s)q(s)\|=2\|q\|` for any `q`
> whose `j`-th coefficient has sign `(-1)^j`. Hence
> `\|F_r(1{-}\cdot,b)\|=F_r(2,b)`, `\|G_r(1{-}\cdot,b)\|=G_r(2,b)` and
> `\|\hat H_r(\cdot,b)\| = 2F_r(2,b{+}1)`.

*Proof.* The coefficient of `s^j` in `p(1{-}s)=\sum_kc_k(1{-}s)^k` is
`(-1)^j\sum_{k\ge j}c_k\binom kj`, so all contributions to a given coefficient
share the sign `(-1)^j` and `\sum_j|\cdot|=\sum_kc_k\sum_j\binom kj=\sum_kc_k2^k=p(2)`.
For the second, the product's `s^j` coefficient is `q_j-q_{j-1}`, whose two terms
again share a sign. `\square` (Verified exactly, `r=0..24`, `b=0..3`.)

And `F_r(2,b)` is exponentially larger than `\sup_{[0,1]}|F_r|=F_r(1,b)`:

`\displaystyle F_r(2,0)=\frac{\varphi_r}{4^r}\sum_{i=0}^r2^{r-i}\binom{2r{+}1}i`,

whose summand `2^{-i}\binom{2r+1}i` peaks at `i=(2r{-}1)/3`, **inside** the
summation range, so the restricted sum is already of the order of the full one,
`(3/2)^{2r+1}2^r=\tfrac32(9/2)^r`, giving `F_r(2,0)\sim\tfrac32\varphi_r(9/8)^r`.

| `r` | 10 | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|---|
| `F_r(2,0)/F_r(1,0)` | `4.600` | `15.60` | `51.18` | `166.6` | `541.5` | `1758.8` |
| ratio in `r` | `1.1359` | `1.12726` | `1.125564` | `1.125150` | `1.125041` | `1.125012` |
| `\big/(9/8)^r` | `1.4164` | `1.4797` | `1.4947` | `1.4985` | `1.4996` | `1.4999` |

— converging to `9/8` and `3/2` exactly as the mechanism predicts. Both `A_r(0)`
and `B_r(0)` inherit this: their ratios in `r` are `1.1945` and `1.1594` at
`r=40`, still decreasing.

### 6.3 The resulting picture

| object | growth in `r` | status |
|---|---|---|
| `D^*_r(b)` — asymptotically sharp constant | `\Theta(r^{3/2})`, constant `3\sqrt\pi/64`, `b`-independent | PROVED (mod. §8.4) — **[Correção pós-adversarial, 2026-08-23]: PROVADA sem "mod.", ver Teorema 3′ do referee, §5.2 e Scorecard item 9 acima; §8.4 referia-se apenas à re-derivação do `ε²`-matching, que também foi confirmada, mas o "mod." aqui era o item separado da Parte 4/row 9 (o passo de Stirling em `b\ge1`), agora fechado.** |
| `S_r(b)` — sup over all `m,n` | `\Theta(r^{3/2})` with a `\approx1.7\times` larger constant | NUMERICALLY CHARACTERIZED |
| `D'_r(b)`, `C'_r(b)` — improved rigorous bound | geometric, measured ratio `1.240` at `r=45`, slowly decreasing | PROVED bound; rate NUMERICALLY CHARACTERIZED |
| `D_r(b)`, `C_r(b)` — the bound as published | factorial, `D_r/D_{r-1}\approx r` | NUMERICALLY CHARACTERIZED |
| `A_r(b)`, `B_r(b)` — the tail/substitution constants | geometric, ratio `\to9/8` | NUMERICALLY CHARACTERIZED, mechanism proved (Lemma 7) |

**None of this weakens the Target Theorem.** `D_r(b)` and `C_r(b)` are, and remain,
finite for every `r,b`; the existence proof of `DISC-DEC-040` is untouched. What
changes is only the *quality* of the constants it produces, and that the open item
(ii) now has an answer.

### 6.4 Independent reproduction of the referee's constants

`loose_bound.py` rebuilds `\Delta_r(t,b,h)`, `A_r(b)`, `B_r(b)`, `D_r(b)`, `C_r(b)`
from scratch (own bivariate-polynomial arithmetic over `Fraction`), asserting along
the way that the `h^0` and `h^1` coefficients of `\Delta_r` vanish identically. It
**reproduces every entry of `REFEREE_REPORT.md` §A.5 exactly** — all six rows of
`A_r(0)/D_r(0)/C_r(0)`, plus the four `b>0` spot checks
`D_2(2)=0.140952`, `D_3(1)=1.087000`, `D_3(5)=0.303012`, `D_4(3)=2.376231`.

---

## 7. Numerical corroboration, consolidated

### 7.1 Six independent exact confirmations of Theorem 3 (`cross_checks.log`)

Each `ψ_n^{(K)}` below was derived elsewhere in this lineage by a **completely
different method** (wave 5/6's exact telescoping-sum ladder), and each was itself
brute-force verified there. Their `1/n^2` coefficients are `H_K(1,0)`:

| `K` | `ψ_n^{(K)}` (source) | `1/n^2` coefficient | `H_K(1,0)` | `\frac{K(3K+1)}{32}\varphi_K-\frac K{12}` |
|---|---|---|---|---|
| 1 | `(4n{+}1)/(6n)` (wave 5) | `0` | `0` | `0` |
| 2 | `(8n^2{+}4n{+}1)/(15n^2)` (wave 5) | `1/15` | `1/15` | `1/15` |
| 3 | `(64n^3{+}48n^2{+}25n{+}6)/(140n^3)` (`k3_attempt_2` §5) | `5/28` | `5/28` | `5/28` |
| 4 | `(128n^4{+}128n^3{+}103n^2{+}52n{+}12)/(315n^4)` (§7.1) | `103/315` | `103/315` | `103/315` |
| 5 | `(\ldots{+}1405n^3{+}\ldots)/(2772n^5)` (§7.1) | `1405/2772` | `1405/2772` | `1405/2772` |

**Sixth, on the `h`-side** (`cross_checks_h_side.log`): `ψ_n^{(3),R}=h_2(0,0)=
\frac{11}{30}+\frac{13}{20n}+\frac{23}{60n^2}+\frac1{10n^3}` (`k3_attempt_2` §5,
PROVED). My reflections give `\hat H_2(0,0)=11/30`, `K_2(0,0)=13/20`, and — from the
**new** `L_r` relation — `L_2(0,0)=23/60`. All three exact.

**Seventh, self-contained:** the same `1/n^2` coefficients re-extracted from my own
exact chain by exact rational interpolation in `1/n`, out-of-sample validated on
five fresh `n` each, `r=1,\dots,7` — all matching `H_r(1,0)`, including
`1431/2002` (`r{=}6`) and `2219/2340` (`r{=}7`), which are *not* in any prior
document.

### 7.2 Validation of my own simulator against facts proved elsewhere

`validate_third_order.log` STEP 0: my from-scratch `(a,b,r)` chain reproduces
`ψ_n^{(1)}=(4n{+}1)/(6n)` (`n=2..8`), `ψ_n^{(2)}=(8n^2{+}4n{+}1)/(15n^2)`
(`n=3..8`), and `g_6(7,0)=355081/823543` — the value the wave-7 referee confirmed
by exhaustive brute force over `592{,}950{,}960` combinations. All exact.
`core.py` additionally reproduces `F_r(1,0)=\varphi_r` and `G_r(1,0)=r\varphi_r/4`
for `r=0,\dots,12`, exactly.

### 7.3 Everything else, at a glance

| check | scope | result |
|---|---|---|
| closed form vs ODE solution | `r=0..45`, `b=0..8`, all `k` | **10143** checks, 0 mismatches |
| coefficient recursion **is** the ODE | `r=0..40`, `b=0..6`, all `k` | **6601** checks, 0 mismatches |
| closed form satisfies the recursion (integers) | idem | **6601** checks, 0 mismatches |
| closed form satisfies it, **symbolic `r,k,b`** | `k\ge1` case + `k=0` case | both simplify to `0` |
| symbolic-`b` ladder vs closed form | `r=0..11` | all `0` |
| `\Delta^{(3)}_r` has `h^0=h^1=h^2=0` | `r=0..24`, `b=0..4` | all vanish |
| `|R^{(3)}_r|\le D^{(3)}_r(b)/n^3` | all `m`, all `n\le90`, `r=1..6`, `b=0,1` | 0 violations |
| `|\varepsilon^{(3)}_r|\le C^{(3)}_r(b)/n^3` | all `a`, all `n\le90`, `r=1..6`, `b=0,1` | 0 violations |
| `R_1\equiv0`; `R_2=1/(15n^2)`; `R_2=H_2/n^2` | 1134 / 377 / 966 points | 0 failures each |
| Theorem 3 vs ODE solution | `r=0..80` | all exact |
| the three binomial identities of §5.1 | `r=1..119` / `1..59` / `2..39` | all exact |
| referee's §A.5 table reproduced | 6 rows + 4 spot checks | all exact |
| Lemma 7's three norm identities | `r=0..24`, `b=0..3` | all exact |

---

## 8. What this resolves, precisely, and what it does not

### 8.1 Relative to open item (ii)

The item asked for "a taxa de crescimento em `r` das constantes de erro
`D_r(b),C_r(b)`", noting the observed/bound discrepancy at `r=6` and that "nenhuma
forma fechada para o crescimento foi buscada". Answered on all three readings:

- **the true constant:** exact closed form (Theorem 3) and exact growth rate
  `\Theta(r^{3/2})` with explicit constant `3\sqrt\pi/64` (Theorem 4), plus
  `b`-independence of the leading constant;
- **the published bound:** factorial, `\tilde\Theta(r!)` — so the `r=6` observation
  understates the problem by many orders of magnitude at larger `r`;
- **the mechanism:** both sources of looseness located exactly (§6.1, §6.2), one of
  them removable by a one-line rigorous change (Proposition 6).

### 8.2 A by-product for open item (i)

Open item (i) is the *all-orders* exact closed form for `ψ_n^{(K)}` at general `K`.
This document does **not** close it, and does not claim to. What it does supply is
**the third rung of that ladder in closed form**: `H_r(t,b)`, general `r`, general
`b`, in the same shape as `F_r` and `G_r`, together with a mechanically-continuable
scheme (the `\varepsilon^j` matching of §3.1) that visibly generalises. Whether
that scheme has a *uniform-in-`j`* closed form — which is what item (i) would need —
is not addressed here. The multiplier sequence `1,\ \binom{k+2}2,\
\tfrac{3k+8}4\binom{k+3}3` is suggestive but three terms is not a pattern.

### 8.3 What remains open

1. **A polynomial-in-`r` rigorous bound.** Proposition 6 gets from factorial to
   geometric. Getting to polynomial requires replacing §4's coefficient-sum norm by
   an actual `\sup_{[0,1]}` bound — Lemma 7 shows precisely what that would buy
   (`(9/8)^r` per use), but no closed-form `\sup_{[0,1]}|q_k(\cdot,b)|` is derived
   here, and the improved recursion's own per-level factor (two contributions of
   `C'_{r-1}(b{+}1)`, coefficient `\to2`) is a separate obstruction that a
   triangle-inequality argument cannot beat.
2. **A closed form for `D^*_r(b)` at `b\ge1`.** Theorem 3 is specific to `b=0`,
   where `i\le r` is exactly half the range of `\binom{2r+1}\cdot`. The asymptotic
   (Theorem 4) is `b`-independent; the exact value is not, and no clean closed form
   was found at `b\ge1`.
3. **Whether `S_r/D^*_r` is bounded** (§5.3, Claim 5).
4. **The exact rate of the improved bound `D'_r(b)`** — measured `1.240` at
   `r=45`, plausibly heading to `9/8` but not established.

### 8.4 The one thing a hostile referee should attack first

Everything in §§3–5 follows mechanically from the `\varepsilon^2` matching of
**§3.1**. That derivation is by hand. Three things make it hard to be wrong and
easy to check, and a referee should verify all three independently:

- its `\varepsilon^0` and `\varepsilon^1` orders **reproduce Facts 2 and 3 exactly**
  — the already-proved `F_r` and `G_r` ODEs — so the scheme is validated one order
  down before it is used;
- the resulting `H_1\equiv0` and `H_2(t,0)\equiv1/15` are exactly the two facts the
  target document found empirically and the wave-8 referee independently
  re-predicted;
- the resulting `H_K(1,0)` reproduces the `1/n^2` coefficient of five
  independently-derived exact `ψ_n^{(K)}` formulas, plus `L_2(0,0)` for
  `ψ_n^{(3),R}` (§7.1).

Nonetheless, **no independent adversarial re-verification of this document has been
performed.** Per the archive's standing discipline, a positive result of this size
requires a dedicated hostile referee who re-derives §3.1 from scratch — own
`\varepsilon`-expansion, own simulator, own closed forms — *before* reading how this
document derives it, and only then integration into `THEOREM.md` may be considered.
**I do not claim the item is catalogued or closed; I claim it is answered and ready
for review.**

### 8.5 Scope discipline

No file outside this directory was created, modified, or deleted. `THEOREM.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `README*.md`,
`PROOF_DEPENDENCY_MAP.md`, `tamesis-cycle-survival/`, and every predecessor
`ATTEMPT.md`/`REFEREE_REPORT.md` are untouched. No git commit was made.

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | The `\varepsilon^2` matching: the `H_r` ODE and the `L_r` relation (§3.1) | **PROVED** by hand, from the exact discrete recursion, by the same finite-and-exact Taylor mechanism as the two orders below it; its `\varepsilon^0`/`\varepsilon^1` orders reproduce the already-PROVED Facts 2/3 exactly. Not independently re-derived by a second party (§8.4) |
| 2 | The coefficient recursion of §3.2 **is** the `H_r` ODE | **PROVED**, exact — 6601 index triples (`r=0..40`, `b=0..6`, all `k`), 0 mismatches |
| 3 | Theorem 1: closed form `e_k^{(r)}(b)=\frac{(3k+8)(k+1)(k+2)(k+3)}{24}\frac{r!}{(r-k-2)!}\prod_{i=1}^{k+3}(r{+}b{+}i)^{-1}` | **PROVED given claim 1**, to `k6_attempt`'s own standard for `d_k^{(r)}(b)`: conjectured from exact data, then verified symbolically for `r,k,b` (general `k\ge1` **and** the `k=0` branch, both `=0`), plus 10143 exact + 6601 exact + 12 symbolic-`b` checks |
| 4 | Corollary 1a: `e_k^{(r)}(b)>0`, so `\max_{[0,1]}|H_r|=H_r(1,b)` at every `n` | **PROVED**, immediate from claim 3 |
| 5 | Theorem 2: the three-term expansion exists, `O(1/n^3)` uniformly | **PROVED given claim 1** — the predecessor's §§3–6 argument verbatim one order up; its one new input (the `h^2` bracket vanishes) is claim 1. Computationally corroborated: `h^0{=}h^1{=}h^2{=}0` for `r=0..24,b=0..4`; 0 violations of both bounds over all `m`, all `a`, all `n\le90` |
| 6 | Corollary 2a: `D^*_r(b)=\lim_n\max_m n^2|R_r|=H_r(1,b)` | **PROVED given claims 4 and 5** |
| 7 | Theorem 3: `D^*_r(0)=\frac{r(3r+1)}{32}\varphi_r-\frac r{12}` exactly | **PROVED given claim 3** — via the odd-`N` half-range split plus three binomial identities, each verified exactly (`r\le119`); the formula itself verified exactly `r=0..80`; **six independent** confirmations against already-PROVED facts derived by a different method (§7.1) |
| 8 | Corollary 3a: `D^*_0(0)=D^*_1(0)=0` exactly — the structural reason for `R_1\equiv0` | **PROVED** (exact cancellation `\frac1{12}-\frac1{12}`) |
| 9 | Theorem 4: `D^*_r(b)=\Theta(r^{3/2})`, leading constant `\frac{3\sqrt\pi}{64}`, `b`-independent | **PROVED at `b=0`** (Theorem 3 + Wallis–Stirling). **For `b\ge1`: PROVED-MODULO the Stirling step being written out in full** — the cancellation `2^{b+1}\cdot2^{-(b+1)}` is stated, not carried out term-by-term here; corroborated to `r=10^5` (slopes `1.502`–`1.512`, ratios `\to1`) — **[Correção pós-adversarial, 2026-08-23]: agora PROVADA incondicionalmente para todo `b`, sem "modulo".** O referee (`adversarial/REFEREE_REPORT.md` Parte 3.3/4.4) derivou a forma fechada exata `D^*_r(b)` para todo `b` (Teorema 3′), da qual a `b`-independência da constante líder segue algebricamente, sem nenhuma estimativa de Stirling para a parte ímpar. O mecanismo de cancelamento aqui declarado estava errado como escrito (F-3: o prefator não contém potência de `2`; o cancelamento real é `\prod_{j=1}^b\frac{2r+2j}{2r+j+1}\to1`) — corrigido em §5.2 acima. Além disso o termo `r^{1/2}` a `b=0` estava com sinal e magnitude errados (F-1: correto `-\sqrt\pi/512`, não `+\sqrt\pi/128`), e o termo linear a `b\ge1` não é `-r/12` mas `-(3b{+}2)r/24` (F-2) — ambos corrigidos em §5.2. Ambas as correções verificadas independentemente pela sessão orquestradora. |
| 10 | `S_r(b)` is attained at the minimal state `n=m=b{+}r{+}1` | **NUMERICALLY VERIFIED**, exhaustive over all `m` and all `n\le70`, `r=2..22`, `b=0,1` — not proved |
| 11 | Claim 5: `S_r(b)=\Theta(r^{3/2})` with a `\approx1.7\times` larger constant | **NUMERICALLY CHARACTERIZED** to `r=150`; `S_r/D^*_r` is increasing throughout and is **not proved bounded** |
| 12 | `D_r(b),C_r(b)` (the published bound) grow factorially, `D_r/D_{r-1}\approx r` | **NUMERICALLY CHARACTERIZED**, exact arithmetic, `r\le30`; my implementation reproduces the wave-8 referee's §A.5 table exactly |
| 13 | Lemma 7: `\|F_r(1-\cdot,b)\|=F_r(2,b)`, `\|\hat H_r\|=2F_r(2,b{+}1)` | **PROVED** (sign alignment under `s\mapsto1{-}s`), verified exactly `r=0..24`, `b=0..3` |
| 14 | The coefficient-sum norm costs `\Theta((9/8)^r)`: `F_r(2,0)\sim\frac32\varphi_r(9/8)^r` | **NUMERICALLY CHARACTERIZED** with a derived mechanism (summand peaks at `i=(2r{-}1)/3`, inside range); ratio measured `1.125012` at `r=60`, `F_r(2,0)/[\varphi_r(9/8)^r]\to1.4999` |
| 15 | Proposition 6: the improved recursion `C'_r,D'_r` is rigorous and still proves the Target Theorem | **PROVED** — `r/n\le r/(b{+}r{+}1)` on the theorem's own hypothesis `n\ge b{+}r{+}1`, and `(n{-}a{-}1{-}b{-}r)/n\in[0,1]` on the valid domain |
| 16 | The improved bound is geometric, ratio `\approx1.24` at `r=45` | **NUMERICALLY CHARACTERIZED**; its exact rate is OPEN |
| 17 | A polynomial-in-`r` rigorous bound | **OPEN** (§8.3 item 1) — both remaining obstructions named |
| 18 | Closed form for `D^*_r(b)`, `b\ge1` | **OPEN** (§8.3 item 2) |
| 19 | All-orders closed form for `ψ_n^{(K)}` (open item (i)) | **NOT CLOSED.** One further rung supplied in closed form (§8.2); no uniform-in-order statement attempted |
| 20 | Independent adversarial re-verification of this document | **NOT PERFORMED** — required before any integration (§8.4) |

**Net honest verdict.** Open item (ii) is **answered**: the true residual constant
is `\Theta(r^{3/2})` with the explicit leading constant `3\sqrt\pi/64` and, at
`b=0`, the exact closed form `\frac{r(3r+1)}{32}\varphi_r-\frac r{12}`; the
published bound is factorial; and the entire discrepancy is accounted for by two
named, measured mechanisms, one of which is removable by a one-line rigorous
change that improves the bound from `\tilde\Theta(r!)` to geometric. This is a
*positive* result and is therefore **not** catalogued by this document: it requires
the archive's mandatory hostile-referee pass first, focused on §3.1 (§8.4). Nothing
here weakens any existing result — the Target Theorem of `DISC-DEC-040`, Teorema 3,
and the Estágio 7 rate coefficient are all untouched; only the *quality* of the
error constants, and the status of open item (ii), change.

---

## 10. Files, reproducibility

All scripts were written from scratch in this directory; nothing is imported from
any sibling or predecessor directory. All use exact `fractions.Fraction` /
`sympy.Rational` / `sympy.Symbol` arithmetic; floating point appears only in
display columns and in `asymptotics.py` PART 3's `mpmath` (dps 60) large-`r`
evaluation, which is cross-checked against exact rationals (§0).

| file | contents | runtime |
|---|---|---|
| `core.py` | own `Poly` type over `Fraction`; re-transcribed `F_r,G_r` closed forms and `\hat H_r,K_r` definitions (labeled reuse); **new** `H_r,L_r`; own exact `(a,b,r)` `Chain` simulator; residuals; `\varphi_r` | seconds |
| `validate_third_order.py` / `.log` | §4: simulator validated against wave-5/6 PROVED facts; `n^2\max|R_r|\to\max|H_r|`; `n^3\max|R^{(3)}_r|` stabilises; exact-identity spot checks | ~2 min |
| `verify_closed_form.py` / `.log` | §3.3: 10143 exact checks (V1), degrees (V1b), symbolic-`b` ladder `r=0..11` (V2) | ~47 s |
| `verify_ek_recursion.py` / `.log` | §3.2/§3.3: STAGE A (recursion **is** the ODE), STAGE B2 (closed form satisfies it, integers), STAGE B1 (**symbolic `r,k,b`**, both branches `=0`) | ~15 s |
| `asymptotics.py` / `.log` | §5: Theorem 3 exact `r\le80`; the three binomial identities; large-`r` behaviour to `r=10^5`; finite-`n` excess | ~3 min |
| `growth_true.py` | §5: exact `D^*_r(b)` table and coefficient-positivity sweep (superseded by the closed form, retained as the pre-closed-form evidence) | ~10 s |
| `loose_bound.py` / `.log` | §6.4: own bivariate `\Delta_r(t,b,h)`; `A_r,B_r,D_r,C_r`; reproduces the referee's §A.5 table exactly; factorial growth | ~1 s |
| `gap_diagnosis.py` / `.log` | §6.1/§6.2: Lemma 7 verified; the `(9/8)^r` rate; the improved recursion side-by-side | ~8 s |
| `third_order_existence.py` / `.log` | §4: `\Delta^{(3)}_r` brackets vanish; `A^{(3)},B^{(3)},D^{(3)},C^{(3)}`; 0 violations on exhaustive exact data | ~12 s |
| `cross_checks.py` / `.log` | §7.1: five exact confirmations + own out-of-sample interpolation; §5.3 exhaustive `S_r` scan; improved bound to `r=45` | ~46 s |
| `cross_checks_h_side.log` | §7.1: the sixth confirmation, `\hat H_2(0,0),K_2(0,0),L_2(0,0)` vs `ψ_n^{(3),R}` | seconds |
| `finite_n_sup.py` / `.log`, `sup_large_r.py`, `finite_n_sup_large_r.log` | §5.3: where `S_r` is attained; `S_r(b)` to `r=150` | ~2 + ~5 min |
| `PROGRESS.log` | chronological checkpoint trail, including the by-hand derivations recorded *before* the corresponding code was written | — |

Reproduce in this order: `python3 core.py`; `python3 validate_third_order.py`;
`python3 verify_closed_form.py 45 8 11`; `python3 verify_ek_recursion.py 40 6`;
`python3 loose_bound.py 16`; `python3 gap_diagnosis.py 60 30`;
`python3 third_order_existence.py 24 4`; `python3 asymptotics.py 80`;
`python3 cross_checks.py 45`; `python3 finite_n_sup.py 60 22 60`;
`python3 sup_large_r.py`.
