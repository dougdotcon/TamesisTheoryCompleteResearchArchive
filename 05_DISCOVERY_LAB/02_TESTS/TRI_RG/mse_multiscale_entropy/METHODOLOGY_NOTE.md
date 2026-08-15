# Nota de metodologia — fechamento dos gaps de `mse-multiscale-entropy`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (tempestade geomagnética de março/1989, degradação de
rolamento FEMTO/PRONOSTIA). Mesmo espírito de disciplina já usado para os
4 candidatos anteriores desta linha.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`
(candidato 1) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #2 entre os 4 novos candidatos — fundamentação
formal de `R_lambda` mais rigorosa já considerada nesta linha (conexão
direta com o Teorema Central do Limite visto como fluxo de RG, Jona-Lasinio
2001), mas com risco real de redundância com a família Hurst já testada
(DFA, wavelet).

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.5): 2 domínios reais com dado baixado/inspecionado —
(a) índice geomagnético Dst/SYM-H, tempestade de 13/03/1989 ("Quebec
Blackout", SYM-H mínimo -714 nT, ano completo de 1989 baixado do NASA/SPDF
OMNIweb, 34,4MB, sha256 registrado); (b) vibração de rolamento até falha
(FEMTO/PRONOSTIA, IEEE PHM 2012 Data Challenge, critério de fim-de-vida
`>20g` definido pelos organizadores, externo ao cálculo de entropia).
Nenhum `Delta I` calculado ainda. Faltam: (a) regra de escala `tau`
cross-domain (a convenção original de Costa usa `tau` inteiro absoluto
1-20, incompatível entre 25,6kHz do rolamento e 5min do Dst); (b)
definição exata de `I(X)` e protocolo de significância; (c) definição de
segmento PRE/POST em cada domínio.

## Gap (a): regra de escala `tau` (`R_lambda`) cross-domain

**Decisão:** coarse-graining de blocos NÃO sobrepostos, exatamente a
definição original de Costa, Goldberger & Peng (2002, *PRL* 89:068102;
2005, *Phys. Rev. E* 71:021906):

```
x_j^(tau) = (1/tau) * sum_{i=(j-1)*tau+1}^{j*tau} x_i
```

**Grade de escala domain-agnostic (fixada a priori, nunca a convenção
literal de Costa et al. de `tau` inteiro absoluto 1-20, que pressupõe
domínios fisiológicos de cadência comparável — inaplicável entre 25,6kHz e
5min):**

- `tau_min = 1` (mesmo ponto de partida universal da convenção original).
- `tau_max = floor(N / MIN_POINTS_AT_COARSEST)`, com
  `MIN_POINTS_AT_COARSEST = 200` — piso de amostra mínimo para uma
  estimativa confiável de SampEn com `m=2` (Yentes et al. 2013, *Annals of
  Biomedical Engineering* 41:349, "The Appropriate Use of Approximate
  Entropy and Sample Entropy with Short Data Sets" — recomendação
  amplamente citada na literatura, não um valor inventado nesta sessão).
- `N_SCALES = min(20, tau_max)` valores de `tau`, log-espaçados entre
  `tau_min` e `tau_max`, arredondados para inteiros únicos.

Esta regra liga `tau_max` diretamente ao tamanho da amostra disponível
(o que de fato limita a confiabilidade da estimativa de SampEn), em vez de
um valor absoluto de tempo ou um número fixo de escalas — a mesma
disciplina "fração/piso não reajustado por domínio" já usada em CSD
(`window_frac`), DFA (`n_max_frac`) e SOC (`lambda`=IEI médio).

## Gap (b): definição de `I(X)`, parâmetros de SampEn e declaração de identificabilidade

**Parâmetros de SampEn** (Richman & Moorman 2000): `m=2` (dimensão de
embedding), `r=0,15*SD(X)` calculado UMA VEZ sobre a série ORIGINAL
(`tau=1`, antes de qualquer coarse-graining) e mantido FIXO em todas as
escalas — convenção original de Costa et al., não a variante posterior
("r ajustado por escala") de alguns trabalhos derivados, para evitar
ambiguidade.

**`I(X)` primário:** `CI` (Complexity Index) = soma de `SampEn(tau)` sobre
toda a grade de escalas — a mesma estatística que Costa et al. usaram para
separar saudável vs. insuficiência cardíaca congestiva.

**`I(X)` secundário (canal companheiro):** `beta` = inclinação OLS de
`SampEn(tau)` vs. `log(tau)` — classificação de operador sob `R_lambda`
já proposta na Fase 0.5 (`beta≈0`: marginal/auto-similar, ponto fixo
não-trivial; `beta<0`: irrelevante, flui para o ponto fixo Gaussiano
trivial do CLT; `beta>0` sem saturar: relevante, processo não-estacionário).

`Delta_CI = CI(POST) - CI(PRE)`, `Delta_beta = beta(POST) - beta(PRE)`.

**Declaração de identificabilidade (Seção 1 de `METHODOLOGY_EXTENSIONS.md`,
obrigatória — risco já identificado na Fase 0.5, não escondido):** para
processos gaussianos autossimilares PUROS, `beta` pode ser essencialmente
um reparâmetro do expoente de Hurst `H`, já testado nesta linha via
`dfa-multiscale-entropy` (NEGATIVO) e o canal `C2` de
`wavelet-multiresolution-scaling` (NEGATIVO). O discriminador que
distingue MSE desses candidatos: `alpha` (DFA) já se mostrou, nesta
própria linha, quase puramente ESPECTRAL (substitutos IAAFT, que
preservam o espectro linear, reproduzem `alpha` real quase exatamente,
por isso o teste de bootstrap por blocos teve que ser adicionado como
primário para DFA). SampEn, ao contrário, é sensível a estrutura NÃO-LINEAR
que um substituto IAAFT NÃO reproduz. **Se `Delta_CI`/`Delta_beta`
sobreviverem ao teste IAAFT (Gap (c) abaixo), isso é evidência de
estrutura não-linear genuína além do que DFA/wavelet já testaram — o
próprio teste de identificabilidade desta linha.** Se não sobreviverem,
colapsa na mesma redundância já identificada como risco.

**Modelo concorrente nomeado e real:** processo gaussiano autossimilar de
`H` único (fGn/fBm) — mesmo concorrente já usado por
`wavelet-multiresolution-scaling` e implicitamente por
`dfa-multiscale-entropy`.

## Gap (c): protocolo de significância — IAAFT como teste PRIMÁRIO (não secundário)

**Decisão, diferente da convenção usada em CSD/DFA/SOC (onde IAAFT ou
Poisson foi secundário):** aqui o substituto IAAFT (Schreiber & Schmitz
1996, mesmo método já usado em `wavelet-multiresolution-scaling` e
`dfa-multiscale-entropy`) é o teste PRIMÁRIO de significância, porque é
literalmente o discriminador de identificabilidade declarado no Gap (b) —
a pergunta "sobrevive ao IAAFT?" NÃO é uma checagem incidental aqui, é a
própria pergunta de pesquisa.

Protocolo: `N_SURROGATES=200` pares (mesma convenção de custo computacional
de `wavelet-multiresolution-scaling`, já que IAAFT é caro), `N_IAAFT_ITER=50`,
substitutos de PRE e POST gerados INDEPENDENTEMENTE cada um da sua própria
série real, `seed=12345`. Teste BICAUDAL: a Fase 0.5 já identificou
ambiguidade de direção na literatura de complexidade geomagnética
(resultados conflitantes sobre se a complexidade sobe ou desce perto de
tempestades) — declarar bicaudal a priori em vez de escolher a direção
depois de ver o resultado. `p = fração de substitutos com
|Delta_CI_substituto| >= |Delta_CI_real|` (e igualmente para `Delta_beta`).

**Validação obrigatória adicional (ANTES de qualquer dado real):** como
o IAAFT é o teste PRIMÁRIO aqui (ao contrário de onde já se mostrou fraco
para `alpha` em DFA), a validação sintética PRECISA confirmar que ele tem
poder real para `CI`/`beta` antes de prosseguir — não pode ser assumido.
Se a validação repetir o mesmo padrão de baixo poder já visto em DFA, a
mesma correção (teste complementar de bootstrap) deve ser adicionada
ANTES de tocar dado real, seguindo a disciplina já estabelecida 2x nesta
linha (DFA, SOC).

## Gap (d): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada 3x nesta linha — CSD, DFA, SOC): PRE (primária) = todo o registro
contínuo disponível anterior à transição documentada; PRE (robustez) = os
50% mais recentes (por CONTAGEM de amostras) desse PRE. POST (primária) =
todo o registro contínuo disponível posterior à transição, até o próximo
evento/confundidor documentado; POST (robustez) = os 50% mais próximos da
transição desse POST.

- **Geomagnetismo:** transição = SSC (storm sudden commencement) em
  13/03/1989 01:27 UT, documentado externamente (Boteler 2019, *Space
  Weather* 17:1427). PRE = período quieto anterior ao SSC (janeiro–início
  de março de 1989, dentro do ano completo já baixado). POST = fase
  principal + recuperação da tempestade após o SSC.
- **Rolamento (FEMTO/PRONOSTIA):** transição = primeiro instante em que a
  amplitude de vibração ultrapassa `20g`, critério de fim-de-vida definido
  pelos organizadores do desafio (Nectoux et al. 2012), externo a qualquer
  cálculo de entropia. PRE = dado disponível antes desse instante; POST =
  dado disponível depois (pode ser um segmento curto, dado que o teste
  geralmente termina logo após a falha — reportar honestamente se `POST`
  ficar pequeno demais para os requisitos de `MIN_POINTS_AT_COARSEST`).

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado. A metodologia acima foi fixada ANTES de qualquer cálculo,
precisamente para que, se um pré-registro for escrito depois, ele possa
declarar honestamente que a regra de escala, a definição de `I(X)` e o
protocolo de significância já existiam antes de qualquer resultado ser
visto.
