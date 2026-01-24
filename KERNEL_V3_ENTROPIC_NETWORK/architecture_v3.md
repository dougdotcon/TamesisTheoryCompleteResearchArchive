# KERNEL v3: ARCHITECTURE VISUALIZATION

This diagram represents the flow of information and entropy in the finalized Tamesis System (Kernel v3).

```mermaid
graph TD
    %% Define Styles
    classDef ont fill:#f9f,stroke:#333,stroke-width:2px;
    classDef dyn fill:#bbf,stroke:#333,stroke-width:2px;
    classDef funct fill:#bfb,stroke:#333,stroke-width:2px;
    classDef phys fill:#fbb,stroke:#333,stroke-width:2px;

    subgraph "I. ONTOLOGY (The Data)"
        Bit(Information Bits) --> Node(Entropic Node)
        Node --> Graph(Causal Graph)
        Graph -->|State Vectors| Tensor(Tensor Network)
    end
    class Bit,Node,Graph,Tensor ont;

    subgraph "II. DYNAMICS (The Engine)"
        Tensor -->|Update Rule| MaxEnt(Entropic Maximization)
        MaxEnt -->|Next Step| Unitarity{Unitary?}
        Unitarity -->|Yes| Quantum(Quantum Evolution)
        Unitarity -->|No| Collapse(Topological Collapse TDTR)
        Quantum --> NextState(State t+1)
        Collapse --> NextState
        NextState -->|Loop| Graph
    end
    class MaxEnt,Unitarity,Quantum,Collapse,NextState dyn;

    subgraph "III. THE FUNCTOR (The Bridge)"
        Graph -->|Coarse Graining| Metric(Emergent Metric g_uv)
        Metric -->|Limit| GR(General Relativity)
        Quantum -->|Limit| QFT(Quantum Field Theory)
        Graph -.->|Analytics| Vis(Module C: Visualization)
    end
    class Metric,GR,QFT,Vis funct;

    subgraph "IV. FUNCTIONALITY (Predictions)"
        Metric -->|Flat Rotation| a0(Stage 2: Galaxy Rotation)
        Metric -->|Refraction| Void(Stage 4: Void Lensing)
        Collapse -->|Mass Scale| Mc(Stage 1: Critical Mass)
        Metric -->|Expansion| H0(Stage 3: Hubble Tension)
        Vis -->|GIFs| a0
        Vis -->|GIFs| Void
    end
    class a0,Void,Mc,H0 phys;

    %% Connect Loops
    H0 -.->|Feedback| Bit
```

## Legend

1. **Ontology (Pink):** The raw data structure. No space, no time, only connected bits.
2. **Dynamics (Blue):** The computational rules. The "CPU" of the universe. Decides if a step preserves info (Quantum) or erases it (Gravity/Collapse).
3. **Functor (Green):** The translator. Converts digital graph data into smooth analog physics (Metric Tensor, Fields).
4. **Functionality (Red):** The observant phenomena. This is where we measure $a_0$, $M_c$, etc.
