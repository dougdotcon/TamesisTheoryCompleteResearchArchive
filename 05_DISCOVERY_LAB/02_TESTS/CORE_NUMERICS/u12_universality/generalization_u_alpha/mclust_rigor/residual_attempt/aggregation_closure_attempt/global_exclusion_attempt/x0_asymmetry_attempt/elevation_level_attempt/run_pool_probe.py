#!/usr/bin/env python3
"""Driver for elev_pool_probe.py -- T1/T2, eight cells in parallel."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (n, b, c, seed)   seeds 20260823810..817, all fresh
CELLS = [
    (65536, 100, 400.0, 20260823810),
    (65536, 300, 150.0, 20260823811),
    (65536, 100, 600.0, 20260823812),
    (65536, 400, 100.0, 20260823813),
    (65536, 200, 150.0, 20260823814),
    (65536,  50, 400.0, 20260823815),
    (65536, 100, 150.0, 20260823816),
    (32768,   8, 160.0, 20260823817),
]
INST = 800
WALKS = 50

if __name__ == "__main__":
    procs = []
    outs = []
    for (n, b, c, seed) in CELLS:
        out = os.path.join(HERE, f"pool_probe_b{b}_c{int(c)}.json")
        outs.append(out)
        log = open(os.path.join(HERE, "parts", f"pool_probe_b{b}_c{int(c)}.log"), "w")
        p = subprocess.Popen(
            [sys.executable, os.path.join(HERE, "elev_pool_probe.py"),
             "--n", str(n), "--b", str(b), "--c", str(c),
             "--inst", str(INST), "--walks", str(WALKS),
             "--seed", str(seed), "--out", out],
            cwd=HERE, stdout=log, stderr=subprocess.STDOUT)
        procs.append((p, log))
        while sum(1 for q, _ in procs if q.poll() is None) >= 4:
            os.wait()
    for p, log in procs:
        p.wait()
        log.close()
    print("done")
