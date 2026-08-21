"""
Run the LOCKED `run_te_analysis` pipeline (te_common.py), UNMODIFIED, on
both real domains x both variants (primary/robust), per
../METHODOLOGY_NOTE.md. Writes result_<domain>_<variant>.json.

Usage: python3 run_real_domain.py <domain> <variant>
  domain: chbmit | turkeyeq
  variant: primary | robust
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import te_common as te  # noqa: E402

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(ANALYSIS_DIR), "data")

DOMAIN_PREFIX = {"chbmit": "chbmit", "turkeyeq": "turkeyeq"}


def load_segment(domain, segment, variant):
    prefix = DOMAIN_PREFIX[domain]
    x = np.load(os.path.join(DATA_DIR, f"{prefix}_{segment}_x_{variant}.npy"))
    y = np.load(os.path.join(DATA_DIR, f"{prefix}_{segment}_y_{variant}.npy"))
    return x, y


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 run_real_domain.py <chbmit|turkeyeq> <primary|robust>")
        sys.exit(1)
    domain, variant = sys.argv[1], sys.argv[2]
    assert domain in DOMAIN_PREFIX
    assert variant in ("primary", "robust")

    print(f"Loading {domain}/{variant} ...", flush=True)
    pre_x, pre_y = load_segment(domain, "pre", variant)
    post_x, post_y = load_segment(domain, "post", variant)
    print(f"  pre: n_x={len(pre_x)} n_y={len(pre_y)}   post: n_x={len(post_x)} n_y={len(post_y)}", flush=True)

    t0 = time.time()
    res = te.run_te_analysis(pre_x, pre_y, post_x, post_y)
    dt = time.time() - t0
    print(f"status={res['status']}  ({dt:.1f}s)", flush=True)
    if res["status"] == "ok":
        print(f"delta={res['delta']}", flush=True)
        print(f"p_iaaft={res['p_iaaft']}", flush=True)
        print(f"p_circular_shift={res['p_circular_shift']}", flush=True)

    res["_domain"] = domain
    res["_variant"] = variant
    res["_wall_time_s"] = dt

    out_path = os.path.join(ANALYSIS_DIR, f"result_{domain}_{variant}.json")
    with open(out_path, "w") as f:
        json.dump(res, f, indent=2, default=str)
    print(f"Wrote {out_path}", flush=True)


if __name__ == "__main__":
    main()
