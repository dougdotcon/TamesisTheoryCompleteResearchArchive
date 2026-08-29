"""
Independent numeric cross-check of k3_exact_closure.py / k4_exact_closure.py.

Deliberately a SEPARATE code path from those two scripts: raw floating
point (no sympy), direct evaluation of the D3/D4 closed-form CDFs cited
in sharp_rate_constants_attempt/ATTEMPT.md Sec.1 (THEOREM.md Estagios
40/43), NOT via any shared helper. This script does not feed anything
into the proved theorems -- it is a sanity net only, per this archive's
established tradition (see e.g. sharp_rate_constants_attempt's own
monte_carlo_bonus.py).

No randomness is used (a dense deterministic grid is used instead) --
this front's mandate anticipated needing none, matching every prior
front in this exact style; confirmed true in practice.
"""
import numpy as np
import time

M3 = 0.712071558138027808419103234207
M4 = 0.708718393409321614178660709132


def h3(n, x):
    k = n * x
    bracket = (k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2
               + (3*n**2 - 11*n - 2)*k
               + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
    F3n = k*(k+1)*bracket / (n**4*(n-1)*(n-2))
    F3c = 1 - (1 - x**2)**3
    return n*(F3n - F3c)


def h4(n, x):
    k = n * x
    Q = (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4 + (-16*n**2 + 80*n + 51)*k**3
         + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
         + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
         + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)
    F4n = k*(k+1)*Q / (n**5*(n-1)*(n-2)*(n-3))
    F4c = 1 - (1 - x**2)**4
    return n*(F4n - F4c)


def grid_check(hfunc, M, n_domain_start, n_grid_start, label):
    """n_domain_start: the PROVED theorem's own domain (n>=5 for K=3,
    n>=6 for K=4) -- only violations at n >= n_domain_start count as a
    real problem. n_grid_start < n_domain_start is included in the scan
    (and reported) purely to show the boundary artifact growing outside
    the claimed domain, exactly as expected -- not a violation of
    anything actually proved."""
    worst_hi, worst_hi_pt = -1e18, None
    worst_lo, worst_lo_pt = 1e18, None
    worst_hi_indomain, worst_hi_indomain_pt = -1e18, None
    worst_lo_indomain, worst_lo_indomain_pt = 1e18, None
    n_ranges = [np.linspace(n_grid_start, 6, 400),
                np.linspace(6, 50, 2000),
                np.linspace(50, 1000, 3000),
                np.geomspace(1000, 1e7, 3000)]
    xs = np.linspace(0, 1, 4001)
    t0 = time.time()
    for nr in n_ranges:
        for nv in nr:
            if nv <= 3:
                continue
            vals = hfunc(nv, xs)
            mx, mn = vals.max(), vals.min()
            if mx > worst_hi:
                worst_hi, worst_hi_pt = mx, (nv, xs[np.argmax(vals)])
            if mn < worst_lo:
                worst_lo, worst_lo_pt = mn, (nv, xs[np.argmin(vals)])
            if nv >= n_domain_start:
                if mx > worst_hi_indomain:
                    worst_hi_indomain, worst_hi_indomain_pt = mx, (nv, xs[np.argmax(vals)])
                if mn < worst_lo_indomain:
                    worst_lo_indomain, worst_lo_indomain_pt = mn, (nv, xs[np.argmin(vals)])
    elapsed = time.time() - t0
    print(f"--- {label} --- (elapsed {elapsed:.1f}s)")
    print(f"  [whole scanned range, n>={n_grid_start}, INCLUDING n below the proved domain]")
    print(f"    max h found: {worst_hi:.10f} at {worst_hi_pt}   M={M:.10f}")
    print(f"    min h found: {worst_lo:.10f} at {worst_lo_pt}   -M={-M:.10f}"
          f"   (below-domain excursions here are EXPECTED, not a bug)")
    print(f"  [restricted to the PROVED domain n>={n_domain_start}]")
    print(f"    max h found: {worst_hi_indomain:.10f}   M={M:.10f}"
          f"   [{'OK' if worst_hi_indomain < M else 'VIOLATION'}]")
    print(f"    min h found: {worst_lo_indomain:.10f}   -M={-M:.10f}"
          f"   [{'OK' if worst_lo_indomain > -M else 'VIOLATION'}]")
    return worst_hi_indomain < M and worst_lo_indomain > -M


ok3 = grid_check(h3, M3, 5, 4.5, "K=3 dense float grid, n in [4.5, 1e7], proved domain n>=5")
ok4 = grid_check(h4, M4, 6, 4.2, "K=4 dense float grid, n in [4.2, 1e7], proved domain n>=6")

print()
print("--- K=4 exact-per-n spot table (confirms min always at x=1 boundary) ---")
for nv in [6, 7, 8, 10, 15, 20, 50, 100, 500, 999]:
    xs = np.linspace(0, 1, 200001)
    vals = h4(nv, xs)
    mx, mn = vals.max(), vals.min()
    xmin = xs[np.argmin(vals)]
    print(f"  n={nv:5d}  max={mx:.8f}  min={mn:.8f} at x={xmin:.5f}"
          f"  (boundary h(n,1)={h4(nv,1.0):.8f})")

print()
print("SUMMARY:", "ALL CHECKS PASSED, zero violations" if (ok3 and ok4) else "VIOLATION FOUND")
