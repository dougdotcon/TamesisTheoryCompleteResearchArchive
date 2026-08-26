"""
Exact finite-n combinatorics for the SECOND-MOMENT fixed-K bridge.

Target quantity: P_n^{(K)}(both) := P(points 0,1 both cyclic | K_n = K),
under THEOREM.md Definition 4 (uniform permutation pi of [n], a uniform
random K-subset R of rerouted indices, i.i.d. Uniform([n]) reroute
targets for i in R), for two FIXED distinct points -- the finite-n
analogue of the already-PROVED continuum quantity E[M_K^2]=1/(K+1)
(Estagio 24, proved directly on L(c) via the whole-space cyclic-mass
density, not via any n->infinity limit).

Section A: brute-force EXACT enumeration (arbitrary-precision integers /
fractions.Fraction, no floating point, no randomness) for K=0,1,2,3,
small n -- same style as THEOREM.md's own k1_exact_check.py and the
parent front's uniform_cyclic_restriction_exact.py.

Section B: for K=1, a hand-derived EXACT closed form in n (see
ATTEMPT.md Section 2; debug_k1_subcases.py records the self-caught
first attempt that was WRONG -- it silently assumed the reroute point
is always disjoint from the two query points, missing the O(1/n)-weight
case where the reroute source coincides with one of the two query
points, an error that flips the leading-order rate from O(1/n^2) [what
one gets from the disjoint case alone, wrongly extrapolated] to the
TRUE O(1/n)). The corrected closed form is cross-checked against
Section A's brute force for every n tested, exactly (not approximately).

Section C: rate extraction -- n*(P_n^{(K)}(both) - 1/(K+1)) computed
exactly for every enumerated (n,K), to see whether it stabilizes
(supporting an O(1/n) rate, as K=1 proves) rather than O(1/n^2) (the
marginal case's rate, THEOREM.md Corollary 4.3 / Proposition 4).

No seeds anywhere in this script (deterministic exact enumeration).
"""
import itertools
from fractions import Fraction
import sympy as sp


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


def both_cyclic_prob_exact(n, K, points=(0, 1)):
    total_configs = 0
    both_count = 0
    all_indices = list(range(n))
    perms = list(itertools.permutations(all_indices))
    subsets = list(itertools.combinations(all_indices, K))
    for R in subsets:
        target_choices = list(itertools.product(range(n), repeat=K)) if K > 0 else [()]
        for perm in perms:
            for targets in target_choices:
                f = list(perm)
                for idx, i in enumerate(R):
                    f[i] = targets[idx]
                total_configs += 1
                cyc = cyclic_set(f, n)
                if points[0] in cyc and points[1] in cyc:
                    both_count += 1
    return Fraction(both_count, total_configs), total_configs


def k1_closed_form_correct(n):
    """CORRECTED exact closed form for P_n^{(1)}(0,1 both cyclic):
    (3n^2 - n + 2) / (6n^2) = 1/2 - 1/(6n) + 1/(3n^2), derived in
    ATTEMPT.md Section 2 by splitting on whether the single reroute
    point coincides with one of the two query points (weight 2/n) or
    not (weight (n-2)/n), each sub-case itself an exact finite sum
    over the pi-cycle length containing the reroute point. Verified
    against debug_k1_subcases.py's independent sympy summation."""
    n = Fraction(n)
    return (3 * n**2 - n + 2) / (6 * n**2)


if __name__ == "__main__":
    print("=== K=0 sanity: both cyclic always (trivial identity, all n) ===")
    for n in range(2, 6):
        val, cfg = both_cyclic_prob_exact(n, 0)
        print(f"n={n} K=0: P(both cyclic) = {val}  (configs={cfg})  target=1  match={val==1}")
        assert val == 1

    print()
    print("=== K=1: brute force vs CORRECTED hand-derived closed form ===")
    print("closed form: (3n^2 - n + 2)/(6n^2) = 1/2 - 1/(6n) + 1/(3n^2)")
    k1_rows = []
    for n in range(2, 8):
        val, cfg = both_cyclic_prob_exact(n, 1)
        cf = k1_closed_form_correct(n)
        match = (val == cf)
        rate = n * (val - Fraction(1, 2))
        print(f"n={n} K=1: brute={val}  closed_form={cf}  match={match}  "
              f"n*(val-1/2)={rate}  (configs={cfg})")
        assert match, f"MISMATCH at n={n}: brute={val} vs closed_form={cf}"
        k1_rows.append((n, val))
    print(f"n*(val-1/2) -> -1/6 as n->oo (exact, since val=1/2-1/(6n)+1/(3n^2) "
          f"=> n*(val-1/2) = -1/6 + 1/(3n) -> -1/6)")

    print()
    print("=== K=2: brute force only (small n, factorial cost) ===")
    k2_rows = []
    for n in range(3, 8):
        val, cfg = both_cyclic_prob_exact(n, 2)
        target = Fraction(1, 3)
        rate = n * (val - target)
        print(f"n={n} K=2: P(both cyclic) = {val} = {float(val):.6f}  "
              f"n*(val-1/3)={rate}={float(rate):.6f}  (configs={cfg})")
        k2_rows.append((n, val))

    print()
    print("=== K=3: brute force only (small n, factorial cost) ===")
    k3_rows = []
    for n in range(4, 7):
        val, cfg = both_cyclic_prob_exact(n, 3)
        target = Fraction(1, 4)
        rate = n * (val - target)
        print(f"n={n} K=3: P(both cyclic) = {val} = {float(val):.6f}  "
              f"n*(val-1/4)={rate}={float(rate):.6f}  (configs={cfg})")
        k3_rows.append((n, val))

    print()
    print("=== Attempt exact rational-function fit for K=2 from 5 data points ===")
    # Fit val(n) = 1/3 + a/n + b/n^2 + c/n^3 (matches the ansatz "O(1/n) rate")
    # using exact rational linear algebra on the collected (n, val) pairs.
    n_sym = sp.symbols('n')
    a, b, c = sp.symbols('a b c')
    if len(k2_rows) >= 3:
        eqs = []
        pts = k2_rows[:3]
        for (nv, val) in pts:
            nv = sp.Integer(nv)
            eqs.append(sp.Eq(sp.Rational(1, 3) + a / nv + b / nv**2 + c / nv**3, sp.Rational(val.numerator, val.denominator)))
        sol = sp.solve(eqs, [a, b, c])
        print("Fit (using first 3 exact data points, ansatz 1/3+a/n+b/n^2+c/n^3):", sol)
        if sol:
            # check against remaining points
            for (nv, val) in k2_rows[3:]:
                pred = sp.Rational(1, 3) + sol[a] / nv + sol[b] / nv**2 + sol[c] / nv**3
                actual = sp.Rational(val.numerator, val.denominator)
                print(f"  n={nv}: predicted={pred}  actual={actual}  match={sp.simplify(pred-actual)==0}")
