"""
Script 01 -- setup and independent re-verification of citable inputs.

This front's mandate (DISC-DEC-145, wave 32 front b) is to attack item 1 of
the predecessor's own Section 7 diagnosis: a UNIFORM (not leading-order-only)
Watson's-lemma-type remainder for the INNER t-integral

    I(n,m,gamma) := int_0^1 t^m (1-t)^m (1-gamma*t)^(n-m) dt

of the Beta(m+1,m+1)-tilted-moment representation

    T(n,m) = C(n+m+1, 2m+1) * (1/B(m+1,m+1)) * I(n,m,gamma)

established (Estagio 54, referee's Pfaff-transform derivation) and used by
the immediate predecessor (Estagio 56, joint_saddle_point_attempt) to build
t*(n,m,gamma) and T_prof(lambda,gamma).

Per the mandate: t*(n,m,gamma) and T_prof(lambda,gamma) are CITED as already
established, not re-derived from scratch. This script performs a light,
disclosed independent sanity check that the cited closed form for t* is
correct (it is the unique root of g'(t)=0 in (0,1)) and that g is globally
concave on (0,1) for gamma in (0,1) -- both facts are already PROVED in the
predecessor's record (Estagio 56 finding 1, referee item (a)); re-confirming
them here is not re-deriving, it is verifying the citable input before
building the new remainder analysis on top of it, per this lineage's
established discipline ("independently re-verify before building on it").

No .py file from any ancestor or referee front was read, imported, or
consulted. All code in this file is written fresh from the mathematical
prose of THEOREM.md Estagio 54/56 and the predecessor's ATTEMPT.md sections
1, 3, 4 (read in full, see this front's own ATTEMPT.md Sec 0).
"""
import sympy as sp

n, m, gam, t = sp.symbols('n m gamma t', positive=True)

# ---------------------------------------------------------------------
# (A) The exact log-integrand g(t) of the Beta-tilted moment, and its
#     derivatives, as CITED from Estagio 56 / predecessor Sec 3.
# ---------------------------------------------------------------------
g = m*sp.log(t) + m*sp.log(1-t) + (n-m)*sp.log(1-gam*t)

gp = sp.diff(g, t)
gpp = sp.diff(g, t, 2)
gppp = sp.diff(g, t, 3)
gpppp = sp.diff(g, t, 4)

print("=== (A) Exact derivatives of g(t) = m ln t + m ln(1-t) + (n-m) ln(1-gamma t) ===")
print("g'(t)  =", sp.simplify(gp))
print("g''(t) =", sp.simplify(gpp))
print("g'''(t)=", sp.simplify(gppp))
print("g''''(t)=", sp.simplify(gpppp))

# ---------------------------------------------------------------------
# (B) Re-verify (fresh sympy, independent of predecessor's own script)
#     that g'(t)=0 reduces, after clearing denominators, to the quadratic
#     gamma(m+n) t^2 - (2m+gamma n) t + m = 0, and that the CITED closed
#     form
#        t*(n,m,gamma) = [2m + gamma n - sqrt(gamma^2 n^2 + 4(1-gamma)m^2)]
#                          / (2 gamma (m+n))
#     is its root vanishing at m=0 (the other root -> 1 there).
# ---------------------------------------------------------------------
print()
print("=== (B) Re-verification of the CITED t* closed form (Estagio 56 finding 1) ===")
gp_num = sp.together(gp)
num, den = sp.fraction(gp_num)
num = sp.expand(num)
print("Numerator of g'(t) after clearing denominators:", num)

quad_target = gam*(m+n)*t**2 - (2*m + gam*n)*t + m
diff_quad = sp.expand(num - quad_target)
print("num - [gamma(m+n) t^2 - (2m+gamma n) t + m] =", diff_quad,
      " (expect 0, up to overall sign convention)")
diff_quad_negsign = sp.expand(num + quad_target)
print("num + [...] =", diff_quad_negsign, " (checking the other sign convention too)")

t_star = (2*m + gam*n - sp.sqrt(gam**2*n**2 + 4*(1-gam)*m**2)) / (2*gam*(m+n))

quad_at_tstar = sp.simplify(quad_target.subs(t, t_star))
print("Quadratic evaluated at cited t*(n,m,gamma):", quad_at_tstar, " (expect 0)")

# vanishes at m=0
print("t* at m=0:", sp.simplify(t_star.subs(m, 0)), " (expect 0)")

# ---------------------------------------------------------------------
# (C) Re-verify global concavity of g on (0,1): each additive term is
#     individually concave (Estagio 56 referee item (a), PROVED there).
# ---------------------------------------------------------------------
print()
print("=== (C) Re-verification of global concavity (each term) ===")
term1 = m*sp.log(t)
term2 = m*sp.log(1-t)
term3 = (n-m)*sp.log(1-gam*t)

d2_term1 = sp.diff(term1, t, 2)
d2_term2 = sp.diff(term2, t, 2)
d2_term3 = sp.diff(term3, t, 2)
print("d2/dt2 [m ln t]        =", d2_term1, " -- negative for t>0, m>0: concave")
print("d2/dt2 [m ln(1-t)]     =", d2_term2, " -- negative for t<1, m>0: concave")
print("d2/dt2 [(n-m) ln(1-gt)]=", sp.simplify(d2_term3),
      " -- negative for gamma t<1, n>m: concave")

# Direct numeric spot check at several points that g'' < 0 throughout,
# not just at t*, confirming global concavity numerically as well.
import random
random.seed(20260951001)  # reserved block, frente (b), first draw of this front
print()
print("=== (C') Numeric spot-check g''(t) < 0 at random interior points ===")
print("[seed 20260951001 drawn from reserved block 20260951000-20260951999]")
bad = 0
for i in range(30):
    n_v = random.randint(20, 200000)
    m_v = random.randint(0, min(n_v - 1, 5000))
    g_v = random.uniform(0.05, 0.95)
    t_v = random.uniform(0.001, 1/max(g_v, 1e-9) - 0.001) if g_v > 0 else random.uniform(0.001, 0.999)
    t_v = min(t_v, 0.999)
    val = float(gpp.subs({n: n_v, m: m_v, gam: g_v, t: t_v}))
    ok = val < 0
    if not ok:
        bad += 1
        print(f"  MISMATCH n={n_v} m={m_v} gamma={g_v:.4f} t={t_v:.4f} g''={val}")
print(f"Checked 30 random points, negative-g'' violations: {bad}")

print()
print("Script 01 complete. All facts in (B),(C) are re-verifications of")
print("ALREADY-PROVED citable inputs (Estagio 56 finding 1 and its referee")
print("item (a)), not new claims of this front.")
