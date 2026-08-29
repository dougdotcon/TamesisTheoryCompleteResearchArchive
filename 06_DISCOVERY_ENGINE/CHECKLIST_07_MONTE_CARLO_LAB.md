# Checklist — Module 7: Monte Carlo Lab (Stage 2)

Source: `ROADMAP.md` §1 Stage 2, item 7. "A standard library for the
triangulation-only Monte Carlo checks this archive already runs
alongside every exact result."

File: `src/tamesis_discovery_engine/montecarlo.py`. Tests:
`tests/test_montecarlo.py`. `numpy`/`scipy` are already project
dependencies.

"Triangulation-only" (per `05_DISCOVERY_LAB`'s own convention, reused
here deliberately) means: Monte Carlo is used to corroborate an
independently-derived exact/closed-form result, never as the sole
source of truth for a claim on its own — this module should make that
discipline structurally easy to follow, not just possible.

## Design

- [ ] `MonteCarloResult` dataclass: `estimate: float`, `stderr: float`,
      `n_trials: int`, `seed: int`.
- [ ] `run_estimator(fn, n_trials, seed) -> MonteCarloResult`: runs `fn`
      (a callable taking a seeded `numpy.random.Generator` and returning
      one scalar sample) `n_trials` times, returns the sample
      mean/standard-error. Must use an injected/seeded RNG (`np.random.
      default_rng(seed)`), never an unseeded global RNG — reproducibility
      is the whole point.
- [ ] `triangulate(estimators: list[tuple[str, callable]], n_trials, seed,
      tolerance) -> TriangulationResult`: runs 2+ **independently
      implemented** estimators for the same quantity (e.g. two different
      sampling schemes) and checks their point estimates agree within
      `tolerance` (accounting for stderr — e.g. a z-style check, not a
      naive point comparison that would be flaky by construction).
      `TriangulationResult` reports each estimator's result and whether
      they triangulate (`agrees: bool`).
- [ ] `convergence_check(fn, sample_sizes: list[int], target, tolerance,
      seed) -> ConvergenceResult`: runs `run_estimator` at each size in
      `sample_sizes` (increasing), confirms the error against `target`
      is non-increasing (allowing minor MC noise via a declared slack)
      and the largest-`n` error is within `tolerance`. Reports the
      per-size errors, not just a boolean, so a caller can see the
      convergence curve.

## Tests (must all pass)

- [ ] `run_estimator` on a synthetic estimator with known ground truth
      (e.g. estimating `pi` via random points in the unit square) with a
      fixed seed is **exactly reproducible** across two separate calls
      with the same seed, and its estimate is within a few stderrs of
      the true value at a reasonably large `n_trials`.
- [ ] `triangulate` with two independently-coded estimators of the same
      known quantity (different sampling schemes, same target) reports
      `agrees=True`.
- [ ] `triangulate` with one estimator deliberately biased (e.g. samples
      from the wrong distribution) reports `agrees=False`, and the
      report identifies which estimator diverged.
- [ ] `convergence_check` on a consistent estimator with growing sample
      sizes shows decreasing error and reports `converged=True`; on a
      biased/inconsistent estimator (error does not shrink with `n`) it
      reports `converged=False`.

## Acceptance

- [ ] `pytest tests/test_montecarlo.py -v` passes with zero failures.
- [ ] No function in this module uses `np.random` without an explicit,
      caller-supplied seed — grep to confirm (this is the guard against
      silently-flaky tests downstream, in any module that later builds
      on this one).
