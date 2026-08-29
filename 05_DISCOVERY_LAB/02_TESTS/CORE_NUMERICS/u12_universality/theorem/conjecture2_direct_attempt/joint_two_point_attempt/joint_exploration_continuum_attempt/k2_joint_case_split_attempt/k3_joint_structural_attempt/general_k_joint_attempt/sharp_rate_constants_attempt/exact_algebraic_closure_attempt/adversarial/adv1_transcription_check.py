"""
Independent from-scratch reconstruction of Delta_n(x) = F_n^{(K)}(x) - F_K(x)
for K=3,4 directly from THEOREM.md's own D3/D4 formulas (Estagios 40, 43),
transcribed verbatim by me from THEOREM.md (read in full, lines 6028-6029 for D3,
lines 6370-6373 for D4), WITHOUT consulting the target's own scripts/ATTEMPT.md.

Goal: compute n*Delta_n(x), take n->infinity limit, and confirm the claimed
leading coefficients g_3(x), g_4(x).
"""
import sympy as sp

n, k, x = sp.symbols('n k x', positive=True)

# --- D3, Estagio 40, THEOREM.md lines 6027-6029 ---
# P(M_n^(3) <= k/n) = k(k+1)[k^4-4k^3-(3n^2-9n-5)k^2+(3n^2-11n-2)k+(3n^4-12n^3+12n^2+2n)] / [n^4(n-1)(n-2)]
D3_num = k*(k+1)*(k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2 + (3*n**2 - 11*n - 2)*k
                  + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
D3_den = n**4*(n-1)*(n-2)
F3n = D3_num / D3_den

# --- D4, Estagio 43, THEOREM.md lines 6370-6373 ---
# P(M_n^(4) <= k/n) = k(k+1) Q(n,k) / [n^5(n-1)(n-2)(n-3)]
# Q(n,k) = -k^6+9k^5+(4n^2-18n-31)k^4+(-16n^2+80n+51)k^3
#          +(-6n^4+42n^3-55n^2-120n-40)k^2+(6n^4-50n^3+97n^2+70n+12)k
#          +4n^6-30n^5+74n^4-52n^3-30n^2-12n
Q = (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4 + (-16*n**2 + 80*n + 51)*k**3
     + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
     + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
     + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)
D4_num = k*(k+1)*Q
D4_den = n**5*(n-1)*(n-2)*(n-3)
F4n = D4_num / D4_den

F3_cont = 1 - (1-x**2)**3
F4_cont = 1 - (1-x**2)**4

print("="*70)
print("STEP 1: substitute k = n*x, form Delta_n(x) = F_n^(K)(x) - F_K(x)")
print("="*70)

Delta3 = F3n.subs(k, n*x) - F3_cont
Delta3 = sp.cancel(Delta3)
print("\nDelta3_n(x) [cancelled] numerator/denominator:")
num3, den3 = sp.fraction(Delta3)
num3 = sp.expand(num3)
den3 = sp.factor(den3)
print("den3 =", den3)

Delta4 = F4n.subs(k, n*x) - F4_cont
Delta4 = sp.cancel(Delta4)
num4, den4 = sp.fraction(Delta4)
num4 = sp.expand(num4)
den4 = sp.factor(den4)
print("den4 =", den4)

print("\n" + "="*70)
print("STEP 2: n*Delta_n(x), then n -> infinity limit (should give g_3, g_4)")
print("="*70)

nDelta3 = sp.together(n*Delta3)
g3_limit = sp.limit(nDelta3, n, sp.oo)
g3_limit = sp.expand(g3_limit)
print("\nlim_{n->oo} n*Delta3_n(x) =", g3_limit)

nDelta4 = sp.together(n*Delta4)
g4_limit = sp.limit(nDelta4, n, sp.oo)
g4_limit = sp.expand(g4_limit)
print("\nlim_{n->oo} n*Delta4_n(x) =", g4_limit)

print("\n" + "="*70)
print("STEP 3: compare against the target's/predecessor's claimed g_3, g_4")
print("="*70)

g3_claimed = 3*x*(x-1)**2*(x+1)*(x**2+1)
g3_claimed_expanded = sp.expand(g3_claimed)
print("\ng3_claimed (factored) expanded =", g3_claimed_expanded)
print("g3_limit - g3_claimed_expanded =", sp.simplify(g3_limit - g3_claimed_expanded))

g4_claimed = -6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x
print("\ng4_claimed =", g4_claimed)
print("g4_limit - g4_claimed =", sp.simplify(g4_limit - g4_claimed))

print("\n" + "="*70)
print("STEP 4: sanity - degree check consistent with 1/n leading order")
print("="*70)
# also directly extract via series in 1/n to double check limit method
u = sp.symbols('u', positive=True)  # u = 1/n
nDelta3_series = sp.series(nDelta3.subs(n, 1/u), u, 0, 2).removeO()
print("\nSeries-based g3 (coeff of u^0 term in n*Delta3 with n=1/u, u->0):")
print(sp.expand(nDelta3_series.subs(u,0)) if nDelta3_series.has(u) else nDelta3_series)

print("\nDONE.")
