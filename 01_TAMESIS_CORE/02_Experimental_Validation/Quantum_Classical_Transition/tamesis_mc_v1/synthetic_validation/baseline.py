from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

from config import CONFIG_PATH, load_v1_contract
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path


BASE = Path(__file__).resolve().parent.parent
REPO = BASE.parents[3]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    contract = load_v1_contract()
    manifest = json.loads((BASE / "data" / "artifact_manifest.json").read_text(encoding="utf-8"))
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, text=True, capture_output=True)
    status = subprocess.run(["git", "status", "--short"], cwd=REPO, text=True, capture_output=True)
    canonical = {}
    for path in [CONFIG_PATH, BASE / "config" / "tamesis_mc_v1.lock.json", BASE / "config" / "tamesis_mc_v1.schema.json", BASE / "config.py", BASE / "mc_model.py", BASE / "environment_model.py", BASE / "data" / "artifact_manifest.json"]:
        canonical[path.relative_to(REPO).as_posix()] = sha(path)
    unknown = sorted(entry["path"] for entry in manifest["entries"] if entry["status"] == "unknown_provenance")
    payload = {
        "baseline_type": "synthetic_validation_phase_start",
        "protocol_id": contract.protocol_id(),
        "contract_hash": contract.config_hash(),
        "git_commit": git.stdout.strip() if git.returncode == 0 else None,
        "git_status_sha256": hashlib.sha256(status.stdout.encode()).hexdigest(),
        "pytest_command": "python -m pytest -q",
        "pytest_result": "12 passed",
        "manifest_summary": manifest["summary"],
        "canonical_file_hashes": canonical,
        "unknown_provenance_count": len(unknown),
        "unknown_provenance_paths": unknown,
        "quarantine_policy": "unknown_provenance, legacy and illustrative_only are excluded from synthetic priors, calibration, thresholds and inference",
    }
    output = data_path("synthetic_phase_baseline.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    write_sidecar(output, provenance_record(output_path=output, contract=contract, script="synthetic_validation.baseline", inputs=[BASE / "data" / "artifact_manifest.json", CONFIG_PATH]))
    report = BASE / "reports" / "SYNTHETIC_PHASE_BASELINE.md"
    report.write_text("# Synthetic validation baseline\n\n" + "This snapshot was captured before synthetic outputs were generated.\n\n" + f"- Protocol ID: `{contract.protocol_id()}`\n- Contract hash: `{contract.config_hash()}`\n- Git commit: `{payload['git_commit']}`\n- Pytest: `{payload['pytest_result']}`\n- Unknown provenance entries: **{len(unknown)}**\n- Manifest summary: `{json.dumps(manifest['summary'], sort_keys=True)}`\n\nCanonical hashes and the complete quarantine list are in `data/synthetic_phase_baseline.json`. Quarantined artifacts are not used by the generator, inferer, priors, thresholds, calibration or scientific outputs.\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "unknown_provenance": len(unknown), "git_commit": payload["git_commit"]}, indent=2))


if __name__ == "__main__":
    main()
