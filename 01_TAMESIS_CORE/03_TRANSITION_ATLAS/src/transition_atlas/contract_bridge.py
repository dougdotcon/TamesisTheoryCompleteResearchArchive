from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any


ATLAS_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ATLAS_ROOT.parents[1]
TAMESIS_ROOT = REPO_ROOT / "01_TAMESIS_CORE" / "02_Experimental_Validation" / "Quantum_Classical_Transition" / "tamesis_mc_v1"
CONFIG_PATH = TAMESIS_ROOT / "config.py"


def load_tamesis_contract() -> dict[str, Any]:
    """Read the active Tamesis contract without copying its structural values."""
    spec = importlib.util.spec_from_file_location("tamesis_mc_v1_config_bridge", CONFIG_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import canonical Tamesis config: {CONFIG_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    contract = module.load_v1_contract()
    payload = module.resolved_contract_payload(contract)
    payload["source_path"] = TAMESIS_ROOT.relative_to(REPO_ROOT).as_posix()
    return payload


def tamesis_integration() -> dict[str, Any]:
    payload = load_tamesis_contract()
    return {
        "protocol_id": payload["protocol_id"],
        "config_hash": payload["config_hash"],
        "Mc_kg": payload["resolved_si"]["Mc_kg"],
        "H0_original": payload["normalized_contract"]["constants"]["H0"]["value"],
        "H0_SI": payload["resolved_si"]["H0_s-1"],
        "tau_c_s": payload["resolved_si"]["tau_c_s"],
        "phase_space_root": payload["structural"]["phase_space_root"],
        "exponent": payload["structural"]["exponent"],
        "alpha": payload["structural"]["alpha"],
        "transition_width": payload["structural"]["transition_width"],
        "visibility_equation": payload["normalized_contract"]["equations"]["visibility"],
        "gamma_equation": payload["structural"]["functional_form"],
        "validity_domain": payload["validity_domain"],
        "limitations": ["separation", "geometry", "composition", "multiparticle_rule", "complete_dynamics"],
        "source_path": payload["source_path"],
    }
