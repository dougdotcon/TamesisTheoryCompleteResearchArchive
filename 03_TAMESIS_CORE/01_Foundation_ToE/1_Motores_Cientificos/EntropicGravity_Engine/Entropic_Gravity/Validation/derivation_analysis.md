# Challenge 2: Theoretical Fundamentals

## The Interpolation Problem
The original code used a hard switch `if a_N < a_0`. This creates a `kink` in the force field, which implies an infinite jerk (da/dt) for particles crossing the threshold. This is unphysical.

## The Improved Derivation
We implemented the standard MOND interpolation function $\mu(x) = x/(1+x)$, inverted to solve for $g$:
$$ g = \frac{g_N + \sqrt{g_N^2 + 4 g_N a_0}}{2} $$

## Comparison Result
As seen in `interpolation_analysis.png`, the Green Curve (Smooth) creates a much more physical transition than the Red Curve (Naive). It avoids the sharp corner at the transition radius.

**Verdict:** The code must be updated to use the Smooth function to withstand peer review.

![Derivation Analysis](interpolation_analysis.png)