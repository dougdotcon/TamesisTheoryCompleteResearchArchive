"""
ADVERSARIAL, INDEPENDENT symbolic re-derivation and recursion-satisfaction check for
k3_attempt_2/ATTEMPT.md SS2-SS3, written from scratch for this referee review.

Two separate, independent things are done here (deliberately NOT importing
markov_transfer.py's g_closed_via_telescoping / h_closed_from_g functions -- this
script re-implements the summation-factor solution to the first-order linear
recursion from scratch, via a different derivation path: the "integrating factor"
P(m) = prod_{t=j+1}^m w(t) method for a first-order linear recurrence, rather than
directly asserting the hockey-stick form):

  PART A. Re-derive, by the standard integrating-factor method for a first-order
  linear recursion g(m) = c(m) + w(m) g(m-1), the closed form
      g(m) = [ sum_{i=j}^m c(i) C(i,j) ] / C(m,j),   j = r+b+1
  starting from w(m) = (m-1-r-b)/m and showing algebraically (sympy, symbolic m, j)
  that the integrating factor P(m) := prod_{t=j+1}^m w(t) equals EXACTLY 1/C(m,j) --
  this is the one identity the whole telescoping method rests on, and it is verified
  here symbolically from the definition of w(m), not assumed.

  PART B. Build the K=3 ladder (g0,h0,g1,h1,g2,h2,g3) using this independently
  re-derived formula, then -- the core ask -- SUBSTITUTE each resulting closed form
  back into the ORIGINAL defining recursion equations (typed fresh from
  ATTEMPT.md SS2's Proposition, not copied from markov_transfer.py's internal
  variable names) and check sympy.simplify(LHS - RHS) == 0 for every level, i.e.
  that the claimed solution actually satisfies the recursion it purports to solve --
  not merely that some summation procedure produced it.

  PART C. Cross-check the resulting psi_n^{(3)}, psi_n^{(3),R} against the exact
  values ATTEMPT.md claims, symbolically (difference == 0), and against
  markov_transfer.py's own output (independent agreement between two differently
  -coded solvers is itself informative).
"""
import sympy as sp

n = sp.Symbol('n', positive=True)
m = sp.Symbol('m', positive=True)
i = sp.Symbol('i', positive=True)
t = sp.Symbol('t', positive=True)
a = sp.Symbol('a', nonnegative=True)
b = sp.Symbol('b', nonnegative=True, integer=True)

print("=" * 70)
print("PART A: verify the integrating factor identity P(m) = 1/C(m,j)")
print("=" * 70)
r_val = sp.Symbol('r_val', nonnegative=True, integer=True)
j = r_val + b + 1
w = (t - 1 - r_val - b) / t  # = (t-j)/t
# P(m) = prod_{t=j+1}^m w(t). Use sympy's Product and simplify (finite product of
# rational functions of t; combinatorial identity: prod_{t=j+1}^m (t-j)/t
#   = [(m-j)!/0!] / [m!/j!] = j!(m-j)!/m! = 1/C(m,j)
P_m = sp.Product((t - j) / t, (t, j + 1, m)).doit()
target_P = 1 / sp.binomial(m, j)
diff_P = sp.simplify(P_m - target_P)
print("P(m) computed via sympy.Product, doit():", P_m)
print("claimed 1/C(m,j):", target_P)
print("difference simplifies to:", diff_P, " -> IDENTITY HOLDS:", diff_P == 0)
print()

print("=" * 70)
print("PART B: build K=3 ladder independently, then verify EACH closed form")
print("        satisfies the ORIGINAL recursion (typed fresh, not imported)")
print("=" * 70)


def solve_g(r, c_of_k_func, b_expr):
    """Independent implementation of the telescoping solution, using the
    integrating-factor form confirmed in Part A: g(m) = sum_{i=j}^m c(i) C(i,j) / C(m,j).
    c_of_k_func: function of symbol i -> c_r(i) expression.
    Returns g_of_m(m_expr) callable."""
    jj = r + b_expr + 1
    summand = sp.simplify(c_of_k_func(i) * sp.binomial(i, jj))
    total = sp.simplify(sp.summation(summand, (i, jj, m)))
    g_of_m_expr = sp.simplify(total / sp.binomial(m, jj))

    def g_func(m_expr, b_expr2=b_expr):
        e = g_of_m_expr
        if b_expr2 is not b_expr:
            e = e.subs(b_expr, b_expr2)
        e = e.subs(m, m_expr)
        return sp.simplify(e)
    return g_func, g_of_m_expr


def h_from_g(r, g_r_func, h_prev_func, a_expr, b_expr):
    """h_r(a,b) = 1/n + (r/n) h_{r-1}(a,b+1) + ((n-1-a-b-r)/n) g_r(a,b+1)."""
    term_h = sp.Integer(0)
    if r >= 1:
        term_h = sp.Rational(r, 1) / n * h_prev_func(a_expr, b_expr + 1)
    term_g = (n - 1 - a_expr - b_expr - r) / n * g_r_func(n - a_expr, b_expr + 1)
    return sp.simplify(sp.Rational(1, 1) / n + term_h + term_g)


# --- r=0 ---
def g0(m_expr, b_expr=b):
    return sp.Rational(1, 1) / (b_expr + 1)


def h0(a_expr, b_expr=b):
    return h_from_g(0, g0, None, a_expr, b_expr)


# --- r=1 ---
def c1(k_sym):
    # c_r(k) = 1/k + (r/k) h_{r-1}(n-k+1, b)
    return sp.simplify(sp.Rational(1, 1) / k_sym + sp.Rational(1, 1) / k_sym * h0(n - k_sym + 1, b))


g1_func, g1_expr = solve_g(1, c1, b)


def h1(a_expr, b_expr=b):
    return h_from_g(1, g1_func, h0, a_expr, b_expr)


# --- r=2 ---
def c2(k_sym):
    return sp.simplify(sp.Rational(1, 1) / k_sym + sp.Rational(2, 1) / k_sym * h1(n - k_sym + 1, b))


g2_func, g2_expr = solve_g(2, c2, b)


def h2(a_expr, b_expr=b):
    return h_from_g(2, g2_func, h1, a_expr, b_expr)


# --- r=3 ---
def c3(k_sym):
    return sp.simplify(sp.Rational(1, 1) / k_sym + sp.Rational(3, 1) / k_sym * h2(n - k_sym + 1, b))


g3_func, g3_expr = solve_g(3, c3, b)

print("g1(m,b) =", g1_expr)
print("g2(m,b) =", g2_expr)
print("g3(m,b) =", g3_expr)
print()

# ---- Now verify EACH level satisfies the ORIGINAL recursion identically ----
print("--- Verifying each closed form satisfies its DEFINING recursion (fresh check) ---")

k_sym = sp.Symbol('k_sym', positive=True)


def check_g_recursion(label, r, g_func, h_prev_func, b_expr=b):
    """g_r(m,b) =?= 1/m + (r/m) h_{r-1}(n-m+1,b) + ((m-1-r-b)/m) g_r(m-1,b)."""
    lhs = g_func(k_sym)
    rhs_h = sp.Integer(0)
    if r >= 1:
        rhs_h = sp.Rational(r, 1) / k_sym * h_prev_func(n - k_sym + 1, b_expr)
    rhs = sp.Rational(1, 1) / k_sym + rhs_h + (k_sym - 1 - r - b_expr) / k_sym * g_func(k_sym - 1)
    diff = sp.simplify(lhs - rhs)
    print(f"{label}: LHS-RHS simplifies to {diff}  -> RECURSION HOLDS: {diff == 0}")
    return diff == 0


def check_h_recursion(label, r, h_func, g_func_at_bplus1_source, h_prev_func):
    """h_r(a,b) =?= 1/n + (r/n) h_{r-1}(a,b+1) + ((n-1-a-b-r)/n) g_r(a,b+1)."""
    a_sym = sp.Symbol('a_sym', nonnegative=True)
    lhs = h_func(a_sym, b)
    rhs_h = sp.Integer(0)
    if r >= 1:
        rhs_h = sp.Rational(r, 1) / n * h_prev_func(a_sym, b + 1)
    rhs_g = (n - 1 - a_sym - b - r) / n * g_func_at_bplus1_source(n - a_sym, b + 1)
    rhs = sp.Rational(1, 1) / n + rhs_h + rhs_g
    diff = sp.simplify(lhs - rhs)
    print(f"{label}: LHS-RHS simplifies to {diff}  -> RECURSION HOLDS: {diff == 0}")
    return diff == 0


all_ok = True
all_ok &= check_g_recursion("g0 recursion (r=0, trivial: no h term)", 0, g0, None)
all_ok &= check_h_recursion("h0 recursion (r=0)", 0, h0, g0, None)
all_ok &= check_g_recursion("g1 recursion (r=1)", 1, g1_func, h0)
all_ok &= check_h_recursion("h1 recursion (r=1)", 1, h1, g1_func, h0)
all_ok &= check_g_recursion("g2 recursion (r=2)", 2, g2_func, h1)
all_ok &= check_h_recursion("h2 recursion (r=2)", 2, h2, g2_func, h1)
all_ok &= check_g_recursion("g3 recursion (r=3)", 3, g3_func, h2)
print()
print("ALL RECURSION CHECKS PASS:" if all_ok else "SOME RECURSION CHECKS FAILED:", all_ok)
print()

print("=" * 70)
print("PART C: cross-check final psi_n^(3), psi_n^(3),R against ATTEMPT.md's claims")
print("=" * 70)
psi3 = sp.simplify(g3_func(n).subs(b, 0))
psi3R = sp.simplify(h2(0, 0))
target_psi3 = sp.Rational(16, 35) + sp.Rational(12, 35) / n + sp.Rational(5, 28) / n**2 + sp.Rational(3, 70) / n**3
target_psi3R = sp.Rational(11, 30) + sp.Rational(13, 20) / n + sp.Rational(23, 60) / n**2 + sp.Rational(1, 10) / n**3

print("psi_n^(3)  (my independent derivation) =", sp.nsimplify(sp.together(psi3)))
print("target from ATTEMPT.md                =", sp.together(target_psi3))
print("difference:", sp.simplify(psi3 - target_psi3), "  MATCH:", sp.simplify(psi3 - target_psi3) == 0)
print()
print("psi_n^(3),R (my independent derivation) =", sp.nsimplify(sp.together(psi3R)))
print("target from ATTEMPT.md                 =", sp.together(target_psi3R))
print("difference:", sp.simplify(psi3R - target_psi3R), "  MATCH:", sp.simplify(psi3R - target_psi3R) == 0)
print()

# Lemma A recombination, independent
K = 3
phi3 = sp.simplify(sp.together(sp.Rational(K, 1) / n * psi3R + (1 - sp.Rational(K, 1) / n) * psi3))
target_phi3 = sp.Rational(16, 35) + sp.Rational(1, 14) / n + sp.Rational(11, 10) / n**2 + sp.Rational(23, 35) / n**3 + sp.Rational(6, 35) / n**4
print("phi_n^(3) via Lemma A (my independent recombination) =", sp.together(phi3))
print("target from ATTEMPT.md                                =", sp.together(target_phi3))
print("difference:", sp.simplify(phi3 - target_phi3), "  MATCH:", sp.simplify(phi3 - target_phi3) == 0)
print()

print("=" * 70)
print("PART D: cross-check against markov_transfer.py's own (differently coded) output")
print("=" * 70)
import sys
sys.path.insert(0, "..")
from markov_transfer import psi_closed_form, psi_rerouted_closed_form, phi_closed_form
mt_psi3 = psi_closed_form(3)
mt_psi3R = psi_rerouted_closed_form(3)
mt_phi3 = phi_closed_form(3)
print("markov_transfer.psi_closed_form(3)          =", mt_psi3)
print("my independent psi3, difference:", sp.simplify(psi3 - mt_psi3), " MATCH:", sp.simplify(psi3 - mt_psi3) == 0)
print("markov_transfer.psi_rerouted_closed_form(3) =", mt_psi3R)
print("my independent psi3R, difference:", sp.simplify(psi3R - mt_psi3R), " MATCH:", sp.simplify(psi3R - mt_psi3R) == 0)
print("markov_transfer.phi_closed_form(3)          =", mt_phi3)
print("my independent phi3, difference:", sp.simplify(phi3 - mt_phi3), " MATCH:", sp.simplify(phi3 - mt_phi3) == 0)
