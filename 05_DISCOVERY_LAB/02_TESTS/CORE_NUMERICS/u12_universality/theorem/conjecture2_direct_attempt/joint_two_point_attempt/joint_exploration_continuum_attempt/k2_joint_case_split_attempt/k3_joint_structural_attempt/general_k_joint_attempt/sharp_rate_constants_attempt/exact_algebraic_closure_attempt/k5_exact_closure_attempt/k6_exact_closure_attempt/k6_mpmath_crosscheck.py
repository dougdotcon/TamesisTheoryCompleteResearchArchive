"""
K6-EXACT-CLOSURE-ATTEMPT. Independent high-precision cross-check of
x6*/M6, using ONLY mpmath -- zero reliance on any sympy symbolic
machinery (a genuinely different computational stack from
k6_exact_closure.py, matching the K=5 predecessor's own convention).

g6(x) is transcribed here TWICE, independently: once in the fully
expanded polynomial form (as printed by d6_derivation.py's Step 2 in
k6_exact_closure.py), and once in the factored form found by sp.factor
there -- and the two are cross-checked against each other numerically
at several points BEFORE either is trusted for the max-finding below
(the same discipline the K=5 predecessor's own crosscheck used).
"""
import mpmath as mp

mp.mp.dps = 50


def g6_expanded(x):
    return (-15 * x ** 12 + 24 * x ** 11 + 45 * x ** 10 - 90 * x ** 9
            - 30 * x ** 8 + 120 * x ** 7 - 30 * x ** 6 - 60 * x ** 5
            + 45 * x ** 4 - 15 * x ** 2 + 6 * x)


def g6_factored(x):
    return -3 * x * (x - 1) ** 5 * (x + 1) ** 4 * (5 * x ** 2 - 3 * x + 2)


def g6p_factored(x):
    # derivative of g6, transcribed independently from the factored
    # critical-point form found in k6_exact_closure.py:
    #   g6'(x) = -6(x-1)^4(x+1)^3(30x^4-14x^3+x^2+4x-1)
    return -6 * (x - 1) ** 4 * (x + 1) ** 3 * (30 * x ** 4 - 14 * x ** 3 + x ** 2 + 4 * x - 1)


print("Cross-checking g6_expanded vs g6_factored at several points:")
max_diff = mp.mpf(0)
for xv in [mp.mpf('0.0'), mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.3'),
           mp.mpf('0.5'), mp.mpf('0.7'), mp.mpf('0.9'), mp.mpf('1.0'),
           mp.mpf('-0.5'), mp.mpf('2.0')]:
    a = g6_expanded(xv)
    b = g6_factored(xv)
    d = abs(a - b)
    max_diff = max(max_diff, d)
    print(f"  x={float(xv):+.2f}  expanded={mp.nstr(a,20)}  factored={mp.nstr(b,20)}  diff={mp.nstr(d,5)}")
assert max_diff < mp.mpf('1e-40'), max_diff
print(f"Max diff = {mp.nstr(max_diff, 10)} -- forms agree. PASSED.\n")

# Also verify g6p_factored is genuinely the derivative of g6_factored,
# by comparing to a numerical derivative at a few points (independent
# sanity, not a proof, but catches a transcription error).
print("Cross-checking g6p_factored against numerical derivative of g6_factored:")
max_diff2 = mp.mpf(0)
for xv in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.6'), mp.mpf('0.9')]:
    analytic = g6p_factored(xv)
    numeric = mp.diff(g6_factored, xv)
    d = abs(analytic - numeric)
    max_diff2 = max(max_diff2, d)
    print(f"  x={float(xv):.2f}  analytic={mp.nstr(analytic,15)}  numeric={mp.nstr(numeric,15)}  diff={mp.nstr(d,5)}")
assert max_diff2 < mp.mpf('1e-35')
print(f"Max diff = {mp.nstr(max_diff2, 10)} -- derivative confirmed. PASSED.\n")

print("=" * 70)
print("Dense scan on [0,1] to bracket the maximum, then Newton polish")
print("on g6'(x)=0 (mpmath.findroot), at 50 decimal digits:")
print("=" * 70)
N_SCAN = 200000
best_x = None
best_v = mp.mpf('-1e100')
for i in range(N_SCAN + 1):
    xv = mp.mpf(i) / N_SCAN
    v = g6_factored(xv)
    if v > best_v:
        best_v = v
        best_x = xv
print(f"dense-scan argmax: x~={float(best_x):.6f}  g6~={float(best_v):.10f}")

x6star = mp.findroot(g6p_factored, best_x)
M6 = g6_factored(x6star)
print(f"\nx6* (mpmath, {mp.mp.dps} dps) = {mp.nstr(x6star, 45)}")
print(f"M6  (mpmath, {mp.mp.dps} dps) = {mp.nstr(M6, 45)}")

# Cross-check against the sympy-derived value (transcribed from
# k6_exact_closure.log, not recomputed via sympy here).
x6star_sympy = mp.mpf('0.26036172400671492484172362842265674')
M6_sympy = mp.mpf('0.67967830129138512967160338683005533')
dx = abs(x6star - x6star_sympy)
dM = abs(M6 - M6_sympy)
print(f"\n|x6*_mpmath - x6*_sympy| = {mp.nstr(dx, 5)}")
print(f"|M6_mpmath  - M6_sympy | = {mp.nstr(dM, 5)}")
assert dx < mp.mpf('1e-30')
assert dM < mp.mpf('1e-30')
print("Matches the sympy-derived values to 30+ digits. PASSED.")

print()
print("Also confirm this is genuinely a MAXIMUM on [0,1] (not just a")
print("critical point), by evaluating g6 at a fine grid and confirming")
print("nothing exceeds M6:")
worst_excess = mp.mpf('-1e100')
for i in range(N_SCAN + 1):
    xv = mp.mpf(i) / N_SCAN
    v = g6_factored(xv)
    worst_excess = max(worst_excess, v - M6)
print(f"max(g6(x) - M6) over the scan = {mp.nstr(worst_excess, 10)} "
      f"(should be ~0 at x=x6*, negative elsewhere)")
assert worst_excess < mp.mpf('1e-9')
print("PASSED -- M6 is confirmed (to scan resolution + Newton polish) the")
print("global maximum of g6 on [0,1].")
