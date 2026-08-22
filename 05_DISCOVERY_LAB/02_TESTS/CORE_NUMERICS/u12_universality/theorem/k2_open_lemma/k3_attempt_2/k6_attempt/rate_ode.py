"""
Continuum (n->infinity) scaling-limit derivation of BOTH the leading order F_r(t,b)
and the O(1/n) correction G_r(t,b) for g_r(m,b) (t=m/n), general r, via a genuine
induction on r using the discrete recursion of ATTEMPT.md Sec.2, expanded to two
orders in 1/n. See k6_attempt/ATTEMPT.md Sec.3 for the full derivation writeup.

State per level r: F_r(t,b) [leading], G_r(t,b) [O(1/n) correction] -- both polynomials
in t; H_r(s,b):=(1-s)F_r(1-s,b+1) [leading of h_r]; K_r(s,b) [O(1/n) correction of h_r].
"""
import sympy as sp

t, s, b = sp.symbols('t s b', nonnegative=True)


def solve_ode_poly(rhs_poly_in_t, r, b_shift_denom_extra):
    """Solve t*X'(t) + D(b)*X(t) = rhs_poly_in_t for X, X polynomial, regular at t=0.
    D(b) = 1+r+b_shift_denom_extra (kept general so caller controls exact coefficient)."""
    poly = sp.Poly(sp.expand(rhs_poly_in_t), t)
    coeffs = poly.all_coeffs()[::-1]  # coeffs[k] = coefficient of t^k
    X = 0
    for k, ck in enumerate(coeffs):
        X += sp.together(ck / (k + b_shift_denom_extra)) * t**k
    return sp.expand(X)


MAXR = 8

F = {0: sp.Rational(1, 1) / (b + 1)}
G = {0: sp.Integer(0)}
H = {0: (1 - s) / (b + 2)}       # Ĥ_0(s,b) = (1-s) F_0(1-s,b+1)
K = {0: sp.Rational(1, 1) / (b + 2)}  # exact from h_0(a,b) formula

for r in range(1, MAXR + 1):
    Fprev_bp1 = F[r - 1].subs(b, b + 1)      # F_{r-1}(t, b+1)
    # ---- F_r via ODE: t F'(t) + (1+r+b) F(t) = 1 + r*t*F_{r-1}(t,b+1)
    rhs_F = 1 + r * t * Fprev_bp1
    Fr = solve_ode_poly(rhs_F, r, 1 + r + b)
    F[r] = sp.expand(Fr)

    # ---- H_r(s,b) = (1-s) F_r(1-s, b+1)
    Hr = sp.expand((1 - s) * F[r].subs({t: 1 - s, b: b + 1}))
    H[r] = Hr

    # ---- G_r via ODE: t G'(t) + (1+r+b) G(t) =
    #        r * d/ds[H_{r-1}(s,b)]|_{s=1-t}  + r*K_{r-1}(1-t,b)
    #        + (t/2) F_r''(t,b) + (1+r+b) F_r'(t,b)
    Hprev_ds = sp.diff(H[r - 1], s)
    Hprev_ds_at = Hprev_ds.subs(s, 1 - t)
    Kprev_at = K[r - 1].subs(s, 1 - t)
    Fr_p = sp.diff(F[r], t)
    Fr_pp = sp.diff(F[r], t, 2)
    rhs_G = sp.expand(r * Hprev_ds_at + r * Kprev_at + sp.Rational(1, 2) * t * Fr_pp + (1 + r + b) * Fr_p)
    Gr = solve_ode_poly(rhs_G, r, 1 + r + b)
    G[r] = sp.expand(Gr)

    # ---- K_r(s,b) = 1 + r*H_{r-1}(s,b+1) + (1-s) G_r(1-s,b+1) - (1+b+r) F_r(1-s,b+1)
    Hprev_bp1 = H[r - 1].subs(b, b + 1)
    Gr_bp1_at = G[r].subs({t: 1 - s, b: b + 1})
    Fr_bp1_at = F[r].subs({t: 1 - s, b: b + 1})
    Kr = sp.expand(1 + r * Hprev_bp1 + (1 - s) * Gr_bp1_at - (1 + b + r) * Fr_bp1_at)
    K[r] = Kr

    print(f"--- r={r} ---")
    print("F_r(t,b) =", F[r])
    print("F_r(1,b) =", sp.simplify(F[r].subs(t, 1)))
    print("G_r(t,b) =", G[r])
    print("G_r(1,b) =", sp.simplify(G[r].subs(t, 1)))
    print("G_r(1,0) =", sp.nsimplify(sp.simplify(G[r].subs({t: 1, b: 0}))))
    phiK = sp.Rational(4**r * sp.factorial(r)**2, sp.factorial(2*r+1))
    predicted = sp.simplify(sp.Rational(r, 4) * phiK)
    print(f"   K*phi_K/4 (conjectured) = {predicted}  match={sp.simplify(G[r].subs({t:1,b:0})-predicted)==0}")
    print(flush=True)

import pickle
with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/rate_ode_data.pkl', 'wb') as f:
    pickle.dump({'F': F, 'G': G, 'H': H, 'K': K}, f)
print("DONE")
