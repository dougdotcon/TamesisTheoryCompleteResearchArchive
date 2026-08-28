"""
v06_warmup_vs_y.py -- characterizes the two-regime behavior of the Neumann/
Picard partial sums Phi^(n) = g + L[Phi^(n-1)] for the closed Volterra-in-y
system: an initial "warm-up" phase (successive-difference ratio can exceed 1
for the first few n, at large y) followed by an eventual SUPER-GEOMETRIC
decay (the ratio itself keeps shrinking with n -- the qualitative signature
of the classical (M*Y)^n/n! Volterra quasi-nilpotency bound, here verified
numerically for a system whose self-referential closure is NOT confined to
a compact x-domain, see Sec 5 of ATTEMPT.md for the analytic discussion of
why the classical theorem does not apply outright here).

Measures, for a range of y at two values of c, the smallest n after which the
ratio of successive |Phi^(n)-Phi^(n-1)| differences stays permanently below
0.5 ("n_cross") -- an empirical proxy for the warm-up length.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from v03_neumann_iteration import run_neumann_experiment


def find_crossover(diffs, thresh=0.5):
    ratios = []
    for i in range(1, len(diffs)):
        if diffs[i - 1] > 0:
            ratios.append(diffs[i] / diffs[i - 1])
        else:
            ratios.append(float("nan"))
    for i, r in enumerate(ratios):
        if r == r and r < thresh and all((rr == rr and rr < thresh) for rr in ratios[i:]):
            return i + 2, ratios
    return None, ratios


if __name__ == "__main__":
    h = 0.1
    Umax = 6.0
    for c_val in [100.0, 1000.0]:
        print(f"=== c={c_val}, eps={1/np.sqrt(c_val):.6f} ===")
        Ycore = 6.0
        n_max = 16
        x_test = [0.0]
        y_test = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        t0 = time.time()
        hist, Nx_seq, eps = run_neumann_experiment(c_val, h, Ycore, Umax, n_max, x_test, y_test, verbose=False)
        print(f"  elapsed={time.time()-t0:.2f}s  Nx_max={Nx_seq[0]}")
        crossings = []
        for (xp, yp), vals in hist.items():
            diffs = [abs(vals[n] - vals[n - 1]) for n in range(1, len(vals))]
            n_cross, ratios = find_crossover(diffs)
            crossings.append((yp, n_cross))
            rstr = ", ".join(f"{r:.3f}" if r == r else "nan" for r in ratios)
            print(f"  y={yp}: n_cross(ratio<0.5 permanently)={n_cross}   ratios=[{rstr}]")
        print()
        ys = [yy for yy, nc in crossings if nc is not None]
        ncs = [nc for yy, nc in crossings if nc is not None]
        if len(ys) >= 2:
            slope, intercept = np.polyfit(ys, ncs, 1)
            print(f"  linear fit n_cross ~ {slope:.3f}*y + {intercept:.3f}  (least squares over {len(ys)} points)")
        print()
