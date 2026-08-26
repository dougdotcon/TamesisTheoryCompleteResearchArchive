"""
Independent fresh evaluator of S_n = sum_{k=1}^n A_k(n,gamma), built from
scratch from the mathematical prose of wave-17 ATTEMPT.md Lemma 1 and this
front's ATTEMPT.md alone. No .py file of any prior front (this front's own
0X_*.py included) was opened or consulted.

Key implementation trick (own device, not copied from anywhere): instead of
recomputing the product P_{k,m} = prod_{i=1}^m (1-(k-i)/n) separately for
every k (which naively costs O(k) per k, O(K^2) total), note

    log P_{k,m} = sum_{i=1}^m log(1-(k-i)/n) = sum_{j=k-m}^{k-1} log(1-j/n)

depends on k,m only through the *endpoints* k-m and k of a fixed 1-D array
  h(j) := log(1 - j/n),  j = 0..n-1.
So with cumlog[t] := sum_{j=0}^{t-1} h(j)  (cumlog[0]=0), we get the O(1)
closed form
    log P_{k,m} = cumlog[k] - cumlog[k-m]     for 0<=m<=k<=n.
This is built once in O(n), after which every A_k is a vectorized
logsumexp over a Binomial(k,gamma) pmf window -- no O(n^2) blowup.

Produces:
  - D_n, E_n at n in {2^14, 2^16, 2^18} for gamma in {0.1,...,0.9,0.99},
    two-point Richardson extrapolation (model x_n = x + c/sqrt(n)),
    compared against the document's own printed table (Sec 6.3).
  - R_n = (S_n/n)/phi_infty(gamma n) at n=2^18 for the 7 gamma values the
    wave-17 front tabulated, compared against both fronts' printed tables
    (Sec 6.5 cross-check), done independently.
"""
import numpy as np
from scipy.stats import binom
from scipy.special import erf, logsumexp

def phi_infty(c):
    # THEOREM.md Theorem 1: phi_infty(c) = (sqrt(pi)/2) c^{-1/2} erf(sqrt(c))
    c = np.asarray(c, dtype=np.float64)
    return (np.sqrt(np.pi) / 2) * c ** -0.5 * erf(np.sqrt(c))


def build_cumlog(n):
    j = np.arange(0, n, dtype=np.float64)
    h = np.log1p(-j / n)  # log(1 - j/n), stable for j near 0
    cumlog = np.concatenate(([0.0], np.cumsum(h)))
    return cumlog  # cumlog[t] = sum_{j=0}^{t-1} log(1-j/n), t=0..n


def Sn_and_pieces(n, gamma, std_width=14.0, k_extra_sigma=8.0):
    """Returns S_n (=sum_k A_k), and K_used (truncation cutoff for k)."""
    beta = gamma * (2 - gamma) / 2
    cumlog = build_cumlog(n)

    # k-truncation: A_k ~ e^{-beta k^2/n}, negligible past K where beta K^2/n
    # is many "e-foldings" past the Gaussian bulk k=O(sqrt(n)). Use the same
    # style cutoff as both fronts: K = ceil(sqrt(4 n ln n / beta)) times a
    # safety factor, capped at n.
    K = int(np.ceil(np.sqrt(max(4.0 * n * np.log(max(n, 3)) / beta, 1.0))))
    K = min(K, n)

    total = 0.0
    for k in range(1, K + 1):
        mean = gamma * k
        sd = np.sqrt(max(k * gamma * (1 - gamma), 1e-300))
        lo = max(0, int(np.floor(mean - std_width * sd)) - 1)
        hi = min(k, int(np.ceil(mean + std_width * sd)) + 1)
        if hi < lo:
            continue
        m = np.arange(lo, hi + 1)
        # log P_{k,m} = cumlog[k] - cumlog[k-m]
        logP = cumlog[k] - cumlog[k - m]
        logpmf = binom.logpmf(m, k, gamma)
        logAk = logsumexp(logpmf + logP)
        total += np.exp(logAk)
    return total, K


def Gn(n, gamma):
    beta = gamma * (2 - gamma) / 2
    return 0.5 * np.sqrt(np.pi * n / beta)


def Sn0_direct(n, gamma):
    """Deterministic half S_n^(0) = sum_{k=1}^n e^{-beta k^2/n + gamma k/(2n)},
    computed independently here in float64 (cross-checked against script 02's
    mpmath version elsewhere) purely to isolate E_n = S_n - S_n^(0)."""
    beta = gamma * (2 - gamma) / 2
    k = np.arange(1, n + 1, dtype=np.float64)
    return np.sum(np.exp(-beta * k * k / n + gamma * k / (2 * n)))


def D_target(gamma):
    return -1.0 / 3.0 * (6 - 8 * gamma + 3 * gamma ** 2) / (2 - gamma) ** 2


def D0_target(gamma):
    return (gamma - 1) / (2 * (2 - gamma))


def E_target(gamma):
    return D_target(gamma) - D0_target(gamma)


def richardson(n1, x1, n2, x2):
    """Two-point Richardson extrapolation assuming x_n = x + c/sqrt(n)."""
    # x1 = x + c/sqrt(n1); x2 = x + c/sqrt(n2)
    s1 = 1 / np.sqrt(n1)
    s2 = 1 / np.sqrt(n2)
    x = (x1 * s2 - x2 * s1) / (s2 - s1)
    return x


print("=" * 100)
print("PART 1: D_n / E_n Richardson extrapolation, independent evaluator, vs document Sec 6.3 table")
print("=" * 100)
ns = [2 ** 14, 2 ** 16, 2 ** 18]
gammas = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]

doc_table = {
    # gamma: (D_target, D_n_extrap_doc, D_diff_doc, E_target, E_n_extrap_doc, E_diff_doc)
    0.1: (-0.48291782, -0.48291782, 4.1e-09, -0.24607572, -0.24607573, -1.9e-08),
    0.3: (-0.44636678, -0.44636674, 4.1e-08, -0.24048443, -0.24048445, -2.1e-08),
    0.5: (-0.40740741, -0.40740729, 1.2e-07, -0.24074074, -0.24074071, 3.1e-08),
    0.7: (-0.36883629, -0.36883608, 2.2e-07, -0.25345168, -0.25345155, 1.3e-07),
    0.9: (-0.33884298, -0.33884273, 2.5e-07, -0.29338843, -0.29338823, 2.0e-07),
    0.99: (-0.33339869, -0.33339846, 2.3e-07, -0.32844819, -0.32844797, 2.2e-07),
}

print(f"{'gamma':>6} {'K(2^18)':>8} {'D_n extrap (mine)':>19} {'D target':>12} {'diff (mine)':>13} "
      f"{'doc D_n extrap':>16} {'doc-mine diff':>15}")
results = {}
for g in gammas:
    Sn_vals = {}
    Sn0_vals = {}
    Kused = None
    for n in ns:
        Sv, K = Sn_and_pieces(n, g)
        Sn_vals[n] = Sv
        Sn0_vals[n] = Sn0_direct(n, g)
        Kused = K
    Dn_vals = {n: Sn_vals[n] - Gn(n, g) for n in ns}
    En_vals = {n: Sn_vals[n] - Sn0_vals[n] for n in ns}
    D_extrap = richardson(ns[-2], Dn_vals[ns[-2]], ns[-1], Dn_vals[ns[-1]])
    E_extrap = richardson(ns[-2], En_vals[ns[-2]], ns[-1], En_vals[ns[-1]])
    Dt = D_target(g)
    Et = E_target(g)
    results[g] = (D_extrap, Dt, E_extrap, Et)
    doc_D_extrap = doc_table[g][1]
    print(f"{g:6.2f} {Kused:8d} {D_extrap:19.10f} {Dt:12.8f} {D_extrap - Dt:13.3e} "
          f"{doc_D_extrap:16.8f} {D_extrap - doc_D_extrap:15.3e}")

print()
print(f"{'gamma':>6} {'E_n extrap (mine)':>19} {'E target':>12} {'diff (mine)':>13} "
      f"{'doc E_n extrap':>16} {'doc-mine diff':>15}")
for g in gammas:
    D_extrap, Dt, E_extrap, Et = results[g]
    doc_E_extrap = doc_table[g][4]
    print(f"{g:6.2f} {E_extrap:19.10f} {Et:12.8f} {E_extrap - Et:13.3e} "
          f"{doc_E_extrap:16.8f} {E_extrap - doc_E_extrap:15.3e}")

print()
print("=" * 100)
print("PART 2: R_n cross-check at n=2^18 against BOTH fronts' printed tables")
print("=" * 100)
n = 2 ** 18
wave17_table = {
    0.1: 1.0256418673, 0.2: 1.0536343736, 0.3: 1.0841136908, 0.4: 1.1174389803,
    0.5: 1.1540659874, 0.6: 1.1945670586, 0.7: 1.2396676769, 0.8: 1.2903013199,
    0.9: 1.3476917252, 0.99: 1.4064644540, 1.0: 1.4134793898,
}
print(f"{'gamma':>6} {'target sqrt(2/(2-g))':>21} {'R_n (mine)':>14} {'wave17 table':>14} "
      f"{'mine-wave17':>13} {'sqrt(n)(R-target) mine':>23}")
for g in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]:
    Sv, K = Sn_and_pieces(n, g)
    Rn = (Sv / n) / phi_infty(g * n)
    target = np.sqrt(2 / (2 - g))
    w17 = wave17_table[g]
    print(f"{g:6.2f} {target:21.12f} {Rn:14.10f} {w17:14.10f} {Rn - w17:13.3e} "
          f"{np.sqrt(n) * (Rn - target):23.6f}")
