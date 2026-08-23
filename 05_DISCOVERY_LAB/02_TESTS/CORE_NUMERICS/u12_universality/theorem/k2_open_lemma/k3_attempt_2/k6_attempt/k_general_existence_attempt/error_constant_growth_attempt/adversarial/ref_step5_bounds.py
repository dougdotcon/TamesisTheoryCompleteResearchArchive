"""
STEP 5 -- Sec 6 (the two looseness mechanisms), Lemma 7, Proposition 6, and the
finite-n supremum S_r(b).

Lemma 7 re-proof (mine, prose in REFEREE_REPORT.md Part 4):
  coefficient of s^j in p(1-s) = (-1)^j sum_{k>=j} c_k C(k,j);  if all c_k >= 0
  every contribution to that coefficient shares the sign (-1)^j, so
  ||p(1-.)|| = sum_j sum_{k>=j} c_k C(k,j) = sum_k c_k 2^k = p(2).
  And if sign(q_j) = (-1)^j then the s^j coefficient of (1-s)q(s) is q_j - q_{j-1}
  whose two terms share the sign (-1)^j, so ||(1-s)q|| = 2||q||.

(9/8)^r mechanism (mine): F_r(2,0) = (phi_r/4^r) sum_{i=0}^{r} 2^{r-i} C(2r+1,i);
  the summand 2^{-i}C(N,i) has ratio (1/2)(N-i)/(i+1), = 1 at i=(N-2)/3=(2r-1)/3,
  strictly inside [0,r] and Theta(sqrt r) standard deviations below the cut, so
  the truncated sum captures all but an exponentially small share of
  (1+1/2)^{2r+1}; hence F_r(2,0) ~ (phi_r/4^r) 2^r (3/2)^{2r+1} = (3/2)phi_r(9/8)^r.
"""

import sys
from fractions import Fraction as Fr

from ref_core import Ladder, Chain, peval, pnorm1, preflect, pmul, phi
from ref_bivar import A_of, B_of, constants

R = int(sys.argv[1]) if len(sys.argv) > 1 else 30
NSUP = int(sys.argv[2]) if len(sys.argv) > 2 else 40

print("=" * 78)
print("STEP 5  Sec 6 mechanisms, Lemma 7, Proposition 6, S_r.  R=%d" % R)
print("=" * 78)

lad = Ladder(R + 2, 3)

# ---------------------------------------------------------------------------
print()
print("(5a) LEMMA 7, exact:")
bad = n = 0
for r in range(0, min(R, 30) + 1):
    for b in range(0, 4):
        F = lad.F[(r, b)]
        G = lad.G[(r, b)]
        H = lad.H[(r, b)]
        n += 4
        if pnorm1(preflect(F)) != peval(F, 2):
            bad += 1
            print("   ||F_r(1-.,b)|| != F_r(2,b) at r=%d b=%d" % (r, b))
        if pnorm1(preflect(G)) != peval(G, 2):
            bad += 1
            print("   ||G_r(1-.,b)|| != G_r(2,b) at r=%d b=%d" % (r, b))
        if pnorm1(preflect(H)) != peval(H, 2):
            bad += 1
            print("   ||H_r(1-.,b)|| != H_r(2,b) at r=%d b=%d" % (r, b))
        if pnorm1(lad.Hh[(r, b)]) != 2 * peval(lad.F[(r, b + 1)], 2):
            bad += 1
            print("   ||Hhat_r(.,b)|| != 2F_r(2,b+1) at r=%d b=%d" % (r, b))
print("   %d exact checks (r=0..%d, b=0..3), %d failures" % (n, min(R, 30), bad))
print("   (the H_r case is my own extension: H_r also has nonneg coefficients)")

print()
print("(5b) the (9/8)^r factor:")
print("      r   F_r(2,0)/F_r(1,0)     ratio in r     /(9/8)^r      3/2 ?")
prev = None
for r in [10, 20, 30, 40, 50, 60]:
    if r > R:
        break
    v = peval(lad.F[(r, 0)], 2) / peval(lad.F[(r, 0)], 1)
    v1 = peval(lad.F[(r - 1, 0)], 2) / peval(lad.F[(r - 1, 0)], 1)
    print("   %5d %18.6f %14.6f %14.6f" %
          (r, float(v), float(v / v1), float(v / Fr(9, 8) ** r)))
print("   check F_r(2,0) = (phi_r/4^r) sum_i 2^{r-i} C(2r+1,i) :")
from math import comb
okid = all(peval(lad.F[(r, 0)], 2)
           == Fr(phi(r), 4 ** r) * sum(2 ** (r - i) * comb(2 * r + 1, i)
                                       for i in range(0, r + 1))
           for r in range(0, min(R, 25) + 1))
print("      r=0..%d : %s" % (min(R, 25), okid))
print("   peak of 2^{-i}C(2r+1,i) at i=(2r-1)/3, strictly inside [0,r] :",
      all(0 <= (2 * r - 1) / 3 <= r for r in range(1, 200)))

# ---------------------------------------------------------------------------
print()
print("(5c) PROPOSITION 6 -- original vs improved bound, both from my own A,B")
D_o, C_o = constants(lad, R, 1, order=2, kappa=2, geo=False)
D_i, C_i = constants(lad, R, 1, order=2, kappa=1, geo=True)
print("      r    D*_r(0) true      D'_r(0) improved     D_r(0) original    D/D'   ")
from ref_step4_helpers import dstar_exact
for r in [6, 10, 16, 20, 30, 40, 45]:
    if r > R:
        break
    ds = dstar_exact(r, 0)
    print("   %5d %16.4g %20.4g %20.4g %10.3g"
          % (r, float(ds), float(D_i[(r, 0)]), float(D_o[(r, 0)]),
             float(D_o[(r, 0)] / D_i[(r, 0)])))
print()
print("      r   D_r/D_{r-1}  C_r/C_{r-1}   D'_r/D'_{r-1}  C'_r/C'_{r-1}")
for r in [6, 10, 16, 20, 30, 40, 45]:
    if r > R:
        break
    print("   %5d %12.4f %12.4f %14.5f %14.5f"
          % (r, float(D_o[(r, 0)] / D_o[(r - 1, 0)]),
             float(C_o[(r, 0)] / C_o[(r - 1, 0)]),
             float(D_i[(r, 0)] / D_i[(r - 1, 0)]),
             float(C_i[(r, 0)] / C_i[(r - 1, 0)])))
print()
print("   A_r(0), B_r(0) growth ratios (target: 1.1945 and 1.1594 at r=40):")
for r in [20, 30, 40, 45]:
    if r > R:
        break
    print("      r=%2d  A ratio=%.4f  B ratio=%.4f"
          % (r, float(A_of(lad, r, 0, 2) / A_of(lad, r - 1, 0, 2)),
             float(B_of(lad, r, 0, 2) / B_of(lad, r - 1, 0, 2))))

print()
print("   Prop 6 hypothesis edge cases:")
print("      r/n <= r/(b+r+1) whenever n>=b+r+1 : trivially true; at r=0 both are 0.")
print("      the level-(r-1),b+1 hypothesis needs n >= (b+1)+(r-1)+1 = b+r+1  -> SAME range: OK")
ok01 = True
for n in range(1, 40):
    for b in range(0, 5):
        for r in range(0, 6):
            if n < b + r + 1:
                continue
            for a in range(0, n - b - r):
                x = Fr(n - a - 1 - b - r, n)
                if not (0 <= x <= 1):
                    ok01 = False
print("      (n-a-1-b-r)/n in [0,1] over every valid (n,a,b,r) with n>=b+r+1 :", ok01)
print("      at a = n-b-r-1 (h_r's own top boundary) it is EXACTLY 0, which is what")
print("      makes the out-of-domain reference g_r(b+r+1,b+1) harmless (issue I-2).")

# ---------------------------------------------------------------------------
print()
print("(5d) S_r(b) := sup over all valid m and all n>=b+r+1 of n^2|R_r(m,b,n)|")
print("     claim: attained at n = m = b+r+1.")
for b in (0, 1):
    for r in range(2, 9):
        best = None
        bestat = None
        atmin = None
        for n in range(b + r + 1, NSUP + 1):
            ch = Chain(n, r, b)
            for m in range(b + r + 1, n + 1):
                t = Fr(m, n)
                Rr = (ch.g[(r, m, b)] - peval(lad.F[(r, b)], t)
                      - peval(lad.G[(r, b)], t) / n)
                val = abs(Rr) * n ** 2
                if best is None or val > best:
                    best, bestat = val, (n, m)
                if n == b + r + 1 and m == n:
                    atmin = val
        print("   r=%d b=%d : S=%.6f at (n,m)=%s ; value at minimal state=%.6f ; match=%s"
              % (r, b, float(best), bestat, float(atmin), bestat == (b + r + 1, b + r + 1)))

print()
print("   S_r(0)/D*_r(0) at the minimal state (target: 1.1056/1.3634/1.5017 at r=4/20/60):")
for r in [4, 8, 12, 20, 30]:
    if r > R:
        break
    n = r + 1
    ch = Chain(n, r, 0)
    t = Fr(1)
    Rr = ch.g[(r, n, 0)] - peval(lad.F[(r, 0)], t) - peval(lad.G[(r, 0)], t) / n
    S = abs(Rr) * n ** 2
    ds = dstar_exact(r, 0)
    print("      r=%2d  S_r(0)=%.6f  D*_r(0)=%.6f  ratio=%.4f  S/r^1.5=%.4f"
          % (r, float(S), float(ds), float(S / ds), float(S) / r ** 1.5))
