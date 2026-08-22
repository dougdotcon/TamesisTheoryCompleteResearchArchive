# Relatório adversarial combinado — reexecução independente + debunker de descoberta de nulos

**Test ID:** `SPARC-FMULTI-STAGE2` (etapa de `DISC-COSMOLOGY-MOND-SPARC-004`, pré-registro `PREREGISTRATION_STAGE2.md`, `DISC-DEC-029`)
**Papel deste agente:** combinado, por mandato explícito de `AGENTS.md` passo 7 +
`METHODOLOGY_EXTENSIONS.md` Seção 5 — (1) reexecução adversarial independente
padrão (reprodução do zero, a partir do pré-registro travado, sem ler o
código do agente primário antes de ter meus próprios números) e (2)
debunker de descoberta adversarial de nulos (caça deliberada por uma
explicação convencional/mundana para o resultado, antes de aceitá-lo).
**Data:** 2026-08-22
**Insumos lidos por completo, ANTES de escrever qualquer linha de código:**
`PREREGISTRATION_STAGE2.md`, `METHODOLOGY_ADDENDUM.md`,
`PROVENANCE_CHAE_EQS.md`, `RESULTS_SUMMARY_STAGE1.md`,
`../PREREGISTRATION.md` (SPARC-004 original), `../../COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md`
(cortes de qualidade exatos), `00_GOVERNANCE/AGENTS.md`,
`00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md`. `RESULTS_PRIMARY_STAGE2.md`,
`analysis/run_stage2_primary_analysis.py` e
`results/result_stage2_primary.json` só foram lidos **depois** de eu ter
meus próprios números independentes prontos (Seção 1 abaixo).

**Veredito resumido (detalhado abaixo):**
- **Parte 1 (reprodução independente): `CONFIRMED`** — todos os números
  batem com o agente primário até a precisão de ponto flutuante reportada
  (mesma semente, pipeline determinístico), nenhum bug encontrado.
- **Parte 2 (debunker): o veredito `BOTH_FALSIFIED` NÃO deve ser aceito
  como está.** Recomendação: **rebaixar para `CLOSED_INCONCLUSIVE`**
  (mesmo padrão de fechamento já usado em v1/v2 desta linha de teste),
  por causa de um confundidor real e estatisticamente robusto descoberto
  pela checagem RUWE exploratória da Seção 2.4 abaixo — não citado nem
  antecipado pelo agente primário, que apenas citou a fração RUWE como
  contexto informativo sem comparar os dois subgrupos.

---

## 1. Parte 1 — Reexecução adversarial independente

### 1.1 Método

Pré-registro lido por completo (Seção 0 acima). Reutilizei (autorizado
explicitamente pelo mandato desta tarefa, e pela Seção 12/DISC-DEC-029 do
próprio pré-registro) o pipeline já travado e adversarialmente verificado
do Estágio 1 — `analysis/selfcal_pipeline.py`,
`analysis/companion_injection.py`, mais o módulo `analysis/deprojection_common.py`
(LOCKED) — sem editar nenhum desses três arquivos. O que escrevi do zero,
**sem consultar `run_stage2_primary_analysis.py` em nenhum momento antes de
ter meus próprios resultados**, foi o script-driver
(`adversarial_stage2/analysis/adversarial_driver_stage2.py`): a sequência
exata de chamadas da Seção 4.1-4.6 do pré-registro, a lógica da regra de
decisão de duas camadas (Seção 5), e a checagem dos 5 gatilhos adversariais
(Seção 6).

Verifiquei, por inspeção direta de `selfcal_pipeline.py` (linhas 424-487),
que `calibrate_f_multi(..., return_raw=True)` propaga a MESMA semente
`seed+777` usada para `final_result` para dentro de `final_raw` — a
correção de código do item 12.4/`DISC-DEC-029` está de fato implementada,
não é apenas texto. Por isso meu driver usa `calib["final_raw"]`
diretamente em `bootstrap_a0_refit()`, **sem reconstrução manual** de
`run_delta_obs_newt_selfcal(...)` — exatamente o ponto que o próprio
pré-registro (Seção 4.5) sinalizou como o maior risco de erro silencioso.

Parâmetros usados (idênticos à Seção 4.6, nenhum escolhido por mim):
`seed=20260822`, `n_mc=200`, `N_bootstrap=2000`, `anchor_bin=4`,
`xtol=5e-4`, `f_lo=0`, `f_hi=0.9`, `include_wobble=True`,
`real_gets_astrometric_noise` não sobrescrito (permanece `False`, o
default correto para dado real).

Amostra: os mesmos 30.203 sistemas de descoberta reais, carregados de
`quality_filtered_sample.parquet` + `hwang_eccentricity_subset.parquet`,
filtrados por `discovery_pair_ids` de `discovery_holdout_split.json`.

**Script:** `analysis/adversarial_driver_stage2.py`
**Resultado numérico completo:** `results/result_adversarial_stage2.json`
**Log de execução:** `results/adversarial_stage2_run.log`
**Tempo de execução:** 389,2 s.

### 1.2 Disciplina do holdout selado

Único ponto de contato com `discovery_holdout_split.json` é
`load_discovery_sample()` (linhas ~90-108 do driver): abre o JSON, extrai
`discovery_pair_ids`/`seed`/`n_discovery`, e imediatamente `del split` —
a chave `holdout_pair_ids` nunca é indexada em nenhuma linha do arquivo.
Confirmado por grep explícito nesta sessão:

```
$ grep -n "holdout_pair_ids\|n_holdout\|catalog\.parquet" \
    adversarial_stage2/analysis/adversarial_driver_stage2.py \
    adversarial_stage2/analysis/debunker_quality_cuts_and_ruwe.py
(zero ocorrências de codigo -- so' aparecem em prosa/docstring explicando a propria disciplina)
```

`catalog.parquet` (catálogo bruto El-Badry completo, 1,8M pares,
pré-corte-de-qualidade) também nunca é aberto por nenhum script desta
pasta — decisão deliberadamente conservadora desta sessão (documentada em
`debunker_quality_cuts_and_ruwe.py`, docstring do módulo): mesmo não
sendo tecnicamente "o holdout selado", tratei-o com a mesma disciplina
porque o próprio mandato desta tarefa pediu grep de `catalog.parquet`
lado a lado com os termos de holdout. Consequência prática: a análise do
item (a) da Seção 2 abaixo usa somente a distribuição de RUWE DENTRO da
amostra já cortada, suprida por literatura externa para o baseline
populacional pré-corte (citada explicitamente, não assumida de memória).

### 1.3 Comparação número a número

| quantidade | minha reprodução independente | agente primário (`result_stage2_primary.json`) | concordância |
|---|---|---|---|
| `f_multi_hat` | `0.10366572259293035` | `0.10366572259293035` | **idêntico** |
| `converged_bracket` | `True` | `True` | idêntico |
| `δ_ancora(f_lo=0)` | `0.05388947196031449` | `0.05388947196031449` | idêntico |
| `δ_ancora(f_hi=0.9)` | `−0.7615471684987544` | `−0.7615471684987544` | idêntico |
| `δ_obs-newt(bin)` corrigido | `[0.07772, 0.06568, 0.04862, 0.04174, −0.00018]` | `[0.07772, 0.06568, 0.04862, 0.04174, −0.00018]` | **idêntico** (10+ casas) |
| `gN_bin_median` (SI) | `[1.8807e-10, 1.6645e-9, 6.2203e-9, 1.7190e-8, 4.8638e-8]` | idêntico | idêntico |
| `n_sys_per_bin` | `[6042, 6040, 6040, 6039, 6042]` | idêntico | idêntico |
| `a0_fit(x0=1.0)` | `6.12469629412745e-11` | `6.12469629412745e-11` | **idêntico** |
| `a0_fit(x0=5.0)` | `6.124648319246344e-11` | `6.124648319246344e-11` | idêntico |
| IC95%(x0=1.0) | `[4.119617e-11, 8.580760e-11]` | `[4.119617e-11, 8.580760e-11]` | **idêntico** |
| IC95%(x0=5.0) | `[4.016289e-11, 8.580629e-11]` | `[4.016289e-11, 8.580629e-11]` | idêntico |
| veredito mecânico | `BOTH_FALSIFIED` | `BOTH_FALSIFIED` | idêntico |
| camada interpretativa resgata H_A/H_B? | Não (fator 1,4×: não; 1,6×: não) | Não | idêntico |
| veredito final | `BOTH_FALSIFIED` | `BOTH_FALSIFIED` | idêntico |
| gatilho 1 (fora de 1 ordem de ambas) | `fired=False` | `fired=False` | idêntico |
| gatilho 2 (bracket não convergido/borda) | `fired=False` | `fired=False` | idêntico |
| gatilho 3 (`f_multi` fora de 0,25-0,47) | `fired=True` | `fired=True` | idêntico |
| gatilho 4 (padrão inconsistente c/ Estágio 1) | `fired=False` | `fired=False` | idêntico |
| gatilho 5 (IC sensível a semente/N) | `fired=False` (IC alt. seed `[4.1188e-11,8.7349e-11]`, N=1000 `[4.1191e-11,8.5909e-11]`) | `fired=False` (IC alt. seed `[3.951e-11,8.569e-11]`, N=1000 `[4.119e-11,8.591e-11]`) | mesmo veredito qualitativo (sementes alternativas diferentes por desenho — cada agente escolheu sua própria semente extra — mas ambas confirmam robustez) |
| fração `RUWE1>1,4 ou RUWE2>1,4` | `0.19150415521636924` (calculada independentemente na Parte 2) | `0.19150415521636924` | **idêntico** |

**Nenhuma discrepância encontrada, de nenhuma magnitude.** A concordância
bit-a-bit em todos os valores estocásticos (que dependem de 200×30.203
sorteios Monte Carlo e 2000 réplicas de bootstrap) confirma que (i) a
sequência de chamadas do meu driver é operacionalmente idêntica à do
agente primário — mesmas sementes usadas nos mesmos pontos, nenhum
descasamento de semente entre `calib["final_result"]` e
`calib["final_raw"]` (o risco específico sinalizado pela Seção 4.5 do
pré-registro); (ii) nenhum dos dois agentes introduziu um bug de
implementação na aplicação do pipeline já travado ao dado real.

### 1.4 Veredito da Parte 1

**`CONFIRMED`.** A análise primária é reproduzível de forma independente,
sem nenhuma discrepância numérica, e a disciplina do holdout selado foi
respeitada por ambos os agentes (grep próprio confirma zero acessos a
`holdout_pair_ids`/`n_holdout`/`catalog.parquet` em ambos os scripts).

---

## 2. Parte 2 — Debunker de descoberta adversarial de nulos

Obrigatório porque o veredito é `BOTH_FALSIFIED`, não "nenhum sinal acima
do ruído" (`PREREGISTRATION_STAGE2.md` Seção 6, último parágrafo,
`METHODOLOGY_EXTENSIONS.md` Seção 5). Instrução: destruir a anomalia
usando qualquer mecanismo convencional conhecido, antes de aceitá-la.

Todas as checagens abaixo usam **somente a amostra de descoberta**
(30.203 sistemas) — nunca o holdout selado, nunca `catalog.parquet` bruto
(ver Seção 1.2). `f_multi_hat` usado em todas as checagens é o **meu
próprio** valor da Parte 1 (`0.103666`), não copiado do agente primário —
mantém o debunker inteiramente ancorado na minha reprodução independente.

**Scripts:** `analysis/debunker_quality_cuts_and_ruwe.py`
**Resultado numérico completo:** `results/result_debunker_quality_cuts_ruwe.json`
**Log:** ver saída do script (capturada nesta sessão).

### 2.1 Item (a) — cortes de qualidade excluem preferencialmente RUWE alto?

**Mecanismo hipotetizado:** nenhum dos cortes já aplicados
(`R<0,01`, concordância de distância `<3σ`, erro relativo de PM `<0,01`,
`BinType=MSMS`, `4<M_G<14`, `200<sepAU<30000`) é um corte de RUWE direto
(confirmado por leitura de `apply_quality_cuts.py`, LOCKED — nenhuma
menção a RUWE no código de corte). Mas El-Badry et al. (2021) nota
explicitamente que fontes com RUWE>1,4 tendem a ter incertezas de
paralaxe subestimadas — o que poderia fazer sistemas com companheira
oculta (RUWE alto) falharem preferencialmente o corte de concordância de
distância `3σ`, mesmo sem nenhum corte de RUWE explícito.

**Medido diretamente na amostra de descoberta:**

| checagem | resultado |
|---|---|
| fração residual com `max(RUWE1,RUWE2)>1,4` (amostra JÁ cortada) | **0,1915** (5784/30203) |
| Spearman ρ(RUWE_max, erro relativo de PM) | **−0,0197** (p=6×10⁻⁴) — praticamente nulo, sinal errado |
| Spearman ρ(RUWE_max, discordância de distância em σ) | **+0,1371** (p≈1,5×10⁻¹²⁶) — fraco mas real e na direção esperada |
| RUWE mediano no quartil MAIS PRÓXIMO da borda do corte de PM (0,01) vs. quartil folgado | `1,093` vs. `1,116` (razão 0,979 — direção OPOSTA à esperada) |
| RUWE mediano no quartil MAIS PRÓXIMO da borda do corte de distância (3σ) vs. quartil folgado | `1,147` vs. `1,089` (razão 1,053 — direção esperada, efeito pequeno) |

**Baseline populacional pré-corte** (literatura externa, verificada por
busca nesta sessão, não assumida de memória — `catalog.parquet` bruto não
foi aberto, ver Seção 1.2): Lindegren (2018) define RUWE≤1,4 como critério
de "boa solução astrométrica" a partir de uma amostra geral de ~339 mil
fontes dentro de 100 pc; levantamentos de aglomerados abertos (α Per,
Plêiades, Presépio) relatam 4,4-5,1% de fontes com RUWE>1,4. Chae (2023)
relata que 18.415/26.615 (69,2%) de sua amostra de binárias largas
satisfazem RUWE<1,2 (limiar mais frouxo que 1,4) — ou seja, **~31%** de
uma amostra de binárias largas SEM corte de RUWE tem RUWE≥1,2. [Lindegren
2018, GAIA-C3-TN-LU-LL-124; El-Badry, Rix & Heintz 2021, MNRAS 506, 2269;
Chae 2023, ApJ 952, 128 — verificados por busca nesta sessão.]

**Leitura:** existe uma correlação real, mas **fraca** (ρ=0,14), entre
RUWE e discordância de distância — na direção esperada pelo mecanismo
hipotetizado, mas explicando pouco da variância. O corte de erro relativo
de PM não mostra correlação alguma com RUWE (ρ≈0, sinal errado) — o
mecanismo hipotetizado especificamente para esse corte **não se sustenta**
nos dados. Mais decisivamente: a fração RESIDUAL de sistemas RUWE-alto na
amostra já cortada (19,15%) **não está deprimida** abaixo do baseline
populacional geral (~5% em aglomerados "limpos", ~31% na amostra de
binárias largas de Chae SEM corte de RUWE, a um limiar mais frouxo) — está
dentro/acima da faixa esperada de uma amostra de binárias largas
razoavelmente não-filtrada por RUWE. Se os cortes já aplicados estivessem
removendo fortemente sistemas RUWE-alto (candidatos a companheira oculta),
a fração residual deveria estar visivelmente REDUZIDA em relação ao
baseline — não é o que se observa.

**Conclusão do item (a): mecanismo real na direção certa (via o corte de
distância), mas quantitativamente FRACO — insuficiente, sozinho, para
explicar uma diferença de 2,4-4,5× entre `f_multi_hat=0,10` e a faixa da
literatura `0,25-0,47`.**

### 2.2 Item (b) — o modelo de wobble simplificado, sozinho, explica o padrão?

`RESULTS_SUMMARY_STAGE1.md` Seção 3 caracteriza o viés residual conhecido
do modelo de wobble simplificado (órbita interna circular, fase uniforme,
`a_in` log-uniforme) como uma tendência de **superestimar** `a0_true` por
um fator `1,4-1,6×` (`0,146-0,204` dex em log de `a0`), concentrada nos
bins de MENOR `g_N` — mesma direção qualitativa (não magnitude) do padrão
real observado.

**Meu `δ_obs-newt(bin)` corrigido real:** `[+0,0777; +0,0657; +0,0486;
+0,0417; −0,0002]` — declínio monotônico do menor para o maior `g_N`,
convergindo para ~0 no bin-âncora (por construção). Magnitude máxima
`0,078` dex no bin de menor `g_N`.

**Comparação:**
- **Direção/forma:** IDÊNTICA à assinatura conhecida (positivo, declinando
  com `g_N`, ~0 no bin-âncora) — nenhuma inversão de sinal, nenhuma
  concentração anômala em `g_N` alto.
- **Magnitude:** `0,078` dex está **abaixo** do piso da faixa de referência
  do Estágio 1 (`0,146-0,204` dex) — não acima, não além de 1 ordem de
  grandeza (gatilho 4 da Seção 6, checado explicitamente por ambos os
  agentes: `fired=False`).
- **Direção do `a0_fit` resultante:** o viés conhecido empurra `a0_fit`
  PARA CIMA (superestimativa). `a0_fit=6,125\times10^{-11}` já está
  **abaixo** de $a_0^A$ (fator `1,77×`) e MUITO abaixo de $a_0^B$ (fator
  `11,1×`) — ou seja, se o viés de wobble estivesse inflando `a0_fit`
  artificialmente para cima, o valor "verdadeiro" (livre desse viés)
  seria **ainda mais baixo**, não mais próximo de $a_0^A$/$a_0^B$. Isto é
  exatamente o que a camada interpretativa da Seção 5 do pré-registro já
  formalizou (dividir pelo fator de viés afasta ainda mais o IC dos dois
  alvos) — confirmado de forma idêntica pelo agente primário e por mim.

**Conclusão do item (b), ao nível AGREGADO:** o padrão pooled é
inteiramente compatível com (na verdade menor que) a assinatura já
conhecida e aceita do Estágio 1 — não é necessário invocar nenhuma
explicação adicional para o padrão AGREGADO. **Mas** esta conclusão
agregada esconde uma heterogeneidade real e importante — ver item (d)
abaixo, que a checagem de padrão da Seção 6 item 4 (por desenho, um
teste só sobre o padrão POOLED) não tem sensibilidade para capturar.

### 2.3 Item (c) — variação amostral/populacional normal?

Busca de literatura nesta sessão (não assumida de memória) mostra que
`f_multi` (ou análogos de fração de multiplicidade oculta em binárias
largas) varia substancialmente entre estudos, dependendo do corte de
qualidade, faixa de separação, e tipo espectral:

| estudo/amostra | valor | corte/contexto |
|---|---|---|
| Chae (2023), amostra principal | `0,48` | 26.615 binárias, `<200pc`, erro relativo de PM `<0,01` — **mesma faixa de corte de PM desta amostra** |
| Chae (2023), subamostra mais estrita | `0,36` | 19.716 binárias, erro relativo de PM `<0,005` (mais apertado) |
| Trabalho recente (2026, arXiv:2607.14450) revisitando QC de Chae | `0,31`/`0,36` | "considerando que alguns dados ruidosos foram removidos" — QC mais apertado reduz `f_multi` calibrado |
| Fração de companheira larga (Hwang et al., separação 200-20.000 UA) | `0,21±0,03` | já abaixo do piso 0,25 da faixa citada pelo pré-registro |
| Fração de alta-ordem-multiplicidade (K+K, M-anãs, sub-solares) | `0,40-0,62` | limite INFERIOR revisado, direção oposta (mais alto) |
| **Este teste (Estágio 2)** | **`0,10`** | `<200pc`, erro relativo de PM `<0,01`, `R<0,01`, concordância de distância `3σ` — SEM corte de RUWE explícito |

[Fontes verificadas por busca nesta sessão: Chae 2023 ApJ 952,128;
Chae 2024 ApJ 960,114 (`PROVENANCE_CHAE_EQS.md` já continha os valores
0,48/0,36); arXiv:2607.14450 "Revisiting Data Quality Control..."; buscas
adicionais sobre fração de companheira larga/alta-ordem-multiplicidade.]

**Leitura:** há variação real e documentada, de até `~3×` (0,21 a 0,62),
entre estudos com metodologia/amostra diferentes — e o próprio Chae mostra
que apertar o controle de qualidade em SUA PRÓPRIA amostra reduz `f_multi`
de `0,48` para `0,31-0,36` (uma redução de `~30-35%`, na MESMA direção do
item (a) acima). Isto é evidência real de que `f_multi` é sensível a
escolhas metodológicas, não um número populacional fixo e universal.
**Mas:** mesmo o valor mais agressivamente filtrado já publicado (`0,31`)
está `~3×` acima do `0,10` calibrado aqui — a variação documentada na
literatura, por si só, não cobre uma diferença desse tamanho. Note também
que esta amostra usa o MESMO corte de erro relativo de PM (`<0,01`) que a
amostra PRINCIPAL (menos filtrada) de Chae, que deu `0,48` — não a
subamostra mais estrita dele — o que torna ainda menos óbvio que a simples
escolha de corte explique a diferença.

**Conclusão do item (c): direção e mecanismo real e documentado (QC mais
apertado → `f_multi` mais baixo), mas magnitude INSUFICIENTE — não cobre
a diferença completa entre `0,10` e a faixa `0,25-0,47`.**

### 2.4 Checagem RUWE exploratória (nova, não tentada pelo agente primário) — achado decisivo

O agente primário citou a fração RUWE (19,15% vs. `frac_has_multi=10,35%`)
como contexto informativo, mas **não comparou os dois subgrupos
diretamente** — deixado explicitamente para esta sessão (`RESULTS_PRIMARY_STAGE2.md`
Seção 8/10). Desenhei e rodei esta checagem eu mesmo, dentro da amostra
de descoberta, usando meu próprio `f_multi_hat=0,1037`.

**Desenho:** dividir a amostra de descoberta em RUWE-alto
(`max(RUWE1,RUWE2)>1,4`, `n=5784`) vs. RUWE-baixo (`n=24419`), e computar
`δ_obs-newt(bin)` separadamente para os dois subgrupos, ANTES (`f_multi=0`,
cru) e DEPOIS (`f_multi=f_multi_hat=0,1037`, a MESMA correção única
aplicada uniformemente aos dois) da correção — mesmo espírito do check
RUWE decisivo que fechou a versão anterior deste teste (`../PREREGISTRATION.md`
Seção 7d), mas agora perguntando se a correção ÚNICA (calibrada na
amostra inteira) é suficiente para os dois subgrupos, não só se eles
diferem no bruto.

**Resultado (`N_bootstrap=500`, exploratório, `N_MC=200` — mesma escala
de ruído MC do Passo 1 principal):**

| bin (menor→maior g_N) | RUWE-alto, cru | RUWE-alto, corrigido (f=0,1037) | RUWE-baixo, cru | RUWE-baixo, corrigido (f=0,1037) |
|---|---|---|---|---|
| 0 | `+0,559` | `+0,486` [IC95% `0,404;0,559`] | `+0,093` | `+0,020` [IC95% `−0,008;0,050`] |
| 1 | `+0,524` | `+0,458` [`0,392;0,531`] | `+0,069` | `+0,002` [`−0,026;0,033`] |
| 2 | `+0,474` | `+0,412` [`0,348;0,476`] | `+0,050` | `−0,012` [`−0,042;0,015`] |
| 3 | `+0,385` | `+0,325` [`0,265;0,391`] | `+0,043` | `−0,014` [`−0,042;0,013`] |
| 4 (âncora) | `+0,225` | **`+0,171`** [IC95% **`0,126;0,212`**] | `−0,012` | `−0,066` [IC95% `−0,096;−0,038`] |

**O achado central:** mesmo no bin-âncora — o bin que a auto-calibração
FORÇA a ficar consistente com zero NA MÉDIA da amostra inteira — o
subgrupo RUWE-alto (19% da amostra) permanece com um excesso de
**`+0,171` dex, com IC95% bootstrap `[0,126; 0,212]` inteiramente acima de
zero**, mesmo depois de aplicar a correção `f_multi_hat=0,1037`. A
diferença RUWE-alto menos RUWE-baixo é **praticamente idêntica antes e
depois da correção** (bin-âncora: `+0,237` dex cru vs. `+0,238` dex
corrigido) — a correção de `f_multi=0,1037` não reduz visivelmente o
GAP entre os dois subgrupos, ela apenas desloca os dois em paralelo (o
suficiente para zerar o RUWE-baixo, numericamente dominante — 81% da
amostra — e insuficiente por larga margem para o RUWE-alto).

**Interpretação:** o modelo de auto-calibração de Chae assume implicitamente
que `f_multi` é aproximadamente homogêneo na população (um único parâmetro
escalar). Esta checagem mostra que isso é **falso** para esta amostra
real: existe um subgrupo de ~19% (marcado por RUWE alto, correlacionado
com companheira não resolvida ou pelo menos com solução astrométrica
degradada) que carrega um excesso de sinal MUITO maior — no bin-âncora,
onde física MOND é desprezível por construção (checagem a priori do
Estágio 1), sobra `+0,17` dex mesmo após a "correção". Um único `f_multi`
escalar, calibrado para zerar a média ponderada pelo tamanho de cada
subgrupo, necessariamente sub-corrige o subgrupo minoritário mais
contaminado e sobre-corrige o subgrupo majoritário menos contaminado (o
RUWE-baixo corrigido fica LIGEIRAMENTE negativo em 4 dos 5 bins,
incluindo o âncora, com IC95% excluindo zero por baixo — sinal do mesmo
efeito na direção oposta). Isto é **exatamente** o tipo de confundidor
convencional que este papel foi mandatado a caçar: não importa se a causa
raiz específica é multiplicidade oculta subestimada no subgrupo RUWE-alto,
ou algum outro artefato astrométrico correlacionado com RUWE alto e não
modelado pelo pipeline (crowding, solução de 5 parâmetros ruim, etc.) —
em qualquer dos dois casos, é um confundidor mundano, não Tamesis, que o
`f_multi` único não captura, e que deixa o `δ_obs-newt(bin)` agregado
(e portanto `a0_fit` e seu IC) sistematicamente não-confiável como medida
limpa.

**Caveat honesto:** este check usa `N_bootstrap=500` (não os `2000`
pré-registrados) e não faz parte da regra de decisão pré-registrada — é
exploratório/diagnóstico, mesma disciplina já usada pelo próprio agente
primário para a fração RUWE simples. Mas o tamanho do efeito (IC95% do
bin-âncora RUWE-alto corrigido inteiramente acima de zero, por uma margem
de `~5×` a largura do próprio IC) é grande o bastante que a conclusão
qualitativa — "o `f_multi` único não corrige adequadamente o subgrupo
RUWE-alto" — não depende de precisão adicional de bootstrap.

---

## 3. Julgamento final — a decisão mais consequente deste relatório

**O veredito `BOTH_FALSIFIED` não deve ser aceito como uma falsificação
limpa de $a_0^A$/$a_0^B$.** Recomendo **rebaixar para `CLOSED_INCONCLUSIVE`**,
mesmo padrão de fechamento já usado quando v1 (bug de ruído astrométrico
assimétrico) e v2 (multiplicidade oculta plausivelmente suficiente sozinha)
desta mesma linha de teste encontraram um confundidor mundano plausível.

**Razão central:** a checagem RUWE da Seção 2.4 demonstra, com dados reais
e um efeito estatisticamente robusto (não marginal), que o modelo de
auto-calibração de `f_multi` — um único parâmetro escalar por desenho —
está mal especificado para a heterogeneidade real desta amostra. Um
subgrupo de ~19% dos sistemas (marcado por RUWE alto) carrega um excesso
de `δ_obs-newt` muito maior que o resto da amostra, e a correção única
calibrada na amostra inteira deixa esse subgrupo com um resíduo grande e
estatisticamente significativo mesmo no bin-âncora — o ponto que deveria
estar, por construção, consistente com zero. Como TODO o resultado
`a0_fit`/IC95%/veredito depende inteiramente do `δ_obs-newt(bin)` pooled
corrigido por esse mesmo `f_multi` único, e esse pooled esconde uma
heterogeneidade de ~5× em magnitude entre subgrupos, `a0_fit=6,125\times10^{-11}`
não pode ser interpretado como uma medição limpa — é o resultado de uma
média mal ajustada a uma população não-homogênea, um mecanismo inteiramente
convencional (nenhum ingrediente Tamesis necessário) capaz de produzir
sozinho o padrão observado.

**Como isso se encaixa com os itens (a)/(b)/(c):**
- (a) e (c) mostram, cada um, um mecanismo real mas quantitativamente
  insuficiente sozinho (seleção correlacionada com RUWE é fraca; variação
  de literatura documentada não cobre a diferença completa).
- (b) mostra que o padrão AGREGADO é compatível com o viés de wobble já
  conhecido — mas exatamente PORQUE o teste do gatilho 4 da Seção 6 só
  olha o padrão agregado, ele não tem sensibilidade para detectar a
  heterogeneidade que (d) revela.
- (d) é o achado decisivo: não é mais uma explicação "parcial e
  insuficiente" como (a)/(c) — é uma demonstração direta, com IC bootstrap
  excluindo zero, de que o mecanismo de correção pré-registrado (um único
  `f_multi`) deixa um confundidor real e substancial sem corrigir num
  subgrupo não-trivial da amostra (19%). Isto por si só já basta para
  que `BOTH_FALSIFIED` não seja aceito como está — os itens (a)/(c) são
  reforço adicional, não a base principal do meu julgamento.

**O que este relatório NÃO conclui:** não estou afirmando que $a_0^A$ ou
$a_0^B$ sejam verdadeiros, nem que exista sinal MOND real nesta amostra —
apenas que a medição específica deste Estágio (`a0_fit` e seu IC),
condicionada a um `f_multi` único mal especificado para a heterogeneidade
real da amostra, não é confiável o suficiente para sustentar uma
falsificação limpa de nenhuma das duas hipóteses por este canal. Uma
melhoria genuína de metodologia (calibrar `f_multi` condicionalmente a
RUWE ou a outra variável de qualidade astrométrica, em vez de um único
escalar; ou excluir explicitamente o subgrupo RUWE-alto e reportar
separadamente) poderia, em uma tentativa futura, produzir uma medição mais
confiável — mas isso é trabalho de pré-registro futuro, fora do escopo
deste relatório adversarial.

**Linguagem apropriada para catalogação** (`AGENTS.md` Proibições —
nunca "Tamesis confirmado/refutado"): "Estágio 2 de `SPARC-FMULTI` produziu
um veredito mecânico `BOTH_FALSIFIED`, mas a reexecução adversarial e o
debunker de descoberta de nulos encontraram um confundidor real e
estatisticamente robusto (heterogeneidade RUWE-correlacionada não
capturada pelo modelo de `f_multi` único) plausivelmente suficiente para
produzir o padrão observado sem física Tamesis — mesmo padrão de decisão
já usado para fechar as versões v1/v2 deste teste. Fechado
`CLOSED_INCONCLUSIVE`."

---

## 4. Arquivos produzidos por esta sessão

- `analysis/adversarial_driver_stage2.py` — driver independente da Parte 1
  (reprodução), escrito do zero a partir do pré-registro.
- `analysis/debunker_quality_cuts_and_ruwe.py` — investigação da Parte 2,
  itens (a) e checagem RUWE (d).
- `results/result_adversarial_stage2.json` — resultado numérico completo
  da Parte 1.
- `results/adversarial_stage2_run.log` — log de execução da Parte 1.
- `results/result_debunker_quality_cuts_ruwe.json` — resultado numérico
  completo da Parte 2 (item a + checagem RUWE).
- `ADVERSARIAL_DEBUNKER_REPORT.md` — este documento.

**Não modificados por esta sessão** (integração é responsabilidade da
sessão orquestradora, conforme mandato): `PREREGISTRATION_STAGE2.md`,
`RESULTS_PRIMARY_STAGE2.md`, `00_GOVERNANCE/DECISION_LEDGER.yaml`,
`01_PORTFOLIO/TEST_QUEUE.yaml`, `00_GOVERNANCE/CLAIM_LEDGER.yaml`. Holdout
selado (12.944 sistemas) nunca acessado, sob nenhuma forma, por nenhum
script desta sessão.

## 5. Limitações desta investigação

- A checagem RUWE (Seção 2.4) usa `N_bootstrap=500` (exploratório, não os
  `2000` do protocolo pré-registrado) — suficiente dado o tamanho do
  efeito, mas não uma reexecução no mesmo padrão de precisão da análise
  principal.
- Não tentei recalibrar `f_multi` condicionalmente a RUWE (ex. dois
  parâmetros, ou uma covariável contínua) — isso seria uma mudança de
  metodologia pré-registrada, fora do escopo de um papel adversarial
  (que não pode reformular o método, só testá-lo/refutá-lo).
- O baseline populacional pré-corte do item (a) vem de literatura externa
  (Lindegren 2018, Chae 2023, El-Badry+2021), não de `catalog.parquet`
  bruto desta linha especificamente — decisão deliberada de não abrir
  esse arquivo (Seção 1.2). Um agente futuro com autorização explícita
  para abrir `catalog.parquet` (que não é o holdout selado, mas contém
  fisicamente os mesmos sistemas do holdout, sem rótulo) poderia refinar
  esta estimativa com o baseline exato desta linha específica, se a sessão
  orquestradora julgar isso necessário e autorizar explicitamente.
- Não investiguei a causa raiz exata do RUWE alto (companheira oculta
  genuína vs. outro artefato astrométrico) — ambas as interpretações
  sustentam a mesma conclusão de debunker (confundidor convencional não
  modelado), mas distingui-las exigiria dado adicional (ex. espectroscopia
  de velocidade radial, catálogo de multiplicidade dedicado) fora do
  escopo desta sessão.
