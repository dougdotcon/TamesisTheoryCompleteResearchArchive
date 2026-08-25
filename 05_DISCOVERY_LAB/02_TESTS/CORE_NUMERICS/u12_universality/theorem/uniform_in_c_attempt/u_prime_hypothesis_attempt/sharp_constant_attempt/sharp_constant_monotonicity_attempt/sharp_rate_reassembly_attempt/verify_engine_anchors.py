# verify_engine_anchors.py -- T1: validate the fresh exact engine against
# (a) brute-force enumeration from Definition 4 (no closed form anywhere),
# (b) archive anchors quoted in prose (exact rationals).
# Deterministic; no seed used.

import sys, time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from engine import (phi_K, Q_exact, phi_nK, phi_nK_bruteforce, psiR,
                    phi_finite, phi_nK_table, phi_inf_bracket)

t0 = time.time()
fails = 0
checks = 0


def report(name, ok, detail=""):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


# ---- T1a: brute force vs closed form -------------------------------------
print("== T1a: closed form vs brute-force enumeration (exact Fraction) ==")
cases = ([(4, K) for K in range(5)] + [(5, K) for K in range(6)]
         + [(6, K) for K in range(5)] + [(7, 0), (7, 1), (7, 2)])
for (n, K) in cases:
    bf = phi_nK_bruteforce(n, K)
    cf = phi_nK(n, K)
    report(f"phi_{n}^({K})", bf == cf, f"= {cf} (bf {bf})  [{time.time()-t0:.0f}s]")

# ---- T1b: prose anchors ---------------------------------------------------
print("== T1b: archive anchors (prose-quoted exact values) ==")
for n in range(2, 51):
    ok = phi_nK(n, 1) == Fraction(2, 3) + Fraction(1, 3 * n * n)
    if not ok:
        report(f"phi_n^(1) closed form n={n}", False)
        break
else:
    report("phi_n^(1) = 2/3 + 1/(3n^2), n=2..50", True)

for n in range(2, 51):
    ok = psiR(n, 1) == Fraction(1, 2) + Fraction(1, 2 * n)
    if not ok:
        report(f"psiR n={n}", False)
        break
else:
    report("psi_n^(1),R = 1/2 + 1/(2n), n=2..50", True)

# phi_n^{(n-1)} = Q(n)/n  -- closed-form engine vs independent Q code
ok = all(phi_nK(n, n - 1) == Q_exact(n) / n for n in range(2, 41))
report("phi_n^(n-1) = Q(n)/n, n=2..40 (closed form vs independent Q)", ok)

report("phi_7^(6) = 355081/823543",
       phi_nK(7, 6) == Fraction(355081, 823543))

anchors = {0: Fraction(1), 1: Fraction(2, 3), 2: Fraction(8, 15),
           3: Fraction(16, 35), 4: Fraction(128, 315)}
report("phi_K anchors K=0..4", all(phi_K(K) == v for K, v in anchors.items()))

report("Q(2)=3/2, Q(3)=17/9",
       Q_exact(2) == Fraction(3, 2) and Q_exact(3) == Fraction(17, 9))

# ---- T1c: mixture endpoint identities ------------------------------------
print("== T1c: mixture phi(n,c) endpoints ==")
for n in range(4, 13):
    tab = phi_nK_table(n)
    ok0 = phi_finite(n, Fraction(0), tab) == 1
    okn = phi_finite(n, Fraction(n), tab) == Q_exact(n) / n
    report(f"phi({n},0)=1 and phi({n},{n})=Q({n})/{n}", ok0 and okn)

# ---- T1d: phi_inf bracket sanity ----------------------------------------
print("== T1d: phi_inf bracket internal consistency ==")
# series path vs tail path must agree near the crossover c=40
for c in [Fraction(39), Fraction(40)]:
    lo1, hi1 = phi_inf_bracket(c)
    report(f"phi_inf({c}) bracket sane", lo1 < hi1 and hi1 - lo1 < Fraction(1, 10**9),
           f"width={float(hi1-lo1):.2e}")
c = Fraction(41)
lo2, hi2 = phi_inf_bracket(c)
from engine import _alt_series_bracket
lo3, hi3 = _alt_series_bracket(c, 0)
report("phi_inf(41): tail-formula bracket contains series bracket midpoint",
       lo2 <= (lo3 + hi3) / 2 <= hi2,
       f"tail=[{float(lo2):.12f},{float(hi2):.12f}] series_mid={float((lo3+hi3)/2):.12f}")

print(f"\nTOTAL: {checks} checks, {fails} failures, {time.time()-t0:.1f}s")
sys.exit(1 if fails else 0)
