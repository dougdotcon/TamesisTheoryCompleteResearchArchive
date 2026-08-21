"""
Download and prepare PRE/POST paired bivariate segments (primary +
robustness) for the Kahramanmaras, Turkey earthquake doublet
(2023-02-06), stations KO.GAZ..HHZ and KO.BNN..HHZ, per
../METHODOLOGY_NOTE.md domain 2. Real data only, fetched directly from
the public IRIS/EarthScope FDSN dataselect web service (no login/token),
no fabrication.

MANDATORY coarse-graining (METHODOLOGY_NOTE.md, avoids the exact
Kilauea/dmd_koopman shared-wave-propagation artifact risk): raw 100Hz
waveform is NEVER fed to the TE estimator. Instead, RMS amplitude in
fixed, non-overlapping BIN_WIDTH_S=120s (2min) bins is computed HERE,
BEFORE saving -- the .npy files already contain the coarse-grained
energy-rate series, not raw waveform.

Transition (USGS event catalog, external): M7.8 Pazarcik,
2023-02-06T01:17:34Z. Next documented event (POST boundary): M7.5
Elbistan, 2023-02-06T10:24:48Z.

Writes (into this same data/ directory):
  turkeyeq_pre_x_primary.npy,  turkeyeq_pre_y_primary.npy,
  turkeyeq_post_x_primary.npy, turkeyeq_post_y_primary.npy,
  turkeyeq_pre_x_robust.npy,   turkeyeq_pre_y_robust.npy,
  turkeyeq_post_x_robust.npy,  turkeyeq_post_y_robust.npy,
  turkeyeq_segments_meta.json
X = GAZ (Gaziantep, ~20km from M7.8 epicenter), Y = BNN (Kayseri,
~230km away). Raw miniseed downloads are NOT saved (see
PROVENANCE_TURKEY_EARTHQUAKE.md).
"""
import io
import json
import os
import urllib.request

import numpy as np
import obspy

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FDSN_BASE = "https://service.iris.edu/fdsnws/dataselect/1/query"
NET, LOC, CHA = "KO", "--", "HHZ"
STA_X = "GAZ"
STA_Y = "BNN"

M78_UTC = "2023-02-06T01:17:34"
M75_UTC = "2023-02-06T10:24:48"

PRE_START = "2023-02-05T01:17:34"
PRE_END = M78_UTC
POST_START = M78_UTC
POST_END = M75_UTC

BIN_WIDTH_S = 120.0  # fixed a priori, METHODOLOGY_NOTE.md


def fetch_mseed(sta, start, end, timeout=300, n_retries=4):
    url = (f"{FDSN_BASE}?net={NET}&sta={sta}&loc={LOC}&cha={CHA}"
           f"&start={start}&end={end}&format=miniseed")
    print(f"  fetching {url}", flush=True)
    last_err = None
    for attempt in range(1, n_retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                raw = resp.read()
            print(f"    {len(raw)} bytes (attempt {attempt})", flush=True)
            return obspy.read(io.BytesIO(raw))
        except Exception as e:
            last_err = e
            print(f"    attempt {attempt}/{n_retries} failed: {e!r} -- retrying", flush=True)
    raise RuntimeError(f"fetch_mseed failed after {n_retries} attempts: {last_err!r}")


def load_window(sta, start, end, label):
    st = fetch_mseed(sta, start, end)
    n_traces_raw = len(st)
    gaps_before = st.get_gaps()
    # Real, small data gaps (order of seconds, out of a 24h/9h window) are
    # filled by LINEAR INTERPOLATION rather than rejected -- standard
    # seismology practice for minor short gaps, and honest: recorded
    # explicitly in provenance metadata below, not silently ignored.
    st.merge(method=1, fill_value="interpolate")
    if len(st) != 1:
        raise RuntimeError(f"[{label}/{sta}] expected a single trace after interpolating merge, "
                            f"got {len(st)} trace(s)")
    tr = st[0]
    is_masked = np.ma.is_masked(tr.data)
    print(f"  [{label}/{sta}] {n_traces_raw} raw trace(s), {len(gaps_before)} gap(s) before merge "
          f"(filled by interpolation), masked_after_merge={is_masked}", flush=True)
    if is_masked:
        raise RuntimeError(f"[{label}/{sta}] still has masked (unfilled) samples after interpolating merge")
    return tr, n_traces_raw, gaps_before


def rms_bin(trace_data, fs, bin_width_s):
    """Non-overlapping RMS-amplitude bins of width bin_width_s seconds."""
    n_per_bin = int(round(bin_width_s * fs))
    n_bins = len(trace_data) // n_per_bin
    if n_bins < 1:
        return np.array([], dtype=float)
    trimmed = trace_data[: n_bins * n_per_bin].astype(float).reshape(n_bins, n_per_bin)
    return np.sqrt(np.mean(trimmed ** 2, axis=1))


def main():
    print("Fetching PRE window (X=GAZ, Y=BNN) ...", flush=True)
    tr_pre_x, ntr_pre_x, gaps_pre_x = load_window(STA_X, PRE_START, PRE_END, "PRE/X")
    tr_pre_y, ntr_pre_y, gaps_pre_y = load_window(STA_Y, PRE_START, PRE_END, "PRE/Y")
    print("Fetching POST window (X=GAZ, Y=BNN) ...", flush=True)
    tr_post_x, ntr_post_x, gaps_post_x = load_window(STA_X, POST_START, POST_END, "POST/X")
    tr_post_y, ntr_post_y, gaps_post_y = load_window(STA_Y, POST_START, POST_END, "POST/Y")

    fs_x_pre, fs_y_pre = tr_pre_x.stats.sampling_rate, tr_pre_y.stats.sampling_rate
    fs_x_post, fs_y_post = tr_post_x.stats.sampling_rate, tr_post_y.stats.sampling_rate
    assert fs_x_pre == fs_y_pre == fs_x_post == fs_y_post, "sampling rate mismatch across traces"
    fs = float(fs_x_pre)
    print(f"fs={fs}Hz for all 4 traces", flush=True)

    rms_pre_x = rms_bin(tr_pre_x.data, fs, BIN_WIDTH_S)
    rms_pre_y = rms_bin(tr_pre_y.data, fs, BIN_WIDTH_S)
    rms_post_x = rms_bin(tr_post_x.data, fs, BIN_WIDTH_S)
    rms_post_y = rms_bin(tr_post_y.data, fs, BIN_WIDTH_S)

    n_pre = min(len(rms_pre_x), len(rms_pre_y))
    n_post = min(len(rms_post_x), len(rms_post_y))
    pre_x_primary, pre_y_primary = rms_pre_x[:n_pre], rms_pre_y[:n_pre]
    post_x_primary, post_y_primary = rms_post_x[:n_post], rms_post_y[:n_post]

    pre_x_robust = pre_x_primary[n_pre // 2:]
    pre_y_robust = pre_y_primary[n_pre // 2:]
    post_x_robust = post_x_primary[: n_post // 2]
    post_y_robust = post_y_primary[: n_post // 2]

    print(f"PRE primary n_bins={n_pre} ({n_pre*BIN_WIDTH_S/3600:.2f}h)  "
          f"POST primary n_bins={n_post} ({n_post*BIN_WIDTH_S/3600:.2f}h)", flush=True)
    print(f"PRE robust n_bins={len(pre_x_robust)}  POST robust n_bins={len(post_x_robust)}", flush=True)
    assert n_pre > 10 and n_post > 10, "too few RMS bins -- refusing to proceed silently"

    np.save(os.path.join(OUT_DIR, "turkeyeq_pre_x_primary.npy"), pre_x_primary)
    np.save(os.path.join(OUT_DIR, "turkeyeq_pre_y_primary.npy"), pre_y_primary)
    np.save(os.path.join(OUT_DIR, "turkeyeq_post_x_primary.npy"), post_x_primary)
    np.save(os.path.join(OUT_DIR, "turkeyeq_post_y_primary.npy"), post_y_primary)
    np.save(os.path.join(OUT_DIR, "turkeyeq_pre_x_robust.npy"), pre_x_robust)
    np.save(os.path.join(OUT_DIR, "turkeyeq_pre_y_robust.npy"), pre_y_robust)
    np.save(os.path.join(OUT_DIR, "turkeyeq_post_x_robust.npy"), post_x_robust)
    np.save(os.path.join(OUT_DIR, "turkeyeq_post_y_robust.npy"), post_y_robust)

    meta = {
        "source": "IRIS/EarthScope FDSN dataselect web service",
        "network": NET, "station_x": STA_X, "station_y": STA_Y, "location": LOC, "channel": CHA,
        "fs_hz_raw": fs, "dt_s_raw": 1.0 / fs,
        "bin_width_s": BIN_WIDTH_S,
        "coarse_graining": "RMS amplitude, non-overlapping bins, computed BEFORE saving (raw waveform never fed to TE)",
        "gap_filling": "small real data gaps (order of seconds) filled by linear interpolation via obspy Stream.merge(method=1, fill_value='interpolate') before RMS binning",
        "n_gaps_pre_x": len(gaps_pre_x), "n_gaps_pre_y": len(gaps_pre_y),
        "n_gaps_post_x": len(gaps_post_x), "n_gaps_post_y": len(gaps_post_y),
        "m78_utc": M78_UTC + "Z", "m75_utc": M75_UTC + "Z",
        "m78_description": "M7.8 Pazarcik mainshock (USGS)",
        "m75_description": "M7.5 Elbistan second mainshock, ~9.12h later (USGS)",
        "pre_window_utc": [PRE_START + "Z", PRE_END + "Z"],
        "post_window_utc": [POST_START + "Z", POST_END + "Z"],
        "pre_trace_x_starttime": str(tr_pre_x.stats.starttime), "pre_trace_x_endtime": str(tr_pre_x.stats.endtime),
        "pre_trace_y_starttime": str(tr_pre_y.stats.starttime), "pre_trace_y_endtime": str(tr_pre_y.stats.endtime),
        "post_trace_x_starttime": str(tr_post_x.stats.starttime), "post_trace_x_endtime": str(tr_post_x.stats.endtime),
        "post_trace_y_starttime": str(tr_post_y.stats.starttime), "post_trace_y_endtime": str(tr_post_y.stats.endtime),
        "pre_primary_n_bins": int(n_pre), "post_primary_n_bins": int(n_post),
        "pre_robust_n_bins": int(len(pre_x_robust)), "post_robust_n_bins": int(len(post_x_robust)),
        "pre_primary_duration_h": n_pre * BIN_WIDTH_S / 3600.0,
        "post_primary_duration_h": n_post * BIN_WIDTH_S / 3600.0,
    }
    with open(os.path.join(OUT_DIR, "turkeyeq_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote turkeyeq_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
