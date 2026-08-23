"""
Independent re-derivation/re-verification of Theorem 6's assembly, from
scratch. Does NOT read the target's own verify_limit.py.

Re-derives, symbolically (sympy) and then numerically (mpmath / exact
Fraction), the algebra chain:

  M_K = Q(K+1) - (K+1) phi_K                                   [Theorem 3, cited]
  Q(K+1) >= sqrt(pi(K+1)/2) - 6                                 [Theorem 5]
  phi_K < sqrt(pi)/(2 sqrt(K))                                  [Lemma 4.1 v_K bound, cited]
  =>  M_K > sqrt(pi(K+1)/2) - 6 - sqrt(pi)/(2 sqrt(K)) * (K+1)
  sqrt(pi(K+1)/2) >= sqrt(pi/2)*sqrt(K)                          [trivial, K+1>=K]
  sqrt(pi)/(2 sqrt(K)) * (K+1) = (sqrt(pi)/2)*(sqrt(K) + 1/sqrt(K))
  =>  M_K > a*sqrt(K) - (sqrt(pi)/2)/sqrt(K) - 6
  =>  M_K/sqrt(K) > a* - (sqrt(pi)/2)/K - 6/sqrt(K)   -> a* as K -> oo

Also verifies the a*-identity a* = sqrt(pi/2) - sqrt(pi)/2 = sqrt(pi)(1/sqrt2-1/2)
and the upper bound (Observation 0, cited from parent's Theorem 4 proof):
  M_K < 1 + a*sqrt(K+1)   =>   M_K/sqrt(K) < 1/sqrt(K) + a*sqrt((K+1)/K) -> a*

then the two-sided squeeze at large scale using an independent phi_K and
Q(K+1) computation (exact Fraction for moderate K, fast mpmath log-gamma /
incremental-log-sum for K up to 10^6).
"""
import sympy as sp
import mpmath as mp
from fractions import Fraction as F

mp.mp.dps = 60

print("############################################")
print("# Part A: a* identity                       #")
print("############################################")
astar_def1 = sp.sqrt(sp.pi)*(1/sp.sqrt(2) - sp.Rational(1,2))
astar_def2 = sp.sqrt(sp.pi/2) - sp.sqrt(sp.pi)/2
print("sqrt(pi)(1/sqrt2-1/2) - [sqrt(pi/2)-sqrt(pi)/2] simplifies to:",
      sp.simplify(astar_def1 - astar_def2), "(expect 0)")
print("a* =", sp.N(astar_def1, 30))

print()
print("############################################")
print("# Part B: symbolic algebra of the lower-bound chain")
print("############################################")
K = sp.symbols('K', positive=True)
sqrt_pi = sp.sqrt(sp.pi)
astar = sqrt_pi*(1/sp.sqrt(2) - sp.Rational(1,2))

# (sqrt(pi)/(2 sqrt(K)))*(K+1) =?= (sqrt(pi)/2)*(sqrt(K)+1/sqrt(K))
lhs1 = (sqrt_pi/(2*sp.sqrt(K)))*(K+1)
rhs1 = (sqrt_pi/2)*(sp.sqrt(K) + 1/sp.sqrt(K))
print("(sqrt(pi)/(2sqrt(K)))(K+1) - (sqrt(pi)/2)(sqrt(K)+1/sqrt(K)) simplifies to:",
      sp.simplify(lhs1 - rhs1), "(expect 0)")

# sqrt(pi(K+1)/2) - sqrt(pi/2)*sqrt(K) >= 0  for K>=... (trivial since K+1>=K)
diff_trivial = sp.sqrt(sp.pi*(K+1)/2) - sp.sqrt(sp.pi/2)*sp.sqrt(K)
print("sqrt(pi(K+1)/2) - sqrt(pi/2)*sqrt(K), evaluated at K=1,5,100:",
      [sp.N(diff_trivial.subs(K, v)) for v in [1,5,100]], "(expect all >=0)")

# assemble: sqrt(pi(K+1)/2) - 6 - (sqrt(pi)/(2sqrt(K)))(K+1)
#        >= sqrt(pi/2)*sqrt(K) - 6 - (sqrt(pi)/2)(sqrt(K)+1/sqrt(K))
#         = [sqrt(pi/2)-sqrt(pi)/2]*sqrt(K) - (sqrt(pi)/2)/sqrt(K) - 6
#         = a*sqrt(K) - (sqrt(pi)/2)/sqrt(K) - 6
final_claim_lhs = sp.sqrt(sp.pi/2)*sp.sqrt(K) - (sqrt_pi/2)*(sp.sqrt(K)+1/sp.sqrt(K))
final_claim_rhs = astar*sp.sqrt(K) - (sqrt_pi/2)/sp.sqrt(K)
print("[sqrt(pi/2)sqrt(K) - (sqrt(pi)/2)(sqrt(K)+1/sqrt(K))] - [a*sqrt(K)-(sqrt(pi)/2)/sqrt(K)] simplifies to:",
      sp.simplify(final_claim_lhs - final_claim_rhs), "(expect 0)")

# dividing by sqrt(K): a*sqrt(K)/sqrt(K) - [(sqrt(pi)/2)/sqrt(K)]/sqrt(K) - 6/sqrt(K)
#   =?= a* - (sqrt(pi)/2)/K - 6/sqrt(K)
div_lhs = (astar*sp.sqrt(K) - (sqrt_pi/2)/sp.sqrt(K) - 6) / sp.sqrt(K)
div_rhs = astar - (sqrt_pi/2)/K - 6/sp.sqrt(K)
print("[a*sqrt(K)-(sqrt(pi)/2)/sqrt(K)-6]/sqrt(K) - [a*-(sqrt(pi)/2)/K-6/sqrt(K)] simplifies to:",
      sp.simplify(div_lhs - div_rhs), "(expect 0)")

print()
print("############################################")
print("# Part C: Observation 0 upper-bound algebra (cited from parent)")
print("############################################")
# M_K < 1 + a*sqrt(K+1)  =>  M_K/sqrt(K) < 1/sqrt(K) + a*sqrt((K+1)/K)
up_lhs = (1 + astar*sp.sqrt(K+1))/sp.sqrt(K)
up_rhs = 1/sp.sqrt(K) + astar*sp.sqrt((K+1)/K)
print("(1+a*sqrt(K+1))/sqrt(K) - [1/sqrt(K)+a*sqrt((K+1)/K)] simplifies to:",
      sp.simplify(up_lhs - up_rhs), "(expect 0)")
# limit as K->oo
lim_up = sp.limit(up_rhs, K, sp.oo)
print("limit of 1/sqrt(K)+a*sqrt((K+1)/K) as K->oo:", lim_up, " (expect a* =", sp.N(astar,10), ")")
lim_lo = sp.limit(div_rhs, K, sp.oo)
print("limit of a*-(sqrt(pi)/2)/K-6/sqrt(K) as K->oo:", lim_lo, " (expect a* =", sp.N(astar,10), ")")

print()
print("############################################")
print("# Part D: numerical two-sided squeeze, independent phi_K/Q(K+1)")
print("############################################")

def phi_K_mp(K):
    # phi_K = 4^K (K!)^2/(2K+1)!  via log-gamma to avoid huge factorials
    K = mp.mpf(K)
    log_phi = K*mp.log(4) + 2*mp.loggamma(K+1) - mp.loggamma(2*K+2)
    return mp.e**log_phi

def Q_mp_incremental(n):
    # Q(n) = sum_{j=0}^{n-1} P_j, P_j computed incrementally via log-sum
    # (avoids O(n) per-term product recomputation; O(n) total mpmath ops)
    n_mp = mp.mpf(n)
    total = mp.mpf(1)  # j=0 term, P_0=1
    log_p = mp.mpf(0)
    for i in range(1, n):
        log_p += mp.log(1 - mp.mpf(i)/n_mp)
        total += mp.e**log_p
    return total

astar_mp = mp.sqrt(mp.pi)*(1/mp.sqrt(2) - mp.mpf(1)/2)
print("a* (mpmath) =", astar_mp)

def check_squeeze(K, Q_Kp1, phiK):
    K_mp = mp.mpf(K)
    MK = Q_Kp1 - (K+1)*phiK
    rK = MK/mp.sqrt(K_mp)
    lower = astar_mp - (mp.sqrt(mp.pi)/2)/K_mp - 6/mp.sqrt(K_mp)
    upper = astar_mp + 1/mp.sqrt(K_mp) + astar_mp*(1/(2*K_mp))  # sqrt(1+1/K)<=1+1/(2K)
    return MK, rK, lower, upper

print("\n--- exact Fraction M_K, K up to 2000 (dense-ish sample), cross-checked vs mpmath ---")
def Q_exact_frac(n):
    total = F(1)
    p = F(1)
    for i in range(1, n):
        p *= F(n - i, n)
        total += p
    return total

def phi_K_exact(K):
    # phi_K = 4^K (K!)^2/(2K+1)!
    from math import factorial
    return F(4**K * factorial(K)**2, factorial(2*K+1))

bad = 0
worst_lo = None
worst_hi = None
test_Ks = list(range(1, 60)) + [80,120,200,400,800,1500,2000]
for K in test_Ks:
    Qk1 = Q_exact_frac(K+1)
    phiK = phi_K_exact(K)
    MK = Qk1 - (K+1)*phiK
    MK_mp = mp.mpf(MK.numerator)/mp.mpf(MK.denominator)
    K_mp = mp.mpf(K)
    rK = MK_mp/mp.sqrt(K_mp)
    lower = astar_mp - (mp.sqrt(mp.pi)/2)/K_mp - 6/mp.sqrt(K_mp)
    upper = astar_mp + 1/mp.sqrt(K_mp) + astar_mp/(2*K_mp)
    ok_lo = rK > lower - mp.mpf('1e-40')  # note: for small K, lower can be very negative -> trivial
    ok_hi = rK < upper + mp.mpf('1e-40')
    if not ok_lo or not ok_hi:
        bad += 1
        print(f"VIOLATION at K={K}: rK={rK} lower={lower} upper={upper}")
    m_lo = rK - lower
    m_hi = upper - rK
    if worst_lo is None or m_lo < worst_lo[0]:
        worst_lo = (m_lo, K)
    if worst_hi is None or m_hi < worst_hi[0]:
        worst_hi = (m_hi, K)
print(f"checked {len(test_Ks)} K values exactly, violations={bad}")
print(f"worst (smallest) margin rK-lower = {worst_lo}")
print(f"worst (smallest) margin upper-rK = {worst_hi}")
print(f"rK at largest tested K={test_Ks[-1]}: {rK}  (a*={astar_mp})")

print("\n--- fast mpmath (log-gamma / incremental log-sum), K up to 200000, sparse ---")
bad2 = 0
sparse_Ks = [1,10,100,1000,5000,10000,30000,50000,80000,100000,150000,200000]
for K in sparse_Ks:
    phiK = phi_K_mp(K)
    Qk1 = Q_mp_incremental(K+1)
    MK, rK, lower, upper = check_squeeze(K, Qk1, phiK)
    ok = (rK > lower - mp.mpf('1e-30')) and (rK < upper + mp.mpf('1e-30'))
    if not ok:
        bad2 += 1
        print(f"VIOLATION at K={K}: rK={rK} lower={lower} upper={upper}")
    print(f"  K={K}: rK={float(rK):.8f}  lower={float(lower):.8f}  upper={float(upper):.8f}  gap(a*-rK)={float(astar_mp-rK):.8f}")
print(f"violations={bad2}")
