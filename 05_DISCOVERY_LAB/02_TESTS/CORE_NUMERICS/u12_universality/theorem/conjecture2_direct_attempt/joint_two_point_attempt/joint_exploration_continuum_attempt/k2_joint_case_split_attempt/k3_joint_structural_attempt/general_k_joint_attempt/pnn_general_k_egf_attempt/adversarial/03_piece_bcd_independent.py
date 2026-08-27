"""
Independent, from-scratch re-derivation of the Piece A/B/C/D r-sum
decomposition (target ATTEMPT.md Sec 2.3), starting ONLY from:
  - Lemma 5's PROVED P0(s), P_same(s,s'), P_disjoint(s,s') formulas
    (THEOREM.md Estagio 35 / predecessor ATTEMPT.md Sec 4, cited),
  - the predecessor's own T(L) description (its Sec 5.1: "sums, over all
    ordered pairs of the n-K non-source roles, the exact probability both
    are cyclic"),
  - elementary position-sum combinatorics (sum_{i=1}^{m} i, and
    sum_{i!=i'} min(i,i') over {1,...,m}, both derived by hand below, not
    copied from anywhere),
  - the already-independently-verified P_same===P_disjoint bonus identity
    (orchestrator's own from-scratch check, re-used here by citation only
    to collapse the cross-arc double sum -- NOT re-derived in this file),
  - this file's own moment_formula_symbolic() from moment_formula_check.py
    (independently derived and validated there).

Derivation (done by hand, reproduced here as comments, then checked in
code against (a) direct brute tuple-composition enumeration and (b) the
already-PROVED Proposition NN3/NN4 closed forms):

Piece B (outside-arc): from O * P0(s) * (L_s-1) [see reduced_model_check.py
comment derivation], expand P0(s) = x_s * sum_S |S|! prod x, group by
subset size r via exchangeability (K choices of "special" source s x
C(K-1,r) choices of r-subset "touched" among the other K-1, all giving the
SAME total moment by exchangeability of composition space):

  sum_L PieceB(L) = K * sum_{r=0}^{K-1} C(K-1,r) r!/n^{r+1} *
                        [mu(L_0^2,r,O^1) - mu(L_0^1,r,O^1)]

Piece C (same-arc): from P0(s) * s_min(L_s)/L_s where
s_min(m) := sum_{i!=i',1<=i,i'<=m} min(i,i') = (m^3-m)/3 (derived by hand:
sum_{i<i'} min(i,i') = sum_{i=1}^{m-1} i*(m-i) = (m-1)m(m+1)/6, times 2 for
both orders). With m=L_s-1: s_min/L_s = (L_s-1)(L_s-2)/3, giving
L_s(L_s-1)(L_s-2) = L_s^3-3L_s^2+2L_s inside the moment:

  sum_L PieceC(L) = (K/3) * sum_{r=0}^{K-1} C(K-1,r) r!/n^{r+1} *
                        [mu(L_0^3,r) - 3 mu(L_0^2,r) + 2 mu(L_0^1,r)]

Piece D (cross-arc): from P_pair(s,s')*(L_s-1)(L_sp-1)/4 summed over
ordered pairs s!=s', using P_pair = 2 x_s x_sp sum_k (k+1)! e_k(x_M) (the
already-verified collapse), expand (L_s^2-L_s)(L_sp^2-L_sp):

  sum_L PieceD(L) = (K(K-1)/2) * sum_{r=0}^{K-2} C(K-2,r) (r+1)!/n^{r+2} *
     [mu(L_0^2 L_1^2,r) - mu(L_0^2 L_1,r) - mu(L_0 L_1^2,r) + mu(L_0 L_1,r)]

These are then checked to be EXACTLY what target's Sec 2.3 states.
"""
import sympy as sp
import time
from math import comb, factorial
from importlib import import_module
moment_mod = import_module("02_moment_formula_independent")
moment_formula_symbolic = moment_mod.moment_formula_symbolic
gen_compositions = moment_mod.gen_compositions

n_sym, K_sym, r_sym = sp.symbols('n K r', positive=True)


def piece_B_total(K, n):
    """Sum over compositions of Piece B(L), as a concrete-K, symbolic-n
    sympy expression, via the r-sum/moment route (independent of the
    tuple-brute-force route in reduced_model_check.py)."""
    total = 0
    for r in range(0, K):
        m2 = moment_formula_symbolic([2], sp.Integer(r), 1, sp.Integer(K), n_sym)
        m1 = moment_formula_symbolic([1], sp.Integer(r), 1, sp.Integer(K), n_sym)
        total += comb(K - 1, r) * factorial(r) / n_sym ** (r + 1) * (m2 - m1)
    return sp.simplify(K * total)


def piece_C_total(K, n):
    total = 0
    for r in range(0, K):
        m3 = moment_formula_symbolic([3], sp.Integer(r), 0, sp.Integer(K), n_sym)
        m2 = moment_formula_symbolic([2], sp.Integer(r), 0, sp.Integer(K), n_sym)
        m1 = moment_formula_symbolic([1], sp.Integer(r), 0, sp.Integer(K), n_sym)
        total += comb(K - 1, r) * factorial(r) / n_sym ** (r + 1) * (m3 - 3 * m2 + 2 * m1)
    return sp.simplify(sp.Rational(K, 3) * total)


def piece_D_total(K, n):
    total = 0
    for r in range(0, K - 1):
        m22 = moment_formula_symbolic([2, 2], sp.Integer(r), 0, sp.Integer(K), n_sym)
        m21 = moment_formula_symbolic([2, 1], sp.Integer(r), 0, sp.Integer(K), n_sym)
        m12 = moment_formula_symbolic([1, 2], sp.Integer(r), 0, sp.Integer(K), n_sym)
        m11 = moment_formula_symbolic([1, 1], sp.Integer(r), 0, sp.Integer(K), n_sym)
        total += comb(K - 2, r) * factorial(r + 1) / n_sym ** (r + 2) * (m22 - m21 - m12 + m11)
    return sp.simplify(sp.Rational(K * (K - 1), 2) * total)


def piece_A_total(K, n):
    """O(O-1) summed over compositions = mu([],0,b=2) - mu([],0,b=1)."""
    m2 = moment_formula_symbolic([], sp.Integer(0), 2, sp.Integer(K), n_sym)
    m1 = moment_formula_symbolic([], sp.Integer(0), 1, sp.Integer(K), n_sym)
    return sp.simplify(m2 - m1)


def Pnn_via_pieces(K):
    """P_nn(n,K) as a symbolic function of n, via Piece A+B+C+D / [C(n,K)(n-K)(n-K-1)]."""
    A = piece_A_total(K, n_sym)
    B = piece_B_total(K, n_sym)
    C = piece_C_total(K, n_sym)
    D = piece_D_total(K, n_sym)
    total = A + B + C + D
    Cnk = sp.binomial(n_sym, K)
    return sp.simplify(total / (Cnk * (n_sym - K) * (n_sym - K - 1)))


if __name__ == "__main__":
    print("=" * 70)
    print("Piece A/B/C/D independently re-derived via r-sum/moment route")
    print("Checked against ALREADY-PROVED Proposition NN3 (K=3), NN4 (K=4)")
    print("=" * 70)

    NN3 = sp.Rational(1, 140) * (35 * n_sym**3 + 38 * n_sym**2 + 23 * n_sym + 6) / n_sym**3
    NN4 = sp.Rational(1, 630) * (126 * n_sym**4 + 187 * n_sym**3 + 177 * n_sym**2 + 98 * n_sym + 24) / n_sym**4

    for K, known in [(3, NN3), (4, NN4)]:
        mine = Pnn_via_pieces(K)
        diff = sp.simplify(mine - known)
        print(f"K={K}: my r-sum-route P_nn(n,{K}) - known closed form  simplifies to: {diff}")
        print(f"   MATCH: {diff == 0}")
        assert diff == 0

    print("\nAlso evaluating the r-sum-route P_nn(n,K) at several concrete n, K=3,4,5,")
    print("(K=5 has no already-proved closed form cited in this file, so this is a")
    print("display/sanity step only -- 01_reduced_model_independent.py's independent tuple-")
    print("enumeration route already cross-validated K=5).")

    for K in (3, 4, 5):
        for nv in (K + 3, K + 6):
            mine = Pnn_via_pieces(K).subs(n_sym, nv)
            print(f"  K={K} n={nv}: r-sum-route P_nn = {mine}")

    print("\n" + "=" * 70)
    print("BONUS UNIFICATION CHECK: does the r-sum/moment-machinery route")
    print("(this file, totally separate code path from 01_reduced_model_")
    print("independent.py's literal tuple/role-pair brute force) ALSO")
    print("reproduce the target's NEW K=7, K=8 closed forms symbolically?")
    print("(Sec 2.3's own Piece A/B/C/D decomposition, re-derived here from")
    print(" first principles, is what the target's fast algorithm actually")
    print(" uses for K=7,8 -- this checks that decomposition's correctness")
    print(" directly and symbolically, not just its final numeric outputs.)")
    print("=" * 70)

    K7_target = (6435 * n_sym**7 + 17548 * n_sym**6 + 35958 * n_sym**5 + 55460 * n_sym**4
                 + 62565 * n_sym**3 + 48628 * n_sym**2 + 23148 * n_sym + 5040) / (51480 * n_sym**7)
    K8_target = (24310 * n_sym**8 + 76627 * n_sym**7 + 186527 * n_sym**6 + 353609 * n_sym**5
                 + 513865 * n_sym**4 + 552592 * n_sym**3 + 412892 * n_sym**2 + 190224 * n_sym + 40320) / (218790 * n_sym**8)

    k78_piece_ok = True
    for K, target in [(7, K7_target), (8, K8_target)]:
        t0 = time.time()
        mine = Pnn_via_pieces(K)
        dt = time.time() - t0
        diff = sp.simplify(mine - target)
        ok = (diff == 0)
        k78_piece_ok &= ok
        print(f"K={K}: r-sum-route P_nn(n,{K}) (took {dt:.2f}s) minus target's closed form "
              f"simplifies to: {diff}   MATCH: {ok}")
    print(f"\nALL K=7/K=8 r-sum-route MATCHES: {k78_piece_ok}")
    assert k78_piece_ok

    print("\nDONE.")
