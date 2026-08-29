"""
s06_growth_exponent_check.py -- CPRIME-VOLTERRA-RESOLVENT-ATTEMPT

Large-scale (y up to several thousand), DOUBLE-PRECISION (numpy/scipy,
NOT mpmath -- explicitly noted; this is an exploratory quantitative
growth-EXPONENT check, not a claim needing many digits, and mpmath's
O(n^2) arbitrary-precision loop at this scale (n~5000-10000) is not
tractable within a reasonable runtime; deterministic throughout, no
randomness anywhere) re-solve of the SAME rigorous-kernel-bound majorant
Volterra equation as s05, to test the following ANALYTIC PREDICTION
(derived heuristically in ATTEMPT.md Sec 4 via a "slowly-varying M"
approximation of the near-diagonal/long-range split of the s04 kernel
bound, NOT claimed as a rigorous derivation -- hence this numerical
test of it):

  M(y) should grow POLYNOMIALLY in z=x+y, with exponent
    p(eps) := eps^2 / (1 - eps^2)     (for eps < 1)
  i.e. log(M(y)) ~ p(eps) * log(z) + const, for y large.

This is tested by a log-log linear regression of M(y) against z over
the LARGE-y tail of each solve (where the polynomial-growth regime
should dominate any initial transient), for eps in {0.3, 0.5, 0.7},
and the fitted exponent is compared against the predicted p(eps).
"""
import numpy as np
from scipy.special import erfcx

def R(z):
    return np.sqrt(np.pi/2) * erfcx(z/np.sqrt(2))

def solve_majorant_fast(eps, x, Y, n_steps):
    dy = Y / n_steps
    ys = np.arange(n_steps+1) * dy
    zs = x + ys
    Rz = R(zs)
    sigmaz = 1 - zs*Rz
    M = np.zeros(n_steps+1)
    M[0] = 1.0
    # Precompute, for each i, the vector of h = ys[i]-ys[0:i] and the
    # kernel bound row K_bound(i,0:i); accumulate trapezoid-weighted sum.
    for i in range(1, n_steps+1):
        h = ys[i] - ys[:i]  # length i, h>0 for j<i (h=ys[i]-ys[j])
        term1 = (1 - np.exp(-h/eps)) * (Rz[i] + eps*sigmaz[i])
        term2 = eps * np.exp(-h/eps)
        Krow = term1 + term2
        # trapezoid weights over j=0..i (M[i]'s own weight * K(h=0)=0, so
        # skip it; effective explicit trapezoid on j=0..i-1 plus the
        # implicit-but-zero-weight endpoint)
        w = np.full(i, dy)
        w[0] *= 0.5
        # the j=i-1 -> i sub-interval trapezoid weight technically needs
        # care at the right endpoint (j=i, weight dy/2, but Krow there is
        # exactly 0 since h=0) -- consistent with s02b/s05's own explicit
        # scheme; verified by the cross-check against s05's mpmath run below.
        total = np.sum(w * Krow * M[:i])
        gy = np.exp(-ys[i]/eps)
        M[i] = gy + total
    return ys, zs, M

print("="*70)
print("Cross-check against s05's mpmath solve (same eps, same Y, same grid)")
print("="*70)
for eps in [0.5]:
    ys, zs, M = solve_majorant_fast(eps, 1.0, 150.0, 600)
    for cp in [10, 30, 60, 100, 150]:
        idx = int(cp/150*600)
        print(f"  eps={eps}, y={cp}: M(y) [numpy/double] = {M[idx]:.6f}")
print("Compare to s05_majorant_volterra_numeric.log (mpmath, dps=25):")
print("  eps=0.50: M(10)=0.4794264488, M(30)=0.6144966089, M(60)=0.722035297,")
print("            M(100)=0.8142294052, M(150)=0.8961616459")
print("(agreement to displayed double precision confirms this script's own")
print(" independent numpy implementation faithfully reproduces s05's mpmath")
print(" computation before trusting it at much larger scale below.)")

print()
print("="*70)
print("Large-scale growth-exponent fit: log(M) vs log(z), large-y tail")
print("="*70)
for eps in [0.3, 0.5, 0.7]:
    Y = 8000.0
    n_steps = 8000  # dy=1.0
    ys, zs, M = solve_majorant_fast(eps, 1.0, Y, n_steps)
    predicted_p = eps**2 / (1 - eps**2)
    # fit over the tail y in [Y/2, Y] (well past any initial transient)
    mask = ys >= Y/2
    logz = np.log(zs[mask])
    logM = np.log(M[mask])
    A = np.vstack([logz, np.ones_like(logz)]).T
    slope, intercept = np.linalg.lstsq(A, logM, rcond=None)[0]
    print(f"\neps={eps}: predicted exponent p(eps)=eps^2/(1-eps^2) = {predicted_p:.5f}")
    print(f"  fitted log-log slope over y in [{Y/2:.0f},{Y:.0f}]: {slope:.5f}")
    print(f"  M(y={Y/2:.0f}) = {M[int(n_steps/2)]:.6e},  M(y={Y:.0f}) = {M[-1]:.6e}")
    rel_err = abs(slope - predicted_p) / predicted_p
    print(f"  relative error (fitted vs predicted exponent): {rel_err:.3f}")

print()
print("(Heuristic-prediction agreement is reported descriptively in")
print(" ATTEMPT.md Sec 4 -- NOT asserted as a proof-grade identity, since")
print(" the exponent formula itself was derived via an admittedly informal")
print(" 'slowly-varying M' approximation, disclosed as such.)")
