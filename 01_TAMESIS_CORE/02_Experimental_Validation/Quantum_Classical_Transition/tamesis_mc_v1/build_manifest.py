from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import V1Contract, load_v1_contract, reject_runtime_overrides


BASE = Path(__file__).resolve().parent
MANIFEST_REL = Path("data/artifact_manifest.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sidecar_for(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".provenance.json")


def iter_artifacts(base: Path):
    for path in sorted(base.rglob("*")):
        if path.is_dir() or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(base)
        if rel == MANIFEST_REL or path.name.endswith(".provenance.json"):
            continue
        yield path


def base_classification(path: Path, base: Path) -> tuple[str, bool]:
    rel = path.relative_to(base).as_posix()
    if rel.startswith("90_LEGACY/") or rel.startswith("00_HOME/legacy/"):
        return "legacy", False
    if rel.startswith("reports/figures/") or path.suffix.lower() in {".png", ".gif"}:
        return "illustrative_only", False
    if path.suffix == ".py":
        return ("illustrative_only", False) if path.name == "generate_figures.py" else ("model_assumption", True)
    if path.suffix in {".json", ".csv"}:
        return "derived_result", True
    return "unknown_provenance", False


def inspect_sidecar(path: Path, base: Path, contract: V1Contract) -> tuple[str, dict[str, Any] | None, list[str]]:
    sidecar = sidecar_for(path)
    if not sidecar.exists():
        return "missing", None, ["missing sidecar"]
    try:
        prov = json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception as exc:
        return "invalid", None, [f"malformed sidecar: {exc}"]
    errors: list[str] = []
    if prov.get("artifact_sha256") != sha256_file(path):
        errors.append("artifact hash mismatch")
    for rel, expected in prov.get("input_hashes", {}).items():
        input_path = base / Path(rel)
        if not input_path.exists():
            errors.append(f"missing input: {rel}")
        elif sha256_file(input_path) != expected:
            errors.append(f"input hash mismatch: {rel}")
    if errors:
        return "invalid", prov, errors
    if prov.get("protocol_id") != contract.protocol_id() or prov.get("config_hash") != contract.config_hash():
        return "stale", prov, ["contract identity mismatch"]
    return "current", prov, []


def classify(path: Path, base: Path, contract: V1Contract) -> tuple[str, bool, dict[str, Any] | None, list[str]]:
    basic, participates = base_classification(path, base)
    state, prov, errors = inspect_sidecar(path, base, contract)
    if state == "invalid":
        return "invalid", participates, prov, errors
    if state == "stale":
        return "canonical_stale", participates, prov, errors
    if state == "current":
        return "canonical_current", participates, prov, []
    if basic in {"legacy", "illustrative_only"}:
        return basic, participates, None, errors
    return "unknown_provenance", participates, None, errors


def build(base: Path = BASE, output_path: Path | None = None, contract: V1Contract | None = None) -> dict[str, Any]:
    base = base.resolve()
    contract = contract or load_v1_contract()
    entries = []
    summary = {key: 0 for key in ("canonical_current", "canonical_stale", "legacy", "illustrative_only", "unknown_provenance", "invalid")}
    for path in iter_artifacts(base):
        status, participates, prov, errors = classify(path, base, contract)
        summary[status] += 1
        sidecar = sidecar_for(path)
        entries.append({
            "path": path.relative_to(base).as_posix(),
            "type": path.suffix.lstrip(".") or "file",
            "script_generator": prov.get("script") if prov else None,
            "inputs": prov.get("input_hashes", {}) if prov else {},
            "parameters": prov.get("arguments", {}) if prov else {},
            "timestamp": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
            "hash": sha256_file(path),
            "sidecar_hash": sha256_file(sidecar) if sidecar.exists() else None,
            "status": status,
            "validation_errors": errors,
            "participates_in_inference": participates,
        })
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "summary": summary,
        "entries": entries,
    }
    out = output_path or (base / MANIFEST_REL)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return manifest


if __name__ == "__main__":
    reject_runtime_overrides()
    build()
