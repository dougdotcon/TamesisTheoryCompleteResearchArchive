# Nota de metodologia — fechamento dos gaps de `kramers-moyal` (Reconstrução de Fokker-Planck via Coeficientes de Kramers-Moyal)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (choque de despeg do Banco Nacional Suíço, EUR/CHF
tick-a-tick; arritmia ventricular maligna, PhysioNet `vfdb`). Mesmo
espírito de disciplina já usado para os 8 candidatos anteriores desta
linha.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md`
(candidato 2) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #2 entre os 4 novos candidatos da Fase 0.6 — a
regra de seleção de `R_lambda` mais principiada de toda a linha (teste
de Markov-Einstein orientado a dado, não janela escolhida), mas com um
risco de identificabilidade CONFIRMADO ANALITICAMENTE (não só
correlação empírica) contra `critical_slowing_down`, já fechado
negativo.

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.6): 2 domínios reais com dado baixado/inspecionado
— (a) tick-a-tick EUR/CHF (Dukascopy, formato binário `.bi5` decodificado
diretamente), choque do SNB de 15/01/2015; (b) PhysioNet MIT-BIH
Malignant Ventricular Arrhythmia Database (`vfdb`), registro 418, ~10
transições N→VFL→N documentadas dentro do mesmo registro contínuo de
35min. Nenhum `Delta I` calculado ainda. Faltam: (a) protocolo exato do
teste de Markov-Einstein/Chapman-Kolmogorov (a própria regra de
`R_lambda`); (b) estimação de `D1(x)`/`D2(x)` e definição exata de
`I(X)`, com a decisão sobre o canal de risco (`kappa`) já resolvida
ANTES de qualquer dado, não depois; (c) definição de PRE/POST; (d) piso
de amostra por bin e teto de subamostragem; (e) protocolo de
significância.

## Gap (a): `R_lambda` — teste de Markov-Einstein / Chapman-Kolmogorov

**Grade de `Delta_tau` candidato:** sequência geométrica começando no
intervalo de amostragem nativo `dt` do domínio, fator de crescimento
`1,5`, até `N_LAG_MAX=20` pontos de grade ou até `Delta_tau` exceder 5%
do comprimento do segmento (o que vier primeiro).

**Binagem de `x` (compartilhada entre o teste de CK e a estimação de
`D1`/`D2` no Gap (b), para consistência):** `N_BINS_X=10` bins por
quantil, calculados UMA VEZ a partir do segmento PRE real (mesma
convenção "estimar do PRE, aplicar aos dois" já usada com sucesso no
RQA para `(m,tau)`) — reaplicados sem recálculo ao POST e a todos os
substitutos de ambos.

**Teste de Chapman-Kolmogorov, para cada `Delta_tau` candidato:**
comparar a distribuição de transição em 2 passos estimada DIRETAMENTE
dos dados (`p_direto(x3|x1; 2*Delta_tau)`) contra a predição de CK
construída pela convolução das distribuições de transição de 1 passo
(`p_CK(x3|x1;2*Delta_tau) = sum_x2 p(x2|x1;Delta_tau)*p(x3|x2;Delta_tau)`),
via distância qui-quadrado entre os dois histogramas de transição.
Significância por bootstrap (reamostragem de índices temporais com
reposição, `N_BOOTSTRAP_CK=200`, recalculando a estatística a cada
réplica) — `p_CK_test = fração de réplicas bootstrap com distância
qui-quadrado >= distância observada`.

**`tau_ME` (a escala de Markov-Einstein, o próprio `R_lambda`):** o
MENOR `Delta_tau` da grade tal que o teste de CK NÃO rejeita
(`p_CK_test>=0,05`) NESSE `Delta_tau` E nos 2 pontos de grade seguintes
(checagem de robustez contra um único não-rejeição por sorte). **Se
nenhum `Delta_tau` da grade satisfizer isso, o domínio/segmento é
REJEITADO por propriedade de Markov não estabelecida** — declarado
honestamente antes de qualquer cálculo, não forçado (mesma disciplina já
usada para grades insuficientes em VG/RQA).

`tau_ME` estimado UMA VEZ a partir do PRE real, reaplicado sem
recálculo ao POST e a todos os substitutos — evita confundir "mudança
genuína de dinâmica" com "escala de Markov diferente escolhida".

**Checagem de Pawula (diagnóstico, reportado honestamente, não um
critério de aceitação/rejeição binário):** `D3(x)` e `D4(x)` calculados
nos mesmos bins; razão `D4/D2^2` reportada como diagnóstico de quão bem
a expansão de Kramers-Moyal trunca numa equação de Fokker-Planck
genuína (Pawula 1967) — se claramente não-negligível, declarado como
limitação honesta, não escondido, mas não usado para descartar o
domínio automaticamente (mesmo espírito de "desvio metodológico
declarado" já usado em MSE/rolamento).

## Gap (b): `D1(x)`/`D2(x)` e `I(X)` — decisão sobre o risco de redundância com CSD tomada ANTES de dado real

**Estimação:** `D1(x) ≈ M1(x,tau_ME)/tau_ME`, `D2(x) ≈
M2(x,tau_ME)/(2*tau_ME)`, onde `M1`/`M2` são o primeiro e segundo
momento condicional do incremento `X(t+tau_ME)-x` dado `X(t)=x`,
calculados nos `N_BINS_X=10` bins fixados no Gap (a). Piso de amostra
por bin: `MIN_SAMPLES_PER_BIN=30` — bins com menos amostras são
marcados indefinidos, não extrapolados.

**Densidade estacionária reconstruída:** `p_st(x) ∝ (1/D2(x)) *
exp(integral 2*D1(x')/D2(x') dx')` (Fokker-Planck estacionária padrão),
integração cumulativa trapezoidal sobre os centros de bin, normalizada a
posteriori.

**Risco de identificabilidade CENTRAL, confirmado ANALITICAMENTE (não
só correlação empírica) — decisão tomada AQUI, antes de qualquer dado
real, não depois de ver um resultado desfavorável:** Ritchie & Sieber
2016 (arXiv:1609.07271) mostra que, para a linearização
Ornstein-Uhlenbeck ao redor de um ponto fixo, tanto AC1 quanto variância
(a base de `critical_slowing_down`, já fechado negativo nesta linha) são
funções algébricas EXATAS da mesma taxa de decaimento
`kappa=-D1'(x*)`. Isso não é um risco hipotético a testar por IAAFT — é
uma identidade algébrica na região linear. **Decisão:** `kappa` NÃO
entra no critério de decisão primário desta rodada — mantido apenas como
canal DIAGNÓSTICO (reportado, mas não parte do veredito), a mesma
disciplina já aplicada a `d_B` em `grafo-de-visibilidade`, exceto que
aqui a demoção é feita a priori, com base numa prova algébrica, não
descoberta post-hoc numa validação.

**`I(X)` primário:** `PKS` (Estatística de Curtose de Forma do
Potencial) = curtose em excesso de `p_st(x)` reconstruída — escalar
contínuo, sempre definido (ao contrário de "contar poços", que é
discreto), sensível a bimodalidade (densidades bimodais tendem a
curtose em excesso negativa/platicúrtica; unimodais fortemente
concentradas, positiva) — a mesma informação de "forma do potencial"
que Livina & Lenton (2007, *GRL* 34:L03712) e Livina, Kwasniok & Lenton
(2010, *Climate of the Past* 6:77) rastrearam via contagem de poços em
transições paleoclimáticas, aqui expressa como um único número contínuo
compatível com o protocolo de significância desta linha.

**`I(X)` companheiro:** `beta_D2` = inclinação OLS de `D2(x)` vs. `x`
(ou vs. `|x-x*|`, testado e reportado com o que for mais estável) —
indicador de ruído multiplicativo/dependente de estado: `beta_D2≈0`
ruído aditivo (convenção implícita de `critical_slowing_down`);
`beta_D2` claramente não-nulo, ruído dependente de estado — um canal que
o arcabouço de CSD estruturalmente não tem análogo algum.

## Gap (c): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada 7x nesta linha): PRE (primária) = todo o registro contínuo
disponível anterior à transição documentada; PRE (robustez) = os 50%
mais recentes (por CONTAGEM de amostras) desse PRE. POST (primária) =
todo o registro contínuo disponível posterior à transição, até o
próximo evento/confundidor documentado; POST (robustez) = os 50% mais
próximos da transição desse POST.

- **EUR/CHF (choque SNB):** transição = anúncio do SNB, 15/01/2015
  ~09:30 UTC. PRE = tick-a-tick antes do anúncio. POST = tick-a-tick
  depois, até o final do dia de negociação documentado ou o próximo
  evento macro relevante.
- **PhysioNet `vfdb` registro 418:** transição = onset da PRIMEIRA
  episódio de VFL anotado no registro (convenção da regra PRE/POST já
  estabelecida, aplicada à primeira transição documentada). PRE = ECG
  antes desse onset. POST = ECG durante o episódio, até o offset
  anotado. **Nota honesta de escopo, declarada a priori:** o registro
  contém ~10 transições N→VFL→N no total — só a primeira é usada nesta
  rodada de fechamento de gaps, seguindo a mesma convenção de "1
  transição por domínio" já usada em todos os candidatos anteriores
  desta linha. As ~9 transições restantes ficam disponíveis, não
  usadas, como semente reaproveitável para uma futura tentativa de
  replicação dentro do próprio registro, se e quando esta linha chegar a
  um Gate de Replicação — não exploradas aqui para não introduzir
  múltiplas comparações não corrigidas no critério de decisão primário.

## Gap (d): piso de amostra e teto de subamostragem

`MIN_SAMPLES_PER_BIN=30` já declarado no Gap (b). Custo computacional
menor que VG/RQA (contagem de momento condicional é O(N) por bin, teste
de CK com bootstrap é o passo mais caro mas ainda tratável) —
`MAX_N_PER_SEGMENT=50000`, decimação por *stride* uniforme se excedido,
aplicada IGUALMENTE aos 2 domínios.

## Gap (e): protocolo de significância — IAAFT

Mesmo protocolo padrão já usado nesta linha: `N_SURROGATES=200`,
`N_IAAFT_ITER=50`, substitutos de PRE e POST gerados
INDEPENDENTEMENTE cada um da sua própria série real, `seed=12345`, teste
BICAUDAL. Cada substituto passa pela MESMA pipeline completa
(`tau_ME` e bins de `x` JÁ FIXADOS do PRE real, não reestimados por
substituto — mesma lógica já usada para `(m,tau)` no RQA). `p = fração
de substitutos com |Delta_PKS_substituto| >= |Delta_PKS_real|` (e
igualmente para `Delta_beta_D2`). **Nota sobre o que este teste
resolve:** ao contrário de MSE/VG/RQA/entropia-de-permutação, o risco
de identificabilidade CENTRAL desta rodada (redundância com CSD via
`kappa`) já foi resolvido no Gap (b) por decisão a priori, não pelo
IAAFT — o IAAFT aqui cumpre o papel padrão desta linha de testar se a
mudança de `PKS`/`beta_D2` excede o que um substituto de espectro
casado produziria, um teste de significância de propósito geral, não
específico a um risco nomeado.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado (mesmo padrão já usado nos 8 candidatos anteriores). A
metodologia acima foi fixada ANTES de qualquer cálculo, incluindo a
decisão de demover `kappa` a diagnóstico — uma correção de desenho
baseada em prova algébrica já publicada, tomada antes de ver qualquer
resultado real, não uma reformulação posterior.
