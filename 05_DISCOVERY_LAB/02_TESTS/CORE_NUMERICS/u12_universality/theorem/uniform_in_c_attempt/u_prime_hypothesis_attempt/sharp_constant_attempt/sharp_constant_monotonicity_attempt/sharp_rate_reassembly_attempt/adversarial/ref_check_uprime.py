# ref_check_uprime.py -- referee check R2: the sharp (U') input of par.3.
# R2a: M_K identity: engine T(K+1,K) == Q(K+1)-(K+1)phi_K, exact.
# R2b: M_K < a*.sqrt(K), certified (compare against ASTAR_LO*sqrt_lo(K)).
# R2c: interior n: 0 <= T(n,K) <= M_K, T nonincreasing in n (spot grid).
# R2d: boundary K=n: |Q(n)-n phi_n| < a*.sqrt(n), exact dense + certified
#      truncated Q at n=5000,10000,30000,50000.
# R2e: re-derivation of the Estagio-19 referee's par.8 boundary algebra:
#      certified 3c^2<1 with c=(1/11)sqrt(pi/2)+sqrt(pi)/4; certified
#      a*sqrt(67)>3; the two O(1/sqrt n) conversion facts.
import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import (phi_K, Q_exact, Q_bracket_truncated, phi_nK,
                        sqrt_bracket, ASTAR_LO, ASTAR_HI, PI_LO, PI_HI,
                        SQRT_PI_LO, SQRT_PI_HI)

t0 = time.time()
fails = 0
checks = 0
def rec(ok, msg):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("  ** FAIL:", msg)

print("== R2a: M_K identity, exact, K=1..300 ==")
bad = 0
for K in range(1, 301):
    n = K + 1
    MK_id = Q_exact(K + 1) - (K + 1) * phi_K(K)
    T = n * (phi_nK(n, K) - phi_K(K))
    if T != MK_id:
        bad += 1
rec(bad == 0, f"M_K identity mismatches: {bad}")
print(f"  300/300 exact, mismatches={bad}, elapsed {time.time()-t0:.0f}s")

print("== R2b: 0 <= M_K < a* sqrt(K), certified, K=1..1000 + sparse to 5000 ==")
Ks = list(range(1, 1001)) + [1200, 1500, 2000, 2500, 3000, 4000, 5000]
worst = (0, None)
bad = 0
for K in Ks:
    MK = Q_exact(K + 1) - (K + 1) * phi_K(K)
    rhs_lo = ASTAR_LO * sqrt_bracket(K)[0]
    if not (0 < MK < rhs_lo):
        bad += 1
    r = MK / rhs_lo
    if r > worst[0]:
        worst = (r, K)
rec(bad == 0, f"M_K bound violations: {bad}")
print(f"  {len(Ks)} pts, violations={bad}, max certified ratio "
      f"{float(worst[0]):.6f} at K={worst[1]}, elapsed {time.time()-t0:.0f}s")

print("== R2c: interior-n monotonicity and 0<=T<=M_K (spot grid) ==")
bad = 0
cnt = 0
for K in [1, 2, 3, 5, 8, 13, 21, 40, 80]:
    MK = Q_exact(K + 1) - (K + 1) * phi_K(K)
    prev = None
    for n in [K + 1, K + 2, K + 3, K + 5, K + 10, K + 30, K + 100]:
        T = n * (phi_nK(n, K) - phi_K(K))
        cnt += 1
        if not (0 <= T <= MK):
            bad += 1
        if prev is not None and T > prev:
            bad += 1
        prev = T
rec(bad == 0, f"interior violations: {bad}")
print(f"  {cnt} cells, violations={bad}")

print("== R2d: boundary K=n: |Q(n)-n phi_n| < a* sqrt(n) ==")
bad = 0
worstb = (0, None)
ns = list(range(1, 601)) + [700, 800, 1000, 1200, 1500, 2000]
for n in ns:
    d = abs(Q_exact(n) - n * phi_K(n))
    rhs_lo = ASTAR_LO * sqrt_bracket(n)[0]
    if not d < rhs_lo:
        bad += 1
    r = d / rhs_lo
    if r > worstb[0]:
        worstb = (r, n)
# exact anchors
rec(abs(Q_exact(1) - 1 * phi_K(1)) == F(1, 3), "anchor n=1: 1/3")
rec(abs(Q_exact(2) - 2 * phi_K(2)) == F(13, 30), "anchor n=2: 13/30")
print(f"  exact anchors: n=1 -> {abs(Q_exact(1)-phi_K(1))}, "
      f"n=2 -> {abs(Q_exact(2)-2*phi_K(2))}")
# certified truncated Q at large n; n phi_n bracket via Lemma 4.1 sandwich:
#   sqrt(pi)/2 * n/sqrt(n+1) < n phi_n < sqrt(pi)/2 * sqrt(n)   (z/v bounds)
for n in [5000, 10000, 30000, 50000]:
    Qlo, Qhi = Q_bracket_truncated(n)
    slo, shi = sqrt_bracket(n)
    s1lo, s1hi = sqrt_bracket(n + 1)
    nphi_lo = SQRT_PI_LO / 2 * F(n) / s1hi
    nphi_hi = SQRT_PI_HI / 2 * shi
    d_hi = max(abs(Qhi - nphi_lo), abs(Qlo - nphi_hi))
    rhs_lo = ASTAR_LO * slo
    ok = d_hi < rhs_lo
    if not ok:
        bad += 1
    print(f"  n={n}: |Q-n.phi_n| <= {float(d_hi):.6f} < "
          f"{float(rhs_lo):.6f} : {ok}")
rec(bad == 0, f"boundary violations: {bad}")
print(f"  {len(ns)+4} boundary pts, violations={bad}, worst exact ratio "
      f"{float(worstb[0]):.6f} at n={worstb[1]}, elapsed {time.time()-t0:.0f}s")

print("== R2e: re-derived Estagio-19 referee par.8 algebra, certified ==")
# upper side constant c = (1/11) sqrt(pi/2) + sqrt(pi)/4 ; need 3 c^2 < 1
c_hi = sqrt_bracket(PI_HI / 2)[1] / 11 + SQRT_PI_HI / 4
rec(3 * c_hi * c_hi < 1, "3c^2 < 1")
print(f"  c_hi = {float(c_hi):.9f}, 3*c_hi^2 = {float(3*c_hi*c_hi):.9f} < 1 :",
      3 * c_hi * c_hi < 1)
# lower side threshold: a* sqrt(67) > 3
val = ASTAR_LO * sqrt_bracket(67)[0]
rec(val > 3, "a* sqrt(67) > 3")
print(f"  a*_lo*sqrt(67)_lo = {float(val):.6f} > 3 :", val > 3)
# and a* sqrt(66) < 3 (so 67 is the right threshold; informational)
print(f"  a*_hi*sqrt(66)_hi = {float(ASTAR_HI*sqrt_bracket(66)[1]):.6f}"
      " (info: <3 confirms threshold)")
# conversion inequality 1/sqrt(1+x) >= 1 - x/2 on [0,3]:
#   (1-x/2)^2 (1+x) - 1 = x^2(x-3)/4 <= 0  -- verify symbolically by expansion
import sympy as sp
x = sp.symbols('x')
expr = sp.expand((1 - x / 2)**2 * (1 + x) - 1 - x**2 * (x - 3) / 4)
rec(expr == 0, "conversion identity")
print("  (1-x/2)^2(1+x)-1 == x^2(x-3)/4 symbolically:", expr == 0)
# full upper-side chain at a few exact n: Q(n)-n.phi_n < a*sqrt(n)-1/3+c/sqrt(n)
bad2 = 0
for n in [3, 5, 10, 50, 200, 500]:
    lhs = Q_exact(n) - n * phi_K(n)
    rhs = (ASTAR_LO * sqrt_bracket(n)[0] - F(1, 3)
           + c_hi / sqrt_bracket(n)[0])
    if not lhs < rhs:
        bad2 += 1
rec(bad2 == 0, "upper-side chain spot check")
print(f"  upper-side chain Q-n.phi_n < a*sqrt(n)-1/3+c/sqrt(n), 6 pts, "
      f"violations={bad2}")
# Theorem 5 (Estagio 13) spot check: Q(n) >= sqrt(pi n/2) - 6
bad3 = 0
for n in [1, 2, 5, 10, 100, 1000, 2000]:
    if not Q_exact(n) >= sqrt_bracket(PI_LO * n / 2)[0] - 6:
        bad3 += 1
rec(bad3 == 0, "Theorem 5 spot check")
print(f"  Q(n) >= sqrt(pi n/2)-6 spot check, 7 pts, violations={bad3}")

print(f"== R2 SUMMARY: {checks} checks, {fails} failures, "
      f"elapsed {time.time()-t0:.0f}s ==")
sys.exit(1 if fails else 0)
