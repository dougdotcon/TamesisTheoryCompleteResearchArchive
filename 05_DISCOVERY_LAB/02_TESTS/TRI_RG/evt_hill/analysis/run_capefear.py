"""
Real-domain run 2/2 -- USGS NWIS, station 02105769 (Cape Fear River at
Lock 1 near Kelly, NC), Hurricane Florence. METHODOLOGY_NOTE.md Gap (d):
  Transition = Florence landfall, 2018-09-14 (NHC-documented; landfall
  near Wrightsville Beach, NC ~07:15 EDT as a Category 1 hurricane after
  weakening from peak Category 4 intensity over open water days earlier
  -- METHODOLOGY_NOTE.md's own text says "categoria 4" but the DATE it
  fixes, 2018-09-14, is what is used here unmodified; the category
  detail is a factual label in the note's prose, not a parameter this
  pipeline consumes).
  PRE = gauge height before landfall, using the long DAILY-VALUE history
  (2000-2018, confirmed accessible by the Fase 0.6 survey) -- the daily
  MAXIMUM statistic (statCd=00001, not the daily MEAN) is used
  specifically to keep PRE and POST as comparable as the available data
  allows in what they represent (a within-day extreme), see the
  "measurement-frequency caveat" section of PROVENANCE_CAPEFEAR.md.
  POST = instantaneous (15-minute) gauge height from landfall through
  recession back toward baseline or the next documented event, whichever
  comes first (weeks, not just the peak days) -- see
  PROVENANCE_CAPEFEAR.md for the exact, pre-declared-mechanical
  recession-threshold rule (baseline = mean of Aug-2018 daily-max
  readings, before any storm influence; PRIMARY = first 3 consecutive
  days back within 10% of that baseline; ROBUSTNESS = first 3
  consecutive days back within 5%).

Confound check REQUIRED by Gap (d) if any significant finding emerges:
the station is at "Lock 1" (a lock/dam) -- gate-operation changes could
alter the exceedance statistic mechanically, independent of anything
climatic. See the confound-check section at the bottom of this script
and CONFOUND_CHECK_CAPEFEAR.md.

Calls `run_evt_hill_analysis` from `evt_hill_common.py` UNMODIFIED.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evt_hill_common import run_evt_hill_analysis, SEED

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

TRANSITION = pd.Timestamp("2018-09-14T00:00:00Z")
BASELINE_WINDOW = (pd.Timestamp("2018-08-01T00:00:00Z"), pd.Timestamp("2018-09-01T00:00:00Z"))


def load_pre_daily_max():
    with open(DATA_DIR / "capefear_pre_dailymax.json") as f:
        d = json.load(f)
    vals = d["value"]["timeSeries"][0]["values"][0]["value"]
    df = pd.DataFrame(vals)
    df["dateTime"] = pd.to_datetime(df["dateTime"], utc=True)
    df["value"] = df["value"].astype(float)
    return df.sort_values("dateTime").reset_index(drop=True)


def load_post_instant():
    with open(DATA_DIR / "capefear_post_instant_wide.json") as f:
        d = json.load(f)
    vals = d["value"]["timeSeries"][0]["values"][0]["value"]
    df = pd.DataFrame(vals)
    df["dateTime"] = pd.to_datetime(df["dateTime"], utc=True)
    df["value"] = df["value"].astype(float)
    return df.sort_values("dateTime").reset_index(drop=True)


def find_recession_end(post_df, baseline, pct_tolerance, n_consecutive_days):
    """First date (inclusive) at which `n_consecutive_days` consecutive
    calendar days ALL have daily-max <= baseline*(1+pct_tolerance).
    Mechanical, pre-declared rule -- see module docstring. Returns the
    date of the LAST day of that streak (i.e. the POST window end date).
    """
    daily_max = post_df.groupby(post_df["dateTime"].dt.date)["value"].max()
    threshold = baseline * (1 + pct_tolerance)
    below = daily_max <= threshold
    run_len = 0
    for date, ok in below.items():
        run_len = run_len + 1 if ok else 0
        if run_len >= n_consecutive_days:
            return date
    return None


def main():
    pre_df = load_pre_daily_max()
    post_df = load_post_instant()

    baseline_mask = (pre_df["dateTime"] >= BASELINE_WINDOW[0]) & (pre_df["dateTime"] < BASELINE_WINDOW[1])
    baseline = float(pre_df.loc[baseline_mask, "value"].mean())
    print(f"PRE baseline (Aug-2018 daily-max mean, pre-storm): {baseline:.3f} ft "
          f"(n={baseline_mask.sum()} days)")

    variants = {
        "primary": {"pct_tolerance": 0.10, "n_consecutive_days": 3},
        "robustness": {"pct_tolerance": 0.05, "n_consecutive_days": 3},
    }

    pre_series = pre_df[pre_df["dateTime"] < TRANSITION]["value"].values
    print(f"n_pre (daily max, {pre_df['dateTime'].min().date()} to "
          f"{pre_df[pre_df['dateTime'] < TRANSITION]['dateTime'].max().date()}) = {len(pre_series)}")

    all_out = {}
    for variant_name, cfg in variants.items():
        end_date = find_recession_end(post_df, baseline, cfg["pct_tolerance"], cfg["n_consecutive_days"])
        if end_date is None:
            print(f"[{variant_name}] recession threshold never met in available window -- skipping")
            continue
        end_ts = pd.Timestamp(end_date, tz="UTC") + pd.Timedelta(days=1)  # inclusive of end_date
        post_series = post_df[(post_df["dateTime"] >= TRANSITION) & (post_df["dateTime"] < end_ts)]["value"].values
        print(f"[{variant_name}] recession threshold ({cfg['pct_tolerance']*100:.0f}%, "
              f"{cfg['n_consecutive_days']} consecutive days) met by {end_date} -- "
              f"POST window 2018-09-14 to {end_date}, n_post={len(post_series)}")

        result = run_evt_hill_analysis(pre_series, post_series, seed=SEED, n_randomizations=200)
        print(f"  status: {result.get('status')}")
        if result.get("status") == "ok":
            print(f"  xi_Hill pre/post: {result['real_pre']['xi_Hill']:.4f} / {result['real_post']['xi_Hill']:.4f}"
                  f"  delta={result['delta_xi_Hill']:.4f}  p={result['p_xi_Hill']}")
            print(f"  xi_MLE  pre/post: {result['real_pre']['xi_MLE']} / {result['real_post']['xi_MLE']}"
                  f"  delta={result['delta_xi_MLE']}  p={result['p_xi_MLE']}")

        all_out[variant_name] = {
            "recession_rule": cfg,
            "baseline_ft": baseline,
            "post_window": ["2018-09-14", str(end_date)],
            "n_pre": int(len(pre_series)),
            "n_post": int(len(post_series)),
            "result": result,
        }

    out = {
        "domain": "capefear_hurricane_florence_2018",
        "candidate": "evt-hill",
        "test_line": "DISC-TRI-RG-001",
        "provenance_file": "data/PROVENANCE_CAPEFEAR.md",
        "transition_date": "2018-09-14",
        "baseline_computation": {"window": ["2018-08-01", "2018-09-01"], "baseline_ft": baseline},
        "measurement_frequency_caveat": "PRE is daily-MAX gauge height (statCd=00001), POST is raw "
            "15-minute instantaneous gauge height. Chosen to minimize (not eliminate) a sampling-density "
            "mismatch -- instantaneous data captures more sub-peak readings than a daily maximum, which "
            "could inflate/alter the apparent tail heaviness of POST independent of any genuine hydrological "
            "change. Declared explicitly, not corrected, since no instantaneous PRE baseline of comparable "
            "length is available for this station (period-of-record limitation confirmed during data pull).",
        "variants": all_out,
    }
    out_path = Path(__file__).resolve().parent / "result_capefear.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
