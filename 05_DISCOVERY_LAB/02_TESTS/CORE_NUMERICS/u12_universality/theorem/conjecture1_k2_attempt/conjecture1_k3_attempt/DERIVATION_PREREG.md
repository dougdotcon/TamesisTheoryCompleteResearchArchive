# Pre-registration — `CONJECTURE-1-K3-ATTEMPT` (wave 15, front (b))

Written and saved **before any script runs**. Timestamp below is authoritative.

```
2026-08-24T18:22Z  DERIVATION_PREREG.md written (this file)
```

## Governance

Wave 15, front (b), authorized by `DISC-DEC-063` in
`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Seed budget reserved
for this front: `20260843000+` (referee reserved range `20260844000+` is
NOT to be used by this front). Confirmed unused before first use: `grep -rn
"20260843"` across `05_DISCOVERY_LAB` returns only the three reservation
lines (`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`,
`01_PORTFOLIO/TEST_QUEUE.yaml`) — no prior actual usage.

This document does **not** edit `THEOREM.md`, any ledger, or any file
outside this front's own working directory. No git command will be run.
This document requires mandatory independent adversarial verification
before any integration into `THEOREM.md` or the ledgers.

## Target

Extend `conjecture1_k2_attempt/ATTEMPT.md`'s whole-space method (which
proved `f_{M_2}(x) = 4x(1-x^2)`, `THEOREM.md` §8 Conjecture 1 at `K=2`,
modulo one classical citation) to `K=3`, aiming at:

`f_{M_3}(x) = 6x(1-x^2)^2` on `(0,1)` (the `K=3` instance of Conjecture 1).

## Method (planned, before any computation)

1. **Lemma 1 generalization.** Three reroute sources `x_1,x_2,x_3 ~
   Unif(0,1)` i.i.d. on an independent `PD(1)` partition. Define region
   masses `(m_1,m_2,m_3)` (Lebesgue measure of points whose
   background-forward flow reaches `x_1,x_2,x_3` first, respectively).
   Conjectured joint law: uniform on the simplex `Δ={m_1,m_2,m_3>0,
   m_1+m_2+m_3<1}`, density 6. Planned proof method: case-split by the
   set-partition of `{x_1,x_2,x_3}` into shared-background-block groups
   (5 patterns: all-same, one of 3 "exactly-two-same" patterns, all-different
   — the Bell number `B_3=5`), using the *same* `PD(1)` residual/size-biased
   citation as the `K=2` proof, applied recursively (once per sequential
   "peel" of a new source), plus a "uniform spacings with labeled gaps"
   fact for splitting a same-block arc among ≥2 co-located sources.
2. **Destination combinatorics.** With 3 destinations `u_1,u_2,u_3`, each
   landing in region 1/2/3/OUT, `4^3=64` raw combinations. Planned approach:
   model the redirect structure as a functional digraph `g:{1,2,3}→
   {1,2,3,OUT}` (`g(i)` = region `u_i` lands in, or OUT); classify by the
   induced cycle structure (self-loops, 2-cycles, 3-cycles, disjoint unions
   thereof, or none); derive that new cyclic mass depends *only* on the
   cycle-core structure and the position variables of redirects that lie
   *on* a cycle (off-cycle nodes contribute zero, generalizing the `K=2`
   "drains away" mechanism). Enumerate exhaustively by code (not by hand
   alone, given the explicitly flagged combinatorial-explosion risk),
   group configurations by identical mass-formula shape, sum probabilities
   per group.
3. **Assembly.** Attempt exact `sympy` marginalization of each group's
   density contribution to `f_{M_3}(x)`, sum, and compare symbolically to
   `6x(1-x^2)^2`.

## Pre-registered success/failure criteria

- **Full closure**: all groups' densities derived exactly and sum to
  `6x(1-x^2)^2` via `sympy.simplify(... ) == 0`, given Lemma 1.
- **Partial closure**: Lemma 1 generalization proved but destination
  combinatorics only partially closes (some groups' exact densities
  derived, others not) — report exactly which groups closed.
- **Non-closure**: if the group count or the required integrals become
  computationally intractable in the time available, STOP and report
  precisely where and why, per standing archive discipline. No
  reformulation of the target, no silent scope narrowing, no forced
  answer.

## Pre-registered numerical checks (run regardless of symbolic outcome)

- **R_MC1**: Monte Carlo check of the generalized Lemma 1 (three-region
  mass law), via an independent discrete finite-`n` permutation simulator
  (not reusing continuum/stick-breaking machinery), several scales.
- **R_MC2**: discrete finite-`n` permutation simulation of the *full*
  `M_3` model (build a real permutation, 3 reroutes, trace the true cyclic
  set by direct orbit-tracing), `n≥10000`, several thousand trials,
  Kolmogorov–Smirnov test of `M_3/n` against `6x(1-x^2)^2`.
- **R_MC3**: if the symbolic recipe (group-by-group) closes even
  partially, a Monte Carlo check of the derived recipe itself (draw
  `(m_1,m_2,m_3)`, draw group, draw `M_3`) for internal consistency.

All Monte Carlo checks use `numpy.random.SeedSequence` values starting at
`20260843000`, incrementing per script — logged in each script's own
output. All symbolic work uses `sympy.Rational`/exact symbolic arithmetic,
never floating point, for anything labeled PROVED.

## Labeling discipline

Every claim in the final `ATTEMPT.md` will be labeled PROVED, CITED,
NUMERICALLY SUPPORTED, or OPEN. If the destination-combinatorics step does
not fully close, the document will say so honestly and precisely, naming
the exact obstruction, per the standing instruction for this front.
