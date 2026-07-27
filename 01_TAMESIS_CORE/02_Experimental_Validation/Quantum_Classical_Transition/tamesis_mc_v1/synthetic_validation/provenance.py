from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from config import load_v1_contract
from .protocol import CONFIG_PATH, config_hash, protocol_id


BASE = Path(__file__).resolve().parent.parent


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_sidecar(output: Path, *, inputs: list[Path], scenario: str | None = None, seed: int | None = None, kind: str = "synthetic_validation_artifact") -> None:
    contract = load_v1_contract()
    record: dict[str, Any] = {
        "artifact": output.relative_to(BASE).as_posix(),
        "artifact_sha256": file_hash(output),
        "artifact_classification": "synthetic_validation_artifact",
        "tamesis_protocol_id": contract.protocol_id(),
        "tamesis_contract_hash": contract.config_hash(),
        "synthetic_protocol_id": protocol_id(),
        "synthetic_config_hash": config_hash(),
        "kind": kind,
        "scenario": scenario,
        "seed": seed,
        "input_hashes": {p.relative_to(BASE).as_posix(): file_hash(p) for p in inputs if p.exists()},
    }
    output.with_suffix(output.suffix + ".provenance.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
