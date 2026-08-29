"""
Independent numeric (mpmath) verification, fresh implementation, of:
 - the swap-route Richardson extrapolation for C(0.5) (target sec.5)
 - the fitted local-decay-rate c(n,gamma) at n=6400 for gamma=1/2,1/5,7/10 (target sec.4/script 06)
 - the T(n,m) vs T_inf(n,m) truncation error at n=20,m=6,gamma=0.2 (target sec.3, script 03 Part C)
Different sample n's / method choices than the target's own scripts where feasible,
to serve as an independent cross-check rather than a re-run.
"""
import mpmath as mp
mp.mp.dps = 25

def T_nm(n, m, gamma):
    x = 1 - gamma
    total = mp.mpf(0)
    xp = mp.mpf(1)
    for j in range(0, n - m + 1):
        total += mp.binomial(j + m, m) * mp.binomial(n - j, m) * xp
        xp *= x
    return total

def S_n_prime_swap(n, gamma):
    total = mp.mpf(0)
    for m in range(0, n + 1):
        Tnm = T_nm(n, m, gamma)
        term = (mp.mpf(gamma)**m / mp.mpf(n)**m) * mp.factorial(m) * Tnm
        total += term
        if m > 20 and term < mp.mpf(10)**(-22) * total:
            break
    return total

def phi_inf(c):
    return (mp.sqrt(mp.pi) / 2) * c**mp.mpf(-0.5) * mp.erf(mp.sqrt(c))

print("="*78)
print("Independent Richardson check, gamma=0.5, DIFFERENT n's than target's script05")
print("(target used n=1600,3200; here: n=1000,4000, 3-point n=1000,2000,4000 too)")
print("="*78)
gamma = mp.mpf('0.5')
target_ratio = mp.sqrt(mp.mpf(2)/(2-gamma))
C_closed = -(mp.mpf(2)/(3*mp.sqrt(mp.pi))) * mp.sqrt(gamma) * (6-8*gamma+3*gamma**2)/(2-gamma)**2
print("target T(gamma) =", target_ratio)
print("C(gamma) closed form =", C_closed)

data = {}
for n in [500, 1000, 2000]:
    Snp = S_n_prime_swap(n, gamma)
    Sn = Snp - 1
    phi_ngn = Sn / n
    pinf = phi_inf(gamma * n)
    R = phi_ngn / pinf
    scaled = mp.sqrt(n) * (R - target_ratio)
    data[n] = scaled
    print(f"  n={n:5d}  R={float(R):.10f}  sqrt(n)*(R-T)={float(scaled):.6f}")

# 2-pt Richardson with DIFFERENT pair than target (1000,2000 instead of 1600,3200)
import math
n1, n2 = 1000, 2000
x1, x2 = float(data[n1]), float(data[n2])
A = [[1, 1/math.sqrt(n1)], [1, 1/math.sqrt(n2)]]
det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
C_extrap = (x1*A[1][1] - A[0][1]*x2) / det
print(f"\n  2-pt Richardson (n={n1},{n2}): C_extrap = {C_extrap:.6f}")
print(f"  C(gamma) closed form           = {float(C_closed):.6f}")
print(f"  |diff| = {abs(C_extrap - float(C_closed)):.6f}")

print()
print("="*78)
print("Independent fitted local rate c(n,gamma) at n=6400, m=1 (fresh mpmath code)")
print("="*78)
def term_m(n, m, gamma):
    Tnm = T_nm(n, m, gamma)
    fact_m = mp.factorial(m)
    return (mp.mpf(gamma)**m / mp.mpf(n)**m) * fact_m * Tnm

for gval, label in [(mp.mpf(1)/2, '1/2'), (mp.mpf(1)/5, '1/5'), (mp.mpf(7)/10, '7/10')]:
    n = 6400
    t0 = term_m(n, 0, gval)
    t1 = term_m(n, 1, gval)
    c_fit = -mp.log(t1/t0) * n
    predicted = 2*(1-gval)/gval
    print(f"  gamma={label}: fitted c(n=6400,m=1) = {float(c_fit):.6f}   predicted 2(1-g)/g = {float(predicted):.6f}")

print()
print("="*78)
print("Independent truncation-error check T(n,m) vs T_inf(n,m) at n=20,m=6,gamma=0.2")
print("(fresh mpmath-based coefficient extraction via high-order Taylor series,")
print(" NOT sympy.series like the target's script03 -- different method entirely)")
print("="*78)
def T_inf_mpmath(n, m, gamma, order_extra=5):
    # [y^m] (1+y)^(n+m+1) / (y+gamma)^(m+1)
    # Use mpmath taylor of f(y) around y=0 to sufficient order.
    f = lambda y: (1+y)**(n+m+1) / (y+gamma)**(m+1)
    coeffs = mp.taylor(f, 0, m)
    return coeffs[m]

n_, m_, g_ = 20, 6, mp.mpf('0.2')
Te = T_nm(n_, m_, g_)
Ti = T_inf_mpmath(n_, m_, g_)
relerr = abs(Te - Ti)/abs(Te)
print(f"  T_exact({n_},{m_},{float(g_)}) = {float(Te):.6f}")
print(f"  T_inf  ({n_},{m_},{float(g_)}) = {float(Ti):.6f}")
print(f"  relative error = {float(relerr):.6e}  (target claimed approx 9e3 = 9000)")

# also check a "safe" regime to confirm approximation IS good there (m << n)
n_, m_, g_ = 100, 3, mp.mpf('0.2')
Te2 = T_nm(n_, m_, g_)
Ti2 = T_inf_mpmath(n_, m_, g_)
relerr2 = abs(Te2-Ti2)/abs(Te2)
print(f"  Sanity (m<<n): T_exact({n_},{m_},{float(g_)})={float(Te2):.6f}  T_inf={float(Ti2):.6f}  relerr={float(relerr2):.3e}")

print("\nDONE.")
