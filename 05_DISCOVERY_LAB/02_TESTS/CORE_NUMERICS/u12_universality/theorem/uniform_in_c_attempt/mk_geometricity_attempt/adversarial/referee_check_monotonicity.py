"""
REFEREE independent check 2 -- Section 2.2's monotonicity argument, the
single most load-bearing step per the target document's own Section 6 flag.

Written from scratch. Claims under test:

  (A) g(j;n) := prod_{i=1}^j (1+i/n) expands as sum_{k=0}^j e_k(1..j) n^{-k},
      e_k the k-th elementary symmetric polynomial of {1,...,j}, e_0=1.
  (B) f_j(n) := n[g(j;n)-1] = sum_{k=1}^j e_k(1..j) n^{1-k}
              = e_1(j) + e_2(j)/n + e_3(j)/n^2 + ...
  (C) every e_k(1,...,j) > 0 for 1<=k<=j.
  (D) f_j(n) is nonincreasing in n (strictly decreasing for j>=2, constant
      for j=0,1), and f_j(n) >= 0 for all n>0, j>=0.
  (E) n(psi_n^{(K)}-phi_K) = (phi_K/4^K) * sum_j C(2K+1,K-j) f_j(n) is
      therefore nonincreasing in n (nonnegative-weighted sum of nonincreasing
      nonnegative functions) and its sup over n>=K+1 is attained at n=K+1.

Part 1 (exact integer/Fraction arithmetic, no sympy symbolic expansion --
that route was tried first and was too slow past j~10 due to sympy's
generic simplify/expand overhead; this is an independent, faster, equally
exact re-implementation): verify (A)/(B)/(C) for j up to 200, using a
from-scratch O(j^2) elementary-symmetric-polynomial computation plus
exact rational-point evaluation (more sample points than unknown
coefficients, which suffices to certify a bounded-degree rational identity).
Part 2 (exact Fraction arithmetic, exhaustive grid): verify (D) directly on
f_j(n) for j=0..100, n=j+1..j+500 -- well beyond the target's own tested
range (j up to 60, n up to j+300).
Part 3 (exact Fraction arithmetic, exhaustive grid): verify (E) -- the
monotonicity AND the argmax location -- for K=1..70, n=K+1..K+350, again
beyond the target's tested range (K up to 40, n up to K+200).
"""
from fractions import Fraction
from math import comb, factorial

# ---------------------------------------------------------------------
# Part 1: check of (A), (B), (C) -- exact arithmetic, no slow symbolic
# expansion. Elementary symmetric polynomials e_k(1,...,j) are computed
# by the textbook O(j^2) DP (multiply out (x+1)(x+2)...(x+j) one factor
# at a time, tracking exact integer coefficients) -- this is itself an
# INDEPENDENT, from-scratch computation of e_k, not sympy's built-in
# symmetric_poly. Positivity is then checked directly on these integers.
# The decomposition claim g(j;n) = sum_k e_k(1..j) n^{-k} is a rational
# function identity of "degree" j in 1/n; we certify it by evaluating
# BOTH sides at j+5 distinct exact rational points n=j+1,...,2j+5 (more
# points than the j+1 unknown coefficients of a degree-j polynomial in
# 1/n), which suffices to prove the polynomial identity exactly (a
# nonzero polynomial of degree <= j cannot vanish at more than j points).
# ---------------------------------------------------------------------
print("=== Part 1: exact decomposition + positivity, j=0..200 ===")


def elementary_symmetric(xs):
    """e_0,...,e_len(xs) of the list xs, via (x+x_1)(x+x_2)...(x+x_m)
    expanded by repeated multiplication, exact integers."""
    coeffs = [1]  # coeffs[k] = e_k so far, coeffs = poly in x with e_k as
    # the coefficient of x^{m-k} in prod(x+x_i); build iteratively.
    for x_i in xs:
        new_coeffs = [0] * (len(coeffs) + 1)
        for k, c in enumerate(coeffs):
            new_coeffs[k] += c          # x^{...} * x  -> shifts (handled by index)
            new_coeffs[k + 1] += c * x_i  # contributes to e_{k+1}
        coeffs = new_coeffs
    return coeffs  # coeffs[k] = e_k(xs), k=0..len(xs)


part1_ok = True
J_TEST = 200
for j in [0, 1, 2, 3, 4, 5, 6, 10, 15, 20, 30, 40, 60, 80, 120, 150, 200]:
    xs = list(range(1, j + 1))
    e = elementary_symmetric(xs)
    assert len(e) == j + 1

    e0_ok = (e[0] == 1)
    positivity_ok = all(e[k] > 0 for k in range(1, j + 1))

    # decomposition check at several exact rational sample points
    decomposition_ok = True
    n_samples = list(range(j + 1, j + 1 + (j + 6)))  # j+6 sample points > j+1 unknowns
    for n_val in n_samples:
        n_frac = Fraction(n_val)
        prod = Fraction(1)
        for i in range(1, j + 1):
            prod *= (1 + Fraction(i, 1) / n_frac)
        predicted = sum(Fraction(e[k]) * n_frac**(-k) for k in range(0, j + 1))
        if prod != predicted:
            decomposition_ok = False
            print(f"  DECOMPOSITION MISMATCH: j={j}, n={n_val}: "
                  f"direct={prod}, predicted={predicted}")

    ok = decomposition_ok and positivity_ok and e0_ok
    part1_ok &= ok
    print(f"j={j}: decomposition (checked at {len(n_samples)} pts) "
          f"{'OK' if decomposition_ok else 'FAIL'}, "
          f"e_0=1 {'OK' if e0_ok else 'FAIL'}, "
          f"e_k>0 for k=1..j {'OK' if positivity_ok else 'FAIL'}")
print(f"Part 1 result: {'ALL PASS' if part1_ok else 'FAILURE DETECTED'}")
print()

# ---------------------------------------------------------------------
# Part 2: exact Fraction grid on f_j(n) monotonicity, j=0..80, n=j+1..j+500
# ---------------------------------------------------------------------
print("=== Part 2: exact f_j(n) nonincreasing-in-n grid, j=0..80, n=j+1..j+500 ===")


def f_j(j, n):
    """f_j(n) = n[prod_{i=1}^j(1+i/n) - 1], exact Fraction, computed directly
    from the *definition* (product form), NOT via the elementary-symmetric
    decomposition being tested -- an independent computational route."""
    n = Fraction(n)
    prod = Fraction(1)
    for i in range(1, j + 1):
        prod *= (1 + Fraction(i, 1) / n)
    return n * (prod - 1)


violations_mono = 0
violations_neg = 0
pairs_checked = 0
J_MAX = 100
N_EXTRA = 500
for j in range(0, J_MAX + 1):
    prev = None
    for n in range(j + 1, j + 1 + N_EXTRA):
        val = f_j(j, n)
        if val < 0:
            violations_neg += 1
            print(f"  NEGATIVE VALUE: j={j}, n={n}, f_j(n)={val}")
        if prev is not None:
            pairs_checked += 1
            if val > prev:  # should be nonincreasing: f_j(n) <= f_j(n-1)
                violations_mono += 1
                print(f"  MONOTONICITY VIOLATION: j={j}, n={n-1}->{n}, "
                      f"f_j({n-1})={prev}, f_j({n})={val}")
        prev = val

print(f"Pairs checked: {pairs_checked}")
print(f"Monotonicity violations: {violations_mono}")
print(f"Negative-value occurrences: {violations_neg}")
print()

# ---------------------------------------------------------------------
# Part 3: exact Fraction grid on n(psi_n^{(K)}-phi_K), K=1..80, n=K+1..K+400
# argmax must be at n=K+1; also nonnegative and nonincreasing throughout.
# ---------------------------------------------------------------------
print("=== Part 3: n(psi_n^{(K)}-phi_K) monotonicity + argmax, K=1..70, n=K+1..K+350 ===")


def phi_frac(K):
    return Fraction(4**K * factorial(K)**2, factorial(2 * K + 1))


def n_psi_minus_phi(K, n):
    """n(psi_n^{(K)} - phi_K), computed DIRECTLY from Corolario A1's closed
    form (independent of the f_j(n) route above -- this exercises the whole
    chain end to end)."""
    phiK = phi_frac(K)
    s = Fraction(0)
    for j in range(0, K + 1):
        c = comb(2 * K + 1, K - j)
        prod = Fraction(1)
        for i in range(1, j + 1):
            prod *= Fraction(n + i, n)
        s += c * prod
    psi_n_K = phiK * s / Fraction(4**K)
    return n * (psi_n_K - phiK)


K_MAX = 70
N_EXTRA_K = 350
violations_mono_K = 0
violations_neg_K = 0
argmax_wrong = 0
pairs_checked_K = 0
for K in range(1, K_MAX + 1):
    values = {}
    prev = None
    for n in range(K + 1, K + 1 + N_EXTRA_K):
        val = n_psi_minus_phi(K, n)
        values[n] = val
        if val < 0:
            violations_neg_K += 1
            print(f"  NEGATIVE: K={K}, n={n}, value={val}")
        if prev is not None:
            pairs_checked_K += 1
            if val > prev:
                violations_mono_K += 1
                print(f"  MONOTONICITY VIOLATION: K={K}, n={n-1}->{n}: {prev} -> {val}")
        prev = val
    # argmax check
    max_n = max(values, key=lambda k: values[k])
    if max_n != K + 1:
        argmax_wrong += 1
        print(f"  ARGMAX WRONG: K={K}, argmax at n={max_n}, not n=K+1={K+1}")

print(f"K range tested: 1..{K_MAX}, n range per K: K+1..K+{N_EXTRA_K}")
print(f"Pairs checked: {pairs_checked_K}")
print(f"Monotonicity violations: {violations_mono_K}")
print(f"Negative-value occurrences: {violations_neg_K}")
print(f"Argmax-not-at-K+1 occurrences: {argmax_wrong} (out of {K_MAX} tested K)")
print()

overall = (part1_ok and violations_mono == 0 and violations_neg == 0
           and violations_mono_K == 0 and violations_neg_K == 0 and argmax_wrong == 0)
print(f"OVERALL: {'ALL CHECKS PASS' if overall else 'FAILURE DETECTED'}")
