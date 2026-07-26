from environment_model import Environment, pressure_for_rate


def test_gas_collision_rate_scales_with_pressure():
    mass = 1e-15
    low = Environment(pressure_pa=1e-15).gas_collision_rate(mass)
    high = Environment(pressure_pa=1e-12).gas_collision_rate(mass)
    assert abs((high / low) - 1000.0) < 1e-9


def test_pressure_for_rate_inverts_gas_rate():
    mass = 1e-15
    target_rate = 1.0
    pressure = pressure_for_rate(target_rate, mass)
    env = Environment(pressure_pa=pressure)
    assert abs(env.gas_collision_rate(mass) - target_rate) < 1e-12
