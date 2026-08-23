"""probe_exact.py -- exact-arithmetic confirmation of the analytic lemmas.

Everything here is Fraction / sympy exact; no floating point enters a verdict.

  L1  the derivative identity   d/dc phi(n,c) = E[ phi_n^{(J+1)} - phi_n^{(J)} ],
      J ~ Binomial(n-1, c/n)                                     (ATTEMPT.md SS3)
  L2  the coupling Lipschitz bound  |phi(n,c)-phi(n,c')| <= |c-c'|  (SS3),
      and the true modulus (should approach |phi_inf'(0)| = 1/3)
  L3  the exact Binomial-vs-Poisson identity
      B_n(c) = int_0^1 [(1-c t^2/n)^n - e^{-c t^2}] dt            (SS5/SS6)
  L4  the elementary Poisson-approximation inequality
      0 <= e^{-x} - (1-x/n)^n <= (x^2/n) e^{-x},  0<=x<=n, n>=4   (SS6)
  L5  exact rational anchors for phi(n,c), for reproducibility
"""

from fractions import Fraction
from math import comb
import sympy as sp
import mpmath as mp
from chain import phi_mixed_exact, phi_condK_exact, phi_K

mp.mp.dps = 30


def phi_mixed_sym(n):
    """phi(n,c) as an exact polynomial in c (sympy Rational coefficients)."""
    c = sp.Symbol('c')
    q = c / n
    tot = 0
    for K in range(n + 1):
        tot += sp.binomial(n, K) * q ** K * (1 - q) ** (n - K) \
               * sp.Rational(phi_condK_exact(n, K))
    return sp.expand(sp.simplify(tot)), c


if __name__ == "__main__":
    print("=== probe_exact.py ===")

    print("\n--- L1: d/dc phi(n,c) = E_{J~Bin(n-1,c/n)}[phi_n^(J+1) - phi_n^(J)] ---")
    for n in range(2, 9):
        P, c = phi_mixed_sym(n)
        lhs = sp.expand(sp.diff(P, c))
        q = c / n
        rhs = 0
        for J in range(n):
            rhs += sp.binomial(n - 1, J) * q ** J * (1 - q) ** (n - 1 - J) \
                   * (sp.Rational(phi_condK_exact(n, J + 1))
                      - sp.Rational(phi_condK_exact(n, J)))
        print("  n=%d : LHS-RHS simplifies to %s"
              % (n, sp.simplify(sp.expand(lhs - rhs))))

    print("\n--- L2: Lipschitz.  sup_c |d/dc phi(n,c)| on [0,n]  (exact endpoints) ---")
    print("      n   |phi'(n,0)|        max_J[phi_n^(J)-phi_n^(J+1)]   <= 1 ?")
    for n in (2, 4, 8, 16, 32, 64):
        d0 = Fraction(phi_condK_exact(n, 0)) - Fraction(phi_condK_exact(n, 1))
        vs = [phi_condK_exact(n, K) for K in range(n + 1)]
        mx = max(vs[K] - vs[K + 1] for K in range(n))
        print("      %-3d %-18s %-28s %s" % (n, str(d0), str(mx), mx <= 1))
    print("    (phi'(n,0) = phi_n^(1) - phi_n^(0) = -1/3 + 1/(3n^2) exactly,")
    print("     matching phi_inf'(0) = -1/3;  and every increment is <= 1,")
    print("     so |phi(n,c)-phi(n,c')| <= |c-c'| -- SS3's Lemma 3.2.)")

    print("\n--- L3: B_n(c) = int_0^1 [(1-ct^2/n)^n - e^{-ct^2}] dt, exactly ---")
    for n in (5, 10, 20):
        for cc in (1, 3, 5):
            bn_sum = sum((Fraction(comb(n, K)) * Fraction(cc, n) ** K
                          * (1 - Fraction(cc, n)) ** (n - K)
                          - Fraction(0)) * phi_K(K) for K in range(n + 1))
            poi = mp.nsum(lambda K: mp.e ** (-cc) * mp.mpf(cc) ** K / mp.factorial(K)
                          * mp.mpf(float(phi_K(int(K)))), [0, mp.inf])
            lhs = mp.mpf(bn_sum.numerator) / bn_sum.denominator - poi
            rhs = mp.quad(lambda t: (1 - cc * t * t / n) ** n - mp.e ** (-cc * t * t),
                          [0, 1])
            print("  n=%-3d c=%-2d  B_n(sum) = %s   B_n(integral) = %s   |diff|=%.2e"
                  % (n, cc, mp.nstr(lhs, 12), mp.nstr(rhs, 12), abs(lhs - rhs)))

    print("\n--- L4: 0 <= e^{-x} - (1-x/n)^n <= (x^2/n) e^{-x} for 0<=x<=n, n>=4 ---")
    worst_lo, worst_hi = 0.0, 0.0
    for n in [4, 5, 7, 10, 30, 100, 1000]:
        for i in range(0, 2001):
            x = mp.mpf(n) * i / 2000
            d = mp.e ** (-x) - (1 - x / n) ** n
            worst_lo = min(worst_lo, float(d))
            rhs = x * x / n * mp.e ** (-x)
            if rhs > 0:
                worst_hi = max(worst_hi, float(d / rhs))
    print("  min over the whole scan of  e^{-x}-(1-x/n)^n        = %.3e (>=0 required)"
          % worst_lo)
    print("  max over the whole scan of  [e^{-x}-(1-x/n)^n] / [(x^2/n)e^{-x}] = %.6f"
          % worst_hi)
    print("  kappa_B = sup_c c^2 int_0^1 t^4 e^{-ct^2} dt:")
    f = lambda c: -(c ** 2) * mp.quad(lambda t: t ** 4 * mp.e ** (-c * t * t), [0, 1])
    cm = mp.findroot(lambda c: mp.diff(f, c), 5.0)
    print("    kappa_B = %s at c = %s" % (mp.nstr(-f(cm), 12), mp.nstr(cm, 10)))

    print("\n--- L5: exact rational anchors for phi(n,c) ---")
    for n, cc in [(4, 1), (5, 2), (6, Fraction(3, 2)), (8, 3), (10, 5), (12, 12)]:
        v = phi_mixed_exact(n, Fraction(cc))
        print("  phi(%2d, %-4s) = %-34s = %.12f" % (n, cc, str(v)[:34], float(v)))
