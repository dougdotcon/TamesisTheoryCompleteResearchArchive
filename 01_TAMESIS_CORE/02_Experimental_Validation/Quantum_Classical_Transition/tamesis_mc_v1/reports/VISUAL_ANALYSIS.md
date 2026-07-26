# Visual Analysis — Tamesis M_c v1

Generated from:

- `data/model_summary.json`
- `data/predictions.csv`
- `data/literature_points.csv`
- `data/target_1e15_analysis.json`
- `data/target_1e15_decision.json`
- `data/target_1e15_thermal_gate.json`

Figures:

- `figures/01_predictions.png`
- `figures/02_literature_points.png`
- `figures/03_target_1e15_visibility.png`
- `figures/04_thermal_gate.png`
- `figures/05_bohr_window_map.png`
- `figures/threshold_activation_loop.gif`
- `figures/bohr_window_loop.gif`

## 1. Prediction curve

The prediction curve shows a sharp qualitative change around `M = M_c`.

Below `M_c`, the current phenomenological model predicts no intrinsic collapse-like loss.
Above `M_c`, the intrinsic rate grows and visibility falls rapidly.

Current numerical anchor:

- `M_c = 5.292674126388712e-16 kg`
- `M_c ≈ 3.187e11 amu`

Interpretation:

The model is not claiming a proof of new physics yet. It is defining a sharp experimental target: if the transition is real, the first useful tests must live near or above this mass scale.

## 2. Literature points

The observed literature points currently sit far below `M_c`.

Interpretation:

Existing observed matter-wave results do not seriously test the Tamesis M_c threshold. They are useful sanity checks because the model must not falsely suppress known molecular and cluster interference, but they are not decisive.

The planned higher-mass experiments matter much more because they begin to approach or cross the active threshold region.

## 3. `1e-15 kg` visibility budget

The `1e-15 kg` target is above the current threshold:

- `M / M_c ≈ 1.889`
- Tamesis visibility at `0.1 s`: `≈ 0.849`
- Tamesis visibility at `1 s`: `≈ 0.194`

This is the first target in the archive that behaves like a candidate decisive experiment.

The scenario plot shows:

- best-case noise: Tamesis signature survives
- at-tolerance noise: Tamesis signature remains visible but less clean
- ten-times-worse noise: signal is suppressed and becomes non-decisive

Interpretation:

This is not finished science yet, but it is the strongest current candidate line.
The experiment only becomes meaningful if the environmental and chip-specific nuisance channels are tightly controlled.

## 4. Thermal gate

The thermal gate plot says:

- `0.1 K` and `1 K`: low blackbody risk
- `4 K`: borderline
- `10 K` and `20 K`: blackbody-dominant

Interpretation:

For a clean first-pass Tamesis test, the design target should be near `1 K` or colder.
Treat `4 K` as an upper warning gate, not as an ideal operating point.

## Current scientific conclusion

Tamesis M_c v1 is not finished.

The current state is:

1. The historical literature does not yet discriminate the model.
2. The `1e-15 kg` target is the real candidate frontier.
3. The decisive regime requires:
   - mass above `M_c`
   - coherence time around `0.1 s`
   - pressure near or below the `10^-13 Pa` band for a clean first-pass test
   - cryogenic temperature, ideally near `1 K` or colder
   - chip noise kept near or better than the extracted tolerance

## Next visual step

Generate a 2D decision map over:

- mass
- observation time
- pressure
- temperature class

The goal is to draw the first explicit `Bohr-window` map:

where Tamesis predicts measurable loss, while ordinary environmental decoherence remains subdominant.

## 5. Bohr-window map and loop animations

The static `Bohr-window` map shows the mass/time region where the intrinsic
Tamesis visibility loss becomes measurable.

The orange `1e-15 kg` candidate is above the threshold and inside the first
interesting frontier band. It is not deep into the saturated-loss region, which
is useful: the experiment would not merely say "everything decohered"; it could
measure a partial visibility loss.

The loop animations are mirrored to the repository root under:

- `02_TAMESIS_MC_V1_OUTPUTS/animations/threshold_activation_loop.gif`
- `02_TAMESIS_MC_V1_OUTPUTS/animations/bohr_window_loop.gif`

They are intentionally reversible loops: the final frame returns to the initial
state, making the transition easier to inspect repeatedly.
