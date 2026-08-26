# REFEREE REPORT — `MCLUST-H1-VALIDITY-ATTEMPT` (wave 20, front c, `DISC-DEC-088`)

**Target:** `.../plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/
mclust_h1_validity_attempt/ATTEMPT.md`. Attacks `H1` (uniform validity of the
matched outer/inner asymptotic decomposition underlying the M-CLUST(b)
plateau's 4-term law), Tree B of `PROOF_DEPENDENCY_MAP.md`.

**Scope note.** This is pure combinatorics/asymptotic analysis internal to
the M-CLUST(b) plateau line (Tree B) — **not** a claim about, or adjacent
to, any Millennium Prize Problem. No such characterization appears anywhere
in the target document, and none appears in this report.

**Referee discipline.** No `.py` file belonging to this front or any front
in its lineage (`mclust_rigor` down through `mclust_h1_validity_attempt`,
inclusive of `mclust_plateau_abstract_real_gap_attempt` and
`plateau_resummation_attempt`) was opened, read, or imported at any point.
Every verification script in this directory (`ref01`–`ref11`) was written
fresh from the mathematical prose of the target `ATTEMPT.md` and its
required reading only. Required reading completed in full, in prose,
before any derivation: `PROOF_DEPENDENCY_MAP.md` §2 (Tree B, `FLOORH2` and
`PLATRESUM` nodes and both dated addenda under `PLATRESUM`); the full
`mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md` (721 lines,
especially §A.2–§A.4 and §B.5); the full `plateau_resummation_attempt/
ATTEMPT.md` (960 lines, especially §4, §4.5, §6). No randomness was needed
anywhere in this review (every check below is exact/deterministic
high-precision arithmetic), so the referee's reserved seed range
`20260895000–20260895999` was not drawn from.

---

## VERDICT

**SOUND, WITH TWO NAMED ISSUES OF NEGLIGIBLE SEVERITY (cosmetic/rhetorical,
not mathematical errors).** The target's central claims all independently
reverify:

1. The Watson-concentration lemma (§2.1) is genuinely airtight elementary
   real analysis, with no hidden gap — independently re-derived below and
   found correct in every step, including the self-caught S1 distinction
   (the lemma is *not* the naive `Phi(x0,inf)=W_inf(x0)`).
2. The reduction of `H1` to `(U1)+(U2)` (§2.2) is honestly scoped — it does
   not overclaim a proof of `H1`, and correctly identifies that `(U1)+(U2)`
   would suffice (via classical Watson's-lemma machinery) without claiming
   either is proved.
3. The exact ODE for `F(x)` (§2.3) is correctly re-derived from `(E1)`;
   the leading-order consistency check against `psi1'=x psi1-1` is
   correct. One minor logical redundancy is named below (Issue 1).
4. `psi3(0) = (7/2)sqrt(pi/2)` and `psi4(0) = -34/3` are independently
   confirmed to 60 correct digits via `mpmath` (dps=60), including an
   explicit check that the disclosed self-caught sign bug (S2) would have
   produced exactly the negative of the correct value, as claimed.
5. **The numerical uniformity grid claims are confirmed to a striking
   degree.** A from-scratch, independent implementation of the general-`s`
   `(P,Q)`-family series recursion (i) reproduces all 7 published anchors
   at `c=1000` to the same relative precision the front itself reports;
   (ii) reproduces the `resid3` cross-check values **`4.0580043...` and
   `4.1746489...`** at `c=1000,2560` — matching the front's own claimed
   values to every digit reported; (iii) reproduces the front's published
   `x=0` and `x=8` rows of the §4.2 eps→0 extrapolation table **to all 8
   published decimal digits, at both orders**, via an entirely independent
   `(K,dps)` sizing and fitting code path; (iv) independently confirms the
   monotonic-tightening-in-`x` pattern at these two endpoints.
6. The stress-test self-correction (§5) is independently reproduced:
   undersized `(K,dps)` genuinely produces catastrophic non-convergence
   (my own run: 0 stable digits, spurious ratio ~4e16) at `x=20,c=200`;
   corrected sizing genuinely converges (my own run: ~17-18 stable digits)
   to a ratio of **0.9833...**, matching the front's reported `0.983` to
   the reported precision.
7. No overclaim of proof, no Millennium Problem language, and no proposed
   replacement of any formula of record was found anywhere in the target
   document. The honest-non-closure framing throughout is accurate and, if
   anything, appropriately conservative given how strongly the numerics
   confirm the claims.

No computational error, no fabricated or unreplicated number, and no
material overclaim was found. The two named issues below do not affect
any conclusion, number, or the overall verdict of the target document.

---

## 1. Watson-concentration lemma (§2.1) — independently re-derived, SOUND

**Re-derivation (from scratch, matching the target's own proof structure
but worked independently before comparing).** From `(E2)`:

```
Phi(x0,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x0+v,y-v) dv
```

Split the `v`-integral at `v=G(delta)` for `y>2G(delta)` (so `y-v>G(delta)`
on the first piece, matching the `(U1)` window `x'∈[x0,x0+G(delta)]`,
`g'=y-v>G(delta)`):

- **First piece** (`v∈[0,G(delta)]`): by `(U1)`, `W(x0+v,y-v) =
  W_inf(x0+v)+O(delta)` uniformly on this range. Substituting and
  extending the `v`-integral of `W_inf` to `[0,inf)` introduces an error
  bounded by `sup|W_inf|*e^{-G(delta)/eps}` (the omitted kernel tail).
- **Second piece** (`v∈[G(delta),y]`): bounded in absolute value by
  `sup|W|*e^{-G(delta)/eps}` regardless of `y` — the kernel mass beyond
  `G(delta)` is exactly `e^{-G(delta)/eps}`, independent of how large `y`
  is. **This term is genuinely bounded, not zero, at this stage** — the
  document's own emphasis on this point is correct and important; it is
  exactly what distinguishes `(STAR)` from the naive collapsed-kernel
  claim.

Combining: for every `delta>0`, `|Phi(x0,y) - (1/eps)int_0^inf e^{-v/eps}
W_inf(x0+v)dv| <= O(delta) + O(e^{-G(delta)/eps})`, uniformly in `y` for
`y>2G(delta)`. Taking `y→inf` first removes the (separate, vanishing)
boundary term `e^{-y/eps}`; the bound above is then independent of `y`.
Taking `delta→0` (with `G(delta)→inf` at **fixed** `eps`, by the
definition of `(U1)`) sends both error terms to `0`. **This proof is
airtight modulo the stated hypotheses `(U1)` and boundedness of `W`; no
gap was found.** It is standard, careful real analysis — essentially a
kernel-concentration/dominated-convergence argument executed correctly.

**On the "not the naive statement" claim (self-caught S1).** Confirmed:
because `eps` is held **fixed** while `y→inf`, the exponential kernel
`e^{-v/eps}/eps` does not collapse to a point mass at `v=0` — it has fixed
spread `~eps` in `v` regardless of `y`. `(STAR)` is therefore a genuine
convolution over `v∈[0,inf)`, not the pointwise value `W_inf(x0)`; only a
**second**, separate limit `eps→0` (taken afterward, in §2.2) localizes
the integral near `v=0`. This distinction is correctly drawn and is not a
rhetorical flourish — it is exactly the content that makes `(STAR)`
nontrivial. The document's characterization of its own self-caught S1 bug
(an earlier draft concluding the naive `Phi(x0,inf)=W_inf(x0)`) is
consistent with this analysis: that earlier conclusion would indeed be
wrong for the reason stated.

**Verdict: SOUND, no gap found.**

---

## 2. Reduction of H1 to (U1)+(U2) (§2.2) — honestly scoped, SOUND

The claim that, given `(U1)+(U2)`, the classical rigorous Watson's-lemma
machinery (Olver, Ch. 2-3) applies to `(STAR)` is correct: `(U2)`
specifically supplies the uniform-in-`x` Poincaré expansion of the
integrand `W_inf(x;eps)` down to the boundary-layer scale `x=O(eps)`,
which is precisely the hypothesis classical Watson's lemma with explicit
error bounds needs. The document is careful to flag the genuine
complication (`W_inf` itself depends on `eps`, unlike the textbook
constant-integrand setting) rather than glossing over it.

**Honesty check.** The document states plainly, repeatedly, and in the
executive summary itself: "Neither `(U1)` nor `(U2)` is proved by this
front," and names the scale of what remains (a maximum-principle or
energy-estimate argument on the exact PDE system) rather than gesturing
vaguely. No claim anywhere suggests `H1` itself is closed by this
reduction. **This matches exactly what the task asked to check, and it
passes: the reduction is real (it replaces one monolithic informal
hypothesis with two independently falsifiable, more checkable ones) and
is not oversold as a proof.**

One very minor, purely rhetorical observation (not an error): the phrase
"`H1` ... is **exactly** the conjunction of `(U1)` and `(U2)`" claims an
equivalence, but what is actually shown is that `(U1)+(U2)` are
**sufficient** to recover the 4-term law rigorously via Watson's lemma;
necessity (that no other route to `H1` could avoid needing something
equivalent to `(U1)`/`(U2)`) is not, and could not easily be, established.
The qualifier "(as it concerns deriving `Pi(c)` via this route)" already
in the text largely defuses this, so it is **not counted as a named
issue** — it is appropriately hedged already.

**Verdict: SOUND, honestly scoped.**

---

## 3. Exact ODE for F(x) (§2.3) — re-derived independently, SOUND, one named issue

**Independent re-derivation**, starting from `(E1)`:
`Psi_x(x,y) = (x+y)Psi(x,y) - I(x,y)`, `I(x,y)=int_0^y Phi(x,y')dy'`.

Writing `I(x,y) = y F(x) + [I(x,y)-yF(x)]`, with `I(x,y)-yF(x) →
C(x)` by hypothesis (i):

```
Psi_x = (x+y)Psi - yF - [I-yF] = x Psi + y(Psi-F) - [I-yF]
```

This is pure algebra (distribute `(x+y)Psi`, regroup) — matches the
document's claimed decomposition exactly, no error.

Given hypothesis (ii) directly (`Psi(x,y)-F(x)=o(1/y)`), the middle term
`y(Psi-F(x)) = y·o(1/y) → 0`. Combined with hypothesis (iii)
(`lim Psi_x = F'(x)`) and hypothesis (i) (`I-yF → C(x)`):

```
F'(x) = x F(x) + 0 - C(x)   =>   F'(x) - x F(x) = -C(x)     (ODE-F)
```

**This final derivation is correct and does not depend on any
unstated assumption beyond (i), (ii), (iii) as given.**

**Named Issue 1 (severity: negligible/cosmetic).** The document's
intermediate "forced" sub-argument — "if `lim Psi(x,y)≠F(x)`, [the middle
term] diverges — a contradiction — so `lim Psi(x,y)=F(x)` is forced ... not
previously stated this way" — is presented as a new, independent
derivation, but it is **redundant with hypothesis (ii)**, which already
assumes `Psi(x,y)-F(x)=o(1/y)` (a stronger statement — a rate — than the
mere convergence `Psi(x,y)→F(x)` the "forced" argument establishes). The
actual derivation of `(ODE-F)` that follows uses hypothesis (ii) directly
("Given (ii), the middle term itself → 0"), not the "forced" sub-claim.
So this aside adds no new content beyond what `(ii)` already grants, and
the framing "not previously stated this way" mildly overstates its
novelty/independence. **This does not affect the correctness of
`(ODE-F)` or any downstream claim** — it is a labeling issue in one
paragraph, not a mathematical gap. Recommended fix (not required for
soundness): either drop the "forced" aside, or explicitly note it is a
corollary of (ii) rather than an independent derivation.

**Leading-order consistency check** (`psi1'=x psi1-1` matching `(ODE-F)`
at `F≈eps psi1`, `C≈eps·const` forcing `const=1`): re-verified
independently, correct.

**Verdict: SOUND, one cosmetic issue (does not affect correctness).**

---

## 4. Closed forms for psi3(x), psi4(x) (§3.3) — independently verified to 60 digits

Script: `ref01_psi_closed_forms.py` (log: `ref01_psi_closed_forms.log`).
`mpmath`, dps=60.

- `R(x):=sqrt(pi/2)*erfcx(x/sqrt2)` independently implemented via
  `e^{x^2/2}erfc(x/sqrt2)` and its `R'=xR-1` identity checked against
  numerical differentiation at 8 points: **agreement to ~60 digits**
  (residuals `~1e-60`).
- General variation-of-parameters formula `y(x)=-e^{x^2/2}int_x^inf
  e^{-t^2/2}f(t)dt` for `y'-xy=f(x)` independently re-derived (product
  rule + Leibniz differentiation-under-the-integral-sign) and confirmed
  algebraically equivalent to the record's own `R(x)` (with `f=-1`).
- **`psi3(0)` computed via the integral formula**: `4.38659948060425087...`
  vs. `(7/2)sqrt(pi/2) = 4.38659948060425087...` — **agreement to the
  full 60-digit precision (exact match at working precision)**.
- Direct numerical check that the integral form solves `psi3'=x psi3+7R'`
  at `x∈{0,0.5,1,2,3}`: residuals `<1e-60` at every point.
- **Sign check (self-caught S2)**: computed the version *without* the
  leading minus sign; got `psi3(0) = -4.38659948060425087...`, i.e.
  **exactly the negative of the correct value** — confirming the S2
  bug-and-fix narrative is precisely accurate, not embellished.
- `psi4(0) = (17/3)R'''(0)`, with `R'''` built via the closure identity
  `R''=R+xR'`, `R'''=2R'+xR''` (independently re-derived by differentiating
  `R'=xR-1` twice) and cross-checked against numerical 3rd-derivative of
  `R` directly: agreement to `~60` digits. Result: `psi4(0) =
  -11.333333... = -34/3` **exactly** (0 diff at working precision).

**Verdict: SOUND, exact numerical match on all four claimed identities.**

---

## 5. Numerical machinery and the uniformity grid (§3, §4) — independently rebuilt, SOUND

### 5.1 Fresh (P,Q)-family recursion, built from prose only

`ref02_family_series.py` implements the recursion described in the
target's own §0/§3.1 (transcribed there from the required reading, not
from any script): family elements `P(s)+Q(s)erfcx(s*sqrt(c/2))`, the
derivative closure `(P+QE)'=(P'-scQ)+(Q'+csQ)E` from `E'=csE-sc`, and the
descending-recursion/`kappa`-pinning solve for the bounded-branch `b_k`
ODE (worked out independently by hand before writing code: matching
`s^j` coefficients of `U'-csU=R` gives `(j+1)u_{j+1}-c u_{j-1}=r_j`,
solved descending from `j=deg(R)` down to `j=1` — using `u_{deg(R)}=0`
structurally — leaving the `j=0` relation `u_1=r_0` to pin `kappa`, using
that the antiderivative `V0` has `V0(0)=0` so `r_0=A_0+sc*kappa` exactly).

### 5.2 Anchor validation (`ref03_validate_and_resid3.py`/`.log`)

All 7 anchors quoted in the target's §3.2 reproduced, with relative
differences essentially identical to what the target itself reports:

| quantity | mine | target's own §3.2 | 
|---|---|---|
| a2(0) | reldiff 5.78e-14 | 5.8e-14 |
| a3(0) | reldiff 4.46e-14 | 4.5e-14 |
| a4(0) | reldiff 4.48e-14 | 4.5e-14 |
| b2(0) | reldiff 1.44e-12 | 1.4e-12 |
| b1(0) | exact (0) | exact (0) |
| Phi(0,0.002) | reldiff 2.68e-8 | 2.7e-8 |
| Phi(0,0.05) [plateau] vs 121-digit record | reldiff 2.2e-21 | 2.2e-21 |

**7/7 PASS, independently, matching the target's own reported precision to
within rounding of the last reported digit at every anchor.**

### 5.3 The decisive resid3 cross-check (`ref04_resid3.py`, `ref05_resid3_v2.py`/`.log`)

`ref04` (kept, undoctored) used `ct0=260` directly with only `dps=90`,
reproducing the SAME "order-2-entire cancellation" catastrophic
non-convergence the required-reading lineage documents for large `c*t0`
at insufficient `(K,dps)` — a useful independent confirmation, on its own,
that this cost structure is real and not an artifact of any one
implementation. `ref05` corrects this (smaller, safely-converged `ct0`,
two-`ct0` convergence check, `dps=100`) and computes:

```
resid3(c=1000) = 4.058004322924504...   (target's own claim: 4.0580043; record: 4.058)
resid3(c=2560) = 4.174648862393955...   (target's own claim: 4.1746489; record: 4.175)
```

**Matches the target's own claimed values to every digit reported.** This
is an independent confirmation via a genuinely different code path
(different polynomial-family bookkeeping details worked out from scratch,
different `(K,dps,ct0)` sizing) — strong evidence the target's §3.4 claim
of "exact match, to every digit the record itself published" is accurate,
not overstated.

### 5.4 General-`s` profile cross-check (`ref06_general_s_profile.py`/`.log`)

Since my `Fam.eval_at` supports evaluation at any `s`, not just `s=0`, I
also reproduced the grandparent document's published `F(s)` table at
`c=1000`, `x∈{0,0.5,1,2,3}` (§6 of `plateau_resummation_attempt/
ATTEMPT.md`) — **all 5 values match to ~1e-12 relative (limited only by
the published table's 12-digit display, not a discrepancy)**, and the
derived `(F-eps R)/eps^2` residual column matches the grandparent's own
published numbers digit-for-digit. This independently validates that the
general-`s` machinery (needed for the whole `(x,c)` grid, §4) is correct,
not just the `s=0` special case.

### 5.5 Spot-checking the (x,c) uniformity grid (§4.1–§4.2)

`ref07_grid_spotcheck.py`/`.log`, `ref08_redo_c200.py`/`.log`: computed
`ratio1`, `ratio2` at 6 individual `(x,c)` points drawn from the target's
own 42-point grid (`x∈{0,2,8}`, `c∈{200,1000,4000,8000}`), all lying
sensibly between 0 and 1 and trending toward 1 as `c` grows at fixed `x` —
qualitatively exactly as claimed. One point (`x=0,c=200`) initially failed
its own convergence self-check at modest `K` (only ~3 stable digits) —
**this is itself informative**: it independently confirms that `x=0`
combined with the smallest tested `c` is the hardest point in the grid
(matching the target's own account of the cost structure), and re-running
with larger `K=420` recovered ~20 stable digits and a sensible ratio.

**The decisive check** (`ref09_x0_row_extrapolation.py`/`.log`,
`ref10_x8_row_extrapolation.py`/`.log`): computed `ratio1`, `ratio2` at
**all 6** of the target's own `c`-values (`200,500,1000,2000,4000,8000`),
at `x=0` and `x=8` (the two extremes of the target's `x`-grid), and
performed the same per-`x` least-squares linear extrapolation to `eps=0`
described in the target's §4.2:

| x | order | my extrapolated ratio | target's ATTEMPT.md §4.2 table |
|---|---|---|---|
| 0 | 1 | **0.99303586** | 0.99303586 |
| 0 | 2 | **0.99166188** | 0.99166188 |
| 8 | 1 | **0.99953952** | 0.99953952 |
| 8 | 2 | **0.99932366** | 0.99932366 |

**Exact match to all 8 published decimal digits, at both orders, at both
tested x-values**, via a completely independent implementation, a
different `(K,dps,ct0)` sizing at each `c`, and an independently-written
extrapolation routine. This is about as strong an independent
confirmation of §4.1–§4.2's numbers as is achievable without literally
reproducing the target's own 42-point grid in full. The monotone
tightening-in-`x` pattern the target claims (`|1-extrap|` shrinking from
`x=0` to `x=8`) is independently reproduced at both orders:
`0.006964→0.000460` (order 1, mine) vs. `0.006964→0.0004605` (target);
`0.008338→0.000676` (order 2, mine) vs. `0.008338→0.0006763` (target).

**Verdict: SOUND. The uniformity grid claims are genuinely, independently
reproducible, not an artifact of one implementation's idiosyncrasies.**

---

## 6. Stress test at x=20 (§5) — self-correction independently reproduced

`ref11_stress_x20.py`/`.log`. At `c=200, x=20` (`s=1.4142`, past the
physical domain, matching the target's own stress point):

- **Undersized sizing** (`K=400, dps=60`, mimicking the target's own first
  pass): my own convergence diagnostic returns `relconv=1.0` (i.e.
  **zero stable digits** — total non-convergence) and a spurious
  `ratio1 ≈ 3.9×10^16`. This independently reproduces the qualitative
  "blow-up" the target reports (`~1.4×10^4`) as a pure numerical artifact
  of undersized `(K,dps)` at this point — the exact order of magnitude of
  the garbage differs (expected, since garbage-from-cancellation is not
  reproducible across different implementations), but the diagnosis
  (complete non-convergence, not a real finding) is confirmed
  independently.
- **Corrected sizing** (`K=800, dps=90`, matching the target's own §5.2
  rerun): converges cleanly (`relconv≈4.5e-18`, ~17 stable digits at that
  `K`) to `ratio1 = 0.983351314...`, matching the target's reported
  `0.983` to the precision stated.
- **Extra-margin run** (`K=1200, dps=130`): agrees with the `K=800` run
  to ~10 significant digits (`0.98335131 4...` vs `0.98335131 2...`,
  diverging in the 11th digit) — indicating the `K=800` value is stable
  to somewhat fewer digits than its own two-`ct0` approach-convergence
  diagnostic alone would suggest (that diagnostic captures approach-in-`t0`
  error but not residual `K`-truncation error at this extreme point). This
  is a technical observation about precision margins at the single most
  extreme grid point tested, **not a challenge to the qualitative or the
  3-significant-figure claim** — my own results confirm `ratio1≈0.9833-
  0.9834` robustly across two independent, well-separated `(K,dps)`
  settings, squarely matching the target's reported `0.983` and its claim
  that this point continues the same clean trend as the rest of the grid.

**Verdict: SOUND. The self-caught-and-corrected S3 narrative is genuine
and independently reproducible; the corrected numerical claim holds up.**

---

## 7. Overall honesty check (§6, §8, executive summary)

- No claim of a proof of `H1`, the 4-term law, or any formula of record
  is made anywhere in the target document; verified by a full read.
- No Millennium Prize Problem language, framing, or adjacency claim
  appears anywhere; the document's own explicit disclaimer (top of file)
  is accurate and the rest of the text is consistent with it throughout.
- The "what remains open" list (§8) accurately reflects what this referee
  independently found still open: `(U1)`/`(U2)` unproved, `(ODE-F)`
  hypotheses (i)-(iii) unproved and only leading-order-checked,
  trans-series content entirely untested, finite tested domain, `H2`
  untouched. Nothing in this referee's independent work contradicts any
  item on that list, and nothing found here should be added to it beyond
  the cosmetic Issue 1 above.
- The three self-caught issues (S1, S2, S3) were independently checked
  against the actual mathematics/numerics where feasible (S1: re-derived
  the correct lemma and confirmed the naive statement would indeed be
  wrong; S2: reproduced the exact sign-flip the bug would have caused;
  S3: reproduced both the undersized-sizing failure and the corrected
  recovery). **All three self-disclosures are accurate, not
  self-serving minimization of a bigger problem.**

---

## 8. Summary of issues found

| # | Location | Description | Severity | Affects any conclusion? |
|---|---|---|---|---|
| 1 | §2.3 | The "forced convergence `Psi(x,y)→F(x)`" aside is redundant with hypothesis (ii), already assumed; framed as a new derivation, it isn't independent of what's already granted. | Negligible / cosmetic | No — `(ODE-F)` itself is correctly derived directly from (i)-(iii) regardless of this aside. |
| 2 | §2.2 | "H1 ... is exactly the conjunction of (U1) and (U2)" claims an equivalence; only sufficiency is actually established (necessity is not, and is not easily establishable). Largely pre-hedged by the surrounding qualifier already in the text. | Negligible / rhetorical | No — no downstream claim relies on necessity, only sufficiency, which is correctly used throughout. |

No other issues — arithmetic, logical, or rhetorical — were found after
hostile, independent re-derivation of every checkable claim named in the
review mandate.

---

## 9. What was independently re-verified (summary)

1. Watson-concentration lemma (§2.1): full proof re-derived from scratch,
   confirmed airtight; the S1 naive-statement distinction confirmed
   correct.
2. Reduction to (U1)+(U2) (§2.2): confirmed honestly scoped, no overclaim.
3. Exact ODE for F(x) (§2.3): re-derived independently from (E1); final
   result confirmed correct; one cosmetic redundancy named (Issue 1).
4. psi3(0), psi4(0) closed forms (§3.3): confirmed to 60 digits via
   `mpmath`; S2 sign-bug narrative independently confirmed accurate.
5. Fresh general-`s` (P,Q)-family recursion: independently implemented
   from prose only; 7/7 published anchors reproduced at matching
   precision; resid3 values (4.058004..., 4.174649...) reproduced to
   every digit claimed; general-`s` F(s) profile table (5 points)
   reproduced to ~1e-12; two full rows (x=0, x=8) of the §4.2
   eps→0-extrapolation table reproduced to all 8 published digits at both
   orders, via an independently-sized (K,dps,ct0) grid and an
   independently-written extrapolation routine; monotone-tightening-in-x
   pattern confirmed at both endpoints.
6. Stress test at x=20, c=200 (§5): both the undersized-sizing failure
   mode and the corrected-sizing recovery (ratio≈0.9833) independently
   reproduced.
7. Overall honesty/no-overclaim check: confirmed across the full
   document, including the executive summary, §6 verdict, and §8 open
   items.

**Final verdict: SOUND, with two negligible-severity, purely
rhetorical/cosmetic issues named above (neither affects any numerical
claim, derivation, or the document's own honest-non-closure verdict on
H1). H1 remains correctly reported as NOT closed.**
