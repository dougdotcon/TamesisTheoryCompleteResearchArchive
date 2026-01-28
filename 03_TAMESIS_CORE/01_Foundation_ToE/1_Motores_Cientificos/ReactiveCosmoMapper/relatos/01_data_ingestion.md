# Report 01: Baryonic Data Ingestion

**Date:** 12/29/2025
**Module:** `src/data_ingestor.py`, `src/sparc_ingestor.py`

## Objective
To establish a robust data pipeline to feed the `ReactiveCosmoMapper` with real observational data, avoiding catalogs pre-processed with Dark Matter models.

## Implemented Strategy

### 1. SPARC (Spitzer Photometry & Accurate Rotation Curves)
- **Challenge:** Direct download from the Case Western server failed due to network/firewall restrictions.
- **Workaround:** Implementation of initial `Mock Data` for concept validation, containing key galaxies (NGC0024, NGC1560, NGC6503).
- **Definitive Solution:** Creation of `SPARCIngestor` capable of converting raw Luminosity (3.6 micron bands) into Total Baryonic Mass ($M_{bar} = M_{star} + M_{gas}$), utilizing the Mass-Luminosity relation ($\Upsilon_{disk} = 0.5, \Upsilon_{bulge} = 0.7$).

### 2. SDSS (Sloan Digital Sky Survey)
- **Challenge:** Massive ingestion of 50,000 galaxies for cosmological mapping.
- **Initial Implementation:** Sequential query via `astroquery` (limited to small samples).
- **Big Data Optimization:**
    - Implementation of **parallel ingestion** (`Multi-threading`).
    - **Sky Partitioning Strategy (RA Partitioning)**: Division of the 360 degrees of Right Ascension into *slices* processed concurrently.
    - Result: Successful download of 50,000 galaxies with Redshift $z > 0.01$ in < 1 minute.

## Results
- Generated file: `data/sparc_master.csv` (Mock/Structural).
- Generated file: `data/sdss_sample.csv` (50,000 records, ~2.5 MB).
- **Status:** Operational and scalable pipeline.
