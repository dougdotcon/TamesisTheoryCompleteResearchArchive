"""
run_full_sweep.py -- the production verification for this front
(GENERAL-P-DSTAR-EXTENSION3-ATTEMPT, wave 19, front (c), DISC-DEC-083):

  p = 41,...,80, r = 0,...,200, b = 0,...,30

checked exactly (fractions.Fraction) against ground_truth.D_star
(independent, from-scratch Corollary A3 implementation) for EVERY one of
the forty new p values, at the same full-scale ceiling (r<=200,b<=30) used
throughout this lineage since wave 16.
"""
import sys
import time
from fractions import Fraction

from ground_truth import D_star as ground_truth_D_star
from assemble import Assembler
from odd_part import build_A_table


def run(p_lo=41, p_hi=80, r_max=200, b_max=30, log=True):
    total_checks = 0
    total_fails = 0
    t_all0 = time.time()

    # Pay the one-time cost of the shared bivariate A_k(x,y) table ONCE,
    # up front, to the full k_max=p_hi needed -- every Assembler build
    # after this reuses it (odd_part.build_H_table just collapses the
    # already-built table at y=beta, no recursion re-run).
    t0 = time.time()
    build_A_table(p_hi)
    a_table_time = time.time() - t0
    if log:
        print(f"[one-time] shared A_k(x,y) bivariate table built to k={p_hi}: {a_table_time:.2f}s")

    per_p_results = []
    for p in range(p_lo, p_hi + 1):
        t_p0 = time.time()
        p_checks = 0
        p_fails = 0
        for b in range(0, b_max + 1):
            asm = Assembler(p, b)
            for r in range(0, r_max + 1):
                got = asm.D_star(r)
                want = ground_truth_D_star(p, r, b)
                p_checks += 1
                total_checks += 1
                if got != want:
                    p_fails += 1
                    total_fails += 1
                    print(f"MISMATCH p={p} r={r} b={b}: got={got} want={want}")
        t_p1 = time.time()
        per_p_results.append((p, p_checks, p_fails, t_p1 - t_p0))
        if log:
            print(f"p={p}: checks={p_checks} fails={p_fails} time={t_p1 - t_p0:.2f}s")
            sys.stdout.flush()

    t_all1 = time.time()
    if log:
        print(f"TOTAL (p={p_lo}..{p_hi}, r=0..{r_max}, b=0..{b_max}): "
              f"checks={total_checks} fails={total_fails} "
              f"wallclock={t_all1 - t_all0:.2f}s (incl. {a_table_time:.2f}s one-time A-table build)")
    return total_checks, total_fails, per_p_results, a_table_time


if __name__ == "__main__":
    checks, fails, per_p, a_time = run()
    print("run_full_sweep.py: OK" if fails == 0 else "run_full_sweep.py: FAILED")
