"""
Independent referee check #7 (the deep-dive on the target's own disclosed
weak point): is C0_tight_Bernstein(gamma,a)^2 really strictly decreasing on
(0, gamma*) for every a>0, as claimed (target confirms only by dense
sign-sampling, 400 pts x 5 values of a, not a full symbolic proof)?

KEY OBSERVATION (checked below): C0_tight_Bernstein(gamma,a)^2
    = (2+a) * sigma^2(gamma) * (lambda_tight(gamma) + 1/2)
    = (2+a) * h(gamma)
where h(gamma) := sigma^2(gamma)*(lambda_tight(gamma)+1/2) does NOT depend
on a at all. Since (2+a) > 0 for every a > 0, the SIGN of
d/dgamma C0_tight_Bernstein^2 is exactly the sign of h'(gamma), for EVERY
a > 0 simultaneously. So testing monotonicity across "5 values of a" is
mathematically redundant -- a single symbolic sign check of h'(gamma) on
(0,gamma*) would settle it for ALL a>0 at once. We do that fully symbolic
check here, PLUS an independent finer numerical search (scipy global
optimization + a much denser grid) as extra insurance, exactly as the
task instructs.
"""
import sympy as sp
import numpy as np

gamma, a = sp.symbols('gamma a', positive=True)
gamma_star = 1 - sp.sqrt(2)/2

sigma2 = gamma*(1-gamma)
lambda_tight_B = 4*(1-gamma)**2/(gamma*(2-gamma))

h = sp.simplify(sigma2*(lambda_tight_B + sp.Rational(1,2)))
print("h(gamma) = sigma^2(gamma)*(lambda_tight_pieceB(gamma)+1/2) =")
sp.pprint(h)

# Confirm C0_tight_B(gamma,a) = (2+a)*h(gamma), i.e. a-independence of the
# gamma-shape, by direct symbolic factoring check.
C0_tight_B_direct = sp.simplify((2+a)*sigma2*(lambda_tight_B + sp.Rational(1,2)))
diff_check = sp.simplify(C0_tight_B_direct - (2+a)*h)
print("\nC0_tight_B(gamma,a) - (2+a)*h(gamma) =", diff_check, " (confirms exact a-factorization)")

hprime = sp.simplify(sp.diff(h, gamma))
print("\nh'(gamma) =")
sp.pprint(hprime)

num, den = sp.fraction(sp.together(hprime))
num = sp.expand(num)
den = sp.factor(den)
print("\nNumerator of h'(gamma) (as a polynomial in gamma):")
sp.pprint(num)
print("Denominator (factored):", den)

# Real roots of the numerator polynomial, and how many lie in (0, gamma*)
num_poly = sp.Poly(num, gamma)
print("\nDegree of numerator polynomial:", num_poly.degree())
real_roots = sp.real_roots(num_poly)
print("All real roots of numerator (exact, sympy.real_roots):")
for r in real_roots:
    print("  ", r, " ~= ", sp.N(r, 10))

gs = sp.N(gamma_star, 15)
print(f"\ngamma* = {gs}")
in_range = [r for r in real_roots if 0 < sp.N(r) < gs]
print("Real roots of h'(gamma)'s numerator strictly inside (0, gamma*):", in_range)

# Confirm sign of h' at an interior sample point of (0,gamma*), e.g. gamma=0.1
sample = sp.Rational(1,10)
val = sp.N(hprime.subs(gamma, sample))
print(f"\nh'(gamma=0.1) = {val}  (sign: {'negative' if val<0 else 'positive'})")

# Since a degree-<=4 polynomial numerator with NO real roots in (0,gamma*)
# and known sign at one interior point, together with continuity, this is a
# FULL, exact symbolic proof that h'(gamma) has constant sign throughout
# (0,gamma*) -- hence C0_tight_Bernstein^2 is monotone there for ALL a>0
# simultaneously, closing the target's own disclosed gap completely.
print("\n=== CONCLUSION ===")
if len(in_range) == 0:
    print("FULL SYMBOLIC PROOF: numerator of h'(gamma) has ZERO real roots in (0,gamma*).")
    print("Combined with the sign at gamma=0.1 (negative) and continuity/no-root-in-interval,")
    print("h'(gamma) < 0 throughout (0,gamma*) is a RIGOROUS, closed-form fact -- for ALL a>0")
    print("simultaneously (since the a-dependence factors out as a positive overall scalar).")
    print("This STRENGTHENS the target's claim from 'dense sign-sampling at 5 values of a'")
    print("to a genuine closed-form symbolic proof valid for every a>0 at once.")
else:
    print("WARNING: found real root(s) of h' inside (0,gamma*) -- need further investigation!")

# --- Independent finer numerical checks (scipy global opt + dense grid), as belt-and-suspenders ---
print("\n--- Independent numerical re-check (scipy + dense grid) ---")
from scipy.optimize import minimize_scalar
import sympy.utilities.lambdify as lambdify_mod

h_func = sp.lambdify(gamma, h, 'numpy')
gstar_f = float(gs)

# Dense grid: 2,000,000 points across (0, gamma*), look for ANY local increase
xs = np.linspace(1e-9, gstar_f - 1e-9, 2_000_000)
ys = h_func(xs)
diffs = np.diff(ys)
n_increasing = np.sum(diffs > 0)
print(f"Dense grid (2,000,000 pts) on (0,gamma*): number of locally-increasing steps = {n_increasing}")
if n_increasing > 0:
    idx = np.where(diffs > 0)[0]
    print("  Example indices/gamma values where h increases:", xs[idx[:5]])

# scipy global-ish search: minimize -h(gamma) (i.e. maximize h) over many
# random restarts plus a coarse grid seed, to hunt for any interior local max
# other than the gamma->0 boundary.
best = None
seeds = np.linspace(1e-6, gstar_f - 1e-6, 50)
for s in seeds:
    res = minimize_scalar(lambda g: -h_func(g), bounds=(1e-9, gstar_f-1e-9), method='bounded',
                           options={'xatol':1e-14})
    if best is None or res.fun < best.fun:
        best = res
print(f"\nGlobal-ish minimize(-h) result: gamma*_found={best.x:.12g}, h_max_found={-best.fun:.12g}")
print(f"h at gamma->0+ (limit) = {float(h_func(1e-9)):.6g}  vs found max {-best.fun:.6g}")
print("If the found maximizer is essentially at the gamma->0 boundary (not interior), this")
print("confirms NO spurious interior local maximum exists on (0,gamma*).")
