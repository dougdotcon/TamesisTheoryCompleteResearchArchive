#!/usr/bin/env python3
"""
Adversarial referee -- Lemma 3 (weighted-forest identity) verified by brute
force with an own exact polynomial engine (dict of exponent tuples ->
Fraction). No sympy, no front code.

W(n) := sum over maps h:[n] -> [n] u {ext} with NO cycle inside [n]
        (self-loops count as cycles) of prod_i w(h(i)),
with w(i)=q_i, w(ext)=e.  Claim: W(n) = e*(e+q_1+...+q_n)^(n-1), n=1..7.
Also: unit-weight counts (n+1)^(n-1), and exact rational evaluation at
e = 1 - (q_1+...+q_n) giving W = e for random rational q's.

Independent re-derivation (referee's own, in the report): acyclic maps ==
parent-pointers of trees on {0,..,n} rooted at 0; weight = w_0 *
prod_v w_v^(deg-1); Pruefer bijection gives sum = w_0 (sum_v w_v)^(n-1).
"""
import itertools, sys
from fractions import Fraction

def pmul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x+y for x, y in zip(ea, eb))
            out[e] = out.get(e, 0) + ca*cb
    return {e: c for e, c in out.items() if c != 0}

def padd(a, b):
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, 0) + c
        if out[e] == 0: del out[e]
    return out

def ppow(a, k):
    nv = len(next(iter(a))) if a else 0
    out = {tuple([0]*nv): 1}
    for _ in range(k):
        out = pmul(out, a)
    return out

def has_internal_cycle(h, n):
    # h[i] in {0..n-1} internal, or -1 = ext
    for start in range(n):
        seen = set()
        x = start
        while x != -1 and x not in seen:
            seen.add(x)
            x = h[x]
        if x != -1:
            return True
    return False

overall_ok = True
for n in range(1, 8):
    nv = n + 1  # variables: e, q_1..q_n
    def mono(idx):  # single-variable monomial
        e = [0]*nv; e[idx] = 1
        return {tuple(e): 1}
    W = {}
    count = 0
    for h in itertools.product(range(-1, n), repeat=n):
        if has_internal_cycle(h, n):
            continue
        count += 1
        term = {tuple([0]*nv): 1}
        for i in range(n):
            term = pmul(term, mono(0) if h[i] == -1 else mono(1 + h[i]))
        W = padd(W, term)
    # target e*(e+q1+..+qn)^(n-1)
    s = mono(0)
    for i in range(n):
        s = padd(s, mono(1+i))
    target = pmul(mono(0), ppow(s, n-1))
    ok_poly = (W == target)
    ok_count = (count == (n+1)**(n-1))
    # exact rational evaluation at e = 1 - sum q, random-ish rationals
    qs = [Fraction(2*i+1, 7*n+3+i) for i in range(n)]
    e_val = 1 - sum(qs)
    vals = [e_val] + qs
    def ev(p):
        t = Fraction(0)
        for expo, c in p.items():
            m = Fraction(c)
            for x, k in zip(vals, expo):
                m *= x**k
            t += m
        return t
    ok_eval = (ev(W) == e_val)
    overall_ok &= ok_poly and ok_count and ok_eval
    print(f"n={n}: acyclic maps={count} vs (n+1)^(n-1)={(n+1)**(n-1)} "
          f"{'PASS' if ok_count else 'FAIL'}; "
          f"W == e*(e+Q)^(n-1) as exact polynomial: {'PASS' if ok_poly else 'FAIL'}; "
          f"eval at e=1-Q gives W=e: {'PASS' if ok_eval else 'FAIL'}")

print()
print("OVERALL:", "ALL PASS" if overall_ok else "*** SOME CHECK FAILED ***")
sys.exit(0 if overall_ok else 1)
