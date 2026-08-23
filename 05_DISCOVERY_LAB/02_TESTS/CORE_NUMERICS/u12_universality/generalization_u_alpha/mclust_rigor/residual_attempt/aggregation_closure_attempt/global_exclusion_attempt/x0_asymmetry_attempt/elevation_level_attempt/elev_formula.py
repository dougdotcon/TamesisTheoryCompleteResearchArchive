#!/usr/bin/env python3
"""
elev_formula.py -- closed forms for wave 10 front (a) `MCLUST-ELEVATION-LEVEL-ATTEMPT`.

Own implementation.  Nothing is imported from `residual_attempt/`,
`aggregation_closure_attempt/`, `global_exclusion_attempt/`,
`x0_asymmetry_attempt/`, `x0_asymmetry_attempt/adversarial/`, `mclust_rigor/`,
or `ualpha_sim.py`.

REUSE, explicitly labelled (formula constants re-transcribed from their stated
closed forms, not code):
  * rho        = 1-(1-c/n)^b                      (wave 4, exact)
  * rho_start  = (c/n)(1-c/n)^b = (c/n)(1-rho)    (wave 4, exact)
  * q_CLUST(s) = s/(1-rho), un-clipped            (wave 4 SS3)
  * P_lead     = 1/(1-rho)                        (residual_attempt SS6)
  * P_exact    = (1-c/n)^{-(b-1)}                 (aggregation_closure SS3)
  * H(t) closed form                              (adversarial/REFEREE_REPORT SS1(i))
        H(t) = 1 - (2/(2-P))(1-t)^P + (P/(2-P))(1-t)^2
  * phi_V4, T, phi_runstart, eps_ref, phi_EPSR    (REFEREE_REPORT SS1(i), SS4.1)

NEW here (this front, derived in DERIVATION_PREREG.md SS2-SS5):
  * lam_pred(t)  -- the t-dependent per-target elevation
  * phi_RED      -- the reduction formula   (1-rho) phi_U(c') + rho eps_RED
"""
import math
import numpy as np
from scipy import integrate, special

# ----------------------------------------------------------------------------
# mechanism constants (REUSE: wave 4, exact)
# ----------------------------------------------------------------------------


def rho_of(b, c, n):
    return 1.0 - (1.0 - c / n) ** b


def rho_start_of(b, c, n):
    return (c / n) * (1.0 - c / n) ** b


def P_lead(b, c, n):
    return 1.0 / (1.0 - rho_of(b, c, n))


def P_exact(b, c, n):
    return (1.0 - c / n) ** (-(b - 1))


# ----------------------------------------------------------------------------
# the master formula with a CONSTANT elevation P  (REUSE: referee SS1(i))
# ----------------------------------------------------------------------------


def H_const_P(t, P):
    """H(t) = t - (1-t)^P * int_0^t (1-Ps)(1-s)^{-P} ds, closed form.

    Written with log1p/expm1 so that it is stable at P -> 1 and P -> 2.
    """
    t = np.asarray(t, dtype=float)
    L = np.log1p(-t)                      # log(1-t)  <= 0
    a = 1.0 - P
    d = 2.0 - P
    # guard the removable singularities of the two ratios
    if abs(d) < 1e-9:
        d = math.copysign(1e-9, d if d != 0.0 else 1.0)
    I = -np.expm1(a * L) - P * np.expm1(d * L) / d
    return t - np.exp(P * L) * I


def _quad(f, a=0.0, b=1.0):
    v, _ = integrate.quad(f, a, b, epsabs=1e-13, epsrel=1e-13, limit=400)
    return v


def phi_V4(b, c, n):
    """phi(cyclic | x0 not in R) under the CONSTANT-elevation ansatz, P = P_lead.
    REUSE: residual_attempt SS6 / referee SS1(i)."""
    P = P_lead(b, c, n)
    return _quad(lambda t: P * (1.0 - t) ** (P - 1.0) * math.exp(-c * H_const_P(t, P)))


def T_V4(b, c, n):
    """T = int_0^1 (1-t)^P e^{-cH} dt.  REUSE: referee SS1(i)."""
    P = P_lead(b, c, n)
    return _quad(lambda t: (1.0 - t) ** P * math.exp(-c * H_const_P(t, P)))


def phi_runstart_V4(b, c, n):
    """One extra forced reroute event at s=0.  REUSE: referee SS4.1(a)."""
    P = P_lead(b, c, n)
    return _quad(lambda t: P * (1.0 - t) ** (2.0 * P - 1.0)
                 * math.exp(-c * H_const_P(t, P)))


def phi_CAND(b, c, n):
    """REUSE: residual_attempt SS6, the (1-rho) dilution with eps = 0."""
    return (1.0 - rho_of(b, c, n)) * phi_V4(b, c, n)


def phi_EPSR(b, c, n):
    """The formula of record (DISC-DEC-044).  REUSE: referee SS4.1/SS10."""
    r = rho_of(b, c, n)
    rs = rho_start_of(b, c, n)
    T = T_V4(b, c, n)
    eps = (rs / r) * phi_runstart_V4(b, c, n) + (1.0 + c * T) / ((1.0 - r) * n)
    return (1.0 - r) * phi_V4(b, c, n) + r * eps


# ----------------------------------------------------------------------------
# NEW (this front): the reduction  M-CLUST(b) | x0 not in R  ==  M-U(c', n')
# ----------------------------------------------------------------------------


def phi_U(c):
    """int_0^1 e^{-c u^2} du, exact."""
    if c <= 0:
        return 1.0
    return 0.5 * math.sqrt(math.pi / c) * math.erf(math.sqrt(c))


def T_U(c):
    """int_0^1 (1-u) e^{-c u^2} du = phi_U(c) - (1-e^{-c})/(2c), exact."""
    if c <= 0:
        return 0.5
    return phi_U(c) - (-math.expm1(-c)) / (2.0 * c)


def c_eff(b, c, n):
    """c' = c (1-rho) -- the reduced-world reroute rate (DERIVATION_PREREG SS4)."""
    return c * (1.0 - rho_of(b, c, n))


def phi_notR_RED(b, c, n):
    """phi(cyclic | x0 not in R) = phi_U(c(1-rho))   (DERIVATION_PREREG eq. 4.2)."""
    return phi_U(c_eff(b, c, n))


def eps_RED(b, c, n):
    """The referee's two eps channels, re-expressed through the reduction:
    phi_runstart -> T_U(c'), E[#f-draws] -> (1 + c' T_U(c'))/(1-rho)."""
    r = rho_of(b, c, n)
    rs = rho_start_of(b, c, n)
    cp = c_eff(b, c, n)
    T = T_U(cp)
    return (rs / r) * T + (1.0 + cp * T) / ((1.0 - r) * n)


def phi_RED(b, c, n):
    """DERIVATION_PREREG eq. (5.1).  No free parameter."""
    r = rho_of(b, c, n)
    return (1.0 - r) * phi_notR_RED(b, c, n) + r * eps_RED(b, c, n)


def lam_pred(t, b, c, n, t_c=None):
    """Per-target closure elevation at traversed mass t, relative to the master
    formula's 1/((1-t)n).   DERIVATION_PREREG eq. (3.1).

    t_c = visited mass restricted to R^c (defaults to t)."""
    r = rho_of(b, c, n)
    if t_c is None:
        t_c = t
    return (1.0 - t) / ((1.0 - r) / (1.0 - c / n) - t_c)


# ----------------------------------------------------------------------------
# self-tests
# ----------------------------------------------------------------------------


def _selftest():
    ok = True

    def chk(name, got, want, tol):
        nonlocal ok
        d = abs(got - want)
        good = d <= tol
        ok = ok and good
        print(f"  [{'ok ' if good else 'FAIL'}] {name}: got={got:.12g} want={want:.12g} diff={d:.3g} tol={tol:.3g}")

    print("== H(t) closed form vs direct numeric inner quadrature ==")
    for P in (1.0, 1.35, 1.9886, 2.0, 2.0000001, 2.5086, 3.7):
        for t in (0.03, 0.2, 0.5, 0.8, 0.97):
            inner, _ = integrate.quad(lambda s: (1 - P * s) * (1 - s) ** (-P), 0, t,
                                      epsabs=1e-14, epsrel=1e-14, limit=400)
            want = t - (1 - t) ** P * inner
            chk(f"H(P={P},t={t})", float(H_const_P(t, P)), want, 5e-10)

    print("== H boundary and P=1 (M-U) ==")
    chk("H(0)", float(H_const_P(0.0, 2.3)), 0.0, 1e-14)
    chk("H(1-)", float(H_const_P(1.0 - 1e-12, 2.3)), 1.0, 1e-9)
    for t in (0.1, 0.5, 0.9):
        chk(f"P=1 => H=t^2 (t={t})", float(H_const_P(t, 1.0)), t * t, 1e-12)

    print("== phi_U / T_U closed forms vs quadrature ==")
    for c in (0.5, 5.0, 75.4, 300.0):
        chk(f"phi_U({c})", phi_U(c), _quad(lambda u: math.exp(-c * u * u)), 1e-12)
        chk(f"T_U({c})", T_U(c), _quad(lambda u: (1 - u) * math.exp(-c * u * u)), 1e-12)

    print("== rho -> 0 limits (b=1 and n huge) ==")
    for c in (10.0, 150.0):
        chk(f"phi_V4(b=1,c={c},n=1e10) -> phi_U", phi_V4(1, c, 1e10), phi_U(c), 1e-7)
        chk(f"phi_RED(b=1,c={c},n=1e10) -> phi_U", phi_RED(1, c, 1e10), phi_U(c), 1e-7)
        chk(f"phi_EPSR(b=1,c={c},n=1e10) -> phi_U", phi_EPSR(1, c, 1e10), phi_U(c), 1e-7)

    print("== phi_RED -> (1-rho) phi_U(c(1-rho)) as c/n -> 0 at fixed rho ==")
    # fixed rho ~ 0.4579: hold b*c/n fixed (scale b and n together, c fixed)
    for scale in (1, 10, 100, 1000):
        n = 65536 * scale
        b = 100 * scale
        c = 400.0
        r = rho_of(b, c, n)
        lead = (1 - r) * phi_U(c_eff(b, c, n))
        got = phi_RED(b, c, n)
        print(f"  n={n:>9d} b={b:>5d} c={c:>7.0f} rho={r:.6f}  "
              f"phi_RED={got:.10f} lead={lead:.10f} rel_gap={(got-lead)/lead:.3e} "
              f"(c/n={c/n:.3e})")

    print("== elevation at t=0 equals the wave-8 lemma value P_exact ==")
    for (b, c, n) in ((100, 400.0, 65536), (300, 150.0, 65536), (400, 100.0, 65536)):
        chk(f"lam_pred(0;b={b},c={c})", float(lam_pred(0.0, b, c, n)), P_exact(b, c, n), 1e-12)

    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _selftest() else 1)
