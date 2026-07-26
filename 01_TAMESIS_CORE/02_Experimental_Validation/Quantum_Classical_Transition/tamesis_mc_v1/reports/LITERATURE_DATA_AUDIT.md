# Literature Data Audit

## Current state

`data/literature_points.csv` is a mixed table:

- observed consistency checks
- planned targets
- excluded non-CM cases

It is useful, but it is not yet the validated schema requested by the technical review.

## What is missing

The current table lacks most of the following fields:

- authors
- year
- DOI
- arXiv source version
- access date
- uncertainty columns
- explicit geometry
- raw-data availability
- code availability
- source provenance per row

## What is already useful

Observed rows:

- C60 fullerene diffraction
- molecule interference beyond 10,000 amu
- oligoporphyrin interference beyond 25 kDa
- sodium nanoparticle interference above 170 kDa

Planned rows:

- throw-and-catch SiO2
- MAQRO
- space high-mass target
- nanodiamond chip proposal
- `1e-15 kg` target

## Important classification

The sodium nanoparticle experiment is a strong observed benchmark, but it is still far below `M_c`.
It validates the low-threshold side only.

The `1e-15 kg` entries are not observed data.
They are target proposals.

## Inference warning

Many current rows have only:

- mass
- separation
- time
- binary coherence status

That is not yet enough for strong model identification.

## Conclusion

The table is adequate for triage.
It is not yet adequate for final discrimination between Tamesis, CSL, GRW, DP and environment.

