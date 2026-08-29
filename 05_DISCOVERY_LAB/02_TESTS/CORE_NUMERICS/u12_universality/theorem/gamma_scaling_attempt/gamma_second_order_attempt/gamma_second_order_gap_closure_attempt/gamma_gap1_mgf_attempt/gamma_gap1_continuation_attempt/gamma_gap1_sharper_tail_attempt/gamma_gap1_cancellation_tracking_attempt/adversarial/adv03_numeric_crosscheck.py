"""
Independent referee numeric cross-check of the two x_K(D)/ln(n) limits,
using the TRUE ceiling K := ceil(sqrt((4/beta) n ln n)) (not the idealized
real-valued surrogate used in the symbolic derivation), at extreme n
(up to 10^200) and several gamma values, mpmath dps=80.
"""
from mpmath import mp, mpf, log, ceil, sqrt

mp.dps = 80

def c_coeffs(gamma, k, n):
    gamma = mpf(gamma); k = mpf(k); n = mpf(n)
    c0 = gamma*k*(2*gamma**2*k**2 - 6*gamma*k**2 + 3*gamma*k + 6*k**2 - 6*k + 1) / (12*n**2)
    c1 = (gamma**2*k**2/2 - gamma*k**2 - gamma*k*n + gamma*k/2 + k**2/2 + k*n - k/2 - n/2 + mpf(1)/12) / n**2
    c2 = (2*gamma*k - 2*k - 2*n + 1) / (4*n**2)
    c3 = mpf(1)/6 / n**2
    return c0, c1, c2, c3

def x_of_D(gamma, k, n, D):
    c0, c1, c2, c3 = c_coeffs(gamma, k, n)
    return c0 + c1*D + c2*D**2 + c3*D**3

def true_K(gamma, n):
    gamma = mpf(gamma); n = mpf(n)
    beta = gamma*(2-gamma)/2
    return ceil(sqrt(4*n*log(n)/beta))

gammas = [mpf('0.5'), mpf('0.1'), mpf('0.01'), mpf('0.9'), mpf('0.99')]
ns = [mpf(10)**50, mpf(10)**100, mpf(10)**200]

print(f"{'gamma':>8} {'n':>8} {'x(Dmax)/ln n':>22} {'predicted 4(1-g)^2/(g(2-g))':>28} {'diff':>12}   {'x(Dmin)/ln n':>16} {'predicted -4':>12} {'diff':>12}")
for gamma in gammas:
    predicted_max = 4*(1-gamma)**2/(gamma*(2-gamma))
    for n in ns:
        K = true_K(gamma, n)
        Dmax = (1-gamma)*K
        Dmin = -gamma*K
        val_max = x_of_D(gamma, K, n, Dmax)/log(n)
        val_min = x_of_D(gamma, K, n, Dmin)/log(n)
        diff_max = val_max - predicted_max
        diff_min = val_min - mpf(-4)
        print(f"{float(gamma):>8.3f} 1e{int(log(n)/log(10)):>4} {float(val_max):>22.10f} {float(predicted_max):>28.10f} {float(diff_max):>12.2e}   {float(val_min):>16.10f} {-4.0:>12.2f} {float(diff_min):>12.2e}")
