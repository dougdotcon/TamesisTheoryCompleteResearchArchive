import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

mp.mp.dps = 100

def fam_eval0(f):
    return p_eval(f.P, 0) + p_eval(f.Q, 0) * erfcx_safe(0)

def Phi_at_0(t0, a_list):
    t0 = mp.mpf(t0)
    s = mp.mpf(0)
    for k, ak in enumerate(a_list):
        s += fam_eval0(ak) * t0 ** k
    return s

R0 = mp.sqrt(mp.pi / 2)
psi2_0 = mp.mpf(-2)

def resid3(Pi_c, c):
    eps = 1 / mp.sqrt(mp.mpf(c))
    return (Pi_c - eps * R0 - eps**2 * psi2_0) / eps**3

def run(c, K, ct0_list):
    print(f"--- c={c}, K={K} ---")
    a, b = build_series(c, K)
    vals = {}
    for ct0 in ct0_list:
        t0 = mp.mpf(ct0) / c
        v = Phi_at_0(t0, a)
        vals[ct0] = v
        print(f"  ct0={ct0}: Phi(0,t0={t0}) = {v}")
    keys = sorted(vals.keys())
    for i in range(len(keys) - 1):
        d = abs(vals[keys[i+1]] - vals[keys[i]])
        print(f"  |S({keys[i+1]})-S({keys[i]})| = {d}")
    Pi_c = vals[keys[-1]]
    r3 = resid3(Pi_c, c)
    print(f"  Pi({c}) (mine) = {Pi_c}")
    print(f"  resid3({c}) = {r3}")
    return Pi_c, r3

print("=" * 70)
print("c=1000, moderate ct0 (should already be in plateau, e^-ct0 tiny)")
print("=" * 70)
Pi1000, r3_1000 = run(1000, 200, [30, 40, 50])

print()
print("=" * 70)
print("c=2560")
print("=" * 70)
Pi2560, r3_2560 = run(2560, 200, [30, 40, 50])

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"resid3(c=1000): mine={r3_1000}   record=4.058   target-front's-own=4.0580043")
print(f"resid3(c=2560): mine={r3_2560}   record=4.175   target-front's-own=4.1746489")

pi1000_ref = mp.mpf("0.0377615983402126188243712025905770479904")
print(f"\nPi(1000) mine = {Pi1000}")
print(f"Pi(1000) ref  = {pi1000_ref}")
print(f"reldiff       = {abs(Pi1000-pi1000_ref)/pi1000_ref}")
