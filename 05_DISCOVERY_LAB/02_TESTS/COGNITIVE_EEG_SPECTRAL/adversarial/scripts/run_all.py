import sys, os, json, re, hashlib, time
sys.path.insert(0, os.path.dirname(__file__))
from pipeline import download_with_retry, process_edf, md5sum

META_PATH = os.path.join(os.path.dirname(__file__), "figshare_meta_adversarial.json")
RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "edf_raw")
OUT_PATH = os.path.join(os.path.dirname(__file__), "adversarial_per_subject.json")
LOG_PATH = os.path.join(os.path.dirname(__file__), "adversarial_run_log.txt")

os.makedirs(RAW_DIR, exist_ok=True)

with open(META_PATH) as f:
    meta = json.load(f)

files = meta["files"]
ec_files = [fl for fl in files if fl["name"].endswith(" EC.edf")]
assert len(ec_files) == 64, f"expected 64 EC files, got {len(ec_files)}"

def parse_subject(name):
    # "MDD S1 EC.edf" / "MDD S11  EC.edf" (double space variants) / "H S1 EC.edf"
    m = re.match(r"^(MDD|H)\s+S(\d+)\s+EC\.edf$", name)
    assert m, f"unparseable filename: {name!r}"
    group = "MDD" if m.group(1) == "MDD" else "HC"
    num = int(m.group(2))
    return group, num

results = []
log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

t0 = time.time()
for i, fl in enumerate(sorted(ec_files, key=lambda x: x["name"]), 1):
    name = fl["name"]
    group, num = parse_subject(name)
    subject_label = f"{group}_S{num}"
    url = fl["download_url"]
    expected_md5 = fl["supplied_md5"]
    size = fl["size"]
    dest = os.path.join(RAW_DIR, f"{subject_label}.edf")

    log(f"[{i}/64] {name} -> {subject_label} size={size} url={url}")

    ok, got_md5, attempts, err = download_with_retry(url, dest, expected_md5, max_retries=3)
    entry = {
        "file_name": name,
        "subject_label": subject_label,
        "group": group,
        "subject_num": num,
        "download_url": url,
        "expected_md5_api": expected_md5,
        "size_api": size,
    }
    if not ok:
        log(f"    DOWNLOAD FAILED after {attempts} attempts: {err}")
        entry["download_ok"] = False
        entry["download_error"] = err
        entry["attempts"] = attempts
        results.append(entry)
        continue

    entry["download_ok"] = True
    entry["downloaded_md5_self"] = got_md5
    entry["md5_matches_api"] = (got_md5 == expected_md5)
    entry["attempts"] = attempts
    log(f"    downloaded OK, md5={got_md5} (attempts={attempts})")

    try:
        proc = process_edf(dest, subject_label)
        entry.update(proc)
        log(f"    n_windows_raw={proc['n_windows_raw']} rejected={proc['n_windows_rejected']} "
            f"frac={proc['reject_frac']:.3f} excluded={proc['excluded_by_artifact_rule']} "
            f"Ibar={proc.get('Ibar')}")
    except Exception as e:
        log(f"    PROCESSING ERROR: {e}")
        entry["processing_error"] = str(e)

    results.append(entry)

    # do not retain raw EDF after computing
    try:
        os.remove(dest)
    except OSError:
        pass

elapsed = time.time() - t0
log(f"\nTotal elapsed: {elapsed:.1f}s for {len(results)} files")

with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

with open(LOG_PATH, "w") as f:
    f.write("\n".join(log_lines) + "\n")

print("\nWROTE", OUT_PATH)
print("WROTE", LOG_PATH)
