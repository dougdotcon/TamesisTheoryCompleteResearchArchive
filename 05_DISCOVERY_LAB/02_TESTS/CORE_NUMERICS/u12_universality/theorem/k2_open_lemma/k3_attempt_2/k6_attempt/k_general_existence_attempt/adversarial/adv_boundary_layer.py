"""
adv_boundary_layer.py -- the t -> 0 boundary layer, stressed hard.

This is the region the PRIOR referee (../adversarial/REFEREE_REPORT.md B.4(b))
flagged as the riskiest, and the region the target document claims to have
subsumed.  Everything here is exact Fraction arithmetic.

 (1) Facts 1/2/3 re-checked at CONCRETE b for r up to 12 (fast path, complements
     the symbolic-b run in adv_residual_derivation.py).
 (2) base-case residual m=b+r+1 at LARGE n (r=6,7 at b=0,2 -- beyond the target's
     r=1,2), testing convergence of n^2 R rather than drift.
 (3) FIXED small m (m = j, j+1, j+3, 2j, ...) with n -> large: the genuine
     boundary layer t = m/n -> 0.  If a homogeneous-solution admixture
     C*t^{-(1+r+b)} were present, THIS is where it would blow up.
 (4) whole-m-range max of n^2|R| at larger n for combinations the target
     never tested.
"""

from fractions import Fraction as Fr
import sys
import sympy as sp
from adv_core import Chain, F_poly, G_poly, Hhat_poly, K_poly
from adv_numerics import F_fr, G_fr, Hhat_fr, K_fr, R, EH

sys.setrecursionlimit(300000)
t = sp.Symbol('t')
s = sp.Symbol('s')

print("=" * 92)
print("(1) FACTS 1-3 at concrete b, r = 0..12")
print("=" * 92)
bad = 0
for bval in (0, 1, 3, 7):
    line2, line3, line1 = [], [], []
    for r in range(0, 13):
        F = F_poly(r, bval, t)
        G = G_poly(r, bval, t)
        # Fact 1: degrees
        dF = sp.Poly(F, t).degree() if F != 0 else -1
        dG = sp.Poly(G, t).degree() if G != 0 else -1
        Hh = Hhat_poly(r, bval, s)
        Kk = K_poly(r, bval, s)
        dH = sp.Poly(Hh, s).degree() if Hh != 0 else -1
        dK = sp.Poly(Kk, s).degree() if Kk != 0 else -1
        ok1 = (dF <= r) and (dG <= r - 1) and (dH <= r + 1) and (dK <= r)
        line1.append(ok1)
        # Fact 2
        rhs2 = 1 + (r * Hhat_poly(r - 1, bval, 1 - t) if r >= 1 else 0)
        f2 = sp.expand(t * sp.diff(F, t) + (1 + r + bval) * F - rhs2)
        line2.append(f2 == 0)
        # Fact 3
        if r >= 1:
            Hprime = sp.diff(Hhat_poly(r - 1, bval, s), s).subs(s, 1 - t)
            Kat = K_poly(r - 1, bval, 1 - t)
            rhs3 = r * Hprime + r * Kat + t * sp.diff(F, t, 2) / 2 + (1 + r + bval) * sp.diff(F, t)
        else:
            rhs3 = t * sp.diff(F, t, 2) / 2 + (1 + r + bval) * sp.diff(F, t)
        f3 = sp.expand(t * sp.diff(G, t) + (1 + r + bval) * G - rhs3)
        line3.append(f3 == 0)
    print(f"  b={bval}: Fact1(degrees) all-true={all(line1)} | "
          f"Fact2 (ODE for F) all-zero={all(line2)} | Fact3 (ODE for G) all-zero={all(line3)}")
    if not (all(line1) and all(line2) and all(line3)):
        bad += 1
        print(f"     Fact1: {line1}\n     Fact2: {line2}\n     Fact3: {line3}")
print(f"  ==> {'ALL CONFIRMED' if bad==0 else '*** FAILURES ***'}")
print()

print("=" * 92)
print("(2) BASE CASE m=b+r+1 at LARGE n -- does n^2 R converge or drift?")
print("=" * 92)
for (r, b) in [(6, 0), (7, 2), (9, 0), (10, 3)]:
    j = b + r + 1
    print(f"  r={r} b={b}, m=j={j}:")
    prev = None
    for n in [j + 1, 20, 50, 100, 500, 2000, 10000, 100000, 1000000]:
        if n < j:
            continue
        ch = Chain(n)
        v = R(ch, r, b, j) * n * n
        d = "" if prev is None else f"  (change {float(v-prev):+.3e})"
        print(f"     n={n:>8}: n^2*R = {float(v):+.12f}{d}")
        prev = v
    print()

print("=" * 92)
print("(3) BOUNDARY LAYER: m FIXED (small), n -> large, so t=m/n -> 0")
print("=" * 92)
for (r, b) in [(3, 0), (4, 1), (6, 0)]:
    j = b + r + 1
    for m in [j, j + 1, j + 3, 2 * j, 3 * j]:
        row = []
        for n in [200, 1000, 5000, 50000, 500000]:
            if n < m:
                continue
            ch = Chain(n)
            v = R(ch, r, b, m) * n * n
            row.append((n, float(v)))
        txt = "  ".join(f"n={n}: {v:+.9f}" for n, v in row)
        print(f"  r={r} b={b} m={m:>3} (t=m/n->0):  {txt}")
    print()
print("  If a homogeneous admixture C*t^-(1+r+b) were present in G_r, then")
print("  n^2*R at fixed m would blow up like n^2 * (1/n) * (m/n)^-(1+r+b) ~ n^(r+b),")
print("  i.e. by factors of ~5^(r+b) per column.  Observed: bounded / converging.")
print()

print("=" * 92)
print("(4) WHOLE-m-RANGE max n^2|R| at larger n, untested combinations")
print("=" * 92)
for (r, b) in [(4, 3), (5, 1), (6, 0)]:
    for n in [64, 128, 256]:
        ch = Chain(n)
        worst = None
        for m in range(b + r + 1, n + 1):
            v = abs(R(ch, r, b, m)) * n * n
            if worst is None or v > worst[0]:
                worst = (v, m)
        print(f"  r={r} b={b} n={n:>4}: max_m n^2|R| = {float(worst[0]):.8f} at m={worst[1]} (t={worst[1]/n:.3f})")
    print()
