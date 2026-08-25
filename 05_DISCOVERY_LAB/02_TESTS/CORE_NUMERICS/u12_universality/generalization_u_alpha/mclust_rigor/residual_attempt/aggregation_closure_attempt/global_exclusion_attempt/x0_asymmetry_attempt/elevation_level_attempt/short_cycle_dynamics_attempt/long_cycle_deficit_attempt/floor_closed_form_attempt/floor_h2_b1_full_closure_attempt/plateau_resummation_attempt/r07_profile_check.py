#!/usr/bin/env python3
"""
r07_profile_check.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Direct numerical test of the DERIVED plateau-profile structure: the g->inf
plateau of Phi(s, g) at fixed s should be

    F(s) = eps*R(x) + eps^2*(2 x R(x) - 2) + O(eps^3),
    x = s*sqrt(c), eps = 1/sqrt(c), R(x) = sqrt(pi/2)*erfcx(x/sqrt(2)),

with F(0) = Pi(c). Evaluates Phi(s, t0) = sum_k a_k(s) t0^k from this
front's own exact (P,Q)-family polynomials at s > 0 (the same validated
recursion; evaluation at s just uses the full polynomials instead of their
constant terms), at c = 1000 and c = 2560, t0 chosen so c*t0 = 230/260.

This also supplies the analytic explanation of the wave-16 SS3.4/referee SS5
near-rank-2 SVD finding: Phi(s,g) ~= e^{-cg} + (1-e^{-cg}) F(s) with F(s)
asymptotically the SAME erfcx shape as psi1 = b_1 (the k=1 series
coefficient), pinned here quantitatively.

Deterministic; no randomness.
"""

import time
from mpmath import mp, mpf, sqrt, pi, erfc, exp, fabs, log10, nstr

import sys
sys.path.insert(0, '.')
from r01_family_series import FamilyRecursion, peval


def phi_at_s(fr, K, s_list, t0_list):
    """run recursion, evaluating a_k(s) on the fly for each s in s_list."""
    c = fr.c
    import r01_family_series as r01
    a_prev = ([mpf(1)], [])
    a_cur = ([-c], [])
    b_prev = ([], [])
    E = {s: exp(c * s**2 / 2) * erfc(s * sqrt(c / 2)) for s in s_list}
    avals = {s: [mpf(1), -c] for s in s_list}
    for k in range(1, K):
        A = r01.padd(r01.pscale(a_prev[0], -c / k), r01.pscale(b_prev[0], c))
        B = r01.padd(r01.pscale(a_prev[1], -c / k), r01.pscale(b_prev[1], c))
        b_cur = fr.bsolve(A, B)
        wP = r01.padd(r01.padd(r01.pscale(a_prev[0], mpf(1) / k),
                               r01.pone_minus_s(b_cur[0])),
                      r01.pscale(b_prev[0], mpf(-1)))
        wQ = r01.padd(r01.padd(r01.pscale(a_prev[1], mpf(1) / k),
                               r01.pone_minus_s(b_cur[1])),
                      r01.pscale(b_prev[1], mpf(-1)))
        dP, dQ = fr.deriv_F(a_cur)
        nP = r01.pscale(r01.padd(r01.padd(dP, r01.pscale(a_cur[0], -c)),
                                 r01.pscale(wP, c)), mpf(1) / (k + 1))
        nQ = r01.pscale(r01.padd(r01.padd(dQ, r01.pscale(a_cur[1], -c)),
                                 r01.pscale(wQ, c)), mpf(1) / (k + 1))
        a_next = (nP, nQ)
        for s in s_list:
            avals[s].append(peval(nP, s) + peval(nQ, s) * E[s])
        a_prev, a_cur, b_prev = a_cur, a_next, b_cur
    out = {}
    for s in s_list:
        row = {}
        for t0 in t0_list:
            acc = mp.zero
            tp = mpf(1)
            for ak in avals[s]:
                acc += ak * tp
                tp *= t0
            row[t0] = acc
        out[s] = row
    return out


def main():
    for cval, K, dps in ((1000, 2000, 360), (2560, 2000, 360)):
        mp.dps = dps
        c = mpf(cval)
        eps = 1 / sqrt(c)
        t0s = [mpf(230) / c, mpf(260) / c]
        xs = [mpf(0), mpf('0.5'), mpf(1), mpf(2), mpf(3)]
        ss = [x * eps for x in xs]
        t = time.time()
        fr = FamilyRecursion(cval)
        res = phi_at_s(fr, K, ss, t0s)
        print(f"c={cval} (K={K}, dps={dps}, {time.time()-t:.0f}s):  "
              f"F(s) vs eps*R(x) + eps^2*(2xR-2)")
        for x, s in zip(xs, ss):
            F1 = res[s][t0s[0]]
            F2 = res[s][t0s[1]]
            stab = fabs(F1 - F2) / fabs(F2) if F2 != 0 else mpf(1)
            R = sqrt(pi / 2) * exp(x**2 / 2) * erfc(x / sqrt(2))  # erfcx(x/sqrt2)
            pred1 = eps * R
            pred2 = eps * R + eps**2 * (2 * x * R - 2)
            r1 = (F2 - pred1) / eps**2          # should -> (2xR-2)
            r2 = (F2 - pred2) / eps**3          # should be O(1)
            print(f"  x={nstr(x,3):>5}  F={nstr(F2, 20):>24}"
                  f"  [t0-stab ~1e{int(log10(stab)) if stab>0 else -dps}]")
            print(f"        (F-eps R)/eps^2 = {nstr(r1, 12):>16}   "
                  f"2xR-2 = {nstr(2*x*R-2, 12):>16}   "
                  f"resid3/eps^3 = {nstr(r2, 8)}")
        print()


if __name__ == '__main__':
    main()
