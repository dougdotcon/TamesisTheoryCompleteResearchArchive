"""
ADVERSARIAL CHECK 4 -- independent, from-scratch grid-based Neumann/Picard
iteration of the closed Volterra-in-y system, built ONLY from the equations
quoted in ATTEMPT.md's own prose (Sec 0, Sec 3.1, Sec 4.1) -- NOT from
reading any .py file of the target front or any ancestor, per the mandate.

Equations used (all transcribed from prose, independently coded):
  I(x,y)   = int_0^y Phi(x,y') dy'                                    (def)
  Psi(x,y) = int_0^inf e^{-u^2/2-u(x+y)} I(x+u,y) du                  (BB-Psi')
  W(x,y)   = (1-eps(x+y)) * Psi(x,y) + eps*I(x,y)                     (NEW-W)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv    (E2)

Grid: uniform step h in both x and y, so x+v and x+u always land on grid
points (no interpolation), same discipline the target front describes.
Phi^(0)(x,y) := e^{-y/eps}.  Iterate the map above using Phi^(n-1) to get
Psi^(n-1), I^(n-1), W^(n-1), then Phi^(n).  All integrals via the
trapezoidal rule (I use numpy.trapz), matching the target's own claimed
O(h^2) discretization (their Richardson test, Sec 5.4, independently
re-derivable in principle but not attempted here -- out of scope for a
LIGHT independent cross-check).

This checks the QUALITATIVE claim of ATTEMPT.md Sec 6: does the
successive-difference ratio |Phi^(n)-Phi^(n-1)|/|Phi^(n-1)-Phi^(n-2)|,
at x=0, eventually decrease monotonically and super-geometrically, at
several y, for c=100? And does the document's OWN claim (Sec 4, crude
operator bound over-predicts warm-up growth) look consistent with
Check 1-3's finding that the TRUE operator is much better behaved than
Sec 4 claims?
"""
import numpy as np

def run(c, h, ymax_track, n_max, Umax=6.0, verbose=False):
    eps = 1.0/np.sqrt(c)
    # x grid needs to extend far enough to support n_max iterations:
    # each iteration needs Phi at x up to x + y + Umax (roughly), shrinking
    # by (ymax_track+Umax) each iteration -- so start with a big enough pad.
    pad_per_iter = ymax_track + Umax
    Xcore = 2.0   # core x-window we actually want accurate (x=0 suffices here)
    Xtot = Xcore + n_max*pad_per_iter
    Nx = int(round(Xtot/h)) + 1
    xs = np.arange(Nx)*h
    Ny = int(round(ymax_track/h)) + 1
    ys = np.arange(Ny)*h
    Nu = int(round(Umax/h)) + 1
    us = np.arange(Nu)*h

    # Phi^(0)(x,y) = e^{-y/eps}, on the full (x,y) grid we need at each stage.
    # We keep Phi as a 2D array [ix, iy] and just always compute on the
    # FULL available domain each iteration (simplification vs. the target's
    # shrinking-window optimization -- mathematically equivalent, just
    # recomputes some unnecessary values; fine for this scale).
    Phi = np.exp(-ys[None,:]/eps) * np.ones((Nx,1))

    history = {y: [] for y in ys}  # we'll track only a few requested y's

    def step(Phi):
        # I(x,y) = int_0^y Phi(x,y') dy'  via cumulative trapezoid over y axis
        I = np.zeros_like(Phi)
        # cumulative trapezoid along axis=1
        if Ny > 1:
            seg = (Phi[:,1:]+Phi[:,:-1])/2.0*h
            I[:,1:] = np.cumsum(seg, axis=1)
        # Psi(x,y) = int_0^inf e^{-u^2/2-u(x+y)} I(x+u,y) du
        # need I at x+u for u in us -> requires I up to x=xs[-1]+Umax, but
        # our I array only covers xs range; since we padded Nx generously
        # for n_max iterations, at any given iteration the "core" region we
        # trust shrinks. We'll just clip: for ix such that ix*h+Umax exceeds
        # domain, skip (those x's are in the padding we don't need this
        # iteration anyway for the FINAL answer, only intermediate).
        Psi = np.zeros_like(Phi)
        kernel = np.exp(-us**2/2.0)  # e^{-u^2/2}, the u(x+y) part applied per (x,y)
        for iy, y in enumerate(ys):
            # for each x, Psi(x,y) = sum_u kernel(u)*exp(-u*(x+y)) * I(x+u,y) * h  (trapz)
            for ix in range(Nx):
                iu_max = min(Nu, Nx-ix)
                if iu_max < 2:
                    Psi[ix,iy] = 0.0
                    continue
                uu = us[:iu_max]
                w = kernel[:iu_max]*np.exp(-uu*(xs[ix]+y))
                vals = w*I[ix:ix+iu_max, iy]
                Psi[ix,iy] = np.trapezoid(vals, dx=h)
        # W(x,y) = (1-eps(x+y))*Psi + eps*I
        W = (1.0 - eps*(xs[:,None]+ys[None,:]))*Psi + eps*I
        # Phi_new(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv
        Phi_new = np.exp(-ys[None,:]/eps)*np.ones((Nx,1))
        for iy, y in enumerate(ys):
            if iy == 0:
                continue
            vs_idx = np.arange(iy+1)  # v = 0..y step h
            vvals = vs_idx*h
            wkernel = np.exp(-vvals/eps)
            for ix in range(Nx):
                iv_max = iy+1
                if ix+iv_max > Nx:
                    iv_max = Nx-ix
                if iv_max < 2:
                    continue
                # W(x+v, y-v): x index ix+iv, y index iy-iv
                vals = np.array([W[ix+iv, iy-iv] for iv in range(iv_max)])
                integ = np.trapezoid(wkernel[:iv_max]*vals, dx=h)
                Phi_new[ix, iy] = np.exp(-y/eps) + integ/eps
        return Phi_new

    Phis = [Phi.copy()]
    for n in range(1, n_max+1):
        Phi = step(Phi)
        Phis.append(Phi.copy())
        if verbose:
            print(f"  iter {n} done")

    return xs, ys, Phis, eps

if __name__ == "__main__":
    import sys
    c = 100
    h = 0.2   # coarser than target's h=0.1, for tractable runtime in this check
    ymax_track = 2.0   # track y up to 2.0 (smaller than target's y up to 6, for runtime)
    n_max = 8
    print(f"Running independent grid Neumann iteration: c={c}, h={h}, ymax={ymax_track}, n_max={n_max}")
    xs, ys, Phis, eps = run(c, h, ymax_track, n_max, Umax=4.0)
    ix0 = 0  # x=0
    print(f"eps={eps}")
    for ytest in [0.4, 1.0, 2.0]:
        iy = int(round(ytest/h))
        seq = [Phis[n][ix0, iy] for n in range(n_max+1)]
        print(f"\ny={ys[iy]:.2f}: Phi^(n) sequence:")
        print("  " + ", ".join(f"{v:.6f}" for v in seq))
        diffs = [abs(seq[n]-seq[n-1]) for n in range(1, n_max+1)]
        print("  diffs: " + ", ".join(f"{d:.6e}" for d in diffs))
        ratios = [diffs[n]/diffs[n-1] if diffs[n-1] > 1e-300 else float('nan') for n in range(1, len(diffs))]
        print("  successive-diff ratios: " + ", ".join(f"{r:.4f}" for r in ratios))
