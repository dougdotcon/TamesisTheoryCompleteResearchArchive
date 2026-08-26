import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

mp.mp.dps = 140

def fam_eval(f, s, c):
    return p_eval(f.P, s) + p_eval(f.Q, s) * erfcx_safe(s * mp.sqrt(c / 2))

def Phi_at_s(s, t0, a_list, c):
    s = mp.mpf(s)
    t0 = mp.mpf(t0)
    total = mp.mpf(0)
    for k, ak in enumerate(a_list):
        total += fam_eval(ak, s, c) * t0 ** k
    return total

def R_func(x):
    x = mp.mpf(x)
    return mp.sqrt(mp.pi / 2) * mp.exp(x * x / 2) * mp.erfc(x / mp.sqrt(2))

def Rprime(x):
    return mp.mpf(x) * R_func(x) - 1

def psi1(x):
    return R_func(x)

def psi2(x):
    x = mp.mpf(x)
    return 2 * x * R_func(x) - 2

def psi3(x):
    x = mp.mpf(x)
    f = lambda t: mp.e**(-t*t/2) * 7 * Rprime(t)
    integral = mp.quad(f, [x, mp.inf])
    return -mp.e**(x*x/2) * integral

def Rpp(x):
    x = mp.mpf(x)
    return R_func(x) + x * Rprime(x)

def Rppp(x):
    x = mp.mpf(x)
    return 2 * Rprime(x) + x * Rpp(x)

def psi4(x):
    return mp.mpf(17) / 3 * Rppp(x)

c = 200
x = 0
K = 420
print(f"c={c}, x={x}, K={K}, dps=140")
a, b = build_series(c, K)
s = mp.mpf(x) / mp.sqrt(c)
for ct0 in [40, 50, 60]:
    t0 = mp.mpf(ct0) / c
    F = Phi_at_s(s, t0, a, c)
    print(f"  ct0={ct0}: F = {F}")

t0_50 = mp.mpf(50) / c
t0_60 = mp.mpf(60) / c
F50 = Phi_at_s(s, t0_50, a, c)
F60 = Phi_at_s(s, t0_60, a, c)
relconv = abs(F60 - F50) / abs(F60)
print(f"convergence check |S(60)-S(50)|/|S(60)| = {relconv}")

eps = 1 / mp.sqrt(mp.mpf(c))
p1, p2, p3, p4 = psi1(x), psi2(x), psi3(x), psi4(x)
F = F60
rho1 = (F - eps * p1) / eps**2
gap1 = rho1 - p2
ratio1 = gap1 / (eps * p3)
rho2 = (F - eps * p1 - eps**2 * p2) / eps**3
gap2 = rho2 - p3
ratio2 = gap2 / (eps * p4)
print(f"ratio1 = {ratio1}")
print(f"ratio2 = {ratio2}")
