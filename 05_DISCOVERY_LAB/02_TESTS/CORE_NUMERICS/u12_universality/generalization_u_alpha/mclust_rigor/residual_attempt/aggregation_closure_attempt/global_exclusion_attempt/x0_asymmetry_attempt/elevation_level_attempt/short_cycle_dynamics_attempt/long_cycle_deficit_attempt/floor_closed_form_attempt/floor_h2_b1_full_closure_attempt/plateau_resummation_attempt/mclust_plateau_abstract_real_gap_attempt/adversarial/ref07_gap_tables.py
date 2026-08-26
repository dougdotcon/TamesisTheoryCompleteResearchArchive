#!/usr/bin/env python3
"""
Independent recomputation of the gap tables T1/T2 cited by the target
document's Sec A.2, using phi_real values transcribed as plain data
(verbatim) from floor_closed_form_attempt/ATTEMPT.md Sec 2 (T1) and Sec 4
(T2 point-level + cluster-robust re-measurement) -- NOT from any .py file,
per the mandate. Pi_abstract = 0.0377615983402126188243712025905770479904
is the record's own established, referee-confirmed, and (in this review)
independently re-derived plateau constant at c=1000 (see ref04_grid.py).
"""
import mpmath as mp

mp.mp.dps = 30
Pi_abs = mp.mpf('0.0377615983402126188243712025905770479904')

def gap_pct(phi_real):
    phi_real = mp.mpf(phi_real)
    return float((Pi_abs - phi_real) / phi_real * 100)

print("=== Table T1 (absolute-ell bins, floor_closed_form_attempt Sec 2) ===")
T1 = [
    ("[500,1000)",   0.011, "0.0298"),
    ("[2000,4000)",  0.046, "0.0265"),
    ("[4000,8000)",  0.092, "0.0253"),
    ("[8000,16384)", 0.186, "0.0258"),
    ("[16384,32768)",0.375, "0.0266"),
    ("[32768,65536)",0.750, "0.0273"),
]
t1_gaps = []
for label, t0mid, phireal in T1:
    g = gap_pct(phireal)
    t1_gaps.append(g)
    print(f"  {label:16s} t0~{t0mid:.3f}  phi_real={phireal}  gap%={g:.2f}%")

print("\n=== Table T2 composite (relative-L/n bins, floor_closed_form_attempt Sec 4) ===")
# point-level phi_real values (Sec 4 fine sub-binning table), except the
# 2 point-level bins that did NOT survive cluster-robust replication
# (per floor_closed_form_attempt's OWN finding), replaced by the
# cluster-robust re-measurement values from the SAME document's Sec 4
# cluster-robustness table.
T2 = [
    (0.046, "0.02781"),
    (0.091, "0.02716"),
    (0.186, "0.02747"),
    (0.312, "0.02673"),
    (0.438, "0.02722"),   # point-level -- SURVIVES cluster replication (kept)
    (0.562, "0.02781"),
    (0.688, "0.02692"),
    (0.812, "0.02637"),   # cluster-robust value (point-level 0.02866 did NOT survive)
    (0.938, "0.02747"),   # cluster-robust value (point-level 0.02577 did NOT survive)
]
t2_gaps = []
t0s = []
for t0mid, phireal in T2:
    g = gap_pct(phireal)
    t2_gaps.append(g)
    t0s.append(t0mid)
    print(f"  t0~{t0mid:.3f}  phi_real={phireal}  gap%={g:.2f}%")

mean_gap = sum(t2_gaps) / len(t2_gaps)
print(f"\nT2 composite: mean gap = {mean_gap:.3f}%, range [{min(t2_gaps):.2f}%, {max(t2_gaps):.2f}%], "
      f"spread = {max(t2_gaps)-min(t2_gaps):.3f} pp")

# Pearson correlation r(gap%, t0)
n = len(t2_gaps)
mean_t0 = sum(t0s) / n
mean_g = mean_gap
cov = sum((t0s[i]-mean_t0)*(t2_gaps[i]-mean_g) for i in range(n))
var_t0 = sum((t-mean_t0)**2 for t in t0s)
var_g = sum((g-mean_g)**2 for g in t2_gaps)
r = cov / (var_t0**0.5 * var_g**0.5)
print(f"Pearson r(gap%, t0) = {r:.4f}  (n={n})")

print("\n=== Cross-check against target document's claimed values ===")
print("Target claims: mean=38.78%, range=[35.78%,43.20%], spread=7.41pp, r=0.331")
print(f"My recompute:  mean={mean_gap:.2f}%, range=[{min(t2_gaps):.2f}%,{max(t2_gaps):.2f}%], "
      f"spread={max(t2_gaps)-min(t2_gaps):.2f}pp, r={r:.3f}")

print("\n=== T1 summary ===")
print(f"T1 gaps: {[f'{g:.2f}%' for g in t1_gaps]}")
print(f"T1 range: [{min(t1_gaps):.2f}%, {max(t1_gaps):.2f}%]  (peak at t0~0.092: {t1_gaps[2]:.2f}%)")
