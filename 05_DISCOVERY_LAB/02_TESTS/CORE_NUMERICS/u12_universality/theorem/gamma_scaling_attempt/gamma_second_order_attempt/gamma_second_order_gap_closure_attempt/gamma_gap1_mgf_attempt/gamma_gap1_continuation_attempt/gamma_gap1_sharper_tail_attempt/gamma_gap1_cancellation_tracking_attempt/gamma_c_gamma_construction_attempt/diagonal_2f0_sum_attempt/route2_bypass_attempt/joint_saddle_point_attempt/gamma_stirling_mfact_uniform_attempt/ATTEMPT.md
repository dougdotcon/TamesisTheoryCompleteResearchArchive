# ATTEMPT — the matching Stirling/`m!`-and-binomial-prefactor correction
# for `term_m(n,γ)`, completing item 2 of the Estágio 56/57 diagnosis

**Wave 33, front (a), `GAMMA-STIRLING-MFACT-UNIFORM-ATTEMPT`, authorized by
`DISC-DEC-148`.** Mandate: attack item 2 of the Estágio 56 §7 diagnosis
(narrowed by Estágio 57 to exactly "item 2 of 3 remaining") — the
Stirling-type asymptotic correction for the `m!`/binomial-prefactor pieces
of `term_m(n,γ)` (the factors OUTSIDE the inner `t`-integral `I(n,m,γ)`,
already corrected by the direct predecessor front,
`gamma_c_gamma_uniform_watson_remainder_attempt`, Estágio 57) — so that,
combined with the predecessor's own cited `Δ(n,m,γ)`, the FULL mesoscale
profile `T_prof(λ,γ)` is upgraded from "leading-order asymptotic" to
"leading order plus an explicit, closed-form, uniformly-verified
next-order correction with a genuinely smaller residual."

---

## VERDICT (up front)

> **A new, closed-form next-order correction `Δ_m(n,m,γ)` for the
> `m!`/binomial-prefactor piece of `term_m(n,γ)` is derived and confirmed —
> by two independent symbolic routes (`sympy.series` and `sympy.limit`)
> and by an independent, series-machinery-free `mpmath` numeric fit up to
> `n=10^{12}`.** Combined with the CITED predecessor correction
> `Δ(n,m,γ)` (Estágio 57), the FULL `term_m(n,γ)` is upgraded from an
> `O(n^{-1/2})`-accurate leading-order approximation `T_prof(λ,γ)` to an
> `O(n^{-1})`-accurate one with an explicit `Δ_total(n,m,γ) = Δ(n,m,γ) +
> Δ_m(n,m,γ)` correction — **confirmed by direct high-precision quadrature
> of the exact `term_m`, log-log slope `-0.500\to-0.500` (uncorrected/
> `Δ`-only) improving to a clean `-1.000` (this front's combined
> correction) at every one of 9 `(λ,γ)` points tested, pushed to
> `n=10^{12}`.** `C(γ)` is untouched by this front and remains entirely
> OPEN, as the mandate anticipated.
>
> **The central new result.** Write `term_m(n,γ)=F(n,m,γ)\cdot I(n,m,γ)`,
> a NEW exact algebraic identity derived here (§1) from the CITED
> `T(n,m)` closed form,
>
> `F(n,m,γ):=\Big(\dfrac{γ}{n}\Big)^m\dfrac{(n+m+1)!}{(n-m)!\,m!}`,
>
> the object item 2 targets. Building the CITED `I_{\mathrm{leading}}
> (n,m,γ):=e^{g(t^*)}\sqrt{2π/A}` (Estágio 56) and the CITED
> `T_{\mathrm{prof}}(λ,γ)` (Estágio 56) into a precisely-defined residual
> `B(n,m,γ):=\ln F(n,m,γ)+\ln I_{\mathrm{leading}}(n,m,γ)-\ln
> T_{\mathrm{prof}}(λ,γ)` — an EXACT, finite-`(n,m)` quantity, no
> approximation yet — this front expands `B` in `ε:=1/\sqrt n` at the
> mesoscale `m=λ\sqrt n` (§3) and finds, symbolically (`sympy`, two
> independent code paths), that the coefficients of `ε^{-4}` through `ε^0`
> ALL vanish exactly (a genuine, non-trivial re-confirmation, via a route
> independent of however `T_{\mathrm{prof}}`'s own original derivation was
> organized, that `T_{\mathrm{prof}}` really is the correct leading-order
> limit of `F\cdot I_{\mathrm{leading}}`), and the leading surviving term
> is
>
> **`Δ_m(n,m,γ):=K(λ,γ)/\sqrt n`,
> `\;K(λ,γ)=\dfrac{3λ}2-\dfrac{λ^3}6-\dfrac1{12λ}-\dfrac λγ`.**
>
> **A clean, checked, previously-unknown fact**: `Δ_m`'s `-1/(12λ)` pole
> as `λ\to0` cancels EXACTLY, symbolically, against the CITED
> predecessor `Δ(n,m,γ)`'s own `+1/(12λ)` pole (§4), so
>
> **`Δ_{\mathrm{total}}(λ,γ):=Δ_m+Δ=\Big(\dfrac{3λ}2-\dfrac{λ^3}6-\dfrac λγ
> \Big)\Big/\sqrt n`**
>
> is pole-free in `λ`, in contrast to either individual piece. This is
> confirmed to be a numerically real effect (§4/§6), not merely an
> algebraic curiosity: the combined correction achieves clean `O(n^{-1})`
> accuracy even at `λ` as small as `0.05`, well outside the predecessor's
> own `λ`-uniformity range for `Δ` alone. **A genuine boundary DOES
> remain**: the `-λ/γ` term is not canceled by anything, so `Δ_m` (and
> hence `Δ_{\mathrm{total}}`) requires `γ` bounded away from `0`
> (confirmed, not merely asserted, §6).
>
> **A load-bearing methodological self-catch (§8 item 1, disclosed, not
> hidden)**: an early version of the central numerical test (§5) used the
> NOMINAL target `λ` (not the ACTUAL `λ=m/\sqrt n` implied by rounding `m`
> to the nearest integer) inside `T_{\mathrm{prof}}`, `Δ`, `Δ_m` — an
> `O(1/\sqrt n)` bookkeeping artifact that masked the true `O(n^{-1})`
> convergence rate at roughly half the tested `n` values (a striking,
> diagnosable even/odd-power-of-10 pattern). Found, diagnosed, and fixed
> before finalizing this document — not silently patched over.
>
> **This upgrades `T_{\mathrm{prof}}(λ,γ)` itself — not just the inner
> `t`-integral (Estágio 57's scope) — to leading order plus an explicit,
> closed-form, numerically-verified `O(n^{-1})`-accurate correction**,
> precisely item 2 of the predecessor's own §7 diagnosis, and no further.
> `C(γ)` is not constructed, bounded, or characterized by this front; item
> 3 (Euler–Maclaurin/Poisson treatment of the outer `m`-sum) and item 4
> (joint two-variable assembly with an explicit `o(1)` remainder) remain
> entirely untouched, as scoped. No claim of progress on any Millennium
> Prize Problem; pure combinatorial/asymptotic mathematics internal to
> this archive, about a specific random-permutation-with-reroutes
> ensemble (`u12_universality`).

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or code
was written**, in the order specified by the dispatching mandate:

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entries
   `DISC-DEC-146` and `DISC-DEC-148`, read in full.
2. `THEOREM.md`, Estágio 56 (`t^*(n,m,γ)`, `T_{\mathrm{prof}}(λ,γ)`, the
   `G_n`-coefficient reproduction, §7's 4-item diagnosis) and Estágio 57
   (the direct predecessor's own `Δ(n,m,γ)` for the inner `t`-integral,
   its scoping to item 1 only, and its explicit naming of item 2 as "the
   matching Stirling/`m!` correction and the `(n+m+1)!/(n-m)!`
   correction"), both read in full.
3. The direct predecessor's full `ATTEMPT.md`
   (`.../joint_saddle_point_attempt/gamma_c_gamma_uniform_watson_remainder_attempt/ATTEMPT.md`,
   636 lines, `wc -l`) — read in full, with particular attention to its §6 (the
   explicit scope boundary: its own `Δ` covers ONLY the inner
   `t`-integral, not the `m!`/binomial-prefactor pieces) and §7 item 2
   (naming precisely the gap this front attacks). Its `Δ(n,m,γ)=
   g''''(t^*)/(8A^2)+5[g'''(t^*)]^2/(24A^3)\sim1/(12λ)/\sqrt n`, `γ`-
   independent, is CITED throughout this document, not re-derived.
4. The predecessor's own `adversarial/REFEREE_REPORT.md` (367 lines,
   `wc -l`) —
   read in full. Confirmed: `C(γ)` open, `Δ` sound with one MODERATE
   (tail Step-2 extrapolation gap, already patched by a dated nota) and
   three LOW issues, none affecting `Δ`'s closed form or its numerical
   confirmation. The referee's own fresh stress-test methodology
   (`(λ,γ,n)` points outside the front's own grid, `exp(g(t)-g(t^*))`
   relative-integrand computation to avoid catastrophic cancellation) is
   the direct model for this front's own §4–§6 numerics.
5. Traced back further, per mandate, to `THEOREM.md` Estágio 56 and the
   underlying `.../route2_bypass_attempt/joint_saddle_point_attempt/
   ATTEMPT.md` (grandparent front, 725 lines, `wc -l` — the same file the
   direct predecessor's own referee found to be 725, not 726, lines) for
   the EXACT definition of
   `\mathrm{term}_m(n,γ):=(γ^m/n^m)\,m!\,T(n,m)`, `T(n,m)=\binom{n+m+1}
   {2m+1}\cdot I(n,m,γ)/B(m+1,m+1)` (its §1, line 183/185/187), which
   this front's §1 below algebraically simplifies (a fresh, exact
   derivation, verified symbolically and by exact-Fraction arithmetic —
   not asserted) into the precise `F(n,m,γ)` object this front's
   correction targets.

**CITED, not re-derived, per the mandate's own explicit instruction:**
`t^*(n,m,γ)` and `T_{\mathrm{prof}}(λ,γ)` (Estágio 56, PROVED/derived +
confirmed), and `Δ(n,m,γ)` (Estágio 57, derived + confirmed by its own
referee). This front re-uses these EXACT closed forms as inputs, re-
plugging them into fresh numerics (§1–§6) rather than re-deriving them.

**No `.py` file of any ancestor, predecessor, or referee front was read,
imported, or consulted anywhere in this front.** Every script (`01`–`05`,
plus sub-labeled `03b`/`03c`/`03d`) is written fresh from the mathematical
prose of the required reading, per the mandate's explicit instruction.

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `README.md`,
`index.html`, and every ancestor/predecessor `ATTEMPT.md`/`adversarial/`
file (read-only). No `git` command of any kind was run. No `adversarial/`
subdirectory created inside this front's own directory; no referee
dispatched (reserved for the orchestrating session, per mandate).

---

## §1 The exact factorization `term_m = F·I`, and the precise target
## (script `01`)

**Citing** (grandparent `ATTEMPT.md` §1, itself citing the referee's
Beta-integral closed form for `T(n,m)`, PROVED):

`\mathrm{term}_m(n,γ):=\dfrac{γ^m}{n^m}\,m!\,T(n,m)`,
`\quad T(n,m)=\binom{n+m+1}{2m+1}\cdot\dfrac{I(n,m,γ)}{B(m+1,m+1)}`,
`\quad I(n,m,γ):=\int_0^1t^m(1-t)^m(1-γt)^{n-m}\,dt`.

**New, this front (pure algebra, exact identity — derived and verified,
not asserted):** expanding `B(m+1,m+1)=m!^2/(2m+1)!` and
`\binom{n+m+1}{2m+1}=(n+m+1)!/[(2m+1)!(n-m)!]`, the `(2m+1)!` factors
cancel EXACTLY, giving

> **`\mathrm{term}_m(n,γ)=F(n,m,γ)\cdot I(n,m,γ)`,
> `\;F(n,m,γ):=\Big(\dfrac γn\Big)^m\dfrac{(n+m+1)!}{(n-m)!\,m!}`.**

This is the precise object item 2 targets: `F` carries every
`m!`/binomial-prefactor piece of `\mathrm{term}_m`, entirely outside `I`.

**Verified** (script `01`): (i) symbolically, `sympy`, exact zero
difference between the two sides; (ii) numerically, 152 exact-`Fraction`
`(n,m,γ)` triples (`n\in\{3,5,8,12,20,37\}`, `m\le6`, `γ\in\{1/4,2/7,1/2,
5/6\}`), max discrepancy exactly `0`; (iii) sanity check `F(n,0,γ)=n+1`,
composed with `I(n,0,γ)=(1-(1-γ)^{n+1})/(γ(n+1))` (the trivial `m=0`
case), reproduces the CITED sanity limit `\mathrm{term}_0(n,γ)=(1-(1-γ)^
{n+1})/γ\to1/γ` exactly.

Full log: `01_term_m_prefactor_derivation.log`.

---

## §2 The classical Stirling series (external fact), and why a "naive"
## per-factor correction is NOT the right object (script `02`)

**Cited, external fact** (Abramowitz & Stegun 6.1.40; independently
verified here against `sympy`'s own asymptotic `loggamma` expansion and
numerically against `mpmath.loggamma` at `z=37` to the expected residual
order, script `02` Part A — the same discipline the direct predecessor
used to validate its own general `Δ` formula):

`\ln Γ(z+1)=z\ln z-z+\tfrac12\ln(2πz)+\dfrac1{12z}-\dfrac1{360z^3}+\cdots`.

**A natural first idea, explored and shown insufficient (script `02` Part
B):** apply this series term-by-term to each of `z_1:=n+m+1`, `z_2:=n-m`,
`z_3:=m` (the three `\ln Γ(z_i+1)` pieces of `\ln F`), giving

`\ln F=\ln F_{\mathrm{stirling0}}+δ_{\mathrm{naive}}`,
`\;δ_{\mathrm{naive}}(n,m,γ):=\dfrac1{12z_1}-\dfrac1{12z_2}-\dfrac1{12z_3}
+O(z^{-3})`,

where `F_{\mathrm{stirling0}}` uses the LEADING Stirling term only for
each factor. **Verified numerically** (dps 50, 6 `(n,m,γ)` points, `n` up
to `10^8`): `δ_{\mathrm{naive}}` correctly captures `\ln F-\ln
F_{\mathrm{stirling0}}` to the expected `O(z_3^{-3})=O(m^{-3})` residual
order (worst residual `3.3\times10^{-11}` vs. expected `\sim10^{-7}`
scale — i.e. even BETTER than the crude `1/(360m^3)` estimate, consistent
with the classical series' known accuracy). At mesoscale `m=λ\sqrt n`,
`\delta_{\mathrm{naive}}`'s dominant piece is `-1/(12m)=-1/(12λ\sqrt n)`
(since `z_1,z_2\sim n`, contributing only `O(1/n)`).

**Why this is NOT yet `Δ_m`, disclosed explicitly (this is the key
conceptual point of this front, gotten right only after an initial wrong
turn — see §8 item 2):** `δ_{\mathrm{naive}}` measures the accuracy of
approximating `F` by a crude Stirling formula AT FIXED, finite `(n,m)` —
a classical, unremarkable fact about factorials. It is NOT the same
question as "how much does `\mathrm{term}_m(n,γ)` deviate from its own
mesoscale LIMIT `T_{\mathrm{prof}}(λ,γ)` at next order in
`1/\sqrt n`" — the actual object item 2 (and this front's mandate) needs.
The latter requires expanding `F` (and its interplay with `I`'s own
leading form) directly IN THE MESOSCALE LIMIT `n\to\infty` at `m=λ\sqrt
n`, which is done properly in §3.

Full log: `02_stirling_series_and_naive_correction.log`.

---

## §3 The correct object: `B(n,m,γ):=\ln F+\ln I_{\mathrm{leading}}-\ln
## T_{\mathrm{prof}}`, and its mesoscale expansion (scripts `03`, `03b`,
## `03c`, `03d`)

**Setup.** Write, using the CITED `t^*(n,m,γ)` (Estágio 56) and CITED
`g(t):=m\ln t+m\ln(1-t)+(n-m)\ln(1-γt)` (Estágio 54/56):

`I_{\mathrm{leading}}(n,m,γ):=e^{g(t^*)}\sqrt{2π/A}`, `\;A:=-g''(t^*)`
(the CITED leading Laplace/Watson approximation to `I`, Estágio 56),

and define, EXACTLY, no approximation yet:

`B(n,m,γ):=\ln F(n,m,γ)+\ln I_{\mathrm{leading}}(n,m,γ)-\ln
T_{\mathrm{prof}}(λ,γ)`.

**Why this is the right object.** `\mathrm{term}_m=F\cdot I=F\cdot
I_{\mathrm{leading}}\cdot(1+Δ+O(Δ^2))` (CITED, predecessor), so

`\ln\mathrm{term}_m=\ln T_{\mathrm{prof}}(λ,γ)+B(n,m,γ)+Δ(n,m,γ)+O(Δ^2)`,

i.e. `B` is EXACTLY "everything left over beyond `T_{\mathrm{prof}}` and
beyond the already-cited `Δ`" — well-defined regardless of how the
original `T_{\mathrm{prof}}` derivation was internally organized, since
`F`, `I_{\mathrm{leading}}`, `T_{\mathrm{prof}}`, `Δ` are ALL fixed, cited
closed forms. **A first, incorrect hand-derivation attempt (disclosed as
self-caught, §8 item 2)** treated `\ln F`'s own mesoscale expansion in
isolation as if it alone gave the needed correction; this is wrong
because `I_{\mathrm{leading}}` (via `g(t^*)`, which is NOT independent of
`n,m` at next order) also contributes at `O(1/\sqrt n)` — the correct
computation must expand `B` as ONE combined object, done here via
`sympy`.

**Substituting `n=1/ε^2`, `m=λ/ε` (`ε:=1/\sqrt n`) and expanding `B` in
`ε`** (script `03`, direct `sympy.series`, terminates in `3.4`s — no
timeout obstacle here, unlike some of the predecessor's own more complex
combined expressions):

> **`B(n,m,γ)=K(λ,γ)\cdot ε+O(ε^2)`,
> `\;K(λ,γ)=\dfrac{3λ}2-\dfrac{λ^3}6-\dfrac1{12λ}-\dfrac λγ`.**

**Explicitly verified (script `03d`) that the coefficients of `ε^{-4},
ε^{-3},ε^{-2},ε^{-1},ε^0` are ALL exactly `0`** (symbolic coefficient
extraction, not merely "not printed" by a truncated series call) — a
genuine, non-trivial re-confirmation that `T_{\mathrm{prof}}` is the
correct leading-order limit of `F\cdot I_{\mathrm{leading}}`, obtained
via THIS front's own independent construction (not by re-deriving
`T_{\mathrm{prof}}`'s original grandparent computation).

**Independently re-derived via `sympy.limit`** (script `03d` Part B, a
genuinely different code path than `.series()`, matching this lineage's
own cross-check discipline): `K(λ,γ)=\lim_{ε\to0}B/ε`, computed
independently, gives the IDENTICAL closed form, symbolic difference `0`.

**Independently confirmed via `mpmath`, dps 60, NO series machinery at
all** (script `03b`): direct high-precision evaluation of `B(n,m,γ)` at 6
`(λ,γ)` points, `n` from `10^4` to `10^{12}`, fitting
`\sqrt n\cdot B(n,m,γ)\to K(λ,γ)` — matches the symbolic closed form to
`5.1\times10^{-5}` relative accuracy or better at `n=10^{12}` at every
point tested (worst case `λ=3.0,γ=0.3`; the tightest, `λ=0.5,γ=0.2`,
matches to `5.7\times10^{-7}`).

**Define, this front's central deliverable:**

> **`Δ_m(n,m,γ):=K(λ,γ)/\sqrt n`.**

Full logs: `03_mesoscale_correction_derivation.log`,
`03b_numeric_crosscheck_of_K.log`, `03d_confirm_no_hidden_lower_order_terms.log`.

---

## §4 A clean, checked pole cancellation: `Δ_m+Δ` has no `1/(12λ)`
## singularity (script `03c`)

The CITED predecessor `Δ(n,m,γ)\sim(1/(12λ))/\sqrt n` and this front's
`Δ_m(n,m,γ)` BOTH contain a `1/(12λ)` term, with OPPOSITE sign:

`Δ_m+Δ` coefficient `=K(λ,γ)+\dfrac1{12λ}=\dfrac{3λ}2-\dfrac{λ^3}6
-\dfrac1{12λ}-\dfrac λγ+\dfrac1{12λ}=\dfrac{3λ}2-\dfrac{λ^3}6-\dfrac λγ`.

**Confirmed exactly by `sympy` symbolic subtraction (script `03c`):**
`0` difference between `K(λ,γ)+1/(12λ)` and `3λ/2-λ^3/6-λ/γ`. This means

> **`Δ_{\mathrm{total}}(λ,γ):=Δ_m+Δ=\Big(\dfrac{3λ}2-\dfrac{λ^3}6-\dfrac
> λγ\Big)\Big/\sqrt n`**,

a POLE-FREE function of `λ`, unlike either `Δ_m` or `Δ` individually
(each blows up as `λ\to0`). This is a genuine, previously-unknown,
checkable algebraic fact about how the predecessor's inner-integral
correction and this front's prefactor correction interlock — **not
asserted as automatically "meaning" anything about uniformity down to
`λ=0` without direct numerical testing**, which §6 supplies.

Full log: `03c_combined_formula_simplify.log`.

---

## §5 The central numerical deliverable: a genuine before/after
## comparison for the FULL `term_m(n,γ)` (script `04`)

**Method.** For each `(λ,γ)` in a grid, and `n` growing over several
decades, compute: (i) `\mathrm{term}_m(n,γ)` EXACTLY — `F(n,m,γ)` via
`mpmath.loggamma` (no approximation, no quadrature) and `I(n,m,γ)` via
adaptive `mpmath` quadrature over the genuine full `[0,1]` domain, seeded
with `t^*\pm K/\sqrt A` (`K=14`–`16`) as interior breakpoints — the same
class of fix the predecessor's own front disclosed as necessary for this
narrow-peaked integrand, independently re-implemented here from scratch
(verified insensitive to `K\in[14,40]` at a spot-checked point, script
`04` docstring). The integrand is evaluated as `\exp(g(t)-g(t^*))`
relative to its own peak, avoiding catastrophic cancellation/underflow —
the predecessor's own disclosed anti-cancellation technique, independently
re-implemented. (ii)–(iv) three approximations: `T_{\mathrm{prof}}`
alone; `T_{\mathrm{prof}}(1+Δ)` (predecessor's `Δ` only); and
`T_{\mathrm{prof}}(1+Δ+Δ_m)` (this front's combined correction).

**Main grid** (6 `(λ,γ)` points spanning `λ\in\{0.3,\ldots,2.0\}`,
`γ\in\{0.3,0.5,0.8\}`, `n=4000` to `1{,}024{,}000`): local log-log slopes
converge cleanly to `-0.500` (leading), `-0.499`-to`-1.003` (Δ-only —
see the `λ=1.0,γ=0.8` exception below), and `-0.999`-to`-1.003`
(`Δ+Δ_m`, this front) — **a full extra order of accuracy, at every
point**.

**A striking, checked exception, explained not hand-waved:**
`(λ,γ)=(1.0,0.8)` shows `Δ`-only ALREADY achieving slope `-1.003`, same
as `Δ+Δ_m`. Investigated (§6, Part C): `K(1,0.8)=0` EXACTLY (symbolic,
confirmed to `<10^{-50}`) — a special point where `Δ_m` itself vanishes
at leading mesoscale order, so `Δ`-only and `Δ+Δ_m` coincide there by
construction. This is an independent CONFIRMATION of the exact
coefficients in `K(λ,γ)`, not an anomaly.

**Extended push to `n=10^{12}`** at three representative points
(`(λ,γ)=(1.0,0.5),(0.3,0.5),(2.0,0.3)`), tracking the LOCAL log-log slope
decade-by-decade: `Δ+Δ_m`'s slope converges to a clean, stable `-1.000`
by `n=10^5`–`10^7` and stays there through `n=10^{12}` at every point,
while `leading` and `Δ`-only both remain pinned at `-0.500` throughout —
**`Δ` alone genuinely does NOT improve the order of accuracy for the FULL
`\mathrm{term}_m`; only `Δ+Δ_m` together do.** This is the direct,
load-bearing numerical substantiation of this front's central claim.

Full log: `04_numeric_before_after_termm.log`.

---

## §6 Boundary behavior: `λ` bounded away from `0` is NOT required for
## `Δ_{\mathrm{total}}`, but `γ` bounded away from `0` IS (script `05`)

**Part A (symbolic):** confirms §4's pole cancellation persists as a
clean numeric limit down to `λ=0.001` (coefficient `\to-0.0005`, matching
`3λ/2\to0` linearly).

**Part B (numeric, the real test — does the algebraic cancellation
survive contact with the un-expanded exact `\mathrm{term}_m`?):**

- **`λ\in\{0.05,0.1,0.25\}`** (well below the predecessor's own tested
  `[0.3,3.0]` range, and matching its own deliberate `λ=0.05`
  boundary-failure point): `Δ+Δ_m`'s error decays CLEANLY at the full
  `O(n^{-1})` rate (ratio exactly `100` per `100\times` increase in `n`,
  at every step, `n=10^6\to10^{10}`) — **the pole cancellation of §4 IS a
  real numerical effect, not merely an algebraic curiosity**: this
  front's combined correction works well BELOW the predecessor's own
  `λ`-uniformity floor, in sharp contrast to `Δ` alone (which the
  predecessor found to degrade there).
- **`λ\in\{5.0,8.0\}`** (above the predecessor's own tested range,
  matching its referee's own stress points): `Δ+Δ_m` still shows clean
  `O(n^{-1})`-type decay, though with a much larger coefficient (`Δ_m`'s
  `-λ^3/6` term grows cubically) — the correction is a genuinely SMALL
  perturbation only once `n` is large enough (e.g. at `λ=8`, `n=10^6`,
  `Δ_m\approx-0.10`, a 10% correction — not yet "small"). No breakdown of
  the asymptotic RATE is found, but the practically useful `n`-range
  shrinks as `λ` grows, exactly as expected from the `λ^3` coefficient
  growth.
- **`γ=0.98`** (near `1`): clean, no issue (`O(n^{-1})` throughout).
- **`γ=0.02`** (near `0`, matching the referee's own stress point): the
  `-λ/γ` term in `K(λ,γ)` is NOT canceled by anything, so `Δ_m` blows up
  as `γ\to0` (`Δ_m\approx-0.049` at `n=10^6,λ=1.0,γ=0.02` — a genuinely
  large, non-small correction at this `n`). The asymptotic `O(n^{-1})`
  rate still eventually holds once `n` is pushed further, but the
  practical range requires `γ` bounded away from `0`. **This is a real,
  substantiated (not merely asserted) boundary of this front's claim,
  directly analogous to the predecessor's own `λ\to0` boundary for `Δ`
  alone — except here it is `γ\to0`, not `λ\to0`, that is the obstruction
  (since the `λ\to0` obstruction was specifically canceled, §4).**

**Part C (the `K(1,0.8)=0` spot-check, §5's exception, resolved):**
`K(1,0.8)=0` confirmed exactly (`<10^{-50}`, dps 60); `Δ`-only and
`Δ+Δ_m` errors match closely at this point (`1.14\times10^{-6}` vs.
`1.14\times10^{-6}` at `n=10^6`; small `\sim3\%` divergence at `n=10^9`
attributable to `Δ_m`'s own tiny nonzero residual at finite `n`, of the
correct sign and order of magnitude).

Full log: `05_boundary_and_pole_cancellation.log`.

---

## §7 What this front does and does NOT claim about `T_{\mathrm{prof}}`
## and `C(γ)`

`Δ_m(n,m,γ)`, combined with the CITED `Δ(n,m,γ)`, upgrades the FULL
`T_{\mathrm{prof}}(λ,γ)`-based approximation of `\mathrm{term}_m(n,γ)`
from `O(n^{-1/2})` accuracy to `O(n^{-1})` accuracy, confirmed uniformly
over `λ\in\{0.3,\ldots,3.0\}` (and, with a larger but still-decaying
coefficient, `λ\in\{0.05,\ldots,8.0\}`), `γ\in\{0.2,\ldots,0.98\}`
(excluding a neighborhood of `γ=0`, where `Δ_m`'s `-λ/γ` term is
unbounded — a genuine, disclosed boundary, not swept aside).

**This front does NOT**: construct, bound, or characterize `C(γ)` in any
way; perform an Euler–Maclaurin/Poisson treatment of the OUTER `m`-sum
(item 3 of Estágio 56/57's diagnosis — a genuinely separate object,
explicitly assigned to the sibling wave-33 front (b), `GAMMA-OUTER-SUM-
POISSON-ATTEMPT`, per `DISC-DEC-148`); or assemble a single, jointly-
controlled two-variable `(t,m)` asymptotic with an explicit `o(1)`
remainder (item 4 — the ORIGINAL Estágio 56 target, explicitly out of
scope for either wave-33 front individually). No piece of items 3–4 was
invoked as a prerequisite anywhere in this front's derivations (§1–§6).

---

## §8 Self-caught issues

1. **The λ-rounding bookkeeping bug in the central numerical test (§5,
   script `04`), found and fixed before finalizing this document.** An
   early version of script `04` computed `m:=\mathrm{round}(λ_{\mathrm
   {target}}\sqrt n)` (necessarily an integer) but then evaluated
   `T_{\mathrm{prof}}`, `Δ`, `Δ_m` at the NOMINAL `λ_{\mathrm{target}}`,
   not the ACTUAL `λ_{\mathrm{actual}}:=m/\sqrt n` implied by the rounded
   integer `m`. Since `λ_{\mathrm{target}}-λ_{\mathrm{actual}}=O(1/\sqrt
   n)` generically (exactly `0` only when `\sqrt n` happens to be an
   integer multiple structure aligning with `λ_{\mathrm{target}}`, e.g.
   at `n=10^{4k}`), this silently injected a SPURIOUS `O(1/\sqrt n)`
   error into every approximation, masking the true `O(n^{-1})`
   convergence of `Δ+Δ_m` at roughly half the tested `n` values — a
   striking, diagnostic even/odd-power-of-10 pattern in the raw output
   (visible directly: at `n=10^5,10^7,10^9,10^{11}` the combined-
   correction error was `\sim10^3`-fold LARGER than at the adjacent
   `n=10^4,10^6,10^8,10^{10}`, and decayed at the WRONG rate,
   `O(n^{-1/2})` not `O(n^{-1})`, across those specific points only).
   Diagnosed directly (not brushed aside as noise): computed
   `λ_{\mathrm{actual}}-λ_{\mathrm{target}}` explicitly at a few sample
   points, confirmed it matched the `O(1/\sqrt n)` pattern exactly,
   fixed by using `λ_{\mathrm{actual}}=m/\sqrt n` consistently everywhere
   in script `04`/`05`. This is a METHODOLOGY bug (a mismatch between the
   idealized continuous-`λ` formulas and the discrete-`m` reality any
   such numerical test must confront), not a flaw in the derived
   `Δ_m`/`K(λ,γ)` formula itself — confirmed by the clean, exact-power-
   of-100 convergence obtained immediately after the fix (§5).
2. **An initial, wrong hand-derivation of `Δ_m`'s coefficient, caught
   before being committed to any script or claim.** A first attempt (not
   run as code, caught during manual derivation planning) treated `\ln
   F`'s own mesoscale expansion IN ISOLATION as the object needed,
   ignoring that `I_{\mathrm{leading}}(n,m,γ)=e^{g(t^*)}\sqrt{2π/A}`
   itself has a NONTRIVIAL `O(1/\sqrt n)` term at mesoscale (since
   `g(t^*)`, `A` both depend on `n,m` beyond their role in
   `T_{\mathrm{prof}}`'s own leading order). This gives a DIFFERENT
   (wrong) coefficient than the correct joint computation. Caught before
   any script was written, by explicitly re-deriving the correct
   bookkeeping (§3's `B:=\ln F+\ln I_{\mathrm{leading}}-\ln
   T_{\mathrm{prof}}` construction, which correctly accounts for both
   pieces jointly) — the committed derivation (script `03`) uses the
   correct construction throughout; the wrong hand attempt is disclosed
   here for transparency, matching this lineage's own discipline of
   surfacing false starts rather than silently discarding them.
3. **No other computational bugs found.** `K(λ,γ)`'s closed form was
   checked FOUR independent ways: (a) `sympy.series` (script `03`), (b)
   explicit coefficient-by-order extraction confirming zero lower-order
   terms (script `03d` Part A), (c) `sympy.limit`, a genuinely different
   symbolic code path (script `03d` Part B), and (d) direct `mpmath` dps
   60 numeric fit with NO series machinery, up to `n=10^{12}` (script
   `03b`) — all four agree exactly (symbolic routes) or to `<5.1\times
   10^{-5}` relative accuracy (the numeric fit, at the largest `n`
   tested). The pole-cancellation of §4 was checked both symbolically
   (exact `sympy` subtraction) and by direct numerical stress test at
   `λ` down to `0.05` (§6), not merely asserted from the algebra.

---

## §9 Numerical verification summary (fresh scripts, logs on disk)

| Script | What it checks | Result |
|---|---|---|
| `01_term_m_prefactor_derivation.py`/`.log` | exact algebraic identity `term_m=F\cdot I`, `F(n,m,γ)=(γ/n)^m(n+m+1)!/((n-m)!m!)`, from the CITED `T(n,m)` closed form; `m=0` sanity composition | 0 discrepancies (symbolic + 152 exact-Fraction checks) |
| `02_stirling_series_and_naive_correction.py`/`.log` | classical Stirling series (external fact) validated against `sympy`'s own asymptotic `loggamma` and numerically; the "naive" per-factor correction `δ_{\mathrm{naive}}`, shown insufficient/distinct from `Δ_m` | Stirling series confirmed exact match; `δ_{\mathrm{naive}}` accurate to expected order, but conceptually the wrong object |
| `03_mesoscale_correction_derivation.py`/`.log` | the correct object `B:=\ln F+\ln I_{\mathrm{leading}}-\ln T_{\mathrm{prof}}`; mesoscale `sympy.series` in `ε=1/\sqrt n`, giving `K(λ,γ)` | direct series succeeded in 3.4s; `K(λ,γ)=3λ/2-λ^3/6-1/(12λ)-λ/γ` derived |
| `03b_numeric_crosscheck_of_K.py`/`.log` | independent `mpmath` dps-60 fit of `\sqrt n\cdot B(n,m,γ)\to K(λ,γ)`, NO series machinery, `n` to `10^{12}`, 6 `(λ,γ)` points | matches symbolic `K` to `<5.1\times10^{-5}` relative at every point |
| `03c_combined_formula_simplify.py`/`.log` | exact symbolic cancellation of the `1/(12λ)` pole between `Δ_m` and the CITED `Δ` | `0` symbolic difference; `Δ_{\mathrm{total}}=(3λ/2-λ^3/6-λ/γ)/\sqrt n` |
| `03d_confirm_no_hidden_lower_order_terms.py`/`.log` | explicit zero-coefficient confirmation at `ε^{-4}`..`ε^0`; independent `sympy.limit` re-derivation of `K(λ,γ)` | all lower-order coefficients exactly `0`; `sympy.limit` matches `sympy.series` exactly |
| `04_numeric_before_after_termm.py`/`.log` | THE central deliverable: direct `mpmath` quadrature of exact `term_m` vs. leading/`Δ`-only/`Δ+Δ_m`, 6-point main grid + 3-point extended push to `n=10^{12}` | leading & `Δ`-only slope `\to-0.500`; `Δ+Δ_m` (this front) slope `\to-1.000`, clean and stable, at every point |
| `05_boundary_and_pole_cancellation.py`/`.log` | symbolic + numeric boundary tests: `λ\to0` pole cancellation survives contact with exact `term_m`; `γ\to0` boundary genuinely required; `K(1,0.8)=0` spot-check | `λ` down to `0.05` works cleanly; `γ=0.02` shows the expected large-but-still-`O(n^{-1})` behavior; `K(1,0.8)=0` confirmed exactly |

All numerics are `sympy` symbolic/exact or `mpmath` at dps 50–60,
deterministic. **Zero randomness used anywhere in this front** (see
Seeds section).

---

## §10 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed, NOT bounded, and
   NOT characterized as a convergent series with a proved remainder** —
   untouched by this front, exactly matching the mandate's own risk
   disclosure.
2. **Item 3 of Estágio 56/57's diagnosis** (an Euler–Maclaurin/Poisson-
   summation treatment of the OUTER `m`-sum itself) — untouched by this
   front, explicitly assigned to the sibling wave-33 front (b) per
   `DISC-DEC-148`.
3. **Item 4** (joint two-variable `(t,m)` assembly, combining this
   front's `Δ_m`, the predecessor's `Δ`, and item 3's outer-sum treatment
   into a single, explicit `o(1)`-remainder statement) — untouched,
   explicitly out of scope for either individual wave-33 front, per the
   mandate (the same depth-comparable-to-Gap-1 assessment the
   grandparent front made, still standing).
4. **`Δ_m`'s (and `Δ_{\mathrm{total}}`'s) `O(n^{-1})` residual is
   confirmed numerically (§5), not derived in closed form.** A genuinely
   next-order term (`O(n^{-3/2})`) was not attempted — consistent with
   staying inside a single-correction-term scope, matching the
   predecessor's own analogous restraint for `Δ`.
5. **The `γ\to0` boundary of `Δ_m`'s validity (§6) is characterized
   numerically (the `-λ/γ` term's growth), not via a formal
   `ε`-`δ`-style uniform bound with an explicit constant.** A future
   front wanting maximal rigor here would need an analytic treatment
   analogous to the predecessor's own semi-rigorous tail argument (its
   §5), not attempted here.
6. **The tail-negligibility of the `I(n,m,γ)` quadrature used throughout
   this front's own numerics (§5/§6) is CITED, not re-derived** — this
   front's own `I_exact` quadrature uses the same breakpoint-seeding
   technique as the predecessor and relies on the predecessor's own
   already-established (semi-rigorous, disclosed) tail argument for why
   this is safe; no NEW tail analysis was performed or was needed, since
   this front introduces no new truncation of `I` itself.

---

## §11 Scorecard

| Claim | Status |
|---|---|
| Exact identity `term_m=F\cdot I`, `F=(γ/n)^m(n+m+1)!/((n-m)!m!)` | **DERIVED (pure algebra) and verified** exactly, symbolically + 152 exact-Fraction checks (§1) |
| Classical Stirling series (external fact) | **cited, cross-checked** against `sympy`'s own asymptotic expansion and `mpmath` numerics (§2) |
| `δ_{\mathrm{naive}}` (naive per-factor correction) is NOT the object item 2 needs | **DERIVED and explicitly distinguished** from the correct object (§2, §8 item 2) |
| `Δ_m(n,m,γ)=K(λ,γ)/\sqrt n`, `K(λ,γ)=3λ/2-λ^3/6-1/(12λ)-λ/γ` | **DERIVED (two independent symbolic routes, `sympy.series` + `sympy.limit`) and independently numerically CONFIRMED** (`mpmath` dps 60, no series machinery, `<5.1\times10^{-5}` rel. accuracy at `n=10^{12}`) (§3) |
| `Δ_m+Δ` pole-free in `λ` (exact `1/(12λ)` cancellation) | **DERIVED (exact symbolic subtraction) and numerically CONFIRMED** to be a real effect surviving contact with exact `term_m`, down to `λ=0.05` (§4, §6) |
| Combined `Δ_{\mathrm{total}}=Δ+Δ_m` upgrades `T_{\mathrm{prof}}`-based approximation of the FULL `term_m` from `O(n^{-1/2})` to `O(n^{-1})` accuracy | **numerically CONFIRMED**, clean log-log slope `-0.500\to-1.000`, at 9 `(λ,γ)` points, pushed to `n=10^{12}` at 3 representative points (§5) — not a formal proof with an explicit universal constant |
| `Δ` alone (predecessor's, without `Δ_m`) does NOT improve the order of accuracy for the FULL `term_m` | **numerically DEMONSTRATED** — slope stays at `-0.500` throughout the extended push, at every point except the special `K(1,0.8)=0` coincidence (§5, §6 Part C) |
| Necessity of `γ` bounded away from `0` | **numerically DEMONSTRATED** (deliberate `γ=0.02` stress test, §6) |
| `λ` bounded away from `0` is NOT required for `Δ_{\mathrm{total}}` (unlike for `Δ` alone) | **numerically DEMONSTRATED**, down to `λ=0.05` (§6) — a genuinely new, non-obvious finding |
| Item 2 of Estágio 56/57 §7 (this front's literal mandate) | **completed**: the FULL `T_{\mathrm{prof}}`-based approximation of `term_m` (not just the inner integral) now has an explicit, closed-form, numerically-verified `O(n^{-1})`-accurate correction |
| **`C(γ)` for `γ\in(0,1)`, the ultimate target** | **remains entirely OPEN**, untouched by this front |

---

## Seeds

**Reserved block for this front:** `20260952000–20260952999`
(`DISC-DEC-148`, wave 33, frente a). **Grep-confirmed unused** before any
code was written: `grep -rn "20260952" 05_DISCOVERY_LAB/` found matches
ONLY in `DECISION_LEDGER.yaml`'s own reservation line and
`DISCOVERY_LAB_STATE.md`'s mirrored reservation line — zero matches in
any script or `ATTEMPT.md` of any other front, confirmed at the start of
this front and again before finalizing this document.

**This front is ENTIRELY DETERMINISTIC.** Every computation is `sympy`
exact symbolic algebra (Parts §1, §2 Part A, §3, §4) or deterministic
`mpmath` high-precision numerics at fixed, explicitly-chosen `(n,m,γ,λ)`
grid points (§2 Part B, §5, §6) — **zero random draws anywhere**, so the
reserved seed block was never actually needed. This is disclosed
explicitly, matching several recent fronts in this lineage that turned
out to be fully deterministic.

| Block | Status |
|---|---|
| `20260952000–20260952999` (this front's reservation, `DISC-DEC-148`, wave 33 frente a) | grep-confirmed **unused** before any code was written; **zero seeds drawn** — every numerical claim in this front is exact symbolic algebra or deterministic `mpmath` at fixed grid points, not randomly sampled |

---

## Scope-discipline confirmation

- Own new subdirectory `gamma_stirling_mfact_uniform_attempt/`, nested
  alongside `gamma_c_gamma_uniform_watson_remainder_attempt/` inside
  `.../joint_saddle_point_attempt/` (matching this lineage's own nesting
  convention — a sibling front, not a further-nested descendant of the
  predecessor), created; `ATTEMPT.md` and all scripts/logs written only
  here.
- `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `README.md`, `index.html`, and every
  ancestor/predecessor `ATTEMPT.md` and `adversarial/` file: **not
  modified**, read-only throughout.
- No `adversarial/` subdirectory created inside this front's own
  directory; no referee dispatched by this front (reserved for the
  orchestrating session, per mandate).
- **No `git` command of any kind was run** by this front.
- No `.py` file of any ancestor, predecessor, or referee front was
  imported, read, copied, or transcribed; every script here (`01`–`05`,
  plus `03b`/`03c`/`03d`) is this front's own independent implementation,
  written fresh from the mathematical prose of the required reading.
- **Scope strictly limited to item 2** of the predecessor's §7 diagnosis
  (the `m!`/binomial-prefactor correction to `T_{\mathrm{prof}}`). Item 3
  (outer-sum Euler–Maclaurin/Poisson treatment, assigned to the sibling
  wave-33 front (b)) and item 4 (joint two-variable assembly) were NOT
  attempted, per mandate. `Δ(n,m,γ)` (item 1) is CITED throughout, never
  re-derived.

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_term_m_prefactor_derivation.py`/`.log` | exact algebraic derivation of `term_m=F\cdot I`, `F(n,m,γ)=(γ/n)^m(n+m+1)!/((n-m)!m!)`, from the CITED `T(n,m)` closed form |
| `02_stirling_series_and_naive_correction.py`/`.log` | the classical Stirling series (external fact, cross-checked), and the "naive" per-factor correction `δ_{\mathrm{naive}}`, shown to be a distinct, insufficient object for item 2's actual target |
| `03_mesoscale_correction_derivation.py`/`.log` | the correct object `B:=\ln F+\ln I_{\mathrm{leading}}-\ln T_{\mathrm{prof}}` and its mesoscale `sympy.series` expansion, giving `K(λ,γ)` and `Δ_m(n,m,γ)` |
| `03b_numeric_crosscheck_of_K.py`/`.log` | independent `mpmath` dps-60 numeric fit of `K(λ,γ)`, no series machinery, `n` up to `10^{12}` |
| `03c_combined_formula_simplify.py`/`.log` | exact symbolic cancellation of the `1/(12λ)` pole between `Δ_m` and the CITED `Δ`, giving `Δ_{\mathrm{total}}` |
| `03d_confirm_no_hidden_lower_order_terms.py`/`.log` | explicit zero-coefficient confirmation at all orders below `ε^1`, and an independent `sympy.limit` re-derivation of `K(λ,γ)` |
| `04_numeric_before_after_termm.py`/`.log` | the central numerical deliverable — direct high-precision quadrature "before vs. after" comparison of `term_m` vs. leading/`Δ`-only/`Δ+Δ_m`, main grid + extended `n\to10^{12}` push |
| `05_boundary_and_pole_cancellation.py`/`.log` | symbolic + numeric boundary tests: the `λ\to0` pole cancellation surviving contact with exact `term_m`, the genuine `γ\to0` boundary, and the `K(1,0.8)=0` spot-check |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No `git` commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
