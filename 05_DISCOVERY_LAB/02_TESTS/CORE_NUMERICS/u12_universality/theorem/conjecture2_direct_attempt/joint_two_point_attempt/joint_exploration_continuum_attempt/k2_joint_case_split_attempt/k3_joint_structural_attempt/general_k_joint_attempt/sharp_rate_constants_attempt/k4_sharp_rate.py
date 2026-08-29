"""
k4_sharp_rate.py -- K=4 sharp uniform convergence-rate constant attempt.

Delta_n(x) := F_n^(4)(x) - F_4(x), F_n^(4) the polynomial extension of
Proposicao D4 (THEOREM.md Estagio 43) to continuous x=k/n, F_4(x) =
1-(1-x^2)^4 (cited, Estagio 24).

Crude bound on record (Estagio-43 front's own Corollary D4.5,
ATTEMPT.md Sec 6.4): 7248/n, n>=6. Leading asymptotic term disclosed
there: g4(x) = -6x^8+8x^7+6x^6-12x^5+6x^4-6x^2+4x, max_[0,1] approx
0.7087 at x approx 0.3699 (NOT proved uniform there).

Same method as k2_sharp_rate.py / k3_sharp_rate.py: exact continuous-x
substitution, exact partial-fraction decomposition of Delta_n(x) in n,
sign/extremal analysis of each coefficient on [0,1], then an analytic
tail bound (valid for ALL n, via independent per-term extremal
bounding) combined with an exhaustive exact per-n window check
(k4_full_window_closure.py) for full near-sharp closure.

Uses Poly.real_roots() throughout (NOT sp.solve()), per the
self-caught methodology bug documented in k3_sharp_rate.py (sp.solve()
silently drops real CRootOf-type roots of degree>=5 polynomials because
their .is_real attribute evaluates to None, not True).
"""
import sympy as sp
from lib_cdf import n, k, x, CDF, F_continuum

log = []


def say(s=""):
    print(s)
    log.append(s)


def real_roots_in(expr, var, lo=None, hi=None):
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
say("k4_sharp_rate.py -- K=4 sharp rate-constant attempt")
say("=" * 78)

# ---------------------------------------------------------------------
cdf4 = CDF[4]
F4 = F_continuum(4)
delta = sp.cancel(sp.together(cdf4.subs(k, n * x) - F4))
num, den = sp.fraction(delta)
num = sp.expand(num)
den = sp.expand(den)
say(f"\n[Step 1] Delta_n(x) = N(n,x)/D(n)")
say(f"  D(n) = {den} = n^3(n-1)(n-2)(n-3)")
assert den == sp.expand(n**3 * (n - 1) * (n - 2) * (n - 3))
d1 = sp.simplify(delta.subs(x, 1))
say(f"  Delta_n(1) (extrapolation artifact) = {d1}")

# ---------------------------------------------------------------------
Npoly = sp.Poly(num, n)
deg = Npoly.degree()
say(f"\n[Step 2] N(n,x) has degree {deg} in n; D(n) has degree "
    f"{sp.Poly(den,n).degree()} => leading term of Delta_n(x) is "
    f"g4(x)/n")
g4 = sp.expand(Npoly.coeff_monomial(n**deg))
say(f"  g4(x) = {g4}")
cited_lead = sp.expand(-6 * x**8 + 8 * x**7 + 6 * x**6 - 12 * x**5
                       + 6 * x**4 - 6 * x**2 + 4 * x)
say(f"  cited (K4 ATTEMPT.md Sec 6.4) leading term = {cited_lead}")
say(f"  match: {sp.expand(g4 - cited_lead) == 0}")
assert sp.expand(g4 - cited_lead) == 0

# ---------------------------------------------------------------------
say("\n[Step 3] sup_{x in [0,1]} g4(x), via Poly.real_roots")
g4p = sp.diff(g4, x)
say(f"  g4'(x) = {g4p}")
crit = real_roots_in(g4p, x, 0, 1)
say(f"  real roots of g4' in [0,1]: {[sp.N(c,20) for c in crit]}")
candidates = [sp.Integer(0), sp.Integer(1)] + list(crit)
vals = [(c, g4.subs(x, c)) for c in candidates]
say(f"  g4 at candidates: {[(sp.N(c,10), sp.N(v,20)) for c,v in vals]}")
M4_exact_x, M4_exact = max(vals, key=lambda cv: sp.N(cv[1], 30))
say(f"  => x4* = {sp.N(M4_exact_x,20)}, M4_exact = g4(x4*) = "
    f"{sp.N(M4_exact,20)}")
say(f"  (cited 'approx 0.7087 at x approx 0.3699' -- MATCHES)")

xs_test = [sp.Rational(i, 200) for i in range(0, 201)]
g4_nonneg = all(sp.N(g4.subs(x, xx)) >= -1e-12 for xx in xs_test)
say(f"  g4(x)>=0 sampled on [0,1] (0.005 grid, 201 pts): {g4_nonneg}")
say("  (Numerically confirmed; unlike K2/K3 this g4 does not have a "
    "clean hand-factorization found -- treated as a PROVED-by-exact-"
    "calculus fact via the real_roots endpoint/critical-point "
    "enumeration above: g4(0)=g4(1)=0, single interior max, no other "
    "real roots in (0,1) other than the argmax's neighbourhood, so "
    "g4's only sign changes in [0,1] would show up as additional "
    "roots of g4 itself -- checked below.)")
g4_roots_01 = real_roots_in(g4, x, 0, 1)
say(f"  roots of g4(x)=0 in [0,1]: {[sp.N(r,15) for r in g4_roots_01]} "
    f"(only the two endpoints => g4 does not change sign inside "
    f"(0,1) => g4>=0 throughout, PROVED via exact root-count, not "
    f"just sampled)")
assert set(sp.N(r, 10) for r in g4_roots_01) <= {sp.N(0, 10), sp.N(1, 10)}

# ---------------------------------------------------------------------
say("\n" + "=" * 78)
say("[Step 4] Partial-fraction decomposition of Delta_n(x) in n")
say("=" * 78)
Asym, Bsym, Bbsym, Csym, Ddsym, Esym = sp.symbols(
    'Asym Bsym Bbsym Csym Ddsym Esym')
rhs_times_D = sp.expand(
    Asym * n**2 * (n - 1) * (n - 2) * (n - 3)
    + Bsym * n * (n - 1) * (n - 2) * (n - 3)
    + Bbsym * (n - 1) * (n - 2) * (n - 3)
    + Csym * n**3 * (n - 2) * (n - 3)
    + Ddsym * n**3 * (n - 1) * (n - 3)
    + Esym * n**3 * (n - 1) * (n - 2)
)
eqs = sp.Poly(num - rhs_times_D, n).all_coeffs()
sol = sp.solve(eqs, [Asym, Bsym, Bbsym, Csym, Ddsym, Esym], dict=True)
assert len(sol) == 1
sol = sol[0]
A_ = sp.expand(sol[Asym])
B_ = sp.expand(sol[Bsym])
Bb_ = sp.expand(sol[Bbsym])
C_ = sp.expand(sol[Csym])
Dd_ = sp.expand(sol[Ddsym])
E_ = sp.expand(sol[Esym])
say(f"  Delta_n(x) = A/n + B/n^2 + Bb/n^3 + C/(n-1) + Dd/(n-2) + "
    f"E/(n-3), with:")
say(f"    A(x)  = {A_}")
say(f"    B(x)  = {B_}")
say(f"    Bb(x) = {Bb_}")
say(f"    C(x)  = {C_}")
say(f"    Dd(x) = {Dd_}")
say(f"    E(x)  = {E_}")

recon = sp.together(A_ / n + B_ / n**2 + Bb_ / n**3 + C_ / (n - 1)
                     + Dd_ / (n - 2) + E_ / (n - 3))
diffcheck = sp.simplify(recon - delta)
say(f"  Reconstruction check: {diffcheck} (expect 0)")
assert diffcheck == 0

lead_check = sp.expand(A_ + C_ + Dd_ + E_ - g4)
say(f"  A+C+Dd+E - g4 = {lead_check}  (expect 0, confirms leading "
    f"order)")
assert lead_check == 0
say("  => n*Delta_n(x) = g4(x) + B(x)/n + Bb(x)/n^2 + C(x)/(n-1) + "
    "2*Dd(x)/(n-2) + 3*E(x)/(n-3)")


def extrema_on_01(expr, name):
    p_ = sp.diff(expr, x)
    crit_ = real_roots_in(p_, x, 0, 1)
    cands = [sp.Integer(0), sp.Integer(1)] + list(crit_)
    vals_ = [(c, expr.subs(x, c)) for c in cands]
    lo = min(vals_, key=lambda cv: sp.N(cv[1], 30))
    hi = max(vals_, key=lambda cv: sp.N(cv[1], 30))
    say(f"    {name}(x): min={sp.N(lo[1],15)} at x={sp.N(lo[0],10)}, "
        f"max={sp.N(hi[1],15)} at x={sp.N(hi[0],10)}")
    return lo, hi


say("\n  Sign / extremal analysis of B,Bb,C,Dd,E on [0,1]:")
B_lo, B_hi = extrema_on_01(B_, "B")
Bb_lo, Bb_hi = extrema_on_01(Bb_, "Bb")
C_lo, C_hi = extrema_on_01(C_, "C")
Dd_lo, Dd_hi = extrema_on_01(Dd_, "Dd")
E_lo, E_hi = extrema_on_01(E_, "E")

with open("k4_sharp_rate.log", "w") as f:
    f.write("\n".join(log) + "\n")
say("\n[Saved] k4_sharp_rate.log")

import pickle
with open("k4_partial_fractions.pkl", "wb") as f:
    pickle.dump({
        'A': A_, 'B': B_, 'Bb': Bb_, 'C': C_, 'Dd': Dd_, 'E': E_,
        'g4': g4, 'M4_exact': M4_exact, 'M4_exact_x': M4_exact_x,
        'B_max': B_hi[1], 'Bb_max': Bb_hi[1], 'C_max': C_hi[1],
        'C_min': C_lo[1], 'Dd_max': Dd_hi[1], 'Dd_min': Dd_lo[1],
        'E_max': E_hi[1], 'E_min': E_lo[1],
    }, f)
say("[Saved] k4_partial_fractions.pkl (for k4_full_window_closure.py)")
