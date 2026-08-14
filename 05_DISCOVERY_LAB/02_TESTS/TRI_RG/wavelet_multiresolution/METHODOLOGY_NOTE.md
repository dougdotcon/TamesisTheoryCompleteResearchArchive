# Nota de metodologia — fechamento dos gaps de `wavelet-multiresolution-scaling`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (sismologia/Tohoku, EEG de crise/CHB-MIT). Mesmo espírito
de disciplina já usado para `critical-slowing-down`
(`../critical_slowing_down/METHODOLOGY_NOTE.md`).

Gaps a fechar (ver `SECOND_DOMAIN_SEARCH.md` e `phase0/PHASE0_SURVEY.md`):
(1) regra de janela/escala cross-domain; (2) cálculo real do método
WTMM/wavelet; (3) protocolo de dados substitutos (IAAFT).

## Escolha de método: log-cumulantes de coeficientes wavelet (WCM), não WTMM/wavelet-leader completo

A Fase 0 mencionou "WTMM" e "wavelet-leader" como formalismos
equivalentes. Por tratabilidade computacional dentro do escopo desta
Fase 0/exploratória (o método de wavelet-leader completo de Jaffard exige
rastrear vizinhanças multi-escala para cada coeficiente, custo
proibitivo para um protocolo de substitutos com centenas de repetições),
esta rodada usa o **método de coeficientes wavelet (WCM) com
log-cumulantes** (Castaing, Gagne & Hopfinger 1990; Delbeke & Abry 2000;
revisado em Wendt, Abry & Jaffard, *IEEE Signal Processing Magazine*
2007, que discute WCM e WLM como variantes relacionadas do mesmo
formalismo de log-cumulantes — WLM é uma melhoria para processos muito
esparsos/tipo-ponto ou momentos `q` negativos, não estritamente
necessária aqui). Isso é uma SIMPLIFICAÇÃO declarada explicitamente, não
uma mudança de candidato: `R_lambda` continua sendo a mesma projeção
multirresolução wavelet (subespaços `V_j` aninhados,
`R_2λ=R_λ'∘R_λ` por construção); `I(X)` passa a ser o log-cumulante de
segunda ordem `C2` (inclinação de `Var(log|d_{j,k}|)` vs. `j`) em vez de
`Δα` via linhas de máximo WTMM — `C2=0` para processo monofractal,
`C2<0` para cascata multifractal genuína, é a estatística padrão
equivalente na literatura de log-cumulantes.

## Gap (1): regra de janela/escala cross-domain

Wavelet: `db4` (Daubechies, 4 momentos nulos), mesma em todo domínio.
Decomposição via `pywt.wavedec` (`mode='periodization'`), nível máximo
permitido pelo comprimento do sinal. Escalas `j` com menos de
`MIN_COEFFS_PER_SCALE=16` coeficientes são descartadas (regra fixa, não
ajustada por domínio) — evita estimar cumulantes com amostra
insuficiente na escala mais grosseira.

**Definição de segmento (regra domain-agnostic):**
- **PRE:** até 2 horas de dado disponível imediatamente ANTES da
  transição documentada (ou todo o disponível, se menor que 2h — caso do
  EEG, que só tem 5 min de pré-transição no arquivo já preparado).
- **POST:** até 2 horas de dado disponível imediatamente DEPOIS da
  transição documentada (ou todo o disponível, se menor — caso do EEG,
  ictal dura só ~40s).
- **Variante robustez:** PRE e POST truncados ao comprimento do menor
  dos dois (`min(len(PRE), len(POST))`), sempre tomando as amostras mais
  próximas da transição em cada lado.

Mesma regra verbal aplicada sem ajuste nos 2 domínios — nenhuma data ou
duração escolhida à mão por domínio.

## Gap (2): estatística de transição

`ΔC2 = C2(POST) - C2(PRE)` (indicador principal de mudança de
multifractalidade) e `ΔC1 = C1(POST) - C1(PRE)` (companheiro, proxy do
expoente H). Calculados com a MESMA pipeline (`wtmm_common.py`) nas duas
variantes (primária e robustez), nos dois domínios, sem reajuste.

## Gap (3): protocolo de dados substitutos

**IAAFT** (Iterative Amplitude Adjusted Fourier Transform — Schreiber &
Schmitz 1996), o mesmo método já citado na Fase 0 e usado por Ivanov et
al. (1999) para descartar multifractalidade espúria de origem linear.
Preserva o espectro de potência linear (logo, preserva H/monofractalidade)
e a distribuição exata de amplitude do sinal original, mas destrói a
estrutura de fase não-linear que produz multifractalidade genuína.

Protocolo: `N_SURROGATES=200` pares de substitutos (um para PRE, um para
POST, gerados INDEPENDENTEMENTE cada um a partir de sua própria série
real — preservando o espectro/distribuição de CADA segmento
separadamente), `N_IAAFT_ITER=50` iterações por substituto, semente fixa
(`seed=12345`). Para cada par `i`, calcula-se `ΔC2_substituto_i =
C2(substituto_POST_i) - C2(substituto_PRE_i)`, formando a distribuição
nula de `ΔC2` sob "nenhuma mudança genuína de estrutura multifractal
além da variabilidade amostral de segmentos consistentes com um processo
linear". Teste BICAUDAL (ao contrário do teste unicaudal de
`critical-slowing-down`, que tinha previsão direcional clara da teoria):
`p = fração de substitutos com |ΔC2_substituto| >= |ΔC2_real|`. Bicaudal
porque, diferente de CSD, não há uma previsão teórica direcional
específica e verificada nesta sessão para a direção de `ΔC2` em onset de
crise epiléptica ou em terremoto (ganho ou perda de multifractalidade) —
declarar isso a priori, sem inventar uma direção, é a escolha honesta.

## Validação contra dado sintético (feita ANTES de tocar dado real)

Primeira tentativa de controle multifractal sintético (cascata binomial
clássica, Meneveau & Sreenivasan 1987, diferenciando a medida
multiplicativa) revelou uma ressalva metodológica real, não um bug:
substitutos IAAFT dessa cascata NÃO zeram o `C2_slope` (substitutos
ficaram entre -0,22 e -0,67, quase tão negativos quanto o real -0,59) —
porque essa construção produz uma distribuição marginal degenerada
(razão max/min ~190x), e o IAAFT preserva essa distribução marginal
exata junto com o espectro linear, o que sozinho já reproduz parte da
assinatura de log-cumulante, mesmo sem preservar a estrutura de cascata
genuína. Isso é uma limitação conhecida do IAAFT já documentada na
literatura para marginais muito pesadas/degeneradas — registrado aqui
honestamente em vez de escondido, e não usado como base de validação.

Controle multifractal substituto, mais bem-comportado e mais próximo do
tipo de processo esperado em dado físico real: ruído gaussiano modulado
por um envelope de cascata multiplicativa log-normal independente
(`x(t) = W(t)·G(t)`, W = cascata de fatores log-normais em árvore
diádica normalizada, G = ruído branco gaussiano) — construção padrão
para gerar intermitência/multifractalidade sintética sem uma marginal
degenerada. Resultado da validação (`n=2^13`, `sigma2=0,8`):

- fGn monofractal (H=0,6): `C2_slope=-0,129`.
- Multifractal (cascata-modulado): `C2_slope=-1,812` — claramente mais
  negativo.
- Substitutos IAAFT do sinal multifractal: `C2_slope` entre -0,37 e
  -0,84 (média -0,66, desvio-padrão 0,19) — deslocados para perto de
  zero em relação ao real, mas não exatamente zero (viés residual
  esperado e aceitável); crucialmente, o valor real (-1,81) fica MUITO
  fora dessa distribuição nula (`p_dC2=0,000` no teste de transição
  completo `PRE=mono, POST=multifractal`).
- Nulo negativo de controle (`PRE=mono, POST=mono` de sorteios
  diferentes do mesmo gerador): `p_dC2=0,45-0,67` — corretamente
  não-significativo nas duas checagens feitas.

Pipeline (`wtmm_common.py`) validado como capaz de distinguir
corretamente multifractalidade genuína de monofractalidade, e de não
disparar falsos positivos sob o nulo, ANTES de qualquer aplicação a
dado real.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING`, nenhum `PREREGISTRATION.md` travado.
