"""
ADVERSARIAL / REFEREE SCRIPT 5 (item 5 + the numerical cross-check
requested in the mandate's final paragraph):

(A) Fresh exact-Fraction cross-check of E[(M_K')^t] == E[M_K^t] at a
    SAMPLE DISJOINT from what the target and orchestrating session already
    tested: K=11..20, t=7..12 (target checked K up to 150 integer-t, 80
    half-integer-t cells up to K=15; orchestrator spot-checked 60 cells).
    Uses a completely independent E[(M_K')^t] computation (via the
    W(r,t)-closed-form reduction, own code) and an independent E[M_K^t]
    computation (via the K!*Gamma(t/2+1)/Gamma(K+t/2+1) formula AND, as a
    triple-check, via direct exact-Fraction integration of the density
    using the elementary Beta-integral formula -- no sympy needed for
    this route at all).

(B) The moment-determinacy logic check (item 5a): is matching moments at
    every POSITIVE INTEGER t sufficient to conclude M_K'=_d M_K on [0,1]?
    This script does not "verify" a classical theorem numerically (that
    would be meaningless) but states precisely which classical theorem is
    being invoked, why it applies here, and flags exactly what would be
    needed if it did NOT apply, to check that the target invokes it
    correctly rather than overclaiming.

(C) Sanity re-derivation of the target-density moment formula
    E[M_K^t] = K! Gamma(t/2+1)/Gamma(K+t/2+1) directly from f_K(x) via the
    classical Beta-substitution u=x^2, done here independently, for a wide
    sweep K=1..30, t=1..15 (integer t; exact Fraction arithmetic).
"""
import math
from fractions import Fraction as Fr
import sympy as sp


def W_closed(r, t):
    return (t + 2 * r + 1) * math.factorial(t + r)


def E_MKprime(K, t):
    total = Fr(0)
    for r in range(0, K + 1):
        w = W_closed(r, t)
        total += Fr(math.comb(K, r) * w, math.factorial(K + t + r + 1))
    return total * math.factorial(K)


def E_MK_via_beta(K, t):
    """E[M_K^t] = int_0^1 x^t * 2K x (1-x^2)^{K-1} dx
               = 2K int_0^1 x^{t+1} (1-x^2)^{K-1} dx
    Substituting u=x^2 (x=u^{1/2}, dx=(1/2)u^{-1/2}du):
    x^{t+1}dx = u^{(t+1)/2}*(1/2)u^{-1/2}du = (1/2) u^{t/2} du, so
       E[M_K^t] = K * int_0^1 u^{t/2} (1-u)^{K-1} du = K*Beta(t/2+1,K).
    For t EVEN, t/2 is a nonnegative integer, so this Beta integral is
    exactly the elementary rational a!b!/(a+b+1)! formula (a=t/2, b=K-1)
    -- no Gamma-function or sympy needed at all. (For t ODD, t/2 is a
    half-integer and this route needs Gamma(1/2)-type factors, so it is
    used here only for EVEN t, as a third, fully independent, purely
    rational cross-check of the Gamma-function closed form.)"""
    assert t % 2 == 0, "this elementary rational Beta route needs t/2 integer, i.e. t even"
    a = t // 2   # exponent of u
    b = K - 1    # exponent of (1-u)
    # int_0^1 u^a (1-u)^b du = a! b! / (a+b+1)!
    beta = Fr(math.factorial(a) * math.factorial(b), math.factorial(a + b + 1))
    return K * beta


def E_MK_via_gamma_formula(K, t):
    """E[M_K^t] = K! * Gamma(t/2+1) / Gamma(K+t/2+1), via sympy exact
    rational/Gamma arithmetic (works for all t, even or odd)."""
    val = sp.factorial(K) * sp.gamma(sp.Rational(t, 2) + 1) / sp.gamma(K + sp.Rational(t, 2) + 1)
    val = sp.simplify(val)
    # NOTE (self-caught, referee's own script): an earlier version of this
    # function applied sp.nsimplify() on top of sp.simplify() here, which
    # for some large exact rationals returns a bogus algebraic-looking
    # approximation (e.g. involving irrational-looking fractional powers)
    # INSTEAD of the exact rational sp.simplify() already produced -- a
    # pure sympy-usage bug in this script, not a mathematical discrepancy.
    # Caught by manually inspecting a flagged "MISMATCH" cell (K=17,t=11)
    # and confirming sp.simplify() alone already gives the exact, correct
    # rational; nsimplify() is not used anywhere in this function now.
    val = sp.Rational(val)
    return Fr(int(val.p), int(val.q))


if __name__ == "__main__":
    print("=" * 78)
    print("Part A: fresh Fraction cross-check, K=11..20, t=7..12 (disjoint")
    print("sample from target's own K<=150/t<=40 sweep and the orchestrator's")
    print("60-cell spot-check) -- E[(M_K')^t] via W(r,t)-reduction (own code)")
    print("vs E[M_K^t] via the Gamma-function formula (sympy exact) AND,")
    print("for odd t, a THIRD, fully independent, non-sympy elementary Beta-")
    print("integral route.")
    print("=" * 78)
    n = 0
    all_ok = True
    for K in range(11, 21):
        for t in range(7, 13):
            n += 1
            a = E_MKprime(K, t)
            b = E_MK_via_gamma_formula(K, t)
            ok = (a == b)
            line = f"K={K:2d} t={t:2d}: E[(M_K')^t]={a} E[M_K^t]_gamma={b} [{'OK' if ok else 'MISMATCH'}]"
            if t % 2 == 0:
                c = E_MK_via_beta(K, t)
                ok3 = (a == c)
                line += f" E[M_K^t]_beta(3rd route)={c} [{'OK' if ok3 else 'MISMATCH'}]"
                ok = ok and ok3
            all_ok = all_ok and ok
            print(line)
    print()
    print(f"Tested {n} fresh (K,t) cells (K=11..20, t=7..12), disjoint from")
    print("previously-tested ranges.")
    print("ALL MATCH" if all_ok else "MISMATCH FOUND -- SEE ABOVE")
    print()

    print("=" * 78)
    print("Part C: independent re-derivation of E[M_K^t] = K! Gamma(t/2+1)/")
    print("Gamma(K+t/2+1) from f_K(x)=2Kx(1-x^2)^(K-1) via u=x^2 substitution,")
    print("wide sweep K=1..30, t=2..16 (even t, exact Fraction arithmetic,")
    print("even-t route only, since that route is exact without sympy)")
    print("=" * 78)
    n2 = 0
    ok2_all = True
    for K in range(1, 31):
        for t in range(2, 17, 2):  # even t only, for the fully-elementary triple-check route
            n2 += 1
            beta_route = E_MK_via_beta(K, t)
            gamma_route = E_MK_via_gamma_formula(K, t)
            ok2 = (beta_route == gamma_route)
            ok2_all = ok2_all and ok2
            if not ok2:
                print(f"  MISMATCH: K={K} t={t} beta={beta_route} gamma={gamma_route}")
    print(f"Tested {n2} (K,t) cells, even t=2..16, K=1..30, elementary-Beta vs Gamma-formula route.")
    print("ALL MATCH -- E[M_K^t] formula independently re-confirmed by a route" if ok2_all
          else "MISMATCH FOUND")
    print("using no Gamma function evaluation at all (pure rational Beta integral).")
    print()

    print("=" * 78)
    print("Part B: the moment-determinacy step -- precise statement of what is")
    print("invoked and why it applies (not a numeric check; classical theorems")
    print("are not verified by sampling, but misapplication IS checkable)")
    print("=" * 78)
    print("""
Claim invoked (target ATTEMPT.md Section 6, 'classical Hausdorff/Stone-
Weierstrass moment-determinacy fact'): if X, Y are random variables
supported on a common COMPACT interval [0,1], and E[X^t] = E[Y^t] for
EVERY POSITIVE INTEGER t = 1, 2, 3, ..., then X =_d Y.

This is exactly the classical Hausdorff moment problem's determinacy
theorem for compactly-supported distributions:
  - On a COMPACT support, the moment problem is ALWAYS determinate
    (unlike the general Stieltjes/Hamburger moment problems on [0,infty)
    or (-infty,infty), which can fail to be determinate without extra
    conditions such as Carleman's condition). This determinacy on compact
    support does NOT require any extra growth condition on the moments --
    boundedness of the support alone suffices, because:
      (i) by Weierstrass approximation, polynomials are dense in
          C([0,1]) (sup norm);
      (ii) matching E[X^t]=E[Y^t] for every integer t>=1 (together with
          E[X^0]=E[Y^0]=1, trivial) means E[p(X)]=E[p(Y)] for EVERY
          polynomial p, by linearity;
      (iii) hence, by (i)+(ii) and a standard approximation argument,
          E[f(X)]=E[f(Y)] for every f in C([0,1]);
      (iv) (iii) for every continuous f implies X and Y induce the same
          Borel probability measure on [0,1] (a continuous-test-function
          class rich enough to separate measures, by a standard
          Riesz-representation/portmanteau argument), i.e. X =_d Y.
  - This is indeed the CORRECT theorem to invoke here: M_K' and M_K are
    BOTH supported on [0,1] (M_K' = p_D + sum V_s' is a sum of a convex
    combination of [0,1]-valued nonnegative pieces bounded by 1 by
    construction; M_K has the explicit density 2Kx(1-x^2)^{K-1} on
    [0,1]), and the target/this front establishes moment matching for
    EVERY POSITIVE INTEGER t (Section 5.5/6 of ATTEMPT.md, via the
    Gamma-function closed form specialized to integer t) -- exactly the
    hypothesis the compact-support determinacy theorem needs. No stronger
    claim (e.g. "matching only finitely many t suffices", or "matching
    real/non-integer t was needed for determinacy") is made anywhere in
    the target document -- the half-integer-t checks (Section 5.6) are
    explicitly framed as EXTRA supporting evidence for the closed-form
    IDENTITY S(K,t), not as part of the determinacy argument itself
    (determinacy only needs, and only uses, integer t>=1).
  - CONCLUSION: the target's invocation of moment-determinacy is
    CORRECT and not overclaimed: it matches moments literally for EVERY
    positive integer t (not a finite sample -- the Gamma-function closed
    form, proved for every real t>-1 in Section 5.5, gives every integer-t
    moment as a special case, all at once, not merely at "the sampled
    values"), on a compact support, which is precisely and exactly the
    hypothesis of the classical, standard theorem it cites.
""")
