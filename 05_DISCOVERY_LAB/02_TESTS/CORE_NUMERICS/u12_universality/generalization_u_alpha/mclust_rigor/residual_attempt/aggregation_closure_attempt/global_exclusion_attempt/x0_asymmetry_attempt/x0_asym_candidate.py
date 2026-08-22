"""x0_asymmetry_attempt -- the ONE candidate formula this front puts forward.

Wave 9, DISC-DEC-041 front (a).

IMPORTANT SCOPE NOTE.  This is NOT the mandated hypothesis.  The mandated
hypothesis (x0's per-target closure elevation differs from that of the
reroute-created arc starts) was measured directly and came out NEGATIVE --
see ATTEMPT.md sec 4.  What is implemented here is a SIDE finding of the
same measurement campaign: the OTHER place where the inherited formalism
treats x0 asymmetrically, namely the dilution factor

    phi_true = (1-rho) * phi(cyclic | x0 not in R) + rho * eps,
    eps := P(cyclic | x0 in R),

where `residual_attempt/ATTEMPT.md` sec 6, and every formula since
(phi_CAND, phi_CAND5, phi_GLOBAL), set eps = 0 exactly, on the argument
that a shadowed x0 "nunca pode ser alcancado por um passo-pi normal".
Stage B of `x0_asymmetry_walk_measure.py` measures eps directly and finds
it is NOT zero: rho*eps is 0.4%-2.2% of phi in the six stress cells, at
10-20 sigma.

------------------------------------------------------------------------
DERIVATION of eps (leading order; same mean-field rigor as the rest of
this line, NOT a proof)
------------------------------------------------------------------------
Given x0 in R, the f-orbit of x0 can return to x0 in exactly two ways:

 (a) RUN-START CHANNEL.  A normal pi-step lands on x0.  The walk only ever
     takes normal pi-steps from points outside R, so this requires
     pi^-1(x0) not in R -- i.e. x0 must be a *run start* in the sense of
     wave 4.  Given x0 in R,
         P(run start | x0 in R) = rho_start/rho,  rho_start = (c/n)(1-rho)
     (rho_start = (c/n)(1-c/n)^b is wave 4's exact run-start density;
     labelled reuse).  Conditionally on that, x0 is a closure target alive
     from t=0 with exactly the same per-target hazard the formalism gives
     any live arc start -- indeed the sliding-window computation for a
     run-start target gives elevation (1-c/n)^-b = 1/(1-rho) = P, the same
     P that phi_CAND already uses -- so the return probability is, to
     leading order, the SAME phi_cond = phi_V4 that the x0-not-in-R case
     has.  [Heuristic step, labelled: the walk from an x0 in R begins with
     an f-jump rather than a pi-step, so its exploration is not literally
     identical; only its role as a TARGET is.]

 (b) F-DRAW CHANNEL.  Some later f-draw lands exactly on x0.  Every f-draw
     is uniform on [n] and independent of everything, so this contributes
     E[#f-draws]/n.  The number of f-draws is (reroute events) x (draws per
     event); reroute events occur at rate c per unit traversed mass (wave 4
     sec 2, exact) and each event's chain makes 1/(1-rho) draws in
     expectation (geometric, continuation probability rho -- wave 4 sec 3,
     labelled reuse), so
         E[#f-draws] = (c/(1-rho)) * T,   T := E[traversed mass at
                                               termination] = int_0^1 S(t) dt
     with S(t) = (1-t)^P exp(-c H(t)) the model's own survival function.

Together:

    eps = (rho_start/rho) * phi_cond + (c/((1-rho) n)) * T
    phi_EPS := (1-rho) * phi_cond + rho * eps
             = (1-rho) * phi_cond * (1 + c/n) + rho*c*T/((1-rho)*n)

Both pieces were checked against the direct stage-B measurement before
being written down as a formula (ATTEMPT.md sec 5.2): channel (a) is
reproduced to 0.75-1.17x and channel (b) to 0.99-1.53x of measurement
across the six cells.  Neither check is exact -- this is a leading-order
account of a small term, not a closed derivation, and it is labelled as
such everywhere.

phi_EPS changes NOTHING else: same P = 1/(1-rho), same q_CLUST(s) =
s/(1-rho), same H(t).  With c/n -> 0 it reduces to phi_CAND identically.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from x0_asym_formula import rho_of, P_lead, H_asym, phi_U, _TRAPZ


def _model(c, n, b, n_outer=400, n_inner=250):
    rho = rho_of(c, n, b)
    P = P_lead(rho)
    t = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H = np.array([H_asym(x, rho, P, n_inner) for x in t])
    omt = np.clip(1.0 - t, 1e-15, None)
    S = np.power(omt, P) * np.exp(-c * H)          # survival past mass t
    phi_cond = _TRAPZ(P * np.power(omt, P - 1.0) * np.exp(-c * H), t)
    T = _TRAPZ(S, t)                               # E[mass at termination]
    return rho, P, phi_cond, T


def phi_CAND(c, n, b):
    """residual_attempt's phi_CAND, rebuilt through this file's machinery
    (eps = 0)."""
    if rho_of(c, n, b) < 1e-12:
        return phi_U(c)
    rho, P, phi_cond, T = _model(c, n, b)
    return (1.0 - rho) * phi_cond


def eps_of(c, n, b):
    rho, P, phi_cond, T = _model(c, n, b)
    rho_start = (c / n) * (1.0 - rho)
    return (rho_start / rho) * phi_cond + (c / ((1.0 - rho) * n)) * T


def phi_EPS(c, n, b):
    """This front's candidate: phi_CAND plus the measured-and-then-derived
    rho*eps term that the (1-rho) dilution factor drops."""
    if rho_of(c, n, b) < 1e-12:
        return phi_U(c)
    rho, P, phi_cond, T = _model(c, n, b)
    rho_start = (c / n) * (1.0 - rho)
    eps = (rho_start / rho) * phi_cond + (c / ((1.0 - rho) * n)) * T
    return (1.0 - rho) * phi_cond + rho * eps


CANDIDATES = {"CAND": phi_CAND, "EPS": phi_EPS}


if __name__ == "__main__":
    import json
    print("sanity: c/n -> 0 must give phi_EPS == phi_CAND")
    for (n, b, c) in [(10 ** 9, 100, 400.0), (10 ** 8, 50, 50.0)]:
        a, e = phi_CAND(c, n, b), phi_EPS(c, n, b)
        print(f"   n={n:.0e} b={b} c={c}: CAND={a:.8f} EPS={e:.8f} rel={100*(e-a)/a:+.2e}%")
    print()
    print("cheap triage against ALREADY RECORDED phi_mc (labelled reuse, no new"
          " simulation): ../mclust_global_validate_results.json, seeds 20260822911")
    with open(os.path.join(HERE, "..", "mclust_global_validate_results.json")) as fh:
        cells = json.load(fh)["cells"]
    print(f"{'n':>6} {'b':>4} {'c':>7} {'rho':>7} | {'phi_mc':>9} | "
          f"{'CAND dev%':>10} {'z':>6} | {'EPS dev%':>9} {'z':>6} | {'eps':>9} {'rho*eps/phi':>11}")
    x2c = x2e = 0.0
    for r in cells:
        n, b, c = r["n"], r["b"], r["c"]
        m, sem = r["phi_mc"], r["sem"]
        a, e = phi_CAND(c, n, b), phi_EPS(c, n, b)
        zc, ze = (m - a) / sem, (m - e) / sem
        x2c += zc * zc
        x2e += ze * ze
        ep = eps_of(c, n, b)
        rho = rho_of(c, n, b)
        print(f"{n:6d} {b:4d} {c:7.1f} {rho:7.4f} | {m:9.6f} | {100*(m-a)/a:+9.2f}% {zc:+6.2f} | "
              f"{100*(m-e)/e:+8.2f}% {ze:+6.2f} | {ep:9.6f} {100*rho*ep/m:10.2f}%")
    print(f"\nchi2 over {len(cells)} recorded cells: CAND={x2c:.2f}  EPS={x2e:.2f}")
    print("(TRIAGE ONLY -- predecessor seeds; the decision run is x0_asym_validate.py)")
