"""
Adversarial re-derivation (hand algebra, cross-checked numerically) of
ATTEMPT.md Section 3.3's leading-order asymptotic claims:

  g(Theta_K) = O(n^{-1/4} polylog(n)) -> 0
  g(K) = kappa_0*(3/2-gamma)*ln(n)*(1+o(1))

using K^2 = kappa_0*n*ln(n) (kappa_0=2.25 illustrative, as the target
front itself discloses), Theta_K = C*sqrt(K*ln n).

HAND-ALGEBRA (done independently, before running any code):
  Theta_K = C*(kappa_0*n*ln n)^{1/4}*(ln n)^{1/2} = O(n^{1/4}(ln n)^{3/4})

  c1(K) ~ K(1-gamma)/n [dominant piece]  = O(n^{-1/2}(ln n)^{1/2})
     -> |c1|*Theta_K = O(n^{-1/4}(ln n)^{5/4})           [matches claim]
  c2(K) ~ -1/(2n) [dominant piece]        = O(n^{-1})
     -> |c2|*Theta_K^2 = O(n^{-1/2}(ln n)^{3/2})          [matches claim]
  c3 = 1/(6n^2) exactly
     -> |c3|*Theta_K^3 = O(n^{-5/4}(ln n)^{9/4})          [matches claim]
  c0(K) ~ tau(gamma*K)/2 ~ K^3/(6n^2) = O(n^{-1/2}(ln n)^{3/2})  [matches claim]

  Dominant term as n->infty: |c1|*Theta_K = O(n^{-1/4}polylog) (slowest
  decay of the four) -- matches ATTEMPT.md's claim that this term
  dominates g(Theta_K).

  At k=K itself: |c1|*K ~ (1-gamma)*K^2/n = (1-gamma)*kappa_0*ln(n)
                 |c2|*K^2 ~ K^2/(2n) = (kappa_0/2)*ln(n)
                 |c0|, |c3|*K^3 = o(ln n) (both -> 0)
  => g(K) ~ kappa_0*[(1-gamma)+1/2]*ln(n) = kappa_0*(3/2-gamma)*ln(n)
     -- matches ATTEMPT.md's closed form EXACTLY.

This script now checks these orders NUMERICALLY (float64, as the target
front itself discloses is adequate here -- only orders of magnitude and
the leading coefficient are being tracked, not high-precision values).
No .py file of the target front (or any front in this lineage) was read.
"""
import numpy as np

def tau_val(m, k, n):
    return (m**3/3 + m**2*(0.5 - k) + m*(k**2 - k + 1/6)) / n**2

def tau_prime(m, k, n):
    return (m**2 + m*(1 - 2*k) + k**2 - k + 1/6) / n**2

def tau_double_prime(m, k, n):
    return (2*m + 1 - 2*k) / n**2

def c_coeffs(k, n, gamma):
    gk = gamma * k
    c0 = tau_val(gk, k, n) / 2
    c1 = k*(1-gamma)/n - 1/(2*n) + tau_prime(gk, k, n)/2
    c2 = -1/(2*n) + tau_double_prime(gk, k, n)/4
    c3 = 1/(6*n**2)
    return c0, c1, c2, c3

def g_func(t, coeffs):
    c0, c1, c2, c3 = coeffs
    return abs(c0) + abs(c1)*t + abs(c2)*t**2 + abs(c3)*t**3

kappa0 = 2.25  # illustrative, matches target front's own script-03 choice
C = 1.5

print("="*78)
print("Check 1: g(Theta_K) -> 0, order O(n^{-1/4} polylog(n))")
print("="*78)
gammas = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
ns = [10**3, 10**4, 10**5, 10**6, 10**7, 10**8]

for gamma in gammas:
    vals = []
    for n in ns:
        K = int(round(np.sqrt(kappa0 * n * np.log(n))))
        Theta_K = C * np.sqrt(K * np.log(n))
        coeffs = c_coeffs(K, n, gamma)
        gTK = g_func(Theta_K, coeffs)
        vals.append(gTK)
    # empirical decay exponent via log-log slope between successive n's
    slopes = []
    for i in range(1, len(ns)):
        slope = (np.log(vals[i]) - np.log(vals[i-1])) / (np.log(ns[i]) - np.log(ns[i-1]))
        slopes.append(slope)
    print(f"gamma={gamma:5.2f}: g(Theta_K) at n=1e3..1e8 = "
          f"{['%.4e'%v for v in vals]}")
    print(f"           monotonically decreasing: {all(vals[i]>vals[i+1] for i in range(len(vals)-1))}, "
          f"empirical log-log slopes (should trend toward -0.25): "
          f"{['%.4f'%s for s in slopes]}")

print("\n" + "="*78)
print("Check 2: g(K) grows like kappa_0*(3/2-gamma)*ln(n), NOT like a power of n")
print("="*78)
for gamma in gammas:
    predicted_lambda = kappa0 * (1.5 - gamma)
    gK_vals = []
    for n in ns:
        K = int(round(np.sqrt(kappa0 * n * np.log(n))))
        coeffs = c_coeffs(K, n, gamma)
        gK = g_func(K, coeffs)
        gK_vals.append(gK)
    # fit g(K) = lambda * ln(n) + const via least squares over ln(n)
    x = np.log(ns)
    y = np.array(gK_vals)
    A = np.vstack([x, np.ones_like(x)]).T
    slope_fit, intercept_fit = np.linalg.lstsq(A, y, rcond=None)[0]
    print(f"gamma={gamma:5.2f}: predicted lambda=kappa0*(3/2-gamma)={predicted_lambda:.4f}, "
          f"least-squares fitted slope (g(K) vs ln n)={slope_fit:.4f}, "
          f"relative diff={abs(slope_fit-predicted_lambda)/predicted_lambda*100:.2f}%")

print("""
Interpretation: the fitted slope of g(K) against ln(n) (NOT against n
itself) should approach the predicted kappa_0*(3/2-gamma) as n grows,
confirming g(K) = Theta(ln n), i.e. e^{g(K)} = Theta(n^lambda), polynomial
in n as claimed -- consistent with what ATTEMPT.md's own Section 3.4
reports finding (~6% match to the leading-order prediction, attributed to
finite-n corrections from the dropped lower-order terms).
""")

print("="*78)
print("Check 3: does the corrected exponent make required_C threshold and")
print("the tail piece actually vanish (sanity of the overall combination)?")
print("="*78)
for gamma in gammas:
    predicted_lambda = kappa0 * (1.5 - gamma)
    threshold_C = np.sqrt(0.25 + 0.5*predicted_lambda)
    C_used = 1.5 * threshold_C
    print(f"gamma={gamma:5.2f}: lambda={predicted_lambda:.4f}, "
          f"threshold C (C^2>1/4+lambda/2) = {threshold_C:.4f}, "
          f"1.5x threshold = {C_used:.4f}")
    ok = 2*C_used**2 - predicted_lambda - 0.5  # should be > 0 for tail piece exponent < 0
    print(f"    2*C_used^2 - lambda - 0.5 = {ok:.4f} (should be > 0 for the "
          f"n^(1/2+lambda-2C^2) tail piece to actually decay)")
