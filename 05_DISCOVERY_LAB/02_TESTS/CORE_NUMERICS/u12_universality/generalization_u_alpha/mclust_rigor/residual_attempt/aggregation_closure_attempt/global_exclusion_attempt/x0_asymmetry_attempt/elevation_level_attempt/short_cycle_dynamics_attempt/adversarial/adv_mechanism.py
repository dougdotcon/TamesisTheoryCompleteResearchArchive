"""
adv_mechanism.py -- large-scale, from-scratch, independent stress test of
Claim 1 (ATTEMPT.md sec 1 / DERIVATION_PREREG.md sec 1.3):

  For the M-CLUST(b) construction, if the pi-cycle through a point has
  length L:
   (a) L<=b, untouched by every seed (prob (1-c/n)^L): the cycle is
       DETERMINISTICALLY an f-cycle -- every point on it is cyclic under f
       with probability exactly 1 (because no point of it is ever pulled
       into R, so f == pi on it exactly).
   (b) L<=b, touched by >=1 seed: the ENTIRE cycle (not just the seed) is
       pulled into R, and it becomes permanently unreachable by any normal
       pi-step (every "run start" test on it fails).

This script never builds f or the cyclic mask -- claim 1 is purely about pi
and R, so we test it directly and vectorized, at much larger scale than
building f state can support, hunting hardest at the b-boundary (L=b-1,
L=b, L=b+1) and at cells engineered to force many seeds onto the same short
cycle.

Independent of short_cycle_dynamics_attempt/*.py, elevation_level_attempt/*.py,
elevation_level_attempt/adversarial/*.py -- none read or imported. Uses only
adv_engine.py (this review's own from-scratch utility module).
"""
import numpy as np
from adv_engine import pi_cycle_labels_lengths


def stress_cell(n, b, c, rng, n_instances, label):
    """Returns dict of counts for one (n,b,c) cell over n_instances instances."""
    p = c / n
    total_short_pts = 0
    total_untouched_pts = 0
    total_touched_pts = 0
    viol_untouched_in_R = 0       # claim (a) violation: untouched short point in R
    viol_touched_not_in_R = 0     # claim (b) violation: touched short point NOT in R
    viol_touched_has_runstart = 0  # claim (b) stronger form: touched short cycle
                                    # has a run-start (reachable by a normal step)
    # boundary bookkeeping
    exact_b_pts = 0
    bminus1_pts = 0
    bplus1_pts = 0
    max_seeds_on_one_short_cycle = 0

    for _ in range(n_instances):
        pi = rng.permutation(n)
        seeds = rng.random(n) < p
        R = np.zeros(n, dtype=bool)
        R[seeds] = True
        cur = np.nonzero(seeds)[0]
        for _ in range(b - 1):
            cur = pi[cur]
            R[cur] = True

        labels, L = pi_cycle_labels_lengths(pi)
        short = L <= b
        if not short.any():
            continue

        ncomp = labels.max() + 1
        seed_count_per_cycle = np.bincount(labels, weights=seeds.astype(np.int64),
                                            minlength=ncomp)
        has_seed_per_cycle = seed_count_per_cycle > 0
        has_seed_point = has_seed_per_cycle[labels]

        untouched = short & (~has_seed_point)
        touched = short & has_seed_point

        total_short_pts += int(short.sum())
        total_untouched_pts += int(untouched.sum())
        total_touched_pts += int(touched.sum())

        viol_untouched_in_R += int(np.sum(untouched & R))
        viol_touched_not_in_R += int(np.sum(touched & (~R)))

        # run-start test: p in R with pi^{-1}(p) not in R => normal step can
        # reach p. Build pi^{-1} once per instance.
        pi_inv = np.empty(n, dtype=pi.dtype)
        pi_inv[pi] = np.arange(n)
        run_start = R & (~R[pi_inv])
        viol_touched_has_runstart += int(np.sum(touched & run_start))

        exact_b_pts += int(np.sum(short & (L == b)))
        bminus1_pts += int(np.sum(short & (L == b - 1)))
        bplus1_pts += int(np.sum(L == b + 1))

        if has_seed_per_cycle.any():
            m = seed_count_per_cycle[short_cycle_ids := np.unique(labels[short & has_seed_point])]
            if m.size:
                max_seeds_on_one_short_cycle = max(max_seeds_on_one_short_cycle,
                                                    int(m.max()))

    return {
        "label": label, "n": n, "b": b, "c": c, "n_instances": n_instances,
        "total_short_pts": total_short_pts,
        "total_untouched_pts": total_untouched_pts,
        "total_touched_pts": total_touched_pts,
        "viol_a_untouched_in_R": viol_untouched_in_R,
        "viol_b_touched_not_in_R": viol_touched_not_in_R,
        "viol_b_touched_runstart": viol_touched_has_runstart,
        "exact_b_pts": exact_b_pts,
        "bminus1_pts": bminus1_pts,
        "bplus1_pts": bplus1_pts,
        "max_seeds_on_one_short_cycle": max_seeds_on_one_short_cycle,
    }


if __name__ == "__main__":
    import time
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        log.append(s)

    ss = np.random.SeedSequence(20260826001)
    rng = np.random.default_rng(ss)

    t0 = time.time()

    cells = [
        # (n, b, c, n_instances, label)
        (65536, 100, 1000, 6000, "target b=100,c=1000,n=65536"),
        (65536, 400, 100, 3000, "b=400,c=100,n=65536"),
        (65536, 200, 150, 3000, "b=200,c=150,n=65536"),
        # extreme-overlap edge case: small n, very high p, to force MANY
        # seeds onto the SAME short cycle and stress the "union of runs"
        # bookkeeping hardest
        (2000, 50, 800, 3000, "edge: small n=2000,b=50,c=800 (p=0.40)"),
        # another edge cell: b small, c moderate, many instances, to build
        # up statistics right at the L=b/b-1/b+1 boundary specifically
        (16384, 30, 300, 4000, "edge: n=16384,b=30,c=300 (p=0.0183)"),
    ]

    results = []
    for (n, b, c, ninst, label) in cells:
        r = stress_cell(n, b, c, rng, ninst, label)
        results.append(r)
        P(f"[{label}]")
        P(f"  instances={ninst}  total_short_pts={r['total_short_pts']}  "
          f"untouched={r['total_untouched_pts']}  touched={r['total_touched_pts']}")
        P(f"  claim(a) violations (untouched short point found in R): "
          f"{r['viol_a_untouched_in_R']}")
        P(f"  claim(b) violations (touched short point NOT in R): "
          f"{r['viol_b_touched_not_in_R']}")
        P(f"  claim(b)-strong violations (touched short cycle HAS a run-start,"
          f" i.e. reachable by a normal step): {r['viol_b_touched_runstart']}")
        P(f"  boundary: L=b pts={r['exact_b_pts']}  L=b-1 pts={r['bminus1_pts']}  "
          f"L=b+1 pts(long,for contrast)={r['bplus1_pts']}")
        P(f"  max seeds observed on a single short cycle: "
          f"{r['max_seeds_on_one_short_cycle']}")
        P("")

    total_short = sum(r["total_short_pts"] for r in results)
    total_untouched = sum(r["total_untouched_pts"] for r in results)
    total_viol = sum(r["viol_a_untouched_in_R"] + r["viol_b_touched_not_in_R"] +
                      r["viol_b_touched_runstart"] for r in results)

    P(f"=== COMBINED across {len(results)} cells ===")
    P(f"total short-cycle points examined (L<=b, touched+untouched): {total_short}")
    P(f"total untouched-short points examined: {total_untouched}")
    P(f"TOTAL VIOLATIONS (claim a + claim b + claim b-strong), summed: {total_viol}")
    P("MECHANISM CLAIM 1: " + ("CONFIRMED, 0 violations" if total_viol == 0
                                else f"REFUTED, {total_viol} violations found"))
    P(f"elapsed: {time.time()-t0:.1f}s")

    with open("adv_mechanism.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
