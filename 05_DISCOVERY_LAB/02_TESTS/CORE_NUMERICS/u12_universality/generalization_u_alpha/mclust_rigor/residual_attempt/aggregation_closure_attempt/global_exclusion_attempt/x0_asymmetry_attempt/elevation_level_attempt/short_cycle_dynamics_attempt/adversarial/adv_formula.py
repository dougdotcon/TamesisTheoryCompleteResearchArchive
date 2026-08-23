"""
adv_formula.py -- independent, from-scratch re-implementation of the closed
forms needed to check ATTEMPT.md / DERIVATION_PREREG.md, built ONLY from the
formulas as printed in prose in:
  - generalization_u_alpha/DERIVATIONS.md line 170:
        phi_U(c) = integral_0^1 e^{-c t^2} dt          (independent of b)
  - elevation_level_attempt/adversarial/REFEREE_REPORT.md sec 11:
        c'' = c(1-c/n)^(b-1) = c(1-rho)/(1-c/n)
        T_U(c') = phi_U(c') - (1-e^{-c'})/(2c')
        phi_REDB = (1-rho)*[phi_U(c'') + (c/n)*T_U(c'')]
                   + rho*(1 + c''*T_U(c'')) / ((1-rho)*n)
  - short_cycle_dynamics_attempt/DERIVATION_PREREG.md sec 2.1/2.2 (the
    front's own candidate, quoted in the mandate and re-derivable from its
    prose): the exact short-cycle combinatorics and phi_REDC.

No .py file of the target front, elevation_level_attempt/, or its
adversarial/ subfolder was read or imported.
"""
import numpy as np
from scipy.special import erf
from scipy import integrate


# ---------------------------------------------------------------------
# phi_U, T_U
# ---------------------------------------------------------------------

def phi_U(c):
    """integral_0^1 e^{-c t^2} dt, closed form via erf; c may be a scalar
    or array. phi_U(0) = 1."""
    c = np.asarray(c, dtype=np.float64)
    out = np.empty_like(c)
    zero = c <= 0
    nz = ~zero
    out[zero] = 1.0
    sc = np.sqrt(c[nz])
    out[nz] = (np.sqrt(np.pi) / (2.0 * sc)) * erf(sc)
    return out if out.shape else float(out)


def phi_U_scalar(c):
    return float(phi_U(np.array([c]))[0])


def T_U(c):
    """T_U(c) = phi_U(c) - (1-e^{-c})/(2c), per referee sec 11."""
    c = np.asarray(c, dtype=np.float64)
    pu = phi_U(c)
    out = np.empty_like(c)
    zero = c <= 0
    nz = ~zero
    # limit as c->0 of (1-e^{-c})/(2c) is 1/2
    out[zero] = pu[zero] - 0.5
    out[nz] = pu[nz] - (1.0 - np.exp(-c[nz])) / (2.0 * c[nz])
    return out if out.shape else float(out)


def T_U_scalar(c):
    return float(T_U(np.array([c]))[0])


# ---------------------------------------------------------------------
# rho, c''
# ---------------------------------------------------------------------

def rho_of(b, c, n):
    return 1.0 - (1.0 - c / n) ** b


def c_pp(b, c, n):
    """c'' = c(1-c/n)^(b-1) = c(1-rho)/(1-c/n)"""
    return c * (1.0 - c / n) ** (b - 1)


# ---------------------------------------------------------------------
# phi_REDB (formula of record, elevation_level_attempt/adversarial sec 11)
# ---------------------------------------------------------------------

def phi_REDB_cond(b, c, n):
    """phi_U(c'') + (c/n)*T_U(c''): candidate for phi(cyclic | x0 not in R)."""
    cpp = c_pp(b, c, n)
    return phi_U_scalar(cpp) + (c / n) * T_U_scalar(cpp)


def eps_REDB(b, c, n):
    """(1 + c''*T_U(c'')) / ((1-rho)*n)"""
    cpp = c_pp(b, c, n)
    rho = rho_of(b, c, n)
    return (1.0 + cpp * T_U_scalar(cpp)) / ((1.0 - rho) * n)


def phi_REDB_full(b, c, n):
    rho = rho_of(b, c, n)
    return (1.0 - rho) * phi_REDB_cond(b, c, n) + rho * eps_REDB(b, c, n)


# ---------------------------------------------------------------------
# Exact short-cycle combinatorics (DERIVATION_PREREG.md sec 2.1),
# re-derived from the classical fact P(cycle length = L) = 1/n for a
# uniform permutation (independently re-derived in adv_mechanism-adjacent
# reasoning; this file only encodes the resulting closed forms).
# ---------------------------------------------------------------------

def S_untouched(b, c, n):
    """(1/n) * sum_{L=1}^{b} (1-c/n)^L -- probability mass that x0 sits on
    an untouched cycle of length <= b."""
    p = c / n
    L = np.arange(1, b + 1)
    return float(np.sum((1 - p) ** L)) / n


def P_Rc_exact(b, c, n):
    """(1/n) * [ sum_{L=1}^{b}(1-c/n)^L + (n-b)(1-c/n)^b ] -- exact P(x0 in R^c)."""
    p = c / n
    L = np.arange(1, b + 1)
    s = float(np.sum((1 - p) ** L))
    return (s + (n - b) * (1 - p) ** b) / n


def w_short(b, c, n):
    return S_untouched(b, c, n) / P_Rc_exact(b, c, n)


def phi_cond_C_v2(b, c, n):
    """w_short*1 + (1-w_short)*phi_U(c'')"""
    w = w_short(b, c, n)
    return w * 1.0 + (1 - w) * phi_U_scalar(c_pp(b, c, n))


def phi_REDC_full(b, c, n):
    """phi_REDC = P(R^c)*phi_cond_C + P(R)*eps_REDB(c'')  -- ATTEMPT.md sec 2:
       (a) exact P(x0 in R^c) replaces the mean-field (1-rho) prefactor,
       (b) phi_cond_C mixture replaces the flat phi_U(c'') conditional.
       eps channel is left AS phi_REDB's (unmodified), per sec 2.2."""
    PRc = P_Rc_exact(b, c, n)
    PR = 1.0 - PRc
    return PRc * phi_cond_C_v2(b, c, n) + PR * eps_REDB(b, c, n)


if __name__ == "__main__":
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        log.append(s)

    P("=== adv_formula.py selfcheck ===")

    # (1) phi_U closed form vs independent numerical quadrature
    P("(1) phi_U closed form vs scipy.integrate.quad, several c:")
    max_rel = 0.0
    for cval in [0.0, 0.001, 0.5, 1.0, 5.0, 20.0, 100.0, 1000.0]:
        q, _ = integrate.quad(lambda t: np.exp(-cval * t * t), 0, 1)
        cf = phi_U_scalar(cval)
        rel = abs(cf - q) / max(abs(q), 1e-300)
        max_rel = max(max_rel, rel)
        P(f"  c={cval:<8g} quad={q:.12f} closed={cf:.12f} rel_err={rel:.3e}")
    P(f"  max relative error: {max_rel:.3e}", "OK" if max_rel < 1e-9 else "FAIL")

    # (2) rho / c'' sanity at target cell
    b, c, n = 100, 1000, 65536
    rho = rho_of(b, c, n)
    cpp = c_pp(b, c, n)
    P(f"(2) target cell b={b},c={c},n={n}: rho={rho:.6f}, c''={cpp:.6f}")

    # (3) phi_REDB at the six grid cells
    cells6 = [(50, 400, 65536), (100, 400, 65536), (100, 600, 65536),
              (200, 150, 65536), (400, 100, 65536), (100, 1000, 65536)]
    P("(3) phi_REDB (full) at the 6-cell grid:")
    for (bb, cc, nn) in cells6:
        P(f"  b={bb},c={cc},n={nn}: rho={rho_of(bb,cc,nn):.4f} "
          f"phi_REDB_full={phi_REDB_full(bb,cc,nn):.6f} "
          f"phi_REDB_cond={phi_REDB_cond(bb,cc,nn):.6f}")

    # (4) w_short, S_untouched, P(Rc) at target cell, sized as ATTEMPT.md
    #     sec 2 states ("w_short ~ 0.359%")
    Su = S_untouched(b, c, n)
    PRc = P_Rc_exact(b, c, n)
    w = w_short(b, c, n)
    P(f"(4) target cell: S_untouched={Su:.8f}, P(Rc)_exact={PRc:.6f}, "
      f"w_short={100*w:.4f}% (ATTEMPT.md claims ~0.359%)")
    P("   ", "OK, matches claimed order of magnitude"
      if abs(100 * w - 0.359) < 0.05 else "MISMATCH vs claimed 0.359%")

    # (5) phi_REDC vs phi_REDB direction at target cell (ATTEMPT.md claims
    #     phi_REDC sits ~+5.6% ABOVE phi_U(c'') at the conditional level,
    #     and phi_REDC is uniformly ABOVE phi_REDB by +1.6%..+6.4% on all 6
    #     grid cells)
    P("(5) phi_REDC vs phi_REDB, 6-cell grid (ATTEMPT.md claims +1.6%..+6.4% "
      "above, uniformly):")
    devs = []
    for (bb, cc, nn) in cells6:
        redb = phi_REDB_full(bb, cc, nn)
        redc = phi_REDC_full(bb, cc, nn)
        dev = 100 * (redc / redb - 1)
        devs.append(dev)
        P(f"  b={bb},c={cc},n={nn}: phi_REDB={redb:.6f} phi_REDC={redc:.6f} "
          f"dev={dev:+.2f}%")
    all_pos = all(d > 0 for d in devs)
    P(f"   all 6 cells phi_REDC > phi_REDB: {all_pos}  "
      f"(range {min(devs):+.2f}% .. {max(devs):+.2f}%)")

    # (6) conditional-level check at target: phi_cond_C vs phi_U(c'')
    pcc = phi_cond_C_v2(b, c, n)
    puc = phi_U_scalar(cpp)
    dev_cond = 100 * (pcc / puc - 1)
    P(f"(6) target cell conditional: phi_cond_C={pcc:.6f} phi_U(c'')={puc:.6f} "
      f"dev={dev_cond:+.2f}% (ATTEMPT.md claims +5.6%)")

    # (7) n->infinity behaviour, fixed (b,c): phi_REDB and phi_REDC -> phi_U(c)
    P("(7) n->infinity check, fixed b=100,c=400: phi_REDB, phi_REDC -> phi_U(c)")
    target_phiU = phi_U_scalar(400)
    for nn in [2**16, 2**18, 2**20, 2**22, 2**24]:
        db = abs(phi_REDB_full(100, 400, nn) - target_phiU)
        dc = abs(phi_REDC_full(100, 400, nn) - target_phiU)
        P(f"  n=2^{int(np.log2(nn))}: |phi_REDB-phi_U(c)|={db:.3e} "
          f"|phi_REDC-phi_U(c)|={dc:.3e}")

    with open("adv_formula_selfcheck.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
