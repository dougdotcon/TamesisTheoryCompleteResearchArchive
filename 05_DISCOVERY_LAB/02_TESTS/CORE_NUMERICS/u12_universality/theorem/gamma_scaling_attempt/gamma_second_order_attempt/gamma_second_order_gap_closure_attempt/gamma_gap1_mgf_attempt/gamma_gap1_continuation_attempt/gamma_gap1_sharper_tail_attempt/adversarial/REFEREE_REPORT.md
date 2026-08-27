# REFEREE REPORT — `GAMMA-GAP1-SHARPER-TAIL-ATTEMPT` (wave 22, front c, `DISC-DEC-096`)

**Target document:** `.../gamma_gap1_continuation_attempt/gamma_gap1_sharper_tail_attempt/ATTEMPT.md`

**Referee discipline.** This report was produced entirely from the mathematical
prose of the target `ATTEMPT.md` and its required-reading lineage:
`THEOREM.md` Estágios 23, 26, 30, 33, and 36 (read in full); the direct
predecessor's `ATTEMPT.md` (`gamma_gap1_continuation_attempt`, 454 lines,
read in full); and the grandparent's `ATTEMPT.md` (`gamma_gap1_mgf_attempt`,
609 lines, read in full, including its dated post-adversarial correction
notes). **No `.py` file belonging to this front or to any front in its
lineage (`gamma_gap1_continuation_attempt`, `gamma_gap1_mgf_attempt`,
`gamma_second_order_gap_closure_attempt`, `gamma_second_order_attempt`,
`gamma_scaling_attempt`, or any other ancestor/sibling) was opened, read, or
imported at any point.** Every script in this `adversarial/` directory
(`ref01`–`ref06`) was written fresh, with the referee's own variable names
and own code structure, directly from the required-reading prose.

**Seeds.** Reserved referee block `20260915000–20260915999` (confirmed
unused by `grep -rn "20260915" 05_DISCOVERY_LAB/` before any code was
written — only the ledger/queue reservation lines were found). **This
referee draws zero random seeds** — every check below is either exact
symbolic algebra (`sympy`) or deterministic high-precision numerics
(`mpmath`, dps=50–60, exact Binomial pmf summation or exact closed-form
evaluation, deterministic grids). The reserved block is disclosed as
unused, not silently abandoned, matching this lineage's own discipline.

---

## VERDICT

> ## SOUND
>
> Every load-bearing mathematical claim in the target document was
> independently re-derived and/or independently numerically verified, with
> **zero violations found anywhere**, including the flagship claim (§4:
> `C0_Bernstein(γ,a)²` bounded and strictly decreasing on all of `(0,1)` for
> every `a>0`), which this referee not only reproduced but **strengthened**
> with a cleaner structural proof (see "Beyond the target's own checks"
> below). The full `n_0(γ)` assembly (§5) was independently reconstructed
> from the prose alone and reproduces the target's own published table —
> **both the OLD (Hoeffding) and NEW (Bernstein) columns, at all 8 sample
> `γ` values, not merely a 2–3 point spot check** — to within `≤0.005`
> decades almost everywhere (worst case `0.03` decades), after this referee
> caught and corrected a limitation in its own first-pass reconstruction of
> the small-`k` residual term (disclosed in full below — this is a referee
> self-correction, not a finding against the target document). No
> arithmetic, algebraic, or logical error was found in the target document
> itself. No Millennium Prize Problem discipline issue. No overclaiming
> detected in the honesty-scrutiny pass (§6 of this report).

---

## Summary of what was independently re-verified, and how

### 1. Bernstein's inequality, re-derived from scratch and checked against the exact Binomial tail

Re-derived the Bennett/Bernstein MGF argument independently for
`D = Σ Y_i`, `Y_i := Bernoulli(γ) − γ`, arriving at the same classical form
the target cites:
`P(|D|>t) ≤ 2·exp(−t²/(2kσ²+(2/3)Mt))`, `σ²=γ(1−γ)`, `M=max(γ,1−γ)`.

- **Part A** (script `ref01`): the calculus fact `eᵘ−1−u ≤ (u²/2)/(1−u/3)`
  for `0≤u<3` — verified on 499 dense points (zero violations, worst margin
  `≈1.8×10⁻¹¹`) and, independently, via the termwise power-series reduction
  `2·3^(j−2) ≤ j!` for `j=2,…,40` (all true).
- **Part B**: the full Bernstein bound checked against the **exact**
  Binomial tail probability via direct `mpmath` (dps=50) pmf summation — no
  normal approximation, no shortcut — across `352` `(k,γ,t)` triples
  (`k∈{5,…,1000}`, `γ∈{0.01,…,0.99}`, thresholds at `0.5×,1×,1.5×,2.5×` the
  natural std-dev scale). **Zero violations**; worst exact/bound ratio
  `≈0.554` (bound never violated, not absurdly loose).
- **Part C**: confirmed the qualitative claim that Bernstein is dramatically
  sharper than Hoeffding away from `γ=1/2` (ratios as small as `≈2.9×10⁻¹³`
  at the referee's own test point) and loses by only a **finite** factor
  exactly at `γ=1/2` (`≈2.27×` at the referee's test point — the specific
  numeric ratios differ from the target's own illustrative point, as
  expected since they depend on the chosen `(k,t)`; the qualitative
  crossover behavior matches exactly).

**Conclusion: the derivation and the "zero violations against exact pmf"
claim are CONFIRMED independently.**

### 2. The slack-parameter (`a>0`) construction

Independently re-derived, by hand algebra, the sufficient condition
`(2/3)MΘ_k ≤ akσ²` ⟹ Bernstein denominator `≤(2+a)kσ²` ⟹
`P(|D|>Θ_k) ≤ 2n^{−C²/((2+a)σ²)}`, and solved for the threshold:

```
(2/3)MΘ_k ≤ akσ²  ⟺  √k ≥ (2MC√(ln n))/(3aσ²)  ⟺  k ≥ (2MC/(3aσ²))²·ln n =: k_2
```

exactly matching the target's claimed `k_2(n,γ,C,a)` formula.

- **Part A** (script `ref02`): confirmed the sufficient condition holds at
  and above `k_2` — `1680` checks, **zero failures**.
- **Part B**: confirmed the resulting clean bound `2n^{−C²/((2+a)σ²)}`
  against the exact Binomial tail at `k` just above `k_2` — `22` checks,
  **zero violations**.
- **Part C**: independent `sympy` symbolic solve of the boundary equation
  `(2/3)MC√(k·ln n) = akσ²` for `k` reproduces the claimed `k_2` formula
  **exactly** (zero symbolic difference).

**Conclusion: CONFIRMED, independently, both algebraically and
numerically.**

### 3. The flagship finding — `C0_Bernstein(γ,a)²` bounded and strictly decreasing on `(0,1)` (the single most important check)

Built `C0_Bernstein(γ,a)² := (2+a)·σ²(γ)·(λ̂(γ)+1/2)` fresh in `sympy`, using
the predecessor's own definitions (`σ²(γ)=γ(1−γ)`, `β(γ)=γ(2−γ)/2`,
`λ̂(γ):=16(7/4−γ)/β(γ)`, all re-verified by direct citation-checking against
the predecessor's `ATTEMPT.md` §4 Step 3, read in full). All four numbered
sub-claims were independently confirmed by exact symbolic algebra (script
`ref03`):

1. **Mechanism claim:** `σ²(γ)·λ̂(γ) → 28` as `γ→0⁺` — confirmed by exact
   `sympy.limit`.
2. **Strict monotone decrease for every `a>0`:** confirmed two ways. (i)
   Spot-checked at 10 representative `a` values (`0.01` to `100`): the
   derivative's numerator has **no real root in `(0,1)`** at any tested
   `a`, and is negative at the midpoint in every case. (ii) **A stronger,
   structural proof this referee found independently**: since
   `C0_Bernstein(γ,a)² = (2+a)·f(γ)` with `f(γ):=σ²(γ)(λ̂(γ)+1/2)`
   **not depending on `a` at all**, and `(2+a)>0` for every `a>0`, the sign
   of `d/dγ C0_Bernstein²` is *identical* to the sign of `f′(γ)` for
   **every** `a>0` simultaneously. `f′(γ)`'s numerator was confirmed by
   `sympy.real_roots` to have **no root in `(0,1)`**, negative at the
   midpoint — proving monotone decrease for the entire family `a>0` **in
   one shot**, not just at sampled `a` values. (This is a strictly stronger
   check than sampling `a`, and confirms the target's claim holds with no
   gap.)
3. **`lim_{γ→0+} = 28a+56`:** confirmed by exact `sympy.limit`, symbolic
   difference from `28a+56` is exactly `0`.
4. **`lim_{γ→1-} = 0`:** confirmed by exact `sympy.limit`.
5. **Independent dense numeric cross-check** (mpmath, 50000-point grid, 4
   values of `a`): monotone decrease confirmed over the whole scan; the
   numeric supremum matches `28a+56` to `<3×10⁻⁵` relative error at every
   tested `a`.
6. **Contrast:** `C0_Hoeffding(γ)² := 1/4+λ̂(γ)/2` (the analogous
   Hoeffding-route quantity, built from the *same* `λ̂` the target uses,
   confirming this is the correct load-bearing quantity per the target's
   own §8 item 1 self-correction) confirmed to diverge (`+∞`) as `γ→0⁺` —
   independently re-confirming, via a fresh derivation, both the
   predecessor's Estágio-36 finding for `λ(γ)` and its analogue for `λ̂(γ)`.
7. **`a=0.05` sup `=57.4`:** confirmed exactly (`28·0.05+56=57.4`).

**Bonus finding (this referee, not previously stated in the target
document).** The referee additionally verified, purely as extra due
diligence, an elegant consistency fact implicit in the two documents: the
"ideal" `a→0⁺` limit `C0_Bernstein(γ,0⁺)² = 2σ²(γ)(λ̂(γ)+1/2)` satisfies

```
C0_Hoeffding(γ)² − C0_Bernstein(γ,0+)² = (γ−1/2)²·(2λ̂(γ)+1) ≥ 0
```

with equality **iff `γ=1/2` exactly** — proving algebraically, in closed
form, the target's own §7 item 5 claim that the ideal-`a` construction is
"still strictly better than Hoeffding for every `γ≠1/2`, and equal to
Hoeffding exactly at `γ=1/2` — never worse in the limit." This was stated
by the target but not proved there; this referee supplies the missing
one-line proof, confirming it is exactly correct.

**Conclusion: the flagship claim is CONFIRMED without qualification, by an
independent derivation that is if anything stronger (proves the "for every
`a>0`" claim structurally, in one shot, rather than by sampling).**

### 4. `σ²(γ)·λ̂(γ) → 28` mechanism claim

Confirmed as part of check 3 above (item 1). As an extra cross-check, this
referee also computed `σ²(γ)·λ(γ)` (using Estágio 36's *tight* asymptotic
`λ`, not the crude `λ̂` the target actually needs) and found it tends to `6`,
not `28`, as `γ→0⁺` — and `28/6 ≈ 4.667`, which matches **exactly** the
lower end of the predecessor's own corrected "`λ̂/λ` looseness factor" range
(`≈4.67` as `γ→0`, per the predecessor's dated post-adversarial correction).
This is an internal consistency check across three independent documents in
the lineage that all agree.

### 5. `n_0(γ)` comparison table — independently reconstructed at all 8 sample `γ`, not merely 2–3

Built, entirely from the required-reading prose (grandparent's exact `x(D)`
cubic / Bulk-Tail Lemma structure; predecessor's tightened coefficient
bounds, `K_max`, `Ĝ`, `Ĝ_Θ`, cited `G_n≤√(πn/β)`, and the `W(n,γ,C)`
Hoeffding assembly; target's Bernstein tail-factor replacement and
small-`k` residual), a **complete independent reconstruction** of the
`W(n,γ,C)` function for both constructions, using `mpmath` at dps=60
working directly on `mpf` values (no log-domain bookkeeping needed, since
`mpmath`'s arbitrary-precision exponent field tolerates the astronomically
large quantities involved — e.g. `Ĝ(n,γ)` in the tens-of-thousands, `n` up
to `10^85` — without overflow).

**By-hand algebraic cross-check first**, before any numerics: expanded
`g(t)=|c₀|+|c₁|t+|c₂|t²+|c₃|t³` at `t=k=K_max` from the predecessor's own
four coefficient-bound formulas and confirmed, term by term, that it
collects to *exactly* the predecessor's claimed closed form `Ĝ(n,γ) =
(10/3+(1−γ)/2)K³/n² + (7/4−γ)K²/n + (11/6)K²/n² + (3/4)K/n` — confirmed
again in-script (`ref04a`/`ref05`) by two independent computational routes
(direct term-by-term vs. the closed form), matching to relative difference
`~10⁻⁶¹` (machine-exact at dps=60).

**Calibration (script `ref04a`/`ref05`):** bisected `log₁₀ n_0(γ)` for the
Hoeffding construction at all 8 sample `γ` and compared against the
predecessor's own *published* table (transcribed as plain values, exactly
as the target document itself did): matched to **`≤0.005` decades at every
one of the 8 points** (e.g. `γ=0.01`: own `84.882` vs. published `84.880`).
This independently validates the entire machinery end-to-end.

**Main comparison, refined (script `ref05`):** extended the same
reconstruction to the Bernstein construction (`a=0.05`), bisecting the new
`log₁₀ n_0(γ)` at all 8 sample `γ`. Result:

| `γ` | own OLD | published OLD | own NEW | target's claimed NEW | own saved | target's claimed saved |
|---|---|---|---|---|---|---|
| 0.99 | 20.789 | 20.790 | 17.716 | 17.720 | 3.073 | 3.070 |
| 0.9 | 36.829 | 36.830 | 33.641 | 33.640 | 3.188 | 3.190 |
| 0.7 | 45.024 | 45.020 | 44.568 | 44.570 | 0.456 | 0.460 |
| 0.5 | 50.276 | 50.280 | 50.349 | 50.350 | −0.073 | −0.070 |
| 0.3 | 55.950 | 55.950 | 55.508 | 55.510 | 0.442 | 0.440 |
| 0.1 | 65.948 | 65.950 | 63.059 | 63.060 | 2.889 | 2.890 |
| 0.05 | 71.783 | 71.780 | 67.078 | 67.080 | 4.705 | 4.700 |
| 0.01 | 84.882 | 84.880 | 75.794 | 75.790 | 9.087 | 9.090 |

**Every single one of the 8 points matches to `≤0.005` decades** — far
beyond the "direction and rough magnitude" bar the task set. This is, in
effect, a full independent reproduction of §5's entire table.

**A genuine referee self-correction, disclosed in full (scripts `ref04a` →
`ref04b` → `ref04c`).** The referee's *first-pass* reconstruction of the
small-`k` residual term (§3 of the target) used coefficient bounds
evaluated at `K_max` (matching the "work entirely with `c_i(K)`" convention
the predecessor documents for the *Bulk/Tail* argument) for the small-`k`
deterministic bound as well. This matched the target's own table almost
exactly at `γ=0.5, 0.1, 0.01` (where the small-`k` term is negligible
either way) but **diverged sharply at `γ=0.99`** (own `19.51` vs. target's
`17.72`) — precisely the one point the target itself flags (§8 item 3) as
the case where the small-`k` term is *not* negligible. Diagnostic scripts
`ref04b`/`ref04c` traced this to the referee's own modeling choice: at the
target's own claimed `n_0(0.99)`, the referee's "bulk+tail" log-value
(`−3.1785`) matched the target's own disclosed intermediate number
(`≈−3.18`) almost exactly, isolating the discrepancy entirely to the
small-`k` piece. Switching to the more natural choice — coefficients
evaluated at the *running* `k=k₂` rather than at `K_max` for this
deterministic sub-bound (there is no structural reason, unlike in the
Bulk/Tail split itself, to inflate small-`k` coefficients to their `K_max`
value) — immediately reconciled the number to `17.716` (target: `17.720`),
and the corresponding `log(small-k term)≈−0.066` versus the target's own
disclosed `≈−0.04` (same order of magnitude, small residual difference
plausibly from minor bookkeeping choices in exactly how the union bound
over `k<k₂` terms is assembled). **This episode is recorded here as a
referee-side modeling artifact, not a finding against the target document**
— if anything, it is additional independent confirmation that the target's
own §8 item 3 self-disclosure (about the small-`k` term's non-negligibility
at `γ=0.99`) is accurate and precisely located.

**Secondary numeric spot-checks (script `ref06`), also independently
reproduced:**
- `k₂/K_max` at `γ=0.99`: `2.010×10⁻³` at `n_0`, shrinking to `3.628×10⁻²³`
  forty decades beyond — matching the target's own claimed `2.0×10⁻³` and
  `3.6×10⁻²³` almost digit-for-digit.
- No-spurious-oscillation (§6): `log W` confirmed monotonically decreasing
  (`increasing_found=False`) from `n_0` through 40 decades beyond, at 5
  representative `γ`, for **both** Hoeffding and Bernstein constructions —
  matching the target's own claim.
- The `s(k)` calculus fact `min_k s(k) = −γ²/(16βn)` was independently
  re-derived by elementary calculus (minimizing the quadratic
  `s(k)=βk²/n−γk/(2n)`): `k*=γ/(4β)`, `s(k*)=−γ²/(16βn)` exactly, matching
  the target's citation.

**Conclusion: the §5 table is CONFIRMED, at all 8 points (not just the
required 2–3), to a precision far tighter than "ballpark."**

---

## 6. Honesty scrutiny

- **"Gap 1 remains NOT closed; `C(γ)` for `γ∈(0,1)` remains fully OPEN"** —
  accurate. Confirmed against the full lineage read: the coefficient bounds
  `|c_i(k)|` and the `Ĝ`/`Ĝ_Θ` assembly are genuinely unchanged from the
  predecessor (independently re-verified in this referee's own §5
  reconstruction, which reused the *same* formulas as cited, not silently
  altered ones); only the tail-probability factor (and the small-`k`
  residual it necessitates) changed. `n_0(γ)` remains astronomically large
  (`10^18`–`10^76` at the tested points) — this referee's own bisection
  confirms this is not an exaggeration.
- **The `γ=0.5` loss (`−0.07` decades) explanation** — checked and found
  correct, not a symptom of an error: `σ²(1/2)=1/4` is exactly Hoeffding's
  implicit worst-case assumption, so at `a>0` fixed, Bernstein-with-slack
  is provably *never* strictly better there (confirmed algebraically in
  check 3 above: the `a→0⁺` ideal limit is exactly *equal* to Hoeffding at
  `γ=1/2`, with any `a>0` adding a small overhead there specifically). The
  numeric sign and magnitude of the loss (`−0.073` decades in this
  referee's own reconstruction) is consistent with this mechanism.
- **The "single `γ`-independent `C`" bonus claim** — correctly scoped. The
  target does not claim this makes `n_0(γ)` itself uniform or more
  practically useful — only that a single split constant `C` now suffices,
  which this referee independently confirmed follows rigorously from the
  boundedness proof (check 3). No overreach detected.
- **§8 self-caught issues** (wrong asymptotic quantity initially, `a=1`
  initially worse at 3/8 points, small-`k` term non-negligible at `γ=0.99`)
  — all three read as genuine, precisely diagnosed, and consistent with
  what this referee's own independent reconstruction found (in particular,
  item 3's disclosure was independently corroborated in detail via the
  `ref04b`/`ref04c` investigation above).
- **Minor presentational note (not a math error).** §5's remark that
  "`γ=0.7` and `γ=0.3` (symmetric around `γ=1/2` by construction, since
  `λ̂(γ)` and `σ²(γ)` are not symmetric but happen to give comparable
  values here)" is confusingly worded (claims "symmetric by construction"
  and "not symmetric" in the same clause) but the underlying numeric claim
  — comparable, sub-1-decade gains at both points — is independently
  confirmed (`0.456` vs `0.442` decades in this referee's own table).
  **Severity: LOW, cosmetic wording only, no mathematical content affected.**

## 7. Millennium Prize Problem discipline

Confirmed: no mention of the Riemann Hypothesis, P vs NP, Navier–Stokes, or
any other Millennium Problem anywhere in the target document. All "no claim
of progress on any Millennium Problem" disclaimers are present and
consistent throughout. Nothing to flag.

---

## Named issues

| # | Severity | Description |
|---|---|---|
| 1 | LOW (cosmetic, referee-side, not a target-document error) | This referee's own first-pass reconstruction of the small-`k` residual term (not the target document's own construction) initially diverged from the target's published `n_0(0.99)` by ~1.8 decades, due to an unforced modeling choice (coefficients at `K_max` rather than at running `k`). Corrected in `ref04b`/`ref04c`; final numbers match the target to `<0.005` decades. Recorded for full transparency of the referee's own process, per this lineage's disclosure norms. |
| 2 | LOW, presentational only | §5's parenthetical about `γ=0.7`/`γ=0.3` "symmetric... not symmetric... happen to give comparable values" is confusingly worded (see §6 above). No mathematical content is affected; the underlying numeric claim is correct. |

**No MODERATE or HIGH severity issues found anywhere in the target
document.**

---

## Files in this directory

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `ref01_bernstein_derivation_and_verification.py`/`.log` | from-scratch Bernstein derivation; verification vs. exact Binomial pmf (mpmath dps=50, zero violations); Bernstein-vs-Hoeffding qualitative comparison |
| `ref02_slack_parameter_k_uniform_verification.py`/`.log` | hand + symbolic re-derivation of `k_2(n,γ,C,a)`; sufficient-condition and clean-bound-vs-exact-pmf checks (zero violations) |
| `ref03_C0_bernstein_flagship_verification.py`/`.log` | the flagship check — exact-algebra boundedness/monotonicity/limits of `C0_Bernstein(γ,a)²`, including the referee's own stronger structural proof and the extra Hoeffding-equality-at-`γ=1/2` proof |
| `ref04a_n0_assembly_reconstruction_initial.py`/`.log` | first-pass independent reconstruction of the full `W(n,γ,C)`/`n_0(γ)` assembly, calibrated against the predecessor's published Hoeffding table; flags the `γ=0.99` discrepancy |
| `ref04b_diagnose_gamma099_discrepancy.py`/`.log` | diagnostic isolating the discrepancy to the small-`k` term |
| `ref04c_refine_smallk_term_test.py`/`.log` | tests and confirms the fix (running-`k` coefficients) |
| `ref05_n0_final_spotcheck_all8.py`/`.log` | final, refined reconstruction — reproduces the target's OLD and NEW `n_0(γ)` tables at all 8 sample `γ` to `≤0.005`–`0.03` decades |
| `ref06_oscillation_and_k2ratio_check.py`/`.log` | independent reproduction of the §6 no-oscillation and `k₂/K_max`-shrinking checks |

### Seeds table

| Block | Status |
|---|---|
| `20260915000–20260915999` (referee reservation) | reserved; **zero seeds drawn** — every check is exact symbolic algebra (`sympy`) or deterministic high-precision numerics (`mpmath` dps=50–60) — disclosed as unused |

No git commands run. No file outside this `adversarial/` subdirectory was
written or modified. `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
`index.html` were not touched.
