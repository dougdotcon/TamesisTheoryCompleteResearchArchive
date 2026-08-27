"""
INDEPENDENT verification of the target's headline claim (ATTEMPT.md Sec
5.3): that Gosper's algorithm returning None on the Piece B/C and Piece D
r-summands, with K left symbolic, is a rigorous certificate that no
hypergeometric-term (elementary Gamma-ratio) closed form exists for these
specific r-sums.

Everything below uses the summand formulas independently derived and
validated in 04_symbolic_summand_gamma_form.py (which matched target's
own quoted Sec 5.2 Gamma-function formulas EXACTLY, both symbolically and
at 135 concrete (K,r,n) points) -- nothing here is read from any .py file
of any front.

sympy/concrete/gosper.py was read directly (its actual installed source,
not any front's code) to determine precisely what `gosper_term`/
`gosper_sum` returning None can and cannot mean:
  (a) hypersimp(f, n) returns None -> f is not even recognized as a
      hypergeometric term in n (term ratio not rational in n). This is a
      WEAKER, structurally different failure mode than genuine
      non-summability, and would NOT license the "rigorous certificate"
      language if it were what happened here.
  (b) hypersimp succeeds, but no polynomial solution of the (correctly,
      completely) computed degree bound exists for the certifying
      polynomial x(n) -> gosper_term explicitly returns None with the
      literal in-source comment "'f(n)' is *not* Gosper-summable". This
      IS the genuine, complete-decision-procedure branch: Gosper's
      algorithm (Petkovsek-Wilf-Zeilberger, "A=B", cited in sympy's own
      docstring) is a PROVEN COMPLETE decision procedure for whether a
      hypergeometric term has a hypergeometric-term antidifference, given
      that the input is confirmed to be a hypergeometric term in the
      first place.

Step 2 below runs hypersimp() directly to determine which branch is
actually operative for our two summands.
"""
import time
import sympy as sp
from sympy import gamma, hypersimp, hyper, hyperexpand, symbols
from sympy.concrete.gosper import gosper_term, gosper_sum

n, K, r = symbols('n K r', positive=True)

# My own, independently-derived and validated (04_symbolic_summand_gamma_form.py)
# Piece B/C summand and Piece D summand -- "bare" convention (external
# integer multiplicity K, resp. K(K-1), stripped; fractional 1/3, 1/2 kept
# -- confirmed to be exactly what target's Sec 5.2 quotes):
summandBC_sym = 2 * gamma(K) * gamma(n + r + 2) / (n ** (r + 1) * gamma(K - r) * gamma(n - K - 1) * gamma(K + r + 4))
summandD_sym = 2 * (r + 1) * gamma(K - 1) * gamma(n + r + 3) / (n ** (r + 2) * gamma(n - K - 1) * gamma(K - r - 1) * gamma(K + r + 5))

print("=" * 70)
print("STEP 1: term ratio T(r+1)/T(r), confirm genuinely rational in r")
print("=" * 70)
ratioBC = sp.simplify(summandBC_sym.subs(r, r + 1) / summandBC_sym)
ratioD = sp.simplify(summandD_sym.subs(r, r + 1) / summandD_sym)
print("Piece B/C ratio:", ratioBC, "  rational_function(r):", ratioBC.is_rational_function(r))
print("Piece D   ratio:", ratioD, "  rational_function(r):", ratioD.is_rational_function(r))

target_ratioBC = -(r + 1 - K) * (n + r + 2) / (n * (r + K + 4))
target_ratioD = -(r + 2) * (r + 2 - K) * (n + r + 3) / (n * (r + 1) * (r + K + 5))
print("Diff from target's own quoted ratios (Sec 5.3, copied verbatim):",
      sp.simplify(target_ratioBC - ratioBC), sp.simplify(target_ratioD - ratioD))

print("\n" + "=" * 70)
print("STEP 2: hypersimp(summand, r) -- which None-branch would be operative?")
print("=" * 70)
hs_BC = hypersimp(summandBC_sym, r)
hs_D = hypersimp(summandD_sym, r)
print("hypersimp(Piece B/C summand, r) [K,n symbolic] =", hs_BC)
print("hypersimp(Piece D   summand, r) [K,n symbolic] =", hs_D)
recognized = (hs_BC is not None) and (hs_D is not None)
print("Both recognized as genuine hypergeometric terms by sympy's own test:", recognized)
print("=> any later gosper_term/gosper_sum None therefore comes from branch (b)")
print("   (genuine non-summability), NOT branch (a) (not a hypergeometric term).")
assert recognized

print("\n" + "=" * 70)
print("STEP 3: gosper_term / gosper_sum directly, K symbolic")
print("=" * 70)
for label, summand, bound in [("B/C", summandBC_sym, (r, 0, K - 1)), ("D", summandD_sym, (r, 0, K - 2))]:
    t0 = time.time()
    gt = gosper_term(summand, r)
    dt1 = time.time() - t0
    t0 = time.time()
    gs = gosper_sum(summand, bound)
    dt2 = time.time() - t0
    print(f"Piece {label}: gosper_term = {gt}  ({dt1:.3f}s)   gosper_sum(bound={bound}) = {gs}  ({dt2:.3f}s)")
    assert gt is None and gs is None

print("\n" + "=" * 70)
print("STEP 4: TRIANGULATION -- gosper_sum at MANY CONCRETE integer K (n kept")
print("symbolic). If the symbolic-K None were an artifact of sympy mishandling")
print("a symbolic PARAMETER, concrete-K runs would plausibly behave differently.")
print("=" * 70)
all_none_BC = True
all_none_D = True
for Kval in range(3, 16):
    gsBC = gosper_sum(summandBC_sym.subs(K, Kval), (r, 0, Kval - 1))
    gsD = gosper_sum(summandD_sym.subs(K, Kval), (r, 0, Kval - 2))
    all_none_BC &= (gsBC is None)
    all_none_D &= (gsD is None)
    print(f"K={Kval:2d}: gosper_sum(B/C)={gsBC}   gosper_sum(D)={gsD}")
print(f"\nAll concrete K=3..15 give None for B/C: {all_none_BC}   for D: {all_none_D}")
assert all_none_BC and all_none_D

print("\n" + "=" * 70)
print("STEP 5: POSITIVE CONTROLS -- confirm this exact harness DOES detect")
print("summability when genuinely present (rules out a trivially-broken")
print("harness that just always returns None)")
print("=" * 70)
gs_poly = gosper_sum(r + 1, (r, 0, K - 1))
expected_poly = sp.simplify(sp.summation(r + 1, (r, 0, K - 1)))
print(f"Control A: sum_r (r+1), r=0..K-1  -> gosper_sum={gs_poly}  expected={expected_poly}"
      f"  MATCH={sp.simplify(gs_poly-expected_poly)==0}")
assert sp.simplify(gs_poly - expected_poly) == 0

gs_tele = gosper_sum(1 / ((r + 1) * (r + 2)), (r, 0, K - 1))
expected_tele = sp.simplify(K / (K + 1))
print(f"Control B: sum_r 1/((r+1)(r+2)), r=0..K-1 -> gosper_sum={gs_tele}  expected={expected_tele}"
      f"  MATCH={sp.simplify(gs_tele-expected_tele)==0}")
assert sp.simplify(gs_tele - expected_tele) == 0

from sympy import factorial
f_doc = (4 * r + 1) * factorial(r) / factorial(2 * r + 1)  # sympy's own gosper.py docstring example
gs_doc_sym_bound = gosper_sum(f_doc, (r, 0, K - 1))
print(f"Control C: gosper.py's own docstring example, symbolic bound r=0..K-1 -> {gs_doc_sym_bound}")
assert gs_doc_sym_bound is not None
print("(Control C confirms the harness finds closed forms for Gamma/factorial-")
print(" heavy summands with a genuinely FREE symbolic upper bound, structurally")
print(" the same setup as our K-symbolic runs above -- so the None results")
print(" above are not an artifact of 'symbolic bound variable' handling either.)")

print("\n" + "=" * 70)
print("STEP 6: the terminating hypergeometric-function fallback (Sec 5.4)")
print("=" * 70)


def summandBC_num(Kv, nv, rv):
    return 2 * sp.gamma(Kv) * sp.gamma(nv + rv + 2) / (
        nv ** (rv + 1) * sp.gamma(Kv - rv) * sp.gamma(nv - Kv - 1) * sp.gamma(Kv + rv + 4))


print("Checking the exact closed-form VALUE of sum_{r=0}^{K-1} summandBC(r)")
print("against candidate hyper(...) objects, at 4 concrete (K,n) pairs:")
all_hyper_ok = True
for Kv, nv in [(6, 10), (5, 9), (7, 12), (4, 8)]:
    S = sum(sp.Rational(summandBC_num(Kv, nv, rv)) for rv in range(0, Kv))
    T0 = sp.Rational(summandBC_num(Kv, nv, 0))
    # target's LITERALLY printed parameter list (3 upper, 1 lower) -- as written
    cand_as_printed = T0 * hyper([1 - Kv, nv + 2, 1], [Kv + 4], sp.Rational(-1, nv))
    ok = (sp.simplify(sp.N(cand_as_printed, 40) - sp.N(S, 40)) < sp.Float('1e-30'))
    all_hyper_ok &= bool(ok)
    print(f"  K={Kv} n={nv}: direct sum S={S}  candidate(as literally printed)={sp.N(cand_as_printed,20)}"
          f"  S(float)={sp.N(S,20)}  MATCH: {ok}")
print(f"\nValue of target's fallback formula confirmed exact at 4/4 points: {all_hyper_ok}")
assert all_hyper_ok

print("\nChecking target's own TYPE LABEL for this fallback ('3F2'):")
h = hyper([1 - K, n + 2, 1], [K + 4], -1 / n)
print("  sympy's own classification of the parameter list target literally")
print("  prints ((1-K, n+2, 1) upper; (K+4) lower) :")
sp.pprint(h)
print("  LaTeX form sympy itself generates:", sp.latex(h))
print("  ap (upper) count:", len(h.ap), "  bq (lower) count:", len(h.bq))
if len(h.ap) == 3 and len(h.bq) == 1:
    print("  ==> This is a 3F1 by direct parameter count and by sympy's own")
    print("      object classification (pFq with p=3,q=1) -- NOT a 3F2 (which")
    print("      would need 2 lower parameters). The VALUE is independently")
    print("      confirmed correct above; only the 'F2' label is a naming slip.")
    label_issue = True
else:
    label_issue = False

print("\nAttempting hyperexpand on the symbolic-(K,n) fallback (target's own")
print("claim: it does NOT reduce to anything elementary):")
res = hyperexpand(h)
still_has_hyper = res.has(sp.functions.special.hyper.hyper)
print("  hyperexpand result contains an unevaluated hyper(...) term:", still_has_hyper)
assert still_has_hyper, "UNEXPECTED: hyperexpand actually reduced this -- would contradict target's claim!"

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("- Term ratios: rational in r, match target's Sec 5.3 exactly.            [CONFIRMED]")
print("- hypersimp: both summands recognized as genuine hypergeometric terms.   [CONFIRMED]")
print("- gosper_term/gosper_sum: None, K symbolic AND at 13 concrete K values.  [CONFIRMED]")
print("- Positive controls: harness correctly finds closed forms when they     [CONFIRMED]")
print("  exist, including with a symbolic bound variable structurally like K.")
print("- 3F2 fallback VALUE: exact match at 4 concrete (K,n) points.            [CONFIRMED]")
print("- hyperexpand: fails to reduce the symbolic-(K,n) fallback further.      [CONFIRMED]")
if label_issue:
    print("- NAMED ISSUE (LOW): target's Sec 5.4 labels the fallback '3F2', but")
    print("  the literally-printed parameter list (3 upper, 1 lower) is a 3F1 by")
    print("  sympy's own classification and by standard convention -- a naming")
    print("  slip, not a value error (the VALUE is exactly correct as shown above).")
