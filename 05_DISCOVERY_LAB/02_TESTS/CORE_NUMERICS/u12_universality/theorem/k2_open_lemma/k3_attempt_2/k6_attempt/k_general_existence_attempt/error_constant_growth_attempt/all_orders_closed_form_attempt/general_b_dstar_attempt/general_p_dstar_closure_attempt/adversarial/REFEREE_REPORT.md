# Hostile referee report — `general_p_dstar_closure_attempt/ATTEMPT.md`

> **Scope.** Wave 15, front (a) hostile-referee pass, per standing archive
> discipline (`DISC-DEC-063`). Pure combinatorics — no Millennium Prize
> claim of any kind is made anywhere in this report, no external data, no
> holdout. Everything below was built entirely from scratch in a new
> `adversarial/` subdirectory; **none of the target front's own scripts**
> (`ground_truth.py`, `ingredients.py`, `odd_part.py`, `assemble.py`) were
> imported or executed — they were not even read, per the task's
> discipline. Nothing outside this directory was created, modified, or
> deleted; no git command was run.

## Verdict

**SOUND. ACCEPT for catalogue**, as a general-`p` closed-form-producing
algorithm for `D^{*(p)}_r(b)` (item 11 of `general_b_dstar_attempt/ATTEMPT.md`'s
scorecard), in exactly the sense the document itself claims — a terminating,
`p`-uniform algorithm, not a single `p`-free elementary formula. No error
was found anywhere in the document's mathematics, its self-caught-bug
narrative, its calibration table, or its honesty framing. This report
independently closes every gap the orchestrating session had not yet
covered and every gap the document's own §6 named, using methods
deliberately different from the target front's own (different `Q_p`
computation route, different central-moment route, different ground-truth
Stirling implementation, no shared code whatsoever).

**~18,650 independent checks in this report, 0 mismatches**, plus one
clean inductive proof (below) that closes the `k=9,10` gap analytically,
not just numerically.

---

## 0. What was already independently confirmed before this pass (not redone)

Per the orchestrator's brief, the following were already verified from
scratch by the orchestrating session and are accepted here without
repetition: `Q_p(u)` via Newton's identities vs. direct `e_p` definition
(`p=1..6`); central moments `\mu_2,\mu_4` vs. direct binomial summation;
`(E2)` verified symbolically for general `r,b`; the `S_{2k-1}(N,m)`
recursion cross-checked at `k=5,6,7`; the full assembled `D^{*(5)}_r(1)`
checked against an independent Corollary A3 ground truth at four points.
This referee's effort concentrated entirely on the five gaps named in the
brief and the document's own §6.

---

## 1. `S_{2k-1}(N,m)` recursion and the `H_k(r,b)` machine at `k=9,10`

This was the document's own top-flagged risk (§6, third bullet): the
`p=9,10` assembly needs `k` up to `9,10` (power `17,19`), but the
document's own direct brute-force coverage of the odd-power machinery
stopped at `k=7` (power `13`).

**1a. Direct brute-force cross-check of the cited recursion itself**
(`check1_S2k1_k9_k10.py`, built from scratch against the literal recursion
quoted in `ATTEMPT.md` §0 item 2): `S_{2k-1}(N,m)=\sum_{i=0}^m(N-2i)^{2k-1}\binom
Ni` vs. the recursion, for `k=9,10,12` (powers `17,19,23`), `N` up to `40`,
every valid `m`: **2700 checks, 0 mismatches.** (The wave-14 referee's own
report already verified this same recursion, independently, to `k=11`
[`abel_identities.py`, `REFEREE_REPORT.md` §1.2] — this check extends that
coverage past `k=11` as well as confirming it at the two specific values
the target document needed.)

**1b. Direct numeric cross-check of the document's own `H(power,depth)`
unrolling formula** (§2.3), implemented from scratch from the formula as
literally printed in `ATTEMPT.md`, against `T(power,d):=P_b\cdot
S_{power}(N-d,r-d)` computed by brute-force summation (no recursion at
all), for `k` up to `10` (power `19`), at `r\in\{9,10,12,15,20,25\}`,
`b\in\{0,1,2,3,5,8\}`: **360 checks, 0 mismatches**
(`check2_Hk_unrolling.py`). This directly extends the document's own
brute-force coverage of `H_k` (stopped at `k=7`) to `k=9,10`.

**1c. A clean inductive proof, closing the gap analytically.** Rather than
relying only on numerics, it is straightforward to prove
`H(\mathrm{power},d)=P_b\cdot S_{\mathrm{power}}(N-d,r-d)` for **every**
`\mathrm{power},d` by induction on `d` (decreasing), using only two already-
established facts: `(E2)` and the cited `S_{2k-1}` recursion. Sketch:

- *Base case* (`\mathrm{power}=1`, any `d`): `H(1,d)=[r]_d/[N]_d` by
  definition. Separately, `P_b\cdot S_1(N{-}d,r{-}d)=P_b\cdot(r{-}d{+}1)
  \binom{N-d}{r-d+1}=[r]_d/([N]_d(r{-}d{+}1))\cdot(r{-}d{+}1)=[r]_d/[N]_d`
  by `(E2)` with `j=d`. Equal.
- *Inductive step*: applying the cited recursion to
  `S_{\mathrm{power}}(N{-}d,r{-}d)` (i.e. with `N'=N-d`, `m=r-d`) gives a
  first term `(N'-2m)^{\mathrm{power}-1}(m{+}1)\binom{N'}{m+1}` where
  `N'-2m=N-d-2(r-d)=\beta+d=\beta_{\mathrm{local}}`, and multiplying by
  `P_b` and applying `(E2)` (`j=d` again) turns
  `P_b\cdot(m{+}1)\binom{N'}{m+1}` into `[r]_d/[N]_d` exactly — so the
  first term becomes `\beta_{\mathrm{local}}^{\mathrm{power}-1}[r]_d/[N]_d`,
  matching `H`'s first term. The recursion's tail term, multiplied by
  `P_b`, becomes `2N_d\sum_s\binom{\mathrm{power}-1}s P_b\cdot
  S_s(N{-}d{-}1,r{-}d{-}1)=2N_d\sum_s\binom{\mathrm{power}-1}s H(s,d{+}1)`
  by the induction hypothesis at depth `d+1`. This is exactly `H`'s tail
  term. Hence `T=H` at depth `d` whenever it holds at depth `d+1`, and by
  the base case it holds at every depth for `\mathrm{power}=1`; a short
  induction on `\mathrm{power}` (fixing `d`, since the recursion for
  `\mathrm{power}` only calls smaller odd powers at `d+1`) then gives
  `T=H` for **every** `(\mathrm{power},d)`, hence for every `k`, not just
  the ones checked numerically. This closes §6's third bullet completely,
  not just at `k=9,10` — the target document's own machinery is now known
  correct for **all** `k`, given only the two already-cited ingredients.

**Conclusion on item 1:** the gap is closed both numerically (2700+360
checks specifically at `k=9,10`) and analytically (the induction above).
No issue found.

---

## 2. The self-caught bug (§2.4): is the fix complete?

Re-derived `w_i(r,b):=P_b\cdot\binom N{r+i}` from the factorial definition
independently: `N=2r+b+1`, so `P_b\binom N{r+i}=\frac{r!(r{+}b)!}{N!}\cdot
\frac{N!}{(r{+}i)!(N{-}r{-}i)!}=\frac{r!(r{+}b)!}{(r{+}i)!(r{+}b{+}1{-}i)!}`
(using `N-r-i=r+b+1-i`, immediate from `N`'s definition) — this
**matches `ATTEMPT.md`'s corrected formula exactly**, with no restriction
on `i`.

Checked this closed form against a direct brute-force evaluation of
`P_b\cdot\binom N{r+i}` (via `math.comb`, independent of the factorial
identity), for `r=0..19`, `b=0..11`, every `i=1..b`: **1320 checks, 0
mismatches.** Specifically targeted the boundary cases named in the
brief — `i=1` and `i=b` — at `r\in\{0,1,2,5,10,20,50\}`,
`b\in\{1,2,3,5,10,20\}`: **84 checks, 0 mismatches**, all included above.
Also verified a structural property that would be an easy place for an
off-by-one to hide (`w_i(r,b)=w_{b+1-i}(r,b)`, a symmetry immediate from
the closed form): **140 checks, 0 failures**; and the explicit value
`w_1(r,b)=1/(r{+}1)` for every `b`: **24 checks, 0 failures**
(`check3_strip_weight.py`). Total for this item: **1568 checks, 0
mismatches.**

No residual off-by-one found, including at both boundaries named in the
brief. The fix is complete.

---

## 3. Scale push for `p=5,6` to the parent's own full scale

Built a complete, independent second implementation of the §2 assembly
formula (`check4_scaleup_p5_p6.py`) — deliberately using **different**
methods from the target document at every ingredient, for maximal
independence:

- `Q_p(u)`: computed by direct DP evaluation of the elementary symmetric
  polynomial `e_p(1,\dots,u)` at `2p+2` integer points, then **exact
  Lagrange interpolation** (via Newton divided differences, `Fraction`
  arithmetic) to recover the polynomial-in-`u` coefficients — not Newton's
  identities (the document's route).
- Central moments `\mu_{2l}(N)`: computed by direct binomial summation at
  a handful of small `N`, then **exact Lagrange interpolation** to a
  polynomial in `N`, evaluated cheaply at large `N` — not the cumulant-
  generating-function Taylor route (the document's route).
- `H_k(r,b)`: the `H(\mathrm{power},d)` recursion as printed in `ATTEMPT.md`
  §2.3 (already independently re-derived and confirmed in §1 above).
- `w_i(r,b)`, `\Phi_b(r)`: from the factorial definitions directly
  (§2 above).
- Ground truth: **own** unsigned-Stirling-number table via the standard
  recurrence, **own** implementation of Corollary A3.

Sanity check at small scale first (`r=0..19,b=0..7`, `p=1..6`, skipping
only the known apparent-removable-pole zone `N<2p` near the origin — the
same degenerate zone `ATTEMPT.md` itself names, already covered
separately by the `r<p` vanishing-boundary tests in both the target
document and the wave-14 lineage): **874 checks, 0 mismatches** across
`p=1,\dots,6`.

**Full-scale push, matching the parent document's own scale exactly**
(`r=200,b=30`, vs. the target document's own `p=5,6` scale of `r\le120,
b\le25`):

| `p` | `r` range | `b` range | checks | mismatches |
|---|---|---|---|---|
| 5 | 0..200 | 0..30 | 6206 | 0 |
| 6 | 0..200 | 0..30 | 6195 | 0 |

**Total: 12 401 checks, 0 mismatches**, at scale that matches the parent's
own `Theorem D1` scale ceiling exactly and exceeds the target document's
own `p=5,6` scale by roughly `2.5\times` in `r`. No scale-dependent failure
found — the mechanism holds as cleanly at `r=200,b=30` as at `r\le20`.

(An intermediate run at `r=160/155,b=28` — 9132 checks, 0 mismatches — was
also produced en route to the `r=200,b=30` run above and is consistent
with it; not double-counted in the totals below.)

---

## 4. Independent re-verification of calibration reductions

Picked the three reductions judged most likely to hide a transcription
error: `p=4,b=1` (the highest-degree polynomial in the document's §3.1
table, degree `3` numerator times `(r+1)`, degree-`3` remainder), `p=3,b=1`,
and `p=2,b=3` (a `b\ge2` instance carrying the `(2r+3)` denominator and a
`(r+1)(r+2)` remainder denominator — the more structurally complex
pattern). Transcribed each printed closed form by hand from `ATTEMPT.md`
§3.1 and evaluated it at `r=0,\dots,249` using the exact rational
`\varphi_r=4^r(r!)^2/(2r{+}1)!`, checked against an independent Corollary A3
ground truth (`check5_calibration_reductions.py`):

| formula | range | checks | mismatches |
|---|---|---|---|
| `p=4,b=1` | `r=0..249` | 250 | 0 |
| `p=3,b=1` | `r=0..249` | 250 | 0 |
| `p=2,b=3` | `r=0..249` | 250 | 0 |

**Total: 750 checks, 0 mismatches.** All three printed formulas, including
the most algebraically complex one in the table, are exactly correct —
transcribed correctly from the underlying algorithm's output, with no
sign error, no off-by-one exponent, and no denominator slip.

---

## 5. Honesty / overclaim search

Read the full document, focusing on §5 ("what this does not do"), §6
(self-named risks), and §7 (scorecard), and cross-checked its framing
against the wave-14 referee's report and `THEOREM.md`'s Estágio 9/14
entries.

- **The "algorithm, not a `p`-free elementary formula" distinction (item
  12) is drawn correctly and consistently with archive convention.**
  `THEOREM.md`'s Estágio 14 entry labels the general-`k` prefactor
  collapse and the wave-14 referee's general-`k` odd-power identity
  PROVED despite both being `k`-parameterized statements (a formula/
  algorithm indexed by an integer `k`, not a `k`-free elementary
  expression) — exactly the same standard this document invokes for its
  own general-`p` algorithm. No inconsistency found; the analogy the
  document draws in §5 item 1 and §7 item 12 is apt, not a rhetorical
  stretch.
- **The claimed check counts add up and match the logs.** `26\,710+800+
  4054+2778=34\,342`, matching the document's own arithmetic; spot-checked
  `assemble.log`, `odd_part.log`, `ingredients.log`, `ground_truth.log`
  (reading logs only, not the scripts that produced them, per the task's
  discipline) — every per-`p` row in `assemble.log`'s sweep table and every
  named check-count in the other three logs matches the numbers quoted in
  `ATTEMPT.md` exactly.
- **No overclaim found in §5's "what this does not do" or the scorecard.**
  Item 13 (arbitrary `p>10`) is correctly marked OPEN, not glossed over.
  Item 14 (strip sum not reduced to a non-summed form) is correctly framed
  as unchanged/by-design, matching the parent's own framing. Item 15
  (no independent adversarial pass yet performed) was accurate at the time
  of writing and is what this report now discharges.
- **The self-caught-bug disclosure (§2.4) is candid and specific** — it
  names the exact wrong/right numerator, the exact failure signature
  (`3624/3926` mismatches), and cross-references the parent's own
  analogous disclosed bug rather than presenting the fix as uneventful.
  This referee's own re-derivation (§2 above) confirms the disclosure is
  accurate and complete.
- **One very minor, non-substantive wording note** (not an error, not
  worth a scorecard downgrade): §0's citation list says the referee's
  identity was "verified... numerically... through `k=11`", which is
  accurate per the wave-14 `REFEREE_REPORT.md`, but the executive summary
  (item 5) separately states this document's *own* spot-check reached only
  `k=8` — the two `k`-bounds refer to different things (the *cited*
  identity's own prior verification depth vs. *this* document's
  independent spot-check depth) and are each individually accurate, but a
  reader skimming only the executive summary could momentarily conflate
  them. Not misleading on a careful read (the distinction is drawn
  correctly in §0 and §6), and now moot in any case: §1 of this report
  extends direct coverage past both bounds and supplies a proof for all
  `k`.

No overclaim found anywhere in the document.

---

## 6. Summary of this report's checks

| # | Check | Method | Checks | Mismatches |
|---|---|---|---|---|
| 1a | `S_{2k-1}` recursion vs. brute force, `k=9,10,12` | from-scratch, literal recursion | 2700 | 0 |
| 1b | `H(power,depth)` unrolling vs. brute-force `S`, `k` up to `10` | from-scratch, literal formula | 360 | 0 |
| 1c | `H = P_b\cdot S` for all `(power,d)` | inductive proof from `(E2)`+recursion | analytic | — |
| 2 | `w_i(r,b)` re-derivation + boundary/symmetry/value checks | from-scratch factorial algebra | 1568 | 0 |
| 3a | Assembly sanity vs. ground truth, `p=1..6`, small scale | independent second implementation | 874 | 0 |
| 3b | Assembly vs. ground truth, `p=5,6`, `r\le200,b\le30` | independent second implementation | 12 401 | 0 |
| 4 | Calibration reductions `p=4,b=1`; `p=3,b=1`; `p=2,b=3` | hand-transcribed formula vs. ground truth | 750 | 0 |

**Total: 18 653 independent checks, 0 mismatches**, plus one closed-form
inductive proof extending the `H_k` machine's correctness to every `k`.

---

## 7. Net verdict

**SOUND. ACCEPT for catalogue.** The document's central claim — a
genuinely general-`p` closed-form-producing algorithm for `D^{*(p)}_r(b)`,
executed and verified for `p=1,\dots,10`, closing item 11 of
`general_b_dstar_attempt/ATTEMPT.md`'s scorecard in the sense the wave-14
referee specified — holds up under a fully independent, methodologically
distinct re-verification. Every gap the orchestrating session flagged and
every risk the document's own §6 named has now been either closed
numerically at higher scale/coverage than the document's own runs, or
closed analytically (the `H_k` induction, §1c, which subsumes the
document's own `k`-by-`k` numeric coverage entirely). No error, no
overclaim, and no residual off-by-one was found anywhere, including at
the specific boundary cases (`i=1`, `i=b`) and scale ceiling (`r=200,b=30`)
the brief asked this report to attack hardest.

**Conditions for integration into `THEOREM.md`:** none beyond the archive's
standing conventions already followed by this front (pre-registration,
exact arithmetic, self-disclosed bug, scoped honesty). This report,
combined with the target document, constitutes complete adversarial
sign-off for item 11 of `general_b_dstar_attempt/ATTEMPT.md`'s scorecard,
`p=1,\dots,10`; `p>10` remains correctly OPEN and unclaimed by either
document.

---

## 8. Files, reproducibility

All checks in this report are exact (`fractions.Fraction`), no randomness
used — the reserved seed range `20260842000+` (`DISC-DEC-063`, referee)
was confirmed unused elsewhere in the archive before this pass began
(`grep -rn "20260841\|20260842" 05_DISCOVERY_LAB/` returns only the
ledger's own reservation lines and this front's/this report's own notes
about the range) and was not needed here either, matching the target
document's own discipline.

| file | contents |
|---|---|
| `check1_S2k1_k9_k10.py` | brute-force vs. recursion, `k=9,10,12` |
| `check2_Hk_unrolling.py` | `H(power,depth)` vs. brute-force `S`, `k` up to `10` |
| `check3_strip_weight.py` | `w_i(r,b)` re-derivation, boundary/symmetry/value checks |
| `check4_scaleup_p5_p6.py` | independent second assembly implementation, `p=5,6` at `r\le200,b\le30` |
| `check5_calibration_reductions.py` | `p=4,b=1`; `p=3,b=1`; `p=2,b=3` reductions vs. ground truth |
| `REFEREE_REPORT.md` | this report |

Reproduce in any order (all self-contained, no shared imports with the
target front's scripts): `python3 check1_S2k1_k9_k10.py`; `python3
check2_Hk_unrolling.py`; `python3 check3_strip_weight.py`; `python3
check4_scaleup_p5_p6.py`; `python3 check5_calibration_reductions.py`.
Total runtime under one minute.
