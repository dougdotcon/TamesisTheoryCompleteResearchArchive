#!/usr/bin/env python3
"""Rebuild elev_reduction_results.json from the per-job part files.
Needed because four jobs of the first launch were killed by the OOM killer
(the cluster bootstrap used to materialise a B x n_rep x 5 array); they were
re-run individually with the same seeds after `elev_mc.py`'s bootstrap was
chunked.  Nothing else changed."""
import json, os
from elev_reduction import STRESS, REPS, SEED0

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
i = 0
for (n, b, c) in STRESS:
    for kind in ("src", "muA", "muB"):
        fn = os.path.join(HERE, "parts", f"red_{i:02d}_{kind}.json")
        if os.path.exists(fn):
            d = json.load(open(fn))
            d["kind"] = kind
            d["src"] = [n, b, c]
            rows.append(d)
        else:
            print("MISSING", fn)
        i += 1
json.dump(dict(seed0=SEED0, n_rep=REPS, rows=rows),
          open(os.path.join(HERE, "elev_reduction_results.json"), "w"), indent=1)
print(f"rebuilt with {len(rows)}/18 jobs")
