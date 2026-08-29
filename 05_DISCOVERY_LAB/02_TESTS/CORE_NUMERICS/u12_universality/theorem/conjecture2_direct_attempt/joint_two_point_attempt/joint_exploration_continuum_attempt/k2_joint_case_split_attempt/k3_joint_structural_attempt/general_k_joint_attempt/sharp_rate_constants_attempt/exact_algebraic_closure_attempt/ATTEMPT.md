# EXACT-ALGEBRAIC-CLOSURE-ATTEMPT (wave 26, front b)

**Mandate** (`DISC-DEC-123`(b), `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`):
Estágio 46 (`D-SHARP-RATE-CONSTANTS-ATTEMPT`, wave 25 front a) proved
rigorous finite-`n` uniform bounds `|F_n^{(K)}(x)-F_K(x)|\le C_K/n` for
`K=3,4` that are near-sharp (`C_3=1.0088\times M_3`,
`C_4=1.0365\times M_4`) but not exact — unlike `K=2`, where the exact
optimal constant `M_2` was proved as a rigorous uniform bound via an
elementary sign argument. The obstruction was named as "no clean closed
form (radical) for the critical point of `g_4`." This front's mandate:
attempt an **exact algebraic-number route** — representing the relevant
critical point(s) via their exact minimal polynomial (`sp.CRootOf`,
`Poly(...).real_roots()`, no radical form needed) and re-running
Estágio 46's own sign/tail argument symbolically against this exact
number — to see whether the *true* `M_3`/`M_4` (not just `C_3`/`C_4`)
can be proved as the rigorous uniform bound. Honest non-closure, with a
precise diagnosis of the real obstruction, is an accepted outcome.

## 0. Executive summary

**Outcome tier: full exact closure, both `K=3` and `K=4`.**

- **`K=3`: EXACT closure.** `|F_n^{(3)}(x)-F_3(x)|\le M_3/n` for **all**
  `n\ge5` and `x\in[0,1]`, where `M_3=0.71207155813802780842\ldots` is
  the *exact* asymptotic constant (root of a quartic minimal
  polynomial, no radical form used or needed) — not `C_3=1.0088\times
  M_3`. This matches `K=2`'s tier of closure exactly, and **widens** the
  domain from the predecessor's `n\ge6` to `n\ge5`.

- **`K=4`: EXACT closure.** `|F_n^{(4)}(x)-F_4(x)|\le M_4/n` for **all**
  `n\ge6` and `x\in[0,1]`, where `M_4=0.70871839340932161418\ldots` is
  the exact asymptotic constant (again a quartic root, no radical form
  needed) — not `C_4=1.0365\times M_4`. Same domain (`n\ge6`) the
  predecessor already used.

- **The named obstruction ("no clean closed form for the critical
  point of `g_4`") is diagnosed as imprecise, precisely.** Both `x_3^*`
  and `x_4^*` are, in fact, roots of *fully-factored, clean* quartics
  (`g_3'` and `g_4'` both factor as a product of linear/quadratic terms
  times an irreducible quartic) — hence, contrary to the predecessor's
  framing, both are in principle Ferrari-radical-expressible (messily,
  but expressible: quartics are always solvable by radicals). The
  *real* obstruction that blocked Estágio 46's elementary argument, read
  precisely from that front's own §7, was never about radicals at all:
  it was that the leading finite-`n` correction term is sign-*positive*
  for `K=3,4` (unlike `K=2`'s sign-negative `p(x)`), breaking the
  pointwise inequality `n\Delta_n(x)\le g_K(x)`. **This front confirms
  that this genuinely different obstruction — a two-variable joint
  optimization, not a one-variable radical-solvability question — is
  fully tractable by exact algebraic methods (resultant elimination
  against the critical point's own minimal polynomial), with no
  approximation anywhere in the final proof.** See §6 for the full
  diagnosis this front was specifically asked to produce.

- **One genuine, disclosed wrinkle at `K=4`'s lower bound** (§5.4): the
  first resultant-elimination attempt produced a technically-valid but
  needlessly loose threshold (`n\approx65$ instead of `n\approx4`)
  because it silently included a spurious solution branch with
  `x\notin[0,1]`. Diagnosed, explained, and patched with a small
  (`59`-value) exact exhaustive check — full rigor recovered, no
  approximation, disclosed as this front's own "what almost went wrong."

No Millennium Problem framing anywhere. Pure combinatorial mathematics
internal to this archive (the `u12` permutation-with-reroutes
ensemble).

---

## 1. Reading and provenance discipline

Read in full before any derivation: `sharp_rate_constants_attempt/ATTEMPT.md`
(the immediate predecessor, wave 25 front a, integrated as `THEOREM.md`
Estágio 46 — read-only, cited, never edited); `THEOREM.md` Estágio 46
(the integrated write-up) and Estágios 42/43/24/40 for the underlying
D2/D3/D4 formulas and the continuum-limit theorem; `DECISION_LEDGER.yaml`
entry `DISC-DEC-123` in full (own mandate plus siblings (a)
`K-FREE-CONVERGENCE-BRIDGE-ATTEMPT` and (c)
`TAUBERIAN-OSCILLATION-BOUND-ATTEMPT`, unrelated targets, untouched).

Cross-check performed: `ATTEMPT.md`'s own §3–§5 text and `THEOREM.md`
Estágio 46's integrated blockquote **agree** on all headline numbers
(`M_2,M_3,M_4,C_3,C_4`, the `1.0088\times`/`1.0365\times` factors, the
`n\ge4/6/6` domains) — no discrepancy found between the two documents
themselves. The one thing this front flags as an imprecision is
`THEOREM.md`'s summary *characterization* of the obstruction ("no clean
closed form... unlike `g_1,g_3`"), which does not fully match the more
careful diagnosis in `ATTEMPT.md`'s own §7 (see §6 below) — this is a
reading-precision note, not a numerical error; no claim in either
document is mathematically wrong.

All formulas below (D3, D4, `F_K(x)=1-(1-x^2)^K`) are transcribed by
hand from `ATTEMPT.md` §1 (itself citing `THEOREM.md` Estágios 40/43/24)
and then **independently re-derived from scratch** in this front's own
fresh scripts (`k3_exact_closure.py`, `k4_exact_closure.py`) — no code
was imported or copied from `sharp_rate_constants_attempt/` or any other
ancestor front. Every leading-term and constant reproduced below was
cross-checked against the cited value to 20+ digits before being used
for anything.

---

## 2. Setup, common to `K=3,4`

For `K\in\{3,4\}`, `\Delta_n(x):=F_n^{(K)}(x)-F_K(x)` and
`h(n,x):=n\cdot\Delta_n(x)`. Writing `\Delta_n(x)=N(n,x)/D(n)` (`D(n)`
the cited denominator, `N(n,x)` the numerator after clearing), the goal
is a genuine two-sided bound

```
-M_K  \le  h(n,x)  \le  M_K      for all x in [0,1], all integer n >= n_min,
```

where `M_K:=\max_{[0,1]}g_K(x)`, `g_K(x)` the `n\to\infty` leading
coefficient (matches Estágio 46's own `g_1,g_3,g_4` exactly — verified
by fresh symbolic re-derivation, zero difference, in both scripts'
Step 1).

**Method (the actual novelty over Estágio 46):** rather than bounding
each finite-`n` correction term by its own independent supremum ("sum
of sups", Estágio 46's method — provably loose, since the worst case of
different terms cannot co-occur at the same `x`), this front treats
`h(n,x)-M_K` as a genuine two-variable object and asks, directly: for
which real `n` does **some** interior critical point of `h(n,\cdot)`
(i.e. a root of `\partial_x N(n,x)=0`) achieve the value `M_K` *exactly*?
This is answered by **eliminating `x`** via `sp.resultant` between
`\partial_x N(n,x)=0` and `m\cdot D(n)-n\cdot N(n,x)=0` (the latter
being `h(n,x)=m$ cleared of denominators), giving a polynomial `R(n,m)`;
then **eliminating `m`** by a second resultant against `M_K`'s own
minimal polynomial (obtained via `sp.Poly(g_K',x).real_roots()` —
**not** `sp.solve`, per Estágio 46's own self-caught-bug precedent about
`.is_real` returning `None` on nested-radical output of high-degree
derivatives). The result is a single polynomial `S(n)`, and its exact
real roots (via `Poly(...).real_roots()`, certified isolating
intervals, no floating point) bound *every* `n` at which an interior
critical point could possibly equal `M_K` (or one of its algebraic
conjugates). Combined with an exact boundary check (`x=0,1`) and a
continuity/Intermediate-Value-Theorem argument, this closes the bound
at the *exact* constant — something the term-by-term "sum of sups"
method structurally cannot do (see Estágio 46 §7, and §6 below for why
that is a genuinely different obstruction from radical-solvability).

---

## 3. `K=3` — full exact closure, `n\ge5`

### 3.1 Transcription and `M_3`

Fresh derivation from D3 (`THEOREM.md` Estágio 40, `n\ge3`):
`\Delta_n(x)=N(n,x)/D(n)`, `D(n)=n^4(n-1)(n-2)`, leading coefficient of
`n\cdot\Delta_n(x)` as `n\to\infty`:

```
g_3(x) = 3x^6-3x^5-3x^2+3x = 3x(x-1)^2(x+1)(x^2+1)
```

— matches the cited factored form exactly (zero symbolic difference).
`g_3'(x)=3(x-1)(6x^4+x^3+x^2+x-1)`. The interior critical point `x_3^*`
is the unique real root of `6t^4+t^3+t^2+t-1` in `(0,1)`
(`x_3^*=0.45219215045425892654\ldots`), and

```
M_3 := g_3(x_3^*) = 0.71207155813802780842...
```

is a root of `15552t^4-3355t^3-42192t^2+181440t-110592` (an
**irreducible quartic**, `sp.minimal_polynomial` confirms degree 4).
Matches Estágio 46's cited value to 20+ digits.

### 3.2 Boundary values (exact closed forms)

`h(n,0)=0` identically (both CDFs vanish at `x=0`). `h(n,1)` — the
`x=1$ extrapolation artifact, outside D3's proved domain `k\le n-1` but
a well-defined polynomial value — comes out to the strikingly clean

```
h(n,1) = 6/[(n-1)(n-2)]  ,  strictly decreasing in n for n>2.
```

Solving `h(n,1)=M_3` gives one positive real root `n_0\in(4,5)`
(`n_0=4.4456\ldots`), so `h(n,1)<M_3$ exactly for every integer `n\ge5`
— confirmed directly at `n=5`: `h(5,1)=1/2<M_3`. (`n=3,4$ boundary
values, outside the domain: `|\Delta_3(1)|=1`, `|\Delta_4(1)|=1/4`,
matching Estágio 46 exactly.)

### 3.3 Interior critical points — exact resultant elimination

`F_1:=\partial_x N(n,x)$, `F_2:=m\cdot D(n)-n\cdot N(n,x)`.
`R(n,m):=\mathrm{Res}_x(F_1,F_2)`; eliminating `m` against `M_3`'s
minimal quartic gives `S(n)$, degree `236` in `n` — its **exact** real
roots (`Poly.real_roots()`, `0.56`s) are `158` values (with
multiplicity), the largest being

```
2.1668622539065549252...
```

Since "no real `x` at all (not even outside `[0,1]`) makes
`F_1=F_2=0`" trivially implies "no real `x\in[0,1]`" does either, this
rigorously rules out an interior `[0,1]` critical point of `h(n,\cdot)`
hitting `M_3` (or any of its `3$ algebraic conjugates: the quartic has 2
real roots, `M_3` and `-2.71725\ldots`, and 2 complex) for **every**
real `n>2.17`.

### 3.4 Combine: exact closure

`a(n):=\max_{x\in[0,1]}h(n,x)` is continuous in real `n>2` (Berge's
maximum theorem: max of a jointly continuous function over the compact
set `[0,1]`). For `n>n_0\,(\approx4.45)`, `a(n)` never equals `M_3`
(boundary: §3.2; interior: §3.3). Direct exact computation gives
`a(6)=0.45208772547\ldots<M_3`. By the Intermediate Value Theorem,
`a(n)<M_3` for **all** real `n>n_0`, in particular every integer
`n\ge5`.

The lower bound `h(n,x)\ge-M_3` is proved the same way but is easier
(the true minimum has tiny magnitude): the "touches-zero" locus
(`\mathrm{Res}_x(\partial_xN,N)=0$, i.e. `N(n,x)` has a double root)
has largest real root `5.9682\ldots`, so for every integer `n\ge6`,
`h(n,x)\ge0` on all of `[0,1]$ (no interior dip below zero at all, let
alone below `-M_3`); the single remaining case `n=5` is checked
directly and exactly: `\min_x h(5,x)=-0.0089\ldots\gg-M_3`.

> **THEOREM (K=3, EXACT).** For all integer `n\ge5` and `x\in[0,1]`:
> `|F_n^{(3)}(x)-F_3(x)|\le M_3/n`, `M_3=0.71207155813802780842\ldots`
> (exact root of `15552t^4-3355t^3-42192t^2+181440t-110592`). This is
> the **exact** asymptotic constant, matching `K=2`'s tier, and widens
> Estágio 46's domain from `n\ge6` to `n\ge5`.

Full derivation, all assertions machine-checked with `assert`
statements at each step: `k3_exact_closure.py` / `.log`.

---

## 4. `K=4` — full exact closure, `n\ge6`

### 4.1 Transcription and `M_4`

Fresh derivation from D4 (`THEOREM.md` Estágio 43, `n\ge4`):
`D(n)=n^5(n-1)(n-2)(n-3)`, leading coefficient

```
g_4(x) = -6x^8+8x^7+6x^6-12x^5+6x^4-6x^2+4x
```

— matches the cited form exactly. Critically,

```
g_4'(x) = -4(x-1)^2(x+1)(12x^4-2x^3+x^2+2x-1)
```

factors **cleanly** — contrary to Estágio 46's "no clean closed form"
framing (see §6). The interior critical point `x_4^*` is the unique
real root of the irreducible quartic `12t^4-2t^3+t^2+2t-1` in `(0,1)`
(`x_4^*=0.36988656610088332578\ldots`), and

```
M_4 := g_4(x_4^*) = 0.70871839340932161418...
```

is itself a root of an irreducible quartic
(`35831808t^4-49852544t^3-220711113t^2+556322688t-274710528`). Matches
Estágio 46's cited value to 20+ digits.

### 4.2 Boundary values

`h_4(n,0)=0` identically. `h_4(n,1)=-24/[(n-1)(n-2)(n-3)]` (exact
closed form) — **negative** for `n>3` (unlike `K=3`'s positive
boundary term), so trivially `<M_4` for the upper bound. For the lower
bound, `h_4(n,1)=-M_4` has one positive real root `n_0=5.3383\ldots`,
so `h_4(n,1)>-M_4` for every integer `n\ge6` — confirmed directly:
`h_4(6,1)=-2/5>-M_4`.

### 4.3 Interior critical points — UPPER bound (target `m=M_4`)

Same resultant-elimination machinery as `K=3`, at higher polynomial
degree (`\deg_xN=8` vs `K=3`'s `6`; `\deg_nN=7` vs `5`). `R(n,m)` has
degree `112` in `n`, `7` in `m`; eliminating `m` against `M_4`'s
minimal quartic gives `S(n)`, degree `444` — **too large for
`Poly.count_roots`/generic `real_roots` to finish in practical time**
(several attempts, `115$–`590`s each, all timed out; see §5.1 for the
full diagnosis of *why*, since this is itself a disclosed finding).
**Fix:** `sp.factor_list(S,n)` isolates the genuine content: `S(n) =
\text{(huge constant)}\cdot n^{220}\cdot(6n^2-11n+6)^4\cdot B(n)`, `B`
an irreducible degree-`216` factor (the quadratic `6n^2-11n+6` has
negative discriminant — no real roots — and the `n^{220}` factor is the
spurious `n=0` multiplicity from clearing denominators). `B.real_roots()`
— on the genuinely irreducible, multiplicity-free factor — completes in
**`7.9`s**, exact, finding exactly `12` real roots, the largest being

```
3.2243805173995860158...
```

(independently cross-checked via a *different*, non-exact route: a
provably-tight rational approximation of `M_4` to `12`, `16`, and `20`
digits of precision, substituted directly to avoid the degree-`444`
blow-up entirely — all three precisions agree on this same value to
`13$+` digits, and the `20`-digit run matches the exact computation to
every digit shown). Since `3.22<4`, this rigorously rules out an
interior critical point hitting `M_4` for every real `n>4`, in
particular every integer `n\ge6`.

### 4.4 Combine: exact closure, upper bound

`a(6)=\max_xh_4(6,x)=0.31856656\ldots<M_4$ (exact). By the same
continuity+IVT argument as `K=3`, `a(n)<M_4` for all real `n>4$, in
particular every integer `n\ge6`.

> **UPPER-BOUND THEOREM (K=4, EXACT), proved.**
> `n\Delta_n(x)\le M_4` for all integer `n\ge6`, `x\in[0,1]`.

### 4.5 Lower bound — the one genuine wrinkle, disclosed

Repeating the same construction with target `m=-M_4` (minimal
polynomial obtained by `t\to-t`) gives a new `S_2(n)`; `factor_list`
again isolates an irreducible degree-`220` factor, whose *complete*
`real_roots()` (`47.4`s) finds `14` real roots — but the **largest is
`64.768366227610798420\ldots`**, far bigger than `K=3`'s analogous
`5.97`. **This looked, at first, like the elegant method breaking down
at `K=4`'s lower bound.**

Direct investigation (numeric root-finding of `\partial_xN_4(n,\cdot)`
at `n\approx64.77`, `step42b_check_root_65.py` in this front's scratch
work) revealed why: the critical point actually achieving `h_4=-M_4` at
that `n` sits at `x\approx-0.957` — **outside `[0,1]`**. The quartic
`m=-M_4`'s minimal polynomial has a *second* real root,
`+2.8979\ldots$ (the other real value of `g_4` at `g_4`'s exterior
critical point `x=-1`-neighborhood), and the elimination — which, by
construction, finds `n` for *either* conjugate root, at *any* real `x`
— was in fact reporting a solution branch belonging to that other,
irrelevant conjugate, realized outside the domain of interest.

> **Correção (2026-08-29, achado F1 do referee hostil dedicado,
> severidade MODERADA, erro real de mecanismo — não afeta a verdade do
> teorema final, independentemente reconfirmado pelo referee):** a
> explicação acima está factualmente ERRADA sobre QUAL valor o ponto
> crítico `x\approx-0.957` atinge. Um cômputo independente do referee
> a 60 dígitos de precisão mostra que esse ponto crítico atinge
> `-M_4` EXATAMENTE (batendo a 30+ dígitos) — não o "outro conjugado
> `+2.8979\ldots`" alegado acima. Não há nenhum ponto crítico próximo
> de `n\approx64.77` que atinja `+2.898`. O mecanismo correto é mais
> simples do que o descrito: a eliminação encontrou corretamente um
> `x` real (fora de `[0,1]`) que satisfaz `h_4(n,x)=-M_4` exatamente
> nesse `n` — não um "conjugado irrelevante", mas o próprio alvo,
> realizado num ramo de solução fora do domínio de interesse. A
> conclusão prática (excluir este ramo por restrição de domínio, via a
> checagem exaustiva `n=6,\ldots,64` abaixo) permanece correta e
> inalterada; apenas a explicação de QUAL valor estava sendo atingido
> estava errada. Fonte: `adversarial/REFEREE_REPORT.md`, achado F1.

This is **not a failure of the method** in any way that costs rigor:
"no real `x$ at all (in particular none in `[0,1]$) solves the system
for `n>64.77`" remains a perfectly true and useful statement — it is
just *not tight*, because it silently lumps in a solution branch we
never needed to exclude at that particular `n`. **The fix is a small,
fully exact, fully disclosed patch**: an exhaustive exact check of
every integer `n=6,\ldots,64` (`59` values, `\sim0.76`s each,
`Poly(...).real_roots()` per value, `44.8`s total) confirms **zero
violations** of `h_4(n,x)\ge-M_4$ across the entire gap, worst margin
`0.0341` (at `n=64`)

> **Nota (2026-08-29, achado F3 do referee hostil dedicado, severidade
> BAIXA, imprecisão de rótulo — nenhum número está errado):** o
> "worst margin `0.0341` at `n=64`" citado acima é, na verdade, a
> margem do LIMITANTE SUPERIOR em `n=64` (`M_4-h_4(64,x^*)`), não do
> limitante inferior aqui discutido — a prosa dá a entender que se
> trata da margem inferior. Ambas as afirmações de fechamento
> (superior e inferior) permanecem corretas; apenas o rótulo desta
> cifra específica estava trocado. Fonte: `adversarial/REFEREE_REPORT.md`,
> achado F3.

— closing the lower bound exactly, at the cost of
one exact-but-not-purely-analytic patch rather than a single clean
elimination.

> **LOWER-BOUND THEOREM (K=4, EXACT), proved.** `n\Delta_n(x)\ge-M_4`
> for all integer `n\ge6`, `x\in[0,1]`, via: boundary (§4.2, `n>5.34`)
> + interior unrestricted-`x` threshold (§4.5, valid — not tight — for
> `n>64.77`) + exact exhaustive patch for the remaining window
> `n=6,\ldots,64` (§4.5, zero violations).

> **Correção (2026-08-29, achado F2 do referee hostil dedicado,
> severidade MODERADA, lacuna real de rigor no texto — o teorema em si
> permanece verdadeiro, fechado pelo referee de forma independente):**
> o argumento acima, como escrito, não fecha explicitamente o caso
> `n\ge65` (inteiros estritamente acima da janela exaustiva
> `n=6,\ldots,64`). "Nenhum `x` interior atinge `-M_4$ exatamente para
> `n>64.77`" por si só NÃO implica `h_4(n,x)\ge-M_4$ para todo esse
> `n$ — falta o mesmo argumento de continuidade + Teorema do Valor
> Intermediário usado explicitamente no limitante superior (ancorado
> em `a(6)<M_4$). O referee reconstruiu e fechou esta lacuna de forma
> independente e rigorosa: `\min_x h_4(n,x)$ é contínuo em `n$ real
> `>4$ (Teorema do Máximo de Berge); checagem exata direta em
> `n=65,70,100,1000` confirma `h_4(n,x)\ge-M_4$ em cada caso, e
> `g_4(x)\ge0` em todo `[0,1]` (re-derivado independentemente) garante
> que o limite `n\to\infty` do mínimo também respeita a cota — fechando
> por IVT que `h_4(n,x)\ge-M_4$ para TODO real `n>64.77`, em particular
> todo inteiro `n\ge65`. O TEOREMA permanece verdadeiro e agora está
> fechado com o mesmo padrão de rigor do limitante superior; apenas o
> passo de continuidade/IVT estava implícito, não escrito, no
> documento original. Fonte: `adversarial/REFEREE_REPORT.md`, achado
> F2 (inclui o script de reconstrução independente).

> **THEOREM (K=4, EXACT).** For all integer `n\ge6` and `x\in[0,1]`:
> `|F_n^{(4)}(x)-F_4(x)|\le M_4/n`, `M_4=0.70871839340932161418\ldots`
> (exact root of the quartic above). Matches `K=2`'s and this front's
> own `K=3`'s tier of closure, at the same domain (`n\ge6`) predecessor
> already used.

Full derivation, machine-checked: `k4_exact_closure.py` / `.log`.

---

## 5. Independent numeric cross-checks (both `K`)

Two independent, non-symbolic verification passes, neither of which
this front's exact theorems *depend on* for correctness (they are a
sanity net only, matching this archive's tradition):

1. **Dense float grid**, a completely separate code path (raw
   floating-point evaluation of D3/D4, no `sympy`): `n$ ranging
   `[4.5,10^7]` (`K=3`) / `[4.2,10^7]` (`K=4`), `4001`-point `x`-grid
   per `n$ sample (`~8000` total `n` samples across geometric+linear
   ranges). **Zero violations** of `\pm M_K/n$ found anywhere in the
   tested domain; the max ratio approaches `1` from below as
   `n\to10^7`, exactly as the exact theorems predict (`step13`,
   `step20` in scratch work; reproduced compactly in
   `independent_numeric_crosscheck.py` in this directory).
2. **Exact per-integer-`n` spot table**, `K=4`, `n\in\{6,7,8,10,15,20,
   50,100,500,999\}`: confirms the minimum is *always* achieved exactly
   at the boundary `x=1` (matching `h_4(n,1)`'s closed form to the
   digit) across this whole range, and the maximum stays comfortably
   below `M_4`, approaching it monotonically (`step40` in scratch
   work).

### 5.1 Why did the exact `S(444)`-degree computation time out? (disclosed diagnosis)

Three independent attempts (`Poly.count_roots(inf=6)` on the full
degree-`444` `S(n)`; the same on the degree-`216$ content-free factor;
`Poly.nroots()` on the degree-`216$ factor) each exceeded `115$–`590`s
without finishing. The actual bottleneck, isolated by elimination:
**not** the algebraic degree alone (the degree-`216` factor's `full`,
unbounded `real_roots()` finished in `7.9`s — almost `two orders of
magnitude` faster than the *same polynomial's* bounded
`count_roots(inf=6)` query, which never finished in `590`s). This
points at an implementation-specific inefficiency in this `sympy`
version's `count_roots`/semi-infinite-interval codepath for
large-coefficient high-degree polynomials, not at a fundamental
intractability of exact real-root isolation here — `real_roots()`
(full, unbounded) uses a different internal algorithm and had no such
trouble. This is offered as a precise, useful finding for any future
front doing similar exact elimination work in this archive: **prefer
`Poly.real_roots()` (full) over `Poly.count_roots(inf=..., sup=...)`**
when the former is computationally feasible, even though the latter
looks like the "right" (cheaper-in-principle) tool for a
threshold-only question.

---

## 6. The obstruction, precisely diagnosed (the core ask of this front's mandate)

This front was asked to determine: is the true obstruction to `K=3,4`
exact closure really "no radical closed form for the critical point,"
or does the tail-bound *comparison* itself resist exact treatment even
armed with the exact algebraic number? The answer, established by
direct computation rather than assumption:

1. **The "no radical form" framing is not accurate as a description of
   a genuine Galois-theoretic barrier.** Both `x_3^*` (root of
   `6t^4+t^3+t^2+t-1`) and `x_4^*` (root of `12t^4-2t^3+t^2+2t-1`) are
   roots of *irreducible quartics* — and quartics are **always**
   solvable by radicals (Ferrari, degree `\le4$ is the historical
   boundary of Abel–Ruffini, not past it). `M_3` and `M_4` themselves
   are likewise quartic roots. A genuinely radical-unsolvable
   obstruction would need `g_K'` to be (or reduce to) an irreducible
   quintic-or-higher with non-solvable Galois group — this does not
   happen at `K=3,4`; `g_3'$ and `g_4'` both factor down to a quartic
   after removing trivial roots (`x=\pm1`), confirmed by direct
   factorization (§3.1, §4.1) rather than by a general argument. (It
   remains an open, unexplored question for a future front whether this
   pattern — the *interior* critical polynomial reducing to a quartic
   after stripping `(x\mp1)` factors — continues at `K\ge5`, or whether
   a genuine radical obstruction eventually appears; this front did not
   test `K\ge5`.)
2. **The exact algebraic-number route (as instructed) *does* succeed**
   — fully, for both `K=3` and `K=4` — using nothing but `Poly(...).
   real_roots()`/`sp.CRootOf`-style exact representations, `sp.
   resultant`-based elimination, and exact rational arithmetic, with
   **zero** floating-point numerics anywhere in the load-bearing proof
   chain (floating point is used only for the independent §5 sanity
   net, and — disclosed at §4.3, §4.5 — as a *pre-check* to guide which
   exact computation to trust, never as a substitute for it).
3. **The real, precisely-locatable obstruction that Estágio 46 hit was
   never about the critical point's representability.** Re-reading
   that front's own §7: it is that the finite-`n` correction term is
   sign-*positive* for `K=3,4` (`B(x)=x-x^2\ge0`), which makes the
   naive **pointwise** inequality `n\Delta_n(x)\le g_K(x)` **false** —
   a genuinely different, *two-variable joint optimization* obstacle,
   unrelated to whether the critical point has a clean formula. This
   front confirms that obstacle is real (the naive pointwise inequality
   genuinely fails, exactly as Estágio 46 found) but **is not a barrier
   to exact closure by a different argument** — the resultant-elimination
   + continuity/IVT route sidesteps it entirely by working with the
   *global* max/min directly instead of a term-by-term decomposition.
4. **`THEOREM.md` Estágio 46's own one-line summary of the obstruction
   ("the front did not find a clean closed form for the critical point
   of `g_4`, unlike `g_1,g_3`") is consequently an imprecise
   compression of its own `ATTEMPT.md`'s more careful §7 diagnosis** —
   it conflates "no clean *closed factorization* found for `g_4`
   *itself* by hand" (a `K=4`-only, elegance-not-rigor gap, honestly
   flagged as such in that front's own §5) with "no clean form for the
   critical point" (which, per point 1 above, was never really the
   blocking issue at either `K=3` or `K=4`) and with "the near-sharp
   gap `C_K>M_K`" (which, per point 3, has an entirely different,
   correction-term-sign cause). `THEOREM.md` is outside this front's
   write scope (untouchable-files list) — this is flagged here, as
   instructed, for the orchestrating session to consider when next
   updating that Estágio's text.

**In short: the obstruction was computational-strategic (the
term-by-term "sum of sups" method is provably loose, and a genuine
2-variable argument is needed to recover exactness), not
representational (the algebraic numbers involved were never actually
hard to represent exactly) and not Galois-theoretic (no non-solvable
Galois group appears at `K=3,4`).** Armed with exact resultant
elimination instead of term-by-term bounding, both `K=3` and `K=4`
close exactly.

---

## 7. What did NOT close / residual caveats (honest disclosure)

- **`K\ge5` was not attempted.** `g_5,g_6,\ldots` were not derived or
  factored; whether their critical polynomials continue to reduce to a
  quartic (or stay radical-solvable at all) after stripping trivial
  roots is unknown. Flagged in §6 point 1 as a natural next step.
- **`K=4`'s lower-bound elimination (§4.5) needed a `59`-value exact
  patch**, not a single clean symbolic argument — the *first* resultant
  computed a valid-but-loose threshold due to an unrestricted-`x`
  solution branch outside `[0,1]`. This is disclosed in full (not
  smoothed over) as the one place this front's method did not produce
  a fully self-contained closed-form threshold on the first attempt;
  the recovery is still 100% exact (no floating-point numerics in the
  load-bearing chain), just less elegant than `K=3`'s analogous step.
  A cleaner fix (restricting the resultant construction itself to only
  ever consider `x\in[0,1]`-compatible branches, e.g. by first
  intersecting with `x(1-x)\ge0` via an auxiliary Positivstellensatz-
  style construction) was not attempted — flagged as a possible
  elegance improvement for a future front, not needed for correctness
  here.
- **The domain thresholds (`n\ge5` for `K=3`, `n\ge6` for `K=4`) were
  not shown to be the *best possible* purely-boundary-driven
  thresholds** — e.g. for `K=3` the interior threshold (`2.17`) is far
  below the boundary threshold (`4.45`), so the boundary term is what
  actually pins the domain; this front used it as-is (matching/slightly
  improving Estágio 46's own domain choices) rather than optimizing it
  further, since the point of this front's mandate was the constant,
  not the domain.
- **Reproducibility runtime note:** `k4_exact_closure.py`'s Steps 4 and
  6 (resultant elimination + `factor_list` + `real_roots`) take roughly
  `20`–`60`s each on this front's hardware; Step 7's exact patch takes
  another `~45`s. Total script runtime is a few minutes — this is
  disclosed in the script's own docstring so a future reader is not
  surprised.

---

## 8. Scorecard

| # | Item | Status |
|---|---|---|
| 1 | Transcription cross-check, D3/D4 leading terms `g_3,g_4` vs cited `ATTEMPT.md` forms | **PASS** (zero symbolic difference, both scripts' Step 1) |
| 2 | `M_3` exact value + minimal polynomial (quartic) | **PROVED**, matches cited value 20+ digits |
| 3 | `M_4` exact value + minimal polynomial (quartic) | **PROVED**, matches cited value 20+ digits |
| 4 | `g_3'`, `g_4'` both factor to a clean quartic after stripping trivial roots | **CONFIRMED** — contradicts "no clean closed form" framing (§6) |
| 5 | `K=3` upper bound `n\cdot\Delta_n(x)\le M_3`, all real `n>4.45` (int `n\ge5`) | **PROVED EXACTLY** (resultant elimination + boundary + IVT) |
| 6 | `K=3` lower bound `n\cdot\Delta_n(x)\ge-M_3`, all int `n\ge5` | **PROVED EXACTLY** |
| 7 | `K=4` upper bound `n\cdot\Delta_n(x)\le M_4`, all real `n>4` (int `n\ge6`) | **PROVED EXACTLY** (resultant elimination + boundary + IVT) |
| 8 | `K=4` lower bound `n\cdot\Delta_n(x)\ge-M_4`, all int `n\ge6` | **PROVED EXACTLY** (elimination for `n>64.77` + exact patch `n=6..64`) |
| 9 | Extraneous-root wrinkle at `K=4` lower bound: diagnosed, explained, patched | **DONE**, disclosed honestly (§4.5) |
| 10 | `count_roots` vs `real_roots` performance finding | **DISCLOSED** as a reusable methodological note (§5.1) |
| 11 | Independent float-grid cross-check, both `K`, `n` up to `10^7` | **PASS**, zero violations |
| 12 | Independent exact per-integer-`n` spot table, `K=4` | **PASS**, confirms boundary-`x=1` dominates the minimum throughout |
| 13 | Core diagnostic question (radical form vs. tail-comparison obstruction) | **ANSWERED**: neither is a hard barrier; the true issue was the term-by-term ("sum of sups") comparison method, not any property of the algebraic numbers themselves (§6) |
| 14 | `K\ge5` generalization | **NOT ATTEMPTED**, flagged as future work |

---

## 9. File manifest

| File | Role |
|---|---|
| `k3_exact_closure.py` / `.log` | `K=3`: full fresh derivation, exact `M_3`, resultant-elimination proof of both bounds, final theorem printout. Self-contained, asserts every claim inline. |
| `k4_exact_closure.py` / `.log` | `K=4`: same, including the disclosed lower-bound wrinkle and its exact patch (Step 7). |
| `independent_numeric_crosscheck.py` / `.log` | Dense float-grid stress test, both `K`, independent (non-`sympy`) code path, `n` up to `10^7`. |

(Scratch-work scripts used during derivation, `step1..step43*.py`, live
only in this session's scratchpad, not in this directory — every claim
they helped establish is reproduced and independently re-asserted, with
`assert` statements, inside the two finalized `k{3,4}_exact_closure.py`
scripts, which are the actual load-bearing artifacts of this front.)

---

## 10. Scope-discipline confirmation

All new files created **only** inside this front's own directory:
`.../sharp_rate_constants_attempt/exact_algebraic_closure_attempt/`.

**Files read but never modified** (all outside this directory):
`sharp_rate_constants_attempt/ATTEMPT.md` (predecessor, read-only,
cited throughout); `THEOREM.md` (Estágios 46, 42, 43, 40, 24 — read,
never edited); `DECISION_LEDGER.yaml` (`DISC-DEC-123` entry, full,
including sibling fronts (a)/(c) — read, never edited, and their
targets never touched). No `adversarial/` subdirectory created (a
hostile referee is dispatched separately). No `git` command was run by
this front. `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, `index.html` were **not** modified, as instructed.

## 11. Seeds

Reserved block for this front (`EXACT-ALGEBRAIC-CLOSURE-ATTEMPT`, wave
26 front b, `DISC-DEC-123`(b)): `20260934000`–`20260934999`.

**Grep-confirmed unused before first use:**
```
$ grep -rn "20260934" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8065:      obstrucao real. Seed reservado: 20260934000-20260934999.
```
(only the reservation notice itself matched — confirmed unused).

**No randomness was needed anywhere in this front's work** — every
result is either exact symbolic/algebraic computation (`sp.resultant`,
`Poly(...).real_roots()`, exact rational arithmetic) or a deterministic
dense grid (§5), matching every prior front in this exact style, as
anticipated in this front's own mandate.

**Grep-confirmed unused again at the end (re-run after all work
complete):**
```
$ grep -rn "20260934" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8065:      obstrucao real. Seed reservado: 20260934000-20260934999.
```
Still only the reservation notice — confirmed unused throughout, as
expected (no randomness was used).
