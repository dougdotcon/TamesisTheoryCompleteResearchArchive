"""Adversarial measurements M1 (exponent grid), M2 (model-comparison grid),
M3 (large-n deviation study). Seeds fixed in ADVERSARIAL_NOTE.md."""
import json
import sys
import time
import numpy as np
from adv_sim import run_cell

C_GRID = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]


def run_grid(name, seed, cells, out):
    ss = np.random.SeedSequence(seed)
    streams = ss.spawn(len(cells))
    res = []
    for (n, c, N), st in zip(cells, streams):
        t0 = time.time()
        rng = np.random.default_rng(st)
        mean, std, sem, _, vals = run_cell(n, c, N, rng)
        dt = time.time() - t0
        theorem = (1 + c) ** -0.5
        rec = dict(n=n, c=c, N=N, phi_mean=mean, phi_std=std, sem=sem,
                   theorem=theorem, dev=mean - theorem, dev_over_sem=(mean - theorem) / sem,
                   seconds=round(dt, 2))
        res.append(rec)
        print(f"[{name}] n={n} c={c} N={N}: phi={mean:.6f}±{sem:.6f} "
              f"theorem={theorem:.6f} dev={mean-theorem:+.6f} ({(mean-theorem)/sem:+.1f} sem) [{dt:.1f}s]",
              flush=True)
        # persist raw samples only for M1 (needed for bootstrap of the fit)
        if name == "M1":
            rec["samples"] = vals.tolist()
    out[name] = res
    with open("adv_results.json", "w") as fh:
        json.dump(out, fh)


out = {}
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    try:
        with open("adv_results.json") as fh:
            out = json.load(fh)
    except FileNotFoundError:
        pass

    if which in ("all", "M1"):
        cells = [(2000, c, 300) for c in C_GRID]
        run_grid("M1", 424242, cells, out)

    if which in ("all", "M2"):
        cells = [(4000, c, 1000) for c in C_GRID]
        run_grid("M2", 8675309, cells, out)

    if which in ("all", "M3"):
        NS = [(2000, 8000), (4000, 8000), (8000, 8000),
              (16000, 6000), (32000, 4000), (64000, 3000)]
        cells = [(n, c, N) for c in (0.5, 50.0) for (n, N) in NS]
        run_grid("M3", 31415926, cells, out)

    print("done", flush=True)
