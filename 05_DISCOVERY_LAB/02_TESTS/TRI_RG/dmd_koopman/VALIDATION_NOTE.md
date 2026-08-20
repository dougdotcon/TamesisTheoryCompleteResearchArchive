# Nota de validação — `dmd_koopman`, ANTES de qualquer dado real

**Status: VALIDAÇÃO PASSA (com o único ajuste pré-autorizado aplicado).**
Candidato segue para dado real (Itália COVID-19, lockdown de 09/03/2020;
Kīlauea 2018, fissura de 03/05/2018) com a pipeline (`analysis/dmd_common.py`)
travada exatamente como usada na validação — nenhuma modificação adicional
de `R_lambda`/`I(X)`/protocolo de significância depois deste ponto.

Script: `analysis/validate_synthetic.py`. Resultado completo:
`analysis/validation_synthetic.json`.

## Resumo honesto do resultado

Diferente de `rqa`/`largest_lyapunov_exponent` (ambos fechados na
validação por um gate de embedding — FNN — que estruturalmente nunca
resolve para ruído/fGn de baixo `H`), este candidato usa um tipo de gate
diferente (seção 1.3 de `METHODOLOGY_NOTE.md`): uma regra de suficiência
de COMPRIMENTO, não de resolubilidade dinâmica — o truncamento de posto
de Gavish-Donoho sempre retorna algum posto `r>=1`, então a pergunta
relevante não é "o embedding resolve?" mas "o canal de
frequência/amortecimento tem poder discriminativo real sob IAAFT?". Esta
pergunta foi testada diretamente com o controle positivo nomeado pela
sondagem da Fase 0.7: um oscilador de Stuart-Landau ruidoso com o
parâmetro de bifurcação de Hopf `mu` variando de foco estável (`mu<0`)
para ciclo-limite (`mu>0`).

**Resultado: o canal `zeta` (razão de amortecimento) mostra poder
discriminativo real e fisicamente correto, com o sinal esperado, tanto na
tentativa 1 quanto na 2 (mais fortemente na 2, após o único ajuste
pré-autorizado). O canal `f_dom` (frequência) mostra um sinal mais fraco,
como previsto a priori em `METHODOLOGY_NOTE.md` §4.1 — a forma normal
cúbica literal de Stuart-Landau não tem acoplamento amplitude-frequência,
então "amolecimento de frequência" não é a assinatura esperada deste
sistema específico; o colapso de amortecimento é.** O controle negativo
não mostrou nenhum sinal falso-positivo em nenhuma das duas tentativas —
checagem de especificidade limpa.

## 0. Diagnóstico de correção de código — senoide pura

`x(t) = sin(2*pi*0,05*t)`, `N=2.000`, dither `1e-6`. Pipeline completa
(SEM `d`/`tau` forçados): `tau=3` (MI), `d=100` (`D_MAX`, teto).

| Canal | Recuperado | Esperado |
|---|---|---|
| `f_dom` | `0,050000000012` | `0,05` (exato) |
| `zeta` | `-2,66e-11` | `~0` (não-amortecido) |
| `n_complex_pairs` | `1` | pelo menos 1 |

**Confirma que Hankel + Gavish-Donoho + DMD exato + extração de
frequência/amortecimento produzem exatamente o valor teórico esperado**
antes de testar em dinâmica estocástica genuinamente ambígua — sinal de
correção de código limpo, sem qualquer discrepância a corrigir.

## 1. Controle positivo, tentativa 1 (`sigma=0,05`, especificação exata de `METHODOLOGY_NOTE.md`)

Stuart-Landau ruidoso, `omega=1,0`, `mu_pre=-0,3` (foco estável),
`mu_post=+0,3` (ciclo-limite), `N=4.000` por segmento, `dt_internal=0,01`,
`sample_dt=0,1` (decimação 10x), transiente de 2.000 passos internos
descartado, sementes de ruído independentes (101 para PRE, 202 para
POST).

Pipeline: `tau=15`, `d=100` (teto `D_MAX`), `r`(PRE)=16, `r`(POST)=28
(Gavish-Donoho, posto recalculado por condição). Ambos os segmentos
recuperaram pares complexo-conjugados normalmente (`n_complex_pairs`
PRE=8, POST=14; `n_real_modes`=0 em ambos — nenhum modo real dominante
sobreviveu ao truncamento de posto neste sistema, então o diagnóstico
`real_dominant_rate` fica `no_real_mode`, reportado honestamente, não um
erro).

| Canal | PRE | POST | Delta | `p` (bicaudal, `n=200`) |
|---|---|---|---|---|
| `f_dom` | 0,013303 | 0,016103 | +0,002800 | 0,23 |
| `zeta` | 0,115936 | 0,000365 | **-0,115571** | 0,085 |
| gap espectral | 0,000927 | 0,000565 | -0,000362 | 0,71 |

`zeta` colapsa de `~0,12` (foco amortecido) para `~0,0004` (praticamente
não-amortecido, consistente com um ciclo-limite genuíno) — direção
FISICAMENTE CORRETA e de grande magnitude — mas `p=0,085`, não cruza o
limiar `p<0,05`. `f_dom` mal se move (`p=0,23`). Gap espectral não mostra
sinal (`p=0,71`) — esperado, já que não é o canal alvo desta hipótese.
**Por `METHODOLOGY_NOTE.md` §4.1/§4.3, nem `f_dom` nem `zeta` cruzaram
`p<0,05`: o gatilho de correção pré-declarado é acionado mecanicamente.**

## 2. Controle negativo, tentativa 1

Duas realizações independentes do MESMO processo (`mu_pre=mu_post=-0,3`,
sementes 303/404), mesmos `omega`, `sigma`, `N`.

| Canal | Delta real | `p` (bicaudal) |
|---|---|---|
| `f_dom` | -0,000725 | 0,575 |
| `zeta` | +0,019780 | 0,655 |
| gap espectral | +0,003863 | 0,07 |

Nenhum canal cruza `p<0,05` — checagem de especificidade correta (sem
falso-positivo quando não há bifurcação genuína).

## 3. Correção pré-autorizada (ÚNICA), acionada mecanicamente pelo resultado da seção 1

Per `METHODOLOGY_NOTE.md` §4.3: `sigma` aumentado de `0,05` para `0,15`
(ruído aditivo mais forte, mais próximo do regime realisticamente ruidoso
de dado real observado nesta linha), mantendo `mu_pre=-0,3`,
`mu_post=+0,3`, `omega=1,0`, `N=4.000`, e TODO o resto (`R_lambda`,
`I(X)`, regra de PRE/POST, protocolo de significância) intacto.

### Controle positivo, tentativa 2 (`sigma=0,15`)

Pipeline: `tau=17`, `d=100`, `r`(PRE)=14, `r`(POST)=24.

| Canal | PRE | POST | Delta | `p` (bicaudal, `n=200`) |
|---|---|---|---|---|
| `f_dom` | 0,013452 | 0,016153 | +0,002701 | 0,08 |
| `zeta` | 0,165821 | 0,002672 | **-0,163149** | **0,03** |
| gap espectral | 0,001938 | 0,001582 | -0,000355 | 0,835 |

**`p_zeta=0,03 < 0,05` — o canal de amortecimento mostra poder
discriminativo real, mesma direção física e magnitude ainda maior que na
tentativa 1.** `f_dom` chega perto (`p=0,08`) mas não cruza o limiar —
consistente com a previsão a priori (§4.1 de `METHODOLOGY_NOTE.md`) de
que o colapso de amortecimento, não a mudança de frequência, é a
assinatura esperada desta forma normal específica.

### Controle negativo, tentativa 2 (`sigma=0,15`)

| Canal | Delta real | `p` (bicaudal) |
|---|---|---|
| `f_dom` | -0,000922 | 0,615 |
| `zeta` | +0,022965 | **0,79** |
| gap espectral | +0,004344 | 0,1 |

Nenhum canal significativo — a mesma checagem de especificidade limpa se
mantém com o `sigma` maior, confirmando que o `p=0,03` do controle
positivo não é um artefato de `sigma` maior por si só (que aumentaria a
variância dos substitutos indiscriminadamente) — é especificamente a
mudança de regime (`mu_pre` -> `mu_post`) que produz o sinal.

## Veredito FINAL — aplicado mecanicamente

Per `METHODOLOGY_NOTE.md`, protocolo de decisão pré-fixado: **o canal
`zeta` mostrou poder discriminativo real sob o controle positivo
corrigido (`p=0,03<0,05`), com direção fisicamente correta em ambas as
tentativas e nenhum falso-positivo no controle negativo correspondente.**
Portanto:

> **A validação sintética obrigatória PASSA. O candidato `dmd_koopman`
> prossegue para dado real (Itália COVID-19, Kīlauea 2018) com a pipeline
> travada exatamente como usada nesta validação — `HANKEL_D_DIVISOR=10,
> D_MIN=10, D_MAX=100`, Gavish-Donoho (caso de ruído desconhecido, fórmula
> geral dependente de `beta`), DMD exato (Tu et al. 2014), seleção do par
> complexo-conjugado de maior `|lambda|`, protocolo IAAFT primário
> (`N_SURROGATES=200, N_IAAFT_ITER=50, seed=12345`) — nenhuma modificação
> adicional depois deste ponto. Nenhuma segunda correção foi feita ou será
> feita, per a disciplina de escalonamento desta linha.**

## Caveats honestos, nomeados explicitamente antes de tocar dado real

1. **`f_dom` não mostrou poder discriminativo significativo em nenhuma das
   duas tentativas** (`p=0,23` e `p=0,08`) — o canal primário sobrevivente
   é especificamente `zeta`, não o par completo `(f_dom, zeta)` como um
   bloco. Isto será reportado honestamente nos resultados de dado real:
   se `f_dom` também não mostrar sinal lá, isso é consistente com este
   achado de validação, não uma surpresa a esconder.
2. **`n_real_modes=0` em todos os 4 segmentos sintéticos testados** — o
   diagnóstico do autovalor real demovido (seção 2.3 de
   `METHODOLOGY_NOTE.md`) não pôde ser calculado (`no_real_mode`) para
   este sistema. Isto é esperado para um oscilador de Stuart-Landau puro
   (a dinâmica é inteiramente rotacional/oscilatória, sem um modo de
   decaimento puramente real dominante sobrevivendo ao truncamento de
   posto) — não indica um problema com o canal diagnóstico em si, que
   pode muito bem resolver normalmente em dado real com uma componente de
   decaimento mais forte (ex.: contagens de casos de COVID, que têm uma
   componente de crescimento/decaimento monótono clara além de qualquer
   oscilação).
3. **`p` de amostra única, sem múltiplas sementes de ruído sintético
   independentes** — o resultado da seção 3 é reproduzível (sementes
   fixas), mas não foi replicado com sementes de ruído sintético
   adicionais para checar a estabilidade exata do valor `p=0,03` (que
   está perto o bastante do limiar `0,05` que uma segunda semente
   plausivelmente poderia empurrar para o outro lado). Isto NÃO é uma
   razão para uma terceira tentativa (não autorizada) — é nomeado aqui
   como um caveat honesto sobre a força da evidência de validação, não
   como uma abertura para mais ajuste. O resultado em dado real (com
   `N_SURROGATES=200` completo e sementes idênticas de produção,
   `seed=12345`) é o teste que decide o candidato, não a validação
   sintética em si.

## Nenhum desvio metodológico além do pré-autorizado

As regras de `tau` (MI, reaproveitado de `rqa_common`), `d` (regra de
comprimento, seção 1.3), truncamento de posto (Gavish-Donoho), DMD exato,
seleção do par complexo primário, gap espectral companheiro, diagnóstico
de autovalor real demovido, e o protocolo IAAFT permanecem exatamente
como fixados em `METHODOLOGY_NOTE.md`, sem reformulação alguma depois de
ver qualquer resultado de controle. O único ajuste feito (`sigma:
0,05->0,15`) foi especificado a priori na própria `METHODOLOGY_NOTE.md`
§4.3, ANTES de rodar o controle positivo tentativa 1, e foi acionado
mecanicamente pelo resultado, não por decisão deste agente após ver o
número.
