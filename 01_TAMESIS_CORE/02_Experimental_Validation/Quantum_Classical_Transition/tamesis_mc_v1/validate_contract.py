from __future__ import annotations

from config import load_v1_contract, reject_runtime_overrides
from mc_model import compute_mc_from_contract, compute_tau_c_from_contract


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    mc_calc = compute_mc_from_contract(contract)
    tau_calc = compute_tau_c_from_contract(contract, contract.mc_kg)
    print(
        {
            "protocol_id": contract.protocol_id(),
            "config_hash": contract.config_hash(),
            "mc_calculated": mc_calc,
            "mc_frozen": contract.mc_kg,
            "tau_calculated": tau_calc,
            "tau_frozen": contract.tau_c_s,
        }
    )


if __name__ == "__main__":
    main()
