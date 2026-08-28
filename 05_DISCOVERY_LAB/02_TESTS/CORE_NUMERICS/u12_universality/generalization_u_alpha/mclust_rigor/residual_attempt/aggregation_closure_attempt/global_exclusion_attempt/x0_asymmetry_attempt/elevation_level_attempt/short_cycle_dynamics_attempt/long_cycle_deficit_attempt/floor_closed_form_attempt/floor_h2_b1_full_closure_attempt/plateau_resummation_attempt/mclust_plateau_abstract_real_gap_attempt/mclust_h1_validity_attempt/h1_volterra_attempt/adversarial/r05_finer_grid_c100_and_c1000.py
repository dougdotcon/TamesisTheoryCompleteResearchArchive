"""
r05_finer_grid_c100_and_c1000.py
---------------------------------
Reruns r04_independent_neumann_iteration.py's `run()` at h=0.1 (matching
ATTEMPT.md's own grid spacing exactly, vs. r04's coarser h=0.2 scan), at
both c=100 and c=1000, to directly compare successive-difference ratios
against the specific numbers ATTEMPT.md Sec 6.2/6.3 publishes.

Run as: python3 r05_finer_grid_c100_and_c1000.py
(imports run() from r04_independent_neumann_iteration.py, which must sit
in the same directory)
"""
import time, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "r04_independent_neumann_iteration.py")).read().split('if __name__')[0])
import numpy as np

def report(c, ytests, ymax_track, n_max, h=0.1, Umax=6.0):
    t0 = time.time()
    print(f"=== c={c}, h={h}, ymax_track={ymax_track}, n_max={n_max}, Umax={Umax} ===")
    xs, ys, Phis, eps = run(c, h, ymax_track, n_max, Umax=Umax)
    print(f"eps={eps}  (elapsed {time.time()-t0:.2f}s)")
    ix0 = 0
    for ytest in ytests:
        iy = int(round(ytest/h))
        if iy >= len(ys):
            continue
        seq = [Phis[n][ix0, iy] for n in range(n_max+1)]
        diffs = [abs(seq[n]-seq[n-1]) for n in range(1, n_max+1)]
        ratios = [diffs[n]/diffs[n-1] if diffs[n-1] > 1e-300 else float('nan')
                  for n in range(1, len(diffs))]
        print(f"y={ys[iy]:.2f}: successive-diff ratios: " +
              ", ".join(f"{r:.4f}" for r in ratios))
    print()

if __name__ == "__main__":
    print("Independent reproduction attempt of ATTEMPT.md Sec 6.2 (c=100) and")
    print("Sec 6.3 (c=1000) successive-difference ratio tables, built from a")
    print("FRESH from-scratch grid Neumann/Picard implementation (r04), not")
    print("from any .py file of the target front or its ancestors.\n")
    print("ATTEMPT.md Sec 6.2 (c=100) published values, for comparison:")
    print("  y=0.5: ratios = 0.207, 0.076, 0.044, 0.031, 0.025, ...")
    print("  y=1.0: ratios = 0.552, 0.197, 0.105, 0.068, 0.049, ...")
    print("  y=2.0: ratios = 1.124, 0.432, 0.238, 0.154, 0.109, ...")
    print("ATTEMPT.md Sec 6.3 (c=1000) published value, for comparison:")
    print("  y=1.0: ratios = 1.112, 0.447, 0.258, 0.175, 0.130, ...")
    print()
    report(100, [0.5, 1.0, 2.0], ymax_track=2.0, n_max=6, h=0.1, Umax=6.0)
    report(1000, [1.0], ymax_track=2.0, n_max=8, h=0.1, Umax=6.0)
