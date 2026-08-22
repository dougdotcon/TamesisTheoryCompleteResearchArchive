"""global_exclusion_attempt -- stage 2: candidate master-formula variants
built from the combined local(order-b)+global(order-tn) exclusion analysis
in ATTEMPT.md sec 2-3.

Own implementation. Does not import any file from residual_attempt/ or
aggregation_closure_attempt/ (re-typed here, matching the SAME structural
pattern -- H_generic/phi_generic -- that both predecessors already used, for
a direct apples-to-apples comparison, but written independently in this
file).

Three formulas compared:

  phi_CAND  (residual_attempt): hazard(s) = P_lead/(1-s), P_lead=1/(1-rho)
  phi_CAND5 (aggregation_closure): hazard(s) = P_exact/(1-s),
            P_exact=(1-c/n)^-(b-1)  [the EXACT sequential-exposure result,
            sec 3.1 of aggregation_closure_attempt/ATTEMPT.md]
  phi_GLOBAL (this front): hazard(s) = P_exact/(1-s-(b-1)/n)
            -- the SAME exact local elevation P_exact, but with the raw
            discrete pool size (1-s)n REDUCED by the (b-1) local-window
            points whenever they have not yet been absorbed into the
            walk's own already-visited history (a small, O(b/n) global-
            local interaction correction; see ATTEMPT.md sec 2.3 for the
            derivation and why it is expected to be small, and sec 4 for
            the direct empirical test of whether a LARGER depth-dependent
            effect exists beyond this term).

All three share q_CLUST(s)=s/(1-rho) [wave 4, reconfirmed by
residual_attempt sec 3.1] and the (1-rho) x0-in-R dilution factor
[residual_attempt sec 6, structurally justified in aggregation_closure
sec 8].
"""
import math

import numpy as np
from scipy import integrate


def phi_U(c):
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


def q_clust(s, rho):
    return s / (1.0 - rho) if rho > 1e-12 else s


def elevation_P_exact(c, n, b):
    return (1.0 - c / n) ** (-(b - 1))


def H_pool(t, rho, elevate_fn, pool_fn, n_steps=400):
    """Generic H(t) for hazard(s) = elevate_fn(s) / pool_fn(s), where
    pool_fn(s) reduces to (1-s) for the standard/CAND/CAND5 forms and to
    (1-s-(b-1)/n) for phi_GLOBAL. elevate_fn(s) reduces to a constant P for
    all three variants tested here (the direct measurement in sec 4 tests
    whether it should instead depend on depth; none of the three closed-
    form candidates below builds in any such dependence, since sec 4's own
    result is what determines whether that is warranted)."""
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    s_grid = np.linspace(0.0, t, n_steps + 1)
    pool_t = max(pool_fn(t), 1e-12)
    pool_s = np.clip(pool_fn(s_grid), 1e-12, None)
    # exp(-int_s^t elevate(r)/pool(r) dr) generalizes (1-t)^P/(1-s)^P only
    # when elevate/pool = P/(1-r) exactly (closed form); for phi_GLOBAL's
    # shifted pool we integrate the exponent directly instead of assuming
    # the closed power-law form.
    integrand_exponent = elevate_fn(s_grid) / pool_s
    trapz = getattr(np, "trapezoid", None) or np.trapz
    # cumulative integral from s to t via reversing: use full grid, then
    # for each s use quad-like cumulative trapezoid from that s to t.
    cum = np.concatenate([[0.0], np.cumsum(
        (integrand_exponent[1:] + integrand_exponent[:-1]) / 2.0 * np.diff(s_grid))])
    exponent_s_to_t = cum[-1] - cum  # int_s^t
    surv_s_from_t = np.exp(-exponent_s_to_t)  # exp(-int_s^t elevate/pool dr)
    integrand = (1.0 - q_clust(s_grid, rho)) * surv_s_from_t
    inner = trapz(integrand, s_grid)
    return t - inner


def phi_pool(c, n, b, elevate_fn, pool_fn, n_outer=350, n_inner=200):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    t_grid = np.linspace(0.0, 1.0 - 1e-7, n_outer + 1)
    H_vals = np.array([H_pool(t, rho, elevate_fn, pool_fn, n_inner) for t in t_grid])
    # base survival (x0's own clock): exp(-int_0^t elevate/pool dr) = same
    # exponent machinery evaluated with s=0 fixed (reuse H_pool's internal
    # cumulative by calling with s_grid from 0 to t; cheaper: recompute
    # directly here since we need it for EVERY t on the outer grid too).
    base = np.array([
        math.exp(-_cum_exponent(0.0, t, rho, elevate_fn, pool_fn, n_inner))
        for t in t_grid])
    density = elevate_fn(t_grid) / np.clip(pool_fn(t_grid), 1e-12, None) * base
    ES = np.exp(-c * H_vals) * base
    trapz = getattr(np, "trapezoid", None) or np.trapz
    integrand_phi = ES * elevate_fn(t_grid) / np.clip(pool_fn(t_grid), 1e-12, None)
    return trapz(integrand_phi, t_grid)


def _cum_exponent(s0, t, rho, elevate_fn, pool_fn, n_steps):
    if t < 1e-13:
        return 0.0
    grid = np.linspace(s0, t, n_steps + 1)
    integrand = elevate_fn(grid) / np.clip(pool_fn(grid), 1e-12, None)
    trapz = getattr(np, "trapezoid", None) or np.trapz
    return trapz(integrand, grid)


def phi_CAND(c, n, b):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    P = 1.0 / (1.0 - rho)
    v = phi_pool(c, n, b, elevate_fn=lambda s: P * np.ones_like(np.atleast_1d(s)) if hasattr(s, "__len__") else P,
                 pool_fn=lambda s: 1.0 - s)
    return (1.0 - rho) * v


def phi_CAND5(c, n, b):
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    P = elevation_P_exact(c, n, b)
    v = phi_pool(c, n, b, elevate_fn=lambda s: P * np.ones_like(np.atleast_1d(s)) if hasattr(s, "__len__") else P,
                 pool_fn=lambda s: 1.0 - s)
    return (1.0 - rho) * v


def phi_GLOBAL(c, n, b):
    """This front's candidate: exact local elevation P_exact, pool size
    reduced by the (b-1) local-window points not yet absorbed into global
    history -- modeled here as a CONSTANT shift (b-1)/n applied uniformly
    (an upper-bound approximation: in reality only the SHALLOW fraction of
    steps needs this shift; sec 4's direct measurement checks whether the
    resulting error from applying it uniformly/always is even detectable,
    given the shift itself is tiny)."""
    rho = rho_of(c, n, b)
    if rho < 1e-9:
        return phi_U(c)
    P = elevation_P_exact(c, n, b)
    shift = (b - 1) / n
    v = phi_pool(c, n, b, elevate_fn=lambda s: P * np.ones_like(np.atleast_1d(s)) if hasattr(s, "__len__") else P,
                 pool_fn=lambda s: np.clip(1.0 - s - shift, 1e-9, None))
    return (1.0 - rho) * v


if __name__ == "__main__":
    print("sanity: rho->0 (b=1,c small) recovers phi_U")
    print("phi_CAND (c=50,n=1e9,b=1):", phi_CAND(50.0, 10 ** 9, 1), " phi_U(50):", phi_U(50.0))
    print("phi_CAND5(c=50,n=1e9,b=1):", phi_CAND5(50.0, 10 ** 9, 1))
    print("phi_GLOBAL(c=50,n=1e9,b=1):", phi_GLOBAL(50.0, 10 ** 9, 1))
    print()
    for (n, b, c) in [(65536, 100, 400.0), (65536, 300, 150.0), (65536, 100, 600.0), (65536, 400, 100.0)]:
        rho = rho_of(c, n, b)
        cand = phi_CAND(c, n, b)
        cand5 = phi_CAND5(c, n, b)
        glob = phi_GLOBAL(c, n, b)
        print(f"n={n} b={b} c={c} rho={rho:.4f} | CAND={cand:.6f} CAND5={cand5:.6f} "
              f"GLOBAL={glob:.6f} | (GLOBAL-CAND5)/CAND5={100*(glob-cand5)/cand5:+.4f}%")
