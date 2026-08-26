"""
Extension of adv04: spot-checks ATTEMPT.md Section 4's table at larger n
(8000, 32000), a subset of gamma values (to keep runtime reasonable),
same from-scratch exact-pmf method (mpmath dps=50).
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


def compute_Rk_gap1(k, n, gamma):
    c0, c1, c2, c3 = c_coeffs(k, n, gamma)
    gk = gamma * k
    p = mp.mpf(gamma)
    q = 1 - p
    pmf = q**k
    E_absx3_exp_absx = mp.mpf(0)
    for m in range(0, k+1):
        D = m - gk
        x = c0 + c1*D + c2*D**2 + c3*D**3
        ax = abs(x)
        E_absx3_exp_absx += pmf * ax**3 * mp.e**ax
        if m < k:
            pmf = pmf * (k - m) / (m + 1) * p / q
    return E_absx3_exp_absx / 6


def s_of_k(k, n, gamma):
    beta = gamma*(2-gamma)/mp.mpf(2)
    return beta*k**2/n - gamma*k/(2*n)


def W_bound(n, gamma, K):
    nn, gg = mp.mpf(n), mp.mpf(gamma)
    W = mp.mpf(0)
    for k in range(1, K+1):
        R_gap1 = compute_Rk_gap1(k, nn, gg)
        w = mp.e**(-s_of_k(k, nn, gg))
        W += w * R_gap1
    return W


reported = {
    8000:  {0.1: 0.1670, 0.5: 0.00717, 0.9: 5.152e-5},
    32000: {0.1: 0.1271, 0.5: 0.00455, 0.9: 1.669e-5},
}

for n in [8000, 32000]:
    ln_n = mp.log(n)
    K = int(round(float(1.5 * mp.sqrt(n * ln_n))))
    print(f"n={n}: K={K}")
    for gamma in [0.1, 0.5, 0.9]:
        t0 = time.time()
        W = W_bound(n, gamma, K)
        elapsed = time.time() - t0
        rep = reported[n][gamma]
        ratio = float(W) / rep
        print(f"  gamma={gamma:4.2f}: computed={float(W):.6e}  reported={rep:.6e}  "
              f"ratio={ratio:.4f}  [{elapsed:.1f}s]")
