#!/usr/bin/env python3
"""
Script 08 -- Push the Taylor/cumulant expansion of E_M[e^{-x(D)}] to
ORDER 6 in x(D) (using script 02's exact D-moments, up to degree 18,
i.e. exactly what x(D)^6 needs) -- FOUR orders beyond Estagio 26 Sec.4's
own order-2 heuristic truncation (which kept only -E[delta], -tau(gamma
k)/2, +E[delta^2]/2, i.e. the order-1-and-2-in-x terms).

Purpose: Estagio 26 Sec.4 argued, via LEADING-ORDER ASYMPTOTIC COUNTING
(Theta notation, not exact computation) that the cubic-log term
kappa(M)/3, the tau(M)-tau(gamma*k) fluctuation, and various cross terms
are all "negligible" at the order that matters (n^{-1/2} relative to
G_n). This script does NOT just count orders -- it computes the EXACT
(to numerical precision) sum
   E_n^{(J)}(n,gamma) := sum_{k=1}^{K} e^{-s(k)} * [T_J(k,n,gamma) - 1]
for the TRUNCATED Taylor series T_J(k,n,gamma) := sum_{j=0}^J
(-1)^j E[x(D)^j]/j!  at J=2 (matching Estagio 26's own order) and J=6
(this front's order, going as far as the exact D-moments already
computed allow), and checks whether the RICHARDSON-EXTRAPOLATED n->infty
limit of E_n^{(6)} still matches E_heuristic(gamma) as closely as
E_n^{(2)} does -- i.e. whether including FOUR more exact orders changes
the numerically-extracted limit at all.

If J=2 and J=6 extrapolate to the SAME limit (to within numerical
precision), this is meaningful independent evidence -- via exact
computation, not order-counting -- that Estagio 26's truncation was not
accidentally dropping a genuine surviving contribution. If they diverge,
that is an important, currently-unknown finding this script is designed
to surface honestly either way.
"""
import pickle
import time
import mpmath as mp
import sympy as sp
from sympy import symbols, Poly, expand, factorial

mp.mp.dps = 50

LOG = []
def log_(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 08 -- order-6 vs order-2 Taylor truncation of E_M[e^{-x(D)}]")
log_("="*78)

with open('moment_data.pkl', 'rb') as f:
    data = pickle.load(f)
g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')
c0 = sp.sympify(data['c0']); c1 = sp.sympify(data['c1'])
c2 = sp.sympify(data['c2']); c3 = sp.sympify(data['c3'])
mu = {int(kk): sp.sympify(v) for kk, v in data['mu'].items()}
x_D = c0 + c1*D + c2*D**2 + c3*D**3

def E_of_xpow(order):
    """Exact E[x(D)^order] via moment substitution D^j -> mu[j]."""
    expr = expand(x_D**order) if order > 0 else sp.Integer(1)
    if order == 0:
        return sp.Integer(1)
    poly = Poly(expr, D)
    total = sp.Integer(0)
    maxdeg = 3*order
    for j in range(0, maxdeg+1):
        coeff = poly.coeff_monomial(D**j) if j > 0 else poly.coeff_monomial(1)
        total += coeff * mu[j]
    return expand(total)

log_("\nComputing E[x(D)^j] for j=0..6 exactly (moment substitution)...")
t0 = time.time()
Ex = {}
for j in range(0, 7):
    tj0 = time.time()
    Ex[j] = E_of_xpow(j)
    log_(f"  j={j}: done in {time.time()-tj0:.1f}s, "
         f"{len(Ex[j].as_ordered_terms()) if Ex[j]!=0 else 0} terms")
log_(f"Total: {time.time()-t0:.1f}s")

with open('Ex_powers.pkl', 'wb') as f:
    pickle.dump({str(jj): sp.srepr(v) for jj, v in Ex.items()}, f)

# T_J - 1 = sum_{j=1}^J (-1)^j E[x^j]/j!
def T_minus_1(J):
    total = sp.Integer(0)
    for j in range(1, J+1):
        total += sp.Rational((-1)**j, 1)/factorial(j) * Ex[j]
    return expand(total)

log_("\nBuilding T_2-1 and T_6-1 (exact rational functions of k,n,gamma)...")
T2m1 = T_minus_1(2)
T6m1 = T_minus_1(6)

T2_f = sp.lambdify((k, n, g), T2m1, modules='mpmath')
T6_f = sp.lambdify((k, n, g), T6m1, modules='mpmath')

def s_of_k(k_val, n_val, gamma):
    beta = gamma*(2-gamma)/2
    return beta*k_val**2/n_val - gamma*k_val/(2*n_val)

def E_n_truncated(n_val, gamma, order_func, Kmax=None):
    if Kmax is None:
        Kmax = n_val
    total = mp.mpf(0)
    for k_val in range(1, int(Kmax)+1):
        w = mp.e**(-s_of_k(k_val, n_val, gamma))
        val = order_func(k_val, n_val, gamma)
        total += w*val
    return total

# E_heuristic(gamma), quoted/cited from Estagio 26 Sec.4 (already
# independently symbolically re-confirmed via Lemma E in that document;
# re-quoted here as a comparison TARGET, not re-derived from scratch
# again in this script -- that re-derivation already lives in the cited
# ancestor document and is not this front's job to repeat).
def E_heuristic(gamma):
    return (-3*gamma**2 + 7*gamma - 6)/(6*(gamma-2)**2)

GAMMAS = [mp.mpf(x) for x in ['0.3', '0.5', '0.7']]
N_LIST = [2**e for e in [10, 12, 14]]  # kept modest: exact sum over ALL k up to n is O(n) calls,
                                        # each a moderate rational-function eval -- feasible up to
                                        # a few thousand/tens of thousands without truncation tricks

log_("\n--- Comparing order-2 (Estagio 26's own order) vs order-6 (this front) ---")
log_("    Richardson-extrapolated limit (2-point, model x_n = x + c/sqrt(n)) vs E_heuristic(gamma)")

for gamma in GAMMAS:
    Eh = E_heuristic(gamma)
    rows = []
    for n_val in N_LIST:
        E2 = E_n_truncated(n_val, gamma, T2_f)
        E6 = E_n_truncated(n_val, gamma, T6_f)
        rows.append((n_val, E2, E6))
        log_(f"  gamma={float(gamma):.1f} n={n_val:>6}: E_n^(2)={mp.nstr(E2,10)}  "
             f"E_n^(6)={mp.nstr(E6,10)}")
    # 2-point Richardson extrapolation using the LAST TWO n values (x_n = x + c/sqrt(n))
    (n1,E2_1,E6_1),(n2,E2_2,E6_2) = rows[-2], rows[-1]
    s1, s2 = mp.mpf(1)/mp.sqrt(n1), mp.mpf(1)/mp.sqrt(n2)
    # solve x + c*s = E(s) for the two points: x = (E2_2*s1 - E2_1*s2)/(s1-s2)... use standard formula
    def richardson(E1, E2):
        return (E2*s1 - E1*s2)/(s1 - s2)
    x2_extrap = richardson(E2_1, E2_2)
    x6_extrap = richardson(E6_1, E6_2)
    log_(f"    Richardson extrap (n={n1},{n2}): order-2 -> {mp.nstr(x2_extrap,10)}  "
         f"order-6 -> {mp.nstr(x6_extrap,10)}   E_heuristic={mp.nstr(Eh,10)}")
    log_(f"    |order-2 - E_heuristic| = {mp.nstr(abs(x2_extrap-Eh),6)}   "
         f"|order-6 - E_heuristic| = {mp.nstr(abs(x6_extrap-Eh),6)}")
    log_(f"    |order-6 - order-2|    = {mp.nstr(abs(x6_extrap-x2_extrap),6)}")
    log_("")

log_("Interpretation: if |order-6 - order-2| is itself small (comparable to or")
log_("smaller than the residual |order-2 - E_heuristic|), the four extra exact")
log_("orders included here do not materially shift the extrapolated limit --")
log_("consistent with (not a proof of) Estagio 26's truncation being adequate")
log_("at the order that determines E(gamma). A LARGE |order-6-order-2| would be")
log_("an important red flag this script is designed to catch honestly.")

with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
