from __future__ import annotations

from .protocol import BASE, config_payload
from .provenance import write_sidecar


def main() -> None:
    paths = list((BASE / "synthetic_validation").glob("*.py"))
    paths += [
        BASE / "test_synthetic_validation.py",
        BASE / "config" / "synthetic_validation_v1.yaml",
        BASE / "config" / "synthetic_validation_v1.schema.json",
        BASE / "reports" / "SYNTHETIC_PHASE_BASELINE.md",
    ]
    for path in paths:
        write_sidecar(path, inputs=[], scenario="synthetic_validation_source", seed=int(config_payload()["master_seed"]), kind="synthetic_validation_source")
    print(f"registered {len(paths)} synthetic source/protocol artifacts")


if __name__ == "__main__":
    main()
