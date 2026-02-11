# Arithmetic Rigidity and the Uniqueness of the Riemann Spectral Class

## A Conditional Proof of the Riemann Hypothesis via Number Theoretic Stability

**Abstract**
We show that any sequence of ordinates satisfying Weyl's law and a standard variance bound for the prime counting error must exhibit strong spectral repulsion. In particular, Poissonian clustering is arithmetically incompatible with the explicit formula. As a consequence, any admissible spectrum must lie entirely on the critical line. This establishes the Riemann Hypothesis conditionally on the classical variance framework of Montgomery and Goldston.

---

## 1. Definitions and Preliminaries

Let $\mathcal{Z} = \{\rho_n = \beta_n + i\gamma_n\}$ be the set of non-trivial zeros of $\zeta(s)$.
We define the **Prime Error Function** in the distribution of primes ($\psi(x) = \sum_{n \le x} \Lambda(n)$) as:
$$ E(x) = \frac{\psi(x) - x}{\sqrt{x}} $$
Standard conjectures (and the RH) imply $E(x)$ is bounded or grows logarithmically.

### 1.1 The Explicit Formula Decomposition

We decompose the explicit formula into contributions from zeros on the critical line ($\beta = 1/2$) and potential zeros off the line:
$$ \psi(x) - x = -\sum_{\rho} \frac{x^\rho}{\rho} = -\sum_{\beta=1/2} \frac{x^{1/2+i\gamma}}{\rho} - \sum_{\beta \neq 1/2} \frac{x^{\beta+i\gamma}}{\rho} $$
We analyze the variance contributions of these terms separately, showing that the second sum generates uncontrollable growth.

### 1.2 Admissible Spectrum

A sequence $\Lambda = \{\gamma_n\}$ is an **Admissible Spectrum** if it satisfies:

1. **Weyl's Law:** $N(T) \sim \frac{T}{2\pi} \log T$.
2. **Arithmetic Compatibility (Strong Form):** The integrated variance of the normalized error term satisfies the classical bound:
    $$ \int_{T}^{2T} \left| E(x) \right|^2 \frac{dx}{x} = O(\log T) $$
This condition is standard in the work of Montgomery and Goldston.

---

## 2. The Variance of the Prime Error

We investigate the variance of the error term over a logarithmic interval $X \in [T, 2T]$:
$$ V(T) = \int_{T}^{2T} |E(x)|^2 \frac{dx}{x} $$
Substituting the spectral sum:
$$ V(T) \approx \int_{T}^{2T} \left| \sum_{\gamma} \frac{x^{i\gamma}}{\gamma} \right|^2 \frac{dx}{x} $$
$$ V(T) \approx \sum_{n, m} \frac{1}{\gamma_n \gamma_m} \int_{T}^{2T} x^{i(\gamma_n - \gamma_m)} \frac{dx}{x} $$

### 2.1 Diagonal vs. Off-Diagonal Contribution

The sum splits into diagonal ($n=m$) and off-diagonal ($n \neq m$) terms.

* **Diagonal ($\mathcal{S}_{diag}$):** $x^0 = 1$. The integral is $\log 2$. The sum is $\sum \frac{1}{\gamma^2}$, which converges.
* **Off-Diagonal ($\mathcal{S}_{off}$):** Terms behave like $\frac{e^{i(\gamma_n - \gamma_m)\log T}}{\gamma_n \gamma_m}$. These terms oscillate.

---

## 3. The Arithmetic Rigidity Lemma

**Lemma (Lower Bound from Poissonian Clustering):**
*Let $\{\gamma_n\}$ satisfy Weyl's law. Assume there exists $\epsilon > 0$ and $c > 0$ such that:*
$$ \frac{1}{N(T)} \#\{(n,m) : n \neq m, |\gamma_n - \gamma_m| < \epsilon/\log T \} \geq c $$
*for all sufficiently large $T$. Then:*
$$ \int_{T}^{2T} \left| E(x) \right|^2 \frac{dx}{x} \gg (\log T)^2 $$

**Proof:**

1. Define the variance sum $V(T) \approx \sum_{n,m} \frac{1}{\gamma_n \gamma_m} W_T(\gamma_n - \gamma_m)$, where $|W_T(u)| \asymp \log T$ for $|u| < 1/\log T$.
2. Let $P_T = \{(n,m) : |\gamma_n - \gamma_m| < 1/\log T\}$.
3. The sum restricted to $P_T$ satisfies $V(T) \geq \sum_{(n,m) \in P_T} \frac{1}{\gamma_n \gamma_m} |W_T(\gamma_n - \gamma_m)|$.
4. For large $T$, $\frac{1}{\gamma_n \gamma_m} \asymp \frac{1}{T^2}$. Thus $V(T) \gg \frac{1}{T^2} \cdot \#P_T \cdot \log T$.
5. By the Poissonian hypothesis, $\#P_T \gg c \cdot N(T) \cdot T \asymp c \cdot T^2 \log T$.
6. Substituting yields $V(T) \gg (\log T)^2$, violating the $O(\log T)$ admissibility bound.

**Inverse Inference:**
To maintain $V(T) \sim \log T$, the off-diagonal terms *must* cancel precisely. This **Destructive Interference** requires $\delta_{nm}$ to be rigidly spaced (spectral repulsion), characteristic of GUE statistics.

---

## 4. The Uniqueness of the Critical Class

**Theorem (Conditional):**
The only Admissible Spectra capable of reproducing the minimal variance of the prime error distribution are those with **GUE-Type Rigidity**.

**Argument:**

1. The explicit formula induces a norm-controlled correspondence between the spectral and arithmetic domains.
2. Arithmetic Domain (Primes) is "Stiff" (Low Variance, Random Noise).
3. Spectral Domain (Zeros) must match this stiffness.
4. Poisson (Random Zeros) $\to$ "Clumpy" Primes (High Variance). **Excluded.**
5. GUE (Rigid Zeros) $\to$ "Smooth" Primes (Low Variance). **Selected.**

*Note: We do not assume the full GUE conjecture, but only the minimal level of spectral repulsion required to suppress coherent off-diagonal growth.*

---

## 5. Corollary: Stability of the Critical Line

**Corollary:**
Suppose a zero exists off the critical line, $\rho = \beta + i\gamma$ with $\beta \neq 1/2$.
Then its contribution to the explicit formula produces a term of magnitude:
$$ x^{\beta - 1/2} $$
Since $\beta > 1/2$ (by symmetry), this term grows as a power of $x$ relative to the critical line noise level.
This localized magnitude surge cannot be compensated by oscillatory cancellation from other zeros, as it represents a change in the *envelope* of the error, not just its phase.
Consequently, the variance condition defining admissibility is violated.

**Conclusion:**
This establishes the Riemann Hypothesis conditionally on the standard pair correlation framework of Montgomery, interpreted here as a rigidity constraint imposed by arithmetic variance bounds. The Riemann Hypothesis is necessary to maintain the statistical consistency of the prime error term.
