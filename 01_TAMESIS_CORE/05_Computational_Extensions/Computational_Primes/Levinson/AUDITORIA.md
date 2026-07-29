# Auditoria rigorosa — Computational Levinson Test

Data: 2026-07-29  
Status: verificação numérica de modelo discreto.

## Achados

O princípio de Levinson possui versões contínuas e discretas, mas o número de estados ligados e o winding dependem de convenções de fase, canais e condições de fronteira. Uma única rede defeituosa não estabelece robustez topológica geral.

## Teste mínimo

Disponibilizar `computational_levinson.py`, especificar todos os parâmetros, testar redes analiticamente solucionáveis, variar tamanho e defeito, e reportar erro de discretização e casos de limiar/ressonância.

## Fonte

- Kellendonk, Richard & Schulz-Baldes, *On the wave operators and Levinson's theorem for lattices*, DOI [10.1007/s00220-002-0724-3](https://doi.org/10.1007/s00220-002-0724-3).
