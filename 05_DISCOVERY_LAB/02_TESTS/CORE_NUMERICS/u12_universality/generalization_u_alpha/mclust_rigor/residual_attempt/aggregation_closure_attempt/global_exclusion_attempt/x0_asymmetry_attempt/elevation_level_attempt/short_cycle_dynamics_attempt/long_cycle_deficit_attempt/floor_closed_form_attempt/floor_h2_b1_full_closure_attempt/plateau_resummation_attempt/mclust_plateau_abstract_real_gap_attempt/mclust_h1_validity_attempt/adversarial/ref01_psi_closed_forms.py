"""
REFEREE independent check (written from scratch, no target-front .py files
read). Verifies:
  (a) R(x) = sqrt(pi/2)*erfcx(x/sqrt(2)) satisfies R' = x R - 1, R(inf)=0.
  (b) psi3(x) := -e^{x^2/2} * int_x^inf e^{-t^2/2} * 7 R'(t) dt
      solves psi3' = x psi3 + 7 R'(x) (verified via finite-difference and
      via the general variation-of-parameters identity), and
      psi3(0) = (7/2) sqrt(pi/2) (claimed in ATTEMPT.md sec 3.3).
  (c) psi4(x) := (17/3) R'''(x), psi4(0) = -34/3 (claimed closed form of
      record, re-derived here via R''=R+xR', R'''=2R'+xR'').
"""
import mpmath as mp

mp.mp.dps = 60

def R(x):
    x = mp.mpf(x)
    return mp.sqrt(mp.pi/2) * mp.erfc(x/mp.sqrt(2)) * mp.e**(x*x/2)
    # erfcx(z) = e^{z^2} erfc(z); here z = x/sqrt(2), z^2 = x^2/2

def Rprime_direct(x):
    # derivative via mpmath's numerical differentiation (independent check)
    return mp.diff(R, x)

def Rprime_formula(x):
    x = mp.mpf(x)
    return x*R(x) - 1

print("=== (a) R' = xR - 1 check ===")
for xv in [0, 0.5, 1, 2, 3, 5, -1, -3]:
    a = Rprime_direct(xv)
    b = Rprime_formula(xv)
    print(f"x={xv:>5}: R'(numeric diff)={a}  xR-1={b}  reldiff={abs(a-b)/abs(b) if b!=0 else abs(a-b)}")

print()
print("R(20) (should be ~0, R(inf)=0):", R(20))
print()

# psi3 via the integral formula
def psi3_integral(x):
    x = mp.mpf(x)
    f = lambda t: mp.e**(-t*t/2) * 7 * Rprime_formula(t)
    integral = mp.quad(f, [x, mp.inf])
    return -mp.e**(x*x/2) * integral

print("=== (b) psi3 checks ===")
psi3_0 = psi3_integral(0)
target = mp.mpf(7)/2 * mp.sqrt(mp.pi/2)
print("psi3(0) computed  :", psi3_0)
print("(7/2)sqrt(pi/2)    :", target)
print("abs diff           :", abs(psi3_0 - target))
print("rel diff           :", abs(psi3_0 - target)/target)
print()

# verify psi3 solves psi3' = x psi3 + 7 R'(x) via numerical differentiation
print("Check psi3' = x*psi3 + 7*R'(x) at a few x (numerical differentiation of the integral form):")
for xv in [0, 0.5, 1, 2, 3]:
    psi3_deriv = mp.diff(psi3_integral, xv)
    rhs = mp.mpf(xv)*psi3_integral(xv) + 7*Rprime_formula(xv)
    print(f"x={xv}: psi3'(numeric)={psi3_deriv}  x*psi3+7R'={rhs}  diff={abs(psi3_deriv-rhs)}")

print()
print("=== (b2) sign check: what if the leading minus sign (self-caught S2) were omitted? ===")
def psi3_integral_WRONG_no_minus(x):
    x = mp.mpf(x)
    f = lambda t: mp.e**(-t*t/2) * 7 * Rprime_formula(t)
    integral = mp.quad(f, [x, mp.inf])
    return mp.e**(x*x/2) * integral  # missing the leading minus

wrong0 = psi3_integral_WRONG_no_minus(0)
print("WRONG (no minus sign) psi3(0):", wrong0, " -- should be -target if sign is the only bug")
print("-target:", -target)

print()
print("=== (c) psi4 checks ===")
def Rpp(x):
    x = mp.mpf(x)
    return R(x) + x*Rprime_formula(x)   # R'' = R + x R'  (from differentiating R'=xR-1)

def Rppp(x):
    x = mp.mpf(x)
    return 2*Rprime_formula(x) + x*Rpp(x)  # R''' = 2R' + x R''

# cross-check via direct numerical differentiation of R three times
def Rppp_numeric(x):
    return mp.diff(R, x, 3)

for xv in [0, 0.5, 1, 2]:
    a = Rppp(xv)
    b = Rppp_numeric(xv)
    print(f"x={xv}: R'''(formula)={a}   R'''(numeric-diff)={b}   diff={abs(a-b)}")

print()
psi4_0 = mp.mpf(17)/3 * Rppp(0)
target4 = mp.mpf(-34)/3
print("psi4(0) = (17/3) R'''(0) =", psi4_0)
print("claimed -34/3            =", target4)
print("diff                      =", abs(psi4_0 - target4))

print()
print("=== (d) sanity: R(0), R'(0), R''(0), R'''(0) exact-ish values ===")
print("R(0)    =", R(0), " expect sqrt(pi/2) =", mp.sqrt(mp.pi/2))
print("R'(0)   =", Rprime_formula(0), " expect -1")
print("R''(0)  =", Rpp(0), " expect sqrt(pi/2)")
print("R'''(0) =", Rppp(0), " expect -2")
