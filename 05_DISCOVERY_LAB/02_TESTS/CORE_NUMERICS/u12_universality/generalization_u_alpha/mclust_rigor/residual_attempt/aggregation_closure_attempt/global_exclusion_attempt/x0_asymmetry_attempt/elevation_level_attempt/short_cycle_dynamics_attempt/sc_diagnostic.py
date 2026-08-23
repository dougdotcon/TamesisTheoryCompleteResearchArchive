"""
sc_diagnostic.py -- T1, the diagnostic split.

For each instance: build the mechanism, compute the cyclic mask (all n
points), the R mask, and the pi-cycle length of every point. Then split the
R^c (x0 not in R) population by whether x0's OWN pi-cycle has length <= b
("short") or > b ("long"), and separately accumulate the cyclic fraction in
each bucket.

Because the whole functional graph and the whole pi-cycle-length array are
available per instance, this measures phi(cyclic | R^c, short) and
phi(cyclic | R^c, long) DIRECTLY, using every R^c point of the instance as a
sample of "x0" -- no separate per-x0 walk needed, and no formula on either
side except in the reporting comparison at the end.
"""

import sys
import time
import numpy as np
import sc_engine as eng
import sc_formula as fm


def bin_edges(b):
    """Cycle-length bins for the extra diagnostic: (b,2b], (2b,5b], (5b,20b],
    (20b, inf). Fixed functional form of the bin edges, chosen before seeing
    any data (a multiplicative grid is the natural scale given L ranges over
    orders of magnitude)."""
    return [b, 2 * b, 5 * b, 20 * b, np.inf]


def measure_cell(n, b, c, N, seed_seq, log=print, log_every=200):
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(N)

    edges = bin_edges(b)
    nbins = len(edges)

    # accumulators, one entry per instance
    n_short_untouched = np.zeros(N, dtype=np.int64)
    cyc_short_untouched = np.zeros(N, dtype=np.int64)
    n_long = np.zeros(N, dtype=np.int64)
    cyc_long = np.zeros(N, dtype=np.int64)
    n_Rc = np.zeros(N, dtype=np.int64)
    cyc_Rc = np.zeros(N, dtype=np.int64)
    n_touched_short = np.zeros(N, dtype=np.int64)  # sanity: should be x0 in R, not R^c
    rho_meas = np.zeros(N, dtype=float)
    n_bin = np.zeros((N, nbins), dtype=np.int64)
    cyc_bin = np.zeros((N, nbins), dtype=np.int64)

    t0 = time.time()
    for i in range(N):
        rng = np.random.default_rng(children[i])
        inst = eng.build_instance(n, b, c, rng)
        pi, R_mask, f = inst["pi"], inst["R_mask"], inst["f"]
        cyclic = eng.cyclic_mask_peeling(f)
        cyc_len = eng.pi_cycle_lengths(pi)

        Rc_mask = ~R_mask
        short_mask = cyc_len <= b

        # "short & untouched" == "short & in R^c" (by construction: if a short
        # cycle is touched, EVERY point on it including x0 is pulled into R --
        # DERIVATION_PREREG.md §1.3 -- so short & R^c implies untouched).
        su_mask = short_mask & Rc_mask
        long_Rc_mask = (~short_mask) & Rc_mask

        n_short_untouched[i] = su_mask.sum()
        cyc_short_untouched[i] = cyclic[su_mask].sum()
        n_long[i] = long_Rc_mask.sum()
        cyc_long[i] = cyclic[long_Rc_mask].sum()
        n_Rc[i] = Rc_mask.sum()
        cyc_Rc[i] = cyclic[Rc_mask].sum()
        n_touched_short[i] = (short_mask & R_mask).sum()
        rho_meas[i] = R_mask.mean()

        lo = b
        for k in range(nbins):
            hi = edges[k]
            m = long_Rc_mask & (cyc_len > lo) & (cyc_len <= hi)
            n_bin[i, k] = m.sum()
            cyc_bin[i, k] = cyclic[m].sum()
            lo = hi

        if log_every and (i + 1) % log_every == 0:
            elapsed = time.time() - t0
            log(f"    [{i+1}/{N}] elapsed={elapsed:.1f}s "
                f"({elapsed/(i+1)*1000:.1f}ms/instance)")

    return dict(
        n_short_untouched=n_short_untouched, cyc_short_untouched=cyc_short_untouched,
        n_long=n_long, cyc_long=cyc_long,
        n_Rc=n_Rc, cyc_Rc=cyc_Rc,
        n_touched_short=n_touched_short, rho_meas=rho_meas,
        n_bin=n_bin, cyc_bin=cyc_bin, edges=edges,
    )


def summarize(res, n, b, c):
    # per-instance ratios (weighted correctly per-instance, then averaged
    # across instances -- standard "ratio of sums per instance, then mean"
    # estimator used throughout this lineage)
    with np.errstate(invalid="ignore", divide="ignore"):
        r_su = res["cyc_short_untouched"] / res["n_short_untouched"]
        r_long = res["cyc_long"] / res["n_long"]
        r_Rc = res["cyc_Rc"] / res["n_Rc"]
    N = len(res["rho_meas"])

    def m_sem(x):
        x = x[np.isfinite(x)]
        return x.mean(), x.std(ddof=1) / np.sqrt(len(x)), len(x)

    out = {}
    out["rho"] = m_sem(res["rho_meas"])
    out["phi_su"] = m_sem(r_su)       # should be 1.0 -- sanity check
    out["phi_long"] = m_sem(r_long)
    out["phi_Rc"] = m_sem(r_Rc)
    out["n_su_total"] = int(res["n_short_untouched"].sum())
    out["n_long_total"] = int(res["n_long"].sum())
    out["n_Rc_total"] = int(res["n_Rc"].sum())
    out["n_touched_short_total"] = int(res["n_touched_short"].sum())
    out["phi_U_cpp"] = fm.phi_U(fm.c_double_prime(b, c, n))
    out["w_short_formula"] = fm.w_short(b, c, n)
    out["w_short_measured"] = out["n_su_total"] / max(out["n_Rc_total"], 1)

    edges = res["edges"]
    nbins = len(edges)
    bin_stats = []
    lo = b
    for k in range(nbins):
        hi = edges[k]
        with np.errstate(invalid="ignore", divide="ignore"):
            r = res["cyc_bin"][:, k] / res["n_bin"][:, k]
        mean, sem, cnt = m_sem(r)
        total_pts = int(res["n_bin"][:, k].sum())
        bin_stats.append((lo, hi, mean, sem, cnt, total_pts))
        lo = hi
    out["bin_stats"] = bin_stats
    return out


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    cell_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    seed_base = int(sys.argv[3]) if len(sys.argv) > 3 else 20260825901

    cells = [
        (65536, 100, 1000),  # target cell
        (65536, 400, 100),   # mild cell, phi_REDB already close
        (65536, 200, 150),   # mid cell
    ]
    n, b, c = cells[cell_idx]

    print(f"sc_diagnostic.py T1 -- cell n={n} b={b} c={c}, N={N}, seed={seed_base}")
    res = measure_cell(n, b, c, N, seed_base, log=print, log_every=max(1, N // 10))
    s = summarize(res, n, b, c)

    print("\n--- summary ---")
    print(f"rho: measured {s['rho'][0]:.5f} +- {s['rho'][1]:.5f} (n={s['rho'][2]})  "
          f"vs formula {fm.rho_of(b,c,n):.5f}")
    print(f"phi(cyclic | short & untouched)  = {s['phi_su'][0]:.6f} +- {s['phi_su'][1]:.6f} "
          f"(n_instances_with_data={s['phi_su'][2]}, total short-untouched pts={s['n_su_total']})"
          f"   [must be 1.0 -- sanity check]")
    print(f"phi(cyclic | long, x0 in R^c)     = {s['phi_long'][0]:.6f} +- {s['phi_long'][1]:.6f} "
          f"(total long-Rc pts={s['n_long_total']})")
    print(f"phi(cyclic | x0 in R^c), overall  = {s['phi_Rc'][0]:.6f} +- {s['phi_Rc'][1]:.6f} "
          f"(total Rc pts={s['n_Rc_total']})")
    print(f"phi_U(c'')  [phi_REDB's conditional]         = {s['phi_U_cpp']:.6f}")
    if s['phi_long'][1] > 0:
        z_long = (s['phi_long'][0] - s['phi_U_cpp']) / s['phi_long'][1]
        print(f"  phi_long - phi_U(c'') = {s['phi_long'][0]-s['phi_U_cpp']:+.6f}  "
              f"({100*(s['phi_long'][0]/s['phi_U_cpp']-1):+.3f}% relative)  z={z_long:+.2f}")
    if s['phi_Rc'][1] > 0:
        z_full = (s['phi_Rc'][0] - s['phi_U_cpp']) / s['phi_Rc'][1]
        print(f"  phi_Rc(all) - phi_U(c'') = {s['phi_Rc'][0]-s['phi_U_cpp']:+.6f}  "
              f"({100*(s['phi_Rc'][0]/s['phi_U_cpp']-1):+.3f}% relative)  z={z_full:+.2f}")
    print(f"w_short: formula={s['w_short_formula']:.6f}  measured={s['w_short_measured']:.6f}")
    print(f"touched-short-cycle points seen (sanity, should be x0 in R not R^c): "
          f"{s['n_touched_short_total']}")

    print("\n--- cycle-length-binned phi(cyclic | x0 in R^c, L in bin), vs phi_U(c'') ---")
    for (lo, hi, mean, sem, cnt, total_pts) in s["bin_stats"]:
        hi_str = f"{hi:.0f}" if np.isfinite(hi) else "inf"
        if sem > 0 and np.isfinite(mean):
            dev = 100 * (mean / s["phi_U_cpp"] - 1)
            z = (mean - s["phi_U_cpp"]) / sem
            print(f"  L in ({lo:.0f},{hi_str}]: phi={mean:.6f}+-{sem:.6f}  "
                  f"(instances={cnt}, pts={total_pts})  dev={dev:+.2f}%  z={z:+.2f}")
        else:
            print(f"  L in ({lo:.0f},{hi_str}]: insufficient data (pts={total_pts})")
