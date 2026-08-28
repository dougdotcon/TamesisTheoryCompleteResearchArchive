"""
v02_new_identity_check.py -- verify the new algebraic identity

    W(x,y) = (1 - eps*(x+y)) * Psi(x,y) + eps * I(x,y)          (NEW-W)

derived by substituting the required reading's own exact (E1)
(Psi_x = (x+y)Psi - I) into (KEY) (W = Psi - eps*Psi_x), i.e. purely
algebraic elimination of Psi_x -- no differentiation of any integral
representation is needed to get W, which is what removes the
"derivative-loss" obstruction h1_energy_estimate_attempt/ATTEMPT.md
Sec 8.4 names as the reason making the full coupled Volterra system
rigorous is hard.

Two independent numerical routes for Psi_x are compared:
  (a) via (E1) directly:      Psi_x = (x+y)Psi - I                  [algebraic]
  (b) via direct differentiation of the b_k(s) series in s:
      Psi(s,g) = sum_k b_k(s) g^k  =>  d(Psi)/ds = sum_k b_k'(s) g^k,
      and Psi_x = eps * d(Psi)/ds (chain rule, x = s*sqrt(c) = s/eps)
      -- using Family.deriv(), NOT (E1), a structurally different route.
If (a) and (b) agree, that is an independent re-verification of (E1)
itself (not just of the new W-identity), before (NEW-W) is trusted.

Also verifies (BB-Psi') itself (already checked by the required reading,
re-verified here independently) and the pulled-out-constant reformulation

    Phi(x,y) = e^{-y/eps} + [(1-eps(x+y))/eps] * A(x,y) + B(x,y)     (E2')
    A(x,y) := int_0^y e^{-v/eps} Psi(x+v,y-v) dv
    B(x,y) := int_0^y e^{-v/eps} I(x+v,y-v) dv

against direct evaluation of (E2) itself.
"""
import sys, os
import mpmath as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v01_family_series import Family, bounded_branch_solve


def build_series(c_val, K, dps):
    old = mp.mp.dps
    mp.mp.dps = dps
    c = mp.mpf(c_val)
    a = [None] * (K + 2)
    b = [None] * (K + 2)
    a[0] = Family([mp.mpf(1)], [], c)
    b[0] = Family([], [], c)
    a[1] = Family([-c], [], c)
    b[1] = bounded_branch_solve(Family([-c], [], c))
    for k in range(1, K + 1):
        term1 = a[k - 1].scale(mp.mpf(1) / k)
        term2 = b[k].mul_1_minus_s()
        w_k = term1.add(term2).sub(b[k - 1])
        akp1 = a[k].deriv().sub(a[k].scale(c)).add(w_k.scale(c)).scale(mp.mpf(1) / (k + 1))
        a[k + 1] = akp1
        if k + 1 <= K:
            src = a[k].scale(-c / (k + 1)).add(b[k].scale(c))
            b[k + 1] = bounded_branch_solve(src)
    mp.mp.dps = old
    return a, b


def eval_Phi(a, s, g, K):
    r = mp.mpf(0); gp = mp.mpf(1)
    for k in range(K + 1):
        r += a[k].eval(s) * gp
        gp *= g
    return r


def eval_Psi(b, s, g, K):
    r = mp.mpf(0); gp = mp.mpf(1)
    for k in range(K + 1):
        r += b[k].eval(s) * gp
        gp *= g
    return r


def eval_Psi_s_direct(b, s, g, K):
    # d(Psi)/ds via term-by-term differentiation of the family series
    r = mp.mpf(0); gp = mp.mpf(1)
    for k in range(K + 1):
        r += b[k].deriv().eval(s) * gp
        gp *= g
    return r


def eval_I_unscaled(a, s, g, K):
    # I_ug(s,g) := int_0^g Phi(s,g') dg' = sum_k a_k(s) g^{k+1}/(k+1)
    r = mp.mpf(0); gp = g
    for k in range(K + 1):
        r += a[k].eval(s) * gp / (k + 1)
        gp *= g
    return r


def eval_I_scaled(a, s, g, K, eps):
    # I(x,y) [scaled] = (1/eps) * I_ug(s,g)
    return eval_I_unscaled(a, s, g, K) / eps


def eval_Psi_scaled_via_BBPsi(a, s, g, c, K, dps, Umax=8.0):
    # Psi(x,y) [scaled] via (BB-Psi'-unscaled):
    #   Psi(s,g) = c * int_0^inf e^{-c[v^2/2+v(s+g)]} * I_ug(s+v,g) dv
    def integrand(v):
        return mp.e ** (-c * (v ** 2 / 2 + v * (s + g))) * eval_I_unscaled(a, s + v, g, K)
    val = mp.quad(integrand, [0, Umax / mp.sqrt(c), 2 * Umax / mp.sqrt(c)])
    return c * val


if __name__ == "__main__":
    mp.mp.dps = 80
    c_val = 200.0
    K = 90
    dps = 90
    print(f"Building family series c={c_val}, K={K}, dps={dps} ...")
    a, b = build_series(c_val, K, dps)
    mp.mp.dps = dps

    c = mp.mpf(c_val)
    eps = 1 / mp.sqrt(c)

    print()
    print("=== Check 1: (E1) cross-check -- Psi_x via (E1) vs via direct d/ds of b_k series ===")
    test_pts = [(mp.mpf('0.00'), mp.mpf('0.05')), (mp.mpf('0.05'), mp.mpf('0.05')),
                (mp.mpf('0.10'), mp.mpf('0.08')), (mp.mpf('0.20'), mp.mpf('0.03'))]
    for s, g in test_pts:
        x = s * mp.sqrt(c)
        y = g * mp.sqrt(c)
        Psi_val = eval_Psi(b, s, g, K)
        I_val = eval_I_scaled(a, s, g, K, eps)
        Psi_x_via_E1 = (x + y) * Psi_val - I_val
        Psi_s_direct = eval_Psi_s_direct(b, s, g, K)
        Psi_x_via_direct_diff = eps * Psi_s_direct  # x=s/eps => d/dx = eps*d/ds
        rel = abs(Psi_x_via_E1 - Psi_x_via_direct_diff) / max(abs(Psi_x_via_E1), mp.mpf('1e-300'))
        print(f"  (s={s},g={g}): Psi_x[E1]={mp.nstr(Psi_x_via_E1,15)}  "
              f"Psi_x[direct d/ds]={mp.nstr(Psi_x_via_direct_diff,15)}  reldiff={mp.nstr(rel,4)}")

    print()
    print("=== Check 2: new identity W = (1-eps(x+y))Psi + eps*I  vs  W = Psi - eps*Psi_x[direct] ===")
    for s, g in test_pts:
        x = s * mp.sqrt(c)
        y = g * mp.sqrt(c)
        Psi_val = eval_Psi(b, s, g, K)
        I_val = eval_I_scaled(a, s, g, K, eps)
        Psi_s_direct = eval_Psi_s_direct(b, s, g, K)
        Psi_x_direct = eps * Psi_s_direct
        W_direct = Psi_val - eps * Psi_x_direct           # original KEY, independent differentiation route
        W_new = (1 - eps * (x + y)) * Psi_val + eps * I_val  # NEW algebraic identity
        rel = abs(W_direct - W_new) / max(abs(W_direct), mp.mpf('1e-300'))
        print(f"  (s={s},g={g}): W[KEY,direct-diff]={mp.nstr(W_direct,15)}  "
              f"W[NEW algebraic]={mp.nstr(W_new,15)}  reldiff={mp.nstr(rel,4)}")

    print()
    print("=== Check 3: (BB-Psi') re-verification (Psi via series vs via renewal integral) ===")
    for s, g in test_pts[:3]:
        Psi_direct = eval_Psi(b, s, g, K)
        Psi_via_BB = eval_Psi_scaled_via_BBPsi(a, s, g, c, K, dps)
        rel = abs(Psi_direct - Psi_via_BB) / max(abs(Psi_direct), mp.mpf('1e-300'))
        print(f"  (s={s},g={g}): Psi[series]={mp.nstr(Psi_direct,15)}  Psi[BB-Psi integral]={mp.nstr(Psi_via_BB,15)}  reldiff={mp.nstr(rel,4)}")

    print()
    print("=== Check 4: (E2') pulled-out-constant form vs direct Phi(x,y) from series ===")
    Umax = 8.0

    def A_of(s, g):
        x = s * mp.sqrt(c); y = g * mp.sqrt(c)
        def integrand(v):
            gp = g - v / mp.sqrt(c)
            sp = s + v / mp.sqrt(c)
            return mp.e ** (-v / eps) * eval_Psi(b, sp, gp, K)
        return mp.quad(integrand, [0, y])

    def B_of(s, g):
        x = s * mp.sqrt(c); y = g * mp.sqrt(c)
        def integrand(v):
            gp = g - v / mp.sqrt(c)
            sp = s + v / mp.sqrt(c)
            return mp.e ** (-v / eps) * eval_I_scaled(a, sp, gp, K, eps)
        return mp.quad(integrand, [0, y])

    for s, g in test_pts[:3]:
        x = s * mp.sqrt(c); y = g * mp.sqrt(c)
        Phi_direct = eval_Phi(a, s, g, K)
        Aval = A_of(s, g)
        Bval = B_of(s, g)
        Phi_E2p = mp.e ** (-y / eps) + ((1 - eps * (x + y)) / eps) * Aval + Bval
        rel = abs(Phi_direct - Phi_E2p) / max(abs(Phi_direct), mp.mpf('1e-300'))
        print(f"  (s={s},g={g}): Phi[series]={mp.nstr(Phi_direct,15)}  Phi[(E2')]={mp.nstr(Phi_E2p,15)}  reldiff={mp.nstr(rel,4)}")
