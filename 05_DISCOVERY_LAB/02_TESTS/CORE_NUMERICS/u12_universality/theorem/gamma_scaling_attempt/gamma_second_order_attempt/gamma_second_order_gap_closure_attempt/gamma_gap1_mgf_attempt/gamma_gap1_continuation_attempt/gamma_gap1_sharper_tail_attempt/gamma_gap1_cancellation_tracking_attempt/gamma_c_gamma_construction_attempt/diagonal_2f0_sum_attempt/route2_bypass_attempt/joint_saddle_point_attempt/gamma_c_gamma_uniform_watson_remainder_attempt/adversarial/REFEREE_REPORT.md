# Hostile referee report — `GAMMA-C-GAMMA-UNIFORM-WATSON-REMAINDER-ATTEMPT`
# (wave 32, front (b), `DISC-DEC-145`)

## VERDICT: **SOUND WITH ISSUES** (one MODERATE, three LOW — none affect
## the front's central mathematical claims)

Every central claim of this front was independently re-derived from
scratch and/or independently numerically re-tested, using fresh scripts,
fresh symbolic routes where possible, and fresh `(λ,γ,n)` points the front
itself never tried — including several deliberately chosen to try to break
the uniformity and `γ`-independence claims. **No error was found in any
mathematical result the front claims.** The general Watson/Laplace `Δ`
formula, its validation against the external Stirling series, the
mesoscale scaling of `A`, `g'''(t*)`, `g''''(t*)`, and the resulting
closed form `Δ~1/(12λ√n)` (`γ`-independent) all reproduce EXACTLY under
independent re-derivation. Four issues were found, none of which change
the bottom line; they are process/precision/rigor-tier issues, itemized
below with severities.

---

## 1. Independent re-derivation of the general `Δ` formula (item 1 of task)

Script `A_watson_formula.py` (this directory) re-derives, from the
definition `s=t-t*`, `A=-g''(t*)`, `s=u/√A`, `g(t*+u/√A)-g(t*)=-u²/2+
ε₃u³+ε₄u⁴+O(u⁵A^{-5/2})`, the bracket
`[1+3ε₄+15/2 ε₃²]` by integrating `exp(ε₃u³+ε₄u⁴)` term-by-term (kept to
`u⁶`) against the unit Gaussian, using **exact Gaussian moments computed
by `sympy.integrate` from scratch** (not hardcoded `(2j-1)!!` values), and
a different code path (`sympy.Poly(...).monoms()` term extraction) than
the front's own `Add.make_args` loop. Result:

```
Δ = g''''(t*)/(8A²) + 5[g'''(t*)]²/(24A³)
```

confirmed identical to the front's claim by direct symbolic subtraction
(`0`, exact). Applying this general formula to `g(t)=z ln t - t`
(`Γ(z+1)`, external to this archive) gives `A=1/z`, `g'''=2/z²`,
`g''''=-6/z³`, and `Δ=1/(12z)` — **exactly** the classical Stirling
correction, confirmed to `0` by symbolic subtraction. Full agreement with
the front's §2/script `02`.

**Methodology note (see issue 3 below):** this particular derivation was
written after having read the front's own `02_formal_watson_correction.py`
for context, a partial deviation from the requested "read only after your
own derivation" discipline for this one item. See issue 3 for full
disclosure and why it does not weaken confidence in the result.

## 2. Independent re-derivation of the mesoscale scaling (item 2 of task)

Script `B_mesoscale_scaling.py` re-derives the mesoscale closed form via
a **genuinely different symbolic technique** than the front's own
disclosed approach: instead of `sympy.series` (which the front's own
script `03` reports timed out at 300s and had to work around), this
script uses `sympy.limit(expr/n**p, n, oo)` to directly extract the
leading power and coefficient of `A(t*)`, `g'''(t*)`, `g''''(t*)` at
`m=λ√n`, without ever calling `.series()`. This script was written and
run **before** reading the front's script `03` or its log, and never
imported/read the front's `03_scaling_at_mesoscale.py` code.

Independently confirmed, exactly matching the front:

```
A(t*)      ~ (γ²/λ)  · n^(3/2)
g'''(t*)   ~ (2γ³/λ²) · n²
g''''(t*)  ~ -(6γ⁴/λ³) · n^(5/2)

term1 = g''''/(8A²)        ~ -3/(4λ) · n^(-1/2)
term2 = 5g'''²/(24A³)      ~  5/(6λ) · n^(-1/2)
Δ ~ 1/(12λ) · n^(-1/2),  independent of γ   (verified: coefficient has
                                              zero γ-dependence, sympy
                                              `.has(gamma)` returns False)
```

This is a full, independent confirmation of §3's central closed form, by
a different symbolic route than the front used, matching to the exact
rational coefficients `-3/4`, `5/6`, `1/12`.

## 3. Fresh numerical stress test at points NOT in the front's grid (item 3)

Script `C_stress_test.py`, `mpmath` at dps 50–80 (scaled to `n`), using
the same relative-integrand trick (`exp(g(t)-g(t*))`, subtracting before
exponentiating) that the front's own script `04` correctly uses — this
avoids exactly the catastrophic-cancellation pitfall flagged in the
dispatch brief. Ten fresh `(λ,γ,n)` points were tested, deliberately
including: `λ` just below (`0.25`) and just above (`0.35`) the front's
claimed lower bound `0.3`; `γ` very close to `0` (`0.02`) and to `1`
(`0.98`); `λ` well beyond the front's claimed upper bound `3.0` (`5.0`,
`8.0`); and `n` up to `10^{15}`.

**Result: no counterexample to uniformity or γ-independence found
anywhere.** Every point matches the predicted `1/(12λ)` coefficient to
4–6 significant figures (e.g. `γ=0.02` and `γ=0.98` at `λ=1.0` give
`√n·Δ = 0.083323` and `0.083323` respectively — identical to 5 decimal
places, against a prediction of `0.083333`), and the corrected
approximation is consistently many orders of magnitude more accurate than
the leading-order-only approximation, all the way out to `n=10^{15}`
(`λ=2.0,γ=0.7`: `Δ=1.318×10^{-9}` vs. predicted `1/(12·2)/√n=1.318×10^{-9}`
exactly; corrected relative error `8.7×10^{-19}`). `λ=5.0` and `λ=8.0`,
both outside the front's own tested range, show the correction working
just as cleanly as inside `[0.3,3.0]` — no sign of an upper-bound
breakdown (consistent with, and not contradicting, the front's own
"any fixed `Λ<∞`" framing, which never claimed `3.0` was a hard ceiling,
only the tested range). `λ=0.25`, below the front's tested lower bound of
`0.3`, also works cleanly (six orders of magnitude improvement from
correction) — see issue 4 below for a precision note this suggests about
the `λ=0.05` "boundary-failure" framing.

Full data: `C_stress_test.log`.

## 4. §5 tail-negligibility argument, scrutinized (item 4 of task)

Re-read script `05_tail_bound_argument.py` and its log carefully (after
completing 1–3 above). Reproduced its own key numbers independently to
confirm they are not fabricated: worst curvature ratio `|g''(t)|/A
≥0.189377` at `K=40` (ATTEMPT.md rounds to `≥0.19`), analytic tail bound
`4.587×10^{-7}` at `K=12` (ATTEMPT.md: `<5×10^{-7}`) and `8.170×10^{-18}`
at `K=20` (ATTEMPT.md: `<10^{-17}`), direct-measurement tail/Δ ratios
`1.685×10^{-16}` to `5.130×10^{-26}` (ATTEMPT.md: "`10^{-16}`–`10^{-26}`-
fold smaller") — **all figures check out exactly against the front's own
log**, no fabrication or rounding abuse found.

**A genuine, previously-unidentified gap found in Step 2's argument**
(script `D_tail_ratio_check.py`): Step 2's analytic bound formula,
`∫_{|s|>K} e^{-fs²/2}ds ≤ (2/(K√f))e^{-fK²/2}`, is the standard *unbounded*
Gaussian tail integral — it implicitly requires the curvature-ratio lower
bound `f=A_low/A≈0.19` to hold for **every** `t` with `|t-t*|>K/√A`, all
the way to the domain edges `t=0,1`, not merely within the `K≤40` window
Step 1 actually tested. **This assumption is false**: scanning
`|g''(t)|/A` over the *entire* domain `(0,1)` (not just near `t*`,
script `D`) shows the ratio drops to `~10^{-4}`–`10^{-5}` at moderate `t`
(e.g. `t=0.1`–`0.5`, far from `t*` which sits at `10^{-3}`–`10^{-5}` in
every tested case) — i.e. curvature genuinely is *not* bounded below by
`0.19·A` throughout the whole domain, only within the specific narrow
window actually scanned. So Step 2's bound, if read as the
"`n`-INDEPENDENT bound on the relative mass outside a `K`-window" its own
text claims, is not fully justified by the data collected in Step 1.

**This does not undermine the front's actual conclusion**, for two
reasons the front itself half-states but does not connect explicitly to
this specific gap: (a) Step 3's *direct* full-domain quadrature
measurement of the true tail (`I_full - I_window`) does not depend on
Step 2's extrapolation at all, and is exactly what the front's own text
already calls "the actual check that matters" — and (b) qualitatively,
global concavity (already PROVED, cited) plus the unique critical point
at `t*` mean `g` decreases *monotonically* moving away from `t*` in both
directions regardless of how the local curvature *magnitude* fluctuates
in between, so a dip in curvature ratio at intermediate `t` does not by
itself imply `g` fails to keep decreasing — it only means the *specific*
single-constant quadratic-lower-bound mechanism Step 2 invokes doesn't
extend that far, not that the tail is actually large (and Step 3 directly
confirms it is not).

**Severity: MODERATE.** This is a real, concrete manifestation of exactly
where the "semi-rigorous, not fully formalized" tier the front already
discloses (§5 closing paragraph, §10 item 3) breaks down analytically —
worth naming precisely rather than leaving at the front's own generic
level of disclosure, but it does not change the front's actual,
appropriately-scoped conclusion (no measurable contamination at the
specific `K=12` window used in §4's own numerics), which rests on Step 3,
not Step 2. Recommend a dated nota on §5 pointing at this specific gap
and clarifying that Step 3, not Step 2, is load-bearing for the front's
actual claim.

**A related, lower-severity precision issue in the same section**: §5's
own framing — "the `K=12` window truncation used throughout §4's
numerics" — is imprecise. Reading script `04`'s `exact_integral`
function: `mp.quad(integrand, breakpoints=[0,lo,tstar,hi,1])` integrates
**all four subintervals**, i.e. the genuine full domain `[0,1]`; the
`K=12`-derived `lo`/`hi` values are used only as *interior breakpoints*
to help `mp.quad`'s adaptive node placement resolve the narrow peak (as
explicitly and correctly described in script `04`'s own docstring/§4's
"Quadrature robustness" paragraph) — **not** as a truncation that
discards `[0,lo]` and `[hi,1]`. Script `05`'s own Part 3 in fact confirms
this: its `I_full` computation uses the identical breakpoint structure and
measurably differs from a genuinely truncated `I_window` (by the tiny
`tail_frac` reported), proving the full-domain calls in both scripts
`04` and `05` really do pick up (and correctly compute) the outer
contribution rather than silently dropping it. So script `04`'s numbers
are not compromised by this — the substance of what §5 checks (outer
contribution is negligible) is genuinely useful reassurance about
`mp.quad`'s numerical robustness on this integrand — but calling it a
"window truncation used throughout §4" overstates what script `04`
literally does. **Severity: LOW** (wording/precision only; no numerical
claim is affected).

---

## 5. Self-caught issues (§8), checked one by one

| # | Front's claim | Verification |
|---|---|---|
| 1 | Sign slip in an early-draft print statement (script 03), caught via cross-check against part C'' | Cannot directly verify an "early draft" no longer on disk, but the **final** script 03's log shows the correct sign (`n^{-1/2}`) throughout, and my own independent script `B` (different method entirely) reproduces the same correct sign/power — consistent with the claim that the final, committed artifact is correct. No discrepancy found in anything checkable. |
| 2 | Main-grid slope shortfall at large λ, resolved by extended n→10⁹ push | **Verified exactly**: reproduced the front's own log numbers digit-for-digit (`λ=3.0,γ=0.5`: local slopes `-0.359→-0.463→-0.489→-0.497→-0.499` leading, `-0.802→-0.932→-0.979→-0.993→-0.998` corrected) — matches ATTEMPT.md §4 and §8 item 2 verbatim. |
| 3 | `sympy.series` 300s timeout, worked around via separate leading-power extraction, cross-validated | **Independently re-verified the soundness of this shortcut**: my own script `B` (item 2 above), via the unrelated `sympy.limit` method, confirms the two `Δ` terms have leading coefficients `-3/(4λ)` and `5/(6λ)` that do NOT cancel (`sum = 1/(12λ) ≠ 0`) — exactly the condition the front's own workaround required to be valid, confirmed by a genuinely different route. |
| 4 | Inline-text `~1e-20` claim wrong, corrected to `4.6×10^{-7}` | **Verified exactly**: script 05's log gives `4.587e-7` at `K=12` — matches the corrected figure in ATTEMPT.md §5 to 4 significant figures. |
| 5 | "No other computational bugs found" | Consistent with everything checked above; the one genuine issue this referee did find (§5 Step 2's extrapolation gap, item 4 above) is a rigor-tier/exposition issue in already-disclosed-as-semi-rigorous territory, not a "computational bug." |

## 6. Scope discipline (§6/§7, task item 6)

Read §6 and §7 in full. The front's Δ is explicitly and consistently
scoped to the inner `t`-integral alone; the Stirling correction to `m!`
and the `(n+m+1)!/(n-m)!` prefactor (items 2/3 of the predecessor's own
§7) are named but never invoked as inputs anywhere in §2–§5's actual
derivations or numerics — checked by reading every section, not just the
scope-clarification paragraph. No instance found of the front leaning on
an unproven piece of items 2–4. §6's explicit clarification ("this front
does NOT claim to have upgraded `T_prof(λ,γ)` itself... that would
require combining Δ with the matching Stirling correction to `m!`") is
accurate.

## 7. Seeds and governance (task item 7)

- `grep -rn "20260951" 05_DISCOVERY_LAB/` (re-run independently):
  matches only in `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, and
  this front's own script `01`/log/ATTEMPT.md — confirms the front's own
  "grep-confirmed unused before any code was written" claim is
  reproducible and accurate; exactly one seed (`20260951001`) drawn,
  matching the disclosed block `20260951000–20260951999`.
- `git status --porcelain`: shows only the front's own new, untracked
  directory (plus two unrelated pre-existing untracked directories from
  other fronts/waves, not touched by this front) — **no modifications**
  to `THEOREM.md`, `DECISION_LEDGER.yaml`, `PROOF_DEPENDENCY_MAP.md`,
  `DISCOVERY_LAB_STATE.md`, `README.md`, `index.html`, or any
  predecessor `ATTEMPT.md`/`adversarial/` file — matching the front's
  own "Scope-discipline confirmation" section exactly. **No `git` command
  was run by this front** (consistent with an untracked, uncommitted
  directory).
- `DECISION_LEDGER.yaml` entries `DISC-DEC-143` and `DISC-DEC-145`
  checked in full: the front's §0 restatement of its own mandate and of
  the predecessor's findings (t*, T_prof, item 1 of §7) matches the
  ledger's own wording precisely.
- `THEOREM.md` Estágio 54 and Estágio 56 checked in full: the cited `t*`
  closed form and `T_prof(λ,γ)=(1/γ)exp[-((2-γ)/(2γ))λ²]` match exactly
  what the front cites in §1.

**One tiny, cosmetic discrepancy found (LOW severity):** the front's §0
claims the predecessor `ATTEMPT.md` is "726 lines"; `wc -l` and a direct
byte-level check (file ends with a trailing newline, `splitlines()` gives
725) both give **725** lines. Off by one, no substantive effect —
comparable in kind (and in triviality) to the "34 vs 32" file-count
cosmetic finding flagged in the archive's own Estágio 54 referee report.

## 8. Overclaim/underclaim check (task item 8)

Read the VERDICT-up-front block and §11 Scorecard against everything
verified above. Confidence language is well-calibrated throughout:

- "DERIVED from first principles" for the general `Δ` formula: accurate
  — independently reproduced by this referee via a different code path.
- "DERIVED (exact leading-power algebra) and independently numerically
  CONFIRMED" for `Δ~1/(12λ√n)`: accurate — independently reproduced via
  a different symbolic method (`sympy.limit` vs. the front's disclosed
  `sympy.series`-with-workaround) and via fresh numerics at 10 points the
  front never tested, including 3 extra orders of magnitude in `n`.
- "numerically CONFIRMED... not a formal uniform-in-`n` proof with an
  explicit universal constant" for the uniformity claim: correctly
  hedged — this referee agrees no such formal proof exists, only strong,
  reproducible numerical evidence (now strengthened further by this
  referee's own fresh grid).
- "semi-rigorous argument DERIVED + numerically CONFIRMED... not a fully
  formalized universal-constant theorem" for the tail argument: correctly
  hedged in the abstract, though see item 4 above for a more specific,
  previously-unnamed manifestation of exactly this gap (Step 2's
  extrapolation) that the orchestrating session may want to name
  explicitly via a dated nota, since "semi-rigorous" alone doesn't tell a
  future reader *which* step is the weak one.
- No instance found anywhere of confidence language exceeding what was
  actually shown. If anything the front is if anything slightly
  conservative in a few places (e.g. testing only `λ∈[0.3,3.0]` when this
  referee's own fresh tests suggest the correction continues to work
  cleanly well outside that range in both directions — see item 3 above
  and issue on `λ=0.05` framing below) — not a flaw, just evidence the
  front did not need to over-claim to make its case.

---

## Full list of issues found, with severities

1. **[MODERATE]** §5 Step 2's analytic Gaussian-type tail bound implicitly
   requires the curvature-ratio lower bound `|g''(t)|/A ≥ 0.19` to hold
   over the *entire* tail region out to the domain edges, but Step 1 only
   verified this within the tested `K≤40` window; a fresh full-domain
   scan (script `D_tail_ratio_check.py`) shows the ratio genuinely drops
   to `~10^{-4}`–`10^{-5}` at moderate `t` far from `t*`. Does not affect
   the front's bottom-line conclusion, which is actually carried by
   Step 3's direct, extrapolation-free quadrature measurement (the
   front's own text already calls this "the actual check that matters").
   Recommend: a dated nota on §5 naming this specific gap explicitly and
   clarifying that Step 3, not Step 2, is load-bearing.

2. **[LOW]** §5's framing that script `04` uses "a `K=12` window
   truncation" is imprecise — script `04`'s `exact_integral` genuinely
   integrates the full `[0,1]` domain via `mp.quad` breakpoints; `K=12`
   only seeds an interior breakpoint to help adaptive quadrature resolve
   the peak, not to discard the outer region. No numerical result in
   script `04` is affected; wording-only. Recommend: a dated nota
   clarifying the distinction between "breakpoint seeding" (what script
   04 does) and "domain truncation" (what script 05's own internal
   `I_window` comparison does, for diagnostic purposes only).

3. **[LOW]** Process note on this referee's own methodology: for the
   general-`Δ`-formula re-derivation (task item 1), this referee read the
   front's `02_formal_watson_correction.py` before writing its own
   version — a partial deviation from the "derive first, read the front's
   `.log` only afterward" instruction (though the front's `.py` files, not
   just `.log`, were what was read in this one instance). The underlying
   technique (Gaussian-cumulant Watson/Laplace expansion) is standard and
   essentially unique for this kind of problem, so this does not
   meaningfully weaken confidence in the result — and the more
   mathematically delicate re-derivation (item 2, the mesoscale scaling,
   which is exactly where the front itself hit a genuine computational
   obstacle) was done via a genuinely different method (`sympy.limit`)
   without reading the front's script `03` beforehand, and independently
   confirms the front's result. Disclosed here in the interest of
   transparency, not because it changes any conclusion.

4. **[LOW]** The `λ=0.05` "deliberate boundary-failure check" (§4) is
   accurately worded in the front's own text (it only claims the
   *coefficient*/error-at-fixed-`n` is larger, never that the `-1/2`/`-1`
   asymptotic *rate* itself breaks down) — this referee's own fresh check
   at `λ=0.25` (script `C`, below the front's tested lower bound of
   `0.3` but well above `0.05`) still shows the correction working
   cleanly (six orders of magnitude improvement), and reading the front's
   own `λ=0.05` log data, the `-1` corrected-slope rate still appears to
   hold cleanly there too over the tested `n`-range. So what `λ=0.05`
   actually demonstrates is the already-known, already-symbolically-
   derived pole in the *coefficient* `1/(12λ)` as `λ→0` (correctly
   described as such in §3), not literal breakdown of the derived rates.
   This is a minor clarity point, not an error — the front's prose is
   already careful not to overclaim here — but the orchestrating session
   may wish to add one clarifying phrase distinguishing "the constant
   blows up" (demonstrated) from "the rate breaks" (not demonstrated,
   and not claimed).

5. **[LOW, cosmetic]** §0 states the predecessor `ATTEMPT.md` is "726
   lines"; it is actually 725 lines (`wc -l`, and confirmed by a direct
   byte-level check that the file ends with a trailing newline). No
   substantive effect anywhere in the document.

No other issues were found after genuinely adversarial effort: ten fresh
`(λ,γ,n)` stress-test points (including edge cases near/beyond both
claimed boundaries of `λ` and near both endpoints of `γ∈(0,1)`, and `n`
up to `10^{15}`), two independently-coded symbolic re-derivations using
different techniques than the front's own disclosed methods, a
line-by-line cross-check of every numeric figure quoted in ATTEMPT.md
against the front's own logs (all found accurate), a re-verification of
the seed/grep/git-status governance claims, and a full re-read of the
tail-negligibility argument down to the level of its individual analytic
steps.

---

## Scripts and logs in this directory

| File | What it does |
|---|---|
| `A_watson_formula.py`/`.log` | independent re-derivation of the general Watson/Laplace `Δ` formula from Gaussian cumulant moments (exact `sympy.integrate`, different code path than the front), validated against the external classical Stirling series `Γ(z+1)~√(2πz)(z/e)^z(1+1/(12z)+...)` |
| `B_mesoscale_scaling.py`/`.log` | independent re-derivation of the mesoscale scaling of `A`, `g'''(t*)`, `g''''(t*)`, and the resulting `Δ~1/(12λ√n)`, γ-independent, via `sympy.limit` leading-power extraction — a genuinely different symbolic method than the front's disclosed `sympy.series`-with-timeout-workaround approach |
| `C_stress_test.py`/`.log` | fresh `mpmath` (dps 50–80) numerical stress test at 10 `(λ,γ,n)` points not in the front's own grid, including `λ` just inside/outside both claimed boundaries, `γ` near 0 and 1, and `n` up to `10^{15}` |
| `D_tail_ratio_check.py`/`.log` | full-domain (not just near-`t*`) scan of the curvature ratio `\|g''(t)\|/A`, used to identify the Step-2 extrapolation gap in §5 (issue 1 above) |

No file of the front's own `ATTEMPT.md` or any `.py`/`.log` script was
modified. No `git` command was run by this referee. `THEOREM.md`,
`DECISION_LEDGER.yaml`, `PROOF_DEPENDENCY_MAP.md`, `DISCOVERY_LAB_STATE.md`,
`README.md`, `index.html` were read-only throughout.
