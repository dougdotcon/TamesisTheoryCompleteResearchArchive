"""
adv_numerics.py -- Part A item 6: FRESH, independent numerical measurement of

        R_r(m,b,n) = g_r(m,b) - F_r(t,b) - (1/n) G_r(t,b),   t = m/n
        eps^h_r(a,b,n) = h_r(a,b) - Hhat_r(s,b) - (1/n) K_r(s,b),  s = a/n

at (r,b,n,m) combinations the target document did NOT test.  Target tested
r=1..5, b in {0,1}, n<=1600 (and, for h_r, r=1,2,3 at b=0 only).  Here:

  (a) base-case boundary m=b+r+1 for r=6 and r=7, at b=0 and b=2;
  (b) large b (b=5) with r=3, full m-range;
  (c) n^2 * R_r at fixed t, growing n, for combinations never tested
      (r=4,b=3 ; r=6,b=0 ; r=3,b=5), to test for log n growth.

Exact Fraction arithmetic throughout.  No floats in any exact claim.
"""

from fractions import Fraction as Fr
from adv_core import Chain, _fall
import math
import sys

sys.setrecursionlimit(200000)


def F_fr(r, b, t):
    tot = Fr(0)
    for k in range(0, r + 1):
        den = 1
        for i in range(1, k + 2):
            den *= (r + b + i)
        tot += Fr(_fall(r, k), den) * (t ** k)
    return tot


def G_fr(r, b, t):
    tot = Fr(0)
    for k in range(0, r):
        den = 1
        for i in range(1, k + 3):
            den *= (r + b + i)
        tot += Fr(math.comb(k + 2, 2) * _fall(r, k + 1), den) * (t ** k)
    return tot


def Hhat_fr(r, b, s):
    return (1 - s) * F_fr(r, b + 1, 1 - s)


def K_fr(r, b, s):
    out = Fr(1)
    if r >= 1:
        out += r * Hhat_fr(r - 1, b + 1, s)
    out += (1 - s) * G_fr(r, b + 1, 1 - s)
    out -= (1 + b + r) * F_fr(r, b + 1, 1 - s)
    return out


def R(chain, r, b, m):
    n = chain.n
    t = Fr(m, n)
    return chain.g_r(m, b, r) - F_fr(r, b, t) - Fr(1, n) * G_fr(r, b, t)


def EH(chain, r, b, a):
    n = chain.n
    s = Fr(a, n)
    return chain.h_r(a, b, r) - Hhat_fr(r, b, s) - Fr(1, n) * K_fr(r, b, s)


def fmt(x):
    return f"{float(x):+.10f}"


if __name__ == "__main__":
    print("=" * 90)
    print("(a) BASE-CASE BOUNDARY  m = b+r+1  -- r=6,7 at b=0 and b=2 (target checked r=1,2 only)")
    print("=" * 90)
    print(f"{'r':>2} {'b':>2} {'n':>5} {'m':>3}   {'R_r(m,b,n)  (exact)':>34}  {'n^2 * R':>16}")
    for (r, b) in [(1, 0), (2, 0), (6, 0), (6, 2), (7, 0), (7, 2)]:
        m0 = b + r + 1
        vals = []
        for n in [m0, m0 + 1, m0 + 3, m0 + 7, m0 + 15, m0 + 31, 2 * m0 + 40, 3 * m0 + 60]:
            if n < m0:
                continue
            ch = Chain(n)
            val = R(ch, r, b, m0)
            vals.append((n, val))
            print(f"{r:>2} {b:>2} {n:>5} {m0:>3}   {str(val):>34}  {fmt(val*n*n):>16}")
        # is n^2 R constant?
        cs = set(v * n * n for n, v in vals)
        print(f"    --> n^2*R_r at the base case is {'CONSTANT = ' + str(cs.pop()) if len(cs)==1 else 'NOT constant; values: ' + str(sorted(set(str(v*n*n) for n,v in vals)))}")
        print()

    print("=" * 90)
    print("(b) LARGE b: r=3, b=5, full m-range  (target's numerics were b in {0,1})")
    print("=" * 90)
    for n in [20, 40, 80, 160]:
        ch = Chain(n)
        r, b = 3, 5
        worst = None
        for m in range(b + r + 1, n + 1):
            v = abs(R(ch, r, b, m)) * n * n
            if worst is None or v > worst[0]:
                worst = (v, m)
        print(f"  n={n:>4}:  max_m n^2|R_3(m,5,n)| = {float(worst[0]):.8f}  attained at m={worst[1]}"
              f"   (t={worst[1]/n:.3f})")
    print()

    print("=" * 90)
    print("(c) n^2 * R_r AT FIXED t, GROWING n -- log-n test, combos not in the target doc")
    print("=" * 90)
    for (r, b, tnum, tden) in [(4, 3, 1, 1), (4, 3, 1, 2), (6, 0, 1, 1), (3, 5, 1, 4), (5, 2, 2, 3)]:
        print(f"  r={r}, b={b}, t={tnum}/{tden}:")
        prev = None
        for n in [24, 48, 96, 192, 384]:
            m = n * tnum // tden
            if m < b + r + 1 or m > n:
                continue
            ch = Chain(n)
            v = R(ch, r, b, m) * n * n
            ratio = "" if prev is None else f"   (ratio to prev: {float(v)/float(prev):.6f})"
            print(f"     n={n:>4} m={m:>4}: n^2*R = {float(v):+.10f}{ratio}")
            prev = v
        print()

    print("=" * 90)
    print("(c2) WHOLE-RANGE UNIFORMITY for r=6,b=0 and r=4,b=3 (never tested by the target)")
    print("=" * 90)
    for (r, b) in [(6, 0), (4, 3)]:
        for n in [16, 32, 64, 128]:
            if n < b + r + 2:
                continue
            ch = Chain(n)
            worst = None
            for m in range(b + r + 1, n + 1):
                v = abs(R(ch, r, b, m)) * n * n
                if worst is None or v > worst[0]:
                    worst = (v, m)
            print(f"  r={r} b={b} n={n:>4}: max_m n^2|R| = {float(worst[0]):.8f} at m={worst[1]}"
                  f" (t={worst[1]/n:.3f})")
        print()

    print("=" * 90)
    print("(d) h_r RESIDUAL, including a=0, for r=4,5 at b=0,2 (target checked r=1,2,3 b=0)")
    print("=" * 90)
    for (r, b) in [(4, 0), (4, 2), (5, 0)]:
        for n in [20, 40, 80]:
            if n <= b + r + 1:
                continue
            ch = Chain(n)
            worst = None
            for a in range(0, n - b - r):
                v = abs(EH(ch, r, b, a)) * n * n
                if worst is None or v > worst[0]:
                    worst = (v, a)
            print(f"  r={r} b={b} n={n:>4}: max_a n^2|eps^h| = {float(worst[0]):.8f} at a={worst[1]}")
        print()
