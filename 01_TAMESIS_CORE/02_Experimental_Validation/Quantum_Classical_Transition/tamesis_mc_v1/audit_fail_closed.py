from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import yaml

from config import CONFIG_PATH, load_v1_contract, reject_runtime_overrides
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path


BASE = Path(__file__).resolve().parent


def command(command: list[str], cwd: Path, env=None) -> dict:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    return {"command": subprocess.list2cmdline(command), "exit_code": result.returncode, "stdout": result.stdout[-800:], "stderr": result.stderr[-800:]}


def module_copy(root: Path, *, include_config: bool = True) -> Path:
    module = root / "01_TAMESIS_CORE" / "02_Experimental_Validation" / "Quantum_Classical_Transition" / "tamesis_mc_v1"
    module.mkdir(parents=True)
    for name in ("config.py", "mc_model.py", "validate_contract.py", "provenance.py", "workspace_paths.py", "verify_artifacts.py", "build_manifest.py"):
        shutil.copy2(BASE / name, module / name)
    if include_config:
        shutil.copytree(BASE / "config", module / "config")
    (module / "data").mkdir()
    return module


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    results = []
    with tempfile.TemporaryDirectory(prefix="tamesis-fail-closed-") as temp_name:
        root = Path(temp_name)
        missing = module_copy(root / "missing")
        (missing / "config" / "tamesis_mc_v1.yaml").unlink()
        results.append({"case": "configuration_missing", **command([sys.executable, "validate_contract.py"], missing)})

        invalid = module_copy(root / "invalid")
        raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
        raw["structural_parameters"]["exponent"]["value"] = 7
        (invalid / "config" / "tamesis_mc_v1.yaml").write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
        results.append({"case": "configuration_invalid", **command([sys.executable, "validate_contract.py"], invalid)})

        cli = command([sys.executable, "validate_contract.py", "--M_c", "1e-15"], BASE)
        cli["case"] = "cli_override"
        results.append(cli)
        env = dict(__import__("os").environ)
        env["TAMESIS_MC_KG"] = "1e-15"
        env_result = command([sys.executable, "validate_contract.py"], BASE, env)
        env_result["case"] = "environment_override"
        results.append(env_result)

        sidecar_dir = root / "sidecar"
        sidecar_dir.mkdir()
        artifact = sidecar_dir / "artifact.json"
        artifact.write_text("{}", encoding="utf-8")
        sidecar_cmd = [sys.executable, "-c", f"from pathlib import Path; from config import load_v1_contract; from provenance import require_current_artifact; require_current_artifact(Path(r'{artifact}'), load_v1_contract())"]
        results.append({"case": "sidecar_missing", **command(sidecar_cmd, BASE)})

        manifest = json.loads((BASE / "data" / "artifact_manifest.json").read_text(encoding="utf-8"))
        manifest["config_hash"] = "0" * 64
        stale_path = root / "stale_manifest.json"
        stale_path.write_text(json.dumps(manifest), encoding="utf-8")
        stale_cmd = [sys.executable, "-c", f"from verify_artifacts import verify_manifest; verify_manifest(Path(r'{stale_path}'))"]
        # Path is intentionally imported by the command itself.
        stale_cmd[2] = "from pathlib import Path; " + stale_cmd[2]
        results.append({"case": "manifest_stale", **command(stale_cmd, BASE)})
    output = data_path("fail_closed_evidence.json")
    output.write_text(json.dumps({"protocol_id": contract.protocol_id(), "config_hash": contract.config_hash(), "cases": results}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_sidecar(output, provenance_record(output_path=output, contract=contract, script="audit_fail_closed.py"))
    print(json.dumps({"cases": [{"case": x["case"], "exit_code": x["exit_code"]} for x in results]}, indent=2))


if __name__ == "__main__":
    main()
