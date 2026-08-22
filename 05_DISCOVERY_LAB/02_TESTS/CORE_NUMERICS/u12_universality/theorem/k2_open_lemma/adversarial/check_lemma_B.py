#!/usr/bin/env python3
"""
Independent brute-force check of ATTEMPT.md Lemma B (co-cycle lemma):
for a uniform random permutation of a set of size m, two fixed distinct
elements lie on the same cycle with probability exactly 1/2, for every
m >= 2.

This is a plain permutation fact (no reroutes involved) -- written from
scratch, not copied from any front script.
"""
from fractions import Fraction as F
from itertools import permutations


def same_cycle(perm, a, b):
    # perm is a tuple, perm[i] = image of i
    cur = a
    while True:
        cur = perm[cur]
        if cur == b:
            return True
        if cur == a:
            return False


def check(m):
    total = 0
    hits = 0
    for perm in permutations(range(m)):
        total += 1
        if same_cycle(perm, 0, 1):
            hits += 1
    return F(hits, total)


if __name__ == "__main__":
    for m in range(2, 9):
        p = check(m)
        print(f"m={m:2d}  P(same cycle) = {p}  == 1/2 ? {p == F(1, 2)}")
