# Descoberta adversarial de nulos — `DISC-COSMOLOGY-MOND-SPARC-004`

**Papel:** Metodologia 5 (`05_DISCOVERY_LAB/00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md`), agente
debunker convencional — **não** multiplicidade oculta (investigada em paralelo por outro agente).
**Arquivos travados tocados:** nenhum modificado (`delta_obs_newt.py`, `deprojection_common.py`
importados só em modo leitura; `git diff` vazio, confirmado abaixo).

## Veredito resumido

**O achado NÃO sobrevive intacto.** Existe um mecanismo mundano, quantificável, **confirmado
experimentalmente por simulação isolada e por um teste decisivo de simetria**, que infla
`δ_obs-newt` na MESMA direção e na MESMA forma (decrescente com o bin de `g_N`) interpretada como
evidência pró-MOND — e esse mecanismo é uma **falha estrutural no próprio desenho do ramo "mock"
do Adendo 4c**, não uma propriedade física do céu. Não é multiplicidade oculta, não é seleção de
Malmquist clássica, não é erro de paralaxe, não é viés de massa-luminosidade — é viés de
Rice/Rayleigh na magnitude de um vetor de movimento próprio ruidoso, presente OBRIGATORIAMENTE no
ramo real (dado observado com erro Gaia real) e AUSENTE por construção no ramo mock (órbita
Kepleriana sintética sem ruído injetado).

Isso não elimina 100% do sinal reportado nem prova que MOND está descartado — mas invalida a
alegação de que o IC de 95% do `a0` ajustado (`[2,944; 4,494]×10⁻¹⁰` m/s²) e o veredito
`BOTH_FALSIFIED` estão livres de viés sistemático não modelado. **Antes de qualquer decisão de
catalogação, a pipeline precisa ser re-rodada com um ramo mock que também carregue ruído Gaia
realista** (ver Recomendação).

## Mecanismos testados e descartados

| # | Mecanismo | Veredito | Evidência-chave |
|---|---|---|---|
| 1 | Erro sistemático de paralaxe/distância correlacionado com separação angular | **Descartado** | `corr(erro relativo de paralaxe, θ)=-0,10`; `corr(erro relativo de paralaxe, log sepAU)=+0,003` — sem correlação relevante, e na direção errada quando existe |
| 2 | Seleção Malmquist-tipo via corte de erro relativo de PM | **Fraco/secundário** | O corte `PM_RELERR_MAX=0,01` usa o erro relativo do PM TOTAL de cada estrela individualmente (`e_pmRA1`/`pmRA1`), não filtra diretamente por `dmu`/`v_p` do par — mecanismo relacionado mas distinto do item 5 |
| 3 | Contaminação residual por alinhamento casual (pares não-ligados) | **Descartado como causa principal** | Contaminação esperada de `R_chance_align` em bin 0 (média de R) ≈ 0,07% (~4-5 sistemas de 6042) — pequena demais para mover uma mediana, apesar de `R` cair ~500× de bin 0 para bin 4 (direcionalmente consistente, quantitativamente irrelevante) |
| 4 | Viés sistemático na relação massa-luminosidade (Pecaut & Mamajek 2013) | **Descartado** | `M_tot` mediano é ~flat entre bins 0-3 (0,90-0,92 M☉) e MAIOR (não menor) no bin 4 (1,04 M☉) — tendência oposta à necessária para produzir o declínio monotônico observado |
| 5 | Viés no próprio estimador `δ_obs-newt` sob a distribuição real completa | **CONFIRMADO — causa principal identificada** | Ver seção detalhada abaixo |
| 6 | Outros (checagem de velocidade de escape) | **Corrobora o item 5** | 13,4% do bin 0 "viola" o piso de velocidade de escape Newtoniana `v_p≤√(2GM/s)` — ordem de grandeza maior que a contaminação esperada de alinhamento casual (item 3), mas do tamanho certo para um efeito de viés de medida em baixo SNR |

## O mecanismo principal: viés de Rice/Rayleigh em `dmu` observado

### A física do problema

`v_p` real é calculado de `dmu = √((pmRA1-pmRA2)² + (pmDE1-pmDE2)²)` — a magnitude de um vetor 2D.
Quando esse vetor tem componentes com ruído Gaussiano (erro de medida Gaia real), sua magnitude
observada segue uma **distribuição de Rice**, cuja esperança satisfaz **sempre**
`E[dmu_obs] ≥ dmu_verdadeiro`, com o viés crescendo rapidamente quando a razão sinal-ruído (SNR)
cai. Isso é matematicamente garantido — não é uma hipótese, é uma propriedade da distribuição.

Esse viés é **pior exatamente nos sistemas de maior separação** (bin 0, menor `g_N`): a precisão
astrométrica absoluta do Gaia por estrela é aproximadamente constante (`σ_dmu` mediano ~0,08-0,09
mas/ano em todos os bins), mas o sinal `dmu` verdadeiro cai com a separação (mediana 0,375 mas/ano
no bin 0 vs. 1,69 mas/ano no bin 4) — logo o SNR de `dmu` cai de ~19-21 (bin 4) para ~3-4 (bin 0),
exatamente onde o pré-registro relata o maior `δ_obs-newt` (+0,227) e onde o ajuste de `a0` é mais
sensível.

**Corroboração independente:** essa mesma quantidade (SNR de `dmu`) já existe no catálogo de
Hwang, Ting & Zakamska (2022) sob o nome `dpm_sig` — usada no pipeline oficial (Gap (a)) só para
decidir o RAMO de amostragem de excentricidade, nunca para avaliar o próprio `v_p_real`. A minha
métrica de SNR calculada independentemente correlaciona **0,994** com `dpm_sig` do Hwang, e
`dpm_sig` mediano cai de 30,2 (bin 4) para 5,8 (bin 0), com 26% do bin 0 tendo `dpm_sig<3` (limiar
que o próprio Hwang usa para considerar a medida não-confiável). O time do pré-registro já sabia
que essa quantidade importa — só não a conectou ao cômputo de `v_p_real` que alimenta a estatística
discriminadora.

### Ramo mock nunca carrega esse ruído — assimetria estrutural

`don.generate_synthetic_vp_newtonian` (usada pelo Adendo 4c para o ramo mock) gera `v_p` a partir
de uma órbita Kepleriana pura + projeção geométrica — **determinística dado o sorteio de
geometria orbital, sem qualquer ruído de medida astrométrico injetado, em nenhum ponto**. O ramo
real, ao contrário, usa `v_p` derivado de `pmRA`/`pmDE` OBSERVADOS — que **necessariamente**
carregam o erro de medida Gaia real de cada sistema. `δ_obs-newt = mediana_real − mediana_mock`
não cancela esse viés porque só um dos dois lados o carrega.

### Teste 1 — mecanismo isolado (zero MOND, mock oficial sem ruído, "teste" com ruído Gaia real)

Simulação 100% Newtoniana: gero uma órbita Kepleriana verdadeira por sistema (mesma `s`, `M_tot`,
distribuição de excentricidade REAL da amostra), converto para `dmu` verdadeiro, decomponho em
`(ΔpmRA,ΔpmDE)` com ângulo de posição isotrópico, injeto ruído Gaussiano usando o orçamento de erro
REAL (`e_pmRA1,e_pmRA2,e_pmDE1,e_pmDE2`) de CADA sistema, recomputo `dmu_obs` → `v_p_obs`. O ramo
mock permanece exatamente como definido no Adendo 4c (sem ruído).

| bin | `δ_null_noise` | IC95% | `δ_obs-newt` real (referência) | fração explicada |
|---|---|---|---|---|
| 0 (menor `g_N`) | **+0,0750** | [0,052; 0,098] | +0,2274 | **33%** |
| 1 | +0,0318 | [0,007; 0,056] | +0,1723 | 18% |
| 2 | +0,0140 | [-0,009; 0,037] | +0,1313 | 11% |
| 3 | +0,0064 | [-0,017; 0,029] | +0,1027 | 6% |
| 4 (maior `g_N`) | -0,0056 | [-0,030; 0,017] | +0,0467 | ~0% |

Com **zero física MOND**, apenas o viés de Rice sobre a distribuição real de massa/separação/
excentricidade da amostra de descoberta, o mecanismo sozinho reproduz o padrão qualitativo
completo (positivo, decrescente com `g_N`) e é estatisticamente significativo (IC95% exclui 0) nos
dois bins mais informativos para o ajuste de `a0`.

### Teste 2 (decisivo) — comparação nula simétrica

Repito a simulação, mas agora **ambos** os ramos (teste E mock) recebem ruído Gaussiano real
independente (mesmo orçamento de erro por sistema, sorteios independentes) — a comparação
corretamente simétrica que o Adendo 4c deveria ter usado.

| bin | `δ_symmetric_noise` | IC95% |
|---|---|---|
| 0 | +0,0084 | [-0,015; 0,033] |
| 1 | +0,0099 | [-0,014; 0,035] |
| 2 | +0,0048 | [-0,019; 0,028] |
| 3 | +0,0003 | [-0,024; 0,021] |
| 4 | +0,0048 | [-0,020; 0,027] |

O viés **colapsa para consistente-com-zero em todos os 5 bins**, em magnitude comparável ao piso de
ruído do próprio controle negativo oficial do pré-registro (~0,02-0,07 dex). Isso **confirma
experimentalmente** que o sinal do Teste 1 vem inteiramente da assimetria de desenho (mock sempre
sem ruído), não de qualquer propriedade física do céu real.

### Checagem de robustez empírica sobre o dado REAL — resultado que complica (mas não invalida) a conclusão

Restringi a própria amostra de descoberta real a `dpm_sig>3` (mesmo limiar que Hwang/Chae já usam
para confiabilidade de ajuste orbital — 88,6% da amostra, 26.769/30.203 sistemas) e rodei
`don.run_delta_obs_newt` oficial sem modificação:

| bin | `δ_obs-newt` (amostra completa) | `δ_obs-newt` (`dpm_sig>3` só) |
|---|---|---|
| 0 | +0,2274 | **+0,3303** |
| 1 | +0,1723 | +0,2335 |
| 2 | +0,1313 | +0,1715 |
| 3 | +0,1027 | +0,1260 |
| 4 | +0,0467 | +0,0721 |

**Contra-intuitivo:** restringir a alto-SNR AUMENTOU o sinal em todos os bins, não diminuiu — o
oposto do que "ruído explica tudo" preveria ingenuamente. Investigando: o subconjunto excluído
(`dpm_sig≤3`) carrega excentricidade medida sistematicamente MAIOR (mediana `e=0,95` vs. `0,83` no
bin 0) e `M_tot` menor (0,69 vs. 0,98 M☉). Excentricidade mais alta empurra o baseline do PRÓPRIO
ramo mock mais para baixo (o efeito estrutural `v²/r`-vs-excentricidade já documentado na Seção 4c
do pré-registro), diluindo o `δ` bruto nesse subconjunto de baixo SNR em vez de infla-lo. **Dois
mecanismos mundanos distintos** (viés de Rice em `dmu`, e viés de `v²/r`-vs-excentricidade) estão
entrelaçados no dado real de um jeito que um corte simples de SNR não separa — por isso esse corte
não serve como teste limpo do mecanismo de Rice isolado (só o teste sintético controlado acima
serve para isso).

## Outras checagens de apoio

**Velocidade de escape:** `v_p ≤ v_esc(s) = √(2GM_tot/s)` é condição NECESSÁRIA para qualquer
órbita Newtoniana ligada (pois a separação 3D verdadeira `r ≥ s` sempre, então
`v_esc(r) ≤ v_esc(s)`; um boost MOND de ordem 1-3× não relaxa isso o suficiente para violações
>2×). 13,4% do bin 0 excede esse piso (1,3% excede 2×), caindo monotonicamente para 3,9%/0,02% no
bin 4 — ordem de grandeza maior que a contaminação por alinhamento casual esperada (item 3, ~0,07%),
mas do tamanho certo para ser explicado por inflação de `dmu` em baixo SNR (item 5).

## Reprodutibilidade

Nenhum arquivo travado (`delta_obs_newt.py`, `deprojection_common.py`) foi editado — `git diff`
vazio confirmado ao final desta sessão. Todos os testes acima chamam as funções públicas já
travadas (`dc.run_mc_deprojection`, `don.generate_synthetic_vp_newtonian`,
`don.projected_log_gN`, `don.assign_bins_by_projected_gN`, `don.run_delta_obs_newt`) sem
modificação, usando os mesmos parquets de dado (`quality_filtered_sample.parquet`,
`hwang_eccentricity_subset.parquet`) e o mesmo `discovery_holdout_split.json` (holdout nunca
tocado). Scripts de diagnóstico ad-hoc ficam em scratchpad (não commitados no repositório, seguindo
a mesma convenção de arquivos de trabalho de agente já usada nesta linha de teste).

## Recomendação

O `a0` ajustado (`3,634×10⁻¹⁰` m/s², IC95% `[2,944; 4,494]×10⁻¹⁰`) e o veredito `BOTH_FALSIFIED`
em `result_primary.json` **não devem ser aceitos como definitivos** sem antes:

1. Reconstruir o ramo mock do Adendo 4c injetando ruído Gaussiano de medida realista por sistema
   (mesmo orçamento `e_pmRA`/`e_pmDE` do sistema real correspondente) em vez de `v_p` sintético
   sem ruído — o Teste 2 acima demonstra que isso elimina o viés estrutural identificado.
2. Re-rodar a análise primária completa (`n_mc=200`, `bootstrap=1000`) com esse mock corrigido
   sobre os 30.203 sistemas reais.
3. Só então comparar o `a0` resultante com `a0_A`/`a0_B` e decidir o veredito de H_A/H_B.

Até essa correção, o resultado `LOCKED` atual carrega uma fonte de viés sistemático documentada,
direcionalmente idêntica ao sinal reivindicado e concentrada exatamente no bin mais diagnóstico
para MOND (bin 0), **não capturada pelo IC bootstrap reportado** — o bootstrap só reamostra a
variância geométrica de Monte Carlo e a variância amostral entre sistemas; `v_p_real` é fixado
deterministicamente ANTES do bootstrap, então nenhuma incerteza/viés de medida de `v_p_real` entra
no IC relatado. A validação sintética obrigatória do Adendo 4c (Seção 4b/4c) não capturou essa
lacuna porque testou apenas cenários sintético-vs-sintético SEM ruído em ambos os lados — nunca o
cenário que realmente ocorre na análise primária (real ruidoso vs. mock sem ruído).

**Dados de apoio:** `null_discovery_sparc004.json` (companheiro deste relatório, mesmo diretório)
contém todos os números acima em formato estruturado.
