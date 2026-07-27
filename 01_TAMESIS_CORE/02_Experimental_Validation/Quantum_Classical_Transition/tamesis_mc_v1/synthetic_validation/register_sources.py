from __future__ import annotations

from .protocol import BASE, config_payload
from .provenance import write_sidecar


def main() -> None:
    paths = list((BASE / "synthetic_validation").glob("*.py"))
    paths += [BASE / "test_robust_v1_2.py"]
    paths += [
        BASE / "test_synthetic_validation.py",
        BASE / "config" / "synthetic_validation_v1.yaml",
        BASE / "config" / "synthetic_validation_v1.schema.json",
        BASE / "config" / "synthetic_validation_v1_1.yaml",
        BASE / "config" / "synthetic_validation_v1_1.schema.json",
        BASE / "config" / "synthetic_validation_v1_2.yaml",
        BASE / "config" / "synthetic_validation_v1_2.schema.json",
        BASE / "config" / "instrument_specification_v0_1.yaml",
        BASE / "config" / "instrument_specification_v0_1.schema.json",
        BASE / "instrument_spec.py",
        BASE / "verify_instrument_spec.py",
        BASE / "run_instrument_spec.py",
        BASE / "config" / "sensor_transfer_models_v0_2.yaml",
        BASE / "config" / "sensor_transfer_models_v0_2.schema.json",
        BASE / "sensor_models.py",
        BASE / "verify_sensor_models.py",
        BASE / "run_sensor_models.py",
        BASE / "config" / "platform_feasibility_v0_3.yaml",
        BASE / "config" / "platform_feasibility_v0_3.schema.json",
        BASE / "platform_feasibility.py",
        BASE / "verify_platform_feasibility.py",
        BASE / "run_platform_feasibility.py",
        BASE / "config" / "demonstrator_a_v0_4.yaml",
        BASE / "config" / "demonstrator_a_v0_4.schema.json",
        BASE / "demonstrator_a.py",
        BASE / "verify_demonstrator_a.py",
        BASE / "run_demonstrator_a.py",
        BASE / "config" / "demonstrator_a_v0_5.yaml",
        BASE / "config" / "demonstrator_a_v0_5.schema.json",
        BASE / "run_demonstrator_a_hardware.py",
        BASE / "test_demonstrator_a_hardware.py",
        BASE / "config" / "demonstrator_a_v0_6.yaml",
        BASE / "config" / "demonstrator_a_v0_6.schema.json",
        BASE / "demonstrator_a_physical.py",
        BASE / "run_demonstrator_a_physical.py",
        BASE / "verify_demonstrator_a_physical.py",
        BASE / "synthetic_validation" / "joint_v1_1.py",
        BASE / "synthetic_validation" / "robust_v1_2.py",
        BASE / "reports" / "SYNTHETIC_PHASE_BASELINE.md",
    ]
    paths += list((BASE / "demonstrator_a_hardware").glob("*.py"))
    for path in paths:
        write_sidecar(path, inputs=[], scenario="synthetic_validation_source", seed=int(config_payload()["master_seed"]), kind="synthetic_validation_source")
    print(f"registered {len(paths)} synthetic source/protocol artifacts")


if __name__ == "__main__":
    main()
