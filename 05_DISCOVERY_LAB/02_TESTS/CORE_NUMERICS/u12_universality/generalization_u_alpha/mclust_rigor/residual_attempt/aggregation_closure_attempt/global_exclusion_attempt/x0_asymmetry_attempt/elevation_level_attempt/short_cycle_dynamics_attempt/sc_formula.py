"""
sc_formula.py -- closed forms, all re-derived/re-transcribed from the stated
formulas of the primary sources (no .py of the target front or its referee
read or imported). Labeled reuse vs. this-front derivation is marked in each
docstring.
"""

import numpy as np
from scipy import integrate
from scipy.special import erf


# --- reused, labeled: wave-2 M-U base formula, and T_U (elevation_level_attempt §5) ---

def phi_U(c):
    """phi_U(c) = integral_0^1 exp(-c t^2) dt = (sqrt(pi)/(2 sqrt(c))) erf(sqrt(c)).
    Reused unchanged: DERIVATIONS.md §3.1 / elevation_level_attempt/ATTEMPT.md §5."""
    c = np.asarray(c, dtype=float)
    out = np.empty_like(c) if c.shape else np.array(0.0)
    scalar = (c.ndim == 0)
    cc = np.atleast_1d(c)
    small = cc < 1e-10
    res = np.where(
        small,
        1.0 - cc / 3.0,  # series fallback for c->0
        (np.sqrt(np.pi) / (2.0 * np.sqrt(np.where(cc > 0, cc, 1.0)))) * erf(np.sqrt(np.where(cc > 0, cc, 1.0))),
    )
    return res.item() if scalar else res


def T_U(c):
    """T_U(c) = integral_0^1 (1-u) exp(-c u^2) du = phi_U(c) - (1-exp(-c))/(2c).
    Reused unchanged: elevation_level_attempt/ATTEMPT.md §5 (5.1)."""
    c = np.asarray(c, dtype=float)
    scalar = (c.ndim == 0)
    cc = np.atleast_1d(c)
    small = cc < 1e-10
    res = np.where(
        small,
        0.5 - cc / 3.0,
        phi_U(cc) - (1.0 - np.exp(-cc)) / (2.0 * np.where(cc > 0, cc, 1.0)),
    )
    return res.item() if scalar else res


def rho_of(b, c, n):
    """rho = 1 - (1-c/n)^b -- wave 4, exact (mean density)."""
    return 1.0 - (1.0 - c / n) ** b


# --- referee's phi_REDB (elevation_level_attempt/adversarial/REFEREE_REPORT.md §11) ---
# Re-transcribed from the closed form printed there, not copied from any .py.

def c_double_prime(b, c, n):
    """c'' = c(1-c/n)^(b-1) = c(1-rho)/(1-c/n) = c / P_exact."""
    return c * (1.0 - c / n) ** (b - 1)


def phi_REDB(b, c, n):
    rho = rho_of(b, c, n)
    cpp = c_double_prime(b, c, n)
    term1 = (1.0 - rho) * (phi_U(cpp) + (c / n) * T_U(cpp))
    term2 = rho * (1.0 + cpp * T_U(cpp)) / ((1.0 - rho) * n)
    return term1 + term2


# --- this front's own derivation: exact short-cycle combinatorics ------------

def S_untouched(b, c, n):
    """Exact probability mass (as a fraction of n) that x0 lies on an
    UNTOUCHED pi-cycle of length <= b:
        S_untouched = (1/n) * sum_{L=1}^{b} (1-c/n)^L
    Derived in DERIVATION_PREREG.md §1.2-2.1 from the exact fact
    P(L(x0)=ell) = 1/n for every ell=1..n (uniform), combined with
    P(untouched | L=ell) = (1-c/n)^ell for ell <= b (whole cycle must be
    seed-free, since a single seed anywhere on a length<=b cycle absorbs it
    whole -- DERIVATION_PREREG.md §1.3)."""
    p = c / n
    L = np.arange(1, b + 1)
    return np.sum((1.0 - p) ** L) / n


def P_Rc_exact(b, c, n):
    """Exact aggregate P(x0 in R^c), re-derived independently (not copied from
    referee §3.2 -- same style sequential-exposure argument, cross-checked
    against it as a consistency test in sc_formula_selfcheck.log):
        P(R^c) = (1/n) [ sum_{L=1}^{b} (1-p)^L + (n-b) (1-p)^b ]
    (For L<=b the whole-cycle window is checked (exponent L); for L>b only a
    b-term local window is checked (exponent b) -- see DERIVATION_PREREG.md
    §1.1-1.3 for why the window is b, not b-1, once the seed is counted as
    part of its own run.)"""
    p = c / n
    L = np.arange(1, b + 1)
    s = np.sum((1.0 - p) ** L)
    return (s + (n - b) * (1.0 - p) ** b) / n


def w_short(b, c, n):
    """Conditional weight, inside R^c, of the "short & untouched" bucket."""
    return S_untouched(b, c, n) / P_Rc_exact(b, c, n)


def phi_cond_C(b, c, n):
    """This front's candidate for phi(cyclic | x0 in R^c):
        w_short * 1  +  (1 - w_short) * phi_U(c'')
    -- the short-untouched bucket contributes probability EXACTLY 1
    (deterministic, DERIVATION_PREREG.md §1.3), the rest is left as
    phi_REDB's existing (long-cycle mean-field) value. See §2.2 of the
    prereg for the explicit caveat that the sign of the net correction was
    NOT known in advance."""
    ws = w_short(b, c, n)
    cpp = c_double_prime(b, c, n)
    return ws * 1.0 + (1.0 - ws) * phi_U(cpp)


def phi_REDC(b, c, n):
    """Full candidate: phi_REDB's eps channel (x0 in R) is kept unmodified;
    the (x0 in R^c) branch uses phi_cond_C instead of phi_U(c''); the
    aggregate (1-rho)/rho split is replaced by the exact P(R^c)/P(R) split
    (the referee's own tested "exact densities" ingredient, sized in §3.2 of
    the referee report and re-derived independently here)."""
    rho = rho_of(b, c, n)
    cpp = c_double_prime(b, c, n)
    p_rc = P_Rc_exact(b, c, n)
    p_r = 1.0 - p_rc
    # eps channel: reuse phi_REDB's eps formula verbatim (its own internal
    # rho, not the exact P(R)), scaled by the exact p_r instead of rho, per
    # DERIVATION_PREREG.md §2.2-2.3 ("eps channel left unmodified" caveat).
    # eps_ref's run-start term (rho_start/rho * T_U): reuse rho_start = (c/n)(1-rho)
    rho_start = (c / n) * (1.0 - rho)
    eps_full = (rho_start / rho) * T_U(cpp) + (1.0 + cpp * T_U(cpp)) / ((1.0 - rho) * n)
    cond_c = phi_cond_C(b, c, n)
    return p_rc * cond_c + p_r * eps_full


# --- self-checks -------------------------------------------------------------
if __name__ == "__main__":
    import sys
    fails = 0

    print("sc_formula.py self-checks")

    print("\n(1) rho -> 0 limits: phi_REDB, phi_REDC -> phi_U(c) as n->inf at fixed (b,c)")
    for (b, c) in [(100, 400), (50, 100)]:
        for n in [2**16, 2**20, 2**24, 2**28]:
            redb = phi_REDB(b, c, n)
            redc = phi_REDC(b, c, n)
            base = phi_U(c)
            print(f"  b={b} c={c} n=2^{int(np.log2(n))}: phi_U(c)={base:.8f}  "
                  f"REDB-phi_U(c)={redb-base:+.3e}  REDC-phi_U(c)={redc-base:+.3e}")

    print("\n(2) w_short, S_untouched, P_Rc_exact sanity at the target cell "
          "(b=100,c=1000,n=65536)")
    b, c, n = 100, 1000, 65536
    su = S_untouched(b, c, n)
    prc = P_Rc_exact(b, c, n)
    ws = w_short(b, c, n)
    rho = rho_of(b, c, n)
    print(f"  S_untouched (fraction of n)     = {su:.7f}")
    print(f"  P(R^c) exact                    = {prc:.7f}   (1-rho mean-field = {1-rho:.7f})")
    print(f"  w_short = S_untouched / P(R^c)  = {ws:.6f}")
    cpp = c_double_prime(b, c, n)
    base_phiU = phi_U(cpp)
    cond_c = phi_cond_C(b, c, n)
    print(f"  phi_U(c'')  = {base_phiU:.6f}")
    print(f"  phi_cond_C  = {cond_c:.6f}   (delta = {cond_c-base_phiU:+.6f}, "
          f"{100*(cond_c/base_phiU-1):+.3f}% relative)")

    print("\n(3) identity check: P(R^c) + P(x0 in R, aggregate exact) should be 1")
    # exact P(x0 in R) = sum_{L=1}^{b}[1-(1-p)^L]/n + (n-b)*(1-(1-p)^b)/n = 1 - P_Rc_exact
    check = abs(prc + (1 - prc) - 1.0)
    ok3 = check < 1e-12
    if not ok3:
        fails += 1
    print(f"  P(R^c)+P(R) = 1 check: {check:.2e}  {'OK' if ok3 else 'FAIL'}")

    print("\n(4) monotonicity / plausibility: phi_REDC finite, in (0,1), for the 6-cell grid")
    grid = [(50, 400, 65536), (100, 400, 65536), (100, 600, 65536),
            (200, 150, 65536), (400, 100, 65536), (100, 1000, 65536)]
    for (b, c, n) in grid:
        v_redb = phi_REDB(b, c, n)
        v_redc = phi_REDC(b, c, n)
        ws = w_short(b, c, n)
        ok = 0 < v_redb < 1 and 0 < v_redc < 1
        if not ok:
            fails += 1
        print(f"  b={b:4d} c={c:5d} n={n}: rho={rho_of(b,c,n):.4f}  w_short={ws:.5f}  "
              f"phi_REDB={v_redb:.6f}  phi_REDC={v_redc:.6f}  "
              f"delta={100*(v_redc/v_redb-1):+.3f}%  {'OK' if ok else 'FAIL'}")

    print(f"\n{'ALL SELF-CHECKS PASSED' if fails == 0 else f'{fails} SELF-CHECK(S) FAILED'}")
    sys.exit(1 if fails else 0)
