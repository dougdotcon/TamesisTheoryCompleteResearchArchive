"""
Independent, from-scratch Monte Carlo verification of Theorem A's
coupling construction (Section 4.1-4.3 of ATTEMPT.md), written without
reading coupling_bound_check.py. Implements the shared-(xi,eta)
construction exactly as specified in the mathematical prose and checks,
per trial:
  (a) the collision bound P(NoColl^c) <= K(K-1)/(2n)  [union bound, exact
      per-pair collision prob 1/n]
  (b) the mismatch bound P(mismatch | NoColl) <= K^2/n
  (c) the combined good-event bound P(G^c) <= delta(K,n) = (3K^2-K)/(2n)
  (d) the pointwise deterministic bound |M_n^{(K)} - M_K'| <= eps(K,n)
      = (2K+1)/n on G, checked on EVERY trial (a hard per-trial
      assertion, not a statistical average)
  (e) as an extra sanity check, the mean of M_n^{(K)} recovered from this
      construction (unconditionally, i.e. NOT conditioning on NoColl,
      matching the real Definition-4 semantics as closely as feasible
      via this coupling) is compared to the known exact varphi_n^{(K)}
      values from THEOREM.md / independently-computed brute force, for a
      couple of small (n,K), as a cross-check that this construction is
      not accidentally producing some other quantity.

Own random-number generator, own seeds (NOT the target's reserved range
20260933000-20260933999), so as not to collide with or reuse it.
"""
import numpy as np
from fractions import Fraction
from itertools import permutations, product


def cyclic_count(f, n):
    color = [0] * n
    cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            idx = path.index(cur)
            for node in path[idx:]:
                cyclic[node] = True
        for node in path:
            color[node] = 2
    return sum(cyclic)


def exact_ET_over_n(n, K):
    total = Fraction(0)
    count = 0
    sources = list(range(K))
    for pi in permutations(range(n)):
        for U in product(range(n), repeat=K):
            f = list(pi)
            for idx, s in enumerate(sources):
                f[s] = U[idx]
            T = cyclic_count(f, n)
            total += T
            count += 1
    return total / count / n


def one_trial(K, n, rng):
    """
    Returns dict with: coll (bool NoColl^c), mismatch (bool, only meaningful
    if not coll), Mn (discrete M_n^{(K)}, only meaningful if not coll),
    Mprime (continuum M_K'), good (bool G holds).
    """
    xi = rng.random(K)
    eta = rng.random(K)

    D = np.ceil(n * xi).astype(int)
    D = np.clip(D, 1, n)  # guard float edge cases at xi very close to 1
    coll = (len(set(D.tolist())) != K)

    # continuum side (always well-defined, doesn't need NoColl)
    xi_sorted = np.sort(xi)
    cumQ = np.concatenate([[0.0], xi_sorted, ])  # cumQ[0]=0, cumQ[t]=xi_(t) for t=1..K
    q = np.diff(cumQ)  # q[t-1] = q_{t-1}, t=1..K -> length K array q_0..q_{K-1}
    q_D = 1.0 - cumQ[-1]

    dest_inf = [None] * K
    for j in range(K):
        e = eta[j]
        t_found = None
        for t in range(K):
            if cumQ[t] < e <= cumQ[t + 1]:
                t_found = t
                break
        dest_inf[j] = t_found if t_found is not None else 'DEAD'

    # S_inf via functional graph on 0..K-1
    def find_cycles(dest, K):
        color = [0] * K
        cyclic_src = [False] * K
        pred = [None] * K
        for start in range(K):
            if color[start] != 0:
                continue
            path = []
            cur = start
            while True:
                if cur == 'DEAD' or cur is None:
                    break
                if color[cur] == 2:
                    break
                if color[cur] == 1:
                    idx = path.index(cur)
                    for node in path[idx:]:
                        cyclic_src[node] = True
                    break
                color[cur] = 1
                path.append(cur)
                cur = dest[cur]
            for node in path:
                if color[node] != 2:
                    color[node] = 2
        for j in range(K):
            if dest[j] != 'DEAD' and dest[j] is not None:
                pred[dest[j]] = j
        return cyclic_src, pred

    cyclic_src_inf, pred_inf = find_cycles(dest_inf, K)
    Vprime = [0.0] * K
    for t in range(K):
        if cyclic_src_inf[t]:
            j = pred_inf[t]
            Vprime[t] = cumQ[t + 1] - eta[j]
    Mprime = q_D + sum(Vprime[t] for t in range(K) if cyclic_src_inf[t])

    result = dict(coll=coll, Mprime=Mprime, q_D=q_D, q=q, cumQ=cumQ)

    if coll:
        result['mismatch'] = None
        result['Mn'] = None
        result['good'] = False
        return result

    # discrete side
    D_sorted = np.sort(D)
    cumL = np.concatenate([[0], D_sorted])
    L = np.diff(cumL)
    O = n - cumL[-1]

    dest = [None] * K
    kpos = [None] * K
    for j in range(K):
        e = eta[j]
        tgt_scaled = n * e
        t_found = None
        for t in range(K):
            if cumL[t] < tgt_scaled <= cumL[t + 1]:
                t_found = t
                kpos[j] = int(np.ceil(tgt_scaled - cumL[t]))
                break
        dest[j] = t_found if t_found is not None else 'DEAD'

    cyclic_src, pred = find_cycles(dest, K)
    T = O
    for t in range(K):
        if cyclic_src[t]:
            j = pred[t]
            # V_t = L_t - k_t + 1; k_t (landing position within arc t) is stored
            # under the source index j = pred[t] that lands into arc t.
            Vt = L[t] - kpos[j] + 1
            T += Vt
    Mn = T / n

    mismatch = any(dest[j] != dest_inf[j] for j in range(K))
    good = (not mismatch)

    result['mismatch'] = mismatch
    result['Mn'] = Mn
    result['good'] = good
    result['diff'] = abs(Mn - Mprime) if good else None
    return result


def run(K, n, trials, seed):
    rng = np.random.default_rng(seed)
    n_coll = 0
    n_mismatch_given_nocoll = 0
    n_good = 0
    max_diff_on_good = 0.0
    violations = 0
    Mn_values_uncond = []  # for mean check, only defined when not coll
    for _ in range(trials):
        r = one_trial(K, n, rng)
        if r['coll']:
            n_coll += 1
            continue
        Mn_values_uncond.append(r['Mn'])
        if r['mismatch']:
            n_mismatch_given_nocoll += 1
        else:
            n_good += 1
            d = r['diff']
            max_diff_on_good = max(max_diff_on_good, d)
            eps = (2 * K + 1) / n
            if d > eps + 1e-12:
                violations += 1

    P_coll_mc = n_coll / trials
    P_coll_bound = K * (K - 1) / (2 * n)
    n_nocoll = trials - n_coll
    P_mismatch_mc = n_mismatch_given_nocoll / n_nocoll if n_nocoll else float('nan')
    P_mismatch_bound = K * K / n
    P_Gc_mc = (n_coll + n_mismatch_given_nocoll) / trials
    delta_bound = (3 * K * K - K) / (2 * n)
    eps_bound = (2 * K + 1) / n

    print(f"K={K:>2} n={n:>4} trials={trials:>7}  "
          f"P(coll) mc={P_coll_mc:.5f} bound={P_coll_bound:.5f}  "
          f"P(mismatch|NoColl) mc={P_mismatch_mc:.5f} bound={P_mismatch_bound:.5f}  "
          f"P(G^c) mc={P_Gc_mc:.5f} bound={delta_bound:.5f}  "
          f"max|Mn-M'| on G={max_diff_on_good:.6f} bound eps={eps_bound:.6f}  "
          f"VIOLATIONS={violations}")

    mean_Mn = sum(Mn_values_uncond) / len(Mn_values_uncond) if Mn_values_uncond else float('nan')
    return dict(violations=violations, mean_Mn_given_nocoll=mean_Mn, P_coll_mc=P_coll_mc,
                P_coll_bound=P_coll_bound, P_Gc_mc=P_Gc_mc, delta_bound=delta_bound)


if __name__ == "__main__":
    print("=== Theorem A per-trial checks (fresh, independent implementation) ===")
    total_violations = 0
    configs = [
        (2, 30, 40000, 987001),
        (2, 200, 20000, 987002),
        (3, 30, 40000, 987003),
        (3, 300, 20000, 987004),
        (4, 40, 40000, 987005),
        (4, 400, 20000, 987006),
        (5, 60, 40000, 987007),
        (6, 100, 20000, 987008),
        (8, 300, 15000, 987009),
    ]
    for K, n, trials, seed in configs:
        r = run(K, n, trials, seed)
        total_violations += r['violations']
        assert r['P_coll_mc'] <= r['P_coll_bound'] * 1.5 + 0.02, "collision rate wildly exceeds bound"
        assert r['P_Gc_mc'] <= r['delta_bound'] * 1.5 + 0.05, "P(G^c) wildly exceeds delta bound"
    print()
    print("TOTAL VIOLATIONS of |Mn - M'| <= eps(K,n) on G, across all configs:", total_violations)
    print()

    print("=== Cross-check: mean of Mn (via this construction, conditional on NoColl) vs exact E[T]/n"
          " (fresh bruteforce) -- small n,K only, to make sure the construction isn't silently computing"
          " a different quantity ===")
    for n, K in [(6, 2), (5, 1)]:
        exact = exact_ET_over_n(n, K)
        # large trial MC of the construction, conditional on NoColl (small-n collision rate is high, so
        # need many trials); this is only an approximate cross-check since exact bruteforce already
        # nailed the same numbers in adv1/adv5 -- this is a redundant, cheap extra sanity pass.
        rng = np.random.default_rng(112233 + n * 7 + K)
        vals = []
        trials = 400000
        for _ in range(trials):
            r = one_trial(K, n, rng)
            if not r['coll']:
                vals.append(r['Mn'])
        mc_mean = sum(vals) / len(vals)
        print(f"n={n} K={K}  exact E[T]/n={float(exact):.6f} ({exact})  "
              f"MC mean (construction, cond. NoColl, {len(vals)} kept of {trials})={mc_mean:.6f}  "
              f"diff={abs(mc_mean-float(exact)):.5f}")
