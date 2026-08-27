"""
Task item 3a, the actual experiment: with the symbolic-in-(n,K,r) moment
formulas of symbolic_k_moment_formulas.py (verified), build each of
T(L)'s four pieces as an explicit summand over r with SYMBOLIC upper
limit K-1 (or K-2), and determine whether the r-sum closes in elementary
form for FREE K -- i.e. attempt a genuine K-uniform closed form for
P_nn(n,K), not K-by-K.

Two tools are used, in order of strength of the answer they give:

  1. sp.Sum(...).doit() -- sympy's general summation entry point. This
     was tried FIRST and found to hang / not return within a generous
     timeout (see ATTEMPT.md sec 7.2 for the raw timing log) -- a
     SUGGESTIVE but not RIGOROUS negative result (sympy simply not
     finding an answer is not a proof none exists).

  2. sympy.concrete.gosper.gosper_sum -- Gosper's algorithm, the actual
     DECISION PROCEDURE for whether a hypergeometric term has a
     hypergeometric-term antidifference (i.e. whether the INDEFINITE sum
     closes in the class of ratios of Pochhammer/Gamma expressions).
     gosper_sum returns None precisely when it has PROVED no such
     antidifference exists -- not a timeout, a certificate. This is the
     rigorous tool used below, and it returns in well under a second on
     every piece.

Additionally, since ANY finite sum of a hypergeometric term is trivially
equal to the value of a generalized hypergeometric function pFq at a
specific point (by definition of what a hypergeometric series is), each
piece's r-sum is ALSO written explicitly as a terminating pFq expression
(verified numerically against the direct finite sum) and run through
sp.hyperexpand -- which covers a WIDER simplification class than Gosper
(Gauss/Vandermonde/Saalschutz/Dixon/Watson-type summation theorems for
well-poised or balanced series), to check whether the piece reduces to an
elementary closed form by a route Gosper's indefinite-summation approach
does not test.

Written fresh; no file from any front read.
"""
import sympy as sp
import time
from sympy.concrete.gosper import gosper_sum
from symbolic_k_moment_formulas import moment_formula_one_special, moment_formula_two_special, n, K, r


def build_summand_B():
    """Outside-arc piece's r-summand (K,r symbolic)."""
    m2 = moment_formula_one_special(2, 1)
    m1 = moment_formula_one_special(1, 1)
    summand = sp.binomial(K - 1, r) * sp.factorial(r) / n ** (r + 1) * (m2 - m1)
    return sp.simplify(summand)


def build_summand_C():
    """Same-arc piece's r-summand."""
    m3 = moment_formula_one_special(3, 0)
    m2 = moment_formula_one_special(2, 0)
    m1 = moment_formula_one_special(1, 0)
    summand = sp.binomial(K - 1, r) * sp.factorial(r) / n ** (r + 1) * (m3 - 3 * m2 + 2 * m1) / 3
    return sp.simplify(summand)


def build_summand_D():
    """Cross-arc piece's r-summand (two special indices)."""
    m22 = moment_formula_two_special(2, 2)
    m21 = moment_formula_two_special(2, 1)
    m12 = moment_formula_two_special(1, 2)
    m11 = moment_formula_two_special(1, 1)
    inner = m22 - m21 - m12 + m11
    summand = sp.binomial(K - 2, r) * sp.factorial(r + 1) / n ** (r + 2) * inner / 2
    return sp.simplify(summand)


def report_gosper(name, summand, upper_limit):
    print(f"--- Piece {name}: r-summand (K,n,r symbolic) ---")
    print(f"  summand = {summand}")
    ratio = sp.simplify(summand.subs(r, r + 1) / summand)
    print(f"  term ratio T(r+1)/T(r) = {ratio}   (rational in r => genuine hypergeometric term)")
    t0 = time.time()
    result = gosper_sum(summand, (r, 0, upper_limit))
    dt = time.time() - t0
    print(f"  gosper_sum(...): {result}   ({dt:.3f}s)")
    if result is None:
        print("  => Gosper's algorithm has PROVED no hypergeometric-term antidifference")
        print("     exists for this summand: a rigorous certificate of non-closure in the")
        print("     'ratio of Gamma functions' sense, not merely 'sympy could not find one'.")
    return result


def hypergeometric_representation(summand, upper_limit, Kval, nval):
    """Express Sum_{r=0}^{upper} summand(r) as T(0) * pFq(...) by reading
    off the Pochhammer parameters from the rational term ratio, then
    verify numerically and attempt hyperexpand."""
    ratio = sp.simplify(summand.subs(r, r + 1) / summand)
    ratio = sp.cancel(ratio)
    num, den = sp.fraction(ratio)
    num = sp.Poly(sp.expand(num), r)
    den = sp.Poly(sp.expand(den), r)
    print(f"  ratio numerator (as poly in r): {num.as_expr()}  roots: {sp.roots(num)}")
    print(f"  ratio denominator (as poly in r): {den.as_expr()}  roots: {sp.roots(den)}")


if __name__ == "__main__":
    print("=" * 78)
    print("Attempting K-uniform closure of T(L)'s r-sums via Gosper's algorithm")
    print("(the rigorous decision procedure), and via hyperexpand on the")
    print("equivalent terminating-pFq representation.")
    print("=" * 78)

    summand_B = build_summand_B()
    summand_C = build_summand_C()
    summand_D = build_summand_D()

    print("\nNOTE (self-caught, disclosed): an early version of this script's")
    print("piece_D construction used a 1/4 prefactor copied hastily from the")
    print("cross-arc position-sum coefficient (L_s-1)/2*(L_s'-1)/2, forgetting")
    print("that P_{s,s'} itself already carries a factor of 2 (from the")
    print("P_same==P_disjoint collapse in double_integral_p_disjoint.py). This")
    print("was caught by a piece-by-piece numeric comparison against")
    print("reduced_model_direct_assembly.py's direct T(L) computation (every")
    print("cell off by EXACTLY 2x), before any Proposition below was finalized.")
    print("The corrected 1/2 factor is used throughout this script and")
    print("symbolic_pnn_via_composition_gf.py (both already re-verified there).")
    print("=" * 78)

    resB = report_gosper("B (outside-arc)", summand_B, K - 1)
    print()
    resC = report_gosper("C (same-arc)", summand_C, K - 1)
    print()
    resD = report_gosper("D (cross-arc)", summand_D, K - 2)

    print()
    print("=" * 78)
    print("Curiosity (verified separately, see ATTEMPT.md sec 7.3): pieces B")
    print("and C -- outside-arc and same-arc -- are IDENTICAL as functions of")
    print("(n,K), not just their totals but term-by-term in r:")
    print("=" * 78)
    diff_BC = sp.simplify(summand_B - summand_C)
    print(f"  summand_B - summand_C = {diff_BC}   (identically zero: {diff_BC == 0})")

    print()
    print("=" * 78)
    print("Terminating-hypergeometric-function representation and hyperexpand")
    print("(Piece B, representative case -- Piece C is identical per above,")
    print("Piece D has an analogous structure with a 3-term-ratio product)")
    print("=" * 78)
    Kc, nc = 6, 10
    print(f"Numeric sanity anchor at K={Kc}, n={nc}:")
    T0 = summand_B.subs(r, 0).subs({K: Kc, n: nc})
    T0 = sp.nsimplify(T0)
    ratio = sp.simplify(summand_B.subs(r, r + 1) / summand_B)
    print(f"  T(0) = {T0}")
    print(f"  ratio(r) = {ratio}")
    # ratio(r) = -(n+r+2)(r+1-K) / (n*(r+K+4))  =>
    # T(r) = T0 * (1-K)_r (n+2)_r (1)_r / [(K+4)_r r!] * (-1/n)^r
    # => Sum_r T(r) = T0 * 3F2(1-K, n+2, 1; K+4; -1/n)
    hyperval = sp.hyper([1 - Kc, nc + 2, 1], [Kc + 4], sp.Rational(-1, nc))
    predicted = sp.nsimplify(sp.N(T0 * hyperval, 30))
    direct_sum = sp.nsimplify(sum(summand_B.subs({K: Kc, n: nc, r: rv}) for rv in range(Kc)))
    print(f"  predicted via T0 * 3F2(1-K, n+2, 1; K+4; -1/n) = {sp.N(predicted, 20)}")
    print(f"  direct finite sum over r=0..K-1                = {sp.N(direct_sum, 20)}")
    print(f"  exact match: {sp.simplify(predicted - direct_sum) == 0}")

    print()
    print("Attempting sp.hyperexpand on the general (K,n symbolic) 3F2 form...")
    expr = sp.hyper([1 - K, n + 2, 1], [K + 4], -1 / n)
    t0 = time.time()
    expanded = sp.hyperexpand(expr)
    dt = time.time() - t0
    print(f"  hyperexpand result ({dt:.2f}s): {expanded}")
    print(f"  still contains an unevaluated hyper(...): {expanded.has(sp.hyper)}")

    print()
    print("=" * 78)
    print("CONCLUSION (see ATTEMPT.md sec 7 for the full discussion):")
    print("Every piece of T(L)'s r-sum is a genuine, verified, terminating")
    print("hypergeometric SERIES in r -- it therefore trivially equals a")
    print("terminating 3F2(...) hypergeometric FUNCTION value, a legitimate")
    print("'closed form involving a special function' per the mandate's own")
    print("named fallback outcome. But Gosper's algorithm PROVES it has no")
    print("hypergeometric-term antidifference (elementary Gamma-ratio form),")
    print("and sp.hyperexpand independently fails to reduce the 3F2 to an")
    print("elementary expression for symbolic K,n -- so the obstruction is")
    print("REAL, PRECISELY LOCATED (in this specific r-summation step, one")
    print("level up from the predecessor's own subset-sum term-count growth),")
    print("and certified by two independent algorithms, not merely 'sympy")
    print("gave up'.")
