#!/usr/bin/env python3
"""
Adversarial referee (wave 17a, DISC-DEC-072) -- independent re-derivation of
Lemma 1 (ATTEMPT.md Sec.2), built ONLY from the prose. No front script read.

Part A: Lemma 1a (labeled circular spacings) -- for b=2..6, every one of the
        (b-1)! ordering cells has a unit-Jacobian triangular map onto the full
        gap simplex, so the labeled-gap density is (b-1)!/ell^(b-1).
Part A2: fresh-seed MC of the labeled gaps (anchor at 0, flow = increasing
        coordinate, gap ENDING at each point), b=2..6, vs Dirichlet(1,..,1).
Part B: the telescoping peel -- for EVERY set partition of {1..K}, K=2..6
        (2+5+15+52+203 patterns), the symbolic product of the four peel factors
        equals prod_j (b_j-1)! exactly (all ell-dependence cancels).
Part C: sum over set partitions of prod (b_j-1)! = K!, K=1..8.

Seeds: 20260861040 (referee range). Exact sympy elsewhere.
"""
import itertools, math, sys
import sympy as sp
import numpy as np
from scipy import stats

def set_partitions(collection):
    collection = list(collection)
    if len(collection) == 1:
        yield [collection]
        return
    first = collection[0]
    for smaller in set_partitions(collection[1:]):
        for i, subset in enumerate(smaller):
            yield smaller[:i] + [[first] + subset] + smaller[i+1:]
        yield [[first]] + smaller

print("="*72)
print("PART A: Lemma 1a -- unit-Jacobian ordering cells, b=2..6")
print("="*72)
ok_A = True
for b in range(2, 7):
    ell = sp.Symbol('ell', positive=True)
    Y = sp.symbols('Y1:%d' % b, positive=True)  # b-1 free points
    n_free = b - 1
    n_cells = 0
    for order in itertools.permutations(range(n_free)):
        # cyclic order in flow direction: 0 -> Y[order[0]] -> ... -> Y[order[-1]] -> 0
        # gap ending at Y[order[0]] is Y[order[0]] - 0; ending at Y[order[k]] is
        # Y[order[k]] - Y[order[k-1]]; anchor's gap = ell - Y[order[-1]] (dependent).
        gaps = {}
        prev = sp.Integer(0)
        for k in order:
            gaps[k] = Y[k] - prev
            prev = Y[k]
        # Jacobian of (Y_free) -> (gaps of the free points), in a FIXED variable
        # order (free point index), which is what a joint density w.r.t. the
        # labeled coordinates means:
        J = sp.Matrix([[sp.diff(gaps[k], Y[m]) for m in range(n_free)]
                       for k in range(n_free)])
        detJ = sp.simplify(J.det())
        if abs(detJ) != 1:
            ok_A = False
            print(f"  b={b} order={order}: |det|={detJ}  *** FAIL")
        n_cells += 1
    print(f"  b={b}: all {n_cells}=(b-1)! ordering cells unimodular -> "
          f"density sum = {math.factorial(b-1)}/ell^{b-1}  "
          f"{'PASS' if ok_A else 'FAIL'}")
# Independent moment route for b=2,3,4: E[prod G^a] by direct integration
print("  moment cross-route (b=2,3,4): labeled-gap mixed moments vs Dirichlet")
ok_A2 = True
for b in range(2, 5):
    ell = sp.Integer(1)
    n_free = b - 1
    Y = sp.symbols('y1:%d' % b, positive=True)
    # labeled gaps as piecewise over orderings; compute E[G_1^2], E[G_1*G_2](b>=3)
    # where G_i = gap ending at free point i, by summing over ordering cells.
    def moment(exps):  # exps over free-point gap labels only
        total = sp.Integer(0)
        for order in itertools.permutations(range(n_free)):
            gaps = {}
            prev = sp.Integer(0)
            for k in order:
                gaps[k] = Y[k] - prev
                prev = Y[k]
            integrand = sp.prod([gaps[i]**e for i, e in enumerate(exps)])
            # region: 0 < Y[order[0]] < Y[order[1]] < ... < 1
            # Nested integration inside-out: after integrating v_idx over
            # (0, v_{idx+1}) the constraint v_idx < v_{idx+1} is consumed, so
            # every later variable integrates from 0 up to the next one.
            # (First version of this harness wrongly used the ALREADY
            # INTEGRATED previous variable as a lower limit -- a referee-side
            # harness bug, caught by leftover symbols in the output; fixed.)
            vars_sorted = [Y[k] for k in order]
            expr = integrand
            for idx in range(len(vars_sorted)):
                v = vars_sorted[idx]
                hi_ = sp.Integer(1) if idx == len(vars_sorted)-1 else vars_sorted[idx+1]
                expr = sp.integrate(expr, (v, sp.Integer(0), hi_))
            total += expr
        return sp.nsimplify(sp.simplify(total))
    def dirich_moment(exps):
        # Dirichlet(1,...,1) with b coordinates; moments of the free-point ones
        num = sp.Integer(math.factorial(b-1))
        for e in exps: num *= sp.Integer(math.factorial(e))
        den = sp.Integer(math.factorial(b-1+sum(exps)))
        return num/den
    tests = [tuple([2]+[0]*(n_free-1))]
    if n_free >= 2: tests.append(tuple([1,1]+[0]*(n_free-2)))
    for exps in tests:
        got, want = moment(exps), dirich_moment(exps)
        match = sp.simplify(got-want) == 0
        ok_A2 &= match
        print(f"    b={b} E[G^{exps}] = {got} vs Dirichlet {want}: "
              f"{'PASS' if match else 'FAIL'}")

print()
print("="*72)
print("PART A2: fresh-seed MC of labeled circular gaps, b=2..6 (N=400000 each)")
print("="*72)
rng = np.random.default_rng(np.random.SeedSequence(20260861040))
ok_MC = True
for b in range(2, 7):
    N = 400000
    n_free = b-1
    Y = rng.random((N, n_free))            # free points on circle of length 1, anchor at 0
    pts = np.concatenate([np.zeros((N,1)), Y], axis=1)   # col 0 = anchor
    # gap ending at point p = p - (largest point strictly below p, cyclically)
    order = np.argsort(pts, axis=1)
    sortedp = np.take_along_axis(pts, order, axis=1)
    gaps_sorted = np.diff(np.concatenate([sortedp, sortedp[:, :1]+1.0], axis=1), axis=1)
    # gap ENDING at sorted point j is sortedp[j]-sortedp[j-1] (cyclic)  -> shift
    gap_end_sorted = np.concatenate([gaps_sorted[:, -1:], gaps_sorted[:, :-1]], axis=1)
    # scatter back to labels
    gap_by_label = np.empty_like(pts)
    np.put_along_axis(gap_by_label, order, gap_end_sorted, axis=1)
    # each labeled gap ~ Beta(1, b-1); test label 1 (a free point) and anchor label 0
    for lab in ([0, 1] if b > 1 else [0]):
        ks = stats.kstest(gap_by_label[:, lab], lambda t, b=b: 1-(1-t)**(b-1))
        m = gap_by_label[:, lab].mean()
        z = (m - 1.0/b)/np.sqrt((1.0/b)*(1-1.0/b)/ (b+1) / N)**1  # rough
        okk = ks.pvalue > 0.001
        ok_MC &= okk
        print(f"  b={b} label={'anchor' if lab==0 else 'free1'}: mean={m:.5f} "
              f"(target {1.0/b:.5f}) KS p={ks.pvalue:.4f} {'PASS' if okk else 'FAIL'}")

print()
print("="*72)
print("PART B: telescoping peel, ALL set partitions, K=2..6")
print("="*72)
ok_B = True
for K in range(2, 7):
    ells = sp.symbols('l1:%d' % (K+1), positive=True)
    n_pat = 0
    all_ok = True
    for part in set_partitions(list(range(1, K+1))):
        blocks = sorted([sorted(bl) for bl in part], key=min)
        R = len(blocks)
        bsz = [len(bl) for bl in blocks]
        c = [0]
        for bj in bsz: c.append(c[-1]+bj)
        s = [sp.Integer(0)]
        for j in range(R): s.append(s[-1] + ells[j])
        prod = sp.Integer(1)
        for j in range(1, R+1):
            bj = bsz[j-1]
            lj = ells[j-1]
            anchor = 1/(1 - s[j-1])                       # residual length density
            members = (lj/(1 - s[j-1]))**(bj-1)           # designated joiners
            stay = ((1 - s[j])/(1 - s[j-1]))**(K - c[j])  # stay-outside sources
            gapsd = sp.Integer(math.factorial(bj-1))/lj**(bj-1)
            prod *= anchor*members*stay*gapsd
        target = sp.Integer(1)
        for bj in bsz: target *= math.factorial(bj-1)
        diff = sp.simplify(prod - target)
        if diff != 0:
            all_ok = False
            print(f"  K={K} partition {blocks}: product != prod(b_j-1)!  *** FAIL")
        n_pat += 1
    ok_B &= all_ok
    print(f"  K={K}: all {n_pat} patterns telescope to prod(b_j-1)! "
          f"{'PASS' if all_ok else 'FAIL'}")

print()
print("="*72)
print("PART C: sum over set partitions of prod (b_j-1)! = K!, K=1..8")
print("="*72)
ok_C = True
for K in range(1, 9):
    tot = 0
    for part in set_partitions(list(range(K))):
        pr = 1
        for bl in part: pr *= math.factorial(len(bl)-1)
        tot += pr
    match = (tot == math.factorial(K))
    ok_C &= match
    print(f"  K={K}: sum = {tot}  K! = {math.factorial(K)}  "
          f"{'PASS' if match else 'FAIL'}")

print()
verdict = ok_A and ok_A2 and ok_MC and ok_B and ok_C
print("OVERALL:", "ALL PASS" if verdict else "*** SOME CHECK FAILED ***")
sys.exit(0 if verdict else 1)
