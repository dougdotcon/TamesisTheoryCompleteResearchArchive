"""u12-limit-characterization (wave 2): pre-registered runs T1-T4.

Independent Monte Carlo of the n->infinity limit object of the u12
ensemble (cycles ~ Poisson-Dirichlet(1) via stick-breaking; K reroutes
at uniform positions with uniform destinations; cyclic mass = mass of
reroute-free cycles + segment mass along cycles of the jump map g),
implemented from scratch (absolute-coordinate arithmetic, separate
free/segment accounting, truncation 1e-12), and compared against the
DERIVED closed form

    phi_inf(c) = int_0^1 exp(-c t^2) dt = 0.5*sqrt(pi/c)*erf(sqrt(c))

and its exact conditional-K values phi_K = 4^K (K!)^2/(2K+1)!.

Seeds, grids, N and acceptance criteria pre-registered in
METHODOLOGY_NOTE.md (T1: held-out grid, SeedSequence(20260821);
T2: wave-1 grid cross-check, SeedSequence(31337); T3: conditional-K,
SeedSequence(64206); T4: free-mass decomposition check on T2 cells).
Single execution, no selective reruns.
"""
import json
import math
import random
import sys
import time
from bisect import bisect_left, bisect_right

import numpy as np
from scipy.stats import chi2

TRUNC = 1e-12


def phi_formula(c):
    """Derived closed form: int_0^1 exp(-c t^2) dt."""
    if c == 0.0:
        return 1.0
    s = math.sqrt(c)
    return 0.5 * math.sqrt(math.pi / c) * math.erf(s)


def phi_K_formula(K):
    """Wallis: int_0^1 (1-t^2)^K dt = 4^K (K!)^2 / (2K+1)!."""
    return 4.0**K * math.factorial(K) ** 2 / math.factorial(2 * K + 1)


def one_realization(K, rng):
    """Return (cyclic_mass, free_mass) for K reroutes. rng: random.Random."""
    # --- stick-breaking PD(1) cycle lengths (absolute start coords) ---
    starts = [0.0]
    rem = 1.0
    while rem > TRUNC:
        L = rem * rng.random()
        starts.append(starts[-1] + L)
        rem -= L
    covered = starts[-1]
    ncyc = len(starts) - 1

    # --- reroute positions (drop the <=1e-12 residual dust) ---
    xs = sorted(rng.random() for _ in range(K))
    xs = [x for x in xs if x < covered]
    if not xs:
        return 1.0, 1.0
    m = len(xs)

    # cycle index of each reroute; per-cycle reroute lists (abs coords)
    cyc_of = [bisect_right(starts, x) - 1 for x in xs]
    percyc = {}
    for j in range(m):
        percyc.setdefault(cyc_of[j], []).append(j)  # xs sorted => lists sorted

    # free mass = residual dust + cycles without any reroute
    free = rem
    for ci in range(ncyc):
        if ci not in percyc:
            free += starts[ci + 1] - starts[ci]

    # --- destinations and jump map g (next reroute forward, cyclic) ---
    g = [-1] * m
    seglen = [0.0] * m
    for j in range(m):
        u = rng.random()
        if u >= covered:
            continue  # residual dust: absorbed (bias <= K*TRUNC)
        ci = bisect_right(starts, u) - 1
        lst = percyc.get(ci)
        if lst is None:
            continue  # reroute-free cycle: absorbed
        lo, hi = starts[ci], starts[ci + 1]
        k = bisect_left(xs, u, lst[0], lst[-1] + 1)
        if k > lst[-1]:  # wrap around the cycle
            tgt = lst[0]
            seglen[j] = (hi - u) + (xs[tgt] - lo)
        else:
            tgt = k
            seglen[j] = xs[tgt] - u
        g[j] = tgt

    # --- nodes on cycles of g (iterative path coloring) ---
    state = bytearray(m)  # 0 new, 1 on current path, 2 finished
    cyc_mass = free
    for s0 in range(m):
        if state[s0]:
            continue
        path = []
        v = s0
        while v != -1 and state[v] == 0:
            state[v] = 1
            path.append(v)
            v = g[v]
        if v != -1 and state[v] == 1:
            i = len(path) - 1
            while path[i] != v:
                i -= 1
            for w in path[i:]:
                cyc_mass += seglen[w]
        for w in path:
            state[w] = 2
    return cyc_mass, free


def run_cell(c, N, seed_seq, fixed_K=None):
    """One MC cell. Returns dict with mean/sem for total and free mass."""
    npg = np.random.default_rng(seed_seq)
    py_seed = int(npg.integers(0, 2**63 - 1))
    rng = random.Random(py_seed)
    if fixed_K is None:
        Ks = npg.poisson(c, size=N)
    else:
        Ks = np.full(N, fixed_K, dtype=np.int64)
    st = sf = st2 = sf2 = 0.0
    for i in range(N):
        tot, fr = one_realization(int(Ks[i]), rng)
        st += tot
        st2 += tot * tot
        sf += fr
        sf2 += fr * fr
    mt = st / N
    mf = sf / N
    vt = max(st2 / N - mt * mt, 0.0) * N / (N - 1)
    vf = max(sf2 / N - mf * mf, 0.0) * N / (N - 1)
    return dict(mean_total=mt, sem_total=math.sqrt(vt / N),
                mean_free=mf, sem_free=math.sqrt(vf / N), N=N)


def main():
    t_start = time.time()
    out = {"runs": {}, "criteria": {}}
    log = open(sys.path[0] + "/limit_sim.log", "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# u12-limit-characterization T1-T4 | started "
        + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    # ---------------- T1: held-out grid ----------------
    T1_C = [0.05, 0.25, 0.75, 1.5, 3.0, 7.0, 15.0, 30.0, 70.0, 100.0]
    N1 = 200_000
    spawns = np.random.SeedSequence(20260821).spawn(len(T1_C))
    t1 = []
    for c, ss in zip(T1_C, spawns):
        r = run_cell(c, N1, ss)
        pred = phi_formula(c)
        z = (r["mean_total"] - pred) / r["sem_total"]
        t1.append(dict(c=c, **r, formula=pred, z=z))
        say(f"[T1] c={c:g}: phi_MC={r['mean_total']:.6f}±{r['sem_total']:.6f} "
            f"formula={pred:.6f} z={z:+.2f} (N={N1})")
    chi1 = sum(row["z"] ** 2 for row in t1)
    p1 = float(chi2.sf(chi1, len(t1)))
    maxz1 = max(abs(row["z"]) for row in t1)
    say(f"[T1] chi2={chi1:.2f} (dof={len(t1)}) p={p1:.4f} max|z|={maxz1:.2f}")
    out["runs"]["T1_heldout"] = t1
    out["criteria"]["T1"] = dict(chi2=chi1, dof=len(t1), p=p1, max_abs_z=maxz1,
                                 passed=bool(p1 >= 0.01 and maxz1 < 4))

    # ---------------- T2: wave-1 grid, new seeds ----------------
    T2_C = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
    N2 = 200_000
    spawns = np.random.SeedSequence(31337).spawn(len(T2_C))
    t2 = []
    for c, ss in zip(T2_C, spawns):
        r = run_cell(c, N2, ss)
        pred = phi_formula(c)
        z = (r["mean_total"] - pred) / r["sem_total"]
        t2.append(dict(c=c, **r, formula=pred, z=z))
        say(f"[T2] c={c:g}: phi_MC={r['mean_total']:.6f}±{r['sem_total']:.6f} "
            f"formula={pred:.6f} z={z:+.2f} (N={N2})")
    chi2v = sum(row["z"] ** 2 for row in t2)
    p2 = float(chi2.sf(chi2v, len(t2)))
    maxz2 = max(abs(row["z"]) for row in t2)
    say(f"[T2] chi2={chi2v:.2f} (dof={len(t2)}) p={p2:.4f} max|z|={maxz2:.2f}")
    out["runs"]["T2_crosscheck"] = t2
    out["criteria"]["T2"] = dict(chi2=chi2v, dof=len(t2), p=p2, max_abs_z=maxz2,
                                 passed=bool(p2 >= 0.01 and maxz2 < 4))

    # ---------------- T3: conditional-K ----------------
    N3 = 400_000
    spawns = np.random.SeedSequence(64206).spawn(5)
    t3 = []
    for K, ss in zip([1, 2, 3, 4, 5], spawns):
        r = run_cell(None, N3, ss, fixed_K=K)
        pred = phi_K_formula(K)
        z = (r["mean_total"] - pred) / r["sem_total"]
        t3.append(dict(K=K, **r, formula=pred, z=z))
        say(f"[T3] K={K}: phi_MC={r['mean_total']:.6f}±{r['sem_total']:.6f} "
            f"phi_K={pred:.6f} z={z:+.2f} (N={N3})")
    chi3 = sum(row["z"] ** 2 for row in t3)
    p3 = float(chi2.sf(chi3, len(t3)))
    maxz3 = max(abs(row["z"]) for row in t3)
    say(f"[T3] chi2={chi3:.2f} (dof={len(t3)}) p={p3:.4f} max|z|={maxz3:.2f}")
    out["runs"]["T3_conditionalK"] = t3
    out["criteria"]["T3"] = dict(chi2=chi3, dof=len(t3), p=p3, max_abs_z=maxz3,
                                 passed=bool(p3 >= 0.01 and maxz3 < 4))

    # ---------------- T4: free-mass decomposition on T2 cells ----------
    t4 = []
    for row in t2:
        c = row["c"]
        pred = (1.0 - math.exp(-c)) / c
        z = (row["mean_free"] - pred) / row["sem_free"]
        t4.append(dict(c=c, mean_free=row["mean_free"],
                       sem_free=row["sem_free"], exact=pred, z=z))
        say(f"[T4] c={c:g}: free_MC={row['mean_free']:.6f}±"
            f"{row['sem_free']:.6f} exact=(1-e^-c)/c={pred:.6f} z={z:+.2f}")
    maxz4 = max(abs(row["z"]) for row in t4)
    say(f"[T4] max|z|={maxz4:.2f}")
    out["runs"]["T4_free_mass"] = t4
    out["criteria"]["T4"] = dict(max_abs_z=maxz4, passed=bool(maxz4 < 4))

    # ---------------- global chi2 (T1+T2 pooled, 17 cells) -------------
    chig = chi1 + chi2v
    pg = float(chi2.sf(chig, len(t1) + len(t2)))
    say(f"[GLOBAL T1+T2] chi2={chig:.2f} (dof={len(t1)+len(t2)}) p={pg:.4f}")
    out["criteria"]["global_T1T2"] = dict(chi2=chig, dof=len(t1) + len(t2), p=pg)

    ok = all(out["criteria"][k]["passed"] for k in ("T1", "T2", "T3", "T4"))
    say(f"# ALL PRE-REGISTERED CRITERIA PASSED: {ok}")
    say(f"# wall time: {time.time()-t_start:.1f} s")
    out["all_passed"] = bool(ok)

    with open(sys.path[0] + "/limit_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved limit_results.json")
    log.close()


if __name__ == "__main__":
    sys.path[0] = sys.path[0] or "."
    main()
