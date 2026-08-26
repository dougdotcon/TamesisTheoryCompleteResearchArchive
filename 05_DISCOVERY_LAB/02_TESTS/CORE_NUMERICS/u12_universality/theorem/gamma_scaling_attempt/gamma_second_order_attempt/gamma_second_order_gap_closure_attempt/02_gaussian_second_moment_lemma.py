"""
Gap 2 closure -- Lemma G2 (Gaussian second-moment sum), numeric verification.

Claim (Lemma G2, derived in ATTEMPT.md Sec.2.3 by differentiating the
already-PROVED Poisson-summation/Jacobi-theta identity of the predecessor's
Lemma D0 w.r.t. the parameter a):

    sum_{k=1}^infty k^2 e^{-a k^2} = (sqrt(pi)/4) a^{-3/2} + O(a^{-5/2} e^{-pi^2/a})

  and therefore, truncating at k=n (a=beta/n so a n^2 = beta n -> infty,
  tail exponentially small):

    sum_{k=1}^n k^2 e^{-beta k^2 / n} = (sqrt(pi)/4)(n/beta)^{3/2}
                                          + O(n^{5/2} e^{-c n})

This script checks the leading-order closed form numerically (mpmath,
dps=50) against brute-force high-precision summation, for several values
of a (equivalently of (n, beta)), and confirms the residual shrinks
super-polynomially (consistent with the claimed exponential order), not
just as a generic power of a.
"""
from mpmath import mp, mpf, exp, sqrt, pi, nsum, inf

mp.dps = 50


def direct_sum_k2(a, kmax):
    total = mpf(0)
    for k in range(1, kmax + 1):
        total += mpf(k) ** 2 * exp(-a * mpf(k) ** 2)
    return total


print("=" * 78)
print("Lemma G2 check: sum_{k=1}^infty k^2 e^{-a k^2}  vs  (sqrt(pi)/4) a^{-3/2}")
print("=" * 78)
print(f"{'a':>12} {'direct sum (kmax=2000)':>28} {'closed form':>20} {'abs resid':>14} {'resid/a^{-3/2} rel':>20}")

as_to_test = [mpf('1.0'), mpf('0.1'), mpf('0.01'), mpf('0.001'), mpf('0.0001')]
residuals = []
for a in as_to_test:
    kmax = 2000
    s = direct_sum_k2(a, kmax)
    closed = (sqrt(pi) / 4) * a ** mpf('-1.5')
    resid = s - closed
    rel = resid / closed
    residuals.append((a, resid))
    print(f"{float(a):12.6g} {float(s):28.16g} {float(closed):20.16g} {float(resid):14.6e} {float(rel):20.6e}")

print()
print("Check the residual shrinks FASTER than any fixed power of a as a->0")
print("(consistent with the claimed e^{-pi^2/a} order, not just O(a^p) for fixed p):")
for j in range(len(as_to_test) - 1):
    a1, r1 = residuals[j]
    a2, r2 = residuals[j + 1]
    if r1 == 0 or r2 == 0:
        continue
    # if resid ~ a^{-5/2} e^{-pi^2/a}, then ln|resid| ~ -pi^2/a + const,
    # so ln|r1/r2| should track pi^2*(1/a2 - 1/a1), NOT a power law.
    import math
    lhs = math.log(abs(float(r1))) - math.log(abs(float(r2)))
    predicted = float(pi) ** 2 * (1 / float(a2) - 1 / float(a1)) + (-1.5) * (
        math.log(float(a1)) - math.log(float(a2))
    )
    print(f"  a: {float(a1):.4g} -> {float(a2):.4g}   ln|r1/r2|={lhs:12.4f}   "
          f"predicted (pi^2*(1/a2-1/a1) + power term)={predicted:12.4f}")

print()
print("=" * 78)
print("Now the *finite-n* truncated version actually used in the ATTEMPT:")
print("  sum_{k=1}^n k^2 e^{-beta k^2/n}  vs  (sqrt(pi)/4)(n/beta)^{3/2}")
print("=" * 78)
print(f"{'gamma':>8} {'n':>10} {'direct sum':>22} {'closed form':>22} {'rel err':>14}")
gammas = [mpf('0.1'), mpf('0.3'), mpf('0.5'), mpf('0.7'), mpf('0.9'), mpf('1.0')]
ns = [2000, 20000, 200000]
for g in gammas:
    beta = g * (2 - g) / 2
    for n in ns:
        a = beta / mpf(n)
        s = direct_sum_k2(a, n)  # sum_{k=1}^n, exact truncation matching the real sum
        closed = (sqrt(pi) / 4) * (mpf(n) / beta) ** mpf('1.5')
        rel = (s - closed) / closed
        print(f"{float(g):8.2f} {n:10d} {float(s):22.10g} {float(closed):22.10g} {float(rel):14.3e}")

print()
print("Relative error should shrink very fast with n (consistent with the")
print("claimed exponentially-small-in-n tail correction), at every gamma.")
