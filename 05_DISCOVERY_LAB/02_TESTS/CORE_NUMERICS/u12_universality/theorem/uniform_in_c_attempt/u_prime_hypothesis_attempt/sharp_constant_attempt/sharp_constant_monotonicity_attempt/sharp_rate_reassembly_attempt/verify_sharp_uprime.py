# verify_sharp_uprime.py -- T2: independent certified re-verification of the
# ingredient this front's theorem cites from Estagio 19:
#   sharp (U'):  |phi_n^{(K)} - phi_K| <= a* sqrt(K)/n  for all 0<=K<=n
# via (i) the binding case n=K+1 (M_K = Q(K+1)-(K+1)phi_K, exact) against a
# certified rational lower bound on a* sqrt(K); (ii) interior n; (iii) the
# K=n boundary |Q(n)-n phi_n| < a* sqrt(n).  All Fraction; no floats in any
# certified comparison. Deterministic; no seed used.

import sys, time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from engine import (phi_K, Q_exact, Q_bracket_truncated, phi_nK,
                    ASTAR_LO, ASTAR_HI, sqrt_lo, sqrt_hi)

t0 = time.time()
fails = 0
print(f"a* in [{float(ASTAR_LO):.12f}, {float(ASTAR_HI):.12f}] (certified)")

# ---- T2a: M_K identity cross-check (closed-form engine vs Q route) --------
print("== T2a: T(K+1,K) = (K+1)(phi_{K+1}^{(K)} - phi_K) == Q(K+1)-(K+1)phi_K ==")
bad = 0
for K in range(1, 201):
    lhs = (K + 1) * (phi_nK(K + 1, K) - phi_K(K))
    rhs = Q_exact(K + 1) - (K + 1) * phi_K(K)
    if lhs != rhs:
        bad += 1
        print(f"  MISMATCH K={K}")
print(f"[{'PASS' if bad == 0 else 'FAIL'}] exact identity, K=1..200, {bad} mismatches")
fails += (bad != 0)

# ---- T2b: binding case M_K < a* sqrt(K), certified ------------------------
print("== T2b: M_K < a*sqrt(K), K dense 1..800 + sparse to 5000 (certified) ==")
Ks = list(range(1, 801)) + [900, 1000, 1200, 1500, 2000, 3000, 5000]
bad = 0
worst_ratio = Fraction(0)
worst_K = None
for K in Ks:
    MK = Q_exact(K + 1) - (K + 1) * phi_K(K)
    bound_lo = ASTAR_LO * sqrt_lo(Fraction(K))
    if not (Fraction(0) <= MK < bound_lo):
        bad += 1
        print(f"  VIOLATION K={K}: M_K={float(MK):.9f} vs {float(bound_lo):.9f}")
    r = MK / (ASTAR_HI * sqrt_hi(Fraction(K)))  # certified LOWER bound on ratio
    if r > worst_ratio:
        worst_ratio, worst_K = r, K
print(f"[{'PASS' if bad == 0 else 'FAIL'}] {len(Ks)} K values, {bad} violations; "
      f"max certified ratio M_K/(a*sqrt K) >= {float(worst_ratio):.6f} at K={worst_K} "
      f"[{time.time()-t0:.0f}s]")
fails += (bad != 0)

# ---- T2c: interior n ------------------------------------------------------
print("== T2c: interior n: 0 <= n(phi_n^{(K)}-phi_K) <= M_K < a*sqrt(K) ==")
bad = 0
cells = 0
for K in [1, 2, 3, 5, 10, 20, 50, 100, 300]:
    MK = Q_exact(K + 1) - (K + 1) * phi_K(K)
    bound_lo = ASTAR_LO * sqrt_lo(Fraction(K))
    prev = None
    for dn in [1, 2, 3, 5, 10, 30, 100, 300]:
        n = K + dn
        T = n * (phi_nK(n, K) - phi_K(K))
        cells += 1
        if not (Fraction(0) <= T <= MK and T < bound_lo):
            bad += 1
            print(f"  VIOLATION K={K} n={n}")
        if prev is not None and T > prev:
            bad += 1
            print(f"  MONOTONICITY VIOLATION K={K} n={n}")
        prev = T
print(f"[{'PASS' if bad == 0 else 'FAIL'}] {cells} cells, {bad} violations "
      f"[{time.time()-t0:.0f}s]")
fails += (bad != 0)

# ---- T2d: boundary K=n ----------------------------------------------------
print("== T2d: boundary |Q(n) - n phi_n| < a*sqrt(n) (phi_n^{(n)}=Q(n)/n) ==")
bad = 0
ns = list(range(1, 401)) + [500, 600, 800, 1000, 1500, 2000]
for n in ns:
    D = abs(Q_exact(n) - n * phi_K(n))
    if not D < ASTAR_LO * sqrt_lo(Fraction(n)):
        bad += 1
        print(f"  VIOLATION n={n}")
print(f"[{'PASS' if bad == 0 else 'FAIL'}] exact, {len(ns)} n values, {bad} violations "
      f"[{time.time()-t0:.0f}s]")
fails += (bad != 0)

# large n via certified truncated Q bracket
bad = 0
for n in [5000, 10000, 30000]:
    qlo, qhi = Q_bracket_truncated(n)
    npn = n * phi_K(n)
    D_hi = max(abs(qlo - npn), abs(qhi - npn))
    ok = D_hi < ASTAR_LO * sqrt_lo(Fraction(n))
    if not ok:
        bad += 1
    print(f"  n={n}: |Q-n phi_n| <= {float(D_hi):.6f} vs a*sqrt(n) >= "
          f"{float(ASTAR_LO*sqrt_lo(Fraction(n))):.6f}  [{'ok' if ok else 'VIOLATION'}]"
          f"  [{time.time()-t0:.0f}s]")
print(f"[{'PASS' if bad == 0 else 'FAIL'}] certified-truncated, 3 n values")
fails += (bad != 0)

# anchors quoted by the referee closure: n=1 -> 1/3, n=2 -> 13/30
a1 = abs(Q_exact(1) - 1 * phi_K(1))
a2 = abs(Q_exact(2) - 2 * phi_K(2))
ok = (a1 == Fraction(1, 3)) and (a2 == Fraction(13, 30))
print(f"[{'PASS' if ok else 'FAIL'}] referee anchors: n=1 gives {a1}, n=2 gives {a2}")
fails += (not ok)

print(f"\nTOTAL fails: {fails}, {time.time()-t0:.1f}s")
sys.exit(1 if fails else 0)
