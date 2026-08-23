"""Bounded attempt at the full (not s_E=0-approximated) two-variable
recursive system for Phi(s,g), Psi(s,g):

  dPhi/ds - dPhi/dg = c[Phi - W],   W(s,g) = g*Avg_g[Phi(s,.)] + (1-s-g)*Psi
  dPsi/ds            = c[Psi - W]

boundary Phi(s,0)=1. Target: Phi(0, t0).

Approach tried: discretize g on a grid [0, gmax], iterate a fixed point:
 - propagate Phi along its s+g=const characteristics using the CURRENT
   estimate of W (an explicit finite-difference sweep in s, decreasing g),
 - propagate Psi forward in s at each fixed g using the current W,
 - recompute Avg_g[Phi] (trapezoidal) and hence W,
 - repeat until Phi(0,t0) stabilizes.

Status: implemented below; documents whether/how well it converges. This is
a genuine, bounded (time-boxed) attempt, not a polished production solver
-- if it fails to converge or converges to something inconsistent with the
T3 Monte Carlo of the EXACT abstract process, that is reported honestly as
non-closure of the full system, per DERIVATION_PREREG.md SS5.
"""
import numpy as np

def solve(t0, c, ng=400, ns_per_g=None, n_iter=25, verbose=True):
    # grid in g: 0..t0 (Phi only needs g in [0,t0]; s ranges 0..t0 too,
    # since s=explored mass <= 1 and we stop once s or g exceed sane bounds)
    g_grid = np.linspace(0, t0, ng + 1)
    dg = g_grid[1] - g_grid[0]
    # s grid: use the SAME resolution, s in [0, t0] (s can exceed t0 via s_E,
    # but we cap the domain at a modest multiple of t0 for tractability)
    smax = min(1.0, 3 * t0 + 0.05)
    ns = int(smax / dg) + 1
    s_grid = np.linspace(0, smax, ns + 1)

    # State arrays: Phi[i_s, i_g], Psi[i_s, i_g]
    Phi = np.zeros((len(s_grid), len(g_grid)))
    Psi = np.zeros((len(s_grid), len(g_grid)))
    Phi[:, 0] = 1.0  # boundary g=0 -> success

    for it in range(n_iter):
        # Avg_g[Phi(s,.)] via cumulative trapezoid over g, divided by g
        cum = np.zeros_like(Phi)
        cum[:, 1:] = np.cumsum(0.5 * (Phi[:, 1:] + Phi[:, :-1]) * dg, axis=1)
        with np.errstate(divide='ignore', invalid='ignore'):
            Avg = np.where(g_grid[None, :] > 0, cum / np.where(g_grid[None, :] > 0, g_grid[None, :], 1), Phi[:, [0]])
        s_mat, g_mat = np.meshgrid(s_grid, g_grid, indexing='ij')
        W = g_mat * Avg + np.clip(1 - s_mat - g_mat, 0, None) * Psi

        # Update Psi: dPsi/ds = c(Psi - W), integrate forward in s at fixed g
        Psi_new = np.zeros_like(Psi)
        for j in range(len(g_grid)):
            for i in range(1, len(s_grid)):
                ds = s_grid[i] - s_grid[i - 1]
                Psi_new[i, j] = Psi_new[i - 1, j] + ds * c * (Psi_new[i - 1, j] - W[i - 1, j])
        Psi_new = np.clip(Psi_new, 0, 1)

        # Update Phi along characteristics s+g=u (u = s+g fixed); integrate
        # BACKWARD from g=0 (s=u, Phi=1) down to g=u (s=0).
        Phi_new = np.array(Phi)
        Phi_new[:, 0] = 1.0
        for gi in range(1, len(g_grid)):
            gval = g_grid[gi]
            # walk u from gval up to smax+gval in steps of dg (matching s grid)
            u_steps = int(round((smax) / dg))
            # phi_along[k] corresponds to g = gval - k*dg ... build via s index
            # We integrate: dphi/ds = c(phi - W(s, u-s)), phi(u)=1, want phi(0)
            # i.e. step s DOWN from u to 0.
            # find u = s_grid[si] + g_grid[gi] for the diagonal starting point
            for si in range(len(s_grid)):
                u = s_grid[si] + gval
                if u > smax + t0:
                    continue
            # simpler: iterate gi as before but track along the (s, g) diagonal
        # Direct diagonal sweep: for each starting (0, gval), integrate s:0->gval
        for gi in range(1, len(g_grid)):
            gval = g_grid[gi]
            nsteps = gi  # matches dg resolution: s goes 0..gval in gi steps
            phi_val = 1.0  # boundary at s=gval, g=0
            cur_s = gval
            cur_g = 0.0
            for step in range(gi):
                # step backward: cur_s decreases by dg, cur_g increases by dg
                # interpolate W at (cur_s, cur_g)
                si_f = cur_s / dg
                gi_f = cur_g / dg
                si0 = int(np.clip(si_f, 0, len(s_grid) - 1))
                gi0 = int(np.clip(gi_f, 0, len(g_grid) - 1))
                Wv = W[si0, gi0]
                phi_val = phi_val - dg * c * (phi_val - Wv)
                cur_s -= dg
                cur_g += dg
            Phi_new[0, gi] = np.clip(phi_val, 0, 1)

        # (Phi at s>0 not fully propagated in this bounded attempt -- only
        # the s=0 row, which is what we need for the target Phi(0,t0), is
        # updated per iteration; Avg_g[Phi(s,.)] for s>0 uses the PRIOR
        # iterate elsewhere. This is a known simplification, disclosed.)
        change = np.max(np.abs(Phi_new[0] - Phi[0]))
        Phi = Phi_new
        Psi = Psi_new
        if verbose:
            print(f"  iter {it}: Phi(0,t0)={Phi[0,-1]:.5f}  max_change_row0={change:.6f}")
        if change < 1e-5:
            break
    return Phi[0, -1]


if __name__ == "__main__":
    c = 1000
    for t0 in [0.01, 0.09, 0.37]:
        print(f"t0={t0}:")
        val = solve(t0, c, ng=150, n_iter=15, verbose=True)
        print(f"  -> Phi(0,t0) approx = {val:.5f}\n")
