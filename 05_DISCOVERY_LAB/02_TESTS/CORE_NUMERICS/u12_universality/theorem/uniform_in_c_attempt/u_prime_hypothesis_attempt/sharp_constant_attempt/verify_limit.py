"""verify_limit.py -- piece 1 assembled limit, and piece 2 numerical scan.

T5. Assembled two-sided bound on r_K := M_K/sqrt(K):
      a* - (sqrt(pi)/2)/K - C/sqrt(K)  <  r_K  <  a* + 1/sqrt(K) + a*/(2K)
    with C=6 (from verify_Q_lower_bound.py's T4), checked against the EXACT
    r_K (Fraction-derived M_K, mpmath sqrt/division only for display and
    comparison) over a wide grid of K, confirming both sides hold and force
    r_K -> a*.

T6 (piece 2, NUMERICAL EVIDENCE ONLY, not a proof -- explicitly not used for
    any PROVED claim, so per the archive's discipline mpmath, not exact
    Fraction, is used here for speed: Fraction's exact big-integer
    computation of Q(n) for a dense grid of n up to several thousand is
    prohibitively slow -- Q(3000) alone via Fraction takes ~1.2s, and a
    dense scan to K=3000 would take on the order of 15 minutes; mpmath at
    50-digit precision computes the same dense grid in seconds). Scan of
    r_K for K=1..N confirming strict monotonic increase and reporting the
    gap a*-r_K alongside 1/(3 sqrt K) for comparison with the classical
    (cited, not re-derived here) next-order Ramanujan-Q asymptotic term
    -1/3.
"""

from fractions import Fraction as F
from math import factorial
import mpmath as mp

mp.mp.dps = 50


def Q_exact(n):
    total = F(0)
    prod = F(1)
    total += prod
    for j in range(1, n):
        prod *= F(n - j, n)
        total += prod
    return total


def phiK_exact(K):
    return F(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def MK_exact(K):
    return Q_exact(K + 1) - (K + 1) * phiK_exact(K)


def to_mp(fr):
    return mp.mpf(fr.numerator) / mp.mpf(fr.denominator)


if __name__ == "__main__":
    astar = mp.sqrt(mp.pi) * (1 / mp.sqrt(2) - mp.mpf(1) / 2)
    C = 6
    print(f"a* = {astar}")
    print()
    print("=== T5: two-sided bound on r_K = M_K/sqrt(K), C=6 ===")
    viol_lo = 0
    viol_hi = 0
    Ks = list(range(1, 60)) + [80, 120, 200, 400, 800, 1500, 3000]
    for K in Ks:
        MK = MK_exact(K)
        MK_mp = to_mp(MK)
        rK = MK_mp / mp.sqrt(K)
        lo = astar - (mp.sqrt(mp.pi) / 2) / K - C / mp.sqrt(K)
        hi = astar + 1 / mp.sqrt(K) + astar / (2 * K)
        ok_lo = rK > lo
        ok_hi = rK < hi
        if not ok_lo:
            viol_lo += 1
        if not ok_hi:
            viol_hi += 1
        if K <= 10 or K in (100, 1000, 3000):
            print(f"  K={K:6d}  r_K={float(rK):.6f}  lo={float(lo):.6f}({'OK' if ok_lo else 'VIOL'})"
                  f"  hi={float(hi):.6f}({'OK' if ok_hi else 'VIOL'})")
    print(f"  totals: lower-bound violations={viol_lo}, upper-bound violations={viol_hi}, over {len(Ks)} K values")
    print("  (lower bound is only informative once C/sqrt(K) < a*, i.e. roughly K>267 for C=6;"
          " for smaller K it is trivially true since RHS is negative -- still logged as OK.)")

    print()
    print("=== T6 (piece 2, numerical evidence only, mpmath 50-digit not exact Fraction -- see docstring): monotonicity scan of r_K ===")

    def Q_mp(n):
        total = mp.mpf(1)
        prod = mp.mpf(1)
        nn = mp.mpf(n)
        for j in range(1, n):
            prod *= (nn - j) / nn
            total += prod
        return total

    prev = None
    decreases = 0
    exceeds_astar = 0
    N = 3000
    rows = []
    phi = mp.mpf(1)  # phi_0
    for K in range(0, N + 1):
        if K >= 1:
            phi *= mp.mpf(2 * K) / mp.mpf(2 * K + 1)  # phi_K from phi_{K-1}: exact ratio (K!)^2 4^K/(2K+1)!
        if K == 0:
            continue
        MK = Q_mp(K + 1) - (K + 1) * phi
        rK = MK / mp.sqrt(K)
        if rK >= astar:
            exceeds_astar += 1
        if prev is not None and rK < prev:
            decreases += 1
            print(f"  DECREASE at K={K}: r_K={float(rK)} < r_{{K-1}}={float(prev)}")
        prev = rK
        rows.append((K, rK))
    print(f"  scanned K=1..{N}: {decreases} decreases (violations of monotonicity), "
          f"{exceeds_astar} values with r_K >= a*")
    print("  gap a*-r_K vs 1/(3 sqrt K) at sample K (context: classical Q(n) next-order term is -1/3):")
    for K in [10, 50, 200, 500, 1000, 2000, 3000]:
        rK = dict(rows)[K] if K in dict(rows) else None
        rK = [r for k, r in rows if k == K][0]
        gap = astar - rK
        ref = mp.mpf(1) / (3 * mp.sqrt(K))
        print(f"    K={K:5d}  gap={float(gap):.6f}  1/(3 sqrt K)={float(ref):.6f}  ratio={float(gap/ref):.4f}")
