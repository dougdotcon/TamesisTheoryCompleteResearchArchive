# DERIVATION_PREREG — mechanistic identification of the long-cycle deficit

**Wave 13, `DISC-DEC-054`, front (b) `LONG-CYCLE-DEFICIT-ATTEMPT`.**
Written and saved BEFORE any real (non-throwaway) simulation of this front is
run — check file mtimes against the `.log` files in this directory. Target:
`short_cycle_dynamics_attempt/ATTEMPT.md` §9 open item 1 — the persistent
~−10% to −15% deficit of the long-`L` (`L>b`) M-CLUST(b) cycle population
relative to `φ_U(c'')`, independently confirmed by
`short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md` §4.1 (far-tail
`(20b,∞)` bin, three cells: target `−6.4%` to `−9.7%`; `b=400,c=100`
`−10.6%` to `−14.7%`; `b=200,c=150`: `−10.7%` to `−12.5%`, all `|z|≥5.5`).

---

## 0. Question and the two live hypotheses (from the mandate, unchanged)

- **H1 (M-CLUST(b)-specific bias).** The deficit comes from a bias in the
  mean-field/Poissonization approximation underlying `φ_q(c)` (`DERIVATIONS.md`
  §1, `H_q(t) = t − (1−t)∫₀ᵗ(1−q(s))/(1−s)ds`) that is *specifically amplified*
  by M-CLUST(b)'s correlated block structure — points within a block of size
  `b` share correlated exposure, unlike the i.i.d.-per-point structure the
  master formula's derivation assumes.
- **H2 (generic finite-n artifact).** The deficit is a generic finite-size
  effect that would appear comparably in other M-q mechanisms (plain M-U,
  i.e. `b=1`; or a `b`-sweep within M-CLUST itself) at matched `(c,n)`, i.e.
  it is not specific to block correlation at all.

## 1. A candidate mechanism, derived (not yet tested) before choosing the tests

**Observation used to design the tests (not itself claimed as an established
result — it motivates T1–T3 but the tests below are what actually decides
anything).** Consider `x₀ ∈ R^c` on a π-cycle of length `L`. A basic
structural fact of any of these mechanisms (M-U, M-CLUST(b), …): the set of
points that can **ever** reach `x₀` by a *pure forward π-step* is exactly the
`L` points of `x₀`'s own π-cycle (a permutation's cycle is forward-closed).
`x₀` becomes cyclic only if some arc, walking forward, eventually lands
exactly on `x₀` — either the original π-walk from `x₀` closing directly
(handled exactly by the short-cycle-untouched mechanism the prior front
isolated), or a *rerouted* arc that has re-entered `x₀`'s own cycle at some
point and then walks forward (along π, since outside `R` the rule reverts to
π) into `x₀`.

A **uniform reroute destination lands on `x₀`'s own cycle with probability
exactly `L/n`** — not a fixed, `L`-independent rate. For `L` a sizeable
fraction of `n` (as is typical: `L` is exactly uniform on `{1,…,n}`, so
`E[L]≈n/2`, and the point-weighted average — which is what the `R^c`
population is dominated by — skews toward large `L`), this is not a
negligible correction to the mean-field bookkeeping, which implicitly treats
"landing on fresh mass" as governed only by the *aggregate* fraction of `[n]`
already visited, not by any correlation between the reroute destination and
`x₀`'s own π-cycle identity. **This effect, if real, has nothing to do with
`b` or block correlation** — it is a property of conditioning on `L` at all,
present identically in plain M-U (`b=1`, D_i=Uniform([n])). This is the
concrete candidate mechanism motivating H2 that this front will test for,
alongside the direct H1-vs-H2 discriminator the mandate proposes. It is
stated here, before any simulation, as the reason T3 (§3) is included, and it
predicts (not yet checked) that the deficit should correlate with `L/n`
specifically, and should be present, in similar rough magnitude, in plain
M-U's own `L`-conditioned population.

---

## 2. Engine reuse (established infrastructure, not re-derived)

`sc_engine.py` (parent directory) is reused unmodified, exactly as its own
selftest validates (`sc_engine_selftest.log`, all 5 groups OK). Key fact used
here: **`build_R_mask(n, b=1, pi, seed_mask)` reduces to `R = seed_mask`
exactly** — the loop `for _ in range(1, b)` never executes when `b=1`, so no
shadowing, no blocks, no chains: this *is* plain M-U (D_i = i.i.d.
Uniform([n]) applied only to the seed itself), matching `DERIVATIONS.md`
§3.1/§3.5's own statement that M-CLUST(1) ≡ M-U mechanically. `sc_formula.py`
is reused unmodified: `c_double_prime(b,c,n) = c·(1−c/n)^(b−1)`, so **at
`b=1`, `c''=c` exactly** — the natural comparison target for the `b=1` run is
therefore `φ_U(c)` itself, falling out of the existing formula as a special
case, no new formula needed. This reuse is checked deterministically before
trusting it (T0 below), not simply assumed.

No `.py` file under `elevation_level_attempt/` or its `adversarial/` is read
or imported (same independence rule as the parent front, extended by
inheritance since this front reuses the *parent's own* `sc_*.py`, which
already satisfies it).

---

## 3. Planned tests, IN ORDER, with criteria fixed now

**T0 — engine sanity for `b=1` (deterministic, cheap, must pass first).**
Build a handful of `b=1` instances and check `R_mask == seed_mask` exactly
(0 violations) and `ρ_measured ≈ c/n` (the `b=1` special case of
`1−(1−c/n)^b`). **Refutation: any violation stops this front to fix the
engine assumption before proceeding.**

**T1 — PRIMARY: matched-`(c,n)` comparison, plain M-U (`b=1`) vs the
original M-CLUST(b) cells, same absolute L-bin edges.** Three cells, `n=65536`
throughout, matching `short_cycle_dynamics_attempt`'s T1 cells exactly in
`(c,n)`:

| cell | c | original b | original far-tail edge (`20b`) |
|---|---|---|---|
| A (target) | 1000 | 100 | 2000 |
| B | 100 | 400 | 8000 |
| C | 150 | 200 | 4000 |

At `b=1`, run the identical diagnostic-split measurement (`sc_engine`'s
`build_instance`/`cyclic_mask_peeling`/`pi_cycle_lengths`, no formula on the
measurement side) using the **same absolute bin edges** as the original cell
(e.g. cell A: `(100,200],(200,500],(500,2000],(2000,∞)` — note these edges
are NOT "20×b" for `b=1`; they are simply the fixed numeric edges the parent
front already used at that `(c,n)`, reused so the comparison is apples to
apples on identical `L` windows). Compare the far-tail bin
`φ(cyclic|x₀∈R^c, L>edge)` against `φ_U(c)` (`=φ_U(c'')` at `b=1`), with
`z`-score and `dev%`, exactly as the parent front's methodology.
`N=2500` per cell (matching the parent front's own T1 `N`).

**Discriminating rule, fixed now:** for each cell, classify the `b=1`
far-tail result as:
- **PRESENT (comparable)** if `z ≤ −3` AND `dev% ≤ −3` (statistically and
  practically a negative deviation of the same sign, at least a few percent).
- **ABSENT/NEGLIGIBLE** if `|z| < 2` or `dev% ≥ 0`.
- **PRESENT BUT SMALLER** if `z≤−3` but `|dev%|` is less than 1/3 of the
  corresponding original-cell far-tail `|dev%|` (using the
  `short_cycle_dynamics_attempt/ATTEMPT.md` §3.1 reported figure as the
  reference: cell A `−9.66%`, cell B `−14.7%`, cell C `−10.7%`).
  **[Correção pós-adversarial, 2026-08-23 — referee de
  `long_cycle_deficit_attempt`: a cifra da célula A, `−9,66%`, está
  mal-atribuída — rastreada à célula errada (`b=400,c=100`) e à
  grandeza errada (comparação `φ_REDC_full` do referee-pai §3.2). A
  cifra correta da linha `(20b,∞)` de `short_cycle_dynamics_attempt/
  ATTEMPT.md` §3.1 para `(100,1000)` é `−9,7%`. Coincidentemente
  próxima, sem efeito sobre nenhuma classificação. Ver
  `adversarial/REFEREE_REPORT.md` §4/§7 e as correções correspondentes
  em `ATTEMPT.md`.]**

If **≥2 of 3** cells classify PRESENT (comparable) → favors **H2**. If **≥2
of 3** classify ABSENT/NEGLIGIBLE or PRESENT BUT SMALLER → favors **H1**.
Otherwise: mixed, reported as such (an acceptable, honest outcome — the
mandate does not require a clean split).

**T2 — SECONDARY: b-sweep dose-response at fixed `(c,n)`.** Fixed cell
`c=1000, n=65536` (the target cell). Sweep `b ∈ {1, 5, 20, 50, 100}` (100 =
the cell's original block size). For each `b`, measure **only** the far-tail
bucket `φ(cyclic | x₀∈R^c, L>2000)` (the same absolute threshold at every
`b`, so the comparison isolates the effect of `b` alone, holding `(c,n)` and
the `L`-window fixed) against `φ_U(c'')` (`c''` depends on `b` via
`c_double_prime`). `N=2000` per `b` value.

**Discriminating rule, fixed now:** compute `|dev%|` at each `b`. If the
ratio `max(|dev%|)/min(|dev%|)` across the 5 points is **< 2×** and there is
no monotonically increasing trend from `b=1` to `b=100` (informal check: the
`b=100` value is not the strict maximum with the sequence otherwise
increasing) → favors **H2** (deficit magnitude ~`b`-independent). If
`|dev%|` at `b=100` is **≥3×** the `b=1` value AND the sequence is
monotonically non-decreasing in `b` (allowing one exception for MC noise) →
favors **H1** (deficit scales with block-correlation strength). Otherwise:
mixed, reported as such.

**T3 — EXPLORATORY/mechanistic (not required for the H1-vs-H2 verdict):**
`L/n`-fraction sub-binning of the far tail at the *original* target cell
(`b=100,c=1000,n=65536`) — split the `(2000,∞)` bin further into
`(2000, n/8], (n/8, n/4], (n/4, n/2], (n/2, n]` and measure `φ(cyclic|x₀∈R^c,
L∈sub-bin)` vs `φ_U(c'')` in each. Tests the §1 candidate mechanism directly:
if `|dev%|` grows with `L/n`, that is evidence for the destination-landing-
on-own-cycle explanation specifically (a generic, `b`-independent mechanism,
supporting H2 by a specific causal story); if `|dev%|` is flat across `L/n`
already by `L=2000` (`L/n≈3%`), the growing-with-`L/n` story is not
supported and the plateau's flatness needs a different explanation. `N=3000`.
Reported honestly regardless of outcome; not a formula candidate.

**No functional form or new bin edges are chosen after seeing T1/T2/T3
data.** If none of T1/T2/T3 cleanly discriminates, that is reported as
honest non-closure — a fully acceptable outcome per the mandate.

---

## 4. Seeds (fresh, reserved range `20260827000+` per `DISC-DEC-054`;
confirmed unused elsewhere by `grep -rn "20260827" ..` over the whole
archive before assignment — only the ledger's own reservation line and an
unrelated numeric substring inside an SDSS data CSV matched, neither a used
`SeedSequence`)

| seed | use |
|---|---|
| `SeedSequence(20260827000)` | T0, `b=1` engine sanity (R=seed_mask, ρ≈c/n) |
| `SeedSequence(20260827001)` | T1 cell A (target, `c=1000,n=65536,b=1`), N=2500 |
| `SeedSequence(20260827002)` | T1 cell B (`c=100,n=65536,b=1`), N=2500 |
| `SeedSequence(20260827003)` | T1 cell C (`c=150,n=65536,b=1`), N=2500 |
| `SeedSequence(20260827010)` | T2 b-sweep, `b=1`, N=2000 |
| `SeedSequence(20260827011)` | T2 b-sweep, `b=5`, N=2000 |
| `SeedSequence(20260827012)` | T2 b-sweep, `b=20`, N=2000 |
| `SeedSequence(20260827013)` | T2 b-sweep, `b=50`, N=2000 |
| `SeedSequence(20260827014)` | T2 b-sweep, `b=100`, N=2000 |
| `SeedSequence(20260827020)` | T3, target cell `b=100` sub-binning, N=3000 |
| `SeedSequence(20260827900+)` | any throwaway/exploratory smoke run, discarded, not counted in any reported number |

---

## 5. Files planned

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | this document |
| `lcd_diagnostic.py` | T0, T1, T3 — generalized diagnostic split with caller-supplied absolute bin edges (imports `sc_engine`, `sc_formula` from the parent directory; no new engine written) |
| `lcd_bsweep.py` | T2 — b-sweep, far-tail-only measurement |
| `lcd_t0.log`, `lcd_t1_cellA.log`, `lcd_t1_cellB.log`, `lcd_t1_cellC.log`, `lcd_t2_bsweep.log`, `lcd_t3_target_subbin.log` | run outputs |
| `ATTEMPT.md` | the write-up |

No git commit. Nothing outside this subfolder is touched. This front reuses
`short_cycle_dynamics_attempt/sc_engine.py` and `sc_formula.py` by import
(read-only), per the mandate's explicit permission ("You MAY reuse it
freely; this is normal research continuity").
