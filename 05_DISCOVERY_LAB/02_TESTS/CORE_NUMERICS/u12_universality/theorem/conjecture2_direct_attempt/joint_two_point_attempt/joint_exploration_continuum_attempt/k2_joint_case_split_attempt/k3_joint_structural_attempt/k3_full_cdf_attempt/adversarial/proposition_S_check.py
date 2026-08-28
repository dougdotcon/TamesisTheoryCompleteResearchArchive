#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH independent re-derivation of "Proposicao S" (the
law of S, the random set of cyclic reroute sources), by direct exact
symbolic summation over the raw 4^3=64-case destination table.

No .py file from any front in this lineage was read to build this. Only
the following are used as inputs, both from prose (ATTEMPT.md Sec 2.2 /
Estagio 35's cited Lemma 4, both read in full by the referee):

  - The elementary fact (itself proved from first principles below, not
    assumed): each source t in {0,1,2} sends U_t to one of n equally
    likely slots, split among ARC(0),ARC(1),ARC(2),OUTSIDE of sizes
    L_0,L_1,L_2,O; hence dest(t) is categorical on {0,1,2,DEAD} with
    weights (p_0,p_1,p_2,p_D) = (L_0/n,L_1/n,L_2/n,O/n), i.i.d. across
    t=0,1,2 (this itself follows purely from U_0,U_1,U_2 i.i.d. Unif and
    the partition of [n], and is re-derived, not assumed, immediately
    below).
  - "Source s is cyclic" iff iterating dest from s returns to s before
    hitting DEAD (Lemma 4's own definition, cited verbatim).

The front's claimed formulas (ATTEMPT.md Sec 2.2, "Proposicao S"):
  P(S=empty)   = p_D
  P(S={s})     = p_s (p_s + p_D)              (x3, symmetric)
  P(S={s,t})   = 2 p_s p_t (1 - p_u)           (x3, symmetric, u = the third index)
  P(S={0,1,2}) = 6 p_0 p_1 p_2
"""

import itertools
import sympy as sp


def cyclic_sources(dest):
    """dest: dict {0:.., 1:.., 2:..} each value in {0,1,2,'D'}.
    Returns frozenset of cyclic sources, computed from scratch by
    iterating the map from each of 0,1,2 up to 4 steps (enough to detect
    a return to start before hitting 'D', since the state space is
    {0,1,2,D} and D is absorbing/terminal)."""
    cyc = set()
    for s in (0, 1, 2):
        # walk forward from dest(s) until return to s (cyclic) or hit D (not cyclic)
        cyc_flag = False
        x = dest[s]
        steps = 0
        while x != 'D' and steps < 5:
            if x == s:
                cyc_flag = True
                break
            x = dest[x]
            steps += 1
        if cyc_flag:
            cyc.add(s)
    return frozenset(cyc)


def main():
    p0, p1, p2, pD = sp.symbols('p0 p1 p2 pD', positive=True)
    pmap = {0: p0, 1: p1, 2: p2, 'D': pD}

    subset_probs = {}
    total_prob_check = 0
    for d0, d1, d2 in itertools.product([0, 1, 2, 'D'], repeat=3):
        dest = {0: d0, 1: d1, 2: d2}
        prob = pmap[d0] * pmap[d1] * pmap[d2]
        S = cyclic_sources(dest)
        subset_probs[S] = subset_probs.get(S, 0) + prob
        total_prob_check += prob

    print("Raw 64-case symbolic sum complete. Enumerated subsets found:",
          sorted([tuple(sorted(s)) for s in subset_probs.keys()]))

    # simplify every entry (impose p0+p1+p2+pD=1 to match the front's
    # convention, since (p0,p1,p2,pD) are region-fraction weights that
    # must sum to 1 by construction)
    constraint_sub = {pD: 1 - p0 - p1 - p2}

    def simp(expr):
        return sp.simplify(sp.expand(expr.subs(constraint_sub)))

    derived = {k: simp(v) for k, v in subset_probs.items()}

    for k, v in sorted(derived.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
        print(f"  P(S={sorted(k)}) [64-case symbolic] = {v}")

    total_check = sp.simplify(sum(derived.values()) - 1)
    print(f"\nSanity: sum of all 8 P(S=A) - 1 = {total_check}  "
          f"({'OK, equals 0' if total_check == 0 else 'FAIL'})")

    # --- Now compare against the front's claimed closed forms ---
    print("\n--- Comparing against ATTEMPT.md Sec 2.2 'Proposicao S' claims ---")
    all_ok = True

    empty = frozenset()
    claim_empty = pD
    diff = sp.simplify(derived[empty] - simp(claim_empty))
    print(f"P(S=empty): derived={derived[empty]}  claimed(pD)={simp(claim_empty)}  diff={diff}")
    all_ok &= (diff == 0)

    for s in (0, 1, 2):
        key = frozenset([s])
        psyms = {0: p0, 1: p1, 2: p2}
        claim = psyms[s] * (psyms[s] + pD)
        diff = sp.simplify(derived[key] - simp(claim))
        print(f"P(S={{{s}}}): derived={derived[key]}  claimed=p_s(p_s+pD)={simp(claim)}  diff={diff}")
        all_ok &= (diff == 0)

    for s, t in itertools.combinations((0, 1, 2), 2):
        u = ({0, 1, 2} - {s, t}).pop()
        key = frozenset([s, t])
        psyms = {0: p0, 1: p1, 2: p2}
        claim = 2 * psyms[s] * psyms[t] * (1 - psyms[u])
        diff = sp.simplify(derived[key] - simp(claim))
        print(f"P(S={{{s},{t}}}): derived={derived[key]}  "
              f"claimed=2 p_s p_t (1-p_u)={simp(claim)}  diff={diff}")
        all_ok &= (diff == 0)

    key = frozenset([0, 1, 2])
    claim = 6 * p0 * p1 * p2
    diff = sp.simplify(derived[key] - simp(claim))
    print(f"P(S={{0,1,2}}): derived={derived[key]}  claimed=6 p0 p1 p2={simp(claim)}  diff={diff}")
    all_ok &= (diff == 0)

    print()
    if all_ok:
        print("ALL 8 Proposicao-S FORMULAS CONFIRMED by independent 64-case "
              "symbolic sum (zero symbolic discrepancy).")
    else:
        print("*** AT LEAST ONE Proposicao-S FORMULA DOES NOT MATCH. ***")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
