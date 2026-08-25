# ADVERSARIAL REFEREE REPORT — wave 17, front (b) `SHARP-RATE-REASSEMBLY-ATTEMPT` (`DISC-DEC-072`)

**Object under test:** `sharp_rate_reassembly_attempt/ATTEMPT.md` —
Teorema R (`|φ(n,c) − φ_∞(c)| ≤ [a*√c + κ_B]/n` for every integer `n≥4`
and real `0≤c≤n`, strict on `(0,n]`, with `a* = √π(1/√2−1/2)` and
`κ_B = sup_{c≥0} c²I₂(c) ∈ (0.28048, 0.2805)` unchanged from Estágio 12),
plus the structural claim that the Estágio 12 assembly consumes the
constant `a` at exactly one step, so Estágio 19's sharp `(U′)` substitutes
verbatim.

**Referee discipline.** This review was hostile and independent. I read,
in full, the target ATTEMPT.md and the *prose* of every cited background
document (`THEOREM.md` Estágios 9–13, 19 and §§3–5, §7 incl. Definition 1/4,
Fact 4.1, Lemma 2, Corolários 4.1–4.2; `uniform_in_c_attempt/ATTEMPT.md`
§§5–7 and its `adversarial/REFEREE_REPORT.md` §4;
`u_prime_hypothesis_attempt/ATTEMPT.md` in full;
`sharp_constant_attempt/ATTEMPT.md`;
`sharp_constant_monotonicity_attempt/ATTEMPT.md` with all dated addenda and
its `adversarial/REFEREE_REPORT.md`, esp. §8). **No `.py` script of the
target front or of any prior front was opened** — the engine, the
brute-force enumerator, the `Q(n)` code, the certified brackets, the κ_B
branch-and-bound, and every verification below were rebuilt from scratch
from the prose statements alone (`ref_engine.py`, this directory). All
load-bearing arithmetic is exact `fractions.Fraction`/integer, with
transcendentals replaced by certified rational brackets (integer-squaring
square roots; `π ∈ (3.14159265358979, 3.14159265358980)`; `e > 2`), always
rounded in the conservative direction (LHS up, RHS down). `mpmath`/`sympy`
appear only in explicitly non-load-bearing display/symbolic checks.
Seeds: `20260863000+` is reserved for this referee (grep-confirmed to
appear only in `DECISION_LEDGER.yaml` line 4782 and `TEST_QUEUE.yaml` line
3063, the reservation lines); the object is fully deterministic and every
check is exact/certified, so the seeds were **reserved-unused** (§ Seeds).

---

## VERDICT (read first)

> **SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**
>
> Teorema R survives a deliberate attempt to break it. Every one of the
> mandated attacks was executed and none found a mathematical error:
> the §2 trace of the Estágio 12 assembly is **accurate against the
> source prose** (the constant `a` enters Teorema B's proof at exactly
> one step, as a black box over the full Binomial support `0≤K≤n`, and
> the additive constant `κ_B` is manufactured entirely inside the `B_n`
> half, which never references `(U′)` or `a`); the sharp `(U′)` input's
> three-case provenance is complete (the `K=n−1` case *is* covered by the
> generic case at `n=K+1`; the Estágio 19 referee's §8 boundary algebra
> was re-derived and re-certified here independently, including the
> certified `3c²<1` and `a*√67>3` endgames); the strictness claim
> survives at `c=n` (the Binomial degenerates to `K=n`, where sharp
> `(U′)` is strict); `κ_B ∈ (0.28048, 0.2805)` was **independently
> re-certified** by this referee's own rational branch-and-bound (which,
> notably, reproduces the target's leaf count 1525 and tightest clearance
> `1.79·10⁻⁸` at `c≈4.107` exactly) and the display value
> `0.280480169024586 @ 4.08675454645254` matches to all printed digits;
> and the final inequality was replicated head-on with this referee's own
> exact engine — validated against brute-force enumeration from
> Definition 4 — on **1 060 certified cells with zero violations**,
> including every near-boundary cell `c ∈ {n, n−¼, n−½, n−1}` on the
> interior grids and the boundary line `c=n` pushed to **`n = 50 000`**
> (beyond the target's own 30 000).
>
> **Two named issues, neither touching any theorem:**
> **R-1 (minor, must fix in cataloguing):** the target's headline
> validation statistic "worst observed `LHS/RHS = 0.970` at
> `(3000,3000)`" (VERDICT item 4 and the T4-total row) is **wrong as a
> maximum over its own stated cell set** — its own T4c cells at
> `n = 5000, 10⁴, 3·10⁴` have certified ratios `0.9767, 0.9834, 0.9904`
> (this referee's computation; any correct computation gives the same).
> The true worst over the target's grid is `≈0.9904` at `(30000,30000)`
> (`0.9926` at this referee's `(50000,50000)`). The error is in the
> *safe* direction for the theorem (all ratios remain `<1`, and it makes
> the tightness claim *stronger*), but the printed statistic is
> inaccurate — most plausibly the ratio tracker ran only over the
> exact-`Q` cells (`n≤3000`) and not the certified-truncated ones.
> **O-1 (nit, inherited):** ingredient I1 cites Fact 4.1 with domain
> `0≤c≤n`, while `THEOREM.md`'s printed Fact 4.1 restricts to `n>c`
> (`q=c/n ∈ (0,1)`). The endpoint `c=n` is covered by Definition 1's own
> `q = c/n ∧ 1` convention, is exactly the already-accepted Proposição
> 7.1 / Lema 5.1 instantiation, and was verified exactly here (brute
> force from Definition 4 at `n=4,5`, `K=n`; mixture endpoints
> `φ(n,n)=Q(n)/n` for `n=4..12`) — a citation-domain nit inherited from
> Estágio 12's own accepted usage, not new to this front.

---

## 1. §2 — the trace claim (attack 1)

Re-read `uniform_in_c_attempt/ATTEMPT.md` §6.2 (Teorema B) and its full
§5–§6 context. The entire proof of Teorema B, as printed there, is:

> `|A_n(c)| ≤ (a/n)·E[√Bin(n,c/n)] ≤ (a/n)·√(E[Bin]) = a√c/n` (Jensen),
> plus Corolário 6.2 (`|B_n| ≤ c²I₂(c)/n ≤ κ_B/n`).

Findings, step by step against the target's (S1)–(S6):

- **(S1)** The split `Δ_n = A_n + B_n` is `uniform_in_c` §5.1, an exact
  identity from (7.1)/(7.2); constant-free. ✔
- **(S2)–(S4)** The `A_n` chain is exactly the Jensen line above; the
  hypothesis `(U′_a)` is consumed **once**, uniformly over the support
  `{0,…,n}` of the Binomial, as a pure multiplicative constant. Nothing
  else in the proof — Lema 5.1, Lema 6.1, Corolário 6.2, the final
  triangle inequality, or the `sup_{[0,C]}` monotonicity remark —
  mentions `a` or any property of it beyond `(U′_a)` itself. ✔
- **(S5)** `κ_B` originates in Corolário 6.2 = Lema 5.1 (`B_n` integral
  form, `n≥1`, `0≤c≤n`) + Lema 6.1 (`n≥4`, `0≤x≤n`, applied at
  `x=ct²∈[0,c]⊆[0,n]`) + the sup over `c`. The `B_n` half contains no
  reference to `(U′)`, `A_n`, or `a`. **The structural-independence claim
  (§5.1 of the target) is verified: `κ* = κ_B` necessarily.** ✔
- **(S6)** The `C≤n` restriction in the sup form is indeed implicit in
  Estágio 12's preamble (`n≥4`, `0≤c≤n`); the target makes it explicit —
  an improvement, not a change. ✔

**No hidden dependence on the numerical value of `a` exists anywhere in
the old assembly.** The wave-11 referee report §4 (re-read) confirms all
of I1–I3, I5–I7 SOUND, exactly as the target's §1 table records.
Conclusion: the verbatim-substitution claim is **correct**.

## 2. §3 — the sharp `(U′)` input (attack 2)

Provenance audit against the source prose:

- **Generic `1≤K≤n−1`.** u_prime Theorem 2 proves `T(n,K)≥0` and
  nonincreasing in `n` on the full domain `n≥K+1` (elementary-symmetric-
  polynomial positivity — re-derived here and spot-verified exactly, 63
  cells, R2c), so `n|φ_n^{(K)}−φ_K| = T(n,K) ≤ T(K+1,K) = M_K`; Estágio
  19's Theorem 2 gives `M_K < a*√K` strictly.
  **The `K=n−1` case is covered by the generic case** — `n≥K+1` holds
  with equality, and `T(K+1,K)=M_K` is exactly the binding cell; no
  boundary argument is needed there (`φ_n^{(n−1)} = Q(n)/n` was verified
  through the engine's Lemma-A route for `n=2..40`, R1b). ✔
- **Boundary `K=n`.** The Estágio 19 referee's §8 argument was
  **re-derived from scratch** (R2e): upper side
  `Q(n)−nφ_n < a*√n − 1/3 + c/√n` with `c = (1/11)√(π/2)+√π/4`, via
  Theorem 1 (Estágio 19) and the conversion
  `nφ_n > (√π/2)·n/√(n+1) ≥ (√π/2)(√n − 1/(2√n))` from the `z_n`-bound
  plus `1/√(1+x) ≥ 1−x/2` on `[0,3]` (identity
  `(1−x/2)²(1+x)−1 = x²(x−3)/4` re-verified symbolically); certified
  `3c² < 1` (referee's own brackets: `c ≤ 0.5570512`,
  `3c² ≤ 0.9309179 < 1`), closing `n≥3`. Lower side via Theorem 5
  (`Q(n) ≥ √(πn/2)−6`, spot-verified exactly) and the `v_n`-bound:
  `nφ_n − Q(n) < 6 − a*√n ≤ a*√n` once `a*√n ≥ 3`; certified
  `a*_lo·√67_lo = 3.0047 > 3` (and `a*_hi·√66_hi = 2.982 < 3`, so 67 is
  the exact threshold). Finite remainder: `|Q(n)−nφ_n| < a*√n` verified
  **exactly** here for `n=1..600` dense plus sparse to `n=2000` (worst
  ratio `0.9803` at `n=2000`), and by certified truncated-`Q` brackets at
  `n = 5000, 10⁴, 3·10⁴, 5·10⁴` — zero violations; exact anchors `1/3`
  (`n=1`) and `13/30` (`n=2`) reproduced. ✔ (R2d/R2e)
- **`K=0`.** `φ_n^{(0)}=1=φ_0` (THEOREM.md (7.4)); difference `0`,
  consistent with `a*√0 = 0`. ✔
- **Independent scale on the generic binding case:** `M_K` identity
  (`T(K+1,K) = Q(K+1)−(K+1)φ_K`) exact for `K=1..300` (R2a);
  `0 < M_K < a*_lo√K_lo` certified for `K=1..1000` dense + sparse to
  `K=5000`, zero violations, max certified ratio **0.987255 at K=5000**
  — reproducing the target's own 0.9873 (R2b).

**The three cases exactly tile `{0,…,n}`, which is exactly what (S3)
consumes. The input is sound, strict for `K≥1`.**

## 3. §4 — Teorema R's proof (attack 3)

- **Jensen step.** `E[√X] ≤ √(E[X])` by concavity; `E[Bin(n,c/n)] = c`
  exactly (valid for all real `0≤c≤n`, `q=c/n≤1`). ✔
- **Strictness on `(0,n]`.** For `c∈(0,n)` every `b_K(c)>0`; at `c=n`
  the Binomial degenerates to the point mass at `K=n` — and sharp `(U′)`
  is *strict* at `K=n≥1` (boundary case above), so the middle inequality
  of the A-half chain stays strict; Jensen degrades to equality there
  (`E[√Bin]=√n=√c`) but is only ever used with `≤`. Strictness
  **survives at `c=n`.** ✔
- **B-half domain.** `x=ct² ∈ [0,c] ⊆ [0,n]` needs `c≤n` (used only
  here, plus `n≥4` for Lema 6.1) — stated correctly. ✔
- **Combine + sup form.** `a*√c+κ_B` nondecreasing in `c`; pointwise
  bound valid on `[0,C]⊆[0,n]`. ✔
- **Decimal form.** Certified here: `a*_hi = 0.36708712… < 0.3670873`
  and `κ_B < 0.2805` (§4 below) — both roundings in the correct
  direction. ✔
- **Numerics:** the inequality itself replicated at 1 060 certified
  cells, zero violations (§5 below).

One nit: the proof invokes I1–I3 "exact identities, `0≤c≤n`" — see O-1
(the `c=n` instance of Fact 4.1 is true and already accepted via Prop.
7.1/Lema 5.1, but the printed Fact 4.1 says `n>c`).

## 4. §5 — κ_B certification (attack 4) — `ref_check_kappa.py` / `.log`

Independent method, same structure (the natural one), own code:

- **Tail:** `c²I₂(c) ≤ (3/8)√(π/c)` (Gaussian fourth moment — the
  derivation by differentiating `∫₀^∞e^{-at²}dt` twice was checked by
  hand), decreasing; certified at `c=5.62`: `≤ 0.2803742 < 0.2805`
  (reproducing the target's printed 0.2803742 exactly) and at `c=6`:
  `≤ 0.2713505`.
- **Head `[0,5.62]`:** adaptive bisection with the certified interval
  bound `sup_{[c₁,c₂]} ≤ c₂²·I₂^hi(c₁)` (valid since `I₂` is decreasing
  in `c`), `I₂` bracketed by its exact alternating series
  `Σ(−c)^k/(k!(2k+5))` with the remainder dominated by the first omitted
  term (domination hypothesis asserted programmatically). Result:
  **1 525 certified leaves** (identical to the target's count — the same
  natural bisection), tightest clearance `1.789·10⁻⁸` on
  `[4.107121, 4.107292]` (target: `1.8·10⁻⁸` at `c≈4.107` ✔), zero
  failures. **`κ_B < 0.2805` CERTIFIED.**
- **Lower witness:** at `c₀=4.086754546`,
  `c₀²I₂(c₀) ∈ (0.280480169024586−ε, …+ε)` with certified series
  bracket, `> 0.28048`. **`κ_B > 0.28048` CERTIFIED.**
- **Display (non-load-bearing):** mpmath 50 dps, closed form
  `c²I₂(c) = c^{−1/2}[(3√π/8)erf(√c) − e^{−c}(3√c/4 + c^{3/2}/2)]`
  (verified against direct quadrature to `<10⁻⁵⁰`): argmax
  `c* = 4.08675454645254`, `κ_B = 0.280480169024586` — **both matching
  the target and the wave-11 referee to every printed digit.**

The target's claim that this upgrades wave-11's F-9 (float-level sup) to
a certified bracket is accurate.

## 5. §7/T4 — final-inequality replication (attack 5) — `ref_check_final_rate.py` / `.log`

Head-on replication with the referee engine: exact rational `φ(n,c)`
(mixture I1 over the referee's own `φ_n^{(K)}` table), `φ_∞(c)` by
certified series/tail brackets, conservative RHS
`(a*_lo·√c_lo + 0.28048)/n` (strictly smaller than the theorem's RHS, so
each PASS machine-proves the theorem's inequality at that cell):

- **Interior:** `n = 4..24` (all) and
  `{28,32,40,48,64,96,128,192,256,384,512}` × ~11–18 `c`-values spanning
  `(0,n]` **including `c = n, n−¼, n−½, n−1` at every `n`**, plus
  `n=1024` × 6 — 453 cells.
- **Boundary line `c=n`** via `φ(n,n)=Q(n)/n`: exact `n=4..600` +
  `{700,800,1000,1500,2000,3000}`; certified truncated-`Q` brackets at
  `n = 5000, 10⁴, 3·10⁴, 5·10⁴` (**50 000 — beyond the target's
  30 000**) — 607 cells.
- **Result: 1 060 certified cells, 0 violations.** Worst
  `LHS/RHS = 0.992553` at `(50000, 50000)`; on the target's own maximal
  cell `(30000,30000)`: `0.990398`. → finding **R-1** (the target's
  "max 0.970" is not the max of its own grid; see Verdict).
- **Halves separately (T4b analogue):** `n∈{8,32,128}` × 9 `c`-values:
  exact `A_n` vs `a*_lo√c_lo/n`; `B_n` bracket vs `c²I₂^lo(c)/n`
  (referee's `I₂` series bracket is valid through `c≤200`, so no analogue
  of the target's self-caught `c>60` bug); sign `B_n ≤ 0` (Lema 5.1);
  and the exact rational identity `Σ_K b_K φ_K = Σ_k C(n,k)(−c/n)^k/(2k+1)`
  — all pass, zero failures.

## 6. §6 — honesty of the sharpness assessment (attack 6) — `ref_check_sharpness.py` / `.log`

- **Asymptotic law along `c=n`:** from proved material —
  `Q(n) = A(n)/2 − θ(n)` with Robbins (two-sided) and FGKP95 Theorem 7
  (`θ(n) = 1/3 + Θ(1/n)`), so `Q(n) = √(πn/2) − 1/3 + O(1/√n)`;
  `nφ_∞(n) = (√π/2)√n − nR(n)` with `0<nR(n)<e^{−n}/2` (Corolário 4.2).
  Hence `n·Δ_n(n) = a*√n − 1/3 + o(1)` — the derivation is sound and the
  claimed provenance (Estágio 13/19 two-sided `Q` bounds + Cor. 4.2) is
  right. Numerically: `n·Δ_n(n) − (a*√n − 1/3)` = `+0.0102, +0.0033,
  +0.0019, +0.0010, +0.0006` at `n = 10², 10³, 3·10³, 10⁴, 3·10⁴` —
  clean decay to 0. Ratio to the bound: `0.8472, 0.9486, 0.9700, 0.9834,
  0.9904` — increasing, `<1` always; the target's quoted `0.847/0.949/
  0.970` reproduce exactly.
- **Scorecard honesty:** claim 8 is labelled "NUMERICALLY CHARACTERIZED
  + asymptotic argument … no formal optimality theorem is claimed" —
  accurate; claim 9 (κ_B optimality) NOT claimed — accurate.
- **Interior overshoot factor:** `a*/(√π/8) = 8(1/√2 − 1/2) = 4(√2−1)
  = 1.6568542` — exact identity confirmed symbolically and numerically.
- **Improvement factors:** `a/a* = 6.13836` (target: 6.1384 ✔);
  full-bound ratio `3.4697` at `c=0.5` (target: 3.47 ✔); T5 excerpt rows
  (`n=256`, `c∈{1,10,100,256}` and the `(3000,3000)` cell) reproduced
  **to every printed digit** from exact rationals (R5b).

## 7. Engine faithfulness (attack 7) — `ref_check_engine.py` / `.log`

The referee engine (closed forms re-typed from prose: Corolário A1 for
`ψ_n^{(K)}`, Proposição 2.1 for `ψ_n^{(K),R}`, Lemma A reduction, Wallis
`φ_K`, `Q(n)` from its definition) vs **brute-force enumeration from
Definition 4** (all `n!` permutations × all `n^K` destination vectors,
rerouted set fixed by the exchangeability stated in Definition 4; cyclic
set computed as the image of `f^n`):

- `n=4,5` all `K`; `n=6`, `K≤4`; `n=7`, `K≤2` — **19/19 exact matches**
  (e.g. `φ_5^{(5)} = 1569/3125 = Q(5)/5` from raw enumeration — an
  independent confirmation of I8 that bypasses Prop. 7.1 entirely).
- Anchors: `φ_n^{(1)} = 2/3+1/(3n²)` (`n≤50`); `ψ_n^{(1)} = 2/3+1/(6n)`,
  `ψ_n^{(1),R} = 1/2+1/(2n)`; `ψ_n^{(2)}`, `ψ_n^{(2),R} =
  (n+1)(5n+2)/(12n²)`, `φ_n^{(2)} = 8/15+1/(30n)+7/(10n²)+1/(5n³)`
  (Estágio 3, `n≤40`); `φ_n^{(n−1)} = Q(n)/n` via the closed-form route
  (`n≤40`); `φ_7^{(6)} = 355081/823543`; `φ_K` and `Q` anchors; mixture
  endpoints `φ(n,0)=1`, `φ(n,n)=Q(n)/n` (`n=4..12`); `φ_∞` bracket
  consistency across the series/tail crossover. **52 checks, 0 failures.**

## 8. §8 — the self-disclosed bug (attack 8)

Checked conceptually, without opening the target's scripts, against the
logic as *described*: the final-inequality check (T4a/T4c) needs exact
`φ(n,c)`, a `φ_∞` bracket, and lower bounds on `a*`, `√c`, `κ_B` — an
`I₂` **lower** bound enters only the per-half diagnostic
`|B_n| ≤ c²I₂(c)/n` (where a conservative check must shrink the RHS,
i.e. needs `I₂^lo`). A vacuous `I₂^lo = 0` at `c>60` therefore can
produce exactly the described spurious "B-half violations" at
`n=128, c≥64` while leaving T4a/T4c untouched. The disclosure is
**consistent and complete**; the referee's own B-half check (series
bracket valid to `c≤200`) passes at all tested cells including
`c=127,128` at `n=128`, confirming there was never a real B-half
violation to find.

## 9. Findings

| id | severity | finding |
|---|---|---|
| R-1 | minor (validation reporting; must fix wording at cataloguing) | "Worst observed `LHS/RHS = 0.970` at `(3000,3000)`" (VERDICT and T4-total row) is not the maximum over the target's own stated 2 594 cells: its T4c cells at `n=5000/10⁴/3·10⁴` have certified ratios `0.9767/0.9834/0.9904`. True max over the target grid `≈0.9904` (`0.9926` at this referee's added `(5·10⁴,5·10⁴)`). Safe direction — every ratio `<1`, tightness claim strengthened — but the printed statistic is wrong; likely the ratio tracker ran only over exact-`Q` cells. No theorem affected. |
| O-1 | nit (citation domain, inherited) | I1 cites Fact 4.1 on `0≤c≤n`; the printed Fact 4.1 (`THEOREM.md` §7.2) says `n>c`. The `c=n` instance is true (Definition 1's `q=c/n∧1`; degenerate Binomial; = Prop. 7.1/Lema 5.1's already-accepted usage) and was verified exactly here, incl. by raw brute force. Worth one clarifying line at cataloguing; inherited from Estágio 12, not introduced by this front. |
| — | none | No mathematical error, gap, misused citation, or overclaim found in §§1–6 of the target; §§8–10 disclosures accurate. |

## 10. Scorecard (target claims vs referee verdict)

| # | Target claim | Referee verdict |
|---|---|---|
| 1 | `a` enters the Estágio 12 assembly at exactly one step (S3); nothing else depends on its value | **CONFIRMED** against source prose (§1 above) |
| 2 | `κ* = κ_B` unchanged, by structural independence of the `B_n` half | **CONFIRMED** (§1) |
| 3 | `κ_B ∈ (0.28048, 0.2805)`, certified | **CONFIRMED by independent certification** (own b&b, 1 525 leaves, own witness; display value matched to all digits) |
| 4 | Teorema R, incl. strictness on `(0,n]` and the decimal form | **CONFIRMED** (proof re-derived; strictness at `c=n` audited; roundings certified; 1 060-cell replication, 0 violations) |
| 5 | Final inequality verified at scale, 0 violations | **CONFIRMED at comparable-to-higher power** (boundary to 50 000 > 30 000; near-boundary cells at every interior `n`) — except the max-ratio statistic, see R-1 |
| 6 | Sharp `(U′)` input, three-case provenance | **CONFIRMED**; `K=n−1` covered by generic case; boundary algebra independently re-derived and certified; 1 007-pt `M_K` check to `K=5000` reproduces the target's 0.9873 |
| 7 | Engine faithful to Definition 4 | **CONFIRMED** (referee's own engine vs referee's own brute force, 19/19 + 33 anchors) |
| 8 | §6 honesty (tightness asymptotics; no optimality theorem claimed) | **CONFIRMED**; asymptotic derivation sound; all quoted numbers reproduce |
| 9 | §8 bug confined to diagnostic | **CONFIRMED conceptually** (final-inequality logic provably never needs `I₂^lo`) |

## 11. Seeds

No randomness was used anywhere in this review: every object checked is
deterministic and every load-bearing check is exact rational or
certified-bracket arithmetic. Seed block `20260863000+` (referee
reservation, `DISC-DEC-072`) was grep-confirmed to appear only in the
ledger/queue reservation lines before work began, and is recorded here as
**reserved-unused**.

| seed | used for |
|---|---|
| `20260863000+` (reserved, referee, `DISC-DEC-072`) | N/A — no randomness anywhere in this review |

## 12. Files (all in this `adversarial/` directory; nothing outside it was created or modified; no git commits)

| file | role | scale / result |
|---|---|---|
| `ref_engine.py` | referee's from-prose engine: `φ_K`, `Q(n)` exact + certified truncated bracket, `ψ_n^{(K)}`/`ψ_n^{(K),R}`/`φ_n^{(K)}` closed forms, exact mixture `φ(n,c)`, certified `√`/π/`a*` brackets, `φ_∞` and `I₂` certified brackets, Definition-4 brute-force enumerator | module |
| `ref_check_engine.py` / `.log` | R1: engine vs brute force + prose anchors | 19/19 brute-force pairs + 33 anchor checks, **0 failures** |
| `ref_check_uprime.py` / `.log` | R2: sharp `(U′)` — `M_K` identity (300 exact), `M_K<a*√K` (1 007 certified pts to `K=5000`, max ratio 0.987255), interior monotonicity (63 cells), boundary `K=n` (610 pts, exact to `n=2000`, truncated to `n=5·10⁴`), §8 boundary algebra re-derivation (certified `3c²<1`, `a*√67>3`, conversion identity) | **0 violations** |
| `ref_check_kappa.py` / `.log` | R3: `κ_B ∈ (0.28048, 0.2805)` — own tail bound + own 1 525-leaf branch-and-bound + own witness; mpmath display | **CERTIFIED**; display `0.280480169024586 @ 4.08675454645254` matches |
| `ref_check_final_rate.py` / `.log` | R4: the final inequality, certified conservative — interior `n≤1024` incl. `c∈{n,n−¼,n−½,n−1}`, boundary `c=n` to `n=5·10⁴`; per-half checks + Lema 5.1 identity | **1 060 cells, 0 violations**; worst ratio 0.992553 at (50000,50000) |
| `ref_check_sharpness.py` / `.log` | R5: §6 arithmetic, T5 table replication, tightness trajectory, R-1 evidence | 22 checks, **0 failures** |

**Run order:** `ref_check_engine.py`, `ref_check_uprime.py`,
`ref_check_kappa.py`, `ref_check_final_rate.py`, `ref_check_sharpness.py`
(each independent; stdlib + `sympy` + `mpmath`, the latter two never
load-bearing). Total runtime ≈ 8 minutes, dominated by the `n=1024` exact
mixture table.

---

## Final verdict

**SOUND WITH NAMED ISSUES (R-1 minor, O-1 nit) — ACCEPT for catalogue.**
The re-assembly genuinely closes: Teorema R is correct as stated, its
proof consumes the sharp `(U′)` exactly as the trace claims, the additive
constant is `κ_B` unchanged for the structural reason given, and the
first certified bracket `κ_B ∈ (0.28048, 0.2805)` withstands independent
re-certification to the last printed digit. The one defect found is a
validation-reporting inaccuracy (the "worst ratio 0.970" statistic, R-1)
that should be corrected to `≈0.99` (at the largest boundary cells) when
catalogued — a correction that, if anything, sharpens the document's own
tightness story. No Millennium Problem claim anywhere; pure combinatorics
internal to this archive.
