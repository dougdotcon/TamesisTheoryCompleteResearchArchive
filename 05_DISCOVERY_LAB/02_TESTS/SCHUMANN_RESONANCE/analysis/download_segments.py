#!/usr/bin/env python3
"""
Download a small, deliberately-chosen real subset of the Sierra Nevada ELF
station 2014 archive (Zenodo record 6348691, DOI 10.5281/zenodo.6348691)
using HTTP Range requests, WITHOUT downloading the full 26.7 GB year zip.

Strategy (documented in PROVENANCE.md):
  1. Zenodo serves the record's file with `Accept-Ranges: bytes` and honors
     HTTP Range requests with 206 Partial Content (verified by hand with
     curl before writing this script).
  2. A ZIP file's central directory sits at the end of the archive. We fetch
     only the last 12 MB (one HTTP request) which is enough to contain the
     End-Of-Central-Directory record, the Zip64 EOCD locator/record, and the
     full central directory (33,815 entries for the whole 2014 archive).
     Python's `zipfile` module is pointed at a custom seekable file-like
     object (`RangeHTTPFile`, in this directory's `range_zip.py`) that
     serves reads from an in-memory cache of fetched byte ranges and issues
     a new HTTP Range GET only for bytes not yet cached.
  3. For each of the specific hourly files we need, we look up its
     (header_offset, compress_size) in the parsed central directory (no
     extra HTTP request needed — already in memory from step 2), then issue
     ONE HTTP Range request that covers the entire local-file-header +
     compressed-data span for that entry, so that zipfile's internal
     (chunked) decompression reads are all served from cache with zero
     further HTTP requests.
  4. zipfile validates each extracted file's CRC32 automatically
     (`BadZipFile` is raised on mismatch), which is our per-file integrity
     check against the archive's own directory (Zenodo only publishes an
     MD5 for the whole 26.7 GB zip, not per inner file).

Selected subset: 3 full ~24h days (24 hourly files per channel, both NS and
EW channels = 48 files/day) spread across three seasons within 2014, per
PREREGISTRATION.md Section 6 (N=3, spread across distinct seasons):
  - Winter: 2014-01-15
  - Spring: 2014-04-15
  - Summer: 2014-07-15
Plus the paired *_info.txt metadata file for every hourly binary file
(tiny, a few hundred bytes each) to read the REAL sample rate and other
acquisition parameters directly from the data's own metadata, per
PREREGISTRATION.md Section 4 (do not assume 256 Hz from secondary
literature).
"""
import hashlib
import json
import re
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from range_zip import RangeHTTPFile  # noqa: E402

RECORD_URL = "https://zenodo.org/api/records/6348691/files/2014.zip/content"
RECORD_LANDING_PAGE = "https://zenodo.org/records/6348691"
RECORD_DOI = "10.5281/zenodo.6348691"
ARCHIVE_MD5 = "916efee568bbbb385bb508541bdff547"  # from Zenodo API record metadata

OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

SEGMENTS = [
    # (label, season, month_dir, day)
    ("2014-01-15", "winter", "1401", 15),
    ("2014-04-15", "spring", "1404", 15),
    ("2014-07-15", "summer", "1407", 15),
]
CHANNELS = {0: "NS", 1: "EW"}


def fetch_with_retry(fn, *args, **kwargs):
    """Retry wrapper for 429 rate-limit responses (Zenodo: ~133 req/min)."""
    for attempt in range(8):
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # requests.HTTPError etc.
            resp = getattr(e, "response", None)
            if resp is not None and resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", "30"))
                print(f"  [rate limited] sleeping {wait}s (attempt {attempt+1})")
                time.sleep(wait + 1)
                continue
            raise
    raise RuntimeError("exceeded retry budget")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f = RangeHTTPFile(RECORD_URL, verbose=True)
    print(f"Remote archive size: {f.size} bytes ({f.size/1e9:.3f} GB)")

    tail = 12 * 1024 * 1024
    fetch_with_retry(f.prefetch, f.size - tail, f.size - 1)
    zf = zipfile.ZipFile(f)
    all_names = zf.namelist()
    print(f"Central directory parsed: {len(all_names)} entries "
          f"(using {f.request_count} HTTP request(s), "
          f"{f.bytes_fetched/1e6:.2f} MB fetched so far)")

    manifest = {
        "source": {
            "record_url": RECORD_LANDING_PAGE,
            "api_file_url": RECORD_URL,
            "doi": RECORD_DOI,
            "archive_md5_from_zenodo_api": ARCHIVE_MD5,
            "archive_size_bytes": f.size,
        },
        "segments": {},
    }

    for label, season, month_dir, day in SEGMENTS:
        seg_info = {"season": season, "channels": {}}
        for sensor, chan_name in CHANNELS.items():
            pat = re.compile(
                r"^2014/" + month_dir + r"/smplGRTU1_sensor_" + str(sensor)
                + r"_14" + month_dir[2:] + f"{day:02d}" + r"(\d{2})(\d{2})$"
            )
            matches = []
            for n in all_names:
                m = pat.match(n)
                if m:
                    matches.append((int(m.group(1)), n))
            matches.sort()
            print(f"\nSegment {label} ({season}) channel {chan_name}: "
                  f"{len(matches)} hourly files found")

            chan_dir = OUT_DIR / label / chan_name
            chan_dir.mkdir(parents=True, exist_ok=True)
            files_meta = []
            for hour_idx, name in matches:
                info_name = name + "_info.txt"
                zi_data = zf.getinfo(name)
                zi_info = zf.getinfo(info_name)

                for zi in (zi_data, zi_info):
                    start = zi.header_offset
                    end = (zi.header_offset + 30 + len(zi.filename.encode("utf-8"))
                           + 512 + zi.compress_size - 1)
                    fetch_with_retry(f.prefetch, start, end)

                data_bytes = fetch_with_retry(zf.read, name)  # CRC32-checked internally
                info_bytes = fetch_with_retry(zf.read, info_name)

                out_bin = chan_dir / Path(name).name
                out_info = chan_dir / Path(info_name).name
                out_bin.write_bytes(data_bytes)
                out_info.write_bytes(info_bytes)

                sha256 = hashlib.sha256(data_bytes).hexdigest()
                files_meta.append({
                    "hour_index": hour_idx,
                    "zip_entry": name,
                    "zip_entry_info": info_name,
                    "local_file": str(out_bin.relative_to(OUT_DIR.parent)),
                    "local_info_file": str(out_info.relative_to(OUT_DIR.parent)),
                    "file_size_bytes": zi_data.file_size,
                    "compress_size_bytes": zi_data.compress_size,
                    "crc32_zip_hex": f"{zi_data.CRC:08x}",
                    "sha256_extracted": sha256,
                    "info_txt": info_bytes.decode("utf-8", errors="replace"),
                })
                print(f"  hour {hour_idx:02d}: {name}  "
                      f"({zi_data.file_size} bytes, CRC32 OK) "
                      f"[reqs so far: {f.request_count}]")

            seg_info["channels"][chan_name] = files_meta
        manifest["segments"][label] = seg_info

    manifest["download_stats"] = {
        "http_requests": f.request_count,
        "bytes_fetched_over_http": f.bytes_fetched,
    }

    manifest_path = OUT_DIR.parent / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote manifest to {manifest_path}")
    print(f"Total HTTP requests: {f.request_count}, "
          f"total bytes fetched over network: {f.bytes_fetched/1e6:.2f} MB "
          f"(vs. {f.size/1e9:.2f} GB full archive)")


if __name__ == "__main__":
    main()
