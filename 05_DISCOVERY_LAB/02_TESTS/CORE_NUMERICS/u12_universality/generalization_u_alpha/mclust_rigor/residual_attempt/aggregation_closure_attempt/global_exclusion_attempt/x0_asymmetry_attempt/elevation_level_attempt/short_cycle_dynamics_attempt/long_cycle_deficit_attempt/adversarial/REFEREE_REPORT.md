# REFEREE REPORT — adversarial review of `long_cycle_deficit_attempt/ATTEMPT.md`

**Wave 13, `DISC-DEC-054`, front (b) `LONG-CYCLE-DEFICIT-ATTEMPT`, mandatory
independent adversarial verification.**

Object under test: `long_cycle_deficit_attempt/ATTEMPT.md` together with its
`DERIVATION_PREREG.md`. Both were read in full, together with
`short_cycle_dynamics_attempt/ATTEMPT.md` §9 open item 1 and
`short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md` §4.1 (the
baseline this front's T1 reuses), before any line of code in this review was
written.

**Scope and discipline.** Everything produced by this review lives in
`long_cycle_deficit_attempt/adversarial/`. `git status --porcelain` (run at
review end) shows exactly one untracked path relative to `HEAD`: the
`long_cycle_deficit_attempt/` folder itself (this review's own subfolder is
inside it). No other file in the repository — not `ATTEMPT.md`, not
`DERIVATION_PREREG.md`, not any ancestor `ATTEMPT.md`/`REFEREE_REPORT.md`,
not `DECISION_LEDGER.yaml` — shows as modified. **No git commit was
created.**

**Independence.** Per the mandate's explicit, narrower-than-usual permission
for this review, `sc_engine.py` and `sc_formula.py` (parent directory,
already adversarially verified SOUND at 2.2× scale) were imported and
trusted as infrastructure. **This front's own new scripts,
`lcd_diagnostic.py` and `lcd_bsweep.py`, were never opened, imported, or
used as evidence at any point** — only `grep`-matched for their literal
seed constants (§7 below), never read for methodology. All measurement
logic (`ref_common.py`) was written from scratch directly against
`sc_engine.py`'s API and `DERIVATION_PREREG.md`'s prose description of the
quantity being measured (`φ(cyclic | x0∈R^c, L>threshold)`).

**Fresh seeds**, drawn from `20260828000+` — the range `DECISION_LEDGER.yaml`
(`DISC-DEC-054`) itself pre-reserves for *this front's referee* — confirmed
unused anywhere in the archive by `grep -rn "20260828"` before use (only the
ledger's own reservation line matched):

| seed | use | N |
|---|---|---|
| `SeedSequence(20260828100)` | T0 re-check (`R_mask==seed_mask`, `ρ≈c/n` at `b=1`) | 30 |
| `SeedSequence(20260828101)` | T1 cell A (`c=1000,b=1,n=65536`, `L>2000`) | 5000 |
| `SeedSequence(20260828102)` | T1 cell B (`c=100,b=1,n=65536`, `L>8000`) | 5000 |
| `SeedSequence(20260828103)` | T1 cell C (`c=150,b=1,n=65536`, `L>4000`) | 5000 |
| `SeedSequence(20260828110)` | T2 b-sweep, `b=1` | 2500 |
| `SeedSequence(20260828111)` | T2 b-sweep, `b=5` | 2500 |
| `SeedSequence(20260828112)` | T2 b-sweep, `b=20` | 2500 |
| `SeedSequence(20260828113)` | T2 b-sweep, `b=50` | 2500 |
| `SeedSequence(20260828114)` | T2 b-sweep, `b=100` | 2500 |

(A handful of throwaway seeds, `999900001`/`999900002`, were used only for
timing smoke-tests during development, discarded, not counted in any
reported number, matching this archive's disclosed-throwaway-seed
convention.) T1's `N=5000` is **2×** the front's own `N=2500`; T2's
`N=2500` per point is **25% above** the front's own `N=2000`.

---

## 0. VERDICT — **SOUND WITH NAMED ISSUES**

T0, T1 (the pre-registered PRIMARY/decisive test), and T2's qualitative
"MIXED/honest non-closure" verdict all **independently reproduce** at equal
or larger scale, with fresh seeds and completely from-scratch measurement
code. I found **no error that changes any of the front's conclusions**. I
did find:

1. A genuine **mis-sourced reference figure** for cell A (`−9.66%`) in
   `DERIVATION_PREREG.md` §3 (present at pre-registration time, so not a
   post-hoc artifact) — traced to the wrong cell *and* the wrong quantity
   from the parent referee's report. Coincidentally close in value to the
   correct figure, so it does not flip cell A's classification, but the
   "well under 1/3" framing built on it is more fragile than presented.
2. **T2's intermediate points (`b=20,50`) are more seed-sensitive than a
   single `N=2000–2500` run's own reported SEM suggests** — my replication's
   shape differs visibly from the front's at these two points (though no
   single point differs at conventional significance), which matters
   because T2's own discriminating rule hinges on ratios that sit close to
   its `2×`/`3×` decision boundaries in *both* runs.
3. A **positive finding that strengthens, not weakens, the front's own
   conclusion**: with 2× the sample size, cell A's T1 z-score crosses the
   pre-registered `z≤−3` bar (mine: `z=−3.39`; front's own post-hoc
   independent-seed combination already flagged this direction at
   `z=−3.70`), resolving the "gap the rule did not anticipate" the front
   flagged for cell A — a properly-powered rerun classifies cell A cleanly
   as **PRESENT BUT SMALLER**, exactly the front's own stated intuition.

None of this threatens the front's central claims or its own explicitly
non-overclaiming synthesis (§5 below).

---

## 1. T0 — engine sanity for `b=1` — **CONFIRMED, exactly**

**Code inspection** (the primary evidence, per the mandate). `sc_engine.py`'s
`build_R_mask(n, b, pi, seed_mask)`:

```python
def build_R_mask(n, b, pi, seed_mask):
    R = seed_mask.copy()
    cur = np.where(seed_mask)[0]
    for _ in range(1, b):
        if cur.size == 0:
            break
        cur = pi[cur]
        R[cur] = True
    return R
```

At `b=1`, `range(1, 1)` is the **empty range** — the loop body never
executes, unconditionally, for any `n`, `c`, `pi`, `seed_mask`. `R` is
therefore `seed_mask.copy()` **exactly**, with no other code path, branch,
or special-casing anywhere in the 320-line file (`build_f` depends only on
the already-computed `R_mask`, not on `b` directly) — I read the whole file,
not just this function, specifically hunting for a hidden `b=1` special case
per the mandate's explicit prompt, and found none. This is not an
approximation to plain M-U; it is definitionally identical to it (matching
`DERIVATIONS.md` §3.1/§3.5's own statement, cited correctly by the front).

**Empirical re-check** (belt-and-braces, `ref_t0.py`, seed `20260828100`,
`N=30`, fresh from my own code — not the front's `lcd_diagnostic.py`):

```
R_mask == seed_mask exactly at b=1: violations=0/30  OK
rho_formula (=c/n) = 0.015259   rho_meas = 0.015319+/-0.000079  z=+0.758  OK
```

Matches the front's own T0 result (`0/20` violations, `z=−1.84`) — both well
within noise of zero. **T0: CONFIRMED.**

---

## 2. T1 — PRIMARY: matched-`(c,n)` comparison, `b=1` vs original M-CLUST(b) — **CONFIRMED, and strengthened**

`ref_t1.py`, own from-scratch measurement (`sc_engine.build_instance`,
`pi_cycle_lengths`, `cyclic_mask_peeling`, no formula on the measurement
side), same absolute `L`-edges as the front, **standard error computed two
independent ways per cell** (Cochran-style ratio-estimator delta method,
cluster = instance; and a `B=2000`-replicate cluster bootstrap) — the two
agree to 3 significant figures at every cell (ratio `0.998`–`1.002`),
ruling out an underestimated-SE artifact on my side, matching the discipline
the parent referee used.

| cell | my `φ_far` | my SEM (delta / boot) | `φ_U(c)` | my dev% | my z (delta/boot) | front's dev% | front's z |
|---|---|---|---|---|---|---|---|
| A (target), N=5000, seed `...101` | 0.027314 | 0.000210 / 0.000210 | 0.028025 | **−2.537%** | **−3.387 / −3.388** | −2.52% | −2.39 |
| B, N=5000, seed `...102` | 0.079155 | 0.000681 / 0.000681 | 0.088623 | **−10.683%** | **−13.900 / −13.906** | −11.30% | −10.21 |
| C, N=5000, seed `...103` | 0.066373 | 0.000543 / 0.000544 | 0.072360 | **−8.274%** | **−11.020 / −10.999** | −8.60% | −8.04 |

**Point-estimate agreement with the front's own `N=2500` run** (`z_diff`
between my dev% and theirs, combining both SEMs): cell A `z_diff=−0.01`,
cell B `z_diff=+0.46`, cell C `z_diff=+0.25` — **all three cells agree with
the front's own numbers within trivial statistical noise.** This is a clean,
honest, non-cherry-picked reproduction at 2× scale.

**Verdict-relevant finding.** All three cells reproduce the deficit at
`b=1` (zero block correlation) at high significance (`z` from `−3.4` to
`−13.9`), same sign as the original `b` values throughout — directly
confirming T1's decisive finding. Applying the pre-registered rule to *my*
numbers: cell B (`10.68/14.7=72.7%`) and cell C (`8.27/10.7=77.3%`) both
still clear **PRESENT (comparable)** (`z≤−3` and `dev%≤−3`), so **T1 still
favors H2 by the pre-registered majority rule**, exactly as the front
concludes.

**Additional finding, not in the front's own report: cell A's ambiguity
resolves cleanly with adequate power.** The front's own `N=2500` run left
cell A "unclassified by the letter of the rule" because `z=−2.39` missed
the `z≤−3` bar (needed for either `PRESENT (comparable)` or
`PRESENT BUT SMALLER`). At `N=5000` I measure `z=−3.39` — **crossing the
bar** — while `dev%=−2.54%` stays essentially unchanged from the front's own
`−2.52%` (as it must, since it's an unbiased estimate of a fixed population
quantity; only the SEM shrinks with `N`, exactly matching the theoretical
`√(5000/2500)×2.39=3.38` scaling). With `dev%=−2.54%` at `26.2%` of the
correct reference (`−9.7%`, see §4 below) — comfortably under the `1/3`
`PRESENT BUT SMALLER` threshold — cell A now cleanly classifies as
**PRESENT BUT SMALLER**, exactly the front's own stated intuition ("closest
in spirit to PRESENT BUT SMALLER"). As an internal cross-check, I also
combined my own T1-cell-A point with my own T2 `b=1` point (§3;
independent seeds `...101` vs `...110`, same underlying quantity):
`z_diff=+0.81` (consistent), inverse-variance-weighted combination
`dev=−2.89%, z=−4.76` — closely matching the front's own analogous post-hoc
combination (`dev=−2.92%, z=−3.70`, §2 below) and further confirming cell
A's true effect is real, small, and stable. **This strengthens, rather than
undermines, the front's H2-leaning T1 conclusion**: properly powered, arguably
all three cells now classify under the pre-registered rule (2×
`PRESENT (comparable)`, 1× `PRESENT BUT SMALLER`), none `ABSENT`. **T1:
CONFIRMED.**

---

## 3. T2 — SECONDARY: b-sweep dose-response — qualitative verdict **CONFIRMED**; point-precision **NAMED ISSUE**

`ref_t2.py`, same measurement code, fixed target cell (`c=1000,n=65536`,
`L>2000` throughout), `N=2500` per `b` (front used `N=2000`):

| b | my ρ | my φ_U(c'') | my φ_far | my SEM | my dev% | my z | front's dev% | front's z |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.0152 | 0.028025 | 0.027023 | 0.000291 | **−3.58** | **−3.44** | −3.42 | −2.88 |
| 5 | 0.0739 | 0.028900 | 0.027945 | 0.000305 | **−3.31** | **−3.13** | −3.56 | −2.99 |
| 20 | 0.2648 | 0.032433 | 0.031074 | 0.000340 | **−4.19** | **−3.99** | −6.34 | −5.28 |
| 50 | 0.5366 | 0.040846 | 0.038527 | 0.000425 | **−5.68** | **−5.45** | −2.89 | −2.42 |
| 100 | 0.7847 | 0.059993 | 0.056159 | 0.000626 | **−6.39** | **−6.12** | −8.95 | −7.74 |

**Structural cross-check (independent of MC noise): qualifying-point counts
match the `N`-ratio essentially exactly at every `b`** — my `total_qualify`
divided by the front's, at `b=1,5,20,50,100`, is `1.2499, 1.2502, 1.2505,
1.2487, 1.2514` against an expected `2500/2000=1.2500`. This confirms my
independently-written measurement code counts **exactly the same
population** the front's script does (same `R^c` definition, same `L`
threshold, same `n`) at every point — any remaining discrepancy is purely
in *which* qualifying points end up cyclic (the numerator), i.e. genuine
Monte Carlo variation, not a definitional mismatch.

**Point-by-point agreement is good at the two endpoints, weaker in the
middle.** `z_diff` (combining both runs' SEMs) at each `b`: `b=1: −0.10`,
`b=5: +0.16`, `b=20: +1.35`, `b=50: −1.76`, `b=100: +1.64`. No single point
differs at conventional significance (`|z|<2` throughout), but the *pattern*
differs: the front's sweep has a pronounced dip at `b=50` (`−2.89%`, nearly
back to the `b=1` noise floor) then jumps to `−8.95%` at `b=100`; mine rises
smoothly and near-monotonically from `b=5` onward (`−3.31→−4.19→−5.68→−6.39`)
with no such dip. This is the T2 analogue of the *exact* phenomenon the
**parent's own referee already flagged and diagnosed** for the near-`b`
`L`-bins (§4.2 of `short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md`):
this statistic's effective sample size is closer to "number of instances"
(here, `N=2000–2500`) than to the raw point count (tens of millions), so
between-seed variance at this `N` is larger than the nominal precision of
any single point suggests — even though my own delta-method-vs-bootstrap SE
cross-check agrees to 3 figures at every point (ratio `0.955`–`1.019`),
ruling out an under-estimated-SE bug specifically; the noise is genuine
seed-to-seed clustering variance, not a broken estimator.

**Consequence for the pre-registered T2 rule.** My own ratios:
`max/min = 6.39/3.31 = 1.93×`, `b100/b1 = 6.39/3.58 = 1.79×` — *both lower*
than the front's (`3.10×`, `2.62×`). Applying the pre-reg's own rule to
*my* data: the ratio is `<2×` (favors H2's first condition), **but** `b=100`
is still my strict maximum with the rest of the sequence (after a small
`b=1→b=5` dip, itself the allowed "one exception") monotonically
increasing — which **fails** H2's second, "no monotonic trend" condition.
The `≥3×`/monotonic-non-decreasing H1 condition also fails (`1.79×≪3×`).
**My replication independently lands on the identical MIXED verdict**, via a
different combination of satisfied/failed sub-conditions than the front's
own run. Both runs' headline ratios sit close to the `2×`/`3×` boundaries —
this closeness, present in *two independent* `N~2000–2500` measurements,
is itself evidence that **T2 is inherently under-resolved at this sample
size**, not that the front's particular run was unlucky. The front's own
"MIXED / honest non-closure" framing for T2 is the right call, and is *more*
robust than a reader might guess from the single reported run alone — but
the **specific figures `2.62×`/`3.10×` should be read as illustrative,
not as precise, reproducible point estimates** (**NAMED ISSUE**, moderate:
this is a precision/stability caveat, not a correctness error — it affects
how much weight a future front should put on the *exact* ratio, not
whether T2's own MIXED verdict is right). **T2: qualitative verdict
CONFIRMED; quantitative precision flagged.**

*Minor, cosmetic:* the `ρ` column in the front's T2 table is close to but
not bit-identical to `sc_formula.rho_of` (e.g. `0.2645` reported vs
`0.26474` formula at `b=20`) — consistent with it being the *measured*
`R_mask.mean()` over `N=2000` instances rather than the closed-form value,
which is unlabeled but not an error (my own measured `ρ` shows the same
small, expected gap from formula: `0.26479` vs `0.26474`).

---

## 4. Formula and arithmetic audit — **all confirmed correct, except one reference-figure mis-citation**

`ref_formula_checks.py`, deterministic, no randomness (log:
`ref_formula_checks.log`).

- **`φ_U(c)` cross-checked against an independent `scipy.integrate.quad`**
  evaluation of `∫₀¹exp(−ct²)dt` at `c=1000,100,150`: relative error
  `≤1.57×10⁻¹⁶` — `sc_formula.phi_U` is the closed form, exactly.
- **T1's `φ_U(c)` column** (`0.028025, 0.088623, 0.072360` for cells A/B/C)
  matches `sc_formula.phi_U(c)` for the front's stated `c` values exactly —
  no cell used the wrong `c`.
- **T2's `φ_U(c'')` column** at `b=1,5,20,50,100,c=1000,n=65536` matches
  `sc_formula.phi_U(sc_formula.c_double_prime(b,1000,65536))` exactly at
  every `b` — no row used the wrong formula or the wrong `b`.
- **`c''(b=1,c,n)=c` exactly**, confirmed algebraically (`(1−c/n)⁰=1`) for
  all three cells — the front's claimed special case at `b=1` holds.
- **All five reported arithmetic ratios recompute exactly**: `11.30/14.7=
  76.87%≈77%`; `8.60/10.7=80.37%≈80%`; `8.95/2.89=3.0969≈3.10×`;
  `8.95/3.42=2.6170≈2.62×`; `3.42/8.95=38.21%≈38.2%`.
- **The post-hoc inverse-variance-weighted combination (T1 cell A + T2
  `b=1`)** recomputes exactly from the front's own stated inputs:
  `z_diff=+0.567` (claimed `+0.57`), combined `dev%=−2.917` (claimed
  `−2.92%`), combined `z=−3.701` (claimed `−3.70`). **No arithmetic error
  anywhere in this front's numeric claims.**

**One genuine issue found: the "`−9.66%`" reference figure for cell A is
mis-sourced.** `DERIVATION_PREREG.md` §3 (written *before* any data —
confirmed a pre-registration-stage error, not post-hoc cherry-picking)
attributes "cell A `−9.66%`" to `short_cycle_dynamics_attempt/ATTEMPT.md`
§3.1's own reported figure. Checked directly: that section's actual
`(20b,∞)` row for cell `(100,1000)` (=cell A/target) is **`−9.7%`
(`z=−9.4`)**, not `−9.66%`. The literal digit string `"9.66"` appears
**exactly once** elsewhere in the whole archive tied to a percentage
figure — `short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md` line
256 / `adv_reduction.log` line 43 — and that occurrence is for cell
**`b=400,c=100`** (this front's own **cell B**, not cell A), comparing
*measured full-φ against `φ_REDC_full`* (the already-refuted reduction
formula, from the parent referee's §3.2 six-cell reduction test) — a
**different quantity from a different test** than the `(20b,∞)`
far-tail-vs-`φ_U(c'')` figure T1 actually reuses. So `−9.66%` is
mis-sourced on two independent axes (wrong cell, wrong quantity).
**Materiality:** the value is coincidentally close to the correct one
(`9.66` vs `9.7`), so cell A's stated "`26%` of reference, well under `1/3`"
classification text is *not* materially changed by using the correct
figure instead (`2.52/9.7=26.0%` vs the reported `2.52/9.66=26.1%`).
**But** the front's own `DERIVATION_PREREG.md` §0 correctly cites the
parent referee's *confirmed range* for cell A as `−6.4%` to `−9.7%` (the
widest independently-replicated spread of the three cells, per
`short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md` §4.1). Using
the *low* end of that same pre-registered range instead: `2.52/6.4=39.4%`
— **not** "well under `1/3`". The front does not disclose that its
qualitative framing depends on which end of its own confirmed range is
used as "the" reference — a genuine, findable citation error, though one
that (by chance, not by choice) landed near the high, more favorable end of
the range and did not flip any classification. **NAMED ISSUE, minor-to-moderate.**
Cell B (`−14.7%`) and cell C (`−10.7%`) references, by contrast, are
correctly sourced — verified to match `short_cycle_dynamics_attempt/
ATTEMPT.md` §3.1's own `(20b,∞)` rows for `(400,100)` and `(200,150)`
exactly (`−14.7% z=−13.3` and `−10.7% z=−9.7` respectively).

---

## 5. Hunting for problems — other checks performed, no further issues found

- **Double-counting / selection effects:** T1's pre-registered majority
  tally uses only the single pre-committed run per cell; the T1-cell-A +
  T2-`b=1` combination is explicitly labeled "post-hoc, not part of the
  pre-registered tally" and uses two *independently seeded* runs of the
  identical quantity — this is a legitimate meta-analytic combination, not
  double-counting (verified by inspecting both cited seeds, `...001` vs
  `...010`, and confirming they are in fact distinct RNG streams).
- **Off-by-one in `L`-threshold definitions:** checked `L>edge` (strict)
  is used consistently in both prose and my re-implementation, at every
  cell and in T2; T3's sub-bin edges (`n/8=8192, n/4=16384, n/2=32768` at
  `n=65536`) are exact integers with no ambiguity.
- **`b=1` hidden special-casing beyond `build_R_mask`:** none found —
  `build_f` depends only on the already-computed `R_mask`, not on `b`
  directly (§1 above); confirmed by reading the whole file.
- **Seed-table honesty:** `grep`-matched (not read for methodology) the
  literal seed constants in `lcd_diagnostic.py` (`20260827000/001/002/
  003/020`) and `lcd_bsweep.py` (`20260827010–014`) — both match the seed
  table in `ATTEMPT.md`/`DERIVATION_PREREG.md` exactly.
- **T3** (the `L/n`-reroute mechanism refutation) was **not**
  independently re-simulated — outside the required scope of this review
  (T0/T1/T2 were the mandated re-runs; T3 is explicitly non-required for
  the H1-vs-H2 verdict per the front's own pre-registration). I confirmed
  only its stated bin edges are exact and consistent; the qualitative
  "flat-then-declining" claim is not independently re-verified here and
  should be treated as **not audited by this review**.

---

## 6. Is the front's "honest partial closure" framing accurate?

**Yes — if anything, slightly conservative in the direction that favors
credibility, not overclaiming.** T1's H2-favoring majority result reproduces
cleanly and, with adequate power, generalizes to all three cells (not just
two of three) under the pre-registered rule. T2's refusal to call a clean
H1-or-H2 verdict is well-founded — not merely because the front's own
`3.10×`/`2.62×` narrowly missed the `2×`/`3×` bars, but because an
independent, differently-seeded replication at higher `N` lands on ratios
(`1.93×`/`1.79×`) that are *also* ambiguous relative to those same bars,
via a different combination of sub-conditions. The two-component synthesis
("a b-independent finite-`n` floor plus a smaller, real, sub-threshold
b-dependent amplification") is a fair description of what both runs show,
and the front is explicit that no closed form is proposed or warranted.
**No overclaim found; no underclaim found beyond cell A's classification,
which this review resolves in the front's own favor.**

---

## 7. Errors and issues found, ordered by importance

1. **`DERIVATION_PREREG.md` §3 / `ATTEMPT.md` §2's cell-A reference figure
   `−9.66%` is mis-sourced** — traced to a different cell (`b=400,c=100`,
   this front's own cell B) and a different quantity (`φ_REDC_full`
   comparison, parent referee §3.2) than the `(20b,∞)`
   far-tail-vs-`φ_U(c'')` figure it is presented as. Coincidentally close
   in value to the correct figure (`−9.7%`), so no classification flips,
   but the "well under `1/3`" framing is more fragile than presented (using
   the front's own confirmed range's low end, `−6.4%`, the same ratio is
   `39.4%`, not "well under `1/3`"). **Does not threaten any of the front's
   conclusions** — cell A fails the `z≤−3` bar either way under the front's
   own `N=2500` run, regardless of which reference value is used.
2. **T2's intermediate points (`b=20,50`) show more between-seed variance
   than their own reported SEMs alone would suggest**, mirroring a
   precision issue the *parent* front's own referee already diagnosed for
   an analogous statistic. Both the front's ratios (`3.10×`/`2.62×`) and my
   independent replication's ratios (`1.93×`/`1.79×`) sit close to the
   pre-registered `2×`/`3×` decision boundaries, on opposite sides of some
   of them — evidence the statistic is genuinely under-resolved at
   `N~2000–2500`, not that either run is simply wrong. **Does not change
   T2's own MIXED verdict**, which both runs independently reach.
3. No other error found. T0's algebraic claim, T1's primary result (all
   three cells, both point estimates and significance), and T2's
   qualitative dose-response conclusion all independently confirm. Every
   arithmetic ratio and the post-hoc weighted-combination numbers in the
   document recompute exactly from the document's own stated inputs.

---

## 8. Scorecard

| claim | status | evidence |
|---|---|---|
| T0: `b=1` ⟹ `R=seed_mask` exactly, zero block correlation | **CONFIRMED**, algebraically (code read) and empirically (0/30 violations, fresh seed) | §1, `ref_t0.py` |
| T1: deficit present at `b=1` for cells B, C (`PRESENT (comparable)`) | **CONFIRMED**, `N=5000` (2×), point estimates agree with front's `N=2500` run within `|z_diff|≤0.46` | §2, `ref_t1.py` |
| T1: cell A weak/marginal, "closest in spirit to PRESENT BUT SMALLER" | **CONFIRMED, and resolved**: at `N=5000`, `z=−3.39` crosses the bar, cell A classifies cleanly as PRESENT BUT SMALLER | §2, `ref_t1.py` |
| T1 majority rule → favors H2 | **CONFIRMED**, robust to my independent re-measurement (2 of 3, or arguably 3 of 3 with adequate power) | §2 |
| T2: MIXED / honest non-closure by the pre-registered numeric rule | **CONFIRMED**, independently, via a different combination of satisfied/failed sub-conditions | §3, `ref_t2.py` |
| T2: `2.62×`/`3.10×` specific ratios | **NAMED ISSUE** — not precisely reproducible at `N~2000–2500`; qualitative "real, sub-3× growth" story holds, exact figures are noise-dominated | §3 |
| `φ_U(c)`, `φ_U(c'')`, `c''(b=1,c,n)=c` formulas used correctly per cell | **CONFIRMED**, exact match to independent `scipy.integrate.quad` and to `sc_formula.py` at every cell/row | §4, `ref_formula_checks.py` |
| All reported arithmetic ratios and the post-hoc weighted combination | **CONFIRMED**, exact recomputation | §4 |
| Cell A reference figure `−9.66%` | **NAMED ISSUE** — mis-sourced (wrong cell, wrong quantity); non-outcome-changing | §4 |
| No double-counting in the post-hoc T1/T2 combination | **CONFIRMED** — genuinely independent seeds | §5 |
| Scope discipline (nothing outside the front's folder touched) | **CONFIRMED** | `git status --porcelain` |
| No overclaim in the synthesis (§5/§6 of `ATTEMPT.md`) vs. the body | **CONFIRMED** | manual audit, §6 above |

---

## 9. Files produced by this review (all in `long_cycle_deficit_attempt/adversarial/`)

| file | role |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref_common.py` | shared measurement code — imports `sc_engine`/`sc_formula` from the parent directory; own from-scratch `run_cell` (multiprocessing across 4 workers, delta-method ratio-estimator SEM + cluster-bootstrap cross-check) |
| `ref_t0.py` / `ref_t0.log` | T0 re-check, seed `20260828100`, `N=30` |
| `ref_t1.py` / `ref_t1.log` | T1 re-run, 3 cells, `N=5000` each, seeds `20260828101–103` |
| `ref_t2.py` / `ref_t2.log` | T2 re-run, full 5-point `b`-sweep, `N=2500` each, seeds `20260828110–114` |
| `ref_formula_checks.py` / `ref_formula_checks.log` | deterministic formula/arithmetic audit — `φ_U` vs `scipy.integrate.quad`, every table value in the document, every claimed ratio, the post-hoc weighted combination, and the `−9.66%` reference-figure provenance trace |
