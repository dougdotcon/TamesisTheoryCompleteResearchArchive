"""
Independent re-derivation of script 08's order-2 vs order-6 Taylor/cumulant
check, for gamma=0.5 only (one representative value, per the scrutiny list
item (f)), built FRESH (own moment recursion, own summation loop, own
Richardson extrapolation), not reading the target's moment_data.pkl or
Ex_powers.pkl.

Also independently re-checks the target's own interpretive claim in
ATTEMPT.md Sec.5: "the four extra exact orders shift the extrapolated
limit by only 4e-5-8e-5 -- comparable to, or smaller than, the residual
gap already present at order 2" -- by directly comparing the *shift*
|order6-order2| against the *order-2 residual* |order2-E_heuristic|
at each gamma, using the SAME numbers the target's own log reports (a
pure arithmetic check, not a re-derivation) to see if that specific
characterization is accurate.
"""
import time
import mpmath as mp
import sympy as sp
from sympy import symbols, log, exp, series, expand, factorial, Poly, binomial

mp.mp.dps = 50

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')
t = symbols('t')

print("="*70)
print("Fresh, independent re-derivation of x(D) and D's moments up to order 18")
print("="*70)

m_sym = symbols('m', integer=True, nonnegative=True)
i_sym = symbols('i', integer=True, positive=True)
tau_m = expand(sp.summation(((k - i_sym)/n)**2, (i_sym, 1, m_sym)))
M_sym = g*k + D
tau_M = expand(tau_m.subs(m_sym, M_sym))
delta_D = D*(2*k*(1-g) - D - 1)/(2*n)
x_D = expand(delta_D + tau_M/2)

# own moment recursion (cumulant-based, but written completely fresh,
# independent implementation from script02's)
MAXORD = 18
cgf1 = log(1 - g + g*exp(t))
ser = series(cgf1, t, 0, MAXORD+1).removeO()
poly = Poly(ser, t)
kt = {0: sp.Integer(0)}
for j in range(1, MAXORD+1):
    kt[j] = expand(factorial(j)*poly.coeff_monomial(t**j))
kD = {0: sp.Integer(0), 1: sp.Integer(0)}
for j in range(2, MAXORD+1):
    kD[j] = k*kt[j]
mu = {0: sp.Integer(1)}
for nn in range(1, MAXORD+1):
    s = sp.Integer(0)
    for mm in range(1, nn+1):
        s += binomial(nn-1, mm-1)*kD[mm]*mu[nn-mm]
    mu[nn] = expand(s)

print("mu_4 (fresh) =", mu[4])
print("Consistency vs cited classical mu_4:",
      sp.simplify(mu[4] - k*g*(1-g)*(1+3*(k-2)*g*(1-g))))

def E_of_xpow(order):
    if order == 0:
        return sp.Integer(1)
    expr = expand(x_D**order)
    poly_ = Poly(expr, D)
    total = sp.Integer(0)
    for j in range(0, 3*order+1):
        c = poly_.coeff_monomial(D**j) if j > 0 else poly_.coeff_monomial(1)
        total += c*mu[j]
    return expand(total)

print("\nComputing E[x(D)^j], j=0..6 (fresh, independent implementation)...")
t0 = time.time()
Ex = {j: E_of_xpow(j) for j in range(7)}
print(f"  done in {time.time()-t0:.1f}s")

def T_minus_1(J):
    total = sp.Integer(0)
    for j in range(1, J+1):
        total += sp.Rational((-1)**j,1)/factorial(j)*Ex[j]
    return expand(total)

T2m1 = T_minus_1(2)
T6m1 = T_minus_1(6)
T2_f = sp.lambdify((k,n,g), T2m1, modules='mpmath')
T6_f = sp.lambdify((k,n,g), T6m1, modules='mpmath')

def s_of_k(k_val, n_val, gamma):
    beta = gamma*(2-gamma)/2
    return beta*k_val**2/n_val - gamma*k_val/(2*n_val)

def E_n_trunc(n_val, gamma, f):
    total = mp.mpf(0)
    for k_val in range(1, int(n_val)+1):
        w = mp.e**(-s_of_k(k_val, n_val, gamma))
        total += w*f(k_val, n_val, gamma)
    return total

def E_heuristic(gamma):
    return (-3*gamma**2+7*gamma-6)/(6*(gamma-2)**2)

gamma = mp.mpf('0.5')
print(f"\n--- gamma={gamma}: independent re-run of E_n^(2), E_n^(6) at n=4096,16384 ---")
rows = []
for n_val in [4096, 16384]:
    E2 = E_n_trunc(n_val, gamma, T2_f)
    E6 = E_n_trunc(n_val, gamma, T6_f)
    rows.append((n_val, E2, E6))
    print(f"  n={n_val}: E_n^(2)={mp.nstr(E2,10)}  E_n^(6)={mp.nstr(E6,10)}")

(n1,E2_1,E6_1),(n2,E2_2,E6_2) = rows
s1, s2 = mp.mpf(1)/mp.sqrt(n1), mp.mpf(1)/mp.sqrt(n2)
def richardson(A,B): return (B*s1 - A*s2)/(s1-s2)
x2 = richardson(E2_1,E2_2); x6 = richardson(E6_1,E6_2)
Eh = E_heuristic(gamma)
print(f"  Richardson extrap: order-2={mp.nstr(x2,10)}  order-6={mp.nstr(x6,10)}  E_heuristic={mp.nstr(Eh,10)}")
print(f"  |order2-Eh|={mp.nstr(abs(x2-Eh),6)}  |order6-Eh|={mp.nstr(abs(x6-Eh),6)}  |order6-order2|={mp.nstr(abs(x6-x2),6)}")

print("\n" + "="*70)
print("Checking the target's own headline interpretive claim (Sec.5):")
print('"the four extra exact orders shift the extrapolated limit by only')
print(' 4e-5-8e-5 -- comparable to, or smaller than, the residual gap')
print(' already present at order 2" -- verified via pure arithmetic on the')
print(" target's OWN reported numbers (08_higher_order_taylor_check.log):")
print("="*70)
target_rows = {
    '0.3': dict(order2_extrap=mp.mpf('-0.2404203489'), order6_extrap=mp.mpf('-0.2403362793'), Eh=mp.mpf('-0.2404844291')),
    '0.5': dict(order2_extrap=mp.mpf('-0.2407160987'), order6_extrap=mp.mpf('-0.2406693901'), Eh=mp.mpf('-0.2407407407')),
    '0.7': dict(order2_extrap=mp.mpf('-0.2534418507'), order6_extrap=mp.mpf('-0.2534057236'), Eh=mp.mpf('-0.2534516765')),
}
for gm, d in target_rows.items():
    r2 = abs(d['order2_extrap']-d['Eh'])
    r6 = abs(d['order6_extrap']-d['Eh'])
    shift = abs(d['order6_extrap']-d['order2_extrap'])
    print(f"  gamma={gm}: order-2 residual |o2-Eh|={mp.nstr(r2,4)}   "
          f"shift |o6-o2|={mp.nstr(shift,4)}   ratio shift/order2-residual={mp.nstr(shift/r2,4)}"
          f"   {'SHIFT EXCEEDS order-2 residual' if shift>r2 else 'shift <= order-2 residual'}")
