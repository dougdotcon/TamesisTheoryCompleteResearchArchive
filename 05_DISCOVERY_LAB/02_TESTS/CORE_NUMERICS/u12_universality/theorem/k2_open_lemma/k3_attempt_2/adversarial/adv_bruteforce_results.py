"""
Consolidated, reproducible run of every fresh brute-force check performed in this
adversarial review (task items 4, 5, 6, 7), using adv_bruteforce.py (this review's
own, independently-coded exhaustive enumeration -- see that file's docstring for how
it differs from psi_bruteforce_ref.py / phi_bruteforce_full.py). Prints PASS/FAIL for
every comparison against ATTEMPT.md's claimed closed forms.

Run with: python3 adv_bruteforce_results.py   (takes ~20s total; the K=3 n=8 point is
the slowest single item at ~12s).
"""
from fractions import Fraction as F
import time
from adv_bruteforce import psi_generic, psi_rerouted, phi_raw

PASS, FAIL = [], []


def check(label, got, want):
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}: {label}  got={got} want={want}")
    (PASS if ok else FAIL).append(label)


t_start = time.time()

print("=" * 70)
print("K=1: psi_generic (target 2/3+1/(6n)), psi_rerouted (target 1/2+1/(2n))")
print("=" * 70)
for nn in range(2, 8):
    check(f"K=1 n={nn} psi_generic", psi_generic(nn, 1), F(4 * nn + 1, 6 * nn))
    check(f"K=1 n={nn} psi_rerouted", psi_rerouted(nn, 1), F(nn + 1, 2 * nn))

print()
print("=" * 70)
print("K=2: psi_generic (target 8/15+4/(15n)+1/(15n^2)), "
      "psi_rerouted (target (5n+2)(n+1)/(12n^2))")
print("=" * 70)
for nn in range(3, 8):
    check(f"K=2 n={nn} psi_generic", psi_generic(nn, 2),
          F(8 * nn**2 + 4 * nn + 1, 15 * nn**2))
    check(f"K=2 n={nn} psi_rerouted", psi_rerouted(nn, 2),
          F((5 * nn + 2) * (nn + 1), 12 * nn**2))

print()
print("=" * 70)
print("K=3 (THE MAIN TARGET): psi_generic (target (64n^3+48n^2+25n+6)/(140n^3))")
print("    task explicitly asked for n=5,6,7 -- also ran n=4 and n=8 for extra margin")
print("=" * 70)
for nn in [4, 5, 6, 7, 8]:
    t0 = time.time()
    v = psi_generic(nn, 3)
    dt = time.time() - t0
    check(f"K=3 n={nn} psi_generic ({dt:.1f}s)", v,
          F(64 * nn**3 + 48 * nn**2 + 25 * nn + 6, 140 * nn**3))

print()
print("=" * 70)
print("K=3: psi_rerouted (target (22n^3+39n^2+23n+6)/(60n^3))")
print("=" * 70)
for nn in [4, 5, 6, 7]:
    check(f"K=3 n={nn} psi_rerouted", psi_rerouted(nn, 3),
          F(22 * nn**3 + 39 * nn**2 + 23 * nn + 6, 60 * nn**3))

print()
print("=" * 70)
print("K=3: phi_raw -- FRESH independent brute force of the RAW Definition-4 average")
print("     (no Lemma A, no generic/rerouted split used at all in this computation)")
print("     target (32n^4+5n^3+77n^2+46n+12)/(70n^4)")
print("=" * 70)
for nn in [4, 5, 6, 7]:
    check(f"K=3 n={nn} phi_raw", phi_raw(nn, 3),
          F(32 * nn**4 + 5 * nn**3 + 77 * nn**2 + 46 * nn + 12, 70 * nn**4))

print()
print("=" * 70)
print("K=4 bonus spot-check (target (128n^4+128n^3+103n^2+52n+12)/(315n^4))")
print("=" * 70)
for nn in [5, 6]:
    check(f"K=4 n={nn} psi_generic", psi_generic(nn, 4),
          F(128 * nn**4 + 128 * nn**3 + 103 * nn**2 + 52 * nn + 12, 315 * nn**4))

print()
print("=" * 70)
print("K=5 bonus spot-check (target (1024n^5+1280n^4+1405n^3+1105n^2+538n+120)/(2772n^5))")
print("=" * 70)
for nn in [6]:
    check(f"K=5 n={nn} psi_generic", psi_generic(nn, 5),
          F(1024 * nn**5 + 1280 * nn**4 + 1405 * nn**3 + 1105 * nn**2 + 538 * nn + 120,
            2772 * nn**5))

print()
print("=" * 70)
print(f"TOTAL: {len(PASS)} PASS, {len(FAIL)} FAIL   (elapsed {time.time()-t_start:.1f}s)")
print("=" * 70)
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print("  -", f)
else:
    print("ALL CHECKS PASSED.")
