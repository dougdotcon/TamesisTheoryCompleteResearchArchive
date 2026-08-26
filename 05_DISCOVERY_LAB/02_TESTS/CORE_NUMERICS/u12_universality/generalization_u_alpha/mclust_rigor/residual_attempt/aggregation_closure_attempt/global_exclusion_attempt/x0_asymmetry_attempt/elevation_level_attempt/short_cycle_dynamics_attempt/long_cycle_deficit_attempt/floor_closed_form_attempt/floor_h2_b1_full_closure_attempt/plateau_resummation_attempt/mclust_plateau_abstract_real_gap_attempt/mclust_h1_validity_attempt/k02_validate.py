"""
k02_validate.py -- validate k01_family_series.py against the PUBLISHED
numeric anchors quoted verbatim (as plain text, transcribed, never
imported as code) in the required-reading ATTEMPT.md documents, at
c=1000. This must pass before k01's machinery is trusted for anything
downstream (H1 profile tests, etc.) -- same discipline as every ancestor
front in this lineage.

Published anchors (from plateau_resummation_attempt/ATTEMPT.md Section 0
/ Section 1.2, and mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md
Section B.1's table of the SAME anchors), all at c=1000:

    a_2(0)  = 520316.636488
    a_3(0)  = -180730907.6285
    a_4(0)  = 47146963944.14
    b_2(0)  = -20816.636488
    b_1(0)  = sqrt(pi*1000/2)              (exact, closed form)
    Phi(0,0.002) = 0.15850015
    plateau Phi(0,t0>=0.02) = 0.0377615983402126188243712025905770479904...
"""
import os
import sys
import time
import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k01_family_series as fam

DPS = 60
K = 220
c = 1000

t0 = time.time()
a, b = fam.build_family(c, K, DPS)
print(f"build_family(c={c}, K={K}, dps={DPS}) took {time.time()-t0:.2f}s")

mp.mp.dps = DPS

checks = []

def rel(v, ref):
    return abs((v - ref) / ref) if ref != 0 else abs(v)

a2_0 = fam.f_eval(a[2], mp.mpf(0), c)
checks.append(("a2(0)", a2_0, mp.mpf('520316.636488')))

a3_0 = fam.f_eval(a[3], mp.mpf(0), c)
checks.append(("a3(0)", a3_0, mp.mpf('-180730907.6285')))

a4_0 = fam.f_eval(a[4], mp.mpf(0), c)
checks.append(("a4(0)", a4_0, mp.mpf('47146963944.14')))

b2_0 = fam.f_eval(b[2], mp.mpf(0), c)
checks.append(("b2(0)", b2_0, mp.mpf('-20816.636488')))

b1_0 = fam.f_eval(b[1], mp.mpf(0), c)
checks.append(("b1(0)", b1_0, mp.sqrt(mp.pi * c / 2)))

phi_0_002 = fam.phi_series_sum(a, mp.mpf(0), mp.mpf('0.002'), K, c)
checks.append(("Phi(0,0.002)", phi_0_002, mp.mpf('0.15850015')))

# plateau: sum out to large t0 so that e^{-c t0} is negligible; use a
# modest K/dps here (60/60) -- deliberately far below the ancestor
# fronts' >=110-digit target since this front's H1 test only needs
# ~15-20 stable digits (see ATTEMPT.md Section 3).
plateau = fam.phi_series_sum(a, mp.mpf(0), mp.mpf('0.05'), K, c)
plateau_ref = mp.mpf('0.0377615983402126188243712025905770479904')
checks.append(("Phi(0,0.05) [plateau]", plateau, plateau_ref))

print()
print(f"{'quantity':<22}{'this front value':<28}{'published anchor':<24}{'rel.diff':<12}")
all_pass = True
for name, val, ref in checks:
    d = rel(val, ref)
    ok = d < mp.mpf('1e-6')  # anchors only quoted to ~6-10 sig figs in the record
    all_pass = all_pass and ok
    print(f"{name:<22}{mp.nstr(val, 15):<28}{mp.nstr(ref, 15):<24}{mp.nstr(d, 4):<12}{'PASS' if ok else 'FAIL'}")

print()
print("ALL PASS" if all_pass else "SOME FAILED")
