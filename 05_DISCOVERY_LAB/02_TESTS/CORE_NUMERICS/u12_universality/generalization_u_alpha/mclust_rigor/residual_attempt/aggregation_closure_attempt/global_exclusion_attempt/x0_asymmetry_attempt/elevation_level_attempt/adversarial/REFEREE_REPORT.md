# REFEREE REPORT — adversarial review of `elevation_level_attempt/ATTEMPT.md`

**Wave 10, `DISC-DEC-045`, front (a) `MCLUST-ELEVATION-LEVEL-ATTEMPT`, mandatory
independent adversarial verification.**

Object under test: `elevation_level_attempt/ATTEMPT.md` (§0–14) together with its
pre-registration `elevation_level_attempt/DERIVATION_PREREG.md`. Both were read
in full before any line of code in this folder was written. The claim under test
is a candidate replacement for the formula of record `φ_EPSR` (`DISC-DEC-044`).

**Scope and discipline.** Everything produced by this review lives in
`elevation_level_attempt/adversarial/`. No file outside it was created, modified
or touched — not `ATTEMPT.md`, not `DERIVATION_PREREG.md`, not any predecessor
`ATTEMPT.md`/`REFEREE_REPORT.md`, not `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, `DERIVATIONS.md`,
`DERIVATION_MCLUST_FIXED.md`, any `README*`, `PROOF_DEPENDENCY_MAP.md`, or
`tamesis-cycle-survival/`. **No git commit was created.** Integration is the
orchestrating session's business.

**Independence.** Every script here (`ref2_*.py`) was written from scratch from
the mechanism as stated in the primary sources (`DERIVATIONS.md` §0–1 and §3.1/
§3.5; `DERIVATION_MCLUST_FIXED.md` §1–4; the predecessor referee report §4.1 for
the `H(t)` closed form and the two `eps` channels). **No `.py` file of the target
front was read at any point** — not `elev_formula.py`, `elev_mc.py`,
`elev_pool_probe.py`, `elev_reduction.py`, `elev_validate.py`,
`elev_triage_recorded.py`, `elev_analysis.py`, nor their drivers — and none of
them is imported. No `ref_*.py` of the predecessor `adversarial/` review was
read or imported either. Only the prose of `ATTEMPT.md` and
`DERIVATION_PREREG.md`, and the numbers printed in their tables, were used.

**Fresh seeds**, verified by `grep` over the whole archive to be unused
anywhere (the archive's used values run to `20260823xxx`; this review uses
`20260824xxx`):

| seed | use |
|---|---|
| `SeedSequence(20260824901–902)` | `ref2_mc.py selftest`, exposure-density checks |
| `SeedSequence(20260824911–919)` | `ref2_walk.py`, the nine T1/T2 probe cells |
| `SeedSequence(20260824920–937)` | `ref2_reduction.py`, the 18 reduction jobs |
| `SeedSequence(20260824940–963)` | `ref2_grid.py`, the fresh 24-cell φ grid |
| `SeedSequence(20260824950)` | `ref2_pool_moments.py` |
| `SeedSequence(20260824985–999)` | debugging / cross-validation runs (labelled) |

---

## 0. VERDICT — split across sub-claims

### Mechanism (T1/T2, §4) → **CONFIRMED**

The constant-elevation ansatz is refuted at the mechanism level, with no formula
involved (χ² = 1925/67 bins) — an independent reproduction of the target's own
headline result. The proposed replacement mechanism, hazard = 1/(pool), is
confirmed to ≈0.2% per cell with 0 audit failures in 5.91×10⁸ steps. This is the
strongest, most decisive evidence in the review, and it does not depend on any
χ² table.

### Reduction (T3, §5) → **STATED FORM REFUTED; CORRECTED FORM MUCH BETTER, NOT PERFECT**

At 300 000/400 000 instances per job — 7.5× the target's precision, now complete
across all 6 pre-registered cells — the reduction as literally stated in (4.1) is
refuted, with the discrepancy growing sharply with ρ and c/n (pooled χ² = 334.6
vs the measured M-U(A); 420.1 vs the continuum form (4.2) the target actually
uses). The corrected parameters of §11 (φ_REDB, c″ = c(1−c/n)^{b−1}) cut the
pooled χ² by ≈3.3× to 101.4 (continuum 123.3) and bring five of the six cells to
|z| ≤ 1.5. But the fix is not complete: the sixth and most extreme cell (b=100,
c=1000, ρ=0.785, the highest c/n tested) alone supplies ≈96% of the corrected
pooled χ², with the corrected form still off by 1.2–1.3% (z ≈ 10) — larger than
the ≈0.77% parameter-shift §5.1 estimates for that cell, so a real residual
beyond the O(c/n) correction survives at extreme parameters, consistent with
§3.2's and §9.4's own note that an unmodelled effect remains there. Everything
qualitative in §2–§4 of the target survives the correction; only φ_U's argument
changes.

### χ²-table evidence (target's own §9/§10) → **SUPPORTING, NOT DECISIVE**

A one-parameter fitted null family cannot beat χ² ≈ 215 in-sample (§8); the
zero-parameter φ_RED reaches 64.9 and the corrected φ_REDB reaches 46.0 — a
real, shape-specific gain. But this evidence folds the elevation model together
with the eps model and quadrature, so it cannot substitute for the
mechanism-level tests above.

### Scope claims → **CONFIRMED**

U_{1/2} is untouched as n→∞, for φ_RED and for φ_REDB alike (§9.1). The wave-3
c_eff concern does not apply (§9.2); §11's correction if anything ties the
reduction more directly to wave 8's constant. The "sign bias is gone" finding
(§8, §10 item 2) holds against the best fitted one-parameter alternative.

### Errors requiring a dated addendum before cataloguing (§10)

In order of importance: (1) the reduction's parameters, wrong at O(c/n) —
load-bearing; (2) "exact row by row except the kill law" is false; (3) "two
exact densities" of §2 are not exact; (4) the printed "λ model (3.1)" column is
mislabeled. Items 5–8 are minor and do not threaten the central claim.

### Recommendation

Integrate the pool-hazard mechanism as established. Catalogue φ_REDB, not
φ_RED as stated, pending the item 1–4 corrections — and record, rather than
paper over, that even φ_REDB leaves an unresolved residual at extreme c/n.

---

## 1. What this review did

| # | mandated item | what was run |
|---|---|---|
| 1 | re-derive the exposure argument §2; test conditional uniformity | symbolic identity check; three deterministic audits on the mechanism; 5.9×10⁸ walk steps with an exogenous pool probe; **exact** closed forms for `E|U_rem|` and `E|R^c|` derived here |
| 2 | re-derive and measure `λ(t)` | own vectorised step-by-step walk simulator, **9 cells, 5.91×10⁸ normal π-steps**, cluster bootstrap over 256–384 independent slots |
| 3 | formula-free reduction test | own M-CLUST **and** own M-U engine, 300 000 / 400 000 instances per job, 6 cells × 3 jobs |
| 4 | check the `φ_RED` derivation | sympy + mpmath(30 dps); independent re-implementation of `φ_CAND`, `φ_EPSR`, `φ_RED`, `φ_RED2` |
| 5 | audit the reported tables | every printed χ², z, sign count and pooled sum recomputed from the printed means/sems |
| 6 | scrutinise "sign bias removed" | one-parameter *fitted* null families vs the zero-parameter `φ_RED` |
| 7 | honesty / scope / the wave-3 `c_eff` question | ρ→0 limit to n = 2³⁶; independent judgement on §6.1 |
| 8 | the `O(c/n)` chain-mass term §6.3 | symbolic re-derivation of `δ` and `H_δ` |

Files produced are listed in §12.

---

## 2. Engine cross-validation (done before trusting anything)

`ref2_mc.py selftest` (`ref2_mc_selftest.log`):

* the cyclic set, computed as `image(f^{2^K})` by repeated squaring, agrees with
  **in-degree peeling** and with **literal per-node orbit following** on 300
  random maps — 0 mismatches;
* `R` built by forward π-iteration agrees with the backward `π^{-j}` membership
  test on 200 random instances — 0 mismatches;
* the wave-4 **shadowing lemma** (`π(R^c)` meets `R` only at run starts):
  **0 violations**;
* `R^c ⊆ U_rem` and `π(R^c) ⊆ U_rem`: **0 violations**;
* `b = 1 ⇒ R = ` the seed set (so M-U is exactly M-CLUST(1) in my engine).

The walk simulator's stamp bookkeeping was checked **step by step against a
literal dictionary-based walker on the same instance and the same 400 starting
points: 0 divergences** (`ref2_walk_debug` runs, §6.4).

The measured `φ(cyclic|x₀∉R)` from the walk simulator agrees with the graph-level
engine (an entirely different algorithm — no walk at all) at
`n=16384, b=50, c=100`: 0.1006 (walk) / 0.1053 (literal walk) / 0.1034 (graph),
i.e. within 1.3σ.

---

## 3. The exposure argument of §2 — re-derived, and where it is not exact

### 3.1 The argument itself is correct

Generate `(Σ, π)` in the order §2 prescribes: reveal the i.i.d. seed marks
(independent of `π`), then for each seed `s` reveal `π(s), …, π^{b−1}(s)`,
following already-revealed values when blocks overlap. After that step `R` is a
measurable function of what has been revealed, and by the standard
sequential-exposure (Fisher–Yates) fact the *unrevealed* part of `π` is a uniform
bijection `A_rem → U_rem` with

```
A_rem = [n] \ {π^j(s) : s∈Σ, 0≤j≤b−2},   U_rem = [n] \ {π^j(s) : s∈Σ, 1≤j≤b−1}.
```

Two structural facts follow, and I verified both **deterministically** (not
statistically) on 40 instances at `n = 8192` with `b = 40`, and again inside every
production walk:

* `I ⊆ R`, hence **`R^c ⊆ U_rem` — always**. 0 violations.
* the walk steps only from `R^c ⊆ A_rem`, hence `π(x) ∈ U_rem` for every normal
  step. **0 violations in 5.91×10⁸ normal π-steps** (this audit runs on *every*
  step in my simulator, not on a 1-in-4096 sample), and 0 re-consumptions
  (injectivity).
* wave-4 shadowing (`π(R^c)` meets `R` only at run starts): 0 violations.

The identity `(1−c/n)^{b−1} = (1−ρ)/(1−c/n)` is trivially true (sympy: difference
simplifies to 0, `ref2_algebra.log` §1).

### 3.2 **(2.1) and (2.2) are NOT exact.** The exact densities, derived here

§2 calls (2.1)–(2.2) "**two exact densities**". They are not: they assume the
`b−1` points `π^{−1}(y),…,π^{−(b−1)}(y)` are distinct, which fails on π-cycles
shorter than `b−1`. For a uniform permutation the cycle through a given point has
length `L` with probability **exactly** `1/n`, and on such a cycle the window has
`min(b−1, L)` distinct members. Hence, **exactly**,

```
P(y ∈ U_rem) = (1/n) Σ_{L=1}^{n} (1−p)^{min(b−1,L)}
             = (1/n)[ Σ_{L=1}^{b−2}(1−p)^L + (n−b+2)(1−p)^{b−1} ] ,   p = c/n
P(y ∉ R)     = (1/n)[ Σ_{L=1}^{b−1}(1−p)^L + (n−b+1)(1−p)^{b} ]
P(y ∈ R∩U_rem) = ((n−b+1)/n) · p (1−p)^{b−1}
```

(the third because on a cycle of length `L ≤ b−1` the window wraps onto `y`
itself, so `y ∈ Σ ∧ y ∈ U_rem` is impossible there). These three satisfy the
exact identity `P(U_rem) − P(R^c) = P(R∩U_rem)`, which is a useful self-check.
`(1−p)^{b−1}` is the `b²c/n² → 0` limit of the first.

Size of the correction, `E|U_rem|/n` exact vs `(1−c/n)^{b−1}`:

| cell | (2.1) | exact | relative error |
|---|---|---|---|
| n=32768, b=8, c=160 | 0.966317 | 0.966320 | +0.0003 % |
| n=65536, b=100, c=400 | 0.545474 | 0.545780 | +0.056 % |
| n=65536, b=400, c=100 | 0.543736 | 0.544982 | **+0.229 %** |
| n=65536, b=200, c=600 | 0.160367 | 0.161267 | **+0.561 %** |
| n=65536, b=400, c=300 | 0.160306 | 0.162116 | **+1.129 %** |
| n=65536, b=800, c=100 | 0.295198 | 0.298636 | **+1.165 %** |

and the same relative error appears in `1−ρ`. Monte-Carlo confirmation at
`b=800, c=100, n=65536` (3000 instances): measured `E|U_rem|/n = 0.29825 ±
0.00082` against the exact `0.298636` (−0.5σ) and against `(2.1)`'s `0.295198`
(+4.2σ). **The exact formula wins; (2.1) is refuted at 4σ in that cell.**

This matters because §11 heuristic item 2 files short-π-cycle events as
"`O(b²/n)`" and drops them, while §2 simultaneously advertises (2.1)–(2.2) as
*exact*. Those two statements cannot both hold. The correct statement is: the
relative error is `O(b²c/n²)`, it is ≤ 0.06 % on the lineage's standard grid
(where it is genuinely negligible) but **+0.6 % to +1.2 % on four of the six
"extreme" cells §9 adds** — the very cells §9 and §12 use to argue that the
residual no longer grows with `b`.

### 3.3 An erratum in the §4 ingredient table

The row

> structurally unclosable arc starts | a fresh arc start `D ∉ R` lies outside
> `U_rem` w.p. `c/n` (it is the successor of a run end) | idem, w.p. `c′/n′`

is **false as written**: `R^c ⊆ U_rem` identically (0 violations in my audit), so
`D ∉ R` lies outside `U_rem` with probability **0**. The intended — and correct
— statement is about the *image of the world*, not `U_rem`: `D` fails to lie in
`π(R^c)` with probability exactly `c/n`, because `π^{−1}(D) ∈ R` requires a seed
at `π^{−b}(D)`, the one point the condition `D ∉ R` leaves unexamined. In M-U the
corresponding defect is `C/N = c/n`, so the row's *conclusion* ("the defect is
equal") survives; only its wording is wrong. Harmless, but it should be fixed
before cataloguing, because §3 then uses `|U_rem|` — not `|π(R^c)|` — as the
hazard denominator, and the distinction between those two is exactly the
`O(c/n)` that §5 below shows is **not** harmless.

### 3.4 Conditional uniformity: still not proved — but now measured much harder

§11 heuristic item 1 concedes that the step

> "given the walk's entire history — including the conditioning on not having
> closed yet — `π(x)` is uniform on `U_rem` minus what the walk has consumed"

is measured, not proved. I did not find a proof either, and I do not think the
front should claim one: the walk's history is *not* a function of the revealed
values alone (it also conditions on non-closure, which is a constraint on the
unrevealed bijection). What I can report is a much stronger measurement than the
document's, obtained with an entirely independent simulator (§4).

---

## 4. T1 / T2 re-run independently — and a distinction the document blurs

### 4.1 What I ran

`ref2_walk.py`: my own step-by-step walk simulator (no `f^{2^k}` shortcut),
`x₀` drawn by rejection from `R^c`, **9 cells**, 256–384 independent walk slots
× 4 batches, **5.91×10⁸ normal π-steps** in total (the target ran 9.1×10⁸ over
8 cells). At every normal step it records, binned by traversed mass
`t = #visited/n`:

```
pool      = |U_rem| − (#normal steps so far)                 [the mechanism]
w_master  = n_live/((1−t)n)     w_exact = n_live/pool
w_cf      = w_master · λ_cf(t),  λ_cf(t) = (1−t)/(A − t/(1+δ)),
                                 A = (1−ρ)/(1−c/n),  δ = c/((1−ρ)n)
hit       = 1{π(x) ∈ Y_live}
```

with `Y` an exogenous 1000-point probe set drawn uniformly from `R^c` at
instance build (note `U_rem \ R = R^c` exactly, §3.1) and `n_live` the probes not
yet consumed as an image. Errors: cluster bootstrap over slots, 4000 replicates.
**Every** step is audited for `π(x) ∈ U_rem` and for non-re-consumption:
**0 failures out of 5.91×10⁸**.

`w_cf` is the addition that matters. The target's §7.0 defines its "λ model
(3.1)" column as `Σw_exact/Σw_master` — i.e. as the **measured per-step pool**.
That is *not* the closed form (3.1), which uses the **ensemble-mean** pool `A·n`.
I compute both and score them separately.

### 4.2 Results

| n | b | c | ρ | bins | χ² vs constant `P_lead` | χ² vs **per-step pool law** | χ² vs **closed form (3.1)** |
|---|---|---|---|---|---|---|---|
| 32768 | 8 | 160 | 0.0384 | 8 | 17.4 | 5.6 | 5.8 |
| 65536 | 100 | 150 | 0.2048 | 8 | 12.9 | 10.6 | 14.8 |
| 65536 | 50 | 400 | 0.2637 | 7 | 12.1 | 2.5 | 2.7 |
| 65536 | 200 | 150 | 0.3676 | 8 | 86.6 | 27.7 | 24.2 |
| 65536 | 400 | 100 | 0.4571 | 8 | 472.6 | 6.5 | **55.3** |
| 65536 | 300 | 150 | 0.4971 | 8 | 318.0 | 7.0 | 15.5 |
| 65536 | 100 | 600 | 0.6014 | 6 | 44.0 | 13.9 | 10.0 |
| 65536 | 800 | 100 | 0.7053 | 8 | 877.2 | 1.4 | **219.9** |
| 65536 | 100 | 1000 | 0.7851 | 6 | 83.8 | 2.4 | 12.0 |
| **pooled** | | | | **67** | **1924.6** | **77.5** | **360.2** |

Aggregate `Σhits/Σw` per cell (must be 1 if the hypothesis is right):

| cell | ρ | hits / Σ(per-step pool) | hits / Σ(closed form 3.1) |
|---|---|---|---|
| 8, 160 | 0.038 | 1.00132 ± 0.00203 | 1.00136 ± 0.00203 |
| 100, 150 | 0.205 | 0.99628 ± 0.00227 | 0.99601 ± 0.00237 |
| 50, 400 | 0.264 | 0.99921 ± 0.00290 | 0.99870 ± 0.00293 |
| 200, 150 | 0.368 | 0.99302 ± 0.00221 | 0.99368 ± 0.00247 |
| 400, 100 | 0.457 | 0.99991 ± 0.00217 | 1.00383 ± 0.00313 |
| 300, 150 | 0.497 | 0.99677 ± 0.00206 | 0.99730 ± 0.00281 |
| 100, 600 | 0.601 | 0.99352 ± 0.00278 | 0.99702 ± 0.00306 |
| 800, 100 | 0.705 | 0.99976 ± 0.00161 | 1.00552 ± 0.00529 |
| 100, 1000 | 0.785 | 0.99999 ± 0.00282 | 0.99962 ± 0.00345 |

**Three conclusions, all independent of the target's numbers.**

1. **The constant-elevation ansatz is refuted at the mechanism level.** χ² = 1925
   over 67 mass bins in 9 cells against `P_lead = 1/(1−ρ)`. This *confirms* the
   target's headline mechanism result with my own simulator, my own seeds and a
   different bin grid (the target reports χ² = 2473 over 56 bins). No `φ` and no
   quadrature enter.
2. **The mechanism the target proposes — hazard = 1/(|U_rem| − #normal steps) —
   is confirmed.** χ² = 77.5 for 67 bins (p ≈ 0.18), and the aggregate ratio is
   within 0.3 % of 1 in every cell with 0.2 % precision. This is a genuinely
   strong result and it is the target's real discovery. Combined with the two
   deterministic audits (0 failures in 5.91×10⁸ steps), the conditional-uniformity
   step of §11 heuristic 1 is confirmed empirically to ≈0.2 % per cell.
3. **The CLOSED FORM (3.1) is a different, weaker statement, and it is refuted.**
   χ² = 360 for 67 bins, driven by the large-`b` cells (`b=800, c=100`: 219.9;
   `b=400, c=100`: 55.3). The closed form uses the ensemble-mean pool `A·n`; the
   surviving walks live preferentially in instances whose `|U_rem|` is *above*
   average (a walk in a bigger pool has a lower closure hazard and lives longer),
   so at high traversed mass the true pool exceeds `A·n − t_c·n`. Example, my own
   numbers, `b=800, c=100`, mass bin [0.100, 0.180]: measured λ = **4.177 ± 0.102**,
   per-step pool law **4.084**, closed form (3.1) **4.807** (−6.2σ). Same pattern
   at `b=400, c=100`, bin [0.100, 0.180]: measured **1.988 ± 0.018**, pool law
   **1.998**, closed form **2.072** (−4.6σ).

The same defect is visible **in the target's own printed table** without running
anything: §7.1's "λ model (3.1)" column for `b=400, c=100` gives 1.9797 for the
bin [0.100, 0.180] and 2.0400 for [0.180, 1.000], while the closed form (3.1)
takes values 2.028–2.254 and ≥2.251 on those bins respectively. A weighted average
of `λ(t)` over a bin cannot fall outside the bin's own range, so **that column is
not (3.1); it is the measured per-step pool ratio** (`ref2_tables.log` §F flags
exactly these three bins as OUTSIDE).

**Consequence for the claim.** §7.3's "the derived λ(t) is consistent with pure
noise, χ² = 50.9 for 56" and §13's "Is the elevation constant? NO — refuted,
χ² 2473.4 vs 50.9" are correct statements about the **pool mechanism**, and
should be worded that way. They are **not** evidence that the closed form (3.1)
— the object `φ_RED` is actually built from — is at noise level. It is not.
Mass-weighted the error is small (the aggregate `hits/Σw_cf` stays within 0.6 %
of 1), so `φ_RED` is not badly damaged by it; but the scorecard line overstates
what was shown.

### 4.3 The live-arc-start cross-check (§7.4) — inconclusive in my hands

I also accumulated the Horvitz–Thompson estimator on the walk's **own** live
closure targets (`x₀` plus every point first reached by an `f`-draw that lies in
`U_rem` — exactly the visited points a normal π-step can land on; a deterministic
audit confirms 0 normal-step terminations outside that set). My two independent
implementations disagree: the vectorised production simulator gives
1.14–1.23 (±0.03) uniformly across ρ ∈ [0.04, 0.79], while a literal
dictionary-based reference walker with a *fixed* 40 walks per instance gives
**1.036 ± 0.040** at `n=16384, b=50, c=100` (20 000 walks, 500 instances, cluster
bootstrap) — consistent with 1. The two implementations are **step-for-step
identical on a fixed instance** (400 walks, 0 divergences), so the difference is
in how instances are weighted: running walks back-to-back for a fixed number of
iterations weights each instance by `1/E[walk length | instance]`, which is
correlated with the estimator itself. I therefore **decline to draw any
conclusion from this channel**, and I flag that the target's §11 open-item-2
number (`0.994 ± 0.003`) is quoted at a precision that my realisation-to-
realisation scatter does not support. The target does not use it anywhere, so
nothing depends on it.

---

## 5. T3, the reduction — **the central negative finding**

### 5.1 The reduction's parameters, re-derived from expected counts

The reduction (4.1) is a statement that the conditioned M-CLUST process *is*
M-U at some `(C, N)`. Whatever else is true, the two sides must at least agree
on the three quantities that fully determine the continuum process:

| ingredient | M-CLUST(b) at `(c,n)` \| `x₀∉R` | M-U at `(C,N)` |
|---|---|---|
| world (points the walk normal-steps from) | `E\|R^c\| = n(1−c/n)^b` | `N − C` |
| image pool (targets a normal step can consume) | `E\|U_rem\| = n(1−c/n)^{b−1}` | `N` |
| reroute rate per normal step | `E\|R∩U_rem\|/E\|U_rem\| = c/n` (exact) | `C/N` |

Solving all three simultaneously gives a **unique** answer:

```
N = n(1−c/n)^{b−1} ,   C = c(1−c/n)^{b−1} = c(1−ρ)/(1−c/n)      (convention B)
```

which indeed satisfies `N − C = n(1−c/n)^b` identically. The document's (4.1),

```
n′ = (1−ρ)n ,  c′ = c(1−ρ)                                       (convention A)
```

gets the rate right (`c′/n′ = c/n`) but undershoots **both** the world and the
pool by `≈ c(1−ρ)` points — e.g. by 294 out of 48 551 at `b=50, c=400, n=65536`,
by 218 out of 35 748 at `b=100, c=400` (`ref2_algebra.log` §8). The document's own
*secondary* convention `n′ = (1−ρ)(n+c)` is convention B to `O(c²/n)`.

The §4 ingredient table papers over this by writing M-U's image pool as
"`n′/(1−c′/n′)`". **M-U's image pool is `n′`, not `n′/(1−c′/n′)`** — for `b = 1`
the revealed-image set `I` is empty, so `U_rem = [n′]` exactly. The table's
"world" row and its "image pool" row therefore contradict each other by a factor
`(1−c/n)`, and (4.1) resolves the contradiction in favour of the world row.
§6.3's assertion that "**the reduction (4.1) is exact row by row except in the
kill law**" is consequently **false**: the image-pool row is also inexact, at the
same `O(c/n)`, and — unlike the kill-law term `δ`, which §6.3 does name and size
— this one is not named anywhere.

Size of the error: `φ_U(c″)/φ_U(c′) − 1` = −0.06 % (`b=8,c=40`) … −0.31 %
(`b=100,c=400`) … −0.46 % (`b=100,c=600`) … **−0.77 %** (`b=100,c=1000`).

### 5.2 The test, at 2.4× the target's precision

`ref2_reduction.py`, my own M-CLUST engine and my own M-U engine (M-U = my
M-CLUST at `b=1`, verified), fresh seeds `20260824920+`, **300 000 M-CLUST
instances and 400 000 M-U instances per job** against the target's 40 000. Errors
are delta-method (instances are i.i.d.), cross-checked against a 1500-replicate
bootstrap on 20 000/50 000/100 000-instance resamples: agreement to <2 % of the
sem. No formula on either side.

Full 6-cell result (`ref2_reduction_analysis.py`, `ref2_reduction_analysis.log`):

| cell | ρ | M-U(A) full | M-U(A) cond | M-U(B) full | M-U(B) cond | φ_U(c′) | φ_U(c″) |
|---|---|---|---|---|---|---|---|
| b=50 c=400 n=65536 | 0.2637 | −0.381% z=−3.02 | −0.401% z=−3.18 | −0.015% z=−0.12 | −0.035% z=−0.28 | −0.210% z=−2.21 | +0.096% z=+1.00 |
| b=100 c=400 n=65536 | 0.4579 | −0.479% z=−3.81 | −0.502% z=−3.99 | −0.058% z=−0.46 | −0.081% z=−0.65 | −0.278% z=−2.92 | +0.028% z=+0.29 |
| b=100 c=600 n=65536 | 0.6014 | −0.774% z=−6.15 | −0.807% z=−6.41 | −0.143% z=−1.13 | −0.175% z=−1.39 | −0.620% z=−6.53 | −0.162% z=−1.70 |
| b=200 c=150 n=65536 | 0.3676 | −0.311% z=−2.47 | −0.324% z=−2.57 | −0.177% z=−1.41 | −0.191% z=−1.51 | −0.164% z=−1.72 | −0.049% z=−0.52 |
| b=400 c=100 n=65536 | 0.4571 | +0.105% z=+0.83 | +0.094% z=+0.74 | +0.081% z=+0.64 | +0.070% z=+0.55 | +0.024% z=+0.25 | +0.100% z=+1.05 |
| b=100 c=1000 n=65536 | 0.7851 | −2.040% z=−16.32 | −2.096% z=−16.77 | −1.240% z=−9.87 | −1.295% z=−10.30 | −1.787% z=−19.00 | −1.029% z=−10.86 |

`dev% = 100·(φ_MCLUST/candidate − 1)`; `z = (φ_MCLUST − candidate)/sd_pooled` (M-U
columns) or `/sem_MCLUST` (continuum columns), as in §5.2.

χ² over 6 cells (1 dof each):

| candidate right-hand side | χ² |
|---|---|
| measured M-U(A) = (c(1−ρ), (1−ρ)n), full φ | 334.56 |
| measured M-U(A), conditional φ(.\|x₀∉R′) | 355.41 |
| measured M-U(B) = (c(1−c/n)^{b−1}, n(1−c/n)^{b−1}), full | **101.37** |
| measured M-U(B), conditional | 111.18 |
| continuum φ_U(c(1−ρ)) [ATTEMPT (4.2)] | 420.06 |
| continuum φ_U(c(1−c/n)^{b−1}) [referee, φ_REDB argument] | 123.25 |

The two cells added by the completed run bracket the grid: `b=400,c=100`
(ρ=0.457, the smallest `c` in the set) shows no resolvable deviation from
either convention (|z|≤1.05 throughout — the O(c/n) parameter shift is
≈c(1−ρ)≈54 points against `N≈35 600`, too small to detect at this precision);
`b=100,c=1000` (ρ=0.785, the largest `c/n` in the set) shows the largest
deviation from *every* candidate, convention B included (z=−9.87, full). That
one cell supplies ≈96% of convention B's 6-cell pooled χ².

### 5.3 What this means

**The reduction as stated in (4.1) is refuted, and refuted on exactly the
criterion the front pre-registered for it.** `DERIVATION_PREREG.md` §6 lists, as
the refutation condition for T3: "*a systematic discrepancy growing with `b` or
`ρ`*". That is precisely what appears once the precision is high enough.

**But the mechanism is not refuted — only its parameters.** Moving to convention
B (equivalently: to the document's own second convention `n′=(1−ρ)(n+c)`, which
it measured and did not adopt) restores agreement to ≤0.2 % everywhere. The
target's own T3 table already shows convention B doing *equally well* at its
precision (χ² 3.93 vs 3.83); the front had the right answer in its hands and
picked the wrong one because at 40 000 instances the two are indistinguishable.

The correct conclusion is therefore:

```
  phi(cyclic | x0 notin R)  =  phi_U( c (1-c/n)^{b-1} )  + O(c/n) terms
                            =  phi_U( c'' ),   c'' = c(1-rho)/(1-c/n)
```

and **not** `φ_U(c(1−ρ))`. The correction is a genuine `O(c/n)` shift of the
argument, not a change of functional form; everything qualitative in §2–§4 of the
target survives it.

---

## 6. The algebra of §4, §5 and §6.3 — all correct

Re-derived from scratch with sympy (exact) and mpmath at 30 dps
(`ref2_algebra.py`, `ref2_algebra.log`; `ref2_formula.py`,
`ref2_formula_selfcheck.log`).

* §2's identity `(1−c/n)^{b−1} ≡ (1−ρ)/(1−c/n)`: difference simplifies to **0**.
* §4's direct check: with hazard `1/(A−t)`, `A = 1−ρ`, and `q_CLUST(s) = s/A`,
  `(1−q(s))/(A−s)` simplifies to **`1/A`** and
  `H(t) = t − (A−t)·t/A` simplifies to **`t²/A`** — difference from `t²/A` is
  symbolically **0**.
* the substitution `∫₀^A (1/A)e^{−ct²/A}dt = ∫₀¹e^{−cAu²}du`: symbolic difference
  **0**.
* `T_U(c′) = φ_U(c′) − (1−e^{−c′})/(2c′)`: symbolic difference **0**; closed form
  vs 50-dps quadrature agree to `<7e-52` at five values of `c′`.
* §6.3: `q(u)=u(1+δ(1−u)) ⇒ (1−q)/(1−u) = 1−δu` exactly, and
  `H_δ(u) = u² + (δ/2)u²(1−u)` — symbolic difference **0**. `δ = c/((1−ρ)n)` is
  the right chain-mass factor: the walk visits `≈ (c/n)/(1−ρ)` points of `R` per
  normal step (one run start plus a geometric chain of mean `1/(1−ρ)`), which is
  exactly `δ` per unit collapsed mass. `δ_extra = cρ/((1−ρ)n)` relative to M-U at
  `(c′,n′)` is likewise correct, because M-U carries its own `C/N = c/n`.
* the two printed forms of (5.1) are algebraically identical (difference `<3e-53`).
* §5's stated numerical checks reproduce: `λ(0) = P_exact` to **machine
  precision** (difference exactly 0.0e+00 in three cells); and
  `φ_RED − (1−ρ)φ_U(c′)` is proportional to `c/n` at fixed `ρ` —
  `3.661e-4 → 3.658e-5 → 3.658e-6 → 3.658e-7` as `c/n` falls by factors of 10.

**Transcription fidelity.** My independent implementations of `φ_CAND`,
`φ_EPSR`, `φ_RED` and `φ_RED2`, built only from the stated closed forms,
reproduce the value implied by the target's own printed `(φ_mc, dev%)` pairs in
**24 of 24 cells to better than 3×10⁻⁴ relative** (`ref2_tables.log` §A). The
document's formula transcription is faithful and its four formula columns are
what it says they are.

**One caveat on the `eps` channels.** §5 re-expresses the referee's two `eps`
channels "with `P → 1`, `c → c′`, `H(t) → u²`", giving
`φ_runstart → T_U(c′)`. That substitution is right *given* the reduction, and it
inherits the reduction's parameter error: under the corrected reduction the
`eps` channels should use `c″`, not `c′`. The change is numerically tiny
(`ρ·eps` is 0.01 %–2.3 % of `φ`, and the shift inside it is ≤0.8 % of that), so
this is bookkeeping rather than a second error.

---

## 7. Audit of the reported tables (§7.1–7.3, §8, §9, §10)

Every printed aggregate was recomputed from the printed per-cell numbers
(`ref2_tables.py`, `ref2_tables.log`).

**Everything that can be checked, checks.**

| checked | result |
|---|---|
| `ρ` and `bc/n` from `(b,c,n)`, 24 cells | 0 mismatches |
| `z` from `(φ_mc, sem, dev%)`, 24 cells × 4 formulas = 96 entries | 0 mismatches |
| §9 χ² (18 cells) = Σz²: CAND / EPSR / RED / RED2 | 324.72 / 181.47 / 30.21 / 26.95 vs printed 324.66 / 181.50 / 30.20 / 26.97 ✓ |
| §9 χ² (24 cells) | 1932.10 / 602.73 / 64.78 / 40.67 vs printed 1931.87 / 602.62 / 64.79 / 40.71 ✓ |
| §9 "below the MC mean" counts | 23 / 20 / 11 / 15 of 24 — all match ✓ |
| §10 pooled χ² over 7 grids, 132 cells | 2923.30 / 1149.83 / 183.34 / 160.11 vs printed 2923.29 / 1149.82 / 183.33 / 160.10 ✓ |
| §10 "standard grids only" (126 cells) | 1316.16 / 728.68 / 148.76 / 146.35 vs printed 1316.08 / 728.70 / 148.74 / 146.36 ✓ |
| §10 below-MC pooled | 115 / 108 / 75 of 132 ✓ |
| §10 sign-test significances | 1.567σ (printed "1.5σ"); p = 7.3e-18 (printed 1e-17); p = 1.3e-13 (printed 1e-13) ✓ |
| §7.3 pooled χ² and bin count | 2473.4 / 50.9 over 56 bins ✓ |
| §7.2 `z` from ratio and sem, 8 cells | 0 mismatches ✓ |
| §8 χ² = Σz² for the three columns | 3.83 / 3.95 / 5.44 vs printed 3.83 / 3.93 / 5.47 ✓ (z rounding) |
| §8 continuum column vs my own `φ_U(c(1−ρ))`, 6 cells | agree to ≤8×10⁻⁶ relative ✓ |

**Two small inaccuracies found.**

1. **§7.2.** "the scatter across cells (0.0022) is about 1.8× the quoted sems".
   From the eight printed ratios the sample sd is **0.00181** (ddof=1) or
   **0.00170** rms about 1.0, against a mean quoted sem of 0.00119 — i.e.
   **1.4–1.5×**, not 1.8×. The error is in the *conservative* direction (the
   document overstates its own scatter), so nothing that depends on it is
   affected.
2. **§7.1.** The column labelled "λ model (3.1)" is not the closed form (3.1);
   see §4.2 above. Three of the twelve printed bins take values strictly outside
   the range `λ(t)` can take anywhere inside their own bin.

**One auditability gap.** §8's two "measured M-U" columns quote `z` values that
require the M-U standard errors, which the table does not print (only the
M-CLUST sem is given). Those `z` cannot be reconstructed from the table; the
implied combined sems (0.000189–0.000443) are consistent with a same-size M-U
run, so I have no reason to doubt them, but the column is not self-auditing.
The continuum column *is* (its `z` uses the M-CLUST sem alone, and reproduces).

---

## 8. "The sign bias is gone" (§10 item 2) — this one holds up, and better than the document argues

The predecessor referee's §5.8 caveat is the right objection: `φ_CAND` sits below
the Monte-Carlo mean in 16–18 of 18 cells on every grid, so **any** strictly
positive correction of roughly the right size buys χ² and flips sign counts.
The document answers with the sign count (108/132 → 75/132, 1.5σ from unbiased),
which is necessary but not sufficient — a one-parameter fitted correction would
also flip it.

I ran the sufficient test. Take `φ_EPSR` and multiply by `(1 + a·g)` for seven
generic shapes `g`, with `a` **fitted by least squares on the very grid being
scored** (this is maximally generous to the null); and separately fit the
one-parameter "measured constant elevation" model `φ_CAND` with
`P = P_lead(1+aρ)`, which is what the previous front's §5.3 effectively did.
Scored on the target's own recorded 24-cell grid (`ref2_null_family.log`):

| model | free parameters | χ² (24 cells) | below-MC |
|---|---|---|---|
| `φ_CAND` | 0 | 1939.4 | 23/24 |
| `φ_EPSR` (formula of record) | 0 | 603.4 | 20/24 |
| `φ_EPSR·(1+a·ρ)`, a fitted | **1** | 219.5 | 13/24 |
| `φ_EPSR·(1+a·bc/n)`, a fitted | **1** | 244.4 | 14/24 |
| `φ_EPSR·(1+a·(−ln(1−ρ)))`, a fitted | **1** | 245.4 | 14/24 |
| `φ_EPSR·(1+a·ρ²)`, a fitted | **1** | 258.9 | 15/24 |
| `φ_EPSR·(1+a·ρ·bc/n)`, a fitted | **1** | 290.5 | 16/24 |
| `φ_EPSR·(1+a·ρ/(1−ρ))`, a fitted | **1** | 302.4 | 16/24 |
| `φ_CAND` with fitted constant elevation `P_lead(1+aρ)` | **1** | 215.3 | — |
| **`φ_RED`** | **0** | **64.9** | 11/24 |
| `φ_RED` with the referee's `c″` (`φ_REDB`, §5) | **0** | **46.0** | 13/24 |
| `φ_RED2` | 0 | 40.7 | 15/24 |

**The best one-parameter ad-hoc correction, fitted in-sample, cannot get below
χ² ≈ 215; the zero-parameter `φ_RED` reaches 64.9 and the corrected `φ_REDB`
reaches 46.0.** The "any positive correction of the right size" objection is
therefore *not* an available explanation of this front's χ² gain: the gain is
specific to the functional shape, by a factor of 3–5 in χ² over the best generic
alternative with a free parameter. **On this point the document is right and, if
anything, under-argues its case.**

That said, I weight the evidence exactly as the mandate asks: the χ²-table
evidence (T4, §10) is *supporting*, not decisive, because it is scored against
`φ` and therefore folds the elevation model together with the `eps` model, the
quadrature and the master formula's own error. The decisive evidence is the two
mechanism-level tests, and they split:

* **T1/T2 (my §4) is convincing.** The constant-elevation ansatz is refuted at
  χ² = 1925/67 with no formula anywhere, and the proposed replacement mechanism
  (hazard = 1/(pool)) is confirmed to 0.2 % per cell with 0 audit failures in
  5.9×10⁸ steps. I regard this as established.
* **T3 (my §5) is convincing *against the stated parameters* and *for* the
  corrected ones.** At 7.5× the target's instance count the stated reduction
  (4.1) fails with a discrepancy that grows with ρ; the corrected reduction
  passes.

So the mechanism-level evidence stands on its own, independent of any χ² table —
which is what makes the split verdict below possible.

---

## 9. Scope, honesty, and the wave-3 `c_eff` question

### 9.1 The U_{1/2} classification really is untouched

`φ_RED → φ_U(c)` as `n → ∞` at fixed `(b,c)`, with the difference falling exactly
like `1/n` (my own mpmath evaluation at `b=100, c=400`):

| n | `φ_RED − φ_U(c)` | relative |
|---|---|---|
| 2¹⁶ | −1.132e-02 | −2.55e-01 |
| 2²⁰ | −8.206e-04 | −1.85e-02 |
| 2²⁴ | −5.176e-05 | −1.17e-03 |
| 2²⁸ | −3.237e-06 | −7.31e-05 |
| 2³² | −2.023e-07 | −4.57e-06 |
| 2³⁶ | −1.265e-08 | −2.85e-07 |

Nothing in §2–§5 requires `n` finite except through `c/n`; every correction term
carries an explicit `c/n` or `ρ`, and `ρ → 0` at fixed `(b,c)`. The same holds
for the corrected `φ_REDB` (`c″ → c` as `c/n → 0`) and for `φ_RED2` (`δ → 0`).
**§12's and §13's "U_{1/2} untouched" is fully supported.** No overclaim here.

### 9.2 §6.1's distinction from the refuted wave-3 `c_eff` **is valid** — and the correction of §5 makes it moot

The concern is real: `φ_U(c(1−ρ)) = φ_U(c(1−c/n)^b) = φ_OLD`, the wave-3 formula
that wave 4 refuted with deviations to −46 %. Is this front smuggling it back?

**No, and for the reason §6.1 gives.** I checked the load-bearing step
independently: wave 4's refutation was of the *rate*, i.e. of the claim that
reroute events occur at `c(1−c/n)^b` per unit mass. I re-derived wave 4's
sliding-window argument and it is exact — conditioned on `x ∉ R`, the `b`-window
ending at `π(x)` differs from the window ending at `x` in exactly one unexamined
point, so `P(π(x) ∈ R | x ∉ R) = c/n` **exactly**, and because each step reveals
one fresh seed mark the encounters are independent across steps. This front uses
that rate, unmodified; the factor `(1−ρ)` enters only through the change of
variable `u = t/(1−ρ)` forced by the elevated hazard, and the answer is then
multiplied by the exact dilution `(1−ρ)`. The two routes are genuinely different
and the two claims are genuinely different (conditional × dilution vs
unconditional). **§6.1 is sound.**

It is worth adding what §6.1 does not say: because the *numbers* coincide, the
χ²-level evidence of §9/§10 cannot by itself distinguish this front's derivation
from "wave 3's formula times `(1−ρ)`". Only the mechanism-level measurement (T1/
T2) can, which is another reason those tests carry the weight.

And there is a pleasant side effect of the §5 correction: under the corrected
reduction the conditional answer is

```
   phi(cyclic | x0 notin R) = phi_U( c (1-c/n)^{b-1} ) = phi_U( c / P_exact )
```

with `P_exact = (1−c/n)^{−(b−1)}` **wave 8's aggregation-lemma constant**, not
wave 3's `c(1−c/n)^b`. The coincidence with `φ_OLD` disappears, and the formula
instead ties directly to the one piece of this lineage that is independently
established and validated (`aggregation_closure_attempt` §4.3). That is a
strictly better place for the front to stand.

### 9.3 §6.3 / `φ_RED2` scoping is honest

The document says plainly: "`φ_RED` (5.1) is the claim of this front and
`φ_RED2` is reported as a quantified, named refinement, not adopted." That is
what §9, §10 and §13 do — every table carries `φ_RED2` as a separate column, the
verdict quotes `φ_RED`, and §11 heuristic item 3 states the reason for not
adopting it (the baseline finite-`n` error of M-U at `(c′,n′)` is not pinned
down). **I find no overclaim in the scoping.** The `δ` algebra is correct (§6).

The one thing §6.3 gets wrong is the sentence introducing it — "the reduction
(4.1) is exact row by row **except in the kill law**" — which is refuted by §5.1
above.

### 9.4 Where §11–§13 overclaim, and where they do not

Supported as written: the `n→∞` limit; the no-curve-fitting audit trail
(`DERIVATION_PREREG.md` predates every `*.json` in the folder — file mtimes
23:15 vs 23:27+, and the formula has no free parameter, so there is nothing that
*could* be fitted); the "adversarial verification REQUIRED, not done here" line;
the honest listing of a remaining residual; the refusal to declare `φ_EPSR`
superseded.

Overclaimed:

* §2 "two **exact** densities" — not exact (§3.2); ≤0.06 % on the standard grid
  but +0.6 %…+1.2 % on four of the six extreme cells.
* §7.3 / §13 "**the derived λ(t)** is consistent with pure noise" — what is at
  noise level is the per-step pool law, not the closed form (3.1) (§4.2).
* §6.3 "exact row by row except in the kill law" — the image-pool row is also
  inexact (§5.1).
* §8 / §11 item 3 / §12 / §13 "**the reduction is CONFIRMED, formula-free,
  χ² = 3.83 / 6 cells**" — confirmed only at 40 000 instances; refuted at
  300 000/400 000 (§5.2). The correct claim is that the *corrected* reduction is
  confirmed.
* §4's "structurally unclosable arc starts" row — wrong as worded (§3.3).

Not overclaimed but worth recording: the front's own §11 open item 1 ("a real
residual remains, χ²/dof ≈ 1.4") and open item 2 (the live-arc-start estimator)
are both honest, and open item 2 is if anything *more* uncertain than stated
(§4.3).

---

## 10. Errors and inaccuracies found, ordered by importance

1. **§4 / §8 / §11 / §12 / §13 — the reduction's parameters are wrong at
   `O(c/n)`, and the stated reduction is refuted by a higher-precision re-run of
   the front's own test.** `n′=(1−ρ)n, c′=c(1−ρ)` undershoots both the mean world
   and the mean image pool by `≈c(1−ρ)` points. At 300 000/400 000 instances the
   measured `φ(cyclic|x₀∉R)` sits below the measured M-U at those parameters by
   an amount that **grows with ρ**, which is the front's own pre-registered
   refutation criterion for T3. The unique parameter choice that matches world,
   pool and rate simultaneously is `N = n(1−c/n)^{b−1}`, `C = c(1−c/n)^{b−1}`,
   and it restores agreement. (§5)
2. **§6.3 — "the reduction (4.1) is exact row by row except in the kill law" is
   false.** The image-pool row is inexact at the same order and is not named
   anywhere. The §4 table hides it by writing M-U's image pool as
   `n′/(1−c′/n′)`; M-U's image pool is `n′`. (§5.1)
3. **§2 — "two exact densities" is wrong.** (2.1)/(2.2) neglect π-cycles shorter
   than `b−1`. Exact closed forms are given in §3.2; the relative error reaches
   **+1.17 %** at `b=800, c=100, n=65536` and **+1.13 %** at `b=400, c=300` — two
   of the six "extreme" cells the front uses to argue the residual no longer
   grows with `b`. Confirmed by Monte Carlo at 4.2σ against (2.1) and −0.5σ
   against the exact form. (§3.2)
4. **§7.3 / §13 — "the derived λ(t) is consistent with pure noise, χ² = 50.9"
   is about the wrong object.** The quantity measured is the per-step pool law
   (which does hold: my χ² = 77.5/67); the closed form (3.1), which is what
   `φ_RED` is built from, is refuted at χ² = 360/67, by up to −6σ per bin at
   large `b`. Visible in the document's own §7.1 table: three printed
   "λ model (3.1)" values lie outside the range `λ(t)` can take inside their own
   bin. (§4.2)
5. **§4 table — "a fresh arc start `D ∉ R` lies outside `U_rem` w.p. `c/n`" is
   false as written** (`R^c ⊆ U_rem` identically). The correct statement is about
   `π(R^c)`; the row's conclusion survives. (§3.3)
6. **§7.2 — "the scatter across cells (0.0022) is about 1.8× the quoted sems"**
   recomputes from the printed ratios as 0.0017–0.0018 and 1.4–1.5×. Conservative
   direction; immaterial. (§7)
7. **§11 open item 2 — the live-arc-start ratio `0.994 ± 0.003`** is quoted at a
   precision my own two implementations cannot reproduce (they disagree by 3.5σ
   with each other). Not used anywhere by the front, so nothing depends on it,
   but the quoted sem should be treated as a lower bound. (§4.3)
8. **§8 — the two "measured M-U" columns are not self-auditing** (the M-U sems
   are not printed, so their `z` cannot be recomputed from the table). (§7)

**None of items 3–8 threatens the front's central mechanism claim.** Item 1 does
not threaten the mechanism either, but it does block cataloguing `φ_RED` in its
stated form.

---

## 11. The corrected candidate

A one-symbol change to (5.1), derived (not fitted), with no new parameter:

```
   c'' = c (1 - c/n)^(b-1) = c(1-rho)/(1-c/n)          [= c / P_exact, wave 8]

   phi_REDB = (1-rho) [ phi_U(c'') + (c/n) T_U(c'') ]
              + rho (1 + c'' T_U(c'')) / ((1-rho) n)
```

Everything else — `φ_U`, `T_U`, the two `eps` channels, the `(1−ρ)` dilution, the
`ρ→0` limit — is unchanged. Properties I verified:

* `φ_REDB → φ_U(c)` as `n→∞` at fixed `(b,c)`: unchanged, `c″ → c`.
* it is the **unique** choice matching mean world, mean pool and reroute rate
  simultaneously (§5.1), and it equals the document's own second convention
  `n′=(1−ρ)(n+c)` to `O(c²/n)`.
* on the formula-free reduction test it is the one that passes (§5.2).
* on the target's own recorded 24-cell grid it lowers χ² from 64.9 to **46.0**
  (cheap triage, labelled; my own fresh-seed grid is in §5.4/§12).
* `φ_RED2`'s `δ` refinement can be applied to it identically.

I also tested a stronger variant, `φ_REDX`, built from the **exact** densities of
§3.2 (exact `ρ`, exact pool, exact run-start density). It is *not* better
(χ² = 64.8 on the same grid): it repairs the worst extreme cell (`b=800, c=100`
goes from +3.13σ to −1.23σ) but overshoots two others. My reading is that on a
π-cycle shorter than `b` the *dynamics* also change (the whole cycle is absorbed
into `R` and becomes unreachable by normal steps), so substituting corrected mean
densities into a formula derived for the long-cycle regime is not enough.
**I do not recommend `φ_REDX`; I record it as a tested and rejected refinement,**
and as evidence that the `O(b²c/n²)` term of §3.2 is a real, separate, unmodelled
effect in the extreme cells.

---

## 12. Files produced by this review (all in `elevation_level_attempt/adversarial/`)

| file | role |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref2_algebra.py` / `.log` | sympy + mpmath re-derivation of §2, §3, §4, §5, §6.3; the matching analysis of §5.1 |
| `ref2_mc.py` / `ref2_mc_selftest.log` | own M-CLUST(b)/M-U engine; three independent constructions of the cyclic set, two of `R`; the deterministic exposure audits |
| `ref2_formula.py` / `ref2_formula_selfcheck.log` | own closed forms: `φ_U`, `T_U`, `H(t;P)`, `φ_V4`, `φ_CAND`, `φ_EPSR`, `φ_RED`, `φ_RED2`, plus the referee's `φ_REDB`, `φ_RED2B`, `φ_REDX` and the **exact** pool/world/run-start densities of §3.2 |
| `ref2_walk.py` / `ref2_walk_*.json` / `ref2_walk_analysis.py` / `ref2_walk_analysis_final.log` | **T1/T2** — own vectorised step-by-step walk simulator with an exogenous pool probe, 9 cells, seeds 20260824911–919, 5.91×10⁸ normal π-steps, every step audited |
| `ref2_reduction.py` / `parts/red_*.npz` / `ref2_reduction_analysis.py` / `ref2_reduction_analysis.log` | **T3** — the formula-free reduction test at 300 000/400 000 instances per job, seeds 20260824920+; **the central negative finding** |
| `ref2_grid.py` / `parts/grid_*.npz` / `ref2_grid_analysis.py` / `ref2_grid_analysis.log` | **T4** — own fresh 24-cell φ grid, seeds 20260824940+, including the six extreme cells |
| `ref2_pool_moments.py` / `.log` | pool/world fluctuation moments; the Jensen term the reduction does not carry |
| `ref2_tables.py` / `ref2_tables.log` | arithmetic audit of every table in §7.1–7.3, §8, §9, §10 |
| `ref2_null_family.py` / `ref2_null_family.log` | the "any positive correction" null test of §8 |
| `run_reduction.sh`, `run_grid.sh`, `run_grid2.sh`, `logs/` | drivers and raw job logs |
