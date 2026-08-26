"""
REFEREE independent from-scratch implementation of the (P,Q)-family series
recursion described in ATTEMPT.md section 0 / section 3.1 (and cross-
described identically in the two required-reading ancestor documents).
No .py file of the target front or its lineage was read.

Recursion (restated from the front's own "established inputs" block,
transcribed as plain text, not copied from any script):

  Phi(s,g) = sum_k a_k(s) g^k,  Psi(s,g) = sum_k b_k(s) g^k
  a_0=1, b_0=0, a_1(s) = -c, b_1(s) = sqrt(pi c/2) * erfcx(s sqrt(c/2))
  a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
  w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
  every a_k, b_k in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials

Family algebra (re-derived by hand from the E'=csE-sc identity, matching
the prose description in the grandparent ATTEMPT.md sec 1.1, quoted
verbatim in the target's own sec 0):
  E(s) := erfcx(s*sqrt(c/2)),  sc := sqrt(2c/pi),  E' = c*s*E - sc
  (P + Q E)' = (P' - sc Q) + (Q' + c s Q) E

Solving b_k's ODE within the family (b_k = U + V E), RHS = A + B E:
  V' = B  =>  V = antideriv(B) + kappa   (antideriv has V(0)=0 by choice)
  U' - c s U = A + sc V =: R
  matching s^j coefficients: (j+1) u_{j+1} - c u_{j-1} = r_j
  solved DESCENDING from j = deg(R) down to j=1 (u_{deg R} := 0, i.e.
  deg U = deg R - 1), leaving the j=0 relation u_1 = r_0 = A_0 + sc*kappa
  (using antideriv(B)(0)=0) which PINS kappa = (u_1 - A_0)/sc.
"""
import mpmath as mp


# ---------- polynomial (coefficient-list, index = power of s) utilities ----

def p_trim(a):
    return a[:] if a else [mp.mpf(0)]

def p_add(a, b):
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        ai = a[i] if i < len(a) else mp.mpf(0)
        bi = b[i] if i < len(b) else mp.mpf(0)
        out.append(ai + bi)
    return out

def p_scale(a, k):
    return [ai * k for ai in a]

def p_shift_up(a):
    # multiply by s
    return [mp.mpf(0)] + a[:]

def p_mul_one_minus_s(a):
    # (1-s)*a(s) = a(s) - s*a(s)
    return p_add(a, p_scale(p_shift_up(a), mp.mpf(-1)))

def p_deriv(a):
    if len(a) <= 1:
        return [mp.mpf(0)]
    return [a[i] * i for i in range(1, len(a))]

def p_antideriv_zero_const(a):
    # integral with integration constant 0
    return [mp.mpf(0)] + [a[i] / (i + 1) for i in range(len(a))]

def p_eval(a, x):
    res = mp.mpf(0)
    for coeff in reversed(a):
        res = res * x + coeff
    return res


# ---------- family element: value = P(s) + Q(s)*E(s) -----------------------

class Fam:
    __slots__ = ("P", "Q")

    def __init__(self, P=None, Q=None):
        self.P = p_trim(P if P is not None else [mp.mpf(0)])
        self.Q = p_trim(Q if Q is not None else [mp.mpf(0)])

    def add(self, other):
        return Fam(p_add(self.P, other.P), p_add(self.Q, other.Q))

    def sub(self, other):
        return Fam(p_add(self.P, p_scale(other.P, -1)),
                    p_add(self.Q, p_scale(other.Q, -1)))

    def scale(self, k):
        return Fam(p_scale(self.P, k), p_scale(self.Q, k))

    def mul_one_minus_s(self):
        return Fam(p_mul_one_minus_s(self.P), p_mul_one_minus_s(self.Q))

    def deriv(self, c, sc):
        # (P + QE)' = (P' - sc Q) + (Q' + c s Q) E
        newP = p_add(p_deriv(self.P), p_scale(self.Q, -sc))
        newQ = p_add(p_deriv(self.Q), p_scale(p_shift_up(self.Q), c))
        return Fam(newP, newQ)

    def eval_at(self, s, c, erfcx_fn):
        Eval = erfcx_fn(s * mp.sqrt(c / 2))
        return p_eval(self.P, s) + p_eval(self.Q, s) * Eval


ZERO = Fam([mp.mpf(0)], [mp.mpf(0)])


def solve_bounded_branch(A, B, c, sc):
    """
    Solve b' - c*s*b = A + B*E for the unique polynomial-family (bounded)
    solution b = U + V*E, where A, B are plain coefficient lists
    (A = RHS.P, B = RHS.Q of the family element A_fam + B_fam*E, both
    already pure-polynomial by construction of the caller).
    """
    A = p_trim(A)
    B = p_trim(B)

    # V0 = antiderivative of B with V0(0) = 0 (so sc*V0's constant term = 0)
    V0 = p_antideriv_zero_const(B)

    # R0 := A + sc*V0  (R = R0 + sc*kappa, kappa only shifts constant term)
    R0 = p_add(A, p_scale(V0, sc))

    N = len(R0) - 1  # degree bound (trailing zeros harmless)
    # We seek U of degree <= N-1 with U' - c s U = R (only using j=1..N
    # equations to fill u_{N-1}..u_0 descending; j=0 equation pins kappa).
    if N <= 0:
        # R0 has no j>=1 content (or is entirely degree 0) -> U is
        # identically 0, and kappa is pinned directly by the j=0 relation
        # u_1 (=0, out of range) = r_0 = A_0 + sc*kappa.
        U = [mp.mpf(0)]
        u1 = mp.mpf(0)
    else:
        r = R0 + [mp.mpf(0)] * max(0, (N + 1) - len(R0))
        u = {-1: mp.mpf(0), N: mp.mpf(0), N + 1: mp.mpf(0)}
        for j in range(N, 0, -1):
            u_jp1 = u.get(j + 1, mp.mpf(0))
            u[j - 1] = ((j + 1) * u_jp1 - r[j]) / c
        U = [u.get(i, mp.mpf(0)) for i in range(N)]
        if not U:
            U = [mp.mpf(0)]
        u1 = u.get(1, mp.mpf(0))

    A0 = A[0] if A else mp.mpf(0)
    kappa = (u1 - A0) / sc

    V = p_add(V0, [kappa])  # add constant kappa to V0
    return Fam(U, V)


def build_series(c, K):
    """
    Build a_0..a_K, b_0..b_K as Fam objects, for a given numeric c
    (mpmath mpf) and truncation order K. Returns (a_list, b_list).
    """
    c = mp.mpf(c)
    sc = mp.sqrt(2 * c / mp.pi)

    a = [None] * (K + 1)
    b = [None] * (K + 1)

    a[0] = Fam([mp.mpf(1)], [mp.mpf(0)])
    b[0] = Fam([mp.mpf(0)], [mp.mpf(0)])
    a[1] = Fam([-c], [mp.mpf(0)])
    b[1] = Fam([mp.mpf(0)], [mp.sqrt(mp.pi * c / 2)])

    for k in range(1, K):
        # w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
        term1 = a[k - 1].scale(mp.mpf(1) / k)
        term2 = b[k].mul_one_minus_s()
        w_k = term1.add(term2).sub(b[k - 1])

        # a_{k+1} = [a_k' - c a_k + c w_k] / (k+1)
        a_kp1 = a[k].deriv(c, sc).sub(a[k].scale(c)).add(w_k.scale(c)).scale(mp.mpf(1) / (k + 1))
        a[k + 1] = a_kp1

        # b_{k+1}: RHS = -c a_k/(k+1) + c b_k =: A_fam + B_fam*E
        rhs = a[k].scale(-c / (k + 1)).add(b[k].scale(c))
        b_kp1 = solve_bounded_branch(rhs.P, rhs.Q, c, sc)
        b[k + 1] = b_kp1

    return a, b


# ---------- numerically-safe erfcx (mpmath has no builtin) -----------------

def erfcx_safe(z):
    z = mp.mpf(z)
    # direct: erfcx(z) = e^{z^2} erfc(z); fine for moderate z at our dps
    # for large z, mpmath's own erfc/exp still work at arbitrary precision
    # as long as dps is generous (mpmath handles the exponent internally),
    # so a single-branch implementation suffices here (unlike a fixed-width
    # float implementation, which would need an asymptotic series for
    # large z to avoid overflow).
    return mp.exp(z * z) * mp.erfc(z)


if __name__ == "__main__":
    mp.mp.dps = 70

    print("Self-test: build a,b up to K=6 at c=1000, print a_0..a_4 at s=0")
    a, b = build_series(1000, 6)
    for k in range(5):
        print(f"a_{k}(0) =", p_eval(a[k].P, 0) + p_eval(a[k].Q, 0) * erfcx_safe(0))
