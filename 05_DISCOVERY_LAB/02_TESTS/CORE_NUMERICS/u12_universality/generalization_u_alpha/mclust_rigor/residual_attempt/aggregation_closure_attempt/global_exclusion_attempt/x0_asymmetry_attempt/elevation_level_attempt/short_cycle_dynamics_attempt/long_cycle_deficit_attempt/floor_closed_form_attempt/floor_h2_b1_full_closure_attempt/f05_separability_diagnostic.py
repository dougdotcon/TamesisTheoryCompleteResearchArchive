"""
f05_separability_diagnostic.py -- quantitative check of whether Phi(s,g), as
produced by the corrected f04 solver, is well-approximated by a LOW-RANK
(separable, Phi(s,g) ~= sum_{r=1}^{R} u_r(s) v_r(g)) form. This is the
concrete, checkable diagnostic behind the "the coupling is fundamental"
claim in the final ATTEMPT.md write-up: if Phi were exactly rank-1
(Phi(s,g)=u(s)v(g)), the nonlocal Avg_g[Phi(s,.)] term would collapse to
u(s)*Avg_g[v], and the whole SS5 system would decouple into two ordinary
(1-variable) problems -- exactly the kind of "local transformation" the
task asks whether the coupling resists. A low SVD rank needed for a good
approximation would say the coupling is "removable" after all; a
persistently high rank (error not shrinking as more terms are added) is
positive evidence the 2D structure is NOT an artifact of a bad
parametrization.
"""
import numpy as np
import json
import sys

sys.path.insert(0, ".")
from f04_corrected_2d_solver import solve

G_MAX, S_MAX, h = 0.40, 0.50, 0.001
print(f"Solving at G_MAX={G_MAX} S_MAX={S_MAX} h={h} for the separability grid...")
g_grid, Phi, Psi, hist = solve(G_MAX, S_MAX, h, n_iter=150, verbose=False)
print(f"  converged in {len(hist)} outer iterations, last change={hist[-1][1]:.2e}")

NS_report = int(round(S_MAX / h))
Phi_grid = Phi[:NS_report + 1, :]  # restrict to the REPORTED (non-extended) s-range
s_grid = np.linspace(0, NS_report * h, NS_report + 1)

print(f"\nPhi grid shape (s x g): {Phi_grid.shape}")

# SVD-based low-rank diagnostic
U, S, Vt = np.linalg.svd(Phi_grid, full_matrices=False)
total_energy = np.sum(S ** 2)
print("\nSingular value spectrum (top 10) and cumulative variance explained:")
cum = 0.0
rows = []
for k in range(min(10, len(S))):
    cum += S[k] ** 2
    frac = cum / total_energy
    rows.append(dict(k=k + 1, singular_value=float(S[k]), cum_frac_variance=float(frac)))
    print(f"  rank {k+1:2d}: sigma={S[k]:12.4f}   cumulative variance frac={frac:.6f}   "
          f"residual frac={1-frac:.2e}")

# Reconstruction error at increasing rank, in RELATIVE Frobenius norm AND in
# the specific quantity that matters (the s=0 row, i.e. Phi(0,.) itself,
# which is phi(t0)):
print("\nReconstruction error of the TARGET row Phi(0,.) at increasing rank:")
phi0_true = Phi_grid[0, :]
rank_rows = []
for R in [1, 2, 3, 5, 8, 12, 20]:
    if R > len(S):
        continue
    recon = (U[:, :R] * S[:R]) @ Vt[:R, :]
    err_full = np.linalg.norm(Phi_grid - recon) / np.linalg.norm(Phi_grid)
    err_row0 = np.linalg.norm(recon[0, :] - phi0_true) / np.linalg.norm(phi0_true)
    rank_rows.append(dict(rank=R, rel_frobenius_err=float(err_full), rel_row0_err=float(err_row0)))
    print(f"  rank {R:3d}: relative Frobenius error={err_full:.3e}   "
          f"relative error on Phi(0,.) row={err_row0:.3e}")

# Also report the "trivial" comparison: how good is the CRUDEST possible
# rank-1 model people would guess first -- Phi(s,g) ~= exp(-c*g) (independent
# of s), i.e. Candidate 1's pointwise-substitution idea generalized off the
# s=0 axis. This is the "is the coupling removable by the FIRST guess"
# sanity anchor.
C = 1000.0
naive_rank1 = np.exp(-C * g_grid)[None, :] * np.ones((NS_report + 1, 1))
err_naive = np.linalg.norm(Phi_grid - naive_rank1) / np.linalg.norm(Phi_grid)
print(f"\nFor comparison, the naive s-independent guess Phi(s,g)~=e^(-cg) gives "
      f"relative Frobenius error={err_naive:.3e} (this is Candidate 1 off-axis; "
      f"ATTEMPT.md SS2 already refuted it on-axis at s=0).")

with open("f05_separability_results.json", "w") as fh:
    json.dump({
        "grid_shape": list(Phi_grid.shape), "h": h, "G_MAX": G_MAX, "S_MAX": S_MAX,
        "singular_values_top10": rows,
        "rank_reconstruction_errors": rank_rows,
        "naive_expneg_cg_rel_frobenius_err": float(err_naive),
    }, fh, indent=2)
