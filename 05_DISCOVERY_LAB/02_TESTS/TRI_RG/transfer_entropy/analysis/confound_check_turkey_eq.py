"""
MANDATORY adversarial reproduction / null-discovery check for the
Turkey earthquake domain, triggered by p<0.05 findings in
result_turkeyeq_primary.json (TE_net p=0.04 IAAFT; TE_sum p=0.005 IAAFT,
p=0.0 circular-shift; STE_sum p=0.0 IAAFT).

DISCOVERY made while inspecting the real data (not fabricated, not
hypothesized in advance): the GAZ (X) PRE-window RMS-bin series has a
smooth, large-amplitude, near-linear ramp occupying ~44% of the 24h PRE
window (bins ~303-719, i.e. the LAST ~10h before the M7.8), reaching
~1.96 million (RMS units) vs a background median of ~7300 -- a >250x
excursion. BNN (Y) shows NOTHING unusual at the same UTC times (flat,
~10,700). This is NOT consistent with a real regional seismic event
(which would appear, even if attenuated, at BOTH stations) -- it is
consistent with a station-specific instrumental transient (e.g. sensor
mass-recentering, common for broadband seismometers) close in time to
the interpolated data gaps already logged in
PROVENANCE_TURKEY_EARTHQUAKE.md (2023-02-05T11:55-11:57 UTC).

Runs 4 adversarial checks:
  (a) MANDATORY placebo split -- split the PRE window itself (no real
      transition at all) into two halves and test for spurious
      "significance". Because the discovered contamination sits in the
      SECOND half of PRE, this placebo split doubles as a direct probe
      of whether the artifact alone can produce a spurious "transition"
      signal.
  (b) Clean-PRE re-test -- rerun the REAL PRE-vs-POST test using ONLY
      the uncontaminated first ~10.1h of PRE (bins 0-302) instead of the
      full 24h PRE.
  (c) High-pass-filtered reproduction -- refetch the raw waveform,
      apply a standard detrend + 1Hz high-pass filter (removes the kind
      of slow instrumental drift that dominates raw-count RMS), rebin
      to RMS, and rerun the REAL PRE-vs-POST test on the filtered data.
  (d) POST early-window check -- does the "coupling" persist if we
      exclude vs. isolate the first 2h after the M7.8 (the biggest
      aftershock-energy burst)?

Writes confound_check_turkey_eq_results.json and prints a summary.
"""
import io
import json
import os
import sys
import time
import urllib.request

import numpy as np
import obspy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import te_common as te  # noqa: E402

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(ANALYSIS_DIR), "data")

FDSN_BASE = "https://service.iris.edu/fdsnws/dataselect/1/query"
NET, LOC, CHA = "KO", "--", "HHZ"
STA_X, STA_Y = "GAZ", "BNN"
PRE_START, PRE_END = "2023-02-05T01:17:34", "2023-02-06T01:17:34"
POST_START, POST_END = "2023-02-06T01:17:34", "2023-02-06T10:24:48"
BIN_WIDTH_S = 120.0
CONTAM_START_BIN = 303  # discovered contamination onset in PRE/X (t=606min=10.10h into PRE)


def load_npy(name):
    return np.load(os.path.join(DATA_DIR, name))


def fetch_mseed(sta, start, end, timeout=300, n_retries=4):
    url = (f"{FDSN_BASE}?net={NET}&sta={sta}&loc={LOC}&cha={CHA}"
           f"&start={start}&end={end}&format=miniseed")
    last_err = None
    for attempt in range(1, n_retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                raw = resp.read()
            return obspy.read(io.BytesIO(raw))
        except Exception as e:
            last_err = e
            print(f"    attempt {attempt}/{n_retries} failed: {e!r} -- retrying", flush=True)
    raise RuntimeError(f"fetch_mseed failed after {n_retries} attempts: {last_err!r}")


def load_filtered_rms(sta, start, end, label):
    st = fetch_mseed(sta, start, end)
    st.merge(method=1, fill_value="interpolate")
    assert len(st) == 1, f"[{label}] expected 1 trace after merge, got {len(st)}"
    tr = st[0]
    assert not np.ma.is_masked(tr.data), f"[{label}] masked samples remain"
    tr.detrend("linear")
    tr.filter("highpass", freq=1.0, corners=4, zerophase=True)
    fs = float(tr.stats.sampling_rate)
    n_per_bin = int(round(BIN_WIDTH_S * fs))
    data = tr.data.astype(float)
    n_bins = len(data) // n_per_bin
    trimmed = data[: n_bins * n_per_bin].reshape(n_bins, n_per_bin)
    rms = np.sqrt(np.mean(trimmed ** 2, axis=1))
    print(f"  [{label}] fs={fs}Hz n_bins={n_bins} (filtered highpass 1Hz)", flush=True)
    return rms


def summarize_result(res):
    if res["status"] != "ok":
        return {"status": res["status"]}
    return {
        "status": "ok",
        "delta": res["delta"],
        "p_iaaft": res["p_iaaft"],
        "p_circular_shift": res["p_circular_shift"],
    }


def main():
    out = {}

    pre_x = load_npy("turkeyeq_pre_x_primary.npy")
    pre_y = load_npy("turkeyeq_pre_y_primary.npy")
    post_x = load_npy("turkeyeq_post_x_primary.npy")
    post_y = load_npy("turkeyeq_post_y_primary.npy")

    # -------------------------------------------------------------
    # Diagnostic: document the contamination discovery quantitatively
    # -------------------------------------------------------------
    print("=== Diagnostic: PRE/X contamination ===", flush=True)
    clean_pre_x = pre_x[:CONTAM_START_BIN]
    contam_pre_x = pre_x[CONTAM_START_BIN:]
    clean_pre_y = pre_y[:CONTAM_START_BIN]
    contam_pre_y = pre_y[CONTAM_START_BIN:]
    diag = {
        "contam_start_bin": CONTAM_START_BIN,
        "pre_x_clean_median": float(np.median(clean_pre_x)),
        "pre_x_clean_max": float(np.max(clean_pre_x)),
        "pre_x_contam_median": float(np.median(contam_pre_x)),
        "pre_x_contam_max": float(np.max(contam_pre_x)),
        "pre_y_clean_median": float(np.median(clean_pre_y)),
        "pre_y_contam_median": float(np.median(contam_pre_y)),
        "pre_y_contam_max": float(np.max(contam_pre_y)),
        "interpretation": (
            "PRE/X (GAZ) median jumps from clean-region to contaminated-region "
            "by >100x while PRE/Y (BNN) stays flat across the same absolute time "
            "window -- station-specific artifact, not a real shared regional signal."
        ),
    }
    print(json.dumps(diag, indent=2), flush=True)
    out["diagnostic"] = diag

    # -------------------------------------------------------------
    # (a) MANDATORY placebo: split PRE itself, no real transition
    # -------------------------------------------------------------
    print("\n=== Check (a): placebo split within PRE (no real transition) ===", flush=True)
    n_pre = len(pre_x)
    half = n_pre // 2
    t0 = time.time()
    res_placebo = te.run_te_analysis(pre_x[:half], pre_y[:half], pre_x[half:], pre_y[half:])
    dt = time.time() - t0
    print(f"  status={res_placebo['status']} ({dt:.1f}s)", flush=True)
    if res_placebo["status"] == "ok":
        print(f"  delta={res_placebo['delta']}", flush=True)
        print(f"  p_iaaft={res_placebo['p_iaaft']}", flush=True)
        print(f"  p_circular_shift={res_placebo['p_circular_shift']}", flush=True)
    out["check_a_placebo_split"] = summarize_result(res_placebo)
    out["check_a_placebo_split"]["note"] = (
        "pseudo-PRE = PRE bins [0:360) (clean), pseudo-POST = PRE bins [360:720) "
        "(includes the contaminated region from bin 303 onward) -- NO real transition."
    )

    # -------------------------------------------------------------
    # (b) Clean-PRE re-test: real PRE truncated to exclude contamination
    # -------------------------------------------------------------
    print("\n=== Check (b): real PRE-vs-POST using ONLY the clean (uncontaminated) PRE ===", flush=True)
    t0 = time.time()
    res_clean_pre = te.run_te_analysis(clean_pre_x, clean_pre_y, post_x, post_y)
    dt = time.time() - t0
    print(f"  status={res_clean_pre['status']} ({dt:.1f}s)", flush=True)
    if res_clean_pre["status"] == "ok":
        print(f"  delta={res_clean_pre['delta']}", flush=True)
        print(f"  p_iaaft={res_clean_pre['p_iaaft']}", flush=True)
        print(f"  p_circular_shift={res_clean_pre['p_circular_shift']}", flush=True)
    out["check_b_clean_pre"] = summarize_result(res_clean_pre)
    out["check_b_clean_pre"]["note"] = f"PRE truncated to bins [0:{CONTAM_START_BIN}) only (~10.1h), POST unchanged (real)."

    # -------------------------------------------------------------
    # (c) High-pass-filtered reproduction (refetch + detrend + 1Hz HP filter)
    # -------------------------------------------------------------
    print("\n=== Check (c): high-pass-filtered (1Hz) reproduction, refetched from IRIS ===", flush=True)
    print("  fetching PRE/X filtered ...", flush=True)
    pre_x_filt = load_filtered_rms(STA_X, PRE_START, PRE_END, "PRE/X filtered")
    print("  fetching PRE/Y filtered ...", flush=True)
    pre_y_filt = load_filtered_rms(STA_Y, PRE_START, PRE_END, "PRE/Y filtered")
    print("  fetching POST/X filtered ...", flush=True)
    post_x_filt = load_filtered_rms(STA_X, POST_START, POST_END, "POST/X filtered")
    print("  fetching POST/Y filtered ...", flush=True)
    post_y_filt = load_filtered_rms(STA_Y, POST_START, POST_END, "POST/Y filtered")

    n_pre_f = min(len(pre_x_filt), len(pre_y_filt))
    n_post_f = min(len(post_x_filt), len(post_y_filt))
    pre_x_filt, pre_y_filt = pre_x_filt[:n_pre_f], pre_y_filt[:n_pre_f]
    post_x_filt, post_y_filt = post_x_filt[:n_post_f], post_y_filt[:n_post_f]

    print(f"  filtered PRE/X median={np.median(pre_x_filt):.1f} max={np.max(pre_x_filt):.1f} "
          f"(vs raw contaminated-region max ~1.96e6)", flush=True)

    t0 = time.time()
    res_filtered = te.run_te_analysis(pre_x_filt, pre_y_filt, post_x_filt, post_y_filt)
    dt = time.time() - t0
    print(f"  status={res_filtered['status']} ({dt:.1f}s)", flush=True)
    if res_filtered["status"] == "ok":
        print(f"  delta={res_filtered['delta']}", flush=True)
        print(f"  p_iaaft={res_filtered['p_iaaft']}", flush=True)
        print(f"  p_circular_shift={res_filtered['p_circular_shift']}", flush=True)
    out["check_c_highpass_filtered"] = summarize_result(res_filtered)
    out["check_c_highpass_filtered"]["note"] = (
        "detrend(linear) + highpass(1Hz, 4 corners, zerophase) applied to raw waveform "
        "BEFORE RMS binning, both channels, both PRE and POST, refetched from IRIS."
    )
    out["check_c_highpass_filtered"]["pre_x_filtered_median"] = float(np.median(pre_x_filt))
    out["check_c_highpass_filtered"]["pre_x_filtered_max"] = float(np.max(pre_x_filt))

    # -------------------------------------------------------------
    # (d) POST early-window check
    # -------------------------------------------------------------
    print("\n=== Check (d): POST early-burst isolation/exclusion ===", flush=True)
    early_bins = 60  # first 2h after M7.8
    post_x_early, post_y_early = post_x[:early_bins], post_y[:early_bins]
    post_x_late, post_y_late = post_x[early_bins:], post_y[early_bins:]

    t0 = time.time()
    res_early = te.run_te_analysis(pre_x, pre_y, post_x_early, post_y_early)
    dt = time.time() - t0
    print(f"  early-only (first 2h of POST): status={res_early['status']} ({dt:.1f}s)", flush=True)
    if res_early["status"] == "ok":
        print(f"    delta={res_early['delta']}", flush=True)
        print(f"    p_iaaft={res_early['p_iaaft']}", flush=True)
        print(f"    p_circular_shift={res_early['p_circular_shift']}", flush=True)
    out["check_d_post_early_only"] = summarize_result(res_early)

    t0 = time.time()
    res_late = te.run_te_analysis(pre_x, pre_y, post_x_late, post_y_late)
    dt = time.time() - t0
    print(f"  excluding first 2h of POST: status={res_late['status']} ({dt:.1f}s)", flush=True)
    if res_late["status"] == "ok":
        print(f"    delta={res_late['delta']}", flush=True)
        print(f"    p_iaaft={res_late['p_iaaft']}", flush=True)
        print(f"    p_circular_shift={res_late['p_circular_shift']}", flush=True)
    out["check_d_post_excluding_early"] = summarize_result(res_late)

    with open(os.path.join(ANALYSIS_DIR, "confound_check_turkey_eq_results.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\nWrote confound_check_turkey_eq_results.json", flush=True)


if __name__ == "__main__":
    main()
