"""probe_tail.py -- numerical control on the PROVED tail lemma of ATTEMPT.md SS4.

Lemma 4.1 (proved there, elementary):  for every n>=1, every c>=0, and every
integer 1 <= J <= n/2, with q := min(c/n, 1),

    phi(n,c)  <=  J/(n-J) + exp( - q J(J-1) / (2n) ).

Since the bound has no n in the first term beyond J/(n-J) <= 2J/n and J may be
taken proportional to n, it yields  sup_{c>=C0} phi(n,c) -> 0 as C0 -> infinity,
uniformly in n -- which is what SS4 uses to upgrade local uniformity to global.
This script checks the inequality against the exact chain, and reports how
sharp it is.
"""

import numpy as np
import mpmath as mp
from chain_multi import phi_mixed_multi
from ecoef import phi_inf

mp.mp.dps = 25


def tail_bound(n, c, J):
    q = min(c / n, 1.0)
    return J / (n - J) + float(mp.e ** (-mp.mpf(q) * J * (J - 1) / (2 * n)))


def best_bound(n, c):
    Js = np.arange(1, n // 2 + 1)
    vals = [tail_bound(n, c, int(J)) for J in Js]
    i = int(np.argmin(vals))
    return vals[i], int(Js[i])


if __name__ == "__main__":
    print("=== probe_tail.py : the proved uniform tail bound of SS4 ===")
    print()
    print("      n      c      phi(n,c)      best bound   J*     ratio")
    viol = 0
    for n in (50, 200, 800, 3200):
        for c in (5.0, 20.0, 50.0, 200.0, 800.0, float(n)):
            if c > n:
                continue
            v = phi_mixed_multi(n, [c], rmax=None)[0]
            b, J = best_bound(n, c)
            if v > b + 1e-12:
                viol += 1
                flag = "  <-- VIOLATION"
            else:
                flag = ""
            print("  %6d %7.1f   %.8f   %.8f   %5d  %.4f%s"
                  % (n, c, v, b, J, v / b, flag))
    print()
    print("  violations of the proved bound:", viol)
    print()
    print("--- the uniform-in-n tail: sup_{c>=C0} phi(n,c) vs the bound at c=C0 ---")
    print("  (SS4 needs only that this -> 0 as C0 -> infinity, uniformly in n)")
    print("      C0     bound at n=10^3   n=10^4   n=10^5   phi_inf(C0)")
    for C0 in (50, 200, 1000, 5000, 25000):
        row = "   %7d " % C0
        for n in (1000, 10000, 100000):
            if C0 > n:
                row += "   %-9s" % "--"
                continue
            b, J = best_bound(n, float(C0))
            row += "   %-9.5f" % b
        row += "   %.6f" % float(phi_inf(C0))
        print(row)
