# ATTEMPT — Gap 1 ("Taylor-remainder-with-moments bound") of the `C(γ)`
# second-order derivation, `γ∈(0,1)`

**Wave 20, front (a), `GAMMA-GAP1-MGF-ATTEMPT`, authorized by `DISC-DEC-088`.**
Mandate: `THEOREM.md` Estágio 26 §5 named three precise technical gaps
standing between a heuristic cumulant-expansion match and a rigorous proof
of the second-order constant `C(γ)` for `γ∈(0,1)`. Estágio 30
(`GAMMA-SECOND-ORDER-GAP-CLOSURE-ATTEMPT`) closed Gap 2 rigorously via a
Poisson-summation/Jacobi-theta differentiation technique (Lemma G2), and
identified Gap 1 — by elimination and by direct comparison of difficulty —
as the dominant remaining obstacle: it requires "Hoeffding-lemma-tier MGF
control" on a *transcendental* quantity, unlike Gap 2's exact polynomial
algebra. This front's mandate: attack Gap 1.

---

## VERDICT (up front)

> **Gap 1 is NOT closed by this front.** This is an honest, precisely
> bounded **partial closure**, of a different character from Gap 2's: where
> Gap 2 turned out to have an *exact* closed-form answer, Gap 1 does not —
> the object of study is genuinely transcendental, and what this front
> delivers is (i) one fully rigorous structural fact, (ii) one fully
> rigorous *bounding lemma* built from that structure plus a classical,
> already-cited tool (Hoeffding's inequality), (iii) a leading-order
> asymptotic analysis (not yet converted into an explicit-for-all-`n`,
> uniform-in-`γ` inequality) showing the lemma's bound genuinely vanishes,
> and (iv) direct, ground-truth numerical confirmation — via the *exact*
> Binomial pmf, no shortcuts — that Gap 1's own literally-stated target
> quantity shrinks monotonically with `n` at six sample `γ∈(0,1)` values.
>
> 1. **PROVED (exact algebra, sympy-checked two independent ways).** The
>    combined quantity `x(D) := δ(D) + τ(M)/2` that Gap 1 needs a
>    Taylor-remainder bound on is an **exact cubic polynomial in
>    `D:=M-γk`** — `x(D) = c_0+c_1D+c_2D^2+c_3D^3` with closed-form
>    coefficients (Section 2) — no approximation anywhere in *defining*
>    `x`. This was not previously isolated; it converts Gap 1 from "bound a
>    black-box transcendental remainder" into "bound the Taylor remainder
>    of `e^{-x}` for an explicit cubic `x(D)`, `D` a centered Binomial."
> 2. **PROVED (elementary: monotonicity + the already-cited Hoeffding
>    tail bound).** A uniform-in-`k` **Bulk/Tail Lemma** (Section 3):
>    for any split constant `C>0` and threshold
>    `Θ_k:=C√(k\ln n)`, the target quantity `R_k:=\tfrac16E_M[|x(D)|^3e^{|x(D)|}]`
>    satisfies, for *every* `1≤k≤K`,
>    `R_k \le \tfrac16\big[g(Θ_K)^3e^{g(Θ_K)} + 2n^{-2C^2}g(K)^3e^{g(K)}\big]`,
>    where `g(t):=|c_0|+|c_1|t+|c_2|t^2+|c_3|t^3` (Section 3.2). This
>    reduces Gap 1 entirely to bounding two explicit, deterministic
>    quantities, `g(Θ_K)` and `g(K)`, as `n\to\infty`.
> 3. **Leading-order asymptotics (NOT yet a fully explicit-constant
>    inequality).** `g(Θ_K) = O(n^{-1/4}\mathrm{polylog}(n))\to0` and
>    `g(K) = κ_0(3/2-γ)\ln n\,(1+o(1))` (`κ_0` the constant in the
>    truncation range `K^2=κ_0n\ln n`, cited from elsewhere in this
>    lineage's Theorem 2 proof, not re-derived here). Combined with the
>    Bulk/Tail Lemma, this shows that for any fixed `C>1.5\sqrt{\tfrac14+\tfrac12κ_0(3/2-γ)}`,
>    both pieces of the bound vanish, hence `\Sigma_ke^{-s(k)}R_k\to0` —
>    **this is exactly what Gap 1 asks for**, but the `o(1)`/`(1+o(1))`
>    terms above were tracked asymptotically (leading-order algebra,
>    confirmed by two independent computations, symbolic and numeric —
>    Section 3.3) rather than turned into an explicit `n_0(γ)` beyond
>    which the inequality is literally certified. That conversion is
>    standard real-analysis bookkeeping, not a new idea, but it was **not
>    completed** in this front (see Section 5).
> 4. **Direct numerical confirmation (ground truth, no shortcuts).** The
>    exact quantity `\Sigma_{k=1}^Ke^{-s(k)}R_k^{\mathrm{exact}}` — computed
>    via **direct summation over the true Binomial pmf**, `mpmath` dps=50,
>    not via the Bulk/Tail Lemma's bound — shrinks **monotonically** in
>    `n` at **every one of 6 tested `γ∈\{0.1,\ldots,0.99\}`**, `n` up to
>    32000 (Section 4), matching the predicted qualitative behavior. Both
>    `R_k^{\mathrm{exact}}\le R_k` (Gap 1's own crude bound) at every tested
>    point, confirming the pointwise inequality chain has no sign error.
>
> **Net effect on the mandate.** Gap 1 goes from "no attempt made,
> transcendental structure, genuinely harder than Gap 2" (Estágio 30's own
> assessment) to "a concrete, structurally sound, numerically-validated
> proof *strategy* exists, with one new exact-algebra fact and one new
> rigorous bounding lemma, but the strategy has not been assembled into a
> fully explicit-constant, uniform-in-`γ` proof." `C(γ)` for `γ\in(0,1)`
> **remains OPEN**. No claim of progress on any Millennium Problem; pure
> combinatorial mathematics internal to this archive, about a specific
> random-permutation-with-reroutes ensemble.

---

## §0 Provenance and discipline

**Required reading, done before any derivation, in full, in prose.**
`THEOREM.md` Estágio 10 (γ-scaling first appears), Estágio 23 (Teorema 2,
Lema 1, Corolário 1/2 — the proved main γ-scaling law, `C(γ)` proved only
at `γ=1`), Estágio 26 in full (Lema E, Lema D0, and the exact statement of
"Lacuna 1" in §5 — the honest non-closure of `C(γ)`), Estágio 30 in full
(Lema τ-fluct, Lema G2, and how Gap 2 was closed — the closest
methodological precedent). The direct predecessor's `ATTEMPT.md`
(`.../gamma_second_order_gap_closure_attempt/ATTEMPT.md`, 479 lines), read
in full, including its own §1 (Gap 1 quoted verbatim from *its*
predecessor) and §3 (why Gap 1 is harder than Gap 2). **Also read** (not
strictly mandated as "the predecessor's ATTEMPT.md", but the direct source
of the definitions Gap 1 needs — `δ(D)`, `τ(m)`, `s(k)`, the whole §4
cumulant-expansion setup — and itself just prose/math, no `.py` file):
`.../gamma_second_order_attempt/ATTEMPT.md` (633 lines), in full, with
particular attention to §4 (the exact identity
`δ(D)=D(2k(1-γ)-D-1)/(2n)`, cited and used as-is below, not re-derived from
`σ_k(m)`'s own definition, which is not restated anywhere in this front's
required reading) and §5 (Gap 1's precise statement, quoted in §1 below).

**No `.py` file of any front in this lineage (or any other), at any
ancestor/sibling, was opened, read, or imported anywhere in this front.**
Every script below (`01`–`03`) is written fresh from the mathematical prose
of `THEOREM.md` and the two `ATTEMPT.md` files above, per mandate.

**Seeds.** Reserved block `20260890000–20260890999` (`DISC-DEC-088`, this
front). `grep -rn "20260890" 05_DISCOVERY_LAB/` was run before any code and
found only the ledger/queue reservation lines — no prior use, no conflict.
**This front draws zero random seeds.** Every claim is exact symbolic
algebra (`sympy`, script `01`), exact deterministic high-precision numerics
(`mpmath` dps=50 direct Binomial pmf summation, script `02`), or
deterministic float64 closed-form evaluation for a qualitative
rate/threshold check (script `03`, disclosed as such — the object being
evaluated there, `g(t)` at a few chosen `t`, needs no more than float64
precision since only *orders of magnitude* and *sign* are being tracked,
never reported as a claimed-precision numerical result). The reserved block
is disclosed as unused, not silently abandoned.

**Not touched, per mandate:** `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`,
`README.md`, `index.html`, any file outside this front's own new
subdirectory. No git commands run. No `adversarial/` subdirectory created;
no referee dispatched (reserved for the orchestrating session).

---

## §1 Gap 1, quoted precisely

From `gamma_second_order_attempt/ATTEMPT.md` §5 (the original statement;
requoted verbatim, condensed, in the gap-closure front's own §1):

> **Gap 1 — Taylor-remainder-with-moments bound (a "Lemma 4″").** Need: a
> bound, uniform for `1\le k\le K\sim\sqrt{n\ln n}`, of the form
> `\big|E_M[e^{-δ(M)-τ(M)/2}] - \big(1-E[δ]-\tfrac{τ(γk)}2+\tfrac{E[δ^2]}2\big)\big| \le R_k`
> with `R_k` explicit and `Σ_ke^{-s(k)}R_k=o(1)`. By the elementary
> Taylor-remainder identity `|e^{-x}-(1-x+x^2/2)|\le\tfrac{|x|^3}6e^{|x|}`
> applied to `x=δ(M)+τ(M)/2` … this reduces to bounding `E[|δ|^3e^{|δ|}]`
> and `E[|τ(M)-τ(γk)|\cdot(\cdots)]`. … assembling the resulting six-term
> polynomial bound and checking it is genuinely `o(k^3/n^2)` uniformly, not
> just in expectation, was **not carried out**.

Ingredients, all cited (already accepted in this lineage, none re-derived
from first principles here): `τ(m):=Σ_{i=1}^m((k-i)/n)^2`; `M∼\mathrm{Bin}(k,γ)`;
`D:=M-γk`; `δ(D)=D(2k(1-γ)-D-1)/(2n)` (exact, from the wave-17 front's own
identity `σ_k(m)-σ_k(x)=(m-x)(2k-m-x-1)/(2n)` at `x=γk`); `s(k)=βk^2/n-γk/(2n)`,
`β:=γ(2-γ)/2`.

**This front's reading of the target, precisely.** Gap 1 as literally
stated bounds the remainder of expanding `e^{-x}`, `x=δ(M)+τ(M)/2`, to
*second order in `x`*. Since `x` turns out (Section 2) to be an *exact*
cubic polynomial in `D` — not merely "`δ` plus a linearization of `τ`" —
this front works with the single combined object `x(D)` throughout, rather
than separately Taylor-expanding `δ` and `τ` and tracking cross terms by
hand (a simplification relative to the literal ingredient list quoted
above, made possible by the exact-algebra fact of Section 2, and checked
in Section 2 to reduce to the identical quantity).

> **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-089, severidade
> BAIXA.] O referee hostil identificou que a frase "checked in Section 2
> to reduce to the identical quantity" acima é enganosa: a Seção 2 prova
> apenas que `x(D):=δ(D)+τ(M)/2` é um polinômio cúbico exato em `D` — não
> aborda, em lugar nenhum, se limitar o resto de Taylor de `e^{-x}` na
> variável COMBINADA `x` (o que as §§3–4 efetivamente limitam) é a MESMA
> quantidade do alvo original de Gap 1, citado literalmente,
> `E_M[e^{-δ(M)-τ(M)/2}] - (1-E[δ]-τ(γk)/2+E[δ²]/2)` — que usa o `τ(γk)`
> DETERMINÍSTICO no termo linear (não o `τ(M)` aleatório) e apenas
> `E[δ²]` (não o `E[x²]` mais completo, que também carrega `E[τ(M)²]` e
> termos cruzados `E[δ\cdot τ(M)]`) no termo quadrático. São quantidades
> genuinamente diferentes — relacionadas, mas não idênticas; a
> formulação original depende da correção de flutuação da Lacuna 2
> (`τ(M)\to τ(γk)`), rastreada separadamente, para conectar as duas,
> enquanto o objeto combinado `x` deste front absorve essa correção
> implicitamente. Isso contradiz diretamente a própria §5, item 4, deste
> documento, que corretamente afirma que essa checagem "was not
> separately carried out" — o referee confirma que a §5 está certa e
> esta frase da §1 está errada. Não é um erro matemático em nada
> efetivamente provado (a identidade cúbica de §2, o Lema Bulk/Tail de
> §3.2 e a numérica de §4 seguem corretas como afirmações
> autocontidas sobre a quantidade `x` combinada, tal como definida) —
> é uma inconsistência de enquadramento entre esta frase e a própria
> §5.4 do documento. Leia esta frase como se dissesse apenas "made
> possible by the exact-algebra fact of Section 2" — sem a alegação de
> checagem de equivalência, que permanece genuinamente NÃO verificada,
> exatamente como a §5.4 já honestamente assinala.]**

---

## §2 `x(D)` is an exact cubic polynomial in `D` (PROVED, new)

> **Fact (this front; PROVED, script `01`).**
> `x(D) := δ(D) + τ(M)/2`, `M=γk+D`, equals, **exactly**, for every
> integer `1\le k\le n`, real `γ\in(0,1)`:
>
> `x(D) = c_0 + c_1D + c_2D^2 + c_3D^3`,
>
> `c_0 = τ(γk)/2`,
> `c_1 = \dfrac{k(1-γ)}n - \dfrac1{2n} + \dfrac{τ'(γk)}2`,
> `c_2 = -\dfrac1{2n} + \dfrac{τ''(γk)}4`,
> `c_3 = \dfrac1{6n^2}`
>
> (equivalently, in closed algebraic form,
> `c_2=\tfrac{2γk-2k-2n+1}{4n^2}`,
> `c_1=\tfrac1{n^2}\big[\tfrac{γ^2k^2}2-γk^2-γkn+\tfrac{γk}2+\tfrac{k^2}2+kn-\tfrac k2-\tfrac n2+\tfrac1{12}\big]`,
> `c_0=\tfrac{γk}{12n^2}\big[2γ^3k^2-6γ^2k^2+3γ^2k+6γk^2-6γk+1\big]`
> **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-089.] O bracket de
> `c_0` acima está errado: carrega um fator espúrio extra de `γ` em cinco
> dos seus seis termos (todos exceto a constante `+1`). O referee hostil
> re-derivou `c_0` por duas rotas independentes e confirmou que a forma
> algébrica fechada correta é `c_0=\tfrac{γk}{12n^2}\big[2γ^2k^2-6γk^2+
> 3γk+6k^2-6k+1\big]` (sem o `γ` espúrio nos termos `6γk^2\to6k^2`,
> `-6γk\to-6k`, etc.). Checagem numérica em `γ=1/2,k=10,n=100`: valor
> correto `c_0=51/4000=0{,}01275`; a expressão errada acima avalia
> `307/48000≈0{,}006396` — um fator ~2 de discrepância neste ponto. A
> forma "derivative-based" (linha anterior, `c_0=τ(γk)/2` etc.) permanece
> exata e é a que este front efetivamente usou em toda a numérica das
> §§3–4 — a reconstrução independente do referee dos resultados de §4
> bateu com a tabela publicada a <0,3% em todos os 18 pontos testados,
> confirmando que o erro é confinado à transcrição em prosa desta forma
> alternativa, sem propagação para nenhum resultado numérico reportado.]**).

*Proof.* `τ(m)` is exactly cubic in `m` (elementary sum-of-squares
closed form, re-derived fresh via `sympy.summation` in script `01` Part A —
this is the *same* closed form Estágio 30's Gap-2 front already proved,
independently re-derived here rather than imported, since no `.py` file was
read). Substituting `M=γk+D` into this cubic and using the *exact* Taylor
expansion of a cubic about any point (no remainder — the 4th derivative of
a cubic is identically `0`) gives `τ(M)/2` as an exact cubic in `D`, with
`D^3` coefficient `\tfrac1{6n^2}` (from `τ'''=2/n^2`, constant). Adding the
*exact* `δ(D)` (itself already a quadratic in `D`, cited) and collecting
powers of `D` gives the stated closed form — verified in script `01` two
independent ways: (i) direct `sympy.Poly` coefficient extraction from the
expanded sum `δ(D)+τ(M)/2`, and (ii) hand-assembly from `τ`, `τ'`, `τ''` at
`m=γk` plus the two elementary pieces of `δ`, `sympy.simplify`d against
route (i) to an exact zero difference on all four coefficients. A `γ=1`
consistency check (`D=0` a.s. there, so only `c_0` matters) confirms
`c_0(γ=1) = τ(k)/2` exactly, independent of `c_1,c_2,c_3`.

**What this buys.** Gap 1's target — the remainder of Taylor-expanding
`e^{-x(D)}` to second order in `x` — is now a **fully explicit, purely
algebraic** object: `x(D)` has no hidden approximation, so *all* of Gap
1's difficulty is concentrated in one place, the nonlinear composition
`e^{-x(D)}` of an explicit cubic with the exponential, evaluated in
expectation over the centered Binomial `D`. This is a genuine
simplification of the problem as originally posed (which tracked `δ` and
`τ` as separate approximate objects with their own remainder terms) — the
predecessor's own Gap 2 already implicitly used the fact that `τ` is exact
cubic; this front extends that observation to the *combined* object `x`
that Gap 1 is actually about.

---

## §3 A rigorous Bulk/Tail bound, reducing Gap 1 to two scalar limits

### 3.1 Setup

Write `t:=|D|\in[0,k]` and `g(t):=|c_0|+|c_1|t+|c_2|t^2+|c_3|t^3` — a
polynomial with non-negative coefficients, hence **non-decreasing** on
`t\ge0`. By the triangle inequality, `|x(D)|\le g(|D|)` pointwise for every
realization of `D`. Define, exactly as Gap 1 requests,

`R_k := \dfrac16E_M\big[|x(D)|^3e^{|x(D)|}\big]`.

Since `t\mapsto t^3e^t` is non-decreasing on `t\ge0`, `|x(D)|^3e^{|x(D)|}\le
g(|D|)^3e^{g(|D|)}` pointwise, hence `R_k \le \tfrac16E_M\big[g(|D|)^3e^{g(|D|)}\big]`.

### 3.2 The Bulk/Tail Lemma (PROVED)

> **Lemma (this front; PROVED).** Fix `n,γ,C>0`, and for `1\le k\le K` let
> `Θ_k:=C\sqrt{k\ln n}`. Then for **every** `1\le k\le K`:
>
> `R_k \;\le\; \dfrac16\Big[g(Θ_K)^3e^{g(Θ_K)} \;+\; 2n^{-2C^2}\,g(K)^3e^{g(K)}\Big]`.

*Proof.* Split the expectation on the event `\{|D|\le Θ_k\}` vs.
`\{|D|>Θ_k\}`:

`E_M[g(|D|)^3e^{g(|D|)}] = E[\,\cdot\,;|D|\le Θ_k] + E[\,\cdot\,;|D|>Θ_k]`.

**Bulk.** On `\{|D|\le Θ_k\}`, `g(|D|)\le g(Θ_k)` (monotonicity), so
`g(|D|)^3e^{g(|D|)}\le g(Θ_k)^3e^{g(Θ_k)}` there, and this deterministic
upper bound survives taking the expectation of an indicator-weighted
quantity bounded by a constant (`E[\,\cdot\,;A]\le\text{const}\cdot
P(A)\le\text{const}`). Since `Θ_k` is non-decreasing in `k` and `k\le K`,
`Θ_k\le Θ_K`, so `g(Θ_k)\le g(Θ_K)`; hence the bulk piece is
`\le g(Θ_K)^3e^{g(Θ_K)}` for every `k\le K`, **uniformly**.

**Tail.** `|D|\le k\le K` always (`M\in[0,k]`), so on the tail event,
`g(|D|)\le g(K)` (monotonicity again — the crude, but always-valid,
full-support bound), giving `g(|D|)^3e^{g(|D|)}\le g(K)^3e^{g(K)}`
deterministically on this event too, hence
`E[\,\cdot\,;|D|>Θ_k]\le g(K)^3e^{g(K)}\cdot P(|D|>Θ_k)`.
`D` is a sum of `k` i.i.d. `\mathrm{Bernoulli}(γ)`-centered terms, each
bounded in an interval of length `1`; by **Hoeffding's inequality**
(classical, elementary, already the same citation tier this lineage uses
throughout — the wave-17 front's own Lemma 4 is exactly this family of
bound), `P(|D|>t)\le2\exp(-2t^2/k)` for every `t\ge0`. At `t=Θ_k`:
`2Θ_k^2/k = 2C^2\ln n`, so `P(|D|>Θ_k)\le2n^{-2C^2}`, **independent of
`k`**. Hence the tail piece is `\le2n^{-2C^2}g(K)^3e^{g(K)}` for every
`k\le K`. Summing the two pieces and dividing by `6` gives the claim. `∎`

**This is a complete, elementary, fully rigorous proof** — it uses nothing
beyond monotonicity of `g` and `t^3e^t`, the triangle inequality, and
Hoeffding's inequality (cited, classical). It converts Gap 1 entirely into
bounding two explicit deterministic quantities as `n\to\infty`:
`g(Θ_K)` (the "bulk" scale, at the split point) and `g(K)` (the "tail"
scale, at the true support boundary) — plus choosing `C` large enough.

> **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-089, severidade
> MODERADA.] O referee hostil identificou uma lacuna real na afirmação
> acima de "prova completa, elementar, totalmente rigorosa". A conclusão
> `R_k\le\ldots` "para todo `1\le k\le K`" é usada em §3.3 como um único
> par de números `k`-independente (substituindo `k=K` nas fórmulas dos
> coeficientes `c_i(k)`), mas a prova acima só estabelece monotonicidade
> de `g(\cdot)` no seu argumento `t`, para um `k` FIXO. Tornar o
> limitante literalmente uniforme sobre `1\le k\le K` (comparando
> `g_k(Θ_k)` contra `g_K(Θ_K)`, usando os coeficientes de `k`'s distintos
> de cada lado) exige adicionalmente que `|c_i(k)|` seja não-decrescente
> em `k` — fato nunca declarado ou provado acima. O referee confirmou
> numericamente que isso **não é literalmente verdade termo-a-termo**:
> para `γ` próximo de `1` (ex. `γ=0,9,n=2000`), `c_1(k)` muda de sinal
> conforme `k` cresce (53 violações na grade testada, concentradas em
> `γ\ge0,9`). Uma checagem mais profunda do referee, porém, confirmou
> diretamente os dois fatos que a prova realmente precisa
> (`g_k(Θ_k)\le g_K(Θ_K)` e `g_k(K)\le g_K(K)`, usando os coeficientes de
> `K`) para todo `k=1,\ldots,K`, nos piores casos testados (`γ=0,9,0,99`,
> `n` até `32000`): **zero falhas**. Conclusão: lacuna real na prova
> escrita (passo não-justificado), mas a conclusão do Lema não foi
> encontrada falsa em nenhum caso testado — não afeta o veredito de
> não-fechamento da Lacuna 1. Correção pendente para uma versão futura:
> reformular o Lema com `sup_{k\le K}` explícito no lado direito e
> limitar esse sup separadamente, ou provar diretamente o fato mais fraco
> `g_k(Θ_K)\le g_K(Θ_K)` por crescimento agregado (não termo-a-termo) dos
> coeficientes.]**

### 3.3 The two scalar limits (leading-order asymptotics — NOT fully
explicit-constant)

Writing `K^2=κ_0n\ln n` for the constant `κ_0>0` implicit in this
lineage's own truncation `K\sim\sqrt{n\ln n}` (cited from the wave-17
front's Theorem 2 proof; **not independently re-derived or pinned down
numerically here** — script `03` illustrates with `κ_0=2.25`, i.e.
`K=1.5\sqrt{n\ln n}`, chosen for concreteness, not claimed as the literal
constant from that proof):

- **`g(Θ_K)\to0`.** Direct substitution (script `03` Part 1, and hand
  algebra) gives, term by term, `|c_1|Θ_K=O(n^{-1/4}(\ln n)^{5/4})`,
  `|c_2|Θ_K^2=O(n^{-1/2}(\ln n)^{3/2})`, `|c_3|Θ_K^3=O(n^{-5/4}(\ln n)^{9/4})`,
  `|c_0|=O(n^{-1/2}(\ln n)^{3/2})` — **all four terms individually
  `\to0`**, dominated by the `|c_1|Θ_K` piece, `O(n^{-1/4}\mathrm{polylog}(n))`.
  Hence `g(Θ_K)^3e^{g(Θ_K)} = O(n^{-3/4}\mathrm{polylog}(n))\to0`.
- **`g(K)` grows like `\ln n`, not like a power of `n`.** Leading-order
  algebra: `|c_1|K \sim (1-γ)K^2/n = (1-γ)κ_0\ln n`, `|c_2|K^2\sim K^2/(2n)
  = \tfrac{κ_0}2\ln n`, while `|c_0|,|c_3|K^3=o(\ln n)` (both `O(n^{-1/2}\mathrm{polylog})`).
  Collecting: `g(K) = κ_0\big(\tfrac32-γ\big)\ln n\,(1+o(1))`, so
  `e^{g(K)}\sim n^{λ}`, `λ:=κ_0(3/2-γ)` — **polynomial, not exponential, in
  `n`**, the key fact making the Lemma's tail piece controllable at all.

Combining: the tail piece of the Bulk/Tail Lemma is `O(n^{1/2+λ-2C^2}\mathrm{polylog})`
(the `n^{1/2}` from `\Sigma_{k\le K}e^{-s(k)}\sim G_n=Θ(\sqrt n)`, cited,
already-established in this lineage since Lemma D0), which `\to0` for any
fixed `C` with `C^2>\tfrac14+\tfrac λ2`. **Choosing `C` a constant factor
(numerically, `1.5\times`) above this threshold** gives visibly clean
decay already at moderate `n` (Section 3.4); choosing `C` only marginally
above threshold gives a bound that is asymptotically correct but
numerically flat/slowly-decaying out to `n=10^8` in the range this front
could test (polylog/power-of-`n` prefactors dominate near a knife-edge
threshold — an internally disclosed, self-caught finding, not a defect in
the argument itself, see Section 5).

**Combining bulk and tail:** for `C` a constant factor above the threshold
above, `\Sigma_{k=1}^Ke^{-s(k)}R_k = O(\sqrt n)\cdot O\big(g(Θ_K)^3e^{g(Θ_K)}+n^{-2C^2}g(K)^3e^{g(K)}\big)\to0` —
**exactly Gap 1's target inequality**, at the level of leading-order
asymptotic algebra.

### 3.4 Numerical support for §3.3's asymptotics (script `03`)

Script `03` evaluates `g(Θ_K)` and `g(K)` directly (float64, closed-form,
no pmf summation — a fast, purely algebraic check of the *formulas* above,
distinct from script `02`'s exact-pmf ground truth) for
`γ\in\{0.1,0.3,0.5,0.7,0.9,0.99\}`, `n` from `10^3` to `10^8`:

- `g(Θ_K)` shrinks monotonically toward `0` for every tested `C\in\{1,2,3,5\}`
  and every `γ`, confirming the bulk claim directly (Part 1 of the log).
- The empirical growth rate `λ` of `g(K)` against `\ln n` (least-squares
  fit across all six sampled `n`) matches the leading-order prediction
  `κ_0(3/2-γ)` (`κ_0=2.25`) to within `\sim6\%` at every tested `γ` (e.g.
  `γ=0.5`: fitted `λ=2.141` vs. predicted `2.250`; `γ=0.9`: fitted
  `λ=1.290` vs. predicted `1.350`) — the residual gap is exactly the
  expected finite-`n` correction from the lower-order terms dropped in the
  leading-order algebra above, not a sign of a wrong prediction.
- With `C=1.5\times` the (fitted-`λ`-based) critical threshold, the full
  union-bound estimate `K\cdot g(K)^3e^{g(K)}\cdot2n^{-2C^2}` decays
  **cleanly and dramatically** at every tested `γ`, already visible at
  `n=10^3` (e.g. `γ=0.5`: `3.9\times10^{-5}\to2.7\times10^{-20}` from
  `n=10^3` to `n=10^8`; `γ=0.1` (the slowest case, largest `λ`):
  `2.6\times10^{-7}\to9.8\times10^{-28}`).
- **Self-caught issue, disclosed and corrected in-script.** The first
  version of script `03`'s Part 2 fit a power law `g(K)\sim n^{\mu}` to
  `g(K)` *itself* against `n` — the wrong quantity (since `g(K)` grows only
  *logarithmically* in `n`, this two-point power-law fit returns a
  spuriously small exponent, e.g. `μ\approx0.058` at every `γ`, an
  artifact of `\ln(\ln n)/\ln(n)\to0`). This silently produced an
  insufficient `C` and union-bound estimates that grew without bound
  (`\sim10^{30}` at `n=10^8`). Caught before any claim was drafted; fixed
  by correctly fitting `λ:=d(g(K))/d(\ln n)` (i.e. treating `e^{g(K)}`, not
  `g(K)`, as the power-law-in-`n` object) — the corrected fit is what §3.3
  and the log above report. Both the buggy and corrected `Part 2` outputs
  were run; only the corrected log is kept, with the correction narrated
  in-script (see script `03`'s own header comment and `required_C`
  docstring).

**What this section does and does not establish.** The Bulk/Tail Lemma
(§3.2) is a complete, rigorous proof of a genuinely useful reduction. The
scalar limits feeding it (§3.3) are established at the level of
leading-order asymptotic algebra, cross-checked by an independent
numerical fit (§3.4) that matches the predicted leading coefficient to
within finite-`n` correction size at 6 sample `γ` — strong evidence the
asymptotics are correct, but **not** a fully quantified "`\forall n\ge
n_0(γ)`" inequality of the kind a literally complete proof of Gap 1 would
need, and **not** checked to hold uniformly over the *continuum*
`γ\in(0,1)` (only at 6 sample points, plus the two endpoint limits
`γ\to0,1` checked to stay finite in the formula `κ_0(3/2-γ)`).

---

## §4 Direct numerical evidence: the exact (pmf-level) target quantity
## itself shrinks with `n` (script `02`)

Independent of §3's analytic strategy, script `02` computes the *actual*
quantities Gap 1 is about, via **direct summation over the true Binomial
pmf** (`mpmath` dps=50, adaptively-truncated summation window, missed tail
mass disclosed to be below the dps=50 floor) — no Hoeffding bound, no
`g(t)` shortcut, nothing but the exact definitions:

`R_k^{\mathrm{exact}} := \big|E_M[e^{-x(D)}] - (1-E[x]+E[x^2]/2)\big|`,
`\quad R_k^{\mathrm{Gap1}} := \tfrac16E_M[|x(D)|^3e^{|x(D)|}]` (Gap 1's own
literal target), and the weighted sums
`W_{\mathrm{exact}}(n,γ):=\Sigma_{k=1}^Ke^{-s(k)}R_k^{\mathrm{exact}}`,
`W_{\mathrm{bound}}(n,γ):=\Sigma_{k=1}^Ke^{-s(k)}R_k^{\mathrm{Gap1}}`
(`K=1.5\sqrt{n\ln n}`, matching script `03`'s illustrative constant).

**Pointwise sanity** (6 spot `(k,n,γ)` triples spanning `γ\in\{0.5,0.3,0.9,0.99\}`):
`R_k^{\mathrm{exact}}\le R_k^{\mathrm{Gap1}}` holds at **every** tested
point (the elementary Lagrange-remainder inequality, confirmed with no
sign or implementation error).

**Main result — `W_{\mathrm{exact}}` and `W_{\mathrm{bound}}` both decrease
monotonically in `n`, at every one of 6 tested `γ`, `n\in\{500,2000,8000,32000\}`:**

| `γ` | `W_{\mathrm{bound}}(500)` | `W_{\mathrm{bound}}(2000)` | `W_{\mathrm{bound}}(8000)` | `W_{\mathrm{bound}}(32000)` | fitted rate (`8000\to32000`) |
|---|---|---|---|---|---|
| 0.1  | `0.2766` | `0.2146` | `0.1670` | `0.1271` | `-0.197` |
| 0.3  | `0.1171` | `0.0721` | `0.0453` | `0.0291` | `-0.320` |
| 0.5  | `0.02085`| `0.01189`| `0.00717`| `0.00455`| `-0.328` |
| 0.7  | `0.002837`|`0.001372`|`0.000746`|`0.000449`| `-0.366` |
| 0.9  | `6.255e-4`|`1.763e-4`|`5.152e-5`|`1.669e-5`| `-0.813` |
| 0.99 | `5.931e-4`|`1.520e-4`|`3.788e-5`|`9.368e-6`| `-1.008` |

(`W_{\mathrm{exact}}` — the true remainder, not Gap 1's crude bound —
decreases at every `γ` too, generally at a comparable or slightly faster
rate; full table in `02_direct_remainder_numerics.log`.) The decay rate
**steepens as `γ\to1`** and is slowest (still clearly `<0`, i.e. still
decreasing) as `γ\to0` — consistent with §3.3's prediction that the
leading exponent `λ=κ_0(3/2-γ)` (hence the required split constant `C`,
hence how close to a "knife-edge" the bound sits at moderate `n`) is
*largest* at small `γ`, where the numerically visible rate should be
slowest to reach its asymptotic value (it need not literally equal
`-1/4` or `-1/2` at any finite, tested `n` — see the note on knife-edge
behavior in §3.3).

This is **direct, ground-truth confirmation** that the quantity Gap 1
literally asks to be `o(1)` genuinely behaves like `o(1)` in the tested
range, independent of and complementary to the analytic strategy of §3.

---

## §5 What remains open, precisely

**Gap 1 is not closed.** What would be needed to close it fully, beyond
this front's contribution:

1. **Convert §3.3's leading-order asymptotics into an explicit,
   `n\ge n_0(γ)`, fully quantified inequality**, and make `n_0` (or the
   constants inside the `O(\cdot)`/`o(1)` notation) explicit — standard
   real-analysis bookkeeping (bounding each dropped lower-order term of
   `c_1(K),c_2(K)` etc. by an explicit function of `n,k,γ`, rather than
   leading-order matching), genuinely more work but not a new idea. This
   front deliberately stopped at leading-order algebra plus independent
   numerical confirmation, judging that assembling the fully
   explicit-constant version was, on its own, comparable in scope to
   Estágio 30's entire Gap-2 closure — a plausible next front's mandate,
   not attempted here.
2. **Uniformity in `γ\in(0,1)` as a continuum**, not just at the 6 sampled
   points (`0.1,0.3,0.5,0.7,0.9,0.99`) plus the two endpoint limits. The
   formula `λ(γ)=κ_0(3/2-γ)` is manifestly continuous and bounded on
   `(0,1)` (between `κ_0` at `γ=1` and `\tfrac32κ_0` at `γ=0`), which
   strongly suggests uniformity holds with a single `γ`-independent `C`
   (say, `C` calibrated to the worst case `γ\to0`), but this was not
   proved as a `\forall γ` statement here.
3. **Pin down `κ_0`, the actual constant in the wave-17 front's own
   `K\sim\sqrt{n\ln n}` truncation**, rather than the illustrative
   `κ_0=2.25` used for concreteness in scripts `02`/`03`. The Bulk/Tail
   Lemma (§3.2) itself is stated for *any* `K` and *any* split constant
   `C`, so this is a matter of substituting the literal constant, not a
   structural gap — but it was not done here (out of this front's scope,
   since pinning it down requires reading the wave-17 front's own Theorem
   2 proof for the exact truncation choice, which this front's required
   reading did not include and which was not separately consulted for
   this narrow purpose).
4. **The `E[δ]`, `E[δ^2]` terms of Gap 1's original (pre-simplification)
   statement were not separately re-derived** — this front works
   throughout with the single combined `x(D)` (§2), which subsumes them,
   but a literal-minded check that the combined approach exactly
   reproduces the six-term polynomial bound of Gap 1's original wording
   (rather than a structurally equivalent but differently-organized bound)
   was not separately carried out.
5. **Gap 3** (uniformity over the full truncation range `k\le K`) is,
   per Estágio 30, "restricted to Gap 1's pieces" at this point — since
   this front's Bulk/Tail Lemma is *already* uniform in `k\le K` by
   construction (the bound `R_k\le\ldots` in §3.2 has no `k`-dependence on
   its right-hand side), **the shape of a Gap-1-driven Gap-3 closure is
   now visible** (once §5.1–5.3 above are completed, Gap 3's remaining
   piece would follow immediately from the Bulk/Tail Lemma's own
   `k`-uniformity, at no extra cost) — but this front makes no claim to
   have closed Gap 3, since Gap 1 itself remains open.

**`C(γ)` for `γ\in(0,1)` remains fully OPEN.** This front's contribution:
one new exact-algebra fact (§2), one new rigorous reduction lemma (§3.2),
leading-order asymptotics plus independent numerical confirmation that the
resulting bound behaves as needed (§3.3–3.4), and direct ground-truth
numerical confirmation of Gap 1's own literal target quantity (§4) — a
genuine, structurally sound, partially-but-not-fully rigorous narrowing of
Gap 1, the harder of the two gaps left after Estágio 30.

---

## §6 Scorecard

| Claim | Status |
|---|---|
| `x(D)=δ(D)+τ(M)/2` is an exact cubic polynomial in `D`, closed-form coefficients | **PROVED** (this front, §2; two independent symbolic routes, sympy-checked, exact zero difference) |
| Bulk/Tail Lemma: `R_k\le\tfrac16[g(Θ_K)^3e^{g(Θ_K)}+2n^{-2C^2}g(K)^3e^{g(K)}]`, uniform `k\le K`, any `C>0` | **PROVED** (this front, §3.2; elementary — monotonicity + Hoeffding's inequality, cited classical) |
| `g(Θ_K)\to0`, `g(K)=κ_0(3/2-γ)\ln n\,(1+o(1))` | **leading-order asymptotics, confirmed by independent numerical fit** (this front, §3.3–3.4) — NOT a fully explicit-constant inequality |
| `\Sigma_ke^{-s(k)}R_k^{\mathrm{Gap1}}\to0` (Gap 1's literal target) | **strong combined analytic+numerical evidence** (§3, §4) — NOT proved with fully explicit constants, uniform in `γ` |
| Direct pmf-level numerical confirmation, `W_{\mathrm{exact}},W_{\mathrm{bound}}\to0`, 6 `γ` values, `n` up to 32000 | **CONFIRMED**, monotone decrease at every tested `γ` (this front, §4, `mpmath` dps=50, exact Binomial pmf) |
| **Gap 1 (Taylor-remainder-with-moments bound on `E_M[e^{-δ(M)-τ(M)/2}]`)** | **PARTIALLY closed** — new exact structure + new rigorous reduction lemma + strong asymptotic/numerical evidence, but not a fully assembled explicit-constant proof |
| Gap 2 (`M`-fluctuation correction to `τ`) | unaffected — remains **CLOSED** (Estágio 30, cited, not re-touched) |
| Gap 3 (uniformity over the truncation range) | unaffected in status — Gap 1's own `k`-uniform Bulk/Tail Lemma (§3.2) makes the *shape* of a future Gap-3 closure visible, but Gap 3 is not claimed closed here |
| **`C(γ)` for `γ∈(0,1)` (the ultimate target, per Estágio 26)** | **NOT PROVED** — still open; Gap 1 narrowed from "no attempt, structurally harder than Gap 2" to "concrete strategy, strong partial rigor and strong numerical support, not fully assembled" |

### What remains open (named precisely)

See §5, items 1–5, for the precise technical remainder of Gap 1 itself.
Everything else this lineage already left open and untouched by this
front: `C(γ)` for `γ\in(0,1)` itself (still fully open, pending Gap 1's
full closure and Gap 3's remaining piece); the intermediate window
`n^ε\le c_n\le n^{2/3}/\log` for the first-order law; the joint two-point
exploration machinery (Estágio 18); `p>20` of `D^{*(p)}_r(b)`; the
continuous-native construction of Theorem J; the distributional bridge
`M_n(c)\to_dM(c)`; the `H2` floor at `b=1`; the DISC-DEC-071 plateau
constant. No claim of progress on any Millennium Problem; pure
combinatorial mathematics internal to this archive.

### Seeds table

| Block | Status |
|---|---|
| `20260890000–20260890999` (this front's reservation, `DISC-DEC-088`) | reserved; **zero seeds drawn** — every result in this front is exact symbolic algebra (`sympy`), deterministic high-precision numerics (`mpmath` dps=50, exact Binomial pmf), or deterministic float64 closed-form evaluation for a qualitative rate/threshold check — disclosed as unused rather than silently abandoned |

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_symbolic_x_polynomial.py` / `.log` | fresh symbolic (sympy) derivation of `x(D)`'s exact cubic closed form, two independent routes, `γ=1` consistency check |
| `02_direct_remainder_numerics.py` / `.log` | ground-truth numeric (mpmath dps=50, exact Binomial pmf, adaptive-window truncation) evaluation of `R_k^{\mathrm{exact}}`, `R_k^{\mathrm{Gap1}}`, and the weighted sums `W_{\mathrm{exact}}(n,γ)`, `W_{\mathrm{bound}}(n,γ)`, `γ\in\{0.1,\ldots,0.99\}`, `n` up to `32000` |
| `03_bulk_tail_split_check.py` / `.log` | fast float64 evaluation of the Bulk/Tail Lemma's own `g(Θ_K)`, `g(K)` quantities and the resulting union-bound estimate, `n` up to `10^8`, all 6 `γ`; includes the self-caught-and-corrected exponent-fitting bug, narrated in-script |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
