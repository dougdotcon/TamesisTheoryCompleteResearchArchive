#!/usr/bin/env python3
"""
REFEREE test R-D: an INDEPENDENT numerical solution of the stated SS5
system, built from the prose equations only (no line of the front's
f04/f06 or the parent's solve_2d_system.py was read):

    dPhi/ds - dPhi/dg = c (Phi - W),   dPsi/ds = c (Psi - W)
    W = g Avg_g[Phi(s,.)] + (1-s-g) Psi,   Avg_g = (1/g) int_0^g Phi dg'
    Phi(s,0) = 1,  target Phi(0,t0).

METHOD (deliberately different from the front's described scheme):
renewal/integral form marched on a uniform (s,g) grid.
  Phi(s,g) = e^{-ch} Phi(s+h, g-h) + int_0^h c e^{-cu} W(s+u, g-u) du
  Psi(s,g) = e^{-ch} Psi(s+h, g)   + int_0^h c e^{-cu} W(s+u, g)   du
with W linearly interpolated along each step (second-order local
quadrature under the exact exponential weight), cumulative-trapezoid Avg_g,
and an outer JACOBI fixed-point iteration (both marches use the previous
iterate's W).  Closures, both with error weight ~ e^{-c s^2/2} (< 1e-30
for the margins used): Psi(s_top, .) = 0 and a ghost top row
Phi(s_top, g) = e^{-c g}.  (1-s-g) is clipped at >= 0 (only relevant in a
region reached with probability < e^{-400}).

Self-tests:
  (i)  W forced to 0  ->  Phi must equal e^{-c g} to machine precision;
  (ii) small-g behaviour of Psi:  Psi(0,g)/g -> psi1(0) = 39.6333;
  (iii) small-t0 row vs the exact closed-form series (ref_a02).
Then: grid-refinement ladder + Richardson at t0 = 0.01/0.02/0.03 (and a
separate ladder for t0 = 0.09), cutoff-margin insensitivity, and a
big-domain run for the SVD diagnostic (ref_a06).
Deterministic (no seeds).
"""
import json
import numpy as np
from scipy.signal import lfilter

C = 1000.0
LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    LOG.append(line)


def solve(h, G, M, tol=1e-11, max_iter=800, force_W_zero=False,
          want_grid=False, quiet=True):
    """Solve on s in [0, M+2G], g in [0, G] with step h.

    M = margin beyond which Psi is cut off to 0 (error ~ e^{-c M^2/2}).
    Returns dict with Phi row at s=0, iteration count, final residual,
    and optionally the full Phi grid."""
    Ng = int(round(G / h))
    Ns = int(round((M + 2 * G) / h))
    g = np.arange(Ng + 1) * h
    s = np.arange(Ns + 1) * h
    e = np.exp(-C * h)
    # exponential-weight linear-interp quadrature weights:
    #   int_0^h c e^{-cu} [W0 + (u/h)(W1-W0)] du = alpha W0 + beta W1
    kappa = (1.0 - e * (1.0 + C * h)) / (C * h)
    alpha = (1.0 - e) - kappa
    beta = kappa
    coef = np.clip(1.0 - s[:, None] - g[None, :], 0.0, None)  # (1-s-g)+
    Phi = np.exp(-C * g)[None, :] * np.ones((Ns + 1, 1))
    Psi = np.zeros((Ns + 1, Ng + 1))
    ghost = np.exp(-C * g)          # top-row closure for the Phi march
    trap_w = np.ones(Ng + 1); trap_w[0] = 0.5   # cumulative trapezoid pieces
    it_hist = []
    for it in range(max_iter):
        if force_W_zero:
            W = np.zeros_like(Phi)
        else:
            # Avg_g[Phi](s, g_j) = (1/g_j) int_0^{g_j} Phi dg'
            csum = np.cumsum((Phi[:, :-1] + Phi[:, 1:]) * (h / 2), axis=1)
            Avg = np.empty_like(Phi)
            Avg[:, 0] = Phi[:, 0]                      # limit g->0
            Avg[:, 1:] = csum / g[1:][None, :]
            W = g[None, :] * Avg + coef * Psi
        # --- Psi march: backward in s at fixed g (first-order recurrence,
        #     solved exactly with lfilter along the reversed s axis)
        src = alpha * W[:-1, :] + beta * W[1:, :]      # source for rows 0..Ns-1
        x = src[::-1, :]                               # top row first
        y = lfilter([1.0], [1.0, -e], x, axis=0)       # y_n = x_n + e y_{n-1}
        Psi_new = np.zeros_like(Psi)
        Psi_new[:-1, :] = y[::-1, :]                   # Psi(s_top)=0 closure
        # --- Phi march: along characteristics (g and s move together)
        Phi_new = np.empty_like(Phi)
        Phi_new[:, 0] = 1.0
        for j in range(1, Ng + 1):
            prev = Phi_new[:, j - 1]
            prev_up = np.empty(Ns + 1)
            prev_up[:-1] = prev[1:]
            prev_up[-1] = ghost[j - 1]
            Wup = np.empty(Ns + 1)
            Wup[:-1] = W[1:, j - 1]
            Wup[-1] = 0.0
            Phi_new[:, j] = e * prev_up + alpha * W[:, j] + beta * Wup
        d = max(np.abs(Phi_new - Phi).max(), np.abs(Psi_new - Psi).max())
        it_hist.append(d)
        Phi, Psi = Phi_new, Psi_new
        if d < tol:
            break
    out = dict(h=h, G=G, M=M, iters=it + 1, final_delta=float(d),
               g=g, row0=Phi[0, :].copy(),
               psi_row0=Psi[0, :].copy(), it_hist=it_hist)
    if want_grid:
        out['Phi'] = Phi
        out['s'] = s
    return out


def row_at(res, t0):
    j = int(round(t0 / res['h']))
    return float(res['row0'][j])


# ------------------------------------------------------------------
log("=" * 72)
log("SELF-TEST (i): W forced to 0  ->  Phi(s,g) = e^{-c g} exactly")
log("=" * 72)
r = solve(2e-4, 0.031, 0.1, force_W_zero=True, max_iter=3)
err = np.abs(r['row0'] - np.exp(-C * r['g'])).max()
log(f"  h=2e-4: max |Phi(0,g) - e^(-cg)| = {err:.3e}   "
    f"{'PASS' if err < 1e-14 else 'FAIL'}")
assert err < 1e-14

log("")
log("=" * 72)
log("MAIN LADDER (G=0.031, M=0.30): grid refinement at t0=0.01/0.02/0.03")
log("=" * 72)
series = json.load(open('ref_a02_series.json'))
S500 = {float(k): v[0] for k, v in series['t0_S500'].items()}
hs = [4e-4, 2e-4, 1e-4, 5e-5, 2.5e-5]
vals = {0.01: [], 0.02: [], 0.03: []}
psi_slope = []
small_t0_check = []
for h in hs:
    res = solve(h, 0.031, 0.30)
    for t0 in vals:
        vals[t0].append(row_at(res, t0))
    # self-test (ii): Psi(0,g)/g at the first few grid points vs psi1(0)
    psi_slope.append(res['psi_row0'][1] / res['g'][1])
    # self-test (iii): Phi(0, t0=0.002) vs exact series value
    small_t0_check.append(row_at(res, 0.002))
    log(f"  h={h:8.1e}  iters={res['iters']:4d}  final_delta={res['final_delta']:.1e}  "
        f"Phi(0,0.01)={vals[0.01][-1]:.6f}  Phi(0,0.02)={vals[0.02][-1]:.6f}  "
        f"Phi(0,0.03)={vals[0.03][-1]:.6f}")

log("")
log("SELF-TEST (ii): Psi(0,h)/h vs psi1(0)=39.63327 (closed form):")
for h, v in zip(hs, psi_slope):
    log(f"  h={h:8.1e}:  Psi(0,h)/h = {v:.4f}")
log("SELF-TEST (iii): Phi(0, 0.002) vs exact series value "
    f"{S500[0.002]:.8f}:")
for h, v in zip(hs, small_t0_check):
    log(f"  h={h:8.1e}:  {v:.8f}   (diff {v - S500[0.002]:+.2e})")

log("")
log("refinement differences and ratios (order-of-convergence check):")
rich = {}
for t0 in (0.01, 0.02, 0.03):
    v = vals[t0]
    diffs = [v[i + 1] - v[i] for i in range(len(v) - 1)]
    ratios = [diffs[i + 1] / diffs[i] for i in range(len(diffs) - 1)]
    # Richardson with the observed final ratio r: limit = v_last + d_last*r/(1-r)
    r_obs = ratios[-1]
    lim = v[-1] + diffs[-1] * r_obs / (1 - r_obs)
    rich[t0] = lim
    log(f"  t0={t0}:  values={['%.6f' % x for x in v]}")
    log(f"          diffs={['%.2e' % d for d in diffs]}  "
        f"ratios={['%.3f' % rr for rr in ratios]}")
    log(f"          Richardson(h->0) = {lim:.6f}   "
        f"[front claims ~0.0377; exact series: {S500.get(t0, float('nan')):.6f}]")

log("")
log("=" * 72)
log("SECOND LADDER (G=0.093, M=0.30): t0=0.09")
log("=" * 72)
v9 = []
for h in [4e-4, 2e-4, 1e-4, 5e-5]:
    res = solve(h, 0.093, 0.30)
    v9.append(row_at(res, 0.09))
    log(f"  h={h:8.1e}  iters={res['iters']:4d}  Phi(0,0.09)={v9[-1]:.6f}")
d9 = [v9[i + 1] - v9[i] for i in range(len(v9) - 1)]
r9 = d9[-1] / d9[-2]
lim9 = v9[-1] + d9[-1] * r9 / (1 - r9)
log(f"  ratios={['%.3f' % (d9[i+1]/d9[i]) for i in range(len(d9)-1)]}  "
    f"Richardson = {lim9:.6f}   [exact series: {S500[0.09]:.6f}]")

log("")
log("=" * 72)
log("CUTOFF-MARGIN (S_MAX) INSENSITIVITY at h=1e-4, G=0.031")
log("=" * 72)
for M in (0.20, 0.25, 0.30, 0.35):
    res = solve(1e-4, 0.031, M)
    log(f"  M={M:.2f}:  Phi(0,0.01)={row_at(res, 0.01):.9f}  "
        f"Phi(0,0.03)={row_at(res, 0.03):.9f}")

log("")
log("=" * 72)
log("BIG-DOMAIN RUNS for the SVD diagnostic (saved to .npz)")
log("=" * 72)
# domain matching the front's f05 SVD region: s in [0,0.5], g in [0,0.4].
# my s-grid must extend to 0.9 so that every characteristic needed for the
# (0.5 x 0.4) region is exactly marched; M=0.5-0.4 => s_top=0.5+2*0.4=1.3 is
# more than needed; use M=0.1 -> s_top = 0.9 exactly.
for h in (1e-3, 5e-4):
    res = solve(h, 0.4, 0.1, want_grid=True)
    ns_keep = int(round(0.5 / h)) + 1
    Phi_sub = res['Phi'][:ns_keep, :]
    np.savez_compressed(f'ref_a05_grid_h{h:g}.npz',
                        Phi=Phi_sub, s=res['s'][:ns_keep], g=res['g'])
    log(f"  h={h:g}: solved on s<=0.9, g<=0.4 ({res['iters']} iters, "
        f"delta {res['final_delta']:.1e}); saved s<=0.5 subgrid "
        f"{Phi_sub.shape} -> ref_a05_grid_h{h:g}.npz")
    log(f"       Phi(0,0.03)={row_at(res, 0.03):.6f}  "
        f"Phi(0,0.09)={row_at(res, 0.09):.6f}  "
        f"Phi(0,0.37)={row_at(res, 0.37):.6f}")

# also save the finest main-ladder grid (small domain) for SVD robustness
res = solve(2.5e-5, 0.031, 0.30, want_grid=True)
np.savez_compressed('ref_a05_grid_fine.npz',
                    Phi=res['Phi'], s=res['s'], g=res['g'])
log(f"  fine grid h=2.5e-5 saved: {res['Phi'].shape} -> ref_a05_grid_fine.npz")

json.dump({"richardson": {str(k): v for k, v in rich.items()},
           "richardson_t0_009": lim9,
           "ladder_G0031": {str(t0): vals[t0] for t0 in vals},
           "hs": hs, "ladder9": v9},
          open('ref_a05_results.json', 'w'), indent=1)
with open('ref_a05_pde_solver.log', 'w') as f:
    f.write("\n".join(LOG) + "\n")
log("done.")
