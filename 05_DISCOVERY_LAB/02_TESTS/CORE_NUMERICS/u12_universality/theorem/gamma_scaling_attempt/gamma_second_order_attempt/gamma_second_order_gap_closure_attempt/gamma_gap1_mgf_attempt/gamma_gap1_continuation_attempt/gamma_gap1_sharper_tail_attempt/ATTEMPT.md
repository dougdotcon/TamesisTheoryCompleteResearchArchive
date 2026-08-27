# ATTEMPT — A sharper tail-control technique for the Bulk/Tail Lemma
# (shrinking `n_0(γ)`, `γ∈(0,1)`)

**Wave 22, front (c), `GAMMA-GAP1-SHARPER-TAIL-ATTEMPT`, authorized by
`DISC-DEC-096`.** Mandate: the direct predecessor
(`GAMMA-GAP1-CONTINUATION-ATTEMPT`) closed the *logical* gap between
leading-order asymptotics and an explicit `∀n≥n_0(γ)` inequality for the
Bulk/Tail Lemma's tail piece, but named — explicitly, as the hardest
unresolved item — that the resulting `n_0(γ)` is astronomically large
(`~10²¹` at `γ=0.99` up to `~10⁸⁵` at `γ=0.01`) because it is built on
Hoeffding's inequality, a generically loose tail bound. Its own §5 item 2
named the fix without attempting it: *"a fundamentally tighter term-by-term
bounding technique ... or a Bernstein/sub-Gaussian MGF bound sharper than
the generic Hoeffding lemma this lineage already uses elsewhere ... This
front did not attempt either."* This front attempts it.

---

## VERDICT (up front)

> **Gap 1 remains NOT closed; `C(γ)` for `γ∈(0,1)` remains fully OPEN.**
> This is a genuine **partial improvement**, not a closure — exactly the
> outcome the dispatching mandate named as fully acceptable for this,
> the hardest item in the wave. Concretely:
>
> 1. **The technique: Bernstein's inequality (variance-aware) in place of
>    Hoeffding (variance-blind).** Derived from scratch (an elementary,
>    ~15-line MGF argument, §2/script `01`), independently verified against
>    the *exact* Binomial tail (`mpmath` dps=50, zero violations, script
>    `01`) and confirmed dramatically sharper than Hoeffding pointwise away
>    from `γ=1/2` (up to `10⁻³²⁸` of Hoeffding's bound at `γ=0.01`,
>    script `01` Part C).
> 2. **Making it `k`-uniform required a new construction** (Hoeffding's
>    clean `k`-cancellation, `P(|D|>Θ_k)=2n^{-2C²}` exactly independent of
>    `k`, has no exact analogue for Bernstein). A "slack parameter" `a>0`
>    device (§3/script `03`) recovers a clean, `k`-independent bound
>    `2n^{-C²/((2+a)σ²)}` for `k≥k_2(n,γ,C,a):=O(\ln n)`, plus a trivial
>    deterministic bound for the residual `k<k_2` region — both
>    independently verified with zero violations (script `03`).
> 3. **The flagship finding (exact algebra, not numeric sampling):
>    `C0_Bernstein(γ,a)²` is BOUNDED on the entire open interval `(0,1)`,
>    for every fixed `a>0`** (§4/script `04`) — unlike `λ(γ)`/`\hatλ(γ)`
>    alone (the Hoeffding-route quantity the predecessor proved
>    **unbounded** as `γ→0⁺`, Estágio 36). The mechanism is structural, not
>    coincidental: `\hatλ(γ)∼28/γ` diverges because `κ_0(γ)∼4/γ` does, but
>    the true Bernoulli variance `σ²(γ)=γ(1-γ)∼γ` shrinks at *exactly* the
>    matching rate, so `σ²(γ)·\hatλ(γ)→28` (finite) as `γ→0⁺`. **A single
>    `γ`-independent `C` now suffices for the entire open interval `(0,1)`
>    simultaneously** — not merely on compact subsets `[γ_0,1)` as under
>    Hoeffding. This is a genuine bonus beyond the task's literal ask
>    (which was about `n_0(γ)`, not uniformity), obtained for free from the
>    same construction.
> 4. **Concretely assembled and bisected `n_0(γ)`, at the same 8 sample
>    `γ` values the predecessor reported** (§5/script `05`), reusing —
>    unchanged, independently re-verified, not re-derived — the
>    predecessor's own coefficient bounds and `\hat G`/`\hat G_Θ` assembly,
>    so the comparison isolates *only* the tail-technique change. A
>    calibration check (this front's own Hoeffding re-implementation vs.
>    the predecessor's *published* table, transcribed as plain values, not
>    code) matches to `<0.01` decades at all 8 points, validating the
>    whole machinery before trusting the new numbers.
>
> **Net numeric result:** genuine reduction in `n_0(γ)` at 7 of 8 tested
> points, ranging from a modest `0.44`–`3.19` decades at moderate `γ` up to
> **`9.09` decades (a factor of `~10⁹`) at `γ=0.01`**, growing systematically
> as `γ→0` or `γ→1` — precisely where the predecessor's construction was
> weakest. At `γ=0.5` the result is a negligible `0.07`-decade *loss*
> (understood, structural, quantified — §7). **This is a constant-factor
> (in the sense of: same power-of-`n` structure of the final threshold,
> `n_0` still a finite but astronomically large explicit number) improvement
> in the *leading constant*, growing without bound as `γ→0,1` — combined
> with a genuine asymptotic-order (bounded- vs. unbounded-`C₀²`) structural
> improvement in the separate question of uniformity across `γ`.**
> `n_0(γ)` remains **far** from numerically useful (`10¹⁸`–`10⁷⁶`, still
> vastly beyond the predecessor's own ground-truth pmf range, `n` up to
> `32000`) — this front does not claim otherwise. No claim of progress on
> any Millennium Problem; pure combinatorial/asymptotic mathematics
> internal to this archive, about a specific random-permutation-with-reroutes
> ensemble.

---

## §0 Provenance and discipline

**Required reading, done in full, in prose, before any derivation or code
was written**, per the dispatching mandate:

1. `THEOREM.md` Estágio 23 (Teorema 2, the leading-order `γ`-scaling
   result), Estágio 26 (Lema E, Lema D0, the reduction of `C(γ)` to Lacunas
   1/2/3), Estágio 30 (Lacuna 2 closure — the closest methodological
   precedent, an *exact* closed-form route, not applicable here since Gap
   1's object is genuinely transcendental), Estágio 33 (the Bulk/Tail
   Lemma, Lacuna 1's structure), and **Estágio 36 in full** (the direct
   predecessor's own contribution: the corrected `κ_0(γ)=8/(γ(2-γ))`,
   `λ(γ)=4(3-2γ)/(γ(2-γ))` continuous but UNBOUNDED on `(0,1)`, and the
   explicit-but-astronomically-large `n_0(γ)` construction, `~10²¹` to
   `~10⁸⁵`).
2. `.../gamma_gap1_mgf_attempt/gamma_gap1_continuation_attempt/ATTEMPT.md`
   (the direct predecessor), read in full — the exact form of the
   Bulk/Tail Lemma's inequality, the Hoeffding-based tail control it uses,
   the exact form of its explicit coefficient bounds and `\hat G`/`\hat
   G_Θ` assembly (§4 Steps 1–6), and precisely how `n_0(γ)` was assembled,
   including the dated post-adversarial correction (looseness factor
   `\hatλ/λ` corrected to `6`, not `3`, at `γ=1`).
3. `.../gamma_second_order_gap_closure_attempt/gamma_gap1_mgf_attempt/ATTEMPT.md`
   (the grandparent), read in full — the exact statement of `C(γ)`'s
   reduction, the exact cubic-polynomial identity for `x(D):=δ(D)+τ(M)/2`
   (§2, including the referee's dated correction to the closed form of
   `c_0`), and the original Bulk/Tail Lemma (§3.2) with its Hoeffding step.

**No `.py` file of this front's own lineage, or any sibling front, was
opened, read, or imported anywhere in this front.** Every script below
(`01`–`06`) is written fresh from the mathematical prose of the three
documents above. Where this front *reuses* a predecessor result without
re-deriving it from first principles (the exact cubic coefficients `c_i`,
the elementary coefficient bounds `|c_i(k)|≤...`, the `\hat G` assembly, the
cited `G_n≤√(πn/β)` bound from the Lemma D0 lineage), it is **independently
re-derived and/or independently numerically re-verified** in script `02`
(zero violations, `n` up to `10⁸⁰`) rather than taken on faith — this is
disclosed explicitly at each point below, distinguishing "cited, re-verified"
from "newly derived by this front."

**Seeds.** Reserved block `20260914000–20260914999` (this front,
`DISC-DEC-096`). `grep -rn "20260914" 05_DISCOVERY_LAB/` was run before any
code and found only the governance-ledger/queue reservation lines — no prior
use, no conflict. **This front draws zero random seeds** — every claim is
exact symbolic algebra (`sympy`, scripts `02`, `03` Part C, `04`) or
deterministic high-precision numerics (`mpmath` dps=50–60, exact pmf
summation or exact closed-form evaluation, scripts `01`, `02`, `03`, `05`,
`06`, all deterministic grids, no Monte Carlo). The reserved block is
disclosed as unused, not silently abandoned.

**Not touched, per mandate:** `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`,
`README.md`, `index.html`, any file outside this front's own new
subdirectory (including the sibling `gamma_gap1_continuation_attempt/`
front's own files and `adversarial/` directory, neither of which was
touched or read as code). No git commands run. No `adversarial/`
subdirectory created inside this front's own directory; no referee
dispatched (reserved for the orchestrating session, per mandate).

---

## §1 What this front attacks, precisely

From the predecessor's own `ATTEMPT.md` §5 item 2 (quoted verbatim):

> *"Sharper constants. The `n_0(γ)` values above are dominated by the
> crude, elementary nature of the coefficient bounds ... and the generous
> `C(γ)=1.2·C_0(γ)` margin choice — a genuinely usable ... explicit bound
> would need either a fundamentally tighter term-by-term bounding technique
> (e.g. tracking exact rather than worst-case cancellation across all three
> coefficients jointly, or a Bernstein/sub-Gaussian MGF bound sharper than
> the generic Hoeffding lemma this lineage already uses elsewhere) or a
> different proof strategy for the tail piece entirely. This front did not
> attempt either."*

This front attacks the first alternative named (a Bernstein-type MGF bound),
per the dispatching mandate's angle 1, and reports honestly on how far it
gets — leaving angle 2 (exact-cancellation tracking in the coefficient
bounds themselves) and angle 3 (a fundamentally different decomposition)
untouched, since angle 1 alone already produces genuine, quantifiable
progress (§7).

**Where in the argument Hoeffding is used, precisely** (grandparent §3.2,
the Bulk/Tail Lemma's *Tail* step): `D:=M-γk`, `M∼\mathrm{Bin}(k,γ)`,
`|D|≤k≤K` always; on the tail event `\{|D|>Θ_k\}`, `Θ_k:=C√(k\ln n)`, the
proof needs `P(|D|>Θ_k)` bounded by something that (i) does not depend on
`k`, and (ii) decays as a clean power of `n`. Hoeffding's inequality
(`D` a sum of `k` i.i.d. terms each bounded in an interval of length `1`)
gives `P(|D|>t)≤2\exp(-2t²/k)`, so at `t=Θ_k`: `2Θ_k²/k=2C²\ln n` **exactly**,
independent of `k` — the source of both its simplicity and its looseness
(it implicitly treats every `γ` as if it had the worst-case variance `1/4`,
i.e. `γ=1/2`).

---

## §2 The technique: Bernstein's inequality, derived and verified (script `01`)

`D=Σ_{i=1}^kY_i`, `Y_i` i.i.d., `Y_i:=\mathrm{Bernoulli}(γ)-γ∈\{1-γ,-γ\}`
w.p. `\{γ,1-γ\}`. Write `σ²(γ):=\mathrm{Var}(Y_i)=γ(1-γ)`,
`M(γ):=\max(γ,1-γ)≥|Y_i|` a.s.

> **Bernstein's inequality (classical; derived from scratch here, cited at
> the same tier this lineage already cites Hoeffding).**
> `\displaystyle P(|D|>t)\le2\exp\!\Big(-\frac{t^2}{2kσ^2+\frac23Mt}\Big)`
> for every `t>0`.

*Proof (elementary, ~15 lines, script `01` docstring; independently
verified numerically below).* For `|Y|≤M`, `E[Y]=0`: `E[Y^j]≤M^{j-2}σ²` for
integer `j≥2` (since `|Y|^j=|Y|^{j-2}Y²≤M^{j-2}Y²` pointwise). Hence
`E[e^{λY}]≤1+(σ²/M²)(e^{λM}-1-λM)≤\exp[(σ²/M²)(e^{λM}-1-λM)]` (Bennett's MGF
bound, classical). The elementary calculus fact `e^u-1-u≤(u²/2)/(1-u/3)` for
`0≤u<3` (proved by termwise comparison of the two power series, an easy
induction: `2·3^{j-2}≤j!` for `j≥2`) gives, at `u=λM`:
`E[e^{λY}]≤\exp[σ²λ²/(2(1-λM/3))]`. Summing `k` i.i.d. copies (`V:=kσ²`) and
Chernoff-optimizing over `λ∈[0,3/M)` (`λ^*=t/(V+Mt/3)`) gives
`P(D≥t)≤\exp(-t²/(2V+2Mt/3))`; two-sided by symmetry. `∎`

**Independent verification (script `01`):**
- Part A: the calculus fact `e^u-1-u≤(u²/2)/(1-u/3)` — `299` points on
  `(0,3)`, **zero violations**.
- Part B: the full inequality vs. the **exact** Binomial tail probability
  (`mpmath` dps=50, direct pmf summation, no shortcuts) — `88` checks across
  `k∈\{5,\ldots,1000\}`, `γ∈\{0.01,\ldots,0.99\}`, `4` threshold multiples —
  **zero violations**; worst `\mathrm{exact}/\mathrm{bound}` ratio `≈0.029`
  (i.e. the bound is never violated and is not absurdly loose either).
- Part C: pointwise comparison against Hoeffding at fixed `(k,t)` across
  `γ` — Bernstein is **dramatically** sharper away from `γ=1/2` (e.g. a
  factor `10^{-328}` of Hoeffding's bound at `γ=0.01`), and *only* loses
  (by a large but finite factor, `≈1.9×10^{10}` at the tested point) exactly
  at `γ=0.5`, where the true variance `σ²=1/4` coincides with what
  Hoeffding implicitly assumes for every `γ` — this is the expected,
  understood crossover, not an anomaly (§7).

---

## §3 Making Bernstein `k`-uniform: the slack-parameter construction (script `03`)

Hoeffding's `2Θ_k²/k=2C²\ln n` cancels the `k`-dependence **exactly**.
Bernstein's denominator `2kσ²+\frac23MΘ_k` has a sub-leading `√k` term (from
the range bound `M`) that does **not** cancel against the `k\ln n` numerator
— so naively, the worst case over `1≤k≤K` occurs at the *smallest* `k`
(`k=1`), where the bound degrades to sub-power-law decay in `n`
(`\exp(-\mathrm{const}·\sqrt{\ln n})`), which is not strong enough to beat
the polynomial-in-`n` growth of the Bulk/Tail Lemma's other side. This is a
genuine structural obstacle the naive substitution does not resolve — this
front's fix:

> **Slack-parameter construction (this front, PROVED, script `03`).** Fix
> `a>0`. If `\frac23MΘ_k≤ak σ²` then the Bernstein denominator
> `≤(2+a)kσ²`, giving
> `\displaystyle P(|D|>Θ_k)\le2\exp\Big(-\frac{C^2\ln n}{(2+a)σ^2}\Big)=2n^{-C^2/((2+a)σ^2)}`
> — **exactly `k`-independent**. Solving the sufficient condition for `k`:
> valid for all `k≥k_2(n,γ,C,a):=\big(2MC/(3aσ^2)\big)^2\ln n`.

For `k<k_2` (a poly-**logarithmic**-in-`n` range, vastly smaller than the
true truncation `K=Θ(\sqrt{n\ln n})`, verified numerically below), **no
probability is needed at all**: `|D|≤k` deterministically, so
`R_k≤\frac16g(k)^3e^{g(k)}` directly, giving a trivial crude union bound
over at most `k_2` terms (using `e^{-s(k)}≤e^{1/2}`, itself justified by an
exact calculus fact, `\min_ks(k)=-γ^2/(16βn)`, script `03` Part C —
confirmed symbolically, zero difference).

**Independent verification (script `03`):**
- Part A: the sufficient condition `\frac23MΘ_k≤akσ^2` holds at and above
  `k_2` — `144` checks across `n,γ,C,a` grids, **zero failures**.
- Part B: the resulting clean, `k`-uniform bound vs. the exact Binomial tail
  probability, `k` just above `k_2`, moderate `n` (exact pmf summation is
  only tractable there) — `84` checks, **zero violations**.
- Part C: `\min_ks(k)=-γ^2/(16βn)` confirmed by exact symbolic calculus
  (`sympy`, zero difference).
- Part D: at the astronomical `n`-scale this front's own `n_0(γ)`
  construction actually needs (`n\sim10^{18}`–`10^{76}`), `k_2/K_{\max}`
  is already `\lesssim10^{-3}` to `10^{-31}` — the small-`k` region is a
  vanishing fraction of the truncation range, as the poly-log-vs-power-law
  argument predicted.

---

## §4 The flagship finding: `C0_Bernstein(γ,a)²` is globally bounded on `(0,1)` (script `04`)

Under Hoeffding, the split constant must satisfy `C²>\frac14+\frac12\hatλ(γ)`
(`\hatλ(γ):=16(7/4-γ)/β(γ)`, the growth rate of the predecessor's own
*explicit, crude* `\hat G(n,γ)` bound — **not** the tighter idealized
asymptotic `λ(γ)`; this front independently confirmed which of the two
quantities is actually load-bearing by first tripping the wrong one, see
§8 item 1). `\hatλ(γ)→+∞` as `γ→0^+` (Estágio 36's own finding, reconfirmed
here) — **no single `γ`-independent `C` exists for all of `(0,1)`** under
Hoeffding.

Under Bernstein-with-slack: `C^2>(2+a)σ^2(γ)(\hatλ(γ)+\frac12)=:C0_{\mathrm{Bernstein}}(γ,a)^2`.

> **PROVED (exact algebra, `sympy`, script `04`).**
> `C0_{\mathrm{Bernstein}}(γ,a)^2` is **strictly decreasing** on `(0,1)` for
> every fixed `a>0` (the derivative's numerator, a cubic in `γ`, is shown
> via `sympy.real_roots` to have **no root in `(0,1)`**, and negative sign
> confirmed at the interior point `γ=1/2`) — hence
> `\sup_{γ\in(0,1)}C0_{\mathrm{Bernstein}}(γ,a)^2=\lim_{γ\to0^+}(\cdot)=28a+56`,
> a **finite** closed form for every `a>0`, vs. Hoeffding's
> `\sup=+\infty`. At `a=0.05` (the value used in §5): `\sup=57.4`, confirmed
> independently by a dense `19{,}999`-point numeric scan (`57.397` found,
> matching to `4` significant figures).

**Why this is not a coincidence.** `\hatλ(γ)∼28/γ` diverges as `γ\to0^+`
because `κ_0(γ)=8/(γ(2-γ))∼4/γ` does (Estágio 36's construction, truncation
`K^2=κ_0n\ln n`). But the *true* Bernoulli variance `σ^2(γ)=γ(1-γ)∼γ`
shrinks at *exactly* the reciprocal rate, so the product
`σ^2(γ)\hatλ(γ)\to28` stays finite. Hoeffding's variance-blind bound cannot
see this cancellation (it always assumes the worst-case `σ^2=1/4`); a
variance-aware bound sees it automatically.

**Consequence (a genuine bonus beyond the literal `n_0(γ)` ask):** a
**single `γ`-independent `C`** now suffices, rigorously, for the entire open
interval `(0,1)` — resolving, via a different tail-control technique
(exactly per the mandate's suggestion), the specific non-uniformity Estágio
36 proved for the Hoeffding route (where only compact-subset uniformity
`[γ_0,1)` was achievable).

---

## §5 Full explicit assembly and the `n_0(γ)` comparison (scripts `02`, `05`)

**Reused, independently re-verified ingredients** (not re-derived from
scratch, since they do not depend on the tail-control technique):
`K_{\max}(n,γ):=4\sqrt{n\ln n/β}`, the elementary coefficient bounds
`|c_0|,|c_1|,|c_2|` and exact `c_3`, the resulting
`\hat G(n,γ):=g_{\mathrm{bound}}(K_{\max},K_{\max},n,γ)`,
`\hat G_Θ(n,γ,C):=g_{\mathrm{bound}}(K_{\max},Θ_{K_{\max}}\text{-bound},n,γ)`,
and the cited `G_n\le\sqrt{πn/β}` (Lemma D0 lineage) — all confirmed by
fresh symbolic re-derivation (`x(D)`'s exact cubic, matching the
grandparent's corrected `c_0` exactly, `sympy`, zero symbolic difference,
two independent routes) and by exhaustive numerical re-verification of the
coefficient bounds (`715` grid points, `n` up to `10^{80}`, **zero
violations**, script `02`).

**The only change:** the tail-probability factor `2n^{-2C^2}` (Hoeffding)
is replaced by `2n^{-C^2/((2+a)σ^2)}` (Bernstein, `a=0.05`) plus the
explicit small-`k` residual term (§3), assembled via `\mathrm{logsumexp}`
in log-domain (`mpmath` dps=60, avoiding overflow at the astronomical `n`
values involved — the same discipline the predecessor used).

**Calibration check, done before trusting any new number** (script `05`):
this front's own from-scratch re-implementation of the **Hoeffding**
construction is bisected for `n_0(γ)` at the same 8 `γ` values and compared
against the predecessor's own **published** table (transcribed as plain
values from its `ATTEMPT.md` prose, not read from any `.py` file):

| `γ` | this front's `C(γ)` | predecessor's `C(γ)` | this front's `\log_{10}n_0` | predecessor's `\log_{10}n_0` |
|---|---|---|---|---|
| 0.99 | 4.2275 | 4.23 | 20.79 | 20.79 |
| 0.9 | 4.4880 | 4.49 | 36.83 | 36.83 |
| 0.7 | 5.1908 | 5.19 | 45.02 | 45.02 |
| 0.5 | 6.2258 | 6.23 | 50.28 | 50.28 |
| 0.3 | 8.1158 | 8.12 | 55.95 | 55.95 |
| 0.1 | 14.1578 | 14.16 | 65.95 | 65.95 |
| 0.05 | 20.0520 | 20.05 | 71.78 | 71.78 |
| 0.01 | 44.8878 | 44.89 | 84.88 | 84.88 |

Maximum discrepancy across all 8 points: **`0.004` decades** — this front's
independent re-implementation of the predecessor's own construction
reproduces its published numbers essentially exactly, validating the
machinery (and, as a side effect, independently re-confirming the
predecessor's own arithmetic).

**Main result — OLD (Hoeffding, predecessor) vs. NEW (Bernstein, this
front, `a=0.05`), `C(γ):=1.2·C_0(γ)` in both cases (same margin
convention):**

| `γ` | OLD `n_0(γ)` (predecessor) | NEW `n_0(γ)` (this front) | decades saved |
|---|---|---|---|
| 0.99 | `\sim10^{20.79}` | `\sim10^{17.72}` | **3.07** |
| 0.9 | `\sim10^{36.83}` | `\sim10^{33.64}` | **3.19** |
| 0.7 | `\sim10^{45.02}` | `\sim10^{44.57}` | 0.46 |
| 0.5 | `\sim10^{50.28}` | `\sim10^{50.35}` | **−0.07** |
| 0.3 | `\sim10^{55.95}` | `\sim10^{55.51}` | 0.44 |
| 0.1 | `\sim10^{65.95}` | `\sim10^{63.06}` | **2.89** |
| 0.05 | `\sim10^{71.78}` | `\sim10^{67.08}` | **4.70** |
| 0.01 | `\sim10^{84.88}` | `\sim10^{75.79}` | **9.09** |

The improvement **grows systematically as `γ→0` or `γ→1`** — exactly where
the Hoeffding-based construction was weakest (per the `\hatλ(γ)`
divergence, §4) — reaching a factor of **`~10⁹`** at `γ=0.01`. At `γ=0.7`
and `γ=0.3` the gain is modest (`<1` decade, `0.46` and `0.44` respectively
— comparable in magnitude, though not related by any exact symmetry of the
underlying quantities); at `γ=0.5` exactly, a small, understood, structural
loss (§7).

> **[Nota pós-adversarial, 2026-08-27 — DISC-DEC-098, sem correção —
> achado cosmético/de clareza de redação, não erro matemático.]** O
> referee hostil (achado #2) apontou que a frase original acima
> ("symmetric around `γ=1/2` by construction, since `\hatλ(γ)` and
> `σ^2(γ)` are not symmetric but happen to give comparable values
> here") era redigida de forma confusa, afirmando "simétrico por
> construção" e "não simétrico" na mesma oração. A alegação numérica
> subjacente (ganhos comparáveis, sub-1-decada, em ambos os pontos)
> está correta e foi confirmada de forma independente pelo referee
> (`0.456` vs `0.442` décadas em sua própria reconstrução). Texto
> corrigido acima para remover a ambiguidade, sem alterar nenhum
> conteúdo matemático ou numérico.

---

## §6 No spurious oscillation; side conditions hold with margin (script `06`)

Since `\log W(n,γ,C,a)` is not obviously monotone in `n` from first
principles near the crossover (both `\hat G` and `\hat G_Θ` grow before the
tail-probability factor dominates), the bisection-found `n_0(γ)` could in
principle be a spurious intermediate sign change rather than the genuine,
durable threshold. Script `06` checks `\log W` on a fine half-decade grid
from `n_0(γ)` through **40 decades beyond**, at 5 representative `γ`, for
**both** constructions:

- Bernstein (this front): **no local increase found anywhere**, at any of
  the 5 tested `γ` (`increasing_found=False` in every case).
- Hoeffding (calibration sanity): likewise **no local increase found
  anywhere** — consistent with the predecessor's own script `06` finding.

Additionally, the `k_2/K_{\max}` side condition (§3) is checked from
`n_0(γ)` through 40 decades beyond at the *tightest* tested case
(`γ=0.99`, where the small-`k` residual term was found to be non-negligible
right at the crossover — §7 item 3): the ratio **strictly shrinks**, from
`2.0\times10^{-3}` at `n_0` down to `3.6\times10^{-23}` forty decades
beyond, confirming the construction only gets *safer*, never more marginal,
further into the regime where the bound is actually used.

---

## §7 What did NOT close, precisely

1. **Gap 1 itself remains open; `C(γ)` for `γ\in(0,1)` remains fully OPEN.**
   This front narrows `n_0(γ)`, sometimes substantially, but does not close
   the underlying gap — exactly the honest, catalogable outcome the
   dispatching mandate named as acceptable for the hardest item in the
   wave.
2. **`n_0(γ)` is still astronomically large** (`10^{18}`–`10^{76}` at the
   tested points) — vastly beyond the predecessor's own ground-truth pmf
   computation range (`n` up to `32000`), and beyond anything numerically
   reachable by direct computation. This front does **not** claim a
   "numerically useful" bound — only a quantified, verified reduction in
   how astronomically large the threshold is.
3. **At `γ=0.5`, the technique gives essentially no improvement (a `0.07`
   decade *loss*, at `a=0.05`).** This is understood and structural, not a
   defect: `σ^2(1/2)=1/4` is *exactly* the worst-case variance Hoeffding
   implicitly assumes for every `γ`, so a variance-aware bound cannot beat
   Hoeffding there — with any fixed slack `a>0`, it loses by a small,
   `a`-dependent margin that `\to0` as `a\to0^+` (§4, §8 item 2). The choice
   `a=0.05` was not optimized per-`γ`; a smaller `a` would push this loss
   closer to zero (at the cost of a larger, but still poly-log and hence
   harmless, small-`k` threshold `k_2`) — not pursued further here.
4. **The coefficient bounds `|c_i(k)|` and the `\hat G`/`\hat G_Θ` assembly
   are UNCHANGED from the predecessor** — still the same crude,
   triangle-inequality-based elementary bounds, with the same
   `\hatλ(γ)/λ(γ)` looseness factor (`\approx3$–$6\times`, per Estágio 36's
   correction) baked in. **Angle 2 of the dispatching mandate
   (exact-cancellation tracking in the coefficient bounds themselves, as
   opposed to the tail-probability step attacked here) was not attempted**
   — a distinct, separately-exploitable source of slack, left fully open.
5. **The `a\to0^+` "ideal" limit was not pushed to.** `C0_{\mathrm{Bernstein}}(γ,a)^2\to2σ^2(γ)(\hatλ(γ)+\frac12)`
   as `a\to0^+` (script `04`), the theoretical best this construction can
   give (still strictly better than Hoeffding for every `γ\ne1/2`, and
   *equal* to Hoeffding exactly at `γ=1/2` — never worse in the limit). The
   concrete `a=0.05` used in §5 leaves a small, disclosed gap to this ideal
   (visible in the `\sup=57.4` vs. ideal `\sup=56`, script `04`) —
   squeezing this further, or optimizing `a=a(γ)`, is a cheap, low-risk
   next increment, not attempted here for scope reasons.
6. **Angle 3 (a fundamentally different decomposition, bypassing tail
   bounds entirely — e.g. a direct combinatorial/generating-function
   argument, or a tight Taylor-remainder analysis) was not attempted.**
   Angle 1 alone already produced genuine, quantifiable, honestly-bounded
   progress, so this front did not need to reach for angle 3; whether it
   would do even better is unexamined.
7. **The exact Chernoff/relative-entropy bound for the Binomial tail**
   (`P(D\ge t)\le\exp(-k\cdot\mathrm{KL}(γ+t/k\,\|\,γ))`, strictly sharper
   than Bernstein, which is itself a relaxation of it) was considered but
   not pursued — it has no simple closed algebraic form (the relative
   entropy `\mathrm{KL}` is transcendental), which would have complicated
   the explicit-constant bookkeeping of §5 well beyond this front's scope;
   named here as a natural, likely-fruitful next step for a future front,
   consistent with the task's framing that even a partial improvement is
   the expected outcome at this difficulty tier.

---

## §8 Self-caught issues, disclosed

1. **Initial construction used the wrong asymptotic quantity.** The first
   pass computed `C0_{\mathrm{Hoeffding}}(γ)^2:=\frac14+\fracλ2` using the
   *tight* asymptotic `λ(γ)` (Estágio 36's own leading-order quantity)
   rather than `\hatλ(γ)` (the growth rate of the predecessor's own
   *explicit, crude* `\hat G(n,γ)` bound, which is what the fully assembled
   `n_0(γ)` construction actually depends on). This was caught immediately
   by the calibration check (§5): the naive Hoeffding re-implementation
   failed to find **any** crossover below `n=10^{200}` at `γ=0.99`
   (bisection assertion failure), wildly inconsistent with the
   predecessor's published `\sim10^{20.79}`. Root cause diagnosed by direct
   inspection (`\hat G(n,γ)/\ln n` empirically `\approx24.3` at `γ=0.99`,
   matching `\hatλ(0.99)=8(4·0.99-7)/(0.99(0.99-2))\approx24.32` exactly,
   not the tight `λ(0.99)\approx4.08`) — fixed by substituting `\hatλ`
   throughout; the calibration check then passed to `<0.01` decades at all
   8 points (§5).
2. **Initial slack choice `a=1` was worse than Hoeffding at 3 of 8 sample
   `γ` points** (`γ=0.7,0.5,0.3`, where `σ^2(γ)` is not far enough below
   `1/4` for the Bernstein gain to outweigh the `a=1` slack overhead) —
   found by direct side-by-side comparison (script `04`'s table), not
   assumed away. Diagnosed as a genuine, understood structural trade-off
   (§7 item 3, item 5), not a bug: as `a\to0^+`, the "worse" region shrinks
   to a single point (`γ=1/2`) with vanishing loss. Resolved by switching
   to `a=0.05` for the final construction (§5), which confines the loss to
   `-0.07` decades at exactly `γ=0.5` and none of the other 7 sampled
   points.
3. **The small-`k` residual term is NOT always negligible.** At `γ=0.99`
   specifically, the side-condition check (script `05`) found
   `\log(\text{small-}k\text{ term})\approx-0.04`, of comparable magnitude
   to `\log(\text{bulk+tail term})\approx-3.18` — not the "utterly
   negligible, many orders of magnitude smaller" behavior seen at the other
   7 sample points (where the gap is `>100` in log-scale). This does **not**
   invalidate the bound (both terms are correctly combined via
   `\mathrm{logsumexp}` before bisection, and the no-oscillation check,
   script `06`, independently confirms the resulting crossover at `γ=0.99`
   is genuine and durable) — but it means the "small-`k` region is
   asymptotically negligible" intuition (true in the `n\to\infty` limit,
   since `k_2=O(\ln n)\ll K_{\max}=O(\sqrt{n\ln n})`) is not yet the
   dominant regime at the specific, still-finite `n_0(0.99)\approx10^{17.7}`
   found here. Disclosed rather than silently smoothed over.

None of the three issues above affects the final reported numbers (all were
caught and resolved *before* the numbers in §5's tables were produced, via
the calibration check and direct comparison tables built for exactly this
purpose) — they are recorded here as part of this front's own working
discipline, in the same spirit as the self-caught-issue disclosures already
standard elsewhere in this lineage (e.g. the grandparent's script `03`
exponent-fitting bug, or the continuation's `\hatλ/λ` factor slip).

---

## §9 Scorecard

| Claim | Status |
|---|---|
| Bernstein's inequality, derived from scratch, matches exact Binomial tail with zero violations | **PROVED and verified** (§2/script `01`) |
| Bernstein dramatically sharper than Hoeffding pointwise away from `γ=1/2`; matches (loses, finite factor) only at `γ=1/2` | **CONFIRMED** (§2/script `01` Part C) |
| Slack-parameter construction gives a clean, `k`-uniform Bernstein tail bound for `k≥k_2(n,γ,C,a)=O(\ln n)` | **PROVED and verified** (§3/script `03`, zero violations) |
| `k_2\ll K_{\max}` at the astronomical `n`-scale this front's `n_0(γ)` needs | **CONFIRMED** (§3/script `03` Part D; §6/script `06` Part C) |
| `C0_{\mathrm{Bernstein}}(γ,a)^2` is exact-algebra-proved BOUNDED and strictly decreasing on the entire open interval `(0,1)`, for every fixed `a>0` | **PROVED** (§4/script `04`) — the flagship structural finding |
| A single `γ`-independent `C` suffices for all of `(0,1)` under Bernstein (vs. compact-subsets-only under Hoeffding) | **PROVED**, a bonus beyond the literal mandate (§4) |
| This front's independent re-implementation reproduces the predecessor's own published `C(γ)`, `n_0(γ)` table | **CONFIRMED**, `<0.01` decades discrepancy at all 8 points (§5/script `05`) |
| Coefficient bounds `\|c_i(k)\|` and `\hat G` assembly, independently re-verified (not re-derived) | **CONFIRMED**, zero violations, `715` grid points, `n` up to `10^{80}` (§5/script `02`) |
| NEW explicit `n_0(γ)`, Bernstein-based, at the same 8 sample `γ` | **COMPUTED and verified**, no spurious oscillation (§5–§6/scripts `05`–`06`) |
| Net improvement: `0.44`–`9.09` decades at 7/8 points, `-0.07` decades (understood, structural) at 1/8 | **QUANTIFIED PRECISELY** (§5) |
| Gap 1 (Taylor-remainder-with-moments bound) | **still NOT closed** — genuine partial improvement in `n_0(γ)`'s leading constant, not a closure |
| `C(γ)` for `γ∈(0,1)` (the ultimate target) | **NOT PROVED** — still fully open |

### Seeds table

| Block | Status |
|---|---|
| `20260914000–20260914999` (this front's reservation, `DISC-DEC-096`) | reserved; **zero seeds drawn** — every result is exact symbolic algebra (`sympy`, scripts `02`, `03` Part C, `04`) or deterministic high-precision numerics (`mpmath` dps=50–60, exact pmf summation or exact closed-form evaluation, scripts `01`, `02`, `03`, `05`, `06`) — disclosed as unused, not silently abandoned |

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_bernstein_inequality.py` / `.log` | from-scratch elementary derivation of Bernstein's inequality (MGF/Chernoff argument); independent numerical verification against the exact Binomial tail (mpmath dps=50, zero violations); pointwise comparison against Hoeffding across `γ` |
| `02_cubic_and_coefficient_bounds.py` / `.log` | fresh symbolic re-derivation of `x(D)`'s exact cubic form (two independent routes, matches the grandparent's corrected `c_0` exactly); independent numerical re-verification of the predecessor's cited elementary coefficient bounds (715 grid points, `n` up to `10^{80}`, zero violations); fresh re-assembly of `\hat G(n,γ)`, cross-checked to match the continuation's stated closed form exactly |
| `03_k_uniform_bernstein_split.py` / `.log` | the slack-parameter construction making Bernstein's tail bound `k`-uniform; sufficient-condition verification; clean-bound-vs-exact-pmf verification; the `s(k)` minimum calculus fact; `k_2` vs. `K_max` scale check at the astronomical `n` this front's own construction needs |
| `04_C0_bernstein_boundedness.py` / `.log` | the flagship finding: exact-algebra proof that `C0_Bernstein(γ,a)²` is bounded and monotone decreasing on all of `(0,1)`, for every fixed `a>0`; comparison table against `C0_Hoeffding(γ)²`; calibration sanity check against the predecessor's published `C(γ)` |
| `05_final_assembly_and_n0_bisection.py` / `.log` | full explicit `W(n,γ,C[,a])` assembly for both Hoeffding and Bernstein; calibration check against the predecessor's published table; the main OLD-vs-NEW `n_0(γ)` bisection results at all 8 sample `γ`; side-condition sanity checks |
| `06_monotonicity_and_side_conditions.py` / `.log` | no-spurious-oscillation check (40 decades beyond each crossover, both constructions); `k_2/K_max` monotone-shrinking check beyond the tightest crossover (`γ=0.99`) |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
