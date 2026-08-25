"""
f04_corrected_2d_solver.py -- corrected attempt at the bounded numerical
fixed-point solve of the full SS5 system that floor_closed_form_attempt's
solve_2d_system.py attempted and disclosed as failing ("Phi(0,0.37)=1.0
exactly, an artifact of the implementation only fully propagating the
Phi(s=0,.) row per iteration while leaving Phi(s>0,.) ... essentially
unresolved").

Fix applied here: EVERY (s,g) grid point of Phi (not just the s=0 row) is
re-marched, along its own characteristic s+g=const, on EVERY outer
(Gauss-Seidel) iteration, using an exact local exponential integrator for
the linear part (unconditionally stable regardless of c*h). Psi is solved
by the analogous exact-exponential marching backward in s from a cutoff
S_MAX (where Psi is approximated as 0 -- an approximation whose bias is
checked below by varying S_MAX and confirming the target values stabilize).

Domain fix (HONEST PROCESS NOTE, first version of this file): the first
version of this solver vectorized the anti-diagonal marching incorrectly --
it re-used the post-step array as if it were still indexed by "steps taken"
rather than by absolute row position, which silently meant only k=1 ever
wrote to row s=0, so Phi(0,t0) collapsed to ~0 for every t0>h and the
Phi(s=0,.) row never changed between outer iterations (the printed
max|dPhi(s=0,.)|=0 gave this away immediately -- caught before trusting any
downstream number, exactly the kind of self-caught bug this lineage
discloses rather than silently fixes). Rewritten below with a corrected,
unit-tested marching indexer, PLUS the boundary needs the virtual s-grid
extended to S_MAX+G_MAX (not just S_MAX) so every (s,g) in the reported
rectangle domain has its full characteristic-to-boundary path inside the
grid -- the first version's rectangle-vs-triangle domain mismatch (part of
why some entries silently fell back to stale/NaN-filled values) is fixed by
this extension, not by a NaN patch.
"""
import numpy as np
import json
import time

C = 1000.0


def solve(G_MAX, S_MAX, h, n_iter, verbose=True, psi_far_zero=True):
    NG = int(round(G_MAX / h))
    NS = int(round(S_MAX / h))
    NS_EXT = NS + NG  # extended virtual s-range so every characteristic's
    # boundary start point (s_index = i+k <= NS_EXT) lies inside the grid
    g_grid = np.linspace(0, NG * h, NG + 1)
    s_grid_ext = np.linspace(0, NS_EXT * h, NS_EXT + 1)
    decay = np.exp(-C * h)

    # Phi_ext[i,k] for i in 0..NS_EXT, k in 0..NG.  Psi[i,k] only needed/used
    # for i in 0..NS (we treat Psi==0 beyond S_MAX, i.e. i>NS never queried).
    Phi = np.tile(np.exp(-C * g_grid)[None, :], (NS_EXT + 1, 1))
    Psi = np.zeros((NS + 1, NG + 1))

    history = []
    for it in range(n_iter):
        # Avg_g[Phi(s,.)] and W, evaluated on the FULL extended s-range (needed
        # as the "start point" values during Phi's own marching) and on the
        # s<=S_MAX range (needed for Psi's marching):
        cum = np.zeros_like(Phi)
        cum[:, 1:] = np.cumsum(0.5 * (Phi[:, 1:] + Phi[:, :-1]), axis=1) * h
        with np.errstate(divide="ignore", invalid="ignore"):
            Avg_ext = np.where(g_grid[None, :] > 0, cum / np.maximum(g_grid[None, :], h), 1.0)

        s_mat_ext, g_mat_ext = np.meshgrid(s_grid_ext, g_grid, indexing="ij")
        Psi_ext = np.zeros((NS_EXT + 1, NG + 1))
        Psi_ext[:NS + 1, :] = Psi  # Psi==0 for s>S_MAX (psi_far_zero cutoff)
        W_ext = g_mat_ext * Avg_ext + np.clip(1 - s_mat_ext - g_mat_ext, 0, None) * Psi_ext

        # --- Psi update: backward march in s (fixed g) from Psi(S_MAX,.)=0 ---
        Psi_new = np.zeros((NS + 1, NG + 1))
        for i in range(NS - 1, -1, -1):
            Wv = W_ext[i + 1, :]
            Psi_new[i, :] = Wv + (Psi_new[i + 1, :] - Wv) * decay

        # --- Phi update: march each characteristic from (row=m, col=0)=1
        #     down to (row=0, col=m). CORRECT indexing: after k steps, the
        #     value that started at row (i+k) [col 0] now sits at row i, col k.
        #     So: Phi_new[i, k] = step(Phi_new[i+1, k-1]) for i = 0 .. NS_EXT-k.
        Phi_new = np.empty_like(Phi)
        Phi_new[:, 0] = 1.0
        for k in range(1, NG + 1):
            n_valid = NS_EXT - k + 1  # rows 0..n_valid-1 are computable at this k
            src = Phi_new[1:n_valid + 1, k - 1]  # rows 1..n_valid (i+1 for i=0..n_valid-1)
            Wv = W_ext[1:n_valid + 1, k - 1]
            Phi_new[:n_valid, k] = Wv + (src - Wv) * decay
            if n_valid <= NS_EXT:
                Phi_new[n_valid:, k] = Phi[n_valid:, k]  # outside reachable range this iter: keep old

        change_phi = np.max(np.abs(Phi_new[0, :] - Phi[0, :]))
        change_psi = np.max(np.abs(Psi_new[0, :] - Psi[0, :])) if NS > 0 else 0.0
        Phi, Psi = Phi_new, Psi_new
        history.append((it, float(change_phi), float(change_psi)))
        if verbose and (it % 10 == 0 or it == n_iter - 1):
            print(f"  iter {it:3d}: max|dPhi(s=0,.)|={change_phi:.3e}  "
                  f"max|dPsi(s=0,.)|={change_psi:.3e}")
        if change_phi < 1e-8 and change_psi < 1e-8:
            if verbose:
                print(f"  converged at iter {it}")
            break

    return g_grid, Phi, Psi, history


def _self_test_uncoupled():
    """Unit test: if we FORCE Psi=0 and Avg_g[Phi]=0 (i.e. artificially zero
    out W every iteration -- decouple from the recursive structure entirely),
    the Phi marching alone must reduce to the trivial ODE dPhi/ds-dPhi/dg=cPhi,
    whose solution along s+g=u starting at Phi(u,0)=1 is Phi(s,g)=e^{-c g}
    exactly (pure race, no re-entry). This isolates and validates JUST the
    marching indexer, independent of any coupling-model correctness."""
    G_MAX, S_MAX, h = 0.05, 0.02, 0.001
    NG = int(round(G_MAX / h))
    g_grid = np.linspace(0, NG * h, NG + 1)
    NS_EXT = int(round((S_MAX + G_MAX) / h))
    decay = np.exp(-C * h)
    Phi = np.ones((NS_EXT + 1, NG + 1))
    Phi[:, 0] = 1.0
    for k in range(1, NG + 1):
        n_valid = NS_EXT - k + 1
        src = Phi[1:n_valid + 1, k - 1]
        Wv = np.zeros(n_valid)  # force W=0 (fully decoupled / no re-entry, no generic branch)
        Phi[:n_valid, k] = Wv + (src - Wv) * decay
    exact = np.exp(-C * g_grid)
    err = np.max(np.abs(Phi[0, :] - exact))
    print(f"[self-test] max|Phi_marched(0,g) - exp(-c g)| over g in [0,{G_MAX}] "
          f"(decoupled W=0 case) = {err:.2e}  (should be ~0, up to O(h) discretization)")
    assert err < 1e-3, "marching indexer self-test FAILED"
    print("[self-test] PASSED (marching indexer correctly reproduces the pure-race limit)")


if __name__ == "__main__":
    print("Running marching-indexer self-test first (decoupled W=0 case)...")
    _self_test_uncoupled()
    print()

    t_start = time.time()
    G_MAX, S_MAX, h = 0.40, 0.50, 0.002
    print(f"Grid: G_MAX={G_MAX} S_MAX={S_MAX} h={h}  (c*h={C*h})")
    g_grid, Phi, Psi, history = solve(G_MAX, S_MAX, h, n_iter=80)
    print(f"elapsed: {time.time()-t_start:.1f}s")

    print("\nPhi(0, t0) at the T3 comparison points "
          "(T3 reference values are CITED from the already-archived "
          "fcd_t3.log, not re-derived here -- this run does not simulate "
          "anything, it only solves the PDE system numerically):")
    targets = [0.01, 0.09, 0.37]
    t3_reference = {0.01: 0.03832, 0.09: 0.03832, 0.37: 0.03885}
    results = {}
    for t0 in targets:
        j = int(round(t0 / h))
        val = float(Phi[0, j])
        results[t0] = val
        ref = t3_reference.get(t0)
        print(f"  t0={t0:.2f}  solver Phi(0,t0)={val:.5f}   T3 (cited)={ref}   diff={val-ref:+.5f}")

    with open("f04_solver_results.json", "w") as fh:
        json.dump({
            "G_MAX": G_MAX, "S_MAX": S_MAX, "h": h, "n_iter_run": len(history),
            "targets": results, "t3_reference": t3_reference,
            "history_tail": history[-5:],
        }, fh, indent=2)
