#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check #5: does Proposition S (general K),
specialized to K=3, EXACTLY reproduce the four separate K=3 formulas
Estagio 40 / k3_full_cdf_attempt/ATTEMPT.md Section 2.2 states (cited
here from that document's prose, re-typed independently, not copy-pasted
from any .py file)?

Estagio 40's four formulas (K=3, p_i:=L_i/n, p_D:=O/n, u = the index not
in {s,t}):
    P(S=empty)   = p_D
    P(S={s})     = p_s (p_s + p_D)
    P(S={s,t})   = 2 p_s p_t (1 - p_u)
    P(S={0,1,2}) = 6 p_0 p_1 p_2

Proposition S (general K): P(S=A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)

This script checks the specialization symbolically and exactly, for EVERY
one of the 8 subsets of {0,1,2} (not just the 4 "shapes"), using the
constraint p_0+p_1+p_2+p_D=1 to justify the p_D+p_s+p_t = 1-p_u rewriting
Estagio 40 uses for the two-element case.
"""
import sympy as sp
import itertools


def proposition_s_general(A, ps, pD):
    m = len(A)
    prod_A = 1
    for a in A:
        prod_A *= ps[a]
    sum_A = sum(ps[a] for a in A) if A else 0
    return sp.factorial(m) * prod_A * (pD + sum_A)


def main():
    p0, p1, p2, pD = sp.symbols('p0 p1 p2 pD')
    ps = {0: p0, 1: p1, 2: p2}
    constraint = sp.Eq(p0 + p1 + p2 + pD, 1)
    # substitute pD = 1 - p0 - p1 - p2 throughout (normalized weights, as
    # required -- Proposition S is a fact about a genuine probability
    # distribution over {0,1,2,DEAD})
    pD_sub = 1 - p0 - p1 - p2

    all_ok = True

    # (a) empty
    lhs = proposition_s_general(frozenset(), ps, pD).subs(pD, pD_sub)
    rhs = pD_sub
    diff = sp.simplify(lhs - rhs)
    ok = diff == 0
    all_ok &= ok
    print(f"P(S=empty): Prop-S={sp.expand(lhs)}  Estagio40={sp.expand(rhs)}  diff={diff}  [{'OK' if ok else 'FAIL'}]")

    # (b) singletons {s}, all 3
    for s in range(3):
        lhs = proposition_s_general(frozenset([s]), ps, pD).subs(pD, pD_sub)
        rhs = ps[s] * (ps[s] + pD_sub)
        diff = sp.simplify(lhs - rhs)
        ok = diff == 0
        all_ok &= ok
        print(f"P(S={{{s}}}): Prop-S={sp.expand(lhs)}  Estagio40={sp.expand(rhs)}  diff={diff}  [{'OK' if ok else 'FAIL'}]")

    # (c) pairs {s,t}, all 3, using u = the third index, and checking
    # BOTH the "2 p_s p_t (p_D+p_s+p_t)" pre-simplified Prop-S form AND
    # the "2 p_s p_t (1-p_u)" Estagio-40 form are the SAME polynomial once
    # pD is substituted (this is the algebraic step Estagio 40 uses
    # p_D+p_s+p_t=1-p_u, itself a direct consequence of normalization --
    # verified explicitly here, not assumed)
    idx = [0, 1, 2]
    for s, t in itertools.combinations(idx, 2):
        u = [i for i in idx if i not in (s, t)][0]
        lhs = proposition_s_general(frozenset([s, t]), ps, pD).subs(pD, pD_sub)
        rhs = 2 * ps[s] * ps[t] * (1 - ps[u])
        diff = sp.simplify(lhs - rhs)
        # also verify the normalization step itself: pD_sub + ps[s] + ps[t] == 1 - ps[u]
        norm_check = sp.simplify((pD_sub + ps[s] + ps[t]) - (1 - ps[u]))
        ok = (diff == 0) and (norm_check == 0)
        all_ok &= ok
        print(f"P(S={{{s},{t}}}): Prop-S={sp.expand(lhs)}  Estagio40={sp.expand(rhs)}  "
              f"diff={diff}  norm_check={norm_check}  [{'OK' if ok else 'FAIL'}]")

    # (d) full set
    lhs = proposition_s_general(frozenset([0, 1, 2]), ps, pD).subs(pD, pD_sub)
    rhs = 6 * p0 * p1 * p2
    diff = sp.simplify(lhs - rhs)
    ok = diff == 0
    all_ok &= ok
    print(f"P(S={{0,1,2}}): Prop-S={sp.expand(lhs)}  Estagio40={sp.expand(rhs)}  diff={diff}  [{'OK' if ok else 'FAIL'}]")

    # (e) sanity: all 8 probabilities (Prop-S form) sum to exactly 1 after
    # the pD substitution -- independent global check
    total = 0
    for r in range(4):
        for A_tuple in itertools.combinations(range(3), r):
            total += proposition_s_general(frozenset(A_tuple), ps, pD).subs(pD, pD_sub)
    total_diff = sp.simplify(total - 1)
    ok = total_diff == 0
    all_ok &= ok
    print(f"Sum of all 8 P(S=A) values (Prop-S form, K=3): {sp.expand(total)}  "
          f"(diff from 1: {total_diff})  [{'OK' if ok else 'FAIL'}]")

    print()
    print("OVERALL:", "ALL RECOVER EXACTLY" if all_ok else "MISMATCH DETECTED")


if __name__ == '__main__':
    main()
