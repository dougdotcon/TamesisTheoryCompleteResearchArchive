"""
Gap (c) -- SOC-redundancy check, MANDATORY before touching any NEW real
data this round. Reuses data and PRE/POST segment definitions ALREADY
committed and locked by `soc_avalanches` (Ridgecrest 2019 seismicity,
GOES XRS solar flares) -- no new download, no new segment definition.

Computes xi_Hill (gap (a) of ../METHODOLOGY_NOTE.md, via
`evt_hill_common.select_k_star`, UNMODIFIED) on the raw continuous
event magnitude/energy series (NOT on soc_avalanches's avalanche
extraction -- METHODOLOGY_NOTE.md gap (c) explicitly wants the tail
behavior of the raw continuous quantity), on the EXACT SAME PRE/POST
segments `soc_avalanches` already locked (same time boundaries, same
Mc completeness cut for Ridgecrest, same single-instrument G15 filter
for GOES), for BOTH the primary and the robustness (50%-by-count)
variant of each domain -- so the redundancy check has the same 4
(domain x variant) data points `soc_avalanches`'s own RESULTS_SUMMARY.md
table reports `tau` for.

Segment definitions replicated from
`soc_avalanches/analysis/result_ridgecrest.json` and
`soc_avalanches/analysis/result_goes_flares.json` (`provenance` /
`segments` keys) -- verified below to reproduce IDENTICAL n_events per
segment as those already-committed result files before any xi_Hill is
computed, as a hard check that the segment replication is exact, not
approximate.

Raw continuous quantity used per domain (declared choice, since
METHODOLOGY_NOTE.md gap (c) says "magnitude/energy" without picking
one): Ridgecrest -> seismic ENERGY (Gutenberg-Richter energy-magnitude
relation, log10(E_joules) = 1.5*M + 4.8), NOT magnitude directly --
magnitude's upper tail is close to EXPONENTIAL (Gutenberg-Richter is a
straight line in linear-magnitude/log-count space), which does not have
a well-defined regularly-varying Hill tail index; energy is the
monotonic transform of magnitude that IS heavy-tailed/power-law by
construction (this is the standard reason Gutenberg-Richter is usually
re-expressed as a power law in energy/seismic moment, not in magnitude,
in the SOC/self-organized-criticality literature this candidate itself
descends from). GOES flares -> peak X-ray FLUX (W/m^2) directly, parsed
from column [72:79] of the raw `goes-xrs-report_*.txt` fixed-width
format (documented in `soc_avalanches/analysis/result_goes_flares.json`
`provenance.file_format.columns_used`, NOT used by soc_avalanches's own
pipeline, which only used the event begin-time column) -- already a
naturally heavy-tailed physical quantity (Lu & Hamilton 1991), no
transform needed.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from evt_hill_common import select_k_star, subsample_segment, MIN_N_PER_SEGMENT

SOC_DIR = Path(__file__).resolve().parents[2] / "soc_avalanches"
SOC_DATA = SOC_DIR / "data"
SOC_ANALYSIS = SOC_DIR / "analysis"


def _xi_report(x, seed):
    x_sub, sub_info = subsample_segment(np.asarray(x, dtype=float))
    r = select_k_star(x_sub, np.random.default_rng(seed))
    r["subsampling"] = sub_info
    return r


# ---------------------------------------------------------------------
# Ridgecrest (seismicity) -- exact segment replication of
# soc_avalanches/analysis/result_ridgecrest.json
# ---------------------------------------------------------------------

def ridgecrest_segments():
    df = pd.read_csv(SOC_DATA / "ridgecrest_catalog.csv", usecols=["time", "mag"])
    df["time"] = pd.to_datetime(df["time"], utc=True, format="ISO8601")
    df["t_epoch"] = df["time"].astype("int64") / 1e9

    win_start = pd.Timestamp("2019-07-04T00:00:00Z")
    win_end = pd.Timestamp("2019-09-04T00:00:00Z")
    mainshock = pd.Timestamp("2019-07-06T03:19:53.040Z")
    Mc_final = 1.35  # soc_avalanches result_ridgecrest.json: mc_determination.Mc_final

    df = df.sort_values("time")
    pre_primary = df[(df.time >= win_start) & (df.time < mainshock) & (df.mag >= Mc_final)]
    post_primary = df[(df.time >= mainshock) & (df.time < win_end) & (df.mag >= Mc_final)]

    # robustness: most-recent 50% by COUNT of pre_primary; 50% by COUNT of
    # post_primary closest to the transition (i.e. the earliest half) --
    # same wording as soc_avalanches's segments.*_robustness_* keys.
    n_pre_half = len(pre_primary) // 2
    n_post_half = len(post_primary) // 2
    pre_robust = pre_primary.iloc[-(len(pre_primary) - n_pre_half):]  # most recent (last) 50% by count
    post_robust = post_primary.iloc[: len(post_primary) - n_post_half]  # earliest 50% by count

    # Gutenberg-Richter energy-magnitude relation (Joules)
    def energy(mag):
        return 10.0 ** (1.5 * mag + 4.8)

    out = {
        "pre_primary": {"mag": pre_primary["mag"].values, "energy": energy(pre_primary["mag"].values),
                         "n_events": int(len(pre_primary)),
                         "time_range_utc": [str(pre_primary.time.min()), str(pre_primary.time.max())]},
        "post_primary": {"mag": post_primary["mag"].values, "energy": energy(post_primary["mag"].values),
                          "n_events": int(len(post_primary)),
                          "time_range_utc": [str(post_primary.time.min()), str(post_primary.time.max())]},
        "pre_robustness": {"mag": pre_robust["mag"].values, "energy": energy(pre_robust["mag"].values),
                            "n_events": int(len(pre_robust)),
                            "time_range_utc": [str(pre_robust.time.min()), str(pre_robust.time.max())]},
        "post_robustness": {"mag": post_robust["mag"].values, "energy": energy(post_robust["mag"].values),
                             "n_events": int(len(post_robust)),
                             "time_range_utc": [str(post_robust.time.min()), str(post_robust.time.max())]},
        "Mc_final": Mc_final,
    }
    return out


# ---------------------------------------------------------------------
# GOES XRS solar flares -- exact segment replication of
# soc_avalanches/analysis/result_goes_flares.json
# ---------------------------------------------------------------------

_GOES_LINE_RE = re.compile(r"^\d{11}")


def _parse_goes_file(path):
    """Parse one goes-xrs-report_*.txt file: returns list of
    (datetime_utc, satellite_code, peak_flux_W_m2)."""
    rows = []
    with open(path, "r") as f:
        for line in f:
            if len(line) < 79 or not _GOES_LINE_RE.match(line):
                continue
            yy_mm_dd = line[5:11]
            begin_hhmm = line[13:17]
            sat = line[67:70].strip()
            flux_str = line[72:79].strip()
            if not (yy_mm_dd.isdigit() and begin_hhmm.isdigit() and len(begin_hhmm) == 4):
                continue
            try:
                flux = float(flux_str)
            except ValueError:
                continue
            year = 2000 + int(yy_mm_dd[0:2])
            month = int(yy_mm_dd[2:4])
            day = int(yy_mm_dd[4:6])
            hh = int(begin_hhmm[0:2])
            mm = int(begin_hhmm[2:4])
            if hh > 23 or mm > 59:
                continue
            try:
                ts = pd.Timestamp(year=year, month=month, day=day, hour=hh, minute=mm, tz="UTC")
            except ValueError:
                continue
            rows.append((ts, sat, flux))
    return rows


def goes_segments():
    files = [
        SOC_DATA / "goes-xrs-report_2014.txt",
        SOC_DATA / "goes-xrs-report_2015_modifiedreplacedmissingrows.txt",
        SOC_DATA / "goes-xrs-report_2016.txt",
        SOC_DATA / "goes-xrs-report_2017-ytd.txt",
    ]
    rows = []
    for fp in files:
        rows.extend(_parse_goes_file(fp))
    df = pd.DataFrame(rows, columns=["time", "sat", "flux"])
    df = df[df["sat"] == "G15"].sort_values("time").reset_index(drop=True)

    transition = pd.Timestamp("2014-04-01T00:00:00Z")
    pre_primary = df[df.time < transition]
    post_primary = df[df.time >= transition]

    n_pre_half = len(pre_primary) // 2
    n_post_half = len(post_primary) // 2
    pre_robust = pre_primary.iloc[-(len(pre_primary) - n_pre_half):]
    post_robust = post_primary.iloc[: len(post_primary) - n_post_half]

    out = {
        "pre_primary": {"flux": pre_primary["flux"].values, "n_events": int(len(pre_primary)),
                         "time_range_utc": [str(pre_primary.time.min()), str(pre_primary.time.max())]},
        "post_primary": {"flux": post_primary["flux"].values, "n_events": int(len(post_primary)),
                          "time_range_utc": [str(post_primary.time.min()), str(post_primary.time.max())]},
        "pre_robustness": {"flux": pre_robust["flux"].values, "n_events": int(len(pre_robust)),
                            "time_range_utc": [str(pre_robust.time.min()), str(pre_robust.time.max())]},
        "post_robustness": {"flux": post_robust["flux"].values, "n_events": int(len(post_robust)),
                             "time_range_utc": [str(post_robust.time.min()), str(post_robust.time.max())]},
    }
    return out


def main():
    rc = ridgecrest_segments()
    goes = goes_segments()

    # Hard check: segment replication must reproduce the EXACT same
    # n_events soc_avalanches's own already-committed result files
    # report, before any xi_Hill is computed on top of it.
    soc_rc = json.load(open(SOC_ANALYSIS / "result_ridgecrest.json"))
    soc_goes = json.load(open(SOC_ANALYSIS / "result_goes_flares.json"))

    expected = {
        "rc_pre_primary": soc_rc["segments"]["pre_primary"]["n_events"],
        "rc_post_primary": soc_rc["segments"]["post_primary"]["n_events"],
        "rc_pre_robust": soc_rc["segments"]["pre_robustness_most_recent_50pct_by_count"]["n_events"],
        "rc_post_robust": soc_rc["segments"]["post_robustness_closest_50pct_by_count"]["n_events"],
        "goes_pre_primary": soc_goes["provenance"]["segment_definition"]["pre_primary"]["n_events"],
        "goes_post_primary": soc_goes["provenance"]["segment_definition"]["post_primary"]["n_events"],
        "goes_pre_robust": soc_goes["provenance"]["segment_definition"]["pre_robustness"]["n_events"],
        "goes_post_robust": soc_goes["provenance"]["segment_definition"]["post_robustness"]["n_events"],
    }
    actual = {
        "rc_pre_primary": rc["pre_primary"]["n_events"],
        "rc_post_primary": rc["post_primary"]["n_events"],
        "rc_pre_robust": rc["pre_robustness"]["n_events"],
        "rc_post_robust": rc["post_robustness"]["n_events"],
        "goes_pre_primary": goes["pre_primary"]["n_events"],
        "goes_post_primary": goes["post_primary"]["n_events"],
        "goes_pre_robust": goes["pre_robustness"]["n_events"],
        "goes_post_robust": goes["post_robustness"]["n_events"],
    }
    mismatches = {k: (expected[k], actual[k]) for k in expected if expected[k] != actual[k]}
    segment_replication_check = {
        "expected_n_events": expected, "actual_n_events": actual,
        "exact_match": len(mismatches) == 0, "mismatches": mismatches,
    }
    print("segment replication check:", "EXACT MATCH" if not mismatches else f"MISMATCHES: {mismatches}")

    # xi_Hill on the raw continuous quantity, per domain/variant
    seed = 12345
    results = {}
    for variant in ["primary", "robustness"]:
        pre_key = "pre_primary" if variant == "primary" else "pre_robustness"
        post_key = "post_primary" if variant == "primary" else "post_robustness"

        rc_pre_r = _xi_report(rc[pre_key]["energy"], seed + 1)
        rc_post_r = _xi_report(rc[post_key]["energy"], seed + 2)
        goes_pre_r = _xi_report(goes[pre_key]["flux"], seed + 3)
        goes_post_r = _xi_report(goes[post_key]["flux"], seed + 4)

        results[variant] = {
            "ridgecrest": {
                "pre": rc_pre_r, "post": rc_post_r,
                "n_events_pre": rc[pre_key]["n_events"], "n_events_post": rc[post_key]["n_events"],
                "time_range_pre": rc[pre_key]["time_range_utc"], "time_range_post": rc[post_key]["time_range_utc"],
                "delta_xi_Hill": (rc_post_r.get("xi_Hill") - rc_pre_r.get("xi_Hill"))
                                 if rc_pre_r.get("status") == "ok" and rc_post_r.get("status") == "ok" else None,
            },
            "goes_flares": {
                "pre": goes_pre_r, "post": goes_post_r,
                "n_events_pre": goes[pre_key]["n_events"], "n_events_post": goes[post_key]["n_events"],
                "time_range_pre": goes[pre_key]["time_range_utc"], "time_range_post": goes[post_key]["time_range_utc"],
                "delta_xi_Hill": (goes_post_r.get("xi_Hill") - goes_pre_r.get("xi_Hill"))
                                 if goes_pre_r.get("status") == "ok" and goes_post_r.get("status") == "ok" else None,
            },
        }

    # SOC's own tau values, from the already-committed result files
    # (RESULTS_SUMMARY.md table), reused verbatim -- NOT recomputed here.
    soc_tau = {
        "primary": {
            "ridgecrest": {"tau_pre": None, "tau_post": soc_rc["results"]["primary"]["tau_post"],
                           "note": "PRE primary has only 9 avalanches -- tau_pre undefined in soc_avalanches itself"},
            "goes_flares": {"tau_pre": soc_goes["results"]["primary"]["tau_pre"],
                             "tau_post": soc_goes["results"]["primary"]["tau_post"]},
        },
        "robustness": {
            "ridgecrest": {
                "tau_pre": soc_rc["results"]["segment_selection_robustness_50pct_split"]["tau_pre"],
                "tau_post": soc_rc["results"]["segment_selection_robustness_50pct_split"]["tau_post"],
            },
            "goes_flares": {
                "tau_pre": soc_goes["results"]["robustness_50pct_nearest_transition"]["tau_pre"],
                "tau_post": soc_goes["results"]["robustness_50pct_nearest_transition"]["tau_post"],
            },
        },
    }
    for variant in soc_tau:
        for domain in soc_tau[variant]:
            tp = soc_tau[variant][domain].get("tau_pre")
            tq = soc_tau[variant][domain].get("tau_post")
            soc_tau[variant][domain]["delta_tau"] = (tq - tp) if (tp is not None and tq is not None) else None

    # Cross-domain/variant correlation between xi_Hill (this candidate)
    # and tau (soc_avalanches's own published channel) -- the decisive
    # redundancy question of gap (c).
    pairs = []
    for variant in ["primary", "robustness"]:
        for domain_key, soc_key in [("ridgecrest", "ridgecrest"), ("goes_flares", "goes_flares")]:
            d_xi = results[variant][domain_key]["delta_xi_Hill"]
            d_tau = soc_tau[variant][soc_key]["delta_tau"]
            if d_xi is not None and d_tau is not None:
                # Sign-convention note (important for interpretation, not
                # just bookkeeping): xi_Hill is INCREASING in tail heaviness
                # (larger xi = heavier power-law tail, P(X>x)~x^-alpha,
                # xi=1/alpha), while tau (avalanche-size power law,
                # P(s)~s^-tau) is DECREASING in tail heaviness (smaller tau
                # = heavier tail). If xi_Hill and tau were tracking the SAME
                # underlying "how heavy is the tail" factor, delta_xi_Hill
                # and delta_tau should be NEGATIVELY correlated raw, i.e.
                # delta_xi_Hill and (-delta_tau) POSITIVELY correlated. Both
                # are reported below -- do not read the raw (non-sign-
                # adjusted) correlation alone as a redundancy verdict.
                pairs.append({
                    "variant": variant, "domain": domain_key,
                    "delta_xi_Hill": d_xi, "delta_tau": d_tau,
                    "delta_tau_sign_flipped_for_heaviness_convention": -d_tau,
                    "same_direction_tail_heaviness_change": bool(np.sign(d_xi) == np.sign(-d_tau)),
                })

    corr = None
    corr_sign_adjusted = None
    n_same_direction = None
    if len(pairs) >= 2:
        xs = np.array([p["delta_xi_Hill"] for p in pairs])
        ys = np.array([p["delta_tau"] for p in pairs])
        if np.std(xs) > 0 and np.std(ys) > 0:
            corr = float(np.corrcoef(xs, ys)[0, 1])
            corr_sign_adjusted = float(np.corrcoef(xs, -ys)[0, 1])
        n_same_direction = int(sum(p["same_direction_tail_heaviness_change"] for p in pairs))

    out = {
        "candidate": "evt-hill", "test_line": "DISC-TRI-RG-001", "gap": "c",
        "raw_quantity_used": {
            "ridgecrest": "seismic energy, Gutenberg-Richter log10(E_joules)=1.5*mag+4.8 "
                          "(declared choice -- magnitude itself has an exponential, not power-law, "
                          "upper tail; see module docstring)",
            "goes_flares": "peak X-ray flux, W/m^2, column [72:79] of raw goes-xrs-report_*.txt "
                           "(not used by soc_avalanches's own pipeline, which only used event begin-time)",
        },
        "segment_replication_check": segment_replication_check,
        "xi_Hill_results": results,
        "soc_tau_reused_from_result_json": soc_tau,
        "delta_xi_Hill_vs_delta_tau_pairs": pairs,
        "n_comparable_pairs": len(pairs),
        "pearson_correlation_delta_xi_Hill_vs_delta_tau_RAW": corr,
        "pearson_correlation_delta_xi_Hill_vs_NEGATIVE_delta_tau_SIGN_ADJUSTED_FOR_HEAVINESS_CONVENTION": corr_sign_adjusted,
        "n_pairs_with_same_direction_tail_heaviness_change": n_same_direction,
        "caveat": "n=3 comparable pairs (Ridgecrest primary excluded -- SOC's own tau_pre is undefined there, "
                  "only 9 avalanches). A Pearson correlation on 3 points has 1 degree of freedom and is NOT "
                  "statistically meaningful on its own -- reported for completeness, interpreted qualitatively "
                  "(same-direction count) in VALIDATION_NOTE.md, not as a hypothesis-test verdict.",
    }
    with open(Path(__file__).resolve().parent / "soc_redundancy_check.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps({
        "n_comparable_pairs": len(pairs), "pairs": pairs,
        "correlation_raw": corr, "correlation_sign_adjusted": corr_sign_adjusted,
        "n_same_direction": n_same_direction,
    }, indent=2))
    print("Wrote soc_redundancy_check.json")


if __name__ == "__main__":
    main()
