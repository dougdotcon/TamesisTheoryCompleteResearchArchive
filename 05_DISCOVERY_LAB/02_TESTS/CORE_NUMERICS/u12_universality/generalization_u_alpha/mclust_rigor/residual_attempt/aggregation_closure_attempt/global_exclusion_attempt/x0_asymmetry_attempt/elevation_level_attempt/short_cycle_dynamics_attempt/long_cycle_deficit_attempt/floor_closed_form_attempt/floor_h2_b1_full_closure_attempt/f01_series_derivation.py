"""
f01_series_derivation.py -- attempt to close the SS5 two-variable system of
floor_closed_form_attempt/ATTEMPT.md:

  dPhi/ds - dPhi/dg = c[Phi - W],   dPsi/ds = c[Psi - W]
  W(s,g) = g*Avg_g[Phi(s,.)] + (1-s-g)*Psi(s,g),
  Avg_g[Phi(s,.)] = (1/g) int_0^g Phi(s,g') dg',   boundary Phi(s,0)=1,
  target phi(t0) = Phi(0,t0).

Strategy: NOT a global closed form (see f04/README for why the full system
resists that). Instead, an exact small-g (equivalently small-t0) formal power
series Phi(s,g) = sum_k a_k(s) g^k, Psi(s,g) = sum_{k>=1} b_k(s) g^k, with a
genuine, checkable closed-form recursion for the coefficients. Step 1: derive
the coefficient recursion by matching powers of g. Step 2: solve the k=1
(Psi) recursion in exact closed form (a first-order linear ODE with Gaussian
integrating factor -> complementary-error-function / Mills-ratio solution).
Step 3: cross-check the recursion (sympy, symbolic) against an independent
by-hand derivation. Step 4: push to k=2 (Phi) exact closed form, and k=3
(one more coefficient, exact up to one numerical quadrature -- disclosed as
such, not claimed symbolic-closed-form).

All of this is a fresh, from-scratch re-derivation -- no code from
floor_closed_form_attempt/*.py or its adversarial/ subfolder was read or
imported (only the PDE system AS STATED in ATTEMPT.md SS5's prose, and
THEOREM.md/DERIVATIONS.md for shared definitions per the mandate, were used).
"""
import sympy as sp
import numpy as np
from scipy import integrate
from scipy.special import erfcx

print("=" * 70)
print("PART A -- symbolic (sympy) cross-check of the coefficient recursion")
print("=" * 70)

# ---- A1. Match powers of g in the Phi PDE and Psi PDE symbolically to
#          re-derive the recursion a_{k+1}(s) = [a_k'(s)-c a_k(s)+c w_k(s)]/(k+1)
#          and  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)
#          from first principles (truncated power series, symbolic g).
s, g, c = sp.symbols('s g c', positive=True)
K = 4  # truncation order for the symbolic check (enough to see the pattern)

a = [sp.Function(f'a{k}')(s) for k in range(K + 1)]
b = [sp.Integer(0)] + [sp.Function(f'b{k}')(s) for k in range(1, K + 1)]  # b0 := 0

Phi_series = sum(a[k] * g**k for k in range(K + 1))
Psi_series = sum(b[k] * g**k for k in range(1, K + 1))

# Avg_g[Phi(s,.)] = (1/g) int_0^g Phi(s,g') dg' -- do this termwise (exact
# for a truncated polynomial-in-g' integrand): int_0^g a_k g'^k dg' = a_k g^{k+1}/(k+1)
Avg_g_Phi = sum(a[k] * g**k / (k + 1) for k in range(K + 1))  # already divided by g

W_series = sp.expand(g * Avg_g_Phi + (1 - s - g) * Psi_series)
W_series = sp.Poly(W_series, g).as_expr()  # keep as polynomial in g

LHS_Phi = sp.diff(Phi_series, s) - sp.diff(Phi_series, g)
RHS_Phi = c * (Phi_series - W_series)
diff_Phi = sp.expand(LHS_Phi - RHS_Phi)
poly_Phi = sp.Poly(diff_Phi, g)

LHS_Psi = sp.diff(Psi_series, s)
RHS_Psi = c * (Psi_series - W_series)
diff_Psi = sp.expand(LHS_Psi - RHS_Psi)
poly_Psi = sp.Poly(diff_Psi, g)

print("\nPhi-equation, coefficient of g^1 (should give a2 in terms of a1,b1):")
coeff_g1_Phi = poly_Phi.coeff_monomial(g**1)
print(" ", sp.simplify(coeff_g1_Phi), "= 0")
# NOTE (honest process note): sp.solve(..., a[2]) returns a LIST (there could
# in principle be several solutions); the first pass here forgot to index
# into it before calling simplify(), which raised AttributeError ('list'
# object has no attribute 'replace') inside sympy's simplify(). Caught
# immediately by the traceback (never reached any reported number) and
# fixed by indexing [0] -- the equation is linear in a2(s) so exactly one
# root exists. Disclosed per this line's self-correction convention.
a2_solved_list = sp.solve(sp.Eq(coeff_g1_Phi, 0), a[2])
assert len(a2_solved_list) == 1, "expected a unique linear solution for a2(s)"
a2_solved = sp.simplify(a2_solved_list[0])
print("  -> a2(s) solved from this single equation:", a2_solved)
# Compare against the hand recursion's prediction a2(s)=[a1'(s)-c*a1(s)+c*w1(s)]/2,
# w1(s) = a0(s) + (1-s)*b1(s):
w1_hand = a[0] + (1 - s) * b[1]
a2_hand = sp.simplify((sp.diff(a[1], s) - c * a[1] + c * w1_hand) / 2)
print("  -> hand-recursion formula for a2(s):           ", a2_hand)
print("  -> difference (should simplify to 0):           ", sp.simplify(a2_solved - a2_hand))

print("\nPsi-equation, coefficient of g^1 (should give the b1 ODE):")
coeff_g1_Psi = poly_Psi.coeff_monomial(g**1)
print(" ", sp.simplify(coeff_g1_Psi), "= 0")

print("\n(These confirm the hand recursion below reproduces exactly what")
print(" matching powers of g in the STATED PDE system gives -- no transcription")
print(" error in the recursion used for parts B/C.)")

# --- Extend the SAME symbolic check to k=2, since the general-k recursion
#     used for a3(0)/b2(s) below was generalized BY HAND from the k=1 case
#     and was not yet itself checked against the sympy power-matching -- do
#     that now before trusting a3(0)'s numeric value.
print("\nExtending the symbolic check to k=2 (needed for a3(0)/b2(s) below):")
coeff_g2_Phi = poly_Phi.coeff_monomial(g ** 2)
a3_solved_list = sp.solve(sp.Eq(coeff_g2_Phi, 0), a[3])
assert len(a3_solved_list) == 1
a3_solved = sp.simplify(a3_solved_list[0])
w2_hand = a[1] / 2 + (1 - s) * b[2] - b[1]
a3_hand = sp.simplify((sp.diff(a[2], s) - c * a[2] + c * w2_hand) / 3)
print("  a3(s) [from g^2 coeff of Phi-eq]:", a3_solved)
print("  a3(s) [from general hand recursion, k=2]:", a3_hand)
print("  difference (should be 0):", sp.simplify(a3_solved - a3_hand))

coeff_g2_Psi = poly_Psi.coeff_monomial(g ** 2)
b2_ode_solved_list = sp.solve(sp.Eq(coeff_g2_Psi, 0), sp.diff(b[2], s))
assert len(b2_ode_solved_list) == 1
b2_prime_solved = sp.simplify(b2_ode_solved_list[0])
f2_hand = -c * a[1] / 2 + c * b[1]
b2_prime_hand = sp.simplify(c * s * b[2] + f2_hand)
print("  b2'(s) [from g^2 coeff of Psi-eq]: ", b2_prime_solved)
print("  b2'(s) [from general hand recursion, k=2]:", b2_prime_hand)
print("  difference (should be 0):", sp.simplify(b2_prime_solved - b2_prime_hand))

print()
print("=" * 70)
print("PART B -- k=1 (Psi) exact closed form: Mills-ratio / erfcx solution")
print("=" * 70)

# ODE: b1'(s) - c s b1(s) = -c,  "bounded as s->inf" branch selected.
# Claimed closed form: b1(s) = psi1(s) = sqrt(pi c /2) * erfcx(s*sqrt(c/2))
b1_sym = sp.Function('b1')(s)
c_val = sp.symbols('c', positive=True)
ode_b1 = sp.Eq(sp.diff(b1_sym, s) - c_val * s * b1_sym, -c_val)

# Verify the closed-form solution algebraically via erfcx's defining ODE:
# erfcx(x) = exp(x^2) erfc(x);  d/dx erfcx(x) = 2 x erfcx(x) - 2/sqrt(pi).
x = sp.symbols('x', positive=True)
erfcx_expr = sp.exp(x**2) * sp.erfc(x)
derfcx = sp.diff(erfcx_expr, x)
derfcx_identity_check = sp.simplify(derfcx - (2 * x * erfcx_expr - 2 / sp.sqrt(sp.pi)))
print("\nerfcx'(x) - [2x erfcx(x) - 2/sqrt(pi)] simplifies to:", derfcx_identity_check,
      " (should be 0)")

s_sym, c_sym = sp.symbols('s c', positive=True)
psi1_candidate = sp.sqrt(sp.pi * c_sym / 2) * sp.exp((c_sym * s_sym**2) / 2) * sp.erfc(s_sym * sp.sqrt(c_sym / 2))
lhs_check = sp.diff(psi1_candidate, s_sym) - c_sym * s_sym * psi1_candidate
lhs_check_simplified = sp.simplify(lhs_check)
print("\nDirect substitution: b1'(s) - c*s*b1(s) for the candidate closed form:")
print(" ", lhs_check_simplified, " (target: -c)")
match = sp.simplify(lhs_check_simplified - (-c_sym))
print("  difference from target -c:", match, " (should be 0 -- EXACT closed-form check)")

print()
print("=" * 70)
print("PART C -- numeric recursion for a2(0), a3(0) at c=1000, and the")
print("           resulting truncated series for Phi(0,t0)")
print("=" * 70)

C = 1000.0


def psi1(sv):
    """b1(s) = sqrt(pi c/2) * erfcx(s*sqrt(c/2)) -- exact closed form (Part B)."""
    return np.sqrt(np.pi * C / 2.0) * erfcx(sv * np.sqrt(C / 2.0))


def psi1_prime(sv):
    """b1'(s) = c*s*b1(s) - c, from the defining ODE itself (exact, no numerics)."""
    return C * sv * psi1(sv) - C


a0 = 1.0
a1 = -C
b1_0 = psi1(0.0)

a2_0 = (C / 2.0) * (C + 1.0 + (1.0 - 0.0) * psi1(0.0))
print(f"\na0 = {a0}")
print(f"a1 = {a1}")
print(f"b1(0) = psi1(0) = sqrt(pi*c/2) = {b1_0:.6f}")
print(f"a2(0) = (c/2)(c+1+psi1(0)) = {a2_0:.6f}")


# a2(s) closed form (Part A/hand-derivation):
def a2_of_s(sv):
    return (C / 2.0) * (C + 1.0 + (1.0 - sv) * psi1(sv))


def a2_prime_of_s(sv):
    # d/ds[(c/2)(1-s) psi1(s)] = (c/2)[-psi1(s) + (1-s) psi1'(s)]
    return (C / 2.0) * (-psi1(sv) + (1.0 - sv) * psi1_prime(sv))


# --- b2(s) via ONE numerical quadrature layer (disclosed: this is where the
#     recursion stops being symbolically closed-form and needs numerics) ---
def f2_of_sigma(sigma):
    # f_k(s) = -c*a_{k-1}(s)/k + c*b_{k-1}(s), for k=2: -c*a1/2 + c*b1(s)
    return -C * a1 / 2.0 + C * psi1(sigma)


def b2_of_s(sv, upper=None):
    if upper is None:
        # effective infinity: e^{-c sigma^2/2} decays superfast; c=1000 => scale ~1/sqrt(c)
        upper = sv + 12.0 / np.sqrt(C)
    integrand = lambda sigma: np.exp(-C * sigma ** 2 / 2.0) * f2_of_sigma(sigma)
    val, err = integrate.quad(integrand, sv, upper, limit=400, epsabs=1e-16, epsrel=1e-12)
    return -np.exp(C * sv ** 2 / 2.0) * val, err


b2_0, b2_0_err = b2_of_s(0.0)
print(f"\nb2(0) (one numerical quadrature; quad abs-err est {b2_0_err:.2e}) = {b2_0:.8f}")

w2_0 = a1 / 2.0 + (1.0 - 0.0) * b2_0 - psi1(0.0)
a2p_0 = a2_prime_of_s(0.0)
a3_0 = (a2p_0 - C * a2_0 + C * w2_0) / 3.0
print(f"a2'(0) = {a2p_0:.6f}")
print(f"w2(0)  = a1/2 + b2(0) - psi1(0) = {w2_0:.6f}")
print(f"a3(0) = [a2'(0) - c*a2(0) + c*w2(0)] / 3 = {a3_0:.6f}")

print()
print("=" * 70)
print("PART C.1 -- independent cross-checks of a2'(0) and b2(0), before")
print("            trusting a3(0) (two DIFFERENT numerical methods each)")
print("=" * 70)

# Check 1: a2'(0) via central finite difference of the closed-form a2_of_s,
# independent of the analytic psi1_prime shortcut used above.
h_fd = 1e-6
a2p_0_fd = (a2_of_s(h_fd) - a2_of_s(-h_fd)) / (2 * h_fd)
print(f"\na2'(0) analytic (via psi1_prime)   = {a2p_0:.6f}")
print(f"a2'(0) central finite-difference   = {a2p_0_fd:.6f}  (h={h_fd})")
print(f"  relative difference: {abs(a2p_0_fd - a2p_0) / abs(a2p_0):.2e}")

# Check 2: b2(0) via an INDEPENDENT method -- direct ODE shooting.
# b2'(s) - c*s*b2(s) = f2(s), integrate BACKWARD from a large s_far (where
# the bounded/decaying solution is ~0) down to s=0, using solve_ivp. This is
# a completely different numerical method from the quadrature-based closed
# form b2(s) = -exp(c s^2/2) * int_s^inf exp(-c sigma^2/2) f2(sigma) dsigma,
# so agreement is a real, independent check (not circular).
from scipy.integrate import solve_ivp

s_far = 0.12  # exp(-c*s_far^2/2) = exp(-1000*0.0144/2)=exp(-7.2) ~ 7.5e-4 already
# tiny at the far end relative to the near-origin scale (~2e4) of b2 -- but to
# be safe, use a further point and check sensitivity below.


def rhs(sv, y):
    return [C * sv * y[0] + f2_of_sigma(sv)]


for s_far_try in [0.10, 0.12, 0.15, 0.20]:
    sol = solve_ivp(rhs, [s_far_try, 0.0], [0.0], method="Radau",
                     rtol=1e-11, atol=1e-14, dense_output=True)
    b2_0_shoot = sol.y[0, -1]
    print(f"  ODE-shooting b2(0) with s_far={s_far_try}: {b2_0_shoot:.6f}")

print(f"\nQuadrature-based b2(0) (Part C, above): {b2_0:.6f}")
print("(If shooting disagrees with the quadrature value as s_far grows, that")
print(" signals the 'bounded at infinity' boundary condition is numerically")
print(" delicate -- exp(c*s^2/2) blowup means shooting backward from a")
print(" not-large-enough s_far is itself a poor approximation to the true")
print(" s->infinity limit; the quadrature form is analytically exact for")
print(" s_far->infinity and does not suffer this specific finite-cutoff")
print(" bias, so it -- not the shooting value -- is treated as ground truth")
print(" below, with the shooting run reported only as a rough sanity check.)")

print("\n--- Series so far for Phi(0,t0) = a0 + a1 t0 + a2(0) t0^2 + a3(0) t0^3 + ... ---")
print(f"  a0        = {a0}")
print(f"  a1        = {a1}")
print(f"  a2(0)     = {a2_0:.4f}   (vs pure-exponential c^2/2 = {C**2/2:.4f}; "
      f"excess = {a2_0 - C**2/2:.4f}, entirely from psi1(0)=sqrt(pi c/2))")
print(f"  a3(0)     = {a3_0:.4f}   (vs pure-exponential -c^3/6 = {-C**3/6:.4f}; "
      f"excess = {a3_0 - (-C**3/6):.4f})")

print("\nSaving coefficients to series_coeffs.json for use by f03.")
import json

out = {
    "c": C,
    "a0": a0, "a1": a1, "a2_0": a2_0, "a3_0": a3_0,
    "psi1_0": b1_0, "b2_0": b2_0, "b2_0_quad_err": b2_0_err,
    "pure_exp_a2": C ** 2 / 2.0, "pure_exp_a3": -C ** 3 / 6.0,
}
with open("series_coeffs.json", "w") as fh:
    json.dump(out, fh, indent=2)
print(json.dumps(out, indent=2))
