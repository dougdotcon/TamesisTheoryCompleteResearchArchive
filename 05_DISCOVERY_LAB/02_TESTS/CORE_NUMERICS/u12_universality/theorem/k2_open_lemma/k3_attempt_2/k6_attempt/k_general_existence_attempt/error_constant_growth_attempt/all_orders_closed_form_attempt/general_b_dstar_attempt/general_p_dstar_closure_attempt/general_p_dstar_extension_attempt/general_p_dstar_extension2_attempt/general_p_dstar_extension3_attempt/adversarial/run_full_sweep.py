"""
Main verification sweep for this referee's independent re-derivation of
`general_p_dstar_extension3_attempt/ATTEMPT.md` (wave 19, front (c)).

Compares `assemble.Assembler.D_star` (this referee's own independent
route: Stirling2/hockey-stick Q_p, power-series moments, closed-sum
H_{2k-1}) against `ground_truth.D_star` (this referee's own independent
Corollary A3 implementation), across the target document's claimed range
`p=41,...,80`.

Scale actually reached (explicitly disclosed, per the task mandate):
  - MAIN exhaustive grid: r=0,...,120, b=0,...,25, for every p=41,...,80.
    This is smaller than the document's own claimed r<=200,b<=30 --
    reduced for this referee's own practical compute-time budget (a
    fresh, non-production-optimized implementation), matching the task
    mandate's explicit "scale down if runtime is prohibitive but be
    explicit" allowance.
  - BOUNDARY exhaustive grid: p in {41,60,80}, r=0,...,200, b=0,...,30 --
    matching the document's OWN claimed full-scale ceiling exactly, at
    three representative p values spanning the whole target range
    (start, middle, end), to directly test whether the reduced main grid
    is hiding any boundary effect at large r,b.
  - RANDOMIZED stress test beyond both grids: see random_spotcheck.py.

fractions.Fraction throughout. No .py file from any front in this
lineage was opened, read, or imported.
"""
import time
import assemble as asm
import ground_truth as gt
import ingredients as ing


def run_main_grid(p_lo, p_hi, r_max, b_max, log=print):
    ing._extend_Q_ladder(p_hi)
    ing._warm_up_moments(2 * p_hi)
    total_checks = 0
    total_fails = 0
    t_start = time.time()
    for p in range(p_lo, p_hi + 1):
        t0 = time.time()
        checks_p = 0
        fails_p = 0
        for b in range(0, b_max + 1):
            a = asm.Assembler(p, b)
            for r in range(0, r_max + 1):
                checks_p += 1
                got = a.D_star(r)
                want = gt.D_star(p, r, b)
                if got != want:
                    fails_p += 1
                    log(f"MISMATCH p={p} r={r} b={b} got={got} want={want}")
        dt = time.time() - t0
        total_checks += checks_p
        total_fails += fails_p
        log(f"p={p}: checks={checks_p} fails={fails_p} time={dt:.2f}s")
    total_time = time.time() - t_start
    log(f"MAIN GRID TOTAL: checks={total_checks} fails={total_fails} "
        f"wallclock={total_time:.2f}s  (p={p_lo}..{p_hi}, r=0..{r_max}, b=0..{b_max})")
    return total_checks, total_fails, total_time


def run_boundary_grid(p_values, r_max, b_max, log=print):
    ing._extend_Q_ladder(max(p_values))
    ing._warm_up_moments(2 * max(p_values))
    total_checks = 0
    total_fails = 0
    t_start = time.time()
    for p in p_values:
        t0 = time.time()
        checks_p = 0
        fails_p = 0
        for b in range(0, b_max + 1):
            a = asm.Assembler(p, b)
            for r in range(0, r_max + 1):
                checks_p += 1
                got = a.D_star(r)
                want = gt.D_star(p, r, b)
                if got != want:
                    fails_p += 1
                    log(f"BOUNDARY MISMATCH p={p} r={r} b={b} got={got} want={want}")
        dt = time.time() - t0
        total_checks += checks_p
        total_fails += fails_p
        log(f"[boundary] p={p}: checks={checks_p} fails={fails_p} time={dt:.2f}s")
    total_time = time.time() - t_start
    log(f"BOUNDARY GRID TOTAL: checks={total_checks} fails={total_fails} "
        f"wallclock={total_time:.2f}s (p in {p_values}, r=0..{r_max}, b=0..{b_max})")
    return total_checks, total_fails, total_time


if __name__ == "__main__":
    print("=== MAIN GRID: p=41..80, r=0..120, b=0..25 ===")
    mc, mf, mt = run_main_grid(41, 80, 120, 25)
    print("=== BOUNDARY GRID: p in {41,60,80}, r=0..200, b=0..30 ===")
    bc, bf, bt = run_boundary_grid([41, 60, 80], 200, 30)
    print(f"GRAND TOTAL (main+boundary): checks={mc+bc} fails={mf+bf} "
          f"wallclock={mt+bt:.2f}s")
