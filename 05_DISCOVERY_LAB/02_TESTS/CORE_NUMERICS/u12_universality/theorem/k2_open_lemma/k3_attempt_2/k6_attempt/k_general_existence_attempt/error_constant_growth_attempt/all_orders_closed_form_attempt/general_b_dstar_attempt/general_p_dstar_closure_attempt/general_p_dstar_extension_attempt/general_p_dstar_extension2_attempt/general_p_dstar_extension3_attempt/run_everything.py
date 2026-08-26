"""
run_everything.py -- combined production driver for this front. Runs every
self-test and the full verification sweep IN ONE PROCESS, so the expensive
one-time shared bivariate A_k(x,y) table build (odd_part.build_A_table,
paid once, amortized across all forty p values and thirty-one b values --
see odd_part.py's module docstring) is not needlessly repeated across
separate process invocations. Each individual module remains independently
runnable via `python3 <module>.py` (as documented in ATTEMPT.md's
reproducibility table) -- doing so simply re-pays the one-time build cost
in that fresh process, which is fine but slower; this driver exists to
produce the actual numbers reported in ATTEMPT.md in one coherent run.
"""
import sys
import time

import ground_truth
import ingredients
import odd_part
import assemble
import run_full_sweep
import random_spotcheck
import print_closed_forms


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    sys.stdout.flush()


def main():
    t_start = time.time()
    results = {}

    section("ground_truth.py self_test")
    ok = ground_truth.self_test()
    results["ground_truth"] = ok

    section("ingredients.py self_test")
    ingredients.Q_poly(80)
    ingredients.warm_up_moments(160)
    ok = ingredients.self_test()
    results["ingredients"] = ok

    section("odd_part.py self_test (builds the shared A-table to k=80)")
    t0 = time.time()
    ok = odd_part.self_test()
    print(f"[odd_part.py self_test wall clock: {time.time() - t0:.2f}s]")
    results["odd_part"] = ok

    section("assemble.py calibration_self_test + module_smoke_test_b1 + r<p full-formula check")
    ok1 = assemble.calibration_self_test()
    ok2 = assemble.module_smoke_test_b1()
    ok3 = assemble.r_lt_p_full_formula_self_test()
    results["assemble"] = ok1 and ok2 and ok3

    section("run_full_sweep.py: p=41..80, r=0..200, b=0..30 (main target)")
    t0 = time.time()
    checks, fails, per_p, a_time = run_full_sweep.run(41, 80, 200, 30)
    print(f"[run_full_sweep wall clock: {time.time() - t0:.2f}s]")
    results["main_sweep"] = (fails == 0)
    results["main_sweep_checks"] = checks
    results["main_sweep_fails"] = fails
    results["main_sweep_per_p"] = per_p
    results["a_table_build_time"] = a_time

    section("print_closed_forms.py: b=0,1 printed forms, p=41..80")
    t0 = time.time()
    lines, pchecks, pfails, qc, qf = print_closed_forms.run(41, 80)
    with open("printed_forms.log", "w") as f:
        f.write("\n".join(lines))
    print(f"[print_closed_forms wall clock: {time.time() - t0:.2f}s]")
    results["printed_forms"] = (pfails == 0 and qf == 0)
    results["printed_forms_checks"] = pchecks
    results["qneg1_checks"] = qc
    results["qneg1_fails"] = qf

    section("random_spotcheck.py: seed 20260884000, reaching beyond the main grid")
    t0 = time.time()
    rchecks, rfails = random_spotcheck.run(n_samples=400, p_range=(41, 80), r_max=400, b_max=60)
    print(f"[random_spotcheck wall clock: {time.time() - t0:.2f}s]")
    results["random_spotcheck"] = (rfails == 0)
    results["random_spotcheck_checks"] = rchecks

    section("SUMMARY")
    for k, v in results.items():
        print(f"{k}: {v}")
    print(f"\nTOTAL WALL CLOCK: {time.time() - t_start:.2f}s")

    all_ok = all([
        results["ground_truth"], results["ingredients"], results["odd_part"],
        results["assemble"], results["main_sweep"], results["printed_forms"],
        results["random_spotcheck"],
    ])
    print("run_everything.py: ALL OK" if all_ok else "run_everything.py: SOME FAILED")
    return results


if __name__ == "__main__":
    main()
