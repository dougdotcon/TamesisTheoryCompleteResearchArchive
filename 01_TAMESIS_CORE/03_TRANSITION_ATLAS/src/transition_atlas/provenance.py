from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .contract_bridge import load_tamesis_contract


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "registry"
OUTPUTS = ROOT / "outputs"


def stable_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(output: Path, inputs: list[Path], *, kind: str) -> dict[str, Any]:
    contract = load_tamesis_contract()
    return {
        "artifact": output.relative_to(ROOT).as_posix(),
        "artifact_sha256": file_hash(output),
        "atlas_version": "0.1",
        "kind": kind,
        "tamesis_protocol_id": contract["protocol_id"],
        "tamesis_config_hash": contract["config_hash"],
        "input_hashes": {p.relative_to(ROOT).as_posix(): file_hash(p) for p in inputs if p.exists()},
    }


def write_sidecar(output: Path, inputs: list[Path], *, kind: str) -> None:
    sidecar = output.with_suffix(output.suffix + ".provenance.json")
    sidecar.write_text(json.dumps(record(output, inputs, kind=kind), indent=2, sort_keys=True) + "\n", encoding="utf-8")
