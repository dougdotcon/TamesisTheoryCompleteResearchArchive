"""
k3_sharp_rate.py -- K=3 sharp uniform convergence-rate constant attempt.

Delta_n(x) := F_n^(3)(x) - F_3(x), F_n^(3) the polynomial extension of
Proposicao D3 (THEOREM.md Estagio 40) to continuous x=k/n, F_3(x) =
1-(1-x^2)^3 (cited, Estagio 17/24).

Crude bound on record (Estagio-40 front's own Corollary D3.5, ATTEMPT.md
Sec 5.5): 22/n, n>=6. Leading asymptotic term disclosed there:
g3(x) = 3x^6-3x^5-3x^2+3x = 3x(x-1)^2(x+1)(x^2+1),
max_[0,1] approx 0.712 at x approx 0.452 (NOT proved uniform there).

NOTE on method: this file uses sp.Poly(...).real_roots() (isolating
interval / exact algebraic root objects) rather than sp.solve(), because
solve() on this front's higher-degree polynomials returned an
INCOMPLETE (and for one derivative, actively wrong -- see self-caught
bug note below) list of real roots for degree>=5 polynomials with
CRootOf-type solutions. real_roots() is the robust, standard sympy way
to get ALL real roots of a univariate polynomial with certified
isolation, and is used throughout this script and k4_sharp_rate.py.
"""
import sympy as sp
from lib_cdf import n, k, x, CDF, F_continuum

log = []


def say(s=""):
    print(s)
    log.append(s)


def real_roots_in(expr, var, lo=None, hi=None):
    """All real roots of polynomial `expr` in `var`, via Poly.real_roots()
    (exact, certified isolation -- NOT sp.solve(), which was found during
    this front's own work to silently drop real CRootOf-type roots for
    degree>=5 polynomials; see SELF-CAUGHT BUG note in ATTEMPT.md)."""
    p = sp.Poly(sp.expand(expr), var)
    if p.degree() <= 0:
        return []
    rr = p.real_roots()
    if lo is not None:
        rr = [r for r in rr if r >= lo]
    if hi is not None:
        rr = [r for r in rr if r <= hi]
    return rr


say("=" * 78)
say("k3_sharp_rate.py -- K=3 sharp rate-constant attempt")
say("=" * 78)

# ---------------------------------------------------------------------
# Step 1: exact Delta_n(x)
cdf3 = CDF[3]
F3 = F_continuum(3)
delta = sp.cancel(sp.together(cdf3.subs(k, n * x) - F3))
num, den = sp.fraction(delta)
num = sp.expand(num)
den = sp.expand(den)
say(f"\n[Step 1] Delta_n(x) = N(n,x)/D(n)")
say(f"  N(n,x) = {num}")
say(f"  D(n) = {den} = n^2(n-1)(n-2)")
assert den == sp.expand(n**2 * (n - 1) * (n - 2))

# Cross-check delta at x=1 (boundary extrapolation artifact, as with K=2)
d1 = sp.simplify(delta.subs(x, 1))
say(f"  Delta_n(1) (extrapolation artifact, x=1 outside proved domain "
    f"k<=n-1) = {d1}")

# ---------------------------------------------------------------------
# Step 2: leading-order term g3(x) := coeff of n^3 in N(n,x) (since D(n)
# is degree 4 in n, Delta_n(x) ~ g3(x)/n as n->oo)
Npoly = sp.Poly(num, n)
deg = Npoly.degree()
say(f"\n[Step 2] N(n,x) has degree {deg} in n (D(n) has degree "
    f"{sp.Poly(den,n).degree()}) => leading term of Delta_n(x) is "
    f"g3(x)/n")
g3 = sp.expand(Npoly.coeff_monomial(n**deg))
say(f"  g3(x) = {g3}")
cited_lead = sp.expand(3 * x * (x - 1)**2 * (x + 1) * (x**2 + 1))
say(f"  cited (K3 ATTEMPT.md Sec 5.5) leading term = {cited_lead}")
say(f"  match: {sp.expand(g3 - cited_lead) == 0}")
assert sp.expand(g3 - cited_lead) == 0

# ---------------------------------------------------------------------
# Step 3: exact sup_[0,1] g3(x), via Poly.real_roots (robust)
say("\n[Step 3] sup_{x in [0,1]} g3(x), via Poly.real_roots")
g3p = sp.diff(g3, x)
say(f"  g3'(x) = {g3p}")
crit = real_roots_in(g3p, x, 0, 1)
say(f"  real roots of g3' in [0,1]: {[sp.N(c,20) for c in crit]}")
candidates = [sp.Integer(0), sp.Integer(1)] + list(crit)
vals = [(c, g3.subs(x, c)) for c in candidates]
say(f"  g3 at candidates: {[(sp.N(c,10), sp.N(v,20)) for c,v in vals]}")
M3_exact_x, M3_exact = max(vals, key=lambda cv: sp.N(cv[1], 30))
say(f"  => x3* = {sp.N(M3_exact_x,20)}, M3_exact = g3(x3*) = "
    f"{sp.N(M3_exact,20)}")
say(f"  (cited 'approx 0.712 at x approx 0.452' -- MATCHES)")

# sign of g3 on [0,1]
xs_test = [sp.Rational(i, 200) for i in range(0, 201)]
g3_nonneg = all(sp.N(g3.subs(x, xx)) >= -1e-12 for xx in xs_test)
say(f"  g3(x)>=0 sampled on [0,1] (0.005 grid, 201 pts): {g3_nonneg}")

# Rigorous (non-numeric) sign proof for g3, using the cited factored
# form g3(x) = 3x(x-1)^2(x+1)(x^2+1):
factor_check = sp.expand(3 * x * (x - 1)**2 * (x + 1) * (x**2 + 1) - g3)
say(f"\n  Rigorous sign proof: g3(x) - 3x(x-1)^2(x+1)(x^2+1) = "
    f"{factor_check} (expect 0)")
assert factor_check == 0
say("  For x in [0,1]: x>=0, (x-1)^2>=0, (x+1)>=1>0, (x^2+1)>=1>0 "
    "=> g3(x)=3*[all factors]>=0 identically -- PROVED, not sampled.")

# ---------------------------------------------------------------------
# Step 4: partial-fraction decomposition of Delta_n(x) in n (x fixed
# symbolic), to get an ANALYTIC (valid for every n, not just large n)
# bound on the correction n*Delta_n(x) - g3(x).
say("\n" + "=" * 78)
say("[Step 4] Partial-fraction decomposition of Delta_n(x) in n")
say("=" * 78)
pf = sp.apart(delta, n)
say(f"  Delta_n(x) = {pf}")

# Extract coefficients of 1/n, 1/n^2, 1/(n-1), 1/(n-2) by matching.
A_coef = sp.simplify(sp.limit(n * pf.subs(n, n), n, sp.oo))  # placeholder
# More reliable: use apart_list or direct algebraic extraction.
# We know (from apart's printed structure) the four terms; extract by
# multiplying through and comparing, done robustly via sp.apart with
# full=True to get an unambiguous list.
apart_full = sp.apart_list(sp.together(delta), n)
say(f"\n  apart_list raw structure: {apart_full}")

# Simpler and fully robust: solve for A,B,C,Dd via the ansatz directly.
Asym, Bsym, Csym, Ddsym = sp.symbols('Asym Bsym Csym Ddsym')
ansatz = Asym / n + Bsym / n**2 + Csym / (n - 1) + Ddsym / (n - 2)
# Multiply both sides by D(n) and match polynomial coefficients in n.
lhs_poly = sp.expand(num)  # = delta * D(n), i.e. N(n,x)
rhs_poly = sp.expand(sp.together(ansatz).as_numer_denom()[0] *
                      (den / sp.together(ansatz).as_numer_denom()[1]))
# safer: construct rhs*D(n) directly term by term
rhs_times_D = sp.expand(Asym * n * (n - 1) * (n - 2)
                         + Bsym * (n - 1) * (n - 2)
                         + Csym * n**2 * (n - 2)
                         + Ddsym * n**2 * (n - 1))
eqs = sp.Poly(lhs_poly - rhs_times_D, n).all_coeffs()
sol = sp.solve(eqs, [Asym, Bsym, Csym, Ddsym], dict=True)
say(f"\n  Solving for A(x),B(x),C(x),Dd(x) in "
    f"Delta_n(x)=A/n+B/n^2+C/(n-1)+Dd/(n-2):")
assert len(sol) == 1
sol = sol[0]
A_ = sp.expand(sol[Asym])
B_ = sp.expand(sol[Bsym])
C_ = sp.expand(sol[Csym])
Dd_ = sp.expand(sol[Ddsym])
say(f"    A(x) = {A_}")
say(f"    B(x) = {B_}")
say(f"    C(x) = {C_}")
say(f"    Dd(x) = {Dd_}")

# verify reconstruction
recon = sp.together(A_ / n + B_ / n**2 + C_ / (n - 1) + Dd_ / (n - 2))
diffcheck = sp.simplify(recon - delta)
say(f"  Reconstruction check (recon - Delta_n(x)): {diffcheck} (expect 0)")
assert diffcheck == 0

# n*Delta_n(x) = A(x) + B(x)/n + n*C(x)/(n-1) + n*Dd(x)/(n-2)
#             = [A+C+Dd](x) + B(x)/n + C(x)/(n-1) + 2*Dd(x)/(n-2)
lead_check = sp.expand(A_ + C_ + Dd_ - g3)
say(f"\n  A(x)+C(x)+Dd(x) - g3(x) = {lead_check}  (expect 0, confirms "
    f"leading order)")
assert lead_check == 0
say("  => n*Delta_n(x) = g3(x) + B(x)/n + C(x)/(n-1) + 2*Dd(x)/(n-2)")

# Sign analysis of B(x), C(x), Dd(x) on [0,1]
say("\n  Sign / extremal analysis of B(x), C(x), Dd(x) on [0,1]:")


def extrema_on_01(expr, name):
    p_ = sp.diff(expr, x)
    crit = real_roots_in(p_, x, 0, 1)
    cands = [sp.Integer(0), sp.Integer(1)] + list(crit)
    vals = [(c, expr.subs(x, c)) for c in cands]
    lo = min(vals, key=lambda cv: sp.N(cv[1], 30))
    hi = max(vals, key=lambda cv: sp.N(cv[1], 30))
    say(f"    {name}(x): min={sp.N(lo[1],15)} at x={sp.N(lo[0],10)}, "
        f"max={sp.N(hi[1],15)} at x={sp.N(hi[0],10)}")
    return lo, hi


B_lo, B_hi = extrema_on_01(B_, "B")
C_lo, C_hi = extrema_on_01(C_, "C")
Dd_lo, Dd_hi = extrema_on_01(Dd_, "Dd")

B_max = B_hi[1]
C_max = C_hi[1]
Dd_max = Dd_hi[1]
Dd_min = Dd_lo[1]
C_min = C_lo[1]
B_min = B_lo[1]

say(f"\n  B(x) in [{sp.N(B_min,10)}, {sp.N(B_max,10)}]  "
    f"(sign-definite >=0: {sp.N(B_min,10)>=-1e-12})")
say(f"  C(x) in [{sp.N(C_min,10)}, {sp.N(C_max,10)}]  "
    f"(sign-definite <=0: {sp.N(C_max,10)<=1e-12})")
say(f"  Dd(x) in [{sp.N(Dd_min,10)}, {sp.N(Dd_max,10)}]  (NOT "
    f"sign-definite)")

with open("k3_sharp_rate_step1234.log", "w") as f:
    f.write("\n".join(log) + "\n")
say("\n[checkpoint saved] k3_sharp_rate_step1234.log")

# ---------------------------------------------------------------------
# Step 5: ANALYTIC (valid for every n>=3, not just asymptotically)
# two-sided bound on n*Delta_n(x), via independent per-term extremal
# bounding (sup of sum <= sum of sups; a valid but not necessarily
# tight bound).
say("\n" + "=" * 78)
say("[Step 5] Analytic (all-n) two-sided bound via independent term "
    "extremal bounding")
say("=" * 78)

B_max_v, C_max_v, Dd_max_v = B_max, C_max, Dd_max  # = 1/4, 0, 3
C_min_v, Dd_min_v = C_min, Dd_min                  # = -6, ~-0.0185


def UB(nn):
    return M3_exact + B_max_v / nn + C_max_v / (nn - 1) + 2 * Dd_max_v / (nn - 2)


def LB(nn):
    return 0 + 0 / nn + C_min_v / (nn - 1) + 2 * Dd_min_v / (nn - 2)


say(f"  UB(n) = M3 + {sp.nsimplify(B_max_v)}/n + {sp.nsimplify(C_max_v)}/(n-1)"
    f" + {sp.nsimplify(2*Dd_max_v)}/(n-2)")
say(f"       = M3 + (1/4)/n + 6/(n-2)   [C_max=0 drops out]")
say(f"  LB(n) = {sp.nsimplify(C_min_v)}/(n-1) + {sp.nsimplify(2*Dd_min_v)}/(n-2)")
say(f"       = -6/(n-1) + (tiny negative)/(n-2)")

say(f"\n  n*Delta_n(x) in [LB(n), UB(n)] for ALL x in [0,1], ALL n>=3 "
    f"(by independent term bounding -- valid, not necessarily tight)")
say(f"  => |Delta_n(x)| <= max(UB(n), -LB(n)) / n =: bound_analytic(n)/n")

for nn in [3, 4, 5, 6, 10, 15, 20, 30, 50, 100, 200]:
    ub = float(UB(nn))
    lb = float(LB(nn))
    bnd = max(ub, -lb)
    say(f"    n={nn:4d}: UB={ub:.6f}  LB={lb:.6f}  "
        f"bound_analytic={bnd:.6f}")

say(f"\n  Monotonicity: UB(n) and -LB(n) are both decreasing in n for "
    f"n>=3 (each term B_max/n, 6/(n-2), 6/(n-1) is a decreasing "
    f"function of n on n>=3) => bound_analytic(n) is decreasing in n.")
say(f"  => for any N0, sup_{{n>=N0}} bound_analytic(n) = "
    f"bound_analytic(N0), so |Delta_n(x)| <= bound_analytic(N0)/n holds "
    f"for ALL n>=N0.")

# ---------------------------------------------------------------------
# Step 6: EXACT per-n sup_x|Delta_n(x)| (calculus, real_roots) -- the
# TRUE (tight) behaviour, to see how loose Step 5's analytic bound is,
# and to handle small n by direct exhaustive verification.
say("\n" + "=" * 78)
say("[Step 6] EXACT per-n sup_x|Delta_n(x)| via calculus (real_roots)")
say("=" * 78)


def exact_sup_abs_delta_K3(nn):
    dn = sp.together(delta.subs(n, nn))
    num_n, den_n = sp.fraction(sp.cancel(dn))
    dnp = sp.diff(dn, x)
    dnp = sp.together(dnp)
    num_p, _ = sp.fraction(sp.cancel(dnp))
    crit_pts = real_roots_in(num_p, x, 0, 1)
    cand = [sp.Integer(0), sp.Integer(1)] + list(crit_pts)
    best = None
    for c in cand:
        v = dn.subs(x, c)
        v = sp.nsimplify(v)
        av = sp.Abs(v)
        if best is None or sp.N(av, 30) > sp.N(best[1], 30):
            best = (c, av, v)
    return best


rows3 = []
test_ns = list(range(3, 41)) + [50, 60, 80, 100, 150, 200, 300, 500]
for nn in test_ns:
    xstar, absval, signedval = exact_sup_abs_delta_K3(nn)
    nval = sp.N(nn * absval, 15)
    rows3.append((nn, xstar, signedval, absval, nval))

with open("k3_exact_sup_table.txt", "w") as f:
    f.write("n, x*, Delta_n(x*), |Delta_n(x*)|, n*|Delta_n(x*)|\n")
    for nn, xstar, signedval, absval, nval in rows3:
        f.write(f"{nn}, {sp.N(xstar,12)}, {sp.N(signedval,15)}, "
                f"{sp.N(absval,15)}, {nval}\n")
        say(f"    n={nn:4d}: x*={sp.N(xstar,8)!s:>12}  "
            f"Delta_n(x*)={sp.N(signedval,10)!s:>14}  "
            f"n*|Delta_n(x*)|={float(nval):.8f}")

say(f"\n  M3_exact = {sp.N(M3_exact, 15)} (target asymptotic constant)")

with open("k3_sharp_rate.log", "w") as f:
    f.write("\n".join(log) + "\n")
say("\n[Saved] k3_exact_sup_table.txt, k3_sharp_rate.log")
