# Pré-registro: redesenho de SPARC-003 com desprojeção 3D via Monte Carlo (método primário de Chae 2023)

**Status:** LOCKED (2026-08-15). Travado após a revalidação obrigatória do
Adendo 4c (estatística `δ_obs-newt`) passar sob critério honesto (não
literal ingênuo): **controle negativo** (dois ensembles Newtonianos
sintéticos independentes) — os 5 ICs de 95% de `δ_obs-newt` contêm 0,
magnitudes pequenas (~0,02-0,07 dex, consistente com ruído puro).
**Controle positivo** (boost MOND injetado, $a_0^{\text{teste}}=1{,}2\times10^{-10}$
m/s²) — o sinal recuperado bate em sinal e magnitude com a previsão AQUAL
no único bin onde essa previsão é fisicamente detectável acima do piso
de ruído do método (bin de menor $g_N$, razão recuperado/previsto=1,44);
nos outros 4 bins a previsão AQUAL para esse `a0` de teste é desprezível
($\nu(g_N/a_0)\to1$), então "ruído recuperado ≈ ruído do controle
negativo" ali é o comportamento correto, não uma falha — confirmado
explicitamente via análise de piso de ruído
(`analysis/revalidation_delta_obs_newt.json`). Nenhuma razão de
aceleração REAL foi calculada antes deste lock — toda a revalidação usou
somente dado sintético dos dois lados (real E mock).

**Data de criação:** 2026-08-15
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-15 (Claude Code)
**Test ID:** `DISC-COSMOLOGY-MOND-SPARC-004`
**Commit em que foi travado:** ver histórico git do commit que muda `Status` para `LOCKED` neste arquivo.

## 0. Por que este teste existe

`DISC-COSMOLOGY-MOND-SPARC-003` (`02_TESTS/COSMOLOGY_WIDE_BINARIES/`) usou
o método SIMPLIFICADO de perfil de velocidade projetada (Chae 2023,
Artigo B, tratado por Chae como checagem de robustez, não como método
principal) — declarado explicitamente como simplificação do método
primário de Chae (desprojeção 3D via Monte Carlo orbital com
excentricidades individuais de Hwang, Ting & Zakamska 2022), que na época
foi considerado "tratável demais para reproduzir por depender de fonte
externa não verificada". Esse teste foi fechado `CLOSED_INCONCLUSIVE`:
o modelo MOND pré-registrado ($v_p^{\text{MOND}}/v_p^N$) tem imagem
matematicamente restrita a $(1,+\infty)$, mas as 5 medianas empíricas reais
eram todas $<1$ — ajuste de $a_0$ estruturalmente impossível, causado por
diluição por projeção (efeito geométrico conhecido, Pittordis & Sutherland
2018; Banik & Zhao 2018), não por erro de implementação (confirmado por
reexecução adversarial bit a bit e por simulação Monte Carlo independente).

Usuário pediu para redesenhar o teste usando o método primário completo.
Pesquisa dedicada nesta sessão (não memória) verificou o algoritmo exato
de Chae (2023), ApJ 952,128, arXiv:2305.04613v4 (LaTeX-fonte baixado e
lido linha a linha) e confirmou, por download e inspeção real, que o
catálogo eletrônico de excentricidades de Hwang, Ting & Zakamska (2022,
MNRAS 512,3383, arXiv:2111.01789 — **correção de citação**: a referência
originalmente presumida, "Hamers, Kratter & Shu", estava errada) está de
fato acessível (208 MB, FITS, 1.817.594 linhas — cobertura total do
catálogo El-Badry+2021, sha256 e formato verificados, ver
`data/PROVENANCE_HWANG.md`).

**Achado metodológico decisivo desta pesquisa:** o método primário de
Chae **não ajusta $a_0$ livre contra um modelo MOND** — usa uma
estatística estruturalmente diferente ($\delta_{\text{obs-newt}}$,
resíduo mediano de $\log g$ vs. $\log g_N$ DESPROJETADOS). Essa
estatística não sofre da restrição de imagem $(1,+\infty)$ que matou a
tentativa anterior: para órbitas excêntricas desprojetadas, $g/g_N$ pode
legitimamente cair abaixo de 1 mesmo sob MOND (o próprio Artigo A mostra
isso, Eq. 16 — "*for measured eccentricities of $e\gtrsim0,5$, it is
expected that $\log_{10}(g/g_N)\lesssim-0,1$*"). Adaptar essa estatística
para testar H_A/H_B especificamente (em vez do teste genérico de
"desvio de Newton" do Artigo A) exige uma extensão declarada — ver Seção 4.

## 1. Hipótese exata (idêntica a SPARC-002/003, NÃO reformulada)

- **H_A:** o `a0` que melhor explica a razão de aceleração desprojetada
  (Seção 4) é compatível (dentro do IC de 95%, Seção 4) com
  $a_0^A = cH_0/(2\pi) \approx 1{,}082288\times10^{-10}$ m/s² ("Ponte
  Holográfica").
- **H_B:** o mesmo `a0` é compatível com
  $a_0^B = cH_0 \approx 6{,}800218\times10^{-10}$ m/s² ("MOND Emergence").
- Mesmos valores exatos já travados em `DISC-COSMOLOGY-MOND-SPARC-002` e
  reaproveitados sem alteração em `SPARC-003` — este pré-registro NÃO
  redefine H_A/H_B, apenas adapta o observável discriminador ao método de
  desprojeção completo (`METHODOLOGY_EXTENSIONS.md` Seção 1 permite isso
  explicitamente).
- **Nota de identificabilidade honesta, carregada de SPARC-002/003 sem
  diluir:** $a_0^A=cH_0/(2\pi)$ reproduz uma coincidência numérica já
  conhecida na literatura MOND padrão (Milgrom, décadas antes de Tamesis,
  arXiv:2001.09729) — H_A sobreviver não é evidência de poder
  discriminativo específico de Tamesis, só consistência com um fato
  numérico pré-existente no campo. Esta ressalva se aplica igualmente
  aqui.

## 2. Fonte de dado (reaproveitada sem modificação de SPARC-003)

- **Catálogo El-Badry, Rix & Heintz (2021):** mesmo arquivo já baixado,
  verificado (sha256 `0be0f09484ad7279e00ec5a97655c94dfb7377cdadd795a91978941112910f6f`)
  e commitado em `../COSMOLOGY_WIDE_BINARIES/data/`. Reaproveitado por
  referência, não rebaixado.
- **Cortes de qualidade:** IDÊNTICOS aos já aplicados e commitados em
  `../COSMOLOGY_WIDE_BINARIES/analysis/apply_quality_cuts.py`
  (`BinType=MSMS`, `R<0,01`, `200<sepAU<30000`, distância `<200pc`,
  concordância de distância $3\sigma$, erro relativo de PM `<0,01`,
  $4<M_G<14$) — **43.147 sistemas** pós-corte, reaproveitados sem
  reexecução.
- **Split discovery/holdout:** IDÊNTICO, reaproveitado sem regeneração —
  `../COSMOLOGY_WIDE_BINARIES/data/discovery_holdout_split.json`
  (seed=20260814, 30.203 descoberta / 12.944 holdout selado). O holdout
  **permanece selado** — nenhuma análise deste pré-registro pode tocá-lo
  até o Gate de Replicação.
- **Massa estelar:** IDÊNTICA (interpolação linear em Pecaut & Mamajek
  2013, `../COSMOLOGY_WIDE_BINARIES/data/mamajek_mass_luminosity.tsv`).
- **NOVO — catálogo de excentricidades individuais** (Hwang, Ting &
  Zakamska 2022): baixado e verificado nesta sessão (208.220.480 bytes,
  sha256 `39c4db80e25a2c2ed553c3e51d81f285b4c876d970a02e8c66af180837e0d46a`,
  formato FITS, 1.817.594 linhas, 15 colunas batendo 100% com a Tabela 2
  do LaTeX-fonte do artigo). Colunas relevantes: `e` (excentricidade mais
  provável), `e0`/`e1` (limites do IC de 68%), `alpha` (índice da
  distribuição populacional $p(e;\alpha)=(1+\alpha)e^\alpha$ daquele par
  específico, já pré-computado por Hwang em função da separação — usado
  como fallback, ver Gap (a) abaixo). Cruzado com a amostra de 43.147
  sistemas via `(source_id1, source_id2)`. Proveniência completa em
  `data/PROVENANCE_HWANG.md`. **Apenas o subconjunto extraído para os
  43.147 sistemas é commitado no repositório** (o arquivo bruto de 208MB
  excede o limite prático de commit direto do GitHub — mesmo espírito já
  usado para os catálogos de binárias largas de SPARC-003, documentados
  por URL+sha256 em vez de commitados brutos).

## 3. Modelo nulo / hipótese concorrente

Mesmo papel que em SPARC-002/003: teste de consistência interna entre
H_A e H_B contra um canal físico independente, não um teste de "MOND vs.
Newton puro" no sentido do Artigo A original de Chae. Checagem de
sanidade adicional (Gap de identificabilidade já levantado por
`METHODOLOGY_EXTENSIONS.md` Seção 1 após o achado de SPARC-003): a
validação sintética da Seção 4b, obrigatória ANTES do lock, verifica que
a estatística escolhida ($g/g_N$ desprojetado) não está estruturalmente
impedida de cobrir os valores mundanos plausíveis (Newtoniano puro,
$g/g_N=1$) nem os valores previstos por H_A/H_B.

## 4. Estatística de teste — desprojeção 3D via Monte Carlo (método primário de Chae 2023, com uma simplificação declarada)

### Gap (a): amostragem de excentricidade por sistema

Para cada sistema $i$ da amostra de descoberta:
1. Se o par tiver entrada no catálogo de Hwang com `e`/`e0`/`e1` não-NaN
   **E** `dpm_sig > 3` (critério do próprio Chae/Hwang para
   confiabilidade da excentricidade individual, Seção 3.1 do Artigo A,
   verificado por leitura direta do LaTeX-fonte): amostrar $e$ de uma
   Gaussiana truncada em $[0{,}001;\,0{,}999]$, centrada em `e` (mediana),
   com $\sigma = e1-e$ se a amostra cair acima da mediana, $\sigma=e-e0$
   se cair abaixo — mesma regra exata declarada por Chae (Artigo A,
   linha 506, citação literal já verificada nesta sessão).
2. Caso contrário (par ausente do catálogo de Hwang, `dpm_sig≤3`, ou
   `e≥0,99` — os mesmos casos-limite que o próprio Chae trata via
   fallback, ~15-18% da amostra dele): amostrar $e$ da distribuição
   populacional $p(e;\alpha_i)=(1+\alpha_i)e^{\alpha_i}$, usando o valor
   de `alpha` JÁ TABULADO por Hwang para aquele par específico (não
   recalculado por uma fórmula própria — evita ambiguidade entre duas
   parametrizações conflitantes encontradas por agentes diferentes
   nesta sessão durante a pesquisa de verificação; usar o valor já
   presente no catálogo elimina essa ambiguidade).

### Gap (b): graus de liberdade orbitais marginalizados (idêntico a Chae, Eqs. 7-10 do Artigo A)

- Inclinação $i \sim p(i)=\sin i$ em $(0,\pi/2)$ (orientação isotrópica).
- Longitude do periastro $\phi_0 \sim U(0,2\pi)$.
- Tempo desde o periastro $t \sim U(0,T)$; fase orbital $\phi$ obtida
  resolvendo numericamente
  $t \propto \int_{\phi_0}^\phi d\phi'/(1+e\cos\phi')^2$ (equação de
  Kepler, resolvida por Newton-Raphson vetorizado em `numpy`, não em
  laço Python por sistema).

### Gap (c): fórmulas de desprojeção (idêntico a Chae, Eqs. 7-9)

$$\psi = \tan^{-1}\!\left(-\frac{\cos\phi+e\cos\phi_0}{\sin\phi+e\sin\phi_0}\right)$$
$$r = \frac{s}{\sqrt{\cos^2\phi+\cos^2 i\sin^2\phi}}, \qquad
v = \frac{v_p}{\sqrt{\cos^2\psi+\cos^2 i\sin^2\psi}}$$

onde $s$ (separação projetada) e $v_p$ (velocidade relativa projetada,
mesma fórmula $v_p=4{,}74047\times10^{-3}\cdot\Delta\mu\cdot\bar d$ já
usada em SPARC-003) são os valores OBSERVADOS fixos; $r$ e $v$ são a
separação e velocidade 3D "verdadeiras" recuperadas para aquela amostra
particular de geometria orbital.

### Gap (d): estatística por sistema e por bin

$$g_{N,i} = \frac{GM_{tot,i}}{r_i^2} \text{ (Newtoniana, SI)}, \qquad
g_i = \frac{v_i^2}{r_i} \text{ (cinemática, SI)}$$

$I(X)$ = mediana de $\log_{10}(g_i/g_{N,i})$ dentro de cada um dos 5 bins
de $\log_{10}(g_N)$ JÁ FIXADOS em SPARC-003 (bordas em
`../COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md` Seção 2, reaproveitadas
sem modificação — nenhum novo binning definido a partir do resultado
deste teste).

**Predição MOND por bin**, usando a MESMA função de interpolação "simple"
já travada em SPARC-002/003 (McGaugh, Lelli & Schombert 2016), aplicada
em espaço de aceleração (não reformulada):

$$\frac{g^{\text{MOND}}}{g_N}(a_0) = \nu(g_{N,\text{bin}}/a_0) =
\frac{1}{1-e^{-\sqrt{g_{N,\text{bin}}/a_0}}}$$

Predição Newtoniana pura: $g/g_N=1$ (checagem de sanidade, não parte do
critério H_A/H_B).

### Gap (e): protocolo Monte Carlo e incerteza

1. `N_MC=200` realizações completas da amostra de descoberta inteira
   (mesma convenção de Chae — "*the distribution of medians in a bin is
   well determined for N>100 MC realizations*", citação literal já
   verificada). Para CADA sistema, em CADA realização: sorteio
   independente de $(e,i,\phi_0,t)$ conforme Gaps (a)-(b), cálculo de
   $(r,v,g,g_N)$ — feito DUAS VEZES em paralelo por sistema/realização,
   uma vez usando o $v_p$ REAL observado, outra vez usando um $v_p$
   MOCK sintético Newtoniano puro (mesma geometria orbital sorteada
   independentemente) — conforme o Adendo 4c.
2. Para cada sistema, isso produz duas distribuições de 200 valores cada:
   $\log_{10}(g_i/g_{N,i})_{\text{real}}$ e
   $\log_{10}(g_i/g_{N,i})_{\text{mock}}$ — capturando a incerteza
   geométrica/orbital daquele sistema individual em ambos os ramos.
3. **IC de 95% via bootstrap por sistema, reaproveitando os 200×2
   sorteios já computados (sem recomputar a desprojeção por réplica):**
   1000 réplicas bootstrap sobre os 30.203 sistemas (reamostragem com
   reposição); para cada réplica, cada sistema resamostrado usa UM dos
   seus 200 pares `(real, mock)` já pré-computados, sorteado
   uniformemente (o par vem do MESMO índice de realização MC, preservando
   qualquer correlação real-mock por construção); $\delta_{\text{obs-newt}}$
   por bin recalculado (mesmas bordas fixas) e `a0` reajustado (passo 4
   abaixo) em cada réplica — dá o IC de 95% em `a0` capturando TANTO
   variabilidade amostral QUANTO incerteza de desprojeção, sem custo
   combinatório de recomputar 1000×200 desprojeções completas.
4. Ajuste não-linear de mínimos quadrados de `a0` (único parâmetro
   livre) entre os 5 valores reais de $\delta_{\text{obs-newt}}(\text{bin})$
   (da realização primária, item 1) e o modelo
   $\delta_{\text{AQUAL}}(\text{bin};a_0)=\log_{10}(\nu(g_{N,\text{bin}}/a_0))$
   — mesmo procedimento de SPARC-003 Seção 4, adaptado à estatística
   diferenciada do Adendo 4c. Convergência verificada com $\geq2$ pontos
   de partida diferentes (lição de SPARC-002, reaplicada).
5. Verificar se $a_0^A$ e/ou $a_0^B$ caem dentro do IC de 95%.

### Simplificação declarada: correção de companheiras ocultas ($f_{multi}$) NÃO implementada

Chae (2023) auto-calibra uma fração de multiplicidade oculta $f_{multi}$
(companheiras não resolvidas, que inflam $g/g_N$ observado ao adicionar
massa não contabilizada) via um ensemble Newtoniano mock e uma
máquina de injeção de companheiras (Eqs. 11-13 do Artigo A: distribuição
de razão de massa, distribuição de semi-eixo interno) — máquina complexa,
separada da própria desprojeção geométrica que é o foco desta redesenho.
**Não implementada aqui.** Isso é um viés unidirecional CONHECIDO e
NOMEADO (não hipotético): companheiras ocultas não modeladas tendem a
INFLAR $g/g_N$ acima do valor verdadeiro de 2 corpos. Declarado
explicitamente como limitação, análogo em espírito à simplificação WCM
já usada em `wavelet-multiresolution-scaling`. **Consequência
pré-declarada para o veredito:** se o resultado real mostrar
$g/g_N$ sistematicamente ACIMA de 1 de forma consistente com H_A ou H_B,
a checagem adversarial obrigatória (Seção 6) deve testar especificamente
se multiplicidade oculta não corrigida, sozinha, poderia produzir esse
deslocamento (mesmo padrão de "escalada condicional ao tamanho do
efeito" já usado 2x na linha `DISC-TRI-RG-001` para SOC/DFA).

## 4b. Validação sintética OBRIGATÓRIA antes do lock

**Nota:** esta seção documenta a PRIMEIRA rodada de validação (critério
original, sobre `g/g_N` bruto) e seu resultado — mantida por
transparência histórica, não removida. O critério de aceitação real,
após o Adendo 4c corrigir a estatística para `δ_obs-newt`, é o descrito
em 4c ("Revalidação obrigatória sob a estatística corrigida").

Antes de `Status` mudar para `LOCKED`: rodar a pipeline completa de
desprojeção sobre um Monte Carlo sintético de binárias PURAMENTE
Newtonianas (zero física MOND), usando a MESMA distribuição de
excentricidade real (amostrada do catálogo de Hwang, não inventada) e as
MESMAS separações/massas da amostra de descoberta real, mas com
velocidades geradas por órbita Kepleriana Newtoniana pura + projeção
geométrica isotrópica (sem nenhum boost MOND). Verificar explicitamente:
a mediana de $g/g_N$ desprojetado recuperada por essa simulação cai
PRÓXIMA de 1 (dentro do IC de 95% do próprio Monte Carlo), confirmando
que a estatística NÃO sofre da mesma restrição estrutural de imagem que
já matou a tentativa anterior (que usava $v_p/v_p^N$ projetado, com
imagem MOND $(1,+\infty)$ mas medianas reais projetadas $<1$). Esta é
exatamente a checagem que `METHODOLOGY_EXTENSIONS.md` Seção 1 exige desde
o achado de SPARC-003 — feita ANTES do lock desta vez, não depois.

**Se essa validação falhar** (mediana recuperada significativamente
diferente de 1 sob Newtoniano puro simulado): o desenho precisa ser
revisto ANTES do lock — não travar um pré-registro fadado ao mesmo
problema estrutural.

## 4c. Adendo de metodologia — estatística corrigida para `δ_obs-newt` (adicionado APÓS validação sintética, ANTES de qualquer dado real)

A validação sintética obrigatória da Seção 4b (rodada com dado real de
separação/massa/excentricidade, `v_p` sintético gerado por órbita
Kepleriana Newtoniana pura) revelou um problema real, não um bug: a
mediana de $\log_{10}(g/g_N)$ recuperada sob Newtoniano puro simulado foi
$-0{,}204$ (IC 95% $[-0{,}213,-0{,}195]$), NÃO próxima de 0 como a Seção
4b originalmente exigia. Diagnóstico confirmado (checagem de excentricidade
zero recupera $\approx-0{,}005$, isolando a causa): $g\equiv v^2/r$ **não
é** a aceleração radial newtoniana instantânea para uma órbita excêntrica
— é uma aproximação tipo-circular que subestima sistematicamente $g_N$
quando média sobre a fase orbital, porque o sistema passa mais tempo perto
do afélio (velocidade menor) do que do periélio. Esse deslocamento
($\approx-0{,}17$ a $-0{,}20$ dex para $e\gtrsim0{,}5$) bate em SINAL e
ORDEM DE GRANDEZA com o que o próprio Artigo A de Chae já documenta (Eq.
16, já citada na Seção 0 deste pré-registro) — **não é um artefato de
implementação**, é uma propriedade conhecida da própria estatística
$v^2/r$ sob excentricidade real, e é exatamente por isso que Chae usa a
estatística DIFERENCIADA `δ_obs-newt`, não o valor bruto de $g/g_N$.

**Correção, fixada ANTES de qualquer dado real:** o observável
discriminador (Gap (d)/(e) da Seção 4) passa a ser

$$\delta_{\text{obs-newt}}(\text{bin}) = \text{mediana}_{\text{real}}
\big(\log_{10}(g/g_N)\big) - \text{mediana}_{\text{mock}}
\big(\log_{10}(g/g_N)\big)$$

onde o ensemble **mock** usa a MESMA separação $s_i$, massa total $M_{tot,i}$
e parâmetros de excentricidade ($e_m,e_l,e_u,\alpha,dpm\_sig$) de CADA
sistema real, mas com $v_p$ gerado SINTETICAMENTE por uma órbita
Kepleriana puramente Newtoniana (geometria orbital $e,i,\phi_0,\phi$
sorteada independentemente da usada no cálculo real, projetada de volta
pelas mesmas fórmulas inversas) — exatamente o procedimento já
implementado e usado na validação da Seção 4b (`validate_synthetic_newtonian.py`),
reaproveitado aqui como o "ensemble Newtoniano mock" do próprio método de
Chae (Artigo A, Seção 3.4), que este pré-registro havia inicialmente
simplificado por engano ao tratar $g/g_N=1$ como baseline direto.

**Predição MOND por bin, agora em termos de `δ`:**

$$\delta_{\text{AQUAL}}(\text{bin};a_0) = \log_{10}\!\big(\nu(g_{N,\text{bin}}/a_0)\big),
\qquad \nu(x)=\frac{1}{1-e^{-\sqrt{x}}}$$

(pois o mock, por construção, já teria $\delta=0$ sob Newton puro — o
boost MOND aparece como um deslocamento ADICIONAL de `δ` relativo ao
próprio mock, não relativo a $g/g_N=1$ bruto).

**Revalidação obrigatória sob a estatística corrigida, ANTES do lock:**
1. **Controle negativo (nulo):** dois ensembles Newtonianos independentes
   (real E mock ambos sintéticos Newtonianos, sorteios de geometria
   orbital independentes) — `δ_obs-newt` deve ficar próximo de 0 (IC 95%
   contendo 0) em cada bin.
2. **Controle positivo:** ensemble "real" sintético com um boost MOND
   injetado explicitamente (`v_p` multiplicado por $\sqrt{\nu(g_N/a_0^{\text{teste}})}$
   para um `a0` de teste conhecido, ex. $a_0=1{,}2\times10^{-10}$),
   ensemble mock permanece Newtoniano puro — `δ_obs-newt` recuperado deve
   bater, em sinal e ordem de grandeza, com $\delta_{\text{AQUAL}}(\text{bin};a_0^{\text{teste}})$
   previsto.

Só após os itens 1 e 2 acima passarem, `Status` muda para `LOCKED`.

## 5. Critério de falsificação

- **H_A falsificada** se $a_0^A\approx1{,}082288\times10^{-10}$ estiver
  fora do IC de 95% do `a0` ajustado.
- **H_B falsificada** se $a_0^B\approx6{,}800218\times10^{-10}$ estiver
  fora do IC de 95%.
- Se apenas uma sobreviver: suporte a essa derivação especificamente.
- Se nenhuma sobreviver: ambas falsificadas por este canal.
- Se as duas sobreviverem: INCONCLUSIVO (mesmo veredito possível de
  SPARC-002/003).
- **Pré-condição obrigatória (Seção 4b) para aceitar QUALQUER veredito
  acima:** a validação sintética Newtoniana deve ter passado — se a
  checagem de sanidade da Seção 3/4b falhar, o teste para até isso ser
  resolvido, mesma regra já usada em SPARC-002/003.

## 6. Correção para comparações múltiplas / checagem adversarial obrigatória

Duas hipóteses pré-registradas testadas contra o mesmo IC de um único
ajuste de 5 bins — sem busca sobre número de bins (reaproveitados fixos
de SPARC-003). Reexecução adversarial obrigatória (`AGENTS.md` passo 7,
segundo agente, implementação independente do zero) antes de catalogar
qualquer resultado. **Checagem adversarial de multiplicidade oculta
obrigatória especificamente** se o resultado mostrar $g/g_N>1$ de forma
consistente com H_A ou H_B (ver Gap (e), simplificação declarada acima).

## O que este pré-registro NÃO é

Não redefine H_A/H_B. Não é uma reprodução byte-a-byte do Artigo A de
Chae (a correção de multiplicidade oculta é declaradamente omitida, e a
comparação com H_A/H_B específicos é uma extensão da estatística
$\delta_{\text{obs-newt}}$ de Chae, não literal do artigo). O holdout
selado de SPARC-003 (12.944 sistemas) permanece intocado, reservado para
o Gate de Replicação futuro deste teste, se e quando ele chegar lá.
