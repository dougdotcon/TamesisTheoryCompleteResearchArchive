# ATTEMPT — closing one of the three named gaps in the `C(γ)` second-order
# derivation, `γ∈(0,1)`

**Wave 19, front (b), `GAMMA-SECOND-ORDER-GAP-CLOSURE-ATTEMPT`, authorized
by `DISC-DEC-083`.**
Mandate: `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/`
`gamma_scaling_attempt/gamma_second_order_attempt/ATTEMPT.md` §5 names three
precise technical gaps standing between a heuristic cumulant-expansion match
and a rigorous proof of the second-order constant `C(γ)` (equivalently
`E(γ):=D(γ)-D_0(γ)`) for `γ∈(0,1)`. This front's mandate: pick the single
most tractable gap and attempt to close it rigorously, honest non-closure
of the *overall* `C(γ)` question being an explicitly acceptable outcome.

---

## VERDICT (up front)

> **Gap 2 ("the `M`-fluctuation correction to `τ`") is CLOSED, rigorously,
> and in a stronger form than originally requested.** The predecessor front
> asked for a bound `E_M[τ(M)] = τ(γk) + O(n^{-3/4})`, uniform for
> `1≤k≤K∼\sqrt{n\ln n}`, calling it "a short, mechanical computation...
> not carried out". This front carries it out completely: `τ(m)` turns out
> to be an *exact cubic polynomial* in `m` (elementary algebra), so
> `E_M[τ(M)]-τ(γk)` has an **exact, closed-form** value — no Taylor
> remainder, no approximation, valid for **every** `1≤k≤n` (not just
> `k≤K`):
>
> `Δτ(k) := E_M[τ(M)] - τ(γk) = \dfrac{-k^2γ(1-γ)^2 + \tfrac16kγ(1-γ)(5-4γ)}{n^2}`
>
> and the weighted sum that actually matters for `E(γ)`,
> `Σ_{k=1}^ne^{-s(k)}|Δτ(k)|`, is proved (via a fresh corollary — Lemma G2 —
> of the predecessor's own already-PROVED Poisson-summation identity) to be
> `O(n^{-1/2})→0`. This is **strictly better** than the `O(n^{-3/4})`
> pointwise bound asked for: the true pointwise order is `O(k^2/n^2)`, and
> the summed contribution vanishes at exactly the same `n^{-1/2}` rate as
> the polynomial correction term the referee already found in Lemma D0's
> error term — a clean structural echo. Gap 2, as literally stated, is
> **fully discharged**.
>
> **This does NOT close `C(γ)` for `γ∈(0,1)`.** Gap 2 was, by the
> predecessor's own assessment, the "easy" one of the three (`τ` is an
> explicit low-degree polynomial; Gap 1's `δ(M)` is transcendental,
> requiring genuine Taylor-remainder-with-MGF machinery). Gaps 1 and 3
> remain fully open, and Gap 1 in particular is now, by elimination, the
> single largest remaining obstacle to a full proof — this front's own
> assessment is that Gap 1 is genuinely harder than Gap 2 turned out to be,
> not merely "the next item on a list": it needs Hoeffding-lemma-tier MGF
> control on a *transcendental* quantity, not exact polynomial algebra.
> Honest status: **`C(γ)` for `γ∈(0,1)` remains OPEN** — this front narrows
> the remaining work from three named gaps to two (Gap 1, Gap 3), and
> shows Gap 3's uniformity concern is *already discharged for the τ-piece*
> specifically (the closed form here holds for the full range `1≤k≤n`, a
> superset of `k≤K`), a small additional dividend beyond closing Gap 2
> itself.
>
> No claim of progress on any Millennium Problem; pure combinatorial
> mathematics internal to this archive, about a specific
> random-permutation-with-reroutes ensemble.

---

## §0 Provenance and discipline

**Required reading, done before any derivation.** `THEOREM.md` Estágio 23
(lines 3903–4011: Teorema 2, the proved γ-scaling law limit for
`γ∈(0,1]`, and the second-order constant `C(γ)` — proved only at `γ=1`,
conjectured for `γ∈(0,1)`) and Estágio 26 (lines 4322–4438: Lemma E,
the proved equivalence between `C(γ)` and the sum `S_n`; Lemma D0, the
proved closed form for `S_n`'s deterministic half `D_0(γ)`, and its
post-adversarial error-term correction, `DISC-DEC-079`). The direct
predecessor, `.../gamma_second_order_attempt/ATTEMPT.md`, read in full
(all 633 lines, including its correction addendum at §3), with special
attention to its §4 (the from-scratch cumulant-expansion heuristic
derivation of `E(γ)`, reproduced and used as the exact context for the
gap this front closes) and §5 (the three named gaps, quoted verbatim in
§1 below).

**No `.py` file of any prior front, in this lineage or any other, was
opened, read, or imported anywhere in this front.** Every script below
(`01`–`04`) is written fresh from the mathematical prose of `THEOREM.md`
and the predecessor `ATTEMPT.md` alone, per mandate.

**Seeds.** Reserved block `20260882000–20260882999` (`DISC-DEC-083`,
this front); referee block `20260883000+`, untouched, per mandate.
`grep -rn "20260882" 05_DISCOVERY_LAB/` was run before any code and
found only the ledger/queue reservation lines (`DECISION_LEDGER.yaml`
line 5559, `TEST_QUEUE.yaml` line 3324) — no prior use, no conflict.
**This front draws zero random seeds.** Every claim below is either
exact algebra (`sympy.Fraction`/symbolic, no floats) or deterministic
high-precision numerics (`mpmath`, dps=50, no randomness) — the object
under study (`Δτ(k)`, `τ(m)`, Binomial moments) is itself fully
deterministic given `(k,n,γ)`, so no Monte Carlo check was needed or
attempted this front. The reserved block is disclosed as unused, not
silently abandoned.

**Not touched, per mandate:** `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, any file outside this
front's own new subdirectory. No git commands run. No `adversarial/`
subdirectory created; no referee dispatched (reserved for the
orchestrating session).

---

## §1 The three gaps, quoted, and which one this front attacks

Verbatim from the predecessor `ATTEMPT.md` §5 (condensed; full text
there):

> **Gap 1 — Taylor-remainder-with-moments bound.** Need a uniform bound
> `|E_M[e^{-δ(M)-τ(M)/2}] - (1-E[δ]-τ(γk)/2+E[δ²]/2)| ≤ R_k` with
> `Σ_ke^{-s(k)}R_k=o(1)`, via the elementary remainder identity
> `|e^{-x}-(1-x+x^2/2)|≤\tfrac{|x|^3}6e^{|x|}` applied to
> `x=δ(M)+τ(M)/2`, reducing to bounding `E[|δ|^3e^{|δ|}]` — "assembling
> the resulting six-term polynomial bound... was **not carried out**".
>
> **Gap 2 — the `M`-fluctuation correction to `τ`.** Need
> `E_M[τ(M)] = τ(γk) + O(n^{-3/4})`, uniformly for `k≤K`, i.e. a
> rigorous bound on `E_M[τ(M)-τ(γk)]` — "**not carried out**, but
> expected straightforward given `τ` is an explicit low-degree
> polynomial in `m` (unlike the transcendental `e^{-δ}` of Gap 1)".
>
> **Gap 3 — uniformity over the whole truncation range.** Extending
> Gaps 1–2's bounds from the "typical" scale `k=Θ(\sqrt n)` to the full
> range `k≤K∼\sqrt{n\ln n}` — assessed by the predecessor as "a
> bookkeeping step, not a new estimate, once Gaps 1–2 are closed", with
> the tail beyond `K` "already free" (handled by the wave-17 front's own
> existing `ρ(K)` bound).

**Choice: Gap 2.** The predecessor's own diagnosis already flags Gap 2
as structurally the easiest of the three — `τ(m)` is an *explicit
low-degree polynomial* in `m`, so no transcendental-function remainder
bound (Gap 1's core difficulty) or MGF/Hoeffding machinery is needed in
principle. This front's own independent assessment, confirmed below,
agrees and goes further: `τ(m)` is not merely "low-degree", it is
*exactly cubic*, which means `E_M[τ(M)]-τ(γk)` can be computed **exactly
in closed form** via linearity of expectation plus the three classical
Binomial raw moments `E[M],E[M^2],E[M^3]` — no approximation, no Taylor
remainder, no order-counting anywhere in the core identity. This
converts Gap 2 from "needs a bound" to "has an exact answer", which is
the most tractable available shape for a gap of this kind.

---

## §2 Gap 2 closed

### 2.1 Setup (recap, exact quotes from the predecessor's §4)

`τ(m):=Σ_{i=1}^m\big(\tfrac{k-i}n\big)^2`, from the log-expansion
`\ln P_{k,m} = -σ_k(m)-τ(m)/2-κ(m)/3-\cdots` (`-\ln(1-x)=x+x^2/2+x^3/3+\cdots`).
`M∼\mathrm{Bin}(k,γ)` is the (Binomial-mean-`γk`) random reroute count.
The predecessor's §4 approximates `E_M[τ(M)]` by the deterministic
`τ(γk)` and calls the resulting error "negligible" without proof — this
is precisely Gap 2.

### 2.2 `τ(m)` is an exact cubic polynomial in `m` (elementary)

`Σ_{i=1}^m(k-i)^2 = mk^2 - km(m+1) + \tfrac{m(m+1)(2m+1)}6`, so

> **Fact (elementary, verified symbolically, script `01` part A).**
> `τ(m) = \dfrac1{n^2}\Big[\dfrac{m^3}3 + m^2\big(\dfrac12-k\big) +
> m\big(k^2-k+\dfrac16\big)\Big]`, exactly, for all integers `0≤m≤k`.

`sympy.summation` of the defining sum and this closed form were
compared symbolically for general `m,k,n` — the difference simplifies
to exactly `0` (script `01`, part A, `PASS`).

### 2.3 `Δτ(k) := E_M[τ(M)] - τ(γk)`: exact closed form (PROVED)

Since `τ(m)` is cubic and `M∼\mathrm{Bin}(k,γ)`, linearity of
expectation reduces `E_M[τ(M)]` to the three classical Binomial raw
moments (factorial-moment form, cited, classical):

`E[M]=kγ`, `E[M^2]=k(k-1)γ^2+kγ`, `E[M^3]=k(k-1)(k-2)γ^3+3k(k-1)γ^2+kγ`.

Substituting into `τ(m)`'s cubic form and subtracting `τ(γk)` (using
`E[M]-γk=0` exactly, so the linear term of `τ` contributes nothing to
`Δτ`) gives, after simplification:

> **Lemma τ-fluct (this front; PROVED).**
> `\displaystyle Δτ(k) = \dfrac{-k^2γ(1-γ)^2 + \tfrac16kγ(1-γ)(5-4γ)}{n^2}`,
> **exactly**, for every `1≤k≤n`, `γ∈(0,1)` — no approximation, no
> truncation range restriction.

*Two independent derivations, both symbolic (script `01`):*
1. **Moment substitution** (part C, route 1): substitute the raw
   moments above into `τ(m)`'s cubic form, `sympy.simplify` — matches
   the stated closed form exactly (`difference = 0`).
2. **Direct pmf summation** (part C, route 2): for concrete
   `k=1,\ldots,6`, `sympy.summation` of `\binom km γ^m(1-γ)^{k-m}τ(m)`
   over `m=0,\ldots,k`, symbolic in `γ`, minus `τ(γk)` — matches the
   closed form exactly at every `k` tested, a route that never invokes
   the general raw-moment formulas of route 1 at all (fully independent
   check of the same claim).

*A third, structural consistency check* (part D): since `τ` is an exact
cubic polynomial, its own 3rd-order Taylor expansion about `m=γk` is
*itself*, with **zero remainder** — so
`Δτ(k) = τ''(γk)\cdot\mathrm{Var}(M)/2 + τ'''(γk)\cdot μ_3(M)/6` should
hold exactly, using the classical Binomial central moments
`\mathrm{Var}(M)=kγ(1-γ)`, `μ_3(M)=kγ(1-γ)(1-2γ)`. This reconstruction
(script `01` part D) matches the closed form exactly — and identifies
the predecessor's own informal remark ("reduces to controlling
`τ''(γk)·v/2` and higher") as the leading term of exactly this exact
expansion, missing only the `μ_3` correction, which this front supplies.

*Independent numeric cross-check* (script `04`, a second, structurally
different implementation — `mpmath` dps=50 direct weighted summation
over the full Binomial support, never using the closed form to
compute, only to compare): 24 `(γ,n,k)` triples, `k` up to 700 (well
beyond `sympy`'s symbolic range of `k≤6`), `n` up to `2×10^5` — every
case matches the closed form to the `mpmath` dps=50 rounding floor
(`max|direct−closed| = 1.587×10^{-48}` across all 24 cases; see script
`04`'s log, table reproduced in §4 below).

### 2.4 Lemma G2: the Gaussian second-moment sum (PROVED, new corollary of the predecessor's own Lemma D0 tool)

To show the *weighted* sum `Σ_ke^{-s(k)}Δτ(k)` vanishes (not just each
`Δτ(k)` individually), the `k^2`-weighted Gaussian sum
`Σ_{k=1}^nk^2e^{-βk^2/n}` is needed. This front derives it as a direct
corollary of the predecessor's own already-PROVED Poisson-summation
identity (Lemma D0, §3: `Σ_{k=-\infty}^\infty e^{-ak^2} = \sqrt{π/a}\,θ(a)`,
`θ(a):=Σ_me^{-π^2m^2/a}\to1` exponentially as `a\to0^+`), **by
differentiating both sides with respect to `a`** — an elementary
operation, justified by uniform convergence of both series on compact
`a`-subintervals of `(0,\infty)` (both sides are manifestly smooth,
term-by-term differentiable there):

> **Lemma G2 (this front; PROVED, elementary corollary of Lemma D0's
> Poisson-summation identity).**
> `Σ_{k=1}^\infty k^2e^{-ak^2} = \dfrac{\sqrt π}4a^{-3/2} + O(a^{-5/2}e^{-π^2/a})`
> as `a\to0^+`; with `a=β/n`, `Σ_{k=1}^nk^2e^{-βk^2/n} =
> \big(\tfrac{\sqrt π}4\big)\big(\tfrac nβ\big)^{3/2} + O(n^{5/2}e^{-cn})`
> for some `c=c(β)>0` (tail `k>n` bound: exponentially small since
> `βn\to\infty`, same style bound as Lemma D0's own tail estimate).

*Proof sketch.* `-\dfrac{d}{da}\sum_{k=-\infty}^\infty e^{-ak^2} =
\sum_kk^2e^{-ak^2}`. Differentiating the RHS
`\sqrt{π/a}\,θ(a)`: the `\sqrt{π/a}` factor differentiates to
`-\tfrac12\sqrt π\,a^{-3/2}`, times `θ(a)\to1`; and
`\sqrt{π/a}\,θ'(a)` is itself `O(a^{-5/2}e^{-π^2/a})` since
`θ'(a)=\sum_{m\ne0}e^{-π^2m^2/a}(π^2m^2/a^2)` is a sum of terms each
exponentially small as `a\to0^+`. Summing over `k\ge1` (halving by
symmetry, `k=0` contributes `0`) gives the stated form. `∎`

*Numeric verification* (script `02`, `mpmath` dps=50): the infinite-sum
version matches the closed form to `\sim10^{-40}`–`10^{-50}` absolute
already at `a=0.1`, with the residual shrinking far faster than any
fixed power of `a` (consistent with the claimed exponential
suppression, though the log-ratio comparison in the script's own output
becomes noise-dominated once the residual itself nears the `dps=50`
floor — disclosed in §5 below). The **finite-`n` truncated** version
actually used (`Σ_{k=1}^nk^2e^{-βk^2/n}` vs.
`(\sqrt π/4)(n/β)^{3/2}`), which is what matters for this front, matches
to `\sim10^{-50}` relative at every tested `(γ,n)` pair, `γ\in\{0.1,
\ldots,1.0\}`, `n\in\{2000,20000,200000\}` — i.e. numerically
indistinguishable from exact at `dps=50` (script `02`'s log, second
table).

### 2.5 The weighted sum vanishes: `Σ_ke^{-s(k)}Δτ(k) = O(n^{-1/2})\to0` (PROVED)

Combining §2.3 (exact `Δτ(k)`) with §2.4 (Lemma G2) and the
predecessor's own already-cited `Σke^{-βk^2/n}\sim n/(2β)`:

`\Big|Σ_{k=1}^ne^{-s(k)}Δτ(k)\Big| ≤ e^{γ/2}\Big[\dfrac{γ(1-γ)^2}{n^2}
Σk^2e^{-βk^2/n} + \dfrac{γ(1-γ)(5-4γ)}{6n^2}Σke^{-βk^2/n}\Big]
= O(n^{-1/2})`

(the `e^{γ/2}` factor bounds the exact `e^{γk/(2n)}\le e^{γ/2}` piece of
`e^{-s(k)}=e^{-βk^2/n}e^{γk/(2n)}` for `k\le n`, crude but sufficient
for an `O(\cdot)` statement — no uniformity subtlety, since the bound is
on the **finite-`n` sum directly**, with no order-of-limits issue at
all). This is *stronger* than Gap 2's requested `O(n^{-3/4})` pointwise
bound: the pointwise order is `O(k^2/n^2)` (so `O((\ln n)/n)` at
`k=K\sim\sqrt{n\ln n}`, far smaller than `n^{-3/4}`), and the *summed*
contribution — the quantity that actually matters for `E(γ)` — is
`O(n^{-1/2})`.

**Direct numeric confirmation, no closed-form shortcut** (script `03`,
`mpmath` dps=50, direct summation of `W_n(γ):=Σ_ke^{-s(k)}|Δτ(k)|` for
each `n` from scratch — this is an independent check of the *whole*
chain §2.3+§2.4 combined, not a re-use of either): for
`γ\in\{0.1,0.3,0.5,0.7,0.9,0.99\}`, `n\in\{10^3,10^4,10^5\}`, the ratio
`W_n/W_{10n}` converges to `\sqrt{10}=3.162278` (the `O(n^{-1/2})`
signature — exactly the diagnostic this lineage already uses for
Lemma D0's own error term):

| `γ` | `W_n/W_{10n}` (`n=10^3\to10^4`) | `W_{10n}/W_{100n}` (`n=10^4\to10^5`) |
|---|---|---|
| 0.1 | 3.154462 | 3.159822 |
| 0.3 | 3.149726 | 3.158356 |
| 0.5 | 3.146136 | 3.157258 |
| 0.7 | 3.138005 | 3.154751 |
| 0.9 | 3.082230 | 3.137538 |
| 0.99| 2.258223 | 2.870148 |

(`γ=0.99` converges more slowly — expected: the leading coefficient
`γ(1-γ)^2` in Lemma G2's application vanishes as `γ\to1`, so
subleading-order finite-`n` effects are relatively larger there at these
`n`; the ratio is still visibly moving toward `\sqrt{10}` as `n` grows,
`2.258\to2.870`, consistent with the same asymptotic rate holding, just
reached more slowly at fixed `n`.)

The **signed** correction `\mathrm{Corr}_n(γ):=Σ_ke^{-s(k)}(-Δτ(k)/2)` —
exactly the quantity that must vanish for the predecessor's §4
substitution `τ(M)\to τ(γk)` to be justified — was also tracked to
`n=10^6`; e.g. at `γ=0.5`: `3.79\times10^{-3}` (`n=10^3`) `\to
1.21\times10^{-4}` (`n=10^6`), monotonically shrinking at every tested
`γ` (script `03`'s log, third table).

### 2.6 What this establishes, precisely

> **Gap 2 (M-fluctuation correction to `τ`): CLOSED.** The substitution
> `E_M[τ(M)]\to τ(γk)` used in the predecessor's §4 derivation of
> `E_{\text{heuristic}}(γ)` contributes **exactly `0`** to the
> `n\to\infty` limit defining `E(γ)`, rigorously — not "expected
> negligible" but proved negligible, via an exact closed form for the
> per-`k` error (§2.3) and a proved `O(n^{-1/2})` bound on the resulting
> weighted sum (§2.4–2.5), the latter itself a clean corollary of a tool
> (Poisson summation) already established and trusted in this lineage.
> This closure holds **uniformly for the entire range `1\le k\le n`**,
> a strictly larger range than the `k\le K\sim\sqrt{n\ln n}` the gap
> asked for — so, restricted to this specific piece of the derivation,
> it also **discharges the corresponding slice of Gap 3** (no separate
> "extend to the tail" step is needed for the `τ`-fluctuation term
> specifically; Gap 3 remains open for Gap 1's pieces).

---

## §3 What remains open (honest scope)

**Gap 1 is untouched and is now the dominant remaining obstacle.**
Nothing in this front bears on `δ(M)=σ_k(M)-s(k)`, the transcendental
piece of the log-expansion. Gap 1 needs genuine Taylor-remainder
control (`|e^{-x}-(1-x+x^2/2)|\le\tfrac{|x|^3}6e^{|x|}`) combined with
Binomial central-moment bounds *and* Hoeffding-lemma-style MGF control
on `E[e^{|δ|}]` — qualitatively harder than Gap 2 turned out to be,
because `δ` enters the expectation *inside an exponential*, not as a
bare low-degree polynomial. This front's assessment, now that Gap 2 has
been fully worked out and found to require nothing beyond elementary
polynomial algebra + classical moments, **sharpens** (does not merely
repeat) the predecessor's own diagnosis: the "no new citation needed"
verdict for Gap 2 is now a *proved fact*, not a guess, while Gap 1's
transcendental structure means it genuinely needs the MGF machinery the
predecessor flagged (the wave-17 front's own Lemma 4,
`E[e^{u|D|}]\le1+ε_k`, cited as reusable) — assembling that into a
six-term polynomial bound, uniform in `k`, was **not attempted here**
(out of scope for a single-gap front; a plausible next front's mandate).

**Gap 3, beyond the `τ`-piece closed here, is untouched.** The
predecessor's own assessment that it "follows mechanically once Gaps
1–2 are closed" is neither confirmed nor refuted by this front for
Gap 1's contribution (only Gap 2's).

**Net effect on the mandate.** `C(γ)` for `γ\in(0,1)` is **still open**.
What changes: the count of named technical gaps standing between the
`§4` heuristic and a full proof drops from three to two (Gap 1, Gap 3),
with Gap 3 now partially pre-discharged for the piece this front closed,
and Gap 1 identified — with a concrete reason, not just by elimination —
as the harder of the two remaining.

---

## §4 Verification summary (symbolic + numeric, cross-validated)

All claims above were checked twice, by structurally different methods,
per this lineage's convention.

| Claim | Symbolic check | Numeric check | Result |
|---|---|---|---|
| `τ(m)` exact cubic closed form | `sympy.summation` vs. claimed polynomial, general `m,k,n` | — (exact identity, no numerics needed) | `PASS`, difference `=0` (script `01`, part A) |
| Binomial raw moments `E[M],E[M^2],E[M^3]` | `sympy.summation` over pmf vs. classical formula, `k=1..5`, symbolic `p` | — | `PASS`, all differences `=0` (script `01`, part B) |
| `Δτ(k)` closed form | route 1 (moment substitution) + route 2 (direct pmf sum, `k=1..6`, independent of route 1) + route 3 (exact 3rd-order Taylor reconstruction) | `mpmath` dps=50 direct weighted pmf summation, `k` up to 700, `n` up to `2\times10^5`, 24 cases | All symbolic differences `=0`; max numeric discrepancy `1.587\times10^{-48}` (rounding floor) (scripts `01` parts C–D, `04`) |
| Lemma G2 (`Σk^2e^{-ak^2}` closed form) | derived by differentiating Lemma D0's cited Poisson-summation identity | `mpmath` dps=50, infinite sum and finite-`n` truncated sum, `a` down to `10^{-4}`, `γ\in\{0.1,\ldots,1.0\}`, `n` up to `2\times10^5` | Finite-`n` relative error `\sim10^{-50}` (rounding floor) at every tested point (script `02`) |
| `Σ_ke^{-s(k)}|Δτ(k)| = O(n^{-1/2})` | algebraic combination of the two closed forms above | direct `mpmath` summation (no shortcut), ratio under `n\to10n\to100n`, `γ\in\{0.1,\ldots,0.99\}` | ratios `\to\sqrt{10}=3.162278` at every `γ` (slower at `γ=0.99`, explained, still trending correctly) (script `03`) |
| Signed correction `\mathrm{Corr}_n(γ)\to0` | — | direct summation, `n` up to `10^6`, 6 `γ` values | monotone decrease to `0` at every `γ` (script `03`) |

No `.py` file of any prior front was read, opened, or imported at any
point.

---

## §5 Self-caught issues (disclosed)

1. **The log-ratio diagnostic in script `02`'s first table is
   noise-dominated at small `a` and was not over-interpreted.** The
   script attempted to fit `\ln|r_1/r_2|` against a naive
   `π^2(1/a_2-1/a_1)+\text{power term}` prediction to demonstrate
   super-polynomial decay of the residual; once the residual itself
   approaches the `mpmath` dps=50 rounding floor (`a\lesssim0.01`, where
   the true residual is already `\sim10^{-48}`–`10^{-45}` — far smaller
   than what any realistic power-law competitor would give), the
   comparison is dominated by rounding noise, not signal, and the raw
   numbers in that block should not be read as a quantitative fit. The
   qualitative conclusion (residual is spectacularly smaller than any
   fixed power of `a`, consistent with exponential suppression) is not
   affected — it is already visible unambiguously at `a=0.1`, where the
   residual is `\sim10^{-40}`, and the **second table** (the
   finite-`n`, `\sqrt π/4\cdot(n/β)^{3/2}` comparison actually used
   downstream) is clean throughout, matching to the rounding floor at
   every tested `(γ,n)`. Disclosed here rather than silently dropped
   from the script.
2. **No computational bugs found** in the core chain (§2.2–2.5); every
   closed-form claim was checked by at least two independent routes
   (symbolic-vs-symbolic in script `01`, or symbolic-vs-high-precision-
   numeric across scripts `01`/`04`, or closed-form-vs-direct-summation
   in scripts `02`/`03`) before being reported.
3. **What was deliberately not attempted.** No attempt was made on
   Gap 1 or the remainder of Gap 3 — a scope decision per the mandate
   (pick one gap, attempt it rigorously), not a failure discovered
   mid-attempt. Gap 1's six-term polynomial bound (`E[|δ|^3e^{|δ|}]`
   plus cross-terms) was not started; based on this front's now-complete
   view of Gap 2's difficulty level, Gap 1 is assessed as substantially
   more work, plausibly still a full front's worth on its own, as the
   predecessor already estimated for "Gaps 1–2 together".

---

## §6 Scorecard

| Claim | Status |
|---|---|
| `τ(m)` exact cubic closed form | **PROVED** (this front, §2.2; elementary algebra, sympy-verified) |
| `Δτ(k)=E_M[τ(M)]-τ(γk)` exact closed form, all `1≤k≤n` | **PROVED** (this front, §2.3; three independent symbolic routes + independent high-precision numeric cross-check) |
| Lemma G2 (`Σ_{k=1}^nk^2e^{-βk^2/n}` closed form) | **PROVED** (this front, §2.4; elementary corollary of the predecessor's own proved Poisson-summation tool, Lemma D0) |
| `Σ_ke^{-s(k)}Δτ(k)=O(n^{-1/2})\to0` | **PROVED** (this front, §2.5; combines the two items above, verified numerically at 6 `γ` values, rate confirmed via `n\to10n` ratio test) |
| **Gap 2 (`M`-fluctuation correction to `τ`), as stated in the predecessor's §5** | **CLOSED** — fully and rigorously, in a strictly stronger form (`O(k^2/n^2)` pointwise, `O(n^{-1/2})` summed, whole range `1≤k≤n`) than the `O(n^{-3/4})`, `k≤K` originally requested |
| Gap 1 (Taylor-remainder-with-moments bound on `E_M[e^{-δ(M)-τ(M)/2}]`) | **UNTOUCHED, OPEN** — assessed by this front (having now fully worked Gap 2) as genuinely harder, needing transcendental-function remainder control + Hoeffding-tier MGF bounds, not just polynomial algebra |
| Gap 3 (uniformity over the full truncation range) | **PARTIALLY discharged** — the `τ`-fluctuation piece closed here already holds on the full range `1≤k≤n`; Gap 1's contribution to Gap 3 is untouched |
| **`C(γ)` for `γ∈(0,1)` (the ultimate target, per Estágio 26)** | **NOT PROVED** — still open; this front narrows the remaining obstruction from three named gaps to two, with Gap 1 now identified as the harder of the two |
| `C(1)=-2/(3\sqrt π)` | unaffected — remains **PROVED** (wave-17 front, cited); this front makes no claim at `γ=1` (the Binomial-fluctuation-in-`τ` object is degenerate there, `\mathrm{Var}=0`, and the closed-form `Δτ(k)` in §2.3 correctly evaluates to `0` at `γ=1`, a trivial but easy consistency check, confirmed in script `01`'s general-`γ` formula by direct substitution) |

### What remains open (named precisely)

1. **Gap 1** — a Taylor-remainder-with-Binomial-moments bound on
   `E_M[e^{-δ(M)-τ(M)/2}]`, requiring: (a) the classical Binomial
   central-moment formulas for `μ_3,μ_4` (cited, not re-derived here);
   (b) Hoeffding's-lemma-style MGF control on `E[e^{u|δ|}]`, reusing
   the wave-17 front's own cited Lemma 4 in principle; (c) assembling
   the resulting bound into a single uniform, summable estimate. None
   of this was attempted by this front.
2. **Gap 3, restricted to Gap 1's pieces** — extending whatever bound
   closes Gap 1 from the "typical" scale to the full truncation range
   `k\le K\sim\sqrt{n\ln n}`. Untouched here (the `τ`-fluctuation
   piece's own uniformity is already resolved, §2.6).
3. Everything the predecessor and the wave-17 front already left open
   and unrelated to this front's mandate: the intermediate window
   `n^ε\le c_n\le n^{2/3}/\log` for the first-order law; the joint
   two-point exploration machinery (Estágio 18); `p>20` of
   `D^{*(p)}_r(b)`; the `H2` floor at `b=1`; the DISC-DEC-071 plateau
   constant.

**`C(γ)` for `γ∈(0,1)` remains fully OPEN.** This front's contribution
is a genuine, complete closure of one of three named technical gaps
(Gap 2), plus a small bonus dividend toward a second (part of Gap 3),
narrowing — not completing — the path to a full proof.

### Seeds table

| Block | Status |
|---|---|
| `20260882000–20260882999` (this front's reservation, `DISC-DEC-083`) | reserved; **zero seeds drawn** — every result in this front is exact symbolic algebra (`sympy`) or deterministic high-precision numerics (`mpmath` dps=50), disclosed as unused rather than silently abandoned |
| `20260883000+` (referee reservation, per mandate) | reserved, not drawn — no referee dispatched by this front |

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_symbolic_delta_tau.py` / `.log` | symbolic (sympy) verification: `τ(m)` cubic closed form; classical Binomial raw moments; `Δτ(k)` exact closed form via two independent routes; exact 3rd-order-Taylor consistency check |
| `02_gaussian_second_moment_lemma.py` / `.log` | numeric (mpmath dps=50) verification of Lemma G2, both the infinite-sum form and the finite-`n` truncated form actually used |
| `03_weighted_sum_convergence.py` / `.log` | numeric (mpmath dps=50) direct summation of the weighted sum `W_n(γ)` and the signed correction `\mathrm{Corr}_n(γ)`, `n\to10n` rate confirmation, leading-order closed-form cross-check |
| `04_direct_pmf_numeric_crosscheck.py` / `.log` | independent numeric (mpmath dps=50) cross-check of `Δτ(k)` via direct weighted Binomial-pmf summation, `k` up to 700 — never uses the closed form to compute, only to compare |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
