# V1.0 Executable Freeze Report

## Frozen parameters

- `M_c = 5.292674126388712e-16 kg`
- `tau_c = 2.176246482178091 s`
- exponent `= 2.0`
- phase-space root `= 8`
- `H_0 = 70 km s^-1 Mpc^-1`
- silica density `= 2200 kg m^-3`

## Contract hash

- `d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`

## Protocol ID

- `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`

## Files that previously risked redefining parameters

- `mc_model.py`
- `analyze_target_1e15.py`
- `compare_models.py`
- `generate_figures.py`
- `run_predictions.py`
- `STATUS.md`

## Conflicts found

- `2.2e-14 kg` in historical status text
- `1e-15 kg / 50 µm / 0.1 s` treated too strongly before the feasibility audit
- exploratory ranking was being read as scientific preference

## Refactorings performed

- added canonical loader
- added schema and lock
- bound model to contract
- added provenance sidecars
- added automatic manifest
- split literature into schema-expanded v2
- bound figure generation directly to the canonical contract

## Results reproduced

- `M_c`
- `tau_c`
- `V(0.1 s)`
- `V(1 s)`
- `1e-15 kg` target analysis

## Results changed

- only metadata and provenance
- no core numeric prediction changed

## Legacy artifacts

- historical root folders in `90_LEGACY`
- exploratory ranking
- old narrative files

## Coverage

- contract validation: passed
- pytest: passed (`12 passed`)
- manifest build: passed
- artifact verification: passed

## Remaining limitations

- rival models remain simplified
- environment model remains first-pass
- 50 µm target support remains provisional

## No adjustment confirmation

No structural parameter was fit or retuned to pass tests.
The freeze is executable, not merely textual.
