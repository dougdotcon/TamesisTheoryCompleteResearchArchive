#!/usr/bin/env python3
"""
elev_validate.py -- T4: fresh-seed validation of phi_RED against phi_EPSR (the
formula of record) and phi_CAND, on

  (i)  the lineage's standard 18-cell grid  (direct comparison with 6 recorded grids)
  (ii) SIX cells deliberately beyond ANYTHING tested in this lineage
       (rho up to 0.84 against a previous maximum of 0.60; b*c/n up to 1.83
        against a previous maximum of 0.92; plus two cells at n = 131072).

All seeds fresh (20260823820-843).  Own MC engine (`elev_mc.py`).
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

G18 = [
    (32768,   8,   10.0), (32768,   8,   40.0), (32768,   8,  160.0),
    (65536,  50,   10.0), (65536,  50,   50.0), (65536,  50,  150.0), (65536, 50, 400.0),
    (65536, 100,   10.0), (65536, 100,   50.0), (65536, 100,  150.0),
    (65536, 100,  400.0), (65536, 100,  600.0),
    (65536, 200,    5.0), (65536, 200,   20.0), (65536, 200,   60.0), (65536, 200, 150.0),
    (65536, 300,  150.0), (65536, 400,  100.0),
]
# beyond anything this lineage has ever tested
EXTRA = [
    (65536, 200,  600.0),    # rho = 0.841, bc/n = 1.83
    (65536, 800,  100.0),    # rho = 0.706, bc/n = 1.22
    (65536, 100, 1000.0),    # rho = 0.785, bc/n = 1.53
    (65536, 400,  300.0),    # rho = 0.841, bc/n = 1.83
    (131072, 200, 800.0),    # rho = 0.705, c/n = 0.0061
    (131072, 400, 400.0),    # rho = 0.705, c/n = 0.0031
]
CELLS = G18 + EXTRA
SEED0 = 20260823820
REPS = 20000

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
    procs = []
    t0 = time.time()
    for i, (n, b, c) in enumerate(CELLS):
        out = os.path.join(HERE, "parts", f"val_{i:02d}.json")
        log = open(os.path.join(HERE, "parts", f"val_{i:02d}.log"), "w")
        p = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "elev_mc.py"),
             "--n", str(n), "--b", str(b), "--c", str(c),
             "--reps", str(REPS), "--seed", str(SEED0 + i), "--out", out],
            cwd=HERE, stdout=log, stderr=subprocess.STDOUT)
        procs.append((p, log))
        while sum(1 for q, _ in procs if q.poll() is None) >= 4:
            time.sleep(2.0)
    for p, log in procs:
        p.wait()
        log.close()
    cells = []
    for i in range(len(CELLS)):
        fn = os.path.join(HERE, "parts", f"val_{i:02d}.json")
        if os.path.exists(fn):
            cells.append(json.load(open(fn)))
    json.dump(dict(seed0=SEED0, n_rep=REPS, grid="G18+EXTRA6", cells=cells),
              open(os.path.join(HERE, "elev_validate_results.json"), "w"), indent=1)
    print(f"done, {len(cells)}/{len(CELLS)} cells, {time.time()-t0:.0f}s")
