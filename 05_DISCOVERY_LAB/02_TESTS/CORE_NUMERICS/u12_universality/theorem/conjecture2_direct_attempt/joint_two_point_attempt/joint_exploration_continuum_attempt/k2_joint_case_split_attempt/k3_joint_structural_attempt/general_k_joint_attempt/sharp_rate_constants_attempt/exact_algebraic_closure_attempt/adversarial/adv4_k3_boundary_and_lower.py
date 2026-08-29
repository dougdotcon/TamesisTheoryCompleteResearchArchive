"""
Independent check of K=3: boundary h(n,1) closed form + threshold vs M_3,
and the "touches-zero" lower-bound locus (largest real root claimed ~5.968).
Also direct exact per-n checks n=5,6,7,8 for sanity.
"""
import sympy as sp

n, k, x, t = sp.symbols('n k x t')

D3_num = k*(k+1)*(k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2 + (3*n**2 - 11*n - 2)*k
                  + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
D3_den = n**4*(n-1)*(n-2)
F3n = D3_num / D3_den
F3_cont = 1 - (1-x**2)**3

Delta3 = sp.cancel(F3n.subs(k, n*x) - F3_cont)
Nx, Dn = sp.fraction(Delta3)
Nx = sp.expand(Nx)

print("="*70)
print("Boundary h(n,1) = n*N(n,1)/D(n)")
print("="*70)
h_n1 = sp.simplify(n*Nx.subs(x,1)/Dn)
h_n1 = sp.cancel(h_n1)
print("h(n,1) =", h_n1)

M3 = sp.Rational(0)  # placeholder, we'll use algebraic M3 via CRootOf
g3 = 3*x**6 - 3*x**5 - 3*x**2 + 3*x
g3p = sp.expand(sp.diff(g3, x))
g3p_poly = sp.Poly(g3p, x)
x3star = [r for r in g3p_poly.real_roots() if 0 < r < 1][0]
M3 = sp.simplify(g3.subs(x, x3star))
print("M3 (exact algebraic) =", sp.N(M3, 25))

eq = sp.Eq(h_n1, M3)
# solve h(n,1) = M3 for n (rational function = algebraic number)
# h(n,1) presumably = 6/((n-1)(n-2)); let's confirm then solve directly
print("\nsimplify check: h(n,1) - 6/((n-1)*(n-2)) =", sp.simplify(h_n1 - sp.Rational(6,1)/((n-1)*(n-2))))

# Solve 6/((n-1)(n-2)) = M3 numerically (M3 known to 30 digits, fine for this purpose)
M3_num = sp.N(M3, 30)
n_poly_num = sp.expand((n-1)*(n-2) - 6/M3_num)
print("\nnumeric polynomial for n (from h(n,1)=M3):", n_poly_num)
n_poly_rat = sp.nsimplify(n_poly_num, rational=False)
sol = sp.solve(sp.Eq((n-1)*(n-2), 6/M3_num), n)
print("solutions:", sol)
positive_sol = [sp.N(s,20) for s in sol if sp.im(s) == 0 and sp.re(s) > 0]
print("positive real root n0 =", positive_sol)

print("\nh(5,1) =", h_n1.subs(n,5), " vs M3 =", sp.N(M3,20))
print("h(4,1) =", h_n1.subs(n,4))
print("h(3,1) =", h_n1.subs(n,3))

print("\n" + "="*70)
print("Lower bound 'touches-zero' locus: resultant_x(dN/dx, N) -> roots in n")
print("="*70)
F1 = sp.expand(sp.diff(Nx, x))
Rtz = sp.resultant(F1, Nx, x)
Rtz = sp.factor(Rtz)
print("Resultant (touches-zero) factor form (first 300 chars):", str(Rtz)[:300])

Rtz_poly = sp.Poly(sp.expand(Rtz) if not Rtz.is_Mul else sp.expand(sp.together(Rtz)), n) if False else None
# factor_list then find real roots of the "genuine" part
content, facs = sp.factor_list(Rtz, n)
print("\nfactor_list content:", content)
for fac, mult in facs:
    d = sp.Poly(fac, n).degree()
    print(f"  factor deg={d} mult={mult}")

# Get all real roots of the full resultant (including multiplicities from spurious factors,
# doesn't matter for finding the largest real root - just need real_roots of full expression)
Rtz_expand = sp.expand(Rtz)
Rtz_full_poly = sp.Poly(Rtz_expand, n)
rr = Rtz_full_poly.real_roots()
rr_num = sorted(set(sp.N(r,20) for r in rr))
print("\nreal roots of touches-zero resultant (numeric, deduped):")
for r in rr_num:
    print("  ", r)
print("\nlargest real root:", rr_num[-1])

print("\n" + "="*70)
print("Direct exact per-n check n=5,6,7,8: sup_x h(n,x) and inf_x h(n,x)")
print("="*70)
for nn in [5,6,7,8,10,20]:
    Nx_n = Nx.subs(n, nn)
    Dn_n = Dn.subs(n, nn)
    h_expr = sp.expand(nn*Nx_n)/Dn_n
    h_expr = sp.cancel(h_expr)
    dh = sp.diff(h_expr, x)
    dh_num = sp.together(dh)
    num_dh, den_dh = sp.fraction(dh_num)
    crit_poly = sp.Poly(sp.expand(num_dh), x)
    crits = crit_poly.real_roots()
    crits_in_01 = [c for c in crits if 0 <= c <= 1]
    candidates = list(crits_in_01) + [sp.Integer(0), sp.Integer(1)]
    vals = [(c, sp.nsimplify(h_expr.subs(x,c)) if False else sp.N(h_expr.subs(x,c),20)) for c in candidates]
    vals_sorted = sorted(vals, key=lambda p: p[1])
    print(f"n={nn}: min={vals_sorted[0]}  max={vals_sorted[-1]}")

print("\nDONE.")
