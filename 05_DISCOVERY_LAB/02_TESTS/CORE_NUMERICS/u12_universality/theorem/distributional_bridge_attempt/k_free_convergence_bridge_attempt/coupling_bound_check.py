"""
Direct Monte Carlo verification of the pathwise coupling construction
behind Theorem A: builds the DISCRETE quantity M_n^{(K)} = T/n and the
CONTINUUM quantity M_K' from a SHARED pair of primitive vectors
(xi_0,...,xi_{K-1}) and (eta_0,...,eta_{K-1}), i.i.d. Uniform(0,1) each,
and checks, for many independent draws and several (n,K):

  (a) empirical P(collision among discrete dividers) vs the claimed bound
      K(K-1)/(2n);
  (b) empirical P(some dest(j) != dest^infty(j) | no collision) vs the
      claimed bound K^2/n;
  (c) on the "good event" (no collision AND all dest match): the pathwise
      bound |M_n^{(K)} - M_K'| <= (2K+1)/n, checked on EVERY such trial
      (a hard pass/fail, not a statistical average);
  (d) the resulting empirical CDF gap sup_x|F_n^{(K)}(x)-F_{M_K'}(x)|
      (estimated over a fine grid of x) against the combined analytic
      bound delta(K,n) + Lip(F_K)*eps(K,n).

No code from any other front is used.
"""
import math
import random


def ceil_div_frac(x_frac, n):
    # ceil(n * x) for x a float in (0,1); n integer
    return math.ceil(n * x_frac)


def run_one_trial(n, K, rng):
    xi = [rng.random() for _ in range(K)]
    eta = [rng.random() for _ in range(K)]

    # ---- discrete side ----
    D = [ceil_div_frac(x, n) for x in xi]  # each in {1,...,n}
    collision = (len(set(D)) != K)
    result = {"collision": collision}
    if collision:
        return result

    order = sorted(range(K), key=lambda i: D[i])
    Dsorted = [D[i] for i in order]
    cumL = [0] * (K + 1)
    for t in range(K):
        cumL[t + 1] = Dsorted[t]
    O = n - Dsorted[-1]
    Ls = [cumL[t + 1] - cumL[t] for t in range(K)]
    assert sum(Ls) + O == n

    # discrete dest(j) for j=0..K-1 via eta_j vs cumL thresholds (0-indexed
    # region t in {0,...,K-1} means eta_j*n in (cumL[t], cumL[t+1]]; region
    # K means DEAD, eta_j*n in (cumL[K], n])
    dest = []
    for j in range(K):
        z = eta[j] * n
        t = None
        for tt in range(K):
            if cumL[tt] < z <= cumL[tt + 1]:
                t = tt
                break
        if t is None:
            t = K  # DEAD
        dest.append(t)

    S = find_cycles(dest, K)

    # V_s (discrete) for s in S: need predecessor j with dest[j]==s
    T = O
    for s in S:
        j = None
        for jj in range(K):
            if dest[jj] == s:
                j = jj
                break
        assert j is not None
        z = eta[j] * n - cumL[s]
        k_s = math.ceil(z)
        assert 1 <= k_s <= Ls[s], (k_s, Ls[s], z)
        V_s = Ls[s] - k_s + 1
        T += V_s
    Mn = T / n

    # ---- continuum side (SAME xi, eta) ----
    xi_sorted = sorted(xi)
    cumQ = [0.0] * (K + 1)
    for t in range(K):
        cumQ[t + 1] = xi_sorted[t]
    qD = 1.0 - cumQ[K]

    dest_inf = []
    for j in range(K):
        z = eta[j]
        t = None
        for tt in range(K):
            if cumQ[tt] < z <= cumQ[tt + 1]:
                t = tt
                break
        if t is None:
            t = K
        dest_inf.append(t)

    Sinf = find_cycles(dest_inf, K)
    Mk_prime = qD
    for s in Sinf:
        j = None
        for jj in range(K):
            if dest_inf[jj] == s:
                j = jj
                break
        assert j is not None
        Vprime_s = cumQ[s + 1] - eta[j]
        assert 0 <= Vprime_s <= cumQ[s + 1] - cumQ[s] + 1e-12
        Mk_prime += Vprime_s

    dest_match = (dest == dest_inf)
    result.update(dict(Mn=Mn, Mk_prime=Mk_prime, S=S, Sinf=Sinf,
                        dest_match=dest_match, diff=abs(Mn - Mk_prime)))
    return result


def find_cycles(dest, K):
    """S = union of cycles of the functional graph on {0,...,K-1} induced
    by dest (values in {0,...,K-1} U {K=DEAD})."""
    S = set()
    for start in range(K):
        path = []
        seen = set()
        x = start
        while x < K and x not in seen:
            seen.add(x)
            path.append(x)
            x = dest[x]
        if x < K and x in seen:
            idx = path.index(x)
            for p in path[idx:]:
                S.add(p)
    return S


def target_F(K, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    return 1 - (1 - x * x) ** K


def main():
    RESERVED_SEED_BASE = 20260933200
    cases = [(2, 50), (2, 500), (4, 50), (4, 500), (6, 50), (6, 500), (8, 200)]
    trials = 60000
    grid = [i / 200.0 for i in range(1, 200)]

    print(f"{'K':>3} {'n':>5} {'trials':>7} {'P(coll) MC':>11} {'P(coll) bnd':>12} "
          f"{'P(mism|noColl) MC':>18} {'P(mism) bnd':>12} "
          f"{'max|Mn-Mkp| (good ev)':>23} {'bnd (2K+1)/n':>13} "
          f"{'sup|Fn-FMkp| MC':>16} {'analytic bnd':>13}")

    for idx, (K, n) in enumerate(cases):
        seed = RESERVED_SEED_BASE + idx
        rng = random.Random(seed)
        n_coll = 0
        n_mismatch_given_nocoll = 0
        n_nocoll = 0
        max_diff_good = 0.0
        n_good = 0
        Mn_samples = []
        Mkp_samples = []
        for _ in range(trials):
            r = run_one_trial(n, K, rng)
            if r["collision"]:
                n_coll += 1
                continue
            n_nocoll += 1
            Mn_samples.append(r["Mn"])
            Mkp_samples.append(r["Mk_prime"])
            if not r["dest_match"]:
                n_mismatch_given_nocoll += 1
                continue
            n_good += 1
            max_diff_good = max(max_diff_good, r["diff"])

        p_coll_mc = n_coll / trials
        p_coll_bnd = K * (K - 1) / (2 * n)
        p_mis_mc = (n_mismatch_given_nocoll / n_nocoll) if n_nocoll else float('nan')
        p_mis_bnd = K * K / n
        eps_bnd = (2 * K + 1) / n

        # empirical sup_x |F_n^{(K)}(x) - F_{M_K'}(x)| over the sampled
        # (unconditional on collision -- both Mn,Mkp sample lists are drawn
        # from the SAME no-collision-conditioned trials, so this compares
        # their conditional empirical CDFs; a fully unconditional version
        # would need to also fold in the collision trials, which contribute
        # <= p_coll_mc to any CDF gap by a trivial union bound, consistent
        # with delta(K,n) already including the collision-probability term)
        Mn_sorted = sorted(Mn_samples)
        Mkp_sorted = sorted(Mkp_samples)
        m1, m2 = len(Mn_sorted), len(Mkp_sorted)
        sup_gap = 0.0
        for x in grid:
            import bisect
            f1 = bisect.bisect_right(Mn_sorted, x) / m1
            f2 = bisect.bisect_right(Mkp_sorted, x) / m2
            sup_gap = max(sup_gap, abs(f1 - f2))

        delta_bnd = p_coll_bnd + p_mis_bnd  # additive good-event failure bound
        # Lipschitz constant of F_K (used for the FINAL, Claim-B-conditional
        # bound only -- not needed to interpret this script's (a)-(c) checks,
        # shown here just for context / cross-reference with the write-up)
        lip_K = 2 * math.sqrt(K)
        analytic_bnd = delta_bnd + lip_K * eps_bnd

        print(f"{K:>3} {n:>5} {trials:>7} {p_coll_mc:>11.5f} {p_coll_bnd:>12.5f} "
              f"{p_mis_mc:>18.5f} {p_mis_bnd:>12.5f} "
              f"{max_diff_good:>23.6f} {eps_bnd:>13.6f} "
              f"{sup_gap:>16.5f} {analytic_bnd:>13.5f}")


if __name__ == "__main__":
    main()
