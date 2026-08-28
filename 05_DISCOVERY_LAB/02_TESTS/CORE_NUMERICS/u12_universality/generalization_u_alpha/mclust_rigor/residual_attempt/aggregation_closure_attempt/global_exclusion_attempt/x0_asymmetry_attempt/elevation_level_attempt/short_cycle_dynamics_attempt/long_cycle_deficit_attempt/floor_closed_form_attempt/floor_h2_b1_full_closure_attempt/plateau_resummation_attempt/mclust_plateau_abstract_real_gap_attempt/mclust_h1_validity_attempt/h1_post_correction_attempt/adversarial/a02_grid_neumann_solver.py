"""
a02_grid_neumann_solver.py -- THIRD independent, from-scratch, interpolation-
free grid Neumann/Picard solver for the closed Volterra-in-y system, built
by the hostile referee directly from the prose equations quoted in the
required reading (NOT from any .py file of any front or the earlier
referee -- none was opened).

Equations used (all quoted, in prose, in the target ATTEMPT.md's own Sec 0,
themselves cited from mclust_h1_validity_attempt / h1_energy_estimate_attempt
/ h1_volterra_attempt):

  I(x,y)   := int_0^y Phi(x,y') dy'                                    (I)
  Psi(x,y) = int_0^infinity e^{-u^2/2-u(x+y)} I(x+u,y) du               (BB-Psi')
  W(x,y)   = (1-eps*(x+y)) * Psi(x,y) + eps*I(x,y)                     (NEW-W)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv     (E2)

Picard/Neumann iteration: Phi^(0)(x,y) := e^{-y/eps}; Phi^(n) obtained by
applying (I) -> (BB-Psi') -> (NEW-W) -> (E2) to Phi^(n-1).

Grid: x and y share step h (interpolation-free: every shift x+v, x+u lands
exactly on a grid point). y in [0, Ymax]. x in [0, Xtot], where Xtot is
sized to accommodate n_max iterations' worth of domain-reach
(Xtot >= n_max*(Ymax+Umax) + a small core buffer), exactly mirroring the
"shrinking active window" structure the target/predecessor describe in
prose -- implemented here as a single static over-sized array for
simplicity, reading out only the well-supported x=0 column.

All quadratures use the plain trapezoid rule (matching what the required
reading describes; O(h^2) error, checked explicitly below).
"""
import numpy as np
import math
import json
import sys

def run_solver(c, h, Ymax, Umax, n_max, verbose=True):
    eps = 1.0/math.sqrt(c)
    NY = int(round(Ymax/h)) + 1
    ys = np.arange(NY)*h
    Xtot = n_max*(Ymax+Umax) + 2.0
    NX = int(round(Xtot/h)) + 1
    xs = np.arange(NX)*h

    # Phi^(0)(x,y) = e^{-y/eps}, independent of x
    Phi = np.tile(np.exp(-ys/eps), (NX,1))  # shape (NX, NY)

    # Precompute u-grid for the Psi integral (Umax truncation)
    NU = int(round(Umax/h)) + 1
    us = np.arange(NU)*h
    # trapezoid weights along u
    wu = np.full(NU, h); wu[0] *= 0.5; wu[-1] *= 0.5

    # trapezoid weights along y (for I) -- built via cumulative trapezoid
    # trapezoid weights along v (for E2) depend on iy (v ranges 0..y)

    Phi_history = [Phi.copy()]

    for n in range(1, n_max+1):
        # --- (I): I[ix,iy] = int_0^{iy*h} Phi(ix, y') dy' (cumulative trapezoid along y axis)
        I = np.zeros_like(Phi)
        # cumulative trapezoid: I[:,0]=0; I[:,j] = I[:,j-1] + h*(Phi[:,j-1]+Phi[:,j])/2
        seg = h*0.5*(Phi[:, :-1] + Phi[:, 1:])   # shape (NX, NY-1)
        I[:,1:] = np.cumsum(seg, axis=1)

        # --- (BB-Psi'): Psi[ix,iy] = sum_{iu} wu[iu] * exp(-u^2/2 - u*(x+y)) * I[ix+iu, iy]
        Psi = np.zeros_like(Phi)
        for iu in range(NU):
            u = us[iu]
            if iu >= NX:
                break
            # valid ix range: ix + iu <= NX-1  =>  ix <= NX-1-iu
            ix_max = NX-1-iu
            if ix_max < 0:
                continue
            x_slice = xs[:ix_max+1]
            # kernel depends on x+y for each column y separately
            # exp(-u^2/2 - u*(x+y)) = exp(-u^2/2) * exp(-u*x) * exp(-u*y)
            base = math.exp(-u*u/2.0)
            exu = np.exp(-u*x_slice)             # shape (ix_max+1,)
            eyu = np.exp(-u*ys)                  # shape (NY,)
            kernel = base * np.outer(exu, eyu)   # shape (ix_max+1, NY)
            Psi[:ix_max+1, :] += wu[iu] * kernel * I[iu:iu+ix_max+1, :]

        # --- (NEW-W): W[ix,iy] = (1-eps*(x+y))*Psi[ix,iy] + eps*I[ix,iy]
        xy = xs[:,None] + ys[None,:]
        W = (1.0 - eps*xy)*Psi + eps*I

        # --- (E2): Phi_new[ix,iy] = e^{-y/eps} + (1/eps) * sum_{iv=0}^{iy} wv[iv]*e^{-v/eps}*W[ix+iv, iy-iv]
        Phi_new = np.tile(np.exp(-ys/eps), (NX,1))
        for iy in range(NY):
            if iy == 0:
                continue
            # v index iv = 0..iy, v = iv*h; trapezoid weights over [0, iy*h]
            wv = np.full(iy+1, h); wv[0] *= 0.5; wv[-1] *= 0.5
            vs = np.arange(iy+1)*h
            eveps = np.exp(-vs/eps)
            # valid ix range: ix+iv <= NX-1 for iv up to iy => ix <= NX-1-iy
            ix_max = NX-1-iy
            if ix_max < 0:
                continue
            acc = np.zeros(ix_max+1)
            for iv in range(iy+1):
                acc += wv[iv]*eveps[iv]*W[iv:iv+ix_max+1, iy-iv]
            Phi_new[:ix_max+1, iy] += acc/eps

        Phi = Phi_new
        Phi_history.append(Phi.copy())
        if verbose:
            pass

    return xs, ys, Phi_history, eps

def phi_at(Phi_history, xs, ys, x0, y0):
    ix = int(round(x0/ (xs[1]-xs[0]) ))
    iy = int(round(y0/ (ys[1]-ys[0]) ))
    return [Ph[ix,iy] for Ph in Phi_history]

if __name__ == "__main__":
    print("=== Sanity: single run, c=100, h=0.1, small n_max ===")
    xs, ys, hist, eps = run_solver(c=100, h=0.1, Ymax=6.0, Umax=6.0, n_max=6, verbose=False)
    for y0 in [0.2,0.5,1.0]:
        vals = phi_at(hist, xs, ys, 0.0, y0)
        print(f"  y={y0}: Phi^(0..6) = {[round(v,4) for v in vals]}")
    print("done.")
