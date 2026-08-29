"""
Referee script 03: scrutiny of the target's claim 4 (Section 6, VERDICT
item 4) -- the "local-rate crossover" from c(gamma)/2 (claimed near-origin
value, m=O(1)) to A(gamma) (mesoscale value, m=Theta(sqrt n)).

This script:
  (1) Re-checks the arithmetic of the target's own illustrative example
      ("e.g. gamma=1/3: c(gamma)/2=1, A(gamma)=2.5", ATTEMPT.md Section 6).
  (2) Re-derives what the target's own script 05 actually PRINTS at the
      very first data point of its crossover grid (m=1, i.e. the step
      m=0->1) and shows this is, by direct algebraic construction, IDENTICAL
      to c(gamma) itself (Part A's own quantity), not c(gamma)/2 -- because
      the "local curvature" formula used in script 05 Part B divides by
      dm^2 = m^2 - prev_m^2, which equals exactly 1 at the very first step
      (m=0 to m=1), making local_curv(0,1) = c(n,gamma) by construction,
      identical to Part A's own printed value at that same n.
"""
import mpmath as mp
from fractions import Fraction as F

mp.mp.dps = 60

print("=" * 78)
print("(1) Arithmetic check of the target's own illustrative example")
print("    ('gamma=1/3: c(gamma)/2=1, A(gamma)=2.5', ATTEMPT.md Section 6)")
print("=" * 78)

gamma = F(1, 3)
c_gamma = 2 * (1 - gamma) / gamma
A_gamma = (2 - gamma) / (2 * gamma)
print(f"c(1/3) = 2(1-gamma)/gamma = {c_gamma} = {float(c_gamma)}")
print(f"c(1/3)/2 = {c_gamma/2} = {float(c_gamma/2)}")
print(f"A(1/3) = (2-gamma)/(2 gamma) = {A_gamma} = {float(A_gamma)}")
print()
print("TARGET CLAIMS (ATTEMPT.md Section 6, and echoed in VERDICT item 4's")
print("framing): 'c(gamma)/2=1, A(gamma)=2.5' at gamma=1/3.")
print(f"ACTUAL VALUE: c(1/3)/2 = {float(c_gamma/2)}, NOT 1.")
assert c_gamma / 2 != 1
assert c_gamma / 2 == 2
print(">>> CONFIRMED: this specific illustrative number in ATTEMPT.md Section 6")
print(">>> is arithmetically WRONG. Correct value is c(1/3)/2 = 2, not 1.")
print("    (A(gamma)=2.5 is itself correctly stated.)")

print()
print("=" * 78)
print("(2) Does the target's own script 05 data actually show the crossover")
print("    'starting at c(gamma)/2' near m=O(1), as claimed?")
print("=" * 78)


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


gamma_v = mp.mpf(1) / 3
n_val = 4_000_000
c_g = 2 * (1 - gamma_v) / gamma_v
c_half = (1 - gamma_v) / gamma_v
A_g = (2 - gamma_v) / (2 * gamma_v)
print(f"gamma=1/3: c(gamma)={mp.nstr(c_g,8)}  c(gamma)/2={mp.nstr(c_half,8)}  A(gamma)={mp.nstr(A_g,8)}")

t0 = term_m_beta_robust(n_val, 0, gamma_v)
t1 = term_m_beta_robust(n_val, 1, gamma_v)
first_step_curv = -n_val * mp.log(t1 / t0) / (1 ** 2 - 0 ** 2)  # dm^2 = 1
print(f"Independently re-computed 'local curvature' at the FIRST step (m=0->1),")
print(f"i.e. -n*log(term_1/term_0)/(1^2-0^2) [same formula as script 05 Part B]:")
print(f"   = {mp.nstr(first_step_curv,10)}")
print()
print(f"Compare to c(gamma)     = {mp.nstr(c_g,10)}   <- MATCHES (as expected: dm^2=1")
print(f"                                                 at the first step makes this")
print(f"                                                 formula algebraically IDENTICAL")
print(f"                                                 to Part A's rate formula)")
print(f"Compare to c(gamma)/2   = {mp.nstr(c_half,10)}   <- the target's CLAIMED near-origin value")
print(f"Compare to A(gamma)     = {mp.nstr(A_g,10)}")

rel_to_c = abs(first_step_curv - c_g) / c_g
rel_to_c_half = abs(first_step_curv - c_half) / c_half
print()
print(f"Relative distance of the actual m=1 value from c(gamma):     {mp.nstr(rel_to_c,6)}")
print(f"Relative distance of the actual m=1 value from c(gamma)/2:   {mp.nstr(rel_to_c_half,6)}")
assert rel_to_c < mp.mpf('1e-4'), "expected m=1 curvature to match c(gamma), not c(gamma)/2"
assert rel_to_c_half > mp.mpf('0.9')
print()
print(">>> CONFIRMED: the target's own printed data (reproduced independently here)")
print(">>> shows the crossover's near-origin (m=1) value equals c(gamma) itself")
print(">>> (matching to 1e-6), NOT c(gamma)/2 as claimed in ATTEMPT.md Section 6 and")
print(">>> the VERDICT's framing of item 4. This is a direct algebraic consequence")
print(">>> (dm^2=1 at the very first step), not a numerical coincidence, and it is")
print(">>> visible directly in the target's OWN log (05_local_rate_crossover.log,")
print(">>> line for m=1: 'local curvature ... = 4.000002' at gamma=1/3, matching")
print(">>> c(1/3)=4.0, not c(1/3)/2=2.0).")
print()
print("The genuinely solid part of claim 4 -- that the curvature is NOT constant")
print("across the m-range, and that it converges cleanly to A(gamma) (not c(gamma)/2)")
print("by m~500-3000 -- is NOT undermined by this finding, and is independently")
print("reconfirmed via claim 1/2 above (A(gamma) is exactly the T_prof curvature).")
print("Only the specific claimed NEAR-ORIGIN VALUE 'c(gamma)/2' is unsupported by")
print("the target's own data and has no evident valid derivation anywhere in the")
print("document (neither the exact m=1 value, which is c(gamma), nor the naively-")
print("invalid mesoscale-formula-at-m=1 value, which Section 8 item 4 itself")
print("correctly identifies as A(gamma), equals c(gamma)/2).")
