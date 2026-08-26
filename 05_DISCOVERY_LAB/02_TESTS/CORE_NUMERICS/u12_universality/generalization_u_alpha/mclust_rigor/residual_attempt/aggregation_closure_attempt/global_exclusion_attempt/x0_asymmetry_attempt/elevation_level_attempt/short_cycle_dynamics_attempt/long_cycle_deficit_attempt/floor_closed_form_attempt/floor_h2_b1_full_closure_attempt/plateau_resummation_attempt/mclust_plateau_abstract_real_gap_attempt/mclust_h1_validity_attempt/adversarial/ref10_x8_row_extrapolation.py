import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

mp.mp.dps = 150

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

def psi1(x): return R_func(x)
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

X = 8
p1x, p2x, p3x, p4x = psi1(X), psi2(X), psi3(X), psi4(X)
print(f"x={X}: psi1={p1x} psi2={p2x} psi3={p3x} psi4={p4x}")

c_list = [200, 500, 1000, 2000, 4000, 8000]
sizing = {
    200: (500, [60, 75]),
    500: (400, [60, 75]),
    1000: (320, [60, 75]),
    2000: (280, [60, 75]),
    4000: (260, [60, 75]),
    8000: (240, [60, 75]),
}

results = []
for c in c_list:
    K, (ct0a, ct0b) = sizing[c]
    a, b = build_series(c, K)
    s = mp.mpf(X) / mp.sqrt(c)
    t0a = mp.mpf(ct0a) / c
    t0b = mp.mpf(ct0b) / c
    Fa = Phi_at_s(s, t0a, a, c)
    Fb = Phi_at_s(s, t0b, a, c)
    relconv = abs(Fb - Fa) / abs(Fb)
    F = Fb
    eps = 1 / mp.sqrt(mp.mpf(c))
    rho1 = (F - eps * p1x) / eps**2
    gap1 = rho1 - p2x
    ratio1 = gap1 / (eps * p3x)
    rho2 = (F - eps * p1x - eps**2 * p2x) / eps**3
    gap2 = rho2 - p3x
    ratio2 = gap2 / (eps * p4x)
    results.append((c, eps, F, ratio1, ratio2, relconv))
    print(f"c={c:5d} eps={float(eps):.6f} convcheck={float(relconv):.2e} "
          f"ratio1={float(ratio1):.8f} ratio2={float(ratio2):.8f}")

xs = [float(r[1]) for r in results]
y1 = [float(r[3]) for r in results]
y2 = [float(r[4]) for r in results]

def linfit_intercept(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    slope = num / den
    intercept = my - slope * mx
    return slope, intercept

slope1, intercept1 = linfit_intercept(xs, y1)
slope2, intercept2 = linfit_intercept(xs, y2)

print()
print(f"linear extrapolation to eps=0, order 1: intercept = {intercept1:.8f}")
print(f"  (target front's own table, x=8, order 1: 0.99953952)")
print(f"linear extrapolation to eps=0, order 2: intercept = {intercept2:.8f}")
print(f"  (target front's own table, x=8, order 2: 0.99932366)")
print()
print("Monotone-tightening check: |1-extrap| at x=0 vs x=8:")
print(f"  order1: x=0 -> {abs(1-0.99303586):.6f}   x=8 -> {abs(1-intercept1):.6f}")
print(f"  order2: x=0 -> {abs(1-0.99166188):.6f}   x=8 -> {abs(1-intercept2):.6f}")
