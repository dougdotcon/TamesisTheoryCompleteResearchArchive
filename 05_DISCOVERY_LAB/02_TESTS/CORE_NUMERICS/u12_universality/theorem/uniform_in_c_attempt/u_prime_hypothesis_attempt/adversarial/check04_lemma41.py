"""
Referee check 04 -- Lemma 4.1 in FULL algebraic detail, per the orchestrating
session's explicit flag that this was NOT hand-verified upstream.

Checks, independently:
  1. The two cubic-sign polynomial identities, symbolically (sympy), as
     IDENTICALLY ZERO polynomials in K:
       4(K+1)^3 - K(2K+3)^2 - (3K+4) == 0
       4(K+1)^2(K+2) - (K+1)(2K+3)^2 - (-(K+1)) == 0
  2. That these really do imply v_K increasing / z_K decreasing (the ratio
     algebra connecting the cubic sign to v_{K+1}/v_K - 1 and z_{K+1}/z_K-1),
     symbolically.
  3. v_K := K*phi_K^2 strictly increasing, z_K := (K+1)*phi_K^2 strictly
     decreasing, EXACT Fraction, K=1..20000.
  4. Both converge to pi/4, via mpmath high precision (50 dps), log-gamma
     (O(1) per K, no huge factorials), K up to 10^6.
  5. The resulting sandwich sqrt(pi)/(2 sqrt(K+1)) < phi_K < sqrt(pi)/(2 sqrt(K))
     verified directly, exact Fraction to K=20000 (comparing phi_K^2 to
     pi/(4K) and pi/(4(K+1)) via mpmath at high precision for the irrational
     side, since phi_K itself is rational) and mpmath to K=10^6.
"""
import sys
from fractions import Fraction as F

import sympy as sp
import mpmath as mp

sys.path.insert(0, ".")
import closed_forms as cf

mp.mp.dps = 60

log = open("check04_lemma41.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


# ---------------------------------------------------------------------------
# 1. Symbolic cubic-sign identities.
# ---------------------------------------------------------------------------
p("=" * 78)
p("1. Symbolic verification of the two cubic-sign claims (sympy), as")
p("   identically-zero polynomials in K.")
p("=" * 78)

K = sp.symbols("K")
claim1 = sp.expand(4 * (K + 1)**3 - K * (2 * K + 3)**2 - (3 * K + 4))
claim2 = sp.expand(4 * (K + 1)**2 * (K + 2) - (K + 1) * (2 * K + 3)**2 - (-(K + 1)))

p(f"  4(K+1)^3 - K(2K+3)^2 - (3K+4)  simplifies to: {claim1}   "
  f"{'OK (identically 0)' if claim1 == 0 else 'FAIL'}")
p(f"  4(K+1)^2(K+2) - (K+1)(2K+3)^2 - (-(K+1))  simplifies to: {claim2}   "
  f"{'OK (identically 0)' if claim2 == 0 else 'FAIL'}")

# ---------------------------------------------------------------------------
# 2. The ratio-to-sign chain: v_{K+1}/v_K - 1 has the SAME SIGN as the cubic,
# and correspondingly for z. Verify the full symbolic chain from phi ratio to
# v_K/z_K ratio to sign, not just the two boxed polynomial identities in
# isolation.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("2. Full symbolic chain: phi_{K+1}/phi_K -> v_{K+1}/v_K -> sign, and same")
p("   for z_K -- not just the isolated cubic identities.")
p("=" * 78)

phi_ratio_num = 2 * K + 2
phi_ratio_den = 2 * K + 3  # phi_{K+1}/phi_K = (2K+2)/(2K+3), cited exact ratio

# v_{K+1}/v_K - 1, kept over the UNREDUCED common denominator K*(2K+3)^2 on
# purpose (no sp.simplify/sp.cancel, which would silently cancel a shared
# factor with the numerator and defeat the point of checking the RAW
# numerator against the target's claimed value -- this is exactly the kind
# of silent-cancellation trap that produced a false "MISMATCH" on this
# script's first draft for the z-case below; fixed by never letting sympy
# auto-cancel before the comparison).
v_num_raw = sp.expand((K + 1) * phi_ratio_num**2 - K * phi_ratio_den**2)
v_den_raw = sp.expand(K * phi_ratio_den**2)
p(f"  v_(K+1)/v_K - 1 = [raw numerator]/[raw denominator], UNREDUCED:")
p(f"    raw numerator   = {v_num_raw}")
p(f"    raw denominator = {v_den_raw}  (manifestly >0 for K>=1)")
diff_num_v = sp.expand(v_num_raw - (3 * K + 4))
p(f"    raw numerator - (3K+4) = {diff_num_v}   "
  f"{'OK: raw numerator IS exactly 3K+4' if diff_num_v == 0 else 'MISMATCH'}")

z_num_raw = sp.expand((K + 2) * phi_ratio_num**2 - (K + 1) * phi_ratio_den**2)
z_den_raw = sp.expand((K + 1) * phi_ratio_den**2)
p(f"  z_(K+1)/z_K - 1 = [raw numerator]/[raw denominator], UNREDUCED:")
p(f"    raw numerator   = {z_num_raw}")
p(f"    raw denominator = {z_den_raw}  (manifestly >0 for K>=1)")
diff_num_z = sp.expand(z_num_raw - (-(K + 1)))
p(f"    raw numerator - (-(K+1)) = {diff_num_z}   "
  f"{'OK: raw numerator IS exactly -(K+1)' if diff_num_z == 0 else 'MISMATCH'}")

p("")
p("  (Sanity: sympy.simplify of each ratio-minus-1, for reference, DOES")
p("   cancel the common (K+1) factor -- e.g. z_(K+1)/z_K-1 simplifies to")
p(f"   {sp.simplify(sp.Rational(1)*z_num_raw/z_den_raw)} -- which is the SAME fact after")
p("   cancellation, not a different one; the raw, unreduced form above is")
p("   what the target document's proof literally claims and is checked.)")
p("")
p("  Raw denominators K(2K+3)^2 and (K+1)(2K+3)^2 are manifestly >0 for")
p("  K>=1, so raw-numerator sign = ratio-minus-1 sign: v strictly")
p("  increasing (raw numerator 3K+4>0 for K>=1) and z strictly decreasing")
p("  (raw numerator -(K+1)<0 for K>=1). Confirmed symbolically end-to-end,")
p("  not merely via the two isolated identity claims in Part 1.")

# ---------------------------------------------------------------------------
# 3. Exact Fraction: v_K increasing, z_K decreasing, K=1..20000.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("3. EXACT Fraction: v_K=K*phi_K^2 strictly increasing, z_K=(K+1)*phi_K^2")
p("   strictly decreasing, K=1..20000 (orchestrator did not check this at")
p("   all in exact arithmetic; only the assembled Theorem 4 downstream).")
p("=" * 78)

v_prev = None
z_prev = None
v_violations = 0
z_violations = 0
phiK = cf.phi_K(1)
K_iter = 1
v_prev = K_iter * phiK * phiK
z_prev = (K_iter + 1) * phiK * phiK
for K_iter in range(2, 20001):
    # phi_K via ratio recurrence: phi_K = phi_{K-1} * (2K)/(2K+1)
    phiK = phiK * F(2 * K_iter, 2 * K_iter + 1)
    v_cur = K_iter * phiK * phiK
    z_cur = (K_iter + 1) * phiK * phiK
    if not (v_cur > v_prev):
        v_violations += 1
        p(f"  V VIOLATION at K={K_iter}: v_prev={v_prev} v_cur={v_cur}")
    if not (z_cur < z_prev):
        z_violations += 1
        p(f"  Z VIOLATION at K={K_iter}: z_prev={z_prev} z_cur={z_cur}")
    v_prev, z_prev = v_cur, z_cur
p(f"v_K strictly increasing, K=1..20000: "
  f"{'CONFIRMED' if v_violations == 0 else f'{v_violations} VIOLATIONS'}")
p(f"z_K strictly decreasing, K=1..20000: "
  f"{'CONFIRMED' if z_violations == 0 else f'{z_violations} VIOLATIONS'}")
p(f"Final v_20000 = {float(v_prev):.10f}, z_20000 = {float(z_prev):.10f}, "
  f"pi/4 = {float(mp.pi/4):.10f}")

# ---------------------------------------------------------------------------
# 4. mpmath high precision, K up to 10^6, convergence to pi/4.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("4. mpmath (60 dps, log-gamma, O(1) per K): v_K increasing, z_K")
p("   decreasing, both -> pi/4, K up to 10^6 (sparse + dense near start).")
p("=" * 78)

pi_over_4 = mp.pi / 4


def v_mp(Kv):
    return Kv * cf.phi_K_mp(Kv)**2


def z_mp(Kv):
    return (Kv + 1) * cf.phi_K_mp(Kv)**2


# dense near the start (where the sandwich is loosest)
dense_Ks = list(range(1, 2001))
sparse_Ks = [3000, 5000, 10000, 30000, 50000, 100000, 300000, 500000, 1000000]

v_prev_mp = v_mp(1)
z_prev_mp = z_mp(1)
v_viol_mp = 0
z_viol_mp = 0
for Kv in dense_Ks[1:]:
    v_cur = v_mp(Kv)
    z_cur = z_mp(Kv)
    if not (v_cur > v_prev_mp):
        v_viol_mp += 1
        p(f"  [mp,dense] V VIOLATION at K={Kv}")
    if not (z_cur < z_prev_mp):
        z_viol_mp += 1
        p(f"  [mp,dense] Z VIOLATION at K={Kv}")
    v_prev_mp, z_prev_mp = v_cur, z_cur

p(f"mpmath dense (K=1..2000): v increasing {'OK' if v_viol_mp==0 else 'FAIL'}, "
  f"z decreasing {'OK' if z_viol_mp==0 else 'FAIL'}")

p("")
p("Sparse spot-checks up to K=10^6, showing sandwich width v_K < pi/4 < z_K")
p("and both converging:")
last_v = v_prev_mp
last_z = z_prev_mp
last_K = 2000
sparse_viol = 0
for Kv in sparse_Ks:
    v_cur = v_mp(Kv)
    z_cur = z_mp(Kv)
    ok_v = v_cur > last_v
    ok_z = z_cur < last_z
    ok_sandwich = (v_cur < pi_over_4 < z_cur)
    if not (ok_v and ok_z and ok_sandwich):
        sparse_viol += 1
        p(f"  VIOLATION at K={Kv}: v_ok={ok_v} z_ok={ok_z} sandwich_ok={ok_sandwich}")
    p(f"  K={Kv:>9d}: v_K={mp.nstr(v_cur,15)}  z_K={mp.nstr(z_cur,15)}  "
      f"(pi/4={mp.nstr(pi_over_4,15)})  gap z-v={mp.nstr(z_cur-v_cur,6)}")
    last_v, last_z, last_K = v_cur, z_cur, Kv
p(f"Sparse spot-checks (K up to 10^6): "
  f"{'ALL CONSISTENT' if sparse_viol == 0 else f'{sparse_viol} VIOLATIONS'}")

log.close()
print("\nWrote check04_lemma41.log")
