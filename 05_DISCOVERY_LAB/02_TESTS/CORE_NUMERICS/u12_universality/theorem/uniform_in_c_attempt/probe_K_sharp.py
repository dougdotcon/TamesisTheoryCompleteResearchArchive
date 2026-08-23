"""probe_K_sharp.py -- the sharp constant in hypothesis (U').

The scan in probe_K.py finds that  max_n  n |phi_n^{(K)} - phi_K|  is always
attained at the smallest admissible n, n = K+1 (all-but-one point rerouted),
and that the ratio to sqrt(K) increases in K.  ATTEMPT.md SS6 predicts the
limit of that ratio is

    a* = sqrt(pi) (1/sqrt2 - 1/2) = 0.3670779...

because phi_{K+1}^{(K)} ~ sqrt(pi/(2(K+1)))  (Ramanujan-Q / random-mapping
value, all but one point rerouted) while phi_K ~ sqrt(pi)/(2 sqrt K).
This script pushes K far enough to see that.
"""

import numpy as np
import mpmath as mp
from probe_K import phi_condK_multi, phiK_f

mp.mp.dps = 30

if __name__ == "__main__":
    astar = float(mp.sqrt(mp.pi) * (1 / mp.sqrt(2) - mp.mpf(1) / 2))
    print("=== probe_K_sharp.py ===")
    print("predicted a* = sqrt(pi)(1/sqrt2 - 1/2) = %.10f" % astar)
    print()
    print("      K       n=K+1: n|d|/sqrt(K)     n=K+2       n=2K       n=10K")
    for K in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        pk = phiK_f(K)
        out = []
        for n in (K + 1, K + 2, 2 * K, 10 * K):
            if n > 200000:
                out.append(float('nan'))
                continue
            v = phi_condK_multi(n, [K])[0]
            out.append(n * abs(v - pk) / np.sqrt(K))
        print("  %7d      %.7f          %.7f   %.7f  %.7f"
              % (K, out[0], out[1], out[2], out[3]))
    print()
    print("--- so the candidate uniform bound is  |phi_n^(K)-phi_K| <= a sqrt(K)/n ---")
    print("--- with any a >= a* = %.7f ; the scan below reports the true max ---" % astar)
    worst = 0.0
    where = None
    for K in list(range(0, 60)) + [80, 120, 200, 400, 800, 1600, 3200]:
        pk = phiK_f(K)
        if K == 0:
            continue
        ns = sorted(set([K + 1, K + 2, K + 3, K + 4, K + 6, K + 10, K + 20,
                         2 * K, 3 * K, 6 * K, 20 * K, 100 * K]))
        ns = [n for n in ns if K + 1 <= n <= 100000]
        for n in ns:
            v = phi_condK_multi(n, [K])[0]
            r = n * abs(v - pk) / np.sqrt(K)
            if r > worst:
                worst, where = r, (K, n)
    print("  max over the scan of  n|phi_n^(K)-phi_K| / sqrt(K)  =  %.7f  at (K,n)=%s"
          % (worst, where))
