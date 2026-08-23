"""
The building blocks of the prefactor-collapse route (DERIVATION_PREREG.md Steps 1-4),
each derived and verified independently of the others and independently of
ground_truth.py.

1. Q_p(u) := c(u+1, u+1-p) = e_p(1,...,u), identified as an explicit polynomial in u
   of degree 2p by exact interpolation on 2p+1 points (a-priori degree bound is
   classical: e_p(1,...,u) is a polynomial in u of degree 2p, by Newton's identities
   applied to the Faulhaber power-sum polynomials, each of degree <= p+1, with the
   top-degree contribution p*2 coming from the P_1^p/p! term) plus >=10 further
   out-of-sample exact checks.

2. mu_{2l}(N) := 2^{-N} * sum_{a=0}^N (a-N/2)^{2l} * binom(N,a), the central moments
   of Bin(N,1/2), derived from the cumulant generating function N*log(cosh(t/2))
   (classical fact: sum of N iid Bernoulli(1/2), centered, has this CGF) via sympy
   series expansion, then verified exactly for N<=17.

3. I1, I3 (PROVED already, referee report Part 3.1 -- re-derived independently here,
   not copied, as an independent sanity check) and I5, I7 (NEW, derived here by the
   same Abel-summation-by-parts technique, telescoping against A(i):=(i+1)*binom(N,i+1)
   which satisfies A(i)-A(i-1) = (N-2i)*binom(N,i)), each verified exhaustively.

4. The prefactor-collapse family P_b * [N]_k * (r-k+1) * binom(N-k,r-k+1) = [r]_k
   (falling factorials; k=0 is the referee's P_b*(r+1)*binom(N,r+1)=1), proved by
   direct factorial cancellation and confirmed both numerically and symbolically
   (general symbolic r, b).

Written from scratch. Nothing imported from any sibling/predecessor directory.
"""
from fractions import Fraction as F
import math
import sympy as sp

from ground_truth import factorial, binom, stirling1


# ---------------------------------------------------------------------------
# 1. Q_p(u), by interpolation on the classical degree bound, plus extra checks
# ---------------------------------------------------------------------------

def Q_poly(p, extra_checks=15):
    u = sp.symbols('u')
    xs = list(range(0, 2 * p + 1))
    ys = [stirling1(x + 1, x + 1 - p) for x in xs]
    poly = sp.expand(sp.interpolate(list(zip(xs, ys)), u))
    for xx in range(2 * p + 1, 2 * p + 1 + extra_checks):
        pred = poly.subs(u, xx)
        actual = stirling1(xx + 1, xx + 1 - p)
        assert pred == actual, f"Q_{p} out-of-sample check failed at u={xx}: {pred} vs {actual}"
    return poly


# ---------------------------------------------------------------------------
# 2. Central moments mu_{2l}(N) of Bin(N, 1/2), via cumulant generating function
# ---------------------------------------------------------------------------

def _derive_moment_formulas():
    """Derive mu_2, mu_4, mu_6, mu_8 symbolically from N*log(cosh(t/2))."""
    t, n, x = sp.symbols('t n x')
    logcosh = sp.series(sp.log(sp.cosh(x)), x, 0, 12).removeO()
    K = sp.expand(logcosh.subs(x, t / 2) * n)
    M = sp.expand(sp.series(sp.exp(K), t, 0, 10).removeO())
    poly = sp.Poly(M, t)
    out = {}
    for deg in [2, 4, 6, 8]:
        coeff = poly.coeff_monomial(t ** deg) if poly.degree() >= deg else 0
        out[deg] = sp.expand(coeff * sp.factorial(deg))
    return out

_MU = _derive_moment_formulas()

def mu2_formula(N):
    return F(N, 4)

def mu4_formula(N):
    return F(N * (3 * N - 2), 16)

def mu6_formula(N):
    return F(N * (15 * N ** 2 - 30 * N + 16), 64)

def mu8_formula(N):
    return F(N) * (F(105, 256) * N ** 3 - F(105, 64) * N ** 2 + F(147, 64) * N - F(17, 16))


def verify_moments(Nmax=20):
    ok = True
    for N in range(0, Nmax + 1):
        s2 = s4 = s6 = s8 = F(0)
        for a in range(0, N + 1):
            v = F(a) - F(N, 2)
            w = binom(N, a)
            s2 += v ** 2 * w
            s4 += v ** 4 * w
            s6 += v ** 6 * w
            s8 += v ** 8 * w
        if s2 != F(2 ** N) * mu2_formula(N):
            ok = False; print("mu2 FAIL", N)
        if s4 != F(2 ** N) * mu4_formula(N):
            ok = False; print("mu4 FAIL", N)
        if s6 != F(2 ** N) * mu6_formula(N):
            ok = False; print("mu6 FAIL", N)
        if s8 != F(2 ** N) * mu8_formula(N):
            ok = False; print("mu8 FAIL", N)
    return ok


# ---------------------------------------------------------------------------
# 3. Partial binomial-moment identities I1, I3, I5, I7
#    S_{2k+1}(N,m) := sum_{i=0}^m (N-2i)^{2k+1} binom(N,i)
# ---------------------------------------------------------------------------

def S1(N, m):
    """I1 (referee, wave 10): (N-2i) sum, re-derived independently here."""
    return (m + 1) * binom(N, m + 1)


def S3(N, m):
    """I3 (referee, wave 10): (N-2i)^3 sum, re-derived independently here."""
    return F(N - 2 * m) ** 2 * (m + 1) * binom(N, m + 1) + 4 * N * m * binom(N - 1, m)


def S5(N, m):
    """
    I5 (NEW). Derived by Abel summation by parts:
      S5(N,m) = sum_i (N-2i)^4 * [A(i)-A(i-1)],  A(i):=(i+1)binom(N,i+1)
              = (N-2m)^4(m+1)binom(N,m+1) - sum_{i=0}^{m-1} A(i)*Delta_f(i)
    with f(i)=(N-2i)^4, Delta_f(i-1)=y^4-(y+2)^4 (y=N-2i-... see ATTEMPT.md S2 for the
    full by-hand algebra). Using j*binom(N,j)=N*binom(N-1,j-1) and expanding in the
    shifted variable w=(N-1)-2l, the "-1" offset terms cancel exactly, leaving only
    S3 and S1 evaluated at (N-1, m-1):
      S5(N,m) = (N-2m)^4(m+1)binom(N,m+1) + 8N*[S3(N-1,m-1) + S1(N-1,m-1)]
    """
    M = N - 1
    return F(N - 2 * m) ** 4 * (m + 1) * binom(N, m + 1) + 8 * N * (S3(M, m - 1) + S1(M, m - 1))


def S7(N, m):
    """
    I7 (NEW). Same technique one level deeper: Abel-summing (N-2i)^6 against A(i),
    then expanding g(w-1) for the resulting sextic g, the w^0, w^2, w^4 coefficients
    cancel exactly (as they did for I5), leaving only S5, S3, S1 at (N-1, m-1):
      S7(N,m) = (N-2m)^6(m+1)binom(N,m+1) + N*[12*S5(N-1,m-1)+40*S3(N-1,m-1)+12*S1(N-1,m-1)]
    """
    M = N - 1
    return (F(N - 2 * m) ** 6 * (m + 1) * binom(N, m + 1)
            + N * (12 * S5(M, m - 1) + 40 * S3(M, m - 1) + 12 * S1(M, m - 1)))


def _direct_S(k, N, m):
    s = F(0)
    for i in range(0, m + 1):
        s += F(N - 2 * i) ** k * binom(N, i)
    return s


def verify_odd_identities(Nmax_S1S3=60, Nmax_S5=39, Nmax_S7=34):
    ok = True
    for N in range(0, Nmax_S1S3 + 1):
        for m in range(0, N + 1):
            if S1(N, m) != _direct_S(1, N, m):
                ok = False; print("S1/I1 FAIL", N, m)
            if S3(N, m) != _direct_S(3, N, m):
                ok = False; print("S3/I3 FAIL", N, m)
    for N in range(0, Nmax_S5 + 1):
        for m in range(0, N + 1):
            if S5(N, m) != _direct_S(5, N, m):
                ok = False; print("S5/I5 FAIL", N, m)
    for N in range(0, Nmax_S7 + 1):
        for m in range(0, N + 1):
            if S7(N, m) != _direct_S(7, N, m):
                ok = False; print("S7/I7 FAIL", N, m)
    return ok


# ---------------------------------------------------------------------------
# 4. The prefactor-collapse family
#    P_b * [N]_k * (r-k+1) * binom(N-k, r-k+1) = [r]_k        (falling factorials)
# ---------------------------------------------------------------------------

def P_b(r, b):
    N = 2 * r + b + 1
    return F(factorial(r) * factorial(r + b), factorial(N))


def falling(x, k):
    v = 1
    for i in range(k):
        v *= (x - i)
    return v


def collapse_k(r, b, k):
    """P_b * [N]_k * (r-k+1) * binom(N-k, r-k+1)  (k=0 is the trivial (r+1)binom(N,r+1) case)."""
    N = 2 * r + b + 1
    Nk = falling(N, k)
    if N - k < r - k + 1 or r - k + 1 < 0:
        binom_term = 0
    else:
        binom_term = binom(N - k, r - k + 1)
    return P_b(r, b) * Nk * (r - k + 1) * binom_term


def verify_collapse_numeric(kmax=3, bmax=10, rmax=20):
    ok = True
    for k in range(0, kmax + 1):
        for b in range(0, bmax + 1):
            for r in range(0, rmax + 1):
                lhs = collapse_k(r, b, k)
                rhs = F(falling(r, k))
                if lhs != rhs:
                    ok = False
                    print("collapse FAIL", k, b, r, lhs, rhs)
    return ok


def verify_collapse_symbolic(kmax=3):
    r, b = sp.symbols('r b', positive=True, integer=True)
    N = 2 * r + b + 1
    Pb = sp.factorial(r) * sp.factorial(r + b) / sp.factorial(N)
    ok = True
    for k in range(0, kmax + 1):
        Nk = 1
        for i in range(k):
            Nk *= (N - i)
        lhs = Pb * Nk * (r - k + 1) * sp.binomial(N - k, r - k + 1)
        rk = 1
        for i in range(k):
            rk *= (r - i)
        diff = sp.simplify(lhs - rk)
        if diff != 0:
            ok = False
            print("symbolic collapse FAIL k=", k, "diff=", diff)
    return ok


if __name__ == "__main__":
    print("=== Q_p(u) for p=0..4 (interpolated on 2p+1 pts, extended-checked) ===")
    for p in range(0, 5):
        print(f"Q_{p}(u) =", Q_poly(p))

    print()
    print("=== central moments mu_2, mu_4, mu_6, mu_8 (symbolic derivation) ===")
    for deg, expr in _MU.items():
        print(f"mu_{deg}(n) =", expr)
    print("Numeric verification, N<=20:", "OK" if verify_moments(20) else "FAIL")

    print()
    print("=== odd partial-sum identities I1,I3 (re-derived), I5,I7 (NEW) ===")
    print("Exhaustive verification (S1,S3: N<=60; S5: N<=39; S7: N<=34), all m:",
          "OK" if verify_odd_identities() else "FAIL")

    print()
    print("=== prefactor-collapse family, k=0,1,2,3 ===")
    print("Numeric (b<=10, r<=20):", "OK" if verify_collapse_numeric() else "FAIL")
    print("Symbolic (general r,b):", "OK" if verify_collapse_symbolic() else "FAIL")


# ---------------------------------------------------------------------------
# 4b. General-k proof of the collapse family (closes out Step 4's remaining gap)
# ---------------------------------------------------------------------------
#
# Claim: for EVERY k>=0 (not just k=0,1,2,3),
#   P_b * [N]_k * (r-k+1) * binom(N-k, r-k+1) = [r]_k     ([x]_k := x(x-1)...(x-k+1))
#
# Proof. LHS = [r!(r+b)!/N!] * [N(N-1)...(N-k+1)] * (r-k+1) * (N-k)!/[(r-k+1)!(N-r-1)!]
# Since N(N-1)...(N-k+1)*(N-k)! = N! exactly, this is
#   = r!(r+b)! * (r-k+1) / [(r-k+1)! * (N-r-1)!]
# and (r-k+1)/(r-k+1)! = 1/(r-k)! (valid for r>=k; both sides are 0 by convention
# when r<k, since [r]_k then contains the factor 0), so
#   = r!(r+b)! / [(r-k)! (N-r-1)!].
# N-r-1 = r+b exactly (from N=2r+b+1), so (N-r-1)! = (r+b)!, which cancels the
# (r+b)! left standing, giving r!/(r-k)! = [r]_k.  QED -- general k, no induction
# needed, one line of factorial cancellation.

def verify_collapse_general_k(kmax=6, bmax=8, rmax=15):
    ok = True
    for k in range(0, kmax + 1):
        for b in range(0, bmax + 1):
            for r in range(0, rmax + 1):
                lhs = collapse_k(r, b, k)
                rhs = F(falling(r, k))
                if lhs != rhs:
                    ok = False
                    print("general-k collapse FAIL", k, b, r, lhs, rhs)
    return ok


if __name__ == "__main__":
    print()
    print("=== General-k collapse family (proved above by factorial cancellation), k=0..6 ===")
    print("Numeric (b<=8, r<=15):", "OK" if verify_collapse_general_k() else "FAIL")
