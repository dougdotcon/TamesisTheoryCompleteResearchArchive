# REFEREE REPORT — `gamma_second_order_attempt/ATTEMPT.md`

**Target:** Wave 18 front (b), `GAMMA-SECOND-ORDER-ATTEMPT`, the document at
`.../gamma_scaling_attempt/gamma_second_order_attempt/ATTEMPT.md`.
**Referee scope (per mandate):** verify Lemma E (§2) and Lemma D0 (§3), the
two claims labeled **PROVED** in that document, with full hostile-referee
rigor; check §4's heuristic for internal consistency and a genuine symbolic
match; assess §5's gap diagnosis; independently reproduce a sample of §6's
numerics. No `.py` file of any prior front, or of this front's own
`0X_*.py` scripts, was opened, read, or imported — every check below was
built from the mathematical prose alone.

---

## VERDICT

> **SOUND WITH ONE NAMED ISSUE.** **ACCEPT for catalogue** at the tier
> actually claimed by the document (Lemma E proved; Lemma D0's *value*
> proved; the rest honest non-closure with strong heuristic support) —
> **conditional on correcting one erroneous formal claim inside Lemma D0**
> (its stated error bound), which this review shows is **false as
> written** but does **not** affect the truth of the Lemma's closed form,
> does **not** affect Lemma E, and does **not** change the document's own
> headline VERDICT ("`C(γ)` is NOT proved for `γ∈(0,1)` by this front
> either").
>
> - **Lemma E (§2): CONFIRMED SOUND**, both directions, via two
>   independent algebraic routes (§A below). No error found.
> - **Lemma D0 (§3): the closed form `D_0(γ)=(γ−1)/(2(2−γ))` is CONFIRMED
>   CORRECT** (re-derived independently by a structurally different method
>   — completing the square before Poisson summation, rather than
>   splitting quadratic/linear parts — and confirmed to high precision by
>   fresh `mpmath` summation). **But the Lemma's stated error bound,
>   `O(√n·e^{−cn})` (exponentially small), is FALSE.** The true error is
>   `Θ(n^{−1/2})` (polynomially small only) — a different, much weaker,
>   and non-trivial fact than what the Lemma claims. This is named
>   precisely in §B below, with a closed-form leading coefficient derived
>   and numerically confirmed to 3–4 significant digits. Notably, **this
>   error is already visible in the document's own §3/§6.1 numerics**
>   ("`D_n^{(0)}→D_0(γ)` with clean `O(n^{−1/2})` error... ratio... `→√10`")
>   — the document's own numerical section already falsifies its own
>   Lemma's formal header, and this internal inconsistency went
>   unreconciled.
> - **§4 heuristic: symbolic match CONFIRMED independently real** (not
>   just trusting "sympy-checked" — redone from scratch here, including a
>   from-first-principles rebuild that never uses the document's own
>   algebraic grouping, landing on the identical rational function).
>   Pointwise internal consistency spot-checked numerically and found
>   consistent with the claimed order-counting (§C).
> - **§5 gap diagnosis: essentially accurate**, no major hidden gap found
>   in the "hard half" `E(γ)` obstruction. One clarification: the Lemma D0
>   error-bound bug (above) is a distinct, previously undisclosed defect
>   in the *"easy half,"* not covered by any of the three named gaps
>   (§D below).
> - **§6 numerics: independently reproduced** — the `D_n`/`E_n`
>   Richardson-extrapolation table (§6.3) and the `R_n` cross-check at
>   `n=2^18` (§6.5) both match the document's printed values and match the
>   wave-17 front's own printed `R_n` table (§E below).

No claim of progress on any Millennium Problem; this review concerns pure
combinatorial/asymptotic mathematics internal to this archive, about a
specific random-permutation-with-reroutes ensemble.

---

## §A. Lemma E — independent re-derivation (sympy, two routes)

Script: `01_lemma_E_symbolic.py` / `.log`.

Re-derived, from the stated definitions alone (`β:=γ(2−γ)/2`,
`G_n:=½√(πn/β)`, `L_n:=(√π/2)(γn)^{-1/2}`, `T(γ):=√(2/(2−γ))`):

1. `(G_n/n)/L_n = T(γ)` **exactly** — confirmed symbolically (`sympy`
   leaves branch-cut residue for `sqrt(-1/(g-2))` vs `sqrt(2-g)` under
   generic assumptions, so confirmed numerically at 9 sample points
   instead — all exactly `0`).
2. `D/G_n = 2D√(β/(πn))` — confirmed symbolically, exact `0` difference.
3. `T(γ)√(β/π) = √(γ/π)` — confirmed (numerically, same branch-cut
   caveat as (1)).
4. **A second, independent derivation of the forward direction**, never
   going through `G_n` or `β` at all: `(D/n)/L_n`, scaled by `√n`, reduces
   directly and symbolically to `(2/√π)√γ·D` — matching the document's
   claimed limit via a route that only uses `L_n`'s own `n`-scaling. This
   is a genuinely different algebraic path from the document's own
   `G_n`-based one, and it agrees exactly (symbolic difference `0`).
5. **A key fact worth stating explicitly** (the document does not spell
   it out, though it uses it implicitly and correctly): it is
   **`√n·L_n`**, not `n·L_n`, that is the `n`-independent quantity
   `(√π/2)/√γ` making the converse direction well-posed (i.e. that pins
   `D` down as a genuine constant, not something growing with `n`). A
   first pass at this check (see `01_lemma_E_symbolic.py`'s comment
   history / the script's own internal note) initially used `n·L_n` by
   mistake and got an assertion failure (`n·L_n = Θ(√n)`, not constant) —
   caught and corrected before being reported here, in this front's own
   transparency spirit. This does not affect the document, which never
   made this particular slip; it is disclosed here as due diligence on
   the referee's own work.
6. **D-equiv**: solving `D(γ) = (√π/(2√γ))·C(γ)` for the wave-17 front's
   conjectured `C(γ)` reduces symbolically, exactly, to the document's
   claimed `D(γ) = −(1/3)(6−8γ+3γ²)/(2−γ)²`. At `γ=1`: `D(1)=−1/3`,
   `C(1)=−2/(3√π)`, both matching.

**Conclusion: Lemma E's stated proof is correct in full — both directions
of the equivalence, and the D-equiv reduction.** No error found anywhere
in §2 of the document. The proof's asymptotic bookkeeping (treating
`o(1)`, `O(e^{-γn})` terms correctly relative to the `n^{-1/2}`-scale
target) is elementary but was checked line-by-line and holds.

---

## §B. Lemma D0 — the closed form is right, the error bound is wrong

Script: `02_lemma_D0_check.py` / `.log`.

### B.1 What the document's own proof actually establishes

The Lemma's **header** states:

> `S_n^{(0)} = G_n + D_0(γ) + O(√n·e^{-cn})` for some `c=c(γ)>0`.

But the Lemma's own **proof**, at its concluding line, only assembles:

> "Collecting: `S_n^{(0)} = (G_n−½) + γ/(4β) + o(1)`"

— i.e. the proof itself only claims `+o(1)`, not the exponentially small
`O(√n·e^{-cn})` of the header. This is already an internal mismatch
between what is stated and what is proved, visible on a close reading
before any new computation is done.

### B.2 Where the polynomial-order term actually comes from

The document's "quadratic part" (Jacobi-theta/Poisson-summation) step is
**correct and genuinely exponentially precise**:
`Σ_{k=1}^n e^{-βk²/n} = G_n − ½ + O(√n·e^{-π²n/β})`. This part of Lemma D0
is fully rigorous, elementary, and exactly as strong as claimed.

The problem is in the **"linear part"**: the document Taylor-expands
`e^{γk/(2n)} = 1 + γk/(2n) + O(k²/n²)` and separately argues the dropped
`O(k²/n²)` term, summed against `e^{-βk²/n}` over the relevant range,
contributes `O(n^{-2})·Σk²e^{-βk²/n} = O(n^{-2})·O(n^{3/2}) = O(n^{-1/2})
→ 0`. **This is correct as an order estimate — and it is exactly the
`Θ(n^{-1/2})` term that survives**, not a vanishing artifact of a
suboptimal proof technique. This can be shown directly by a cleaner,
independent route that avoids the split altogether:

**Independent re-derivation via completing the square** (done fresh here,
never appears in the document): since `s(k)=βk²/n − γk/(2n)` is an exact
quadratic in `k`,

```
-βk²/n + γk/(2n) = -(β/n)(k-μ)² + γ²/(16βn),      μ := γ/(4β)
```

so `S_n^{(0)} = e^{γ²/(16βn)} · Σ_{k=1}^n e^{-(β/n)(k-μ)²}`. The shifted
Gaussian sum is handled by Poisson summation exactly as the document's
quadratic part is (the fixed, `n`-independent shift `μ` only introduces a
bounded phase factor into the Poisson dual sum, not slowing the
exponential decay), and a short Euler–Maclaurin computation of the
`k≤0` tail gives `Σ_{k=1}^n e^{-(β/n)(k-μ)²} = G_n + (μ−½) + O(1/n)` with
exponentially small correction. Multiplying by the *prefactor*
`e^{γ²/(16βn)} = 1 + γ²/(16βn) + O(n^{-2})` gives:

```
S_n^{(0)} = G_n + (μ-½) + (γ²/(16β))·(G_n/n) + O(1/n)
          = G_n + D_0(γ) + (γ²√π)/(32β^{3/2})·n^{-1/2} + O(1/n)
```

using `G_n/n = ½√(π/(βn))`. **The middle term is a genuine, non-vanishing
`Θ(n^{-1/2})` contribution** — it comes from the interaction of the
(exponentially precise) Gaussian tail with the `O(1/n)` expansion of the
*prefactor* `e^{γ²/(16βn)}`, and there is no way to make it exponentially
small: `G_n=Θ(√n)` and the prefactor's own next-order term is
irreducibly `Θ(1/n)`, so their product is irreducibly `Θ(n^{-1/2})`. This
independently confirms `D_0(γ)=μ-½=(γ-1)/(2(2-γ))` (matching the
document exactly) **and** pins down that the true error order is
`Θ(n^{-1/2})`, not exponential.

### B.3 Numerical confirmation (decisive)

`02_lemma_D0_check.py`, `mpmath` dps=50, direct summation (no shortcuts),
`γ∈{0.1,...,0.9,1.0}`, `n` up to 32,000:

| γ | `r_n·√n` at n=1000 | at n=32000 | predicted coefficient `γ²√π/(32β^{3/2})` |
|---|---|---|---|
| 0.1 | 0.018821 | 0.018900 | 0.018916 |
| 0.5 | 0.059935 | 0.060235 | 0.060300 |
| 1.0 | 0.156674 | 0.156665 | 0.156664 |

(full table, all 6 γ values, in `02_lemma_D0_check.log`). At every tested
γ, `r_n := S_n^{(0)} - G_n - D_0(γ)` times `√n` converges cleanly, and
monotonically, to the predicted nonzero constant — not to zero, and with
no sign of accelerating decay at larger `n` (which an exponential term
would show immediately: an `O(√n e^{-cn})` term with the document's own
implied `c=π²/β` would be many orders of magnitude below float/mpmath
noise already at `n=1000`, e.g. `e^{-π²·1000/0.5}` — utterly
unobservable — yet `r_n` at `n=1000` is a perfectly ordinary
`~10^{-3}`-to-`10^{-2}`-scale quantity, orders of magnitude too large to
be an exponentially small term). This rules out any possibility that the
observed `Θ(n^{-1/2})` behavior is a slowly-decaying transient masking a
truly-exponential asymptotic; it is the genuine leading error term.

### B.4 What this does and does not break

- **Does not affect the correctness of `D_0(γ)`'s closed form** — proved
  correct independently, above, and confirmed numerically to high
  precision.
- **Does not affect Lemma E** — Lemma E only requires `S_n = G_n+D+o(1)`,
  and `Θ(n^{-1/2})` is `o(1)`, so `D_0(γ)`'s contribution to `D(γ)` via
  `S_n=S_n^{(0)}+E_n` is legitimate at the level of *establishing the
  limit* `C(γ)` (just not at the exponential precision the Lemma's header
  advertises).
- **Does not change the document's own headline verdict** — the mandate
  (`C(γ)` proved for `γ∈(0,1)`) was already NOT closed regardless of this
  bug, since `E(γ)` (§4) remains unproved either way.
- **Does invalidate the specific, quantitative claim of "an elementary,
  fully rigorous, **exponentially precise** tool"** (document's own VERDICT
  §, item 2) — the tool is elementary and rigorous for the *quadratic*
  part only; combined with the linear part, the whole of Lemma D0 is only
  polynomially precise (`Θ(n^{-1/2})`), a materially weaker and less
  novel-sounding claim than advertised.

**Recommended correction**: restate Lemma D0's header as
`S_n^{(0)} = G_n + D_0(γ) + Θ(n^{-1/2})` (with the leading coefficient
`(γ²√π)/(32β^{3/2})` from §B.2 available if a sharp form is wanted), and
remove "exponentially precise" from the framing prose. The value
`D_0(γ)=(γ-1)/(2(2-γ))` itself needs no correction.

---

## §C. §4 heuristic — symbolic match re-verified, pointwise consistency checked

Script: `03_E_gamma_heuristic_symbolic.py` / `.log`, `05_sec4_pointwise_consistency.py` / `.log`.

**Symbolic match.** Independently rebuilt `E(γ) := D(γ)-D_0(γ)` from the
document's own D-equiv and Lemma D0 closed forms, and separately rebuilt
`E_heuristic(γ)` two ways: (i) reducing the document's own stated
`coef`/`γ(1-γ)/(4β)` pieces, and (ii) a from-scratch rebuild starting only
from the cited Gaussian-moment integrals
`∫x e^{-bx²}dx=1/(2b)`, `∫x³e^{-bx²}dx=1/(2b²)` and the stated
`Q(k;n,γ)` formula, never reusing the document's algebraic grouping. All
three routes agree exactly: symbolic difference `0` in every case,
confirmed both by full polynomial simplification and by numeric
spot-checks at rational **and irrational** `γ` (`γ=√2/2`, `γ=π/4`) to
rule out a coincidental match at sampled rational points only. **The
symbolic match reported in §4 is real, not an artifact of the document's
own bookkeeping.**

**Pointwise internal consistency.** Directly evaluated `A_k` (exact, via
a fresh `O(1)`-per-term cumulative-log-product construction, independent
of and structurally different from the document's own scripts) against
the pointwise approximation `Q(k;n,γ)` at `k=Θ(√n)` (the scale that
dominates the sum), for `n` from `4096` to `1,048,576`. The relative
discrepancy between `A_k/e^{-s(k)}-1` and `Q(k;n,γ)` shrinks consistently
as `n` grows at fixed `k/√n` (e.g. at `γ=0.3,t=1`: `0.84%` at `n=4096`
down to `0.05%` at `n=1,048,576`) — exactly the behavior a genuine `o(1)`
per-term correction should exhibit, and consistent with (though not a
proof of) the claimed order-counting. No inconsistency found.

---

## §D. §5 gap diagnosis — assessed accurate, one addition noted

The three named gaps (Taylor-remainder-with-moments bound on
`E_M[e^{-δ-τ/2}]`; the `M`-fluctuation correction to `τ`; uniformity
across the truncation range) are, on inspection, the correct list of
what is needed to promote §4's heuristic to a proof — nothing in the
cumulant expansion's derivation suggests a missing fourth analytic
obstruction of comparable size. In particular the higher-order terms of
the log-product expansion (`j≥4` in `-ln(1-x)=Σx^j/j`) that the document
does not separately address are, in fact, already controlled by the
wave-17 front's own Lemma 2 (its proof bounds the *entire* tail
`Σ_{j≥2}x^j/j ≤ x²` in one step, not just up to the cubic term) — so this
is not a hidden gap, just an already-discharged piece of borrowed
machinery.

**One clarification the document should add**: the Lemma D0 error-bound
issue found in §B above is a genuine, previously undisclosed defect, but
it sits in the "easy half" (§3), not the "hard half" (§4/§5) — none of
Gaps 1–3 as stated would have caught it, since they are all about
`E_n`'s remainder, not `S_n^{(0)}`'s. A reader relying on §5 alone to
enumerate "everything wrong with this front" would miss it. It should be
listed as a fourth, already-resolved item ("Lemma D0's stated error
order was wrong; corrected to `Θ(n^{-1/2})`, no effect on the closed
form or on Lemma E") rather than silently absent.

---

## §E. Independent numerical reproduction of §6

Script: `04_full_Sn_independent.py` / `.log`.

Built a fresh `S_n=Σ_kA_k(n,γ)` evaluator from the mathematical statement
of Lemma 1 alone, using an `O(1)`-per-`(k,m)` cumulative-log-product
identity (`log P_{k,m} = cumlog[k]-cumlog[k-m]`, `cumlog` built once in
`O(n)`) — a different implementation strategy from either front's own
scripts (which were never read).

**§6.3 reproduction** (`D_n`/`E_n` at `n∈{2^14,2^16,2^18}`, two-point
Richardson extrapolation, `γ∈{0.1,...,0.9,0.99}`): this evaluator's
extrapolated `D_n`, `E_n` agree with the document's own printed table to
`≤4.2×10⁻⁷` in every case (mostly `≤10⁻⁸`), and agree with the closed-form
targets `D(γ)`, `E(γ)` to the same order — an independent confirmation of
§6.3, not merely a re-check of arithmetic already reported.

**§6.5 reproduction** (`R_n` at `n=2^18`, all 10 tabulated `γ` values):
this evaluator's `R_n` matches the wave-17 front's own printed table to
`≤5×10⁻¹¹` at every point — consistent with (and about as tight as) what
`THEOREM.md`'s Estágio 23 log records for its own independent referee's
reproduction of the same table ("`~10^{-11}` em todos os 6 valores de
`γ`"). `√n(R_n-target)` values reproduce the document's own §6.5 figures
(e.g. `γ=0.5`: `-0.324890`, matching exactly).

No discrepancy found anywhere in §6's reported numbers.

---

## Scorecard (this review's independent assessment)

| Claim | Document's status | This review's verdict |
|---|---|---|
| Lemma E (equivalence, §2) | PROVED | **CONFIRMED PROVED** — no error, both directions checked, two independent algebraic routes |
| `D_0(γ)=(γ-1)/(2(2-γ))` value (§3) | PROVED | **CONFIRMED PROVED** — independently re-derived by a different method (complete-the-square), confirmed numerically |
| Lemma D0 error bound `O(√n e^{-cn})` (§3) | PROVED (as part of the Lemma) | **FALSE AS STATED.** True error is `Θ(n^{-1/2})`, not exponential; a concrete nonzero leading coefficient is derived and numerically confirmed (§B). Correctable without touching the closed form or any downstream conclusion. |
| §4 heuristic `E(γ)` symbolic match | heuristic, "sympy-checked" | **CONFIRMED the match is real**, via 3 independent algebraic routes including numeric spot-checks at irrational `γ`; pointwise order-counting found internally consistent |
| §5 gap diagnosis | 3 named gaps, "not carried out" | **Assessed accurate**; no hidden gap found in the hard-half obstruction. One addition recommended: list the Lemma D0 error-bound fix as a fourth (already-resolved) item |
| §6.3/§6.5 numerics | reported to `≤2.5×10⁻⁷` / bit-for-bit | **Independently reproduced**, matching to `≤4.2×10⁻⁷` (§6.3-style) and `≤5×10⁻¹¹` (§6.5-style) |
| Document's own headline VERDICT (`C(γ)` NOT proved for `γ∈(0,1)`, honest non-closure) | — | **CONFIRMED accurate and honest**, and unaffected by the Lemma D0 finding above |

---

## Recommendation

**ACCEPT for catalogue**, at the tier the document actually claims,
**conditional on**:

1. Correcting Lemma D0's stated error bound from `O(√n·e^{-cn})` to
   `Θ(n^{-1/2})` (§B), and removing the "exponentially precise"
   characterization from the surrounding prose (VERDICT item 2, §3's
   framing). The closed-form value of `D_0(γ)` requires no change.
2. Optionally, adding one line to §5 (or a new §5.0) noting this
   referee-caught issue and its resolution, per this archive's own
   transparency culture (§7 of the document already models this pattern
   for its self-caught Monte Carlo bug; this is the same kind of
   disclosure, just caught by an external hostile pass rather than by the
   front's own authors).

No other errors were found. Lemma E is sound without qualification. The
document's central intellectual claim — an honest, precisely diagnosed
non-closure of the mandate, with real new content (`D_0(γ)`, the
equivalence lemma, a second independent heuristic route for `E(γ)`) and
correctly labeled tiers of certainty — survives this review intact,
modulo the one correction above.

---

## Files in this directory

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `01_lemma_E_symbolic.py` / `.log` | independent symbolic re-derivation of Lemma E (§A) |
| `02_lemma_D0_check.py` / `.log` | Lemma D0 value + error-order check, `mpmath` dps=50 (§B) |
| `03_E_gamma_heuristic_symbolic.py` / `.log` | independent symbolic re-derivation of §4's `E(γ)` heuristic match (§C) |
| `04_full_Sn_independent.py` / `.log` | fresh `S_n=Σ_kA_k` evaluator (`O(1)`-per-term cumulative-log trick), §6.3/§6.5 reproduction (§E) |
| `05_sec4_pointwise_consistency.py` / `.log` | pointwise `A_k` vs `Q(k;n,γ)` consistency check (§C) |

No Monte Carlo / randomized code was needed for this review — every check
above is either exact symbolic algebra (`sympy`) or deterministic
high-precision numerics (`mpmath`/`float64`), so the reserved seed range
`20260873000+` was not drawn from. No `.py` script of any prior front, or
of this front's own numbered scripts, was opened, read, or imported at
any point in this review. No git commits made by this review.
