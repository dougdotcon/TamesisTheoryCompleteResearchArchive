"""
Script 05: reconciling this front's mesoscale curvature A(gamma) =
(2-gamma)/(2 gamma) (script 03, valid for m = Theta(sqrt n)) with the
predecessor's PROVED near-origin local decay rate c(gamma) = 2(1-gamma)/
gamma (Estagio 52 / diagonal_2f0_sum_attempt/ATTEMPT.md Section 4, valid
at FIXED small m as n -> infty).

Self-caught issue, disclosed (see ATTEMPT.md "Self-caught issues"): a
first attempt at this script's underlying derivation treated m as a FREE
symbol (not scaled with n) in the SAME Laplace/Stirling formula used for
the mesoscale profile (script 03), took n -> infty at fixed symbolic m,
and got a pure quadratic-in-m correction with NO linear-in-m term --
which, evaluated at m=1, predicts a local rate of A(gamma), NOT c(gamma).
This APPEARED to contradict the predecessor's own PROVED c(gamma). Before
concluding anything was wrong (in either front's math), the apparent
contradiction was investigated directly: the Laplace/Watson approximation
used in script 03 is asymptotic *in m* (it requires m -> infty for the
integral's peak to sharpen) -- so extrapolating that SAME approximation
formula down to m=1 is an invalid use of an asymptotic result outside its
regime of validity, not a genuine derivation of the m=1 behavior. It is
expected, not a paradox, that a fixed-m limit and an m=Theta(sqrt n)
"mesoscale" limit of the SAME family term_m(n,gamma) can have different
local curvatures -- exactly the phenomenon this script demonstrates
directly and quantitatively below, with NO invocation of the (m-large-
only-valid) Laplace formula: c(gamma) and A(gamma) are two different,
both individually correct, facts about term_m, valid in two different
regimes (m=O(1) vs m=Theta(sqrt n)), and this script exhibits the
CROSSOVER between them using only the exact (non-asymptotic) formula for
term_m.

This does not correct or contradict anything in the predecessor's or any
ancestor's record -- c(gamma) remains exactly as proved. It is a new,
disclosed piece of understanding from this front: the specific curvature
that governs the OUTER SUM's dominant mass (m=Theta(sqrt n), which is what
actually controls S_n') is A(gamma), not c(gamma)/2 -- worth flagging
explicitly since the predecessor's own prose ("consistent with ... a
Gaussian envelope term_m~term_0*exp(-c(gamma)m^2/(2n))") could otherwise
be read as claiming the near-origin rate governs the WHOLE profile, which
this script shows numerically it does not (the predecessor's own text
already carefully hedges this specific extrapolation as "numerically
supported", not "PROVED" -- this script sharpens exactly which part of
that claim holds and which doesn't).
"""
import mpmath as mp

mp.mp.dps = 60


def t_star_mp(n, m, gamma):
    n = mp.mpf(n); m = mp.mpf(m); gamma = mp.mpf(gamma)
    disc = gamma ** 2 * n ** 2 + 4 * (1 - gamma) * m ** 2
    return (2 * m + gamma * n - mp.sqrt(disc)) / (2 * gamma * (m + n))


def term_m_beta_robust(n, m, gamma, maxdegree=10):
    n_mp = mp.mpf(n); m_mp = mp.mpf(m)
    Cnorm = mp.binomial(n_mp + m_mp + 1, 2 * m_mp + 1)
    beta_pref = mp.factorial(2 * m_mp + 1) / (mp.factorial(m_mp) ** 2)
    integrand = lambda t: t ** m_mp * (1 - t) ** m_mp * (1 - gamma * t) ** (n_mp - m_mp)
    if m == 0:
        integral_val = mp.quad(integrand, [0, 1])
    else:
        ts = t_star_mp(n, m, gamma)
        gpp = -m_mp / ts ** 2 - m_mp / (1 - ts) ** 2 - gamma ** 2 * (n_mp - m_mp) / (1 - gamma * ts) ** 2
        width = 1 / mp.sqrt(-gpp)
        pts = sorted(set([mp.mpf(0), max(mp.mpf(0), ts - 6 * width), ts,
                           min(mp.mpf(1), ts + 6 * width), mp.mpf(1)]))
        integral_val = mp.quad(integrand, pts, maxdegree=maxdegree)
    T = Cnorm * beta_pref * integral_val
    return (gamma ** m_mp) * mp.factorial(m_mp) * T / (n_mp ** m_mp)


print("=" * 78)
print("Part A: confirm the near-origin (m=1) local rate -> c(gamma)=2(1-gamma)/gamma")
print("        as n grows, at FIXED m=1 (reproducing the predecessor's own PROVED")
print("        fact, independently, via THIS front's Beta-integral route)")
print("=" * 78)
for gnum, gden in [(1, 3), (1, 2), (3, 5)]:
    gamma = mp.mpf(gnum) / mp.mpf(gden)
    c_gamma = 2 * (1 - gamma) / gamma
    print(f"gamma={gnum}/{gden}: predecessor's c(gamma)=2(1-gamma)/gamma = {mp.nstr(c_gamma,10)}")
    for n_val in [2000, 20000, 200000, 2000000]:
        t0 = term_m_beta_robust(n_val, 0, gamma)
        t1 = term_m_beta_robust(n_val, 1, gamma)
        rate = -n_val * mp.log(t1 / t0)
        print(f"    n={n_val:>8}: local rate at m=0->1 = {mp.nstr(rate,10)} "
              f"(target {mp.nstr(c_gamma,10)}, diff {mp.nstr(abs(rate-c_gamma),4)})")
    print()

print("=" * 78)
print("Part B: the local curvature CROSSOVER as m grows from O(1) to Theta(sqrt n),")
print("        at large FIXED n -- from c(gamma)/2 (near m=0) to A(gamma) (m~sqrt n)")
print("=" * 78)
for gnum, gden in [(1, 3), (1, 2)]:
    gamma = mp.mpf(gnum) / mp.mpf(gden)
    c_half = (1 - gamma) / gamma
    A_gamma = (2 - gamma) / (2 * gamma)
    print(f"gamma={gnum}/{gden}: c(gamma)/2={mp.nstr(c_half,8)}  A(gamma)={mp.nstr(A_gamma,8)}")
    n_val = 4_000_000
    sqrt_n = mp.sqrt(n_val)
    print(f"  (n={n_val}, sqrt(n)={mp.nstr(sqrt_n,6)})")
    m_list = [0, 1, 2, 4, 8, 16, 32, 64, int(sqrt_n / 4), int(sqrt_n / 2), int(sqrt_n), int(1.5 * sqrt_n)]
    prev_term = None
    prev_m = None
    for m_val in m_list:
        t = term_m_beta_robust(n_val, m_val, gamma)
        if prev_term is not None:
            dm2 = m_val ** 2 - prev_m ** 2
            local_curv = -n_val * mp.log(t / prev_term) / dm2 if dm2 != 0 else mp.mpf('nan')
            lam_here = m_val / sqrt_n
            print(f"    m={m_val:>7} (lambda={mp.nstr(lam_here,4)}): "
                  f"local curvature over [prev_m,m] = {mp.nstr(local_curv,8)}")
        prev_term = t
        prev_m = m_val
    print(f"    -> should read ~{mp.nstr(c_half,6)} near m=O(1), drifting toward "
          f"~{mp.nstr(A_gamma,6)} as m approaches Theta(sqrt n).")
    print()

print("Interpretation: the local curvature is NOT constant across the whole range of")
print("m -- it starts near c(gamma)/2 = (1-gamma)/gamma for m=O(1) and drifts toward")
print("A(gamma) = (2-gamma)/(2 gamma) as m grows into the Theta(sqrt n) mesoscale that")
print("dominates the outer sum S_n'. Both endpoints are individually consistent with")
print("independently-verified facts (predecessor's c(gamma) at one end, this front's")
print("T_prof at the other) -- the crossover itself, and the fact that it is A(gamma),")
print("not c(gamma)/2, that governs the mass-dominant range, is this front's own,")
print("newly disclosed, structural finding.")
