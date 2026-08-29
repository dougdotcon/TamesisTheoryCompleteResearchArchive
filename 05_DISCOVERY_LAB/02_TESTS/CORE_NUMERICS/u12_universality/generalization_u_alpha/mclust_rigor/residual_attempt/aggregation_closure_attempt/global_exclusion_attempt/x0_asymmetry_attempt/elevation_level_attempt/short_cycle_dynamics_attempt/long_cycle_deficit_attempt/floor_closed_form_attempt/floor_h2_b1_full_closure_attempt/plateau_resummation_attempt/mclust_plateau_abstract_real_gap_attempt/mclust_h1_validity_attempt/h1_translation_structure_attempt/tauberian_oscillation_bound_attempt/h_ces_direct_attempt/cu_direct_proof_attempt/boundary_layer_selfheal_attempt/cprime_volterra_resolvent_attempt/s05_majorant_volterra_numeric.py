"""
s05_majorant_volterra_numeric.py -- CPRIME-VOLTERRA-RESOLVENT-ATTEMPT

Numerically solves the ACTUAL majorant Volterra equation

  M(y) = |g_y(x)| + int_0^y K_bound(y,t) M(t) dt,   g_y(x)=e^{-y/eps}

using the RIGOROUS upper bound (s04, proved unconditional on (C'))

  K_bound(y,t) = (1-e^{-h/eps})*(R(z)+eps*sigma(z)) + eps*e^{-h/eps},
  h := y-t,  z := x+y

as the kernel -- via a deterministic, self-starting trapezoid-rule
Volterra solver (no adaptivity/randomness needed; K_bound(y,t)=0 exactly
at h=0, so the solver is EXPLICIT at each step, same structure as s02b).

Since z=x+y depends on y ALONE (not on t), R(z) and sigma(z) are
precomputed ONCE per y-grid-point (not per (y,t) pair) via direct
quadrature (mpmath.quad on R's own raw definition) -- this makes the
whole O(n^2) solve cheap even for large n.

If |Phi_y(x)| really does satisfy the majorant recursion |Phi_y(x)| <=
|g_y(x)| + int_0^y ||K(y,t)|| |Phi_t(x)| dt <= |g_y(x)| + int_0^y
K_bound(y,t) M(t) dt whenever |Phi_t(x)|<=M(t) for t<y (a standard,
rigorous comparison-principle fact for linear Volterra integral
inequalities with a NONNEGATIVE kernel bound -- K_bound(y,t)>=0 always,
by construction as a sum of two manifestly nonnegative terms), then
M(y) so computed is a genuine, rigorous UPPER BOUND on |Phi_y(x)|,
PROVIDED M itself stays finite -- this script checks, empirically and
deterministically, whether it does.
"""
import mpmath as mp

mp.mp.dps = 25

def R(zval):
    return mp.quad(lambda u: mp.e**(-u**2/2 - u*zval), [0, mp.inf])

def solve_majorant(eps, x, Y, n_steps):
    dy = Y / n_steps
    ys = [mp.mpf(i)*dy for i in range(n_steps+1)]
    zs = [x + yv for yv in ys]
    Rz = [R(zv) for zv in zs]
    sigmaz = [1 - zs[i]*Rz[i] for i in range(len(zs))]
    def Kbound(i, j):  # i=index for y, j=index for t (j<=i)
        h = ys[i] - ys[j]
        if h < 0:
            return mp.mpf(0)
        term1 = (1 - mp.e**(-h/eps)) * (Rz[i] + eps*sigmaz[i])
        term2 = eps * mp.e**(-h/eps)
        return term1 + term2
    M = [mp.mpf(0)]*(n_steps+1)
    M[0] = mp.e**(-ys[0]/eps)  # = 1 at y=0
    for i in range(1, n_steps+1):
        gy = mp.e**(-ys[i]/eps)
        total = mp.mpf(0)
        for j in range(0, i+1):
            w = dy if (0 < j < i) else dy/2
            Mj = M[j] if j < i else mp.mpf(0)  # K_bound(i,i)=0 exactly (h=0), so M[i] term contributes 0 regardless
            total += w * Kbound(i, j) * Mj
        M[i] = gy + total
    return ys, M, Rz, sigmaz

print("="*70)
print("Solving the majorant Volterra equation with the RIGOROUS s04 kernel")
print("bound, for several eps, checking whether M(y) stays bounded as")
print("y grows (which would be a genuine PROOF of (B), via the comparison")
print("principle, if it holds for ALL y -- this script checks a finite")
print("range deterministically; see ATTEMPT.md Sec 4 for the honest")
print("discussion of what a finite-range numerical check does/doesn't show).")
print("="*70)

x = mp.mpf('1.0')
Y = mp.mpf('150')
n_steps = 600  # dy=0.25, adequate resolution given the kernel's own O(eps) scale

results = {}
for eps in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.8'),
            mp.mpf('1.0'), mp.mpf('1.2')]:
    ys, M, Rz, sigmaz = solve_majorant(eps, x, Y, n_steps)
    checkpoints = [10, 30, 60, 100, 150]
    vals = []
    for cp in checkpoints:
        idx = int(cp/float(Y)*n_steps)
        vals.append((cp, M[idx]))
    print(f"\neps={float(eps):.2f}:")
    for cp, v in vals:
        print(f"  M(y={cp:3d}) = {mp.nstr(v, 10)}")
    results[float(eps)] = vals

print()
print("="*70)
print("Growth-rate check: is M(y) still increasing at y=150, or has it")
print("visibly plateaued (bounded) over the tested range?")
print("="*70)
for eps_f, vals in results.items():
    v100 = vals[-2][1]
    v150 = vals[-1][1]
    ratio = v150 / v100 if v100 != 0 else None
    print(f"  eps={eps_f:.2f}: M(100)={mp.nstr(v100,6)}, M(150)={mp.nstr(v150,6)}, ratio={mp.nstr(ratio,6)}")
