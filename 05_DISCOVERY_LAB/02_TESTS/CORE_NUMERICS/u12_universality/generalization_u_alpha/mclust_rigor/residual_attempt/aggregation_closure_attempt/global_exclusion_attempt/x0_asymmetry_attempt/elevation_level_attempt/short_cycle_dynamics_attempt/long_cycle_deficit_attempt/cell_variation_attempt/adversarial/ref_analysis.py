"""
ref_analysis.py -- referee's full independent re-analysis, combining:
  (1) my own 9 freshly re-simulated cells (ref_grid_raw.npz, seeds
      20260840100+), reduced to point estimates HERE (not copied from
      ref_grid.log's printed dev%/z -- recomputed straight from the raw
      per-instance (n_far,cyc_far) arrays via ref_stats.ratio_estimator_sem,
      to keep one single audited code path).
  (2) the document's own reported values (ATTEMPT.md S2) for the 4 cells
      NOT independently re-measured (G1a, G2b, G3a, G4b) -- used ONLY to
      complete sub-group membership for the hybrid-table range test,
      clearly labeled, never presented as this review's own data.

Produces: point-estimate replication check (z_diff per remeasured cell),
hybrid-table pooled correlations (+Bonferroni, leave-one-out, partial corr,
Spearman), hybrid-table sub-group range tests, and a cluster-bootstrap
SEM cross-check for the cells that matter most to the argument.
"""
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ref_stats as rs
import ref_measure as rm

_HERE = os.path.dirname(os.path.abspath(__file__))

# --- document's own reported figures (ATTEMPT.md S2), for (a) replication
# z_diff comparison on the 9 cells I remeasured, and (b) hybrid-table filler
# for the 4 cells I did not remeasure. Transcribed verbatim, not recomputed. -
DOC = {
    # id: (b, c, rho, dev_own%, z_own, dev_b1%, z_b1, h2share%, h2sem_pp)
    "A":   (100, 1000, 0.7851, -8.06, -6.93, -3.32, -2.80, 41.2, 15.9),
    "G1a": (25, 1000, 0.3191, -3.79, -3.20, -1.35, -1.11, 35.5, 33.7),
    "G1b": (50, 1000, 0.5364, -2.37, -1.97, -1.64, -1.36, None, None),
    "G1d": (200, 1000, 0.9538, -19.64, -17.34, -2.41, -2.00, 12.3, 6.2),
    "G2a": (100, 200, 0.2633, -8.42, -6.95, -7.41, -6.31, 88.0, 18.8),
    "G2b": (100, 500, 0.5351, -8.06, -7.05, -1.77, -1.45, 21.9, 15.5),
    "G2d": (100, 2000, 0.9549, -20.31, -17.75, -1.26, -1.09, 6.2, 5.7),
    "G3a": (335, 300, 0.7850, -10.81, -8.96, -5.40, -4.56, 50.0, 12.3),
    "G3c": (50, 2000, 0.7877, -6.00, -5.16, -3.41, -2.93, 56.9, 22.3),
    "G3d": (1007, 100, 0.7851, -22.14, -15.54, -10.54, -7.65, 47.6, 6.9),
    "B":   (400, 100, 0.4571, -13.37, -11.08, -9.36, -7.56, 70.0, 11.2),
    "G4b": (80, 500, 0.4581, -8.64, -7.59, -5.57, -4.78, 64.5, 16.0),
    "G4c": (26, 1500, 0.4523, -4.27, -3.67, -1.98, -1.70, 46.5, 30.2),
}

REMEASURED = ["A", "G1b", "G1d", "G2a", "G2d", "G3c", "G3d", "B", "G4c"]
NOT_REMEASURED = ["G1a", "G2b", "G3a", "G4b"]


def main():
    npz = np.load(os.path.join(_HERE, "ref_grid_raw.npz"))
    mine = {}
    for cell_id in REMEASURED:
        b, c, rho, cpp_own, phi_ref_own, phi_ref_b1 = None, None, None, None, None, None
        meta = npz[f"{cell_id}_meta"]
        (b, c, n, threshold, rho, cpp_own, phi_ref_own, phi_ref_b1,
         logged_dev_own, logged_z_own, logged_sem_own,
         logged_dev_b1, logged_z_b1, logged_sem_b1,
         logged_share, logged_sem_share) = meta

        n_far_own = npz[f"{cell_id}_own_n_far"]
        cyc_far_own = npz[f"{cell_id}_own_cyc_far"]
        n_far_b1 = npz[f"{cell_id}_b1_n_far"]
        cyc_far_b1 = npz[f"{cell_id}_b1_cyc_far"]

        phi_own, sem_own = rm.ratio_estimator_sem(n_far_own, cyc_far_own)
        dev_own = 100.0 * (phi_own / phi_ref_own - 1.0)
        sem_own_pct = 100.0 * sem_own / phi_ref_own
        z_own = (phi_own - phi_ref_own) / sem_own

        phi_b1, sem_b1 = rm.ratio_estimator_sem(n_far_b1, cyc_far_b1)
        dev_b1 = 100.0 * (phi_b1 / phi_ref_b1 - 1.0)
        sem_b1_pct = 100.0 * sem_b1 / phi_ref_b1
        z_b1 = (phi_b1 - phi_ref_b1) / sem_b1

        excluded = not (dev_own < 0 and abs(z_own) >= 2)
        share, sem_share = (None, None)
        if not excluded:
            share, sem_share = rm.h2_share(dev_own, dev_b1, sem_own_pct, sem_b1_pct)

        mine[cell_id] = dict(b=b, c=c, rho=rho, dev_own=dev_own, z_own=z_own,
                              sem_own_pct=sem_own_pct, dev_b1=dev_b1, z_b1=z_b1,
                              sem_b1_pct=sem_b1_pct, share=share, sem_share=sem_share,
                              excluded=excluded,
                              n_far_own=n_far_own, cyc_far_own=cyc_far_own,
                              n_far_b1=n_far_b1, cyc_far_b1=cyc_far_b1)

    print("=" * 78)
    print("1. REPLICATION CHECK: my recomputed point estimates vs DOC's reported")
    print("=" * 78)
    print(f"{'id':6s} {'my dev_own%':>12s} {'doc dev_own%':>13s} {'z_diff':>8s}  "
          f"{'my dev_b1%':>11s} {'doc dev_b1%':>12s} {'z_diff':>8s}  "
          f"{'my share%':>10s} {'doc share%':>11s}")
    for cid in REMEASURED:
        m = mine[cid]
        d = DOC[cid]
        _, _, z_diff_own = rs.pairwise_z(d[3], abs(d[3]) / abs(d[4]), m['dev_own'], m['sem_own_pct'])
        _, _, z_diff_b1 = rs.pairwise_z(d[5], abs(d[5]) / abs(d[6]), m['dev_b1'], m['sem_b1_pct'])
        my_share_s = f"{m['share']*100:.1f}" if m['share'] is not None else "EXCL"
        doc_share_s = f"{d[7]:.1f}" if d[7] is not None else "EXCL"
        print(f"{cid:6s} {m['dev_own']:12.3f} {d[3]:13.2f} {z_diff_own:8.2f}  "
              f"{m['dev_b1']:11.3f} {d[5]:12.2f} {z_diff_b1:8.2f}  "
              f"{my_share_s:>10s} {doc_share_s:>11s}")

    print()
    print("=" * 78)
    print("2. HYBRID TABLE (my 9 remeasured + doc's 4 not-remeasured cells)")
    print("=" * 78)
    hybrid = {}
    for cid in REMEASURED:
        m = mine[cid]
        # NOTE: m['share']/m['sem_share'] from rm.h2_share are on a FRACTION
        # (0-1) scale (dev_b1_pct/dev_own_pct is a plain ratio of two already-
        # percent numbers); DOC's stored values are on a PERCENT (0-100)
        # scale. Multiply by 100 here so hybrid table units match DOC's.
        share_pct = m['share'] * 100.0 if m['share'] is not None else None
        sem_share_pct = m['sem_share'] * 100.0 if m['sem_share'] is not None else None
        hybrid[cid] = dict(b=m['b'], c=m['c'], rho=m['rho'], share=share_pct,
                            sem_share=sem_share_pct, excluded=m['excluded'], source="mine")
    for cid in NOT_REMEASURED:
        d = DOC[cid]
        hybrid[cid] = dict(b=d[0], c=d[1], rho=d[2], share=d[7], sem_share=d[8],
                            excluded=(d[7] is None), source="doc")
    for cid, h in hybrid.items():
        s = f"{h['share']:.1f}%" if not h['excluded'] else "EXCLUDED"
        print(f"  {cid:6s} b={h['b']:6.0f} c={h['c']:6.0f} rho={h['rho']:.4f}  "
              f"share={s:>10s}  [{h['source']}]")

    defined = {k: v for k, v in hybrid.items() if not v['excluded']}
    ids = list(defined.keys())
    b_arr = np.array([defined[i]['b'] for i in ids], dtype=float)
    c_arr = np.array([defined[i]['c'] for i in ids], dtype=float)
    rho_arr = np.array([defined[i]['rho'] for i in ids], dtype=float)
    share_arr = np.array([defined[i]['share'] for i in ids], dtype=float)

    print(f"\n  n(defined)={len(ids)}  (excluded: {[k for k,v in hybrid.items() if v['excluded']]})")

    print()
    print("=" * 78)
    print("3. HYBRID pooled correlations + Bonferroni + Spearman + leave-one-out")
    print("=" * 78)
    ps = []
    for name, cov in [("rho", rho_arr), ("log10(c)", np.log10(c_arr)), ("log10(b)", np.log10(b_arr))]:
        res = rs.pearson_r_t_p(cov, share_arr, n_perm=50000, perm_seed=7)
        sr = rs.spearman_r(cov, share_arr)
        ps.append(res['p_param'])
        print(f"  {name:10s} Pearson r={res['r']:+.4f} t={res['t']:+.4f} df={res['df']} "
              f"p={res['p_param']:.4f} (perm p={res['p_perm']:.4f})   Spearman r={sr:+.4f}")
    bonf = rs.bonferroni(ps)
    print(f"  Bonferroni (m=3) alpha_adj={bonf['alpha_adj']:.4f}  survives={bonf['survives']}")

    print("\n  Leave-one-out on rho correlation:")
    for i, name in enumerate(ids):
        mask = np.ones(len(ids), dtype=bool); mask[i] = False
        res = rs.pearson_r_t_p(rho_arr[mask], share_arr[mask], n_perm=0)
        print(f"    drop {name:6s}: r={res['r']:+.4f} p={res['p_param']:.4f}")

    pc_b = rs.partial_corr(np.log10(b_arr), share_arr, rho_arr)
    pc_c = rs.partial_corr(np.log10(c_arr), share_arr, rho_arr)
    print(f"\n  partial r(log10(b),share|rho) = {pc_b:+.4f}")
    print(f"  partial r(log10(c),share|rho) = {pc_c:+.4f}")

    print()
    print("=" * 78)
    print("4. HYBRID sub-group range tests")
    print("=" * 78)
    groups = {
        "G1": ["A", "G1a", "G1b", "G1d"],
        "G2": ["A", "G2a", "G2b", "G2d"],
        "G3": ["A", "G3a", "G3c", "G3d"],
        "G4": ["B", "G4b", "G4c"],
    }
    for g, members in groups.items():
        avail = [m for m in members if m in defined]
        sh = np.array([defined[m]['share'] for m in avail])
        se = np.array([defined[m]['sem_share'] for m in avail])
        r = rs.subgroup_range_ztest(sh, se)
        excl_note = "" if len(avail) == len(members) else f"  (missing: {[m for m in members if m not in avail]})"
        print(f"  {g}: members={avail} range={r['range_pp']:.1f}pp z={r['z']:+.2f} "
              f"max={avail[r['imax']]} min={avail[r['imin']]}{excl_note}")

    print()
    print("=" * 78)
    print("5. Cluster-bootstrap SEM cross-check (G2a, G2d, G1b, A -- own-b condition)")
    print("=" * 78)
    for cid in ["G2a", "G2d", "G1b", "A"]:
        m = mine[cid]
        boot = rs.cluster_bootstrap_ratio(m['n_far_own'], m['cyc_far_own'], B=4000, seed=hash(cid) % (2**31))
        phi_ref = None
        print(f"  {cid}: delta-method SEM(phi_far)={m['sem_own_pct']*abs(1):.6f}(pct scale n/a) ; "
              f"bootstrap sem(phi_far) vs delta-method sem(phi_far) ratio check below")
        n_far_own = m['n_far_own']; cyc_far_own = m['cyc_far_own']
        phi_hat, sem_delta = rm.ratio_estimator_sem(n_far_own, cyc_far_own)
        print(f"      phi_far={phi_hat:.6f}  delta-SEM={sem_delta:.6f}  "
              f"bootstrap-SEM={boot['sem']:.6f}  ratio(boot/delta)={boot['sem']/sem_delta:.4f}")


if __name__ == "__main__":
    main()
