#!/usr/bin/env python3
"""
Cross-check ATTEMPT.md's claimed closed forms against MY OWN independent
brute-force numbers (ref_bruteforce_K*.json), using exact Fraction
arithmetic throughout. No floating point comparison anywhere.
"""
import glob
import json
from fractions import Fraction as F


def psi1(n):
    return F(2, 3) + F(1, 6) / n


def psi1_R(n):
    return F(1, 2) + F(1, 2) / n


def phi1(n):
    return F(2, 3) + F(1, 3) / n**2


def psi2(n):
    return F(8, 15) + F(4, 15) / n + F(1, 15) / n**2


def psi2_R_fitted(n):
    # ATTEMPT.md §6: (5n+2)(n+1)/(12 n^2)
    return F((5 * n + 2) * (n + 1), 12 * n**2)


def phi2_bonus(n):
    # ATTEMPT.md §6: 8/15 + 1/(30n) + 7/(10 n^2) + 1/(5 n^3)
    return F(8, 15) + F(1, 30) / n + F(7, 10) / n**2 + F(1, 5) / n**3


def load_all():
    data = {1: {}, 2: {}, 3: {}}
    for path in glob.glob("ref_bruteforce_K*.json"):
        K = int(path.split("_K")[1].split("_n")[0])
        with open(path) as fh:
            d = json.load(fh)
        for n_str, rec in d.items():
            n = int(n_str)
            data[K][n] = {
                "psi": F(rec["psi"]),
                "psi_R": F(rec["psi_R"]),
                "phi": F(rec["phi"]),
            }
    return data


def main():
    data = load_all()
    print("=" * 100)
    print("K=1 checks (ATTEMPT.md §3, cross-checking THEOREM.md Proposition 4)")
    print("=" * 100)
    for n in sorted(data[1]):
        rec = data[1][n]
        c1 = psi1(n) == rec["psi"]
        c2 = psi1_R(n) == rec["psi_R"]
        c3 = phi1(n) == rec["phi"]
        print(f"n={n:2d}  psi match={c1}  psi_R match={c2}  phi(Prop4) match={c3}"
              f"   [psi={rec['psi']}, psi_R={rec['psi_R']}, phi={rec['phi']}]")
        assert c1 and c2 and c3, f"MISMATCH at n={n}, K=1"

    print()
    print("=" * 100)
    print("K=2 checks (ATTEMPT.md §4.4 psi formula, §6 psi_R fitted formula + bonus phi)")
    print("=" * 100)
    for n in sorted(data[2]):
        rec = data[2][n]
        c1 = psi2(n) == rec["psi"]
        c2 = psi2_R_fitted(n) == rec["psi_R"]
        c3 = phi2_bonus(n) == rec["phi"]
        print(f"n={n:2d}  psi match={c1}  psi_R(fitted) match={c2}  phi(bonus) match={c3}"
              f"   [psi={rec['psi']}, psi_R={rec['psi_R']}, phi={rec['phi']}]")
        assert c1, f"psi_n^(2) MISMATCH at n={n}"
        assert c2, f"psi_n^(2),R fitted-formula MISMATCH at n={n}"
        assert c3, f"phi_n^(2) bonus-formula MISMATCH at n={n}"

    print()
    print("=" * 100)
    print("K=3 (no closed form claimed; just echoing my own numbers next to")
    print("ATTEMPT.md's §7.3 table values, for the reader to eyeball-diff)")
    print("=" * 100)
    attempt_k3_psi = {
        4: F(71, 128), 5: F(1333, 2500), 6: F(187, 360),
        7: F(4897, 9604), 8: F(18023, 35840),
    }
    for n in sorted(data[3]):
        rec = data[3][n]
        claimed = attempt_k3_psi.get(n)
        match = (claimed == rec["psi"]) if claimed is not None else None
        print(f"n={n:2d}  my psi={rec['psi']}  ATTEMPT psi={claimed}  match={match}")

    print()
    print("ALL ASSERTIONS PASSED (K=1, K=2 closed forms match independent brute force exactly)")


if __name__ == "__main__":
    main()
