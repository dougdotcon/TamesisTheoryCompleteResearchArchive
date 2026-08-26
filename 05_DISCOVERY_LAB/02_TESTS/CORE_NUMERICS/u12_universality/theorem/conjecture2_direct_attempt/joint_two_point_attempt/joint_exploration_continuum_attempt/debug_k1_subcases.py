"""
Debug harness: isolate the K=1 two-point bridge computation into its
two sub-cases (reroute point disjoint from the query pair vs. reroute
point equal to one of the query points) and check each hand-derived
formula against exact brute force with R FIXED (not averaged over R),
before reassembling. This produced the correction recorded in
ATTEMPT.md Section 2 / Section 7.1 (first hand-derivation missed the
"rerouted point coincides with a query point" case entirely).
"""
import itertools
from fractions import Fraction


def cyclic_set(f, n):
    cyclic = set()
    for start in range(n):
        seen_set = set()
        x = start
        while x not in seen_set:
            seen_set.add(x)
            x = f[x]
        if x == start:
            cyclic.add(start)
    return cyclic


def both_cyclic_given_R(n, R, points=(0, 1)):
    """Exact P(points both cyclic | reroute set = R fixed), K=len(R)."""
    K = len(R)
    total = 0
    both = 0
    perms = list(itertools.permutations(range(n)))
    target_choices = list(itertools.product(range(n), repeat=K)) if K > 0 else [()]
    for perm in perms:
        for targets in target_choices:
            f = list(perm)
            for idx, i in enumerate(R):
                f[i] = targets[idx]
            total += 1
            cyc = cyclic_set(f, n)
            if points[0] in cyc and points[1] in cyc:
                both += 1
    return Fraction(both, total)


def V_a_formula(n):
    """Case (a): reroute point r notin {query points}. WLOG rerouted
    point is labeled distinctly from query points 1,2 (here use 0 as
    the generic reroute point, 1,2 as query points -- matches the
    brute force call below with R=(0,), points=(1,2))."""
    n = Fraction(n)
    total = Fraction(0)
    for ell in range(1, int(n) + 1):
        ell = Fraction(ell)
        denom = (n - 1) * (n - 2)
        p_neither = (n - ell) * (n - ell - 1) / denom
        p_one = 2 * (ell - 1) * (n - ell) / denom
        p_both = (ell - 1) * (ell - 2) / denom
        contrib = p_neither * 1 + p_one * (ell / (2 * n)) + p_both * (ell / (3 * n))
        total += contrib * Fraction(1, int(n))
    return total


def V_b_formula(n):
    """Case (b): reroute point r = one of the two query points (WLOG
    query points are 0 [rerouted] and 1 [not rerouted])."""
    n = Fraction(n)
    total = Fraction(0)
    for ell in range(1, int(n) + 1):
        ell = Fraction(ell)
        val = ell * (2 * n - ell - 1) / (2 * n * (n - 1))
        total += val * Fraction(1, int(n))
    return total


if __name__ == "__main__":
    print("=== Case (a): reroute point disjoint from query pair ===")
    print("Brute force R=(0,), query points=(1,2), vs V_a_formula(n)")
    for n in range(3, 7):
        bf = both_cyclic_given_R(n, (0,), points=(1, 2))
        formula = V_a_formula(n)
        status = "MATCH" if bf == formula else "MISMATCH"
        print(f"n={n}: brute={bf}  formula={formula}  [{status}]")

    print()
    print("=== Case (b): reroute point = one of the query pair ===")
    print("Brute force R=(0,), query points=(0,1), vs V_b_formula(n)")
    for n in range(3, 7):
        bf = both_cyclic_given_R(n, (0,), points=(0, 1))
        formula = V_b_formula(n)
        status = "MATCH" if bf == formula else "MISMATCH"
        print(f"n={n}: brute={bf}  formula={formula}  [{status}]")

    print()
    print("=== Reassembled K=1 total: (n-2)/n * V_a + (2/n) * V_b, vs full brute force ===")
    from fractions import Fraction as F
    for n in range(3, 7):
        Va = V_a_formula(n)
        Vb = V_b_formula(n)
        total_formula = F(n - 2, n) * Va + F(2, n) * Vb
        # full brute force over all R of size 1 (average), query points (0,1)
        total_bf = Fraction(0)
        cnt = 0
        for r in range(n):
            bf = both_cyclic_given_R(n, (r,), points=(0, 1))
            total_bf += bf
            cnt += 1
        total_bf /= cnt
        status = "MATCH" if total_bf == total_formula else "MISMATCH"
        print(f"n={n}: reassembled_formula={total_formula}  full_brute_avg_over_R={total_bf}  [{status}]")
