"""
a05_sec25_table_and_slope_precision_checks.py

(A) Independent spot-check of the target's Sec 2.5 illustrative table
    (sup_{z>=y} h_eps(z) vs y, at eps=0.1 and eps=1/sqrt(1000)) -- a
    non-load-bearing sanity table (the actual proof does not depend on
    these specific numbers), included for completeness.

(B) Precision check of the target's prose characterization in Sec 4.3:
    "the rigorous slope (~3.4-3.5) is roughly 5-7x the empirically
    measured slope" -- least-squares slope of the front's OWN reported
    rigorous-bound table (Sec 4.3), compared against the asymptotic
    slope e*M and against the empirical slopes.
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 30

def R(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2)*mp.erfc(z/mp.sqrt(2))*mp.e**(z*z/2)

def h(z, eps):
    z = mp.mpf(z); eps = mp.mpf(eps)
    return abs(1-eps*z)*R(z)

def sup_over_zgey(y, eps, extra_range=2000, npts=4000):
    zs = np.linspace(float(y), float(y)+extra_range, npts)
    best = 0.0
    for zf in zs:
        v = float(h(zf, eps))
        if v > best:
            best = v
    return best

print("="*70)
print("PART A: Sec 2.5 illustrative table spot-check (non-load-bearing)")
print("="*70)
rows = [
    (0.1, [1,5,20,100,1000,10000], [0.590,0.0975,0.0976,0.0980,0.0993,0.0999]),
    (float(1/mp.sqrt(1000)), [1,5,20,100,1000,10000], [0.635,0.162,0.0292,0.0296,0.0309,0.0315]),
]
for eps, ys, targets in rows:
    print(f"\neps={eps:.6f}:")
    for y0, tgt in zip(ys, targets):
        v = sup_over_zgey(y0, eps)
        reldiff = abs(v-tgt)/tgt if tgt else float('nan')
        print(f"  y={y0:>6}: this referee sup~={v:.4f}   target reported={tgt:.4f}   reldiff={reldiff*100:.1f}%")
print()
print("Reading: values are grid-resolution-sensitive (both sides use a finite")
print("numerical scan, not a closed-form sup), agree to within a few percent,")
print("and both independently confirm the QUALITATIVE claim (no growth in y,")
print("settling near a small constant near eps) -- this table is illustrative")
print("only; no proof in the target document depends on its exact digits.")

print()
print("="*70)
print("PART B: Sec 4.3 slope characterization precision check")
print("="*70)
y = np.array([0.5,1,2,3,4,5,6])
rig100 = np.array([3,5,9,13,16,20,24])
rig1000 = np.array([3,5,8,12,15,19,22])
emp100_slope, emp1000_slope = 0.4895, 0.7552

A = np.vstack([y, np.ones(len(y))]).T
m100, b100 = np.linalg.lstsq(A, rig100, rcond=None)[0]
m1000, b1000 = np.linalg.lstsq(A, rig1000, rcond=None)[0]

M100 = float(mp.sqrt(mp.pi/2)) + 0.1
M1000 = float(mp.sqrt(mp.pi/2)) + 1/np.sqrt(1000)
asym_slope100 = np.e*M100
asym_slope1000 = np.e*M1000

print(f"c=100:  least-squares slope of the front's OWN rigorous-bound table = {m100:.4f}")
print(f"        asymptotic slope e*M (M=sqrt(pi/2)+eps)                    = {asym_slope100:.4f}")
print(f"        target's prose characterization: '~3.4-3.5'                -> {'UNDERSELLS' if m100>3.5 else 'consistent'}")
print(f"        ratio to empirical slope {emp100_slope}: {m100/emp100_slope:.3f}x (asymptotic: {asym_slope100/emp100_slope:.3f}x)")
print()
print(f"c=1000: least-squares slope of the front's OWN rigorous-bound table = {m1000:.4f}")
print(f"        asymptotic slope e*M                                       = {asym_slope1000:.4f}")
print(f"        target's prose characterization: '~3.4-3.5'                -> {'consistent' if 3.4<=m1000<=3.5 else 'borderline'}")
print(f"        ratio to empirical slope {emp1000_slope}: {m1000/emp1000_slope:.3f}x (asymptotic: {asym_slope1000/emp1000_slope:.3f}x)")
print()
print("Reading: the target's prose says 'rigorous slope ~3.4-3.5' and 'roughly")
print("5-7x' the empirical slope. The c=1000 figure matches (~3.47-3.49). The")
print("c=100 figure (least-squares slope of the front's own table: ~3.77;")
print(f"asymptotic e*M: ~{asym_slope100:.2f}) is measurably above the stated '~3.4-3.5'")
print("range, and the resulting ratio spread is closer to ~4.6x-7.7x than the")
print("stated '5-7x'. This is an approximate prose characterization, not a")
print("number used in any subsequent derivation or in the domination check")
print("(which is verified per-point, exactly, in a03/a04) -- LOW severity,")
print("descriptive imprecision only.")
