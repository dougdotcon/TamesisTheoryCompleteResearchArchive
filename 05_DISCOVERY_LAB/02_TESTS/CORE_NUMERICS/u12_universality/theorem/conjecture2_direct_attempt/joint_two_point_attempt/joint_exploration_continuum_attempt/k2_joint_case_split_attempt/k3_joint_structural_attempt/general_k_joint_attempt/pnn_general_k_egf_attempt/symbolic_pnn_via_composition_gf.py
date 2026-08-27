"""
Task item 2 (main event): push the integral/GF representation through the
FULL composition sum, for a CONCRETE K. Uses gf_moment_machinery.py's
validated GF-moment machinery, plus the Governing-Source Reindexing
exchangeability (THEOREM.md Estagio 35 sec 2 / predecessor sec 2, already
PROVED, cited) to replace "loop over all K sources" / "loop over all
subsets S" with binomial-coefficient multiplicities -- i.e. this is the
genuine push-through of the integral idea into T(L)'s composition sum.

Written fresh; no file from any front read; only P_0/P_same/P_disjoint's
already-PROVED closed forms (and this front's own P_same==P_disjoint
collapse) are used as inputs -- same mathematical ingredients as
reduced_model_direct_assembly.py, but assembled via generating functions
instead of direct enumeration of the L-simplex, which is why this script
is 100-1000x faster (K=6: ~0.3s here vs ~26s for the direct brute
composition sum at a single large n, and the predecessor's own nested-Sum
approach reportedly took ~166s at K=6) and scales cleanly to K=7,8.

T(L) piece derivations (same structural breakdown as
reduced_model_direct_assembly.py, but each piece re-expressed as an
explicit sum over subset SIZE r, using exchangeability to replace "sum
over all C(K-1,r) subsets" with "C(K-1,r) times one representative
value" -- itself a further, K-specific simplification enabled by
Governing-Source Reindexing):

  Piece A (outside-outside): O*(O-1), no subset sum, no source touched.

  Piece B (outside-arc), representative source index 0, multiplicity K:
    K * Sum_{r=0}^{K-1} [C(K-1,r) r! / n^{r+1}] *
        [moment(L_0^2, r plain, O^1) - moment(L_0^1, r plain, O^1)]
    (from O * (L_0/n) * Sum_S|S|!Prod_S x_u * (L_0-1), L_0(L_0-1)=L_0^2-L_0)

  Piece C (same-arc), representative source index 0, multiplicity K:
    (K/3) * Sum_r [C(K-1,r) r!/n^{r+1}] *
        [moment(L_0^3,r,O^0) - 3 moment(L_0^2,r,O^0) + 2 moment(L_0^1,r,O^0)]
    (from P_0(0)*(L_0-2)(L_0-1)/3, expanding the cubic)

  Piece D (cross-arc), representative pair (0,1), multiplicity K(K-1):
    K(K-1) * Sum_r [C(K-2,r)(r+1)!/n^{r+2}] * (1/2) *
        [moment(L_0^2 L_1^2) - moment(L_0^2 L_1) - moment(L_0 L_1^2) + moment(L_0 L_1)]
    (from (L_0-1)/2*(L_1-1)/2 * P_{0,1}, P_{0,1}=2 x_0 x_1 Sum_S(|S|+1)!...;
    the 1/2 factor -- NOT 1/4 -- was cross-checked piece-by-piece against
    reduced_model_direct_assembly.py's direct T(L) computation: an
    earlier draft of this script had /4 here, off by exactly 2x at every
    tested (n,K) cell, caught by that piece-by-piece comparison before
    any Proposition in this document was finalized; see ATTEMPT.md
    sec 7 for the full disclosure)
"""
import sympy as sp
import time
from gf_moment_machinery import composition_moment_symbolic

n = sp.symbols('n', positive=True)


def piece_A_outside_outside(K):
    return (composition_moment_symbolic(n, K, {}, O_power=2)
            - composition_moment_symbolic(n, K, {}, O_power=1))


def piece_B_outside_arc(K):
    total = sp.Integer(0)
    for r in range(0, K):
        mult = sp.binomial(K - 1, r) * sp.factorial(r) / n ** (r + 1)
        t2 = {0: 2}; t1 = {0: 1}
        for j in range(1, r + 1):
            t2[j] = 1; t1[j] = 1
        m2 = composition_moment_symbolic(n, K, t2, O_power=1)
        m1 = composition_moment_symbolic(n, K, t1, O_power=1)
        total += mult * (m2 - m1)
    return K * total


def piece_C_same_arc(K):
    total = sp.Integer(0)
    for r in range(0, K):
        mult = sp.binomial(K - 1, r) * sp.factorial(r) / n ** (r + 1)
        base = {j: 1 for j in range(1, r + 1)}
        t3 = dict(base); t3[0] = 3
        t2 = dict(base); t2[0] = 2
        t1 = dict(base); t1[0] = 1
        m3 = composition_moment_symbolic(n, K, t3, O_power=0)
        m2 = composition_moment_symbolic(n, K, t2, O_power=0)
        m1 = composition_moment_symbolic(n, K, t1, O_power=0)
        total += mult * (m3 - 3 * m2 + 2 * m1) / 3
    return K * total


def piece_D_cross_arc(K):
    if K < 2:
        return sp.Integer(0)
    total = sp.Integer(0)
    for r in range(0, K - 1):
        mult = sp.binomial(K - 2, r) * sp.factorial(r + 1) / n ** (r + 2)
        base = {j: 1 for j in range(2, 2 + r)}
        combos = [((2, 2), 1), ((2, 1), -1), ((1, 2), -1), ((1, 1), 1)]
        inner = sp.Integer(0)
        for (a0, a1), sign in combos:
            touched = dict(base)
            touched[0] = a0
            touched[1] = a1
            inner += sign * composition_moment_symbolic(n, K, touched, O_power=0)
        total += mult * inner / 2
    return K * (K - 1) * total


def T_total(K):
    return sp.together(piece_A_outside_outside(K) + piece_B_outside_arc(K)
                        + piece_C_same_arc(K) + piece_D_cross_arc(K))


def pnn_symbolic(K):
    Tt = T_total(K)
    denom = sp.binomial(n, K) * (n - K) * (n - K - 1)
    return sp.cancel(sp.together(Tt / denom))


def pnn_closed_form(K):
    """Fully simplified P(n)/n^K closed form (binomial(n+a,b) terms
    expanded out into an explicit numerator polynomial)."""
    expr = pnn_symbolic(K)
    return sp.nsimplify(sp.simplify(expr.rewrite(sp.factorial)))


if __name__ == "__main__":
    print("=" * 78)
    print("Symbolic-in-n P_nn(n,K) via the GF/moment push-through of the")
    print("composition sum, for concrete K -- vs already-PROVED / ")
    print("predecessor-reported closed forms")
    print("=" * 78)

    known = {
        1: (3 * n + 1) / (6 * n),
        2: (10 * n ** 2 + 7 * n + 2) / (30 * n ** 2),
        3: (35 * n ** 3 + 38 * n ** 2 + 23 * n + 6) / (140 * n ** 3),
        4: (126 * n ** 4 + 187 * n ** 3 + 177 * n ** 2 + 98 * n + 24) / (630 * n ** 4),
        5: (462 * n ** 5 + 874 * n ** 4 + 1139 * n ** 3 + 989 * n ** 2 + 514 * n + 120) / (2772 * n ** 5),
        6: (1716 * n ** 6 + 3958 * n ** 5 + 6616 * n ** 4 + 7933 * n ** 3
            + 6472 * n ** 2 + 3204 * n + 720) / (12012 * n ** 6),
    }
    for K in range(1, 7):
        t0 = time.time()
        mine = pnn_symbolic(K)
        dt = time.time() - t0
        diff = sp.simplify(mine - known[K])
        print(f"K={K}: match_known_formula = {diff == 0}   ({dt:.2f}s, raw binomial form)")
        if diff != 0:
            print(f"   mine  = {sp.simplify(mine)}")
            print(f"   known = {sp.simplify(known[K])}")

    print()
    print("=" * 78)
    print("Same checks, but fully simplified into explicit P(n)/(D n^K) form")
    print("=" * 78)
    for K in range(1, 7):
        t0 = time.time()
        cf = pnn_closed_form(K)
        dt = time.time() - t0
        diff = sp.simplify(cf - known[K])
        print(f"K={K} ({dt:.2f}s): {cf}   matches known = {diff == 0}")

    print()
    print("=" * 78)
    print("NEW: K=7, K=8 -- full closed forms, independently verified in")
    print("c1_table_k7_k8.py against reduced_model_direct_assembly.py at")
    print("several concrete n (see that script's log)")
    print("=" * 78)
    for K in [7, 8]:
        t0 = time.time()
        cf = pnn_closed_form(K)
        dt = time.time() - t0
        print(f"K={K} ({dt:.2f}s): P_nn(n,{K}) = {cf}")
