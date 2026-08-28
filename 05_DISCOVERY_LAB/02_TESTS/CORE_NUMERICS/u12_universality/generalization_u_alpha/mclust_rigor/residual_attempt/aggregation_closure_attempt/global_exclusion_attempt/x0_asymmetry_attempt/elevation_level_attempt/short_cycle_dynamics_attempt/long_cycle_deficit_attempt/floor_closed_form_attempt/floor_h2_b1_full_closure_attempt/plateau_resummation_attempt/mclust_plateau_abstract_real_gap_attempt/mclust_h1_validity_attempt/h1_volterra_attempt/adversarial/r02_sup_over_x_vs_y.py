"""
ADVERSARIAL CHECK 2 -- directly test whether sup_{x>=0} |(M_y K_A^raw(y,t) f)(x)|
(operator norm restricted to the physically relevant x>=0 half-line, exactly
the domain ATTEMPT.md Sec 4.4 claims shows unbounded/linear-in-y growth)
actually GROWS with y, or stays bounded / decreases, as y -> infinity, at
FIXED eps and t=0 (worst case: full v-integration range).

From Check 1: (M_y K_A^raw(y,t)[1])(x) = h_eps(x+y) * (1 - e^{-(y-t)/eps}),
h_eps(z) := |1-eps*z| * R(z).  For x in [0,infty), z=x+y ranges over
[y, infinity) -- z=0 is NOT reachable once y>0.  This script computes
sup_{x>=0} of this quantity directly (fine grid + refine), for growing y,
independently of the closed-form reasoning in the accompanying prose.
"""
import mpmath as mp
mp.mp.dps = 50

def R(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.e**(z*z/2)

def h(z, eps):
    z = mp.mpf(z); eps = mp.mpf(eps)
    return abs(1 - eps*z) * R(z)

def sup_over_x(y, eps, t=0, xmax_mult=50, n=4000):
    y = mp.mpf(y); eps = mp.mpf(eps); t = mp.mpf(t)
    factor = (1 - mp.e**(-(y-t)/eps))
    # scan x from 0 up to xmax_mult/eps (should comfortably cover any local max)
    xmax = xmax_mult
    best = mp.mpf(0); bestx = mp.mpf(0)
    for i in range(n+1):
        x = mp.mpf(i)/n * xmax
        v = h(x+y, eps) * factor
        if v > best:
            best = v; bestx = x
    return best, bestx

eps = mp.mpf('0.1')   # c=100
print(f"=== eps={eps} (c=100), t=0, scanning x in [0,50] for each y ===")
for y in [mp.mpf(v) for v in [0.001, 0.5, 1, 2, 5, 10, 20, 50, 100, 300, 1000]]:
    s, xstar = sup_over_x(y, eps, t=0, xmax_mult=80, n=3000)
    print(f"  y={float(y):>9.3f}   sup_x |M_y K_A^raw(y,0)[1](x)| = {float(s):.8f}   (attained near x={float(xstar):.4f})")

print()
eps = mp.mpf('0.0316227766')  # c=1000
print(f"=== eps={eps} (c=1000), t=0 ===")
for y in [mp.mpf(v) for v in [0.001, 0.5, 1, 2, 5, 10, 20, 50, 100, 300, 1000]]:
    s, xstar = sup_over_x(y, eps, t=0, xmax_mult=200, n=3000)
    print(f"  y={float(y):>9.3f}   sup = {float(s):.8f}   (near x={float(xstar):.4f})")

print()
print("Reference: sqrt(pi/2) =", float(mp.sqrt(mp.pi/2)))
