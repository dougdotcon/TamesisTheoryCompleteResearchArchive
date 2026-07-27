SENSOR_TRANSFER_MODELS_NOT_VALIDATED

# Sensor transfer models v0.2 execution report

Protocol: `tamesis-sensor-models-v0.2:35d8056bc6438062b2cbf951e1ec2fc2a1b130dadcfa1ec5d3a9bc41cc050562`. Previous protocols were preserved. Forward/inverse models were specified for pressure, temperature candidates, phase, detector, mass and trajectory. Full ideal fusion improves rank 3→9 and condition 517,445→67,267, but the absolute condition remains above the preregistered maximum 10,000. Internal temperature is not independently validated in 1–4 K; therefore the thermal false-threshold criterion and the phase-wide approval criteria are not met.

| Question | Result | Limitation |
|---|---|---|
| Temporal requirements derived? | Partly | latency/clock drift remain assumptions |
| T_int dynamic model? | Yes | particle parameters uncalibrated |
| Primary/secondary thermometry? | Candidate only | 1–4 K unsupported |
| Effective pressure identifiable? | Provisional | transfer extrapolation pending |
| Detector efficiency/saturation? | Simulation-calibrated | hardware calibration pending |
| Phase/trajectory reconstructible? | Provisional | transfer functions pending |
| Absolute condition improved? | Yes, to 67,267 | still above 10,000 |
| Thermal false threshold controlled? | Only ideal synthetic fusion | real sensor not demonstrated |
| Tamesis signal preserved? | Synthetic only | thermal bias can mimic it |
| 1e-15 kg testable? | Conditional | internal thermometry is required |
