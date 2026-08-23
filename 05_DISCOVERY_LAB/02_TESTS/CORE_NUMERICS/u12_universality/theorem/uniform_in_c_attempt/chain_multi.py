"""chain_multi.py -- vectorised-over-c version of chain.phi_mixed_fast.

Same recursion, same derivation; the state array is (n_c, rmax+1) so a whole
grid of c-values is advanced simultaneously.  Cross-checked against
chain.phi_mixed_exact / phi_mixed_fast in the self-test at the bottom.
"""

import numpy as np


def phi_mixed_multi(n, cs, rmax=None, dtype=np.float64):
    """phi(n,c) for every c in cs (array-like), one backward pass.

    rmax truncates the reroute-count index R.  R is stochastically dominated by
    Binomial(n, c/n), so rmax >> max(cs) makes the truncation error negligible;
    rmax=None disables truncation (cost O(n^2)).
    """
    cs = np.asarray(cs, dtype=dtype)
    q = cs / dtype(n)
    assert np.all(q >= 0) and np.all(q <= 1)
    if rmax is None:
        rmax = n
    rmax = int(min(rmax, n))
    nn = dtype(n)
    q = q[:, None]

    j = n - 1
    top = min(j, rmax)
    R = np.arange(0, top + 1, dtype=dtype)[None, :]
    P = q / nn + (1 - q) / (R + 1)
    for j in range(n - 2, -1, -1):
        top = min(j, rmax)
        R = np.arange(0, top + 1, dtype=dtype)[None, :]
        a = nn - j + R
        Psame = P[:, : top + 1]
        if top + 1 < P.shape[1]:
            Pup = P[:, 1: top + 2]
        else:
            Pup = np.concatenate([P[:, 1: top + 1], P[:, top: top + 1]], axis=1)
        P = q * (1.0 / nn + (nn - j - 1) / nn * Pup) \
            + (1 - q) * (1.0 / a + (nn - j - 1) / a * Psame)
    return np.asarray(P[:, 0], dtype=np.float64)


def default_rmax(cmax, n):
    return int(min(n, np.ceil(cmax + 14 * np.sqrt(cmax + 1) + 80)))


if __name__ == "__main__":
    from fractions import Fraction
    from chain import phi_mixed_exact, phi_mixed_fast
    print("=== self-test: chain_multi.py ===")
    bad = 0
    for n in (7, 31, 120):
        cs = [0.0, 0.5, 1.0, 3.0, 7.0, min(20.0, n), float(n)]
        cs = [c for c in cs if c <= n]
        got = phi_mixed_multi(n, cs, rmax=None)
        for c, g in zip(cs, got):
            ref = phi_mixed_fast(n, c)
            if abs(g - ref) > 1e-13:
                bad += 1
                print("  MISMATCH n=%d c=%s: %.16f vs %.16f" % (n, c, g, ref))
    print("  untruncated multi == scalar engine:", "OK" if bad == 0 else "FAIL")

    # truncation audit
    print("  truncation audit (|rmax vs 2*rmax| difference):")
    for n, cmax in [(2000, 5.0), (2000, 40.0), (8000, 100.0)]:
        cs = np.linspace(0, cmax, 9)
        r1 = default_rmax(cmax, n)
        a = phi_mixed_multi(n, cs, rmax=r1)
        b = phi_mixed_multi(n, cs, rmax=min(n, 2 * r1))
        print("    n=%-6d cmax=%-6s rmax=%-5d max|diff| = %.3e"
              % (n, cmax, r1, np.max(np.abs(a - b))))
    # exact spot check
    n = 40
    for c in (Fraction(3), Fraction(17, 2)):
        g = phi_mixed_multi(n, [float(c)], rmax=None)[0]
        e = float(phi_mixed_exact(n, c))
        print("  exact spot n=40 c=%-6s  |diff| = %.2e" % (c, abs(g - e)))
