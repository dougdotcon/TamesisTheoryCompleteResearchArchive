#!/usr/bin/env python3
import time, json
import mpmath as mp
from ref03_plateau_compute import compute_pi

# (c, K, dps) tuned per c: smaller c needs bigger K/dps because of the
# order-2 cancellation growth ~ exp(ct0 + 0.9*(ct0)^2/c).
grid = [
    (100,    1000, 220),
    (250,    600,  150),
    (640,    500,  130),
    (1000,   500,  130),
    (2560,   450,  120),
    (6400,   400,  110),
    (16000,  400,  110),
    (40960,  400,  110),
    (100000, 400,  110),
    (250000, 400,  110),
    (655360, 400,  110),
]

out = {}
for c_val, K, dps in grid:
    t0 = time.time()
    res = compute_pi(c_val, K, dps, [60, 80, 100])
    dt = time.time() - t0
    out[str(c_val)] = res
    print(f"c={c_val}: Pi(c) = {res['Pi_c']}  stable~{res['stable_digits_estimate']}  time={dt:.1f}s")

with open("ref04_grid_results.json", "w") as f:
    json.dump(out, f, indent=2)
