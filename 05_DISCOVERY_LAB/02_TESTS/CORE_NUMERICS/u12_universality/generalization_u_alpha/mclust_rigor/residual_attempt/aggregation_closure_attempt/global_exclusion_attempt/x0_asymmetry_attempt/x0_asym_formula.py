"""x0_asymmetry_attempt -- the ASYMMETRIC-ELEVATION master formula.

Wave 9, DISC-DEC-041 front (a), `MCLUST-X0-ASYMMETRY-ATTEMPT`.

WRITTEN BEFORE ANY NEW MEASUREMENT (pre-registration of the model that the
measurement in x0_asymmetry_walk_measure.py is designed to feed).  Own
implementation; imports nothing from residual_attempt/,
aggregation_closure_attempt/ or global_exclusion_attempt/.

------------------------------------------------------------------------
WHAT THIS ENCODES
------------------------------------------------------------------------
The M-CLUST(b) master formula, as it stands after `residual_attempt/`
(phi_CAND) and `aggregation_closure_attempt/` (phi_CAND5), applies ONE
elevation factor P to the per-arc-start closure hazard, uniformly over
every live arc start:

    hazard of closure into ONE given live arc start, per unit mass
        = P / (1 - t)

with P = 1/(1-rho)  [phi_CAND, residual_attempt sec 6]
  or P = (1-c/n)^-(b-1)  [phi_CAND5, aggregation_closure sec 3].

`global_exclusion_attempt/ATTEMPT.md` sec 6 item (b) names, as an
UNTESTED suspicion, that x0 -- fixed since the start of the walk, never
created by a reroute draw -- may not obey the same elevation as the other
members of Y_live, which are all created dynamically by reroute survival.

This module implements the two-parameter generalisation in which those two
populations are allowed DIFFERENT constant elevations:

    P0 := elevation of the closure hazard into x0 itself
    P1 := elevation of the closure hazard into each reroute-created arc start

Re-deriving the master formula (DERIVATIONS.md sec 1, Poisson PGFL,
conditioning on reroute times -- redone here from scratch with the two
elevations kept distinct):

    base (x0's own closure clock):
        exp(-int_0^t P0 dr/(1-r)) = (1-t)^P0
    per reroute event at mass s (kills w.p. q(s); otherwise creates ONE new
    arc start that then carries hazard P1/(1-r) for r in [s,t]):
        F(s) = (1-q(s)) * ((1-t)/(1-s))^P1
    E[S(t)] = (1-t)^P0 * exp(-c * H(t)),
        H(t) = t - (1-t)^P1 * int_0^t (1-q(s)) (1-s)^-P1 ds        (A)
    phi = int_0^1 [P0/(1-t)] * E[S(t)] dt
        = int_0^1 P0 (1-t)^(P0-1) exp(-c H(t)) dt                  (B)

Checks built in below:
  * P0 = P1 = 1/(1-rho)  reproduces phi_V4 of residual_attempt EXACTLY
    (its integrand is ES/((1-rho)(1-t)) = p (1-t)^(p-1) exp(-cH), p=1/(1-rho)).
  * P0 = P1 = 1 and q(s)=s gives H = t^2 and phi = int_0^1 exp(-c t^2) dt
    = phi_U (M-U, wave 2).
  * rho -> 0 gives P0 = P1 -> 1 and recovers phi_U.

The x0-in-R dilution factor of residual_attempt sec 6 is kept, but in the
slightly more general form that this front measures directly (sec 4 of
ATTEMPT.md):

    phi_true = (1-rho) * phi(x0 not in R) + rho * eps,
    eps := P(cyclic | x0 in R)

phi_CAND/phi_CAND5/phi_GLOBAL all set eps = 0.  `eps` is a free input here
so that a MEASURED value can be substituted; eps=0.0 reproduces the
predecessors exactly.

------------------------------------------------------------------------
LABELLED REUSE OF PREDECESSOR CONVENTIONS (explicit, per the convention
these documents already use for shared building blocks)
------------------------------------------------------------------------
 * rho = 1 - (1-c/n)^b                       [wave 4, exact]
 * q_CLUST(s) = s/(1-rho), NOT clipped at 1  [wave 4; the un-clipped
   convention is what mclust_residual_v4.py uses, and is kept here so that
   P0=P1 reproduces phi_CAND to machine precision rather than approximately]
Everything else (the integration machinery, the two-elevation derivation
above, the eps term) is written from scratch in this file.
"""
import math

import numpy as np
from scipy import integrate

_TRAPZ = getattr(np, "trapezoid", None) or np.trapz


def rho_of(c, n, b):
    """rho = 1 - (1-c/n)^b -- exact density of R (wave 4, labelled reuse)."""
    return 1.0 - (1.0 - c / n) ** b


def P_lead(rho):
    """phi_CAND's elevation, 1/(1-rho) (residual_attempt sec 6)."""
    return 1.0 / (1.0 - rho)


def P_exact(c, n, b):
    """phi_CAND5's elevation, (1-c/n)^-(b-1) (aggregation_closure sec 3)."""
    return (1.0 - c / n) ** (-(b - 1))


def phi_U(c):
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0.0, 1.0, limit=200)
    return v


def q_clust(s, rho):
    """s/(1-rho), un-clipped (labelled reuse of wave 4's convention)."""
    if rho <= 1e-12:
        return s
    return s / (1.0 - rho)


def H_asym(t, rho, P1, n_inner=400):
    """Equation (A): H(t) = t - (1-t)^P1 * int_0^t (1-q(s))(1-s)^-P1 ds."""
    if t < 1e-13:
        return 0.0
    s_grid = np.linspace(0.0, t, n_inner + 1)
    one_minus_s = np.clip(1.0 - s_grid, 1e-15, None)
    integrand = (1.0 - q_clust(s_grid, rho)) * np.power(one_minus_s, -P1)
    inner = _TRAPZ(integrand, s_grid)
    return t - (max(1.0 - t, 0.0) ** P1) * inner


def phi_asym(c, n, b, P0, P1, eps=0.0, n_outer=400, n_inner=250,
             dilute=True, return_diag=False):
    """Equation (B) plus the x0-in-R decomposition.

    phi = (1-rho) * int_0^1 P0 (1-t)^(P0-1) exp(-c H(t)) dt + rho * eps
    (the (1-rho) prefactor and the rho*eps term are dropped if dilute=False,
    in which case the bare conditional P(cyclic | x0 not in R) is returned).
    """
    rho = rho_of(c, n, b)
    if rho < 1e-12:
        v = phi_U(c)
        return (v, dict(H_end=1.0)) if return_diag else v
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_asym(t, rho, P1, n_inner) for t in t_grid])
    one_minus_t = np.clip(1.0 - t_grid, 1e-15, None)
    integrand = P0 * np.power(one_minus_t, P0 - 1.0) * np.exp(-c * H_vals)
    cond = _TRAPZ(integrand, t_grid)
    v = (1.0 - rho) * cond + rho * eps if dilute else cond
    if return_diag:
        return v, dict(H_end=H_vals[-1], cond=cond, rho=rho)
    return v


def phi_CAND_own(c, n, b):
    """Own re-implementation of residual_attempt's phi_CAND = (1-rho) phi_V4,
    as the P0=P1=1/(1-rho), eps=0 special case of phi_asym."""
    rho = rho_of(c, n, b)
    if rho < 1e-12:
        return phi_U(c)
    p = P_lead(rho)
    return phi_asym(c, n, b, p, p, eps=0.0)


def phi_CAND5_own(c, n, b):
    """Own re-implementation of aggregation_closure's phi_CAND5, as the
    P0=P1=(1-c/n)^-(b-1), eps=0 special case."""
    rho = rho_of(c, n, b)
    if rho < 1e-12:
        return phi_U(c)
    p = P_exact(c, n, b)
    return phi_asym(c, n, b, p, p, eps=0.0)


def solve_P0_needed(c, n, b, P1, phi_target, eps=0.0,
                    lo=0.2, hi=20.0, tol=1e-10):
    """Given P1 (and eps), find the constant P0 that makes phi match a target.

    Diagnostic used in ATTEMPT.md sec 5: how large would x0's OWN elevation
    have to be, holding the other arc starts at P1, to reproduce the measured
    phi_mc?  Bisection; phi is monotone increasing in P0 over the range used
    (checked numerically at call sites)."""
    f = lambda P0: phi_asym(c, n, b, P0, P1, eps=eps) - phi_target
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


if __name__ == "__main__":
    print("=== sanity checks for x0_asym_formula.py ===")
    # 1. rho -> 0 recovers phi_U
    for c in (10.0, 50.0, 200.0):
        v = phi_asym(c, 10 ** 9, 1, 1.0, 1.0, 0.0)
        print(f"  rho->0 (n=1e9,b=1) c={c:6.1f}: phi_asym={v:.8f}  phi_U={phi_U(c):.8f}"
              f"  diff={v - phi_U(c):+.2e}")
    # 2. P0=P1=1, q(s)=s (rho->0) -> H=t^2 exactly
    rho_tiny = 1e-15
    for t in (0.1, 0.5, 0.9):
        print(f"  H_asym(t={t}, rho~0, P1=1) = {H_asym(t, rho_tiny, 1.0):.8f}"
              f"   t^2 = {t * t:.8f}")
    # 3. symmetric case reproduces the predecessors' published numbers
    print("\n  symmetric special cases vs published predecessor values")
    print(f"  {'n':>7} {'b':>4} {'c':>7} {'rho':>7} | {'phi_CAND_own':>13} {'phi_CAND5_own':>14}")
    for (n, b, c) in [(65536, 100, 400.0), (65536, 300, 150.0),
                      (65536, 100, 600.0), (65536, 400, 100.0)]:
        print(f"  {n:7d} {b:4d} {c:7.1f} {rho_of(c, n, b):7.4f} | "
              f"{phi_CAND_own(c, n, b):13.6f} {phi_CAND5_own(c, n, b):14.6f}")
    # 4. monotonicity of phi in P0 (needed by solve_P0_needed)
    print("\n  monotonicity of phi in P0 (n=65536,b=100,c=400, P1=P_lead):")
    rho = rho_of(400.0, 65536, 100)
    p1 = P_lead(rho)
    for P0 in (1.0, 1.5, p1, 2.0, 2.5, 3.0):
        print(f"    P0={P0:6.3f} -> phi={phi_asym(400.0, 65536, 100, P0, p1):.6f}")
