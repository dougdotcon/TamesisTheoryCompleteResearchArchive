"""
k01_watson_bookkeeping_sympy.py -- MCLUST-H2-VALIDITY-ATTEMPT

Fresh, from-scratch symbolic verification of the CENTRAL claim of this
front's theoretical reduction of H2: that the "y-differentiated
homogeneous equation" governing chi_n(x,y) := d(psi_n)/dy is HOMOGENEOUS
at every perturbative order n (not just n=1, the only order the required
reading states this for), GIVEN the Watson/eps-expansion bookkeeping of
Phi in terms of W = Psi - eps*Psi_x (the (KEY) identity of the required
reading) to all orders, and GIVEN the previously-established orders
1..n-1 are already known to be y-independent.

No .py file from any ancestor front (mclust_rigor lineage, down through
mclust_h1_validity_attempt) was opened, read, or imported. Everything
below is re-derived from the PROSE of the required reading:
  - (E1):  Psi_x(x,y) = (x+y)*Psi(x,y) - I(x,y),  I := int_0^y Phi dy'
  - (KEY): W = Psi - eps*Psi_x
  - (E2):  Phi(x,y) = e^{-y/eps} + (1/eps)*int_0^y e^{-v/eps} W(x+v,y-v) dv
  - the required reading's own explicit leading-order statement
    "Phi = W + eps*(W_x - W_y) + O(eps^2)" (plateau_resummation_attempt
    ATTEMPT.md Section 4.2), which is the m=0,1 case of the GENERAL
    Watson/Taylor operator expansion used below,
        Phi(x,y) ~ sum_{m>=0} eps^m * (d/dx - d/dy)^m W(x,y)
    (outer region y >> eps, dropping the exponentially small e^{-y/eps}
    boundary-layer term and extending the integral's upper limit to
    infinity -- both standard, and both already used, in the m=0,1 case,
    by the required reading itself; this script uses the operator
    literally, to ALL orders, via repeated application of d/dx-d/dy,
    with NO extra 1/m! factor -- verified explicitly below that the
    moment integral (1/eps) int_0^inf e^{-v/eps} v^m/m! dv = eps^m
    exactly cancels the Taylor 1/m!, so the m-th operator power carries
    coefficient exactly 1, not 1/m!).

STEP 0 below re-derives/verifies this moment-integral cancellation
itself (symbolically, exact) before it is used for anything.

STEP 1 re-derives the ORDER-1 result already stated in the required
reading (psi1_xy = (x+y)*psi1_y, homogeneous) directly from the
required reading's own explicit psi1 equation, as an independent
sanity check before generalizing.

STEP 2 is the new content: derive, from (E1)'s EXACT y-derivative
identity (Psi_xy = Psi + (x+y)*Psi_y - Phi, valid before any
eps-expansion) combined with the Watson-operator formula for Phi's
order-n coefficient phi_n in terms of the omega_k := psi_k -
d(psi_{k-1})/dx (k=1..n, psi_0:=0, the (KEY)-identity order-n
coefficients of W), the quantity

    f_n := psi_n - phi_n

order by order, n = 1..N_MAX, INDUCTIVELY substituting the
already-verified fact "psi_k depends on x only" (k < n) at each step
(enforced by representing resolved orders as sympy Function(x) objects,
so that any y-partial-derivative of them is automatically, mechanically,
zero -- not asserted by hand). psi_n itself (the order under test) is
represented as a genuine bivariate Function(x,y). The claim under test:
f_n simplifies to EXACTLY 0 for every n tested, which (via the elementary
Growth-Exclusion Lemma of k02, homogeneous case) proves chi_n := d(psi_n)/dy
solves a HOMOGENEOUS ODE in x, hence chi_n = 0 identically (psi_n really
IS y-independent), justifying moving to n+1 with psi_n now also treated
as a function of x alone.

This is checked mechanically here for n = 1..6, together with a hand
proof (written up in ATTEMPT.md) of the general telescoping identity
that makes f_n = 0 true for ALL n, not just the six tested here.
"""

import sympy as sp

x, y, t, eps, m_sym = sp.symbols('x y t eps m', real=True)

print("=" * 78)
print("STEP 0: moment-integral / Taylor-coefficient cancellation check")
print("=" * 78)
# (1/eps) * int_0^inf e^{-v/eps} v^m dv  should equal  eps^m * m!
# i.e. combined with the Taylor factor 1/m!, the operator coefficient is
# exactly 1 (no leftover 1/m!).
v, eps_s, m_test = sp.symbols('v eps_s m_test', positive=True)
for mm in range(0, 6):
    integral = sp.integrate(sp.exp(-v / eps_s) * v**mm, (v, 0, sp.oo))
    coeff = sp.simplify(integral / eps_s)          # this is (1/eps)*int e^{-v/eps} v^m dv
    coeff_over_factorial = sp.simplify(coeff / sp.factorial(mm))
    print(f"  m={mm}: (1/eps) int e^-v/eps v^m dv = {sp.simplify(coeff)}  "
          f"=> /m! = {coeff_over_factorial}  (expect eps_s**{mm})")
    assert sp.simplify(coeff_over_factorial - eps_s**mm) == 0, "moment/factorial mismatch!"
print("PASS: (1/eps)*int_0^inf e^{-v/eps} v^m/m! dv = eps^m exactly, all m=0..5.")
print("      => Phi = sum_m eps^m * (d/dx - d/dy)^m W(x,y), NO extra 1/m!.")

print()
print("=" * 78)
print("STEP 1: order-1 base case, re-derived directly from the required")
print("reading's own explicit psi1 equation (independent sanity check)")
print("=" * 78)
psi1_xy = sp.Function('psi1')(x, y)
# required reading: psi1_x = (x+y)*psi1 - 1 - int_0^y psi1(x,y') dy'
# Represent the integral term abstractly via its DEFINING property under
# d/dy: d/dy int_0^y psi1(x,y') dy' = psi1(x,y) (fundamental theorem of
# calculus) -- this is the only fact about the integral term needed, so
# we encode the FULL equation's y-derivative directly rather than
# symbolically differentiating an unevaluated Integral object (sympy
# cannot differentiate under an unspecified antiderivative symbolically
# in a way that reveals this cancellation on its own, so we perform the
# two differentiation steps -- of (x+y)*psi1 and of the integral term --
# separately, exactly as done by hand in ATTEMPT.md, and let sympy do
# the mechanical simplification of the REMAINING algebra).
lhs_y_deriv = sp.diff(sp.diff(psi1_xy, x), y)          # d/dy [psi1_x] = psi1_xy
rhs_y_deriv = (sp.diff((x + y) * psi1_xy, y)            # d/dy[(x+y)*psi1]
               - psi1_xy)                                # - d/dy[int_0^y psi1 dy'] = -psi1(x,y)
identity_1 = sp.simplify(lhs_y_deriv - rhs_y_deriv)
print("  d/dy[psi1_x] - d/dy[(x+y)*psi1 - 1 - int_0^y psi1 dy']  (as an")
print("  expression in psi1, psi1_y, using FTC for the integral term):")
print("   =", identity_1)
# Expect: psi1_xy - (x+y)*psi1_y  identically (the "-1" and the two
# "psi1(x,y)" pieces from (x+y)*psi1's implicit y-dependence-of-nothing
# and from the integral's FTC derivative must cancel).
chi1 = sp.Function('chi1')(x, y)   # chi1 := psi1_y, as an independent symbol for display
target = sp.diff(sp.diff(psi1_xy, x), y) - (x + y) * sp.diff(psi1_xy, y)
print("  psi1_xy - (x+y)*psi1_y  (should be the SAME expression as above) =",
      sp.simplify(target - identity_1))
assert sp.simplify(target - identity_1) == 0
print("PASS: (psi1_y)_x = (x+y)*psi1_y identically -- HOMOGENEOUS, matches")
print("      the required reading's stated n=1 result, re-derived fresh.")

print()
print("=" * 78)
print("STEP 2: general order-n Watson bookkeeping, n = 1..6, inductive")
print("=" * 78)

N_MAX = 6


def watson_power(expr, m, xv, yv):
    """Apply (d/dx - d/dy) to expr, m times (iterated operator, matches
    Step 0's confirmed coefficient-1 normalization -- NOT the closed-form
    binomial with any extra factor)."""
    e = expr
    for _ in range(m):
        e = sp.diff(e, xv) - sp.diff(e, yv)
    return e


# psi_funcs[k] holds the sympy object representing psi_k. For orders
# already resolved (proved y-independent) we store a Function(x) object;
# for the order currently under test we store a genuine Function(x,y).
psi_funcs = {0: sp.Integer(0)}     # psi_0 := 0 (Psi's expansion starts at eps^1)
resolved = set()                    # orders proved y-independent so far

all_f_n_results = {}

for n in range(1, N_MAX + 1):
    # order n is the order under test: represent psi_n as bivariate
    psi_n_test = sp.Function(f'psi{n}')(x, y)
    psi_funcs[n] = psi_n_test

    # omega_k := psi_k - d(psi_{k-1})/dx, for k = 1..n
    omega = {}
    for k in range(1, n + 1):
        pk = psi_funcs[k]
        pkm1 = psi_funcs[k - 1]
        omega[k] = pk - sp.diff(pkm1, x)

    # phi_n = sum_{m=0}^{n-1} (d/dx-d/dy)^m [ omega_{n-m} ]
    phi_n = 0
    for mm in range(0, n):
        k = n - mm
        phi_n += watson_power(omega[k], mm, x, y)

    f_n = sp.simplify(psi_n_test - phi_n)
    all_f_n_results[n] = f_n
    print(f"  n={n}: f_n = psi_n - phi_n  simplifies to:  {f_n}")

    if sp.simplify(f_n) == 0:
        print(f"       => f_{n} == 0 identically: chi_{n}'s ODE is HOMOGENEOUS")
        print(f"          => chi_{n} == 0 by the Growth-Exclusion Lemma (k02)")
        print(f"          => psi_{n} IS y-independent. Proceeding with psi_{n}"
              f" now treated as Function(x) only.")
        # Replace psi_n by a function-of-x-only object for subsequent orders,
        # mechanically enforcing the inductive hypothesis (any further
        # d/dy applied to it will be 0 automatically, not asserted by hand).
        psi_n_resolved = sp.Function(f'psi{n}')(x)
        psi_funcs[n] = psi_n_resolved
        resolved.add(n)
    else:
        print(f"       => f_{n} != 0: chi_{n}'s ODE would be INHOMOGENEOUS at this order.")
        print(f"          Induction would break here (not observed for n<={N_MAX}).")
        # Keep psi_n bivariate for any further steps (none attempted past
        # a break, by design of this script).
        break

print()
if len(resolved) == N_MAX:
    print(f"ALL {N_MAX} tested orders PASS: f_n == 0 for n = 1..{N_MAX}.")
    print("Every order's y-derivative equation is homogeneous given the")
    print("previous orders are y-independent -- clean mechanical induction,")
    print("consistent with (and independently confirming) the general")
    print("telescoping-sum proof for ALL n given in ATTEMPT.md Section 3.2.")
else:
    print(f"Induction broke at n={min(n for n in range(1,N_MAX+1) if n not in resolved)}"
          f" -- see printed f_n above.")

print()
print("=" * 78)
print("STEP 3: general-n telescoping identity, symbolic check with an")
print("explicit finite sum (n up to 8), NOT relying on Step 2's per-n")
print("re-derivation -- direct algebraic identity check")
print("=" * 78)
# Claim (proved by hand in ATTEMPT.md Section 3.2):
#   sum_{m=1}^{n-1} omega_{n-m}^{(m)}(x) = psi_{n-1}'(x)
# where omega_k = psi_k - psi_{k-1}', ALL treated as pure functions of x
# (this is the identity used to show phi_n = psi_n exactly, i.e. f_n=0,
# GIVEN psi_1..psi_{n-1} already established y-independent). Verify this
# purely algebraic claim directly and generally-in-form for n=2..9 using
# abstract univariate functions (no y at all -- this isolates the
# COMBINATORIAL identity from the inductive/PDE argument of Step 2, as a
# second, independent check of the same underlying claim).
for n in range(2, 10):
    psis = {0: sp.Integer(0)}
    for k in range(1, n):
        psis[k] = sp.Function(f'p{k}')(x)
    omega_x = {k: psis[k] - sp.diff(psis[k - 1], x) for k in range(1, n)}
    lhs = 0
    for mm in range(1, n):
        k = n - mm
        lhs += sp.diff(omega_x[k], x, mm)
    rhs = sp.diff(psis[n - 1], x)
    diff_check = sp.simplify(lhs - rhs)
    print(f"  n={n}: sum_(m=1)^(n-1) omega_(n-m)^(m)(x) - psi_(n-1)'(x) = {diff_check}")
    assert diff_check == 0
print("PASS: telescoping identity holds exactly for n=2..9 (abstract,")
print("      symbol-independent of any specific psi_k closed form).")
print()
print("ALL STEPS PASS.")
