"""
sc_engine.py -- own M-CLUST(b) engine, written from scratch from the prose
mechanism in DERIVATION_PREREG.md (which is itself re-derived from
DERIVATIONS.md, DERIVATION_MCLUST_FIXED.md, and the two primary sources of
this front -- elevation_level_attempt/ATTEMPT.md and its referee report --
read only in prose form, no .py file of either read or imported).

Mechanism:
  n points, pi a uniform random permutation.
  Each point is an i.i.d. seed with probability p = c/n.
  For each seed s, the run/block is the full b-point forward orbit
    {s, pi(s), pi^2(s), ..., pi^{b-1}(s)}  (b points, seed included).
  R = union of all blocks.
  Every point of R (seed or interior, no distinction) gets an i.i.d.
    Uniform([n]) destination f(x), drawn once and fixed.
  Outside R, f = pi.
  phi = E[ (1/n) * #{x : x lies on a cycle of f} ].

Cycle detection: in-degree peeling (Kahn-style). A point survives peeling
iff it lies on a cycle of f -- standard, exact, O(n).

Cycle-length utility: the pi-cycle length through any point, needed to
condition on "is x0 on a short (<=b) cycle" -- computed once per instance
via straightforward orbit-following (pi is a permutation, so this is cheap:
total work across all points to label every pi-cycle is O(n)).
"""

import numpy as np
from collections import deque


def build_pi(n, rng):
    """Uniform random permutation of [0..n-1], as an array pi with pi[x] = image of x."""
    return rng.permutation(n)


def build_seeds(n, c, rng):
    p = c / n
    return rng.random(n) < p


def build_R_mask(n, b, pi, seed_mask):
    """R = union over seeds s of {s, pi(s), ..., pi^{b-1}(s)} -- b points, seed included."""
    R = seed_mask.copy()
    cur = np.where(seed_mask)[0]
    for _ in range(1, b):
        if cur.size == 0:
            break
        cur = pi[cur]
        R[cur] = True
    return R


def build_f(n, pi, R_mask, rng):
    """f(x) = pi(x) if x not in R; f(x) = i.i.d. Uniform([n]) if x in R."""
    f = pi.copy()
    n_R = int(R_mask.sum())
    if n_R > 0:
        f[R_mask] = rng.integers(0, n, size=n_R)
    return f


def cyclic_mask_peeling(f):
    """In-degree peeling (Kahn-style). Returns boolean mask: True iff x lies on
    a cycle of f. Exact, O(n)."""
    n = f.shape[0]
    indeg = np.bincount(f, minlength=n).astype(np.int64)
    active = np.ones(n, dtype=bool)
    q = deque(np.where(indeg == 0)[0].tolist())
    while q:
        x = q.popleft()
        if not active[x]:
            continue
        active[x] = False
        y = f[x]
        indeg[y] -= 1
        if indeg[y] == 0 and active[y]:
            q.append(y)
    return active


def pi_cycle_lengths(pi):
    """Returns an array cyc_len of shape (n,) with cyc_len[x] = length of the
    pi-cycle containing x. O(n), pi is a permutation (bijection) so every
    point lies on exactly one cycle."""
    n = pi.shape[0]
    cyc_len = np.zeros(n, dtype=np.int64)
    visited = np.zeros(n, dtype=bool)
    for start in range(n):
        if visited[start]:
            continue
        # walk the cycle from start
        members = []
        x = start
        while not visited[x]:
            visited[x] = True
            members.append(x)
            x = pi[x]
        L = len(members)
        cyc_len[np.array(members, dtype=np.int64)] = L
    return cyc_len


def build_instance(n, b, c, rng):
    """Full instance: returns dict with pi, seed_mask, R_mask, f, and (lazily)
    nothing else -- cycle lengths / cyclic mask computed on demand by callers
    to avoid paying for them when not needed."""
    pi = build_pi(n, rng)
    seed_mask = build_seeds(n, c, rng)
    R_mask = build_R_mask(n, b, pi, seed_mask)
    f = build_f(n, pi, R_mask, rng)
    return dict(pi=pi, seed_mask=seed_mask, R_mask=R_mask, f=f)


def cyclic_check_matches(f, pi, members):
    """Every member must satisfy f(x) == pi(x), and the resulting f-restricted
    map on members must equal a cyclic permutation (which it does automatically
    since f=pi there and members are exactly one pi-cycle)."""
    return bool(np.array_equal(f[members], pi[members]))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import time

    verbose = "-v" in sys.argv

    print("sc_engine.py selftest")
    fails = 0

    # --- (a) rho_measured vs 1-(1-c/n)^b, several cells --------------------
    cells = [
        (32768, 8, 40),
        (65536, 50, 400),
        (65536, 100, 400),
        (65536, 100, 600),
        (65536, 100, 1000),
        (65536, 200, 150),
        (65536, 400, 100),
        (65536, 400, 300),
    ]
    ss = np.random.SeedSequence(20260825900)
    children = ss.spawn(len(cells) * 30 + 1000)
    child_iter = iter(children)

    print("\n(a) rho_measured vs 1-(1-c/n)^b, 30 instances per cell")
    for (n, b, c) in cells:
        p = c / n
        rho_formula = 1 - (1 - p) ** b
        rho_vals = []
        for _ in range(30):
            rng = np.random.default_rng(next(child_iter))
            inst = build_instance(n, b, c, rng)
            rho_vals.append(inst["R_mask"].mean())
        rho_meas = np.mean(rho_vals)
        rho_sem = np.std(rho_vals, ddof=1) / np.sqrt(len(rho_vals))
        z = (rho_meas - rho_formula) / rho_sem if rho_sem > 0 else 0.0
        ok = abs(z) < 4.0
        if not ok:
            fails += 1
        print(f"  n={n:6d} b={b:4d} c={c:5d}  rho_formula={rho_formula:.5f}  "
              f"rho_meas={rho_meas:.5f}+-{rho_sem:.5f}  z={z:+.2f}  {'OK' if ok else 'FAIL'}")

    # --- (b) R^c subseteq U_rem: always ------------------------------------
    # U_rem = [n] \ {pi^j(s): s in seeds, 1<=j<=b-1}  (the b-1 forward images,
    # NOT including the seed itself at j=0). Check R^c (= [n]\R, with R the
    # full b-point block including the seed) is always a subset of U_rem.
    print("\n(b) R^c subseteq U_rem -- always (0 violations required)")
    viol_b = 0
    n_checked_b = 0
    for (n, b, c) in cells[:4]:
        for _ in range(10):
            rng = np.random.default_rng(next(child_iter))
            pi = build_pi(n, rng)
            seed_mask = build_seeds(n, c, rng)
            R_mask = build_R_mask(n, b, pi, seed_mask)
            # U_rem: complement of the b-1 forward-images set (j=1..b-1)
            images_mask = np.zeros(n, dtype=bool)
            cur = np.where(seed_mask)[0]
            for _ in range(1, b):
                if cur.size == 0:
                    break
                cur = pi[cur]
                images_mask[cur] = True
            U_rem_mask = ~images_mask
            Rc_mask = ~R_mask
            viol = np.count_nonzero(Rc_mask & ~U_rem_mask)
            viol_b += viol
            n_checked_b += 1
    ok_b = viol_b == 0
    if not ok_b:
        fails += 1
    print(f"  {n_checked_b} instances checked, violations={viol_b}  {'OK' if ok_b else 'FAIL'}")

    # --- (c) fully-untouched short (L<=b) cycle is exactly an f-cycle ------
    print("\n(c) untouched cycle length<=b is exactly a cycle of f (0 violations)")
    viol_c = 0
    n_short_checked = 0
    for (n, b, c) in [(32768, 8, 40), (65536, 50, 400), (65536, 100, 400)]:
        for _ in range(15):
            rng = np.random.default_rng(next(child_iter))
            inst = build_instance(n, b, c, rng)
            pi, seed_mask, R_mask, f = inst["pi"], inst["seed_mask"], inst["R_mask"], inst["f"]
            cyc_len = pi_cycle_lengths(pi)
            # short & untouched: cyc_len <= b and no point of R touches this cycle
            short_mask = cyc_len <= b
            # a cycle is untouched iff none of its members are in R; since
            # R_mask is defined per point, "untouched" for point x means: no
            # member of x's pi-cycle is in R. Compute per-cycle OR of R_mask.
            # (cheap: iterate only over short-cycle points, few of them)
            idx = np.where(short_mask)[0]
            n_short_checked += idx.size
            checked_cycles = set()
            for x in idx:
                L = cyc_len[x]
                if L not in checked_cycles or True:
                    pass
            # group short points by cycle via orbit walk (cheap, few points)
            done = np.zeros(n, dtype=bool)
            for x in idx:
                if done[x]:
                    continue
                members = []
                y = x
                while not done[y]:
                    done[y] = True
                    members.append(y)
                    y = pi[y]
                members = np.array(members)
                touched = R_mask[members].any()
                if not touched:
                    # every member must be an f-cycle point, and f restricted
                    # to members must equal pi restricted to members
                    if not cyclic_check_matches(f, pi, members):
                        viol_c += 1
    ok_c = viol_c == 0
    if not ok_c:
        fails += 1
    print(f"  {n_short_checked} short-cycle points examined, violations={viol_c}  "
          f"{'OK' if ok_c else 'FAIL'}")

    # --- (d) fully-touched short cycle has zero run starts ------------------
    print("\n(d) touched short (L<=b) cycle has zero run starts (0 violations)")
    viol_d = 0
    n_touched_checked = 0
    for (n, b, c) in [(65536, 100, 1000), (65536, 400, 300)]:
        for _ in range(15):
            rng = np.random.default_rng(next(child_iter))
            inst = build_instance(n, b, c, rng)
            pi, seed_mask, R_mask = inst["pi"], inst["seed_mask"], inst["R_mask"]
            cyc_len = pi_cycle_lengths(pi)
            short_mask = cyc_len <= b
            idx = np.where(short_mask)[0]
            done = np.zeros(n, dtype=bool)
            for x in idx:
                if done[x]:
                    continue
                members = []
                y = x
                while not done[y]:
                    done[y] = True
                    members.append(y)
                    y = pi[y]
                members = np.array(members)
                touched = R_mask[members].any()
                if touched:
                    n_touched_checked += 1
                    # run start = p in R with pi^{-1}(p) not in R.
                    # pi^{-1}(p) for p=members[i] is members[i-1] (cyclically)
                    predecessors = np.roll(members, 1)
                    run_starts = R_mask[members] & (~R_mask[predecessors])
                    if run_starts.any():
                        viol_d += 1
    ok_d = viol_d == 0
    if not ok_d:
        fails += 1
    print(f"  {n_touched_checked} touched short cycles examined, violations={viol_d}  "
          f"{'OK' if ok_d else 'FAIL'}")

    # --- (e) cyclic_mask_peeling sanity: brute-force cross-check on small n ---
    print("\n(e) cyclic_mask_peeling vs brute-force orbit-following, small n")
    viol_e = 0
    for trial in range(200):
        rng = np.random.default_rng(next(child_iter))
        nn = 60
        f_small = rng.integers(0, nn, size=nn)
        mask_peel = cyclic_mask_peeling(f_small)
        # brute force: x cyclic iff iterating f from x returns to x within nn steps
        mask_brute = np.zeros(nn, dtype=bool)
        for x in range(nn):
            y = x
            for _ in range(nn):
                y = f_small[y]
                if y == x:
                    mask_brute[x] = True
                    break
        if not np.array_equal(mask_peel, mask_brute):
            viol_e += 1
    ok_e = viol_e == 0
    if not ok_e:
        fails += 1
    print(f"  200 random small functional graphs, mismatches={viol_e}  {'OK' if ok_e else 'FAIL'}")

    # --- timing ---------------------------------------------------------
    print("\n(timing) one instance at n=65536, b=100, c=1000")
    rng = np.random.default_rng(np.random.SeedSequence(20260825900).spawn(1)[0])
    t0 = time.time()
    inst = build_instance(65536, 100, 1000, rng)
    t1 = time.time()
    mask = cyclic_mask_peeling(inst["f"])
    t2 = time.time()
    clens = pi_cycle_lengths(inst["pi"])
    t3 = time.time()
    print(f"  build_instance: {t1-t0:.4f}s   cyclic_mask_peeling: {t2-t1:.4f}s   "
          f"pi_cycle_lengths: {t3-t2:.4f}s   phi_this_instance={mask.mean():.5f}")

    print(f"\n{'ALL SELFTESTS PASSED' if fails == 0 else f'{fails} SELFTEST GROUPS FAILED'}")
    sys.exit(1 if fails else 0)
