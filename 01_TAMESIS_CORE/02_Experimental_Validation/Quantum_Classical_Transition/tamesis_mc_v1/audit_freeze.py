"""Executable evidence for the independent Tamesis M_c v1.0 freeze audit."""

from __future__ import annotations

import copy
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable

import yaml

from build_manifest import build, sha256_file
from config import CONFIG_PATH, ContractError, load_v1_contract, reject_runtime_overrides
from provenance import provenance_record, require_current_artifact, write_sidecar
from verify_artifacts import ArtifactVerificationError, verify_manifest
from workspace_paths import data_path


BASE = Path(__file__).resolve().parent


def run_command(command: list[str], *, env: dict[str, str] | None = None, cwd: Path = BASE) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    return {
        "command": subprocess.list2cmdline(command),
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def contract_mutations() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("Mc_plus_1_percent", lambda d: d["derived_quantities"]["Mc_kg"].__setitem__("value", d["derived_quantities"]["Mc_kg"]["value"] * 1.01)),
        ("Mc_next_serializable_float", lambda d: d["derived_quantities"]["Mc_kg"].__setitem__("value", math.nextafter(float(d["derived_quantities"]["Mc_kg"]["value"]), math.inf))),
        ("phase_space_root_7", lambda d: d["structural_parameters"]["phase_space_root"].__setitem__("value", 7)),
        ("phase_space_root_9", lambda d: d["structural_parameters"]["phase_space_root"].__setitem__("value", 9)),
        ("tau_c_changed", lambda d: d["structural_parameters"]["tau_c"].__setitem__("value", 2.2)),
        ("alpha_defined", lambda d: d["structural_parameters"]["alpha"].__setitem__("value", 1.0)),
        ("transition_width_defined", lambda d: d["structural_parameters"]["transition_width"].__setitem__("value", 0.1)),
        ("Mc_unit_changed", lambda d: d["derived_quantities"]["Mc_kg"].__setitem__("unit", "g")),
        ("H0_incompatible_unit", lambda d: d["constants"]["H0"].__setitem__("unit", "kg")),
        ("unknown_structural_field", lambda d: d["structural_parameters"].__setitem__("hidden_default", {"value": 1, "classification": "modelling_assumption"})),
        ("missing_structural_field", lambda d: d["structural_parameters"].pop("exponent")),
        ("input_without_unit", lambda d: d["structural_parameters"]["tau_c"].pop("unit")),
        ("incompatible_version", lambda d: d.__setitem__("version", "2.0")),
        ("structural_edit_same_version", lambda d: d["constants"]["H0"].__setitem__("value", 71.0)),
    ]


def run_contract_mutations() -> list[dict[str, Any]]:
    source = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    results = []
    with tempfile.TemporaryDirectory(prefix="tamesis-mutations-") as temp_name:
        temp = Path(temp_name)
        for index, (name, mutate) in enumerate(contract_mutations(), start=1):
            candidate = copy.deepcopy(source)
            mutate(candidate)
            path = temp / f"{index:02d}_{name}.yaml"
            path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
            try:
                load_v1_contract(path)
            except Exception as exc:
                results.append({"mutation": name, "command": f"load_v1_contract({path.name})", "exit_code": 1, "rejected": True, "error_type": type(exc).__name__, "message": str(exc)})
            else:
                results.append({"mutation": name, "command": f"load_v1_contract({path.name})", "exit_code": 0, "rejected": False, "error_type": None, "message": "accepted unexpectedly"})
    return results


def runtime_override_evidence() -> list[dict[str, Any]]:
    cli = run_command([sys.executable, "validate_contract.py", "--Mc", "1e-15"])
    cli["mutation"] = "CLI structural override"
    env = os.environ.copy()
    env["TAMESIS_MC_KG"] = "1e-15"
    env_result = run_command([sys.executable, "validate_contract.py"], env=env)
    env_result["mutation"] = "environment structural override"
    return [cli, env_result]


def sidecar_and_manifest_evidence(contract) -> dict[str, Any]:
    results: dict[str, Any] = {"states": {}, "rejections": {}}
    with tempfile.TemporaryDirectory(prefix="tamesis-manifest-") as temp_name:
        temp = Path(temp_name)
        (temp / "90_LEGACY").mkdir()
        artifacts = {
            "current.txt": b"current",
            "stale.txt": b"stale",
            "90_LEGACY/legacy.txt": b"legacy",
            "figure.png": b"not-a-real-png-but-illustrative",
            "unknown.txt": b"unknown",
            "invalid.txt": b"invalid",
        }
        for rel, content in artifacts.items():
            path = temp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        current = temp / "current.txt"
        write_sidecar(current, provenance_record(output_path=current, contract=contract, script="audit_freeze.py"))
        stale = temp / "stale.txt"
        stale_record = provenance_record(output_path=stale, contract=contract, script="audit_freeze.py")
        stale_record["protocol_id"] = "tamesis-mc-v0.9:previous"
        write_sidecar(stale, stale_record)
        invalid = temp / "invalid.txt"
        invalid_record = provenance_record(output_path=invalid, contract=contract, script="audit_freeze.py")
        write_sidecar(invalid, invalid_record)
        invalid_sidecar = invalid.with_suffix(".txt.provenance.json")
        invalid_data = json.loads(invalid_sidecar.read_text(encoding="utf-8"))
        invalid_data["artifact_sha256"] = "0" * 64
        invalid_sidecar.write_text(json.dumps(invalid_data), encoding="utf-8")
        manifest_path = temp / "data" / "artifact_manifest.json"
        manifest = build(base=temp, output_path=manifest_path, contract=contract)
        results["states"] = manifest["summary"]

        def rejection(name: str, mutate: Callable[[], None], restore: Callable[[], None]) -> None:
            mutate()
            try:
                verify_manifest(manifest_path, base=temp, contract=contract)
            except Exception as exc:
                results["rejections"][name] = {"rejected": True, "exit_code": 1, "message": str(exc)}
            else:
                results["rejections"][name] = {"rejected": False, "exit_code": 0, "message": "accepted unexpectedly"}
            finally:
                restore()

        original_current = current.read_bytes()
        rejection("artifact_removed", lambda: current.unlink(), lambda: current.write_bytes(original_current))
        rejection("artifact_edited", lambda: current.write_bytes(b"edited"), lambda: current.write_bytes(original_current))
        current_sidecar = current.with_suffix(".txt.provenance.json")
        original_sidecar = current_sidecar.read_bytes()
        rejection("sidecar_removed", lambda: current_sidecar.unlink(), lambda: current_sidecar.write_bytes(original_sidecar))
        rejection("sidecar_tampered", lambda: current_sidecar.write_bytes(b"{}"), lambda: current_sidecar.write_bytes(original_sidecar))
        original_manifest = manifest_path.read_bytes()
        def alter_manifest() -> None:
            data = json.loads(original_manifest)
            data["entries"][0]["hash"] = "f" * 64
            manifest_path.write_text(json.dumps(data), encoding="utf-8")
        rejection("manifest_edited", alter_manifest, lambda: manifest_path.write_bytes(original_manifest))
        manual = temp / "manual_output.json"
        rejection("manual_unlisted_output", lambda: manual.write_text("{}", encoding="utf-8"), lambda: manual.unlink(missing_ok=True))
        old = temp / "official_previous_version.json"
        def add_old() -> None:
            old.write_text("{}", encoding="utf-8")
            record = provenance_record(output_path=old, contract=contract, script="audit_freeze.py")
            record["protocol_id"] = "tamesis-mc-v0.9:previous"
            write_sidecar(old, record)
        rejection("previous_version_unlisted_output", add_old, lambda: (old.unlink(missing_ok=True), old.with_suffix(".json.provenance.json").unlink(missing_ok=True)))

        try:
            require_current_artifact(current, contract)
            results["current_chain_validation"] = "passed"
        except Exception as exc:
            results["current_chain_validation"] = f"failed: {exc}"
        bad_record = json.loads(current_sidecar.read_text(encoding="utf-8"))
        bad_record["config_hash"] = "0" * 64
        current_sidecar.write_text(json.dumps(bad_record), encoding="utf-8")
        try:
            require_current_artifact(current, contract)
            results["wrong_sidecar_contract_hash"] = {"rejected": False}
        except Exception as exc:
            results["wrong_sidecar_contract_hash"] = {"rejected": True, "message": str(exc)}
    return results


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    before = sha256_file(CONFIG_PATH)
    evidence = {
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "official_yaml_sha256_before": before,
        "contract_mutations": run_contract_mutations(),
        "runtime_overrides": runtime_override_evidence(),
        "manifest_and_sidecars": sidecar_and_manifest_evidence(contract),
        "official_yaml_sha256_after": sha256_file(CONFIG_PATH),
    }
    evidence["official_contract_unchanged"] = evidence["official_yaml_sha256_before"] == evidence["official_yaml_sha256_after"]
    output = data_path("freeze_audit_evidence.json")
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    write_sidecar(output, provenance_record(output_path=output, contract=contract, script="audit_freeze.py"))
    rejected = sum(item.get("rejected", item.get("exit_code") != 0) for item in evidence["contract_mutations"] + evidence["runtime_overrides"])
    print(json.dumps({"output": str(output), "mutation_rejections": rejected, "official_contract_unchanged": evidence["official_contract_unchanged"]}, indent=2))


if __name__ == "__main__":
    main()
