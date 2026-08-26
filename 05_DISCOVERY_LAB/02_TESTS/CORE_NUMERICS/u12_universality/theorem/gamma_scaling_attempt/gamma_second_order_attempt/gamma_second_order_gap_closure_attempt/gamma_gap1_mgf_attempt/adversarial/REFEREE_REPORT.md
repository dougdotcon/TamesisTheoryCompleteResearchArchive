# REFEREE REPORT — `GAMMA-GAP1-MGF-ATTEMPT` (`DISC-DEC-088`)

**Target:** `.../gamma_second_order_gap_closure_attempt/gamma_gap1_mgf_attempt/ATTEMPT.md`
(wave 20, front a). Attacks Gap 1 ("Taylor-remainder-with-moments bound")
of `THEOREM.md` Estágio 26 §5, part of the still-open derivation of the
second-order constant `C(γ)` of the γ-scaling law for `γ∈(0,1)`.

**Referee discipline.** No `.py` file of this front, or of any front in
its lineage (`gamma_scaling_attempt`, `gamma_second_order_attempt`,
`gamma_second_order_gap_closure_attempt`, `gamma_gap1_mgf_attempt`), was
opened, read, or imported at any point. Every verification script below
(`adv01`–`adv04b`, in this `adversarial/` directory) was written fresh
from the mathematical prose of the target `ATTEMPT.md` and its required
reading only. Required reading completed in full, in prose, before any
derivation: `THEOREM.md` Estágio 10, Estágio 23 (Teorema 2, Lema 1,
Corolário 1/2), Estágio 26 in full (Lema E, Lema D0, Lacuna 1 in §5),
Estágio 30 in full (Lema τ-fluct, Lema G2); and both predecessor
`ATTEMPT.md` files in full
(`gamma_second_order_attempt/ATTEMPT.md`, 633 lines;
`gamma_second_order_gap_closure_attempt/ATTEMPT.md`, 479 lines).
No randomized checks were needed — every claim under review is exact
symbolic algebra or deterministic numerics — so the referee's reserved
seed block `20260891000–20260891999` was disclosed as unused, drawn zero
times, exactly mirroring the target front's own (unused) seed
disclosure.

---

## VERDICT

> **SOUND WITH NAMED ISSUES — the target front's own headline verdict
> ("Gap 1 is NOT closed; `C(γ)` for `γ∈(0,1)` remains OPEN") is fully
> correct and, if anything, is not overstated anywhere.** All four of the
> front's substantive numbered claims in its own up-front VERDICT block
> were independently re-derived or re-verified from scratch and confirmed
> essentially exactly, with **three named issues** below — none of which
> changes the front's own bottom-line non-closure verdict, but two of
> which are genuine, precisely-locatable errors/gaps in the *written
> document* that should be corrected before this front is treated as a
> clean reference for any future front building on it.

---

## Issues found (severity-ordered)

### Issue 1 — MODERATE. Bulk/Tail Lemma (§3.2) relies on an unstated,
### and not-literally-true-pointwise, monotonicity-in-`k` assumption

The Lemma's stated conclusion, `R_k ≤ (1/6)[g(Θ_K)³e^{g(Θ_K)} +
2n^{-2C²}g(K)³e^{g(K)}]` "for every `1≤k≤K`", is used downstream in §3.3
as a **single, `k`-independent pair of numbers** — i.e. `g(Θ_K)` and
`g(K)` are evaluated by substituting `k=K` into the `c_i(k)` coefficient
formulas (this is exactly how §3.3 computes them: `|c1|Θ_K`,
`|c1|K∼(1-γ)K²/n`, etc., always with `K` plugged into `c1(k)`). But the
Lemma's own proof (the "Bulk" paragraph) only establishes monotonicity of
`g(·)` **in its argument `t`**, for one *fixed* `k`. Making the final
bound literally uniform over `1≤k≤K` (i.e. valid to compare `g_k(Θ_k)`
against `g_K(Θ_K)`, using different `k`'s own coefficients on each side)
additionally requires `|c_i(k)|` to be **non-decreasing in `k`** — a fact
the document never states or proves.

This referee checked this directly (`adv02_bulk_tail_check.py`,
Part 2 "Monotonicity-in-k check"): **it is not literally true.** For
`γ` close to `1` (e.g. `γ=0.9`, `n=2000`), `c1(k) = k(1-γ)/n - 1/(2n) +
τ'(γk)/2` **changes sign** as `k` grows (its leading term
`k(1-γ)/n` shrinks toward the size of the other pieces when `1-γ` is
small), causing `|c1(k)|` to dip toward `0` before rising again — a clear,
reproducible, non-monotone excursion (53 violations found across the
tested `(n,γ,k)` grid, concentrated at `γ≥0.9`).

**However** — and this is why the issue is rated MODERATE, not fatal —
`adv02b_monotonicity_deep_check.py` checked the two facts the proof
*actually needs* (`g_k(Θ_k) ≤ g_K(Θ_K)` and `g_k(K) ≤ g_K(K)`, using
`K`'s own coefficients on the right) directly, for every `k=1..K`, at the
worst-offending cases found (`γ=0.9,0.99`, `n` up to `32000`): **zero
failures** in every case tested. The coefficient dip is real but too
small in absolute magnitude (dominated by the `c0`/`c2` terms) to ever
flip the assembled inequality in the ranges tested. **Conclusion: this is
a genuine gap in the written proof (an unjustified step, silently
assuming a fact that is not literally true term-by-term), but the
underlying Bulk/Tail Lemma conclusion is not found to be false anywhere
tested.** Fix: either (a) explicitly prove the needed weaker fact
(`g_k(Θ_K) ≤ g_K(Θ_K)` combining coefficient growth in the *aggregate*,
not term-by-term), or (b) restate the Lemma with a `sup_{k≤K}` on the
right-hand side and separately bound that sup.

### Issue 2 — LOW. §2's "closed algebraic form" for `c0` contains a
### transcription/algebra error (five of six bracket terms off by one
### spurious factor of `γ`)

`ATTEMPT.md` §2 states two equivalent forms for `x(D)`'s coefficients:
a "derivative-based form" and an "equivalently, in closed algebraic
form". This referee independently re-derived `x(D)`'s coefficients two
ways (`adv01_symbolic_x_polynomial.py`: direct `sympy` substitution +
`Poly` extraction, and independent hand-assembly via `τ,τ',τ''` at
`m=γk`), confirming both routes agree exactly with each other and with
the document's **derivative-based form** for all four coefficients
(`c0,c1,c2,c3`) — no error there.

The **closed algebraic form**, however, is wrong for `c0`. The document
states
`c_0 = (γk/(12n²))·[2γ³k²-6γ²k²+3γ²k+6γk²-6γk+1]`;
the correct closed form (confirmed against both independent derivation
routes) is
`c_0 = (γk/(12n²))·[2γ²k²-6γk²+3γk+6k²-6k+1]`
— i.e. the stated bracket has an extra spurious factor of `γ` on **five
of its six terms** (every term except the constant `+1`), as if `γ·`
were applied to the whole bracket except its constant term. Numeric
spot-check at `γ=1/2, k=10, n=100`: correct `c0 = 51/4000 = 0.01275`;
the document's stated closed-form expression evaluates to
`307/48000 ≈ 0.006396` — off by roughly a factor of 2 at this point (the
discrepancy is `γ`- and `k`-dependent in general, not a fixed ratio).
`c1,c2,c3`'s closed algebraic forms are all correct (confirmed exactly).

**Why this is rated LOW, not higher:** this referee's from-scratch
reproduction of §4's numeric table (`adv04_pmf_table_check.py`,
`adv04b_large_n_check.py`) — computed using the **correct** derivative-based
`c0` — matched the document's own printed `W_bound(n,γ)` table to within
`0.3%` at every one of 18 tested `(n,γ)` points (ratios `0.9908`–`1.0001`,
see Issues-independent verification section below). This strongly
indicates the front's actual verification script (`01_symbolic_x_polynomial.py`,
not read by this referee, but its *behavior* is visible through its
downstream numeric output) computed and used the correct value
internally, and the error is confined to the **prose transcription** of
the "equivalently, closed algebraic form" alternate expression — not a
computational error that propagated into any of the front's reported
results. It should still be corrected, since a reader who trusted the
printed closed form and used it to hand-check `c0` at a specific point
would get a wrong number.

### Issue 3 — LOW. §1's claim that combined-`x` equivalence to Gap 1's
### literal original target "was checked in Section 2" is not actually
### substantiated, and is separately (correctly) admitted as unverified
### in §5

§1 states: "...a simplification relative to the literal ingredient list
quoted above, made possible by the exact-algebra fact of Section 2, **and
checked in Section 2 to reduce to the identical quantity**." But Section
2 proves only that `x(D):=δ(D)+τ(M)/2` is an exact cubic polynomial in
`D` — it does not address, anywhere, whether bounding the Taylor
remainder of `e^{-x}` in the *combined* variable `x` (i.e. `E_M[e^{-x}] -
(1-E[x]+E[x²]/2)`, what §3–§4 actually bound) is the same quantity as
Gap 1's *literally quoted* original target,
`E_M[e^{-δ(M)-τ(M)/2}] - (1-E[δ]-τ(γk)/2+E[δ²]/2)` — which uses the
*deterministic* `τ(γk)` in the linear term (not the random `τ(M)`) and
only `E[δ²]` (not the fuller `E[x²]` that also carries `E[τ(M)²]` and
cross terms `E[δ·τ(M)]`) in the quadratic term. These are genuinely
different — related but not identical — target quantities; the original
formulation explicitly relies on the *separately-tracked* Gap 2
fluctuation correction (`τ(M)→τ(γk)`) to bridge the two, while this
front's combined-`x` object folds that correction in implicitly. Section
5, item 4, elsewhere in the **same document**, *correctly* states: "a
literal-minded check that the combined approach exactly reproduces the
six-term polynomial bound of Gap 1's original wording... was not
separately carried out" — directly contradicting §1's "checked in
Section 2" phrasing.

This is an internal inconsistency in the document's own cross-referencing
(what §1 claims was checked vs. what §5 admits was not), not a
mathematical error in anything actually proved: the cubic identity
(§2), the Bulk/Tail Lemma (§3.2), and the numerics (§4) are all
correctly-posed, self-consistent statements *about the combined-`x`
quantity as defined*, and stand on their own regardless of this framing
issue. But as written, §1 oversells what Section 2 established. Fix:
remove or soften "checked in Section 2 to reduce to the identical
quantity" in §1, since §5.4 already honestly flags this as unverified.

---

## Independent re-verification performed (summary)

| Claim (ATTEMPT.md) | Method | Result |
|---|---|---|
| §2: `x(D)` exact cubic in `D`, derivative-based form (`c0..c3`) | Fresh `sympy` re-derivation, two independent routes (direct substitution+`Poly`, and hand Taylor-assembly via `τ,τ',τ''`), cross-checked to exact `0` difference, then compared to ATTEMPT.md's own stated formulas | **Exact match**, all 4 coefficients, both internal routes and against the document (`adv01_symbolic_x_polynomial.py/.log`) |
| §2: `x(D)`'s "closed algebraic form" | Same symbolic re-derivation, compared coefficient-by-coefficient | **`c0` MISMATCH found** (Issue 2); `c1,c2,c3` exact match |
| §2: `γ=1` consistency (`c0(1)=τ(k)/2`) | Symbolic substitution | Exact match |
| §3.2: monotonicity of `g`, `t³eᵗ`; triangle inequality; Hoeffding tail bound `P(|D|>Θ_k)≤2n^{-2C²}` | Independent re-derivation of each proof step + numeric spot-check of the algebraic identity `2Θ_k²/k = 2C²ln n` | All confirmed correct (`adv02_bulk_tail_check.py`) |
| §3.2: assembled inequality `R_k ≤ (1/6)[...]`, uniform in `k≤K` | Direct exact-pmf computation (mpmath dps=50) of the true `E_M[g(|D|)³e^{g(|D|)}]` vs. the claimed RHS, 7 spot points; plus a full `k=1..K` sweep of the two component facts the proof needs, at the coefficient-non-monotonicity worst cases | Spot points: LHS≤RHS holds at all 7. Full sweep: **0/60, 0/120, 0/240, 0/30** failures — but see **Issue 1** (unstated assumption) |
| §3.3: `g(Θ_K)=O(n^{-1/4}\text{polylog})→0`; `g(K)=κ_0(3/2-γ)\ln n\,(1+o(1))` | Independent hand-algebra re-derivation term-by-term (dominant-term order counting) + numeric scaling-law fits, `n` up to `10^8`, all 6 tested `γ` | Hand algebra reproduces both closed forms **exactly**; numeric fitted `λ` matches predicted `κ_0(3/2-γ)` to **4.3%–5.3%** (front's own §3.4 reports `~6%`) — consistent (`adv03_asymptotics_check.py`) |
| §4: `W_bound(n,γ)` table, exact pmf-level ground truth | From-scratch mpmath dps=50 direct Binomial-pmf summation (recursive pmf, no shortcuts), `n∈{500,2000,8000,32000}`, all 6 `γ` (18 points total) | **Ratio to reported value 0.9908–1.0001 at every point** (12/18 points within 0.05%); `R_k^{exact}≤R_k^{Gap1}` confirmed with **zero violations** (0/84, 0/185 pointwise checks); monotone decrease in `n` confirmed at every `γ` (`adv04_pmf_table_check.py`, `adv04b_large_n_check.py`) |
| Overall verdict: no overclaiming, no Millennium Problem language | `grep -in "millennium"` over the target document | **0 matches** — none anywhere |

---

## Assessment of the front's own honesty/scope claims

The front's self-assessment in §5 ("what remains open, precisely") and
§6 (scorecard) is **accurate and, if anything, conservative**: it
correctly labels the asymptotics of §3.3 as "leading-order, NOT a fully
explicit-constant inequality" (confirmed true — the algebra is only
leading-order, and this referee's independent numeric fit shows the same
~5% finite-`n` gap the front itself reports), correctly does not claim
Gap 1 is closed anywhere, and correctly flags (§5.4) the very equivalence
question this referee also flags as Issue 3 above — the front's §5.4 is
in fact *more* honest than its own §1, which is precisely the
inconsistency named there. No claim of progress on any Millennium
Problem appears anywhere in the document, consistent with its own
repeated disclaimers.

## What was NOT independently re-derived (explicitly out of scope, cited
## by the target front itself as accepted external input)

- The origin of `δ(D) = D(2k(1-γ)-D-1)/(2n)` from `σ_k(m)`'s own
  definition (`σ_k(m)-σ_k(x)=(m-x)(2k-m-x-1)/(2n)`) — this identity's own
  derivation lies outside this referee's mandated required-reading chain,
  exactly as the target front itself discloses ("cited and used as-is
  below, not re-derived from `σ_k(m)`'s own definition, which is not
  restated anywhere in this front's required reading"). It was
  independently re-verified in earlier soundness rounds of this lineage
  (Estágio 23's own referee re-derived Lemma 1 from Definição 1 by hand)
  and is treated here, as the target front treats it, as trusted prior
  art.
- `κ_0`, the literal constant in the wave-17 truncation `K∼√(n\ln n)` —
  the target front itself uses an illustrative `κ_0=2.25` and explicitly
  flags this as not pinned down; this referee used the same illustrative
  value for direct comparability, per the front's own disclosed
  convention.

---

## Final verdict

**SOUND WITH NAMED ISSUES.** The target front's central, load-bearing
claims — the exact cubic-polynomial identity for `x(D)` (derivative-based
form), the Bulk/Tail Lemma's final inequality (confirmed to hold in every
tested case despite an under-justified proof step), the leading-order
asymptotics of §3.3, and the ground-truth pmf-level numerics of §4 — all
independently re-verify, most to very high precision (§4's table
reproduces to `<0.1%` at most points, `<1%` at all 18 tested points). The
front's own headline verdict — **Gap 1 not closed; `C(γ)` for `γ∈(0,1)`
remains OPEN** — is correct, not overstated, and (per this referee's
independent check) not understated either: every genuinely-proved piece
(§2's algebra, §3.2's lemma) really is proved, and every
leading-order/heuristic piece is honestly labeled as such.

Three issues are named above, none of which changes this bottom-line
verdict:
- **Issue 1 (MODERATE):** the Bulk/Tail Lemma's use as a single
  `k`-uniform bound relies on an unstated monotonicity-in-`k` assumption
  about `|c_i(k)|` that is not literally true pointwise (though the
  Lemma's actual conclusion was not found to fail anywhere tested).
- **Issue 2 (LOW):** `c0`'s "closed algebraic form" in §2 has a
  transcription/algebra error (extra factor of `γ` on 5 of 6 bracket
  terms); the derivative-based form (used, per this referee's
  reconstruction, for the front's actual reported numerics) is exact.
- **Issue 3 (LOW):** §1 overclaims that the combined-`x` reformulation's
  equivalence to Gap 1's literal original target "was checked in Section
  2" — Section 2 does not address this, and §5.4 elsewhere in the same
  document correctly (and consistently with this referee's own finding)
  flags it as not done.

**Recommendation:** ACCEPT for catalogue at the tier the front itself
claims (honest partial closure, Gap 1 not proved), with Issues 1–3
corrected by dated addenda before any future front cites this one's §2
closed-algebraic-form or §3.2 as a black box without re-checking.
