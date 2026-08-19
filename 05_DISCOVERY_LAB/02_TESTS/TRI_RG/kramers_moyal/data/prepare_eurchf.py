"""
Download and prepare PRE/POST EUR/CHF tick-price segments (primary +
robustness) around the Swiss National Bank (SNB) de-peg shock,
2015-01-15, per METHODOLOGY_NOTE.md Gap (c). Real data only, fetched
directly from Dukascopy's public historical tick-data feed (binary
`.bi5` LZMA-compressed hourly files, no login/token), no fabrication.
Re-verified fresh in THIS session (not trusting any uncommitted cache
from the Fase 0.6 survey session).

Format (Dukascopy `.bi5`, LZMA-compressed, verified here by direct
inspection of a decoded file, not assumed from memory): each tick is a
20-byte big-endian record `>iiiff`:
  time_ms_offset (int32, ms since the top of the file's hour),
  ask*10^5 (int32), bid*10^5 (int32),
  ask_volume (float32, millions of the base currency),
  bid_volume (float32).
EUR/CHF point value = 10^5 (5 decimal digits), confirmed empirically:
decoded prices cluster at ~1.20090-1.20102 in the pre-announcement hour,
matching the well-documented SNB floor (EUR/CHF was pegged with a floor
at 1.2000, defended near 1.2009-1.2010 in practice).

Download reliability note (found empirically in this session): the
Dukascopy datafeed host intermittently resets the TLS connection after
a successful request (`Recv failure: Connection reset by peer`) --
observed non-deterministically, not tied to any specific hour/URL (a
retry of the SAME URL that just failed succeeds later). Retried here
with exponential backoff + jitter, capped attempts, each failure logged
-- an outright download failure after all retries is reported as a
failure for that hour, never silently skipped or replaced with
fabricated data.

Date range: all 24 hourly files for 2015-01-15 (UTC), which fully
contains the announcement (~09:30 UTC, 10:30 CET -- Switzerland is on
CET/UTC+1 in January, no DST) with several hours of continuous
pre-announcement trading on both sides.

Writes (into this same data/ directory):
  eurchf_pre_primary.npy, eurchf_post_primary.npy,
  eurchf_pre_robust.npy, eurchf_post_robust.npy,
  eurchf_segments_meta.json
The mid price series (ask+bid)/2 is used as the analysis series `x`.
Raw `.bi5` downloads are NOT committed (fetched fresh each run) -- see
../data/PROVENANCE_EURCHF.md for exact URLs/reproduction steps.
"""
import json
import lzma
import os
import struct
import time
import urllib.request
import urllib.error

import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL = "EURCHF"
YEAR = 2015
MONTH_0INDEXED = "00"  # Dukascopy months are 0-indexed: January = "00"
DAY = "15"
POINT_VALUE = 100000.0  # EUR/CHF, 5 decimal digits
ANNOUNCEMENT_HOUR_UTC = 9
ANNOUNCEMENT_MINUTE_UTC = 30  # 09:30 UTC = 10:30 CET, well-documented SNB announcement time

URL_TMPL = "https://datafeed.dukascopy.com/datafeed/{symbol}/{year}/{month}/{day}/{hour:02d}h_ticks.bi5"

RECORD_FMT = ">iiiff"
RECORD_SIZE = struct.calcsize(RECORD_FMT)


def fetch_hour(hour, max_retries=8, base_delay=2.0):
    """Fetch and decode one hourly .bi5 file, with retry/backoff for the
    intermittent connection resets observed empirically (see module
    docstring). Returns a structured array of (t_ms_offset, ask, bid,
    ask_vol, bid_vol) for that hour, or an EMPTY array if the hour had
    zero ticks (a genuinely empty low-liquidity hour is a valid,
    non-error outcome for .bi5 -- Dukascopy returns a 0-byte/empty file,
    not a 404, for hours with no ticks). Raises RuntimeError only after
    exhausting all retries on a genuine download failure.
    """
    url = URL_TMPL.format(symbol=SYMBOL, year=YEAR, month=MONTH_0INDEXED, day=DAY, hour=hour)
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
            if len(raw) == 0:
                print(f"    hour={hour:02d} EMPTY (0 bytes, no ticks this hour) url={url}", flush=True)
                return np.array([], dtype=[("t_ms", "i4"), ("ask", "i4"), ("bid", "i4"), ("askv", "f4"), ("bidv", "f4")])
            data = lzma.decompress(raw)
            n = len(data) // RECORD_SIZE
            recs = struct.unpack(f">{'iiiff' * n}", data)
            arr = np.array(
                [tuple(recs[i * 5:(i + 1) * 5]) for i in range(n)],
                dtype=[("t_ms", "i4"), ("ask", "i4"), ("bid", "i4"), ("askv", "f4"), ("bidv", "f4")],
            )
            print(f"    hour={hour:02d} OK n_ticks={n} (attempt {attempt}) url={url}", flush=True)
            return arr
        except Exception as e:  # noqa: BLE001 -- deliberately broad: retry on ANY transient network error
            last_err = e
            delay = base_delay * (1.5 ** (attempt - 1)) + np.random.uniform(0, 1.0)
            print(f"    hour={hour:02d} attempt {attempt}/{max_retries} FAILED ({type(e).__name__}: {e}) "
                  f"-- retrying in {delay:.1f}s", flush=True)
            time.sleep(delay)
    raise RuntimeError(f"Failed to download hour={hour:02d} after {max_retries} attempts: {last_err}")


def main():
    print(f"Downloading {SYMBOL} tick data for {YEAR}-{MONTH_0INDEXED[::-1] if False else '01'}-{DAY} "
          f"(all 24 UTC hours) from Dukascopy ...", flush=True)
    all_hours = {}
    for hour in range(24):
        all_hours[hour] = fetch_hour(hour)

    total_ticks = sum(len(a) for a in all_hours.values())
    print(f"Total ticks across all 24 hours: {total_ticks}", flush=True)
    assert total_ticks > 0, "zero ticks downloaded across the whole day -- refusing to proceed without real data"

    # Build a single chronological array: absolute ms since 2015-01-15T00:00:00 UTC.
    all_t_ms, all_ask, all_bid = [], [], []
    for hour in range(24):
        arr = all_hours[hour]
        if len(arr) == 0:
            continue
        all_t_ms.append(arr["t_ms"].astype(np.int64) + hour * 3600 * 1000)
        all_ask.append(arr["ask"].astype(np.float64) / POINT_VALUE)
        all_bid.append(arr["bid"].astype(np.float64) / POINT_VALUE)
    t_ms = np.concatenate(all_t_ms)
    ask = np.concatenate(all_ask)
    bid = np.concatenate(all_bid)

    # ticks within an hour file are already time-ordered by construction
    # (Dukascopy convention), but sort explicitly across the hour
    # boundary concatenation for safety -- never assumed.
    order = np.argsort(t_ms, kind="stable")
    t_ms, ask, bid = t_ms[order], ask[order], bid[order]
    mid = (ask + bid) / 2.0

    announcement_ms = (ANNOUNCEMENT_HOUR_UTC * 3600 + ANNOUNCEMENT_MINUTE_UTC * 60) * 1000
    split_idx = int(np.searchsorted(t_ms, announcement_ms))

    # Diagnostic: confirm empirically (not just assumed from external
    # documentation) that a genuine structural break in price occurs
    # near the assumed announcement time -- report the price level just
    # before/after the split, and the max 1-tick jump in a +-5min window
    # around the split, for honest documentation.
    window_mask = (t_ms > announcement_ms - 5 * 60 * 1000) & (t_ms < announcement_ms + 5 * 60 * 1000)
    window_mid = mid[window_mask]
    max_jump_near_split = float(np.max(np.abs(np.diff(window_mid)))) if len(window_mid) > 1 else None
    price_just_before = float(mid[split_idx - 1]) if split_idx > 0 else None
    price_just_after = float(mid[split_idx]) if split_idx < len(mid) else None
    price_5min_before = float(mid[np.searchsorted(t_ms, announcement_ms - 5 * 60 * 1000)]) if np.any(t_ms < announcement_ms - 5 * 60 * 1000) else None
    price_5min_after_idx = np.searchsorted(t_ms, announcement_ms + 5 * 60 * 1000)
    price_5min_after = float(mid[min(price_5min_after_idx, len(mid) - 1)]) if len(mid) else None

    print(f"Split at {ANNOUNCEMENT_HOUR_UTC:02d}:{ANNOUNCEMENT_MINUTE_UTC:02d} UTC "
          f"(ms={announcement_ms}) -> split_idx={split_idx} / {len(mid)} total ticks", flush=True)
    print(f"  price 5min before announcement: {price_5min_before}", flush=True)
    print(f"  price just before split: {price_just_before}", flush=True)
    print(f"  price just after split:  {price_just_after}", flush=True)
    print(f"  price 5min after announcement:  {price_5min_after}", flush=True)
    print(f"  max single-tick jump within +-5min of split: {max_jump_near_split}", flush=True)

    pre_primary = mid[:split_idx]
    post_primary = mid[split_idx:]
    n_pre, n_post = len(pre_primary), len(post_primary)
    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

    print(f"PRE primary n={n_pre}  POST primary n={n_post}", flush=True)
    print(f"PRE robust n={len(pre_robust)}  POST robust n={len(post_robust)}", flush=True)
    assert n_pre > 100 and n_post > 100, "PRE or POST segment implausibly small -- refusing to proceed"

    np.save(os.path.join(OUT_DIR, "eurchf_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "eurchf_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "eurchf_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "eurchf_post_robust.npy"), post_robust)

    # Native "dt" for reporting purposes: median inter-tick interval in
    # seconds, over the FULL day (ticks are irregularly spaced -- see
    # PROVENANCE_EURCHF.md for the explicit note on why this choice does
    # not affect PKS, the decision channel, since D1/D2's ratio -- and
    # hence the reconstructed p_st and PKS -- is scale-invariant in
    # tau/dt; dt only affects the ABSOLUTE reported tau_ME/D-coefficient
    # values, not PKS itself).
    dt_diffs_s = np.diff(t_ms) / 1000.0
    dt_diffs_s = dt_diffs_s[dt_diffs_s > 0]
    median_dt_s = float(np.median(dt_diffs_s)) if len(dt_diffs_s) else None

    meta = {
        "source": "Dukascopy historical tick data feed, EUR/CHF",
        "symbol": SYMBOL, "date_utc": f"{YEAR}-01-{DAY}",
        "point_value": POINT_VALUE,
        "n_hours_with_data": int(sum(1 for h in all_hours.values() if len(h) > 0)),
        "n_hours_empty": int(sum(1 for h in all_hours.values() if len(h) == 0)),
        "per_hour_tick_counts": {str(h): int(len(all_hours[h])) for h in range(24)},
        "total_ticks_day": int(total_ticks),
        "announcement_hour_utc": ANNOUNCEMENT_HOUR_UTC, "announcement_minute_utc": ANNOUNCEMENT_MINUTE_UTC,
        "announcement_ms_since_midnight_utc": announcement_ms,
        "split_idx": split_idx,
        "price_5min_before_announcement": price_5min_before,
        "price_just_before_split": price_just_before,
        "price_just_after_split": price_just_after,
        "price_5min_after_announcement": price_5min_after,
        "max_single_tick_jump_within_5min_of_split": max_jump_near_split,
        "median_inter_tick_dt_seconds_full_day": median_dt_s,
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
    }
    with open(os.path.join(OUT_DIR, "eurchf_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote eurchf_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
