#!/usr/bin/env python3
"""
Independent verification of the K=4 analytic tail-bound decomposition:
  n*Delta4_n(x) = g4(x) + B(x)/n + Bbar(x)/n^2 + C(x)/(n-1) + 2*D(x)/(n-2)
                  + 3*E(x)/(n-3)
via an independent undetermined-coefficients ansatz (not sp.apart, not
the front's own method), confirming B,Bbar,C,D,E and their max/min on
[0,1], and reconstructing C_4 at N0=1000.
"""
import sympy as sp

n, x, k = sp.symbols('n x k')

Q = ( -k**6 + 9*k**5 + (4*n**2-18*n-31)*k**4 + (-16*n**2+80*n+51)*k**3
      + (-6*n**4+42*n**3-55*n**2-120*n-40)*k**2
      + (6*n**4-50*n**3+97*n**2+70*n+12)*k
      + 4*n**6-30*n**5+74*n**4-52*n**3-30*n**2-12*n )
D4_k = k*(k+1)*Q / (n**5*(n-1)*(n-2)*(n-3))
F4 = 1-(1-x**2)**4
Delta4 = sp.cancel(D4_k.subs(k, n*x) - F4)
nDelta4 = sp.cancel(n*Delta4)

g4 = sp.expand(-6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x)

rem = sp.together(nDelta4 - g4)

Bx, Bbx, Cx, Dx, Ex = sp.symbols('Bx Bbx Cx Dx Ex')
ansatz = Bx/n + Bbx/n**2 + Cx/(n-1) + 2*Dx/(n-2) + 3*Ex/(n-3)
diff_expr = sp.together(rem - ansatz)
numer = sp.numer(diff_expr)
numer_poly = sp.Poly(sp.expand(numer), n)
eqs = list(numer_poly.all_coeffs())
sol = sp.solve(eqs, [Bx, Bbx, Cx, Dx, Ex], dict=True)
print("solved:", len(sol), "solution(s)")
s = sol[0]
Bexpr = sp.expand(s[Bx]); Bbexpr = sp.expand(s[Bbx]); Cexpr = sp.expand(s[Cx])
Dexpr = sp.expand(s[Dx]); Eexpr = sp.expand(s[Ex])
print("B(x)    =", Bexpr)
print("Bbar(x) =", Bbexpr)
print("C(x)    =", Cexpr)
print("D(x)    =", Dexpr)
print("E(x)    =", Eexpr)

Bbar_claimed = 2*x - 2*x**2
print("\nBbar - claimed(2x-2x^2):", sp.simplify(Bbexpr - Bbar_claimed))

reconstructed = g4 + Bexpr/n + Bbexpr/n**2 + Cexpr/(n-1) + 2*Dexpr/(n-2) + 3*Eexpr/(n-3)
check = sp.simplify(sp.cancel(reconstructed - nDelta4))
print("\nreconstructed - nDelta4 (expect 0):", check)

def maxmin_on_01(expr):
    p = sp.diff(expr, x)
    poly = sp.Poly(sp.expand(p), x)
    crit = [r for r in poly.real_roots() if 0 <= r <= 1] if poly.degree() > 0 else []
    cands = [sp.Integer(0), sp.Integer(1)] + crit
    vals = [(sp.N(expr.subs(x, c), 25), c) for c in cands]
    vmax = max(vals, key=lambda t: t[0])
    vmin = min(vals, key=lambda t: t[0])
    return vmax, vmin

print()
for name, expr in [('B', Bexpr), ('Bbar', Bbexpr), ('C', Cexpr), ('D', Dexpr), ('E', Eexpr)]:
    vmax, vmin = maxmin_on_01(expr)
    print(f"{name}(x): max={vmax[0]} at x={sp.N(vmax[1],10)}   min={vmin[0]} at x={sp.N(vmin[1],10)}")

Bmax = maxmin_on_01(Bexpr)[0][0]
Bbmax = maxmin_on_01(Bbexpr)[0][0]
Cmax = maxmin_on_01(Cexpr)[0][0]
Dmax = maxmin_on_01(Dexpr)[0][0]
Emax = maxmin_on_01(Eexpr)[0][0]
print(f"\nBmax={Bmax} (claimed 1.6339...)")
print(f"Bbarmax={Bbmax} (claimed 1/2=0.5)")
print(f"Cmax={Cmax} (claimed 0)")
print(f"Dmax={Dmax} (claimed 12)")
print(f"Emax={Emax} (claimed 0.0519...)")

g4p = sp.diff(g4, x)
proots = sp.Poly(g4p, x).real_roots()
interior = [r for r in proots if 0 < r < 1]
cands4 = interior + [sp.Integer(0), sp.Integer(1)]
M4 = max([g4.subs(x, c) for c in cands4], key=lambda v: sp.N(v, 30))
M4 = sp.N(M4, 40)
print(f"\nM4 = {M4}")

N0 = 1000
C4_reconstructed = M4 + Bmax/N0 + Bbmax/N0**2 + 2*Dmax/(N0-2) + 3*Emax/(N0-3)
print(f"C4 reconstructed at N0=1000: {sp.N(C4_reconstructed,30)}")
print("front's claimed C4:          0.7345569184500456912259...")
