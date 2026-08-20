"""
Download and prepare PRE/POST ankle-vertical-acceleration segments
(primary + robustness) for the Daphnet Freezing-of-Gait dataset, subject
`S01R01`, per ../METHODOLOGY_NOTE.md Gap (c), Domain 1. Real data only,
fetched directly from the public UCI ML Repository archive (no
login/token), no fabrication.

Source: UCI ML Repository, "Daphnet Freezing of Gait Dataset"
  https://archive.ics.uci.edu/ml/machine-learning-databases/00245/dataset_fog_release.zip
Record used: dataset_fog_release/dataset/S01R01.txt (fs=64Hz, 11 columns,
tab/space-separated): col0=time_ms, col1-3=ankle accel (fwd/vertical/
lateral, mg), col4-6=thigh accel, col7-9=trunk accel, col10=annotation
(0=out-of-protocol, 1=walking/no-freeze, 2=freeze), per
dataset_fog_release/doc/documentation.html (re-verified directly in this
session, not assumed from memory).

Channel used (Gap (c), Bachlin et al. 2010's primary sensor/axis for the
freeze-index algorithm): ankle vertical acceleration = column index 2
(0-indexed), i.e. the 3rd column of the file.

Transition (Gap (c), fixed a priori): onset of the FIRST video-annotated
freeze episode (label transitions 1->2), used as the PRE/POST boundary.
PRE = full continuous record from the start of the file to this onset
(mixed out-of-protocol/walking labels, no intra-segment filtering by
label -- the label only delimits the PRE/POST boundary, per this line's
established convention). POST = full continuous record from this onset
to the end of the file (necessarily contains 17 further freeze episodes
plus intervening walking -- reported honestly as "post-freeze-onset
regime", not "a single isolated freeze episode").

Writes (into this same data/ directory):
  daphnet_pre_primary.npy, daphnet_post_primary.npy,
  daphnet_pre_robust.npy, daphnet_post_robust.npy,
  daphnet_segments_meta.json
Raw download (dataset_fog_release.zip, ~21MB) is NOT committed to the
repo -- see ../data/PROVENANCE_DAPHNET.md for exact URL/reproduction
steps.
"""
import io
import json
import os
import zipfile

import numpy as np
import urllib.request

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00245/dataset_fog_release.zip"
ZIP_MEMBER = "dataset_fog_release/dataset/S01R01.txt"
FS_HZ = 64.0
CHANNEL_INDEX = 2  # ankle vertical acceleration (0-indexed column of the 11-column file)


def main():
    print(f"Fetching {URL} ...", flush=True)
    with urllib.request.urlopen(URL, timeout=180) as resp:
        raw_zip = resp.read()
    print(f"  downloaded {len(raw_zip)} bytes", flush=True)

    with zipfile.ZipFile(io.BytesIO(raw_zip)) as zf:
        with zf.open(ZIP_MEMBER) as f:
            data = np.loadtxt(f)

    print(f"  {ZIP_MEMBER}: shape={data.shape}", flush=True)
    assert data.shape[1] == 11, f"unexpected column count: {data.shape[1]}"

    labels = data[:, 10].astype(int)
    unique_labels, label_counts = np.unique(labels, return_counts=True)
    print(f"  unique labels: {dict(zip(unique_labels.tolist(), label_counts.tolist()))}", flush=True)

    is_freeze = (labels == 2).astype(int)
    transitions = np.diff(is_freeze)
    onsets = np.where(transitions == 1)[0] + 1
    offsets = np.where(transitions == -1)[0] + 1
    print(f"  n freeze episodes (label==2 contiguous runs): {len(onsets)}", flush=True)
    assert len(onsets) >= 1, "no freeze episode found in S01R01 -- cannot proceed without fabricating a transition"

    onset = int(onsets[0])
    print(f"  first freeze onset: sample={onset} (t={data[onset,0]/1000.0:.3f}s, "
          f"label[onset-1]={labels[onset-1]}, label[onset]={labels[onset]})", flush=True)

    channel_name = "ankle_vertical_accel_mg"
    full_signal = data[:, CHANNEL_INDEX].astype(float)
    assert not np.isnan(full_signal).any(), "unexpected NaN in raw Daphnet signal -- refusing to proceed"

    n_total = len(full_signal)
    pre_primary = full_signal[:onset]
    post_primary = full_signal[onset:]
    n_pre, n_post = len(pre_primary), len(post_primary)

    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

    print(f"PRE primary n={n_pre} ({n_pre/FS_HZ:.2f}s)  POST primary n={n_post} ({n_post/FS_HZ:.2f}s)", flush=True)
    print(f"PRE robust n={len(pre_robust)}  POST robust n={len(post_robust)}", flush=True)
    assert n_pre > 0 and n_post > 0
    assert n_pre + n_post == n_total

    np.save(os.path.join(OUT_DIR, "daphnet_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "daphnet_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "daphnet_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "daphnet_post_robust.npy"), post_robust)

    meta = {
        "source": "UCI ML Repository, Daphnet Freezing-of-Gait Dataset",
        "url": URL,
        "record": "S01R01",
        "fs_hz": FS_HZ, "dt_s": 1.0 / FS_HZ,
        "channel_index": CHANNEL_INDEX, "channel_name": channel_name,
        "n_total_samples": int(n_total),
        "unique_labels": {int(k): int(v) for k, v in zip(unique_labels, label_counts)},
        "n_freeze_episodes_total": int(len(onsets)),
        "n_freeze_episode_offsets_found": int(len(offsets)),
        "chosen_transition_index": 0,
        "chosen_onset_sample_0indexed": onset,
        "chosen_onset_time_s": float(data[onset, 0] / 1000.0),
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
        "pre_primary_duration_s": n_pre / FS_HZ,
        "post_primary_duration_s": n_post / FS_HZ,
    }
    with open(os.path.join(OUT_DIR, "daphnet_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote daphnet_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
