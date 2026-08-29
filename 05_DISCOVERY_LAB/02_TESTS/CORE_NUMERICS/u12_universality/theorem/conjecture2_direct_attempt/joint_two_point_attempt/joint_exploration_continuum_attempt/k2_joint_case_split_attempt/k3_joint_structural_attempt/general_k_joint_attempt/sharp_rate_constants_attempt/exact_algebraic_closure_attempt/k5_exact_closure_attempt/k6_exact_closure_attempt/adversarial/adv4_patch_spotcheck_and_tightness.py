"""
Hostile referee, K6-EXACT-CLOSURE-ATTEMPT.

(1) Independent spot-check of the exact per-integer-n patch (target's
    k6_exact_patch_n8_42.py) at REFEREE-CHOSEN n values (deliberately
    different from a full 8..42 re-run): n=8 (left edge), n=20 (middle),
    n=34 and n=35 (straddling the confirmed S2(n) sign change -- the
    most adversarially interesting points, since if the "extraneous
    branch, not a real violation" diagnosis were wrong, THIS is exactly
    where a real violation would first show up), n=42 (right edge of the
    patch), and n=50, n=100 (beyond the patch, to independently spot the
    continuity+IVT-covered region too, as extra due diligence beyond
    what the target's own document strictly needs).

(2) Independent confirmation of the n_0=8 TIGHTNESS claim: h6(7,1)=-1
    exactly, and -1 < -M6, so n=7 genuinely violates the bound (n_0=8 is
    the true minimal threshold, not merely a sufficient one).

Uses D6(n,k) from adv1's own independently-confirmed derivation. Written
fresh (own routine for max/min via real_roots on the fixed-n derivative),
not copied from the target's own sup_inf_h6_exact.
"""
import sympy as sp

n, x, k = sp.symbols('n x k', real=True)
K = 6

Bracket6 = (
    -k**10 + 25*k**9 + 6*k**8*n**2 - 45*k**8*n - 270*k**8 - 96*k**7*n**2
    + 760*k**7*n + 1650*k**7 - 15*k**6*n**4 + 195*k**6*n**3 - 9*k**6*n**2
    - 5380*k**6*n - 6273*k**6 + 135*k**5*n**4 - 1875*k**5*n**3
    + 4359*k**5*n**2 + 20734*k**5*n + 15345*k**5 + 20*k**4*n**6
    - 330*k**4*n**5 + 1375*k**4*n**4 + 3600*k**4*n**3 - 22441*k**4*n**2
    - 47215*k**4*n - 24080*k**4 - 80*k**3*n**6 + 1440*k**3*n**5
    - 7975*k**3*n**4 + 4641*k**3*n**3 + 50821*k**3*n**2 + 64330*k**3*n
    + 23300*k**3 - 15*k**2*n**8 + 270*k**2*n**7 - 1730*k**2*n**6
    + 3435*k**2*n**5 + 7610*k**2*n**4 - 20391*k**2*n**3 - 58916*k**2*n**2
    - 50320*k**2*n - 12576*k**2 + 15*k*n**8 - 310*k*n**7 + 2360*k*n**6
    - 7055*k*n**5 + 730*k*n**4 + 20526*k*n**3 + 33716*k*n**2 + 20016*k*n
    + 2880*k + 6*n**10 - 105*n**9 + 720*n**8 - 2375*n**7 + 3384*n**6
    - 10*n**5 - 1860*n**4 - 6696*n**3 - 7440*n**2 - 2880*n
)
Dn6 = n ** 7 * (n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)
D6_formula = k * (k + 1) * Bracket6 / Dn6

F6n = sp.cancel(D6_formula.subs(k, n * x))
F6_cont = sp.expand(1 - (1 - x ** 2) ** K)
Delta6 = sp.cancel(F6n - F6_cont)
Num6 = sp.expand(sp.cancel(Delta6 * Dn6))

Npoly_n = sp.Poly(Num6, n)
g6 = sp.expand(Npoly_n.coeff_monomial(n ** Npoly_n.degree()))
g6p = sp.expand(sp.diff(g6, x))
x6star = [c for c in sp.Poly(g6p, x).real_roots() if 0 < sp.N(c) < 1][0]
M6 = sp.simplify(g6.subs(x, x6star))
print("M6 =", sp.N(M6, 30))


def exact_max_min_h6(nv):
    """Exact max_x h6(nv,x) and min_x h6(nv,x) over x in [0,1], for a
    FIXED integer nv, via Poly(dh/dx, x).real_roots() -- independent
    implementation (uses Num6/Dn6 substitution + sp.diff, a different
    call sequence from the target's own sup_inf_h6_exact, though
    necessarily the same underlying math)."""
    Numn = Num6.subs(n, sp.Integer(nv))
    Dnn = Dn6.subs(n, sp.Integer(nv))
    h_of_x = sp.expand(sp.Integer(nv) * Numn / Dnn)
    hp = sp.Poly(h_of_x, x)
    dh = hp.diff(x)
    crit_pts = sp.Poly(dh, x).real_roots()
    cands = [c for c in crit_pts if 0 <= sp.N(c) <= 1] + [sp.Integer(0), sp.Integer(1)]
    evals = [(c, hp(c)) for c in cands]
    hi = max(evals, key=lambda cv: sp.N(cv[1]))
    lo = min(evals, key=lambda cv: sp.N(cv[1]))
    return hi, lo


print()
print("=" * 78)
print("(1) REFEREE-CHOSEN spot-check of the exact per-integer-n patch")
print("=" * 78)
referee_ns = [8, 20, 34, 35, 42, 50, 100]
M6_num = sp.N(M6, 30)
all_ok = True
for nv in referee_ns:
    hi, lo = exact_max_min_h6(nv)
    hi_val = sp.N(hi[1], 30)
    lo_val = sp.N(lo[1], 30)
    hi_ok = hi_val <= M6_num
    lo_ok = lo_val >= -M6_num
    ok = hi_ok and lo_ok
    all_ok = all_ok and ok
    print(f"  n={nv:4d}: max_x h6 = {hi_val}  (<=M6: {hi_ok})   "
          f"min_x h6 = {lo_val}  (>=-M6: {lo_ok})   OK={ok}")
print(f"\nALL referee-chosen n OK: {all_ok}")
assert all_ok
print("CONFIRMED (independent spot-check, including the two most "
      "adversarially-interesting points n=34,35 straddling the confirmed "
      "S2(n) sign change -- no violation found there, exactly as the "
      "target's own full n=8..42 sweep claims).")

print()
print("=" * 78)
print("(2) n_0=8 TIGHTNESS: does n=7 genuinely violate the lower bound?")
print("=" * 78)
h1_at_7 = sp.simplify((Num6.subs(n, 7) * 7 / Dn6.subs(n, 7)).subs(x, 1))
print("h6(7,1) [exact, referee's own independent evaluation] =", h1_at_7)
assert h1_at_7 == -1
print("CONFIRMED: h6(7,1) = -1 exactly.")
neg_M6 = -M6_num
print(f"-M6 = {neg_M6}")
assert sp.N(h1_at_7) < neg_M6
print("CONFIRMED: h6(7,1) = -1 < -M6 ~= -0.6797, so n=7 GENUINELY VIOLATES "
      "the lower bound -M6 <= h6(n,x). n_0=8 is confirmed to be the true "
      "minimal integer threshold (not merely an upper bound on "
      "sufficiency), independently reproduced.")

# Extra: also directly confirm max_x h6(7,x) so a reader can see the full
# picture at n=7 (not just the boundary x=1 value already checked).
hi7, lo7 = exact_max_min_h6(7)
print(f"\n(context) at n=7: max_x h6(7,x) = {sp.N(hi7[1],20)} (achieved at "
      f"x={sp.N(hi7[0],10)}), min_x h6(7,x) = {sp.N(lo7[1],20)} (achieved "
      f"at x={sp.N(lo7[0],10)})")
assert sp.N(lo7[1]) == sp.N(h1_at_7), "min at n=7 should be exactly the x=1 boundary value"
print("Confirms the minimum at n=7 is achieved exactly at the boundary "
      "x=1 (matching h6(7,1)), consistent with the general pattern that "
      "the boundary term, not an interior critical point, drives the "
      "K=6 lower-bound violation just below the domain.")
