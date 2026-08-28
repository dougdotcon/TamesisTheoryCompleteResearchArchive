"""
a03_ratio_and_ncross.py -- using the independent grid solver of
a02_grid_neumann_solver.py, this script:

 (A) Reproduces the successive-difference ratio tables published in
     h1_volterra_attempt/ATTEMPT.md Sec 6.2/6.3 (and independently
     re-derived by that front's own referee), at c=100 (y=0.5,1.0,2.0) and
     c=1000 (y=1.0) -- spot-checking claim 5 of the mandate.

 (B) Computes n_cross(y) (smallest n after which the ratio stays
     permanently below 0.5, matching the predecessor's own definition
     exactly) at a fine y-grid (0.5 to 6.0, step 0.5) for c=100 and
     c=1000 -- reproducing the target front's own Sec 5.4 measurement
     independently, and thereby also cross-checking the internal
     count-consistency of the target's own Sec 5.3 claims.

 (C) Compares every measured n_cross(y) against the target's rigorous
     bound n_cross_rigorous(y) = ceil(M*e*y)+1, M=sqrt(pi/2)+eps, to
     verify the "rigorous bound dominates every measured point" claim
     (claim 3 of the mandate).
"""
import numpy as np
import math
import time
import sys
sys.path.insert(0, ".")
from a02_grid_neumann_solver import run_solver, phi_at

SQRT_PI_2 = math.sqrt(math.pi/2)

def successive_diff_ratios(vals, n_ratios=5):
    diffs = [vals[i]-vals[i-1] for i in range(1, len(vals))]
    ratios = []
    for i in range(1, len(diffs)):
        if diffs[i-1] == 0:
            ratios.append(float('nan'))
        else:
            ratios.append(abs(diffs[i]/diffs[i-1]))
    return ratios[:n_ratios]

NOISE_FLOOR = 1e-13  # float64 double-precision noise floor for this problem's
                      # magnitude scale (Phi ~ O(0.01-0.3)); below this, a
                      # successive difference is float64 rounding noise, not
                      # a meaningful Picard-iteration residual -- once the
                      # iteration has converged this far, it has certainly
                      # already crossed any threshold ratio a converged
                      # (super-geometrically decaying) sequence would need.

def n_cross_from_ratios(vals, threshold=0.5):
    """Smallest n (Picard step index) after which the successive-difference
    ratio stays PERMANENTLY below `threshold`, exactly the predecessor's own
    stated definition ("the smallest n after which the ratio stays
    permanently below 0.5") -- but robust to float64 noise once the
    iteration has converged to machine precision (diffs below NOISE_FLOOR
    are treated as "the tail has converged", not as spurious noise ratios)."""
    diffs = [vals[i]-vals[i-1] for i in range(1, len(vals))]
    ratios = []
    for i in range(1, len(diffs)):
        if abs(diffs[i-1]) < NOISE_FLOOR:
            ratios.append(None)   # denominator is noise -> treat as "converged", not a real ratio
        elif abs(diffs[i]) < NOISE_FLOOR:
            ratios.append(0.0)    # numerator has converged to noise floor -> effectively 0
        else:
            ratios.append(abs(diffs[i]/diffs[i-1]))
    # find smallest i such that every subsequent entry is either < threshold
    # or None (meaning "already converged past floating point resolution",
    # which certainly satisfies "ratio stays below threshold" mathematically)
    for i in range(len(ratios)):
        ok = True
        for r in ratios[i:]:
            if r is not None and r >= threshold:
                ok = False
                break
        if ok:
            return i+2
    return None

def M_bound(eps):
    return SQRT_PI_2 + eps

def n_cross_rigorous(y, eps):
    M = M_bound(eps)
    return math.ceil(M*math.e*y) + 1

if __name__ == "__main__":
    t_start = time.time()
    print("="*70)
    print("PART A: successive-difference ratio spot-check")
    print("="*70)
    # c=100, need y up to 2.0, use modest n_max
    xs,ys,hist,eps100 = run_solver(c=100, h=0.1, Ymax=6.0, Umax=6.0, n_max=8, verbose=False)
    for y0 in [0.5, 1.0, 2.0]:
        vals = phi_at(hist, xs, ys, 0.0, y0)
        ratios = successive_diff_ratios(vals, n_ratios=5)
        print(f"c=100, y={y0}: this referee's ratios (n=2..6) = "
              f"{[round(r,4) for r in ratios]}")
    published = {
        (100,0.5): [0.207,0.076,0.044,0.031,0.025],
        (100,1.0): [0.552,0.197,0.105,0.068,0.049],
        (100,2.0): [1.124,0.432,0.238,0.154,0.109],
    }
    print()
    print("Published (h1_volterra_attempt Sec 6.2, transcribed as plain text):")
    for k,v in published.items():
        print(f"  c={k[0]}, y={k[1]}: {v}")

    print()
    xs2,ys2,hist2,eps1000 = run_solver(c=1000, h=0.1, Ymax=6.0, Umax=6.0, n_max=8, verbose=False)
    vals = phi_at(hist2, xs2, ys2, 0.0, 1.0)
    ratios = successive_diff_ratios(vals, n_ratios=5)
    print(f"c=1000, y=1.0: this referee's ratios (n=2..6) = {[round(r,4) for r in ratios]}")
    print("Published (h1_volterra_attempt Sec 6.3): [1.112, 0.447, 0.258, 0.175, 0.130]")
    print(f"  (elapsed so far: {time.time()-t_start:.1f}s)")

    print()
    print("="*70)
    print("PART B: n_cross(y) fine grid, c=100 and c=1000, y=0.5..6.0 step 0.5")
    print("="*70)
    n_max_big = 14
    xsB, ysB, histB, epsB100 = run_solver(c=100, h=0.1, Ymax=6.0, Umax=6.0, n_max=n_max_big, verbose=False)
    print(f"  (c=100 solve done, elapsed {time.time()-t_start:.1f}s)")
    xsB2, ysB2, histB2, epsB1000 = run_solver(c=1000, h=0.1, Ymax=6.0, Umax=6.0, n_max=n_max_big, verbose=False)
    print(f"  (c=1000 solve done, elapsed {time.time()-t_start:.1f}s)")

    yvals = [round(0.5*k,2) for k in range(1,13)]  # 0.5 .. 6.0 step 0.5
    results = {}
    for c, xs_, ys_, hist_, eps_ in [(100, xsB, ysB, histB, epsB100), (1000, xsB2, ysB2, histB2, epsB1000)]:
        row = []
        for y0 in yvals:
            vals = phi_at(hist_, xs_, ys_, 0.0, y0)
            nc = n_cross_from_ratios(vals, threshold=0.5)
            nc_rig = n_cross_rigorous(y0, eps_)
            row.append((y0, nc, nc_rig))
        results[c] = row
        print(f"\nc={c}, eps={eps_:.6f}, M=sqrt(pi/2)+eps={M_bound(eps_):.6f}:")
        print(f"{'y':>6} {'n_cross (this ref.)':>20} {'n_cross_rigorous':>18} {'dominates?':>12}")
        for y0,nc,ncr in row:
            dom = (nc is not None) and (ncr >= nc)
            print(f"{y0:>6} {str(nc):>20} {ncr:>18} {str(dom):>12}")

    print()
    print(f"Total elapsed: {time.time()-t_start:.1f}s")

    print()
    print("="*70)
    print("PART C: comparison against predecessor's/target's published integer-y table")
    print("="*70)
    predecessor_table = {
        100:  {0.5:2, 1.0:2, 2.0:3, 3.0:4, 4.0:4, 5.0:5, 6.0:5},
        1000: {0.5:2, 1.0:3, 2.0:4, 3.0:5, 4.0:6, 5.0:6, 6.0:7},
    }
    for c in [100,1000]:
        row = dict((y0,nc) for y0,nc,_ in results[c])
        print(f"\nc={c}:")
        print(f"{'y':>6} {'predecessor pub.':>18} {'this referee':>14} {'match?':>8}")
        exact = 0
        for y0 in [0.5,1.0,2.0,3.0,4.0,5.0,6.0]:
            pub = predecessor_table[c][y0]
            mine = row.get(y0)
            match = (pub == mine)
            exact += int(match)
            print(f"{y0:>6} {pub:>18} {str(mine):>14} {str(match):>8}")
        print(f"  exact matches: {exact}/7")
