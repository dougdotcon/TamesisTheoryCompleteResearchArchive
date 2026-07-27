from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .contract_bridge import tamesis_integration
from .loader import load_regimes, load_transitions
from .models import Evidence, Protocol, Regime, Transition
from .provenance import REGISTRY, ROOT, file_hash, write_sidecar


def main() -> None:
    (ROOT / "schemas").mkdir(exist_ok=True)
    (ROOT / "outputs").mkdir(exist_ok=True)
    schemas = {"regime.schema.json": Regime.model_json_schema(), "transition.schema.json": Transition.model_json_schema(), "evidence.schema.json": Evidence.model_json_schema(), "protocol.schema.json": Protocol.model_json_schema()}
    for name, schema in schemas.items():
        (ROOT / "schemas" / name).write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    integration = tamesis_integration()
    output = REGISTRY / "protocols" / "tamesis_mc_v1_resolved.json"
    output.write_text(json.dumps({"protocol": "tamesis_mc_v1", "integration": integration}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "atlas_version": "0.1",
        "tamesis_protocol_id": integration["protocol_id"],
        "tamesis_config_hash": integration["config_hash"],
        "regimes": sorted(load_regimes()),
        "transitions": sorted(load_transitions()),
        "schema_hashes": {name: hashlib.sha256(json.dumps(schema, sort_keys=True).encode()).hexdigest() for name, schema in schemas.items()},
    }
    manifest_path = ROOT / "outputs" / "atlas_registry_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_sidecar(output, [ROOT / "config" / "atlas_v0_1.yaml"], kind="resolved_contract_registry")
    write_sidecar(manifest_path, [output] + [ROOT / "schemas" / name for name in schemas], kind="atlas_manifest")
    print(json.dumps({"regimes": len(manifest["regimes"]), "transitions": len(manifest["transitions"]), "schemas": len(schemas)}, indent=2))


if __name__ == "__main__":
    main()
