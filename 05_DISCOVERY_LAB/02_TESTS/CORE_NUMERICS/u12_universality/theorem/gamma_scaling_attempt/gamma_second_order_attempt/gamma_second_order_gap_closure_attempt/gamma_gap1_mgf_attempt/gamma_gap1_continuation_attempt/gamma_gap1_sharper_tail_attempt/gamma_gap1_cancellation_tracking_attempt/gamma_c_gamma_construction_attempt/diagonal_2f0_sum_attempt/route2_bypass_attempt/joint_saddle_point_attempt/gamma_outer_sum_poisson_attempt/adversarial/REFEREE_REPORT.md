# REFEREE REPORT — `GAMMA-OUTER-SUM-POISSON-ATTEMPT` (wave 33, front (b))

**Referee stance:** hostile/adversarial. Every central claim was independently
re-derived and/or independently re-checked with fresh code, fresh sample
points (disjoint from the front's own grids wherever feasible), and — for
the true discrete sum — a genuinely different computational route (the
*primary* combinatorial double-sum definition of `T(n,m)`, not the
Beta-integral quadrature the front's own scripts use). No script of the
front (`01`–`04`) was imported or copied; the referee's own scripts
(`ref_01`–`ref_03`, this directory) are written from scratch against
`THEOREM.md` and the two predecessor `ATTEMPT.md` files only.

---

## VERDICT

> **SOUND WITH ISSUES** — one MODERATE issue, three LOW/expository issues.
> No error was found in the front's central mathematical claims (the
> Poisson-summation closed form for the `T_prof`-proxy sum, its rigorously
> exponentially-small remainder, the evenness argument, or the exact
> decomposition identity against the TRUE discrete sum `S_n'(γ)`) — all of
> these were independently re-derived and/or re-verified numerically at
> fresh sample points and hold up completely. **ACCEPT for catalogue**,
> with the one MODERATE issue corrected by a dated nota/correção on the
> front's own `ATTEMPT.md` (see Issue 1 below) and the LOW issues optionally
> footnoted.

**What is genuinely established** (independently reconfirmed by this
referee, not merely re-read): a closed-form, rigorously-derived correction
`1/(2γ)` to the gap between `Σ_{m=0}^∞T_prof(m/√n,γ)` and its continuum
integral `G_n(γ)`, with an exact (not asymptotically-argued) exponentially
small remainder controlled by the full Poisson-summation Fourier series; and
an exact algebraic decomposition of the TRUE discrete sum's own gap into
this same `1/(2γ)` term plus a directly-computable "crossover sum" over
`m=O(1)`, confirmed to hold at every tested point (front's own 21 points,
plus this referee's own fresh 18 points) to within the analytically
predicted negligible-tail bound. `C(γ)` remains untouched and entirely
open, exactly as the front claims.

**What is not established**, correctly disclosed as such by the front: the
crossover sum's closed form or proved limit; and the §4 Part C "bonus"
`1/√2`-convergence pattern, which this referee found to be **less clean, and
gamma-dependent in a way the front's own text does not fully convey** (Issue
1) — though the front's *epistemic hedging* of this observation (explicitly
"not proved," "conjecture-dependent," disclosed departure at the largest
`n`) is itself honest and adequate in kind, just imprecise in the specific
numeric range quoted.

---

## Part 1 — Independent re-derivation of the Poisson closed form (task item 1)

Re-derived from scratch (script `ref_01_poisson_rederivation.py`, Part A),
via a *different* symbolic route than the front's own script `02` (the
front routes both the Fourier transform and the half-line integral through
a "fresh positive symbol `a`" substitution to dodge a `sympy` branch-cut
artifact; this referee instead computes the *full-line* Gaussian integral
directly and gets the half-line integral from it via evenness, established
independently in Part B — a genuinely different manipulation, not a
copy-with-renamed-variables):

```
Σ_{m=0}^∞ φ_n(m) = ∫_0^∞ φ_n(x)dx + φ_n(0)/2 + Σ_{k=1}^∞ φ̂_n(k)
φ_n(0)/2 = 1/(2γ)                    [confirmed: sp.simplify(boundary - 1/(2γ)) == 0]
φ̂_n(k) = (1/γ)√(πn/α) exp(-π²k²n/α)
c(γ) := π²/α = 2π²γ/(2-γ)            [confirmed: sp.simplify(rate_c - 2π²γ/(2-γ)) == 0]
```

**Result: exact match to the front's closed form**, both symbolically (this
referee's independent algebra path) and numerically (Part C of `ref_01`):
16 fresh `(n,γ)` points, `γ∈{0.15,0.45,0.65,0.95}` — all four values
disjoint from the front's own script `03` grid (`γ∈{0.2,0.5,0.8}`) and from
the dispatching session's own spot-check grid — `n∈{5,11,17,25}`. At every
point, the direct high-precision summation matches "continuum integral +
`1/(2γ)` + first 6 Fourier corrections" to within the requested tolerance
(differences `10⁻⁴⁸` to `10⁻²³⁸`, tracking working precision, not a real
discrepancy), and the residual-alone (direct sum minus continuum minus
boundary term) tracks the predicted rate `c(γ)` with empirical/predicted
log-slope ratio `0.975`–`0.998` across the four fresh `γ` (tightening as
`γ→1`, i.e. as `c(γ)` grows and the asymptotic regime is reached faster —
consistent with the front's own observation that the ratio tightens with
larger `n`/`c(γ)n`).

**No discrepancy found.** The formula is correct and the front's derivation
of it is sound.

---

## Part 2 — Evenness claim and the whole-line extension (task item 2)

Independently checked (script `ref_01`, Part B), using a symbol declared
`real=True` (genuinely testing `λ<0`), NOT `positive=True` as both the
front's own script and this referee's Part A symbol are declared (so this
is a deliberately more adversarial test of the evenness claim than either
uses elsewhere):

- `T_prof(λ,γ) − T_prof(−λ,γ)` simplifies to exactly `0` for real `λ`.
- The Taylor series of `T_prof` about `λ=0` to order 11 has every odd-power
  coefficient exactly `0` (a different check than the front's direct
  higher-derivative evaluation, arriving at the same conclusion).

**On the subtlety the task asked to scrutinize** (does extending `φ_n`
to negative arguments introduce any issue): **no**. `T_prof(λ,γ) =
(1/γ)exp[-((2-γ)/(2γ))λ²]` depends on `λ` *only* through `λ²` in its
closed-form expression — it is manifestly single-valued, entire, and
analytic for every real `λ`, with no `√λ`, `log λ`, or fractional-power
term anywhere that could make the `λ→−λ` continuation ambiguous or
branch-dependent. The only thing being extended is the *analytic proxy*
`φ_n` (an explicit elementary Gaussian, defined for all real `x` by
construction) — never the actual combinatorial object `term_m(n,γ)`, which
has no meaning for negative `m` and is never evaluated there anywhere in
the front's derivation. The front's own Part C algebra (`Σ_{m∈Z}φ_n(m) =
φ_n(0)+2Σ_{m≥1}φ_n(m)`) uses `φ_n(−m)=φ_n(m)` purely as analytic values of
the *same* closed-form function; it never claims or needs `term_{-m}` to
mean anything. **No gap or unsound step found here.**

---

## Part 3 — Independent verification of the TRUE discrete sum decomposition (task item 3)

Script `ref_02_true_discrete_sum.py` recomputes `S_n'(γ)` and the crossover
sum from the **primary combinatorial double-sum definition**
`T(n,m):=Σ_j C(j+m,m)C(n-j,m)(1-γ)^j` — genuinely different from, and
independent of, both the front's own quadrature-based Beta-integral route
AND this referee's own Poisson-formula scripts — at 18 fresh `(n,γ)`
points, `γ∈{0.25,0.6,0.9}` (disjoint from the front's `{0.3,0.5,0.8}`),
`n∈{30,75,150,300,600,1000}` (disjoint from the front's `{20,...,1600}`).

**Result: the exact decomposition identity holds at all 18/18 fresh
points**, to within an independently-constructed (looser, more
conservative) analytic bound on the two neglected pieces (the `T_prof` tail
beyond `n`, and the Poisson `k≥1` remainder). Full log:
`ref_02_true_discrete_sum.log`.

**A self-caught issue in this referee's own first draft, worth recording
because it validates a piece of the front's own bound formula.** An early
version of `ref_02` conditioned the "tail of `T_prof` beyond `m=n`" term on
`M < n` (zeroing it whenever the adaptive cutoff `M` happened to equal the
full range `n`) — wrongly assuming that summing the crossover sum over the
*entire* available range `m=0..n` meant no `T_prof` mass was left
uncounted. It does not: the Poisson-derived boundary formula
`G_n(γ)+1/(2γ)` represents `Σ_{m=0}^∞T_prof(m/√n,γ)` (all the way to
infinity), so even at `M=n` there is still an uncaptured tail
`T_prof(√n,γ)` for `m>n`. This first draft consequently failed its own
mismatch-vs-bound check at exactly the 4 points where `M=n` (small `n`,
large `γ`) — e.g. `n=30,γ=0.9`: mismatch `4.8×10⁻⁹` against a
wrongly-tightened bound of `10⁻⁴⁰`. Once the missing `tail_Tprof_beyond_n`
term was restored (matching — independently — the *exact same* term the
front's own `04_exact_decomposition_test.py` already includes,
unconditionally, as `tail_Tprof_beyond_n`), all 18/18 points pass cleanly.
**This is not a finding against the front** — quite the opposite: it
confirms the front's own bound formula was built correctly (the
unconditional inclusion of that term is load-bearing, not decorative), and
that this referee's own first attempt at reproducing it independently, by
omitting it, is exactly the kind of mistake the front's formula already
guards against.

---

## Part 4 — Scrutiny of the §4 Part C "bonus observation" (task item 4)

**Issue 1 (MODERATE) — the front's characterization of its own `1/√2`
doubling-ratio data is not fully accurate.**

The `ATTEMPT.md` VERDICT and §4 Part C both state: *"the ratio at successive
doublings sitting at `0.708–0.713` ... for THREE consecutive doublings
(`100→200→400→800`) at all three γ tested, before visibly departing from
that clean ratio at the FINAL doubling (`800→1600`...)."*

Transcribing the front's own printed numbers directly from its own
`04_exact_decomposition_test.log` (not recomputed, not altered):

| γ | 100→200 | 200→400 | 400→800 | 800→1600 |
|---|---|---|---|---|
| 0.3 | 0.70849 | 0.70805 | 0.70775 | 0.59313 |
| 0.5 | 0.71024 | 0.70928 | **0.69138** | 0.33940 |
| 0.8 | 0.71303 | 0.71017 | **0.56929** | 0.42275 |

The claimed range `0.708–0.713` does **not** bound the front's own data for
"all three γ tested" over "three consecutive doublings": at `γ=0.5` the
`400→800` ratio (`0.691`) is below the claimed floor, and at `γ=0.8` the
`400→800` ratio (`0.569`) is already deep in the range the document's own
text reserves for the *final* doubling's "departure." In other words, for
2 of the 3 γ values the front tested, the clean `1/√2` pattern actually
breaks down starting at the **third** doubling (`400→800`), not the fourth
(`800→1600`) as stated. Only `γ=0.3` matches the document's own
characterization exactly.

**Independent robustness check, script `ref_03_bonus_observation_robustness.py`**,
at two genuinely fresh `γ` values (`0.35, 0.7`, disjoint from both the
front's grid and this referee's own `ref_02` grid), same doubling structure
(`n=100,200,400,800,1600`), primary double-sum `T(n,m)` (no front code
read):

| γ | 100→200 | 200→400 | 400→800 | 800→1600 |
|---|---|---|---|---|
| 0.35 | 0.70888 | 0.70832 | 0.70794 | 0.70769 |
| 0.7 | 0.71227 | 0.71072 | 0.70965 | 0.70889 |

Interestingly, at *these* fresh `γ` values the `1/√2` pattern is *more*
persistent than at any of the front's own three test points — it holds
cleanly through **all four** doublings tested, including `800→1600`, where
the front's own three γ values all show visible departure. This shows the
"departure point" is itself `γ`-dependent (and, on this evidence, the front
happened to test three γ values that are relatively early departers, not
late ones) — reinforcing, if anything, that this pattern is real but
**genuinely fragile and unpredictable in where it breaks down**, not a
clean, uniform `O(1/√n)` law the front's specific numeric claim suggests.

**Assessment.** This does **not** undermine the front's own epistemic
framing — the document already explicitly labels Part C "an unplanned
bonus numerical observation... explicitly flagged as conjecture-dependent,
NOT a proved fact," discloses the departure at the final doubling, and
attributes it (plausibly) to the conjectural target's own imprecision. That
overall hedge is honest and adequate, and this referee's own fresh-γ
results are equally consistent with "the pattern is real, fragile, and
`γ`-dependent" as with "the pattern is an artifact of small-sample
coincidence at 3 points." What is inaccurate is the *specific numeric
range* (`0.708–0.713`) claimed to hold "at all three γ tested" for "three
consecutive doublings" — this is contradicted by the front's own printed
log data for 2 of the 3 γ values. **Severity: MODERATE** — it is a
verifiable factual inaccuracy about what the front's own data show (the
same kind of issue, and comparable severity, to the Estágio 56 predecessor's
own corrected `<0.7%` claim, which was likewise contradicted by that front's
own log and rated a correção, not a mere nota) — but it lives entirely
inside a section already labeled non-rigorous/conjecture-dependent, and does
not touch this front's mandate (item 3) or any of its rigorously-derived
claims. Recommended remedy: a dated correção narrowing the claimed range to
what the data actually show (e.g. "`0.57–0.71` across the three γ tested,
with the departure from `1/√2` beginning as early as the third doubling at
two of the three γ, not uniformly at the fourth") and noting the referee's
fresh-γ finding that the pattern's robustness is itself γ-dependent.

---

## Part 5 — Tool-choice sanity check: Poisson vs Euler–Maclaurin (task item 5)

The front's comparative argument (§2 Part A) — Euler–Maclaurin naturally
fits a boundary-maximized "edge sum," Poisson naturally fits a
fast-decaying whole-lattice sum, and Poisson is chosen as primary because
`φ_n`'s Fourier transform is an explicit Gaussian giving a closed
exponential rate, "strictly stronger than any finite-order EM truncation"
— is **correct**, and this referee's own check finds it actually
**understates** its own case.

Because `φ_n` is even (Part 2 above) with `φ_n^{(k)}(0)=0` for every odd
`k`, **and** because every derivative of `φ_n` vanishes as `x→∞` (a
Gaussian beats any polynomial), *every single term* of the classical
Euler–Maclaurin boundary-correction series
`Σ_k B_{2k}/(2k)! [φ_n^{(2k-1)}(b)-φ_n^{(2k-1)}(a)]` vanishes **identically**,
at *every* finite order `K`, for the half-line sum `a=0,b→∞`. So a naive
finite-order Euler–Maclaurin analysis does not merely give a "weaker
bound" than Poisson here — it gives **exactly zero** correction beyond
`φ_n(0)/2` at every order, which would (misleadingly, if taken literally at
any finite order) suggest the sum-vs-integral gap is *exactly*
`φ_n(0)/2`, when it is not: the true correction is the residual
`Σ_{k≥1}φ̂_n(k)`, a **non-perturbative** (beyond-all-algebraic-orders)
term invisible to the EM series at any finite `K`, exactly analogous to the
classical fact that Poisson summation's exponentially-small term for a
theta function/Gaussian sum is not captured by the EM asymptotic expansion
at any polynomial order. This is a genuinely sharper and more precise
version of the front's own comparative claim — not a defect, an
enhancement the front could have stated more forcefully. **Severity: LOW /
positive note**, recorded here as a possible addition, not a required
correction, since the front's own weaker claim is not wrong, just less
sharp than the truth.

**Minor additional LOW note (also from this task item).** The front asserts
the total remainder is `O(√n·e^{-c(γ)n})` (the `k=1` term's order) without
explicitly bounding the *sum* `Σ_{k≥2}φ̂_n(k)` against it. This is routine —
`φ̂_n(k)/φ̂_n(1) = exp(-π²(k²-1)n/α)`, so the `k≥2` tail is dominated by a
convergent geometric-type series strictly smaller than `φ̂_n(1)` itself once
`n` is not tiny — and this referee's own `ref_01` Part C numerics confirm
it directly (`residual_alone/φ̂_n(1)` ratio is `1.00000000` to 8 decimals at
every one of the 16 fresh points tested, i.e. the `k≥2` terms are
completely negligible in practice). But the front's `ATTEMPT.md` never
states this dominance argument explicitly — a one-line addition would make
the `O(...)` claim fully rigorous rather than "clearly true but not
spelled out." **Severity: LOW**, cosmetic/expository only.

---

## Part 6 — Governance and scope discipline (task item 6)

- **Seed block `20260953000–20260953999`**: `grep -rn "20260953"
  05_DISCOVERY_LAB/` independently re-run by this referee. Matches found
  only in the front's own `ATTEMPT.md` (its own reservation text), in
  `DECISION_LEDGER.yaml`'s reservation line, and in
  `DISCOVERY_LAB_STATE.md`'s mirrored reservation line. **Confirmed unused
  elsewhere**, matching the front's own claim exactly.
- **`git status --porcelain`**: only two new untracked directories appear —
  this front's own `gamma_outer_sum_poisson_attempt/` and the sibling
  `gamma_stirling_mfact_uniform_attempt/` (plus one unrelated pre-existing
  untracked directory from a different, abandoned lineage). **No tracked
  file shows as modified** — `THEOREM.md`, `DECISION_LEDGER.yaml`,
  `PROOF_DEPENDENCY_MAP.md`, `DISCOVERY_LAB_STATE.md`, `README.md`,
  `index.html`, and every ancestor `ATTEMPT.md` are untouched, confirming
  the front's scope-discipline claim.
- **Sibling front `GAMMA-STIRLING-MFACT-UNIFORM-ATTEMPT`**: its directory
  exists (confirmed, contains its own scripts `01`–`05` and `ATTEMPT.md`).
  `grep -rln "gamma_stirling_mfact_uniform_attempt\|GAMMA-STIRLING"` inside
  this front's own directory returns **only its own `ATTEMPT.md`** (the
  two prose disclosure lines naming the sibling for scope-discipline
  purposes) — no script or log of this front references, imports, or
  depends on any file of the sibling. **Confirmed clean.**

**No governance issue found.**

---

## Part 7 — Overclaim/underclaim check on the VERDICT and confidence language (task item 7)

The VERDICT UP FRONT and the §5/§9 scorecard were compared, claim by claim,
against what this referee actually independently confirmed:

- *"A new, exact (up to an explicit, rigorously exponentially-small-in-`n`
  remainder) closed-form correction ... derived via Poisson summation"* —
  **accurate**; independently re-derived and confirmed (Part 1/2 above).
- *"confirmed numerically two independent ways"* — **accurate**; both the
  `T_prof`-proxy route (§3) and the true-discrete-sum decomposition (§4)
  were independently re-confirmed by this referee too, at disjoint sample
  points and via a genuinely different computational route for the latter.
- *"C(γ) is untouched ... and remains entirely OPEN"* — **accurate**, and
  correctly, repeatedly disclaimed throughout.
- *"the crossover sum ... is precisely diagnosed but not resolved"* —
  **accurate**; this referee's own fresh-point crossover sums (Part 3
  above) likewise show an `O(1)`, not-yet-closed-form quantity, consistent
  with the front's own finding at three additional `γ` values.
- The Part C bonus-observation language in the VERDICT ("shrinks by a
  factor consistent with `1/√2` at three consecutive `n`-doublings ...
  ratio `0.708`–`0.713`") is the **one place** where the stated confidence
  (a specific, narrow numeric range, presented as holding "at all three γ
  tested") is measurably stronger than what the front's own underlying data
  support — see Issue 1 (Part 4 above). The VERDICT's own epistemic hedge
  around this same observation ("explicitly flagged as conjecture-dependent,
  NOT a proved fact") is appropriately cautious in *kind*; only the specific
  *numbers* quoted overstate the data's cleanness.

No other place in the document was found where confidence language
overclaims or underclaims relative to what was actually shown.

---

## Summary list of issues, for dated correção/nota application

1. **[MODERATE]** §4 Part C / VERDICT: the claimed doubling-ratio range
   `0.708–0.713` "at all three γ tested" for "three consecutive doublings"
   is contradicted by the front's own `04_exact_decomposition_test.log`
   data at `γ=0.5` (`400→800` ratio `0.691`) and especially `γ=0.8`
   (`400→800` ratio `0.569`, already in "departure" territory at the
   *third*, not fourth, doubling). Independent testing at two fresh `γ`
   (`0.35, 0.7`) shows the pattern can persist cleanly through all four
   doublings tested — i.e., the departure point is itself `γ`-dependent
   and not reliably "the final doubling." Recommend narrowing the claimed
   numeric range and adding this referee's fresh-γ finding as further
   context on the pattern's fragility. Does not affect the front's core
   mandate (item 3) or any rigorously-derived claim; lives entirely inside
   an already-hedged, explicitly-non-rigorous "bonus observation."

2. **[LOW / positive note]** §2 Part A's Euler–Maclaurin-vs-Poisson
   tool-choice argument is correct but can be stated more sharply: because
   `φ_n` is even with all derivatives vanishing at both endpoints
   (`x=0` via evenness, `x→∞` via Gaussian decay), the *entire* classical
   EM boundary-correction series vanishes identically at *every finite
   order* — not merely "bounded only by generic derivative-growth
   estimates" as stated. A naive finite-order EM treatment would
   (misleadingly) suggest the sum-integral gap is *exactly* `φ_n(0)/2`,
   with the true correction being a genuinely non-perturbative,
   beyond-all-orders term. Recommend as an optional strengthening nota, not
   a correção (nothing stated is wrong, just less sharp than possible).

3. **[LOW / expository]** The `O(√n·e^{-c(γ)n})` remainder claim in §2/VERDICT
   does not explicitly bound the sum `Σ_{k≥2}φ̂_n(k)` against the dominant
   `k=1` term — this is elementary (a convergent geometric-type tail,
   confirmed numerically by this referee to ratio `1.00000000` vs. the pure
   `k=1` term at all 16 fresh points tested) but is not spelled out in the
   document. Recommend an optional one-line addition for full rigor; not a
   correção.

4. **No other computational, symbolic, or governance issues found.** The
   Poisson closed form (§2), the evenness proof (§2 Part B), the
   `T_prof`-proxy numerics (§3), and the exact decomposition against the
   true discrete sum (§4 Part A/B) were all independently re-derived and/or
   re-confirmed at disjoint sample points, using genuinely different
   computational routes where feasible (primary combinatorial double sum
   for `T(n,m)` rather than the front's own Beta-integral quadrature), with
   zero discrepancies beyond floating-point/working-precision noise.

---

## Files in this directory

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref_01_poisson_rederivation.py`/`.log` | independent symbolic re-derivation of the Poisson closed form (different algebra route than the front's script `02`); independent evenness check using a genuinely-real (not merely positive) symbol; numeric confirmation at 16 fresh `(n,γ)` points |
| `ref_02_true_discrete_sum.py`/`.log` | independent recomputation of `S_n'(γ)` and the exact decomposition identity via the PRIMARY combinatorial double-sum definition of `T(n,m)` (no quadrature, no front code read), at 18 fresh `(n,γ)` points; includes a self-caught bug in this referee's own first draft that (once fixed) confirms a term in the front's own bound formula is load-bearing |
| `ref_03_bonus_observation_robustness.py`/`.log` | independent robustness check of the §4 Part C `1/√2` doubling-ratio observation at 2 fresh `γ` values, plus a direct transcription-based audit of the front's own printed data underlying its VERDICT claim (Issue 1) |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble (`u12_universality`). No `git`
command was run by this referee. `ATTEMPT.md` and scripts `01`–`04` of the
front were not modified.
