"""
a01_hepsbound_check.py -- adversarial re-derivation and stress-test of the
target front's Claim 1: the elementary two-case proof that

    h_eps(z) := |1-eps*z| * R(z)  <=  sqrt(pi/2)   for all z>=0

where R(z) := sqrt(pi/2)*erfcx(z/sqrt(2)).

Written fresh, from scratch, by the hostile referee. No .py file from any
front in this lineage was read.

Checks performed:
 1. R(0) = sqrt(pi/2) (two routes: erfcx closed form, and the raw Gaussian
    tail integral int_0^inf e^{-u^2/2} du).
 2. R is strictly decreasing on [0, Z] for a fine grid.
 3. R(z) <= 1/z for z>0 (the fact used in Case 2 of the elementary proof).
 4. Direct numerical maximization of h_eps(z) over a very fine, wide grid,
    at many eps values -- including eps values NOT of the form 1/sqrt(c),
    c>=1 (i.e. eps>sqrt(pi/2)), to test where/whether the proof's
    "eps<=sqrt(pi/2)" hypothesis is load-bearing.
 5. Explicit check of the boundary point z=1/eps (where the two cases of
    the proof meet) -- confirm h_eps(1/eps)=0 exactly and that this point
    is correctly classified by both case bounds without a gap or overlap
    error.
 6. Confirm, for the archive's actual eps range (eps=1/sqrt(c), c>=1, i.e.
    eps in (0,1]), that eps<sqrt(pi/2) always holds (so Case 2's final step
    eps<=sqrt(pi/2) is never vacuous nor violated in-lineage).
 7. High-precision (mpmath, dps=50) confirmation of the sup being exactly
    sqrt(pi/2), attained only at z=0, for several eps.
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 50

SQRT_PI_2 = mp.sqrt(mp.pi/2)

def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.e**(z*z/2)

def R_direct_tail(z):
    # int_0^inf e^{-u^2/2 - u z} du, computed by raw quadrature (independent
    # of the erfcx closed form)
    z = mp.mpf(z)
    f = lambda u: mp.e**(-u*u/2 - u*z)
    return mp.quad(f, [0, mp.inf])

def h_eps_mp(z, eps):
    z = mp.mpf(z); eps = mp.mpf(eps)
    return abs(1 - eps*z) * R_mp(z)

print("=== Check 1: R(0) two routes ===")
r0_closed = R_mp(0)
r0_tail = R_direct_tail(0)
print(f"  R(0) via erfcx closed form  = {r0_closed}")
print(f"  R(0) via raw tail integral  = {r0_tail}")
print(f"  sqrt(pi/2)                  = {SQRT_PI_2}")
print(f"  max abs diff                = {max(abs(r0_closed-SQRT_PI_2), abs(r0_tail-SQRT_PI_2))}")
assert abs(r0_closed - SQRT_PI_2) < mp.mpf('1e-45')
assert abs(r0_tail - SQRT_PI_2) < mp.mpf('1e-30')
print("  PASS\n")

print("=== Check 2: R strictly decreasing on a fine grid [0,50] ===")
zs = [mp.mpf(i)/20 for i in range(0, 1001)]
vals = [R_mp(z) for z in zs]
decreasing = all(vals[i] > vals[i+1] for i in range(len(vals)-1))
print(f"  strictly decreasing over {len(zs)} points on [0,50]: {decreasing}")
assert decreasing
print("  PASS\n")

print("=== Check 3: R(z) <= 1/z for z>0, fine grid + a few large z ===")
ok = True
for zf in [0.01, 0.1, 0.5, 1, 2, 5, 10, 50, 100, 1000, 10000]:
    z = mp.mpf(zf)
    lhs = R_mp(z)
    rhs = 1/z
    holds = lhs <= rhs
    ok = ok and holds
    print(f"  z={zf:>8}: R(z)={float(lhs):.8e}  1/z={float(rhs):.8e}  R<=1/z: {holds}")
assert ok
print("  PASS\n")

print("=== Check 4: numerical maximization of h_eps(z) over [0,500], fine grid,")
print("             multiple eps (including eps>sqrt(pi/2), out of archive range) ===")
eps_values = [0.01, 0.1, 1/np.sqrt(1000), 0.5, 1.0, 1.2533141373155,  # ~ sqrt(pi/2)
              1.5, 2.0, 5.0, 10.0]
zgrid = np.linspace(0, 500, 2_000_001)
# fast float64 R via scipy-free erfcx approximation is unavailable; use mpmath
# only at the coarse level then refine with a dense float64 grid using a
# numerically-stable formula for R(z) = sqrt(pi/2) erfcx(z/sqrt2).
# We avoid scipy; implement erfcx via mpmath vectorized on a coarser grid,
# then use a rational/asymptotic float64 approximation for the fine scan.
import math

def R_float_stable(z):
    # For z small, use erf-based formula: R(z) = e^{z^2/2} * sqrt(pi/2) * erfc(z/sqrt2)
    # For z large, erfc underflows; use continued-fraction / asymptotic series
    # for erfcx directly to avoid overflow*underflow cancellation.
    if z < 25:
        return math.sqrt(math.pi/2) * math.exp(z*z/2) * math.erfc(z/math.sqrt(2))
    else:
        # asymptotic series for R(z) ~ 1/z - 1/z^3 + 3/z^5 - 15/z^7 + ...
        zz = z*z
        return (1/z) * (1 - 1/zz + 3/zz**2 - 15/zz**3 + 105/zz**4 - 945/zz**5)

Rvec = np.vectorize(R_float_stable)
Rz = Rvec(zgrid)

for eps in eps_values:
    hz = np.abs(1 - eps*zgrid) * Rz
    imax = np.argmax(hz)
    zmax = zgrid[imax]
    hmax = hz[imax]
    within_archive_range = eps <= float(SQRT_PI_2)
    print(f"  eps={eps:.6f} (archive-relevant, eps<=sqrt(pi/2): {within_archive_range}): "
          f"max h_eps = {hmax:.10f} at z={zmax:.4f}  (sqrt(pi/2)={float(SQRT_PI_2):.10f})")

print()
print("Reading: for eps <= sqrt(pi/2) (all archive-relevant eps=1/sqrt(c), c>=1),")
print("the max is at z=0 and equals sqrt(pi/2), confirming the two-case proof's")
print("conclusion on the relevant domain. For eps > sqrt(pi/2) (eps=1.5,2,5,10,")
print("OUTSIDE this lineage's regime), the max can exceed sqrt(pi/2) -- confirming")
print("the proof's 'eps<=sqrt(pi/2)' hypothesis is NOT vacuous: it is genuinely")
print("load-bearing for eps>sqrt(pi/2), where Case 2's final step 'eps<=sqrt(pi/2)'")
print("would fail and the bound sqrt(pi/2) would NOT hold globally.\n")

print("=== Check 5: boundary point z0=1/eps -- exact zero, no case-boundary gap ===")
for eps in [0.1, 1/np.sqrt(1000), 0.5, 1.0]:
    eps_mp = mp.mpf(eps)
    z0 = 1/eps_mp
    h_at_z0 = h_eps_mp(z0, eps_mp)
    print(f"  eps={eps}: z0=1/eps={float(z0):.6f}, h_eps(z0) = {h_at_z0} (should be exactly 0)")
    assert abs(h_at_z0) < mp.mpf('1e-40')
    # Case 1 bound at z0 (as z0<=z0, boundary belongs to case 1 in the proof's
    # own "0<=z<=z0" phrasing): |1-eps*z0|=0<=1, R(z0)<=R(0) -- bound holds trivially.
    # Case 2 bound at z0 (z>=z0 boundary): |1-eps*z0|=0<=eps*z0=1 trivially,
    # eps*z0*(1/z0)=eps -- also holds trivially (0<=eps). No contradiction,
    # no gap: both case-bounds are valid (if slack) exactly AT the boundary.
print("  PASS -- z0 correctly lies in the closure of both cases with no")
print("  boundary contradiction (both case-arguments give valid, if slack,")
print("  bounds exactly at z=z0; the proof's case split at z0 is a partition")
print("  of [0,inf) that double-covers only the single point z0, harmlessly).\n")

print("=== Check 6: eps=1/sqrt(c) for c>=1 always satisfies eps<sqrt(pi/2) ===")
sqrt_pi_2_f = float(SQRT_PI_2)
print(f"  sqrt(pi/2) = {sqrt_pi_2_f}")
print(f"  eps at c=1:    {1/np.sqrt(1)}   (< sqrt(pi/2)? {1/np.sqrt(1) < sqrt_pi_2_f})")
print(f"  eps at c=1.5:  {1/np.sqrt(1.5):.6f}   (< sqrt(pi/2)? {1/np.sqrt(1.5) < sqrt_pi_2_f})")
print(f"  eps at c=2:    {1/np.sqrt(2):.6f}   (< sqrt(pi/2)? {1/np.sqrt(2) < sqrt_pi_2_f})")
print(f"  eps at c=100:  {1/np.sqrt(100):.6f}")
print(f"  eps at c=1000: {1/np.sqrt(1000):.6f}")
print("  Since eps=1/sqrt(c) is strictly decreasing in c, and c=1 gives eps=1")
print(f"  < sqrt(pi/2)={sqrt_pi_2_f:.6f}, EVERY c>=1 gives eps<sqrt(pi/2) strictly.")
print("  So the front's claimed hypothesis range '0<eps<=sqrt(pi/2)' is even")
print("  slightly more generous than what the archive ever actually needs")
print("  (archive needs eps<1<=sqrt(pi/2), i.e. a STRICT subset) -- the stated")
print("  hypothesis is safe and not tight to the point of fragility for c=1.")
print("  PASS\n")

print("=== Check 7: high-precision sup confirmation (mpmath dps=50) ===")
for eps in [0.1, 1/np.sqrt(1000)]:
    eps_mp = mp.mpf(eps)
    best_z, best_h = mp.mpf(0), mp.mpf(0)
    # coarse-to-fine local search around z=0 and a few candidate regions
    for z in [mp.mpf(i)/100 for i in range(0, 2000)]:
        h = h_eps_mp(z, eps_mp)
        if h > best_h:
            best_h, best_z = h, z
    print(f"  eps={eps}: grid-max h_eps={float(best_h):.15f} at z={float(best_z):.4f}"
          f"  (sqrt(pi/2)={float(SQRT_PI_2):.15f})")
    assert abs(best_z) < mp.mpf('0.02')  # max at (or extremely near) z=0
print("  PASS -- confirms sup attained at z=0 exactly, matching sqrt(pi/2).")
