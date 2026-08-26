# REFEREE REPORT — `GAMMA-SECOND-ORDER-GAP-CLOSURE-ATTEMPT`

**Target document:**
`.../gamma_scaling_attempt/gamma_second_order_attempt/gamma_second_order_gap_closure_attempt/ATTEMPT.md`
(wave 19, front (b), authorized by `DISC-DEC-083`).

**Referee discipline.** No `.py` file belonging to any front in this lineage
(this front's own `01`–`04` scripts, the predecessor's `01`–`05`, or the
wave-17 front's scripts) was opened, read, or imported at any point. Every
check below was rebuilt from scratch from the mathematical prose of
`THEOREM.md` (Estágio 23, lines 3903–4011; Estágio 26, lines 4322–4438) and
the predecessor `ATTEMPT.md` (all 633 lines, read in full including its
correction addendum) and the target `ATTEMPT.md` (all 479 lines, read in
full). `τ(m)`'s cubic form and `Δτ(k)`'s closed form were first derived by
hand (elementary algebra) before any code was written, then confirmed
symbolically. Seed-range check: `grep -rn "20260883" 05_DISCOVERY_LAB/` was
run before writing any code and found only reservation-label references
(this front's own `ATTEMPT.md` lines 84/462, `DECISION_LEDGER.yaml` line
5560, `TEST_QUEUE.yaml` line 3324) — confirmed unused. This referee drew
**zero** random seeds: every check performed is exact symbolic algebra
(`sympy`) or deterministic high-precision numerics (`mpmath`, dps=50), so no
seed from the reserved `20260883000+` block was needed. The reservation is
disclosed as unused, not silently abandoned.

---

## VERDICT

> **SOUND — ACCEPT for catalogue**, at exactly the tier claimed: Gap 2 (the
> `M`-fluctuation correction to `τ`), as literally stated in the
> predecessor's §5, is genuinely and rigorously closed, in a form strictly
> stronger than requested. No mathematical error, citation misuse, or
> overclaim was found anywhere in the target document's central chain
> (§2.2–2.5). Two bugs were found and fixed in this referee's **own**
> verification code (disclosed in full below, §D) — both caught before any
> conclusion was drawn from the buggy output, and neither affects the
> verdict once fixed. One clarifying observation is raised (not a defect):
> the `O(n^{-1/2})` bound established in §2.5 is genuinely proved only
> **pointwise in `γ`**, not uniformly on `(0,1)`, and the document's own
> `γ=0.99` numerics honestly display this — but this does not weaken the
> claimed closure, because the predecessor's Gap 2, as literally worded,
> never asked for uniformity in `γ`, only in `k` (at fixed `γ`), and the
> target document delivers uniformity in `k` over the *entire* range
> `1≤k≤n`, a strict superset of what was asked. This is recorded as a named
> scope clarification in §E below, not a named issue against the front.
>
> No claim of progress on any Millennium Problem is made anywhere in the
> target document or in this report; this is pure combinatorial mathematics
> internal to this archive, concerning a specific
> random-permutation-with-reroutes ensemble.

---

## A. Independent re-derivation of `τ(m)`'s cubic closed form (claim 1)

**By hand, before any code.** `τ(m) = (1/n²)Σ_{i=1}^m(k-i)²`. Expanding
`(k-i)² = k²-2ki+i²` and summing termwise with the classical
`Σi = m(m+1)/2`, `Σi² = m(m+1)(2m+1)/6`:

`Σ_{i=1}^m(k-i)² = mk² - km(m+1) + m(m+1)(2m+1)/6`

Expanding `km(m+1) = km²+km` and `m(m+1)(2m+1)/6 = m³/3+m²/2+m/6`, and
collecting by power of `m`:

`= m³/3 + m²(1/2-k) + m(k²-k+1/6)`

— **exactly** the document's claim 1. Confirmed a second way, symbolically,
in `adv01_symbolic_delta_tau.py` Part A: `sympy.summation` of the defining
sum minus the claimed cubic form, simplified to exactly `0` for general
symbolic `m,k,n`. **PASS — claim 1 fully confirmed, independently, by hand
and symbolically.**

---

## B. Independent re-derivation of `Δτ(k)`'s closed form (claim 2)

**By hand.** Substituting the cubic form of §A at `m=M` and `m=γk`,
subtracting, and using linearity of expectation with the classical Binomial
raw moments `E[M]=kγ`, `E[M²]=k(k-1)γ²+kγ`,
`E[M³]=k(k-1)(k-2)γ³+3k(k-1)γ²+kγ`: the linear-in-`m` term of `τ` drops out
exactly because `E[M]-γk=0`. Working through the remaining quadratic and
cubic pieces (`E[M²]-(γk)²=kγ(1-γ)`;
`E[M³]-(γk)³=3γ²(1-γ)k²+γ(1-γ)(1-2γ)k`, itself hand-verified by direct
expansion) and collecting by power of `k` gives, after simplification,

`Δτ(k) = [-k²γ(1-γ)² + (1/6)kγ(1-γ)(5-4γ)]/n²`

— **exactly** the document's claim 2, matching digit-for-digit by hand
before any code was run.

**Confirmed independently three further ways**, all in
`adv01_symbolic_delta_tau.py`:

1. **Part C route 1 (moment substitution, general symbolic `k`,`γ`):**
   `sympy.simplify` of (moment-substituted `E_M[τ(M)]` minus `τ(γk)`) minus
   the claimed closed form gives exactly `0`.
2. **Part C route 2 (direct pmf summation, `k=1..6`, symbolic in `γ`,
   structurally independent of route 1 — never invokes the general raw-
   moment formulas):** `Σ_{m=0}^kC(k,m)γ^m(1-γ)^{k-m}τ(m) - τ(γk)` computed
   by direct symbolic summation, matches the closed form exactly (`diff=0`)
   at every `k=1,...,6`.
3. **Part D (exact 3rd-order Taylor reconstruction — a genuine third
   route, not just a restatement):** since `τ` is an exact cubic
   polynomial, `τ''(γk)·Var(M)/2 + τ'''(γk)·μ₃(M)/6` (using the classical
   central moments `Var(M)=kγ(1-γ)`, `μ₃(M)=kγ(1-γ)(1-2γ)`) must equal
   `Δτ(k)` **exactly**, with zero remainder — confirmed symbolically,
   `diff=0`.

All four independent derivations (hand + 3 symbolic routes) agree exactly.
**Independent numeric cross-check** (own script, mpmath dps=50, direct
weighted Binomial-pmf summation over `m=0..k`, `k` up to a few hundred,
`n` up to `10^5`, never using the closed form to compute — only to
compare) also confirmed agreement to the dps=50 rounding floor (details in
§D below, where a bug in an earlier version of this exact script is
disclosed). **PASS — claim 2 fully confirmed, four independent ways.**

---

## C. Independent verification of Lemma G2 (claim 3)

### C.1 The differentiation step — is it justified?

**By hand.** Start from Lemma D0's cited Poisson-summation identity
(already PROVED in Estágio 26, used here as a black box):
`Σ_{k=-∞}^∞e^{-ak²} = √(π/a)·θ(a)`, `θ(a):=Σ_me^{-π²m²/a}`. For `a` in a
compact interval `[a₀,a₁]⊂(0,∞)`: both `Σ_ke^{-ak²}` and its termwise
derivative series `Σ_k k²e^{-ak²}` converge **uniformly** on `[a₀,a₁]`, by
the Weierstrass M-test — `k²e^{-ak²}≤k²e^{-a₀k²}` for `a≥a₀`, and
`Σ_kk²e^{-a₀k²}<∞`. By the standard theorem (termwise differentiation is
valid when the differentiated series converges uniformly and the original
series converges at one point), differentiating termwise is legitimate on
every such compact subinterval, hence on all of `(0,∞)`. **This referee
agrees: the document's justification is valid and sufficient — no gap
here.** Carrying out the differentiation:

`-d/da[Σ_ke^{-ak²}] = Σ_kk²e^{-ak²}` (LHS)

`d/da[√(π/a)θ(a)] = -½√π·a^{-3/2}θ(a) + √(π/a)θ'(a)`, `θ'(a)=Σ_{m≠0}e^{-π²m²/a}(π²m²/a²)`

Since `θ(a)=1+O(e^{-π²/a})` and `θ'(a)=O(a^{-2}e^{-π²/a})` as `a→0+`, and
summing over `k≥1` (the `k=0` term contributes `0`, halving by evenness):

`Σ_{k=1}^∞k²e^{-ak²} = (√π/4)a^{-3/2} + O(a^{-5/2}e^{-π²/a})`

— **exactly** the document's Lemma G2, confirmed by hand independently.

### C.2 Numeric cross-check (own script, `adv02_lemma_g2.py`, mpmath dps=50)

**Infinite-sum form**, `a∈{0.1,0.01,0.001,0.0001}`: direct summation
(kmax chosen from `a` and dps to guarantee tail negligibility) vs.
`(√π/4)a^{-3/2}`. Relative differences: `5.4×10^{-41}`, `4.6×10^{-51}`,
`1.6×10^{-51}`, `3.2×10^{-51}` — indistinguishable from `0` at the dps=50
floor at every tested `a`.

**Finite-`n` truncated form** (the one actually used downstream),
`γ∈{0.1,...,1.0}`, `n∈{2000,20000,200000}`: `Σ_{k=1}^nk²e^{-βk²/n}` vs.
`(√π/4)(n/β)^{3/2}`, relative differences uniformly `~10^{-50}` to
`10^{-51}` across all 18 `(γ,n)` pairs — matches the document's own
reported `~10^{-50}` claim exactly.

**Tail sanity check** (own addition, not in the document): confirmed
directly that `Σ_{k=1}^∞ - Σ_{k=1}^n` (the `k>n` tail) is of order
`10^{-45}`–`10^{-46}` at `n=2000`, i.e. utterly negligible relative to the
finite sum (`~10^5`–`10^6`) — the exponential-tail claim used to justify
truncating the infinite sum at `n` is numerically confirmed, not merely
asserted.

**PASS — Lemma G2 fully confirmed, both by hand-derivation and independent
high-precision numerics, both forms.**

---

## D. Independent verification of the combination step §2.5 (claim 4)

### D.1 The bound `e^{-s(k)}=e^{-βk²/n}e^{γk/(2n)}≤e^{-βk²/n}e^{γ/2}` for `k≤n`

Algebraically trivial (`γk/(2n)` is increasing in `k∈[0,n]`, maximized at
`k=n` giving `γ/2`) — but checked exhaustively anyway, not just asserted:
own script swept `γ∈{0.1,0.5,0.9,0.99}`, `k=1,...,500`, **zero
violations**. **PASS.**

### D.2 The algebra of the combined bound

By hand: `|Σ_ke^{-s(k)}Δτ(k)| ≤ Σ_ke^{-s(k)}|Δτ(k)| ≤
e^{γ/2}[γ(1-γ)²/n²·Σk²e^{-βk²/n} + γ(1-γ)(5-4γ)/(6n²)·Σke^{-βk²/n}]`.
Substituting Lemma G2 (`Σk²e^{-βk²/n}=Θ(n^{3/2})`) into the first term gives
`Θ(n^{-1/2})`; substituting the predecessor's already-cited
`Σke^{-βk²/n}~n/(2β)=Θ(n)` into the second term gives `Θ(n^{-1})`, strictly
subdominant. Total: `O(n^{-1/2})`. **The algebra is correct — confirmed
independently by hand.**

### D.3 Direct numeric confirmation, no shortcut (own script, `adv03_combination.py`, mpmath dps=50)

`W_n(γ):=Σ_{k=1}^ne^{-s(k)}|Δτ(k)|` was recomputed from scratch (own
re-implementation of `s(k)` and `Δτ(k)` from their own closed-form
definitions, no reuse of `adv02`'s cached sums), `γ∈{0.1,0.3,0.5,0.7,0.9,
0.99}`, `n∈{1000,10000,100000}`. Result — **bit-for-bit identical to the
target document's own §2.5 table**:

| `γ` | `W_n/W_{10n}` (this referee) | (document) | `W_{10n}/W_{100n}` (this referee) | (document) |
|---|---|---|---|---|
| 0.1 | 3.1544624 | 3.154462 | 3.1598222 | 3.159822 |
| 0.3 | 3.1497255 | 3.149726 | 3.1583558 | 3.158356 |
| 0.5 | 3.1461363 | 3.146136 | 3.1572581 | 3.157258 |
| 0.7 | 3.1380046 | 3.138005 | 3.1547508 | 3.154751 |
| 0.9 | 3.0822303 | 3.082230 | 3.1375382 | 3.137538 |
| 0.99| 2.2582227 | 2.258223 | 2.8701481 | 2.870148 |

Every ratio converges toward `√10=3.16227766` — the `O(n^{-1/2})`
signature — at every `γ`, exactly reproducing the document's own numbers
to the digits shown. The **signed correction**
`Corr_n(γ):=Σ_ke^{-s(k)}(-Δτ(k)/2)` was also independently tracked to
`n=10^6` (own script goes one `γ` further than needed): at `γ=0.5`,
`3.79×10^{-3}`(`n=10³`)`→1.21×10^{-4}`(`n=10^6`) — matching the document's
quoted numbers exactly, and monotone shrinkage confirmed at all six tested
`γ`. **PASS — claim 4 fully confirmed, independent code, bit-for-bit
agreement.**

### D.4 Bugs found in this referee's own verification code (disclosed)

Two bugs were found and fixed in `adv01_symbolic_delta_tau.py` **before**
any conclusion was drawn from its output — both are disclosed here in full,
per the mandate:

1. **Unsubstituted free symbol.** The first version of the route-2 (direct
   pmf summation) check defined a helper `tau_of(m)` closing over the
   *symbolic* variable `k`, and the loop iterated over concrete integer
   values `kk=1,...,6` without substituting `k→kk` inside `tau_of`'s own
   body before comparing to the closed form (which *was* correctly
   evaluated at `k=kk`). This produced six spurious nonzero "differences"
   that were in fact just leftover `k` vs `kk` mismatch, not a real
   disagreement with the document's claim. **Fixed** by explicitly
   `.subs(k, kk)` inside the helper before use; all six cases then matched
   exactly (`diff=0`).
2. **Silent float leakage from mixed Python/sympy integer arithmetic.**
   After fixing bug 1, a second, smaller discrepancy appeared at `k=2`
   only (`~10^{-15}` relative), traced to plain Python `int` values (from
   `range()`) being used directly in expressions like `mval**3/3`: when
   *neither* operand of a division is yet a `sympy` object, Python
   performs the division in pure floating-point *before* sympy ever sees
   it (e.g. `8/3 → 2.6666...` as a float, not `Rational(8,3)`), silently
   contaminating an otherwise-exact symbolic computation with a tiny
   float residual. **Fixed** by wrapping every concrete integer (`kk` and
   each `m`-value) in `sp.Integer(...)` before any arithmetic; all six
   `k=1,...,6` cases then matched exactly (`diff=0`, confirmed in the
   final script and log now in this `adversarial/` directory). This is a
   general trap worth naming for future fronts in this lineage that mix
   Python-native loop indices with `sympy` symbolic expressions.

No bugs were found in `adv02_lemma_g2.py` or `adv03_combination.py`
(numeric-only mpmath scripts, no symbolic/float-mixing risk); no bugs found
in the target document's own mathematics.

---

## E. Assessment of the gap-closure claim and its scope (claims 5, 9, 10)

### E.1 Is Gap 2, as the predecessor actually stated it, genuinely and fully discharged?

**Yes.** Re-reading the predecessor's §5 verbatim (also quoted verbatim in
the target document's own §1): Gap 2 asks for
`E_M[τ(M)] = τ(γk) + O(n^{-3/4})`, **uniformly for `k≤K∼√(n ln n)`**. The
word "uniformly" there refers unambiguously to uniformity **in `k`**, at
fixed `γ` — there is no mention of uniformity in `γ` anywhere in the
predecessor's Gap 2 wording (checked by re-reading the full §5 block, lines
402–412, of the predecessor `ATTEMPT.md`). The target document delivers an
**exact closed form** (not merely a bound) valid for **every**
`1≤k≤n` — a strict superset of `k≤K` (since `K≤n` for all `n` large enough
that `√(n ln n)≤n`, true for `n≥1`) — with pointwise order `O(k²/n²)`,
which at `k=K∼√(n ln n)` gives `O((ln n)/n)`, genuinely smaller than the
requested `O(n^{-3/4})` (since `(ln n)/n = o(n^{-3/4})`, hand-checked: this
is equivalent to `ln n = o(n^{1/4})`, standard). **The closure is real,
correctly scoped to what was actually asked, and strictly stronger in both
the pointwise order and the range of `k` covered.**

### E.2 The `γ=0.99` slow-convergence disclosure — does it undermine claim 4?

**No, but it is worth naming precisely, which this report now does.** The
`O(n^{-1/2})` bound of §2.5 is established, both in the document and in
this referee's independent re-derivation (§D above), for **each fixed
`γ`** — Lemma G2 itself is a fixed-`a` (hence fixed-`γ`) asymptotic
statement, and the triangle-inequality bound assembling it uses the
`γ`-uniform but crude prefactor `e^{γ/2}≤e^{1/2}`. Neither step, as
written, produces a bound of the form
`sup_{γ∈(0,1)}n^{1/2}W_n(γ)≤C` **uniform in `γ`** — and the `γ=0.99` row
of the document's own table (ratio `2.258→2.870` across two doublings of
`n`, visibly still short of `√10=3.162`) is direct numerical evidence that
no such uniform bound is established: the *rate at which* the `n^{-1/2}`
asymptotic regime is reached degrades as `γ→1` (because the leading
coefficient `γ(1-γ)²` in the dominant term of the bound vanishes as
`γ→1`, so subleading finite-`n` corrections are relatively larger there at
any fixed `n`, requiring larger `n` before the asymptotic ratio is
visible). This referee independently confirmed the same qualitative
pattern (§D.3 table above) with bit-for-bit matching numbers.

**Why this does not weaken the claimed closure:** as established in §E.1,
the predecessor's Gap 2 never asked for uniformity in `γ` — only in `k`,
at fixed `γ`. A pointwise-in-`γ` `O(n^{-1/2})` result, for every fixed
`γ∈(0,1)`, is exactly what is needed to justify, for each fixed `γ`, that
the `n→∞` limit defining `E(γ)` is unaffected by the `τ(M)→τ(γk)`
substitution — which is the actual role Gap 2 plays in the larger
derivation (recall `C(γ)` itself, per Estágio 23/26, is a fixed-`γ`,
`n→∞` limit; uniformity in `γ` was never part of *this* piece's job,
unlike the wave-17 front's own separate, already-discharged bonus target
of uniformity on compacts `[γ₀,1]` for the *first-order* law). The target
document does not claim `γ`-uniformity for this result, and correctly does
not need to.

**One genuine scope note for the record** (not a defect in the target
document, but worth flagging for whoever eventually attempts the full
`C(γ)` proof): if a future front wants a version of Gap 2's closure that
is uniform on compact `γ`-subintervals `[γ₀,γ₁]⊂(0,1)` — e.g. to support a
`γ`-uniform version of the overall `C(γ)` theorem, echoing the wave-17
front's own Corollary 1 for the first-order law — the bound as currently
proved does **not** automatically supply that; the `γ(1-γ)²→0` vanishing
of the leading coefficient as `γ→1` (and, symmetrically, an analogous
degeneracy could arise as `γ→0`, not tested numerically here since the
document's own table stops at `γ=0.1`) would need separate treatment. This
is explicitly **not** a claim the target document makes, so it is not a
finding against it — it is flagged here only because the mandate
specifically asked whether the uniformity question is genuinely
independent of Gap 3, and the answer is: yes, independent, but a *related*
uniformity-in-`γ` question does lurk one level further out, outside both
Gap 2 and Gap 3 as currently named.

### E.3 Does closing Gap 2 for `1≤k≤n` logically pre-discharge part of Gap 3?

**Yes, and the reasoning is sound.** Gap 3, as stated by the predecessor,
is specifically about *extending* Gaps 1–2's bounds from the "typical"
scale `k=Θ(√n)` to the full truncation range `k≤K∼√(n ln n)` — i.e., Gap 3
is a bookkeeping step needed only because Gaps 1–2, as originally
sketched, were derived only at the typical scale. Since the target
document's Gap 2 closure is an **exact identity** derived directly and
without any typical-scale restriction — it holds for literally every
`1≤k≤n` by construction (§2.3), and its weighted sum (§2.4–2.5) is also
bounded directly over the full range `k=1,...,n`, never restricted to
`k=Θ(√n)` at any intermediate step — there is no "typical scale" version
of this particular result that needs separate extension. The document's
claim that this "pre-discharges" the τ-piece of Gap 3 is therefore not an
optimistic gloss; it is a direct structural consequence of *how* the proof
was carried out (globally from the start, not locally-then-extended). This
referee finds no logical gap in this reasoning. The document is also
careful to scope this correctly: it explicitly does **not** claim any part
of Gap 1's contribution to Gap 3 is discharged, which is correct — Gap 1
was untouched by this front.

### E.4 Overall verdict claims (claim 5)

- **Gap 2 fully closed**: confirmed, §A–D above.
- **Gap 1 untouched, now the dominant obstacle**: confirmed untouched (no
  claim in the target document bears on `δ(M)`, the transcendental piece);
  the qualitative assessment that it is "harder" is a reasonable
  diagnostic judgment, correctly presented as an assessment rather than a
  proved fact, and consistent with the structural difference (transcendental
  exponential vs. exact polynomial) — this referee agrees with the
  characterization.
- **Gap 3 partially discharged (τ-piece only)**: confirmed sound, §E.3.
- **`C(γ)` for `γ∈(0,1)` remains fully open**: confirmed — nothing in the
  target document, nor in this referee's independent checks, closes any
  part of the transcendental (Gap 1) half of the derivation, and the
  document is explicit and consistent about this throughout (verdict
  block, §3, §6 scorecard, "what remains open" list — no internal
  contradiction found).

---

## F. Summary of numeric results (all reproduced independently, own code)

| Quantity | This referee | Target document | Agreement |
|---|---|---|---|
| `τ(m)` cubic form (symbolic, general `m,k,n`) | diff `=0` | claimed exact | exact match |
| `Δτ(k)` closed form, route 1 (moment sub.) | diff `=0` | claimed exact | exact match |
| `Δτ(k)` closed form, route 2 (direct pmf, `k=1..6`) | diff `=0` (after fixing 2 own bugs) | diff `=0` | exact match |
| `Δτ(k)` closed form, route 3 (exact Taylor, own addition) | diff `=0` | diff `=0` (doc's own route 3) | exact match |
| Lemma G2, infinite sum, `a=0.1,...,10^{-4}` | reldiff `~10^{-41}`–`10^{-51}` | "`~10^{-40}`–`10^{-50}`" | consistent |
| Lemma G2, finite-`n` sum, 18 `(γ,n)` pairs | reldiff `~10^{-50}`–`10^{-51}` | "`~10^{-50}`" | exact match |
| `e^{-s(k)}≤e^{-βk²/n}e^{γ/2}` violations, `k≤500`, 4 `γ` | 0 | 0 (asserted) | exact match |
| `W_n/W_{10n}` ratios, 6 `γ` values, two doublings | bit-for-bit table, §D.3 | same table, §2.5 | exact match |
| `Corr_n(γ=0.5)`, `n=10^3→10^6` | `3.79×10^{-3}→1.21×10^{-4}` | `3.79×10^{-3}→1.21×10^{-4}` | exact match |

---

## G. Final scorecard (this referee's own)

| Claim | Referee verdict |
|---|---|
| 1. `τ(m)` exact cubic closed form | **CONFIRMED** — by hand and symbolically |
| 2. `Δτ(k)` exact closed form | **CONFIRMED** — by hand and via 3 independent symbolic routes + numeric cross-check |
| 3. Lemma G2 (differentiated Poisson summation) | **CONFIRMED** — differentiation step justified (uniform convergence on compacts, agreed valid), formula confirmed by hand and to `~10^{-50}` numerically, both infinite and finite-`n` forms |
| 4. `Σ_ke^{-s(k)}Δτ(k)=O(n^{-1/2})→0` | **CONFIRMED** — bound algebra correct (hand-checked), numerics bit-for-bit reproduced independently, `n^{-1/2}` signature (`√10` ratio test) confirmed at all 6 tested `γ` |
| 5. Gap 2 fully/rigorously closed, stronger than requested | **CONFIRMED**, correctly scoped (§E.1) |
| Gap 1 untouched, now dominant obstacle | **CONFIRMED untouched**; "dominant" is a reasonable, correctly-labeled assessment |
| Gap 3 partially discharged (τ-piece) | **CONFIRMED sound**, logic verified (§E.3) |
| `C(γ)` for `γ∈(0,1)` remains open | **CONFIRMED** — no part of Gap 1 touched by this front or found closed by this referee |
| Seeds `20260883000+` reservation | **CONFIRMED unused**, no conflict found; this referee also drew zero seeds (no randomness needed for any check performed) |

**No mathematical error, citation misuse, or overclaim was found in the
target document.** Two bugs were found and fixed in this referee's own
verification code (§D.4), both caught before drawing any conclusion from
buggy output, and neither changes any verdict once corrected. One
clarifying scope note is recorded (§E.2) — pointwise-in-`γ`, not
uniform-in-`γ`, `O(n^{-1/2})` — which the target document's own numerics
already display honestly and which does not weaken its claimed closure of
Gap 2 as literally stated.

## VERDICT (repeated)

> **SOUND — ACCEPT for catalogue**, at the tier claimed: Gap 2 closed
> fully and rigorously, in a form strictly stronger than requested; Gap 1
> correctly identified as untouched and now the dominant remaining
> obstacle; Gap 3 correctly assessed as partially (not fully) discharged;
> `C(γ)` for `γ∈(0,1)` correctly and consistently reported as still open
> throughout. No claim of progress on any Millennium Problem; pure
> combinatorial mathematics internal to this archive, about a specific
> random-permutation-with-reroutes ensemble.

---

## Files in this directory

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `adv01_symbolic_delta_tau.py` / `.log` | fresh symbolic (`sympy`) re-derivation: `τ(m)` cubic form; classical Binomial raw moments `k=1..6`; `Δτ(k)` via two independent routes (moment substitution, direct pmf summation) plus a third exact-Taylor-reconstruction consistency check; includes the two self-caught-and-fixed bugs described in §D.4, left visible in comments |
| `adv02_lemma_g2.py` / `.log` | fresh numeric (`mpmath` dps=50) verification of Lemma G2, infinite-sum and finite-`n` truncated forms, plus an added tail-negligibility sanity check not present in the target document |
| `adv03_combination.py` / `.log` | fresh numeric (`mpmath` dps=50) direct summation of `W_n(γ)` and `Corr_n(γ)`, the `e^{-s(k)}` bound-violation sweep, and the `n→10n→100n` ratio test, reproducing the target document's §2.5 table bit-for-bit |

No `.py` file of any prior front (this lineage or any other) was opened,
read, or imported at any point in producing this report. No git commands
were run. `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, and
`DISCOVERY_LAB_STATE.md` were not touched. No claim of progress on any
Millennium Problem anywhere in this report.
