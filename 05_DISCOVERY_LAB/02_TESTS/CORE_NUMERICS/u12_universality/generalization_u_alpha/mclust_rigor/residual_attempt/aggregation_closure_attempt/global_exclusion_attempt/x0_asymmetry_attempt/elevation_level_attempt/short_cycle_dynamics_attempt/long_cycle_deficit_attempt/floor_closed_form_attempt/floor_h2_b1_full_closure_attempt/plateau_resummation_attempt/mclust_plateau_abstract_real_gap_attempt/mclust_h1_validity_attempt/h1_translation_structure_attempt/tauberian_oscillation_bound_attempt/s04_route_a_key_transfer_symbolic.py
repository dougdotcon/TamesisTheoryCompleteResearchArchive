"""
s04_route_a_key_transfer_symbolic.py

TAUBERIAN-OSCILLATION-BOUND-ATTEMPT, wave 26 front (c).

Mandate candidate route (a): transfer the ALREADY-PROVED oscillation bound
on Psi, "(star-star)" (h1_energy_estimate_attempt Sec 5.1, cited):
    sup_x |Psi(x,y2)-Psi(x,y1)|  <=  (y2-y1)*K*R(y1)  <=  (y2-y1)*K/y1
to Phi, via the exact identities (E1),(KEY),(E2) (cited, record facts):
    Psi_x = (x+y)Psi - I,   I := int_0^y Phi(x,y') dy'                 (E1)
    W = Psi - eps * dPsi/dx                                            (KEY)
    Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv    (E2)

This script checks, symbolically/algebraically, exactly how far this route
gets and exactly where it stalls -- independent of, and prior to, the
successful route (b) pursued in s01/s02/main document.

Written FRESH; sympy for exact algebraic manipulation, no ancestor .py
opened or imported.
"""
import sympy as sp

print("=" * 90)
print("STEP 1: an algebraic simplification of (KEY), substituting (E1)")
print("=" * 90)

x, y, eps, Psi, Psi_x, I = sp.symbols('x y eps Psi Psi_x I', real=True)
z = x + y
My = (1 - eps * z) / eps

# (E1): Psi_x = (x+y)*Psi - I  =>  Psi_x_expr
Psi_x_expr = z * Psi - I

# (KEY): W = Psi - eps*Psi_x
W_via_KEY = Psi - eps * Psi_x_expr
W_via_KEY_simplified = sp.expand(W_via_KEY)
print(f"W = Psi - eps*Psi_x, substituting Psi_x=(x+y)Psi-I:")
print(f"  W = {W_via_KEY_simplified}")

# claim: W = eps*(My*Psi + I)
W_claim = eps * (My * Psi + I)
diff = sp.simplify(W_via_KEY_simplified - W_claim)
print(f"\n[check] W - eps*(M_y*Psi + I) = {diff}  (should be 0)")
assert diff == 0
print("-> PASS: W(x,y) = eps*[M_y*Psi(x,y) + I(x,y)]  -- exact algebraic")
print("   identity, a new (to this front) simplification combining (KEY)")
print("   and (E1); NOT independently a new fact (both inputs are already")
print("   record facts), just a re-packaging.")

print()
print("=" * 90)
print("STEP 2: why this does NOT let (star-star) [on Psi] control W's")
print("oscillation without EXTRA information")
print("=" * 90)
print("""
Delta_W(x) := W(x,y2) - W(x,y1)
            = eps*[M_y2*Psi(x,y2) - M_y1*Psi(x,y1)]  +  eps*[I(x,y2)-I(x,y1)]

Expand the first bracket (M_y2 = M_y1 - Delta, Delta:=y2-y1, since M_y=1/eps-z
and z2=z1+Delta):
""")
y1s, y2s, Delta_s = sp.symbols('y1 y2 Delta', positive=True)
z1s = x + y1s
z2s = x + y2s
My1 = (1 - eps * z1s) / eps
My2 = (1 - eps * z2s) / eps
Psi1, Psi2 = sp.symbols('Psi1 Psi2', real=True)
bracket1 = sp.expand(My2 * Psi2 - My1 * Psi1)
# rewrite as My2*(Psi2-Psi1) + (My2-My1)*Psi1
rewrite = sp.expand(My2 * (Psi2 - Psi1) + (My2 - My1) * Psi1)
check2 = sp.simplify(bracket1 - rewrite)
print(f"[check] M_y2*Psi2 - M_y1*Psi1  ==  M_y2*(Psi2-Psi1) + (M_y2-M_y1)*Psi1 ? "
      f"residual={check2}")
assert check2 == 0
My2_minus_My1 = sp.simplify(My2 - My1)
print(f"\nM_y2 - M_y1 = {My2_minus_My1}  (exactly -(y2-y1), a CONTROLLED, O(Delta)")
print("  quantity -- this part is FINE, poses no obstruction.)")
print()
My2_expr_at_large_z = My2
print("BUT M_y2 itself = 1/eps - z2  ->  -infinity as y2->infinity (UNBOUNDED,")
print("linearly in z2) -- so 'M_y2*(Psi2-Psi1)' is a product of an UNBOUNDED")
print("(in y2) quantity M_y2 and the OSCILLATION we are trying to bound.")
print("(star-star) bounds |Psi2-Psi1| by O(Delta/y1) -- multiplying by")
print("|M_y2|~O(z2)~O(y2) gives O(Delta*y2/y1), which for Delta=delta*y1 is")
print("O(delta*y2) -- LINEARLY GROWING in y2, NOT vanishing. The naive")
print("product bound is USELESS here (this is exactly the same 'M_y is")
print("individually unbounded' fact that h1_translation_structure_attempt's")
print("whole Part A/B was built to show gets RESCUED only by an EXACT")
print("cancellation against the OTHER piece of the kernel (K_B) -- a")
print("cancellation specific to the Phi Volterra equation's own kernel")
print("structure, which is NOT available here: M_y2*(Psi2-Psi1) has no")
print("companion term to cancel against inside (KEY) alone.")
print()
print("The eps*[I(x,y2)-I(x,y1)] term: I(x,y2)-I(x,y1) = int_{y1}^{y2}")
print("Phi(x,y')dy' + [does NOT reduce further without knowing Phi's own")
print("behavior on [y1,y2] -- circular if the goal IS to bound Phi's")
print("oscillation]. Bounded crudely by Delta*M_Phi (fine, O(delta*y1),")
print("i.e. O(delta) after normalizing by z ~ y1 in a LATER step -- but")
print("this crude bound is exactly as strong as what route (b) already")
print("gets directly, with none of route (a)'s extra apparatus.")

print()
print("=" * 90)
print("STEP 3: the DIRECT route via (KEY) alone (not via E1-substitution)")
print("hits the SAME wall from a different angle: needs d/dx of Delta_Psi")
print("=" * 90)
print("""
W = Psi - eps*Psi_x  directly (no E1 substitution):
  Delta_W(x) = Delta_Psi(x) - eps * d/dx[Delta_Psi(x)]

(star-star) bounds sup_x|Delta_Psi(x)| -- a SUP-NORM bound on Delta_Psi
ITSELF, not on its x-DERIVATIVE. Bounding d/dx[Delta_Psi(x)] would need a
SEPARATE oscillation-type bound on Psi_x(x,y2)-Psi_x(x,y1), which is NOT
part of (star-star) and is not derived anywhere in the required reading
(h1_energy_estimate_attempt Sec 8.4 names exactly this "derivative loss"
as the reason its OWN contraction-mapping route via (BB-Psi') does not
close either -- differentiating an identity in x requires control of the
x-derivative of the difference, not merely the difference itself). This
front's own algebra above confirms, via the (E1)-substituted route, that
even AVOIDING an explicit Psi_x term does not avoid the underlying
obstruction -- it resurfaces as the unbounded-M_y-times-oscillation term
in Step 2. Two syntactically different routes into the SAME wall.
""")

print("=" * 90)
print("CONCLUSION")
print("=" * 90)
print("""
Route (a) -- transferring (star-star) from Psi to Phi via (KEY)/(E2) or the
algebraically-equivalent (E1)-substituted form -- does NOT close the gap.
Both forms of the attempt reduce to needing EITHER an oscillation bound on
Psi_x (not available) OR a bound on M_y*(Psi2-Psi1) that requires exactly
the kind of exact, structure-specific cancellation
h1_translation_structure_attempt found for the Phi-Volterra kernel
K(y,t)=M_y*K_A^raw+K_B specifically -- a cancellation NOT available for the
raw (KEY) identity applied directly to Psi (there is no "K_B-like"
companion term here to cancel M_y*Delta_Psi against). Route (a) is,
precisely, a DEAD END -- confirming and sharpening (not merely repeating)
h1_energy_estimate_attempt Sec 8.4's general "derivative loss" diagnosis
into the SPECIFIC obstruction for THIS route (an unbounded M_y multiplying
an O(Delta/y1) oscillation, rather than an abstractly-named derivative-loss
issue). Route (b) (this front's s01/s02/main document), which works
DIRECTLY off the ALREADY-CANCELLATION-AWARE closed-form kernel for
K(y,t) rather than re-deriving a fresh cancellation for W, is the only one
of the two mandate-named routes that succeeds (with the caveats named
throughout this front's other scripts and the main document).
""")
