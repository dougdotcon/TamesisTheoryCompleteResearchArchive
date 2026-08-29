"""
Independent, from-scratch reconstruction of the K=3 resultant-elimination
argument (target ATTEMPT.md Sec 3.3-3.4), WITHOUT reading the target's
own k3_exact_closure.py script.

Steps:
 1. Build N(n,x), D(n) for Delta3_n(x) (reduced form, own convention).
 2. F1 := d/dx N(n,x); F2 := m*D(n) - n*N(n,x).
 3. R(n,m) := resultant_x(F1, F2).
 4. Eliminate m against M_3's minimal quartic (independently derived, adv2).
 5. real_roots of resulting S(n); report largest.
 6. Boundary h(n,1) closed form + its threshold vs M_3.
 7. "Touches-zero" lower-bound locus: resultant_x(dN/dx, N) -> real roots,
    largest root claimed ~5.968.
 8. Direct exact check at small integer n (n=5,6,...) to build confidence.
"""
import sympy as sp
import time

n, k, x, m, t = sp.symbols('n k x m t')

# --- Rebuild D3 exactly as before (own transcription, independent) ---
D3_num = k*(k+1)*(k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2 + (3*n**2 - 11*n - 2)*k
                  + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
D3_den = n**4*(n-1)*(n-2)
F3n = D3_num / D3_den
F3_cont = 1 - (1-x**2)**3

Delta3 = sp.cancel(F3n.subs(k, n*x) - F3_cont)
Nx, Dn = sp.fraction(Delta3)
Nx = sp.expand(Nx)
Dn = sp.factor(Dn)
print("Reduced D(n) =", Dn)
print("N(n,x) degree in n:", sp.Poly(Nx, n).degree())
print("N(n,x) degree in x:", sp.Poly(Nx, x).degree())

# h(n,x) = n*Nx/Dn  (this IS n*Delta3)
# We want interior critical points: dN/dx = 0 (since d/dx of h(n,x) = n/Dn * dNx/dx,
# and n/Dn != 0 for n>2, critical points of h in x coincide with critical points of Nx in x)

F1 = sp.expand(sp.diff(Nx, x))
print("\ndeg_x F1:", sp.Poly(F1, x).degree())

# h(n,x) = m  <=>  n*Nx = m*Dn  <=>  F2 := m*Dn - n*Nx = 0
F2 = sp.expand(m*Dn - n*Nx)
print("deg_x F2:", sp.Poly(F2, x).degree())

t0 = time.time()
R = sp.resultant(F1, F2, x)
R = sp.factor(R)
t1 = time.time()
print(f"\nR(n,m) computed in {t1-t0:.2f}s")
print("R(n,m) factor form (first 300 chars):", str(R)[:300], "...")

# M_3's minimal quartic (independently derived earlier, adv2):
M3_minpoly = 15552*t**4 - 3355*t**3 - 42192*t**2 + 181440*t - 110592
print("\nM3 minimal quartic:", M3_minpoly)

# Eliminate m: resultant_m(R(n,m), M3_minpoly(m)) -> S(n)
t0 = time.time()
S = sp.resultant(R, M3_minpoly.subs(t, m), m)
t1 = time.time()
print(f"\nS(n) computed in {t1-t0:.2f}s, degree in n:", sp.Poly(S, n).degree())

t0 = time.time()
Spoly = sp.Poly(S, n)
Sfactors = sp.factor_list(S, n)
t1 = time.time()
print(f"factor_list(S,n) done in {t1-t0:.2f}s")
print("Content:", Sfactors[0])
for fac, mult in Sfactors[1]:
    d = sp.Poly(fac, n).degree()
    print(f"  factor deg={d} mult={mult}: {str(fac)[:150]}")

t0 = time.time()
real_roots_S = Spoly.real_roots()
t1 = time.time()
print(f"\nreal_roots(S) direct: {len(real_roots_S)} roots in {t1-t0:.2f}s")
real_roots_S_num = sorted([sp.N(r, 25) for r in real_roots_S])
print("largest real root of S(n):", real_roots_S_num[-1])
print("all real roots (numeric):")
for r in real_roots_S_num:
    print("  ", r)

print("\nDONE Step 1 (upper-bound interior elimination, K=3).")
