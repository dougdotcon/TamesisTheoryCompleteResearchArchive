# Metrics of Hybrid Stability

We move beyond "User Satisfaction" to "System Physics".

---

## 1. Information-Theoretic Metrics

### 1.1 Entropy Reduction Rate ($\dot{S}$)

The rate at which the uncertainty about the document's validity decreases.
$$ \dot{S} = \frac{\Delta S_{Shannon}}{T_{task}} $$
*Goal:* Maximize $\dot{S}$.

### 1.2 Information Leakage ($L$)

The amount of false information (Noise) that passes through the filter and is accepted as truth by the Human.
$$ L = \sum_{i \in Errors} P(Accept|Error_i) $$
*Goal:* Minimize $L$ (ideally $L=0$).

## 2. Control-Theoretic Metrics

### 2.1 Stability Margin

The buffer between the current processing rate and the critical saturation point.
$$ M_{stable} = 1 - \frac{\Phi_{in}}{C_{max}} $$
If $M_{stable} < 0$, the system is thermally run-away (Panic/Giving up).

### 2.2 Rejection Ratio ($\rho$)

The ratio of machine output rejection.
$$ \rho = \frac{N_{rejected}}{N_{total}} $$
An optimal hybrid system should have a $\rho$ that matches the generator's intrinsic error rate $\epsilon_M$.

- $\rho \ll \epsilon_M$: Under-filtering (Gullibility).
- $\rho \gg \epsilon_M$: Over-filtering (Paranoia/Inefficiency).

## 3. Thermodynamic Metrics

### 3.1 Cognitive Cost ($E_{cog}$)

Measured via proxy (Task Time $\times$ Cognitive Load Index) or direct physiological measures (Pupillometry).

### 3.2 Efficiency ($\eta$)

$$ \eta = \frac{\text{Correct Logic Gates}}{E_{cog} + E_{compute}} $$
A hybrid system is justifiable only if $\eta_{hybrid} > \eta_{human}$.
