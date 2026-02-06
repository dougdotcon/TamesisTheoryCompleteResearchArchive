# Relatório 03: Visualização Cosmológica 3D

**Data:** 29/12/2025
**Módulo:** `src/visualizer.py`, `src/solidify_universe.py`

## Objetivo
Mapear a estrutura em grande escala do universo ("Teia Cósmica") sob a ótica da Gravidade Reativa, transformando dados brutos de Redshift em uma geometria 3D navegável.

## Tecnologia de Visualização
1. **Conversão de Coordenadas:**
    - Transformação de coordenadas esféricas (RA, Dec, Redshift) para Cartesianas (X, Y, Z em Mpc).
    - Uso da Lei de Hubble e métricas cosmológicas (`astropy.cosmology`) para distâncias precisas.

2. **Geração de Malha (Mesh Generation):**
    - Exportação para formato **Wavefront OBJ** (padrão industrial).
    - **Algoritmo de Filamentos:** Uso de `KDTree` (scipy) para conectar galáxias vizinhas (distância $< 10$ Mpc), revelando a topologia da rede cósmica.

3. **Solidificação (Solução de Renderização):**
    - Problema Identificado: Visualizadores padrão (Windows 3D Viewer) não renderizam nuvens de pontos (v) nativamente.
    - Solução: Script `solidify_universe.py` que transmuta cada vértice (ponto) em um **Cubo** geométrico (8 vértices, 6 faces).
    - Escala: Cubos de 15 Mpc para visibilidade em escala macro.

## Resultados Big Data
- Ingestão: 50.000 Galáxias processadas.
- **Arquivo Final:** `reactive_universe_solid.obj` (~27 MB).
- **Estatísticas da Teia:**
    - Vértices: 50.000 galáxias.
    - Arestas (Túneis/Filamentos): 358.923 conexões.
- **Análise Visual:** A renderização revela aglomerados densos e grandes vazios cósmicos (*voids*), compatíveis com a estrutura filamentar esperada onde a gravidade entrópica atua com maior intensidade (regiões de baixa aceleração).
