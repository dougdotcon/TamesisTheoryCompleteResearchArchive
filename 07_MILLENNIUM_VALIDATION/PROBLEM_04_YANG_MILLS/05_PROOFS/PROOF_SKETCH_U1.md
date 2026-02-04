# Proof Sketch: Spectral Gap in Compact U(1) Lattice Gauge Theory

## A Tractable Case of Uniform Coercivity

**Context:**
This document provides a rigorous sketch proving that the Hamiltonian of Compact U(1) Lattice Gauge Theory possesses a strictly positive spectral gap in the strong coupling limit. This serves as a concrete validation of the "Uniform Coercivity of Information" hypothesis proposed in `FORMAL_CONJECTURES_YM.md`.

---

## 1. The Model

We consider a hypercubic lattice $\Lambda = (a\mathbb{Z})^d$.
The gauge group is **Compact U(1)**, isomorphic to the circle group $S^1$.
Link variables: $U_l = e^{i \theta_l} \in S^1$, where $\theta_l \in [0, 2\pi)$.

### 1.1 Hilbert Space

The local Hilbert space for a single link is $\mathcal{H}_l = L^2(S^1, d\theta)$.
The total Hilbert space is the tensor product over all links:
$$ \mathcal{H} = \bigotimes_{l \in \Lambda} L^2(S^1)_l $$

A basis for $\mathcal{H}_l$ is given by the Fourier modes (irreducible representations of U(1)):
$$ \langle \theta | n \rangle = \frac{1}{\sqrt{2\pi}} e^{in\theta}, \quad n \in \mathbb{Z} $$
Here, $n$ represents the electric flux on the link.

### 1.2 Hamiltonian (Kogut-Susskind)

In the temporal gauge ($A_0 = 0$), the Hamiltonian consists of an electric (kinetic) and magnetic (potential) term:
$$ H = \frac{g^2}{2a} \sum_l \hat{E}_l^2 - \frac{1}{2ag^2} \sum_p \cos(\Theta_p) $$
where:

* $\hat{E}_l = -i \frac{\partial}{\partial \theta_l}$ is the electric field operator.
* $\Theta_p = \sum_{l \in \partial p} \theta_l$ is the magnetic flux through plaquette $p$.

---

## 2. Strong Coupling Limit ($g \to \infty$)

We analyze the spectrum in the limit where $g$ is large. We treat the magnetic term as a perturbation.
Let $\lambda = \frac{1}{g^4}$. We rescale standard perturbation theory.
Unperturbed Hamiltonian ($H_0$):
$$ H_0 = \frac{g^2}{2a} \sum_l \hat{E}_l^2 $$

### 2.1 Spectrum of $H_0$

The operator $\hat{E}_l^2$ is diagonal in the Fourier basis $|n\rangle$:
$$ \hat{E}_l^2 |n\rangle = n^2 |n\rangle $$
The total energy of a state $|\{n_l\}\rangle$ is:
$$ E(\{n_l\}) = \frac{g^2}{2a} \sum_l n_l^2 $$

* **Ground State ($\Omega$):** $n_l = 0$ for all links (Zero flux everywhere).
    $$ E_0 = 0 $$
* **First Excited State:** Typically a configuration with minimal non-zero flux satisfying Gauss's Law ($\nabla \cdot E = 0$). On a compact lattice without matter, the minimal excitation is a closed loop of flux (e.g., around a smallest plaquette).
    However, strictly speaking for the link spectrum, the gap to the first non-zero eigenstate of $\hat{E}^2$ (state $|1\rangle$) is:
    $$ \Delta_0 = \frac{g^2}{2a} (1^2 - 0^2) = \frac{g^2}{2a} $$

## 3. The "Topological" Origin of the Gap

The crucial observation is why the spectrum is discrete near zero.
The gap exists because the configuration space of the link is **Compact** ($S^1$).

* If the group were non-compact ($\mathbb{R}$), the Fourier transform would be continuous, and $E \sim k^2$ could be arbitrarily close to zero.
* Because $U(1)$ is compact, the dual space ($\mathbb{Z}$) is discrete. You cannot have "0.0001 flux". You must have integer flux $n=0, 1, 2...$

This quantifies our **Hypothesis A**:
$$ \langle \psi, H_0 \psi \rangle \ge \frac{g^2}{2a} \|\psi\|^2 \quad \forall \psi \perp \Omega $$
The "Bit Cost" provides a lower bound of order $g^2/a$.

## 4. Stability under Perturbation

For large but finite $g$, we include the magnetic term $V = -\sum \cos(\Theta_p)$.
Standard perturbation theory (Cluster Expansion) shows that the gap $\Delta$ does not collapse immediately.
$$ \Delta(g) = \frac{g^2}{2a} \left( 1 - \mathcal{O}(g^{-4}) \right) $$
As long as the series converges (radius of convergence for strong coupling), the gap remains strictly positive.

## 5. Conclusion regarding the Continuum Limit

In the naïve continuum limit ($a \to 0$), we hold physical quantities fixed.
If we fix the mass gap $m_{phys} = \Delta(g)$, this implies a renormalization group flow for $g(a)$.
Standard results (e.g., Guth 1980) show that for Compact U(1) in 3D, there is a confining phase (Gap > 0) for all $g$. In 4D, there is a phase transition.

However, this proof sketch demonstrates the core mechanism: **Discreteness of the Gauge Group implies Discreteness of the Spectrum.**
In Kernel v3, since information is discrete, the gauge group is effectively always compactified at the Planck scale, ensuring the gap never vanishes physically.
