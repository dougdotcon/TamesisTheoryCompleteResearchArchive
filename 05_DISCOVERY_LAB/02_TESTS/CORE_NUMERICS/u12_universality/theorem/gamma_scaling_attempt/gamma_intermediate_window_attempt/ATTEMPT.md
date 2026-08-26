# ATTEMPT — the intermediate window `n^ε ≤ c_n ≤ n^{2/3}/log n`: closing the residual gap between Estágio 10 and Corolário 2

**`GAMMA-INTERMEDIATE-WINDOW-ATTEMPT`, `DISC-DEC-088`, wave 20 front
(d).** First dedicated attack on the "natural residual gap" named
explicitly in `THEOREM.md` (Estágio 23) and in the predecessor's own
`gamma_scaling_attempt/ATTEMPT.md` §8 ("What remains open", item 2):
the relative-error / universality question for `c_n` growing with `n`
strictly between the fixed-`c` regime of Estágio 10 and the
`γ_n ≥ n^{-1/3}\ln n` regime of Corolário 2 (Estágio 23).

Pure combinatorics / asymptotic analysis internal to this archive
(`Tamesis Discovery Lab`). **No claim of any kind about any Millennium
Prize Problem is made anywhere in this document.**

---

## VERDICT (up front)

> **FULL CLOSURE of the named window**, by direct combination of two
> **already-PROVED** archive results — **Teorema R** (Estágio 22) and
> **Corolário 4.2** (Estágio 6) — exactly the "most direct route" the
> mandate asked to check first. No new machinery was needed; the
> closure is three lines of elementary algebra plus bookkeeping of an
> already-certified constant bracket.
>
> **Theorem W (this document, PROVED).** For every integer `n≥4` and
> every real `1 ≤ c ≤ n`,
>
> `\displaystyle \left|\frac{φ(n,c)}{φ_∞(c)} - 1\right| \;\le\; B(n,c) := \frac{a^*\sqrt c + κ_B}{n\left[(\sqrt π/2)c^{-1/2} - e^{-c}/(2c)\right]}`,
>
> with `a^*=\sqrt π(1/\sqrt2-1/2)=0.36708721\ldots` and `κ_B<0.2805`
> (Estágio 22's certified bracket). **Consequently**, for every fixed
> `ε∈(0,2/3)` **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-090.
> O referee hostil identificou que este box afirmava originalmente
> `ε∈(0,1)`, inconsistente com a própria §0 abaixo, que deriva
> corretamente que a janela só é genuinamente (eventualmente) não-vazia
> para `ε∈(0,2/3)` — para `ε\ge2/3`, `n^ε` eventualmente excede
> `n^{2/3}/\log n` e nenhuma sequência satisfaz os limites da janela
> para todo `n` grande, tornando o "teorema" para `ε\in[2/3,1)`
> verdadeiro apenas vacuamente. Corrigido para `ε∈(0,2/3)`, batendo com
> a §0. Não é um erro matemático — o conteúdo substantivo (fechamento
> para `ε∈(0,2/3)`) é exatamente o que §0, §2 e §3 sempre afirmaram
> corretamente e o que o referee verificou.]** and every sequence `c_n`
> with `n^ε ≤ c_n ≤ n^{2/3}/\log n`
> — the exact named window —
>
> `\displaystyle \frac{φ(n,c_n)}{φ_∞(c_n)} \longrightarrow 1` as `n\to\infty`,
>
> with the fully explicit, non-asymptotic rate `B(n,c_n) \le
> \big(2a^*/\sqrt π\big)\,(c_n/n)\,(1+o(1))`, i.e. `O\!\big(n^{-1/3}/\log n\big)`
> at the window's hardest (upper) edge and faster at every other point
> of the window.
>
> **Bonus, beyond the mandate (flagged honestly, not claimed as the
> headline result):** `B(n,c_n)\to0` for *any* sequence with
> `c_n\to\infty` and `c_n=o(n)` — no lower-growth-rate hypothesis on
> `c_n` is needed at all. This strictly subsumes the `γ_n\to0` half of
> Corolário 2 (which required the extra hypothesis
> `γ_n n^{1/3}/\ln n\to\infty`) via a much shorter argument; it does
> **not** touch, weaken, or reprove Corolário 2's `γ_n\to γ^*\in(0,1]`
> half, which needs the finer machinery and gives strictly more (the
> exact non-trivial limit `\sqrt{2/(2-γ^*)}`, plus a proved
> `O(n^{-1/4})` rate and a conjectured second-order term) — genuinely
> different, harder territory this front did not attempt.

---

## §0 The window, restated precisely, with its two boundary regimes

**The object** (Definition 1, `THEOREM.md` §1): `π` a uniform
permutation of `[n]`; `ξ_i` i.i.d. Bernoulli(`q`), `q=\min(c/n,1)`;
`U_i` i.i.d. uniform on `[n]`; `f(i)=U_i` if `ξ_i=1`, else `f(i)=π(i)`;
`φ(n,c) := E[\#\{i \text{ cyclic}\}]/n`.

**Boundary regime A — Estágio 10 (fixed `c`).** For `c` in a fixed
compact `[0,C]` (or all of `[0,\infty)`, Teorema C), as `n\to\infty`:
`\sup_c|φ(n,c)-φ_∞(c)|\to0` — an **absolute** statement. Since `c` is
fixed, `φ_∞(c)>0` is a fixed positive constant, so this trivially also
gives the **relative** statement `φ(n,c)/φ_∞(c)\to1`. Estágio 10 does
not, and was never meant to, say anything about `c=c_n\to\infty`.

**Boundary regime B — Corolário 2, Estágio 23 (`γ_n:=c_n/n`).** For
`γ_n\to γ^*\in(0,1]`, `φ(n,γ_n n)/φ_∞(γ_n n)\to\sqrt{2/(2-γ^*)}`; in
particular for `γ_n\to0` **subject to** `γ_n n^{1/3}/\ln n\to\infty`
(equivalently `c_n \gg n^{2/3}\ln n`), the ratio `\to1`. The
predecessor's own Remark (§6, "what Corolário 2 does *not* claim")
states verbatim: for `γ_n` decaying faster than `n^{-1/3}\ln n`
(`c_n \ll n^{2/3}\ln n`), "this front proves nothing... the *relative*
statement in the window `n^ε \ll c_n \ll n^{2/3}/\log` is left open —
named here as the natural residual gap." This is copied essentially
verbatim into `THEOREM.md` Estágio 23.

**The window itself, precisely:** for a fixed `ε\in(0,1)` (the
mandate's phrasing implicitly intends `ε\in(0,2/3)` so the window is
non-empty for large `n`, verified numerically in §2 below for
`ε\in\{0.1,0.3,0.5,0.6\}`),

`\displaystyle n^ε \;\le\; c_n \;\le\; \frac{n^{2/3}}{\log n}`.

Two structural facts about the window, both elementary and both used
below: (i) `c_n\to\infty` (from the lower edge, `n^ε\to\infty` for any
`ε>0`); (ii) `c_n=o(n)` (from the upper edge,
`n^{2/3}/(n\log n)=n^{-1/3}/\log n\to0`) — in particular `γ_n=c_n/n\to0`
throughout the window, so the *target* value in this window is the
"no-degradation" limit `1`, not a non-trivial `\sqrt{2/(2-γ)}`; and
(iii) the window's upper edge is, for every `n>e`, strictly **below**
Corolário 2's threshold: `n^{2/3}/\log n < n^{2/3}\log n` iff
`1/\log n<\log n` iff `n>e` — so the window is a genuine gap, not an
overlap, for all `n` of interest.

---

## §1 Approach: check Teorema R first (the direct route)

The mandate flagged this as the route most likely to resolve the
window directly, and it does. Two already-PROVED ingredients, both
cited (not re-derived) from `THEOREM.md`:

> **Teorema R (`THEOREM.md`, Estágio 22, PROVED, cited).** For every
> integer `n\ge4` and every real `0\le c\le n`:
> `|φ(n,c)-φ_∞(c)| \le (a^*\sqrt c+κ_B)/n`, `a^*=\sqrt π(1/\sqrt2-1/2)`,
> `κ_B\in(0.28048,0.2805)` (certified branch-and-bound bracket).

> **Corolário 4.2 (`THEOREM.md`, Estágio 6, PROVED, cited).** For
> every real `c>0`: `φ_∞(c) = (\sqrt π/2)c^{-1/2} - R(c)`,
> `0<R(c)<e^{-c}/(2c)`.

The predecessor front (`gamma_scaling_attempt`) explicitly considered
and rejected this exact route — but only for the *fixed-`γ`* regime
`c=γn`, `γ` a constant `>0`: there, `φ_∞(γn)=\Theta(n^{-1/2})` while
Teorema R's bound is `O(1/n)` absolute, giving `O(1)` **relative**
error — genuinely vacuous. That diagnosis is correct for fixed `γ>0`
and is **not** disputed here.

**What the predecessor did not check separately: whether the same
route is vacuous in the `γ_n\to0` regime.** It is not. In this regime
`φ_∞(c_n) \sim (\sqrt π/2)c_n^{-1/2}`, which — because `c_n=o(n)` — is
*larger* than `\Theta(n^{-1/2})`, so dividing Teorema R's `O(1/n)`
absolute bound by it gives a genuinely vanishing relative bound. This
is exactly the mechanism this document exploits.

**Combining the two bounds** (elementary: `|φ/φ_∞-1|=|Δ_n(c)|/φ_∞(c)`,
apply Teorema R to the numerator and Corolário 4.2's lower estimate to
the denominator) gives Theorem W stated in the verdict. The only
non-trivial bookkeeping is checking the denominator
`(\sqrt π/2)c^{-1/2}-e^{-c}/(2c)` stays positive on the window — it
does, comfortably: numerically the crossover to positivity is at
`c\approx0.2094` (found by bisection, §2, script 01), and the window's
lower edge `c_n\ge n^ε>1` for every `n\ge4,\,ε>0` is far above it, so
`c\ge1` is used as a clean, safely-sufficient hypothesis in Theorem W's
statement.

---

## §2 Verification

All verification uses `mpmath` at `dps=50` (no naive float64 for
anything claimed as evidence) or exact/high-precision closed-form
manipulation; no randomness is used anywhere (this is a fully
deterministic algebraic/analytic combination of two cited theorems,
not a Monte Carlo question) — the reserved seed range
`20260896000`–`20260896999` was not needed and was not drawn from. No
`.py` file of any front in this lineage was opened; both verification
scripts below were built from scratch from the prose of `THEOREM.md`
and the predecessor's `ATTEMPT.md` (read in full, as required) only.

### Script `01_verify_bound_algebra.py` — the combined bound, at scale

- Confirms `a^*=\sqrt π(1/\sqrt2-1/2)=0.36708721186\ldots` to 50 digits
  and uses a certified-conservative rounding (`0.3670873`, `0.2805`)
  for `a^*,κ_B` so every downstream inequality remains a valid (if
  microscopically loose) upper bound.
- Confirms the window is non-empty for `ε\in\{0.1,0.3\}` already at
  `n=10^3` and for `ε=0.5` from `n\gtrsim10^{12}`, `ε=0.6` needs larger
  `n` still — consistent with the window requiring `ε<2/3` for
  eventual non-emptiness.
  **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-090.] O referee
  hostil encontrou que o limiar "`n\gtrsim10^{12}`" para `ε=0.5` reflete
  um artefato de grade de teste esparsa (provavelmente potências de dez
  bem espaçadas), não a verdadeira travessia. Re-derivação independente
  do referee localiza a travessia real entre `n=10^7` e `n=10^8` (em
  `n=10^7`: `\ln n=16{,}12>n^{1/6}=14{,}68`, falha; em `n=10^8`:
  `\ln n=18{,}42<n^{1/6}=21{,}54`, satisfaz) — quatro a cinco ordens de
  magnitude mais cedo que o valor declarado. As alegações para
  `ε\in\{0.1,0.3\}` ("já em `n=10^3`") e `ε=0.6` ("precisa de `n`
  maior ainda", travessia real independentemente localizada entre
  `10^{26}` e `10^{27}`) permanecem corretas — conservadoras, mesmo.
  Não afeta nenhum teorema: a não-vacuidade da janela para todo
  `ε<2/3` em `n` suficientemente grande é o único fato que a prova
  realmente usa, e permanece correta; o problema é confinado a esta
  descrição numérica auxiliar do §2, não à substância do fechamento.]**
- Evaluates `B(n,c_n)` at the window's **worst (upper) edge**
  `c_n=n^{2/3}/\ln n` for `n` from `10^2` to `10^{300}`: **strictly
  decreasing, `\to0`**, and already `<0.03` at `n=100` — the closure is
  not just asymptotic window-dressing, it is numerically meaningful at
  small, ordinary `n`.
- Confirms the predicted leading asymptotic order
  `B(n,n^{2/3}/\ln n) \sim (2a^*/\sqrt π)\,n^{-1/3}/\ln n`: the ratio
  of the exact bound to this leading term converges to `1.0000002` by
  `n=10^{20}` and stays there out to `n=10^{1000}` — confirming the
  analytic derivation, not just its qualitative direction.
- Confirms the **lower** edge `c_n=n^ε` (`ε=0.1,0.3,0.5`) decays even
  faster, as expected (`B=O(n^{ε-1})`, a strictly faster rate than the
  upper edge's `O(n^{-1/3}/\log n)` for `ε<2/3`).
- Non-vacuousness/honesty check: at `ε=0.3`, the bound at the window's
  hardest point already drops below `0.5` at `n=10`, below `0.1` at
  `n=100`, below `0.01` at `n=1000` — the asymptotic closure "kicks in"
  at ordinary, not astronomical, `n`.

Full transcript: `01_verify_bound_algebra.log`.

### Script `02_verify_phi_finite_n.py` — independent finite-`n` engine

An independent, from-scratch implementation of the exact finite-`n`
double-sum formula for `φ(n,c)` (Lemma 1, derived and PROVED —
including independent referee re-derivation — in the predecessor's
`gamma_scaling_attempt/ATTEMPT.md` §1, cited here by its stated
formula only, no `.py` opened):

`φ(n,qn) = \tfrac1n\sum_{k=1}^n A_k(n,q)`, `A_k=\sum_{m=0}^k\binom km q^m(1-q)^{k-m}P_{k,m}`,
`P_{k,m}=\prod_{i=1}^m(1-\tfrac{k-i}n)`,

evaluated with `mpmath` at `dps=50`, incrementally (`O(n^2)` total
work, exact recurrences for the binomial coefficient, the power term,
and the partial product — a performance detail only, not a different
quantity). Purpose: an *empirical*, independent check on top of the
pure algebra of script 01, going one level deeper than "trust the
citation."

- **(a) Sanity.** `φ(n,0)=1` exactly for `n=1,5,20,100` (Remark 1.1 of
  the predecessor's Lemma 1) — confirms the from-scratch engine is
  correctly wired before trusting it for anything else.
- **(b) Teorema R, pointwise, re-checked independently.** At 20 test
  points spanning `n\in\{30,100,300,1000,3000\}` and
  `c=n^α`, `α\in\{0.15,0.35,0.55,0.65\}` (the last two exceed the
  window's own `2/3` cutoff deliberately, as a stress test), **zero
  violations** of `|φ(n,c)-φ_∞(c)|\le(a^*\sqrt c+κ_B)/n` — this is a
  consistency re-check of the theorem's transcription and of the
  independent engine, not a re-proof of Teorema R itself (which is
  already an accepted, referee-verified archive result).
- **(c) Ratio trend.** At every fixed `α`, the ratio
  `φ(n,c)/φ_∞(c)` visibly moves toward `1` as `n` grows
  (e.g. at `α=0.15`: `0.9978\to0.9999642` from `n=30` to `n=3000`; at
  `α=0.65`, just past the window's own boundary shape and hence
  converging more slowly as expected: `1.0372\to1.0130`) — direct
  empirical confirmation of the mechanism, independent of the abstract
  bound algebra.

Full transcript: `02_verify_phi_finite_n.log`.

---

## §3 What this does and does not close, precisely

**Closes, fully:** the named window `n^ε\le c_n\le n^{2/3}/\log n`,
for every fixed `ε\in(0,2/3)` — `φ(n,c_n)/φ_∞(c_n)\to1`, with an
explicit non-asymptotic bound `B(n,c_n)` (Theorem W) and confirmed
leading rate `O(n^{-1/3}/\log n)` at the window's hardest point.

**Also closes, as an honestly-flagged bonus beyond the named window:**
the same conclusion for *any* `c_n\to\infty` with `c_n=o(n)` — no
lower-rate restriction on `c_n` is needed, unlike Corolário 2's
`γ_n\to0` sub-case (which required `γ_n n^{1/3}/\ln n\to\infty`).
Combined with Estágio 10 (bounded `c`, trivial) this means: **for
`γ_n:=c_n/n\to0`, `φ(n,c_n)/φ_∞(c_n)\to1` unconditionally, with no rate
hypothesis on `γ_n` at all.** This does not touch Corolário 2's
`γ_n\to γ^*\in(0,1]` half (the genuinely harder case with a non-trivial
limit and a proved `O(n^{-1/4})` rate) — that result is strictly
stronger where it applies and is not reproved, weakened, or superseded
here.

**Does NOT close:** the sharper questions the predecessor and
`THEOREM.md` leave open elsewhere in this line — a proved (not just
conjectured) `n^{-1/2}` rate and second-order term `C(γ)` for
`γ\in(0,1)` (Estágio 23/26); whether an analogue of the second-order
term `C(γ)\to?` exists and is provable as `γ_n\to0` inside the window
(not attempted here — Theorem W only gives the leading `\to1` fact
with an `O(c_n/n)`-type rate, not a matched second-order constant);
Conjecturas 1–2 (already closed elsewhere, untouched here); anything
about `H2` at `b=1`, `p>20`, or the joint two-point exploration
(untouched, irrelevant to this window). **No claim of progress on any
Millennium Prize Problem is made or implied anywhere in this
document** — this is pure combinatorial/asymptotic mathematics
internal to the Tamesis Discovery Lab archive.

---

## §4 Honesty notes

- The headline closure is genuinely a three-line combination of two
  results already at PROVED, referee-accepted status in `THEOREM.md`
  (Teorema R, Estágio 22; Corolário 4.2, Estágio 6). No new deep
  mathematics was required — the contribution of this front is the
  **diagnosis** that the predecessor's own correct rejection of this
  route for fixed `γ>0` does not extend to the `γ_n\to0` window, plus
  carrying out the resulting (easy but previously undone) combination
  rigorously and checking it does not silently break down anywhere
  inside the named window.
- The "bonus" claim (no rate restriction needed for `γ_n\to0`) is
  presented honestly as a byproduct, not oversold: it is strictly
  weaker in content than Corolário 2's `γ_n\to γ^*>0` half (which gives
  a non-trivial limit value, a proved rate, and a conjectured
  second-order term); it only strengthens the specific `γ_n\to0`
  sub-case of Corolário 2 by removing an unnecessary hypothesis for
  the "ratio `\to1`" conclusion alone.
- Every numeric constant used (`a^*`, `κ_B`'s bracket) is taken **by
  citation** from already-PROVED, already-referee-audited results in
  `THEOREM.md`; none is re-derived here, consistent with how the
  archive's own fronts routinely build on prior PROVED results without
  re-proving them each time. `a^*`'s exact closed form was independently
  recomputed to 50 digits in script 01 as a transcription check.
- Both verification scripts are original, written from the prose only
  (no predecessor `.py` file was opened, per the hard constraint); no
  git command was run; no referee was dispatched (out of scope for
  this front, per mandate); no governance file (`THEOREM.md`,
  `DECISION_LEDGER.yaml`, etc.) was touched.

---

## §5 Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_verify_bound_algebra.py` / `.log` | combined-bound evaluation at scale (`mpmath` dps=50); window non-emptiness; worst-edge decay `n=10^2..10^{300}`; leading-order confirmation; lower-edge decay; non-vacuousness/honesty thresholds |
| `02_verify_phi_finite_n.py` / `.log` | independent from-scratch finite-`n` engine for `φ(n,c)` (Lemma 1 double sum, `mpmath` dps=50); sanity check; 20-point Teorema R re-check (0 violations); ratio-to-1 trend at moderate, computationally-reachable `n` |

No Millennium Problem claims anywhere; pure combinatorial mathematics
internal to this archive. No git commits made by this front.
