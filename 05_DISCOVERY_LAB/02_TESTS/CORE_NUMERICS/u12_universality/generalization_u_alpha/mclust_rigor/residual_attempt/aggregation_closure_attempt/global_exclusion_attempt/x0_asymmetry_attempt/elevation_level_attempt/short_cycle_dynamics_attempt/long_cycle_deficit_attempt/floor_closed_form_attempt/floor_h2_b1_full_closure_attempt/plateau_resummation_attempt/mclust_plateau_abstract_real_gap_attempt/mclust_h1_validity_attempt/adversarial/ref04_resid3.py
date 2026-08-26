import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

mp.mp.dps = 90

def fam_eval0(f):
    return p_eval(f.P, 0) + p_eval(f.Q, 0) * erfcx_safe(0)

def Phi_at_0(t0, a_list):
    t0 = mp.mpf(t0)
    s = mp.mpf(0)
    for k, ak in enumerate(a_list):
        s += fam_eval0(ak) * t0 ** k
    return s

def compute_Pi(c, K, ct0_values):
    a, b = build_series(c, K)
    results = {}
    for ct0 in ct0_values:
        t0 = mp.mpf(ct0) / c
        results[ct0] = Phi_at_0(t0, a)
    return results, a

R0 = mp.sqrt(mp.pi / 2)   # psi1(0)
psi2_0 = mp.mpf(-2)       # psi2(0) = 2*0*R(0) - 2

def resid3(Pi_c, c):
    eps = 1 / mp.sqrt(mp.mpf(c))
    return (Pi_c - eps * R0 - eps**2 * psi2_0) / eps**3

print("=" * 70)
print("c = 1000")
print("=" * 70)
K1 = 260
res1, a1 = compute_Pi(1000, K1, [180, 220, 260])
for ct0, val in res1.items():
    print(f"ct0={ct0}: Phi(0,{ct0}/1000) = {val}")
diff_hi = abs(res1[260] - res1[220])
diff_lo = abs(res1[220] - res1[180])
print(f"approach-convergence check: |S(220)-S(260)| = {diff_hi}, |S(180)-S(220)| = {diff_lo}")
Pi1000 = res1[260]
r3_1000 = resid3(Pi1000, 1000)
print(f"Pi(1000) (mine, K={K1}) = {Pi1000}")
print(f"resid3(c=1000) = {r3_1000}")
print(f"published record resid3(c=1000) = 4.058, target front's own = 4.0580043")

print()
print("=" * 70)
print("c = 2560")
print("=" * 70)
K2 = 260
res2, a2 = compute_Pi(2560, K2, [180, 220, 260])
for ct0, val in res2.items():
    print(f"ct0={ct0}: Phi(0,{ct0}/2560) = {val}")
diff_hi2 = abs(res2[260] - res2[220])
diff_lo2 = abs(res2[220] - res2[180])
print(f"approach-convergence check: |S(220)-S(260)| = {diff_hi2}, |S(180)-S(220)| = {diff_lo2}")
Pi2560 = res2[260]
r3_2560 = resid3(Pi2560, 2560)
print(f"Pi(2560) (mine, K={K2}) = {Pi2560}")
print(f"resid3(c=2560) = {r3_2560}")
print(f"published record resid3(c=2560) = 4.175, target front's own = 4.1746489")

print()
print("=" * 70)
print("cross-check Pi(1000) against the 121-digit record value")
print("=" * 70)
pi1000_ref = mp.mpf("0.0377615983402126188243712025905770479904")
print("mine    :", Pi1000)
print("record  :", pi1000_ref)
print("reldiff :", abs(Pi1000 - pi1000_ref) / pi1000_ref)
