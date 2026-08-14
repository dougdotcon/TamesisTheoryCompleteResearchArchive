# Pré-registro: réplica independente do veredito de SPARC-002 via binárias largas reais do Gaia

**Status:** LOCKED
**Data de criação:** 2026-08-14
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-14 (Claude Code)
**Test ID:** `DISC-COSMOLOGY-MOND-SPARC-003`
**Commit em que foi travado:** ver histórico git do commit que introduz este arquivo.

> Preenchido e commitado ANTES de calcular qualquer razão de velocidade ou
> ajustar `a0` a partir do dado real. O split discovery/holdout
> (`data/discovery_holdout_split.json`) e os cortes de qualidade
> (`analysis/apply_quality_cuts.py`, `analysis/generate_split_and_bins.py`)
> já foram aplicados — mas usam SOMENTE variáveis preditoras (massa
> derivada de fotometria, separação projetada) para filtrar a amostra e
> definir bordas de bin, NUNCA a proveniência de movimento próprio/
> velocidade que entra na estatística de teste (Seção 4). Nenhuma razão
> de velocidade observada foi calculada antes deste lock.

## 0. Por que este teste existe

`DISC-COSMOLOGY-MOND-SPARC-002` (`02_TESTS/COSMOLOGY_A0_DERIVATION/`)
testou duas derivações internas conflitantes de `a0` (Seção 1 abaixo)
contra curvas de rotação SPARC reais. Na amostra de descoberta (120
galáxias), H_A sobreviveu e H_B foi falsificada; o Gate de Replicação
(holdout de 55 galáxias, terceiro agente independente) **não confirmou**
esse resultado — `g-dagger` no holdout saiu muito diferente, IC largo
demais para distinguir as duas hipóteses (`REPLICATION_FAILED_INCONCLUSIVE`).

Uma Fase 0 de busca (`02_TESTS/COSMOLOGY_WIDE_BINARIES/phase0/PHASE0_SEARCH.md`,
2026-08-14) não encontrou nenhuma alegação Tamesis-específica genuinamente
nova além das duas já testadas em SPARC-002 — toda fórmula adicional no
corpo teórico reproduz exatamente MOND padrão ou já foi auto-refutada.
A rota recomendada, adotada aqui: tratar SPARC-003 como uma **réplica
independente** do veredito ainda inconclusivo de SPARC-002, usando um
sistema físico completamente diferente de curvas de rotação — binárias
largas Keplerianas do Gaia — para responder à mesma pergunta com um
canal observacional que nunca foi tocado por SPARC-001 nem SPARC-002.

**Achado de integridade colateral** (não parte deste teste, registrado em
`TEST_QUEUE.yaml` campo `achado_de_integridade`):
`01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE/lab_gravity/analysis/gaia_real_analysis.py`
contém uma tabela de binárias largas rotulada como dado real do
El-Badry+2021 mas com `source_id` sequenciais/artificiais e progressão de
velocidade monotônica demais — dado fabricado. Este pré-registro usa o
catálogo El-Badry, Rix & Heintz (2021) **real**, baixado e verificado
nesta sessão (Seção 2), não a tabela fabricada.

## 1. Hipótese exata (idêntica a SPARC-002, não reformulada)

- **H_A:** o valor de `a0` que melhor ajusta a razão de velocidade das
  binárias largas (Seção 4) é estatisticamente compatível (dentro do
  intervalo de confiança bootstrap de 95%, Seção 4) com
  $a_0^A = cH_0/(2\pi) \approx 1{,}0823\times10^{-10}$ m/s² ("Ponte
  Holográfica").
- **H_B:** o mesmo `a0` ajustado é compatível com
  $a_0^B = cH_0 \approx 6{,}8002\times10^{-10}$ m/s² ("MOND Emergence").
- Mesmos valores exatos de $H_0=70$ km/s/Mpc, mesma fórmula, já travados
  em `DISC-COSMOLOGY-MOND-SPARC-002` — recalculados nesta sessão
  (`analysis/generate_split_and_bins.py`) e conferindo dígito a dígito:
  $a_0^A=1{,}082288\times10^{-10}$, $a_0^B=6{,}800218\times10^{-10}$.
- Este teste NÃO redefine H_A/H_B — apenas aplica o mesmo critério de
  decisão a um observável discriminador adaptado ao novo sistema físico
  (Seção 4), conforme `METHODOLOGY_EXTENSIONS.md` Seção 1 permite.

## 2. Fonte de dado

- **Catálogo:** El-Badry, Rix & Heintz (2021), MNRAS 506, 2269 —
  binárias largas do Gaia EDR3, 1.817.594 pares. Baixado por completo
  nesta sessão: `https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/catalog.dat.gz`
  (1.937.351.290 bytes = 100% do Content-Length declarado, sha256
  `0be0f09484ad7279e00ec5a97655c94dfb7377cdadd795a91978941112910f6f`,
  verificado duas vezes de forma independente, `gzip -t` confirmou
  integridade). ReadMe oficial baixado e parseado programaticamente
  (217 colunas, largura exata batendo com Lrecl=2844 declarado).
  Proveniência completa em `data/PROVENANCE.md`. Contagem de linhas
  (1.817.594) bate exatamente com o abstract do paper.
- **Cortes de qualidade** (sourced de Chae 2023 ApJ 952,128,
  arXiv:2305.04613, e Chae 2023 arXiv:2309.10404 — ambos baixados e lidos
  por completo nesta sessão, não assumidos de memória):
  - `BinType == "MSMS"` (ambas componentes sequência principal).
  - `R < 0,01` (probabilidade de alinhamento casual, El-Badry+2021 §3.2
    Eq. 8 — verificado por fetch direto).
  - `200 < sepAU < 30.000` (separação projetada, AU).
  - Distância heliocêntrica média `< 200` pc.
  - Concordância de distância: $|d_A-d_B| < 3\sqrt{\sigma_{d_A}^2+\sigma_{d_B}^2}$.
  - Erro relativo de movimento próprio `< 0,01` em ambas componentes.
  - Magnitude absoluta Gaia G de ambas componentes: $4 < M_G < 14$.
  - **Desvio declarado do corte exato de Chae:** Chae usa `RUWE<1,2`
    como corte adicional (Artigo B, item 1) e um corte de erro de
    paralaxe relativo separado; este pré-registro NÃO aplica RUWE nem
    corte de paralaxe separado (o corte de concordância de distância já
    absorve grande parte do mesmo efeito). Declarado aqui como
    simplificação honesta, não escondida.
  - Amostra resultante após todos os cortes E interpolação de massa bem
    sucedida: **43.147 sistemas** (`analysis/apply_quality_cuts.py`,
    executado nesta sessão, script commitado).
- **Massa estelar** (catálogo NÃO traz massa diretamente — confirmado
  por busca em todas as 217 colunas): derivada via magnitude absoluta
  Gaia G ($M_G = G - 5\log_{10}(d_{pc}) + 5$) interpolada linearmente na
  relação massa-luminosidade de Pecaut & Mamajek (2013, ApJS 208, 9),
  tabela atualizada de Eric Mamajek baixada diretamente de
  `https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt`
  nesta sessão (72 pontos válidos com `M_G` e `Msun` tabelados,
  B3V–L2V, cobrindo folgadamente a faixa $4<M_G<14$ exigida pelo corte
  de qualidade). Tabela salva em `data/mamajek_mass_luminosity.tsv`.
  **Desvio declarado:** Chae (2023) usa um polinômio de grau 10 próprio
  (Tabela 1 do Artigo A) ajustado à mesma tabela-fonte; este pré-registro
  usa interpolação linear direta na tabela de Mamajek em vez de
  reproduzir o polinômio exato de Chae (cujos coeficientes não foram
  extraídos por completo na verificação desta sessão) — mesma fonte
  primária, método de interpolação mais simples, declarado
  explicitamente.
- **Split discovery/holdout:** gerado nesta sessão com seed determinístico
  `20260814` (data de lock), `numpy.random.default_rng(20260814).shuffle`
  sobre os 43.147 sistemas pós-corte, 70% (**30.203**) para descoberta,
  30% (**12.944**) para holdout. Lista exata (por par `Source1_Source2`)
  em `data/discovery_holdout_split.json`. **O holdout permanece selado
  até o Gate de Replicação** — nenhuma análise deste pré-registro pode
  tocá-lo.
- **Bordas de bin** (definidas SOMENTE a partir de `Mtot_Msun` e `sepAU`
  da amostra de descoberta — nunca de movimento próprio/velocidade):
  5 bins de quantil igual em $\log_{10}(g_N)$, $g_N \equiv GM_{tot}/s^2$
  (SI), calculados sobre os 30.203 sistemas de descoberta:
  `[-11,7012; -9,1728; -8,4667; -7,9752; -7,5548; -6,5224]`
  (~6.040-6.041 sistemas por bin). Note que $\log_{10}(a_0^A)=-9,9657$
  cai dentro do bin 1 (o de menor aceleração, onde o efeito MOND deveria
  ser mais forte) e $\log_{10}(a_0^B)=-9,1675$ cai bem próximo da borda
  entre os bins 1 e 2 — ambos os valores candidatos estão cobertos pela
  faixa de dado disponível, dando poder genuíno ao teste.

## 3. Modelo nulo / hipótese concorrente

Mesmo papel que em SPARC-002: não há um "nulo" único no sentido do
piloto — é um teste de consistência interna entre H_A e H_B, calibrado
contra dado real de um canal físico independente. Checagem de sanidade
(não afeta o veredito H_A/H_B): o `a0` ajustado deve estar em ordem de
grandeza compatível com o valor de literatura padrão MOND
$a_0\approx1,2\times10^{-10}$ m/s² (McGaugh et al. 2016) — se sair muito
diferente (ex. por mais de uma ordem de grandeza), é sinal de erro de
implementação, e o teste para até isso ser resolvido, antes de aceitar
qualquer veredito H_A/H_B.

## 4. Estatística de teste

**Observável discriminador** (adaptado do método de perfil de
velocidade empilhada de Chae 2023, Artigo B Seção 4.2 — declarado como
simplificação do método primário de Chae, que usa desprojeção 3D via
Monte Carlo orbital com excentricidades individuais de Hwang et al. 2022,
não reproduzida aqui por depender de uma fonte externa não verificada
nesta sessão; a estatística projetada é tratada por Chae como checagem
de robustez, não como método principal — mas é real, publicada, e usada
por trabalhos anteriores como Pittordis & Sutherland 2018 e Banik & Zhao
2018):

1. Para cada sistema $i$ da amostra de descoberta:
   - $\Delta\mu_i = \sqrt{(\text{pmRA}_{1i}-\text{pmRA}_{2i})^2 +
     (\text{pmDE}_{1i}-\text{pmDE}_{2i})^2}$ (mas/yr).
   - $v_{p,i}^{\text{obs}} = 4{,}74047\times10^{-3} \cdot \Delta\mu_i \cdot
     \bar d_i$ (km/s, $\bar d_i$ = distância média do par em pc) — fórmula
     de Chae (2023), Artigo A, Eq. 4, verificada por fetch direto.
   - $g_{N,i} = GM_{tot,i}/s_i^2$ (aceleração Newtoniana projetada, SI).
   - $v_{p,i}^{N} = \sqrt{GM_{tot,i}/s_i}$ (velocidade circular Newtoniana
     projetada, SI).
2. Para cada um dos 5 bins de $\log_{10}(g_N)$ (bordas fixadas na Seção
   2): mediana empírica de $v_{p}^{\text{obs}}/v_{p}^{N}$ sobre os
   sistemas do bin.
3. Modelo MOND previsto por bin, usando a MESMA função de interpolação
   "simple" já travada em SPARC-002 (McGaugh, Lelli & Schombert 2016),
   agora aplicada em espaço de velocidade em vez de aceleração — sem
   reformular a função:
   $$\frac{v_p^{\text{MOND}}}{v_p^N}(a_0) = \left(1-e^{-\sqrt{g_{N,\text{bin}}/a_0}}\right)^{-1/2}$$
   onde $g_{N,\text{bin}}$ é a mediana de $g_N$ dentro do bin.
4. Ajuste não-linear de mínimos quadrados de $a_0$ (único parâmetro
   livre) entre as 5 razões medianas empíricas (passo 2) e o modelo
   (passo 3).
5. Intervalo de confiança de 95% em $a_0$ via bootstrap por sistema
   (reamostragem com reposição dos 30.203 sistemas de descoberta, 1000
   réplicas; para cada réplica, os sistemas são re-binados usando as
   MESMAS bordas fixas da Seção 2 — nunca rebinado por quantil da
   réplica — medianas e ajuste de $a_0$ recalculados).
6. Verificar se $a_0^A$ e/ou $a_0^B$ caem dentro do IC de 95%.

## 5. Critério de falsificação

- **H_A falsificada** se $a_0^A\approx1,0823\times10^{-10}$ estiver fora
  do IC de 95% do $a_0$ ajustado.
- **H_B falsificada** se $a_0^B\approx6,8002\times10^{-10}$ estiver fora
  do IC de 95%.
- Se apenas uma sobreviver: suporte a essa derivação especificamente,
  independentemente do canal SPARC — achado mais forte que SPARC-002
  sozinho, por vir de um sistema físico completamente diferente.
- Se nenhuma sobreviver: ambas as derivações internas são falsificadas
  por este canal independente — resultado válido e informativo.
- Se as duas sobreviverem: IC largo demais para distinguir — INCONCLUSIVO
  quanto à escolha entre A e B (mesmo veredito possível de SPARC-002).

## 6. Correção para comparações múltiplas

Duas hipóteses pré-registradas (H_A, H_B) testadas contra o mesmo IC de
um único ajuste agregado de 5 bins — não há busca sobre número de bins,
cortes de qualidade alternativos, ou outras estatísticas além das já
declaradas nesta seção. Nenhuma correção de Bonferroni/FDR aplicável além
de declarar explicitamente que são duas hipóteses, não uma.

## 7. O que NÃO está sendo testado

- Isto NÃO testa "Tamesis vs. ΛCDM" nem "Tamesis vs. MOND padrão" — ambas
  H_A e H_B são internas a Tamesis (Tamesis já reduz a MOND padrão neste
  domínio, ver `PHASE0_SEARCH.md` Rota 2).
- Isto NÃO reproduz o teste de Chae (2023) em si (Newton puro vs.
  AQUAL/EFE, $\gamma_g\approx1$ vs. $\approx1,4$) — usa a mesma fonte de
  dado e uma estatística projetada simplificada derivada do mesmo campo,
  mas para uma pergunta diferente (qual valor de $a_0$, não se há quebra
  de gravidade).
- Um resultado aqui NÃO decide entre MOND e matéria escura, nem resolve
  sozinho o veredito de SPARC-002 — é uma réplica de canal independente,
  registrada com seu próprio peso evidencial, a ser combinada
  qualitativamente (não estatisticamente fundida) com o resultado já
  registrado de SPARC-002.
- Nenhum resultado implica progresso em qualquer Problema do Millennium.
- O holdout (12.944 sistemas) só é aberto no Gate de Replicação — a
  análise desta sessão (descoberta, 30.203 sistemas) não decide sozinha
  o veredito final; é `ANALYZED`, não `REPLICATION_PASSED`.
- Não corrige nem usa o dado fabricado de `gaia_real_analysis.py` (Seção
  0) — esse achado de integridade é reportado separadamente, fora do
  escopo deste teste.

---

## [Preenchido depois da análise] Resultado

Analisados os 30.203 sistemas de descoberta (holdout de 12.944 nunca
lido além da contagem). Bordas de bin fixas reutilizadas sem alteração;
contagens por bin: 6042/6040/6040/6039/6042. `a0_A` e `a0_B`
recalculados batem dígito a dígito com os valores da Seção 1.

**5 medianas empíricas de $v_p^{\text{obs}}/v_p^N$ por bin (log$_{10}(g_N)$
crescente):** `0,6932; 0,6409; 0,6243; 0,6150; 0,5941` — **todas abaixo
de 1**.

**Checagem de convergência do ajuste (Seção 4, passo 4): FALHOU.**
$a_0$ ajustado a partir de $x_0=1$: $5,047\times10^{-13}$ m/s²; a partir
de $x_0=5$: $4,242\times10^{-13}$ m/s² — diferem ~16%, não convergem ao
mesmo valor.

**Checagem de sanidade (Seção 3): FALHOU.** $a_0$ ajustado
(~$5\times10^{-13}$) está ~2,4 ordens de grandeza abaixo do valor de
referência McGaugh ($1,2\times10^{-10}$) — muito além da tolerância de
1 ordem de grandeza declarada.

**Causa raiz identificada (não é erro de implementação — verificado por
fórmulas conferidas termo a termo, spot-check manual de sistemas
individuais, e confirmação independente por Monte Carlo — ver Veredito
adversarial abaixo):** o modelo MOND "simple" em espaço de velocidade,
$(1-e^{-\sqrt{g_N/a_0}})^{-1/2}$, tem imagem estritamente em
$(1,+\infty)$ para qualquer $a_0>0$ finito. As 5 medianas empíricas são
todas $<1$. Não existe $a_0$ que faça o modelo alcançar o alvo — o
ajuste é estruturalmente mal-condicionado (sem mínimo interior),
explicando tanto a não-convergência quanto a falha de sanidade. Causa
provável: diluição por projeção, já antecipada no preâmbulo da Seção 4
como limitação declarada da estatística simplificada (em vez do método
de desprojeção 3D completo de Chae).

**Por instrução explícita da própria Seção 3 deste pré-registro** ("se
não estiver [em ordem de grandeza compatível]... o teste para até isso
ser resolvido, antes de aceitar qualquer veredito H_A/H_B"): **nenhum
veredito H_A/H_B é aceito a partir deste resultado.** O critério
literal da Seção 5, aplicado mecanicamente, produziria `BOTH_FALSIFIED`
— mas isso não é lido como evidência real contra $a_0^A$ ou $a_0^B$,
por não haver poder de discriminação genuíno na estatística como
pré-registrada (ver diagnóstico completo abaixo).

Resultado completo:
`analysis/result_primary.json`. Script: `analysis/run_preregistered_analysis.py`.

## [Preenchido depois da reexecução adversarial] Veredito adversarial

Reexecução independente (agente separado, implementação escrita do
zero a partir SOMENTE deste `PREREGISTRATION.md`, sem ler
`run_preregistered_analysis.py` nem `result_primary.json` antes de ter
seu próprio resultado pronto).

**Concordância bit a bit em toda a parte determinística:** contagens
por bin, medianas de `g_N` e de razão por bin, ambos os ajustes de
$a_0$ ($x_0=1$ e $x_0=5$), a magnitude da falha de sanidade, e
$a_0^A$/$a_0^B$ — idênticos entre as duas implementações. **Nenhum bug
de fórmula, unidade, constante ou binagem encontrado em nenhum dos dois
scripts.**

IC bootstrap divergiu inicialmente entre os dois agentes por uma
**ambiguidade textual não coberta pelo pré-registro** (se a checagem de
convergência dupla de $a_0$ deve ser reaplicada a cada réplica de
bootstrap ou só ao ajuste agregado primário) — não um bug; as duas
políticas foram testadas e documentadas lado a lado em
`result_adversarial.json`, ambas levando ao mesmo veredito qualitativo.

**Confirmação independente adicional, decisiva:** o agente adversarial
rodou uma simulação de Monte Carlo própria ($N=200.000$) de binárias
Keplerianas **puramente Newtonianas** (excentricidade térmica
$f(e)=2e$, orientação isotrópica, fase orbital uniforme — nenhuma
física MOND envolvida) e obteve mediana$(v_{\text{proj}}/v_{\text{circ}})
\approx 0,55$ — mesma ordem de grandeza das medianas $<1$ observadas no
dado real. Isso é o efeito de diluição por projeção já documentado na
literatura (Pittordis & Sutherland 2018; Banik & Zhao 2018) e confirma
que valores de razão $<1$ são esperados por geometria de projeção
sozinha, independentemente de qualquer física de $a_0$.

**Veredito adversarial final:** o critério literal da Seção 5 produz
`BOTH_FALSIFIED` nos dois scripts, mas essa conclusão é **cientificamente
vazia** — a estatística projetada simplificada, como pré-registrada na
Seção 4, não tem poder de discriminação genuíno entre H_A e H_B (nem
entre nenhum valor de $a_0$) neste canal de dado, por incompatibilidade
estrutural entre a imagem do modelo e o efeito de diluição por
projeção. **Isto deve ser registrado como uma limitação estrutural do
desenho do teste pré-registrado — não como uma réplica válida do
veredito de SPARC-002.** Holdout (12.944 sistemas) confirmado intocado
pelos dois agentes — permanece selado, disponível para um teste futuro
genuinamente redesenhado (ex. com desprojeção Monte Carlo completa).

Resultado completo: `analysis/result_adversarial.json`. Script:
`analysis/adversarial_reproduction.py`.
