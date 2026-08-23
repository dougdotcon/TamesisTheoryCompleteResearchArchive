"""ecoef.py -- the predicted 1/n coefficient e(c) of phi(n,c) - phi_infty(c).

Derived in ATTEMPT.md SS5:

    e(c) = 1/4 [ c (I_0(c) - I_1(c)) + 2 I_0(c) - 2 ]  -  (c^2/2) I_2(c),
    I_k(c) = int_0^1 t^{2k} e^{-c t^2} dt.

The two pieces are, respectively,
    E_{Poi(c)}[c_K]                       (the fixed-K rate coefficient, Estagio 7)
  - (c^2/2) E_{Poi(c)}[Delta^2 phi_K]     (the Binomial-vs-Poisson 1/n mismatch)
with c_K = [(K+2)phi_K - 2]/4  and  Delta^2 phi_K = phi_{K+2}-2phi_{K+1}+phi_K.
"""

import mpmath as mp

mp.mp.dps = 40


def I(k, c):
    c = mp.mpf(c)
    return mp.quad(lambda t: t ** (2 * k) * mp.e ** (-c * t * t), [0, 1])


def phi_inf(c):
    c = mp.mpf(c)
    if c == 0:
        return mp.mpf(1)
    return mp.sqrt(mp.pi) / 2 / mp.sqrt(c) * mp.erf(mp.sqrt(c))


def e_of_c(c):
    c = mp.mpf(c)
    I0, I1, I2 = phi_inf(c), I(1, c), I(2, c)
    return (c * (I0 - I1) + 2 * I0 - 2) / 4 - c * c / 2 * I2


def e_part_A(c):
    """E_{Poi(c)}[c_K] alone (the fixed-K rate part)."""
    c = mp.mpf(c)
    return (c * (phi_inf(c) - I(1, c)) + 2 * phi_inf(c) - 2) / 4


def e_part_B(c):
    """-(c^2/2) E[Delta^2 phi_K]: the Binomial->Poisson mismatch part."""
    c = mp.mpf(c)
    return -c * c / 2 * I(2, c)


if __name__ == "__main__":
    print("=== ecoef.py : e(c) and its two parts ===")
    print("  c        e(c)            E[c_K]          binom-mismatch   sqrt(pi c)/8-1/2")
    for c in [0.25, 0.5, 1, 2, 3, 5, 8, 10, 20, 50, 100, 400, 1600, 10 ** 4, 10 ** 6]:
        print("  %-8s %+.10f  %+.10f  %+.10f   %+.6f"
              % (c, e_of_c(c), e_part_A(c), e_part_B(c),
                 mp.sqrt(mp.pi * c) / 8 - mp.mpf(1) / 2))
    print()
    # small-c expansion:  e(c) = -c^2/12 + O(c^3)?  Also get the c^3 coefficient.
    print("  small-c check:  e(c)/c^2 -> -1/12 = %.10f" % (-1.0 / 12))
    for c in [mp.mpf(1) / 2 ** k for k in range(2, 12)]:
        print("    c=%-14s e(c)/c^2 = %+.12f" % (mp.nstr(c, 6), e_of_c(c) / c / c))
    print()
    # exact rational small-c Taylor coefficients of e(c), via series of I_k
    import sympy as sp
    cs = sp.symbols('c', positive=True)
    N = 8
    def Iser(k):
        return sum((-cs) ** j / (sp.factorial(j) * (2 * j + 2 * k + 1)) for j in range(N))
    eser = sp.expand(sp.series(
        (cs * (Iser(0) - Iser(1)) + 2 * Iser(0) - 2) / 4 - cs ** 2 / 2 * Iser(2),
        cs, 0, N).removeO())
    print("  exact Taylor of e(c) (sympy):")
    p = sp.Poly(eser, cs)
    for j in range(0, N):
        print("    [c^%d] e = %s" % (j, sp.nsimplify(p.coeff_monomial(cs ** j))))
    # zero crossing
    print()
    lo, hi = mp.mpf(1), mp.mpf(200)
    root = mp.findroot(e_of_c, [lo, hi], solver='bisect')
    print("  e(c) = 0 at c = %s  (e<0 below, e>0 above)" % mp.nstr(root, 12))
    print("  min of e(c):")
    cm = mp.findroot(lambda c: mp.diff(e_of_c, c), 2.0)
    print("    argmin c* = %s,  e(c*) = %s" % (mp.nstr(cm, 10), mp.nstr(e_of_c(cm), 10)))
