"""
g02_validate_anchors.py -- validate g01_family_series.py against every
published numeric anchor of record BEFORE trusting it for anything else.

Anchors (all c=1000), cited from floor_h2_b1_full_closure_attempt/ATTEMPT.md
(post-referee values) and plateau_resummation_attempt/ATTEMPT.md SS0/SS1.2:

    a_2(0)  =  520316.636488
    a_3(0)  = -180730907.6285
    a_4(0)  =  47146963944.14
    b_2(0)  = -20816.636488
    b_1(0)  =  sqrt(pi*c/2)          (exact closed form)
    Phi(0,0.002) = 0.15850015
    Phi(0,t0>=0.02) plateau = 0.0377615983402126188243712025905770479904...
      (121-digit value quoted by plateau_resummation_attempt SS3, itself
       referee-reproduced to all quoted digits)
"""
import mpmath as mp
from g01_family_series import build_a_b


def phi0(a, t0, K=None):
    if K is None:
        K = len(a) - 1
    s = mp.mpf(0)
    t0 = mp.mpf(t0)
    p = mp.mpf(1)
    for k in range(0, K + 1):
        s += a[k].at0() * p
        p *= t0
    return s


def main():
    dps = 80
    c = 1000
    K = 60
    mp.mp.dps = dps
    a, b = build_a_b(c, K, dps)

    checks = []
    checks.append(("a2(0)", a[2].at0(), mp.mpf("520316.636488")))
    checks.append(("a3(0)", a[3].at0(), mp.mpf("-180730907.6285")))
    checks.append(("a4(0)", a[4].at0(), mp.mpf("47146963944.14")))
    checks.append(("b2(0)", b[2].at0(), mp.mpf("-20816.636488")))
    checks.append(("b1(0)", b[1].at0(), mp.sqrt(mp.pi * c / 2)))

    print(f"{'quantity':10s} {'fresh value':40s} {'anchor':25s} {'rel diff':12s}")
    all_ok = True
    for name, val, anchor in checks:
        rel = abs(val - anchor) / abs(anchor)
        ok = rel < mp.mpf("1e-8")
        all_ok &= ok
        print(f"{name:10s} {mp.nstr(val, 20):40s} {mp.nstr(anchor,20):25s} {mp.nstr(rel,4):12s} {'PASS' if ok else 'FAIL'}")

    # Phi(0,0.002) anchor (needs enough K; K=60 is far more than enough at
    # such small t0 since c*t0=2 only)
    val = phi0(a, mp.mpf("0.002"))
    anchor = mp.mpf("0.15850015")
    rel = abs(val - anchor) / abs(anchor)
    ok = rel < mp.mpf("1e-6")
    all_ok &= ok
    print(f"{'Phi(0,.002)':10s} {mp.nstr(val, 20):40s} {mp.nstr(anchor,20):25s} {mp.nstr(rel,4):12s} {'PASS' if ok else 'FAIL'}")

    print()
    print("ALL ANCHORS:", "PASS" if all_ok else "FAIL -- DO NOT TRUST DOWNSTREAM RESULTS")


if __name__ == "__main__":
    main()
