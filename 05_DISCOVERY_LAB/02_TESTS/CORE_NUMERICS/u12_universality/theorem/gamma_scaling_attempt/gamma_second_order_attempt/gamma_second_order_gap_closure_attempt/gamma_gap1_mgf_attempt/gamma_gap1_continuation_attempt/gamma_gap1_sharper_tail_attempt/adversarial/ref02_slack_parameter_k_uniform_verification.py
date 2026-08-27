"""
REFEREE script 02 -- independent re-derivation and verification of the
"slack-parameter" construction (target ATTEMPT.md section 3) that makes
the Bernstein tail bound k-uniform.

Claim under test:
  Fix a>0. If (2/3)*M*Theta_k <= a*k*sigma^2 then the Bernstein denominator
  2*k*sigma^2 + (2/3)*M*Theta_k <= (2+a)*k*sigma^2, giving

      P(|D|>Theta_k) <= 2*exp(-C^2*ln(n)/((2+a)*sigma^2)) = 2*n^{-C^2/((2+a)*sigma^2)}

  -- exactly k-independent -- valid for all k >= k_2(n,gamma,C,a) :=
  (2*M*C/(3*a*sigma^2))^2 * ln(n).

This script independently re-derives the k_2 formula by hand-algebra (shown
in the docstring below and cross-checked symbolically with sympy), then
verifies numerically:

  Part A: the sufficient condition (2/3)*M*Theta_k <= a*k*sigma^2 holds for
          k >= k_2, fails (generically) for k somewhat below k_2 -- confirming
          k_2 is the right threshold, not just *a* sufficient one far off.
  Part B: the resulting clean bound 2*n^{-C^2/((2+a)*sigma^2)} is never
          violated by the EXACT Binomial tail probability at k just above k_2.
  Part C: symbolic sympy re-derivation of k_2 from the sufficient condition,
          confirming algebraically (not just numerically) that the claimed
          closed form is the exact solution of the inequality for k.

Hand derivation of k_2 (own work, not copied):
  Theta_k = C*sqrt(k*ln n).  Condition:
      (2/3) M * C * sqrt(k ln n)  <=  a k sigma^2
  Divide both sides by sqrt(k) (k>0):
      (2/3) M C sqrt(ln n)  <=  a sigma^2 sqrt(k)
      sqrt(k)  >=  (2 M C sqrt(ln n)) / (3 a sigma^2)
      k  >=  (2 M C / (3 a sigma^2))^2 * ln n     =: k_2(n,gamma,C,a).
This matches the target's claimed k_2 exactly.

No .py file of this front or its lineage was read. Own code, own variable
names. No randomness drawn (deterministic grids + exact symbolic algebra).
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 50


def sigma2_of(gamma):
    return gamma * (1 - gamma)


def M_of(gamma):
    return max(gamma, 1 - gamma)


def theta(k, C, n):
    return C * mp.sqrt(mp.mpf(k) * mp.log(n))


def k2_formula(n, gamma, C, a):
    sigma2 = sigma2_of(gamma)
    M = M_of(gamma)
    return (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)


def sufficient_condition_holds(k, n, gamma, C, a):
    """(2/3) M Theta_k <= a k sigma^2 ?"""
    sigma2 = sigma2_of(gamma)
    M = M_of(gamma)
    lhs = mp.mpf(2) / 3 * M * theta(k, C, n)
    rhs = a * k * sigma2
    return lhs <= rhs, lhs, rhs


def clean_bound(n, gamma, C, a):
    sigma2 = sigma2_of(gamma)
    exponent = -(C * C) / ((2 + a) * sigma2)
    return 2 * n ** exponent


def exact_binomial_tail(k, gamma, t):
    k_int = int(k)
    gamma = mp.mpf(gamma)
    t = mp.mpf(t)
    total = mp.mpf(0)
    for m in range(0, k_int + 1):
        d = mp.mpf(m) - gamma * k_int
        if abs(d) > t:
            pmf = mp.binomial(k_int, m) * gamma ** m * (1 - gamma) ** (k_int - m)
            total += pmf
    return total


def check_part_a():
    print("=== Part A: sufficient condition holds for k>=k_2, threshold is tight ===")
    ns = [mp.mpf(x) for x in [50, 200, 1000, 10000, 1e6]]
    gammas = [mp.mpf(x) for x in ['0.01', '0.1', '0.3', '0.5', '0.7', '0.9', '0.99']]
    Cs = [mp.mpf(x) for x in ['1.0', '2.0', '5.0', '10.0']]
    a_s = [mp.mpf(x) for x in ['0.05', '0.5', '1.0']]
    total_checks = 0
    failures_at_or_above_k2 = 0
    holds_just_below = 0
    tested_below = 0
    for n in ns:
        for gamma in gammas:
            for C in Cs:
                for a in a_s:
                    k2 = k2_formula(n, gamma, C, a)
                    k2_ceil = int(mp.ceil(k2))
                    if k2_ceil < 1:
                        k2_ceil = 1
                    # check just at and above k2
                    for k in [k2_ceil, k2_ceil + 1, k2_ceil + 10, k2_ceil * 2]:
                        total_checks += 1
                        holds, lhs, rhs = sufficient_condition_holds(k, n, gamma, C, a)
                        if not holds:
                            failures_at_or_above_k2 += 1
                            print(f"  FAIL (should hold) n={n} gamma={gamma} C={C} a={a} "
                                  f"k={k} k2={float(k2):.3f} lhs={lhs} rhs={rhs}")
                    # check somewhat below k2 -- expect it to generically fail
                    # (confirming k2 is genuinely load-bearing, not slack)
                    k_below = int(mp.floor(k2 * mp.mpf('0.5')))
                    if k_below >= 1:
                        tested_below += 1
                        holds, lhs, rhs = sufficient_condition_holds(k_below, n, gamma, C, a)
                        if holds:
                            holds_just_below += 1
    print(f"  checks at/above k2 (must all hold): {total_checks}, failures: {failures_at_or_above_k2}")
    print(f"  checks at k2/2 (expected to generically FAIL the sufficient cond.): "
          f"{tested_below}, still held: {holds_just_below} "
          f"(nonzero here is fine -- it only shows k2 is not perfectly tight at every "
          f"corner, not that the k>=k2 direction is wrong)")
    return failures_at_or_above_k2 == 0


def check_part_b():
    print()
    print("=== Part B: clean k-uniform bound vs EXACT Binomial tail, k just above k_2 ===")
    # moderate n so exact pmf summation is tractable
    ns = [mp.mpf(x) for x in [80, 300, 1200, 5000]]
    gammas = [mp.mpf(x) for x in ['0.1', '0.3', '0.5', '0.7', '0.9']]
    Cs = [mp.mpf(x) for x in ['1.0', '2.0']]
    a_s = [mp.mpf(x) for x in ['0.1', '0.5']]
    checks = 0
    violations = 0
    for n in ns:
        for gamma in gammas:
            for C in Cs:
                for a in a_s:
                    k2 = k2_formula(n, gamma, C, a)
                    k = int(mp.ceil(k2)) + 2
                    if k > int(n) or k < 1:
                        continue
                    checks += 1
                    t = theta(k, C, n)
                    exact = exact_binomial_tail(k, gamma, t)
                    bound = clean_bound(n, gamma, C, a)
                    if exact > bound:
                        violations += 1
                        print(f"  VIOLATION n={n} gamma={gamma} C={C} a={a} k={k}: "
                              f"exact={exact} > bound={bound}")
    print(f"  checks performed: {checks}, violations: {violations}")
    return violations == 0


def check_part_c_symbolic():
    print()
    print("=== Part C: symbolic re-derivation of k_2 (sympy, exact algebra) ===")
    k, n, C, a, sig2, M = sp.symbols('k n C a sig2 M', positive=True)
    lnn = sp.symbols('lnn', positive=True)  # stand-in for ln(n)
    theta_k = C * sp.sqrt(k * lnn)
    lhs = sp.Rational(2, 3) * M * theta_k
    rhs = a * k * sig2
    # Solve lhs = rhs for k (equality, boundary of the sufficient condition)
    eq = sp.Eq(lhs, rhs)
    sol = sp.solve(eq, k)
    print(f"  sympy solve((2/3)*M*C*sqrt(k*lnn) = a*k*sig2, k) -> {sol}")
    claimed_k2 = (2 * M * C / (3 * a * sig2)) ** 2 * lnn
    print(f"  claimed k2 formula: {claimed_k2}")
    match = False
    for s in sol:
        diff = sp.simplify(s - claimed_k2)
        print(f"    candidate root {s}: difference from claimed k2 = {diff}")
        if diff == 0:
            match = True
    print(f"  symbolic match: {'PASS' if match else 'FAIL'}")
    return match


if __name__ == "__main__":
    ok_a = check_part_a()
    ok_b = check_part_b()
    ok_c = check_part_c_symbolic()
    print()
    print("=== SUMMARY ===")
    print(f"Part A (sufficient condition holds at/above k2): {'PASS' if ok_a else 'FAIL'}")
    print(f"Part B (clean bound vs exact pmf, zero violations required): {'PASS' if ok_b else 'FAIL'}")
    print(f"Part C (symbolic k2 formula match): {'PASS' if ok_c else 'FAIL'}")
