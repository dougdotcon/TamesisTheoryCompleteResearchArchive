"""
Download and prepare PRE/POST vertical-velocity seismic segments
(primary + robustness) for the Kilauea 2018 Lower East Rift Zone (LERZ)
eruption, station `HV.HAT..HHZ`, per ../METHODOLOGY_NOTE.md Gap (c),
Domain 2. Real data only, fetched directly from the public IRIS/
EarthScope FDSN dataselect web service (no login/token), no fabrication.

Transition (fixed a priori): opening of the first LERZ eruptive fissure
in Leilani Estates, locked at 2018-05-03T18:00:00 UTC (USGS HVO).
PRE = 24h window immediately before the transition
  (2018-05-02T18:00:00 -- 2018-05-03T18:00:00 UTC).
POST = from the transition to the next independently-documented
  large-magnitude event, the M6.9 south-flank earthquake
  (2018-05-04T22:32:54 UTC, USGS -- the largest Hawaii earthquake since
  1975), used as the POST boundary per this line's "next documented
  event" convention.

Writes (into this same data/ directory):
  kilauea_pre_primary.npy, kilauea_post_primary.npy,
  kilauea_pre_robust.npy, kilauea_post_robust.npy,
  kilauea_segments_meta.json
Raw miniseed downloads are NOT committed to the repo (large: ~11MB PRE +
~15MB POST compressed; ~150MB combined as float64 .npy) -- see
../data/PROVENANCE_KILAUEA.md for exact URLs/reproduction steps.
"""
import json
import os

import numpy as np
import obspy
import urllib.request

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FDSN_BASE = "https://service.iris.edu/fdsnws/dataselect/1/query"
NET, STA, LOC, CHA = "HV", "HAT", "--", "HHZ"
PRE_START, PRE_END = "2018-05-02T18:00:00", "2018-05-03T18:00:00"
POST_START, POST_END = "2018-05-03T18:00:00", "2018-05-04T22:32:54"


def fetch_mseed(start, end):
    url = (f"{FDSN_BASE}?net={NET}&sta={STA}&loc={LOC}&cha={CHA}"
           f"&start={start}&end={end}&format=miniseed")
    print(f"  fetching {url}", flush=True)
    with urllib.request.urlopen(url, timeout=300) as resp:
        raw = resp.read()
    print(f"    {len(raw)} bytes", flush=True)
    return obspy.read(io_bytes(raw))


def io_bytes(raw):
    import io
    return io.BytesIO(raw)


def load_window(start, end, label):
    st = fetch_mseed(start, end)
    gaps = st.get_gaps()
    print(f"  [{label}] {len(st)} trace(s), gaps={gaps}", flush=True)
    assert len(st) == 1, f"[{label}] expected a single continuous trace, got {len(st)} -- refusing to proceed with gaps"
    assert len(gaps) == 0, f"[{label}] gaps present in trace -- refusing to proceed silently"
    tr = st[0]
    return tr


def main():
    print("Fetching PRE window ...", flush=True)
    tr_pre = load_window(PRE_START, PRE_END, "PRE")
    print("Fetching POST window ...", flush=True)
    tr_post = load_window(POST_START, POST_END, "POST")

    fs_pre, fs_post = tr_pre.stats.sampling_rate, tr_post.stats.sampling_rate
    assert fs_pre == fs_post, f"sampling rate mismatch: PRE={fs_pre} POST={fs_post}"
    fs = fs_pre

    pre_primary = tr_pre.data.astype(float)
    post_primary = tr_post.data.astype(float)
    n_pre, n_post = len(pre_primary), len(post_primary)

    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

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
        "network": NET, "station": STA, "location": LOC, "channel": CHA,
        "fs_hz": float(fs), "dt_s": 1.0 / float(fs),
        "transition_utc": "2018-05-03T18:00:00Z",
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
