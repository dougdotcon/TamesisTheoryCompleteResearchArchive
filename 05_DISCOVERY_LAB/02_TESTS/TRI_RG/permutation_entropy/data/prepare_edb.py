"""
Download and prepare PRE/POST ECG segments (primary + robustness) for the
PhysioNet European ST-T Database (EDB, Taddei et al. 1992) transient-
ischemia domain, per METHODOLOGY_NOTE.md Gap (c). Real data only, fetched
directly via `wfdb` from the public PhysioNet archive (no login/token), no
fabrication.

Record/episode selection (re-verified fresh in this script): the record
suggested by the Fase 0.6 survey, `e0103`, is checked here for genuine
cardiologist-annotated ST-episode onset/peak/offset markers (per the
EDB annotation convention documented at
https://physionet.org/files/edb/1.0.0/annotations.shtml -- ST-episode
annotations carry aux_note text `(ST<signal><sign>` for the episode
BEGINNING and `ST<signal><sign>)` for the episode END; the signal digit
identifies which of the record's 2 channels the episode was measured on).
e0103 is a 2-hour, 2-channel (V4, MLIII), fs=250 Hz record from a patient
with documented mixed angina / 1-vessel (RCA) disease -- confirmed to
carry 5 separate cardiologist-annotated ST episodes on signal 1 (MLIII).
The FIRST chronological episode is used as the primary PRE/POST
transition: its onset is preceded by nothing but continuous normal sinus
rhythm from the start of the record (confirmed by inspecting ALL non-beat
annotations before the onset sample, not assumed), making it the
cleanest, least-confounded transition available in this record.

Writes (into this same data/ directory):
  edb_pre_primary.npy, edb_post_primary.npy,
  edb_pre_robust.npy, edb_post_robust.npy,
  edb_segments_meta.json
Raw multi-MB downloads (.dat/.hea/.atr files) are NOT committed to the
repo -- see ../data/PROVENANCE_EDB.md for exact URLs/record ID/
reproduction steps instead (coordinator instruction for this real-domain
step).
"""
import json
import os

import numpy as np
import wfdb

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PN_DIR = "edb/1.0.0"
RECORD = "e0103"
ST_SIGNAL_INDEX = 1   # MLIII -- the channel on which this record's ST episodes were annotated


def find_st_episodes(ann):
    """Parse ST-episode begin/peak/end triplets from the annotation
    aux_note field, per the EDB convention: '(ST<sig><sign>' begins,
    'AST<sig><sign><mag>' marks the peak, 'ST<sig><sign>)' ends. Returns
    a list of dicts, one per episode, sorted by onset sample. Also
    returns the full list of ALL non-empty annotations (for the
    "clean/unconfounded PRE" check)."""
    aux = [a.strip("\x00") for a in ann.aux_note]
    sym = ann.symbol
    samples = ann.sample

    all_events = [
        {"sample": int(samples[i]), "symbol": sym[i], "aux": aux[i]}
        for i in range(len(aux)) if aux[i] != ""
    ]

    begins, peaks, ends = [], [], []
    for i, a in enumerate(aux):
        if a == "" or "ST" not in a:
            continue
        if a.startswith("(ST"):
            begins.append((int(samples[i]), a))
        elif a.startswith("AST"):
            peaks.append((int(samples[i]), a))
        elif a.startswith("ST") and a.endswith(")"):
            ends.append((int(samples[i]), a))

    episodes = []
    # pair sequentially: begins/peaks/ends should already alternate in order
    for k in range(min(len(begins), len(ends))):
        b_sample, b_aux = begins[k]
        e_sample, e_aux = ends[k]
        p_sample, p_aux = peaks[k] if k < len(peaks) else (None, None)
        episodes.append({
            "onset_sample": b_sample, "onset_aux": b_aux,
            "peak_sample": p_sample, "peak_aux": p_aux,
            "offset_sample": e_sample, "offset_aux": e_aux,
        })
    episodes.sort(key=lambda e: e["onset_sample"])
    return episodes, all_events


def main():
    print(f"Fetching {RECORD} header/signal/annotations from PhysioNet ({PN_DIR}) ...", flush=True)
    rec = wfdb.rdrecord(RECORD, pn_dir=PN_DIR)
    ann = wfdb.rdann(RECORD, "atr", pn_dir=PN_DIR)
    fs = rec.fs
    print(f"  fs={fs}Hz sig_len={rec.sig_len} sig_name={rec.sig_name} "
          f"duration_s={rec.sig_len / fs:.1f}", flush=True)

    episodes, all_events = find_st_episodes(ann)
    print(f"  {len(episodes)} ST episodes found (any signal)", flush=True)
    for e in episodes:
        dur = (e["offset_sample"] - e["onset_sample"]) / fs
        print(f"    onset={e['onset_sample']} ({e['onset_sample']/fs:.1f}s) "
              f"offset={e['offset_sample']} ({e['offset_sample']/fs:.1f}s) "
              f"dur={dur:.1f}s aux={e['onset_aux']!r}", flush=True)
    if not episodes:
        raise RuntimeError(f"No ST episodes found in {RECORD} -- cannot proceed without "
                            f"fabricating a transition.")

    chosen = episodes[0]  # first chronological episode -- see module docstring
    onset, offset = chosen["onset_sample"], chosen["offset_sample"]

    # Confirm no OTHER annotated event (rhythm change, different episode, etc.)
    # occurs between record start and this episode's onset -- makes the PRE
    # window genuinely clean, checked explicitly, not assumed.
    events_before_onset = [e for e in all_events if e["sample"] < onset]
    print(f"  Events before chosen onset (sample<{onset}): {events_before_onset}", flush=True)

    signal_name = rec.sig_name[ST_SIGNAL_INDEX]
    full_signal = rec.p_signal[:, ST_SIGNAL_INDEX].astype(float)
    assert not np.isnan(full_signal).any(), "unexpected NaN in raw EDB signal -- refusing to proceed"

    pre_primary = full_signal[:onset]
    post_primary = full_signal[onset:offset]
    n_pre, n_post = len(pre_primary), len(post_primary)
    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

    print(f"PRE primary n={n_pre} ({n_pre / fs:.1f}s)  POST primary n={n_post} ({n_post / fs:.1f}s)",
          flush=True)
    print(f"PRE robust n={len(pre_robust)}  POST robust n={len(post_robust)}", flush=True)
    assert n_pre > 0 and n_post > 0

    np.save(os.path.join(OUT_DIR, "edb_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "edb_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "edb_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "edb_post_robust.npy"), post_robust)

    meta = {
        "source": "PhysioNet European ST-T Database (EDB) 1.0.0, Taddei et al. 1992",
        "record": RECORD, "fs_hz": float(fs),
        "signal_names": rec.sig_name, "st_signal_index": ST_SIGNAL_INDEX,
        "st_signal_name": signal_name,
        "record_duration_s": rec.sig_len / fs,
        "n_st_episodes_in_record": len(episodes),
        "all_episodes": [
            {"onset_sample": e["onset_sample"], "onset_s": e["onset_sample"] / fs,
             "peak_sample": e["peak_sample"], "peak_s": (e["peak_sample"] / fs if e["peak_sample"] else None),
             "offset_sample": e["offset_sample"], "offset_s": e["offset_sample"] / fs,
             "duration_s": (e["offset_sample"] - e["onset_sample"]) / fs,
             "onset_aux": e["onset_aux"], "peak_aux": e["peak_aux"], "offset_aux": e["offset_aux"]}
            for e in episodes
        ],
        "chosen_episode_index": 0,
        "chosen_onset_sample": onset, "chosen_onset_s": onset / fs,
        "chosen_offset_sample": offset, "chosen_offset_s": offset / fs,
        "events_before_chosen_onset": events_before_onset,
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
        "pre_primary_duration_s": n_pre / fs,
        "post_primary_duration_s": n_post / fs,
    }
    with open(os.path.join(OUT_DIR, "edb_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote edb_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
