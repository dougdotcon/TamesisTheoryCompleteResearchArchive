"""
Fresh, from-scratch cycle-detection utilities for the u12 random-permutation-
with-reroutes ensemble (THEOREM.md Definition 1/4). Written independently by
the adversarial referee; NOT copied from, or derived by reading, any .py file
belonging to any front in this lineage (including the target front's own
scripts). Unit-tested below (run this file directly) before being imported by
any brute-force enumeration script.

Model (Definition 4, K reroutes fixed WLOG at {0,...,K-1}):
  f(i) = U_i        if i < K   (rerouted)
  f(i) = pi(i)       otherwise

A point i is "cyclic" for f iff iterating f from i returns to i in finitely
many steps (equivalently: i lies on a directed cycle of f's functional
digraph). Since f maps a finite set [n] to itself (not necessarily a
bijection when K>=1), we detect cyclicity by the classic "each node has
out-degree 1" functional-graph algorithm: follow the unique forward path
from i; it must eventually hit a repeated node (pigeonhole, since [n] is
finite); i is cyclic iff the first repeated node on i's own forward path is
i itself.
"""

def cyclic_points(f):
    """
    f: list of length n, f[i] in [0, n). Represents a functional digraph
    i -> f[i].
    Returns: a set of the points i in [0, n) that are cyclic for f.

    Implementation: standard color-based functional-graph traversal.
    WHITE = unvisited, GRAY = on current path (not yet resolved),
    BLACK = fully resolved (its cyclic/non-cyclic status is known).
    We walk from each unvisited node, marking the path GRAY; when we hit
    a node that is GRAY (i.e. on the current path), we've found a new
    cycle -- every node in the path from that node onward (i.e. the part
    of the path that is itself GRAY, from the repeat point to the current
    node) is cyclic. If we hit a BLACK node, the whole GRAY prefix is
    non-cyclic (it feeds into an already-resolved structure that this
    node is not part of a fresh cycle with).
    """
    n = len(f)
    color = [0] * n  # 0=white, 1=gray, 2=black
    is_cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        node = start
        while color[node] == 0:
            color[node] = 1
            path.append(node)
            node = f[node]
        if color[node] == 1:
            # node is on the current path -> found a new cycle starting at
            # the position of `node` in `path`.
            idx = path.index(node)
            for p in path[idx:]:
                is_cyclic[p] = True
        # mark entire path black now (resolved)
        for p in path:
            color[p] = 2
    return {i for i in range(n) if is_cyclic[i]}


# ---------------------------------------------------------------------------
# Unit tests: hand-built examples with known answers, run before any use.
# ---------------------------------------------------------------------------
def _run_unit_tests():
    results = []

    def check(name, f, expected):
        got = cyclic_points(f)
        ok = (got == set(expected))
        results.append((name, ok, got, set(expected)))
        return ok

    # 1. Identity permutation on 4 points: every point is its own fixed
    #    point / 1-cycle -> all cyclic.
    check("identity_4", [0, 1, 2, 3], {0, 1, 2, 3})

    # 2. A single 4-cycle: 0->1->2->3->0. All cyclic.
    check("single_4cycle", [1, 2, 3, 0], {0, 1, 2, 3})

    # 3. Two 2-cycles: 0<->1, 2<->3. All cyclic.
    check("two_2cycles", [1, 0, 3, 2], {0, 1, 2, 3})

    # 4. A permutation with a 3-cycle + fixed point: 0->1->2->0, 3->3.
    check("3cycle_plus_fixed", [1, 2, 0, 3], {0, 1, 2, 3})

    # 5. Non-permutation functional graph: a "rho" shape.
    #    0->1->2->1 (2,1 form a 2-cycle; 0 feeds in, not cyclic). 3->3 (fixed).
    check("rho_shape", [1, 2, 1, 3], {1, 2, 3})

    # 6. Longer tail into a cycle: 0->1->2->3->1 (cycle {1,2,3}; 0 feeds in).
    check("tail_into_cycle", [1, 2, 3, 1], {1, 2, 3})

    # 7. All points feed into a single fixed point (star): 0->2,1->2,2->2,3->2.
    check("star_into_fixed", [2, 2, 2, 2], {2})

    # 8. Two disjoint components, one a 2-cycle {0,1}, other a tail into a
    #    fixed point: 0->1->0, 2->3->3.
    check("two_components", [1, 0, 3, 3], {0, 1, 3})

    # 9. n=1 trivial: 0->0 (fixed point, cyclic).
    check("n1_fixed", [0], {0})

    # 10. A reroute example matching THEOREM.md Prop 4's own case split:
    #     n=5, pi = (0 1 2 3 4) i.e. pi(i)=i+1 mod 5 (single 5-cycle),
    #     reroute source i*=0, U=2 (so f(0)=2, f(i)=pi(i) for i=1..4).
    #     Trace: 0->2->3->4->0->2->... cycle {0,2,3,4}; point 1 (=pi(0),
    #     now unreachable from 0) still maps 1->2 under pi, f(1)=pi(1)=2
    #     since 1 is not the reroute source. So f = [2,2,3,4,0].
    #     Expected per Prop 4 Step 3 with U=c_d, d=2 (c_0=0,c_1=1,c_2=2,...):
    #     "d in {1,...,L-1}: L-d+1 points of C cyclic" -> L=5,d=2 -> 5-2+1=4
    #     points of C cyclic, out of L=5 -> point c_1=1 is the excluded one.
    check("prop4_style_reroute", [2, 2, 3, 4, 0], {0, 2, 3, 4})

    all_ok = all(ok for _, ok, _, _ in results)
    print(f"cycle_utils unit tests: {'ALL PASS' if all_ok else 'FAILURES FOUND'}")
    for name, ok, got, exp in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}: got={sorted(got)} expected={sorted(exp)}")
    return all_ok


if __name__ == "__main__":
    ok = _run_unit_tests()
    import sys
    sys.exit(0 if ok else 1)
