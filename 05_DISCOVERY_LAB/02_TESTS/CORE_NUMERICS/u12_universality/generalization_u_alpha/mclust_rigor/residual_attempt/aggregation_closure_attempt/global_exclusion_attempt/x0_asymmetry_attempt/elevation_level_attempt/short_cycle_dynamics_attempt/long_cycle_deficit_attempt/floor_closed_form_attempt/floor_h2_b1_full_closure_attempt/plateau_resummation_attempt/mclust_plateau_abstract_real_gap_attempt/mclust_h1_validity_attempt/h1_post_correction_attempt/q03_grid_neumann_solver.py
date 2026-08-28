"""
q03_grid_neumann_solver.py

A FRESH, from-scratch, interpolation-free grid Picard/Neumann solver for
the closed Volterra-in-y system, coded ONLY from the prose equations in
the required reading (h1_volterra_attempt/ATTEMPT.md Sec 2-6):

  (NEW-W):    W(x,y) = (1-eps(x+y))*Psi(x,y) + eps*I(x,y)
  (E2'):      Phi(x,y) = e^{-y/eps} + [(1-eps(x+y))/eps]*A(x,y) + B(x,y)
                A(x,y) := int_0^y e^{-v/eps} Psi(x+v,y-v) dv
                B(x,y) := int_0^y e^{-v/eps} I(x+v,y-v) dv
  (BB-Psi'):  Psi(x,y) = int_0^infinity e^{-u^2/2-u(x+y)} I(x+u,y) du
  I:          I(x,y) = int_0^y Phi(x,y') dy'

Grid: x and y share the same step h (interpolation-free: every shift used
by the formulas -- x+v, x+u -- lands exactly on a grid point). The map
Phi^(n) -> Phi^(n+1), evaluated at position x, reaches Phi^(n) values at
x-shifts up to (Ymax_used_in_A + Umax_used_in_BB-Psi'), so an accurate
Phi^(n_max) at x=0 requires Phi^(0) to be defined on an x-window of width
n_max*(Ymax+Umax); Phi^(0)(x,y)=e^{-y/eps} is explicit (x-independent),
so no precomputation is needed there.

No .py file from any ancestor front or the referee was opened, read, or
imported at any point -- this implementation, its trapezoid-weight
bookkeeping, and its vectorization strategy were all worked out fresh
from the prose above.

We reproduce (independently) the predecessor's Sec 6.2/6.3
successive-difference-ratio tables and Sec 6.4 n_cross(y) table, at
x=0, c in {100,1000}, y up to 6.0.
"""
import numpy as np
import time

def run(c, h=0.1, Ymax=6.0, Umax=6.0, n_max=12, verbose=True):
    eps = 1.0/np.sqrt(c)
    Ny = int(round(Ymax/h)) + 1                      # y = 0..Ymax
    Nu = int(round(Umax/h)) + 1                       # u = 0..Umax (for BB-Psi' truncation)
    per_iter_consumption = Ny - 1 + Nu - 1             # grid steps consumed in x per iteration
    Nx = n_max*per_iter_consumption + 50 + 1           # generous buffer
    Y = np.arange(Ny)*h
    X = np.arange(Nx)*h

    if verbose:
        print(f"  c={c}, eps={eps:.6f}, h={h}, Ny={Ny}, Nu={Nu}, Nx={Nx} "
              f"(array size {Nx*Ny:,})")

    # Phi^(0)(x,y) = e^{-y/eps}, independent of x
    phi = np.tile(np.exp(-Y/eps), (Nx, 1))            # shape (Nx, Ny)

    history_x0 = [phi[0, :].copy()]                    # Phi^(n)(0, y) for each n

    # trapezoid weights for the u-integral (fixed upper limit Umax, all iy)
    w_u = np.full(Nu, h)
    w_u[0] = h/2.0
    w_u[-1] = h/2.0

    t0 = time.time()
    for n in range(1, n_max+1):
        # ---- 1. I(x,y) = int_0^y Phi(x,y') dy'  (cumulative trapezoid over y) ----
        I = np.zeros_like(phi)
        incr = 0.5*h*(phi[:, :-1] + phi[:, 1:])         # shape (Nx, Ny-1)
        I[:, 1:] = np.cumsum(incr, axis=1)

        # ---- 2. Psi(x,y) = int_0^Umax e^{-u^2/2-u(x+y)} I(x+u,y) du ----
        Psi = np.zeros_like(phi)
        for iu in range(Nu):
            u = iu*h
            if Nx - iu <= 0:
                break
            kx = np.exp(-u*X[:Nx-iu])                   # depends on ix
            ky = np.exp(-u*Y)                             # depends on iy
            ku = np.exp(-u*u/2.0)
            Psi[:Nx-iu, :] += (w_u[iu]*ku) * kx[:, None] * ky[None, :] * I[iu:Nx, :]

        # ---- 3. A(x,y), B(x,y) via v-integral 0..y (variable upper limit) ----
        A = np.zeros_like(phi)
        B = np.zeros_like(phi)
        # main pass: uniform weight h (iv=0 gets h/2), correction for the
        # y-dependent right endpoint (iv=iy) applied afterward
        for iv in range(Ny):
            v = iv*h
            wv = (h/2.0) if iv == 0 else h
            ev = np.exp(-v/eps)
            if Nx - iv <= 0:
                break
            A[:Nx-iv, iv:Ny] += (wv*ev) * Psi[iv:Nx, 0:Ny-iv]
            B[:Nx-iv, iv:Ny] += (wv*ev) * I[iv:Nx, 0:Ny-iv]
        # right-endpoint (v=y, i.e. iv=iy) correction: was counted at weight
        # h above (for iv>0), should be h/2 -> subtract h/2 of that term
        for iy in range(1, Ny):
            v = iy*h
            ev = np.exp(-v/eps)
            if Nx - iy <= 0:
                break
            A[:Nx-iy, iy] -= (h/2.0*ev) * Psi[iy:Nx, 0]
            B[:Nx-iy, iy] -= (h/2.0*ev) * I[iy:Nx, 0]

        # ---- 4. (E2') update ----
        coeff = (1.0 - eps*(X[:, None] + Y[None, :])) / eps   # shape (Nx, Ny)
        g = np.exp(-Y/eps)[None, :]
        phi_new = g + coeff*A + B

        # ---- 5. shrink to the trustworthy core (drop the last consumed strip) ----
        core = Nx - per_iter_consumption
        phi_new = phi_new[:core, :]
        # re-pad back to full Nx width with (stale, no-longer-trusted) values
        # so array shapes stay consistent across iterations; only [:core] is
        # ever used/read at the NEXT iteration's shifted slices anyway once
        # Nx shrinks -- simplest: just keep shrinking Nx physically.
        phi = phi_new
        Nx = core
        X = np.arange(Nx)*h

        history_x0.append(phi[0, :].copy() if Nx > 0 else np.full(Ny, np.nan))

    if verbose:
        print(f"  done in {time.time()-t0:.2f}s, final core width Nx={Nx}")

    return np.array(history_x0), Y, eps   # shape (n_max+1, Ny)


def ratios_at_y(history, Y, y_target):
    iy = int(round(y_target/ (Y[1]-Y[0])))
    seq = history[:, iy]
    diffs = np.abs(np.diff(seq))
    ratios = diffs[1:] / diffs[:-1]
    return ratios


def n_cross_from_ratios(ratios, threshold=0.5):
    # smallest n (1-indexed into the ratio-sequence position, matching the
    # predecessor's own "index of the ratio value" convention: ratios[0] is
    # the ratio after n=2 (comparing steps 2-1 vs 1-0)) after which ALL
    # subsequent ratios stay below threshold
    for k in range(len(ratios)):
        if np.all(ratios[k:] < threshold):
            # predecessor's n_cross(y) := smallest n after which ratio stays
            # permanently below 0.5; ratios[k] corresponds to Picard step n=k+2
            return k + 2
    return None


if __name__ == "__main__":
    print("="*78)
    print("Fresh grid Neumann/Picard solver -- reproducing Sec 6.2/6.3/6.4")
    print("="*78)

    published_ratios_c100 = {
        0.5: [0.207, 0.076, 0.044, 0.031, 0.025],
        1.0: [0.552, 0.197, 0.105, 0.068, 0.049],
        2.0: [1.124, 0.432, 0.238, 0.154, 0.109],
        3.0: [1.550, 0.622, 0.352, 0.232, 0.166],
        4.0: [1.879, 0.775, 0.448, 0.299, 0.217],
        5.0: [2.143, 0.901, 0.528, 0.357, 0.261],
        6.0: [2.362, 1.008, 0.597, 0.407, 0.300],
    }
    published_ratios_c1000 = {
        1.0: [1.112, 0.447, 0.258, 0.175, 0.130],
        3.0: [2.659, 1.121, 0.663, 0.454, 0.338],
        6.0: [3.937, 1.728, 1.049, 0.732, 0.552],
    }
    published_ncross_c100 = {0.5:2,1.0:2,2.0:3,3.0:4,4.0:4,5.0:5,6.0:5}
    published_ncross_c1000 = {0.5:2,1.0:3,2.0:4,3.0:5,4.0:6,5.0:6,6.0:7}

    for c, pubtab, pubncross in [
        (100, published_ratios_c100, published_ncross_c100),
        (1000, published_ratios_c1000, published_ncross_c1000),
    ]:
        print(f"\n----- c={c} -----")
        history, Y, eps = run(c, h=0.1, Ymax=6.0, Umax=6.0, n_max=12)
        for y in sorted(pubtab.keys()):
            ratios = ratios_at_y(history, Y, y)
            ours = ratios[:5]
            pub = pubtab[y]
            print(f"  y={y:>4.1f}: published = {['%.3f'%v for v in pub]}")
            print(f"          this front = {['%.4f'%v for v in ours]}")
            max_rel_diff = max(abs(o-p)/p for o,p in zip(ours,pub))
            print(f"          max rel diff (first 5 ratios) = {max_rel_diff:.4f}")
        print(f"  n_cross(y) comparison (threshold ratio<0.5, this front's full")
        print(f"  computed sequence vs predecessor's published Sec 6.4 values):")
        ncross_table = published_ncross_c100 if c == 100 else published_ncross_c1000
        for y in sorted(ncross_table.keys()):
            ratios = ratios_at_y(history, Y, y)
            nc = n_cross_from_ratios(ratios, threshold=0.5)
            flag = "" if nc == ncross_table[y] else "  <-- differs, see Sec 5.3 disclosure"
            print(f"    y={y:>4.1f}: published n_cross={ncross_table[y]:>2d}   "
                  f"this front's n_cross={nc}{flag}")

    print("\n" + "="*78)
    print("Fine y-grid (step 0.5) n_cross(y) measurement and linear-fit slope,")
    print("this front's own independent replication -- compared against the")
    print("predecessor's own published fit (0.500y+2.200 at c=100,")
    print("0.771y+2.467 at c=1000, ATTEMPT.md Sec 6.4)")
    print("="*78)
    for c in [100, 1000]:
        history, Y, eps = run(c, h=0.1, Ymax=6.0, Umax=6.0, n_max=12, verbose=False)
        ys = np.arange(0.5, 6.01, 0.5)
        ncs = []
        for y in ys:
            r = ratios_at_y(history, Y, y)
            nc = n_cross_from_ratios(r, threshold=0.5)
            ncs.append(nc)
        ys_arr = np.array(ys); ncs_arr = np.array(ncs, dtype=float)
        slope, intercept = np.polyfit(ys_arr, ncs_arr, 1)
        print(f"c={c}: n_cross measured (0.5-step y-grid) = {ncs}")
        print(f"  this front's fit:      n_cross ~ {slope:.4f}*y + {intercept:.4f}")
        pub_slope = 0.500 if c == 100 else 0.771
        pub_intercept = 2.200 if c == 100 else 2.467
        print(f"  predecessor's fit:     n_cross ~ {pub_slope:.4f}*y + {pub_intercept:.4f}")
        print(f"  slope rel. diff: {abs(slope-pub_slope)/pub_slope:.4f}")
