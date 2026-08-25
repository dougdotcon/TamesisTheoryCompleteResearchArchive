#!/usr/bin/env python3
"""
r01_family_series.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT (DISC-DEC-072)

Fresh, from-scratch implementation of the b=1 floor abstract-process series
recursion INSIDE the closed family
    F = { P(s) + Q(s) * E(s) : P, Q polynomials },   E(s) = erfcx(s*sqrt(c/2)),
re-derived from the prose of record only (mandate; no script of the wave-16
front or its referee was opened).

Established recursion (referee-proved, session-verified; restated in the
wave-17 mandate):
    a_0 = 1, a_1 = -c, b_0 = 0,
    for k >= 1:
        b_k' - c s b_k = -c a_{k-1}/k + c b_{k-1}      (bounded branch)
        w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
        a_{k+1} = [a_k' - c a_k + c w_k]/(k+1)
    Phi(0,t0) = sum_k a_k(0) t0^k.

Own re-derivation of the family solve (independent of the referee's script):
  E'(s) = c s E(s) - sqrt(2c/pi)                        [erfcx' identity]
  hence in F:  (P + Q E)' = (P' - sc*Q) + (Q' + c s Q) E,  sc := sqrt(2c/pi).
  Bounded-branch solve of  b' - c s b = A(s) + B(s) E(s)  with b = U + V E:
     E-part:      V' = B          => V = int B + kappa   (kappa = const, free)
     non-E part:  U' - c s U - sc V = A.
  Writing R := A + sc*(int B)  (kappa excluded; kappa only enters the s^0
  coefficient), matching s^j coefficients of U' - c s U = R + sc*kappa*[j=0]:
     (j+1) u_{j+1} - c u_{j-1} = r_j
  gives, descending from j = d := deg R (with u_j = 0 for j >= d):
     u_{j-1} = ((j+1) u_{j+1} - r_j)/c ,   j = d, d-1, ..., 1
  and the leftover j = 0 relation  u_1 = r_0 + sc*kappa  PINS kappa:
     kappa = (u_1 - r_0)/sc .
  The polynomial ansatz automatically discards the exp(c s^2/2) homogeneous
  branch, i.e. selects the bounded branch; within F the solution is unique.

Everything is deterministic. No randomness anywhere in this front.
"""

from mpmath import mp, mpf, sqrt, pi, erfc, exp, fabs, log10
import json
import sys
import time

# ---------------------------------------------------------------- poly utils
# polynomials = python lists of mpf, index = power of s


def padd(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else mp.zero) + (q[i] if i < len(q) else mp.zero)
            for i in range(n)]


def pscale(p, x):
    return [ci * x for ci in p]


def pderiv(p):
    return [p[i] * i for i in range(1, len(p))]


def pint(p):
    """antiderivative with zero constant term"""
    return [mp.zero] + [p[i] / (i + 1) for i in range(len(p))]


def pshift(p):
    """multiply by s"""
    return [mp.zero] + list(p)


def pone_minus_s(p):
    """multiply by (1 - s)"""
    return padd(p, pscale(pshift(p), mpf(-1)))


def peval(p, x):
    acc = mp.zero
    for c in reversed(p):
        acc = acc * x + c
    return acc


# ------------------------------------------------------------ family algebra
class FamilyRecursion:
    def __init__(self, c):
        self.c = mpf(c)
        self.sc = sqrt(2 * self.c / pi)          # sqrt(2c/pi)
        self.rt = sqrt(pi * self.c / 2)          # sqrt(pi c / 2) = c / sc

    def deriv_F(self, PQ):
        P, Q = PQ
        dP = padd(pderiv(P), pscale(Q, -self.sc))
        dQ = padd(pderiv(Q), pscale(pshift(Q), self.c))
        return (dP, dQ)

    def bsolve(self, A, B):
        """bounded-branch solve of b' - c s b = A + B E, returns (U, V)."""
        c = self.c
        V0 = pint(B)                              # kappa not yet included
        R = padd(A, pscale(V0, self.sc))
        # trim exact trailing zeros (structural only; mpf zeros are exact
        # when produced by padding)
        while len(R) > 1 and R[-1] == 0:
            R.pop()
        d = len(R) - 1
        u = [mp.zero] * (d + 2)
        for j in range(d, 0, -1):
            u[j - 1] = ((j + 1) * u[j + 1] - R[j]) / c
        r0 = R[0] if R else mp.zero
        kappa = (u[1] - r0) / self.sc
        U = u[:max(d, 1)]
        while len(U) > 1 and U[-1] == 0:
            U.pop()
        V = list(V0)                              # pint() always returns >=1 term
        V[0] = V[0] + kappa
        return (U, V)

    def run(self, K, keep_polys_at=()):
        """run recursion to a_K; return dict with a_k(0), b_k(0) lists and
        optionally full (P,Q) polys at selected orders."""
        c = self.c
        a_prev = ([mpf(1)], [])                   # a_0
        a_cur = ([-c], [])                        # a_1
        b_prev = ([], [])                         # b_0
        a0_vals = [mpf(1), -c]
        b0_vals = [mp.zero]
        kept = {}
        for k in range(1, K):
            # b_k
            A = padd(pscale(a_prev[0], -c / k), pscale(b_prev[0], c))
            B = padd(pscale(a_prev[1], -c / k), pscale(b_prev[1], c))
            b_cur = self.bsolve(A, B)
            b0_vals.append((b_cur[0][0] if b_cur[0] else mp.zero)
                           + (b_cur[1][0] if b_cur[1] else mp.zero))
            # w_k
            wP = padd(padd(pscale(a_prev[0], mpf(1) / k),
                           pone_minus_s(b_cur[0])), pscale(b_prev[0], mpf(-1)))
            wQ = padd(padd(pscale(a_prev[1], mpf(1) / k),
                           pone_minus_s(b_cur[1])), pscale(b_prev[1], mpf(-1)))
            # a_{k+1}
            dP, dQ = self.deriv_F(a_cur)
            nP = pscale(padd(padd(dP, pscale(a_cur[0], -c)), pscale(wP, c)),
                        mpf(1) / (k + 1))
            nQ = pscale(padd(padd(dQ, pscale(a_cur[1], -c)), pscale(wQ, c)),
                        mpf(1) / (k + 1))
            a_next = (nP, nQ)
            a0_vals.append((nP[0] if nP else mp.zero)
                           + (nQ[0] if nQ else mp.zero))
            if k in keep_polys_at:
                kept[k] = {'b': b_cur, 'a_next': a_next}
            a_prev, a_cur, b_prev = a_cur, a_next, b_cur
        return {'a0': a0_vals, 'b0': b0_vals, 'kept': kept}


def sum_series(a0_vals, t0):
    """sum Phi(0,t0) = sum a_k(0) t0^k; return (value, max|term|, |last term|)"""
    t0 = mpf(t0)
    acc = mp.zero
    tp = mpf(1)
    mx = mp.zero
    last = mp.zero
    for ak in a0_vals:
        term = ak * tp
        acc += term
        a = fabs(term)
        if a > mx:
            mx = a
        last = a
        tp *= t0
    return acc, mx, last


# --------------------------------------------------------------- validation
def validate_anchors():
    """Validate against the published anchors (c=1000) from the record."""
    print("=" * 70)
    print("VALIDATION vs published anchors, c=1000")
    print("=" * 70)
    mp.dps = 60
    fr = FamilyRecursion(1000)
    out = fr.run(60, keep_polys_at=(2, 3))
    a0 = out['a0']
    b0 = out['b0']
    c = mpf(1000)
    rt = sqrt(pi * c / 2)
    checks = []

    def chk(name, got, want, tol):
        ok = fabs(got - want) <= tol * max(mpf(1), fabs(want))
        checks.append(ok)
        print(f"  {name:28s} got {mp.nstr(got, 16):>24s}  want {want}  "
              f"{'OK' if ok else 'FAIL'}")

    # published numeric anchors
    chk("a_2(0)", a0[2], mpf('520316.636488'), mpf('1e-11'))
    chk("a_3(0)", a0[3], mpf('-180730907.6285'), mpf('1e-12'))
    chk("a_4(0)", a0[4], mpf('47146963944.14'), mpf('1e-12'))
    chk("b_2(0)", b0[2], mpf('-20816.636488'), mpf('1e-11'))
    # closed forms of record (referee, prose): b_2(s), a_3(0), b_1 = psi1
    chk("b_1(0) = sqrt(pi c/2)", b0[1], rt, mpf('1e-50'))
    a3_exact = -(c**3 / 2 + 5 * c**2 / 2 + (c**2 + 3 * c / 2) * rt) / 3
    chk("a_3(0) closed form", a0[3], a3_exact, mpf('1e-50'))
    b2_exact0 = -c - (c / 2) * rt          # b2(0) = -c - (c/2) sqrt(pi c/2)
    chk("b_2(0) closed form", b0[2], b2_exact0, mpf('1e-50'))
    # b_2(s) at s=0.3 vs closed form -c - (c/2) rt (1-2s) erfcx(s sqrt(c/2))
    kept = out['kept'][2]['b']
    s = mpf('0.3')
    E = exp(c * s**2 / 2) * erfc(s * sqrt(c / 2))
    got = peval(kept[0], s) + peval(kept[1], s) * E
    want = -c - (c / 2) * rt * (1 - 2 * s) * E
    chk("b_2(0.3) closed form", got, want, mpf('1e-45'))
    # referee's printed b_3(s):
    # c^2(8-7s)/12 + sqrt(2 pi) c^{3/2} (7cs^2-8cs+2c+7)/24 * E
    kept3 = out['kept'][3]['b'] if 3 in out['kept'] else None
    if kept3:
        got = peval(kept3[0], s) + peval(kept3[1], s) * E
        want = c**2 * (8 - 7 * s) / 12 \
            + sqrt(2 * pi) * c**mpf('1.5') * (7 * c * s**2 - 8 * c * s
                                              + 2 * c + 7) / 24 * E
        chk("b_3(0.3) closed form", got, want, mpf('1e-40'))
    # series value anchor
    v, mx, last = sum_series(a0, mpf('0.002'))
    chk("Phi(0,0.002)", v, mpf('0.15850015'), mpf('5e-8'))
    print(f"  anchors: {sum(checks)}/{len(checks)} OK")
    return all(checks)


def validate_plateau_quick():
    print("=" * 70)
    print("QUICK plateau check, c=1000 (low precision)")
    print("=" * 70)
    mp.dps = 120
    t = time.time()
    fr = FamilyRecursion(1000)
    out = fr.run(700)
    ok = True
    for t0 in ('0.03', '0.05'):
        v, mx, last = sum_series(out['a0'], mpf(t0))
        print(f"  Phi(0,{t0}) = {mp.nstr(v, 20)}   max|term| ~ 1e{int(log10(mx))}"
              f"  last|term| ~ 1e{int(log10(last)) if last > 0 else -999}")
        ok = ok and fabs(v - mpf('0.0377615983')) < mpf('1e-9')
    print(f"  plateau anchor 0.0377615983: {'OK' if ok else 'FAIL'}"
          f"   ({time.time()-t:.1f}s)")
    return ok


if __name__ == '__main__':
    ok1 = validate_anchors()
    ok2 = validate_plateau_quick()
    print()
    print(f"ALL VALIDATION: {'PASS' if (ok1 and ok2) else 'FAIL'}")
    sys.exit(0 if (ok1 and ok2) else 1)
