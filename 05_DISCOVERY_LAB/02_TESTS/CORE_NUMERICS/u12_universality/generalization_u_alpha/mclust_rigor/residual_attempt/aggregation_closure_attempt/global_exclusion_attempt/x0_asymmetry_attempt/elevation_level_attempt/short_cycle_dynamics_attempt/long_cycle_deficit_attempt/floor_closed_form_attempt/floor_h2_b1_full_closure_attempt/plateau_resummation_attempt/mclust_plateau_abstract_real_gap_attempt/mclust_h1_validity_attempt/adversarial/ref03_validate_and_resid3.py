import mpmath as mp
from ref02_family_series import build_series, p_eval, erfcx_safe

mp.mp.dps = 80

print("=" * 70)
print("PART 1: validation against the 7 published anchors quoted in")
print("ATTEMPT.md sec 3.2 (c=1000)")
print("=" * 70)

K = 220
a, b = build_series(1000, K)

def fam_eval0(f):
    return p_eval(f.P, 0) + p_eval(f.Q, 0) * erfcx_safe(0)

anchors = {
    "a2(0)": (fam_eval0(a[2]), mp.mpf("520316.636488")),
    "a3(0)": (fam_eval0(a[3]), mp.mpf("-180730907.6285")),
    "a4(0)": (fam_eval0(a[4]), mp.mpf("47146963944.14")),
    "b2(0)": (fam_eval0(b[2]), mp.mpf("-20816.636488")),
    "b1(0)": (fam_eval0(b[1]), mp.sqrt(mp.pi * 1000 / 2)),
}

for name, (got, want) in anchors.items():
    reldiff = abs(got - want) / abs(want)
    print(f"{name:8s} mine={got}  published~={want}  reldiff={reldiff}")

# Phi(0, t0) = sum_k a_k(0) t0^k
def Phi_at_0(t0, a_list, dps_guard=True):
    t0 = mp.mpf(t0)
    s = mp.mpf(0)
    for k, ak in enumerate(a_list):
        term = fam_eval0(ak) * t0 ** k
        s += term
    return s

phi_0002 = Phi_at_0(mp.mpf("0.002"), a)
print(f"\nPhi(0,0.002) mine={phi_0002}  published~=0.15850015  reldiff={abs(phi_0002-mp.mpf('0.15850015'))/mp.mpf('0.15850015')}")

# plateau at t0=0.05 (c*t0 = 50 -- need bigger K for full convergence, but
# published-record Pi(1000) value truncated already known; let's still probe)
phi_005 = Phi_at_0(mp.mpf("0.05"), a)
pi1000_ref = mp.mpf("0.0377615983402126188243712025905770479904")
print(f"Phi(0,0.05)  mine={phi_005}")
print(f"Pi(1000) ref (121 digit, from record) = {pi1000_ref}")
print(f"reldiff (K={K} only, expect NOT fully converged since c*t0=50 needs larger K/dps): "
      f"{abs(phi_005-pi1000_ref)/pi1000_ref}")
