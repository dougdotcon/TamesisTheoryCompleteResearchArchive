#!/usr/bin/env python3
"""
Independent (from-scratch) exact brute-force enumeration for the K2-OPEN-LEMMA
adversarial verification. Written WITHOUT looking at the front's
psi_bruteforce.py / psi_k2_case_formula.py / derive_closed_forms.py /
psi_k3_exploration.py scripts.

Definition used (matches THEOREM.md Definition 1 / Definition 4, and
ATTEMPT.md's ψ_n^{(K)}, ψ_n^{(K),R}, φ_n^{(K)}):

  Fix n, fix K in {1,2,3}. Sources = {0,...,K-1} (0-indexed labeled points).
  π ranges over ALL n! permutations of {0,...,n-1} (uniform).
  (U_0,...,U_{K-1}) ranges over ALL n^K target tuples (uniform, independent
  of π and of each other).
  f(i) = U_i for i < K,  f(i) = π(i) for i >= K.

  A point r is CYCLIC under f iff iterating r -> f(r) -> f(f(r)) -> ...
  returns to r before repeating any other point first (equivalently: r lies
  on a directed cycle of f's functional digraph).

  psi_n_K       := P(point K is cyclic)         [generic point, index K, the
                                                   first point NOT a source]
  psi_n_K_R     := P(point 0 is cyclic)          [a rerouted source point]
  phi_n_K       := E[#cyclic points]/n           [average over ALL n points]

All computed with EXACT rational arithmetic (fractions.Fraction), by
counting integer hit totals over the n! * n^K enumeration and dividing once
at the end (avoids Fraction overhead in the inner loop for speed).

Cyclic-point detection for a full permutation-with-K-reroutes functional
digraph f, computed for ALL n points at once in O(n) per (pi,U) instance
using the standard functional-graph coloring algorithm:
  color[i] = 0 (unvisited), 1 (on current walk, not yet resolved), 2 (done)
  cyclic[i] = True/False once resolved.
Walk forward from each unvisited i; if we hit a point with color==1 that is
on the CURRENT walk, everything from that point to the end of the walk is
on a cycle (cyclic=True), everything walked before that point is not
(cyclic=False, feeds into the cycle without being on it); if we hit a point
with color==2, we inherit its cyclic status only if that status directly
propagates forward is False -- but functional graphs: if we hit an already
completed node, none of the CURRENT walk is cyclic (the current walk merges
into a non-repeating tail or an already-classified cycle without itself
looping back), except each node's cyclic flag was already correctly set in
the earlier pass, so nothing more to do; the current partial walk's points
are simply all non-cyclic (they will never return to themselves).
"""
import sys
import time
from fractions import Fraction
from itertools import permutations, product


def cyclic_flags(f, n):
    """Return a list of booleans: cyclic_flags[i] = True iff i is cyclic
    under f (f is a list of length n, f[i] in range(n))."""
    color = [0] * n  # 0 unvisited, 1 in-progress, 2 done
    cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            # cur is on the current path -> found a fresh cycle starting at cur
            idx = path.index(cur)
            for j in range(idx, len(path)):
                cyclic[path[j]] = True
            for j in range(0, idx):
                cyclic[path[j]] = False
        # else color[cur]==2: nothing on this path is cyclic (already-known
        # target is not part of a NEW cycle discovered here); cyclic[.]
        # for path entries stays False (default), which is correct.
        for p in path:
            color[p] = 2
    return cyclic


def run(n, K, verbose=True):
    assert n > K >= 1
    total_instances = 0
    hit_generic = 0   # point K cyclic
    hit_rerouted = 0  # point 0 cyclic
    hit_total = 0     # sum over all n points, all instances

    perms = permutations(range(n))
    targets_range = list(range(n))

    t0 = time.time()
    for pi in perms:
        pi = list(pi)
        for Uvec in product(targets_range, repeat=K):
            f = [0] * n
            for i in range(K):
                f[i] = Uvec[i]
            for i in range(K, n):
                f[i] = pi[i]
            cyc = cyclic_flags(f, n)
            total_instances += 1
            if cyc[K]:
                hit_generic += 1
            if cyc[0]:
                hit_rerouted += 1
            hit_total += sum(cyc)
    elapsed = time.time() - t0

    psi = Fraction(hit_generic, total_instances)
    psi_R = Fraction(hit_rerouted, total_instances)
    phi = Fraction(hit_total, n * total_instances)

    if verbose:
        print(f"n={n} K={K}  instances={total_instances}  elapsed={elapsed:.2f}s")
        print(f"  psi_n^({K})   = {psi}  = {float(psi):.10f}")
        print(f"  psi_n^({K}),R = {psi_R}  = {float(psi_R):.10f}")
        print(f"  phi_n^({K})   = {phi}  = {float(phi):.10f}")
        # Lemma A check: phi = (K/n) psi_R + (1-K/n) psi , EXACT
        lemA = Fraction(K, n) * psi_R + Fraction(n - K, n) * psi
        ok = (lemA == phi)
        print(f"  LemmaA predicts phi = {lemA}  ==  computed phi ? {ok}")
        sys.stdout.flush()
    return psi, psi_R, phi, total_instances, elapsed


if __name__ == "__main__":
    K = int(sys.argv[1])
    n_lo = int(sys.argv[2])
    n_hi = int(sys.argv[3])
    results = {}
    for n in range(n_lo, n_hi + 1):
        psi, psi_R, phi, tot, elapsed = run(n, K)
        results[n] = {
            "psi": str(psi), "psi_R": str(psi_R), "phi": str(phi),
            "instances": tot, "elapsed_sec": elapsed,
        }
    import json
    outname = f"ref_bruteforce_K{K}_n{n_lo}-{n_hi}.json"
    with open(outname, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Wrote {outname}")
