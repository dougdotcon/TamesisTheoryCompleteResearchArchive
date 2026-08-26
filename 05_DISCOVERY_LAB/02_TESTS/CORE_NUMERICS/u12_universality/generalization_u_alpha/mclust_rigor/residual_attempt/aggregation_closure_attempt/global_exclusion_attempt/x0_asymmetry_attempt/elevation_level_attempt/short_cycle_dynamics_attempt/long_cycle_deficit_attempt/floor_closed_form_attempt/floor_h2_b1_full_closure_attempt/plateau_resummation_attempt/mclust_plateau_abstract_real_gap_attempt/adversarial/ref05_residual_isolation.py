#!/usr/bin/env python3
"""
Independent residual-isolation fit for d4, d5 using MY OWN Pi(c) grid
(ref04_grid_results.json), and the ALREADY-EXACT closed forms
d0=1, d1=-2*sqrt(2/pi), d2=7/2, d3=-(34/3)*sqrt(2/pi) (established, not
re-derived here -- these are the record's own DERIVED+numerically-confirmed
coefficients, matched independently against my own grid below as a sanity
check before trusting the higher-order residual).
"""
import json
import mpmath as mp

mp.mp.dps = 60

with open("ref04_grid_results.json") as f:
    grid = json.load(f)

d0 = mp.mpf(1)
d1 = -2 * mp.sqrt(mp.mpf(2) / mp.pi)
d2 = mp.mpf('3.5')
d3 = -(mp.mpf(34) / 3) * mp.sqrt(mp.mpf(2) / mp.pi)

print("d0..d3 (closed forms):", d0, d1, d2, d3)

rows = []
for cstr, entry in grid.items():
    c = mp.mpf(cstr)
    pi_c = mp.mpf(entry["Pi_c"])
    eps = 1 / mp.sqrt(c)
    y = pi_c * mp.sqrt(2 * c / mp.pi)
    R4 = (y - d0 - d1 * eps - d2 * eps**2 - d3 * eps**3) / eps**4
    rows.append((c, eps, y, R4))

rows.sort(key=lambda r: r[0])  # sort by c ascending -> eps descending
print("\nc, eps, y, R4:")
for c, eps, y, R4 in rows:
    print(f"  c={float(c):>10.0f}  eps={float(eps):.6f}  y={mp.nstr(y,15)}  R4={mp.nstr(R4,10)}")

# d0..d3 sanity check: compare y directly against the closed-form prediction
# through order 3, i.e. check that (y - d0 - d1 eps - d2 eps^2 - d3 eps^3) is
# indeed O(eps^4) and not, say, O(eps^2) (which would falsify d2/d3).
print("\nSanity: (y-d0-d1eps-d2eps^2)/eps^3 should -> d3 as eps->0:")
for c, eps, y, R4 in rows:
    val = (y - d0 - d1 * eps - d2 * eps**2) / eps**3
    print(f"  c={float(c):>10.0f}  eps={float(eps):.6f}  (y-..)/eps^3={mp.nstr(val,8)}  (pred d3={mp.nstr(d3,8)})")

# Now fit R4(eps) = d4 + d5*eps + O(eps^2) via least squares / exact small fits
def linfit(xs, ys):
    # simple 2-point / least-squares linear fit d4 + d5*x = y
    n = len(xs)
    if n == 2:
        x1, x2 = xs
        y1, y2 = ys
        d5f = (y2 - y1) / (x2 - x1)
        d4f = y1 - d5f * x1
        return d4f, d5f
    # least squares
    sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    n = mp.mpf(len(xs))
    d5f = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    d4f = (sy - d5f * sx) / n
    return d4f, d5f

def quadfit(xs, ys):
    # exact/least-squares quadratic fit d4 + d5*x + d6*x^2 = y (Vandermonde LSQ via normal equations)
    n = len(xs)
    S0 = mp.mpf(n)
    S1 = sum(xs); S2 = sum(x**2 for x in xs); S3 = sum(x**3 for x in xs); S4 = sum(x**4 for x in xs)
    T0 = sum(ys); T1 = sum(x*y for x, y in zip(xs, ys)); T2 = sum(x**2*y for x, y in zip(xs, ys))
    A = mp.matrix([[S0, S1, S2], [S1, S2, S3], [S2, S3, S4]])
    b = mp.matrix([T0, T1, T2])
    sol = mp.lu_solve(A, b)
    return sol[0], sol[1], sol[2]

xs_all = [r[1] for r in rows]
ys_all = [r[3] for r in rows]

print("\n--- Fits for d4, d5 ---")

# all 11 points, linear
d4_lin_all, d5_lin_all = linfit(xs_all, ys_all)
print(f"linear fit, all {len(xs_all)} pts: d4={mp.nstr(d4_lin_all,10)}  d5={mp.nstr(d5_lin_all,10)}")

# 5 largest-c (smallest eps) points
rows_by_c_desc = sorted(rows, key=lambda r: -r[0])
top5 = rows_by_c_desc[:5]
xs5 = [r[1] for r in top5]; ys5 = [r[3] for r in top5]
d4_5, d5_5 = linfit(xs5, ys5)
print(f"linear fit, 5 largest-c: d4={mp.nstr(d4_5,10)}  d5={mp.nstr(d5_5,10)}")

# quadratic fit, 7 largest-c points
top7 = rows_by_c_desc[:7]
xs7 = [r[1] for r in top7]; ys7 = [r[3] for r in top7]
d4_q7, d5_q7, d6_q7 = quadfit(xs7, ys7)
print(f"quadratic fit, 7 largest-c: d4={mp.nstr(d4_q7,10)}  d5={mp.nstr(d5_q7,10)}  d6={mp.nstr(d6_q7,10)}")

# quadratic fit, all 11 points (over-determined LSQ)
d4_qall, d5_qall, d6_qall = quadfit(xs_all, ys_all)
print(f"quadratic fit, all 11 pts (LSQ): d4={mp.nstr(d4_qall,10)}  d5={mp.nstr(d5_qall,10)}  d6={mp.nstr(d6_qall,10)}")

# Compare against conjectured values
d4_conj = mp.mpf(209) / 8
d5_conj = -(mp.mpf(1546) / 15) * mp.sqrt(mp.mpf(2) / mp.pi)
print(f"\nConjectured d4 = 209/8 = {mp.nstr(d4_conj,10)}")
print(f"Conjectured d5 = -(1546/15)*sqrt(2/pi) = {mp.nstr(d5_conj,10)}")

def pctdiff(a, b):
    return float((a - b) / b * 100)

print(f"\nquadratic-7 d4 vs conj: {pctdiff(d4_q7, d4_conj):.5f}%  ({mp.nstr(d4_q7,10)} vs {mp.nstr(d4_conj,10)})")
print(f"quadratic-7 d5 vs conj: {pctdiff(d5_q7, d5_conj):.5f}%  ({mp.nstr(d5_q7,10)} vs {mp.nstr(d5_conj,10)})")
print(f"linear-all d4 vs conj: {pctdiff(d4_lin_all, d4_conj):.5f}%")
print(f"linear-5 d4 vs conj: {pctdiff(d4_5, d4_conj):.5f}%")

# compare against TARGET document's own claimed values
d4_target = mp.mpf('26.1246')
d5_target = mp.mpf('-82.017')
print(f"\nTarget doc claims: d4={d4_target}  d5={d5_target}")
print(f"My quadratic-7 d4 vs target's: diff = {mp.nstr(d4_q7-d4_target,6)}")
print(f"My quadratic-7 d5 vs target's: diff = {mp.nstr(d5_q7-d5_target,6)}")
