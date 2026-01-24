# Implementation Plan: Origins (Topological Spin)

## Goal

To demonstrate that Spin-1/2 statistics ($\psi \xrightarrow{360^\circ} -\psi$, $\psi \xrightarrow{720^\circ} +\psi$) are a necessary consequence of a particle having a **Genus-1 (Toroidal) Topology**, supporting the TARDIS hypothesis that fermions are micro-wormholes.

## User Review Required
>
> [!NOTE]
> **Visualization Choice:** We will simulate the **"Dirac Belt Trick"** (or Plate Trick). This is the standard topological proof that a tethered object requires 720 degrees of rotation to untangle. We will map this explicitly to the topology of a wormhole mouth.

## Proposed Changes

### 1. `limits/origins/simulation/`

#### [NEW] `spinor_visualizer.py`

- **Function:** Generate a 3D animation of a "tethered" object rotating.
- **Physics:**
  - Represent the particle as a core (wormhole mouth).
  - Represent the "electric flux lines" as ribbons/belts connecting to infinity.
  - Show that a $360^\circ$ rotation twists the ribbons (state $-1$).
  - Show that a $720^\circ$ rotation allows the ribbons to pass through each other and untangle (state $+1$).
- **Output:** `spinor_rotation.mp4` (or GIF) and `topology_comparison.png`.

### 2. `limits/origins/topology/`

#### [NEW] `wormhole_geometry.py`

- **Function:** Plot the Penrose diagram or embedding diagram of a Genus-1 Wormhole (Torus).
- **Goal:** Visually contrast a Genus-0 (Sphere/Scalar) vs Genus-1 (Torus/Spinor).

## Verification Plan

### Automated

- Run `spinor_visualizer.py`.
- Check if the "Tangle Index" returns to 0 after 720 degrees.
- Verify it remains non-zero after 360 degrees.

### Manual Verification

- Watch the animation.
- Confirm the visual analogy clearly explains "Why 720 degrees?".
