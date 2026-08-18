"""
Prepare PRE/POST segments (primary + robustness) for the 2 real domains,
per METHODOLOGY_NOTE.md Gap (c). Real data only, no fabrication -- every
value here comes directly from the downloaded files.
"""
import numpy as np
import datetime
import json

# ---------------------------------------------------------------------
# Domain 1: Geomagnetism -- NASA OMNI SYM-H, 2015, 5-min resolution
# ---------------------------------------------------------------------
years, doys, hours, mins, symh = [], [], [], [], []
with open("omni_5min2015.asc") as f:
    for line in f:
        p = line.split()
        years.append(int(p[0])); doys.append(int(p[1]))
        hours.append(int(p[2])); mins.append(int(p[3]))
        symh.append(int(p[41]))  # SYM/H, field 42 (1-indexed)

years = np.array(years); doys = np.array(doys)
hours = np.array(hours); mins = np.array(mins)
symh = np.array(symh, dtype=float)

# Build actual datetimes (Day is day-of-year, 1-indexed)
base = datetime.datetime(2015, 1, 1)
dts = np.array([
    base + datetime.timedelta(days=int(d - 1), hours=int(h), minutes=int(m))
    for d, h, m in zip(doys, hours, mins)
])

ssc = datetime.datetime(2015, 3, 17, 4, 45)   # Kamide & Kusano 2015, verified via web search
next_storm = datetime.datetime(2015, 6, 22, 0, 0)  # next documented major storm (Dst~-204/-208 nT), 22-25 June 2015

pre_mask = dts < ssc
post_mask = (dts >= ssc) & (dts < next_storm)

geo_pre_primary = symh[pre_mask]
geo_post_primary = symh[post_mask]

n_pre = len(geo_pre_primary)
n_post = len(geo_post_primary)
geo_pre_robust = geo_pre_primary[n_pre // 2:]     # most recent 50% by count
geo_post_robust = geo_post_primary[: n_post // 2]  # 50% closest to transition

print("=== Geomagnetic (SYM-H) ===")
print("PRE primary n =", n_pre, "range", dts[pre_mask][0], "to", dts[pre_mask][-1])
print("POST primary n =", n_post, "range", dts[post_mask][0], "to", dts[post_mask][-1])
print("PRE robust n =", len(geo_pre_robust))
print("POST robust n =", len(geo_post_robust))
print("any NaN in pre/post:", np.isnan(geo_pre_primary).any(), np.isnan(geo_post_primary).any())

np.save("geo_pre_primary.npy", geo_pre_primary)
np.save("geo_post_primary.npy", geo_post_primary)
np.save("geo_pre_robust.npy", geo_pre_robust)
np.save("geo_post_robust.npy", geo_post_robust)

# ---------------------------------------------------------------------
# Domain 2: Hydrology -- USGS 08074500 Whiteoak Bayou, gage height (00065, ft)
# ---------------------------------------------------------------------
def parse_usgs_rdb(path):
    dts_list, vals_list = [], []
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if p[0] == "agency_cd" or (len(p) > 0 and p[0].endswith("s") and p[0][:-1].isdigit()):
                continue  # header/format rows
            if len(p) < 5:
                continue
            agency, site, dt_str, tz, val = p[0], p[1], p[2], p[3], p[4]
            if agency != "USGS":
                continue
            try:
                val_f = float(val)
            except ValueError:
                continue  # missing/non-numeric (e.g. "Ice", blank) -- skip, do not fabricate
            try:
                dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            dts_list.append(dt)
            vals_list.append(val_f)
    return np.array(dts_list), np.array(vals_list, dtype=float)

pre_dts, pre_vals = parse_usgs_rdb("usgs_pre_raw.rdb")
post_dts, post_vals = parse_usgs_rdb("usgs_post_raw.rdb")

print("\n=== Hydrology (gage height, ft) ===")
print("PRE primary n =", len(pre_vals), "range", pre_dts[0] if len(pre_dts) else None, "to", pre_dts[-1] if len(pre_dts) else None)
print("POST primary n =", len(post_vals), "range", post_dts[0] if len(post_dts) else None, "to", post_dts[-1] if len(post_dts) else None)
print("PRE min/max ft:", pre_vals.min(), pre_vals.max())
print("POST min/max ft:", post_vals.min(), post_vals.max(), "(documented peak 44.31 expected in POST)")

n_pre_h = len(pre_vals)
n_post_h = len(post_vals)
hydro_pre_robust = pre_vals[n_pre_h // 2:]
hydro_post_robust = post_vals[: n_post_h // 2]

np.save("hydro_pre_primary.npy", pre_vals)
np.save("hydro_post_primary.npy", post_vals)
np.save("hydro_pre_robust.npy", hydro_pre_robust)
np.save("hydro_post_robust.npy", hydro_post_robust)

meta = {
    "geomagnetic": {
        "ssc_utc": str(ssc), "next_storm_utc": str(next_storm),
        "pre_primary_n": int(n_pre), "post_primary_n": int(n_post),
        "pre_robust_n": int(len(geo_pre_robust)), "post_robust_n": int(len(geo_post_robust)),
        "pre_primary_range": [str(dts[pre_mask][0]), str(dts[pre_mask][-1])],
        "post_primary_range": [str(dts[post_mask][0]), str(dts[post_mask][-1])],
    },
    "hydrology": {
        "transition_date": "2017-08-25",
        "pre_primary_n": int(n_pre_h), "post_primary_n": int(n_post_h),
        "pre_robust_n": int(len(hydro_pre_robust)), "post_robust_n": int(len(hydro_post_robust)),
        "pre_primary_range": [str(pre_dts[0]), str(pre_dts[-1])],
        "post_primary_range": [str(post_dts[0]), str(post_dts[-1])],
        "post_max_ft": float(post_vals.max()),
        "post_max_ft_datetime": str(post_dts[np.argmax(post_vals)]),
    },
}
with open("segments_meta.json", "w") as f:
    json.dump(meta, f, indent=2)
print("\nWrote segments_meta.json")
