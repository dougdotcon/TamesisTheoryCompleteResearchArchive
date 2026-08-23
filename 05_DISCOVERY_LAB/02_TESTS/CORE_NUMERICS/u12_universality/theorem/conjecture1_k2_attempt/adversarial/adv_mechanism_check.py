"""
ADVERSARIAL REFEREE -- independent, from-scratch, per-CELL check of the 9-cell
mechanism table in ATTEMPT.md sec 3 ("Step B -- the reroute dynamics given
(m1,m2)"). This is the part neither the front's own R4 (aggregate density KS
test) nor the orchestrating session's symbolic re-derivation actually tested:
whether the CLOSED-FORM formula claimed for each of the 9 raw (u1-landing,
u2-landing) combinations is mechanically correct.

Method (fully independent -- builds the actual mapping f and finds its cyclic
set by literal orbit-tracing; does not import any formula from ATTEMPT.md or
its scripts beyond the table entries being tested, which are re-typed here by
hand from the document text for comparison purposes only):

  1. Draw a fresh uniform random permutation pi of [n] (background).
  2. Draw two distinct labels x1, x2 uniformly (randomizes across trials).
  3. Determine region1 (points whose background-forward flow reaches x1
     before x2, if ever) and region2 (symmetric for x2) as explicit ordered
     lists (far-edge -> source), exactly as in Lemma 1's own definition.
     m1, m2 = their lengths.
  4. Draw u1, u2 i.i.d. uniform on [n] (reroute destinations).
  5. Classify each of u1, u2 as landing in region1 ("R1"), region2 ("R2") or
     OUT, and record its 0-indexed position within its region if applicable
     (0 = far edge, region-length-1 = the source itself).
  6. Build f = pi except f[x1]=u1, f[x2]=u2. Find the ACTUAL cyclic set of f
     by a standard from-scratch color-marking orbit-trace (ground truth,
     no formulas assumed).
  7. Independently compute the CLAIMED cyclic mass using the 9-cell table
     from ATTEMPT.md sec 3, hand-transcribed below, as a function of
     (region-landing class of u1, u2) and the measured positions.
  8. Compare claimed vs actual EXACTLY (this is discrete combinatorics --
     the mechanism claim, if correct, should hold with exact equality at
     every finite n, not just asymptotically, since it is a graph-theoretic
     fact about a specific finite mapping, not a distributional limit).

Any mismatch, even in one trial, is reported with full diagnostic detail.
"""
import numpy as np
import json
from collections import defaultdict, Counter

def trace_cycle(pi, start):
    seq = [start]
    pos = {start: 0}
    cur = pi[start]
    while cur != start:
        seq.append(cur)
        pos[cur] = len(seq) - 1
        cur = pi[cur]
    return seq, pos

def build_regions(pi, x1, x2, n):
    seq, pos = trace_cycle(pi, x1)
    L1 = len(seq)
    if x2 in pos:
        posx2 = pos[x2]
        A = posx2
        m1 = L1 - A
        m2 = A
        region2_ordered = seq[1:posx2+1]            # after x1 up to & incl x2, len m2
        region1_ordered = seq[posx2+1:] + [x1]        # after x2 around to x1 incl, len m1
        same_block = True
    else:
        region1_ordered = seq[1:] + [x1]
        m1 = L1
        seq2, pos2 = trace_cycle(pi, x2)
        m2 = len(seq2)
        region2_ordered = seq2[1:] + [x2]
        same_block = False
    return region1_ordered, region2_ordered, m1, m2, same_block

def find_cyclic(f, n):
    color = np.zeros(n, dtype=np.int8)  # 0 unvisited, 1 in-path, 2 done
    cyclic = np.zeros(n, dtype=bool)
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        pos_in_path = {}
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            pos_in_path[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            idx = pos_in_path[cur]
            for node in path[idx:]:
                cyclic[node] = True
        for node in path:
            color[node] = 2
    return cyclic

def claimed_new_mass(c1, p1, c2, p2, m1, m2):
    """Hand-transcribed from ATTEMPT.md sec 3's 3x3 table (the FIRST table,
    listing the *new* cyclic mass created within the disturbed region --
    NOT yet including the always-cyclic OUT mass, which is added separately)."""
    if c1 == 'R1' and c2 == 'R2':
        # both self: D1=p1 (u1's pos in region1), D2=p2 (u2's pos in region2)
        return (m1 - p1) + (m2 - p2)
    if c1 == 'R1' and c2 == 'R1':
        return (m1 - p1)
    if c1 == 'R1' and c2 == 'OUT':
        return (m1 - p1)
    if c1 == 'R2' and c2 == 'R2':
        return (m2 - p2)
    if c1 == 'R2' and c2 == 'R1':
        # double-cross: E2 = p1 (u1's pos within region2), E1 = p2 (u2's pos within region1)
        E2 = p1
        E1 = p2
        return (m1 - E1) + (m2 - E2)
    if c1 == 'R2' and c2 == 'OUT':
        return 0
    if c1 == 'OUT' and c2 == 'R2':
        return (m2 - p2)
    if c1 == 'OUT' and c2 == 'R1':
        return 0
    if c1 == 'OUT' and c2 == 'OUT':
        return 0
    raise ValueError((c1, c2))

def cell_name(c1, c2):
    return f"u1={c1},u2={c2}"

def run(n, n_trials, seed, verbose_mismatches=10):
    rng = np.random.default_rng(seed)
    mismatches = []
    cell_counts = Counter()
    cell_match = Counter()
    n_u1_eq_u2 = 0
    n_u_eq_source = 0
    for t in range(n_trials):
        pi = rng.permutation(n)
        x1, x2 = rng.choice(n, size=2, replace=False)
        x1, x2 = int(x1), int(x2)
        region1_ordered, region2_ordered, m1, m2, same_block = build_regions(pi, x1, x2, n)
        pos1_map = {p: i for i, p in enumerate(region1_ordered)}
        pos2_map = {p: i for i, p in enumerate(region2_ordered)}

        u1 = int(rng.integers(0, n))
        u2 = int(rng.integers(0, n))
        if u1 == u2:
            n_u1_eq_u2 += 1
        if u1 == x1 or u2 == x2:
            n_u_eq_source += 1

        def classify(pt):
            if pt in pos1_map:
                return ('R1', pos1_map[pt])
            if pt in pos2_map:
                return ('R2', pos2_map[pt])
            return ('OUT', None)

        c1, p1 = classify(u1)
        c2, p2 = classify(u2)

        f = np.array(pi, copy=True)
        f[x1] = u1
        f[x2] = u2
        cyclic = find_cyclic(f, n)
        actual_M2 = int(cyclic.sum())

        OUT_mass = n - m1 - m2
        new_mass = claimed_new_mass(c1, p1, c2, p2, m1, m2)
        claimed_M2 = OUT_mass + new_mass

        cname = cell_name(c1, c2)
        cell_counts[cname] += 1
        if claimed_M2 == actual_M2:
            cell_match[cname] += 1
        else:
            if len(mismatches) < verbose_mismatches:
                mismatches.append(dict(
                    trial=t, n=n, x1=x1, x2=x2, u1=u1, u2=u2,
                    m1=m1, m2=m2, same_block=same_block,
                    c1=c1, p1=p1, c2=c2, p2=p2,
                    OUT_mass=OUT_mass, new_mass_claimed=new_mass,
                    claimed_M2=claimed_M2, actual_M2=actual_M2,
                ))

    total_trials = n_trials
    total_match = sum(cell_match.values())
    return dict(
        n=n, n_trials=n_trials, seed=seed,
        total_match=total_match, total_trials=total_trials,
        exact_match_rate=total_match / total_trials,
        n_u1_eq_u2=n_u1_eq_u2, n_u_eq_source=n_u_eq_source,
        cell_counts=dict(cell_counts), cell_match=dict(cell_match),
        cell_match_rate={k: cell_match[k] / cell_counts[k] for k in cell_counts},
        mismatches=mismatches,
    )

def main():
    all_results = {}
    # Config chosen so all 9 raw cells get non-trivial coverage: moderate n
    # keeps region masses a sizeable fraction of n so cross/self/OUT all occur
    # with decent frequency; large trial count for statistical confidence.
    for n, n_trials, seed in [(30, 200000, 20260836011), (200, 60000, 20260836012)]:
        res = run(n, n_trials, seed)
        all_results[f"n={n}"] = res
        print(f"=== n={n}, trials={n_trials} ===")
        print(f"exact match rate: {res['exact_match_rate']:.8f} "
              f"({res['total_match']}/{res['total_trials']})")
        print(f"u1==u2 collisions: {res['n_u1_eq_u2']}, "
              f"u_i==own source collisions: {res['n_u_eq_source']}")
        print("per-cell counts / match-rate:")
        for k in sorted(res['cell_counts']):
            print(f"  {k}: n={res['cell_counts'][k]:7d}  match_rate={res['cell_match_rate'][k]:.6f}")
        if res['mismatches']:
            print(f"!!! {len(res['mismatches'])} MISMATCHES (showing up to 10):")
            for m in res['mismatches']:
                print("   ", m)
        print()

    with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_mechanism_check.json", "w") as f:
        json.dump(all_results, f, indent=2, default=str)

if __name__ == "__main__":
    main()
