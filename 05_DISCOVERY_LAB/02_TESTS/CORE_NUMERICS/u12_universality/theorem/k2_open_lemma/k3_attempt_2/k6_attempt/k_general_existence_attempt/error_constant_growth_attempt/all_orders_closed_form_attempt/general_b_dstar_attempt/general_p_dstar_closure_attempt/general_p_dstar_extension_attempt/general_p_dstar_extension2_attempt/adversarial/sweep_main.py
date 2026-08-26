"""
Referee's own exhaustive verification sweep: Assembler.D_star (built
fresh, from scratch) vs ground_truth.D_star (Corollary A3, built
fresh, from scratch), for p=21,...,40.

Scale: r=0..R_MAX, b=0..B_MAX, chosen to fit this referee's practical
compute budget for this task (explicitly scaled down from the target
document's claimed r<=200,b<=30 -- see REFEREE_REPORT.md for why and
what scale was actually reached).
"""
import sys
import time
from fractions import Fraction

from assemble import Assembler
from ground_truth import D_star as gt_D_star

R_MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 150
B_MAX = int(sys.argv[2]) if len(sys.argv) > 2 else 25
P_LO = int(sys.argv[3]) if len(sys.argv) > 3 else 21
P_HI = int(sys.argv[4]) if len(sys.argv) > 4 else 40

total_checks = 0
total_fails = 0
t_start = time.time()

with open("sweep_main.log", "w") as log:
    def out(s):
        print(s)
        log.write(s + "\n")
        log.flush()

    out(f"referee main sweep: p={P_LO}..{P_HI}, r=0..{R_MAX}, b=0..{B_MAX}")
    for p in range(P_LO, P_HI + 1):
        asm = Assembler()
        tp0 = time.time()
        checks = 0
        fails = 0
        for b in range(0, B_MAX + 1):
            for r in range(0, R_MAX + 1):
                got = asm.D_star(p, r, b)
                want = gt_D_star(p, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    out(f"MISMATCH p={p} r={r} b={b} got={got} want={want}")
        tp1 = time.time()
        total_checks += checks
        total_fails += fails
        out(f"p={p}: checks={checks} fails={fails} time={tp1 - tp0:.2f}s")

    t_end = time.time()
    out(f"TOTAL: checks={total_checks} fails={total_fails} wallclock={t_end - t_start:.2f}s")
