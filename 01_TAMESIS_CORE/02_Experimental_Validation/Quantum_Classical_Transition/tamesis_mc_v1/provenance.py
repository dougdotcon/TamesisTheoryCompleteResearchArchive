from __future__ import annotations

import hashlib
import importlib.metadata as metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import V1Contract


BASE = Path(__file__).resolve().parent


def stable_hash(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def package_versions(packages: list[str]) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for name in packages:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def provenance_record(
    *,
    output_path: Path,
    contract: V1Contract,
    script: str,
    inputs: list[str] | None = None,
    arguments: dict[str, Any] | None = None,
    seed: int | None = None,
    status: str = "derived_result",
    epistemic_status: str = "derived_result",
) -> dict[str, Any]:
    inputs = inputs or []
    arguments = arguments or {}
    input_hashes = {}
    for item in inputs:
        path = Path(item).resolve()
        if path.exists() and path.is_file():
            try:
                key = path.relative_to(BASE).as_posix()
            except ValueError:
                key = path.name
            input_hashes[key] = file_hash(path)
    try:
        artifact = output_path.resolve().relative_to(BASE).as_posix()
    except ValueError:
        artifact = output_path.name
    return {
        "artifact": artifact,
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "config_path": "config/tamesis_mc_v1.yaml",
        "input_hashes": input_hashes,
        "script": script,
        "arguments": arguments,
        "commit": git_commit(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "dependencies": package_versions(["numpy", "pandas", "matplotlib", "seaborn", "pydantic", "PyYAML", "imageio"]),
        "seed": seed,
        "status": status,
        "epistemic_status": epistemic_status,
    }


def write_sidecar(path: Path, provenance: dict[str, Any]) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"cannot write provenance for missing artifact: {path}")
    provenance = dict(provenance)
    provenance["artifact_sha256"] = file_hash(path)
    sidecar = path.with_suffix(path.suffix + ".provenance.json")
    sidecar.write_text(json.dumps(provenance, indent=2, sort_keys=True), encoding="utf-8")
    return sidecar


def require_current_artifact(path: Path, contract: V1Contract) -> dict[str, Any]:
    """Reject a derived input unless its sidecar and complete hash chain are current."""
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"missing required input artifact: {path}")
    sidecar = path.with_suffix(path.suffix + ".provenance.json")
    if not sidecar.exists():
        raise RuntimeError(f"missing provenance sidecar for required input: {path}")
    try:
        record = json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"malformed provenance sidecar for {path}: {exc}") from exc
    if record.get("protocol_id") != contract.protocol_id():
        raise RuntimeError(f"stale protocol ID for required input: {path}")
    if record.get("config_hash") != contract.config_hash():
        raise RuntimeError(f"stale config hash for required input: {path}")
    if record.get("artifact_sha256") != file_hash(path):
        raise RuntimeError(f"artifact hash mismatch for required input: {path}")
    for rel, expected in record.get("input_hashes", {}).items():
        upstream = BASE / Path(rel)
        if not upstream.exists() or file_hash(upstream) != expected:
            raise RuntimeError(f"upstream input hash mismatch for {path}: {rel}")
    return record
