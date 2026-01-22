# Relatório 01: Ingestão de Dados Bariônicos

**Data:** 29/12/2025
**Módulo:** `src/data_ingestor.py`, `src/sparc_ingestor.py`

## Objetivo
Estabelecer um pipeline de dados robusto para alimentar o `ReactiveCosmoMapper` com dados observacionais reais, evitando dados pré-processados por modelos de Matéria Escura.

## Estratégia Implementada

### 1. SPARC (Spitzer Photometry & Accurate Rotation Curves)
- **Desafio:** O download direto do servidor da Case Western falhou devido a restrições de rede/firewall.
- **Solução de Contorno:** Implementação de um `Mock Data` inicial para validação de conceito, contendo galáxias chave (NGC0024, NGC1560, NGC6503).
- **Solução Definitiva:** Criação do `SPARCIngestor` capaz de converter dados brutos de Luminosidade (Bandas 3.6 microns) em Massa Bariônica Total ($M_{bar} = M_{star} + M_{gas}$), utilizando a relação Massa-Luminosidade ($\Upsilon_{disk} = 0.5, \Upsilon_{bulge} = 0.7$).

### 2. SDSS (Sloan Digital Sky Survey)
- **Desafio:** Ingestão massiva de 50.000 galáxias para mapeamento cosmológico.
- **Implementação Inicial:** Consulta sequencial via `astroquery` (limitada a pequenas amostras).
- **Otimização Big Data:**
    - Implementação de **ingestão paralela** (`Multi-threading`).
    - Estratégia de **Particionamento de Céu (RA Partitioning)**: Divisão dos 360 graus de Ascensão Reta em *slices* processados concorrentemente.
    - Resultado: Download bem-sucedido de 50.000 galáxias com Redshift $z > 0.01$ em < 1 minuto.

## Resultados
- Arquivo gerado: `data/sparc_master.csv` (Mock/Estrutural).
- Arquivo gerado: `data/sdss_sample.csv` (50.000 registros, ~2.5 MB).
- **Status:** Pipeline operacional e escalável.
