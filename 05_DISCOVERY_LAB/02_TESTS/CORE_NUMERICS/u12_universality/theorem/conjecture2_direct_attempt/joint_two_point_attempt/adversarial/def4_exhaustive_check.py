#!/usr/bin/env python3
"""
REFEREE, FRESH FROM SCRATCH. Independent exhaustive verification of

  - Theorem J (Uniform Cyclic Restriction Theorem): under Definition 4
    (THEOREM.md), conditional on {C(f)=c} for any realized cyclic set c
    with |c|=m>=2, f restricted to c is EXACTLY uniform over Sym(c).
  - Corollary: P(i,j both cyclic, same cycle) = P(i,j both cyclic,
    different cycle) = (1/2) P(i,j both cyclic), exactly, for a fixed
    pair (0,1).

built ENTIRELY from the prose of Definition 4 and re-derived from
scratch. No script from this front's directory (finite_n_exact_enum.py,
uniform_cyclic_restriction_exact.py, symbolic_checks.py) was opened,
read, or imported to write this file.

MODEL (Definition 4, THEOREM.md Sec 7.2 / ATTEMPT.md Sec 1):
  Fix n>=2, 0<=K<=n. pi ~ Uniform(Sym(n)). R ~ Uniform(K-subset of [n]),
  independent of pi. For i in R, U_i iid Uniform([n]), independent of
  (pi,R). f(i) := U_i if i in R, else pi(i).

  A point i is *cyclic* iff its forward f-orbit returns to i (i.e. i
  lies on a directed cycle of f's functional digraph). C(f) is the set
  of cyclic points; f restricted to C(f) is a bijection C(f)->C(f).

EXACT ENUMERATION STRATEGY (efficiency device, not a shortcut on
correctness): the uniform measure over (pi, R, U) with pi ~ Uniform(Sym(n))
is EXACTLY equivalent, for the purposes of computing f, to:
  - R ranges uniformly over all C(n,K) K-subsets;
  - D := [n] \ R (size n-K). Only pi restricted to domain D matters for
    f (f(i)=pi(i) for i in D; pi's values on R are discarded since those
    domain points use U_i instead). As pi ranges uniformly over Sym(n),
    the restriction pi|_D ranges uniformly over all INJECTIONS D -> [n]
    (an elementary, well known fact: for a uniform random permutation of
    [n], the restriction of its value-assignment to any fixed domain
    subset D, as pi ranges over Sym(n), hits every injection D->[n]
    with EXACTLY EQUAL multiplicity K! = (n - |D|)!, since each
    injection extends to a permutation of [n] in exactly K! ways, by
    completing the bijection between the unused K domain slots R and
    the unused K codomain values via any bijection between them).
  - U ranges uniformly over [n]^K (independent).
This reduces the enumeration from n! full permutations (of which only
the restriction to D matters) to n!/K! injections D->[n], each carried
with an explicit integer weight K! -- an EXACT reweighting, not an
approximation, that is verified for correctness by an internal
consistency check (Sec "SANITY CHECK" below: total weighted count must
equal n! * C(n,K) * n^K exactly) before any conclusion is drawn from it.

All arithmetic is with Python's arbitrary-precision integers; exact
Fraction is used only for the final printed ratios. No floating point
anywhere in the counting. Deterministic exhaustive enumeration -- no
randomness, no seed needed anywhere in this script.
"""
import itertools
import math
import sys
import time
from fractions import Fraction
from collections import Counter


def cyclic_points_and_cycle_ids(f, n):
    """f: tuple of length n, f[i] in range(n) (a possibly-non-injective
    functional-graph mapping [n]->[n]).
    Returns (cyclic: list[bool] length n, cid: dict i->cycle-id for
    cyclic i only). Fresh, elementary path-marking algorithm: for each
    unvisited start, walk forward recording the path; if we return to a
    node already on the CURRENT path, everything from that node onward
    in the path is a genuine cycle; otherwise (we hit an already-fully-
    resolved node from a previous walk) nothing new is cyclic on this
    path. O(n) total work across all starts.
    """
    UNVISITED, ON_PATH, DONE = 0, 1, 2
    state = [UNVISITED] * n
    cyclic = [False] * n
    cid = {}
    next_cid = 0
    for start in range(n):
        if state[start] != UNVISITED:
            continue
        path = []
        pos_in_path = {}
        v = start
        while state[v] == UNVISITED:
            state[v] = ON_PATH
            pos_in_path[v] = len(path)
            path.append(v)
            v = f[v]
        if state[v] == ON_PATH:
            # v is on the current path -> path[pos_in_path[v]:] is a cycle
            idx = pos_in_path[v]
            this_cid = next_cid
            next_cid += 1
            for u in path[idx:]:
                cyclic[u] = True
                cid[u] = this_cid
        # mark entire path DONE (whether or not it produced a cycle)
        for u in path:
            state[u] = DONE
    return cyclic, cid


def run_cell(n, K, do_restriction_check=True, pair=(0, 1), verbose=True):
    """Exhaustively enumerate Definition 4's model at fixed (n,K).
    Returns a dict of results, and prints a summary line."""
    assert 0 <= K <= n
    t0 = time.time()
    D = [i for i in range(n) if True]  # placeholder, recomputed per R below
    Kfact = math.factorial(K)

    total_weight = 0                    # sanity: must equal n! * C(n,K) * n^K
    # Pair-check counters (cheap, always computed)
    i0, j0 = pair
    both_w = 0
    same_w = 0
    diff_w = 0

    # Restriction-uniformity tally: key = (c as sorted tuple, rho as tuple
    # of images in that sorted order) -> weighted count
    tally = Counter() if do_restriction_check else None

    n_R = 0
    for R in itertools.combinations(range(n), K):
        n_R += 1
        Rset = set(R)
        Dsorted = [x for x in range(n) if x not in Rset]
        nD = len(Dsorted)
        # all injections Dsorted -> [n], represented as tuples of images
        # in the order of Dsorted (itertools.permutations(range(n), nD)
        # gives exactly this: all ordered nD-tuples of distinct values
        # from range(n))
        for sigma in itertools.permutations(range(n), nD):
            # sigma[k] = image of Dsorted[k] under this injection
            for U in itertools.product(range(n), repeat=K):
                # build f
                f = [0] * n
                for k, dpt in enumerate(Dsorted):
                    f[dpt] = sigma[k]
                for k, rpt in enumerate(R):
                    f[rpt] = U[k]
                f = tuple(f)

                w = Kfact
                total_weight += w

                cyclic, cid = cyclic_points_and_cycle_ids(f, n)

                # --- pair check ---
                if cyclic[i0] and cyclic[j0]:
                    both_w += w
                    if cid[i0] == cid[j0]:
                        same_w += w
                    else:
                        diff_w += w

                # --- restriction-uniformity check ---
                if do_restriction_check:
                    c = tuple(i for i in range(n) if cyclic[i])
                    if len(c) >= 2:
                        rho = tuple(f[i] for i in c)
                        tally[(c, rho)] += w

    elapsed = time.time() - t0

    # sanity check on total weight
    expected_total = math.factorial(n) * math.comb(n, K) * (n ** K)
    weight_ok = (total_weight == expected_total)

    result = {
        "n": n, "K": K,
        "elapsed_s": elapsed,
        "total_weight": total_weight,
        "expected_total": expected_total,
        "weight_ok": weight_ok,
        "both_w": both_w, "same_w": same_w, "diff_w": diff_w,
    }

    if both_w > 0:
        p_both = Fraction(both_w, total_weight)
        p_same = Fraction(same_w, total_weight)
        p_diff = Fraction(diff_w, total_weight)
        corollary_ok = (same_w == diff_w) and (2 * same_w == both_w)
        result.update(p_both=p_both, p_same=p_same, p_diff=p_diff,
                      corollary_ok=corollary_ok)
    else:
        result.update(p_both=Fraction(0), p_same=Fraction(0),
                      p_diff=Fraction(0), corollary_ok=True)  # vacuous

    if do_restriction_check:
        # group tally by c, verify: (a) exactly factorial(len(c)) distinct
        # rho observed, (b) all with EXACTLY equal weighted count
        by_c = {}
        for (c, rho), w in tally.items():
            by_c.setdefault(c, {})[rho] = w
        thm_violations = []
        n_c_checked = 0
        for c, rho_counts in by_c.items():
            m = len(c)
            expected_perms = math.factorial(m)
            n_c_checked += 1
            observed = len(rho_counts)
            counts = set(rho_counts.values())
            if observed != expected_perms:
                thm_violations.append(
                    f"c={c}: observed {observed} distinct restrictions, "
                    f"expected {expected_perms} (=|Sym(c)|)")
            elif len(counts) != 1:
                thm_violations.append(
                    f"c={c}: restrictions NOT all equal count: {sorted(rho_counts.items())}")
        result["n_c_checked"] = n_c_checked
        result["thm_violations"] = thm_violations
        result["thm_ok"] = (len(thm_violations) == 0)

    if verbose:
        line = (f"n={n:2d} K={K:2d} | weight_ok={weight_ok} | "
                f"P_both={result['p_both']} P_same={result['p_same']} "
                f"P_diff={result['p_diff']} | corollary_ok={result['corollary_ok']}")
        if do_restriction_check:
            line += f" | thm_ok={result['thm_ok']} (c's checked: {result['n_c_checked']})"
        line += f" | {elapsed:.1f}s"
        print(line)
        sys.stdout.flush()
        if do_restriction_check and result["thm_violations"]:
            for v in result["thm_violations"][:20]:
                print("    VIOLATION:", v)

    return result


def main():
    cells = []
    # K=0: entirely new coverage (front's Sec 4.1 table starts at K=1)
    for n in range(2, 9):
        cells.append((n, 0, True))
    # K=1: front tested n=3..7; extend by one to n=8
    for n in range(3, 9):
        cells.append((n, 1, True))
    # K=2: front tested n=3..7; reproduce in full (independent redo)
    for n in range(3, 8):
        cells.append((n, 2, True))
    # K=3: front tested n=3..6; extend to n=7
    for n in range(3, 8):
        cells.append((n, 3, True))
    # K=4: front tested n=4..6 (incl K=n=4); extend to n=7
    for n in range(4, 8):
        cells.append((n, 4, True))
    # K=5: front tested n=5..6 (incl K=n=5); extend to n=7
    for n in range(5, 8):
        cells.append((n, 5, True))
    # K=6: entirely new K value, incl K=n=6 boundary
    for n in range(6, 8):
        cells.append((n, 6, True))
    # K=7: new K=n=7 boundary
    cells.append((7, 7, True))

    print(f"Total cells to run: {len(cells)}")
    print("Format: n, K, weight sanity check, exact P_both/P_same/P_diff, "
          "corollary check, Theorem J restriction-uniformity check, runtime")
    print("-" * 100)
    sys.stdout.flush()

    all_results = []
    all_ok = True
    for (n, K, do_restr) in cells:
        r = run_cell(n, K, do_restriction_check=do_restr)
        all_results.append(r)
        if not r["weight_ok"] or not r["corollary_ok"]:
            all_ok = False
        if do_restr and not r.get("thm_ok", True):
            all_ok = False

    print("-" * 100)
    n_cells = len(all_results)
    n_thm_checked = sum(1 for r in all_results if "thm_ok" in r)
    n_thm_ok = sum(1 for r in all_results if r.get("thm_ok"))
    n_cor_ok = sum(1 for r in all_results if r["corollary_ok"])
    n_weight_ok = sum(1 for r in all_results if r["weight_ok"])
    print(f"Cells run: {n_cells}")
    print(f"Weight-sanity checks passed: {n_weight_ok}/{n_cells}")
    print(f"Corollary (same=diff=half) checks passed: {n_cor_ok}/{n_cells}")
    print(f"Theorem J restriction-uniformity checks passed: {n_thm_ok}/{n_thm_checked}")
    print()
    if all_ok:
        print("OVERALL RESULT: ZERO VIOLATIONS across all cells.")
    else:
        print("OVERALL RESULT: VIOLATIONS FOUND -- see above.")


if __name__ == "__main__":
    main()
