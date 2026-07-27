from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from config import load_v1_contract, reject_runtime_overrides
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path


BASE = Path(__file__).resolve().parent


def run_variant(name: str, mutate) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"tamesis-summary-{name}-") as temp_name:
        parent = Path(temp_name)
        module = parent / "01_TAMESIS_CORE" / "02_Experimental_Validation" / "Quantum_Classical_Transition" / "tamesis_mc_v1"
        shutil.copytree(BASE, module)
        summary = module / "data" / "model_summary.json"
        mutate(summary)
        # plot_predictions intentionally validates its upstream model_summary chain;
        # the remaining figures/GIF exercise the structural visual path directly.
        command = [sys.executable, "-c", "import generate_figures as g; g.plot_literature(); g.plot_target_1e15(); g.plot_thermal_gate(); g.plot_bohr_window_map(); g.make_threshold_animation()"]
        completed = subprocess.run(command, cwd=module, capture_output=True, text=True)
        return {"variant": name, "command": " ".join(command), "exit_code": completed.returncode, "stdout_tail": completed.stdout[-1000:], "stderr_tail": completed.stderr[-1000:], "expected": completed.returncode == 0}


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    evidence = {
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "variants": [
            run_variant("absent", lambda p: (p.unlink(), p.with_suffix(".json.provenance.json").unlink(missing_ok=True))),
            run_variant("incorrect_Mc", lambda p: p.write_text(json.dumps({"Mc_kg": 1e-9, "tau_c_s": contract.tau_c_s}), encoding="utf-8")),
            run_variant("incorrect_tau_c", lambda p: p.write_text(json.dumps({"Mc_kg": contract.mc_kg, "tau_c_s": 1e9}), encoding="utf-8")),
            run_variant("malformed", lambda p: p.write_text("{not-json", encoding="utf-8")),
        ],
        "structural_source": "generate_figures.py: CONTRACT = load_v1_contract(); all structural figure/GIF functions use CONTRACT.mc_kg, CONTRACT.tau_c_s or CONTRACT.exponent; model_summary is not read.",
    }
    output = data_path("model_summary_independence_evidence.json")
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_sidecar(output, provenance_record(output_path=output, contract=contract, script="audit_model_summary_independence.py"))
    print(json.dumps({"variants": [{"name": x["variant"], "exit_code": x["exit_code"]} for x in evidence["variants"]]}, indent=2))


if __name__ == "__main__":
    main()
