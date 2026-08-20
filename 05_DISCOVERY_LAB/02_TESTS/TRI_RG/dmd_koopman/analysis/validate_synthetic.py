"""
Mandatory synthetic validation for `dmd_koopman`, run BEFORE any real
data is touched (METHODOLOGY_NOTE.md section 4).

Runs, in order:
  0. Code-correctness diagnostic: pure sinusoid -> expect a recovered
     complex-conjugate pair with |lambda|~=1 (undamped), f_dom~=f0.
  1. Positive control: noisy Stuart-Landau oscillator, PRE = stable focus
     (mu<0), POST = limit cycle (mu>0) -- tests whether f_dom/zeta show
     real discriminative power under IAAFT.
  2. Negative control: two independent realizations of the SAME
     (non-bifurcating) Stuart-Landau process (mu_pre=mu_post<0).
  3. If (1) fails by low power (not structural non-computability): the
     ONE pre-authorized correction (sigma: 0.05 -> 0.15) is applied and
     (1)+(2) are re-run once. No further attempts.

Writes validation_synthetic.json with the full result set.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmd_common import run_dmd_analysis, compute_dmd_features, estimate_d, SEED

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rqa", "analysis")
)
from rqa_common import estimate_tau  # noqa: E402

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")

N_MC_VALIDATION = 200  # same N_SURROGATES as the locked pipeline


# ==========================================================================
# 0. Code-correctness diagnostic: pure sinusoid
# ==========================================================================

def diagnostic_sinusoid():
    n = 2000
    f0 = 0.05  # cycles/sample, period 20 samples
    t = np.arange(n)
    rng = np.random.default_rng(1)
    x = np.sin(2 * np.pi * f0 * t) + 1e-6 * rng.standard_normal(n)

    tau_info = estimate_tau(x)
    tau = tau_info["tau"]
    d_info = estimate_d(n, tau)
    d = d_info["d"]

    feat = compute_dmd_features(x, d, tau)
    return {
        "n": n, "f0_true": f0, "tau_info": tau_info, "d_info": d_info,
        "feat": {k: v for k, v in feat.items() if k not in ("prep_info",)},
    }


# ==========================================================================
# 1/2. Stuart-Landau simulator (Euler-Maruyama)
# ==========================================================================

def simulate_stuart_landau(mu, omega, sigma, n_keep, dt_internal=0.01, decimate=10,
                            transient_steps=2000, seed=0):
    """Noisy Stuart-Landau oscillator:
      dx = (mu*x - omega*y - (x^2+y^2)*x) dt + sigma*dW_x
      dy = (mu*y + omega*x - (x^2+y^2)*y) dt + sigma*dW_y
    Returns the scalar observable x(t), subsampled every `decimate` internal
    steps, AFTER discarding `transient_steps` internal steps, length n_keep
    (in decimated/sample units).
    """
    rng = np.random.default_rng(seed)
    sqrt_dt = np.sqrt(dt_internal)
    n_internal = transient_steps + n_keep * decimate

    x, y = 0.1, 0.0
    xs = np.empty(n_internal + 1)
    ys = np.empty(n_internal + 1)
    xs[0], ys[0] = x, y
    for i in range(1, n_internal + 1):
        r2 = x * x + y * y
        dx = (mu * x - omega * y - r2 * x) * dt_internal + sigma * sqrt_dt * rng.standard_normal()
        dy = (mu * y + omega * x - r2 * y) * dt_internal + sigma * sqrt_dt * rng.standard_normal()
        x, y = x + dx, y + dy
        xs[i], ys[i] = x, y

    x_post_transient = xs[transient_steps + 1:]
    x_decimated = x_post_transient[::decimate][:n_keep]
    return x_decimated


OMEGA = 1.0
SIGMA_V1 = 0.05
MU_PRE = -0.3
MU_POST = 0.3
N_KEEP = 4000
DT_INTERNAL = 0.01
DECIMATE = 10
TRANSIENT = 2000


def run_positive_control(sigma, label):
    pre = simulate_stuart_landau(MU_PRE, OMEGA, sigma, N_KEEP, dt_internal=DT_INTERNAL,
                                  decimate=DECIMATE, transient_steps=TRANSIENT, seed=101)
    post = simulate_stuart_landau(MU_POST, OMEGA, sigma, N_KEEP, dt_internal=DT_INTERNAL,
                                   decimate=DECIMATE, transient_steps=TRANSIENT, seed=202)
    t0 = time.time()
    result = run_dmd_analysis(pre, post, seed=SEED, n_mc=N_MC_VALIDATION)
    elapsed = time.time() - t0
    return {"label": label, "sigma": sigma, "mu_pre": MU_PRE, "mu_post": MU_POST,
            "omega": OMEGA, "n_keep": N_KEEP, "wall_clock_seconds": elapsed,
            "result": result}


def run_negative_control(sigma, label):
    pre = simulate_stuart_landau(MU_PRE, OMEGA, sigma, N_KEEP, dt_internal=DT_INTERNAL,
                                  decimate=DECIMATE, transient_steps=TRANSIENT, seed=303)
    post = simulate_stuart_landau(MU_PRE, OMEGA, sigma, N_KEEP, dt_internal=DT_INTERNAL,
                                   decimate=DECIMATE, transient_steps=TRANSIENT, seed=404)
    t0 = time.time()
    result = run_dmd_analysis(pre, post, seed=SEED, n_mc=N_MC_VALIDATION)
    elapsed = time.time() - t0
    return {"label": label, "sigma": sigma, "mu_pre": MU_PRE, "mu_post": MU_PRE,
            "omega": OMEGA, "n_keep": N_KEEP, "wall_clock_seconds": elapsed,
            "result": result}


def _strip_heavy(result):
    """Drop bulky per-surrogate/intermediate objects not needed for the
    JSON report (keeps top-level scalars, p-values, config, diagnostics)."""
    if result is None:
        return None
    keep_keys = [
        "status", "tau", "d", "delta_f_dom", "delta_zeta", "delta_spectral_gap",
        "delta_real_dominant_rate", "p_f_dom", "p_zeta", "p_spectral_gap",
        "f_dom_pre", "f_dom_post", "zeta_pre", "zeta_post",
        "spectral_gap_pre", "spectral_gap_post",
        "real_dominant_rate_pre", "real_dominant_rate_post",
        "surrogate_f_dom_mean", "surrogate_f_dom_std", "surrogate_f_dom_n_valid",
        "surrogate_f_dom_n_undefined",
        "surrogate_zeta_mean", "surrogate_zeta_std", "surrogate_zeta_n_valid",
        "surrogate_zeta_n_undefined",
        "surrogate_gap_mean", "surrogate_gap_std", "surrogate_gap_n_valid",
        "surrogate_gap_n_undefined",
        "diagnostics", "config", "tau_info", "d_info",
    ]
    out = {}
    for k in keep_keys:
        if k in result:
            v = result[k]
            if k in ("tau_info",) and isinstance(v, dict):
                v = {kk: vv for kk, vv in v.items() if kk != "mi_curve"}
            out[k] = v
    # real_pre/real_post: keep only status + rank_info + primary/real-diag statuses
    for side in ("real_pre", "real_post"):
        r = result.get(side)
        if isinstance(r, dict):
            out[side] = {
                "status": r.get("status"), "rank_info": r.get("rank_info"),
                "n_complex_pairs": r.get("n_complex_pairs"), "n_real_modes": r.get("n_real_modes"),
                "primary_status": r.get("primary_status"),
                "real_diagnostic_status": r.get("real_diagnostic_status"),
                "reconstruction_residual": r.get("reconstruction_residual"),
            }
    return out


def main():
    print("=== 0. Code-correctness diagnostic: pure sinusoid ===", flush=True)
    diag0 = diagnostic_sinusoid()
    print(json.dumps({k: v for k, v in diag0["feat"].items()
                       if k in ("status", "f_dom", "zeta", "spectral_gap",
                                 "real_dominant_rate", "n_complex_pairs", "n_real_modes")},
                      indent=2), flush=True)

    print("\n=== 1. Positive control v1 (sigma=0.05) ===", flush=True)
    pos_v1 = run_positive_control(SIGMA_V1, "positive_control_v1")
    print(f"p_f_dom={pos_v1['result'].get('p_f_dom')} "
          f"p_zeta={pos_v1['result'].get('p_zeta')} "
          f"p_spectral_gap={pos_v1['result'].get('p_spectral_gap')}", flush=True)
    print(f"delta_f_dom={pos_v1['result'].get('delta_f_dom')} "
          f"delta_zeta={pos_v1['result'].get('delta_zeta')}", flush=True)
    print(f"real_pre status={pos_v1['result']['real_pre']['status']} "
          f"n_complex_pairs={pos_v1['result']['real_pre'].get('n_complex_pairs')} "
          f"real_post status={pos_v1['result']['real_post']['status']} "
          f"n_complex_pairs={pos_v1['result']['real_post'].get('n_complex_pairs')}", flush=True)

    print("\n=== 2. Negative control (sigma=0.05) ===", flush=True)
    neg_v1 = run_negative_control(SIGMA_V1, "negative_control_v1")
    print(f"p_f_dom={neg_v1['result'].get('p_f_dom')} "
          f"p_zeta={neg_v1['result'].get('p_zeta')} "
          f"p_spectral_gap={neg_v1['result'].get('p_spectral_gap')}", flush=True)

    def _passes(res):
        r = res["result"]
        if r["status"] != "ok":
            return False
        for key in ("p_f_dom", "p_zeta"):
            p = r.get(key)
            if p is not None and p < 0.05:
                return True
        return False

    v1_passes = _passes(pos_v1)

    correction_applied = False
    pos_v2 = None
    neg_v2 = None

    structural_failure = (pos_v1["result"]["status"] != "ok") or \
        (pos_v1["result"]["real_pre"]["status"] != "ok") or \
        (pos_v1["result"]["real_post"]["status"] != "ok")

    if not v1_passes and not structural_failure:
        print("\n=== v1 did not show power; applying the ONE pre-authorized "
              "correction (sigma: 0.05 -> 0.15) ===", flush=True)
        correction_applied = True
        SIGMA_V2 = 0.15
        pos_v2 = run_positive_control(SIGMA_V2, "positive_control_v2_sigma0.15")
        print(f"[v2] p_f_dom={pos_v2['result'].get('p_f_dom')} "
              f"p_zeta={pos_v2['result'].get('p_zeta')} "
              f"p_spectral_gap={pos_v2['result'].get('p_spectral_gap')}", flush=True)
        neg_v2 = run_negative_control(SIGMA_V2, "negative_control_v2_sigma0.15")
        print(f"[v2 neg] p_f_dom={neg_v2['result'].get('p_f_dom')} "
              f"p_zeta={neg_v2['result'].get('p_zeta')} "
              f"p_spectral_gap={neg_v2['result'].get('p_spectral_gap')}", flush=True)
        v2_passes = _passes(pos_v2)
    else:
        v2_passes = None

    final_pass = v1_passes or (v2_passes is True)

    report = {
        "diagnostic_0_sinusoid": diag0,
        "positive_control_v1": {**pos_v1, "result": _strip_heavy(pos_v1["result"])},
        "negative_control_v1": {**neg_v1, "result": _strip_heavy(neg_v1["result"])},
        "correction_applied": correction_applied,
        "positive_control_v2": (
            {**pos_v2, "result": _strip_heavy(pos_v2["result"])} if pos_v2 else None
        ),
        "negative_control_v2": (
            {**neg_v2, "result": _strip_heavy(neg_v2["result"])} if neg_v2 else None
        ),
        "v1_passes": v1_passes,
        "structural_failure_v1": structural_failure,
        "v2_passes": v2_passes,
        "final_verdict": "PASS" if final_pass else "FAIL_CLOSE_AT_VALIDATION",
    }

    with open(OUT_PATH, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nWrote {OUT_PATH}", flush=True)
    print(f"FINAL VERDICT: {report['final_verdict']}", flush=True)


if __name__ == "__main__":
    main()
