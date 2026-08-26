"""
K=3 stress test (adversarial mandate item 11): is the target document's
diagnosis -- that K=3 needs a genuinely new "functional graph on arcs"
treatment, not just more bookkeeping on the K=2-style flat table -- correct?

We build the "all three sources on one pi-cycle, cyclic order 0->1->2->0"
topology explicitly:
   0 -> e_1 -> ... -> e_{p-1} -> 1 -> b_1 -> ... -> b_{q-1} -> 2
     -> c_1 -> ... -> c_{r-1} -> 0
(arc_A = e's, ending at source 1; arc_B = b's, ending at source 2;
 arc_C = c's, ending at source 0), plus O outside fixed points, n=p+q+r+O.

Sources: 0,1,2 with independent reroute targets U_0,U_1,U_2 in [n].

TEST: does P(e_i cyclic) [e_i interior to arc_A, at position i] depend on
q,r only through the SUM q+r (as a naive flat/K=2-style extrapolation of
Lemma 2's R1 formula "i(n+q)/n^2" would suggest, replacing the single
"other arc length q" by "total other-arc length q+r"), or does it depend
on the individual split (q,r) even when q+r is held fixed? If the latter,
this is direct evidence that per-arc bookkeeping (not just an aggregate)
is required at K=3 -- i.e. that treating "the other stuff" as one lump
sum (as sufficed at K=2, where there IS only one other arc) is NOT valid
once there are >=2 other arcs, supporting the target document's diagnosis
that a genuinely richer structure (the reduced functional graph on the
arcs themselves) is needed at K=3.
"""
import sys
import os
import itertools
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cycle_utils import cyclic_points


def build_pi_k3_onecycle(n, p, q, r, O):
    assert p >= 1 and q >= 1 and r >= 1
    assert p + q + r + O == n
    pi = [0] * n
    labels = list(range(3, n))  # 0,1,2 reserved as sources
    idx = 0

    e_pts = []
    for _ in range(p - 1):
        e_pts.append(labels[idx]); idx += 1
    b_pts = []
    for _ in range(q - 1):
        b_pts.append(labels[idx]); idx += 1
    c_pts = []
    for _ in range(r - 1):
        c_pts.append(labels[idx]); idx += 1
    outside = []
    for _ in range(O):
        outside.append(labels[idx]); idx += 1
    assert idx == n - 3

    chain = [0] + e_pts + [1] + b_pts + [2] + c_pts + [0]
    for a, b_ in zip(chain[:-1], chain[1:]):
        pi[a] = b_
    for o in outside:
        pi[o] = o

    e_full = e_pts + [1]  # e_1..e_p (e_p=1)
    return pi, e_pts, b_pts, c_pts, outside  # e_pts = interior only (e_1..e_{p-1})


def cyclic_prob_for_arcA_points(n, p, q, r, O):
    """Returns dict: position i (1..p-1) -> Fraction P(e_i cyclic), by full
    enumeration of (U0,U1,U2) in [n]^3."""
    pi, e_pts, b_pts, c_pts, outside = build_pi_k3_onecycle(n, p, q, r, O)
    total = n ** 3
    from collections import defaultdict
    count = defaultdict(int)
    for u0 in range(n):
        for u1 in range(n):
            for u2 in range(n):
                f = list(pi)
                f[0] = u0
                f[1] = u1
                f[2] = u2
                cyc = cyclic_points(f)
                for i, pt in enumerate(e_pts, start=1):
                    if pt in cyc:
                        count[i] += 1
    return {i: Fraction(c, total) for i, c in count.items()}


if __name__ == "__main__":
    # Fix n, p, and i; vary (q,r) with q+r held constant; see if P(e_i cyclic)
    # changes across different (q,r) splits.
    n = 10
    p = 4          # arc_A has 3 interior points e_1,e_2,e_3
    qr_sum = 4      # q+r fixed at 4 (so O = n-p-qr_sum = 2)
    O = n - p - qr_sum
    splits = [(q, qr_sum - q) for q in range(1, qr_sum)]  # q,r >=1

    print(f"n={n}, p={p} (arc_A interior positions 1..{p-1}), q+r fixed = {qr_sum}, O={O}")
    print("Testing whether P(e_i cyclic) depends on the (q,r) SPLIT, or only on q+r (naive flat guess).\n")

    results = {}
    for (q, r) in splits:
        probs = cyclic_prob_for_arcA_points(n, p, q, r, O)
        results[(q, r)] = probs
        print(f"  (q,r)=({q},{r}): P(e_i cyclic) for i=1..{p-1} -> "
              f"{[f'{probs[i]} ({float(probs[i]):.5f})' for i in sorted(probs)]}")

    # Check: are all splits identical (naive flat guess would predict yes)?
    first_split = splits[0]
    all_identical = all(results[s] == results[first_split] for s in splits)
    print()
    if all_identical:
        print("RESULT: P(e_i cyclic) is IDENTICAL across all (q,r) splits with q+r fixed")
        print("        -> the naive 'flat aggregate' extrapolation from K=2's formula "
              "WOULD be adequate for this marginal quantity (though joint/chain effects "
              "may still differ -- see joint test below).")
    else:
        print("RESULT: P(e_i cyclic) DIFFERS across (q,r) splits with q+r fixed")
        print("        -> confirms the naive flat/aggregate extrapolation of the K=2 "
              "formula is WRONG at K=3: the finer per-arc structure (not just a sum) "
              "genuinely matters, supporting the target document's diagnosis that K=3 "
              "requires new machinery (tracking the arcs individually / the induced "
              "functional graph on arcs), not just bigger bookkeeping on the same K=2-style flat table.")

    # Naive candidate formula check: i*(n+q+r)/n^2 (direct extrapolation of R1
    # with "q" -> "q+r", i.e. treating ALL non-home arcs as one lump).
    print()
    print("Naive candidate formula i*(n+q+r)/n^2 vs actual, per split:")
    for (q, r) in splits:
        probs = results[(q, r)]
        for i in sorted(probs):
            naive = Fraction(i * (n + q + r), n * n)
            actual = probs[i]
            flag = "MATCH" if naive == actual else "MISMATCH"
            print(f"  (q,r)=({q},{r}) i={i}: naive={naive} ({float(naive):.5f}) "
                  f"actual={actual} ({float(actual):.5f}) -> {flag}")
