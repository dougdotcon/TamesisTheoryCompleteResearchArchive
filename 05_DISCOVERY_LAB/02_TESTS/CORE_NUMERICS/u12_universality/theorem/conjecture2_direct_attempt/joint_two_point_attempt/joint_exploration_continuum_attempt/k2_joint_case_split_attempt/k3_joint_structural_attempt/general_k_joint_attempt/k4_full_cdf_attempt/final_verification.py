"""
K4-FULL-CDF-ATTEMPT: consolidated independent verification.

(A) Proposicao D4 vs. fresh true brute force of Definition 4 itself
    (true_bruteforce_full_cdf_k4.py's saved bf_pmf_N.pkl files), every k.
(B) Proposicao D4 vs. the independent O(n^4) reference engine
    (conditional_cdf.full_cdf_exact, built from Proposicao S + the
    Decomposition Theorem, NOT from Proposicao D4's own closed form).
(C) Exact symbolic recovery of the mean and moment limits (Corollaries
    D4.2-D4.4).
"""
import sys
import glob
import pickle
import time
from fractions import Fraction

import sympy as sp

sys.path.insert(0, '.')
from conditional_cdf import full_cdf_exact

n, k = sp.symbols('n k')

with open('F_generic.pkl', 'rb') as f:
    F = pickle.load(f)


def D4(nv, kv):
    got = sp.Rational(F.subs({n: sp.Integer(nv), k: sp.Integer(kv)}))
    return Fraction(got.p, got.q)


def check_A():
    print("=" * 78)
    print("(A) Proposicao D4 vs fresh true brute force of Definition 4, K=4")
    print("=" * 78)
    files = sorted(glob.glob('bf_pmf_*.pkl'))
    total_checks = 0
    total_mism = 0
    for fn in files:
        with open(fn, 'rb') as fh:
            data = pickle.load(fh)
        nv = data['n']
        cdf = data['cdf']
        total = data['total']
        mism = 0
        for kv in range(0, nv):
            exp = cdf[kv]
            got = D4(nv, kv)
            total_checks += 1
            if exp != got:
                mism += 1
                total_mism += 1
                print(f"    MISMATCH n={nv} k={kv}: bruteforce={exp} D4={got}")
        print(f"  n={nv}: configs={total}, k=0..{nv-1} checked, mismatches={mism}  "
              f"{'OK' if mism == 0 else 'FAIL'}  (elapsed {data['elapsed']:.1f}s)")
    print(f"Total: {total_checks} exact rational comparisons, {total_mism} mismatches.")
    return total_mism == 0


def check_B():
    print()
    print("=" * 78)
    print("(B) Proposicao D4 vs independent O(n^4) reference engine")
    print("=" * 78)
    total = 0
    mism = 0
    t0 = time.time()
    dense_ns = list(range(4, 21))
    for nv in dense_ns:
        for kv in range(0, nv):
            exp, ncomp = full_cdf_exact(nv, kv)
            got = D4(nv, kv)
            total += 1
            if exp != got:
                mism += 1
                print(f"    MISMATCH n={nv} k={kv}: exact={exp} D4={got}")
        print(f"  n={nv}: every k checked ({nv} values)")
    sparse_ns = [22, 25, 28, 30]
    for nv in sparse_ns:
        for kv in range(0, nv, 3):
            exp, ncomp = full_cdf_exact(nv, kv)
            got = D4(nv, kv)
            total += 1
            if exp != got:
                mism += 1
                print(f"    MISMATCH n={nv} k={kv}: exact={exp} D4={got}")
        print(f"  n={nv}: every 3rd k checked")
    print(f"Total exact comparisons: {total}, mismatches: {mism} "
          f"(elapsed {time.time()-t0:.1f}s)")
    return mism == 0


def check_C():
    print()
    print("=" * 78)
    print("(C) Exact symbolic recovery of mean and moment limits (D4.2-D4.4)")
    print("=" * 78)

    S1_ = sp.summation(F, (k, 0, n - 1))
    phi_n4 = sp.simplify(1 - S1_ / n)
    phi_n4 = sp.apart(phi_n4, n)
    print("phi_n^(4) [D4.2, NEW full finite-n formula, derived from D4] =")
    print(" ", phi_n4)
    phi4_const = phi_n4.as_poly(1 / n).nth(0) if False else sp.limit(phi_n4, n, sp.oo)
    c4_coeff = sp.limit((phi_n4 - phi4_const) * n, n, sp.oo)
    print(f"  constant term (n->oo limit) = {phi4_const}   (cited target: 128/315, Estagio 4/24)")
    print(f"  coefficient of 1/n          = {c4_coeff}   (cited target: 23/210, Estagio 6/7)")
    ok_mean = (phi4_const == sp.Rational(128, 315)) and (c4_coeff == sp.Rational(23, 210))
    print("  MATCH" if ok_mean else "  MISMATCH")

    S2 = sp.summation((2 * k + 1) * F, (k, 0, n - 1))
    ET2 = sp.simplify(n**2 - S2)
    EM2 = sp.simplify(ET2 / n**2)
    EM2 = sp.apart(EM2, n)
    lim2 = sp.limit(EM2, n, sp.oo)
    print()
    print("E[(M_n^(4))^2] [D4.3] =", EM2)
    print(f"  limit n->oo = {lim2}   (cited target: 1/5 = 1/(K+1), Estagio 24)")
    ok_m2 = (lim2 == sp.Rational(1, 5))
    print("  MATCH" if ok_m2 else "  MISMATCH")

    j = sp.Symbol('j')
    weight = 3 * (j + 1)**2 - 3 * (j + 1) + 1
    S3 = sp.summation(weight * (1 - F.subs(k, j)), (j, 0, n - 1))
    ET3 = sp.simplify(S3)
    EM3 = sp.simplify(ET3 / n**3)
    EM3 = sp.apart(EM3, n)
    lim3 = sp.limit(EM3, n, sp.oo)
    print()
    print("E[(M_n^(4))^3] [D4.4] =", EM3)
    target3 = sp.Rational(128, 1155)
    print(f"  limit n->oo = {lim3}   (target: {target3}, derived here directly from the")
    print("   CITED general-K continuum density f_{M_K}(x)=2Kx(1-x^2)^(K-1),")
    print("   Estagio 24, by elementary integration -- see ATTEMPT.md Section 6.3)")
    ok_m3 = (lim3 == target3)
    print("  MATCH" if ok_m3 else "  MISMATCH")

    with open('mean_moments.pkl', 'wb') as fh:
        pickle.dump(dict(phi_n4=phi_n4, EM2=EM2, EM3=EM3), fh)

    return ok_mean and ok_m2 and ok_m3


if __name__ == "__main__":
    okA = check_A()
    okB = check_B()
    okC = check_C()
    print()
    print("=" * 78)
    print(f"FINAL: (A) brute force {'PASS' if okA else 'FAIL'} | "
          f"(B) O(n^4) engine {'PASS' if okB else 'FAIL'} | "
          f"(C) moments {'PASS' if okC else 'FAIL'}")
    print("=" * 78)
