#!/usr/bin/env python3
# ym_lmc_full.py — compact, functional implementation: ROC + LMC + resolvent tracking + spectrum analysis

import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla, scipy.fft as fft, math, os, time
import matplotlib.pyplot as plt

# ---------- params (compact)
L = (4,4,4,4)            # (Lt,Lx,Ly,Lz)
Lt,Lx,Ly,Lz = L
PERIODIC = True
gamma_plus,gamma_zero,gamma_minus = 0.8,1.4,2.8
arith_beta = 0.06
diag_scale = 1.0
mollifier_widths = [1.0,0.5,0.25]   # simulate a -> 0
neigs = 8
use_fallback = True   # if no t_nodes.npy

# ---------- helpers
Nt = Lt*Lx*Ly*Lz
def lin_idx(t,x,y,z): return (((t%Lt)*Lx + (x%Lx))*Ly + (y%Ly))*Lz + (z%Lz)
def inv_idx(i):
    z = i%Lz; y=(i//Lz)%Ly; x=(i//(Ly*Lz))%Lx; t=i//(Lx*Ly*Lz); return t,x,y,z

# ---------- load / build LMC field (1D array length Nt) and mollify -> sigma^a on lattice
def load_or_build_tnodes(N):
    if os.path.exists("t_nodes.npy"):
        arr = np.load("t_nodes.npy").astype(float)
        if arr.size != N:
            arr = np.interp(np.linspace(0,arr.size-1,N), np.arange(arr.size), arr)
        return arr.copy()
    if not use_fallback:
        raise FileNotFoundError("t_nodes.npy missing")
    # fallback smooth pattern
    out = np.zeros(N)
    for i in range(N):
        t,x,y,z = inv_idx(i)
        out[i] = 0.6*np.sin(2*math.pi*x/Lx)+0.4*np.cos(2*math.pi*y/Ly)+0.3*math.sin(2*math.pi*z/Lz)
    return out

# ---------- discrete Fourier Hodge projectors for vector fields on lattice
# We implement scalar field model but produce projector-like channels via FFT of scalar -> use k-direction decomposition.
def build_hodge_projectors_scalar(Nt,shape):
    # shape = (Lt,Lx,Ly,Lz) -> we only use spatial 3D (x,y,z) Fourier per time-slice
    # Build per-site projector weights: P_grad (longitudinal), P_trans = 1-P_grad, P_zero = k==0 mask
    P_plus = np.zeros(Nt)
    P_zero = np.zeros(Nt)
    P_minus = np.zeros(Nt)
    # compute 3D k-grid once
    kx = 2*math.pi*np.fft.fftfreq(Lx)
    ky = 2*math.pi*np.fft.fftfreq(Ly)
    kz = 2*math.pi*np.fft.fftfreq(Lz)
    KK = np.zeros((Lx,Ly,Lz))
    for ix in range(Lx):
        for iy in range(Ly):
            for iz in range(Lz):
                KK[ix,iy,iz] = kx[ix]**2 + ky[iy]**2 + kz[iz]**2
    for t in range(Lt):
        for ix in range(Lx):
            for iy in range(Ly):
                for iz in range(Lz):
                    i = lin_idx(t,ix,iy,iz)
                    if KK[ix,iy,iz] == 0:
                        P_zero[i] = 1.0
                        P_plus[i] = 0.0
                        P_minus[i] = 0.0
                    else:
                        # pick longitudinal fraction ~1/(1+|k|) to model separation
                        frac = 1.0/(1.0 + math.sqrt(KK[ix,iy,iz]))
                        P_plus[i] = frac
                        P_minus[i] = 1.0 - frac
    # normalize so P_plus+P_zero+P_minus =1
    s = P_plus+P_minus+P_zero
    s[s==0]=1
    P_plus/=s; P_minus/=s; P_zero/=s
    return P_plus,P_zero,P_minus

# ---------- discrete Laplacian (periodic) sparse operator
def build_laplacian():
    rows,cols,data = [],[],[]
    for i in range(Nt):
        t,x,y,z = inv_idx(i)
        deg=0
        for dt,dx,dy,dz in ((1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),(0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1)):
            nt = (t+dt)%Lt if PERIODIC else t+dt
            nx = (x+dx)%Lx if PERIODIC else x+dx
            ny = (y+dy)%Ly if PERIODIC else y+dy
            nz = (z+dz)%Lz if PERIODIC else z+dz
            if 0<=nt<Lt and 0<=nx<Lx and 0<=ny<Ly and 0<=nz<Lz:
                j = lin_idx(nt,nx,ny,nz)
                rows.append(i); cols.append(j); data.append(-1.0)
                deg+=1
        rows.append(i); cols.append(i); data.append(deg)
    Lmat = sp.coo_matrix((data,(rows,cols)), shape=(Nt,Nt)).tocsr()
    return Lmat

# ---------- build K[σ] as -β * sqrt(σ) * Laplacian * sqrt(σ) (symmetric, models σ-dependent coupling)
def build_K_of_sigma(sigma, lap):
    s = np.sqrt(np.maximum(sigma,1e-12))
    S = sp.diags(s)
    K = -arith_beta * (S.dot(lap.dot(S)))
    return K

# ---------- build M from P projectors: M = γ+ P_plus + γ0 P_zero + γ- P_minus (diagonal)
def build_M_from_P(Pp,P0,Pm):
    diag = gamma_plus*Pp + gamma_zero*P0 + gamma_minus*Pm
    return sp.diags(diag, format='csr')

# ---------- norm-resolvent difference ||(H_a - z)^{-1} - (H - z)^{-1}||
def resolvent_norm_diff(Ha, H, z):
    I = sp.eye(Nt, format='csr')
    Ha_mz = Ha - z*I
    H_mz  = H  - z*I

    try:
        Ra = spla.spsolve(Ha_mz, sp.eye(Nt).toarray())
        R  = spla.spsolve(H_mz,  sp.eye(Nt).toarray())
        return np.linalg.norm(Ra - R, 2)
    except Exception:
        # power iteration fallback
        def matvec(v):
            x1 = spla.spsolve(Ha_mz, v)
            x2 = spla.spsolve(H_mz,  v)
            return x1 - x2
        v = np.random.randn(Nt); v/=np.linalg.norm(v)
        for _ in range(12):
            w = matvec(v)
            n = np.linalg.norm(w)
            if n == 0: return 0.0
            v = w/n
        return n

# ---------- spacing distribution and GUE compare (Wigner surmise for GUE)
def level_spacing_dist(evals, bins=30):
    s = np.diff(np.sort(evals))
    s = s/np.mean(s) if s.size>0 else s
    hist,edges = np.histogram(s, bins=bins, density=True)
    centers = 0.5*(edges[:-1]+edges[1:])
    # GUE approx (Wigner surmise for GUE)
    gue = (32.0/ (math.pi**2)) * centers**2 * np.exp(-4*centers**2/math.pi)
    return centers,hist,gue

# ---------- main: compute for mollifier widths (simulate a->0) and track resolvent + gap
def main():
    t0=time.time()
    t_nodes = load_or_build_tnodes(Nt)
    lap = build_laplacian()
    Pp,P0,Pm = build_hodge_projectors_scalar(Nt,L)
    M = build_M_from_P(Pp,P0,Pm)
    # baseline H using most-regular sigma (largest mollifier width)
    resolvent_diffs=[]
    gaps=[]
    eigen_collections=[]
    H_reference=None
    z = 1.0 + 0.1j  # resolvent point off-real axis
    for idx_a,a in enumerate(mollifier_widths):
        # mollify t_nodes in 4D via simple gaussian in spatial coords per-time-slice
        sigma = np.zeros(Nt)
        # map 1D t_nodes -> lattice by direct copy/interp
        if t_nodes.size == Nt:
            base = t_nodes.copy()
        else:
            base = np.interp(np.linspace(0,t_nodes.size-1,Nt), np.arange(t_nodes.size), t_nodes)
        # simple local smoothing by gaussian in index-space (cheap: convolution in 3D per slice via FFT)
        # reshape to (Lt,Lx,Ly,Lz)
        arr = base.reshape((Lt,Lx,Ly,Lz))
        # perform spatial FFT per time-slice
        for t in range(Lt):
            A = arr[t]
            A_k = fft.fftn(A)
            # gaussian filter in k-space
            kgrid = np.zeros_like(A_k, dtype=float)
            for ix in range(Lx):
                for iy in range(Ly):
                    for iz in range(Lz):
                        kx = np.fft.fftfreq(Lx)[ix]
                        ky = np.fft.fftfreq(Ly)[iy]
                        kz = np.fft.fftfreq(Lz)[iz]
                        ksq = kx*kx+ky*ky+kz*kz
                        kgrid[ix,iy,iz] = math.exp(- (2*math.pi*ksq) * (a**2))
            A_k_filtered = A_k * kgrid
            A_filtered = np.real(fft.ifftn(A_k_filtered))
            arr[t] = A_filtered
        sigma = arr.reshape(Nt)
        # build K and H
        K = build_K_of_sigma(sigma, lap)
        H = M + K
        # eigs
        kreq = min(neigs, Nt-2)
        try:
            vals, vecs = spla.eigsh(H, k=kreq, which='SA', tol=1e-8)
        except Exception:
            vals = np.linalg.eigvalsh(H.toarray())
            vals = np.sort(vals)[:kreq]
        vals = np.sort(np.real(vals))
        eigen_collections.append(vals)
        gap = vals[1]-vals[0] if vals.size>1 else np.nan
        gaps.append(gap)
        # resolvent norms
        if idx_a==0:
            H_reference = H
            resolvent_diffs.append(0.0)
        else:
            diff = resolvent_norm_diff(H, H_reference, z)
            resolvent_diffs.append(diff)
    # final analysis: spacing for last H
    centers,hist,gue = level_spacing_dist(eigen_collections[-1])
    # plot compact
    plt.figure(figsize=(8,3))
    plt.subplot(1,3,1)
    plt.plot(mollifier_widths, gaps,'o-'); plt.xlabel('a'); plt.title('gap vs a')
    plt.subplot(1,3,2)
    plt.plot(mollifier_widths, resolvent_diffs,'o-'); plt.xlabel('a'); plt.title('||R_a-R_ref||')
    plt.subplot(1,3,3)
    if centers.size>0:
        plt.bar(centers, hist, width=centers[1]-centers[0], alpha=0.6, label='emp')
        plt.plot(centers, gue, 'r--', label='GUE-surmise')
        plt.legend()
    plt.tight_layout()
    plt.savefig("ym_analysis.png", dpi=180)
    # print summary
    print("Runtime: {:.2f}s".format(time.time()-t0))
    for i,a in enumerate(mollifier_widths):
        print(f"a={a:.4g} gap={gaps[i]:.6g} resdiff={resolvent_diffs[i]:.6g}")
    print("smallest evals (last a):", eigen_collections[-1][:min(8,len(eigen_collections[-1]))])
    plt.show()

if __name__=="__main__":
    main()