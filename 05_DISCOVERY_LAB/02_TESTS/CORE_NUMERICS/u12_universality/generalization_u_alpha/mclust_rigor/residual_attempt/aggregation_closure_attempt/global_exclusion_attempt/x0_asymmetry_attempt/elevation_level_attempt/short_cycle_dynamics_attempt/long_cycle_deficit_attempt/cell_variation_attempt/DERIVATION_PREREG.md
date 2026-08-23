# DERIVATION_PREREG — what drives the cell-to-cell H2-share variation?

**Wave 14, `DISC-DEC-057`, front (e) `CELL-VARIATION-ATTEMPT`.**
Written and saved BEFORE any real (non-throwaway) simulation of this front
runs — check this file's mtime against every `.log` file in this directory,
all later. Throwaway timing/correctness smoke tests used seeds
`999900010`/`999900011` (outside the reserved range, discarded, not counted
in any reported number, matching this archive's disclosed-throwaway-seed
convention) purely to size `N` and validate the multiprocessing
parallelization is bit-identical to single-process before locking this design.

Target: `long_cycle_deficit_attempt/ATTEMPT.md` §5, verbatim —

> The cell-to-cell variation in how much of the total deficit is already
> present at `b=1` (`~26–38%` at the target cell vs `~77–80%` at cells B/C)
> is itself an unexplained, honestly-reported open pattern — it did not
> correlate simply with `b` alone, since the three original cells differ in
> both `c` and `b` simultaneously, and no further covariate (e.g. the final
> excluded fraction `ρ` ... ) was tested here; chasing it would require a
> new pre-registration, not a post-hoc fit, so it is left open rather than
> speculated on.

This document is that new pre-registration.

---

## 0. The confound in the original three cells

Original cells (`short_cycle_dynamics_attempt/ATTEMPT.md`), all `n=65536`,
with `ρ = 1-(1-c/n)^b` (`sc_formula.rho_of`, re-verified here by direct
computation, not copied):

| cell | b | c | ρ | H2 share (from `long_cycle_deficit_attempt`) |
|---|---|---|---|---|
| A (target) | 100 | 1000 | 0.7851 | 26–39% (depending which end of the confirmed range is used as reference, per the referee's correction) |
| B | 400 | 100 | 0.4571 | 76.9% (`11.30/14.7`) |
| C | 200 | 150 | 0.3676 | 80.4% (`8.60/10.7`) |

`b`, `c`, and `ρ` all move together across A→B→C (`b`: 100→400→200 — not
even monotonic; `c`: 1000→100→150; `ρ`: 0.79→0.46→0.37 — monotonic and
tracks the H2-share drop most cleanly of the three, but with only 3 points
and all covariates confounded, this is not evidence, only a hint motivating
the design below). **No prior test held any one of `{ρ,b,c}` fixed while
varying the other two.** This front does that, twice, at two different `ρ`
levels, plus two more sweeps that hold `c` or `b` fixed while `ρ` is allowed
to move freely — four independent sub-comparisons in total.

---

## 1. Engine and formula reuse (established, not re-derived)

`sc_engine.py` and `sc_formula.py` (`short_cycle_dynamics_attempt/`, two
directories up) are imported unmodified — already adversarially verified
SOUND by two independent referees at this point in the lineage
(`short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md`,
`long_cycle_deficit_attempt/adversarial/REFEREE_REPORT.md`). No other `.py`
anywhere in the archive is read or imported by this front's own code.

Key identity reused, re-verified algebraically and by the parent lineage's
own `T0` (not re-derived here): `c''(b=1,c,n) = c·(1-c/n)^0 = c` exactly, so
`φ_U(c'')` at `b=1` **is** `φ_U(c)` — no special-casing needed in the
measurement code; calling `sc_formula.c_double_prime(1,c,n)` and
`sc_formula.phi_U` on the result reduces to `φ_U(c)` automatically.

**`n=65536` is held fixed at every cell in this design.** The mandate names
`ρ`, `c`, `b` as the covariates to disentangle; `n` is deliberately not
varied here (a fourth covariate is out of scope for a design already sized
at 13 cells × 2 conditions). This is a stated limitation, not an oversight.

---

## 2. Methodology — reusing BOTH parent T1 definitions exactly

For a cell defined by `(b,c)` at `n=65536`, with `threshold := 20·b` (the
**original** cell's own far-tail edge, matching
`short_cycle_dynamics_attempt`'s own bin convention exactly):

- **"own-`b` deficit"** = `φ(cyclic | x₀∈R^c, L>threshold)` measured at the
  cell's own `b`, compared against `φ_U(c''(b,c,n))` — this is
  `short_cycle_dynamics_attempt`'s T1 far-tail methodology, reused exactly
  (same absolute-threshold-vs-`φ_U(c'')` comparison, same `R^c`/`L`
  definitions from `sc_engine.py`).
- **"`b=1` deficit"** = the identical measurement (**same absolute
  `threshold`**, same `c`, same `n`) but with the mechanism run at `b=1`,
  compared against `φ_U(c''(1,c,n)) = φ_U(c)` — this is
  `long_cycle_deficit_attempt`'s T1 methodology, reused exactly (matched-
  `(c,n)`, same-bin-edge comparison of `b=1` against the cell's own original
  edge).

Both conditions per cell use **one shared measurement function**
(`cv_measure.measure_far_tail(n,b,c,N,seed,threshold)`), called once with
`b=b_orig` and once with `b=1`, with everything else held fixed — this
guarantees the two figures being ratio'd are computed by literally the same
code path, differing only in the `b` argument, eliminating any
methodology-mismatch risk between the two conditions.

For each cell: `dev_orig% = 100·(φ_far,orig/φ_U(c''_orig) − 1)`,
`z_orig = (φ_far,orig − φ_U(c''_orig))/SEM_orig`, and symmetrically
`dev_b1%`, `z_b1`. **H2 share := dev_b1% / dev_orig%** (signed ratio of the
raw deviations, matching exactly how `long_cycle_deficit_attempt/ATTEMPT.md`
§3–5 computed its own three H2-share figures, e.g. `2.52/9.7`, `11.30/14.7`,
`8.60/10.7` — same definition, not a new one invented post-hoc).

**Exclusion rule, fixed now:** a cell's H2 share is reported as **undefined**
and excluded from the cross-cell correlation/regression (though its raw
numbers are still reported in the full table) if `dev_orig% ≥ 0` or
`|z_orig| < 2` — i.e. if the own-`b` deficit itself is not established at
that cell, "what fraction of it survives at `b=1`" is not a meaningful
question.

**SEM on H2 share (delta method, independent samples):** since `dev_orig`
and `dev_b1` come from disjoint RNG seeds (independent measurements),
`Var(H2share) ≈ H2share² · [(SEM_devb1/dev_b1)² + (SEM_devorig/dev_orig)²]`,
with `SEM_dev% = 100·SEM_φ/φ_U`. Used only to gauge whether cross-cell H2-share
differences within a "held-fixed" sub-group exceed measurement noise — not
used to change any classification rule below.

---

## 3. The 13-cell design (locked now)

All cells `n=65536`. `ρ`, `c''`, `φ_U(c'')` computed by direct call to
`sc_formula` (deterministic, no RNG) and reported to 4 decimals in the
results table for audit.

| id | b | c | ρ (formula) | threshold=20b | group(s) |
|---|---|---|---|---|---|
| A | 100 | 1000 | 0.7851 | 2000 | G1, G2, G3 (hub) |
| G1a | 25 | 1000 | 0.3191 | 500 | G1 |
| G1b | 50 | 1000 | 0.5364 | 1000 | G1 |
| G1d | 200 | 1000 | 0.9538 | 4000 | G1 |
| G2a | 100 | 200 | 0.2633 | 2000 | G2 |
| G2b | 100 | 500 | 0.5351 | 2000 | G2 |
| G2d | 100 | 2000 | 0.9549 | 2000 | G2 |
| G3a | 335 | 300 | 0.7850 | 6700 | G3 |
| G3c | 50 | 2000 | 0.7877 | 1000 | G3 |
| G3d | 1007 | 100 | 0.7851 | 20140 | G3 |
| B | 400 | 100 | 0.4571 | 8000 | G4 (hub) |
| G4b | 80 | 500 | 0.4581 | 1600 | G4 |
| G4c | 26 | 1500 | 0.4523 | 520 | G4 |

**Sub-comparisons (the design's actual discriminating power — four of
them, satisfying the mandate's "at least two" requirement twice over):**

- **G1** — `c=1000` fixed; `b∈{25,50,100,200}` varies (8×); `ρ` co-varies
  freely with `b` (0.32→0.95). Isolates `b`(+`ρ`) from `c`.
- **G2** — `b=100` fixed; `c∈{200,500,1000,2000}` varies (10×); `ρ`
  co-varies freely with `c` (0.26→0.95). Isolates `c`(+`ρ`) from `b`.
- **G3** — `ρ≈0.785–0.788` held fixed (matching cell A's own `ρ`); `b`
  varies 50→1007 (20×) and `c` varies 100→2000 (20×) **jointly**, chosen so
  `ρ` stays put. If H2 share is flat here despite `b,c` moving 20× each,
  that is direct evidence `ρ` (not `b` or `c` individually) is what matters.
- **G4** — `ρ≈0.452–0.458` held fixed (matching cell B's own `ρ`, at a
  *different* level than G3, for robustness against G3 being a fluke); `b`
  varies 26→400 (15×), `c` varies 100→1500 (15×) jointly. Note: `B` itself
  (`b=400,c=100`) is this front's own fresh re-measurement of the original
  parent-front cell B, at a different absolute threshold origin (`8000`,
  matching `B`'s own `20b`) — serves as an internal replication check
  against the two prior fronts' own cell-B figures.

`A` and `B` are each counted once in the overall 13-cell pool despite
belonging to multiple groups (same measurement, not re-drawn per group).

---

## 4. Statistics — fixed now, before any real data

1. **Per-cell table**: `ρ, c'', φ_U(c''), φ_far, SEM, dev%, z` for both the
   own-`b` and `b=1` conditions, plus `H2share` and its delta-method SEM,
   for all 13 cells.
2. **Pooled correlation** (secondary, cruder summary): among cells with a
   defined H2 share (§2 exclusion rule), Pearson `r` between `H2share` and
   each of `ρ`, `log10(c)`, `log10(b)` separately (log-transformed `c,b`
   because both span roughly an order of magnitude or more across the
   design; `ρ∈[0,1]` is used untransformed). Report `r`, `t=r√(n-2)/√(1-r²)`,
   `df=n-2`, two-sided `p` (via `scipy.stats.t.sf`). Also one multiple OLS
   regression `H2share ~ 1 + ρ + log10(c) + log10(b)` (via
   `numpy.linalg.lstsq`), reporting each coefficient, its standard error
   (from the residual covariance matrix), `t`, `p` (`df=n-4`).
3. **Sub-group range test (PRIMARY discriminator, fixed now):** for each of
   G1, G2, G3, G4, compute `range_i = max(H2share) − min(H2share)` within
   that group (percentage points). Classify each group as:
   - **flat** if `range_i ≤ 15pp`
   - **varies substantially** if `range_i ≥ 30pp`
   - **ambiguous** if `15pp < range_i < 30pp`

   **Decision rule:**
   - If **both** `ρ`-fixed groups (G3, G4) are *flat* **and** at least one of
     the `ρ`-varying groups (G1, G2) *varies substantially* → **ρ is the
     driver** (H2 share tracks `ρ` regardless of the specific `(b,c)` pair).
   - Symmetrically: if G1 (the `b`-varying, `c`-fixed group) is *flat* while
     both `ρ`-fixed groups vary substantially → **`b` is not a driver once
     `c` is controlled, but something else is** (inconclusive on `ρ` unless
     G2/G3/G4 pattern also points the same way) — reported as such, not
     forced.
   - If **no** group is flat (all four `range_i ≥ 15pp`, most `≥30pp`) →
     **honest negative result**: none of `ρ,c,b` alone (holding the other
     roughly fixed) explains the H2-share variation — reported as a
     rigorous non-closure, exactly as acceptable per the mandate.
   - Any other pattern (e.g. only one of G3/G4 flat, or a group lands
     squarely in the 15–30pp "ambiguous" band) is reported as **partial/
     mixed**, with the pooled regression (§4.2) offered as secondary,
     non-decisive context — no forcing of a clean verdict.
4. **No functional form, no new bin edges, and no cell is added or dropped**
   after seeing any T1-style measurement from this front. The 13-cell table
   and the classification thresholds (15pp/30pp) are locked as of this
   document's timestamp.

---

## 5. Implementation and sample size

`cv_measure.py` (this directory) implements one function,
`measure_far_tail(n,b,c,N,seed_seq,threshold,nworkers=4)`, built directly
against `sc_engine.build_instance`/`cyclic_mask_peeling`/`pi_cycle_lengths`
(no formula on the measurement side) — the same measurement logic as
`long_cycle_deficit_attempt/lcd_bsweep.py`'s `measure_far_tail`, but
authored fresh for this front (per this lineage's convention that each
front writes its own measurement code against the shared `sc_engine`/
`sc_formula` infrastructure rather than importing a sibling front's
diagnostic script) and parallelized across `nworkers=4` processes via
`multiprocessing.Pool.imap` for wall-clock feasibility at 26 measurement
runs. **Verified deterministic** before use: single-process and 4-process
runs on the same `SeedSequence` produce bit-identical `n_far`/`cyc_far`/`ρ`
arrays (throwaway check, seed `999900010`, `N=60`, not counted as data) —
`numpy.random.SeedSequence.spawn()` children are independent of how work is
distributed across workers.

`N=2000` per measurement (own-`b` and `b=1` each), matching
`long_cycle_deficit_attempt`'s own T2 `N` — chosen after a throwaway timing
check (seed `999900011`, `N=400`, 4 workers, `≈23ms/instance` effective)
showed the full 26-run grid completes in `≈20` minutes at this `N`, a
practical budget for a 13-cell design. This is below the parent front's own
`N=2500` T1; where a cell's own-`b` or `b=1` deficit turns out weak, its `z`
will honestly reflect that (and, per §2's exclusion rule, an underpowered
cell is excluded from the correlation analysis, not force-classified).

---

## 6. Seeds (fresh, reserved range `20260839000+` per `DISC-DEC-057` front
(e); confirmed unused anywhere in the archive by
`grep -rn "20260839"`/`"20260840"` restricted to text file types before
assignment — only `DECISION_LEDGER.yaml`'s own reservation line matched
either string, for both this front's range and the referee's adjacent
`20260840000+` range, which this front does **not** use)

| seed | use | N |
|---|---|---|
| `SeedSequence(20260839000)` | T0, `b=1` engine sanity re-check | 30 |
| `SeedSequence(20260839001)` | A, own-`b` (`b=100,c=1000`) | 2000 |
| `SeedSequence(20260839002)` | A, `b=1` (matched `c=1000`, threshold 2000) | 2000 |
| `SeedSequence(20260839003)` | G1a, own-`b` (`b=25,c=1000`) | 2000 |
| `SeedSequence(20260839004)` | G1a, `b=1` (threshold 500) | 2000 |
| `SeedSequence(20260839005)` | G1b, own-`b` (`b=50,c=1000`) | 2000 |
| `SeedSequence(20260839006)` | G1b, `b=1` (threshold 1000) | 2000 |
| `SeedSequence(20260839007)` | G1d, own-`b` (`b=200,c=1000`) | 2000 |
| `SeedSequence(20260839008)` | G1d, `b=1` (threshold 4000) | 2000 |
| `SeedSequence(20260839009)` | G2a, own-`b` (`b=100,c=200`) | 2000 |
| `SeedSequence(20260839010)` | G2a, `b=1` (threshold 2000) | 2000 |
| `SeedSequence(20260839011)` | G2b, own-`b` (`b=100,c=500`) | 2000 |
| `SeedSequence(20260839012)` | G2b, `b=1` (threshold 2000) | 2000 |
| `SeedSequence(20260839013)` | G2d, own-`b` (`b=100,c=2000`) | 2000 |
| `SeedSequence(20260839014)` | G2d, `b=1` (threshold 2000) | 2000 |
| `SeedSequence(20260839015)` | G3a, own-`b` (`b=335,c=300`) | 2000 |
| `SeedSequence(20260839016)` | G3a, `b=1` (threshold 6700) | 2000 |
| `SeedSequence(20260839017)` | G3c, own-`b` (`b=50,c=2000`) | 2000 |
| `SeedSequence(20260839018)` | G3c, `b=1` (threshold 1000) | 2000 |
| `SeedSequence(20260839019)` | G3d, own-`b` (`b=1007,c=100`) | 2000 |
| `SeedSequence(20260839020)` | G3d, `b=1` (threshold 20140) | 2000 |
| `SeedSequence(20260839021)` | B, own-`b` (`b=400,c=100`) | 2000 |
| `SeedSequence(20260839022)` | B, `b=1` (threshold 8000) | 2000 |
| `SeedSequence(20260839023)` | G4b, own-`b` (`b=80,c=500`) | 2000 |
| `SeedSequence(20260839024)` | G4b, `b=1` (threshold 1600) | 2000 |
| `SeedSequence(20260839025)` | G4c, own-`b` (`b=26,c=1500`) | 2000 |
| `SeedSequence(20260839026)` | G4c, `b=1` (threshold 520) | 2000 |
| `SeedSequence(20260839900+)` | any throwaway/exploratory run, discarded | — |

(Throwaway-only, outside the reserved range, already used and disclosed in
§5: `999900010`, `999900011`.)

---

## 7. Files planned

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | this document |
| `cv_measure.py` | shared measurement function (T0 + all 26 far-tail runs), imports `sc_engine`/`sc_formula` |
| `cv_grid.py` | driver: runs T0, then all 13 cells × 2 conditions in the locked order/seeds above, logs to `cv_grid.log` |
| `cv_analysis.py` | deterministic (no RNG) post-hoc analysis: H2 shares, delta-method SEMs, Pearson/OLS, sub-group ranges and the §4.3 decision rule, applied to `cv_grid.log`'s numbers |
| `cv_grid.log` | full run output |
| `cv_analysis.log` | analysis output |
| `ATTEMPT.md` | the write-up |

No git commit. Nothing outside this subfolder is touched. This front reuses
`short_cycle_dynamics_attempt/sc_engine.py` and `sc_formula.py` by import
(read-only), per the mandate's explicit permission, exactly as
`long_cycle_deficit_attempt` did.
