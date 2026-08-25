"""
PROVED (by explicit, exactly-verified example): {number of cyclic
points} is NOT monotonically non-increasing as reroutes are added one
at a time to a FIXED background permutation -- i.e. there is no
"obvious" pathwise-monotone coupling of M_n(c) across increasing K
(equivalently, across increasing c under the natural Poissonization
coupling of ATTEMPT.md Section 4). This directly supports the negative
finding of ATTEMPT.md Section 4: {M(c)}_{c>=0} is not simply Markov (or
monotone) in c under the natural "superpose more marks" coupling.

Mechanism: a reroute of a currently NON-cyclic point x, if it happens
to land on an ANCESTOR of x (a point whose current forward orbit passes
through x), closes a brand-new cycle out of previously-noncyclic
territory -- INCREASING the cyclic count, even though a reroute was
just ADDED (more corruption, not less).

n=6, background permutation pi = (1 2 3)(4 5 6):
  K=0 (no reroutes): pi itself, all 6 points cyclic.
  K=1 (reroute point 1 -> 5): cyclic count DROPS to 3 (cyclic set
       {4,5,6}; the old 3-cycle {1,2,3} is broken into a tail
       2->3->1->(joins the 456 cycle) with none of 1,2,3 cyclic).
  K=2 (ALSO reroute point 3 -> 2, i.e. onto one of 3's own current
       ancestors: in the K=1 graph, 2->3, so 2 is an ancestor of 3):
       this closes a NEW 2-cycle {2,3}, and cyclic count RISES to 5
       (cyclic set {2,3,4,5,6}) -- MORE than the K=1 configuration's 3,
       despite K=2 having MORE reroutes than K=1.

This is checked here by exact simulation of the functional graph (cycle
detection by direct forward-orbit tracing, exact, no floating point,
no randomness).
"""


def cyclic_count_and_set(f, n):
    cyc = []
    for x in range(1, n + 1):
        seen = set()
        y = x
        is_cyclic = False
        for _ in range(n + 1):
            y = f[y]
            if y == x:
                is_cyclic = True
                break
            if y in seen:
                break
            seen.add(y)
        if is_cyclic:
            cyc.append(x)
    return len(cyc), cyc


def main():
    n = 6
    pi = {1: 2, 2: 3, 3: 1, 4: 5, 5: 6, 6: 4}  # (1 2 3)(4 5 6)

    k0_count, k0_set = cyclic_count_and_set(pi, n)
    print(f"K=0 (background pi only): cyclic count = {k0_count}, set = {k0_set}")
    assert k0_count == n, "a permutation must have every point cyclic"

    f1 = dict(pi)
    f1[1] = 5  # reroute point 1 -> 5 (leaves its own 3-cycle)
    k1_count, k1_set = cyclic_count_and_set(f1, n)
    print(f"K=1 (reroute 1->5):        cyclic count = {k1_count}, set = {k1_set}")
    assert (k1_count, sorted(k1_set)) == (3, [4, 5, 6])

    f2 = dict(f1)
    f2[3] = 2  # ADD a second, independent reroute: point 3 -> 2 (2 is 3's ancestor in f1)
    k2_count, k2_set = cyclic_count_and_set(f2, n)
    print(f"K=2 (also reroute 3->2):   cyclic count = {k2_count}, set = {k2_set}")
    assert (k2_count, sorted(k2_set)) == (5, [2, 3, 4, 5, 6])

    print()
    print(f"K=1 -> K=2 (adding ONE more reroute): cyclic count went {k1_count} -> {k2_count}"
          f" ({'INCREASE' if k2_count > k1_count else 'not an increase'})")
    assert k2_count > k1_count, "counterexample did not reproduce -- STOP, do not use this claim"
    print("COUNTEREXAMPLE CONFIRMED: adding a reroute can strictly INCREASE the cyclic count.")
    print("Hence {cyclic count} is not pathwise monotone in K (equivalently, in c under the")
    print("natural Poissonization coupling) -- see ATTEMPT.md Section 4.2.")


if __name__ == "__main__":
    main()
