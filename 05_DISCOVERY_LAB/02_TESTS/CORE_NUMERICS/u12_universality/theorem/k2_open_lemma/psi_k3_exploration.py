"""
Secondary, exploratory numerics (not a proof): checks whether psi_n^{(K)} (the
generic-point quantity of the Reduction Lemma, ATTEMPT.md SS2) continues its O(1/n)
convergence to phi_K at K=3, beyond the K=1 (proved, SS3) and K=2 (proved, SS4-5) cases
that this document closes analytically. This is exhaustive brute-force enumeration
(exact rational arithmetic), not a coupling proof -- offered as honest supporting
evidence for the plausibility of the general-K conjecture in ATTEMPT.md SS7, nothing
more. n=8 takes ~35s; n=9+ was not attempted (cost grows like n! * n^3).
"""
from psi_bruteforce import psi_n_K
from fractions import Fraction as F
import time
import sys

phi3 = F(4 ** 3 * (6) ** 2, 5040)  # 4^K (K!)^2 / (2K+1)! at K=3 = 64*36/5040 = 16/35
assert phi3 == F(16, 35)

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print(f"phi_3 = {phi3} = {float(phi3):.8f}  (Lemma 2, THEOREM.md SS5.2)")
    for n in range(4, nmax + 1):
        t0 = time.time()
        val = psi_n_K(n, 3, reference="generic")
        dev = val - phi3
        print(f"n={n} psi_n^(3)={val}={float(val):.8f}  dev={float(dev):.8f}  "
              f"n*dev={float(n*dev):.6f}  time={time.time()-t0:.1f}s")
        sys.stdout.flush()
