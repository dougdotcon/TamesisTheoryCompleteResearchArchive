"""Referee exact re-verification of ATTEMPT.md Section 4.2's counterexample,
rebuilt from prose only (no front script read), with TWO independent
cyclic-set algorithms cross-checked against each other, plus a referee
EXTENSION: exhaustive scan of every possible second reroute from the K=1
configuration, to test the exact logical reach of Section 4.3's claim
("direction of the next jump is not deterministic in M").

Model (1-indexed, per THEOREM.md Definition 1):
  n = 6, pi = (1 2 3)(4 5 6):  pi(1)=2, pi(2)=3, pi(3)=1,
                               pi(4)=5, pi(5)=6, pi(6)=4.
  K=1: reroute 1 -> 5.  Claimed cyclic set {4,5,6}, count 3.
  K=2: additionally reroute 3 -> 2.  Claimed cyclic set {2,3,4,5,6}, count 5.
"""
FAIL = 0


def check(name, ok, detail=""):
    global FAIL
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))


def cyclic_orbit(f, n):
    """Algorithm 1: for each i, follow the orbit with a visited list; i is
    cyclic iff the orbit returns to i."""
    out = set()
    for i in range(1, n + 1):
        seen = set()
        j = f[i]
        steps = 0
        while j not in seen and steps <= n + 2:
            if j == i:
                out.add(i)
                break
            seen.add(j)
            j = f[j]
            steps += 1
    return out


def cyclic_peel(f, n):
    """Algorithm 2 (independent): repeatedly delete in-degree-0 nodes
    (Kahn peeling); survivors are exactly the cyclic nodes."""
    indeg = {i: 0 for i in range(1, n + 1)}
    for i in range(1, n + 1):
        indeg[f[i]] += 1
    stack = [i for i in range(1, n + 1) if indeg[i] == 0]
    removed = set()
    while stack:
        v = stack.pop()
        removed.add(v)
        w = f[v]
        indeg[w] -= 1
        if indeg[w] == 0 and w not in removed:
            stack.append(w)
    return set(range(1, n + 1)) - removed


def cyclic_set(f, n):
    a = cyclic_orbit(f, n)
    b = cyclic_peel(f, n)
    assert a == b, f"ALGORITHM DISAGREEMENT: {a} vs {b} on {f}"
    return a


n = 6
pi = {1: 2, 2: 3, 3: 1, 4: 5, 5: 6, 6: 4}

# K = 0
f0 = dict(pi)
c0 = cyclic_set(f0, n)
check("K=0: all 6 points cyclic", c0 == {1, 2, 3, 4, 5, 6}, f"set={sorted(c0)}")

# K = 1: reroute 1 -> 5
f1 = dict(pi)
f1[1] = 5
c1 = cyclic_set(f1, n)
check("K=1 (1->5): cyclic set == {4,5,6}, count 3",
      c1 == {4, 5, 6}, f"set={sorted(c1)} count={len(c1)}")

# hand-check of the document's quoted trajectory: 2->3->1->5->6->4->5->...
traj = [2]
j = 2
for _ in range(7):
    j = f1[j]
    traj.append(j)
check("K=1 trajectory from 2 is 2,3,1,5,6,4,5,6 (enters {4,5,6}, no return)",
      traj == [2, 3, 1, 5, 6, 4, 5, 6], f"traj={traj}")

# K = 2: additionally reroute 3 -> 2
f2 = dict(f1)
f2[3] = 2
c2 = cyclic_set(f2, n)
check("K=2 (also 3->2): cyclic set == {2,3,4,5,6}, count 5",
      c2 == {2, 3, 4, 5, 6}, f"set={sorted(c2)} count={len(c2)}")
check("cyclic count strictly increased 3 -> 5 on adding one reroute",
      len(c1) == 3 and len(c2) == 5)
# the mechanism claim: 2 is 3's ancestor in the K=1 configuration (f1(2)=3)
check("mechanism: f1(2) == 3 (destination 2 is an ancestor of source 3)",
      f1[2] == 3)

# ------------------------------------------------------------------
# Referee extension: ALL possible second reroutes from the K=1 config.
# Sources s in {2..6} (point 1 already rerouted; a second mark lands on a
# distinct point), destinations d in {1..6} (uniform incl. self-loops).
# Question: from this single configuration (hence single M value), can the
# cyclic count move BOTH up and down?  (Needed to refute even a
# "direction deterministic in M" generator; ATTEMPT.md 4.2 exhibits only
# the up-move from this state.)
# ------------------------------------------------------------------
print()
print("Referee scan: all 30 second reroutes (s in 2..6, d in 1..6) from the")
print("K=1 configuration (count 3):")
ups, downs, sames = [], [], []
for s in range(2, n + 1):
    for d in range(1, n + 1):
        fx = dict(f1)
        fx[s] = d
        cnt = len(cyclic_set(fx, n))
        if cnt > 3:
            ups.append((s, d, cnt))
        elif cnt < 3:
            downs.append((s, d, cnt))
        else:
            sames.append((s, d, cnt))
print(f"  increases ({len(ups)}): {ups}")
print(f"  decreases ({len(downs)}): {downs}")
print(f"  unchanged ({len(sames)}): {sames}")
check("document's exhibited up-move (3->2 gives 5) present in scan",
      (3, 2, 5) in ups)
check("BOTH directions occur from the SAME configuration "
      "(refutes deterministic-direction-in-M, and a fortiori monotonicity)",
      len(ups) > 0 and len(downs) > 0)

print()
print("TOTAL FAILURES:", FAIL)
assert FAIL == 0, "AT LEAST ONE COUNTEREXAMPLE CHECK FAILED"
print("ALL COUNTEREXAMPLE CHECKS PASSED (exact, two independent algorithms)")
