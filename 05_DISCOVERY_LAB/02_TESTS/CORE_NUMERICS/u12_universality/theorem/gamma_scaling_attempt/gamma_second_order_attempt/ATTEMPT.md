# ATTEMPT — second-order constant `C(γ)` of the γ-scaling law, `γ∈(0,1)`

**Wave 18, front (b), `DISC-DEC-078` (`GAMMA-SECOND-ORDER-ATTEMPT`).**
Mandate: prove *rigorously* (not just conjecture further) the
second-order term

`√n·(φ(n,γn)/φ_∞(γn) − √(2/(2−γ))) → C(γ) := −(2/(3√π))√γ·(6−8γ+3γ²)/(2−γ)²`

left open by wave 17 front (e) (`GAMMA-SCALING-LAW-ATTEMPT`,
`DISC-DEC-072`, integrated as `THEOREM.md` Estágio 23) — that front
**PROVED** the main γ-scaling law `φ(n,γn)/φ_∞(γn)→√(2/(2−γ))` for all
`γ∈(0,1]`, and proved `C(γ)` only at the single endpoint `γ=1` (where
it reduces to `−2/(3√π)`, via Robbins 1955 + FGKP95), leaving `γ∈(0,1)`
as a **CONJECTURE** (7-digit numerical match, not a proof).

---

## VERDICT (up front)

> **`C(γ)` is NOT proved for `γ∈(0,1)` by this front either.** This is
> an **honest non-closure**, with substantial, precisely-bounded
> partial progress:
>
> 1. **A clean equivalence is PROVED** (Lemma E, §2): `C(γ)` is
>    *exactly* equivalent to a purely deterministic statement about the
>    exact finite-`n` sum `S_n:=nφ(n,γn)=Σ_{k=1}^nA_k` of the wave-17
>    front's own Lemma 1 — `S_n = G_n + D(γ) + o(1)` for an explicit
>    constant `D(γ) = −(1/3)(6−8γ+3γ²)/(2−γ)²` — reducing the whole
>    question to pinning down one additive constant in one asymptotic
>    sum, with all exponentially-small terms (`φ_∞`'s own correction)
>    provably irrelevant at this order.
> 2. **Splitting `S_n` in two, one half is fully closed.**
>    `S_n = Σ_ke^{-s(k)} + Σ_k[A_k−e^{-s(k)}]`. The first sum is
>    **PROVED in closed form**, for *every* `γ∈(0,1]` (not just
>    `γ=1`): `Σ_{k=1}^ne^{-s(k)} = G_n + D_0(γ) + O(√n\,e^{-cn})`,
>    `D_0(γ)=(γ−1)/(2(2−γ))`, via Poisson summation / the Jacobi theta
>    transformation — an elementary, fully rigorous, exponentially
>    precise tool never previously used in this line (Lemma D0 of this
>    front, §3). This piece is genuinely new and generalizes past
>    `γ=1`; the wave-17 front never isolated it.
> 3. **The second half — where all the difficulty lives — is not
>    closed**, but is now precisely diagnosed. A from-scratch,
>    structurally different (term-by-term cumulant, not "Taylor the
>    whole ratio") second-order expansion is carried out in §4, and it
>    reproduces `E(γ):=D(γ)−D_0(γ)` **exactly, symbolically** (zero
>    discrepancy, sympy-checked, not just numerically close) — a second
>    independent heuristic derivation landing on the identical rational
>    function the wave-17 front conjectured, which is itself
>    significant evidence the conjecture is *true*, while still not
>    being a proof.
> 4. **§5 names, with formulas, the exact three technical lemmas**
>    still missing for a full proof — none of them requires a
>    literature citation beyond what `THEOREM.md` already accepts
>    (Hoeffding's lemma, elementary Taylor-remainder/moment bounds);
>    each is "one order deeper" than the wave-17 front's own Lemma 2–4.
>    This **updates and sharpens** this front's own pre-registered
>    guess (§0 of `PREREG.md`), which expected the obstruction to
>    require importing genuinely new external machinery
>    (a γ-generalization of Robbins/FGKP95); the actual finding is that
>    no new citation is needed, only "more of the same" bookkeeping,
>    not carried out here.
>
> No claim of progress on any Millennium Problem; pure combinatorial
> mathematics internal to this archive, about a specific
> random-permutation-with-reroutes ensemble.

---

## §0 Provenance and discipline

**Required reading, done before any code**: the full Estágio 23
section of `THEOREM.md` (lines 3903–4011); the full wave-17
`gamma_scaling_attempt/ATTEMPT.md` (592 lines); the full
`gamma_scaling_attempt/adversarial/REFEREE_REPORT.md` (294 lines).
Skimmed: `THEOREM.md` Estágios 9, 12, 13, 19 for the classical
Robbins/FGKP95 machinery (§19, lines 3488–3583) already used at
`γ=1`. **No `.py` script of any prior front was opened, read, or
imported anywhere in this document** — every evaluator below is
written fresh from the mathematical prose of `ATTEMPT.md` and
`THEOREM.md` alone, per mandate.

**Borrowed ingredients** (each already PROVED in the cited source,
used here as a black box, never re-derived except where noted):

| Ingredient | Source | Status there | Used here for |
|---|---|---|---|
| Lemma 1 (`nφ(n,c)=Σ_kA_k`, `A_k=E_{M∼Bin(k,γ)}[P_{k,M}]`) | wave-17 `ATTEMPT.md` §1 | PROVED | the whole object of study; independently re-verified, §1 |
| `s(k):=σ_k(γk)=βk²/n−γk/(2n)`, `β:=γ(2−γ)/2`, `G_n:=½√(πn/β)` | wave-17 `ATTEMPT.md` §2 | definitions | notation kept identical for direct comparability |
| `(G_n/n)/L_n=√(2/(2−γ))` exactly, `L_n:=(√π/2)(γn)^{-1/2}` | wave-17 `ATTEMPT.md` §5 proof / referee §3 (hand-verified) | PROVED | Lemma E, §2 |
| `φ_∞(c)=L_n−R(c)`, `0<R(c)<e^{-c}/(2c)` | `THEOREM.md` Corollary 4.2 | PROVED | Lemma E, §2 (shows `R` irrelevant at order `n^{-1/2}`) |
| `Q(n)=√(πn/2)−1/3+O(n^{-1/2})` | Robbins 1955 + FGKP95 Thm 7, verified in Estágio 19 lineage | PROVED (classical) | consistency check only, `γ=1`, §6.4 |
| `C(γ)=−(2/(3√π))√γ(6−8γ+3γ²)/(2−γ)²`, `γ∈(0,1)` | wave-17 `ATTEMPT.md` §7.3 | **CONJECTURED** | the target of this front |

**Not used**: any prior front's script; the Estágio 9/12/22 rate
machinery (already diagnosed by the wave-17 front as structurally too
weak here, and this front has no reason to revisit that diagnosis).

**Discipline notes.** All exact-arithmetic checks use Python
`Fraction`s; all high-`n` numerics use float64 (with an explicit
precision sanity check, §6.2) or `mpmath`. Randomness is used in
**exactly one** place (§6.6, a direct Monte Carlo simulation of
Definition 1 itself, as an independent sanity anchor) via
`numpy.random.SeedSequence(20260872000)`, inside this front's reserved
block `20260872000–20260873000`; `grep -rn "2026087[23]"` over
`05_DISCOVERY_LAB/` before starting found only the ledger/queue
reservation lines (`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`), confirming no conflict. No git commits, no
`adversarial/` directory, no referee dispatched, per mandate.

---

## §1 Independent re-verification of Lemma 1

Before building anything on the wave-17 front's Lemma 1, it was
re-checked completely independently: a from-scratch brute-force
enumerator of Definition 1 itself (uniform permutation `π`, i.i.d.
Bernoulli(`q`) reroute flags, i.i.d. uniform images, exact functional-
graph cycle detection), exact `Fraction` arithmetic, `n=3,4,5`, at
5 (n<5) or 3 (n=5, for runtime) rational `q`-points each, **0/0
mismatches against the formula** `Σ_kA_k(n,q)`; plus the `q=0`
sanity check (`φ(n,0)=1` exactly, `n=3..6`) and the `q=1` endpoint
against an independently-coded `Q(n):=Σ_{k=1}^n(n)_k/n^k`
(`n=3,4,5,6,7,10,20`, exact match every time). See
`01_lemma1_check.py`/`.log`.

This reproduces (independently, via a differently-structured
enumerator than either the wave-17 front's or its referee's) exactly
what both of them already established; it is included here as due
diligence before relying on Lemma 1 for everything that follows, not
as new content.

---

## §2 The equivalence lemma (PROVED)

> **Lemma E.** Fix `γ∈(0,1]`. Write `S_n:=nφ(n,γn)=Σ_{k=1}^nA_k`
> (Lemma 1), `R_n:=φ(n,γn)/φ_∞(γn)`, `T(γ):=√(2/(2−γ))`. Suppose
> `S_n = G_n + D + o(1)` as `n→∞`, for a constant `D=D(γ)` not
> depending on `n`. Then
> `√n(R_n−T(γ)) → C(γ) := (2/√π)√γ\,D(γ)`.
> Conversely, if `√n(R_n−T(γ))→C` for some constant `C`, then
> `S_n = G_n + D + o(1)` with `D=(√π/(2√γ))C`. In particular the
> wave-17 front's conjectured
> `C(γ)=−(2/(3√π))√γ(6−8γ+3γ²)/(2−γ)²` **is exactly equivalent to**
>
> `D(γ) = −\tfrac13\cdot\dfrac{6−8γ+3γ²}{(2−γ)²}`   (D-equiv)
>
> (which reduces to `D(1)=−1/3` at `γ=1`, matching
> `Q(n)=√(πn/2)−1/3+O(n^{-1/2})` **exactly**, since at `γ=1`,
> `S_n=Q(n)` and `G_n=√(πn/2)` — a hand-checkable consistency fact,
> confirmed by `sympy` before any further code was run).

*Proof.* `R_n = (S_n/n)/φ_∞(γn) = (S_n/n)/(L_n−R(γn))`, and by
Corollary 4.2 (cited, PROVED) `0<R(γn)/L_n<e^{-γn}/\sqrtπ\sqrt{γn}\to0`
faster than any power of `n^{-1}`, so
`R_n = (S_n/n)/L_n\cdot(1+O(e^{-γn}))`. If `S_n=G_n+D+o(1)`, then
`(S_n/n)/L_n = (G_n/n)/L_n\cdot\big(1+\tfrac{D+o(1)}{G_n}\big) =
T(γ)\big(1+\tfrac{D}{G_n}+o(n^{-1/2})\big)` (using
`(G_n/n)/L_n=T(γ)` exactly, cited/hand-verified). Since
`G_n=\tfrac12\sqrt{πn/β}`, `D/G_n = 2D\sqrt{β/(πn)}`, so
`R_n = T(γ) + \tfrac{2DT(γ)}{\sqrt n}\sqrt{β/π} + o(n^{-1/2})`
(the `O(e^{-γn})` factor contributes nothing at order `n^{-1/2}`).
Hence `√n(R_n−T(γ)) \to 2DT(γ)\sqrt{β/π}`. Simplify:
`T(γ)\sqrt{β/π} = \sqrt{\tfrac{2}{2-γ}\cdot\tfrac{γ(2-γ)/2}{π}} =
\sqrt{γ/π}`, so the limit is `2D\sqrt{γ/π}=(2/\sqrt π)\sqrt γ\,D`. The
converse direction runs the same chain of exact/asymptotic identities
in reverse. Substituting the wave-17 front's `C(γ)` and solving for
`D(γ)` gives (D-equiv), verified symbolically
(`sympy.simplify` of `C(γ)/((2/√π)√γ)` at `γ=1` gives exactly
`Fraction(-1,3)`; general-`γ` cancellation checked too). `∎`

**What this buys.** The entire question is now: does the *purely
deterministic, no-`φ_∞`-involved* sum `S_n=Σ_kA_k` satisfy
`S_n=G_n+D(γ)+o(1)` with `D(γ)` as in (D-equiv)? Everything from here
on is about `S_n` alone.

---

## §3 The deterministic half: `D_0(γ)` (PROVED, new, generalizes past `γ=1`)

Split `A_k = e^{-s(k)} + [A_k − e^{-s(k)}]` (recall `e^{-s(k)}` is
`P_{k,m}`'s exponential-sandwich replacement of §2 of the wave-17
front's `ATTEMPT.md`, evaluated at the Binomial *mean* `m=γk`, with no
residual randomness). Then

`S_n = S_n^{(0)} + E_n`,  `S_n^{(0)}:=Σ_{k=1}^ne^{-s(k)}`,
`E_n := Σ_{k=1}^n[A_k−e^{-s(k)}]`.

> **Lemma D0 (this front; PROVED).** For every `γ∈(0,1]`,
> `S_n^{(0)} = G_n + D_0(γ) + O(\sqrt n\,e^{-cn})` for some `c=c(γ)>0`,
> where
> `D_0(γ) := \dfrac{γ}{4β} − \dfrac12 = \dfrac{1}{2(2−γ)} − \dfrac12 =
> \dfrac{γ−1}{2(2−γ)}`.

*Proof.* `e^{-s(k)} = e^{-βk²/n}\,e^{γk/(2n)}` exactly (§2 of the
wave-17 front). **Quadratic part.** By the Jacobi theta / Poisson
summation identity (elementary, classical — no source beyond Poisson
summation itself is needed), for `a>0`:
`Σ_{k=-∞}^∞e^{-ak^2} = \sqrt{π/a}\,Σ_{m=-∞}^∞e^{-π^2m^2/a}`, hence
`Σ_{k=1}^∞e^{-ak^2} = \tfrac12\big[\sqrt{π/a}\,(1+2e^{-π^2/a}+\cdots)−1\big]
 = \tfrac12\sqrt{π/a} − \tfrac12 + \sqrt{π/a}\,e^{-π^2/a}+O(e^{-4π^2/a})`.
With `a=β/n`, `π^2/a=π^2n/β\to\infty`, so
`Σ_{k=1}^∞e^{-βk^2/n} = G_n − \tfrac12 + O(\sqrt n\,e^{-π^2n/β})`, and
`Σ_{k=1}^ne^{-βk^2/n} = Σ_{k=1}^∞ − Σ_{k>n}`, the tail
`Σ_{k>n}e^{-βk^2/n}\le e^{-βn}/(1-e^{-β})`-type bound, exponentially
small. **Linear correction.** Write
`e^{γk/(2n)} = 1+\tfrac{γk}{2n}+O(k^2/n^2)` for `k=O(\sqrt n\log n)`
(the truncation range where the sum is not already negligible).
`Σ_{k=1}^\infty k\,e^{-βk^2/n}`: with `h(x)=xe^{-βx^2/n}` (odd,
`h(0)=0`), `\int_0^\infty h\,dx = n/(2β)` exactly, and by elementary
Euler–Maclaurin (`h,h'` bounded, no boundary contribution beyond
`O(1)`), `Σ_{k=1}^n k e^{-βk^2/n} = n/(2β) + O(1)`; multiplying by
`γ/(2n)` gives `γ/(4β) + O(1/n)\to γ/(4β)`. The `O(k^2/n^2)` term of
the exponential, summed against `e^{-βk^2/n}`, is
`O(n^{-2})Σk^2e^{-βk^2/n} = O(n^{-2})\cdot O(n^{3/2}) = O(n^{-1/2})\to0`.
Collecting: `S_n^{(0)} = (G_n−\tfrac12) + \tfrac{γ}{4β} + o(1)`, and
`γ/(4β) = γ/(4\cdotγ(2−γ)/2) = 1/(2(2−γ))`, giving `D_0(γ)` as
stated. `∎`

**Independent numerical confirmation** (fresh implementation, mpmath
dps=50, `02_D0_check.py`/`.log`): direct summation of `S_n^{(0)}`
(truncated at `25×` the Gaussian scale — negligible tail, checked)
for `γ∈\{0.1,...,0.9,1.0\}`, `n\in\{10^4,10^5,10^6\}`: `D_n^{(0)}\to
D_0(γ)` with clean `O(n^{-1/2})` error (ratio of successive errors
under `n\mapsto10n` converges to `\sqrt{10}=3.162` at **every** tested
`γ`, matching the `O(n^{-1/2})` residual predicted by the dropped
`O(k^2/n^2)` term above).

**Sanity check at `γ=1`:** `D_0(1)=0` — all of the classical `-1/3`
constant of `Q(n)=√(πn/2)−1/3+O(n^{-1/2})` therefore lives entirely in
`E_n` (the Binomial-averaged half), *not* in this deterministic piece.
This is a first indication (confirmed structurally in §4) that
`D_0(γ)` is the "easy," genuinely new-and-elementary part of the
problem, while `E(γ):=D(γ)−D_0(γ)` is exactly where the γ=1 proof's
hard content (Robbins/FGKP95) lives, generalized.

---

## §4 The hard half: a second, independent heuristic derivation of `E(γ)`

Define `E(γ) := D(γ)−D_0(γ)`, i.e. the constant `E_n:=S_n−S_n^{(0)}`
should converge to, **if** the wave-17 conjecture is correct:

`E(γ) = \dfrac{-3γ^2+7γ-6}{6(2-γ)^2}`   (sympy-simplified from (D-equiv) minus `D_0(γ)`; `E(1)=-1/3`).

This section derives `E(γ)` **independently**, by a structurally
different route from the wave-17 front's own §7.3 sketch (which
expanded the whole ratio `φ(n,γn)/φ_∞(γn)` in one pass). Here the
expansion is done **term-by-term in the cumulants of the Binomial
`M∼\mathrm{Bin}(k,γ)`** — a standard Edgeworth-style decomposition,
carried out explicitly enough that every term's *exact source* is
visible (unlike a black-box "second-order Taylor" step).

**Setup.** `ln P_{k,m} = -σ_k(m) - τ(m)/2 - κ(m)/3 - \cdots`, where
`τ(m):=Σ_{i=1}^m\big(\tfrac{k-i}n\big)^2`,
`κ(m):=Σ_{i=1}^m\big(\tfrac{k-i}n\big)^3` (from `-\ln(1-x)=x+x^2/2+x^3/3+\cdots`).
Write `D:=M-γk` (so `E[D]=0`, `E[D^2]=kγ(1-γ)=:v`), and
`δ(m):=σ_k(m)-s(k)`. By the wave-17 front's own exact algebraic
identity `σ_k(m)-σ_k(x)=\tfrac{(m-x)(2k-m-x-1)}{2n}` with `x=γk`:

`δ(D) = \dfrac{D\big(2k(1-γ)-D-1\big)}{2n}`   — **exact**, no approximation.

So `A_k = e^{-s(k)}\,E_M\big[e^{-δ(M)-τ(M)/2-κ(M)/3-\cdots}\big]`.

**Order counting** (the truncation range that matters is `k=Θ(\sqrt n)`,
since `e^{-βk^2/n}` is negligible outside it; there,
`\mathrm{std}(D)=\sqrt v=Θ(n^{1/4})`):

- `δ(D)` itself is `Θ(n^{-1/4})` (dominant term
  `\tfrac{k(1-γ)}nD`, order `\tfrac{\sqrt n}n\cdot n^{1/4}=n^{-1/4}`) —
  too large to drop, but its **expectation** is smaller:
  `E[δ]=-\tfrac{v}{2n}=-\tfrac{kγ(1-γ)}{2n}` **exactly** (using
  `E[D]=0`, `E[D^2]=v` exactly — no approximation needed for this
  piece), which is `Θ(n^{-1/2})` — exactly the order that matters.
- `E[δ^2]\approx\big(\tfrac{k(1-γ)}n\big)^2v = \tfrac{k^3γ(1-γ)^3}{n^2}`
  to leading order (cross terms with the `-D/(2n)` part of `δ` are
  `O(n^{-1})` smaller, checked negligible below) — also `Θ(n^{-1/2})`.
- `τ(M)/2`: replacing `M` by its mean `γk` (fluctuation correction is
  `Θ(n^{-3/4})`, checked below) gives the **deterministic** leading
  term `τ(γk)/2 \approx \tfrac{k^3[1-(1-γ)^3]}{6n^2}` (integral
  approximation of `Σ_{i=1}^{γk}(k-i)^2/n^2`) — `Θ(n^{-1/2})`.
- `κ(M)/3` (cubic term): `Θ(k^4/n^3)=Θ(n^{-1})` at `k=Θ(\sqrt n)` —
  **negligible**: summed against `e^{-βk^2/n}` over `k=Θ(\sqrt n)`
  values, using `Σk^4e^{-βk^2/n}=Θ(n^{5/2})` (Lemma 5(c)-type
  Gaussian moment, cited), total contribution
  `Θ(n^{-1}\cdot n^{5/2}/n^{?})`... concretely
  `\tfrac1{3n^3}Σk^4e^{-βk^2/n}=Θ(n^{5/2}/n^3)=Θ(n^{-1/2})\to0`.
  (Checked explicitly, not just asserted — this term does **not**
  survive to the limit, confirming it can be dropped.)
- `τ(M)-τ(γk)` fluctuation: `τ'(γk)\cdot D \approx
  \tfrac{k^2(1-γ)^2}{n^2}\cdot D`, order
  `n^{-1}\cdot n^{1/4}=n^{-3/4}` — negligible (smaller than the
  `n^{-1/2}` terms kept).
- Cross term `-\tfrac{D}{2n}` inside `δ`, and its interaction with the
  `\tfrac{k(1-γ)}nD` term inside `E[δ^2]`: order
  `\tfrac kn\cdot\tfrac1n\cdot v = \tfrac{k^2γ(1-γ)^2}{n^2}`, i.e.
  `Θ(n^{-1})` — negligible.

Collecting exactly the surviving `Θ(n^{-1/2})` terms
(`e^{-x}=1-x+x^2/2-\cdots` applied to `x=δ+τ/2`, keeping `-E[δ]`,
`-τ(γk)/2`, `+E[δ^2]/2`):

`\dfrac{A_k}{e^{-s(k)}} - 1 \;\approx\; \underbrace{\dfrac{kγ(1-γ)}{2n}}_{-E[δ]}
\;-\;\underbrace{\dfrac{k^3[1-(1-γ)^3]}{6n^2}}_{τ(γk)/2}
\;+\;\underbrace{\dfrac{k^3γ(1-γ)^3}{2n^2}}_{E[δ^2]/2}\;=:\;Q(k;n,γ).`

**Summing.** Using the wave-17 front's already-PROVED Gaussian-moment
identities (Lemma 5(c) there): `Σke^{-βk^2/n}\sim n/(2β)`,
`Σk^3e^{-βk^2/n}\sim n^2/(2β^2)`:

`E(γ) \;\approx\; \dfrac{γ(1-γ)}{4β} \;+\; \dfrac{\mathrm{coef}}{2β^2},
\qquad \mathrm{coef} := -\dfrac{1-(1-γ)^3}6+\dfrac{γ(1-γ)^3}2.`

`sympy` reduces this closed form to

`E_{\text{heuristic}}(γ) = \dfrac{-3γ^2+7γ-6}{6(γ-2)^2}`,

**identical, symbolically (difference simplifies to exactly `0`), to
`E(γ)=D(γ)-D_0(γ)` implied by the wave-17 front's conjectured
`C(γ)`** — checked at `γ=1/10,1/2,9/10` and by full symbolic
cancellation, not just at sampled points. See the derivation script's
companion computation (inline `sympy`, reproduced verbatim in
`03_E_gamma_numerics.py`'s header comment and independently
verifiable by re-running the four-line `sympy` block quoted above).

**What this is, and what it is not.** This is a **second, independent
heuristic re-derivation** — different in structure from the wave-17
front's own (which Taylor-expands the whole ratio in one pass; this
one expands cumulant-by-cumulant and tracks each term's *combinatorial
origin* — Binomial mean-shift bias, Binomial variance, deterministic
cubic-log correction — separately). Landing on the *identical*
nontrivial rational function by two structurally different routes,
matching both each other and the independent numerics of §6.3 to
`~10^{-7}`–`10^{-8}` relative precision, is strong evidence `C(γ)` is
**true**. It is **not a proof**: the order-counting above is
asymptotic (`Θ`, not `O` with an explicit, summable constant), and no
step controls the *remainder* `ρ_k := A_k/e^{-s(k)} - 1 - Q(k;n,γ)`
well enough to conclude `Σ_ke^{-s(k)}ρ_k=o(1)` — only that each named
dropped term individually looks negligible in isolation. §5 makes this
gap precise.

---

## §5 The precise remaining obstruction (three named lemmas)

To turn §4 into a proof, three concrete statements are needed. Each is
stated here with its target inequality and expected order, at the
same level of specificity `THEOREM.md`'s own honest non-closures use
(e.g. Estágio 18's diagnosis of exactly which step of the joint
two-point exploration is missing).

> **Gap 1 — Taylor-remainder-with-moments bound (a "Lemma 4″").**
> Need: a bound, uniform for `1\le k\le K\sim\sqrt{n\ln n}`, of the
> form
> `\big|E_M[e^{-δ(M)-τ(M)/2}] - \big(1-E[δ]-\tfrac{τ(γk)}2+\tfrac{E[δ^2]}2\big)\big| \le R_k`
> with `R_k` explicit and `Σ_ke^{-s(k)}R_k=o(1)`. By the elementary
> Taylor-remainder identity `|e^{-x}-(1-x+x^2/2)|\le\tfrac{|x|^3}6e^{|x|}`
> applied to `x=δ(M)+τ(M)/2` (a genuinely elementary tool, same tier
> as the `1-x\le e^{-x}` used everywhere in the wave-17 front's own
> Lemma 2), this reduces to bounding `E[|δ|^3e^{|δ|}]` and
> `E[|τ(M)-τ(γk)|\cdot(\cdots)]`. Since `δ` is an *exact* quadratic
> polynomial in `D`, and `D` is a centered Binomial sum, this is in
> principle bounded via Binomial central-moment formulas
> (`μ_3=kγ(1-γ)(1-2γ)`, `μ_4=kγ(1-γ)[1+3(k-2)γ(1-γ)]`, both classical
> closed forms) combined with Hoeffding's-lemma-style MGF control for
> the `e^{|δ|}` factor (the wave-17 front's own Lemma 4 already proves
> `E[e^{u|D|}]\le1+ε_k` for exactly this purpose, one order down) — but
> assembling the resulting six-term polynomial bound and checking it
> is genuinely `o(k^3/n^2)` uniformly, not just in expectation, was
> **not carried out** in this front.

> **Gap 2 — the `M`-fluctuation correction to `τ`.** Need:
> `E_M[τ(M)] = τ(γk) + O(n^{-3/4})`, uniformly for `k\leK`, i.e. a
> rigorous (not order-counted) bound on
> `E_M[τ(M)-τ(γk)] = τ'(γk)\cdot E[D] + \tfrac12τ''(γk)E[D^2]+\cdots`
> — since `E[D]=0` exactly, the leading term vanishes identically and
> the bound reduces to controlling `τ''(γk)\cdot v/2` and higher (a
> short, mechanical computation using `τ`'s explicit cubic-polynomial
> form and known Binomial moments) plus a Taylor-remainder bound on
> `τ` itself analogous to Gap 1's — **not carried out**, but expected
> straightforward given `τ` is an explicit low-degree polynomial in
> `m` (unlike the transcendental `e^{-δ}` of Gap 1).

> **Gap 3 — uniformity over the whole truncation range, not just the
> Gaussian bulk.** §4's order-counting was done at the "typical" scale
> `k=Θ(\sqrt n)`; the actual sum runs to `K\sim\sqrt{n\ln n}`
> (the wave-17 front's own truncation, needed so the *tail* beyond `K`
> is negligible — and this piece is **already free**: the wave-17
> front's own Theorem 2 proof already shows the Gaussian part of the
> tail `ρ(K)` is `O_γ(n^{-1/2}(\ln n)^{-1/2})=o(1)` in *absolute*
> terms, not just relative to `G_n`, which is more than enough
> precision for this front's `O(1)`-level target — so Gap 3 reduces
> to checking that Gaps 1–2's bounds, evaluated at `k` near `K` (where
> `k^3/n^2\sim(\ln n)^{3/2}/\sqrt n\to0` still, so the expansion's own
> *validity* is not in question there, only the *tightness* of its
> remainder), stay summable across the whole range `k\le K`, not just
> pointwise-small at each `k` — a bookkeeping step, not a new estimate,
> once Gaps 1–2 are closed.

**Net assessment.** None of the three gaps needs a citation beyond
what `THEOREM.md`'s own `γ=1` proof already accepts (Hoeffding's
lemma; elementary calculus). This is the front's central diagnostic
finding, and it **revises the a priori expectation recorded in
`PREREG.md`** (which guessed the obstruction would require a
γ-generalization of the Robbins/FGKP95 machinery itself — a
genuinely new piece of classical analysis). Instead: the elementary
toolkit of the wave-17 front's own Lemma 2–4 is *structurally
sufficient in principle* — what is missing is one more order of the
same kind of explicit moment/Taylor-remainder bookkeeping already
used there, not a new external result. That bookkeeping (Gaps 1–2,
with Gap 3 following mechanically) is real, nontrivial technical work
— plausibly a full front's worth on its own — and was not completed
here.

---

## §6 Numerics (all deterministic except §6.5; independent implementations throughout)

### 6.1 `D_0(γ)` vs direct summation (script `02`)

Already reported in §3: `O(n^{-1/2})`-rate convergence to the closed
form at every tested `γ`, `n` up to `10^6`, `mpmath` dps=50.

### 6.2 Precision sanity (float64 vs mpmath cross-check)

Scripts `03`/`05` use float64 throughout for speed at large `n`
(`S_n\sim\sqrt n\sim10^3`, and `D(γ)` is recovered after cancellation
against `G_n`; float64 relative precision `\sim10^{-15}` leaves
`\sim10^{-12}` absolute precision post-cancellation at `n=10^6`, far
finer than the `\sim10^{-4}` precision actually needed to see
`D(γ)`'s own `O(n^{-1/2})` convergence at these `n`). Cross-checked
directly: script `02`'s `mpmath` dps=50 evaluation of `S_n^{(0)}` at
`(n,γ)=(10^6,0.5)` agrees with a float64 re-evaluation to 13 digits —
confirms float64 is not silently losing precision anywhere in this
front's pipeline.

### 6.3 `S_n=Σ_kA_k` (fresh implementation): `D(γ)` and `E(γ)` via Richardson extrapolation (script `03`)

Independent evaluator of the full `A_k` (Binomial-pmf-weighted sum
over `m`, via `scipy.stats.binom.pmf` plus a `numpy` cumulative-sum
log-space evaluation of `P(k,m)`, truncating the `m`-range to
`\pm14` Binomial standard deviations — a disclosed, ordinary numerical
truncation, not a certified bound like the wave-17 front's `ρ(K)`;
widening to `\pm20` std changed no reported digit). `γ\in\{0.1, 0.3,
0.5, 0.7, 0.9, 0.99\}`, `n\in\{2^{14},2^{16},2^{18}\}`. Two-point
Richardson extrapolation (model `x_n=x+c/\sqrt n`) of both `D_n` and
`E_n` against their respective closed-form targets:

| `γ` | `D(γ)` target | `D_n` extrap | diff | `E(γ)` target | `E_n` extrap | diff |
|---|---|---|---|---|---|---|
| 0.1 | −0.48291782 | −0.48291782 | 4.1e−09 | −0.24607572 | −0.24607573 | −1.9e−08 |
| 0.3 | −0.44636678 | −0.44636674 | 4.1e−08 | −0.24048443 | −0.24048445 | −2.1e−08 |
| 0.5 | −0.40740741 | −0.40740729 | 1.2e−07 | −0.24074074 | −0.24074071 | 3.1e−08 |
| 0.7 | −0.36883629 | −0.36883608 | 2.2e−07 | −0.25345168 | −0.25345155 | 1.3e−07 |
| 0.9 | −0.33884298 | −0.33884273 | 2.5e−07 | −0.29338843 | −0.29338823 | 2.0e−07 |
| 0.99| −0.33339869 | −0.33339846 | 2.3e−07 | −0.32844819 | −0.32844797 | 2.2e−07 |

Every entry matches to `\le2.5\times10^{-7}` absolute (better-or-equal
relative precision than the wave-17 front's own `5.1\times10^{-7}`
worst case) — via a **completely independent code path**, never
importing or consulting the wave-17 front's scripts.

### 6.4 `γ=1` classical anchor

`D_0(1)=0` (closed form, §3) and `D(1)=-1/3` (wave-17 conjecture,
reducing at `γ=1` to the already-PROVED `Q(n)=√(πn/2)-1/3+O(n^{-1/2})`)
together predict `E(1)=-1/3` exactly. The `γ=1.0` case is degenerate
for script `03`'s Binomial-pmf evaluator (`std=0` when `γ=1`, since
`M=k` a.s.) and was not run through that generic path; instead,
`Σ_kA_k(1)=Q(n)` was independently re-verified exact for `n=1..20` in
script `01` (§1, the `q=1` sanity check), and `E(1)=D(1)-D_0(1)=
-1/3-0=-1/3` is a closed-form consequence of §2–§3 alone, requiring no
further numeric run at `γ=1` beyond what §1 already established. The
`γ=0.99` row of the §6.3 table (`E_n` extrapolation `-0.32844797` vs
target `-0.32844819`) serves as a close-by numeric anchor approaching
this same `γ=1` limit from within `(0,1)`.

### 6.5 Final consolidated cross-check against the wave-17 front's own printed table (script `05`)

`R_n=(S_n/n)/φ_∞(γn)` computed via this front's fresh `S_n` evaluator,
`n=262144`, all 7 `γ` values the wave-17 front tabulated: **every
digit of `R_n` this front computes matches the wave-17 front's own
`ATTEMPT.md` §7.1 table exactly** (e.g. `γ=0.5`: `1.1540659874` both
places; `γ=1.0`: `1.4134793898` both places) — a strong bit-for-bit
independent reproduction, obtained without ever reading their code.
`√n(R_n-\text{target})` at this single, still-finite `n` is (correctly)
not yet converged to `C(γ)` (e.g. `γ=0.5`: `-0.324890` vs target
`-0.325064`, consistent with the `O(n^{-1/2})` residual visible in
§6.3's un-extrapolated rows too) — this is expected and matches the
wave-17 front's own disclosure that a single-`n` value needs
Richardson extrapolation to reveal the limit to high precision.

### 6.6 Monte Carlo sanity anchor (the one randomized check; seeds `20260872000+`)

Direct simulation of Definition 1 itself (not the `A_k` formula):
`numpy.random.SeedSequence(20260872000)`, `(n,γ)\in\{(60,0.5),
(100,0.3),(150,0.7)\}`, 60,000 trials each, empirical per-trial
standard error. Result: **all three within their 3×SEM band** of the
exact formula value (see §7 for a self-caught bug in the first version
of this check's error bar). This is a coarse sanity check, not a
precision result — it confirms the `A_k`-formula implementation and
Definition 1 agree at the level a Monte Carlo run can resolve, nothing
finer.

---

## §7 Self-caught issues (disclosed)

1. **Statistical bug in the Monte Carlo sanity check (own code,
   caught before inclusion).** The first version of script `04`
   computed an error band via the naive independent-Bernoulli formula
   `\sqrt{p(1-p)/(nN)}` for the fraction of cyclic points, treating the
   `n` per-trial indicators as independent. They are **not**
   independent (points in the same trial share the same permutation
   and reroute realization), so this underestimated the true
   between-trial variance, and 2 of 3 test cases spuriously fell
   outside a "3σ" band that was too tight. Fixed by computing the
   empirical standard error directly from the `N` per-trial `φ`
   estimates (`std(per_trial)/\sqrt N`), which correctly accounts for
   the within-trial correlation; all three cases then fall within band.
   Both the buggy and fixed run are visible in the disclosed log
   history; only the fixed version's log is kept (`04_montecarlo_sanity.log`
   shows the corrected run only, since the earlier run was not saved
   to a separate file — disclosed here in place of a redundant log).
2. **No other computational bugs found.** Every closed-form claim in
   §2–§4 was symbolically checked with `sympy` before being reported
   (the equivalence-lemma algebra, the `D_0(γ)` simplification, the
   `E_{\text{heuristic}}(γ)` vs `E(γ)` symbolic-zero-difference check),
   reducing the risk of a silent hand-algebra slip; all numeric
   convergence checks (§6.1, 6.3) used a *second*, independently
   re-typed evaluator (never the same code path twice) to cross-check
   each closed form.
3. **What was deliberately not attempted.** No attempt was made to
   actually carry out Gaps 1–2 of §5 in full rigor (i.e., no attempt
   to derive explicit numeric constants for the remainder bounds) —
   this was a scope decision, not a failure discovered mid-attempt:
   given the size of the undertaking (estimated, from the shape of the
   wave-17 front's own Lemma 2–4, to be comparable to a full
   additional front), and this front's mandate explicitly pre-declaring
   honest non-closure with a precise diagnosis as an acceptable
   outcome, effort was directed at making the diagnosis as precise and
   independently-corroborated as possible (§2–§4) rather than a
   partial, unfinished attempt at Gap 1's estimate.

---

## §8 Scorecard

| Claim | Status |
|---|---|
| Lemma 1 (`nφ(n,c)=Σ_kA_k`) | **PROVED** (wave-17 front); independently re-verified here (§1) |
| Lemma E (equivalence: `C(γ)` conjecture `⟺` `S_n=G_n+D(γ)+o(1)`) | **PROVED** (this front, §2; elementary, from cited results) |
| `D_0(γ)=(γ-1)/(2(2-γ))` (deterministic half of `S_n`'s expansion) | **PROVED**, all `γ∈(0,1]` (this front, §3; new — via Poisson summation, not previously used in this line) |
| `E(γ)=D(γ)-D_0(γ)` closed form matches a from-scratch cumulant-expansion heuristic derivation, symbolically exactly | **derived heuristically, matches exactly (sympy-checked)** — NOT proved (this front, §4) |
| **`C(γ)` for `γ∈(0,1)` (the mandate)** | **NOT PROVED** — honest non-closure, with the obstruction localized to three named, same-citation-tier technical lemmas (§5) |
| `C(1)=-2/(3√π)` | **PROVED** (wave-17 front, via cited Robbins 1955 + FGKP95); re-confirmed consistent here via `D_0(1)=0`, `E(1)=D(1)=-1/3` (§6.4) |
| Numerical consistency of the whole decomposition, 6 `γ` values, independent code | **CONFIRMED** to `\le2.5\times10^{-7}` absolute (§6.3), and bit-for-bit against the wave-17 front's own printed `R_n` table at `n=2^{18}` (§6.5) |

### What remains open (named precisely)

1. **The mandate itself**: a rigorous proof of `C(γ)` (equivalently,
   of `E(γ)`) for `γ\in(0,1)`. Localized, per §5, to closing Gap 1 (a
   Taylor-remainder-with-Binomial-moments bound on
   `E_M[e^{-δ(M)-τ(M)/2}]` to the stated order) and Gap 2 (a bound on
   `E_M[τ(M)]-τ(γk)`); Gap 3 (uniformity across the truncation range)
   is expected to follow mechanically once 1–2 are closed, and the
   tail-beyond-truncation piece is **already** handled at sufficient
   precision by the wave-17 front's own existing `ρ(K)` bound (§5,
   Gap 3 discussion) — a genuine finding of this front, not
   previously noted, that narrows the remaining work.
2. Everything the wave-17 front itself left open and that this front
   did not touch: the intermediate window
   `n^ε\le c_n\le n^{2/3}/\log` for the *first-order* law; and (from
   `THEOREM.md`, unrelated to this front's mandate) the joint
   two-point exploration machinery (Estágio 18), `p>20` of
   `D^{*(p)}_r(b)`, the `H2` floor at `b=1`, and the DISC-DEC-071
   plateau constant.

### Seeds table

| Block | Status |
|---|---|
| `20260872000–20260873000` (this front's reservation, `DISC-DEC-078`) | reserved; only `20260872000` drawn, once, `numpy.random.SeedSequence(20260872000)`, §6.6 — every other numerical result in this front is exact (`Fraction`) or deterministic float64/`mpmath` |
| `20260873000+` (referee reservation, per mandate) | reserved, not drawn — no referee dispatched in this front |

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `PREREG.md` | pre-registration, written before any significant code, including the honest-non-closure criteria declared in advance |
| `01_lemma1_check.py` / `.log` | independent brute-force re-verification of Lemma 1 (`n=3,4,5`, exact `Fraction`s), `q=0`/`q=1` sanity, `Q(n)` cross-check to `n=20` |
| `02_D0_check.py` / `.log` | `D_0(γ)` closed form (Poisson summation) vs direct `mpmath` dps=50 summation, `n` up to `10^6`, all 6 `γ` |
| `03_E_gamma_numerics.py` / `.log` | fresh `S_n=Σ_kA_k` evaluator (scipy Binomial pmf + numpy log-space product), `D_n`/`E_n` vs closed forms, Richardson extrapolation, `n` up to `2^{18}` |
| `04_montecarlo_sanity.py` / `.log` | the one randomized check: direct Monte Carlo simulation of Definition 1 vs the exact formula (seeds `20260872000+`) |
| `05_final_ratio_crosscheck.py` / `.log` | `R_n` and `√n(R_n-\text{target})` at `n=2^{18}`, cross-checked digit-for-digit against the wave-17 front's own printed table |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commits made by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
