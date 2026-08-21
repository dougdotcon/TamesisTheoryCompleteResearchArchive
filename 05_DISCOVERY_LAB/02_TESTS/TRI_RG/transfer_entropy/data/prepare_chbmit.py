"""
Download and prepare PRE/POST paired bivariate segments (primary +
robustness) for the CHB-MIT Scalp EEG Database, subject chb01,
`chb01_03.edf`, channels FP1-F7 (frontal) and T7-P7 (temporal), seizure
onset transition (t=2996s within the file), per ../METHODOLOGY_NOTE.md
domain 1. Real data only, fetched directly from the public PhysioNet
Open Data server (no login/token), no fabrication.

Single-file design (chb01_03.edf only, NOT extended into chb01_04.edf) --
decision and rationale in METHODOLOGY_NOTE.md ("Escolha de desenho").

Writes (into this same data/ directory):
  chbmit_pre_x_primary.npy,  chbmit_pre_y_primary.npy,
  chbmit_post_x_primary.npy, chbmit_post_y_primary.npy,
  chbmit_pre_x_robust.npy,   chbmit_pre_y_robust.npy,
  chbmit_post_x_robust.npy,  chbmit_post_y_robust.npy,
  chbmit_segments_meta.json
X = FP1-F7 (frontal), Y = T7-P7 (temporal) -- consistent labeling used
throughout analysis/result_chbmit_*.json.
"""
import io
import json
import os
import urllib.request

import numpy as np
import pyedflib

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://physionet.org/files/chbmit/1.0.0/chb01/chb01_03.edf"
SUMMARY_URL = "https://physionet.org/files/chbmit/1.0.0/chb01/chb01-summary.txt"

CHAN_X = "FP1-F7"
CHAN_Y = "T7-P7"
SEIZURE_START_S = 2996
SEIZURE_END_S = 3036
FILE_DURATION_S = 3600  # confirmed 13:43:04 -> 14:43:04 in chb01-summary.txt


def fetch_bytes(url, timeout=300):
    print(f"  fetching {url}", flush=True)
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        raw = resp.read()
    print(f"    {len(raw)} bytes", flush=True)
    return raw


def main():
    summary_raw = fetch_bytes(SUMMARY_URL, timeout=60).decode("utf-8", errors="replace")
    assert "chb01_03.edf" in summary_raw
    assert "Seizure Start Time: 2996 seconds" in summary_raw
    assert "Seizure End Time: 3036 seconds" in summary_raw
    print("  chb01-summary.txt confirms seizure window [2996s,3036s] for chb01_03.edf", flush=True)

    edf_raw = fetch_bytes(BASE_URL)
    tmp_path = os.path.join(OUT_DIR, "_chb01_03_tmp.edf")
    with open(tmp_path, "wb") as f:
        f.write(edf_raw)

    f = pyedflib.EdfReader(tmp_path)
    labels = f.getSignalLabels()
    assert CHAN_X in labels, f"{CHAN_X} not found in {labels}"
    assert CHAN_Y in labels, f"{CHAN_Y} not found in {labels}"
    idx_x = labels.index(CHAN_X)
    idx_y = labels.index(CHAN_Y)
    fs_x = f.getSampleFrequency(idx_x)
    fs_y = f.getSampleFrequency(idx_y)
    assert fs_x == fs_y, f"sampling rate mismatch: X={fs_x} Y={fs_y}"
    fs = float(fs_x)
    n_samples_x = f.getNSamples()[idx_x]
    n_samples_y = f.getNSamples()[idx_y]
    x_full = f.readSignal(idx_x)
    y_full = f.readSignal(idx_y)
    f.close()
    os.remove(tmp_path)

    print(f"  fs={fs}Hz  n_samples X={n_samples_x} Y={n_samples_y}  "
          f"duration={n_samples_x/fs:.1f}s", flush=True)
    assert abs(n_samples_x / fs - FILE_DURATION_S) < 5, "file duration does not match summary (~3600s)"

    onset_idx = int(round(SEIZURE_START_S * fs))

    pre_x_primary = x_full[:onset_idx]
    pre_y_primary = y_full[:onset_idx]
    post_x_primary = x_full[onset_idx:]
    post_y_primary = y_full[onset_idx:]

    n_pre = len(pre_x_primary)
    n_post = len(post_x_primary)

    pre_x_robust = pre_x_primary[n_pre // 2:]
    pre_y_robust = pre_y_primary[n_pre // 2:]
    post_x_robust = post_x_primary[: n_post // 2]
    post_y_robust = post_y_primary[: n_post // 2]

    print(f"PRE primary n={n_pre} ({n_pre/fs:.1f}s)  POST primary n={n_post} ({n_post/fs:.1f}s)", flush=True)
    print(f"PRE robust n={len(pre_x_robust)} ({len(pre_x_robust)/fs:.1f}s)  "
          f"POST robust n={len(post_x_robust)} ({len(post_x_robust)/fs:.1f}s)", flush=True)

    np.save(os.path.join(OUT_DIR, "chbmit_pre_x_primary.npy"), pre_x_primary)
    np.save(os.path.join(OUT_DIR, "chbmit_pre_y_primary.npy"), pre_y_primary)
    np.save(os.path.join(OUT_DIR, "chbmit_post_x_primary.npy"), post_x_primary)
    np.save(os.path.join(OUT_DIR, "chbmit_post_y_primary.npy"), post_y_primary)
    np.save(os.path.join(OUT_DIR, "chbmit_pre_x_robust.npy"), pre_x_robust)
    np.save(os.path.join(OUT_DIR, "chbmit_pre_y_robust.npy"), pre_y_robust)
    np.save(os.path.join(OUT_DIR, "chbmit_post_x_robust.npy"), post_x_robust)
    np.save(os.path.join(OUT_DIR, "chbmit_post_y_robust.npy"), post_y_robust)

    meta = {
        "source": "PhysioNet CHB-MIT Scalp EEG Database v1.0.0",
        "url": BASE_URL,
        "subject": "chb01", "file": "chb01_03.edf",
        "channel_x": CHAN_X, "channel_y": CHAN_Y,
        "fs_hz": fs, "dt_s": 1.0 / fs,
        "n_samples_x_full": int(n_samples_x), "n_samples_y_full": int(n_samples_y),
        "seizure_start_s": SEIZURE_START_S, "seizure_end_s": SEIZURE_END_S,
        "onset_sample_index": int(onset_idx),
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_x_robust)), "post_robust_n": int(len(post_x_robust)),
        "pre_primary_duration_s": n_pre / fs, "post_primary_duration_s": n_post / fs,
        "montage": "bipolar (native EDF channel pairs, not re-derived)",
        "single_file_design": True,
        "single_file_design_rationale": (
            "chb01_03.edf only, NOT extended into chb01_04.edf -- avoids assuming "
            "gap-free continuity across separately recorded EDF files and avoids "
            "mixing two distinct seizure episodes into one POST condition; see "
            "METHODOLOGY_NOTE.md 'Escolha de desenho'."
        ),
    }
    with open(os.path.join(OUT_DIR, "chbmit_segments_meta.json"), "w") as fjson:
        json.dump(meta, fjson, indent=2)
    print("Wrote chbmit_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
