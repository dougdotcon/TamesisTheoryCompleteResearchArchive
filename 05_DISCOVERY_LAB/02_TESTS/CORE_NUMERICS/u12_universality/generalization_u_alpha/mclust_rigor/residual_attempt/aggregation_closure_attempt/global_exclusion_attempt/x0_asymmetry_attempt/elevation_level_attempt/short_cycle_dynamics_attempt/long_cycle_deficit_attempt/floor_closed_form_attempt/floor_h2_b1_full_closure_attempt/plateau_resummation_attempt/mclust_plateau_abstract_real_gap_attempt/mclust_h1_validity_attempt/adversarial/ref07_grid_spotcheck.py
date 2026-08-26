import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

mp.mp.dps = 100

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

def Rpp(x):
    x = mp.mpf(x)
    return R_func(x) + x * Rprime(x)

def Rppp(x):
    x = mp.mpf(x)
    return 2 * Rprime(x) + x * Rpp(x)

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

def psi4(x):
    return mp.mpf(17) / 3 * Rppp(x)


def F_at(x, c, K, ct0):
    a, b = build_series(c, K)
    s = mp.mpf(x) / mp.sqrt(c)
    t0 = mp.mpf(ct0) / c
    return Phi_at_s(s, t0, a, c)


def ratios(x, c, K, ct0):
    eps = 1 / mp.sqrt(mp.mpf(c))
    F = F_at(x, c, K, ct0)
    p1, p2, p3, p4 = psi1(x), psi2(x), psi3(x), psi4(x)
    rho1 = (F - eps * p1) / eps**2
    gap1 = rho1 - p2
    ratio1 = gap1 / (eps * p3)
    rho2 = (F - eps * p1 - eps**2 * p2) / eps**3
    gap2 = rho2 - p3
    ratio2 = gap2 / (eps * p4)
    return dict(F=F, eps=eps, p1=p1, p2=p2, p3=p3, p4=p4,
                rho1=rho1, gap1=gap1, ratio1=ratio1,
                rho2=rho2, gap2=gap2, ratio2=ratio2)


print("Spot-checking a handful of (x,c) points from the target front's own")
print("42-point grid (x in {0,0.5,1,2,4,6,8}, c in {200,500,1000,2000,4000,8000}),")
print("computed independently (my own machinery, ct0 chosen for plateau depth).")
print()

# choose modest but safe ct0 per c so we stay well converged; verify with a
# two-ct0 check at each point.
points = [
    (2, 1000, 200, [40, 50]),
    (2, 4000, 200, [40, 50]),
    (0, 200, 200, [40, 50]),
    (0, 8000, 200, [40, 50]),
    (8, 1000, 260, [50, 60]),
    (8, 8000, 260, [50, 60]),
]

for x, c, K, ct0_pair in points:
    print(f"--- x={x}, c={c} ---")
    a, b = build_series(c, K)
    s = mp.mpf(x) / mp.sqrt(c)
    vals = {}
    for ct0 in ct0_pair:
        t0 = mp.mpf(ct0) / c
        vals[ct0] = Phi_at_s(s, t0, a, c)
    keys = sorted(vals)
    conv = abs(vals[keys[-1]] - vals[keys[-2]])
    relconv = conv / abs(vals[keys[-1]]) if vals[keys[-1]] != 0 else conv
    print(f"  convergence check |S({keys[-1]})-S({keys[-2]})| rel = {float(relconv):.3e}")
    F = vals[keys[-1]]
    eps = 1 / mp.sqrt(mp.mpf(c))
    p1, p2, p3, p4 = psi1(x), psi2(x), psi3(x), psi4(x)
    rho1 = (F - eps * p1) / eps**2
    gap1 = rho1 - p2
    ratio1 = gap1 / (eps * p3) if p3 != 0 else None
    rho2 = (F - eps * p1 - eps**2 * p2) / eps**3
    gap2 = rho2 - p3
    ratio2 = gap2 / (eps * p4) if p4 != 0 else None
    print(f"  F(x;c)  = {F}")
    print(f"  psi1={float(p1):.6f} psi2={float(p2):.6f} psi3={float(p3):.6f} psi4={float(p4):.6f}")
    print(f"  ratio1 (should -> 1 as eps->0) = {float(ratio1) if ratio1 is not None else 'NA (psi3=0)'}")
    print(f"  ratio2 (should -> 1 as eps->0) = {float(ratio2) if ratio2 is not None else 'NA (psi4=0)'}")
    print()
