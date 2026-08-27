"""
e05_approach_rate.py -- NEW numerical experiment: does Phi(s,g) approach
its g->infinity plateau EXPONENTIALLY (rate ~e^{-g c} = e^{-y/eps}, as the
required reading states, but only ever checks/uses at x=0) or with some
other (e.g. power-law) rate, AT GENERAL s -- and does the rate itself
look like it depends on s?

This bears directly on (U1): (U1) needs W(x,g) to converge to W_inf(x) as
g->infinity, LOCALLY UNIFORMLY in x. A necessary (far from sufficient)
prerequisite is that the convergence RATE not degrade wildly as x ranges
over a window -- this experiment is the first direct check, at general x,
of what that rate actually looks like (ancestor fronts checked eps->0
uniformity of the ALREADY-CONVERGED plateau profile, not the g->infinity
approach rate itself).

Method: fixed s, c; evaluate Phi(s,g) via the (validated, e01) direct
series summation at a grid g_i = g0 + i*dg; form consecutive differences
d_i = Phi(s,g_i) - Phi(s,g_{i+1}); look at ratios d_i/d_{i+1}.
  - pure exponential decay e^{-gc}  =>  ratio is CONSTANT = e^{dg*c}
  - power-law decay ~1/g^p          =>  ratio -> 1 as g grows (NOT e^{dg c})
  - exponential x algebraic prefactor (WKB-type) => ratio converges TO
    e^{dg*c} as g grows, approaching from above or below.
"""

import mpmath as mp
import e01_family_series as fs


def main():
    c_val = 100
    K = 320
    dps = 320
    mp.mp.dps = dps
    c = mp.mpf(c_val)

    print(f"=== e05_approach_rate :: c={c_val}, K={K}, dps={dps} ===")
    a, b = fs.build_series(c, K, dps)

    dg = mp.mpf('0.04')
    g0 = mp.mpf('0.06')
    n_g = 11
    gs = [g0 + dg * i for i in range(n_g)]
    expected_ratio = mp.e ** (dg * c)
    print(f"step dg={dg}, expected pure-exponential ratio e^(dg*c) = {mp.nstr(expected_ratio,12)}\n")

    for s0 in [mp.mpf('0.0'), mp.mpf('0.2'), mp.mpf('0.4')]:
        print(f"--- s = {mp.nstr(s0,4)} ---")
        Phi_of_g = fs.eval_Phi(a, s0, c)
        vals = [Phi_of_g(g) for g in gs]
        diffs = [vals[i] - vals[i + 1] for i in range(len(vals) - 1)]
        ratios = []
        for i in range(len(diffs) - 1):
            if diffs[i + 1] != 0:
                r = diffs[i] / diffs[i + 1]
                ratios.append(r)
                print(f"  g={mp.nstr(gs[i],4)}: diff={mp.nstr(diffs[i],8)}  ratio={mp.nstr(r,10)}  "
                      f"(ratio/expected={mp.nstr(r/expected_ratio,8)})")
        print()

    print("Reading: if the printed 'ratio' column trends toward the "
          "'expected pure-exponential ratio' above as g grows (rather than "
          "toward 1, which is what a power-law rate would show), the "
          "g->infinity approach is consistent with the exponential rate "
          "e^{-g c} = e^{-y/eps} at THIS s -- and if this holds similarly "
          "at every tested s, the rate itself does not show an obvious, "
          "gross x-dependence over the tested window (necessary but far "
          "from sufficient evidence toward (U1)).")


if __name__ == "__main__":
    main()
