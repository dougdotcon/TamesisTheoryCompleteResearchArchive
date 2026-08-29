# ATTEMPT — testing the `(c/n)^{1/4}` rate candidate (and neighbors)
# against the abstract-vs-real gap bin data (`MCLUST-GAP-RATE-CANDIDATE-ATTEMPT`)

**Wave 25, front (d), authorized by `DISC-DEC-118` in
`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`.** Target: the
concrete, explicitly-named, not-yet-executed next step flagged by the
hostile referee (`DISC-DEC-085`, correction "N1") on
`mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md` §A.4 — test the
candidate rate law `(c/n)^{1/4}` directly against the abstract-vs-real
gap bin data, whose prefactor (`~1.10×`) the referee found numerically
closer to the observed `~38.8%` gap than the three rates the target
document actually tested (`1/n`, `1/√n`, `√(c/n)`), but which was never
itself tested against the bin-resolved data. For exhaustion of the
"simple power law in `c/n`" candidate class, the neighboring exponents
`(c/n)^{1/3}` and `(c/n)^{1/5}` are tested alongside it.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`), the b=1
floor's abstract `(s,g)` recursive process — pure combinatorial/asymptotic
mathematics about a random-permutation-with-reroutes ensemble. It is a
standalone object, entirely independent of the archive's separate Tree A
(u₁/₂ / "Lemma Aberto") line in `THEOREM.md`. Nothing here is, or is
adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.**

**Seeds: none used.** This front's reserved range `20260932000-999` was
grep-confirmed unused before work began (`grep -rn "20260932"
05_DISCOVERY_LAB/` matched only the ledger reservation line and the
`DISCOVERY_LAB_STATE.md` block-summary line — see §Seeds below). Every
result in this document is a deterministic arithmetic computation
(`Decimal`/plain-`float` transcription cross-checks and closed-form power
evaluations) against already-published, already-vetted bin data — no
Monte Carlo, no simulation, no randomness of any kind was needed or used.

---

## EXECUTIVE SUMMARY (read first)

**Outcome tier: (b) elimination of the simple-power-law-in-`(c/n)`
candidate CLASS as a SHAPE explanation for the abstract-vs-real gap's
`t0`-dependence, rigorously (not just numerically) — combined with (c) a
sharper diagnosis of why the referee's magnitude-level "closeness" of
`(c/n)^{1/4}` is best read as a numerical coincidence at one calibration
point, not evidence for a genuine rate law. No candidate reaches tier (a)
closure under the precision bar stated below (§1).**

- **Structural fact, established here first (not previously stated this
  way):** in every bin table this front (or the parent front) has access
  to, `c=1000` and `n=65536` are FIXED — only `t0=L/n` varies bin to bin.
  Consequently `(c/n)^p`, for ANY exponent `p`, is a single CONSTANT
  NUMBER across every bin. This makes the candidate class structurally
  **shape-blind by construction**: fitting a prefactor `A` to minimize
  the sum of squared residuals against the bin data reduces exactly to
  fitting the sample mean (`A* = mean(gap)/rate`), and the resulting
  per-bin residuals are IDENTICAL, bin-for-bin, for `p=1/3`, `1/4`, and
  `1/5` — verified numerically to `<1e-9` (`r02_power_law_fit.py`,
  "degeneracy check"). **No exponent in this family can ever explain any
  part of the observed `t0`-trend** (the weak `r=0.33` correlation on the
  cluster-robust T2 composite table); this is provable from the data's
  own dependency structure, not merely an empirical near-miss.
- **Magnitude-only comparison** (the only axis on which these candidates
  *can* differ): using the cluster-robust T2-composite table (the more
  reliable of the two, per the parent front's own §A.2 caveat), the
  best-fit prefactor is `1.5633×` for `p=1/3`, `1.1033×` for `p=1/4`
  (essentially reproducing the referee's own `~1.10×`, confirming this
  front uses the same convention), and `0.8951×` for `p=1/5` — i.e.
  **`p=1/5` is numerically about as close to a "natural" (order-unity)
  prefactor as `p=1/4`**, just from the other side (`0.895` vs `1.103`,
  both `~10-11%` from unity). `p=1/3` is clearly worse (`56%` from unity).
- **Why `1/4`'s closeness is not, on inspection, "special":** solving
  `(c/n)^{p*} = mean(gap)` exactly for the exponent that gives a prefactor
  of EXACTLY `1` gives `p* = 0.2265` on T2-composite and `p* = 0.2140` on
  T1 — a generic real number close to neither `1/4` nor `1/5` exclusively,
  and **drifting between the two available tables of the same underlying
  quantity** depending on binning convention. Because `(c/n)^p` sweeps
  continuously and monotonically from `1` (at `p=0`) to `0` (as
  `p→∞`), *some* `p*` giving prefactor `≈1` is guaranteed to exist near
  any target percentage — landing close to a "nice" fraction like `1/4`
  is therefore not, by itself, informative confirmation of anything.
- **Precision bar (§1) is failed by all three exponents, even under the
  most generous (best-fit, not "natural") prefactor**: the T2-composite
  max per-bin residual is `4.42` percentage points (pp) — over the
  stated `3pp` closure tolerance — and the (less reliable, uncorrected)
  T1 table's max residual is `14.13pp`, far over. **No closure.**
- **Exploratory extension (clearly flagged, beyond the literal mandate,
  §4):** replacing the fixed `n` by a `t0`-dependent "remaining room"
  `n_eff(t0) = n(1-t0)`, motivated by the parent front's own boundary
  (`s+g≤1`) discussion, does NOT rescue the shape — it makes the fit
  decisively WORSE (`R² = -13.6` on T2-composite relative to the flat
  mean-only null, for `p=1/4`; all three exponents strongly negative on
  both tables). This corroborates, independently, the parent front's own
  §A.3 finding that the boundary mechanism is not the primary driver.
- **What this front adds to the record, honestly stated:** (i) the
  named-but-untested candidate `(c/n)^{1/4}` is now tested, and does NOT
  close the gap; (ii) the whole class of `(c/n)^p` power laws is shown,
  rigorously, to have zero capacity to explain the gap's (weak but
  real, cluster-robust, `r=0.33`) `t0`-dependence — a structural
  elimination, not just a numerical failure to fit; (iii) the referee's
  own "closer" observation for `p=1/4` is traced to a single-point
  magnitude coincidence, quantified and shown not to be robust across
  the two available bin tables of the same quantity; (iv) a natural,
  cheap `t0`-dependent generalization is tried and found to make things
  worse, not better. **The gap's true source remains unidentified** —
  this front narrows the search space (away from simple power laws in
  `c/n`, fixed or boundary-adjusted) without replacing the explanation.

No formula of record (`φ_REDB`, `Φ_U(c)`, `Φ_∞(c)`, the four-term
asymptotic law) is touched or proposed as changed anywhere below.

---

## 0. Reading discipline and data provenance

Read in full, prose, before any computation: the parent front's own
`.../mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md` (all of Part A,
§A.1-§A.6, plus its executive summary and §0 provenance section); its
`adversarial/REFEREE_REPORT.md` §4.3 (the exact source of the N1 finding
and its `ref08_scaling_completeness.py`/`.log`, which independently
computed the `1.56×`/`1.10×` prefactors this front's own §2 reproduces
and extends); the relevant dated addendum in
`05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/PROOF_DEPENDENCY_MAP.md`
(the `2026-08-26 — DISC-DEC-083/DISC-DEC-085` entry under node
`PLATRESUM`). The ultimate source of the T1/T2 bin data itself
(`floor_closed_form_attempt/ATTEMPT.md` §2, §4) was consulted only to
confirm the parent front's own transcription (its SEM columns, used in
§5 below); no re-simulation of the real engine was performed anywhere in
this front.

**This front's own new subdirectory** (everything written to, per the
mandate, confined to):
```
.../plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/
    gap_rate_candidate_attempt/
```
Nothing outside it — including the parent `mclust_plateau_abstract_real_
gap_attempt/ATTEMPT.md` itself and the sibling `mclust_h1_validity_
attempt/` subdirectory (a separate, later, wave-20 front on a different
question, H1) — was written to. Both were read-only references. No
`THEOREM.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`,
`PROOF_DEPENDENCY_MAP.md`, `README.md`, or `index.html` file was opened
for writing. No git command was run.

**Inputs taken as established** (PROVED/vetted, cited not re-derived):
```
Pi(1000) = Phi(0,t0>=0.02) = 0.0377615983402126188243712025905770479904...
  (the exact abstract plateau constant; established by FLOORH2 + PLATRESUM,
   re-cross-validated 3x independently including by the parent front's own
   g04/ref04 grids to <1e-38 relative -- reused here as a constant.)

c = 1000, n = 65536   (the record's fixed target cell, restated
  identically by every document in this lineage since wave-14)

T1 (absolute-ell bins) and T2-composite (relative L/n bins,
cluster-robust at bins 8,9 per floor_closed_form_attempt's own finding):
  gap%_i := (Pi_abstract - phi_real_i) / phi_real_i * 100
  -- transcribed verbatim from the parent front's Sec A.2 tables.
```

---

## 1. Precision bar (stated up front, before any fit is examined)

To avoid post-hoc rationalization, the closure/elimination bars are fixed
here, before §2's results are read as pass/fail:

- **CLOSURE (tier a)** requires, for the T2-composite table (the more
  reliable of the two — see §0 and the parent front's own §A.2 caveat
  about T1 not being cluster-corrected): a candidate rate `(c/n)^p`, using
  a prefactor `A` that is either (i) exactly `1` ("no free parameter"), or
  (ii) fitted but lying within `±25%` of unity (`A∈[0.75,1.25]`, a
  generous but not unlimited "order-unity, not an arbitrary fudge factor"
  bound), predicts **every** bin's `gap%_i` to within **`3` percentage
  points** (chosen as materially less than half of T2-composite's own
  observed `7.41pp` total spread — a tolerance that would make the
  candidate a genuinely tight fit, not just "same order of magnitude").
  A candidate satisfying this is closure.
- **ELIMINATION (tier b) — of the CLASS, not merely one exponent** — holds
  if it can be shown, independent of curve-fitting quality, that no
  exponent in the family can in principle explain the observed
  `t0`-dependence (as opposed to merely its level/mean) — i.e. a
  structural argument, not a numerical near-miss. (§2 below establishes
  exactly this.)
- Otherwise, the honest report is **(c) sharper diagnosis without a
  winning candidate** — precisely quantifying how close/far each tested
  exponent comes, and why.

---

## 2. Core result: the candidate class is shape-blind by construction

### 2.1 The structural fact

`c=1000` and `n=65536` never vary across any bin in T1 or T2 — only
`t0=L/n` does. `c/n = 1000/65536 = 125/8192 = 0.0152587890625` exactly,
a SINGLE number, for every bin. Hence `rate(p) := (c/n)^p` is likewise a
single number per exponent, identical across all bins. Fitting
`gap_i ≈ A·rate(p)` by ordinary least squares over bins therefore has the
closed-form solution `A* = mean(gap)/rate(p)` (elementary: the normal
equation for a constant regressor `x_i≡rate(p)` reduces to `A*·rate(p) =
mean(gap)`) — i.e. **the best-fit prediction for every bin is just the
sample mean**, regardless of which `p` is chosen.

**Verified numerically** (`r02_power_law_fit.py`, "degeneracy check"
section, `r02_power_law_fit.log`): for `p ∈ {1/3, 1/4, 1/5}`, on both T1
and T2-composite, `max_i |model_residual_i - (gap_i - mean(gap))|` is
`≤ 7×10⁻¹⁵` (pure floating-point roundoff) — i.e. **exactly** as
predicted. The Pearson correlation of the fitted-model residuals against
`t0` is therefore, and is verified to be, IDENTICAL to the raw correlation
of `gap_i` against `t0` itself: `r=+0.0211` (T1) and `r=+0.3301` (T2
composite, matching the parent's own `0.331` to 4 significant figures).

**Reading this plainly:** whatever fraction of the observed `t0`-trend is
"real" (T2-composite's cluster-robust `r=0.33`, weak but the parent
front's own honest characterization, not this front's invention), **0%**
of it can ever be attributed to a candidate of the literal form
`(c/n)^p` with `c,n` fixed at the single measured cell — the model has no
free parameter capable of producing ANY `t0`-dependence at all. This is
not a fitting failure to be improved with a better exponent; it is a
structural property of the candidate class given this dataset. **This
alone is sufficient to answer the mandate's "is the shape of the
`t0`-dependence actually well-matched, or just coincidentally close in
magnitude" question: it is not matched at all — it cannot be, by
construction — so any apparent closeness is necessarily a magnitude-only
coincidence.**

### 2.2 Magnitude-only comparison across exponents

Since shape is moot, the only remaining question is how close each
exponent's rate comes to the OBSERVED LEVEL (mean gap), and whether that
requires an implausible prefactor. Full table (`r02_power_law_fit.py`,
`r02_power_law_fit.log`; both bin tables shown, T2-composite is the
primary/more-reliable one per §0):

**T2-composite (mean gap = 38.7756%, n=9 bins, the primary table):**

| candidate | rate `(c/n)^p` | best-fit prefactor `A*` | `\|A*-1\|` | RMS resid. (fit, pp) | max\|resid\| (fit, pp) | RMS resid. (natural `A=1`, pp) |
|---|---|---|---|---|---|---|
| `1/n` | `0.0015%` | `25412` | huge | 2.345 | 4.424 | 38.845 |
| `1/√n` | `0.3906%` | `99.27` | huge | 2.345 | 4.424 | 38.457 |
| `(c/n)^(1/2)` = `√(c/n)` | `12.3526%` | `3.1390` | `2.14` | 2.345 | 4.424 | 26.527 |
| `(c/n)^(1/3)` **[new]** | `24.8031%` | `1.5633` | `0.56` | 2.345 | 4.424 | 14.168 |
| `(c/n)^(1/4)` **[new, N1 target]** | `35.1463%` | `1.1033` | `0.10` | 2.345 | 4.424 | 4.321 |
| `(c/n)^(1/5)` **[new]** | `43.3216%` | `0.8951` | `0.11` | 2.345 | 4.424 | 5.115 |

**T1, absolute-`ell` bins (mean gap = 40.8533%, n=6 bins, NOT
cluster-corrected — retained for completeness only, per the parent
front's own caveat that its shape may partly be correlated-bin-noise):**

| candidate | rate | `A*` | `\|A*-1\|` | RMS resid. (fit, pp) | max\|resid\| (fit, pp) | RMS resid. (natural `A=1`, pp) |
|---|---|---|---|---|---|---|
| `1/n` | `0.0015%` | `26774` | huge | 7.201 | 14.133 | 41.482 |
| `1/√n` | `0.3906%` | `104.58` | huge | 7.201 | 14.133 | 41.098 |
| `(c/n)^(1/2)` | `12.3526%` | `3.3073` | `2.31` | 7.201 | 14.133 | 29.396 |
| `(c/n)^(1/3)` | `24.8031%` | `1.6471` | `0.65` | 7.201 | 14.133 | 17.591 |
| `(c/n)^(1/4)` | `35.1463%` | `1.1624` | `0.16` | 7.201 | 14.133 | 9.188 |
| `(c/n)^(1/5)` | `43.3216%` | `0.9430` | `0.06` | 7.201 | 14.133 | 7.612 |

**Reading (magnitude only):** on T2-composite, `p=1/4` and `p=1/5` are
both within `~11%` of a unit prefactor (`1.10×` and `0.90×`
respectively) — genuinely close, reproducing the referee's own `~1.10×`
figure for `p=1/4` almost exactly (this front's `1.1033` vs. the
referee's quoted `~1.10`) and confirming this front is using the same
`(c,n)` convention. `p=1/3` is clearly worse (`1.56×`). On T1, `p=1/5`
is marginally the closest to unity (`0.94×`, vs `1.16×` for `p=1/4`) —
**the ranking between `1/4` and `1/5` is not even stable across the two
available bin tables of the same underlying quantity**, which is the
first concrete piece of evidence that "closeness to `1/4`" specifically
is not a robust signal (elaborated in §3).

### 2.3 Closure-bar verdict (§1's stated tolerance)

Even under the single most generous evaluation — the best-FIT prefactor
(not a "natural" one), which by §2.1 makes every bin's prediction equal
to the sample mean — the max per-bin residual is **`4.42pp` on
T2-composite** and **`14.13pp` on T1**, both **exceeding the stated
`3pp` closure tolerance**, for every one of the three exponents
identically (§2.1's degeneracy). **No candidate reaches tier (a) closure**
on either table, under the bar fixed in §1 before this section was
written.

---

## 3. Why `(c/n)^{1/4}`'s magnitude-closeness looks coincidental

Because `g(p):=(c/n)^p` is continuous and strictly monotonically
decreasing in `p` (from `1` at `p=0` to `0` as `p→∞`), for ANY target
percentage strictly between `0%` and `100%` there necessarily EXISTS some
real `p*` with `g(p*)` = that target exactly — i.e. a prefactor-1 match
is guaranteed to exist SOMEWHERE near any observed level, for a
sufficiently fine choice of `p`. This makes "prefactor close to `1` for
SOME simple-looking fraction `p`" a weak form of evidence on its own —
what would be informative is if the fraction that works were independently
motivated (derived from theory before being checked), or if it were
STABLE across independent measurements of the same target quantity.
Neither holds here:

**Solving for the exact unit-prefactor exponent** `p*` such that
`(c/n)^{p*} = mean(gap)` (`r02_power_law_fit.py`, "exact-unit-prefactor
exponent" section):

| table | mean gap | `p*` | `1/p*` |
|---|---|---|---|
| T2-composite (primary) | `38.7756%` | `0.226505` | `4.4149` |
| T1 (uncorrected) | `40.8533%` | `0.214025` | `4.6723` |

`p*≈0.2265` (T2) and `p*≈0.2140` (T1) are unremarkable real numbers,
close to neither `1/4=0.25` nor `1/5=0.20` specifically — they sit
roughly midway between the two, drifting by about `6%` relative between
the two available bin tables of the SAME underlying gap quantity, purely
as a function of which (already-published, already-vetted) binning
convention is used. **A genuine rate law derived from the process's own
dynamics should not depend on the analyst's choice of histogram bins.**
This drift is a second, independent piece of evidence (beyond §2.1's
shape-blindness) that the referee's `~1.10×` "closeness" for `p=1/4` is
best read as: `1/4` happens to be the nearest conventionally-simple
fraction to the true unit-prefactor exponent AT ONE FIXED calibration
point (`c=1000,n=65536`) — not as a signature of an underlying `1/4`
power law. With only one `(c,n)` pair measured anywhere in this archive's
M-CLUST(b) plateau-gap record (confirmed by a search of every `ATTEMPT.md`
under this lineage for a second, independently-measured `(c,n,gap)`
triple — none exists; see §6), this candidate class is fundamentally
UNDERDETERMINED from the available data: one number (the mean gap) cannot
simultaneously pin down two free parameters (exponent AND prefactor) in a
way that is falsifiable, only in a way that is always satisfiable for an
appropriate `p`.

---

## 4. Exploratory, non-mandate extension: a `t0`-dependent generalization

The mandate's own wording ("whether the shape ... is actually
well-matched ... or just coincidentally close") invites checking whether
a natural, CHEAP generalization that restores genuine `t0`-dependence
does any better. This is explicitly flagged as **beyond** the literal
`(c/n)^{1/4}`-class mandate — a bonus robustness check, not a required
deliverable, and not itself a new theoretical claim.

Motivated by the parent front's own §A.3 discussion (the `s+g≤1` boundary
/ "room" `1-t0`), define an effective remaining pool `n_eff(t0) :=
n·(1-t0)` and `rate_eff(t0,p) := (c/n_eff(t0))^p`, which genuinely varies
bin-to-bin (growing as `t0→1`, where "room" shrinks) — making a real,
non-degenerate least-squares fit of a single prefactor `A` possible.
(`r03_perbin_and_exploratory.py`, "Part B", `r03_perbin_and_exploratory.log`.)

| `p` | table | fitted `A` | RMS resid (pp) | max\|resid\| (pp) | `R²` vs. flat-mean null |
|---|---|---|---|---|---|
| `1/3` | T1 | `1.3888` | `10.532` | `16.361` | `-1.139` |
| `1/3` | T2-composite | `1.0155` | `12.091` | `26.177` | **`-25.58`** |
| `1/4` | T1 | `1.0326` | `9.218` | `13.005` | `-0.639` |
| `1/4` | T2-composite | `0.8237` | `8.959` | `20.554` | **`-13.59`** |
| `1/5` | T1 | `0.8615` | `8.556` | `11.209` | `-0.412` |
| `1/5` | T2-composite | `0.7186` | `7.123` | `16.832` | **`-8.22`** |

**Every `R²` is strongly negative** — i.e. this `t0`-dependent
generalization fits WORSE than simply predicting the flat sample mean for
every bin, on both tables, for all three exponents. The mechanism fails
specifically because `n_eff(t0)→0` as `t0→1`, driving `rate_eff` up
sharply near the tail (e.g. `p=1/4`, T2: predicted `58.0%` at `t0=0.938`
vs. observed `37.46%`, a `-20.55pp` miss) — the real data does NOT show
this upturn (T2-composite's largest gap, `43.20%`, occurs at `t0=0.812`,
not at the extreme tail `t0=0.938`, exactly the same "no boundary blow-up"
pattern the parent front's own §A.3 already reported by a different,
qualitative argument). **This is independent, quantitative corroboration
of the parent front's finding that the `s+g≤1` boundary mechanism is not
the primary driver** — obtained here via a completely different route
(a fitted rate-law extension) than the parent's own PDE-characteristics
argument.

---

## 5. Complete comparative table (mandate's "exhaustion" request)

Combining this front's new results with the parent front's own
already-established findings (cited, not re-derived) for a single
side-by-side view. "Status" reflects each candidate's own best framing
per the document that examined it:

| candidate | type | best available match to `~38.8%` gap | shape (`t0`) content | status |
|---|---|---|---|---|
| `1/n` | finite-`n`, literal | needs `~25000×` prefactor | none (constant) | **disfavored** (parent §A.4, confirmed here) |
| `1/√n` | finite-`n`, literal | needs `~99×` prefactor | none (constant) | **disfavored** (parent §A.4, confirmed here) |
| `(c/n)^(1/2)=√(c/n)` | finite-`n`, literal | needs `~3.1-3.3×` prefactor | none (constant) | **disfavored** (parent §A.4; "most generous of the 3 originally tested," still a real unexplained factor) |
| `(c/n)^(1/3)` | finite-`n`, power law | needs `~1.56-1.65×` prefactor | **zero, by construction (§2.1)** | **disfavored** (this front, new) |
| `(c/n)^(1/4)` | finite-`n`, power law (N1 target) | needs `~1.10-1.16×` prefactor (closest magnitude match of any candidate tested to date) | **zero, by construction (§2.1)** | **does not close** (magnitude-closest, but no shape content and `3pp` closure bar failed at `4.42pp`; §3's `p*`-drift argument suggests coincidence) |
| `(c/n)^(1/5)` | finite-`n`, power law | needs `~0.89-0.94×` prefactor (comparably close to `1/4`, opposite side) | **zero, by construction (§2.1)** | **does not close** (comparably magnitude-close to `1/4`; undermines `1/4`'s specialness, §2.2) |
| `n_eff(t0)=n(1-t0)` boundary variant, `p=1/4` | finite-`n`, `t0`-dependent (exploratory) | fitted `A≈0.82`, but `R²=-13.6` | present, but **wrong sign/shape** (blows up near `t0→1`, data doesn't) | **disfavored** (this front §4, corroborates parent §A.3) |
| `s+g≤1` boundary (H-boundary) | structural | — (qualitative) | predicts growth near `t0→1`; data roughly flat | **weakened as primary driver** (parent §A.3, not re-derived here; independently corroborated by this front's §4) |
| generic vanishing finite-`n` (H-finite-n) | structural | needs an unidentified large prefactor at any of the naturally-small rates checked (`1/n`,`1/√n`,`√(c/n)`) — and now also at `(c/n)^{1/3,1/4,1/5}` for the SHAPE (§2.1), though `1/4,1/5` come close for the LEVEL alone | mixed | **weakened as primary driver, more completely than before**: the parent's own §A.4 already disfavored 3 rates; this front extends that to the two rates the referee itself flagged as untested, on BOTH magnitude (does not clear the `3pp` closure bar) AND — newly established — shape (zero capacity by construction) |

**No candidate in this table achieves closure.** The overall
"simple-power-law-in-`(c/n)`" class, taken as a family (any fixed
exponent, at the single measured `(c,n)` cell), is **eliminated as a
shape explanation** rigorously (§2.1) and **falls short of the stated
magnitude closure bar** for every exponent tested (§2.3), even though
`(c/n)^{1/4}` (and, comparably, `(c/n)^{1/5}`) remain the closest
magnitude matches among everything tried to date in this lineage.

---

## 6. Search for a second `(c,n)` calibration point (none found)

Because §3's argument turns on this being a single-point calibration, a
search was made for any OTHER place in this archive's M-CLUST(b) lineage
where the abstract-vs-real plateau gap (or an analogous quantity) was
measured at a DIFFERENT `(c,n)` pair, which would allow the exponent `p`
to be genuinely fit (2+ points constrain both `p` and `A` non-trivially)
rather than merely calibrated to reproduce one number:

```
grep -rln "n=65536\|65536" --include="ATTEMPT.md" \
  05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/
```

This confirms `n=65536` (and `c=1000`) is the record's single fixed
target cell for the M-CLUST(1) real-engine measurements feeding this
specific gap statistic throughout the whole lineage — no second
`(c,n,gap)` triple for the SAME plateau-gap quantity exists anywhere in
the archive to date. (Other fronts in this lineage use different `n`
values for unrelated statistics — e.g. `elevation_level_attempt`'s
`n=131072` cells, `short_cycle_dynamics_attempt`'s `n≈50k-800k` per-cell
counts — but none of these measure the abstract-vs-real PLATEAU gap
`Φ(0,t0)` vs. `φ(ell)` at a second `(c,n)`; they are different
statistics entirely, not usable here without a substantial new
measurement campaign, which is out of this front's "fast and cheap,
fit against existing data" scope.) **This is named as the single most
concrete next step for a future front wanting to move past a magnitude-
only comparison**: a second real-engine measurement at a different `n`
(e.g. `n=16384` or `n=262144`, holding `c=1000` fixed) together with the
abstract plateau constant at the same `c` (already computable to
arbitrary precision, no new theory needed — reuse
`mclust_plateau_abstract_real_gap_attempt/g01_family_series.py`'s
recursion) would let `p` actually be fit rather than merely tried at
three guesses. **Sketched, not executed, per this front's "fast and
cheap" scope** — the same honest-disclosure convention as the parent
front's own §A.5.

---

## 7. What did NOT close, precisely

1. **The gap's true source remains unidentified.** This front narrows the
   candidate space (rules out the entire fixed-`(c,n)` power-law class as
   a shape explanation, rigorously; further disfavors `1/3`, weakens
   `1/4`/`1/5`'s apparent magnitude edge via the `p*`-drift argument; rules
   out one natural `t0`-dependent boundary-based generalization) but
   proposes no replacement mechanism.
2. **No candidate reaches the `3pp` closure bar** (§1, §2.3) on either
   bin table, even under the most generous (best-fit) prefactor
   evaluation.
3. **The magnitude-only "closeness" of `(c/n)^{1/4}`** (and, comparably,
   `(c/n)^{1/5}`) to the observed mean gap is REAL (confirmed, not
   disputed) but is argued here (§3) to be more consistent with a
   single-point coincidence than a genuine rate law, because (i) the
   exact unit-prefactor exponent `p*` is a generic, non-simple number
   that (ii) drifts between the two available bin tables of the same
   quantity. This is an ARGUMENT, not a proof of coincidence — a second
   independent `(c,n)` measurement (§6) is the concrete way to settle it,
   not attempted here.
4. **T1 vs. T2-composite shape disagreement** (already disclosed by the
   parent front, §A.2) is untouched by this front — both tables were
   used, side by side, exactly as the parent front left them.
5. **The exploratory `n_eff(t0)` extension (§4) is not itself proposed as
   a serious candidate** — it was tried cheaply, decisively failed
   (strongly negative `R²`), and is reported as a negative result and as
   corroboration of the parent's own boundary-hypothesis skepticism, not
   as a new mechanism.
6. **H1, H2, the plateau resummation closed form, and every open item
   from the parent front's own §"What remains open"** are entirely
   untouched — this front's scope was strictly the rate-candidate
   question named by DISC-DEC-118(d).

---

## 8. Scorecard

| item | outcome |
|---|---|
| `(c/n)^{1/4}` tested against bin data (mandate's central ask) | **Done. Does not close** (§2.3: max resid `4.42pp` on T2-composite, `14.13pp` on T1, vs. `3pp` bar); closest magnitude match among all candidates tried to date (`1.10×` prefactor) |
| `(c/n)^{1/3}`, `(c/n)^{1/5}` tested (exhaustion of neighbors) | **Done.** `1/3` clearly worse (`1.56×`); `1/5` comparably close to `1/4` (`0.895×`), undermining `1/4`'s apparent specialness |
| Whether prefactor is consistent across bins/`t0` or drifts | **Answered rigorously**: the model has NO capacity to vary by bin (§2.1) — the "prefactor" implied per-bin (`gap_i/rate`) necessarily mirrors `gap_i`'s own spread exactly (`19.1%` relative spread on T2-composite, `55.2%` on T1; `r03_perbin_and_exploratory.py` Part A) |
| Whether shape of `t0`-dependence is well-matched or coincidental | **Answered: cannot be matched at all, by construction** (§2.1) — any apparent match is necessarily magnitude-only |
| Comparative table incl. previously-tried/weakened candidates | **Done** (§5) |
| Precision bar stated up front | **Done** (§1), applied without post-hoc adjustment |
| Full predicted-vs-observed residual tables | **Done** (§2.2 tables; per-bin detail in `r02_power_law_fit.log`, `r03_perbin_and_exploratory.log`) |
| Cross-check of transcribed data against parent's own numbers | **Done** (`r01_reconstruct_and_crosscheck.py`; max discrepancy `0.0049pp`, pure `Decimal`-vs-published-rounding, both tables) |
| Outcome tier | **(b) elimination of the power-law-in-`(c/n)` CLASS as a shape explanation (rigorous) + (c) sharper diagnosis of the magnitude-only near-miss (not closure)** |
| Millennium Problem claims | **None. Not applicable — this is M-CLUST(b), Tree B, unrelated to `THEOREM.md`'s Tree A line.** |

---

## Seeds

**None used.** Reserved range `20260932000-20260932999` (this front, wave
25(d) per `DISC-DEC-118`) was grep-confirmed unused before first use:

```
$ grep -rn "20260932" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:...(reservation line)
05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md:...(block-summary line)
```
— only the ledger reservation and state-summary lines, exactly as
expected before a front's first use. As anticipated in the mandate,
this front turned out to be pure numerical fitting against already-vetted
existing bin data (transcribed and cross-checked, §0/§2.1), so no Monte
Carlo or other random sampling was needed anywhere; the reserved range
remains entirely unused at the end of this front, exactly like the
parent front's own `20260886000-999` range.

---

## Scope-discipline confirmation

- All work confined to this front's own new subdirectory
  (`.../mclust_plateau_abstract_real_gap_attempt/gap_rate_candidate_attempt/`).
- The parent front (`mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md`
  and its own scripts/`adversarial/`) and the sibling
  `mclust_h1_validity_attempt/` subdirectory were read-only references;
  neither was modified.
- `THEOREM.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`,
  `PROOF_DEPENDENCY_MAP.md`, `README.md`, `index.html`: none opened for
  writing, none modified — integration into these is a separate step per
  the mandate.
- No git command was run.
- No `adversarial/` subdirectory created and no referee dispatched by
  this front itself (consistent with the mandate's scope — that is a
  separate orchestration step).
- No claim of progress on any Millennium Prize Problem appears anywhere
  in this document; this is pure combinatorial mathematics on the
  M-CLUST(b) plateau mechanism (Tree B), independent of `THEOREM.md`'s
  Tree A (u₁/₂) line.

---

## Files

| file | role |
|---|---|
| `r01_reconstruct_and_crosscheck.py` / `.log` | transcribes T1/T2-composite bin data + `Pi(1000)` from the parent front's own published tables; recomputes every `gap%` from scratch and confirms it matches the parent's published numbers to `<0.005pp` (transcription cross-check, §0) |
| `r02_power_law_fit.py` / `.log`, `r02_fit_results.json` | core candidate test: computes `(c/n)^p` for `p∈{1/2,1/3,1/4,1/5}` plus `1/n`,`1/√n`; fits prefactors; demonstrates the shape-blindness degeneracy (§2.1) numerically; solves for the exact unit-prefactor exponent `p*` (§3) |
| `r03_perbin_and_exploratory.py` / `.log`, `r03_results.json` | Part A: per-bin implied-prefactor table (mandate's "consistent or drifts" question, §2.1/§8); Part B: exploratory `n_eff(t0)=n(1-t0)` `t0`-dependent generalization, decisively rejected (§4) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`gap_rate_candidate_attempt/` subdirectory was written to.
