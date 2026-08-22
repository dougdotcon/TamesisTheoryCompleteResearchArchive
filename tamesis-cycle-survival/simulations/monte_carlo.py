#!/usr/bin/env python3
"""
monte_carlo.py -- Monte Carlo estimate of phi(n,c) at large n, compared
against the closed-form limit phi_inf(c) = int_0^1 e^{-c t^2} dt
(proofs/derivation.md, Theorem 1).

Model (Definition 1): pi a uniform permutation of [n]; independently, each
point i is rerouted with probability q=c/n to a uniform random target;
observable phi(n,c) = E[#cyclic points]/n.

Cyclic-point counting: a point i is on a cycle of the functional graph of f
iff i lies in the "eventual image" of f, i.e. the image of f composed with
itself M times for any M at least as large as the longest possible
transient length (<= n). We compute this via repeated squaring
(g <- g[g], doubling the effective number of applications each step) for
enough doublings that 2^doublings >= n, then count the number of distinct
values in g -- this equals the number of cyclic points. Fully vectorized
with numpy; O(n log n) per trial.

Fixed seed for reproducibility (--seed, default 20260822).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import erf

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def phi_inf_formula(c: float) -> float:
    if c == 0:
        return 1.0
    return 0.5 * math.sqrt(math.pi / c) * erf(math.sqrt(c))


def count_cyclic_points(f: np.ndarray) -> int:
    """Number of points on a directed cycle of the functional graph of f,
    via iterated squaring (see module docstring). f is a 1-D int array with
    f[i] in [0, n)."""
    n = f.shape[0]
    g = f.copy()
    doublings = max(1, int(np.ceil(np.log2(n)))) + 2  # generous margin past n
    for _ in range(doublings):
        g = g[g]
    return int(np.unique(g).shape[0])


def mc_trial(n: int, c: float, rng: np.random.Generator) -> float:
    q = c / n
    perm = rng.permutation(n)
    mask = rng.random(n) < q
    targets = rng.integers(0, n, size=n)
    f = np.where(mask, targets, perm)
    return count_cyclic_points(f) / n


def mc_estimate(n: int, c: float, trials: int, rng: np.random.Generator) -> tuple[float, float]:
    vals = np.fromiter((mc_trial(n, c, rng) for _ in range(trials)), dtype=float, count=trials)
    mean = float(vals.mean())
    sem = float(vals.std(ddof=1) / math.sqrt(trials))
    return mean, sem


def run(n: int, c_values: list[float], trials: int, seed: int) -> list[dict]:
    rng = np.random.default_rng(seed)
    rows = []
    print(f"\n=== Monte Carlo phi(n={n},c) vs. phi_inf(c), {trials} trials/cell, seed={seed} ===")
    print(f"{'c':>8} {'MC mean':>12} {'MC SEM':>10} {'phi_inf(c)':>12} {'z':>8} {'verdict':>8}")
    for c in c_values:
        mean, sem = mc_estimate(n, c, trials, rng)
        target = phi_inf_formula(c)
        z = (mean - target) / sem if sem > 0 else float("nan")
        verdict = "PASS" if abs(z) < 4.0 else "WARN"
        print(f"{c:>8.4f} {mean:>12.6f} {sem:>10.6f} {target:>12.6f} {z:>8.2f} {verdict:>8}")
        rows.append({"n": n, "c": c, "mc_mean": mean, "mc_sem": sem,
                      "phi_inf_c": target, "z": z, "trials": trials, "verdict": verdict})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=20000, help="finite-n model size")
    parser.add_argument("--trials", type=int, default=400, help="MC trials per c value")
    parser.add_argument("--seed", type=int, default=20260822, help="RNG seed")
    parser.add_argument("--c", type=float, nargs="*", default=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
                         help="list of c values to test")
    parser.add_argument("--no-json", action="store_true", help="skip writing data/monte_carlo_results.json")
    args = parser.parse_args()

    rows = run(args.n, args.c, args.trials, args.seed)

    n_fail = sum(1 for r in rows if r["verdict"] != "PASS")
    print(f"\n{len(rows) - n_fail}/{len(rows)} cells within |z|<4.")

    if not args.no_json:
        DATA_DIR.mkdir(exist_ok=True)
        out_path = DATA_DIR / "monte_carlo_results.json"
        with open(out_path, "w") as fh:
            json.dump({
                "description": "Monte Carlo estimates of phi(n,c) at large n, vs. the proved "
                                "closed form phi_inf(c) (proofs/derivation.md, Theorem 1). "
                                "z = (mc_mean - phi_inf_c) / mc_sem.",
                "n": args.n, "trials_per_cell": args.trials, "seed": args.seed,
                "rows": rows,
            }, fh, indent=2)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
