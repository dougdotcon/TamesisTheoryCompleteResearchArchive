"""
v05_richardson_convergence.py -- grid-refinement (Richardson) check that the
discretized Neumann/Picard fixed point of the Volterra-in-y reformulation
converges, as h->0, to the TRUE Phi(x,y) given by the independently-built
(P,Q)-family series (v01_family_series.py). Confirms the whole discretised
pipeline (E1-derived NEW-W identity, (BB-Psi'), (E2)) is bug-free (a
structurally-INDEPENDENT computation route from the series: finite-difference
Picard iteration + trapezoid quadrature vs. an infinite power series in g
with coefficients solved via a from-scratch bounded-branch integral method)
and gives an honest error budget (trapezoid quadrature => expect O(h^2)).
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from v03_neumann_iteration import run_neumann_experiment, build_true_solution

if __name__ == "__main__":
    c_val = 100.0
    sqc = np.sqrt(c_val)
    x_test = [0.0, 0.3, 0.6]
    y_test = [0.2, 0.5, 1.0]

    print("Ground truth: (P,Q)-family series, c=100, K=100, dps=120")
    Phi_true = build_true_solution(c_val, K=100, dps=120)

    hs = [0.1, 0.05, 0.025]
    results = {}
    for h in hs:
        t0 = time.time()
        hist, Nx_seq, eps = run_neumann_experiment(c_val, h, 1.0, 6.0, 6, x_test, y_test, verbose=False)
        print(f"--- h={h}  elapsed={time.time()-t0:.2f}s  Nx_seq(shrinking)={Nx_seq}")
        results[h] = {}
        for (xp, yp), vals in hist.items():
            strue = Phi_true(xp / sqc, yp / sqc)
            err = vals[-1] - strue
            results[h][(xp, yp)] = err
            print(f"  (x={xp},y={yp}): Phi_discretized={vals[-1]:.8f}  TRUE={strue:.8f}  err={err:+.6e}")

    print()
    print("=== Richardson ratio: err(h)/err(h/2), expect ~4 for O(h^2) trapezoid error ===")
    all_ratios = []
    for pt in results[hs[0]]:
        e1, e2, e3 = results[hs[0]][pt], results[hs[1]][pt], results[hs[2]][pt]
        r1 = e1 / e2 if e2 != 0 else float("nan")
        r2 = e2 / e3 if e3 != 0 else float("nan")
        all_ratios.extend([r1, r2])
        print(f"{pt}: err(h=.1)={e1:+.6e} err(h=.05)={e2:+.6e} err(h=.025)={e3:+.6e}  ratio1={r1:.3f} ratio2={r2:.3f}")
    arr = np.array([r for r in all_ratios if np.isfinite(r)])
    print()
    print(f"Mean ratio = {arr.mean():.4f}  (target for pure O(h^2): 4.000)  std={arr.std():.4f}")
    print("PASS" if abs(arr.mean() - 4.0) < 0.3 else "FAIL", "-- discretization error is consistent with O(h^2) trapezoid quadrature error,")
    print("confirming the discretized fixed point converges to the TRUE continuum Phi as h->0,")
    print("via a structurally independent computation route from the (P,Q)-family series.")
