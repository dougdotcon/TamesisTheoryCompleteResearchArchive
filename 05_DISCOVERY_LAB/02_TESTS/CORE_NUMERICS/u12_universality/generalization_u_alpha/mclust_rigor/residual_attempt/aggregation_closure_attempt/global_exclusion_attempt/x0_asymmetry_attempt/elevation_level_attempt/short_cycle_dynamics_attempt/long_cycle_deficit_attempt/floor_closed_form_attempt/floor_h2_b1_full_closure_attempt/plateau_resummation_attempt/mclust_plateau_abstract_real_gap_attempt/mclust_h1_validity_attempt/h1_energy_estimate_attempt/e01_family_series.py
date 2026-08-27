"""
e01_family_series.py -- FRESH, independent implementation of the (P,Q)-family
series recursion for Phi(s,g), Psi(s,g), built entirely from the prose
recursion quoted (identically) in plateau_resummation_attempt/ATTEMPT.md Sec.1.1
and mclust_h1_validity_attempt/ATTEMPT.md Sec.0/Sec.3.1 (required reading).

No .py file from any ancestor front was opened, read, or imported. This module
is written from scratch against the mathematical recursion only.

Representation: each a_k(s), b_k(s) lies in the family
    F = { P(s) + Q(s) * erfcx(s*sqrt(c/2)) : P, Q polynomials }
and is represented as a pair of coefficient lists (P, Q) (lowest degree first,
mpmath mpf coefficients), i.e. a_k(s) = sum_j P[j] s^j + erfcx(s*sqrt(c/2)) * sum_j Q[j] s^j.

Recursion (verbatim from required reading):
    a_0 = 1, b_0 = 0
    a_1(s) = -c
    b_1(s) = sqrt(pi c/2) * erfcx(s sqrt(c/2))
    a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
    b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
    w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
"""

import mpmath as mp


# ----------------------------------------------------------------------
# Polynomial arithmetic (lists of mpf, lowest degree first)
# ----------------------------------------------------------------------

def p_zero():
    return [mp.mpf(0)]


def p_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def p_add(p, q):
    n = max(len(p), len(q))
    out = [mp.mpf(0)] * n
    for i, c in enumerate(p):
        out[i] += c
    for i, c in enumerate(q):
        out[i] += c
    return p_trim(out)


def p_scale(p, a):
    return p_trim([a * c for c in p])


def p_sub(p, q):
    return p_add(p, p_scale(q, mp.mpf(-1)))


def p_deriv(p):
    if len(p) <= 1:
        return p_zero()
    return p_trim([i * p[i] for i in range(1, len(p))])


def p_mul_s(p):
    """multiply polynomial by s (shift up one degree)"""
    return p_trim([mp.mpf(0)] + list(p))


def p_mul_one_minus_s(p):
    """multiply polynomial by (1-s)"""
    return p_sub(p, p_mul_s(p))


def p_eval(p, s):
    r = mp.mpf(0)
    for c in reversed(p):
        r = r * s + c
    return r


def p_antideriv(p):
    """indefinite antiderivative with zero constant term"""
    out = [mp.mpf(0)] + [p[i] / (i + 1) for i in range(len(p))]
    return p_trim(out)


# ----------------------------------------------------------------------
# Family element: pair (P, Q) representing P(s) + Q(s)*E(s), E(s):=erfcx(s*sqrt(c/2))
# ----------------------------------------------------------------------

class FamElt:
    __slots__ = ("P", "Q")

    def __init__(self, P, Q):
        self.P = p_trim(P)
        self.Q = p_trim(Q)

    @staticmethod
    def zero():
        return FamElt(p_zero(), p_zero())

    @staticmethod
    def const(a):
        return FamElt([mp.mpf(a)], p_zero())

    @staticmethod
    def const_E(a):
        return FamElt(p_zero(), [mp.mpf(a)])

    def __add__(self, o):
        return FamElt(p_add(self.P, o.P), p_add(self.Q, o.Q))

    def __sub__(self, o):
        return FamElt(p_sub(self.P, o.P), p_sub(self.Q, o.Q))

    def scale(self, a):
        return FamElt(p_scale(self.P, a), p_scale(self.Q, a))

    def mul_one_minus_s(self):
        return FamElt(p_mul_one_minus_s(self.P), p_mul_one_minus_s(self.Q))

    def deriv(self, c, sc):
        """
        (P + Q E)' = (P' - sc*Q) + (Q' + c*s*Q) E
        """
        newP = p_sub(p_deriv(self.P), p_scale(self.Q, sc))
        newQ = p_add(p_deriv(self.Q), p_scale(p_mul_s(self.Q), c))
        return FamElt(newP, newQ)

    def eval(self, s, c):
        Eval = erfcx(s * mp.sqrt(c / mp.mpf(2)))
        return p_eval(self.P, s) + Eval * p_eval(self.Q, s)


# ----------------------------------------------------------------------
# Numerically safe erfcx(z) = e^{z^2} erfc(z)
#   direct formula for |z| <= 6, asymptotic series beyond (per required
#   reading's own description of what an ancestor front used -- built
#   fresh here, independently, from the standard asymptotic series of
#   erfcx, not copied from any script).
# ----------------------------------------------------------------------

def erfcx(z):
    z = mp.mpf(z)
    if abs(z) <= 6:
        return mp.e ** (z * z) * mp.erfc(z)
    # asymptotic series: erfcx(z) ~ 1/(z sqrt(pi)) * sum_{n>=0} (-1)^n (2n-1)!! / (2 z^2)^n
    # (2n-1)!! with (-1)!!:=1.  Sum enough terms for the working precision,
    # then stop (asymptotic series -- do not over-sum).
    s = mp.mpf(0)
    term = mp.mpf(1)
    dbl = mp.mpf(1)  # will hold (2n-1)!!
    n = 0
    prev_abs = None
    while n < 60:
        if n == 0:
            term = mp.mpf(1)
        else:
            dbl *= (2 * n - 1)
            term = ((-1) ** n) * dbl / (2 * z * z) ** n
        if prev_abs is not None and abs(term) > prev_abs:
            break  # asymptotic series started diverging -- stop before it does
        s += term
        prev_abs = abs(term)
        n += 1
    return s / (z * mp.sqrt(mp.pi))


# ----------------------------------------------------------------------
# Solve b_k' - c s b_k = A + B*E   (A, B polynomials), bounded branch,
# by the descending-recursion / kappa-pinning method (Sec 1.1 of the
# required reading, re-derived and re-implemented independently below).
# ----------------------------------------------------------------------

def _solve_U_descending(R, c):
    """
    Solve U'(s) - c s U(s) = R(s) for a POLYNOMIAL U, given polynomial R
    (R has degree N; the unique polynomial solution has degree N-1).
    Returns U's coefficient list.
    """
    R = p_trim(R)
    N = len(R) - 1  # degree of R
    if R == p_zero():
        return p_zero()
    # U indexed 0..N+1; U[N]=U[N+1]=0 (deg U = N-1, forced by matching the
    # top two degrees of R -- see module docstring / ATTEMPT.md Sec 2 for
    # the index derivation). Fill DOWNWARD: at index j we need U[j+1],
    # already populated either as a seed (j=N,N-1) or from an earlier
    # (higher-j) iteration of this same loop -- using a flat array indexed
    # by degree avoids any off-by-one in "how many steps back" that value
    # sits (this is exactly the bug caught and fixed here, self-caught
    # issue S1 in ATTEMPT.md).
    U = [mp.mpf(0)] * (N + 2)
    for j in range(N, 0, -1):
        rj = R[j] if j < len(R) else mp.mpf(0)
        U[j - 1] = ((j + 1) * U[j + 1] - rj) / c
    return p_trim(U[:N])


def solve_b_step(A: FamElt, c, sc):
    """
    Solve b' - c s b = A.P(s) + A.Q(s)*E(s)   for b in the family F,
    bounded as s->+infinity (selection = discard the e^{c s^2/2} branch).

    Method (Sec 1.1 of required reading, re-implemented independently):
      write b = U + V E.  E-part: V' = B  =>  V = antideriv(B) + kappa.
      non-E part: U' - c s U = A + sc*V =: R(s).
      Solve U via _solve_U_descending (linear in kappa: run once with
      kappa=0, once with kappa=1, then use the LEFTOVER j=0 equation of
      the descending solve -- U's own defining relation evaluated at
      j=0, i.e. u_1 = r_0 -- to pin kappa uniquely.)
    """
    Acoef, Bcoef = A.P, A.Q
    Vbase = p_antideriv(Bcoef)  # antiderivative with 0 constant

    def R_for_kappa(kappa):
        V = p_add(Vbase, [mp.mpf(kappa)])
        R = p_add(Acoef, p_scale(V, sc))
        return R, V

    R0, V0 = R_for_kappa(0)
    R1, V1 = R_for_kappa(1)
    U0 = _solve_U_descending(R0, c)
    U1 = _solve_U_descending(R1, c)

    # leftover equation: u_1 = r_0  (the j=0 relation of U'-csU=R, since
    # u_{-1}=0: (0+1)*u_1 - c*u_{-1} = r_0  =>  u_1 = r_0 )
    def coeff1(p):
        return p[1] if len(p) > 1 else mp.mpf(0)

    def coeff0(p):
        return p[0] if len(p) > 0 else mp.mpf(0)

    lhs0 = coeff1(U0) - coeff0(R0)   # should be 0 if kappa were correct already at kappa=0
    lhs_slope = (coeff1(U1) - coeff0(R1)) - lhs0  # change per unit kappa
    if lhs_slope == 0:
        kappa = mp.mpf(0)
    else:
        kappa = -lhs0 / lhs_slope

    R, V = R_for_kappa(kappa)
    U = _solve_U_descending(R, c)
    return FamElt(U, V)


# ----------------------------------------------------------------------
# Build the full a_k, b_k sequence up to order K, at fixed c.
# ----------------------------------------------------------------------

def build_series(c, K, dps):
    mp.mp.dps = dps
    c = mp.mpf(c)
    sc = mp.sqrt(2 * c / mp.pi)

    a = [None] * (K + 2)
    b = [None] * (K + 2)
    a[0] = FamElt.const(1)
    b[0] = FamElt.zero()
    a[1] = FamElt.const(-c)
    b[1] = FamElt.const_E(mp.sqrt(mp.pi * c / 2))

    for k in range(1, K + 1):
        # w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
        w_k = a[k - 1].scale(mp.mpf(1) / k) + b[k].mul_one_minus_s() - b[k - 1]
        # a_{k+1} = [a_k' - c a_k + c w_k] / (k+1)
        rhs = a[k].deriv(c, sc) - a[k].scale(c) + w_k.scale(c)
        a[k + 1] = rhs.scale(mp.mpf(1) / (k + 1))
        # b_{k+1}:  b_{k+1}' - c s b_{k+1} = -c a_k/(k+1) + c b_k
        src = a[k].scale(-c / (k + 1)) + b[k].scale(c)
        b[k + 1] = solve_b_step(src, c, sc)

    return a[: K + 1], b[: K + 1]


def eval_Phi(a_list, s, c, gmax_terms=None):
    """Phi(s,g) as a function of g, returned as callable via Horner in g."""
    coeffs = [ak.eval(s, c) for ak in a_list]

    def Phi_of_g(g):
        r = mp.mpf(0)
        for coef in reversed(coeffs):
            r = r * g + coef
        return r

    return Phi_of_g


def eval_Psi(b_list, s, c):
    coeffs = [bk.eval(s, c) for bk in b_list]

    def Psi_of_g(g):
        r = mp.mpf(0)
        for coef in reversed(coeffs):
            r = r * g + coef
        return r

    return Psi_of_g


if __name__ == "__main__":
    # Anchor validation at c=1000 against the SAME 7 published anchors used
    # throughout this lineage (transcribed as plain text from the required
    # reading -- never imported as code). K=220, dps=280 here: dps=280 was
    # found necessary (not dps=60) after the fix to _solve_U_descending --
    # see ATTEMPT.md Sec 8 (self-caught issue S1) and Sec 2.4 for why the
    # cancellation in evaluating Phi(0,0.05)'s power series (peak term
    # magnitude ~1e22 against a ~4e-2 answer) needs this much working
    # precision even though K=220 alone is enough for TRUNCATION.
    print("e01_family_series module -- anchor validation at c=1000, K=220, dps=280")
    dps = 280
    mp.mp.dps = dps
    c = 1000
    K = 220
    a, b = build_series(c, K, dps)
    Phi0 = eval_Phi(a, mp.mpf(0), c)
    anchors = [
        ("a2(0)", a[2].eval(mp.mpf(0), c), "520316.636488"),
        ("a3(0)", a[3].eval(mp.mpf(0), c), "-180730907.6285"),
        ("a4(0)", a[4].eval(mp.mpf(0), c), "47146963944.14"),
        ("b2(0)", b[2].eval(mp.mpf(0), c), "-20816.636488"),
        ("b1(0)", b[1].eval(mp.mpf(0), c), str(mp.sqrt(mp.pi * 1000 / 2))),
        ("Phi(0,0.002)", Phi0(mp.mpf('0.002')), "0.15850015"),
        ("Phi(0,0.05) [plateau]", Phi0(mp.mpf('0.05')), "0.0377615983402126"),
    ]
    for name, val, target in anchors:
        print(f"{name:24s} = {mp.nstr(val, 24)}   (published anchor: {target})")
