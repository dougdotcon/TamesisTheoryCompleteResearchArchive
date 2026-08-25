# Adversarial referee, sharp_constant_monotonicity_attempt -- Part 3:
#   Theorem 2:  M_K < a* sqrt(K)  for every K>=1,  a* = sqrt(pi)(1/sqrt2 - 1/2).
#
#   (A) assembly re-derived: the subtraction step, the exact identity
#       sqrt(pi/2) - sqrt(pi)/2 = a*, the closed form LHS(1)=sqrt(pi)(17/11-sqrt2)
#       (sympy, symbolic zero), and the monotonicity of LHS(K);
#   (B) LHS(1) < 1/3 re-proved with the REFEREE'S OWN integer-squaring bounds
#       (different integers from the document's), pure rational arithmetic;
#   (C) the DOCUMENT'S OWN rational chain re-verified integer by integer;
#   (D) certified-rational check of the assembled elementary bound
#       Q_ub(K+1) - (sqrt(pi)/2)sqrt(K+1) < a* sqrt(K), dense + sparse;
#   (E) MAIN exact check: exact-Fraction M_K = Q(K+1) - (K+1)phi_K vs a
#       certified rational LOWER bound on a* sqrt(K); dense K=1..1000 + sparse
#       to K=10000 (exceeding the target's exact range 800/3000);
#   (F) T5e analog: exact Q(K+1) + ONLY the cited z_K-bound, certified rational.
# No randomness. None of the target's scripts/logs was read.
import sys
from fractions import Fraction as F
from math import isqrt
import mpmath as mp
import sympy as sp

mp.mp.dps = 60
LOG = []
def log(s=""):
    print(s)
    LOG.append(str(s))
fails = 0

PI_LO = F(31415926535897932, 10**16)
PI_HI = F(31415926535897933, 10**16)
D = 10**30

def sqrt_lo(fr):
    x = (fr.numerator * D * D) // fr.denominator
    return F(isqrt(x), D)

def sqrt_hi(fr):
    x = -((-fr.numerator * D * D) // fr.denominator)
    return F(isqrt(x) + 1, D)

def Q_exact(n):
    t = n ** (n - 1)
    tot = t
    for j in range(1, n):
        t = (t // n) * (n - j)
        tot += t
    return F(tot, n ** (n - 1))

def phi_exact(K):
    """phi_K = 4^K (K!)^2 / (2K+1)!  exact."""
    num = 4 ** K
    f = 1
    for i in range(2, K + 1):
        f *= i
    num *= f * f
    den = 1
    for i in range(2, 2 * K + 2):
        den *= i
    return F(num, den)

def astar_sqrtK_lower(K):
    """certified rational LOWER bound on a* sqrt(K) = sqrt(pi K/2) - sqrt(pi K)/2."""
    return sqrt_lo(PI_LO * K / 2) - sqrt_hi(PI_HI * K) / 2

def astar_sqrtK_upper(K):
    return sqrt_hi(PI_HI * K / 2) - sqrt_lo(PI_LO * K) / 2

# ----------------------------------------------------------------------------
log("=" * 78)
log("(A) ASSEMBLY RE-DERIVED (symbolic)")
log("=" * 78)
pi, K = sp.pi, sp.symbols('K', positive=True)
astar = sp.sqrt(pi) * (1 / sp.sqrt(2) - sp.Rational(1, 2))
c1 = sp.simplify(sp.sqrt(pi / 2) - sp.sqrt(pi) / 2 - astar)
log(f"  sqrt(pi/2) - sqrt(pi)/2 - a*  == {c1}   (the identity used in the display)")
# the displayed equation of the proof:
lhs_disp = sp.sqrt(pi * (K + 1) / 2) - sp.sqrt(pi) / 2 * sp.sqrt(K + 1)
c2 = sp.simplify(lhs_disp - astar * sp.sqrt(K + 1))
log(f"  sqrt(pi(K+1)/2) - (sqrt(pi)/2)sqrt(K+1) - a*sqrt(K+1)  == {c2}")
# reduction to LHS(K) < 1/3:
red = sp.simplify((astar * sp.sqrt(K + 1) - sp.Rational(1, 3)
                   + sp.sqrt(pi / (2 * (K + 1))) / 11 - astar * sp.sqrt(K))
                  - (astar * (sp.sqrt(K + 1) - sp.sqrt(K))
                     + sp.sqrt(pi / (2 * (K + 1))) / 11 - sp.Rational(1, 3)))
log(f"  [RHS - a*sqrt(K)] - [LHS(K) - 1/3]  == {red}   (the 'it remains to show' rewrite)")
lhs1 = astar * (sp.sqrt(2) - 1) + sp.sqrt(pi) / 22
c3 = sp.simplify(lhs1 - sp.sqrt(pi) * (sp.Rational(17, 11) - sp.sqrt(2)))
log(f"  LHS(1) - sqrt(pi)(17/11 - sqrt(2))  == {c3}   (closed form confirmed)")
if any(x != 0 for x in (c1, c2, red, c3)): fails += 1

log("")
log("  Monotonicity of LHS(K) (referee re-derivation): sqrt(K+1)-sqrt(K) =")
log("  1/(sqrt(K+1)+sqrt(K)), denominator strictly increasing => term strictly")
log("  decreasing; sqrt(pi/(2(K+1))) strictly decreasing. Sum of two strictly")
log("  decreasing positive terms is strictly decreasing => LHS(K) <= LHS(1).")
d1 = sp.simplify(sp.diff(sp.sqrt(K + 1) - sp.sqrt(K), K))
d1s = sp.simplify(d1 * 2 * sp.sqrt(K) * sp.sqrt(K + 1) * (sp.sqrt(K + 1) + sp.sqrt(K)))
log(f"  d/dK[sqrt(K+1)-sqrt(K)] = {d1}  (= (sqrt(K)-sqrt(K+1))/(2 sqrt(K K+1)) < 0)")
# numeric strict-decrease scan
prev = None
mono_bad = []
ks = list(range(1, 2001)) + [5000, 10**4, 10**5, 10**6]
for k in ks:
    v = (mp.sqrt(mp.pi)*(1/mp.sqrt(2)-mp.mpf(0.5))) * (mp.sqrt(k+1)-mp.sqrt(k)) \
        + mp.sqrt(mp.pi/(2*(k+1)))/11
    if prev is not None and not (v < prev[0]):
        mono_bad.append(k)
    if not (v < mp.mpf(1)/3):
        mono_bad.append(('>1/3', k))
    prev = (v, k)
log(f"  numeric scan K=1..2000 + sparse to 10^6: strict-decrease/'<1/3' violations: "
    f"{mono_bad if mono_bad else 'none'}")
if mono_bad: fails += 1

log("")
log("  Subtraction-step audit: Q(K+1) < UB (strict, Thm 1) and (K+1)phi_K > LB")
log("  (strict, Lemma 4.1 z-bound) => M_K = Q(K+1) - (K+1)phi_K < UB - LB, strict.")
log("  Direction of both citations checked against the parent documents' texts:")
log("  Theorem 3 gives equality M_K = Q(K+1)-(K+1)phi_K; z-bound (K+1)phi_K^2 >")
log("  pi/4 => (K+1)phi_K > (sqrt(pi)/2)sqrt(K+1) after multiplying by (K+1) and")
log("  taking positive square roots -- rearrangement re-derived and correct.")

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(B) LHS(1) < 1/3 -- REFEREE'S OWN RATIONAL PROOF (own integers, not the")
log("    document's).  LHS(1) = sqrt(pi)(17/11 - sqrt(2)).")
log("=" * 78)
# own bounds: sqrt2 > 141421356/10^8 ; sqrt(pi) < 17724539/10^7 with pi < PI_HI
a = 141421356
chk_a = a * a < 2 * 10**16
log(f"  {a}^2 = {a*a} < 2*10^16 = {2*10**16}: {chk_a}   => sqrt(2) > {a}/10^8")
b = 17724539
# need (b/10^7)^2 > PI_HI  <=>  b^2 * 10^2 > 31415926535897933
chk_b = b * b * 100 > PI_HI.numerator  # PI_HI = .../10^16, b^2/10^14 vs .../10^16
log(f"  {b}^2 * 10^2 = {b*b*100} > {PI_HI.numerator}: {chk_b}   "
    f"=> sqrt(pi) < sqrt(PI_HI) < {b}/10^7")
# positivity of the factor: 17/11 - sqrt2 > 17/11 - sqrt2_hi; need only that the
# UPPER-bound substitution direction is sound: 17/11 - sqrt2 < 17/11 - sqrt2_lo,
# and 17/11 - sqrt2_lo > 0 so multiplying the two upper bounds is legitimate.
f_up = F(17, 11) - F(a, 10**8)
log(f"  17/11 - sqrt2_lo = {f_up} = {float(f_up):.9f} > 0: {f_up > 0}")
UB = F(b, 10**7) * f_up
log(f"  LHS(1) < ({b}/10^7) * ({f_up.numerator}/{f_up.denominator}) = "
    f"{UB.numerator}/{UB.denominator} = {float(UB):.9f}")
chk_third = 3 * UB.numerator < UB.denominator
log(f"  3 * {UB.numerator} = {3*UB.numerator} < {UB.denominator}: {chk_third}"
    f"   =>  LHS(1) < 1/3.   QED (pure integers)")
if not (chk_a and chk_b and f_up > 0 and chk_third): fails += 1

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(C) THE DOCUMENT'S OWN RATIONAL CHAIN, integer by integer")
log("=" * 78)
c = []
c.append(("14142^2 = 199996164", 14142**2 == 199996164))
c.append(("199996164 < 2*10^8", 14142**2 < 2 * 10**8))
c.append(("14143^2 = 200024449", 14143**2 == 200024449))
c.append(("200024449 > 2*10^8", 14143**2 > 2 * 10**8))
c.append(("17725^2 = 314175625", 17725**2 == 314175625))
c.append(("314175625 > 3.1416e8", 17725**2 > 314160000))
c.append(("pi < 3.1416", PI_HI < F(31416, 10**4)))
# a* upper bound: (17725/10000)(10000/14142 - 1/2) -- and equality with 2076661/5656800
astar_ub_doc = F(17725, 10**4) * (F(10**4, 14142) - F(1, 2))
c.append(("(17725/10^4)(10^4/14142 - 1/2) == 2076661/5656800",
          astar_ub_doc == F(2076661, 5656800)))
# is it really an upper bound on a*? certified: a* = sqrt(pi)(1/sqrt2 - 1/2)
astar_hi_cert = sqrt_hi(PI_HI) * (1 / sqrt_lo(F(2)) - F(1, 2))
c.append(("2076661/5656800 really >= a* (referee-certified)",
          F(2076661, 5656800) > astar_hi_cert - F(1, 10**20) and
          F(2076661, 5656800) > sqrt_lo(PI_LO) * (1/sqrt_hi(F(2)) - F(1,2))))
# document's final fraction
total_doc = F(2076661, 5656800) * (F(14143, 10**4) - 1) + F(17725, 220000)
c.append(("(2076661/5656800)(4143/10^4) + 17725/220000 == 48257687251/207416000000",
          total_doc == F(48257687251, 207416000000)))
c.append(("3 * 48257687251 < 207416000000", 3 * 48257687251 < 207416000000))
for name, ok in c:
    log(f"  {name}: {ok}")
    if not ok: fails += 1
log(f"  document's rational value = {float(total_doc):.6f} (doc says ~0.232661);")
log(f"  true LHS(1) = {mp.nstr((mp.sqrt(mp.pi)*(mp.mpf(17)/11 - mp.sqrt(2))), 8)} -- "
    f"upper bound valid and direction-sound at every substitution.")

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(D) ASSEMBLED ELEMENTARY BOUND, certified rational:")
log("    Q_ub(K+1) - (sqrt(pi)/2)sqrt(K+1) < a* sqrt(K)")
log("    [Q_ub(n) = sqrt(pi n/2) - 1/3 + (1/11)sqrt(pi/(2n))]")
log("=" * 78)
viol = []
worst = None
kk = list(range(1, 601)) + [800, 1000, 2000, 5000, 10**4, 10**5]
for Kv in kk:
    n = Kv + 1
    upper = (sqrt_hi(PI_HI * n / 2) - F(1, 3) + F(1, 11) * sqrt_hi(PI_HI / (2 * n))
             - sqrt_lo(PI_LO * n) / 2)
    rhs = astar_sqrtK_lower(Kv)
    if not (upper < rhs):
        viol.append(Kv)
    m = float(rhs - upper)
    if worst is None or m < worst[0]: worst = (m, Kv)
log(f"  {len(kk)} points (dense K=1..600 + sparse to 10^5): "
    f"violations: {viol if viol else 'NONE (certified)'}")
log(f"  smallest gap {worst[0]:.6f} at K={worst[1]} (document's T5c reports "
    f"worst margin -0.1007 at K=1)")
if viol: fails += 1

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(E) MAIN EXACT CHECK: exact-Fraction M_K vs certified rational lower bound")
log("    on a* sqrt(K); dense K=1..1000 + sparse to K=10000")
log("=" * 78)
viol = []
worst = None
margins = {}
sparse = [1200, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000]
Q_cache = {}
for Kv in list(range(1, 1001)) + sparse:
    q = Q_exact(Kv + 1)
    Q_cache[Kv + 1] = q
    MK = q - (Kv + 1) * phi_exact(Kv)
    lb = astar_sqrtK_lower(Kv)
    if not (MK < lb):
        viol.append(Kv)
    m = float(astar_sqrtK_upper(Kv) - MK)   # display margin (safe upper est.)
    margins[Kv] = m
    if worst is None or m < worst[0]: worst = (m, Kv)
log(f"  {1000+len(sparse)} points, violations: "
    f"{viol if viol else 'NONE -- M_K < a* sqrt(K) certified at every point'}")
M1 = Q_cache[2] - 2 * phi_exact(1)
log(f"  M_1 = {M1} (document says 1/6 exactly): {M1 == F(1,6)}")
log(f"  margin a*sqrt(K)-M_K at K=1:     {margins[1]:.6f}  (doc: 0.2004)")
log(f"  margin at K=1000:  {margins[1000]:.6f}")
log(f"  margin at K=10000: {margins[10000]:.6f}   (-> 1/3 from below, as the")
log(f"  gap a*-r_K ~ 1/(3 sqrt(K)) implies; smallest margin {worst[0]:.6f} at K={worst[1]})")
if viol or M1 != F(1, 6): fails += 1

r10000 = float(F(Q_cache[10001].numerator, Q_cache[10001].denominator)
               - 10001 * phi_exact(10000)) / mp.sqrt(10000)
log(f"  r_10000 = M_10000/sqrt(10000) = {mp.nstr(r10000, 8)}  vs  a* = "
    f"{mp.nstr(mp.sqrt(mp.pi)*(1/mp.sqrt(2)-mp.mpf(0.5)), 8)}  (approach from below)")

# ----------------------------------------------------------------------------
log("")
log("=" * 78)
log("(F) T5e ANALOG (isolating the z_K citation + algebra from Theorem 1):")
log("    exact Q(K+1) - (sqrt(pi)/2)sqrt(K+1)  <  a* sqrt(K), certified rational")
log("=" * 78)
viol = []
for Kv in list(range(1, 401)) + [500, 600, 800, 1000, 1500, 2000, 3000]:
    q = Q_cache.get(Kv + 1) or Q_exact(Kv + 1)
    upper = q - sqrt_lo(PI_LO * (Kv + 1)) / 2
    if not (upper < astar_sqrtK_lower(Kv)):
        viol.append(Kv)
log(f"  407 points (dense K=1..400 + sparse to 3000): violations: "
    f"{viol if viol else 'NONE (certified)'}")
if viol: fails += 1

log("")
log("=" * 78)
log(f"PART-3 RESULT: {'ALL CHECKS PASSED (0 failures)' if fails == 0 else f'{fails} FAILURE GROUPS'}")
log("=" * 78)
with open(__file__.replace(".py", ".log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
sys.exit(0 if fails == 0 else 1)
