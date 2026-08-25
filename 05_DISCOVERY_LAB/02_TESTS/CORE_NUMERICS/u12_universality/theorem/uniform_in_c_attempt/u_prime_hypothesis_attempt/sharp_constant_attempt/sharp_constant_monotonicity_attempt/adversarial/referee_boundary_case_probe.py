# Adversarial referee, sharp_constant_monotonicity_attempt -- Part 4:
#   Section 6 scope audit.  The target claims the K=n boundary case of (U')
#   cannot be immediately upgraded to the sharp constant because "the index
#   mismatch between n phi_n (needed) and Lemma 4.1's z_K-bound at K=n (which
#   gives (n+1)phi_n, not n phi_n) reintroduces exactly the kind of O(1)-losing
#   conversion step ...".
#
#   REFEREE FINDING (demonstrated below): the index-conversion loss is NOT O(1).
#   Converting the z-bound exactly (multiply by n/(n+1)) gives
#       n phi_n > (sqrt(pi)/2) n/sqrt(n+1),
#   and the elementary inequality 1/sqrt(1+x) >= 1 - x/2 (0<=x<=3) gives
#       n/sqrt(n+1) >= sqrt(n) - 1/(2 sqrt(n)),
#   an O(1/sqrt(n)) loss.  The parent's O(1) loss came from its own cruder
#   choice n/sqrt(n+1) >= sqrt(n)-1, which is avoidable.  With this document's
#   own Theorem 1 plus already-catalogued archive results (Theorem 5 of
#   sharp_constant_attempt, Lemma 4.1) the boundary case CLOSES with the sharp
#   constant:  |Q(n) - n phi_n| < a* sqrt(n)  for every n>=1:
#     upper side:  proof for n>=3  + exact checks n=1,2;
#     lower side:  proof for n>=67 + exact checks n=1..66.
#   Every finite check below is CERTIFIED RATIONAL (no float in any verdict).
# No randomness. None of the target's scripts/logs was read.
import sys
from fractions import Fraction as F
from math import isqrt
import mpmath as mp
import sympy as sp

mp.mp.dps = 60
LOG = []
def log(s=""):
    print(s)
    LOG.append(str(s))
fails = 0

PI_LO = F(31415926535897932, 10**16)
PI_HI = F(31415926535897933, 10**16)
D = 10**30

def sqrt_lo(fr):
    x = (fr.numerator * D * D) // fr.denominator
    return F(isqrt(x), D)

def sqrt_hi(fr):
    x = -((-fr.numerator * D * D) // fr.denominator)
    return F(isqrt(x) + 1, D)

def Q_exact(n):
    t = n ** (n - 1)
    tot = t
    for j in range(1, n):
        t = (t // n) * (n - j)
        tot += t
    return F(tot, n ** (n - 1))

def phi_exact(K):
    num = 4 ** K
    f = 1
    for i in range(2, K + 1):
        f *= i
    num *= f * f
    den = 1
    for i in range(2, 2 * K + 2):
        den *= i
    return F(num, den)

log("=" * 78)
log("(P0) The size of the actual index-conversion loss")
log("     loss(n) := (sqrt(pi)/2)(sqrt(n) - n/sqrt(n+1))  --  claimed by the")
log("     target to be 'O(1)-losing'; in fact  loss(n) <= (sqrt(pi)/4)/sqrt(n):")
log("=" * 78)
x = sp.symbols('x', nonnegative=True)
expand = sp.expand((1 - x / 2) ** 2 * (1 + x) - 1)
log(f"  Lemma R1: (1-x/2)^2 (1+x) - 1 = {expand} = x^2(x-3)/4 <= 0 for 0<=x<=3,")
log("  so 1/sqrt(1+x) >= 1-x/2 there; with x=1/n:  n/sqrt(n+1) >= sqrt(n)-1/(2 sqrt(n)).")
for n in [1, 2, 5, 10, 100, 10**4, 10**6]:
    loss = (mp.sqrt(mp.pi)/2) * (mp.sqrt(n) - n/mp.sqrt(n+1))
    cap = (mp.sqrt(mp.pi)/4) / mp.sqrt(n)
    log(f"   n={n:>8}: loss = {mp.nstr(loss, 5):>12}   (sqrt(pi)/4)/sqrt(n) = "
        f"{mp.nstr(cap, 5):>12}   loss<=cap: {loss <= cap + mp.mpf(10)**-40}")
log("  -> the conversion loss decays like 1/sqrt(n); it is NOT O(1).  (The")
log("     parent's crude n/sqrt(n+1) >= sqrt(n)-1 was O(1)-lossy, but nothing")
log("     forces that choice.)")

log("")
log("=" * 78)
log("(P1) UPPER SIDE for n >= 3:  Q(n) - n phi_n < a* sqrt(n).")
log("     Q(n) < sqrt(pi n/2) - 1/3 + (1/11)sqrt(pi/(2n))          [Theorem 1]")
log("     n phi_n > (sqrt(pi)/2)(sqrt(n) - 1/(2 sqrt(n)))          [z-bound + R1]")
log("     => Q(n)-n phi_n < a* sqrt(n) - 1/3 + c/sqrt(n),")
log("        c := (1/11)sqrt(pi/2) + sqrt(pi)/4.")
log("     Need c/sqrt(n) <= 1/3 for n>=3, i.e. 9 c^2 <= 3:")
log("=" * 78)
c_hi = F(1, 11) * sqrt_hi(PI_HI / 2) + sqrt_hi(PI_HI) / 4
chk = 3 * c_hi * c_hi < 1          # c^2 < 1/3  <=>  c < 1/sqrt(3)  <=> c/sqrt(3) <= 1/3
log(f"  certified c <= {float(c_hi):.9f};  3 c^2 = {float(3*c_hi*c_hi):.9f} < 1: {chk}")
log(f"  => c < 1/sqrt(3), so c/sqrt(n) <= c/sqrt(3) < 1/3 for every n>=3.  QED")
if not chk: fails += 1

log("")
log("=" * 78)
log("(P2) LOWER SIDE for n >= 67:  n phi_n - Q(n) < a* sqrt(n).")
log("     n phi_n < (sqrt(pi)/2) sqrt(n)                            [v-bound]")
log("     Q(n) >= sqrt(pi n/2) - 6            [Theorem 5, sharp_constant_attempt,")
log("                                          adversarially ACCEPTED]")
log("     => n phi_n - Q(n) < 6 - a* sqrt(n) <= a* sqrt(n)  iff  a* sqrt(n) >= 3.")
log("     Certified check that a* sqrt(67) > 3:")
log("=" * 78)
astar_lo = sqrt_lo(PI_LO / 2) - sqrt_hi(PI_HI) / 2
val = astar_lo * sqrt_lo(F(67))
log(f"  a*_lo = {float(astar_lo):.10f};  a*_lo * sqrt_lo(67) = {float(val):.6f} > 3: {val > 3}")
if not (val > 3): fails += 1
log("  => for n>=67 the lower side closes;  n=1..66 handled exactly below.")

log("")
log("=" * 78)
log("(P3) EXACT FINITE CHECKS (certified rational): |Q(n) - n phi_n| < a* sqrt(n)")
log("     for n = 1..80  (covers upper-side n=1,2 and lower-side n=1..66)")
log("=" * 78)
viol = []
for n in range(1, 81):
    diff = Q_exact(n) - n * phi_exact(n)
    lb = sqrt_lo(PI_LO * n / 2) - sqrt_hi(PI_HI * n) / 2   # a* sqrt(n) lower
    if not (abs(diff) < lb):
        viol.append(n)
log(f"  n=1..80: violations: {viol if viol else 'NONE (all certified)'}")
d1 = Q_exact(1) - 1 * phi_exact(1)
d2 = Q_exact(2) - 2 * phi_exact(2)
log(f"  spot values: Q(1)-phi_1 = {d1} (=1/3 < a*: "
    f"{abs(d1) < sqrt_lo(PI_LO/2)-sqrt_hi(PI_HI)/2});  Q(2)-2 phi_2 = {d2} "
    f"(=13/30 < a* sqrt(2) ~ 0.519)")
if viol: fails += 1

log("")
log("=" * 78)
log("(P4) CONSEQUENCE (referee observation, NOT a claim of the target document):")
log("     combining P1-P3 with the target's own Theorem 2 (generic case, K<=n-1,")
log("     via M_K -- verified in Part 3) and the trivial K=0 case (M_0=0), the")
log("     FULL sharp-constant upgrade of hypothesis (U'),")
log("         |phi_n^{(K)} - phi_K| <= a* sqrt(K)/n   for all 0<=K<=n,")
log("     follows from results already in the archive plus this half-page")
log("     argument.  Section 6's assessment that the boundary case 'would need")
log("     a genuinely separate derivation' therefore stands, in the weak sense")
log("     that a separate (short) argument is needed -- but its stated REASON")
log("     ('O(1)-losing conversion') is quantitatively wrong (P0), and the")
log("     described difficulty is overstated: the derivation is elementary and")
log("     uses no tool beyond what the archive has already accepted.")
M0 = Q_exact(1) - 1 * phi_exact(0)
log(f"     (K=0 sanity: M_0 = Q(1) - phi_0 = {M0}, trivially fine.)")
log("=" * 78)

log("")
log(f"PART-4 RESULT: {'ALL CHECKS PASSED (0 failures)' if fails == 0 else f'{fails} FAILURE GROUPS'}")
with open(__file__.replace(".py", ".log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
sys.exit(0 if fails == 0 else 1)
