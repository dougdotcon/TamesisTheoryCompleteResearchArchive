# Pre-registration — `CONJECTURE-1-K4-ATTEMPT`

Written and saved **before any script runs**. Timestamp below is authoritative.

```
2026-08-25T17:14Z  DERIVATION_PREREG.md written (this file)
```

## Governance

This is a dispatched research front (orchestrating session's task), targeting
`THEOREM.md` §8 Conjecture 1 at `K=4`. Seed budget reserved for this front:
`20260850000+` (confirmed unused before first use — `grep -rn "20260850"`
across the archive returns only the three reservation lines in
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml` — see
`DISCOVERY_LAB_STATE.md`'s own text: "20260850000+ a 20260859000+ (uma faixa
de 1000 por frente + referee)"). This document does **not** edit
`THEOREM.md`, any ledger, `PROOF_DEPENDENCY_MAP.md`, `DISCOVERY_LAB_STATE.md`,
`TEST_QUEUE.yaml`, any README, or any sibling attempt's files. No git command
is run. No `adversarial/` subdirectory is created and no referee is
dispatched by this front — that is the orchestrating session's job, later.
This document requires mandatory independent adversarial verification before
any integration into `THEOREM.md` or the ledgers — nothing here is asserted
as fact anywhere else in the archive until that review completes.

## Target

Extend `conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md`'s
whole-space method (which proved `f_{M_3}(x)=6x(1-x^2)^2`, `K=3`) to `K=4`,
aiming at:

`f_{M_4}(x) = 8x(1-x^2)^3` on `(0,1)` (the `K=4` instance of Conjecture 1).

## Explicit acknowledgment of risk

The `K=3` document's own §7 states in so many words that whether the
"shape-collapse" mechanism (off-cycle nodes contribute zero new cyclic mass
regardless of target, collapsing `4^K`/`5^K`-raw-configuration explosion down
to a number of shapes growing only with cycle-structure counts on `K`
labels) continues to work at `K=4` and beyond is "a new, genuinely open
question this document raises but does not attempt to answer." This front
is the first attempt to answer that question. An honest non-closure — if
Lemma 1's generalization or the destination-combinatorics collapse becomes
intractable, or breaks down structurally — is a fully acceptable, valuable,
catalogable outcome. No forced closure, no silent narrowing of scope.

## Method (planned, before any computation)

1. **Lemma 1 generalization (Step A).** Four reroute sources
   `x_1,...,x_4 ~ Unif(0,1)` i.i.d. on an independent `PD(1)` partition.
   Region masses `(m_1,...,m_4)`, conjectured uniform (density `4!=24`) on
   the simplex `Δ_4={m_i>0, Σm_i<1}`. Planned proof: case-split by the
   set-partition of `{x_1,...,x_4}` into shared-background-block groups —
   `B_4=15` (Bell number) co-block patterns, grouped into 5 *shapes* by
   partition-integer-type (`4`; `3+1`; `2+2`; `2+1+1`; `1+1+1+1`), using
   the same `PD(1)` residual/size-biased citation as `K=2`/`K=3`, applied
   recursively (up to 3 sequential peels for the `1+1+1+1` pattern), plus
   the "labeled uniform circular spacings are Dirichlet" fact (already used
   at `n=2`, `K=2`'s Lemma 1; proved inline at `n=3`, `K=3`'s Lemma 1) now
   needed at `n=4` (the `AllSame` pattern) — planned to be proved inline the
   same way (direct integration over the `3!=6` cyclic orderings of the 3
   free co-located points relative to the anchor), or via a clean general
   argument from classical uniform-order-statistics spacings if that proves
   cleaner, with an explicit note of which route was actually used.
2. **Destination combinatorics (Step B).** With 4 destinations
   `u_1,...,u_4`, each landing in region `1,2,3,4` or `OUT`: `5^4=625` raw
   combinations. Planned approach: identical structural fact to `K=2`/`K=3`
   — model the redirect structure as a functional digraph
   `g:{1,2,3,4}→{1,2,3,4,OUT}`; a node contributes new cyclic mass iff it
   lies on a genuine cycle of `g`; every off-cycle node contributes exactly
   zero regardless of target (the proof of this fact is `K`-independent, so
   it is expected to carry over verbatim — this is not itself the risky
   step). Classify raw configs by cycle structure (which subset is on-cycle,
   and its internal cycle decomposition) via **exhaustive brute-force
   enumeration** (not by hand, given this exact risk was flagged). The
   number of *shape types* by cycle-partition-type is predicted (before any
   code runs) to be `Σ_{s=0}^{4} p(s) = p(0)+p(1)+p(2)+p(3)+p(4) =
   1+1+2+3+5 = 12` (generalizing the `K=3` finding of exactly `7 =
   p(0)+p(1)+p(2)+p(3)` shapes) — this specific numerical prediction is
   made *before* running the enumeration script, as a falsifiable check.
3. **Assembly (Step C/D).** Derive each shape's exact density contribution
   via `sympy` symbolic marginalization (never a Dirac delta), sum, compare
   symbolically to `8x(1-x^2)^3`.
4. **Reduction check.** Apply this front's own general method with 3 sources
   instead of 4 and confirm it reproduces the already-PROVED `K=3` result
   `6x(1-x^2)^2` group-by-group (generalizing `K=3`'s own R2 check against
   `K=2`).

## Pre-registered success/failure criteria

- **Full closure**: Lemma 1 generalizes, the destination-combinatorics
  collapse to a tractable, exhaustively-enumerated set of shapes, all
  shape densities derived exactly, and the sum equals `8x(1-x^2)^3` via
  `sympy.simplify(...) == 0`.
- **Partial closure**: e.g. Lemma 1 generalizes but the destination
  combinatorics do not collapse cleanly (or vice versa) — report exactly
  how far the derivation got and precisely what breaks, with no
  overclaiming.
- **Non-closure**: if the case count or required integrals become
  computationally or symbolically intractable in the time available, STOP
  and report precisely where and why. No reformulation of the target, no
  silent scope narrowing, no forced answer.

## Pre-registered numerical checks (run regardless of symbolic outcome)

- **R_MC1**: independent discrete-permutation Monte Carlo check of the
  generalized Lemma 1 (four-region mass law), several scales.
- **R_MC2**: discrete finite-`n` permutation simulation of the *full* `M_4`
  model (build a real permutation, 4 reroutes, trace the true cyclic set by
  direct orbit-tracing), `n≥10000`, several thousand trials, KS test of
  `M_4/n` against `8x(1-x^2)^3` (if the symbolic derivation closes) or
  against the raw simulated distribution (if not, still reported as a
  standalone numerical characterization).
- **R_MC3**: if the symbolic recipe closes even partially, a Monte Carlo
  check of the derived recipe itself for internal consistency.
- **Mechanism check**: discrete per-configuration exact-match check of the
  cycle-classification mechanism (generalizing the `K=3` referee-style
  260,000/52,000-trial check), at least two scales.

All Monte Carlo checks use `numpy.random.SeedSequence` values starting at
`20260850000`, incrementing per script — logged in each script's own output,
never reused across different checks. All symbolic work uses
`sympy.Rational`/exact symbolic arithmetic, never floating point, for
anything labeled PROVED.

## Labeling discipline

Every claim in the final `ATTEMPT.md` will be labeled PROVED, CITED,
NUMERICALLY SUPPORTED, or OPEN. If any step does not fully close, the
document will say so honestly and precisely, naming the exact obstruction.
Any bug caught during this work will be reported in the open (symptom,
diagnosis, fix), not silently patched, per this archive's standing
discipline.
