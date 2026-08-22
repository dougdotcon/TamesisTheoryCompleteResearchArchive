#!/usr/bin/env python3
"""
finite_n.py -- exact (brute-force) enumeration for the cycle-survival model
at small n, cross-checked against the closed-form limit phi_inf(c) and the
conditional-K law phi_K.

Model (Definition 1 of proofs/derivation.md): pi a uniform permutation of
[n] = {0,...,n-1}; independently, each point i is "rerouted" with
probability q = c/n to a uniform random target in [n] (replacing f(i)=pi(i)
by f(i) = uniform); otherwise f(i) = pi(i). Observable:
    phi(n,c) = E[ #{i : i is on a cycle of f} ] / n.

Exact quantities computed here, both via brute force (no sampling):

  1. phi_n^{(K)}: phi(n,c) conditioned on EXACTLY K points being rerouted
     (Definition 4). By exchangeability this does not depend on which K
     points are rerouted, so we fix them to be {0,...,K-1} and brute-force
     over all n! permutations and all n^K reroute-target assignments.
     Cost: O(n! * n^K). Exact for K=0 (trivially phi_n^{(0)}=1) and proved
     in closed form for K=1 (phi_n^{(1)} = 2/3 + 1/(3n^2)); K=2 has no known
     closed form and is reported as raw exact-enumeration data.

  2. phi(n,c): the full observable, obtained by exactly mixing phi_n^{(K)}
     over K ~ Binomial(n, c/n) (this is an EXACT identity, not an
     approximation -- see proofs/derivation.md Fact 4.1). Only tractable
     for small n since it requires phi_n^{(K)} for every K = 0..n, and the
     brute-force cost of the K=n term is n!*n^n.

Nothing here is sampled; every number is an exact rational or exact-sum
floating point computation over an explicitly enumerated finite sample
space. Run as a script for a demonstration table; import the functions for
programmatic use.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.special import comb

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _num_cyclic(f: list[int]) -> int:
    """Exact count of points on a directed cycle of the functional graph
    of f (f: [n] -> [n], represented as a list of length n).

    Uses the standard O(n) three-color DFS for functional graphs: walk
    forward from each unvisited node, marking nodes IN_PROGRESS; if the
    walk revisits an IN_PROGRESS node, everything from that point back to
    the revisited node forms a cycle (mark those cyclic); if the walk hits
    an already-DONE node, the whole current path is non-cyclic (it feeds
    into structure resolved earlier).
    """
    n = len(f)
    UNVISITED, IN_PROGRESS, DONE = 0, 1, 2
    state = [UNVISITED] * n
    cyclic = [False] * n
    for start in range(n):
        if state[start] != UNVISITED:
            continue
        path = []
        node = start
        while state[node] == UNVISITED:
            state[node] = IN_PROGRESS
            path.append(node)
            node = f[node]
        if state[node] == IN_PROGRESS:
            # node is the entry point of a new cycle found within this path
            idx = path.index(node)
            for p in path[idx:]:
                cyclic[p] = True
        for p in path:
            state[p] = DONE
    return sum(cyclic)


def exact_phi_K(n: int, K: int) -> Fraction:
    """Exact phi_n^{(K)} as a Fraction: brute force over all n! permutations
    of [0..n-1] and all n^K reroute-target tuples for the fixed rerouted
    index set {0,...,K-1} (exchangeability, proved in proofs/derivation.md
    Definition 4, means the specific choice of index set does not matter).
    """
    if not (0 <= K <= n):
        raise ValueError(f"need 0 <= K <= n, got K={K}, n={n}")
    if K == 0:
        return Fraction(1, 1)  # f = pi exactly: every point of a bijection is cyclic

    total = 0
    count = 0
    rerouted = list(range(K))
    for perm in itertools.permutations(range(n)):
        f_base = list(perm)
        for targets in itertools.product(range(n), repeat=K):
            f = f_base.copy()
            for idx, t in zip(rerouted, targets):
                f[idx] = t
            total += _num_cyclic(f)
            count += 1
    return Fraction(total, count * n)


def exact_phi_K1_formula(n: int) -> Fraction:
    """Closed form phi_n^{(1)} = 2/3 + 1/(3 n^2), proved in
    proofs/derivation.md (Proposition 4). Returned as an exact Fraction for
    direct comparison against exact_phi_K(n, 1).
    """
    return Fraction(2, 3) + Fraction(1, 3 * n * n)


def exact_phi_full(n: int, c: float) -> float:
    """Exact (to float precision) phi(n,c), by mixing phi_n^{(K)} over
    K ~ Binomial(n, c/n), K = 0..n (Fact 4.1 -- an exact identity, not an
    approximation of any kind, given exact phi_n^{(K)} for every K).

    Cost is dominated by the K=n term: O(n! * n^n). Only usable for small n
    (n <= 5 is fast; n=6 takes tens of seconds; n>=7 is not recommended).
    """
    q = c / n
    if not (0 < q < 1):
        raise ValueError(f"need 0 < c/n < 1 (Definition 1's proviso n > c); got c/n={q}")
    total = 0.0
    for K in range(n + 1):
        weight = comb(n, K, exact=False) * (q ** K) * ((1 - q) ** (n - K))
        if weight < 1e-14 and K > c:
            # negligible tail weight past the mode; skip the (expensive) enumeration
            continue
        phiK = float(exact_phi_K(n, K))
        total += weight * phiK
    return total


def phi_inf_formula(c: float) -> float:
    """The proved closed form phi_inf(c) = int_0^1 e^{-c t^2} dt, via erf."""
    from scipy.special import erf

    if c == 0:
        return 1.0
    return 0.5 * math.sqrt(math.pi / c) * erf(math.sqrt(c))


def phi_K_formula(K: int) -> Fraction:
    """The proved Wallis-integral closed form phi_K = 4^K (K!)^2 / (2K+1)!."""
    return Fraction(4 ** K * math.factorial(K) ** 2, math.factorial(2 * K + 1))


def demo_K1_exact_matches_formula(max_n: int = 9) -> list[dict]:
    print(f"\n=== phi_n^(1): brute-force exact enumeration vs. closed form 2/3 + 1/(3n^2) ===")
    print(f"{'n':>3} {'exact (brute force)':>22} {'formula':>22} {'match?':>8}")
    rows = []
    for n in range(1, max_n + 1):
        bf = exact_phi_K(n, 1)
        formula = exact_phi_K1_formula(n)
        assert bf == formula, f"MISMATCH at n={n}: brute force {bf} != formula {formula}"
        print(f"{n:>3} {str(bf):>22} {str(formula):>22} {'OK':>8}")
        rows.append({"n": n, "exact": str(bf), "formula": str(formula), "value": float(bf)})
    print("All exact rational matches confirmed (Proposition 4).")
    return rows


def demo_K2_exact_vs_wallis_mean(max_n: int = 7) -> list[dict]:
    print(f"\n=== phi_n^(2): brute-force exact enumeration vs. Wallis-integral limit phi_2=8/15 ===")
    print("(No closed finite-n formula is proved for K=2 -- see proofs/derivation.md,")
    print(" 'Open Lemma'. This table shows convergence toward phi_2, not an identity.)")
    target = phi_K_formula(2)
    print(f"{'n':>3} {'exact phi_n^(2)':>22} {'decimal':>12} {'n^2*(phi_n^(2)-phi_2)':>24}")
    rows = []
    for n in range(2, max_n + 1):
        bf = exact_phi_K(n, 2)
        dev = float(bf) - float(target)
        print(f"{n:>3} {str(bf):>22} {float(bf):>12.6f} {n * n * dev:>24.4f}")
        rows.append({"n": n, "exact": str(bf), "value": float(bf), "rescaled_deviation": n * n * dev})
    print(f"(target phi_2 = {target} = {float(target):.6f})")
    return {"rows": rows, "target_phi_2": float(target)}


def demo_full_phi(max_n: int = 4, c_values: Iterable[float] = (0.5, 1.0, 2.0)) -> list[dict]:
    print(f"\n=== phi(n,c): full exact mixture (Fact 4.1) vs. limit phi_inf(c) ===")
    print(f"{'n':>3} {'c':>6} {'exact phi(n,c)':>16} {'phi_inf(c)':>14} {'|diff|':>10}")
    rows = []
    for c in c_values:
        for n in range(max(2, math.ceil(c) + 1), max_n + 1):
            exact = exact_phi_full(n, c)
            limit = phi_inf_formula(c)
            print(f"{n:>3} {c:>6.2f} {exact:>16.8f} {limit:>14.8f} {abs(exact - limit):>10.6f}")
            rows.append({"n": n, "c": c, "exact_phi_n_c": exact, "phi_inf_c": limit,
                         "abs_diff": abs(exact - limit)})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n-k1", type=int, default=9,
                         help="max n for the K=1 exact-vs-formula table (cost ~ n!*n; n=9 "
                              "takes a few seconds, n>=11 is impractically slow)")
    parser.add_argument("--max-n-k2", type=int, default=7,
                         help="max n for the K=2 exact-enumeration table (cost ~ n!*n^2; "
                              "n=7 is fast, n=8 takes ~30-60s, n>=9 is impractical)")
    parser.add_argument("--max-n-full", type=int, default=4,
                         help="max n for the full phi(n,c) exact mixture table (cost ~ n!*n^n "
                              "dominated by the K=n term; n=4 is instant, n=5 takes a few "
                              "seconds, n>=6 is impractical without further optimization)")
    parser.add_argument("--no-json", action="store_true", help="skip writing data/finite_n_results.json")
    args = parser.parse_args()

    k1_rows = demo_K1_exact_matches_formula(args.max_n_k1)
    k2_result = demo_K2_exact_vs_wallis_mean(args.max_n_k2)
    full_rows = demo_full_phi(args.max_n_full)

    if not args.no_json:
        DATA_DIR.mkdir(exist_ok=True)
        out_path = DATA_DIR / "finite_n_results.json"
        with open(out_path, "w") as fh:
            json.dump({
                "description": "Exact (brute-force, no sampling) small-n enumeration results "
                                "for the cycle-survival model, cross-checked against the proved "
                                "closed forms in proofs/derivation.md.",
                "phi_n_K1_vs_formula": k1_rows,
                "phi_n_K2_vs_wallis_limit": k2_result,
                "phi_n_c_full_mixture_vs_phi_inf": full_rows,
            }, fh, indent=2)
        print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
