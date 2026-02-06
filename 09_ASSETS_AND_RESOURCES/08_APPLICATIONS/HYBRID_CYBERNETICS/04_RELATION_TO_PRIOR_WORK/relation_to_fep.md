# Relation to the Free Energy Principle (FEP)

Karl Friston's *Free Energy Principle* states that biological agents minimize Variational Free Energy (Surprise) to maintain homeostasis.
$$ F = E_q[\ln q(\vartheta) - \ln p(o, \vartheta)] $$

## The Coupled FEP Problem

In a Hybrid System, we have two agents minimizing Free Energy:

1. **AI ($M$):** Minimizes prediction error on the *next token* (Local textual consistency).
2. **Human ($H$):** Minimizes prediction error on the *world state* (Global semantic consistency).

## The Conflict

These two objectives are orthogonal.

- $M$ can minimize its Free Energy by hallucinating a plausible lie.
- This lie *increases* the Free Energy of $H$ (Surprise upon verification).

**Hybrid Cybernetics** is the study of the **Nash Equilibrium-like state** where minimizing $F_M$ does not maximize $F_H$. We seek a "Pareto-Optimal Inference".
