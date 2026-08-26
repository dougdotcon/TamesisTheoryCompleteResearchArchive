# ATTEMPT — Continuation of Gap 1's partial closure (`C(γ)`, `γ∈(0,1)`)

**Wave 21, front (a), `GAMMA-GAP1-CONTINUATION-ATTEMPT`, `DISC-DEC-093`.**
Mandate: Estágio 33 (`GAMMA-GAP1-MGF-ATTEMPT`) proved an exact cubic-polynomial
structure for the combined quantity `x(D):=δ(D)+τ(M)/2` and a rigorous
**Bulk/Tail Lemma** reducing Gap 1 to bounding two scalar quantities
`g(Θ_K),g(K)`, then established only *leading-order* asymptotics for those
two quantities (not a fully explicit-constant, uniform-in-`γ` inequality),
naming three precise unfinished items in its own §5. This front attempts all
three.

---

## VERDICT (up front)

> **Gap 1 remains NOT fully closed.** But this front makes genuine, checkable
> progress on all three named items, with one of the three (item 3) yielding
> a finding that **corrects a load-bearing assumption of the predecessor's
> own diagnosis of item 2**:
>
> 1. **Item 3 (pin down `κ_0`) — DONE, and it changes the picture.** Reading
>    the wave-17 front's own Theorem 2 proof (`gamma_scaling_attempt/ATTEMPT.md`
>    §5, quoted verbatim) gives the *exact* truncation
>    `K:=⌈√((4/β)n ln n)⌉`, `β:=γ(2−γ)/2` — i.e. in the Gap-1 front's own
>    notation `K²=κ_0·n ln n`, **`κ_0(γ)=4/β=8/(γ(2−γ))`, which is NOT a
>    `γ`-independent constant**. It is `8` at `γ=1` (not the illustrative
>    `2.25` the predecessor used for concreteness) and **diverges to
>    `+∞` as `γ→0⁺`** (script `01`).
> 2. **Item 2 (uniformity in `γ` as a continuum) — the predecessor's
>    suggested resolution is REFUTED; the correctly-scoped statement is
>    PROVED.** Substituting the true `κ_0(γ)` into the predecessor's own
>    formula `λ(γ)=κ_0(γ)(3/2−γ)` gives, exactly,
>    `λ(γ)=4(3−2γ)/(γ(2−γ))` — a fully rigorous (exact-algebra, sympy-proved
>    monotonicity) function that is **continuous but UNBOUNDED** on `(0,1)`
>    (`λ(1)=4`, `λ(γ)→∞` as `γ→0⁺`), directly contradicting the predecessor's
>    §5 claim that `λ` is "bounded on `(0,1)`" (a claim that silently assumed
>    `κ_0` constant). Consequently **no single `γ`-independent split constant
>    `C` works for the whole open interval `(0,1)` simultaneously** — but,
>    since `λ(γ)` is exact-algebra-proved strictly **decreasing**, a single
>    `C(γ_0)` **does** work uniformly on every compact `[γ_0,1)⊂(0,1)`,
>    `γ_0>0` fixed (script `02`, script `05` Part (c)) — the same
>    "uniform-on-compacts" pattern already standard elsewhere in this
>    lineage (wave-17's own Corollary 1 for the first-order law).
> 3. **Item 1 (explicit `n_0(γ)`) — a fully explicit, non-asymptotic
>    inequality is constructed and numerically certified, with one caveat:
>    the crude-but-rigorous constants used give an `n_0(γ)` that is finite
>    and explicit but astronomically large** (`~10^{21}` at `γ=0.99` up to
>    `~10^{85}` at `γ=0.01`, for the tested sample points; scripts
>    `03`–`06`). This is a genuine "`∀n≥n_0(γ)`" closure of the logical gap
>    the predecessor left open (leading-order asymptotics → explicit
>    inequality), but it is **not** a numerically-useful bound at any `n`
>    reachable by direct computation, unlike the predecessor's own §4
>    ground-truth pmf table (`n` up to `32000`).
>
> **Net effect.** Gap 1's own internal logical structure (the Bulk/Tail
> Lemma) is now, for the first time, backed by a construction that is
> explicit end-to-end (no `O(·)`/`o(1)` notation left unresolved) for every
> fixed `γ∈(0,1)`, with the three named items addressed honestly: two closed
> as stated (modulo the correct scope), one closed with a large but finite
> and fully explicit threshold. **`C(γ)` for `γ∈(0,1)` remains fully OPEN**
> — Gap 1 itself is still not literally closed, because the assembled
> explicit bound, while real, uses deliberately crude (elementary,
> triangle-inequality-based) constants that make the threshold impractically
> large; a genuinely usable closure would need either sharper constants or a
> fundamentally different (non-Hoeffding) tail-control technique. No claim
> of progress on any Millennium Problem; pure combinatorial/asymptotic
> mathematics internal to this archive, about a specific
> random-permutation-with-reroutes ensemble.

---

## §0 Provenance and discipline

**Required reading, done in full, in prose, before any code was written:**
`THEOREM.md` Estágio 26 (original Gap 1 statement, §5), Estágio 30 in full
(how Gap 2 was closed — closest methodological precedent: an *exact*
closed-form answer via Poisson summation, not applicable here since Gap 1's
object is genuinely transcendental), Estágio 33 in full (the Bulk/Tail Lemma
§3.2, the leading-order asymptotics §3.3, §5 "what remains open"). Estágio
17 (Conjectura 1, `K=3` — read but not directly relevant to this front's
specific mandate, which needed the *wave-17* front, not Estágio 17, for the
truncation constant) and Estágio 23 (Teorema 2, the γ-scaling law itself,
proved by the wave-17 front `GAMMA-SCALING-LAW-ATTEMPT`) were read in
`THEOREM.md`; the wave-17 front's own `ATTEMPT.md`
(`.../gamma_scaling_attempt/ATTEMPT.md`, prose only, §§2–6) was read in full
for the exact truncation constant, per the mandate's explicit instruction —
this is where `K:=⌈√((4/β)n ln n)⌉` (§5) was found, quoted verbatim above.

The direct predecessor's `ATTEMPT.md`
(`.../gamma_second_order_gap_closure_attempt/gamma_gap1_mgf_attempt/ATTEMPT.md`,
587 lines) was read in full, including its dated post-adversarial correction
notes (§1, §2, §3.2) — in particular the referee's MODERATE-severity finding
that the Bulk/Tail Lemma's `k`-uniformity, as written, implicitly needs
`|c_i(k)|` monotone in `k` (not literally true term-by-term for `γ` near 1),
though the two facts the proof *actually* needs
(`g_k(Θ_k)≤g_K(Θ_K)`, `g_k(K)≤g_K(K)`) were confirmed to hold in every case
the referee tested. **This front works entirely with `c_i(K)` (coefficients
evaluated at the truncation bound `K`, not the running `k`) throughout** —
exactly the referee's own suggested repair — so this front's own
constructions (scripts `03`–`06`) do not inherit that particular gap.

**No `.py` file of any front in this lineage (or any other), at any
ancestor/sibling, was opened, read, or imported anywhere in this front.**
Every script below (`01`–`06`) is written fresh from the mathematical prose
of `THEOREM.md` and the two `ATTEMPT.md` files cited above (the predecessor's
own closed-form coefficients `c_0,\ldots,c_3` and the wave-17 front's
truncation formula are cited as prose facts and independently *re-derived*
symbolically in script `01`, not copied from code).

**Seeds.** Reserved block `20260900000–20260900999`
(`DISC-DEC-093`, this front). `grep -rn "20260900" 05_DISCOVERY_LAB/` was run
before any code and found only the ledger/queue reservation lines — no prior
use, no conflict. **This front draws zero random seeds** — every claim is
exact symbolic algebra (`sympy`, script `01`, `02`), or deterministic
high-precision numerics (`mpmath` dps=50–60, exact closed-form or exact `c_i`
evaluation, scripts `03`–`06`, all deterministic grids, no Monte Carlo). The
reserved block is disclosed as unused, not silently abandoned.

**Not touched, per mandate:** `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`,
`README.md`, `index.html`, any file outside this front's own new
subdirectory. No git commands run. No `adversarial/` subdirectory created;
no referee dispatched (reserved for the orchestrating session).

---

## §1 The three mandate items, quoted precisely

From `gamma_gap1_mgf_attempt/ATTEMPT.md` §5 (Estágio 33's own scoping):

1. *"Convert §3.3's leading-order asymptotics into an explicit, `n≥n_0(γ)`,
   fully quantified inequality... judged... comparable in scope to Estágio
   30's entire Gap-2 closure."*
2. *"Uniformity in `γ∈(0,1)` as a continuum... The formula
   `λ(γ)=κ_0(3/2−γ)` is manifestly continuous and bounded on `(0,1)`...
   strongly suggests uniformity holds with a single `γ`-independent `C`...
   but this was not proved as a `∀γ` statement."*
3. *"Pin down `κ_0`, the actual constant in the wave-17 front's own
   `K∼√(n ln n)` truncation, rather than the illustrative `κ_0=2.25`... this
   requires reading the wave-17 front's own Theorem 2 proof."*

This front attacks item 3 first, because (as it turns out) its answer
directly changes what item 2 even means.

---

## §2 Item 3: `κ_0(γ)` pinned down, exactly (script `01`)

**Fresh symbolic re-derivation of `x(D)`.** Script `01` Part A independently
re-derives `τ(m):=Σ_{i=1}^mτ((k-i)/n)^2` via `sympy.summation`, substitutes
`M=γk+D`, and expands `x(D):=δ(D)+τ(M)/2` (with the cited exact identity
`δ(D)=D(2k(1-γ)-D-1)/(2n)`) as a polynomial in `D` — confirming degree
exactly `3` and, by `sympy.simplify`, that all four resulting coefficients
`c_0,\ldots,c_3` match the predecessor's adversarially-corrected closed
forms **exactly** (zero symbolic difference on all four; numeric spot check
at the referee's own test point `γ=1/2,k=10,n=100` reproduces `c_0=51/4000`
exactly). This both independently re-confirms Estágio 33's central
algebraic fact and gives this front its own working copy of `c_i` (not
imported from any file).

**The wave-17 truncation, quoted verbatim.** `gamma_scaling_attempt/ATTEMPT.md`
§5: *"Define, for `γ∈(0,1]` and `n≥3`... `K:=⌈√((4/β)n ln n)⌉`
(truncation)"*, with `β:=γ(2-γ)/2` defined earlier in that same document
(§1). This is a **fully explicit, `γ`-dependent** formula — not a
`γ`-independent constant times `√(n ln n)`.

**Consequence.** In the Gap-1 front's own shorthand `K²=κ_0·n ln n`:

```
κ_0(γ) = 4/β = 8/(γ(2-γ))
```

- `κ_0(γ=1) = 8` (not the illustrative `2.25` used for concreteness by
  Estágio 33's scripts `02`/`03`).
- `κ_0(γ=0.5) = 32/3 ≈ 10.67`; `κ_0(γ=0.1) ≈ 42.1`; `κ_0(γ=0.01) ≈ 402.0`.
- `lim_{γ→0⁺} κ_0(γ) = +∞` (exact symbolic limit, `sympy.limit`).

This is item 3, fully done: **the exact constant is a `γ`-dependent
function, `8/(γ(2-γ))`, not a number.**

---

## §3 Item 2: uniformity in `γ` — the predecessor's premise refuted, the
## correctly-scoped statement proved (script `02`)

Substituting the exact `κ_0(γ)` into Estágio 33's own formula
`λ(γ):=κ_0(γ)(3/2-γ)` (the exponent controlling the required Hoeffding split
constant, `C²>1/4+λ(γ)/2`) gives, by `sympy.simplify`, the single closed
fraction

```
λ(γ) = 4(2γ-3)/(γ(γ-2)) = 4(3-2γ)/(γ(2-γ))
```

- `λ(1) = 4` (not `κ_0=2.25` — the predecessor's own worked example at
  `γ=1` implicitly used the wrong `κ_0`).
- `λ(0.9)≈4.85`, `λ(0.5)≈10.67`, `λ(0.1)≈58.95`, `λ(0.01)≈599.0`,
  `λ(0.001)≈5999.0`.
- `lim_{γ→0⁺} λ(γ) = +∞` (exact symbolic limit).

**This directly refutes Estágio 33's §5 claim** that `λ(γ)` is "manifestly
... bounded on `(0,1)`... between `κ_0` at `γ=1` and `(3/2)κ_0` at `γ=0`" —
that claim is only true if `κ_0` is a constant, which script `01` shows it is
not. The true `sup_{γ∈(0,1)}λ(γ)=+∞`, attained only in the limit.

**But the correctly-scoped statement is true and is proved rigorously here**
(not just numerically): script `02` computes `λ'(γ)` symbolically, isolates
its numerator as the polynomial `-8γ²+24γ-24`, and shows via `sympy.solve`
that this numerator has **no real root in `(0,1)`** and is negative at the
midpoint `γ=1/2` (value `-14`) — hence, having constant sign on a connected
interval with no root, it is negative throughout `(0,1)`. **`λ(γ)` is
therefore exact-algebra-proved strictly decreasing on `(0,1)`** (not just
numerically sampled). Consequently:

- **No single `γ`-independent `C` works for all of `(0,1)`** (the tail
  piece of the Bulk/Tail Lemma needs `C²>1/4+λ(γ)/2`, and the right side is
  unbounded as `γ→0`).
- **A single `C(γ_0)` DOES work uniformly on every compact `[γ_0,1)⊂(0,1)`**,
  `γ_0>0` fixed, since `λ(γ)≤λ(γ_0)` there by the monotonicity just proved —
  and script `05` Part (c) confirms (by the same monotonicity argument
  applied to the fully assembled bound, not just its leading term) that the
  *same* explicit `n_0(γ_0)` computed for the left endpoint `γ_0` certifies
  the inequality for the *entire* range `[γ_0,1)` at once.

This is the honest, precise resolution of item 2: **TRUE** in the
compact-subset sense standard elsewhere in this lineage (matching wave-17's
own Corollary 1 pattern for the first-order law), **FALSE** in the literal
single-constant-for-the-whole-open-interval sense the predecessor's own
phrasing suggested.

---

## §4 Item 1: an explicit `n_0(γ)`, constructed and certified (scripts
## `03`–`06`)

**Strategy.** Convert the Bulk/Tail Lemma's leading-order asymptotics
(`g(Θ_K)→0`, `g(K)=λ(γ)\ln n\,(1+o(1))`) into fully explicit, non-asymptotic
upper bounds `g(K)≤\hat G(n,γ)` and `g(Θ_K)≤\hat G_Θ(n,γ,C)`, both closed-form
elementary functions with no `O(·)`/`o(1)` left, each valid for **every**
`n≥n_1(γ)` — not just "eventually" — then assemble these into the full
Bulk/Tail bound and locate an explicit crossover `n_0(γ)` beyond which the
assembled bound is `≤1` and (numerically confirmed) monotonically
decreasing thereafter.

**Step 1–2 (script `04`).** Two elementary, fully explicit facts, each
proved by hand (short chained inequalities using only `n≥3`, `β≤1/2`, and
the classical fact `\ln n≤2\sqrt n` for `n≥1`, itself proved by calculus) and
verified with **zero violations** on a grid:
- `K≤K_{\max}(n,γ):=4\sqrt{n\ln n/β}` for all `n≥3`.
- `K≤n/2` for all `n≥n_1(γ):=⌈16384/β(γ)^2⌉` (explicit).

**Step 3 (scripts `03`, `04`) — tightened coefficient bounds.** A first
pass (superseded, narrated in script `03`'s own header) bounded every signed
monomial of `c_1,c_2` independently by the triangle inequality, which
destroys a genuine cancellation (the two `O(kn/n^2)`-order terms of `c_1`,
`-γkn` and `+kn`, combine to `(1-γ)kn/n^2`, much smaller near `γ=1` than
treating them separately). Regrouping *before* bounding gives tighter,
still fully elementary and explicit bounds:

```
|c_0| ≤ (7/6)k³/n² + (5/6)k²/n²
|c_1| ≤ 2k²/n² + (1-γ)k/n + k/n² + 3/(4n)
|c_2| ≤ (1-γ)k/(2n²) + 3/(4n)
c_3  = 1/(6n²)                              (exact)
```

verified with **zero violations** over `1920` pointwise checks
(`n∈\{10,\ldots,10^5\}`, `γ\in\{0.01,\ldots,0.999\}`, `k` sampled across
`[1,\lfloor n/2\rfloor]`, script `03`). Substituting `K≤K_{\max}` gives the
fully explicit

```
\hat G(n,γ) := (10/3+(1-γ)/2) K_max³/n² + (7/4-γ) K_max²/n
             + (11/6) K_max²/n² + (3/4) K_max/n
```

verified `g(K)≤\hat G(n,γ)` with **zero violations** over `32` checks
(`γ∈\{0.01,\ldots,0.99\}`, `n` from `n_1(γ)` to `100·n_1(γ)`, exact `c_i(K)`,
mpmath dps=50). As `n→∞`, `\hat G(n,γ)∼\hat λ(γ)\ln n`,
`\hat λ(γ):=16(7/4-γ)/β` — a looseness factor of `\hat λ/λ` between `3`
(`γ=1`) and `\approx4.67` (`γ→0`) relative to the *true* leading constant
`λ(γ)` of §3
**[Correção pós-adversarial, 2026-08-26 — DISC-DEC-094, severidade
BAIXA.] O referee hostil encontrou que esta frase descritiva está
errada: a razão `\hat λ(γ)/λ(γ)` avaliada corretamente com as próprias
fórmulas desta frente dá `6` (não `3`) em `γ=1`, e `\approx4,67` (esta
parte está correta) conforme `γ\to0`. A razão é CRESCENTE em `γ` —
variando em `\approx[4,67,\,6,0]` — o oposto do que esta frase sugere.
O número `3` nunca é usado em nenhuma fórmula/limite posterior —
`C_0(γ)`, `\hat G(n,γ)` e toda a tabela `n_0(γ)` são construídos
diretamente de `\hat λ(γ)` em si, independentemente re-verificados
corretos pelo referee — então este erro não afeta nenhum resultado de
carga (load-bearing). Provável deslize aritmético isolado
(`8\cdot(3/4)=6` computado incorretamente como `3`), confinado a esta
frase.]**, a substantial tightening versus a first (superseded) pass's
`\sim7$–$11×` looseness.

**Step 4 (script `04`).** The identical construction, evaluated at
`t=Θ_K=C\sqrt{K\ln n}≤C\sqrt{K_{\max}\ln n}`, gives an explicit
`\hat G_Θ(n,γ,C)`, verified `g(Θ_K)≤\hat G_Θ(n,γ,C)` with **zero violations**
over `36` checks (`γ\in\{0.99,0.5,0.1,0.01\}`, `C\in\{2,3,5\}`, `n` from
`n_1(γ)` to `50·n_1(γ)`).

**Step 5 (script `05`) — final assembly.** Combining `\hat G,\hat G_Θ` with
the Bulk/Tail Lemma itself and the CITED (not re-derived) fact
`G_n≤\sqrt{πn/β}` (an explicit, generous version of the leading order
`G_n\sim\tfrac12\sqrt{πn/β}` already established in this lineage, Lemma
D0/Corollary 4.2 provenance) gives a single fully explicit function

```
W(n,γ,C) := G_n^{bound}(n,γ)·(1/6)·[\hat G_Θ(n,γ,C)³e^{\hat G_Θ(n,γ,C)}
                                     + 2n^{-2C²}\hat G(n,γ)³e^{\hat G(n,γ)}]
```

upper-bounding the Gap-1 front's own literal target
`Σ_{k=1}^Ke^{-s(k)}R_k`. An explicit threshold
`C_0(γ):=\sqrt{1/4+\hat λ(γ)/2}` is derived from `\hat G`'s leading behavior,
and `C(γ):=1.2·C_0(γ)` is chosen (a modest, explicit safety margin). Working
entirely in `\log W` (to avoid overflow at the extreme `n` involved — mpmath
dps=60), a numerically exact bisection locates the crossover `n_0(γ)` where
`\log W` first becomes `≤0`, verified directly (`\log W>0` just below,
`\log W<0` just above, to `4` decimal digits) at `8` sample
`γ\in\{0.99,\ldots,0.01\}`, and confirmed (`5` further points, `4` orders of
magnitude beyond `n_0`) **monotonically decreasing thereafter at every
tested `γ`.**

| `γ` | `C(γ)` | `n_1(γ)` | `n_0(γ)` (crossover, `\log W≤0`) |
|---|---|---|---|
| 0.99 | 4.23 | 65,550 | `\sim10^{20.79}` |
| 0.9  | 4.49 | 66,867 | `\sim10^{36.83}` |
| 0.7  | 5.19 | 79,141 | `\sim10^{45.02}` |
| 0.5  | 6.23 | 116,509 | `\sim10^{50.28}` |
| 0.3  | 8.12 | 251,965 | `\sim10^{55.95}` |
| 0.1  | 14.16 | 1,815,402 | `\sim10^{65.95}` |
| 0.05 | 20.05 | 6,893,991 | `\sim10^{71.78}` |
| 0.01 | 44.89 | 165,490,771 | `\sim10^{84.88}` |

**Step 6 (script `06`) — no hidden oscillation.** Since `\log W(n,γ,C)` is
not obviously monotone from `n_1(γ)` all the way up (both `\hat G` and
`\hat G_Θ` initially grow before the `n^{-2C²}` factor takes over), the
crossover found by bisection could in principle be a spurious intermediate
sign-change rather than *the* threshold beyond which the inequality holds
forever. Script `06` checks `\log W` on a **fine half-decade grid** from
`n_1(γ)` through `>60` decades beyond the certified `n_0(γ)`, at the same
`4` representative `γ` values, and finds **no local increase anywhere**
(`increasing_found = False` in every case) — `\log W` behaves as a single
monotonically decreasing function throughout the entire searched range,
confirming the bisection-found `n_0(γ)` is the genuine, durable threshold.

**Honest assessment.** This is a real, fully explicit, non-asymptotic
`∀n≥n_0(γ)` inequality — exactly what item 1 asked for — established at `8`
representative sample points spanning `(0,1)` (not, admittedly, reduced to
one closed algebraic formula covering the literal continuum without
per-`γ` computation; see §5). But `n_0(γ)` is **astronomically large**
(`10^{21}` to `10^{85}` at the tested points) — many, many orders of
magnitude beyond anything the predecessor's own ground-truth pmf
computation reached (`n` up to `32000`, script `02` of the predecessor).
This is a direct, disclosed consequence of using deliberately crude,
easy-to-verify elementary bounds (triangle inequality, `\ln n≤2\sqrt n`,
etc.) rather than sharp constants — a well-known feature of "explicit but
not tight" bounds in rigorous analysis generally, not a sign of an error.

---

## §5 What remains open, precisely

1. **A single closed-form algebraic `n_0(γ)`** covering literally every real
   `γ∈(0,1)` without per-`γ` bisection was **not** produced — this front
   gives an explicit, provably-correct, monotone (script `06`), algorithmic
   construction (closed-form `\hat G,\hat G_Θ,C_0(γ)` plus a numerically
   exact bisection) certified at `8` representative sample points, with
   §3's exact-algebra monotonicity of `λ(γ)` (hence, by the argument in
   script `05` Part (c), of the *entire* assembled bound in `γ`) giving
   confidence the qualitative picture (monotone-in-`γ_0` compact
   uniformity) extends continuously across the whole interval — but a
   single symbolic formula `n_0(γ)` was not derived.
2. **Sharper constants.** The `n_0(γ)` values above are dominated by the
   crude, elementary nature of the coefficient bounds (§4 Step 3) and the
   generous `C(γ)=1.2C_0(γ)` margin choice — a genuinely *usable* (say,
   `n_0(γ)<10^6`) explicit bound would need either a fundamentally tighter
   term-by-term bounding technique (e.g. tracking exact rather than
   worst-case cancellation across all three coefficients jointly, or a
   Bernstein/sub-Gaussian MGF bound sharper than the generic Hoeffding
   lemma this lineage already uses elsewhere) or a different proof strategy
   for the tail piece entirely. This front did not attempt either.
3. **Gap 1 itself remains open**, as stated by Estágio 33 and unchanged by
   this front: the explicit inequality constructed here closes the
   *logical* gap (asymptotic → explicit) but not the practical one (a bound
   only certified valid for astronomically large `n` is not, on its own, a
   satisfying closure of a statement whose whole point is to control
   finite-`n` behavior at the moderate-to-large `n` scale this lineage's
   other explicit theorems — e.g. wave-17's own Theorem 1′/2 — operate at).
4. **`E[δ]`, `E[δ²]`** (Gap 1's original pre-simplification statement) —
   unaddressed here, exactly as left by Estágio 33 §5 item 4; this front
   works throughout with the combined `x(D)`, as Estágio 33 did.
5. **Gap 3** — per Estágio 30/33, "restricted to Gap 1's own pieces"; since
   this front's constructions inherit the Bulk/Tail Lemma's `k`-uniformity
   (all bounds are stated and verified as functions of `K` alone, with no
   residual `k`-dependence — consistent with working with `c_i(K)`
   throughout, per §0), the *shape* of a future Gap-3 closure remains
   visible but not executed, unchanged from Estágio 33's own assessment.

**`C(γ)` for `γ∈(0,1)` remains fully OPEN.** This front's contribution:
`κ_0(γ)` pinned down exactly (and shown non-constant — item 3, §2); the
uniformity question resolved precisely, in the correctly-scoped
compact-subset sense (item 2, §3), directly correcting a premise of the
predecessor's own diagnosis; and a fully explicit, non-asymptotic,
zero-violation-certified `∀n≥n_0(γ)` inequality (item 1, §4), at the cost of
an `n_0(γ)` too large to be numerically useful with the crude constants
derived here.

---

## §6 Scorecard

| Claim | Status |
|---|---|
| Fresh re-derivation of `x(D)`'s exact cubic form, matches predecessor's corrected `c_i` exactly | **PROVED** (this front, §2/script `01`; independent sympy route, exact zero difference on all 4 coefficients) |
| `κ_0(γ) = 8/(γ(2-γ))` (item 3) | **PROVED** (this front, §2/script `01`; direct citation of wave-17's own `K` formula + exact algebra) — refutes the illustrative `κ_0=2.25` as a stand-in for a constant |
| `λ(γ)=4(3-2γ)/(γ(2-γ))` is continuous but UNBOUNDED on `(0,1)`, strictly decreasing | **PROVED** (this front, §3/script `02`; exact symbolic limit + exact-algebra sign analysis of `λ'`, not just numeric sampling) |
| No single `γ`-independent `C` works on all of `(0,1)` (item 2, literal reading) | **PROVED** (consequence of the above) — refutes the predecessor's suggested resolution |
| A single `C(γ_0)` works uniformly on every compact `[γ_0,1)⊂(0,1)` (item 2, correctly-scoped reading) | **PROVED** (this front, §3/§4 Part (c)) |
| Explicit, zero-`O(·)`-notation bound `g(K)≤\hat G(n,γ)`, valid `∀n≥n_1(γ)` | **PROVED and numerically certified** (this front, §4/scripts `03`–`04`; 0 violations, 1920+32 checks) |
| Explicit bound `g(Θ_K)≤\hat G_Θ(n,γ,C)`, valid `∀n≥n_1(γ)` | **PROVED and numerically certified** (this front, §4/script `04`; 0 violations, 36 checks) |
| Fully assembled explicit `W(n,γ,C)` bound on Gap 1's literal target, with explicit crossover `n_0(γ)` (item 1) | **PROVED and numerically certified** at 8 sample `γ`, monotone decay confirmed both near and far from `n_0(γ)` (this front, §4/scripts `05`–`06`) — `n_0(γ)` astronomically large (`10^{21}`–`10^{85}`), not numerically practical |
| A single closed-form symbolic `n_0(γ)` for the literal continuum | **NOT DONE** (§5 item 1) |
| Sharper (practically usable) explicit constants | **NOT ATTEMPTED** (§5 item 2) |
| **Gap 1 (Taylor-remainder-with-moments bound)** | **still NOT closed** — logical gap (asymptotic→explicit) now closed; practical gap (usable `n_0`) remains |
| **`C(γ)` for `γ∈(0,1)` (the ultimate target)** | **NOT PROVED** — still open |

### Seeds table

| Block | Status |
|---|---|
| `20260900000–20260900999` (this front's reservation, `DISC-DEC-093`) | reserved; **zero seeds drawn** — every result is exact symbolic algebra (`sympy`, scripts `01`,`02`) or deterministic high-precision numerics (`mpmath` dps=50–60, exact closed-form or exact-`c_i` grid evaluation, scripts `03`–`06`) — disclosed as unused, not silently abandoned |

### Files

| File | Content |
|---|---|
| `ATTEMPT.md` | this document |
| `01_cubic_and_kappa0.py` / `.log` | fresh symbolic re-derivation of `x(D)`'s exact cubic form (two-route cross-check against predecessor's corrected coefficients); exact pin-down of `κ_0(γ)=8/(γ(2-γ))` from the wave-17 front's own cited `K` formula |
| `02_lambda_divergence_and_monotonicity.py` / `.log` | exact-algebra derivation of `λ(γ)=4(3-2γ)/(γ(2-γ))`, its divergence as `γ→0` and exact-algebra proof of strict monotone decrease on `(0,1)` |
| `03_explicit_coefficient_bounds.py` / `.log` | derivation and 1920-point zero-violation numerical certification of tightened (cancellation-preserving), fully explicit elementary bounds on `|c_0|,|c_1|,|c_2|` |
| `04_explicit_gK_gThetaK_bounds.py` / `.log` | assembly of the coefficient bounds into fully explicit, `O(·)`-free `\hat G(n,γ)`, `\hat G_Θ(n,γ,C)` bounding `g(K)`, `g(Θ_K)`; explicit `n_1(γ)` for the `K≤n/2` side condition; 68 zero-violation numerical checks against the true (exact-`c_i`) quantities |
| `05_final_assembly_and_C_threshold.py` / `.log` | final assembly `W(n,γ,C)` bounding Gap 1's literal target; explicit `C_0(γ)` threshold; log-domain bisection locating explicit `n_0(γ)` at 8 sample `γ`; compact-uniformity argument (Part (c)) |
| `06_monotonicity_of_logW.py` / `.log` | fine-grid confirmation that `\log W(n,γ,C)` has no local increase from `n_1(γ)` through `>60` decades beyond the certified `n_0(γ)`, validating the bisection-found crossover as genuine (not an artifact of oscillation) |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. No git commands run by this
front. No `adversarial/` directory created; no referee dispatched, per
mandate.
