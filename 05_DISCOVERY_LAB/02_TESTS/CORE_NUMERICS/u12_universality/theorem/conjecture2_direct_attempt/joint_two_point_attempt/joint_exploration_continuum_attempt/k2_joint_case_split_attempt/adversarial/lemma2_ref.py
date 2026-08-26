"""
Independent, from-scratch verification of the target document's "Two-Source
Redirect-Structure Lemma" (Lemma 2, its (R1)-(R5) formulas), derived and
checked WITHOUT reading the document's own case-by-case proof narrative in
detail (worked from the bare statement of what p,q,e_i,d_i mean, per the
adversarial mandate's anchoring-avoidance instruction). We build two EXPLICIT
permutation topologies for given arc lengths (p,q) and outside count O:

  Topology "same": a single pi-cycle containing both reroute sources 0,1,
     arranged as  0 -> e_1 -> e_2 -> ... -> e_{p-1} -> e_p(=1)
                    -> d_1 -> d_2 -> ... -> d_{q-1} -> d_q(=0)
     (so arc_1 = (e_1,...,e_p=1), length p; arc_2 = (d_1,...,d_q=0), length q),
     plus O further points forming their own separate fixed points (each its
     own 1-cycle) -- their internal pi-structure never matters here (Sec 3.1
     of the target doc already notes "outside" points are automatically
     cyclic for f regardless of U0,U1, so any fixed pi-structure works for
     this check; we use fixed points for simplicity).

  Topology "diff": TWO separate pi-cycles, one of length p containing source
     0 (0 -> e_1 -> ... -> e_{p-1} -> 0), one of length q containing source 1
     (1 -> d_1 -> ... -> d_{q-1} -> 1), plus O outside fixed points.
     [This corresponds to sigma(0)=0, sigma(1)=1 in Lemma 1's contracted
     permutation, i.e. the two sources on DIFFERENT background cycles.]

For each topology and each (U_0, U_1) in [n]^2 (full enumeration, no
randomness), we build f (source 0 -> U_0, source 1 -> U_1, else pi) and use
our own cycle_utils.cyclic_points to determine, for EVERY arc-interior point
e_i (1<=i<=p-1) and d_i (1<=i<=q-1), whether it is cyclic. We then check the
document's claimed closed forms:

  (R1) P(e_i cyclic) = i(n+q)/n^2
  (R2) P(d_i cyclic) = i(n+p)/n^2
  (R3) P(e_i, e_i' both cyclic) = min(i,i')*(n+q)/n^2  [monotone containment]
  (R4) symmetric for two d's
  (R5) P(e_i, d_i' both cyclic) = 2*i*i'/n^2

against DIRECT exact counts, for BOTH topologies (the document claims the
formulas hold "regardless of whether 0,1 share a cycle" -- we test this
claim explicitly, which the document's own unit test description does not
appear to isolate by topology in the same direct way).
"""
import sys
import os
import itertools
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cycle_utils import cyclic_points


def build_pi_same(n, p, q, O):
    """Single cycle 0,e_1..e_{p-1},1,d_1..d_{q-1}(len q incl endpoint 0),
    then O outside fixed points. Returns pi as list, plus arc index lists."""
    assert p >= 1 and q >= 1 and p + q + O == n
    pi = [0] * n
    labels = list(range(2, n))  # labels available for fillers/outside, since 0,1 reserved
    idx = 0
    e_points = []  # e_1..e_{p-1} (interior), e_p = 1
    for _ in range(p - 1):
        e_points.append(labels[idx]); idx += 1
    d_points = []
    for _ in range(q - 1):
        d_points.append(labels[idx]); idx += 1
    outside_points = []
    for _ in range(O):
        outside_points.append(labels[idx]); idx += 1
    assert idx == n - 2

    chain = [0] + e_points + [1] + d_points + [0]  # cyclic chain closing back to 0
    for a, b in zip(chain[:-1], chain[1:]):
        pi[a] = b
    for o in outside_points:
        pi[o] = o
    e_full = e_points + [1]     # e_1..e_p (e_p=1)
    d_full = d_points + [0]     # d_1..d_q (d_q=0)
    return pi, e_full, d_full, outside_points


def build_pi_diff(n, p, q, O):
    """Two separate cycles: 0's own cycle length p (0,e_1..e_{p-1},back to 0);
    1's own cycle length q (1,d_1..d_{q-1}, back to 1); O outside fixed pts."""
    assert p >= 1 and q >= 1 and p + q + O == n
    pi = [0] * n
    labels = list(range(2, n))
    idx = 0
    e_points = []
    for _ in range(p - 1):
        e_points.append(labels[idx]); idx += 1
    d_points = []
    for _ in range(q - 1):
        d_points.append(labels[idx]); idx += 1
    outside_points = []
    for _ in range(O):
        outside_points.append(labels[idx]); idx += 1
    assert idx == n - 2

    chain0 = [0] + e_points + [0]
    for a, b in zip(chain0[:-1], chain0[1:]):
        pi[a] = b
    chain1 = [1] + d_points + [1]
    for a, b in zip(chain1[:-1], chain1[1:]):
        pi[a] = b
    for o in outside_points:
        pi[o] = o
    e_full = e_points + [1]  # NOTE: e_p is conventionally "1" per doc's naming
    # but in the "diff" topology 1 is not on 0's arc at all. We keep e_full as
    # just the interior e_i points for testing purposes (we never need e_p
    # itself, only interior points e_1..e_{p-1}), likewise for d_full.
    return pi, e_points, d_points, outside_points


def check_cell(n, p, q, O, topology, verbose=True):
    if topology == "same":
        pi, e_full, d_full, outside = build_pi_same(n, p, q, O)
        e_interior = e_full[:-1]  # e_1..e_{p-1} (drop e_p=1)
        d_interior = d_full[:-1]  # d_1..d_{q-1} (drop d_q=0)
    else:
        pi, e_interior, d_interior, outside = build_pi_diff(n, p, q, O)

    # counts[point] = number of (U0,U1) making it cyclic
    from collections import defaultdict
    cyclic_count = defaultdict(int)
    both_ee = defaultdict(int)  # (i,i') interior e pairs (1-indexed) -> count both cyclic
    both_dd = defaultdict(int)
    both_ed = defaultdict(int)
    total = n * n

    for u0 in range(n):
        for u1 in range(n):
            f = list(pi)
            f[0] = u0
            f[1] = u1
            cyc = cyclic_points(f)
            for point in cyc:
                cyclic_count[point] += 1
            e_cyc = [1 if pt in cyc else 0 for pt in e_interior]
            d_cyc = [1 if pt in cyc else 0 for pt in d_interior]
            for i in range(len(e_interior)):
                for ip in range(len(e_interior)):
                    if i != ip and e_cyc[i] and e_cyc[ip]:
                        both_ee[(i + 1, ip + 1)] += 1
            for i in range(len(d_interior)):
                for ip in range(len(d_interior)):
                    if i != ip and d_cyc[i] and d_cyc[ip]:
                        both_dd[(i + 1, ip + 1)] += 1
            for i in range(len(e_interior)):
                for ip in range(len(d_interior)):
                    if e_cyc[i] and d_cyc[ip]:
                        both_ed[(i + 1, ip + 1)] += 1

    mismatches = []

    # R1: P(e_i cyclic) = i*(n+q)/n^2
    for i, pt in enumerate(e_interior, start=1):
        observed = Fraction(cyclic_count[pt], total)
        predicted = Fraction(i * (n + q), n * n)
        if observed != predicted:
            mismatches.append(("R1", i, observed, predicted))

    # R2: P(d_i cyclic) = i*(n+p)/n^2
    for i, pt in enumerate(d_interior, start=1):
        observed = Fraction(cyclic_count[pt], total)
        predicted = Fraction(i * (n + p), n * n)
        if observed != predicted:
            mismatches.append(("R2", i, observed, predicted))

    # R3: P(e_i,e_i' both) = min(i,i')*(n+q)/n^2
    for (i, ip), cnt in both_ee.items():
        observed = Fraction(cnt, total)
        predicted = Fraction(min(i, ip) * (n + q), n * n)
        if observed != predicted:
            mismatches.append(("R3", (i, ip), observed, predicted))

    # R4: symmetric
    for (i, ip), cnt in both_dd.items():
        observed = Fraction(cnt, total)
        predicted = Fraction(min(i, ip) * (n + p), n * n)
        if observed != predicted:
            mismatches.append(("R4", (i, ip), observed, predicted))

    # R5: P(e_i,d_i' both) = 2*i*i'/n^2
    for (i, ip), cnt in both_ed.items():
        observed = Fraction(cnt, total)
        predicted = Fraction(2 * i * ip, n * n)
        if observed != predicted:
            mismatches.append(("R5", (i, ip), observed, predicted))

    ok = len(mismatches) == 0
    if verbose:
        print(f"n={n} p={p} q={q} O={O} topology={topology}: "
              f"{'PASS' if ok else 'FAIL'} "
              f"(checked R1:{len(e_interior)} R2:{len(d_interior)} "
              f"R3:{len(both_ee)} R4:{len(both_dd)} R5:{len(both_ed)})")
        if not ok:
            for m in mismatches[:10]:
                print("   MISMATCH:", m)
    return ok, mismatches


if __name__ == "__main__":
    configs = []
    # A spread of (n,p,q,O) with p,q>=1 (need p>=2 or q>=2 to have interior
    # points to test R1/R2/R3/R4; R5 needs both p,q>=2 for interior pairs).
    for n in [6, 7, 8, 9]:
        for p in range(1, n):
            for q in range(1, n - p + 1):
                O = n - p - q
                if O < 0:
                    continue
                configs.append((n, p, q, O))

    total_checks = 0
    total_pass = 0
    fail_list = []
    for (n, p, q, O) in configs:
        for topo in ("same", "diff"):
            ok, mism = check_cell(n, p, q, O, topo, verbose=False)
            total_checks += 1
            if ok:
                total_pass += 1
            else:
                fail_list.append((n, p, q, O, topo, mism))

    print(f"Lemma 2 (R1)-(R5) independent check: {total_pass}/{total_checks} (n,p,q,O,topology) cells fully PASS")
    if fail_list:
        print(f"FAILURES: {len(fail_list)}")
        for f in fail_list[:20]:
            print("  ", f[:5], "first mismatch:", f[5][0] if f[5] else None)
    else:
        print("0 mismatches across every sub-formula, every configuration, BOTH topologies.")
