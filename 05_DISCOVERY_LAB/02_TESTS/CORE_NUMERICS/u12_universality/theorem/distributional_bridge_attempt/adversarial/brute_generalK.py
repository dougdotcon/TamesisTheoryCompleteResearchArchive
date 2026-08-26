"""
Independent brute-force check, general K, of:
  (a) Lemma P2's exact second-moment decomposition identity
  (b) the P_nn(n,K) values reported in ATTEMPT.md Table (Sec 7.1(c))
  (c) the exact pattern P_nn(n,1) = 1/2 + 1/(6n)

Model (Definition 4): rerouted indices fixed WLOG at {0,...,K-1} (0-indexed).
pi ranges over all n! permutations of {0,...,n-1}; (U_0,...,U_{K-1}) ranges
over all n^K tuples, each in {0,...,n-1}, independent of pi. Every
(pi, U-tuple) equally likely: n! * n^K total configurations.
f(i) = U_i for i < K,  f(i) = pi(i) for i >= K.

Exact Fraction arithmetic throughout.
"""
import sys, os, itertools, math
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cyclic import cyclic_mask


def brute_stats(n, K):
    """Return: dict k->count of T=k; count of (n-1,n-2 both cyclic) [nn pair,
    0-indexed last two indices, valid iff K<=n-2]; count of (n-1, 0 both
    cyclic) [nr pair, valid iff K>=1 and n-1>=K i.e. always for K<=n-1];
    count of (0,1 both cyclic) [rr pair, valid iff K>=2]; total configs."""
    idx = list(range(n))
    Tcounts = {}
    nn_cnt = 0
    nr_cnt = 0
    rr_cnt = 0
    have_nn = (K <= n - 2)
    have_nr = (K >= 1) and (n - 1 >= K)  # n-1 is a non-rerouted index (index n-1, rerouted are 0..K-1)
    have_rr = (K >= 2)
    total = 0
    for pi in itertools.permutations(idx):
        for U in itertools.product(range(n), repeat=K):
            f = list(U) + [pi[i] for i in range(K, n)]
            cm = cyclic_mask(f)
            T = sum(cm)
            Tcounts[T] = Tcounts.get(T, 0) + 1
            total += 1
            if have_nn and cm[n - 1] and cm[n - 2]:
                nn_cnt += 1
            if have_nr and cm[n - 1] and cm[0]:
                nr_cnt += 1
            if have_rr and cm[0] and cm[1]:
                rr_cnt += 1
    return Tcounts, nn_cnt, nr_cnt, rr_cnt, total, have_nn, have_nr, have_rr


def moments_from_counts(Tcounts, total, n):
    ET = sum(Fraction(c, total) * k for k, c in Tcounts.items())
    ET2 = sum(Fraction(c, total) * k * k for k, c in Tcounts.items())
    phi = ET / n
    EM2 = ET2 / Fraction(n * n)
    return phi, EM2


def check_lemma_P2(n, K):
    Tcounts, nn_cnt, nr_cnt, rr_cnt, total, have_nn, have_nr, have_rr = brute_stats(n, K)
    phi, EM2_direct = moments_from_counts(Tcounts, total, n)
    if not (have_nn and have_nr):
        return None  # need K<=n-2 for nn and K>=1,n-1>=K for nr; skip incomplete cells
    Pnn = Fraction(nn_cnt, total)
    Pnr = Fraction(nr_cnt, total)
    Prr = Fraction(rr_cnt, total) if have_rr else Fraction(0)  # coefficient is 0 anyway if K<2

    coeff_nn = Fraction((n - K) * (n - K - 1), n * n)
    coeff_nr = Fraction(2 * K * (n - K), n * n)
    coeff_rr = Fraction(K * (K - 1), n * n)

    EM2_lemma = phi / n + coeff_nn * Pnn + coeff_nr * Pnr + coeff_rr * Prr
    return {
        "n": n, "K": K,
        "phi": phi, "EM2_direct": EM2_direct, "EM2_lemma": EM2_lemma,
        "match": EM2_direct == EM2_lemma,
        "Pnn": Pnn, "Pnr": Pnr, "Prr": Prr, "have_rr": have_rr,
    }


def main():
    print("=== Lemma P2 exact identity cross-check ===")
    all_ok = True
    cells = []
    cells += [(n, 1) for n in range(3, 8)]
    cells += [(n, 2) for n in range(4, 8)]
    cells += [(n, 3) for n in range(5, 7)]
    for n, K in cells:
        r = check_lemma_P2(n, K)
        if r is None:
            continue
        all_ok = all_ok and r["match"]
        print(f"n={n:2d} K={K}  phi={str(r['phi']):>10}  EM2_direct={str(r['EM2_direct']):>10}  "
              f"EM2_lemma={str(r['EM2_lemma']):>10}  {'OK' if r['match'] else 'MISMATCH <<<<'}")
    print("ALL LEMMA P2 CHECKS MATCH" if all_ok else "MISMATCH FOUND IN LEMMA P2")

    print()
    print("=== P_nn(n,1) = 1/2 + 1/(6n) exact pattern check ===")
    all_ok2 = True
    for n in range(3, 8):
        r = check_lemma_P2(n, 1)
        claimed = Fraction(1, 2) + Fraction(1, 6 * n)
        ok = (r["Pnn"] == claimed)
        all_ok2 = all_ok2 and ok
        print(f"n={n}  Pnn={r['Pnn']}  claimed(1/2+1/(6n))={claimed}  {'OK' if ok else 'MISMATCH <<<<'}")
    print("ALL P_nn(n,1) PATTERN CHECKS MATCH" if all_ok2 else "MISMATCH FOUND")

    print()
    print("=== P_nn(n,K) values vs ATTEMPT.md Table Sec 7.1(c), K=2,3 ===")
    # ATTEMPT.md's own reported decimals (Sec 7.1(c) table), reproduced here
    # purely as a comparison target -- computed independently below, not read
    # from the front's own exact_enumeration_results.json.
    for n, K in [(4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3)]:
        r = check_lemma_P2(n, K)
        if r is None:
            print(f"n={n} K={K}: skipped (pair not available)")
            continue
        dec = float(r["Pnn"])
        print(f"n={n:2d} K={K}  Pnn(exact)={str(r['Pnn']):>10}  Pnn(decimal)={dec:.5f}   target 1/(K+1)={1/(K+1):.5f}")


if __name__ == "__main__":
    main()
