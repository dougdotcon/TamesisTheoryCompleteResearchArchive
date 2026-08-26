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

psi1_0 = R_func(0)
psi2_0 = mp.mpf(-2)
psi3_0 = mp.mpf(7) / 2 * mp.sqrt(mp.pi / 2)
psi4_0 = mp.mpf(-34) / 3

# c-grid matches the target front's own 6 values (ATTEMPT.md sec 4.1)
c_list = [200, 500, 1000, 2000, 4000, 8000]
# per-c (K, ct0-pair) sized generously; smaller c needs bigger K, matching
# the same "order-2-entire cancellation cost wall" pattern documented in
# the required-reading lineage (grandparent doc sec 2.2) and in this
# front's own sec 5.1.
sizing = {
    200: (420, [50, 60]),
    500: (300, [50, 60]),
    1000: (260, [50, 60]),
    2000: (220, [50, 60]),
    4000: (200, [50, 60]),
    8000: (200, [50, 60]),
}

results = []
for c in c_list:
    K, (ct0a, ct0b) = sizing[c]
    a, b = build_series(c, K)
    s = mp.mpf(0)
    t0a = mp.mpf(ct0a) / c
    t0b = mp.mpf(ct0b) / c
    Fa = Phi_at_s(s, t0a, a, c)
    Fb = Phi_at_s(s, t0b, a, c)
    relconv = abs(Fb - Fa) / abs(Fb)
    F = Fb
    eps = 1 / mp.sqrt(mp.mpf(c))
    rho1 = (F - eps * psi1_0) / eps**2
    gap1 = rho1 - psi2_0
    ratio1 = gap1 / (eps * psi3_0)
    rho2 = (F - eps * psi1_0 - eps**2 * psi2_0) / eps**3
    gap2 = rho2 - psi3_0
    ratio2 = gap2 / (eps * psi4_0)
    results.append((c, eps, F, ratio1, ratio2, relconv))
    print(f"c={c:5d} eps={float(eps):.6f} convcheck={float(relconv):.2e} "
          f"ratio1={float(ratio1):.8f} ratio2={float(ratio2):.8f}")

# naive least-squares linear extrapolation of ratio vs eps to eps=0,
# same style as ATTEMPT.md sec 4.2's "per-x linear (Richardson-type)
# extrapolation"
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
print(f"  (target front's own table, x=0, order 1: 0.99303586)")
print(f"linear extrapolation to eps=0, order 2: intercept = {intercept2:.8f}")
print(f"  (target front's own table, x=0, order 2: 0.99166188)")
