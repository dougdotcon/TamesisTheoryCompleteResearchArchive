"""
Run run_lzc_analysis (UNMODIFIED, imported from lzc_common.py) on one
real PRE/POST domain/variant. Mirrors kramers_moyal/analysis/
run_real_domain.py and the equivalent scripts elsewhere in this lab.
`lzc_common.py`'s core logic is never touched here -- only data loading.

Usage: python3 run_real_domain.py <domain> <variant>
  domain: daphnet | kilauea
  variant: primary | robust
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lzc_common import run_lzc_analysis, SEED

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

DOMAIN_PREFIX = {"daphnet": "daphnet", "kilauea": "kilauea"}


def main():
    domain, variant = sys.argv[1], sys.argv[2]
    prefix = DOMAIN_PREFIX[domain]
    pre = np.load(os.path.join(DATA_DIR, f"{prefix}_pre_{variant}.npy"))
    post = np.load(os.path.join(DATA_DIR, f"{prefix}_post_{variant}.npy"))

    print(f"[{domain}/{variant}] n_pre_raw={len(pre)} n_post_raw={len(post)}", flush=True)
    t0 = time.time()
    result = run_lzc_analysis(pre, post, seed=SEED)
    elapsed = time.time() - t0
    result["wall_clock_seconds"] = elapsed
    result["domain"] = domain
    result["variant"] = variant

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"result_{domain}_{variant}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[{domain}/{variant}] DONE in {elapsed:.1f}s -> {out_path}", flush=True)
    print(f"[{domain}/{variant}] status={result['status']}", flush=True)
    if result["status"] == "ok":
        print(f"[{domain}/{variant}] LZC_median: PRE={result['LZC_median_pre']} POST={result['LZC_median_post']} "
              f"delta={result['delta_LZC_median']} p={result['p_LZC_median']}", flush=True)
        print(f"[{domain}/{variant}] LZC_ternary: PRE={result['LZC_ternary_pre']} POST={result['LZC_ternary_post']} "
              f"delta={result['delta_LZC_ternary']} p={result['p_LZC_ternary']}", flush=True)
        print(f"[{domain}/{variant}] subsample_info: pre={result['config']['pre_subsample_info']} "
              f"post={result['config']['post_subsample_info']}", flush=True)
    else:
        print(f"[{domain}/{variant}] insufficient_samples: real_pre={result['real_pre']} real_post={result['real_post']}", flush=True)


if __name__ == "__main__":
    main()
