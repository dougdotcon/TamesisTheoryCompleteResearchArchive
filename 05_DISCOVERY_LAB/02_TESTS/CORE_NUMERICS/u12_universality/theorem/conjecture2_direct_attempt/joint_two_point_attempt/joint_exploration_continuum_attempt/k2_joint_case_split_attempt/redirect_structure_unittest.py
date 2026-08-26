"""
Unit test for the "two-source redirect structure" lemma derived from scratch
in ATTEMPT.md (this front, k2_joint_case_split_attempt).

Setup (matches the derivation): two disjoint "arcs" of lengths p, q are
built as explicit chains inside a universe of n points:
  arc1 = points labeled 0, 1, ..., p-1  (position i <-> label i-1, i=1..p)
    f(label i-1) = label i        for i = 1..p-2   (position i -> i+1)
    f(label p-1) = U1             (the tail, "arc1 position p" = source "1")
  arc2 = points labeled p, p+1, ..., p+q-1 (position i <-> label p+i-1)
    f(label p+i-1) = label p+i    for i = 1..q-2
    f(label p+q-1) = U0           (the tail, "arc2 position q" = source "0")
  outside = points labeled p+q, ..., n-1, each a fixed point f(x)=x.

U0, U1 range independently and uniformly over all n labels (0..n-1) -- this
is EXACTLY Definition 4's reroute-target law, decoupled here from the
background-permutation machinery so this script tests ONLY the redirect
combinatorics (the "9-case" analysis), not the permutation-position
distribution (that part is tested separately by the full brute-force
enumeration against Definition 4 itself, in brute_force_k2.py).

Claims tested (all with exact Fraction arithmetic over all n^2 (U0,U1)
pairs, i.e. no sampling):
  (R1) P(arc1 position i cyclic) = i*(n+q) / n^2            for i=1..p-1
  (R2) P(arc2 position i cyclic) = i*(n+p) / n^2            for i=1..q-1
  (R3) P(both arc1 positions i<i' cyclic) = min(i,i')*(n+q) / n^2
  (R4) P(both arc2 positions i<i' cyclic) = min(i,i')*(n+p) / n^2
  (R5) P(arc1 position i AND arc2 position i' both cyclic) = 2*i*i' / n^2
"""
from fractions import Fraction
import itertools

def build_and_check(n, p, q, verbose=False):
    assert p >= 1 and q >= 1 and p + q <= n
    outside_start = p + q

    def cyclic_set(u0, u1):
        # f as described
        def f(x):
            if x == p - 1:
                return u1
            if x == p + q - 1:
                return u0
            if x < p - 1:
                return x + 1
            if p <= x < p + q - 1:
                return x + 1
            return x  # outside, fixed point

        cyclic = set()
        # only need to test arc1/arc2 points (positions 1..p-1, 1..q-1);
        # tail points (p-1, p+q-1) and outside are not "query" positions.
        for start in list(range(0, p - 1)) + list(range(p, p + q - 1)):
            seen = []
            x = start
            visited = set()
            while x not in visited:
                visited.add(x)
                seen.append(x)
                x = f(x)
            # x is now the first repeated node; it's the entrance to the
            # eventual cycle. start is "cyclic" iff start == x (i.e. start
            # itself is on the cycle, not just feeding into it) -- more
            # precisely, start is cyclic iff start is reachable again from
            # itself, i.e. start is in the cycle {x, f(x), f(f(x)), ...}
            # until back to x. Standard test: walk again from x until back
            # to x, check if start is among those.
            cyc = []
            y = x
            while True:
                cyc.append(y)
                y = f(y)
                if y == x:
                    break
            if start in cyc:
                cyclic.add(start)
        return cyclic

    # position <-> label maps
    def arc1_label(i):  # i = 1..p-1
        return i - 1

    def arc2_label(i):  # i = 1..q-1
        return p + i - 1

    total = n * n
    cnt_e = {i: 0 for i in range(1, p)}
    cnt_d = {i: 0 for i in range(1, q)}
    cnt_ee = {}  # (i<i') both arc1
    cnt_dd = {}
    cnt_ed = {}  # (i in arc1, i' in arc2)

    for u0 in range(n):
        for u1 in range(n):
            cyc = cyclic_set(u0, u1)
            for i in range(1, p):
                if arc1_label(i) in cyc:
                    cnt_e[i] += 1
            for i in range(1, q):
                if arc2_label(i) in cyc:
                    cnt_d[i] += 1
            for i in range(1, p):
                for ip in range(i + 1, p):
                    key = (i, ip)
                    both = (arc1_label(i) in cyc) and (arc1_label(ip) in cyc)
                    cnt_ee[key] = cnt_ee.get(key, 0) + (1 if both else 0)
            for i in range(1, q):
                for ip in range(i + 1, q):
                    key = (i, ip)
                    both = (arc2_label(i) in cyc) and (arc2_label(ip) in cyc)
                    cnt_dd[key] = cnt_dd.get(key, 0) + (1 if both else 0)
            for i in range(1, p):
                for ip in range(1, q):
                    key = (i, ip)
                    both = (arc1_label(i) in cyc) and (arc2_label(ip) in cyc)
                    cnt_ed[key] = cnt_ed.get(key, 0) + (1 if both else 0)

    mismatches = []

    def check(name, got_count, predicted):
        got = Fraction(got_count, total)
        if got != predicted:
            mismatches.append((name, got, predicted))

    for i in range(1, p):
        pred = Fraction(i * (n + q), n * n)
        check(f"P(e_{i} cyclic)", cnt_e[i], pred)
    for i in range(1, q):
        pred = Fraction(i * (n + p), n * n)
        check(f"P(d_{i} cyclic)", cnt_d[i], pred)
    for (i, ip), c in cnt_ee.items():
        pred = Fraction(min(i, ip) * (n + q), n * n)
        check(f"P(e_{i},e_{ip} both)", c, pred)
    for (i, ip), c in cnt_dd.items():
        pred = Fraction(min(i, ip) * (n + p), n * n)
        check(f"P(d_{i},d_{ip} both)", c, pred)
    for (i, ip), c in cnt_ed.items():
        pred = Fraction(2 * i * ip, n * n)
        check(f"P(e_{i},d_{ip} both)", c, pred)

    if verbose:
        print(f"n={n} p={p} q={q}: {len(mismatches)} mismatches out of "
              f"{len(cnt_e)+len(cnt_d)+len(cnt_ee)+len(cnt_dd)+len(cnt_ed)} checks")
    return mismatches


if __name__ == "__main__":
    all_mismatches = []
    total_checks = 0
    cases = []
    for n in range(2, 10):
        for p in range(1, n):
            for q in range(1, n - p + 1):
                cases.append((n, p, q))
    print(f"Testing {len(cases)} (n,p,q) configurations...")
    for (n, p, q) in cases:
        mm = build_and_check(n, p, q)
        all_mismatches.extend([(n, p, q, *m) for m in mm])

    print(f"Total (n,p,q) configurations tested: {len(cases)}")
    print(f"Total mismatches: {len(all_mismatches)}")
    if all_mismatches:
        for m in all_mismatches[:30]:
            print("MISMATCH:", m)
    else:
        print("ALL REDIRECT-STRUCTURE FORMULAS (R1)-(R5) CONFIRMED EXACTLY, "
              "0 mismatches, all (n,p,q) with n=2..9.")
