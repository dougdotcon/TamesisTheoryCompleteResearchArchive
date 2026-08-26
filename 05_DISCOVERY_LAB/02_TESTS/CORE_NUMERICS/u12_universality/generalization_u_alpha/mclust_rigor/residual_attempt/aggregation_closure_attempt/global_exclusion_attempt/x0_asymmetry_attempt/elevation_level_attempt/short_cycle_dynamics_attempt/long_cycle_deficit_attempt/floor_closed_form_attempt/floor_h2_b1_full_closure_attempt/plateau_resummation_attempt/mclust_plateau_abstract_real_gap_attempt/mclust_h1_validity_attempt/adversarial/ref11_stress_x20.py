import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

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

def psi1(x): return R_func(x)
def psi2(x):
    x = mp.mpf(x)
    return 2 * x * R_func(x) - 2
def psi3(x):
    x = mp.mpf(x)
    f = lambda t: mp.e**(-t*t/2) * 7 * Rprime(t)
    integral = mp.quad(f, [x, mp.inf])
    return -mp.e**(x*x/2) * integral

def run(c, X, K, dps, ct0pair, label):
    mp.mp.dps = dps
    a, b = build_series(c, K)
    s = mp.mpf(X) / mp.sqrt(c)
    t0a = mp.mpf(ct0pair[0]) / c
    t0b = mp.mpf(ct0pair[1]) / c
    Fa = Phi_at_s(s, t0a, a, c)
    Fb = Phi_at_s(s, t0b, a, c)
    relconv = abs(Fb - Fa) / abs(Fb) if Fb != 0 else abs(Fb-Fa)
    F = Fb
    eps = 1 / mp.sqrt(mp.mpf(c))
    p1x, p2x, p3x = psi1(X), psi2(X), psi3(X)
    rho1 = (F - eps * p1x) / eps**2
    gap1 = rho1 - p2x
    ratio1 = gap1 / (eps * p3x)
    print(f"[{label}] c={c} x={X} K={K} dps={dps}: convcheck(rel)={float(relconv):.3e}  "
          f"F={F}")
    print(f"        ratio1 = {ratio1}")
    return relconv, ratio1

print("=== UNDERSIZED sizing, mimicking the front's own first (failed) pass ===")
run(200, 20, 400, 60, (45, 60), "undersized, K=400,dps=60")

print()
print("=== CORRECTED sizing, mimicking the front's own §5.2 rerun ===")
run(200, 20, 800, 90, (45, 60), "corrected, K=800,dps=90")

print()
print("=== push even further to confirm true convergence (independent of their sizing choice) ===")
run(200, 20, 1200, 130, (45, 60), "extra margin, K=1200,dps=130")
