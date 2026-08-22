# REFEREE REPORT — adversarial review of `x0_asymmetry_attempt/ATTEMPT.md` §5.1–5.2

Independent, hostile review of the **secondary positive claim** of wave 9 front (a)
(`MCLUST-X0-ASYMMETRY-ATTEMPT`), dispatched by `DISC-DEC-043`.
The primary refutation of the x₀-asymmetry hypothesis (§4 of the target) is already
integrated and is **not** reviewed here. §5.3 (elevation level) and §5.4 (M-U
finite-n control) were read for context only, as instructed; where my own
measurements happen to bear on §5.3 I say so and label it out of scope.

Nothing outside this `adversarial/` subfolder was created or modified. No git
commit was made.

---

## 0. VERDICT

### Sub-claim 1 — `eps := P(x₀ cyclic | x₀ ∈ R)` is NOT zero → **SOUND**

Confirmed, and far more strongly than the target itself establishes. I measured
`eps` in **18 cells** (target: 6) with **3.0×10⁴ – 6.8×10⁵ cyclic events per cell**
(target: 157–483), by a method that **simulates no walk at all**, and cross-checked it
on five further independent seeds and at three values of `n`. `eps` is nonzero at
190σ–260σ per cell. My values agree with the target's stage-B measurement in 5 of its
6 cells.

The predecessor's `eps = 0` was not a harmless idealisation. Its stated
justification disposes correctly of the *shadowed interior* of `R` and then
silently discards the *run-start* sub-population, which is `ρ_start/ρ ≈ 1/b` of `R`
and whose return probability is of order `φ` itself. I reached this conclusion
independently, before reading §5, and for the same reason the target gives.

### Sub-claim 2 — `φ_EPS` improves on `φ_CAND` → **SOUND WITH NAMED ISSUES**

The improvement is **real, reproducible and out-of-sample**. All four claimed χ²
reductions reproduce arithmetically to <0.1; the improvement repeats on two fresh
referee grids at 4× the target's precision; the term it adds is provably part of an
**exact** decomposition, and replacing the modelled `eps` by the **exactly measured**
`eps` changes χ² by <1 %.

**But the leading-order derivation in §5.2 contains two distinct, systematic,
individually-demonstrable errors — one in each channel** (§4): the **run-start**
channel is **2 %–33 % too high** and the **f-draw** channel is **5 %–43 % too low**.
They are present with the same sign in **all 18 cells of the grid**, in all 11 cells
of an independent channel probe, across a 4× range of `n`, and across `b` from 1 to
400 — and they are **not** "low event counts / Poisson noise" as §5.2 asserts. Both
are correctable inside the front's own formalism, and I derive and verify the
corrections against measurements with 10²–10³× the target's statistics. Because the
two errors have opposite signs they largely cancel in `φ`, which is why the χ² claim
survives intact while the derivation does not.

### Recommendation (split — see §10)

* **Integrate `eps ≠ 0` as an established fact.**
* **Catalogue `φ_EPS` as an adversarially verified improvement over `φ_CAND`** —
  but only together with the corrected two-channel derivation of §4, which is
  numerically ≥ `φ_EPS` on all six grids tested and whose ingredients are *measured*
  rather than fitted.
* **Record that the `eps` channel is now exhausted**: no future front should spend
  effort refining it. The whole remaining residual is in `φ(cyclic | x₀ ∉ R)`, i.e.
  in the elevation level of §5.3 — which my measurements independently confirm.

### Coverage of the dispatched review items

| dispatched item | where |
|---|---|
| 1. own judgement on whether `eps = 0` was ever reasonable, formed before reading §5 | §2 |
| 2. own simulator measuring `eps` in the 6 stress cells, fresh seeds, different strategy | §1(ii)(iii), §4.2 — done in 18 cells, 4 seeds, by a walk-free method (deviation from the letter of the dispatch explained in §1(iii)) |
| 3. cross-validation against ≥2 earlier recorded grids before trusting it | §3 — four grids, 72 comparisons |
| 4. independent `eps`, compared cell by cell against the target | §4.2 |
| 5. scrutiny of the §5.2 two-channel derivation, re-derived first | §4.1, §4.3, §4.4, §4.5 |
| 6. own validation script, own MC, own χ² for both formulas on the 18-cell grid | §5.1–§5.3 |
| 7a. holds under a different seed? | §5.4 — yes, six grids |
| 7b. do the three recorded-grid χ² improvements check out? | §5.2 — yes, to <0.1 |
| 7c. any sign of tuning after seeing validation data? | §5.7 — no |
| 8. are the two channel-ratio sanity numbers as claimed; is the Poisson excuse legitimate? | §4.4 "This settles review item 8" — numbers nearly right, excuse **not** legitimate |
| 9. is `φ_EPS` honestly scoped; is the scorecard accurate? | §8 — yes |

---

## 1. Method, and what makes it independent

Every script in `adversarial/` was written from scratch from the primary sources
(`DERIVATIONS.md` §0–3.6 & §6, `DERIVATION_MCLUST_FIXED.md` §1–4,
`residual_attempt/ATTEMPT.md` §6). Nothing is imported or copied from
`x0_asymmetry_walk_measure.py`, `x0_asym_candidate.py`, `x0_asym_validate.py`,
`x0_asym_formula.py`, `x0_asym_analysis.py`, `mclust_residual_v4.py`,
`mclust_global_formula.py`, any `mclust_*_validate.py`, or `ualpha_sim.py`. The one
exception is `ref_quadrature_audit.py`, which *executes the target's module as an
object under test* and feeds nothing back into my own pipeline.

Fresh seeds, none used anywhere in this lineage (verified by `grep` over the whole
archive): `SeedSequence(20260823700)` self-tests, `(20260823701)` primary 18-cell
grid, `(20260823703)` second independent 18-cell grid, `(20260823704)` channel probe,
`(20260823705)` n-scaling, `(20260823706)` small-b probe, `(20260823707)` estimator
comparability. None of `20260822018`, `918302033`, `720330339`, `20260822901–904`,
`20260822910–911`, `20260822941–945` was reused.

Three deliberate method differences from the target.

**(i) Formula — closed form instead of nested trapezoids.**
The target evaluates `H(t)` by a 250-point uniform trapezoid inside a 400-point
uniform trapezoid. I found the inner integral in closed form. With `P = 1/(1−ρ)` and
the lineage's un-clipped `q_CLUST(s) = s/(1−ρ) = Ps`:

```
I(t) = ∫₀ᵗ (1−Ps)(1−s)^(−P) ds ,   substitute u = 1−s, 1−q = (1−P) + Pu
     = ∫_{1−t}^{1} [(1−P) + Pu] u^(−P) du
     = [1 − (1−t)^(1−P)] + (P/(2−P))·[1 − (1−t)^(2−P)]                (P ≠ 1, 2)

H(t) = t − (1−t)^P·I(t)
     = t + (1−t) − (1−t)^P − (P/(2−P))[(1−t)^P − (1−t)²]
     = 1 − (2/(2−P))(1−t)^P + (P/(2−P))(1−t)²                          (★)

φ_V4 = ∫₀¹ P(1−t)^(P−1) e^(−cH(t)) dt        T = ∫₀¹ (1−t)^P e^(−cH(t)) dt
φ_CAND = (1−ρ)·φ_V4
```

Checks built in: `H(0)=0`; `H(1⁻)=1`; `P=1 ⇒ H = 1 − 2(1−t) + (1−t)² = t²`, recovering
M-U exactly. (★) was verified against direct numerical inner quadrature at six values
of `t` in four cells to `<1e-10` (`ref_selftest.log`, `ref_formula.py` `__main__`).
The remaining 1-D integral is adaptive Gauss–Kronrod at `epsabs=epsrel=1e-13`, audited
against `mpmath` at 40 decimal digits (agreement `3e-14 … 1e-13`).

**(ii) Monte-Carlo engine — three independent constructions of everything.**
The mechanism's `R` is built by forward `π`-iteration and cross-checked, on 120 random
instances, against *two* further independent constructions: a `π`-cycle-offset
construction (decompose `π` into cycles, mark positions `p … p+b−1 mod L`) and a
backward `π^{−k}` membership test (the literal reading of the shadowing statement).
The cyclic set is computed by adaptive iterated squaring, audited on every 100th
production instance by vectorised in-degree peeling, and both were checked against
brute-force orbit following on 300 random maps. The cycle-predecessor map used for
the channel split was checked against literal orbit following.

**(iii) The `eps` estimator — the important difference.**
The target measures `eps` by rejection-sampling **one** `x₀ ∈ R` per walk and
simulating that walk step by step with a visited-stamp array. **I never simulate a
walk.** I build the whole functional graph, compute its exact cyclic set, and read

```
eps_hat = Σ_instances |cyc ∩ R|  /  Σ_instances |R|
```

which uses **every** point of `R` in **every** instance (≈3×10⁴ per instance at
n = 65536, instead of 1). Same wall time, ~10² × the events, and — decisively for a
referee — there is no walk bookkeeping that *could* be buggy: no visited stamps, no
chain handling, no arc-start accounting, no step budget. This is a deliberate
departure from the letter of the dispatch ("write your own walk-level simulator"): it
measures exactly the same quantity, by definition, and strictly dominates a walk
simulator in both precision and bug surface.

The two channels separate exactly as well. For cyclic `x`, its unique predecessor on
the cycle is `y = f^{−1}(x)` restricted to the cyclic set;

* `y ∉ R ⇒ f(y) = π(y) = x` — reached by a **normal π-step**, so `x` is necessarily a
  run start (the target's `n_norm_x0`);
* `y ∈ R` — reached by a uniform **f-draw** (the target's `n_rr_x0`).

Uncertainties are **cluster bootstrap over instances** (3000 replicates, resampled
jointly so ratios and derived quantities stay correlated), as this lineage requires.

**Estimator comparability** (`ref_estimator_check.py`). The target's stage-B estimator
converges to the *mean of ratios* `E[|cyc∩R|/|R|]`; mine is the *ratio of sums*
`E[|cyc∩R|]/E[|R|]`. The ratio of sums is the one that makes
`φ = (1−ρ)·φ(·|x₀∉R) + ρ·eps` an exact identity, because `E[|R|]/n = ρ` exactly, so it
is the right one to compare a formula against. The two differ by `−0.005 %`,
`−0.047 %`, `−0.109 %` in the three stress cells checked (`CV(|R|) = 0.029…0.080`) —
immaterial — but by `+4.4 %` in `b=8, c=10` where `CV(|R|) = 0.32`. Since the target
only measured cells with `c ≥ 100`, this affects nothing it claims; it is recorded so
the two sets of numbers are known to be comparable.

---

## 2. Was `eps = 0` ever reasonable? (independent judgement, formed before reading §5)

`R` splits into **run starts** (`π^{−1}(x) ∉ R`) and **shadowed interior members**.
`residual_attempt/ATTEMPT.md` §6 argues that a shadowed `x₀` "nunca pode ser alcançado
por um passo-π normal" — correct, and exactly wave 4's shadowing lemma. It then writes

> "se x₀ é um membro interior de bloco (fração ≈(b−1)/b de R, ou seja quase todo ρ),
> x₀ nunca pode ser alcançado por um passo-π normal … Logo φ(x₀ sombreado) ≈ 0"

and passes from `φ(shadowed) ≈ 0` to `eps ≈ 0`. That step drops the run-start
fraction `ρ_start/ρ = (c/n)(1−ρ)/ρ ≈ 1/b`, whose members are **ordinary live closure
targets**: a run start `p` is reachable by a π-step from `π^{−1}(p) ∉ R`, and the
sliding-window count gives it the *same* per-target hazard as any non-`R` arc start
(there are `c(1−ρ)` run starts and the walk meets one at rate `c` per unit mass, so
the per-run-start hazard is `1/((1−ρ)(1−t))` — exactly the elevation `φ_CAND` already
assigns). So a priori

```
eps ≈ (ρ_start/ρ)·(something of order φ_cond)  +  E[#f-draws]/n
```

— strictly positive and of order `φ_cond/b`, not zero. At `b = 8` that is ~12 % of
`φ_cond`; I measure `eps = 2.87×10⁻²` there against `φ = 0.279`. At `b = 1` I measure
`eps = 0.2298` against `φ_cond = 0.2799`. **`eps = 0` was never right.**

What makes the predecessor's mistake benign is that the term enters `φ` only through
`ρ·eps ≈ ρ_start·φ_cond = (c/n)·φ_CAND`, i.e. suppressed by `c/n`. And the
predecessor's quantitative escape clause — "remaining channel estimated ≤0.6 %,
negligible" — refers only to the f-draw channel and is about right for *it* (I measure
that channel at 0.4–0.9 % of `φ_cond` in the stress cells). It simply does not cover
the channel that dominates `eps`.

**So on this point the target is not merely right, it is right for the right reason.**

---

## 3. Cross-validation of my simulator (mandatory; done before trusting it)

`ref_analysis.py` §1. My `φ_mc` (18 cells × 20 000 instances) against `φ_mc` already
recorded by four earlier runs of this lineage under four different seeds:

| recorded grid | comparisons | \|z\|max | χ² / dof | mean z |
|---|---|---|---|---|
| `mclust_residual_validate_results.json` (720330339) | 18 | 1.92 | 15.1 / 18 | −0.07 |
| `mclust_aggregation_validate_results.json` (20260822904) | 18 | 2.25 | 26.2 / 18 | −0.23 |
| `mclust_global_validate_results.json` (20260822911) | 18 | 2.09 | 13.0 / 18 | +0.23 |
| `x0_asym_validate_results.json` (target, 20260822943) | 18 | 2.21 | 21.9 / 18 | −0.41 |
| **pooled** | **72** | **2.25** | **76.2 / 72** | **−0.120** |

No systematic offset; no outlier beyond 2.3σ. This exceeds the two-document standard
the mandate sets. As a by-product it establishes that **the lineage's quoted `φ_mc`
standard errors are well calibrated** (pooled χ²/dof = 1.06) — which is what makes
the χ² comparisons in §5.2 of the target interpretable at all.

---

## 4. `eps` measured, and the two errors in the §5.2 derivation

### 4.1 My independent leading-order derivation

Done before reading §5.2. Two channels, as the target has them:

* **Run-start channel.** `P(run start | x₀ ∈ R) = ρ_start/ρ`, `ρ_start = (c/n)(1−ρ)`.
* **f-draw channel.** Every f-draw is uniform on `[n]`, contributing `E[#draws]/n`.

Where I differ — and both differences live **inside the front's own master formula**,
not outside it.

#### (a) The run-start walk has TWO live targets at `t = 0`, not one

For `x₀ ∉ R` the walk *starts at* `x₀`, so `x₀` is simultaneously the unique live
closure target and the start of the arc being traversed: `K(0) = 1`, and the master
formula's base factor is `(1−t)^P`.

For `x₀` a **run start**, the walk starts with an f-draw to a fresh point `D₁`, and
`D₁` is itself a live closure target — closing into `D₁` kills. In the master
formula's own bookkeeping this is exactly *one extra reroute event forced at `s = 0`*,
whose per-event factor is `F(0) = (1−q(0))·((1−t)/(1−0))^P = (1−t)^P` since `q(0)=0`.
Hence

```
S_runstart(t) = (1−t)^P · S_cond(t) = (1−t)^(2P) · e^(−cH(t))
φ_runstart    = ∫₀¹ P (1−t)^(2P−1) e^(−cH(t)) dt   <   φ_cond = φ_V4
```

This is **not** a subleading correction. `φ_runstart/φ_V4` = **0.748** at `c=5`,
**0.821** at `c=10`, **0.926** at `c=50`, **0.943–0.967** at `c=150…600`.

§5.2 asserts the ratio is 1 — "x₀ é um alvo vivo desde t=0 com a mesma elevação que
qualquer arc start …, logo a probabilidade de retorno é, a ordem líder, o MESMO
φ_cond = φ_V4" — and labels the step heuristic. The *elevation* half of that sentence
is correct (I re-derived `1/(1−ρ)` for a run-start target independently, and my fits
confirm it). The *return probability* half is wrong at leading order, and the correct
leading order is available in closed form from the formalism the front already has.
**The "heuristic, labelled" tag therefore understates a real, removable error.**

#### (b) The f-draw count misses the opening chain

§5.2 writes `E[#draws] = (c/(1−ρ))·T`: reroute events met *later along the walk* at
rate `c` per unit traversed mass, times `1/(1−ρ)` draws per chain. But the walk from
**any** `x₀ ∈ R` *begins* with a draw at `x₀` itself, and that opening chain makes
`1/(1−ρ)` draws in expectation before any mass has been traversed. Hence

```
E[#draws] = (1 + c·T)/(1−ρ)          not   c·T/(1−ρ)
```

Referee's corrected leading order (`ref_formula.eps_ref`, `phi_EPSR`):

```
eps_ref = (ρ_start/ρ)·φ_runstart + (1 + c·T)/((1−ρ)·n)
φ_EPSR  = (1−ρ)·φ_V4 + ρ·eps_ref
```

### 4.2 `eps` measured — referee vs the target's stage B

`ref_analysis.py` §2, six stress cells, n = 65536, 20 000 instances each:

| b | c | referee `eps` (events) | target stage-B `eps` (events) | z(diff) | σ vs 0 (referee) |
|---|---|---|---|---|---|
| 50 | 400 | 1.1773e-3 ± 4.7e-6 (406 658) | 1.2075e-3 ± 5.6e-5 (483) | −0.54 | 252 |
| 100 | 400 | 8.0363e-4 ± 3.1e-6 (482 006) | 7.5800e-4 ± 3.9e-5 (379) | +1.15 | 258 |
| 100 | 600 | 8.6931e-4 ± 3.5e-6 (684 937) | 8.5000e-4 ± 4.2e-5 (425) | +0.46 | 248 |
| 200 | 150 | 5.6080e-4 ± 2.3e-6 (269 991) | 6.3667e-4 ± 4.5e-5 (191) | −1.67 | 242 |
| 300 | 150 | 4.7227e-4 ± 2.0e-6 (307 203) | 4.1500e-4 ± 3.2e-5 (166) | +1.80 | 241 |
| 400 | 100 | 3.9891e-4 ± 1.6e-6 (238 318) | 5.2333e-4 ± 4.2e-5 (157) | **−2.96** | 243 |

**`eps ≠ 0` is confirmed beyond any doubt.** Magnitudes agree in 5 of 6 cells. The
sixth is a +3.4σ upward Poisson fluctuation of the target's own 157-event sample
(157 observed against 119.7 expected from my 238 318-event measurement); two further
independent seeds give 3.935e-4 ± 3.4e-6 (`ref_estimator_check`) and 3.93e-4
(`ref_channel_probe`), i.e. the target's value is the outlier.

Over the six cells the referee-vs-target comparison gives χ² = 19.3/6 (p ≈ 0.004):
**the target's stage-B error bars look mildly under-dispersed** — the same phenomenon
the target itself flags as open item 2 of §6 (realisation-to-realisation scatter
≈1.8× the cluster-bootstrap sem). Nothing here threatens `eps ≠ 0`; it only means the
quoted **"12.5σ–21.7σ" should honestly be read as ≈8σ–14σ**.

Full 18-cell table (`ref_analysis.py` §2b): `eps` ranges 3.99e-4 … 2.87e-2, every cell
at 190σ–260σ from zero, and `ρ·eps/φ` ranges 0.01 % (b=200,c=5) to **2.26 %**
(b=100,c=600). For the six stress cells the range is 0.28 %–2.26 %, against the
target's claimed 0.36 %–2.19 % (the low end differs only because of the b=400/c=100
fluctuation above).

### 4.3 The two heuristic steps of §5.2, tested directly and model-free

`ref_channel_probe.py`, an independent fourth seed (20260823704), 6000 instances per
cell, 11 cells. Both §5.2 assertions are testable *exactly* from the functional graph:

* `P(cyclic via a π-step | x₀ is a run start)` — the quantity §5.2 claims equals
  `φ_cond`. Divided here by the **measured** `φ(cyclic|x₀∉R)` of the same instances,
  so no model enters the target's column; the referee's prediction is rescaled by the
  identical factor, so no model enters that one either.
* `E[N]`, the expected number of f-draws. `P(channel B) = E[N]/n` **exactly** (the
  draws are i.i.d. uniform on `[n]`, `N` is a stopping time with respect to them, and
  at most one draw can hit `x₀` since it terminates the walk — Wald). So the channel-B
  rate *is* a measurement of `E[N]`, with no walk simulated.

| n | b | c | ρ | P(cyc via π \| run start) | ÷ measured `φ_cond` — **target's claim** | ÷ rescaled `φ_runstart` — **referee's** | `E[N]` measured | `E[N]` target | `E[N]` referee |
|---|---|---|---|---|---|---|---|---|---|
| 32768 | 8 | 10 | 0.0024 | 0.22794 ± 0.00198 | **0.819** | **0.997** | 3.68 ± 0.50 | 2.31 | **3.31** |
| 32768 | 8 | 160 | 0.0384 | 0.06876 ± 0.00049 | **0.955** | **1.000** | 12.07 ± 0.25 | 10.92 | **11.96** |
| 65536 | 50 | 10 | 0.0076 | 0.22903 ± 0.00192 | **0.835** | **1.017** | 3.49 ± 0.28 | 2.31 | **3.32** |
| 65536 | 200 | 5 | 0.0151 | 0.29620 ± 0.00279 | **0.753** | **1.006** | 2.45 ± 0.16 | 1.49 | **2.51** |
| 65536 | 100 | 150 | 0.2048 | 0.07617 ± 0.00055 | **0.945** | **0.996** | 12.72 ± 0.14 | 11.59 | **12.85** |
| 65536 | 50 | 400 | 0.2637 | 0.04967 ± 0.00035 | **0.967** | **0.999** | 21.52 ± 0.19 | 20.04 | **21.40** |
| 65536 | 200 | 150 | 0.3676 | 0.08573 ± 0.00062 | **0.946** | **1.003** | 14.57 ± 0.14 | 12.96 | **14.54** |
| 65536 | 100 | 400 | 0.4579 | 0.05759 ± 0.00040 | **0.958** | **0.995** | 24.80 ± 0.20 | 23.30 | **25.14** |
| 65536 | 400 | 100 | 0.4571 | 0.11146 ± 0.00082 | **0.928** | **1.002** | 12.85 ± 0.13 | 11.26 | **13.10** |
| 65536 | 300 | 150 | 0.4971 | 0.09587 ± 0.00070 | **0.941** | **1.004** | 16.35 ± 0.15 | 14.49 | **16.47** |
| 65536 | 100 | 600 | 0.6014 | 0.05501 ± 0.00038 | **0.967** | **1.003** | 35.27 ± 0.28 | 33.39 | **35.90** |

**Eleven cells out of eleven, both channels, with no model in the denominator.** The
target's run-start step is low by 3.3 %–24.7 %, its f-draw step is low by 8 %–64 %; the
referee's corrected forms are right to 0.3 %–1.7 % and to well inside the statistical
error respectively. These are the two steps §5.2 flags as "heuristic, labelled".

### 4.4 The channels across the whole grid — measured / derived, 18 cells

`tgt` = the target's §5.2 leading order; `ref` = the corrected one of §4.1.

| n | b | c | run-start meas/tgt | run-start meas/ref | f-draw meas/tgt | f-draw meas/ref |
|---|---|---|---|---|---|---|
| 32768 | 8 | 10 | **0.817** | 0.994 ± 0.004 | **1.436** | 1.001 ± 0.078 |
| 32768 | 8 | 40 | 0.910 | 0.999 | 1.211 | 1.012 |
| 32768 | 8 | 160 | 0.961 | 1.006 | 1.090 | 0.995 |
| 65536 | 50 | 10 | **0.823** | 1.002 | **1.527** | 1.063 |
| 65536 | 50 | 50 | 0.926 | 1.008 | 1.171 | 0.995 |
| 65536 | 50 | 150 | 0.953 | 1.001 | 1.098 | 0.996 |
| 65536 | 50 | 400 | 0.972 | 1.004 | 1.070 | 1.002 |
| 65536 | 100 | 10 | **0.824** | 1.004 | **1.549** | 1.077 |
| 65536 | 100 | 50 | 0.923 | 1.006 | 1.204 | 1.020 |
| 65536 | 100 | 150 | 0.947 | 0.999 | 1.106 | 0.998 |
| 65536 | 100 | 400 | 0.980 | 1.018 | 1.076 | 0.997 |
| 65536 | 100 | 600 | 0.967 | 1.002 | 1.056 | 0.983 |
| 65536 | 200 | 5 | **0.753** | 1.006 | **1.741** | 1.036 |
| 65536 | 200 | 20 | 0.876 | 1.006 | 1.330 | 1.025 |
| 65536 | 200 | 60 | 0.927 | 1.006 | 1.181 | 1.007 |
| 65536 | 200 | 150 | 0.961 | 1.019 | 1.120 | 0.999 |
| 65536 | 300 | 150 | 0.961 | 1.026 | 1.132 | 0.995 |
| 65536 | 400 | 100 | 0.941 | 1.016 | 1.157 | 0.994 |

The target's two channels are wrong **in the same direction in every one of 18 cells**,
with a clean monotone dependence on `c` — the signature of a missing term, not of
Poisson noise. The corrected forms land within 0.1–2.6 % everywhere, the residual
scatter being an order of magnitude smaller than the errors removed.

#### The f-draw channel, stated as an exact expectation

`P(channel B) = E[N]/n` **exactly**, where `N` is the number of f-draws the walk makes:
the draws are i.i.d. uniform on `[n]`, `N` is a stopping time with respect to them, at
most one draw can hit `x₀` (it terminates the walk), so Wald gives
`P = E[Σ_{i≤N} 1{D_i = x₀}] = E[N]/n`. So my channel-B measurement *is* a measurement
of `E[N]`, with no walk simulated:

| n | b | c | **E[N] measured** | target `cT/(1−ρ)` | referee `(1+cT)/(1−ρ)` |
|---|---|---|---|---|---|
| 32768 | 8 | 10 | 3.310 ± 0.259 | 2.305 | **3.308** |
| 32768 | 8 | 40 | 6.210 ± 0.181 | 5.129 | **6.139** |
| 32768 | 8 | 160 | 11.904 ± 0.134 | 10.919 | **11.959** |
| 65536 | 50 | 10 | 3.528 ± 0.153 | 2.311 | **3.319** |
| 65536 | 50 | 50 | 6.880 ± 0.102 | 5.875 | **6.914** |
| 65536 | 50 | 150 | 12.028 ± 0.092 | 10.955 | **12.076** |
| 65536 | 50 | 400 | 21.441 ± 0.110 | 20.039 | **21.397** |
| 65536 | 100 | 10 | 3.592 ± 0.114 | 2.319 | **3.335** |
| 65536 | 100 | 50 | 7.208 ± 0.077 | 5.985 | **7.064** |
| 65536 | 100 | 150 | 12.817 ± 0.078 | 11.588 | **12.846** |
| 65536 | 100 | 400 | 25.074 ± 0.111 | 23.295 | **25.140** |
| 65536 | 100 | 600 | 35.267 ± 0.155 | 33.386 | **35.895** |
| 65536 | 200 | 5 | 2.600 ± 0.093 | 1.493 | **2.508** |
| 65536 | 200 | 20 | 4.745 ± 0.068 | 3.567 | **4.630** |
| 65536 | 200 | 60 | 8.217 ± 0.063 | 6.959 | **8.160** |
| 65536 | 200 | 150 | 14.520 ± 0.078 | 12.960 | **14.542** |
| 65536 | 300 | 150 | 16.397 ± 0.081 | 14.485 | **16.474** |
| 65536 | 400 | 100 | 13.020 ± 0.068 | 11.256 | **13.098** |

The measured excess over the target's formula is `1.00, 1.08, 0.99, 1.22, 1.01, 1.07,
1.40, 1.27, 1.22, 1.23, 1.78, 1.88, 1.11, 1.18, 1.26, 1.56, 1.91, 1.76` draws against
the predicted `1/(1−ρ) = 1.00 … 2.51`. The `+1` is confirmed cell by cell; the only
cell where the corrected form is off by more than 1.5 % is `b=100, c=600` (ρ = 0.60),
at −1.7 %, which I report as the honest edge of the leading-order account.

#### This settles review item 8

The target's own reported channel ratios (§5.2: run-start **0.75–1.17**, f-draw
**0.99–1.53**) recompute, from its own retained
`x0_asymmetry_walk_measure_B_results.json` and my high-precision formulas, to
**0.757–1.222** and **0.990–1.533**. The f-draw range matches the document exactly.
The run-start upper end is **1.222, not the 1.17 the document states** for
b=400/c=100 — a transcription-level inaccuracy that happens to flatter the derivation.

More importantly, **the document's explanation for the scatter is wrong**:

> "as duas piores razões do canal sorteio-f … são as de menor contagem — 79 e 70
> eventos, ou seja 11 %–12 % de erro estatístico só de Poisson"

With 10²–10³× more events the deviations are systematic, of opposite sign in the two
channels, monotone in `c`, and removable by a derivation the front could have done
with the machinery it already had. The Poisson reading was a defensible
interpretation of six noisy numbers; it is not what is going on.

### 4.5 Two further out-of-sample confirmations

**n-scaling** (`ref_nscaling.py`, seed 20260823705) — a direction the target never
probed. Same `(b,c)`, `n` varied 4×, so `ρ` sweeps 0.26 → 0.71:

| n | b | c | ρ | `eps` meas/tgt | meas/ref | run-start meas/tgt | meas/ref | f-draw meas/tgt | meas/ref |
|---|---|---|---|---|---|---|---|---|---|
| 32768 | 100 | 400 | 0.7072 | 1.041 | 0.981 | 0.952 | 1.003 | 1.078 | 0.973 |
| 65536 | 100 | 400 | 0.4579 | 1.020 | 1.005 | 0.973 | 1.012 | 1.076 | 0.997 |
| 131072 | 100 | 400 | 0.2633 | 1.001 | 1.007 | 0.974 | 1.007 | 1.076 | 1.007 |
| 32768 | 200 | 150 | 0.6005 | 1.075 | 1.011 | 0.956 | 1.028 | 1.156 | 1.001 |
| 65536 | 200 | 150 | 0.3676 | 1.003 | 0.996 | 0.944 | 1.001 | 1.109 | 0.988 |
| 131072 | 200 | 150 | 0.2047 | 0.987 | 1.007 | 0.955 | 1.007 | 1.118 | 1.008 |

Note the pattern: the target's **f-draw** ratio is stuck at ≈1.076 for `(100,400)` and
≈1.11–1.16 for `(200,150)` *independently of `n`* — a constant multiplicative miss, which
is exactly what a missing additive `1/(1−ρ)` in `E[#draws]` produces at fixed `(b,c,ρ)`;
and the target's **run-start** ratio is stuck at ≈0.95–0.97, which is
`φ_runstart/φ_V4` at that `c`. Noise does not behave like that.

**Small `b`, including `b = 1` (M-CLUST(1) ≡ M-U)** (`ref_smallb_probe.py`, seed
20260823706), where `ρ_start/ρ → 1 − c/n` and the run-start channel essentially *is*
`eps`, so the two competing accounts differ by up to 25 %. The measured quantity is
`P(cyclic via a π-step | x₀ is a run start)` — the exact object §5.2 claims equals
`φ_cond`:

| n | b | c | ρ | run-start fraction meas / formula | P(cyc via π \| run start) | ÷ `φ_V4` (target) | ÷ `φ_runstart` (referee) |
|---|---|---|---|---|---|---|---|
| 16384 | 1 | 10 | 0.00061 | 0.99936 / 0.99939 | 0.22981 ± 0.00104 | **0.820** (−48.7σ) | **0.998** (−0.6σ) |
| 16384 | 1 | 50 | 0.00305 | 0.99688 / 0.99695 | 0.11539 ± 0.00046 | **0.919** | **0.999** |
| 16384 | 1 | 200 | 0.01221 | 0.98772 / 0.98779 | 0.06083 ± 0.00023 | 0.965 | 1.005 |
| 16384 | 2 | 50 | 0.00609 | 0.49766 / 0.49771 | 0.11515 ± 0.00047 | 0.916 | 0.996 |
| 16384 | 4 | 50 | 0.01215 | 0.24803 / 0.24810 | 0.11633 ± 0.00047 | 0.923 | 1.004 |
| 16384 | 8 | 50 | 0.02415 | 0.12324 / 0.12329 | 0.11592 ± 0.00048 | 0.915 | 0.995 |
| 65536 | 1 | 50 | 0.00076 | 0.99920 / 0.99924 | 0.11599 ± 0.00060 | 0.925 | 1.005 |
| 65536 | 2 | 400 | 0.01217 | 0.49543 / 0.49543 | 0.04332 ± 0.00021 | 0.972 | 1.000 |

**Model-free version of the same test.** Both columns above divide by a *modelled*
`φ_cond`, so one could object that the master formula's own finite-n bias is doing the
work. It is not. Dividing instead by the **measured** `φ(cyclic | x₀ ∉ R)` of the same
instances (and rescaling the referee's prediction by the identical factor
`φ_notR,measured / φ_V4`, which cancels that bias):

| n | b | c | P(cyc via π \| run start) | ÷ measured `φ(·\|x₀∉R)` = target's claim | ÷ rescaled `φ_runstart` = referee's claim |
|---|---|---|---|---|
| 16384 | 1 | 10 | 0.22981 | **0.8186** | **0.9964** |
| 16384 | 1 | 50 | 0.11539 | 0.9238 | 1.0040 |
| 16384 | 1 | 200 | 0.06083 | 0.9607 | 1.0009 |
| 16384 | 2 | 50 | 0.11515 | 0.9200 | 1.0000 |
| 16384 | 4 | 50 | 0.11633 | 0.9223 | 1.0027 |
| 16384 | 8 | 50 | 0.11592 | 0.9199 | 1.0006 |
| 65536 | 1 | 50 | 0.11599 | 0.9156 | 0.9950 |
| 65536 | 2 | 400 | 0.04332 | 0.9727 | 1.0012 |

At `b = 1, c = 10` the target's claim is wrong by 18 % at **−48.7σ**; the referee's
closed form is right to 0.4 % or better in all eight cells, with no model input at all. Across `b ∈ {1,2,4,8,50,100,200,300,400}`,
`c ∈ [5, 600]`, `n ∈ [16384, 131072]`, `ρ ∈ [0.0006, 0.71]` the corrected form holds to
0.1–2.8 % while the target's is wrong by 3–25 %. The run-start-fraction formula
`ρ_start/ρ` itself is confirmed to 5 decimal places, so the error is entirely in the
per-run-start return probability, exactly as §4.1(a) predicts.

---

## 5. Does `φ_EPS` improve on `φ_CAND`? (review items 6, 7)

### 5.1 Quadrature audit — no numerical artefact (review item 7b, part 1)

`ref_quadrature_audit.py` runs the target's own `phi_CAND` / `phi_EPS` (400×250
uniform trapezoid) against my adaptive Gauss–Kronrod on the closed-form `H`, on all 18
cells. **Worst relative disagreement: 3.5×10⁻⁵ for both formulas** — three orders of
magnitude below the effect being claimed (`φ_EPS − φ_CAND` = 0.008 % … 2.28 %) and two
orders below the Monte-Carlo errors. The target's coarse-looking trapezoid is fine
because the integrand is a near-Gaussian with `f'(0)=0`, where the trapezoid rule is
super-algebraically accurate.

Also verified: `φ_EPS → φ_CAND` as `c/n → 0`, with the relative gap exactly `∝ c/n`
(`+5.0e-7` at n=10⁸, `+4.0e-7` at n=10⁹, `+4.0e-8` at n=10¹⁰), matching the target's
"diff < 5e-7 relativo" claim.

And the whole formula chain closes: my independently derived closed-form `φ_CAND`
agrees with the `phi_cand` column **recorded by all three predecessor validators**
(54 cells) to a worst relative difference of **4.6×10⁻⁵**. So the formula of record,
the target's re-implementation of it, and my from-scratch closed form are the same
object.

### 5.2 The four already-recorded grids recompute as claimed (review item 7b)

`ref_recorded_grids.py`, my own formulas, reading only the `phi_mc`/`sem` columns out
of the predecessors' JSON:

| grid | target's claim | referee recomputation | `φ_EPSR` (corrected) |
|---|---|---|---|
| `residual_attempt` (720330339) | 81.54 → 49.99 | **81.60 → 50.03** | 49.58 |
| `aggregation_closure` (20260822904) | 73.57 → 46.59 | **73.63 → 46.61** | 46.52 |
| `global_exclusion` (20260822911) | 79.99 → 44.13 | **80.06 → 44.17** | 43.58 |
| target fresh (20260822943) | 121.69 → 71.98 | **121.78 → 72.04** | 71.40 |

Every claimed number reproduces to <0.1 in χ²; the tiny residue is exactly the
quadrature difference of §5.1. **Review item 7(b): confirmed.**

### 5.3 My own fresh 18-cell grid — 20 000 instances per cell (4× the target's precision)

Seed 20260823701 (`ref_analysis.py` §4):

| n | b | c | ρ | `φ_mc` (sem) | `φ_CAND` dev % (z) | `φ_EPS` dev % (z) | `φ_EPSR` dev % (z) |
|---|---|---|---|---|---|---|---|
| 32768 | 8 | 10 | 0.0024 | 0.279286 (0.001036) | −0.189 (−0.51) | −0.219 (−0.59) | −0.214 (−0.58) |
| 32768 | 8 | 40 | 0.0097 | 0.139042 (0.000517) | −0.226 (−0.61) | −0.348 (−0.94) | −0.338 (−0.91) |
| 32768 | 8 | 160 | 0.0384 | 0.069251 (0.000250) | +0.917 (+2.52) | +0.408 (+1.13) | +0.428 (+1.18) |
| 65536 | 50 | 10 | 0.0076 | 0.281422 (0.001034) | +0.907 (+2.45) | +0.891 (+2.40) | +0.894 (+2.41) |
| 65536 | 50 | 50 | 0.0374 | 0.123703 (0.000454) | +0.817 (+2.21) | +0.737 (+2.00) | +0.743 (+2.01) |
| 65536 | 50 | 150 | 0.1083 | 0.068389 (0.000261) | +0.446 (+1.16) | +0.190 (+0.50) | +0.199 (+0.52) |
| 65536 | 50 | 400 | 0.2637 | 0.038285 (0.000145) | +1.282 (+3.35) | +0.455 (+1.20) | +0.460 (+1.21) |
| 65536 | 100 | 10 | 0.0151 | 0.279045 (0.001040) | +0.540 (+1.44) | +0.524 (+1.40) | +0.527 (+1.41) |
| 65536 | 100 | 50 | 0.0735 | 0.120851 (0.000450) | +0.604 (+1.61) | +0.522 (+1.39) | +0.527 (+1.41) |
| 65536 | 100 | 150 | 0.2048 | 0.064203 (0.000238) | +0.222 (+0.60) | −0.063 (−0.17) | −0.058 (−0.16) |
| 65536 | 100 | 400 | 0.4579 | 0.033121 (0.000122) | +2.727 (+7.22) | +1.594 (+4.27) | +1.577 (+4.22) |
| 65536 | 100 | 600 | 0.6014 | 0.023183 (0.000088) | +3.002 (+7.71) | +0.709 (+1.86) | +0.641 (+1.68) |
| 65536 | 200 | 5 | 0.0151 | 0.393200 (0.001437) | +0.437 (+1.19) | +0.429 (+1.17) | +0.431 (+1.17) |
| 65536 | 200 | 20 | 0.0592 | 0.192795 (0.000712) | +0.865 (+2.32) | +0.833 (+2.24) | +0.836 (+2.25) |
| 65536 | 200 | 60 | 0.1674 | 0.104238 (0.000391) | +0.780 (+2.06) | +0.671 (+1.77) | +0.675 (+1.79) |
| 65536 | 200 | 150 | 0.3676 | 0.058162 (0.000216) | +2.561 (+6.73) | +2.196 (+5.79) | +2.193 (+5.78) |
| 65536 | 300 | 150 | 0.4971 | 0.052066 (0.000194) | +3.731 (+9.64) | +3.268 (+8.48) | +3.252 (+8.44) |
| 65536 | 400 | 100 | 0.4571 | 0.065254 (0.000240) | +2.365 (+6.27) | +2.083 (+5.54) | +2.074 (+5.52) |

```
chi2 (18 cells, seed 20260823701):  CAND = 335.6   EPS = 185.2   EPSR = 183.6
formula below MC in 16 / 15 / 15 of 18 cells
```

**The improvement is confirmed on a fresh grid with a fresh seed, an independent
simulator and independent quadrature**, at 4× the target's precision. (My χ² values
are ~2.8× the target's simply because my sems are ~2× smaller; what matters is the
ratio and the deviations, both of which reproduce.)

### 5.4 Second independent seed (review item 7a)

Seed 20260823703, 18 cells × 20 000 instances (`ref_analysis.py` §6):

```
chi2 (18 cells, seed 20260823703):  CAND = 298.8   EPS = 153.8   EPSR = 152.6
formula below MC in 15 / 14 / 14 of 18 cells
```

Cell-by-cell the two referee grids agree: **χ² = 22.6 / 18** on `φ_mc`
(sem calibration factor 1.12, |z|max = 2.51) and **χ² = 15.5 / 18** on `eps`
(|z|max = 1.82). So my error bars are honest and `eps` reproduces across seeds.

**The improvement factor is stable across all six independent grids:**

| grid | χ²(`φ_CAND`) | χ²(`φ_EPS`) | ratio |
|---|---|---|---|
| `residual_attempt` (720330339) | 81.60 | 50.03 | 1.63 |
| `aggregation_closure` (20260822904) | 73.63 | 46.61 | 1.58 |
| `global_exclusion` (20260822911) | 80.06 | 44.17 | 1.81 |
| target fresh (20260822943) | 121.78 | 72.04 | 1.69 |
| **referee grid A (20260823701)** | **335.6** | **185.2** | **1.81** |
| **referee grid C (20260823703)** | **298.8** | **153.8** | **1.94** |

**Review item 7(a): the improvement is not seed-dependent.**

### 5.5 The decisive test: replace the model by the measurement

`φ = (1−ρ)·φ(cyclic|x₀∉R) + ρ·eps` is an **exact identity**. So the only open question
about the `eps` term is whether the *model* is accurate. Substituting my directly
measured `eps`:

```
chi2 (18 cells, seed 20260823701):
    phi_CAND                       = 335.6
    phi_EPS  (target's model eps)  = 185.2
    phi_EPSR (referee's model eps) = 183.6
    phi_CAND + rho * eps_MEASURED  = 183.2      <-- the exact term
```

**The eps channel is exhausted.** A perfect model of `eps` would buy 2.0 units of χ²
out of the 165 that remain (1.2 %). `φ_EPS` already captures 99 % of the achievable
gain; `φ_EPSR` captures 99.8 %. No future front should spend effort here.

### 5.6 Where the residual actually is (corroborates §5.3; out of scope, reported free)

My measurement also gives `φ(cyclic | x₀ ∉ R)` directly, which is exactly what
`φ_V4` is supposed to model:

| b, c | ρ | measured `φ(·|x₀∉R)` | `φ_V4` | dev |
|---|---|---|---|---|
| 8, 10 | 0.0024 | 0.279900 | 0.280497 | −0.21 % |
| 8, 40 | 0.0097 | 0.140249 | 0.140725 | −0.34 % |
| 8, 160 | 0.0384 | 0.071668 | 0.071362 | +0.43 % |
| 50, 10 | 0.0076 | 0.283540 | 0.281029 | +0.89 % |
| 50, 50 | 0.0374 | 0.128417 | 0.127474 | +0.74 % |
| 50, 150 | 0.1083 | 0.076492 | 0.076350 | +0.19 % |
| 50, 400 | 0.2637 | 0.051562 | 0.051338 | +0.44 % |
| 100, 10 | 0.0151 | 0.283288 | 0.281814 | +0.52 % |
| 100, 50 | 0.0735 | 0.130343 | 0.129652 | +0.53 % |
| 100, 150 | 0.2048 | 0.080493 | 0.080559 | −0.08 % |
| 100, 400 | 0.4579 | 0.060385 | 0.059471 | +1.54 % |
| 100, 600 | 0.6014 | 0.056811 | 0.056463 | +0.62 % |
| 200, 5 | 0.0151 | 0.399228 | 0.397510 | +0.43 % |
| 200, 20 | 0.0592 | 0.204830 | 0.203173 | +0.82 % |
| 200, 60 | 0.1674 | 0.124975 | 0.124225 | +0.60 % |
| 200, 150 | 0.3676 | 0.091603 | 0.089679 | +2.14 % |
| 300, 150 | 0.4971 | 0.102897 | 0.099814 | **+3.09 %** |
| 400, 100 | 0.4571 | 0.119574 | 0.117418 | **+1.84 %** |

This is the residual, essentially in full, and it lives entirely in `φ_V4` — i.e. in
the elevation model. **Independent confirmation of the target's §5.3 localisation**,
obtained by a completely different route (no HT estimator, no walk, no `λ` fitting).

### 5.7 Was anything tuned after seeing validation data? (review item 7c)

**No.** Evidence:

* File mtimes: `x0_asym_candidate.py` **21:21:47Z**; `x0_asym_validate.py`
  **21:23:22Z**; `x0_asym_validate_results.json` **21:27:24Z**. The candidate was
  never touched after the fresh validation produced numbers.
* `PROGRESS.log` 21:23:52Z announces the derivation plus the *cheap triage* on
  already-recorded data (χ² 80.0 → 44.1, the 911 grid) and says the fresh-seed
  validation was launched afterwards; 21:37:03Z reports its result. Order: derive →
  triage on old data → validate out of sample. Consistent.
* The formula has **no free parameter**; there is nothing that *could* be fitted.
* The strongest evidence is adversarial rather than documentary: the published
  derivation **under-fits the front's own measured channel ratios** (0.76–1.22 and
  0.99–1.53 rather than 1.00). Nobody tuning to their own data publishes that. This
  is the fingerprint of an honest, incomplete derivation.

One caveat the document itself records: the two channels were *identified* after
stage B existed and were "conferido contra a medição do estágio B antes de ser
escrito como fórmula". That is measurement-guided model *selection*, not parameter
fitting; the fresh-seed grid is genuinely out of sample, and two independent referee
grids reproduce it.

### 5.8 One honest caveat about what the χ² reduction proves

`φ_CAND` is below the Monte-Carlo mean in 16–18 of 18 cells on every grid tested. Any
strictly positive additive correction of roughly the right size would therefore reduce
χ². **The χ² reduction alone is weak evidence for the specific functional form.**
What makes `φ_EPS` sound is not the χ² number but §5.5: the term it adds belongs to an
exact decomposition, and its modelled value now agrees with the directly measured
value to within 1 % of the achievable χ² gain. The archive should record the claim on
*that* basis, not on the χ² basis the target leads with.

---

## 6. Errors and inaccuracies found in the target document

Ordered by importance. **None overturns either headline claim.**

1. **§5.2, run-start channel — wrong at leading order.** "logo a probabilidade de
   retorno é, a ordem líder, o MESMO φ_cond = φ_V4". It is
   `φ_runstart = ∫P(1−t)^{2P−1}e^{−cH}dt`, i.e. `φ_cond` is 2 %–33 % too high over the
   grid, because the run-start walk carries **two** live targets from `t=0` rather than
   one. Demonstrated model-free at −48.7σ in `b=1, c=10`. Labelled "heuristic", but the
   label understates a derivable, removable leading-order error. (§4.1a, §4.3, §4.4,
   §4.5)
2. **§5.2, f-draw channel — missing the opening chain.**
   `E[#draws] = cT/(1−ρ)` should be `(1+cT)/(1−ρ)`; the published form is 5 %–43 % too
   low, confirmed cell by cell against an *exact* measurement of `E[N]` in 18 + 11
   cells. (§4.1b, §4.3, §4.4)
3. **§5.2, the "Poisson noise" explanation for the channel-ratio scatter is wrong.**
   The scatter is systematic, of opposite sign in the two channels, and monotone in
   `c`. (§4.3)
4. **§5.1, "onde a forma derivada erra" is misdiagnosed.** The document names
   b=400/c=100 (−3.3σ) and b=200/c=150 (−1.9σ) as the failing cells. With 10³× more
   events the derived value there is 3.6 % and 1.8 % low — *among the better cells* —
   and the apparent failure was an upward fluctuation of the front's own 157- and
   191-event samples. The real failure pattern is a near-uniform +2 % … +4.5 %
   underestimate driven by items 1–2.
5. **§5.2, minor numerical inaccuracy.** The stated run-start ratio range
   "0,75–1,17" recomputes from the front's own retained JSON as 0.757–**1.222**; the
   1.17 attributed to b=400/c=100 is 1.222.
6. **§5.1 significance framing.** "12,5–21,7σ" is correct Poisson arithmetic on the
   front's counts, but its own §6 open-item 2 says its sems are under-dispersed ≈1.8×,
   and my 6-cell comparison against a 10³× larger sample gives χ² = 19.3/6. The honest
   range is **≈8σ–14σ**. Immaterial to the claim.
7. **Traceability gap.** The channel-ratio numbers quoted in §5.2 exist only in the
   prose — no script in the subfolder computes or persists them (`x0_asym_analysis.py`
   does not; `x0_asym_candidate.py`'s `__main__` prints only the χ² triage). Every
   other number in §5 is backed by a retained artefact.
8. **§5.4 (context only, out of scope).** "φ_CAND fica ABAIXO da média MC em 18 de 18
   células" is partly seed luck: on my two 20 000-instance grids it is **16/18** and
   **15/18**, with the `b=8` low-ρ cells landing negative. The *direction* of the
   observation survives (16/18 has binomial p = 0.0012; 15/18 p = 0.008); "18 of 18"
   does not, and the four `ρ ≤ 0.015` cells the front singles out come out
   −0.19 %, −0.23 %, +0.54 %, +0.44 % (grid A) and −0.17 %, +0.05 %, −0.22 %, −0.19 %
   (grid C) — i.e. consistent with zero, not with a uniform positive offset. This
   weakens (it does not refute) the premise of §5.4's opening paragraph; §5.4's own
   conclusion, that the master formula's finite-n bias is O(1/n) and negligible at
   n = 65536, is unaffected.

---

## 7. What I attacked and could not break

* the mechanism implementation — three independent constructions of `R` agree on 120
  random instances, and my `|R|` and run-start densities match `ρ` and `ρ_start` to 5
  decimal places;
* the cyclic-set computation — three algorithms agree (adaptive squaring, vectorised
  in-degree peeling, brute-force orbit following), with in-run auditing;
* the master-formula quadrature — the target's trapezoid is good to 3.5×10⁻⁵;
* the `φ_mc` values of the whole lineage — 72 comparisons, χ²/dof = 1.06, no offset;
* the four claimed χ² reductions — all reproduce to <0.1;
* the sign, order of magnitude and cell-by-cell pattern of `eps`;
* `φ_EPS → φ_CAND` as `c/n → 0` — relative gap exactly ∝ c/n;
* the absence of post-hoc tuning;
* the target's §4 discipline as it bears on §5 — the primary refutation's replication
  practice is what caught the −3.7σ non-replication, and the same practice is what
  I found *missing* from stage B (single realisation, 157–483 events, no replication),
  which is precisely where its one wrong cell-level statement came from.

---

## 8. Assessment of the target's honesty and scorecard (review item 9)

The document does **not** overclaim. §5.2 states explicitly that `φ_EPS` "não fecha o
resíduo (χ²=72 contra ~18 esperado por ruído puro)", that it is "pequena comparada ao
que falta", that the bulk of the residual is in the elevation level (§5.3), and that
the claim "exige verificação adversarial independente antes de qualquer catalogação, e
esta frente NÃO a declara integrada nem substitui φ_CAND como fórmula de registro".
§7 and §8 repeat this. The three scorecard rows in scope:

| scorecard row | referee finding |
|---|---|
| `eps ≠ 0` — **ESTABELECIDO** | **Accurate**, with the σ range restated as ≈8–14σ rather than 12.5–21.7σ. |
| `φ_EPS melhora φ_CAND` — **SIM, com sementes novas** | **Accurate**, and reproduced on two further independent grids. |
| `φ_EPS fecha o resíduo` — **não** | **Accurate**, and strengthened: the term is now *exhausted*. |

The one place the document is less accurate than it needed to be is the internal
diagnosis of its own derivation (items 1–4 of §6), where it accepted a noise
explanation for a structural discrepancy it had the tools to resolve. That is a
failure of adversarial pressure on its own secondary finding, not of honesty: the
front labelled the step heuristic, published the discrepant ratios rather than hiding
them, and referred the whole claim out for exactly this review.

---

## 9. Files produced by this review (all in `adversarial/`)

| file | role |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref_formula.py` | own closed-form `H`, adaptive-quadrature `φ_V4`/`T`/`φ_CAND`/`φ_EPS`, the referee's `φ_runstart`, `eps_ref`, `φ_EPSR`; mpmath audit. `python3 ref_formula.py` runs the self-checks |
| `ref_mclust_mc.py` | own M-CLUST(b) engine and the walk-free `eps` estimator with exact channel split. `python3 ref_mclust_mc.py selftest` runs all consistency checks |
| `ref_selftest.log` | output of that selftest |
| `ref_formula_selfcheck.log` | closed-form `H` vs numeric inner integral; `ρ→0 ⇒ φ_U`; scipy vs mpmath(40 dps) |
| `ref_quadrature_audit.py` / `.log` | the target's trapezoid vs high precision, 18 cells |
| `ref_recorded_grids.py` / `.log` | recomputation of the four claimed χ² reductions |
| `ref_mc_A_*.json` | primary 18-cell grid, seed 20260823701, 20 000 instances/cell |
| `ref_mc_C_*.json` | second independent 18-cell grid, seed 20260823703 |
| `ref_channel_probe.py` / `.log` / `.json` | direct test of the two §5.2 heuristic steps, seed 20260823704 |
| `ref_nscaling.py` / `.log` / `.json` | n-scaling out-of-sample test, seed 20260823705 |
| `ref_smallb_probe.py` / `.log` / `.json` | small-`b` (incl. `b=1`) probe, seed 20260823706 |
| `ref_estimator_check.py` / `.log` / `.json` | ratio-of-sums vs mean-of-ratios comparability, seed 20260823707 |
| `ref_analysis.py` / `ref_analysis.log` | all cross-validation, `eps`, channel and χ² tables |
| `parts/` | per-cell stdout of the parallel grid runs |

---

## 10. Recommendation

**(A) `eps ≠ 0` — integrate as an ESTABLISHED FACT.**
It is a direct measurement, now replicated by an independent referee with an
independent method and 10²× the statistics, in 18 cells rather than 6, on four
independent seeds. The expressed assumption `eps = 0` in `φ_CAND`, `φ_CAND5` and
`φ_GLOBAL` is wrong; the magnitude is `ρ·eps` = 0.01 %–2.3 % of `φ`. Record the
significance as ≈8σ–14σ per stress cell rather than 12.5σ–21.7σ, and record the
mechanism: the assumption failed because the *run-start* sub-population of `R`
(density `ρ_start = (c/n)(1−ρ)`, i.e. ≈1/b of `R`) consists of ordinary live closure
targets, not shadowed points.

**(B) `φ_EPS` — catalogue as an adversarially verified improvement over `φ_CAND`,
with the derivation corrected.**
`φ_EPS` is strictly better than `φ_CAND` on all six grids tested (four recorded, two
fresh referee grids), is parameter-free, reduces to `φ_CAND` as `c/n → 0`, never
materially overshoots, and adds a term that provably belongs to an exact
decomposition. It should not be rejected merely because its derivation is imperfect —
omitting the term would be *knowingly* wrong.

However, cataloguing §5.2 **as written** would enshrine in the archive the statement
"P(cyclic | x₀ is a run start) = φ_cond at leading order", which is false by 18 % at
`b=1, c=10` and by 3–7 % in the stress cells, and the statement
`E[#f-draws] = cT/(1−ρ)`, which is low by 4–74 %. Both are the kind of reusable
intermediate result later fronts pick up. I therefore recommend the corrected pair

```
φ_runstart = ∫₀¹ P (1−t)^(2P−1) e^(−c H(t)) dt          (one extra forced event at s=0)
E[#f-draws] = (1 + c·T)/(1−ρ)                            (the opening chain at x₀)
eps        = (ρ_start/ρ)·φ_runstart + (1 + c·T)/((1−ρ)·n)
φ_EPSR     = (1−ρ)·φ_V4 + ρ·eps
```

be recorded alongside, or in place of, §5.2's forms. `φ_EPSR` is numerically ≥ `φ_EPS`
on every grid tested (χ²: 49.58 vs 50.03; 46.52 vs 46.61; 43.58 vs 44.17; 71.40 vs
72.04; 183.6 vs 185.2) and each of its two ingredients is *measured* — not fitted —
to 0.1–2.8 % across 32 cells spanning `b ∈ [1,400]`, `c ∈ [5,600]`, `n ∈ [16384,131072]`,
`ρ ∈ [0.0006, 0.71]`.

Governance note, offered rather than decided: `φ_EPSR` is itself a positive claim,
originating with the referee. Its ingredients were measured rather than fitted and the
measurements *are* the adversarial check, so in my judgement the discipline is already
satisfied; but if the orchestrating session prefers, catalogue `φ_EPS` now with an
explicit "derivation corrected in `adversarial/REFEREE_REPORT.md` §4" annotation and
queue `φ_EPSR` as its own front.

**(C) Record that the `eps` channel is EXHAUSTED.**
Substituting the exactly measured `eps` for the modelled one moves χ² from 185.2 to
183.2 out of 335.6 → an irreducible 183. **No further work on `eps` can close
anything.** The whole remaining residual lives in `φ(cyclic | x₀ ∉ R)`, which I measure
to deviate from `φ_V4` by −0.34 % … +3.09 % in a pattern that reproduces the residual
in full — an independent confirmation of §5.3's localisation, obtained without any HT
estimator or `λ` fit. That is where the next front belongs.

**(D) Do NOT change anything about the U_{1/2} classification.**
Nothing in this review touches it. `φ_EPS`/`φ_EPSR` differ from `φ_CAND` only at
`O(c/n)`, i.e. they vanish in the `n → ∞` limit at fixed `(b, c)`; the entire claim is
a finite-n correction, exactly as the lineage frames it.

**(E) A process note for the lineage.**
The one wrong cell-level statement in §5.1 (`b=400/c=100`, "−3.3σ") comes from a
single realisation with 157 events and no replication — in the same document whose
primary result was saved by exactly the replication discipline it applied there
(§4.3). The asymmetry is worth recording: the front replicated its *mandated*
hypothesis and did not replicate its *secondary* measurement. A cheap rule would be to
require the same replication standard for any cell-level claim that is used to
diagnose a formula, not just for the mandated one.
