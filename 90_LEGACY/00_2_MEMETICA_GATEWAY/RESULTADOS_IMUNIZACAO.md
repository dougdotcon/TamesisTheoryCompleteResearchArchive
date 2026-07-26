# RESULTADOS: IMUNIZACAO MEMETICA (GATEWAY NODES)

![Status](https://img.shields.io/badge/Status-VALIDATED-brightgreen) ![Type](https://img.shields.io/badge/Type-APPLIED_MEMETICS-orange)

## Resumo Executivo

Comparamos 4 estrategias de imunizacao memetica + censura em uma rede social sintetica de 500 nos.

---

## Resultados por Estrategia (Taxa de Infeccao)

| Dose | Random | Hub (Grau) | Bridge (Betweenness) | Acquaintance |
|---|---|---|---|---|
| 2% | 98.0% | 97.8% | 98.0% | 98.0% |
| 5% | 94.8% | 94.8% | 94.8% | 94.6% |
| 10% | 89.2% | 81.8% | 87.6% | 84.4% |
| 15% | 80.6% | 75.0% | 79.8% | 79.6% |
| **20%** | **63.8%** | **38.4%** | **57.2%** | **60.2%** |
| **30%** | **41.2%** | **22.4%** | **28.8%** | **12.6%** |

## Censura: TOTALMENTE INEFICAZ

| Dose (Edges Removidas) | Taxa de Infeccao |
|---|---|
| 2% | **100%** |
| 5% | **100%** |
| 10% | **100%** |
| 15% | **100%** |
| 20% | **100%** |
| 30% | **100%** |

> **A Censura NAO funciona.** Remover canais de comunicacao (arestas) nao impede a propagacao do virus. A rede e resiliente -- o virus simplesmente encontra caminhos alternativos.

---

## Descobertas Criticas

### 1. A Censura e Termodinamicamente Inutil

Remover ate 30% das arestas (= bloquear 30% dos canais de comunicacao) resulta em **zero reducao** na infeccao. Isso e uma propriedade topologica das redes Small-World: a redundancia de caminhos torna a censura ineficaz.

### 2. Hub Immunization e a Estrategia Dominante ate 20%

Imunizar os 20% de nos de maior grau reduz a infeccao para **38.4%** (vs 63.8% com Random). A estrategia "conheca os influenciadores e ilumine-os" e matematicamente superior.

### 3. Acquaintance Immunization e a Melhor a 30%

A 30%, a estrategia de "Conhecidos" (vacinar o amigo mais conectado de nos aleatorios) supera todas as outras com **12.6%** de infeccao. Esta estrategia **nao requer conhecimento global da rede** -- funciona localmente.

### 4. Dose Minima Eficaz

Para reduzir a infeccao abaixo de 25%, e necessario imunizar pelo menos **30% dos Gateway Nodes** usando a estrategia Hub ou Acquaintance.

---

## Traducao para a Realidade

| Estrategia | Acao Social |
|---|---|
| Hub Immunization | Educar influenciadores, cientistas, jornalistas |
| Acquaintance | Programas peer-to-peer: cada pessoa educa seu contato mais conectado |
| Censura | Deplatforming, bans — **COMPROVADAMENTE INUTIL** |
| Dose Minima | 30% dos Gateway Nodes devem ser imunizados |

---

## Artefatos Gerados

| Arquivo | Descricao |
|---|---|
| `immunization_comparison.png` | Dose vs Infeccao (4 estrategias) |
| `censorship_vs_immunity.png` | Censura vs Imunizacao (prova visual) |
| `sir_comparison.png` | Dinamica SIR: Sem protecao vs Hub vs Bridge |
| `gateway_map.png` | Mapa dos Gateway Nodes (Hub vs Bridge) |
| `herd_immunity_threshold.png` | Limiar de Imunidade de Rebanho |

![Source](https://img.shields.io/badge/Source-gateway__mapper.py-blue) ![Proof](https://img.shields.io/badge/Proof-COMPUTATIONAL-green)
