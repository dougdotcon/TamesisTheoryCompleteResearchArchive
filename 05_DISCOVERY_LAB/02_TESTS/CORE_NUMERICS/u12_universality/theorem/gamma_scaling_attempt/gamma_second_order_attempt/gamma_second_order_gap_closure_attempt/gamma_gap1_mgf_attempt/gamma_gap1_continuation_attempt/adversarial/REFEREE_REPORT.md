# REFEREE REPORT — `GAMMA-GAP1-CONTINUATION-ATTEMPT` (wave 21, front a, `DISC-DEC-093`)

**Target:** `.../gamma_gap1_mgf_attempt/gamma_gap1_continuation_attempt/ATTEMPT.md`

**Referee discipline.** No `.py` file of this front, or of any ancestor or
sibling front in this lineage, was opened, read, or imported at any point.
Every check below was derived fresh from the mathematical prose of the
target `ATTEMPT.md`, `THEOREM.md` (Estágios 26, 30, 33), the wave‑17
front's own `ATTEMPT.md` (`gamma_scaling_attempt/ATTEMPT.md`), and the
direct predecessor's `ATTEMPT.md` (`gamma_gap1_mgf_attempt/ATTEMPT.md`),
all read in full, in prose, before any code was written. Reserved seed
range `20260901000–20260901999` was not needed — every claim under review
is exact symbolic algebra or deterministic high‑precision numerics; zero
random seeds drawn. No governance file was touched, no file outside this
`adversarial/` subdirectory was written, no git command was run.

---

## VERDICT

> **SOUND WITH ONE NAMED ISSUE (LOW severity, cosmetic/narrative only) —
> ACCEPT for catalogue.**
>
> The central correction claim — that Estágio 33's illustrative constant
> `κ_0=2.25` is wrong as a stand‑in for a genuine constant, that the true
> value from the wave‑17 front's own truncation formula is the
> **`γ`‑dependent** function `κ_0(γ)=8/(γ(2−γ))`, and that consequently
> `λ(γ)=4(3−2γ)/(γ(2−γ))` is continuous but **UNBOUNDED** on `(0,1)`
> (not "bounded" as Estágio 33's own §5 literally claimed) — is
> **CONFIRMED, independently, beyond reasonable doubt.** This directly
> refutes a load‑bearing sentence of Estágio 33's own diagnosis (already
> integrated into `THEOREM.md`/`DECISION_LEDGER.yaml`) and should be
> applied as a correction.
>
> The correctly‑scoped replacement (a single `C(γ_0)` works uniformly on
> every compact `[γ_0,1)`, not on the whole open interval) is a direct,
> immediate logical corollary of the exact‑algebra monotonicity of `λ`,
> and is **CONFIRMED**.
>
> The fully explicit, non‑asymptotic construction of item 1 (§4 of the
> target) — the tightened coefficient bounds, the `\hat G(n,γ)` formula,
> the `K≤K_max` elementary bound, the assembled `W(n,γ,C)`, the explicit
> `C(γ)`, and the reported `n_0(γ)` crossover table at all 8 sample
> `γ` values — was **independently reconstructed from the prose alone**
> and matches the front's own reported numbers to remarkable precision
> (exact integer agreement on all 8 `n_1(γ)` values; agreement to
> `<0.004` in `log_{10}(n_0)` at all 8 sample points; exact agreement to
> the reported 2–4 significant figures on all 8 `C(γ)` values). This is
> about as strong an independent confirmation as is achievable without
> reading the front's own code.
>
> **One LOW‑severity, purely narrative/cosmetic error was found** (see
> "Named issues" below): a single descriptive sentence in §4 Step 3
> misstates a numerical "looseness factor" comparison (claims `3` at
> `γ=1`; the true value, computed from the very formulas the sentence
> itself cites, is `6`). This number is not used anywhere downstream —
> `C(γ)`, `\hat G(n,γ)`, and the `n_0(γ)` table were all independently
> verified correct using the *actual* (correct) `λ̂(γ)` formula — so this
> does not affect the verdict of soundness.
>
> The overall verdict of the front — Gap 1 still **not** closed, `C(γ)`
> for `γ∈(0,1)` still fully **OPEN**, no claim of progress on any
> Millennium Problem — is accurate and is not overstated anywhere the
> referee checked.

---

## 1. The central correction claim (highest priority)

### 1.1 Primary-source verification

Direct reading of `gamma_scaling_attempt/ATTEMPT.md` (the wave‑17 front,
read in full) confirms, verbatim, in §5 (line ~307):

> `K := ⌈√((4/β)n ln n)⌉` (truncation)

with `β := γ(2−γ)/2` defined earlier in the same document, §2 (line ~173).
This `K` is the truncation used throughout wave‑17's own Theorem 1′/Theorem 2
proof (the finite‑`n` sandwich for `nφ(n,γn)`) — it is *not* a different
`K` used for an unrelated purpose, and `β` has no other meaning elsewhere
in that document. **The target front's quotation and its reading of the
context are accurate.**

### 1.2 Independent re-derivation (script `01`)

Given `K² = κ_0·n·ln n` (the Gap‑1 lineage's own shorthand, as used by both
the predecessor and the target), `κ_0 = 4/β` follows immediately from
squaring `K`'s defining formula (the ceiling adds only `O(1)`, irrelevant
to the leading constant `κ_0`). Independently re-derived with sympy from
scratch:

```
κ_0(γ) = 8/(γ(2−γ))     [exact zero symbolic difference from the claimed form]
κ_0(1) = 8, κ_0(0.5) = 32/3 ≈ 10.667, κ_0(0.1) ≈ 42.105, κ_0(0.01) ≈ 402.010
lim_{γ→0+} κ_0(γ) = +∞   (exact sympy limit)
```

All values match the target's reported figures exactly.

```
λ(γ) = κ_0(γ)·(3/2−γ) = 4(3−2γ)/(γ(2−γ))     [exact zero symbolic difference]
λ(1) = 4, λ(0.9) ≈ 4.848, λ(0.5) ≈ 10.667, λ(0.1) ≈ 58.947,
λ(0.01) ≈ 598.995, λ(0.001) ≈ 5998.9995     — ALL match the target's table exactly
lim_{γ→0+} λ(γ) = +∞    (exact sympy limit)
```

This directly and unambiguously **refutes** Estágio 33's own §5 claim
(quoted, and confirmed present verbatim in the predecessor's own
`ATTEMPT.md` §5 item 2) that "`λ(γ)=κ_0(3/2−γ)` is manifestly continuous
and bounded on `(0,1)` (between `κ_0` at `γ=1` and `(3/2)κ_0` at `γ=0`)" —
that statement is true only if `κ_0` is a `γ`-independent constant, which
it demonstrably is not.

### 1.3 Monotonicity of `λ(γ)`, independently confirmed two ways

`λ'(γ)`'s numerator, `−8γ²+24γ−24`, was independently derived (matching
the target's cited form exactly, including the numeric value `−14` at
`γ=1/2`) and shown to have **no real root in `(0,1)`** two independent
ways: (i) `sympy.solve` on the exact polynomial, and (ii) a 19,999‑point
fine numeric scan of the exact numerator over `(0,1)`, finding a single
constant sign (`−1`) throughout, no zero crossings. Since the denominator
`γ²(2−γ)²>0` on `(0,1)` (checked), `λ'(γ)<0` throughout, i.e. **`λ` is
exact‑algebra‑proved strictly decreasing on `(0,1)`**, confirming the
target's claim.

**Conclusion on item 3 and item 2 (literal reading): CONFIRMED, no
qualification needed.**

---

## 2. The compact-uniformity replacement (item 2, correctly-scoped)

This is a direct logical corollary of §1.3's monotonicity result, not a
separately new computation: since `λ(γ)` is strictly decreasing on
`(0,1)`, for any fixed `γ_0>0` and any `γ∈[γ_0,1)`, `λ(γ)≤λ(γ_0)`. The
Bulk/Tail Lemma's threshold requirement `C²>1/4+λ(γ)/2` is therefore
satisfied for the *entire* range `[γ_0,1)` by any `C` chosen to satisfy it
at the single worst-case point `γ_0`. **CONFIRMED** — this is exactly the
standard "uniform on compacts" pattern already used elsewhere in this
lineage (wave‑17's own Corollary 1), correctly identified as such by the
target.

---

## 3. Explicit coefficient bounds (§4 Step 3)

### 3.1 Fresh re-derivation of `x(D)`'s cubic structure (script `02`)

`τ(m)` was re-derived from scratch via `sympy.summation`, giving
`τ(m) = k²m/n² − km²/n² − km/n² + m³/(3n²) + m²/(2n²) + m/(6n²)`. Substituting
`M=γk+D` into this cubic and adding the cited exact `δ(D)=D(2k(1−γ)−D−1)/(2n)`
gives, by two independent routes (direct-substitution + `Poly` extraction,
and hand-assembly from `τ,τ',τ''` at `m=γk`), an **exact zero symbolic
difference** on all four coefficients. The independently re-derived
`c_0 = γk(2γ²k²−6γk²+3γk+6k²−6k+1)/(12n²)` matches **exactly** the
closed algebraic form that Estágio 33's own referee corrected (fixing a
spurious extra `γ` factor found in the front's first draft) — an
independent confirmation, from a completely different lineage front, that
the *corrected* `c_0` formula is right. The historical spot check
`c_0(γ=1/2,k=10,n=100) = 51/4000` was also reproduced exactly.

### 3.2 Numerical certification of the tightened bounds

The target's claimed bounds

```
|c_0| ≤ (7/6)k³/n² + (5/6)k²/n²
|c_1| ≤ 2k²/n² + (1−γ)k/n + k/n² + 3/(4n)
|c_2| ≤ (1−γ)k/(2n²) + 3/(4n)
c_3  = 1/(6n²)                              (exact)
```

were checked against the exact `c_i` derived in §3.1 above, using **exact
rational (`sympy.Rational`) arithmetic — no floating point, no roundoff**
— over a grid of `n∈{10,30,100,1000,10⁴,10⁵,10⁶}`, `γ∈{0.01,0.05,0.1,
0.3,0.5,0.7,0.9,0.99,0.999}`, and 5–8 sampled `k` per `(n,γ)` pair spanning
`[1,⌊n/2⌋]`: **1836 pointwise checks, zero violations.**

**Conclusion: CONFIRMED.**

---

## 4. `\hat G(n,γ)`, `K≤K_max`, and the leading asymptotic (script `03`)

### 4.1 `\hat G(n,γ)` formula

Substituting `k=K_max` symbolically into `g(K)=|c_0|+|c_1|K+|c_2|K²+c_3K³`
using the Step‑3 bounds (independently re-verified above) and expanding
gives, by direct symbolic comparison, **an exact zero difference** from
the target's claimed closed form
`\hat G(n,γ)=(10/3+(1−γ)/2)K_max³/n²+(7/4−γ)K_max²/n+(11/6)K_max²/n²+(3/4)K_max/n`.
**CONFIRMED** as an exact algebraic consequence of the coefficient bounds.

### 4.2 `K ≤ K_max(n,γ) := 4√(n ln n/β)`, all `n≥3`

Confirmed by an elementary independent argument: `K=⌈y⌉` with
`y:=2√(n ln n/β)`; since `y≥1` at the worst case `(n=3,β=1/2)` (checked:
`y≈5.13`), `⌈y⌉≤y+1≤2y=4√(n ln n/β)=K_max`. Also checked numerically
against the exact `K` at 70 `(n,γ)` points spanning `n=3` to `n=10⁸⁰`:
**zero violations.**

### 4.3 Leading asymptotic `\hat G(n,γ) ~ λ̂(γ) ln n`

`lim_{n→∞} \hat G(n,γ)/ln(n)` was computed symbolically and shown to equal
`16(7/4−γ)/β` **exactly** (zero symbolic difference from the target's
claimed `λ̂(γ)`).

**Conclusion: all of §4.1–4.3 CONFIRMED.**

---

## 5. Final assembly `W(n,γ,C)` and the `n_0(γ)` crossover table (script `04`)

The full construction — `Θ_max(n,γ,C):=C√(K_max ln n)`, `\hat G_Θ(n,γ,C)`
(the "identical construction" evaluated at `t=Θ_max`), `G_n^{bound}(n,γ):=
√(πn/β)`, `W(n,γ,C):=G_n^{bound}·(1/6)[\hat G_Θ³e^{\hat G_Θ}+2n^{−2C²}\hat G³e^{\hat G}]`,
`C_0(γ):=√(1/4+λ̂(γ)/2)`, `C(γ):=1.2C_0(γ)` — was **reconstructed entirely
from the ATTEMPT.md prose**, without ever consulting the target's own
scripts, and evaluated in log-space with `mpmath` dps=60 (mirroring the
front's own stated methodology). Log-space bisection was used to locate
`n_0(γ):=inf\{n:\log W(n,γ,C(γ))≤0\}`, and `n_1(γ):=⌈16384/β(γ)²⌉` was
computed identically to the target's own stated formula.

**Result — all 8 reported sample `γ` values checked (task asked for 2–3;
all 8 were done since the reconstruction was cheap once validated):**

| `γ` | our `C(γ)` | reported | our `n_1(γ)` | reported `n_1` | match | our `log₁₀n_0` | reported | `Δ` |
|---|---|---|---|---|---|---|---|---|
| 0.99 | 4.2275 | 4.23 | 65,550 | 65,550 | **EXACT** | 20.7889 | 20.79 | −0.0011 |
| 0.9 | 4.4880 | 4.49 | 66,867 | 66,867 | **EXACT** | 36.8288 | 36.83 | −0.0012 |
| 0.7 | 5.1908 | 5.19 | 79,141 | 79,141 | **EXACT** | 45.0238 | 45.02 | +0.0038 |
| 0.5 | 6.2258 | 6.23 | 116,509 | 116,509 | **EXACT** | 50.2760 | 50.28 | −0.0040 |
| 0.3 | 8.1158 | 8.12 | 251,965 | 251,965 | **EXACT** | 55.9502 | 55.95 | +0.0002 |
| 0.1 | 14.1578 | 14.16 | 1,815,402 | 1,815,402 | **EXACT** | 65.9479 | 65.95 | −0.0021 |
| 0.05 | 20.0520 | 20.05 | 6,893,991 | 6,893,991 | **EXACT** | 71.7832 | 71.78 | +0.0032 |
| 0.01 | 44.8878 | 44.89 | 165,490,771 | 165,490,771 | **EXACT** | 84.8813 | 84.88 | +0.0013 |

Every single `n_1(γ)` value matches the target's table **as an exact
integer**, and every `log₁₀(n_0(γ))` matches to within `0.004` (i.e. the
reported 2‑decimal‑digit precision). This is essentially a complete
independent confirmation of §4 Step 5's numeric table, achieved without
ever reading the target's own code — the referee's from-scratch
reconstruction of the formulas from prose alone reproduces the published
numbers to their full reported precision. Sign of `log W` was also
confirmed to flip correctly (`>0` just below, `<0` just above, to 6
decimal digits) at each of the 3 primary sample points.

**Conclusion: CONFIRMED at all 8 sample points.**

---

## 6. Monotonicity of `log W` (no spurious oscillation, script `05`)

Independent fine-grid scan (4000 points, `log₁₀(n)` axis, `mpmath` dps=60)
of the reconstructed `log W(n,γ,C(γ))` from `n_1(γ)` through more than 60
decades past the certified `n_0(γ)`, at `γ=0.5` and `γ=0.01`: **no local
increase found anywhere** in either scan (`increasing_found = False`),
consistent with the target's own script‑06 finding.

**Conclusion: CONFIRMED at both tested `γ`.**

---

## 7. Overall verdict check

Direct reading of the target's own VERDICT box, §5, and §6 scorecard
confirms: Gap 1 is explicitly and repeatedly stated as **NOT fully
closed**; `C(γ)` for `γ∈(0,1)` is explicitly and repeatedly stated as
**fully OPEN**; the honest caveat that `n_0(γ)` is astronomically large
and "not a numerically-useful bound at any `n` reachable by direct
computation" is stated prominently, not buried; and the closing lines of
every major section state "No claim of progress on any Millennium
Problem; pure combinatorial/asymptotic mathematics internal to this
archive." **No overstatement found anywhere in the document.**

---

## Named issues

### Issue 1 (LOW severity, narrative/cosmetic only — does not affect any load-bearing result)

§4 Step 3 states: *"a looseness factor of `λ̂/λ` between `3` (`γ=1`) and
`≈4.67` (`γ→0`) relative to the true leading constant `λ(γ)` of §3."*

Independent computation (script `06`), using the front's own stated
formulas `λ(γ)=4(3−2γ)/(γ(2−γ))` (§3) and `λ̂(γ)=16(7/4−γ)/β` (§4 Step 3,
independently confirmed exact in §4.3 above), gives:

```
λ̂(γ)/λ(γ) at γ=1:      6.000000    (NOT 3, as the text claims)
λ̂(γ)/λ(γ) as γ→0+:      4.666667    (≈4.67 — this part IS correct)
```

The ratio is **increasing** in `γ`, ranging over approximately `[4.667,
6.0]` on `(0,1)` — the true range and its direction both differ from what
the sentence states ("between 3 (γ=1) and ≈4.67 (γ→0)" implies the ratio
is *larger* near `γ→0` and *smaller* at `γ=1`; the true behavior is the
opposite). This looks like an isolated arithmetic slip (e.g. `8·(3/4)=6`
miscomputed as `3`) confined to one descriptive sentence.

**Why this does not affect the verdict:** the number "3" appearing in
this sentence is never used in any subsequent formula, bound, or
computation — `C_0(γ)`, `C(γ)`, `\hat G(n,γ)`, and the entire `n_0(γ)`
table are all built directly from `λ̂(γ)` itself (confirmed exact in §4.3
above and reproduced to full precision in §5 above), not from the
`λ̂/λ` ratio. The ratio sentence is purely descriptive color-commentary
about how "loose" the crude bound is relative to the true asymptotic
constant, and its numeric error does not propagate anywhere.

**Recommendation:** correct "between `3` (`γ=1`) and `≈4.67` (`γ→0`)" to
"between `≈4.67` (`γ→0`) and `6` (`γ=1`)" (or equivalently state the range
as `[14/3, 6]`, increasing in `γ`) if/when this front's text is further
edited; not a blocker to integration as-is.

### No other issues found

Every other numerical, symbolic, and structural claim independently
checked in Sections 1–6 above matched the target's own reported values
either exactly (symbolic algebra; `n_1(γ)` integers; `Ĝ` formula; `K≤K_max`
elementary bound; `λ̂(γ)` leading asymptotic) or to the target's own
reported numerical precision (`C(γ)` to 2–4 significant figures at all 8
points; `log₁₀ n_0(γ)` to within `0.004` at all 8 points).

---

## Summary of what was independently re-verified, and how

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | Wave-17's `K:=⌈√((4/β)n ln n)⌉`, `β:=γ(2−γ)/2`, in the correct context | direct primary-source reading | CONFIRMED, quotation accurate |
| 2 | `κ_0(γ)=8/(γ(2−γ))`, values, `γ→0` divergence | sympy, exact algebra | CONFIRMED exactly |
| 3 | `λ(γ)=4(3−2γ)/(γ(2−γ))`, values, `γ→0` divergence | sympy, exact algebra | CONFIRMED exactly |
| 4 | `λ(γ)` strictly decreasing on `(0,1)` | sympy `solve` + 19,999-pt scan | CONFIRMED, no root in `(0,1)` |
| 5 | Compact-uniformity `C(γ_0)` on `[γ_0,1)` | direct logical corollary of #4 | CONFIRMED |
| 6 | `x(D)` exact cubic, `c_0..c_3` (post-adversarial-corrected forms) | fresh sympy, 2 independent routes | CONFIRMED exactly, incl. `c_0` spot value |
| 7 | Tightened `|c_0|,|c_1|,|c_2|` bounds | exact-rational grid, 1836 checks | 0 violations |
| 8 | `\hat G(n,γ)` = algebraic consequence of bounds at `k=K_max` | sympy symbolic expansion | CONFIRMED exactly |
| 9 | `K≤K_max=4√(n ln n/β)`, `n≥3` | elementary proof + 70-pt grid to `n=10⁸⁰` | CONFIRMED, 0 violations |
| 10 | `\hat G(n,γ)∼λ̂(γ)ln n`, `λ̂:=16(7/4−γ)/β` | sympy symbolic limit | CONFIRMED exactly |
| 11 | `C_0(γ)`, `C(γ)=1.2C_0(γ)`, all 8 table values | reconstructed from prose | CONFIRMED, matches to reported precision |
| 12 | `n_1(γ)=⌈16384/β²⌉`, all 8 table values | reconstructed from prose | CONFIRMED, **exact integer match**, all 8 |
| 13 | `n_0(γ)` crossover, all 8 table values | mpmath dps=60 log-space bisection | CONFIRMED, `Δlog₁₀<0.004`, all 8 |
| 14 | No spurious oscillation of `log W` | 4000-pt grid, 2 sample `γ`, `n_1` to `n_0+60` decades | CONFIRMED, no local increase |
| 15 | Verdict not overstated; no Millennium claim | direct textual reading | CONFIRMED |

**Files in this directory:**
`01_kappa0_lambda_algebra.py`/`.log`,
`02_coefficient_bounds_check.py`/`.log`,
`03_Ghat_formula_and_Kmax_check.py`/`.log`,
`04_W_assembly_and_n0_crossover.py`/`.log` (+ `04b_full_table_check.log`,
all-8-`γ` extension of script 04),
`05_monotonicity_of_logW.py`/`.log`,
`06_looseness_factor_and_n1_sidecondition_check.log` (ad hoc check, no
separate `.py` needed — one-off script run inline and logged).

No `.py` file of any front in this lineage was read. No governance file
touched. No git command run. No claim of progress on any Millennium
Problem; this review is of pure combinatorial/asymptotic mathematics
internal to this archive, about a specific
random-permutation-with-reroutes ensemble.
