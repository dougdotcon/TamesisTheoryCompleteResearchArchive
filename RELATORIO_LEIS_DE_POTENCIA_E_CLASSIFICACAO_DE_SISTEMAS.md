# Auditoria de leis de potência e classificação dos sistemas Tamesis

**Data da auditoria:** 2026-07-29  
**Base conceitual:** `TASKS/leidepotencia-identificar-novossistemas.md` (leitura integral)  
**Escopo:** arquivos de pesquisa em `01_TAMESIS_CORE`, `02_TAMESIS_MC_V1_OUTPUTS`, `RECURSOS_PARA_PESQUISA` e `90_LEGACY`. A pasta `04_FORMAL_RESEARCH_LAB` foi mantida fora da auditoria por seu protocolo próprio.

## Conclusão executiva

O texto da tarefa é uma boa fonte de hipóteses, mas não demonstra que todos os sistemas complexos obedecem a uma única lei de potência. Ele mistura pelo menos seis objetos estatísticos distintos: distribuição de valores, distribuição de eventos, correlação espacial, espectro de rede, escalamento próximo a uma transição e lei de contagem. Eles não podem ser comparados apenas porque aparecem como uma reta em um gráfico log-log.

Na pesquisa local encontrei:

1. **Uma assinatura direta de lei de potência já declarada:** a função de correlação de dois pontos do `ReactiveCosmoMapper`, com `ξ(r)=(r/r₀)^−1,8`. É uma alegação de validação legada, não uma confirmação independente da teoria.
2. **Duas propostas formais de escalamento:** a classe de transição `U_{1/2}` (`α=0,5`) e o regime “Critical Integration” da topologia cognitiva (`P(k)~k^−γ`). Ambas são hipóteses/modelos, não resultados empíricos publicados.
3. **Vários candidatos a criticidade, universalidade, redes e sistemas hierárquicos**, mas sem uma série de dados e uma comparação estatística que permitam chamar o resultado de lei de potência.
4. **Um resultado metodológico importante:** a própria descoberta U12 afirma que cada sistema pode ter sua própria lei (`log n` para mapas aleatórios, `n/log n` para primos), portanto a classificação deve ser por mecanismo e observável, e não por uma constante universal imposta a todos.

## O que deve ser chamado de lei de potência

Para uma variável positiva `X`, a hipótese de cauda é

```text
p(x) = C x^−α,       x ≥ x_min
P(X ≥ x) ∝ x^−(α−1)  (para α > 1).
```

Em uma correlação espacial, a grandeza é outra:

```text
ξ(r) ∝ r^−γ.
```

Em uma transição crítica, o expoente relaciona uma observável ao afastamento do ponto crítico, por exemplo `O(t)∝|t|^β` ou `ξ(t)∝|t|^−ν`. Em uma rede, normalmente se testa a distribuição de grau `P(k)`, não a distribuição de qualquer variável chamada “complexidade”. Em uma lei espectral, devem ser especificados densidade espectral, espaçamento ou rigidez; isso não é automaticamente uma cauda de Pareto.

O procedimento mínimo é: definir a unidade e a variável antes de olhar os dados; estimar `x_min` e `α` por máxima verossimilhança; testar ajuste com estatística KS e bootstrap; comparar verossimilhança com lognormal, exponencial, Weibull e lei de potência truncada; declarar a faixa de escala e a incerteza; repetir em dados independentes. Regressão linear em histograma log-log é apenas visualização. Clauset, Shalizi e Newman propõem exatamente essa combinação de máxima verossimilhança, KS e razões de verossimilhança, porque ajuste por mínimos quadrados pode ser enganoso [artigo e DOI](https://doi.org/10.1137/070710111). Stumpf e Porter alertam que muitas leis de potência publicadas não têm suporte estatístico ou mecanismo causal suficiente [Science, DOI](https://doi.org/10.1126/science.1216142).

### Critérios de decisão

Um resultado pode ser rotulado como **H2 — suporte empírico** somente se houver: (a) pelo menos uma faixa de escala substancial, idealmente duas ordens de grandeza quando a resolução permitir; (b) cauda ou escalamento fora da faixa de saturação e do ruído; (c) poder preditivo fora da amostra; (d) alternativas não inferiores; e (e) mecanismo compatível. Caso contrário, use **H1 — hipótese formal**, **E1 — evidência computacional/legada**, **E0 — menção lexical**, ou **Q — quarentena especulativa**.

## O que o arquivo da tarefa realmente acrescenta

O transcript usa como exemplos Pareto, terremotos, incêndios, avalanches, fractais, magnetismo no ponto de Curie, criticidade auto-organizada, redes da Internet e crescimento por conexão preferencial. Ele também faz uma distinção correta entre crescimento multiplicativo, que tende a produzir lognormal, e mecanismos adicionais que podem produzir uma cauda de potência. O exemplo da pilha de areia é apresentado como modelo; o próprio texto registra que uma pilha de areia real pode não obedecer à mesma lei. Portanto, “criticidade auto-organizada” deve ser tratada como mecanismo a ser testado, nunca como explicação automática.

## Classificação dos sistemas já presentes no repositório

| Grupo de sistema | Observável correto | Material local | Estado atual | Próximo teste |
|---|---|---|---|---|
| **A. Redes sem escala / topologia** | `P(k)`, força, grau, assortatividade, modularidade, k-core | [PAPER A — teoria topológica cognitiva](90_LEGACY/08_COGNITIVE_TOPOLOGY/TOPOLOGICAL_THEORY_OF_COGNITIVE_STATES/PAPER_A_TOPOLOGICAL_THEORY.md:60) | **H1**: propõe `P(k)~k^−γ` para “Critical Integration” e três regimes cognitivos; não há série empírica no artigo | Extrair redes/temporais reais, estimar cauda, comparar lognormal e potência truncada; testar se os três regimes se separam fora da amostra |
| **B. Transições críticas / avalanches** | tamanho, duração e área de eventos; suscetibilidade; comprimento de correlação; escalamento finito | [U12 — classe `U_{1/2}`](01_TAMESIS_CORE/06_Universality_Discovery/Regime_Transitions/Theory/index.html:185), relatórios de massa crítica em `RECURSOS_PARA_PESQUISA/PATH_A_SCIENTIFIC_TRUTH/STAGE_01_Mc_CRITICAL_MASS` | **H1/H0**: `α=0,5` é resultado analítico do modelo; a massa crítica é programa/candidato, não demonstração de cauda em dados | Simulações em vários `n`, colapso de tamanho finito, estimativa de expoentes e comparação com classes conhecidas; medir avalanches em vez de apenas o parâmetro de controle |
| **C. Clustering espacial cosmológico** | função de correlação `ξ(r)` e sua covariância | [ReactiveCosmoMapper — validação estatística](01_TAMESIS_CORE/01_Foundation/Scientific_Engines/ReactiveCosmoMapper/relatos/04_statistical_validation.md:23) | **E1**: declara `γ≈1,8` e comparação com ΛCDM; é o caso local mais próximo de uma lei observacional, porém o relatório é legado e não fornece uma análise reprodutível completa | Recalcular Landy–Szalay em catálogos e mocks, corrigir geometria cônica/seleção, publicar intervalo de `r`, covariância, bootstrap e comparação com alternativas |
| **D. Espectros e universalidade** | `P(s)` de espaçamentos, number variance, rigidez espectral, densidade de estados | [paper de universalidade espectral](RECURSOS_PARA_PESQUISA/PROOF/paper_02_spectral_universality.html), materiais Riemann/GUE e Laplacianos | **E0/H1**: universalidade espectral não é uma lei de potência de cauda por definição | Testar a estatística espectral apropriada; só introduzir expoente se existir uma janela de escalamento identificável |
| **E. Crescimento multiplicativo / seleção** | distribuição de tamanho, retorno, riqueza, sucesso, tempo de vida | documentos de crescimento, startups, seleção estrutural e ecossistemas | **H0/H1**: o mecanismo multiplicativo sozinho favorece lognormal; Pareto, truncamento e misturas são hipóteses concorrentes | Ajustar lognormal, Pareto, Pareto truncada e modelos de mistura; separar crescimento de sobrevivência, seleção e vantagem cumulativa |
| **F. Fractais, ramificações e geometria hierárquica** | dimensão fractal, massa-raio, distribuição de ramos, box-counting, escalamento | cosmologia reativa, grafos computacionais, propostas holográficas e sistemas biológicos | **H1**: analogia geométrica; fractalidade não prova uma distribuição de potência para eventos | Medir dimensão e invariância de escala em imagens/grafos; verificar dependência de resolução, limites e anisotropia |
| **G. Eventos extremos e risco sistêmico** | cauda de perdas, mortes, falhas, incêndios, colapsos | menções em relatórios de vulnerabilidade, ecossistemas e teoria cognitiva | **E0/H1**: não há base local consolidada de eventos independentes | Montar séries com definição de evento, censura e exposição; usar quantis e Expected Shortfall, não a média isolada |
| **H. Leis de contagem específicas do sistema** | número de ciclos, primos, órbitas ou objetos até `n` | [DISCOVERY_SUMMARY U12](01_TAMESIS_CORE/06_Universality_Discovery/U12_Discovery/DISCOVERY_SUMMARY.md:195) | **E1/H1**: `~(1/2)log(n)+γ` para mapas aleatórios e `n/log(n)` para primos; é evidência contra uma lei única, não a favor dela | Preservar a lei própria de cada classe e não rebatizá-la como “potência” sem derivação |

### Resultado da auditoria

O inventário lexical (Markdown/HTML, excluindo o laboratório formal, `publicar`, `publicados` e este relatório) encontra: `power law` em **21** arquivos, `power-law` em **9**, `lei de potência` em **7**, `Pareto` em **4**, `scale-free` em **8**, `criticality` em **22**, `critical exponent` em **11**, `log-log` em **4** e `avalanche` em **3**. Não há ocorrência literal de `heavy tail`, `preferential attachment` ou `self-organized critical` nesse recorte. Esses números se sobrepõem e são apenas um filtro de triagem, não uma contagem de descobertas: vários usos são documentação, comparação, nomes de algoritmos (“Pareto search”) ou propostas sem dados. A classificação acima evita converter uma palavra em evidência.

## Como identificar um novo sistema no acervo

Para cada estudo, criar uma ficha com os campos abaixo:

```text
ID do sistema
Unidades e fronteiras do sistema
Estado/observável medido
Evento ou série temporal usada
Escala mínima, máxima e resolução
Lei candidata e expoente
Mecanismo gerador proposto
Alternativas estatísticas
Dependência entre observações e censura
Dados/código reproduzíveis
Nível E0/E1/H1/H2/Q
Critério de falsificação
```

O agrupamento deve seguir o par **observável + mecanismo**. Por exemplo, “rede cognitiva” e “Internet” podem compartilhar uma distribuição de grau, mas só pertencem à mesma classe se apresentarem mecanismos comparáveis (crescimento, conexão preferencial, restrições de capacidade) e expoentes/estatísticas compatíveis. “Cérebro”, “corpo”, “genoma” e “universo” não devem ser colocados na mesma classe apenas por serem sistemas complexos.

## Programa de pesquisa recomendado

1. **Fase de inventário:** preencher as fichas dos grupos A–H e separar cada afirmação em observação, modelo, interpretação e previsão.
2. **Fase estatística:** implementar um protocolo comum de MLE + KS/bootstrap + comparação de alternativas; conservar os dados brutos e o código.
3. **Fase de mecanismos:** para redes, testar crescimento e conexão preferencial; para transições, testar escalamento finito e correlação; para crescimento, comparar processo multiplicativo/lognormal; para fractais, medir dimensão.
4. **Fase de replicação:** validar apenas resultados que sobrevivam a outra janela de escala, outro catálogo/simulação e outro método de estimação.
5. **Fase de síntese:** só depois comparar expoentes entre grupos. Uma “classe de universalidade Tamesis” exigiria invariância demonstrada entre sistemas independentes, não apenas uma semelhança visual.

## Limites conceituais para a tese maior

Leis de potência podem ser uma linguagem para descrever hierarquia, caudas pesadas e invariância de escala. Elas não demonstram, por si só, que a natureza “economiza energia”, que consciência é uma reação a complexidade, que o corpo é uma extensão de um genoma ou que existe um universo computacional. Essas são hipóteses causais separadas. A ponte só será científica se cada uma produzir uma variável mensurável, uma previsão quantitativa e um teste que possa falhar.

## Fontes metodológicas e de referência

- Clauset, Shalizi & Newman (2009), *Power-law distributions in empirical data*, SIAM Review, DOI [10.1137/070710111](https://doi.org/10.1137/070710111).
- Stumpf & Porter (2012), *Critical truths about power laws*, Science, DOI [10.1126/science.1216142](https://doi.org/10.1126/science.1216142).
- Bak, Tang & Wiesenfeld (1987), *Self-organized criticality: An explanation of the 1/f noise*, Physical Review Letters, DOI [10.1103/PhysRevLett.59.381](https://doi.org/10.1103/PhysRevLett.59.381).
- Barabási & Albert (1999), *Emergence of scaling in random networks*, Science, DOI [10.1126/science.286.5439.509](https://doi.org/10.1126/science.286.5439.509).
- Zehavi et al. (2002), *Galaxy clustering in early SDSS redshift data*, descrição e preprint [astro-ph/0106476](https://arxiv.org/abs/astro-ph/0106476), que reporta `ξ(r)` aproximadamente como potência em uma faixa limitada.

**Classificação final:** há um resultado cosmológico local que merece reanálise como assinatura de potência; há modelos teóricos de redes e transições que podem gerar novos testes; e há muitas menções que devem permanecer como hipóteses ou quarentena até que dados e comparações estatísticas sejam produzidos.
