"""
ADVERSARIAL SCRIPT 3(d) -- extract gosper_sum for K=3 (own single-fraction
term, independently re-derived and verified in script3 investigation) and
check it numerically against a from-scratch brute truncated V-sum, at
concrete (n,O,r,t) configurations INDEPENDENT of the front's own reported
numbers.
"""
import sympy as sp
from sympy.concrete.gosper import gosper_sum
from math import comb
import time

V, r, n, K, O, t = sp.symbols('V r n K O t')


def safe_comb(a, b):
    if a < 0 or b < 0 or b > a:
        return 0
    return comb(a, b)


def InnerJ_closed(nv, Kv, rv, Vv, Ov):
    Nv = nv - Vv - Ov
    if rv == Kv:
        return nv * safe_comb(Nv + rv - 1, rv - 1)
    return (Ov + Vv) * safe_comb(Nv + rv - 1, Kv - 1) + rv * safe_comb(Nv + rv - 1, Kv)


def brute_Vsum(nv, Kv, rv, Ov, tv):
    """sum_{V=r}^{t} C(V-1,r-1)*InnerJ(V,O), direct."""
    total = 0
    for Vv in range(rv, tv + 1):
        cV = safe_comb(Vv - 1, rv - 1) if rv >= 1 else (1 if Vv == 0 else 0)
        total += cV * InnerJ_closed(nv, Kv, rv, Vv, Ov)
    return total


if __name__ == "__main__":
    Kv_fixed = 3
    coeff = K*O + K*V - K*r - O*r - V*r + n*r + r**2
    single_frac = sp.binomial(V-1, r-1) * coeff * sp.factorial(n-O-V+r-1) / (sp.factorial(K)*sp.factorial(n-K-O-V+r))
    term_K3 = single_frac.subs(K, Kv_fixed)

    print("Extracting gosper_sum for K=3 (own re-derived term)...")
    t0 = time.time()
    closed = gosper_sum(term_K3, (V, r, t))
    print(f"gosper_sum done in {time.time()-t0:.2f}s")
    print("closed form (indefinite sum V=r..t):")
    sp.pprint(closed)

    print()
    print("=" * 70)
    print("Numeric verification against brute truncated V-sum, K=3,")
    print("concrete (n,O,r,t) configs chosen independently by the referee")
    print("=" * 70)
    configs = [
        (14, 2, 1, 6),
        (14, 2, 2, 7),
        (20, 3, 2, 9),
        (11, 0, 1, 5),
        (16, 1, 3, 8),
    ]
    all_ok = True
    for (nv, Ov, rv, tv) in configs:
        brute = brute_Vsum(nv, Kv_fixed, rv, Ov, tv)
        via_closed = closed.subs({n: nv, O: Ov, r: rv, t: tv})
        via_closed = sp.nsimplify(sp.simplify(via_closed))
        ok = (sp.Integer(brute) == via_closed)
        all_ok &= ok
        print(f"n={nv} O={Ov} r={rv} t={tv}: brute={brute}  closed-form={via_closed}  match={ok}")
    print("ALL MATCH:", all_ok)
