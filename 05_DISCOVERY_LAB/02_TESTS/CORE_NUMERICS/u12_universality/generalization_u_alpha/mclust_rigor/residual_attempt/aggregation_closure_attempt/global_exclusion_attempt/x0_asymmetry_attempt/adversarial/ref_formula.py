"""REFEREE, independent re-implementation of the M-CLUST(b) finite-n formulas.

Adversarial review of `x0_asymmetry_attempt/ATTEMPT.md` sec 5.1-5.2.

Written from the PRIMARY sources only:
  * `generalization_u_alpha/DERIVATIONS.md` sec 0-1   (master formula M-q)
  * `mclust_rigor/DERIVATION_MCLUST_FIXED.md` sec 1-4 (rho, rho_start,
    the sliding-window rate c, q_CLUST(s) = s/(1-rho))
  * `mclust_rigor/residual_attempt/ATTEMPT.md` sec 6  (multiplicative
    elevation P = 1/(1-rho), phi_V4, phi_CAND = (1-rho) phi_V4)

Nothing is imported from, or copied out of, `x0_asym_formula.py`,
`x0_asym_candidate.py`, `mclust_residual_v4.py`, `mclust_global_formula.py`
or any other script of the lineage.

--------------------------------------------------------------------------
DELIBERATE METHOD DIFFERENCE (this is the point of the exercise)
--------------------------------------------------------------------------
The target computes H(t) by an inner 250-point TRAPEZOID rule and phi by an
outer 400-point TRAPEZOID rule on a uniform grid.  Here H(t) is obtained in
CLOSED FORM (the inner integral is elementary), and the remaining
one-dimensional integral is done with adaptive Gauss-Kronrod (scipy.quad,
epsabs=epsrel=1e-13) and independently with mpmath at 40 decimal digits.
So a quadrature error in the target shows up as a disagreement rather than
being inherited.

Own derivation of the closed form (re-done here, not taken from anywhere):

    P      := 1/(1-rho)                       (elevation, residual_attempt)
    q(s)   := s/(1-rho) = P s                 (wave 4; NOT clipped at 1 --
                                               the convention phi_CAND uses)
    H(t)    = t - (1-t)^P * I(t),
    I(t)   := int_0^t (1-q(s)) (1-s)^-P ds

    substitute u = 1-s, so 1-q(s) = 1-P(1-u) = (1-P) + P u :

    I(t) = int_{1-t}^{1} [(1-P) + P u] u^-P du
         = [1 - (1-t)^(1-P)] + (P/(2-P)) [1 - (1-t)^(2-P)]        (P != 1,2)

    hence, using (1-t)^P (1-t)^(1-P) = (1-t) and (1-t)^P (1-t)^(2-P) = (1-t)^2,

    H(t) = t + (1-t) - (1-t)^P - (P/(2-P)) [(1-t)^P - (1-t)^2]
         = 1 - (2/(2-P)) (1-t)^P + (P/(2-P)) (1-t)^2              (*)

    checks:  H(0) = 1 - 2/(2-P) + P/(2-P) = 0            ok
             H(1-) = 1                                    ok  (P > 0)
             P = 1 (rho = 0):  1 - 2(1-t) + (1-t)^2 = t^2  ok  (recovers M-U)

    phi_V4 = int_0^1 P (1-t)^(P-1) exp(-c H(t)) dt
    T      = int_0^1 (1-t)^P     exp(-c H(t)) dt   ( = E[traversed mass] )
    phi_CAND = (1-rho) * phi_V4                                   (eps = 0)

The P = 2 case (rho = 1/2 exactly) is handled by a logarithmic limit; it
does not occur in any cell of the grids used.
"""
import math

import numpy as np
from scipy import integrate

try:
    import mpmath as mp
except ImportError:                                   # pragma: no cover
    mp = None


# ---------------------------------------------------------------- mechanism
def rho_of(c, n, b):
    """rho = |R|/n = 1 - (1-c/n)^b.  Exact (wave 4 sec 1)."""
    return 1.0 - (1.0 - c / n) ** b


def rho_start_of(c, n, b):
    """run-start density = (c/n)(1-c/n)^b = (c/n)(1-rho).  Exact (wave 4)."""
    return (c / n) * (1.0 - c / n) ** b


# ---------------------------------------------------------------- H closed form
def H_closed(t, P):
    """Equation (*) above: H(t) for the elevated-hazard model with q(s)=Ps."""
    omt = 1.0 - t
    if abs(P - 2.0) < 1e-12:
        # limit P->2 :  H = 1 - (1-t)^2 [1 - 2 ln(1-t)]  ... derived as the
        # limit of (*) via l'Hopital in (2-P); guarded, unused on our grids.
        if omt <= 0.0:
            return 1.0
        return 1.0 - omt * omt * (1.0 - 2.0 * math.log(omt))
    return 1.0 - (2.0 / (2.0 - P)) * omt ** P + (P / (2.0 - P)) * omt * omt


def _integrand_phi(u, c, P):
    """phi_V4 integrand in u = 1-t :  P u^(P-1) exp(-c H)."""
    H = 1.0 - (2.0 / (2.0 - P)) * u ** P + (P / (2.0 - P)) * u * u
    return P * u ** (P - 1.0) * math.exp(-c * H)


def _integrand_T(u, c, P):
    """T integrand in u = 1-t :  u^P exp(-c H)."""
    H = 1.0 - (2.0 / (2.0 - P)) * u ** P + (P / (2.0 - P)) * u * u
    return u ** P * math.exp(-c * H)


def phi_V4_and_T(c, n, b, tol=1e-13):
    """(phi_V4, T) by adaptive Gauss-Kronrod on the closed-form H."""
    rho = rho_of(c, n, b)
    P = 1.0 / (1.0 - rho)
    # the integrand is concentrated near u = 1 (t = 0) with width ~ 1/sqrt(cP);
    # give quad the break point so it never misses the peak.
    w = min(1.0, 8.0 / math.sqrt(max(c * P, 1.0)))
    pts = [0.0, max(0.0, 1.0 - 4.0 * w), max(0.0, 1.0 - w), 1.0]
    pts = sorted(set(pts))
    phi = 0.0
    T = 0.0
    for a, bnd in zip(pts[:-1], pts[1:]):
        v, _ = integrate.quad(_integrand_phi, a, bnd, args=(c, P),
                              epsabs=tol, epsrel=tol, limit=400)
        phi += v
        v, _ = integrate.quad(_integrand_T, a, bnd, args=(c, P),
                              epsabs=tol, epsrel=tol, limit=400)
        T += v
    return phi, T


def phi_U(c, tol=1e-14):
    """M-U reference, int_0^1 exp(-c t^2) dt."""
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0.0, 1.0,
                          epsabs=tol, epsrel=tol, limit=400)
    return v


# ---------------------------------------------------------------- formulas
def phi_CAND(c, n, b):
    """Formula of record (residual_attempt sec 6): (1-rho) * phi_V4, eps = 0."""
    rho = rho_of(c, n, b)
    if rho < 1e-14:
        return phi_U(c)
    v4, _T = phi_V4_and_T(c, n, b)
    return (1.0 - rho) * v4


def eps_target(c, n, b):
    """The TARGET's leading-order eps (ATTEMPT.md sec 5.2), recomputed here:

        eps = (rho_start/rho) phi_cond + (c/((1-rho) n)) T
    """
    rho = rho_of(c, n, b)
    v4, T = phi_V4_and_T(c, n, b)
    rs = rho_start_of(c, n, b)
    return (rs / rho) * v4 + (c / ((1.0 - rho) * n)) * T


def phi_EPS(c, n, b):
    """The TARGET's candidate, recomputed independently."""
    rho = rho_of(c, n, b)
    if rho < 1e-14:
        return phi_U(c)
    v4, T = phi_V4_and_T(c, n, b)
    rs = rho_start_of(c, n, b)
    eps = (rs / rho) * v4 + (c / ((1.0 - rho) * n)) * T
    return (1.0 - rho) * v4 + rho * eps


# ---------------------------------------------------------------------------
# REFEREE'S OWN CORRECTION TO BOTH CHANNELS (derived independently; see
# REFEREE_REPORT.md sec 4).
#
# (a) RUN-START CHANNEL.  The target asserts P(cyclic | x0 a run start) =
#     phi_cond "at leading order", on the grounds that x0 is a live target
#     from t = 0 with the same elevation.  That part is right, but it is only
#     half the comparison.  For x0 NOT in R the walk STARTS AT x0, so x0 is
#     simultaneously the unique live target AND the start of the arc being
#     traversed: exactly ONE live target at t = 0.  For x0 a RUN START the
#     walk starts with an f-draw to a fresh point D1, and D1 is itself a live
#     closure target (closing into D1 kills), so there are TWO live targets
#     at t = 0.  In the master formula's own bookkeeping this is precisely
#     "one extra reroute event forced at s = 0": its per-event factor is
#         F(0) = (1 - q(0)) ((1-t)/(1-0))^P = (1-t)^P     (q(0) = 0)
#     so the survival curve of the run-start walk is
#         S_rs(t) = (1-t)^P * S_cond(t) = (1-t)^(2P) exp(-c H(t))
#     and therefore
#         phi_runstart = int_0^1 P (1-t)^(2P-1) exp(-c H(t)) dt   <  phi_cond.
#     This is NOT a subleading correction: the ratio phi_runstart/phi_cond is
#     0.82 at c = 10 and ~0.95 at c = 400.
#
# (b) F-DRAW CHANNEL.  E[#f-draws] = (c/(1-rho)) T counts only the reroute
#     events the walk MEETS later, at rate c per unit traversed mass.  But
#     the walk from an x0 in R begins with a draw at x0 itself, and that
#     opening chain makes 1/(1-rho) draws in expectation before the walk has
#     traversed any mass at all.  Hence E[#f-draws] = (1 + c T)/(1-rho).
# ---------------------------------------------------------------------------
def _integrand_phirs(u, c, P):
    H = 1.0 - (2.0 / (2.0 - P)) * u ** P + (P / (2.0 - P)) * u * u
    return P * u ** (2.0 * P - 1.0) * math.exp(-c * H)


def phi_runstart(c, n, b, tol=1e-13):
    """P(cyclic | x0 is a run start), referee's leading order (see (a))."""
    rho = rho_of(c, n, b)
    P = 1.0 / (1.0 - rho)
    w = min(1.0, 8.0 / math.sqrt(max(c * P, 1.0)))
    pts = sorted(set([0.0, max(0.0, 1.0 - 4.0 * w), max(0.0, 1.0 - w), 1.0]))
    tot = 0.0
    for a, bnd in zip(pts[:-1], pts[1:]):
        v, _ = integrate.quad(_integrand_phirs, a, bnd, args=(c, P),
                              epsabs=tol, epsrel=tol, limit=400)
        tot += v
    return tot


def eps_ref(c, n, b):
    """Referee's leading-order eps, both channels corrected."""
    rho = rho_of(c, n, b)
    _v4, T = phi_V4_and_T(c, n, b)
    rs = rho_start_of(c, n, b)
    return (rs / rho) * phi_runstart(c, n, b) + (1.0 + c * T) / ((1.0 - rho) * n)


def phi_EPSR(c, n, b):
    """phi_CAND + rho * eps_ref  (referee's corrected counterpart of phi_EPS)."""
    rho = rho_of(c, n, b)
    if rho < 1e-14:
        return phi_U(c)
    v4, _T = phi_V4_and_T(c, n, b)
    return (1.0 - rho) * v4 + rho * eps_ref(c, n, b)


CANDIDATES = {"CAND": phi_CAND, "EPS": phi_EPS, "EPSR": phi_EPSR}


# ---------------------------------------------------------------- mpmath audit
def phi_V4_and_T_mp(c, n, b, dps=40):
    """Same two integrals at `dps` decimal digits with mpmath (independent of
    scipy).  Used only as an audit of the quadrature, it is slow."""
    if mp is None:                                    # pragma: no cover
        return None, None
    with mp.workdps(dps):
        rho = mp.mpf(1) - (mp.mpf(1) - mp.mpf(c) / n) ** b
        P = 1 / (1 - rho)
        cc = mp.mpf(c)

        def Hm(u):
            return 1 - (2 / (2 - P)) * u ** P + (P / (2 - P)) * u ** 2

        fphi = lambda u: P * u ** (P - 1) * mp.e ** (-cc * Hm(u))
        fT = lambda u: u ** P * mp.e ** (-cc * Hm(u))
        a = mp.mpf(1) - mp.mpf(20) / mp.sqrt(cc * P)
        if a < 0:
            a = mp.mpf(0)
        pv = mp.quad(fphi, [0, a, 1])
        tv = mp.quad(fT, [0, a, 1])
        return float(pv), float(tv)


if __name__ == "__main__":
    print("=== ref_formula.py self-checks ===")
    print("\n[1] H closed form vs direct numerical inner integral")
    for (nn, bb, cc) in [(65536, 100, 400.0), (65536, 100, 600.0),
                         (65536, 400, 100.0), (32768, 8, 160.0)]:
        rho = rho_of(cc, nn, bb)
        P = 1.0 / (1.0 - rho)
        for t in (0.001, 0.01, 0.05, 0.2, 0.6, 0.95):
            inner, _ = integrate.quad(
                lambda s: (1.0 - P * s) * (1.0 - s) ** (-P), 0.0, t,
                epsabs=1e-14, epsrel=1e-14, limit=400)
            Hnum = t - (1.0 - t) ** P * inner
            Hcf = H_closed(t, P)
            assert abs(Hnum - Hcf) < 1e-10 * max(1.0, abs(Hcf)), (t, Hnum, Hcf)
        print(f"   b={bb:3d} c={cc:6.1f} rho={rho:.4f} P={P:.4f}: closed form"
              f" == numeric inner integral to <1e-10 at 6 values of t   OK")

    print("\n[2] rho -> 0 must recover phi_U exactly")
    for c in (10.0, 50.0, 200.0, 600.0):
        v = phi_CAND(c, 10 ** 12, 1)
        print(f"   c={c:6.1f}: phi_CAND(n=1e12,b=1)={v:.12f}  phi_U={phi_U(c):.12f}"
              f"  diff={v - phi_U(c):+.2e}")

    print("\n[3] scipy quad vs mpmath (40 dps), phi_V4 and T")
    for (nn, bb, cc) in [(65536, 100, 400.0), (65536, 300, 150.0),
                         (65536, 100, 600.0), (65536, 400, 100.0),
                         (65536, 200, 5.0), (32768, 8, 10.0)]:
        a, b_ = phi_V4_and_T(cc, nn, bb)
        am, bm = phi_V4_and_T_mp(cc, nn, bb)
        print(f"   b={bb:3d} c={cc:6.1f}: phi_V4 {a:.12f} vs {am:.12f}"
              f" (rel {abs(a-am)/am:.1e}) | T {b_:.12f} vs {bm:.12f}"
              f" (rel {abs(b_-bm)/bm:.1e})")
