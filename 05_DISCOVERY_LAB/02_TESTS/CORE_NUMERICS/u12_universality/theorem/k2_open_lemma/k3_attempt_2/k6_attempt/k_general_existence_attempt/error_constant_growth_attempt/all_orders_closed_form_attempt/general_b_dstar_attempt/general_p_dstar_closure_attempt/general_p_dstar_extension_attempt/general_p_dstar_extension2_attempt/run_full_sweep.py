"""
run_full_sweep.py -- the production verification sweep for this front:
p = 21,...,40 (the full target range: the mandate's floor p=21..30,
doubled to the stretch target p=31..40, both reached at the SAME scale,
uniformly, matching the wave-16 predecessor's own scale discipline), each
at r=0,...,200, b=0,...,30 -- exact Fraction comparison against
ground_truth.D_star (Corollary A3, independent Stirling-number
implementation) for every (p,r,b) triple.

Also runs a reduced-scale exploratory push p=41,...,60 (r<=60,b<=10) as
honestly-labelled bonus evidence of continued tractability beyond the
front's committed target -- NOT claimed as full-scale-verified.

Prints a per-p table (mirroring both predecessor fronts' own reporting
style) plus a grand total, and writes the full log to
run_full_sweep.log.
"""

import time
from assemble import verify_range, speed_route_selftest, calibration_self_test


def main():
    print("=== pre-sweep self-checks ===")
    ok1 = speed_route_selftest()
    ok2 = calibration_self_test()
    if not (ok1 and ok2):
        print("PRE-SWEEP SELF-CHECKS FAILED -- aborting main sweep.")
        return

    print()
    print("=== main sweep: p=21..40, r=0..200, b=0..30 ===")
    grand_checks = 0
    grand_fails = 0
    grand_time = 0.0
    rows = []
    for p in range(21, 41):
        checks, fails, examples, elapsed = verify_range(p, r_max=200, b_max=30)
        grand_checks += checks
        grand_fails += fails
        grand_time += elapsed
        rows.append((p, 200, 30, checks, fails, elapsed))
        print(f"p={p:2d} | r=0..200 | b=0..30 | checks={checks:5d} | fails={fails} | time={elapsed:6.2f}s")
        if fails:
            for ex in examples:
                print(f"   FAIL EXAMPLE: p,r,b,got,want = {ex}")

    print()
    print(f"MAIN SWEEP TOTAL: {grand_checks} checks, {grand_fails} fails, {grand_time:.1f}s")

    print()
    print("=== exploratory stretch (reduced scale, NOT claimed as full-scale-verified): "
          "p=41..60, r=0..60, b=0..10 ===")
    stretch_checks = 0
    stretch_fails = 0
    stretch_time = 0.0
    stretch_rows = []
    for p in range(41, 61):
        checks, fails, examples, elapsed = verify_range(p, r_max=60, b_max=10)
        stretch_checks += checks
        stretch_fails += fails
        stretch_time += elapsed
        stretch_rows.append((p, 60, 10, checks, fails, elapsed))
        print(f"p={p:2d} | r=0..60 | b=0..10 | checks={checks:4d} | fails={fails} | time={elapsed:6.2f}s")
        if fails:
            for ex in examples:
                print(f"   FAIL EXAMPLE: p,r,b,got,want = {ex}")

    print()
    print(f"STRETCH SWEEP TOTAL: {stretch_checks} checks, {stretch_fails} fails, {stretch_time:.1f}s")

    print()
    print(f"GRAND TOTAL (main + stretch): {grand_checks + stretch_checks} checks, "
          f"{grand_fails + stretch_fails} fails")


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"\nWall clock: {time.time()-t0:.1f}s")
