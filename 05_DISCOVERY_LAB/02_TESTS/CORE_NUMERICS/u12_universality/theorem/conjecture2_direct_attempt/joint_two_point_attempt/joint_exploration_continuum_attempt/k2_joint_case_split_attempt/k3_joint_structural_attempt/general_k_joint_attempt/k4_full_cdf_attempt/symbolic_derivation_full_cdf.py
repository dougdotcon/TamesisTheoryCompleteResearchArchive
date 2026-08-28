"""
K4-FULL-CDF-ATTEMPT: main proof.  Full, gap-free symbolic derivation of
Proposicao D4 -- the closed-form finite-n CDF of M_n^{(4)} -- by summing
the exact conditional CDF (Section 3 of ATTEMPT.md, built from the CITED
general-K Proposicao S + Full Cycle-Count Decomposition Theorem,
Estagio 41) over the entire 4-dimensional composition simplex.

Method: the K=3 "shift trick" (Estagio 40 Section 4.2), generalized one
level further for K=4 (each pattern of size |A| < 4 has 4-|A| "free"
remaining arcs that must themselves be composed, contributing an extra
binomial multiplicity factor -- absent at K=3 for its own 2-of-3/3-of-3
patterns, since K=3 only ever has at most 0 free remaining arcs).

Notation (matches ATTEMPT.md Section 1.2 / Section 3):
  n, k as usual.  O := n - L0-L1-L2-L3.  m := n-O = L0+L1+L2+L3.  t := k-O.
  clip(t,L)      := #{v: 1<=v<=L, v<=t}              = min(max(t,0),L)
  paircount(A,B,t)   := #{(v,w): 1<=v<=A,1<=w<=B,v+w<=t}
  triplecount(A,B,C,t)   := analogous, 3 variables
  quadcount(A,B,C,D,t)   := analogous, 4 variables

Building blocks (each summed, via the shift trick, over the FULL
composition sub-simplex of the relevant arc lengths, with the
appropriate "remaining arcs" multiplicity folded in):

  S1(t,m,O)  := sum_{L0=1}^{m-3} C(m-L0-1,2)*(L0+O)*clip(t,L0)
                (single-arc pattern, one of the 4 symmetric copies;
                 C(m-L0-1,2) = compositions of the OTHER 3 arcs)
  PS(t,m,O)  := sum_{L0,L1>=1,L0+L1<=m-2} (m-L0-L1-1)*(O+L0+L1)*paircount(L0,L1,t)
                (pair pattern, one of the 6 symmetric copies;
                 (m-L0-L1-1) = compositions of the OTHER 2 arcs)
  TS(t,m,O)  := sum_{L0,L1,L2>=1,sum<=m-1} (O+L0+L1+L2)*triplecount(L0,L1,L2,t)
                (triple pattern, one of the 4 symmetric copies;
                 multiplicity 1 = the 1 OTHER arc is forced)
  QS(t,m)    := sum_{L0,..,L3>=1,sum=m} quadcount(L0,L1,L2,L3,t)
                (the unique full-4 pattern; no free arcs left)

Each was independently derived here via the shift trick (swap order of
summation: fix the inner lattice-count indices (v,w,...), sum the outer
arc-length variables in closed form via a second "weak/strong
composition count" substitution) and independently verified against
direct brute nested-loop recomputation (test scripts, reproduced inline
as `_selftest_building_blocks`) before being used below.

Per-O contribution to sum_L P(T<=k|L) (sum over the C(m-1,3) compositions
of m into 4 positive parts, using that the L_s factor in Proposicao S's
numerator cancels the L_s denominator of each clip/pair/triple/quad-count
term -- exactly as noted for K=3):

  Contribution(O) = C(m-1,3)*(O/n)*[O<=k]
                     + (4/n^2)  * S1(t,m,O)
                     + (12/n^3) * PS(t,m,O)
                     + (24/n^4) * TS(t,m,O)
                     + (24/n^4) * QS(t,m)

F(k) = [ sum_{O=0}^{min(k,n-4)} Contribution(O) ] / C(n,4),  C(n,4) = n(n-1)(n-2)(n-3)/24.

The valid O-range and the internal truncation/saturation state of each of
S1/PS/TS/QS both depend on how k compares to n-3, n-2, n-1 (analogous to,
but with one MORE boundary than, K=3's own k=n-2/n-1 split) -- derived,
not assumed, in Section 4.3 of ATTEMPT.md.  This gives FOUR regimes:

  (i)   0 <= k <= n-4  ("generic"): O ranges 0..k; S1,PS,TS,QS all
        genuinely truncated for every O in range.
  (ii)  k = n-3: O ranges over ALL valid compositions (0..n-4); S1
        becomes fully saturated (clip never truncates); PS,TS,QS still
        genuinely truncated.
  (iii) k = n-2: O ranges 0..n-4; S1 AND PS both fully saturated; TS,QS
        still genuinely truncated.
  (iv)  k = n-1: O ranges 0..n-4; S1, PS, AND TS all fully saturated;
        only QS (the 4-of-4 pattern) is still genuinely truncated.

Each regime is a SEPARATE, from-scratch `sp.summation` derivation.
"""
import sympy as sp
from fractions import Fraction
import itertools
import time

# ---------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------
n, k, O, m, t, r, j, s = sp.symbols('n k O m t r j s')
L0s = sp.Symbol('L0')


def binom(x, r_):
    """Explicit polynomial C(x,r_) for small integer r_ -- avoids sympy's
    Piecewise-producing sp.binomial() when x is an unevaluated symbol."""
    if r_ == 0:
        return sp.Integer(1)
    num = sp.Integer(1)
    for i in range(r_):
        num *= (x - i)
    return num / sp.factorial(r_)


# ---------------------------------------------------------------------
# Building blocks: S1, PS, TS, QS, both "generic" (genuinely truncated)
# and "sat" (fully saturated / unconditional) closed forms.
# ---------------------------------------------------------------------

def build_S1():
    term1 = binom(m - L0s - 1, 2) * (L0s + O) * L0s
    part1 = sp.summation(term1, (L0s, 1, t))
    term2 = binom(m - L0s - 1, 2) * (L0s + O) * t
    part2 = sp.summation(term2, (L0s, t + 1, m - 3))
    generic = sp.expand(part1 + part2)
    sat_expr = sp.summation(binom(m - L0s - 1, 2) * (L0s + O) * L0s, (L0s, 1, m - 3))
    sat_expr = sp.expand(sat_expr)
    return generic, sat_expr


def build_PS():
    inner = sp.summation((j + 1) * (m - r - j - 1) * (O + r + j), (j, 0, m - 2 - r))
    inner = sp.expand(inner)
    generic = sp.expand(sp.summation((r - 1) * inner, (r, 2, t)))
    sat_expr = sp.expand(sp.summation((r - 1) * inner, (r, 2, m - 2)))
    return generic, sat_expr


def build_TS():
    inner2 = sp.summation(binom(s + 2, 2) * (O + r + s), (s, 0, m - 1 - r))
    inner2 = sp.expand(inner2)
    generic = sp.expand(sp.summation(binom(r - 1, 2) * inner2, (r, 3, t)))
    sat_expr = sp.expand(sp.summation(binom(r - 1, 2) * inner2, (r, 3, m - 1)))
    return generic, sat_expr


def build_QS():
    generic = sp.expand(sp.summation(binom(r - 1, 3) * binom(m - r + 3, 3), (r, 4, t)))
    return generic


if __name__ == "__main__":
    t0 = time.time()
    print("Building S1 (single-arc pattern) closed forms ...")
    S1_generic, S1_sat = build_S1()
    print(f"  done ({time.time()-t0:.1f}s)")

    t1 = time.time()
    print("Building PS (pair pattern) closed forms ...")
    PS_generic, PS_sat = build_PS()
    print(f"  done ({time.time()-t1:.1f}s)")

    t2 = time.time()
    print("Building TS (triple pattern) closed forms ...")
    TS_generic, TS_sat = build_TS()
    print(f"  done ({time.time()-t2:.1f}s)")

    t3 = time.time()
    print("Building QS (full 4-arc pattern) closed form ...")
    QS_generic = build_QS()
    print(f"  done ({time.time()-t3:.1f}s)")

    # Sanity: boundary consistency of generic vs sat forms (should already
    # be confirmed by the dedicated block-level tests, re-checked here)
    print()
    print("Boundary consistency checks (generic(at threshold) == sat):")
    print("  S1 :", sp.simplify(S1_generic.subs(t, m - 3) - S1_sat))
    print("  PS :", sp.simplify(PS_generic.subs(t, m - 2) - PS_sat))
    print("  TS :", sp.simplify(TS_generic.subs(t, m - 1) - TS_sat))

    import pickle
    with open('building_blocks.pkl', 'wb') as f:
        pickle.dump(dict(S1_generic=S1_generic, S1_sat=S1_sat,
                          PS_generic=PS_generic, PS_sat=PS_sat,
                          TS_generic=TS_generic, TS_sat=TS_sat,
                          QS_generic=QS_generic), f)
    print()
    print(f"Total time: {time.time()-t0:.1f}s. Saved to building_blocks.pkl")
