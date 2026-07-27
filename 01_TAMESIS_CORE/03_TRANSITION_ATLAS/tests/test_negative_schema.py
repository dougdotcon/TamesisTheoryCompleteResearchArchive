from __future__ import annotations

import pytest

from src.transition_atlas.models import Regime, Transition


def test_regime_unknown_field_rejected():
    with pytest.raises(Exception):
        Regime.model_validate({"regime_id": "x", "unknown": 0})


def test_transition_unknown_field_rejected():
    with pytest.raises(Exception):
        Transition.model_validate({"transition_id": "x", "unknown": 0})
