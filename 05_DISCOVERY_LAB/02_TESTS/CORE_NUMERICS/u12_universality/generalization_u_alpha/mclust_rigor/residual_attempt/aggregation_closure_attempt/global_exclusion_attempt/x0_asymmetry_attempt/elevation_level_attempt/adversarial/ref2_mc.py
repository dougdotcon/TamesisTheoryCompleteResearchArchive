"""ref2_mc.py -- the adversarial referee's OWN M-CLUST(b) / M-U engine.

Written from scratch from the mechanism as stated in
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` section 1 and
`generalization_u_alpha/DERIVATIONS.md` sections 3.1/3.5.
Nothing imported or copied from any script of the target front
(`elev_*.py`), of `x0_asymmetry_attempt/`, of its `adversarial/` review,
or of any earlier front.

Mechanism (M-CLUST(b) at (c, n)):
  pi           uniform random permutation of [n]
  seed[x]      i.i.d. Bernoulli(c/n), independent of pi
  block(s)     {s, pi(s), ..., pi^(b-1)(s)}   for every seed s
  R            union of blocks
  f(x)         i.i.d. uniform on [n]   if x in R
               pi(x)                   if x not in R
  cyclic set   the set of x lying on a cycle of the functional graph f
  phi          E[|cyc|] / n

M-U at (C, N) is exactly M-CLUST(1) at (C, N).

Run `python3 ref2_mc.py selftest` for the built-in validation.
"""
import math
import sys

import numpy as np

# ---------------------------------------------------------------------------
# instance construction
# ---------------------------------------------------------------------------


def build_R(pi, seed_mask, b):
    """R = union over seeds s of {s, pi(s), ..., pi^(b-1)(s)}.

    Forward iteration along pi.  Handles overlapping blocks and blocks
    longer than their own pi-cycle correctly (repeated marking is idempotent).
    """
    n = pi.shape[0]
    R = np.zeros(n, dtype=bool)
    cur = np.flatnonzero(seed_mask)
    if cur.size == 0:
        return R
    R[cur] = True
    for _ in range(b - 1):
        cur = pi[cur]
        R[cur] = True
    return R


def build_R_backward(pi_inv, seed_mask, b):
    """Independent construction #2: z in R iff some pi^{-j}(z), 0<=j<=b-1, is a seed.

    Backward iteration, the literal reading of the membership definition.
    Used only in the self-test (it is the same cost but a different code path).
    """
    n = pi_inv.shape[0]
    R = seed_mask.copy()
    cur = np.arange(n)
    for _ in range(b - 1):
        cur = pi_inv[cur]
        R |= seed_mask[cur]
    return R


def build_instance(rng, n, b, c, want_pi_inv=False):
    """Returns (pi, seed_mask, R, f)."""
    pi = rng.permutation(n).astype(np.int64)
    seed_mask = rng.random(n) < (c / n)
    R = build_R(pi, seed_mask, b)
    f = pi.copy()
    nR = int(R.sum())
    if nR:
        f[R] = rng.integers(0, n, size=nR, dtype=np.int64)
    out = [pi, seed_mask, R, f]
    if want_pi_inv:
        pi_inv = np.empty(n, dtype=np.int64)
        pi_inv[pi] = np.arange(n)
        out.append(pi_inv)
    return tuple(out)


# ---------------------------------------------------------------------------
# exact cyclic set of a functional graph
# ---------------------------------------------------------------------------


def cyclic_set(f):
    """The set of points lying on a cycle of the functional graph of f.

    cyc = image(f^m) for any m >= n, because every forward orbit reaches its
    cycle in < n steps and f^m restricted to the cyclic set is a bijection.
    Computed by repeated squaring: g <- g o g, K = ceil(log2(n)) times.
    """
    n = f.shape[0]
    K = max(1, int(math.ceil(math.log2(max(n, 2)))))
    g = f
    for _ in range(K):
        g = g[g]
    cyc = np.zeros(n, dtype=bool)
    cyc[g] = True
    return cyc


def cyclic_set_peel(f):
    """Independent construction #2 of the cyclic set: in-degree peeling.

    Repeatedly delete nodes with in-degree 0; what survives is exactly the
    union of the cycles.  O(n) total work, different code path from the
    doubling method.  Used only in the self-test.
    """
    n = f.shape[0]
    alive = np.ones(n, dtype=bool)
    indeg = np.bincount(f, minlength=n)
    frontier = np.flatnonzero(indeg == 0)
    while frontier.size:
        alive[frontier] = False
        tgt = f[frontier]
        dec = np.bincount(tgt, minlength=n)
        indeg = indeg - dec
        cand = np.unique(tgt)
        cand = cand[alive[cand] & (indeg[cand] == 0)]
        frontier = cand
    return alive


def cyclic_set_bruteforce(f):
    """Independent construction #3: literal orbit following, per node."""
    n = f.shape[0]
    out = np.zeros(n, dtype=bool)
    for x in range(n):
        y = x
        for _ in range(n + 1):
            y = f[y]
            if y == x:
                out[x] = True
                break
    return out


# ---------------------------------------------------------------------------
# grid-level phi measurement (graph level, no walk)
# ---------------------------------------------------------------------------


def measure_cell(seed_seq, n, b, c, n_inst, chunk_report=None):
    """Per-instance sufficient statistics for phi, phi(.|x0 notin R), eps.

    Returns dict of per-instance arrays:
       n_cyc        |cyc|
       n_cyc_notR   |cyc \\ R|
       n_notR       |R^c|
       n_R          |R|
       n_cyc_R      |cyc & R|
    """
    rng = np.random.default_rng(seed_seq)
    a_cyc = np.empty(n_inst, dtype=np.int64)
    a_cyc_notR = np.empty(n_inst, dtype=np.int64)
    a_notR = np.empty(n_inst, dtype=np.int64)
    for i in range(n_inst):
        pi, sm, R, f = build_instance(rng, n, b, c)
        cyc = cyclic_set(f)
        a_cyc[i] = cyc.sum()
        notR = ~R
        a_cyc_notR[i] = np.count_nonzero(cyc & notR)
        a_notR[i] = np.count_nonzero(notR)
        if chunk_report and (i + 1) % chunk_report == 0:
            print("      ... %d/%d" % (i + 1, n_inst), flush=True)
    return {
        "n_cyc": a_cyc,
        "n_cyc_notR": a_cyc_notR,
        "n_notR": a_notR,
        "n_R": n - a_notR,
        "n_cyc_R": a_cyc - a_cyc_notR,
        "n": n, "b": b, "c": c, "n_inst": n_inst,
    }


def ratio_boot(num, den, rng, nboot=2000):
    """Cluster bootstrap over instances of the ratio of sums."""
    m = num.shape[0]
    point = num.sum() / den.sum()
    idx = rng.integers(0, m, size=(nboot, m))
    reps = num[idx].sum(axis=1) / den[idx].sum(axis=1)
    return point, float(reps.std(ddof=1))


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------


def selftest():
    print("ref2_mc.py selftest -- referee's own engine")
    rng = np.random.default_rng(np.random.SeedSequence(20260824901))

    # (1) cyclic set: three constructions agree on random maps
    bad = 0
    for trial in range(300):
        n = int(rng.integers(3, 60))
        f = rng.integers(0, n, size=n, dtype=np.int64)
        a = cyclic_set(f)
        bp = cyclic_set_peel(f)
        cbf = cyclic_set_bruteforce(f)
        if not (np.array_equal(a, bp) and np.array_equal(a, cbf)):
            bad += 1
    print("  (1) cyclic_set: doubling vs peeling vs brute force, "
          "300 random maps -> mismatches =", bad)

    # (2) R: forward vs backward construction
    bad = 0
    for trial in range(200):
        n = int(rng.integers(8, 400))
        b = int(rng.integers(1, 25))
        c = float(rng.uniform(0.0, 0.4)) * n
        pi = rng.permutation(n).astype(np.int64)
        sm = rng.random(n) < (c / n)
        pi_inv = np.empty(n, dtype=np.int64)
        pi_inv[pi] = np.arange(n)
        if not np.array_equal(build_R(pi, sm, b), build_R_backward(pi_inv, sm, b)):
            bad += 1
    print("  (2) build_R forward vs backward, 200 random instances -> "
          "mismatches =", bad)

    # (3) shadowing lemma: pi(R^c) meets R only at run starts
    # (4) R^c subset U_rem  and  |U_rem| = n(1-c/n)^(b-1) in expectation
    # (5) pi(x) in U_rem for every x in R^c  (the exposure claim, deterministic)
    n, b, c = 8192, 40, 60
    tot_pool, tot_n, viol_shadow, viol_urem, viol_img = 0, 0, 0, 0, 0
    tot_RU = 0
    for trial in range(40):
        pi, sm, R, f, pi_inv = build_instance(rng, n, b, c, want_pi_inv=True)
        # I = images revealed while exposing R: pi^j(s), 1<=j<=b-1
        I = np.zeros(n, dtype=bool)
        cur = np.flatnonzero(sm)
        for _ in range(b - 1):
            cur = pi[cur]
            I[cur] = True
        U = ~I
        tot_pool += int(U.sum())
        tot_n += n
        tot_RU += int((R & U).sum())
        notR = ~R
        # (5) images of R^c land in U_rem
        viol_img += int(np.count_nonzero(I[pi[notR]]))
        # (4) R^c subset of U_rem
        viol_urem += int(np.count_nonzero(I[notR]))
        # (3) shadowing: pi(x) in R  =>  pi(x) is a run start
        img = pi[notR]
        inR = img[R[img]]
        pred_in_R = R[pi_inv[inR]]
        viol_shadow += int(np.count_nonzero(pred_in_R))
    p = c / n
    print("  (3) shadowing violations (pi(R^c) meeting non-run-start R) =",
          viol_shadow)
    print("  (4) R^c \\subset U_rem violations =", viol_urem,
          "   (proves R^c subset U_rem, so a fresh arc start is ALWAYS in U_rem)")
    print("  (5) pi(R^c) \\subset U_rem violations =", viol_img)
    print("  (6) |U_rem|/n measured = %.8f   (1-c/n)^(b-1) = %.8f   "
          "rel.dev = %+.3e"
          % (tot_pool / tot_n, (1 - p) ** (b - 1),
             tot_pool / tot_n / (1 - p) ** (b - 1) - 1))
    print("  (7) |R cap U_rem|/n measured = %.8f   (c/n)(1-c/n)^(b-1) = %.8f"
          "   rel.dev = %+.3e"
          % (tot_RU / tot_n, p * (1 - p) ** (b - 1),
             tot_RU / tot_n / (p * (1 - p) ** (b - 1)) - 1))

    # (8) rho measured vs 1-(1-c/n)^b
    tot_R, tot_n = 0, 0
    for trial in range(40):
        pi, sm, R, f = build_instance(rng, n, b, c)
        tot_R += int(R.sum())
        tot_n += n
    print("  (8) rho measured = %.8f   1-(1-c/n)^b = %.8f   rel.dev = %+.3e"
          % (tot_R / tot_n, 1 - (1 - p) ** b,
             (tot_R / tot_n) / (1 - (1 - p) ** b) - 1))

    # (9) M-U (b=1) at small c against the known continuum limit is done
    #     in ref2_reduction.py; here just check b=1 => R == seed set
    pi, sm, R, f = build_instance(rng, 1000, 1, 30)
    print("  (9) b=1: R == seed set ->", bool(np.array_equal(R, sm)))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    else:
        print(__doc__)
