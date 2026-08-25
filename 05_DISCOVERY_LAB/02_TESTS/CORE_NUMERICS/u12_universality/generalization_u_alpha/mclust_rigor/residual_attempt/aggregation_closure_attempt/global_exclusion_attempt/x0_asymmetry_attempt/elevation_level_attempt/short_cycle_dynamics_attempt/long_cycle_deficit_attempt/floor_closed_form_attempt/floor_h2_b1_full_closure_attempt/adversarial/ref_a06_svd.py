#!/usr/bin/env python3
"""
REFEREE test R-E: independent check of the front's SS3.4 separability
finding (SVD near-rank-2 of the converged Phi(s,g) surface), on the
referee's OWN solver output (different discretization family), plus an
assessment of WHY the surface is near-rank-2:

  boundary-layer + plateau structure:  Phi(s,g) ~ e^{-cg}*1 + (1-e^{-cg})*F(s)
  is ALREADY a rank-2 surface; the diagnostic below measures how much of
  the claimed rank-2 dominance is explained by this mundane explicit
  ansatz (no SVD fitting at all), and how the SVD numbers depend on
  grid resolution and on the region (with/without the g<~1/c layer).

Deterministic (no seeds).
"""
import json
import numpy as np

C = 1000.0
LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    LOG.append(line)

def svd_report(Phi, name):
    sv = np.linalg.svd(Phi, compute_uv=False)
    tot = np.sum(sv**2)
    cum = np.cumsum(sv**2) / tot
    log(f"  {name}:")
    log(f"    shape={Phi.shape}  sigma1..5 = "
        + " ".join(f"{x:.3e}" for x in sv[:5]))
    log(f"    energy: rank-1 {100*cum[0]:.5f}%   rank-2 {100*cum[1]:.8f}%   "
        f"rank-3 {100*cum[2]:.10f}%")
    return cum

def rank2_row0_err(Phi):
    U, sv, Vt = np.linalg.svd(Phi, full_matrices=False)
    rec = (U[:, :2] * sv[:2]) @ Vt[:2, :]
    r0 = Phi[0, :]
    return float(np.max(np.abs(rec[0, :] - r0)) / np.max(np.abs(r0)))

results = {}
for tag, fn in [("h=1e-3 (front's f05 region, s<=0.5 x g<=0.4)",
                 'ref_a05_grid_h0.001.npz'),
                ("h=5e-4 (same region, finer)", 'ref_a05_grid_h0.0005.npz'),
                ("h=2.5e-5 (fine ladder grid, s<=0.362 x g<=0.031)",
                 'ref_a05_grid_fine.npz')]:
    d = np.load(fn)
    Phi, s, g = d['Phi'], d['s'], d['g']
    log("=" * 72)
    log(f"GRID: {tag}")
    log("=" * 72)
    cum = svd_report(Phi, "full grid")
    log(f"    rank-2 reconstruction of the target row Phi(0,.): max rel err"
        f" = {rank2_row0_err(Phi):.2e}")
    # region dependence: cut away the g <~ 1/c boundary layer
    jcut = np.searchsorted(g, 0.01)
    cum_nl = svd_report(Phi[:, jcut:], "g >= 0.01 only (layer removed)")
    # explicit mundane rank-2 ansatz: e^{-cg} + (1-e^{-cg}) F(s),
    # F(s) taken as the profile at the largest available g (no fitting):
    F = (Phi[:, -1] - np.exp(-C * g[-1])) / (1 - np.exp(-C * g[-1]))
    ansatz = np.exp(-C * g)[None, :] \
        + (1 - np.exp(-C * g))[None, :] * F[:, None]
    resid = Phi - ansatz
    rel = np.linalg.norm(resid) / np.linalg.norm(Phi)
    relmax = np.abs(resid).max()
    log(f"    explicit ansatz e^-cg + (1-e^-cg)F(s), F = profile at "
        f"g={g[-1]:.3f} (NO fitting):")
    log(f"      relative Frobenius residual = {rel:.3e}   max abs residual ="
        f" {relmax:.3e}")
    log(f"      energy captured by this fixed rank-2 surface = "
        f"{100*(1-rel**2):.6f}%")
    # s-shape similarity across g (the front's 'direct inspection'):
    spreads = []
    for gv in (0.01, 0.03):
        j = np.searchsorted(g, gv)
        if j < len(g):
            col = Phi[:, j]
            spreads.append((gv, float(col.max() - col.min())))
    for gv in (0.05, 0.1, 0.2, 0.3):
        j = np.searchsorted(g, gv)
        if j < len(g):
            col = Phi[:, j]
            spreads.append((gv, float(col.max() - col.min())))
    log("    spread over s of Phi(.,g) (front reported ~3.1e-2 matching to"
        " 3 sig figs across g at its h=1e-3):")
    log("      " + "  ".join(f"g={gv:g}: {sp:.4e}" for gv, sp in spreads))
    results[tag] = dict(rank1=float(cum[0]), rank2=float(cum[1]),
                        rank1_nolayer=float(cum_nl[0]),
                        rank2_nolayer=float(cum_nl[1]),
                        ansatz_rel_resid=rel, ansatz_energy=float(1 - rel**2))
    log("")

json.dump(results, open('ref_a06_results.json', 'w'), indent=1)
with open('ref_a06_svd.log', 'w') as f:
    f.write("\n".join(LOG) + "\n")
log("done.")
