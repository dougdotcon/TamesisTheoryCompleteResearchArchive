# Auditoria — Candidato U₂ / dinâmica de Lindblad

**Status:** needs_data  
**Nível global:** H1/S1 — base matemática estabelecida; interpretação holográfica ainda especulativa

## Pergunta auditável

É possível derivar os coeficientes de dissipação `γ_k` de uma geometria ou fator de forma espectral, preservando complete positivity, trace preservation e previsões distintas do modelo Lindblad fenomenológico?

## Correções aplicadas

- Separada a equação de Lindblad, que é padrão, da interpretação Tamesis de defeitos topológicos e bulk holográfico.
- Removidas afirmações de recuperação automática de unitariedade.
- Especificado que a extensão precisa de um mapa entre geometria, fator espectral e `γ_k`.
- Adicionada a referência DOI original de Lindblad.

## Lacunas

1. Não existe derivação apresentada para `γ_k` a partir do spectral form factor.
2. “Defeito topológico” e “horizonte” não têm definição matemática no artigo.
3. Não há benchmark contra modelos de banho, ruído ou equações mestras microscópicas.
4. A preservação da unitariedade global não é demonstrada pela dinâmica reduzida.

## Próximo teste

Escolher um modelo microscópico com ambiente, derivar a dinâmica reduzida e comparar os `γ_k` previstos pela hipótese geométrica com a estimação direta. Verificar complete positivity, conservação de traço, escalas temporais e uma assinatura espectral fora da amostra.

## Fontes verificadas

- Lindblad (1976), [geradores de semigrupos quânticos](https://doi.org/10.1007/BF01608499).
- Breuer & Petruccione, *The Theory of Open Quantum Systems*.
- Bousso (2002), [revisão do princípio holográfico](https://doi.org/10.1103/RevModPhys.74.825).
