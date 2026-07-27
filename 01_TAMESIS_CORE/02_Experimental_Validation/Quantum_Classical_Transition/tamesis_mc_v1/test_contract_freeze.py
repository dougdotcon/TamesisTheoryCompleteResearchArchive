from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

import config as config_module
from config import ContractError, load_v1_contract
from mc_model import McModel, compute_mc_from_contract


def test_contract_reproduces_frozen_mc_and_protocol_id():
    contract = load_v1_contract()
    assert contract.mc_kg == pytest.approx(5.292674126388712e-16, rel=0, abs=1e-30)
    assert compute_mc_from_contract(contract) == pytest.approx(contract.mc_kg, rel=0, abs=1e-30)
    assert contract.protocol_id().startswith("tamesis-mc-v1.0:")
    assert contract.config_hash() in contract.protocol_id()


def test_model_is_bound_to_contract():
    model = McModel()
    assert model.mc == pytest.approx(5.292674126388712e-16, rel=0, abs=1e-30)
    assert model.summary()["protocol_id"].startswith("tamesis-mc-v1.0:")


def _write_temp_config(tmp_path: Path, mutate) -> Path:
    src = Path(config_module.CONFIG_PATH)
    data = yaml.safe_load(src.read_text(encoding="utf-8"))
    mutate(data)
    dst = tmp_path / "tamesis_mc_v1.yaml"
    dst.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return dst


def test_rejects_modified_mc(tmp_path: Path):
    bad_path = _write_temp_config(
        tmp_path,
        lambda data: data["derived_quantities"]["Mc_kg"].__setitem__("value", 1.23e-15),
    )
    with pytest.raises(ContractError):
        load_v1_contract(bad_path)


def test_rejects_modified_exponent(tmp_path: Path):
    bad_path = _write_temp_config(
        tmp_path,
        lambda data: data["structural_parameters"]["exponent"].__setitem__("value", 3.0),
    )
    with pytest.raises(ContractError):
        load_v1_contract(bad_path)


def test_rejects_modified_unit(tmp_path: Path):
    bad_path = _write_temp_config(
        tmp_path,
        lambda data: data["constants"]["H0"].__setitem__("unit", "m s^-1"),
    )
    with pytest.raises(ContractError):
        load_v1_contract(bad_path)


def test_hash_is_deterministic():
    contract1 = load_v1_contract()
    contract2 = load_v1_contract()
    assert contract1.config_hash() == contract2.config_hash()
    assert json.dumps(contract1.normalized_payload(), sort_keys=True) == json.dumps(contract2.normalized_payload(), sort_keys=True)

