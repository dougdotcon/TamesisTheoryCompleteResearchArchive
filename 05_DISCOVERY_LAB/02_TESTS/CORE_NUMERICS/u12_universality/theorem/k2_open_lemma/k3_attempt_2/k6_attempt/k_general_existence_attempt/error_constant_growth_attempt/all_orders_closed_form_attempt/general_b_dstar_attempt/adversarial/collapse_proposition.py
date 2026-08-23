"""
Independent re-derivation and verification of the general-k prefactor-collapse
proposition (ATTEMPT.md sec 3.4):

  P_b * [N]_k * (r-k+1) * C(N-k, r-k+1) = [r]_k     for every k>=0,

  N := 2r+b+1, P_b := r!(r+b)!/N!, [x]_k := x(x-1)...(x-k+1) (falling
  factorial), both sides 0 by convention when r<k.

Re-derivation (redone from scratch below, matching the document's one-line
proof step by step -- see referee report prose for the write-up):

  [N]_k * (N-k)! = N!  exactly (definition of falling factorial), so

  P_b [N]_k (r-k+1) C(N-k,r-k+1)
    = (r!(r+b)!/N!) * N! * (r-k+1) / [ (r-k+1)! (N-k-(r-k+1))! ]
    = r!(r+b)! (r-k+1) / [ (r-k+1)! (N-r-1)! ]
    = r!(r+b)! / [ (r-k)! (N-r-1)! ]          [since (r-k+1)/(r-k+1)!=1/(r-k)!]

  and N-r-1 = r+b EXACTLY (from N=2r+b+1), so (N-r-1)!=(r+b)! cancels the
  (r+b)! in the numerator, leaving r!/(r-k)! = [r]_k.  QED

This script checks: (1) the intermediate identity N-r-1=r+b algebraically,
(2) the full collapse numerically over a much larger grid than the document
used (k up to 20, b up to 40, r up to 80), (3) symbolically for general
r,b (sympy, k up to 15), (4) the r<k edge case specifically and exhaustively,
(5) edge cases k=0, k>N (degenerate), r=0.
"""
from fractions import Fraction
import sympy as sp


def binom_conv(n, k):
    """C(n,k) with the standard convention C(n,k)=0 if k<0 or k>n, for n>=0
    integer. (For n<0 we do not need it here -- N-k is always used with
    N>=k>=0 in this front's route, but we still guard against surprises.)"""
    if n < 0:
        return Fraction(0)
    if k < 0 or k > n:
        return Fraction(0)
    num = 1
    for i in range(k):
        num *= (n - i)
    den = 1
    for i in range(1, k + 1):
        den *= i
    return Fraction(num, den)


def fact(n):
    if n < 0:
        raise ValueError("factorial of negative")
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def falling(x, k):
    """[x]_k = x(x-1)...(x-k+1), works for any integer x (can be negative or
    less than k -- standard falling-factorial convention, will naturally
    include a zero factor when 0<=x<k)."""
    p = 1
    for i in range(k):
        p *= (x - i)
    return p


def P_b(r, b):
    N = 2 * r + b + 1
    return Fraction(fact(r) * fact(r + b), fact(N))


def lhs(k, r, b):
    N = 2 * r + b + 1
    Nk_falling = falling(N, k)  # [N]_k, could involve N-k+1..N; N>=k always here since N=2r+b+1>=r+1>k typically, but compute generally
    c = binom_conv(N - k, r - k + 1)  # convention handles r-k+1<0 -> 0, and N-k<0 impossible here since N-k=2r+b+1-k
    return P_b(r, b) * Nk_falling * (r - k + 1) * c


def rhs(k, r):
    return Fraction(falling(r, k))


def check_identity_N_minus_r_minus_1(r_max, b_max):
    fails = 0
    checks = 0
    for r in range(0, r_max + 1):
        for b in range(0, b_max + 1):
            N = 2 * r + b + 1
            checks += 1
            if N - r - 1 != r + b:
                fails += 1
                print("FAIL N-r-1=r+b", r, b, N)
    print(f"check_identity_N_minus_r_minus_1: {checks} checks, {fails} failures")
    return fails


def numeric_sweep(k_max, r_max, b_max):
    fails = 0
    checks = 0
    for k in range(0, k_max + 1):
        for r in range(0, r_max + 1):
            for b in range(0, b_max + 1):
                L = lhs(k, r, b)
                R = rhs(k, r)
                checks += 1
                if L != R:
                    fails += 1
                    print(f"FAIL k={k} r={r} b={b}: lhs={L} rhs={R}")
    print(f"numeric_sweep(k_max={k_max},r_max={r_max},b_max={b_max}): "
          f"{checks} checks, {fails} failures")
    return fails, checks


def rk_edge_case_focus(k_max, b_max):
    """Focus specifically on r<k (the edge case the document itself flags
    as needing most scrutiny), including r=0 with k>0."""
    fails = 0
    checks = 0
    for k in range(1, k_max + 1):
        for r in range(0, k):  # r < k strictly
            for b in range(0, b_max + 1):
                L = lhs(k, r, b)
                R = rhs(k, r)
                checks += 1
                if L != 0 or R != 0:
                    fails += 1
                    print(f"FAIL (r<k edge) k={k} r={r} b={b}: lhs={L} rhs={R} "
                          f"(expected both 0)")
    print(f"rk_edge_case_focus(k_max={k_max},b_max={b_max}): "
          f"{checks} checks (all should have lhs=rhs=0), {fails} failures")
    return fails


def symbolic_general_rb(k_max):
    """Symbolic verification for GENERAL symbolic r,b (not just concrete
    numbers), k=0..k_max, via sympy.simplify on the difference. This proves
    the identity as a rational-function identity in r,b for each concrete k
    (the k-dependence itself is handled by the by-hand general proof above,
    reproduced in the referee report)."""
    r, b = sp.symbols('r b', positive=True)
    N = 2 * r + b + 1
    Pb = sp.factorial(r) * sp.factorial(r + b) / sp.factorial(N)
    fails = 0
    for k in range(0, k_max + 1):
        Nk = sp.Fraction if False else None
        # [N]_k as a product (works symbolically as a product of k terms)
        Nk_falling = sp.prod([N - i for i in range(k)]) if k > 0 else 1
        Cnk = sp.binomial(N - k, r - k + 1)
        L = Pb * Nk_falling * (r - k + 1) * Cnk
        Rk = sp.prod([r - i for i in range(k)]) if k > 0 else 1
        diff = sp.simplify(L - Rk)
        ok = (diff == 0)
        if not ok:
            fails += 1
            print(f"SYMBOLIC FAIL k={k}: L-R simplifies to {diff}")
        else:
            print(f"symbolic OK k={k}")
    print(f"symbolic_general_rb(k_max={k_max}): {k_max+1} k-values checked, "
          f"{fails} failures")
    return fails


def k_greater_than_N_case(r_max, b_max, k_extra=5):
    """What happens when k > N (so [N]_k contains a factor N-N=0 among its
    terms, and separately k > r trivially forces the r<k branch)? Check the
    identity is not silently wrong there either -- both sides must be 0."""
    fails = 0
    checks = 0
    for r in range(0, r_max + 1):
        for b in range(0, b_max + 1):
            N = 2 * r + b + 1
            for k in range(N, N + k_extra + 1):
                L = lhs(k, r, b)
                R = rhs(k, r) if r >= k else Fraction(0)
                # rhs(k,r) with r<k already yields 0 via falling() naturally
                Rv = rhs(k, r)
                checks += 1
                if L != Rv:
                    fails += 1
                    print(f"FAIL k>=N case: k={k} N={N} r={r} b={b}: lhs={L} rhs={Rv}")
    print(f"k_greater_than_N_case: {checks} checks, {fails} failures")
    return fails


if __name__ == "__main__":
    print("=" * 70)
    f0 = check_identity_N_minus_r_minus_1(r_max=200, b_max=200)
    print("=" * 70)
    f1, n1 = numeric_sweep(k_max=20, r_max=80, b_max=40)
    print("=" * 70)
    f2 = rk_edge_case_focus(k_max=25, b_max=40)
    print("=" * 70)
    f3 = symbolic_general_rb(k_max=15)
    print("=" * 70)
    f4 = k_greater_than_N_case(r_max=15, b_max=10, k_extra=6)
    print("=" * 70)
    total = f0 + f1 + f2 + f3 + f4
    print(f"TOTAL FAILURES: {total}")
