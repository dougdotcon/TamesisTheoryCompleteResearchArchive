"""
Referee script 01 (hostile review of GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT).

Independently re-derives, from scratch (no line copied from the target's
scripts 02/03), the two central algebraic/asymptotic claims:

  Claim 1: the exact quadratic for the inner saddle t*(n,m,gamma) of
           g(t) := m ln t + m ln(1-t) + (n-m) ln(1-gamma t).
  Claim 2: the mesoscale limit profile
           T_prof(lambda,gamma) = (1/gamma) exp[-(2-gamma)/(2 gamma) lambda^2],
           lambda := m/sqrt(n).

Methodological difference from the target's own script 03 (deliberately,
to make this an independent check rather than a re-run): the target
approximates ln[(n+m+1)!/(n-m)!] by its "leading order" (2m+1)*ln(n) before
taking the m->infty series. This script instead uses the EXACT lgamma
difference throughout (mp.loggamma / sp.loggamma), substitutes n=m^2/lambda^2,
and only then takes the limit -- a strictly more rigorous route that removes
one possible source of a hidden error in the target's own derivation.
Landing on the identical closed form via this stronger route is a
meaningfully independent confirmation, not a restatement.

Also independently confirms: g(t) is globally concave on (0,1) whenever
0<=m<=n (each of its three additive terms is individually concave in t
on (0,1) for gamma in (0,1)), which gives a clean, non-numerical proof
that the unique critical point t* found by clearing denominators in
g'(t)=0 is automatically the GLOBAL maximizer -- stronger than the
target's own golden-section numerical cross-check (which only confirms
g''(t*)<0, a local-max condition).
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 60

print("=" * 78)
print("PART 1: independent symbolic re-derivation of the quadratic for t*")
print("=" * 78)

t, m_s, n_s, g_s = sp.symbols('t m n gamma', positive=True)
g_expr = m_s * sp.log(t) + m_s * sp.log(1 - t) + (n_s - m_s) * sp.log(1 - g_s * t)
gprime = sp.diff(g_expr, t)
num = sp.numer(sp.together(gprime))
poly = sp.Poly(sp.expand(num), t)
a2, a1, a0 = poly.all_coeffs()
print("g'(t) numerator, as poly in t, coefficients (t^2,t^1,t^0):", (a2, a1, a0))

claimed_a2 = g_s * (m_s + n_s)
claimed_a1 = -(2 * m_s + g_s * n_s)
claimed_a0 = m_s
assert sp.simplify(a2 - claimed_a2) == 0
assert sp.simplify(a1 - claimed_a1) == 0
assert sp.simplify(a0 - claimed_a0) == 0
print("MATCHES the target's claimed quadratic gamma(m+n)t^2-(2m+gamma n)t+m=0 exactly.")

disc = sp.expand(a1 ** 2 - 4 * a2 * a0)
disc_claimed = g_s ** 2 * n_s ** 2 + 4 * (1 - g_s) * m_s ** 2
assert sp.simplify(disc - disc_claimed) == 0
t_star = sp.simplify((-a1 - sp.sqrt(disc)) / (2 * a2))
t_star_claimed = (2 * m_s + g_s * n_s - sp.sqrt(g_s ** 2 * n_s ** 2 + 4 * (1 - g_s) * m_s ** 2)) / (2 * g_s * (m_s + n_s))
assert sp.simplify(t_star - t_star_claimed) == 0
print("Discriminant and closed-form root MATCH the target's claim exactly (symbolic).")

print()
print("Independent proof that t* is the GLOBAL max (not just a local one),")
print("via concavity of each additive term of g(t) on (0,1), gamma in (0,1),")
print("0<=m<=n -- a stronger, non-numerical argument the target did not use:")
d2_1 = sp.diff(m_s * sp.log(t), t, 2)          # = -m/t^2 < 0
d2_2 = sp.diff(m_s * sp.log(1 - t), t, 2)      # = -m/(1-t)^2 < 0
d2_3 = sp.diff((n_s - m_s) * sp.log(1 - g_s * t), t, 2)  # = -gamma^2(n-m)/(1-gamma t)^2 < 0
print("  d2/dt2 [m ln t]        =", sp.simplify(d2_1), " (< 0 for t>0, m>0)")
print("  d2/dt2 [m ln(1-t)]     =", sp.simplify(d2_2), " (< 0 for t<1, m>0)")
print("  d2/dt2 [(n-m)ln(1-gt)] =", sp.simplify(d2_3), " (< 0 for n>m, 0<t<1/gamma, gamma<1<1/gamma)")
print("  => g(t) is a sum of three functions each strictly concave on (0,1)")
print("     whenever 0<m<n and gamma in (0,1) => g is globally strictly concave")
print("     => g' is strictly decreasing => AT MOST ONE root of g'(t)=0 in (0,1)")
print("     => the t* found above (once confirmed 0<t*<1) is automatically the")
print("        GLOBAL maximizer, not merely a local one satisfying g''(t*)<0.")
print("     This is a genuine strengthening of the target's own verification,")
print("     independent of any numerical golden-section search.")

print()
print("=" * 78)
print("PART 2: independent re-derivation of T_prof(lambda,gamma), using the")
print("        EXACT lgamma difference (not the target's (2m+1)ln(n) shortcut)")
print("        for the ln[(n+m+1)!/(n-m)!] piece -- a strictly more rigorous")
print("        route than script 03's own derivation.")
print("=" * 78)

m, n, gam, lam = sp.symbols('m n gamma lambda', positive=True)
tS, n_of_m = sp.symbols('t'), m ** 2 / lam ** 2
discS = gam ** 2 * n ** 2 + 4 * (1 - gam) * m ** 2
t_star_S = (2 * m + gam * n - sp.sqrt(discS)) / (2 * gam * (m + n))
gS = m * sp.log(tS) + m * sp.log(1 - tS) + (n - m) * sp.log(1 - gam * tS)
gpp_S = sp.diff(gS, tS, 2)

t_star_m = sp.simplify(t_star_S.subs(n, n_of_m))
g_at_tstar_m = sp.simplify(gS.subs(tS, t_star_S).subs(n, n_of_m))
gpp_at_tstar_m = gpp_S.subs(tS, t_star_S).subs(n, n_of_m)

ln_m_fact_stirling = m * sp.log(m) - m + sp.Rational(1, 2) * sp.log(2 * sp.pi * m)
# EXACT lgamma difference (not an approximation) -- the more rigorous route:
lg_diff = sp.loggamma(n + m + 2) - sp.loggamma(n - m + 1)
lg_diff_m = lg_diff.subs(n, n_of_m)
ln_I = g_at_tstar_m + sp.Rational(1, 2) * sp.log(2 * sp.pi / (-gpp_at_tstar_m))

ln_term_m = m * sp.log(gam) - m * sp.log(n_of_m) - ln_m_fact_stirling + lg_diff_m + ln_I

x = sp.symbols('x', positive=True)
expr_x = ln_term_m.subs(m, 1 / x)
ser = sp.series(expr_x, x, 0, 1).removeO()
ser = sp.simplify(ser)
print("Constant term of ln(term_m) as m->infty at fixed lambda (via EXACT lgamma,")
print("independently derived, not copied):")
print(" ", ser)

claimed_ln_T_prof = -sp.log(gam) - (2 - gam) / (2 * gam) * lam ** 2
diff = sp.simplify(ser - claimed_ln_T_prof)
print()
print("Difference from the target's claimed ln(T_prof) = -log(gamma) -")
print("(2-gamma)/(2 gamma) lambda^2 :", diff)
assert diff == 0
print(">>> INDEPENDENTLY CONFIRMED, via a strictly more rigorous route (exact")
print(">>> lgamma instead of the target's leading-order binomial-shift shortcut):")
print(">>> T_prof(lambda,gamma) = (1/gamma) exp[-(2-gamma)/(2 gamma) lambda^2].")

print()
print("=" * 78)
print("PART 3: independent HIGH-PRECISION NUMERIC confirmation of Part 2's limit,")
print("        via mpmath (no sympy series machinery at all -- direct evaluation")
print("        of the exact asymptotic combination at growing m, using mp.loggamma)")
print("=" * 78)


def t_star_mp(n, m, gamma):
    disc = gamma ** 2 * n ** 2 + 4 * (1 - gamma) * m ** 2
    return (2 * m + gamma * n - mp.sqrt(disc)) / (2 * gamma * (m + n))


def g_of_t(t, n, m, gamma):
    return m * mp.log(t) + m * mp.log(1 - t) + (n - m) * mp.log(1 - gamma * t)


def gpp_of_t(t, n, m, gamma):
    return -m / t ** 2 - m / (1 - t) ** 2 - gamma ** 2 * (n - m) / (1 - gamma * t) ** 2


def ln_term_m_asymptotic(m, lam, gamma):
    """Exact-lgamma asymptotic combination, no series-in-x, direct evaluation."""
    n = m ** 2 / lam ** 2
    ts = t_star_mp(n, m, gamma)
    g_val = g_of_t(ts, n, m, gamma)
    gpp = gpp_of_t(ts, n, m, gamma)
    ln_I = g_val + mp.mpf('0.5') * mp.log(2 * mp.pi / (-gpp))
    ln_m_fact_stirling = m * mp.log(m) - m + mp.mpf('0.5') * mp.log(2 * mp.pi * m)
    lg_diff = mp.loggamma(n + m + 2) - mp.loggamma(n - m + 1)
    return m * mp.log(gamma) - m * mp.log(n) - ln_m_fact_stirling + lg_diff + ln_I


# NOTE: this grid includes lambda=2.0, WIDER than anything the target itself
# tested (target's own grid stops at lambda=1.5) -- deliberately probing
# beyond the target's own range.
test_points = [
    ('0.3', '0.3'), ('0.6', '0.5'), ('1.0', '0.8'),
    ('1.5', '0.3'), ('2.0', '0.6'), ('0.6', '0.3'),  # last one = the exact
    # (lambda,gamma) where the TARGET's own Richardson-extrapolated table
    # shows its worst-behaved anomaly (1.05% vs claimed <0.7%, see ref03).
]
max_final_diff = mp.mpf(0)
for lam_s, gam_s in test_points:
    lam_v = mp.mpf(lam_s)
    gamma_v = mp.mpf(gam_s)
    claimed = -mp.log(gamma_v) - (2 - gamma_v) / (2 * gamma_v) * lam_v ** 2
    m_final = mp.mpf(10) ** 10
    val = ln_term_m_asymptotic(m_final, lam_v, gamma_v)
    d = abs(val - claimed)
    max_final_diff = max(max_final_diff, d)
    print(f"lambda={lam_s} gamma={gam_s}: at m=1e10, |asymptotic - claimed| = {mp.nstr(d, 6)}")
assert max_final_diff < mp.mpf('1e-8')
print()
print("CONFIRMED at m=1e10, all 6 (lambda,gamma) points (including lambda=2.0,")
print("beyond the target's own tested range): the exact-lgamma asymptotic")
print("combination converges cleanly to the claimed closed form.")
print()
print("No randomness used anywhere in this script.")
