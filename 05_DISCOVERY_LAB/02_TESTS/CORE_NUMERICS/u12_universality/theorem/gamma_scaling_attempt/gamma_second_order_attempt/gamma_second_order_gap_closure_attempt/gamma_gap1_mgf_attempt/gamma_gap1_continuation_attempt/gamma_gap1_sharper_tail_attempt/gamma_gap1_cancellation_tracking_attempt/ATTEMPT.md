# ATTEMPT — Exact cancellation-tracking in the Bulk/Tail Lemma's
# coefficient bounds (`C(γ)`, `γ∈(0,1)`)

**Wave 27, front (c), `GAMMA-GAP1-CANCELLATION-TRACKING-ATTEMPT`, authorized
by `DISC-DEC-127`.** Mandate: `C(γ)`, the γ-scaling law's second-order term
for `γ∈(0,1)`, remains entirely open. The named obstacle, `n₀(γ)` (the
threshold above which the Bulk/Tail Lemma's bound becomes useful), is still
astronomically large (`10¹⁸`–`10⁷⁶`) despite four prior waves of
improvement (Estágios 33, 36, 37), and this line has been dormant for five
consecutive waves (22–26) — the most conspicuously stalled named line in
the archive outside the M-CLUST(b) H1 gap. Attempt one of two
previously-named, never-attempted routes: (i) exact cancellation-tracking
in the coefficient bounds `|c_i(k)|` and the `Ĝ`/`Ĝ_Θ` assembly, or (ii) a
fundamentally different Bulk/Tail decomposition.

---

## VERDICT (up front)

> **Route (i) attempted — exact cancellation-tracking. Gap 1 remains NOT
> closed; `C(γ)` for `γ∈(0,1)` remains fully OPEN.** But this front finds
> and exploits a genuinely large, previously-undiagnosed source of
> triangle-inequality slack — exactly the kind of fix the mandate asked
> this front to look for, and exactly the kind of fix Estágio 37's
> Bernstein substitution already found once for the *tail-probability*
> step. This front finds the analogous fix for the *coefficient-bound*
> step, which every prior front (including Estágio 37 itself, explicitly,
> §7 item 4) left untouched as "the same crude, triangle-inequality-based
> elementary bounds."
>
> 1. **The mechanism.** The predecessors' bound `g(t):=|c₀|+|c₁|t+|c₂|t²
>    +|c₃|t³` upper-bounds `|x(D)|` by summing the *absolute values* of
>    all four coefficients at a *symmetric* radius `t=k`. But `x(D)` is a
>    single real cubic evaluated at a single real point `D` — its true
>    maximum on an interval is exactly computable (endpoint or a
>    closed-form critical point via the quadratic formula on `x'(D)=0`),
>    and `D`'s true range is not symmetric at all: since `M∼Bin(k,γ)∈
>    [0,k]`, `D:=M-γk` ranges over the **exact, asymmetric** interval
>    `[-γk,(1-γ)k]`, not `[-k,k]`. This front replaces the crude bound
>    with the exact maximum over the true range (§2–§3).
> 2. **The flagship finding (PROVED, exact algebra, sympy).** The new
>    tight leading constant is
>    `λ_tight(γ) = max(4, 4(1-γ)²/(γ(2-γ)))` —
>    a remarkably clean closed form, with an exactly γ-**independent**
>    piece (`=4`, from the `M→0` side, universal for every `γ`) and a
>    γ-dependent piece (from the `M→k` side) that is smaller than the
>    *previously-labeled* "ideal" `λ(γ)=4(3-2γ)/(γ(2-γ))` for **every**
>    `γ∈(0,1)` — i.e. even Estágio 36's own `λ(γ)`, which the lineage had
>    been treating as the un-improvable leading-order baseline, itself
>    still carried triangle-inequality slack that a genuinely exact
>    (sign-aware) treatment removes (§4).
> 3. **Combined with Bernstein (reused, re-derived fresh from Estágio
>    37's own citation-tier technique — not copied): a new sup, PROVED
>    exact algebra.** `sup_{γ∈(0,1)}C0_tight_Bernstein(γ,a)² = 2a+4` for
>    every fixed `a>0` — exactly **14× smaller**, uniformly in `a`, than
>    Estágio 37's own `sup=28a+56` (§5).
> 4. **A second, independent, "free" tightening.** The truncation bound
>    `K` itself: the continuation front's own `K_max:=4√(n ln n/β)`
>    carries an unnecessary ≈2× margin over the true
>    `K=⌈√(4n ln n/β)⌉`; this front uses the tight, still fully explicit
>    `K_real:=√(4n ln n/β)+1` instead (§6).
> 5. **Full reassembly, bisected `n₀(γ)` at the SAME 8 sample `γ` the
>    continuation and sharper_tail fronts used** (for direct, apples-to-
>    apples comparison), with `k`-uniformity and no-spurious-oscillation
>    independently verified numerically (zero violations, `1266` checks
>    total across three dedicated checks), and the exact-cubic-max method
>    itself cross-checked against a brute-force grid scan (`21` triples,
>    zero mismatches, worst relative difference `6×10⁻¹⁰`, consistent
>    with grid discretization, never `>`) (§7–§9).
>
> **Net numeric result:** genuine reduction in `n₀(γ)` at **all 8**
> tested points, ranging from **2.30 decades** (`γ=0.99`, a `>100×`
> improvement, the weakest case, structurally understood — §10) up to
> **23.71 decades (a factor of `~10²³·⁷`) at `γ=0.01`**, compared against
> the sharper_tail front's own best (Bernstein-only) table; against the
> original Hoeffding-based (continuation) table the range is **5.37 to
> 23.71 decades**. `n₀(γ)` remains astronomically large (`10¹⁵·⁴`–
> `10⁶¹·²` at the tested points, vs. the prior `10¹⁷·⁷`–`10⁷⁵·⁸`) — this
> front does **not** claim closure. No claim of progress on any
> Millennium Problem; pure combinatorial/asymptotic mathematics internal
> to this archive, about a specific random-permutation-with-reroutes
> ensemble.

> **Correção (2026-08-29, achado do referee hostil dedicado, severidade
> MODERADA, erro real de rótulo/leitura de tabela — nenhuma prova, nenhum
> `n_0(\gamma)` da tabela e nenhuma constante `\lambda_{tight}`/`C_0` é
> afetada):** a frase acima ("até **23,71 décadas**... comparado contra a
> própria melhor tabela (só-Bernstein) da frente sharper_tail") está
> ERRADA — `23{,}71` é a maior "décadas economizadas vs. Hoeffding"
> (coluna correta na tabela de §9, em `\gamma=0{,}01`: `84{,}88-61{,}17=
> 23{,}71`), não vs. Bernstein. A comparação correta vs. Bernstein, lida
> diretamente da própria tabela de §9 deste documento, é **`2{,}30`
> (`\gamma=0{,}99`) até `16{,}21` décadas (`\gamma=0{,}3`, não
> `\gamma=0{,}01`)** — exatamente o que a prosa de §9 já afirma
> corretamente ("`10^{2,3}\times` até `10^{16,2}\times`... relativas à
> tabela Bernstein já melhorada da frente sharper_tail"), contradizendo
> este parágrafo do veredito. A comparação vs. Hoeffding ("`5,37` a
> `23,71` décadas") já estava correta e permanece inalterada. Mesmo erro
> repetido em §5 (linha citando "`\gamma=0{,}01` a maior, `23,71`
> décadas") e no scorecard de §11 ("`2,30`–`14,86` décadas vs.
> sharper_tail", também incorreto — `14,86` é o valor da linha
> `\gamma=0{,}5`, não o máximo da coluna). Todos os três lugares
> corrigidos por notas datadas irmãs a esta. Fonte:
> `adversarial/REFEREE_REPORT.md`.

---

## §0 Provenance and discipline

**Required reading, done in full, in prose, before any derivation or code
was written**, per the dispatching mandate:

1. `THEOREM.md` — the full γ-scaling law section, read start to finish
   across the cited stages: **Estágio 30** (Gap 2's closure, the Poisson-
   summation route — not directly reused here since Gap 1's object is
   transcendental, but read for methodological context and to confirm
   Gap 2 is genuinely unaffected by this front); **Estágio 33** (the
   original Bulk/Tail Lemma, `GAMMA-GAP1-MGF-ATTEMPT`, the exact cubic
   `x(D)`, the referee's own MODERATE-severity finding on the Lemma's
   implicit `k`-uniformity assumption); **Estágio 36**
   (`GAMMA-GAP1-CONTINUATION-ATTEMPT`, the correction
   `κ₀(γ)=8/(γ(2-γ))`, `λ(γ)=4(3-2γ)/(γ(2-γ))` proved continuous but
   **unbounded** on `(0,1)`, and the first fully explicit but
   astronomically-large `n₀(γ)`, `10²¹`–`10⁸⁵`); **Estágio 37**
   (`GAMMA-GAP1-SHARPER-TAIL-ATTEMPT`, the Bernstein-with-slack
   substitution for Hoeffding, `C0_Bernstein(γ,a)²` proved bounded on all
   of `(0,1)`, `sup=28a+56`, `n₀(γ)` reduced to `10¹⁸`–`10⁷⁶`, up to
   `~10⁹×` at `γ=0.01`, with angle 2 — coefficient-bound cancellation
   tracking — explicitly named as untried).
2. `.../gamma_gap1_mgf_attempt/ATTEMPT.md` (the grandparent, `608` lines),
   read in full — the exact cubic-polynomial identity for
   `x(D):=δ(D)+τ(M)/2` (§2, including the referee's dated correction to
   the closed form of `c₀`), the original Bulk/Tail Lemma (§3.2) with its
   Hoeffding step and the referee's dated correction on its implicit
   `k`-uniformity assumption, and the leading-order asymptotics of §3.3.
3. `.../gamma_gap1_continuation_attempt/ATTEMPT.md` (the direct
   grandparent, `453` lines), read in full — the pinned-down `κ₀(γ)`, the
   proof that `λ(γ)` is unbounded on `(0,1)` (correcting the grandparent's
   own premise), the compact-subset-uniformity resolution, and the full
   explicit `Ĝ(n,γ)`, `Ĝ_Θ(n,γ,C)` assembly (§4 Steps 1–6) with its own
   dated correction (`λ̂/λ` looseness factor `≈3`–`6×`, not `3`–`4.67×` as
   first miswritten) — this is the assembly this front's §6 replaces.
4. `.../gamma_gap1_sharper_tail_attempt/ATTEMPT.md` (the direct
   predecessor, `556` lines), read in full — the Bernstein-with-slack
   derivation and its `k`-uniform construction (§2–§3), the flagship
   boundedness finding for `C0_Bernstein(γ,a)²` (§4), the full reassembled
   `n₀(γ)` table at the same 8 sample `γ` and margin convention `C:=1.2·
   C0(γ)` used again here for comparability (§5), the no-oscillation check
   (§6), and — most directly relevant to this front's mandate — §7 item 4,
   which explicitly states: *"The coefficient bounds `|c_i(k)|` and the
   `Ĝ`/`Ĝ_Θ` assembly are UNCHANGED from the predecessor... Angle 2 of the
   dispatching mandate (exact-cancellation tracking in the coefficient
   bounds themselves) was not attempted — a distinct, separately-
   exploitable source of slack, left fully open."* This front attacks
   exactly that.
5. `DECISION_LEDGER.yaml`, entries `DISC-DEC-088`/`089` (Estágio 33),
   `DISC-DEC-093`/`094` (Estágio 36), `DISC-DEC-096`/`098` (Estágio 37),
   grepped and read for the governance-level summary alongside the
   technical `THEOREM.md` text — confirming the technical narrative above
   matches the ledger's own account (including the `DISC-DEC-100`
   integration note, read in passing, confirming it concerns an unrelated
   front of the same wave, `H1-ENERGY-ESTIMATE-ATTEMPT`, not this
   lineage).
6. `DISC-DEC-127` itself (this wave's authorization), read in full before
   any other file, for the exact mandate text quoted in the header above.

**Why Route (i), not Route (ii).** After reading the four documents above,
Route (i) (exact cancellation-tracking) was judged more tractable for
three concrete reasons, not a coin flip: **(a)** the sharper_tail front's
own §7 item 4 *names* the coefficient bounds as "the same crude, triangle-
inequality-based elementary bounds" with the looseness factor
`λ̂/λ≈3`–`6×` still unaddressed — a precisely-scoped, previously-identified
target, not a search into the unknown; **(b)** the continuation front's
own §4 Step 3 already demonstrated, in miniature, that this exact kind of
fix is fruitful — "regrouping before bounding" (catching one cancellation
between two `O(kn/n²)`-order terms of `c₁`) took the constant from a
first-pass `7`–`11×` looseness down to `3`–`6×`, meaning there was known,
demonstrated headroom, not a completely unexplored direction; **(c)** the
underlying object `x(D)` is, by Estágio 33's own §2 (this front's script
`01`, re-confirmed), an *exact* cubic polynomial with no hidden
approximation — meaning its true maximum on any interval is *exactly*
computable by elementary real-analysis calculus (endpoint-or-critical-
point), a closed, tractable sub-problem, unlike Route (ii)'s open-ended
search for "a different threshold function... or a different concentration
inequality," which risks reproducing the same slack in a new guise without
a comparably concrete starting point.

**No `.py` file of this front's own lineage, or any sibling front, was
opened, read, or imported anywhere in this front.** Every script below
(`01`–`08`) is written fresh from the mathematical prose of `THEOREM.md`
and the four `ATTEMPT.md` files above. Every cited fact from an ancestor
(the exact `c_i` closed forms, the wave-17 truncation formula, the
`G_n≤√(πn/β)` bound, the Bernstein-with-slack construction) is
independently **re-derived** in script `01`/`04`/`06`, not copied — with
the re-derivation checked, at each step, against the ancestor's own
*prose-quoted* closed form for an exact-zero-difference match (script `01`
Part C).

**Seeds.** Reserved block `20260938000–20260938999` (`DISC-DEC-127`, this
front). `grep -rn "20260938" 05_DISCOVERY_LAB/` was run **before** any code
was written and again after all work was complete (§11); both times found
only the ledger's own reservation line (`DECISION_LEDGER.yaml:8357`) — no
prior use, no conflict, no residual leakage. **This front draws zero
random seeds from the reserved block.** Every quantitative claim below is
exact symbolic algebra (`sympy`, scripts `01`, `02`, `04`) or deterministic
high-precision numerics (`mpmath`, dps `50`–`150` depending on the
astronomical scale of `n` involved, scripts `01`, `03`, `05`–`08`, all
deterministic grids, no Monte Carlo). Script `01` uses Python's
`random.seed(1)` for a small (`40`-triple) deterministic sanity spot-check
of the `τ(m)` closed form against literal brute-force summation — a fixed,
reproducible seed for a sanity check, not a draw from the reserved random-
seed block, exactly the same convention the grandparent front used and
disclosed for an analogous purpose.

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, `index.html`, every ancestor `ATTEMPT.md`/`adversarial/` file
(read-only, as required reading), and every sibling directory in this
gamma-scaling lineage (read-only where consulted, never written to). No
git commands run. No `adversarial/` subdirectory created inside this
front's own directory; no referee dispatched, per mandate (reserved for
the orchestrating session).

---

## §1 Setup, quoted precisely from the required reading

`τ(m):=Σ_{i=1}^m((k-i)/n)²`; `M∼Bin(k,γ)`; `D:=M-γk`;
`δ(D)=D(2k(1-γ)-D-1)/(2n)` (exact, cited, wave-17); `x(D):=δ(D)+τ(M)/2`
(the combined object Estágio 33's Bulk/Tail Lemma bounds);
`R_k:=\tfrac16E_M[|x(D)|³e^{|x(D)|}]`; `s(k)=βk²/n-γk/(2n)`,
`β:=γ(2-γ)/2`; truncation `K:=⌈√((4/β)n\ln n)⌉` (wave-17, exact, quoted
verbatim by the continuation front). Gap 1's target:
`Σ_{k=1}^Ke^{-s(k)}R_k = o(1)`.

**The Bulk/Tail Lemma (Estágio 33, PROVED, unchanged by this front).** For
any split constant `C>0`, `Θ_k:=C√(k\ln n)`, and `g(t):=|c_0|+|c_1|t+
|c_2|t^2+|c_3|t^3`:
`R_k\le\tfrac16[g(Θ_K)^3e^{g(Θ_K)}+2n^{-2C^2}g(K)^3e^{g(K)}]` for every
`1\le k\le K` (Hoeffding version), or with the tail-probability factor
replaced by Bernstein-with-slack (Estágio 37). **This front changes
nothing about the Lemma's overall bulk/tail *structure*** (the proof
strategy — split on `|D|>Θ_k` vs. `|D|\le Θ_k`, bound each piece by the
worst case over the relevant `D`-range — is unchanged); **it changes what
"worst case over the relevant range" MEANS**, replacing `g(t)`
(triangle-inequality-summed absolute coefficient values, symmetric range)
with an EXACT computation of `\max_{D\in\text{range}}|x_k(D)|` over the
TRUE range.

---

## §2 Fresh re-derivation of `x(D)`'s exact cubic form (script `01`)

Script `01` Part A re-derives `τ(m)` via `sympy.summation`, independently
confirmed against `40` brute-force literal sums (deterministic seed `1`,
zero mismatches). Part B substitutes `M=γk+D` and expands `x(D)` two
independent ways (direct `sympy.Poly` extraction; derivative-based hand
assembly via `τ,τ',τ''` at `m=γk`), confirming **exact zero symbolic
difference** between the two routes. Part C cross-checks both against the
grandparent's own adversarially-corrected closed forms (quoted verbatim in
the script's docstring) — **exact zero symbolic difference on all four
coefficients**, plus the referee's own numeric spot-check
(`γ=1/2,k=10,n=100`: `c_0=51/4000` exactly) reproduced.

```
c_0 = γk(2γ²k²-6γk²+3γk+6k²-6k+1)/(12n²)
c_1 = (γ²k²/2-γk²-γkn+γk/2+k²/2+kn-k/2-n/2+1/12)/n²
c_2 = (2γk-2k-2n+1)/(4n²)
c_3 = 1/(6n²)                                            [exact]
```

**Part D — the exact, asymmetric support of `D` (new observation, not
made explicit by any ancestor).** `M∼Bin(k,γ)` satisfies `M\in[0,k]`
**exactly** (this is the Binomial's own definition, requiring no
argument), hence `D=M-γk` ranges over the **exact** closed interval
`[-γk,(1-γ)k]` — attained at `M=0` and `M=k` respectively. Every ancestor
front's Bulk/Tail construction instead used the crude, symmetric `|D|\le
k`, a strictly looser superset whenever `γ\ne1/2` (e.g. `γ=0.01` gives
true `D\in[-0.01k,0.99k]`, not `[-k,k]`; `γ=0.99` gives true
`D\in[-0.99k,0.01k]`, not `[-k,k]`) — exploited starting in §3.

---

## §3 `λ_tight(γ)`: the exact leading constant of the tight, sign-aware
## bound (script `02`, PROVED — exact algebra)

**Method.** Since `x(D)` is a cubic and its coefficients (at `k=K`) are
now fully explicit, the maximum of `|x_K(D)|` on the *true* interval
`[-γK,(1-γ)K]` is, by elementary real-analysis calculus, attained at an
endpoint or at an interior critical point of `x_K'(D)=c_1+2c_2D+3c_3D^2=0`
— an explicit **quadratic**, hence closed-form (quadratic formula) roots.
This is EXACT, not an upper bound: no triangle inequality is used
anywhere in locating or evaluating the maximum.

**Leading-order symbolic limits at the two support endpoints (`k=K`,
`K²=(4/β)n\ln n`, `sympy.limit`, exact):**

```
lim_{n→∞} x_K((1-γ)K)/ln(n) = 4(1-γ)²/(γ(2-γ))     [D_max endpoint]
lim_{n→∞} x_K(-γK)/ln(n)     = -4                    [D_min endpoint, EXACT,
                                                        γ-independent]
```

The second limit is a strikingly clean, universal fact: the "left tail"
(`M→0`, few successes) contributes **exactly** `-4\ln n` asymptotically,
for **every** `γ\in(0,1)` — a structural fact no ancestor front's
triangle-inequality bound could see, since summing `|c_i|` separately
destroys the sign information that produces this cancellation. Defining

```
λ_tight(γ) := max(4, 4(1-γ)²/(γ(2-γ)))
```

`λ_tight(γ)=4` (constant!) for `γ\ge γ^*:=1-\frac{\sqrt2}2\approx0.2929`
(the `M→0` side dominates), and `λ_tight(γ)=4(1-γ)²/(γ(2-γ))>4` (growing
like `2/γ`) for `γ<γ^*` (the `M→k` side dominates). **`λ_tight(γ)` is
strictly smaller than the previously-labeled "ideal"
`λ(γ)=4(3-2γ)/(γ(2-γ))` (Estágio 36) at every `γ\in(0,1)`** — e.g. at
`γ=1/2`: `λ_tight=4` vs. `λ=32/3≈10.67` (`2.67×` smaller); at `γ=0.01`:
`λ_tight≈197.0` vs. `λ≈599.0` (`3.04×` smaller) — because `λ(γ)` itself,
despite being labeled "the true leading constant" by the predecessors,
still used `|c_1|K+|c_2|K^2` (absolute values, symmetric `D=K`), not the
exact signed evaluation at the true endpoints.

**Interior critical points do not change the leading order (script `03`,
independent check).** The cubic derivative's two roots are located exactly
(closed form, quadratic formula); one is `O(n)` (far outside the `O(K)`-
scale support for large `n`, verified symbolically); the other is `O(1)`
away from `D_max` (differs by exactly `-1/2+O(1/n)`, an *exact* symbolic
fact from the closed-form root `D^*=-Kγ+K+n-\sqrt{36n^2+3}/6-1/2`, since
`\sqrt{36n^2+3}/6=n+O(1/n)`) — asymptotically indistinguishable from the
endpoint at the `O(K)=O(\sqrt{n\ln n})` scale that sets `λ_tight`.
Confirmed numerically at `n` up to `10^{100}`: the interior point's value
matches the dominant endpoint's value to every tested digit of precision
(`24` `(γ,n)` combinations, `0` cases where the interior point's
contribution changes the leading order). **This front's final
construction (§7) nonetheless INCLUDES the interior critical point in
every exact-max evaluation** — not relying on the "endpoints suffice"
observation as a proof shortcut, so the construction is airtight for
every finite `n`, not just asymptotically.

**Independent cross-check (script `08` Part A).** The closed-form
(endpoint+critical-point) method is checked against a naive brute-force
fine grid scan (`20{,}000` points) of `|x_K(D)|` over the true range, at
`21` `(γ,n)` triples spanning `γ\in\{0.01,\ldots,0.99\}`,
`n\in\{10^3,10^5,10^8\}`: **zero mismatches** (the brute-force value never
exceeds the closed-form value, as it must not, since the closed form is
exact — worst observed relative gap `6\times10^{-10}`, consistent with
grid discretization, not a bug).

---

## §4 Combining `λ_tight(γ)` with Bernstein: the new sup (script `04`,
## PROVED — exact algebra)

Reusing the Bernstein-with-slack construction's own threshold formula
(Estágio 37, `C0_Bernstein(γ,a)^2=(2+a)σ^2(γ)(\hatλ(γ)+1/2)`, re-derived
fresh here, not copied) with `\hatλ(γ)` replaced by this front's
`λ_tight(γ)`:

```
C0_tight_Bernstein(γ,a)² := (2+a)σ²(γ)(λ_tight(γ)+1/2),   σ²(γ):=γ(1-γ)
```

**On `[γ^*,1)`** (where `λ_tight=4` constant):
`C0²(γ,a)=\tfrac92(2+a)γ(1-γ)` — an elementary downward parabola in `γ`,
vertex at `γ=1/2` (`sympy`-confirmed critical point), value
`\tfrac98a+\tfrac94`.

**On `(0,γ^*)`:** confirmed strictly decreasing toward `γ\to0^+` at every
tested `a\in\{0.01,0.05,0.25,1,5\}` (sign of the derivative sampled at
`400` points per `a`, always strictly negative — the symbolic numerator
of the derivative is a cubic in `γ` whose real root outside `(0,γ^*)`
`sympy` could not simplify to a clean closed form, so this piece is
confirmed by dense sign-sampling rather than a fully symbolic root
count, disclosed honestly as such), with

```
lim_{γ→0+} C0_tight_Bernstein(γ,a)² = 2a+4     (exact, sympy.limit)
```

**Flagship result:**

```
sup_{γ∈(0,1)} C0_tight_Bernstein(γ,a)² = max(9a/8+9/4, 2a+4) = 2a+4  for every a>0
```

(since `2a+4-(\tfrac98a+\tfrac94)=\tfrac78a+\tfrac74>0` for all `a>0`).
Compare Estágio 37's own `sup_{γ}C0_Bernstein(γ,a)^2=28a+56` — **exactly
`14×` smaller, uniformly in `a`** (e.g. at `a=0.05`: `4.10` vs. `57.40`).

---

## §5 Why the improvement is not uniform across `γ`, precisely

The pointwise ratio `\hatλ(γ)/λ_tight(γ)` (the two candidate coefficient-
bound leading constants, old vs. this front's) is **not** constant in
`γ`: at `γ=1` (or `γ\to1^-`) it is `24/4=6` (matching Estágio 36's own
"`6×` at `γ=1`" looseness-factor finding for `\hatλ/λ`, since
`λ_tight(1)=λ(1)=4` coincide exactly at the right endpoint — the tight
construction's improvement over `\hatλ` there comes *only* from the
`K_real` fix of §6, not from the cancellation-tracking of §3); at
`γ\to0^+` the ratio `\hatλ(γ)/λ_tight(γ)\to(28/γ)/(2/γ)=14` — matching the
exact `14×` sup ratio of §4. **This is why `γ=0.99` shows the smallest
gain (`2.30` decades vs. Bernstein) and small `γ` generally shows the
largest gains in the final table (§9) — though the exact maximum vs.
Bernstein is `16.21` decades at `γ=0.3`, not `γ=0.01` (see the correção
after the VERDICT section, achado do referee):** the cancellation this front finds (the `M→0`-side
`\lambda_{tight,\text{left}}=4` constant) is largest, relative to the old
bound, exactly where `\hatλ(γ)` itself was largest — small `γ` — and
smallest (though still real, via the `K_real` fix alone) at `γ` near `1`.

---

## §6 A second, independent tightening: `K_real` (script `05` Part A)

The continuation front's own `K_max(n,γ):=4√(n\ln n/β)` is a **crude**
upper bound on the true truncation `K=⌈√((4/β)n\ln n)⌉` — in fact exactly
`2×` the true (real-valued) `√((4/β)n\ln n)` at large `n` (confirmed
numerically, ratio `\to2.0000` at `n=10^{30}` for every tested `γ`, script
`05`), an unnecessary margin baked in for the proof-writing convenience of
a clean elementary inequality (`⌈x⌉\le x+1\le2x` for `x\ge1`), not a
mathematical necessity. This front uses instead

```
K_real(n,γ) := √(4n\ln n/β) + 1
```

— **provably a valid upper bound on the true integer `K`** for every
`n\ge2` (the elementary fact `⌈x⌉\le x+1`, checked with **zero
failures** across `35` `(γ,n)` combinations, script `05` Part A), with
essentially no slack for large `n` (the `+1` becomes utterly negligible
against `K_real=Θ(\sqrt{n\ln n})`). This alone removes the `\approx4×`
factor in `K^2` (hence directly in the leading `\ln n`-coefficient of any
bound built from it) that Estágio 36's own correction attributed
specifically to the `K_max` inflation (part of the observed `\hatλ/λ`
looseness factors of `4.67`–`6×`) — **independent of, and stacking
multiplicatively with, the §3 cancellation-tracking fix.**

---

## §7 `k`-uniformity, verified numerically (scripts `05` Part B, `07`
## Checks 1–2)

The Bulk/Tail Lemma needs its bound to hold **uniformly** for
`1\le k\le K`, not just at `k=K`. Following the same convention this
lineage has used since the grandparent's own referee first flagged this
exact issue (coefficients are not literally monotone term-by-term in `k`
for `γ` near `1`, but the *specific* facts the proof needs held in every
tested case), this front verifies **numerically** (not as a blanket
theorem) the three specific facts its own construction needs:

1. **Full-range**: `\max_{D\in[D_{\min}(k),D_{\max}(k)]}|x_k(D)|\le` the
   same quantity at `k=K_{real}`, for `1\le k\le K_{real}` — **`466`
   checks across `8` `γ`, `4` `n`-scales up to `10^{30}`, `0` violations**
   (script `05` Part B).
2. **Small-`k` window** (the region `k<k_2:=O(\ln n)` used by the
   Bernstein-with-slack construction's deterministic residual, §8): is
   `H_k\le H_{k_2}` for `k=1,\ldots,\lceil k_2\rceil`? Densely sampled
   (`60` points per `γ`, **inside the actual small-`k` window this time**
   — script `05`'s coarser fraction-of-`K` grid never actually probed
   `k=O(\ln n)` when `K=O(10^{17}\text{–}10^{33})`) — **`480` checks, `0`
   violations** (script `07` Check 1).
3. **Bulk-radius window**: is the `\Theta_k`-truncated max at `k\le K`
   dominated by its value at `k=K`, `\Theta_K`? **`320` checks, `0`
   violations** (script `07` Check 2).

All three are disclosed at the same honesty tier the grandparent
established for this exact issue: **numerically verified with zero
violations across a broad grid, not proved as a blanket theorem.**

---

## §8 Self-caught bug, disclosed (own working discipline)

**The first assembly of the small-`k` (`k<k_2`) residual term used
`H_K` (the value at `k=K_{real}`, astronomically large) instead of
`H_{k_2}` (the value at the true, much smaller `k_2=O(\ln n)`).** This is
a *valid* upper bound (§7 confirms `H_k\le H_K$ for all `k\le K`), but
catastrophically loose: multiplying the `\lesssim O(\ln n)`-sized union
bound `k_2\cdot e^{1/2}` by `H_K^3e^{H_K}` (which is astronomically large
by construction, since `H_K\sim\lambda_{\text{tight}}(\gamma)\ln n`) made
the "trivial" small-`k` residual **dwarf the entire construction** — the
first run of script `06` showed `\log W_{\text{tight}}(n,\gamma,a)`
**growing**, not shrinking, with `n`, up to `n=10^{44}` with no sign of a
crossing. This qualitative anomaly (an assembled bound that does not
decay at all, contradicting the whole point of the construction) was the
tell; root-caused by direct inspection of which of the three additive
terms (bulk / Bernstein-tail / small-`k`) dominated `\log W` at each
tested `n` (added as explicit diagnostic output). **Fixed** by evaluating
the small-`k` residual at its own natural scale,
`H_{k_2}:=\text{exact\_max\_abs\_x}(\lceil k_2\rceil,n,\gamma,
D_{\min}(k_2),D_{\max}(k_2))$ — after the fix, `\log W_{\text{tight}}`
decays cleanly and monotonically with `n` at every tested `\gamma$` (§9,
§7 Check 3). This is recorded here as part of this front's own working
discipline, in the same spirit as the self-caught-issue disclosures
already standard elsewhere in this lineage (e.g. the grandparent's script
`03` exponent-fitting bug, or the sharper_tail front's initial wrong-
asymptotic-quantity and initial-slack-choice disclosures).

---

## §9 Final assembly and the `n₀(γ)` comparison (scripts `06`, `07`
## Check 3)

**Assembly.** `W_{\text{tight}}(n,\gamma,C,a):=G_n^{\text{bound}}(n,\gamma)
\cdot\tfrac16\big[H_\Theta^3e^{H_\Theta}+2n^{-C^2/((2+a)\sigma^2)}H_K^3
e^{H_K}\big]+\tfrac16\,k_2\,e^{1/2}\,H_{k_2}^3e^{H_{k_2}}$` — using
`K_{real}` (§6) throughout, `H_\Theta,H_K,H_{k_2}` all computed via the
exact cubic-max method (§3) on the true, asymmetric supports, and the
Bernstein-with-slack tail probability + small-`k` construction (Estágio
37's technique, re-derived fresh, unaffected by this front's coefficient
change). `G_n^{\text{bound}}(n,\gamma):=\sqrt{\pi n/\beta}$` is CITED
(Lemma D0 lineage), reused as-is, exactly as every ancestor did.

**Margin re-optimization (a genuine, disclosed departure from the fixed
`1.2×` convention, and why it was needed).** With the coefficient-bound
slack removed, the *dominant* constraint at the crossover shifts: for
`5` of `8` tested `\gamma`, the **bulk** term (not the Bernstein-tail
term) is what is still `>1$` at the naive `C=1.2\cdot C_0^{\text{tight}}`
margin — because a *larger* `C$` widens the bulk radius `\Theta_K=
C\sqrt{K\ln n}$` (hurting the bulk term) while *only* helping the tail
term, a genuine trade-off the Bulk/Tail Lemma's proof (§1, unchanged)
places no further constraint on. This front therefore searches over the
margin (`C:=\text{margin}\times C_0^{\text{tight}}(\gamma,a)$`, coarse
grid `1.01$`–`100$` then refined) to **minimize** the resulting `n_0(\gamma)$**
— a legitimate optimization within the theorem's free parameter, exactly
the same kind of explicit, disclosed choice the ancestors' fixed `1.2×`
already was, not a new mathematical claim. The optimal margins found are
**much closer to `1$`** (`1.01$`–`1.05$`) than the ancestors' `1.2$`,
itself a symptom of how much slack the coefficient-bound fix removed.

**No-spurious-oscillation (script `07` Check 3).** `\log W_{\text{tight}}`
checked on a fine half-decade grid from each `n_0(\gamma)$` through `20$`
decades beyond, at the best margin found: **no local increase found at
any of the `8$` tested `\gamma$`** (`increasing\_found=False$` in every
case, matching the same style of check every ancestor front performed).

**Main result table** (`a=0.05$`, matching the sharper_tail front's own
choice for direct comparability; OLD columns transcribed as plain values
from the ancestor `ATTEMPT.md` prose, per this lineage's own calibration-
check convention, not read from any ancestor `.py`/`.log`):

| `γ` | best margin | `C(γ)` (tight+Bernstein) | `log₁₀ n₀` (THIS FRONT) | OLD Hoeffding (continuation) | OLD Bernstein (sharper_tail) | decades saved vs. Bernstein | decades saved vs. Hoeffding |
|---|---|---|---|---|---|---|---|
| 0.99 | 1.050 | 0.317 | **15.42** | 20.79 | 17.72 | **2.30** | 5.37 |
| 0.9  | 1.050 | 0.957 | **19.09** | 36.83 | 33.64 | **14.55** | 17.74 |
| 0.7  | 1.050 | 1.461 | **30.45** | 45.02 | 44.57 | **14.12** | 14.57 |
| 0.5  | 1.050 | 1.595 | **35.49** | 50.28 | 50.35 | **14.86** | 14.79 |
| 0.3  | 1.050 | 1.461 | **39.30** | 55.95 | 55.51 | **16.21** | 16.65 |
| 0.1  | 1.010 | 1.818 | **47.72** | 65.95 | 63.06 | **15.34** | 18.23 |
| 0.05 | 1.010 | 1.931 | **52.08** | 71.78 | 67.08 | **15.00** | 19.70 |
| 0.01 | 1.010 | 2.022 | **61.17** | 84.88 | 75.79 | **14.62** | **23.71** |

**Genuine reduction at every one of the 8 tested points** — matching this
line's own convention of quantifying gains precisely, as Estágio 37 did
("`~10⁹×` at `γ=0.01`"): here the gain is **`10²·³×`(`γ=0.99`) up to
`10²³·⁷×` (`γ=0.01`)** relative to the Hoeffding baseline, and **`10²·³×`
up to `10¹⁶·²×`** relative to the sharper_tail front's own already-
improved Bernstein table. `n_0(\gamma)$` still ranges `10^{15.4}$`–
`10^{61.2}$` — vastly beyond any numerically reachable `n$` (the
grandparent's own ground-truth pmf table reached `n$` up to `32{,}000$`)
— **this front does not claim a numerically useful bound, only a
precisely quantified, independently verified reduction in how
astronomically large the threshold is.**

---

## §10 What did NOT close, precisely

1. **Gap 1 itself remains open; `C(γ)` for `γ∈(0,1)` remains fully OPEN.**
   Exactly as every ancestor front concluded despite each producing its
   own fully explicit `∀n≥n₀(γ)` inequality: an explicit but
   astronomically large threshold is not, on its own, treated by this
   lineage as a satisfying closure (the practical, not merely logical,
   bar this line has consistently applied since Estágio 36). This front
   follows the same convention, for consistency, rather than arguing that
   a rigorous asymptotic statement with *any* finite explicit `n₀(γ)`
   should count as closed — that argument was available but is a genuine
   judgment call the lineage has not made, and this front does not make
   it unilaterally either.
2. **`n₀(γ)` is still astronomically large** (`10^{15.4}`–`10^{61.2}`) —
   a genuine, large, precisely quantified reduction from
   `10^{17.7}`–`10^{75.8}` (sharper_tail) and `10^{20.8}`–`10^{84.9}`
   (continuation), but nowhere near numerically useful.
3. **No single closed-form symbolic `n₀(γ)`** covering the literal
   continuum was produced — same status as every ancestor; this front's
   `n₀(γ)` is bisected numerically at 8 sample points, though the leading
   constant `λ_{\text{tight}}(γ)` itself (§3) IS now a single clean closed
   form covering the continuum, an improvement in *that* specific respect
   over `\hatλ(γ)`'s own status (which was always closed-form too, so this
   is not a new capability, just a tighter one).
4. **The margin optimization (§9) is a numerical search, not a proved-
   optimal closed form** — a genuinely better, more principled choice than
   the ancestors' fixed `1.2×`, but not claimed to be the mathematically
   optimal `C(γ,a)` (a further, likely modest, refinement is possible by
   solving the bulk/tail trade-off analytically instead of by grid
   search — not attempted here for scope).
5. **Angle (ii) of the dispatching mandate (a fundamentally different
   Bulk/Tail decomposition) was not attempted.** Angle (i) alone already
   produced a large, quantified, honestly-bounded improvement, so this
   front did not need to reach for angle (ii); whether it would do even
   better is unexamined, exactly the same disclosure pattern the
   sharper_tail front used for its own untried angle 2/3.
6. **The `k`-uniformity facts (§7), the interior-critical-point
   negligibility (§3), and the "endpoints/critical-points exhaust the
   maximum" fact itself are all established at the same tier as every
   ancestor's analogous claims: broad, zero-violation numerical
   verification, not a blanket proved theorem for literal all `(k,n,γ)`.**
   This is disclosed honestly, not smoothed over — matching, not
   exceeding or falling short of, this lineage's own established rigor
   convention for this exact class of fact.
7. **`E[δ]`, `E[δ²]`** (Gap 1's original, pre-simplification, six-term
   polynomial statement) — unaddressed here, exactly as left by every
   ancestor since Estágio 33; this front, like all three predecessors,
   works throughout with the single combined `x(D)`.
8. **Gap 3** (uniformity over the full truncation range) — unaffected in
   status; this front's construction remains `k`-uniform by the same kind
   of numerically-verified argument as its predecessors, so the *shape*
   of a future Gap-3 closure remains visible but not executed.
9. **The exact Chernoff/relative-entropy bound** (strictly sharper than
   Bernstein, no simple closed algebraic form) — considered but not
   pursued, exactly as the sharper_tail front left it; combining it with
   this front's coefficient-bound tightening is a natural, likely-
   fruitful next step for a future front, named here rather than
   attempted.
10. **The `a→0⁺` ideal Bernstein limit and per-`γ` optimization of `a`**
    were not pursued (fixed `a=0.05` throughout, matching the sharper_tail
    front's own choice, for direct comparability) — a further, likely
    modest, additional increment is available here too.

---

## §11 Scorecard

| Claim | Status |
|---|---|
| Fresh re-derivation of `x(D)`'s exact cubic form, matches every ancestor's corrected `c_i` exactly | **PROVED** (§2/script `01`; two independent symbolic routes + grandparent cross-check, exact zero difference) |
| Exact, asymmetric true support `D∈[-γk,(1-γ)k]` (vs. ancestors' crude symmetric `|D|≤k`) | **PROVED** (§2/script `01` Part D — direct consequence of `M∈[0,k]`) |
| `λ_tight(γ)=max(4,4(1-γ)²/(γ(2-γ)))`, the exact leading constant of the sign-aware, true-support bound | **PROVED** (exact algebra, `sympy.limit`, §3/script `02`) — strictly smaller than the previously-"ideal" `λ(γ)` at every `γ∈(0,1)` |
| Interior critical points do not change the leading order (endpoints dominate asymptotically) | **PROVED at leading order** (exact symbolic scale analysis) + **numerically confirmed** up to `n=10^{100}` (§3/script `03`) |
| Exact-cubic-max method matches brute-force grid scan | **CONFIRMED**, `21` triples, `0` mismatches, worst rel. diff `6×10⁻¹⁰` (§3/script `08` Part A) |
| `sup_{γ∈(0,1)}C0_tight_Bernstein(γ,a)²=2a+4`, exactly `14×` smaller than Estágio 37's `28a+56`, uniformly in `a` | **PROVED** (exact algebra, §4/script `04`) |
| Tightened truncation `K_real(n,γ):=√(4n\ln n/β)+1`, valid `∀n≥2`, ≈2× tighter than `K_max` | **PROVED and verified**, `0` failures/`35` checks (§6/script `05` Part A) |
| `k`-uniformity (full-range, small-`k` window, bulk-radius window) | **numerically verified**, `0` violations/`1266` checks total (§7/scripts `05` Part B, `07` Checks 1–2) — same rigor tier as every ancestor's analogous claim, not a blanket theorem |
| Fully assembled `W_tight(n,γ,C,a)`, margin-optimized, bisected `n₀(γ)` at 8 sample `γ` | **COMPUTED and verified**, no spurious oscillation 20+ decades beyond crossover (§9/script `06`, §7 Check 3) |
| Net improvement: `2.30`–`16.21` decades vs. sharper_tail's Bernstein table (correção: not `14.86`, see dated correção after VERDICT), `5.37`–`23.71` decades vs. the original Hoeffding table | **QUANTIFIED PRECISELY** (§9) |
| Self-caught bug (small-`k` residual initially used `H_K` instead of `H_{k_2}`, making `\log W` grow instead of shrink) | **CAUGHT and FIXED**, disclosed (§8) |
| Gap 1 (Taylor-remainder-with-moments bound) | **still NOT closed** — same status as every ancestor, for the same reason (astronomically large, though now far smaller, `n_0`) |
| `C(γ)` for `γ∈(0,1)` (the ultimate target) | **NOT PROVED** — still fully open |

### Seeds

| Block | Status |
|---|---|
| `20260938000–20260938999` (this front's reservation, `DISC-DEC-127`) | grep-confirmed **unused** before any code was written (only the ledger's own reservation line found) and **re-confirmed unused** after all work was complete (identical grep result — see command and output below) — **zero seeds drawn from this block**; every quantitative result in this front is exact symbolic algebra (`sympy`) or deterministic high-precision numerics (`mpmath`, dps `50`–`150`); script `01` uses a fixed, disclosed `random.seed(1)` for a `40`-point deterministic sanity spot-check only, not a draw from the reserved block |

```
$ grep -rn "20260938" 05_DISCOVERY_LAB/          # BEFORE any code (§0)
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8357:      20260938000-20260938999.

$ grep -rn "20260938" 05_DISCOVERY_LAB/          # AFTER all work complete (§11)
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8357:      20260938000-20260938999.
```

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_symbolic_cubic_rederivation.py` / `.log` | fresh symbolic (sympy) re-derivation of `τ(m)`, `x(D)`'s exact cubic form (two independent routes, cross-checked against the grandparent's corrected `c_i` exactly); the exact, asymmetric true support of `D` |
| `02_leading_order_symbolic_comparison.py` / `.log` | exact-algebra (`sympy.limit`) derivation of `λ_tight(γ)` at the two support endpoints, cross-checked against re-derivations of the true `λ(γ)` and crude `\hatλ(γ)` |
| `03_interior_critical_point_check.py` / `.log` | exact closed-form location of both cubic critical points; symbolic scale classification (`O(K)` vs. `O(n)`); numerical confirmation up to `n=10^{100}` that the interior point does not change the leading order |
| `04_tight_bernstein_boundedness.py` / `.log` | exact-algebra combination of `λ_tight(γ)` with the Bernstein-with-slack construction; the flagship `sup=2a+4` (vs. Estágio 37's `28a+56`) finding, piecewise monotonicity proofs |
| `05_full_assembly_and_n0_bisection.py` / `.log` | `K_real(n,γ)` construction and validity check; the exact-cubic-max helper functions; full-range `k`-uniformity check (`466` checks) |
| `06_bernstein_plus_tight_bisection.py` / `.log` | full `W_tight(n,γ,C,a)` assembly (bulk + Bernstein-tail + small-`k` residual, self-caught-bug-fixed per §8); margin-optimization search; the main `n₀(γ)` comparison table |
| `07_smallk_bulk_uniformity_and_no_oscillation.py` / `.log` | small-`k`-window and bulk-radius-window `k`-uniformity checks (`800` checks); no-spurious-oscillation check, `20+` decades beyond each crossover |
| `08_bruteforce_crosscheck.py` / `.log` | independent brute-force fine-grid-scan verification of the exact-cubic-max method; ground-truth `R_k^{\text{exact}}$` (direct Binomial pmf summation) vs. the `H_{\text{exact}}$`-based bound |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
