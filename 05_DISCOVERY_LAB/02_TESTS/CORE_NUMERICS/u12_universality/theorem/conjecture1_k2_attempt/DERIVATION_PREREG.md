# Pre-registration — `CONJECTURE-1-K2-ATTEMPT`

> Governance. Wave 14, front (c), authorized by `DISC-DEC-057` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Written and saved
> **before** any script is run or any numeric/symbolic value is computed.
> Nothing outside this directory
> (`theorem/conjecture1_k2_attempt/`) will be created, modified, or
> deleted. `THEOREM.md` (closed/finalized text) is not edited by this
> front. No git command will be run. Seed budget reserved for this front:
> `20260835000+` (own checks), `20260836000+` (reserved for the future
> adversarial referee) — confirmed unused anywhere in the archive by
> `grep -rn` before writing this file (only appears in the
> `DECISION_LEDGER.yaml` allocation line itself).

## 1. Target claim

`THEOREM.md` §8, Conjecture 1, at `K=2`:

`f_{M_2}(x) = 4x(1-x^2)`, `x ∈ (0,1)`,

the density of `M_2 := Leb(cyclic set)` on `L(c)` (Definition 3, conditioned
on exactly `K=2` marks per §5.1) — proved only at `K=1` (§5.3: `f_{M_1}(x) =
2x`, "a genuinely new whole-space computation"). This document attempts to
generalize §5.3's method to `K=2`: fix the two rerouted points, split into
cases by how their images and cycle memberships interact, compute each
case's contribution to the density, sum.

## 2. Planned proof strategy (worked out by hand below; sympy will verify,
not originate, the algebra)

**2.1 The continuum whole-space `K=2` model**, matching DERIVATION.md §5's
`K=1` object exactly, generalized: two independent reroute points `x_1,x_2 ~
Unif(0,1)` i.i.d., each with an independent destination `u_1,u_2 ~
Unif(0,1)` i.i.d., superimposed on an independent `PD(1)`-partition
background. (Exchangeability of the finite discrete model, Definition 4,
justifies WLOG-fixing two labeled sources exactly as Prop. 4's proof does
for `K=1`; this is the continuum/`L(c)` redescription of that same model,
matching §5.3's own redescription for `K=1`.)

**2.2 Step A — background cycle-membership of the two sources (planned,
NOT yet numerically checked).** Let `B_1,B_2` be the background blocks
containing `x_1,x_2`. Two exhaustive cases:
- **Same block** (`x_1,x_2 ∈` the same cycle `C`, length `L`): by Fact A
  (`THEOREM.md` §2.3, already PROVED) `L~Unif(0,1)`; given `L=ℓ`, the
  forward arc-distance `A` from `x_1` to `x_2` is planned to be `Unif(0,ℓ)`
  (uniform position within the block, by the same "uniform point within a
  cyclic block of known length" fact used in §5.3's own Branch 2).
- **Different blocks**: by a residual/stick-breaking argument for `PD(1)`
  (planned citation: McCloskey 1965, Patil–Taillie 1977 — the *same*
  classical fact `THEOREM.md` Proposition 2.4 already cites for its own
  construction, not a new citation) — given `L_1=ℓ`, the *residual*
  partition (mass `1-ℓ`), rescaled by `1/(1-ℓ)`, is again `PD(1)`,
  independent of `ℓ`, so `L_2/(1-L_1) ~ Unif(0,1)` independent of `L_1`.

Writing `(m_1,m_2) := (L-A,A)` in the same-block case and `(m_1,m_2) :=
(L_1,L_2)` in the different-blocks case (i.e. `m_1` = the mass of the
region whose points, under background flow, reach `x_1` first; `m_2`
likewise for `x_2`), the plan is to show, by exact change-of-variables in
each case, that the joint law of `(m_1,m_2)` (marginalized over
same/different, each case weighted by its own probability) is **uniform**
on the triangle `T = {m_1,m_2>0,\ m_1+m_2<1}` — i.e. exact density `2` on
`T`. (Hand computation below suggests this; sympy will verify by exact
symbolic reduction, not merely evaluate. **This is the step at highest
risk of a hidden error** — flagged before any computation as the single
most likely place a mistake could hide, precisely because a symmetric,
constant answer is aesthetically tempting and worth extra scrutiny.)

**2.3 Step B — the reroute dynamics given `(m_1,m_2)` (planned 9-case →
4-group table, not yet symbolically checked).** Generalizing §5.3's
2-branch split: within the disturbed region, "region 1" (mass `m_1`) funnels
to `x_1`'s outgoing arrow (`u_1`), "region 2" (mass `m_2`) funnels to `x_2`'s
(`u_2`); everything outside (mass `1-m_1-m_2`) is untouched background,
always fully cyclic, and never gains or loses cyclic points regardless of
where `u_1,u_2` land in it (redirects into untouched background only ever
add an absorbed transient tail — this "general principle" is stated and
will be checked as a standalone lemma before use). Each `u_i` independently
lands in region 1 (prob `m_1`), region 2 (prob `m_2`), or "out" (prob
`1-m_1-m_2`), giving `3×3=9` combinations, planned to collapse into 4
mutually exclusive groups by the resulting cyclic-mass formula:
- **A** (`u_1`→region 1 *or* `u_2`→region 2, in the "both self-loop"
  sub-case): `M_2 = 1-D_1-D_2`, `D_1~Unif(0,m_1)`, `D_2~Unif(0,m_2)`
  independent; probability `2 m_1 m_2`.
- **B**: `M_2 = 1-m_2-D_1`, `D_1~Unif(0,m_1)`; probability `m_1(1-m_2)`.
- **C**: `M_2 = 1-m_1-D_2`, `D_2~Unif(0,m_2)`; probability `m_2(1-m_1)`.
- **D**: `M_2 = 1-m_1-m_2` deterministic; probability `1-m_1-m_2`.

**2.4 Step C — assembling the density.** `f_{M_2}(x) = \frac{d}{dx}
P(M_2\le x)`, computed by integrating the four groups' contributions over
`(m_1,m_2)\in T` with weight `2` (the Step-A density), each group's inner
distribution as in 2.3 — a mechanical (if tedious) `sympy` symbolic
integration, planned as the main computational step of this document.

**2.5 Step D — comparison.** Compare the resulting `f_{M_2}(x)` to
`4x(1-x^2)` symbolically (`sympy.simplify(f_computed - f_target) == 0`,
checked on the open interval, not just at sample points).

## 3. Refutation / acceptance criteria (fixed before any computation)

- **R1 (mean check, necessary).** `∫_0^1 x·f_{M_2}(x)dx` must equal `φ_2 =
  8/15` exactly (symbolic). Failure means an error exists somewhere in
  Step A–C and must be found before anything is reported as established.
- **R2 (K=1 degeneracy check).** Setting up the identical machinery with
  `K=1` (a single source, "region 1" mass `m_1=L\sim\mathrm{Unif}(0,1)`, no
  region 2) must reproduce `f_{M_1}(x)=2x` exactly — a direct sanity
  re-derivation of the already-PROVED §5.3 result via the same case-split
  language used here, checked symbolically.
- **R3 (Step-A uniformity check).** The claimed joint density `2` on `T`
  for `(m_1,m_2)` will be independently checked two ways: (i) direct
  symbolic change-of-variables from the `(L,A)` / `(L_1,L_2)`
  descriptions; (ii) a from-scratch Monte Carlo simulation of `(m_1,m_2)`
  under the two-case recipe (own draws, not reusing (i)'s formulas)
  compared to the uniform-triangle law by a 2D KS-type check (e.g. compare
  `E[m_1],E[m_2],E[m_1m_2],\mathrm{Cov}(m_1,m_2)` to their exact
  values under `\mathrm{Unif}(T)`, plus a 1D KS test on `m_1+m_2` against
  its exact target density `2(1-\ell)` — chosen because it is the
  quantity with a clean closed-form marginal, `\ell\in(0,1)`).
- **R4 (independent finite-`n` cross-check of the WHOLE recipe, not just
  Step A).** A separate, from-scratch Monte Carlo of the **discrete**
  finite-`n` model of Definition 4 at `K=2` (uniform permutation of `[n]`,
  two fixed rerouted indices, i.i.d. uniform targets, large `n`) will
  produce an empirical distribution of the cyclic-mass fraction; this is
  compared, via a KS test, against **both** `4x(1-x^2)` and the
  `f_{M_2}` this document derives (if the two differ). This is the
  strongest available independent check, since it does not reuse *any*
  of this document's continuum machinery (Step A or B) — it re-simulates
  the discrete ensemble directly, exactly as `k2_exact_exploration.py`
  did for the mean, but here for the *full distribution*, at larger `n`
  than that script used (which only tracked the mean, not the shape).
- **R5 (continuum Monte Carlo of the *derived* recipe).** A direct Monte
  Carlo simulation of the exact 2.2–2.3 recipe (draw `(m_1,m_2)`, draw
  group, draw `M_2`), large `N`, KS test against `4x(1-x^2)` — this
  checks that the recipe, *if Step A/B are correct*, is consistent with
  the conjecture; it is not, by itself, independent evidence that Step
  A/B are correct (R4 is the check for that).

If R1–R2 fail, the derivation has an error and will be debugged or
reported as broken (not silently patched to force agreement). If R1–R2
pass but R5's symbolic step (2.5) shows `f_{M_2}(x) \ne 4x(1-x^2)`
identically, while R3/R4 both support the *derived* recipe over the
conjectured density, this will be reported as a genuine candidate
refutation of Conjecture 1 at `K=2` — flagged prominently, not
downplayed, and specifically **not** asserted as a final refutation
without the standing adversarial-referee requirement this archive applies
to every positive finding.

## 4. What "success" (a proof) requires, concretely

- Every step in 2.2–2.4 re-derivable by hand from elementary facts (Fact
  A, the residual/stick-breaking property, elementary conditional
  probability) plus the explicit case enumeration — no unproved new
  machinery beyond what §5.3 and Proposition 2.4 already use.
- `sympy` used for exact symbolic integration/simplification throughout
  Step C onward; no floating point in anything labeled PROVED.
- Monte Carlo (R4, R5) used only as supporting/refuting numerical
  evidence, clearly labeled as such, with KS statistics reported.
- Honest labeling: PROVED steps stay PROVED; anything that does not close
  is reported precisely as open, with the exact missing/uncertain step
  named (per the task's explicit invitation to report partial progress,
  a necessary-condition check, a reduction, or an honest non-closure).

## 5. Randomness / seeds

Any Monte Carlo in R3–R5 draws seeds from `numpy.random.SeedSequence`
starting at `20260835000` (this front's reserved block, confirmed unused
above); every seed actually used will be tabulated in `ATTEMPT.md`.

## 6. Files this document commits to producing

- `derive_density_symbolic.py` / `.log` — Steps A–D (2.2–2.5), R1–R2.
- `mc_step_a_check.py` / `.log` — R3.
- `discrete_k2_full_distribution_mc.py` / `.log` — R4.
- `mc_recipe_check.py` / `.log` — R5.
- `ATTEMPT.md` — final write-up, structured like sibling attempts in this
  archive (executive summary, derivation, verification table, honest
  scorecard, precise statement of what remains open if anything does).

Timestamp of this pre-registration precedes every script/log file above
(checked in `ATTEMPT.md` §0 via `ls -la --time-style=full-iso`).
