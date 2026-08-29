# Hostile referee report — `GAMMA-STIRLING-MFACT-UNIFORM-ATTEMPT`
# (wave 33, front (a), `DISC-DEC-148`)

## VERDICT: **SOUND** — no error found after genuine adversarial effort

Every central mathematical claim of this front was independently
re-derived from primary/cited definitions, using fresh scripts written
without importing or copying the front's own code, and — where the task
mandate asked for it — via methods genuinely different from the front's
own two internal cross-checks (`sympy.series` and `sympy.limit`). **No
mathematical, numerical, or bookkeeping error was found anywhere in this
front's central claims.** Six independent scripts (below, `adversarial/
ref01`–`ref05` + `ref03b`) reproduce, from scratch, the exact
factorization `term_m = F·I`, the closed form `K(λ,γ)=3λ/2−λ³/6−1/(12λ)
−λ/γ`, the exact vanishing of all lower-order (`ε^{-4}`…`ε^0`)
coefficients, the `1/(12λ)`-pole cancellation against the CITED
predecessor `Δ`, the central `−0.5→−1.0` before/after slope improvement
on a completely fresh `(λ,γ,n)` grid pushed to `n=10^{10}`, and the
`γ→0` unboundedness of `Δ_m`. One LOW-severity process issue is noted
(self-disclosed by the front, confirmed harmless) and one LOW-severity
observation about reproducing a disclosed computational obstacle. No
MODERATE or HIGH issues found.

`C(γ)` remains entirely open, as this front itself states throughout; no
claim of progress on any Millennium Prize Problem was made or is endorsed
here — this is pure combinatorial/asymptotic mathematics about a specific
random-permutation-with-reroutes ensemble (`u12_universality`), internal
to this archive.

---

## 0. Method

Read in full, in the order specified by the dispatch: `THEOREM.md`
Estágio 56 and 57 (lines 7818–8047); the direct predecessor's full
`ATTEMPT.md` (636 lines, `gamma_c_gamma_uniform_watson_remainder_attempt`)
§1–§3, §6–§8; its own `adversarial/REFEREE_REPORT.md` (367 lines); the
grandparent `ATTEMPT.md` (725 lines) §1; and the front under review in
full (656 lines), together with all eight of its scripts (`01`, `02`,
`03`, `03b`, `03c`, `03d`, `04`, `05`) and their `.log` outputs.

Every check below was written and run independently, without reading the
front's own `.py` files before writing the corresponding referee script
(scripts were read afterward, to audit for bugs, per the mandate's item 6
— reading for audit is not the same as copying). Six fresh scripts are
saved in this `adversarial/` directory alongside this report, with their
logs.

---

## 1. Independent re-derivation of `F(n,m,γ)` (item 1 of the mandate)

**File:** `ref01_factorization.py` / `.log`

Built purely from the primary cited definitions (grandparent
`ATTEMPT.md` §1: `term_m:=(γ^m/n^m)·m!·T(n,m)`, `T(n,m)=C(n+m+1,2m+1)·
I(n,m,γ)/B(m+1,m+1)`, `B(m+1,m+1)=m!²/(2m+1)!`, `C(n+m+1,2m+1)=(n+m+1)!/
[(2m+1)!(n-m)!]`), independently of the front's own script `01`:

- **Symbolic** (`sympy`, exact): `term_m/I − F_claim` simplifies to
  exactly `0`.
- **Numeric** (exact `Fraction` arithmetic, 200 random `(n,m,γ)` triples
  on a grid disjoint from both the front's own grid and the dispatching
  session's earlier spot-check, deterministic seed for reproducibility
  only — no probabilistic method involved): max discrepancy exactly `0`.

**Confirmed independently**: `term_m(n,γ)=F(n,m,γ)·I(n,m,γ)`,
`F(n,m,γ)=(γ/n)^m(n+m+1)!/[(n-m)!m!]`, exactly as the front derives in
its own §1.

---

## 2–3. Independent re-derivation of `K(λ,γ)` and confirmation that the
## `ε^{-4}`…`ε^0` coefficients genuinely vanish (items 2–3 of the mandate)

**File:** `ref02_K_curvefit.py` / `.log`

The mandate asked for a *third*, genuinely independent method beyond the
front's own `sympy.series` (script `03`) and `sympy.limit` (script
`03d`). Implemented: **pure numeric curve-fitting**, with no symbolic
series/limit machinery at all. `B(n,m,γ):=\ln F+\ln I_{\mathrm{leading}}
-\ln T_{\mathrm{prof}}$ was evaluated at high `mpmath` precision (dps
150) with `m=λ\sqrt n$ CONTINUOUS (no integer rounding — `loggamma`
accepts real arguments, so this decouples the *asymptotic-expansion*
question from the *integer-m bookkeeping* question tested separately in
§5), at 7 values of `n$ in geometric progression spanning `n\sim10^{24}$
to `n\sim10^{46}$ (dps 150 supports this dynamic range safely), and an
exact linear system was solved (`mp.lu_solve`, a genuine Vandermonde-type
fit for the 7 unknown Laurent coefficients `c_{-4},\ldots,c_2$) — a
method with zero shared code or algorithm with either of the front's own
two routes.

Tested at 5 **fresh** `(λ,γ)` points, none matching the front's own grids
in scripts `03b`/`04`/`05`:

| `(λ,γ)` | max\|fitted `c_{-4..0}`\| | fitted `c_1` vs `K(λ,γ)` rel. err |
|---|---|---|
| `(1.0,0.5)` | `1.8×10^{-42}` | `1.08×10^{-26}` |
| `(0.5,0.3)` | `3.5×10^{-42}` | `1.42×10^{-26}` |
| `(2.0,0.7)` | `2.1×10^{-42}` | `7.57×10^{-27}` |
| `(0.3,0.9)` | `7.1×10^{-43}` | `1.92×10^{-26}` |
| `(1.5,0.2)` | `5.7×10^{-40}` | `4.40×10^{-25}` |

**Confirmed independently, by a method sharing no code with the front's
own two internal cross-checks**: the `ε^{-4}`…`ε^0` coefficients of
`B` are genuinely (numerically indistinguishable from exactly) zero, and
the leading `ε^1` coefficient matches the front's closed form
`K(λ,γ)=3λ/2−λ³/6−1/(12λ)−λ/γ` to `<5\times10^{-25}` relative accuracy —
five to six orders of magnitude tighter than the front's own `mpmath`
cross-check (`5.1\times10^{-5}$ at `n=10^{12}$, script `03b`), simply
because this fit can push `n$ far beyond what a direct high-`n` `mpmath`
evaluation can reach, being a fit rather than a limit-in-`n$.

---

## 4. Independent re-derivation of the `1/(12λ)` pole cancellation
## (item 4 of the mandate)

**Files:** `ref03_pole_cancellation.py` / `.log` (failed, disclosed
below), `ref03b_pole_cancellation_fast.py` / `.log` (succeeded)

A first attempt (`ref03`) re-derived the predecessor's own `Δ(n,m,γ)`
mesoscale limit via a single combined `sympy.series` call on the full
ratio `g''''/(8A²)+5(g''')²/(24A³)`, substituted at `m=λ\sqrt n$ —
**this independently reproduced the exact same computational wall the
predecessor front itself disclosed** (its own §3/§8 item 3: "a first
attempt... did not terminate within a 300-second timeout"): the referee's
own attempt was killed by a 250s timeout, confirming this is a genuine
`sympy` performance obstacle, not a fabricated excuse in either
document.

Following (independently, not copying) the same *strategy* the
predecessor disclosed — expand `A`, `g'''(t^*)`, `g''''(t^*)`
SEPARATELY (each terminates in under 1s) and combine algebraically —
`ref03b` succeeded in under 2 seconds and re-derived, from the
predecessor's own general Watson/Laplace formula (cited, not the
front-under-review's own construction):

`Δ_{\mathrm{pred}}(n,m,γ)\sim\dfrac{1}{12λ}\cdot\dfrac1{\sqrt n}`

— matching the CITED predecessor closed form exactly. Combined
symbolically with `K(λ,γ)`:

`K(λ,γ)+\dfrac1{12λ}=\dfrac{3λ}2-\dfrac{λ^3}6-\dfrac λγ` (symbolic
difference `0`), and `\lim_{λ\to0}\left[K(λ,γ)+\dfrac1{12λ}\right]=0`.

**Confirmed independently**: the `1/(12λ)` poles of `Δ_m` and the CITED
`Δ` cancel EXACTLY, matching the front's own §4 claim, re-derived from
the predecessor's own formula rather than by re-typing the front's
script `03c`.

---

## 5. Independent reproduction of the central before/after numerical
## deliverable (item 5 of the mandate)

**File:** `ref04_term_m_before_after.py` / `.log`

Written from scratch without reading the front's own script `04` before
writing this one (read only afterward, for the audit in §6 below). Uses
`term_m(n,γ)=e^{\ln F(n,m,γ)}\cdot I_{\mathrm{exact}}(n,m,γ)`, `F` via
`mpmath.loggamma`, `I_{\mathrm{exact}}` via adaptive `mpmath` quadrature
(dps 50) with breakpoints seeded at `t^*\pm18/\sqrt A`, integrand
evaluated relative to its own peak (`\exp[g(t)-g(t^*)]`) to avoid
cancellation — independently re-implemented, same general technique
disclosed by both predecessor and front-under-review as necessary for
this narrow-peaked integrand.

Four **fresh** `(λ,γ)` points, none overlapping the front's own 6-point
main grid or 3-point extended push: `(0.7,0.6)`, `(1.2,0.4)`,
`(2.5,0.55)`, `(0.4,0.65)`, each pushed to `n=10^{10}` across 7 decades:

| `(λ,γ)` | leading/Δ-only slope (large `n`) | `Δ+Δ_m` slope (large `n`) |
|---|---|---|
| `(0.7,0.6)` | `→−0.500` | `→−1.000` |
| `(1.2,0.4)` | `→−0.500` | `→−1.000` |
| `(2.5,0.55)` | `→−0.500` | `→−1.000` |
| `(0.4,0.65)` | `→−0.500` | `→−1.000` |

At every fresh point, the local log-log slope of `Δ+Δ_m`'s relative
error converges cleanly to `−1.000` by `n\sim10^6$–`10^7$ and stays
there through `n=10^{10}$, while `leading` and `Δ`-only both remain
pinned at `−0.500` throughout — **exactly reproducing the front's
central claim on an entirely independent grid**, using an independently
written quadrature/anti-cancellation implementation.

---

## 6. Scrutiny of the self-caught λ-rounding bug (§8 item 1)

Read the actual committed `04_numeric_before_after_termm.py` and
`05_boundary_and_pole_cancellation.py` line-by-line (not just the
narrative). In both files, `errs_at(nn, lam_target, gam)` uses
`lam_target` ONLY to compute the rounded integer `m`; the ACTUAL
`lam = m/mp.sqrt(nn_mp)` is then computed and used consistently in every
subsequent call to `T_prof`, `Delta_predecessor`, and `Delta_m_this_
front` — `grep -n "lam_target"` across both files confirms `lam_target`
never reappears after the `m=round(...)` line. **The fix is genuinely and
consistently applied throughout the final committed scripts, not merely
in the narrative.** Scripts `03`/`03b`/`03c`/`03d` use continuous
(non-integer) `m=λ/ε` symbolically throughout, so this integer-rounding
bug class does not apply to them at all — checked, no analogous issue
present. No other numeric claim in the document appears to be affected by
a similar nominal-vs-actual mismatch.

---

## 7. Independent check of the `γ→0` boundary claim (§6)

**File:** `ref05_gamma_to_0_boundary.py` / `.log`

- **Symbolic**: `sympy.limit(K(λ,γ), γ, 0, dir='+')` returns `-oo` for
  fixed `λ>0` — confirmed independently that no other γ-dependent piece
  of `Δ`, `K`, or `T_prof`'s own `ε^1`-order structure offsets the
  `−λ/γ` term (the predecessor's `Δ` is exactly `γ`-independent,
  re-confirmed in §4 above; `T_prof`'s own `γ`-dependence is a
  leading-order, `ε^0` effect, a logically separate matter from `K`'s
  `ε^1`-order divergence).
- **Numeric** (independent curve-fit, same method as §2–3, fresh `γ`
  values `0.15, 0.08, 0.04, 0.02` at `λ=1` fixed): fitted `K` tracks the
  closed form to `<5\times10^{-23}` relative error at every point,
  confirming the `1/γ` growth exactly (`K(1,0.02)=-48.75$, independently
  matching the front's own script `05` log value `Delta_m=-4.875e-02` at
  `n=10^6$ exactly, since `-48.75/\sqrt{10^6}=-0.04875$).

**Confirmed independently**: the `γ\to0` boundary is real, unbounded,
and un-cancelled, exactly as the front claims, not merely asserted.

---

## 8. Governance/process check — the disclosed `git status --porcelain`

Ran `git log --format='%H %ad %s' -3` and `git status --porcelain` (and
`git diff --stat`) myself. Findings:

- The three most recent commits are the wave-33 authorization commit and
  two prior wave-32 closure commits — **no new commit exists from this
  front**, confirming the front never committed anything.
- `git diff --stat` is empty — **no tracked file was modified** by this
  front.
- `git status --porcelain` shows only new **untracked** directories: this
  front's own `gamma_stirling_mfact_uniform_attempt/`, the sibling wave-33
  front (b)'s own `gamma_outer_sum_poisson_attempt/` (pre-existing,
  unrelated to this front), and an unrelated pre-existing abandoned
  directory (`k3_full_cdf_attempt_ABANDONED_STALLED`) from a different
  lineage entirely.

**Confirmed**: the front's self-disclosed `git status --porcelain`
diagnostic call had zero actual effect on the repository — no commit, no
staged change, no push, no mutation of any kind. This is exactly what the
front's own disclosure claimed. **Severity: LOW** — a technical violation
of the "no git command of any kind" instruction (even a read-only one
should not have been run without the instruction anticipating it), fully
self-disclosed, zero actual harm. Recommend a dated nota, not a
correção, since nothing needs correcting — only the process norm needs
re-affirming for future fronts.

---

## 9. Scope-discipline / seed-block check

- `grep -rn "20260952" 05_DISCOVERY_LAB/` (run independently): matches
  ONLY the reservation lines in `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, and the front's own `ATTEMPT.md`'s citation
  of that same grep result — **zero matches in any script**, confirming
  the reserved seed block `20260952000–20260952999` was never used
  anywhere, exactly as claimed (deterministic `sympy`/`mpmath` throughout,
  no randomness).
- No file outside the front's own new `gamma_stirling_mfact_uniform_
  attempt/` subdirectory was modified (confirmed via `git diff --stat`
  above being empty and `git status --porcelain` showing only new,
  unrelated-lineage untracked directories).
- `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `README.md`, `index.html`, and every
  ancestor/predecessor `ATTEMPT.md`/`adversarial/` file: confirmed
  read-only (untouched by `git diff --stat`).

**No scope-discipline issue found.**

---

## 10. Overclaim/underclaim check

Compared the VERDICT-up-front language and the §11 scorecard against
what was actually established (as independently re-confirmed above):

- The verdict's specific numerical claims (log-log slopes `-0.500\to
  -1.000` at "every one of 9 `(λ,γ)` points... pushed to `n=10^{12}`")
  were checked directly against the front's own `04_numeric_before_
  after_termm.log` and match exactly (6 main-grid points + 3
  extended-push points = 9); independently re-confirmed on 4 fresh points
  in §5 above.
- The hedging language is appropriately calibrated, not overclaiming:
  "not a formal proof with an explicit universal constant" (§11, for the
  `O(n^{-1})` upgrade), "characterized numerically... not via a formal
  `ε`-`δ`-style uniform bound" (§10 item 5, for the `γ\to0` boundary) —
  both accurately describe the actual epistemic status of what was shown,
  which this referee's own independent numerics (§5, §7) corroborate
  rather than contradict.
- The claim that `K(1,0.8)=0$ "EXACTLY" (§5/§6 Part C) was independently
  hand-verified: `3/2-1/6-1/12-1/0.8=1.5-0.1\overline6-0.08\overline3-1.25
  =0` exactly — correct, not an overclaim.
- No place was found where the document's confidence language exceeds
  what was actually shown, nor any place where it understates a result
  that was in fact more strongly established than stated. The one
  disclosed self-caught bug (§8 item 1) is presented with accurate,
  specific severity language ("METHODOLOGY bug... not a flaw in the
  derived `Δ_m`/`K(λ,γ)` formula itself") — independently confirmed
  correct in §6 above (the formula was never wrong; only an early test
  harness was).

**No overclaim or underclaim found.**

---

## Issues found (all severities)

| # | Issue | Severity | Disposition |
|---|---|---|---|
| 1 | The front ran one read-only `git status --porcelain` diagnostic, a technical violation of its dispatch's "no git command of any kind" instruction — self-disclosed by the front itself. | **LOW** | Confirmed zero actual effect on the repository (§8 above: no commit, no staged change, no push). Recommend a dated nota on the front's own `ATTEMPT.md` (or the orchestrating session's integration note) re-affirming the norm; no correção needed since nothing was actually altered. |
| 2 | This referee's own first attempt at re-deriving the predecessor's `Δ` mesoscale limit via a single combined `sympy.series` call timed out at 250s. | **LOW / informational** | Not a flaw in the front under review — this independently *corroborates* the front's own and the predecessor's own disclosed `sympy` performance obstacle (predecessor's own §8 item 3, front's own §3 narrative) as a real, reproducible `sympy` behavior on this class of expression, not a one-off or fabricated excuse. Resolved by the disclosed separate-expand-then-combine workaround, independently re-implemented in `ref03b`, in under 2 seconds. |

No MODERATE or HIGH severity issues were found. No mathematical error,
no numerical discrepancy beyond expected precision limits, no
mis-transcription of any log figure into the prose, and no scope or
governance violation with actual effect were found anywhere in this
front's central claims, after genuine independent re-derivation of every
one of them (factorization, closed-form `K(λ,γ)`, vanishing of all lower
Laurent orders, pole cancellation, the central before/after numerics on a
fresh grid to `n=10^{10}$, the λ-rounding bug fix verified in the actual
committed code, and the `γ\to0` boundary) by methods substantially
independent of the front's own.

---

## Recommendation

**ACCEPT for catalogue.** `C(γ)` remains entirely open, as the front
itself states throughout and as this referee independently confirms is
not contradicted by anything found here. Item 2 of the Estágio 56/57 §7
diagnosis (the Stirling/`m!`-and-binomial-prefactor correction to the
FULL `T_{\mathrm{prof}}(λ,γ)`) is genuinely completed: `Δ_m(n,m,γ)=
K(λ,γ)/\sqrt n$, combined with the CITED predecessor `Δ(n,m,γ)`, upgrades
`T_{\mathrm{prof}}`-based approximation of the full `term_m(n,γ)` from
`O(n^{-1/2})$ to `O(n^{-1})$ accuracy, independently re-confirmed. Items
3 (outer-sum Euler–Maclaurin/Poisson treatment) and 4 (joint two-variable
assembly) remain untouched, exactly as scoped and assigned.

---

## Files in this directory

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `ref01_factorization.py`/`.log` | independent re-derivation of `term_m=F·I` from primary definitions, fresh grid |
| `ref02_K_curvefit.py`/`.log` | independent, series/limit-free numeric curve-fit re-derivation of `K(λ,γ)` and confirmation that `ε^{-4}`…`ε^0` coefficients vanish |
| `ref03_pole_cancellation.py`/`.log` | first (timed-out) attempt at re-deriving `Δ`'s mesoscale limit via combined `sympy.series` — kept, disclosed, superseded by `ref03b` |
| `ref03b_pole_cancellation_fast.py`/`.log` | successful independent re-derivation of `Δ`'s mesoscale limit and the `1/(12λ)` pole cancellation |
| `ref04_term_m_before_after.py`/`.log` | independent reproduction of the central before/after numerical deliverable, fresh `(λ,γ)` grid, `n` to `10^{10}` |
| `ref05_gamma_to_0_boundary.py`/`.log` | independent symbolic + numeric confirmation of the `γ→0` boundary claim |

No Millennium Problem claims anywhere; pure combinatorial/asymptotic
mathematics internal to this archive, about a specific
random-permutation-with-reroutes ensemble. This referee ran only
read-only `git log`/`git status`/`git diff --stat` commands (item 8's
governance check); no mutating git command was run.
