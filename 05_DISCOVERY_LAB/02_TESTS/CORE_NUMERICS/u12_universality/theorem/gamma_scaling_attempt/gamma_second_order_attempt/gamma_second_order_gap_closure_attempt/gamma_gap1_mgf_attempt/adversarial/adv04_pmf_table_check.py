"""
Adversarial, from-scratch rebuild of ATTEMPT.md Section 4's direct
pmf-level numerical evidence: computes

  R_k^exact := |E_M[e^{-x(D)}] - (1 - E_M[x] + E_M[x^2]/2)|
  R_k^Gap1  := (1/6) E_M[|x(D)|^3 e^{|x(D)|}]     (Gap 1's own literal target)
  W_bound(n,gamma) := sum_{k=1}^K e^{-s(k)} R_k^Gap1
  W_exact(n,gamma)  := sum_{k=1}^K e^{-s(k)} R_k^exact

via DIRECT summation over the true Binomial(k,gamma) pmf, mpmath dps=50,
using a numerically-stable RECURSIVE pmf evaluation (pmf(0)=(1-gamma)^k,
pmf(m)=pmf(m-1)*(k-m+1)/m*gamma/(1-gamma)) -- exact, no shortcuts, no
Hoeffding/Gaussian approximation anywhere. x(D) uses THIS referee's own
independently re-derived and verified (script adv01) c0..c3 coefficients
(the derivative-based form, confirmed exactly correct and confirmed to
match ATTEMPT.md's own derivative-based form).

K(n) := round(1.5*sqrt(n*ln(n)))  [ATTEMPT.md Section 4: "K=1.5 sqrt(n ln n),
matching script 03's illustrative constant" -- gamma-independent]

s(k) := beta*k^2/n - gamma*k/(2n),  beta := gamma*(2-gamma)/2.

No .py file of any front in this lineage was read or imported. Comparison
is against ATTEMPT.md's own printed table (Section 4), at n=500 and
n=2000, all 6 tested gamma values, to check both magnitude (order-of-
magnitude match; K's rounding convention is not fully pinned down in the
prose, so exact-to-4-digits reproduction is not expected) and the
qualitative claims: monotone decrease in n, R_k^exact <= R_k^Gap1 pointwise.
"""
import mpmath as mp
import time

mp.mp.dps = 50


def tau_val(m, k, n):
    return (m**3/3 + m**2*(mp.mpf('0.5') - k) + m*(k**2 - k + mp.mpf(1)/6)) / n**2

def tau_prime(m, k, n):
    return (m**2 + m*(1 - 2*k) + k**2 - k + mp.mpf(1)/6) / n**2

def tau_double_prime(m, k, n):
    return (2*m + 1 - 2*k) / n**2

def c_coeffs(k, n, gamma):
    gk = gamma * k
    c0 = tau_val(gk, k, n) / 2
    c1 = k*(1-gamma)/n - mp.mpf(1)/(2*n) + tau_prime(gk, k, n)/2
    c2 = -mp.mpf(1)/(2*n) + tau_double_prime(gk, k, n)/4
    c3 = mp.mpf(1)/(6*n**2)
    return c0, c1, c2, c3


def compute_Rk(k, n, gamma):
    """Direct pmf-level computation of R_k^exact and R_k^Gap1 for one k."""
    c0, c1, c2, c3 = c_coeffs(k, n, gamma)
    gk = gamma * k

    # recursive exact Binomial(k,gamma) pmf, m=0..k
    p = mp.mpf(gamma)
    q = 1 - p
    pmf = q**k
    Ex = mp.mpf(0)
    Ex2 = mp.mpf(0)
    E_exp_negx = mp.mpf(0)
    E_absx3_exp_absx = mp.mpf(0)

    for m in range(0, k+1):
        D = m - gk
        x = c0 + c1*D + c2*D**2 + c3*D**3
        Ex += pmf * x
        Ex2 += pmf * x**2
        E_exp_negx += pmf * mp.e**(-x)
        ax = abs(x)
        E_absx3_exp_absx += pmf * ax**3 * mp.e**ax
        if m < k:
            pmf = pmf * (k - m) / (m + 1) * p / q

    R_exact = abs(E_exp_negx - (1 - Ex + Ex2/2))
    R_gap1 = E_absx3_exp_absx / 6
    return R_exact, R_gap1


def s_of_k(k, n, gamma):
    beta = gamma*(2-gamma)/mp.mpf(2)
    return beta*k**2/n - gamma*k/(2*n)


def W_bound_and_exact(n, gamma, K):
    nn, gg = mp.mpf(n), mp.mpf(gamma)
    W_bound = mp.mpf(0)
    W_exact = mp.mpf(0)
    pointwise_violations = 0
    for k in range(1, K+1):
        R_exact, R_gap1 = compute_Rk(k, nn, gg)
        if R_exact > R_gap1 + mp.mpf('1e-30'):
            pointwise_violations += 1
        w = mp.e**(-s_of_k(k, nn, gg))
        W_bound += w * R_gap1
        W_exact += w * R_exact
    return W_bound, W_exact, pointwise_violations


reported_W_bound = {
    500:   {0.1: 0.2766, 0.3: 0.1171, 0.5: 0.02085, 0.7: 0.002837, 0.9: 6.255e-4, 0.99: 5.931e-4},
    2000:  {0.1: 0.2146, 0.3: 0.0721, 0.5: 0.01189, 0.7: 0.001372, 0.9: 1.763e-4, 0.99: 1.520e-4},
}

print("="*90)
print("Rebuilding ATTEMPT.md Section 4's table from scratch, mpmath dps=50, exact pmf")
print("="*90)

results = {}
for n in [500, 2000]:
    ln_n = mp.log(n)
    K = int(round(float(1.5 * mp.sqrt(n * ln_n))))
    print(f"\nn={n}: K = round(1.5*sqrt(n*ln n)) = {K}")
    results[n] = {}
    for gamma in [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
        t0 = time.time()
        W_bound, W_exact, viol = W_bound_and_exact(n, gamma, K)
        elapsed = time.time() - t0
        results[n][gamma] = (float(W_bound), float(W_exact), viol)
        rep = reported_W_bound[n][gamma]
        ratio = float(W_bound) / rep if rep != 0 else float('nan')
        print(f"  gamma={gamma:5.2f}: W_bound(computed)={float(W_bound):.6e}  "
              f"W_bound(reported)={rep:.6e}  ratio={ratio:.4f}  "
              f"W_exact={float(W_exact):.6e}  "
              f"R_exact<=R_gap1 violations={viol}/{K}  [{elapsed:.1f}s]")

print("\n" + "="*90)
print("Monotone-decrease-in-n check (n=500 -> n=2000), computed values")
print("="*90)
for gamma in [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    w500 = results[500][gamma][0]
    w2000 = results[2000][gamma][0]
    print(f"  gamma={gamma:5.2f}: W_bound(500)={w500:.6e} -> W_bound(2000)={w2000:.6e}  "
          f"decreasing: {w2000 < w500}")

print("""
Interpretation: exact numeric agreement with ATTEMPT.md's printed table to
4 significant figures is NOT expected here, because the prose does not
pin down whether K is computed via round(), floor(), or int() of
1.5*sqrt(n*ln n) (a difference of +/-1 in K shifts the sum by one term's
weighted contribution) -- this is a minor documentation gap (K's rounding
convention is left unstated), not a mathematical error, and this script's
own choice (round()) is disclosed above. What matters, and is checked
here directly against ground truth (not against the target's own
numbers): (i) order-of-magnitude / ratio-to-reported match (ratio should
be close to 1, not off by orders of magnitude); (ii) the qualitative
claims -- R_k^exact <= R_k^Gap1 pointwise (zero violations expected, per
the elementary Lagrange-remainder inequality), and W_bound decreasing
monotonically from n=500 to n=2000 at every tested gamma.
""")
