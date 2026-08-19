"""
Download and prepare PRE/POST ECG segments (primary + robustness) for the
PhysioNet MIT-BIH Malignant Ventricular Arrhythmia Database (`vfdb`),
record 418, per METHODOLOGY_NOTE.md Gap (c). Real data only, fetched
directly via `wfdb` from the public PhysioNet archive (no login/token), no
fabrication. Mirrors permutation_entropy/data/prepare_edb.py for this line.

Transition selection (re-verified fresh in this script, per Gap (c)'s
explicit scope decision -- only the FIRST N->VFL transition in the record
is used, not all ~10): record `418` is a 35-minute (2100s), 2-channel
(both generically labeled "ECG", fs=250Hz, gain=200) continuous recording.
Rhythm annotations use aux_note `(N` (normal) and `(VFL` (ventricular
flutter/fibrillation) markers -- confirmed here to be the ONLY two aux_note
values in the entire record (121 annotations total). The FIRST chronological
`(VFL` onset is at sample 99624 (398.496s); the record has exactly ONE
annotation before it (`(N` at sample 18, marking the start of normal
rhythm) -- confirming the PRE window is genuinely unconfounded (checked
explicitly, not assumed). The episode returns to `(N` at sample 101499
(405.996s), a 7.5s episode (1875 samples) -- short, but it is what "the
first documented transition" gives; used as specified by
METHODOLOGY_NOTE.md Gap (c), not substituted for a longer later episode.

Channel choice: both channels are generically named "ECG" in this record
(no distinguishing lead label, unlike EDB's V4/MLIII). Channel 0 has
visibly larger dynamic range (std=0.53mV vs. 0.22mV for channel 1) --
used as the primary analysis channel, documented here as an explicit,
non-arbitrary-but-simple choice (not re-derived from the transition data
itself).

Writes (into this same data/ directory):
  vfdb_pre_primary.npy, vfdb_post_primary.npy,
  vfdb_pre_robust.npy, vfdb_post_robust.npy,
  vfdb_segments_meta.json
Raw downloads are NOT committed to the repo (wfdb streams directly from
PhysioNet, no local raw file ever created) -- see
../data/PROVENANCE_VFDB.md for exact URLs/record ID/reproduction steps.
"""
import json
import os

import numpy as np
import wfdb

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PN_DIR = "vfdb/1.0.0"
RECORD = "418"
CHANNEL_INDEX = 0  # both channels generically "ECG" -- larger-dynamic-range channel used, see module docstring


def main():
    print(f"Fetching {RECORD} header/signal/annotations from PhysioNet ({PN_DIR}) ...", flush=True)
    rec = wfdb.rdrecord(RECORD, pn_dir=PN_DIR)
    ann = wfdb.rdann(RECORD, "atr", pn_dir=PN_DIR)
    fs = rec.fs
    print(f"  fs={fs}Hz sig_len={rec.sig_len} sig_name={rec.sig_name} "
          f"duration_s={rec.sig_len / fs:.1f} n_channels={rec.p_signal.shape[1]}", flush=True)

    aux = [a.strip("\x00") for a in ann.aux_note]
    sym = ann.symbol
    samples = ann.sample
    all_events = [{"sample": int(samples[i]), "symbol": sym[i], "aux": aux[i]} for i in range(len(aux))]
    print(f"  {len(all_events)} annotations total; unique aux_note values: {sorted(set(aux))}", flush=True)

    vfl_onsets = [e["sample"] for e in all_events if e["aux"] == "(VFL"]
    n_onsets = [e["sample"] for e in all_events if e["aux"] == "(N"]
    if not vfl_onsets:
        raise RuntimeError("No (VFL onset found in record 418 -- cannot proceed without fabricating a transition.")
    onset = vfl_onsets[0]
    offsets_after_onset = [s for s in n_onsets if s > onset]
    if not offsets_after_onset:
        raise RuntimeError("No (N offset found after the first (VFL onset -- cannot bound the POST episode.")
    offset = offsets_after_onset[0]

    events_before_onset = [e for e in all_events if e["sample"] < onset]
    print(f"  First (VFL onset: sample={onset} ({onset/fs:.3f}s)", flush=True)
    print(f"  Episode (N offset: sample={offset} ({offset/fs:.3f}s), duration={((offset-onset)/fs):.3f}s", flush=True)
    print(f"  Events before onset (sample<{onset}): {events_before_onset}", flush=True)
    print(f"  Total (VFL onsets in record (all N->VFL transitions, only 1st used per Gap (c)): {len(vfl_onsets)}", flush=True)

    channel_name = rec.sig_name[CHANNEL_INDEX]
    full_signal = rec.p_signal[:, CHANNEL_INDEX].astype(float)
    assert not np.isnan(full_signal).any(), "unexpected NaN in raw vfdb signal -- refusing to proceed"

    pre_primary = full_signal[:onset]
    post_primary = full_signal[onset:offset]
    n_pre, n_post = len(pre_primary), len(post_primary)
    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

    print(f"PRE primary n={n_pre} ({n_pre/fs:.1f}s)  POST primary n={n_post} ({n_post/fs:.1f}s)", flush=True)
    print(f"PRE robust n={len(pre_robust)}  POST robust n={len(post_robust)}", flush=True)
    assert n_pre > 0 and n_post > 0

    np.save(os.path.join(OUT_DIR, "vfdb_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "vfdb_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "vfdb_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "vfdb_post_robust.npy"), post_robust)

    meta = {
        "source": "PhysioNet MIT-BIH Malignant Ventricular Arrhythmia Database (vfdb) 1.0.0",
        "record": RECORD, "fs_hz": float(fs), "dt_s": 1.0 / float(fs),
        "sig_name": rec.sig_name, "channel_index": CHANNEL_INDEX, "channel_name": channel_name,
        "record_duration_s": rec.sig_len / fs,
        "n_annotations_total": len(all_events),
        "unique_aux_note_values": sorted(set(aux)),
        "n_vfl_onsets_in_record": len(vfl_onsets),
        "chosen_transition_index": 0,
        "chosen_onset_sample": int(onset), "chosen_onset_s": onset / fs,
        "chosen_offset_sample": int(offset), "chosen_offset_s": offset / fs,
        "chosen_episode_duration_s": (offset - onset) / fs,
        "events_before_chosen_onset": events_before_onset,
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
        "pre_primary_duration_s": n_pre / fs,
        "post_primary_duration_s": n_post / fs,
    }
    with open(os.path.join(OUT_DIR, "vfdb_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote vfdb_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
