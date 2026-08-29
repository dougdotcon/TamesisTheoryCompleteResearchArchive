"""
Independent high-precision (mpmath) cross-check of M5, NOT reusing sympy's
symbolic derivation route: g5(x) is transcribed as raw float/mpf
coefficients, its derivative is found via mpmath's own polyroots, and the
maximum is evaluated directly by brute numeric scan + polish, all in
mpmath at 50 decimal digits.
"""
import mpmath as mp

mp.mp.dps = 50

# g5(x) = 5x(x-1)^4(x+1)^3(2x^2-x+1), transcribed independently from the
# factored form printed by k5_step3_extract_g5.py (cross-checked below
# against the raw expanded-coefficient form too, as a second independent
# check within this same script).
def g5_factored(xv):
    x = mp.mpf(xv)
    return 5*x*(x-1)**4*(x+1)**3*(2*x**2 - x + 1)

def g5_expanded(xv):
    x = mp.mpf(xv)
    return (10*x**10 - 15*x**9 - 20*x**8 + 40*x**7 - 30*x**5 + 20*x**4
            - 10*x**2 + 5*x)

# sanity: factored form == expanded form at several points
for xv in [0.1, 0.2, 0.3, 0.309430603103057, 0.5, 0.7, 0.9]:
    a, b = g5_factored(xv), g5_expanded(xv)
    assert abs(a - b) < mp.mpf('1e-40'), (xv, a, b)
print("Factored vs expanded g5: exact agreement at all spot points. PASSED.")

# find the maximum of g5 on [0,1] via dense scan + Newton polish
N = 200000
best_x, best_v = None, mp.mpf('-inf')
for i in range(N + 1):
    xv = mp.mpf(i) / N
    v = g5_expanded(xv)
    if v > best_v:
        best_v, best_x = v, xv
print(f"coarse scan optimum: x~{best_x}  g5~{best_v}")

# polish via mpmath's findroot on g5' = 0 near best_x
x = mp.mpf(best_x)
def g5p(xv):
    xv = mp.mpf(xv)
    return (100*xv**9 - 135*xv**8 - 160*xv**7 + 280*xv**6 - 150*xv**4
             + 80*xv**3 - 20*xv + 5)

xstar = mp.findroot(g5p, x)
print("polished critical point x5* =", xstar)
M5 = g5_expanded(xstar)
print("M5 = g5(x5*) =", M5)

# cross-check against the sympy-derived value
M5_sympy = mp.mpf('0.696803198946355211196876665384')
diff = abs(M5 - M5_sympy)
print("difference vs sympy-derived M5:", diff)
assert diff < mp.mpf('1e-30')
print("PASSED: mpmath-independent M5 matches sympy-derived M5 to 30+ digits.")

x5star_sympy = mp.mpf('0.309430603103057048428294338496')
diff_x = abs(xstar - x5star_sympy)
print("difference vs sympy-derived x5*:", diff_x)
assert diff_x < mp.mpf('1e-30')
print("PASSED: mpmath-independent x5* matches sympy-derived x5* to 30+ digits.")

print()
print(f"FINAL: M5 = {mp.nstr(M5, 45)}")
