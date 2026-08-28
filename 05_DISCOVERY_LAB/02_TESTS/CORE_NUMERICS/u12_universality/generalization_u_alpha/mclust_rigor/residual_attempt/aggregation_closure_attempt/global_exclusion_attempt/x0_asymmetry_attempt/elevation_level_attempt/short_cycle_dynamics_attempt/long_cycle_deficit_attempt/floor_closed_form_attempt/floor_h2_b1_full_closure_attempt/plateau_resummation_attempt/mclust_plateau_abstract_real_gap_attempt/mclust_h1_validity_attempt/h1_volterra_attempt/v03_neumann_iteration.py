"""
v03_neumann_iteration.py -- numerical Neumann-series (Picard-iteration) test
of the Volterra-in-y reformulation of (E2), for h1_volterra_attempt.

Builds the linear map
    Phi -> g + L[Phi],   g(x,y) := e^{-y/eps}
    L[Phi](x,y) := (1/eps) int_0^y e^{-v/eps} W[Phi](x+v,y-v) dv
    W[Phi](x,y) := (1-eps(x+y)) Psi[Phi](x,y) + eps I[Phi](x,y)      (NEW identity,
                    derived in v02 from (E1)+(KEY), verified there)
    Psi[Phi](x,y) := int_0^inf e^{-u^2/2-u(x+y)} I[Phi](x+u,y) du     (BB-Psi')
    I[Phi](x,y) := int_0^y Phi(x,y') dy'

and iterates Phi^(0) = g, Phi^(n+1) = g + L[Phi^(n)], comparing Phi^(n) against
the TRUE solution (from the independently-validated (P,Q)-family series,
v01_family_series.py) at a handful of core (x,y) points, for n=0..n_max.
This is the direct, literal "several terms of the Neumann series, check the
partial sums stabilize" test the mandate calls for.

Grid discretisation, no interpolation: x and y share the SAME step h, so
every shift (x+v, x+u) used by the formulas above lands exactly on a grid
point. Because L reaches x -> x+y+u (up to Umax), computing Phi^(n) accurately
on a "core" x-window [0,Xcore] requires Phi^(n-1) on an EXTENDED window
[0,Xcore + Ycore + Umax]; iterating n_max times therefore uses a domain that
SHRINKS by (Ycore+Umax) each step, starting from a total width
Xcore + n_max*(Ycore+Umax) at n=0 (where Phi^(0)=g is explicit and needs no
precomputation at all) down to exactly Xcore at n=n_max.
"""
import numpy as np
import mpmath as mp
import sys, os, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v01_family_series import Family, bounded_branch_solve, poly_trim


def build_true_solution(c_val, K, dps):
    """Ground truth Phi(s,g) via the validated (P,Q)-family series."""
    old = mp.mp.dps
    mp.mp.dps = dps
    c = mp.mpf(c_val)
    a = [None] * (K + 2)
    b = [None] * (K + 2)
    a[0] = Family([mp.mpf(1)], [], c)
    b[0] = Family([], [], c)
    a[1] = Family([-c], [], c)
    b[1] = bounded_branch_solve(Family([-c], [], c))
    for k in range(1, K + 1):
        term1 = a[k - 1].scale(mp.mpf(1) / k)
        term2 = b[k].mul_1_minus_s()
        w_k = term1.add(term2).sub(b[k - 1])
        akp1 = a[k].deriv().sub(a[k].scale(c)).add(w_k.scale(c)).scale(mp.mpf(1) / (k + 1))
        a[k + 1] = akp1
        if k + 1 <= K:
            src = a[k].scale(-c / (k + 1)).add(b[k].scale(c))
            b[k + 1] = bounded_branch_solve(src)
    mp.mp.dps = old

    def Phi_true(s_val, g_val):
        mp.mp.dps = dps
        s = mp.mpf(s_val)
        g = mp.mpf(g_val)
        r = mp.mpf(0)
        gp = mp.mpf(1)
        for k in range(K + 1):
            r += a[k].eval(s) * gp
            gp *= g
        return float(r)

    return Phi_true


def run_neumann_experiment(c_val, h, Ycore, Umax, n_max, x_test_pts, y_test_pts,
                            K_true=140, dps_true=90, verbose=True):
    eps = 1.0 / np.sqrt(c_val)
    Ny = int(round(Ycore / h)) + 1
    y_grid = np.arange(Ny) * h
    Lu = int(round(Umax / h))
    u_grid = np.arange(Lu + 1) * h
    growth_steps = (Ny - 1) + Lu  # extra x-grid points consumed per L-application

    Xcore_steps = int(round(max(x_test_pts) / h)) + 1
    Nx_current = Xcore_steps + n_max * growth_steps
    x_grid_full = np.arange(Nx_current) * h

    def phi0_field(Nx):
        return np.tile(np.exp(-y_grid / eps), (Nx, 1))

    def trapz_cumulative(field):
        # cumulative trapezoid along axis=1 (y), returns same shape, [.,0]=0
        Nx_, Ny_ = field.shape
        out = np.zeros_like(field)
        # cumulative integral via cumulative sum of trapezoid increments
        incr = h * 0.5 * (field[:, 1:] + field[:, :-1])
        out[:, 1:] = np.cumsum(incr, axis=1)
        return out

    def trapz_weights(n):
        # weights for trapezoid rule over n+1 points spaced h apart
        w = np.full(n + 1, h)
        if n >= 1:
            w[0] *= 0.5
            w[-1] *= 0.5
        return w

    Phi = phi0_field(Nx_current)
    Nx_seq = [Nx_current]
    history = {pt: [] for pt in [(xp, yp) for xp in x_test_pts for yp in y_test_pts]}

    def record(field, Nx):
        xg = np.arange(Nx) * h
        for xp in x_test_pts:
            ix = int(round(xp / h))
            if ix >= Nx:
                continue
            for yp in y_test_pts:
                jy = int(round(yp / h))
                if jy >= Ny:
                    continue
                history[(xp, yp)].append(field[ix, jy])

    record(Phi, Nx_current)

    for n in range(1, n_max + 1):
        Nx_new = Nx_current - growth_steps
        # I[i',j'] for all i' in current grid
        I = trapz_cumulative(Phi)  # shape (Nx_current, Ny)

        # Psi[i',j'] for i' in [0, Nx_current-Lu-1]
        Nx_psi = Nx_current - Lu
        Psi = np.zeros((Nx_psi, Ny))
        xg_psi = np.arange(Nx_psi) * h
        for l in range(Lu + 1):
            wl = h if (0 < l < Lu) else 0.5 * h
            ul = u_grid[l]
            # kernel exp(-ul^2/2 - ul*(x_i'+y_j')) for i' in [0,Nx_psi), j' in [0,Ny)
            xshift = xg_psi[:, None] + y_grid[None, :]
            kernel = np.exp(-0.5 * ul * ul - ul * xshift)
            Psi += wl * kernel * I[l:l + Nx_psi, :]
        # W = (1-eps(x+y))*Psi + eps*I   on the Psi-sized window
        xy_sum = xg_psi[:, None] + y_grid[None, :]
        W = (1.0 - eps * xy_sum) * Psi + eps * I[:Nx_psi, :]

        # Phi_new[i,j] for i in [0,Nx_new-1]
        Phi_new = np.zeros((Nx_new, Ny))
        for j in range(Ny):
            g_val = np.exp(-y_grid[j] / eps)
            if j == 0:
                Phi_new[:, j] = g_val
                continue
            wv = trapz_weights(j)  # length j+1, for v_k=k*h, k=0..j
            v_idx = np.arange(j + 1)
            kernel_v = np.exp(-v_idx * h / eps)
            # W[i+k, j-k] for i in [0,Nx_new), k in [0,j]
            acc = np.zeros(Nx_new)
            for k in range(j + 1):
                acc += wv[k] * kernel_v[k] * W[k:k + Nx_new, j - k]
            Phi_new[:, j] = g_val + acc / eps

        Phi = Phi_new
        Nx_current = Nx_new
        Nx_seq.append(Nx_current)
        record(Phi, Nx_current)
        if verbose:
            print(f"  n={n}: Nx_current={Nx_current}")

    return history, Nx_seq, eps


if __name__ == "__main__":
    t0 = time.time()
    c_val = 100.0
    h = 0.1
    Ycore = 1.0
    Umax = 6.0
    n_max = 5
    x_test_pts = [0.0, 0.3, 0.6]
    y_test_pts = [0.2, 0.5, 1.0]

    print("Building ground truth via validated (P,Q)-family series (c=100, K=100, dps=120)...")
    Phi_true = build_true_solution(c_val, K=100, dps=120)
    sqc = np.sqrt(c_val)

    print("Running Neumann/Picard iteration, grid h=0.1, Ycore=1.0, Umax=6.0, n_max=5 ...")
    history, Nx_seq, eps = run_neumann_experiment(
        c_val, h, Ycore, Umax, n_max, x_test_pts, y_test_pts,
        K_true=100, dps_true=120)

    print()
    print("eps =", eps)
    print("Nx_seq (grid width per iteration, shrinking):", Nx_seq)
    print()
    print("=== Neumann partial sums Phi^(n)(x,y) [SCALED coords] vs true Phi (via s=x/sqrt(c), g=y/sqrt(c)) (c=100) ===")
    for (xp, yp), vals in history.items():
        s_true = Phi_true(xp / sqc, yp / sqc)
        print(f"(x={xp},y={yp}):")
        for n, v in enumerate(vals):
            err = abs(v - s_true)
            print(f"    n={n}: Phi^(n)={v:.10f}   |err|={err:.3e}")
        print(f"    TRUE   ={s_true:.10f}")
    print()
    print("elapsed:", time.time() - t0, "s")
