"""
g05_residual_isolation.py -- an independent numerical route to the 5th
asymptotic coefficient d4 (the eps^4 term of y(eps):=Pi(c)*sqrt(2c/pi)),
and a first numerical read on d5, DIFFERENT FROM plateau_resummation_
attempt's own method (its own blind degree-6/7 Vandermonde fit of ALL of
d0..d6 simultaneously, ill-conditioned past d3 by its own admission).

METHOD ("residual isolation"): d0, d1, d2, d3 are already established in
CLOSED FORM (DERIVED, heuristic n<=4, machine-verified algebra, plus
independently confirmed to 12/9/6/4 digits by two prior independent
numerical fits -- plateau_resummation_attempt SS5 and its referee SS3.4).
Using the EXACT closed-form values for d0..d3 (not re-fitted), define

    R4(c) := [y(eps) - d0 - d1*eps - d2*eps^2 - d3*eps^3] / eps^4

which should converge to d4 as eps->0 (c->infty), with R4(c) = d4 +
d5*eps + O(eps^2). This is much better-conditioned than a simultaneous
high-degree fit of ALL coefficients, because it does not need to
"re-discover" d0..d3 from noisy/truncated data -- it uses their own
already-established closed forms directly, isolating only the two
genuinely unknown quantities (d4, d5) in a plain LINEAR fit of R4 against
eps.

Uses this front's own fresh (P,Q)-family computation (g04_grid_results.json,
11 values of c spanning c=100..655360, a 6553x range -- WIDER than either
ancestor front's own 1024x range, reaching c=100, a value NEITHER ancestor
front's own direct-summation method could complete).
"""
import json
import mpmath as mp

mp.mp.dps = 50

SQRT_2_PI = mp.sqrt(2 / mp.pi)  # = sqrt(2/pi)
D0 = mp.mpf(1)
D1 = -2 * SQRT_2_PI
D2 = mp.mpf(7) / 2
D3 = -(mp.mpf(34) / 3) * SQRT_2_PI

D4_CONJECTURED = mp.mpf(209) / 8            # = 26.125, UNPROVEN (record's own gamma_5=209/24 pattern conjecture)
D5_CONJECTURED = -(mp.mpf(1546) / 15) * SQRT_2_PI  # UNPROVEN, same conjecture


def load_grid():
    with open("g04_grid_results.json") as f:
        raw = json.load(f)
    out = {}
    for c_str, rec in raw.items():
        c = mp.mpf(c_str)
        Pi = mp.mpf(rec["Pi"])
        out[c] = Pi
    return out


def main():
    grid = load_grid()
    cs = sorted(grid.keys())

    print(f"d0 (exact)  = {mp.nstr(D0,20)}")
    print(f"d1 (exact)  = {mp.nstr(D1,20)}   [= -2*sqrt(2/pi)]")
    print(f"d2 (exact)  = {mp.nstr(D2,20)}   [= 7/2]")
    print(f"d3 (exact)  = {mp.nstr(D3,20)}   [= -(34/3)*sqrt(2/pi)]")
    print()
    print(f"{'c':>10s} {'eps':>12s} {'y(eps)':>22s} {'R4(c)':>18s}")
    rows = []
    for c in cs:
        Pi = grid[c]
        eps = 1 / mp.sqrt(c)
        y = Pi * mp.sqrt(2 * c / mp.pi)
        resid = y - D0 - D1 * eps - D2 * eps**2 - D3 * eps**3
        R4 = resid / eps**4
        rows.append((c, eps, y, R4))
        print(f"{float(c):>10.0f} {float(eps):>12.6f} {mp.nstr(y,18):>22s} {mp.nstr(R4,12):>18s}")

    print()
    print("R4(c) should -> d4 as c->infty (eps->0); R4(c) ~= d4 + d5*eps + O(eps^2).")
    print(f"Conjectured (record, UNPROVEN): d4 = 209/8 = {mp.nstr(D4_CONJECTURED,10)}")
    print(f"Conjectured (record, UNPROVEN): d5 = -(1546/15)*sqrt(2/pi) = {mp.nstr(D5_CONJECTURED,10)}")
    print()

    # (a) naive extrapolation: just look at R4 at the largest c (smallest eps)
    c_max, eps_min, y_max, R4_max = rows[-1]
    print(f"R4 at largest c={float(c_max):.0f} (eps={float(eps_min):.5f}): {mp.nstr(R4_max,15)}")
    print(f"   vs conjectured d4=209/8: diff = {mp.nstr(R4_max-D4_CONJECTURED,6)}"
          f"  ({mp.nstr(100*(R4_max-D4_CONJECTURED)/D4_CONJECTURED,4)}% )")

    # (b) linear fit of R4(c) vs eps over ALL points: R4 = d4 + d5*eps
    #     (least-squares by hand, exact rational-free formula, mpmath)
    n = len(rows)
    xs = [r[1] for r in rows]   # eps
    ys = [r[3] for r in rows]   # R4
    mx = sum(xs) / n
    my = sum(ys) / n
    Sxx = sum((x - mx) ** 2 for x in xs)
    Sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    d5_fit = Sxy / Sxx
    d4_fit = my - d5_fit * mx
    print()
    print(f"Linear fit R4(eps) = d4 + d5*eps  (all {n} points, least squares):")
    print(f"   d4_fit = {mp.nstr(d4_fit, 15)}")
    print(f"   d5_fit = {mp.nstr(d5_fit, 15)}")
    print(f"   d4_fit vs conjectured 209/8={mp.nstr(D4_CONJECTURED,10)}: "
          f"diff={mp.nstr(d4_fit-D4_CONJECTURED,6)} ({mp.nstr(100*(d4_fit-D4_CONJECTURED)/D4_CONJECTURED,4)}%)")
    print(f"   d5_fit vs conjectured {mp.nstr(D5_CONJECTURED,10)}: "
          f"diff={mp.nstr(d5_fit-D5_CONJECTURED,6)} ({mp.nstr(100*(d5_fit-D5_CONJECTURED)/D5_CONJECTURED,4)}%)")

    # (c) restrict the linear fit to only the 5 largest-c (smallest-eps)
    #     points, where the linear (in eps) approximation to R4 should be
    #     most accurate (least contamination from d6*eps^2+...)
    sub = rows[-5:]
    xs2 = [r[1] for r in sub]
    ys2 = [r[3] for r in sub]
    n2 = len(sub)
    mx2 = sum(xs2) / n2
    my2 = sum(ys2) / n2
    Sxx2 = sum((x - mx2) ** 2 for x in xs2)
    Sxy2 = sum((x - mx2) * (y - my2) for x, y in zip(xs2, ys2))
    d5_fit2 = Sxy2 / Sxx2
    d4_fit2 = my2 - d5_fit2 * mx2
    print()
    print(f"Same linear fit, restricted to the {n2} LARGEST-c points (c>={float(sub[0][0]):.0f}):")
    print(f"   d4_fit = {mp.nstr(d4_fit2, 15)}")
    print(f"   d5_fit = {mp.nstr(d5_fit2, 15)}")
    print(f"   d4_fit vs conjectured: diff={mp.nstr(d4_fit2-D4_CONJECTURED,6)} "
          f"({mp.nstr(100*(d4_fit2-D4_CONJECTURED)/D4_CONJECTURED,4)}%)")

    # (d) stability check: same fit using only the 4 SMALLEST-c points
    #     (widest eps range -- tests whether d4/d5 extraction is stable
    #     across which subset of the grid is used, a basic overfitting/
    #     contamination diagnostic)
    sub3 = rows[:4]
    xs3 = [r[1] for r in sub3]
    ys3 = [r[3] for r in sub3]
    n3 = len(sub3)
    mx3 = sum(xs3) / n3
    my3 = sum(ys3) / n3
    Sxx3 = sum((x - mx3) ** 2 for x in xs3)
    Sxy3 = sum((x - mx3) * (y - my3) for x, y in zip(xs3, ys3))
    d5_fit3 = Sxy3 / Sxx3
    d4_fit3 = my3 - d5_fit3 * mx3
    print()
    print(f"Same linear fit, restricted to the {n3} SMALLEST-c points (c<={float(sub3[-1][0]):.0f}):")
    print(f"   d4_fit = {mp.nstr(d4_fit3, 15)}")
    print(f"   d5_fit = {mp.nstr(d5_fit3, 15)}")

    print()
    print("Cross-subset stability of d4 (this front's own diagnostic, analogous")
    print("to the ancestor front's own cross-subset check for its d0..d6 fit):")
    print(f"   all-11-point fit:      d4 = {mp.nstr(d4_fit,10)}")
    print(f"   5-largest-c fit:       d4 = {mp.nstr(d4_fit2,10)}")
    print(f"   4-smallest-c fit:      d4 = {mp.nstr(d4_fit3,10)}")
    spread = max(d4_fit, d4_fit2, d4_fit3) - min(d4_fit, d4_fit2, d4_fit3)
    print(f"   spread across the 3 subsets = {mp.nstr(spread,6)}")
    print(f"   d5_fit (5-largest-c) vs conjectured: diff={mp.nstr(d5_fit2-D5_CONJECTURED,6)} "
          f"({mp.nstr(100*(d5_fit2-D5_CONJECTURED)/D5_CONJECTURED,4)}%)")

    # (e) quadratic fit R4 = d4 + d5*eps + d6*eps^2 on the 7 largest-c
    #     points (exact 3x3 linear solve, mpmath) -- checks whether
    #     removing a further eps^2 contamination term sharpens d4 more
    sub4 = rows[-7:]
    A = mp.matrix(3, 3)
    rhs = mp.matrix(3, 1)
    for i in range(3):
        rhs[i] = sum(r[3] * r[1] ** i for r in sub4)
        for j in range(3):
            A[i, j] = sum(r[1] ** (i + j) for r in sub4)
    sol = mp.lu_solve(A, rhs)
    d4_quad, d5_quad, d6_quad = sol[0], sol[1], sol[2]
    print()
    print(f"Quadratic fit R4(eps) = d4 + d5*eps + d6*eps^2  (7 largest-c points, exact 3x3 solve):")
    print(f"   d4 = {mp.nstr(d4_quad, 15)}   vs 209/8={mp.nstr(D4_CONJECTURED,10)}: "
          f"diff={mp.nstr(d4_quad-D4_CONJECTURED,6)} ({mp.nstr(100*(d4_quad-D4_CONJECTURED)/D4_CONJECTURED,4)}%)")
    print(f"   d5 = {mp.nstr(d5_quad, 15)}   vs conjectured={mp.nstr(D5_CONJECTURED,10)}: "
          f"diff={mp.nstr(d5_quad-D5_CONJECTURED,6)} ({mp.nstr(100*(d5_quad-D5_CONJECTURED)/D5_CONJECTURED,4)}%)")
    print(f"   d6 = {mp.nstr(d6_quad, 15)}   (no prediction on record to compare against)")

    with open("g05_residual_results.json", "w") as f:
        json.dump({
            "d4_fit_all11": mp.nstr(d4_fit, 20),
            "d5_fit_all11": mp.nstr(d5_fit, 20),
            "d4_fit_5largest": mp.nstr(d4_fit2, 20),
            "d5_fit_5largest": mp.nstr(d5_fit2, 20),
            "d4_fit_4smallest": mp.nstr(d4_fit3, 20),
            "d5_fit_4smallest": mp.nstr(d5_fit3, 20),
            "d4_conjectured_209_8": mp.nstr(D4_CONJECTURED, 20),
            "d5_conjectured": mp.nstr(D5_CONJECTURED, 20),
            "R4_table": [[mp.nstr(c, 10), mp.nstr(eps, 10), mp.nstr(R4, 15)] for c, eps, y, R4 in rows],
        }, f, indent=2)
    print("\nSaved g05_residual_results.json")


if __name__ == "__main__":
    main()
