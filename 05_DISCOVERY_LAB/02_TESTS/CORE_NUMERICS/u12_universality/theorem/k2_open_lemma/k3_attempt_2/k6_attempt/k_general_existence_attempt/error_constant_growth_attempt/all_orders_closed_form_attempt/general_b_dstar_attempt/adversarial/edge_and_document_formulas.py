"""
Edge cases (r=0, r<p, b=0 boundary, large r, large b) + verification of the
document's PRINTED concrete b=2,3 closed-form instances against ground truth,
purely as extra scrutiny beyond the main sweep in assembled.py.
"""
from fractions import Fraction
import time
from own_ground_truth import D_star, varphi, fact
from assembled import D_assembled


def phi_frac(r):
    return varphi(r)


def check_document_instances(r_max):
    fails = 0
    checks = 0

    def D1_2(r):
        return Fraction((r + 2) * (r + 3), 2 * (2 * r + 3)) * phi_frac(r) - Fraction(r + 2, 2 * (r + 1))

    def D1_3(r):
        return Fraction((r + 3) * (r + 6), 2 * (2 * r + 3)) * phi_frac(r) \
            - Fraction(3 * r * r + 17 * r + 24, 4 * (r + 1) * (r + 2))

    def D2_2(r):
        return Fraction(3 * r ** 3 + 33 * r ** 2 + 94 * r + 80, 16 * (2 * r + 3)) * phi_frac(r) \
            - Fraction(2 * r ** 2 + 9 * r + 10, 6 * (r + 1))

    def D2_3(r):
        return Fraction(3 * r ** 3 + 58 * r ** 2 + 265 * r + 354, 16 * (2 * r + 3)) * phi_frac(r) \
            - Fraction((r + 3) * (11 * r ** 2 + 75 * r + 118), 24 * (r + 1) * (r + 2))

    def D3_2(r):
        return Fraction(5 * r ** 4 + 104 * r ** 3 + 501 * r ** 2 + 914 * r + 576, 64 * (2 * r + 3)) * phi_frac(r) \
            - Fraction(5 * r ** 3 + 39 * r ** 2 + 94 * r + 72, 24 * (r + 1))

    targets = [
        ("D1_2", 1, 2, D1_2), ("D1_3", 1, 3, D1_3),
        ("D2_2", 2, 2, D2_2), ("D2_3", 2, 3, D2_3),
        ("D3_2", 3, 2, D3_2),
    ]
    for name, p, b, fn in targets:
        for r in range(0, r_max + 1):
            got = fn(r)
            want = D_star(p, r, b)
            checks += 1
            if got != want:
                fails += 1
                print(f"FAIL document formula {name} r={r}: {got} vs {want}")
    print(f"check_document_instances(r_max={r_max}): {checks} checks, {fails} failures")
    return fails


def check_r_less_than_p(p_max, r_max_extra, b_max, assembled_p_max=4):
    """D^{*(p)}_r(b) must be exactly 0 for r<p (empty sum in Corollary A3);
    check ground truth for p up to p_max (pure Corollary A3, no scope limit),
    and additionally cross-check the assembled formula for p up to
    assembled_p_max (the document's actual claimed scope, p=1..4 -- the
    moments/Q_p machinery here is only built out to p=4)."""
    fails = 0
    checks = 0
    for p in range(1, p_max + 1):
        for r in range(0, p):  # r < p strictly, includes r=0
            for b in range(0, b_max + 1):
                gt = D_star(p, r, b)
                checks += 1
                if gt != 0:
                    fails += 1
                    print(f"FAIL ground truth nonzero for r<p: p={p} r={r} b={b}: {gt}")
                if p <= assembled_p_max:
                    asm = D_assembled(p, r, b)
                    checks += 1
                    if asm != 0:
                        fails += 1
                        print(f"FAIL assembled nonzero for r<p: p={p} r={r} b={b}: {asm}")
                    checks += 1
                    if asm != gt:
                        fails += 1
                        print(f"FAIL assembled!=gt for r<p: p={p} r={r} b={b}: {asm} vs {gt}")
    print(f"check_r_less_than_p(p_max={p_max}, b_max={b_max}): {checks} checks, {fails} failures")
    return fails


def check_r_equals_p(p_max, b_max):
    """r=p is the first nonzero case (single term j=p): sanity + agreement."""
    fails = 0
    checks = 0
    for p in range(0, p_max + 1):
        r = p
        for b in range(0, b_max + 1):
            gt = D_star(p, r, b)
            checks += 1
            asm = D_assembled(p, r, b) if p >= 1 else None
            if p >= 1:
                checks += 1
                if asm != gt:
                    fails += 1
                    print(f"FAIL r=p boundary p={p} b={b}: asm={asm} gt={gt}")
    print(f"check_r_equals_p(p_max={p_max}, b_max={b_max}): {checks} checks, {fails} failures")
    return fails


def check_b_zero_boundary(p_max, r_max):
    fails = 0
    checks = 0
    for p in range(1, p_max + 1):
        for r in range(0, r_max + 1):
            gt = D_star(p, r, 0)
            asm = D_assembled(p, r, 0)
            checks += 1
            if gt != asm:
                fails += 1
                print(f"FAIL b=0 boundary p={p} r={r}: asm={asm} gt={gt}")
    print(f"check_b_zero_boundary(p_max={p_max}, r_max={r_max}): {checks} checks, {fails} failures")
    return fails


def check_large_r_large_b(p_max, r_values, b_values):
    fails = 0
    checks = 0
    for p in range(1, p_max + 1):
        for r in r_values:
            for b in b_values:
                gt = D_star(p, r, b)
                asm = D_assembled(p, r, b)
                checks += 1
                if gt != asm:
                    fails += 1
                    print(f"FAIL large r/b p={p} r={r} b={b}: asm(len={len(str(asm))}) gt(len={len(str(gt))})")
    print(f"check_large_r_large_b: r in {r_values}, b in {b_values}, p<={p_max}: "
          f"{checks} checks, {fails} failures")
    return fails


if __name__ == "__main__":
    t0 = time.time()
    f1 = check_document_instances(r_max=300)
    print(f"  elapsed {time.time()-t0:.1f}s")

    t0 = time.time()
    f2 = check_r_less_than_p(p_max=8, r_max_extra=0, b_max=15, assembled_p_max=4)
    print(f"  elapsed {time.time()-t0:.1f}s")

    t0 = time.time()
    f3 = check_r_equals_p(p_max=4, b_max=15)
    print(f"  elapsed {time.time()-t0:.1f}s")

    t0 = time.time()
    f4 = check_b_zero_boundary(p_max=4, r_max=200)
    print(f"  elapsed {time.time()-t0:.1f}s")

    t0 = time.time()
    f5 = check_large_r_large_b(p_max=4, r_values=[300, 500, 800],
                                b_values=[0, 1, 2, 5, 10, 20, 40])
    print(f"  elapsed {time.time()-t0:.1f}s")

    total = f1 + f2 + f3 + f4 + f5
    print(f"TOTAL FAILURES: {total}")
