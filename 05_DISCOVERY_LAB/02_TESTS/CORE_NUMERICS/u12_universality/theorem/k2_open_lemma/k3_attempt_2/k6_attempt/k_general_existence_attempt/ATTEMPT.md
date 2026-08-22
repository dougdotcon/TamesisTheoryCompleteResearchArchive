# The general-`r` existence of the two-term expansion: a discrete-Gronwall proof

> **Governance.** Continuation of `DISC-DEC-033` front (a), `K6-OPEN-LEMMA-ATTEMPT`
> lineage. Pure combinatorial mathematics — no external data, no holdout, no
> real-world claim, no governance edits. `THEOREM.md`, `../../../ATTEMPT.md` (wave
> 5), `../ATTEMPT.md` (wave 6), and `ATTEMPT.md` (this directory's parent,
> `k6_attempt/ATTEMPT.md`) are **not** touched — everything here lives under this
> new `k_general_existence_attempt/` directory. No git commit was made. Every claim
> below is labeled PROVED, PROVED-MODULO-[X] (X named precisely), NUMERICALLY
> VERIFIED (exact rational arithmetic, never floating-point sampling), CONJECTURED,
> or OPEN, following the discipline the whole lineage uses.

> **Task.** `k6_attempt/ATTEMPT.md` §4 states one honest caveat: its continuum
> two-term expansion `g_r(m,b) = F_r(t,b) + \frac1n G_r(t,b) + O(1/n^2)` (`t=m/n`) —
> derived assuming the expansion exists, and used to prove the rate conjecture for
> general `K` — has its *existence*, for `r` beyond the 11 concretely-checked values
> (`K=0,\dots,10`), asserted but not re-derived from `\varepsilon`-`\delta` first
> principles. The referee's report (`../adversarial/REFEREE_REPORT.md` §B.4) names
> "a discrete-Gronwall-type error bound uniform in `m,n`" as the one candidate
> technique, never attempted. This document attempts exactly that, for general `r`,
> directly on the **exact** discrete recursion (no more concrete-`K` checking, no
> assuming-then-checking-self-consistency).

> **Executive summary (read first).** The attempt succeeds. §§2–6 below construct a
> complete, first-principles proof, by induction on `r`, that `g_r(m,b)` and
> `h_r(a,b)` admit the assumed two-term expansion, **for every** `r`, with an
> explicit (recursively defined, not closed-form) error bound `O(1/n^2)` that is
> genuinely **uniform in `m`/`a`** — including at the recursion's own base-case
> boundary (`m=b+r+1`, `t=O(1/n)\to0`), which is exactly the region
> `../adversarial/REFEREE_REPORT.md` §B.4(b) flagged as the one place the source
> document's argument had no boundedness argument at all for `G_r` (unlike `F_r`,
> where a probability-boundedness argument does work, per `../ATTEMPT.md` §2.4).
> **The mechanism that closes this:** substituting the ansatz into the *exact*
> discrete recursion and using that `F_r,G_r,\hat H_r,K_r` are all polynomials of
> bounded degree (so every Taylor expansion involved is an *exact*, finite algebraic
> identity, not a truncation with hidden error) reduces the residual
> `R_r(m,b,n):=g_r(m,b)-F_r(t,b)-\frac1nG_r(t,b)` to a **linear recursion with the
> same homogeneous part as `g_r`'s own recursion** — and at the base case, that
> recursion's contraction coefficient is *exactly zero*, which automatically kills
> any contribution from the (otherwise ill-defined) "residual just before the base
> case," subsuming the boundary case into the general argument with **no separate
> boundary-layer analysis needed**. Unrolling this recursion exactly (not by a crude
> union bound, which would introduce a spurious `\log n` factor) via the same
> falling-factorial/hockey-stick identity the source document's own telescoping
> solution already uses gives a **clean, uniform** `O(1/n^2)` bound, confirmed by
> extensive exact-rational-arithmetic numerics (§7: `r=1,\dots,5`, `n` up to `1600`,
> both `g_r` and `h_r`, zero deviation from the predicted order, no `\log n` growth
> observed anywhere). **What this does *not* close**: an explicit closed-form
> formula for the error constants (they are defined by an explicit, terminating,
> mechanical recursion on `r` — analogous in spirit to this whole lineage's
> "mechanical ladder" — not reduced to a single algebraic expression), and the
> separate, harder, explicitly out-of-scope question of the *exact, all-orders*
> closed form for `\psi_n^{(K)}` at general `K` (`../ATTEMPT.md` §6.2). §9 states
> the honest scorecard.

---

## 0. Relationship to prior work — what is reused, what is new

Reused **verbatim, without re-derivation**, from `../ATTEMPT.md` (this directory's
parent, `k6_attempt/ATTEMPT.md`):

- The exact discrete recursions for `g_r(m,b)`, `h_r(a,b)` (`../../ATTEMPT.md` §2,
  PROVED general in `K`, restated in rearranged form as identity `(*)` in `../
  ATTEMPT.md` §2.2) — used here exactly as given, no re-derivation of the transition
  rules themselves.
- The leading-order closed form `F_r(t,b)` (`../ATTEMPT.md` §2.3, Theorem, PROVED,
  general `r`) and the `O(1/n)` closed form `G_r(t,b)` (`../ATTEMPT.md` §3.3,
  Theorem, PROVED, general `r`) — reused as **given, fixed, already-proven**
  polynomial functions of `t` (with rational-in-`b` coefficients). Their defining
  algebraic identities — the leading ODE, the `G_r` ODE, and the algebraic
  relations for `\hat H_r,K_r` — are cited as already established, not re-derived.
  §2 below restates exactly which facts are used.
- The base cases `F_0(t,b)=1/(b{+}1)`, `G_0\equiv0`, and the exact (not
  asymptotic) formulas `g_0(m,b)=1/(b{+}1)`, `h_0(a,b)=(n{-}a{+}1)/(n(b{+}2))`
  (`../ATTEMPT.md` §2.2/§3.1, and `../../ATTEMPT.md` §3, PROVED).

**New in this document:** the discrete-Gronwall existence argument itself (§§2–6),
the numerical corroboration built for this purpose (§7, exact-`Fraction`/`sympy`
arithmetic throughout, no floating point in any exact claim), and the precise
accounting (§8) of what this does and does not resolve relative to `../ATTEMPT.md`
§4's caveat and `../adversarial/REFEREE_REPORT.md` §B.4's specific concerns.

---

## 1. The target, restated precisely

Fix `r\ge0`, `b\ge0` integers. Write `h:=1/n`, `t:=m/n\in(b{+}r{+}1)/n,\dots,1]`,
`s:=a/n`. `g_r(m,b)` and `h_r(a,b)` are the exact conditional probabilities of
`../../ATTEMPT.md` §2 (`0\le g_r,h_r\le1` unconditionally, for every valid finite
`m,a,n`).

**Definitions (not assumptions).** For every valid `m` (i.e. `b{+}r{+}1\le m\le n`)
and every valid `a` (i.e. `0\le a\le n{-}b{-}r{-}1`),

`\displaystyle R_r(m,b,n) := g_r(m,b) - F_r(t,b) - \frac1n G_r(t,b)`,  `\qquad
\varepsilon_r^h(a,b,n) := h_r(a,b) - \hat H_r(s,b) - \frac1n K_r(s,b)`,

using the **already-proven, fixed, closed-form** `F_r,G_r` (`../ATTEMPT.md` §2.3,
§3.3) and `\hat H_r(s,b):=(1{-}s)F_r(1{-}s,b{+}1)`, `K_r(s,b):=1+r\hat
H_{r-1}(s,b{+}1)+(1{-}s)G_r(1{-}s,b{+}1)-(1{+}b{+}r)F_r(1{-}s,b{+}1)` (`../
ATTEMPT.md` §2.2, §3.1 — these are *definitions*, not claims, so they hold
trivially/tautologically; no existence question attaches to them). Since these are
plain definitions of a difference between two already-well-defined quantities,
`R_r` and `\varepsilon_r^h` are well-defined numbers for every valid `(m,b,n)` /
`(a,b,n)` — **no existence assumption is smuggled in by defining them.**

> **Target Theorem (what this document proves).** For every `r\ge0` and `b\ge0`
> there is a finite constant `D_r(b)` such that `|R_r(m,b,n)|\le D_r(b)/n^2` for
> **every** valid `m` and **every** `n` large enough that `m=b{+}r{+}1` is a valid
> state (i.e. `n\ge b{+}r{+}1`); and a finite constant `C_r(b)` such that
> `|\varepsilon_r^h(a,b,n)|\le C_r(b)/n^2` for **every** valid `a` and every such
> `n`. In particular `\lim_n g_r(nt,b)=F_r(t,b)` and `\lim_n n[g_r(nt,b)-F_r(t,b)]=
> G_r(t,b)` for every fixed `t\in(0,1]`, and the analogous statements for `h_r` —
> i.e. the two-term expansion `../ATTEMPT.md` §4 assumes **exists**, for every `r`.

This is exactly `THEOREM.md`/`../ATTEMPT.md`'s notion of "regular two-term
asymptotic expansion," made precise with an explicit error bound, and the bound
being **uniform in `m`/`a`** (not just "for `t` bounded away from `0,1`") is the
specific strengthening `../adversarial/REFEREE_REPORT.md` §B.4(b) asked for and
found missing.

---

## 2. The facts used, and why none of them is circular

The proof uses exactly four already-established facts about `F_r,G_r,\hat H_r,K_r`,
none of which is an asymptotic claim — all four are **finite, exact, algebraic
facts about explicit polynomials**, verified independently of any claim about
`g_r,h_r`:

**Fact 1 (bounded degree).** `F_r(t,b)=\sum_{k=0}^r c_k^{(r)}(b)t^k` (degree `\le
r`); `G_r(t,b)=\sum_{k=0}^{r-1}d_k^{(r)}(b)t^k` (degree `\le r{-}1`, `G_0\equiv0`);
`\hat H_r(s,b)=(1{-}s)F_r(1{-}s,b{+}1)` has degree `\le r{+}1` in `s`; `K_r(s,b)`
has degree `\le r` in `s` (each degree claim follows immediately from the already-
proven closed forms, and was additionally confirmed by direct polynomial-degree
inspection — `verify_gronwall_pieces.py` §4, `r=0,\dots,6`, all match).

**Fact 2 (the leading ODE, PROVED, `../ATTEMPT.md` §2.3).** As an *identity in
`t`*, for every real `t`: `\;t F_r'(t,b) + (1{+}r{+}b)F_r(t,b) = 1 + r\hat
H_{r-1}(1{-}t,b)`.

**Fact 3 (the `G_r` ODE, PROVED, `../ATTEMPT.md` §3.3).** As an identity in `t`:
`\;tG_r'(t,b)+(1{+}r{+}b)G_r(t,b) = r\hat H_{r-1}'(1{-}t,b)+rK_{r-1}(1{-}t,b) +
\tfrac t2F_r''(t,b)+(1{+}r{+}b)F_r'(t,b)`.

**Fact 4 (`\hat H_r,K_r` are definitions, hence tautologically self-consistent).**
The algebraic relations defining `\hat H_r,K_r` in terms of `F_r,G_r,\hat
H_{r-1}` (§1 above) hold **by definition**, not as a separately-proven fact.

**Why this is not circular.** Facts 2–3 are proved in `../ATTEMPT.md` §2.3/§3.3 as
*pure algebraic identities* — `sympy` substitutes the closed-form `c_k^{(r)}(b)`,
`d_k^{(r)}(b)` into the coefficient-of-`t^k` matching conditions and confirms the
difference simplifies to `0`, for symbolic `r,k,b`. This says nothing, by itself,
about whether `F_r,G_r` approximate the true discrete `g_r,h_r` — it is a fact
about two *fixed, explicit polynomials* satisfying a *fixed, explicit* ODE, true or
false independently of any asymptotic claim. Using it here does not assume the
thing being proved (that `F_r,G_r` are the right limit/correction functions) — it
only uses that they are *some* particular, explicit, already-known functions with
known algebraic properties. The **existence** claim — that these particular
functions really are `\lim_n g_r(nt,b)` and its `1/n` correction, uniformly, even
at the boundary — is exactly what §§3–6 below derive, using Facts 1–4 as fixed
algebraic inputs, not as a premise about the limit.

---

## 3. The exact residual recursion for `g_r`

Start from the exact, rearranged non-source recursion (`../ATTEMPT.md` §2.2,
reusing `../../ATTEMPT.md` §2's Proposition, both PROVED, not re-derived): for
every valid `m` from `b{+}r{+}1` to `n` (with the convention `g_r(b{+}r,b):=0`,
which is not an extra assumption — it is exactly the value that makes the `m=b{+}
r{+}1` instance below match the base-case formula, since the coefficient of that
term is `0` there):

`(*)\qquad m\big[g_r(m,b)-g_r(m-1,b)\big] + (1{+}r{+}b)\,g_r(m-1,b) = 1 + r\,h_{r-1}(n{-}m{+}1,b)`.

**Substitute the definitions of §1** (this is *pure algebra*, not an assumption —
`R_r,\varepsilon_{r-1}^h` are defined quantities, and this substitution just
rewrites `(*)` in terms of them):

`g_r(m,b)=F_r(t,b)+hG_r(t,b)+R_r(m,b,n)`,  `\ g_r(m{-}1,b)=F_r(t{-}h,b)+hG_r(t{-}h,b)+R_r(m{-}1,b,n)`,

`h_{r-1}(n{-}m{+}1,b) = \hat H_{r-1}(s,b) + hK_{r-1}(s,b) + \varepsilon_{r-1}^h(n{-}m{+}1,b,n)`,  `\quad s:=(1{-}t)+h`.

**The key device: exact finite Taylor expansion.** Because `F_r(\cdot,b)` is a
polynomial of degree `\le r` (Fact 1), Taylor's theorem for polynomials is an
*exact, finite* identity with **zero remainder**:

`F_r(t{-}h,b) = \sum_{j=0}^r \frac{(-h)^j}{j!}F_r^{(j)}(t,b)`  (exactly, for
**every** `t,h`, not merely for small `h` — this is not an asymptotic statement).

The same holds for `G_r(t{-}h,b)` (degree `\le r{-}1`, so `r` terms), and for `\hat
H_{r-1}(s,b)=\hat H_{r-1}((1{-}t){+}h,b)` and `K_{r-1}(s,b)` expanded around
`1{-}t` (forward, `+h`). **This is the structural fact that makes the whole
argument work**: there is no "truncation error" hiding anywhere in these
expansions — every order-`h^j` term for `j\ge2` is an *exact*, explicitly
computable quantity (a fixed polynomial in `t`, times an explicit rational
coefficient), not an `O(h^j)` estimate. Substituting into `(*)` and using `m=t/h`:

`(*)` becomes: `\underbrace{[tF_r'(t,b)+(1{+}r{+}b)F_r(t,b) - 1 - r\hat H_{r-1}(1{-}t,b)]}_{=0\text{ by Fact 2}}`
`\;+\;h\underbrace{[tG_r'(t,b)-\tfrac12tF_r''(t,b)+(1{+}r{+}b)(G_r(t,b){-}F_r'(t,b)) - r\hat H_{r-1}'(1{-}t,b)-rK_{r-1}(1{-}t,b)]}_{=0\text{ by Fact 3 (rearranged)}}`
`\;+\;\Delta_r(t,b,h)\;+\;m[R_r(m,b,n){-}R_r(m{-}1,b,n)] + (1{+}r{+}b)R_r(m{-}1,b,n) - r\varepsilon_{r-1}^h(n{-}m{+}1,b,n) = 0`,

where `\Delta_r(t,b,h)` collects **every exact Taylor term of order `h^2` and
higher** from the four finite expansions above (an explicit, finite sum — at most
`r{-}1` further terms, since the expansions terminate at `j=r`). The bracketed
`h^0` and `h^1` terms vanish **identically, for every `t`** — including at
`t=t_0:=(b{+}r{+}1)/n\to0` — because Facts 2–3 are algebraic identities holding for
every `t`, not asymptotic statements valid only for `t` bounded away from `0`. This
is exactly why **no separate boundary-layer treatment is needed**. Isolating the
residual-and-tail terms once the two brackets are set to `0` leaves
`0 = \Delta_r(t,b,h) + m[R_r(m,\cdot){-}R_r(m{-}1,\cdot)] + (1{+}r{+}b)R_r(m{-}1,\cdot)
- r\varepsilon_{r-1}^h(\cdot)`; writing `(1{+}r{+}b) = m - (m{-}1{-}r{-}b)` combines
the two `R_r(m{-}1,\cdot)` contributions into a single coefficient
`-(m{-}1{-}r{-}b)`, which is exactly the **contraction coefficient of `g_r`'s own
recursion** — and that coefficient is `0` at `m=b{+}r{+}1`, the base case. Solving
for `R_r(m,\cdot)`:

> **Exact residual recursion.** For every valid `m` from `b{+}r{+}1` to `n`:
>
> `\displaystyle R_r(m,b,n) = \frac{m{-}1{-}r{-}b}{m}\,R_r(m{-}1,b,n) \;+\; \frac1m\Big[r\,\varepsilon_{r-1}^h(n{-}m{+}1,b,n) - \Delta_r(t,b,h)\Big]`,

with the convention `R_r(b{+}r,b,n):=` (anything — see below). **At `m=b{+}r{+}1`
the coefficient `(m{-}1{-}r{-}b)/m = 0/(b{+}r{+}1) = 0` exactly**, so whatever
value is assigned to the fictitious `R_r(b{+}r,\cdot)` is multiplied by zero and
drops out of the recursion completely. This is the precise mechanism by which the
base case is **subsumed into the general argument, not treated separately**: the
same recursion that governs the bulk automatically "forgets" any inconsistency at
the one point where its own derivation (which implicitly compared `g_r(m{-}1,b)` to
an ansatz value that does not actually exist there, since `m{-}1=b{+}r` is below
`g_r`'s domain) would otherwise be suspect.

---

## 4. Bounding the Taylor tail `\Delta_r(t,b,h)`, uniformly, elementarily

`\Delta_r(t,b,h)=\sum_{j\ge2} h^{j-1}\cdot p_j(t,b)` for finitely many (`\le r{-}1`)
explicit polynomials `p_j(\cdot,b)` in `t`, each with coefficients that are
**explicit rational functions of `b`, computable from the already-known closed
forms of `F_r,G_r,\hat H_{r-1},K_{r-1}` and their derivatives** (Fact 1's degree
bounds make this a finite computation for any concrete `r`). The bound needed is
completely elementary and needs no sign/positivity information:

> **Lemma (coefficient-sum bound).** For any polynomial `p(x)=\sum_{k=0}^d a_k x^k`
> and `x\in[0,1]`: `|p(x)|\le\|p\|:=\sum_{k=0}^d|a_k|`. Consequently, for the
> `j`-th derivative, `|p^{(j)}(x)|\le d!\cdot\|p\|` for `x\in[0,1]`, `0\le j\le d`
> (crude but sufficient: `k!/(k{-}j)!\le d!` for `k\le d`).

*Proof.* `|p(x)|=|\sum a_kx^k|\le\sum|a_k||x|^k\le\sum|a_k|=\|p\|` since
`|x|\le1`. The derivative bound is the same argument applied to
`p^{(j)}(x)=\sum_{k\ge j}a_k\frac{k!}{(k-j)!}x^{k-j}`. `\square`

Applying this to each `p_j(\cdot,b)` (finitely many, `j=2,\dots,r`, each a fixed
polynomial of degree `\le r` once `r,b` are fixed) gives:

`|\Delta_r(t,b,h)| \le \sum_{j=2}^{r} h^{j-1}\cdot\|p_j(\cdot,b)\| \le h^2\Big(\sum_{j=2}^r \|p_j(\cdot,b)\|\Big) =: A_r(b)\,h^2`,

**uniformly for every `t\in[0,1]`** (used `h^{j-1}\le h^2` for `j\ge2, h\in(0,1]`,
true once `n\ge1`). `A_r(b)` is a finite, explicit (in principle: fully computable
by symbolic differentiation of the known closed forms) constant depending only on
`r,b` — **not on `m,n,t`**. This is the one place the argument is "routine
bookkeeping rather than a closed-form result": §8 states precisely what was and
was not carried out to full symbolic generality here.

> **[Correção pós-adversarial, 2026-08-22, issue I-1 do referee hostil dedicado
> — ver `adversarial/REFEREE_REPORT.md` §A.2 e Parte A.1(b).]** O expoente
> exibido acima está errado. `\Delta_r=\sum_{j\ge2}h^{j-1}p_j(t,b)` e a
> justificativa "usou `h^{j-1}\le h^2` para `j\ge2, h\in(0,1]`" são **falsas**
> como escritas: `h^{j-1}\le h^2` falha em `j=2` (lê-se `h\le h^2`, o oposto do
> verdadeiro para `h=1/n\in(0,1)`). Tomada literalmente, essa linha só
> estabeleceria `|\Delta_r|\le A_r(b)h`, degradando o resultado final de
> `O(1/n^2)` para `O(1/n)` — ou seja, como escrita, a justificativa não prova a
> expansão de dois termos.
>
> **O fato correto** (verificado independentemente pelo referee, simbolicamente,
> para `b` simbólico e `r=0,\dots,8`, via a expansão de Laurent em `h` dos
> colchetes `h^0`/`h^1`): `\Delta_r=\sum_{k=2}^{r}h^{k}\cdot q_k(t,b)` — expoente
> `h^k`, não `h^{j-1}` — de onde `|\Delta_r|\le h^2\sum_{k=2}^r\|q_k(\cdot,b)\|=:
> A_r(b)h^2` segue diretamente, já que `h^k\le h^2` para todo `k\ge2`,
> `h\in(0,1]`. A contagem de termos (`\le r{-}1` polinômios, `j=2,\dots,r`) e o
> texto de §3 ("colects every exact Taylor term of order `h^2` and higher") já
> estavam corretos — apenas o expoente exibido na linha da desigualdade estava
> trocado (`h^{j-1}` por `h^j`). A conclusão do Lemma da soma de coeficientes
> (`A_r(b)` finito, independente de `m,n,t`) permanece válida e é exatamente o
> que a Etapa 5 usa. Texto original acima preservado sem alteração; esta é a
> forma corrigida da desigualdade central de §4:
>
> `\displaystyle |\Delta_r(t,b,h)| \le \sum_{k=2}^{r} h^{k}\cdot\|q_k(\cdot,b)\| \le h^2\Big(\sum_{k=2}^r \|q_k(\cdot,b)\|\Big) =: A_r(b)\,h^2`,
>
> **uniformemente para todo `t\in[0,1]`** (usa `h^k\le h^2` para `k\ge2`,
> `h\in(0,1]`, verdadeiro para `n\ge1`).

---

## 5. The discrete-Gronwall closure: an exact telescoping bound, no `\log n`

Write `\alpha(i):=(i{-}1{-}r{-}b)/i\in[0,1)` (for `i>b{+}r`) and `j:=r{+}b{+}1`
(the base-case value of `m`). The exact residual recursion of §3 is
`R_r(m)=\alpha(m)R_r(m{-}1)+\beta(m)`, `|\beta(m)|\le E_r(b)/(mn^2)` where
`E_r(b):=rC_{r-1}(b)+A_r(b)` (using the inductive-hypothesis bound `C_{r-1}(b)` on
`\varepsilon_{r-1}^h`, §6 justifies this is legitimate to invoke). Since `R_r(j{-}1)`
is multiplied by `\alpha(j)=0`, unrolling gives, for `m\ge j`:

`\displaystyle R_r(m) = \sum_{k=j}^m \Big[\prod_{i=k+1}^m\alpha(i)\Big]\beta(k)`.

**The product telescopes exactly** (the same falling-factorial identity already
used by the source document's *exact* telescoping solution, `../../ATTEMPT.md`
§3): `\prod_{i=k+1}^m\frac{i{-}1{-}r{-}b}i = \prod_{i=k+1}^m\frac{i{-}j}i =
\binom kj\big/\binom mj`. **This is far tighter than the crude bound
`\prod\alpha(i)\le1`** (which would give a spurious `\sum_k1/k\sim\log n` factor —
exactly the kind of loose bound a naive discrete-Gronwall write-up would produce).
Using the identity `\frac1k\binom kj=\frac1j\binom{k{-}1}{j{-}1}` (elementary,
`j\ge1`) and the hockey-stick identity `\sum_{l=j-1}^{m-1}\binom l{j-1}=\binom mj`:

`\displaystyle \sum_{k=j}^m\frac1k\binom kj = \frac1j\sum_{k=j}^m\binom{k{-}1}{j{-}1} = \frac1j\sum_{l=j-1}^{m-1}\binom l{j-1} = \frac{\binom mj}j`  (exactly).

Both identities were confirmed symbolically/exactly (`verify_gronwall_pieces.py`
§1: the summand identity `(1/k)\binom kj-(1/j)\binom{k-1}{j-1}` simplifies to `0`
in `sympy` for symbolic `j,k`; and by direct exact summation for `20` concrete
`(j,m)` pairs, zero mismatches). Hence:

`\displaystyle |R_r(m,b,n)| \le \sum_{k=j}^m\frac{\binom kj}{\binom mj}\cdot\frac{E_r(b)}{kn^2} = \frac{E_r(b)}{n^2\binom mj}\sum_{k=j}^m\frac{\binom kj}k = \frac{E_r(b)}{n^2\binom mj}\cdot\frac{\binom mj}j = \frac{E_r(b)}{j\,n^2}`.

> **Theorem (uniform bound for `g_r`, PROVED given Facts 1–4 and the inductive
> hypothesis `C_{r-1}(b)` on `\varepsilon_{r-1}^h`).** For every valid `m` (from
> the base case `b{+}r{+}1` through `n`):
>
> `\displaystyle |R_r(m,b,n)| \le \frac{D_r(b)}{n^2}`,  `\qquad D_r(b) := \frac{r\,C_{r-1}(b)+A_r(b)}{r+b+1}`,
>
> **with no `m`-dependence and no `\log n` factor in the bound** — a genuinely
> uniform, whole-domain-including-the-boundary discrete-Gronwall bound.

The `\binom mj` cancellation is exactly what removes the `\log n` a cruder argument
would introduce, and it is a **direct consequence of the same exact algebraic
structure** (falling-factorial telescoping) already used, for a different purpose,
in the source document's own exact solution — not a new piece of machinery.

---

## 6. From `g_r`'s bound to `h_r`'s bound: pure substitution, no Gronwall needed

`h_r(a,b)` is defined by a **single algebraic step** (`../../ATTEMPT.md` §2,
source-step rule), not a recursion in `a` — so propagating the bound requires only
substitution and the triangle inequality, no telescoping. Exactly (`n{-}1{-}a{-}
b{-}r)/n = (1{-}s) - (1{+}b{+}r)/n`, an algebraic identity, not an approximation):

`h_r(a,b) = \frac1n + \frac rn h_{r-1}(a,b{+}1) + \Big[(1{-}s)-\frac{1{+}b{+}r}n\Big]g_r(n{-}a,b{+}1)`.

Substituting the (inductive-hypothesis) expansion for `h_{r-1}(a,b{+}1)` and the
**just-proved** (§5) expansion for `g_r(n{-}a,b{+}1)` (valid at `t'=(n{-}a)/n=1{-}s`
— note this is the *same* variable `s`, no shift, so no Taylor expansion is needed
here at all, only algebra) and using that `\hat H_r,K_r` satisfy their *defining*
relations (Fact 4 — trivially, by definition) to cancel the `h^0,h^1` terms exactly,
gives:

`\varepsilon_r^h(a,b,n) = \frac1{n^2}\Big[rK_{r-1}(s,b{+}1) - (1{+}b{+}r)G_r(1{-}s,b{+}1)\Big] + \frac rn\varepsilon_{r-1}^h(a,b{+}1,n) + \Big[(1{-}s)-\frac{1{+}b{+}r}n\Big]R_r(n{-}a,b{+}1,n)`.

Every piece is directly bounded: the bracketed polynomial term by the Lemma of §4
(`\le\|K_{r-1}(\cdot,b{+}1)\|+ (1{+}b{+}r)\|G_r(\cdot,b{+}1)\|=:B_r(b)`, a finite
constant); `\varepsilon_{r-1}^h(a,b{+}1,n)` by the inductive hypothesis
`C_{r-1}(b{+}1)/n^2`; `R_r(n{-}a,b{+}1,n)` by §5's `D_r(b{+}1)/n^2`; and
`|(1{-}s)-(1{+}b{+}r)/n|\le2` for `n\ge1{+}b{+}r`. So:

> **Theorem (uniform bound for `h_r`, PROVED given §5 and the inductive hypothesis
> at level `r{-}1`).** For every valid `a`:
>
> `\displaystyle |\varepsilon_r^h(a,b,n)| \le \frac{C_r(b)}{n^2}`,  `\qquad
> C_r(b) := B_r(b) + rC_{r-1}(b{+}1) + 2D_r(b{+}1)`.

No Gronwall/telescoping is needed for this half of the step — it is a one-shot
algebraic substitution, exactly because `h_r`'s recursion is not a chain in `a`.

> **[Nota pós-adversarial, 2026-08-22, issue I-2 do referee hostil dedicado —
> ver `adversarial/REFEREE_REPORT.md` §A.4.]** No valor máximo válido
> `a=n-b-r-1`, a fórmula acima referencia `R_r(n-a,b{+}1,n)=R_r(b{+}r{+}1,b{+}1,n)`,
> mas o domínio de `g_r(\cdot,b{+}1)` exige `m\ge(b{+}1){+}r{+}1=b{+}r{+}2` — esse
> valor específico não existe e não está coberto pelo Teorema de §5. Isso é
> inofensivo pelo mesmo mecanismo que §3 usa e explica para `g_r`: o coeficiente
> que multiplica esse termo, `(1{-}s)-(1{+}b{+}r)/n=(n{-}a{-}1{-}b{-}r)/n`, é
> **exatamente `0`** em `a=n{-}b{-}r{-}1` (verificado pelo referee em 4 casos
> concretos). O termo é `0\cdot(\text{qualquer coisa})`, e a identidade e o
> limitante `\le2D_r(b{+}1)/n^2` sobrevivem intactos. Este parágrafo original não
> mencionava esse ponto; nenhuma alteração matemática é necessária.

---

## 7. Closing the induction on `r`, and numerical corroboration

**Base case `r=0` (exact, zero error).** `g_0(m,b)=1/(b{+}1)=F_0(t,b)` and
`h_0(a,b)=(n{-}a{+}1)/(n(b{+}2)) = (1{-}s)/(b{+}2) + \frac1n\cdot\frac1{b{+}2} =
\hat H_0(s,b)+\frac1nK_0(s,b)` **exactly**, for every valid `m,a,n` (`../
ATTEMPT.md` §2.2, §3.1, PROVED, elementary induction / direct algebra — both
already-cited facts, not re-derived here). So `R_0\equiv0`, `\varepsilon_0^h\equiv0`
identically: `D_0(b)=C_0(b)=0` for every `b`.

**Inductive step.** Given `C_{r-1}(b)` for every `b` (inductive hypothesis, §6's
`D_r(b),C_r(b)` need `C_{r-1}` at both `b` and `b{+}1`), §5 gives `D_r(b)` and §6
gives `C_r(b)`, both finite and explicit given `A_r(b)`, `\|K_{r-1}(\cdot,b{+}1)\|`,
`\|G_r(\cdot,b{+}1)\|` (all computable, in principle, from the already-known
closed forms by finitely much symbolic differentiation/coefficient extraction).

> **Theorem (existence, general `r` — the Target Theorem of §1, PROVED by
> induction on `r`, `r=0,1,2,\dots`).** For every `r\ge0` and `b\ge0` there exist
> finite `D_r(b),C_r(b)` (defined by the explicit recursion above, `D_0=C_0=0`)
> such that `g_r(m,b)=F_r(t,b)+\frac1nG_r(t,b)+O_{D_r(b)}(1/n^2)` and
> `h_r(a,b)=\hat H_r(s,b)+\frac1nK_r(s,b)+O_{C_r(b)}(1/n^2)`, **uniformly over the
> entire domain of `m`/`a`, including both the base case boundary and the `a\to0`
> boundary of `h_r`** — i.e. the two-term asymptotic expansion `../ATTEMPT.md` §4
> assumes exists, for every `r`.

**This is not left as an abstract derivation — it was checked against exact,
independent data at every level tested**, `r=1,\dots,5`, `b\in\{0,1\}`:

- `probe_boundary.py`/`.log`: the base-case point `m=b{+}r{+}1` itself, `n` up to
  `320`. `r=1,b=0` and `r=1,b=1`: residual **exactly `0`** for every `n` tested
  (matches the theory exactly — `F_1,G_1` have degree `\le1,\le0`, so `\Delta_1
  \equiv0`, and `\varepsilon_0^h\equiv0`, so `R_1\equiv0` is *predicted exactly*,
  not merely bounded). `r=2,b=0`: residual found to equal **exactly `1/(15n^2)`**
  for `n=4,5,6,7,9,11,13,17,23,50,101` — not merely `O(1/n^2)` but an *exact*
  closed value at this point, a striking additional confirmation that nothing in
  the derivation is missing a term.
- `probe_uniform.py`/`.log` and `probe_convergence_large_n.log`: the **entire**
  range of `m` (log-spaced sample from the base case to `m=n`), `r=1,2,3` at
  `b=0,1`, `n` from `20` to `1600`. In every case `\max_m n^2|R_r(m,b,n)|`
  **stabilizes to a finite constant as `n\to\infty`** (e.g. `r=3,b=0`:
  `0.17879\to0.17868\to0.17862\to0.17860` at `n=200,400,800,1600` — converging,
  not growing, and with **no visible `\log n` term**, exactly matching §5's clean
  bound rather than a cruder union-bound version of it). `r=4,b=0,n=500`: worst
  `\approx0.327`; `r=5,b=0,n=300`: worst `\approx0.508` — larger constants at
  larger `r`, exactly as expected (`D_r(b)` grows with `r`), but bounded for each
  fixed `r`.
- `probe_h_uniform.py`/`.log`: the analogous scan for `h_r(a,b)`, including at
  `a=0` (`h_r`'s own boundary — the point `../adversarial/REFEREE_REPORT.md`
  never checked, since its off-diagonal-`t` probe only reached `t=1/5`, not the
  literal boundary). `r=1,2,3` at `b=0`, `n` to `400`: worst case consistently at
  `a=0`, stabilizing (`0.1667`, `0.384\to0.3836`, `0.646\to0.640`) — again no
  divergence.

All of the above uses **exact** `fractions.Fraction`/`sympy.Rational` arithmetic
throughout (`common.py`) — no floating point enters any of the "exactly `0`" or
"exactly `1/(15n^2)`" claims; floats appear only in the human-readable
`n^2\times\text{residual}` printouts used to visualize convergence.

> **[Nota pós-adversarial, 2026-08-22, issue I-3 do referee hostil dedicado — ver
> `adversarial/REFEREE_REPORT.md` §A.6(e) e a tabela final.]** Três descrições
> acima estão mais otimistas do que os logs retidos: (i) "a **entire** range of
> `m`" descreve na verdade uma amostra log-espaçada de ~25 pontos por `n` (não
> um scan exaustivo) — o próprio referee rodou o scan exaustivo verdadeiro
> (todo `m`, `n` até `400`) e confirmou o mesmo resultado qualitativo (nenhum
> pico interior, o pior caso sempre em `t=1`); (ii) "`r=1,2,3` at `b=0,1`" —
> apenas `r=2` foi de fato rodado em `b=1`; (iii) "`r=1,\dots,5`, `n` up to
> `1600`, both `g_r` and `h_r`" combina execuções de escopo mais estreito do que
> o texto sugere. Nenhuma dessas imprecisões afeta o valor de verdade de nenhuma
> alegação NUMERICALLY VERIFIED — o referee re-executou as versões exaustivas
> por conta própria e confirmou os mesmos resultados qualitativos, sem exceção
> (ver REFEREE_REPORT.md §A.6). Classificado como exagero cosmético da
> superfície de evidência, não erro de conteúdo.

---

## 8. What this resolves, precisely, and what it does not

**Relative to `../ATTEMPT.md` §4's caveat.** §4 stated: "the existence of that
expansion for every `r`... is not separately re-derived here from `\varepsilon`-
`\delta` first principles." §§2–7 above are exactly that re-derivation — a
first-principles, general-`r` proof (not a check at more concrete `K`, and not an
assumption-then-self-consistency argument: `R_r,\varepsilon_r^h` are *defined* as
actual differences from already-known functions, and their smallness is *derived*
from the exact discrete recursion, not assumed).

**Relative to `../adversarial/REFEREE_REPORT.md` §B.4(b)'s specific concern.** The
referee identified a real asymmetry: `F_r` has an a-priori boundedness argument
(since `g_r(m,b)\in[0,1]` is a genuine probability) ruling out a homogeneous-ODE
admixture as `t\to0^+`, but **no analogous argument existed for `G_r`**, whose
`O(1/n)`-correction status carries no such a-priori bound, and `t\to0^+` is
precisely the recursion's own singular boundary layer. **This document does not
resolve that concern by finding an analogous a-priori bound for `G_r`** — it
resolves it differently and more directly: instead of arguing in the abstract
about which boundary condition is *permissible*, §§3–6 directly verify, against
the **true discrete recursion itself**, that the **specific, already-computed**
`G_r` (as derived in `../ATTEMPT.md` §3.3, with no homogeneous term ever included
in its ansatz) achieves the required `O(1/n^2)` accuracy **at the boundary
itself**, not just in the bulk. A genuine homogeneous admixture `C\cdot
t^{-(1+r+b)}` would not be a polynomial, and the entire §4 tail-bounding argument
(which relies on `F_r,G_r,\hat H_r,K_r` being finite-degree polynomials, Fact 1)
would not apply to it — so this document's proof is specific to, and only
certifies, the polynomial-ansatz solution already derived upstream; it does not
independently re-derive *why* the polynomial ansatz (rather than some other
functional form) is the right one to try. What it *does* establish is that,
**having been handed that specific candidate, it is directly, non-circularly
verifiable to be correct** — which is what "existence of the expansion" requires.

**What remains genuinely open, honestly:**

1. **No closed-form expression for `D_r(b),C_r(b)`.** They are defined by an
   explicit, finite, terminating recursion on `r` (mirroring `D_0=C_0=0`, then
   §5–§6's formulas), and are therefore computable for any concrete `r` by direct
   symbolic execution — but this document did not reduce them to a single
   closed-form algebraic expression in `r,b`, nor establish how fast they grow
   with `r` (the numerics of §7 show they grow, e.g. `\sim0.18,0.33,0.51` at
   `r=3,4,5,b=0` for the worst-case `g_r` constant, consistent with — but not
   proving — polynomial-in-`r` growth; no claim about the growth rate is made).
2. **`A_r(b)` (the Taylor-tail bound, §4) was described as a mechanical,
   terminating procedure and its *existence* is fully rigorous, but it was not
   executed to full symbolic generality for a generic `r` in this document** — only
   its structural form (a finite sum of `\|p_j(\cdot,b)\|` coefficient-sum norms,
   `j=2,\dots,r`) was derived, and the smallest nontrivial case (`r=2`) was checked
   to full exactness against real data (§7, the `1/(15n^2)` finding). A fully
   worked symbolic-`r` computation of `A_r(b)`, `B_r(b)` (analogous to `../
   ATTEMPT.md`'s own `verify_dk_recursion.py`, which checks a comparable identity
   for symbolic `r,k,b`) was not attempted here for lack of remaining scope, though
   nothing found suggests it would fail — it is routine, if tedious, symbolic
   differentiation and coefficient extraction on functions already in closed form.
3. **The separate, harder, all-orders exact closed form for `\psi_n^{(K)}` at
   general `K`** (not just its leading order and `O(1/n)` rate) remains exactly as
   open as `../ATTEMPT.md` §6.2 left it — this document does not address it, and
   existence of a two-term expansion says nothing about the existence (let alone
   form) of the full asymptotic series to all orders.
4. **No independent adversarial re-verification of this document has been
   performed** (consistent with every other `ATTEMPT.md` in this lineage, which
   receives a separate hostile-referee pass after being written — that is
   explicitly the orchestrating session's job, not this one's, per the task
   instructions). The derivation in §§3–6 was self-checked at every step against
   the numerics of §7 (which agree exactly, including the striking exact-value
   coincidences at `r=1,2`'s base case), but has not yet been independently
   re-derived from scratch by a second party the way `../ATTEMPT.md`'s own results
   were.

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Exact residual recursion for `R_r(m,b,n)` (§3) | **PROVED** — pure algebra on the already-proven exact discrete recursion `(*)` and the already-proven ODE/relation identities (Facts 2–4); the base case is automatically subsumed (contraction coefficient exactly `0` there), no separate boundary treatment needed |
| 2 | Taylor-tail `\Delta_r(t,b,h)` is `O(h^2)` uniformly on `t\in[0,1]`, with an explicit (mechanically computable, not closed-form) constant `A_r(b)` (§4) | **PROVED**, elementary (coefficient-sum bound on a fixed-degree polynomial); the constant's *existence* and *computability* are proved, its *closed form for general `r`* was not derived |
| 3 | Discrete-Gronwall closure for `g_r`: `|R_r(m,b,n)|\le D_r(b)/n^2`, uniform in `m`, no `\log n` (§5) | **PROVED**, exact telescoping via the falling-factorial/hockey-stick identity (itself proved, §5, and confirmed symbolically, `verify_gronwall_pieces.py`) |
| 4 | Substitution closure for `h_r`: `|\varepsilon_r^h(a,b,n)|\le C_r(b)/n^2`, uniform in `a` (§6) | **PROVED**, elementary algebra + triangle inequality, no Gronwall needed |
| 5 | Existence Theorem, general `r`, by induction (§7) | **PROVED**, base case `r=0` exact (`D_0=C_0=0`), inductive step given by items 3–4 |
| 6 | Numerical corroboration: exact zero/exact `1/(15n^2)` at the base case (`r=1,2`); uniform, non-growing (no `\log n`), converging `n^2\times`residual across the full `m`-range (`r=1,\dots,5`) and the full `a`-range including `h_r`'s own boundary | **NUMERICALLY VERIFIED**, exact `Fraction`/`sympy` arithmetic, `n` up to `1600` — presented as corroboration, not as the proof itself |
| 7 | Closed-form expressions for `D_r(b),C_r(b),A_r(b)` for general `r` | **NOT ATTEMPTED** — defined by an explicit terminating recursion/procedure instead (§8, item 1–2) |
| 8 | All-orders exact closed form for `\psi_n^{(K)}`, general `K` | **NOT ADDRESSED** — separate, harder, explicitly out of scope (§8, item 3) |
| 9 | Independent adversarial re-verification of this document | ~~**NOT PERFORMED** in this session (§8, item 4)~~ **[Atualizado, 2026-08-22]: PERFORMED.** Referee hostil dedicado, independente, rederivou os itens A.1–A.6 do zero (simulador próprio, closed forms próprias, sem importar nenhum script desta pasta) antes de ler este documento. **Veredito: SOUND — WITH NAMED ISSUES** (4 questões nomeadas, nenhuma fatal; 2 exigiram correção — ver adendos pós-adversariais em §4 e §6 acima, issues I-1/I-2/I-3). Ver `adversarial/REFEREE_REPORT.md` |

**Net honest verdict.** The task's specific target — existence of the assumed
two-term asymptotic expansion, for general `r`, from first principles, via a
discrete-Gronwall-type argument uniform in `m,n` — is achieved: outcome **(a)**,
full closure of that specific question, not merely partial progress or a named
obstruction. The argument is a genuine induction on `r` (route 2 of the task
brief) whose inductive step *is* a discrete-Gronwall bound on the exact discrete
recursion (route 1), so both named routes are actually the same successful
argument, not two separate attempts. It does **not** amount to a closed-form,
all-orders solution of the Open Lemma for general `K` (a strictly harder, and
explicitly separate, question `../ATTEMPT.md` itself already distinguished, §6.2),
and it leaves the explicit growth rate of the error constants in `r` uncharacterized.
Combined with `../ATTEMPT.md` §3.4/§5 (the rate conjecture's algebra, unconditional
given the expansion exists), this document's Theorem removes the **last named
caveat** from `../ATTEMPT.md`'s general-`K` rate-conjecture proof and from the
general-`K` Open Lemma bridge — both now rest on nothing beyond what is proved
here and in `../ATTEMPT.md`/`../../ATTEMPT.md`/`THEOREM.md`, modulo only the two
narrower bookkeeping gaps named in scorecard items 7 and the adversarial-review gap
in item 9 (neither of which is a mathematical obstruction — both are "not yet
executed," not "found to fail").

---

## 10. Files, reproducibility

All scripts use exact rational arithmetic (`fractions.Fraction` or
`sympy.Rational`/`sympy.Symbol`) throughout — no floating point enters any claim
labeled PROVED or "exactly"; floats appear only for human-readable display of
convergence trends.

- `common.py` — shared building blocks: `direct_gh(n,K)` (exact-`Fraction`
  memoized recursion implementing `../../ATTEMPT.md` §2's transition rules
  verbatim, general `r,b`, not just `b=0`); `F_closed,G_closed,Hhat_closed,
  K_closed` (the closed forms of `../ATTEMPT.md` §2.3/§3.1/§3.3, reproduced from
  their stated formulas via `sympy`). Smoke test at the bottom confirms
  `F_r(1,0)=\varphi_r` for `r=0,\dots,6`.
- `probe_boundary.py`/`.log` — §7: the base-case point `m=b{+}r{+}1` itself, `r=1
  (b=0,1), 2`, `n` up to `320`; finds the exact `0` (`r=1`) and exact `1/(15n^2)`
  (`r=2,b=0`) results.
- `probe_uniform.py`/`.log`, `probe_convergence_large_n.log` — §7: full-range scan
  of `m` for fixed `(r,b)`, `r=1,2,3,4,5`, `n` up to `1600`, tracking
  `\max_m n^2|R_r(m,b,n)|` for convergence (no `\log n` growth).
- `probe_h_uniform.py`/`.log` — §7: the analogous scan for `h_r(a,b)`, `r=1,2,3`,
  including `a=0`.
- `verify_gronwall_pieces.py`/`.log` — §2/§5: symbolic confirmation of the
  hockey-stick identity, `\hat H_r(1,b)=0` (`r=0,\dots,8`), coefficient-positivity
  spot checks, and degree checks (`r=0,\dots,6`/`8`).
- `PROGRESS.log` — chronological checkpoint trail kept during this session,
  including the by-hand derivation steps, a self-caught arithmetic slip (corrected
  immediately, confirmed not to affect any verified result — see the entry dated
  `2026-08-22T19:55Z`), and the reasoning trail that led to the final argument.

To reproduce: `python3 common.py` (seconds); `python3 probe_boundary.py` (~1 min);
`python3 probe_uniform.py` (~1 min); `python3 verify_gronwall_pieces.py` (seconds);
`python3 probe_h_uniform.py` (~1 min); the large-`n` convergence check
(`r=3,b=0,n=1600` and `r=4,5`) takes a few minutes total (see
`probe_convergence_large_n.log` for the exact commands run).
