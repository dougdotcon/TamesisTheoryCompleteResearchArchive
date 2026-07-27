# Blind calibration of GeV nanodiamond thermometry at 5–20 K

## 1. Scope and motivation

This project asks whether the spectrum of an individual GeV-bearing diamond
particle can provide calibrated stationary thermometry between 5 K and 20 K.
The central difficulty is not merely detecting a temperature-dependent optical
feature. The response must be separated from laser heating, spectral diffusion,
strain, charge-state changes, magnetic field, detector effects, wavelength
drift, and particle-to-particle variation.

The protocol therefore treats thermometry as a transfer-model and metrology
problem. Each particle retains a persistent identity, all raw data are
preserved, calibration is particle-specific, and final validation is blind.

This phase explicitly excludes levitation, spatial superposition, collapse
models, interferometric visibility, `Gamma_T`, and `M_c` inference.

## 2. Experimental architecture

The minimal stationary arrangement comprises:

- a cryostat capable of controlled operation over 5–20 K;
- a traceable or documented primary reference thermometer;
- a secondary thermometer near the sample stage;
- temperature control with timestamped readback;
- a low-power optical excitation source;
- traceable or characterized optical power measurement;
- wavelength reference and spectrometer;
- characterized detector and timed acquisition;
- dark and background acquisition;
- magnetic field measurement or control;
- raw spectral storage with immutable identifiers;
- a method to relocate the same particle.

The sample is preferably an individually addressable GeV-bearing nanodiamond or
small diamond particle with documented origin, morphology, manipulation
history, and initial raw spectrum.

## 3. Q0 — hardware qualification

Q0 is completed before any physical result is accepted. Every instrument is
registered with:

```text
instrument_id
instrument_type
manufacturer
model
serial_number
calibration_id
calibration_date
calibration_range
measurement_uncertainty
resolution
repeatability
drift
traceability_status
data_format
responsible_person
```

Unknown information remains `unknown`. A manufacturer specification is not a
substitute for a calibration record.

Q0 fails if the reference thermometer has no defensible traceability chain,
spectral resolution is inadequate for the observed response, power at the
particle cannot be bounded, detector nonlinearity is uncontrolled, raw data
cannot be preserved, timing is irrecoverable, or particle identity is not
persistent.

The only Q0 outcomes are:

```text
HARDWARE_QUALIFICATION_PASSED
HARDWARE_QUALIFICATION_FAILED
```

Failure is informative and must include the blocking component and evidence.

## 4. A0 — pilot particle characterization

### 4.1 Registration

Assign each physical particle a stable `particle_id`. Record sample lot,
supplier or fabrication route, substrate/location coordinates, images,
dimensions or morphology, GeV identification evidence, and manipulation
history. The identifier must survive sessions and operators.

### 4.2 Acquisition block

For each particle and session:

1. record instrument and calibration identifiers;
2. record dark and background;
3. acquire an initial raw spectrum at the lowest viable power;
4. run randomized excitation-power levels;
5. insert return-to-low-power measurements;
6. acquire a fixed-condition stability time series;
7. characterize detector and optical saturation;
8. quantify line position, linewidth, intensity, and spectral diffusion;
9. vary magnetic field when available;
10. record known or suspected strain, charge, orientation, and polarization
    effects;
11. preserve raw counts, wavelength coordinates, timestamps, and telemetry.

Raw data must never be overwritten by corrected data. Any processing product
receives a new identifier and records its inputs.

### 4.3 A0 decisions

```text
advance_to_A1
repeat_A0
reject_candidate
inconclusive
```

`advance_to_A1` means only that the particle is sufficiently stable and
characterized to attempt blind calibration. It is not a thermometry validation.

## 5. Derivations required before A1

Real time series, not simulated values, must determine:

- short- and long-window stability;
- drift rate and confidence interval;
- Allan deviation over relevant integration times;
- autocorrelation and effective sample size;
- equilibrium/settling criteria;
- wavelength-reference contribution;
- detector and fitting uncertainty;
- reference-thermometer uncertainty;
- repeatability and hysteresis;
- optical self-heating limit `Delta T_max,budget`.

No universal self-heating threshold is assumed in advance. The budget must be
derived from the partner instrument and the intended thermometry accuracy.

## 6. A1 — blind stationary calibration

A1 spans 5–20 K using ascending, descending, and randomized blocks with
replication and multiple accepted optical powers. Equilibrium is declared only
using criteria derived before validation.

Four roles should be separated where practical:

- hardware operator;
- data custodian, who retains the hidden temperatures;
- calibration analyst, who builds the model on development data;
- blind validation analyst, who receives coded validation spectra.

Filnames, directories, timestamps, acquisition order, metadata, and temperature
controller exports can leak hidden setpoints. The custodian must produce a
sanitized blind package and record a leakage audit.

The calibration model is frozen before validation predictions. Every prediction
is associated with a sample ID, uncertainty interval, model hash, input hash,
and timestamp. The reference reveal occurs only after coverage is complete and
hashes are verified.

## 7. Success, failure, and publication

The protocol does not impose a positive result. Final material decisions are:

```text
material_candidate_selected
material_candidate_not_selected
material_candidate_inconclusive
calibration_run_invalid
```

Numerical acceptance thresholds must be agreed and preregistered after Q0/A0
characterize achievable resolution, but before the blind validation set is
revealed. At minimum the decision addresses calibration error, uncertainty
coverage, repeatability, hysteresis, usable yield, and self-heating.

A negative or inconclusive result remains publishable if it identifies physical
limits, cross-sensitivities, or metrological requirements. A selected candidate
means only that stationary particle-specific thermometry worked in the
demonstrated domain. It does not establish levitated thermometry or support
Tamesis.

## 8. First pilot request

The smallest pilot uses one persistently identifiable GeV particle and produces:

- one complete Q0 inventory;
- raw dark/background;
- an initial low-power spectrum;
- a short randomized power sweep;
- return-to-low-power checks;
- a fixed-condition stability series;
- complete instrument and particle metadata.

This pilot should be reviewed before expanding the number of particles or
committing cryostat time to A1.

## 9. Collaboration structure

The experimental partner controls hardware safety and operation. The protocol
coordinator maintains the frozen design, schemas, provenance, and analysis.
Data ownership, embargo, authorship criteria, repository visibility, sample
ownership, costs, and right to publish negative results must be agreed before
acquisition.

No partner is asked to endorse Tamesis. The collaboration is complete and
scientifically useful as a standalone GeV thermometry study.

