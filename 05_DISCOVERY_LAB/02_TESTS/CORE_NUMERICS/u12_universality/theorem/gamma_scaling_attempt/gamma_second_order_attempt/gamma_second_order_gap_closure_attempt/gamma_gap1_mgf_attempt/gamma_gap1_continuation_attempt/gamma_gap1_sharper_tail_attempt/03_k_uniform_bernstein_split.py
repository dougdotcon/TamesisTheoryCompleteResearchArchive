"""
GAMMA-GAP1-SHARPER-TAIL-ATTEMPT, script 03.

The grandparent's Bulk/Tail Lemma needs a tail-probability bound
P(|D|>Theta_k) that is valid UNIFORMLY for every 1<=k<=K (Theta_k :=
C*sqrt(k*ln n)) with a bound that does not depend on k -- Hoeffding gives
this "for free" via an exact algebraic cancellation (2*Theta_k^2/k = 2*C^2*ln n,
EXACTLY independent of k). Bernstein's bound (script 01) does NOT have this
exact cancellation: its denominator 2*k*sigma^2 + (2/3)*M*Theta_k has a
sub-leading sqrt(k) correction that does not cancel against the k*ln(n)
numerator. This script builds and verifies the fix used by this front: a
"slack parameter" a>0 construction that recovers a clean, k-independent
bound for the LARGE-k range, plus an explicit deterministic (no probability
needed) bound for the residual SMALL-k range.

Construction.
  sigma^2(gamma):=gamma(1-gamma), M(gamma):=max(gamma,1-gamma).
  For any a>0: IF (2/3)*M*Theta_k <= a*k*sigma^2  THEN the Bernstein
  denominator 2*k*sigma^2+(2/3)*M*Theta_k <= (2+a)*k*sigma^2, hence
    P(|D|>Theta_k) <= 2*exp(-Theta_k^2/((2+a)*k*sigma^2))
                     = 2*exp(-C^2*ln(n)/((2+a)*sigma^2))     [k CANCELS exactly]
                     = 2 * n^{-C^2/((2+a)*sigma^2)},
  a clean, k-independent bound -- valid whenever the sufficient condition
  holds. Solving the sufficient condition for k (since Theta_k=C*sqrt(k ln n)):
    (2/3)*M*C*sqrt(k ln n) <= a*k*sigma^2
    <=>  sqrt(k) >= (2*M*C*sqrt(ln n))/(3*a*sigma^2)
    <=>  k >= k_2(n,gamma,C,a) := (2*M*C/(3*a*sigma^2))^2 * ln(n).

So for k in [k_2(n,gamma,C,a), K]: use the clean Bernstein bound above.
For k in [1, k_2(n,gamma,C,a)]: no probability is needed at all -- since
|D|<=k a.s., use the DETERMINISTIC bound R_k <= (1/6)*g(k)^3*e^{g(k)}
directly (g monotone non-decreasing, so g(k)<=g(k_2) there), then a crude
union bound over at most k_2 terms, weighted by e^{-s(k)}<=e^{1/2}
(elementary: s(k)=beta*k^2/n-gamma*k/(2n) has minimum -gamma^2/(16*beta*n)
over all k>=0, which is a tiny O(1/n) negative number for any n of interest,
certainly >=-1/2).

Since k_2(n,gamma,C,a) = O(ln n) (poly-LOGARITHMIC in n) while the true
truncation K = Theta(sqrt(n ln n)) (POLYNOMIAL in sqrt(n)), for any FIXED
a>0 the small-k region becomes vanishingly small relative to [1,K] as
n grows -- this script verifies numerically that k_2 << K_max at the scale
this front's own n_0(gamma) construction (script 05) actually needs, and
that the sufficient condition and clean bound are both valid, with zero
violations against the exact Binomial tail.
"""
import mpmath as mp

mp.mp.dps = 50


def exact_tail_prob(k, gam, t):
    gam = mp.mpf(gam)
    k = int(k)
    total = mp.mpf(0)
    for j in range(0, k + 1):
        D = j - gam * k
        if abs(D) > t:
            pmf = mp.binomial(k, j) * gam ** j * (1 - gam) ** (k - j)
            total += pmf
    return total


def k2_threshold(n, gam, C, a):
    gam = mp.mpf(gam)
    sigma2 = gam * (1 - gam)
    M = max(gam, 1 - gam)
    return (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)


def clean_bound(n, gam, C, a):
    gam = mp.mpf(gam)
    sigma2 = gam * (1 - gam)
    exponent = C ** 2 / ((2 + a) * sigma2)
    return 2 * mp.mpf(n) ** (-exponent)


print("=" * 78)
print("PART A: sufficient condition (2/3)*M*Theta_k <= a*k*sigma^2 holds for")
print("every k >= k_2(n,gamma,C,a) (checked right at and above the threshold)")
print("=" * 78)
fail = 0
for n_val in [1000, 10 ** 6, 10 ** 40]:
    for gam_f in [0.01, 0.1, 0.5, 0.9, 0.99]:
        for C_val in [3.0, 5.0, 9.0]:
            for a_val in [0.05, 0.5, 1.0, 2.0]:
                gam = mp.mpf(gam_f)
                sigma2 = gam * (1 - gam)
                M = max(gam, 1 - gam)
                k2 = k2_threshold(n_val, gam_f, C_val, a_val)
                for mult in [1.0, 1.5, 3.0]:
                    k_test = int(mp.ceil(k2 * mult)) + 1
                    Theta_k = C_val * mp.sqrt(mp.mpf(k_test) * mp.log(n_val))
                    lhs = mp.mpf(2) / 3 * M * Theta_k
                    rhs = a_val * k_test * sigma2
                    if lhs > rhs:
                        fail += 1
                        print("FAIL suff cond", n_val, gam_f, C_val, a_val, mult)
print("failures (must be 0):", fail)
assert fail == 0

print()
print("=" * 78)
print("PART B: clean k-uniform bound vs EXACT tail prob, k just above k_2,")
print("moderate n (exact pmf summation is only tractable at moderate n/k)")
print("=" * 78)
violations = 0
checked = 0
for n_val in [50, 200, 2000]:
    for gam_f in [0.02, 0.1, 0.3, 0.5, 0.8, 0.95]:
        for C_val in [2.0, 4.0]:
            a_val = 1.0
            k2 = k2_threshold(n_val, gam_f, C_val, a_val)
            k2i = max(1, int(mp.ceil(k2)))
            for mult in [1.0, 1.5, 3.0, 8.0]:
                k_test = int(k2i * mult) + 1
                if k_test > 5000:
                    continue
                Theta_k = C_val * mp.sqrt(mp.mpf(k_test) * mp.log(n_val))
                if Theta_k > k_test:
                    continue  # Theta_k must stay within the true support [0,k]
                exact = exact_tail_prob(k_test, gam_f, Theta_k)
                bound = clean_bound(n_val, gam_f, C_val, a_val)
                checked += 1
                if exact > bound + mp.mpf('1e-45'):
                    violations += 1
                    print("VIOLATION", n_val, gam_f, C_val, k_test)
print(f"checked={checked} violations={violations}")
assert violations == 0

print()
print("=" * 78)
print("PART C: s(k) global minimum, justifying e^{-s(k)}<=e^{1/2} for the")
print("small-k crude union bound (elementary calculus, exact)")
print("=" * 78)
import sympy as sp
k_s, n_s, gam_s = sp.symbols('k n gamma', positive=True)
beta_s = gam_s * (2 - gam_s) / 2
s_expr = beta_s * k_s ** 2 / n_s - gam_s * k_s / (2 * n_s)
kstar = gam_s / (4 * beta_s)
s_at_kstar = sp.simplify(s_expr.subs(k_s, kstar))
target = -gam_s ** 2 / (16 * beta_s * n_s)
diff = sp.simplify(s_at_kstar - target)
print("min_k s(k) [calculus, k*=gamma/(4*beta)] =", s_at_kstar)
print("claimed closed form -gamma^2/(16*beta*n):", target)
print("difference (must be 0):", diff)
assert diff == 0
print("=> min_k s(k) = -gamma^2/(16*beta*n), an O(1/n) quantity, hence")
print("   e^{-s(k)} <= e^{gamma^2/(16*beta*n)} <= e^{1/2} for any n with")
print("   gamma^2/(16*beta*n) <= 1/2, true for all n>=1 in practice here.")

print()
print("=" * 78)
print("PART D: k_2(n,gamma,C,a=0.05) vs K_max(n,gamma), at the scale this")
print("front's n_0(gamma) construction (script 05) actually needs")
print("=" * 78)


def beta_of(gam):
    return gam * (2 - gam) / 2


def Kmax_of(n, gam):
    return 4 * mp.sqrt(n * mp.log(n) / beta_of(gam))


mp.mp.dps = 60
a_val = mp.mpf('0.05')
for gam_f, C_val, log10n in [('0.99', 0.85, 18), ('0.5', 6.3, 51), ('0.01', 9.0, 76)]:
    gam = mp.mpf(gam_f)
    n_val = mp.mpf(10) ** log10n
    k2 = k2_threshold(n_val, gam, mp.mpf(C_val), a_val)
    Km = Kmax_of(n_val, gam)
    print(f"gamma={gam_f}: n=10^{log10n}  k2={float(k2):.4g}  Kmax={float(Km):.4g}  "
          f"k2/Kmax={float(k2 / Km):.3e}")

print()
print("All Part A/B/C/D checks passed.")
