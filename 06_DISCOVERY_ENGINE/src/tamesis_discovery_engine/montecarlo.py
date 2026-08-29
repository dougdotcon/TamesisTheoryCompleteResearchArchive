"""Monte Carlo Lab — Stage 2 module of the Tamesis Discovery Engine.

A standard library for the triangulation-only Monte Carlo checks
``05_DISCOVERY_LAB`` already runs alongside every exact result
(``CHECKLIST_07_MONTE_CARLO_LAB.md``, ``ROADMAP.md`` Stage 2 item 7). This
module has no dependency on any other Stage 1/2 module — it is pure
numerics, safe to import on its own.

"Triangulation-only" (the convention this module deliberately reuses,
spelled out in the checklist) means: Monte Carlo corroborates an
independently-derived exact/closed-form result, never stands alone as the
sole source of truth for a claim. :func:`triangulate` and
:func:`convergence_check` exist to make that discipline structurally easy —
a caller reaching for a single, unchecked point estimate has to go out of
their way to skip the comparison this module hands them for free.

Reproducibility discipline
----------------------------
Every entry point below takes an explicit ``seed`` and threads it into a
freshly constructed ``numpy.random.default_rng(seed)``, which is the only
source of randomness a caller-supplied ``fn`` ever sees — no function in
this module reads ``np.random``'s implicit global state. Two calls with the
same seed therefore always produce bit-identical results, which is the
entire point: an unseeded, silently-flaky Monte Carlo check is exactly what
"triangulation-only" is meant to rule out.

Agreement checks
------------------
:func:`triangulate` compares estimators pairwise with a z-style check —
``|estimate_i - estimate_j| <= tolerance * sqrt(stderr_i**2 + stderr_j**2)``
— rather than a naive point comparison, since two unbiased Monte Carlo
estimators of the same quantity are expected to differ by a little sampling
noise even when they agree; ``tolerance`` is the check's z-score threshold
(e.g. ``3.0`` for a 3-sigma-ish band), not an absolute or relative error
bound. ``agrees`` is ``True`` only if *every* pair agrees — triangulation
means all independent estimators corroborate each other, not merely most of
them.

When ``agrees`` is ``False``, ``diverging`` names the estimator(s)
responsible rather than every estimator that happened to sit in some
disagreeing pair: with 3+ estimators, one is flagged only if it disagrees
with a strict majority of the others, so two mutually-consistent estimators
against one outlier correctly names just the outlier. With exactly 2
estimators there is no third reference to break the tie, so both are
named — triangulation fundamentally cannot single out which of two is wrong
on its own; that is what a third, independent estimator is for.
:func:`convergence_check` instead tracks one estimator's error against a
known ``target`` as ``n`` grows, allowing a declared ``slack`` for
non-monotonic MC noise between adjacent sizes rather than demanding a
strictly decreasing curve.
"""

from __future__ import annotations

import dataclasses
import math
from typing import Callable, List, Sequence, Tuple

import numpy as np

__all__ = [
    "MonteCarloResult",
    "TriangulationResult",
    "ConvergenceResult",
    "run_estimator",
    "triangulate",
    "convergence_check",
]

Estimator = Callable[[np.random.Generator], float]


@dataclasses.dataclass(frozen=True)
class MonteCarloResult:
    estimate: float
    stderr: float
    n_trials: int
    seed: int


@dataclasses.dataclass(frozen=True)
class TriangulationResult:
    results: List[Tuple[str, MonteCarloResult]]
    agrees: bool
    tolerance: float
    max_z: float
    diverging: List[str]


@dataclasses.dataclass(frozen=True)
class ConvergenceResult:
    sample_sizes: List[int]
    errors: List[float]
    results: List[MonteCarloResult]
    target: float
    tolerance: float
    converged: bool


def run_estimator(fn: Estimator, n_trials: int, seed: int) -> MonteCarloResult:
    if n_trials < 2:
        raise ValueError(f"n_trials must be >= 2 to compute a standard error, got {n_trials}")

    rng = np.random.default_rng(seed)
    samples = np.fromiter((fn(rng) for _ in range(n_trials)), dtype=float, count=n_trials)

    estimate = float(np.mean(samples))
    stderr = float(np.std(samples, ddof=1) / math.sqrt(n_trials))
    return MonteCarloResult(estimate=estimate, stderr=stderr, n_trials=n_trials, seed=seed)


def triangulate(
    estimators: Sequence[Tuple[str, Estimator]],
    n_trials: int,
    seed: int,
    tolerance: float = 3.0,
) -> TriangulationResult:
    if len(estimators) < 2:
        raise ValueError(f"triangulate needs at least 2 independent estimators, got {len(estimators)}")

    results = [
        (name, run_estimator(fn, n_trials, seed + offset))
        for offset, (name, fn) in enumerate(estimators)
    ]
    n = len(results)

    max_z = 0.0
    disagree_count = [0] * n
    any_disagreement = False
    for i in range(n):
        _, result_i = results[i]
        for j in range(i + 1, n):
            _, result_j = results[j]
            combined_stderr = math.sqrt(result_i.stderr**2 + result_j.stderr**2)
            if combined_stderr == 0.0:
                z = 0.0 if result_i.estimate == result_j.estimate else math.inf
            else:
                z = abs(result_i.estimate - result_j.estimate) / combined_stderr
            max_z = max(max_z, z)
            if z > tolerance:
                any_disagreement = True
                disagree_count[i] += 1
                disagree_count[j] += 1

    agrees = not any_disagreement
    diverging_names: List[str] = []
    if any_disagreement:
        majority_threshold = (n - 1) / 2.0
        diverging_names = sorted(
            name
            for (name, _), count in zip(results, disagree_count)
            if count > majority_threshold
        )

    return TriangulationResult(
        results=results,
        agrees=agrees,
        tolerance=tolerance,
        max_z=max_z,
        diverging=diverging_names,
    )


def convergence_check(
    fn: Estimator,
    sample_sizes: Sequence[int],
    target: float,
    tolerance: float,
    seed: int,
    slack: float = 1.5,
) -> ConvergenceResult:
    if len(sample_sizes) < 2:
        raise ValueError(f"convergence_check needs at least 2 sample sizes, got {len(sample_sizes)}")
    if list(sample_sizes) != sorted(sample_sizes):
        raise ValueError(f"sample_sizes must be strictly increasing, got {list(sample_sizes)}")

    results = [run_estimator(fn, n, seed) for n in sample_sizes]
    errors = [abs(result.estimate - target) for result in results]

    non_increasing = all(
        errors[i + 1] <= errors[i] * slack for i in range(len(errors) - 1)
    )
    within_final_tolerance = errors[-1] <= tolerance
    converged = non_increasing and within_final_tolerance

    return ConvergenceResult(
        sample_sizes=list(sample_sizes),
        errors=errors,
        results=results,
        target=target,
        tolerance=tolerance,
        converged=converged,
    )
