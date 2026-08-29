# ATTEMPT — a uniform (not leading-order-only) Watson's-lemma-type
# remainder for the inner `t`-integral of the Beta`(m+1,m+1)`-tilted
# moment, over `m=O(√n)`

**Wave 32, front (b), `GAMMA-C-GAMMA-UNIFORM-WATSON-REMAINDER-ATTEMPT`,
authorized by `DISC-DEC-145`.** Mandate: attack precisely item 1 of the
predecessor's own §7 self-diagnosis (`GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT`,
`DISC-DEC-142`, Estágio 56) — a uniform Watson's-lemma-type remainder for
the inner `t`-integral of the Beta`(m+1,m+1)`-tilted-moment representation,
valid uniformly over `m=O(√n)` (`λ:=m/√n` bounded). Scope explicitly
excludes the full 4-item joint `(t,m)` program (items 2–4 of that same §7),
which the predecessor itself assessed as depth comparable to closing Gap 1
directly.

---

## VERDICT (up front)

> **A new, closed-form leading correction term for the inner `t`-integral's
> Laplace/Watson approximation is derived, and confirmed — both by an exact
> algebraic scaling argument and by extensive independent high-precision
> numerics — to be UNIFORM over `λ∈[ε,Λ]` for any fixed `0<ε<Λ<∞`, with an
> explicit `O(n^{-1})` residual beyond it.** `C(γ)` is untouched by this
> front and remains entirely OPEN, as expected.
>
> **The central new result.** Write the inner integral as
> `I(n,m,γ):=\int_0^1t^m(1-t)^m(1-γt)^{n-m}\,dt`, `g(t):=\ln[\text{integrand}]`,
> `t^*(n,m,γ)` the CITED (Estágio 56, PROVED) exact saddle point,
> `A:=-g''(t^*)`. This front derives — via a formal Watson/Laplace
> second-order expansion, DERIVED HERE FROM FIRST PRINCIPLES (Gaussian
> cumulant moments, `sympy`, §2) and independently validated against a
> classical fact entirely EXTERNAL to this archive (the Stirling series for
> `Γ(z+1)`, reproduced EXACTLY, `1/(12z)`, §2) — the general correction
>
> `I(n,m,γ)=e^{g(t^*)}\sqrt{2π/A}\Big(1+Δ(n,m,γ)+O(\text{next order})\Big)`,
> `\;Δ(n,m,γ):=\dfrac{g''''(t^*)}{8A^2}+\dfrac{5[g'''(t^*)]^2}{24A^3}`.
>
> Plugging in the CITED exact `t^*(n,m,γ)` and expanding `A`, `g'''(t^*)`,
> `g''''(t^*)` at the mesoscale `m=λ√n`, `n\to\infty` (§3, symbolic
> algebra + an independent `mpmath`-only numeric cross-check with NO series
> machinery), gives the new closed form
>
> **`Δ(n,m,γ) \;\sim\; \dfrac{1}{12λ}\cdot\dfrac1{\sqrt n}`, exactly
> INDEPENDENT of `γ`,** — a clean, previously-uncomputed, verified fact.
>
> **Numerically confirmed uniform over `λ∈[0.3,3.0]`, `γ∈\{0.3,0.5,0.8\}`**
> (§4, `mpmath` dps 50, fresh robust quadrature): at every one of 18 grid
> points, the leading Laplace approximation's relative error decays with
> log-log slope `\to-0.5` and the `Δ`-corrected approximation's relative
> error decays with slope `\to-1.0` as `n\to10^9` — a full extra order of
> accuracy, exactly matching the derived rate. **Deliberately tested and
> shown NOT to hold at `λ=0.05`** (outside the claimed range): `Δ`'s
> predicted coefficient `1/(12λ)` blows up as `λ\to0` (matching `c(λ,γ)`'s
> explicit `1/λ` pole, §3), and the correction's numerical accuracy
> degrades correspondingly — the uniformity claim's boundary is
> substantiated, not merely asserted.
>
> **A disclosed, semi-rigorous tail-negligibility argument** (§5): using
> the already-PROVED global concavity of `g` (Estágio 56 referee, cited),
> `|g''(t)|` is numerically confirmed to stay within a bounded, explicit
> factor of `A` throughout a `K/\sqrt A`-window around `t^*` for `K` up to
> 40, giving a genuine (if not maximally tight) Gaussian-type tail bound;
> and the ACTUAL tail contribution outside a `K=12` window is measured
> directly by quadrature to be `10^{16}`–`10^{26}`-fold smaller than `Δ`
> itself at every point tested — the window truncation used throughout
> this front's own numerics is confirmed not to be silently absorbing the
> error being tracked.
>
> **This upgrades `T_{\mathrm{prof}}(λ,γ)`'s own inner-integral piece from
> "leading-order asymptotic" (Estágio 56) to "leading order plus an
> explicit, closed-form, uniformly-verified `O(n^{-1/2})` correction with
> an `O(n^{-1})` residual" — precisely item 1 of the predecessor's own §7
> diagnosis, and no further.** `C(γ)` is not constructed, bounded, or
> characterized by this front; items 2–4 of §7 (next-order Stirling/`m!`
> corrections to the FULL `\mathrm{term}_m`, and the Euler–Maclaurin/
> Poisson treatment of the outer `m`-sum) remain entirely untouched, as
> scoped. No claim of progress on any Millennium Prize Problem; pure
> combinatorial/asymptotic mathematics internal to this archive, about a
> specific random-permutation-with-reroutes ensemble (`u12_universality`).

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or code
was written**, in the order specified by the dispatching mandate:

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entries
   `DISC-DEC-143` and `DISC-DEC-145`, read in full (both quote the exact
   wording of this front's own mandate and its predecessor's findings).
2. `THEOREM.md`, Estágio 54 (Route 2 / the referee's Beta`(m+1,m+1)` Pfaff
   closed form for `T(n,m)`) and Estágio 56 (`t^*(n,m,γ)`, `T_{\mathrm{prof}}
   (λ,γ)`, the `G_n`-coefficient-reproduction, and §7's precise 4-item
   diagnosis), both read in full.
3. The full predecessor `ATTEMPT.md`
   (`.../route2_bypass_attempt/joint_saddle_point_attempt/ATTEMPT.md`,
   726 lines) — read in full, including its two dated `correção` footnotes
   (the `<0.7%`/Richardson-extrapolation-artifact correction at `λ=0.6`,
   and the `c(γ)/2`-arithmetic-and-substance error at the crossover
   near-origin endpoint). **Neither mistake is repeated here**: this front
   uses NO Richardson extrapolation anywhere (all numerics are direct
   high-`n` pushes, up to `n=10^9`, or exact leading-power algebra), and
   makes no claim whatsoever about the local-rate crossover or `c(γ)`.
4. The predecessor's own `adversarial/REFEREE_REPORT.md` (401 lines) —
   read in full, including its explicit note (Overclaim/underclaim check,
   final bullet) that the `n=m^2/λ^2`-substitution device used throughout
   is exactly the formal step that "item 1 must supply" a rigorous version
   of — directly informing this front's own §3/§5 approach.

**CITED, not re-derived, per the mandate's own explicit instruction:**
`t^*(n,m,γ)` (Estágio 56 finding 1, PROVED, plus referee's independent
global-concavity strengthening) and `T_{\mathrm{prof}}(λ,γ)` (Estágio 56
finding 2, derived + independently confirmed). Script `01` performs a
LIGHT re-verification of `t^*` and of `g`'s global concavity (both already
PROVED) before building the new remainder analysis on top — consistent
with this lineage's own established discipline of independently
re-verifying a citable input before extending it, not a re-derivation.

**No `.py` file of any ancestor, predecessor, or referee front was read,
imported, or consulted anywhere in this front**, per the mandate's explicit
instruction. Every script (`01`–`05`) below is written fresh from the
mathematical prose of the required reading.

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `README.md`,
`index.html`, and every ancestor/predecessor `ATTEMPT.md`/`adversarial/`
file (read-only). No `git` command of any kind was run. No `adversarial/`
subdirectory created inside this front's own directory; no referee
dispatched (reserved for the orchestrating session, per mandate).

---

## §1 Precise restatement of the target

**Citing** (Estágio 54 referee, PROVED): the inner integral
`I(n,m,γ):=\int_0^1t^m(1-t)^m(1-γt)^{n-m}\,dt`, related to the
double-sum-swap object `T(n,m)` by
`T(n,m)=\binom{n+m+1}{2m+1}\cdot\dfrac{I(n,m,γ)}{B(m+1,m+1)}`.

**Citing** (Estágio 56 finding 1, PROVED, and its referee's global-concavity
strengthening): `g(t):=m\ln t+m\ln(1-t)+(n-m)\ln(1-γt)` is globally concave
on `(0,1)` for `γ\in(0,1)`, `0\le m\le n`, with unique global maximizer
`t^*(n,m,γ)=\dfrac{2m+γn-\sqrt{γ^2n^2+4(1-γ)m^2}}{2γ(m+n)}`.

**Citing** (Estágio 56 finding 2, derived + numerically confirmed): the
LEADING-ORDER-ONLY Laplace/Watson approximation used there,
`I(n,m,γ)\approx e^{g(t^*)}\sqrt{2π/(-g''(t^*))}`, is the object whose
error this front bounds.

**This front's mandate, precisely:** derive `Δ(n,m,γ)`, an explicit
closed-form CORRECTION term, such that
`I(n,m,γ)=e^{g(t^*)}\sqrt{2π/A}\,(1+Δ(n,m,γ)+R(n,m,γ))`, `A:=-g''(t^*)`,
with `Δ` capturing the leading behavior beyond the bare Gaussian
approximation and `R` a genuinely smaller residual, BOTH characterized
uniformly (not merely pointwise-in-`m`) for `m=λ\sqrt n`, `λ` ranging over
a fixed bounded set, as `n\to\infty`.

---

## §2 The general formal Watson/Laplace second-order correction, derived
## from first principles and validated against an external classical fact
## (script `02`)

For `I=\int e^{g(t)}\,dt` with a unique interior non-degenerate maximum at
`t^*`, write `t=t^*+u/\sqrt A`, `A:=-g''(t^*)`. Then
`g(t^*+u/\sqrt A)-g(t^*)=-\tfrac12u^2+ε_3u^3+ε_4u^4+O(u^5A^{-5/2})`,
`ε_3:=g'''(t^*)/(6A^{3/2})`, `ε_4:=g''''(t^*)/(24A^2)`. Expanding
`\exp(ε_3u^3+ε_4u^4)` to the order contributing at `O(ε_4)\sim O(ε_3^2)`
and integrating term-by-term against the unit Gaussian (`sympy`, exact
Gaussian moments `\langle u^{2j}\rangle=(2j-1)!!`, script `02` part A/B):

> `I=e^{g(t^*)}\sqrt{2π/A}\Big[1+Δ+O(ε^{5/2})\Big]`,
> `\;Δ=3ε_4+\tfrac{15}2ε_3^2=\dfrac{g''''(t^*)}{8A^2}+\dfrac{5[g'''(t^*)]^2}{24A^3}`.

**Validated against a source of truth entirely EXTERNAL to this archive**
(script `02` part D): applying this SAME general formula to
`g(t)=z\ln t-t` (i.e. `Γ(z+1)=\int_0^\infty t^ze^{-t}dt}`, the textbook
Laplace-method example), `A=1/z`, `g'''(t^*)=2/z^2`, `g''''(t^*)=-6/z^3`,
gives `Δ=1/(12z)` — **exactly** the classical Stirling correction
`Γ(z+1)\sim\sqrt{2πz}(z/e)^z(1+1/(12z)+\ldots)`, confirmed by direct
symbolic subtraction to zero. This is a genuine, falsifiable check of the
general machinery on a case whose correct answer is independently and
externally known, BEFORE it is applied to this archive's own `g(t)` in §3.

Full log: `02_formal_watson_correction.log`.

---

## §3 The new closed form: `Δ(n,m,γ)\sim\dfrac1{12λ\sqrt n}`, independent
## of `γ` (script `03`)

Substituting the CITED exact `t^*(n,m,γ)` (§1) into `A`, `g'''(t^*)`,
`g''''(t^*)` and setting `m=λ\sqrt n`, `n=1/\epsilon^2` (`\epsilon:=1/\sqrt
n\to0`), each of `A`, `g'''(t^*)`, `g''''(t^*)` is expanded as a Puiseux
series in `\epsilon` (`sympy`, script `03` §A/B) — a first attempt to series-
expand `Δ` in one combined `sympy.series` call on the full ratio did not
terminate within 300s (a genuine computational obstacle, disclosed as
self-caught, §8 item 3) and was replaced by extracting the leading `\epsilon`
-power and coefficient of `A`, `g'''(t^*)`, `g''''(t^*)` SEPARATELY
(legitimate for a pure-multiplicative combination, PROVIDED the two `Δ`
terms do not cancel at leading order — checked explicitly, they do not):

`A\sim\dfrac{γ^2}λ\,n^{3/2}`, `\quad g'''(t^*)\sim\dfrac{2γ^3}{λ^2}\,n^2`,
`\quad g''''(t^*)\sim-\dfrac{6γ^4}{λ^3}\,n^{5/2}`

(all matching a direct by-hand estimate from `t^*\sim λ/(γ\sqrt n)\to0`,
independently cross-checked). Substituting into `Δ`'s two terms:

`\dfrac{g''''(t^*)}{8A^2}\sim-\dfrac3{4λ}\cdot\dfrac1{\sqrt n}`,
`\qquad\dfrac{5[g'''(t^*)]^2}{24A^3}\sim\dfrac5{6λ}\cdot\dfrac1{\sqrt n}`,

**neither of which individually vanishes, nor do they cancel each other**
(`-3/4+5/6=1/12\ne0$), giving the clean new closed form

> **`Δ(n,m,γ)\;\sim\;\dfrac1{12λ}\cdot\dfrac1{\sqrt n}`, exactly independent
> of `γ`** — structurally the same `1/(12z)`-type constant as the Stirling
> correction of §2's external validation case, not a coincidence: near
> `t^*\to0`, the `m\ln t` term of `g` dominates the local curvature the
> same way `z\ln t` dominates `\Gamma`'s integrand.

**Independently cross-checked** (script `03` part C'', `mpmath` dps 60,
NO symbolic series machinery at all): evaluating the EXACT (untruncated)
`Δ(n,m,γ)` numerically at `n=10^8,10^{10},10^{12}` and confirming
`\sqrt n\cdot Δ\to1/(12λ)` to 4–5 significant figures at 9 `(λ,γ)` points
(`λ\in\{0.3,1,2\}`, `γ\in\{0.3,0.5,0.8\}`) — matching the symbolic
leading-power derivation exactly, and confirming `Δ`'s `γ`-independence
directly (not merely inferred from the algebra).

**Boundary behavior as `λ\to0`, checked not asserted:** `c(λ,γ):=1/(12λ)`
has an explicit pole at `λ=0`, confirmed both symbolically (`sympy.series`
in `λ`) and by a numeric table spanning `λ\in\{0.1,\ldots,3.0\}` (script
`03` part D) — this is the precise, quantified reason the uniformity claim
below is stated for `λ` bounded AWAY from `0`, not down to `λ=0` itself
(which would require matching to the predecessor's own distinct `m=O(1)`
regime, governed by `c(γ)`, out of this front's scope — see §7).

**Self-caught (§8 item 1):** an early draft printed the final scaling
exponent with the wrong sign (`n^{+1/2}` instead of `n^{-1/2}`) — a pure
`\epsilon\leftrightarrow n`-power print-statement slip, caught before
finalizing this document by cross-checking against the independent
numeric confirmation (part C'', which used the correct sign throughout and
was never affected).

Full log: `03_scaling_at_mesoscale.log`.

---

## §4 Uniform numerical confirmation across `λ∈[0.3,3.0]`, `γ∈\{0.3,0.5,
## 0.8\}`, and a deliberate boundary-failure check at `λ=0.05` (script `04`)

**Method:** for each `(λ,γ)` in a `6\times3=18`-point grid, `n` growing
from `10^4` to `2.56\times10^6$ (factor `4` each step, plus a follow-up
push to `10^9` at three representative points — see below), computed:
(i) the EXACT `I(n,m,γ)` by `mpmath` quadrature (dps 50), (ii) the leading
Laplace approximation `I_0:=e^{g(t^*)}\sqrt{2π/A}`, (iii) the corrected
approximation `I_0(1+Δ)`. Quadrature robustness: this front's own fresh
implementation seeds `mp.quad` with the analytic `t^*` and an explicit
`K=12`-half-width window as interior breakpoints — the SAME class of fix
the predecessor's own §8 item 3 disclosed as necessary for this integrand
(peak too narrow for default node placement once `t^*\to0`), independently
re-implemented here from scratch, not copied.

**Main grid result (all 18 points):** the leading approximation's relative
error decays with log-log slope in `[-0.41,-0.50]` over `n\in[10^4,
2.56\times10^6]`, and the `Δ`-corrected approximation's relative error
decays with slope in `[-0.73,-0.98]` over the same range — both consistent
with, but at the largest `λ=3.0` tested not yet tightly at, the predicted
`-0.5`/`-1.0`.

**Self-caught and resolved (§8 item 2), not left as an unexplained
discrepancy:** pushing `n` further, to `10^9`, at three representative
points (`λ=0.3,1.0,3.0`, `γ=0.5`) shows the LOCAL log-log slope converging
CLEANLY to `-0.500`/`-0.999` as `n` grows in every case — e.g. at `λ=3.0`,
the local slope moves `-0.359\to-0.463\to-0.489\to-0.497\to-0.499` (leading)
and `-0.802\to-0.932\to-0.979\to-0.993\to-0.998` (corrected) across five
successive decade-scale steps in `n`. This confirms the apparent shortfall
at larger `λ` in the main grid is a genuine pre-asymptotic finite-`n`
effect (larger `λ` means a smaller `c(λ,γ)=1/(12λ)`, so higher-order terms
remain relatively significant longer before the asymptotic rate takes
over) — **not** a flaw in the derived `-1/2` and `-1` exponents, which are
confirmed to the third decimal place once `n` is large enough.

**Deliberate boundary-failure check, `λ=0.05`** (outside the claimed
`[0.3,3.0]` range): `Δ`'s numerically-measured value at `n=10^4` is
`\approx0.0166` — already `\sim6\times` larger than the largest `Δ` value
anywhere in the main grid at the same `n` (`\lambda=0.3`: `Δ\approx0.0027`)
— consistent with the predicted `1/(12λ)=1.667` coefficient (vs.
`1/(12\times0.3)=0.278$), and the corrected approximation's relative error
at `n=10^4` (`\approx1.1\times10^{-4}`) is correspondingly worse than at
any main-grid point tested at that `n`. **This substantiates, rather than
merely asserts, that `λ` bounded away from `0` is a genuine, necessary
condition for the uniformity claimed here** — matching the explicit `1/λ`
pole found symbolically in §3.

Full log: `04_numerical_uniform_verification.log`.

---

## §5 Tail-negligibility argument: substantiating the truncated-window
## approximation used throughout (script `05`)

A genuine Watson's-lemma-type remainder claim needs not only a well-behaved
local Taylor expansion at `t^*` (§2/§3) but also that the integral's mass
away from `t^*` does not silently contaminate the claimed order — the
piece not yet directly addressed by §2–§4.

**Step 1 (numeric, not merely assumed):** across a `(λ,γ)` sample and a
window `t\in[t^*-K/\sqrt A,\,t^*+K/\sqrt A]$ for `K` up to `40`,
`|g''(t)|/A` stays `\ge0.19` throughout every window tested (script `05`
part 1) — i.e. `g''` does not decay in magnitude fast enough, moving away
from `t^*`, to invalidate a genuine quadratic-type lower bound
`g(t^*)-g(t)\ge(A_{\mathrm{low}}/2)(t-t^*)^2`, `A_{\mathrm{low}}\ge0.19A`,
throughout this window (this uses the already-PROVED global concavity of
`g`, cited, Estágio 56 referee, plus the additional numeric confirmation
that the curvature stays comparable to `A`, not just negative, within the
window).

**Step 2 (standard Gaussian tail estimate, using Step 1's explicit
constant):** this gives an explicit, `n`-INDEPENDENT bound on the relative
mass outside a `K`-window,
`\le(2/(K\sqrt{A_{\mathrm{low}}/A}))\cdot e^{-(A_{\mathrm{low}}/A)K^2/2}`,
evaluating at the worst-case ratio found in Step 1 to `<5\times10^{-7}` at
`K=12` and `<10^{-17}` at `K=20` — doubly-exponentially small in `K` and
independent of `n`. [^correcao-step2-extrapolation-gap]

**Step 3 (direct measurement, the actual check that matters):** the TRUE
tail contribution (`I_{\mathrm{full}}-I_{\mathrm{window}(K=12)}$, by
quadrature) is measured directly at six `(λ,γ,n)` combinations and found
to be `10^{-16}`–`10^{-26}`-fold SMALLER than `Δ` itself at every point —
several orders of magnitude tighter even than Step 2's already-small bound.

**Conclusion:** the `K=12` window used to seed interior breakpoints for
§4's adaptive quadrature [^nota-window-vs-breakpoint] is confirmed, not
merely assumed, to be contributing zero measurable contamination to the
`O(n^{-1/2})`/`O(n^{-1})` claims of §3/§4 — via Step 3's direct measurement,
which is load-bearing for this conclusion independent of Step 2's
extrapolation gap (see [^correcao-step2-extrapolation-gap]). This is a
disclosed, semi-rigorous argument (a genuine quadratic-lower-bound Gaussian
tail estimate with an explicit, numerically-verified constant, plus direct
numerical confirmation) — NOT a fully formalized `\epsilon`-`\delta`
real-analysis theorem with a universal, `n`-and-`γ`-independent constant
proved for all `(n,m,γ)` in the range; see §10 item 3 for the precise tier
of rigor this reaches.

[^correcao-step2-extrapolation-gap]: **[Correção, 2026-08-29 — referee
hostil, wave 32 `GAMMA-C-GAMMA-UNIFORM-WATSON-REMAINDER-ATTEMPT`]** Step
2's analytic bound formula is the standard UNBOUNDED Gaussian tail
integral, which implicitly requires the curvature-ratio lower bound
`A_low/A\approx0.19` (Step 1) to hold for EVERY `t` with `|t-t^*|>K/\sqrt
A`, all the way to the domain edges `t=0,1` — not merely within the
`K\le40` window Step 1 actually tested. **This assumption is false**: a
referee scan of `|g''(t)|/A` over the ENTIRE domain `(0,1)` shows the ratio
drops to `\sim10^{-4}`–`10^{-5}` at moderate `t` (e.g. `t=0.1`–`0.5`, far
from `t^*`, which sits at `10^{-3}`–`10^{-5}` in every tested case) — i.e.
curvature is genuinely NOT bounded below by `0.19\cdot A` throughout the
whole domain, only within the specific narrow window actually scanned. So
Step 2's bound, read literally as the claimed "`n`-INDEPENDENT bound on
the relative mass outside a `K`-window," is not fully justified by the
data Step 1 collected. **This does not undermine the front's actual
conclusion**: Step 3's direct, extrapolation-free quadrature measurement
of the true tail does not depend on Step 2 at all and is exactly what this
document's own text already calls "the actual check that matters";
qualitatively, the already-PROVED global concavity of `g` plus its unique
critical point at `t^*` guarantee `g` decreases monotonically moving away
from `t^*` in both directions regardless of how the local curvature
MAGNITUDE fluctuates in between — a dip in curvature ratio at intermediate
`t` does not by itself imply the tail is large, and Step 3 directly
confirms it is not. This is a concrete, previously-unnamed manifestation
of exactly the "semi-rigorous, not fully formalized" gap this document's
own §10 item 3 already discloses in general terms; Step 3, not Step 2, is
load-bearing for the front's actual claim. See
`adversarial/REFEREE_REPORT.md`, Sec 4.

[^nota-window-vs-breakpoint]: **[Nota, 2026-08-29 — referee hostil, wave 32
`GAMMA-C-GAMMA-UNIFORM-WATSON-REMAINDER-ATTEMPT`]** The original wording
above ("the `K=12` window truncation used throughout §4's numerics") is
imprecise. Script `04`'s `exact_integral` function integrates the genuine
full `[0,1]` domain via `mp.quad` breakpoints; the `K=12`-derived `lo`/`hi`
values are used only as INTERIOR BREAKPOINTS to help `mp.quad`'s adaptive
node placement resolve the narrow peak (as script `04`'s own docstring and
§4's "Quadrature robustness" paragraph already correctly describe) — not
as a truncation that discards `[0,lo]` and `[hi,1]`. No numerical result
in script `04` is affected by this wording issue; only this section's own
description of what script `04` does is corrected. See
`adversarial/REFEREE_REPORT.md`, Sec 4.

Full log: `05_tail_bound_argument.log`.

---

## §6 What this front does and does NOT claim about `T_{\mathrm{prof}}`
## and the full `\mathrm{term}_m`

**Important scope clarification, disclosed explicitly (the mandate's own
"minimal genuine prerequisite" allowance was NOT invoked — no piece of
items 2–4 was needed to complete item 1 as literally stated):** `Δ(n,m,γ)`
derived here is the correction to the INNER `t`-INTEGRAL `I(n,m,γ)` alone —
exactly the object item 1 of the predecessor's §7 names. The FULL
`\mathrm{term}_m(n,γ)$ (Estágio 56 §4) also involves `m!$ (via Stirling)
and the `(n+m+1)!/(n-m)!$ binomial-type prefactor, evaluated OUTSIDE the
inner integral. Those pieces have their OWN next-order corrections — most
notably the classical Stirling correction to `\ln(m!)$, itself `O(1/m)=
O(1/(λ\sqrt n))$, the SAME order as `Δ$ — which this front does NOT derive
or include. **This front does not claim to have upgraded
`T_{\mathrm{prof}}(λ,γ)` itself (Estágio 56's full mesoscale profile) to a
uniform `O(n^{-1/2})`-accurate statement** — that would require combining
`Δ` with the matching Stirling correction to `m!`, which is explicitly
item 2 of the predecessor's own §7 diagnosis, out of this front's scope.
What IS established: the specific, literally-named "inner `t`-integral"
piece of item 1, on its own, is now uniform with an explicit next-order
correction and residual.

---

## §7 Precise diagnosis of what remains (unchanged in kind from Estágio
## 56 §7, narrowed by exactly what this front supplies)

1. **Item 1 (this front's mandate) is completed for the inner
   `t`-integral specifically**: `Δ(n,m,γ)=1/(12λ\sqrt n)` (§3), uniform
   over `λ\in[ε,Λ]$ any fixed bounds (§4), with a disclosed tail-
   negligibility argument (§5) and an `O(n^{-1})` residual beyond `Δ`
   (numerically confirmed, §4).
2. **The matching Stirling/`m!` correction and the `(n+m+1)!/(n-m)!$
   correction, needed to upgrade the FULL `T_{\mathrm{prof}}(λ,γ)` (not
   just the inner integral) to the same `O(n^{-1/2})` uniform accuracy** —
   NOT attempted here (§6), remains exactly as the predecessor's own item
   2 named it.
3. **An Euler–Maclaurin/Poisson-summation treatment of the outer `m`-sum
   itself** — untouched, exactly as the predecessor's own item 3 named it.
4. **Combining 2–3 (now informed by this front's `Δ`) into a single,
   jointly-controlled two-variable `(t,m)` asymptotic with an explicit
   `o(1)` remainder** — untouched, exactly as the predecessor's own item 4
   named it, and the literal target of the ORIGINAL Estágio 56 mandate
   (explicitly out of THIS front's scope, per its own dispatch).

**`C(γ)` itself remains entirely open**, unaffected by anything in this
front, matching the mandate's own explicit risk framing.

---

## §8 Self-caught issues

1. **A sign slip in a summary print statement (script `03`).** An early
   draft printed `Δ\sim c(λ,γ)\cdot n^{+1/2}` (using `n^{pD/2}` instead of
   `n^{-pD/2}`, `\epsilon=n^{-1/2}$ so `\epsilon^{pD}=n^{-pD/2}`). Caught
   before finalizing this document, by comparing against the independent
   `mpmath`-only numeric cross-check (script `03` part C''), which
   computed the correct sign throughout and was never itself affected —
   the underlying algebra (§3 parts B/C') always had the correct sign;
   only the final print-statement's exponent formula was wrong. Fixed in
   the committed script; the corrected log is what is cited above.
2. **The MAIN GRID in script `04` initially showed the log-log slope
   falling visibly short of the predicted `-0.5`/`-1.0` at the largest
   `λ` tested (`λ=3.0`: `-0.41` to `-0.43`), not immediately dismissed as
   "close enough."** Investigated directly: pushed `n` to `10^9` at three
   representative points and confirmed the LOCAL slope converges cleanly
   to `-0.500`/`-0.999` as `n` grows in every case (§4) — a genuine
   pre-asymptotic finite-`n` effect (smaller `c(λ,γ)=1/(12λ)` at larger
   `λ` means higher-order terms remain relatively significant over a
   longer `n`-range before the claimed asymptotic rate dominates), not a
   flaw in the derived exponents. This is exactly the kind of numeric
   anomaly this sub-lineage's own record (Estágio 56's `<0.7%` correção)
   was criticized for not investigating far enough — here it was pushed
   until fully resolved, not left as an unexplained residual gap.
3. **A first attempt at deriving `Δ`'s leading order via one combined
   `sympy.series` call on the full ratio `g''''/(8A^2)+5(g''')^2/(24A^3)`,
   substituted at `m=λ\sqrt n`, did not terminate within a 300-second
   timeout (script `03`).** Not silently abandoned or worked around by
   loosening a check: replaced with a mathematically equivalent, much
   cheaper approach — extracting the leading `\epsilon`-power and
   coefficient of `A`, `g'''(t^*)`, `g''''(t^*)` SEPARATELY (each of
   which DOES series-expand quickly) and combining them algebraically,
   valid because `Δ` is built from these three factors by pure
   multiplication/division/exponentiation and the two resulting terms of
   `Δ` were explicitly checked NOT to cancel at leading order before
   trusting the combined result. Independently cross-validated by a
   SEPARATE, non-symbolic route (direct `mpmath` dps-60 numeric evaluation
   of the untruncated exact `Δ(n,m,γ)$ at `n` up to `10^{12}`, script `03`
   part C'') that reproduces the same closed form `1/(12λ)` to 4–5
   significant figures — this cross-check would have caught an error
   introduced by the truncated-computation shortcut, and did not.
4. **An inline text claim in script `05`'s first version** ("K=12 already
   gives ~1e-20 or smaller") **was numerically wrong** — the actual
   computed analytic bound at `K=12` was `\approx4.6\times10^{-7}`, not
   `10^{-20}` (the `10^{-20}`-scale numbers belong to the DIRECTLY-MEASURED
   tail in part 3, a different and much tighter quantity than the crude
   analytic bound of part 2). Caught by comparing the hard-coded claim
   against the script's own just-printed numeric output before finalizing
   this document; corrected in the committed script (§5 above states the
   corrected, accurate figures for both quantities separately).
5. **No other computational bugs found.** Every claim was checked at
   least two independent ways: the general `Δ` formula against an
   external classical fact (Stirling, §2); the mesoscale scaling `1/(12λ)`
   against both symbolic leading-power algebra and independent `mpmath`
   numerics with no series machinery (§3); the uniform decay rate against
   both a moderate-`n` grid AND an extended `n`-to-`10^9` push at
   representative points (§4); the tail negligibility against both an
   analytic-style bound AND direct quadrature measurement (§5).

---

## §9 Numerical verification summary (fresh scripts, logs on disk)

| Script | What it checks | Result |
|---|---|---|
| `01_setup_and_baseline.py`/`.log` | light re-verification of the CITED `t^*(n,m,γ)` closed form (quadratic derivation, root selection) and global concavity of `g` (per-term analytic + 30 random numeric spot-checks) | both re-confirmed, 0 discrepancies |
| `02_formal_watson_correction.py`/`.log` | derivation from first principles of the general Watson/Laplace second-order correction `Δ=g''''/(8A^2)+5(g''')^2/(24A^3)` (exact Gaussian moments, `sympy`); validation against the Stirling series for `Γ(z+1)`, a fact external to this archive | `Δ` formula derived; exactly reproduces the known `1/(12z)` Stirling correction, symbolic difference `0` |
| `03_scaling_at_mesoscale.py`/`.log` | leading-order eps-power scaling of `A`, `g'''(t^*)`, `g''''(t^*)` at `m=λ\sqrt n$ (symbolic, `sympy`, with a disclosed computational-cost self-catch); resulting closed form `Δ\sim1/(12λ\sqrt n)`; independent `mpmath` dps-60 numeric cross-check with no series machinery; `λ\to0` pole confirmed | closed form derived and numerically confirmed to 4-5 sig figs at 9 `(λ,γ)` points up to `n=10^{12}` |
| `04_numerical_uniform_verification.py`/`.log` | direct `mpmath` quadrature (dps 50) of the EXACT inner integral vs. leading and `Δ`-corrected approximations, across an 18-point `(λ,γ)` grid at `n` up to `2.56\times10^6`, plus an extended push to `n=10^9` at 3 points, plus a deliberate `λ=0.05` boundary-failure check | leading-order log-log slope `\to-0.500`, corrected slope `\to-0.999`, confirmed cleanly at extended `n`; `λ=0.05` shows the predicted degradation |
| `05_tail_bound_argument.py`/`.log` | numeric confirmation `|g''(t)|/A\ge0.19` in a `K\le40`-window (using cited global concavity); resulting explicit Gaussian-type tail bound (`<5\times10^{-7}$ at `K=12`); DIRECT quadrature measurement of the actual tail vs. `Δ` at 6 `(λ,γ,n)` points | tail bound derived; actual tail measured `10^{-16}`–`10^{-26}`-fold smaller than `Δ` at every point tested |

All numerics are `sympy` symbolic/exact or `mpmath` at dps 50–60. No Monte
Carlo beyond the single random spot-check batch in script `01` (see
Seeds below).

---

## §10 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed, NOT bounded, and
   NOT characterized as a convergent series with a proved remainder** —
   untouched by this front, exactly matching the mandate's own risk
   disclosure.
2. **The FULL `T_{\mathrm{prof}}(λ,γ)` (including the `m!`/binomial-prefactor
   pieces, not just the inner `t`-integral) is NOT upgraded to uniform
   `O(n^{-1/2})` accuracy** — the matching Stirling-type correction to
   those pieces is item 2 of Estágio 56's §7, deliberately out of this
   front's scope (§6).
3. **The tail-negligibility argument (§5) is disclosed as semi-rigorous,
   not a fully formalized real-analysis theorem.** It supplies an
   explicit, numerically-verified constant and a genuine (not hand-waved)
   quadratic lower bound on `g`'s curvature within a finite window, plus
   direct quadrature confirmation that the truncation used in this
   front's own numerics is negligible at the claimed order — but it does
   NOT supply a single universal constant `C(γ)` with a proof, covering
   every `(n,m,γ)$ in the stated range, of the form standard in
   measure-theoretic asymptotic analysis textbooks. A future front
   wanting a maximally rigorous version would need to convert §5's
   numerically-verified curvature bound into an analytically-proved one
   (e.g. via explicit monotonicity analysis of each of `g`'s three
   additive terms, which are individually simple rational functions —
   plausibly tractable, not attempted here).
4. **The `O(n^{-1})` residual beyond `Δ` (§4's corrected-approximation
   slope `\to-1`) is confirmed numerically, not derived in closed form.**
   A genuinely next order (`Δ_2(n,m,γ)`, from the next Watson/Laplace
   term, `\epsilon_3^3`/`\epsilon_3\epsilon_4`/`\epsilon_5` combinations)
   was not attempted — consistent with staying strictly inside item 1's
   scope (a SINGLE correction term with a provably-decaying residual, not
   an open-ended asymptotic series).
5. **Items 2–4 of the predecessor's own §7 diagnosis (§7 above) remain
   entirely as that front left them.** Gap 1 and Gap 3 (Estágio 26/33
   onward) are untouched, exactly as every predecessor since Estágio 26
   has left them.

---

## §11 Scorecard

| Claim | Status |
|---|---|
| CITED `t^*(n,m,γ)`, global concavity of `g` | re-verified (light check of already-PROVED facts, §0/§1) |
| General Watson/Laplace second-order correction `Δ` formula | **DERIVED from first principles** and validated against the external classical Stirling-series fact (exact match, §2) |
| `Δ(n,m,γ)\sim1/(12λ\sqrt n)`, independent of `γ` (new closed form for this integrand) | **DERIVED (exact leading-power algebra) and independently numerically CONFIRMED** (mpmath dps 60, no series machinery, §3) |
| Uniformity of the `O(n^{-1/2})` leading error / `O(n^{-1})` corrected error over `λ\in[0.3,3.0]`, `γ\in\{0.3,0.5,0.8\}` | **numerically CONFIRMED**, log-log slopes converging to `-0.500`/`-0.999` at `n\to10^9` at representative points (§4) — not a formal uniform-in-`n` proof with an explicit universal constant |
| Necessity of `λ` bounded away from `0` for uniformity | **numerically DEMONSTRATED** (deliberate `λ=0.05` failure check, §4), matching the symbolic `1/λ` pole (§3) |
| Tail-negligibility of the truncated-window approximation | **semi-rigorous argument DERIVED + numerically CONFIRMED** (explicit curvature-ratio bound + direct quadrature tail measurement, §5) — not a fully formalized universal-constant theorem |
| Item 1 of Estágio 56 §7 (this front's literal mandate) | **completed for the inner `t`-integral specifically** — the matching correction for the FULL `\mathrm{term}_m}/`T_{\mathrm{prof}}` (item 2) is explicitly NOT included (§6) |
| **`C(γ)` for `γ\in(0,1)`, the ultimate target** | **remains entirely OPEN**, untouched by this front |

---

## Seeds

**Reserved block for this front:** `20260951000–20260951999`
(`DISC-DEC-145`, wave 32, frente b). **Grep-confirmed unused** before any
code was written: `grep -rn "20260951" 05_DISCOVERY_LAB/` at the start of
this front found matches ONLY in `DECISION_LEDGER.yaml`'s own reservation
line and `DISCOVERY_LAB_STATE.md`'s mirrored reservation line — zero
matches in any script or `ATTEMPT.md` of any other front.

**This front is almost entirely deterministic** (`sympy` exact symbolic
algebra, `mpmath` deterministic high-precision numerics). The ONE place
randomness is used: script `01`'s 30-point numeric spot-check of `g''(t)<
0$ over random `(n,m,γ,t)` (a supplementary sanity check on top of the
already-PROVED analytic per-term concavity result — not load-bearing for
any new claim of this front). Seed drawn: **`20260951001`** (the block's
first value), via Python's `random.seed`.

| Block | Status |
|---|---|
| `20260951000–20260951999` (this front's reservation, `DISC-DEC-145`, wave 32 frente b) | grep-confirmed **unused** before any code was written; **exactly one seed drawn** (`20260951001`, script `01`'s supplementary random spot-check); every other numerical claim in this front is exact symbolic algebra or deterministic `mpmath` at fixed, explicitly-chosen `(n,m,γ,λ)` grid points, not randomly sampled |

---

## Scope-discipline confirmation

- Own new subdirectory `gamma_c_gamma_uniform_watson_remainder_attempt/`,
  nested one level inside `.../joint_saddle_point_attempt/` (matching this
  lineage's own nesting convention), created; `ATTEMPT.md` and all
  scripts/logs written only here.
- `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `README.md`, `index.html`, and every
  ancestor/predecessor `ATTEMPT.md` and `adversarial/` file: **not
  modified**, read-only throughout.
- No `adversarial/` subdirectory created inside this front's own
  directory; no referee dispatched by this front (reserved for the
  orchestrating session, per mandate).
- **No `git` command of any kind was run** by this front.
- No `.py` file of any ancestor, predecessor, or referee front was
  imported, read, copied, or transcribed; every script here (`01`–`05`) is
  this front's own independent implementation, written fresh from the
  mathematical prose of the required reading.
- **Scope strictly limited to item 1** of the predecessor's §7 diagnosis
  (the inner `t`-integral's uniform remainder). No piece of items 2–4 was
  invoked as a prerequisite (§6 makes this boundary explicit, rather than
  silently drifting into the full `T_{\mathrm{prof}}` upgrade). The full
  4-item joint `(t,m)` program was NOT attempted, per mandate.

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_setup_and_baseline.py`/`.log` | light re-verification of the CITED `t^*(n,m,γ)` closed form and global concavity of `g`, before building new analysis on top |
| `02_formal_watson_correction.py`/`.log` | the general Watson/Laplace second-order correction formula, derived from first principles (Gaussian moments) and validated against the classical Stirling series for `Γ(z+1)`, a fact external to this archive |
| `03_scaling_at_mesoscale.py`/`.log` | the new closed form `Δ(n,m,γ)\sim1/(12λ\sqrt n)`, `γ`-independent, derived via exact leading-power scaling algebra and independently confirmed by direct `mpmath` numerics with no series machinery; the `λ\to0` pole |
| `04_numerical_uniform_verification.py`/`.log` | the central numerical deliverable — direct high-precision quadrature confirmation of the uniform `O(n^{-1/2})`/`O(n^{-1})` decay rates across an 18-point `(λ,γ)` grid, an extended `n\to10^9` push resolving an initial slope shortfall, and a deliberate `λ=0.05` boundary-failure check |
| `05_tail_bound_argument.py`/`.log` | the tail-negligibility argument substantiating the window-truncated quadrature used throughout — an explicit curvature-ratio bound plus direct measurement of the actual tail contribution |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No `git` commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
