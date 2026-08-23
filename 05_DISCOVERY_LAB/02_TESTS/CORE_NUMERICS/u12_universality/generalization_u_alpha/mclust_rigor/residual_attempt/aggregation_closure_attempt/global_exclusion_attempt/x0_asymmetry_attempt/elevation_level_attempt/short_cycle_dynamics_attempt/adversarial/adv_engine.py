"""
adv_engine.py -- independent, from-scratch M-CLUST(b) engine for the
adversarial review of short_cycle_dynamics_attempt/ATTEMPT.md.

Written without reading any .py file under short_cycle_dynamics_attempt/,
elevation_level_attempt/, or elevation_level_attempt/adversarial/. Built only
from the prose mechanism as stated in ATTEMPT.md / DERIVATION_PREREG.md
(quoted/paraphrased in the referee report we were handed) and the archive's
own prose derivation documents.

Mechanism (independently re-read from the target's own prose, not code):
  - n points, pi a uniform random permutation.
  - each point is an i.i.d. seed with probability p = c/n.
  - for each seed s, its "run" is the full b-point forward orbit
    {s, pi(s), pi^2(s), ..., pi^{b-1}(s)}  (the seed itself included).
  - R = union of all runs.
  - every point of R gets an i.i.d. Uniform([n]) destination (drawn once,
    fixed); outside R, f = pi.
  - phi = E[ (1/n) * #{x : x cyclic under f} ].

All randomness uses numpy.random.Generator seeded from a numpy
SeedSequence, never global numpy state.
"""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def pi_cycle_lengths(pi):
    """Exact cycle length of the pi-cycle through every point.

    pi is a permutation array. The directed graph i -> pi[i] is, because pi
    is a bijection, a disjoint union of simple cycles (every node has
    in-degree and out-degree exactly 1), so its weakly-connected components
    are exactly the pi-cycles, and component size = cycle length.
    """
    n = len(pi)
    rows = np.arange(n)
    data = np.ones(n, dtype=np.int8)
    A = coo_matrix((data, (rows, pi)), shape=(n, n))
    ncomp, labels = connected_components(A, directed=True, connection="weak")
    counts = np.bincount(labels, minlength=ncomp)
    return counts[labels]


def pi_cycle_labels_lengths(pi):
    """Like pi_cycle_lengths, but also returns the per-point cycle-id label
    (so cycles can be grouped vectorized, e.g. via np.bincount(labels, ...))."""
    n = len(pi)
    rows = np.arange(n)
    data = np.ones(n, dtype=np.int8)
    A = coo_matrix((data, (rows, pi)), shape=(n, n))
    ncomp, labels = connected_components(A, directed=True, connection="weak")
    counts = np.bincount(labels, minlength=ncomp)
    return labels, counts[labels]


def build_instance(n, b, c, rng):
    """Build one M-CLUST(b) instance.

    Returns dict with pi, seeds (bool mask), R (bool mask), f, cyc_len_pi
    (pi-cycle length of every point), n_seeds.
    """
    p = c / n
    pi = rng.permutation(n)
    seeds = rng.random(n) < p
    R = np.zeros(n, dtype=bool)
    R[seeds] = True
    cur = np.nonzero(seeds)[0]
    # b-point run = seed itself (already marked) + (b-1) forward steps
    for _ in range(b - 1):
        cur = pi[cur]
        R[cur] = True
    f = pi.copy()
    nR = int(R.sum())
    if nR > 0:
        f[R] = rng.integers(0, n, size=nR)
    cyc_len_pi = pi_cycle_lengths(pi)
    return {
        "pi": pi,
        "seeds": seeds,
        "R": R,
        "f": f,
        "cyc_len_pi": cyc_len_pi,
        "n_seeds": int(seeds.sum()),
    }


def cyclic_mask_peeling(f):
    """Cyclic-node mask of a functional graph f (every node out-degree 1),
    via in-degree peeling (repeatedly strip in-degree-0 leaves). Nodes never
    removed are exactly the cyclic ones. O(n), per-instance sequential
    (not batched -- long tails in this mechanism make round-synchronized
    batch peeling slow, as the target document itself notes; a sequential
    stack avoids that entirely).
    """
    n = len(f)
    indeg = np.bincount(f, minlength=n).astype(np.int64)
    stack = list(np.nonzero(indeg == 0)[0])
    removed = np.zeros(n, dtype=bool)
    while stack:
        x = stack.pop()
        if removed[x]:
            continue
        removed[x] = True
        y = f[x]
        indeg[y] -= 1
        if indeg[y] == 0 and not removed[y]:
            stack.append(y)
    return ~removed


def cyclic_mask_bruteforce(f):
    """O(n^2)-ish literal orbit-following cyclic mask, for cross-checking
    cyclic_mask_peeling on SMALL graphs only. x is cyclic iff iterating f
    from x returns to x before revisiting any other node."""
    n = len(f)
    cyclic = np.zeros(n, dtype=bool)
    for x in range(n):
        seen = set()
        cur = x
        while True:
            if cur == x and len(seen) > 0:
                cyclic[x] = True
                break
            if cur in seen:
                cyclic[x] = False
                break
            seen.add(cur)
            cur = f[cur]
    return cyclic


if __name__ == "__main__":
    # ---- T0-style self-test, own engine, from scratch ----
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        log.append(s)

    P("=== adv_engine.py selftest ===")

    # (0) pi_cycle_lengths correctness on a hand-built permutation
    pi_small = np.array([1, 2, 0, 4, 3])  # cycles (0,1,2) len3, (3,4) len2
    L = pi_cycle_lengths(pi_small)
    ok0 = np.array_equal(L, [3, 3, 3, 2, 2])
    P("(0) pi_cycle_lengths hand-check:", "OK" if ok0 else f"FAIL got {L}")
    assert ok0

    ss = np.random.SeedSequence(20260826000)
    rng = np.random.default_rng(ss)

    # (a) rho_measured vs 1-(1-c/n)^b
    cells = [(50, 400, 65536), (100, 400, 65536), (100, 600, 65536),
             (200, 150, 65536), (400, 100, 65536), (100, 1000, 65536),
             (8, 40, 8192), (800, 100, 65536)]
    max_z = 0.0
    n_rho_inst = 30
    for (b, c, n) in cells:
        rho_th = 1 - (1 - c / n) ** b
        vals = []
        for _ in range(n_rho_inst):
            inst = build_instance(n, b, c, rng)
            vals.append(inst["R"].mean())
        vals = np.array(vals)
        mean = vals.mean()
        sem = vals.std(ddof=1) / np.sqrt(n_rho_inst)
        z = (mean - rho_th) / sem if sem > 0 else 0.0
        max_z = max(max_z, abs(z))
        P(f"  (a) b={b},c={c},n={n}: rho_th={rho_th:.6f} rho_meas={mean:.6f} "
          f"z={z:+.2f}")
    P(f"(a) max|z| over {len(cells)} cells, {n_rho_inst} inst/cell:", f"{max_z:.3f}",
      "OK" if max_z < 4.0 else "FAIL")

    # (b) R^c subset of U_rem: U_rem = [n] \ {pi^j(s): s in seeds, 1<=j<=b-1}
    n_b_viol = 0
    n_b_inst = 40
    b0, c0, n0 = 100, 400, 65536
    for _ in range(n_b_inst):
        inst = build_instance(n0, b0, c0, rng)
        pi, seeds, R = inst["pi"], inst["seeds"], inst["R"]
        U_rem = np.ones(n0, dtype=bool)
        cur = np.nonzero(seeds)[0]
        for _ in range(b0 - 1):
            cur = pi[cur]
            U_rem[cur] = False
        viol = np.sum((~R) & (~U_rem))
        n_b_viol += viol
    P(f"(b) R^c subseteq U_rem: {n_b_inst} instances, violations = {n_b_viol}",
      "OK" if n_b_viol == 0 else "FAIL")

    # (c)/(d) short-cycle mechanism deterministic check (own from-scratch,
    # independent of adv_mechanism.py's larger-scale version)
    n_c_pts = 0
    n_c_viol = 0
    n_d_cyc = 0
    n_d_viol = 0
    for _ in range(60):
        b1, c1, n1 = 40, 300, 4096
        inst = build_instance(n1, b1, c1, rng)
        pi, seeds, R, L = inst["pi"], inst["seeds"], inst["R"], inst["cyc_len_pi"]
        short = L <= b1
        # group by cycle: find representative cycles among short points
        idx_short = np.nonzero(short)[0]
        visited_cyc = set()
        for x in idx_short:
            # find the cycle's node set by walking pi (cheap: L[x] <= b1 <= 40)
            key = None
            cyc_nodes = []
            cur = x
            for _ in range(int(L[x])):
                cyc_nodes.append(cur)
                cur = pi[cur]
            root = min(cyc_nodes)
            if root in visited_cyc:
                continue
            visited_cyc.add(root)
            has_seed = seeds[cyc_nodes].any()
            n_c_pts += len(cyc_nodes)
            if not has_seed:
                # (c): untouched short cycle => every point NOT in R
                if R[cyc_nodes].any():
                    n_c_viol += 1
            else:
                # (d): touched short cycle => every point IS in R
                n_d_cyc += 1
                if not R[cyc_nodes].all():
                    n_d_viol += 1
    P(f"(c) untouched short cycle => 0 points in R: {n_c_pts} short-cycle points, "
      f"violations={n_c_viol}", "OK" if n_c_viol == 0 else "FAIL")
    P(f"(d) touched short cycle => ALL points in R: {n_d_cyc} touched short cycles, "
      f"violations={n_d_viol}", "OK" if n_d_viol == 0 else "FAIL")

    # (e) cyclic_mask_peeling vs brute-force on small random functional graphs
    n_e_mismatch = 0
    for _ in range(200):
        nn = rng.integers(5, 40)
        f_small = rng.integers(0, nn, size=nn)
        cp = cyclic_mask_peeling(f_small)
        cb = cyclic_mask_bruteforce(f_small)
        if not np.array_equal(cp, cb):
            n_e_mismatch += 1
    P(f"(e) cyclic_mask_peeling vs brute-force: 200 random small graphs, "
      f"mismatches={n_e_mismatch}", "OK" if n_e_mismatch == 0 else "FAIL")

    all_ok = (max_z < 4.0) and (n_b_viol == 0) and (n_c_viol == 0) and \
        (n_d_viol == 0) and (n_e_mismatch == 0)
    P("ALL SELFTESTS PASSED" if all_ok else "SOME SELFTESTS FAILED")

    with open("adv_engine_selftest.log", "w") as fh:
        fh.write("\n".join(log) + "\n")
