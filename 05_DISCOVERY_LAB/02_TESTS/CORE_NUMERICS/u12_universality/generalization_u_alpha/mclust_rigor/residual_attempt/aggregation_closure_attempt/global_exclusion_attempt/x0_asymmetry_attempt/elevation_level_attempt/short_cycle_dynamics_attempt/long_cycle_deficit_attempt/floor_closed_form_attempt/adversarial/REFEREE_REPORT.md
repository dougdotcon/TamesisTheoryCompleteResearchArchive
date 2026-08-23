# REFEREE REPORT — adversarial review of `floor_closed_form_attempt/ATTEMPT.md`

**Wave 14, `DISC-DEC-057`, front (b) `FLOOR-CLOSED-FORM-ATTEMPT`, mandatory
independent adversarial verification.**

Object under test: `floor_closed_form_attempt/ATTEMPT.md` together with its
`DERIVATION_PREREG.md`. Both were read in full, together with
`long_cycle_deficit_attempt/ATTEMPT.md` and its
`adversarial/REFEREE_REPORT.md` (background/citation context), and
`sc_engine.py`/`sc_formula.py` (parent lineage, already-adversarially-
verified infrastructure), before any line of this review's own code was
written.

**Independence / discipline.** None of this front's own scripts
(`fcd_t0.py`, `fcd_t1.py`, `fcd_t2.py`, `fcd_t2_cluster.py`, `fcd_t3.py`,
`derive_closed_form.py`, `check_formula_heuristic.py`, `solve_2d_system.py`,
`abstract_sim.py`, `explore_phiL.py`, `explore_ndep.py`) were read, opened,
or imported at any point in this review. All measurement code
(`ref_common.py`, `ref_mp_worker.py`, `ref_identity_check.py`,
`ref_t1_candidate1.py`, `ref_t2_finebinning.py`, `ref_t3_abstract.py`, all
in this `adversarial/` subdirectory) was written from scratch against
`sc_engine.py`'s API and the *prose* of `ATTEMPT.md`/the review mandate
only. `git status --porcelain` at review end shows exactly one untracked
path, `floor_closed_form_attempt/` (this front's own subtree, which
`ATTEMPT.md` itself discloses was never committed) — no tracked file
anywhere in the repository is modified. **No git commit was made.**
`ATTEMPT.md`, `THEOREM.md`, and all governance files were read-only.

**Fresh seeds**, all from `SeedSequence(20260834000)`–`(20260834004)`,
the range `DECISION_LEDGER.yaml` (`DISC-DEC-057`) reserves for *this
front's referee* — confirmed unused anywhere in the archive by
`grep -rn "20260834"` before use (only the ledger's own reservation line
and `DERIVATION_PREREG.md`'s own "not used by this front" disclaimer
matched):

| seed | use | N | script | log |
|---|---|---|---|---|
| `SeedSequence(20260834000)` | identity/Fact-A sanity re-check (T0-analogue) | 400 (+20 for the `R_mask` check) | `ref_identity_check.py` | `ref_identity_check.log` |
| `SeedSequence(20260834001)` | T1 replication: Candidate-1 rejection | 8000 | `ref_t1_candidate1.py` | `ref_t1_candidate1.log` |
| `SeedSequence(20260834002)` | T2 replication, run A: fine-bin cluster-robust | 15000 | `ref_t2_finebinning.py A` | `ref_t2_runA.log` |
| `SeedSequence(20260834003)` | T2 replication, run B: independent re-seed | 15000 | `ref_t2_finebinning.py B` | `ref_t2_runB.log` |
| `SeedSequence(20260834004)` | T3 replication: abstract recursive-process | 200000 per `t0` (6 `t0` values) | `ref_t3_abstract.py` | `ref_t3_abstract.log` |

All `N`s are **≥5× the front's own N** at every corresponding test (T1:
5.3×, T2 per-run: 5×, T3: 5×), plus T2 is run **twice**, independently
seeded, specifically to stress-test cross-run replication — the exact axis
on which the front caught its own instability.

---

## 0. VERDICT — **SOUND WITH NAMED ISSUES**. ACCEPT for catalogue.

Every load-bearing claim in `ATTEMPT.md` that this review's mandate assigned
for independent empirical re-verification — T1's Candidate-1 rejection, T3's
abstract-process plateau (built from the prose description alone, not from
`fcd_t3.py`), and T2/T2b's central empirical question ("is there ANY
significant positive sub-region in the far tail, or is 'negative throughout,
`−1%` to `−5%`, no resolved finer structure' the honest summary?") —
**independently replicates**, at higher power, with fresh seeds, from
scratch. I found:

1. **One genuine bug in my OWN code**, caught by internal cross-checking
   before it reached any reported number (§3 below) — disclosed in full,
   not swept under the rug, precisely because this document's own T0/T2b
   self-corrections set that standard.
2. **One real, if minor, imprecision in `ATTEMPT.md` §7's synthesis**: the
   claim of "cross-run agreement (for 7 of 9 T2 bins)" overstates what
   T2/T2b's own internal comparison actually demonstrates (§5 below) — a
   wording issue, not a numerical error, and one that this review's own
   independent T2/T2b replication (§4) now actually *substantiates* for the
   first time across all 9 bins.
3. **No error that changes the front's central verdict.** The "HONEST
   PARTIAL CLOSURE" framing holds up under independent scrutiny — if
   anything, my replication shows the front's post-withdrawal caution was
   *appropriately conservative*, not excessive: the coarse "negative
   throughout, `−1%` to `−5%`" claim is now more solidly established than
   the front's own `N=3000` runs alone could show, and no positive
   sub-region turns up anywhere even at ~5× the power.

---

## 1. T0-analogue: identity/Fact-A sanity re-check (`ref_identity_check.py`)

Not the focus of this review — the orchestrating session already performed
an exact, brute-force `Fraction`-arithmetic verification of Facts A/B and
identity (1.1) at `n=5,6` (five `(n,c,threshold)` cells, all matching
exactly). This is a belt-and-braces check at the real `n=65536` engine
scale, from scratch:

- **`b=1 ⟹ R_mask==seed_mask` exactly**: 0/20 violations. Confirmed.
- **Identity (1.1)** (direct `φ_far(2000)` vs. same-run measured-count-
  weighted per-bin sum): `0.026600` both ways, **exact match** (same
  underlying sums, as they must be — this is an algebraic identity, not an
  empirical claim).
- **The theoretical-bin-width-reweighted variant** (the front's disclosed
  "unresolved minor discrepancy" in their own T0, `0.027497` vs `0.027701`,
  `z=−13.9`) **reproduces the same qualitative pattern independently**: my
  `N=400` run gives `0.026600` (measured-weighted) vs `0.026609`
  (theoretical-weighted) — small but nonzero, same direction. This is a
  useful independent data point supporting the front's own diagnosis (an
  instance-level-correlation artifact, not a coding bug specific to their
  script) — it shows up again in completely independent code at a
  completely different `N`.
- A coarse decile-binned check of `L`'s marginal uniformity (Fact A),
  pooling all non-seed points of `N=400` instances, gave a huge
  chi-square (`440705` on 9 dof) — **this is expected, not a red flag**:
  pooling all `n` points of a *single* permutation instance and binning by
  that instance's own cycle-length structure is dominated by whichever few
  giant cycles that instance happens to have (standard Golomb–Dickman
  behavior), so per-instance bin counts are extremely correlated even
  though their *expectation* across instances is exactly uniform (Fact A).
  Sanity-checked directly: expected count in bin `(2000,4000]` over `N`
  instances is `N×2000` (bin width) by Fact A; observed totals in the later
  T1/T2 runs (`N=8000`→`~16.0M` expected vs measured within a few %;
  `N=15000`→`30.0M` expected vs `29.4M`/`29.6M` measured) match closely.
  This chi-square finding is, incidentally, a clean independent illustration
  of *exactly* the correlation phenomenon this archive's referees have
  flagged before and that motivates the cluster-robust design in §4 below.

## 2. T1 replication: Candidate-1 rejection (`ref_t1_candidate1.py`)

Target cell `c=1000,n=65536,b=1`, same bin edges as the front's own T1 (for
direct comparability only — the measurement code and seed are fully
independent), `N=8000` (5.3× the front's `N=1500`):

| `L` bin | `n_pts` | `φ̂` | Candidate-1 pred. | `z` |
|---|---|---|---|---|
| `[1,50)` | 382,515 | 0.71552 | 0.999849 | −389.8 |
| `[500,1000)` | 3,930,306 | 0.02690 | 0.877247 | −10419 |
| `[2000,4000)` | 15,699,518 | 0.02689 | 0.123012 | −2354 |
| `[4000,8000)` | 31,604,239 | 0.02749 | 0.000229 | **+937** |
| `[8000,16384)` | 65,448,754 | 0.02748 | ~0 | **+1360** |
| `[16384,32768)` | 129,341,775 | 0.02760 | ~0 | **+1916** |
| `[32768,65536]` | 258,413,169 | 0.02721 | ~0 | **+2689** |

Pre-registered-style criterion (≥3 of the `L≥4000` bins at `z≥10` against
Candidate 1): **met, 4/4**, at even more overwhelming significance than the
front's own (their `z` for the same 4 bins: `+397,+563,+798,+1176`; mine:
`+937,+1360,+1916,+2689` — larger `N`, larger `z`, same conclusion).
`φ̂` over the `L≥2000` bins: `[0.0269, 0.0275, 0.0275, 0.0276, 0.0272]`,
max/min ratio `1.026` — a clean plateau, **not** the Candidate-1 decay
(which predicts `~10⁻²⁴⁵` at `L/n=0.9`). **T1's rejection of Candidate 1,
and the plateau claim, both independently CONFIRM.**

## 3. T3 replication: abstract recursive-process simulator (`ref_t3_abstract.py`)

Built entirely from the prose in `ATTEMPT.md` §3.1/§4/§5 (state `(s,g)`,
mode `G`/`E`; boundary `Φ(s,0)=1`; at a "mark" — modeled as an exact,
non-discretized continuous-time process with `Exp(c)` inter-mark increments
of `s` — resolve `kill` w.p. `s` / `land in gap` w.p. `g` (`new gap
~Unif(0,g)`, mode→`G`) / `generic` w.p. `1−s−g` (mode→`E`, `g` unchanged);
in mode `G`, `s` and `g` move together, `g→0` before the next mark = SUCCESS)
— cross-checked against the governing PDEs in §5 (the `W(s,g)` formula's
absence of an explicit `s`-weighted term is exactly the "kill contributes 0"
fact, confirming the reading is faithful to the stated system, not just to
the prose in isolation). Implemented as a fully vectorized, exact
event-driven Monte Carlo (no time-grid discretization/approximation of its
own). `N=200,000` per `t0` (5× the front's `N=40000`):

| `t0` | `φ_abstract` (mine) | SEM | front's reported |
|---|---|---|---|
| 0.0001 | 0.90536 | 0.00065 | 0.905±0.0015 |
| 0.001 | 0.37847 | 0.00108 | 0.376±0.0024 |
| 0.01 | 0.03770 | 0.00043 | 0.0383±0.0010 |
| 0.09 | 0.03744 | 0.00042 | 0.0383±0.0010 |
| 0.37 | 0.03701 | 0.00042 | 0.0389±0.0010 |
| 0.90 | 0.03762 | 0.00043 | 0.0374±0.0010 |

Essentially **exact agreement**, point by point, with an implementation
built from the natural-language spec alone, never having seen `fcd_t3.py`.
Plateau criterion (ratio of the two largest-`t0` values to `t0=0.09`, must
stay in `[0.5,2]×`): `0.989` and `1.005` — **MET**, decisively. This is
strong, independent confirmation both that the mechanism (§3.1) genuinely
produces a plateau when simulated in its full (not mass-free-approximated)
form, and that the specific numeric level the front reports
(`≈0.037–0.039`) is reproducible from the prose spec, not an artifact of
their particular script. It also independently reproduces the *gap* the
front honestly disclosed (abstract-process plateau `≈0.0370–0.0378` sits
above the real engine's `≈0.026–0.028`, per §2 above) — this gap is real
and shows up in fully independent code on both sides, so the front's
disclosure of it as unresolved (not swept away) is the right call.

## 4. T2/T2b replication: fine `L/n` sub-binning, cluster-robust, two
independent runs (`ref_t2_finebinning.py`)

**A bug I found and fixed in my OWN code first (disclosed in full, per this
document's own standard of practice).** My first pass at this test used
`np.clip` to force `searchsorted` bin indices into range; for T2's bin edges
(which start at `2000`, not `1`), this silently dumped every point with
`L<2000` (short cycles, `φ` far above the plateau, e.g. `φ≈0.7` for very
short cycles) into the *first* reported bin `(2000,4000]`, producing a wildly
spurious `dev%=+51%`, `z=+549` and `z_cl=+42` result for that one bin. This
was caught immediately by cross-checking against T1 (same cell, overlapping
bin `[2000,4000)` measured completely independently gave `φ̂=0.02689`, not
`0.04242`) and by an expected-count sanity check (Fact A predicts
`N×`bin-width points per bin in expectation; the contaminated bin's count
was consistent with the correct expectation, meaning the *composition*, not
the count, was wrong). Fixed by excluding out-of-range `searchsorted`
indices instead of clipping them; both T2 runs (A and B) were then run
**fully fresh** with the fix. This bug lived entirely in this review's own
new code, never touched `sc_engine.py`/`sc_formula.py`, and never touched
any reported front-of-record number — it is disclosed here only in the
interest of the same transparency this archive asks of every front.

**Post-fix results, target cell `c=1000,n=65536,b=1`, front's own T2 bin
edges (`2000,4000,8000,16384,24576,32768,40960,49152,57344,65536`), `φ_U(1000)=0.028025`:**

| `L` bin | run A `dev%_cl` (`z_cl`) | run B `dev%_cl` (`z_cl`) | `z_diff`(A−B) | combined `dev%` (`z`) |
|---|---|---|---|---|
| `(2000,4000]` | −3.89 (−2.79) | −2.68 (−1.93) | −0.61 | **−3.29 (−3.34)** |
| `(4000,8000]` | −2.95 (−2.79) | −2.45 (−2.33) | −0.33 | **−2.70 (−3.62)** |
| `(8000,16384]` | −3.17 (−3.85) | −2.49 (−2.97) | −0.58 | **−2.84 (−4.83)** |
| `(16384,24576]` | −4.32 (−4.73) | −2.36 (−2.62) | −1.53 | **−3.33 (−5.19)** |
| `(24576,32768]` | −4.83 (−5.11) | −3.77 (−3.85) | −0.78 | **−4.32 (−6.35)** |
| `(32768,40960]` | −3.27 (−3.29) | −4.11 (−4.12) | +0.60 | **−3.69 (−5.24)** |
| `(40960,49152]` | −3.99 (−3.78) | −2.23 (−2.16) | −1.19 | **−3.09 (−4.19)** |
| `(49152,57344]` | −3.52 (−3.10) | −3.71 (−3.39) | +0.12 | **−3.62 (−4.59)** |
| `(57344,65536]` | −3.18 (−2.71) | −2.49 (−2.10) | −0.42 | **−2.84 (−3.40)** |

**Every one of the 9 bins is negative in both independent runs, and negative
in the combined estimate at `z≤−3.3` throughout — no bin shows a significant
positive cluster-level deviation anywhere, in either run alone or combined.
No bin shows a sign flip between run A and run B (all `|z_diff|<1.6`, fully
consistent with pure Monte Carlo noise).** In particular:

- The bin `(49152,57344]` (`L/n∈(0.75,0.875]`) — where the front's
  *original*, since-withdrawn T2 point-level run found a significantly
  **positive** bump (`+2.25%`, `z=+18.2`) — is **clearly negative** in both
  of my independent runs (`−3.52%`/`−3.71%`, `z_cl≈−3.1`/`−3.4`), matching
  the *direction* of the front's own cluster-robust T2b re-check
  (`−5.91%`) far more closely than the original point-level claim it
  withdrew. This independently confirms the withdrawal was correct.
- The bin `(57344,65536]` (`L/n∈(0.875,1]`) — the front's original T2's
  most dramatic point (`−8.04%`, `z=−72.8`, later found by T2b to shrink to
  a non-significant `−1.97%`, `z=−0.82`) — comes out at a modest, solidly
  mid-pack `−2.84%` (`z=−3.40`, combined) in my replication: **neither as
  extreme as the original point-level claim nor exactly matching the small
  T2b figure, but consistent with both being noisy `N=3000`-scale estimates
  of a real, modest, negative effect around the front's own final claimed
  order of magnitude.**
- Combined `dev%` across all 9 bins ranges `−2.70%` to `−4.32%` — **inside**
  the front's own final claimed `−1%` to `−5%` band, with no exceptions, and
  no discernible monotonic or non-monotonic trend beyond bin-to-bin noise
  (the small dip in the middle bins, `24576–40960`, does not clear a
  distinguishing bar against the flanks given typical per-bin SEMs of
  `~0.6–1%`).

**Conclusion on the T2/T2b crux question:** this review's own independently-
seeded, ~5×-more-powered, fully cluster-robust, two-run replication finds
**no significant positive sub-region anywhere in the far tail** — the
front's own withdrawal in §4, and its final coarse "negative throughout,
`−1%` to `−5%`, no resolved finer structure" summary, is the **correct**
honest characterization, not an over-conservative one. If anything, this
review supplies the properly-powered, all-9-bins, two-independent-run check
that the front's own `N=3000`/`N=3000` T2/T2b pair could only partially
provide (T2b directly re-checked only 3 of the 9 bins) — see §5.

## 5. The one named issue: §7's "cross-run agreement (7 of 9 T2 bins)"

`ATTEMPT.md` §7 states: *"`φ(ℓ)/φ_U(c)−1` sits in roughly the `−1%` to `−5%`
range... in the SAME direction and comparable magnitude in two
independently-seeded `N=3000` runs (T2 and its cluster-robust follow-up) —
this cross-run agreement (for 7 of 9 T2 bins) is the actually-robust part of
the finding."*

**This slightly overstates what T2/T2b's own comparison established.** T2b
(`fcd_t2_cluster.py`, per §4's own table) directly cluster-cross-checked
only **3 of the 9** T2 bins — `(24576,32768]`, `(49152,57344]`, and
`(57344,65536]` — not 7. Of those 3, only **1** (`(24576,32768]`) is
reported as genuinely agreeing in both sign and rough magnitude; the other
2 are precisely the ones the document goes on to say are "withdrawn" for
disagreeing (one sign-flips, one loses significance). The "7 of 9" figure
appears to count the 7 bins that were **never independently re-checked with
cluster SEM at all** (i.e., not contradicted, only untested) as if they were
confirmed by cross-run agreement — a real, if minor, imprecision: absence of
a contradicting re-measurement is not the same evidentiary category as a
demonstrated agreement across two independent seeds. This does not affect
any `z`-score or numerical result in the document; it is a synthesis-wording
issue in §7 only.

**Mitigating this fully:** §4's cross-run replication run in this review
(all 9 bins, two fully independent `N=15000` seeds, cluster-robust
throughout) now genuinely supplies the missing evidence — every one of the
9 bins *does* independently cross-run-agree in sign and rough magnitude
(§4's table), which is the substantive claim §7 was reaching for. The
front's underlying scientific instinct here was right; the specific
"7 of 9" justification offered for it, at the time it was written, was not
yet actually established by the front's own data. **Recommended fix (for
the front's authors or governance, not made here per the mandate against
modifying `ATTEMPT.md`): reword §7's bullet to either (a) drop the "7 of 9"
figure and describe the T2/T2b comparison honestly as "directly re-checked
on 3 of 9 bins, 1 of which replicated," or (b) cite this adversarial
review's §4 as the actual source of the all-9-bin cross-run confirmation.**

## 6. Other overclaim/error search (§2 arithmetic, §3.2 closed form, general read)

- **§3.2's closed-form numbers** (`Φ(t0)` at `t0=0.001,0.05,0.5,0.9` via
  `s_{1,2}=(−c±√(c²+4c/t0))/2`, `Φ(g)=[s₁e^{s₁g}−s₂e^{s₂g}]/(s₁−s₂)`)
  were independently recomputed from the stated formula (not from
  `derive_closed_form.py`): `0.65627, 0.05033, 0.00539, 0.00301` vs.
  reported `0.656, 0.050, 0.0053, 0.0030` — **exact match** to the reported
  precision. No arithmetic error; the document's honest rejection of this
  candidate (predicts continued decay, contradicts the observed/simulated
  plateau) is correct as stated.
- **`φ_U(1000)=0.028025`**, used throughout, independently recomputed via
  `scipy.integrate.quad` directly on `∫₀¹e^{-1000t²}dt` (not via
  `sc_formula.phi_U`, as a cross-check on the reused infrastructure):
  `0.0280250 ± 2×10⁻¹⁰` — matches exactly.
- **§3.1's "gap re-entry" mechanism** — this review did not re-derive it
  (it is a purely deterministic, non-random cyclic-order fact, and the
  orchestrating session already checked it exhaustively for every cycle
  length `L=2..11` and every starting index). Re-reading the proof text
  itself: it is correct and essentially a restatement of "on a directed
  cycle, walking forward from any point reaches a second marked point
  before reaching a third point that lies strictly between the second point
  and the first, going forward" — a tautological fact about cyclic order,
  correctly applied to the specific "already-visited arc is immediately
  downstream of `x0`" structure of this problem. No issue found.
- **§5's disclosed numerical-attempt failure** (`solve_2d_system.py`,
  `Φ(0,0.37)=1.0` artifact) is reported as a *named* implementation failure
  with a specific diagnosed cause (the `Φ(s>0,·)` row not being resolved
  before being used inside `Avg_g` for `s>0`), not glossed over or silently
  dropped. This is exactly the right way to report a failed sub-attempt;
  no independent re-implementation of this bounded, disclosed-as-failed
  attempt was undertaken (out of scope — nothing is asserted to follow
  from it).
- **General read of §6–§7**: the Established/Heuristic/Open trichotomy is,
  apart from the one §7 imprecision named in §5 above, an accurate
  reflection of what is actually shown. In particular, the document does
  **not** overclaim that T2's finer (bump/no-bump) structure is resolved —
  it explicitly, repeatedly says the opposite ("this front does not claim
  to have resolved it," "explicitly unresolved," "left open") — and this
  review's own higher-powered replication (§4) confirms that caution was
  warranted, not merely defensive.

## 7. Does "HONEST PARTIAL CLOSURE" hold up?

Yes. Re-examined specifically for whether the T2 withdrawal was itself
sufficiently conservative (this review's mandate's central question):
**it was — if anything, mildly under-confident rather than over-confident.**
The front withdrew a specific finer claim it could not defend at `N=3000`
and fell back to the coarser "negative throughout, `−1%` to `−5%`" summary.
This review's independent, ~5×-larger, two-run, fully cluster-robust
re-measurement (§4) finds that coarser summary to be **exactly right, with
no exceptions across all 9 bins and no hint of a positive sub-region even at
substantially higher power** — the honest thing to have claimed, and the
front claimed it, no more and no less (net of the one wording imprecision in
§5, which understates rather than overstates the strength of that specific
claim's evidentiary basis at the time of writing, and is now moot given
this review's own confirmation).

---

## 8. Files (this review)

| file | role |
|---|---|
| `ref_common.py` | shared measurement code (engine wrapper, binning, multiprocessing driver) — written from scratch against `sc_engine.py`'s API |
| `ref_mp_worker.py` | multiprocessing worker for real-engine (`n=65536`) batched runs |
| `ref_identity_check.py`/`.log` | T0-analogue: `b=1` reduction + identity (1.1) sanity re-check |
| `ref_t1_candidate1.py`/`.log` | T1 replication: Candidate-1 rejection, `N=8000` |
| `ref_t2_finebinning.py`, `ref_t2_runA.log`/`.npz`, `ref_t2_runB.log`/`.npz` | T2/T2b replication: two independent `N=15000` cluster-robust runs |
| `ref_t3_abstract.py`/`.log` | T3 replication: abstract recursive-process simulator, built from prose alone, `N=200000` per `t0` |
| `REFEREE_REPORT.md` | this document |

No file outside `floor_closed_form_attempt/adversarial/` was written or
modified. No git commit made.

---

> **VERDICT: SOUND WITH NAMED ISSUES.** Every empirically-testable claim
> assigned to this review for independent re-verification (T1's Candidate-1
> rejection, T3's abstract-process plateau built from the prose spec alone,
> and T2/T2b's central "is there really no positive sub-region" question)
> **independently replicates**, at 5×+ the front's own statistical power,
> from scratch, with fresh seeds. One minor wording imprecision is named in
> §5 (§7's "7 of 9 bins" cross-run-agreement framing overstates what T2/T2b
> alone established, though this review's own §4 now actually establishes
> the intended claim properly). One bug was found and fixed in this
> review's own code before it reached any reported number (§4), disclosed
> in the same spirit of transparency this front itself modeled. **No error
> changes the front's verdict.** The "HONEST PARTIAL CLOSURE" framing, and
> specifically the decision to withdraw T2's finer bin-by-bin claim while
> keeping the coarser cross-run-robust one, holds up under independent,
> higher-powered scrutiny — this review finds the withdrawal was the right
> call and the surviving coarse claim is, if anything, more solidly true
> than the front's own `N=3000` evidence alone could show. **ACCEPT for
> catalogue**, with the §5 wording issue flagged for optional correction by
> the front's authors or governance (not made here, per the mandate against
> modifying `ATTEMPT.md`).
