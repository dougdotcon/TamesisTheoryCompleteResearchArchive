"""
k06_uniformity_analysis.py -- post-processes k04_uniformity_grid_results.json
into the uniformity metrics reported in ATTEMPT.md Section 5.4/5.5:

  order-1 test:  ratio1(x,c) := gap1(x,c) / (eps * psi2... )  -- WRONG, see
  actual definition below (gap1 already uses psi2 as the order-1
  prediction target; the NEXT-order comparison uses psi3):

  ratio_{N}(x,c) := gap_N(x,c) / (eps * psi_{N+2}(x))

  where gap_N := rho_N - psi_{N+1}(x) is the residual AFTER matching
  the derived asymptotic prediction through order N+1 (see k04's own
  in-line comments), so ratio_N should -> 1 as eps -> 0 at each fixed x
  if the (N+1)->(N+2) order matched-asymptotics step is valid there.
  This script computes ratio_1 (using psi3, N=1) and ratio_2 (using
  psi4, N=2) across the whole (x,c) grid, plus a per-x linear
  extrapolation of ratio_N(x,eps) to eps=0 (least squares over all 6
  c-values), and reports the extrapolated value's distance from the
  H1-predicted 1 -- the central UNIFORMITY-IN-x diagnostic of this
  front: does this distance stay bounded (or even shrink, as observed)
  as x grows, or does it blow up?
"""
import json
import mpmath as mp
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k03_profiles as prof

mp.mp.dps = 50

with open("k04_uniformity_grid_results.json") as f:
    data = json.load(f)

by_x = {}
for r in data:
    x = r["x"]
    eps = mp.mpf(r["eps"])
    gap1 = mp.mpf(r["gap1"])
    gap2 = mp.mpf(r["gap2"])
    psi3v = mp.mpf(r["psi3"])
    psi4v = prof.psi4(x)
    ratio1 = gap1 / (eps * psi3v)
    ratio2 = gap2 / (eps * psi4v) if psi4v != 0 else None
    by_x.setdefault(x, []).append((eps, ratio1, ratio2))


def linfit_extrap(pairs):
    """Least-squares fit y = a + b*eps over the given (eps, y) pairs;
    returns the extrapolated intercept a (value at eps=0)."""
    n = len(pairs)
    sx = sum(e for e, _ in pairs)
    sy = sum(y for _, y in pairs)
    sxx = sum(e * e for e, _ in pairs)
    sxy = sum(e * y for e, y in pairs)
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = (sy - b * sx) / n
    return a


print("=== ORDER-1 uniformity: ratio1(x,c) := gap1/(eps*psi3(x)), should -> 1 ===")
print(f"{'x':>5}  ratios (c=200..8000, ascending)")
extrap1 = {}
for x in sorted(by_x, key=float):
    lst = sorted(by_x[x])
    print(f"{x:>5}  " + ", ".join(mp.nstr(r1, 5) for _, r1, _ in lst))
    extrap1[x] = linfit_extrap([(e, r1) for e, r1, _ in lst])

print("\nlinear extrapolation to eps->0 (order-1 test):")
for x in sorted(extrap1, key=float):
    a = extrap1[x]
    print(f"  x={x:>5}: extrap={mp.nstr(a,8)}  |1-extrap|={mp.nstr(abs(1-a),4)}")

print("\n=== ORDER-2 uniformity: ratio2(x,c) := gap2/(eps*psi4(x)), should -> 1 ===")
print(f"{'x':>5}  ratios (c=200..8000, ascending)")
extrap2 = {}
for x in sorted(by_x, key=float):
    lst = sorted(by_x[x])
    print(f"{x:>5}  " + ", ".join(mp.nstr(r2, 5) for _, _, r2 in lst))
    extrap2[x] = linfit_extrap([(e, r2) for e, _, r2 in lst])

print("\nlinear extrapolation to eps->0 (order-2 test):")
for x in sorted(extrap2, key=float):
    a = extrap2[x]
    print(f"  x={x:>5}: extrap={mp.nstr(a,8)}  |1-extrap|={mp.nstr(abs(1-a),4)}")

print("\n=== Summary: does |1-extrap| grow or shrink with x? ===")
xs_sorted = sorted(extrap1, key=float)
o1 = [float(abs(1 - extrap1[x])) for x in xs_sorted]
o2 = [float(abs(1 - extrap2[x])) for x in xs_sorted]
print("x:              ", xs_sorted)
print("order-1 |1-extrap|:", [f"{v:.4g}" for v in o1])
print("order-2 |1-extrap|:", [f"{v:.4g}" for v in o2])
print("order-1 monotone non-increasing in x:", all(o1[i] >= o1[i+1] - 1e-9 for i in range(len(o1)-1)))
print("order-2 monotone non-increasing in x:", all(o2[i] >= o2[i+1] - 1e-9 for i in range(len(o2)-1)))
