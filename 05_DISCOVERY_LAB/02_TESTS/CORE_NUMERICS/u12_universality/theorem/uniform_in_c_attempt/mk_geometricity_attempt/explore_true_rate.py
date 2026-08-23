"""
Purely informational / exploratory (NOT part of the proof -- Route A's proof
only needs the crude geometric upper bound already established and verified
in compute_MK.py / R3). This script asks: what does the TRUE growth rate of
M_K^psi look like, given how much slack compute_MK.py found (ratio
bound/M_K^psi already ~1.3e2 at K=20 and exploding)?

Hypothesis suggested by the K=1..300 data: M_K^psi = Theta(sqrt(K)), the
SAME order as the already-PROVED n->oo limit K*phi_K/4 (Estagio 6). Checked
here by extending to larger K (mpmath, dps=80, to avoid huge exact Fraction
factorials) and tracking M_K^psi / sqrt(K) and M_K^psi - K*phi_K/4.

This does not change the verdict of Route A (which only needs *a* finite
geometric bound, already proved and verified) -- it only characterizes, for
honesty, how far from sharp that bound is, exactly as
error_constant_growth_attempt/ATTEMPT.md did for D_r(b) vs D*_r(b).
"""
import mpmath as mp
from math import comb

mp.mp.dps = 80


def MK_psi_mpmath(K):
    n = K + 1
    total = mp.mpf(0)
    for j in range(0, K + 1):
        w = mp.mpf(comb(2 * K + 1, K - j))
        prod = mp.mpf(1)
        for i in range(1, j + 1):
            prod *= mp.mpf(n + i) / mp.mpf(n)
        total += w * n * (prod - 1)
    phiK = mp.mpf(4)**K * mp.factorial(K)**2 / mp.factorial(2 * K + 1)
    return phiK * total / mp.mpf(4)**K


def phi_K_mpmath(K):
    return mp.mpf(4)**K * mp.factorial(K)**2 / mp.factorial(2 * K + 1) / mp.mpf(4)**K \
        if False else mp.mpf(4)**K * mp.factorial(K)**2 / mp.factorial(2 * K + 1)


print("=== exploratory: M_K^psi vs sqrt(K) and vs the n->oo limit K*phi_K/4 ===\n")
print(f"{'K':>6} {'M_K^psi':>14} {'M_K^psi/sqrt(K)':>18} {'K*phi_K/4':>14} "
      f"{'M_K^psi/(K*phi_K/4)':>20} {'M_K^psi - K*phi_K/4':>20}")

Ks = [10, 30, 100, 300, 1000, 3000]
# NOTE: an initial run also attempted K=10000, 30000, but the naive
# recomputation of math.comb(2K+1, K-j) from scratch for every one of the
# K+1 values of j (each a multi-thousand-digit integer at that range) made
# it too slow to finish within a reasonable wall-clock budget; it was killed
# and the range was capped at K=3000 (already enough to see the trend
# clearly -- this whole script is informational context, not part of the
# proof, so no further optimization was pursued).
for K in Ks:
    m = MK_psi_mpmath(K)
    phiK = phi_K_mpmath(K)
    lim = K * phiK / 4
    print(f"{K:>6} {float(m):>14.6f} {float(m/mp.sqrt(K)):>18.6f} {float(lim):>14.6f} "
          f"{float(m/lim):>20.6f} {float(m-lim):>20.6f}")

print("\n=== sqrt(pi)/8 landmark (Estagio 7 leading constant of c_K, K*phi_K/4 ~ sqrt(pi*K)/8) ===")
print(f"sqrt(pi)/8 = {float(mp.sqrt(mp.pi)/8):.10f}")
for K in Ks:
    m = MK_psi_mpmath(K)
    print(f"K={K:>6}: M_K^psi/sqrt(K) = {float(m/mp.sqrt(K)):.6f}  "
          f"(vs sqrt(pi)/8 = {float(mp.sqrt(mp.pi)/8):.6f})")
