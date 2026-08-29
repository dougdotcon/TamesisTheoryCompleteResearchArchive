"""
Script 02 -- the GENERAL formal second-order Watson/Laplace correction
formula for an integral of the form I = int e^{g(t)} dt with a unique
interior non-degenerate maximum, derived symbolically here from scratch
(not cited from any file), plus a sanity check against a classical,
independently-known instance of exactly this same expansion (the Stirling
series for Gamma(z+1), itself a textbook Laplace-method computation) --
so the general machinery is validated on a case whose correct answer is
known from a source entirely outside this archive, BEFORE it is applied
to the archive's own g(t) in script 03.

Setup: let s := t - t*, A := -g''(t*) > 0 (so g(t*+s) = g(t*) - (A/2)s^2 +
(g'''(t*)/6) s^3 + (g''''(t*)/24) s^4 + O(s^5)). Substituting s = u/sqrt(A)
turns the quadratic piece into a standard unit Gaussian -u^2/2, and the
cubic/quartic terms into small parameters

    eps3 := g'''(t*) / (6 A^(3/2)),   eps4 := g''''(t*) / (24 A^2)

(both -> 0 as A -> infinity, provided g''', g'''' do not grow too fast --
this is exactly the "regularity/growth condition" that script 03 checks
explicitly for THIS front's specific integrand). Formally,

    I ~ e^{g(t*)} sqrt(2 pi / A) * [ 1 + Delta + O(eps^{5/2}) ],
    Delta := 3 eps4 + 15 eps3^2   (see derivation below; NOT 1/2 eps3^2,
                                    the correct even-moment weight for s^6
                                    is <s^6>_gaussian = 15).

This script derives that coefficients (3 and 15, or rather 1/8 and 5/24
after eps3, eps4 are folded back into g''', g''''/A powers) directly from
the Gaussian moments, purely symbolically, with sympy verifying the moment
integrals exactly.
"""
import sympy as sp

u, A, e3, e4, gppp_val, gpppp_val = sp.symbols('u A eps3 eps4 gppp gpppp', positive=True)

print("=== (A) Gaussian moments int_{-oo}^{oo} e^{-u^2/2} u^(2j) du / sqrt(2 pi) ===")
for j in range(0, 5):
    mom = sp.integrate(u**(2*j) * sp.exp(-u**2/2), (u, -sp.oo, sp.oo)) / sp.sqrt(2*sp.pi)
    print(f"  <u^{2*j}> = {sp.simplify(mom)}   (expect (2j-1)!! = {sp.factorial2(2*j-1) if j>0 else 1})")

print()
print("=== (B) Formal expansion of exp(eps3 u^3 + eps4 u^4) to the order that")
print("        contributes at O(eps4) ~ O(eps3^2), i.e. up to and including u^6 ===")
eps3, eps4 = sp.symbols('eps3 eps4')
expr = 1 + eps3*u**3 + eps4*u**4 + sp.Rational(1,2)*eps3**2*u**6
# integrate term by term against the *unnormalized* Gaussian weight e^{-u^2/2}
gaussian_norm = sp.sqrt(2*sp.pi)
integral_terms = []
for term in sp.Add.make_args(expr):
    coeff, u_pow = term.as_coeff_exponent(u) if term.has(u) else (term, 0)
    mom = sp.integrate(u**u_pow * sp.exp(-u**2/2), (u, -sp.oo, sp.oo))
    integral_terms.append(sp.simplify(coeff*mom))
total = sp.expand(sum(integral_terms) / gaussian_norm)
print("  (1/sqrt(2 pi)) * int e^{-u^2/2} [1 + eps3 u^3 + eps4 u^4 + eps3^2 u^6 / 2] du =")
print("   ", total)

Delta_formal = sp.expand(total - 1)
print()
print("So the bracket [1 + Delta] with Delta (to leading orders in eps3,eps4) =")
print("   Delta =", Delta_formal)

print()
print("=== (C) Substituting back eps3 = g'''(t*)/(6 A^{3/2}), eps4 = g''''(t*)/(24 A^2) ===")
gppp_t, gpppp_t, Asym = sp.symbols("g3star g4star A", positive=True)
eps3_sub = gppp_t / (6*Asym**sp.Rational(3,2))
eps4_sub = gpppp_t / (24*Asym**2)
Delta_explicit = Delta_formal.subs({eps3: eps3_sub, eps4: eps4_sub})
Delta_explicit = sp.simplify(Delta_explicit)
print("  Delta(n,m,gamma) =", Delta_explicit)
print("  i.e. Delta = g''''(t*)/(8 A^2)  +  5 [g'''(t*)]^2 / (24 A^3)")

# Confirm the two named closed-form pieces match by direct algebra
claim = gppp_t**2*5/(24*Asym**3) + gpppp_t/(8*Asym**2)
print("  difference from claimed closed form:", sp.simplify(Delta_explicit - claim), "(expect 0)")

print()
print("=== (D) SANITY CHECK against a source EXTERNAL to this archive:")
print("        Stirling's series for Gamma(z+1) = int_0^oo t^z e^{-t} dt,")
print("        z=n, via the SAME formal machinery derived above. ===")
# g(t) := n ln t - t, maximized at t* = n, A = -g''(t*) = n/t*^2 = 1/n
z = sp.symbols('z', positive=True)
tt = sp.symbols('tt', positive=True)
g_gamma = z*sp.log(tt) - tt
gpp_gamma = sp.diff(g_gamma, tt, 2)
gppp_gamma = sp.diff(g_gamma, tt, 3)
gpppp_gamma = sp.diff(g_gamma, tt, 4)
tstar_gamma = z  # standard: g'(t)=z/t - 1=0 => t*=z
A_gamma = sp.simplify(-gpp_gamma.subs(tt, tstar_gamma))
g3_gamma = sp.simplify(gppp_gamma.subs(tt, tstar_gamma))
g4_gamma = sp.simplify(gpppp_gamma.subs(tt, tstar_gamma))
print("  A =", A_gamma, "  g'''(t*) =", g3_gamma, "  g''''(t*) =", g4_gamma)

Delta_gamma_case = Delta_explicit.subs({Asym: A_gamma, gppp_t: g3_gamma, gpppp_t: g4_gamma})
Delta_gamma_case = sp.simplify(Delta_gamma_case)
print("  Formal Delta for the Gamma-function case =", Delta_gamma_case)
print("  Known Stirling correction Gamma(z+1) ~ sqrt(2 pi z) (z/e)^z (1 + 1/(12z) + ...):")
print("  predicted 1/(12z) vs. our Delta:", sp.simplify(Delta_gamma_case - sp.Rational(1,12)/z), "(expect 0)")
print()
print("This confirms the general Delta formula derived in (A)-(C) reproduces")
print("the CLASSICAL, textbook-known Stirling correction 1/(12z) EXACTLY on a")
print("case with a source of truth entirely external to this archive -- the")
print("general Watson/Laplace second-order machinery used in script 03 for")
print("this front's own g(t) is validated before being applied there.")
