"""ref2_formula.py -- the referee's own re-implementation of every closed form
in the lineage that this review needs, from the stated formulas only.

  phi_U(c)     = int_0^1 exp(-c u^2) du                       (M-U, wave 2)
  T_U(c)       = int_0^1 (1-u) exp(-c u^2) du
  H(t;P)       = 1 - (2/(2-P))(1-t)^P + (P/(2-P))(1-t)^2      (referee 4.1 / 1(i))
  phi_V4       = int_0^1 P (1-t)^(P-1) exp(-c H) dt           P = P_lead = 1/(1-rho)
  T            = int_0^1 (1-t)^P exp(-c H) dt
  phi_runstart = int_0^1 P (1-t)^(2P-1) exp(-c H) dt
  phi_CAND     = (1-rho) phi_V4
  eps_ref      = (rho_start/rho) phi_runstart + (1 + c T)/((1-rho) n)
  phi_EPSR     = (1-rho) phi_V4 + rho eps_ref                 (formula of record)
  phi_RED      = (1-rho)[phi_U(c') + (c/n) T_U(c')]
                 + rho (1 + c' T_U(c'))/((1-rho) n)           c' = c(1-rho)   (5.1)
  phi_RED2     = phi_RED with H_delta(u) = u^2 + (delta/2) u^2 (1-u),
                 delta = c/((1-rho) n)                        (6.1)
  phi_REDB     = referee's variant: c'' = c(1-c/n)^(b-1)  (pool+world matched)

All quadrature is mpmath at 30 dps; the closed form for H is audited against
direct inner quadrature.
"""
import mpmath as mp

mp.mp.dps = 30


def rho_of(b, c, n):
    return 1 - (1 - mp.mpf(c) / n) ** b


def rho_start_of(b, c, n):
    return (mp.mpf(c) / n) * (1 - mp.mpf(c) / n) ** b


# --------------------------------------------------------------------------
# M-U building blocks
# --------------------------------------------------------------------------
def phi_U(cp):
    cp = mp.mpf(cp)
    if cp == 0:
        return mp.mpf(1)
    return mp.sqrt(mp.pi) / (2 * mp.sqrt(cp)) * mp.erf(mp.sqrt(cp))


def T_U(cp):
    cp = mp.mpf(cp)
    if cp == 0:
        return mp.mpf("0.5")
    return phi_U(cp) - (1 - mp.e ** (-cp)) / (2 * cp)


# --------------------------------------------------------------------------
# the constant-elevation family (phi_CAND / phi_EPSR)
# --------------------------------------------------------------------------
def H_closed(t, P):
    t = mp.mpf(t)
    P = mp.mpf(P)
    om = 1 - t
    if abs(P - 2) < mp.mpf("1e-12"):
        # limit of (P/(2-P))[1-(1-t)^(2-P)] as P->2 is -2 ln(1-t)
        I = (1 - om ** (1 - P)) + (-2 * mp.log(om) if om > 0 else mp.inf)
        return t - om ** P * I
    return 1 - (2 / (2 - P)) * om ** P + (P / (2 - P)) * om ** 2


def H_quad(t, P):
    """H(t) = t - (1-t)^P int_0^t (1-Ps)(1-s)^(-P) ds  -- direct inner quadrature."""
    P = mp.mpf(P)
    I = mp.quad(lambda s: (1 - P * s) * (1 - s) ** (-P), [0, mp.mpf(t)])
    return mp.mpf(t) - (1 - mp.mpf(t)) ** P * I


def _int01(fn):
    return mp.quad(fn, [0, mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"),
                        mp.mpf("0.9"), mp.mpf("0.99"), 1])


def phi_V4(b, c, n):
    rho = rho_of(b, c, n)
    P = 1 / (1 - rho)
    c = mp.mpf(c)
    return _int01(lambda t: P * (1 - t) ** (P - 1) * mp.e ** (-c * H_closed(t, P)))


def T_V4(b, c, n):
    rho = rho_of(b, c, n)
    P = 1 / (1 - rho)
    c = mp.mpf(c)
    return _int01(lambda t: (1 - t) ** P * mp.e ** (-c * H_closed(t, P)))


def phi_runstart(b, c, n):
    rho = rho_of(b, c, n)
    P = 1 / (1 - rho)
    c = mp.mpf(c)
    return _int01(lambda t: P * (1 - t) ** (2 * P - 1)
                  * mp.e ** (-c * H_closed(t, P)))


def phi_CAND(b, c, n):
    return (1 - rho_of(b, c, n)) * phi_V4(b, c, n)


def eps_ref(b, c, n):
    rho = rho_of(b, c, n)
    rs = rho_start_of(b, c, n)
    return (rs / rho) * phi_runstart(b, c, n) + \
           (1 + mp.mpf(c) * T_V4(b, c, n)) / ((1 - rho) * n)


def phi_EPSR(b, c, n):
    rho = rho_of(b, c, n)
    return (1 - rho) * phi_V4(b, c, n) + rho * eps_ref(b, c, n)


# --------------------------------------------------------------------------
# the candidate under review
# --------------------------------------------------------------------------
def phi_RED(b, c, n, cprime=None):
    rho = rho_of(b, c, n)
    cp = mp.mpf(c) * (1 - rho) if cprime is None else mp.mpf(cprime)
    rs = rho_start_of(b, c, n)
    epsR = (rs / rho) * T_U(cp) + (1 + cp * T_U(cp)) / ((1 - rho) * n)
    return (1 - rho) * phi_U(cp) + rho * epsR


def phi_REDB(b, c, n):
    """referee variant: c'' = c(1-c/n)^(b-1), the pool+world-matched reduction."""
    cpp = mp.mpf(c) * (1 - mp.mpf(c) / n) ** (b - 1)
    return phi_RED(b, c, n, cprime=cpp)


def _Hdelta(u, delta):
    return u ** 2 + (delta / 2) * u ** 2 * (1 - u)


def phi_RED2(b, c, n, cprime=None):
    rho = rho_of(b, c, n)
    cp = mp.mpf(c) * (1 - rho) if cprime is None else mp.mpf(cprime)
    delta = mp.mpf(c) / ((1 - rho) * n)
    rs = rho_start_of(b, c, n)
    pU = _int01(lambda u: mp.e ** (-cp * _Hdelta(u, delta)))
    tU = _int01(lambda u: (1 - u) * mp.e ** (-cp * _Hdelta(u, delta)))
    epsR = (rs / rho) * tU + (1 + cp * tU) / ((1 - rho) * n)
    return (1 - rho) * pU + rho * epsR


def phi_RED2B(b, c, n):
    cpp = mp.mpf(c) * (1 - mp.mpf(c) / n) ** (b - 1)
    return phi_RED2(b, c, n, cprime=cpp)


if __name__ == "__main__":
    print("ref2_formula selfcheck")
    for (b, c, n) in [(8, 40, 32768), (100, 400, 65536), (100, 600, 65536),
                      (400, 100, 65536), (200, 600, 65536)]:
        rho = rho_of(b, c, n)
        P = 1 / (1 - rho)
        worst = max(abs(H_closed(t, P) - H_quad(t, P))
                    for t in [0.05, 0.2, 0.5, 0.8, 0.95])
        print("  b=%4d c=%5d rho=%.4f P=%.4f  max|H_closed-H_quad|=%.2e" %
              (b, c, rho, P, worst))
        print("      phi_CAND=%.10f phi_EPSR=%.10f phi_RED=%.10f "
              "phi_RED2=%.10f phi_REDB=%.10f"
              % (phi_CAND(b, c, n), phi_EPSR(b, c, n), phi_RED(b, c, n),
                 phi_RED2(b, c, n), phi_REDB(b, c, n)))


# --------------------------------------------------------------------------
# EXACT expected pool / world densities for M-CLUST(b), including the
# short-pi-cycle correction that (2.1)/(2.2) of ATTEMPT.md drop.
#
# For a uniform permutation of [n], the cycle containing a given point has
# length L with probability exactly 1/n, L = 1..n.  A point y lies in U_rem
# iff none of pi^{-1}(y),...,pi^{-(b-1)}(y) is a seed; on a cycle of length L
# that set has min(b-1, L) DISTINCT members, so
#
#     P(y in U_rem) = (1/n) sum_{L=1}^{n} (1-p)^{min(b-1,L)}
#                   = (1/n)[ sum_{L=1}^{b-2}(1-p)^L + (n-b+2)(1-p)^{b-1} ]
#     P(y notin R)  = (1/n)[ sum_{L=1}^{b-1}(1-p)^L + (n-b+1)(1-p)^{b} ]
#
# and (2.1) P(y in U_rem) = (1-p)^{b-1} is the b^2 p / n -> 0 limit of this.
# --------------------------------------------------------------------------
def _tail_mean(m, p, n):
    """(1/n)[ sum_{L=1}^{m-1}(1-p)^L + (n-m+1)(1-p)^m ]  for m <= n."""
    p = mp.mpf(p)
    q = 1 - p
    if m <= 1:
        return (mp.mpf(n - m + 1) * q ** m) / n
    S = q * (1 - q ** (m - 1)) / p
    return (S + (n - m + 1) * q ** m) / n


def pool_density_exact(b, c, n):
    """E|U_rem| / n, exactly (short pi-cycles included)."""
    return _tail_mean(b - 1, mp.mpf(c) / n, n)


def world_density_exact(b, c, n):
    """E|R^c| / n = 1 - E rho, exactly (short pi-cycles included)."""
    return _tail_mean(b, mp.mpf(c) / n, n)


def runstart_pool_density_exact(b, c, n):
    """E|R cap U_rem| / n, exactly: p (1-p)^{b-1} restricted to cycles L >= b."""
    p = mp.mpf(c) / n
    return (mp.mpf(n - b + 1) / n) * p * (1 - p) ** (b - 1)


def runstart_density_exact(b, c, n):
    """E(run-start density) = P(p in Sigma and no seed among pi^{-1..-b}(p)),
    exactly: on a pi-cycle of length L <= b the window wraps onto p itself, so
    the event is impossible there."""
    p = mp.mpf(c) / n
    return (mp.mpf(n - b) / n) * p * (1 - p) ** b


def phi_REDX(b, c, n, with_delta=False):
    """Referee's exact-moment reduction.

    Mean-matches BOTH the world and the image pool of M-CLUST(b) to M-U(C,N),
    using the exact expected densities (short pi-cycles included):

        N = n * pool_density_exact(b,c,n)          (= E|U_rem|)
        C = n * (pool_density_exact - world_density_exact)   (= E|R cap U_rem|)
        N - C = n * world_density_exact            (= E|R^c|)   -- exact identity
        C / N = the exact per-normal-step reroute rate

    and uses the exact rho, rho_start in the eps channels.  Optionally adds the
    section-6.3 chain-mass term delta.
    """
    Wd = world_density_exact(b, c, n)
    Nd = pool_density_exact(b, c, n)
    C = n * (Nd - Wd)
    rho = 1 - Wd
    rs = runstart_density_exact(b, c, n)
    if with_delta:
        delta = C / (n * Wd) * (1 / Wd)      # c/((1-rho) n) with c -> C-scale
        pU = _int01(lambda u: mp.e ** (-C * _Hdelta(u, delta)))
        tU = _int01(lambda u: (1 - u) * mp.e ** (-C * _Hdelta(u, delta)))
    else:
        pU, tU = phi_U(C), T_U(C)
    epsR = (rs / rho) * tU + (1 + C * tU) / (Wd * n)
    return Wd * pU + rho * epsR
