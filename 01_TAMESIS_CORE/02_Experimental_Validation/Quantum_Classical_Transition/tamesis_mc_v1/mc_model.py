"""Tamesis M_c v1.0: minimal, auditable critical-mass model.

This module intentionally contains no fitted curve and no environmental model.
Environmental decoherence must be measured or supplied as a nuisance rate.
The 1/8 exponent and the sharp threshold are hypotheses of this version.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt


@dataclass(frozen=True)
class Constants:
    G: float = 6.67430e-11
    hbar: float = 1.054571817e-34
    c: float = 299_792_458.0
    h0_km_s_mpc: float = 70.0
    silica_density: float = 2200.0

    @property
    def h0_s(self) -> float:
        return self.h0_km_s_mpc * 1000.0 / 3.0856775814913673e22

    @property
    def planck_length(self) -> float:
        return sqrt(self.hbar * self.G / self.c**3)

    @property
    def planck_mass(self) -> float:
        return sqrt(self.hbar * self.c / self.G)

    @property
    def planck_acceleration(self) -> float:
        return self.c**2 / self.planck_length

    @property
    def a0(self) -> float:
        return self.c * self.h0_s


@dataclass(frozen=True)
class McModel:
    """Minimal Tamesis threshold model.

    Status of quantities:
      - h0_km_s_mpc and silica_density: experimental/model inputs;
      - exponent: hypothesis (not derived in v1.0);
      - mc, radius, tau_c: derived quantities;
      - threshold and environmental independence: falsifiable hypotheses.
    """

    constants: Constants = Constants()
    exponent: float = 2.0
    phase_space_root: int = 8

    def __post_init__(self) -> None:
        if self.exponent <= 0:
            raise ValueError("exponent must be positive")
        if self.phase_space_root <= 0:
            raise ValueError("phase_space_root must be positive")

    @property
    def mc(self) -> float:
        c = self.constants
        return c.planck_mass * (c.a0 / c.planck_acceleration) ** (1.0 / self.phase_space_root)

    @property
    def radius(self) -> float:
        return (3.0 * self.mc / (4.0 * pi * self.constants.silica_density)) ** (1.0 / 3.0)

    @property
    def tau_c(self) -> float:
        c = self.constants
        # Convention used by the existing Tamesis proposal: E_g = G M^2 / R.
        return c.hbar * self.radius / (c.G * self.mc**2)

    @property
    def threshold_rate(self) -> float:
        return 1.0 / self.tau_c

    def intrinsic_rate(self, mass: float) -> float:
        """One-sided sharp-threshold rate Γ_T(M), in s^-1."""
        if mass < 0:
            raise ValueError("mass must be non-negative")
        if mass <= self.mc:
            return 0.0
        return self.threshold_rate * (mass / self.mc) ** self.exponent

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

    def summary(self) -> dict[str, float]:
        c = self.constants
        return {
            "H0_km_s_Mpc": c.h0_km_s_mpc,
            "a0_m_s2": c.a0,
            "phase_space_root_hypothesis": float(self.phase_space_root),
            "exponent_hypothesis": self.exponent,
            "Mc_kg": self.mc,
            "Mc_amu": self.mc / 1.66053906660e-27,
            "silica_radius_m": self.radius,
            "tau_c_s": self.tau_c,
            "threshold_rate_s-1": self.threshold_rate,
        }
