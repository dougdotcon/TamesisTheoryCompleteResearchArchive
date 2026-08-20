"""
Download and prepare PRE/POST vertical-velocity seismic segments
(primary + robustness) for the Kilauea 2018 Lower East Rift Zone (LERZ)
eruption, May-3 fissure-opening transition, per ../METHODOLOGY_NOTE.md
section 5.2. Real data only, fetched directly from the public IRIS/
EarthScope FDSN dataselect web service (no login/token), no fabrication.

Station: HV.BYL..HHZ (100Hz) -- verified available for the needed window
in this session (station-level query + a 5-minute test fetch both
succeeded). Falls back to HV.HAT..HHZ (the station used by
lempel_ziv_complexity for the SAME transition) ONLY if BYL's fetch fails
for the actual PRE/POST windows -- the fallback decision and its outcome
are recorded in PROVENANCE_KILAUEA.md, not decided for convenience after
seeing the data.

Transition (fixed a priori, METHODOLOGY_NOTE.md section 5.2): opening of
the first LERZ eruptive fissure in Leilani Estates, 2018-05-03, locked at
2018-05-03T18:00:00 UTC (same operational convention already used by
lempel_ziv_complexity/data/prepare_kilauea.py for this EXACT event).
PRE = 24h window immediately before the transition.
POST = from the transition to the next independently-documented
  large-magnitude event, the M6.9 south-flank earthquake
  (2018-05-04T22:32:54 UTC, USGS).

Writes (into this same data/ directory):
  kilauea_pre_primary.npy, kilauea_post_primary.npy,
  kilauea_pre_robust.npy, kilauea_post_robust.npy,
  kilauea_segments_meta.json
Raw miniseed downloads are NOT committed (see PROVENANCE_KILAUEA.md).
"""
import io
import json
import os
import urllib.request

import numpy as np
import obspy

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FDSN_BASE = "https://service.iris.edu/fdsnws/dataselect/1/query"
NET, LOC, CHA = "HV", "--", "HHZ"
STA_PRIMARY = "BYL"
STA_FALLBACK = "HAT"
PRE_START, PRE_END = "2018-05-02T18:00:00", "2018-05-03T18:00:00"
POST_START, POST_END = "2018-05-03T18:00:00", "2018-05-04T22:32:54"


def fetch_mseed(sta, start, end):
    url = (f"{FDSN_BASE}?net={NET}&sta={sta}&loc={LOC}&cha={CHA}"
           f"&start={start}&end={end}&format=miniseed")
    print(f"  fetching {url}", flush=True)
    with urllib.request.urlopen(url, timeout=300) as resp:
        raw = resp.read()
    print(f"    {len(raw)} bytes", flush=True)
    return obspy.read(io.BytesIO(raw))


def load_window(sta, start, end, label):
    st = fetch_mseed(sta, start, end)
    gaps = st.get_gaps()
    print(f"  [{label}/{sta}] {len(st)} trace(s), gaps={gaps}", flush=True)
    if len(st) != 1 or len(gaps) != 0:
        raise RuntimeError(f"[{label}/{sta}] expected a single continuous trace, "
                            f"got {len(st)} trace(s), gaps={gaps}")
    return st[0]


def load_with_fallback(start, end, label):
    try:
        tr = load_window(STA_PRIMARY, start, end, label)
        return tr, STA_PRIMARY, None
    except Exception as e:
        print(f"  [{label}] {STA_PRIMARY} failed ({e}); falling back to {STA_FALLBACK}", flush=True)
        tr = load_window(STA_FALLBACK, start, end, label)
        return tr, STA_FALLBACK, str(e)


def main():
    print("Fetching PRE window ...", flush=True)
    tr_pre, sta_pre, fallback_reason_pre = load_with_fallback(PRE_START, PRE_END, "PRE")
    print("Fetching POST window ...", flush=True)
    tr_post, sta_post, fallback_reason_post = load_with_fallback(POST_START, POST_END, "POST")

    assert sta_pre == sta_post, (
        f"PRE used {sta_pre} but POST used {sta_post} -- refusing to mix stations "
        f"within one domain/transition"
    )
    station_used = sta_pre

    fs_pre, fs_post = tr_pre.stats.sampling_rate, tr_post.stats.sampling_rate
    assert fs_pre == fs_post, f"sampling rate mismatch: PRE={fs_pre} POST={fs_post}"
    fs = fs_pre

    pre_primary = tr_pre.data.astype(float)
    post_primary = tr_post.data.astype(float)
    n_pre, n_post = len(pre_primary), len(post_primary)

    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

    print(f"Station used: {station_used}", flush=True)
    print(f"PRE primary n={n_pre} ({n_pre/fs/3600:.2f}h)  POST primary n={n_post} ({n_post/fs/3600:.2f}h)", flush=True)
    print(f"PRE robust n={len(pre_robust)} ({len(pre_robust)/fs/3600:.2f}h)  "
          f"POST robust n={len(post_robust)} ({len(post_robust)/fs/3600:.2f}h)", flush=True)
    assert n_pre > 0 and n_post > 0

    np.save(os.path.join(OUT_DIR, "kilauea_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "kilauea_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "kilauea_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "kilauea_post_robust.npy"), post_robust)

    meta = {
        "source": "IRIS/EarthScope FDSN dataselect web service",
        "network": NET, "station": station_used, "location": LOC, "channel": CHA,
        "station_fallback_used": station_used != STA_PRIMARY,
        "fallback_reason_pre": fallback_reason_pre, "fallback_reason_post": fallback_reason_post,
        "fs_hz": float(fs), "dt_s": 1.0 / float(fs),
        "transition_utc": "2018-05-03T18:00:00Z",
        "transition_description": "Opening of first LERZ eruptive fissure, Leilani Estates, 2018-05-03 (USGS HVO)",
        "pre_window_utc": [PRE_START, PRE_END],
        "post_window_utc": [POST_START, POST_END],
        "post_boundary_event": "M6.9 Kilauea south-flank earthquake, 2018-05-04T22:32:54 UTC (USGS)",
        "pre_trace_starttime": str(tr_pre.stats.starttime),
        "pre_trace_endtime": str(tr_pre.stats.endtime),
        "post_trace_starttime": str(tr_post.stats.starttime),
        "post_trace_endtime": str(tr_post.stats.endtime),
        "pre_n_gaps": 0, "post_n_gaps": 0,
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
        "pre_primary_duration_h": n_pre / fs / 3600.0,
        "post_primary_duration_h": n_post / fs / 3600.0,
    }
    with open(os.path.join(OUT_DIR, "kilauea_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote kilauea_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
