# Tamesis M_c v1 — computational freeze

Freeze date: **2026-07-26**

## Frozen state

```text
software_status: frozen_and_ready
campaign_state: HARDWARE_QUALIFICATION_NOT_STARTED
physical_evidence: false
next_required_input: real_hardware_metadata_and_calibration_records
a2_status: blocked
tamesis_inference: prohibited
```

This is the legitimate endpoint of the exclusively computational program. The
repository contains a complete pre-hardware protocol, but no real instrument,
particle, calibration, thermal sweep, blind prediction, or reveal.

The current formal conclusion is:

```text
A0_A1_HARDWARE_PACKAGE_READY_WITH_LIMITATIONS
```

## Frozen identifiers

- Physical model:
  `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`
- Demonstrator A:
  `tamesis-demonstrator-a-v0.6:277a26656c9a4b20ae8c24295e0594b6d0ebfb7686fb7c04add68ed4f08119cd`
- Model mass:
  `M_c = 5.292674126388712e-16 kg`
- Model time:
  `tau_c = 2.176246482178091 s`
- Fixed mass exponent: `2`
- Fixed derivation root: `8`

These values must not be changed after observing data and still be described as
the same preregistered test.

## What the computational phase established

- a reproducible and falsifiable phenomenological contract;
- explicit comparisons with environmental decoherence, CSL, GRW, and
  Diósi–Penrose model families;
- synthetic evidence that single-time and contaminated designs can be
  structurally non-identifiable;
- the need for independent internal-particle thermometry;
- a platform and sensor feasibility audit;
- a fail-closed A0/A1 protocol for GeV-center single-particle thermometry;
- explicit separation between software readiness and physical evidence.

## What it did not establish

- that `M_c` is a measured constant;
- that a new quantum-to-classical law exists;
- that `Gamma_T` has been observed;
- that Tamesis is favored over environmental decoherence or collapse models;
- that GeV thermometry works in a levitated superposition experiment;
- any result comparable in evidential status to the Bohr model.

## Conditions for resumption

Work may resume when at least one of the following is supplied:

- a real instrument inventory with serial and calibration identifiers;
- certificates or documented calibration chains;
- raw spectra from identifiable GeV particles;
- real thermal time series;
- real A0 campaign records;
- documented access to a collaborating laboratory.

The next operational sequence is:

1. qualify hardware in Q0;
2. characterize candidate particles in A0;
3. derive stability, drift, Allan deviation, uncertainty, and heating limits;
4. run the randomized and blinded 5–20 K A1 sweep;
5. lock predictions before reveal;
6. issue only one of the four preregistered material-candidate decisions.

Until then, the external operational state is:

```text
PAUSED_PENDING_HARDWARE_AND_METROLOGY
```

## Canonical evidence

- [Campaign state](01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/data/demonstrator_a_v0_6/campaign_state.json)
- [Execution report](01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/DEMONSTRATOR_A_V0_6_EXECUTION_REPORT.md)
- [Limitations](01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/DEMONSTRATOR_A_V0_6_LIMITATIONS.md)
- [Q0 qualification](01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/Q0_INSTRUMENT_QUALIFICATION.md)
- [A0-to-A1 selection](01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/A0_TO_A1_SELECTION.md)
- [Blind validation result](01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/A1_BLIND_VALIDATION_RESULT.md)

This freeze preserves the research history. It does not erase Tamesis, TRI,
TDTR, or the Atlas; it prevents exploratory claims from being mistaken for the
current evidential result.
