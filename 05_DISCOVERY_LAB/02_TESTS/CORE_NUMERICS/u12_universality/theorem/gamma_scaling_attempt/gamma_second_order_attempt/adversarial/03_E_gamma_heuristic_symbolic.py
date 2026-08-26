"""
Independent symbolic re-derivation of Sec 4's heuristic E(gamma).

The document claims (Sec 4):
  E(gamma) ~= gamma(1-gamma)/(4 beta) + coef/(2 beta^2)
  coef := -(1-(1-gamma)^3)/6 + gamma(1-gamma)^3/2
and that this "sympy reduces" to
  E_heuristic(gamma) = (-3g^2+7g-6) / (6(g-2)^2)
which is claimed to match, EXACTLY symbolically, E(gamma) := D(gamma) - D_0(gamma)
from Lemma E's D-equiv and Lemma D0's closed form.

This script redoes both pieces of algebra completely independently.
"""
import sympy as sp

g = sp.symbols('gamma', positive=True)
beta = g * (2 - g) / 2

print("=== Step 1: reduce the document's E_heuristic formula from its own stated pieces ===")
coef = -(1 - (1 - g) ** 3) / 6 + g * (1 - g) ** 3 / 2
E_heur_raw = g * (1 - g) / (4 * beta) + coef / (2 * beta ** 2)
E_heur_reduced = sp.simplify(E_heur_raw)
print("E_heuristic(gamma), reduced from raw pieces:", E_heur_reduced)

E_heur_claimed = (-3 * g ** 2 + 7 * g - 6) / (6 * (g - 2) ** 2)
print("Document's claimed closed form:            ", E_heur_claimed)
diff_step1 = sp.simplify(E_heur_raw - E_heur_claimed)
print("Difference (raw pieces vs claimed closed form), should be 0:", diff_step1)

print("\n=== Step 2: independently recompute E(gamma) := D(gamma) - D0(gamma) ===")
D_of_gamma = -sp.Rational(1, 3) * (6 - 8 * g + 3 * g ** 2) / (2 - g) ** 2   # from Lemma E / D-equiv
D0_of_gamma = (g - 1) / (2 * (2 - g))                                       # from Lemma D0
E_target = sp.simplify(D_of_gamma - D0_of_gamma)
print("D(gamma)  =", D_of_gamma)
print("D0(gamma) =", D0_of_gamma)
print("E(gamma) = D(gamma)-D0(gamma), simplified:", E_target)

print("\n=== Step 3: the central claim -- do the heuristic and the target match EXACTLY? ===")
diff_final = sp.simplify(E_heur_claimed - E_target)
print("E_heuristic(gamma) - E(gamma) simplifies to:", diff_final)
diff_final_raw = sp.simplify(E_heur_raw - E_target)
print("(sanity, using the RAW un-simplified heuristic pieces directly):", diff_final_raw)

# numeric spot check at several points, incl. irrational ones, to rule out
# a coincidental polynomial identity that only happens to match at a few
# rational points (paranoia check)
print("\n=== Step 4: numeric spot-check at several points (rational and irrational) ===")
for val in [sp.Rational(1, 10), sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(9, 10),
            sp.sqrt(2) / 2, sp.pi / 4]:
    a = E_heur_claimed.subs(g, val)
    b = E_target.subs(g, val)
    print(f"gamma={float(val):.6f}: E_heuristic={sp.N(a,20)}  E_target={sp.N(b,20)}  "
          f"diff={sp.N(a-b,20)}")

print("\n=== Step 5: internal-consistency check of the order-counting claims in Sec 4 ===")
print("Checking the two cited Gaussian-moment asymptotics used to go from Q(k;n,gamma) to E(gamma):")
print("  Sum_k k e^{-beta k^2/n} ~ n/(2 beta)   [[from wave-17 Lemma 5(c), cited]]")
print("  Sum_k k^3 e^{-beta k^2/n} ~ n^2/(2 beta^2)")
n = sp.symbols('n', positive=True)
b = sp.symbols('b', positive=True)  # beta placeholder for the Gaussian-integral identity
# Using Lemma5(c) closed forms from wave-17 ATTEMPT.md (cited, already proved there):
# int_0^inf x e^{-b x^2} dx = 1/(2b);  int_0^inf x^3 e^{-b x^2} dx = 1/(2 b^2)
x = sp.symbols('x', positive=True)
I1 = sp.integrate(x * sp.exp(-b * x ** 2), (x, 0, sp.oo))
I3 = sp.integrate(x ** 3 * sp.exp(-b * x ** 2), (x, 0, sp.oo))
print("  int_0^inf x e^{-b x^2} dx =", I1, " (with b=beta/n, this is n/(2 beta) -- check:",
      sp.simplify(I1.subs(b, beta / n) - n / (2 * beta)), ")")
print("  int_0^inf x^3 e^{-b x^2} dx =", I3, " (with b=beta/n, this is n^2/(2 beta^2) -- check:",
      sp.simplify(I3.subs(b, beta / n) - n ** 2 / (2 * beta ** 2)), ")")

print("\nRebuilding E(gamma)_approx from Q(k;n,gamma) summed against these moments, from scratch")
# Q(k;n,gamma) = k*gamma(1-gamma)/(2n)  -  k^3[1-(1-gamma)^3]/(6 n^2)  +  k^3 gamma(1-gamma)^3/(2 n^2)
# Sum_k e^{-s(k)} Q(k;n,gamma)  ~  gamma(1-gamma)/(2n) * [n/(2 beta)]
#                                 + [-[1-(1-gamma)^3]/6 + gamma(1-gamma)^3/2]/n^2 * [n^2/(2 beta^2)]
term1 = (g * (1 - g) / (2 * n)) * (n / (2 * beta))
term2 = (-(1 - (1 - g) ** 3) / 6 + g * (1 - g) ** 3 / 2) / n ** 2 * (n ** 2 / (2 * beta ** 2))
E_rebuilt = sp.simplify(term1 + term2)
print("Rebuilt E(gamma) from first principles (own derivation, not copying doc's coef grouping):",
      E_rebuilt)
print("Matches document's E_heur_raw?  diff =", sp.simplify(E_rebuilt - E_heur_raw))
print("Matches E_target (D-D0)?        diff =", sp.simplify(E_rebuilt - E_target))
