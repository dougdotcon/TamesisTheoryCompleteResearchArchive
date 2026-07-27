# Q0 — formulário de inventário para o laboratório

Use `confirmed`, `unknown` ou `not_available`; anexe evidência. Não use valores
de catálogo como se fossem medidos.

```text
lab_name:
institution:
principal_contact:
technical_contact:
date:
instrument_operator:
data_custodian:

cryostat_model:
cryostat_serial:
sample_space:
optical_access:
operating_range_K:
primary_reference_thermometer:
reference_serial:
reference_calibration_id:
reference_calibration_date:
reference_range_K:
reference_uncertainty_K:
traceability_status:
secondary_stage_thermometer:
controller_model:
temperature_readback_rate:

optical_source_model:
source_wavelength_nm:
power_meter_model:
power_meter_serial:
power_calibration_id:
power_at_particle_estimation_method:
wavelength_reference:
spectrometer_model:
spectrometer_serial:
spectral_resolution_nm:
detector_model:
detector_linearity_range:
detector_saturation_test:
timed_acquisition:
dark_acquisition_supported:
background_acquisition_supported:
raw_export_format:

magnetic_field_control_or_sensor:
strain_or_polarization_controls:
sample_source_or_lot:
candidate_centers:
particle_identification_method:
particle_relocation_method:
particle_morphology_measurement:
sample_manipulation_history:

q0_status: HARDWARE_QUALIFICATION_PASSED | HARDWARE_QUALIFICATION_FAILED
blocking_items:
evidence_links:
operator_signature:
```

