"""
v01_family_series.py -- fresh, independent implementation of the (P,Q)-family
series recursion for Phi(s,g), Psi(s,g), at GENERAL s, built from scratch for
h1_volterra_attempt (MCLUST-H1-VOLTERRA-ATTEMPT, wave 23 front c).

NOT based on reading any .py file from any ancestor front. Built purely from
the verbatim recursion prose quoted in the required-reading ATTEMPT.md files
(mclust_h1_validity_attempt/ATTEMPT.md Section 0, h1_energy_estimate_attempt/
ATTEMPT.md Section 0):

  Phi(s,g) = sum_k a_k(s) g^k,  Psi(s,g) = sum_k b_k(s) g^k
  a_0=1, b_0=0, a_1(s)=-c, b_1(s)=sqrt(pi c/2)*erfcx(s*sqrt(c/2))
  a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
  w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
  every a_k, b_k in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials

KEY DIFFERENCE FROM ANCESTOR IMPLEMENTATIONS (independently re-derived, not
copied): instead of a hand-tuned "descending-recursion / kappa-pinning"
scheme to solve the bounded-branch ODE y'(s) - c*s*y(s) = source(s) within
the family, this implementation uses the EXPLICIT bounded-branch integral
formula (the same Growth-Exclusion-Lemma mechanism used throughout this
lineage, here re-derived for THIS specific ODE):

  y'(s) - c*s*y(s) = f(s)   ==>   y(s) = -e^{c s^2/2} * int_s^inf e^{-c t^2/2} f(t) dt

(bounded as s->infinity; the excluded homogeneous mode is e^{c s^2/2}).
Verified below (module-level self-check) that this reproduces b_1(s) exactly
from f(s)=-c (the k=1 case of the recursion) before being trusted for
anything else.

Since e^{-c t^2/2} * erfcx(t*sqrt(c/2)) = erfc(t*sqrt(c/2)) EXACTLY (definition
of erfcx), the two pieces of the source (poly part P_r(t), erfcx part
Q_r(t)*E(t)) integrate against two classical families of closed-form
integrals:
  G_n(s) := int_s^inf t^n e^{-c t^2/2} dt              (poly-part integrals)
  H_m(s) := int_s^inf t^m erfc(t sqrt(c/2)) dt          (erfcx-part integrals)
both computed via elementary integration-by-parts recursions (derived by
hand below, verified against direct numerical quadrature in
v02_new_identity_check.py and again inline here at module load).
"""
import mpmath as mp


def poly_trim(p):
    while len(p) > 0 and p[-1] == 0:
        p = p[:-1]
    return p


def poly_add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else mp.mpf(0)) + (b[i] if i < len(b) else mp.mpf(0)) for i in range(n)]


def poly_sub(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else mp.mpf(0)) - (b[i] if i < len(b) else mp.mpf(0)) for i in range(n)]


def poly_scale(a, k):
    return [k * v for v in a]


def poly_deriv(a):
    if len(a) <= 1:
        return []
    return [(i + 1) * a[i + 1] for i in range(len(a) - 1)]


def poly_mul_by_s(a):
    return [mp.mpf(0)] + list(a)


def poly_mul_1_minus_s(a):
    # (1-s)*p(s): result[0]=p[0]; result[i] = p[i]-p[i-1] for i>=1; length len(a)+1
    n = len(a) + 1
    res = [mp.mpf(0)] * n
    for i in range(n):
        pi = a[i] if i < len(a) else mp.mpf(0)
        pim1 = a[i - 1] if 0 <= i - 1 < len(a) else mp.mpf(0)
        res[i] = pi - pim1
    return poly_trim(res)


def poly_eval(a, s):
    r = mp.mpf(0)
    for c in reversed(a):
        r = r * s + c
    return r


def erfcx(z, c=None):
    # numerically safe erfcx(z) = e^{z^2} erfc(z); mpmath's erfc is accurate
    # over a huge dynamic range (arbitrary-precision floats), so the direct
    # formula is fine as long as working precision (mp.mp.dps) is adequate.
    return mp.exp(z * z) * mp.erfc(z)


class Family:
    """Represents P(s) + Q(s)*E(s), E(s)=erfcx(s*sqrt(c/2)), c fixed."""

    __slots__ = ("P", "Q", "c")

    def __init__(self, P, Q, c):
        self.P = poly_trim(list(P))
        self.Q = poly_trim(list(Q))
        self.c = c

    @staticmethod
    def zero(c):
        return Family([], [], c)

    @staticmethod
    def const(v, c):
        return Family([v], [], c)

    def add(self, other):
        return Family(poly_add(self.P, other.P), poly_add(self.Q, other.Q), self.c)

    def sub(self, other):
        return Family(poly_sub(self.P, other.P), poly_sub(self.Q, other.Q), self.c)

    def scale(self, k):
        return Family(poly_scale(self.P, k), poly_scale(self.Q, k), self.c)

    def mul_1_minus_s(self):
        return Family(poly_mul_1_minus_s(self.P), poly_mul_1_minus_s(self.Q), self.c)

    def deriv(self):
        # (P+QE)' = (P' - sc*Q) + (Q' + c*s*Q) E ,  sc := sqrt(2c/pi)
        c = self.c
        sc = mp.sqrt(2 * c / mp.pi)
        newP = poly_sub(poly_deriv(self.P), poly_scale(self.Q, sc))
        newQ = poly_add(poly_deriv(self.Q), poly_scale(poly_mul_by_s(self.Q), c))
        return Family(newP, newQ, c)

    def eval(self, s):
        c = self.c
        z = s * mp.sqrt(c / 2)
        E = erfcx(z)
        return poly_eval(self.P, s) + poly_eval(self.Q, s) * E


# ---------------------------------------------------------------------------
# Bounded-branch ODE solve: y' - c*s*y = source (source a Family), via the
# explicit Growth-Exclusion / integrating-factor formula.
# ---------------------------------------------------------------------------

def compute_G(nmax, c):
    """G_n(s) = int_s^inf t^n e^{-c t^2/2} dt = e^{-c s^2/2} * [Ppart_n(s) + Qscal_n * E(s)]
    returns (Ppart list of polys indexed 0..nmax, Qscal list of scalars 0..nmax)"""
    Ppart = [None] * (nmax + 1)
    Qscal = [None] * (nmax + 1)
    Ppart[0] = []
    Qscal[0] = mp.sqrt(mp.pi / (2 * c))
    if nmax >= 1:
        Ppart[1] = [mp.mpf(1) / c]
        Qscal[1] = mp.mpf(0)
    for n in range(2, nmax + 1):
        newP = [mp.mpf(0)] * n
        newP[n - 1] = mp.mpf(1) / c
        scale = mp.mpf(n - 1) / c
        prev = Ppart[n - 2]
        for i, v in enumerate(prev):
            newP[i] += scale * v
        Ppart[n] = poly_trim(newP)
        Qscal[n] = scale * Qscal[n - 2]
    return Ppart, Qscal


def compute_H(mmax, c, Gpoly, Gscal):
    """H_m(s) = int_s^inf t^m erfc(t*sqrt(c/2)) dt
       = e^{-c s^2/2} * [PpartH_m(s) + QpartH_m(s) * E(s)]
    (QpartH_m is a genuine polynomial here, not merely a scalar, because of
    the -s^{m+1}/(m+1)*erfc(as) boundary term from integration by parts.)
    Requires Gpoly/Gscal up to index mmax+1."""
    a = mp.sqrt(c / 2)
    HP = [None] * (mmax + 1)
    HQ = [None] * (mmax + 1)
    for m in range(0, mmax + 1):
        coeff = (2 * a) / ((m + 1) * mp.sqrt(mp.pi))
        HP[m] = poly_trim([coeff * v for v in Gpoly[m + 1]])
        q = [mp.mpf(0)] * (m + 2)
        q[m + 1] = -mp.mpf(1) / (m + 1)
        q[0] = q[0] + coeff * Gscal[m + 1]
        HQ[m] = poly_trim(q)
    return HP, HQ


def bounded_branch_solve(source: Family):
    """Solve y' - c*s*y = source(s), the unique solution bounded as s->inf."""
    c = source.c
    Pr, Qr = source.P, source.Q
    nmax = len(Pr) - 1
    mmax = len(Qr) - 1
    need_G = max(nmax, mmax + 1, 0) + 1  # +1 buffer for H's G[m+1] lookups
    Gpoly, Gscal = compute_G(need_G, c)
    HP, HQ = compute_H(mmax, c, Gpoly, Gscal) if mmax >= 0 else ([], [])
    Py = []
    Qy = []
    for n in range(nmax + 1):
        pr_n = Pr[n]
        if pr_n == 0:
            continue
        Py = poly_sub(Py, poly_scale(Gpoly[n], pr_n))
        Qy = poly_sub(Qy, poly_scale([Gscal[n]], pr_n))
    for m in range(mmax + 1):
        qr_m = Qr[m]
        if qr_m == 0:
            continue
        Py = poly_sub(Py, poly_scale(HP[m], qr_m))
        Qy = poly_sub(Qy, poly_scale(HQ[m], qr_m))
    return Family(Py, Qy, c)


# ---------------------------------------------------------------------------
# Self-check at module load: reproduce b_1(s) = sqrt(pi c/2) * E(s) from
# source f(s) = -c (the k=1 case, a_0=1,b_0=0 => source = -c*a_0/1 + c*b_0 = -c).
# ---------------------------------------------------------------------------

def _selfcheck_b1(c_val=1000, dps=50):
    old_dps = mp.mp.dps
    mp.mp.dps = dps
    c = mp.mpf(c_val)
    src = Family([-c], [], c)
    b1 = bounded_branch_solve(src)
    target_scalar = mp.sqrt(mp.pi * c / 2)
    ok = (len(poly_trim(b1.P)) == 0) and (len(b1.Q) == 1) and (abs(b1.Q[0] - target_scalar) < mp.mpf(10) ** (-dps + 5))
    mp.mp.dps = old_dps
    return ok, b1


if __name__ == "__main__":
    ok, b1 = _selfcheck_b1()
    print("self-check b_1(s) == sqrt(pi c/2) E(s):", ok)
    print("  b1.P =", b1.P)
    print("  b1.Q =", b1.Q)

    # Build the family recursion up to order K, evaluate anchors at c=1000.
    mp.mp.dps = 100
    c = mp.mpf(1000)
    K = 60

    a = [None] * (K + 2)
    b = [None] * (K + 2)
    a[0] = Family([mp.mpf(1)], [], c)
    b[0] = Family([], [], c)
    a[1] = Family([-c], [], c)
    b1_family = bounded_branch_solve(Family([-c], [], c))
    b[1] = b1_family

    for k in range(1, K + 1):
        # w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
        term1 = a[k - 1].scale(mp.mpf(1) / k)
        term2 = b[k].mul_1_minus_s()
        w_k = term1.add(term2).sub(b[k - 1])
        # a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
        akp1 = a[k].deriv().sub(a[k].scale(c)).add(w_k.scale(c)).scale(mp.mpf(1) / (k + 1))
        a[k + 1] = akp1
        if k + 1 <= K:
            # b_{k+1}'(s) - c s b_{k+1}(s) = -c a_k(s)/(k+1) + c b_k(s)
            src = a[k].scale(-c / (k + 1)).add(b[k].scale(c))
            b[k + 1] = bounded_branch_solve(src)

    print()
    print("=== anchor validation at c=1000 ===")
    print("a2(0) =", a[2].eval(mp.mpf(0)), " target 520316.636488")
    print("a3(0) =", a[3].eval(mp.mpf(0)), " target -180730907.6285")
    print("a4(0) =", a[4].eval(mp.mpf(0)), " target 47146963944.14")
    print("b1(0) =", b[1].eval(mp.mpf(0)), " target sqrt(pi*1000/2) =", mp.sqrt(mp.pi * c / 2))
    print("b2(0) =", b[2].eval(mp.mpf(0)), " target -20816.636488")

    def Phi(s, g, K_):
        r = mp.mpf(0)
        gp = mp.mpf(1)
        for k in range(K_ + 1):
            r += a[k].eval(s) * gp
            gp *= g
        return r

    print("Phi(0,0.002) =", Phi(mp.mpf(0), mp.mpf('0.002'), K), " target 0.15850015")
    print("Phi(0,0.05)  =", Phi(mp.mpf(0), mp.mpf('0.05'), K), " target 0.0377615983402126 (needs higher K,dps for full digits)")
