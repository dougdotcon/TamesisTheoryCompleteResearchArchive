"""Tests for the auditable M_c v1.0 model."""

from math import isclose

from mc_model import McModel


def test_derived_scale_and_radius() -> None:
    model = McModel()
    assert isclose(model.mc, 5.292674e-16, rel_tol=2e-6)
    assert isclose(model.radius, 3.85823e-7, rel_tol=2e-6)
    assert isclose(model.tau_c, 2.17625, rel_tol=2e-6)


def test_sharp_threshold_is_explicit() -> None:
    model = McModel()
    assert model.intrinsic_rate(model.mc) == 0.0
    assert isclose(model.intrinsic_rate(model.mc * (1.0 + 1e-9)), 1.0 / model.tau_c, rel_tol=1e-8)


def test_quadratic_scaling_above_threshold() -> None:
    model = McModel()
    assert isclose(model.intrinsic_rate(2.0 * model.mc) / model.intrinsic_rate(4.0 * model.mc), 0.25)


def test_environment_is_an_explicit_nuisance() -> None:
    model = McModel()
    assert model.visibility(0.5 * model.mc, 1.0, environmental_rate=1.0) < 1.0
    assert model.intrinsic_rate(0.5 * model.mc) == 0.0
