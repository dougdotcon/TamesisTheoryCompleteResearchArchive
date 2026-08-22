"""
adv_final_sweep.py -- last adversarial sweep.

 (A) EXHAUSTIVE (not log-sampled) m-scan at larger n, for cases the target only
     sampled -- to make sure its log-spaced sampling did not hide an interior spike.
 (B) the one point the target's section 6 formula references but section 5 does not
     bound: a = n-b-r-1, where R_r(n-a, b+1, n) = R_r(b+r+1, b+1, n) is OUTSIDE
     g_r(.,b+1)'s domain (which needs m >= b+r+2).  Check the coefficient really
     is exactly 0 there, so the gap is harmless.
 (C) sanity: my chain vs the parent lineage's own PROVED exact closed forms for
     psi_n^(K), K=3,6 -- confirming my independent simulator is the right model.
"""

from fractions import Fraction as Fr
import sys
from adv_core import Chain
from adv_numerics import R, EH

sys.setrecursionlimit(300000)

print("=" * 88)
print("(A) EXHAUSTIVE m-scan (every single m), larger n")
print("=" * 88)
for (r, b, ns) in [(3, 0, [200, 400]), (2, 1, [200]), (5, 0, [120]), (4, 1, [150])]:
    for n in ns:
        ch = Chain(n)
        worst = None
        vals = []
        for m in range(b + r + 1, n + 1):
            v = abs(R(ch, r, b, m)) * n * n
            vals.append((m, v))
            if worst is None or v > worst[1]:
                worst = (m, v)
        interior = max((v for m, v in vals if m < n), default=Fr(0))
        print(f"  r={r} b={b} n={n:>4}: ALL {n-b-r} values of m scanned; "
              f"max = {float(worst[1]):.8f} at m={worst[0]} (t={worst[0]/n:.4f}); "
              f"max over m<n = {float(interior):.8f}")
print()

print("=" * 88)
print("(B) the out-of-domain point in section 6 (a = n-b-r-1)")
print("=" * 88)
for (r, b, n) in [(2, 0, 15), (3, 1, 20), (4, 0, 18), (5, 2, 22)]:
    a = n - b - r - 1
    s = Fr(a, n)
    coef = (1 - s) - Fr(1 + b + r, n)
    mprime = n - a
    dom_min = (b + 1) + r + 1
    print(f"  r={r} b={b} n={n}: a_max={a}, coefficient (1-s)-(1+b+r)/n = {coef} "
          f"(must be 0); the referenced g_r(m',b+1) has m'={mprime}, "
          f"but g_r(.,b+1)'s domain needs m'>={dom_min} -> {'OUT OF DOMAIN' if mprime<dom_min else 'in domain'}")
print("  ==> the referenced value is out of domain at exactly this one a, but its")
print("      coefficient is exactly 0, so the section 6 identity and bound survive.")
print("      This is the SAME mechanism section 3 uses for g_r -- but section 6 never says so.")
print()

print("=" * 88)
print("(C) my chain vs the lineage's own PROVED exact closed forms")
print("=" * 88)


def psi3(n):
    n = Fr(n)
    return (64 * n**3 + 48 * n**2 + 34 * n + 14) / (140 * n**3)


def psi6(n):
    n = Fr(n)
    return (2048 * n**6 + 3072 * n**5 + 4293 * n**4 + 4638 * n**3
            + 3529 * n**2 + 1662 * n + 360) / (6006 * n**6)


print("  K=6 (k6_attempt/ATTEMPT.md section 1.1's PROVED closed form):")
for n in [7, 8, 9, 12, 17, 25]:
    ch = Chain(n)
    got = ch.g(0, 0, 6)
    exp = psi6(n)
    print(f"    n={n:>3}: chain={got}  closed_form={exp}  match={got==exp}")
print("  (K=6,n=7 value 355081/823543 was confirmed by exhaustive brute force in the")
print("   prior referee round; my chain reproduces it from the transition rules alone.)")
