"""
ATTEMPT.md Sec.3.3: the central symbolic proof of this document.

Verifies -- for SYMBOLIC r,k,b, not looped over concrete values -- that the
conjectured closed form

  d_k^{(r)}(b) = (k+1)(k+2)/2 * [r!/(r-k-1)!] / prod_{i=1}^{k+2}(r+b+i)

satisfies the EXACT defining recursion derived (ATTEMPT.md Sec.3.1) from matching the
coefficient of t^k on both sides of the G_r ODE:

  (k+1+r+b) d_k^{(r)}(b) = -r(k+1) c_k^{(r-1)}(b+1)                     [k>=1 and k=0]
                          + r * [K_{r-1}(1-t,b)]_k
                          + (k+1)*c_{k+1}^{(r)}(b)*[(1+r+b)+k/2]

  [K_{r-1}(1-t,b)]_k = (r-1) c_{k-1}^{(r-2)}(b+2) + d_{k-1}^{(r-1)}(b+1) - (r+b) c_k^{(r-1)}(b+1)   (k>=1)
  [K_{r-1}(1-t,b)]_0 = 1 - (r+b) c_0^{(r-1)}(b+1)

using the ALREADY-PROVEN closed form for c_k^{(r)}(b) (F_r's coefficients, Sec.2.3).

If both cases reduce to 0 for generic r,k,b, this proves (by induction on r, given the
base case G_0=0 and the already-proved c_k^{(r)}(b)) that the conjectured d_k^{(r)}(b)
formula is correct for EVERY r -- not merely fit to the concrete r=0..8 data it was
first read off from (rate_ode.py).

The second half of this script cross-validates G_r(1,b) = sum_k d_k^{(r)}(b) against
B_r(b), computed DIRECTLY (independently of this whole continuum derivation) as the
1/n coefficient of markov_transfer.py's own exact (m,b)-symbolic g_r(m,b) output, for
r=1..5 (the full range where that exact symbolic-b closed form was extracted).
"""
import sys
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import pickle

r, k, b = sp.symbols('r k b', positive=True)


def c_sym(rr, kk, bb):
    """Symbolic-r,k closed form for c_kk^{(rr)}(bb) (F_rr's t^kk coefficient, PROVED
    Sec.2.3), as a Gamma-function-style ratio valid formally for generic rr,kk."""
    num = sp.factorial(rr) / sp.factorial(rr - kk)
    den = sp.rf(rr + bb + 1, kk + 1)  # rising factorial (r+b+1)...(r+b+k+1), k+1 terms
    return num / den


def d_sym(rr, kk, bb):
    """Conjectured closed form for d_kk^{(rr)}(bb) (G_rr's t^kk coefficient)."""
    num = ((kk + 1) * (kk + 2)) / 2 * sp.factorial(rr) / sp.factorial(rr - kk - 1)
    den = sp.rf(rr + bb + 1, kk + 2)  # rising factorial, k+2 terms
    return num / den


print("=== Part 1: symbolic-r,k,b verification of the defining recursion ===\n")

LHS = (k + 1 + r + b) * d_sym(r, k, b)

piece1 = -r * (k + 1) * c_sym(r - 1, k, b + 1)
piece3 = (k + 1) * c_sym(r, k + 1, b) * ((1 + r + b) + k / sp.Integer(2))
piece2_general = r * ((r - 1) * c_sym(r - 2, k - 1, b + 2) + d_sym(r - 1, k - 1, b + 1) - (r + b) * c_sym(r - 1, k, b + 1))

RHS_general = piece1 + piece2_general + piece3
diff_general = sp.simplify(LHS - RHS_general)
print("General k>=1 case, symbolic r,k,b: LHS-RHS simplify =", diff_general)

piece2_k0 = r * (1 - (r + b) * c_sym(r - 1, 0, b + 1))
piece3_k0 = (0 + 1) * c_sym(r, 1, b) * ((1 + r + b) + 0 / sp.Integer(2))
piece1_k0 = -r * (0 + 1) * c_sym(r - 1, 0, b + 1)
LHS_k0 = (0 + 1 + r + b) * d_sym(r, 0, b)
RHS_k0 = piece1_k0 + piece2_k0 + piece3_k0
diff_k0 = sp.simplify(LHS_k0 - RHS_k0)
print("k=0 special case, symbolic r,b:    LHS-RHS simplify =", diff_k0)

print()
print("=== Part 2: cross-validate G_r(1,b) = sum_k d_k^{(r)}(b) against the exact")
print("    discrete-formula B_r(b), r=1..5, full b-dependence ===\n")

with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/pattern_data.pkl', 'rb') as f:
    data = pickle.load(f)
g_full = data['g_full']

import markov_transfer as mt
bb = mt.b
n, mm = mt.n, mt.m


def d_closed_plain(rr, kk, bval):
    num = ((kk + 1) * (kk + 2)) / 2 * sp.factorial(rr) / sp.factorial(rr - kk - 1)
    den = 1
    for i in range(1, kk + 3):
        den *= (rr + bval + i)
    return num / den


def G_closed(rr, bval):
    return sum(d_closed_plain(rr, kk, bval) for kk in range(0, rr))


allmatch = True
for rv in range(1, 6):
    expr = g_full[rv].subs(mm, n)
    A = sp.limit(expr, n, sp.oo)
    Bexact = sp.limit((expr - A) * n, n, sp.oo)
    Gnew = G_closed(rv, bb)
    diff = sp.cancel(sp.together(Gnew - Bexact))
    ok = (diff == 0)
    allmatch = allmatch and ok
    print(f"r={rv}: match={ok}   B_exact={sp.factor(Bexact)}")
print("ALL MATCH:", allmatch)
