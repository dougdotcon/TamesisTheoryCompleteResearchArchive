"""aggregation_closure_attempt -- stage 0 (cheap triage, NOT new simulation):
reuse residual_attempt/H_true_extracted.json (already-collected empirical
H_true(t) from the direct-walk simulator, SeedSequence(918302033)) to check
whether the DERIVED exact elevation P=(1-c/n)^-(b-1) fits the measured
small-t quadratic coefficient H_true(t)/t^2 any better than the
predecessor's leading-order P=1/(1-rho). Pure reuse of existing data (same
spirit as residual_attempt's own "reuse_check" scripts) -- no new
simulation in this script; the fresh, independent test is
lemma_direct_test*.py and mclust_aggregation_validate.py.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RESIDUAL_ATTEMPT = os.path.dirname(HERE)


def main():
    with open(os.path.join(RESIDUAL_ATTEMPT, "H_true_extracted.json")) as fh:
        d = json.load(fh)

    print(f"{'b':>4} {'c':>6} {'rho':>7} | {'H_true/t^2 (small t)':>22} | "
          f"{'(1-rho/2)/(1-rho) [wave4]':>26} | {'1/(1-rho) [CAND]':>18} | "
          f"{'P=(1-c/n)^-(b-1) [CAND5]':>26}")
    rows = []
    for cell in d["cells"]:
        n, b, c, rho = cell["n"], cell["b"], cell["c"], cell["rho"]
        pts = [p for p in cell["points"] if 0.0 < p["t"] < 0.03 and p["h_true"] > 0]
        if not pts:
            continue
        ratios = [p["h_true"] / (p["t"] ** 2) for p in pts]
        ratio_lo = min(ratios)
        ratio_hi = max(ratios)
        wave4_pred = (1.0 - rho / 2.0) / (1.0 - rho)
        cand_pred = 1.0 / (1.0 - rho)
        cand5_pred = (1.0 - c / n) ** (-(b - 1))
        print(f"{b:4d} {c:6.1f} {rho:7.4f} | [{ratio_lo:8.4f}, {ratio_hi:8.4f}]{'':>3} | "
              f"{wave4_pred:26.4f} | {cand_pred:18.4f} | {cand5_pred:26.4f}")
        rows.append(dict(b=b, c=c, rho=rho, ratio_lo=ratio_lo, ratio_hi=ratio_hi,
                          wave4_pred=wave4_pred, cand_pred=cand_pred, cand5_pred=cand5_pred))

    with open(os.path.join(HERE, "quadratic_coeff_reuse_check.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("\nsaved quadratic_coeff_reuse_check.json")
    print("\nNote: CAND5's P is closer to CAND's 1/(1-rho) than either is to the")
    print("measured range -- the (1-c/n) refinement is much smaller than the gap")
    print("between EITHER constant-elevation model and the true H(t) shape.")


if __name__ == "__main__":
    main()
