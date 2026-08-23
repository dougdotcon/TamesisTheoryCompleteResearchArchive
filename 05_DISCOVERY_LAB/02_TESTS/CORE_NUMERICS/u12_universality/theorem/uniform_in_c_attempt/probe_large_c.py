"""probe_large_c.py -- question 2 of the brief: c growing with n.

Three things:
  (A) the joint regime c = gamma*n, gamma in (0,1] fixed:
        predicted  sqrt(n) phi(n, gamma n) -> sqrt( pi / (2 gamma (2-gamma)) ),
        hence      phi(n,c)/phi_inf(c)     -> sqrt( 2/(2-gamma) )  > 1,
      i.e. the limit law survives in ABSOLUTE terms (both sides are Theta(n^-1/2))
      but fails by a constant factor in RELATIVE terms.
  (B) the global sup over the whole admissible range c in [0,n].
  (C) where the global sup is attained, and its order in n.
"""

import numpy as np
import mpmath as mp
from chain_multi import phi_mixed_multi
from ecoef import phi_inf

mp.mp.dps = 30


def pred_gamma(gamma):
    return float(mp.sqrt(mp.pi / (2 * mp.mpf(gamma) * (2 - mp.mpf(gamma)))))


if __name__ == "__main__":
    print("=== probe_large_c.py ===")
    print()
    print("--- (A) c = gamma*n :  sqrt(n) * phi(n, gamma n)  ->  sqrt(pi/(2 g (2-g))) ---")
    gammas = [0.05, 0.1, 0.25, 0.5, 0.75, 1.0]
    ns = [250, 500, 1000, 2000, 4000]
    print("   gamma " + "".join("   n=%-9d" % n for n in ns) + "     predicted")
    for g in gammas:
        row = "  %6.2f " % g
        for n in ns:
            c = g * n
            v = phi_mixed_multi(n, [c], rmax=None)[0]
            row += "  %-10.6f" % (np.sqrt(n) * v)
        row += "   %.6f" % pred_gamma(g)
        print(row)

    print()
    print("--- (A') ratio phi(n,gamma n) / phi_inf(gamma n)  ->  sqrt(2/(2-gamma)) ---")
    print("   gamma " + "".join("   n=%-9d" % n for n in ns) + "     predicted")
    for g in gammas:
        row = "  %6.2f " % g
        for n in ns:
            c = g * n
            v = phi_mixed_multi(n, [c], rmax=None)[0]
            row += "  %-10.6f" % (v / float(phi_inf(c)))
        row += "   %.6f" % float(mp.sqrt(2 / (2 - mp.mpf(g))))
        print(row)

    print()
    print("--- (A'') absolute difference at c = gamma n: sqrt(n)*|phi - phi_inf| ---")
    print("   gamma " + "".join("   n=%-9d" % n for n in ns) + "     predicted")
    for g in gammas:
        row = "  %6.2f " % g
        for n in ns:
            c = g * n
            v = phi_mixed_multi(n, [c], rmax=None)[0]
            row += "  %-10.6f" % (np.sqrt(n) * abs(v - float(phi_inf(c))))
        pred = abs(pred_gamma(g) - float(mp.sqrt(mp.pi) / 2 / mp.sqrt(g)))
        row += "   %.6f" % pred
        print(row)

    print()
    print("--- (B)/(C) global sup over c in [0,n] ---")
    print("       n    sup|Delta_n|    argmax c*   c*/n    sqrt(n)*sup   n*sup")
    for n in [125, 250, 500, 1000, 2000, 4000]:
        # log-ish grid dense near the top of the range plus a linear sweep
        cs = np.unique(np.concatenate([
            np.linspace(0.0, min(30.0, n), 61),
            np.geomspace(max(1e-3, 1.0), float(n), 220),
            np.linspace(0.5 * n, float(n), 60)]))
        cs = cs[cs <= n]
        v = phi_mixed_multi(n, cs, rmax=None)
        d = v - np.array([float(phi_inf(c)) for c in cs])
        i = int(np.argmax(np.abs(d)))
        print("    %5d   %.8f   %10.3f  %6.3f   %.6f    %.4f"
              % (n, abs(d[i]), cs[i], cs[i] / n, np.sqrt(n) * abs(d[i]), n * abs(d[i])))

    print()
    print("--- (C') the c -> infinity tail at fixed n (q = min(c/n,1) convention) ---")
    print("   phi(n,c) is constant = phi(n,n) for c >= n; phi_inf(c) -> 0, so")
    print("   sup_{c>=n} |Delta_n| = phi(n,n) exactly.")
    print("       n     phi(n,n)     sqrt(n)*phi(n,n)   sqrt(pi/2)=%.6f"
          % float(mp.sqrt(mp.pi / 2)))
    for n in [100, 400, 1600, 6400]:
        v = phi_mixed_multi(n, [float(n)], rmax=None)[0]
        print("    %6d   %.8f   %.6f" % (n, v, np.sqrt(n) * v))
