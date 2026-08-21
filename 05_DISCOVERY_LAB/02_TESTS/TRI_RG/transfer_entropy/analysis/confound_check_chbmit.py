"""
Adversarial reproduction / null-discovery check for the CHB-MIT domain,
triggered by ONE isolated p<0.05 finding in result_chbmit_robust.json
(STE_sum, circular-shift null ONLY, p=0.025 -- the SAME channel's IAAFT
null on the SAME variant gives p=0.725, and the PRIMARY variant shows
nothing for STE_sum at all, p=0.425/0.18). Weak/isolated by itself
(consistent with the ~8% base false-positive rate observed in
VALIDATION_NOTE.md's negative control), but per this line's protocol ANY
p<0.05 triggers the mandatory adversarial check, and this candidate's
own pre-named confound (volume conduction, Nolte et al. 2008) must be
tested explicitly.

Check: nearby (electrode-sharing) vs. distant (current) channel pair,
same seizure transition. If a channel pair with NO physiological reason
to show ictal coupling (arbitrarily distant, e.g. right-hemisphere
occipital vs left-hemisphere frontal) shows the SAME or STRONGER
"significance" than our tested pair, that is evidence of generic
domain/pipeline sensitivity, not a channel-specific effect -- and if a
pair that SHARES an electrode with T7-P7 (F7-T7, maximal volume-
conduction risk) shows a much stronger effect, that specifically
implicates volume conduction.

Writes confound_check_chbmit_results.json.
"""
import io
import json
import os
import sys
import time
import urllib.request

import numpy as np
import pyedflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import te_common as te  # noqa: E402

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(ANALYSIS_DIR), "data")
EDF_URL = "https://physionet.org/files/chbmit/1.0.0/chb01/chb01_03.edf"
SEIZURE_START_S = 2996

# Adversarial pairs (physiologically implausible / volume-conduction-prone)
PAIR_NEARBY = ("F7-T7", "T7-P7")       # shares electrode T7 with our real Y channel -- maximal volume-conduction risk
PAIR_DISTANT = ("P4-O2", "F8-T8")      # right-hemisphere posterior vs right-hemisphere anterior-temporal, no shared electrode, arbitrary


def fetch_edf_channels(url, chan_names, timeout=300):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        raw = resp.read()
    tmp_path = os.path.join(ANALYSIS_DIR, "_chb01_03_tmp_confound.edf")
    with open(tmp_path, "wb") as f:
        f.write(raw)
    f = pyedflib.EdfReader(tmp_path)
    labels = f.getSignalLabels()
    out = {}
    fs = None
    for name in chan_names:
        assert name in labels, f"{name} not in {labels}"
        idx = labels.index(name)
        fs_c = f.getSampleFrequency(idx)
        if fs is None:
            fs = fs_c
        assert fs_c == fs
        out[name] = f.readSignal(idx)
    f.close()
    os.remove(tmp_path)
    return out, float(fs)


def run_pair(x, y, onset_idx, label):
    pre_x, pre_y = x[:onset_idx], y[:onset_idx]
    post_x, post_y = x[onset_idx:], y[onset_idx:]
    t0 = time.time()
    res = te.run_te_analysis(pre_x, pre_y, post_x, post_y)
    dt = time.time() - t0
    print(f"  [{label}] status={res['status']} ({dt:.1f}s)", flush=True)
    if res["status"] == "ok":
        print(f"    delta={res['delta']}", flush=True)
        print(f"    p_iaaft={res['p_iaaft']}", flush=True)
        print(f"    p_circular_shift={res['p_circular_shift']}", flush=True)
    return res


def summarize(res):
    if res["status"] != "ok":
        return {"status": res["status"]}
    return {"status": "ok", "delta": res["delta"], "p_iaaft": res["p_iaaft"],
            "p_circular_shift": res["p_circular_shift"]}


def main():
    print("Fetching chb01_03.edf channels for adversarial pairs ...", flush=True)
    all_chans = set(PAIR_NEARBY) | set(PAIR_DISTANT)
    signals, fs = fetch_edf_channels(EDF_URL, sorted(all_chans))
    print(f"  fs={fs}Hz, channels loaded: {list(signals.keys())}", flush=True)
    onset_idx = int(round(SEIZURE_START_S * fs))

    out = {}

    print(f"\n=== Nearby pair (shares electrode T7 with real Y): {PAIR_NEARBY} ===", flush=True)
    res_nearby = run_pair(signals[PAIR_NEARBY[0]], signals[PAIR_NEARBY[1]], onset_idx, "nearby")
    out["nearby_pair"] = {"channels": list(PAIR_NEARBY), **summarize(res_nearby)}

    print(f"\n=== Distant/implausible pair: {PAIR_DISTANT} ===", flush=True)
    res_distant = run_pair(signals[PAIR_DISTANT[0]], signals[PAIR_DISTANT[1]], onset_idx, "distant")
    out["distant_pair"] = {"channels": list(PAIR_DISTANT), **summarize(res_distant)}

    with open(os.path.join(ANALYSIS_DIR, "confound_check_chbmit_results.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\nWrote confound_check_chbmit_results.json", flush=True)


if __name__ == "__main__":
    main()
