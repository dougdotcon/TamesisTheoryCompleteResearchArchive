#!/usr/bin/env python3
"""Weighted-forest identity  W(n) = e*(e+q_1+...+q_n)^(n-1)  — exact check.

Fresh code; no prior front/referee script read or imported.

W(n) := sum over ALL maps f:[n] -> [n] u {ext} that contain no cycle
inside [n] (self-loops f(i)=i count as cycles) of prod_i w(f(i)),
with w(j)=q_j (distinct symbols) and w(ext)=e.

Verified as an EXACT multivariate polynomial identity (own dict-based
polynomial arithmetic over integers; no floating point, no sympy needed)
for n = 1..6 — n=5 is the case K=5 needs; n=6 is beyond target.
Also verifies the unit-weight specialization (counts) = (n+1)^(n-1),
and the degenerate evaluation at e = 1-Q, i.e. e+Q=1: W = e = 1-Q.

The general-n PROOF (Prüfer bijection) is in ATTEMPT.md §3; this script is
the independent brute-force verification of the same identity.
"""
import itertools
from fractions import Fraction

ok_all = True


def check(label, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        ok_all = False


# ------------- tiny exact multivariate polynomial engine (dict of tuples)
def pmul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            out[e] = out.get(e, 0) + ca * cb
    return {e: c for e, c in out.items() if c != 0}


def padd(a, b):
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c != 0}


def has_internal_cycle(f, n):
    """f: tuple of targets in 0..n-1 (internal) or n (ext)."""
    for i in range(n):
        v = i
        for _ in range(n + 1):
            if v == n:
                break
            v = f[v]
            if v == i:
                return True
    return False


for n in range(1, 7):
    nv = n + 1  # variables: q_1..q_n, e (last)
    unit = {tuple([0] * nv): 1}

    def var(i):
        e = [0] * nv
        e[i] = 1
        return {tuple(e): 1}

    # brute-force W(n)
    W = {}
    count_acyclic = 0
    for f in itertools.product(range(n + 1), repeat=n):
        if has_internal_cycle(f, n):
            continue
        count_acyclic += 1
        term = unit
        for i in range(n):
            term = pmul(term, var(f[i]) if f[i] < n else var(n))
        W = padd(W, term)
    # closed form e*(e + q_1 + ... + q_n)^(n-1)
    s = var(n)
    for i in range(n):
        s = padd(s, var(i))
    closed = var(n)
    for _ in range(n - 1):
        closed = pmul(closed, s)
    check(f"n={n}: W(n) == e*(e+sum q)^(n-1) as exact polynomial identity "
          f"({count_acyclic} acyclic maps of {(n+1)**n})",
          W == closed)
    check(f"n={n}: acyclic count = (n+1)^(n-1) = {(n+1)**(n-1)}",
          count_acyclic == (n + 1) ** (n - 1))

    # degenerate evaluation at e = 1 - (q_1+...+q_n), q_i = arbitrary
    # rationals summing to Q<1: W should equal 1-Q exactly.
    import random
    random.seed(0)  # deterministic spot values; no MC here, exact arithmetic
    for trial in range(3):
        qs = [Fraction(random.randint(1, 20), 200) for _ in range(n)]
        Q = sum(qs)
        e_val = 1 - Q
        vals = qs + [e_val]
        tot = Fraction(0)
        for expo, c in W.items():
            t = Fraction(c)
            for x, p in zip(vals, expo):
                t *= x ** p
            tot += t
        if tot != 1 - Q:
            check(f"n={n}: degenerate evaluation trial {trial}", False)
            break
    else:
        check(f"n={n}: W = 1-Q exactly at e=1-Q (3 exact rational points)",
              True)

print("=" * 72)
print("ALL CHECKS PASSED" if ok_all else "SOME CHECKS FAILED")
