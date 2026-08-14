# Nota de metodologia — reformulação e fechamento dos 3 gaps de `dfa-multiscale-entropy`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo FINAL
de `Delta alpha` nos 2 domínios (fisiologia/apneia, PhysioNet Apnea-ECG;
paleoclima/GISP2). Mesmo espírito de disciplina já usado para
`critical-slowing-down` (`../critical_slowing_down/METHODOLOGY_NOTE.md`) e
`wavelet-multiresolution-scaling` (`../wavelet_multiresolution/METHODOLOGY_NOTE.md`).

## Contexto: por que este candidato está sendo retestado

A Fase 0 (`../phase0/PHASE0_SURVEY.md`, candidato 3) rebaixou
`dfa-multiscale-entropy` porque os 2 domínios usados então (PhysioNet
saudável-vs-ICC; NOAA continental-vs-oceânico) eram comparações ESTÁTICAS
de classe entre sujeitos/sistemas diferentes, não transições temporais
dentro do mesmo sistema — a exigência central de `DISC-TRI-RG-001`. Um
agente de busca dedicado (após `DISC-DEC-005` ser revertida a pedido do
usuário, "retome a linha DISC-TRI-RG-001") encontrou um domínio fisiológico
com transição genuína: **PhysioNet Apnea-ECG Database, registro `a04`**
(paciente com AHI=77,4, apneia severa documentada por Thomas Penzel) — 35
min contínuos de respiração normal seguidos imediatamente por 140 min
contínuos de apneia/hipopneia, dentro do mesmo registro do mesmo paciente
na mesma noite, com rótulo minuto-a-minuto de fonte clínica EXTERNA (escore
humano de sinais respiratórios/SpO2, independente do próprio ECG).
Registros de backup no mesmo banco (`a18`, `a14`, `a01`) mapeados para
replicação futura.

Um teste de viabilidade EXPLORATÓRIO (pipeline própria não validada, regra
de janela ad hoc = exatamente os limites do rótulo clínico, sem robustez)
já foi rodado pelo agente de busca sobre `a04`: alpha(PRE)=1,133,
alpha(POST completo)=0,840, alpha(POST truncado ao tamanho do PRE)=0,929.
**Isto NÃO é o resultado final** — é equivalente ao mesmo tipo de checagem
de viabilidade que a Fase 0 original já fez para os outros candidatos antes
de qualquer fechamento de gaps (ex. CSD's Fase 0 só verificou acesso ao
dado, não `Delta I`; aqui a verificação foi um pouco além, computando um
`alpha` de fato, mas com pipeline não validada e regra de janela não fixada
a priori). O cálculo que conta para o veredito desta linha é o que segue
abaixo, com pipeline validada contra dado sintético e regra fixada ANTES do
cálculo final.

## Escolha de segundo domínio: paleoclima GISP2 (reaproveitado de `critical-slowing-down`)

Para satisfazer a exigência CROSS-DOMAIN de `DISC-TRI-RG-001` (a mesma
fórmula `I(X)`, sem reformulação, em sistemas fisicamente distintos), o
segundo domínio é o núcleo de gelo GISP2 (NOAA/Alley 2000) já baixado e
verificado para `critical-slowing-down`
(`../critical_slowing_down/analysis/result_gisp2.json`), mesma transição
Younger Dryas→Preboreal (~11,5 kyr BP), mesmos dados brutos, mesma
definição operacional de fronteira de transição (`Age > 11.5 kyr BP`
estritamente). Isto reaproveita infraestrutura já verificada em vez de
gastar uma nova busca/download — o dado é genuinamente diferente do domínio
fisiológico (temperatura/acumulação de gelo vs. intervalos R-R cardíacos),
o que é exatamente o tipo de par cross-domain que esta linha pede.

## Gap (a): regra de escala DFA (`R_lambda`)

**Decisão:** procedimento DFA de ordem 1 padrão (Peng et al. 1994 *Phys.
Rev. E* 49:1685; 1995 *Chaos* 5:82-87 — batimento cardíaco):

1. Série `x` (intervalos RR ou valores de temperatura, já em ordem
   cronológica) → série integrada `y(k) = sum_{i=1}^{k} (x_i - mean(x))`.
2. Dividir `y` em blocos NÃO sobrepostos de tamanho `n`; ajustar tendência
   linear (ordem 1) local em cada bloco; `F(n) = sqrt(media sobre blocos da
   media do quadrado do resíduo)`.
3. `alpha` = inclinação da regressão `log F(n)` vs. `log n`.

**Faixa de escala (fração adimensional do comprimento do segmento, mesma
convenção de `critical-slowing-down` — nunca unidade física absoluta, já
que os dois domínios têm grades de amostragem incomparáveis: ~1 amostra/
batimento cardíaco vs. amostras de gelo espaçadas irregularmente em kyr):

- `n_min = 4` (mínimo padrão da literatura para ajuste linear estável de
  ordem 1 — Peng et al.; não ajustado por domínio).
- `n_max_frac = 0.25` → `n_max = floor(0.25 * N)` (convenção padrão que
  garante pelo menos 4 blocos não sobrepostos na escala mais grosseira).
- `N_SCALES = 20` valores de `n`, log-espaçados entre `n_min` e `n_max`,
  arredondados para inteiros únicos.

**Canais reportados (companheiros, mesmo espírito do par AC1/variância de
CSD e ΔC1/ΔC2 de wavelet):**
- `alpha` (principal): regressão sobre TODA a faixa `[n_min, n_max]`.
- `alpha1` (curto prazo): regressão sobre `[n_min, 16]`.
- `alpha2` (longo prazo): regressão sobre `[16, n_max]`, só reportado se
  `n_max >= 16` (caso contrário, reportado como indefinido, nunca
  substituído silenciosamente). `n_split = 16` é convenção fixada a priori
  da literatura de HRV (Peng et al.; Iyengar et al. 1996), não escolhida
  depois de ver o resultado.

`Delta alpha = alpha(POST) - alpha(PRE)`, e igualmente `Delta alpha1`,
`Delta alpha2`.

## Gap (b): definição de segmento PRE/POST (regra domain-agnostic)

Regra EXATAMENTE reaproveitada de `critical-slowing-down` (que já resolveu
o mesmo problema de domínios com densidade de amostragem incomparável —
GISP2 kyr-scale vs. ECG batimento-a-batimento):

- **PRE (primária):** todo o registro contínuo disponível anterior ao
  limite documentado da transição.
- **PRE (robustez):** os 50% mais recentes (mais próximos da transição)
  desse mesmo segmento primário.
- **POST (primária):** todo o registro contínuo disponível posterior ao
  limite documentado da transição, até o próximo evento/rótulo documentado
  que encerraria essa mesma condição (para apneia: até o próximo rótulo `N`
  na sequência clínica; para GISP2: até a amostra mais recente disponível
  no registro, já que não há evento intermediário documentado nesta sessão
  entre o Preboreal e o presente).
- **POST (robustez):** os 50% mais próximos da transição desse mesmo
  segmento primário.

Aplicada sem ajuste nos 2 domínios:
- **Apneia-ECG (`a04`):** PRE = 35 min N (2.747 intervalos RR), POST = 140
  min A contínuos (9.195 intervalos RR) — mesmos limites já mapeados pelo
  agente de busca via rótulo clínico oficial.
- **GISP2:** PRE = todas as amostras com `Age > 11.5 kyr BP` (764 amostras,
  idêntico ao segmento primário já usado em `critical-slowing-down`). POST
  = todas as amostras com `Age <= 11.5 kyr BP` até a amostra mais recente
  do registro (contagem exata a determinar na execução; mesma regra
  aplicada sem inspeção visual do resultado antes do cálculo).

**Limitação honesta declarada a priori:** apneia obstrutiva não é um evento
discreto único (como onset de FV ou início de crise) — é um processo
cíclico dentro do bloco POST (ciclos apneia→hipopneia→despertar a cada
~30-90s). Isto é reportado explicitamente, não escondido: é defensável
testar DFA sobre esse bloco (DFA é sensível a estrutura de correlação
multiescala, e a oscilação cíclica é um componente de escala adicional
genuíno), mas é uma diferença qualitativa em relação aos outros domínios já
testados nesta linha (que tiveram transições mais próximas de evento único).

## Gap (c): protocolo de dados substitutos

**Decisão:** IAAFT (Schreiber & Schmitz 1996), o MESMO método já usado em
`wavelet-multiresolution-scaling` — reaproveitar a ferramenta, não
reformular por domínio. `N_SURROGATES=200` pares (um substituto PRE, um
POST, gerados independentemente cada um a partir de sua própria série
real), `N_IAAFT_ITER=50`, semente fixa (`seed=12345`).

Para cada par `i`: `Delta alpha_substituto_i = alpha(substituto_POST_i) -
alpha(substituto_PRE_i)` (e igualmente para `alpha1`, `alpha2`), formando a
distribuição nula sob "nenhuma mudança genuína de estrutura de correlação
além do que um processo linear com o mesmo espectro/amplitude produziria".

**Teste BICAUDAL** (mesmo raciocínio de `wavelet-multiresolution-scaling`,
diferente do teste unicaudal de CSD): a literatura (Penzel et al. 2003)
documenta mudança de `alpha` com apneia, mas a direção reportada depende de
qual sub-banda/canal — não há uma previsão direcional única e verificada
nesta sessão a priori. Declarar bicaudal em vez de escolher a direção
depois de ver o resultado é a escolha honesta. `p = fração de substitutos
com |Delta alpha_substituto| >= |Delta alpha_real|` (e igualmente para
alpha1, alpha2).

**Checagem obrigatória de marginal degenerada (lição de governança
adicionada em `METHODOLOGY_EXTENSIONS.md` após o achado de
`wavelet-multiresolution-scaling`):** ANTES de aceitar qualquer `p` do
IAAFT como válido, reportar a razão max/min de cada segmento real (PRE e
POST, nos 2 domínios) e compará-la ao patamar ~190x que se mostrou
diagnóstico de falha do IAAFT no caso da cascata binomial. Se algum
segmento ultrapassar esse patamar, o `p` correspondente deve ser reportado
com a mesma ressalva já documentada (substitutos IAAFT podem não zerar a
estatística sob marginal degenerada/cauda pesada).

## Adendo ao Gap (c) — teste complementar de bootstrap por blocos (adicionado APÓS validação sintética, ANTES de qualquer dado real)

A validação sintética obrigatória (seção abaixo) revelou um problema
estrutural real com o teste IAAFT bicaudal especificado acima, não um bug:
o controle positivo (`PRE`=fGn `H=0,5`, `POST`=fGn `H=0,9`, mudança de
correlação inequívoca por construção) NÃO atingiu `p<0,05`
(`p_alpha=0,255`). Diagnóstico: substitutos IAAFT preservam o espectro de
amplitude EXATO de cada segmento real, e `alpha` do DFA é essencialmente
uma quantidade espectral/linear para um processo gaussiano autossimilar —
então o substituto do PRE reproduz um `alpha` quase idêntico ao `alpha`
real do PRE, e o mesmo para o POST, deixando a distribuição nula de `Delta
alpha` centrada quase exatamente no `Delta alpha` real. O teste IAAFT, como
especificado, responde a uma pergunta mais estreita ("há estrutura NÃO-
LINEAR além do espectro linear de cada segmento?"), não "há alguma mudança
de `alpha`?" — e é precisamente para isso que existe a etapa de validação
antes de tocar dado real (mesma disciplina de
`METHODOLOGY_EXTENSIONS.md` Seção 1, lição de `DISC-COSMOLOGY-MOND-SPARC-003`).

**Correção, fixada ANTES de qualquer cálculo em dado real:** adicionar um
segundo teste, complementar ao IAAFT (que continua sendo calculado e
reportado, pois responde a uma pergunta real e válida sobre estrutura não-
linear) — um teste de **bootstrap por blocos móveis** (moving-block
bootstrap, Künsch 1989), desenhado especificamente para testar se
`Delta alpha` excede a variabilidade de estimação de amostra finita, sem
depender de preservar o espectro (o problema do IAAFT aqui):

1. Para cada segmento (PRE e POST, independentemente), comprimento de bloco
   `L = n_max` daquele MESMO segmento (o maior `n` já usado na própria
   grade de escala DFA desse segmento — regra fixada a priori, ligada
   diretamente à análise, não um valor arbitrário) — blocos grandes o
   bastante para preservar a estrutura de correlação até a escala mais
   grosseira efetivamente medida.
2. Gerar `N_BOOTSTRAP=1000` reamostras por blocos móveis com reposição
   (blocos de tamanho `L`, início sorteado uniformemente, concatenados até
   igualar o comprimento original do segmento) de CADA segmento,
   independentemente. Semente fixa (`seed=12345`), reaproveitada da mesma
   convenção já usada nesta nota.
3. Computar `alpha` (mesma pipeline `compute_alphas`, sem modificação) em
   cada reamostra — dando duas distribuições bootstrap independentes,
   `alpha_boot_PRE` e `alpha_boot_POST`, cada uma com 1000 valores.
4. Parear a `i`-ésima reamostra do PRE com a `i`-ésima do POST (pareamento
   arbitrário entre distribuições independentes, convenção padrão de
   bootstrap de duas amostras) para formar `Delta alpha_boot_i =
   alpha_boot_POST_i - alpha_boot_PRE_i`, 1000 valores.
5. Reportar o intervalo percentílico de 95% de `Delta alpha_boot` (e
   `Delta alpha1_boot`, `Delta alpha2_boot`) e se ele exclui zero
   (bicaudal, mesmo espírito de "sem previsão direcional a priori" já
   declarado para o IAAFT); `p_bootstrap = 2 * min(fração de `Delta
   alpha_boot <= 0`, fração de `Delta alpha_boot >= 0`)`, construção padrão
   de p-valor percentílico bicaudal.

**Interpretação declarada a priori:** o veredito desta linha depende do
teste de bootstrap por blocos para a pergunta "há uma diferença real de
`alpha` maior que ruído de amostra finita?" — o IAAFT continua reportado
como checagem COMPLEMENTAR e mais estreita ("essa diferença reflete algo
além de estrutura linear/espectral?"), não como o teste principal, dado o
limite de poder já demonstrado na validação. Isto é análogo à lição já
registrada para `ΔC1` em `wavelet-multiresolution-scaling` ("provavelmente
reflete apenas amplitude, não estrutura genuína") — aqui, ao contrário, é o
teste original que se mostrou fraco demais, não o achado.

## Validação contra dado sintético (obrigatória ANTES do cálculo final real)

Pipeline nova (`analysis/dfa_common.py`, implementação limpa, não
reaproveitada de outro teste do laboratório) deve ser validada, nesta
ordem, ANTES de tocar qualquer segmento PRE/POST real dos 2 domínios:

1. Ruído branco (`alpha` teórico `~0,5`) e passeio aleatório (`alpha`
   teórico `~1,5`) — checagem de sanidade padrão.
2. Controle positivo sintético: PRE = ruído gaussiano fracionário (fGn,
   `H=0,5`), POST = fGn com `H` claramente diferente (ex. `H=0,9`) —
   pipeline deve detectar `Delta alpha` real fora da distribuição nula dos
   substitutos IAAFT (`p` pequeno).
3. Controle negativo: PRE e POST = fGn do MESMO `H`, sorteios
   independentes — `p` deve ser tipicamente não-significativo.
4. Checagem de marginal degenerada (lição do gap (c) acima): confirmar que
   nenhum dos controles sintéticos usados tem razão max/min patologicamente
   alta, e registrar a razão max/min de cada um para referência de
   comparação com o dado real.
5. Repetir os controles positivo e negativo (item 2 e 3) com o teste de
   bootstrap por blocos móveis do adendo acima, confirmando que ele
   recupera poder onde o IAAFT falhou (`p_bootstrap` pequeno no controle
   positivo H=0,5 vs H=0,9) e continua corretamente não-significativo no
   controle negativo (mesmo H, sorteios independentes).

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado. O número de viabilidade já visto (1,133/0,840/0,929) NÃO será
usado como resultado — o veredito desta linha depende exclusivamente do
cálculo feito com a pipeline validada e a regra de segmento fixada acima,
rodado depois deste commit.
