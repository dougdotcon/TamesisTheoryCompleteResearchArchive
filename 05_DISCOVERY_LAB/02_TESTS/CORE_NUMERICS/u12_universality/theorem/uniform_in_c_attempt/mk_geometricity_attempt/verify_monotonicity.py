"""
R2: verify the monotonicity claim underlying Route A step 2 of
DERIVATION_PREREG.md:

  (a) f_j(n) := n[prod_{i=1}^j (1+i/n) - 1] equals
      sum_{k=1}^j e_k(1,...,j) / n^{k-1}, e_k the elementary symmetric
      polynomials of {1,...,j} -- checked symbolically, exact.
  (b) every e_k(1,...,j) > 0 for k=1,...,j -- checked exactly for a range
      of j.
  (c) f_j(n) is therefore nonincreasing in n (constant for j<=1, strictly
      decreasing for j>=2) -- checked directly, exact Fraction arithmetic,
      by comparing f_j(n) and f_j(n+1) for a grid of (j,n).
  (d) consequently n(psi_n^{(K)}-phi_K), a nonnegative combination (weights
      C(2K+1,K-j) >= 0) of the f_j(n), is itself nonincreasing in n, with
      supremum over n>=K+1 attained AT n=K+1 -- checked directly, exact,
      for an exhaustive grid of (K,n).
  (e) as a byproduct: psi_n^{(K)} - phi_K >= 0 always (approaches the limit
      from above) -- checked directly.

All exact (fractions.Fraction / sympy.Rational). No randomness.
"""
import sympy as sp
from fractions import Fraction as Fr
from math import comb, factorial


# ---------- (a),(b): elementary symmetric polynomials, symbolic ----------
def elementary_symmetric(values, k):
    """Exact e_k(values) via the standard DP (all Fraction/int arithmetic)."""
    n = len(values)
    # dp[i][k] = e_k of first i values
    dp = [[Fr(0)] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = Fr(1)
    for i in range(1, n + 1):
        v = values[i - 1]
        for kk in range(1, k + 1):
            dp[i][kk] = dp[i - 1][kk] + v * dp[i - 1][kk - 1]
    return dp[n][k]


print("=== R2(a)/(b): f_j(n) = sum_k e_k(1..j)/n^{k-1}, e_k > 0 ===\n")
n_sym = sp.symbols('n')
all_pass = True
for j in range(0, 15):
    values = list(range(1, j + 1))
    prod = sp.prod([1 + sp.Integer(i) / n_sym for i in values]) if j > 0 else sp.Integer(1)
    f_j_direct = sp.simplify(n_sym * (prod - 1))
    # reconstruct via elementary symmetric polynomials
    f_j_ek = sp.Integer(0)
    ek_list = []
    for k in range(1, j + 1):
        ek = elementary_symmetric(values, k)
        ek_sp = sp.Rational(ek.numerator, ek.denominator)
        ek_list.append(ek_sp)
        f_j_ek += ek_sp / n_sym**(k - 1)
    match = sp.simplify(f_j_direct - f_j_ek) == 0
    all_positive = all(e > 0 for e in ek_list)
    all_pass = all_pass and match and (all_positive or j == 0)
    print(f"j={j:2d}: identity match={match}  all e_k>0: {all_positive if j > 0 else 'n/a (j=0)'}"
          f"  e_k={ek_list}")

print(f"\n(a)/(b) all pass: {all_pass}\n")

# ---------- (c): f_j(n) nonincreasing in n, exact, exhaustive grid ----------
def f_j_exact(j, n):
    """Exact f_j(n) = n*[prod_{i=1}^j (1+i/n) - 1], Fraction arithmetic."""
    n = Fr(n)
    prod = Fr(1)
    for i in range(1, j + 1):
        prod *= (1 + Fr(i, n))
    return n * (prod - 1)


print("=== R2(c): f_j(n) nonincreasing in n, exhaustive grid j=0..60, n=j+1..j+300 ===")
violations_c = 0
checked_c = 0
for j in range(0, 61):
    prev = None
    for n in range(max(1, j), j + 301):
        if n == 0:
            continue
        cur = f_j_exact(j, n)
        if prev is not None:
            checked_c += 1
            if cur > prev:  # should be nonincreasing: f_j(n) <= f_j(n-1)
                violations_c += 1
                print(f"  VIOLATION j={j} n={n}: f_j(n)={float(cur)} > f_j(n-1)={float(prev)}")
        prev = cur
print(f"checked {checked_c} consecutive pairs, violations={violations_c}\n")

# ---------- (d): n(psi_n^{(K)}-phi_K) nonincreasing in n, sup at n=K+1 -----
def phi_r(r):
    r = Fr(r)
    rr = int(r)
    return Fr(4**rr * factorial(rr)**2, factorial(2 * rr + 1))


def n_psi_minus_phi_exact(K, n):
    """Exact n*(psi_n^{(K)} - phi_K) via Corolario A1, Fraction arithmetic."""
    K = int(K)
    n = Fr(n)
    total = Fr(0)
    for j in range(0, K + 1):
        w = Fr(comb(2 * K + 1, K - j))
        prod = Fr(1)
        for i in range(1, j + 1):
            prod *= (1 + Fr(i) / n)
        total += w * n * (prod - 1)
    return phi_r(K) / Fr(4**K) * total


print("=== R2(d): n(psi_n^{(K)}-phi_K) nonincreasing in n, sup at n=K+1 ===")
print("(exhaustive grid K=1..40, n=K+1..K+200)")
violations_d = 0
checked_d = 0
neg_count = 0
argmax_ok = 0
for K in range(1, 41):
    vals = {}
    for n in range(K + 1, K + 201):
        v = n_psi_minus_phi_exact(K, n)
        vals[n] = v
        if v < 0:
            neg_count += 1
    ns = sorted(vals.keys())
    for i in range(1, len(ns)):
        checked_d += 1
        if vals[ns[i]] > vals[ns[i - 1]]:
            violations_d += 1
            print(f"  VIOLATION K={K} n={ns[i]}: {float(vals[ns[i]])} > n={ns[i-1]}: {float(vals[ns[i-1]])}")
    # argmax check
    best_n = max(vals, key=lambda k: vals[k])
    if best_n == K + 1:
        argmax_ok += 1
    else:
        print(f"  ARGMAX MISMATCH K={K}: argmax at n={best_n}, expected n={K+1}")
print(f"checked {checked_d} consecutive pairs, violations={violations_d}, "
      f"negative values seen={neg_count}, argmax-at-(K+1) count={argmax_ok}/40\n")

print(f"=== ALL R2 CHECKS PASS: "
      f"{all_pass and violations_c == 0 and violations_d == 0 and neg_count == 0 and argmax_ok == 40} ===")
