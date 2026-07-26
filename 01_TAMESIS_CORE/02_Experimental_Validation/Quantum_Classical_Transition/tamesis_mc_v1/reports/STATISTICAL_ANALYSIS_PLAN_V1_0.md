# Statistical Analysis Plan v1.0

## Primary observable

Primary observable:

- fringe visibility, or
- binary coherence outcome when visibility is not available

## Likelihood

Current default likelihood:

- Bernoulli likelihood for observed coherence / decoherence

If raw fringe counts become available:

- use a count-based likelihood instead

## Model classes

- Tamesis M_c v1
- CSL
- GRW
- Diósi–Penrose
- environmental baseline

## Nuisance parameters

At minimum:

- gas collision rate
- magnetic/current noise rate
- blackbody rate
- family-specific nuisance decay where justified

## Priors

This version should be pre-registered before final inference.

Until then:

- do not use post-hoc priors to rescue model fit

## Inclusion / exclusion

Include only rows with:

- verified source
- explicit status
- reproducible numeric fields

Exclude:

- internal phononic / non-CM cases
- illustrative points
- unknown provenance rows

## Discrimination rule

Report a model as preferred only if:

- the likelihood difference is material,
- the model remains identifiable under nuisance variation,
- and the result survives the registered comparison set.

## Allowed outcomes

- `excluded_under_registered_assumptions`
- `compatible_but_not_tested`
- `models_not_identifiable`
- `environment_dominated`
- `tamesis_preferred_within_registered_model_set`
- `rival_model_preferred_within_registered_model_set`
- `insufficient_data`

## Current status

The current dataset is still closer to:

- `compatible_but_not_tested`
- `models_not_identifiable`

than to a decisive final comparison.

