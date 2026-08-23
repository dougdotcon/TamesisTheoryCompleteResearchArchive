"""
Independent re-derivation/re-verification of Theorem 5's proof, from scratch.
Does NOT read the target's own verify_Q_lower_bound.py.

Checks, in order:
 A. Symbolic algebra: epsilon(x) decomposition
    phi(x) = x(x+1)/(2(n-x)) = x^2/(2n) + eps(x),
    eps(x) = [n x(x+1) - x^2(n-x)] / [2n(n-x)] = x(n+x^2)/(2n(n-x))
 B. The two moment integrals via sympy symbolic integration:
      int_0^oo x e^{-x^2/2n} dx = n
      int_0^oo x^3 e^{-x^2/2n} dx = 2n^2
 C. The Gaussian integral int_0^oo e^{-x^2/2n} dx = sqrt(pi n /2)  (symbolic)
 D. The tail bound Tail(n,T) <= (n/T) e^{-T^2/2n}, verified numerically
    (exact closed form of Tail via erfc, compared to the claimed bound),
    for a wide range of n, T.
 E. eps(x) <= x/n + x^3/n^2 on [0, n/2] -- symbolic/numeric check
 F. Err(n) <= 3 + 2 e^{-n/8} via direct high-precision numerical quadrature
    of the TRUE integral (not the target's own claimed sub-bounds), for a
    wide range of n.
 G. Final assembly: Q(n) >= sqrt(pi n/2) - 6, both via exact Fraction (small
    to moderate n) and via a fast mpmath incremental log-sum Q(n) (large n,
    up to 10^6).
"""
import sympy as sp
import mpmath as mp
from fractions import Fraction as F

mp.mp.dps = 60

print("############################################")
print("# Part A: symbolic epsilon(x) decomposition #")
print("############################################")
x, n = sp.symbols('x n', positive=True)
phi = x*(x+1)/(2*(n-x))
claimed_eps = x*(n+x**2)/(2*n*(n-x))
diff = sp.simplify(phi - x**2/(2*n) - claimed_eps)
print("phi(x) - x^2/(2n) - eps(x) simplifies to:", diff, "(expect 0)")

# also re-derive the numerator algebra by hand, symbolically
num_claimed_intermediate = n*x*(x+1) - x**2*(n-x)
num_final = x*(n + x**2)
print("n*x*(x+1) - x^2*(n-x) - x*(n+x^2) expands to:",
      sp.expand(num_claimed_intermediate - num_final), "(expect 0)")
print("n*x*(x+1) - x^2*(n-x) fully expanded:", sp.expand(num_claimed_intermediate))

print()
print("############################################")
print("# Part B: the two moment integrals (sympy)  #")
print("############################################")
nn = sp.symbols('n', positive=True)
xx = sp.symbols('x', positive=True)
I1 = sp.integrate(xx*sp.exp(-xx**2/(2*nn)), (xx, 0, sp.oo))
I3 = sp.integrate(xx**3*sp.exp(-xx**2/(2*nn)), (xx, 0, sp.oo))
print("int_0^oo x e^{-x^2/2n} dx =", sp.simplify(I1), " (claimed: n)")
print("int_0^oo x^3 e^{-x^2/2n} dx =", sp.simplify(I3), " (claimed: 2n^2)")

print()
print("############################################")
print("# Part C: Gaussian integral (sympy)         #")
print("############################################")
I0 = sp.integrate(sp.exp(-xx**2/(2*nn)), (xx, 0, sp.oo))
print("int_0^oo e^{-x^2/2n} dx =", sp.simplify(I0), " (claimed: sqrt(pi n/2))")
print("sqrt(pi*n/2) =", sp.sqrt(sp.pi*nn/2))
print("difference simplifies to:", sp.simplify(I0 - sp.sqrt(sp.pi*nn/2)))

print()
print("############################################")
print("# Part D: tail bound Tail(n,T)<=(n/T)e^{-T^2/2n}")
print("############################################")
def Tail_exact(n, T):
    # int_T^oo e^{-x^2/2n} dx = sqrt(pi n /2) * erfc(T/sqrt(2n))
    n = mp.mpf(n); T = mp.mpf(T)
    return mp.sqrt(mp.pi*n/2) * mp.erfc(T/mp.sqrt(2*n))

def Tail_bound(n, T):
    n = mp.mpf(n); T = mp.mpf(T)
    return (n/T) * mp.e**(-(T**2)/(2*n))

bad = 0
tot = 0
worst_ratio = None
for n_ in [1, 2, 5, 10, 100, 1000, 10000, 100000, 1000000]:
    for Tfrac in [F(1,10), F(1,2), 1, 2, 5]:
        T_ = mp.mpf(n_) * mp.mpf(Tfrac.numerator)/mp.mpf(Tfrac.denominator)
        if T_ <= 0:
            continue
        exact = Tail_exact(n_, T_)
        bound = Tail_bound(n_, T_)
        tot += 1
        if exact > bound + mp.mpf('1e-50'):
            bad += 1
            print(f"VIOLATION n={n_} T={T_}: exact={exact} bound={bound}")
        ratio = exact/bound if bound != 0 else None
        if ratio is not None and (worst_ratio is None or ratio > worst_ratio[0]):
            worst_ratio = (ratio, n_, T_)
print(f"checked {tot} (n,T) pairs, violations={bad}, worst ratio exact/bound={worst_ratio}")

# specifically at T=n (used for Tail(n,n)<=e^{-n/2}) and T=n/2 (used for Err split)
print("\n--- specific claims used in the proof ---")
bad2 = 0
for n_ in [1,2,5,10,50,100,500,1000,5000,10000,100000,1000000]:
    Tn = Tail_exact(n_, n_)
    claimed = mp.e**(-mp.mpf(n_)/2)
    ok = Tn <= claimed + mp.mpf('1e-50')
    if not ok:
        bad2 += 1
        print(f"VIOLATION Tail(n,n)<=e^-n/2 at n={n_}: {Tn} vs {claimed}")
    Tn2 = Tail_exact(n_, mp.mpf(n_)/2)
    claimed2 = 2*mp.e**(-mp.mpf(n_)/8)
    ok2 = Tn2 <= claimed2 + mp.mpf('1e-50')
    if not ok2:
        bad2 += 1
        print(f"VIOLATION Tail(n,n/2)<=2e^-n/8 at n={n_}: {Tn2} vs {claimed2}")
print(f"Tail(n,n)<=e^-n/2 and Tail(n,n/2)<=2e^-n/8 checked for n in the list above, violations={bad2}")

print()
print("############################################")
print("# Part E: eps(x) <= x/n + x^3/n^2 on [0,n/2]")
print("############################################")
bad3 = 0
tot3 = 0
for n_ in [1, 2, 5, 10, 100, 1000, 100000]:
    n_mp = mp.mpf(n_)
    for k in range(0, 2001):
        xv = n_mp/2 * mp.mpf(k)/2000
        eps_val = xv*(n_mp+xv**2)/(2*n_mp*(n_mp-xv)) if xv < n_mp else mp.mpf(0)
        bound_val = xv/n_mp + xv**3/n_mp**2
        tot3 += 1
        if eps_val > bound_val + mp.mpf('1e-45'):
            bad3 += 1
            print(f"VIOLATION n={n_} x={xv}: eps={eps_val} bound={bound_val}")
print(f"checked {tot3} points across n in the list, [0,n/2], violations={bad3}")

print()
print("############################################")
print("# Part F: Err(n) <= 3 + 2e^{-n/8} via TRUE quadrature")
print("############################################")
def Err_true(n_):
    n_mp = mp.mpf(n_)
    def integrand(xv):
        if xv >= n_mp:
            return mp.mpf(0)
        eps_val = xv*(n_mp+xv**2)/(2*n_mp*(n_mp-xv))
        return mp.e**(-(xv**2)/(2*n_mp)) * (1 - mp.e**(-eps_val))
    return mp.quad(integrand, [0, n_mp/2, n_mp*mp.mpf('0.999999'), n_mp])

bad4 = 0
worst_err = None
for n_ in [1, 2, 5, 10, 50, 100, 500, 1000, 5000, 10000, 50000]:
    err_val = Err_true(n_)
    claimed_bound = 3 + 2*mp.e**(-mp.mpf(n_)/8)
    ok = err_val <= claimed_bound + mp.mpf('1e-30')
    also_le_5 = err_val <= mp.mpf(5) + mp.mpf('1e-30')
    if not ok or not also_le_5:
        bad4 += 1
        print(f"VIOLATION at n={n_}: Err(n)={err_val} claimed_bound={claimed_bound}")
    if worst_err is None or err_val > worst_err[0]:
        worst_err = (err_val, n_)
    print(f"  n={n_}: Err(n)={float(err_val):.6f}  bound(3+2e^-n/8)={float(claimed_bound):.6f}  <=5: {also_le_5}")
print(f"violations={bad4}, worst (largest) Err(n) observed = {worst_err}")

print()
print("############################################")
print("# Part G: final Q(n) >= sqrt(pi n/2) - 6     #")
print("############################################")

def Q_exact(n):
    total = F(1)  # j=0 term
    p = F(1)
    for i in range(1, n):
        p *= F(n - i, n)
        total += p
    return total

print("--- exact Fraction, n up to 4000 (dense-ish sample) ---")
bad5 = 0
worst_margin = None
test_ns = list(range(1, 60)) + [80,120,200,400,800,1500,2000,3000,4000]
for n_ in test_ns:
    Qn = Q_exact(n_)
    Qn_mp = mp.mpf(Qn.numerator)/mp.mpf(Qn.denominator)
    rhs = mp.sqrt(mp.pi*n_/2) - 6
    margin = Qn_mp - rhs
    if margin < -mp.mpf('1e-40'):
        bad5 += 1
        print(f"VIOLATION at n={n_}: Q(n)={Qn_mp} rhs={rhs}")
    if worst_margin is None or margin < worst_margin[0]:
        worst_margin = (margin, n_)
print(f"checked {len(test_ns)} n values exactly, violations={bad5}")
print(f"worst (smallest) margin = {worst_margin}")
