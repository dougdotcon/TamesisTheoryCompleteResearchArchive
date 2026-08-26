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

# grandparent (plateau_resummation_attempt/ATTEMPT.md sec 6) published F(s)
# table at c=1000, x in {0,0.5,1,2,3} -- independent cross-check target
published_c1000 = {
    0.0: mp.mpf("0.037761598340"),
    0.5: mp.mpf("0.026651014044"),
    1.0: mp.mpf("0.020078232025"),
    2.0: mp.mpf("0.013021626995"),
    3.0: mp.mpf("0.009464425126"),
}

c = 1000
K = 200
print(f"Building series at c={c}, K={K} ...")
a, b = build_series(c, K)

print(f"{'x':>5} {'s=x/sqrt(c)':>18} {'F(s) mine':>28} {'published':>16} {'reldiff':>12}")
for x, pub in published_c1000.items():
    s = mp.mpf(x) / mp.sqrt(c)
    t0 = mp.mpf(50) / c   # ct0=50, deep in plateau at c=1000 as established above
    F = Phi_at_s(s, t0, a, c)
    reldiff = abs(F - pub) / pub if pub != 0 else abs(F)
    print(f"{x:5.1f} {float(s):18.10f} {str(F)[:28]:>28} {str(pub):>16} {float(reldiff):.3e}")

print()
print("Also cross-check the 2nd-order profile prediction 2xR(x)-2 (grandparent sec 6):")
eps = 1 / mp.sqrt(mp.mpf(c))
for x in [0.0, 0.5, 1.0, 2.0, 3.0]:
    s = mp.mpf(x) / mp.sqrt(c)
    t0 = mp.mpf(50) / c
    F = Phi_at_s(s, t0, a, c)
    Rx = R_func(x)
    resid2 = (F - eps * Rx) / eps**2
    pred2 = 2 * mp.mpf(x) * Rx - 2
    print(f"x={x}: (F-eps*R)/eps^2 = {float(resid2):.6f}   predicted 2xR-2 = {float(pred2):.6f}")
