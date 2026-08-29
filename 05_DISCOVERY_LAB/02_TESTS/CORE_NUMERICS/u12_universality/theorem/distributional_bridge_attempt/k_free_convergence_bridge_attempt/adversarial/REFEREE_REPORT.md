# Hostile adversarial referee report — `K-FREE-CONVERGENCE-BRIDGE-ATTEMPT`

**Target:** `.../distributional_bridge_attempt/k_free_convergence_bridge_attempt/ATTEMPT.md`
(wave 26, front (a), `DISC-DEC-123`). Pure combinatorial mathematics about
the u12 random-permutation-with-reroutes ensemble. **Not a Millennium
Prize Problem; no claim of that kind appears anywhere in the target or in
this report.**

**Referee protocol.** Read `THEOREM.md` §7 (fixed-`K` bridge machinery,
Open Lemma §7.4) and §8 (Lema R, Proposições D0–D4, `φ_K` formula) in
full; `distributional_bridge_attempt/ATTEMPT.md` (`K=0,1` closure) in
full; `general_k_decomposition_attempt/ATTEMPT.md` (Estágio 41, Proposição
S general-`K`, the Decomposition Theorem) in full; `DECISION_LEDGER.yaml`
`DISC-DEC-123` in full — **all before opening any of the target's own
`.py` scripts**. Theorem A and Claim B were then re-derived by hand from
the raw definitions, and independently re-implemented from scratch (no
target script imported, read, or copied) to cross-check every
quantitative claim. Only after this independent work were the target's
own scripts (`coupling_bound_check.py`, `verify_MK_moments.py`, etc.)
opened, to confirm they are genuine, non-fabricated implementations of
what the prose describes.

---

## Verdict: **SOUND WITH NAMED ISSUES**

Theorem A (the unconditional, `K`-free coupling bound) and every
supporting computation for Claim B (moments, the `W(r,t)` structural
reduction, the Lipschitz-constant lemma, the final `8K²` arithmetic) were
independently re-derived and re-implemented from scratch and found to be
**correct, with zero discrepancies**, against extensive fresh computation
(35/35 exact moment matches via a second independent implementation,
~235,000 fresh Monte Carlo trials with **zero** violations of Theorem A's
deterministic bound, exact full-pmf reproduction of literal Definition 4
by the underlying reduced-model machinery at four `(n,K)` cells including
`K=3`, and full symbolic/arithmetic reproduction of the `W(r,1)`,
`W(r,2)` closed forms and the `Λ_K ≤ 2√K`, `8K²` bounds). The document's
own conditional/unconditional labeling is scrupulously honest throughout
— the Main Theorem is never asserted unconditionally for `K≥2` anywhere,
including in the executive summary and scorecard. One genuine, but
low-severity and entirely non-load-bearing, mathematical error was found
(§7 item 3's abandoned side-remark on a Laplace-transform identity — see
Finding 1). No error was found in Theorem A, in Claim B's evidence, in
the Main Theorem's conditional statement, or in the document's governance
and disclosure discipline.

---

## Findings

### Finding 1 (LOW severity, non-load-bearing) — an incorrect distributional identity in an explicitly abandoned side-remark

Section 7, item 3, reads (ATTEMPT.md lines 638–644):

> "...using the identity, re-derived independently in this document's own
> reasoning ... that `1-M_K \overset{d}{=} \max(U_1,\ldots,U_K)`,
> equivalently `M_K\overset{d}{=}\sqrt{\min(U_1,\ldots,U_K)}`"

These two statements are **not equivalent**, and the first is **false**.
The correct pairing (verified below, both analytically and numerically)
is:

`M_K \overset{d}{=} \sqrt{\min(U_1,\ldots,U_K)}` — **correct**: since
`F_K(x)=1-(1-x^2)^K=P(\min(U_i)\le x^2)`.

`1-M_K^2 \overset{d}{=} \max(U_1,\ldots,U_K)` — the actually-equivalent
statement (via `1-\min(U_i) \overset d= \max(1-U_i) \overset d=
\max(U_i)`, using `U_i\overset d=1-U_i`), **not** `1-M_K \overset{d}{=}
\max(U_i)` as literally written.

Checked at `K=1` both analytically and by direct Monte Carlo simulation
of `THEOREM.md` §5.3's own exact `K=1` construction
(`n=400{,}000`, this report's own fresh code, not the target's):
`E[1-M_1]\approx0.3328` (matching the correct value `1/3`, since
`E[M_1]=2/3`), grossly inconsistent with `E[\max(U_1)]=E[U_1]=0.5`
(the false identity's implied value); `E[1-M_1^2]\approx0.4993`, matching
`E[\max(U_1)]=0.5` (the correct identity) to Monte Carlo noise.

**Why this does not affect the verdict.** This identity appears **only**
inside a route the document itself explicitly labels "attempted and
abandoned" (§7 item 3's own words) — a Laplace-transform approach to a
direct, non-case-by-case proof of Claim B that the document says did not
get past the algebraic setup stage. It is not used in Theorem A's proof,
not used in any of Claim B's actual evidence (§5.1–5.4), and not used in
the Main Theorem (§6). Fixing it (replace `1-M_K` with `1-M_K^2` in the
displayed identity) would not change any proved or evidenced claim
anywhere else in the document. Flagged here because a hostile referee
should name every verifiable error found, however small; this one is
real but cosmetic.

### Finding 2 (INFORMATIONAL, not a defect) — the final constant `8K²` is admittedly loose

Self-disclosed by the document itself (§7 item 5, "not examined... very
likely leaves room for a better constant"). Independently confirmed: the
exact bracket `\tfrac{3K^2-K}2+4K^{1.5}+2\sqrt K` (using the *exact*
`\Lambda_K`, not even the `2\sqrt K` relaxation) is already well below
`8K^2` for every `K` tested — e.g. at `K=100` the exact bracket is
`\approx16{,}681` against a stated bound of `80{,}000`, roughly a factor
of `4.8` slack (this report's `adv4_lipschitz_and_arithmetic.py`). This
is exactly what the document itself says (not a hidden issue), recorded
here only to confirm the self-assessment is accurate, not optimistic.

No other issues — mathematical, numerical, or disclosure-related — were
found.

---

## Independent re-derivation and re-verification, in detail

### 1. Theorem A (the coupling bound) — re-derived by hand from the raw definitions, before opening `coupling_bound_check.py`

Every step of §4.1–4.3 was reworked from scratch on the raw definitions
(Governing-Source Reindexing, i.i.d. categorical destinations,
landing-position-uniform, Proposição S, the Decomposition Theorem — all
cited, none re-derived, exactly as the target discloses) and found
correct:

- **Fact 1** (`P(\mathrm{NoColl}^c)\le K(K-1)/(2n)`, conditional
  uniformity given `\mathrm{NoColl}`): re-derived directly —
  `D_i=\lceil n\xi_i\rceil` is exactly `\mathrm{Unif}\{1,\ldots,n\}`, each
  pairwise collision probability is *exactly* `1/n` (not merely bounded
  by it), union bound over `\binom K2` pairs gives the stated bound
  exactly. Correct.
- **The "no accumulation over `t`" claim — the crux the mandate
  specifically flagged as worth scrutinizing.** Re-derived and confirmed
  correct: this is a direct consequence of a genuinely correct and
  standard fact, "sorting is `1`-Lipschitz in `\ell^\infty` under matched
  indices" (proved by the target via a level-set/order-statistic
  argument, itself re-verified independently here), applied to the *same*
  index set `\{\xi_i\}` vs `\{D_i/n\}` — **not** a sum of `t` per-gap
  errors. Since `|D_i/n-\xi_i|\le1/n` for every `i` individually
  (deterministic, from the ceiling), the sorting lemma gives
  `|D_{(t)}/n-\xi_{(t)}|\le1/n` for **every** `t=1,\ldots,K` directly,
  with no `t`-dependent accumulation. This is the correct reason the
  bound stays `K`-free-friendly rather than acquiring an extra factor of
  `K` or `t` from summing gap errors, and it holds up under independent
  scrutiny — a genuinely clean, correct application of a classical
  technique (the same "couple the same perturbation through a monotone
  rearrangement" idea underlying strong-approximation couplings of
  empirical processes).
- **The mismatch-zone argument.** Re-derived and confirmed correct: for
  fixed `j`, the set of `\eta_j` values that could cause
  `\mathrm{dest}(j)\ne\mathrm{dest}^\infty(j)` is contained in a union of
  `K` intervals (one per internal threshold `t=1,\ldots,K`), each of
  length *exactly* `|\mathrm{cumL}(t)/n-\mathrm{cumQ}(t)|\le1/n` (not
  `2/n` — this was checked carefully, since a factor-of-2 slip here would
  propagate) — giving `P(\text{mismatch}_j\mid\xi)\le K/n`
  **deterministically in `\xi`** (since `\eta_j\perp\xi`), hence
  unconditionally too, and a union bound over `j=0,\ldots,K-1` gives
  `K^2/n`. Correct.
- **Avoiding the `2^K` blow-up — re-checked for a hidden need to
  enumerate subsets.** The mandate specifically asked whether the
  argument "implicitly needs to consider all `2^K` subsets." It does not:
  `S=S^\infty` follows from `\mathrm{dest}=\mathrm{dest}^\infty` as
  *functions* on `\{0,\ldots,K-1\}` — a single pointwise equality, whose
  failure is itself bounded by a union over `K` sources (not `2^K`
  subsets) each contributing an `O(K/n)` per-source mismatch probability.
  No subset of `\{0,\ldots,K-1\}` is ever enumerated anywhere in the
  proof of Theorem A. This is a correct and genuinely `K`-free technique,
  not a disguised exponential-cost argument.
- **The pointwise bound on `G`.** Re-derived the algebra
  `V_t/n-V_t' = [\mathrm{cumL}(t+1)/n-\mathrm{cumQ}(t+1)]+\delta_1/n`,
  `\delta_1\in(0,1]`, giving `|V_t/n-V_t'|\le2/n`, and
  `|O/n-q_D|\le1/n`; summing over `|S|\le K` cyclic sources gives
  `|M_n^{(K)}-M_K'|\le(2K+1)/n` on `G`. Correct, matches exactly.
- **Assembling the CDF bound.** The two-sided
  `F_{M_K'}(x-\varepsilon)-\delta \le F_n^{(K)}(x) \le
  F_{M_K'}(x+\varepsilon)+\delta` argument, and its Lipschitz-constant
  corollary, were re-derived independently and match exactly.

**Numerical re-verification of Theorem A** (`adv6_theoremA_coupling.py`,
fresh implementation, own seeds `987001`–`987009` and `112233+`, **not**
the target's reserved range): 9 `(K,n)` configurations spanning
`K=2,\ldots,8`, `n=30,\ldots,400`, ~235,000 total trials. **Zero
violations** of the deterministic bound `|M_n^{(K)}-M_K'|\le(2K+1)/n` on
the good event `G`, in every single trial across every configuration.
Collision-rate and mismatch-rate Monte Carlo estimates track their
analytic bounds from below in every row (log:
`adv6_theoremA_coupling.log`). A separate mean cross-check
(construction's `M_n^{(K)}` conditional on `\mathrm{NoColl}` vs. exact
`E[T]/n` from a from-scratch brute force) confirms the construction is
not silently computing some other quantity.

**A deeper check of the underlying machinery than the mandate strictly
required, done because it is cheap and is the actual foundation Theorem A
stands on** (`adv5_reduced_model_pmf.py`): the reduced-model recipe
(uniform-`K`-subset dividers + i.i.d. categorical destinations +
landing-position-uniform + `T=O+\sum_{s\in S}V_s`) was checked, by exact
enumeration (not sampling), to reproduce the **entire exact pmf** of `T`
— not just its mean — against a from-scratch brute force of literal
Definition 4, at `(n,K)\in\{(4,1),(5,2),(6,2),(5,3)\}`. **Exact match,
every probability, every cell, including `K=3`.** This substantially
strengthens confidence in the whole Estágio 41 machinery Theorem A is
built from, beyond what the mandate's own "spot-check `E[T]/n`" ask
required.

### 2. Claim B — independently re-verified

**`K=1` (claimed PROVED).** Re-checked term for term against `THEOREM.md`
§5.3: `THEOREM.md`'s `u\notin C` branch (probability `1-L`, `M_1=1-L`)
matches `M_K'`'s `S=\emptyset` branch (probability `1-L`, `M_1'=1-L`)
exactly; `THEOREM.md`'s `u\in C` branch (probability `L`, `M_1=1-L+D`,
`D\mid L\sim\mathrm{Unif}(0,L)`) matches `M_K'`'s `S=\{0\}` branch
(probability `L`, `M_1'=(1-L)+V_0'`, `V_0'\mid L\sim\mathrm{Unif}(0,L)`)
exactly. This is a genuine proof by algebraic identity of the two
constructions, not merely numerical agreement — confirmed by direct
inspection and cross-checked numerically (`n=400{,}000`, fresh code,
mean `0.6666`, variance `0.0556`, matching `2/3` and `1/18` respectively
to Monte Carlo noise for both constructions independently).

**The 35 exact moment matches (`K=1,\ldots,7`, `t=1,\ldots,5`),
independently re-derived via a completely fresh second implementation**
(`adv2_moments.py`, not reading `verify_MK_moments.py` beforehand):
Route A — `sympy` symbolic integration of `x^t\cdot2Kx(1-x^2)^{K-1}` over
`[0,1]`; Route B — an independent re-implementation of the
Proposition-S-plus-Dirichlet-moment computation, built only from the
prose description in ATTEMPT.md (expand Proposition S into monomials,
multinomial-expand the conditional moment, apply the Dirichlet-moment
closed form). **All 35 cells match exactly** (exact `Fraction` equality,
not floating point), and every value matches the target's own reported
table verbatim (log: `adv2_moments.log`).

**Section 5.3's structural claims** (`adv3_W_pattern.py`, fresh
implementation from the prose only): the closed forms
`W(r,1)=2\,r!\,(r+1)^2` and `W(r,2)=r!\,(r+1)(r+2)(2r+3)` were
independently re-derived and checked for `r=0,\ldots,8` — **exact match
in every case**. The identity
`E[(M_K')^t]=K!\sum_{r=0}^K\binom Kr\,W(r,t)/(K+t+r+1)!` was
independently re-derived and checked against the independent `sympy`
target-density route for `K=1,\ldots,6`, `t=1,2,3` — **all match**. As an
extra check not explicitly claimed by the target, `W(r,t)`'s
independence from *which* size-`r` subset is chosen (not just its size)
was verified directly for four non-prefix subsets — confirmed.

**Extended KS-style evidence** (`adv7_MKprime_direct_sim.py`, fresh
simulation of `M_K'` directly from its §3 construction, not reusing
`MK_prime_KS_test.py`): mean and a 19-point empirical-vs-exact CDF
comparison at `K=3,7,15` all land within Monte Carlo noise of the exact
target, consistent with (and extending, on our own terms, to `K=15`) the
target's own KS-test table reaching `K=20`.

**The Lipschitz-constant lemma (§6)** (`adv4_lipschitz_and_arithmetic.py`):
the critical point `x^*=1/\sqrt{2K-1}` (including its correct handling
at the `K=1` boundary case, where the true maximizer is `x=1`, not an
interior stationary point — the formula degenerates correctly there,
`\Lambda_1=2`) was verified against direct symbolic differentiation and
against a `200{,}000`-point grid scan of `f_K` on `[0,1]` for
`K=1,2,3,5,10,20`, confirming `x^*` is the **global maximum**, not merely
*a* critical point. `\Lambda_K\le2\sqrt K` was checked for
`K=1,\ldots,100`. The final arithmetic
`\delta(K,n)+\Lambda_K\varepsilon(K,n)\le8K^2/n` was independently
recomputed (both with the exact `\Lambda_K` and with the `2\sqrt K`
relaxation) for `K=1,\ldots,1000` — holds in every case, with the slack
noted in Finding 2.

### 3. Self-caught issues (§8) — checked, accurately described

The three disclosed self-caught issues (an early `O(K^3/n)` mismatch
bound from erroneously accumulating per-gap errors instead of applying
the sorting lemma directly; a traced-through-by-hand, no-bug-found
correctness question about redundant cycle-graph traversal; and the
cross-checked exact-arithmetic pipeline) were read against the final
document and found to be accurately described, with no evidence any
downstream number was computed with a since-corrected buggy version.

---

## Scope, seed, and governance discipline — confirmed

- **Seeds.** Reserved range `20260933000`–`20260933999`
  (`DISC-DEC-123`, frente (a)) re-confirmed via
  `grep -rn "20260933" 05_DISCOVERY_LAB/`: the string appears **only** in
  `DECISION_LEDGER.yaml`'s reservation line and inside the target's own
  directory — no collision with any other front, before or after this
  referee's own work (this report's own scripts deliberately used
  disjoint seeds, `987001`–`987009` / `112233+` / `555001`–`555003`, none
  in the reserved range, to avoid any risk of confusion with the target's
  own randomness).
- **File scope.** `git status --porcelain` at the repository root shows
  **no modified (`M`) tracked files anywhere** — only new, untracked
  (`??`) directories, exactly the three wave-26 front directories
  authorized by `DISC-DEC-123` (including this front's own) plus one
  unrelated pre-existing untracked directory from a different lineage.
  `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `README.md`, and `index.html` are all
  untouched by this front, confirming the target's own §13 claim.
- **No `git` commands.** Consistent with the clean `git status` (no
  stray commits, no staged changes) — nothing in the repository state is
  inconsistent with the target's disclosure that no `git` command was
  run.
- **Honest conditional labeling.** Every occurrence of "unconditional" in
  the document was checked (`grep -n unconditional`) — each refers either
  to Theorem A itself (correctly unconditional, since it never invokes
  Claim B), to the trivial `K=0` case, or to an already-established
  result cited from elsewhere in the archive (Estágio 24's Conjecture 1
  general-`K`). **No occurrence anywhere claims an unconditional
  `F_n^{(K)}(x)\to F_K(x)` rate for `K\ge2`.** The executive summary, §6's
  Main Theorem statement, and every scorecard row referencing the Main
  Theorem are explicitly labeled "conditional on Claim B." This is a
  genuinely disciplined document given how strong Claim B's supporting
  evidence is (35/35 exact moment matches, KS tests to `K=20`) — exactly
  the overclaiming risk the mandate flagged, and it was avoided.
- **No target script was read before the corresponding independent
  re-derivation/re-implementation** — `coupling_bound_check.py` and
  `verify_MK_moments.py` were opened only after this report's own
  Theorem-A hand-derivation, fresh Monte Carlo (`adv6`), and fresh
  moment/`W(r,t)` computation (`adv2`, `adv3`) were already complete and
  logged; both target scripts were then confirmed to be genuine,
  non-fabricated implementations matching the prose (not hardcoded
  answers), independently corroborating rather than being the source of
  this report's conclusions.

---

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `adv1_bruteforce_def4.py` / `.log` | fresh brute force of literal Definition 4; confirms the mandate's specific `E[T]/n` spot-check values (`n=4,K=1`: `11/16`; `n=5,K=1`: `17/25`; `n=4,K=2`: `113/192`; plus 4 more cells) |
| `adv2_moments.py` / `.log` | fresh, independent re-derivation of all 35 exact moment matches for Claim B (two independent routes, no target code) |
| `adv3_W_pattern.py` / `.log` | fresh re-derivation of the `W(r,1)`, `W(r,2)` closed forms, the `K!`-sum identity, and a subset-symmetry check |
| `adv4_lipschitz_and_arithmetic.py` / `.log` | fresh verification of the `\Lambda_K` Lipschitz lemma (incl. grid-scan confirmation of global maximality) and the final `8K^2` arithmetic |
| `adv5_reduced_model_pmf.py` / `.log` | exact full-pmf (not just mean) cross-check of the reduced-model machinery against literal Definition 4, `K` up to `3` |
| `adv6_theoremA_coupling.py` / `.log` | fresh Monte Carlo re-implementation of Theorem A's full coupling construction; ~235,000 trials, zero violations |
| `adv7_MKprime_direct_sim.py` / `.log` | fresh direct simulation of `M_K'` vs. the exact target CDF, `K=3,7,15` |

---

## Summary for the orchestrating session

**Theorem A is correct and unconditional.** Independently re-derived by
hand from the raw cited facts and re-implemented from scratch with zero
discrepancies against ~235,000 fresh Monte Carlo trials (zero violations
of its deterministic per-trial bound) and an exact full-pmf check of its
underlying machinery. The specific techniques the mandate flagged for
scrutiny — the "no accumulation over `t`" claim and the avoidance of a
`2^K` blow-up — both check out as genuinely correct, not merely
plausible-sounding.

**Claim B's evidence is exactly as strong as claimed, and no stronger.**
All 35 exact moment matches, the `W(r,1)`/`W(r,2)` closed forms, and the
Lipschitz/arithmetic bound were independently reproduced with zero
discrepancies. The document never overclaims Claim B as proved for
`K\ge2`, and never lets the Main Theorem escape its "conditional on Claim
B" label.

**One real but cosmetic, non-load-bearing error was found and is named**
(Finding 1, an incorrect distributional identity inside an explicitly
abandoned exploratory paragraph) — hence **SOUND WITH NAMED ISSUES**
rather than an unqualified SOUND. Nothing else — no mathematical error,
no numerical discrepancy, no governance or disclosure lapse — was found
anywhere in the target document.
