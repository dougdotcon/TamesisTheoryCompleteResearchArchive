# Zeta Connection

This directory contains tools for comparing operator eigenvalues with known Riemann zeros.

## Files

| File | Purpose |
|------|---------|
| `zeta_zeros_analysis.py` | Load Riemann zeros and compare with operator spectrum |

## Usage

```python
from zeta_zeros_analysis import RiemannZerosLoader, SpectralComparison

# Load zeros
loader = RiemannZerosLoader()
zeros = loader.load_zeros(n_zeros=100)

# Compare with operator eigenvalues
comp = SpectralComparison()
result = comp.compute_correlation(eigenvalues, zeros)
```

## Important Note

This is **numerical exploration**, not proof.
The correlation between our naive operator and Riemann zeros is expected to be weak.
