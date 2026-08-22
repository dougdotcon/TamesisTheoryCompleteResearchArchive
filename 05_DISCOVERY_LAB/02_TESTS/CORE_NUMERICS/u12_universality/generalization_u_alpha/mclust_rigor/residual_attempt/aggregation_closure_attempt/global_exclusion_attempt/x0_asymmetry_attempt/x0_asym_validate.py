"""x0_asymmetry_attempt -- stage 3: FRESH 18-cell validation.

Wave 9, DISC-DEC-041 front (a).

Independent Monte-Carlo driver, OWN implementation.  Imports only this
front's own `x0_asym_formula.py`; imports nothing from `residual_attempt/`,
`aggregation_closure_attempt/` or `global_exclusion_attempt/`.

Two deliberate independences from every predecessor validation in this line:

  * SEEDS: np.random.SeedSequence(20260822943) -- not 20260822018 (wave 4),
    918302033 / 720330339 (residual_attempt), 20260822901-904
    (aggregation_closure), 20260822910-911 (global_exclusion), nor
    20260822941 (this front's walk measurement).
  * ALGORITHM for the cyclic set: two independent implementations, both
    written here -- PEELING (repeatedly delete points of in-degree 0; what
    survives is exactly the set of points on cycles of f) and iterated
    squaring F <- F[F] with the image taken.  `_selftest()` checks both
    against brute-force orbit following on 200 random maps, and the
    production run cross-checks them against each other on every 200th
    instance (n_algo_crosschecks in the output), so a bug in either shows
    up rather than being inherited.  Squaring carries the bulk because it
    is vectorised; peeling is the independent auditor.

Grid: the same 18 cells the last three validations in this line used, so
the chi^2 numbers are directly comparable.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x0_asym_formula import rho_of, P_lead, P_exact, phi_asym, phi_CAND_own

SEED_ROOT = 20260822943


def build_f(n, b, c, rng):
    """M-CLUST(b) functional graph f (own implementation, re-read from
    DERIVATION_MCLUST_FIXED.md sec 1)."""
    pi = rng.permutation(n)
    inR = rng.random(n) < (c / n)
    front = np.flatnonzero(inR)
    for _ in range(b - 1):
        if front.size == 0:
            break
        front = pi[front]
        inR[front] = True
    f = pi.copy()
    idx = np.flatnonzero(inR)
    if idx.size:
        f[idx] = rng.integers(0, n, idx.size)
    return f


def cyclic_fraction_peel(f, n):
    """Fraction of points lying on a cycle of the functional graph f, by
    in-degree peeling.  A point is cyclic iff it is never removed."""
    indeg = np.bincount(f, minlength=n).astype(np.int64)
    stack = np.flatnonzero(indeg == 0).tolist()
    fl = f.tolist()
    il = indeg.tolist()
    removed = 0
    while stack:
        v = stack.pop()
        removed += 1
        u = fl[v]
        il[u] -= 1
        if il[u] == 0:
            stack.append(u)
    return (n - removed) / n


def cyclic_fraction_square(f, n):
    """Cross-check algorithm: image of f^(2^k) with 2^k >= n is exactly the
    cyclic set."""
    k = int(math.ceil(math.log2(n))) + 1
    F = f
    for _ in range(k):
        F = F[F]
    mask = np.zeros(n, dtype=bool)
    mask[F] = True
    return mask.sum() / n


def _selftest():
    rng = np.random.default_rng(12345)
    for _ in range(200):
        n = int(rng.integers(3, 60))
        f = rng.integers(0, n, n)
        # brute force: x cyclic iff x reappears in its own forward orbit
        cyc = 0
        for x in range(n):
            y = x
            for _ in range(n + 1):
                y = f[y]
            # y is now certainly on a cycle; x is cyclic iff its orbit returns
            z = f[x]
            hit = (z == x)
            for _ in range(n + 1):
                if z == x:
                    hit = True
                    break
                z = f[z]
            cyc += 1 if hit else 0
        a = cyclic_fraction_peel(f, n)
        b = cyclic_fraction_square(f, n)
        assert abs(a - cyc / n) < 1e-12, (n, a, cyc / n)
        assert abs(b - cyc / n) < 1e-12, (n, b, cyc / n)
    print("selftest OK: peeling == squaring == brute force on 200 random maps")


CELLS = ([(32768, 8, c, 4000) for c in (10.0, 40.0, 160.0)]
         + [(65536, 50, c, 5000) for c in (10.0, 50.0, 150.0, 400.0)]
         + [(65536, 100, c, 5000) for c in (10.0, 50.0, 150.0, 400.0)]
         + [(65536, 200, c, 5000) for c in (5.0, 20.0, 60.0, 150.0)]
         + [(65536, 300, 150.0, 5000), (65536, 100, 600.0, 5000),
            (65536, 400, 100.0, 5000)])


def main(candidates):
    """`candidates` maps a formula name -> callable(c, n, b) -> phi."""
    t0 = time.time()
    log = open(os.path.join(HERE, "x0_asym_validate.log"), "w")

    def say(m):
        print(m, flush=True)
        log.write(m + "\n")
        log.flush()

    say("# x0_asym_validate | started %s"
        % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    say("# own implementation, SeedSequence(%d); cyclic set by iterated squaring,"
        " cross-checked against an independent peeling implementation on every"
        " 200th instance" % SEED_ROOT)
    names = list(candidates)
    spawns = np.random.SeedSequence(SEED_ROOT).spawn(len(CELLS))
    out = {"seed_root": SEED_ROOT, "cells": []}
    chi2 = {k: 0.0 for k in names}
    for (n, b, c, n_rep), ss in zip(CELLS, spawns):
        rng = np.random.default_rng(ss)
        vals = np.empty(n_rep)
        n_xcheck = 0
        for i in range(n_rep):
            f = build_f(n, b, c, rng)
            vals[i] = cyclic_fraction_square(f, n)
            if i % 200 == 0:              # in-run cross-check of the two algorithms
                assert abs(vals[i] - cyclic_fraction_peel(f, n)) < 1e-12
                n_xcheck += 1
        m = float(vals.mean())
        sem = float(vals.std(ddof=1) / math.sqrt(n_rep))
        rho = rho_of(c, n, b)
        row = dict(n=n, b=b, c=c, n_rep=n_rep, rho=rho, bcn=b * c / n,
                   phi_mc=m, sem=sem, n_algo_crosschecks=n_xcheck)
        msg = ("n=%6d b=%3d c=%6.1f rho=%.4f | MC=%.6f+-%.6f |" % (n, b, c, rho, m, sem))
        for k in names:
            v = candidates[k](c, n, b)
            z = (m - v) / sem
            chi2[k] += z * z
            row["phi_" + k] = v
            row["z_" + k] = z
            row["dev_%s_pct" % k] = 100 * (m - v) / v
            msg += " %s dev=%+7.2f%% (z=%+6.2f) |" % (k, 100 * (m - v) / v, z)
        out["cells"].append(row)
        say(msg)
    say("")
    for k in names:
        say("# chi2 (%s, %d cells): %.2f" % (k, len(CELLS), chi2[k]))
    say("# wall %.1f s" % (time.time() - t0))
    out["chi2"] = chi2
    with open(os.path.join(HERE, "x0_asym_validate_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved x0_asym_validate_results.json")
    log.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        _selftest()
    else:
        import x0_asym_candidate as cand
        main(cand.CANDIDATES)
