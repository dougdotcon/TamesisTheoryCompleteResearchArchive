# IMPLEMENTATION PLAN: Experiment 04 - The Holographic Bounce Buffer

**Goal:** Demonstrate the "Big Bounce" principle as a software resilience pattern.
**Principle:** "When Information Density hits the Bekenstein Bound, Space Repels Energy."

## 1. The Engineering Challenge (DDoS Simulation)

We simulate a server receiving requests at a rate $R_{in}$ much higher than its processing rate $R_{proc}$.

* **Standard Server (FIFO):** Buffer fills up. New requests are dropped (Packet Loss = 100% of excess). System crashes or halts.
* **Tamesis Serve (Elastic):** As Buffer Fill $F \to 1.0$, the "Entropic Pressure" rises.
  * Instead of dropping new packets, we **compress old packets** (lossy holographic projection) to make space.
  * We trade **Resolution** for **Liveness**.

## 2. Technical Implementation (`exp_04_big_bounce_buffer.py`)

1. **Classes:**
    * `Request`: Has `payload` (data) and `resolution` (1.0 = Full, 0.1 = Thumbnail).
    * `Server`: Has `buffer` (max capacity in bytes).
2. **The Bounce Mechanism:**
    * On `enqueue(req)`:
        * If `buffer_size + req.size > capacity`:
            * Calculate Pressure $P = \frac{1}{capacity - size}$.
            * **Compress:** Select oldest items in buffer and degrade their resolution (hashing/summarizing) until space is freed.
            * Accept new request.
3. **Metrics:**
    * **Survival Time:** How long until total lockup?
    * **Data Retained:** What % of total history is preserved?

## 3. Success Condition

* The Standard Server will have a "Cliff Edge" failure profile.
* The Tamesis Server will show a "graceful degradation" curve, maintaining 100% uptime by sacrificing precision.
* This proves that **Entropic Elasticity (Gravity)** is a superior stability mechanism to rigid exclusion (Pauli).
