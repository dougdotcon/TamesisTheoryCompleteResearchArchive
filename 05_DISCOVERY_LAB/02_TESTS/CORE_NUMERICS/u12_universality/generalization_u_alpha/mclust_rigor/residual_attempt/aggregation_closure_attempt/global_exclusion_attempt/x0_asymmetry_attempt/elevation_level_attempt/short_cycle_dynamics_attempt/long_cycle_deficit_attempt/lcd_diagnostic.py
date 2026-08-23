"""
lcd_diagnostic.py -- generalized diagnostic split, reusing sc_engine.py and
sc_formula.py from the parent directory (short_cycle_dynamics_attempt/)
UNMODIFIED, by import. No new engine is written -- per the mandate, reusing
already-validated infrastructure (sc_engine_selftest.log, all 5 groups OK)
is normal research continuity, not adversarial contamination.

Unlike sc_diagnostic.py (which derives its bin edges from b as [b,2b,5b,20b,
inf]), this script takes CALLER-SUPPLIED ABSOLUTE bin edges, so the same
numeric L-windows can be measured at b=1 (plain M-U) as were measured at the
original b in short_cycle_dynamics_attempt -- the whole point of T1/T3
(DERIVATION_PREREG.md SS3).

T0 (engine sanity for b=1) is also implemented here, as a fast deterministic
check that must pass before T1/T3 numbers are trusted.
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sc_engine as eng
import sc_formula as fm


def t0_engine_sanity(n=65536, c=1000, ninstances=20, seed_seq=20260827000, log=print):
    """b=1 must reduce R_mask exactly to seed_mask (no shadowing at all), and
    rho_measured must match c/n (the b=1 special case of 1-(1-c/n)^b)."""
    log(f"lcd_diagnostic.py T0 -- b=1 engine sanity, n={n} c={c}, "
        f"{ninstances} instances, seed={seed_seq}")
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(ninstances)
    viol_Rmask = 0
    rho_vals = []
    for i in range(ninstances):
        rng = np.random.default_rng(children[i])
        pi = eng.build_pi(n, rng)
        seed_mask = eng.build_seeds(n, c, rng)
        R_mask = eng.build_R_mask(n, 1, pi, seed_mask)
        if not np.array_equal(R_mask, seed_mask):
            viol_Rmask += 1
        rho_vals.append(R_mask.mean())
    rho_meas = np.mean(rho_vals)
    rho_sem = np.std(rho_vals, ddof=1) / np.sqrt(len(rho_vals))
    rho_formula = c / n
    z = (rho_meas - rho_formula) / rho_sem if rho_sem > 0 else 0.0
    ok = (viol_Rmask == 0) and (abs(z) < 4.0)
    log(f"  R_mask == seed_mask exactly at b=1: violations={viol_Rmask}/{ninstances}  "
        f"{'OK' if viol_Rmask == 0 else 'FAIL'}")
    log(f"  rho_formula (=c/n) = {rho_formula:.6f}   rho_meas = {rho_meas:.6f}+-{rho_sem:.6f}  "
        f"z={z:+.2f}  {'OK' if abs(z) < 4.0 else 'FAIL'}")
    log(f"  T0 {'PASSED' if ok else 'FAILED'}")
    return ok


def measure_cell(n, b, c, N, seed_seq, edges, b_split=None, log=print, log_every=200):
    """Same measurement logic as sc_diagnostic.measure_cell, but with
    CALLER-SUPPLIED absolute bin edges (a list, e.g. [100,200,500,2000,np.inf])
    instead of edges derived from b. b_split (default: b) is the threshold
    used for the short-untouched/long split and the su sanity check; it is
    independent of the fine bin edges."""
    if b_split is None:
        b_split = b
    ss = np.random.SeedSequence(seed_seq)
    children = ss.spawn(N)

    nbins = len(edges)

    n_short_untouched = np.zeros(N, dtype=np.int64)
    cyc_short_untouched = np.zeros(N, dtype=np.int64)
    n_long = np.zeros(N, dtype=np.int64)
    cyc_long = np.zeros(N, dtype=np.int64)
    n_Rc = np.zeros(N, dtype=np.int64)
    cyc_Rc = np.zeros(N, dtype=np.int64)
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
        short_mask = cyc_len <= b_split

        su_mask = short_mask & Rc_mask
        long_Rc_mask = (~short_mask) & Rc_mask

        n_short_untouched[i] = su_mask.sum()
        cyc_short_untouched[i] = cyclic[su_mask].sum()
        n_long[i] = long_Rc_mask.sum()
        cyc_long[i] = cyclic[long_Rc_mask].sum()
        n_Rc[i] = Rc_mask.sum()
        cyc_Rc[i] = cyclic[Rc_mask].sum()
        rho_meas[i] = R_mask.mean()

        lo = edges[0]
        n_bin[i, 0] = 0
        cyc_bin[i, 0] = 0
        for k in range(1, nbins):
            hi = edges[k]
            m = Rc_mask & (cyc_len > lo) & (cyc_len <= hi)
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
        rho_meas=rho_meas,
        n_bin=n_bin, cyc_bin=cyc_bin, edges=edges,
    )


def summarize(res, n, b, c):
    with np.errstate(invalid="ignore", divide="ignore"):
        r_su = res["cyc_short_untouched"] / res["n_short_untouched"]
        r_long = res["cyc_long"] / res["n_long"]
        r_Rc = res["cyc_Rc"] / res["n_Rc"]

    def m_sem(x):
        x = x[np.isfinite(x)]
        return x.mean(), x.std(ddof=1) / np.sqrt(len(x)), len(x)

    out = {}
    out["rho"] = m_sem(res["rho_meas"])
    out["phi_su"] = m_sem(r_su)
    out["phi_long"] = m_sem(r_long)
    out["phi_Rc"] = m_sem(r_Rc)
    out["n_su_total"] = int(res["n_short_untouched"].sum())
    out["n_long_total"] = int(res["n_long"].sum())
    out["n_Rc_total"] = int(res["n_Rc"].sum())
    out["phi_U_cpp"] = fm.phi_U(fm.c_double_prime(b, c, n))

    edges = res["edges"]
    nbins = len(edges)
    bin_stats = []
    lo = edges[0]
    for k in range(1, nbins):
        hi = edges[k]
        with np.errstate(invalid="ignore", divide="ignore"):
            r = res["cyc_bin"][:, k] / res["n_bin"][:, k]
        mean, sem, cnt = m_sem(r)
        total_pts = int(res["n_bin"][:, k].sum())
        bin_stats.append((lo, hi, mean, sem, cnt, total_pts))
        lo = hi
    out["bin_stats"] = bin_stats
    return out


def report(s, n, b, c, log=print):
    log(f"rho: measured {s['rho'][0]:.5f} +- {s['rho'][1]:.5f} (n={s['rho'][2]})  "
        f"vs formula {fm.rho_of(b,c,n):.5f}")
    log(f"phi(cyclic | short & untouched) = {s['phi_su'][0]:.6f} +- {s['phi_su'][1]:.6f} "
        f"(pts={s['n_su_total']})   [sanity, should be 1.0]")
    log(f"phi(cyclic | long, x0 in R^c)   = {s['phi_long'][0]:.6f} +- {s['phi_long'][1]:.6f} "
        f"(pts={s['n_long_total']})")
    log(f"phi(cyclic | x0 in R^c), overall = {s['phi_Rc'][0]:.6f} +- {s['phi_Rc'][1]:.6f} "
        f"(pts={s['n_Rc_total']})")
    log(f"phi_U(c'') [comparison target]   = {s['phi_U_cpp']:.6f}")
    if s['phi_long'][1] > 0:
        z_long = (s['phi_long'][0] - s['phi_U_cpp']) / s['phi_long'][1]
        dev_long = 100 * (s['phi_long'][0] / s['phi_U_cpp'] - 1)
        log(f"  phi_long - phi_U(c'') = {s['phi_long'][0]-s['phi_U_cpp']:+.6f}  "
            f"({dev_long:+.3f}% relative)  z={z_long:+.2f}")

    log("\n--- cycle-length-binned phi(cyclic | x0 in R^c, L in bin), vs phi_U(c'') ---")
    for (lo, hi, mean, sem, cnt, total_pts) in s["bin_stats"]:
        hi_str = f"{hi:.0f}" if np.isfinite(hi) else "inf"
        if sem > 0 and np.isfinite(mean):
            dev = 100 * (mean / s["phi_U_cpp"] - 1)
            z = (mean - s["phi_U_cpp"]) / sem
            log(f"  L in ({lo:.0f},{hi_str}]: phi={mean:.6f}+-{sem:.6f}  "
                f"(instances={cnt}, pts={total_pts})  dev={dev:+.2f}%  z={z:+.2f}")
        else:
            log(f"  L in ({lo:.0f},{hi_str}]: insufficient data (pts={total_pts})")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "t0"

    if mode == "t0":
        ok = t0_engine_sanity()
        sys.exit(0 if ok else 1)

    elif mode == "t1":
        # T1 cells: (n, b=1, c, N, seed, edges)
        cellname = sys.argv[2]
        cells = {
            "A": (65536, 1000, 2500, 20260827001, [100, 200, 500, 2000, np.inf]),
            "B": (65536, 100, 2500, 20260827002, [400, 800, 2000, 8000, np.inf]),
            "C": (65536, 150, 2500, 20260827003, [200, 400, 1000, 4000, np.inf]),
        }
        n, c, N, seed, edges = cells[cellname]
        b = 1
        print(f"lcd_diagnostic.py T1 cell {cellname} -- n={n} b={b} c={c}, N={N}, "
              f"seed={seed}, edges={edges}")
        res = measure_cell(n, b, c, N, seed, edges, log=print, log_every=max(1, N // 10))
        s = summarize(res, n, b, c)
        print("\n--- summary ---")
        report(s, n, b, c)

    elif mode == "t3":
        # T3: target cell at ORIGINAL b=100, sub-binned far tail by L/n fraction
        n, b, c = 65536, 100, 1000
        N = 3000
        seed = 20260827020
        edges = [2000, n / 8, n / 4, n / 2, n]
        print(f"lcd_diagnostic.py T3 -- n={n} b={b} c={c}, N={N}, seed={seed}, "
              f"L/n subbins of far tail, edges={edges}")
        res = measure_cell(n, b, c, N, seed, edges, log=print, log_every=max(1, N // 10))
        s = summarize(res, n, b, c)
        print("\n--- summary ---")
        report(s, n, b, c)

    else:
        print(f"unknown mode {mode}")
        sys.exit(2)
