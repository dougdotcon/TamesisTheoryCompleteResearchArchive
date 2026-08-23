"""
STEP 1 -- independent re-derivation of the eps^2 matching (target's Sec 3.1) and
of Theorem 1 (the e_k^{(r)}(b) closed form).

The ladder in ref_core.py solves MY OWN eps^0/eps^1/eps^2 ODEs.  Two things are
tested here:

  (A) VALIDATION ONE ORDER DOWN.  My eps^0 and eps^1 ODEs, solved by my own
      solver, must reproduce the already-PROVED c_k^{(r)}(b) and d_k^{(r)}(b).
      If they do not, my derivation (or the solver) is broken and nothing else
      below can be trusted.

  (B) THE NEW ORDER.  My eps^2 ODE, solved the same way, is compared to the
      target document's claimed Theorem 1 closed form e_k^{(r)}(b).

Plus: base-case sanity (H_0 = L_0 = 0, H_1 = 0, H_2(t,0) = 1/15), degrees, and
positivity of the coefficients (Corollary 1a).
"""

import sys
from fractions import Fraction as Fr
from ref_core import (Ladder, c_closed, d_closed, e_closed, peval, pnorm1,
                      pzero, psub, ptrim)

R = int(sys.argv[1]) if len(sys.argv) > 1 else 30
B = int(sys.argv[2]) if len(sys.argv) > 2 else 8

print("=" * 78)
print("STEP 1  eps^2 matching, re-derived independently.  R=%d  B=%d" % (R, B))
print("=" * 78)

lad = Ladder(R, B)

# --- (A) validation one order down --------------------------------------
okF = okG = 0
badF = badG = 0
for r in range(0, R + 1):
    for b in range(0, B + 1):
        F = lad.F[(r, b)]
        G = lad.G[(r, b)]
        for k in range(0, r + 3):          # includes out-of-range k (must be 0)
            fk = F[k] if k < len(F) else Fr(0)
            gk = G[k] if k < len(G) else Fr(0)
            if fk == c_closed(r, k, b):
                okF += 1
            else:
                badF += 1
                if badF < 5:
                    print("   F MISMATCH r=%d k=%d b=%d  mine=%s  closed=%s"
                          % (r, k, b, fk, c_closed(r, k, b)))
            if gk == d_closed(r, k, b):
                okG += 1
            else:
                badG += 1
                if badG < 5:
                    print("   G MISMATCH r=%d k=%d b=%d  mine=%s  closed=%s"
                          % (r, k, b, gk, d_closed(r, k, b)))
print("(A1) my eps^0 ODE solution vs PROVED c_k^{(r)}(b):  %d checks, %d mismatches"
      % (okF, badF))
print("(A2) my eps^1 ODE solution vs PROVED d_k^{(r)}(b):  %d checks, %d mismatches"
      % (okG, badG))

# --- (B) the new order ---------------------------------------------------
okH = badH = 0
degbad = 0
posbad = 0
for r in range(0, R + 1):
    for b in range(0, B + 1):
        H = lad.H[(r, b)]
        for k in range(0, r + 3):
            hk = H[k] if k < len(H) else Fr(0)
            if hk == e_closed(r, k, b):
                okH += 1
            else:
                badH += 1
                if badH < 8:
                    print("   H MISMATCH r=%d k=%d b=%d  mine=%s  claimed=%s"
                          % (r, k, b, hk, e_closed(r, k, b)))
        # degree
        Ht = ptrim(H)
        deg = len(Ht) - 1 if Ht != [Fr(0)] else None
        want = r - 2 if r >= 2 else None
        if deg != want:
            degbad += 1
            print("   DEG r=%d b=%d  deg=%s want=%s" % (r, b, deg, want))
        # positivity of all coefficients 0..r-2
        for k in range(0, max(0, r - 1)):
            if (H[k] if k < len(H) else Fr(0)) <= 0:
                posbad += 1
print("(B1) my eps^2 ODE solution vs Theorem 1's e_k^{(r)}(b):  %d checks, %d mismatches"
      % (okH, badH))
print("(B2) deg H_r = r-2 (H_0=H_1=0):  %d violations" % degbad)
print("(B3) Corollary 1a  e_k^{(r)}(b) > 0 for 0<=k<=r-2:  %d violations" % posbad)

# --- base cases ----------------------------------------------------------
print()
print("Base cases (independent):")
for b in range(0, 4):
    print("   H_0(.,%d)=%s   L_0(.,%d)=%s   H_1(.,%d)=%s"
          % (b, lad.H[(0, b)], b, lad.L[(0, b)], b, lad.H[(1, b)]))
print("   H_2(t,0) =", lad.H[(2, 0)], " -> H_2(1,0) =", peval(lad.H[(2, 0)], 1))
print("   H_2(t,1) =", lad.H[(2, 1)])
print("   H_3(t,0) =", lad.H[(3, 0)])

# --- the h-side sixth cross-check: psi_n^{(3),R} = h_2(0,0) --------------
print()
print("h-side cross-check against PROVED psi_n^{(3),R} = 11/30 + 13/(20n) + 23/(60n^2) + 1/(10n^3):")
print("   Hhat_2(0,0) =", peval(lad.Hh[(2, 0)], 0), "  (want 11/30)")
print("   K_2(0,0)    =", peval(lad.K[(2, 0)], 0), "  (want 13/20)")
print("   L_2(0,0)    =", peval(lad.L[(2, 0)], 0), "  (want 23/60)   <- from MY L_r relation")

# --- D*_r(0) = H_r(1,0) table -------------------------------------------
print()
print("My H_r(1,0) for r=0..9 (from my own ODE, not from any closed form):")
print("   ", [str(peval(lad.H[(r, 0)], 1)) for r in range(0, 10)])
print("My H_r(1,1) for r=0..7:")
print("   ", [str(peval(lad.H[(r, 1)], 1)) for r in range(0, 8)])
