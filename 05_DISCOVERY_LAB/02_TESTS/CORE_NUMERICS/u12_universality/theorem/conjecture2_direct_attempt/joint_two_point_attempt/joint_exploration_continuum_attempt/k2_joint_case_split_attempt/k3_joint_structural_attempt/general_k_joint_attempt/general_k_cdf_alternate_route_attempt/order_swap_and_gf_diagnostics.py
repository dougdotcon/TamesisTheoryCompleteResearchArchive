"""
Two supplementary diagnostic explorations, sharpening WHY the W-collapsed
sum (gosper_certification_W.py) still fails to close for symbolic K, and
whether the obstruction is really "about K" or something more structural.

DIAGNOSTIC 1 (order-swap control): instead of summing over W first (this
front's main route) and leaving the outer r-assembly (sum_{r=0}^{K}) for
later, what if the FULL combined term (including the C(K,r)*r!/n^{r+1}
outer-assembly weight) is summed over r FIRST, for FIXED W? Because
C(W,r) vanishes automatically for r>W (standard binomial convention),
the r-sum can run over its own full natural range r=0..K with no
case-split needed. Tested here directly: this order FAILS Gosper
already at CONCRETE K (not just symbolic K) -- strictly worse than the
W-first order this front's main route uses. This confirms (a) that
W-first is the correct/better order to attempt, matching the pattern
Estagio 39/44 both found (their own obstructions also only bite at
symbolic K, not concrete K -- the W-first order matches that pattern,
the r-first order does not even reach it), and (b) that the outer
r-assembly is independently, structurally hard on its own terms --
consistent with Estagio 39's own historical obstruction living in
exactly this same style of r-indexed sum for the simpler quantity
P_nn(n,K).

DIAGNOSTIC 2 (generating-function-in-K, mandate avenue (b)): does
folding K into a generating-function marker x (turning the
symbolic-DEGREE binomial C(n-W+r-1,K) into an ordinary generating
function coefficient) make the resulting W-sum Gosper-summable for
(x,n,r) ALL symbolic? Uses the clean OGF identity (proved below):
    sum_{K=0}^infty InnerJ(W;K) x^K = (W*x+r)*(1+x)^{n-W+r-1}
Answer: YES for r CONCRETE (any r=0..5 tested, x,n symbolic) -- but the
obstruction reappears, in the SAME form, once r is ALSO left symbolic
(with x,n symbolic, K entirely gone). This shows the true obstruction is
not "K is hard" per se, but "a symbolic-degree binomial coefficient
whose degree is ALSO a free parameter coupled to the summation variable's
own combinatorics" -- and this front's construction has exactly TWO such
parameters (K and r) trading places under the K-to-x substitution. This
is new, sharper structural content beyond either Estagio 39's or Estagio
44's own diagnoses.
"""
import time
import sympy as sp
from sympy.concrete.gosper import gosper_term
from sympy.simplify import hypersimp
from fractions import Fraction
import sys
sys.path.insert(0, '.')
from reference_Sr_double_sum import InnerJ_direct

n, r, W, K = sp.symbols('n r W K', integer=True, positive=True)


def verify_InnerJ_OGF_numerically():
    print()
    print("  Direct numeric check of the InnerJ OGF identity itself (not just")
    print("  the abstract binomial theorem), via COEFFICIENT EXTRACTION:")
    print("  [x^K] (W*x+r)*(1+x)^(n-W+r-1) ?= InnerJ_true(W;n,K,r), for every")
    print("  K in its valid range r<=K<=n-W+r, at several concrete (n,W,r).")
    print()
    print("  (Self-disclosed bug in an earlier draft of this exact check: a")
    print("  first attempt compared a TRUNCATED SUM sum_{K=r}^{Kmax}")
    print("  InnerJ_true(K)*x^K against the FULL closed-form polynomial")
    print("  (W*x+r)*(1+x)^(n-W+r-1) directly -- but that polynomial's low-order")
    print("  x^0,...,x^{r-1} coefficients are generically NONZERO (they come")
    print("  from the same algebraic formula continued to K<r, where it is not")
    print("  combinatorially meaningful as InnerJ), so a sum starting at K=r")
    print("  necessarily disagreed with the full polynomial by exactly that")
    print("  missing low-order part -- a verification-range bug, not an error")
    print("  in the underlying identity. Fixed below by comparing COEFFICIENTS")
    print("  one K at a time, which is well-defined and correct for every")
    print("  K>=r regardless of what happens for K<r.)")
    x = sp.symbols('x')
    all_ok = True
    for (nv, Wv, rv) in [(12, 5, 2), (10, 3, 1), (9, 4, 0), (14, 6, 3)]:
        M = nv - Wv + rv - 1
        poly = sp.Poly(sp.expand((Wv * x + rv) * (1 + x) ** M), x)
        for Kv in range(rv, nv - Wv + rv + 1):
            coeff = poly.coeff_monomial(x ** Kv) if Kv <= poly.degree() else 0
            true_val = InnerJ_direct(nv, Kv, rv, Wv, 0)
            ok = (coeff == true_val)
            all_ok = all_ok and ok
            if not ok:
                print(f"    MISMATCH n={nv} W={Wv} r={rv} K={Kv}: "
                      f"[x^K]GF={coeff} InnerJ_true={true_val}")
    print(f"  InnerJ OGF identity verified via coefficient extraction "
          f"(many n,W,r,K): {all_ok}")
    return all_ok


def diagnostic_1_order_swap():
    print("DIAGNOSTIC 1: order-swap control -- sum over r FIRST (fixed W)")
    print("-" * 70)

    def RTerm(Kval_or_symbol):
        N = n - W
        A1 = sp.binomial(N + r - 1, Kval_or_symbol - 1)
        A2 = sp.binomial(N + r - 1, Kval_or_symbol)
        InnerJ = W * A1 + r * A2
        cW = sp.binomial(W, r)
        outer = sp.binomial(Kval_or_symbol, r) * sp.factorial(r) / n ** (r + 1)
        return sp.simplify(outer * cW * InnerJ)

    print("  Concrete K, r as the summation variable:")
    any_concrete_succeeds = False
    for Kval in [1, 2, 3, 4, 5]:
        term = RTerm(sp.Integer(Kval))
        ratio_ok = hypersimp(term, r) is not None
        t0 = time.time()
        res = gosper_term(term, r)
        dt = time.time() - t0
        print(f"    K={Kval}: hypersimp recognizes term = {ratio_ok}; "
              f"gosper_term(in r) = {'FOUND' if res is not None else 'None'}   [{dt:.2f}s]")
        any_concrete_succeeds = any_concrete_succeeds or (res is not None)
    print(f"  Any concrete K succeeded via r-first order: {any_concrete_succeeds}")
    print("  (Contrast: W-first order (gosper_certification_W.py) succeeds")
    print("  at EVERY concrete K=1..7 tested. r-first fails already at every")
    print("  concrete K tried here -- a strictly worse order, confirming")
    print("  W-first is the structurally correct organization to attempt.)")
    return not any_concrete_succeeds


def prove_K_generating_function():
    print()
    print("Sub-step: proving the OGF identity sum_K InnerJ(W;K) x^K =")
    print("(W*x+r)*(1+x)^(n-W+r-1), by the binomial theorem, symbolically.")
    print("-" * 70)
    xg = sp.symbols('xg', positive=True)
    Kp = sp.symbols('Kp', integer=True, nonnegative=True)
    Msym = sp.symbols('M', integer=True, nonnegative=True)
    # binomial theorem: sum_{K=0}^{M} C(M,K) x^K = (1+x)^M
    lhs = sp.summation(sp.binomial(Msym, Kp) * xg ** Kp, (Kp, 0, Msym))
    rhs = (1 + xg) ** Msym
    diff_raw = sp.simplify(lhs - rhs)
    print(f"  sp.summation(C(M,K)*x^K, K=0..M) - (1+x)^M = {diff_raw}")
    print(f"  NOTE (self-disclosed): sp.summation's symbolic-M result carries a")
    print(f"  Piecewise convergence condition (|x|<=1) that is a cosmetic")
    print(f"  artifact of sympy's default hypergeometric-series summation")
    print(f"  machinery -- NOT a genuine restriction, since the sum is finite")
    print(f"  (M a nonnegative integer, no convergence question can arise).")
    print(f"  Proper verification: check the identity holds for EVERY concrete")
    print(f"  M as an exact polynomial identity in x (this is literally Newton's")
    print(f"  Binomial Theorem for nonnegative integer exponents, elementary):")
    ok = True
    for Mval in range(0, 12):
        lhs_c = sum(sp.binomial(Mval, kk) * xg ** kk for kk in range(0, Mval + 1))
        rhs_c = (1 + xg) ** Mval
        d = sp.expand(lhs_c - rhs_c)
        if d != 0:
            ok = False
            print(f"    MISMATCH at M={Mval}: {d}")
    print(f"  Verified as an exact polynomial identity in x for M=0..11: {ok}")
    print(f"  (This IS the OGF identity used, with M := n-W+r-1, applied twice --")
    print(f"  once for the C(.,K-1) piece via the standard index shift, once")
    print(f"  directly for the C(.,K) piece.)")
    print(f"  PROVED (elementary Binomial Theorem, concrete-M spot-checked): {ok}")
    return ok


def diagnostic_2_gf_in_K():
    print()
    print("DIAGNOSTIC 2: generating-function-in-K (mandate avenue (b))")
    print("-" * 70)
    xg = sp.symbols('xg', positive=True)

    def GF_term(rval_or_symbol):
        Tterm = sp.binomial(W, rval_or_symbol) * (W * xg + rval_or_symbol) * \
            (1 + xg) ** (n - W + rval_or_symbol - 1)
        return sp.simplify(Tterm)

    print("  K eliminated (folded into GF marker x). r CONCRETE, x & n symbolic:")
    all_concrete_r_ok = True
    for rv in [0, 1, 2, 3, 4, 5]:
        term = GF_term(rv)
        t0 = time.time()
        res = gosper_term(term, W)
        dt = time.time() - t0
        ok = res is not None
        all_concrete_r_ok = all_concrete_r_ok and ok
        print(f"    r={rv}: gosper_term = {'FOUND' if ok else 'None'}   [{dt:.2f}s]")
    print(f"  All concrete r (0..5) Gosper-summable with K eliminated via GF: {all_concrete_r_ok}")

    print()
    print("  r ALSO symbolic (x, n, r all free -- K is entirely gone from this term):")
    term_rsym = GF_term(r)
    ratio = hypersimp(term_rsym, W)
    ratio_ok = ratio is not None
    print(f"    hypersimp recognizes term as hypergeometric: {ratio_ok}")
    t0 = time.time()
    res = gosper_term(term_rsym, W)
    dt = time.time() - t0
    is_cert = (res is None) and ratio_ok
    print(f"    gosper_term(term, W), r symbolic -> {res}   [{dt:.2f}s]")
    print(f"    Genuine certificate (hypersimp succeeded, algorithm ran, None "
          f"returned): {is_cert}")
    return all_concrete_r_ok, is_cert


if __name__ == "__main__":
    d1_ok = diagnostic_1_order_swap()
    gf_ok = prove_K_generating_function()
    gf_numeric_ok = verify_InnerJ_OGF_numerically()
    d2_concrete_ok, d2_symbolic_cert = diagnostic_2_gf_in_K()
    print()
    print("=" * 70)
    print("SUMMARY")
    print(f"  Diagnostic 1 (r-first order fails even at concrete K): {d1_ok}")
    print(f"  OGF-in-K identity proved (elementary + numeric): {gf_ok and gf_numeric_ok}")
    print(f"  Diagnostic 2 (GF-marked W-sum succeeds for r CONCRETE): {d2_concrete_ok}")
    print(f"  Diagnostic 2 (GF-marked W-sum fails once r is ALSO symbolic, genuine): {d2_symbolic_cert}")
    print()
    print("Interpretation: folding K into a generating-function marker x removes")
    print("K's own symbolic-degree-binomial obstruction cleanly, but the SAME")
    print("kind of obstruction reappears on r once r is also left symbolic. The")
    print("obstruction is not specifically 'about K' -- it is about having TWO")
    print("simultaneous free 'family-size' parameters (K and r) each entering a")
    print("binomial coefficient's DEGREE while also coupling to the summation")
    print("variable. This is a sharper structural diagnosis than either Estagio")
    print("39's or Estagio 44's own (each of which only ever had ONE such")
    print("parameter -- K alone -- left symbolic at the point of certification).")
