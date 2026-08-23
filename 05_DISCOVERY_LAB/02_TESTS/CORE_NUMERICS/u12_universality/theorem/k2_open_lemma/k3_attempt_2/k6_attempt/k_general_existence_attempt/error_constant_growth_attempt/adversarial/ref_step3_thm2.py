"""
STEP 3 -- Theorem 2 (three-term existence, O(1/n^3) uniform), checked two ways.

(3A)  THE REDUCTION.  The predecessor's discrete-Gronwall argument needs
      |Delta_r^(3)| <= A^(3)_r(b) h^3 uniformly on t in [0,1].  Delta_r^(3) is
      built here from scratch as an exact bivariate polynomial in (t,h); the
      claim under test is that its h^0, h^1 AND h^2 brackets vanish identically
      in t, i.e. Delta^(3) = sum_{k>=3} h^k q_k(t,b).  Verified for the 2-term
      object too (h^0,h^1), which is the predecessor's own post-adversarial
      corrected statement.

(3B)  MY OWN SIMULATOR.  The exact discrete recursion is run at many n, and
        n^2 max_m |R_r|  ->  H_r(1,b)          (Corollary 2a)
        n^3 max_m |R^(3)_r|  stabilises        (Theorem 2)
      plus a direct violation count against my own D^(3)_r(b), C^(3)_r(b).

Also: reproduction of the wave-8 referee's A_r(0)/D_r(0)/C_r(0) table, from my
own Delta_r -- a check on the whole bivariate machinery.
"""

import sys
from fractions import Fraction as Fr

from ref_core import Ladder, Chain, peval, pnorm1
from ref_bivar import (delta2, delta3, bh_coeff, bmax_h, A_of, B_of,
                       brackets_vanish, constants)

R = int(sys.argv[1]) if len(sys.argv) > 1 else 16
B = int(sys.argv[2]) if len(sys.argv) > 2 else 4

print("=" * 78)
print("STEP 3  Theorem 2 -- brackets, constants, and my own finite-n simulator")
print("=" * 78)

lad = Ladder(R + 2, B + 2)

# ---------------------------------------------------------------------------
print()
print("(3A) brackets of Delta_r (2-term) and Delta_r^(3) (3-term) vanish?")
bad2 = bad3 = 0
n2 = n3 = 0
for r in range(0, R + 1):
    for b in range(0, B + 1):
        v2 = brackets_vanish(lad, r, b, 2)
        v3 = brackets_vanish(lad, r, b, 3)
        n2 += 1
        n3 += 1
        if not all(v2):
            bad2 += 1
            print("   Delta_r h^0/h^1 NONZERO at r=%d b=%d : %s" % (r, b, v2))
        if not all(v3):
            bad3 += 1
            print("   Delta_r^(3) h^0/h^1/h^2 NONZERO at r=%d b=%d : %s" % (r, b, v3))
print("   2-term: h^0,h^1 vanish for r=0..%d, b=0..%d  -> %d/%d ok"
      % (R, B, n2 - bad2, n2))
print("   3-term: h^0,h^1,h^2 vanish for r=0..%d, b=0..%d -> %d/%d ok"
      % (R, B, n3 - bad3, n3))
print("   lowest surviving h-power of Delta_r^(3):",
      [(r, min([j for j in range(0, bmax_h(delta3(lad, r, 0)) + 1)
                if any(c != 0 for c in bh_coeff(delta3(lad, r, 0), j))] or [None]))
       for r in range(2, min(R, 8) + 1)])
print("   highest h-power of Delta_r^(3) (should be r):",
      [(r, bmax_h(delta3(lad, r, 0))) for r in range(2, min(R, 8) + 1)])

# ---------------------------------------------------------------------------
print()
print("(3A') reproduction of the wave-8 referee's table (from MY OWN Delta_r):")
D2, C2 = constants(lad, R, B, order=2, kappa=2, geo=False)
print("      r  b        A_r(b)         D_r(b)          C_r(b)")
for r in range(1, 7):
    print("   %4d %2d  %14.6f %14.6f  %14.6f"
          % (r, 0, float(A_of(lad, r, 0, 2)), float(D2[(r, 0)]), float(C2[(r, 0)])))
print("   referee A.5 target:  D_2(2)=0.140952  D_3(1)=1.087000  D_3(5)=0.303012  D_4(3)=2.376231")
print("   mine              :  D_2(2)=%.6f  D_3(1)=%.6f  D_3(5)=%.6f  D_4(3)=%.6f"
      % (float(D2[(2, 2)]), float(D2[(3, 1)]), float(D2[(3, 5)]), float(D2[(4, 3)])))
print("   referee A.5 target:  C_2(2)=1.406746  C_3(1)=6.955026")
print("   mine              :  C_2(2)=%.6f  C_3(1)=%.6f"
      % (float(C2[(2, 2)]), float(C2[(3, 1)])))

# ---------------------------------------------------------------------------
print()
print("(3A'') third-order constants D^(3), C^(3) (kappa=1, as the target states):")
D3, C3 = constants(lad, R, B, order=3, kappa=1, geo=False)
D3k2, C3k2 = constants(lad, R, B, order=3, kappa=2, geo=False)
print("      r     A^(3)_r(0)      D^(3)_r(0)      C^(3)_r(0)   [kappa=2: D,C]")
for r in range(1, 8):
    print("   %4d %14.6f %14.6f %14.6f    %.6f %.6f"
          % (r, float(A_of(lad, r, 0, 3)), float(D3[(r, 0)]), float(C3[(r, 0)]),
             float(D3k2[(r, 0)]), float(C3k2[(r, 0)])))

# ---------------------------------------------------------------------------
print()
print("(3B) my own exact simulator")
NS = [12, 16, 20, 24, 30, 40, 60, 80]
for (r, b) in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (2, 2)]:
    print("   r=%d b=%d   H_r(1,b)=%s = %.6f    D^(3)_r(b)=%.4f  C^(3)_r(b)=%.4f"
          % (r, b, peval(lad.H[(r, b)], 1), float(peval(lad.H[(r, b)], 1)),
             float(D3[(r, b)]), float(C3[(r, b)])))
    hdr = "        n"
    l1 = "   n^2max|R|"
    l2 = "   n^3max|R3|"
    l3 = "   n^3max|e3|"
    viol = viole = 0
    for n in NS:
        if n < b + r + 3:
            continue
        ch = Chain(n, r, b + 1)
        m2 = Fr(0)
        m3 = Fr(0)
        for m in range(b + r + 1, n + 1):
            t = Fr(m, n)
            Rr = ch.g[(r, m, b)] - peval(lad.F[(r, b)], t) - peval(lad.G[(r, b)], t) / n
            R3 = Rr - peval(lad.H[(r, b)], t) / n ** 2
            m2 = max(m2, abs(Rr))
            m3 = max(m3, abs(R3))
            if abs(R3) * n ** 3 > D3[(r, b)]:
                viol += 1
        me = Fr(0)
        for a in range(0, n - b - r):
            s = Fr(a, n)
            e3 = (ch.h[(r, a, b)] - peval(lad.Hh[(r, b)], s)
                  - peval(lad.K[(r, b)], s) / n - peval(lad.L[(r, b)], s) / n ** 2)
            me = max(me, abs(e3))
            if abs(e3) * n ** 3 > C3[(r, b)]:
                viole += 1
        hdr += "%12d" % n
        l1 += "%12.6f" % float(m2 * n ** 2)
        l2 += "%12.6f" % float(m3 * n ** 3)
        l3 += "%12.6f" % float(me * n ** 3)
    print(hdr)
    print(l1)
    print(l2)
    print(l3)
    print("      violations of |R^(3)|<=D^(3)/n^3 : %d ;  of |eps^(3)|<=C^(3)/n^3 : %d"
          % (viol, viole))

# exact identity spot checks
print()
print("   exact spot checks:")
for n in (6, 7, 9, 11, 15):
    ch = Chain(n, 3, 3)
    ok1 = all(ch.g[(1, m, 0)] - peval(lad.F[(1, 0)], Fr(m, n))
              - peval(lad.G[(1, 0)], Fr(m, n)) / n == 0
              for m in range(2, n + 1))
    ok2 = all(ch.g[(2, m, 0)] - peval(lad.F[(2, 0)], Fr(m, n))
              - peval(lad.G[(2, 0)], Fr(m, n)) / n == Fr(1, 15 * n ** 2)
              for m in range(3, n + 1))
    print("      n=%2d  R_1==0 : %s    R_2==1/(15n^2) : %s" % (n, ok1, ok2))
    print("            psi_n^(1)=g_1(n,0)=%s (want %s) ; psi_n^(2)=%s (want %s)"
          % (ch.g[(1, n, 0)], Fr(4 * n + 1, 6 * n), ch.g[(2, n, 0)],
             Fr(8 * n * n + 4 * n + 1, 15 * n * n)))
