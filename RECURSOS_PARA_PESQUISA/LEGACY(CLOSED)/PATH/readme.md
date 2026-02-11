# Intellectual Mining Engine

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Prototype-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

## Project Overview

The **Intellectual Mining Engine** ("Patent Miner") is an automated system designed to identify, analyze, and capitalize on undervalued intellectual property assets. Specifically, it targets expired patents that were previously unviable due to technical, cost, or regulatory barriers but have become feasible with modern technology (AI, new materials, automation).

**Core Objective**: To transform dormant intellectual assets into actionable business opportunities by applying a rigorous "Viability Formula".

---

## Development Status

### Completed

- [x] **Project Scaffolding**: Established directory structure and dependencies.
- [x] **Core Engine**: Implemented `patent_miner.py` CLI structure.
- [x] **Ingestion Module**: Mocked scraper for fetching patent data.
- [x] **AI Analysis Module**: Integrated LLM logic for viability assessment.
- [x] **Scoring System**: Implemented formula: `Score = (Potential * 2) + (Cost_Barrier * 2) + (Reg_Barrier * 3)`.
- [x] **Verification**: Validated prototype with dry-run tests.

### Roadmap

- [ ] **Live API Integration**: Replace mock LLM with OpenRouter/OpenAI API.
- [ ] **Data Pipeline**: Implement real scraping for Google Patents/USPTO.
- [ ] **Database**: Migrate from CSV to SQLite/PostgreSQL for scale.
- [ ] **Web Interface**: Develop Dashboard (Streamlit/React) for asset visualization.

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Installation

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

The miner supports three operational modes:

**1. Mock Mode (Instant Demo)**

```bash
python patent_miner.py --query "autonomous energy" --limit 5
```

**2. Real Data Mode (Hugging Face)**

```bash
python patent_miner.py --source hf --limit 5
```

**3. Full AI Mode (Real Data + Real Analysis)**

```bash
python patent_miner.py --source hf --limit 3 --apikey YOUR_OPENROUTER_KEY
```

The tool will:

1. Search for expired patents matching the query.
2. Analyze technical feasibility using AI.
3. Calculate a "Viability Score".
4. Output a ranked CSV file (`patent_mining_results.csv`).

---

## Theoretical Framework

### 1. The Core Hypothesis

The central premise is to "transform what is dead into something profitable." This distinction separates true market creators from mere executors. The key insight is not the resource itself, but the cognitive and institutional blocks preventing its exploration.

Common barriers include:

- Decisions made with outdated data.
- Lack of political incentives.
- Regulatory fear.
- High initial cost vs. long-term return.

### 2. Historical Context: The Rose Island

The case of Giorgio Rosa (Rose Island) demonstrates:

- The State decides based on precedent, not imagination.
- Innovation appearing outside standard models is viewed as a threat.
- True innovation often arises in legal gray zones.

The relevance to this project: **"Something was judged unviable, but no one revisited the premise."**

### 3. Validated Examples

- **Israel (Negev Desert)**: From "unproductive" to agritech exporter.
- **Chernobyl**: From dead zone to biodiversity lab and energy hub.
- **Shenzhen**: From ignored territory to Special Economic Zone.

### 4. Opportunity Clusters

We identify three primary forms of arbitrage:

#### A. Temporal Arbitrage

Exploiting the gap between when a technology becomes possible and when the system accepts it.

#### B. Cognitive Arbitrage

Gaining value by questioning accepted premises and re-reading old decisions with new data.

#### C. Institutional Arbitrage

Creating value where laws are outdated or regulations are lagging.

### 5. Implementation Strategy

This project operationalizes the theory via a 5-step pipeline:

1. **Source**: Public patent databases (Google Patents, USPTO).
2. **Filter**: Hard filters for status (Expired) and Date (<2005).
3. **enrich**: Extract full technical text.
4. **Analyze**: AI assessment of current viability.
5. **Score**: Prioritization based on the Viability Formula.

### 6. Target Sectors (2025-2035)

- **Energy**: Modular Nuclear (SMR), Waste-to-Energy.
- **Health**: Industrial Cannabis, Gene Therapy.
- **Infrastructure**: Drones, Autonomous Systems.
- **State/Finance**: CBDCs, Digital Identity.

---

*This project represents "Opportunity Engineering" — generating value before the market perceives it.*
