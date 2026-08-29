# REFEREE REPORT — `gap_rate_candidate_attempt/ATTEMPT.md`
(`MCLUST-GAP-RATE-CANDIDATE-ATTEMPT`, wave 25 front (d), `DISC-DEC-118`)

## VERDICT: **SOUND**

No errors found. Every headline numerical claim in the target document was
independently reconstructed from scratch — before the target's own scripts
were opened — using data transcribed directly by this referee from the
cited source documents, and matched the target's reported numbers exactly
(to the precision both sides reported). The document's mechanical
discipline claims (no git, no seeds/randomness used, scope confined to its
own subdirectory) were independently audited and confirmed. One
initially-puzzling mtime anomaly (a sibling directory with files dated the
same day) was investigated and resolved as unrelated, separately-authorized
archive activity, not a scope violation by this front. This is pure
combinatorial/asymptotic mathematics (M-CLUST(b), Tree B); no Millennium
Prize Problem claim appears anywhere, consistent with the document's own
disclaimer.

---

## 1. Method

Per the mandate: read the target `ATTEMPT.md` in full, then the parent
front's `ATTEMPT.md` §A.1/§A.2/§A.4 (and enough of Parts A/B for context),
then `floor_closed_form_attempt/ATTEMPT.md` §2/§4 (the ultimate source of
the T1/T2 bin data), then the parent's own `adversarial/REFEREE_REPORT.md`
§4.3 (the exact source of the "N1" finding this front addresses). Only
*after* independently transcribing the bin data from these sources and
re-deriving every claimed number from scratch (`adv01_independent_
reconstruction.py`, written before any target `.py` file was opened) were
the target's own `r01`/`r02`/`r03` scripts read, to check methodology and
confirm the logs are genuine (re-run fresh, diffed byte-for-byte against
the checked-in `.log` files — all three matched exactly). A separate
mechanical audit (`adv02_scope_git_seed_audit.py`) checked git usage, seed
usage, the reserved-seed-block claim, and file mtimes archive-wide.

## 2. What was independently confirmed

**(1) The fixed-`(c,n)` premise.** Directly quoted from the parent's own
§A.4: `n=65536` is described as "the record's own target cell" throughout,
and `floor_closed_form_attempt/ATTEMPT.md` §2/§4 states "Target cell
`c=1000,n=65536,b=1`" for both T1's and T2's underlying simulations
(`fcd_t1.py`/`fcd_t2.py`/`fcd_t2_cluster.py`). Neither table has a `c` or
`n` column — only `t0`/`L` and `phi_real` vary. The premise is correct:
`(c/n)^p` is necessarily one fixed number per `p`, for any table drawn from
this record.

**(2) Independent re-derivation of the fit.** `adv01_independent_
reconstruction.py`, using bin data transcribed by hand from the parent's
§A.2 (not copied from the target's own `r01`/`r02`), reproduced *every*
number in the target's §2.2 tables to the reported precision:
- T2-composite best-fit prefactors: `A*=1.5633` (p=1/3), `1.1033` (p=1/4),
  `0.8951` (p=1/5) — exact match.
- T1: `1.6471`, `1.1624`, `0.9430` — exact match.
- RMS/max residuals (fit): T2 `2.345pp`/`4.424pp`, T1 `7.201pp`/`14.133pp`
  — exact match (target rounds to `4.42pp`/`14.13pp`).
- Natural-`A=1` RMS residuals for all six (table, p) combinations — exact
  match to 3-4 significant figures.
- Degeneracy check: the fitted-model residual and `(gap_i - mean(gap))`
  agree to floating-point roundoff (`<1e-9`) for every exponent tested —
  confirms the "shape-blind by construction" claim is not merely asserted
  but arithmetically true.

**(3) Exact-unit-prefactor exponent `p*`.** Independently solved
`(c/n)^{p*} = mean(gap)`: `p*=0.214025` (T1), `p*=0.226505` (T2) — exact
match to the target's reported values (`0.2140`/`0.2265`), including the
`1/p*` values (`4.6723`/`4.4149`).

**(4) Precision-bar ordering and outcome.** §1 of the target ("Precision
bar, stated up front, before any fit is examined") precedes §2 ("Core
result") in document order — the ordering claim is correct on inspection,
not merely asserted. The stated bar (≤3pp per bin, best-fit prefactor
within `±25%` of unity) is failed by all three exponents on both tables
under the target's own numbers (T2 max resid `4.42pp > 3pp`; T1
`14.13pp > 3pp`) — independently confirmed via `adv01`.

**(5) Transcription cross-check.** Independently recomputed `gap% =
(Pi_abstract - phi_real)/phi_real*100` from the `phi_real` values quoted in
`floor_closed_form_attempt/ATTEMPT.md` §2/§4 (Decimal, 50-digit precision)
and compared to the published, rounded gap% figures in both T1 and T2:
max discrepancy `0.004865pp`, matching the target's claimed `"max
discrepancy 0.0049pp"` exactly, and consistent with pure rounding
artifacts of the published 4-5-significant-figure `phi_real` inputs — not
a transcription error.

**(6) Exploratory `n_eff(t0)=n(1-t0)` extension (§4).** Independently
re-fit (genuine, non-degenerate OLS since `x_i` now varies with `t0`):
reproduced every `(A, RMS, max|resid|, R²)` quadruple in the target's §4
table exactly, for all three exponents on both tables (e.g. T2, p=1/4:
`A=0.8237`, `RMS=8.959pp`, `max=20.554pp`, `R²=-13.591`, matching the
target's `"-13.59"`). Spot-checked the specific claim "predicted `58.0%`
at `t0=0.938` vs. observed `37.46%`, a `-20.55pp` miss": independently
computed `A·rate_eff = 0.8237 × 70.434% = 58.01%`, miss `= 37.46 - 58.01 =
-20.55pp` — exact match.

**(7) N1 correctly represented.** Read the parent's own
`adversarial/REFEREE_REPORT.md` §4.3 directly: the referee's own table
gives `(c/n)^{1/3}=24.80%` needing `~1.56×`, `(c/n)^{1/4}=35.15%` needing
`~1.10×` — exactly what the target's header and §0 attribute to N1. The
target's characterization of N1 ("flagged `(c/n)^{1/4}` as never tested
against bin data, prefactor `~1.10×`") is accurate, not a strawman or
exaggeration of the referee's actual finding.

**(8) Mechanical/scope-discipline audit** (`adv02_scope_git_seed_audit.py`):
- No `git`/`subprocess`/`os.system` call in any of the 3 target scripts.
- No code-level randomness usage in any of the 3 target scripts (the sole
  "random" hit is the English word inside "no new simulation, no
  randomness" prose, not a code construct).
- The reserved seed block `20260932000-20260932999` is referenced nowhere
  in the archive except the `DECISION_LEDGER.yaml` reservation line, the
  `DISCOVERY_LAB_STATE.md` summary line, and the target's own
  `ATTEMPT.md` — genuinely unused, consistent with the document's claim
  that no Monte Carlo was needed.
- All three target scripts reproduce their checked-in `.log` files
  byte-for-byte when re-run fresh — the logs are genuine script output,
  not hand-edited or fabricated text.
- The parent front's own top-level files and its own `adversarial/` all
  predate 2026-08-29 (0 files dated today) — confirms the target did not
  touch them.

**(9) The one anomaly investigated and resolved.** The sibling
`mclust_h1_validity_attempt/` directory contains a NEW subdirectory,
`h1_translation_structure_attempt/` (8 files), dated 2026-08-29 —
initially looking like a possible scope violation, since the mandate's
checklist expects sibling files to predate that date. Investigation
(reading the file's own header, and cross-checking `DECISION_LEDGER.yaml`)
confirmed this is `H1-TRANSLATION-STRUCTURE-ATTEMPT`, wave 25's
**separately-authorized front (c)** under the SAME `DISC-DEC-118` decision
that authorizes the target front (d) — a topically unrelated question
(kernel exponential-conjugation / translation-invariance for the H1 line),
running the same day under its own seed block
(`20260931000-20260931999`, distinct from front (d)'s
`20260932000-20260932999`). A grep cross-check of all 4 new `.py` files
found no reference to gap-rate/power-law content. This is normal
same-day multi-front archive parallelism, not attributable to the target
document, whose own scope-discipline section (correctly) never claims
responsibility for `mclust_h1_validity_attempt/`'s future contents — only
that it was not modified by *this* front, which remains true.

## 3. Findings

**None.** No fabricated results, no cherry-picked bins (full 6-bin T1 and
9-bin T2-composite tables used, matching the parent's published tables
exactly), no unit/convention mismatch between T1 and T2 (both derived from
the same `Pi_abstract` constant and the same `c=1000,n=65536` cell), no
inconsistency between the executive summary and the detailed body (every
exec-summary number was checked against its corresponding section and
matched), no closure claimed where none was earned (the document
explicitly and repeatedly states "No candidate reaches tier (a) closure"),
and no framing overreach: the "shape-blindness" argument is explicitly
labeled "elementary" in the document's own §2.1 prose at the moment it is
introduced, and the elimination language used ("tier (b), of the CLASS")
is exactly the tier definition the document itself sets up in §1 *before*
presenting results — not an inflated claim smuggled in after the fact. The
document is also careful to keep "eliminated for SHAPE" (rigorous,
structural) and "does not reach closure for MAGNITUDE" (empirical,
bar-based) as two separate, correctly-scoped claims, rather than
conflating them.

This archive's standing discipline treats an honest non-closure/
elimination result as fully legitimate; nothing here changes that — the
elimination argument and the degeneracy argument underpinning it are both
independently confirmed correct and honestly scoped.

## 4. A procedural note on this referee's own footprint

`adv02`'s "(E)" check re-runs the target's 3 scripts **in place** (in the
target's own directory) in order to diff their fresh stdout against the
checked-in `.log` files. `r02_power_law_fit.py` and
`r03_perbin_and_exploratory.py` write `r02_fit_results.json` /
`r03_results.json` as a side effect, so this refreshed those two files'
mtimes (both already dated 2026-08-29, from the target front's own
original run — no cross-day contamination). Verified independently
(`sha256sum`, plus a from-scratch re-run in an isolated temp copy): both
JSON files are **byte-identical** before and after — content is 100%
unchanged, since the computation is deterministic. No file outside this
`adversarial/` directory was substantively modified; disclosed here for
full transparency per the mandate's strict "do not modify files outside
`adversarial/`" instruction.

## 5. Files in this directory

| file | role |
|---|---|
| `adv01_independent_reconstruction.py` / `.log` / `adv01_results.json` | From-scratch re-derivation (before target scripts were read) of the structural degeneracy claim, magnitude fits, `p*` solving, Pearson `r`, the `n_eff(t0)` exploratory extension, and the transcription cross-check |
| `adv02_scope_git_seed_audit.py` / `.log` | Mechanical audit: git-usage, seed-usage, reserved-seed-block archive-wide scope, file mtimes (target dir, parent dir, parent's adversarial/, sibling dir), and fresh-rerun-vs-checked-in-log diff for all 3 target scripts |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was modified. No git
command was run.
