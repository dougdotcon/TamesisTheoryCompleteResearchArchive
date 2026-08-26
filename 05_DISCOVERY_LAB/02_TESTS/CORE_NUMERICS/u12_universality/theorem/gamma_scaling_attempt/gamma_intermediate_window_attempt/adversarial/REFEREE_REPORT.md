# REFEREE REPORT — `GAMMA-INTERMEDIATE-WINDOW-ATTEMPT` (`DISC-DEC-088`, wave 20 front d)

**Target.** `gamma_intermediate_window_attempt/ATTEMPT.md`, which claims
**FULL CLOSURE** of the intermediate window `n^ε ≤ c_n ≤ n^{2/3}/log(n)`
(fixed `ε∈(0,2/3)`), via a direct combination of two already-PROVED
archive results — Teorema R (`THEOREM.md`, Estágio 22) and Corolário 4.2
(`THEOREM.md`, Estágio 6) — plus a "bonus" claim that the same argument
gives `φ(n,c_n)/φ_∞(c_n)→1` for *any* `c_n→∞` with `c_n=o(n)`, no rate
restriction needed, strictly subsuming the `γ_n→0` half of Corolário 2
(`THEOREM.md`, Estágio 23).

This is pure combinatorics/asymptotic analysis internal to the Tamesis
Discovery Lab archive. **No claim of any kind about any Millennium Prize
Problem is made anywhere in the target document, and none is made in
this report.**

---

## VERDICT

> **SOUND WITH NAMED ISSUES (both minor, presentational — no
> mathematical error found).**

After a genuinely hostile, from-scratch re-derivation of every
algebraic step, an independent re-implementation of the finite-`n`
engine, and digit-level cross-checks of the document's own numeric
claims, **every mathematical assertion in `ATTEMPT.md` was confirmed
correct**: the assembled Theorem W is a valid bound, both cited
theorems are quoted exactly as they appear in `THEOREM.md`, the window
is genuinely non-empty and disjoint from Corolário 2's regime for the
claimed `ε` range, the claimed asymptotic rates at both edges are
correct, and — most importantly, given how surprising the "bonus"
claim is — it was independently re-derived algebraically **and**
confirmed numerically with a sequence (`c_n=log n`) that provably
falls *outside* Corolário 2's hypothesis but *inside* the bonus's
hypothesis, exactly as claimed. Two minor, non-mathematical issues
were found in the presentation/evidence layer (below); neither
invalidates any theorem, bound, or the overall closure claim.

---

## Issues found

### Issue 1 — MINOR (presentational inconsistency in the verdict box's `ε` range)

The VERDICT box states the closure holds "for every fixed `ε∈(0,1)`",
but §0 of the same document correctly derives that the window
`n^ε≤c_n≤n^{2/3}/\log n` is genuinely (eventually) non-empty **only**
for `ε∈(0,2/3)` — for `ε≥2/3`, `n^ε` eventually exceeds
`n^{2/3}/\log n` and no sequence can satisfy the window's bounds for
all large `n`, so the "theorem" for `ε∈[2/3,1)` is true only
**vacuously** (no sequence satisfies the hypothesis). The verdict
box's headline range is therefore misleadingly broad relative to
where the closure is substantive; §0 states the correct, narrower
range explicitly. This is a wording/consistency slip between two
places in the same document, not a mathematical error — the
substantive content (closure for `ε∈(0,2/3)`) is exactly what §0, §2,
and §3 correctly claim and what this report verifies below.

*Fix:* change the verdict box's "`ε∈(0,1)`" to "`ε∈(0,2/3)`" to match
§0's own derivation.

### Issue 2 — MINOR (a reported numeric threshold appears to reflect a sparse test grid, not the true crossover)

§2's description of script `01_verify_bound_algebra.py`'s output
states: "the window is non-empty for `ε∈{0.1,0.3}` already at `n=10^3`
and for `ε=0.5` from `n≳10^12`, `ε=0.6` needs larger `n` still."

Independent re-derivation (this report's `ref01_bound_algebra.py`,
§(5)) finds the true crossover for `ε=0.5` — i.e. the smallest `n`
with `n^{0.5}≤n^{2/3}/\ln n`, equivalently `\ln n ≤ n^{1/6}` — lies
between `n=10^7` and `n=10^8` (checked directly: at `n=10^7`,
`\ln n=16.12 > n^{1/6}=14.68`, condition fails; at `n=10^8`,
`\ln n=18.42 < n^{1/6}=21.54`, condition holds). This is **four to
five orders of magnitude earlier** than the document's stated
"`n≳10^12`". By contrast, the `ε=0.1`, `ε=0.3` claims ("already at
`n=10^3`") and the `ε=0.6` claim ("needs larger `n` still", true
crossover independently found here between `10^{26}` and `10^{27}`)
are consistent with — indeed conservative relative to — the true
crossovers, so this is specific to the `ε=0.5` line.

The most likely explanation is that script 01 tested non-emptiness
only at a sparse set of grid points (e.g. powers of ten with large
gaps such as `{10^3,10^6,10^9,10^12,\dots}`) and reported the first
*tested* point at which the condition held, rather than searching for
the true threshold — which would make the statement technically
non-false about the tested grid but misleading as phrased ("needs
`n≳10^12`" reads as a near-tight threshold, not as "first grid point
tested"). This does not affect any theorem: window non-emptiness for
every `ε<2/3` at large enough `n` is correct and is the only thing
actually needed by the proof; this issue is confined to a descriptive
numeric aside in §2.

*Fix:* either soften the phrasing ("non-empty by our tested grid
point `n=10^{12}`, though not searched for tightness") or re-run with
a finer grid between `10^6` and `10^{12}` to report the true, much
earlier crossover.

No other issues — mathematical, citation, or presentational — were
found.

---

## What was independently re-verified, and how

All work is original: no `.py` file of this front or of any front in
its lineage (`gamma_scaling_attempt` and all its descendants) was
opened at any point. Every script below was built from the prose of
`THEOREM.md` and of the two `ATTEMPT.md` documents named in the
mandate, read in full. `mpmath` at `dps=50` was used throughout; no
randomness is involved anywhere (this is a deterministic
algebraic/analytic question), so the reserved seed range
`20260897000–20260897999` was not drawn from.

### 1. Algebra check (Theorem W's assembly)

Re-derived by hand and confirmed computationally that
`|φ/φ_∞-1| = |φ-φ_∞|/φ_∞(c) ≤ [Teorema R's numerator]/L(c)` is valid
whenever `L(c):=(√π/2)c^{-1/2}-e^{-c}/(2c) > 0`, since Corolário 4.2
gives `φ_∞(c) > L(c)` unconditionally for `c>0` (so `0<L(c)<φ_∞(c)`
implies `1/φ_∞(c) < 1/L(c)` whenever `L(c)>0`). This is exactly the
combination the document performs — no gap in the assembly.

`ref01_bound_algebra.py`:
- Recomputed `a*=√π(1/√2-1/2)` to 50 digits:
  `0.3670872118627422375...`, matching the document's quoted value.
- Independently bisected the crossover of `L(c)` to positivity:
  `c*≈0.209396914612444`, matching the document's claimed `≈0.2094`.
- Confirmed `L(c)>0` comfortably for all `c≥1` (sampled densely on
  `[1,1000]`; minimum value `≈0.028` at `c≈1000`, still positive).
- Noted the closed-form identity `2a*/√π = √2-1` exactly (a useful
  internal consistency check on the constant, not itself claimed in
  the target document).

### 2. Citation accuracy

Read Estágio 22 (Teorema R) and Estágio 6 §4.2 (Corolário 4.2) of
`THEOREM.md` in full. Both are quoted **exactly**, including domains
of validity, strict-vs-non-strict inequalities, and constants:

- Teorema R: `n≥4` integer, `0≤c≤n` real,
  `|φ(n,c)-φ_∞(c)| ≤ (a*√c+κ_B)/n`, `a*=0.36708721...`,
  `κ_B∈(0.28048,0.2805)` (certified rational bracket), strict for
  `c∈(0,n]`. `ATTEMPT.md`'s "`κ_B<0.2805`" is a correct (conservative)
  reading of the cited bracket.
- Corolário 4.2: `φ_∞(c)=(√π/2)c^{-1/2}-R(c)`, `0<R(c)<e^{-c}/(2c)`
  for all `c>0`. Quoted exactly.

Also cross-checked the predecessor's Remark ("what Corolário 2 does
not claim", `gamma_scaling_attempt/ATTEMPT.md` §6) against the target
document's quotation of it: matches essentially verbatim (the target
writes `c_n` where the predecessor writes `c`, a cosmetic variable
rename, no content change), and matches the corresponding "what
remains open" item recorded at the end of Estágio 23 in `THEOREM.md`.
No citation errors of any kind found.

### 3. Window well-definedness

Re-derived independently (§(5) of `ref01_bound_algebra.py`):

- Non-emptiness for `ε∈(0,2/3)` confirmed at large `n` for
  `ε∈{0.1,0.3,0.5,0.6,0.65}` (all eventually non-empty); confirmed
  **not** eventually non-empty (up to `n=10^{400}` tested) for
  `ε∈{2/3,0.7,0.9}`, exactly matching the `2/3` cutoff claimed in §0.
  (See Issue 2 above for the one numeric-threshold discrepancy found.)
- Disjointness from Corolário 2's regime: independently confirmed
  `n^{2/3}/\log n < n^{2/3}\log n \iff n>e`, matching the document's
  claim exactly (checked at `n=3, e, 10, 100, 10^6`).

### 4. Asymptotic rate claims

Re-derived algebraically that for `c→∞`,
`B(n,c) = (a*√c+κ_B)/(n L(c)) = (2a*/√π)(c/n)(1+o(1))`, since
`L(c)\sim(√π/2)c^{-1/2}` as `c→∞`. Confirmed numerically
(`ref01_bound_algebra.py`, §(4a)/(4b)):

- Upper (hardest) edge `c_n=n^{2/3}/\log n`: `B(n,c_n)` strictly
  decreasing from `n=10` to `n=10^{300}` tested, ratio to the claimed
  leading term `(2a*/√π)n^{-1/3}/\log n → 1` (already `1.0000002` by
  `n=10^{20}`, exactly `1.0` to displayed precision by `n=10^{50}`).
  Also reproduced the document's specific honesty-check numbers
  exactly: `B<0.5` at `n=10`, `<0.1` at `n=100`, `<0.01` at `n=1000`
  for `ε=0.3`'s hardest point — matched digit-for-digit.
- Lower edge `c_n=n^ε`, `ε∈{0.1,0.3,0.5}`: confirmed decay rate
  `O(n^{ε-1})`, ratio to leading term `→1` in every case.

### 5. The "bonus" claim (`c_n→∞`, `c_n=o(n)`, no rate hypothesis)

Re-derived algebraically (not merely re-quoted): for `c≥c_0` (any
fixed constant with `L(c_0)>0`), `L(c)≥(√π/4)c^{-1/2}`, giving
`B(n,c) ≤ (4/√π)(a*c+κ_B\sqrt c)/n ≤ (4/√π)(a*+κ_B)\,c/n`, which `→0`
whenever `c_n/n→0` — **with no constraint on how slowly `c_n→∞`**.
This confirms the bonus claim from first principles, independent of
the document's own presentation.

Then stress-tested numerically with a genuinely slow sequence,
`c_n=\log n`, chosen because it provably fails Corolário 2's
hypothesis: with `γ_n=\log(n)/n`,
`γ_n\,n^{1/3}/\ln n = n^{-2/3} \to 0`, not `\to\infty` — so
Corolário 2 says nothing about this sequence. `ref02_phi_finite_n.py`
part (d) computed `φ(n,\log n)` via an independent from-scratch
finite-`n` engine (below) at `n=30,\dots,3000` and found the ratio
`φ(n,\log n)/φ_∞(\log n)` converging to `1` (`|ratio-1|` shrinking
from `4.1\cdot10^{-4}` at `n=30` to `1.4\cdot10^{-4}` at `n=3000`,
staying inside Theorem W's bound at every point) — exactly the
"strictly subsumes" behavior claimed, verified on a sequence outside
Corolário 2's reach. `ref03_fixedgamma_vacuous_check.py` additionally
confirmed, by contrast, that for **fixed** `γ>0` (`c=γn`), `B(n,γn)`
converges to a **nonzero** constant as `n\to\infty` (e.g. `≈0.0414`,
`0.1243`, `0.2899` for `γ=0.1,0.3,0.7`) rather than to `0` — i.e. the
Teorema-R route genuinely is vacuous there, exactly as the
predecessor diagnosed and as the target document states without
disputing. The boundary between the two regimes (`c_n=o(n)` vs.
`c_n=\Theta(n)`) is drawn correctly, and the document is honest that
it does not touch, weaken, or reprove Corolário 2's `γ_n\to\gamma^*>0`
half.

### 6. Numerical evidence — independent finite-`n` engine

`ref02_phi_finite_n.py` and `ref04_n3000_crosscheck.py` implement, from
scratch, the exact double-sum formula (cited as Lemma 1 of the
predecessor, quoted only by its stated formula, no `.py` opened):
`φ(n,qn) = (1/n)\sum_{k=1}^n A_k`,
`A_k = \sum_{m=0}^k \binom km q^m(1-q)^{k-m}P_{k,m}`,
`P_{k,m} = \prod_{i=1}^m(1-\frac{k-i}n)`, evaluated with `mpmath`
`dps=50` via incremental binomial-pmf and partial-product recurrences
(`O(n^2)` total work — a performance detail, not a different
quantity).

- **Sanity**: `φ(n,0)=1` exactly for `n=1,5,20,100`. ✓.
- **Teorema R pointwise**: 16 points spanning `n\in\{30,100,300,1000\}`
  and `c=n^\alpha`, `\alpha\in\{0.15,0.35,0.55,0.65\}` (the last
  deliberately beyond the window's own `2/3` cutoff, as a stress
  test): **zero violations**.
- **Ratio-to-1 trend**: confirmed monotone approach to `1` at every
  window-representative `\alpha` tested.
- **Digit-level cross-check of the document's own reported numbers**:
  independently recomputed the two specific values the document
  reports at `n=3000` — claimed `\alpha=0.15\to0.9999642`,
  independent recomputation: `0.9999641627` (matches to every
  displayed digit); claimed `\alpha=0.65\to1.0130`, independent
  recomputation: `1.013041391` (matches). This is strong evidence the
  document's own script 02 is correctly implemented and its reported
  numbers are genuine, not just internally consistent.

---

## Summary

The mathematics in `gamma_intermediate_window_attempt/ATTEMPT.md`
holds up under hostile, from-scratch scrutiny: the algebraic assembly
of Theorem W is correct and correctly bounded away from division
issues; both cited theorems (Teorema R, Corolário 4.2) are quoted
exactly; the named window is genuinely non-empty and disjoint from
Corolário 2's regime for the claimed `ε` range; the claimed asymptotic
rates at both edges were independently re-derived and numerically
confirmed; the "bonus" generalization (no rate hypothesis needed for
`c_n\to\infty`, `c_n=o(n)`) was independently proved from first
principles and confirmed on a sequence (`c_n=\log n`) that provably
lies outside Corolário 2's hypothesis, exactly validating the
"strictly subsumes" claim; and the document's own reported numerics
were reproduced digit-for-digit by a fully independent implementation.
Two minor, purely presentational issues were found (an inconsistent
`ε`-range in the verdict box vs. §0, and one numeric non-emptiness
threshold that looks like a sparse-grid artifact) — neither touches
any theorem or the correctness of the closure. No claim of progress on
any Millennium Prize Problem appears anywhere in the target document
or in this report.

**Final verdict: SOUND WITH NAMED ISSUES (both minor, presentational
only) — the FULL CLOSURE claim and the bonus generalization both stand.**
