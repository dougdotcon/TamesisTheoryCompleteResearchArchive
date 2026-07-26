# Target 1e-15 kg: decision matrix

This is the current first-pass decision for the strongest Tamesis candidate.

## Tamesis core

```text
M = 1e-15 kg
M/Mc = 1.8894
V_Tamesis(0.1 s) = 0.8487
V_Tamesis(1.0 s) = 0.1939
```

## Gas environment

- clean first-pass boundary: `P_gas < 7e-13 Pa`
- at `1e-15 Pa`: gas is negligible
- at `1e-12 Pa`: gas is a small nuisance
- at `1e-10 Pa`: gas dominates

## Normalized chip noise

Using the extracted contrast tolerances:

- magnetic gradient fluctuation tolerance: `1e-7`
- initial position tolerance: `1e-9 m`

the normalized first-pass noise scan gives:

- best case: Tamesis remains visible
- at tolerance: Tamesis remains visible but closer to the edge
- 10x worse: Tamesis is suppressed

## Conclusion

This target is not yet a discovery.
It is the first place where a Bohr-level discovery could realistically happen.

The experiment must satisfy both:

- vacuum in the `10^-13 Pa` class or better;
- chip noise close to the extracted contrast tolerances.

If those conditions fail, the target remains interesting but non-decisive.
