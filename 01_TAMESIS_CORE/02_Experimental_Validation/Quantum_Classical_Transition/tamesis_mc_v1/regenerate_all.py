from __future__ import annotations

import subprocess
import sys

from config import reject_runtime_overrides


COMMANDS = [
    ["python", "validate_environment.py"],
    ["python", "validate_contract.py"],
    ["python", "resolve_contract.py"],
    ["python", "run_predictions.py"],
    ["python", "compare_models.py"],
    ["python", "prioritize_targets.py"],
    ["python", "analyze_target_1e15.py"],
    ["python", "target_1e15_noise_budget.py"],
    ["python", "target_1e15_sensitivity.py"],
    ["python", "target_1e15_decision.py"],
    ["python", "target_1e15_thermal_gate.py"],
    ["python", "generate_figures.py"],
    ["python", "build_manifest.py"],
    ["python", "verify_artifacts.py"],
    ["python", "-m", "pytest", "-q"],
]


def main() -> None:
    reject_runtime_overrides()
    for cmd in COMMANDS:
        print(f"$ {' '.join(cmd)}")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
