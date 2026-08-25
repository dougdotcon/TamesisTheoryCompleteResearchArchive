# Conjecture 2, attempted directly — the moment method, Poissonization-in-`c`, and the obstruction common to both

> **Governance.** Wave 16, front (e) (`CONJECTURE-2-DIRECT-ATTEMPT`),
> authorized by `DISC-DEC-066` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Pre-registered
> in `DERIVATION_PREREG.md` before any script ran. Every claim below is
> labeled PROVED, CITED (a named classical fact used without
> re-derivation, at the same rigor level `THEOREM.md` itself uses),
> NUMERICALLY EXPLORED (exploratory data informing a stated open
> sub-problem — never offered as evidence toward a proof of Conjecture
> 2 itself), or OPEN. `THEOREM.md` (closed/finalized text) is **not**
> edited by this document, nor is any ledger or governance file. No git
> command was run. Seeds used: `20260858010`, `20260858011`,
> `20260858012` (this front's reserved block `20260858000+`, confirmed
> unused before first use). The referee range `20260859000+` was
> **not** used here. **This document requires mandatory independent
> adversarial verification before any integration into `THEOREM.md` or
> any ledger** — nothing here is asserted as fact anywhere else in the
> archive until that review completes. No `adversarial/` subdirectory
> was created by this front, and no referee was dispatched by it.

> **Executive summary (read first).** This front was dispatched
> explicitly expecting that "no genuine direct route exists" might be
> the only honest finding, with that outcome pre-declared fully
> acceptable. **That is close to, but not exactly, what happened.**
> No full direct proof of Conjecture 2 was found. But the attempt
> produced more than a bare non-closure:
>
> 1. A **precise architecture** for what a direct proof would look
>    like — the *moment method*: since `M(c)\in[0,1]` a.s., its law is
>    uniquely determined by its moment sequence (a classical, CITED
>    fact), and each moment `E[M(c)^p]` reduces, by the *same*
>    Fubini/exchangeability device Theorem 1 already uses for the mean
>    (`p=1`), to a `p`-point joint-cyclic-probability integral that
>    never fixes `K` — genuinely `K`-free in the same sense Theorem 1
>    is. If this could be carried out for every `p`, it **would** be a
>    full, direct, `K`-free proof.
> 2. For `p=2` (the second moment / variance), a **clean, new,
>    directly-checkable target**: `E[M(c)^2]=(1-e^{-c})/c` (PROVED here,
>    elementary calculus on the conjectured law — not previously stated
>    anywhere in `THEOREM.md`), plus a bonus exact fact
>    `E[M_K^2]=1/(K+1)` for every `K`.
> 3. A **fully elementary, PROVED reduction** of the `p=2` joint
>    probability to a same/different-background-block case split, with
>    every sub-fact independently cross-checked against exact
>    finite-`n` enumeration (`n=2,\dots,7`, zero deviations across three
>    separate classical-combinatorics facts).
> 4. A **PROVED, exact partial result** inside the hard case (the
>    "intact-block certificate": a rigorous lower bound on the joint
>    probability, verified with zero logical violations against direct
>    simulation).
> 5. A **precisely located obstruction**: the joint (`p\ge2`) computation
>    needs information about reroute *destinations* that Theorem 1's own
>    single-point machinery (Definition 3) is built to discard — this
>    document identifies exactly where that information is needed and
>    why the natural one-point apparatus does not supply it, and reports
>    honestly that reconstructing it from Definition 2's more primitive
>    picture is open, non-trivial new work, not executed here.
> 6. A **separate, fully rigorous negative finding**: the natural
>    "Poissonize in `c`" coupling does **not** make `\{M(c)\}_{c\ge0}` a
>    monotone or Markov process, refuting (via an exact, hand-verified
>    counterexample) the most natural route to a closed PDE for the
>    marginal law of `M(c)` in `c`.
> 7. A **unifying diagnosis**: both obstructions found (destination
>    information; non-Markovianity in `c`) trace back to the *same*
>    underlying fact — the full state needed is the entire reroute
>    configuration, not any low-dimensional summary — which is also,
>    from a different angle, exactly why Conjecture 1 needs its
>    case-by-case route. This is stated precisely in Section 6, not
>    asserted vaguely.
>
> **Net verdict: honest non-closure, with substantial, provable partial
> structural progress and a precise diagnosis of the obstruction** —
> not a full proof, and not a bare "nothing found" either. See Section
> 8 for the complete honest accounting and Section 9 for the scorecard.

---

## 0. Discipline / provenance

`DERIVATION_PREREG.md` (this directory) was written and saved before
any script ran; every file below postdates it:

```
2026-08-25T17:32Z  DERIVATION_PREREG.md
2026-08-25T17:32Z+ target_second_moment_symbolic.py/.log
2026-08-25T17:33Z+ same_cycle_exact_check.py/.log
2026-08-25T17:34Z+ two_point_exploration_mc.py (first draft)
2026-08-25T17:37Z+ two_point_exploration_mc_c1.log/.json
2026-08-25T17:40Z+ two_point_exploration_mc_c4.log/.json, correlation_ratio_analysis.py/.log
2026-08-25T17:41Z+ forward_offset_uniform_check.py/.log, different_block_joint_check.py/.log
2026-08-25T17:43Z+ intact_block_lower_bound_check.py/.log (and a docstring fix to
                    two_point_exploration_mc.py -- see the Honest process note, Section 3.5)
2026-08-25T17:44Z+ monotonicity_counterexample.py/.log
2026-08-25T17:5xZ  ATTEMPT.md (this file)
```

All arithmetic labeled PROVED is exact (`sympy` symbolic integration,
or exact-enumeration combinatorics via `itertools.permutations` with
integer/`Fraction` counts — no floating point in any PROVED step).
Floating point appears only in the NUMERICALLY EXPLORED Monte Carlo
sections (`two_point_exploration_mc.py`,
`intact_block_lower_bound_check.py`), clearly labeled as such.
`numpy.random.default_rng` seeds start at `20260858010` (this front's
reserved block), confirmed unused by `grep -rn "20260858"` across the
archive before first use — the only prior hits were the two
reservation lines in `DECISION_LEDGER.yaml` and `TEST_QUEUE.yaml`.

---

## 1. Setup: what "direct" means here, precisely

`THEOREM.md` §8, Conjecture 2:

`M(c) \overset{d}{=} \min(1,\sqrt{E/c})`, `E\sim\mathrm{Exp}(1)`, i.e.
`P(M(c)\le x)=1-e^{-cx^2}` for `x\in(0,1)` with an atom `e^{-c}` at
`x=1`, where `M(c) := \mathrm{Leb}(\text{cyclic set of }L(c))`
(Definition 3, `THEOREM.md` §2.2) and `M(c)` is, *by construction*, the
Poisson(`c`)-mixture of `M_K` (Conjecture 1's object) over
`K\sim\mathrm{Poisson}(c)` independent.

**Important clarification, stated up front so no step below is
misread.** `M(c)` is *defined* as this mixture — that is not something
a "direct" proof could or should try to avoid; it is what the symbol
means. What a case-by-case proof of Conjecture 2 would require is
proving Conjecture 1's *density formula* `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`
separately for every `K\ge2` and then summing — infeasible in
principle, since "every `K`" is not a finite list, however far the
current case-by-case front (`K=1,2,3` proved; `K=4` attempted this same
wave) manages to push. A **direct** proof is one that establishes the
*mixture's* law (or enough of it) by a computation that operates on the
full Poisson(`c`) mark process itself — exactly as Theorem 1 already
does for the *mean* `E[M(c)]=\varphi_\infty(c)` (`THEOREM.md` §3), via
a single-point exploration that never conditions on, or sums over,
`K` — rather than by first resolving the `K`-conditional law and then
mixing.

---

## 2. Why moments would suffice — the architecture, if it closed

**Fact (CITED, classical — the determinacy of the moment problem on a
compact interval).** If `X` is a real random variable with
`X\in[0,1]` a.s., then the law of `X` is uniquely determined by its
moment sequence `(E[X^p])_{p\ge0}`. (Standard: polynomials are dense in
`C[0,1]` by the Stone–Weierstrass theorem, so
`\int g\,d\mu_X = \int g\,d\mu_Y` for every continuous `g` — hence for
every Borel set by a standard approximation argument — whenever `X,Y`
have the same moments and both live on `[0,1]`; equivalently, the
Hausdorff moment problem on a compact interval is always determinate.
No convergence-of-moment-generating-function subtlety arises, unlike
the unbounded-support case, precisely because `[0,1]` is compact.)

`M(c)\in[0,1]` a.s. (it is a Lebesgue measure of a subset of `[0,1]`).
**So: if `E[M(c)^p]` could be computed, for every integer `p\ge1`,
directly from `L(c)`'s primitives (Definition 3) without ever fixing
`K`, and shown to match the moments of `\min(1,\sqrt{E/c})`, that would
constitute a complete, genuinely `K`-free, direct proof of Conjecture
2.** This is the precise target Route 1 (Section 3) pursues, and the
precise sense in which "the moment method" is not a vague slogan here
but a concrete, correct-if-completed strategy.

The mean case (`p=1`) is exactly Theorem 1's own proof: by Fubini
(§2.4 of `THEOREM.md`, already PROVED),

`E[M(c)] = E\Big[\int_0^1 1\{x\text{ cyclic}\}\,dx\Big] = \int_0^1 P(x\text{ cyclic})\,dx = P(x_0\text{ cyclic}) = \varphi_\infty(c)`,

using only a **single** query point's marginal probability (exchangeability
makes the integrand constant in `x`, collapsing the integral to one
evaluation). This single-point marginal is computed by Definition 3's
hazard-clock exploration directly on the full Poisson(`c`) mark
process — Theorem 1's Steps 3–5 (`THEOREM.md` §3) use the
marking/thinning theorem for Poisson processes precisely to avoid ever
conditioning on `K`. The `p\ge2` case is the natural generalization:

`E[M(c)^p] = E\Big[\int_{[0,1]^p} \prod_{i=1}^p 1\{x_i\text{ cyclic}\}\,dx_1\cdots dx_p\Big] = \int_{[0,1]^p} P(x_1,\dots,x_p\text{ all cyclic})\,dx_1\cdots dx_p`,

again by Fubini–Tonelli (identical justification to `THEOREM.md` §2.4:
the integrand is a non-negative, jointly measurable function of
`(x_1,\dots,x_p,\omega)`). The only new ingredient needed is the
**joint** `p`-point cyclic probability, in place of the marginal.

---

## 3. Route 1: the moment method, `p=2`

### 3.1 The target, computed exactly (PROVED)

Before attempting the hard direction, fix a precise, checkable target:
what does Conjecture 2 predict for `E[M(c)^2]`?

`target_second_moment_symbolic.py` computes this two independent ways
in exact symbolic arithmetic (`sympy`), both matching:

- **Route A**, directly from `M(c)=\min(1,\sqrt{E/c})`: since
  `M(c)^2=\min(1,E/c)`,
  `E[M(c)^2] = \int_0^c \frac ec e^{-e}de + \int_c^\infty e^{-e}de = \frac{e^c-1}{c}e^{-c} = \dfrac{1-e^{-c}}{c}`.
- **Route B**, via the `K`-mixture definition itself (Conjecture 1's
  density, `K\ge1` — `sympy` integrates `\int_0^1 x^2\cdot2Kx(1-x^2)^{K-1}dx`
  symbolically in `K` and finds the clean closed form
  **`E[M_K^2]=1/(K+1)`** for every `K\ge1`, a new exact fact not
  previously recorded in `THEOREM.md`), plus the `K=0` term
  (`M_0\equiv1`, so `E[M_0^2]=1`), Poisson-mixed over
  `K\sim\mathrm{Poisson}(c)`: `sympy` sums the series in closed form and
  gets the *same* `\dfrac{1-e^{-c}}{c}`.

Both routes agree exactly (`sympy.simplify` of the difference is `0`)
and match numerically at `c=0.5,1,2,5,10` to `10` decimal places (see
`target_second_moment_symbolic.log`). This is **not** new evidence for
Conjecture 2 (routes A and B are two ways of unpacking the *same*
conjectured object, so their agreement is a consistency check on the
arithmetic, not an independent confirmation) — it *is* a genuine new,
previously-unrecorded closed form (`E[M(c)^2]=(1-e^{-c})/c`, and the
per-`K` fact `E[M_K^2]=1/(K+1)`) that gives Route 1 a concrete, checkable
target.

### 3.2 The block-structure reduction (PROVED, elementary)

By exchangeability/rotation-invariance of the underlying PD(1) +
Poisson(`c`) construction (`THEOREM.md` §2.1, Definition 2 — the
circle `[0,1)` with its PD(1) block partition and independent
Poisson(`c`) marks is invariant in law under rotation, the same
structural fact Definition 3's own "unroll from `x_0`" device already
relies on), `E[M(c)^2] = \int_0^1\int_0^1 P(x_1,x_2\text{ both cyclic})\,dx_1dx_2`
splits cleanly on whether `x_1,x_2` land in the **same** background
PD(1) block (cycle) or **different** ones. Three elementary facts,
each derived here from Fact A (`THEOREM.md` §2.3, PROVED) plus the
residual/self-similarity property of `PD(1)` (the *same* mechanism
Definition 3 §2.2 itself uses to build `T_j=S_j+(1-S_j)(1-e^{-E_j})` —
not a new citation beyond what `THEOREM.md` already uses):

> **Lemma B1 (same/different split).** `P(x_1,x_2\text{ same block})=1/2`.
> *Proof.* By Fact A, `x_1`'s own block length `L\sim\mathrm{Unif}(0,1)`.
> Given `L=\ell`, an independent uniform `x_2` lands in that
> measure-`\ell` block with probability exactly `\ell` (elementary).
> So `P(\text{same}) = E[L] = \int_0^1\ell\,d\ell = 1/2`. `\square`

> **Lemma B2 (same-block case).** Given same block, the shared length
> `L` has density `f_L(\ell)=2\ell` on `(0,1)`, and given `L=\ell`, the
> forward arc-offset `\Delta` from `x_1` to `x_2` within the block is
> `\mathrm{Unif}(0,\ell)`.
> *Proof.* Unconditional sub-density: `P(L\in d\ell,\text{same})=1\cdot
> \ell\,d\ell` (density-`1` block length, times probability `\ell` that
> `x_2` lands inside); normalizing by `P(\text{same})=1/2` gives
> `f_{L\mid\text{same}}(\ell)=2\ell`. Given `x_2` lands in the block
> (measure `\ell`, with its own cyclic/rotational order per Definition
> 2), it is uniform within it by the same exchangeability that gives
> Fact A itself, so the forward offset is `\mathrm{Unif}(0,\ell)`. `\square`

> **Lemma B3 (different-block case).** Given different blocks, the
> joint sub-density of `(L_1,L_2)` is exactly `1` (constant) on the
> simplex `\{\ell_1,\ell_2>0,\ell_1+\ell_2<1\}` — equivalently, density
> `2` (uniform) once conditioned on "different."
> *Proof.* `P(L_1\in d\ell_1, x_2\notin\text{block}_1, L_2\in d\ell_2) =
> 1\cdot d\ell_1\cdot(1-\ell_1)\cdot\frac{1}{1-\ell_1}\,d\ell_2 = d\ell_1\,d\ell_2`,
> using the `PD(1)` residual/self-similarity fact (CITED, Kingman 1975;
> Arratia–Barbour–Tavaré 2003 — the same citation `THEOREM.md`
> Proposition 2.4 already uses): conditional on `x_2` missing block 1
> (probability `1-\ell_1`), `x_2` is a fresh size-biased pick from the
> *rescaled* remaining `PD(1)` partition, so `L_2/(1-\ell_1)\sim\mathrm
> {Unif}(0,1)`, i.e. `L_2\mid(\ell_1,\text{different})\sim(1-\ell_1)\cdot
> \mathrm{Unif}(0,1)`. `\square`

**Independent cross-check (discrete, exact, `n=2,\dots,7`).** All three
facts have an exact finite-`n` analogue for a uniform random
permutation, verified by brute-force enumeration over every
permutation (`itertools.permutations`, exact integer counts — see
`same_cycle_exact_check.py`, `forward_offset_uniform_check.py`,
`different_block_joint_check.py`):

- `P(1,2\text{ in the same cycle}) = 1/2` **exactly**, for every
  `n=2,\dots,7` (a classical fact, confirmed here from scratch).
- Given same cycle of length `\ell`, the forward `\pi`-distance from
  `1` to `2` is exactly uniform on `\{1,\dots,\ell-1\}`, for every
  `\ell` and every `n=3,\dots,7` (checked cell-by-cell: every count
  within a given `\ell` is identical).
- Given different cycles of lengths `(\ell_1,\ell_2)`, every lattice
  point `(\ell_1,\ell_2)` with `\ell_1,\ell_2\ge1,\ \ell_1+\ell_2\le n`
  carries exactly the same count, for every `n=3,\dots,7` (a single
  distinct count value across all valid pairs, checked exhaustively).

All three checks pass with zero deviations (see the three `.log`
files). This block-structure reduction is genuinely `K`-free (no `K`
appears anywhere in Lemmas B1–B3) and reusable for any `p`-point
extension of this method (for `p\ge3` query points the same-style
co-block reduction becomes the Bell-number case split already solved,
for a *different* purpose — reroute-source points, not query points —
in `conjecture1_k2_attempt/ATTEMPT.md` and
`conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md`; that
machinery is directly reusable here without re-derivation, a genuine
side benefit of this front's approach — see Section 6).

### 3.3 The obstruction: joint mark-exploration needs destination information Definition 3 discards

Lemmas B1–B3 reduce `E[M(c)^2]` to two conditional joint-cyclic
probabilities: `g_{\text{same}}(\ell) := P(x_1,x_2\text{ both cyclic}
\mid\text{same block},L=\ell)` and an analogous quantity for the
different-block case. Computing these requires extending Theorem 1's
hazard-clock exploration (Definition 3, `THEOREM.md` §2.2) from **one**
reference point to **two**, run jointly on the *same* realization of
the Poisson(`c`) marks.

This document attempted that extension directly and did **not**
complete it, for a reason that can be stated precisely rather than
vaguely: Definition 3's construction determines a single reference
point's fate using primitives `(\Theta_j,E_j)`, `i.i.d.` per mark,
*abstracted away from the mark's actual physical destination* — the
comparison `\Theta_j` vs `S_j`, and the closure-clock
`T_j=S_j+(1-S_j)(1-e^{-E_j})`, are a device that Proposition 2.4
(`THEOREM.md` §2.3, CITED) certifies reproduces the *correct marginal
law for one query point*, without needing to track where the mark's
destination *actually* lands relative to any second point. For **two**
simultaneous query points, the physical destination of a given mark
has consequences for **both** explorations that are correlated through
the *same* physical location — a fact the one-point abstraction has no
mechanism to preserve, because it was never asked to. Concretely: this
document could not derive, from Definition 3's stated primitives alone,
a rule for "running the algorithm from `x_2`'s vantage point using the
same `(\Theta_j,E_j)` draws already used for `x_1`" that is
demonstrably consistent with a single underlying physical construction
(as opposed to two independent, and therefore wrong, applications of
the one-point recipe). Reconstructing the joint law correctly appears
to require returning to Definition 2's more primitive picture (actual
Poisson(`c`) marks with actual `\mathrm{Unif}(0,1)` destinations on the
circle, and the PD(1) partition's actual cyclic order) and re-deriving
a genuinely two-reference-point exploration process from there — a
substantial, well-posed, but **not completed** piece of new
mathematics.

**This is stated as a located, honest gap, not a proof of
impossibility.** It is entirely possible a cleverer joint construction
exists; this document did not find one, and reports precisely what was
tried and where it stalled, rather than asserting a negative that was
not established.

### 3.4 A proved partial result inside the hard case: the intact-block certificate

One clean, fully rigorous partial result **was** extracted from the
same-block case, giving an exact, provable lower bound on `g_{\text{
same}}(\ell)` (finite-`n` form, Definition 1's model):

> **Lemma B4 (intact-block certificate, PROVED).** If none of the `\ell`
> points of the shared background `\pi`-cycle is independently selected
> for reroute (probability exactly `(1-c/n)^\ell` in the finite-`n`
> model `M_n(c)`, `\to e^{-c\ell/n}` as `n\to\infty` at fixed
> `\ell/n=t`), then **both** query points are cyclic.
> *Proof.* If no point of the shared cycle is rerouted, every point's
> `f`-image within the cycle equals its `\pi`-image, so the cycle is a
> literal, unbroken directed cycle of `f` — every point on it,
> including both query points, is cyclic by definition (its forward
> `f`-orbit returns to itself after exactly `\ell` steps). Points
> outside the cycle being rerouted onto it does not affect this: an
> external point redirected onto the cycle merely becomes a tributary
> feeding in, without altering any cycle member's own outgoing edge.
> `\square`

Since `t<1` a.s. (`t=T_0\sim\mathrm{Unif}(0,1)`), this lower bound
`e^{-ct}` is **strictly smaller** than Theorem 1's marginal
`e^{-ct^2}` (as `t<1\Rightarrow t>t^2`), i.e. it is a genuinely weaker
— but genuinely *proved* — statement than "the joint equals the
marginal." `intact_block_lower_bound_check.py` verifies the logical
implication directly against simulation: across `5{,}345` sample
paths in which the intact-block event held (`c=1,n=4000,\text{trials}=
20000`, seed `20260858012`), **zero** violations of "intact `\Rightarrow`
both cyclic" occurred, and in every one of 8 `\ell/n`-buckets the
empirical `P(\text{both cyclic})` was `\ge` the empirical
`P(\text{intact})`, exactly as the set-inclusion `\{\text{intact}\}
\subseteq\{\text{both cyclic}\}` requires (see the table in
`intact_block_lower_bound_check.log`). This is a small but genuine
piece of the same-block joint law obtained with full rigor.

### 3.5 Numerically explored: characterizing `g(\ell)` empirically

Because Section 3.3's obstruction blocks a full closed form, this
document instead **measured** `g_{\text{same}}(\ell)` directly from
the finite-`n` model (Definition 1: uniform permutation + independent
Bernoulli`(c/n)` reroutes for *every* point, mixing `K` automatically —
`two_point_exploration_mc.py`), to characterize the open sub-problem
with real data rather than leave it purely abstract. **This is
exploratory numerics informing an open sub-problem specific to this
document's own new construction (`g(\ell)`, which appears nowhere in
`THEOREM.md`) — it is not new evidence toward Conjecture 2 itself**,
whose own KS-test evidence at `c=1` already exists in `THEOREM.md` §8
and is not re-litigated here.

**Honest process note.** The script's first draft mislabeled the
candidate `\exp(-c\ell^2)` as a "fully-intact-block-only" guess in a
comment; that is wrong — `\exp(-c\ell^2)` is Theorem 1's own **marginal**
formula `P(x\text{ cyclic}\mid\text{own block length}=\ell)`, a
strictly *larger* quantity than the true intact-block probability
`e^{-c\ell}` derived independently in Lemma B4 (since `\ell<1
\Rightarrow \ell^2<\ell\Rightarrow e^{-c\ell^2}>e^{-c\ell}`). The
mislabel was caught by cross-checking Lemma B4's numbers against the
first Monte Carlo run's printed table (which briefly appeared to show
`g(\ell)` dipping *below* what was — mistakenly — believed to be a
rigorous lower bound, at the smallest `\ell` bucket; re-deriving the
true lower bound in Lemma B4 and re-checking within one self-consistent
run resolved the apparent contradiction cleanly). The docstring was
corrected in place (see `two_point_exploration_mc.py`'s current header);
no numeric output was affected, only a verbal mischaracterization of
what one already-correctly-computed quantity represented.

**Results** (`c=1`, `n=8000`, `40{,}000` trials, seed `20260858010`;
repeated at `c=4` with seed `20260858011` for robustness; full tables
in `two_point_exploration_mc_c{1,4}.log`). As a harness sanity check
(not new evidence — these are already-established quantities), the
marginal `P(\text{cyclic})` and `E[M(c)^2]` measured in the *same* runs
matched their known targets closely: at `c=1`,
`E[\text{fraction cyclic}]_{\text{MC}}=0.74635` vs
`\varphi_\infty(1)=0.74682`, and
`E[(\text{fraction cyclic})^2]_{\text{MC}}=0.63164` vs the Section 3.1
target `(1-e^{-1})/1=0.63212`; similarly at `c=4`
(`0.44128` vs `0.44104`, `0.24559` vs `0.24542`). These confirm the
simulation harness is correctly implemented — a prerequisite for
trusting the new `g(\ell)` measurements, not a new finding.

`g(\ell)` itself matches **neither** simple candidate at any `\ell`
tested:

| `\ell/n` (mid) | `g(\ell)` empirical (`c=1`) | `\exp(-c\ell^2)` | `\exp(-2c\ell^2)` |
|---|---|---|---|
| 0.19 | 0.854 | 0.965 | 0.932 |
| 0.44 | 0.691 | 0.826 | 0.682 |
| 0.69 | 0.605 | 0.623 | 0.389 |
| 0.94 | 0.551 | 0.415 | 0.172 |

`correlation_ratio_analysis.py` sharpens this into a normalized
correlation ratio `\rho(\ell) := (g-\overline m^2)/(\overline m-
\overline m^2)` (using the *empirical finite-n marginal* `\overline m`,
not the continuum `e^{-c\ell^2}`, to avoid exactly the finite-`n`
comparison pitfall the Honest process note above describes; `\rho=1`
means "always cyclic together," `\rho=0` means "conditionally
independent given `\ell`"). At both `c=1` and `c=4`, `\rho(\ell)` is
large (roughly `0.7`–`1.0`, noisy at the very smallest sampled bucket)
for small-to-mid `\ell` and **decreases** toward roughly `0.3`–`0.5` as
`\ell\to1` — a reproducible, qualitatively consistent pattern across
both `c` values (full tables in `correlation_ratio_analysis.log`). This
is directionally consistent with Lemma B4's mechanism (for small `\ell`
the dominant way either point is cyclic at all is via the intact-block
route, which automatically couples both points together; for larger
`\ell` there is more room for asymmetric partial-disruption outcomes
that leave exactly one of the two points cyclic), but this document
does **not** derive `\rho(\ell)` in closed form or prove the decreasing
pattern — it is reported as exploratory data characterizing exactly how
far from "trivial" (independent, or perfectly coupled) the true answer
is, informing what a completed Route 1 would need to reproduce.

### 3.6 Verdict on Route 1

**PROVED:** the moment-method architecture (Section 2); the `p=2`
target `E[M(c)^2]=(1-e^{-c})/c` and `E[M_K^2]=1/(K+1)`; the full
block-structure reduction (Lemmas B1–B3, with independent finite-`n`
cross-checks); the intact-block lower bound (Lemma B4, with a
zero-violation direct verification). **OPEN:** the joint
mark-exploration computation itself (Section 3.3) — the piece that
would be needed to turn the reduction into a closed form and check it
against Section 3.1's target. **NUMERICALLY EXPLORED**, not proved:
the qualitative shape of `g(\ell)` / `\rho(\ell)`.

---

## 4. Route 2: is `\{M(c)\}_{c\ge0}` Markov in `c`?

### 4.1 The Poissonization-in-`c` coupling

Realize **all** `c\ge0` simultaneously on one probability space: let
`\{(S_i,\Theta_i,T_i)\}_{i\ge1}` be a Poisson process of rate `1` on
`[0,1)\times[0,1)\times[0,\infty)` (positions, destinations, and
"birth times" `T_i`, the last coordinate itself a rate-`1` Poisson
process on `[0,\infty)` when marginalized), independent of the shared
`\mathrm{PD}(1)` cycle partition. For each `c\ge0`, the marks with
`T_i\le c` are, by the restriction/mapping theorem for Poisson
processes (CITED, Kingman 1993 — the same fact `THEOREM.md` §3 Step 3
already uses), exactly a rate-`c` Poisson process on `[0,1)` with i.i.d.
`\mathrm{Unif}(0,1)` destinations — i.e. Definition 3's own mark
process at parameter `c`. This realizes `\{L(c)\}_{c\ge0}` (hence
`\{M(c)\}_{c\ge0}`) jointly, on one space, with marks only ever *added*
as `c` increases ("`c` as time"). This is the natural candidate
coupling a reader familiar with Poissonization would reach for, and the
one this front was asked to consider explicitly (task brief, route
"embedding/coupling ... via the Markov/Lévy structure of a Poisson
process in `c`").

### 4.2 The counterexample (PROVED)

If `\{M(c)\}` were monotone non-increasing pathwise under this
coupling, or if it were Markov in `c` with a generator depending only
on the current value `M(c)`, a master (Kolmogorov forward) equation for
the marginal density of `M(c)` would be a natural next target. Both
fail, and this document proves it with an explicit, hand-verified,
zero-ambiguity finite example rather than an appeal to intuition
(`monotonicity_counterexample.py`):

Take `n=6`, background permutation `\pi=(1\,2\,3)(4\,5\,6)` (two
`3`-cycles; `K=0`: all `6` points cyclic, trivially). Add **one**
reroute, `1\to5`: the cyclic set becomes `\{4,5,6\}` (count `3` — the
old `\{1,2,3\}` cycle is destroyed: `2\to3\to1\to5\to6\to4\to5\to\cdots`
never returns to `1`, `2`, or `3`). Now add a **second**, independent
reroute on top of the first, `3\to2` — note `2` is `3`'s own
**ancestor** in the `K=1` configuration (`f(2)=3`), so this closes a
brand-new `2`-cycle `\{2,3\}` (`3\to2\to3`) out of what was, a moment
ago, non-cyclic territory. The cyclic set becomes `\{2,3,4,5,6\}`
(count `5`).

**`K=1\to K=2`, adding one more reroute: cyclic count goes `3\to5` — a
strict increase**, verified by direct, exact functional-graph
simulation (`monotonicity_counterexample.log`; the script asserts both
counts and halts loudly if either fails to reproduce). The mechanism
(a reroute of a non-cyclic point landing on one of *its own current
ancestors* closes a new cycle out of previously "dead" territory) is
general, not an artifact of this specific example — it is exactly the
"`U=c_d`" branch of `THEOREM.md` §7.3 Step 3's own case analysis,
applied here to a point *other than* the one that discrete argument was
originally about, on top of an *already-modified* (not virgin
permutation) background.

### 4.3 What this rules out, and what it does not

**PROVED:** under the natural Poissonization-in-`c` coupling of
Section 4.1, `\{M(c)\}_{c\ge0}` is **not** pathwise monotone
non-increasing. Consequently, `\{M(c)\}` cannot be Markov in `c` with a
generator depending on `M(c)` alone in any way that would make "does
`M` go up or down at the next mark" a deterministic-in-`M(c)` question
— the answer genuinely depends on finer structure (specifically, on
where the *currently non-cyclic* mass's forward trajectories point,
which points are whose ancestors right now) that the scalar `M(c)` does
not record. A master/generator equation closing on the marginal law of
`M(c)` alone, via a simple "add one mark, see how `M` changes" analysis,
therefore does not follow the route this section set out to check.

**What this does NOT show:** it does not show `\{M(c)\}` fails to be
Markov with respect to some *richer* state (the full reroute
configuration certainly *is* Markov in `c`, trivially — that state
just is not low-dimensional), nor does it rule out some entirely
different, cleverer route to a PDE for the marginal CDF that does not
go via a naive per-mark generator on `M(c)` itself. Neither alternative
was found; both remain open.

---

## 5. Route 3, flagged but not executed: an auxiliary-Poisson MGF idea

One further structural idea was identified as promising enough to
record, though it was not carried out: for `\lambda>0`, scatter an
independent auxiliary Poisson(`\lambda`) process `\mathcal P_\lambda` on
`[0,1)`. By the standard Poisson-restriction identity,
`E[e^{-\lambda M(c)}] = P(\text{no point of }\mathcal P_\lambda\text{
lands in the cyclic set}) = P(\text{every point of }\mathcal P_\lambda
\text{ is non-cyclic})`. This recasts the Laplace transform of `M(c)`
— which, if obtained in closed form and matched against
`\min(1,\sqrt{E/c})`'s own transform, would be a full direct proof, by
the same determinacy fact as Section 2 (Laplace transforms determine
laws on `[0,\infty)`, a fortiori on `[0,1]`) — as a *void probability*
of a second, independent Poisson process against the same cyclic-set
structure. Whether this void probability is any more tractable than
the `p`-point moments of Section 3 was not investigated; it plausibly
inherits exactly the same destination-information obstruction (Section
3.3), since "is a given point non-cyclic" is still the same single-point
predicate being asked jointly across many points. Recorded here as a
**named, well-posed, unattempted** direction for any follow-up front,
not as partial progress in itself.

---

## 6. Unifying diagnosis: one obstruction, two faces — and how it differs from Conjecture 1's

Sections 3 and 4 found two apparently different obstructions. They are,
on inspection, **the same underlying fact seen from two angles**:

- Route 1 needed, and could not obtain, the *joint* fate of two
  reference points — which requires knowing, for the shared mark
  process, not just "does each point individually survive" but the
  *correlated* physical routing of destinations between them.
- Route 2 found that the scalar `M(c)` is not Markov in `c` because
  the *next* mark's effect on `M` depends on the current fine structure
  (who is whose ancestor right now) — again, information beyond any
  single scalar or single-point marginal.

**Both are instances of one fact: the cyclic set of `L(c)` is
determined by the *entire* configuration of the reroute process, and no
proper summary of it smaller than "the whole configuration" — not the
pair `(x_1,x_2)`'s joint status, not the scalar `M(c)`, not the count
`K` alone — carries enough information to predict its own future
evolution or its own multi-point correlations.** This is genuinely
`K`-free in origin (it is not "the K-by-K case analysis is
combinatorially large"; it would appear even for the Poisson(`c`)
process directly, with `K` never mentioned) — but it is a **different**
kind of largeness than Conjecture 1's, worth stating precisely rather
than lumping together: Conjecture 1's obstruction (see
`conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md` §7) is that
the number of *destination-combinatorics shapes* needed to classify how
`K` reroute **sources** interact grows (at least) as fast as the number
of permutation-with-cycle-structure patterns on `K` labels, faster than
`K!`. This document's obstruction is different in kind: it is not that
a *count* grows with a parameter under this document's control (there
is no analogous "grows with `p`" explosion visible yet at `p=2`, since
`p=2` itself is not solved) — it is that the *necessary state* for the
`p`-point joint law is not capturable by reusing the *marginal*
apparatus (Definition 3) at all, for any fixed small `p`. Put plainly:
Conjecture 1's route is blocked by *combinatorial growth in a solvable
setup*; this document's routes are blocked by *not yet possessing a
correct joint setup*, `p=2` included. That the `p=2` case remains open
even in principle (not just "large") is the more fundamental of the two
obstructions, and is exactly why this document reports honest
non-closure rather than "closed for small `p`, open for large `p`."

---

## 7. Verification summary

| Check | Type | Result |
|---|---|---|
| `E[M(c)^2]=(1-e^{-c})/c`, two independent symbolic routes | PROVED (symbolic) | exact match, `sympy.simplify` diff `=0`; numeric agreement to 10 d.p. at 5 values of `c` |
| `E[M_K^2]=1/(K+1)` | PROVED (symbolic, new) | closed form via `sympy` integration in `K` |
| `P(x_1,x_2\text{ same block})=1/2` | PROVED (elementary) + exact discrete cross-check | discrete: `1/2` exactly for `n=2,\dots,7` |
| same-block: `L` density `2\ell`, offset `\mathrm{Unif}(0,\ell)` | PROVED (elementary) + exact discrete cross-check | discrete: exactly uniform counts, `n=3,\dots,7` |
| different-block: `(L_1,L_2)` uniform on simplex | PROVED (elementary) + exact discrete cross-check | discrete: single count value across all lattice pairs, `n=3,\dots,7` |
| intact-block certificate (Lemma B4) | PROVED (elementary) + zero-violation MC check | 0/5345 violations, `c=1,n=4000`, seed `20260858012` |
| non-monotonicity of cyclic count under added reroutes | PROVED (explicit example) | `n=6`: `K=1\to K=2` count `3\to5`, verified exactly |
| `g(\ell)` empirical shape vs two naive candidates | NUMERICALLY EXPLORED | matches neither; `\rho(\ell)` decreasing, `c=1,4`, reproducible |
| MC harness sanity (marginal mean, 2nd moment vs known targets) | NUMERICALLY EXPLORED (sanity only) | within statistical noise at `c=1,4` |

---

## 8. Scope, honesty, and what remains open

**What is PROVED here.** The moment-method architecture and its
correctness-if-completed (Section 2); a new exact closed form
`E[M(c)^2]=(1-e^{-c})/c` and `E[M_K^2]=1/(K+1)` (Section 3.1); a
complete, elementary, independently-cross-checked reduction of the
`p=2` joint probability to a same/different-block case split (Section
3.2, Lemmas B1–B3); an exact partial result inside the hard case
(Section 3.4, Lemma B4, the intact-block lower bound); and a rigorous
negative finding — via an explicit, hand-checked counterexample, not
an appeal to plausibility — that the natural Poissonization-in-`c`
coupling does not make `M(c)` monotone or simply Markov in `c`
(Section 4).

**What is NOT proved.** A full or even partial closed form for the
`p=2` joint cyclic probability `g(\ell)` beyond Lemma B4's lower bound;
consequently, `E[M(c)^2]` was **not** independently re-derived from
`L(c)`'s primitives by this document (only computed *from the
conjectured law itself*, Section 3.1 — a target, not a derivation of
that target). No moment `p\ge2` was actually computed from first
principles. The auxiliary-Poisson MGF idea (Section 5) was named but
not attempted at all. **No full or partial proof of Conjecture 2
itself is claimed anywhere in this document.**

**Why the obstruction is genuinely different from — not merely a
restatement of — Conjecture 1's `K`-by-`K` obstruction.** See Section 6
for the precise statement. In brief: this document's blocking point is
reached already at `p=2`, with no parameter analogous to Conjecture 1's
`K` yet shown to be the source of growth — the obstruction is "no
correct joint construction was found," not "the correct construction
exists but its case count explodes." This is arguably a *harder* kind
of open problem than Conjecture 1's (where the shape of the
combinatorics, if not its full resolution for every `K`, is at least
understood), and this document does not overstate its own progress
against it.

**What a follow-up front would need.** A genuine re-derivation of
Definition 2's exploration process (not Definition 3's already-
marginalized one) for two — and eventually `p` — simultaneous reference
points, tracking actual mark destinations rather than the abstracted
`(\Theta_j,E_j)\sim\mathrm{Unif}(0,1)\otimes\mathrm{Exp}(1)` proxies.
This is squarely the kind of "new closed-form whole-space computation"
`THEOREM.md` §5.4 already flags as the missing ingredient for
Conjecture 1 itself (§5.3's `K=1` method, generalized) — worth noting,
since it suggests the *same* new piece of mathematics (a genuinely
joint, non-marginalized exploration process for `L(c)`) might be the
key unlock for *both* Conjecture 1's general-`K` case and Conjecture
2's direct route, rather than these being two unrelated open problems.
This is offered as a lead, not a claim.

**No claim of progress on any Millennium Problem.** This document is
purely internal combinatorial/probabilistic mathematics on the
archive's own random-permutation-with-reroutes ensemble, exactly as
every other document in this lineage states.

---

## 9. Scorecard

| Item | Status |
|---|---|
| Full direct proof of Conjecture 2 | **NOT achieved** — honest non-closure |
| Moment-method architecture (Section 2) | PROVED (correct-if-completed statement) |
| `E[M(c)^2]=(1-e^{-c})/c`, `E[M_K^2]=1/(K+1)` | PROVED (symbolic, new closed forms) |
| Block-structure reduction, `p=2` (Lemmas B1–B3) | PROVED (elementary) + exact finite-`n` cross-checks, `n=2,\dots,7` |
| Intact-block certificate (Lemma B4) | PROVED (elementary) + zero-violation MC verification |
| Joint mark-exploration for `p=2` (the actual hard step) | **OPEN** — precisely located obstruction (Section 3.3), not resolved |
| `g(\ell)`, `\rho(\ell)` empirical characterization | NUMERICALLY EXPLORED (not proof), reproducible across `c=1,4` |
| Poissonization-in-`c` monotonicity/Markov property | **DISPROVED** (rigorous counterexample, Section 4.2) |
| Auxiliary-Poisson MGF route | named, **not attempted** (Section 5) |
| Unifying diagnosis of the obstruction, vs. Conjecture 1's | stated precisely (Section 6), not merely asserted |

**This document's net result: honest non-closure of Conjecture 2's
direct route, with real, provable partial structural progress — a new
exact target moment, a fully elementary and cross-checked reduction of
the hardest step's easy half, one proved exact lower bound inside the
hard half, a precisely located (not vaguely gestured-at) obstruction,
and a rigorous negative finding ruling out the most natural alternative
route (Poissonization-in-`c`).** Consistent with `DISC-DEC-066`(e)'s own
framing of this front as the highest-risk of the wave, with honest
non-closure declared acceptable in advance — this is exactly that
outcome, reported with everything that was actually established along
the way. Ready for the standing adversarial-referee requirement this
archive applies to every front before any integration into
`THEOREM.md`.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `two_point_exploration_mc.py` (c=1 run) | `20260858010` | reserved `20260858000+` |
| `two_point_exploration_mc.py` (c=4 run) | `20260858011` | reserved `20260858000+` |
| `intact_block_lower_bound_check.py` | `20260858012` | reserved `20260858000+` |

All other scripts (`target_second_moment_symbolic.py`,
`same_cycle_exact_check.py`, `forward_offset_uniform_check.py`,
`different_block_joint_check.py`, `monotonicity_counterexample.py`,
`correlation_ratio_analysis.py`) are exact/symbolic or deterministic
post-processing and use no random seed. No seed from the
referee-reserved range `20260859000+` was used by this front.

## Files table

| File | Role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any script ran |
| `target_second_moment_symbolic.py` / `.log` | Section 3.1: `E[M(c)^2]` and `E[M_K^2]` closed forms |
| `same_cycle_exact_check.py` / `.log` | Section 3.2, Lemma B1 discrete cross-check |
| `forward_offset_uniform_check.py` / `.log` | Section 3.2, Lemma B2 discrete cross-check |
| `different_block_joint_check.py` / `.log` | Section 3.2, Lemma B3 discrete cross-check |
| `intact_block_lower_bound_check.py` / `.log` | Section 3.4, Lemma B4 and its zero-violation verification |
| `two_point_exploration_mc.py` + `two_point_exploration_mc_c{1,4}.log` / `_results.json` | Section 3.5: `g(\ell)` empirical exploration, both `c` values |
| `correlation_ratio_analysis.py` / `.log` | Section 3.5: `\rho(\ell)` post-processing of the two MC runs |
| `monotonicity_counterexample.py` / `.log` | Section 4.2: the exact non-monotonicity counterexample |
| `ATTEMPT.md` | this document |
