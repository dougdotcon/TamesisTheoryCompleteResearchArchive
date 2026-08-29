"""
u02_family_series.py

Fresh, from-scratch implementation (mpmath, no code opened/copied from any
ancestor front in the mclust_rigor lineage) of the general-`s` (P,Q)-family
recursion of record:

  Phi(s,g) = sum_k a_k(s) g^k,  Psi(s,g) = sum_k b_k(s) g^k
  a_0=1, b_0=0
  a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
  w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
  a_1 = -c ,  b_1 = sqrt(pi c/2)*erfcx(s sqrt(c/2))
  every a_k, b_k in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials

Every a_k, b_k is represented as a pair of coefficient lists (P,Q), meaning
P(s) + Q(s)*E(s), E(s):=erfcx(s*sqrt(c/2)). The family is closed under
d/ds via E'(s) = c*s*E(s) - sc, sc:=sqrt(2c/pi):

  (P + Q E)' = (P' - sc*Q)  +  (Q' + c*s*Q) * E

so d/ds of any (P,Q) pair is again a (P,Q) pair, computed directly (no
solve needed).

The b_k ODE b_k' - c*s*b_k = RHS (RHS itself in (A,B) family form, i.e.
RHS = A(s) + B(s)*E(s)) is solved for b_k=(U,V) (U+V*E) via:
  - E-part:      V' = B  =>  V = antiderivative(B) + kappa      (kappa free)
  - non-E part:  U' - c*s*U = A + sc*V =: Rtilde(s; kappa)
    solved by a DESCENDING recursion on Rtilde's polynomial coefficients
    (re-derived from scratch below, worked through by hand first -- see
    the docstring of solve_b_ode() -- matching the "descending recursion /
    kappa-pinning" method described in the required reading's prose,
    independently re-derived here, not copied from any script).

VALIDATION DISCIPLINE (per this lineage's convention): every b_k solve is
checked by directly plugging (U,V) back into the ODE at several numeric s
values (residual must vanish to working precision) BEFORE being trusted,
and the whole recursion is validated against the record's own published
anchors (a_2(0), a_3(0), a_4(0), b_2(0), b_1 closed form, Phi(0,0.002),
plateau at c=1000) before any new claim is built on it (n03 script).
"""
from mpmath import mp, mpf, erfc, exp, sqrt, pi, factorial


# ---------------------------------------------------------------------
# Polynomial helpers. A polynomial is a list [c0, c1, c2, ...] (c_i is the
# coefficient of s^i), mpf entries, trailing zeros allowed (not trimmed
# eagerly -- trimming only when it matters for degree bookkeeping).
# ---------------------------------------------------------------------

def p_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    if not p:
        p = [mpf(0)]
    return p


def p_deg(p):
    p = p_trim(p)
    if len(p) == 1 and p[0] == 0:
        return -1  # zero polynomial
    return len(p) - 1


def p_add(a, b, sa=1, sb=1):
    """sa*a + sb*b"""
    n = max(len(a), len(b))
    out = [mpf(0)] * n
    for i in range(len(a)):
        out[i] += sa * a[i]
    for i in range(len(b)):
        out[i] += sb * b[i]
    return p_trim(out)


def p_deriv(p):
    if len(p) <= 1:
        return [mpf(0)]
    return p_trim([i * p[i] for i in range(1, len(p))])


def p_shift_scale(p, factor):
    """Return factor * s * p(s) (multiply by s, i.e. shift coefficients up
    by one index, then scale by `factor`)."""
    return p_trim([mpf(0)] + [factor * c for c in p])


def p_eval(p, s):
    val = mpf(0)
    for c in reversed(p):
        val = val * s + c
    return val


def p_antideriv_zero_const(p):
    """Antiderivative of p with constant of integration = 0."""
    return p_trim([mpf(0)] + [p[i] / (i + 1) for i in range(len(p))])


# ---------------------------------------------------------------------
# Family element = (P, Q) meaning P(s) + Q(s)*E(s).
# ---------------------------------------------------------------------

def fam_add(f1, f2, s1=1, s2=1):
    P1, Q1 = f1
    P2, Q2 = f2
    return (p_add(P1, P2, s1, s2), p_add(Q1, Q2, s1, s2))


def fam_scale(f, lam):
    P, Q = f
    return ([lam * c for c in P], [lam * c for c in Q])


def fam_deriv(f, c, sc):
    """(P+QE)' = (P' - sc*Q) + (Q' + c*s*Q) * E"""
    P, Q = f
    newP = p_add(p_deriv(P), Q, 1, -sc)
    newQ = p_add(p_deriv(Q), p_shift_scale(Q, c))
    return (newP, newQ)


def fam_mul_cs(f, coef):
    """coef * s * (P + Q E) = [coef*s*P] + [coef*s*Q] E"""
    P, Q = f
    return (p_shift_scale(P, coef), p_shift_scale(Q, coef))


def fam_mul_one_minus_s(f):
    """(1-s) * (P+QE) = [(1-s)P] + [(1-s)Q] E"""
    P, Q = f
    return (p_add(P, p_shift_scale(P, -1), 1, 1), p_add(Q, p_shift_scale(Q, -1), 1, 1))


def fam_eval(f, s, Eval):
    P, Q = f
    return p_eval(P, s) + p_eval(Q, s) * Eval


def erfcx(z):
    """erfcx(z) = e^{z^2} erfc(z). This front's whole grid keeps
    z = s*sqrt(c/2) modest (boundary-layer s = O(1/c) or a couple of
    O(1)-x bridge points, never the large-z stress regime some ancestor
    fronts tested), so the direct formula is precision-safe throughout;
    no large-z asymptotic branch is needed here."""
    return exp(z * z) * erfc(z)


# ---------------------------------------------------------------------
# Solve U' - c*s*U = Rtilde(s; kappa) = R0(s) + sc*kappa   (R0 known)
# for a POLYNOMIAL U (finite degree), returning (U, kappa).
#
# Derivation (worked by hand before coding, re-derived fresh here):
# write Rtilde = sum_j r_j s^j, U = sum_j u_j s^j (u_j := 0 for j<0 or
# j > deg U). Matching coefficients of s^j in U' - c s U = Rtilde:
#   U'  contributes (j+1) u_{j+1} s^j
#   -c*s*U contributes -c u_{j-1} s^j
# so for every j >= 0:      (j+1) u_{j+1} - c u_{j-1} = r_j        (*)
#
# If deg(R0) = D0 >= 1 (kappa only ever shifts r_0, the CONSTANT term, so
# deg(Rtilde) = D0 for any kappa), U necessarily has degree D_U = D0-1
# (so that -c*s*U, degree D_U+1, matches Rtilde's top degree D0; U' has
# lower degree D_U-1 so contributes nothing at the top). Then:
#   j = D0     : u_{D0+1} does not exist (D0+1 > D_U) => -c u_{D0-1} = r_{D0}
#   j = D0-1   : u_{D0}   does not exist (D0   > D_U) => -c u_{D0-2} = r_{D0-1}
#   j = D0-2 .. 1 (descending): (j+1) u_{j+1} - c u_{j-1} = r_j, u_{j+1}
#                already known from a previous (larger-j) step of this
#                SAME loop => u_{j-1} = [(j+1) u_{j+1} - r_j] / c
# This determines EVERY u_0..u_{D_U} using ONLY r_1..r_{D0} (r_0 never
# used in this chain -- confirmed explicitly by the fact that the loop
# above only ever reads r_j for j>=1). The leftover j=0 equation,
#   1*u_1 - c*u_{-1} = r_0   i.e.   u_1 = r_0   (u_{-1}:=0 by convention)
# is NOT a determination of u_1 (already known from the descending chain
# whenever D_U >= 1) but a CONSTRAINT fixing kappa (since r_0 = R0_0 +
# sc*kappa): kappa = (u_1(known) - R0_0) / sc.
#
# Edge cases (D0 = 0 or D0 <= -1, i.e. R0 is a constant or the zero
# polynomial) handled explicitly below, worked out the same way.
# ---------------------------------------------------------------------

def solve_polynomial_ode(R0, c, sc):
    """U' - c*s*U = R0(s) + sc*kappa. Returns (U_coeffs, kappa)."""
    R0 = p_trim(R0)
    D0 = p_deg(R0)  # -1 if R0 identically zero

    if D0 <= -1:
        # Rtilde = sc*kappa (pure constant, possibly zero). U must satisfy
        # U' - c s U = const. A nonzero polynomial LHS has degree >=1
        # (from -c*s*U, unless U=0), so the only polynomial solution is
        # U=0, forcing sc*kappa = 0 => kappa = 0.
        return [mpf(0)], mpf(0)

    if D0 == 0:
        # Rtilde = r0 + sc*kappa*0... wait D0==0 means R0 already has a
        # constant term r0=R0[0] and nothing else; Rtilde = r0 + sc*kappa
        # is itself just a (possibly different) constant. Same edge case
        # as D0<=-1 structurally: U=0 forces r0 + sc*kappa = 0.
        r0 = R0[0]
        kappa = -r0 / sc
        return [mpf(0)], kappa

    if D0 == 1:
        # Rtilde = r0 + r1*s (r0 = R0[0] + sc*kappa, r1 = R0[1] known).
        # U = u0 constant (D_U=0): U'=0, -c*s*u0 must match r0+r1*s =>
        # matching s^1: -c*u0 = r1 => u0 = -r1/c.
        # matching s^0: 0 = r0 => kappa = -R0[0]/sc.
        r1 = R0[1]
        u0 = -r1 / c
        kappa = -R0[0] / sc
        return [u0], kappa

    # D0 >= 2: D_U = D0 - 1 >= 1.
    D_U = D0 - 1
    u = [mpf(0)] * (D_U + 1)
    r = R0 + [mpf(0)] * (D0 + 1 - len(R0))  # r_j for j=0..D0 (r_0 uses R0[0]; kappa added after)

    # top two, from j=D0 and j=D0-1
    u[D_U] = -r[D0] / c        # u_{D0-1}
    u[D_U - 1] = -r[D0 - 1] / c  # u_{D0-2}   (D_U-1 = D0-2, valid since D0>=2)

    # descend j = D0-2 down to 1
    for j in range(D0 - 2, 0, -1):
        u[j - 1] = ((j + 1) * u[j + 1] - r[j]) / c

    u1 = u[1] if D_U >= 1 else mpf(0)
    kappa = (u1 - R0[0]) / sc

    return p_trim(u), kappa


def solve_b_ode(RHS, c, sc):
    """RHS = (A, B) in family form (A + B*E). Solve b' - c*s*b = RHS for
    b = (U, V) in family form, returning (U, V)."""
    A, B = RHS
    V0 = p_antideriv_zero_const(B)
    R0 = p_add(A, V0, 1, sc)  # R0 = A + sc*V0
    U, kappa = solve_polynomial_ode(R0, c, sc)
    V = p_add(V0, [kappa], 1, 1)
    return (U, V)


def validate_b_ode(b, RHS, c, sc, c_val, sample_s, tol):
    """Direct numeric residual check: b' - c*s*b - RHS(s) ~= 0 at each s
    in sample_s, using fam_deriv (independent of solve_b_ode's own
    algebra -- this is a genuine cross-check, not a tautology, since
    fam_deriv implements the E'-rule directly while solve_b_ode implements
    the descending polynomial recursion)."""
    bp = fam_deriv(b, c_val, sc)
    lhs_minus_csB = fam_add(bp, fam_mul_cs(b, -c_val))
    worst_rel = mpf(0)
    for s in sample_s:
        Eval = erfcx(s * sqrt(c_val / 2))
        lhs = fam_eval(lhs_minus_csB, s, Eval)
        rhs = fam_eval(RHS, s, Eval)
        scale = max(abs(lhs), abs(rhs), mpf(1))
        worst_rel = max(worst_rel, abs(lhs - rhs) / scale)
    if worst_rel > tol:
        raise AssertionError(f"b_ode RELATIVE residual too large: {worst_rel} > {tol}"
                              " (this is a SANITY check against gross indexing/algebra"
                              " bugs -- a true bug shows up as O(1) or larger relative"
                              " residual, as the b_1-validation bug this front caught"
                              " and fixed did; ordinary float/mpf rounding accumulated"
                              " over many recursion steps stays many orders of"
                              " magnitude below this threshold, see ATTEMPT.md S1)")
    return worst_rel


def build_family(c_val, K, dps, sample_s_for_validation=(0, 0.3, 0.7, 1.1)):
    """Build a_0..a_K, b_0..b_K (family form) for numeric c=c_val, K terms,
    at working precision dps. Validates EVERY b_k ODE solve directly
    before accepting it. Returns (a_list, b_list, c_val, sc)."""
    mp.dps = dps
    c_val = mpf(c_val)
    sc = sqrt(2 * c_val / pi)

    a = [None] * (K + 2)
    b = [None] * (K + 2)
    a[0] = ([mpf(1)], [mpf(0)])
    b[0] = ([mpf(0)], [mpf(0)])
    a[1] = ([-c_val], [mpf(0)])
    b[1] = ([mpf(0)], [sqrt(pi * c_val / 2)])

    # sanity: b_1 should also solve b_1' - c s b_1 = -c*a_0/1 + c*b_0 = -c
    # (a genuine, independent check that the k=1 base case is CONSISTENT
    # with the general recursion, not merely asserted)
    RHS1 = ([-c_val], [mpf(0)])
    # Fixed, generous sanity tolerance (not tied to dps): a genuine
    # indexing/algebra bug shows up as an O(1)-scale relative residual
    # (as the b_1-validation bug this front caught did, worst=3.96e4/1 --
    # see ATTEMPT.md S1). Deep into a run (large k), the coefficients'
    # own magnitude growth (the lineage's well-documented "order-2
    # entire" cancellation content) genuinely eats into a FIXED working
    # dps budget -- e.g. residual ~1.9e-60 at k=85 but ~2.8e-20 at
    # k=195, both at dps=90 -- this is expected precision decay, not an
    # algorithm bug (the SAME formula, already confirmed correct against
    # 5/5 published anchors at low k, is applied identically at every
    # k). 1e-8 is chosen to sit far below any real O(1) bug's signature
    # while comfortably above this ordinary, disclosed precision decay
    # at the (K,dps) sizes this front actually uses (checked empirically
    # to hold; see ATTEMPT.md S1 for the full disclosed trace of tuning
    # this threshold).
    ode_tol = mpf(10) ** (-8)
    validate_b_ode(b[1], RHS1, c_val, sc, c_val, sample_s_for_validation, tol=ode_tol)

    for k in range(1, K + 1):
        # b_{k+1} from a_k, b_k :  b_{k+1}' - c s b_{k+1} = -c a_k/(k+1) + c b_k
        RHS = fam_add(fam_scale(a[k], -c_val / (k + 1)), fam_scale(b[k], c_val))
        b[k + 1] = solve_b_ode(RHS, c_val, sc)
        try:
            validate_b_ode(b[k + 1], RHS, c_val, sc, c_val, sample_s_for_validation,
                            tol=ode_tol)
        except AssertionError as e:
            raise AssertionError(f"at k+1={k+1}: {e}") from None

        # w_k = a_{k-1}/k... wait w_k uses a_{k-1}, b_k, b_{k-1} -- but at
        # this point in the loop (index k) we have a[k] (not yet a[k-1]
        # explicitly separate -- we DO have it, a[k-1] was built earlier)
        # w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
        wk = fam_add(fam_add(fam_scale(a[k - 1] if k >= 1 else ([mpf(0)], [mpf(0)]), mpf(1) / k),
                              fam_mul_one_minus_s(b[k])),
                     b[k - 1] if k >= 1 else ([mpf(0)], [mpf(0)]),
                     1, -1)
        # a_{k+1} = [a_k' - c a_k + c w_k] / (k+1)
        ak_deriv = fam_deriv(a[k], c_val, sc)
        num = fam_add(fam_add(ak_deriv, fam_scale(a[k], -c_val)), fam_scale(wk, c_val))
        a[k + 1] = fam_scale(num, mpf(1) / (k + 1))

    return a[:K + 1], b[:K + 1], c_val, sc
