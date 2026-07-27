from __future__ import annotations
import json
from .protocol import BASE, config_hash, config_payload, protocol_id

def validate_schema_shape(cfg: dict) -> None:
    schema = json.loads((BASE / "config" / "synthetic_validation_v1.schema.json").read_text(encoding="utf-8"))
    missing = sorted(set(schema["required"]) - set(cfg))
    unknown = sorted(set(cfg) - set(schema["properties"])) if schema.get("additionalProperties") is False else []
    if missing or unknown:
        raise RuntimeError(f"synthetic schema mismatch: missing={missing}, unknown={unknown}")
    if len(cfg["misspecification_scenarios"]) < schema["properties"]["misspecification_scenarios"]["minItems"]:
        raise RuntimeError("synthetic schema requires all adversarial misspecification scenarios")

def main() -> None:
    cfg = config_payload()
    validate_schema_shape(cfg)
    print(json.dumps({"valid": True, "synthetic_protocol_id": protocol_id(), "synthetic_config_hash": config_hash(), "tamesis_protocol_id": cfg["tamesis_protocol_id"], "tamesis_contract_hash": cfg["tamesis_contract_hash"]}, indent=2))

if __name__ == "__main__": main()
