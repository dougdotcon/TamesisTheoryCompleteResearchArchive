"""
ADVERSARIAL REFEREE: the DOMAIN CAVEAT, tested as a biconditional.

The target states the caveat next to Theorem B.  The orchestrating session hit
it as an infinite loop.  The precise question: is the out-of-domain reference in
the recursion ALWAYS killed by an exactly-zero coefficient, and never otherwise?

Two separate boundary facts must be checked, and they are NOT the same fact:

 (D1) in rule (*)  [non-source step]: g_r(m,b) references g_r(m-1,b).
      At the minimum m = b+r+1 the reference m-1 = b+r is out of domain;
      the coefficient (m-1-r-b)/m is exactly 0 there.
 (D2) in rule (**) [source step]: h_r(a,b) references g_r(n-a, b+1), whose
      domain is m >= (b+1)+r+1 = b+r+2.  At the maximum a = n-b-r-1 the
      reference is m = b+r+1, exactly ONE BELOW that domain; the coefficient
      (n-1-a-b-r)/n is exactly 0 there.

 (D3) separately: Theorem B evaluates ghat_r(n-a+1, b+1) at a=0, i.e. at
      m' = n+1 > n, outside the probabilistic domain.  This is NOT a defect:
      the (*) identity proved in Sec.4.1 is a POLYNOMIAL identity in m, valid
      at every integer m, and h is DEFINED by that expression.  Verified here
      by checking (*) for ghat with symbolic m (done in ref_symbolic.py) and by
      checking that no step of the raw recursion ever needs g_r out of domain.
"""
from fractions import Fraction as F
import sys
from ref_sim import Raw, g_hat, h_hat

n1 = n2 = n3 = n4 = 0
bad = []
for n in range(2, 30):
    for r in range(0, n):
        for b in range(0, n - r):
            # ---- (D1)
            for m in range(b + r + 1, n + 1):
                coef = F(m - 1 - r - b, m)
                out_of_domain = (m - 1 < b + r + 1)
                if out_of_domain:
                    n1 += 1
                    if coef != 0:
                        bad.append(("D1 out-of-domain but coef != 0", n, r, b, m, coef))
                else:
                    n2 += 1
                    if coef == 0:
                        bad.append(("D1 in-domain but coef == 0", n, r, b, m))
            # ---- (D2)
            for a in range(0, n - b - r):
                coef = F(n - 1 - a - b - r, n)
                mref = n - a
                out_of_domain = (mref < (b + 1) + r + 1)
                if out_of_domain:
                    n3 += 1
                    if coef != 0:
                        bad.append(("D2 out-of-domain but coef != 0", n, r, b, a, coef, mref))
                else:
                    n4 += 1
                    if coef == 0:
                        bad.append(("D2 in-domain but coef == 0", n, r, b, a, mref))

print("=" * 74)
print("DOMAIN CAVEAT, tested as a strict BICONDITIONAL")
print("=" * 74)
print(f"  (D1) rule (*)  : {n1:6d} out-of-domain references, ALL with coefficient exactly 0")
print(f"                   {n2:6d} in-domain references,     NONE with coefficient 0")
print(f"  (D2) rule (**) : {n3:6d} out-of-domain references, ALL with coefficient exactly 0")
print(f"                   {n4:6d} in-domain references,     NONE with coefficient 0")
print(f"  n=2..29, all r, all b, every valid state")
print(f"  VIOLATIONS: {len(bad)}")
for x in bad[:10]:
    print("   ", x)

print()
print("  Note the ASYMMETRY, which is the trap:")
print("    in (*)  the out-of-domain reference is m-1 = b+r,   one below g_r(.,b)'s min b+r+1")
print("    in (**) the out-of-domain reference is n-a = b+r+1, one below g_r(.,b+1)'s min b+r+2")
print("  Both are 'one below the minimum', but for DIFFERENT b, which is why a naive")
print("  implementation that guards only (*) still diverges on (**).")

# ---- (D3): Theorem B at a=0 evaluates ghat out of the probabilistic domain,
#            but the raw recursion never does.
print()
print("=" * 74)
print("(D3) Theorem B at a=0 evaluates ghat_r(n+1, b+1) -- outside the")
print("     probabilistic domain.  Is that a defect?")
print("=" * 74)
nb = 0
for n in range(3, 22):
    Rw = Raw(n)
    for r in range(0, min(6, n - 1) + 1):
        for b in range(0, min(4, n - 1 - r) + 1):
            lhs = Rw.hr(r, 0, b)
            rhs = h_hat(r, 0, b, n)          # uses ghat at m' = n+1
            nb += 1
            if lhs != rhs:
                bad.append(("D3", n, r, b, lhs, rhs))
print(f"  h_r(0,b) [true probability, raw recursion] == (n+1)/n * ghat_r(n+1, b+1)")
print(f"    {nb} exact checks, {len([x for x in bad if x[0]=='D3'])} mismatches")
print("  -> NOT a defect: ghat is a POLYNOMIAL expression, the Sec.4.1 identity is a")
print("     polynomial identity in m valid at every integer, and the raw recursion")
print("     itself never evaluates g_r out of domain (asserted throughout ref_sim.py).")
print()
print("=" * 74)
print(f"DOMAIN VERDICT: {len(bad)} violations -> the caveat's reasoning is SOUND")
print("=" * 74)
sys.exit(1 if bad else 0)
