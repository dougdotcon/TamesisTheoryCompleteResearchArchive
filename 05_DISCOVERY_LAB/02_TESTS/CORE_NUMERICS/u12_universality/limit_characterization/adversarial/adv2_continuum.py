"""Surfaces (b2) and (d): direct simulation of the n->infinity limit object.

Construction (structural, NOT via the exploration-process derivation):
 - cycle lengths: stick-breaking GEM(1) until residual < 1e-12; residual
   treated as unmarked cyclic dust (marks/jumps landing there: absorb-fail
   for jumps; mark probability ~1e-12, ignored).
 - K marks (Poisson(c) for (b2); fixed K for (d)) at uniform positions,
   uniform jump destinations.
 - cyclic mass per realization (exact given the realization):
     mass of cycles with no marks (+ residual dust)
   + sum over edges of cycles of the mark->mark jump graph of the segment
     length from destination u_i forward to the next mark.
   Mark->mark graph: mark i jumps to u_i; if u_i is on a marked cycle,
   successor = first mark at arc-distance >= 0 forward from u_i; else sink.
   Cycles of that functional graph found by iterated-visit walk.

Per-realization output is the exact conditional cyclic mass given the
structure; averaging over realizations estimates phi_infinity(c).
"""
import numpy as np, json, math, sys, time
from bisect import bisect_left

ROOT = sys.path[0]
EPS = 1e-12

def one_realization(c, rng, K=None):
    # stick-breaking GEM(1)
    lengths = []
    starts = []
    rem = 1.0
    pos = 0.0
    while rem > EPS:
        u = rng.random()
        L = rem * u
        lengths.append(L)
        starts.append(pos)
        pos += L
        rem -= L
    lengths = np.array(lengths)
    starts = np.array(starts)
    ncyc = len(lengths)
    marked_end = pos  # mass in explicit cycles; [pos,1) is dust
    if K is None:
        K = rng.poisson(c)
    if K == 0:
        return 1.0
    marks = rng.random(K) * 1.0
    dests = rng.random(K) * 1.0
    # assign marks to cycles (marks in dust: prob ~1e-12, treat as no-op mark on dust -> ignore)
    keep = marks < marked_end
    marks = marks[keep]
    if len(marks) == 0:
        return 1.0
    K = len(marks)
    dests = dests[:K]  # keep pairing arbitrary; dests iid uniform anyway
    cyc_idx = np.searchsorted(starts, marks, side="right") - 1
    # per-cycle sorted mark local positions
    marks_by_cycle = {}
    for i in range(K):
        marks_by_cycle.setdefault(int(cyc_idx[i]), []).append(i)
    local = marks - starts[cyc_idx]  # position within cycle
    sorted_marks = {}  # cycle -> (sorted local positions, mark ids)
    for cy, ids in marks_by_cycle.items():
        loc = [(local[i], i) for i in ids]
        loc.sort()
        sorted_marks[cy] = ([x for x, _ in loc], [i for _, i in loc])
    # unmarked cycle mass + dust
    unmarked = (1.0 - marked_end) + sum(
        lengths[cy] for cy in range(ncyc) if cy not in sorted_marks)
    # successor of each mark: where does its destination lead?
    succ = np.full(K, -1, dtype=int)       # -1 = sink (unmarked cycle or dust)
    seglen = np.zeros(K)                   # arc length dest -> next mark
    for i in range(K):
        d = dests[i]
        if d >= marked_end:
            continue
        cy = int(np.searchsorted(starts, d, side="right") - 1)
        sm = sorted_marks.get(cy)
        if sm is None:
            continue
        loc, ids = sm
        dloc = d - starts[cy]
        j = bisect_left(loc, dloc)
        if j < len(loc):
            succ[i] = ids[j]
            seglen[i] = loc[j] - dloc
        else:  # wrap to first mark on the cycle
            succ[i] = ids[0]
            seglen[i] = (lengths[cy] - dloc) + loc[0]
    # find cyclic marks of the succ functional graph (with sinks)
    state = np.zeros(K, dtype=np.int8)
    cyclic_edge_mass = 0.0
    orderpos = {}
    for s in range(K):
        if state[s]:
            continue
        path = []
        v = s
        while v != -1 and state[v] == 0:
            state[v] = 1
            orderpos[v] = len(path)
            path.append(v)
            v = succ[v]
        if v != -1 and state[v] == 1:
            # cycle: marks path[orderpos[v]:]; add their outgoing segment lengths
            for w in path[orderpos[v]:]:
                cyclic_edge_mass += seglen[w]
        for w in path:
            state[w] = 2
    return unmarked + cyclic_edge_mass

def run(c, N, seed, K=None):
    rng = np.random.default_rng(seed)
    tot = 0.0
    tot2 = 0.0
    for _ in range(N):
        v = one_realization(c, rng, K=K)
        tot += v
        tot2 += v * v
    m = tot / N
    var = tot2 / N - m * m
    return m, math.sqrt(max(var, 0) / N)

if __name__ == "__main__":
    t0 = time.time()
    out = {"poisson": {}, "conditional": {}}
    print("== (b2) Poisson(c) continuum, seed 55510123 ==", flush=True)
    cs = [0.37, 0.5, 1.0, 2.71828, 7.5, 23.0, 50.0]
    N = 400000
    chi2 = 0.0
    for ci, c in enumerate(cs):
        m, sem = run(c, N, 55510123 + ci)
        phi = 0.5*math.sqrt(math.pi/c)*math.erf(math.sqrt(c))
        z = (m - phi)/sem
        chi2 += z*z
        out["poisson"][str(c)] = {"N": N, "mean": m, "sem": sem, "phi_claim": phi,
                                  "dev": m - phi, "z": z}
        print(f"c={c}: phi_cont = {m:.6f} +- {sem:.6f}  claim {phi:.6f}  dev {m-phi:+.6f}  z={z:+.2f}  [{time.time()-t0:.0f}s]", flush=True)
    from scipy import stats
    p = float(stats.chi2.sf(chi2, len(cs)))
    out["poisson_chi2"] = {"chi2": chi2, "dof": len(cs), "p": p}
    print(f"joint chi2 = {chi2:.2f} / {len(cs)} dof, p = {p:.3f}", flush=True)

    print("== (d) fixed-K conditional law, seed 90210777 ==", flush=True)
    targets = {1: 2/3, 2: 8/15, 3: 16/35}
    N2 = 400000
    for K in [1, 2, 3]:
        m, sem = run(0.0, N2, 90210777 + K, K=K)
        t = targets[K]
        z = (m - t)/sem
        out["conditional"][str(K)] = {"N": N2, "mean": m, "sem": sem,
                                      "target_4K_KfactSq_over_2K1fact": t,
                                      "dev": m - t, "z": z}
        print(f"K={K}: phi_K = {m:.6f} +- {sem:.6f}  target {t:.6f}  dev {m-t:+.6f}  z={z:+.2f}  [{time.time()-t0:.0f}s]", flush=True)
    with open(ROOT + "/adv2_continuum.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"saved adv2_continuum.json  total {time.time()-t0:.0f}s")
