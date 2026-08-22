# Nota adversarial (plano + sementes) — mecanismo M-WEIB(β), intermediate_alpha_search (onda 5, DISC-DEC-022)

**Gravado ANTES de qualquer execução numérica desta verificação.**
**Data/hora (UTC):** 2026-08-22.

## Disciplina de leitura (cumprida)

Li: (1) o parágrafo-alvo do mandato (resumo da alegação, reproduzido
abaixo); (2) `../../DERIVATIONS.md` inteiro (fórmula-mestre M-q §1,
lei do expoente + piso/teto §2, mecanismos §3, tabela §5); (3)
`../../../theorem/THEOREM.md` §0–6 (Definição 3, Teorema 1 e sua prova
completa — a "identidade nuclear" Step 4, `P(sucesso em s)=1-t`
independente de `s`); (4) `MECANISMO_ALPHA_INTERMEDIARIO.md` **apenas**
o VEREDITO EXECUTIVO (linhas 1–46) — o suficiente para fixar a
definição operacional de M-WEIB(β) ("processo de Poisson não-homogêneo
com intensidade em forma de Weibull, mesma regra de destino uniforme de
M-U").

**NÃO li:** §1 (busca de literatura), §2 (derivação própria, incl.
2.1–2.7), §3 (validação numérica), §4 (near-misses) do arquivo-alvo;
`verify_algebra.py`, `continuum_sim.py`, `finiten_sim.py`,
`supplementary_checks.py` nem seus logs/JSONs. Todos os simuladores e
re-derivações abaixo são escritos do zero a partir da definição
operacional apenas.

## Alvo (conforme entendido do mandato, a verificar)

M-WEIB(β): mesma regra de destino de M-U (destino uniforme em [0,1),
kill prob = massa já visitada = s), mas a taxa de eventos de reroteamento
deixa de ser constante `c` e passa a ser um processo de Poisson não-
homogêneo com função-valor-médio (cumulativa) `Λ(t)=c·t^β` (jargão de
confiabilidade: "processo Weibull", intensidade instantânea
`λ(t)=Λ'(t)=cβt^{β-1}`, decrescente para β<1 = "mortalidade infantil").
Alegação central: bracket(s,t)=t exatamente, H(t)=t·Λ(t)/c, fórmula
fechada φ_WEIB(c;β)=∫₀¹e^{-c·t^{1+β}}dt, α=1/(1+β)∈(1/2,1) para
β∈(0,1), M-U recuperado em β→1, mecanismos α=1 recuperados em β→0,
alegadamente FORA da família M-q, validado por 2 simuladores próprios
deles (evento-contínuo e finito-n até n=32768).

## (1) Re-derivação própria (rota independente, ANTES de rodar qualquer script)

Generalizo a prova do Teorema 1 (THEOREM.md §3, Definição 3) trocando o
processo de Poisson homogêneo de taxa `c` por um processo de Poisson
NÃO-homogêneo de intensidade determinística `λ(s)` (função-valor-médio
`Λ(t)=∫₀ᵗλ`), mantendo TUDO o resto idêntico (regra de destino uniforme
⇒ kill prob `q(s)=s`; relógio de fechamento padrão `T=s+(1-s)(1-e^{-E})`,
`E~Exp(1)`).

- **Passo 1** (T₀~Unif(0,1), independente do resto): inalterado — só
  usa que E₀ é independente de tudo mais, não usa a taxa do processo.
- **Passo 2** (evento {x₀ cíclico}∩{T₀=t} = interseção sobre marcas
  antes de t): inalterado — é puramente combinatório sobre a ordem das
  marcas e do relógio de fechamento, não usa a taxa.
- **Passo 3** (restrição de um processo de Poisson a [0,t) é Poisson
  com a intensidade restrita, independente do resto): fato-padrão de
  processos de Poisson que vale para intensidade DETERMINÍSTICA
  qualquer, não só constante (incrementos independentes sobre
  conjuntos disjuntos é a própria definição via medida de intensidade).
- **Passo 4** (probabilidade de sucesso por marca em `s<t`): cálculo
  IDÊNTICO ao Teorema 1 — depende só de UMA marca condicionada a estar
  em `s`, usa apenas a regra de kill `q(s)=s` e o relógio de
  fechamento; não envolve a taxa do processo em nenhum ponto.
  `P(sucesso em s) = (1-s)·(1-t)/(1-s) = 1-t`, independente de `s`
  — **exatamente a mesma identidade "bracket=t", e por construção ela
  sobrevive a QUALQUER perfil de taxa `λ(s)`**, pois a taxa nunca entra
  no cálculo do Passo 4.
- **Passo 5** (marcação/afinamento de Poisson, generalizado): para um
  processo de Poisson (homogêneo ou não) de intensidade `λ(s)`,
  afinado por uma probabilidade de "falha" que aqui é CONSTANTE (`=t`,
  independente de `s`, pelo Passo 4), o número de marcas "falhas" em
  `[0,t)` é Poisson com média `∫₀ᵗλ(s)·t ds = t·∫₀ᵗλ(s)ds = t·Λ(t)`.
  Isso é o teorema de marcação/afinamento padrão para processos de
  Poisson não-homogêneos (Kingman 1993 cap. 5), não precisa de `λ`
  constante.

⇒ `P(x₀ cíclico | T₀=t) = e^{-t·Λ(t)}`, logo (definindo H(t):=t·Λ(t)/c
para casar com a convenção `exp(-c·H(t))`, `H(1)=1`):

**H(t) = t·Λ(t)/c — CONFIRMO a identidade, exatamente, para QUALQUER
perfil `Λ` (não só Weibull), contanto que a regra de destino permaneça
a de M-U (`q(s)=s`).** Não encontrei nenhum termo descartado
incorretamente; a "razão" da identidade é mais forte do que o
relatório sugere — não é uma coincidência do perfil Weibull, é uma
propriedade de QUALQUER perturbação pura-da-taxa sob a regra M-U.

Com `Λ(t)=c·t^β`: H(t) = t·(c t^β)/c = t^{1+β} ⇒
**φ_WEIB(c;β) = ∫₀¹ e^{-c·t^{1+β}} dt — CONFIRMO a forma fechada.**

**Cauda (Watson/Laplace, feita à mão):** substituição `u=c^{1/(1+β)}t`:
∫₀¹e^{-ct^{1+β}}dt = c^{-1/(1+β)}∫₀^{c^{1/(1+β)}}e^{-u^{1+β}}du →
c^{-1/(1+β)}·Γ(1+1/(1+β)) quando c→∞ (cauda do integrando decai
exponencialmente além de u~O(1), erro exponencialmente pequeno).
**CONFIRMO α=1/(1+β)**, com coeficiente Γ(1+1/(1+β)) (checagem:
β=1 ⇒ Γ(3/2)=√π/2, bate com M-U exato).

## (2) A questão central de robustez: M-WEIB é REALMENTE fora de M-q?

Ideia a testar (mandato item 5, antes de rodar nada): a classe M-q é
definida por TAXA CONSTANTE `c` + `q(s)` livre. M-WEIB usa `q(s)=s` FIXO
(igual a M-U) + taxa livre. Isso são dois eixos de generalização
DIFERENTES do mesmo objeto de partida. Pergunta: será que o `φ_WEIB(c;β)`
— como FUNÇÃO de `c` — coincide EXATAMENTE com `φ_q(c)` de algum `q(t)`
válido (0≤q≤1) da família M-q?

Como a fórmula mestre de M-q dá `H_q(t) = t-(1-t)∫₀ᵗ(1-q(s))/(1-s)ds`
e essa relação é LINEAR (portanto invertível) em `q`, resolvo
analiticamente (à mão, ANTES de rodar) `H_q(t)=t^{1+β}` para `q(t)`:

`q(t) = [(1+β)t^β - β t^{1+β} - t] / (1-t)`

(checagem em β=1: dá q(t)=t, i.e. M-U exatamente ✓; em β=0: dá q≡1 ✓,
casando com DERIVATIONS.md "q≡1 ⇒ H=t"). **Predição pré-registrada a
testar numericamente:** para β∈(0,1) este `q(t)` deve permanecer em
[0,1] em todo o domínio (tornando M-WEIB(β<1) EXATAMENTE reproduzível
dentro de M-q, o que enfraqueceria a alegação "genuinamente fora de
M-q" ao nível do observável φ(c), mesmo que o MECANISMO microscópico
seja de fato diferente); para β>1 este mesmo `q(t)` deve sair de [0,1]
em algum ponto do domínio (o que explicaria e sustentaria, de forma
limpa, por que só o lado β>1 pode furar o piso α≥1/2 sem contradizer o
teorema piso/teto — a família M-q inteira, por definição, não alcança
esse `H(t)`). Isso será checado numericamente em
`mq_equivalence.py` antes de qualquer outra simulação, por ser
cálculo determinístico (sem Monte Carlo).

## (3) Simuladores próprios (do zero, sem ver o código deles)

**Simulador A (evento-contínuo, "amostragem direta do processo
misto").** Diferente da rota de "explorar por Definição 3 genérica": eu
amostro primeiro `K~Poisson(c)` (nº total de marcas), depois as `K`
posições i.i.d. via `S=U^{1/β}` (`U~Unif(0,1)`) — isso é exatamente
Beta(β,1), a lei condicional de uma marca de um processo de Poisson não-
homog. de intensidade `λ(s)=cβs^{β-1}` dado o total `K` (fato-padrão de
processos de Poisson, verificado por CDF: `P(U^{1/β}≤x)=P(U≤x^β)=x^β`).
Depois simulo Θ_j~Unif(0,1) (kill se Θ_j<S_j), E_j~Exp(1) (relógio de
fechamento), corro o laço de exploração (implementação própria) e
registro se x₀ é cíclico. Grade: β∈{0.25,0.5,0.75,0.9} (0.9 fora da
grade deles — teste extra pedido pelo mandato), c∈{0.5,1,2,4,8,16,32,64}
(grade DIFERENTE da grade típica c∈{0.5,2,10,40,160} usada nas
verificações adversariais anteriores desta árvore, para não repetir
acidentalmente a mesma grade). N_trials por célula: 300 000 (orçamento
de tempo).

**Teste cirúrgico da identidade (não é o φ(c) completo — testa H(t)
diretamente):** para uma grade de `t` fixos (0.1,0.3,0.5,0.7,0.9),
`β∈{0.25,0.5,0.75}`, `c∈{1,4,16}`, amostro SÓ as marcas em `[0,t)`
(`K_t~Poisson(Λ(t))`, posições `S=t·V^{1/β}`), decido falha/sucesso por
marca (Θ<S ⇒ kill; senão relógio `T=S+(1-S)(1-e^{-E})`, falha se
`T≤t`), com 300 000 réplicas por célula, e comparo `P̂(zero falhas)`
contra `e^{-t·Λ(t)}` teórico. Isso ataca DIRETAMENTE a alegação
"bracket(s,t)=t independente de s" sem passar pela integral em t.

**Simulador B (finito-n, revelação preguiçosa da permutação +
reroteamento dependente do RANK de visitação, não do rótulo fixo).**
Ponto de cuidado identificado ANTES de programar: a taxa de M-WEIB deve
depender da FRAÇÃO DE MASSA JÁ EXPLORADA AO LONGO DA ÓRBITA de x₀ — uma
quantidade dinâmica revelada passo a passo — e NÃO de um rótulo fixo
`i/n` externo (marcar por rótulo fixo, independente da ordem de
visitação, produziria de fato uma taxa efetivamente CONSTANTE no limite,
já que `π` é uniforme e a ordem de visitação é uma ordem aleatória
"cega" aos rótulos — essa é precisamente a razão estrutural, também
usada em DERIVATIONS.md §0/§1, de por que o modelo `M_n(c)` de rótulo
fixo dá taxa constante `c` no limite contínuo). Implementação: revelo
`π` preguiçosamente a partir de `x₀`; no passo `k` (tendo já explorado
`k-1` pontos, massa `≈(k-1)/n`), decido reroteamento com probabilidade
`Λ(k/n)-Λ((k-1)/n)` (construção padrão de discretização de processo de
Poisson não-homog. por incrementos), destino uniforme em `[n]` se
reroteado, senão sigo `π` revelado preguiçosamente (próximo alvo
uniforme entre os ainda não usados como imagem, incluindo a possibilidade
de fechar em x₀). `n∈{2000,8000,32768}`, mesma grade de β acima,
c∈{1,4,16} (subgrade, para caber no orçamento de tempo — n=32768 é
caro). Trials: 20000 (n=2000,8000), 4000 (n=32768).

## Sementes

`numpy.random.default_rng` com sementes fixas e DIFERENTES por
simulador/grade, escolhidas ANTES de rodar, sem tentativa-e-erro:
- Simulador A (φ completo): seed 20260822
- Teste cirúrgico H(t): seed 20260823
- Simulador B (finito-n): seed 20260824
- q(t)-equivalência (determinística, sem semente)

## Critério de veredito (fixado antes de rodar)

- (a) Identidade H(t)=t·Λ(t)/c: CONFIRMADA se `P̂(zero falhas)` cai
  dentro de ~3 erros-padrão binomiais de `e^{-tΛ(t)}` em ≥ 90% das
  células da grade cirúrgica.
- (b) Forma fechada + expoente: CONFIRMADA se φ̂(c;β) do Simulador A
  cair dentro de ~3σ Monte Carlo da quadratura numérica de
  ∫₀¹e^{-ct^{1+β}}dt em todas as células, E se α̂ (ajuste log-log em c
  grande) bater com 1/(1+β) dentro de ~0.05 de tolerância absoluta.
- (c) "Fora de M-q": estrutura EXATA — não é um teste estatístico, é a
  checagem determinística de se `q(t)` (fórmula acima) permanece em
  [0,1] para β<1 e sai de [0,1] para β>1. O veredito aqui é sobre a
  ALEGAÇÃO DE NOVIDADE, não sobre a correção matemática da forma
  fechada (que já terá sido confirmada em (a)/(b)).
- (d) Reprodução numérica finito-n: qualitativa — declínio de α̂ com
  n crescente do viés vs. o valor contínuo, mesmo padrão do relatório
  do front (não uma réplica exata, já que a grade/sementes são
  diferentes).

Nenhum dos resultados acima foi visto antes de escrever esta nota.
