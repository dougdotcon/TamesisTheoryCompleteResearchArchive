"""
PART A finding (adversarial referee, k6_attempt): ATTEMPT.md Sec.1.2, check 4,
claims:

  "phi_n^{(6)} = (4096n^7+2186n^6+29676n^5+47655n^4+56117n^3+45424n^2+22428n
   +5040)/(12012n^7) ... with n->infinity limit exactly phi_6=1024/3003 and
   1/n coefficient 512/1001, matching 6*phi_6/4=512/1001 exactly (a sixth
   independent confirmation of the rate pattern, from the COMBINED not the
   generic-point quantity)."

This script shows, three independent ways, that the CLOSED FORM ITSELF is
correct (matches this referee's own independent re-derivation of both
psi_n^{(6)} and psi_n^{(6),R} via the K=6 ladder, and their Lemma-A
recombination) but the CLAIM about its 1/n coefficient is WRONG: the true
1/n coefficient of this (correct) closed form is 1093/6006 (~0.18198), NOT
512/1001 (~0.51149). The "6*phi_6/4" rate pattern is correctly proven (Sec.
3.4) and correctly confirmed (Sec.1.1, Sec.3.4) for psi_n^{(K)} -- the
GENERIC-POINT quantity -- but does NOT hold for the recombined phi_n^{(K)}
(consistent with the historical K=1,2,3 precedents in wave 5/wave 6, where
the phi_n^{(K)} rate coefficients are 0 [K=1, an even more special
cancellation], 1/30 [K=2], and 1/14 [K=3] respectively -- none of which
equal K*phi_K/4 either). This appears to be an isolated arithmetic/narrative
slip in Sec.1.2's prose, not an error in the actual mathematics or in any
other PROVED claim: Sec.5's own "phi_n^{(K)}-phi_K = Theta(1/n)" claim (a
weaker, ORDER-only statement, not a claim about the specific coefficient)
remains correct, and the psi-based rate conjecture (Sec.3.4, Sec.5's
Theorem, Scorecard row 7-8) is entirely unaffected, since it was never about
phi_n^{(K)} to begin with.
"""
import sympy as sp
from fractions import Fraction as F

n = sp.symbols('n', positive=True)

psi6_claimed = sp.together(2048*n**6+3072*n**5+4293*n**4+4638*n**3+3529*n**2+1662*n+360) / (6006*n**6)
psiR6_claimed = sp.together(1586*n**6+4458*n**5+6915*n**4+8055*n**3+6496*n**2+3204*n+720) / (5544*n**6)
phi6_claimed_closed_form = sp.together(4096*n**7+2186*n**6+29676*n**5+47655*n**4+56117*n**3+45424*n**2+22428*n+5040) / (12012*n**7)

print("=== Method 1: Lemma-A recombination of the (independently verified,")
print("    see adv_k6_recursion_check.py) psi_n^(6), psi_n^(6),R matches the")
print("    document's own claimed phi_n^(6) closed form exactly ===")
recombined = sp.simplify(sp.together(sp.Rational(6, 1) / n * psiR6_claimed + (1 - sp.Rational(6, 1) / n) * psi6_claimed))
print("Lemma-A recombination:", recombined)
print("Document's claimed phi_n^(6):", sp.simplify(phi6_claimed_closed_form))
print("difference:", sp.simplify(recombined - phi6_claimed_closed_form), " (0 => the closed form itself is correct)")
assert sp.simplify(recombined - phi6_claimed_closed_form) == 0

print()
print("=== Method 2: sp.limit-based extraction of the TRUE 1/n coefficient ===")
lim = sp.limit(phi6_claimed_closed_form, n, sp.oo)
rate = sp.limit((phi6_claimed_closed_form - lim) * n, n, sp.oo)
print(f"limit = {lim}  (matches claimed phi_6=1024/3003: {lim == sp.Rational(1024,3003)})")
print(f"TRUE 1/n coefficient (sp.limit) = {rate}")
print(f"Document's claim: 512/1001 = {sp.Rational(512,1001)}")
print(f"Document's claim matches computed value: {rate == sp.Rational(512,1001)}   <-- FALSE: mismatch")
print(f"6*phi_6/4 = {sp.simplify(sp.Rational(6,4)*sp.Rational(1024,3003))}")

print()
print("=== Method 3: sp.series-based extraction (independent sympy code path) ===")
x = sp.symbols('x', positive=True)
ser = sp.series(phi6_claimed_closed_form.subs(n, 1 / x), x, 0, 2)
print("Series in x=1/n:", ser)

print()
print("=== Method 4: plain-Python Fraction numerics, n up to 1,000,000")
print("    (no sympy at all -- eliminates any possibility of a sympy-specific")
print("    artifact) ===")


def psi6(nv):
    nv = F(nv)
    return (2048*nv**6+3072*nv**5+4293*nv**4+4638*nv**3+3529*nv**2+1662*nv+360) / (6006*nv**6)


def psiR6(nv):
    nv = F(nv)
    return (1586*nv**6+4458*nv**5+6915*nv**4+8055*nv**3+6496*nv**2+3204*nv+720) / (5544*nv**6)


def phi6(nv):
    nv = F(nv)
    K = F(6)
    return K / nv * psiR6(nv) + (1 - K / nv) * psi6(nv)


phi6_limit = F(1024, 3003)
for nv in [1000, 10000, 100000, 1000000]:
    val = phi6(nv)
    coeff_est = (val - phi6_limit) * nv
    print(f"  n={nv}: n*(phi_n^6 - phi_6) = {float(coeff_est):.6f}  (converging to 1093/6006={float(F(1093,6006)):.6f}, NOT 512/1001={float(F(512,1001)):.6f})")

print()
print("=== CONCLUSION ===")
print("The exact closed form for phi_n^(6) in ATTEMPT.md Sec.1.2 is CORRECT")
print("(independently re-derived and confirmed above and in")
print("adv_k6_recursion_check.py). The document's claim that its 1/n")
print("coefficient is 512/1001 (\"matching 6*phi_6/4 exactly\") is WRONG: the")
print("true 1/n coefficient is 1093/6006, confirmed by FOUR independent")
print("methods above (Lemma-A algebra, sp.limit, sp.series, plain-Fraction")
print("numerics extrapolation). This is a factual/arithmetic error in the")
print("document's narrative claim, isolated to this one sentence in Sec.1.2 --")
print("it does not affect: (a) the correctness of the phi_n^(6) closed form")
print("itself, (b) the K=6 Open Lemma proof (phi_n^(6)->phi_6, needs only the")
print("LIMIT, not the rate), (c) the psi-based rate conjecture (Sec.3.4,")
print("Sec.5, Scorecard rows 7-8), which was never a claim about phi_n^(K),")
print("or (d) Sec.5's weaker 'phi_n^(K)-phi_K = Theta(1/n)' order claim (still")
print("true, since 1093/6006 != 0).")
