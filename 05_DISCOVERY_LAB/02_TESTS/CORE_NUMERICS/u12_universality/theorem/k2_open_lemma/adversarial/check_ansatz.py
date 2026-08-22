#!/usr/bin/env python3
"""
Ansatz-uniqueness stress test for ATTEMPT.md's fitted formula
  psi_n^{(2),R} = (A n^2 + B n + C) / (15 n^2)     [their stated family, §6]

Using MY OWN independently-computed brute-force values (ref_bruteforce_K2_*.json),
NOT the front's psi_k2_rerouted.log:

(1) Solve for A,B,C from an INDEPENDENT split of 3 points (n=3,4,5 -- the
    front fit on n=6,7,8 and checked n=3,4,5; here we fit on the opposite
    triple and check the other one, as a genuinely independent confirmation
    that the answer is not an artifact of which 3 points were chosen).
(2) Report whether the resulting formula matches ALL 6 of my own data
    points exactly.
(3) Stress-test uniqueness: also try fitting a strictly larger family,
    (A n^3 + B n^2 + C n + D) / (15 n^3) (4 unknowns), from 4 points
    (n=3,4,5,6), and check whether it predicts n=7,8 correctly. If the
    "true" answer really has D=0 and reduces to the 3-parameter family,
    this larger family, fit on 4 points, should still recover the exact
    n^2-denominator formula (and match the held-out points); if instead
    it predicts something different at n=7,8, that would mean 6 points do
    NOT uniquely pin down the closed form without assuming the smaller
    ansatz -- worth knowing either way.
"""
import glob
import json
from fractions import Fraction as F


def load_k2():
    data = {}
    for path in glob.glob("ref_bruteforce_K2_*.json"):
        with open(path) as fh:
            d = json.load(fh)
        for n_str, rec in d.items():
            data[int(n_str)] = F(rec["psi_R"])
    return data


def solve_3x3(rows):
    # rows: list of (n, value) with value = (A n^2 + B n + C)/(15 n^2)
    # i.e. 15 n^2 * value = A n^2 + B n + C
    # Solve the 3x3 linear system exactly with Fractions (Cramer's rule).
    import itertools

    M = []
    rhs = []
    for n, val in rows:
        M.append([F(n * n), F(n), F(1)])
        rhs.append(F(15) * n * n * val)

    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    D = det3(M)
    sols = []
    for col in range(3):
        Mi = [row[:] for row in M]
        for r in range(3):
            Mi[r][col] = rhs[r]
        sols.append(det3(Mi) / D)
    return sols  # A, B, C


def solve_4x4(rows):
    # rows: list of (n, value) with value = (A n^3+B n^2+C n+D)/(15 n^3)
    M = []
    rhs = []
    for n, val in rows:
        M.append([F(n**3), F(n**2), F(n), F(1)])
        rhs.append(F(15) * n**3 * val)
    # Gaussian elimination with Fractions
    import copy
    A = [row[:] + [rhs[i]] for i, row in enumerate(M)]
    n = 4
    for col in range(n):
        piv = None
        for r in range(col, n):
            if A[r][col] != 0:
                piv = r
                break
        A[col], A[piv] = A[piv], A[col]
        pivval = A[col][col]
        A[col] = [x / pivval for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                factor = A[r][col]
                A[r] = [A[r][k] - factor * A[col][k] for k in range(n + 1)]
    return [A[i][n] for i in range(n)]


def main():
    data = load_k2()
    print("My own psi_n^(2),R values:")
    for n in sorted(data):
        print(f"  n={n}: {data[n]}")
    print()

    # --- (1) fit on n=3,4,5 (opposite split from ATTEMPT.md's n=6,7,8) ---
    fit_pts = [(3, data[3]), (4, data[4]), (5, data[5])]
    A, B, C = solve_3x3(fit_pts)
    print(f"Fit on n=3,4,5 (independent split, opposite of ATTEMPT.md's n=6,7,8):")
    print(f"  A={A}, B={B}, C={C}")
    print(f"  i.e. psi_n^(2),R = ({A} n^2 + {B} n + {C}) / (15 n^2)")
    all_match = True
    for n in sorted(data):
        pred = (A * n * n + B * n + C) / (15 * n * n)
        ok = (pred == data[n])
        all_match &= ok
        tag = "FIT" if n in (3, 4, 5) else "HOLDOUT"
        print(f"    n={n} [{tag}]: predicted={pred}  actual={data[n]}  match={ok}")
    print(f"  => ALL 6 MATCH (fit-on-{{3,4,5}} split): {all_match}")
    print()

    # Compare to ATTEMPT.md's claimed A,B,C (their stated family form, before
    # simplifying to (5n+2)(n+1)/(12n^2)):
    # (5n+2)(n+1)/(12n^2) = (5n^2+7n+2)/(12n^2) = (25n^2/4 + 35n/4 + 5/2)/(15n^2)
    A_claimed, B_claimed, C_claimed = F(25, 4), F(35, 4), F(5, 2)
    print(f"ATTEMPT.md's claimed (A,B,C) = ({A_claimed}, {B_claimed}, {C_claimed})")
    print(f"My independently-fit (A,B,C)  = ({A}, {B}, {C})")
    print(f"Identical? {(A, B, C) == (A_claimed, B_claimed, C_claimed)}")
    print()

    # --- (3) stress test: fit a STRICTLY LARGER family (4 params, n^3 denom) ---
    print("Stress test: fit the larger 4-parameter family")
    print("  psi_n^(2),R = (A n^3 + B n^2 + C n + D) / (15 n^3)")
    print("on n=3,4,5,6 and see what it predicts at n=7,8 (holdout).")
    fit_pts4 = [(3, data[3]), (4, data[4]), (5, data[5]), (6, data[6])]
    A4, B4, C4, D4 = solve_4x4(fit_pts4)
    print(f"  A={A4}, B={B4}, C={C4}, D={D4}")
    for n in (7, 8):
        pred = (A4 * n**3 + B4 * n**2 + C4 * n + D4) / (15 * n**3)
        print(f"    n={n} [HOLDOUT]: predicted={pred}  actual={data[n]}  match={pred == data[n]}")
    print(f"  (if A4==0 and this reduces to the 3-param family, that's a consistency")
    print(f"   check, not new information; if A4 != 0 but still matches holdout,")
    print(f"   that would show the 6 points do NOT uniquely pin the n^2-denominator")
    print(f"   ansatz over the n^3-denominator one.)")


if __name__ == "__main__":
    main()
