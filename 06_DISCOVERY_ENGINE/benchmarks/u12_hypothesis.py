"""Independent u12 permutation-with-reroutes benchmark for the Discovery Engine.

This is the required Stage 1 validation benchmark
(``CHECKLIST_00_INTEGRATION_AND_VALIDATION.md``, "The required benchmark").
Everything below is written directly from the bare combinatorial definitions
in `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/THEOREM.md`
(read, not imported — this file has no dependency on ``05_DISCOVERY_LAB`` at
all) and recomputes its own answers from scratch. THEOREM.md's stated closed
forms appear here only as labeled *targets*, at the bottom of this module,
never as part of any computation above them.

The ensemble (Definition 1, THEOREM.md section 1 — "`M_n(c)`"): fix `n` and
`c >= 0`. Let `pi` be a uniformly random permutation of `{0, ..., n-1}`.
Independently, for each `i`, let `xi_i` be i.i.d. Bernoulli with
`P(xi_i = 1) = min(c/n, 1)`, and let `U_i` be i.i.d. uniform on
`{0, ..., n-1}`. Define the random mapping `f(i) = U_i` if `xi_i = 1`, else
`f(i) = pi(i)`. A point `i` is *cyclic* iff iterating `f` from `i` returns to
`i` in finitely many steps (equivalently, `i` lies on a directed cycle of
`f`'s functional graph). The observable is
`phi(n, c) := E[#{cyclic points}] / n`.

Definition 4 (THEOREM.md section 7.2) conditions the same ensemble on
exactly `K` of the `n` indices being rerouted (rather than each
independently with probability `c/n`); write `phi_n^(K)` for the resulting
conditional mean cyclic fraction. By the exchangeability THEOREM.md itself
proves at Definition 4 ("conditioning on `K_n=K` leaves `pi` uniform and
makes the set of `K` rerouted indices a uniform random `K`-subset of `[n]`,
independent of `pi`; ... `phi_n^(K)` depends only on `(n,K)`, not on *which*
subset is realized"), the brute-force enumeration below is free to fix the
rerouted indices to `{0, ..., K-1}` rather than summing over all
`C(n,K)` subsets — this only reduces the enumeration's cost, it does not
change what is being computed, and it is a documented structural fact
about the ensemble, not a numeric result being smuggled in.

The `L(c)` limit object (Definition 3, THEOREM.md section 2.2) is not
reimplemented here directly (its explicit arc-head construction is the
proof machinery THEOREM.md itself uses to *derive* the closed forms below;
reimplementing it and then "checking" it against the same closed forms
would not be an independent check). Instead this module checks the two
things THEOREM.md actually claims about how the finite ensemble behaves
*as `n -> infinity`*: convergence of `phi(n,c)` to `phi_infinity(c)`
(mixed over `xi`, `pi`, and `U`, Monte Carlo), and, for fixed `K`,
convergence of the finite-`n` cyclic-*mass* distribution (conditioned on
exactly `K` reroutes) to the `K=1` continuum density THEOREM.md proves.
"""

from __future__ import annotations

import itertools
import math
from collections import deque
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Cyclic-point detection: shared by the brute-force and Monte Carlo paths.
# ---------------------------------------------------------------------------


def cyclic_mask(f: Sequence[int]) -> List[bool]:
    """Which indices of the functional graph `f : [n] -> [n]` lie on a cycle.

    A point is cyclic iff it is never "peeled off": repeatedly remove any
    point with in-degree zero (nothing maps to it any more, so it cannot be
    on a cycle) and decrement the in-degree of its image; whatever survives
    every round of peeling is exactly the union of `f`'s directed cycles.
    This is the standard `O(n)` algorithm for functional-graph cycle
    detection (Kahn's-algorithm-style topological peeling), independent of
    whether `f` happens to be a permutation.
    """

    n = len(f)
    indegree = [0] * n
    for target in f:
        indegree[target] += 1

    removed = [False] * n
    queue = deque(i for i in range(n) if indegree[i] == 0)
    while queue:
        i = queue.popleft()
        removed[i] = True
        j = f[i]
        indegree[j] -= 1
        if indegree[j] == 0 and not removed[j]:
            queue.append(j)

    return [not r for r in removed]


def cyclic_fraction(f: Sequence[int]) -> float:
    mask = cyclic_mask(f)
    return sum(mask) / len(mask)


def cyclic_mask_numpy(f: np.ndarray) -> np.ndarray:
    """Vectorized cyclic-point detection for Monte Carlo's tight inner loop.

    Same peeling algorithm as :func:`cyclic_mask`; kept separate (rather
    than making :func:`cyclic_mask` numpy-only) so the brute-force path
    above stays plain Python/`Fraction`-friendly and this path stays
    numpy-native for speed at the `n` in the thousands the Monte Carlo
    simulator runs at.
    """

    n = f.shape[0]
    indegree = np.bincount(f, minlength=n).astype(np.int64)
    removed = np.zeros(n, dtype=bool)
    queue = deque(np.flatnonzero(indegree == 0).tolist())
    while queue:
        i = queue.popleft()
        removed[i] = True
        j = int(f[i])
        indegree[j] -= 1
        if indegree[j] == 0 and not removed[j]:
            queue.append(j)
    return ~removed


def cyclic_mask_via_coloring(f: np.ndarray) -> np.ndarray:
    """A second, algorithmically different `O(n)` cyclic-point detector.

    Instead of peeling in-degree-zero points from the outside in
    (:func:`cyclic_mask_numpy`), this follows each point's forward orbit
    (path-following with three-coloring: unvisited/in-progress/done, as in
    classic functional-graph cycle detection), marking every point on the
    orbit's eventual cycle once that orbit closes back on itself or runs
    into an already-classified point. Every point is pushed onto exactly
    one path and colored exactly once, so this is also `O(n)` total, but it
    detects the *same* cycles by tracing forward from each point rather
    than peeling non-cycle points from every direction at once — used as
    the independent second algorithm for the Monte Carlo reproduction
    check in ``tests/test_u12_end_to_end.py``.
    """

    n = f.shape[0]
    UNVISITED, IN_PROGRESS, DONE = 0, 1, 2
    state = np.full(n, UNVISITED, dtype=np.int8)
    is_cyclic = np.zeros(n, dtype=bool)
    f_list = f.tolist()

    for start in range(n):
        if state[start] != UNVISITED:
            continue
        path = []
        position_in_path: Dict[int, int] = {}
        node = start
        while state[node] == UNVISITED:
            state[node] = IN_PROGRESS
            position_in_path[node] = len(path)
            path.append(node)
            node = f_list[node]
        if state[node] == IN_PROGRESS:
            for i in path[position_in_path[node] :]:
                is_cyclic[i] = True
        for i in path:
            state[i] = DONE

    return is_cyclic


# ---------------------------------------------------------------------------
# 1. Brute-force / exact enumeration (small n) — Definitions 1 and 4.
# ---------------------------------------------------------------------------


def brute_force_cyclic_count_distribution(n: int, K: int) -> Dict[int, Fraction]:
    """Exact distribution of `#{cyclic points}` under Definition 4's
    `M_n(c)` conditioned on exactly `K` reroutes, by enumerating every
    permutation of `{0,...,n-1}` and every choice of reroute target for
    each of the `K` rerouted indices (fixed, WLOG, to `{0,...,K-1}` — see
    module docstring).

    Returns an exact `Fraction`-valued probability mass function keyed by
    the (integer) number of cyclic points, so its own exact CDF, exact
    mean, or exact variance can all be recovered from it without any
    floating-point rounding — this is the "exact CDF of `M_n`" the
    checklist asks for, generalized to any `K` (`K=0` gives the trivial
    point mass at `n`; `K>=1` gives the richer distribution used to check
    Proposition 4's finite-`n` correction term below).
    """

    if not (0 <= K <= n):
        raise ValueError(f"K={K!r} must satisfy 0 <= K <= n={n!r}")

    rerouted = tuple(range(K))
    counts: Dict[int, int] = {}
    total_outcomes = 0

    for perm in itertools.permutations(range(n)):
        base = list(perm)
        for targets in itertools.product(range(n), repeat=K):
            f = list(base)
            for idx, i in zip(targets, rerouted):
                f[i] = idx
            n_cyclic = sum(cyclic_mask(f))
            counts[n_cyclic] = counts.get(n_cyclic, 0) + 1
            total_outcomes += 1

    return {value: Fraction(count, total_outcomes) for value, count in counts.items()}


def brute_force_phi_n_K(n: int, K: int) -> Fraction:
    """Exact `phi_n^(K)` (Definition 4): `E[#cyclic/n | exactly K reroutes]`."""

    distribution = brute_force_cyclic_count_distribution(n, K)
    mean_count = sum(value * prob for value, prob in distribution.items())
    return mean_count / n


def brute_force_cdf(distribution: Dict[int, Fraction], threshold_fraction: float, n: int) -> Fraction:
    """`P(#cyclic/n <= threshold_fraction)` from an exact count distribution."""

    return sum(
        prob for value, prob in distribution.items() if value / n <= threshold_fraction + 1e-12
    )


def brute_force_phi_n_K_second_algorithm(n: int, K: int) -> Fraction:
    """A second, differently-structured exact enumeration of `phi_n^(K)`.

    Used by ``tests/test_u12_end_to_end.py`` as the *independent* second
    implementation for the reproduction step: instead of building the full
    functional graph and peeling in-degrees (:func:`brute_force_phi_n_K`),
    this walks the permutation's cycle structure directly, splices the `K`
    reroutes into it one at a time, and counts survivors by explicit graph
    traversal from every point — a different algorithm over the same
    Definition 1/4 primitives, not a relabeled copy of the first.
    """

    if not (0 <= K <= n):
        raise ValueError(f"K={K!r} must satisfy 0 <= K <= n={n!r}")

    rerouted = set(range(K))
    total_cyclic = Fraction(0)
    total_outcomes = 0

    for perm in itertools.permutations(range(n)):
        for targets in itertools.product(range(n), repeat=K):
            f = {}
            for i in range(n):
                f[i] = perm[i]
            for offset, i in enumerate(sorted(rerouted)):
                f[i] = targets[offset]

            n_cyclic = 0
            for start in range(n):
                visited = []
                seen = set()
                current = start
                while current not in seen:
                    seen.add(current)
                    visited.append(current)
                    current = f[current]
                if current == start:
                    n_cyclic += 1

            total_cyclic += n_cyclic
            total_outcomes += 1

    return total_cyclic / (total_outcomes * n)


# ---------------------------------------------------------------------------
# 2. Monte Carlo simulator (large n) — Definitions 1 and 4.
# ---------------------------------------------------------------------------


def sample_f(n: int, c: float, rng: np.random.Generator) -> np.ndarray:
    """One draw of Definition 1's random mapping `f` on `{0,...,n-1}`."""

    perm = rng.permutation(n)
    p = min(c / n, 1.0)
    reroute = rng.random(n) < p
    targets = rng.integers(0, n, size=n)
    return np.where(reroute, targets, perm)


def sample_f_exact_K(n: int, K: int, rng: np.random.Generator) -> np.ndarray:
    """One draw of Definition 4's ensemble: `pi` uniform, exactly `K` of the
    `n` indices (a uniform random `K`-subset) rerouted to a uniform target.
    """

    if not (0 <= K <= n):
        raise ValueError(f"K={K!r} must satisfy 0 <= K <= n={n!r}")

    perm = rng.permutation(n)
    rerouted_indices = rng.choice(n, size=K, replace=False)
    targets = rng.integers(0, n, size=K)
    f = perm.copy()
    f[rerouted_indices] = targets
    return f


def monte_carlo_phi(
    n: int,
    c: float,
    trials: int,
    rng: np.random.Generator,
    cyclic_detector=cyclic_mask_numpy,
) -> Tuple[float, float]:
    """Monte Carlo estimate of `phi(n,c)` and its standard error over
    `trials` independent draws of Definition 1's ensemble.

    ``cyclic_detector`` defaults to the in-degree-peeling algorithm
    (:func:`cyclic_mask_numpy`) but accepts any function with the same
    `f -> boolean mask` signature — passing :func:`cyclic_mask_via_coloring`
    exercises a second, differently-structured cyclic-point algorithm over
    the exact same random draws (same ``rng`` state consumed in the same
    order), which is what ``tests/test_u12_end_to_end.py`` uses for its
    Monte-Carlo-side reproduction check.
    """

    fractions = np.empty(trials, dtype=np.float64)
    for t in range(trials):
        f = sample_f(n, c, rng)
        fractions[t] = cyclic_detector(f).mean()
    return float(fractions.mean()), float(fractions.std(ddof=1) / math.sqrt(trials))


def monte_carlo_cyclic_mass_samples(
    n: int,
    K: int,
    trials: int,
    rng: np.random.Generator,
    cyclic_detector=cyclic_mask_numpy,
) -> np.ndarray:
    """`trials` i.i.d. draws of the cyclic-mass fraction `#cyclic/n` under
    Definition 4's ensemble conditioned on exactly `K` reroutes — used to
    empirically check the finite-`n` distribution against the `M_K`
    continuum density THEOREM.md proves (`K=1`) as `n` grows.

    See :func:`monte_carlo_phi` for ``cyclic_detector``.
    """

    fractions = np.empty(trials, dtype=np.float64)
    for t in range(trials):
        f = sample_f_exact_K(n, K, rng)
        fractions[t] = cyclic_detector(f).mean()
    return fractions


# ---------------------------------------------------------------------------
# 3. Closed-form targets — hardcoded directly from THEOREM.md, used only as
#    comparison targets for the independently-computed values above.
# ---------------------------------------------------------------------------


def phi_infinity(c: float) -> float:
    """Theorem 1: `phi_infinity(c) = (1/2) sqrt(pi/c) erf(sqrt(c))`, the
    `n -> infinity` limit of `phi(n,c)` (value `1` at `c=0` by continuity).
    """

    if c <= 0:
        return 1.0
    return 0.5 * math.sqrt(math.pi / c) * math.erf(math.sqrt(c))


def phi_K_mean(K: int) -> float:
    """Lemma 2 (mean): `phi_K = 4^K (K!)^2 / (2K+1)!`, the `K`-reroute
    continuum mean cyclic fraction (`Wallis integral` closed form).
    """

    return (4.0**K) * (math.factorial(K) ** 2) / math.factorial(2 * K + 1)


def phi_n_1_closed_form(n: int) -> float:
    """Proposition 4: the exact finite-`n` correction term for `K=1`,
    `phi_n^(1) = 2/3 + 1/(3n^2)`.
    """

    return 2.0 / 3.0 + 1.0 / (3.0 * n * n)


def m1_density(x: float) -> float:
    """Lemma 2 (density, K=1), proved in THEOREM.md section 5.3:
    `f_{M_1}(x) = 2x` on `(0,1)`.
    """

    return 2.0 * x


def m1_cdf(x: float) -> float:
    """`F_{M_1}(x) = x^2` on `[0,1]`, the antiderivative of `f_{M_1}`."""

    return x * x


def gamma_scaling_target(gamma: float) -> float:
    """`phi(n, gamma*n) / phi_infinity(gamma*n) -> sqrt(2/(2-gamma))` as
    `n -> infinity` at fixed `gamma = c/n` (THEOREM.md, Estagio 10/23).
    """

    return math.sqrt(2.0 / (2.0 - gamma))
