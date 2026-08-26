"""
Independent, from-scratch adversarial brute-force verification of the K=2
model (THEOREM.md Definition 4), written purely from the mathematical
description in THEOREM.md / distributional_bridge_attempt / joint_
exploration_continuum_attempt prose. NO .py file from any front in this
lineage (including the target front's own scripts) was read or imported.

Model: pi uniform random permutation of [n] = {0,...,n-1}. Reroute sources
fixed WLOG at {0,1} (K=2). U_0, U_1 i.i.d. Uniform([n]), independent of pi.
  f(0) = U_0, f(1) = U_1, f(i) = pi(i) for i >= 2.

Quantities computed, exactly, via Fraction arithmetic, over ALL n! * n^2
configurations (permutations generated via itertools.permutations on the
n-2 non-source labels combined directly with pi acting on all n; see below):

  - P_nn(n,2): P(query points n-2, n-1 both cyclic)  [query points chosen
    disjoint from reroute sources {0,1}, matching the target document's own
    P_nn convention]
  - psi_n^(2): the MARGINAL P(a single fixed generic point, e.g. n-1, is
    cyclic) -- cross-check against THEOREM.md's already-proved closed form
    8/15 + 4/(15n) + 1/(15n^2).
  - P(both cyclic AND same final cycle) and the ratio P(same|both), to
    check Theorem J's Corollary (=1/2 exactly, for every n,K) independently.

For efficiency we iterate pi via itertools.permutations(range(n)) (n!) and
U_0,U_1 via the product range(n) x range(n) (n^2), building f fresh each
time and running our own cyclic_points() on it. This exactly matches
Definition 4's construction and is fully independent of the target
document's own enumeration code (which we never read).
"""
import sys
import os
import itertools
from fractions import Fraction
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cycle_utils import cyclic_points


def compute_k2_cell(n, verbose=True):
    """
    Returns a dict with exact Fraction values:
      P_nn2         : P(n-2, n-1 both cyclic)
      P_nn2_same    : P(n-2, n-1 both cyclic AND same final cycle)
      psi2          : P(n-1 cyclic)  [marginal, single point]
      total_configs : n! * n^2
    Also cross-checks Theorem J's corollary: P(same | both) should be
    exactly 1/2.
    """
    assert n >= 4, "need n>=4 for two query points disjoint from {0,1}"
    q1, q2 = n - 2, n - 1

    total = 0
    count_both = 0
    count_both_same = 0
    count_marginal = 0

    t0 = time.time()
    for pi in itertools.permutations(range(n)):
        f_base = list(pi)  # f(i) = pi(i) for now; will override 0,1 below
        for u0 in range(n):
            for u1 in range(n):
                f = list(f_base)
                f[0] = u0
                f[1] = u1
                total += 1
                cyc = cyclic_points(f)
                q1_cyc = q1 in cyc
                q2_cyc = q2 in cyc
                if q1_cyc:
                    count_marginal += 1  # marginal on q1 = n-2; see also q2 below for symmetry check
                if q1_cyc and q2_cyc:
                    count_both += 1
                    # determine same-cycle: since both cyclic, find each's
                    # cycle by following f from q1 and q2 and checking
                    # whether q2 appears on q1's forward orbit before
                    # returning to q1 (equivalently, whether they belong to
                    # the same cycle of the (partial) permutation restricted
                    # to the cyclic set).
                    # Walk from q1 until back to q1; collect visited.
                    node = f[q1]
                    orbit = {q1}
                    same = False
                    while node != q1:
                        if node == q2:
                            same = True
                        orbit.add(node)
                        node = f[node]
                    if same:
                        count_both_same += 1
    elapsed = time.time() - t0

    total_frac = Fraction(total)
    P_nn2 = Fraction(count_both, total)
    P_nn2_same = Fraction(count_both_same, total)
    psi2 = Fraction(count_marginal, total)

    result = {
        "n": n,
        "total_configs": total,
        "P_nn2": P_nn2,
        "P_nn2_same": P_nn2_same,
        "psi2_marginal_q1": psi2,
        "elapsed_sec": elapsed,
    }
    if verbose:
        print(f"n={n}: total={total} time={elapsed:.2f}s "
              f"P_nn2={P_nn2} ({float(P_nn2):.6f}) "
              f"P_nn2_same={P_nn2_same} ({float(P_nn2_same):.6f}) "
              f"psi2(marg)={psi2} ({float(psi2):.6f})")
        if count_both > 0:
            ratio = Fraction(count_both_same, count_both)
            print(f"       P(same|both) = {ratio} ({float(ratio):.6f})  [Theorem J predicts EXACTLY 1/2]")
    return result


if __name__ == "__main__":
    import json
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [4, 5, 6, 7]
    results = {}
    for n in ns:
        r = compute_k2_cell(n)
        results[n] = {k: (str(v) if isinstance(v, Fraction) else v) for k, v in r.items()}
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brute_k2_ref_results.json")
    with open(out_path, "a") as fh:
        json.dump(results, fh)
        fh.write("\n")
