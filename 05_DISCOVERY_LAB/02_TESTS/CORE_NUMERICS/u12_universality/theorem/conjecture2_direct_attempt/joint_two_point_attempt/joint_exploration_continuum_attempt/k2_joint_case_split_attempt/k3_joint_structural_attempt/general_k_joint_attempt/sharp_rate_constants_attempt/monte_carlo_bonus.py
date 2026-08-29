"""
monte_carlo_bonus.py -- optional large-(n,x) random stress-test of the
FINAL proved bounds, in the tradition of this archive's other fronts'
"Monte Carlo bonus" triangulation checks (see e.g. K2/K3/K4
full_cdf_attempt ATTEMPT.md files, Sec 6.4/§6/§7.4).

NOT required for the proofs themselves (those are exact, symbolic,
and exhaustive over the relevant finite windows -- see
k2_sharp_rate.py Step 6/7, k3_full_window_closure.py,
k4_full_window_closure.py). This script is an EXTRA sanity net: random
(n,x) pairs, evaluated in exact rational arithmetic (sp.Rational), to
catch any blunder the exhaustive/symbolic checks might have missed by
construction (e.g. an off-by-one in a domain restriction).

Reserved seed block for this front (D-SHARP-RATE-CONSTANTS-ATTEMPT,
wave 25 front a, DISC-DEC-118): 20260929000-20260929999.
Seeds used here (all within the reserved block, grep-confirmed unused
before first use in this front, see ATTEMPT.md Seeds-used section):
  20260929001 -- K=2 stress test
  20260929002 -- K=3 stress test
  20260929003 -- K=4 stress test
"""
import random
import sympy as sp
from lib_cdf import n, k, x, CDF, F_continuum

log = []


def say(s=""):
    print(s)
    log.append(s)


say("=" * 78)
say("monte_carlo_bonus.py -- random (n,x) stress test of final bounds")
say("=" * 78)

# Final constants under test, as plain floats (sufficient for a STRESS
# TEST -- the actual proofs are exact/symbolic and live in the other
# scripts; this script's role is only an additional numeric sanity net).
M2 = 0.71072657606222206206
C2 = M2  # K=2: proved bound is EXACTLY M2_exact/n for n>=4 (full closure)
# C3, C4 are the final PROVED constants from k3_full_window_closure.log /
# k4_full_window_closure.log (hardcoded here, not re-parsed, to keep this
# stress-test script simple and independent of log text formatting; the
# values are copied verbatim from those two logs' own printed headers).
C3 = 0.7183335821861240008038727732851894951722
C4 = 0.7345569184500456912259247911642612891263

say(f"\nFinal constants under test:")
say(f"  K=2: C2={C2}  (n>=4, EXACT full closure)")
say(f"  K=3: C3={C3}  (n>=6, near-sharp closure, N0=1000)")
say(f"  K=4: C4={C4}  (n>=6, near-sharp closure, N0=1000)")

DOMAIN_N0 = {2: 4, 3: 6, 4: 6}
CONST = {2: C2, 3: C3, 4: C4}
SEEDS = {2: 20260929001, 3: 20260929002, 4: 20260929003}


# IMPORTANT (self-caught precision issue, avoided): a first version of
# this script used sp.lambdify + Python floats to evaluate Delta_n(x)
# for randomly sampled n up to 10^6. For K=4 the numerator/denominator
# polynomials are degree ~6 in n; evaluating them naively in float64
# for n=10^6 means computing a difference between terms of order
# n^6~10^36 to recover a result of order 1/n~10^-6 -- a catastrophic-
# cancellation loss of ~42 decimal digits, far beyond float64's ~15-16
# digit precision. This would silently produce numerical GARBAGE, not
# a genuine stress test. Caught before trusting any output (by
# reasoning about the polynomial degrees vs. the sampled n range, not
# by an observed failure) and fixed by using EXACT sympy rational
# substitution throughout (Python's arbitrary-precision integers make
# this exact regardless of how large n is), with only the FINAL
# comparison against the bound done via high-precision (50-digit)
# decimal evaluation -- never floats for the Delta_n(x) computation
# itself.
DELTA_EXPR = {}
for K in (2, 3, 4):
    cdf_ = CDF[K]
    F_ = F_continuum(K)
    DELTA_EXPR[K] = cdf_.subs(k, n * x) - F_

NSAMPLES = 3000
NMAX = {2: 10**6, 3: 10**6, 4: 10**6}

for K in (2, 3, 4):
    rng = random.Random(SEEDS[K])
    say(f"\n[K={K}] seed={SEEDS[K]}  n_samples={NSAMPLES}  "
        f"n range=[{DOMAIN_N0[K]},{NMAX[K]}]  (exact rational "
        f"arithmetic, no floats until final comparison)")
    worst_ratio = None
    worst_case = None
    n_violations = 0
    expr = DELTA_EXPR[K]
    for _ in range(NSAMPLES):
        nn = rng.randint(DOMAIN_N0[K], NMAX[K])
        xnum = rng.randint(0, 10**6)
        xx = sp.Rational(xnum, 10**6)  # exact rational in [0,1]
        val_exact = expr.subs({n: sp.Integer(nn), x: xx})
        val = abs(sp.N(val_exact, 50))
        bound = sp.Float(CONST[K], 50) / nn
        ratio = float(val / bound) if bound > 0 else 0.0
        if worst_ratio is None or ratio > worst_ratio:
            worst_ratio = ratio
            worst_case = (nn, xx, val, bound)
        if ratio > 1.0 + 1e-9:
            n_violations += 1
    say(f"  worst |Delta_n(x)|/bound ratio = {worst_ratio:.10f} at "
        f"(n,x)=({worst_case[0]},{sp.nsimplify(worst_case[1])})  "
        f"(must be <=1)")
    say(f"  violations: {n_violations} / {NSAMPLES}")
    assert n_violations == 0, f"K={K}: Monte Carlo found a VIOLATION!"

say("\nPASS: no violations found in any of the three K=2,3,4 stress "
    "tests.")

with open("monte_carlo_bonus.log", "w") as f:
    f.write("\n".join(log) + "\n")
say("\n[Saved] monte_carlo_bonus.log")
