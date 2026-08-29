"""
Attempt to find a K-free (indeed r-only-depending) closed form for the
combinatorial weight W(r,t), defined so that

    E[(M_K')^t] = K! * sum_{r=0}^{K} C(K,r) * W(r,t) / (K+t+r+1)!

(a restructuring of the exact computation in verify_MK_moments.py, using
that both Proposition S applied to a size-r subset A and the r-fold
uniform-sum moment, combined, always produce monomials of total degree
exactly t+r+1, so the Dirichlet-moment denominator is always (K+t+r+1)!).

If W(r,t) turns out to have a simple closed form in r (for fixed t), the
sum over r may become sympy-summable in closed form for symbolic K, turning
the (so far only numerically/exactly verified for K<=7) claim
M_K' =_d M_K into an actual K-free proof.
"""
import itertools
import math
from fractions import Fraction as Fr

import sympy as sp

import sys
sys.path.insert(0, '.')
from verify_MK_moments import prop_S_monomials, conditional_moment_monomials, multiply_monomials, dirichlet_monomial_moment, E_MKprime_power, target_moment


def W(r, t):
    A = tuple(range(r))
    propS = prop_S_monomials(r, A)
    cond = conditional_moment_monomials(r, A, t)
    prod = multiply_monomials(propS, cond, r)
    total = Fr(0)
    for exps, coeff in prod.items():
        assert sum(exps) == t + r + 1, (exps, t, r)
        fact_prod = 1
        for e in exps:
            fact_prod *= math.factorial(e)
        total += coeff * fact_prod
    return total


def E_via_W(K, t, Wcache):
    total = Fr(0)
    for r in range(0, K + 1):
        c = math.comb(K, r)
        w = Wcache.get((r, t))
        if w is None:
            w = W(r, t)
            Wcache[(r, t)] = w
        total += c * w / math.factorial(K + t + r + 1)
    return total * math.factorial(K)


if __name__ == "__main__":
    Wcache = {}
    print("Cross-check: E_via_W(K,t) vs E_MKprime_power(K,t) (both exact routes)")
    ok_all = True
    for K in range(1, 6):
        for t in range(1, 4):
            a = E_via_W(K, t, Wcache)
            b = E_MKprime_power(K, t)
            ok = (a == b)
            ok_all = ok_all and ok
            print(f"K={K} t={t}: via_W={a} direct={b} {'OK' if ok else 'MISMATCH'}")
    print("ALL OK" if ok_all else "MISMATCH FOUND")
    print()

    print("W(r,t) table:")
    for t in range(1, 5):
        row = [W(r, t) for r in range(0, 8)]
        print(f"t={t}: {row}")

    print()
    print("Trying to recognize W(r,1) and W(r,2) as closed forms in r via sympy rational_interpolate / ratsimp of ratios")
    r_sym = sp.symbols('r', nonnegative=True, integer=True)
    for t in range(1, 4):
        vals = [W(r, t) for r in range(0, 9)]
        print(f"t={t} raw values: {vals}")
        # look at ratio W(r,t) / r!  and W(r,t)*something obvious
        ratios_factorial = [sp.nsimplify(vals[r]) / sp.factorial(r) for r in range(len(vals))]
        print(f"  W(r,t)/r! = {ratios_factorial}")
        ratios_next = [ (sp.nsimplify(vals[r+1])/sp.nsimplify(vals[r]) if vals[r] != 0 else None) for r in range(len(vals)-1)]
        print(f"  W(r+1,t)/W(r,t) = {ratios_next}")
