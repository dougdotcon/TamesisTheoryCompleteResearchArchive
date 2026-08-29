# ATTEMPT — closing the diagonal `2F0` sum for `S_n(γ)`, and a
# correction to the predecessor's Charlier non-identification

**Wave 29, front (b), `DIAGONAL-2F0-SUM-ATTEMPT`, authorized by
`DISC-DEC-134`.** Mandate: attempt to close the "diagonal-parameter"
`2F0` sum `S_n(γ):=\sum_{k=1}^n(1-γ)^k\,{}_2F_0(-k,n-k+1;;w)`,
`w=-γ/((1-γ)n)`, identified by the immediate predecessor (Estágio 51,
`GAMMA-C-GAMMA-CONSTRUCTION-ATTEMPT`) as the single most promising
unexploited lead toward `C(γ)`, `γ\in(0,1)` — either directly (Route 1)
or via a fundamentally different technique for `C(γ)` (Route 2).

---

## VERDICT (up front)

> **The diagonal `2F0` sum is NOT closed. `C(γ)` for `γ\in(0,1)` remains
> entirely OPEN.** This front pursued Route 1 (closing the diagonal sum
> directly) substantially, and found that it does **not** yield a
> closed form or a rigorous route to the second-order term within the
> time available — but the reason it fails is now understood precisely,
> not just asserted, and two independent lines of genuinely new,
> verified work came out of the attempt:
>
> 1. **A correction to the predecessor's own record (verified, concrete).**
>    The predecessor's Estágio-51 front reported that identifying `A_k`
>    with the classical Charlier polynomial family "does NOT check out"
>    (an exact, `n`-independent residual `-2γ` at `k=1`) and dropped the
>    naming claim. **This front re-derived the identification from
>    scratch using the standard DLMF (18.20.1) sign convention,
>    `C_n(x;a):={}_2F_0(-n,-x;;-1/a)`, and found it to be an EXACT
>    algebraic identity** — `A_k(n,γ)=(1-γ)^k\,C_k(k-n-1;\,(1-γ)n/γ)`,
>    confirmed symbolically (`k=0..6`) and on 50 fresh exact-`Fraction`
>    numeric spot checks, 0 mismatches. Moreover, **this front
>    reproduced the predecessor's exact `-2γ` residual exactly** by
>    using the single most natural sign slip (`+1/a` instead of DLMF's
>    `-1/a` inside the `2F0`) — strong, concrete evidence that the
>    predecessor's non-identification was a sign-convention bug in
>    their own script, not a mathematical fact, and that the
>    predecessor's own dedicated referee (who re-read, but did not
>    independently re-derive, that specific claim) missed it. The
>    Charlier identification IS real; see §2 for why this does not, on
>    its own, unlock the diagonal sum either way.
> 2. **A new exact double-sum reformation of `S_n`, with a genuinely
>    new sub-identity, PROVED**, but shown — analytically and
>    numerically, not just by failing to find something better — to
>    retain the *same* `Θ(\sqrt n)`-scale Gaussian/CLT structure as the
>    original `k`-sum, merely relocated to a new index `m` with a
>    different (exactly identified) constant. This is a genuine
>    structural finding, not a non-result: it explains *why* naively
>    swapping the order of summation does not sidestep the difficulty
>    that has stopped five prior fronts, and it should save a future
>    front from re-attempting exactly this path expecting an easy win.
>    A fresh, independent numerical computation of `S_n` via this new
>    route (entirely different algorithm from every ancestor's direct
>    `k`-sum) reproduces the already-conjectured `T(γ)` and `C(γ)` to
>    good precision, at moderate `n` — genuine new corroborating
>    evidence, not proof.
>
> **No claim of progress on any Millennium Problem; pure
> combinatorial/asymptotic mathematics internal to this archive, about
> a specific random-permutation-with-reroutes ensemble.**

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or
code was written**, per the dispatching mandate, in the order specified:

1. `.../gamma_gap1_cancellation_tracking_attempt/gamma_c_gamma_construction_attempt/ATTEMPT.md`
   (611 lines, the immediate predecessor, wave 28 front (b)) — read in
   full, with particular attention to §1 (the precise target `C(γ)`,
   `S_n`, and how they relate to Lemma E/`D_0(γ)`) and §2 (the exact
   `2F0` fact for `A_k`, the failed Charlier attempt, and the precise
   diagnosis of why the `2F0` fact alone doesn't close things). Also
   read: §7 (what remains open), §8 (self-caught issues), §9
   (scorecard).
2. `.../gamma_c_gamma_construction_attempt/adversarial/REFEREE_REPORT.md`
   (373 lines, sibling directory) — read in full. Independently
   confirmed the `2F0` identity and the surrounding moment machinery;
   confirmed the Charlier non-identification claim only by **re-reading**
   the predecessor's own log (§(g)), not by an independent
   re-derivation — this front's own script `02` found this specific
   claim does not survive independent re-derivation (see VERDICT item 1).
3. `THEOREM.md` — **Estágio 26** (`C(γ)` first named as the open
   second-order term; `D_0(γ)` and Lemma E PROVED; the three named
   technical gaps, "Lacuna 1/2/3", with Lacuna 2 later closed by
   Estágio 30) and **Estágio 51** (the immediate predecessor's own
   integration into `THEOREM.md`, confirming the same three-item
   verdict as its own `ATTEMPT.md`, and naming this front's mandate
   explicitly: close the diagonal-parameter sum of §2, or find a
   fundamentally different technique — not a sixth `n_0(γ)`-tightening
   front).
4. `.../gamma_scaling_attempt/ATTEMPT.md` (592 lines, the ultimate
   ancestor, wave 17 front (e)) — read in full, in particular §1
   (Lemma 1's exact combinatorial proof, the original definitions of
   `A_k`, `P_{k,m}`, `φ(n,γn)`) and §7.3 (the original heuristic
   derivation of `C(γ)`, cited but not re-derived here).

**No `.py` file of any ancestor or predecessor was read or imported
anywhere in this front.** Every script below (`01`–`07`) is written
fresh from the mathematical prose cited above; every borrowed fact
(the `2F0` identity itself, the definitions of `A_k`/`P_{k,m}`, the
closed forms `T(γ)`, `C(γ)`, `D_0(γ)`, `E_{\text{heuristic}}(γ)`) is
independently **re-derived or re-verified** in this front's own
scripts, not copied.

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, `index.html`, every ancestor/predecessor `ATTEMPT.md` and
`adversarial/` file (read-only), every sibling directory. No `git`
command of any kind was run. No `adversarial/` subdirectory created
inside this front's own directory; no referee dispatched (reserved for
the orchestrating session, per mandate).

---

## §1 Precise restatement of the target

Quoting the predecessor (itself quoting Lemma 1 and Lemma E, both
PROVED, cited): for `γ\in(0,1]`, `n\varphi(n,γn)=S_n:=\sum_{k=1}^n A_k`,
and `C(γ)` (the open second-order term of the `γ`-scaling law,
`\sqrt n(\varphi(n,γn)/\varphi_\infty(γn)-T(γ))\to C(γ)`,
`T(γ):=\sqrt{2/(2-γ)}`) is equivalent (Lemma E, PROVED) to
`S_n=G_n+D(γ)+o(1)`, `G_n:=\tfrac12\sqrt{πn/β}`, `β:=γ(2-γ)/2`,
`D(γ)=D_0(γ)+E(γ)`, with `D_0(γ)=(γ-1)/(2(2-γ))` PROVED (Lemma D0) and
`E(γ)` — conjectured to equal the closed form
`E_{\text{heuristic}}(γ):=\dfrac{-3γ^2+7γ-6}{6(γ-2)^2}` — the open
"hard half."

The predecessor's new exact fact (re-verified independently here,
script `01`): `A_k(n,γ)=(1-γ)^k\cdot{}_2F_0(-k,n-k+1;;w)`,
`w:=-γ/((1-γ)n)`, so

`S_n(γ) = \sum_{k=1}^n (1-γ)^k\,{}_2F_0(-k,\,n-k+1;\,;\,w)`

is exactly the object `nφ(n,γn)`, a **diagonal-parameter** `2F0` sum
(degree `-k` and second upper parameter `n-k+1` both move with `k`, at
fixed argument `w`) — this front's target, per the mandate.

---

## §2 Route 1(b): the Charlier identification, corrected (script `02`)

**The predecessor's naive parameter match, `x=k-n-1`,
`a=(1-γ)n/γ`, against `C_n(x;a):={}_2F_0(-n,-x;;-1/a)`, is in fact an
EXACT algebraic identity — it is a pure substitution into the same
series, not a claim requiring numerical confirmation.** Since
`{}_2F_0(A,B;;z)` is manifestly symmetric in `(A,B)`, setting `-x=n-k+1`
and `-1/a=w` inside the DLMF definition literally reproduces the
predecessor's own `2F0(-k,n-k+1;;w)` term by term. This front
re-verified this by hand (`k=1,2`) and then in fresh `sympy` code
(script `02`, Part A): **0/7 mismatches, `k=0..6`, symbolic `n,γ`**,
plus 50 fresh exact-`Fraction` numeric spot checks (Part D, seed
`20260943002`, reserved block): **0 mismatches**.

`A_k(n,γ) = (1-γ)^k \cdot C_k\big(k-n-1;\;(1-γ)n/γ\big)`,  EXACT, for
every `1\le k\le n`, `γ\in(0,1)`.

**Diagnosing the predecessor's reported `-2γ` residual (script `02`,
Part B/C).** There is more than one sign convention for Charlier
polynomials in the literature; the single most natural slip is using
`{}_2F_0(-n,-x;;+1/a)` instead of DLMF's `-1/a`. This front implemented
that variant explicitly and found it reproduces the predecessor's
reported residual **exactly**: at `k=1`, `(1-γ)\cdot C_1^{\text{wrong
sign}}(x;a) = 1-2γ`, i.e. a residual of `-2γ` against the true `A_1=1`
— matching the predecessor's own reported number digit-for-digit. At
`k=2` the wrong-sign residual is
`4γ(γn-γ-n+1)/n`, an `n`-dependent polynomial, also fully consistent
with "increasingly complex nonzero residuals" as the predecessor
described for `k\ge2`. This is strong, concrete (not merely
suggestive) evidence that the predecessor's own Charlier
implementation had a sign-convention bug, and that neither the
predecessor nor their dedicated referee (who re-read, rather than
independently re-derived, this specific sub-claim — see the referee
report §(g)) caught it.

> **[Correção, 2026-08-29 — referee hostil, wave 29
> `DIAGONAL-2F0-SUM-ATTEMPT`]** "neither the predecessor... caught it"
> acima leva a caracterização um pouco longe demais: a própria prosa
> do predecessor já suspeitava, em termos gerais, "provável divergência
> de sinal/convenção" para o resíduo observado — apenas nunca testou
> essa hipótese explicitamente. O achado central desta frente (o bug de
> sinal concreto, identificado e confirmado byte-a-byte contra o script
> `01` do predecessor pelo referee hostil desta própria frente) continua
> válido e sobrevive ao escrutínio; apenas a frase "não capturado por
> ninguém" é imprecisa — deveria ler "suspeitado em termos gerais pelo
> predecessor, mas nunca testado ou confirmado, por nenhum dos dois."
> Não afeta nenhuma conclusão matemática desta frente. Ver
> `adversarial/REFEREE_REPORT.md`.

**Why the corrected identification still does not unlock the diagonal
sum.** `S_n(γ)`, in Charlier language, is exactly

`S_n(γ) = \sum_{k=1}^n (1-γ)^k\,C_k\big(k-(n+1);\;a\big)`,  `a=(1-γ)n/γ` fixed,

a sum over **both** degree `k` and evaluation point `x_k=k-(n+1)`
increasing together at the same rate (`k-x_k = n+1`, constant) — a
genuine "anti-diagonal" or "codiagonal" sum of a classical orthogonal
polynomial family, at *fixed* auxiliary parameter `a`. This front
attempted the natural next step: express `C_k(x_k;a)` via the Charlier
EGF `\sum_kC_k(x;a)t^k/k!=e^t(1-t/a)^x` and a Cauchy coefficient
extraction, `C_k(x_k;a)=\dfrac{k!}{2\pi i}\oint\dfrac{e^t(1-t/a)^{x_k}}{t^{k+1}}dt`.
Because `x_k` is itself linear in `k`, this factors as
`(1-t/a)^{x_k}=(1-t/a)^{-(n+1)}\cdot(1-t/a)^k`, turning the diagonal
sum into `\sum_k k!\,z(t)^k` for `z(t):=(1-γ)(1-t/a)/t` (after
absorbing the `(1-γ)^k` prefactor) — a **factorially divergent**
(Borel-type, not ordinarily-convergent) power series in `k`, precisely
because `C_k` is only an *exponential*-generating-function object in
its degree; there is no elementary closed form for
`\sum_k k! z^k` (it is only Borel-summable, `=\int_0^\infty
\frac{e^{-t}}{1-zt}dt` formally). **This is a structural, not merely
practical, obstruction**: the standard Charlier-EGF route to diagonal
sums runs into exactly the same factorial-growth wall that makes `2F0`
a divergent hypergeometric series in general (it converges here only
because the sum over `m` inside each `A_k` terminates at `m=k` — the
outer sum over `k` itself has no such protection). This front did not
find a way around this wall via the Charlier route in the time
available; recorded as a genuine dead end for this specific technique,
not a claim that no technique can work.

---

## §3 Route 1(a): the double-sum reformation of `S_n` (scripts `03`, `04`, `06`, `07`)

**A different manipulation, not using Charlier at all: swap the order
of summation in the original `k,m` double sum.** Writing
`S_n':=S_n+1=\sum_{k=0}^n A_k` (including the trivial `A_0=1` term to
avoid an off-by-one), and using `P_{k,m}=(n-k+1)_m/n^m` (Lemma 1,
cited), then substituting `j=k-m`:

> **New exact identity (this front, PROVED, script `03` Part A).**
> `S_n' = \sum_{m=0}^n \dfrac{γ^m}{n^m}\,m!\,T(n,m)`,
> `T(n,m):=\sum_{j=0}^{n-m}\binom{j+m}{m}\binom{n-j}{m}(1-γ)^j`.

Verified exactly (16 exact-`Fraction` checks, `n\in\{3,5,8,12\}`,
4 rational `γ`): **0 mismatches**.

**A genuinely new sub-identity found en route (script `03` Part B).**
At the pure combinatorial level (weight `\equiv1`, i.e. the `j`-sum
without the `(1-γ)^j` factor), `T(n,m)` collapses via a classical
Vandermonde-type binomial convolution — the Cauchy product of two
copies of the negative-binomial generating function
`(1-x)^{-(m+1)}`:

> `\sum_{j=0}^{n-m}\binom{j+m}{m}\binom{n-j}{m} = \binom{n+m+1}{2m+1}`,

verified symbolically and numerically for all `0\le m\le n\le8` (44
cases, script `03` Part B): **0 mismatches**. This exact identity
appears nowhere in this lineage's prior work (checked: none of the
five required-reading documents mentions a Vandermonde-type
convolution).

**The weighted (`γ`-general) case does not collapse the same way** —
the finite `j`-sum `T(n,m)` is a genuinely truncated negative-binomial
series (no elementary closed form in general; this is the same class
of object, an incomplete-Beta-function-type partial sum, that
resisted closure elsewhere in this front's exploration too). This
front instead tested the natural approximation of **extending the
`j`-sum to infinity**, `T_\infty(n,m):=[y^m](1+y)^{n+m+1}/(y+γ)^{m+1}`
(a coefficient-extraction form obtained by summing the geometric-type
series `\sum_j\binom{j+m}{m}u(y)^j=(1-u(y))^{-(m+1)}`, `u(y):=(1-γ)/(1+y)`,
for `|y|` small). **Numerically (script `03` Part C/C2), the relative
error `|T_\infty-T|/T` shrinks extremely fast as `n` grows at fixed
`m` — consistent with an error exponentially small in `n-m`** — but at
`n=20,m=6,γ=0.2` (where `m` is a sizeable fraction of `n`) the
approximation is badly wrong (relative error `\approx9\times10^3`),
confirming this approximation is legitimate **only** in the regime
`m\ll n` that matters for `S_n'` (`m\le k\le K\sim\sqrt{n\ln n}`, per
Lemma 3, cited). **No rigorous bound on this truncation error was
derived** (a Cauchy-estimate bound is sketched in this front's working
notes but not completed to a clean closed form) — reported honestly as
numerically-supported, not proved; see §6 (open items).

---

## §4 Why the double-sum reformation does not reduce the difficulty
## (scripts `04`, `06`, `07`)

**Empirical shape of the swapped sum (script `04`).** Computing
`\text{term}_m:=(γ^m/n^m)\,m!\,T(n,m)` exactly (rational arithmetic)
across `m=0,\ldots,60` at `n\in\{50,200,800\}`, `γ=1/2`:
`\text{term}_m` is **monotonically decreasing** in `m` from its value
at `m=0` (`\approx1/γ`), but decays *slowly* — at `n=800`, `m=60` is
still at `\approx0.2\%$` [**Correção, 2026-08-29 — referee hostil**: o
valor correto, lido diretamente do próprio `script 04`'s dados, é
`0{,}11\%`, não `\approx0{,}2\%` (`\approx1{,}8\times` de diferença) —
não afeta a conclusão qualitativa ("ainda não desprezível") nem
nenhum resultado quantificado em §4/§6. Ver
`adversarial/REFEREE_REPORT.md`.] of the peak value, not yet negligible; the
`m`-range needed to reach genuine decay **grows with `n`**, not fixed.
This already suggests the swap has not produced an "easy," `O(1)`-wide
sum.

> **Quantified finding (this front, proved for the leading local rate,
> script `07`; the full Gaussian-shape claim numerically supported,
> script `06`).** The local decay rate
> `c(n,γ):=-\log(\text{term}_1/\text{term}_0)\cdot n` converges, as
> `n\to\infty` at fixed `γ`, to the **exact** limit
> `c(γ) = \dfrac{2(1-γ)}γ`,
> proved symbolically (script `07`: exact closed forms for
> `\text{term}_0(n,γ)=(1-(1-γ)^{n+1})/γ` and `\text{term}_1(n,γ)`,
> exponentially-small-in-`n` terms dropped, then
> `n\log(\text{term}_0/\text{term}_1)\to2(1-γ)/γ` taken as an ordinary
> rational-function limit) and matching, to the digits shown, the
> independently-fitted numeric rate at `n=400,1600,6400` for three
> sample `γ` (script `06`; e.g. `γ=1/2`: fitted `2.00031\to` predicted
> `2`; `γ=1/5`: fitted `8.00500\to` predicted `8`; `γ=7/10`: fitted
> `0.85720\to` predicted `0.857143`).

This is consistent with (and, for the leading local rate, proves) a
Gaussian envelope `\text{term}_m\sim\text{term}_0\cdot
e^{-c(γ)m^2/(2n)}` for `m=O(\sqrt n)` — i.e. **the swapped `m`-sum has
the same `Θ(\sqrt n)` characteristic scale as the original `A_k\sim
e^{-βk^2/n}` profile**, merely with a *different* constant
(`c(γ)=2(1-γ)/γ` versus the original `β=γ(2-γ)/2` — these are not
proportional to one another, e.g. at `γ=1/2`: `c=2`, `β=0.375`, ratio
`5.33`; at `γ=0.7`: `c=0.857`, `β=0.455`, ratio `1.88` — so the swap
genuinely redistributes the sum's mass, it does not merely relabel
it). **The practical consequence: any rigorous asymptotic treatment of
`\sum_m\text{term}_m` to the precision needed for `C(γ)` would require
a Laplace/Gaussian-sum analysis of comparable depth to the moment/
cumulant machinery already used and found insufficient (Gap 1) by five
prior fronts — this reformation is not a shortcut.** This is reported
as a genuine, informative structural finding, precisely because it
forecloses (with reasons, not just failure-to-find) the most natural
next thing a future front would try along this exact path.

---

## §5 Independent numerical cross-check via the new route (script `05`)

As a check that the double-sum reformation is not just formally
correct but *usable*, and as independent supporting evidence for the
standing `T(γ)`/`C(γ)` conjectures via a **computational algorithm no
ancestor used** (every prior front's high-`n` numerics summed over `k`
directly; this sums over `m`), this front computed `S_n` via
`\sum_m\text{term}_m` (mpmath, dps `40`, exact `T(n,m)` — **not** the
`T_\infty` approximation of §3, to avoid conflating two separate
approximations) at `n=200,\ldots,3200`, `γ=1/2`:

| `n` | `R(n):=φ(n,γn)/φ_\infty(γn)` | `R-T(γ)` | `\sqrt n(R-T(γ))` |
|---|---|---|---|
| 200 | 1.1321559951 | −2.25e−02 | −0.318828 |
| 400 | 1.1386684891 | −1.60e−02 | −0.320641 |
| 800 | 1.1433186008 | −1.14e−02 | −0.321930 |
| 1600 | 1.1466294256 | −8.07e−03 | −0.322845 |
| 3200 | 1.1489819366 | −5.72e−03 | −0.323493 |

2-point Richardson extrapolation (`n=1600,3200`, model
`x_n=C+b/\sqrt n`, matching this lineage's own established
extrapolation convention): `C_{\text{extrap}}=-0.325058`, versus the
closed form `C(0.5)=-0.325064` — **agreement to `6\times10^{-6}`**, via
a route that shares no code or algorithm with any ancestor's
computation of `S_n`. Cross-validated against a fresh, independently
written direct `k`-sum evaluator (same script, separate function) at
`n=50,100`: agreement to `\sim10^{-31}` (dps-`40` roundoff floor),
confirming the swap-sum implementation itself is correct, not merely
"close by luck" at the Richardson-extrapolated scale.

**Status: numerical evidence, not proof** — same standing as the
ancestor lineage's own numerics for `C(γ)` (Estágio 26 §6, wave-17
§7.3). It does newly confirm that the double-sum machinery of §3–§4 is
internally consistent and could, in principle, form the numerical
backbone of a future front's work, even though this front did not
push it to a closed-form or rigorous asymptotic result.

---

## §6 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed, NOT bounded, and
   NOT characterized as a convergent series with a proved remainder.**
   No progress beyond the predecessor's own honest non-closure.
2. **The diagonal `2F0`/Charlier sum (§2) remains unclosed.** The
   Charlier identification is now confirmed exact, but the natural
   EGF/Cauchy-extraction route to it is shown (§2, this front) to hit a
   factorial-divergence wall structurally, not just practically —
   named here as a genuine dead end for *this* technique, though not a
   proof that no technique using the Charlier structure could work
   (e.g., a Borel-summation-aware treatment of the divergent series was
   not attempted).
3. **The double-sum reformation (§3) does not, by itself, reduce the
   asymptotic difficulty** — quantified precisely in §4. A future front
   pursuing this exact path should expect to need Laplace-method work
   on the `m`-sum of comparable depth to the existing `k`-sum
   machinery, not a shortcut.
4. **No rigorous bound on the `T(n,m)\to T_\infty(n,m)` truncation
   error (§3) was derived** — only numerically supported (shrinking
   fast for `n\gg m`). A Cauchy-estimate-based bound looks achievable
   (sketched, not completed) and is named here as concrete unfinished
   work for a future front, more tractable-looking than closing `C(γ)`
   itself.
5. **Route 2 (a technique bypassing the `A_k`/`2F0` machinery entirely
   — e.g. a differential-equation-in-`n` recursion for `S_n`, or a
   Watson's-lemma treatment of a wholly different integral
   representation) was NOT attempted** by this front; all of the
   effort here builds on and extends the `A_k`/`2F0` structure (Route
   1). This is disclosed as a genuine scope limitation, not a claim
   that Route 2 was tried and failed.
6. **Gap 1 and Gap 3** (THEOREM.md, Estágio 26/33 onward) remain
   exactly as the predecessor left them — untouched by this front,
   whose entire effort was on the `2F0`/double-sum lead specifically,
   not on the moment/cumulant `n_0(γ)`-tightening machinery.
7. **The general-`m` Gaussian-envelope claim of §4 is proved only at
   the leading local rate (`m=0\to1`)**, not as a uniform statement for
   all `m=O(\sqrt n)` — the numeric fit (script `06`) and the shape
   probe (script `04`) support it strongly but a full proof (e.g. via
   the exact alternating-sum closed form for `T_\infty(n,m)`, script
   `03`'s Part C derivation) was not carried out for general `m`.

---

## §7 Self-caught issues

1. **Dead/no-op code in script `03`'s first draft (caught before
   running, by inspection).** An early version of
   `S_n_prime_via_swap` accumulated two `+0` terms from a half-written
   refactor (computing `\binom mm\cdot0` and `1\cdot0` explicitly).
   These are mathematically inert (add exactly zero) so no numeric
   result was ever wrong, but the code was cleaned up before running
   any check, for clarity and to avoid confusion on re-read.
2. **`Fraction`-based arithmetic infeasible at the `n` needed for
   script `06` (caught before running, by estimation, not by a failed
   run).** Script `06` initially followed scripts `03`/`04`'s exact-
   `Fraction` pattern for `T(n,m)`; before running it at the target
   `n` (up to `6400`), it was recognized that `(1-γ)^j` for `γ` with
   denominator `10` and `j` up to `\sim6400` produces a `Fraction` with
   a `\sim10^{6400}`-digit denominator — computationally infeasible.
   Switched to `mpmath` (dps `40`) for this script, and — because this
   removes the exact-rational safety net the rest of this front relies
   on — added an explicit cross-check (script `06` Part 0) confirming
   the `mpmath` evaluator reproduces the exact-`Fraction`
   `\text{term}_m` values from script `04` to `<10^{-9}` absolute error
   at `n=50,γ=1/2,m=0..5` (0/6 mismatches) before trusting any
   larger-`n` output from it.
3. **Scrutiny of script `05`'s early-stopping cutoff.** `05`'s
   `S_n_prime_swap` stops accumulating once a term falls below
   `10^{-30}` of the running total (`m>20` guard). Given §4's finding
   that `\text{term}_m` decays only like a Gaussian of width
   `\sim\sqrt{n/c(γ)}`, this cutoff triggers at `m` in the many
   hundreds for `n=3200`, not at a suspiciously small `m` — checked
   directly (companion diagnostic, not saved as a numbered script:
   continuing the `n=3200,γ=1/2` sum for `100` further terms past the
   early-stop point changes the total by an amount consistent with the
   dps-`40` precision floor, not a truncation artifact) before trusting
   the §5 table's `n=3200` row.
4. **No other computational bugs found.** Every exact claim in §2–§4
   was checked at least two independent ways (symbolic vs. numeric
   exact-`Fraction`; the swapped-sum identity vs. a fresh direct-`k`-sum
   evaluator; the fitted Gaussian rate vs. an independent symbolic
   derivation of the same limit).

---

## §8 Scorecard

| Claim | Status |
|---|---|
| Charlier identification `A_k=(1-γ)^k C_k(k-n-1;(1-γ)n/γ)` (DLMF sign convention) | **PROVED** (§2, script `02`; symbolic `k=0..6` + 50 exact numeric spot checks) |
| Diagnosis that the predecessor's `-2γ` residual is reproduced exactly by a specific sign-convention bug | **STRONGLY EVIDENCED** (§2, script `02` Parts B/C) — a correction to the predecessor's (and its referee's) record, not itself a new obstruction |
| Charlier-EGF/Cauchy-extraction route to the diagonal sum hits a factorial-divergence wall | **SHOWN** (structural argument, §2) — not a proof no Charlier-based technique can work |
| Double-sum swap identity `S_n'=\sum_m(γ^m/n^m)m!\,T(n,m)` | **PROVED** (§3, script `03` Part A; 16 exact checks) |
| Vandermonde-type convolution `T(n,m)|_{\text{weight}=1}=\binom{n+m+1}{2m+1}` | **PROVED** (§3, script `03` Part B; 44 exact checks) — new to this lineage |
| `T(n,m)\to T_\infty(n,m)` (extend-to-infinity) approximation valid for `m\ll n` | **numerically supported only**, not proved (§3, script `03` Part C/C2) |
| Swapped `m`-sum has the same `Θ(\sqrt n)` Gaussian scale as the original `k`-sum | **quantified**: leading local rate `c(γ)=2(1-γ)/γ` PROVED (script `07`); full Gaussian-envelope shape numerically supported (scripts `04`,`06`) |
| Swap-route independent numerical reproduction of `T(γ)`,`C(γ)` | **CONFIRMED numerically** (§5, script `05`; Richardson-extrapolated `C_{\text{est}}=-0.325058` vs. closed form `-0.325064`) — evidence, not proof |
| **The diagonal `2F0` sum `S_n(γ)`** | **NOT CLOSED** |
| **`C(γ)` for `γ\in(0,1)`, the ultimate target** | **remains entirely OPEN** |

---

## Seeds

| Block | Status |
|---|---|
| `20260943000–20260943999` (this front's reservation, `DISC-DEC-134`, wave 29 frente b) | grep-confirmed **unused** before any code was written (only a coincidental digit substring inside an unrelated `COSMOLOGY_WIDE_BINARIES` JSON file, and the `DECISION_LEDGER.yaml` reservation line itself) — two seeds drawn from this block, both disclosed below; every other quantitative claim in this front is exact symbolic algebra (`sympy`), exact rational arithmetic (`Fraction`), or deterministic high-precision numerics (`mpmath`, dps `40`) |
| `random.seed(20260943001)` (script `01`, Part C numeric spot-check, 60 points) | from the reserved block |
| `random.seed(20260943002)` (script `02`, Part D numeric spot-check, 50 points) | from the reserved block |

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_baseline_2f0_identity.py`/`.log` | fresh, independent re-verification of the predecessor's `A_k=(1-γ)^k\,{}_2F_0(-k,n-k+1;;w)` identity (Pochhammer rewriting + symbolic + 60 exact numeric checks) |
| `02_charlier_identity_correction.py`/`.log` | the corrected Charlier identification (DLMF sign convention), symbolic + 50 exact numeric checks; reproduction of the predecessor's `-2γ` residual via the wrong-sign variant |
| `03_double_sum_swap.py`/`.log` | the exact double-sum swap identity; the Vandermonde-type convolution sub-identity; the extend-to-infinity approximation and its numerically-observed error behavior |
| `04_m_sum_shape_probe.py`/`.log` | empirical profile of `\text{term}_m` vs. `m`; confirms slow, non-`O(1)`-width decay |
| `05_swap_route_independent_numerics.py`/`.log` | independent numerical computation of `S_n`/`T(γ)`/`C(γ)` via the swap route, mpmath dps 40, `n` up to 3200, Richardson extrapolation, cross-check vs. a fresh direct-`k`-sum evaluator |
| `06_m_sum_gaussian_width_fit.py`/`.log` | numeric fit of the `\text{term}_m` local decay rate `c(n,γ)`, converging to `2(1-γ)/γ` |
| `07_symbolic_width_confirmation.py`/`.log` | symbolic (sympy) proof that the `m=0\to1` local decay rate converges exactly to `2(1-γ)/γ` |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
