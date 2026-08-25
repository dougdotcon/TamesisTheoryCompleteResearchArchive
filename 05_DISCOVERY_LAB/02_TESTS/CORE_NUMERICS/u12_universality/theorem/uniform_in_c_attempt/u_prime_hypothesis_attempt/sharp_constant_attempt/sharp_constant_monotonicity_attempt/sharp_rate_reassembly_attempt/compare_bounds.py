# compare_bounds.py -- T5: comparison table, sharp vs non-sharp bound vs the
# true deviation |Delta_n(c)| (exact rational phi(n,c), certified phi_inf
# bracket; display in floats). Also the n->infty profile e(c) (Estagio 10's
# closed form, re-derived numerically here for display only) for context.
# Deterministic; no seed used.

import sys, time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from engine import (phi_nK_table, phi_finite, phi_inf_bracket, Q_exact,
                    ASTAR_LO, ASTAR_HI, AOLD_LO, AOLD_HI, sqrt_lo, sqrt_hi)

import mpmath as mp
mp.mp.dps = 30

t0 = time.time()
KAPPA = mp.mpf("0.280480169024586")
ASTAR = (mp.sqrt(mp.pi / 2) - mp.sqrt(mp.pi) / 2)
AOLD = 1 + mp.sqrt(mp.pi / 2)


def e_profile(c):
    """e(c) = (1/2) int_0^1 [1-(1+ct^2+c^2 t^4) e^{-ct^2}]/t^2 dt (Estagio 10)."""
    f = lambda t: (1 - (1 + c * t * t + (c * t * t) ** 2) * mp.e**(-c * t * t)) / (t * t)
    return mp.quad(f, [0, 1]) / 2


print("constants: a* = %s  (old a = %s);  a/a* = %s" %
      (mp.nstr(ASTAR, 10), mp.nstr(AOLD, 10), mp.nstr(AOLD / ASTAR, 8)))
print("kappa* = kappa_B = %s (UNCHANGED by the reassembly)" % mp.nstr(KAPPA, 12))
print("large-c overshoot of the sharp bound vs truth: a*/(sqrt(pi)/8) = 4(sqrt2-1) = %s"
      % mp.nstr(4 * (mp.sqrt(2) - 1), 10))
print()

header = (f"{'n':>5} {'c':>10} | {'n|Delta_n(c)|':>14} {'sharp n*bd':>12} "
          f"{'old n*bd':>12} | {'sharp/true':>10} {'old/sharp':>10}")
for n in [16, 64, 256]:
    tab = phi_nK_table(n)
    print(f"-- n = {n} " + "-" * (len(header) - 10))
    print(header)
    cs = [Fraction(1, 2), Fraction(1), Fraction(2284, 1000), Fraction(5),
          Fraction(10)] + [Fraction(x) for x in (25, 50, 100, 200) if x < n] \
         + [Fraction(n)]
    for c in cs:
        phin = phi_finite(n, c, tab)
        lo, hi = phi_inf_bracket(c)
        tru = float(n * max(abs(phin - lo), abs(phin - hi)))
        cf = mp.mpf(c.numerator) / c.denominator
        sharp = float(ASTAR * mp.sqrt(cf) + KAPPA)
        old = float(AOLD * mp.sqrt(cf) + KAPPA)
        print(f"{n:>5} {float(c):>10.4f} | {tru:>14.6f} {sharp:>12.6f} "
              f"{old:>12.6f} | {sharp/tru if tru else float('inf'):>10.3f} "
              f"{old/sharp:>10.3f}")
print()
print("-- n -> infinity reference: n|Delta_n| -> |e(c)| (Teorema E, Estagio 10/11) --")
print(f"{'c':>10} | {'|e(c)|':>12} {'sharp bd':>12} {'old bd':>12} | "
      f"{'sharp/|e|':>10} {'old/|e|':>10}")
for cv in [0.5, 1, 2.2838, 5, 10, 25, 100, 400, 1600]:
    c = mp.mpf(cv)
    e = abs(e_profile(c))
    sharp = ASTAR * mp.sqrt(c) + KAPPA
    old = AOLD * mp.sqrt(c) + KAPPA
    print(f"{cv:>10.4f} | {float(e):>12.6f} {float(sharp):>12.6f} "
          f"{float(old):>12.6f} | {float(sharp/e):>10.3f} {float(old/e):>10.3f}")

print()
print("-- boundary line c = n: the binding direction (bound asymptotically tight) --")
print(f"{'n':>7} | {'n|Delta_n(n)|':>14} {'sharp n*bd':>12} {'ratio':>8}")
for n in [10, 30, 100, 300, 1000, 3000]:
    phin = Q_exact(n) / n
    lo, hi = phi_inf_bracket(Fraction(n))
    tru = float(n * max(abs(phin - lo), abs(phin - hi)))
    sharp = float(ASTAR * mp.sqrt(n) + KAPPA)
    print(f"{n:>7} | {tru:>14.6f} {sharp:>12.6f} {tru/sharp:>8.4f}")

print(f"\ntime: {time.time()-t0:.1f}s")
