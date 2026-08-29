"""
Independent K=4 upper-bound resultant elimination (target Sec 4.3).
Loads Nx, Dn from pickle (adv5). Builds F1, F2, R(n,m), then S(n) by
eliminating m against M4's minimal quartic. Times each step. Then
factor_list(S,n) to isolate genuine content, matching target's claimed
n^220 * (6n^2-11n+6)^4 * B(n), B irreducible degree 216, largest real
root ~3.2244.
"""
import sympy as sp
import time, pickle

n, x, m, t = sp.symbols('n x m t')

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_Nx_Dn.pkl','rb') as f:
    d = pickle.load(f)
Nx, Dn = d['Nx'], d['Dn']

M4_minpoly = 35831808*t**4 - 49852544*t**3 - 220711113*t**2 + 556322688*t - 274710528

F1 = sp.expand(sp.diff(Nx, x))
print("deg_x F1:", sp.Poly(F1,x).degree())
F2 = sp.expand(m*Dn - n*Nx)
print("deg_x F2:", sp.Poly(F2,x).degree())

t0 = time.time()
R = sp.resultant(F1, F2, x)
t1 = time.time()
print(f"R(n,m) computed in {t1-t0:.2f}s")
Rpoly_nm = sp.Poly(R, n, m)
print("R degree in n:", sp.degree(R, n), " degree in m:", sp.degree(R, m))

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_R_upper.pkl','wb') as f:
    pickle.dump(R, f)

t0 = time.time()
S = sp.resultant(R, M4_minpoly.subs(t,m), m)
t1 = time.time()
print(f"S(n) computed in {t1-t0:.2f}s, degree in n: {sp.degree(S,n)}")

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_S_upper.pkl','wb') as f:
    pickle.dump(S, f)

t0 = time.time()
content, facs = sp.factor_list(S, n)
t1 = time.time()
print(f"factor_list(S,n) in {t1-t0:.2f}s; content={content}")
for fac, mult in facs:
    dpoly = sp.Poly(fac, n)
    print(f"  factor deg={dpoly.degree()} mult={mult}: {str(fac)[:120]}")
