"""
Mandatory synthetic validation for `transfer_entropy`, BEFORE any real
data is touched (METHODOLOGY_NOTE.md discipline, same as every prior
candidate in DISC-TRI-RG-001).

Three tiers:
  0. Code-correctness diagnostic (NOT the identifiability validation
     itself): (a) two independent Gaussian white-noise channels -> TE
     should be ~0 in both directions; (b) a coupled AR(1) system with a
     KNOWN unidirectional coupling (X->Y) -> TE(X->Y) should exceed
     TE(Y->X), i.e. TE_net should have the correct sign, well before any
     surrogate testing is even relevant.
  1. Positive control: PRE = uncoupled AR(1) pair (c=0), POST = SAME
     AR(1) pair with coupling switched ON (c=C_STRONG). Tests whether
     TE_net / TE_sum (KSG, primary) show genuine discriminative power
     against BOTH the IAAFT null (primary) and the circular-shift null
     (companion), run through the exact `run_te_analysis` entry point,
     unmodified.
  2. Negative control: PRE and POST are two SEPARATE realizations of the
     SAME uncoupled process (no real transition at all) -- checks that
     the pipeline does not spuriously report significance when nothing
     changed. Run across 3 independent seeds (cheap: ~1-2 min per run)
     for a slightly more informative false-positive read than a single
     draw, without over-interpreting it as a full false-positive-rate
     estimate.

ONE pre-authorized, mechanical correction (METHODOLOGY_NOTE.md
escalation discipline) is applied ONLY if the positive control (tier 1)
shows NO discriminative power in TE_net/TE_sum under EITHER null:
increase C_STRONG from 0.5 to 0.8 (coupling-strength adjustment,
mechanically pre-declared here, not tuned after seeing results) and
re-run tier 1 once. No further attempts after that.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import te_common as te  # noqa: E402

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 12345

N_PER_HALF = 3000  # PRE/POST length for tier 1/2, comfortably below MAX_N_PER_SEGMENT=4000
PHI_X = 0.6
PHI_Y = 0.3
C_STRONG_V1 = 0.5
C_STRONG_V2 = 0.8  # ONE pre-authorized correction value, mechanical, declared here a priori


def gen_ar1_pair(n, phi_x, phi_y, c, seed, burn_in=200):
    """X: AR(1). Y: AR(1) + coupling c*X[t-1] (X->Y unidirectional,
    ground truth). c=0 -> no coupling (independent AR(1) processes)."""
    rng = np.random.default_rng(seed)
    n_tot = n + burn_in
    x = np.zeros(n_tot)
    y = np.zeros(n_tot)
    for t in range(1, n_tot):
        x[t] = phi_x * x[t - 1] + rng.normal(0, 1.0)
        y[t] = phi_y * y[t - 1] + c * x[t - 1] + rng.normal(0, 0.5)
    return x[burn_in:], y[burn_in:]


def tier0_code_correctness():
    print("=== Tier 0: code-correctness diagnostic ===", flush=True)
    results = {}

    # (a) two independent Gaussian channels -> TE ~ 0 both directions
    rng = np.random.default_rng(SEED)
    x = rng.normal(0, 1, 2000)
    y = rng.normal(0, 1, 2000)
    emb_x = te.own_history_embedding(x)
    emb_y = te.own_history_embedding(y)
    mx, taux = emb_x["m"], emb_x["tau"]
    my, tauy = emb_y["m"], emb_y["tau"]
    te_xy, _ = te.te_ksg(x, y, mx, taux, my, tauy)
    te_yx, _ = te.te_ksg(y, x, my, tauy, mx, taux)
    print(f"  independent Gaussians: TE(X->Y)={te_xy:.5f}  TE(Y->X)={te_yx:.5f}", flush=True)
    results["independent_gaussians"] = {
        "TE_XY": te_xy, "TE_YX": te_yx,
        "embedding_x": {"m": mx, "tau": taux}, "embedding_y": {"m": my, "tau": tauy},
        "near_zero_pass": bool(abs(te_xy) < 0.15 and abs(te_yx) < 0.15),
    }

    # (b) coupled AR(1), X->Y, known direction -> TE(X->Y) > TE(Y->X)
    x2, y2 = gen_ar1_pair(2000, PHI_X, PHI_Y, C_STRONG_V1, seed=SEED + 1)
    emb_x2 = te.own_history_embedding(x2)
    emb_y2 = te.own_history_embedding(y2)
    mx2, taux2 = emb_x2["m"], emb_x2["tau"]
    my2, tauy2 = emb_y2["m"], emb_y2["tau"]
    te_xy2, _ = te.te_ksg(x2, y2, mx2, taux2, my2, tauy2)
    te_yx2, _ = te.te_ksg(y2, x2, my2, tauy2, mx2, taux2)
    print(f"  coupled AR(1) (c={C_STRONG_V1}, X->Y ground truth): "
          f"TE(X->Y)={te_xy2:.5f}  TE(Y->X)={te_yx2:.5f}", flush=True)
    results["coupled_ar1_direction"] = {
        "TE_XY": te_xy2, "TE_YX": te_yx2, "c": C_STRONG_V1,
        "embedding_x": {"m": mx2, "tau": taux2}, "embedding_y": {"m": my2, "tau": tauy2},
        "correct_direction_pass": bool(te_xy2 > te_yx2),
    }

    overall_pass = results["independent_gaussians"]["near_zero_pass"] and \
        results["coupled_ar1_direction"]["correct_direction_pass"]
    results["overall_pass"] = bool(overall_pass)
    print(f"  Tier 0 overall_pass = {overall_pass}", flush=True)
    return results


def run_tier1(c_strong, label):
    print(f"=== Tier 1: positive control ({label}, c_strong={c_strong}) ===", flush=True)
    t0 = time.time()
    pre_x, pre_y = gen_ar1_pair(N_PER_HALF, PHI_X, PHI_Y, 0.0, seed=SEED + 10)
    post_x, post_y = gen_ar1_pair(N_PER_HALF, PHI_X, PHI_Y, c_strong, seed=SEED + 11)
    res = te.run_te_analysis(pre_x, pre_y, post_x, post_y)
    dt = time.time() - t0
    print(f"  status={res['status']}  ({dt:.1f}s)", flush=True)
    if res["status"] == "ok":
        print(f"  delta={res['delta']}", flush=True)
        print(f"  p_iaaft={res['p_iaaft']}", flush=True)
        print(f"  p_circular_shift={res['p_circular_shift']}", flush=True)
    res["_wall_time_s"] = dt
    res["_label"] = label
    res["_c_strong"] = c_strong
    return res


def tier1_positive_control():
    res_v1 = run_tier1(C_STRONG_V1, "v1_c0.5")
    passed_v1 = False
    if res_v1["status"] == "ok":
        for ch in ["TE_net", "TE_sum"]:
            p1 = res_v1["p_iaaft"].get(ch)
            p2 = res_v1["p_circular_shift"].get(ch)
            if (p1 is not None and p1 < 0.05) or (p2 is not None and p2 < 0.05):
                passed_v1 = True
    return res_v1, passed_v1


def tier1_correction():
    res_v2 = run_tier1(C_STRONG_V2, "v2_c0.8_ONE_PRE_AUTHORIZED_CORRECTION")
    passed_v2 = False
    if res_v2["status"] == "ok":
        for ch in ["TE_net", "TE_sum"]:
            p1 = res_v2["p_iaaft"].get(ch)
            p2 = res_v2["p_circular_shift"].get(ch)
            if (p1 is not None and p1 < 0.05) or (p2 is not None and p2 < 0.05):
                passed_v2 = True
    return res_v2, passed_v2


def tier2_negative_control(n_seeds=3):
    print(f"=== Tier 2: negative control ({n_seeds} seeds, no real transition) ===", flush=True)
    all_res = []
    n_false_positive = 0
    n_checked = 0
    for i in range(n_seeds):
        t0 = time.time()
        # two SEPARATE realizations of the SAME uncoupled process -- no
        # real transition; PRE and POST are just different random draws
        pre_x, pre_y = gen_ar1_pair(N_PER_HALF, PHI_X, PHI_Y, 0.0, seed=SEED + 100 + 2 * i)
        post_x, post_y = gen_ar1_pair(N_PER_HALF, PHI_X, PHI_Y, 0.0, seed=SEED + 101 + 2 * i)
        res = te.run_te_analysis(pre_x, pre_y, post_x, post_y)
        dt = time.time() - t0
        print(f"  seed {i}: status={res['status']} ({dt:.1f}s)", flush=True)
        if res["status"] == "ok":
            print(f"    delta={res['delta']}", flush=True)
            print(f"    p_iaaft={res['p_iaaft']}", flush=True)
            print(f"    p_circular_shift={res['p_circular_shift']}", flush=True)
            for ch in ["TE_net", "TE_sum"]:
                for pdict in (res["p_iaaft"], res["p_circular_shift"]):
                    p = pdict.get(ch)
                    if p is not None:
                        n_checked += 1
                        if p < 0.05:
                            n_false_positive += 1
        res["_wall_time_s"] = dt
        res["_seed_index"] = i
        all_res.append(res)
    fp_rate = (n_false_positive / n_checked) if n_checked else None
    print(f"  false-positive rate across seeds/channels/nulls: "
          f"{n_false_positive}/{n_checked} = {fp_rate}", flush=True)
    return all_res, fp_rate


def main():
    t_start = time.time()
    out = {"seed": SEED, "n_per_half": N_PER_HALF, "phi_x": PHI_X, "phi_y": PHI_Y}

    tier0 = tier0_code_correctness()
    out["tier0_code_correctness"] = tier0
    if not tier0["overall_pass"]:
        out["final_verdict"] = "CODE_CORRECTNESS_FAILED_STOP"
        with open(os.path.join(OUT_DIR, "validation_synthetic.json"), "w") as f:
            json.dump(out, f, indent=2, default=str)
        print("Tier 0 FAILED -- stopping before tier 1/2. See validation_synthetic.json.", flush=True)
        return

    res_v1, passed_v1 = tier1_positive_control()
    out["tier1_positive_control_v1"] = res_v1
    out["tier1_v1_passed"] = passed_v1

    correction_applied = False
    if not passed_v1:
        correction_applied = True
        res_v2, passed_v2 = tier1_correction()
        out["tier1_positive_control_v2_correction"] = res_v2
        out["tier1_v2_passed"] = passed_v2
        positive_control_passed = passed_v2
    else:
        positive_control_passed = True
    out["correction_applied"] = correction_applied

    tier2_results, fp_rate = tier2_negative_control()
    out["tier2_negative_control"] = tier2_results
    out["tier2_false_positive_rate"] = fp_rate

    if positive_control_passed:
        out["final_verdict"] = "PASS_PROCEED_TO_REAL_DATA"
    else:
        out["final_verdict"] = "CLOSE_AT_VALIDATION_NO_DISCRIMINATIVE_POWER"

    out["_total_wall_time_s"] = time.time() - t_start
    with open(os.path.join(OUT_DIR, "validation_synthetic.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nFINAL VERDICT: {out['final_verdict']}", flush=True)
    print(f"Total wall time: {out['_total_wall_time_s']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
