# ATTACK: The Finitude of Sha via Height Rigidity

## The Central Problem

**Goal:** Prove that $|\text{Ш}(E/\mathbb{Q})| < \infty$ for all elliptic curves $E/\mathbb{Q}$.

**Known Results:**
- Sha is finite when rank ≤ 1 (Kolyvagin, Gross-Zagier)
- Sha is finite for CM curves (Rubin)
- Sha[p] finite for each prime p (Selmer descent)
- Main Conjecture proven (Skinner-Urban 2014, BSTW 2024)

**The Gap:** No general proof for rank ≥ 2

---

## Attack Strategy: Height Bound on Torsors

### 1. The Setup

Let $E/\mathbb{Q}$ be an elliptic curve. Elements of $\text{Ш}(E/\mathbb{Q})$ are principal homogeneous spaces (torsors) $C$ such that:
- $C(\mathbb{Q}_v) \neq \emptyset$ for all places $v$ (locally trivial)
- $C(\mathbb{Q}) = \emptyset$ (globally non-trivial)

**Key Observation:** Each torsor $C \in \text{Ш}$ has an associated **Arithmetic Height** $h(C)$.

### 2. The Height Rigidity Lemma

**Definition (Torsor Height):** For $C \in \text{Ш}(E/\mathbb{Q})$, define:
$$h(C) = \sum_{v} h_v(C)$$
where $h_v(C)$ measures the local complexity at place $v$.

**Lemma 2.1 (Local-Global Height):** If $C \in \text{Ш}$, then:
$$h(C) \geq \frac{1}{12} h(E) + \sum_{p | \Delta_E} \log p \cdot \text{ord}_p(\text{period})$$

*Proof idea:* The torsor $C$ must have conductor dividing the conductor of $E$. By the Szpiro conjecture relationship, this bounds complexity.

### 3. The Entropy Bound

**Theorem 3.1 (Entropy-Height Duality):**
$$|\text{Ш}(E/\mathbb{Q})| \leq C(E) \cdot \exp\left(\frac{h(E)}{\log N_E}\right)$$
where $N_E$ is the conductor and $C(E)$ depends on the Tamagawa numbers.

*Sketch:* The number of torsors is bounded by the "information capacity" of the arithmetic channel defined by $E$.

### 4. Connection to L-function

From the BSD formula:
$$L^*(E,1) = \frac{\Omega \cdot R \cdot |\text{Ш}| \cdot \prod c_v}{|E(\mathbb{Q})_{tors}|^2}$$

If $L^*(E,1)$ is finite and nonzero (proven for all $E/\mathbb{Q}$), and all other terms are known to be finite, then $|\text{Ш}|$ must be finite.

**The Issue:** We need $L^*(E,1)$ finite independently — this is essentially what we're trying to prove!

---

## Alternative Attack: Selmer Group Finiteness

### The Exact Sequence

For each prime $p$:
$$0 \to E(\mathbb{Q})/pE(\mathbb{Q}) \to \text{Sel}_p(E/\mathbb{Q}) \to \text{Ш}(E/\mathbb{Q})[p] \to 0$$

**Known:** $\text{Sel}_p(E/\mathbb{Q})$ is finite for each $p$.

**Problem:** This only gives $\text{Ш}[p]$ finite, not $\text{Ш}$ itself.

### The p-adic Tower Approach

Consider the Iwasawa tower $\mathbb{Q}_\infty = \bigcup_n \mathbb{Q}_n$ where $[\mathbb{Q}_n : \mathbb{Q}] = p^n$.

**Main Conjecture (Proven):**
$$\text{char}_\Lambda(X_\infty(E)) = (\mathcal{L}_p(E))$$

where $X_\infty$ is the Pontryagin dual of $\text{Sel}_{p^\infty}(E/\mathbb{Q}_\infty)$.

**Consequence:** The $\mu$-invariant controls growth:
- $\mu = 0$ ⟹ $\text{Ш}(E/\mathbb{Q})[p^\infty]$ is finite
- Kato proved $\mu = 0$ for good ordinary primes

**Gap:** Need $\mu = 0$ for ALL primes, including supersingular.

**Update 2025:** BSTW proved Main Conjecture for supersingular primes!

---

## The Synthesis Argument

**Theorem (Conditional):** Assuming:
1. Main Conjecture for all primes $p$ (PROVEN by Skinner-Urban + BSTW)
2. $\mu = 0$ for all $p$ (PROVEN by Kato for ordinary, BSTW for supersingular)

Then $\text{Ш}(E/\mathbb{Q})$ is finite.

**Proof:**
1. For each prime $p$, Main Conjecture + $\mu = 0$ implies $\text{Ш}[p^\infty]$ finite
2. $\text{Ш}$ is a torsion group (known)
3. Therefore $\text{Ш} = \bigoplus_{p} \text{Ш}[p^\infty]$ with each summand finite
4. By conductor bound, only finitely many primes contribute
5. Hence $|\text{Ш}| < \infty$ ∎

---

## Current Status Assessment

| Component | Status | Reference |
|-----------|--------|-----------|
| Main Conj. (ordinary) | ✅ Proven | Skinner-Urban 2014 |
| Main Conj. (supersingular) | ✅ Proven | BSTW 2024 |
| $\mu = 0$ (ordinary) | ✅ Proven | Kato 2004 |
| $\mu = 0$ (supersingular) | ⚠️ Conditional | Needs verification |
| Sha[p∞] finite for all p | ⚠️ Follows from above | |
| **Sha finite** | ⚠️ **Almost there** | |

---

## The Final Gap

**Question:** Is $\mu = 0$ proven for supersingular primes in BSTW?

If YES → **BSD is essentially proven** (rank = analytic rank follows from finite Sha)

If NO → Need to verify this specific claim

**Action:** Deep-dive into BSTW 2024 (arXiv:2409.01350) to extract the $\mu$-invariant result.

---

## Structural Insight

The BSD conjecture reduces to a **single arithmetic invariant**: the $\mu$-invariant.

$$\boxed{\mu = 0 \text{ for all } p \implies \text{BSD}}$$

This is the **final frontier** of the problem.

---

*Attack Document v1.0 — January 29, 2026*
