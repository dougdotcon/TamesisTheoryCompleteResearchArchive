from __future__ import annotations

import json

from config import load_v1_contract, reject_runtime_overrides, resolved_contract_payload
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    output = data_path("resolved_contract_v1_0.json")
    payload = resolved_contract_payload(contract)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_sidecar(
        output,
        provenance_record(
            output_path=output,
            contract=contract,
            script="resolve_contract.py",
            inputs=[],
            arguments={},
        ),
    )
    print(json.dumps({"output": str(output), "protocol_id": contract.protocol_id(), "config_hash": contract.config_hash()}, indent=2))


if __name__ == "__main__":
    main()
