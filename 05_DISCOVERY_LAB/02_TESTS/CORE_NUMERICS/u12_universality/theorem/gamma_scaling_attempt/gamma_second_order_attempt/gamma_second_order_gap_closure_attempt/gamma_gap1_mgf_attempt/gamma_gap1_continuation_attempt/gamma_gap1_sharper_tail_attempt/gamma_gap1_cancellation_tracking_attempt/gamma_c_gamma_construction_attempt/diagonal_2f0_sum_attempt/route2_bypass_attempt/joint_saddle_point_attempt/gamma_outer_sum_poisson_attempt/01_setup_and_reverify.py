#!/usr/bin/env python3
"""
Script 01 -- GAMMA-OUTER-SUM-POISSON-ATTEMPT, wave 33 front (b).

Light re-verification (per this lineage's established discipline: never
trust a citable predecessor fact blindly before building new analysis on
top of it) of the facts this front CITES from THEOREM.md Estagios 54/56/57
and the joint_saddle_point_attempt ATTEMPT.md:

  (A) T(n,m) = C(n+m+1, 2m+1) * (1/B(m+1,m+1)) * I(n,m,gamma),
      I(n,m,gamma) = int_0^1 t^m (1-t)^m (1-gamma t)^(n-m) dt.
      [Estagio 54, referee's Pfaff/Beta closed form -- PROVED]

  (B) term_m(n,gamma) := (gamma^m / n^m) * m! * T(n,m),
      S_n'(gamma) := 1 + S_n(gamma) = sum_{m=0}^n term_m(n,gamma).
      [predecessor's double-sum-swap identity -- PROVED, cited]

  (C) term_0(n,gamma) = (1 - (1-gamma)^(n+1)) / gamma  -->  1/gamma
      as n -> infinity.  [predecessor script 01 part D, cited exact fact]

  (D) T_prof(lambda,gamma) = (1/gamma) * exp[-((2-gamma)/(2*gamma)) * lambda^2]
      [Estagio 56 finding 2, PROVED/confirmed, cited]
      and its leading integral EXACTLY reproduces G_n's coefficient:
      int_0^infty T_prof(lambda,gamma) dlambda = (1/2) sqrt(pi/beta),
      beta = gamma*(2-gamma)/2.   [Estagio 56 finding 3, cited]

Every check here is against PRIMARY definitions (re-derived / re-evaluated
from scratch), not against any predecessor .py file (none was read).
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 50

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

log("=" * 78)
log("PART A: T(n,m) Beta-integral closed form vs direct double-sum definition")
log("=" * 78)

def T_nm_direct(n, m, gamma):
    """Direct double-sum-swap object, from its OWN primary definition:
    T(n,m) := sum_j C(j+m,m) C(n-j,m) (1-gamma)^j.
    (This is the object cited as PROVED at Estagio 52/54; we recompute it
    directly from this combinatorial definition, not from any closed form.)
    """
    total = mp.mpf(0)
    for j in range(0, n - m + 1):
        total += mp.binomial(j + m, m) * mp.binomial(n - j, m) * (1 - gamma) ** j
    return total

def T_nm_beta(n, m, gamma):
    """Referee's cited closed form: T(n,m) = C(n+m+1,2m+1) * I(n,m,gamma) / B(m+1,m+1)."""
    pref = mp.binomial(n + m + 1, 2 * m + 1)
    B = mp.beta(m + 1, m + 1)

    def integrand(t):
        return t ** m * (1 - t) ** m * (1 - gamma * t) ** (n - m)

    tstar = mesoscale_tstar(n, m, gamma)
    if 0 < tstar < 1:
        A = curvature_A(n, m, gamma, tstar)
        w = 8.0 / mp.sqrt(A) if A > 0 else 0.05
        lo = max(mp.mpf('1e-30'), tstar - w)
        hi = min(1 - mp.mpf('1e-30'), tstar + w)
        breakpoints = sorted(set([0, float(lo), float(tstar), float(hi), 1]))
    else:
        breakpoints = [0, 1]
    val = mp.quad(integrand, breakpoints)
    return pref * val / B

def mesoscale_tstar(n, m, gamma):
    """Cited exact closed form (Estagio 56 finding 1, PROVED)."""
    n_, m_, g_ = mp.mpf(n), mp.mpf(m), mp.mpf(gamma)
    disc = g_ ** 2 * n_ ** 2 + 4 * (1 - g_) * m_ ** 2
    return (2 * m_ + g_ * n_ - mp.sqrt(disc)) / (2 * g_ * (m_ + n_))

def curvature_A(n, m, gamma, t):
    n_, m_, g_ = mp.mpf(n), mp.mpf(m), mp.mpf(gamma)
    gpp = -m_ / t ** 2 - m_ / (1 - t) ** 2 - g_ ** 2 * (n_ - m_) / (1 - g_ * t) ** 2
    return -gpp

max_rel_err_A = mp.mpf(0)
n_checks = 0
for n in [6, 10, 15, 22, 30]:
    for m in range(0, min(n, 5) + 1):
        for gamma in [mp.mpf('0.2'), mp.mpf('0.35'), mp.mpf('0.5'), mp.mpf('0.7'), mp.mpf('0.85')]:
            if m > n:
                continue
            Td = T_nm_direct(n, m, gamma)
            Tb = T_nm_beta(n, m, gamma)
            rel = abs(Td - Tb) / abs(Td) if Td != 0 else abs(Tb)
            max_rel_err_A = max(max_rel_err_A, rel)
            n_checks += 1

log(f"Checked {n_checks} (n,m,gamma) triples, n in [6,30], m in [0,5], 5 gamma values.")
log(f"Max relative error, direct double-sum vs Beta-integral closed form: {max_rel_err_A}")
assert max_rel_err_A < mp.mpf('1e-35'), "FACT (A) FAILED re-verification"
log("FACT (A) re-verified: PASS (closed form matches primary combinatorial definition).")

log("")
log("=" * 78)
log("PART B: term_m(n,gamma) = (gamma^m/n^m) m! T(n,m); term_0 exact limit")
log("=" * 78)

def term_m(n, m, gamma, T_nm_func=T_nm_beta):
    n_, g_ = mp.mpf(n), mp.mpf(gamma)
    return (g_ ** m / n_ ** m) * mp.factorial(m) * T_nm_func(n, m, gamma)

# term_0(n,gamma) primary definition check: at m=0, T(n,0) = sum_j C(n-j,0)*(1-gamma)^j
# = sum_{j=0}^n (1-gamma)^j = (1-(1-gamma)^{n+1})/gamma.  term_0 = (gamma^0/n^0)*0!*T(n,0)
# = T(n,0) itself.  So term_0(n,gamma) = (1-(1-gamma)^{n+1})/gamma -> 1/gamma. Recompute
# DIRECTLY from the T(n,0) double sum (not the claimed closed form) as the primary check.
log("term_0(n,gamma) direct-sum vs claimed closed form (1-(1-g)^(n+1))/g, and limit 1/g:")
for gamma in [mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.8')]:
    for n in [50, 500, 5000]:
        T0_direct = T_nm_direct(n, 0, gamma)
        T0_closed = (1 - (1 - gamma) ** (n + 1)) / gamma
        rel = abs(T0_direct - T0_closed) / abs(T0_direct)
        log(f"  gamma={float(gamma)}, n={n}: T0_direct={float(T0_direct):.12f}, "
            f"T0_closed={float(T0_closed):.12f}, rel_err={float(rel):.3e}")
        assert rel < mp.mpf('1e-30')
    lim_val = 1 / gamma
    T0_big = (1 - (1 - gamma) ** (5001)) / gamma
    log(f"  gamma={float(gamma)}: T0(n=5000)={float(T0_big):.15f} vs 1/gamma={float(lim_val):.15f}, "
        f"diff={float(abs(T0_big-lim_val)):.3e}")
log("FACT (C) re-verified: PASS (term_0 -> 1/gamma exactly, exponentially fast).")

log("")
log("=" * 78)
log("PART D: T_prof(lambda,gamma) closed form -- symbolic re-derivation sanity")
log("=" * 78)

lam, g = sp.symbols('lambda gamma', positive=True)
T_prof_expr = sp.Rational(1) / g * sp.exp(-((2 - g) / (2 * g)) * lam ** 2)
log("T_prof(lambda,gamma) [cited, Estagio 56 finding 2] =", T_prof_expr)
log("T_prof(0,gamma) =", sp.simplify(T_prof_expr.subs(lam, 0)), " (matches term_0 limit 1/gamma: PASS)")

beta_sym = g * (2 - g) / 2

# sympy's raw integrate()/simplify() on T_prof directly hits a branch-cut
# artifact (sqrt(-1/(gamma-2)) vs sqrt(2-gamma) disagreeing on which square
# root sympy prefers for a symbol only declared positive, not restricted to
# (0,2)) -- NOT a math error, just a simplification-path issue. Route around
# it by substituting the standard closed form for the general Gaussian
# integral int_0^oo exp(-a*x^2)dx = sqrt(pi)/(2*sqrt(a)) for a fresh POSITIVE
# symbol a, then plugging in a = (2-gamma)/(2*gamma) afterward -- the
# textbook derivation, not sympy's own (possibly branch-ambiguous) engine.
a_sym = sp.symbols('a', positive=True)
gaussian_integral_generic = sp.sqrt(sp.pi) / (2 * sp.sqrt(a_sym))  # int_0^oo exp(-a x^2) dx
a_val = (2 - g) / (2 * g)
integral_val = sp.Rational(1) / g * gaussian_integral_generic.subs(a_sym, a_val)
integral_val = sp.simplify(sp.powsimp(integral_val, force=True))

target = sp.Rational(1, 2) * sp.sqrt(sp.pi / beta_sym)
target = sp.simplify(sp.powsimp(target, force=True))

# Now both sides are simple sqrt(pi/(gamma*(2-gamma)))-type expressions;
# compare via the ratio (robust to any remaining sqrt-normalization
# difference) rather than the raw difference.
ratio = sp.simplify(sp.powsimp(integral_val / target, force=True))
log("int_0^oo T_prof dlambda [via textbook Gaussian formula, a>0 fresh symbol] =", integral_val)
log("target (1/2) sqrt(pi/beta), beta=gamma(2-gamma)/2 =", target)
log("ratio (integral_val / target), force-simplified =", ratio, " (PASS if == 1)")
assert ratio == 1, "FACT (D), G_n-reproducing integral, FAILED re-verification"
log("FACT (D) re-verified via textbook substitution route: PASS (ratio == 1 exactly).")

# Independent numeric cross-check at 6 rational gamma values (routes around
# any remaining symbolic-simplification fragility with a fully independent
# check: direct high-precision mpmath quadrature of T_prof against the
# closed-form target).
log("Independent mpmath numeric cross-check (dps 50), 6 rational gamma:")
for gfrac in [mp.mpf(1) / 7, mp.mpf(1) / 3, mp.mpf(1) / 2, mp.mpf(2) / 3, mp.mpf(4) / 5, mp.mpf(9) / 10]:
    def Tprof_mp(lmb, gval=gfrac):
        return (1 / gval) * mp.e ** (-((2 - gval) / (2 * gval)) * lmb ** 2)
    num_int = mp.quad(Tprof_mp, [0, mp.inf])
    beta_mp = gfrac * (2 - gfrac) / 2
    tgt = mp.mpf('0.5') * mp.sqrt(mp.pi / beta_mp)
    rel = abs(num_int - tgt) / tgt
    log(f"  gamma={float(gfrac):.6f}: int={float(num_int):.15f}, target={float(tgt):.15f}, rel_err={float(rel):.3e}")
    assert rel < mp.mpf('1e-40')
log("FACT (D) numeric cross-check: PASS at all 6 points.")

with open("01_setup_and_reverify.log", "w") as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written to 01_setup_and_reverify.log")
