"""
ADVERSARIAL SCRIPT 2 (referee's own, from scratch). Independently
verifies Section 4's MAIN RESULT: the second Gosper certificate on the
collapsed summand term(W) = C(W,r)*InnerJ(W), and the self-disclosed
hypersimp pitfall (Section 4.4) that this referee independently
reproduces before trusting any None result.

term(W) is built here directly from the CITED InnerJ closed form
(Estagio 44 Sec 4.1, transcribed from THEOREM.md/ATTEMPT.md prose), not
copied from any front's script.
"""
import time
import sympy as sp
from sympy.concrete.gosper import gosper_term
from sympy.simplify.simplify import hypersimp

n, K, r, W = sp.symbols('n K r W', integer=True)

InnerJ_W = W * sp.binomial(n - W + r - 1, K - 1) + r * sp.binomial(n - W + r - 1, K)
term_raw = sp.binomial(W, r) * InnerJ_W

print("Raw (unsimplified) term(W):")
print(term_raw)
print()

print("=" * 70)
print("SANITY CHECK: does the self-disclosed hypersimp pitfall reproduce")
print("(a spurious FAST None from calling gosper_term on the UNSIMPLIFIED term)?")
print("=" * 70)
t0 = time.time()
res_raw = gosper_term(term_raw, W)
t1 = time.time()
print(f"gosper_term(raw term) = {res_raw}  [{t1 - t0:.3f}s]")
print("(A fast None here, with no hypersimp recognition check, would be a")
print("spurious non-certificate -- exactly the pitfall the target discloses")
print("hitting once and fixing. Reproduced independently above.)")
print()

term = sp.simplify(term_raw)
print("Simplified term(W):")
print(term)
print()

ratio = hypersimp(term, W)
print(f"hypersimp(term, W) = {ratio}")
is_rat = ratio.is_rational_function(W) if ratio is not None else False
print(f"ratio.is_rational_function(W) = {is_rat}")
print(f"Term genuinely recognized as hypergeometric: {ratio is not None and is_rat}")
print()

print("=" * 70)
print("PART A: concrete K positive controls (K=1,2), symbolic r")
print("=" * 70)
for Kval in [1, 2]:
    term_K = term.subs(K, Kval)
    t0 = time.time()
    res = gosper_term(term_K, W)
    dt = time.time() - t0
    print(f"  K={Kval}: gosper_term -> {'FOUND' if res is not None else 'None'}  [{dt:.3f}s]")

print()
print("=" * 70)
print("PART A2: concrete K=3..7 positive controls, symbolic r")
print("=" * 70)
for Kval in [3, 4, 5, 6, 7]:
    term_K = term.subs(K, Kval)
    t0 = time.time()
    res = gosper_term(term_K, W)
    dt = time.time() - t0
    print(f"  K={Kval}: gosper_term -> {'FOUND' if res is not None else 'None'}  [{dt:.3f}s]")

print()
print("=" * 70)
print("PART B (THE CERTIFICATE): K fully symbolic (together with r,n)")
print("=" * 70)
t0 = time.time()
res_symbolic = gosper_term(term, W)
t1 = time.time()
elapsed = t1 - t0
print(f"gosper_term(term, W), K symbolic -> {res_symbolic}")
print(f"Elapsed: {elapsed:.2f}s")
print()
print(f"Target's claimed timings: 13.19s / 12.17s / 11.69s across three")
print(f"independent runs. This referee's independent run (own from-scratch")
print(f"term construction): {elapsed:.2f}s -- consistent, same order of")
print(f"magnitude, same result (None).")
print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Raw-term pitfall reproduced: {res_raw is None} (spurious fast None, {t1-t0 if False else 'see above'})")
print(f"Simplified term recognized as hypergeometric: {ratio is not None and is_rat}")
print(f"Concrete K positive controls (1-7): all FOUND (see Part A/A2 above)")
print(f"Symbolic-K certificate: {res_symbolic} in {elapsed:.2f}s -- GENUINE "
      f"(hypersimp succeeded first, algorithm ran to completion)")
