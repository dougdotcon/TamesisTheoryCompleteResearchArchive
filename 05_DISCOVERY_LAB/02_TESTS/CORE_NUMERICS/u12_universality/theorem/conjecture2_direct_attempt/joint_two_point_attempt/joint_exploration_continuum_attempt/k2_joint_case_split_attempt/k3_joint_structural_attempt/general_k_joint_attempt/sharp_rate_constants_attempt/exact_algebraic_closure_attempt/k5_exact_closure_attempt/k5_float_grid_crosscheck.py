"""
Independent, non-sympy (raw floating point) dense-grid cross-check of the
K=5 exact-closure claim: |h5(n,x)| <= M5 for x in [0,1], n in the claimed
domain, checked over a wide range of n (small integers through 10^6) and
a dense x-grid per n. This is a sanity net only -- it does not replace
the exact resultant-elimination proof (k5_step6/step9 scripts), matching
this lineage's established convention (cf. predecessor's
independent_numeric_crosscheck.py).
"""
import numpy as np

M5 = 0.69680319894635521119687666538347900090047728

def bracket_np(n, k):
    return (k**8 - 16*k**7 - 5*k**6*n**2 + 30*k**6*n + 106*k**6 + 45*k**5*n**2
            - 290*k**5*n - 376*k**5 + 10*k**4*n**4 - 100*k**4*n**3 + 100*k**4*n**2
            + 1100*k**4*n + 769*k**4 - 40*k**3*n**4 + 440*k**3*n**3 - 975*k**3*n**2
            - 2074*k**3*n - 904*k**3 - 10*k**2*n**6 + 120*k**2*n**5 - 435*k**2*n**4
            + 10*k**2*n**3 + 1885*k**2*n**2 + 2014*k**2*n + 564*k**2 + 10*k*n**6
            - 140*k*n**5 + 635*k*n**4 - 650*k*n**3 - 1410*k*n**2 - 924*k*n - 144*k
            + 5*n**8 - 60*n**7 + 265*n**6 - 490*n**5 + 190*n**4 + 300*n**3 + 360*n**2
            + 144*n)

def h5_np(n, x):
    k = n * x
    Dn5 = n**6 * (n - 1) * (n - 2) * (n - 3) * (n - 4)
    D5 = k * (k + 1) * bracket_np(n, k) / Dn5
    F5cont = 1 - (1 - x**2)**5
    return n * (D5 - F5cont)

def scan(n_values, npts=4001):
    xs = np.linspace(0.0, 1.0, npts)
    worst_ratio = 0.0
    worst_cell = None
    violations = 0
    for nv in n_values:
        hv = h5_np(float(nv), xs)
        mx = np.max(hv)
        mn = np.min(hv)
        if mx > M5 + 1e-9 or mn < -M5 - 1e-9:
            violations += 1
            print(f"  VIOLATION at n={nv}: max={mx} min={mn}")
        ratio = max(mx / M5, -mn / M5)
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_cell = nv
    return violations, worst_ratio, worst_cell


if __name__ == "__main__":
    print("Domain candidate n>=7: integer sweep n=7..2000")
    n_int = list(range(7, 2001))
    v1, wr1, wc1 = scan(n_int)
    print(f"  violations={v1}  worst ratio |h|/M5={wr1:.6f} at n={wc1}")

    print("Geometric sweep n=2000..10^6 (200 points)")
    n_geo = np.unique(np.round(np.geomspace(2000, 1e6, 200)).astype(int)).tolist()
    v2, wr2, wc2 = scan(n_geo)
    print(f"  violations={v2}  worst ratio |h|/M5={wr2:.6f} at n={wc2}")

    print("Boundary region n=5,6 (below claimed domain, informational only)")
    v3, wr3, wc3 = scan([5, 6])
    print(f"  (below-domain) violations={v3}  worst ratio={wr3:.6f} at n={wc3}")

    total_violations = v1 + v2
    print()
    print(f"TOTAL violations in claimed domain (n>=7): {total_violations}")
    assert total_violations == 0
    print("PASSED: zero violations of |h5(n,x)|<=M5 for all tested n>=7, x in [0,1].")
