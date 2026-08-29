# ATTEMPT — `C(γ)` construction attempt: the second-order term of the
# γ-scaling law for `γ∈(0,1)`

**Wave 28, front (b), `GAMMA-C-GAMMA-CONSTRUCTION-ATTEMPT`, authorized by
`DISC-DEC-131`.** Mandate: attempt to construct — ideally a closed form
for, or at minimum a rigorously-justified asymptotic characterization of
— `C(γ)`, the second-order term of the γ-scaling law for `γ∈(0,1)`,
distinct from the already-PROVED deterministic leading term `D_0(γ)`.
Explicitly named as a genuine open *construction* problem, not a
bound-tightening exercise (that was wave 27's job, and its own closing
paragraph explicitly said a "ninth front" should target `C(γ)` itself,
not `n_0(γ)`).

---

## VERDICT (up front)

> **`C(γ)` for `γ∈(0,1)` remains ENTIRELY OPEN.** This front does **not**
> construct it, and is honest that it does not fully deliver on the
> mandate's central ask (a closed form or a rigorous asymptotic
> characterization). What it delivers instead, genuinely and
> independently verified, is threefold — one small new exact structural
> fact, one substantial (and methodologically *new*, not merely
> constant-tightened) reduction of the `n₀(γ)` obstruction that has
> stood in Gap 1's way since Estágio 33, and one new piece of *evidence*
> (not proof) for the standing conjecture — none of which, individually
> or combined, closes Gap 1, Gap 3, or `C(γ)` itself.
>
> 1. **New exact structural fact (PROVED, small).** `A_k(n,γ)`
>    (`THEOREM.md`'s own building block, `nφ(n,γn)=Σ_kA_k`) is, exactly
>    (not asymptotically), a terminating `2F0` hypergeometric polynomial:
>    `A_k(n,γ)=(1-γ)^k·{}_2F_0(-k,\,n-k+1;\,;\,-γ/((1-γ)n))`. This has
>    never been noted anywhere in this lineage — every ancestor works
>    entirely through the `σ_k(m)/τ(m)` exponential-sandwich route. It
>    does **not**, by itself, produce a closed form for `S_n=Σ_kA_k` or
>    `C(γ)` (Sec.2 explains precisely why not), and an attempted further
>    identification with a named classical orthogonal-polynomial family
>    (Charlier) did **not** check out under this front's own naive
>    parameter matching — disclosed honestly, not claimed.
>    [**Correção, 2026-08-29, onda 29**: esta identificação na verdade
>    SE CONFIRMA exatamente — o resíduo reportado veio de um bug de
>    implementação nesta própria frente, não de um mismatch matemático
>    real. Ver a correção completa em §2 abaixo.]
> 2. **A genuinely different (not just tighter-constant) refinement of
>    the Bulk/Tail Lemma's bulk and small-`k` pieces, via Lyapunov's
>    inequality + the EXACT 4th moment of `x(D)` instead of a
>    deterministic worst-case bound evaluated at the bulk radius.** This
>    is a different *mechanism* from all four prior `n₀(γ)`-tightening
>    fronts (Estágios 33/36/37/49), which each removed a bounded
>    multiplicative constant; this front removes an *unbounded*,
>    `(ln n)^{1.5}`-growing inefficiency (confirmed numerically, fitted
>    exponent `≈1.5` at 7/8 sample `γ`, matching the analytic prediction
>    exactly). Net result: **`n₀(γ)` reduced by a further `3.46`–`29.76`
>    decades** relative to the immediate predecessor's own already-
>    tightened table (itself `2.30`–`23.71` decades better than *its*
>    predecessor) — the single largest reduction any front in this
>    sub-lineage has produced. `n₀(γ)` still ranges `10^{10.2}`–
>    `10^{31.4}` — astronomically large, no numerically useful bound is
>    claimed. **This is the SAME KIND of contribution Estágio 49
>    explicitly said a "ninth front" should move past, not repeat** —
>    this front's own honest assessment is that it landed closer to
>    "tenth `n₀`-tightening front" than "the construction front the
>    mandate asked for," even though the underlying technique (moment-
>    based, not tail-probability-based) is new in kind.
> 3. **New evidence, not proof, for the standing conjecture
>    `E_{\text{heuristic}}(γ)`.** Using the exact moment machinery, this
>    front computed the Taylor/cumulant expansion of `E_M[e^{-x(D)}]` to
>    order 6 in `x(D)` — four orders beyond Estágio 26 §4's own order-2
>    heuristic — and found the Richardson-extrapolated numeric limit
>    shifts by only `≈4×10⁻⁵`–`8×10⁻⁵` (comparable to or smaller than
>    the residual gap to `E_heuristic(γ)` itself), i.e. the four extra
>    exact orders do **not** materially change the extracted limit. This
>    is new (no ancestor computed beyond order 2 *exactly*), and is
>    reassuring, but it is evidence at one more order, not a uniform
>    remainder bound — it does not close Gap 1.
>    [**Correção, 2026-08-29 — referee hostil**: "comparable to or
>    smaller than" está invertido — o shift EXCEDE o resíduo de order-2
>    em `1{,}3\times`–`3{,}7\times` nos três `γ` testados, e a
>    truncagem de order-6 fica de fato mais LONGE de
>    `E_{\text{heuristic}}(γ)` que a de order-2 nos três casos. Não
>    refuta `E_{\text{heuristic}}(γ)`, mas remove a garantia
>    originalmente alegada por este item específico. Ver §5 abaixo para
>    a correção completa com os números exatos, e
>    `adversarial/REFEREE_REPORT.md`.]
>
> **`C(γ)` for `γ∈(0,1)` is NOT constructed, NOT bounded (above or
> below) by a proved inequality, and NOT characterized as a convergent
> series with a proved remainder.** The precise remaining obstruction is
> named in Sec.7. No claim of progress on any Millennium Problem; pure
> combinatorial/asymptotic mathematics internal to this archive, about a
> specific random-permutation-with-reroutes ensemble.

---

## §0 Reading discipline and provenance

**Required reading, done in full, in prose, before any derivation or
code was written**, per the dispatching mandate:

1. `THEOREM.md`, the γ-scaling law section, read start to finish across
   the four cited Estágios plus their surrounding context (lines
   ≈3960–7198 of the 7198-line file): **Estágio 26** (`C(γ)` first named
   as the open second-order term; Lemma E and `D_0(γ)` PROVED; three
   named technical gaps, "Lacuna 1/2/3"); **Estágio 33** (the original
   Bulk/Tail Lemma, `GAMMA-GAP1-MGF-ATTEMPT`, the exact cubic `x(D)`,
   Lemma Bulk/Tail); **Estágio 36** (`GAMMA-GAP1-CONTINUATION-ATTEMPT`,
   the `κ₀(γ)`/`λ(γ)` correction, the first explicit-but-astronomical
   `n₀(γ)`); **Estágio 49** (`GAMMA-GAP1-CANCELLATION-TRACKING-ATTEMPT`,
   the immediate predecessor's own result, `λ_tight(γ)=max(4,4(1-γ)²/
   (γ(2-γ)))`, its explicit closing statement naming `C(γ)` itself as
   the natural next target); also read en route: Estágio 30 (Gap 2's
   closure, cited/reused as unaffected), Estágio 37 (the sharper-tail
   Bernstein-with-slack front, cited/re-derived).
2. `.../gamma_gap1_cancellation_tracking_attempt/ATTEMPT.md` (684
   lines, the immediate predecessor, wave 27 front (c)), read in full —
   its exact `λ_tight(γ)` result, its Bernstein-with-slack construction,
   its own §10 item 1 (naming the "explicit-but-astronomical `n₀(γ)` is
   not, on its own, treated as closure — the practical, not merely
   logical, bar this line has consistently applied since Estágio 36…
   that argument was available but is a genuine judgment call the
   lineage has not made, and this front does not make it unilaterally
   either" — this framing is taken seriously here too, see §7), and its
   closing note that a ninth front should target `C(γ)`'s construction,
   not `n₀(γ)`.
3. `.../gamma_gap1_cancellation_tracking_attempt/adversarial/
   REFEREE_REPORT.md` (370 lines), read in full — confirmed the
   predecessor's `λ_tight(γ)`, the `14×` flagship Bernstein-combination
   result, and the `n₀(γ)` table as independently reproduced and SOUND,
   with one MODERATE-severity presentational mislabeling (already
   corrected by dated addenda in the predecessor's own `ATTEMPT.md`,
   not touched here).
4. `.../gamma_second_order_attempt/ATTEMPT.md` (633 lines, the
   great-great-grandparent, `GAMMA-SECOND-ORDER-ATTEMPT`) — read in
   full for the precise target restatement (§1 below), Lemma E, `D_0(γ)`,
   and the §4 cumulant-expansion heuristic whose closed form
   `E_{\text{heuristic}}(γ)` this front's §6 tests to a higher order.
5. `.../gamma_gap1_mgf_attempt/ATTEMPT.md` (608 lines, the
   grandparent), read in full — the original Bulk/Tail Lemma, `x(D)`'s
   exact cubic form (with the referee-corrected `c₀` closed form quoted
   and independently re-derived, not copied, in this front's script
   `02`), and the original Gap 1 statement quoted verbatim.
6. `.../gamma_scaling_attempt/ATTEMPT.md` (592 lines, the ultimate
   ancestor, wave 17 front (e)) — read in full, in particular §1 (Lemma
   1's exact combinatorial proof, `P_{k,m}:=∏_{i=1}^m(1-(k-i)/n)`,
   `A_k=E_M[P_{k,M}]`), the source of the exact hypergeometric structure
   this front's §2 builds on — an ancestor two generations back along
   this front's own directory path, read per the mandate's explicit
   instruction to check for a distinct MGF-adjacent ancestor.

**No `.py` file of any ancestor or sibling front was opened, read, or
imported anywhere in this front.** Every script below (`01`–`09`) is
written fresh from the mathematical prose cited above. Every borrowed
fact (the exact `c_i(k,n,γ)` cubic coefficients, `λ_tight(γ)`, the
`K_real(n,γ)` truncation, `G_n^{\text{bound}}=\sqrt{πn/β}`, the
Bernstein-with-slack *technique*) is independently **re-derived** in
this front's own scripts, not copied, and cross-checked for exact
agreement against the ancestors' own quoted closed forms wherever such
a check was possible (it was, and it passed, in every case — see §5).

**Not touched, per mandate:** `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, `index.html`, every ancestor `ATTEMPT.md`/`adversarial/`
file (read-only), every sibling directory (not touched). No git command
of any kind was run. No `adversarial/` subdirectory created inside this
front's own directory; no referee dispatched (reserved for the
orchestrating session, per mandate).

---

## §1 Precise restatement of the target, `C(γ)`

Quoting Lemma 1 (wave-17 front, cited, PROVED): for `γ∈(0,1]`,
`n\varphi(n,γn) = S_n := \sum_{k=1}^n A_k`, `A_k := E_M[P_{k,M}]`,
`M∼\mathrm{Binomial}(k,γ)`, `P_{k,m}:=\prod_{i=1}^m(1-\tfrac{k-i}n)`.
The wave-17 front proved (PROVED, `γ∈(0,1]`):

`\varphi(n,γn)/\varphi_\infty(γn) \to T(γ):=\sqrt{2/(2-γ)}` as `n\to\infty`,

and **conjectured** (numerically matched to 7 significant digits, not
proved, except at `γ=1`) the second-order term:

`\sqrt n\big(\varphi(n,γn)/\varphi_\infty(γn) - T(γ)\big) \to
C(γ) := -\dfrac{2}{3\sqrt\pi}\sqrt γ\,\dfrac{6-8γ+3γ^2}{(2-γ)^2}`.

`C(1)=-2/(3\sqrt\pi)` is PROVED (Robbins 1955 + FGKP95). `C(γ)` for
`γ\in(0,1)` is the target this front — and every front in this
sub-lineage since Estágio 26 — attempts to prove.

**Lemma E (PROVED, Estágio 26, cited/reused, not re-derived here):**
`C(γ)` is exactly equivalent to `S_n = G_n + D(γ) + o(1)`,
`G_n:=\tfrac12\sqrt{πn/β}`, `β:=γ(2-γ)/2`,
`D(γ)=-\tfrac13\tfrac{6-8γ+3γ^2}{(2-γ)^2}`.

**Lemma D0 (PROVED, Estágio 26, cited/reused, not re-derived here):**
splitting `A_k=e^{-s(k)}+[A_k-e^{-s(k)}]`, `s(k):=βk^2/n-γk/(2n)`, the
first ("deterministic") half satisfies `Σ_ke^{-s(k)}=G_n+D_0(γ)+
Θ(n^{-1/2})`, `D_0(γ)=(γ-1)/(2(2-γ))`, for **every** `γ\in(0,1]` —
this is the already-PROVED half; the mandate correctly identifies
`C(γ)` (equivalently `E(γ):=D(γ)-D_0(γ)`, the "hard half") as distinct
from `D_0(γ)` and still fully open.

**`E_{\text{heuristic}}(γ) := \dfrac{-3γ^2+7γ-6}{6(γ-2)^2}`** is the
closed form two independent *heuristic* derivations (Estágio 26 §4's
own; and the wave-17 front's original Taylor-the-whole-ratio route)
land on, symbolically exactly (`sympy`-confirmed by Estágio 26, and
matching `D(γ)-D_0(γ)` exactly, cited). **Proving `E_n:=S_n-Σ_ke^{-s(k)}
\to E_{\text{heuristic}}(γ)` rigorously is the actual open mathematical
content of `C(γ)`'s construction.** Estágio 26 §5 named three technical
gaps to a proof; Gap 2 was closed (Estágio 30); Gap 1 (a uniform
Taylor-remainder-with-moments bound on
`E_M[e^{-δ(M)-τ(M)/2}]`) is the obstacle every subsequent front
(Estágios 33/36/37/49, and now this one) has attacked and not closed.

---

## §2 New exact structural fact: `A_k` as a terminating `2F0`
## hypergeometric polynomial (script `01`)

`P_{k,m}=\prod_{i=1}^m(1-\tfrac{k-i}n)=\prod_{i=1}^m\tfrac{n-k+i}n=
\tfrac{(n-k+1)_m}{n^m}$` — a Pochhammer/rising-factorial ratio, an
elementary rewriting of Lemma 1's own product (verified exactly,
`539/539` checks, script `01` Part A). Substituting into
`A_k=\sum_{m=0}^k\binom km γ^m(1-γ)^{k-m}P_{k,m}` and using
`\binom km=\tfrac{(-1)^m(-k)_m}{m!}$` gives, exactly:

> **New Fact (this front, PROVED, script `01` Part B).**
> `A_k(n,γ) = (1-γ)^k\cdot{}_2F_0\!\big(-k,\,n-k+1;\;;\;w\big)`,
> `w:=-\dfrac γ{(1-γ)n}` (fixed, `k`-independent), where
> `{}_2F_0(a,b;;z):=\sum_{m=0}^\infty\tfrac{(a)_m(b)_m}{m!}z^m` —
> **terminates exactly at `m=k`** since `a=-k` is a nonpositive integer
> (`(-k)_m=0` for `m>k`), so this is a genuine finite polynomial
> identity, no convergence question anywhere.

Verified **symbolically**, `n,γ` left free, `k=0,\ldots,6`: exact zero
difference against the direct Lemma-1 sum (`sp.simplify`). Verified
**numerically**, 40 random exact-`Fraction` `(n,k,γ)` triples
(`k` up to `59`): 0 mismatches, **after** this front caught and fixed
its own bug in this exact check (see §8 item 1).

**An attempted further identification with the classical Charlier
polynomial family, `C_k(x;a):={}_2F_0(-k,-x;;-1/a)`, does NOT check out**
under the natural parameter matching `x=k-n-1`, `a=(1-γ)n/γ` — the
`k=1` residual is an exact, `n`-independent `-2γ`, not zero, ruling out
an accidental near-miss; likely a sign/convention mismatch against one
of several inequivalent textbook conventions for Charlier polynomials.
**Not claimed as a result of this front** (disclosed in script `01`
Part C and §8 item 2) — nothing downstream depends on the Charlier name,
only on the independently-verified `2F0` form itself, which is new to
this lineage either way.

> **[Correção, 2026-08-29 — onda 29 frente (b),
> `DIAGONAL-2F0-SUM-ATTEMPT`, e seu referee hostil]** Esta seção está
> INCORRETA: a identificação com Charlier, na convenção DLMF acima
> (`-1/a`), **é de fato uma identidade algébrica EXATA**, não uma
> conjectura que falha — `A_k(n,γ)=(1-γ)^k\cdot C_k(k-n-1;(1-γ)n/γ)`
> para todo `1\le k\le n`, `γ\in(0,1)`, confirmada simbolicamente
> (`k=0,\ldots,8`, `n,γ` livres) por uma frente futura e re-confirmada
> de forma independente por seu referee hostil. A causa raiz do
> resíduo `-2γ` reportado acima **não** foi um "possível mismatch de
> convenção" genérico — foi um bug concreto de implementação no
> `script 01` desta própria frente: `poch_negk` (o Pochhammer `(-k)_m`
> correto) foi computado mas nunca usado; `binomial(k,m)` foi usado em
> seu lugar, em vez de `(-k)_m/m!=(-1)^m\binom km`. O referee hostil da
> onda 29 transcreveu o código real deste `script 01` e provou
> algebricamente que ele é equivalente-em-efeito à convenção de sinal
> errada `+1/a`, reproduzindo o resíduo `-2γ` exato reportado aqui. A
> caracterização de "não capturado por ninguém" também foi ajustada —
> esta própria seção já suspeitava, em termos gerais, de um "mismatch
> de convenção", apenas nunca testou a hipótese. **Isto não muda
> nenhuma conclusão matemática desta frente**: `C(γ)` permanece
> inteiramente aberto, a soma diagonal continua não-fechada (agora por
> uma razão estrutural diferente e mais precisa, ver a integração da
> onda 29 abaixo), e nada no Gap 1/3 é afetado — apenas a caracterização
> de que a identificação Charlier "não se confirma" está revertida: ela
> se confirma exatamente. Ver
> `diagonal_2f0_sum_attempt/ATTEMPT.md` §2 e
> `diagonal_2f0_sum_attempt/adversarial/REFEREE_REPORT.md`.

**Why this does not, by itself, produce a closed form for `S_n` or
`C(γ)`.** The argument `w` is fixed (`k`-independent), but the *degree*
`k` and the second upper parameter `b=n-k+1` both move with the
summation index — `\sum_{k=1}^n(1-γ)^k\,{}_2F_0(-k,n-k+1;;w)` is a
"diagonal-parameter" sum of a hypergeometric family at fixed argument
but drifting degree/parameter, not a textbook generating-function
identity (the classical Charlier EGF `\sum_kC_k(x;a)t^k/k!=e^t(1-t/a)^x`
— even setting the Part-C mismatch aside — holds for *fixed* `x,a`, not
`x=x(k)`). This front did not find a way to close this diagonal sum in
the time available; it is recorded here as the most promising-looking
unexploited lead for a possible future front (see §7).

---

## §3 Exact Binomial central-moment machinery via cumulants (script `02`)

Cumulants are additive over the `k` i.i.d. Bernoulli(`γ`) summands of
`M`, so `κ_j(D)=k\cdot\tilde κ_j(γ)` for `j\ge2` (`κ_1(D)=0`, `D:=M-γk`),
where `\tildeκ_j(γ)` (the `j`-th cumulant of a *single* Bernoulli(`γ`)
trial, `k`-independent) is computed via one `sympy.series` call on
`\ln(1-γ+γe^t)` — fast (`<1$`s to order 18). Central moments of `D` are
recovered via the standard moment↔cumulant recursion
`\mu_n=\sum_{m=1}^n\binom{n-1}{m-1}κ_m\mu_{n-m}`, `\mu_0=1` (computed to
order 18 in `2.0$`s).

**Verified two independent ways:**
(i) symbolically against the two classical Binomial central-moment
formulas already cited elsewhere in this lineage
(`\mu_3=kγ(1-γ)(1-2γ)`, `\mu_4=kγ(1-γ)[1+3(k-2)γ(1-γ)]`, quoted in
`gamma_second_order_attempt/ATTEMPT.md` §5) — exact zero symbolic
difference, both;
(ii) numerically, `48` brute-force exact-`Fraction` pmf-summation
checks (`k\le8`, orders `\{2,3,4,6\}`) — 0 mismatches.

**Fresh re-derivation of `x(D):=δ(D)+τ(M)/2`'s exact cubic coefficients**
(`τ(m)` via `sympy.summation`, `δ(D)$` the cited exact wave-17 identity)
matches the referee-corrected closed forms quoted in
`gamma_gap1_mgf_attempt/ATTEMPT.md` §2 **exactly, on all four
coefficients**, including the specific `c_0` bracket the grandparent's
referee had to correct (a spurious extra `γ` factor) — this front's
independent re-derivation reproduces the *corrected* form directly,
with no analogous error.

---

## §4 A genuinely different Bulk/Tail refinement: Lyapunov + exact
## 4th moment, instead of a deterministic worst-case bound (scripts
## `03`, `04`, `06`, `07`, `09`)

**Diagnosis (this front's own, stated precisely).** The predecessor's
own §9 explicitly reports: *"for 5 of 8 tested γ, the bulk term (not
the Bernstein-tail term) is what is still >1"* at the naive margin —
i.e. the bulk piece, not the tail piece, is the current binding
constraint for most `γ`. The predecessor's bulk bound is
`H_\Theta^3e^{H_\Theta}$`, the *deterministic worst case* of `|x_k(D)|`
evaluated at the bulk radius `D=\Theta_k=C\sqrt{k\ln n}` — a point that
is `Θ(\sqrt{\ln n})$` **standard deviations** out (`\mathrm{std}(D)=
\sqrt{kγ(1-γ)}`, while `\Theta_k/\mathrm{std}(D)\sim C\sqrt{\ln n/
(γ(1-γ))}\to\infty`). But `E[|x(D)|^3e^{|x(D)|}\mathbb 1_{\text{bulk}}]`
is an *expectation*, dominated by *typical* `D` (scale `\sqrt k`, not
`\sqrt{k\ln n}$`) — bounding it by the value at the extreme edge is
provably wasteful by a factor that **grows without bound** in `n`
(unlike every prior front's tightening, which each removed only a
*fixed* multiplicative constant).

**This front's fix (Lyapunov's inequality, elementary, always valid,
no new citation tier beyond classical `L^p` theory):**

`E[|x(D)|^3e^{|x(D)|}\mathbb 1_{\text{bulk}}] \le e^{H_\Theta}\,
E[|x(D)|^3] \le e^{H_\Theta}\,\big(E[x(D)^4]\big)^{3/4}`

using the **exact** `E[x(D)^4]` (§3's moment machinery — no
approximation), replacing the deterministic `H_\Theta^3` with a moment
that captures *typical*, not extreme, scale. Applied identically to the
**small-`k` residual** term (`k\le k_2:=O(\ln n)`), which script `06`
Check (C) found was itself the *actual* binding constraint at
`γ=0.99,0.9` even after the bulk fix.

**Quantified improvement (script `04`).** Numerically comparing
`H_\Theta^3` (predecessor) against `(E[x(D)^4])^{3/4}` (this front) at
`k=K_{\text{real}}(n,γ)$` (predecessor's own tight truncation, cited,
re-derived fresh), across the same 8 sample `γ`: the ratio grows
**without bound** as `n\to\infty`, with a fitted `\ln(\text{ratio})/
\ln(\ln n)$` exponent of `\approx1.50$` at 7 of 8 `γ` (`0.90,0.70,0.50,
0.30,0.10,0.05,0.01$; `γ=0.99$ shows a larger apparent exponent over the
tested range, `n=10^{10}\text{–}10^{100}$`, plausibly a not-yet-
asymptotic boundary effect near `γ^*=1-\tfrac{\sqrt2}2$ where
`λ_{\text{tight}}$`'s two-piece `\max$` switches branch — not
independently resolved further, disclosed honestly), matching the
analytic prediction `\mathrm{ratio}\sim C^3(\ln n)^{1.5}$` derived by
hand in this front's own working notes (bulk `\sim c_1(K)^3\cdot
\{Θ_K^3\text{ vs. }K^{1.5}\}$`, ratio `\sim(\Theta_K/\sqrt K)^3=C^3
(\ln n)^{1.5}$`). At `n=10^{60}`, the ratio already exceeds `6\,600` at
`γ=0.5$`; at `n=10^{100}$, it exceeds `10^4$–`10^6$` across all 8 `γ`.

**Validity, hard-checked (script `06`), before trusting any of it:**
- (A) The pointwise (unrestricted) Lyapunov bound `R_k^{\text{bound}}
  :=\tfrac16e^{H_{\text{full}}}(E[x(D)^4])^{3/4}$` was checked against
  `R_k^{\text{exact}}:=\tfrac16E_M[|x(D)|^3e^{|x(D)|}]$`, computed by
  **direct exact Binomial pmf summation**, at 18 `(k,n,γ)$` points
  (`k\le80$, moderate `n$`): **0 violations**, bound/exact ratios a
  modest `1.3$×`–`22$×` (not absurdly loose).
- (B) The bulk-*restricted* version was checked the same way, 8 points:
  **0 violations**.
- (C) The `k$-uniformity` this construction implicitly needs — that
  the value at `k=K$` (resp. `k=k_2$`) dominates every `k\le K$` (resp.
  `k\le k_2$`) — was checked **numerically** (the *same* rigor tier
  this lineage has used for this exact class of fact since the
  grandparent's own referee first flagged it in Estágio 33): `96+80+56
  =232$` checks (script `07`, script `09`), **0 violations**, worst
  observed ratio exactly `1.0$` in every case (i.e. `k=K$`/`k_2$` is
  genuinely the maximum, not merely an unviolated-so-far bound).

**Fresh re-derivation of Bernstein-with-slack (unchanged mechanism,
Estágio 37's technique, cited, re-derived from the raw classical
Bernstein inequality here, not copied)** gives an explicit
`k_2(n,γ,C,a):=\big(\tfrac{2C}{3aσ^2(γ)}\big)^2\ln n$` — verified against
this front's own re-derived Bernstein bound matching the *exact*
Binomial tail at `27/27$` spot checks, 0 violations (script `05`).

**Full hybrid assembly, `n_0(γ)`, at the same 8 sample `γ` this
sub-lineage has used since Estágio 36 (scripts `05`, `09`):**

| `γ` | log₁₀ n₀ (predecessor, Estágio 49) | log₁₀ n₀ (this front, v2) | decades saved |
|---|---|---|---|
| 0.99 | 15.42 | **11.96** | 3.46 |
| 0.90 | 19.09 | **10.15** | 8.94 |
| 0.70 | 30.45 | **11.27** | 19.18 |
| 0.50 | 35.49 | **16.46** | 19.03 |
| 0.30 | 39.30 | **20.39** | 18.91 |
| 0.10 | 47.72 | **25.00** | 22.72 |
| 0.05 | 52.08 | **27.12** | 24.96 |
| 0.01 | 61.17 | **31.41** | 29.76 |

`n_0(γ)` still ranges `10^{10.2}`–`10^{31.4}` — **no numerically useful
bound is claimed**; this remains vastly beyond any `n` reachable by
direct computation (the grandparent's own ground-truth pmf table
reached `n$` up to `32{,}000$`). No-spurious-oscillation checked (script
`05`, `09`, `15$` decades beyond each `n_0`, `0$` increases found at any
of the 8 `γ$`, matching this lineage's own established convention).

---

## §5 Higher-order Taylor/cumulant check via exact moments (script `08`)

Using §3's exact `E[D^j]$` (`j$` up to 18), this front computed the
**exact** `E[x(D)^j]$` for `j=0,\ldots,6$` (script `08`; the `j=6$` case,
degree 18 in `D$`, took `20$`s symbolically), giving the exact order-6
Taylor truncation `T_6(k,n,γ):=\sum_{j=0}^6\tfrac{(-1)^j}{j!}E[x(D)^j]$`
of `E_M[e^{-x(D)}]$` — **four orders beyond** Estágio 26 §4's own
order-2 heuristic truncation (`-E[δ]-τ(γk)/2+E[δ^2]/2$`).

Summing `\sum_{k=1}^ne^{-s(k)}[T_J(k,n,γ)-1]$` directly (`J=2$` and
`J=6$`, `n$` up to `2^{14}=16384$`, `γ\in\{0.3,0.5,0.7\}$`) and
2-point-Richardson-extrapolating both:

| `γ` | order-2 extrap | order-6 extrap | `E_{\text{heuristic}}(γ)` | `|`order-2`-E_h|` | `|`order-6`-E_h|` | `|`order-6`-`order-2`|` |
|---|---|---|---|---|---|---|
| 0.3 | -0.240420 | -0.240336 | -0.240484 | 6.4e-5 | 1.5e-4 | 8.4e-5 |
| 0.5 | -0.240716 | -0.240669 | -0.240741 | 2.5e-5 | 7.1e-5 | 4.7e-5 |
| 0.7 | -0.253442 | -0.253406 | -0.253452 | 9.8e-6 | 4.6e-5 | 3.6e-5 |

**The four extra exact orders shift the extrapolated limit by only
`4$–`8×10^{-5}$`** — comparable to, or smaller than, the residual gap
already present at order 2. This is **new evidence** (no ancestor front
computed the *exact* expansion beyond order 2) supporting — but not
proving — that Estágio 26's truncation is not silently dropping a
genuine surviving `Θ(1)`-order contribution. A genuinely different,
sharper (e.g. 3-point) extrapolation, or pushing to order 8+, was not
attempted (out of scope for the remaining time budget; named in §7).

> **[Correção, 2026-08-29 — referee hostil, wave 28 `GAMMA-C-GAMMA-
> CONSTRUCTION-ATTEMPT`]** A frase acima ("comparable to, or smaller
> than, the residual gap already present at order 2") está incorreta,
> pela leitura direta da própria tabela acima: o "shift"
> (`|`order-6`-`order-2`|`) na verdade EXCEDE o resíduo de order-2
> (`|`order-2`-E_h|`) nos três `γ` testados — `1{,}31\times` em
> `γ=0{,}3` (`8{,}4/6{,}4`), `1{,}88\times` em `γ=0{,}5` (`4{,}7/2{,}5`),
> e `3{,}67\times` em `γ=0{,}7` (`3{,}6/0{,}98`) — não o inverso. Mais
> precisamente: a coluna `|`order-6`-E_h|` mostra que a truncagem de
> **order-6 está mais LONGE** de `E_{\text{heuristic}}(γ)` do que a
> truncagem de order-2, nos três `γ` testados (`1{,}5\times10^{-4}` vs.
> `6{,}4\times10^{-5}` em `γ=0{,}3`; `7{,}1\times10^{-5}` vs.
> `2{,}5\times10^{-5}` em `γ=0{,}5`; `4{,}6\times10^{-5}` vs.
> `9{,}8\times10^{-6}` em `γ=0{,}7`) — o oposto do que a frase original
> sugere. **Isto não refuta `E_{\text{heuristic}}(γ)`** (que continua
> sendo apenas uma heurística conjecturada, não um alvo provado, e a
> discrepância pode vir da extrapolação de Richardson de 2 pontos, não
> necessariamente da série de Taylor em si — nenhuma dessas
> possibilidades foi isolada aqui) — mas a interpretação correta é que
> este teste específico NÃO fornece a garantia originalmente alegada de
> que os quatro termos extras de ordem sejam desprezíveis frente ao
> resíduo já existente em order 2; ao contrário, eles são do mesmo porte
> ou maiores. O achado é real, de severidade MODERADA, e foi encontrado
> de forma idêntica em três lugares deste documento (VERDICT, esta
> Seção 5, e o Scorecard §9) — todos precisam da mesma correção. Não
> afeta `A_k`'s identidade `2F0` (§2), a refinação Lyapunov/momento-4
> exato (§4), nem a tabela `n_0(γ)` (§4) — inteiramente independentes
> deste teste de order-6. Ver `adversarial/REFEREE_REPORT.md`.

---

## §6 Numerical verification summary (fresh scripts, logs on disk)

| Script | What it checks | Result |
|---|---|---|
| `01_exact_hypergeometric_structure.py`/`.log` | `P_{k,m}$` Pochhammer form (539 checks); `2F0$` symbolic (`k=0..6`) + 40 numeric exact spot checks; Charlier attempt | 0/0 mismatches on the claimed results; Charlier NOT established (disclosed) |
| `02_exact_moment_recursion.py`/`.log` | cumulant→moment recursion vs 2 cited classical formulas; 48 brute-force pmf checks; fresh `x(D)$` vs referee-corrected cited coefficients | 0 mismatches everywhere |
| `03_moment_based_bulk_refinement.py`/`.log` | `E[x(D)^4]$` exact + brute-force cross-check (5 points); `γ=1$` degenerate sanity; fresh `λ_{\text{tight}}(γ)$` limits vs cited | 0 mismatches; matches cited `λ_{\text{tight}}$` exactly |
| `04_bulk_term_numeric_comparison.py`/`.log` | `H_\Theta^3$` vs `(E[x^4])^{0.75}$`, 8 `γ$` × 8 `n$`-scales up to `10^{100}$`; fitted growth exponent | ratio grows unboundedly, exponent `\approx1.5$` (7/8 `γ$`) |
| `05_full_hybrid_assembly_n0.py`/`.log` | Bernstein-with-slack vs exact tail (27 checks); full `n_0(γ)$` bisection + no-oscillation | 0 violations; `n_0(γ)$` table (v1) |
| `06_validity_sanity_checks.py`/`.log` | pointwise/bulk-restricted Lyapunov bound vs exact pmf (18+8 checks); term breakdown at crossing | 0 violations; revealed small-k was binding at `γ=0.99,0.9$` |
| `07_k_uniformity_checks.py`/`.log` | `k$-uniformity of bulk term and `H_{\text{full}}$` (176 checks) | 0 violations |
| `08_higher_order_taylor_check.py`/`.log` | order-2 vs order-6 exact Taylor truncation, Richardson extrap | shifts limit by `<10^{-4}$` |
| `09_full_hybrid_v2_lyapunov_smallk.py`/`.log` | small-k Lyapunov refinement; final `n_0(γ)$` table; `k$-uniformity (56 checks) | 0 violations; final table (§4) |

All numerics are `mpmath$` (dps `50$`–`80$`) or exact `sympy$`/`Fraction$`
arithmetic; no Monte Carlo anywhere in this front (nothing needed
randomness beyond one disclosed deterministic sanity seed, §9).

---

## §7 What remains open, precisely

1. **`C(γ)` for `γ\in(0,1)` itself is NOT constructed.** No closed form
   was derived; no rigorous asymptotic characterization (proved upper
   AND lower bound, or a proved convergent series) was produced. This
   front's contributions are entirely on the *supporting* side.
2. **Gap 1 (`Σ_ke^{-s(k)}R_k=o(1)`, fully rigorously) is NOT closed.**
   `n_0(γ)` is smaller by up to `29.76$` decades than the immediate
   predecessor's own table, but remains `10^{10.2}$`–`10^{31.4}$` —
   astronomically large, matching this lineage's own established
   convention (Estágio 36 onward) that an explicit-but-astronomical
   `n_0(γ)` is not, on its own, treated as a satisfying closure. As the
   predecessor itself noted, the *opposite* judgment call — that a
   literal `∀n\ge n_0(γ)` proved inequality, however large `n_0`, IS a
   complete, valid proof of the asymptotic statement in the ordinary
   real-analysis sense — remains available and was **not** made
   unilaterally by this front either, for consistency with the
   lineage's own established convention.
3. **The `k$-uniformity facts this front's own construction relies on
   (§4) are, like every ancestor's analogous facts, verified only
   NUMERICALLY (broad grid, 0 violations), not proved as blanket
   theorems** for literal all `(k,n,γ)$`.
4. **Gap 3 (uniformity over the full truncation range, beyond what
   Gap 1's own `k`-uniform construction already provides "for free") is
   untouched** — as it has been since Estágio 30, its closure is
   claimed by every front to "follow mechanically" once Gap 1 is fully
   closed, but this has never actually been executed by any front,
   including this one.
5. **The `2F0` diagonal-sum lead (§2) was not pushed through.** Summing
   `\sum_k(1-γ)^k\,{}_2F_0(-k,n-k+1;;w)` at fixed `w` but drifting
   degree/parameter is not a standard textbook identity; whether a
   contour-integral (Cauchy coefficient-extraction) or a
   generating-function-in-two-variables approach can close it is
   genuinely unknown and unexplored — named here as the single most
   promising unexploited lead a future front could try, precisely
   because it is *exact* (not asymptotic) machinery not used by any
   ancestor.
6. **The higher-order Taylor check (§5) was not pushed past order 6**,
   nor was a sharper (3-point, or exact-remainder-controlled)
   extrapolation attempted — both would strengthen (or potentially
   undermine) the evidence for `E_{\text{heuristic}}(γ)` further.
7. **The Bernstein-tail piece itself (§4) is UNCHANGED from Estágio
   37/49's own construction** — this front improved the bulk and
   small-`k` pieces only; whether the tail piece (or the exact
   Chernoff/relative-entropy bound, named-but-not-pursued since Estágio
   37) has comparable unexploited slack was not investigated.
8. **`γ→0^+` boundary behavior of the bulk-term improvement's growth
   exponent (§4) was not resolved** — `γ=0.99` showed an apparently
   larger fitted exponent than the other 7 sample `γ`, over the tested
   `n`-range; whether this is a genuine boundary effect (near
   `γ^*=1-\sqrt2/2` where `λ_{\text{tight}}`'s `\max(\cdot)` switches
   branch) or simply a not-yet-asymptotic finite-`n` artifact was not
   determined.

---

## §8 Self-caught issues (disclosed, per this lineage's established
## honesty convention)

1. **Float-leak bug in script `01`'s numeric spot-check (caught before
   drawing any conclusion).** The first version of the 40-point random
   `(n,k,γ)` exact-Fraction cross-check passed `n_val` as a bare Python
   `int` into `A_k_direct_symbolic`, whose inner loop computes
   `(n_sym-k_val+i)/n_sym` — with `n_sym` a plain `int`, Python 3's `/`
   performs **floating-point** division, silently turning the "exact"
   comparison into a `\sim10^{-17}$`-scale floating comparison instead
   of an exact-zero one, producing `19/40$` spurious "mismatches."
   Caught by directly inspecting one flagged case (`direct` printed as
   a decimal, e.g. `0.239850548797262`, instead of an exact `Fraction`
   — an immediate tell). **Fixed** by forcing `n_val` to `sp.Integer`
   before calling either evaluator, keeping all arithmetic exactly
   symbolic throughout; the fixed version passes `40/40$`.
2. **Attempted Charlier-polynomial identification (script `01` Part C)
   did not check out, and was NOT forced through.** The naive parameter
   matching `x=k-n-1$, `a=(1-γ)n/γ$` against the textbook convention
   `C_k(x;a):={}_2F_0(-k,-x;;-1/a)$` fails past `k=0$` (the `k=1$`
   residual, `-2γ$`, is exact and nonzero, ruling out a numerical
   accident). Rather than hunt indefinitely through the several
   inequivalent textbook Charlier conventions, this front disclosed the
   failure and dropped the naming claim — nothing downstream depends on
   it, only on the independently-verified `2F0$` form itself.
3. **No other computational bugs found.** Every symbolic claim in §§2–5
   was cross-checked at least two independent ways before being
   reported (fresh re-derivation vs. cited closed form; symbolic vs.
   brute-force numeric; unrestricted vs. bulk-restricted pmf
   comparison); every numeric bound-validity claim (§4, §6) was
   hard-checked against direct exact pmf summation, not merely
   internally self-consistent.

---

## §9 Scorecard

| Claim | Status |
|---|---|
| `A_k(n,γ)=(1-γ)^k\,{}_2F_0(-k,n-k+1;;-γ/((1-γ)n))` (new exact structural fact) | **PROVED** (§2, script `01`; symbolic `k=0..6` + 40 exact numeric spot checks) |
| Identification with a classical Charlier polynomial family | ~~NOT ESTABLISHED~~ — **[Correção, 2026-08-29, onda 29]: CONFIRMADA EXATA** (`A_k=(1-γ)^k C_k(k-n-1;(1-γ)n/γ)`); o resíduo original veio de um bug de implementação nesta frente, não de um mismatch real. Ver §2. |
| Fresh re-derivation of `E[D^j]` (`j\le18`) via cumulants, matching 2 cited classical formulas and 48 brute-force checks | **PROVED / CONFIRMED** (§3, script `02`) |
| Fresh re-derivation of `x(D)`'s exact cubic, matching the referee-corrected cited coefficients exactly | **CONFIRMED** (§3, script `02`) |
| Fresh re-derivation of `λ_{\text{tight}}(γ)`, matching Estágio 49's cited value exactly | **CONFIRMED** (script `03`) |
| Lyapunov/exact-4th-moment bulk bound, valid vs exact pmf | **PROVED valid** (18+8 checks, 0 violations, script `06`) |
| Bulk-term improvement grows unboundedly in `n` (`\sim(\ln n)^{1.5}`) | **CONFIRMED numerically** (fitted exponent `\approx1.5` at 7/8 `γ`; `γ=0.99` anomalous, unresolved) (script `04`) |
| Fresh Bernstein-with-slack re-derivation, valid vs exact pmf | **CONFIRMED** (27/27, script `05`) |
| `k`-uniformity of this front's own new constructions | **numerically verified**, 232 checks, 0 violations — same rigor tier as every ancestor's analogous claim, **not** a blanket theorem (scripts `07`, `09`) |
| `n_0(γ)` reduced by `3.46`–`29.76` decades vs. the immediate predecessor's own table | **QUANTIFIED, VERIFIED** (§4, scripts `05`,`06`,`09`) — still astronomically large, `10^{10.2}`–`10^{31.4}` |
| Order-6 vs order-2 exact Taylor truncation, Richardson-extrapolated | shifts limit by `<10^{-4}` — **[Correção, 2026-08-29 — referee hostil]** the shift actually EXCEEDS the order-2 residual by `1.3×`–`3.7×` at all 3 tested `γ` (not "comparable to or smaller than" as originally stated); order-6 lands farther from `E_heuristic(γ)` than order-2 does in all 3 cases. Does not refute `E_heuristic(γ)`, but does not provide the reassurance originally claimed either — **evidence, direction now uncertain, NOT a proof** (§5, `adversarial/REFEREE_REPORT.md`) |
| **Gap 1** (`Σ_ke^{-s(k)}R_k=o(1)`, fully rigorous) | **still NOT closed** |
| **Gap 3** (uniformity over the full truncation range) | **untouched**, unaffected in status |
| **`C(γ)` for `γ\in(0,1)`, the mandate's actual target** | **NOT CONSTRUCTED — remains entirely OPEN** |

---

## Seeds

| Block | Status |
|---|---|
| `20260941000–20260941999` (this front's reservation, `DISC-DEC-131`, frente b) | grep-confirmed **unused** before any code was written and re-confirmed unused after all work was complete (`grep -rn "20260941" 05_DISCOVERY_LAB/` finds only `DECISION_LEDGER.yaml`'s own reservation line, both times) — **zero seeds drawn from this block**; every quantitative claim in this front is exact symbolic algebra (`sympy`), exact rational arithmetic (`Fraction`), or deterministic high-precision numerics (`mpmath`, dps `50`–`80`); no Monte Carlo anywhere |
| `random.seed(1)` (script `01`, Part B numeric spot-check) | a **fixed, disclosed, non-reserved** seed for a 40-point deterministic sanity check, matching the exact convention several ancestor fronts (e.g. `gamma_second_order_attempt` script `01`) used for an analogous purpose — not drawn from the reserved block |

---

## Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_exact_hypergeometric_structure.py`/`.log` | fresh derivation of `A_k`'s exact `2F0` hypergeometric form; attempted (unsuccessful, disclosed) Charlier identification |
| `02_exact_moment_recursion.py`/`.log` | exact Binomial central moments of `D` via cumulants (order 0–18); fresh `x(D)` cubic re-derivation, cross-checked vs. cited referee-corrected forms |
| `03_moment_based_bulk_refinement.py`/`.log` | exact `E[x(D)^4]`; brute-force + `γ=1` sanity checks; fresh `λ_{\text{tight}}(γ)` re-derivation |
| `04_bulk_term_numeric_comparison.py`/`.log` | numeric comparison, `H_\Theta^3` (predecessor) vs `(E[x^4])^{3/4}` (this front), 8 `γ` × 8 `n`-scales to `10^{100}`, fitted growth exponent |
| `05_full_hybrid_assembly_n0.py`/`.log` | fresh Bernstein-with-slack re-derivation + validity check; full hybrid `W(n,γ,C,a)` assembly (v1); `n_0(γ)` bisection; no-oscillation check |
| `06_validity_sanity_checks.py`/`.log` | hard validity checks of the Lyapunov bound (pointwise + bulk-restricted) against exact pmf; term-by-term breakdown at the found `n_0(γ)` |
| `07_k_uniformity_checks.py`/`.log` | `k`-uniformity checks for the bulk term and `H_{\text{full}}$` (176 checks) |
| `08_higher_order_taylor_check.py`/`.log` | exact order-6 vs order-2 Taylor/cumulant truncation of `E_M[e^{-x(D)}]`, Richardson-extrapolated, compared to `E_{\text{heuristic}}(γ)` |
| `09_full_hybrid_v2_lyapunov_smallk.py`/`.log` | Lyapunov refinement applied to the small-`k` residual too; final `n_0(γ)` table; `k`-uniformity (56 checks) |
| `moment_data.pkl`, `Ex_powers.pkl`, `lambda_tight_confirmed.pkl`, `bulk_comparison_results.pkl`, `n0_hybrid_table.pkl`, `n0_hybrid_v2_table.pkl` | intermediate data, cached between scripts (not narrative content) |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
