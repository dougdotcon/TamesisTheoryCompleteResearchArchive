"""
Adversarial referee script 03.

(A) Independently verify that the target's claimed closed form

    Ghat(n,gamma) := (10/3+(1-gamma)/2) K_max^3/n^2 + (7/4-gamma) K_max^2/n
                     + (11/6) K_max^2/n^2 + (3/4) K_max/n

is exactly the algebraic consequence of substituting k=K_max into

    g(k) <= |c0|_bound(k) + |c1|_bound(k)*k + |c2|_bound(k)*k^2 + c3*k^3

using the Step-3 coefficient bounds independently re-verified in script 02.
Pure symbolic algebra -- no numerics.

(B) Independently verify the elementary claim
        K <= K_max(n,gamma) := 4*sqrt(n*ln(n)/beta)   for all n>=3
    where K := ceil( sqrt((4/beta)*n*ln(n)) ) is the wave-17 front's own
    truncation (confirmed by direct reading of gamma_scaling_attempt/
    ATTEMPT.md Sec.5), by an independent elementary argument:
    for y>=1, ceil(y) <= y+1 <= 2y (since y>=1 => 1<=y).
    Then apply to y := sqrt((4/beta)*n*ln n) = 2*sqrt(n*ln(n)/beta), and
    check y>=1 holds for every n>=3, gamma in (0,1) -- so ceil(y) <= 2y,
    i.e. K <= 4*sqrt(n*ln(n)/beta) = K_max.  Checked both symbolically
    (worst case beta=1/2, n=3) and via a numeric grid.

(C) Independently verify the claimed leading asymptotic
        Ghat(n,gamma) ~ lambdahat(gamma)*ln(n),  lambdahat(gamma):=16*(7/4-gamma)/beta
    by symbolic limit of Ghat(n,gamma)/ln(n) as n->infinity (gamma fixed).
"""
import sympy as sp

n, K = sp.symbols('n K', positive=True)
gamma = sp.symbols('gamma', positive=True)
beta = gamma * (2 - gamma) / 2

c0_bound_k = sp.Rational(7, 6) * K ** 3 / n ** 2 + sp.Rational(5, 6) * K ** 2 / n ** 2
c1_bound_k = 2 * K ** 2 / n ** 2 + (1 - gamma) * K / n + K / n ** 2 + sp.Rational(3, 4) / n
c2_bound_k = (1 - gamma) * K / (2 * n ** 2) + sp.Rational(3, 4) / n
c3_exact = sp.Rational(1, 6) / n ** 2

# g(K) <= c0_bound(K) + c1_bound(K)*K + c2_bound(K)*K^2 + c3*K^3
g_at_K = sp.expand(c0_bound_k + c1_bound_k * K + c2_bound_k * K ** 2 + c3_exact * K ** 3)
print("Our own assembled g(K) upper bound, expanded:")
print(" ", g_at_K)

Ghat_claimed = sp.expand(
    (sp.Rational(10, 3) + (1 - gamma) / 2) * K ** 3 / n ** 2
    + (sp.Rational(7, 4) - gamma) * K ** 2 / n
    + sp.Rational(11, 6) * K ** 2 / n ** 2
    + sp.Rational(3, 4) * K / n
)
print("\nTarget's claimed Ghat(n,gamma) [with K_max -> K symbol], expanded:")
print(" ", Ghat_claimed)

diff = sp.simplify(g_at_K - Ghat_claimed)
print("\nDifference (should be exactly 0):", diff)
assert diff == 0, "Ghat formula does NOT match the algebraic consequence of the Step-3 bounds!"
print("=== (A) Ghat(n,gamma) formula independently CONFIRMED as the exact ===")
print("=== algebraic consequence of substituting k=K_max into the Step-3 bounds. ===\n")

# --- (B) K <= K_max check ---
print("--- (B) K <= K_max(n,gamma) := 4*sqrt(n*ln(n)/beta), all n>=3 ---")
import mpmath as mp
mp.mp.dps = 50

def K_exact(nv, gv):
    b = gv * (2 - gv) / 2
    return mp.ceil(mp.sqrt((4 / b) * nv * mp.log(nv)))

def K_max_f(nv, gv):
    b = gv * (2 - gv) / 2
    return 4 * mp.sqrt(nv * mp.log(nv) / b)

viol = []
n_test = [3, 4, 5, 10, 100, 1000, 10 ** 6, 10 ** 12, 10 ** 30, 10 ** 80]
gamma_test = [mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5'),
              mp.mpf('0.9'), mp.mpf('0.99'), mp.mpf('0.999')]
checked = 0
for nv in n_test:
    for gv in gamma_test:
        checked += 1
        Kv = K_exact(nv, gv)
        Kmv = K_max_f(nv, gv)
        if not (Kv <= Kmv):
            viol.append((nv, gv, Kv, Kmv))
print(f"Checked {checked} (n,gamma) points; violations: {len(viol)}")
for v in viol:
    print("  VIOLATION:", v)
assert len(viol) == 0
print("=== (B) K <= K_max CONFIRMED over the tested grid (n up to 1e80). ===\n")

# elementary symbolic argument confirming it in general:
# y := 2*sqrt(n*ln(n)/beta); claim y>=1 for all n>=3, gamma in (0,1)
# worst case (smallest y) is beta largest (beta<=1/2) and n smallest (n=3)
y_worst = 2 * sp.sqrt(3 * sp.log(3) / sp.Rational(1, 2))
print("Worst-case y at n=3, beta=1/2 (gamma=1):", float(y_worst))
assert float(y_worst) >= 1, "y>=1 worst-case check failed!"
print("y>=1 holds at the worst case (n=3,beta=1/2) hence for all n>=3, all gamma in (0,1]")
print("=> ceil(y) <= y+1 <= 2y (elementary, since y>=1) => K <= 4*sqrt(n ln n/beta) = K_max.\n")

# --- (C) leading asymptotic of Ghat ---
print("--- (C) leading asymptotic Ghat(n,gamma) ~ lambdahat(gamma)*ln(n) ---")
Kmax_sym = 4 * sp.sqrt(n * sp.log(n) / beta)
Ghat_n = sp.expand(
    (sp.Rational(10, 3) + (1 - gamma) / 2) * Kmax_sym ** 3 / n ** 2
    + (sp.Rational(7, 4) - gamma) * Kmax_sym ** 2 / n
    + sp.Rational(11, 6) * Kmax_sym ** 2 / n ** 2
    + sp.Rational(3, 4) * Kmax_sym / n
)
ratio = Ghat_n / sp.log(n)
lim_ratio = sp.limit(ratio, n, sp.oo)
lim_ratio = sp.simplify(lim_ratio)
print("lim_{n->infty} Ghat(n,gamma)/ln(n) =", lim_ratio)

lambdahat_claimed = sp.simplify(16 * (sp.Rational(7, 4) - gamma) / beta)
print("Claimed lambdahat(gamma) = 16*(7/4-gamma)/beta =", lambdahat_claimed)
diff2 = sp.simplify(lim_ratio - lambdahat_claimed)
print("Difference (should be 0):", diff2)
assert diff2 == 0, "lambdahat leading-asymptotic claim MISMATCH!"
print("=== (C) lambdahat(gamma) = 16*(7/4-gamma)/beta CONFIRMED as exact leading asymptotic of Ghat. ===")

# spot values of lambdahat at the front's sample gammas, cross-check against
# C0(gamma):=sqrt(1/4+lambdahat/2), C(gamma):=1.2*C0(gamma)
print("\nSpot values (gamma, lambdahat, C0, C=1.2*C0):")
for gv in [sp.Rational(99, 100), sp.Rational(9, 10), sp.Rational(7, 10),
           sp.Rational(1, 2), sp.Rational(3, 10), sp.Rational(1, 10),
           sp.Rational(1, 20), sp.Rational(1, 100)]:
    lh = float(lambdahat_claimed.subs(gamma, gv))
    C0 = (0.25 + lh / 2) ** 0.5
    C = 1.2 * C0
    print(f"  gamma={float(gv):.2f}: lambdahat={lh:.4f}  C0={C0:.4f}  C={C:.4f}")
