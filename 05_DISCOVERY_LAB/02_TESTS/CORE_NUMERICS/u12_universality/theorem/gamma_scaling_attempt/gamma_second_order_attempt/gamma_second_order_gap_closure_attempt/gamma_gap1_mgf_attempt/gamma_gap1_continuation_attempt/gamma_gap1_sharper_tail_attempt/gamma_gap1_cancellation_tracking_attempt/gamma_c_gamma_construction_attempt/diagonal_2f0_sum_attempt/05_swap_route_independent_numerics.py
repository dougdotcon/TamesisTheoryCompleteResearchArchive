"""
Script 05 -- independent numerical confirmation via the swap-order route.

Computes S_n' = sum_{m=0}^{n} term_m, term_m = (gamma^m/n^m) m! T(n,m),
T(n,m) = sum_{j=0}^{n-m} C(j+m,m) C(n-j,m) (1-gamma)^j, using mpmath
(high precision, avoids overflow/underflow) -- a computational route
that is STRUCTURALLY DIFFERENT from every ancestor's direct k-sum
(sum_k A_k) evaluator. If this independently reproduces the already-
established T(gamma)=sqrt(2/(2-gamma)) leading order (and is
consistent with the conjectured C(gamma) at second order), that is a
genuine new numerical cross-check via different machinery -- NOT a
proof, but independent evidence the double-sum reformation (script 03)
is correct and behaves as expected at practically reachable n.

No claim of a fresh closed form is made or tested here; this is purely
a numerics script (mpmath), matching the archive's discipline.
"""
import mpmath as mp
mp.mp.dps = 40

def T_nm(n, m, gamma):
    x = 1 - gamma
    total = mp.mpf(0)
    for j in range(0, n - m + 1):
        total += mp.binomial(j + m, m) * mp.binomial(n - j, m) * x**j
    return total

def S_n_prime_swap(n, gamma, m_cutoff=None):
    """S_n' = S_n + 1, via the m-first swapped double sum."""
    if m_cutoff is None:
        m_cutoff = n
    total = mp.mpf(0)
    for m in range(0, min(n, m_cutoff) + 1):
        Tnm = T_nm(n, m, gamma)
        term = (mp.mpf(gamma)**m / mp.mpf(n)**m) * mp.factorial(m) * Tnm
        total += term
        if m > 20 and term < mp.mpf(10)**(-30) * total:
            break  # term has become utterly negligible; safe early stop
    return total

def phi_inf(c):
    # phi_inf(c) = (sqrt(pi)/2) c^{-1/2} erf(sqrt(c))  (THEOREM.md Theorem 1, cited)
    return (mp.sqrt(mp.pi) / 2) * c**mp.mpf(-0.5) * mp.erf(mp.sqrt(c))

def target_ratio(gamma):
    return mp.sqrt(mp.mpf(2) / (2 - gamma))

def C_closed_form(gamma):
    return -(mp.mpf(2) / (3 * mp.sqrt(mp.pi))) * mp.sqrt(gamma) * (6 - 8 * gamma + 3 * gamma**2) / (2 - gamma)**2

print("=== Swap-route computation of S_n (independent of the direct k-sum) ===")
print("gamma=0.5, several n; comparing R(n) := phi(n,gamma n)/phi_inf(gamma n) to "
      "target T(gamma)=sqrt(2/(2-gamma)), and sqrt(n)*(R-target) to C(gamma).")
print()

gamma = mp.mpf('0.5')
target = target_ratio(gamma)
Cval = C_closed_form(gamma)
print(f"target T(gamma) = {target}")
print(f"C(gamma) closed form = {Cval}")
print()

ns = [200, 400, 800, 1600, 3200]
results = []
print(f"{'n':>6} {'S_n':>18} {'phi(n,gn)':>16} {'R(n)':>14} {'R-target':>12} {'sqrt(n)*(R-t)':>14}")
for n in ns:
    Sn_prime = S_n_prime_swap(n, gamma)
    Sn = Sn_prime - 1  # S_n = sum_{k=1}^n A_k
    phi_ngn = Sn / n
    c = gamma * n
    pinf = phi_inf(c)
    R = phi_ngn / pinf
    diff = R - target
    scaled = mp.sqrt(n) * diff
    results.append((n, float(Sn), float(phi_ngn), float(R), float(diff), float(scaled)))
    print(f"{n:6d} {float(Sn):18.6f} {float(phi_ngn):16.10f} {float(R):14.10f} "
          f"{float(diff):12.4e} {float(scaled):14.6f}")

print()
print("Richardson extrapolation (model x_n = C + b/sqrt(n)), using last two n:")
n1, n2 = ns[-2], ns[-1]
x1 = results[-2][5]
x2 = results[-1][5]
# x_n = C + b/sqrt(n)  =>  solve 2x2 linear system
import math
A = [[1, 1/math.sqrt(n1)], [1, 1/math.sqrt(n2)]]
bvec = [x1, x2]
det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
C_extrap = (bvec[0]*A[1][1] - A[0][1]*bvec[1]) / det
print(f"  C_extrap (swap-route, n={n1},{n2}) = {C_extrap:.6f}")
print(f"  C(gamma) closed form              = {float(Cval):.6f}")
print(f"  |diff| = {abs(C_extrap - float(Cval)):.6f}")

print()
print("=== Cross-check vs a fresh, independent DIRECT k-sum evaluator (same script, "
      "different loop -- sanity that S_n itself is computed correctly) ===")
def S_n_direct_k(n, gamma):
    total = mp.mpf(0)
    beta = gamma * (2 - gamma) / 2
    for k in range(1, n + 1):
        # A_k via exact Binomial-mixture sum over M (small-ish n only, this is
        # for cross-validation at moderate n, O(n^2) cost)
        Ak = mp.mpf(0)
        for Mval in range(0, k + 1):
            pmf = mp.binomial(k, Mval) * gamma**Mval * (1 - gamma)**(k - Mval)
            prod = mp.mpf(1)
            for i in range(1, Mval + 1):
                prod *= (1 - mp.mpf(k - i) / n)
            Ak += pmf * prod
        total += Ak
    return total

for n in [50, 100]:
    Sn_direct = S_n_direct_k(n, gamma)
    Sn_swap = S_n_prime_swap(n, gamma) - 1
    print(f"  n={n}: S_n(direct k-sum)={float(Sn_direct):.10f}  "
          f"S_n(swap m-sum)={float(Sn_swap):.10f}  "
          f"diff={float(abs(Sn_direct-Sn_swap)):.3e}")
