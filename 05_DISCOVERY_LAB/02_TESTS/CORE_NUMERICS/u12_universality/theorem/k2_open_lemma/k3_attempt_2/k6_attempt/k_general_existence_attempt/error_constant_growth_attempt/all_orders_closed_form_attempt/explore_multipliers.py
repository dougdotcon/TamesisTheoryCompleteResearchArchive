"""
explore_multipliers.py -- read off the order-p coefficients of Phi[p]_r(t,b)
and strip the shared falling-factorial / denominator-product structure, to
expose the "multiplier" M_p(k) at each order p.

Conjectured shape (matching orders p=0,1,2 which are already PROVED):

    [t^k] Phi[p]_r(t,b) = M_p(k) * r!/(r-k-p)! * 1/prod_{i=1}^{k+p+1}(r+b+i)

so    M_p(k) = coeff * prod_{i=1}^{k+p+1}(r+b+i) * (r-k-p)!/r!
and the whole point is that this must come out INDEPENDENT of r and b.
"""

import sys
from fractions import Fraction
from core import Ladder, _ff, _denom

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
RMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 16
BMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 5

L = Ladder(Fraction(0))

print("=" * 78)
print("STAGE 1 -- is the multiplier M_p(k) independent of r and b?")
print("=" * 78)
mult = {}      # (p,k) -> Fraction
consistent = True
count = 0
for p in range(0, PMAX + 1):
    for r in range(0, RMAX + 1):
        for d in range(0, BMAX + 1):
            b = Fraction(d)
            P = L.phi(p, r, d)
            for k in range(0, r - p + 1):
                num = _ff(r, k, p)
                if num == 0:
                    continue
                m = P.coeff(k) * Fraction(_denom(k, p, r, b), num)
                count += 1
                key = (p, k)
                if key in mult:
                    if mult[key] != m:
                        consistent = False
                        print("  INCONSISTENT at p=%d k=%d r=%d b=%d: %s vs %s"
                              % (p, k, r, d, m, mult[key]))
                else:
                    mult[key] = m
print("  checked %d (p,k,r,b) instances; r,b-independence holds: %s"
      % (count, consistent))

print()
print("=" * 78)
print("STAGE 2 -- also check the top-end vanishing (k > r-p  =>  coeff 0)")
print("=" * 78)
bad = 0
for p in range(0, PMAX + 1):
    for r in range(0, RMAX + 1):
        for d in range(0, BMAX + 1):
            P = L.phi(p, r, d)
            for k in range(max(0, r - p + 1), r + 4):
                if P.coeff(k) != 0:
                    bad += 1
print("  nonzero coefficients above degree r-p:", bad)

print()
print("=" * 78)
print("STAGE 3 -- the multiplier table M_p(k)")
print("=" * 78)
KMAX = min(10, RMAX - PMAX)
hdr = "  p\\k |" + "".join("%10d" % k for k in range(0, KMAX + 1))
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for p in range(0, PMAX + 1):
    row = "  %3d |" % p
    for k in range(0, KMAX + 1):
        v = mult.get((p, k))
        row += "%10s" % (v if v is not None else "-")
    print(row)

print()
print("  known ground truth:  M_0(k)=1,  M_1(k)=C(k+2,2),  "
      "M_2(k)=(3k+8)(k+1)(k+2)(k+3)/24")
ok = True
for k in range(0, KMAX + 1):
    if mult.get((0, k)) != 1:
        ok = False
    if mult.get((1, k)) != Fraction((k + 1) * (k + 2), 2):
        ok = False
    if mult.get((2, k)) != Fraction((3 * k + 8) * (k + 1) * (k + 2) * (k + 3), 24):
        ok = False
print("  orders 0,1,2 agree with the PROVED multipliers:", ok)

print()
print("=" * 78)
print("STAGE 4 -- normalised multiplier  N_p(k) := M_p(k)*(2p)!/(k+1)_{2p}")
print("     [(k+1)_{2p} = (k+1)(k+2)...(k+2p)]   -- limit as k->inf should be")
print("     (2p-1)!! if the leading coefficient of M_p is 1/(2^p p!)")
print("=" * 78)


def rising(k, j):
    acc = 1
    for i in range(j):
        acc *= (k + 1 + i)
    return acc


import math
for p in range(0, PMAX + 1):
    row = []
    for k in range(0, KMAX + 1):
        v = mult.get((p, k))
        if v is None:
            row.append("-")
            continue
        N = v * Fraction(math.factorial(2 * p), rising(k, 2 * p))
        row.append(str(N))
    dd = math.prod(range(2 * p - 1, 0, -2)) if p > 0 else 1
    print("  p=%d  (2p-1)!!=%-5d : %s" % (p, dd, ", ".join(row)))
