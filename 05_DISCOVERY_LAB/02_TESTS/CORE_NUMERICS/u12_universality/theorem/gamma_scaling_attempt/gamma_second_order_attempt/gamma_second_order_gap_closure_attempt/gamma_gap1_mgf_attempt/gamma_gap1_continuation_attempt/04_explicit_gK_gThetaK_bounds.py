"""
04_explicit_gK_gThetaK_bounds.py  (revised: tighter, cancellation-preserving
coefficient bounds from script 03)

Assembles script 03's explicit coefficient bounds into fully explicit,
for-all-n-above-an-explicit-threshold bounds on g(K) and g(Theta_K), the two
scalar quantities the Bulk/Tail Lemma (gamma_gap1_mgf_attempt/ATTEMPT.md
Section 3.2) reduces Gap 1 to. This is the mandate item 1 conversion: leading-
order asymptotics -> explicit inequality with an explicit n_0(gamma).

Reserved seed block 20260900000-20260900999: unused (deterministic).
"""
import mpmath as mp

mp.mp.dps = 50


def beta_of(gamma):
    return gamma * (2 - gamma) / 2


def K_exact(n, gamma):
    n = mp.mpf(n); gamma = mp.mpf(gamma)
    beta = beta_of(gamma)
    return mp.ceil(mp.sqrt(4 * n * mp.log(n) / beta))


def exact_c(k, n, gamma):
    k = mp.mpf(k); n = mp.mpf(n); gamma = mp.mpf(gamma)
    c0 = (gamma * k / (12 * n ** 2)) * (
        2 * gamma ** 2 * k ** 2 - 6 * gamma * k ** 2 + 3 * gamma * k
        + 6 * k ** 2 - 6 * k + 1
    )
    c1 = (1 / n ** 2) * (
        (gamma ** 2 * k ** 2) / 2 - gamma * k ** 2 - gamma * k * n
        + (gamma * k) / 2 + (k ** 2) / 2 + k * n - k / 2 - n / 2 + mp.mpf(1) / 12
    )
    c2 = (2 * gamma * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
    c3 = mp.mpf(1) / (6 * n ** 2)
    return c0, c1, c2, c3


def g_exact_at_K(n, gamma, t):
    K = K_exact(n, gamma)
    c0, c1, c2, c3 = exact_c(K, n, gamma)
    t = mp.mpf(t)
    return abs(c0) + abs(c1) * t + abs(c2) * t ** 2 + abs(c3) * t ** 3


print("=" * 78)
print("STEP 1: K <= 4*sqrt(n ln n / beta)  (K^2 <= 16 n ln n / beta)")
print("=" * 78)
viol1 = 0
for n in [3, 4, 10, 100, 1000, 10000, 100000, 10 ** 6]:
    for gs in ['0.01', '0.05', '0.1', '0.3', '0.5', '0.7', '0.9', '0.99']:
        gamma = mp.mpf(gs)
        beta = beta_of(gamma)
        K = K_exact(n, gamma)
        Kmax_clean = 4 * mp.sqrt(mp.mpf(n) * mp.log(n) / beta)
        if K > Kmax_clean:
            viol1 += 1
print(f"Violations of K <= 4 sqrt(n ln n/beta): {viol1} (expect 0)")
assert viol1 == 0
print("(derivation as in the previous revision: K^2 <= 4X, X=4 n ln n/beta, "
      "for n>=3, since X>=1.)")

print("\n" + "=" * 78)
print("STEP 2: K <= n/2 for n >= n_1(gamma) := ceil(16384/beta^2)")
print("=" * 78)


def n1_of(gamma):
    beta = beta_of(gamma)
    return int(mp.ceil(16384 / beta ** 2))


viol2 = 0
for gs in ['0.01', '0.05', '0.1', '0.3', '0.5', '0.7', '0.9', '0.99']:
    gamma = mp.mpf(gs)
    n1 = n1_of(gamma)
    print(f"  gamma={gs:<6}  beta={float(beta_of(gamma)):.6f}  n_1(gamma)={n1}")
    for n in sorted({n1, n1 + 1, n1 * 2, n1 * 10}):
        if n < 3:
            continue
        K = K_exact(n, gamma)
        if K > mp.mpf(n) / 2:
            viol2 += 1
print(f"\nViolations of K<=n/2 for n>=n_1(gamma): {viol2} (expect 0)")
assert viol2 == 0

print("\n" + "=" * 78)
print("STEP 3: tightened explicit bound g(K) <= Ghat(n,gamma), n>=n_1(gamma)")
print("=" * 78)
print("""
Using script 03's cancellation-preserving bounds
  |c0|<=(7/6)k^3/n^2+(5/6)k^2/n^2
  |c1|<=2k^2/n^2+(1-gamma)k/n+k/n^2+3/(4n)
  |c2|<=(1-gamma)k/(2n^2)+3/(4n)
  c3=1/(6n^2)
evaluated at k=K, substituting K<=K_max=4 sqrt(n ln n/beta) (Step 1; valid
since all these bounds are nondecreasing in k, and g's own coefficients are
manifestly >=0 so g(t) itself is nondecreasing -- already used by the
Bulk/Tail Lemma):

  g(K) <= |c0|+|c1|K+|c2|K^2+|c3|K^3
        <= [7/6+2+ (1-gamma)/2 +1/6] K_max^3/n^2
           + [(1-gamma)+3/4] K_max^2/n
           + [5/6+1] K_max^2/n^2
           + [3/4] K_max/n
        =  (10/3 + (1-gamma)/2) K_max^3/n^2 + (7/4-gamma) K_max^2/n
           + (11/6) K_max^2/n^2 + (3/4) K_max/n
        =: Ghat(n,gamma)     [fully explicit closed form]

As n->infinity, Ghat(n,gamma) ~ (7/4-gamma)*16*ln(n)/beta =: lambda_hat(gamma)*ln(n)
(the other three terms -> 0 absolutely), with lambda_hat(gamma) := 16(7/4-gamma)/beta
-- compare to the TRUE leading constant lambda(gamma)=kappa_0(gamma)(3/2-gamma)
=(4/beta)(3/2-gamma) (script 02): lambda_hat/lambda = 4(7/4-gamma)/(3/2-gamma),
a modest looseness factor between 14/3~4.67 (gamma->0) and 3 (gamma=1) --
much tighter than the first-pass bound's ~7-11x looseness.
""")


def Ghat(n, gamma):
    n = mp.mpf(n); gamma = mp.mpf(gamma)
    beta = beta_of(gamma)
    Kmax = 4 * mp.sqrt(n * mp.log(n) / beta)
    coefK3 = mp.mpf(10) / 3 + (1 - gamma) / 2
    coefK2_n = mp.mpf(7) / 4 - gamma
    coefK2_n2 = mp.mpf(11) / 6
    coefK_n = mp.mpf(3) / 4
    return (coefK3 * Kmax ** 3 / n ** 2 + coefK2_n * Kmax ** 2 / n
            + coefK2_n2 * Kmax ** 2 / n ** 2 + coefK_n * Kmax / n)


def lambda_hat(gamma):
    gamma = mp.mpf(gamma)
    beta = beta_of(gamma)
    return 16 * (mp.mpf(7) / 4 - gamma) / beta


viol3 = 0
checks3 = 0
print(f"{'gamma':>7} {'n':>12} {'g(K) true':>16} {'Ghat bound':>16} {'ratio true/bound':>18}")
for gs in ['0.99', '0.9', '0.7', '0.5', '0.3', '0.1', '0.05', '0.01']:
    gamma = mp.mpf(gs)
    n1 = n1_of(gamma)
    for n in sorted({n1, n1 * 2, n1 * 10, n1 * 100}):
        checks3 += 1
        gK = g_exact_at_K(n, gamma, K_exact(n, gamma))
        gh = Ghat(n, gamma)
        ok = gK <= gh
        ratio = gK / gh if gh > 0 else mp.mpf('nan')
        print(f"{gs:>7} {n:>12} {float(gK):>16.6f} {float(gh):>16.6f} {float(ratio):>18.6f}")
        if not ok:
            viol3 += 1
            print("    VIOLATION")
print(f"\nTotal checks: {checks3}, violations: {viol3} (expect 0)")
assert viol3 == 0

print(f"\nlambda_hat(gamma) (this front's explicit, looser-but-honest leading")
print(f"constant) vs. lambda(gamma) (true leading constant, script 02):")
for gs in ['0.99', '0.5', '0.1', '0.01']:
    gamma = mp.mpf(gs)
    beta = beta_of(gamma)
    lam_true = (4 / beta) * (mp.mpf('1.5') - gamma)
    print(f"  gamma={gs:<6} lambda_hat={float(lambda_hat(gamma)):>10.4f}  "
          f"lambda_true={float(lam_true):>10.4f}  ratio={float(lambda_hat(gamma)/lam_true):>6.3f}")

print("\n" + "=" * 78)
print("STEP 4: explicit bound on g(Theta_K), Theta_K = C sqrt(K ln n)")
print("=" * 78)


def GhatTheta(n, gamma, C):
    n = mp.mpf(n); gamma = mp.mpf(gamma); C = mp.mpf(C)
    beta = beta_of(gamma)
    Kmax = 4 * mp.sqrt(n * mp.log(n) / beta)
    Thetamax = C * mp.sqrt(Kmax * mp.log(n))
    c0_piece = mp.mpf(7) / 6 * Kmax ** 3 / n ** 2 + mp.mpf(5) / 6 * Kmax ** 2 / n ** 2
    c1_pref = 2 * Kmax ** 2 / n ** 2 + (1 - gamma) * Kmax / n + Kmax / n ** 2 + mp.mpf(3) / (4 * n)
    c2_pref = (1 - gamma) * Kmax / (2 * n ** 2) + mp.mpf(3) / (4 * n)
    c3_piece = Thetamax ** 3 / (6 * n ** 2)
    return c0_piece + c1_pref * Thetamax + c2_pref * Thetamax ** 2 + c3_piece


viol4 = 0
checks4 = 0
print(f"{'gamma':>7} {'C':>4} {'n':>10} {'g(ThetaK) true':>16} {'bound':>16} {'ok':>4}")
for gs in ['0.99', '0.5', '0.1', '0.01']:
    gamma = mp.mpf(gs)
    n1 = n1_of(gamma)
    for C in [2, 3, 5]:
        for n in sorted({n1, n1 * 5, n1 * 50}):
            checks4 += 1
            K = K_exact(n, gamma)
            ThetaK = C * mp.sqrt(K * mp.log(n))
            gTh_true = g_exact_at_K(n, gamma, ThetaK)
            gTh_bound = GhatTheta(n, gamma, C)
            ok = gTh_true <= gTh_bound
            print(f"{gs:>7} {C:>4} {n:>10} {float(gTh_true):>16.6f} "
                  f"{float(gTh_bound):>16.6f} {str(ok):>4}")
            if not ok:
                viol4 += 1
print(f"\nTotal checks: {checks4}, violations: {viol4} (expect 0)")
assert viol4 == 0

print("\nDone.")
