# DERIVATION_PREREG — written BEFORE any simulation of this front

Purpose: fix, in writing and with a verifiable timestamp, the derivation and
the resulting candidate formula **before** running a single new simulation, so
that the discipline of DISC-DEC-045 ("no curve-fitting; every candidate must be
*derived* from the mechanism") is auditable rather than merely asserted.

Nothing below was obtained by fitting anything to `φ_mc`. The only numbers I had
seen when writing this were the ones printed in the predecessor documents I was
mandated to read.

---

## 1. The mechanism, restated (no redefinition)

`π` uniform permutation of `[n]`; seeds i.i.d. `Bernoulli(c/n)`, independent of
`π`; block of a seed `s` is `{s, π(s), …, π^{b−1}(s)}`; `R` = union of blocks;
for `x ∈ R`, `f(x)` is an i.i.d. uniform draw on `[n]`; for `x ∉ R`, `f(x)=π(x)`.
`ρ = 1 − (1−c/n)^b`, `ρ_start = (c/n)(1−c/n)^b = (c/n)(1−ρ)` (exact, wave 4).

Terminology (wave 4): `p ∈ R` is a **run start** iff `π^{−1}(p) ∉ R`; a **run**
is a maximal `π`-consecutive stretch of `R`; the last element of a run is a
**run end**.

## 2. The exposure that makes `R` known before the walk starts

Generate in this order:

1. Reveal the **seed set** `Σ` (i.i.d. marks, independent of `π`).
2. For every seed `s`, reveal `π(s), π²(s), …, π^{b−1}(s)` (b−1 forward
   `π`-queries; follow already-revealed values when the blocks overlap). After
   this step **`R` is completely determined** as a subset of `[n]`.
3. What remains of `π` is a **uniform bijection** between
   ```
   A_rem = [n] \ A ,  A = { π^j(s) : s ∈ Σ, 0 ≤ j ≤ b−2 }   (revealed arguments)
   U_rem = [n] \ I ,  I = { π^j(s) : s ∈ Σ, 1 ≤ j ≤ b−1 }   (revealed images)
   ```
   (standard sequential-exposure / Fisher–Yates fact, the same tool
   `aggregation_closure_attempt/ATTEMPT.md` §3.1 uses).

Two densities follow immediately, exactly:

```
P(y ∈ U_rem) = P(no seed among π^{−1}(y),…,π^{−(b−1)}(y)) = (1−c/n)^{b−1}
             = (1−ρ)/(1−c/n)                                          (2.1)
P(y ∈ R ∩ U_rem) = (c/n)(1−c/n)^{b−1}                                 (2.2)
```

`R \ I` is the set of seeds not covered by another seed's block; it contains the
run starts and differs from them only by `O((c/n)²)` per point.

**Consequence 1 (recovers the wave-8 lemma).** The walk only ever takes a
`π`-step from a point `x ∉ R` (a point of `R` reroutes instead), and `x ∉ R ⟹
x ∈ A_rem`. Therefore, at the very first step, `π(x)` is **uniform on `U_rem`**,
so the per-target density is
```
1/|U_rem| = (1−c/n)^{−(b−1)}/n = P_exact/n .
```
That is *exactly* the elevation `P_exact = (1−c/n)^{−(b−1)}` that
`aggregation_closure_attempt/ATTEMPT.md` §3 derived by a different route and
validated at production scale (their §4.3, χ²=1.93/4). So this exposure
reproduces the one piece of the lineage that is already independently
established — a necessary sanity condition before using it for anything new.

## 3. The piece every predecessor missed: the pool keeps shrinking inside `U_rem`

`φ_V4` / `φ_CAND` / `φ_CAND5` / `φ_GLOBAL` all posit a **constant** elevation `P`
multiplying the inherited hazard `1/(1−t)`:
```
per-target closure hazard  =  P / ((1−t) n)   per step .
```
The `(1−t)n` is the master formula's pool of "points not yet consumed as a
`π`-image", inherited from M-U (`global_exclusion_attempt/ATTEMPT.md` §1
re-established this reading).

But in M-CLUST(b) the pool the walk actually draws from is `U_rem`, **not**
`[n]`, and the walk consumes from `U_rem`:

* every normal `π`-step is taken from a visited point of `R^c` and consumes one
  value of `U_rem` (namely its image);
* the number of normal steps taken up to the moment the walk has visited a
  fraction `t` of `[n]` is the number of visited `R^c` points, `t_c·n`, and
  `t_c = t − O(c t/n)` (the visited points of `R` are the run starts hit,
  `≈ c t`, plus the chain points, `≈ c t ρ/(1−ρ)`).

Hence, at traversed mass `t`,
```
|U_rem(t)| = n·(1−ρ)/(1−c/n) − t_c·n ,
per-target closure hazard = 1/|U_rem(t)| per step,
```
i.e., **relative to the master formula's `1/((1−t)n)`,**
```
        λ(t) = (1−t) / ( (1−ρ)/(1−c/n) − t )   ≈   (1−t)/(1−ρ−t)          (3.1)
```
`λ(0) = P_exact` (matches §2), and **`λ(t)` grows with `t`**. THIS is the
candidate explanation of the measured excess of the elevation over
`P_lead = 1/(1−ρ)`: the elevation is not a constant, and every constant-`P`
formula in this lineage is evaluating it at `t = 0`.

Predicted shape, pre-registered: `λ(t)/P_lead ≈ (1−t)(1−ρ)/(1−ρ−t)`, an
increasing function of `t` equal to `1` at `t=0`, whose growth rate is set by
`1/(1−ρ)` — so it grows with `ρ`, and (at fixed `ρ`) with the traversed mass at
which the walk typically ends, which itself grows as `c` falls, i.e. **with `b`
at fixed `ρ`**. Both dependences reported by the two predecessor measurements.

## 4. The exact reduction: M-CLUST(b) conditioned on `x₀ ∉ R` **is** M-U

The subtractive hazard (3.1) is not an isolated patch. Once `R` is exposed, the
whole conditioned process collapses:

**Claim.** Conditionally on `x₀ ∉ R`, the exploration of the `f`-orbit of `x₀`
in M-CLUST(b) with parameters `(c, n)` is, in the continuum description this
lineage uses, *identical* to the exploration in **M-U** with
```
        n' = (1−ρ) n ,        c' = c(1−ρ) ,        c'/n' = c/n .            (4.1)
```

Ingredients, each checked against the pieces already established in the lineage:

* **World.** The walk lives on `R^c` (mass `(1−ρ)n`); it enters `R` only at run
  starts, and leaves immediately by an `f`-draw (wave 4 shadowing lemma).
* **Closure hazard.** §3: per target, `1/|U_rem(t)|`. Writing the collapsed mass
  `u = t_c/(1−ρ)`, this is `1/((1−u)·(1−ρ)n·(1+c/n)^{-1}) `, i.e. exactly M-U's
  `1/((1−u) n')` up to the same `(1−c/n)` factor M-U itself carries.
* **Reroute rate.** Per normal step, `P(π(x) ∈ R ∩ U_rem)` = (2.2)/(2.1) = `c/n`,
  constant. In collapsed mass units (`du = 1/n'`) that is a rate
  `c/n · n' = c(1−ρ) = c'` per unit mass — constant, exactly as in M-U, where the
  rate is `c'/n' · n' = c'`. (This is the wave-4 "encounter rate = c per unit
  mass" statement, re-expressed in collapsed units.)
* **Kill probability.** An `f`-draw is uniform on `[n]`: it kills on visited mass
  `t`, re-draws on fresh `R` (mass `≈ρ`), survives on fresh `R^c`. So a *chain*
  kills with probability `t/(1−ρ) = u` — i.e. `q(u) = u`, which is **M-U's own
  kill law** (`DERIVATIONS.md` §3.1), not the elevated `q_CLUST(s)=s/(1−ρ)`
  written in `t`-units. The two statements are the same statement in different
  coordinates; wave 4's `q_CLUST` is confirmed, not contradicted.
* **Surviving reroute ⇒ exactly one new arc start.** Same in both.
* **Structurally-unclosable targets.** A fresh arc start `D ∉ R` fails to be in
  `U_rem` with probability `c/n` (it is the successor of a run end). In M-U the
  same holds with probability `c'/n' = c/n`. The defect is *equal*, so it does
  not break the match.

Therefore, in the continuum limit,
```
φ(cyclic | x₀ ∉ R)  =  φ_U(c(1−ρ))  =  ∫₀¹ e^{−c(1−ρ) u²} du .            (4.2)
```

Two remarks I record now, before seeing any datum:

* (4.2) is exactly `φ_OLD`, the wave-3 formula of `DERIVATIONS.md` §3.5
  (`φ_U(c(1−c/n)^b)`), which `residual_attempt/ATTEMPT.md` §2.2 re-derived as
  `φ_v3` and **discarded** — but discarded *before* §6 of the same document
  discovered the `x₀ ∈ R` dilution factor, and it was never re-tested with it.
  The claim here is that `φ_OLD` was always the right **conditional** answer and
  was only ever compared against the **unconditional** `φ`.
* The reduction is a statement about the conditioned process, so it can be
  tested **without the master formula at all**: simulate M-U at `(c', n')` and
  compare to the measured `φ(cyclic | x₀ ∉ R)` of M-CLUST(b) at `(c, n)`.

## 5. Candidate formula (`φ_RED`), fixed here, no free parameter

Reusing the exact total-probability decomposition and the referee's corrected
`eps` channels (`adversarial/REFEREE_REPORT.md` §4.1), re-expressed through the
reduction (4.1) — i.e. with `P → 1`, `c → c'`, `H(t) → u²`:

```
φ_U(c') = ∫₀¹ e^{−c' u²} du
T(c')   = ∫₀¹ (1−u) e^{−c' u²} du                      (= φ_runstart under (4.1))
eps_RED = (ρ_start/ρ)·T(c')  +  (1 + c'·T(c')) / ((1−ρ)·n)
φ_RED   = (1−ρ)·φ_U(c')  +  ρ·eps_RED
        = (1−ρ)[ φ_U(c') + (c/n)·T(c') ]  +  ρ(1 + c'T(c'))/((1−ρ)n)      (5.1)
```

Checks that must hold (to be verified in code, not asserted):
`ρ → 0 ⇒ φ_RED → φ_U(c)`; `φ_RED → (1−ρ)φ_U(c(1−ρ))` as `c/n → 0`;
`b = 1 ⇒ φ_RED` reduces to the M-U expression up to `O(c/n)`.

## 6. Pre-registered tests and decision criteria

| # | test | what would REFUTE the derivation |
|---|---|---|
| T1 | direct measurement of the per-target elevation `λ(t)` in mass bins, HT estimator, own walk simulator | `λ(t)` flat in `t`, or growing at a rate incompatible with (3.1) |
| T2 | direct measurement of the pool `|U_rem(t)|` along the walk | `|U_rem(t)|/n ≠ (1−ρ)/(1−c/n) − t_c` beyond `O(c/n)` |
| T3 | **reduction test**: measured `φ(cyclic\|x₀∉R)` for M-CLUST(b,c,n) vs measured `φ(cyclic)` for M-U(c(1−ρ), (1−ρ)n) — no formula involved on either side | a systematic discrepancy growing with `b` or `ρ` |
| T4 | fresh 18-cell grid: `φ_RED` vs `φ_EPSR` vs `φ_CAND` | `φ_RED` not better, or its residual still grows with `b`/`ρ` |

If T1–T3 pass and T4 shows the residual no longer grows with `b`/`ρ`, the claim
is: *the elevation excess is fully explained, and it is not a new constant but a
`t`-dependence that the constant-`P` ansatz cannot represent.* Any leftover
residual is then `O(c/n)`, of the same order as the pieces deliberately dropped
in §4 (visited `R` mass in the kill law, chain points inside `t`), and must be
reported as such rather than closed.

Written before any simulation of this front.
