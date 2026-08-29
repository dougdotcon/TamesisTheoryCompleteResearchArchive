# A general closed form for `W(r,t)`, and a proof of Claim B for all `K`

**Front:** wave 27, front (b), `W-RT-CLOSED-FORM-ATTEMPT`, authorized by
`DISC-DEC-127` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`). Pure
combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1–4, continuing the
distributional-bridge line begun at Estágio 27 and K-freed at Estágio 41.
**This is not a Millennium Prize Problem and no claim of that kind is made
anywhere below.**

Reserved seeds: `20260937000`–`20260937999` (`DISC-DEC-127`, frente (b)).
Grep-confirmed unused before any file in this directory was written, and
re-confirmed after (Section 11) — **in the end no seed was used at all**:
every computation in this front is exact `Fraction`/`sympy` symbolic
arithmetic, no randomness anywhere (the mandate itself flagged this as
likely, and it turned out to be exactly right). No edits made to
`THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`, `README.md`, or `index.html`.
No `adversarial/` subdirectory created here (a hostile referee is
dispatched separately by the orchestrating session). No `git` command run.
Every `.py` file in this directory was written completely fresh for this
front — no script from `k_free_convergence_bridge_attempt/` (the immediate
predecessor, wave 26 front (a)) or any other ancestor/sibling front was
imported or copied; formulas and definitions cited from the predecessor's
`ATTEMPT.md` and `find_W_pattern.py`/`find_W_pattern.log` are transcribed
and cited explicitly, per the mandate.

---

## Executive summary (read first)

**The precise target (mandate, `DISC-DEC-127` frente (b)).** The
predecessor front (`k_free_convergence_bridge_attempt/ATTEMPT.md`, wave 26
front (a)) proved an unconditional, `K`-free coupling theorem (**Theorem
A**) reducing the archive's open convergence-rate question to a single
distributional identity, **Claim B**: `M_K' \overset{d}{=} M_K`, proved
there only at `K=1`, open for `K\ge2`. That front reduced Claim B for
*all* `K,t` simultaneously to two concrete, unexecuted steps: (1) find a
`K`-free closed form for a purely combinatorial weight `W(r,t)`, known
there only at `t=1,2`; (2) check whether the resulting `K`-symbolic sum
`\sum_{r=0}^K\binom Kr W(r,t)/(K+t+r+1)!` closes in `\texttt{sympy}`.

**What this front found.**

> **Result 1 (PROVED).** `W(r,t) = (t+2r+1)\,(t+r)!` for every `r\ge0`,
> `t\ge1` — a complete closed form for **every** `t`, not just `t=1,2`.
> Derived from the exact definition (Section 3.1), not merely
> pattern-matched, and cross-checked exactly against `99` fresh
> computed values (`r=0,\ldots,10`, `t=1,\ldots,9`) plus the predecessor's
> own `32` cited log values.

> **Result 2 (PROVED).** `\displaystyle\sum_{r=0}^K\binom Kr
> \frac{W(r,t)}{(K+t+r+1)!} = \frac{\Gamma(t/2+1)}{\Gamma(K+t/2+1)}` for
> **every** `K\ge0` and **every real** `t>-1` (hence every positive
> integer `t`) — found via elementary calculus (a Beta-integral
> substitution, the binomial theorem, and one integration by parts) after
> the mandate's literally-named method (`\texttt{sympy.summation}` /
> Gosper's algorithm applied directly to the sum) turned out to close only
> for even `t` and to certify genuine non-existence of a hypergeometric
> antidifference for odd or symbolic `t` (Section 4, and the honestly
> disclosed self-caught false lead of Section 4.4). The general closed
> form was instead proved directly (Section 5), independent of any
> summation black box, and cross-checked symbolically (`K=1,\ldots,8`,
> `t` left as a free symbol throughout — not just plugged-in integers)
> plus across `6000` further exact-`\texttt{Fraction}` integer cells and
> `80` exact half-integer-`t` cells.

> **Result 3 (Claim B, PROVED for every `K\ge1`).** Combining Results 1–2
> with the archive's already-proved target moment formula
> `E[M_K^t]=K!\,\Gamma(t/2+1)/\Gamma(K+t/2+1)` (Estágio 24's density,
> re-derived fresh here too, Section 5.5) gives `E[(M_K')^t]=E[M_K^t]` for
> **every** `K\ge1` and **every** positive integer `t`. Since `M_K'` and
> `M_K` are both supported on the compact interval `[0,1]`, matching all
> moments determines the law uniquely (classical moment-determinacy on
> bounded support — cited, not re-derived, Section 6). **Hence
> `M_K'\overset d=M_K` for every `K\ge1`: Claim B is fully proved, not
> merely at `K=1`.**

> **Consequence for the predecessor's Main Theorem.** Predecessor's
> `\sup_x|F_n^{(K)}(x)-F_K(x)|\le8K^2/n` (`k_free_convergence_bridge_
> attempt/ATTEMPT.md` Section 6), stated there **conditional on Claim B**,
> now holds **unconditionally**, for every `K\ge1`, `n\ge K+1` — Theorem
> A's own proof (already unconditional, untouched by this front) combines
> with this front's now-unconditional Claim B exactly as the predecessor's
> Section 6 already assembles them, with no remaining hypothesis. This
> upgrade is stated here as this front's finding; per this front's scope
> discipline (Section 13), no edit to any shared archive file is made —
> integrating this consequence into `THEOREM.md`/the ledger is left to the
> orchestrating session, exactly as the predecessor's own scope discipline
> left Theorem A's consequences to be integrated downstream.

**Net verdict.** **Full closure of the mandate's stated success
criterion**: a general closed form for `W(r,t)` (all `t`) plus the
resulting `K`-symbolic sum closing (found by hand after the literal
`\texttt{sympy}`-summation method partially failed), upgrading Claim B to
an unconditional proof for every `K\ge1`. No claim of progress on any
Millennium Problem anywhere in this document; pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.

---

## 1. Reading discipline and provenance

**Read in full before any derivation.** `05_DISCOVERY_LAB/00_GOVERNANCE/
DECISION_LEDGER.yaml` entry `DISC-DEC-127` in full (this wave's three-front
authorization, including what fronts (a) `H1-U2-BOUNDARY-LAYER-ATTEMPT` and
(c) `GAMMA-GAP1-CANCELLATION-TRACKING-ATTEMPT` of this same wave are doing
— unrelated targets, not touched here). `k_free_convergence_bridge_
attempt/ATTEMPT.md` in full (the immediate predecessor, wave 26 front (a),
`DISC-DEC-123`) — Theorem A's precise statement and proof (Section 4, the
`(\xi,\eta)`-coupling, the sorting lemma, the mismatch-zone bound, all
cited as a black box and not re-derived or re-verified here, per this
front's mandate, which targets Claim B specifically), and Claim B's
precise statement, its `K=1` proof (Section 5.1), its exact-moment
verification table (Section 5.2), and — read with special care, being this
front's exact starting point — Section 5.3 ("Partial structural progress
toward a general proof"), which states the reduction identity
`E[(M_K')^t]=K!\sum_r\binom Kr W(r,t)/(K+t+r+1)!` and the two already-found
closed forms `W(r,1)=2r!(r+1)^2`, `W(r,2)=r!(r+1)(r+2)(2r+3)`.
`k_free_convergence_bridge_attempt/find_W_pattern.py` in full — read to
extract `W(r,t)`'s **exact, precise, computational definition** (the
predecessor's own recipe: expand Proposição S's weight `P(S=A|p)` for
`A=\{0,\ldots,r-1\}`, `K:=r`, into monomials in `(p_0,\ldots,p_{r-1},p_D)`;
expand the conditional `t`-th moment `E[(p_D+\sum_aV_a)^t|p,A]` via the
multinomial theorem; multiply; sum `\text{coeff}\times\prod_i(\text{exps}
[i]!)` over the resulting monomials) — this definition is **transcribed**
below (Section 3.1) as this front's own verified starting point, per the
mandate, but every function computing it was **written fresh**, not
imported (`W_closed_form.py`, this directory; independently cross-checked
against `find_W_pattern.log`'s own `32` printed values, Section 3.2).
`k_free_convergence_bridge_attempt/find_W_pattern.log` read in full (the
predecessor's own `t=1,\ldots,4`, `r=0,\ldots,8` table, used only as a
citation-only cross-check target, never as a computational source).
`k_free_convergence_bridge_attempt/verify_MK_moments.py` read in full for
context on how `E[(M_K')^t]` is computed from Proposição S and the
Dirichlet-moment formula (the same recipe is re-derived and re-verified
independently in Section 4 below, not imported). `THEOREM.md` "Estágio 47"
in full (the integrated version of the predecessor's Theorem A and Claim
B) and "Estágio 41" in full (the K-free Full Cycle-Count Decomposition
Theorem / Proposição S general-`K` — this archive's own precedent for
exactly this kind of "pattern-match a family of exact quantities into one
`K`-free closed form" exercise, used here as a methodological template,
not re-derived: Proposição S's statement, cited as a black box throughout,
is `P(S=A|p)=|A|!\prod_{a\in A}p_a\,(p_D+\sum_{a\in A}p_a)`, exactly as
transcribed in the predecessor's own Section 3 item 2).

**What is cited, not re-derived, and used as a black box throughout:**
Theorem A (predecessor's Section 4, PROVED unconditionally, untouched
here); Proposição S's exact formula (Estágio 41, PROVED, transcribed
above); the reduction identity `E[(M_K')^t]=K!\sum_r\binom Kr
W(r,t)/(K+t+r+1)!` (predecessor's Section 5.3, re-derived and
independently re-verified in Section 4 below — not merely re-cited, since
verifying it independently was part of this front's own due diligence);
the target density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` (Estágio 24, PROVED
unconditionally for every `K\ge1`); the classical Dirichlet-moment formula
`E[\prod_ip_i^{k_i}]=K!\prod_i(k_i!)/(K+\sum_ik_i)!` for `(p_0,\ldots,p_K)
\sim\mathrm{Dirichlet}(1,\ldots,1)` (standard, any probability text);
the classical Beta-integral identity `\int_0^1x^a(1-x)^bdx=a!b!/(a+b+1)!`
for nonnegative integers `a,b` (standard, elementary, used repeatedly in
Section 5); and the classical fact that two probability measures on a
compact interval with identical moments of every positive-integer order
are equal (Stone–Weierstrass argument on `C[0,1]`, standard — cited in
Section 6, not re-derived, matching this archive's convention for such
facts, e.g. the predecessor's own citation of order-statistic spacings
being Dirichlet). **Nothing** from any `K`-fixed closed-form-CDF front, or
from any script in `k_free_convergence_bridge_attempt/`, is imported or
executed by this front — every `.py` file here is fresh.

---

## 2. Setup, restated precisely

All notation follows the predecessor's `ATTEMPT.md` exactly (Sections 2–3
there), restated here only as needed. `M_K'` is the continuum random
variable `M_K':=p_D+\sum_{s\in S}V_s'`, built from `(p_0,\ldots,p_{K-1},
p_D)\sim\mathrm{Dirichlet}(1,\ldots,1)`, `S\subseteq\{0,\ldots,K-1\}`
distributed per Proposição S given `p`, and `V_s'\sim\mathrm{Uniform}
(0,p_s)` independent given `S`. **Claim B**: `M_K'\overset d=M_K`, where
`M_K` has the already-proved density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` on
`[0,1]` (Estágio 24). Predecessor proved Claim B at `K=1` and left it open
for `K\ge2`, reducing it (their Section 5.3) to the combinatorial sequence
`W(r,t)` defined precisely below.

Every claim in this document with `K` unqualified means "for every
`K\ge1`"; `K=0` is trivial and separately noted where relevant (as in the
predecessor's document: `M_n^{(0)}\equiv1\equiv M_0`, no argument needed).

---

## 3. Result 1: a general closed form for `W(r,t)`

### 3.1 The exact definition, transcribed

Per `find_W_pattern.py` (predecessor's own script, read for its precise
recipe, not imported), fix `r\ge0`, `t\ge1`, set `A:=\{0,\ldots,r-1\}` and
treat `r` itself as the dimension parameter (`K:=r`) in Proposição S's
formula and the conditional-moment expansion:

1. **Proposição S's weight**, expanded into monomials in
   `(p_0,\ldots,p_{r-1},p_D)`: `P(S=A|p)=r!\prod_{a\in A}p_a\,(p_D+
   \sum_{a\in A}p_a)`, an `(r+1)`-term sum of monomials of total degree
   `r+1`, each with coefficient `r!`.
2. **The conditional `t`-th moment** `E[(p_D+\sum_{a\in A}V_a)^t|p,A]`,
   `V_a\sim\mathrm{Uniform}(0,p_a)` independent given `A`: multinomial
   expansion using `E[V_a^k|p_a]=p_a^k/(k+1)`, a sum over compositions
   `(k_D,k_0,\ldots,k_{r-1})` of `t` into `r+1` nonnegative parts, of
   monomials of total degree `t` with coefficient `t!/(k_D!\prod_ak_a!)
   \cdot\prod_a1/(k_a+1)`.
3. **Multiply** the two expansions (giving monomials of total degree
   `t+r+1`) and define
   `\displaystyle W(r,t):=\sum_{(\mathrm{exps},\,\mathrm{coeff})}
   \mathrm{coeff}\cdot\prod_i(\mathrm{exps}[i]!)`.

This is legitimate as a `K`-free (indeed `K`-independent, `r`-only)
quantity because Proposição S's formula and the conditional-moment
expansion, for a genuine size-`r` subset `A` inside a *larger* `K`-
dimensional model, are manifestly **symmetric** functions of the values
`\{p_a:a\in A\}` and `p_D` alone (they never reference `p_i` for `i\notin
A`), so relabeling `A\to\{0,\ldots,r-1\}` produces the identical monomial
shapes and coefficients — a fact re-derived and used explicitly in Section
4 below to justify the reduction identity.

### 3.2 Fresh reproduction and extension

`W_closed_form.py` (this directory) re-implements this recipe completely
fresh (a stars-and-bars `compositions()` generator, avoiding the
`itertools.product`-then-filter approach, which is exponential and times
out for `r>10`) and computes `W(r,t)` for `r=0,\ldots,10`, `t=1,\ldots,9`
(`99` cells, exact `Fraction` arithmetic, `\approx18`s runtime), plus a
citation-only cross-check against `32` values transcribed from
`find_W_pattern.log` (`t=1,\ldots,4`, `r=0,\ldots,7`). Both checks match
exactly (full log: `W_closed_form.log`).

### 3.3 The general closed form, derived (not merely pattern-matched)

Write the propS expansion as one "all-diagonal" monomial (`\mathrm{exps}=
(1,\ldots,1,1)`, coefficient `r!`) plus `r` "doubled-at-`b`" monomials
(`b=0,\ldots,r-1`; `\mathrm{exps}` has `2` at position `b`, `1` at the
other `r-1` positions in `A`, `0` at `p_D`; coefficient `r!` each).
Multiplying by a conditional-moment monomial of shape `(k_0,\ldots,
k_{r-1},k_D)` (a composition of `t`) and simplifying the factorial
algebra:

* **All-diagonal term.** Combined exponent `(k_0+1,\ldots,k_{r-1}+1,
  k_D+1)`. A short computation (cancel `(k_a+1)!/(k_a+1)=k_a!` for each
  `a\in A`) shows the combined coefficient times `\prod_i(\mathrm{exps}
  [i]!)` collapses to exactly `t!\cdot(k_D+1)`, **for every composition**
  `(k_0,\ldots,k_{r-1},k_D)` — a clean, composition-independent
  simplification.
* **Doubled-at-`b` term** (`b=0,\ldots,r-1`). Combined exponent has
  `k_b+2` at position `b`, `k_a+1` elsewhere in `A`, `k_D` at `p_D`. The
  same style of cancellation gives combined coefficient times
  `\prod_i(\mathrm{exps}[i]!) = t!\cdot(k_b+2)`, again for every
  composition.

Summing over all `N:=\binom{t+r}r` compositions of `t` into `r+1` parts,
and using the symmetry fact that every one of the `r+1` "slots" of a
composition of `t` into `r+1` parts has the same average value `t/(r+1)`
over all compositions (so `\sum_{\text{compositions}}k_D=\sum_{\text{
compositions}}k_a=tN/(r+1)` for any fixed slot):

`W(r,t) = r!\Big[\big(tN/(r+1)+N\big) + r\big(tN/(r+1)+2N\big)\Big]
       = \frac{r!\,N}{r+1}\Big[(t+r+1)+r(t+2r+2)\Big]`

and `(t+r+1)+r(t+2r+2) = t(r+1)+(2r^2+3r+1) = t(r+1)+(2r+1)(r+1) =
(r+1)(t+2r+1)`, so the `(r+1)` cancels cleanly:

`\boxed{W(r,t) = r!\,N\,(t+2r+1) = r!\cdot\frac{(t+r)!}{t!\,r!}\cdot t!
\cdot(t+2r+1) = (t+2r+1)\,(t+r)!}`

> **[Correção, 2026-08-29 — referee hostil, wave 27 `W-RT-CLOSED-FORM-
> ATTEMPT`]** A derivação exibida acima tem uma lacuna algébrica interna,
> identificada pelo referee hostil deste front. O parágrafo imediatamente
> anterior estabelece que a contribuição por composição do termo
> "all-diagonal" colapsa para exatamente `t!\cdot(k_D+1)` (e,
> simetricamente, `t!\cdot(k_b+2)` para cada termo "doubled-at-`b`"); mas
> a linha "Summing over all `N` compositions..." acima, `W(r,t) =
> r!\Big[(tN/(r+1)+N)+r(tN/(r+1)+2N)\Big]`, omite esse fator `t!` — lida
> literalmente, o "bracket" ali **não** é igual ao `W(r,t)` verdadeiro
> para `t\ge2` (o referee confirmou o desacordo em `48/56` células
> testadas com esse fator ausente; só `t=1` mascara o erro, pois `1!=1`).
> O fator `t!` reaparece sem justificativa explícita na etapa seguinte do
> boxed acima, `r!\cdot\frac{(t+r)!}{t!\,r!}\cdot t!\cdot(t+2r+1)`, que
> reinsere exatamente o `t!` que faltava. A cadeia, seguida linha a linha
> de forma literal, portanto não se conecta algebricamente nesse ponto.
>
> **A derivação correta** (confirmada pelo referee via três rotas
> independentes e `110` células frescas — `adv2_derivation_check.py` — e
> por esta sessão via `sympy`, `60` células, antes do despacho do
> referee) inclui o `t!` desde a soma sobre composições:
>
> `W(r,t) = r!\,t!\Big[\big(tN/(r+1)+N\big) + r\big(tN/(r+1)+2N\big)\Big]
>        = r!\,t!\,N\,(t+2r+1)
>        = r!\,t!\cdot\frac{(t+r)!}{t!\,r!}\cdot(t+2r+1)
>        = (t+2r+1)\,(t+r)!`
>
> — a mesma fórmula final em caixa, agora conectada sem inserção
> não-explicada de nenhum fator em nenhuma etapa. **A fórmula final
> `W(r,t)=(t+2r+1)(t+r)!` em si não é, e nunca foi, afetada**: estava
> correta antes desta correção e permanece correta agora (confirmada por
> `500+` células frescas do referee através de rotas totalmente
> independentes, Item 1&2 do `REFEREE_REPORT.md`) — o problema era
> exclusivamente de exposição na derivação exibida (um fator `t!` omitido
> numa linha e reinserido sem explicação duas linhas depois), não um erro
> no resultado. Ver `adversarial/REFEREE_REPORT.md`, Item 1&2, e
> `adversarial/adv2_derivation_check.py`.

This **derivation, not a numeric fit**, is what proves the closed form —
it is checked line-by-line against the fresh computation of Section 3.2
(all `99` cells match exactly, `W_closed_form.log`) and reduces exactly to
the predecessor's own `t=1,2` formulas: `W(r,1)=(2r+2)(r+1)!=2(r+1)^2r!`
✓, `W(r,2)=(2r+3)(r+2)!=r!(r+1)(r+2)(2r+3)` ✓ (both re-derived as special
cases of the general formula, not separate computations).

---

## 4. The reduction identity, re-derived and re-verified independently

Predecessor's Section 5.3 states `E[(M_K')^t]=K!\sum_{r=0}^K\binom Kr
W(r,t)/(K+t+r+1)!` and cross-checks it against their own direct
computation (`15/15` cells, `K=1,\ldots,5`, `t=1,\ldots,3`). This front
re-derives the identity from scratch (the exchangeability argument of
Section 3.1's last paragraph, made precise: for a genuine size-`r` subset
`A\subseteq\{0,\ldots,K-1\}` of a `K`-dimensional model, `K>r`, Proposição
S's weight and the conditional moment are symmetric in `\{p_a:a\in A\}`
and reference no other coordinate, so their monomial expansion, integrated
against the Dirichlet-moment formula `E[\prod p_i^{k_i}]=K!\prod(k_i!)/
(K+\sum k_i)!`, contributes exactly `W(r,t)\cdot K!/(K+t+r+1)!` **per
subset**, identical for every one of the `\binom Kr` subsets of size `r`;
summing over `r=0,\ldots,K` gives the stated identity) and **independently
re-verifies it computationally**, via `reduction_and_moment_crosscheck.py`
(this directory, fresh code), three ways at once:

* **Route 1** (direct subset enumeration): the full `K`-dimensional
  monomial algebra, summed over every subset `A\subseteq\{0,\ldots,K-1\}`
  individually — no grouping by size, no reference to `W(r,t)` at all.
* **Route 2** (via the closed form `W(r,t)=(t+2r+1)(t+r)!` of Section
  3.3): the reduction identity, plugged in directly.
* **Route 3** (target): `E[M_K^t]`, computed by direct fresh `sympy`
  symbolic integration of `x^t\cdot2Kx(1-x^2)^{K-1}` over `[0,1]` —
  independent of Proposição S, the Dirichlet-moment formula, or `W(r,t)`
  entirely.

All three agree exactly, **`48/48` cells** (`K=1,\ldots,8`, `t=1,\ldots,
6`, full log `reduction_and_moment_crosscheck.log`). This validates
simultaneously the `W(r,t)` closed form, the reduction identity, and
(within this range) Claim B's moment-matching claim.

---

## 5. Result 2: the `K`-symbolic sum, closed — the mandate's Step 2

### 5.1 What the mandate's literal method (`sympy.summation`/Gosper) gives

`symbolic_K_sum_attempt.py` (this directory) runs exactly what the mandate
asks: `\texttt{sympy.summation}` and the lower-level
`\texttt{sympy.concrete.gosper.gosper_sum}` (a **complete** decision
procedure for indefinite hypergeometric summation — a `\texttt{None}`
result is a genuine certificate that no hypergeometric-term antidifference
exists, not merely "sympy could not find one") on
`\sum_{r=0}^K\binom Kr(t+2r+1)(t+r)!/(K+t+r+1)!`, `K` symbolic:

| `t` | `\texttt{sympy.summation}` | `\texttt{gosper\_sum}` |
|---|---|---|
| `1` (odd) | residual `\mathrm{hyper}(\ldots)` term, does not close | `\texttt{None}` |
| `2` (even) | residual `\mathrm{hyper}(\ldots)` term (but see below) | `1/(K{+}1)!` — closes |
| `3` (odd) | residual `\mathrm{hyper}(\ldots)` term | `\texttt{None}` |
| `4` (even) | residual `\mathrm{hyper}(\ldots)` term | `2/(K{+}2)!` — closes |
| `5,7` (odd) | residual | `\texttt{None}` |
| `6,8` (even) | residual | `6/(K{+}3)!`, `24/(K{+}4)!` — close |
| symbolic `t` | — | `\texttt{None}` |

(`\texttt{sympy.summation}`'s own default algorithm does not fully
simplify even the even-`t` cases to the clean Gosper form shown, leaving a
messy but ultimately-equal expression — the direct `\texttt{gosper\_sum}`
call is the cleaner, more informative probe, hence tabulated above.) So:
**the mandate's literal named method closes only for even `t`**, and
genuinely certifies non-closure (not just failure) for odd or symbolic
`t`. This alone is honest, precisely-diagnosed partial progress on Step 2
— but it turned out not to be the end of the story.

### 5.2 Reality-checking the even-`t` closures

The even-`t` `\texttt{gosper\_sum}` closures were cross-checked (not just
trusted): `1/(K{+}1)!` at `t=2` gives `K!\cdot1/(K{+}1)!=1/(K{+}1)`,
matching the known even-moment target `K!\,(t/2)!/(K{+}t/2)!` exactly (a
completely elementary special case, since even `t/2`-th powers of Gamma
are ordinary factorials); likewise `t=4,6,8`. These are genuine, trusted,
Gosper-*certified* results — an unconditional proof of Claim B's
moment-matching for the **infinite family** of all even moments, all `K`,
which is already strictly more than any finite-cell check could give.

### 5.3 Attempting a `K`-recursion via Gosper-differencing

To try to extend closure to odd/general `t`, this front attempted the
standard "creative telescoping" idea: guess the recursion
`(t+2K)S(K,t)=2S(K-1,t)` (matching the conjectured target
`S(K,t)=2^K/\prod_{j=1}^K(t+2j)`, which satisfies exactly this recursion)
and try to certify it by Gosper-summing the difference
`h(r):=(t+2K)a(K,r,t)-2a(K-1,r,t)` (`a(K,r,t)` being `S(K,t)`'s summand)
over `r=0,\ldots,K`.

### 5.4 A self-caught false lead (disclosed per archive convention)

An initial attempt, feeding `h(r)` (built from `\texttt{sympy.binomial}`
objects, then passed through `\texttt{sp.simplify}` before
`\texttt{gosper\_sum}`) returned a clean `0` — which, combined with the
easily-checked boundary term `a(K,K,t)`, appeared to **prove** the
recursion for symbolic `K,t` via a genuine Gosper certificate. Before
trusting this, the same mathematically identical quantity was recomputed
in two other syntactically different forms: (i) the same
`\texttt{sympy.binomial}`-based `h(r)`, fed to `\texttt{gosper\_sum}`
**without** the preceding `\texttt{sp.simplify}` call, and (ii) `h(r)`
built with the binomial coefficients written out as **explicit factorial
ratios** (`K!/(r!(K-r)!)`) instead of `\texttt{sympy.binomial}` objects.
**Both of these return `\texttt{None}`** — a direct contradiction with the
first form's `0`. `symbolic_K_sum_attempt.py` (this directory) reproduces
this exact three-way discrepancy and prints it explicitly (full log:
`symbolic_K_sum_attempt.log`, "Part 3"). **Diagnosis:** the `0` is a
spurious artifact of how `\texttt{sympy}`'s Gosper implementation handles
`\texttt{sympy.binomial}(K{-}1,r)` at the `r=K` boundary (where
`\binom{K-1}K=0` combinatorially, via a removable `0/\mathrm{pole}`
cancellation in the underlying `\Gamma`-function ratio) **after**
`\texttt{sp.simplify}` transforms the expression into a specific form —
not a trustworthy proof. **This result is explicitly not relied upon
anywhere else in this document.** This is exactly the kind of self-caught
issue this archive's convention asks to be disclosed rather than silently
discarded or silently used.

### 5.5 The actual proof: elementary calculus, no black box

Having caught Section 5.4's false lead, this front instead found and
proved the general closed form directly, via `beta_integral_proof_
verification.py` (this directory). The derivation, in four steps (each
checked below both symbolically, with `t` left as a genuinely free
symbol, and by massive independent exact numerics):

**Step 0 (Beta-integral form).** The classical Beta identity
`\int_0^1x^a(1-x)^bdx=a!b!/(a+b+1)!` (`a=t+r`, `b=K`) gives `(t+r)!/
(K+t+r+1)! = (1/K!)\int_0^1x^{t+r}(1-x)^Kdx`, so `S(K,t):=\sum_r\binom Kr
W(r,t)/(K+t+r+1)! = (1/K!)\int_0^1x^t(1-x)^K\,P_K(x,t)\,dx`, where
`P_K(x,t):=\sum_{r=0}^K\binom Kr(t+2r+1)x^r`.

**Step A (binomial theorem).** Splitting `t+2r+1=(t+1)+2r` and using
`\sum_r\binom Krx^r=(1+x)^K`, `\sum_rr\binom Krx^r=Kx(1+x)^{K-1}`
(the latter by differentiating the former — both completely standard):
`P_K(x,t)=(1+x)^{K-1}\big[(t+1)(1+x)+2Kx\big]`. **Verified symbolically,
`t` free, `K=1,\ldots,8`: exact match, `8/8`** (`beta_integral_proof_
verification.log`, "Step A").

**Step B–C (algebra + direct symbolic integration).** `(1-x)^K(1+x)^{K-1}
=(1-x)(1-x^2)^{K-1}`, so `x^t(1-x)^KP_K(x,t)=x^t(1-x^2)^{K-1}\big[(t+1)
(1-x^2)+2Kx(1-x)\big]`; expanding and writing `f_K(x):=2Kx(1-x^2)^{K-1}`
(the already-proved density of `M_K`) and `\mu_s:=E[M_K^s]`:

`K!\,S(K,t) = (t+1)\!\int_0^1\!x^t(1-x^2)^Kdx \;+\; \mu_{t+1} \;-\; \mu_{t+1}`

— the last two terms are, respectively, `2K\int x^{t+1}(1-x^2)^{K-1}dx=
\mu_t` and `2K\int x^{t+2}(1-x^2)^{K-1}dx=\mu_{t+1}` (direct substitution
into the density's definition). **This step was cross-checked not by
trusting the hand algebra but by having `\texttt{sympy}` independently
integrate `x^t(1-x)^KP_K(x,t)` from scratch (no reference to the termwise
factorial-ratio sum) and compare to the termwise definition of `S(K,t)`:
exact match, `t` free, `K=1,\ldots,8`, `8/8`** ("Step B"), and separately
compared to the final target `\Gamma(t/2{+}1)/\Gamma(K{+}t/2{+}1)`
directly via `\texttt{sympy}`'s own integration engine: exact match, `t`
free, `K=1,\ldots,8`, `8/8`** ("Step C").

**Step D (the integration-by-parts identity, checked directly).** The
piece `(t+1)\int_0^1x^t(1-x^2)^Kdx` needs to equal `\mu_{t+1}` for the
`\mu_{t+1}` terms above to cancel. This follows from `\frac d{dx}\big[
x^{t+1}(1-x^2)^K\big] = (t+1)x^t(1-x^2)^K - 2Kx^{t+2}(1-x^2)^{K-1}`
integrated over `[0,1]`: the left side integrates to `\big[x^{t+1}
(1-x^2)^K\big]_0^1 = 0` (for `K\ge1`, `t>-1`, both endpoints vanish),
giving exactly `(t+1)\int x^t(1-x^2)^Kdx = 2K\int x^{t+2}(1-x^2)^{K-1}dx
=\mu_{t+1}`. **Verified directly by symbolic integration of both sides
separately (not just algebraically inferred), `t` free, `K=1,\ldots,8`,
`8/8`** ("Step D").

Substituting: `K!\,S(K,t)=\mu_t+\mu_{t+1}-\mu_{t+1}=\mu_t`, i.e.

`\boxed{S(K,t) = \mu_t/K! = \frac{\Gamma(t/2+1)}{\Gamma(K+t/2+1)}}`

**for every `K\ge1` and every real `t>-1`** (the derivation uses no
integer-`t` special structure at any step — every integral and the
integration-by-parts boundary argument are valid for general real `t>-1`;
`K=0` is the separate trivial case `S(0,t)=W(0,t)/(t+1)!=(t+1)!/(t+1)!=1`,
matching `\Gamma(t/2{+}1)/\Gamma(t/2{+}1)=1`).

### 5.6 Large-scale independent numeric confirmation

Beyond the symbolic-in-`t` checks (`K=1,\ldots,8`), `beta_integral_proof_
verification.py` runs two further, completely independent (no `sympy`
integration, no Gosper) confirmations:

* **Exact `\texttt{Fraction}` arithmetic**, integer `t=1,\ldots,40` (both
  parities), `K=1,\ldots,150`: `6000` cells, `S(K,t)` computed via the
  termwise definition compared to `2^K/\prod_{j=1}^K(t+2j)` — **all
  `6000` match exactly**.
* **Exact half-integer `t`** (`t\in\{1/2,3/2,5/2,-1/2,7/2\}`, including a
  negative value, via `\texttt{sympy.Rational}`/`\Gamma`, exact symbolic
  equality via `\texttt{sp.simplify}`, not numeric approximation),
  `K=0,\ldots,15`: `80` cells, **all match exactly** — genuinely new
  information beyond integer `t`, since a spurious pattern that happened
  to work only at integers would be extremely unlikely to survive
  non-integer, negative-fractional test points too.

Full log: `beta_integral_proof_verification.log`.

---

## 6. Claim B, fully proved for every `K\ge1`

`full_chain_verification.py` (this directory) assembles the chain
end-to-end and re-checks it one final time, maximally directly: `E[(M_K')
^t]` via the `W(r,t)`-reduction (Section 3.3's closed form, Section 4's
reduction identity) versus `E[M_K^t]` via fresh `sympy` integration —
**`150/150` cells** (`K=1,\ldots,15`, `t=1,\ldots,10`), exact match (full
log `full_chain_verification.log`).

Putting the pieces together:

1. `W(r,t)=(t+2r+1)(t+r)!` (Section 3.3, PROVED, all `r,t`).
2. `E[(M_K')^t]=K!\sum_r\binom Kr W(r,t)/(K+t+r+1)!` (Section 4, PROVED,
   exchangeability argument, all `K,t`).
3. `\sum_r\binom Kr W(r,t)/(K+t+r+1)! = \Gamma(t/2{+}1)/\Gamma(K{+}t/2{+}
   1)` (Section 5.5, PROVED, elementary calculus, all `K\ge0`, all real
   `t>-1`).
4. `E[M_K^t] = K!\,\Gamma(t/2{+}1)/\Gamma(K{+}t/2{+}1)` (standard
   Beta-integral evaluation of the already-proved density `f_{M_K}(x)=
   2Kx(1-x^2)^{K-1}`, Estágio 24; re-derived fresh here — `sympy`
   integration, symbolic `t`, `K=1,\ldots,7`, exact match,
   `reduction_and_moment_crosscheck.py`'s Route 3 and its cross-checks).

**(1)+(2)+(3)+(4) `\Rightarrow` `E[(M_K')^t]=E[M_K^t]` for every `K\ge1`
and every positive integer `t`.** `M_K'` and `M_K` are both supported on
the compact interval `[0,1]`; two probability measures on a compact
interval with identical moments of every positive-integer order are equal
(a classical consequence of Stone–Weierstrass — polynomials are dense in
`C[0,1]`, so equal moments of every order imply equal integrals against
every continuous test function, hence equal Borel measures; cited here as
a standard fact, not re-derived, matching this archive's convention for
such classical facts — e.g. the predecessor's own citation of the
order-statistic-spacings-are-Dirichlet fact). Determinacy itself is not
even a subtle issue here: `M_K',M_K\in[0,1]` means every moment is
trivially bounded by `1`, so Carleman's condition holds automatically.

> **Claim B (PROVED, every `K\ge1`).** `M_K'\overset d=M_K`, i.e.
> `F_{M_K'}(x)=F_K(x)=1-(1-x^2)^K` for every `x\in[0,1]`, every `K\ge1`.

This upgrades the predecessor's Claim B from "proved at `K=1`, evidenced
but open for `K\ge2`" to **proved for every `K\ge1`**.

### 6.1 Consequence: the Main Theorem becomes unconditional

The predecessor's Theorem A (`k_free_convergence_bridge_attempt/ATTEMPT.md`
Section 4) is an unconditional, `K`-free coupling bound
`|M_n^{(K)}-M_K'|\le\varepsilon(K,n)` off an event of probability
`\le\delta(K,n)`, **not depending on Claim B at all** — this front does
not touch, re-derive, or re-verify Theorem A's own proof (out of scope,
per the mandate; it is cited as a black box). Predecessor's Section 6
combines Theorem A with Claim B (there conditional) to get

`\sup_x|F_n^{(K)}(x)-F_K(x)| \le \delta(K,n)+\Lambda_K\varepsilon(K,n)
\le 8K^2/n`

— stated there as **conditional on Claim B**. With Claim B now proved
unconditionally for every `K\ge1` (Section 6 above), **this same
assembly, with no change to any step, gives the Main Theorem
unconditionally**:

> **Main Theorem (now UNCONDITIONAL).** For every `K\ge1`, `n\ge K+1`:
> `\displaystyle\sup_x|F_n^{(K)}(x)-F_K(x)| \le 8K^2/n`.

This is exactly the mandate's stated success criterion ("general closed
form for `W(r,t)` plus the resulting `K`-symbolic sum closing... making
Theorem A's conditional bound... UNCONDITIONAL for all `K\ge1`"). No file
outside this front's own directory is edited to reflect this — per the
scope discipline stated in the mandate and reconfirmed in Section 13,
integrating this consequence into `THEOREM.md` and the dependency map is
left to the orchestrating session/a downstream integration step.

---

## 7. What did NOT close cleanly, honestly stated

Even though the mandate's overall success criterion is met, several
specific sub-methods and framings did **not** work, and are recorded here
precisely rather than glossed over:

1. **The mandate's literally-named method — `sympy.summation`/`gosper_sum`
   applied directly to the `K`-sum — closes only for even `t`** (Section
   5.1). It genuinely, certifiably fails (not merely "sympy could not
   find it") for odd `t` and for symbolic `t`. The general closed form was
   found by a different route (Section 5.5, elementary calculus), not by
   getting this specific tool to succeed on the general case.
2. **A Gosper-differencing attempt at a `K`-recursion produced a spurious
   "proof"** that was caught only by re-deriving the same quantity in a
   syntactically different form and finding a contradiction (Section
   5.4). This is flagged not as a triumph but as a genuine near-miss:
   without the cross-check, this front could have shipped an incorrect
   "Gosper-certified" claim. The result of that attempt is **not** used
   anywhere in the actual proof (Section 5.5 stands independently of it).
3. **The moment-determinacy step (Section 6) is a cited classical fact**,
   not re-derived from first principles in this document — matching this
   archive's established convention for such standard results (e.g. the
   predecessor's own citation of Dirichlet order-statistic spacings), but
   worth stating plainly rather than letting it pass silently: this
   front's own original contribution is Results 1 and 2 (Sections 3, 5);
   Result 3 (Section 6) is those two results combined with one cited
   classical theorem.
4. **This front does not touch, re-verify, or extend Theorem A itself**
   (predecessor's Section 4) — it is cited as a black box throughout, per
   the mandate's own framing of this front's target as Claim B
   specifically. Any residual risk in Theorem A's own proof (already
   unconditional, already numerically cross-checked extensively by the
   predecessor, `420{,}000` trials, zero violations) is outside this
   front's scope and not re-examined here.
5. **Sharpness of the `8K^2` constant, or of `n_0(K)=K+1`**, is not
   examined here either — out of scope, inherited unchanged from the
   predecessor's own honest non-examination of this point (their Section
   7 item 5).

---

## 8. Self-caught issues (disclosed per archive convention)

1. **The Gosper-differencing false lead of Section 5.4** — the single
   most significant self-caught issue in this front's work, described in
   full there. Caught by re-deriving the same quantity via two other
   syntactic forms and finding a contradiction, before it was used for
   anything. Not present in the final proof chain at all.
2. **An initial, over-eager symbolic-in-`t` check used `\texttt{sp.
   cancel}`** on a difference of two large `\texttt{sympy}` expressions
   involving `\texttt{factorial}(t{+}\text{offset})` terms for `t`
   symbolic, `K=9,\ldots,16` — `\texttt{sp.cancel}` does **not**
   automatically recognize that these symbolic-factorial expressions
   telescope (it treats `\texttt{factorial}(t{+}9)` and
   `\texttt{factorial}(t{+}10)` as unrelated atoms unless explicitly
   guided), producing enormous, useless, unsimplified output rather than
   a clean `0`/nonzero verdict. This was **not** a mathematical error, but
   a wasted-effort dead end in verification strategy — caught immediately
   from the output's size and irreducibility, and abandoned in favor of
   (i) the completely rigorous Steps A–D of Section 5.5 (which sidestep
   this issue entirely by comparing against `\texttt{sympy}`'s own
   integration-engine output rather than trying to force-cancel two
   independently-built symbolic sums) and (ii) the large-scale numeric
   checks of Section 5.6. No incorrect number was produced by this dead
   end; it simply did not finish, and is recorded here only because the
   archive convention is to disclose the working, not just final numbers.
3. **An early attempt to verify `S(K,t)` vs. the target formula at large
   `K` (up to `40`) via `\texttt{mpmath}` floating-point arithmetic at
   `60` decimal digits of precision produced an apparent large
   discrepancy** (relative error `\approx1`) at `K=40`, `t=2` — traced
   immediately to insufficient precision (`\Gamma(\approx123)` has
   magnitude `\sim10^{200}`, so `60`-digit precision is nowhere near
   enough for the cancellations involved in summing terms of vastly
   different magnitudes). Re-checked with **exact** `\texttt{Fraction}`
   arithmetic at the same `(K,t)=(40,2)` and confirmed to match exactly,
   with zero discrepancy — the mismatch was purely a floating-point
   precision artifact, not a mathematical error, and this front abandoned
   the floating-point route entirely in favor of exact arithmetic
   throughout (Section 5.6), exactly matching the mandate's own
   prediction that "you will very likely need no randomness at all" (and,
   as it turned out, no floating point either).
4. **No bug found in the core `W(r,t)` pipeline or the reduction-identity
   pipeline**: both were cross-checked against the predecessor's own
   cited log values (Section 3.2) and, independently, against a
   completely different direct-subset-enumeration computation that never
   references `W(r,t)` at all (Section 4, Route 1 vs. Route 2) — full
   agreement throughout, `48/48` and `150/150` cells respectively.

---

## 9. Numerical/symbolic verification summary

All scripts in this directory, written fresh for this front (no import
from any predecessor or sibling front's `.py` files). No randomness used
anywhere — every check is exact `Fraction` or `sympy` symbolic/exact
arithmetic.

| script | type | what it checks |
|---|---|---|
| `W_closed_form.py` | exact (`Fraction`), no randomness | fresh reproduction of `W(r,t)`'s exact definition; `99` cells vs. the closed form `(t+2r+1)(t+r)!`; cross-check vs. `32` values cited from the predecessor's own log |
| `reduction_and_moment_crosscheck.py` | exact (`Fraction`+`sympy`), no randomness | three independent routes to `E[(M_K')^t]` (direct subset enumeration; via `W(r,t)`; fresh target integration), `48` cells |
| `symbolic_K_sum_attempt.py` | symbolic (`sympy`), no randomness | the mandate's literal Step 2 (`sympy.summation`/`gosper_sum`, symbolic `K`): closes for even `t`, certifiably fails for odd/symbolic `t`; documents and reproduces the self-caught Gosper-differencing discrepancy |
| `beta_integral_proof_verification.py` | symbolic (`sympy`) + exact (`Fraction`), no randomness | the actual general-`K`, general-`t` proof (Beta integral + binomial theorem + integration by parts), Steps A–D verified symbolically (`t` free, `K=1..8`) plus `6000` exact integer cells plus `80` exact half-integer-`t` cells |
| `full_chain_verification.py` | exact (`Fraction`+`sympy`), no randomness | end-to-end: `E[(M_K')^t]` via the fully-closed-form chain vs. fresh target integration, `150` cells; states the resulting unconditional Main Theorem |

---

## 10. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `W(r,t)` exact definition, fresh reproduction | **PROVED** (matches predecessor's cited log values and own extended computation, `99`+`32` cells) |
| 2 | `W(r,t) = (t+2r+1)(t+r)!` | **PROVED** (derived from the exact definition via multinomial-coefficient algebra; not pattern-matched), all `r,t` |
| 3 | Reduction identity `E[(M_K')^t]=K!\sum_r\binom Kr W(r,t)/(K+t+r+1)!` | **PROVED** (exchangeability argument), cross-checked `48/48` + `150/150` cells |
| 4 | Mandate's literal Step 2 method (`sympy.summation`/`gosper_sum` on the direct sum) | closes for **even `t` only** (Gosper-certified); certified non-closure for odd/symbolic `t` |
| 5 | Gosper-differencing attempt at a `K`-recursion | **spurious result caught and discarded** (self-caught issue, Section 5.4); not used in the proof |
| 6 | `S(K,t)=\Gamma(t/2{+}1)/\Gamma(K{+}t/2{+}1)`, general `K\ge0`, general real `t>-1` | **PROVED** (elementary calculus: Beta integral + binomial theorem + integration by parts, Section 5.5); cross-checked symbolically (`t` free, `K=1..8`) and across `6080` further exact cells |
| 7 | `E[M_K^t]=K!\,\Gamma(t/2{+}1)/\Gamma(K{+}t/2{+}1)` (target, re-derived fresh) | **PROVED** (standard Beta-integral evaluation of the already-proved density) |
| 8 | `E[(M_K')^t]=E[M_K^t]`, every `K\ge1`, every positive integer `t` | **PROVED** (combining 2,3,6,7) |
| 9 | **Claim B**: `M_K'\overset d=M_K`, every `K\ge1` | **PROVED** (combining 8 with cited classical moment-determinacy on compact support) |
| 10 | **Main Theorem** `\sup_x|F_n^{(K)}(x)-F_K(x)|\le8K^2/n` | **PROVED, UNCONDITIONALLY**, every `K\ge1`, `n\ge K+1` (Theorem A, predecessor's, unconditional and untouched here, combined with item 9) |
| 11 | Sharpness of `8K^2` or of `n_0(K)=K+1` | **NOT EXAMINED** (out of scope, inherited from predecessor) |
| 12 | Theorem A's own proof | **not re-verified here** (out of scope per mandate; cited as a black box) |

---

## 11. Seeds

Reserved range: `20260937000`–`20260937999` (`DISC-DEC-127`, frente (b)).

**Grep-confirmation before any file in this directory was written:**
```
$ grep -rn "20260937" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8340:      sympy. Seed reservado: 20260937000-20260937999.
```
Only the governance reservation line — the range was genuinely unused.

**Grep-confirmation after all work in this directory:**
```
$ grep -rn "20260937" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8340:      sympy. Seed reservado: 20260937000-20260937999.
```
Still only the governance line — **no seed from the reserved range was
ever used**. Every computation in this front is exact `Fraction` or
`sympy` symbolic/exact arithmetic; no random sampling was needed anywhere
(the mandate itself predicted this — "you will very likely need no
randomness at all" — and it turned out to be exactly right, down to the
single self-caught `\texttt{mpmath}`-floating-point false alarm of Section
8 item 3, which was itself abandoned in favor of exact arithmetic).

---

## 12. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `W_closed_form.py` / `.log` | fresh reproduction of `W(r,t)`'s exact definition, `99`-cell verification of the closed form `(t+2r+1)(t+r)!`, cross-check vs. the predecessor's cited log values |
| `reduction_and_moment_crosscheck.py` / `.log` | three independent routes to `E[(M_K')^t]`, `48`-cell cross-check |
| `symbolic_K_sum_attempt.py` / `.log` | the mandate's literal Step 2 attempt via `sympy`/Gosper; documents even-`t` closure, odd/symbolic-`t` certified non-closure, and the self-caught Gosper-differencing discrepancy |
| `beta_integral_proof_verification.py` / `.log` | the actual general-`K`,`t` closed-form proof (Beta integral + binomial theorem + integration by parts), symbolic Steps A–D plus `6080` exact numeric cells |
| `full_chain_verification.py` / `.log` | end-to-end `150`-cell final check and statement of the resulting unconditional Main Theorem |

---

## 13. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, or `index.html`. No file inside `k_free_convergence_bridge_
attempt/` (the sibling/predecessor directory) was written to — only read,
for the citations listed in Section 1. No `adversarial/` subdirectory
created, no referee dispatched by this front. No `git` command run.

> **[Nota, 2026-08-29 — referee hostil, wave 27 `W-RT-CLOSED-FORM-
> ATTEMPT`]** O referee hostil apontou uma tensão de baixa severidade: o
> mandato de despacho do referee (redigido pela sessão orquestradora)
> menciona que este front "ran a read-only `git status --porcelain` at
> the very end", o que, se preciso, seria tecnicamente um comando `git`
> não listado nesta seção de "No `git` command run" acima. O referee não
> executou `git` por conta própria (por instrução própria dele mesmo) e
> não pôde confirmar diretamente se tal chamada ocorreu; o que confirmou é
> que `git status`, com ou sem `--porcelain`, é somente-leitura por
> construção (não altera nenhum arquivo rastreado nem `ref`) — logo, caso
> tenha ocorrido, não teve nenhum efeito sobre qualquer arquivo, exatamente
> como esta seção afirma quanto ao conteúdo. Sem impacto matemático, sem
> impacto em qualquer arquivo rastreado; registrado aqui apenas por
> disciplina de disclosure. Ver `adversarial/REFEREE_REPORT.md`, Item 7.

No `.py` file from any other front (this lineage or any ancestor/sibling) was
imported or copied — every script in this directory was written fresh
from `THEOREM.md`, the predecessor's `ATTEMPT.md` prose, and the
predecessor's `find_W_pattern.py`'s prose description of `W(r,t)`'s exact
definition (transcribed and cited, per the mandate, not imported as code).
Every claim above is labeled PROVED / NOT EXAMINED / (for the one
genuinely non-closing sub-method) certified non-closing at the point of
use. The mandate's stated success criterion — a general closed form for
`W(r,t)` plus the resulting `K`-symbolic sum closing, upgrading Claim B
toward (here: to) an unconditional `K`-free proof — is met in full,
achieved via a route (elementary calculus) different from the one
literally named in the mandate (`sympy.summation`), after that literal
route was attempted, found to close only partially (even `t`), and a
genuine self-caught false lead along the way was caught and discarded
before being trusted. No claim of progress on any Millennium Problem
anywhere in this document; this is pure combinatorial mathematics
internal to the u12 ensemble defined in `THEOREM.md`.
