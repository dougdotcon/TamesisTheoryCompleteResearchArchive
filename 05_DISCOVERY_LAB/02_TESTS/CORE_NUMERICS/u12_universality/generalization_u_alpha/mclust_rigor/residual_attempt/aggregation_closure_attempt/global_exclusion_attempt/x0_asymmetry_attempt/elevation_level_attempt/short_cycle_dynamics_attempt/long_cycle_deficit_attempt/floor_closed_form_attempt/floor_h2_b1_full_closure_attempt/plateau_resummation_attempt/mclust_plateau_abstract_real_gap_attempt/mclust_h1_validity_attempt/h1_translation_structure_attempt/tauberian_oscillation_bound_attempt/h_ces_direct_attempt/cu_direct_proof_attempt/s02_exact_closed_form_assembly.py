#!/usr/bin/env python3
"""
s02_exact_closed_form_assembly.py -- wave 29 front (a), CU-DIRECT-PROOF-ATTEMPT

Redo the assembly of the closed-form kernel identity

  K(y,t) f(x) = [f(x) - e^{-h/eps} f(x+h)] / z  +  [error term]      z:=x+y

(cited, h1_translation_structure_attempt Sec 4, DISC-DEC-122) EXACTLY --
using ONLY the fully rigorous, non-asymptotic Gordon-type bounds proved in
s01/s01b (no formal asymptotic series for R(z) anywhere) -- to determine
PRECISELY what regularity of f is needed for the error term to be
UNIFORMLY O(1/z^2), i.e. to prove hypothesis (U) as an actual theorem
rather than a numerically-tested claim.

MAIN FINDING OF THIS SCRIPT (see PART 4 summary at the end): the closed
form splits cleanly into two pieces --

  (a) a piece built ONLY from f's VALUES at x and x+h (via F1:=f(x),
      F2:=e^{-h/eps}f(x+h), and KB:=K_B(h)f(x), all already implicit in
      the exact IBP identity) -- this piece is shown here to match the
      target [F1-F2]/z to a RIGOROUS, EXPLICIT O(1/z^2) (in fact O(1/z^3)
      for one sub-piece), using ONLY hypothesis (B) (boundedness). NO
      Lipschitz/C^1 regularity of f is needed for this piece -- new,
      stronger-than-any-ancestor-front result.

  (b) a genuine residual piece (Efull, from the part of the Watson-lemma
      remainder rho(h',z) beyond its f'(x+h')*sigma(z) "linear" leading
      behavior) which DOES need f's regularity: under (C') alone (f
      Lipschitz, constant L1, t-uniform) it is only O(1/z) after the
      (1-eps*z)/eps~-z amplification -- INSUFFICIENT for (U) as literally
      stated; under (C')+(C'') (f' ALSO Lipschitz, constant L2 -- i.e. f
      is C^{1,1}, t-uniform) it is O(1/z^2) -- SUFFICIENT. This precisely
      locates the true prerequisite for (U): (C') alone is not obviously
      enough; a genuine (if mild) strengthening to C^{1,1} regularity is
      what this front's rigorous route actually needs.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

print("=" * 78)
print("PART 1 -- exact symbolic assembly (R(z) kept exact via sigma(z))")
print("=" * 78)

z, eps, sigma = sp.symbols('z eps sigma', positive=True)
KB, F1, F2 = sp.symbols('KB F1 F2', real=True)

Rz = (1 - sigma) / z
c = (1 - eps * z) * Rz / eps
one_plus_c = sp.simplify(1 + c)
print("1+c(z) [with R(z)=(1-sigma)/z] =", one_plus_c)

prefactor = (1 - eps * z) / eps
leading_rho_term = prefactor * sigma * (F2 - F1 + KB / eps)
K_main = sp.expand(one_plus_c * KB + leading_rho_term)

coeff_KB = sp.simplify(sp.diff(K_main, KB))
coeff_F2 = sp.simplify(sp.diff(K_main, F2))
coeff_F1 = sp.simplify(sp.diff(K_main, F1))
assert sp.simplify(coeff_F1 + coeff_F2) == 0
print("coeff(KB)     =", sp.factor(coeff_KB))
print("coeff(F2-F1)  =", sp.factor(coeff_F2))
print()

print("=" * 78)
print("PART 2 -- rigorous O(1/z^2) bound on coeff(F2-F1) - (-1/z)")
print("=" * 78)
# coeff(F2-F1) = -sigma*z + sigma/eps.  Target: -1/z.
# Rewrite -sigma*z + 1/z = (1 - sigma*z^2)/z  [algebra, confirmed below]
diff_F = sp.simplify(coeff_F2 - (sp.Integer(-1)/z))
alg_check = sp.simplify(diff_F - ((1 - sigma*z**2)/z + sigma/eps))
print("coeff(F2-F1)-(-1/z) - [(1-sigma*z^2)/z + sigma/eps] =", alg_check, " (must be 0)")
assert alg_check == 0
print("CONFIRMED: coeff(F2-F1) - (-1/z) = (1-sigma*z^2)/z + sigma/eps")
print()
print("From s01b (Gordon bracket, exact, non-asymptotic):")
print("  1/(1+z^2) <= 1-z^2*sigma(z) <= 3/(z^2+3)      for all z>0")
print("  0 <= sigma(z) <= 1/(1+z^2)  <= 1/z^2                        (s01 G2)")
print()
print("=> |(1-sigma*z^2)/z| <= 3/(z(z^2+3)) = O(1/z^3)")
print("=> |sigma/eps|        <= 1/(eps*(1+z^2)) = O(1/(eps*z^2))")
print("=> |coeff(F2-F1)-(-1/z)| <= 3/(z(z^2+3)) + 1/(eps*(1+z^2))")
print("   = O(1/(eps*z^2))   [RIGOROUS, uses ONLY R(z)'s own properties --")
print("     NO Lipschitz/C^1 regularity of f needed for this piece.]")
print()
# numeric spot confirmation of the exact bracket via direct R(z):
def R_mp(zz):
    zz = mp.mpf(zz)
    return mp.sqrt(mp.pi / 2) * mp.erfc(zz / mp.sqrt(2)) * mp.exp(zz ** 2 / 2)

print(f"{'z':>8} {'eps':>6} {'|coeff(F2-F1)+1/z|':>20} {'bound 3/(z(z2+3))+1/(eps(1+z2))':>34}")
worst_ratio = 0
for zz in [mp.mpf(x) for x in [2,5,10,50,100,1000,10000]]:
    for ee in [mp.mpf('0.05'), mp.mpf('0.1'), mp.mpf('1')]:
        Ra = R_mp(zz)
        sig = 1 - zz*Ra
        actual = abs(-sig*zz + sig/ee - (-1/zz))
        bound = 3/(zz*(zz**2+3)) + 1/(ee*(1+zz**2))
        ratio = actual/bound
        worst_ratio = max(worst_ratio, float(ratio))
        assert actual <= bound + mp.mpf('1e-30'), (zz, ee, actual, bound)
        print(f"{float(zz):8.4g} {float(ee):6.3g} {float(actual):20.6e} {float(bound):34.6e}")
print(f"worst actual/bound ratio observed: {worst_ratio:.6f}  (must be <=1)")
print()

print("=" * 78)
print("PART 3 -- rigorous O(1/z^2) bound on coeff(KB)")
print("=" * 78)
alg_check2 = sp.simplify(coeff_KB - ((1 - sigma*z**2)/(eps*z) + sigma*(1 + 1/eps**2 - 1/(eps*z))))
print("coeff(KB) - [(1-sigma*z^2)/(eps*z) + sigma*(1+1/eps^2-1/(eps*z))] =", alg_check2, " (must be 0)")
assert alg_check2 == 0
print("CONFIRMED regrouping. Using the SAME two rigorous bounds as Part 2:")
print("  |(1-sigma*z^2)/(eps*z)|            <= 3/(eps*z*(z^2+3))         = O(1/(eps*z^3))")
print("  |sigma*(1+1/eps^2-1/(eps*z))|      <= [1/(1+z^2)]*(1+1/eps^2+1/eps) = O(1/z^2)  (eps fixed)")
print("=> |coeff(KB)| = O(1/z^2)  [again RIGOROUS, again NO Lipschitz/C^1 needed]")
print()
print(f"{'z':>8} {'eps':>6} {'|coeff(KB)|':>16} {'crude bound':>20}")
for zz in [mp.mpf(x) for x in [2,5,10,50,100,1000]]:
    for ee in [mp.mpf('0.1'), mp.mpf('1')]:
        Ra = R_mp(zz)
        sig = 1 - zz*Ra
        actual = abs(sig - sig*zz/ee - sig/(ee*zz) + 1/(ee*zz) + sig/ee**2)
        bound = 3/(ee*zz*(zz**2+3)) + (1/(1+zz**2))*(1+1/ee**2+1/ee)
        assert actual <= bound + mp.mpf('1e-30')
        print(f"{float(zz):8.4g} {float(ee):6.3g} {float(actual):16.6e} {float(bound):20.6e}")
print()

print("=" * 78)
print("PART 4 -- SUMMARY: where does f's regularity actually enter (U)?")
print("=" * 78)
print("""
The two pieces bounded above (Parts 2-3) show that the "value-only" part
of the closed form (built from F1=f(x), F2=e^{-h/eps}f(x+h), KB=K_B(h)f(x)
-- i.e. the part of K(y,t)f(x) surviving the IBP identity applied to
rho's LEADING term f'(x+h')*sigma(z)) matches [f(x)-e^{-h/eps}f(x+h)]/z
to a RIGOROUS O(1/z^2) using ONLY hypothesis (B). This alone is a genuine
strengthening over every ancestor front's treatment of THIS piece (they
used a formal Mills-ratio SERIES for c(z), with no rigorous remainder
bound; here it is a fully explicit, provable double inequality).

What remains is the residual Efull := int_0^h e^{-h'/eps} E(h',z) dh',
E(h',z) := rho(h',z) - f'(x+h')*sigma(z)  [the part of the Watson-lemma
remainder BEYOND its leading linear-in-u term], multiplied by the
UNBOUNDED prefactor (1-eps*z)/eps ~ -z/eps for large z. This is where
f's regularity genuinely enters (verified quantitatively in s03):

  * under (C') ALONE (f Lipschitz-L1, t-uniform): the only bound
    available is |E(h',z)| <= 2*L1*sigma(z) = O(1/z^2) [same ORDER as
    rho itself -- no cancellation of its own leading term is available
    without more structure], so |(1-eps z)/eps * Efull| = O(1/z) --
    INSUFFICIENT to reach the target O(1/z^2).

  * under (C')+(C'') (f' ALSO Lipschitz-L2, t-uniform -- i.e. f in
    C^{1,1}, t-uniformly): |E(h',z)| <= (L2/2)*R''(z) <= L2/z^3 (s01
    G3, rigorous), giving |(1-eps z)/eps * Efull| = O(1/z^2) --
    SUFFICIENT.

CONCLUSION: this front's rigorous route proves (U) conditional on (B) +
(C')+(C'') -- i.e. conditional on a MILD but genuine strengthening of
(C') as literally named in this lineage's record (Lipschitz continuity
of Phi_t(.), t-uniform) to ALSO include Lipschitz continuity of Phi_t'(.)
(t-uniform), i.e. Phi_t in C^{1,1} uniformly in t. This is verified
quantitatively (both symbolically and via a concrete kink-function
numerical stress test) in s03/s04.
""")
