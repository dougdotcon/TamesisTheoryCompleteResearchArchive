"""
Real-domain run 1/2 -- NOAA GHCN-Daily, station PDX (USW00024229), 2021
Pacific Northwest heat dome. METHODOLOGY_NOTE.md Gap (d):
  Transition = NWS Portland Excessive Heat Warning onset, 2021-06-25
  (verified via web search: NWS Portland issued the warning on
  2021-06-25 for Sat/Sun/Mon 2021-06-26 through 2021-06-28; peak TMAX
  46.7C on 2021-06-28 matches the documented all-time PDX record --
  confirms the date already fixed in METHODOLOGY_NOTE.md, no change).
  PRE = daily TMAX before 2021-06-25 (all available history back to
  2000-01-01, "several years" per orchestrator instruction).
  POST = daily TMAX from 2021-06-25 through the next documented heat
  event or end of July 2021, whichever comes first -- no other PNW heat
  event as extreme as the June 2021 dome is documented before
  2021-07-31, so the full end-of-July bound is used (the MORE GENEROUS
  of the two possible bounds, chosen to give POST the largest possible
  sample count, not to induce a particular outcome).

Calls `run_evt_hill_analysis` from `evt_hill_common.py` UNMODIFIED.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evt_hill_common import run_evt_hill_analysis, SEED

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_pdx_tmax():
    with open(DATA_DIR / "pdx_tmax_raw.json") as f:
        recs = json.load(f)
    rows = [(r["DATE"], float(r["TMAX"])) for r in recs if r.get("TMAX") not in (None, "")]
    rows.sort()
    return rows


def main():
    rows = load_pdx_tmax()
    transition = "2021-06-25"
    post_end = "2021-07-31"

    pre = [v for d, v in rows if d < transition]
    post = [v for d, v in rows if transition <= d <= post_end]

    print(f"n_pre={len(pre)} (from {rows[0][0]} to day before {transition})")
    print(f"n_post={len(post)} (from {transition} to {post_end})")

    result = run_evt_hill_analysis(pre, post, seed=SEED, n_randomizations=200)

    out = {
        "domain": "pdx_heat_wave_2021",
        "candidate": "evt-hill",
        "test_line": "DISC-TRI-RG-001",
        "provenance_file": "data/PROVENANCE_PDX.md",
        "transition_date": transition,
        "post_end_date": post_end,
        "n_pre_raw": len(pre),
        "n_post_raw": len(post),
        "result": result,
    }
    out_path = Path(__file__).resolve().parent / "result_pdx.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    print("status:", result.get("status"))
    if result.get("status") == "ok":
        print("xi_Hill pre/post:", result["real_pre"]["xi_Hill"], result["real_post"]["xi_Hill"])
        print("delta_xi_Hill:", result["delta_xi_Hill"], "p_xi_Hill:", result["p_xi_Hill"])
        print("delta_xi_MLE:", result["delta_xi_MLE"], "p_xi_MLE:", result["p_xi_MLE"])
    else:
        print("Non-ok status -- see result_pdx.json for full diagnostics.")
        if "real_pre" in result:
            print("  real_pre status:", result["real_pre"].get("status"))
        if "real_post" in result:
            print("  real_post status:", result["real_post"].get("status"))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
