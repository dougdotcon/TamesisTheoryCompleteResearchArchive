"""
Run run_km_analysis (UNMODIFIED, imported from km_common.py) on one real
PRE/POST domain/variant. Mirrors permutation_entropy/analysis/
run_real_domain.py and visibility_graph/analysis/run_real_domain.py for
this test line. `km_common.py`'s core logic is never touched here --
only data loading and the `dt` (native sampling interval) needed by the
pipeline's public entry point.

`dt` per domain:
  vfdb:    1/fs = 1/250 Hz = 0.004s (regularly sampled ECG).
  eurchf:  median inter-tick interval over the full download day
           (irregularly-spaced ticks -- see ../data/PROVENANCE_EURCHF.md
           for the explicit note on why this choice does not affect PKS,
           the sole decision channel per METHODOLOGY_NOTE.md's addendum:
           D1/D2's ratio -- and hence the reconstructed p_st and PKS --
           is scale-invariant under a uniform rescaling of tau/dt; dt
           only affects the ABSOLUTE reported tau_ME/D-coefficient
           values and the lag grid's real-time cutoff conversion, both
           purely for reporting, not PKS's numeric value or p-value).

Usage: python3 run_real_domain.py <domain> <variant>
  domain: vfdb | eurchf
  variant: primary | robust
"""
import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from km_common import run_km_analysis, SEED

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

DOMAIN_PREFIX = {"vfdb": "vfdb", "eurchf": "eurchf"}


def load_dt(domain):
    if domain == "vfdb":
        with open(os.path.join(DATA_DIR, "vfdb_segments_meta.json")) as f:
            meta = json.load(f)
        return meta["dt_s"]
    elif domain == "eurchf":
        with open(os.path.join(DATA_DIR, "eurchf_segments_meta.json")) as f:
            meta = json.load(f)
        return meta["median_inter_tick_dt_seconds_full_day"]
    raise ValueError(f"unknown domain {domain!r}")


def main():
    domain, variant = sys.argv[1], sys.argv[2]
    prefix = DOMAIN_PREFIX[domain]
    pre = np.load(os.path.join(DATA_DIR, f"{prefix}_pre_{variant}.npy"))
    post = np.load(os.path.join(DATA_DIR, f"{prefix}_post_{variant}.npy"))
    dt = load_dt(domain)

    print(f"[{domain}/{variant}] n_pre_raw={len(pre)} n_post_raw={len(post)} dt={dt}", flush=True)
    t0 = time.time()
    result = run_km_analysis(pre, post, dt=dt, seed=SEED)
    elapsed = time.time() - t0
    result["wall_clock_seconds"] = elapsed
    result["domain"] = domain
    result["variant"] = variant
    result["dt_used"] = dt

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"result_{domain}_{variant}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[{domain}/{variant}] DONE in {elapsed:.1f}s -> {out_path}", flush=True)
    print(f"[{domain}/{variant}] status={result['status']}", flush=True)
    if result["status"] == "ok":
        tme = result["tau_me_result"]
        print(f"[{domain}/{variant}] tau_ME: {tme['tau_me_samples']} samples "
              f"({tme['tau_me_time']}s), grid_index={tme['tau_me_grid_index']} "
              f"of {tme['n_grid_points']} candidates", flush=True)
        print(f"[{domain}/{variant}] PKS_pre={result['PKS_pre']} PKS_post={result['PKS_post']} "
              f"delta_PKS={result['delta_PKS']} p_PKS={result['p_PKS']}  <-- DECISION CHANNEL", flush=True)
        print(f"[{domain}/{variant}] beta_D2_pre={result['beta_D2_pre']} beta_D2_post={result['beta_D2_post']} "
              f"delta_beta_D2={result['delta_beta_D2']} p_beta_D2={result['p_beta_D2']}  (diagnostic only)", flush=True)
        print(f"[{domain}/{variant}] kappa_pre={result['kappa_pre']} kappa_post={result['kappa_post']} "
              f"delta_kappa={result['delta_kappa']}  (diagnostic only, never in any p-value)", flush=True)
    else:
        print(f"[{domain}/{variant}] tau_ME NOT established: {result['tau_me_result']}", flush=True)


if __name__ == "__main__":
    main()
