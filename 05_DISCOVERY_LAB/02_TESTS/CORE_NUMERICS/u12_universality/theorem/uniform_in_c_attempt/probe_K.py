"""probe_K.py -- the uniform-in-K input needed for an EXPLICIT rate.

The soft proof of local (and global) uniformity in ATTEMPT.md SS3-SS4 needs no
rate.  An explicit O(1/n) bound uniform on [0,C] needs, in addition, a bound on
|phi_n^{(K)} - phi_K| that is uniform in K (Estagio 6/7 give the exact 1/n
coefficient c_K for each FIXED K, with no uniformity in K).  This script tests
the two candidate hypotheses of ATTEMPT.md SS6:

  (U)   |phi_n^{(K)} - phi_K| <= K / n          for all 0 <= K <= n
  (U')  |phi_n^{(K)} - phi_K| <= a sqrt(K) / n  for all 0 <= K <= n

and also monotonicity  phi_n^{(K+1)} <= phi_n^{(K)}  (which would give a second,
independent proof of the tail step of ATTEMPT.md SS4), plus the Estagio-7 check
n (phi_n^{(K)} - phi_K) -> c_K = [(K+2)phi_K - 2]/4.
"""

import numpy as np
import mpmath as mp
from chain import phi_condK_exact, phi_K
from fractions import Fraction

mp.mp.dps = 30


def phi_condK_multi(n, Ks, dtype=np.float64):
    """phi_n^{(K)} for every K in Ks simultaneously.  O(n * min(max K, n))."""
    Ks = np.asarray(Ks, dtype=dtype)[:, None]
    rmax = int(min(float(Ks.max()), n))
    nn = dtype(n)
    j = n - 1
    top = min(j, rmax)
    R = np.arange(0, top + 1, dtype=dtype)[None, :]
    rem = dtype(n - j)
    pr = np.clip((Ks - R) / rem, 0.0, 1.0)
    P = pr / nn + (1 - pr) / (R + 1)
    for j in range(n - 2, -1, -1):
        top = min(j, rmax)
        R = np.arange(0, top + 1, dtype=dtype)[None, :]
        rem = dtype(n - j)
        pr = np.clip((Ks - R) / rem, 0.0, 1.0)
        a = nn - j + R
        Psame = P[:, : top + 1]
        if top + 1 < P.shape[1]:
            Pup = P[:, 1: top + 2]
        else:
            Pup = np.concatenate([P[:, 1: top + 1], P[:, top: top + 1]], axis=1)
        P = pr * (1.0 / nn + (nn - j - 1) / nn * Pup) \
            + (1 - pr) * (1.0 / a + (nn - j - 1) / a * Psame)
    return np.asarray(P[:, 0], dtype=np.float64)


def phiK_f(K):
    return float(phi_K(int(K)))


def cK(K):
    K = int(K)
    return float((Fraction(K + 2) * phi_K(K) - 2) / 4)


if __name__ == "__main__":
    print("=== probe_K.py ===")

    print("\n--- engine cross-check: multi vs exact Fraction ---")
    bad = 0
    for n in (9, 25, 60):
        Ks = list(range(0, n + 1, max(1, n // 7)))
        got = phi_condK_multi(n, Ks)
        for K, g in zip(Ks, got):
            e = float(phi_condK_exact(n, K))
            if abs(g - e) > 1e-12:
                bad += 1
                print("  MISMATCH n=%d K=%d %.16f %.16f" % (n, K, g, e))
    print("  OK" if bad == 0 else "  FAIL")

    print("\n--- Estagio-7 check: n (phi_n^(K) - phi_K) -> c_K = [(K+2)phi_K-2]/4 ---")
    print("      K      n=500        n=2000       n=8000        c_K (exact)")
    for K in [1, 2, 3, 6, 10, 20, 50]:
        row = "  %5d " % K
        for n in (500, 2000, 8000):
            v = phi_condK_multi(n, [K])[0]
            row += "  %+11.7f" % (n * (v - phiK_f(K)))
        row += "   %+.7f" % cK(K)
        print(row)

    print("\n--- (U)/(U') scan: max over n of  n|phi_n^(K)-phi_K| / K  and  / sqrt(K) ---")
    print("     K    argmax-n   n|d|        n|d|/K     n|d|/sqrt(K)   c_K/sqrt(K)")
    for K in [1, 2, 3, 5, 8, 12, 20, 32, 50, 80, 128, 200, 320, 512]:
        best = (0.0, None)
        pk = phiK_f(K)
        ns = sorted(set([K + 1, K + 2, K + 3, K + 5, K + 8, K + 13, 2 * K, 3 * K,
                         5 * K, 10 * K, 25 * K, 100 * K, 4 * K + 40, 2000, 8000]))
        ns = [n for n in ns if n >= K + 1 and n <= 20000]
        vals = {}
        for n in ns:
            v = phi_condK_multi(n, [K])[0]
            s = n * abs(v - pk)
            vals[n] = s
            if s > best[0]:
                best = (s, n)
        s, nb = best
        print("  %5d   %7d   %9.5f   %8.5f   %10.5f    %8.5f"
              % (K, nb, s, s / K, s / np.sqrt(K), cK(K) / np.sqrt(K)))

    print("\n--- monotonicity  phi_n^{(K+1)} <= phi_n^{(K)} ?  (exhaustive in K) ---")
    worst = None
    for n in [5, 12, 30, 80, 200, 600]:
        Ks = list(range(0, n + 1))
        v = phi_condK_multi(n, Ks)
        d = np.diff(v)
        mx = float(d.max())
        print("  n=%-5d  max_K [phi_n^(K+1) - phi_n^(K)] = %+.3e  (<=0 means monotone)"
              % (n, mx))
        if worst is None or mx > worst:
            worst = mx
    print("  worst over all n scanned: %+.3e" % worst)
    # exact-arithmetic confirmation at small n
    print("  exact-Fraction confirmation, n=2..9, all K:")
    allok = True
    for n in range(2, 10):
        vs = [phi_condK_exact(n, K) for K in range(n + 1)]
        ok = all(vs[K + 1] <= vs[K] for K in range(n))
        allok &= ok
        print("    n=%d strictly-decreasing-in-K: %s" % (n, ok))
    print("  exact verdict:", "monotone in every case" if allok else "COUNTEREXAMPLE")
