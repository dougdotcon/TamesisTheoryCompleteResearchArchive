"""
Run run_dmd_analysis (UNMODIFIED, imported from dmd_common.py) on one
real PRE/POST domain/variant. Mirrors lempel_ziv_complexity/analysis/
run_real_domain.py and the equivalent scripts elsewhere in this lab.
`dmd_common.py`'s core logic is never touched here -- only data loading.

Usage: python3 run_real_domain.py <domain> <variant>
  domain: covid_italy | kilauea
  variant: primary | robust
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmd_common import run_dmd_analysis, SEED

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

DOMAIN_PREFIX = {"covid_italy": "covid_italy", "kilauea": "kilauea"}


def _to_jsonable(obj):
    """Strip numpy scalar/array types and complex numbers recursively so
    json.dump can handle the (rich, nested) result dict."""
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}
    if isinstance(obj, np.ndarray):
        return _to_jsonable(obj.tolist())
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def main():
    domain, variant = sys.argv[1], sys.argv[2]
    prefix = DOMAIN_PREFIX[domain]
    pre = np.load(os.path.join(DATA_DIR, f"{prefix}_pre_{variant}.npy"))
    post = np.load(os.path.join(DATA_DIR, f"{prefix}_post_{variant}.npy"))

    print(f"[{domain}/{variant}] n_pre_raw={len(pre)} n_post_raw={len(post)}", flush=True)
    t0 = time.time()
    result = run_dmd_analysis(pre, post, seed=SEED)
    elapsed = time.time() - t0
    result["wall_clock_seconds"] = elapsed
    result["domain"] = domain
    result["variant"] = variant

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"result_{domain}_{variant}.json")
    with open(out_path, "w") as f:
        json.dump(_to_jsonable(result), f, indent=2)

    print(f"[{domain}/{variant}] DONE in {elapsed:.1f}s -> {out_path}", flush=True)
    print(f"[{domain}/{variant}] status={result['status']}", flush=True)
    if result["status"] == "ok":
        print(f"[{domain}/{variant}] f_dom: PRE={result['f_dom_pre']} POST={result['f_dom_post']} "
              f"delta={result['delta_f_dom']} p={result['p_f_dom']}", flush=True)
        print(f"[{domain}/{variant}] zeta: PRE={result['zeta_pre']} POST={result['zeta_post']} "
              f"delta={result['delta_zeta']} p={result['p_zeta']}", flush=True)
        print(f"[{domain}/{variant}] spectral_gap: PRE={result['spectral_gap_pre']} "
              f"POST={result['spectral_gap_post']} delta={result['delta_spectral_gap']} "
              f"p={result['p_spectral_gap']}", flush=True)
        print(f"[{domain}/{variant}] real_dominant_rate (diagnostic-only): "
              f"PRE={result['real_dominant_rate_pre']} POST={result['real_dominant_rate_post']}", flush=True)
        print(f"[{domain}/{variant}] tau={result['tau']} d={result['d']}", flush=True)
        print(f"[{domain}/{variant}] subsample_info: pre={result['diagnostics']['pre_subsampling']} "
              f"post={result['diagnostics']['post_subsampling']}", flush=True)
    else:
        print(f"[{domain}/{variant}] NOT fully computed: tau_info={result.get('tau_info')} "
              f"d_info={result.get('d_info')}", flush=True)


if __name__ == "__main__":
    main()
