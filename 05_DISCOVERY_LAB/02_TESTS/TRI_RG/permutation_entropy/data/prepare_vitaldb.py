"""
Download and prepare PRE/POST EEG segments (primary + robustness) for the
VitalDB anesthesia-induction domain, per METHODOLOGY_NOTE.md Gap (c). Real
data only, fetched directly from the public VitalDB API (no login/token),
no fabrication -- every value here comes directly from the downloaded
files. Re-verifies case/track selection itself rather than trusting any
prior session's unsaved cache (per task instructions).

VitalDB API (https://api.vitaldb.net, Lee et al. 2022, JMIR Med Inform,
Seoul National University Hospital):
  - /cases : gzip CSV, case-level metadata (anestart/aneend/casestart/
    caseend etc.), one row per case.
  - /trks  : gzip CSV, (caseid, tname, tid) for every track of every case.
  - /{tid} : gzip CSV, the raw waveform/numeric data for one track ("Time"
    column non-blank only at a sample's real resync points; blank Time
    rows continue at the fixed native sampling interval; blank value
    rows are missing/dropped samples -- NEVER fabricated, just excluded).

Case/track selection (re-verified fresh in this script, not hardcoded
blindly): scans /cases + /trks for cases carrying a BIS/EEG1_WAV or
BIS/EEG2_WAV raw EEG waveform track (~128 Hz) AND a documented
`anestart` that falls INSIDE the case's own recorded time range
(casestart <= anestart <= caseend) with >= 600s of track available on
BOTH sides of anestart -- then picks the candidate with the largest
min(PRE_duration, POST_duration), i.e. the best-balanced case. Case 1
(the case a prior, uncommitted Fase 0.6 session referenced) is explicitly
NOT usable for the PRE/POST design here: its anestart=-552s falls BEFORE
the case's own track start (casestart=0), so no PRE segment exists for
it under this candidate's Gap (c) definition -- confirmed by this
script's own re-verification, not assumed.

Writes (into this same data/ directory):
  vitaldb_pre_primary.npy, vitaldb_post_primary.npy,
  vitaldb_pre_robust.npy, vitaldb_post_robust.npy,
  vitaldb_segments_meta.json
Raw multi-MB downloads (cases.csv, trks.csv, the full per-case waveform
CSV) are NOT committed to the repo -- see ../data/PROVENANCE_VITALDB.md
for exact URLs/track IDs/reproduction steps instead (coordinator
instruction for this real-domain step).
"""
import csv
import io
import json
import os

import numpy as np
import requests

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
API_BASE = "https://api.vitaldb.net"

PRE_POST_MIN_SECONDS = 600.0   # candidate-selection floor, both sides of anestart
EEG_TRACK_NAMES = ("BIS/EEG1_WAV", "BIS/EEG2_WAV")


def fetch_csv_rows(path):
    r = requests.get(f"{API_BASE}/{path}", timeout=120)
    r.raise_for_status()
    text = r.content.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def fetch_track_csv(tid):
    r = requests.get(f"{API_BASE}/{tid}", timeout=300)
    r.raise_for_status()
    text = r.content.decode("utf-8-sig")
    return list(csv.reader(io.StringIO(text)))


def select_case():
    """Re-verify case/track selection fresh (never trust a cached
    choice blindly). Returns dict with caseid, tid, tname, and the
    case-level timing fields used."""
    print("Fetching /cases ...", flush=True)
    cases = fetch_csv_rows("cases")
    print(f"  {len(cases)} cases", flush=True)
    print("Fetching /trks ...", flush=True)
    trk_rows = fetch_csv_rows("trks")
    print(f"  {len(trk_rows)} track rows", flush=True)

    eeg_tracks = {}  # caseid -> {tname: tid}
    for row in trk_rows:
        if row["tname"] in EEG_TRACK_NAMES:
            eeg_tracks.setdefault(row["caseid"], {})[row["tname"]] = row["tid"]

    candidates = []
    for row in cases:
        cid = row["caseid"]
        if cid not in eeg_tracks:
            continue
        try:
            casestart = float(row["casestart"]); caseend = float(row["caseend"])
            anestart = float(row["anestart"]); aneend = float(row["aneend"])
        except (ValueError, KeyError):
            continue
        if not (casestart <= anestart <= caseend):
            continue  # anestart outside the recorded track range -- no valid PRE
        pre_dur = anestart - casestart
        post_dur = min(aneend, caseend) - anestart
        if pre_dur >= PRE_POST_MIN_SECONDS and post_dur >= PRE_POST_MIN_SECONDS:
            candidates.append({
                "caseid": cid, "casestart": casestart, "caseend": caseend,
                "anestart": anestart, "aneend": aneend,
                "pre_dur": pre_dur, "post_dur": post_dur,
                "tname": "BIS/EEG1_WAV" if "BIS/EEG1_WAV" in eeg_tracks[cid] else "BIS/EEG2_WAV",
            })
    print(f"  {len(candidates)} candidate cases (EEG track present, anestart inside "
          f"recorded range, >= {PRE_POST_MIN_SECONDS:.0f}s on both sides)", flush=True)
    if not candidates:
        raise RuntimeError("No VitalDB case satisfies the PRE/POST design -- cannot proceed "
                            "without fabricating data.")

    candidates.sort(key=lambda c: -min(c["pre_dur"], c["post_dur"]))
    best = candidates[0]
    best["tid"] = eeg_tracks[best["caseid"]][best["tname"]]
    print(f"Selected case {best['caseid']}: pre_dur={best['pre_dur']:.1f}s "
          f"post_dur={best['post_dur']:.1f}s track={best['tname']}", flush=True)
    return best, candidates[:15]


def reconstruct_series(rows):
    """Parse one VitalDB track CSV (rows already parsed by csv.reader,
    header excluded): reconstruct the uniform sample-time grid from the
    first two explicit Time entries (fixed native sampling interval,
    Time left blank on every subsequent row until a final resync entry),
    verify against the final explicit Time entry, then return
    (times, values) for the samples that HAVE a non-blank value --
    missing samples are dropped, never fabricated/interpolated.
    """
    header = rows[0]
    data = rows[1:]
    n = len(data)
    t0 = float(data[0][0])
    t1 = float(data[1][0])
    dt = t1 - t0
    times = t0 + dt * np.arange(n)

    # sanity-check against the last explicit (non-blank) Time entry, if any
    last_explicit = None
    for i in range(n - 1, -1, -1):
        if data[i][0] != "":
            last_explicit = (i, float(data[i][0]))
            break
    check_ok = None
    if last_explicit is not None:
        i, t_claimed = last_explicit
        t_reconstructed = times[i]
        check_ok = bool(abs(t_claimed - t_reconstructed) < 0.5)  # sub-second tolerance
    values = np.array([np.nan if row[1] == "" else float(row[1]) for row in data], dtype=float)
    valid = ~np.isnan(values)
    n_missing = int((~valid).sum())
    return times[valid], values[valid], {
        "header": header, "n_total_rows": n, "dt": dt, "fs_hz": 1.0 / dt,
        "n_missing": n_missing, "frac_missing": n_missing / n,
        "last_explicit_time_check_ok": check_ok,
    }


def main():
    case, top_candidates = select_case()
    caseid, tid = case["caseid"], case["tid"]
    anestart, aneend = case["anestart"], case["aneend"]

    print(f"Downloading waveform track {tid} for case {caseid} ...", flush=True)
    rows = fetch_track_csv(tid)
    times, values, parse_info = reconstruct_series(rows)
    print(f"  n_valid_samples={len(values)} fs={parse_info['fs_hz']:.4f}Hz "
          f"frac_missing={parse_info['frac_missing']:.5f} "
          f"time_range=[{times[0]:.2f},{times[-1]:.2f}]s", flush=True)

    track_end_time = float(times[-1])
    post_end_time = min(aneend, track_end_time)
    post_end_capped_by_track = bool(aneend > track_end_time)

    pre_mask = times < anestart
    post_mask = (times >= anestart) & (times <= post_end_time)

    pre_primary = values[pre_mask]
    post_primary = values[post_mask]
    n_pre, n_post = len(pre_primary), len(post_primary)
    pre_robust = pre_primary[n_pre // 2:]        # most recent 50% by count
    post_robust = post_primary[: n_post // 2]     # 50% closest to the transition

    print(f"PRE primary n={n_pre} ({n_pre / parse_info['fs_hz']:.1f}s)  "
          f"POST primary n={n_post} ({n_post / parse_info['fs_hz']:.1f}s)", flush=True)
    print(f"PRE robust n={len(pre_robust)}  POST robust n={len(post_robust)}", flush=True)
    assert n_pre > 0 and n_post > 0, "empty PRE or POST segment -- refusing to proceed"
    assert not np.isnan(pre_primary).any() and not np.isnan(post_primary).any()

    np.save(os.path.join(OUT_DIR, "vitaldb_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "vitaldb_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "vitaldb_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "vitaldb_post_robust.npy"), post_robust)

    meta = {
        "source": "VitalDB API (https://api.vitaldb.net), Lee et al. 2022 JMIR Med Inform",
        "caseid": caseid, "track_id": tid, "track_name": case["tname"],
        "fs_hz": parse_info["fs_hz"],
        "casestart_s": case["casestart"], "caseend_s": case["caseend"],
        "anestart_s": anestart, "aneend_s": aneend,
        "track_recorded_time_range_s": [float(times[0]), float(times[-1])],
        "post_end_time_s_used": post_end_time,
        "post_end_capped_by_track_availability": post_end_capped_by_track,
        "n_missing_samples_dropped": parse_info["n_missing"],
        "frac_missing": parse_info["frac_missing"],
        "sampling_grid_reconstruction_check_ok": parse_info["last_explicit_time_check_ok"],
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
        "pre_primary_duration_s": n_pre / parse_info["fs_hz"],
        "post_primary_duration_s": n_post / parse_info["fs_hz"],
        "top_candidate_cases_considered": [
            {k: v for k, v in c.items() if k != "tname"} | {"tname": c["tname"]}
            for c in top_candidates
        ],
    }
    with open(os.path.join(OUT_DIR, "vitaldb_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote vitaldb_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
