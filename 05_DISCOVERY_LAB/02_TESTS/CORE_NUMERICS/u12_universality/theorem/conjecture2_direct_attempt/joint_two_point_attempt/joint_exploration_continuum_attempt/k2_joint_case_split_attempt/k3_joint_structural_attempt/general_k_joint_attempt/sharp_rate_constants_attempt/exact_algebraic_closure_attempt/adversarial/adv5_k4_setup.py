"""
Independent K=4 setup: build N(n,x), D(n) for Delta4_n(x), confirm g_4,
M_4, and boundary h(n,1) closed form.
"""
import sympy as sp

n, k, x, t = sp.symbols('n k x t')

Q = (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4 + (-16*n**2 + 80*n + 51)*k**3
     + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
     + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
     + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)
D4_num = k*(k+1)*Q
D4_den = n**5*(n-1)*(n-2)*(n-3)
F4n = D4_num / D4_den
F4_cont = 1 - (1-x**2)**4

Delta4 = sp.cancel(F4n.subs(k, n*x) - F4_cont)
Nx, Dn = sp.fraction(Delta4)
Nx = sp.expand(Nx)
Dn = sp.factor(Dn)
print("Reduced D(n) =", Dn)
print("N(n,x) degree in n:", sp.Poly(Nx, n).degree())
print("N(n,x) degree in x:", sp.Poly(Nx, x).degree())

# save Nx, Dn to a file for reuse
with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_Nx_Dn.pkl','wb') as f:
    import pickle
    pickle.dump({'Nx': Nx, 'Dn': Dn}, f)

print("\nh(n,1) =", sp.cancel(n*Nx.subs(x,1)/Dn))

g4 = -6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x
g4p = sp.expand(sp.diff(g4, x))
g4p_poly = sp.Poly(g4p, x)
x4star = [r for r in g4p_poly.real_roots() if 0 < r < 1][0]
M4 = sp.simplify(g4.subs(x, x4star))
print("\nM4 =", sp.N(M4, 25))
M4_minpoly = sp.minimal_polynomial(M4, t)
print("M4 minpoly:", M4_minpoly)

print("\nh(6,1) =", sp.cancel(n*Nx.subs(x,1)/Dn).subs(n,6))
print("Compare -M4:", -sp.N(M4,20))
