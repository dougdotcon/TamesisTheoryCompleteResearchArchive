"""Locked analysis for the adversarial reproduction (spec: PREREGISTRATION.md
Sections 3-6 only).

  y_T = mean(M*) + c_T - lnln T   vs   x_T = lnlnln T
  WLS, free intercept, w_T = 1/EP_T^2, EP_T^2 = sd_T^2/M_T + EP(c_T)^2
  slope bhat +- SE (unscaled WLS SE; chi2 reported as shape descriptor only)
  z_m = (bhat - p_m)/sqrt(SE^2 + EP(p_m)^2) for the five locked curves
  ternary rule of Section 6; S2 sanity (sd in [0.3, 0.9]).
"""

import json
import os

import numpy as np

from rs_zeta_adv import HEIGHTS, M_PER_HEIGHT

HERE = os.path.dirname(os.path.abspath(__file__))
SLICE_DIR = os.path.join(HERE, "slices_adv")

# Locked calibrated curves (PREREGISTRATION.md Section 4)
CURVES = {
    "iid_v1": (+0.0072, 0.0),
    "iid_v2": (+0.1352, 0.0),
    "iid_v3": (-0.2235, 0.0),
    "cue_v1": (-0.4160, 0.0125),
    "cue_v2": (-0.6871, 0.0141),
}


def main():
    rows = []
    for k, (T, M) in enumerate(zip(HEIGHTS, M_PER_HEIGHT)):
        arr = np.load(os.path.join(SLICE_DIR, f"height_{k}.npy"))
        assert arr.shape == (M,) and not np.any(np.isnan(arr)), \
            f"height {k} incomplete"
        with open(os.path.join(SLICE_DIR, f"cal_height_{k}.json")) as f:
            cal = json.load(f)
        mean_raw = float(np.mean(arr))
        sd = float(np.std(arr, ddof=1))
        c, epc = cal["c_T"], cal["EP_c_T"]
        ep_tot = float(np.sqrt(sd * sd / M + epc * epc))
        rows.append({
            "k": k, "T": T, "M": M,
            "mean_raw": mean_raw, "sd": sd,
            "c_T": c, "EP_c_T": epc,
            "mean_corrected": mean_raw + c,
            "EP_total": ep_tot,
        })

    x = np.array([np.log(np.log(np.log(r["T"]))) for r in rows])
    y = np.array([r["mean_corrected"] - np.log(np.log(r["T"])) for r in rows])
    w = np.array([1.0 / r["EP_total"] ** 2 for r in rows])

    Sw = w.sum()
    Swx = (w * x).sum()
    Swy = (w * y).sum()
    Swxx = (w * x * x).sum()
    Swxy = (w * x * y).sum()
    D = Sw * Swxx - Swx * Swx
    b = (Sw * Swxy - Swx * Swy) / D
    a = (Swxx * Swy - Swx * Swxy) / D
    se_b = float(np.sqrt(Sw / D))
    se_a = float(np.sqrt(Swxx / D))
    resid = y - a - b * x
    chi2 = float((w * resid * resid).sum())

    zs = {}
    for name, (p, ep_p) in CURVES.items():
        zs[name] = float((b - p) / np.sqrt(se_b ** 2 + ep_p ** 2))
    z_asym = {"minus_3_4": float((b + 0.75) / se_b),
              "minus_1_4": float((b + 0.25) / se_b)}

    # Ternary rule (Section 6), on |z|
    az = {n: abs(v) for n, v in zs.items()}
    fhk_favored = (az["cue_v1"] < 3 and az["iid_v1"] >= 5
                   and az["iid_v2"] >= 5 and az["iid_v3"] >= 3)
    iid_favored = (az["iid_v1"] < 3 and az["cue_v1"] >= 5
                   and az["cue_v2"] >= 3)
    if fhk_favored:
        verdict, subcase = "FHK_FAVORED", None
    elif iid_favored:
        verdict, subcase = "IID_FAVORED", None
    else:
        verdict = "INCONCLUSIVE"
        both_canonical_rejected = az["cue_v1"] >= 3 and az["iid_v1"] >= 3
        both_compatible = az["cue_v1"] < 3 and az["iid_v1"] < 3
        if both_canonical_rejected:
            subcase = "NEITHER_MODEL"
        elif both_compatible:
            subcase = "UNDERPOWERED"
        else:
            subcase = "PARTIAL"

    s2_pass = all(0.3 <= r["sd"] <= 0.9 for r in rows)

    out = {
        "subset": "FULL_M (15600 windows, no reduction)",
        "per_height": rows,
        "wls": {"x": x.tolist(), "y": y.tolist(), "weights": w.tolist(),
                "intercept": float(a), "se_intercept": se_a,
                "slope_bhat": float(b), "se_bhat": se_b,
                "chi2_5dof": chi2},
        "z_vs_locked_curves": zs,
        "z_vs_asymptotic_secondary": z_asym,
        "ternary_verdict": verdict,
        "inconclusive_subcase": subcase,
        "sanity_S2_sd_in_0.3_0.9": bool(s2_pass),
        "sanity_S1": "N/A (replaced by post-lock cell-by-cell comparison "
                     "vs primary; triage not read pre-lock)",
    }
    with open(os.path.join(HERE, "adversarial_result.json"), "w") as f:
        json.dump(out, f, indent=2)

    print("=== ADVERSARIAL RESULT (numbers locked at first print) ===")
    for r in rows:
        print(f"T=1e{int(np.log10(r['T'])):02d}: mean_raw={r['mean_raw']:.4f} "
              f"c_T={r['c_T']:+.4f} corrected={r['mean_corrected']:.4f} "
              f"sd={r['sd']:.3f} EP={r['EP_total']:.4f}")
    print(f"bhat = {b:+.4f} +- {se_b:.4f}   intercept = {a:+.4f}   "
          f"chi2(5) = {chi2:.2f}")
    for n, v in zs.items():
        print(f"z_{n} = {v:+.2f}")
    print(f"z vs -3/4: {z_asym['minus_3_4']:+.2f}   "
          f"z vs -1/4: {z_asym['minus_1_4']:+.2f}")
    print(f"VERDICT: {verdict}" + (f" / {subcase}" if subcase else ""))
    print(f"S2 pass: {s2_pass}")


if __name__ == "__main__":
    main()
