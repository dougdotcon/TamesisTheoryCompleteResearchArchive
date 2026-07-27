# Protocol annex

## Frozen references

- Scientific freeze: [`../PROJECT_FREEZE.md`](../PROJECT_FREEZE.md)
- Machine-readable state: [`../PROJECT_STATE.json`](../PROJECT_STATE.json)
- Technical nucleus:
  [`../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/`](../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/)
- Demonstrator A v0.6 execution report:
  [`DEMONSTRATOR_A_V0_6_EXECUTION_REPORT.md`](../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/DEMONSTRATOR_A_V0_6_EXECUTION_REPORT.md)
- Q0 qualification report:
  [`Q0_INSTRUMENT_QUALIFICATION.md`](../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/Q0_INSTRUMENT_QUALIFICATION.md)
- A0 hardware runbook:
  [`A0_HARDWARE_RUNBOOK.md`](../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/A0_HARDWARE_RUNBOOK.md)
- A1 hardware runbook:
  [`A1_HARDWARE_RUNBOOK.md`](../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/reports/A1_HARDWARE_RUNBOOK.md)

## Protocol identity

```text
tamesis-demonstrator-a-v0.6:
277a26656c9a4b20ae8c24295e0594b6d0ebfb7686fb7c04add68ed4f08119cd
```

Repository snapshot:

```text
commit: c47e37ce7691628da664a533ec1a6c7c707a61c0
tag: tamesis-mc-v1-computational-freeze
tag: tamesis-demonstrator-a-v0.6-hardware-ready
```

The second tag must point to the same frozen commit. Operational collaboration
documents may evolve independently, but the scientific protocol does not.

## Required record schemas

Schemas already frozen in the technical nucleus include:

- `raw_spectral_record.schema.json`
- `particle_characterization_record.schema.json`
- `thermal_equilibrium_record.schema.json`
- `stationary_calibration_record.schema.json`
- `thermal_sweep_record.schema.json`
- `blind_temperature_prediction.schema.json`
- `blind_temperature_reveal.schema.json`
- `particle_selection_decision.schema.json`
- `invalid_run_record.schema.json`

Before acquisition, the laboratory should confirm that its native exports can
be mapped to these records without discarding raw data.

## Change-control rule

Hardware-driven clarifications are documented as deviations or amendments. A
new protocol version is justified only when real hardware reveals a requirement
that changes acquisition, blinding, inference, or a decision rule. Changes made
after observing validation truth cannot be applied retroactively.

