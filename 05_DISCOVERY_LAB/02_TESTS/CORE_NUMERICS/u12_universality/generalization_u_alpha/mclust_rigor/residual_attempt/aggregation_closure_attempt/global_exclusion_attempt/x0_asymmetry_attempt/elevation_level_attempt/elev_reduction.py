#!/usr/bin/env python3
"""
elev_reduction.py -- T3 of DERIVATION_PREREG.md, the FORMULA-FREE test.

Claim (4.1): conditionally on x0 not in R, the M-CLUST(b) exploration at (c, n) is
the M-U exploration at (c' = c(1-rho), n' = (1-rho) n).  Because M-U = M-CLUST(1),
BOTH sides can be measured with the very same engine and the very same estimator,
so the comparison involves no master formula, no quadrature and no elevation at
all:

      phi(cyclic | x0 not in R)  for  M-CLUST(b, c,  n )
  ==  phi(cyclic | x0 not in R)  for  M-CLUST(1, c', n')            (n' = (1-rho) n)

Two conventions for n' are run side by side (they differ by c(1-rho) points, i.e.
by a relative c/n, and the derivation does not distinguish them at leading order):
    n'_A = round((1-rho) n)          -- match the size of the world R^c
    n'_B = round((1-rho)(n + c))     -- match the size of the pool U_rem
Seeds 20260823850-20260823873, all fresh.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

STRESS = [
    (65536, 100, 400.0),
    (65536, 300, 150.0),
    (65536, 100, 600.0),
    (65536, 400, 100.0),
    (65536, 200, 150.0),
    (65536,  50, 400.0),
]
REPS = 40000
SEED0 = 20260823850


def jobs():
    out = []
    k = 0
    for (n, b, c) in STRESS:
        rho = 1.0 - (1.0 - c / n) ** b
        out.append(("src", n, b, c, SEED0 + k, dict(src=(n, b, c))))
        k += 1
        nA = int(round((1.0 - rho) * n))
        out.append(("muA", nA, 1, c * (1.0 - rho), SEED0 + k, dict(src=(n, b, c))))
        k += 1
        nB = int(round((1.0 - rho) * (n + c)))
        out.append(("muB", nB, 1, c * (1.0 - rho), SEED0 + k, dict(src=(n, b, c))))
        k += 1
    return out


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
    J = jobs()
    procs = []
    t0 = time.time()
    for i, (kind, n, b, c, seed, meta) in enumerate(J):
        out = os.path.join(HERE, "parts", f"red_{i:02d}_{kind}.json")
        log = open(os.path.join(HERE, "parts", f"red_{i:02d}_{kind}.log"), "w")
        p = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "elev_mc.py"),
             "--n", str(n), "--b", str(b), "--c", str(c),
             "--reps", str(REPS), "--seed", str(seed), "--out", out],
            cwd=HERE, stdout=log, stderr=subprocess.STDOUT)
        procs.append((p, log))
        while sum(1 for q, _ in procs if q.poll() is None) >= 4:
            time.sleep(2.0)
    for p, log in procs:
        p.wait()
        log.close()
    rows = []
    for i, (kind, n, b, c, seed, meta) in enumerate(J):
        fn = os.path.join(HERE, "parts", f"red_{i:02d}_{kind}.json")
        if os.path.exists(fn):
            d = json.load(open(fn))
            d["kind"] = kind
            d["src"] = meta["src"]
            rows.append(d)
    json.dump(dict(seed0=SEED0, n_rep=REPS, rows=rows),
              open(os.path.join(HERE, "elev_reduction_results.json"), "w"), indent=1)
    print(f"done, {len(rows)}/{len(J)} jobs, {time.time()-t0:.0f}s")
