"""
order_ladder.py
  (1) the mandated fourth rung  I_r = Phi[3]_r  and  M_r = Psi[3]_r,
  (2) the multiplier table with the Stirling identification,
  (3) the truncation-order check: the p-term truncation error is EXACTLY the
      tail  sum_{q>p} eps^q Phi[q]_r  (so identically 0 once p > r), checked
      against the from-scratch exact discrete simulator,
  (4) the all-orders sharp residual constants D*^(p)_r(b) = Phi[p]_r(1,b).
All arithmetic exact.
"""

import sys
from fractions import Fraction
from core import Ladder, Chain, _ff, _denom, phi_wallis

_C = {}


def stirling1u(N, M):
    if N < 0 or M < 0:
        return 0
    if N == 0:
        return 1 if M == 0 else 0
    if M == 0:
        return 0
    key = (N, M)
    v = _C.get(key)
    if v is None:
        v = (N - 1) * stirling1u(N - 1, M) + stirling1u(N - 1, M - 1)
        _C[key] = v
    return v


def coeff_closed(k, p, r, b):
    if k < 0 or k + p > r:
        return Fraction(0)
    return Fraction(stirling1u(k + p + 1, k + 1) * _ff(r, k, p),
                    _denom(k, p, r, b))


def A_j(r, j, b):
    if j < 0 or j > r:
        return Fraction(0)
    return Fraction(_ff(r, j, 0), _denom(j, 0, r, b))


L = Ladder(Fraction(0))

print("=" * 78)
print("PART 1 -- the mandated fourth rung:  I_r := Phi[3]_r  (order 1/n^3)")
print("=" * 78)
print("  claimed:  [t^k] I_r(t,b) = c(k+4,k+1) * r!/(r-k-3)! "
      "/ prod_{i=1}^{k+4}(r+b+i)")
print("  with     c(k+4,k+1) = C(k+4,2)*C(k+4,4) "
      "= (k+1)(k+2)(k+3)^2(k+4)^2/48")
bad = 0
for k in range(0, 30):
    v = Fraction((k + 1) * (k + 2) * (k + 3) ** 2 * (k + 4) ** 2, 48)
    if Fraction(stirling1u(k + 4, k + 1)) != v:
        bad += 1
    cc = Fraction((k + 4) * (k + 3), 2) * Fraction(
        (k + 1) * (k + 2) * (k + 3) * (k + 4), 24)
    if Fraction(stirling1u(k + 4, k + 1)) != cc:
        bad += 1
print("  c(k+4,k+1) == C(k+4,2)C(k+4,4) == (k+1)(k+2)(k+3)^2(k+4)^2/48,"
      " k=0..29: failures =", bad)
bad = 0
ck = 0
for r in range(0, 22):
    for d in range(0, 7):
        P = L.phi(3, r, d)
        for k in range(0, r + 4):
            ck += 1
            if P.coeff(k) != coeff_closed(k, 3, r, Fraction(d)):
                bad += 1
print("  I_r closed form vs the ODE ladder, r=0..21, b=0..6, all k:"
      " %d checks, %d mismatches" % (ck, bad))
print("  first few I_r(t,0):")
for r in range(0, 8):
    print("     r=%d : %s" % (r, L.phi(3, r, 0).c))

print()
print("  and the h-side fourth rung  M_r := Psi[3]_r  (order 1/n^3):")
print("     M_r(s,b) = sum_k c(k+4,k+1) * r!/(r-k-2)! (1-s)^k"
      " / prod_{i=1}^{k+3}(r+b+1+i)")
bad = 0
ck = 0
for r in range(0, 16):
    for d in range(0, 5):
        E = L.eta(3, r, d)      # eta[3]_r(t,b) = Psi[3]_r(1-t,b), variable u=t
        for k in range(0, r + 4):
            ck += 1
            want = (Fraction(stirling1u(k + 4, k + 1))
                    * A_j(r, k + 2, Fraction(d) + 1))
            if E.coeff(k) != want:
                bad += 1
print("     %d checks, %d mismatches" % (ck, bad))
print("  M_2(0,0) = %s  (PROVED 1/n^3 coefficient of psi_n^(3),R is 1/10)"
      % L.eta(3, 2, 0).ev(Fraction(1)))

print()
print("=" * 78)
print("PART 2 -- the multiplier ladder")
print("=" * 78)
print("  order   multiplier M_p(k)          identification")
rows = [
    (0, "1", "c(k+1,k+1)"),
    (1, "C(k+2,2)", "c(k+2,k+1)"),
    (2, "(3k+8)/4 * C(k+3,3)", "c(k+3,k+1)"),
    (3, "C(k+4,2) * C(k+4,4)", "c(k+4,k+1)   <-- NEW"),
]
for p, f, ident in rows:
    print("  1/n^%d   %-26s %s" % (p, f, ident))
print("  1/n^p   c(k+p+1,k+1)               unsigned Stirling 1st kind")
print()
print("  M_p(k) table (rows p, cols k) -- read off the ladder, then matched:")
hdr = "   p\\k |" + "".join("%12d" % k for k in range(0, 7))
print(hdr)
for p in range(0, 8):
    row = "   %3d |" % p
    for k in range(0, 7):
        row += "%12d" % stirling1u(k + p + 1, k + 1)
    print(row)

print()
print("=" * 78)
print("PART 3 -- the truncation error is EXACTLY the tail (so 0 once p>r)")
print("     R^(p)_r(m,b,n) := g_r(m,b) - sum_{q=0}^{p-1} Phi[q]_r(t,b)/n^q")
print("     claim:  R^(p)_r = sum_{q=p}^{r} Phi[q]_r(t,b)/n^q   EXACTLY")
print("=" * 78)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 22
checks = 0
bad = 0
zero_beyond = 0
for n in range(2, NMAX + 1):
    ch = Chain(n)
    for r in range(0, min(n, 8)):
        for bb in range(0, min(n - r, 5)):
            for m in range(bb + r + 1, n + 1):
                if (n - m) + bb + r >= n:
                    continue
                t = Fraction(m, n)
                g = ch.g_r(m, bb, r)
                for p in range(0, r + 3):
                    head = sum(L.phi(q, r, bb).ev(t) * Fraction(1, n ** q)
                               for q in range(0, p))
                    tail = sum(L.phi(q, r, bb).ev(t) * Fraction(1, n ** q)
                               for q in range(p, r + 1))
                    checks += 1
                    if g - head != tail:
                        bad += 1
                    if p > r and (g - head) != 0:
                        zero_beyond += 1
print("  %d exact checks, %d mismatches" % (checks, bad))
print("  cases with p>r where the residual was NOT exactly 0:", zero_beyond)

print()
print("  --> in particular the mandated check: the FOUR-term truncation error")
print("      g_r - F_r - G_r/n - H_r/n^2 - I_r/n^3  is exactly")
print("      sum_{q>=4} Phi[q]_r/n^q, hence identically 0 for r<=3 and")
print("      exactly Theta(1/n^4) for r>=4 with constant Phi[4]_r(1,b).")
tab = []
for r in range(0, 9):
    tab.append((r, L.phi(4, r, 0).ev(Fraction(1))))
print("      Phi[4]_r(1,0) for r=0..8: " + ", ".join(
    "%d:%s" % (r, v) for r, v in tab))

print()
print("=" * 78)
print("PART 4 -- the all-orders sharp residual constants")
print("     D*^(p)_r(b) := lim_n n^p max_m |R^(p)_r| = Phi[p]_r(1,b)")
print("     (max at t=1 since every coefficient c(k+p+1,k+1) > 0)")
print("=" * 78)
print("  cross-check p=2, b=0 against Estagio 8 Theorem 3:"
      "  r(3r+1)/32 * varphi_r - r/12")
bad = 0
for r in range(0, 40):
    want = Fraction(r * (3 * r + 1), 32) * phi_wallis(r) - Fraction(r, 12)
    got = sum(coeff_closed(k, 2, r, 0) for k in range(0, r + 1))
    if got != want:
        bad += 1
print("  r=0..39 : failures =", bad)
print()
print("  the new p=3, b=0 constants D*^(3)_r(0) = I_r(1,0):")
for r in range(0, 11):
    v = sum(coeff_closed(k, 3, r, 0) for k in range(0, r + 1))
    print("     r=%2d : %-24s = %.8f" % (r, v, float(v)))

print()
print("=" * 78)
print("PART 5 -- the h-side terminates too:  Psi[p]_r == 0 for p > r+1,")
print("          and h_r(a,b) = sum_{p=0}^{r+1} Psi[p]_r(s,b)/n^p  EXACTLY")
print("=" * 78)
bad = 0
for r in range(0, 10):
    for d in range(0, 4):
        for p in range(0, r + 5):
            if p > r + 1 and L.eta(p, r, d).deg() >= 0:
                bad += 1
print("  nonzero Psi[p]_r with p > r+1 (r<=9, b<=3):", bad)
print("  degrees of Psi[p]_6(.,0), p=0..9:",
      [L.eta(p, 6, 0).deg() for p in range(0, 10)])
checks = 0
bad = 0
for n in range(3, 20):
    ch = Chain(n)
    for r in range(0, min(n, 7)):
        for bb in range(0, min(n - r, 4)):
            for a in range(0, n - bb - r):
                sv = Fraction(a, n)
                tot = sum(L.eta(p, r, bb).ev(1 - sv) * Fraction(1, n ** p)
                          for p in range(0, r + 2))
                checks += 1
                if tot != ch.h_r(a, bb, r):
                    bad += 1
print("  %d exact checks against the simulator, %d mismatches" % (checks, bad))
