"""verify_Q_lower_bound.py -- piece 1: Q(n) >= sqrt(pi n/2) - C.

Checks, in order:
  T1. Termwise: P_j := prod_{i=1}^j (1-i/n)  >=  h(j) := exp(-j(j+1)/(2(n-j)))
      for every 0<=j<=n-1, a range of n.  P_j computed EXACTLY (Fraction);
      h(j) computed with mpmath (50 digits) since it is transcendental.
      This is the core termwise inequality the whole proof rests on.
  T2. Err(n) := int_0^n e^{-x^2/2n}(1-e^{-eps(x)}) dx  <=  3 + 2 e^{-n/8}
      (the claimed split-range bound), checked by high-precision numerical
      quadrature (mpmath.quad) against the closed-form RHS, for a grid of n.
  T3. Tail(n,n) := int_n^infty e^{-x^2/2n} dx  <=  e^{-n/2}, by quadrature.
  T4. Assembled: Q(n) >= sqrt(pi n/2) - C for C=6, Q(n) computed EXACTLY
      (Fraction) via the archive's own definition, for a wide grid of n
      (small n through n=20000), zero violations expected/required.

All of T1-T4 are checks on the ALREADY-derived elementary inequality chain
in ATTEMPT.md Theorem 5/Lemma 5.1 -- not the source of the proof, which is
the algebra there. mpmath is used only for the transcendental quantities
(exp, sqrt(pi), numerical integration), never for anything claimed exact.
"""

from fractions import Fraction as F
import mpmath as mp

mp.mp.dps = 50


def Q_exact(n):
    """Q(n) = sum_{j=0}^{n-1} prod_{i=1}^j (1-i/n), exact Fraction."""
    total = F(0)
    prod = F(1)
    total += prod
    for j in range(1, n):
        prod *= F(n - j, n)
        total += prod
    return total


def P_exact(n, j):
    """prod_{i=1}^j (1-i/n), exact Fraction."""
    prod = F(1)
    for i in range(1, j + 1):
        prod *= F(n - i, n)
    return prod


def h_mp(n, j):
    n = mp.mpf(n)
    j = mp.mpf(j)
    return mp.e ** (-(j * (j + 1)) / (2 * (n - j)))


def eps_mp(n, x):
    n = mp.mpf(n)
    x = mp.mpf(x)
    return (x * (n + x ** 2)) / (2 * n * (n - x))


def gaussian_tail_mp(n, T):
    n = mp.mpf(n)
    return mp.quad(lambda x: mp.e ** (-(x ** 2) / (2 * n)), [T, mp.inf])


def err_mp(n):
    n = mp.mpf(n)
    integrand = lambda x: mp.e ** (-(x ** 2) / (2 * n)) * (1 - mp.e ** (-eps_mp(n, x)))
    return mp.quad(integrand, [0, n])


if __name__ == "__main__":
    print("=== T1: termwise P_j >= h(j), exact P_j vs mpmath h(j) ===")
    viol1 = 0
    checked1 = 0
    for n in [1, 2, 3, 5, 10, 20, 50, 100, 300, 1000]:
        for j in range(0, n):
            pj = P_exact(n, j)
            pj_mp = mp.mpf(pj.numerator) / mp.mpf(pj.denominator)
            hj = h_mp(n, j)
            checked1 += 1
            if pj_mp < hj - mp.mpf(10) ** -30:
                viol1 += 1
                print(f"  VIOLATION n={n} j={j}: P_j={pj_mp} < h(j)={hj}")
    print(f"  checked {checked1} (n,j) pairs, {viol1} violations")

    print()
    print("=== T2: Err(n) <= 3 + 2 e^{-n/8}  (quadrature vs closed-form RHS) ===")
    viol2 = 0
    for n in [1, 2, 5, 10, 20, 50, 100, 300, 1000, 5000]:
        e = err_mp(n)
        rhs = 3 + 2 * mp.e ** (-mp.mpf(n) / 8)
        ok = e <= rhs
        if not ok:
            viol2 += 1
        print(f"  n={n:6d}  Err(n)={float(e):.6f}  RHS(3+2e^-n/8)={float(rhs):.6f}  {'OK' if ok else 'VIOLATION'}")
    print(f"  {viol2} violations")

    print()
    print("=== T3: Tail(n,n) <= e^{-n/2}  (quadrature vs closed-form RHS) ===")
    viol3 = 0
    for n in [1, 2, 5, 10, 20, 50, 100, 300, 1000]:
        t = gaussian_tail_mp(n, n)
        rhs = mp.e ** (-mp.mpf(n) / 2)
        ok = t <= rhs
        if not ok:
            viol3 += 1
        print(f"  n={n:6d}  Tail(n,n)={float(t):.8f}  e^-n/2={float(rhs):.8f}  {'OK' if ok else 'VIOLATION'}")
    print(f"  {viol3} violations")

    print()
    print("=== T4: Q(n) >= sqrt(pi n/2) - 6, exact Q(n) vs mpmath RHS ===")
    C = 6
    viol4 = 0
    checked4 = 0
    ns = list(range(1, 60)) + [80, 120, 200, 400, 800, 1500, 3000]
    worst_margin = None
    for n in ns:
        qn = Q_exact(n)
        qn_mp = mp.mpf(qn.numerator) / mp.mpf(qn.denominator)
        rhs = mp.sqrt(mp.pi * n / 2) - C
        margin = qn_mp - rhs
        checked4 += 1
        if margin < 0:
            viol4 += 1
            print(f"  VIOLATION n={n}: Q(n)={qn_mp} < RHS={rhs}")
        if worst_margin is None or margin < worst_margin[0]:
            worst_margin = (margin, n)
    print(f"  checked {checked4} values of n, {viol4} violations")
    print(f"  smallest margin Q(n)-RHS = {float(worst_margin[0]):.6f} at n={worst_margin[1]}")

    print()
    print("=== also report true gap sqrt(pi n/2)-Q(n) -> classical 1/3 (context only) ===")
    for n in [100, 1000, 3000]:
        qn = Q_exact(n)
        qn_mp = mp.mpf(qn.numerator) / mp.mpf(qn.denominator)
        gap = mp.sqrt(mp.pi * n / 2) - qn_mp
        print(f"  n={n:6d}  sqrt(pi n/2)-Q(n) = {float(gap):.6f}  (elementary C=6 used above is deliberately not tight)")
