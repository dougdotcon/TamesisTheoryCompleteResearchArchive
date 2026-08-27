"""
v05_oscillation_bound_check.py
--------------------------------
Independent numerical sanity check of the target's oscillation bound
(star-star), Sec5 of ATTEMPT.md:

  sup_{x>=0} |Psi(x,y2)-Psi(x,y1)|  <=  (y2-y1) * K * R(y1)  <=  (y2-y1)*K/y1

using the referee's OWN series solver (v03), own (s, g1, g2) triples
(distinct from the target's own g1=0.06, g2 in {0.10,0.18,0.30}, c=100
grid), and an independently-measured K := 2*max(|Phi|,|Psi|) over the
sampled domain (own sampling, own convention -- matches the target's
own convention of K bounding |Phi|+|Psi| via 2*max(...) as a simple,
disclosed empirical proxy, but computed from THIS run's own samples).

In UNSCALED units (s,g), with x=s*sqrt(c), y=g*sqrt(c), y2-y1=(g2-g1)*sqrt(c),
R(y1) = R(g1*sqrt(c)):
  sup_s |Psi(s,g2)-Psi(s,g1)|  <=  (g2-g1)*sqrt(c) * K * R(g1*sqrt(c))
"""
import mpmath as mp
import v03_series_solver as v

mp.mp.dps = 40

def R_closed(z):
    w = z/mp.sqrt(2)
    return mp.sqrt(mp.pi/2) * mp.e**(w*w) * mp.erfc(w)

def check_converged(a, b, a2, b2, s_list, g, c_val, tag=""):
    """K-convergence sanity check (own convention, per lineage discipline):
    compare Phi,Psi at two different K over the s-grid and g used; flags
    (rather than silently trusts) any under-converged point."""
    worst = mp.mpf(0)
    for s0 in s_list:
        p1 = v.Phi_series(a, s0, g, c_val)
        p2 = v.Phi_series(a2, s0, g, c_val)
        rp = abs(p1-p2)/abs(p2) if p2 != 0 else abs(p1-p2)
        q1 = v.Psi_series(b, s0, g, c_val)
        q2 = v.Psi_series(b2, s0, g, c_val)
        rq = abs(q1-q2)/abs(q2) if q2 != 0 else abs(q1-q2)
        worst = max(worst, rp, rq)
    ok = worst < mp.mpf('1e-12')
    print(f"  [K-convergence check {tag}] worst reldiff between K and K_check = {mp.nstr(worst,6)}  {'OK' if ok else '*** NOT CONVERGED ***'}")
    return ok

def run_check(c_val, K, s_list, g1, g2, label="", K_check=None):
    print(f"\n--- c={float(c_val)}, K={K}, g1={float(g1)}, g2={float(g2)}  {label} ---")
    a, b = v.build_series(c_val, K)
    if K_check is not None:
        a2, b2 = v.build_series(c_val, K_check)
        ok1 = check_converged(a, b, a2, b2, s_list, g1, c_val, tag=f"(g1={float(g1)})")
        ok2 = check_converged(a, b, a2, b2, s_list, g2, c_val, tag=f"(g2={float(g2)})")
        if not (ok1 and ok2):
            print("  ** using K_check series instead of K for this triple **")
            a, b = a2, b2

    sqrt_c = mp.sqrt(c_val)
    y1 = g1*sqrt_c
    h = (g2-g1)*sqrt_c

    Phi_vals, Psi_vals, Delta_vals = [], [], []
    for s0 in s_list:
        phi1 = v.Phi_series(a, s0, g1, c_val)
        phi2 = v.Phi_series(a, s0, g2, c_val)
        psi1v = v.Psi_series(b, s0, g1, c_val)
        psi2v = v.Psi_series(b, s0, g2, c_val)
        Phi_vals += [phi1, phi2]
        Psi_vals += [psi1v, psi2v]
        Delta_vals.append(abs(psi2v - psi1v))
        print(f"  s0={float(s0):6.3f}  Phi(s0,g1)={mp.nstr(phi1,12)}  Phi(s0,g2)={mp.nstr(phi2,12)}  "
              f"Psi(s0,g1)={mp.nstr(psi1v,12)}  Psi(s0,g2)={mp.nstr(psi2v,12)}  |Delta Psi|={mp.nstr(Delta_vals[-1],12)}")

    K_emp = 2*max(max(abs(x) for x in Phi_vals), max(abs(x) for x in Psi_vals))
    sup_delta = max(Delta_vals)
    bound_Rterm = h * K_emp * R_closed(y1)
    bound_loose = h * K_emp / y1

    print(f"\n  Empirical K = 2*max(|Phi|,|Psi|) over these samples = {mp.nstr(K_emp,10)}")
    print(f"  sup_s |Delta Psi|                 = {mp.nstr(sup_delta,10)}")
    print(f"  bound h*K*R(y1)   (tighter form)  = {mp.nstr(bound_Rterm,10)}")
    print(f"  bound h*K/y1      (looser form)   = {mp.nstr(bound_loose,10)}")
    ok1 = sup_delta <= bound_Rterm
    ok2 = sup_delta <= bound_loose
    print(f"  sup_delta <= h*K*R(y1)? {ok1}   sup_delta <= h*K/y1? {ok2}")
    print(f"  ratio (LHS/RHS, tighter form) = {mp.nstr(sup_delta/bound_Rterm,6)}")
    return ok1, ok2, sup_delta, bound_Rterm, bound_loose


if __name__ == "__main__":
    print("="*78)
    print("Independent check of the global-in-x oscillation bound (star-star)")
    print("Own series solver, own (s,g1,g2,c) choices, distinct from target's grid.")
    print("="*78)

    results = []
    c_val = mp.mpf(1000)
    K = 260
    K_check = 340
    s_list = [mp.mpf(v_) for v_ in ['0', '0.02', '0.05', '0.08', '0.12']]

    results.append(run_check(c_val, K, s_list, mp.mpf('0.02'), mp.mpf('0.035'), label="(own triple 1)", K_check=K_check))
    results.append(run_check(c_val, K, s_list, mp.mpf('0.02'), mp.mpf('0.06'), label="(own triple 2, larger h)", K_check=K_check))
    results.append(run_check(c_val, K, s_list, mp.mpf('0.045'), mp.mpf('0.055'), label="(own triple 3, small h, larger y1)", K_check=K_check))

    print("\n" + "="*78)
    print("SUMMARY")
    print("="*78)
    all_ok = all(r[0] and r[1] for r in results)
    print("Bound (star-star) VIOLATED at any tested point?" , not all_ok)
    print("(False means: never violated across all own-chosen triples -- consistent")
    print(" with the target's own claim that the bound holds, just loose.)")
    for i, r in enumerate(results):
        print(f"  triple {i+1}: ratio LHS/RHS(tighter) = {mp.nstr(r[2]/r[3],6)}")
