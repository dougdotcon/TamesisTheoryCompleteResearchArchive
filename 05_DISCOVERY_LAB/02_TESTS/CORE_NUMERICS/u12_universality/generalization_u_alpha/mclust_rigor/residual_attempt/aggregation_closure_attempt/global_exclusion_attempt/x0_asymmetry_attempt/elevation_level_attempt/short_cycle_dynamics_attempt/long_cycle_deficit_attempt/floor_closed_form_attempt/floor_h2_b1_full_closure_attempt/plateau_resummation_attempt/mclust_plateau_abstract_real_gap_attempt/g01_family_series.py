"""
g01_family_series.py -- FRESH, from-scratch implementation of the (P,Q)-
family recursion for the b=1 floor's Phi(0,t0) series coefficients.

Written ENTIRELY from the prose of record (no .py file from any ancestor
front in this lineage was opened, per the mandate). Sources for the
mathematics reproduced here:

  - floor_h2_b1_full_closure_attempt/ATTEMPT.md SS1-SS2 and its
    adversarial/REFEREE_REPORT.md SS1 (recursion; psi1 closed form;
    the {P(s)+Q(s)*erfcx(s*sqrt(c/2))} family closure induction).
  - plateau_resummation_attempt/ATTEMPT.md SS0-SS1 (restated recursion;
    the (P,Q)-family solve technique: writing b = U + V*E, V'=B,
    U'-c*s*U = A + sc*V =: R, solved by DESCENDING coefficient matching
    from degree(R) down to 0, with the leftover j=0 relation pinning the
    free constant kappa).

Governing recursion (all sources agree, stated identically):

    Phi(s,g) = sum_k a_k(s) g^k,  Psi(s,g) = sum_k b_k(s) g^k
    a_0 = 1, b_0 = 0
    a_{k+1}(s) = [a_k'(s) - c*a_k(s) + c*w_k(s)] / (k+1)
    b_k'(s) - c*s*b_k(s) = -c*a_{k-1}(s)/k + c*b_{k-1}(s)      (k>=1)
    w_k(s) = a_{k-1}(s)/k + (1-s)*b_k(s) - b_{k-1}(s)          (k>=1)
    a_1(s) = -c  (constant)
    b_1(s) = psi1(s) = sqrt(pi*c/2) * erfcx(s*sqrt(c/2))

Every a_k, b_k lies in F = {P(s) + Q(s)*E(s) : P,Q polynomials},
E(s) := erfcx(s*sqrt(c/2)), using the closure identity

    E'(s) = c*s*E(s) - sc,   sc := sqrt(2*c/pi)

(independently re-derivable from the standard identity
erfcx'(z) = 2*z*erfcx(z) - 2/sqrt(pi) via the chain rule z=s*sqrt(c/2)).

This module represents every element of F as a pair of coefficient lists
(P, Q) -- P[i] is the coefficient of s^i in P(s), same for Q -- using
mpmath mpf arithmetic at a caller-specified precision. All arithmetic
(derivative, the b-ODE solve) is EXACT rational/polynomial algebra done
in floating point at high precision; no numerical quadrature anywhere.
"""

import mpmath as mp


def poly_trim(p):
    """Drop trailing exact zeros (keeps at least length 1)."""
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def poly_add(p, q):
    n = max(len(p), len(q))
    out = [mp.mpf(0)] * n
    for i, c in enumerate(p):
        out[i] += c
    for i, c in enumerate(q):
        out[i] += c
    return poly_trim(out)


def poly_sub(p, q):
    return poly_add(p, [-c for c in q])


def poly_scale(p, lam):
    return poly_trim([lam * c for c in p])


def poly_mul_1ms(p):
    """Multiply polynomial p(s) by (1-s)."""
    n = len(p)
    out = [mp.mpf(0)] * (n + 1)
    for i, c in enumerate(p):
        out[i] += c       # from "1*p"
        out[i + 1] -= c   # from "-s*p"
    return poly_trim(out)


def poly_deriv(p):
    n = len(p)
    if n <= 1:
        return [mp.mpf(0)]
    out = [mp.mpf(i) * p[i] for i in range(1, n)]
    return poly_trim(out)


def poly_integral_no_const(p):
    """Antiderivative of p(s) with the added constant fixed to 0."""
    out = [mp.mpf(0)] * (len(p) + 1)
    for i, c in enumerate(p):
        out[i + 1] = c / mp.mpf(i + 1)
    return poly_trim(out)


class F:
    """An element P(s) + Q(s)*E(s) of the family F, E(s)=erfcx(s*sqrt(c/2))."""

    __slots__ = ("P", "Q")

    def __init__(self, P, Q):
        self.P = poly_trim(list(P))
        self.Q = poly_trim(list(Q))

    @staticmethod
    def const(v):
        return F([mp.mpf(v)], [mp.mpf(0)])

    @staticmethod
    def zero():
        return F.const(0)

    def __add__(self, other):
        return F(poly_add(self.P, other.P), poly_add(self.Q, other.Q))

    def __sub__(self, other):
        return F(poly_sub(self.P, other.P), poly_sub(self.Q, other.Q))

    def scale(self, lam):
        return F(poly_scale(self.P, lam), poly_scale(self.Q, lam))

    def mul_1ms(self):
        return F(poly_mul_1ms(self.P), poly_mul_1ms(self.Q))

    def deriv(self, c, sc):
        """
        d/ds [P + Q*E] = (P' - sc*Q) + (Q' + c*s*Q)*E
        using E' = c*s*E - sc.
        """
        newP = poly_sub(poly_deriv(self.P), poly_scale(self.Q, sc))
        # Q' + c*s*Q  (c*s*Q is a shift-and-scale)
        csQ = [mp.mpf(0)] * (len(self.Q) + 1)
        for i, coeff in enumerate(self.Q):
            csQ[i + 1] = c * coeff
        newQ = poly_add(poly_deriv(self.Q), csQ)
        return F(newP, newQ)

    def at0(self):
        """Value at s=0: P(0) + Q(0)*E(0) = P[0] + Q[0]*1  (erfcx(0)=1)."""
        p0 = self.P[0] if self.P else mp.mpf(0)
        q0 = self.Q[0] if self.Q else mp.mpf(0)
        return p0 + q0

    def eval_s(self, s, c):
        """Full numeric evaluation at general s (for cross-checks only)."""
        Pv = mp.polyval(list(reversed(self.P)), s)
        Qv = mp.polyval(list(reversed(self.Q)), s)
        Ev = mp.erfc(s * mp.sqrt(c / mp.mpf(2))) * mp.exp(c * s * s / 2) if False else _erfcx(s * mp.sqrt(c / mp.mpf(2)))
        return Pv + Qv * Ev


def _erfcx(x):
    """erfcx(x) = exp(x^2)*erfc(x), numerically stable via mpmath directly."""
    return mp.erfc(x) * mp.exp(x * x)


def solve_b_ode(A, B, c, sc):
    """
    Solve b' - c*s*b = A(s) + B(s)*E(s) for the UNIQUE bounded-branch
    solution b = U(s) + V(s)*E(s) in F.

    V' = B  =>  V = integral(B) + kappa   (kappa a free constant)
    U' - c*s*U = A + sc*V =: R(s)         (R depends linearly on kappa
                                            only through its CONSTANT term,
                                            since kappa itself is constant)

    U is forced to be a polynomial of degree deg(R)-1 (else U'-c*s*U has
    degree deg(R)+1, matching only if the leading coefficient is 0 -- ruled
    out generically); solved by descending coefficient matching from
    j=deg(R) down to j=1, leaving the j=0 relation "u_1 = r_0" as a
    consistency condition that PINS kappa (kappa = (u_1 - A_0)/sc), rather
    than an extra free unknown -- this IS the boundedness selection (the
    homogeneous solution e^{c*s^2/2} is a non-polynomial function of s
    outside F, so requiring b in F -- i.e. requiring boundedness under E's
    own normalization -- automatically discards it).
    """
    V0 = poly_integral_no_const(B)  # kappa-independent part of V
    R0 = poly_add(A, poly_scale(V0, sc))  # kappa-independent part of R
    dR = len(R0) - 1  # degree of R0 (R and R0 share degree for dR>=1)

    if dR < 1:
        # R0 is (at most) a constant -- degenerate low-order case.
        # U' - c*s*U = r0 (constant, possibly plus sc*kappa).
        # A polynomial U solving this with U constant-degree only works if
        # r0=0 (U=0) generically; handle the one required low-order case
        # (k=1: A=-c, B=0) explicitly and generally via direct small solve.
        # For safety, fall back to a slow, general small-case solver.
        return _solve_b_ode_small(A, B, c, sc)

    # u_{dR-1} .. u_0, computed by descending recursion, dict-indexed by
    # power j (u_j) to avoid any off-by-one error.
    r = list(R0) + [mp.mpf(0)]  # pad so r[dR] is safe to index
    # j = dR:  -c*u_{dR-1} = r_{dR}   (u_{dR+1}=0, out of range)
    uu = {dR - 1: -r[dR] / c}
    for j in range(dR - 1, 0, -1):
        u_jp1 = uu.get(j + 1, mp.mpf(0))
        uu[j - 1] = ((j + 1) * u_jp1 - r[j]) / c
    u1 = uu.get(1, mp.mpf(0))
    A0 = A[0] if A else mp.mpf(0)
    kappa = (u1 - A0) / sc

    Ulist = [mp.mpf(0)] * dR
    for j, val in uu.items():
        if 0 <= j < dR:
            Ulist[j] = val
    U = poly_trim(Ulist)
    V = poly_add(V0, [kappa])
    return F(U, V)


def _solve_b_ode_small(A, B, c, sc):
    """
    Degenerate fallback for deg(R0) <= 0 (used only at k=1, where
    A=[-c], B=[0]). Solve U'-c*s*U = A0 + sc*kappa (a pure constant RHS)
    with U a polynomial and boundedness (U in F, i.e. finite degree).
    U'-c*s*U for U=sum u_j s^j has NO constant term unless U=0 (the
    s^0-coefficient of U'-c*s*U is 1*u_1, and higher terms force
    u_1=u_3=...=0 unless the RHS is a nonzero polynomial of positive
    degree) -- for a strictly constant target this forces u_j=0 for all
    j>=1 UNLESS the target constant is 0, and separately kappa is pinned
    by requiring the s^0 coefficient match: u_1 = A0 + sc*kappa. Taking
    the minimal (deg U = 0, i.e. U=u_0 only, hence u_1=0) solution gives
    kappa = -A0/sc, U=[u_0] with u_0 free at this order -- but degree-0 U
    must also satisfy the s^1... actually for deg(R)=0 the correct
    minimal polynomial solution has degree -1 i.e. U=0 identically once
    kappa is chosen correctly, checked directly against the known k=1
    anchor (b_1=psi1, U=0, V=kappa=sqrt(pi*c/2)) below.
    """
    A0 = A[0] if A else mp.mpf(0)
    B0 = B[0] if B else mp.mpf(0)
    if any(x != 0 for x in A[1:]) or any(x != 0 for x in B[1:]):
        raise NotImplementedError("small-case fallback only supports constant A,B")
    # V' = B = B0 (constant) => V = B0*s + kappa
    # U' - c*s*U = A0 + sc*(B0*s+kappa) =: R(s) = sc*B0*s + (A0+sc*kappa)
    # For k=1: B0=0, so R is the pure constant (A0+sc*kappa).
    # U=0 works iff R=0 identically, i.e. kappa = -A0/sc AND sc*B0=0.
    if B0 != 0:
        raise NotImplementedError("small-case fallback: B0 must be 0")
    kappa = -A0 / sc
    U = [mp.mpf(0)]
    V = [kappa, B0] if B0 != 0 else [kappa]
    return F(U, V)


def build_a_b(c, K, dps):
    """
    Build a_k, b_k (as F objects) for k=0..K at fixed parameter c, using
    working precision `dps` decimal digits.

    Returns (a_list, b_list) with a_list[k], b_list[k] the F-objects for
    a_k(s), b_k(s).
    """
    mp.mp.dps = dps
    cc = mp.mpf(c)
    sc = mp.sqrt(2 * cc / mp.pi)

    a = [None] * (K + 1)
    b = [None] * (K + 1)
    a[0] = F.const(1)
    b[0] = F.zero()
    # a_1 = -c (constant)
    a[1] = F.const(-cc)
    # b_1 solves b_1' - c*s*b_1 = -c*a_0/1 + c*b_0 = -c  (A=[-c], B=[0])
    b[1] = solve_b_ode([-cc], [mp.mpf(0)], cc, sc)

    for k in range(1, K):
        # w_k = a_{k-1}/k + (1-s)*b_k - b_{k-1}
        term1 = a[k - 1].scale(mp.mpf(1) / k)
        term2 = b[k].mul_1ms()
        w_k = term1 + term2 - b[k - 1]
        # a_{k+1} = [a_k' - c*a_k + c*w_k] / (k+1)
        a_kp1 = (a[k].deriv(cc, sc) - a[k].scale(cc) + w_k.scale(cc)).scale(mp.mpf(1) / (k + 1))
        a[k + 1] = a_kp1

        if k + 1 <= K:
            # b_{k+1} solves b' - c*s*b = -c*a_k/(k+1) + c*b_k
            A_ = poly_add(poly_scale(a[k].P, -cc / (k + 1)), poly_scale(b[k].P, cc))
            B_ = poly_add(poly_scale(a[k].Q, -cc / (k + 1)), poly_scale(b[k].Q, cc))
            b[k + 1] = solve_b_ode(A_, B_, cc, sc)

    return a, b


if __name__ == "__main__":
    # Minimal smoke test; full anchor validation is in g02_validate_anchors.py
    mp.mp.dps = 60
    c = 1000
    a, b = build_a_b(c, 6, 60)
    print("a1(0) =", a[1].at0(), " expected -1000")
    print("a2(0) =", a[2].at0(), " expected 520316.636488...")
    print("a3(0) =", a[3].at0(), " expected -180730907.6285...")
    print("a4(0) =", a[4].at0(), " expected 47146963944.14...")
    print("b1(0) =", b[1].at0(), " expected sqrt(pi*c/2)=", mp.sqrt(mp.pi * c / 2))
    print("b2(0) =", b[2].at0(), " expected -20816.636488...")
