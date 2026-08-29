# ATTEMPT — Route 2: bypassing the `A_k`/`2F0` machinery entirely for
# `C(γ)`, `γ∈(0,1)`

**Wave 30, front (a), `ROUTE2-BYPASS-ATTEMPT`, authorized by
`DISC-DEC-138`.** Mandate: attempt a genuinely different — not
`A_k`/`2F0`-machinery-decorating — technique for `C(γ)`, `γ∈(0,1)`, the
open second-order term of the γ-scaling law, after the immediate
predecessor (wave 29 front b) explicitly named "Route 2" (bypassing the
`A_k`/`2F0` structure entirely) as the single unexplored direction left
in this sub-lineage, having exhausted two routes *within* that structure
(the Charlier identification and the double-sum swap), both hitting
distinct-but-related structural walls.

---

## VERDICT (up front)

> **`C(γ)` for `γ∈(0,1)` remains ENTIRELY OPEN.** This front pursued
> Route 2 genuinely — every result below is derived from mathematical
> objects (a *different* hypergeometric family, a *different*,
> genuinely more primitive random variable, and an empirical
> holonomicity test) that no ancestor or predecessor ever wrote down —
> and it does **not** close `C(γ)`. What it delivers, all independently
> verified against fresh code:
>
> 1. **A new exact structural fact, PROVED, genuinely different from
>    the predecessor's `2F0`/Charlier object.** The predecessor's own
>    PROVED double-sum-swap kernel `T(n,m)` (weighted case, which the
>    predecessor explicitly reported "has no elementary closed form in
>    general") **is exactly a terminating Gauss hypergeometric `2F1`**:
>    `T(n,m) = \binom nm\,{}_2F_1\!\big(-(n-m),\,m+1;\,-n;\,1-γ\big)`,
>    confirmed by an exact ratio test (symbolic) and 80 fresh exact-
>    `Fraction` numeric spot checks, 0 mismatches. This is a `2F1`
>    (Gauss), not the predecessor's diagonal `2F0` — a genuinely
>    different classical hypergeometric family, with different (and, in
>    principle, richer) transformation theory.
> 2. **A new exact PROBABILISTIC fact, PROVED — the "more primitive
>    random object" the mandate's option (iii) asked for, found.**
>    `T(n,m)`'s normalized kernel `p_m(j) := \binom{j+m}m\binom{n-j}m /
>    \binom{n+m+1}{2m+1}` is **exactly** the pmf of the **median**
>    (middle order statistic) of a uniform random `(2m+1)`-subset drawn
>    **without replacement** from `\{1,\ldots,n+m+1\}` — a classical,
>    well-studied discrete distribution, confirmed against the standard
>    order-statistic pmf formula (106 exact checks, 0 mismatches) and
>    its classical exact mean/variance formulas (cross-checked against
>    brute-force summation, 0 mismatches). This is a genuinely different
>    — and more primitive — random variable than the `M∼\mathrm{Bin}(k,γ)`
>    count that every prior front's moment/cumulant machinery is built
>    on.
> 3. **A new closed-form asymptotic scaling law for this object's
>    large-deviations saddle point, derived and numerically confirmed
>    to sub-percent accuracy and tightening as `n,m→∞`.**
>    `T(n,m)`, in this language, is a **tilted** (not central) moment of
>    the median — the true maximizer `j^*` of the sum is *not* near the
>    untilted mean `(n-m)/2` for any `γ` not extremely close to `1`,
>    i.e. this is a genuine large-deviations object. Leading-order
>    calculus on the exact discrete crossing condition, in the regime
>    `m=o(n)` that matters for `S_n`, gives `j^*\sim m(1-γ)/γ` as
>    `m,n\to\infty`; confirmed to `<0.35\%` relative deviation already at
>    `n=4\times10^6,m\sim632` at all four sample `γ` tested, tightening
>    as `n,m` grow further (one small non-monotonic step at `γ=0.9`,
>    traced to integer rounding at very small absolute `j^*`, not a
>    failure of the scaling law — see §4).
> 4. **A genuinely orthogonal empirical test (Route 2(i), the
>    difference-equation route), with an honest NEGATIVE result.**
>    `S_n(γ)`, at two independent fixed rational `γ` (`1/2` and `1/3`),
>    was tested — via exact rational linear algebra, not floating-point
>    curve-fitting — for a low-order linear P-recursion in `n`
>    (`\sum_ip_i(n)S_{n+i}=0`, `p_i` polynomial). **No such recursion
>    was found** for any order `\le4` and per-coefficient degree `\le5`
>    at `γ=1/2` (20 `(r,d)` combinations), nor for order `\le3`/degree
>    `\le4` at `γ=1/3` (12 more), in every one of the 32 tested
>    combinations, each fit over-determined by 6 extra equations (a true
>    "zero nontrivial nullspace" result, not a near-miss). This is a
>    genuinely different
>    kind of evidence (creative-telescoping/holonomicity theory, not
>    analytic asymptotics) independently supporting the "diagonal, not
>    reducible to a low-complexity object in `n` alone" diagnosis this
>    front reaches from two other angles too.
>
> **None of these four findings, individually or combined, closes
> `C(γ)`.** Assembling the full asymptotic of `S_n` through the new
> `2F1`/order-statistic route (finding 1–3) requires a genuine **joint
> two-variable** (`m` and `j`) Laplace/saddle-point analysis; this front
> located the saddle-point scaling law (finding 3) but did **not**
> carry the analysis through to the needed sub-leading order — this is
> disclosed explicitly, not glossed over, in §5. **The central honest
> finding of this front is that a THIRD, genuinely independent lens on
> this exact same finite sum `S_n(γ)` — reached via completely different
> mathematical objects (Gauss hypergeometric functions and order
> statistics of finite sampling, as opposed to the predecessor's
> `2F0`/Charlier polynomials and Binomial cumulants) — lands on a
> problem of the same qualitative shape and comparable technical depth
> as the moment/cumulant machinery that six prior fronts have already
> found insufficient.** No claim of progress on any Millennium Problem;
> pure combinatorial/asymptotic mathematics internal to this archive,
> about a specific random-permutation-with-reroutes ensemble.

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or
code was written**, in the order specified by the dispatching mandate:

1. `.../gamma_c_gamma_construction_attempt/diagonal_2f0_sum_attempt/ATTEMPT.md`
   (501 lines, the immediate predecessor, wave 29 front b) — read in
   full. Its central findings (quoted, not re-derived): the exact
   Charlier identification `A_k(n,γ)=(1-γ)^kC_k(k-n-1;(1-γ)n/γ)` (DLMF
   convention, a corrected record); the Charlier-EGF/Cauchy-extraction
   route hitting a genuine factorial-divergence (Borel-type) wall; the
   double-sum-swap identity `S_n'=\sum_m(γ^m/n^m)m!\,T(n,m)`,
   `T(n,m):=\sum_j\binom{j+m}m\binom{n-j}m(1-γ)^j` (PROVED), and its
   `Θ(\sqrt n)`-scale characteristic width (rate `c(γ)=2(1-γ)/γ`,
   PROVED for the leading local term). "Route 2," a technique bypassing
   the `A_k`/`2F0` machinery entirely, explicitly named as
   not-attempted.
2. `THEOREM.md` — **Estágio 26** (`C(γ)` first named; `D_0(γ)` PROVED;
   `E_{\text{heuristic}}(γ)` order-2 cumulant heuristic); **Estágio 51**
   (the `2F0` fact, wave 28); **Estágio 52** (the immediate
   predecessor's integration: both structural walls, the Charlier
   correction, Route 2 named as the open direction) — all three read in
   full.
3. `.../gamma_c_gamma_construction_attempt/ATTEMPT.md` (643 lines, wave
   28 front b, grandparent) — read in full, for the exact
   `E_{\text{heuristic}}(γ)` order-6 Taylor/cumulant machinery (§5), the
   exact moment/cumulant apparatus (§3), and the original (uncorrected)
   Charlier attempt (§2, later corrected by the predecessor).
4. `.../gamma_second_order_attempt/ATTEMPT.md` (633 lines,
   great-great-grandparent) — read in full, for Lemma E (PROVED), the
   `D_0(γ)` derivation via Poisson summation (§3), and the original
   order-2 cumulant-expansion heuristic (§4) this whole line targets a
   rigorous version of.
5. `.../gamma_scaling_attempt/ATTEMPT.md` (592 lines, wave 17 front e,
   ultimate ancestor) — read in full, for Lemma 1's exact combinatorial
   proof and the precise definitions `A_k`, `P_{k,m}`, `S_n:=\sum_kA_k`,
   `φ(n,γn)`.

**No `.py` file of any ancestor or predecessor was opened, read, or
imported anywhere in this front.** Every script below (`01`–`06`) is
written fresh from the mathematical prose cited above. Every fact
borrowed from a predecessor's own PROVED result — the double-sum-swap
identity `S_n'=\sum_m(γ^m/n^m)m!T(n,m)` itself, and the predecessor's
own PROVED unweighted Vandermonde-type identity
`\sum_j\binom{j+m}m\binom{n-j}m=\binom{n+m+1}{2m+1}` — is **independently
re-derived and re-verified from scratch** in this front's own script
`01` (the swap identity) and script `03` Part A (the Vandermonde
identity), before being built on; nothing is taken on faith from the
predecessor's own numbers.

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
PROVED, cited): for `γ\in(0,1]`, `n\varphi(n,γn)=S_n:=\sum_{k=1}^nA_k`,
and `C(γ)` (the open second-order term of the γ-scaling law,
`\sqrt n(\varphi(n,γn)/\varphi_\infty(γn)-T(γ))\to C(γ)`,
`T(γ):=\sqrt{2/(2-γ)}`) is equivalent (Lemma E, PROVED) to
`S_n=G_n+D(γ)+o(1)`, `G_n:=\tfrac12\sqrt{πn/β}`, `β:=γ(2-γ)/2`,
`D(γ)=D_0(γ)+E(γ)`, with `D_0(γ)=(γ-1)/(2(2-γ))` PROVED (Lemma D0) and
`E(γ)` — conjectured to equal
`E_{\text{heuristic}}(γ):=\dfrac{-3γ^2+7γ-6}{6(γ-2)^2}` — the open "hard
half."

**The predecessor's PROVED double-sum-swap identity, re-derived fresh
here (script `01` Part B, own code, 12 exact checks, 0 mismatches),
is this front's starting point:**

`S_n'(γ):=1+S_n(γ) = \sum_{m=0}^n\dfrac{γ^m}{n^m}\,m!\;T(n,m)`,
`\quad T(n,m):=\sum_{j=0}^{n-m}\binom{j+m}m\binom{n-j}m(1-γ)^j`.

The predecessor showed `T(n,m)` has "no elementary closed form in
general" for `γ\ne1`, and that a naive swap of summation order retains
the same `Θ(\sqrt n)`-scale Gaussian structure as the original `k`-sum.
**This front's mandate: find genuinely new mathematical objects — not
further algebraic reshuffling of the same exact finite sum — that
illuminate or advance `T(n,m)`/`S_n` beyond what the predecessor's
`A_k`/`2F0`/Charlier lens could reach.**

---

## §2 A genuinely different hypergeometric identification: `T(n,m)` is
## a terminating Gauss `2F1` (script `02`)

**New exact fact (this front, PROVED).**

`T(n,m) = \binom nm\;{}_2F_1\!\big(-(n-m),\,m+1;\,-n;\,1-γ\big)`,
a **terminating Gauss hypergeometric series** (upper parameter
`-(n-m)` is a nonpositive integer for `m\le n`).

*Derivation.* The summand `t_j:=\binom{j+m}m\binom{n-j}m(1-γ)^j` has
term ratio (symbolic, sympy, script `02` Part A)

`\dfrac{t_{j+1}}{t_j} = \dfrac{(j+m+1)(j+m-n)}{(j+1)(j-n)}(1-γ)`,

which matches, **exactly** (symbolic difference `0`), the canonical
ratio of a `2F1(A,B;C;z)` term with `A=-(n-m)`, `B=m+1`, `C=-n`,
`z=1-γ`. This is a genuine new identification: `2F1` (Gauss), not the
predecessor's `2F0`. It is qualitatively different machinery because a
terminating `2F1` — unlike `2F0`, which has no elementary closed
generating-function/EGF identity at fixed argument and drifting degree
— sits inside the extremely well-developed classical theory of Gauss
hypergeometric functions: Euler/Pfaff transformations, contiguous
relations, and (for the *non*-degenerate case) Euler's integral
representation.

**Verified two independent ways, both exact:**
(i) a fresh finite-Pochhammer-sum sympy evaluator (script `02` Part B,
44 `(n,m)` pairs, `n\le8`, `γ=3/10`): 0 mismatches, **after** this
front caught and fixed its own bug in this exact check (see §6 item 1);
(ii) a completely separate, from-scratch exact-`Fraction`
terminating-`2F1` evaluator, no sympy at all (script `02` Part C, 80
checks across `n\in\{4,6,9,11,14\}`, `m\in\{0,1,2,3\}`,
`γ\in\{1/3,3/10,7/20,1/2\}`): 0 mismatches.

**Why Euler's integral representation does NOT directly apply, and why
that matters.** Euler's classical integral,
`{}_2F_1(A,B;C;z)=\frac{\Gamma(C)}{\Gamma(B)\Gamma(C-B)}\int_0^1t^{B-1}(1-t)^{C-B-1}(1-zt)^{-A}dt`,
requires `\mathrm{Re}(C)>\mathrm{Re}(B)>0`. Here `C=-n` is a
*nonpositive integer* — `\Gamma(C)` has a pole, and the representation
does not apply as stated. This is not a minor technicality: it is the
`2F1` analogue of exactly the same obstruction (a negative-integer
parameter placed where the classical convergent-integral machinery
needs a positive one) that made the predecessor's Charlier-EGF route
factorially divergent. A genuine fix (e.g. a Pfaff-type transformation
swapping which parameter plays the role of the negative integer, since
`A=-(n-m)` is *also* a nonpositive integer, `m\le n`) was identified as
the natural next step but **not carried through to a usable integral**
in the time available — named honestly in §5 as unfinished, concrete,
plausibly tractable work for a future front, not glossed over.

---

## §3 A genuinely different — and more primitive — random object:
## `T(n,m)` as a tilted order-statistic moment (script `03`)

Rather than pursue the `2F1` integral representation further, this
front instead asked the mandate's option-(iii) question directly: what
random object *more primitive* than `M\sim\mathrm{Bin}(k,γ)` is
`S_n`/`T(n,m)` secretly an expectation over? The answer, found and
proved exactly:

> **New fact (this front, PROVED, script `03` Part A/B).** Normalizing
> by the predecessor's own PROVED Vandermonde-type identity (cited,
> **independently re-verified here**, 119 fresh exact checks, 0
> mismatches), `p_m(j):=\binom{j+m}m\binom{n-j}m/\binom{n+m+1}{2m+1}` is
> a genuine probability distribution on `j=0,\ldots,n-m`, and it is
> **exactly** the pmf of the `(m+1)`-th order statistic (the **median**)
> of a uniform random `(2m+1)`-element subset of `\{1,\ldots,n+m+1\}`
> drawn **without replacement**, via `v=j+m+1`. Confirmed against the
> classical order-statistic pmf formula
> `P(X_{(r)}=v)=\binom{v-1}{r-1}\binom{N-v}{s-r}/\binom Ns`
> (`N=n+m+1`, `s=2m+1`, `r=m+1`): 106 exact-`Fraction` checks, 0
> mismatches.

So `T(n,m) = \binom{n+m+1}{2m+1}\,E\big[(1-γ)^{X-m-1}\big]`, `X` the
median of a random subset — a genuinely different, and more primitive,
random variable than any Binomial count used anywhere else in this
lineage.

**Exact mean and variance (script `03` Part C).** By the manifest
symmetry `p_m(j)=p_m(n-m-j)` (checked directly, 64 exact checks, 0
mismatches) and the classical closed forms for order-statistic moments
of sampling without replacement (`E[X_{(r)}]=r(N+1)/(s+1)`,
`\mathrm{Var}[X_{(r)}]=r(s+1-r)(N+1)(N-s)/((s+1)^2(s+2))`, symbolically
simplified via sympy and cross-checked against brute-force exact
summation, 12 `(n,m)` pairs, 0 mismatches):

`E[j] = \dfrac{n-m}2, \qquad \mathrm{Var}[j] = \dfrac{(n+m+2)(n-m)}{4(2m+3)}.`

**`T(n,m)` is a large-deviations, not a CLT-regime, object (script `03`
Part D).** `E[(1-γ)^j]` is an exponential-family moment evaluated at
the *fixed* point `\ln(1-γ)`, not a small perturbation near `0` — the
true maximizer `j^*` of the tilted summand need not be near the
untilted mean `(n-m)/2` at all. Located exactly (exact-`Fraction`
ratio-crossing test) at `n=400`, `m\in\{5,10,20\}`, `γ\in\{0.3,0.5,0.9\}`:
at `γ=0.9`, `j^*` collapses to essentially `0` (e.g. `j^*=0`–`2`,
`\ll(n-m)/2\approx190`); at `γ=0.3`, `j^*` stays a much larger fraction
of the untilted mean (`10$–`20\%` of it) but is still far from it. This
rules out any naive "expand near the mean" shortcut for this object —
confirming (via a completely different, order-statistic-theoretic
argument) the same qualitative obstruction the predecessor's Binomial-
cumulant machinery has faced all along, but reached here from first
principles about a *different* random variable.

---

## §4 A new closed-form scaling law for the saddle point (script `05`)

Pushing §3 Part D further: the exact discrete crossing condition for
`j^*` is `(j^*+m+1)(n-j^*-m)/[(j^*+1)(n-j^*)]\cdot(1-γ)=1`. In the
regime relevant to `S_n` (`m=o(n)`, and, as confirmed below, `j^*=O(m)`
too, so `j^*,m\ll n`), the factor `(n-j^*-m)/(n-j^*)=1+O(m/n)\to1`,
leaving, to leading order as `m,j^*\to\infty`,
`(j^*+m)/j^*\to1/(1-γ)`, i.e.

> **New scaling law (this front, derived; numerically confirmed to
> tighten as `n,m\to\infty`, script `05`).**
> `j^*(m,n,γ) \sim m\dfrac{1-γ}γ` as `m,n\to\infty` with `m=o(n)`.

Confirmed at four sample `γ\in\{0.5,0.3,0.9,0.2\}`, with `m` scaled
`\propto\sqrt n` (`m/\sqrt n\approx0.316` held fixed) across
`n=4\times10^3,4\times10^4,4\times10^5,4\times10^6` (own fresh exact-
`Fraction` ratio-crossing locator, re-implemented independently of
script `03`'s version): the relative deviation of `j^*/m` from the
predicted limit `(1-γ)/γ` shrinks at every `γ` as `n,m` grow, from
`2.5$–`10\%` at the smallest scale down to `0.08$–`0.32\%` at the
largest — e.g. `γ=0.5`: `5.0\%\to1.6\%\to0.5\%\to0.16\%`; `γ=0.9`:
`10.0\%\to14.3\%\to1.0\%\to0.32\%$` (the one non-monotone step, at
`γ=0.9` between the two smallest scales, occurs where absolute `j^*`
is tiny — `j^*=2\to6$ — so a single-unit integer-rounding effect is an
`O(1/j^*)=O(15$–`50\%)` correction, fully consistent with what is
observed; the trend is unambiguous and monotone once `j^*\gtrsim20`,
as seen at every other `γ`, and at `γ=0.9` itself from the third point
on). This is a genuinely new,
verified quantitative fact about the exponential tilting of the median
order statistic — structurally analogous in spirit to (but derived by
an entirely different method than) the predecessor's own
`c(γ)=2(1-γ)/γ` local-decay-rate finding for the outer `m`-sum (§4 of
the predecessor's `ATTEMPT.md`) — the two rate functions are **not**
the same closed form (`(1-γ)/γ` here vs. `2(1-γ)/γ` there), confirming
they are genuinely different objects, not a disguised restatement.

---

## §5 Why this does not, by itself, advance `S_n`/`C(γ)` further

**The honest diagnosis.** Assembling `S_n'=\sum_m(γ^m/n^m)m!\,T(n,m)`
via §2–§4's lens requires understanding `T(n,m)` — a tilted median-order-
statistic moment — uniformly across the **whole relevant range**
`m=O(\sqrt n)` (not just its leading-order saddle-point *location*,
found in §4, but the full Laplace/Gaussian *approximation* around that
saddle, to the precision needed for a `Θ(1)`-level second-order
constant), and then performing a **second**, outer Laplace/Gaussian
analysis over `m` itself (as the predecessor's own §4 already showed is
needed even after the swap, independently of this front's new
`2F1`/order-statistic reformulation). This is a genuine **two-variable
joint saddle-point problem** (`j$ and `m$ both `O(\sqrt n)$, coupled
through `T(n,m)$'s own `m$-dependence), of a technical depth this front
judges comparable to — not less than — the moment/cumulant machinery
(Gap 1) that six prior fronts (Estágios 33/36/37/49/51/52) have already
attacked and found insufficient. **This front did not carry the
two-variable analysis through**, for the same reason none of those six
fronts closed Gap 1 in one pass: it is genuinely substantial technical
work (uniform Laplace-method error control in two coupled variables,
not "more of the same" bookkeeping at one level deeper).

**What WOULD be needed to push this further (named precisely, for a
future front, matching this lineage's own convention of naming concrete
next steps rather than vague hope):**
1. A **uniform** (in `m=O(\sqrt n)`) Gaussian/Laplace approximation of
   `T(n,m)` around its saddle `j^*(m,n,γ)$ (§4), with an explicit,
   summable remainder bound — the direct `2F1$-analogue of the
   predecessor's Gap 1 (a Taylor-remainder-with-moments bound), but for
   the order-statistic tilted distribution instead of the Binomial.
2. A Pfaff-type hypergeometric transformation converting
   `{}_2F_1(-(n-m),m+1;-n;1-γ)$ into an equivalent representation with a
   **positive** (not `-n$) lower parameter, restoring access to Euler's
   integral representation (§2) — genuinely different, and possibly
   more tractable than a from-scratch Laplace analysis of the raw
   finite sum, but not attempted here.
3. Combining 1–2 with the already-established outer-`m$-sum Gaussian
   envelope (predecessor's §4, rate `c(γ)=2(1-γ)/γ$, PROVED for the
   leading local term) into a single joint two-dimensional Laplace
   computation.

None of this was completed. **`C(γ)` for `γ\in(0,1)` is NOT
constructed, NOT bounded, and NOT characterized as a convergent series
with a proved remainder** by this front, exactly as by every
predecessor since Estágio 26.

> **[Nota, 2026-08-29 — referee hostil, wave 30 `ROUTE2-BYPASS-ATTEMPT`]**
> The referee dispatched for this front carried §5 item 2's named
> "Pfaff-type fix" all the way through to a genuinely new, clean closed
> form that this front itself did **not** reach. Applying DLMF 15.8.7
> (`{}_2F_1(-N,b;c;z)=[(c-b)_N/(c)_N]\,{}_2F_1(-N,b;1+b-c-N;1-z)`,
> `N:=n-m`) to this front's own `T(n,m)={}_2F_1(-(n-m),m+1;-n;1-γ)`
> identity (§2) transforms the lower parameter to `1+b-c-N=2m+2` — a
> **manifestly positive integer for every `m\ge0`**, escaping the
> `C=-n` obstruction diagnosed in §2 — and, carrying this through
> Euler's integral representation on the transformed series (now valid)
> and simplifying the resulting Pochhammer/Gamma prefactors, yields
>
> `T(n,m) = \binom{n+m+1}{2m+1}\cdot E_{t\sim\mathrm{Beta}(m+1,m+1)}\big[(1-γt)^{n-m}\big]`,
>
> independently verified by the referee to `<5\times10^{-51}` relative
> error (`mpmath`, 50 digits, 40 `(n,m,γ)` triples, `n` up to `50`,
> `m` up to `7`). This identifies `T(n,m)`, divided by this front's own
> §3 Vandermonde normalizer, as **exactly** the tilted moment of a
> `\mathrm{Beta}(m+1,m+1)` random variable — the textbook continuum
> limit of this front's own §3 discrete median-order-statistic object
> (`t\sim\mathrm{Beta}(m+1,m+1)` is precisely what `j/(n+m+1)` converges
> to as sample size grows), tying §2 and §3 into a single coherent
> object exactly along the route named but not executed here. This
> **does not close `C(γ)`** — the §5 two-variable joint Laplace/saddle-
> point analysis is still required — but it hands a future front a
> ready-made classical Beta-integral for a Watson's-lemma/Laplace
> treatment in place of raw Pochhammer-sum manipulation, updating §8
> item 3 from "identified but not executed" to "identified and now
> carried through to a verified closed form (this addendum); the
> resulting integral itself remains untreated." See
> `adversarial/REFEREE_REPORT.md`, item (d), and its script
> `ref05_full_integral_closure.py`.

---

## §6 Self-caught issues

1. **`sp.hyper()` degenerate-parameter bug in script `02`'s first Part
   B draft (caught by inspection of the error pattern, before drawing
   any conclusion).** The first version of Part B evaluated the `2F1`
   identification via `sp.hyper([-(n-m),m+1],[-n],1-γ)` directly. At
   `m=0`, the upper parameter `-(n-m)=-n` **exactly equals** the lower
   parameter `-n` — the classical confluent identity
   `{}_2F_1(a,b;a;z)=(1-z)^{-b}$ (an INFINITE geometric series) then
   fires, and `sp.hyper()` silently evaluates the **non-terminating**
   series instead of the intended finite truncation, giving a wrong
   (too-large) number. Caught immediately: **all 8** mismatches in that
   run were exactly the `m=0` rows (`n=1,\ldots,8`), a pattern too
   clean to be a coincidence. **Fixed** by replacing `sp.hyper()` with
   an explicit, hand-written finite-Pochhammer-sum evaluator
   (`two_F1_finite_sympy`, capped at `nterms=n-m`, never symbolically
   extended to infinity) — the fixed version passes `44/44`. This is
   the same *class* of bug (confluent-parameter degeneracy silently
   changing which classical identity fires) as the predecessor's own
   corrected Charlier finding one front back, encountered independently
   here in a different piece of code, on a different (though related)
   object — worth flagging for any future front using `sp.hyper()` on a
   parameter family where two parameters can coincide.
2. **Interpretive slip in script `03`'s first Part D write-up (caught
   before finalizing this document, by re-reading the printed numbers
   against the written sentence).** An early draft's interpretation
   sentence had the direction of the tilting effect backwards ("at
   `γ=0.9` the tilt is mild" — the printed data show the *opposite*:
   `j^*` collapses nearly to `0` at `γ=0.9`, the *strong*-tilt case,
   since `(1-γ)\to0$ decays fastest there). No numeric value was wrong
   — only the prose description of which `γ` was which — corrected
   directly in the source (script `03`) before this document was
   written, not left as a dated addendum, since it was caught before
   any downstream conclusion depended on the wrong direction.
3. **Performance/degeneracy failure at very large `n` in script `06`'s
   exploratory (unlogged) timing tests, not in the final logged run.**
   While probing how far the `mpmath.hyp2f1`-based route (script `06`)
   could scale, `n=2^{24}` triggered `mpmath.libmp.libhyper.
   NoConvergence` even after special-casing the `m=0` degenerate
   parameter case (item 1's issue, resurfacing numerically rather than
   symbolically) — `mpmath`'s automatic transformation-selection logic
   for this specific degenerate-adjacent parameter family apparently
   breaks down well before `n=2^{24}`, for reasons not fully diagnosed
   in the time available. **Not investigated further and not needed**:
   the logged run (§7, up to `n=2^{18}`) already matches the wave-17
   front's own printed table value to `1.6\times10^{-11}` and the
   closed-form `C(0.5)` to `9.5\times10^{-8}` via Richardson
   extrapolation, more than sufficient corroboration; pushing to larger
   `n` was a nice-to-have, not load-bearing, and abandoned honestly
   rather than silently worked around.
4. **[Correção, 2026-08-29 — referee hostil, wave 30
   `ROUTE2-BYPASS-ATTEMPT`]** Script `02`'s header docstring described
   its Euler-integral discussion as "the basis for this front's
   Watson's-lemma / Laplace-method attempt in script `04`" — but script
   `04` is the P-recursion search (Route 2(i)), not a Watson's-lemma
   attempt; no such script exists in this front (the idea is named in
   §2/§5 as unexecuted). An apparent leftover from an earlier
   numbering/planning pass, caught by the referee, not this front. Purely
   a code comment, not reflected anywhere in this document's own prose,
   and does not affect any claim. See `adversarial/REFEREE_REPORT.md`,
   cosmetic finding 2.
5. **No other computational bugs found.** Every exact claim in §2–§4
   was checked at least two independent ways (symbolic ratio test vs.
   two separate finite-sum evaluators for the `2F1` identity; the
   order-statistic pmf identity checked against both its own
   normalization and the classical order-statistic formula; the mean
   and variance checked against both a symbolic closed-form simplify
   and brute-force exact summation; the saddle-point scaling law
   checked at growing `(n,m)$ for convergence, not asserted from a
   single point).

---

## §7 Numerical verification summary (fresh scripts, logs on disk)

| Script | What it checks | Result |
|---|---|---|
| `01_baseline_fresh.py`/`.log` | fresh re-derivation of `A_k`/`S_n` from Lemma 1's own definition (own code); independent re-derivation of the predecessor's PROVED double-sum-swap identity, 12 exact checks | 0/0 mismatches |
| `02_2F1_identification.py`/`.log` | the new `T(n,m)={}_2F_1(\ldots)$ identity: symbolic ratio test; 44 finite-sum sympy checks (after the self-caught `sp.hyper()` bug fix); 80 fresh exact-`Fraction` checks, no sympy | 0 mismatches everywhere; self-caught bug documented |
| `03_order_statistic_identification.py`/`.log` | Vandermonde normalizer (119 checks); order-statistic pmf match (106 checks); symmetry (64 checks); mean/variance vs. classical formula and brute force (12 checks); saddle-point tilting illustration | 0 mismatches everywhere |
| `04_precursion_search.py`/`.log` | empirical P-recursion search for `S_n(γ)$ in `n$, exact rational nullspace: `γ=1/2`, `r\le4,d\le5$ (20 combos) and `γ=1/3`, `r\le3,d\le4$ (12 combos) — `32$ total, over-determined by 6 eqns each [^tbl] | **no recursion found** anywhere tested (genuine negative result) |

[^tbl]: **[Correção, 2026-08-29 — referee hostil, wave 30
`ROUTE2-BYPASS-ATTEMPT`]** This row originally read "`γ\in\{1/2,1/3\}$,
`r\le4,d\le5$ (34 `(r,d)$ combos)", conflating the two `γ`'s distinct
search ranges into one and mis-totaling `20+12=32` as `34`. The body
text (VERDICT item 4, §4) already stated the correct `20`/`12` split;
only this summary table was wrong. Corrected here; does not affect the
negative result itself or any quantitative claim. See
`adversarial/REFEREE_REPORT.md`, cosmetic finding 1.
| `05_saddle_scaling_check.py`/`.log` | `j^*/m\to(1-γ)/γ$ convergence, 4 `γ$, `n$ up to `4\times10^6$, exact-`Fraction$ ratio-crossing locator | confirmed, relative deviation shrinks to `<0.35\%$ at largest scale, all 4 `γ$ |
| `06_mpmath_2F1_route_numerics.py`/`.log` | independent mpmath (dps 40/50) evaluation of `S_n$ via the `2F1$ route (`mpmath.hyp2f1$ term-by-term); sanity gate vs. exact values; `n$ up to `2^{18}$; comparison to wave-17's own printed table value; Richardson extrapolation vs. `C(0.5)$ | gate 0 mismatches; `n=2^{18}$ match to `1.6\times10^{-11}$; extrapolated `C$ matches closed form to `9.5\times10^{-8}$ |

All numerics are exact `Fraction`/`sympy` rational arithmetic, or
`mpmath` at dps 40–50 (script `06` only). No Monte Carlo, no
`numpy.random`/`random.seed` call anywhere in this front's code.

---

## §8 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed, NOT bounded, and
   NOT characterized as a convergent series with a proved remainder.**
   No progress toward closing it beyond every predecessor's own honest
   non-closure. This front's contributions are new structural/
   probabilistic *understanding*, not movement on the number itself.
2. **The two-variable (`j`,`m`) joint Laplace/saddle-point analysis
   named in §5 was NOT carried out.** This is, in this front's own
   assessment, the single most concrete next step this specific new
   lens (the `2F1`/order-statistic reformulation) opens up — a future
   front attempting it should expect work of comparable depth to
   closing Gap 1 via the existing moment/cumulant route, not a
   shortcut, per the honest diagnosis of §5.
3. **The Pfaff-transformation route to a genuinely valid Euler-integral
   representation of `T(n,m)` (§2, §5 item 2) was identified but not
   executed.** Concrete, scoped, plausibly tractable — named here
   explicitly as unfinished work, not merely gestured at.
4. **The P-recursion search (§4/script `04`) is empirical, not a
   proof of non-holonomicity.** It rules out low-order/low-degree
   recursions at two sample `γ`, within a bounded search grid; it does
   **not** prove no P-recursion exists at any order/degree, nor that
   none exists with `γ`-symbolic (rather than fixed-rational)
   coefficients — a genuine scope limitation, disclosed honestly.
5. **Gap 1 and Gap 3** (`THEOREM.md`, Estágio 26/33 onward) remain
   exactly as the predecessor left them — untouched by this front,
   whose entire effort was on genuinely new (Route 2) machinery, not
   the existing moment/cumulant `n_0(γ)`-tightening apparatus.
6. **The order-statistic large-deviations rate function itself (the
   full log-asymptotic of the tilted summand at its saddle, beyond just
   the saddle's *location*, §4) was not derived.** This is the natural
   next quantitative step before attempting item 2's joint analysis,
   and was not attempted here for lack of remaining time budget.

---

## §9 Scorecard

| Claim | Status |
|---|---|
| `T(n,m)=\binom nm\,{}_2F_1(-(n-m),m+1;-n;1-γ)` (new exact `2F1` identity) | **PROVED** (§2, script `02`; symbolic ratio test + 124 exact numeric checks across two independent evaluators) |
| Euler's integral representation is not directly usable (`C=-n` nonpositive integer) | **DIAGNOSED** (§2) — a genuine structural obstruction, analogous to but distinct from the predecessor's Charlier-EGF wall |
| `p_m(j)` is exactly the pmf of the median of a random `(2m+1)`-subset without replacement (new exact probabilistic fact) | **PROVED** (§3, script `03`; 225 exact numeric checks: 119 normalizer + 106 pmf-match) |
| Exact mean/variance of this order statistic | **PROVED / CONFIRMED** (§3, script `03`; symbolic + brute-force) |
| `T(n,m)` is a large-deviations (tilted), not CLT-regime, object | **DEMONSTRATED** (§3 Part D) |
| Saddle-point scaling law `j^*\sim m(1-γ)/γ` | **derived (leading order) and numerically CONFIRMED**, tightening as `n,m\to\infty` (§4, script `05`) — not a fully rigorous uniform bound |
| Empirical P-recursion-in-`n` search, `γ\in\{1/2,1/3\}`, `r\le4,d\le5` | **NO recursion found** (§4/script `04`) — genuine negative result, exact rational linear algebra, not floating-point |
| Independent `mpmath.hyp2f1`-route numerical reproduction of `T(γ)`/`C(0.5)` | **CONFIRMED** (§7, script `06`; `n=2^{18}` match to wave-17's own table to `1.6\times10^{-11}`; Richardson-extrapolated `C` matches closed form to `9.5\times10^{-8}`) |
| Two-variable joint saddle-point analysis needed to push further | **named precisely, NOT carried out** (§5) |
| **`C(γ)` for `γ\in(0,1)`, the ultimate target** | **remains entirely OPEN** |

---

## Seeds

| Block | Status |
|---|---|
| `20260945000–20260945999` (this front's reservation, `DISC-DEC-138`, wave 30 frente a) | grep-confirmed **unused** before any code was written (only the `DECISION_LEDGER.yaml` reservation line itself) — **zero seeds drawn from this block, and zero seeds drawn anywhere in this front**: every quantitative claim is exact symbolic algebra (`sympy`), exact rational arithmetic (`Fraction`), or deterministic high-precision numerics (`mpmath`, dps 40–50); no `random`/`numpy.random` call appears anywhere in scripts `01`–`06` |

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_baseline_fresh.py`/`.log` | fresh, independent re-derivation of `A_k`/`S_n` (Lemma 1's own definition) and of the predecessor's PROVED double-sum-swap identity |
| `02_2F1_identification.py`/`.log` | the new `T(n,m)` `2F1` identity: symbolic ratio test, finite-sum sympy cross-check (with a self-caught-and-fixed `sp.hyper()` degeneracy bug), and a from-scratch exact-`Fraction` terminating-`2F1` evaluator |
| `03_order_statistic_identification.py`/`.log` | the new order-statistic/median probabilistic identity for `T(n,m)`'s kernel; exact mean/variance; the large-deviations/tilting illustration |
| `04_precursion_search.py`/`.log` | the empirical P-recursion-in-`n` search (Route 2(i)), exact rational nullspace linear algebra, two independent `S_n` evaluators as a gate, two independent `γ` |
| `05_saddle_scaling_check.py`/`.log` | the `j^*\sim m(1-γ)/γ` saddle-point scaling-law numerical confirmation, four `γ`, `n` up to `4\times10^6` |
| `06_mpmath_2F1_route_numerics.py`/`.log` | independent high-precision (`mpmath`) numerical evaluation of `S_n`/`C(γ)` via this front's own `2F1` identity, cross-checked against the wave-17 front's own printed table and the closed-form `C(0.5)` |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No `git` commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
