"""
u03_validate_anchors.py -- validate u02_family_series.py against the record's own
PUBLISHED anchor numbers (quoted as plain text in the required reading,
never imported as code), before trusting it for anything new.
"""
from mpmath import mp, mpf, sqrt, pi
from u02_family_series import build_family, fam_eval, erfcx, p_eval

mp.dps = 60
c_val = mpf(1000)
K = 30  # only need low orders for these anchors

a, b, c_val, sc = build_family(c_val, K, dps=60)


def at0(fam):
    P, Q = fam
    return P[0] + Q[0] * erfcx(mpf(0) * sqrt(c_val / 2))  # s=0 => erfcx(0)=1


anchors = {
    "a2(0)": (at0(a[2]), mpf("520316.636488")),
    "a3(0)": (at0(a[3]), mpf("-180730907.6285")),
    "a4(0)": (at0(a[4]), mpf("47146963944.14")),
    "b2(0)": (at0(b[2]), mpf("-20816.636488")),
    "b1(0)": (at0(b[1]), sqrt(pi * c_val / 2)),
}

print("=" * 70)
print(f"Validation at c={c_val}, K={K}, dps=60")
print("=" * 70)
all_pass = True
for name, (val, ref) in anchors.items():
    reldiff = abs(val - ref) / abs(ref) if ref != 0 else abs(val - ref)
    ok = reldiff < mpf(10) ** -8
    all_pass &= ok
    print(f"  {name:10s} = {val}   ref={ref}   reldiff={reldiff}   {'PASS' if ok else 'FAIL'}")

# Phi(0,0.002) and plateau -- need larger K for convergence at t0~0.05-ish
# (c*t0 large). NOTE (self-caught issue S3, ATTEMPT.md): an earlier attempt
# here matched the ANCESTOR fronts' own deep target c*t0 in {230,260} (their
# choice, aimed at >=110 STABLE digits) at K=260,dps=200 -- this FAILED
# outright (truncation error ~100% relative, nowhere near converged; K~2000
# is what the ancestors report needing for that target at c=1000). This
# front does not need >=110 digits -- c*t0 in {60,80} (approach error
# ~e^{-60}~1e-26, already far more than the ~20-25 stable digits this
# front's own new results actually need) converges cleanly at a much
# smaller K=400,dps=250 (empirically probed, u04/u05 scripts) -- used here
# and throughout u06/u07/u08.
K2 = 400
a2list, b2list, c_val2, sc2 = build_family(c_val, K2, dps=250)


def Phi_at(s, t0, alist, K_use, dps_use):
    mp.dps = dps_use
    Eval = erfcx(s * sqrt(c_val2 / 2))
    total = mpf(0)
    t0p = mpf(1)
    for k in range(K_use + 1):
        total += fam_eval(alist[k], s, Eval) * t0p
        t0p *= t0
    return total


phi_small = Phi_at(mpf(0), mpf("0.002"), a2list, K2, 250)
print(f"\n  Phi(0,0.002) = {phi_small}   ref=0.15850015   "
      f"reldiff={abs(phi_small-mpf('0.15850015'))/mpf('0.15850015')}")

phi_plateau_a = Phi_at(mpf(0), mpf(60) / c_val2, a2list, K2, 250)
phi_plateau_b = Phi_at(mpf(0), mpf(80) / c_val2, a2list, K2, 250)
approach = abs(phi_plateau_a - phi_plateau_b)
ref_plateau = mpf("0.0377615983402126")
print(f"\n  Phi(0, t0=60/c) = {phi_plateau_a}")
print(f"  Phi(0, t0=80/c) = {phi_plateau_b}")
print(f"  approach |diff|   = {approach}")
print(f"  ref plateau       = {ref_plateau}")
print(f"  reldiff vs ref    = {abs(phi_plateau_b-ref_plateau)/ref_plateau}")

ok_small = abs(phi_small - mpf("0.15850015")) / mpf("0.15850015") < mpf(10) ** -6
ok_plateau = abs(phi_plateau_b - ref_plateau) / ref_plateau < mpf(10) ** -10
all_pass &= ok_small & ok_plateau
print(f"\n  Phi(0,0.002): {'PASS' if ok_small else 'FAIL'}")
print(f"  plateau:      {'PASS' if ok_plateau else 'FAIL'}")

print("\n" + ("ALL PASS" if all_pass else "SOME FAILED"))
