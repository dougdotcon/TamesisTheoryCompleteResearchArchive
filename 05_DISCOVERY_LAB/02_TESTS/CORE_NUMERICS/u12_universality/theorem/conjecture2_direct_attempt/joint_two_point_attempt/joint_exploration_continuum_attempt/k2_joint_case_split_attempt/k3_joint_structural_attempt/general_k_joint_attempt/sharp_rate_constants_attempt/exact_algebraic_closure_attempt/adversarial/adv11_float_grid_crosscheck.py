"""
Independent, fresh float-grid cross-check (item 7): a completely separate
non-sympy code path evaluating D3/D4 with raw Python floats, across a
range of n (up to 10^5) and a fine x-grid, confirming |h(n,x)| <= M_K
throughout, for K=3 (n>=5) and K=4 (n>=6).
"""
import numpy as np

M3 = 0.712071558138027808419103234207
M4 = 0.708718393409321614178660709132

def h3(n, x):
    k = n*x
    # D3 numerator/denominator (raw, from THEOREM.md Estagio 40)
    num = k*(k+1)*(k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2 + (3*n**2 - 11*n - 2)*k
                    + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
    den = n**4*(n-1)*(n-2)
    F3n = num/den
    F3c = 1 - (1-x**2)**3
    return n*(F3n - F3c)

def h4(n, x):
    k = n*x
    Q = (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4 + (-16*n**2 + 80*n + 51)*k**3
         + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
         + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
         + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)
    num = k*(k+1)*Q
    den = n**5*(n-1)*(n-2)*(n-3)
    F4n = num/den
    F4c = 1 - (1-x**2)**4
    return n*(F4n - F4c)

xgrid = np.linspace(0, 1, 4001)

print("="*70)
print("K=3 float-grid cross-check, n=5..2000 (integer) + geometric to 1e5")
print("="*70)
worst_ratio3 = 0
worst_at3 = None
violations3 = 0
n_values_3 = list(range(5, 2001)) + [2500, 5000, 7500, 10000, 25000, 50000, 100000]
for n in n_values_3:
    vals = h3(float(n), xgrid)
    mx = np.max(np.abs(vals))
    ratio = mx / M3
    if mx > M3 * (1 + 1e-9):
        violations3 += 1
        print(f"  VIOLATION n={n}: max|h3|={mx} > M3={M3}")
    if ratio > worst_ratio3:
        worst_ratio3 = ratio
        worst_at3 = n
print(f"n values tested: {len(n_values_3)}, violations: {violations3}")
print(f"worst ratio max|h3|/M3 = {worst_ratio3} at n={worst_at3}")

print()
print("="*70)
print("K=4 float-grid cross-check, n=6..2000 (integer) + geometric to 1e5")
print("="*70)
worst_ratio4 = 0
worst_at4 = None
violations4 = 0
n_values_4 = list(range(6, 2001)) + [2500, 5000, 7500, 10000, 25000, 50000, 100000]
for n in n_values_4:
    vals = h4(float(n), xgrid)
    mx = np.max(np.abs(vals))
    ratio = mx / M4
    if mx > M4 * (1 + 1e-9):
        violations4 += 1
        print(f"  VIOLATION n={n}: max|h4|={mx} > M4={M4}")
    if ratio > worst_ratio4:
        worst_ratio4 = ratio
        worst_at4 = n
print(f"n values tested: {len(n_values_4)}, violations: {violations4}")
print(f"worst ratio max|h4|/M4 = {worst_ratio4} at n={worst_at4}")

print("\nNote: for very large n (>~1e4-1e5), float64 catastrophic cancellation")
print("(computing a ~1/n-scale quantity as a difference of ~n^6-n^8-scale terms)")
print("starts eroding precision -- consistent with predecessor/target's own")
print("disclosed finding about needing exact rational arithmetic for n up to 1e6+.")
print("This script deliberately stays in a range (<=1e5) where float64's ~15-16")
print("significant digits are still enough to be a meaningful (not misleading)")
print("cross-check; it is a sanity net, not a load-bearing proof step, matching")
print("both fronts' own stated role for this kind of check.")
