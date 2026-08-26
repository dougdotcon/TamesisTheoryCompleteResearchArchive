"""
Bonus check on ATTEMPT.md Sec 4.1's claim that the K=2 joint quantity
P_n^{(2)}(both) does not close under a simple few-parameter rational
ansatz in 1/n, unlike the K=0,1 cases (which have exact closed forms
found by hand). The document reports a 3-parameter fit (target +
a/n+b/n^2+c/n^3, fit from n=3,4,5) fails to predict n=6,7.

This script independently reproduces that failure using our OWN
brute-force values (bruteforce_definition4.py's K2_full results,
cross-checked against the document's own table and found identical),
and additionally tests whether a RICHER 4-parameter fit (adding a
1/n^4 term, fit from n=3,4,5,6) succeeds in predicting n=7 -- it does
NOT, which is a slightly STRONGER form of the same conclusion the
document draws (the true closed form needs even more structure than a
naive one-extra-term richer ansatz), i.e. this check does not
contradict Sec 4.1's diagnosis -- if anything it corroborates it more
strongly than the document itself demonstrates.

Exact symbolic (sympy) arithmetic throughout -- no floating point, no
randomness, no seed needed.
"""
import sympy as sp

n, a, b, c, d = sp.symbols('n a b c d')

# K=2 exact values, independently re-derived by our own brute-force
# enumeration (bruteforce_definition4.py, Section 6) -- confirmed
# identical to the document's own table.
data = {
    3: sp.Rational(10, 27),
    4: sp.Rational(49, 144),
    5: sp.Rational(33, 100),
    6: sp.Rational(44, 135),
    7: sp.Rational(143, 441),
}
target = sp.Rational(1, 3)  # 1/(K+1) at K=2

print("=" * 78)
print("K=2 rational-fit extrapolation test (reproducing/stress-testing")
print("ATTEMPT.md Sec 4.1's claimed failure)")
print("=" * 78)

# --- 3-parameter fit, as reported in the document ---
model3 = target + a / n + b / n**2 + c / n**3
eqs3 = [sp.Eq(model3.subs(n, k), data[k]) for k in (3, 4, 5)]
sol3 = sp.solve(eqs3, [a, b, c])
pred3_6 = sp.simplify(model3.subs(sol3).subs(n, 6))
pred3_7 = sp.simplify(model3.subs(sol3).subs(n, 7))
print(f"3-param ansatz 1/3+a/n+b/n^2+c/n^3, fit on n=3,4,5: {sol3}")
print(f"  predicts n=6: {pred3_6}  actual: {data[6]}  "
      f"MATCH={sp.simplify(pred3_6 - data[6]) == 0}")
print(f"  predicts n=7: {pred3_7}  actual: {data[7]}  "
      f"MATCH={sp.simplify(pred3_7 - data[7]) == 0}")
assert sp.simplify(pred3_6 - data[6]) != 0
assert sp.simplify(pred3_7 - data[7]) != 0
print("  CONFIRMED: 3-param fit fails to predict n=6,7, exactly as the "
      "document reports.")
print()

# --- richer 4-parameter fit: does adding one more term rescue it? ---
model4 = target + a / n + b / n**2 + c / n**3 + d / n**4
eqs4 = [sp.Eq(model4.subs(n, k), data[k]) for k in (3, 4, 5, 6)]
sol4 = sp.solve(eqs4, [a, b, c, d])
pred4_7 = sp.simplify(model4.subs(sol4).subs(n, 7))
print(f"4-param ansatz 1/3+a/n+b/n^2+c/n^3+d/n^4, fit on n=3,4,5,6: {sol4}")
print(f"  predicts n=7: {pred4_7}  actual: {data[7]}  "
      f"MATCH={sp.simplify(pred4_7 - data[7]) == 0}")
assert sp.simplify(pred4_7 - data[7]) != 0
print("  CONFIRMED: even a RICHER 4-parameter fit (using 4 exact data")
print("  points, one more than the document's 3-param/3-point attempt)")
print("  STILL fails to predict the 5th point. This corroborates -- does")
print("  NOT contradict -- ATTEMPT.md Sec 4.1's claim that the true K=2")
print("  joint closed form needs more structure than a small polynomial-")
print("  in-1/n fit can recover from a handful of points. If anything")
print("  this is stronger evidence for the difficulty than the document")
print("  itself presents.")
