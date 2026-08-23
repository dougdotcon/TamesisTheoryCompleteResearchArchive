"""probe_taylor.py -- the 1/n coefficient e_j of the j-th c-Taylor coefficient.

ATTEMPT.md SS5 derives e(c) analytically as

    e(c) = E_{Poi(c)}[c_K] - (c^2/2) E_{Poi(c)}[Delta^2 phi_K]
         = 1/4 [ c(I_0-I_1) + 2 I_0 - 2 ] - (c^2/2) I_2.

SS5.4 derives, completely independently and by finite exact algebra (no
interchange of limits, no analyticity), the coefficient-wise statement

    n ( [c^j] phi(n,.) - [c^j] phi_inf ) -> e_j
    e_j = (-1)^j / j! * [ sum_K (-1)^K C(j,K) c_K  -  C(j,2) sum_K (-1)^K C(j,K) phi_K ]

with the sums finite (K = 0..j) and c_K = [(K+2)phi_K - 2]/4 (Estagio 7).
This script checks that these two routes give the SAME numbers, exactly, and
that finite-n exact Taylor coefficients converge to them.
"""

from fractions import Fraction
from math import comb
import sympy as sp
from chain import phi_condK_exact, phi_K


def cK(K):
    return (Fraction(K + 2) * phi_K(K) - 2) / 4


def e_j_algebraic(j):
    """Exact e_j from the finite-difference formula (SS5.4)."""
    s1 = sum(Fraction((-1) ** K * comb(j, K)) * cK(K) for K in range(j + 1))
    s2 = sum(Fraction((-1) ** K * comb(j, K)) * phi_K(K) for K in range(j + 1))
    return Fraction((-1) ** j, 1) * (s1 - comb(j, 2) * s2) / Fraction(sp.factorial(j))


def e_j_analytic(J):
    """Exact Taylor coefficients of e(c) from the integral formula (SS5)."""
    c = sp.symbols('c')
    N = J + 3
    def Iser(k):
        return sum((-c) ** m / (sp.factorial(m) * (2 * m + 2 * k + 1)) for m in range(N))
    e = sp.expand((c * (Iser(0) - Iser(1)) + 2 * Iser(0) - 2) / 4 - c ** 2 / 2 * Iser(2))
    p = sp.Poly(e, c)
    return [sp.nsimplify(p.coeff_monomial(c ** j)) for j in range(J + 1)]


def taylor_phi_n(n, j):
    """[c^j] phi(n,c), exact:  (-1)^j n^{-j} C(n,j) sum_K (-1)^K C(j,K) phi_n^{(K)}."""
    s = sum(Fraction((-1) ** K * comb(j, K)) * phi_condK_exact(n, K)
            for K in range(j + 1))
    return Fraction((-1) ** j) * Fraction(comb(n, j), n ** j) * s


def taylor_phi_inf(j):
    return Fraction((-1) ** j, sp.factorial(j) * (2 * j + 1))


if __name__ == "__main__":
    print("=== probe_taylor.py ===")
    J = 8
    ana = e_j_analytic(J)
    print("\n--- e_j: integral route  vs  finite-difference route (both exact) ---")
    print("    j     [c^j] e(c) (integral)     e_j (finite difference)    equal?")
    for j in range(J + 1):
        a = Fraction(sp.Rational(ana[j]).p, sp.Rational(ana[j]).q)
        b = e_j_algebraic(j)
        print("   %3d     %-24s  %-24s  %s" % (j, str(a), str(b), a == b))

    print("\n--- finite-n check: n([c^j]phi(n,.) - [c^j]phi_inf) -> e_j (exact) ---")
    for j in (2, 3, 4, 5):
        tinf = taylor_phi_inf(j)
        print("   j=%d  (e_j = %s = %.10f)" % (j, e_j_algebraic(j), float(e_j_algebraic(j))))
        for n in (20, 40, 80, 160, 320, 640):
            v = taylor_phi_n(n, j)
            print("        n=%-5d n*([c^j]phi_n - [c^j]phi_inf) = %+.10f"
                  % (n, float(n * (v - tinf))))
