"""extrapolate.py -- Richardson extrapolation of the two sequences that should
both converge to  a* = sqrt(pi)(1/sqrt2 - 1/2) = 0.3670872119...

  (i)  max_n n|phi_n^{(K)} - phi_K| / sqrt(K)      (probe_K_sharp.log, in K)
  (ii) sqrt(n) * sup_{c in [0,n]} |Delta_n(c)|     (probe_large_c.log, in n)

Both are expected to approach a* with an O(x^{-1/2}) correction, so the
two-point Richardson  L = (v2*s2 - v1*s1)/(s2 - s1),  s = 1/sqrt(x)  applies.
Input values are transcribed from the two logs; nothing is recomputed here.
"""

import mpmath as mp

mp.mp.dps = 25
astar = mp.sqrt(mp.pi) * (1 / mp.sqrt(2) - mp.mpf(1) / 2)


def rich(x1, v1, x2, v2):
    s1, s2 = 1 / mp.sqrt(x1), 1 / mp.sqrt(x2)
    return (mp.mpf(v2) * s1 - mp.mpf(v1) * s2) / (s1 - s2)


if __name__ == "__main__":
    print("a* = sqrt(pi)(1/sqrt2 - 1/2) =", mp.nstr(astar, 12))
    print()
    print("(i) probe_K_sharp.log, n=K+1 column:")
    seqK = [(1024, '0.3568427'), (2048, '0.3598077'), (4096, '0.3619220'),
            (8192, '0.3634260'), (16384, '0.3644938')]
    for (x1, v1), (x2, v2) in zip(seqK, seqK[1:]):
        print("    K=%-6d,%-6d -> %s" % (x1, x2, mp.nstr(rich(x1, v1, x2, v2), 8)))
    print()
    print("(ii) probe_large_c.log, sqrt(n)*sup_{[0,n]}|Delta_n|:")
    seqN = [(250, '0.346416'), (500, '0.352386'), (1000, '0.356650'),
            (2000, '0.359686'), (4000, '0.361843')]
    for (x1, v1), (x2, v2) in zip(seqN, seqN[1:]):
        print("    n=%-6d,%-6d -> %s" % (x1, x2, mp.nstr(rich(x1, v1, x2, v2), 8)))
