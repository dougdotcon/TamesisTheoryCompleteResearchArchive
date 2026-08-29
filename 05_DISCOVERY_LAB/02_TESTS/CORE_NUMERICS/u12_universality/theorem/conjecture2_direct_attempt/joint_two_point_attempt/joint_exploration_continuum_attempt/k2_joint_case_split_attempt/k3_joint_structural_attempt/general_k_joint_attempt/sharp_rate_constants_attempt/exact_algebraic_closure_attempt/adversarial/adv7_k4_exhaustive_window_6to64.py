"""
Independent, from-scratch exhaustive exact check: for every integer
n=6..64 (K=4), confirm h(n,x) >= -M4 for all x in [0,1], via exact
Poly(...).real_roots() calculus (critical points of h(n,.) on [0,1],
plus endpoints), NOT sampling. This is a completely fresh implementation,
written without reading the target's own k4_exact_closure.py Step 7.

Also reports h(n,x) <= M4 (the upper-bound side) over the same window,
as an extra free cross-check.
"""
import sympy as sp
import pickle, time

n, x, t = sp.symbols('n x t')

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_Nx_Dn.pkl','rb') as f:
    d = pickle.load(f)
Nx, Dn = d['Nx'], d['Dn']

g4 = -6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x
g4p_poly = sp.Poly(sp.diff(g4,x), x)
x4star = [r for r in g4p_poly.real_roots() if 0 < r < 1][0]
M4 = sp.simplify(g4.subs(x, x4star))
M4_num = sp.N(M4, 30)
print("M4 =", M4_num)

results = []
t0 = time.time()
worst_margin_lower = None
worst_n_lower = None
worst_margin_upper = None
worst_n_upper = None
violations = 0

for nn in range(6, 65):
    Nx_n = sp.expand(Nx.subs(n, nn))
    Dn_n = Dn.subs(n, nn)
    h_expr = sp.cancel(nn*Nx_n/Dn_n)
    dh = sp.together(sp.diff(h_expr, x))
    num_dh, den_dh = sp.fraction(dh)
    crit_poly = sp.Poly(sp.expand(num_dh), x)
    crits = crit_poly.real_roots()
    crits_in_01 = [c for c in crits if 0 <= c <= 1]
    candidates = list(crits_in_01) + [sp.Integer(0), sp.Integer(1)]
    vals = [sp.N(h_expr.subs(x, c), 30) for c in candidates]
    hmin = min(vals)
    hmax = max(vals)
    margin_lower = hmin - (-M4_num)   # should be >= 0
    margin_upper = M4_num - hmax      # should be >= 0
    if margin_lower < 0 or margin_upper < 0:
        violations += 1
        print(f"  *** VIOLATION at n={nn}: hmin={hmin} hmax={hmax}")
    if worst_margin_lower is None or margin_lower < worst_margin_lower:
        worst_margin_lower = margin_lower
        worst_n_lower = nn
    if worst_margin_upper is None or margin_upper < worst_margin_upper:
        worst_margin_upper = margin_upper
        worst_n_upper = nn
    results.append((nn, hmin, hmax, margin_lower, margin_upper))

t1 = time.time()
print(f"\nChecked n=6..64 ({len(results)} values) in {t1-t0:.2f}s")
print(f"Violations: {violations}")
print(f"Worst lower-bound margin: {worst_margin_lower} at n={worst_n_lower}")
print(f"Worst upper-bound margin: {worst_margin_upper} at n={worst_n_upper}")

print("\nPer-n table (n, hmin, margin_lower=hmin+M4):")
for nn, hmin, hmax, ml, mu in results:
    print(f"  n={nn:3d}  hmin={float(hmin):+.6f}  margin_lower={float(ml):.6f}  hmax={float(hmax):+.6f}  margin_upper={float(mu):.6f}")
