"""
Download and prepare PRE/POST daily-incidence segments (primary +
robustness) for the Italy COVID-19 first-wave national lockdown
transition, per ../METHODOLOGY_NOTE.md section 5.1. Real data only,
fetched directly from the public JHU CSSE GitHub raw CSV (no login/
token), no fabrication.

Transition (fixed a priori): national lockdown decree "Io resto a casa"
(DPCM), 2020-03-09.
PRE = daily incidence (first difference of cumulative confirmed cases,
  standard epidemiological convention avoiding the trivial monotonic
  autocorrelation of the raw cumulative series) from the first day with
  a nonzero case count through 2020-03-08 (inclusive).
POST = daily incidence from 2020-03-09 through 2020-03-21 (inclusive) --
  the day BEFORE the next documented national-scale policy confounder,
  the DPCM of 2020-03-22 (total shutdown of all non-essential production
  activity) -- avoids mixing two distinct national policy changes in the
  same POST segment.

Writes (into this same data/ directory):
  covid_italy_pre_primary.npy, covid_italy_post_primary.npy,
  covid_italy_pre_robust.npy, covid_italy_post_robust.npy,
  covid_italy_segments_meta.json
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta

import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
JHU_URL = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
           "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

LOCKDOWN_DATE = "2020-03-09"          # "Io resto a casa" DPCM
NEXT_CONFOUNDER_DATE = "2020-03-22"   # total non-essential shutdown DPCM


def fetch_csv():
    print(f"  fetching {JHU_URL}", flush=True)
    with urllib.request.urlopen(JHU_URL, timeout=120) as resp:
        text = resp.read().decode("utf-8")
    print(f"    {len(text)} bytes", flush=True)
    return text


def parse_italy_row(csv_text):
    lines = csv_text.strip().split("\n")
    header = lines[0].split(",")
    date_cols = header[4:]
    dates = [datetime.strptime(d, "%m/%d/%y") for d in date_cols]

    italy_line = None
    for line in lines[1:]:
        parts = line.split(",")
        # Province/State, Country/Region, Lat, Long, then daily counts
        if parts[1] == "Italy" and parts[0] == "":
            italy_line = parts
            break
    if italy_line is None:
        raise RuntimeError("Italy row not found in JHU CSV")

    counts = [int(float(v)) if v.strip() != "" else 0 for v in italy_line[4:]]
    assert len(counts) == len(dates), f"length mismatch: {len(counts)} counts vs {len(dates)} dates"
    return dates, np.array(counts, dtype=float)


def main():
    csv_text = fetch_csv()
    dates, cum_counts = parse_italy_row(csv_text)

    # daily incidence = first difference of cumulative counts
    incidence = np.diff(cum_counts)
    incidence_dates = dates[1:]  # incidence[i] corresponds to incidence_dates[i]

    # first day with a nonzero cumulative count (first confirmed case in Italy)
    first_case_idx = int(np.argmax(cum_counts > 0))
    first_case_date = dates[first_case_idx]
    print(f"First nonzero cumulative-case day: {first_case_date.date()}", flush=True)

    lockdown_dt = datetime.strptime(LOCKDOWN_DATE, "%Y-%m-%d")
    next_confounder_dt = datetime.strptime(NEXT_CONFOUNDER_DATE, "%Y-%m-%d")

    # PRE: incidence from first_case_date through the day before lockdown (2020-03-08 incl.)
    pre_mask = [(d >= first_case_date) and (d < lockdown_dt) for d in incidence_dates]
    # POST: incidence from lockdown_dt through the day before the next confounder
    post_mask = [(d >= lockdown_dt) and (d < next_confounder_dt) for d in incidence_dates]

    pre_primary = incidence[np.array(pre_mask)]
    post_primary = incidence[np.array(post_mask)]

    pre_dates_used = [d for d, m in zip(incidence_dates, pre_mask) if m]
    post_dates_used = [d for d, m in zip(incidence_dates, post_mask) if m]

    n_pre, n_post = len(pre_primary), len(post_primary)
    pre_robust = pre_primary[n_pre // 2:]
    post_robust = post_primary[: n_post // 2]

    print(f"PRE primary n={n_pre}  ({pre_dates_used[0].date()} .. {pre_dates_used[-1].date()})", flush=True)
    print(f"POST primary n={n_post}  ({post_dates_used[0].date()} .. {post_dates_used[-1].date()})", flush=True)
    print(f"PRE robust n={len(pre_robust)}  POST robust n={len(post_robust)}", flush=True)
    print(f"PRE primary values: {pre_primary.tolist()}", flush=True)
    print(f"POST primary values: {post_primary.tolist()}", flush=True)
    assert n_pre > 0 and n_post > 0

    np.save(os.path.join(OUT_DIR, "covid_italy_pre_primary.npy"), pre_primary)
    np.save(os.path.join(OUT_DIR, "covid_italy_post_primary.npy"), post_primary)
    np.save(os.path.join(OUT_DIR, "covid_italy_pre_robust.npy"), pre_robust)
    np.save(os.path.join(OUT_DIR, "covid_italy_post_robust.npy"), post_robust)

    meta = {
        "source": "JHU CSSE COVID-19 time_series_covid19_confirmed_global.csv (GitHub raw)",
        "url": JHU_URL,
        "series_used": "daily incidence (first difference of cumulative confirmed cases)",
        "country": "Italy",
        "transition_date": LOCKDOWN_DATE,
        "transition_description": "National lockdown decree \"Io resto a casa\" (DPCM), 2020-03-09",
        "post_boundary_date": NEXT_CONFOUNDER_DATE,
        "post_boundary_description": "DPCM total shutdown of non-essential production activity, 2020-03-22",
        "first_case_date": str(first_case_date.date()),
        "pre_date_range": [str(pre_dates_used[0].date()), str(pre_dates_used[-1].date())],
        "post_date_range": [str(post_dates_used[0].date()), str(post_dates_used[-1].date())],
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(pre_robust)), "post_robust_n": int(len(post_robust)),
        "pre_primary_values": pre_primary.tolist(),
        "post_primary_values": post_primary.tolist(),
    }
    with open(os.path.join(OUT_DIR, "covid_italy_segments_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("Wrote covid_italy_segments_meta.json", flush=True)


if __name__ == "__main__":
    main()
