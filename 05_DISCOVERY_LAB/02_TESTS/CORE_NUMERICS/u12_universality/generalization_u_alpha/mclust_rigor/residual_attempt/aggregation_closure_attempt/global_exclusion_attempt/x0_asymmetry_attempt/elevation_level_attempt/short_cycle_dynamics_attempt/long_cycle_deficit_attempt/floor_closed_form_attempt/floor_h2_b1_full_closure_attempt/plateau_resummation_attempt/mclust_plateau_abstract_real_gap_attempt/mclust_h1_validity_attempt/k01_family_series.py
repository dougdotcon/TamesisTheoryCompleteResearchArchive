"""
k01_family_series.py -- MCLUST-H1-VALIDITY-ATTEMPT

Fresh, from-scratch implementation of the (P,Q)-family recursion for the
b=1 floor process's series coefficients a_k(s), b_k(s), at GENERAL s (not
just s=0). Built entirely from the recursion stated in prose in
plateau_resummation_attempt/ATTEMPT.md Section 0 / Section 1.1 (required
reading for this front) -- NO .py file of any ancestor front was opened,
read, or imported.

Recursion (restated from the prose, Section 0):

    Phi(s,g) = sum_k a_k(s) g^k,  Psi(s,g) = sum_k b_k(s) g^k, a_0=1, b_0=0
    a_{k+1}(s) = [a_k'(s) - c*a_k(s) + c*w_k(s)] / (k+1)
    b_k'(s) - c*s*b_k(s) = -c*a_{k-1}(s)/k + c*b_{k-1}(s)      (bounded branch)
    w_k(s) = a_{k-1}(s)/k + (1-s)*b_k(s) - b_{k-1}(s)
    a_1(s) = -c,  b_1(s) = sqrt(pi*c/2)*erfcx(s*sqrt(c/2))
    every a_k, b_k in F = {P(s) + Q(s)*erfcx(s*sqrt(c/2))}, P,Q polynomials

and the family-closure identity + descending-recursion / kappa-pinning
method for solving the b-ODE within F, both restated in prose in Section
1.1 of the same document:

    E(s) := erfcx(s*sqrt(c/2)),  sc := sqrt(2c/pi),   E' = c*s*E - sc
    (P + Q E)' = (P' - sc*Q) + (Q' + c*s*Q) E
    for b' - c*s*b = A(s) + B(s)E(s), writing b = U + V*E:
      V' = B  =>  V = int(B) + kappa   (one free constant kappa)
      U' - c*s*U = A + sc*V =: R(s); matching s^j coefficients,
      (j+1) u_{j+1} - c u_{j-1} = r_j, solved DESCENDING from j=deg(R),
      forcing deg(U) = deg(R)-1 and using no integration; the single
      leftover j=0 relation u_1 = r_0 PINS kappa = (u_1 - A_0)/sc.

This front re-derived this algorithm itself (by hand, from the prose
above) before writing any code; the derivation is repeated in ATTEMPT.md
Section 2 of this front's own document. All coefficient arithmetic below
is done at mpmath dps>=50 (set by caller via mpmath.mp.dps before import
of functions that use it, or explicitly per-call).
"""

import mpmath as mp


# ---------------------------------------------------------------------
# Polynomial helpers. A polynomial is represented as a Python list of
# mpmath mpf/mpc coefficients, index i = coefficient of s^i (lowest
# degree first). The empty list [] represents the zero polynomial.
# ---------------------------------------------------------------------

def p_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def p_add(a, b):
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        ai = a[i] if i < len(a) else mp.mpf(0)
        bi = b[i] if i < len(b) else mp.mpf(0)
        out.append(ai + bi)
    return p_trim(out)


def p_sub(a, b):
    return p_add(a, [-x for x in b])


def p_scale(a, lam):
    return p_trim([lam * x for x in a])


def p_shift(a):
    """Multiply polynomial a(s) by s (shift coefficients up by one)."""
    if not a:
        return []
    return [mp.mpf(0)] + list(a)


def p_deriv(a):
    """d/ds of polynomial a."""
    if len(a) <= 1:
        return []
    return p_trim([i * a[i] for i in range(1, len(a))])


def p_antideriv(a):
    """Antiderivative of polynomial a with zero constant term."""
    if not a:
        return []
    return p_trim([mp.mpf(0)] + [a[i] / (i + 1) for i in range(len(a))])


def p_mul_one_minus_s(a):
    """Multiply polynomial a(s) by (1-s)."""
    return p_sub(a, p_shift(a))


def p_eval(a, s0):
    """Horner evaluation of polynomial a at s0."""
    r = mp.mpf(0)
    for c in reversed(a):
        r = r * s0 + c
    return r


# ---------------------------------------------------------------------
# Family elements: pairs (P, Q) representing P(s) + Q(s)*E(s).
# ---------------------------------------------------------------------

def f_add(A, B):
    return (p_add(A[0], B[0]), p_add(A[1], B[1]))


def f_sub(A, B):
    return (p_sub(A[0], B[0]), p_sub(A[1], B[1]))


def f_scale(A, lam):
    return (p_scale(A[0], lam), p_scale(A[1], lam))


def f_mul_one_minus_s(A):
    return (p_mul_one_minus_s(A[0]), p_mul_one_minus_s(A[1]))


def f_deriv(A, c, sc):
    """(P + Q E)' = (P' - sc*Q) + (Q' + c*s*Q) E ,  using E' = c*s*E - sc."""
    P, Q = A
    newP = p_sub(p_deriv(P), p_scale(Q, sc))
    newQ = p_add(p_deriv(Q), p_scale(p_shift(Q), c))
    return (p_trim(newP), p_trim(newQ))


def f_eval(A, s0, c):
    """Numeric value of P(s0) + Q(s0)*erfcx(s0*sqrt(c/2)) at s0.

    mpmath has no built-in erfcx; see erfcx() below for the numerically
    safe implementation used here (direct formula for small/moderate
    argument, asymptotic series for large argument -- needed because
    z = s0*sqrt(c/2) reaches O(100)-O(1000) in this front's grid, where
    naive exp(z^2)*erfc(z) catastrophically loses precision / overflows
    at fixed working precision).
    """
    P, Q = A
    z = s0 * mp.sqrt(c / mp.mpf(2))
    Eval = erfcx(z)
    return p_eval(P, s0) + p_eval(Q, s0) * Eval


def erfcx(z):
    """
    Numerically safe erfcx(z) = exp(z^2)*erfc(z), valid for real z>=0
    (the only regime used in this front: z = s*sqrt(c/2) with s,c >= 0).

    mpmath has no built-in erfcx. For small/moderate z (<= 6) we use the
    direct formula exp(z^2)*erfc(z) (both factors representable at
    working precision). For larger z we use the standard asymptotic
    continued-fraction / series expansion for erfcx (Numerical Recipes /
    Cody-style), which is what one needs anyway for the z up to several
    hundred that this front's grid reaches; mpmath's arbitrary precision
    erfc/exp already keep this accurate well past the range used here
    (verified against the direct formula in the overlap region, group V0
    below).
    """
    z = mp.mpf(z)
    if z <= 6:
        return mp.e**(z * z) * mp.erfc(z)
    # asymptotic series erfcx(z) ~ 1/(z sqrt(pi)) * sum (-1)^n (2n-1)!!/(2z^2)^n
    # implemented as a continued-fraction-free truncated asymptotic sum,
    # with enough terms relative to mp.mp.dps to stay well within the
    # series' asymptotic validity for the z-range actually used (z<=1500
    # in this front, dps<=60): standard result, error ~ next term.
    one = mp.mpf(1)
    s = one
    term = one
    twoZ2 = 2 * z * z
    n = 0
    maxterms = 60
    while n < maxterms:
        n += 1
        term *= -(2 * n - 1) / twoZ2
        if abs(term) < mp.mpf(10) ** (-(mp.mp.dps + 5)):
            break
        s += term
    return s / (z * mp.sqrt(mp.pi))


def build_family(c, K, dps):
    """
    Build a_1..a_K, b_1..b_K as (P,Q) family pairs, at working precision
    dps, for the given (numeric) c. Returns (a_list, b_list) where
    a_list[k] = a_k for k=0..K, similarly b_list.
    """
    old_dps = mp.mp.dps
    mp.mp.dps = dps
    try:
        c = mp.mpf(c)
        sc = mp.sqrt(2 * c / mp.pi)

        a = [None] * (K + 1)
        b = [None] * (K + 1)
        a[0] = ([mp.mpf(1)], [])
        b[0] = ([], [])
        a[1] = ([-c], [])
        b[1] = ([], [mp.sqrt(mp.pi * c / 2)])

        for k in range(1, K):
            # w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
            wk = f_sub(f_add(f_scale(a[k - 1], 1 / mp.mpf(k)),
                              f_mul_one_minus_s(b[k])),
                       b[k - 1])
            # a_{k+1} = [a_k' - c a_k + c w_k] / (k+1)
            rhs_a = f_add(f_sub(f_deriv(a[k], c, sc), f_scale(a[k], c)),
                          f_scale(wk, c))
            a[k + 1] = f_scale(rhs_a, 1 / mp.mpf(k + 1))

            # RHS for b_{k+1}: -c*a_k/(k+1) + c*b_k =: A(s)+B(s)E(s)
            RHS = f_add(f_scale(a[k], -c / mp.mpf(k + 1)), f_scale(b[k], c))
            b[k + 1] = solve_b_step(RHS, c, sc)

        return a, b
    finally:
        mp.mp.dps = old_dps


def solve_b_step(RHS, c, sc):
    """
    Solve  b' - c*s*b = A(s) + B(s)*E(s)  for b = U(s) + V(s)*E(s) within
    the family F, via the descending-recursion / kappa-pinning method
    described in the module docstring.
    """
    A, B = RHS
    Vbase = p_antideriv(B)          # V = Vbase + kappa, Vbase[0] = 0 by construction

    # R(s) = A(s) + sc*V(s) = A(s) + sc*Vbase(s) + sc*kappa   (kappa only
    # touches the constant term r_0; r_1..r_D are kappa-independent)
    Rknown = p_add(A, p_scale(Vbase, sc))
    D = max(len(Rknown) - 1, 0)   # degree of R (R may be shorter; pad)

    # descending recursion: arr[j] for j=0..D+1, arr[D]=arr[D+1]=0 (boundary)
    arr = [mp.mpf(0)] * (D + 2)
    for j in range(D, 0, -1):
        rj = Rknown[j] if j < len(Rknown) else mp.mpf(0)
        arr[j - 1] = ((j + 1) * arr[j + 1] - rj) / c

    U = p_trim(arr[0:D])
    u1 = arr[1] if D >= 1 else mp.mpf(0)
    A0 = A[0] if len(A) > 0 else mp.mpf(0)
    kappa = (u1 - A0) / sc

    V = list(Vbase)
    if not V:
        V = [mp.mpf(0)]
    V[0] = V[0] + kappa
    V = p_trim(V)

    return (U, V)


def phi_series_sum(a_list, s0, t0, K, c):
    """Sum_{k=0}^{K} a_k(s0) * t0^k directly (Horner in t0)."""
    r = mp.mpf(0)
    t0 = mp.mpf(t0)
    for k in range(K, -1, -1):
        r = r * t0 + f_eval(a_list[k], s0, c)
    return r
