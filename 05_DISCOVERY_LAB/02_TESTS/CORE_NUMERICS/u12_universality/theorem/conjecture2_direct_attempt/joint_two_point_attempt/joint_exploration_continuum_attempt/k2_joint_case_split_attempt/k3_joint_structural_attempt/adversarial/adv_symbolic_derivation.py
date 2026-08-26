"""
Independent, from-scratch SYMBOLIC (sympy, exact Rational) re-derivation
of Proposition NN3's closed form, via the same case-split machinery
(Lemma 1 + Lemma 5) already independently re-verified in
adv_lemma1_m3.py / adv_lemma5_check.py / adv_reduced_model_assembly.py,
but this time summed in full symbolic closed form (sp.summation over the
composition region), exactly as claimed possible in ATTEMPT.md section
4.2 -- built fresh, own code, not copied from symbolic_derivation_k3.py.

No .py file from any front in the lineage was read.
"""
import sympy as sp

n, L0, L1, L2, O = sp.symbols('n L0 L1 L2 O', positive=True)
i, j = sp.symbols('i j', positive=True)


def P_single_sym(pos, La, Lb, nv):
    return pos * (2*La*Lb + La*nv + Lb*nv + nv**2) / nv**3


def P_cross_sym(posA, posB, Lother, nv):
    return 2 * posA * posB * (2*Lother + nv) / nv**3


def T_symbolic(L0v, L1v, L2v, nv):
    Ov = nv - L0v - L1v - L2v
    Ls = {0: L0v, 1: L1v, 2: L2v}
    others = {0: (L1v, L2v), 1: (L0v, L2v), 2: (L0v, L1v)}

    total = sp.Integer(0)
    total += Ov * (Ov - 1)

    single_expr = {}
    for s in (0, 1, 2):
        La, Lb = others[s]
        expr = sp.summation(P_single_sym(i, La, Lb, nv), (i, 1, Ls[s] - 1))
        single_expr[s] = sp.simplify(expr)

    oa = sum(single_expr.values())
    total += 2 * Ov * oa

    for s in (0, 1, 2):
        La, Lb = others[s]
        Lsv = Ls[s]
        # sum_{pos=1}^{Ls-1} P_single(pos) * (Ls-1-pos)
        expr = sp.summation(P_single_sym(i, La, Lb, nv) * (Lsv - 1 - i), (i, 1, Lsv - 1))
        total += 2 * sp.simplify(expr)

    pairs = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]
    for s, t, other in pairs:
        Lo = Ls[other]
        expr = sp.summation(
            sp.summation(P_cross_sym(i, j, Lo, nv), (j, 1, Ls[t] - 1)),
            (i, 1, Ls[s] - 1)
        )
        total += 2 * sp.simplify(expr)

    return sp.expand(total)


if __name__ == '__main__':
    print("Building symbolic T(L0,L1,L2,n) ...")
    Tsym = T_symbolic(L0, L1, L2, n)
    Tsym = sp.expand(Tsym)
    print("T(L0,L1,L2,n) built (degree check):", sp.Poly(Tsym, L0, L1, L2).total_degree())

    print("Summing over L2 = 1 .. n-L0-L1 ...")
    S2 = sp.summation(Tsym, (L2, 1, n - L0 - L1))
    S2 = sp.simplify(S2)

    print("Summing over L1 = 1 .. n-L0-1 ...")
    S1 = sp.summation(S2, (L1, 1, n - L0 - 1))
    S1 = sp.simplify(S1)

    print("Summing over L0 = 1 .. n-2 ...")
    S0 = sp.summation(S1, (L0, 1, n - 2))
    S0 = sp.simplify(S0)

    print("Raw triple sum of T:", S0)

    num_compositions = sp.binomial(n, 3)
    denom_role_pairs = (n - 3) * (n - 4)

    Pnn3 = sp.simplify(S0 / (num_compositions * denom_role_pairs))
    Pnn3 = sp.factor(sp.simplify(Pnn3))
    print()
    print("Derived P_nn(n,3) =", Pnn3)

    claimed = sp.Rational(1) * (35*n**3 + 38*n**2 + 23*n + 6) / (140*n**3)
    diff = sp.simplify(Pnn3 - claimed)
    print("Claimed P_nn(n,3) =", sp.simplify(claimed))
    print("Difference (should be 0):", diff)
    print()
    print(f"SYMBOLIC_TRIPLE_SUM_MATCHES_CLAIMED_CLOSED_FORM: {diff == 0}")
