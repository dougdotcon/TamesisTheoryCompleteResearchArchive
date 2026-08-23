"""
REFEREE independent check 3 -- Section 2.3's crude geometric bound.

Written from scratch. Claims under test:

  (i) The exact identity sum_{i=0}^{K} C(2K+1,i) = 2^{2K}, for every K>=0
      (the "odd-N half-sum identity"). We verify it two ways: (a) direct
      exact computation for K=0..400; (b) an independent symbolic proof
      via the binomial theorem at x=1 plus the involution i -> 2K+1-i on
      {0,...,2K+1} (which is fixed-point-free since 2K+1 is odd, splitting
      the full sum 2^{2K+1} into two equal halves).

  (ii) At n=K+1: for 0<=j<=K, g(j;K+1) <= exp(K/2), using 1+x<=e^x termwise
       and j(j+1) <= K(K+1) for j<=K. Hence M_K^psi <= phi_K (K+1) e^{K/2}.
       We check this bound holds against the EXACT value of M_K^psi
       (computed independently, via Corolario A1's closed form, exact
       Fraction arithmetic) for a wide range of K.

mpmath at high precision is used only for evaluating the irrational
quantity e^{K/2} and phi_K*(K+1)*e^{K/2}; M_K^psi itself is always computed
first as an exact Fraction and only converted to mpmath for the final
comparison.
"""
import sympy as sp
from fractions import Fraction
from math import comb, factorial
import mpmath as mp

mp.mp.dps = 80

print("=== (i)(a) sum_{i=0}^K C(2K+1,i) = 2^{2K}, exact, K=0..400 ===")
viol = 0
for K in range(0, 401):
    lhs = sum(comb(2 * K + 1, i) for i in range(0, K + 1))
    rhs = 2**(2 * K)
    if lhs != rhs:
        viol += 1
        print(f"  MISMATCH at K={K}: lhs={lhs}, rhs={rhs}")
print(f"K=0..400: {viol} violations")
print()

print("=== (i)(b) independent symbolic proof of the identity ===")
K = sp.symbols('K', nonnegative=True, integer=True)
# Binomial theorem at x=1: sum_{i=0}^{2K+1} C(2K+1,i) = 2^{2K+1}.
# Involution i -> 2K+1-i on {0,...,2K+1}: fixed point would need i=2K+1-i,
# i.e. 2i=2K+1, impossible for integer i since 2K+1 is odd. So the
# involution is fixed-point-free, pairing i in {0,...,K} bijectively with
# 2K+1-i in {K+1,...,2K+1} (since i<=K  <=>  2K+1-i>=K+1). Also
# C(2K+1,i) = C(2K+1,2K+1-i) (symmetry of binomial coefficients). Hence
# sum_{i=0}^{K} C(2K+1,i) = sum_{i=K+1}^{2K+1} C(2K+1,i), and the two halves
# sum to 2^{2K+1}, so each half is 2^{2K}.
# Check the bijection claim symbolically/exactly for many K, and the
# binomial symmetry, from scratch:
sym_ok = True
for Kval in range(0, 60):
    N = 2 * Kval + 1
    # involution has no fixed point in {0,...,N}
    fixed_points = [i for i in range(0, N + 1) if i == N - i]
    if fixed_points:
        sym_ok = False
        print(f"  Involution has a fixed point at K={Kval}: {fixed_points}")
    # bijection {0..K} <-> {K+1..2K+1} via i -> N-i
    lower = set(range(0, Kval + 1))
    upper = set(range(Kval + 1, N + 1))
    mapped = set(N - i for i in lower)
    if mapped != upper:
        sym_ok = False
        print(f"  Bijection fails at K={Kval}")
    # binomial symmetry C(N,i) = C(N,N-i)
    for i in range(0, N + 1):
        if comb(N, i) != comb(N, N - i):
            sym_ok = False
            print(f"  Binomial symmetry fails at K={Kval}, i={i}")
    # full sum = 2^{2K+1}
    full = sum(comb(N, i) for i in range(0, N + 1))
    if full != 2**N:
        sym_ok = False
        print(f"  Full binomial sum wrong at K={Kval}")
print(f"Involution fixed-point-free, bijection, binomial symmetry, full-sum=2^{{2K+1}}: "
      f"{'ALL OK, K=0..59' if sym_ok else 'FAILURE'}")
print("Conclusion: sum_{i=0}^K C(2K+1,i) = (1/2)*2^{2K+1} = 2^{2K}, confirmed both numerically and structurally.")
print()

print("=== (ii) M_K^psi <= phi_K (K+1) e^{K/2}, exact M_K^psi vs mpmath bound ===")


def phi_frac(Kv):
    return Fraction(4**Kv * factorial(Kv)**2, factorial(2 * Kv + 1))


def M_K_psi_exact(Kv):
    """M_K^psi = (K+1)(psi_{K+1}^{(K)} - phi_K), exact Fraction, via
    Corolario A1's closed form at n=K+1 -- independent re-implementation."""
    n = Kv + 1
    phiK = phi_frac(Kv)
    s = Fraction(0)
    for j in range(0, Kv + 1):
        c = comb(2 * Kv + 1, Kv - j)
        prod = Fraction(1)
        for i in range(1, j + 1):
            prod *= Fraction(n + i, n)
        s += c * prod
    psi_val = phiK * s / Fraction(4**Kv)
    return n * (psi_val - phiK)


viol_bound = 0
worst_ratio = None
K_LIST = list(range(1, 401))
for Kv in K_LIST:
    exact_val = M_K_psi_exact(Kv)
    exact_mp = mp.mpf(exact_val.numerator) / mp.mpf(exact_val.denominator)
    phiK = phi_frac(Kv)
    phiK_mp = mp.mpf(phiK.numerator) / mp.mpf(phiK.denominator)
    bound_mp = phiK_mp * (Kv + 1) * mp.e**(mp.mpf(Kv) / 2)
    if exact_mp > bound_mp:
        viol_bound += 1
        print(f"  BOUND VIOLATED at K={Kv}: M_K^psi={exact_mp}, bound={bound_mp}")
    ratio = exact_mp / bound_mp
    if worst_ratio is None or ratio > worst_ratio[0]:
        worst_ratio = (ratio, Kv)

print(f"K=1..400: {viol_bound} bound violations")
print(f"Tightest ratio M_K^psi/bound observed: {worst_ratio[0]} at K={worst_ratio[1]} "
      f"(should be << 1, confirming the bound is valid but crude)")
print()

# Additional independent sanity check: also test the crude termwise
# inequality 1+x <= e^x directly, and the claim j(j+1)<=K(K+1) for j<=K
print("=== (ii) sanity: termwise 1+x<=e^x and j(j+1)<=K(K+1) for 0<=j<=K ===")
tw_viol = 0
for Kv in range(0, 200):
    for j in range(0, Kv + 1):
        if j * (j + 1) > Kv * (Kv + 1):
            tw_viol += 1
            print(f"  j(j+1)<=K(K+1) FAILS: K={Kv}, j={j}")
# 1+x <= e^x is a textbook fact; spot-check numerically at high precision
import random
random.seed(0)
e_x_viol = 0
for _ in range(2000):
    x = mp.mpf(random.uniform(0, 50))
    if 1 + x > mp.e**x:
        e_x_viol += 1
print(f"j(j+1)<=K(K+1) violations (K=0..199): {tw_viol}")
print(f"1+x<=e^x spot-check violations (2000 random x in [0,50]): {e_x_viol}")
print()

overall = (viol == 0 and sym_ok and viol_bound == 0 and tw_viol == 0 and e_x_viol == 0)
print(f"OVERALL: {'ALL CHECKS PASS' if overall else 'FAILURE DETECTED'}")
