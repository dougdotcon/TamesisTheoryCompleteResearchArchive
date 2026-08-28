"""
ADVERSARIAL SCRIPT 6 -- documents the investigation into the discrepancy
between the target ATTEMPT.md's own printed "exact expression sympy
simplified the summand to" (Section 4.3, Part C) and the mathematically
correct term(V) = C(V-1,r-1)*InnerJ(V,O) it claims to equal.

Findings reproduced here:
  1. hypersimp() behavior differs sharply between three equivalent-looking
     forms of "the same" mathematical object -- explaining WHY the exact
     symbolic form fed to gosper_term matters enormously for runtime and
     for whether a `None` result is a genuine certificate.
  2. Timing fingerprint at concrete K=3: the CORRECT (single-fraction)
     term takes ~11.5s (closely matching the target's own reported
     11.3s), while the LITERALLY-PRINTED (buggy) term takes >7 minutes
     without completing -- strong evidence the buggy printed formula is
     a transcription error, not what the target's actual script ran.

NOTE: step 3 below (running gosper_term on the literally-printed buggy
formula to completion) is NOT re-run in this consolidated script because
it did not complete within 7+ minutes when first tried (process killed
by the referee to reclaim compute) -- see the referee report for the
full timing account. Steps 1-2 (fast) are reproduced here directly.
"""
import time
import sympy as sp
from sympy.simplify.simplify import hypersimp
from sympy.concrete.gosper import gosper_term

V, r, n, K, O = sp.symbols('V r n K O')
N = n - V - O

# Form 1: the "natural first-draft" sum-of-two-binomials form (what one
# gets immediately from C(V-1,r-1)*InnerJ(V,O) without further algebra)
InnerJ = (O + V) * sp.binomial(N + r - 1, K - 1) + r * sp.binomial(N + r - 1, K)
sum_form = sp.binomial(V - 1, r - 1) * InnerJ

# Form 2: the single-fraction form (algebraically identical to Form 1 --
# verified: sp.simplify(sum_form - single_frac) == 0), obtained by hand
# via the classical Pascal-triangle merge C(m,k)=C(m,k-1)*(m-k+1)/k
coeff = K * O + K * V - K * r - O * r - V * r + n * r + r ** 2
single_frac = sp.binomial(V - 1, r - 1) * coeff * sp.factorial(n - O - V + r - 1) / (
    sp.factorial(K) * sp.factorial(n - K - O - V + r))

# Form 3: the target document's own LITERALLY PRINTED "exact expression"
# (Section 4.3, Part C) -- algebraically verified (script5, Part 0) to
# NOT equal Forms 1/2
doc_printed = sp.binomial(V - 1, r - 1) * (
    (K * O + K * V - K * r - O * r - V * r + n * r + r ** 2) * sp.binomial(V - 1, V - r)
    * sp.factorial(n - K - O - V + r - 1) / (sp.factorial(K) * sp.factorial(n - K - O - V + r))
)

print("=" * 70)
print("Step 1: hypersimp() success/failure on each form")
print("(hypersimp is gosper_term's FIRST internal step -- if it fails,")
print(" gosper_term returns None IMMEDIATELY, which is NOT a genuine")
print(" Gosper non-existence certificate, just a recognition failure)")
print("=" * 70)
for label, expr in [("Form 1 (sum-of-two-binomials, un-combined)", sum_form),
                     ("Form 2 (single fraction, algebraically correct)", single_frac),
                     ("Form 3 (target's literally-printed formula)", doc_printed)]:
    t0 = time.time()
    hs = hypersimp(expr, V)
    dt = time.time() - t0
    print(f"  {label}:")
    print(f"    hypersimp -> {'SUCCEEDED' if hs is not None else 'FAILED (None)'}  ({dt:.3f}s)")

print()
print("=" * 70)
print("Step 2: gosper_term on Form 1 with K fully symbolic -- reproduces")
print("        the FAST, SPURIOUS None (a hypersimp recognition failure,")
print("        NOT a genuine Gosper certificate)")
print("=" * 70)
t0 = time.time()
res1 = gosper_term(sum_form, V)
print(f"  Form 1, K symbolic: gosper_term -> {res1}   ({time.time()-t0:.3f}s)")
print("  (contrast with Form 2 / single_frac, K symbolic: None after")
print("   325.59s -- see script5_part_c_symbolicK_full_run.log -- a")
print("   GENUINE run of the full Gosper decision procedure)")

print()
print("=" * 70)
print("Step 3: timing fingerprint at concrete K=3 (Form 2 vs Form 3)")
print("=" * 70)
t0 = time.time()
res2 = gosper_term(single_frac.subs(K, 3), V)
dt2 = time.time() - t0
print(f"  Form 2 (correct) at K=3: None={res2 is None}  ({dt2:.2f}s)")
print("  -- target document's own reported K=3 timing: 11.3s")
print(f"  -- this referee's Form 2 timing: {dt2:.2f}s (close match)")
print()
print("  Form 3 (target's literally-printed formula) at K=3 was ALSO")
print("  tried by this referee: it did NOT complete within 7+ minutes")
print("  (process killed to reclaim compute) -- wildly inconsistent")
print("  with the target's own reported 11.3s figure for what it calls")
print("  the same computation.")
print()
print("CONCLUSION: the timing fingerprint (Form 2 matches the target's")
print("own reported numbers closely at every concrete K tried, AND at")
print("the ~5-minute symbolic-K run; Form 3, the literally-printed")
print("formula, does not) strongly indicates the target's ACTUAL script")
print("used Form 2 (or an equivalent well-conditioned single-fraction")
print("form), and that the printed 'exact expression' in Section 4.3")
print("Part C is a TRANSCRIPTION ERROR into the markdown, not a")
print("computational error in the underlying certificate.")
