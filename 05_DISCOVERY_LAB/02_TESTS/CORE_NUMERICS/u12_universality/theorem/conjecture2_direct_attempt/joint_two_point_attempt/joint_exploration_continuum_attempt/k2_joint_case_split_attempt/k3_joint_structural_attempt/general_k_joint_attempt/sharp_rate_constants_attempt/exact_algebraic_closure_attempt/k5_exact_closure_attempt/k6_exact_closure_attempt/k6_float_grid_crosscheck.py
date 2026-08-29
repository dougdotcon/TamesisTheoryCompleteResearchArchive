"""
K6-EXACT-CLOSURE-ATTEMPT. Independent, non-sympy, raw double-precision
floating-point dense-grid stress test of the claimed exact theorem:

    |h6(n,x)| <= M6   for every integer n>=8, every x in [0,1]

h6(n,x) := n*(F_n^{(6)}(n*x/n) - F_6(x)) = n*Delta_6(x), computed here
DIRECTLY from Proposicao D6's own closed form (transcribed by hand,
independently, from k6_exact_closure.log's own printed Bracket6/Dn6),
substituting k=n*x -- NOT via sp.Poly/N(n,x)/Num6 machinery, a
genuinely different code path (raw Python floats, no symbolic algebra
at all) from every other script in this front.

As a negative control (matching this lineage's own convention -- the
K=5 predecessor's float-grid script did the identical thing), n=6,7
(below the claimed domain n>=8) are ALSO scanned and are expected to
show genuine violations -- confirming the domain boundary is exactly
where the exact theorem says it is, not merely "somewhere safely
inside" a looser bound.
"""
import math

M6 = 0.67967830129138512967160338683005533


def D6_bracket(n, k):
    return (
        -k**10 + 25*k**9 + 6*k**8*n**2 - 45*k**8*n - 270*k**8
        - 96*k**7*n**2 + 760*k**7*n + 1650*k**7
        - 15*k**6*n**4 + 195*k**6*n**3 - 9*k**6*n**2 - 5380*k**6*n - 6273*k**6
        + 135*k**5*n**4 - 1875*k**5*n**3 + 4359*k**5*n**2 + 20734*k**5*n + 15345*k**5
        + 20*k**4*n**6 - 330*k**4*n**5 + 1375*k**4*n**4 + 3600*k**4*n**3
        - 22441*k**4*n**2 - 47215*k**4*n - 24080*k**4
        - 80*k**3*n**6 + 1440*k**3*n**5 - 7975*k**3*n**4 + 4641*k**3*n**3
        + 50821*k**3*n**2 + 64330*k**3*n + 23300*k**3
        - 15*k**2*n**8 + 270*k**2*n**7 - 1730*k**2*n**6 + 3435*k**2*n**5
        + 7610*k**2*n**4 - 20391*k**2*n**3 - 58916*k**2*n**2 - 50320*k**2*n - 12576*k**2
        + 15*k*n**8 - 310*k*n**7 + 2360*k*n**6 - 7055*k*n**5 + 730*k*n**4
        + 20526*k*n**3 + 33716*k*n**2 + 20016*k*n + 2880*k
        + 6*n**10 - 105*n**9 + 720*n**8 - 2375*n**7 + 3384*n**6 - 10*n**5
        - 1860*n**4 - 6696*n**3 - 7440*n**2 - 2880*n
    )


def D6(n, k):
    den = n ** 7.0 * (n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)
    return k * (k + 1) * D6_bracket(n, k) / den


def F6_cont(x):
    return 1.0 - (1.0 - x * x) ** 6


def h6(n, x):
    k = n * x
    return n * (D6(n, k) - F6_cont(x))


def scan_n(n, n_x=4001):
    worst_over = -1e300
    worst_x = None
    for i in range(n_x):
        x = i / (n_x - 1)
        v = h6(n, x)
        if v - M6 > worst_over:
            worst_over = v - M6
            worst_x = x
        if -v - M6 > worst_over:
            worst_over = -v - M6
            worst_x = x
    return worst_over, worst_x


if __name__ == "__main__":
    print("=" * 74)
    print("Negative control: n=6,7 (BELOW claimed domain n>=8) -- expect")
    print("genuine violations of |h6(n,x)|<=M6:")
    print("=" * 74)
    for n in [6, 7]:
        worst, xw = scan_n(n)
        status = "VIOLATION (expected)" if worst > 1e-9 else "no violation (unexpected!)"
        print(f"  n={n}: max(|h6|-M6) over grid = {worst:.6f} at x={xw:.4f}   {status}")
        if n == 7:
            print(f"    h6({n},1) = {h6(n,1.0):.6f}   -M6 = {-M6:.6f}   "
                  f"(should violate: h6(7,1) < -M6)")

    print()
    print("=" * 74)
    print("Claimed domain: integer sweep n=8..2000, geometric sweep")
    print("n=2000..10^6 (200 points), 4001-point x-grid per n. Expect")
    print("ZERO violations anywhere.")
    print("=" * 74)
    max_over_all = -1e300
    worst_n = None
    worst_x_all = None
    violations = 0
    for n in range(8, 2001):
        worst, xw = scan_n(n, n_x=801 if n > 100 else 4001)
        if worst > 1e-9:
            violations += 1
            print(f"  VIOLATION at n={n}: max(|h6|-M6)={worst:.8f} at x={xw:.4f}")
        if worst > max_over_all:
            max_over_all = worst
            worst_n = n
            worst_x_all = xw

    geo_ns = []
    r = 2000.0
    for i in range(200):
        geo_ns.append(int(round(r)))
        r *= (1_000_000 / 2000.0) ** (1 / 199)
    geo_ns = sorted(set(n for n in geo_ns if n >= 2000))
    for n in geo_ns:
        worst, xw = scan_n(n, n_x=401)
        if worst > 1e-9:
            violations += 1
            print(f"  VIOLATION at n={n}: max(|h6|-M6)={worst:.8f} at x={xw:.4f}")
        if worst > max_over_all:
            max_over_all = worst
            worst_n = n
            worst_x_all = xw

    print()
    print(f"Total violations in claimed domain (n>=8): {violations}")
    print(f"Closest approach to the bound: max(|h6|-M6) = {max_over_all:.10f} "
          f"at n={worst_n}, x={worst_x_all:.4f}")
    print(f"(negative means the bound holds strictly at this point; should")
    print(f"approach 0 from below as n->infinity, since g6(x6*)=M6 exactly)")
    assert violations == 0, f"{violations} violations found in the claimed domain!"
    print("\nZERO violations confirmed across the full claimed domain. PASSED.")

    # ratio check at n=10^6, x near x6*
    n_big = 1_000_000
    x6star = 0.26036172400671492484172362842265674
    v = h6(n_big, x6star)
    print(f"\nh6({n_big}, x6*) = {v:.10f}   M6 = {M6:.10f}   ratio = {v/M6:.8f}")
    print("(should approach 1 from below as n->infinity)")
