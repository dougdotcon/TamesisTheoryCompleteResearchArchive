"""
Run run_pe_analysis (UNMODIFIED, imported from pe_common.py) on one real
PRE/POST domain/variant. Mirrors visibility_graph/analysis/run_real_domain.py
for this test line.

Usage: python3 run_real_domain.py <domain> <variant>
  domain: vitaldb | edb
  variant: primary | robust
"""
import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_common import run_pe_analysis, SEED

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

domain, variant = sys.argv[1], sys.argv[2]
pre = np.load(os.path.join(DATA_DIR, f"{domain}_pre_{variant}.npy"))
post = np.load(os.path.join(DATA_DIR, f"{domain}_post_{variant}.npy"))

print(f"[{domain}/{variant}] n_pre_raw={len(pre)} n_post_raw={len(post)}", flush=True)
t0 = time.time()
result = run_pe_analysis(pre, post, seed=SEED)
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
    print(f"[{domain}/{variant}] PCI_pre={result['PCI_pre']} PCI_post={result['PCI_post']} "
          f"delta_PCI={result['delta_PCI']} p_PCI={result['p_PCI']}", flush=True)
    print(f"[{domain}/{variant}] MCI_pre={result['MCI_pre']} MCI_post={result['MCI_post']} "
          f"delta_MCI={result['delta_MCI']} p_MCI={result['p_MCI']}", flush=True)
