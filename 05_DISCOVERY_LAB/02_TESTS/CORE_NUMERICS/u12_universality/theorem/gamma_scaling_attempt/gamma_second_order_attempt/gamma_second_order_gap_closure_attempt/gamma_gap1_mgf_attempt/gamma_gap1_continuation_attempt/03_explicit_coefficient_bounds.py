"""
03_explicit_coefficient_bounds.py  (revised: cancellation-preserving bounds)

Derives and numerically verifies EXPLICIT, fully-constant elementary upper
bounds on |c_0(k,n,gamma)|, |c_1|, |c_2| (c_3=1/(6n^2) is already explicit),
valid whenever 1 <= k <= n/2 and 0 < gamma <= 1. These are the building
blocks for turning the Gap-1 front's leading-order asymptotics (Section 3.3
of gamma_gap1_mgf_attempt/ATTEMPT.md) into a genuinely explicit, for-all-n-
above-an-explicit-threshold inequality (mandate item 1).

Revision note. A first pass (superseded, see ATTEMPT.md Section 3 of this
front for the narrated correction) bounded every signed monomial of c1, c2
by its absolute value independently via the triangle inequality. That is
valid but destroys a real cancellation: c1's two dominant O(kn/n^2)-order
terms are -gamma*k*n and +k*n, which COMBINE to k*n*(1-gamma)/n^2 =
(1-gamma)k/n -- much smaller than gamma*k/n+k/n for gamma near 1 -- and
similarly for c2's -2k*(1-gamma)/(4n^2) term. Keeping this cancellation
explicit (grouping the two terms before bounding, instead of after) gives a
substantially tighter, still fully elementary and explicit, bound:

  |c0| <= (7/6) k^3/n^2 + (5/6) k^2/n^2                          [unchanged]
  |c1| <= 2 k^2/n^2 + (1-gamma) k/n + k/n^2 + 3/(4n)
  |c2| <= (1-gamma) k/(2n^2) + 3/(4n)
  c3   =  1/(6n^2)                                                [exact]

This script checks these four bounds by DIRECT NUMERIC EVALUATION of the
exact c_i (mpmath, dps=50) against the bound's right-hand side, over a large
grid of (k, n, gamma), 1<=k<=floor(n/2), confirming zero violations.

Reserved seed block 20260900000-20260900999: unused (deterministic grid, no
randomness).
"""
import mpmath as mp

mp.mp.dps = 50


def exact_c(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n); gamma = mp.mpf(gamma)
    c0 = (gamma * k / (12 * n ** 2)) * (
        2 * gamma ** 2 * k ** 2 - 6 * gamma * k ** 2 + 3 * gamma * k
        + 6 * k ** 2 - 6 * k + 1
    )
    c1 = (1 / n ** 2) * (
        (gamma ** 2 * k ** 2) / 2 - gamma * k ** 2 - gamma * k * n
        + (gamma * k) / 2 + (k ** 2) / 2 + k * n - k / 2 - n / 2 + mp.mpf(1) / 12
    )
    c2 = (2 * gamma * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
    c3 = mp.mpf(1) / (6 * n ** 2)
    return c0, c1, c2, c3


def bound_c0(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n)
    return mp.mpf(7) / 6 * k ** 3 / n ** 2 + mp.mpf(5) / 6 * k ** 2 / n ** 2


def bound_c1(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n); gamma = mp.mpf(gamma)
    return (2 * k ** 2 / n ** 2 + (1 - gamma) * k / n + k / n ** 2
            + mp.mpf(3) / (4 * n))


def bound_c2(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n); gamma = mp.mpf(gamma)
    return (1 - gamma) * k / (2 * n ** 2) + mp.mpf(3) / (4 * n)


print("Derivation of the cancellation-preserving c1, c2 bounds:")
print("""
c1 = (1/n^2)[ (g^2 k^2)/2 - g k^2 - g k n + (g k)/2 + k^2/2 + k n - k/2 - n/2 + 1/12 ]
   = (1/n^2)[ (g^2 k^2)/2 - g k^2 + (g k)/2 + k^2/2 - k/2 - n/2 + 1/12  +  k n (1-g) ]
Bounding the first six terms by triangle inequality (0<g<=1, so g^2<=g<=1):
  |(g^2k^2)/2 - g k^2 + (gk)/2 + k^2/2 - k/2 - n/2 + 1/12|
     <= k^2/2 + k^2 + k/2 + k^2/2 + k/2 + n/2 + 1/12 = 2k^2 + k + n/2 + 1/12
so |c1| <= [2k^2 + k + n/2 + 1/12 + kn(1-g)] / n^2
         = 2k^2/n^2 + k/n^2 + 1/(2n) + 1/(12n^2) + (1-g)k/n
        <= 2k^2/n^2 + (1-g)k/n + k/n^2 + 3/(4n)
(using 1/(2n)+1/(12n^2) <= 3/(4n) for n>=1: at n=1, 0.5+0.0833=0.583<=0.75).

c2 = (2 g k - 2k - 2n + 1)/(4n^2) = [ -2k(1-g) - 2n + 1 ] / (4n^2)
   |c2| <= [2k(1-g) + 2n + 1] / (4n^2) = (1-g)k/(2n^2) + 1/(2n) + 1/(4n^2)
        <= (1-g)k/(2n^2) + 3/(4n)   (same n>=1 bundling as above).
""")

n_values = [10, 30, 100, 316, 1000, 3162, 10000, 31623, 100000]
gamma_values = [mp.mpf(g) for g in
                ['0.01', '0.05', '0.1', '0.2', '0.3', '0.5', '0.7', '0.9', '0.99', '0.999']]

violations = []
n_checks = 0
worst_ratio = {'c0': mp.mpf(0), 'c1': mp.mpf(0), 'c2': mp.mpf(0)}

for n in n_values:
    kmax = n // 2
    if kmax < 1:
        continue
    k_samples = sorted(set(
        [1, 2, 3, max(1, kmax // 100), max(1, kmax // 10), max(1, kmax // 3),
         max(1, kmax // 2), kmax]
    ))
    for k in k_samples:
        if k < 1 or k > kmax:
            continue
        for gamma in gamma_values:
            c0, c1, c2, c3 = exact_c(k, n, gamma)
            b0, b1, b2 = bound_c0(k, n, gamma), bound_c1(k, n, gamma), bound_c2(k, n, gamma)
            n_checks += 3
            ok0 = abs(c0) <= b0 + mp.mpf('1e-40')
            ok1 = abs(c1) <= b1 + mp.mpf('1e-40')
            ok2 = abs(c2) <= b2 + mp.mpf('1e-40')
            if b0 > 0:
                worst_ratio['c0'] = max(worst_ratio['c0'], abs(c0) / b0)
            if b1 > 0:
                worst_ratio['c1'] = max(worst_ratio['c1'], abs(c1) / b1)
            if b2 > 0:
                worst_ratio['c2'] = max(worst_ratio['c2'], abs(c2) / b2)
            if not (ok0 and ok1 and ok2):
                violations.append((n, k, float(gamma), ok0, ok1, ok2))

print(f"Total pointwise inequality checks: {n_checks}")
print(f"Grid: n in {n_values}")
print(f"      gamma in {[float(g) for g in gamma_values]}")
print(f"      k sampled across [1, floor(n/2)] at several points per n")
print(f"\nViolations found: {len(violations)}")
if violations:
    for v in violations[:20]:
        print("  VIOLATION:", v)
else:
    print("Zero violations -- the three explicit cancellation-preserving bounds")
    print("  |c0| <= (7/6) k^3/n^2 + (5/6) k^2/n^2")
    print("  |c1| <= 2 k^2/n^2 + (1-gamma) k/n + k/n^2 + 3/(4n)")
    print("  |c2| <= (1-gamma) k/(2n^2) + 3/(4n)")
    print("hold at every tested (k,n,gamma) point with 1<=k<=floor(n/2).")

print("\nWorst-case (true/bound) tightness ratio observed per coefficient:")
for lbl in ['c0', 'c1', 'c2']:
    if worst_ratio[lbl] > 0:
        print(f"  max(|{lbl}|/bound_{lbl}) over grid = {float(worst_ratio[lbl]):.6f} "
              f"(must be <= 1 for validity)")

assert len(violations) == 0, "Crude coefficient bounds FALSIFIED -- see violations above"
print(f"\nAll three bounds numerically CONFIRMED valid (0 violations, "
      f"{n_checks} checks) on the tested grid.")
