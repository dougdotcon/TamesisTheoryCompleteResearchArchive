"""
cross_checks.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

Three independent corroborations of the central result, plus the two remaining
quantitative questions.

  X1  D*_r(0) = H_r(1,0) against the 1/n^2 coefficient of the FIVE exact
      psi_n^{(K)} closed forms already PROVED elsewhere in this lineage by a
      COMPLETELY DIFFERENT method (wave 6's exact telescoping-sum ladder,
      k3_attempt_2/ATTEMPT.md SS4/SS5/SS7.1), each itself brute-force verified
      there.  Transcribed here by hand from those statements.

  X2  the finite-n supremum:  is  sup_{m,n} n^2|R_r(m,b,n)|  itself Theta(r^{3/2}),
      or does the finite-n excess over D*_r(b) grow?

  X3  the improved (rigorous) bound D'_r(b) pushed to larger r, to pin its
      exponential rate.

Exact arithmetic throughout; floats for display only.
"""

import sys
from fractions import Fraction as Fr
from functools import lru_cache
from math import log
import core as C
import loose_bound as LB

sys.setrecursionlimit(100000)

print("=" * 98)
print("X1.  D*_r(0) = H_r(1,0)  vs  the 1/n^2 coefficient of the already-PROVED")
print("     exact psi_n^{(K)} closed forms (wave 5 / wave 6, different method).")
print("=" * 98)
# psi_n^{(K)} = g_K(n,0), transcribed verbatim from the sources named above.
known = {
    1: ("(4n+1)/(6n)                        [wave 5, PROVED]", Fr(0)),
    2: ("(8n^2+4n+1)/(15n^2)                [wave 5, PROVED]", Fr(1, 15)),
    3: ("(64n^3+48n^2+25n+6)/(140n^3)       [k3_attempt_2 SS5, PROVED]", Fr(5, 28)),
    4: ("(128n^4+128n^3+103n^2+52n+12)/(315n^4)   [k3_attempt_2 SS7.1]", Fr(103, 315)),
    5: ("(1024n^5+1280n^4+1405n^3+1105n^2+538n+120)/(2772n^5) [SS7.1]", Fr(1405, 2772)),
}
allok = True
for K in sorted(known):
    src, coef = known[K]
    mine = C.H(K, 0).eval(Fr(1))
    formula = Fr(K * (3 * K + 1), 32) * C.phi(K) - Fr(K, 12)
    ok = (mine == coef == formula)
    allok &= ok
    print("   K=%d  1/n^2 coeff of psi_n^{(K)} = %-10s   H_K(1,0) = %-10s   "
          "K(3K+1)phi_K/32 - K/12 = %-10s   %s"
          % (K, coef, mine, formula, "MATCH" if ok else "MISMATCH"))
    print("        source: psi_n^{(K)} = %s" % src)
print("   five independent exact matches:", allok)

# and an extra: re-derive the 1/n^2 coefficient directly from my own exact Chain,
# by exact rational polynomial fitting in 1/n, validated OUT OF SAMPLE.
print()
print("   X1b.  Same coefficient extracted independently from MY OWN exact chain, by")
print("         exact rational interpolation in 1/n, validated out-of-sample.")


def extract_coeffs(r, b, deg):
    """Exact interpolation of g_r(n,b) as a polynomial in 1/n of degree deg."""
    ns = [b + r + 1 + i for i in range(deg + 1)]
    ys = []
    for n in ns:
        ys.append(C.Chain(n).g(r, n, b))
    xs = [Fr(1, n) for n in ns]

    def pmul(p, q):
        out = [Fr(0)] * (len(p) + len(q) - 1)
        for i2, a in enumerate(p):
            for j2, bb in enumerate(q):
                out[i2 + j2] += a * bb
        return out

    coeffs = [Fr(0)] * (deg + 1)
    for i in range(deg + 1):
        basis = [Fr(1)]
        den = Fr(1)
        for j in range(deg + 1):
            if j == i:
                continue
            basis = pmul(basis, [-xs[j], Fr(1)])
            den *= (xs[i] - xs[j])
        for k2 in range(len(basis)):
            coeffs[k2] += ys[i] * basis[k2] / den
    return coeffs


for r in range(1, 8):
    deg = r + 1          # psi_n^{(r)} is a polynomial of degree r in 1/n
    co = extract_coeffs(r, 0, deg)
    # out-of-sample validation
    oos = True
    for n in range(2 * r + 8, 2 * r + 13):
        val = sum(co[k] * Fr(1, n) ** k for k in range(len(co)))
        if val != C.Chain(n).g(r, n, 0):
            oos = False
    print("      r=%d : interpolated 1/n^2 coeff = %-14s  H_r(1,0) = %-14s  match=%s  "
          "out-of-sample(5 fresh n)=%s"
          % (r, co[2], C.H(r, 0).eval(Fr(1)), co[2] == C.H(r, 0).eval(Fr(1)), oos))

print()
print("=" * 98)
print("X2.  Is the FINITE-n supremum itself Theta(r^{3/2})?")
print("     sup over ALL valid n (scanned to NMAX) and ALL valid m, vs D*_r(b).")
print("=" * 98)
NMAX = 70
print("   %3s %3s | %-16s %-16s %-8s %-14s" %
      ("r", "b", "sup n^2|R_r|", "D*_r(b)", "ratio", "argmax (n,m)"))
for b in (0, 1):
    for r in list(range(2, 15)):
        best = Fr(0)
        arg = None
        for n in range(b + r + 1, NMAX + 1):
            ch = C.Chain(n)
            for m in range(b + r + 1, n + 1):
                v = abs(C.R_resid(ch, r, m, b)) * n * n
                if v > best:
                    best, arg = v, (n, m)
        ds = C.H(r, b).eval(Fr(1))
        print("   %3d %3d | %-16.9f %-16.9f %-8.4f (%d,%d)"
              % (r, b, float(best), float(ds), float(best / ds) if ds else float("nan"),
                 arg[0], arg[1]))

print()
print("=" * 98)
print("X3.  The improved rigorous bound D'_r(b), pushed further -- its growth law.")
print("=" * 98)


@lru_cache(maxsize=None)
def Dimp(r, b):
    if r == 0:
        return Fr(0)
    return (r * Cimp(r - 1, b) + LB.A(r, b)) / Fr(r + b + 1)


@lru_cache(maxsize=None)
def Cimp(r, b):
    if r == 0:
        return Fr(0)
    return LB.B(r, b) + Fr(r, b + r + 1) * Cimp(r - 1, b + 1) + Dimp(r, b + 1)


print("   %4s | %-14s %-12s %-14s %-14s %-14s"
      % ("r", "D'_r(0)", "ratio", "D'_r/(9/8)^r", "D*_r(0)", "D'/D*"))
prev = None
RG = int(sys.argv[1]) if len(sys.argv) > 1 else 45
for r in range(2, RG + 1):
    di = Dimp(r, 0)
    dt = C.H(r, 0).eval(Fr(1))
    if r % 3 == 0 or r < 8:
        print("   %4d | %-14.6g %-12.6f %-14.6g %-14.6g %-14.6g"
              % (r, float(di), float(di / prev) if prev else float("nan"),
                 float(di) / (9.0 / 8.0) ** r, float(dt), float(di / dt)))
    prev = di
print()
print("   (the 'ratio' column is the geometric growth rate of the improved bound;")
print("    contrast the ORIGINAL bound, whose ratio grows like r -- factorial.)")
