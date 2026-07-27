"""Tamesis M_c v1.0 core model bound to the canonical contract."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt

from config import V1Contract, load_v1_contract


def compute_mc_from_contract(contract: V1Contract) -> float:
    c = float(contract.constants.c.value)
    hbar = float(contract.constants.hbar.value)
    G = float(contract.constants.G.value)
    h0 = contract.h0_si
    planck_length = sqrt(hbar * G / c**3)
    planck_mass = sqrt(hbar * c / G)
    planck_acceleration = c**2 / planck_length
    a0 = c * h0
    return planck_mass * (a0 / planck_acceleration) ** (1.0 / contract.phase_space_root)


def compute_tau_c_from_contract(contract: V1Contract, mc: float | None = None) -> float:
    G = float(contract.constants.G.value)
    hbar = float(contract.constants.hbar.value)
    density = float(contract.constants.silica_density.value)
    mc_value = contract.mc_kg if mc is None else mc
    radius = (3.0 * mc_value / (4.0 * pi * density)) ** (1.0 / 3.0)
    return hbar * radius / (G * mc_value**2)


@dataclass(frozen=True)
class McModel:
    """Minimal threshold model that reads the frozen v1.0 contract."""

    contract: V1Contract | None = None

    def __post_init__(self) -> None:
        if self.contract is None:
            object.__setattr__(self, "contract", load_v1_contract())
        # Fail closed if frozen values drift from the canonical equation.
        mc_calc = compute_mc_from_contract(self.contract)
        if abs(mc_calc - self.contract.mc_kg) > 1e-30:
            raise ValueError(
                f"contract Mc mismatch: calculated={mc_calc} frozen={self.contract.mc_kg} "
                f"hash={self.contract.config_hash()}"
            )
        tau_calc = compute_tau_c_from_contract(self.contract, self.contract.mc_kg)
        if abs(tau_calc - self.contract.tau_c_s) > 1e-15:
            raise ValueError(
                f"contract tau_c mismatch: calculated={tau_calc} frozen={self.contract.tau_c_s} "
                f"hash={self.contract.config_hash()}"
            )

    @property
    def mc(self) -> float:
        return self.contract.mc_kg

    @property
    def radius(self) -> float:
        density = float(self.contract.constants.silica_density.value)
        return (3.0 * self.mc / (4.0 * pi * density)) ** (1.0 / 3.0)

    @property
    def tau_c(self) -> float:
        return self.contract.tau_c_s

    @property
    def threshold_rate(self) -> float:
        return 1.0 / self.tau_c

    def intrinsic_rate(self, mass: float) -> float:
        """One-sided sharp-threshold rate Γ_T(M), in s^-1."""
        if mass < 0:
            raise ValueError("mass must be non-negative")
        if mass <= self.mc:
            return 0.0
        return self.threshold_rate * (mass / self.mc) ** self.contract.exponent

    def coherence_time(self, mass: float) -> float:
        rate = self.intrinsic_rate(mass)
        return float("inf") if rate == 0.0 else 1.0 / rate

    def visibility(self, mass: float, time_s: float, environmental_rate: float = 0.0) -> float:
        if time_s < 0 or environmental_rate < 0:
            raise ValueError("time and environmental_rate must be non-negative")
        return exp(-(self.intrinsic_rate(mass) + environmental_rate) * time_s)

    def half_visibility_time(self, mass: float, environmental_rate: float = 0.0) -> float:
        rate = self.intrinsic_rate(mass) + environmental_rate
        return float("inf") if rate == 0.0 else log(2.0) / rate

    def summary(self) -> dict[str, float | str]:
        return {
            "protocol_id": self.contract.protocol_id(),
            "config_hash": self.contract.config_hash(),
            "H0_km_s_Mpc": float(self.contract.constants.H0.value),
            "a0_m_s2": self.contract.h0_si * float(self.contract.constants.c.value),
            "phase_space_root_hypothesis": float(self.contract.phase_space_root),
            "exponent_hypothesis": self.contract.exponent,
            "Mc_kg": self.mc,
            "Mc_amu": self.mc / 1.66053906660e-27,
            "silica_radius_m": self.radius,
            "tau_c_s": self.tau_c,
            "threshold_rate_s-1": self.threshold_rate,
        }

