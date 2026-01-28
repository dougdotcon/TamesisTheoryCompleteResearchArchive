# Stage 43: Formal Definition of "Regime"

## Status: IN PROGRESS

## Objective

Transform "regime" from informal discourse into a rigorous mathematical object.

---

## Core Definition

A **regime** is a triple:

```
R = (S, P, O)
```

| Component | Symbol | Description |
|-----------|--------|-------------|
| State Space | S | The mathematical space where states live |
| Perturbation | P | The mechanism that drives transitions |
| Observable | O | What we measure from the dynamics |

---

## Deliverables

- [x] Formal definition with examples
- [ ] Python implementation (`regime_formalism.py`)
- [ ] Catalog of known regimes (`regime_catalog.py`)
- [ ] Documentation (`index.html`)

---

## Key Insight

The regime triple (S, P, O) determines the universality class.

Changing ANY component → changes the critical exponent.

This is why U_{1/2} is specific to:

- S = Permutation space (discrete)
- P = Bernoulli perturbation
- O = Cycle counting

---

## Connection to Tamesis

The Tamesis program discovered U_{1/2} empirically.
TRI explains WHY it exists and WHY it differs from U_2, U_0.
