# Adversarial referee report — D-SHARP-RATE-CONSTANTS-ATTEMPT

**Target:** `.../general_k_joint_attempt/sharp_rate_constants_attempt/ATTEMPT.md`
(wave 25, front a, `DISC-DEC-118`).

**Method.** All core numeric/symbolic claims (items 1-4 of the mandate)
were independently re-derived from scratch in sympy — starting only from
THEOREM.md's Estágios 40/42/43 prose (Proposições D2/D3/D4, hand-
transcribed by the referee, never copy-pasted from the front's own
`lib_cdf.py`) — **before** any of the front's own `.py` scripts were
opened. Only after completing the independent derivations did this
referee read the front's scripts, to check the two self-disclosed bugs,
scope discipline, and general code quality. Nine independent scripts were
written (`adv_k2.py`, `adv_k3.py`, `adv_k4.py`, `adv_k3_tailbound.py`,
`adv_k4_tailbound.py`, `adv_mc.py`, plus their logs) — see the file
manifest at the end.

## Verdict: **SOUND WITH NAMED ISSUES — ACCEPT for catalogue**

No mathematical error was found in any proved bound, constant, or formula
in this document. Every numeric claim independently checked — `M_2`,
`M_3`, `M_4`, `C_3`, `C_4`, the K=2 full-closure theorem, both exhaustive-
window claims, the Monte Carlo worst-cases, and all seven exact boundary
values — matched the front's own reported figures to the full precision
tested (typically 20-30 significant digits, several to exact rational
equality). One MODERATE and two LOW/informational issues are named below;
none of them invalidates any proved result.

**The THEOREM.md Estágio 42 error claim (mandate item 4): CONFIRMED, YES,
this is a genuine, valuable correction.** See §4 below.

---

## 1. K=2 — full closure at the exact asymptotic constant: CONFIRMED

Independently re-derived from Proposição D2 (`k(k+1)(2n²-3n+k-k²)/[n³(n-1)]`,
transcribed by hand from THEOREM.md line 6262), substituting `k=nx` and
subtracting `F_2(x)=1-(1-x²)²`:

- `Δ_n(x)` matches the front's cited intermediate form exactly (`sp.simplify`
  difference = 0).
- `n·Δ_n(x) → g_1(x) = 2x-x²-x⁴` as `n→∞`, confirmed both by direct
  `sp.limit` and by the polynomial-degree/leading-coefficient method —
  zero symbolic difference between the two independent routes.
- `g_1'(x)=0` solved via `sp.Poly(g_1',x).real_roots()` (not `solve()`,
  per the mandate's own caution): unique interior root
  `x*=0.589754512301458384278801747096...`, confirmed **identical** to
  the real root of `2t³+t-1=0` found independently via
  `Poly(2t³+t-1,t).real_roots()`. **Confirmed the root-vs-value
  distinction the mandate flagged**: the cubic's root *is* `x*` (the
  argmax location), a different number from `M_2=g_1(x*)`, which is the
  function value there.
- `M_2 = g_1(x*) = 0.710726576062222062064...`, matching the front's
  claimed `0.71072657606222206206` to the 21st digit tested
  (difference `≈4×10⁻²¹`, i.e. exact at the precision either side
  carries).
- Re-derived the elementary sign argument from scratch: `g_1≥0` on
  `[0,1]` (factor `x(2-x-x³)`, `2-x-x³` strictly decreasing, `=0` at
  `x=1`); `p(x)=-x⁴-x≤0`, min `p(1)=-2`; threshold
  `n≥1+2/M_2=3.81402...⟹n≥4` — reproduced exactly.
- Direct numeric spot-check of `|Δ_n(x)|≤M_2/n` on a 2001-point grid at
  `n=4,5,10,50`: zero violations, worst ratios 0.938/0.771/0.893/0.980
  (all `<1`).

**Independently confirmed: this is a genuinely correct, sharp, PROVED
bound for all `n≥4`, not just numerically plausible.**

## 2. K=3 — near-sharp closure: CONFIRMED

- `g_3(x)` re-derived independently from Proposição D3 as
  `n→∞`: `3x⁶-3x⁵-3x²+3x`, confirmed identical to the front's factored
  form `3x(x-1)²(x+1)(x²+1)` (zero symbolic difference) — this referee
  did **not** just trust the factorization, it re-expanded and compared
  against the independently-limit-derived polynomial.
- `M_3 = 0.712071558138027808419...` via `real_roots()`, matching the
  claimed `0.71207155813802780842` to 21 digits; `x*=0.452192150454258926538...`
  matches exactly.
- **Exhaustive-window spot-check, 21 scattered `n` in `[6,999]`**
  (`6,7,8,10,13,20,29,45,63,90,130,180,250,333,420,555,650,777,888,950,999`):
  for each `n`, this referee independently computed the *exact*
  `sup_x|Δ_n(x)|` via its own critical-point calculus on the D3 formula
  (not reusing the front's partial-fraction machinery), multiplied by
  `n`, and compared to `C_3=0.71833358218612400080`. **Zero violations.**
  The `n=999` case reproduced the front's own reported worst-ratio
  (`0.98939`) and `n·sup=0.7107098948` essentially digit-for-digit.
- **Independently re-derived the analytic tail-bound partial-fraction
  decomposition from scratch**, via an undetermined-coefficients ansatz
  distinct from both the front's own method (`sp.apart` cross-checked
  against ansatz-and-solve) — `B(x)=x-x²`, `C(x)` (deg 6), `D(x)` (deg 6)
  all matched the front's claimed forms exactly; `B_max=1/4`, `C_max=0`,
  `D_max=3` all reproduced exactly. Reconstructing
  `C_3=M_3+1/(4·1000)+6/998` from these independently-derived
  coefficients gives `0.718333582186124000803874...`, matching the
  front's claimed value to 21 digits. **This validates the extension of
  the bound to all `n≥1000`, not just the window this referee directly
  swept.**

## 3. K=4 — near-sharp closure: CONFIRMED

- `g_4(x)` re-derived independently from Proposição D4 as `n→∞`:
  `-6x⁸+8x⁷+6x⁶-12x⁵+6x⁴-6x²+4x`, exact symbolic match to the front's
  cited form.
- `M_4` found two independent ways: (i) `Poly(g_4',x).real_roots()` on
  the degree-7 derivative — one interior root
  `x*=0.369886566100883325779927...`, `M_4=0.708718393409321614178660...`;
  (ii) a fully independent 200,000-point `mpmath` dense-grid argmax
  search, landing on `x≈0.369885`, `value≈0.7087183934` — agreeing with
  the algebraic answer to the grid's own resolution. Both match the
  claimed `0.70871839340932161418` to 21 digits. Also independently
  confirmed (as the front honestly disclosed) that `g_4` has **no clean
  hand factorization** — verified `g_4≥0` on `[0,1]` via exact real-root
  count (only roots are the endpoints `x=0,1`), the same honest,
  non-elegant-but-rigorous method the front used.
- **Exhaustive-window spot-check, the same 21 scattered `n`**: zero
  violations against `C_4=0.7345569184500456912259`; `n=999` reproduces
  the front's own reported figures (`ratio=0.96188727`,
  `n·sup=0.7065609492`) essentially exactly.
- **Independently re-derived the 5-term partial-fraction decomposition**
  (`B(x)/n+B̄(x)/n²+C(x)/(n-1)+2D(x)/(n-2)+3E(x)/(n-3)`) from scratch via
  undetermined coefficients: all five polynomials matched the front's
  implicit forms; `B_max=1.633879883...`, `B̄_max=1/2`, `C_max=0`,
  `D_max=12`, `E_max=0.051860272...` all reproduced exactly (matching
  the front's rounded figures `1.6339`, `0.5`, `0`, `12`, `0.0519`).
  Reconstructing `C_4` at `N_0=1000` from these gives
  `0.734556918450045691225924791237`, matching the front's claimed
  value to 24 digits.

## 4. THEOREM.md Estágio 42 error claim: **CONFIRMED — genuine, correctly
diagnosed error; a valuable catch**

(a) **Text exists exactly as described.** `grep -n '0{,}167' THEOREM.md`
hits line 6280 (Estágio 42): *"a constante assintótica mais afiada do
limitante de convergência (`\approx0{,}167/n`, correspondendo ao `12/n`
observado numericamente como o pior caso real) não foi provada..."* — the
brace-escaped LaTeX comma is real; a naive `grep '0,167'` genuinely finds
nothing (independently confirmed both ways).

(b) **`0.7107` is the mathematically correct value, not `0.167`.** This
referee's own from-scratch derivation in §1 above (independent of the
front, independent of THEOREM.md's own prose) gives
`M_2=0.71072657606222...` as the true `n→∞` leading rate constant for
`K=2`. Cross-checked two further independent sources, both read directly
by this referee (not taken on the front's word):
  - `k2_full_cdf_attempt/ATTEMPT.md` itself states `≈0.7107/n` / `≈0.711/n`
    at **four** separate locations (lines 83, 576, 703, 794).
  - `k4_full_cdf_attempt/ATTEMPT.md`'s own cross-family comparison (line
    653) states "consistent in magnitude with D2's `≈0.7107`".

  `0.167` appears nowhere in either sibling document as a claimed K=2
  rate constant.

(c) **Origin-tracing verified precise, not coincidental.** Computed
`|Δ_4(1)|` directly from the D2 formula (independent re-derivation, §1):
`Δ_4(1) = -1/6` exactly, so `|Δ_4(1)|=1/6=0.1666...`. And
`2/(4·3)=1/6` exactly. **This is an exact rational identity, not an
approximate numerical coincidence** — confirmed via `sp.Rational`
equality, not float comparison. The front's diagnosis — that `0.167` is
the finite-`n=4` boundary-extrapolation value, conflated with the
`n→∞` asymptotic constant — is precisely, not just plausibly, correct.

**Bonus finding (not requested, discovered during scope-discipline
mtime checks, §6 below): the same erroneous `0,167/n` figure has also
propagated into `DECISION_LEDGER.yaml`'s own `DISC-DEC-118` mandate
text** (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, the
"(a) D-SHARP-RATE-CONSTANTS-ATTEMPT" line, `~0,167/n` alongside the
correct `~0,712/n` and `~0,7087/n` for K=3/K=4). This independently
confirms the front's own §0 remark that "`DECISION_LEDGER.yaml`... which
inherited the same figure into this front's own mandate text" is
accurate — the error is not confined to one prose sentence in THEOREM.md
but was copied into the governance ledger's own wave-25 authorization.
Both should be corrected together.

**Conclusion on item 4: yes, confirm the error. This is a legitimate,
rigorously-traced correction to a previously-referee-accepted THEOREM.md
passage, and should be treated as a positive finding about this front's
diligence, not a defect in its own work.**

## 5. Self-disclosed bugs

### Bug 1: `sp.solve()` silently dropping real roots (nested-radical /
`CRootOf` forms) — **diagnosis confirmed real; fix confirmed INCOMPLETE**

Independently reproduced the exact phenomenon on `g_3'(x)` (K=3's
quintic derivative): `sp.solve()` returns 5 solutions, 4 of them deeply-
nested radicals with `.is_real == None`; a naive `[s for s in sols if
s.is_real]` filter keeps only `x=1` (value `0`), **silently dropping**
the two real roots `x≈-0.715` and `x≈0.452` (the true interior maximum)
that `Poly(...).real_roots()` correctly finds. This would indeed produce
the absurd `M_3=0` the front describes. **Confirmed real, confirmed
correctly diagnosed.**

**However**: the fix is described in ATTEMPT.md §6 as applied "throughout
every script in this front (`k2_sharp_rate.py`'s `exact_sup_abs_delta`
helper likewise switched, for consistency...)". **This is not accurate.**
`k2_sharp_rate.py`, as it exists on disk (the version that produced the
cited `k2_sharp_rate.log` and all of §3's numbers), contains **zero**
calls to `real_roots()` and **four** calls to `sp.solve()` combined with
the exact naive `.is_real` filter pattern that caused the K=3 bug (lines
85-90, 110-111, 136-139, 256-260) — including inside `exact_sup_abs_delta`
itself (line 136-139), the very function the prose names as fixed.
`k3_sharp_rate.py`, `k4_sharp_rate.py`, `k3_full_window_closure.py`, and
`k4_full_window_closure.py` **do** correctly use a shared
`real_roots_in()` helper throughout (confirmed by reading each) — only
`k2_sharp_rate.py` was actually missed.

**Does this corrupt any result?** No — independently checked. Every
polynomial `sp.solve()` is called on in `k2_sharp_rate.py` (`g_1'`, `p'`,
and the per-`n` `Delta_n(x)` derivative in `exact_sup_abs_delta`) is a
**cubic with exactly one real root**; the two `is_real=None` roots in
each case are *genuinely* complex (confirmed by comparing against
`real_roots()` output — identical single-real-root set every time), so
the naive filter happens to keep the correct root by mathematical luck,
not code robustness. This referee's fully independent `real_roots()`-
based re-derivation (§1) matches `k2_sharp_rate.py`'s `solve()`-based
numbers exactly, confirming **no numerical error resulted this time**.

**Severity: MODERATE.** Two distinct problems, both real: (i) a false
factual claim in ATTEMPT.md §6 about what the shipped code does; (ii) the
exact bug-prone pattern the front identified as dangerous is still live
in one file, un-triggered here only because K=2's polynomials happen to
be single-real-root cubics — a fragile state, not a robust fix. Not HIGH
because no cited number is actually wrong (independently verified) and
not LOW because the document makes a specific, checkable, false claim
about its own code that a reader would reasonably rely on.

### Bug 2: `monte_carlo_bonus.py` missing `n`-substitution / avoided
float catastrophic-cancellation — **confirmed real, confirmed correctly
fixed**

Read the final `monte_carlo_bonus.py` in full. Confirms: `DELTA_EXPR[K]`
retains both symbols `n` and `x`; the sampling loop calls
`expr.subs({n: sp.Integer(nn), x: xx})` — **both** symbols substituted,
`xx` an exact `sp.Rational`, `nn` an arbitrary-precision Python int cast
to `sp.Integer` — exactly the fix the prose describes, with no
`lambdify`/float path anywhere in the numerator/denominator evaluation;
only the final ratio (`sp.N(..., 50)`) touches floating precision, after
the exact computation. This structurally rules out the described
catastrophic-cancellation failure mode (`n^6~10^36` terms cancelling to
`~10⁻⁶`) for `K=4`, `n` up to `10⁶`.

**Independent reproducibility check** (`adv_mc.py`): reran the identical
Monte Carlo procedure with the front's own reserved seeds
(`20260929001/002/003`), using this referee's own from-scratch `Delta`
expressions (not the front's `lib_cdf.py`) and the front's claimed
`C_2,C_3,C_4` constants. Result: **exact reproduction** of the front's
own reported worst-case `(n,x)` pairs and ratios —
`(697419, 18427/31250)→0.9999985309` (K=2),
`(833191, 112933/250000)→0.9912791521` (K=3),
`(888271, 184709/500000)→0.9648196284` (K=4), zero violations in all
3000-sample runs each. This is strong evidence the RNG/seed discipline
and the exact-arithmetic pipeline are both genuinely reproducible and
correct, not just internally self-consistent.

**Severity: none (informational PASS).**

## 6. Scope and seed discipline

- **`grep -rn "git"` across all `.py` files in the front's directory**:
  zero shell/git-command hits (the three hits found are all inside code
  comments discussing floating-point precision, not commands). No
  `subprocess`/`os.system`/`os.popen` calls anywhere.
- **Seeds**: `grep` confirms exactly `20260929001/002/003` used, all
  inside the reserved block `20260929000-20260929999`; nothing outside
  the block found.
- **`THEOREM.md` mtime**: `2026-08-28 23:31:01` — strictly *before* the
  front's own working window (`2026-08-29 01:48-02:14`, from its own
  file mtimes). Confirms `THEOREM.md` was not touched during this
  front's work.
- **`DECISION_LEDGER.yaml` mtime**: `2026-08-29 02:07:27` — this
  *does* fall inside the front's working window (LOW/informational,
  flagged for transparency since the mandate specifically asked for an
  mtime check). However: `grep`-ing every `.py` file in the front's
  directory for `DECISION_LEDGER` or any `open(...)` call targeting a
  path outside the current directory finds **none** — every `open()` in
  every script (11 total) writes/reads only its own local
  `.log`/`.txt`/`.pkl` file, by bare filename, in the working directory.
  There is no code path in this front's scripts capable of touching the
  ledger. `DISC-DEC-118`'s own text describes "4 frentes paralelas"
  authorized in the same wave, and this front's own §0 independently
  states the erroneous `0,167` figure was *inherited* into (not written
  by) its mandate text — both consistent with the ledger mtime being
  explained by concurrent orchestrator-level activity (other wave-25
  fronts reporting, or ledger entry finalization), not a scope violation
  by this front. **Not scored as a finding against this front** — noted
  only because the mandate asked for the check.
- `DISCOVERY_LAB_STATE.md` mtime (`02:07:35`) is likewise inside the
  window but for the same reason (no script in this front opens it by
  write path — the front's own claim is a single read for a seed-
  reservation grep, consistent with no mtime-changing access).
- Sibling `ATTEMPT.md` files (`k2_full_cdf_attempt`, `k3_full_cdf_attempt`,
  `k4_full_cdf_attempt`) all have mtimes well before the front's window
  (`2026-08-28`, hours earlier) — consistent with "read but not
  modified."
- **`k3_full_cdf_attempt/ATTEMPT.md`'s own "22 vs 62" typo claim**
  (cited by this front in §1): independently read lines 488-502 of that
  file. Confirmed exactly as described — line 492 derives and states
  `22/n`, line 502 (same paragraph) refers to "the crude `62/n` bound".
  A real internal typo in that other document, correctly identified by
  this front, not a fabrication.

## 7. General failure-mode hunt

- **Fabrication**: none found. Every headline number was independently
  reconstructed via at least one method wholly independent of the
  front's own code (hand-transcribed source formulas, from-scratch
  sympy derivations, an independent partial-fraction ansatz, an
  independent Monte Carlo rerun with the same seeds). All matched.
- **Executive-summary vs. detailed-derivation consistency**: no
  discrepancy found. §0's "full closure, exactly at the pure asymptotic
  constant" claim for K=2 is justified by the elementary sign argument
  in §3 and matches the Scorecard (§8, item 3: PROVED). The "near-sharp,
  not exact" framing for K=3/K=4 is stated consistently in §0, §4, §5,
  §7, and the Scorecard (item 11: "NOT ACHIEVED — structural obstruction
  named precisely") — never silently upgraded to "exact" anywhere in the
  document.
- **Overclaim check**: none found beyond the one documentation
  inaccuracy in §5 above (which is about code-vs-prose, not about the
  proved mathematical results).
- **Boundary-value spot checks** (not explicitly requested but cheap and
  worthwhile): independently recomputed all seven claimed exact boundary
  values — `|Δ_2(1)|=1`, `|Δ_3(1)|=1/3` (K=2); `|Δ_3(1)|=1`,
  `|Δ_4(1)|=1/4`, `|Δ_5(1)|=1/10` (K=3); `|Δ_4(1)|=1`, `|Δ_5(1)|=1/5`
  (K=4) — all match exactly, including the front's own noted "log prints
  signed values" cosmetic detail.

## 8. Findings summary

| # | Finding | Severity | Affects any proved result? |
|---|---|---|---|
| F1 | `ATTEMPT.md` §6 claims `k2_sharp_rate.py`'s `exact_sup_abs_delta` helper was "switched to `real_roots()`... for consistency"; the shipped file still uses `sp.solve()`+naive `.is_real` filtering throughout (0 `real_roots()` calls, 4 `sp.solve()` calls). The exact bug-prone pattern the front itself flagged as dangerous remains live in this one file, untriggered only because K=2's relevant polynomials are all single-real-root cubics (independently verified). | **MODERATE** | No — independently re-derived every K=2 number via `real_roots()` from scratch; all match `k2_sharp_rate.py`'s `solve()`-based output exactly. |
| F2 | The correct sharper K=2 constant `≈0.7107/n` — confirmed independently in §1/§4 — is mis-stated as `≈0.167/n` not only in `THEOREM.md` Estágio 42 (already known to the front) but also in `DECISION_LEDGER.yaml`'s own `DISC-DEC-118` mandate text, which the front's front-matter inherited the number from. | **LOW / informational** (positive finding — confirms and extends the front's own §0 correction claim) | No — this is an error in THEOREM.md/DECISION_LEDGER.yaml, not in this front's own results. |
| F3 | `DECISION_LEDGER.yaml` and `DISCOVERY_LAB_STATE.md` mtimes fall inside this front's working window. No script in the front's directory contains any file-access path outside its own directory (grep-confirmed), consistent with the front's own read-only claim; most plausibly explained by concurrent orchestrator/ledger activity for the other parallel wave-25 fronts. | **LOW / informational**, not scored against the front | No |

No HIGH-severity findings. No mathematical result in this document was
found to be incorrect, unsupported, or overclaimed.

## 9. What this referee independently reconstructed (recap)

- K=2: `Δ_n(x)` in closed form; `g_1(x)=2x-x²-x⁴`; `M_2` via
  `real_roots()`, matched to 21 digits; the full elementary closure proof
  (sign facts, threshold `n≥4`); numeric spot-checks at `n=4,5,10,50`.
- K=3: `g_3(x)` and its factorization; `M_3` via `real_roots()`, matched
  to 21 digits; a from-scratch exhaustive-window spot-check at 21
  scattered `n∈[6,999]` (zero violations, exact match to front's `n=999`
  figures); an independent 3-term partial-fraction decomposition
  (`B,C,D` all matched exactly) reconstructing `C_3` to 21 digits.
- K=4: `g_4(x)`; `M_4` via both `real_roots()` and an independent
  200,000-point numerical grid search, matched to 21 digits; the same
  21-point exhaustive-window spot-check (zero violations, exact match to
  front's `n=999` figures); an independent 5-term partial-fraction
  decomposition (`B,B̄,C,D,E` all matched exactly) reconstructing `C_4`
  to 24 digits.
- The THEOREM.md Estágio 42 `0,167` error: text location confirmed;
  correct value `0.7107` independently confirmed three ways (own
  derivation + two sibling documents read directly); origin-tracing
  (`|Δ_4(1)|=1/6` exactly) confirmed as an exact rational identity;
  additionally found the same error propagated into
  `DECISION_LEDGER.yaml`.
- Both self-disclosed bugs: Bug 1 (`solve()` dropping real roots)
  independently reproduced and confirmed correctly diagnosed, but its
  claimed fix is incomplete (`k2_sharp_rate.py` unfixed, F1 above); Bug 2
  (Monte Carlo missing substitution / precision trap) confirmed correctly
  fixed, with an independent seed-for-seed rerun reproducing the front's
  exact reported worst cases.
- Scope/seed discipline: confirmed clean (no git, no shell-outs, seeds
  within reserved block, `THEOREM.md` untouched; ledger/state-file mtime
  overlap explained and not attributable to this front's own code).

## 10. File manifest (this referee's own work, `adversarial/`)

| File | Role |
|---|---|
| `adv_k2.py` / `.log` | Independent K=2 derivation: Δ_n(x), g_1(x), M_2 via `real_roots()`, elementary sign-argument re-derivation, n≥4 threshold, numeric spot-checks n=4,5,10,50 |
| `adv_k3.py` / `.log` | Independent K=3 derivation: g_3(x), M_3, 21-point exhaustive-window spot-check n∈[6,999] |
| `adv_k4.py` / `.log` | Independent K=4 derivation: g_4(x), M_4 (real_roots + independent grid search), 21-point exhaustive-window spot-check n∈[6,999] |
| `adv_k3_tailbound.py` / `.log` | Independent re-derivation (undetermined-coefficients ansatz) of the K=3 3-term partial-fraction decomposition and reconstruction of C_3 |
| `adv_k4_tailbound.py` / `.log` | Independent re-derivation of the K=4 5-term partial-fraction decomposition and reconstruction of C_4 |
| `adv_mc.py` / `.log` | Independent Monte Carlo rerun, front's own seeds, this referee's own Delta expressions — reproduces the front's worst-case (n,x) pairs and ratios exactly |
| `REFEREE_REPORT.md` | This report |

No file outside `adversarial/` was created or modified by this referee.
No `git` command was run.
