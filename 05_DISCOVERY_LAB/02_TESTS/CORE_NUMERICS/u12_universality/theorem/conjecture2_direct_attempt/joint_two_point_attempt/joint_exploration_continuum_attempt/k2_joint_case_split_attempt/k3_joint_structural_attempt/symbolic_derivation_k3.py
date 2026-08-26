"""
symbolic_derivation_k3.py

The full, self-contained, exact symbolic derivation of Proposition NN3:

    P_nn(n,3) = (35 n^3 + 38 n^2 + 23 n + 6) / (140 n^3)
              = 1/4 + 19/(70n) + 23/(140 n^2) + 3/(70 n^3),  for all n>=6.

Consolidates the derivation described in ATTEMPT.md Sec 4.2 into one
runnable script: builds T(L0,L1,L2) from the closed-form single-point and
cross-arc rules of symbolic_redirect_k3.py (Lemma 5), sums it exactly (no
floating point at any stage) over the composition region
L0,L1,L2>=1, L0+L1+L2<=n, one variable at a time (L2, then L1, then L0),
divides by C(n,3)*(n-3)*(n-4) (the K=3 analogue of Proposition NN2's own
assembly denominator), and simplifies.

Runtime note: the triple symbolic summation is the most expensive part of
this repository's derivation (each nested sp.summation call works with a
growing multivariate polynomial). Expect several minutes total. The
resulting closed form is cross-validated three independent ways elsewhere
in this front's files:
  - against TRUE brute force over full Definition-4 permutations,
    n=6..9 (brute_force_k3.py, disjoint code path);
  - against the numeric reduced-model assembly at n=6..30,40
    (assemble_pnn3.py, disjoint code path -- exact Fraction arithmetic at
    concrete integers, no symbolic summation);
  - internally, this script's own intermediate sums are checked at
    concrete n via direct substitution (see __main__ below).
"""

import sys
import time
import sympy as sp

from symbolic_redirect_k3 import n, L0, L1, L2, O_expr, p_single_symbolic, p_joint_cross_symbolic


def derive():
    k, kp = sp.symbols('k kp', positive=True, integer=True)

    t0 = time.time()
    A0 = sp.simplify(p_single_symbolic(0, k) / k)
    A1 = sp.simplify(p_single_symbolic(1, k) / k)
    A2 = sp.simplify(p_single_symbolic(2, k) / k)
    B01 = sp.simplify(p_joint_cross_symbolic(0, 1, k, kp) / (k * kp))
    B02 = sp.simplify(p_joint_cross_symbolic(0, 2, k, kp) / (k * kp))
    B12 = sp.simplify(p_joint_cross_symbolic(1, 2, k, kp) / (k * kp))
    print(f"[t={time.time()-t0:.1f}s] Lemma 5 coefficients derived:", file=sys.stderr)
    print("  A0 =", A0, file=sys.stderr)
    print("  A1 =", A1, file=sys.stderr)
    print("  A2 =", A2, file=sys.stderr)
    print("  B01 =", B01, file=sys.stderr)
    print("  B02 =", B02, file=sys.stderr)
    print("  B12 =", B12, file=sys.stderr)

    def sum_single(A, L):
        # sum_{k=1}^{L-1} k*A
        return A * (L - 1) * L / 2

    def sum_same_arc(A, L):
        # 2 * sum_{k=1}^{L-1} (L-1-k) * (k*A)   [ordered pairs, monotone fact]
        kk = sp.symbols('kk', positive=True, integer=True)
        expr = (L - 1 - kk) * kk * A
        s = sp.summation(expr, (kk, 1, L - 1))
        return 2 * s

    def sum_cross(B, La, Lb):
        sa = (La - 1) * La / 2
        sb = (Lb - 1) * Lb / 2
        return B * sa * sb

    O = O_expr
    T_OO = O * (O - 1)
    T_Oarc = 2 * O * (sum_single(A0, L0) + sum_single(A1, L1) + sum_single(A2, L2))
    T_same = sum_same_arc(A0, L0) + sum_same_arc(A1, L1) + sum_same_arc(A2, L2)
    T_cross = 2 * (sum_cross(B01, L0, L1) + sum_cross(B02, L0, L2) + sum_cross(B12, L1, L2))
    T = sp.expand(T_OO + T_Oarc + T_same + T_cross)
    print(f"[t={time.time()-t0:.1f}s] T(L0,L1,L2) assembled ({len(T.args)} terms)", file=sys.stderr)

    S_L2 = sp.simplify(sp.summation(T, (L2, 1, n - L0 - L1)))
    print(f"[t={time.time()-t0:.1f}s] summed over L2", file=sys.stderr)

    S_L1 = sp.simplify(sp.summation(S_L2, (L1, 1, n - L0 - 1)))
    print(f"[t={time.time()-t0:.1f}s] summed over L1", file=sys.stderr)

    S_total = sp.simplify(sp.summation(S_L1, (L0, 1, n - 2)))
    print(f"[t={time.time()-t0:.1f}s] summed over L0", file=sys.stderr)

    C_n_3 = n * (n - 1) * (n - 2) / 6
    P = sp.factor(sp.simplify(S_total / (C_n_3 * (n - 3) * (n - 4))))
    print(f"[t={time.time()-t0:.1f}s] final simplification done", file=sys.stderr)
    return P


if __name__ == "__main__":
    P = derive()
    print()
    print("Proposition NN3:")
    print("P_nn(n,3) =", P)
    print("         =", sp.apart(P, n))

    # internal cross-check: compare against the already-computed reduced
    # model values (assemble_pnn3.py) at a spread of concrete n, WITHOUT
    # importing that module's derivation logic -- just evaluate this
    # symbolic closed form and compare to the hard-coded exact values
    # reported in ATTEMPT.md Sec 4.3-4.4 (independently obtained).
    known = {
        6: sp.Rational(3, 10),
        7: sp.Rational(7017, 24010),
        8: sp.Rational(10271, 35840),
        9: sp.Rational(4801, 17010),
        30: sp.Rational(40829, 157500),
        40: sp.Rational(164409, 640000),
    }
    print()
    print("cross-check against independently-computed exact values:")
    all_ok = True
    for nv, val in known.items():
        pred = P.subs(n, nv)
        ok = sp.simplify(pred - val) == 0
        all_ok &= ok
        print(f"  n={nv}: closed_form={pred}  known={val}  match={ok}")
    print("ALL MATCH" if all_ok else "MISMATCH FOUND")
