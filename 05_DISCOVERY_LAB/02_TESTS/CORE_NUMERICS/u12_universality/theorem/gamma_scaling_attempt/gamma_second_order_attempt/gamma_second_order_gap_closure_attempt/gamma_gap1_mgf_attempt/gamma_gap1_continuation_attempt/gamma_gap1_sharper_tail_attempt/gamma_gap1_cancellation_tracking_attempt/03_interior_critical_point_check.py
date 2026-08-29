"""
03_interior_critical_point_check.py

Script 02 found the leading-order limits of x_K(D) at the two TRUE support
endpoints D_min=-gamma*K, D_max=(1-gamma)*K. But x_K(D) is a cubic; its
absolute maximum on the closed interval [D_min,D_max] could in principle
occur at an INTERIOR critical point instead (a root of
x_K'(D) = c1 + 2*c2*D + 3*c3*D^2 = 0), which basic real-analysis calculus
requires checking, not assuming away -- this script does that check
rigorously, both symbolically (leading order) and numerically (exact, at
finite n).

Finding (spoiler, established below): since c3(K) = 1/(6n^2) -> 0 much
faster than c2(K) ~ -1/(2n) (leading order, negative for large n), x_K(D)//
restricted to the O(sqrt(n ln n))-scale window is, to leading order, a
downward parabola c0 + c1*D + c2*D^2 (c2<0) plus a vanishing cubic
correction. A downward parabola's unique critical point is a MAXIMUM
(of x_K itself, not of |x_K|) at D* = -c1/(2*c2). This script locates D*
exactly (both roots of the full cubic derivative, not just the parabola
approximation) and checks (a) whether it lies inside the true support
interval, and (b) how its value compares to the two endpoint values, both
at leading order (symbolic) and at extreme finite n (numeric, mpmath).
"""
import sympy as sp
import mpmath as mp

k, n, gamma, D = sp.symbols('k n gamma D', positive=True)
nn = sp.Symbol('n', positive=True)
K = sp.Symbol('K', positive=True)

m = sp.Symbol('m')
i = sp.Symbol('i', integer=True, positive=True)
tau_m = sp.expand(sp.summation(((k - i) / n) ** 2, (i, 1, m)))
delta_D = D * (2 * k * (1 - gamma) - D - 1) / (2 * n)
tau_M = tau_m.subs(m, gamma * k + D)
x_D = sp.expand(delta_D + tau_M / 2)
x_poly = sp.Poly(x_D, D)
c3 = sp.simplify(x_poly.coeff_monomial(D ** 3)).subs(k, K)
c2 = sp.simplify(x_poly.coeff_monomial(D ** 2)).subs(k, K)
c1 = sp.simplify(x_poly.coeff_monomial(D)).subs(k, K)
c0 = sp.simplify(x_poly.coeff_monomial(1)).subs(k, K)

x_K = c0 + c1 * D + c2 * D ** 2 + c3 * D ** 3
xprime = sp.diff(x_K, D)
print("x_K'(D) =", sp.simplify(xprime))

# Solve the quadratic x_K'(D) = c1 + 2 c2 D + 3 c3 D^2 = 0 exactly.
Dsym = sp.Symbol('Dstar')
quad = c1 + 2 * c2 * Dsym + 3 * c3 * Dsym ** 2
roots = sp.solve(sp.Eq(quad, 0), Dsym)
print()
print(f"Two exact critical-point roots (function of K, n, gamma):")
for r in roots:
    print("  D* =", sp.simplify(r))

print()
print("=" * 78)
print("Which root is O(K) (i.e. potentially inside [-gamma*K,(1-gamma)*K])")
print("and which is O(n) (far outside the support for large n)?")
print("=" * 78)
# Substitute K = sqrt(4 n ln(n) / beta) and take leading order as n->infty
# of D*/K for each root, to classify its scale relative to K.
beta = gamma * (2 - gamma) / 2
Ksub = sp.sqrt(4 * nn * sp.log(nn) / beta)
for idx, r in enumerate(roots):
    r_n = sp.simplify(r).subs(K, Ksub)
    ratio_to_K = sp.simplify(r_n / Ksub)
    lim_ratio = sp.limit(ratio_to_K, nn, sp.oo)
    print(f"Root {idx}: D*/K -> {lim_ratio} as n->infty (gamma symbolic)")

print()
print("=" * 78)
print("Evaluate the 'small' root (the one that stays O(K)) at several gamma,")
print("check numerically whether it falls inside (D_min,D_max) = ")
print("(-gamma*K, (1-gamma)*K), and if so, compare x_K there to the two")
print("endpoint values -- at ASTRONOMICALLY large, representative finite n")
print("(mpmath, high precision, exact c_i(K,n,gamma) -- no leading-order")
print("shortcut in this numeric check).")
print("=" * 78)

mp.mp.dps = 80


def c_exact(Kval, nval, gval):
    K_, n_, g_ = Kval, nval, gval
    c0v = g_ * K_ * (2 * g_ ** 2 * K_ ** 2 - 6 * g_ * K_ ** 2 + 3 * g_ * K_
                      + 6 * K_ ** 2 - 6 * K_ + 1) / (12 * n_ ** 2)
    c1v = (g_ ** 2 * K_ ** 2 / 2 - g_ * K_ ** 2 - g_ * K_ * n_ + g_ * K_ / 2
           + K_ ** 2 / 2 + K_ * n_ - K_ / 2 - n_ / 2 + mp.mpf(1) / 12) / n_ ** 2
    c2v = (2 * g_ * K_ - 2 * K_ - 2 * n_ + 1) / (4 * n_ ** 2)
    c3v = mp.mpf(1) / (6 * n_ ** 2)
    return c0v, c1v, c2v, c3v


def x_of_D(Kval, nval, gval, Dval):
    c0v, c1v, c2v, c3v = c_exact(Kval, nval, gval)
    return c0v + c1v * Dval + c2v * Dval ** 2 + c3v * Dval ** 3


results = []
for gval_f in [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    gval = mp.mpf(gval_f)
    betav = gval * (2 - gval) / 2
    for nval_f in [mp.mpf('1e30'), mp.mpf('1e60'), mp.mpf('1e100')]:
        nval = nval_f
        Kval = mp.sqrt(4 * nval * mp.log(nval) / betav)
        Dmin = -gval * Kval
        Dmax = (1 - gval) * Kval
        c0v, c1v, c2v, c3v = c_exact(Kval, nval, gval)
        # small root of 3*c3*D^2 + 2*c2*D + c1 = 0
        disc = (2 * c2v) ** 2 - 4 * (3 * c3v) * c1v
        if disc < 0:
            Dstar_candidates = []
        else:
            sq = mp.sqrt(disc)
            r1 = (-2 * c2v + sq) / (2 * 3 * c3v)
            r2 = (-2 * c2v - sq) / (2 * 3 * c3v)
            Dstar_candidates = [r1, r2]
        # keep only the root(s) inside [Dmin,Dmax]
        inside = [r for r in Dstar_candidates if Dmin <= r <= Dmax]
        x_dmin = x_of_D(Kval, nval, gval, Dmin)
        x_dmax = x_of_D(Kval, nval, gval, Dmax)
        best_endpoint = max(abs(x_dmin), abs(x_dmax))
        interior_vals = [x_of_D(Kval, nval, gval, r) for r in inside]
        best_interior = max([abs(v) for v in interior_vals], default=mp.mpf(0))
        overall_max = max(best_endpoint, best_interior)
        interior_dominates = best_interior > best_endpoint
        results.append((gval_f, nval_f, len(inside), float(best_endpoint),
                         float(best_interior), interior_dominates))
        print(f"gamma={gval_f:<5} n=1e{float(mp.log10(nval_f)):.0f}  "
              f"#interior_crit_in_range={len(inside)}  "
              f"|x|@endpoints={float(best_endpoint):.6e}  "
              f"|x|@interior={float(best_interior):.6e}  "
              f"interior_dominates={interior_dominates}")

print()
n_dom = sum(1 for r in results if r[5])
print(f"Interior critical point strictly dominates the endpoints in "
      f"{n_dom}/{len(results)} tested (gamma,n) combinations.")
