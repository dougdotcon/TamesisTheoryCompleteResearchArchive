# Notas do debunker convencional (Descoberta adversarial de nulos, item 5 de `METHODOLOGY_EXTENSIONS.md`)

**Papel:** não reexecutar a análise (já reproduzida por dois agentes) — tentar
explicar `DISC-CLAIM-002` sem nenhum ingrediente Tamesis, usando qualquer
mecanismo convencional. Cálculos abaixo usam exclusivamente as 120 galáxias
de `discovery_galaxies` em `data/discovery_holdout_split.json` (holdout de
55 galáxias não tocado). Script de referência:
`/tmp/.../scratchpad/adversary_analysis.py` (não commitado — reprodutível a
partir deste texto).

## 1. Largura do IC vs. prior a priori razoável

Recálculo independente (código próprio, não copiado dos scripts primário/
adversarial) reproduz o ajuste: `g†=1.1977e-10`, IC bootstrap 95%
(1000 réplicas, seed própria) = `[6.83e-11, 2.68e-10]` — consistente com
`result_primary.json` (`[6.76e-11, 2.78e-10]`) e `result_adversarial.json`
(`[6.87e-11, 2.63e-10]`) a menos de ~5% de diferença entre implementações
independentes.

Fração de um prior log-uniforme sobre `a0` que cairia dentro do IC de 95%
publicado (`result_primary.json`) **apenas por acaso**, para diferentes
faixas "razoáveis" de escala de aceleração:

| Faixa do prior (log-uniforme) | Fração dentro do IC |
|---|---|
| 1e-11 a 1e-8 m/s² (3 décadas) | 20.4% |
| 1e-11 a 1e-9 m/s² (2 décadas) | 30.7% |
| 1e-12 a 1e-8 m/s² (4 décadas) | 15.3% |

**Interpretação:** o IC não é um artefato tão largo que "qualquer coisa
sobrevive" — mesmo na faixa mais generosa, ~70-85% de um prior log-uniforme
razoável seria excluído. Mas também não é estreito: ~1 em cada 3 a 5
valores candidatos de `a0` tirados ao acaso de um prior razoável cairia
dentro do IC apenas por largura estatística, sem nenhuma relação com a
física do candidato. H_A sobreviver é evidência real, mas fraca — da ordem
de um fator de 3-5x de poder discriminativo, não uma rejeição decisiva de
alternativas genéricas.

## 2. Sensibilidade a sistemáticas conhecidas do SPARC

Recálculo restrito a subconjuntos da amostra de descoberta (120 galáxias):

| Subconjunto | N galáxias | g† | razão vs. amostra completa |
|---|---|---|---|
| Completa | 120 | 1.1977e-10 | 1.000 |
| Q=1 (melhor qualidade) apenas | 69 | 1.1952e-10 | 0.998 |
| Q=2,3 apenas | 51 | 1.2081e-10 | 1.009 |
| Excluindo Inc<30° | 111 | 1.1848e-10 | 0.989 |

IC bootstrap para Q=1 apenas: `[6.47e-11, 2.62e-10]` — H_A ainda dentro,
H_B ainda fora. Nenhum corte por qualidade ou inclinação desloca `g†` por
mais de ~1.1%.

**Erro de distância:** erro fracionário mediano de distância na amostra de
descoberta é ~13.9% (mediano), ~15.9% (média), lido diretamente de `e_D/D`
no catálogo `.mrt`. Perturbação Monte Carlo (200 réplicas) com erro de
distância *independente por galáxia* (não correlacionado) desloca `g†`
médio para 1.29e-10 (ruído em grande parte cancela ao poolar 120 galáxias
independentes) — ainda a >5x de distância de `a0_B`.

Teste de pior caso: um viés sistemático **coerente** (toda a escala de
distância do catálogo deslocada na mesma direção simultaneamente — cenário
implausível dado que o catálogo mistura vários métodos de distância
independentes, TRGB/Cepheids/Hubble-flow/SNe) de até 30%:

| Fator de escala de distância aplicado a TODAS as galáxias | g† resultante | razão vs. a0_B |
|---|---|---|
| 0.80 (distâncias 20% menores) | 1.497e-10 | 0.220 |
| 1.00 (real) | 1.198e-10 | 0.176 |
| 1.30 (distâncias 30% maiores) | 0.921e-10 | 0.135 |

Para o ponto central alcançar `a0_B` (6.80e-10) seria necessário um erro de
escala de distância coerente de fator ~5.7x em todo o catálogo — muito além
de qualquer sistemática plausível documentada para SPARC (~10-20%,
Lelli/McGaugh/Schombert 2016).

**Conclusão do item 2:** nenhuma sistemática convencional testada (Q flag,
inclinação, erro de distância aleatório ou sistemático coerente até 30%)
chega perto de deslocar `g†` o suficiente para reconciliar H_B com o dado,
nem de derrubar H_A do IC. O resultado é robusto a esse tipo de mecanismo.

## 3. a0_A = cH0/(2π) é uma "coincidência cósmica" pré-existente na literatura MOND

Busca externa confirma: Milgrom já notara, décadas antes deste teste, que
`2π·a0 ≈ c·H0` (equivalentemente `a0 ≈ cH0/(2π)`) é uma coincidência
numérica discutida na literatura padrão de MOND (não uma predição nova de
Tamesis) — ver p.ex. discussão em Milgrom, "The a0-cosmology connection in
MOND" (arXiv:2001.09729) e revisões subsequentes. Isso significa que H_A
"sobreviver" ao dado real SPARC não é evidência de que a "Ponte
Holográfica" tenha poder discriminativo específico de Tamesis — é
consistente com um fato numérico já conhecido no campo antes de qualquer
formulação Tamesis. Qualquer framework (incluindo a observação nua de
Milgrom, sem nenhum aparato teórico Tamesis) que apontasse para
`a0≈cH0/(2π)` passaria pelo mesmo teste.

## 4. Circularidade parcial

`g†` ajustado nesta sessão reproduz o valor publicado por McGaugh, Lelli &
Schombert (2016) a 0.2% de diferença. Isso é esperado, não uma confirmação
independente: a fórmula da RAR e a amostra SPARC usadas aqui são as mesmas
(um subconjunto) que originaram o valor de literatura. O teste não é
circular no sentido forte (dado sintético gerado pelo próprio modelo, como
no Achado 7 do audit legado EFE) — dados reais e independentes de qualquer
cálculo de `a0` foram usados — mas é circular no sentido fraco de que
"ajustar RAR ao SPARC reproduz RAR/SPARC" é garantido a priori, independente
de qual candidato de `a0` está sendo testado. A parte genuinamente testável
é só a comparação final: os dois números candidatos (a0_A, a0_B) caem ou
não dentro do IC de um ajuste que já era esperado reproduzir ~1.2e-10.
