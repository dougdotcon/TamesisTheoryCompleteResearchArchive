"""Run two isolated v1.0 regenerations and compare scientific-content hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageSequence

from config import load_v1_contract, reject_runtime_overrides
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path


BASE = Path(__file__).resolve().parent


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visual_content_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with Image.open(path) as image:
        for frame in ImageSequence.Iterator(image):
            rgba = frame.convert("RGBA")
            digest.update(str(rgba.size).encode("ascii"))
            digest.update(rgba.tobytes())
    return digest.hexdigest()


def copy_clean_source(destination: Path) -> None:
    destination.mkdir(parents=True)
    for path in BASE.glob("*.py"):
        shutil.copy2(path, destination / path.name)
    shutil.copy2(BASE / "requirements-lock.txt", destination / "requirements-lock.txt")
    shutil.copytree(BASE / "config", destination / "config")
    (destination / "data").mkdir()
    for name in ("literature_points.csv", "literature_points_v2.csv"):
        shutil.copy2(BASE / "data" / name, destination / "data" / name)


def collect(root: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    paths = list((root / "data").glob("*.json")) + list((root / "data").glob("*.csv")) + list((root / "reports" / "figures").glob("*.png")) + list((root / "reports" / "figures").glob("*.gif"))
    for path in sorted(paths):
        rel = path.relative_to(root).as_posix()
        if rel == "data/artifact_manifest.json" or path.name.endswith(".provenance.json"):
            continue
        entry = {"sha256": hash_file(path)}
        if path.suffix.lower() in {".png", ".gif"}:
            entry["normalized_visual_sha256"] = visual_content_hash(path)
        result[rel] = entry
    return result


def run_once(parent: Path, label: str) -> tuple[dict, dict]:
    module = parent / label / "01_TAMESIS_CORE" / "02_Experimental_Validation" / "Quantum_Classical_Transition" / "tamesis_mc_v1"
    copy_clean_source(module)
    completed = subprocess.run([sys.executable, "regenerate_all.py"], cwd=module, text=True, capture_output=True)
    run = {
        "command": f"{sys.executable} regenerate_all.py",
        "cwd_layout": f"{label}/01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1",
        "exit_code": completed.returncode,
        "stdout_tail": "\n".join(completed.stdout.splitlines()[-30:]),
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-30:]),
    }
    if completed.returncode != 0:
        raise RuntimeError(f"clean reproduction {label} failed: {run}")
    return run, collect(module)


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    with tempfile.TemporaryDirectory(prefix="tamesis-clean-repro-") as temp_name:
        parent = Path(temp_name)
        run1, hashes1 = run_once(parent, "run1")
        run2, hashes2 = run_once(parent, "run2")
    official = collect(BASE)
    rows = []
    all_paths = sorted(set(official) | set(hashes1) | set(hashes2))
    for rel in all_paths:
        old = official.get(rel, {})
        first = hashes1.get(rel, {})
        second = hashes2.get(rel, {})
        if first.get("sha256") == second.get("sha256"):
            status = "none"
        elif first.get("normalized_visual_sha256") and first.get("normalized_visual_sha256") == second.get("normalized_visual_sha256"):
            status = "metadata_only"
        else:
            status = "unexpected"
        rows.append({"artifact": rel, "hash_previous": old.get("sha256"), "hash_run_1": first.get("sha256"), "hash_run_2": second.get("sha256"), "normalized_run_1": first.get("normalized_visual_sha256"), "normalized_run_2": second.get("normalized_visual_sha256"), "status": status})
    evidence = {
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "run_1": run1,
        "run_2": run2,
        "artifacts": rows,
        "summary": {
            "compared": len(rows),
            "byte_identical_between_clean_runs": sum(row["hash_run_1"] == row["hash_run_2"] and row["hash_run_1"] is not None for row in rows),
            "metadata_only": sum(row["status"] == "metadata_only" for row in rows),
            "unexpected": sum(row["status"] == "unexpected" for row in rows),
        },
    }
    output = data_path("clean_reproducibility_evidence.json")
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_sidecar(output, provenance_record(output_path=output, contract=contract, script="clean_reproduce.py"))
    print(json.dumps(evidence["summary"], indent=2))


if __name__ == "__main__":
    main()
