# REFEREE REPORT — `GAMMA-SCALING-LAW-ATTEMPT` (`DISC-DEC-072`, wave 17 front (e))

**Object under test:**
`05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/gamma_scaling_attempt/ATTEMPT.md`
— claims the γ-scaling law `φ(n,γn)/φ_∞(γn) → √(2/(2−γ))`, `c=γn`, fixed
`γ ∈ (0,1]`.

**Note on provenance of this report.** A prior background-agent instance
of this same referee assignment stalled after producing partial scratch
files (`ref01…ref05`) in this directory but no report. Per dispatch
instructions, none of those `ref0*.py`/`.json`/`.log` files were opened,
read, or imported at any point in this review — every check below
(`av01`–`av05`) was rebuilt entirely from scratch, from ATTEMPT.md's and
THEOREM.md's prose alone.

---

## VERDICT

> ## **SOUND — ACCEPT for catalogue**, at the tier ATTEMPT.md itself
> claims: **Theorem 2 (the full mandate, `γ∈(0,1]`) is PROVED**, both
> stretch goals (**Corollary 1**, uniformity on compacts of `(0,1]`, and
> **Corollary 2**, moving `γ_n→0`) are **PROVED**, and the bonus
> second-order term is correctly, explicitly labeled **PROVED only at
> `γ=1`** and **CONJECTURED (not proved) for `γ∈(0,1)`** — the document
> does not overclaim anywhere it was checked. No mathematical error,
> citation misuse, or overclaim was found in the object under test.

No named issues rise to a correctness problem. Two minor **observations**
(not defects) are recorded in §6.

---

## 1. What was actually claimed (read in full before any code)

ATTEMPT.md attacks the open item recorded at THEOREM.md, Estágio 10
("Sobre `c` crescendo com `n`... `φ(n,c)/φ_∞(c)→√(2/(2−γ))`, provado no
extremo `γ=1`... caracterizado numericamente para `γ∈(0,1)`"), reaffirmed
still-open through Estágio 22 ("a lei de escala `γ∈(0,1)` (sob revisão na
onda 17)"). This front claims a **full proof**, not a partial result and
not honest non-closure:

- **Theorem 2**: `φ(n,γn)/φ_∞(γn) → √(2/(2−γ))` for every fixed
  `γ∈(0,1]`, rate `O_γ(n^{-1/4})`, via a brand-new exact finite-`n`
  double-sum formula (**Lemma 1**) derived from scratch from Definition 1
  of THEOREM.md, NOT from the Estágio 9/12/22 machinery (explicitly
  disclaimed as structurally too weak for the relative-ratio question at
  `c=γn`, since its absolute rate `a√c/n` is `Θ(n^{-1/2})`, the same
  order as `φ_∞(γn)` itself — I checked this diagnosis by hand, §3.1).
- **Corollary 1** (stretch 1): uniform convergence on every compact
  `[γ_0,1]⊂(0,1]`.
- **Corollary 2** (stretch 2): moving `γ_n→0` with
  `γ_n n^{1/3}/\ln n → ∞` still gives the law, and the ratio → 1 as
  `γ_n→0` — matching `√(2/(2−0))=1`.
- **Corollary 3**: `γ=1` endpoint independently re-derived (`√2`,
  `φ(n,n)=Q(n)/n`), consistent with, but not claimed to improve, the
  archive's existing sharp-rate results.
- **Bonus**: a second-order constant `C(γ)`, PROVED only at `γ=1`
  (reduces to the archive's own `-2/(3√π)`), CONJECTURED elsewhere —
  correctly not folded into the main scorecard as proved.
- Named residual gap disclosed: the intermediate window
  `n^ε ≤ c_n ≤ n^{2/3}/\log` between the fixed-`c` regime and Corollary
  2's `γ_n ≥ n^{-1/3}\ln n` regime is left open, explicitly.

## 2. Full re-read of THEOREM.md's cited machinery

Read in full: Definition 1 (§1), Definition 3/`φ_∞` construction (§2),
Theorem 1 and its proof (§3), Corollary 4.1–4.2 (§4), and the extension
log for Estágios 9, 10, 11, 12, 13, 19, 22. Findings:

- **Definition 1** as quoted in ATTEMPT.md §0 matches THEOREM.md §1
  verbatim (`f(i)=U_i` if `ξ_i=1` else `π(i)`, `q=c/n∧1`).
- **Theorem 1** (`φ_∞(c)=∫_0^1 e^{-ct^2}dt`) and **Corollary 4.2**
  (`φ_∞(c)=(√π/2)c^{-1/2}-R(c)`, `0<R(c)<e^{-c}/(2c)`) match verbatim;
  both are used only as cited, black-box inputs in ATTEMPT.md (denominator
  of the ratio, and the final ratio step in Theorem 2's proof) — never
  re-derived or silently strengthened.
- **Estágio 9**'s all-orders closed form and **Estágio 12/22**'s rate
  `|Δ_n(c)|≤[a√c+κ_B]/n` (`a=1+√(π/2)` at Estágio 12, sharpened to
  `a*=0.367…` at Estágio 22, `κ_B=0.2805…` unchanged in both) are
  correctly listed in ATTEMPT.md's §0 table as **NOT used** anywhere in
  the proof — confirmed: neither appears in any downstream lemma/theorem
  of ATTEMPT.md, only in the introductory motivation for why a new route
  was needed.
- **Estágio 10**'s "post-adversarial correction" establishing
  `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n` **exactly** (not just approximately) is
  quoted correctly by ATTEMPT.md Remark 1.2's framing.
- **Estágio 13/19** `Q(n)=√(πn/2)-1/3+O(n^{-1/2})` (Robbins 1955 +
  FGKP95 `θ(n)→1/3`) is used **only** in the γ=1 case of the §7.3
  second-order remark, as disclosed — confirmed against THEOREM.md line
  3485 (`Q(n)=n!e^n/(2n^n)-θ(n)`, `θ(n)→1/3`, FGKP95 eq. 1.4).
- The γ-law's status ("caracterizada, não provada") is reaffirmed as
  still-open through Estágio 22, i.e. this is genuinely the first
  dedicated attack on it, as claimed.

## 3. Independent hand-derivation audit (no code)

**Lemma 1** (the exact double-sum formula) was re-derived from scratch by
hand from Definition 1, independently of ATTEMPT.md's own proof text,
before writing any code: the cyclic-point count decomposes as a sum over
*candidate* directed `k`-cycles `C` of `|C|·1{C⊆f}`; conditioning on
`ξ|_C` and using independence of `π`, `U`, `ξ` gives
`P(C⊆f)=Σ_m C(k,m)q^m(1-q)^{k-m}n^{-m}/(n)_{k-m}`; multiplying by the
count of `k`-cycles `(n)_k/k` and `|C|=k`, and using
`(n)_k/(n)_{k-m}=∏_{i=1}^m(n-k+i)`, reproduces Lemma 1 exactly. This
matches ATTEMPT.md's own proof step-for-step — **independently
confirmed correct**, not merely read and accepted.

**Core asymptotic mechanism** (why `√(2/(2−γ))` is the right constant):
verified by hand that, exactly (no approximation), with
`β=γ(2-γ)/2`, `G_n=(1/2)√(πn/β)`, `L_n=(√π/2)(γn)^{-1/2}`:

`(G_n/n)/L_n = √(γ/β) = √(2/(2-γ))`

— this is the one-line algebraic core of Theorem 2's proof (the Gaussian
integral of the truncated sum, divided by the leading order of `φ_∞`),
and it checks out exactly by hand computation, confirming the constant
`√(2/(2-γ))` is not a numerical coincidence but falls out of the ratio of
two explicit Gaussian-integral normalizations.

**Second-order constant at `γ=1`**: `C(1)` from the closed form
`C(γ)=-(2/(3√π))√γ(6-8γ+3γ²)/(2-γ)²` was hand/computer-checked to equal
`-2/(3√π)` exactly (Python one-liner, exact float match to 15 digits) —
matches the claimed reduction.

## 4. Independent numerics (fresh code, `av01`–`av05`, adversarial/)

**Discipline:** none of the front's `.py` scripts, nor the prior stalled
referee's `ref0*.py` scripts, were opened or imported. Every evaluator
below was typed from ATTEMPT.md's *prose statements* only. No randomness
used anywhere (deterministic recursion); seed block `20260869000+`
reserved-but-unused, confirmed via `grep -rn "20260869" 05_DISCOVERY_LAB/`
— only two ledger/queue reservation lines match
(`00_GOVERNANCE/DECISION_LEDGER.yaml`, `01_PORTFOLIO/TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`), no draws found anywhere.

### av01 — Lemma 1 vs. from-scratch brute force of Definition 1 (exact)

Brute-forced Definition 1 directly (enumerate rerouted subsets `S`,
injective π-images on the complement, all `U`-assignments on `S`,
exact functional-graph cycle detection), independent of Lemma 1's own
derivation, at `n=3,4,5`, using exact `Fraction` arithmetic, at `n+2`
rational `q`-points per `n` (enough to pin down the degree-`n` polynomial
in `q` exactly). **Result: exact match at every point, every `n`**,
including the `q=1` endpoint against an independently-computed
`Q(n):=Σ_{k=1}^n (n)_k/n^k` (`Q(3)/3=17/27`, `Q(4)/4=71/128`,
`Q(5)/5=1569/3125`, all matching both brute force and Lemma 1 exactly),
and the `q=0` sanity check (`φ(n,0)=1`). **0 mismatches.**

### av02 — Theorem 2 (the γ-scaling law) at scale, independent evaluator

Adaptive-truncation float64 evaluator of `Σ_k A_k(n,q)` (self-certifying
stop: 80 consecutive negligible terms, not the front's own `K` formula),
`γ∈{0.1,0.3,0.5,0.7,0.9,1.0}`, `n∈{2^8,...,2^18}` — same grid scale as
ATTEMPT.md §7.1. `φ_∞` cross-checked two ways (closed form vs.
`scipy.integrate.quad`, agreement to `<3e-16` relative). **Result:**
`R(n,γ)` converges monotonically to `target=√(2/(2-γ))` from below at
every γ, and at `n=262144` the computed `R` values agree with
ATTEMPT.md's own printed table to **every printed digit** (e.g.
`R(262144,0.5)=1.1540659874` both places; `R(262144,1.0)=1.4134793898`
both places) — a strong independent confirmation that is not merely
"consistent" but bit-for-bit reproducing. The diagnostic `√n·err`
converges to a stable γ-dependent constant (e.g. `→ -0.32489` at
`γ=0.5`), confirming the empirical `O(n^{-1/2})` decay claimed in
ATTEMPT.md §7.1 (my raw "ratio across doublings" print label was
imprecise — my `n`-grid quadruples, not doubles, each step, so the
observed ratio → 2.0 is the *correct* signature of `O(n^{-1/2})` decay
under quadrupling, not a discrepancy with the front's own quoted
`√2`-under-doubling figure).

### av03 — Theorem 1′ finite-`n` sandwich, literal re-typing of §5's formulas

`K, ω, δ, J_{3/2}, J_3, ρ, T, G_n, U, Lo` re-typed symbol-for-symbol from
ATTEMPT.md §5, checked against av02's independent `nφ(n,γn)` evaluator at
the same 30-point grid ATTEMPT.md reports (`γ∈{0.1,...,0.9,1.0}×
n∈{2^10,...,2^18}`). **Result: 30/30 sandwich holds**, including the one
point (`γ=0.1,n=1024`) where the side condition `K≤n/2` fails and `U`
becomes vacuously astronomical (`~3.2e18`) — exactly matching
ATTEMPT.md's own disclosure of that point.

### av04 — Lemma 2/3/4 pointwise inequality audit

Independent pointwise check of Lemma 2(a)/(b), Lemma 3, and Lemma 4
(upper/lower) at `(n,γ)∈{(65536,0.3),(65536,0.8),(4096,0.15),(4096,0.95)}`,
`k` up to ~10,000, ~154,000 total pointwise checks. **First pass found
888 apparent violations of Lemma 2(a)** — traced to a bug in *my own*
diagnostic script (comparing the raw product `P_{k,m}` against
`exp(-σ)` computed in ordinary float64, which silently underflows to
exactly `0.0` for `σ≳745` before the equally-tiny true product does,
manufacturing a spurious "violation" against a literal zero). Fixed by
recomputing the same check in log-space (robust to underflow) and
reran: **0/154,000 violations** across all five inequalities. This is
documented as *my own* transient bug, not a front defect — corrected
script (`av04_lemma234_pointwise.py`) and both logs are kept for the
record.

### av05 — Second-order conjecture + Corollary 2, independent numerics

*Part A*: two-point Richardson extrapolation of
`x_n=√n(R_n-\text{target})` at `n=2^16,2^17` against `C(γ)`'s closed
form, `γ∈{0.3,0.5,0.9,1.0}`. **Result:** relative deviation
`1.3e-7` to `1.0e-6` at all four γ — matching ATTEMPT.md's own claimed
`5.1e-7` worst-case precision, independently reproduced.

*Part B*: `γ_n=n^{-1/4}` (satisfies the Corollary 2 hypothesis
`γ_n n^{1/3}/\ln n → ∞`, since this equals `n^{1/12}/\ln n`), `n` up to
`2^18`. **Result:** `R(n,γ_n)` decreases monotonically toward 1
(`1.0404 → 1.0298 → 1.0216 → 1.0155 → 1.0110`) and tracks the *moving*
target `√(2/(2-γ_n))` closely and increasingly tightly at every step —
qualitatively consistent with Corollary 2. **Caveat honestly noted**:
`n^{1/12}` grows so slowly that the hypothesis statistic
`γ_n n^{1/3}/\ln n` only reaches `≈0.23` even at `n=2^18` (nowhere near
"large"), so this is a directional plausibility check, not a
deep-asymptotic confirmation — see §6, observation 1.

## 5. Logical/scope audit (attack list items 3–5)

- **Domain proved**: full mandate `γ∈(0,1]`, not a sub-interval; both
  stretch goals also proved, as claimed — confirmed by re-reading the
  proofs of Corollary 1 (uniformization via worst-constant substitution
  `β↦β_0` on `[γ_0,1]`, a standard and here correctly-executed technique)
  and Corollary 2 (the envelope terms of Theorem 2 are literally
  γ-dependent only through `β,a_γ`, so nothing breaks when `γ=γ_n`
  varies with `n`; the stated sufficient condition
  `γ_n n^{1/3}/\ln n→∞` was checked term-by-term against each envelope
  piece in the proof of Corollary 2 and is indeed sufficient for each).
- **γ=1 endpoint consistency**: checked — Theorem 2 at `γ=1` gives `√2`,
  matching the archive's existing `φ(n,n)=Q(n)/n` fact exactly (Corollary
  3), and my av01 brute force independently confirms
  `φ(n,n)=Q(n)/n` at `n=3,4,5` exactly.
- **No hidden upper/lower-bound-only gap**: Theorem 1′ is a genuine
  two-sided sandwich (confirmed numerically, av03), and Theorem 2's proof
  correctly derives a two-sided bound on the *ratio* from it plus
  Corollary 4.2's two-sided bound on `φ_∞`, not just one side.
  Corollary 2's explicitly-disclosed residual gap (the
  `n^ε≤c_n≤n^{2/3}/\log` window) is precisely and honestly named, not
  glossed as solved.
- **No non-closure claimed**, so item 5 of the attack list (verify
  obstruction precisely stated) does not apply to the main result; it
  does apply to the *disclosed* residual gap and to the second-order
  conjecture, both of which are precisely and honestly scoped (checked
  against the algebra of Corollary 2's proof and against the explicit
  "Status: CONJECTURED... not done rigorously" language of §7.3).

## 6. Observations (not defects)

1. **Corollary 2's numerical illustration engages the asymptotic regime
   weakly at practically reachable `n`.** Because the sufficient
   condition is `γ_n n^{1/3}/\ln n→∞` and `n^{1/12}` grows extremely
   slowly, any concrete schedule like `γ_n=n^{-1/4}` only reaches a
   hypothesis-statistic of `≈0.23` by `n=2^18`. The *proof* of Corollary
   2 is unaffected (I checked its logic term-by-term, §5); this is only
   a note that neither this report's nor (presumably) the front's own
   numerical illustration of the `γ_n→0` sub-case can be "deep" at
   realistic `n` — the mathematical content of the corollary rests on the
   proof, not the illustration, and the proof holds up.
2. My own first-pass av04 script had a float64-underflow bug (§4, av04)
   that manufactured 888 spurious "violations"; this was diagnosed,
   fixed, and rerun to 0/154,000 before being included in this report. It
   is disclosed here in the interest of transparency about the review
   process, not as a finding about the target document.

## 7. Seeds table

| Seed block | Status |
|---|---|
| `20260868000+` (front's reservation, per ATTEMPT.md §0) | reserved, front reports never drawn |
| `20260869000+` (referee reservation, per dispatch) | reserved, **not drawn** — no randomness used anywhere in this review (all checks are exact/deterministic: exact rational brute force, deterministic float64/adaptive-truncation recursion) |

`grep -rn "20260869" 05_DISCOVERY_LAB/` confirms only ledger/queue
reservation-record lines match (`00_GOVERNANCE/DECISION_LEDGER.yaml`,
`01_PORTFOLIO/TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`); no computation
anywhere in this review or in the archive draws from this block.

## 8. Files (all in `adversarial/`, this review)

| File | Content |
|---|---|
| `av01_lemma1_bruteforce.py` / `.log` | Exact `Fraction`-arithmetic brute force of Definition 1 vs. Lemma 1, `n=3,4,5`, all match; `q=0,1` sanity/endpoint checks |
| `av02_gamma_grid_independent.py` / `.log` / `.json` | Independent float64 evaluator of Theorem 2's ratio `R(n,γ)`, γ×n grid up to `n=2^18`; `φ_∞` cross-checked two ways |
| `av03_theorem1prime_sandwich.py` / `.log` / `.json` | Literal re-typing of Theorem 1′'s `Lo/U` envelope from ATTEMPT.md §5, checked against av02's `nφ` at the front's own 30-point grid: 30/30 |
| `av04_lemma234_pointwise.py` / `.log` | Pointwise audit of Lemma 2/3/4, ~154,000 checks, 0 violations (after fixing an underflow bug in my own first pass, disclosed) |
| `av05_secondorder_and_corollary2.py` / `.log` | Independent Richardson-extrapolation check of the second-order constant `C(γ)`; independent numerical illustration of Corollary 2's `γ_n→0` case |
| `REFEREE_REPORT.md` | this report |

Pre-existing files from a prior stalled referee attempt
(`ref01_lemma1_bruteforce.py/.log`, `ref02_gamma_grid.py/.log/.json`,
`ref03_theorem1prime.py`, `ref04_inequality_audits.py`,
`ref05_second_order.py`) were left untouched and were **not** opened,
read, or imported at any point in this review, including
`ref02_gamma_grid.json/.log` — every result in this report comes from
this review's own `av01`–`av05` scripts alone.

No git commits made by this review.
