import wfdb
import numpy as np
import json

DATA_DIR = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/TRI_RG/dfa_multiscale_entropy/data"
REC = f"{DATA_DIR}/a04"

ann_apn = wfdb.rdann(REC, "apn")
ann_qrs = wfdb.rdann(REC, "qrs")

fs = 100.0
labels = ann_apn.symbol
samples_apn = ann_apn.sample
print("n_minute_labels", len(labels))
print("unique symbols", set(labels))

# full run-length sequence of labels
runs = []
cur = labels[0]
start = 0
for i in range(1, len(labels)):
    if labels[i] != cur:
        runs.append((cur, start, i - 1, i - start))
        cur = labels[i]
        start = i
runs.append((cur, start, len(labels) - 1, len(labels) - start))
print("\nAll label runs (symbol, minute_start, minute_end, n_minutes):")
for r in runs:
    print(r)

qrs_samples = ann_qrs.sample
rr = np.diff(qrs_samples) / fs  # seconds
print("\ntotal beats:", len(qrs_samples))
print("total RR intervals:", len(rr))
print("RR range (s):", rr.min(), rr.max())

# histogram-ish outlier detection: successive RR ratio jumps
ratios = rr[1:] / rr[:-1]
big_jump_mask = (ratios > 1.2) | (ratios < 1/1.2)
print("\nFraction of successive RR pairs with >20% jump (whole record):", big_jump_mask.mean())

def segment_rr(lo_min, hi_min_inclusive):
    lo_samp = lo_min * 6000
    hi_samp = (hi_min_inclusive + 1) * 6000
    # beat indices within [lo_samp, hi_samp)
    beat_mask = (qrs_samples >= lo_samp) & (qrs_samples < hi_samp)
    beats = qrs_samples[beat_mask]
    rr_seg = np.diff(beats) / fs
    return rr_seg, beats

pre_rr, pre_beats = segment_rr(0, 34)
post_rr, post_beats = segment_rr(35, 174)
print("\nPRE: n_rr=", len(pre_rr), "min/max=", pre_rr.min(), pre_rr.max(), "mean=", pre_rr.mean(), "std=", pre_rr.std())
print("POST: n_rr=", len(post_rr), "min/max=", post_rr.min(), post_rr.max(), "mean=", post_rr.mean(), "std=", post_rr.std())

def outlier_stats(rr_seg, name):
    ratios = rr_seg[1:] / rr_seg[:-1]
    jump_mask = (ratios > 1.2) | (ratios < 1/1.2)
    extreme_mask = (ratios > 1.5) | (ratios < 1/1.5)
    print(f"{name}: frac >20% jump = {jump_mask.mean():.4f} ({jump_mask.sum()} of {len(ratios)}); "
          f"frac >50% jump = {extreme_mask.mean():.4f} ({extreme_mask.sum()} of {len(ratios)})")
    # percentiles
    p = np.percentile(rr_seg, [0.5, 1, 5, 50, 95, 99, 99.5])
    print(f"  percentiles [0.5,1,5,50,95,99,99.5]: {p}")

outlier_stats(pre_rr, "PRE")
outlier_stats(post_rr, "POST")

# Look for other N runs later in the night that could serve as "late night, no apnea" controls
print("\nSearching for N runs of length >= 10 minutes after the POST block (minute > 174):")
for sym, s0, s1, n in runs:
    if sym == "N" and s0 > 174:
        print(f"  N run: minutes [{s0},{s1}], n_minutes={n}")

print("\nAll runs >= 10 minutes anywhere in the record:")
for sym, s0, s1, n in runs:
    if n >= 10:
        print(f"  {sym} run: minutes [{s0},{s1}], n_minutes={n}")

# save runs to json for later use
with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/a04_runs.json", "w") as f:
    json.dump({"runs": runs, "n_labels": len(labels)}, f, indent=2)
