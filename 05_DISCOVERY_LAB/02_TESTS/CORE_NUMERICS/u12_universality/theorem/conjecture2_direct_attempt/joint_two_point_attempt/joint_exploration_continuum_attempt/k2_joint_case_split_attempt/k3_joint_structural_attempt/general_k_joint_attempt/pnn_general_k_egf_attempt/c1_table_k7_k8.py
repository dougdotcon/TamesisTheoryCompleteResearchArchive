"""
Task item 4 (bonus): using the general-K algorithm's OWN provably-correct
method (symbolic_pnn_via_composition_gf.py, re-derived/re-implemented in
this front from the mathematical description in THEOREM.md and the
predecessor's ATTEMPT.md -- not by reading any predecessor .py file),
compute c_1(K) (the coefficient of 1/n in P_nn(n,K)) at K=7 and K=8,
extending the predecessor's own table (K=1..6:
1/6, 7/30, 19/70, 187/630, 437/1386, 1979/6006).

Reported as RAW DATA ONLY. Per the mandate: do NOT propose or fit a
closed-form pattern for c_1(K) -- the predecessor explicitly declined to
do this with only 6 points, citing a self-caught bug from an earlier
premature pattern-fit attempt (its own sec 5.2/8.3); this front respects
that discipline and adds two more raw data points only.

Independent verification of the underlying K=7,K=8 closed forms (not just
c_1) against TWO separate routes:
  (a) reduced_model_direct_assembly.py -- a completely different
      (slow, direct Fraction-enumeration-over-the-L-simplex) code path,
      at several concrete n each;
  (b) monte_carlo_k7_k8.py -- direct simulation of Definition 4's actual
      model at large n.
"""
import sys
import time
from fractions import Fraction
import sympy as sp

from symbolic_pnn_via_composition_gf import pnn_closed_form, n
from reduced_model_direct_assembly import assemble_pnn

# NOTE (self-caught, disclosed): an earlier version of this script
# re-declared `n = sp.symbols('n')` here WITHOUT the `positive=True`
# assumption carried by the `n` used throughout symbolic_pnn_via_
# composition_gf.py / gf_moment_machinery.py. Sympy treats symbols with
# different assumption sets as genuinely different symbols even when they
# share a name, so `closed_forms[K].subs(n, nv)` silently did nothing (the
# expression still contained the OTHER `n`), which surfaced immediately as
# a `sp.Rational(...)` TypeError on a still-symbolic expression -- caught
# before any verification result below was taken as final. Fixed by
# importing the correct `n` symbol directly instead of re-declaring it
# (the same class of bug, and the same kind of fix, as an earlier
# debugging step recorded in ATTEMPT.md sec 7.2).

print("=" * 78)
print("Deriving full closed forms for K=7, K=8 via the general-K GF/moment")
print("algorithm (symbolic_pnn_via_composition_gf.py)")
print("=" * 78)
closed_forms = {}
for K in [7, 8]:
    t0 = time.time()
    cf = pnn_closed_form(K)
    dt = time.time() - t0
    closed_forms[K] = cf
    print(f"K={K} ({dt:.2f}s): P_nn(n,{K}) = {cf}")

print()
print("=" * 78)
print("Independent verification route (a): reduced_model_direct_assembly.py")
print("(a completely different, direct-enumeration code path) at several")
print("concrete n")
print("=" * 78)
all_ok = True
verify_points = {7: [9, 11, 13, 16], 8: [10, 12]}
for K, ns in verify_points.items():
    for nv in ns:
        t0 = time.time()
        direct = assemble_pnn(nv, K)
        dt = time.time() - t0
        # EXACT substitution -- no lambdify/float roundtrip, which earlier
        # produced spurious decimal-rounded mismatches (self-caught before
        # any result below was taken as final; see ATTEMPT.md sec 7.4)
        pred_expr = closed_forms[K].subs(n, nv)
        pred = sp.Rational(sp.nsimplify(pred_expr))
        ok = (pred == direct)
        all_ok = all_ok and ok
        print(f"  K={K}, n={nv}: direct={direct}  formula={pred}  match={ok}  ({dt:.1f}s)")

print()
print(f"Route (a) -- ALL MATCH: {all_ok}")
print()
print("See monte_carlo_k7_k8.py for independent route (b) -- large-n Monte")
print("Carlo triangulation (own log: monte_carlo_k7_k8.log).")

print()
print("=" * 78)
print("Extracting c_0(K) and c_1(K) (coefficients of 1/n^0 and 1/n^1) from")
print("the verified closed forms, K=7,8, extending the predecessor's table")
print("=" * 78)


def extract_c0_c1(cf, K):
    num, den = sp.fraction(sp.together(cf))
    num_poly = sp.Poly(sp.expand(num), n)
    den_val = sp.expand(den)  # D * n^K
    D = den_val / n ** K
    D = sp.nsimplify(D)
    coeffs = num_poly.all_coeffs()  # highest degree first, degree K down to 0
    # coeffs[0] is coefficient of n^K, coeffs[1] of n^{K-1}, etc.
    c0 = sp.nsimplify(coeffs[0] / D)
    c1 = sp.nsimplify(coeffs[1] / D)
    return c0, c1


predecessor_table = {
    1: Fraction(1, 6), 2: Fraction(7, 30), 3: Fraction(19, 70),
    4: Fraction(187, 630), 5: Fraction(437, 1386), 6: Fraction(1979, 6006),
}

print()
print(f"{'K':>3} {'c_0=1/(K+1)':>14} {'c_1 (exact)':>16} {'c_1 (decimal)':>16}  source")
print("-" * 78)
for K in range(1, 7):
    c1 = predecessor_table[K]
    print(f"{K:>3} {'1/' + str(K+1):>14} {str(c1):>16} {float(c1):>16.5f}  predecessor (Estagio 27/31/35, cited)")

c1_new = {}
for K in [7, 8]:
    c0, c1 = extract_c0_c1(closed_forms[K], K)
    c1_frac = Fraction(int(sp.fraction(sp.nsimplify(c1))[0]), int(sp.fraction(sp.nsimplify(c1))[1]))
    c1_new[K] = c1_frac
    expected_c0 = Fraction(1, K + 1)
    c0_ok = (Fraction(int(sp.fraction(c0)[0]), int(sp.fraction(c0)[1])) == expected_c0)
    print(f"{K:>3} {str(c0):>14} {str(c1_frac):>16} {float(c1_frac):>16.5f}  THIS FRONT (new)"
          f"   [c_0 == 1/(K+1) sanity check: {c0_ok}]")

print()
print("=" * 78)
print("RAW DATA TABLE, c_1(K), K=1..8 -- extended, no pattern proposed or fit")
print("(successive ratios shown only as already-reported context, per the")
print(" predecessor's own table, not as a new fitting exercise):")
print("=" * 78)
all_c1 = dict(predecessor_table)
all_c1.update(c1_new)
prev = None
for K in range(1, 9):
    c1 = all_c1[K]
    ratio_str = ""
    if prev is not None:
        ratio_str = f"   ratio to K-1: {float(c1/prev):.4f}"
    print(f"  K={K}: c_1 = {c1} = {float(c1):.5f}{ratio_str}")
    prev = c1

print()
print("No closed form or fit is proposed for c_1(K) as a function of K.")
print("Reported as raw data only, per the mandate.")
