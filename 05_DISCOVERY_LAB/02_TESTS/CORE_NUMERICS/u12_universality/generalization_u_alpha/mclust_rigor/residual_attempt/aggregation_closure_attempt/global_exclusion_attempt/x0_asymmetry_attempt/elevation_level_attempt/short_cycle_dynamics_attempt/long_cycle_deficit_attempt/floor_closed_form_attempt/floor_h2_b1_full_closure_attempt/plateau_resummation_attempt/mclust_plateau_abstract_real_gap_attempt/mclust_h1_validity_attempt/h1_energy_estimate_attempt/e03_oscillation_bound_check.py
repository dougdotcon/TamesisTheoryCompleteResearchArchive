"""
e03_oscillation_bound_check.py -- numerical check of the GLOBAL-in-x
oscillation bound (star-star) derived in ATTEMPT.md Sec 3.2:

    sup_{x>=0} |Psi(x,y2) - Psi(x,y1)|  <=  (y2-y1) * Kconst * R(x0+y1)

for ANY x0>=0 achieving the sup (R is DEcreasing, so the bound's tightest
form is with x=0), where R(z) = sqrt(pi/2)*erfcx(z/sqrt2) is the SAME
function used throughout this lineage for psi1, and Kconst is an upper
bound on |Phi|+|Psi| over the domain swept.

In UNSCALED (s,g) variables (x=s*sqrt(c), y=g*sqrt(c)):

    sup_s |Psi(s,g2)-Psi(s,g1)|  <=  sqrt(c)*(g2-g1) * Kconst * R(sqrt(c)*g1)

This script computes the LHS directly (via the already-validated e01
family-series solver -- direct summation, no quadrature) over a grid of
s, and compares against the RHS using an OBSERVED (not independently
proved) Kconst = max(|Phi|,|Psi|) over the tested domain, to check the
bound is never violated.
"""

import mpmath as mp
import e01_family_series as fs


def R_func(z):
    return mp.sqrt(mp.pi / 2) * fs.erfcx(z / mp.sqrt(2))


def main():
    c_val = 100
    K = 220
    dps = 210
    mp.mp.dps = dps
    c = mp.mpf(c_val)
    sqrt_c = mp.sqrt(c)

    print(f"=== e03_oscillation_bound_check :: c={c_val}, K={K}, dps={dps} ===")
    a, b = fs.build_series(c, K, dps)

    s_grid = [mp.mpf(v) for v in ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5"]]
    g1 = mp.mpf("0.06")
    g2_list = [mp.mpf(v) for v in ["0.10", "0.18", "0.30"]]

    # empirically observed bound on |Phi|,|Psi| over the tested domain
    obs_max = mp.mpf(0)
    Phi_vals, Psi_vals = {}, {}
    all_g = sorted(set([g1] + g2_list))
    for s0 in s_grid:
        Phi_of_g = fs.eval_Phi(a, s0, c)
        Psi_of_g = fs.eval_Psi(b, s0, c)
        for g in all_g:
            pv, qv = Phi_of_g(g), Psi_of_g(g)
            Phi_vals[(s0, g)] = pv
            Psi_vals[(s0, g)] = qv
            obs_max = max(obs_max, abs(pv), abs(qv))

    Kconst = 2 * obs_max
    print(f"observed max(|Phi|,|Psi|) over tested domain = {mp.nstr(obs_max,10)}")
    print(f"Kconst used (2x observed max, per the derivation's |f|<=(g2-g1)(M_Phi+M_Psi) "
          f"bound) = {mp.nstr(Kconst,10)}\n")

    all_pass = True
    for g2 in g2_list:
        lhs_vals = []
        for s0 in s_grid:
            diff = abs(Psi_vals[(s0, g2)] - Psi_vals[(s0, g1)])
            lhs_vals.append(diff)
        lhs_sup = max(lhs_vals)
        rhs = sqrt_c * (g2 - g1) * Kconst * R_func(sqrt_c * g1)
        ok = lhs_sup <= rhs
        all_pass = all_pass and ok
        print(f"g1={mp.nstr(g1,4)} g2={mp.nstr(g2,4)}: "
              f"sup_s|Psi(s,g2)-Psi(s,g1)| = {mp.nstr(lhs_sup,12)}   "
              f"bound RHS = {mp.nstr(rhs,12)}   "
              f"ratio(LHS/RHS) = {mp.nstr(lhs_sup/rhs,8)}   "
              f"{'OK' if ok else 'VIOLATED'}")

    print()
    print("VERDICT:", "bound holds at every tested (s,g1,g2) -- consistent "
          "with the derivation (Sec 3.2)." if all_pass else
          "BOUND VIOLATED somewhere -- derivation or constant needs revisiting.")


if __name__ == "__main__":
    main()
