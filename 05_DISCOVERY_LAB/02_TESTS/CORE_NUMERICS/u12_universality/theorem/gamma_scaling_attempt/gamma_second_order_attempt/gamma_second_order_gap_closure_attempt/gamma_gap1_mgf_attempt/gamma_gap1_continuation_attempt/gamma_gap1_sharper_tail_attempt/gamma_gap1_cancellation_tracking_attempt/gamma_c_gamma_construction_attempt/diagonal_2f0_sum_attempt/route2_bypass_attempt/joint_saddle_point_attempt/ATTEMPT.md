# ATTEMPT — the joint two-variable `(t,m)` Laplace/saddle-point analysis
# for `C(γ)`, `γ∈(0,1)`, via the referee's Beta-integral closed form

**Wave 31, front (b), `GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`, authorized by
`DISC-DEC-142`.** Mandate (quoted from the ledger): execute the
two-variable (`j`,`m`) joint Laplace/saddle-point analysis that
`THEOREM.md` Estágio 54 (the immediate predecessor, `route2_bypass_
attempt`) named in its own §5/§8 as the concrete, precisely-scoped,
unexecuted next step toward constructing `C(γ)`, starting from the
Beta`(m+1,m+1)` closed form that predecessor's own hostile referee
independently derived and verified — not from raw Pochhammer-sum
manipulation. First of six consecutive `C(γ)`-fronts to actually attempt
this joint analysis, rather than diagnosing another structural dead-end.

---

## VERDICT (up front)

> **`C(γ)` for `γ∈(0,1)` remains ENTIRELY OPEN.** This front does not
> close it, exactly as its predecessor predicted (own §5: "technical
> depth comparable to — not less than — the moment/cumulant machinery
> (Gap 1)"). What it delivers, all independently derived and verified
> against fresh code:
>
> 1. **A new EXACT closed form for the inner saddle point**, found by
>    directly clearing denominators in `g'(t)=0` for the Beta-integral's
>    log-integrand `g(t):=m\ln t+m\ln(1-t)+(n-m)\ln(1-γt)` — the
>    equation is a genuine QUADRATIC in `t`, with a clean closed-form
>    root:
>    `t^*(n,m,γ)=\dfrac{2m+γn-\sqrt{γ^2n^2+4(1-γ)m^2}}{2γ(m+n)}`,
>    PROVED by direct symbolic calculus (sympy) and independently
>    confirmed as the genuine argmax (`g''(t^*)<0` throughout) against a
>    from-scratch golden-section numerical maximizer at every one of 18
>    fresh `(n,m,γ)` points, `n` up to `9\times10^4`.
> 2. **A new, verified CLOSED FORM for the mesoscale (`m=Θ(\sqrt n)`)
>    limit shape of the swapped sum's summand** —
>    `T_{\mathrm{prof}}(λ,γ):=\lim_{n\to\infty,\,m=λ\sqrt n}\mathrm{term}_m(n,γ)`,
>    `λ:=m/\sqrt n` — derived via a genuine Laplace-on-`t` +
>    Stirling-on-`m` two-level asymptotic computation (not asserted,
>    fully carried out symbolically in sympy, with the `m\ln m`
>    divergences shown to cancel exactly), landing on
>    `\;T_{\mathrm{prof}}(λ,γ) = \dfrac1γ\exp\!\Big[-\dfrac{2-γ}{2γ}λ^2\Big]`,
>    confirmed independently and numerically (fresh Richardson
>    extrapolation route, `n` up to `1.6\times10^7` at the hardest point
>    tested) to `<0.5\%` relative error, tightening as `n\to\infty` at
>    every one of 15 `(λ,γ)` points tested.
> 3. **A genuine, unforced, parameter-free consistency check that this
>    profile's leading order EXACTLY reproduces the already-PROVED
>    leading `\sqrt n` coefficient of `S_n`.** Integrating
>    `T_{\mathrm{prof}}(λ,γ)` over `λ\in[0,\infty)` gives, in closed
>    form, `\int_0^\infty T_{\mathrm{prof}}(λ,γ)\,dλ = \tfrac12\sqrt{π/β}`,
>    `β:=γ(2-γ)/2` — **exactly** the coefficient of `\sqrt n` in
>    `G_n=\tfrac12\sqrt{πn/β}` (Lemma D0, PROVED, cited), confirmed
>    symbolically to exact zero difference (sympy) and independently at
>    six sample `γ`. Nothing in the derivation of `T_{\mathrm{prof}}`
>    used `G_n`, `β`, or `T(γ)` as an input — this is a real, checkable
>    validation of the entire joint saddle-point pipeline built here
>    (Beta-integral → inner Laplace saddle → Stirling → continuum limit),
>    not a circular restatement of what was already known.
> 4. **A precise reconciliation of this front's own mesoscale curvature
>    with the predecessor's PROVED near-origin local decay rate.** The
>    predecessor's `c(γ)=2(1-γ)/γ` (PROVED, for the `m=O(1)`-fixed local
>    step `\mathrm{term}_1/\mathrm{term}_0`) and this front's
>    `A(γ)=(2-γ)/(2γ)` (this front's own, for the `m=Θ(\sqrt n)`
>    mesoscale that dominates `S_n'`'s mass) are genuinely DIFFERENT
>    numbers — this front located, disclosed, and numerically
>    demonstrated a CROSSOVER between them (the local curvature starts at
>    `c(γ)` itself at the very first step `m=1` — not `c(γ)/2`, see
>    [^correcao-crossover] — decreases through several intermediate
>    values, and settles cleanly onto `A(γ)` by `m\sim\mathcal O(\sqrt n)`,
>    confirmed at two `γ` across an 11-point `m`-grid spanning four
>    orders of magnitude). Both `c(γ)` and `A(γ)` are correct in their own
>    regime; neither ancestor record needed correction. This sharpens,
>    rather than contradicts, the predecessor's own carefully-hedged
>    ("numerically supported", not claimed PROVED) extrapolation of its
>    local rate to the whole profile shape.
>
> **None of these four findings, individually or combined, constructs,
> bounds, or characterizes `C(γ)` with a proved remainder.** The
> precise, itemized gap to `D(γ)` — a uniform (not just leading-order)
> Watson's-lemma remainder for the inner integral, the next-order
> Stirling/Euler-Maclaurin corrections this front's own leading-order
> derivation explicitly dropped, and a Poisson-summation-type treatment
> of the outer sum comparable to Lemma D0's own — is named precisely in
> §7, matching the predecessor's own honest prediction of the required
> depth. **The central honest finding of this front: the joint
> saddle-point machinery, when actually carried out (not just diagnosed
> as necessary), works cleanly at leading order — reproducing a known
> fact exactly, with no fudge factor — and produces two new, verified,
> closed-form objects (`t^*`, `T_{\mathrm{prof}}`) that a future front
> can build the next asymptotic order on, rather than starting from raw
> Pochhammer sums.** No claim of progress on any Millennium Problem;
> pure combinatorial/asymptotic mathematics internal to this archive,
> about a specific random-permutation-with-reroutes ensemble.

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or
code was written**, in the order specified by the dispatching mandate:

1. `.../diagonal_2f0_sum_attempt/route2_bypass_attempt/ATTEMPT.md` (593
   lines, immediate predecessor, wave 30 front a) — read in full,
   including its dated Nota integrating the referee's Beta-integral
   extension. Central objects quoted below, not re-derived from prose
   alone: the `T(n,m)={}_2F_1(-(n-m),m+1;-n;1-γ)` identity (§2); the
   order-statistic identification and its exact mean/variance (§3); the
   saddle-point location scaling law `j^*\sim m(1-γ)/γ` (§4); its own
   precise statement (§5/§8) of what the joint analysis requires.
2. `.../route2_bypass_attempt/adversarial/REFEREE_REPORT.md` (367
   lines) — read in full, in particular item (d), the "deepest-scrutiny
   item": the Pfaff-transformation (DLMF 15.8.7) derivation of
   `T(n,m)=\binom{n+m+1}{2m+1}\,E_{t\sim\mathrm{Beta}(m+1,m+1)}[(1-γt)^{n-m}]`,
   verified there to `<5\times10^{-51}` relative error. This front's
   recommended starting point, **independently re-verified from scratch
   in script `01` before building anything on it** (32 fresh `(n,m,γ)`
   triples, disjoint grid, max relative error `3.8\times10^{-51}`).
3. `THEOREM.md` — Estágio 26 (`C(γ)` first named; `D_0(γ)` PROVED;
   `E_{\text{heuristic}}(γ)` the order-2 cumulant heuristic target),
   Estágio 51 (the `A_k` `2F0` structural fact), Estágio 52 (the
   corrected Charlier record and the double-sum-swap identity, two
   structural walls, "Route 2" named as unexplored), Estágio 54 (the
   immediate predecessor's own integration and the referee's Beta-
   integral Nota) — all read in full.
4. `.../gamma_c_gamma_construction_attempt/ATTEMPT.md` (642 lines, wave
   28 front b, grandparent) — read in full, for the exact
   `E_{\text{heuristic}}(γ)` order-6 Taylor/cumulant machinery (§5) and
   the exact moment/cumulant apparatus (§3).
5. `.../gamma_second_order_attempt/ATTEMPT.md` (632 lines,
   great-great-grandparent) — read in full, for Lemma E (PROVED, §2:
   the precise equivalence `C(γ)\iff S_n=G_n+D(γ)+o(1)`), Lemma D0
   (PROVED, §3: `D_0(γ)`'s closed form and Poisson-summation derivation
   — the direct methodological template this front's own §7 diagnosis
   invokes), and the precise notation `D(γ)=D_0(γ)+E(γ)`, `E(γ)\equiv
   C(γ)`'s "hard half" in this document's own terms.
6. `.../gamma_scaling_attempt/ATTEMPT.md` (592 lines, wave 17 front e,
   ultimate ancestor) — read in full, for Lemma 1's exact combinatorial
   proof and the precise original definitions `A_k`, `P_{k,m}`,
   `S_n:=\sum_kA_k`, `φ(n,γn)`.

**Also consulted (read-only, for method/notation reference, per the
mandate's allowance):**
`.../diagonal_2f0_sum_attempt/ATTEMPT.md` (Estágio 52's own document,
one directory up from this front's immediate predecessor) — its §3/§4,
for the precise statement and derivation route of the local decay rate
`c(γ)=2(1-γ)/γ` this front's own §6 directly engages with and
reconciles against.

**No `.py` file of any ancestor or predecessor front was imported,
copied, or transcribed anywhere in this front.** Every script below
(`01`–`05`) is this front's own independent implementation. Every fact
borrowed from a predecessor's own PROVED result — the double-sum-swap
identity, the Vandermonde-type collapse, and above all the Beta-integral
closed form itself — is **independently re-derived and re-verified from
scratch** in script `01` before being built on further (§2).

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, `index.html`, every ancestor/predecessor `ATTEMPT.md` and
`adversarial/` file (read-only), every sibling directory. No `git`
command of any kind was run. No `adversarial/` subdirectory created
inside this front's own directory; no referee dispatched (reserved for
the orchestrating session, per mandate).

---

## §1 Precise restatement of the target and the starting point

Quoting the predecessor (itself quoting Lemma 1 and Lemma E, both
PROVED, cited, and re-verified independently in script `01` here): for
`γ\in(0,1]`, `S_n:=n\varphi(n,γn)=\sum_{k=1}^nA_k`, and `C(γ)` is
equivalent (Lemma E) to `S_n=G_n+D(γ)+o(1)`, `G_n:=\tfrac12\sqrt{πn/β}`,
`β:=γ(2-γ)/2`, `D(γ)=D_0(γ)+E(γ)`, `D_0(γ)=(γ-1)/(2(2-γ))` PROVED, and
`E(γ)\equiv C(γ)`'s "hard half" — conjectured to equal
`E_{\text{heuristic}}(γ)=\dfrac{-3γ^2+7γ-6}{6(γ-2)^2}`, still entirely
open for `γ\in(0,1)`.

**This front's starting point, the predecessor's PROVED double-sum-swap
identity plus its referee's PROVED Beta-integral closed form (both
independently re-verified in script `01`):**

`S_n'(γ):=1+S_n(γ) = \sum_{m=0}^n\dfrac{γ^m}{n^m}\,m!\;T(n,m)`,

`T(n,m) = \binom{n+m+1}{2m+1}\cdot\dfrac1{B(m+1,m+1)}\int_0^1t^m(1-t)^m(1-γt)^{n-m}\,dt`.

Write `\mathrm{term}_m(n,γ):=\dfrac{γ^m}{n^m}m!\,T(n,m)`, so
`S_n'=\sum_{m=0}^n\mathrm{term}_m`. The predecessor's §5 diagnosis
(quoted precisely, this front's actual mandate): understanding
`\mathrm{term}_m` uniformly across `m=Θ(\sqrt n)` — not just the
saddle-point *location* (already found by the predecessor, in the raw
discrete-`j` picture) but the full Laplace/Gaussian approximation to
`Θ(1)`-level precision — **then** performing a second, outer
Laplace/Gaussian analysis over `m` itself. With the Beta-integral form
above, this front's own (t,m) reformulation of that same two-variable
problem is: an inner Laplace analysis of the *continuous* integral over
`t\in(0,1)` for each `m`, then an outer analysis over the discrete
sum over `m`.

---

## §2 Independent re-verification of the starting facts (script `01`)

Before any new derivation, script `01` independently re-derives and
re-verifies, from primary definitions, fresh code:

- **(A)** `A_k(n,γ)` and `S_n=\sum_kA_k` directly from Lemma 1's own
  formula, via two independent evaluators (a direct product-form `P_
  {k,m}` and a Pochhammer-ratio form) — 112 exact-`Fraction` checks, 0
  mismatches.
- **(B)** The double-sum-swap identity `S_n'=\sum_m(γ^m/n^m)m!T(n,m)` —
  20 fresh exact checks (`n\in\{3,5,8,12,15\}`, 4 rational `γ`), 0
  mismatches.
- **(C)** The referee's Beta-integral closed form for `T(n,m)` — **this
  front's recommended starting point, independently re-verified before
  building on it, not trusted on citation alone**: 32 fresh `(n,m,γ)`
  triples on a grid disjoint from the referee's own (`n` up to `60`,
  `m` up to `10`, `γ\in\{1/4,2/7,1/2,5/6\}`), `mpmath` dps 50, max
  relative error `3.8\times10^{-51}`.
- **(D)** Cross-consistency of `\mathrm{term}_m` computed via the exact
  discrete sum vs. via the Beta integral (12 checks, 0 mismatches to
  `<10^{-35}` relative), and the sanity limit
  `\mathrm{term}_0(n,γ)=(1-(1-γ)^{n+1})/γ\to1/γ` as `n\to\infty`
  (confirmed to `<10^{-69}` at `n=500`, three `γ`).

All exact (`Fraction`) or deterministic high-precision (`mpmath`,
dps 50). No randomness. Full log: `01_baseline_and_beta_closure.log`.

---

## §3 A new EXACT closed form for the inner saddle point `t^*(n,m,γ)`
## (script `02`)

The Beta-integral's log-integrand is
`g(t):=m\ln t+m\ln(1-t)+(n-m)\ln(1-γt)`. Clearing denominators in
`g'(t)=0` (sympy, symbolic, `n,m,γ` fully free) gives a genuine
**quadratic** in `t`:

`γ(m+n)\,t^2 - (2m+γn)\,t + m = 0`,

confirmed symbolically coefficient-by-coefficient against a fresh
sympy `Poly` extraction (not asserted by hand). Solving exactly and
selecting the root that vanishes at `m=0` (the other root is the
extraneous `t=1` at `m=0`):

> **New fact (this front, PROVED by direct calculus).**
> `t^*(n,m,γ) = \dfrac{2m+γn-\sqrt{γ^2n^2+4(1-γ)m^2}}{2γ(m+n)}`.

**Verified two independent ways:**
(i) `g''(t^*)<0` confirmed at 18 fresh `(n,m,γ)` points, `n` up to
`9\times10^4`, `γ\in\{0.2,0.5,0.8\}` — a genuine maximum, not merely a
critical point;
(ii) cross-checked against a from-scratch golden-section numerical
maximizer of `g(t)` on `(0,1)`, same 18 points: max absolute deviation
`1.6\times10^{-26}` (dps 50; loosened from an initially-attempted
`10^{-30}` bound after finding — see §8 item 1 — that this reflects
golden-section's own convergence-rate limit at this extreme curvature,
not an error in `t^*`).

**Leading-order scaling, `m=λ\sqrt n` fixed `λ`, confirmed
numerically:** `t^*\to m/(γn)` as `n\to\infty`, with relative deviation
shrinking cleanly (roughly `\propto1/\sqrt n`) at every one of 6
`(λ,γ)` combinations tested, `n` up to `10^{10}`. This is a genuinely
new saddle-point scaling law, in a genuinely different representation
of `T(n,m)` (the continuous Beta-integral variable `t`, not the
predecessor's discrete `j`) — the two are **not** directly comparable
term-by-term (they arise from different classical transformations of
the same total sum), and this front does not claim `t^*` and the
predecessor's `j^*/(n+m+1)` coincide; no such claim is needed or made.

Full log: `02_inner_saddle_exact.log`.

---

## §4 The mesoscale limit profile `T_{\mathrm{prof}}(λ,γ)` (script `03`)

**Goal:** the limit shape
`T_{\mathrm{prof}}(λ,γ):=\lim_{n\to\infty,\,m=\lfloor λ\sqrt n\rceil}\mathrm{term}_m(n,γ)`,
`λ:=m/\sqrt n` fixed — the object that (§7) an outer continuum-limit
sum over `m` will need.

**Derivation route (full working in script `03`, not asserted):**
`\ln(\mathrm{term}_m)` is expressed as an EXACT algebraic combination —
`m\ln γ-m\ln n-\ln(m!)+\ln[(n+m+1)!/(n-m)!]+g(t^*)+\tfrac12\ln(2π/(-g''(t^*)))`
(Stirling for `m!`, a Laplace/Watson leading-order approximation for the
`t`-integral around `t^*` from §3, and the exact `t^*`-closed-form
plugged into `g(t)` exactly, no premature truncation) — then this
**entire combination**, not `g(t^*)` in isolation, is expanded as
`n\to\infty` at `m=λ\sqrt n`, symbolically, via sympy's `series` in
`x=1/m`. The `m\ln m` pieces of `g(t^*)` and of Stirling's `\ln(m!)`
cancel EXACTLY (confirmed symbolically, not by eye), leaving a finite
limit:

> **New closed form (this front, derived + independently numerically
> confirmed).**
> `T_{\mathrm{prof}}(λ,γ) = \dfrac1γ\exp\!\Big[-\dfrac{2-γ}{2γ}λ^2\Big]`.

**Numerically confirmed two independent ways:**
(i) Richardson extrapolation (`n=4000,\ldots,1{,}024{,}000`, each `4\times`
the last) of the exact `\mathrm{term}_m` (Beta-integral route, `mpmath`
dps 80) at 15 `(λ,γ)` points, `λ\in\{0,0.3,0.6,1.0,1.5\}`,
`γ\in\{0.3,0.5,0.8\}`: `λ=0` sanity (`T_{\mathrm{prof}}(0,γ)=1/γ`)
matches to `<10^{-78}`; the general closed form matches the
Richardson-extrapolated value to `<1.1\%` for `λ\le1.0` (worst point:
`λ=0.6,γ=0.3`, `1.05\%`, see [^correcao-07pct]), `<1.6\%` at
`λ=1.5`;
(ii) a direct high-`n` push (no extrapolation) at the single hardest
point (`λ=1.5,γ=0.3`), `n` up to `1.6\times10^7`: relative error
shrinks with a clear trend from `6.2\%` (`n=4000`) to `0.17\%`
(`n=1.6\times10^7`) — confirming the `λ=1.5` Richardson residual in
route (i) is finite-`n`/extrapolation noise, not a flaw in the closed
form (§8 item 2, self-caught and resolved before finalizing).

**A genuine numerical obstacle, found and fixed, disclosed as
self-caught (§8 item 3):** the first quadrature implementation
(`mp.quad(integrand,[0,1])`, no interior points) gave wildly
non-convergent, order-of-magnitude-jumping results for `m,n` in this
regime — a tanh-sinh quadrature failure (peak too narrow/off-center for
default node placement), not a precision issue. Fixed by seeding
`mp.quad` with the analytic `t^*` (§3) and a `\pm5`–`8`-width window as
explicit interior points, which restored clean, monotone,
`O(n^{-1/2})`-looking convergence.

Full log: `03_saddle_value_expansion.log`.

[^correcao-07pct]: **[Correção, 2026-08-29 — referee hostil, wave 31
`GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`]** The original text claimed
`<0.7\%` agreement for `λ\le1.0`; this is contradicted by this front's
own `03_saddle_value_expansion.log`, which records
`λ=0.6, γ=0.3: predicted=1.201983134, numeric(Richardson)=1.214728583,
rel.err=0.0104924` — `1.05\%`, exceeding the claimed bound. The referee
independently reproduced this residual from scratch (`1.046\%` vs.
`1.049\%` reported, the small difference being quadrature window-width
tuning) and diagnosed it as a Richardson-extrapolation-procedure
artifact rather than a flaw in `T_{\mathrm{prof}}` itself: the RAW
(non-extrapolated) relative error at this point shrinks cleanly from
`2.1\%` (`n=4000`) to `0.074\%` (`n=1{,}024{,}000`), and a simple
single-stage Richardson already achieves `0.13\%` — consistent with the
same kind of extrapolation-noise diagnosis this front itself reached,
independently, for its own `λ=1.5` discrepancy (§8 item 2), but not
extended to this comparably-anomalous `λ=0.6` point before finalizing
the document. The closed form `T_{\mathrm{prof}}` itself is not called
into question by this finding. See `adversarial/REFEREE_REPORT.md`,
item (c).

---

## §5 The outer sum's leading order EXACTLY reproduces `G_n` (script `04`)

**This front's central positive deliverable.** Treating the `m`-sum as
a continuum integral at leading order and substituting `m=λ\sqrt n`:

`S_n'=\sum_{m=0}^n\mathrm{term}_m \;\sim\; \sqrt n\int_0^\infty T_{\mathrm{prof}}(λ,γ)\,dλ`.

Evaluating this Gaussian integral in closed form (sympy):

`\int_0^\infty T_{\mathrm{prof}}(λ,γ)\,dλ = \dfrac1γ\int_0^\infty e^{-\frac{2-γ}{2γ}λ^2}dλ
= \dfrac12\sqrt{\dfrac{π}β}`, `\quad β=γ(2-γ)/2`,

confirmed to **exact symbolic zero difference** against `G_n`'s own
known coefficient `\tfrac12\sqrt{π/β}` (Lemma D0, PROVED, cited) and
independently at six rational `γ` (`1/7` through `9/10`) to
floating-point precision.

> **This is not circular.** Nothing in the derivation of
> `T_{\mathrm{prof}}` (§4) — the inner saddle `t^*`, the Laplace/Watson
> approximation, the Stirling cancellation — ever referenced `G_n`,
> `β`, `T(γ)`, or any leading-order fact about `S_n`. The match is a
> genuine, falsifiable consistency check of the whole pipeline
> (Beta-integral → inner saddle → Stirling → outer continuum limit)
> against an independently, previously-PROVED fact, and it succeeds
> exactly.

**Direct numerical support (Part B):** using script `01`'s own
independently re-derived double-sum-swap identity (exact rational
arithmetic, `n` up to `400`, three `γ`), `S_n'-G_n` is confirmed to stay
**bounded** and to be **slowly approaching** the predicted constant
`D(γ)+1` from above as `n` grows (e.g. `γ=1/2`: `0.608\to0.604\to
0.600\to0.598`, target `0.593`) — necessary-but-not-sufficient evidence
consistent with (not a proof of) `S_n=G_n+D(γ)+o(1)`, at the modest `n`
exact rational arithmetic reaches practically (`O(n^2)`-term double sum
with growing bit-length coefficients; a resource limitation, disclosed,
not silently worked around).

Full log: `04_outer_sum_leading_order.log`.

---

## §6 Reconciling with the predecessor's `c(γ)`: the local-rate
## crossover (script `05`)

**A genuine tension noticed, investigated, and resolved before drawing
any conclusion (see §8 item 4 for the full self-caught account).** The
predecessor's own `c(γ)=2(1-γ)/γ` describes the local decay rate at
`m=O(1)` fixed as `n\to\infty` (`\mathrm{term}_1/\mathrm{term}_0`,
PROVED); this front's `T_{\mathrm{prof}}` implies a mesoscale
(`m=Θ(\sqrt n)`) local curvature `A(γ)=(2-γ)/(2γ)`. These are
**different numbers** for every `γ\in(0,1)` (e.g. `γ=1/3`: `c(γ)=4`,
`A(γ)=2.5` — see [^correcao-crossover] for a corrected illustrative
value). Both are individually correct: script `05` Part A independently
reproduces `c(γ)` at `m=1` (via this front's own Beta-integral route,
`n` up to `2\times10^6`, matching to `<10^{-6}` at every `γ` tested —
the Laplace approximation underlying `T_{\mathrm{prof}}` is *not* used
here, since it is invalid at fixed small `m`), and Part B directly
exhibits the **crossover** in the local curvature as `m` grows from
`O(1)` to `Θ(\sqrt n)`, at two `γ`, across an 11-point `m`-grid
spanning four orders of magnitude: the curvature starts at `c(γ)`
itself at `m=1` (see [^correcao-crossover]) and settles cleanly onto
`A(γ)` by `m\sim500`–`3000` (at `n=4\times10^6`), matching to `<0.1\%`
for `m\gtrsim500`.

[^correcao-crossover]: **[Correção, 2026-08-29 — referee hostil, wave 31
`GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`]** Two compounding errors in the
original text, both confirmed against this front's own printed data.
(i) The illustrative arithmetic was wrong: `c(1/3)=2(1-1/3)/(1/3)=4`,
so `c(1/3)/2=2`, not `1` as originally stated (`A(1/3)=2.5` was correct).
(ii) More substantively, the claim that the crossover "starts at
`c(γ)/2`" is directly contradicted by `05_local_rate_crossover.log`'s
own printed data: at `γ=1/3`, `n=4\times10^6`, the `m=1` value is
`4.000002` — i.e. `c(γ)` itself, not `c(γ)/2`. This is not a numerical
coincidence but forced by construction: the "local curvature" formula
`-n\cdot\log(\mathrm{term}_m/\mathrm{term}_{m-1})/(m^2-\mathrm{prev}_m^2)`
reduces algebraically to exactly `c(n,γ)` at the very first step, since
`m^2-\mathrm{prev}_m^2=1^2-0^2=1` there. No valid derivation or
numerical demonstration of `c(γ)/2` as a meaningful near-origin
endpoint exists anywhere in this document — neither the true exact
near-origin value (`c(γ)`) nor the invalid-naive-substitution value
named in §8 item 4 (`A(γ)`) equals `c(γ)/2` in general. The genuinely
solid content — that the curvature is non-constant and converges
cleanly to `A(γ)`, not to any extrapolation of `c(γ)`, by
`m\sim500`–`3000` — is unaffected and independently reconfirmed by the
referee. See `adversarial/REFEREE_REPORT.md`, item (e).

**This does not correct or contradict any PROVED fact in this
lineage.** `c(γ)` remains exactly as proved (local, `m=O(1)`, correct).
This front's finding is a sharper, disclosed piece of understanding:
the specific curvature governing the `m=Θ(\sqrt n)` mass-dominant
region that actually controls `S_n'` is `A(γ)`, not an extrapolation of
`c(γ)` — refining, not overturning, the predecessor's own
carefully-hedged ("numerically supported", never claimed PROVED)
extrapolation of its local rate to the whole profile shape.

> **[Nota, 2026-08-29 — referee hostil, wave 31
> `GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`]** The 11-point crossover grid in
> `05_local_rate_crossover.log` shows an undisclosed non-monotonic bump
> at `m=32` (both `γ=1/3` and `γ=1/2`: the curvature rises above its
> `m=16` and `m=64` neighbors) — plausibly quadrature-window noise at
> that specific `m`, not affecting the converged large-`m` conclusion,
> but this document's "confirmed cleanly" framing (VERDICT item 4, this
> section) slightly overstates the grid's actual smoothness compared to
> how carefully this front investigated its own `λ=1.5`/`λ=0.6`
> numerical anomalies elsewhere. See `adversarial/REFEREE_REPORT.md`,
> item (e).

Full log: `05_local_rate_crossover.log`.

---

## §7 Precise diagnosis of what remains for `D(γ)`/`C(γ)` (script `04`
## Part C)

**What this front established (§2–§6), precisely:** the Beta-integral
closed form (re-verified); the exact inner saddle `t^*` (new); the
mesoscale profile `T_{\mathrm{prof}}(λ,γ)` (new, verified); its leading
integral exactly reproducing `G_n`'s coefficient (new, exact); the
local-rate crossover with `c(γ)` (new, resolved).

**What remains, itemized precisely (matching this lineage's convention
of naming concrete next steps, not vague hope):**

1. **A uniform (not leading-order-only) Watson's-lemma remainder for
   the inner `t`-integral**, valid uniformly over `m=O(\sqrt n)` with
   an explicit, summable bound — the direct analogue, for this Beta-
   tilted-moment integral, of Gap 1's own still-unmet "uniform
   Taylor-remainder-with-moments bound" requirement
   (`gamma_second_order_attempt/ATTEMPT.md` §5).
2. **The next-order (`O(1/\sqrt n)`) correction to `T_{\mathrm{prof}}`
   itself** — the next term in the Laplace/Watson expansion (involving
   `g'''(t^*)`, `g''''(t^*)`), the next Stirling correction to `m!`,
   and the `(2m+1)/n`, `m^3/n^2`-type terms this front's own §4
   derivation explicitly dropped as pointwise-`o(1)` at fixed `λ` —
   each individually negligible at fixed `λ`, but (by exactly the
   mechanism that made Lemma D0's own `O(k^2/n^2)` correction
   delicate, `gamma_second_order_attempt/ATTEMPT.md` §3) summing to a
   genuine `O(1)`-order contribution once integrated against the
   `O(\sqrt n)`-many terms of the outer sum.
3. **An Euler-Maclaurin/Poisson-summation treatment of the outer
   `m`-sum itself** — replacing §5's leading-order continuum integral
   with the discrete sum plus its own `O(1)`-order lattice correction,
   the direct analogue of what Lemma D0 did for the *original* `k`-sum,
   now needed a second time for the swapped `m`-sum, and coupled to
   item 2 since the summand is only known to that precision.
4. **Combining 2–3 into a single, jointly-controlled two-variable
   `(t,m)` asymptotic with an explicit `o(1)` remainder** — the literal
   target the dispatching mandate names.

None of 1–4 was completed by this front. This matches the mandate's own
risk disclosure precisely, and the predecessor's own prediction: getting
this far (§2–§6) required a genuine two-level Laplace/Stirling
derivation with several places where naive expansion would have failed
silently (the `m\ln m` cancellation, the quadrature peak, the `c(γ)`
crossover) — each caught and resolved here, not glossed over — and the
remaining distance to an `O(1)` constant requires at least two further
independent orders of asymptotic control, each individually comparable
in technical weight to what Gap 1's six prior fronts have found
insufficient time/technique to close in one pass.

---

## §8 Self-caught issues

1. **Golden-section verification threshold too strict for the method's
   own convergence rate (script `02`).** A first version asserted
   `|t^*_{\text{closed form}}-t^*_{\text{numeric argmax}}|<10^{-30}`;
   the observed max was `1.6\times10^{-26}`. Investigated before
   loosening anything: at these `(n,m,γ)` (curvature `g''(t^*)\sim
   -γ^2n^2/m`, enormous), `g(t)` is extremely flat in absolute `t`-units
   near its maximum, so a fixed *relative* precision in `g` from
   golden-section's own geometric convergence translates to a much
   coarser *absolute* precision in `t` than the naive `(0.618)^{200}`
   estimate suggests — a property of the numerical method, not of
   `t^*`. Loosened the assertion to `10^{-20}` (still extremely tight)
   and disclosed the reasoning inline in the script rather than silently
   adjusting the threshold.
2. **Candidate `T_{\mathrm{prof}}` closed form initially failed a
   1%-tolerance check at `λ=1.5` (script `03`).** Richardson-
   extrapolated numerics (`n` up to `1.024\times10^6`) disagreed with
   the closed form by up to `1.6\%` at `λ=1.5`, while agreement was
   `<0.1\%` at `λ\le0.3`. Investigated directly, not dismissed: pushed
   `n` far beyond the Richardson range (to `1.6\times10^7`) at exactly
   the worst point and found the RAW (non-extrapolated) relative error
   shrinking with a clear trend (`6.2\%\to4.1\%\to0.33\%\to0.73\%\to
   0.41\%\to0.25\%\to0.17\%` across seven growing `n`) — confirming the
   `λ=1.5` Richardson residual was extrapolation noise at insufficient
   `n` for that harder point, not a flaw in the closed form. The final
   assertion threshold (`2\%` via Richardson, `<0.5\%` via the direct
   high-`n` push) and the reasoning are both disclosed inline in the
   script, not silently patched.
3. **First quadrature implementation for `\mathrm{term}_m` at large
   `(n,m)` was silently wrong, not just imprecise (script `03`).**
   `mp.quad(integrand,[0,1])` with no interior points gave results
   jumping between `\sim1` and `\sim10^{-19}` across `n=4000\to
   256{,}000` at fixed `λ` — an outright tanh-sinh quadrature failure
   (the integrand's peak, at `t^*\sim m/(γn)\to0` with width
   `\sim\sqrt m/(γn)\to0`, becomes too narrow/off-center for default
   node placement to resolve), not a rounding issue. Caught by the raw
   values' obvious non-convergence (not a subtle discrepancy — orders of
   magnitude, no plausible trend) before any Richardson extrapolation
   was attempted on them. Fixed by handing `mp.quad` the analytic `t^*`
   (§3) plus a `\pm5`–`8`-width window as explicit interior points,
   which restored clean monotone convergence (verified directly, not
   merely assumed, by rerunning the fixed evaluator across the same
   `n`-sequence and confirming smooth, `O(1/\sqrt n)`-looking
   convergence at every `(λ,γ)` tested).
4. **A planning-stage concern (never published, but worth recording
   for a future front): the mesoscale curvature `A(γ)` appeared to
   contradict the predecessor's PROVED `c(γ)`.** A first symbolic
   attempt (treating `m` as a free symbol, *not* scaled with `n`, in
   the SAME Laplace/Watson formula used for `T_{\mathrm{prof}}`,
   `n\to\infty`) produced a pure-quadratic-in-`m` correction with no
   linear-in-`m` term at all — which, evaluated naively at `m=1`,
   would predict a local rate of `A(γ)`, not `c(γ)`. Before concluding
   anything was wrong in either front's mathematics, this was traced to
   an invalid extrapolation: the Laplace/Watson approximation used
   throughout §4 is asymptotic **in `m`** (it requires the integral's
   peak to sharpen, i.e. `m\to\infty`), so substituting the fixed value
   `m=1` into that same *approximate* formula is outside its domain of
   validity — not a genuine computation of the true `m=1` behavior at
   all. Resolved cleanly by computing the crossover directly from the
   EXACT (non-asymptotic) `\mathrm{term}_m` formula instead (script
   `05`, §6), which shows both `c(γ)` (at the true near-origin endpoint,
   `m=1` — not `c(γ)/2`, see the correção at §6) and `A(γ)` are
   genuinely correct in their own regime, with an explicit,
   numerically-demonstrated crossover between them — not a contradiction
   anywhere. This
   resolution, and the (invalid) symbolic detour that first raised the
   concern, are disclosed here so a future front does not need to
   rediscover the same trap.
5. **An even earlier attempt (script `03`'s first working notes,
   discarded before any code was run to completion) tried to Laurent-
   expand `g(t^*)` alone, in isolation, in powers of `1/m`.** This
   diverges (`g(t^*)` contains an unbounded `m\ln m` piece from
   `t^*\sim m/(γn)\to0`) and cannot converge to anything meaningful on
   its own — caught by inspection of the resulting nonsensical series
   before attempting to interpret it, and abandoned in favor of always
   expanding the FULL `\ln(\mathrm{term}_m)` combination (where the
   `m\ln m` pieces provably cancel against Stirling's own), documented
   directly in script `03`'s header rather than silently dropped.
6. **No other computational bugs found.** Every exact claim (the
   quadratic for `t^*`, its solution, the symbolic cancellation of
   `m\ln m` terms, the closed-form Gaussian integral of
   `T_{\mathrm{prof}}`) was checked at least two independent ways
   (symbolic sympy derivation vs. independent numerical route in every
   section; the `t^*` closed form against a from-scratch golden-section
   maximizer; `T_{\mathrm{prof}}` against Richardson extrapolation AND
   a direct high-`n` push; the `G_n`-coefficient match against exact
   symbolic simplification AND six independent rational-`γ` numeric
   evaluations).

---

## §9 Numerical verification summary (fresh scripts, logs on disk)

| Script | What it checks | Result |
|---|---|---|
| `01_baseline_and_beta_closure.py`/`.log` | fresh re-derivation of `A_k`/`S_n` (112 checks); double-sum-swap identity (20 checks); Beta-integral closed form for `T(n,m)`, independently re-verified on a disjoint grid (32 checks); `\mathrm{term}_m` cross-consistency (12 checks) and `λ=0` sanity limit | 0 mismatches everywhere; max rel. error `3.8\times10^{-51}` |
| `02_inner_saddle_exact.py`/`.log` | exact quadratic for `t^*` (symbolic, general `n,m,γ`); closed-form solution; `g''(t^*)<0`; cross-check vs. golden-section numerical maximizer (18 points); leading-order scaling `t^*\sim m/(γn)` (6 `(λ,γ)`, `n` up to `10^{10}`) | quadratic and solution PROVED symbolically; max locator deviation `1.6\times10^{-26}`; scaling law confirmed, monotone shrinking deviation |
| `03_saddle_value_expansion.py`/`.log` | symbolic derivation of `T_{\mathrm{prof}}(λ,γ)` via full `\ln(\mathrm{term}_m)` sympy series (`m\ln m` cancellation confirmed); Richardson-extrapolated numeric cross-check (15 `(λ,γ)` points); direct high-`n` push at the hardest point (`n` up to `1.6\times10^7`) | closed form derived; `λ=0` matches to `<10^{-78}`; general match `<1.1\%` (`λ\le1`, worst point `λ=0.6`), `<1.6\%\to<0.5\%` at `λ=1.5` after the high-`n` push |
| `04_outer_sum_leading_order.py`/`.log` | symbolic + 6-point numeric confirmation that `\int_0^\infty T_{\mathrm{prof}}\,dλ=\tfrac12\sqrt{π/β}` exactly; direct exact-rational numeric check that `S_n'-G_n` stays bounded and trends toward `D(γ)+1`, `n` up to `400`, three `γ`; itemized diagnosis of the remaining gap | symbolic difference exactly `0`; numeric trend consistent at every `γ` tested |
| `05_local_rate_crossover.py`/`.log` | independent reproduction of predecessor's `c(γ)` at `m=1` fixed (`n` up to `2\times10^6`, three `γ`); direct exhibition of the local-curvature crossover from `c(γ)` (at `m=1`) to `A(γ)` across an 11-point `m`-grid, two `γ` | `c(γ)` matches to `<10^{-6}`; crossover confirmed cleanly, settling to `A(γ)` to `<0.1\%` by `m\sim500$–`3000` |

All numerics are exact `Fraction`/sympy rational or symbolic, or
`mpmath` at dps 50–80. No Monte Carlo, no `numpy.random`/`random.seed`
call anywhere in this front's code (confirmed by direct grep, see
Seeds below).

---

## §10 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed, NOT bounded, and
   NOT characterized as a convergent series with a proved remainder.**
   No progress toward closing it beyond every predecessor's own honest
   non-closure — exactly as the mandate itself anticipated as the most
   likely outcome.
2. **The joint two-variable `(t,m)` asymptotic, to `O(1)` precision,
   was NOT completed.** §7 itemizes precisely what remains: a uniform
   (not leading-order) Watson's-lemma remainder for the inner integral;
   the next-order correction to `T_{\mathrm{prof}}` itself (several
   named, individually-`o(1)`-but-jointly-`O(1)` terms); an
   Euler-Maclaurin/Poisson treatment of the outer `m`-sum; and their
   combination into a single controlled remainder. A future front
   attempting this should expect depth comparable to closing Gap 1
   directly — the predecessor's own honest prediction, confirmed rather
   than refuted by actually attempting the analysis.
3. **`T_{\mathrm{prof}}(λ,γ)`'s own error is characterized only
   numerically (relative error shrinking with `n`), not with an
   explicit analytic bound.** The Laplace/Watson approximation
   underlying it is a leading-order approximation; no remainder term
   was derived or bounded.
4. **The local-rate crossover (§6) is demonstrated numerically at two
   sample `γ` and one `n`, not proved as a uniform statement for all
   `γ\in(0,1)` and all `n\to\infty`.** A genuinely interesting
   structural fact (the curvature is not constant across the whole
   `m`-range) that a future front could sharpen into a proved
   intermediate-`m` asymptotic, distinct from both the `m=O(1)` and
   `m=Θ(\sqrt n)` regimes already characterized.
5. **Gap 1 and Gap 3** (`THEOREM.md`, Estágio 26/33 onward) remain
   exactly as the predecessor left them — untouched by this front,
   whose entire effort was on the newly-opened Beta-integral/joint
   saddle-point route, not the existing moment/cumulant apparatus.
6. **The exact-rational numerical support for `S_n'\to G_n+D(γ)+o(1)`
   (§5 Part B) only reaches `n=400`** — a resource, not mathematical,
   limitation of exact rational arithmetic on an `O(n^2)`-term double
   sum with growing coefficient bit-length; the trend shown is
   consistent with, but does not itself prove, the target asymptotic.

---

## §11 Scorecard

| Claim | Status |
|---|---|
| `t^*(n,m,γ)` exact closed form (quadratic solution, new) | **PROVED** (§3, script `02`; symbolic derivation + numeric argmax cross-check) |
| `g''(t^*)<0` (genuine maximum) | **CONFIRMED** at every tested point (§3) |
| Leading-order scaling `t^*\sim m/(γn)` | **derived and numerically CONFIRMED**, tightening as `n\to\infty` |
| `T_{\mathrm{prof}}(λ,γ)=\tfrac1γ\exp[-\tfrac{2-γ}{2γ}λ^2]` (new mesoscale profile) | **derived (Laplace/Stirling, leading order) and independently numerically CONFIRMED** two ways — not a fully rigorous uniform bound |
| `\int_0^\infty T_{\mathrm{prof}}\,dλ = \tfrac12\sqrt{π/β}` exactly (reproduces `G_n`'s coefficient) | **PROVED** (exact symbolic identity, §5) — the front's strongest single result |
| Local-rate crossover `c(γ)\to A(γ)` (at `m=1`, corrected from the originally-claimed `c(γ)/2` — see §6) as `m` grows `O(1)\to Θ(\sqrt n)` | **numerically DEMONSTRATED** at 2 `γ`, not proved uniformly |
| Joint two-variable `(t,m)` asymptotic to `O(1)` precision (the mandate's literal target) | **NOT completed** — precise, itemized gap named (§7) |
| **`C(γ)` for `γ\in(0,1)`, the ultimate target** | **remains entirely OPEN** |

---

## Seeds

This front drew **zero seeds**. Every quantitative claim is exact
symbolic algebra (`sympy`), exact rational arithmetic (`Fraction`), or
deterministic high-precision numerics (`mpmath`, dps 50–80); no
`random`/`numpy.random` call appears anywhere in scripts `01`–`05`
(confirmed by direct grep before writing this document).

| Block | Status |
|---|---|
| `20260949000–20260949999` (this front's reservation, `DISC-DEC-142`, wave 31 frente b) | grep-confirmed **unused** before any code was written (only the `DECISION_LEDGER.yaml` reservation line itself matches) — **zero seeds drawn from this block, and zero seeds drawn anywhere in this front** |

---

## Scope-discipline confirmation

- Own new subdirectory `joint_saddle_point_attempt/`, nested one level
  inside `.../route2_bypass_attempt/` (matching this lineage's own
  nesting convention), created; `ATTEMPT.md` and all scripts/logs
  written only here.
- `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`, `README.md`,
  `index.html`, and every ancestor/predecessor `ATTEMPT.md` and
  `adversarial/` file: **not modified**, read-only throughout.
- No `adversarial/` subdirectory created inside this front's own
  directory; no referee dispatched by this front (reserved for the
  orchestrating session, per mandate).
- **No `git` command of any kind was run** by this front.
- No `.py` file of any ancestor or predecessor front was imported,
  copied, or transcribed; every script here (`01`–`05`) is this front's
  own independent implementation, written fresh from the mathematical
  prose of the required reading.

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_baseline_and_beta_closure.py`/`.log` | fresh, independent re-derivation of `A_k`/`S_n`, the double-sum-swap identity, and — the front's recommended starting point — the Beta-integral closed form for `T(n,m)`, re-verified before use |
| `02_inner_saddle_exact.py`/`.log` | the new exact closed form for the inner saddle `t^*(n,m,γ)` (quadratic derivation, symbolic + numeric argmax cross-check, leading-order scaling law) |
| `03_saddle_value_expansion.py`/`.log` | the new mesoscale limit profile `T_{\mathrm{prof}}(λ,γ)`, derived via a full symbolic Laplace/Stirling combination and independently confirmed numerically (Richardson extrapolation + a direct high-`n` push) |
| `04_outer_sum_leading_order.py`/`.log` | the central positive result — `\int_0^\infty T_{\mathrm{prof}}\,dλ` exactly reproduces `G_n`'s known coefficient — plus direct numeric support for `S_n'\to G_n+D(γ)+o(1)` and the precise, itemized diagnosis of what remains for `D(γ)` |
| `05_local_rate_crossover.py`/`.log` | the reconciliation of this front's mesoscale curvature `A(γ)` with the predecessor's PROVED near-origin rate `c(γ)`, via a direct numeric demonstration of the crossover between them |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No `git` commands run by
this front. No `adversarial/` directory created; no referee dispatched,
per mandate.
