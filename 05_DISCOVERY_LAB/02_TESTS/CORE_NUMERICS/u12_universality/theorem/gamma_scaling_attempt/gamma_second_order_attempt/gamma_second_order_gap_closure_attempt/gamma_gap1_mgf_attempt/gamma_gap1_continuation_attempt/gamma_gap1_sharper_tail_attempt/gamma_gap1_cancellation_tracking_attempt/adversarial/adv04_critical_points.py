"""
Independent referee check #4: the two critical points of
x_K'(D) = c1 + 2*c2*D + 3*c3*D^2 = 0 (quadratic in D, coefficients at k=K).

Verify:
 (a) the quadratic formula gives two real roots (generically)
 (b) one root is O(n) (asymptotically far outside the O(K)=O(sqrt(n ln n))
     support)
 (c) the other root equals the target's claimed closed form
     D* = -K*gamma + K + n - sqrt(36 n^2 + 3)/6 - 1/2
     and that this differs from D_max=(1-gamma)K by exactly -1/2+O(1/n)
 (d) x_K'(D*) = 0 exactly (symbolic check)
 (e) sqrt(36n^2+3)/6 = n + O(1/n)  (elementary asymptotic fact)
"""
import sympy as sp

n, gamma, k, D = sp.symbols('n gamma k D', positive=True)

c0 = gamma*k*(2*gamma**2*k**2 - 6*gamma*k**2 + 3*gamma*k + 6*k**2 - 6*k + 1) / (12*n**2)
c1 = (gamma**2*k**2/2 - gamma*k**2 - gamma*k*n + gamma*k/2 + k**2/2 + k*n - k/2 - n/2 + sp.Rational(1,12)) / n**2
c2 = (2*gamma*k - 2*k - 2*n + 1) / (4*n**2)
c3 = sp.Rational(1,6) / n**2

xprime = c1 + 2*c2*D + 3*c3*D**2   # quadratic in D

# Solve exactly via sympy (should reproduce quadratic formula)
roots = sp.solve(sp.Eq(xprime, 0), D)
print("Number of roots found:", len(roots))
for i, r in enumerate(roots):
    print(f"root[{i}] = {sp.simplify(r)}")

# Now substitute k -> K = sqrt(4 n ln(n)/beta) is transcendental; instead the
# target's closed form for D* doesn't carry k=K substituted in this specific
# form (it's expressed with K as a free symbol still, alongside n). Let's
# keep k=K symbolic (call it Ksym) and compare against target's formula,
# which is stated in terms of K, gamma, n:
# D* = -K*gamma + K + n - sqrt(36 n^2+3)/6 - 1/2
Ksym = sp.symbols('K', positive=True)
xprime_K = xprime.subs(k, Ksym)
roots_K = sp.solve(sp.Eq(xprime_K, 0), D)
print("\nRoots with k replaced by symbolic K:")
for i, r in enumerate(roots_K):
    r_s = sp.simplify(r)
    print(f"root[{i}] = {r_s}")

target_Dstar = -Ksym*gamma + Ksym + n - sp.sqrt(36*n**2+3)/6 - sp.Rational(1,2)

print("\nChecking which of the two roots matches the target's closed form D*...")
for i, r in enumerate(roots_K):
    diff = sp.simplify(r - target_Dstar)
    print(f"root[{i}] - target_Dstar = {diff}")

# Verify x_K'(D*) = 0 exactly by direct substitution (not via solve, to
# double check independently)
print("\nDirect verification x_K'(D*) = 0 (substitute target's D* into xprime_K):")
check = sp.simplify(xprime_K.subs(D, target_Dstar))
print("xprime_K(D*) =", check)

# sqrt(36n^2+3)/6 = n + O(1/n) check: series expansion
expr = sp.sqrt(36*n**2+3)/6
series = sp.series(expr, n, sp.oo, 3)
print("\nSeries of sqrt(36n^2+3)/6 as n->oo:", series)

# D* - D_max = ? (D_max = (1-gamma)*K)
D_max = (1-gamma)*Ksym
diff_Dstar_Dmax = sp.simplify(target_Dstar - D_max)
print("\nD* - D_max (target's closed form) =", diff_Dstar_Dmax)
print("As n->oo this should be exactly -1/2 + O(1/n); series in n:")
series2 = sp.series(diff_Dstar_Dmax, n, sp.oo, 2)
print(series2)
