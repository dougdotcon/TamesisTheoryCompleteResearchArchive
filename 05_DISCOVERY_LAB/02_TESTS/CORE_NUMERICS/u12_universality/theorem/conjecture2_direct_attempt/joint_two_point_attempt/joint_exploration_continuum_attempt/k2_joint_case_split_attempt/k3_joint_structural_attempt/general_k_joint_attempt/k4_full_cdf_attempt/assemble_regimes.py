"""
K4-FULL-CDF-ATTEMPT: assembles the four regime-specific closed forms of
Proposicao D4 by summing Contribution(O) (built from the S1/PS/TS/QS
building blocks of symbolic_derivation_full_cdf.py) over the composition
simplex.  See that file's module docstring for the full derivation
strategy and the precise statement of the four regimes.
"""
import sympy as sp
import pickle
import time

n, k, O, m, t = sp.symbols('n k O m t')

with open('building_blocks.pkl', 'rb') as f:
    B = pickle.load(f)

S1_generic, S1_sat = B['S1_generic'], B['S1_sat']
PS_generic, PS_sat = B['PS_generic'], B['PS_sat']
TS_generic, TS_sat = B['TS_generic'], B['TS_sat']
QS_generic = B['QS_generic']


def binom(x, r_):
    if r_ == 0:
        return sp.Integer(1)
    num = sp.Integer(1)
    for i in range(r_):
        num *= (x - i)
    return num / sp.factorial(r_)


CnK = n * (n - 1) * (n - 2) * (n - 3) / 24  # C(n,4)


def contribution(S1_expr, PS_expr, TS_expr, QS_expr, include_O_indicator=False):
    """Contribution(O) with the four building-block expressions (already
    in terms of t,m,O) substituted t=k-O, m=n-O.  Returns expression in
    O, n, k."""
    empty = binom(m - 1, 3) * (O / n)
    total = (empty
             + sp.Rational(4, 1) / n**2 * S1_expr
             + sp.Rational(12, 1) / n**3 * PS_expr
             + sp.Rational(24, 1) / n**4 * TS_expr
             + sp.Rational(24, 1) / n**4 * QS_expr)
    total = total.subs({t: k - O, m: n - O})
    return sp.expand(total)


def derive_regime_generic():
    """Regime (i): 0<=k<=n-4.  O ranges 0..k.  All patterns genuinely
    truncated for every O in range."""
    cont = contribution(S1_generic, PS_generic, TS_generic, QS_generic)
    total = sp.summation(cont, (O, 0, k))
    total = sp.expand(total)
    F = sp.cancel(total / CnK)
    return F


def derive_regime_boundary(k_value, S1_expr, PS_expr, TS_expr, QS_expr):
    """Regimes (ii)/(iii)/(iv): O ranges 0..n-4 (full range), k fixed to
    k_value (n-3, n-2, or n-1); the appropriate saturated/generic mix of
    building blocks is passed in by the caller."""
    cont = contribution(S1_expr, PS_expr, TS_expr, QS_expr)
    cont = cont.subs(k, k_value)
    total = sp.summation(cont, (O, 0, n - 4))
    total = sp.expand(total)
    F = sp.cancel(total / CnK.subs(k, k_value))
    F = F.subs(k, k_value)  # CnK has no k anyway, but be safe
    return sp.simplify(F)


if __name__ == "__main__":
    t0 = time.time()
    print("=" * 78)
    print("REGIME (i): 0 <= k <= n-4")
    print("=" * 78)
    F_generic = derive_regime_generic()
    print(f"  derived in {time.time()-t0:.1f}s")
    print("F_generic(n,k) =", F_generic)
    with open('F_generic.pkl', 'wb') as f:
        pickle.dump(F_generic, f)

    t1 = time.time()
    print()
    print("=" * 78)
    print("REGIME (ii): k = n-3")
    print("=" * 78)
    # S1 saturated; PS,TS,QS at t=m-3, still generic
    S1e = S1_sat
    PSe = PS_generic.subs(t, m - 3)
    TSe = TS_generic.subs(t, m - 3)
    QSe = QS_generic.subs(t, m - 3)
    F_ii = derive_regime_boundary(n - 3, S1e, PSe, TSe, QSe)
    print(f"  derived in {time.time()-t1:.1f}s")
    print("F(n-3) =", F_ii)
    with open('F_ii.pkl', 'wb') as f:
        pickle.dump(F_ii, f)

    t2 = time.time()
    print()
    print("=" * 78)
    print("REGIME (iii): k = n-2")
    print("=" * 78)
    S1e = S1_sat
    PSe = PS_sat
    TSe = TS_generic.subs(t, m - 2)
    QSe = QS_generic.subs(t, m - 2)
    F_iii = derive_regime_boundary(n - 2, S1e, PSe, TSe, QSe)
    print(f"  derived in {time.time()-t2:.1f}s")
    print("F(n-2) =", F_iii)
    with open('F_iii.pkl', 'wb') as f:
        pickle.dump(F_iii, f)

    t3 = time.time()
    print()
    print("=" * 78)
    print("REGIME (iv): k = n-1")
    print("=" * 78)
    S1e = S1_sat
    PSe = PS_sat
    TSe = TS_sat
    QSe = QS_generic.subs(t, m - 1)
    F_iv = derive_regime_boundary(n - 1, S1e, PSe, TSe, QSe)
    print(f"  derived in {time.time()-t3:.1f}s")
    print("F(n-1) =", F_iv)
    with open('F_iv.pkl', 'wb') as f:
        pickle.dump(F_iv, f)

    print()
    print(f"Total time: {time.time()-t0:.1f}s")

    print()
    print("=" * 78)
    print("COLLAPSE CHECK: does F_generic(k), evaluated at k=n-3,n-2,n-1,")
    print("match F(n-3), F(n-2), F(n-1) derived independently above?")
    print("=" * 78)
    d2 = sp.simplify(F_generic.subs(k, n - 3) - F_ii)
    d3 = sp.simplify(F_generic.subs(k, n - 2) - F_iii)
    d4 = sp.simplify(F_generic.subs(k, n - 1) - F_iv)
    print("  F_generic(n-3) - F(n-3) =", d2)
    print("  F_generic(n-2) - F(n-2) =", d3)
    print("  F_generic(n-1) - F(n-1) =", d4)
    if d2 == 0 and d3 == 0 and d4 == 0:
        print("COLLAPSE CONFIRMED: a single formula (F_generic) covers ALL")
        print("0<=k<=n-1 -- this IS Proposicao D4.")
    else:
        print("NO COLLAPSE: the CDF genuinely needs the piecewise statement.")
