"""
s02b_renewal_numeric.py -- CPRIME-VOLTERRA-RESOLVENT-ATTEMPT

Independent NUMERIC confirmation (mpmath, deterministic quadrature, no
sampling/no randomness) that the majorant renewal equation

  M(y) = 1 + int_0^y k(y-t) M(t) dt,   k(h) = c*(1-exp(-h/eps))

genuinely grows like A*exp(s_+ * y) for large y, with s_+ = s_+(c,eps)
exactly as derived in s02's Part 2/3 (closed form
(sqrt(1+4*c*eps)-1)/(2*eps)) -- via DIRECT numerical solution of the
Volterra integral equation by a simple deterministic self-starting
quadrature (trapezoid-rule Volterra solver, fixed step, no adaptivity
needed since the solution and kernel are smooth), NOT by trusting the
Laplace-transform algebra alone.
"""
import mpmath as mp

mp.mp.dps = 30

def s_plus(c, eps):
    return (mp.sqrt(1 + 4*c*eps) - 1) / (2*eps)

def solve_renewal(c, eps, Y, n_steps):
    """Solve M(y) = 1 + int_0^y k(y-t) M(t) dt via a simple trapezoid-rule
    self-starting Volterra solver on a uniform grid [0,Y], n_steps intervals.
    k(h) = c*(1-exp(-h/eps))."""
    dy = Y / n_steps
    ys = [mp.mpf(i) * dy for i in range(n_steps + 1)]
    M = [mp.mpf(0)] * (n_steps + 1)
    M[0] = mp.mpf(1)  # M(0) = 1 + int_0^0(...) = 1
    kfun = lambda h: c * (1 - mp.e**(-h/eps))
    for n in range(1, n_steps + 1):
        yn = ys[n]
        # trapezoid rule on int_0^{yn} k(yn-t) M(t) dt using M[0..n-1] (M[n] unknown)
        # implicit trapezoid: unknown M[n] appears with weight (dy/2)*k(0)=0 since k(0)=0
        # so it's actually EXPLICIT here (no need to solve for M[n] implicitly)
        total = mp.mpf(0)
        for j in range(0, n + 1):
            tj = ys[j]
            w = dy if (0 < j < n) else dy/2
            total += w * kfun(yn - tj) * (M[j] if j < n else mp.mpf(0))
            # M[n] unknown skipped (weight * k(0) = weight*0 = 0 anyway)
        M[n] = 1 + total
    return ys, M

print("="*70)
print("Direct Volterra-quadrature solve of the renewal majorant equation,")
print("cross-checked against the closed-form Malthusian rate s_+(c,eps)")
print("="*70)

for eps in [mp.mpf('0.5'), mp.mpf('1.0')]:
    c = eps  # ||K_B(h)|| case
    sp_val = s_plus(c, eps)
    Y = mp.mpf(30)
    n_steps = 3000
    ys, M = solve_renewal(c, eps, Y, n_steps)
    # Estimate the empirical growth rate from log(M) slope over the LAST
    # quarter of the range (where the exponential term should dominate
    # over the transient/particular-solution contribution).
    i1 = int(n_steps * 0.75)
    i2 = n_steps
    y1, y2 = ys[i1], ys[i2]
    M1, M2 = M[i1], M[i2]
    empirical_rate = (mp.log(M2) - mp.log(M1)) / (y2 - y1)
    print(f"\neps={float(eps):.3f}, c=eps: predicted s_+ = {float(sp_val):.8f}")
    print(f"  M(y) at y={float(y1):.2f}: {float(M1):.6e}")
    print(f"  M(y) at y={float(y2):.2f}: {float(M2):.6e}")
    print(f"  empirical growth rate (log-slope over last quarter): {float(empirical_rate):.8f}")
    rel_err = abs(empirical_rate - sp_val) / sp_val
    print(f"  relative error vs predicted s_+: {float(rel_err):.3e}")
    assert rel_err < mp.mpf('1e-3'), f"empirical rate does not match predicted s_+ (eps={eps})"
    print("  PASS: empirical exponential growth rate matches closed-form s_+ to <1e-3.")

print()
print("="*70)
print("Sanity check: M(y) genuinely EXCEEDS any fixed bound as y grows")
print("(i.e. is NOT merely a slow transient) -- confirms the majorant is")
print("truly unbounded, not just 'looks big at moderate y'.")
print("="*70)
eps = mp.mpf('0.5')
c = eps
N_SANITY = 800  # reduced from an initial 4000: at dps=30 the O(n^2) trapezoid
# loop timed out (>2 min) at n_steps=4000 over Y=40 -- caught by direct
# wall-clock observation (Sec 5, Self-caught issues, Issue 2). 800 steps
# over Y=40 (dy=0.05) is still far finer than needed for a log-slope
# sanity check and completes in well under a minute.
ys, M = solve_renewal(c, eps, mp.mpf(40), N_SANITY)
for target_y in [5, 10, 20, 30, 40]:
    idx = int(target_y / 40 * N_SANITY)
    print(f"  y={target_y:2d}: M(y) = {float(M[idx]):.4e}")
assert M[-1] > 100 * M[int(N_SANITY*0.25)]
print("  M(y) grows by >100x from y=10 to y=40 -- confirms genuine unbounded")
print("  exponential growth, not a bounded transient. PASS")

print()
print("ALL s02b NUMERICAL CHECKS PASSED.")
