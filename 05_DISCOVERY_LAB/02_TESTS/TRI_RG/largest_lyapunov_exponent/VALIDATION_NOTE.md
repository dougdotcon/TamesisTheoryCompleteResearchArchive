# Nota de validação — `largest_lyapunov_exponent` (LLE, algoritmo de Rosenstein), ANTES de qualquer dado real

**Status: FINAL — candidato `largest_lyapunov_exponent` FECHADO NA ETAPA DE
VALIDAÇÃO.** Validação sintética obrigatória (`METHODOLOGY_NOTE.md`,
pipeline `analysis/lle_common.py`, script `analysis/validate_synthetic.py`)
concluída em DUAS tentativas de controle positivo pré-autorizadas (mapa
logístico, depois sistema de Rössler) — nenhuma estabeleceu poder real do
IAAFT em `lambda_1`/`D2`. Resultado completo em
`analysis/validation_synthetic.json`. **Nenhum dado real (Kīlauea 2018,
início explosivo de 17/05; MIT-BIH `afdb` registro `04936`) foi tocado em
nenhum momento desta linha de investigação para este candidato.**

## Resumo honesto do resultado

Este candidato reproduz, quase ponto-a-ponto, o mesmo achado estrutural já
documentado por `RQA` (`rqa/VALIDATION_NOTE.md`) — esperado, já que a
maquinaria de embedding (FNN de Kennel, Brown & Abarbanel 1992; informação
mútua de Fraser & Swinney 1986) é literalmente importada, não
reimplementada, de `rqa/analysis/rqa_common.py`:

**O controle positivo, exatamente como especificado em
`METHODOLOGY_NOTE.md` (PRE = ruído branco Gaussiano iid), não pôde ser
calculado.** FNN nunca cai abaixo do limiar de 1% para nenhum `m` em
`1..10` quando aplicado a ruído branco iid puro — a curva de fração de FNN
obtida aqui (`0,996 / 0,748 / 0,294 / 0,179 / 0,185 / 0,217 / 0,246 / 0,314
/ 0,408 / 0,531` para `m=1..10`) é praticamente idêntica à já observada por
`RQA` para o mesmo tipo de série (mínimo em `m=4`, ~17,9%, nunca cruzando
1%). Como `(m,tau)` é compartilhado entre `lambda_1` e `D2`, essa falha
bloqueia AMBOS os canais simultaneamente. O redesenho pré-autorizado (Passo
1b, PRE=fGn `H=0,7`, POST=Rössler) FOI executado (ver seção própria abaixo)
— o embedding resolveu desta vez, mas **nenhum dos dois canais mostrou
poder estatístico real contra o IAAFT**.

## Diagnóstico 0a — correção de código contra resposta analítica conhecida (embedding FORÇADO, mapa logístico)

Executado ANTES de qualquer controle de identificabilidade, como exigido
pela tarefa. Mapa logístico (`r=4`), `N=3.000`, embedding FORÇADO para
`m=2, tau=1` (contornando deliberadamente o gate de FNN **só para este
diagnóstico** — nunca feito na pipeline real, que sempre aplica o gate
obrigatório sem `m` forçado). `lambda_1` teórico = `ln(2) ≈ 0,693`
nats/iteração.

**Achado durante este diagnóstico, corrigido ANTES de qualquer controle
estocástico ou dado real:** a regra ingênua "maior janela estável entre
`m*,m*+1,m*+2`" (sem mais nada) é INSUFICIENTE — o platô de saturação da
curva de divergência de um atrator caótico limitado (distâncias saturam no
diâmetro do atrator após ~10-15 passos) é trivialmente "estável entre `m`"
(inclinação próxima de zero em todo `m`, satisfazendo a tolerância relativa
de forma vazia) e, por ser mais longo que a verdadeira região de
crescimento exponencial, VENCERIA a regra "maior janela", retornando
silenciosamente `lambda_1≈0` em vez da taxa de divergência genuína.
Confirmado numericamente: janela do platô (`i=12..199`) dá inclinação
`4,5e-5`, `R²=0,005`; janela inicial genuína (`i=0..9`) dá inclinação
`0,691`, `R²=0,99999`. **Correção, feita durante este diagnóstico de
código, ANTES de qualquer controle de identificabilidade:** adicionado um
critério conjunto de qualidade de ajuste `R²>=0,95` (`MIN_R2_FOR_LINEAR_
REGION`, documentado em `lle_common.py` e em `METHODOLOGY_NOTE.md`) — não é
uma reformulação de `R_lambda`/`I(X)` após ver resultado real ou de
controle, é um refinamento mecânico da regra de detecção automática de
região linear, feito ANTES de qualquer um desses cálculos.

Com a correção aplicada: `lambda_1=0,5631` (`R²=0,963`, janela `k=0..15`)
contra o teórico `0,693` — mesma ordem de grandeza, sinal correto, razoável
para uma estimativa automática de amostra finita (mesmo espírito do
`%DET=0,9994` de RQA "muito próximo de 1,0 mas não exato"). **Confirma que
o código de curva de divergência de Rosenstein + critério de convergência
de Kantz-Schreiber está correto** antes de testar em dado genuinamente
ambíguo.

## Diagnóstico 0b — sanidade da pipeline completa (gate de FNN ativo) em sinal periódico não-caótico

Onda senoidal determinística (período 50, `N=1.000`) com dither de `1e-6`
(mesma técnica/razão já usada por `RQA` — quebra recorrências exatas de
ponto flutuante que explodiriam o critério de razão do FNN). Pipeline
completa (SEM `m` forçado): `tau=5`, `m=4` resolvido normalmente por FNN.
`D2=0,967` (`R²=0,964`) — correto, perto de 1,0, já que uma órbita periódica
é uma curva fechada 1-D. **`lambda_1`: `linear_region_not_resolved`** —
resultado CORRETO, não uma falha: um sinal periódico tem expoente de
Lyapunov genuíno igual a zero, então não deveria existir uma região de
crescimento exponencial genuína a ser encontrada, e a pipeline
corretamente não "inventa" uma.

## Controles sintéticos de identificabilidade (`N=2.000`, `seed=12345`, `N_SURROGATES=200`)

### Controle positivo, tentativa 1 (`METHODOLOGY_NOTE.md`, especificação exata)

PRE = ruído branco Gaussiano iid. POST = mapa logístico caótico (`r=4`),
remapeado por posto sobre os valores exatos do PRE. Espectro confirmado
quase plano em ambos (`spectral_exponent_pre=-0,027`,
`spectral_exponent_post=+0,022`, praticamente idêntico ao já visto no
controle equivalente de RQA).

| Canal | Resultado |
|---|---|
| `tau` (PRE) | `2` (mínimo local de MI, `status=ok`) |
| `m` (PRE, FNN) | **NÃO RESOLVIDO** — fração mínima de FNN = 17,9% em `m=4`, curva completa: `99,6% / 74,8% / 29,4% / 17,9% / 18,5% / 21,7% / 24,6% / 31,4% / 40,8% / 53,1%` |
| `lambda_1`, `D2` | **indefinidos** — embedding compartilhado nunca fixado |
| `p_lambda1`, `p_d2` | **indefinidos** (não "não significativo") |

### Controle negativo (dois sorteios independentes de fGn-like, `H=0,7` fixo)

Sonda diretamente o risco espectral/linear — e, ao contrário do ruído
branco, resolve o embedding (`m=4, tau=49`), permitindo exercitar a
pipeline completa (embedding + Rosenstein + Kantz-Schreiber + `D2` + IAAFT)
de ponta a ponta.

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | `n` válido/indefinido | `p` (bicaudal) | veredito |
|---|---|---|---|---|---|---|---|---|
| `lambda_1` | 0,002431 | 0,005214 | +0,002783 | −0,000428 | 0,001833 | 194/6 | **0,103** | corretamente não significativo |
| `D2` | 1,8619 | 1,7440 | −0,117959 | 0,185288 | 0,487997 | 200/0 | **0,79** | corretamente não significativo |

`R²` da região linear de `lambda_1` ficou alto em ambos (`PRE=0,972`,
`POST=0,996`) — confirma que a região identificada é uma região
genuinamente linear, não um artefato do gate de `R²>=0,95` recém-adicionado
selecionando algo espúrio. `n=194/200` substitutos válidos em `lambda_1`
(6 substitutos IAAFT tiveram embedding/região linear não resolvidos —
esperado e tratado como indefinido, não como zero), `n=200/200` em `D2`.

## Redesenho do controle positivo (Passo 1b, pré-autorizado em `METHODOLOGY_NOTE.md`, acionado mecanicamente pelo resultado acima)

Como o controle positivo v1 bateu em `embedding_not_resolved` — o MESMO
modo de falha exato já visto por `RQA` — o protocolo de decisão pré-fixado
em `METHODOLOGY_NOTE.md` foi acionado automaticamente (não por decisão
deste agente): trocar a fonte do sinal caótico de POST do mapa logístico
para o sistema de Rössler (`a=0,2, b=0,2, c=5,7`, RK4, `dt_internal=0,01`,
`sample_dt=0,15` — mesmos parâmetros já validados por `RQA` por darem um
expoente espectral próximo do alvo do fGn `H=0,7`), mantendo PRE=fGn-like
`H=0,7` e a mesma técnica de remapeamento por posto.

### Casamento espectral (reportado honestamente, sem exigir perfeição)

| Série | Expoente espectral |
|---|---|
| PRE (fGn H=0,7) | 2,3726 |
| Rössler bruto (antes do remap) | 2,3968 |
| POST (Rössler remapeado sobre PRE) | 1,9583 |

Casamento bom mas não perfeito — idêntico ao padrão já visto na validação
de RQA (mesma técnica, mesmos parâmetros de Rössler).

### Resultado — embedding RESOLVE (confirma que a correção de desenho funciona nesse nível)

| | Valor |
|---|---|
| `tau` (PRE) | 40 |
| `m` (PRE, FNN) | 4 (`status=ok`) — **mesmo `(m,tau)=(4,40)` encontrado por RQA para o par PRE/POST equivalente**, esperado dado o mesmo código/técnica de geração |
| `lambda_1` PRE / POST / Δ | 0,004569 / 0,016970 / **+0,012401** |
| `D2` PRE / POST / Δ | 1,17969 / 1,49470 / **+0,315007** |
| média nula IAAFT (`lambda_1`) | −0,036581 (desvio 0,054270) |
| média nula IAAFT (`D2`) | −0,043512 (desvio 0,257867) |
| `p_lambda1` (bicaudal, `n=200`) | **1,0** |
| `p_d2` (bicaudal, `n=200`) | **0,16** |
| σ-equivalente | `lambda_1`: ≈0,90σ · `D2`: ≈1,39σ |
| `R²` da região linear de `lambda_1` (PRE/POST) | 0,959 / 0,958 (regiões genuinamente lineares, não artefato do gate) |

**Resultado: `p_lambda1=1,0` (o valor bicaudal menos significativo
possível — o Δ real fica dentro da massa central da distribuição nula, não
nas caudas) e `p_d2=0,16` (não cruza o limiar `p<0,05`).** Nenhum dos dois
canais mostra separação clara da nula IAAFT, apesar de o embedding ter
resolvido normalmente e as regiões lineares identificadas serem
genuinamente bem ajustadas (`R²` alto).

## Teste do fallback de bootstrap (pré-autorizado, testado explicitamente)

`METHODOLOGY_NOTE.md` pré-autoriza bootstrap por blocos móveis (Kunsch
1989) como teste PRIMÁRIO complementar apenas para um padrão de BAIXO
PODER (não para não-computabilidade estrutural). A máquina de bootstrap
(`run_block_bootstrap_test_lle`, reaproveitando `moving_block_bootstrap_
resample` de `rqa_common.py`) está pronta em `lle_common.py`. Testado
diretamente aqui na caracterização estrutural (não assumido): **25
reamostras de blocos móveis (`L=20`) do mesmo ruído branco do controle
positivo v1 — 0/25 resolveram o embedding (`m<=10`)** — idêntico ao achado
de RQA, confirma que este é o mesmo tipo de parede estrutural (não um
problema de poder do IAAFT que o bootstrap pudesse consertar). Dado que o
controle positivo v2 (Rössler) TEVE seu embedding resolvido mas mesmo assim
não mostrou poder real, o bootstrap não foi formalmente acionado como
teste PRIMÁRIO de significância para v2 — a regra de acionamento em
`METHODOLOGY_NOTE.md` é para um padrão de baixo poder JÁ estabelecido
noutra linha (DFA-alpha), e aqui o resultado de v2 já é decisivo por si só
sob o protocolo IAAFT primário, sem ambiguidade que justificasse acionar o
fallback antes de aplicar o veredito mecânico abaixo.

## Caracterização da parede estrutural (fronteira de resolubilidade do FNN, confirmando — não assumindo — que reproduz a de RQA)

| Verificação | Resultado |
|---|---|
| Varredura fGn-like, `H` fixo, `N=2.000` | `H=0,1`: falha. `H=0,3` a `H=0,9`: resolve (`m` entre 3 e 8) |
| Varredura AR(1), `phi` fixo, `N=2.000` | `phi=0,0` a `phi=0,9`: falha. `phi=0,95`: resolve (`m=7`) |
| Bootstrap em ruído branco | `0/25` reamostras resolveram o embedding |

Resultado praticamente idêntico ao já documentado por RQA (esperado — MESMO
código de `estimate_tau`/`estimate_m`, importado sem modificação) —
confirma que a fronteira de resolubilidade não é peculiar a este
candidato, é uma propriedade do gate de FNN travado (`R_tol=10, A_tol=2,
m<=10`) compartilhado por ambas as candidaturas.

## Veredito FINAL — aplicado mecanicamente, sem desvio

Per `METHODOLOGY_NOTE.md`, protocolo de decisão pré-fixado para o passo
único de redesenho: **nenhum dos dois canais (`lambda_1`, `D2`) mostrou
poder real sob o segundo desenho** (`p_lambda1=1,0`, `p_d2=0,16`, ambos
`IAAFT_LOW_POWER`). Portanto:

> **O candidato `largest_lyapunov_exponent` é FECHADO NA ETAPA DE
> VALIDAÇÃO — a identificabilidade de `lambda_1`/`D2` sob a convenção de
> embedding travada (`R_tol=10`, `A_tol=2`, `m<=10`, janela de Theiler via
> período orbital médio, critério de convergência de Kantz-Schreiber com
> `R²>=0,95`) não pôde ser estabelecida com NENHUM dos dois desenhos de
> controle positivo tentados (mapa logístico nem Rössler). Nenhum dado real
> (Kīlauea 2018, MIT-BIH `afdb`) foi tocado em nenhum momento desta linha
> de investigação para este candidato. Este é um resultado válido, honesto
> e completo — "identificabilidade não estabelecida na validação
> sintética" —, não um resultado parcial, abandonado, ou uma falha a
> esconder. Nenhuma terceira tentativa de redesenho foi feita, conforme
> pré-autorizado e travado ANTES de ver este resultado.**

## Uma distinção honesta em relação a `RQA`, nomeada explicitamente

Diferente de `RQA` (onde o controle positivo v2/Rössler também falhou, mas
de forma extrema — `p=1,0` em ambos os canais, com o Δ real MENOR em
magnitude que quase todos os 200 substitutos), aqui o resultado é misto:
`lambda_1` falha de forma tão decisiva quanto RQA (`p=1,0`), mas `D2`
chega bem mais perto do limiar (`p=0,16`, σ-equivalente `≈1,39`) sem
cruzá-lo. Isto é reportado aqui com honestidade, não escondido: `D2` não
mostrou poder estatisticamente significativo sob o critério pré-declarado
(`p<0,05`), então o protocolo de decisão mecânico se aplica exatamente da
mesma forma — mas o valor numérico em si sugere que, com um controle
positivo ainda melhor casado espectralmente ou um `N` maior, `D2`
especificamente poderia eventualmente separar-se da nula. Isso NÃO
justifica uma terceira tentativa (não autorizada por `METHODOLOGY_NOTE.md`,
disciplina de escalonamento desta linha) — é reportado apenas como um
detalhe honesto do resultado, não como uma abertura para mais tentativas.

## Nenhum desvio metodológico além do pré-autorizado

As regras de `tau`, `m` (gate de FNN obrigatório, hard reject), janela de
Theiler, região de ajuste linear (incluindo o gate `R²>=0,95` adicionado
durante o diagnóstico de código, ANTES de qualquer controle estocástico),
teto de subamostragem, e o protocolo IAAFT permanecem exatamente como
fixados em `METHODOLOGY_NOTE.md`, sem reformulação alguma depois de ver
qualquer resultado de controle ou dado real. **Este agente NÃO decidiu
retirar `lambda_1` ou `D2` do critério de decisão** — essa é uma decisão de
governança que cabe à sessão orquestradora, per o mesmo princípio já usado
em `RQA`.

## Estado da linha após este fechamento

Com este candidato, `largest_lyapunov_exponent` (13º candidato identificado
para `DISC-TRI-RG-001`, 2º dos 3 novos da Fase 0.7) é o **2º candidato
consecutivo desta linha (depois de `RQA`) a fechar inteiramente na etapa de
validação sintética**, pelo MESMO motivo estrutural raiz (gate de FNN
compartilhado, herdado por importação de código, não coincidência). Registro
de `RESULTS_SUMMARY.md`, `TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md` para
esta linha fica a cargo da sessão orquestradora.
