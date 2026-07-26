"""Minimal environmental decoherence estimates for M_c target triage.

This is not a full experimental noise model. It is a transparent first-pass
calculator for deciding whether a proposed target is worth deeper analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from math import exp, pi, sqrt


@dataclass(frozen=True)
class Environment:
    pressure_pa: float = 1e-15
    gas_temperature_k: float = 20.0
    gas_molecular_mass_kg: float = 28.0 * 1.66053906660e-27
    material_density_kg_m3: float = 3500.0
    magnetic_or_current_noise_rate_s: float = 0.0
    blackbody_rate_s: float = 0.0

    @property
    def boltzmann(self) -> float:
        return 1.380649e-23

    def radius_from_mass(self, mass_kg: float) -> float:
        return (3.0 * mass_kg / (4.0 * pi * self.material_density_kg_m3)) ** (1.0 / 3.0)

    def gas_collision_rate(self, mass_kg: float) -> float:
        """Rough hard-sphere gas collision rate n sigma v."""
        if self.pressure_pa <= 0:
            return 0.0
        number_density = self.pressure_pa / (self.boltzmann * self.gas_temperature_k)
        radius = self.radius_from_mass(mass_kg)
        cross_section = pi * radius * radius
        mean_speed = sqrt(8.0 * self.boltzmann * self.gas_temperature_k / (pi * self.gas_molecular_mass_kg))
        return number_density * cross_section * mean_speed

    def total_rate(self, mass_kg: float) -> float:
        return (
            self.gas_collision_rate(mass_kg)
            + self.magnetic_or_current_noise_rate_s
            + self.blackbody_rate_s
        )

    def visibility(self, mass_kg: float, time_s: float) -> float:
        return exp(-self.total_rate(mass_kg) * time_s)

    def summary(self, mass_kg: float) -> dict:
        data = asdict(self)
        data.update(
            {
                "particle_radius_m": self.radius_from_mass(mass_kg),
                "gas_collision_rate_s-1": self.gas_collision_rate(mass_kg),
                "total_environment_rate_s-1": self.total_rate(mass_kg),
            }
        )
        return data


def pressure_for_rate(target_rate_s: float, mass_kg: float, temperature_k: float = 20.0) -> float:
    """Invert the gas-collision estimate for a desired collision rate."""
    env = Environment(pressure_pa=1.0, gas_temperature_k=temperature_k)
    rate_at_one_pa = env.gas_collision_rate(mass_kg)
    if rate_at_one_pa == 0:
        return float("inf")
    return target_rate_s / rate_at_one_pa
