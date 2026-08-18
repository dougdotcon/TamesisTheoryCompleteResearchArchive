"""
Run run_vg_analysis (UNMODIFIED, imported from vg_common.py) on one real
PRE/POST variant. Called separately per (domain, variant) so the 4 runs can
execute in parallel background processes.

Usage: python3 run_real_domain.py <domain> <variant>
  domain: geo | hydro
  variant: primary | robust
"""
import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vg_common import run_vg_analysis, SEED

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

domain, variant = sys.argv[1], sys.argv[2]
pre = np.load(os.path.join(DATA_DIR, f"{domain}_pre_{variant}.npy"))
post = np.load(os.path.join(DATA_DIR, f"{domain}_post_{variant}.npy"))

print(f"[{domain}/{variant}] n_pre_raw={len(pre)} n_post_raw={len(post)}", flush=True)
t0 = time.time()
result = run_vg_analysis(pre, post, seed=SEED)
elapsed = time.time() - t0
result["wall_clock_seconds"] = elapsed
result["domain"] = domain
result["variant"] = variant

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"result_{domain}_{variant}.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"[{domain}/{variant}] DONE in {elapsed:.1f}s -> {out_path}", flush=True)
print(f"[{domain}/{variant}] d_B_pre={result['d_B_pre']} d_B_post={result['d_B_post']} "
      f"p_d_B={result['p_d_B']} status_pre={result['real_pre']['status']} status_post={result['real_post']['status']}", flush=True)
print(f"[{domain}/{variant}] C_pre={result['C_pre']} C_post={result['C_post']} delta_C={result['delta_C']} p_C={result['p_C']}", flush=True)
