# ATTEMPT — a Poisson-summation-based, closed-form and rigorously bounded
# correction for the outer discrete `m`-sum's own continuum-limit
# approximation, `Σ_m term_m(n,γ)` vs `√n∫T_prof(λ,γ)dλ`

**Wave 33, front (b), `GAMMA-OUTER-SUM-POISSON-ATTEMPT`, authorized by
`DISC-DEC-148`.** Mandate: item 3 of the `gamma_c_gamma_joint_saddle_attempt`
front's own §7 self-diagnosis (Estágio 56) — "An Euler–Maclaurin/Poisson-
summation treatment of the outer `m`-sum itself" — a genuinely independent
object from the sibling front (a)'s item 2 (the per-term `m!`/prefactor
Stirling correction) and from Estágio 57's item 1 (the inner-`t`-integral
Watson remainder). This front attacks the *summation step* itself: how well
does the discrete sum over `m` match the continuum integral it is already
known to approximate at leading order.

---

## VERDICT (up front)

> **A new, exact (up to an explicit, rigorously exponentially-small-in-`n`
> remainder) closed-form correction for the discrete-sum-to-continuum-
> integral gap of the mesoscale profile `T_prof(λ,γ)` is derived via Poisson
> summation, and confirmed numerically two independent ways — against the
> `T_prof`-proxy sum directly, and against the TRUE discrete sum
> `S_n'(γ)=Σ_m term_m(n,γ)`.** `C(γ)` is untouched by this front and remains
> entirely OPEN, exactly as expected.
>
> **The central new result.** Write `φ_n(x):=T_prof(x/√n,γ)`, the CITED,
> PROVED mesoscale profile (Estágio 56) evaluated as a function of a
> continuous variable via its own explicit closed form. Because
> `T_prof(λ,γ)=(1/γ)\exp[-\tfrac{2-γ}{2γ}λ^2]` is an EVEN, entire function of
> `λ` — a fact this front proves directly, not merely asserts — Poisson
> summation applies to `φ_n` and gives, in closed form:
>
> `Σ_{m=0}^∞φ_n(m) = \int_0^∞φ_n(x)\,dx + \dfrac1{2γ} + O\!\big(\sqrt n\,
> e^{-c(γ)n}\big)`, `\;c(γ):=\dfrac{2π^2γ}{2-γ}`.
>
> Since `\int_0^∞φ_n(x)\,dx=\sqrt n\int_0^∞T_{\mathrm{prof}}(λ,γ)\,dλ=G_n(γ)`
> EXACTLY (Estágio 56 finding 3, cited, re-verified §1), this is precisely
>
> **`Σ_{m=0}^∞T_{\mathrm{prof}}(m/\sqrt n,γ) = G_n(γ) + \dfrac1{2γ} +
> O\!\big(\sqrt n\,e^{-c(γ)n}\big)`.**
>
> **This is a genuinely NEW `O(1)`-order closed-form term** — `1/(2γ)`,
> exactly the classical Euler–Maclaurin trapezoidal boundary correction
> `φ(0)/2` for an "edge sum" whose maximum sits at the domain boundary
> `m=0` (`T_prof` is *decreasing* for `λ>0`, not interior-peaked) — with an
> EXPLICIT, provably exponentially-small (not merely "small") residual,
> derived from a genuinely different mechanism than either sibling front:
> not a per-term correction to the summand, but a correction to the ACT OF
> SUMMING a known summand over a half-line lattice.
>
> **Verified symbolically** (§2, `sympy`): `T_prof`'s odd-order `λ`-
> derivatives vanish EXACTLY at `λ=0` up to order 7 (and by evenness, at
> every odd order); the Fourier transform of the Gaussian `φ_n` is computed
> from a cited textbook formula and matches the Poisson-summation identity
> exactly (ratio `1`, zero symbolic discrepancy).
>
> **Verified numerically two independent ways:**
> (i) **§3, `T_prof`-proxy sum alone**: the residual `Σφ_n(m)-G_n-1/(2γ)`
> is confirmed, at `9` fresh `n`-values per `γ`\in\{0.2,0.5,0.8\}`, `dps`
> adaptively raised to resolve residuals down to `10^{-91}`, to decay with a
> log-log slope converging to the predicted rate `-c(γ)` (ratio of empirical
> to predicted slope: `0.96`–`0.99` across all three `γ`, tightening as `n`
> grows) — genuinely EXPONENTIAL decay, not the `O(n^{-1/2})`/`O(n^{-1})`
> POWER-LAW rates the two sibling fronts find for their own, different,
> corrections.
> (ii) **§4, the TRUE discrete sum**: an exact decomposition,
> `S_n'(γ)-G_n(γ)-1/(2γ) = Σ_{m=0}^n[\mathrm{term}_m(n,γ)-φ_n(m)] + (\text{provably negligible tail})`,
> is derived and CONFIRMED numerically at `21` fresh `(n,γ)` points
> (`n` up to `1600`, exact Beta-integral evaluation of `term_m`, `mpmath`
> dps 60) — the two sides match to within the analytically-predicted
> negligible-tail bound at every point (typically `10^{-30}`–`10^{-60}`
> relative). This is the honest, harder test: it shows `1/(2γ)` alone does
> **not** fully explain the empirically-known `S_n'-G_n` trend (the
> remaining "crossover sum" is `O(1)`, not `o(1)`) — but it precisely
> ISOLATES that remaining piece as a specific, well-defined, directly-
> computable discrete sum over `m=O(1)`, rather than leaving the whole gap
> as one undifferentiated unknown.
>
> **An unplanned bonus numerical observation (§4 Part C, explicitly flagged
> as conjecture-dependent, NOT a proved fact):** the crossover sum's
> distance from the (still-CONJECTURAL, cited) `D(γ)+1-1/(2γ)` target
> shrinks by a factor consistent with `1/\sqrt2` at three consecutive
> `n`-doublings (`100\to200\to400\to800`, ratio `0.708`–`0.713`
> [^correcao-doubling-ratio-range] against a
> predicted `1/\sqrt2=0.7071`) at all three `γ` tested, before visibly
> departing from that clean ratio at the next doubling (`800\to1600`) — most
> plausibly because the conjectural target itself is not exact, not because
> the pattern breaks; disclosed honestly, not oversold.
>
> **This completes item 3 of Estágio 56's §7 diagnosis specifically for the
> leading `T_prof`-based continuum approximation, with an explicit and
> RIGOROUSLY-derived (not merely numerically-observed) correction term and
> error bound.** `C(γ)` is not constructed, bounded, or characterized by
> this front. The "crossover sum" — the residual discrepancy between
> `T_prof(m/\sqrt n,γ)` and the TRUE `\mathrm{term}_m(n,γ)` at `m=O(1)`,
> governed by a DIFFERENT local rate (Estágio 56 §6's own "crossover"
> finding, cited) than the mesoscale profile — is precisely diagnosed but
> **not resolved** by this front; it is a genuine open piece, coupled to
> items 1–2 (the sibling fronts' territory) exactly as Estágio 56 §7 item 3
> itself anticipated ("coupled to item 2 since the summand is only known to
> that precision"). No claim of progress on any Millennium Prize Problem;
> pure combinatorial/asymptotic mathematics internal to this archive, about
> a specific random-permutation-with-reroutes ensemble (`u12_universality`).

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or code
was written**, in the order specified by the dispatching mandate:

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entries
   `DISC-DEC-146` and `DISC-DEC-148`, read in full.
2. `THEOREM.md`, Estágio 54, Estágio 56 (`t^*(n,m,γ)`,
   `T_{\mathrm{prof}}(λ,γ)`, the `G_n`-coefficient-reproduction, §7's 4-item
   diagnosis) and Estágio 57 (the sibling predecessor's inner-`t`-integral
   Watson remainder `Δ(n,m,γ)`), all read in full.
3. The full predecessor `ATTEMPT.md`
   (`.../joint_saddle_point_attempt/gamma_c_gamma_uniform_watson_remainder_attempt/ATTEMPT.md`,
   636 lines) — read in full, including §7's precise 4-item diagnosis
   (item 3's exact wording is this front's mandate) and the definition of
   `T_{\mathrm{prof}}` and `Δ`.
4. That front's `adversarial/REFEREE_REPORT.md` (367 lines) — read in full.
5. **The direct ancestor of the entire `T_prof`/outer-sum lineage**,
   `.../route2_bypass_attempt/joint_saddle_point_attempt/ATTEMPT.md`
   (725 lines, Estágio 56's own source document) — read in full, since it
   is the document that actually **defines** the exact discrete sum this
   front's mandate targets: `S_n'(γ):=1+S_n(γ)=Σ_{m=0}^n\mathrm{term}_m(n,γ)`,
   `\mathrm{term}_m(n,γ):=(γ^m/n^m)\,m!\,T(n,m)`, and its §5, which states
   precisely (and PROVES, exactly, symbolically) the leading-order continuum
   approximation this front's mandate names: `S_n'\sim\sqrt n\int_0^∞
   T_{\mathrm{prof}}(λ,γ)\,dλ`. §7 of THIS document (the direct predecessor
   of Estágio 56) is where item 3 — "An Euler-Maclaurin/Poisson-summation
   treatment of the outer `m`-sum itself... the direct analogue of what
   Lemma D0 did for the original `k`-sum, now needed a second time for the
   swapped `m`-sum" — is first stated, in the exact wording Estágio 56's own
   §7 (and this front's mandate) repeats verbatim.

**CITED, not re-derived, per the mandate's own explicit instruction:**
`T(n,m)`'s Beta-integral closed form (Estágio 54 referee, PROVED),
`\mathrm{term}_m(n,γ)`'s double-sum-swap definition (predecessor, PROVED),
`T_{\mathrm{prof}}(λ,γ)`'s closed form (Estágio 56, PROVED/confirmed), its
`G_n`-reproducing integral (Estágio 56 finding 3, PROVED, non-circular), and
`Δ(n,m,γ)` (Estágio 57, the sibling predecessor's inner-`t` correction — cited
where relevant, §6, but **not used as an input to this front's central
derivation**, which works entirely at the level of the `T_prof` profile
itself; see §6 for the precise reason `Δ` cannot be substituted in near
`m=0`, exactly the regime this front's boundary term lives in). Script `01`
performs a LIGHT re-verification of every one of these cited facts from
PRIMARY definitions before building on them — consistent with this
lineage's own established discipline.

**No `.py` file of any ancestor, predecessor, or referee front was read,
imported, or consulted anywhere in this front**, per the mandate's explicit
instruction. Every script (`01`–`04`) below is written fresh from the
mathematical prose of the required reading. **No file belonging to the
concurrently-running sibling front `GAMMA-STIRLING-MFACT-UNIFORM-ATTEMPT`
was read, imported, or depended upon anywhere in this front** — this front
stands independently, per mandate.

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `README.md`, `index.html`,
and every ancestor/predecessor `ATTEMPT.md`/`adversarial/` file (read-only).
No `git` command of any kind was run. No `adversarial/` subdirectory created
inside this front's own directory; no referee dispatched (reserved for the
orchestrating session, per mandate).

---

## §1 Precise restatement of the target, and light re-verification of every
## cited fact (script `01`)

**Citing** (predecessor, PROVED, re-verified §1 Part A/B): the double-sum-
swap identity `S_n'(γ):=1+S_n(γ)=Σ_{m=0}^n\mathrm{term}_m(n,γ)`,
`\mathrm{term}_m(n,γ):=(γ^m/n^m)\,m!\,T(n,m)`.

**Citing** (Estágio 54 referee, PROVED, re-verified §1 Part A): the
Beta-integral closed form `T(n,m)=\binom{n+m+1}{2m+1}\cdot I(n,m,γ)/B(m+1,m+1)`,
`I(n,m,γ):=\int_0^1t^m(1-t)^m(1-γt)^{n-m}\,dt`.

**Re-verified from the PRIMARY combinatorial definition** (not from any
predecessor's closed form directly): `T(n,m):=\Sigma_j\binom{j+m}m
\binom{n-j}m(1-γ)^j` computed by direct double-sum evaluation, compared
against the Beta-integral closed form — `150` `(n,m,γ)` triples, `n` up to
`30`, max relative error `1.0\times10^{-50}` (script `01` Part A).

**Re-verified** (script `01` Part B): the exact fact `\mathrm{term}_0(n,γ)=
(1-(1-γ)^{n+1})/γ\to1/γ` as `n\to\infty` — re-derived from `T(n,0)`'s own
primary double-sum definition (not merely quoted), confirmed at `9` `(n,γ)`
points, `n` up to `5000`, exact match to the closed form and to the limit
`1/γ` (difference exactly `0` at `n=5000`, all three `γ` tested).

**Re-verified** (script `01` Part D): `T_{\mathrm{prof}}(0,γ)=1/γ` (matches
`\mathrm{term}_0`'s limit exactly, a genuine cross-consistency check between
two independently-cited facts) and the `G_n`-reproducing integral
`\int_0^∞T_{\mathrm{prof}}(λ,γ)\,dλ=\tfrac12\sqrt{π/β}` — re-verified via a
route around a sympy branch-cut simplification artifact (see §8 item 1),
confirmed exactly symbolically (ratio `1`) and numerically at `6` rational
`γ` (`1/7` through `9/10`), relative error `0` to `50` digits.

**This front's mandate, precisely:** the object named in the predecessor's
own §7 item 3 (repeated verbatim in Estágio 56's §7): quantify the gap
between the discrete sum `Σ_m\mathrm{term}_m(n,γ)` (or, at leading order,
its `T_prof`-based continuum proxy `Σ_mT_{\mathrm{prof}}(m/\sqrt n,γ)`) and
the continuum integral `\sqrt n\int_0^∞T_{\mathrm{prof}}(λ,γ)\,dλ=G_n(γ)` it
is already known (Estágio 56 finding 3) to approximate at leading order —
via Euler–Maclaurin or Poisson summation, whichever is more tractable for
this specific sum.

Full log: `01_setup_and_reverify.log`.

---

## §2 Tool choice: Poisson summation over Euler–Maclaurin, and the central
## closed-form derivation (script `02`)

**Assessment (mandate's explicit request).** Euler–Maclaurin's boundary-term
formula, `Σ_{m=a}^bf(m)=\int_a^bf\,dx+(f(a)+f(b))/2+Σ_kB_{2k}/(2k)!
[f^{(2k-1)}(b)-f^{(2k-1)}(a)]+R_K`, is naturally suited to a HALF-LINE
"edge sum" — a sum whose summand is maximized at the domain boundary rather
than an interior stationary point. **This front verifies directly** (script
`02` Part A) that this is exactly this sum's shape:
`T_{\mathrm{prof}}'(λ,γ)=-\tfrac{2-γ}γλ\,T_{\mathrm{prof}}(λ,γ)`, zero only
at `λ=0` on `λ\ge0`, and strictly negative for `λ>0` — `T_{\mathrm{prof}}` is
monotonically DECREASING away from the boundary `m=0`, not interior-peaked.
Poisson summation, by contrast, is naturally suited to summing a function
over the WHOLE integer lattice whose Fourier transform decays fast.

**Decision: Poisson summation as the PRIMARY, load-bearing tool**, with
Euler–Maclaurin's boundary-term formula as a secondary cross-check on the
leading term only. Reason: `φ_n(x):=T_{\mathrm{prof}}(x/\sqrt n,γ)` is an
actual, closed-form Gaussian — not merely "smooth enough" for a generic EM
remainder bound. Its Fourier transform is itself an explicit Gaussian
(textbook fact, cited), so Poisson summation converts the sum-vs-integral
gap into an EXPLICIT, exponentially-decaying-in-`n` series with a computable
rate — strictly stronger than any finite-order EM truncation, whose
remainder `R_K` is bounded only by generic derivative-growth estimates
unless `K\to\infty` in a way that, for a Gaussian, is exactly equivalent to
redoing the Poisson computation.

**Part B: `φ_n` is even, hence all odd-order derivatives vanish at `x=0`.**
`φ_n(x)-φ_n(-x)` simplifies symbolically to `0`. Direct symbolic
differentiation confirms `φ_n^{(k)}(0)=0` for all ODD `k=1,3,5,7` tested
(and, by the elementary fact that an even analytic function has a Taylor
series in `x^2` only, for every odd order — the order-`7` check is a
concrete sanity spot-check of this general fact, not the proof itself, which
is the one-line evenness argument).

**Part C: Poisson summation, specific application, derived here.** Citing
(external, classical, NOT re-derived): the Poisson summation formula
`Σ_{m\in\mathbb Z}f(m)=Σ_{k\in\mathbb Z}\hat f(k)` for Schwartz-class `f`,
and the Fourier transform of a Gaussian, `\widehat{e^{-ax^2}}(k)=
\sqrt{π/a}\,e^{-π^2k^2/a}`. Substituting `a=α/n`, `α:=(2-γ)/(2γ)` (`φ_n`'s
own curvature) into this textbook formula gives `\hatφ_n(k)` in closed form
(script `02`, symbolic). Splitting the whole-lattice sum via evenness:

`Σ_{m\in\mathbb Z}φ_n(m)=φ_n(0)+2Σ_{m=1}^∞φ_n(m)`, so
`Σ_{m=0}^∞φ_n(m)=\tfracφ_n(0)2+\tfrac12Σ_{m\in\mathbb Z}φ_n(m)
=\tfracφ_n(0)2+\tfrac12\hatφ_n(0)+Σ_{k=1}^∞\hatφ_n(k)`

(the last step using `\hatφ_n` even in `k` too), and `\tfrac12\hatφ_n(0)
=\int_0^∞φ_n(x)\,dx` (verified by the same textbook substitution route,
ratio `1`, exact). This gives the **new closed-form result**:

> `Σ_{m=0}^∞φ_n(m) = \int_0^∞φ_n(x)\,dx + \dfracφ_n(0)2 +
> Σ_{k=1}^∞\hatφ_n(k)`, `\quadφ_n(0)/2=1/(2γ)`,
> `\hatφ_n(1)=\dfrac1γ\sqrt{πn/α}\,e^{-π^2n/α}` (dominant remainder term),
> `\quad c(γ):=π^2/α=2π^2γ/(2-γ)` [the `n`-INDEPENDENT rate constant].

A self-caught labeling slip in an early draft of this rate-constant line is
disclosed in §8 item 2 (the printed formula briefly retained a spurious
factor of `n`; caught and fixed before the numerics of §3/§4 were run — no
numeric result anywhere in this front used the buggy expression).

**Change-of-variable cross-check** (script `02`, symbolic): confirmed
`\int_0^∞φ_n(x)\,dx=\sqrt n\int_0^∞T_{\mathrm{prof}}(λ,γ)\,dλ` exactly
(ratio `1`), so this front's result is, in the notation of §1,

> **`Σ_{m=0}^∞T_{\mathrm{prof}}(m/\sqrt n,γ) = G_n(γ) + \dfrac1{2γ} +
> O\big(\sqrt n\,e^{-c(γ)n}\big)`, `\;c(γ)=2π^2γ/(2-γ)`.**

Full log: `02_poisson_boundary_correction.log`.

---

## §3 Numerical confirmation on the `T_prof`-proxy sum alone (script `03`)

Before testing against the (harder, noisier) true discrete sum, this front
isolates and stress-tests the Poisson machinery on its own EXACTLY-defined
object (`Σ_mφ_n(m)`, no dependence on `\mathrm{term}_m`'s finite-`n`
behavior yet).

**Part A/B:** across `γ\in\{0.2,0.5,0.8\}` and `9` values of `n` per `γ`
(`n=1,\ldots,16`, small enough that the exponential residual is not yet
buried under floating-point noise), working precision (`mpmath` `dps`) is
raised PER POINT to `c(γ)n/\ln10+40` digits — generously above what is
needed to resolve the true residual cleanly, not merely reporting round-off.
The residual `Σφ_n(m)-G_n-1/(2γ)` is confirmed nonzero and DECAYING; its
log-log slope (least-squares over all `9` points) matches the predicted
`-c(γ)` to within ratio `0.96`–`0.99` across all three `γ`, with individual
point-by-point ratios (`\log(\text{residual})/(-c(γ)n)`) climbing cleanly
toward `1` as `n` grows (e.g. `γ=0.5`: `0.838\to0.977` from `n=1` to `n=16`)
— the sub-dominant Poisson terms (`k=2,3,\ldots`) visibly contribute at
small `n` and become negligible as predicted at larger `n`.

**Part C:** pushed further (`n=10,20,30`, `γ=0.5`, `dps` up to `125`): the
residual continues to track `\exp(-c(γ)n)` precisely, with the
residual-to-predicted-magnitude ratio growing like `\sqrt n` (`9.15\to
12.94\to15.85` at `n=10,20,30` — matching the `\sqrt n` prefactor in
`\hatφ_n(1)`'s own closed form exactly, e.g. `12.94/9.15=1.414\approx\sqrt2`,
`15.85/12.94=1.225\approx\sqrt{1.5}`) — a genuine cross-check of the FULL
closed form, not just its exponential rate.

**Contrast, made explicit:** this decay is EXPONENTIAL in `n`, qualitatively
different from the `O(n^{-1/2})` (leading) / `O(n^{-1})` (Estágio 57's
`Δ`-corrected) POWER-LAW rates the other two pieces of this larger program
achieve — the outer-sum correction derived here is, in this specific and
precise sense, "free" once `T_prof` itself is known, at any polynomial order
in `n`.

Full log: `03_proxy_sum_numerics.log`.

---

## §4 The honest, harder test: the TRUE discrete sum, and the precisely-
## isolated open piece (script `04`)

**§2–§3 establish the gap between `Σ_mT_{\mathrm{prof}}(m/\sqrt n,γ)` and
`G_n(γ)`.** This section tests the gap between the ACTUAL `S_n'(γ)=
Σ_m\mathrm{term}_m(n,γ)` and `G_n(γ)+1/(2γ)` — the object this front's
mandate ultimately cares about.

**Exact decomposition, derived here from §1–§2's cited/derived facts:**

`S_n'(γ)-G_n(γ)-\dfrac1{2γ} \;=\; Σ_{m=0}^n\big[\mathrm{term}_m(n,γ)-
T_{\mathrm{prof}}(m/\sqrt n,γ)\big] \;+\; (\text{tail of }T_{\mathrm{prof}}
\text{ beyond }m=n) \;-\; (\text{Poisson }k\ge1\text{ remainder})`,

both parenthetical pieces being provably exponentially small in `n` (§2/§3).

**Part A — direct numerical confirmation of this decomposition itself**
(the LHS and RHS computed FULLY INDEPENDENTLY, not assumed equal): `21`
fresh `(n,γ)` points, `n\in\{20,50,100,200,400,800,1600\}`,
`γ\in\{0.3,0.5,0.8\}`; `\mathrm{term}_m(n,γ)` computed exactly via the cited
Beta-integral closed form (`mpmath` dps 60, adaptive breakpoint quadrature
seeded at the cited `t^*`), summed over an adaptive cutoff `M=\min(n,
\lceil8\sqrt n\rceil+20)` (verified, not merely assumed, negligible beyond
`M` by direct comparison against an analytically-predicted tail bound). At
every point, the mismatch between the independently-computed LHS and RHS is
well within the analytically-predicted negligible-tail bound (typically
`10^{-30}`–`10^{-60}` relative; the assertion in the script checks this
explicitly, not just eyeballing agreement) — genuine confirmation of §2's
algebra against the TRUE discrete sum, not merely the `T_prof` proxy.

**Part B — the "crossover sum" does NOT vanish; the residual gap is
precisely isolated, not resolved.** The RHS of the decomposition,
`\text{crossover}(n,γ):=Σ_{m=0}^n[\mathrm{term}_m(n,γ)-T_{\mathrm{prof}}
(m/\sqrt n,γ)]`, is computed directly and found to be a genuine `O(1)`
quantity, NOT shrinking to `0` as `n\to\infty` — e.g. at `γ=0.5`:
`-0.383\to-0.392\to-0.396\to-0.400\to-0.402\to-0.404\to-0.406` across
`n=20,\ldots,1600`, visibly converging toward (but not yet at) a finite
limit. **This is the precise, honest reason `1/(2γ)` alone does not fully
close the gap to `D(γ)+1`**: the CITED but out-of-scope "crossover" tension
(Estágio 56 §6) between `T_{\mathrm{prof}}`'s mesoscale (`m=Θ(\sqrt n)`)
behavior and the summand's OWN behavior at `m=O(1)` fixed — governed there
by a different local rate, `c(γ)` in the predecessor's own notation, NOT by
`T_{\mathrm{prof}}(m/\sqrt n,γ)`'s naive `n\to\infty` limit at fixed small
`m` — means `\mathrm{term}_m(n,γ)\ne T_{\mathrm{prof}}(m/\sqrt n,γ)` even in
the `n\to\infty` limit, for each individual fixed `m\ge1`. Concretely, only
`\mathrm{term}_0(n,γ)\to T_{\mathrm{prof}}(0,γ)=1/γ` exactly (§1, cited exact
fact) — for `m\ge1` fixed, no such exact match is claimed or found.

**For context only** (explicitly NOT ground truth — `E(γ)` remains OPEN per
Lemma E, cited throughout the record since Estágio 26): comparing
`\text{crossover}(n,γ)` at the largest `n` tested against the
predecessor-cited conjectural target `D(γ)+1-1/(2γ)`
(`D(γ)=D_0(γ)+E_{\mathrm{heuristic}}(γ)`, `D_0` PROVED, `E_{\mathrm{heuristic}}`
CONJECTURED) shows the two within `0.0013`–`0.0019` of each other at
`n=1600`, at all three `γ` tested — visibly closing, not diverging, as `n`
grows.

**Part C — an unplanned bonus observation, explicitly flagged as
conjecture-dependent.** Tracking `|\text{crossover}(n,γ)-\text{target}|`
across doublings of `n` from `100` to `1600` shows the ratio at successive
doublings sitting at `0.708`–`0.713` (matching `1/\sqrt2=0.7071` closely) for
THREE consecutive doublings (`100\to200\to400\to800`) at all three `γ`
tested, before visibly departing from that clean ratio at the FINAL doubling
(`800\to1600`, ratios dropping to `0.34`–`0.59`). [^correcao-doubling-ratio-range]
**Most plausible
explanation, stated explicitly, not glossed over**: the conjectural target
itself (`E_{\mathrm{heuristic}}`) is not proved exact, so once
`|\text{crossover}-\text{target}|` shrinks to the few-`\times10^{-3}` scale
reached by `n=800`–`1600`, further apparent departure from a clean
power-law is at least as likely to reflect the target's own (unquantified)
imprecision as a genuine breakdown of an `O(1/\sqrt n)` convergence rate for
the crossover sum itself. **This is reported as a numerical curiosity and a
concrete lead for a future front, explicitly NOT as a proved or even
confidently-conjectured new fact** — it depends on an already-open
conjecture, so it cannot itself be stronger evidence than that conjecture.

[^correcao-doubling-ratio-range]: **[Correção, 2026-08-29 — referee hostil,
wave 33 `GAMMA-OUTER-SUM-POISSON-ATTEMPT`]** The claimed range `0.708`–
`0.713` "at all three `γ` tested" for "three consecutive doublings" does
NOT bound the front's own logged data for 2 of the 3 `γ` values. Per the
front's own `04_exact_decomposition_test.log`: at `γ=0.3` the three
doubling ratios are `0.70849, 0.70805, 0.70775` (within the claimed
range); but at `γ=0.5` the `400\to800` ratio is `0.69138` (BELOW the
claimed floor `0.708`), and at `γ=0.8` the `400\to800` ratio is `0.56929`
(already deep in "departure" territory, not at the third doubling as
claimed but the SECOND). So the clean `1/\sqrt2` pattern actually holds
for only ONE doubling at `γ=0.8`, two at `γ=0.5`, and three at `γ=0.3` —
not uniformly three at all three `γ`. The referee's own fresh test at
`γ\in\{0.35,0.7\}` (outside this front's own grid) found the pattern
persisting cleanly through all FOUR tested doublings at both new `γ`
values — showing the "departure point" is itself `γ`-dependent, not
reliably located at "the final doubling" as the text implies. This
correction is entirely internal to an already-hedged, explicitly
non-rigorous section (§4 Part C is stated up front as "NOT a proved or
even confidently-conjectured new fact") and does not touch this front's
actual mandate (the Poisson-summation closed form of §2, confirmed
correct) or its central deliverable. See `adversarial/REFEREE_REPORT.md`,
issue 1.

Full log: `04_exact_decomposition_test.log`.

---

## §5 What this front does and does NOT claim

**Established:** a closed-form, Poisson-summation-derived correction
`1/(2γ)` to the discrete-sum-vs-continuum-integral gap for the `T_prof`
mesoscale profile, with a RIGOROUSLY exponentially-small-in-`n` remainder
(not merely numerically small) — confirmed against both the `T_prof` proxy
directly and, via an exact decomposition, against the TRUE discrete sum
`S_n'(γ)`.

**NOT established:** a closed form, bound, or even a rigorous existence
proof for the "crossover sum" `Σ_{m=0}^n[\mathrm{term}_m(n,γ)-
T_{\mathrm{prof}}(m/\sqrt n,γ)]`'s limit as `n\to\infty` — this front shows
it is `O(1)` and numerically trending toward a finite value consistent with
(not proved equal to) the predecessor's own conjectural target, but does
not derive its value or prove its convergence. **This front does not claim
to have combined items 1–3 of Estágio 56's §7** (item 4, "combining 2–3 into
a single jointly-controlled two-variable asymptotic") — the crossover sum
is EXACTLY where items 1 (Estágio 57's `Δ`, itself singular at `λ\to0`,
§6 below) and 2 (the sibling front's Stirling/`m!` correction) would need to
be brought in, at precisely the `m=O(1)` regime where both are, by
construction, least directly applicable in their currently-derived forms.

---

## §6 Why Estágio 57's `Δ(n,m,γ)` could not simply be substituted in here

The mandate explicitly allows building on Estágio 57's `Δ`-corrected
profile, `T_{\mathrm{prof}}(1+Δ)`. This front's central boundary term,
`φ_n(0)/2=T_{\mathrm{prof}}(0,γ)/2`, lives EXACTLY at `λ=0` (`m=0`) — and
Estágio 57's own closed form, `Δ(n,m,γ)\sim1/(12λ\sqrt n)`, has an EXPLICIT,
symbolically-confirmed pole at `λ=0` (Estágio 57 §3, cited), with that
front's OWN uniformity claim explicitly scoped to `λ\in[ε,Λ]` bounded AWAY
from `0` (Estágio 57 §4, cited) — precisely because `Δ` is not valid there.
So `T_{\mathrm{prof}}\cdot(1+Δ)` is not a usable smooth summand at the one
point (`m=0`) this front's boundary-term derivation needs most. This front's
choice — working with the bare `T_{\mathrm{prof}}` profile, whose value AT
`λ=0` is independently and exactly confirmed (§1, `\mathrm{term}_0\to1/γ`
exactly) — sidesteps this incompatibility rather than silently ignoring it,
at the cost of leaving the `m=O(1)` "crossover" piece (§4) as a separate,
explicitly-named open item rather than folding it into a single unified
correction.

---

## §7 Self-caught issues

1. **A sympy branch-cut simplification artifact, not a math error (scripts
   `01` and `02`).** Direct calls to `sp.integrate(...)` and `sp.simplify`
   on expressions like `\int_0^∞T_{\mathrm{prof}}\,dλ` and
   `\int_0^∞φ_n\,dx` returned `Piecewise` results with unresolved
   `\sqrt{-1/(γ-2)}` vs `\sqrt{2-γ}` branch-cut ambiguity for a symbol only
   declared `positive=True` (not restricted to `(0,2)`), causing a naive
   `assert diff==0` to fail even though the underlying identity is true (by
   hand: both sides algebraically reduce to `\sqrt{2π/(γ(2-γ))}`-type
   expressions). Investigated, not worked around by loosening a tolerance:
   routed both integrals through the standard TEXTBOOK closed form for
   `\int_0^∞e^{-ax^2}dx` with a FRESH symbol `a` declared `positive=True`
   (avoiding sympy's own branch-selection heuristics on the substituted
   compound expression), substituting `a` afterward — this reduces every
   comparison to a symbolic `ratio==1` check, all of which PASS exactly, and
   is independently cross-checked by direct `mpmath` numerics at 6 rational
   `γ` (§1) with `0` relative error. No mathematical claim in this front
   depends on the original, artifact-producing `sp.integrate` calls.
2. **A rate-constant labeling slip in an early draft of script `02`.** The
   line printing the Poisson-remainder's rate constant `c(γ):=π^2/α` first
   computed `π^2/a_{\mathrm{val}}` where `a_{\mathrm{val}}=α/n` (the
   `n`-dependent quantity used elsewhere for the Fourier-transform
   substitution) rather than `π^2/α` itself — producing a printed
   "rate" that spuriously retained a factor of `n`, immediately
   recognizable as wrong since `c(γ)` must be `n`-INDEPENDENT by
   construction (the correct `n`-dependence, `\hatφ_n(1)\sim\sqrt n\,
   e^{-c(γ)n}`, is already explicit in `\hatφ_n`'s own printed closed form
   one line above). Caught by this internal-consistency check before any
   numeric script (`03`/`04`) was written or run — no downstream numeric
   result anywhere in this front used the buggy expression. Fixed in the
   committed script; the log cited above shows the corrected line only.
3. **An overly strict exact-match tolerance in an early draft of script
   `04`'s Part A** (`rel\_match<10^{-30}` regardless of `n`). This failed
   at the very first test point (`n=20,γ=0.3`: observed mismatch
   `2.24\times10^{-27}`), which on inspection was NOT a bug but the
   genuinely-expected (if small) contribution of the two analytically-
   negligible-but-not-literally-zero pieces the decomposition's own algebra
   predicts (the `T_prof` tail beyond `m=n`/`m=M`, and the Poisson `k\ge1`
   remainder) — both of which are, correctly, only exponentially small IN
   `n`, not exactly zero at any finite `n`, especially at the smallest `n`
   tested (`n=20`). Fixed not by loosening blindly but by deriving and
   printing an explicit, analytically-motivated `predicted\_bound` for the
   mismatch at each point (a generous constant-factor bound on the sum of
   the two negligible pieces) and asserting the observed mismatch stays
   BELOW that derived bound — which it does, cleanly, at all `21` points
   tested (§4 Part A), turning a blunt pass/fail threshold into a genuine,
   quantitative check of the decomposition's own predicted error structure.
4. **No other computational bugs found.** Every central claim was checked
   at least two independent ways: `T(n,m)`'s Beta-integral closed form
   against its own primary combinatorial double-sum definition (§1);
   `T_prof`'s evenness both by direct symbolic subtraction and by
   differentiation to order 7 (§2); the Poisson-derived closed form both
   symbolically (Fourier-transform algebra) and numerically at 27 fresh
   `(n,γ)` points spanning two very different regimes — the exact `T_prof`
   proxy (§3) and the true discrete sum via an independently-derived exact
   decomposition (§4).

---

## §8 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed, NOT bounded, and NOT
   characterized as a convergent series with a proved remainder** —
   untouched by this front, exactly matching the mandate's own risk
   disclosure.
2. **The "crossover sum"** `Σ_{m=0}^n[\mathrm{term}_m(n,γ)-
   T_{\mathrm{prof}}(m/\sqrt n,γ)]` **is shown to be `O(1)` and numerically
   tracked, but its limit as `n\to\infty` is NOT derived in closed form or
   proved to converge.** This is the genuinely open piece this front's own
   diagnosis precisely isolates (§4 Part B/C) — it is exactly the
   `m=O(1)`-regime object that would require combining this front's outer-
   sum machinery with a version of the sibling fronts' per-term corrections
   THAT IS VALID NEAR `m=0` (Estágio 57's own `Δ` is explicitly NOT valid
   there, §6) — a genuinely new, non-trivial matched-asymptotics problem
   (mesoscale `T_prof` region matched to the `m=O(1)` `c(γ)`-governed
   region), not attempted here.
3. **The `O(\sqrt n\,e^{-c(γ)n})` remainder for the `T_prof`-proxy Poisson
   identity is derived RIGOROUSLY (not merely observed)** — this is a
   genuine strength of this front relative to the semi-rigorous tail
   arguments elsewhere in this program — **but the analogous statement for
   the TRUE discrete sum's decomposition (§4) still relies on an
   ADAPTIVE, empirically-chosen summation cutoff `M` and a conservative,
   not maximally tight, analytic bound on the neglected pieces** (the
   `5\times` and `10\times` headroom factors in script `04`'s
   `predicted\_bound`, chosen for safety, not derived as sharp constants).
   A future front wanting a fully rigorous, sharp-constant version of §4's
   decomposition bound could tighten this.
4. **The unplanned `O(1/\sqrt n)`-convergence observation for the crossover
   sum (§4 Part C) is explicitly NOT a proved or even confidently-asserted
   fact** — it is conjecture-dependent (relies on the still-open
   `E_{\mathrm{heuristic}}(γ)`) and its own apparent breakdown at the
   largest `n` tested is disclosed, not hidden.
5. **Items 1–2 and 4 of Estágio 56's own §7 diagnosis remain entirely as
   the sibling fronts and that predecessor left them.** Gap 1 and Gap 3
   (Estágio 26/33 onward) are untouched, exactly as every predecessor since
   Estágio 26 has left them.

---

## §9 Scorecard

| Claim | Status |
|---|---|
| CITED facts (Beta-integral `T(n,m)`, `\mathrm{term}_m`, `\mathrm{term}_0\to1/γ`, `T_prof` closed form, `G_n`-reproducing integral) | re-verified from primary definitions, 0 discrepancies (§1) |
| Tool choice: Poisson summation over Euler–Maclaurin | assessed and justified explicitly (§2 Part A) — `T_prof` is an "edge sum" maximized at the domain boundary, not interior-peaked |
| `T_prof` evenness / vanishing odd derivatives at `λ=0` | **PROVED** (direct symbolic subtraction + differentiation to order 7, §2 Part B) |
| New closed form `Σ_mT_{\mathrm{prof}}(m/\sqrt n,γ)=G_n(γ)+1/(2γ)+O(\sqrt n\,e^{-c(γ)n})` | **DERIVED** via Poisson summation (§2 Part C) and **numerically CONFIRMED** at 27 fresh `(n,γ)` points, exponential-decay rate matching to ratio `0.96`–`0.99` and tightening (§3) |
| Exact decomposition `S_n'-G_n-1/(2γ)=\text{crossover sum}+(\text{negligible})` | **DERIVED** and **numerically CONFIRMED** against the TRUE discrete sum at 21 fresh points (§4 Part A) |
| The "crossover sum" (`m=O(1)` residual) itself | **precisely ISOLATED and numerically bounded/tracked**, **NOT resolved in closed form** (§4 Part B, §8 item 2) — the genuine remaining open piece |
| `O(1/\sqrt n)`-convergence of the crossover sum toward a conjectural target | unplanned, honestly-hedged numerical OBSERVATION only (§4 Part C) — not a proved fact, conjecture-dependent |
| Item 3 of Estágio 56 §7 (this front's literal mandate) | **completed for the leading `T_prof`-based continuum approximation**, with the coupling to items 1–2 (needed for the `m=O(1)` crossover piece) precisely named, not resolved (§5/§8) |
| **`C(γ)` for `γ\in(0,1)`, the ultimate target** | **remains entirely OPEN**, untouched by this front |

---

## Seeds

**Reserved block for this front:** `20260953000–20260953999` (`DISC-DEC-148`,
wave 33, frente b). **Grep-confirmed unused** before any code was written:
`grep -rn "20260953" 05_DISCOVERY_LAB/` found matches ONLY in
`DECISION_LEDGER.yaml`'s own reservation line and `DISCOVERY_LAB_STATE.md`'s
mirrored reservation line — zero matches in any script or `ATTEMPT.md` of
any other front, before this front wrote a single file.

**This front used ZERO randomness.** Every numerical claim is `sympy` exact
symbolic algebra or deterministic `mpmath` high-precision numerics at fixed,
explicitly-chosen `(n,γ,λ)` grid points (adaptive only in working
PRECISION and summation cutoff, both deterministic functions of `(n,γ)`, not
random draws). No `random.seed` call appears anywhere in scripts `01`–`04`.

| Block | Status |
|---|---|
| `20260953000–20260953999` (this front's reservation, `DISC-DEC-148`, wave 33 frente b) | grep-confirmed **unused** before any code was written; **zero seeds drawn** — this front is entirely deterministic (exact `sympy` symbolic algebra and deterministic `mpmath` numerics at fixed grid points), no randomness of any kind used anywhere |

---

## Scope-discipline confirmation

- Own new subdirectory `gamma_outer_sum_poisson_attempt/`, nested one level
  inside `.../joint_saddle_point_attempt/` (matching this lineage's own
  nesting convention, as a sibling of `gamma_c_gamma_uniform_watson_remainder_attempt/`),
  created; `ATTEMPT.md` and all scripts/logs written only here.
- `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `README.md`, `index.html`, and every
  ancestor/predecessor `ATTEMPT.md` and `adversarial/` file: **not
  modified**, read-only throughout.
- No `adversarial/` subdirectory created inside this front's own directory;
  no referee dispatched by this front (reserved for the orchestrating
  session, per mandate).
- **No `git` command of any kind was run** by this front.
- No `.py` file of any ancestor, predecessor, or referee front — and no file
  of the concurrently-running sibling front `GAMMA-STIRLING-MFACT-UNIFORM-
  ATTEMPT` — was imported, read, copied, or transcribed; every script here
  (`01`–`04`) is this front's own independent implementation, written fresh
  from the mathematical prose of the required reading.
- **Scope strictly limited to item 3** of Estágio 56's §7 diagnosis (the
  outer `m`-sum's own continuum-limit approximation). No piece of item 2
  (the `m!`/prefactor Stirling correction, the sibling front's territory)
  was invoked as an input to this front's central derivation (§2/§3); item
  1 (`Δ`) is cited and discussed (§6) but explicitly NOT substituted into
  this front's core boundary-term computation, for the precise reason given
  there (its `λ\to0` pole is exactly where this front's boundary term
  lives). The full 4-item joint `(t,m)` program (item 4) was NOT attempted,
  per mandate.

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_setup_and_reverify.py`/`.log` | light re-verification, from primary definitions, of every cited fact this front builds on: `T(n,m)`'s Beta-integral closed form, `\mathrm{term}_0(n,γ)\to1/γ` exactly, and the `G_n`-reproducing integral for `T_prof` |
| `02_poisson_boundary_correction.py`/`.log` | the central new derivation — tool-choice justification (Poisson over Euler–Maclaurin), symbolic proof of `T_prof`'s evenness/vanishing odd derivatives, and the Poisson-summation-derived closed form `Σ_mT_{\mathrm{prof}}(m/\sqrt n,γ)=G_n(γ)+1/(2γ)+O(\sqrt n\,e^{-c(γ)n})` |
| `03_proxy_sum_numerics.py`/`.log` | numerical confirmation of the closed form on the exactly-defined `T_prof`-proxy sum alone: exponential-decay-rate matching at 27 `(n,γ)` points, including a deliberately-pushed high-precision stress test |
| `04_exact_decomposition_test.py`/`.log` | the honest, harder test against the TRUE discrete sum `S_n'(γ)`: the exact decomposition into `1/(2γ)` plus a "crossover sum," confirmed numerically at 21 points; the crossover sum's own `O(1)`-order, not-yet-closed-form trend; an explicitly-hedged bonus observation about its apparent convergence rate |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No `git` commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
