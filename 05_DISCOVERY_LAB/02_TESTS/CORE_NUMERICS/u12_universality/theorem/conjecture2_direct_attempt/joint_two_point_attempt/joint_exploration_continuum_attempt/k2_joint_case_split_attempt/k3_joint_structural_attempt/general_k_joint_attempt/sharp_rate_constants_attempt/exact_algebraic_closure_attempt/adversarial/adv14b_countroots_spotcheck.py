import sympy as sp, pickle, time
n = sp.Symbol('n')
with open('k4_S_upper.pkl','rb') as f:
    S = pickle.load(f)
content, facs = sp.factor_list(S, n)
B = max(facs, key=lambda fm: sp.Poly(fm[0],n).degree())[0]
Bpoly = sp.Poly(B, n)
t0=time.time()
c = Bpoly.count_roots(inf=6)
print(f"count_roots(inf=6): {time.time()-t0:.2f}s, count={c}")
