#!/usr/bin/env python3
"""
INDEPENDENT position-level reduced model, built fresh from the arc
mechanics described in ATTEMPT.md Sec 1.2 / Sec 2 (prose only -- no .py
file from any front in this lineage was read).

Arc mechanics (as described in ATTEMPT.md Sec 1.2, citing the K=2
predecessor's Lemma 1, and independently re-derivable from Definition 4
directly):

  - ARC(0) = points e_1, ..., e_{L0}, with e_{L0} = source 0 itself.
    f(e_i) = e_{i+1} for i < L0 (unmodified pi edge); f(e_{L0}) = f(0) = U0.
  - ARC(1) = points d_1, ..., d_{L1}, with d_{L1} = source 1 itself.
    f(d_i) = d_{i+1} for i < L1; f(d_{L1}) = f(1) = U1.
  - The remaining O = n - L0 - L1 points are "outside": their pi-cycles
    never touch 0 or 1, so under f they are unaffected and automatically
    cyclic, regardless of U0, U1.
  - U0, U1 are i.i.d. Uniform([n]); conditioned on (L0, L1), U0 (resp U1)
    lands in ARC(0) at a uniform position (prob L0/n total), in ARC(1) at
    a uniform position (prob L1/n total), or "outside" (prob O/n, in
    which case that source's chain is dead -- never cyclic).

This script builds, independently, for given (n, L0, L1), the EXACT
conditional distribution of T_arc := #{cyclic points among ARC(0) u
ARC(1)} by enumerating all (L0+L1+1) x (L0+L1+1) landing-class
combinations for (U0, U1) (positions within each arc, or DEAD), each
weighted by exact Fraction probabilities, and running our own from-
scratch cycle detector on the resulting 2-source functional graph. This
is NOT the same code path as "V_s ~ Uniform, use paircount" -- it
re-derives that fact by direct simulation of the arc positions.

Two uses:
  (1) spot-check against the paircount-based conditional CDF formula
      transcribed from ATTEMPT.md Sec 3 (as a formula to test, not as
      part of the model).
  (2) average over the whole (L0, L1) simplex (uniform, C(n,2) pairs, per
      the cited Marked-Point Gap Structure Lemma) to build an independent
      O(n^3)-ish reference engine, checked against Proposicao D2's closed
      form for many n (well beyond true-brute-force reach).
"""
import sys
from fractions import Fraction
from itertools import product


def conditional_T_arc_pmf(n, L0, L1):
    """Return dict t -> Fraction P(T_arc = t | L0, L1), t in
    0..L0+L1, via exact enumeration over landing classes of (U0,U1)."""
    O = n - L0 - L1
    assert O >= 0

    # Landing classes for a source's target: ('e', k) for k=1..L0,
    # ('d', k) for k=1..L1, or 'DEAD'. Each has an exact probability out
    # of n (each individual arc position has weight 1, DEAD has weight O).
    classes = [('e', k) for k in range(1, L0 + 1)] + \
              [('d', k) for k in range(1, L1 + 1)] + \
              (['DEAD'] * 1 if O > 0 else [])
    # weight of 'DEAD' class as a single class must be O (not 1), so
    # handle it specially instead of folding into the loop below.

    def target_node(cls):
        # returns the node U0/U1 effectively points to, or None if DEAD
        if cls == 'DEAD':
            return None
        return cls

    def weight(cls):
        return O if cls == 'DEAD' else 1

    total_pairs_weight = n * n
    pmf = {}

    nodes_e = [('e', i) for i in range(1, L0 + 1)]
    nodes_d = [('d', i) for i in range(1, L1 + 1)]
    all_nodes = nodes_e + nodes_d

    def default_edge(node):
        kind, i = node
        if kind == 'e':
            if i < L0:
                return ('e', i + 1)
            return None  # e_{L0} = source 0, edge determined by U0
        else:
            if i < L1:
                return ('d', i + 1)
            return None  # d_{L1} = source 1, edge determined by U1

    for cls0 in classes:
        for cls1 in classes:
            w = weight(cls0) * weight(cls1)
            f = {}
            for node in all_nodes:
                de = default_edge(node)
                if de is not None:
                    f[node] = de
            f[('e', L0)] = target_node(cls0)  # source 0's f-edge (U0)
            f[('d', L1)] = target_node(cls1)  # source 1's f-edge (U1)

            # cycle detection on this small graph; None = DEAD sink.
            color = {}
            cyclic = set()
            for start in all_nodes:
                if color.get(start) is not None:
                    continue
                path = []
                node = start
                while node is not None and color.get(node) is None:
                    color[node] = 'gray'
                    path.append(node)
                    node = f.get(node)
                if node is not None and color.get(node) == 'gray':
                    idx = path.index(node)
                    for c in path[idx:]:
                        cyclic.add(c)
                for c in path:
                    color[c] = 'black'
            t = len(cyclic)
            pmf[t] = pmf.get(t, 0) + w

    return {t: Fraction(v, total_pairs_weight) for t, v in pmf.items()}


def paircount_slow(A, B, m):
    """#{(v,w): 1<=v<=A, 1<=w<=B, v+w<=m} by direct O(A) loop --
    transcribed from ATTEMPT.md Sec 3 as the formula UNDER TEST (used
    only for the spot-check comparison, never inside the independent
    model above). Kept as the ground-truth reference for paircount()."""
    if m < 2:
        return 0
    total = 0
    for v in range(1, min(A, m - 1) + 1):
        wmax = min(B, m - v)
        if wmax >= 1:
            total += wmax
    return total


def paircount(A, B, m):
    """O(1) closed-form version of paircount_slow, derived independently
    (not from any front's code) purely to make the large-n sweep below
    tractable; cross-checked against paircount_slow by exhaustive random
    testing before use (see self_test_paircount())."""
    if m < 2:
        return 0
    vmax = min(A, m - 1)
    if vmax < 1:
        return 0
    v0 = m - B  # for v <= v0: min(B, m-v) = B ; for v > v0: = m-v
    total = 0
    r1_hi = min(v0, vmax)
    if r1_hi >= 1:
        total += r1_hi * B
    r2_lo = max(v0 + 1, 1)
    if r2_lo <= vmax:
        n_terms = vmax - r2_lo + 1
        first = m - r2_lo
        last = m - vmax
        total += n_terms * (first + last) // 2
    return total


def self_test_paircount():
    import random
    rng = random.Random(20260923501)  # reserved sub-range, see report
    for _ in range(20000):
        A = rng.randint(1, 40)
        B = rng.randint(1, 40)
        m = rng.randint(-2, 90)
        a = paircount_slow(A, B, m)
        b = paircount(A, B, m)
        if a != b:
            raise AssertionError(f"paircount mismatch A={A} B={B} m={m}: "
                                  f"slow={a} fast={b}")
    print("self_test_paircount: 20000/20000 random cases OK "
          "(fast closed-form paircount matches slow O(A) loop)")


def formula_conditional_cdf(n, L0, L1, k):
    """ATTEMPT.md Sec 3's claimed closed form for P(T <= k | L0, L1),
    transcribed as a formula under test (not used to build the
    independent model)."""
    O = n - L0 - L1
    p0 = Fraction(L0, n)
    p1 = Fraction(L1, n)
    pD = Fraction(O, n)
    P_empty = pD
    P_0 = p0 * (p0 + pD)
    P_1 = p1 * (p1 + pD)
    P_01 = 2 * p0 * p1

    def clip(x, lo, hi):
        return max(lo, min(x, hi))

    t = k - O
    term_empty = P_empty * (1 if O <= k else 0)
    term_0 = P_0 * Fraction(clip(t, 0, L0), L0)
    term_1 = P_1 * Fraction(clip(t, 0, L1), L1)
    term_01 = P_01 * Fraction(paircount(L0, L1, t), L0 * L1)
    return term_empty + term_0 + term_1 + term_01


def d2_formula(n, k):
    if k >= n:
        return Fraction(1)
    if k < 0:
        return Fraction(0)
    num = k * (k + 1) * (2 * n * n - 3 * n + k - k * k)
    den = n ** 3 * (n - 1)
    return Fraction(num, den)


def spotcheck_conditional_cdf():
    print("=== Spot-check: independent position-level model vs the "
          "paircount-based conditional-CDF FORMULA (ATTEMPT.md Sec 3) ===")
    configs = [(6, 2, 3), (7, 3, 2), (8, 4, 3), (9, 5, 2), (10, 3, 4),
               (5, 1, 3), (5, 3, 1), (12, 6, 5)]
    all_ok = True
    n_checks = 0
    for (n, L0, L1) in configs:
        pmf = conditional_T_arc_pmf(n, L0, L1)
        O = n - L0 - L1
        for k in range(0, n + 1):
            t = k - O
            # P(T<=k|L) = P(O<=k) [i.e. O<=k always contributes O outside
            # points which are automatically cyclic] but here pmf is over
            # T_arc only; convert: P(T<=k|L) = 0 if k<O, else
            # sum_{t'<=t} pmf(t')
            if k < O:
                model_val = Fraction(0)
            else:
                model_val = sum(v for tt, v in pmf.items() if tt <= t)
            formula_val = formula_conditional_cdf(n, L0, L1, k)
            n_checks += 1
            ok = (model_val == formula_val)
            all_ok &= ok
            status = "OK" if ok else "MISMATCH"
            if not ok:
                print(f"  n={n} L0={L0} L1={L1} k={k}: model={model_val} "
                      f"formula={formula_val}  {status}")
        print(f"  n={n} L0={L0} L1={L1}: all k checked "
              f"({'OK' if all_ok else 'SEE MISMATCHES ABOVE'})")
    print(f"Total comparisons: {n_checks}")
    print("VERDICT:", "MATCH" if all_ok else "MISMATCH FOUND")
    print()
    return all_ok


def independent_full_cdf_exact(n, k):
    """Average the position-level model over the whole (L0,L1) simplex,
    uniform over C(n,2) pairs with L0,L1>=1, L0+L1<=n (per the cited
    Marked-Point Gap Structure Lemma) -- an independent reference engine,
    NOT using Proposicao D2's own closed form or the paircount formula at
    all (only the from-scratch position-level model above)."""
    total_pairs = 0
    acc = Fraction(0)
    for L0 in range(1, n):
        for L1 in range(1, n - L0 + 1):
            total_pairs += 1
            O = n - L0 - L1
            pmf = conditional_T_arc_pmf(n, L0, L1)
            t = k - O
            if k < O:
                val = Fraction(0)
            else:
                val = sum(v for tt, v in pmf.items() if tt <= t)
            acc += val
    assert total_pairs == n * (n - 1) // 2
    return acc / total_pairs


def large_n_check(ns):
    print("=== Independent O(n^3)-ish reference engine (position-level "
          "model, simplex-averaged) vs Proposicao D2 closed form ===")
    all_ok = True
    n_checks = 0
    for n in ns:
        n_ok = True
        for k in range(0, n):
            ref = independent_full_cdf_exact(n, k)
            claim = d2_formula(n, k)
            n_checks += 1
            ok = (ref == claim)
            n_ok &= ok
            all_ok &= ok
            if not ok:
                print(f"  MISMATCH n={n} k={k}: reference={ref} "
                      f"D2={claim}")
        # explicit boundary check, called out separately per the mandate
        boundary_ref = independent_full_cdf_exact(n, n - 1)
        boundary_claim = d2_formula(n, n - 1)
        boundary_ok = (boundary_ref == boundary_claim)
        all_ok &= boundary_ok
        print(f"  n={n}: every k in 0..{n-1} checked, "
              f"{'ALL MATCH' if n_ok else 'MISMATCH'}  "
              f"[boundary k=n-1: {'OK' if boundary_ok else 'MISMATCH'}, "
              f"value={boundary_ref}]")
    print(f"Total comparisons: {n_checks}")
    print("VERDICT:", "ALL MATCH" if all_ok else "MISMATCH FOUND")
    return all_ok


def large_n_check_via_validated_formula(ns):
    """Second-layer check: sum the paircount-based conditional-CDF FORMULA
    (ATTEMPT.md Sec 3) over the whole (L0,L1) simplex directly (O(n^2)
    cells per n, no raw position-level simulation) and compare to
    Proposicao D2. This formula was itself already validated, cell-by-
    cell, against the fully-independent raw position-level simulation in
    spotcheck_conditional_cdf() above -- so this is legitimately an
    independent check of the SIMPLEX-AVERAGING step of the derivation
    (i.e. that averaging the -- already validated -- conditional law over
    the (L0,L1) simplex really does reproduce Proposicao D2's closed
    form), reaching much larger n than the O(n^5) raw simulation above or
    even the front's own O(n^2)-per-n reference engine's n=60 reach."""
    print()
    print("=== Second-layer check: validated conditional-CDF formula, "
          "simplex-averaged directly, vs Proposicao D2 (larger n) ===")
    all_ok = True
    n_checks = 0
    for n in ns:
        total_pairs = n * (n - 1) // 2
        n_ok = True
        for k in range(0, n):
            acc = Fraction(0)
            for L0 in range(1, n):
                for L1 in range(1, n - L0 + 1):
                    acc += formula_conditional_cdf(n, L0, L1, k)
            ref = acc / total_pairs
            claim = d2_formula(n, k)
            n_checks += 1
            ok = (ref == claim)
            n_ok &= ok
            all_ok &= ok
            if not ok:
                print(f"  MISMATCH n={n} k={k}: reference={ref} D2={claim}")
        print(f"  n={n}: every k in 0..{n-1} checked, "
              f"{'ALL MATCH' if n_ok else 'MISMATCH'}")
    print(f"Total comparisons: {n_checks}")
    print("VERDICT:", "ALL MATCH" if all_ok else "MISMATCH FOUND")
    return all_ok


if __name__ == "__main__":
    self_test_paircount()
    ok1 = spotcheck_conditional_cdf()
    # Layer 1: fully independent raw position-level simulation, no
    # formula involved at all -- expensive (O(n^5)-ish), keep n moderate.
    ns_raw = list(range(2, 26)) + [28, 30]
    ok2 = large_n_check(ns_raw)
    # Layer 2: the now-validated formula, simplex-summed directly --
    # cheap (O(n^3) per n), push much further.
    ns_formula = [40, 60, 80, 100, 130, 160, 200]
    ok3 = large_n_check_via_validated_formula(ns_formula)
    print()
    print("OVERALL VERDICT:", "SOUND" if (ok1 and ok2 and ok3) else "MISMATCH FOUND -- SEE ABOVE")
