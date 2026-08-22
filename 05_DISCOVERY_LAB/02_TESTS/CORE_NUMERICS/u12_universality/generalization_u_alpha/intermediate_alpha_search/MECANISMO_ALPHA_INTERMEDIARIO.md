# MECANISMO_ALPHA_INTERMEDIARIO — busca por um mecanismo intrínseco natural com α ∈ (1/2, 1)

**Linha:** DISC-CORE-NUMERICS-001, frente `u12-generalization-u-alpha`
(onda 3, DISC-DEC-015; onda 4 do mclust_rigor, DISC-DEC-018).
**Governança:** última entrada do ledger no momento desta frente,
DISC-DEC-022. **Data:** 2026-08-22. **Escopo:** pergunta aberta deixada
por `RESULTS_SUMMARY.md`/`DERIVATIONS.md` §6.3 — "não encontramos
mecanismo intrínseco natural" que realize α estritamente entre 1/2 e 1.
Esta pasta (`intermediate_alpha_search/`) contém uma busca dedicada em
duas frentes: literatura (`SEARCH_LOG.md`) e derivação própria (aqui).
Este arquivo é o `FINDINGS.md` pedido pelo mandato da tarefa — nomeado
`MECANISMO_ALPHA_INTERMEDIARIO.md` para descrever seu conteúdo
especificamente (mesmo papel, mesmo conteúdo). Convenção de rótulos
herdada de `DERIVATIONS.md`: DERIVADO / HEURÍSTICO / CONJECTURADO, cada
passo marcado.

## VEREDITO EXECUTIVO

> **Frente literatura: NÃO ENCONTRADO** — nenhum processo nomeado da
> literatura de probabilidade é, por reinterpretação direta, um
> mecanismo M-q com β∈(0,1) (ver `SEARCH_LOG.md`, 15 buscas). O achado
> estrutural da busca (Seção 1 abaixo) é que isso não é coincidência.
>
> **Frente derivação própria: ENCONTRADO** — um mecanismo natural,
> **fora da família M-q estrita** (portanto exatamente a opção (b) do
> mandato desta frente), que realiza **α = 1/(1+β) ∈ (1/2, 1) para
> β∈(0,1)**, com fórmula fechada φ_WEIB(c;β) = ∫₀¹ e^{−c·t^{1+β}} dt,
> DERIVADO por uma identidade algébrica exata (não uma heurística
> ad hoc) e **validado numericamente por dois simuladores próprios e
> independentes** (evento-contínuo: casa com a teoria a <1.6σ em 15/15
> células, 3 valores de β; permutação finito-n: mesmo padrão
> qualitativo com viés finito-n honesto e caracterizado, que
> **encolhe mensuravelmente com n**). O mecanismo: em vez de perturbar
> a REGRA DE DESTINO q(s) (o eixo já esgotado pela frente anterior),
> perturba-se a **TAXA DE EVENTOS** — usando um processo de Poisson
> não-homogêneo com intensidade em forma de Weibull (um objeto padrão
> de teoria de confiabilidade, "risco decrescente"/"mortalidade
> infantil"), mantendo a MESMA regra de destino uniforme de M-U. Um
> corolário notável e verificado numericamente: o mesmo eixo, do lado
> β>1 ("risco crescente"/desgaste), **quebra o piso α≥1/2** que
> `DERIVATIONS.md` §2 prova ser impossível DENTRO da família M-q —
> confirmando que o piso é uma propriedade da taxa constante, não uma
> lei universal para todo mecanismo de redirecionamento pontual.

---

## 1. Frente literatura — o que foi buscado e por que veio vazio (e por quê isso é informativo)

Busca completa em `SEARCH_LOG.md` (15 queries `WebSearch` + 9 `WebFetch`
de verificação, itens 22-23 do log). Classes de processos cobertas,
cada uma um candidato plausível a "expoente de cauda ajustável de forma
contínua": processo de Chinese-Restaurant/Pitman-Yor de dois parâmetros
(crescimento do número de mesas ~ N^d), urnas de Pólya generalizadas com
reforço em lei de potência, processos de Hawkes com kernel em lei de
potência (Omori-Utsu, Ogata 1988 — ETAS), teoria de renovação com cauda
regularmente variável (média infinita), processo de Poisson fracionário
/ subordinador estável inverso (Meerschaert-Straka), processos de
ramificação idade-dependentes com variação regular (teorema de Slack
1968), coalescência-fragmentação com taxas regularmente variáveis,
mapeamentos aleatórios clássicos (ρ/τ de Flajolet-Odlyzko/Pollard-rho),
redes small-world com rewiring em lei de potência, e busca direta por
"redirecionamento parcial de permutação"/"fração cíclica sob
perturbação".

**Nenhum resultado é, por reinterpretação, um mecanismo M-q com
β∈(0,1).** Mas a busca revelou um padrão estrutural consistente, que é
o achado central desta seção:

> **Em TODOS os processos nomeados acima que produzem um expoente de
> cauda ajustável continuamente via um parâmetro de variação regular, a
> variação regular entra em um objeto NÃO-LIMITADO — uma TAXA, uma
> FUNÇÃO GERADORA, ou um KERNEL DE MEMÓRIA — nunca numa PROBABILIDADE
> CONDICIONAL LIMITADA a [0,1] com o perfil exigido por q(s)~a·s^β.**

Concretamente: Pitman-Yor injeta a variação regular no *parâmetro de
desconto* que governa a FUNÇÃO GERADORA da partição; Hawkes/Omori injeta
no *kernel de intensidade* (um objeto ilimitado, taxa de eventos por
tempo); o teorema de Slack (achado mais próximo em espírito — ver
`SEARCH_LOG.md` #12/#13) injeta na *função geradora de probabilidade da
prole*, h(s)=s+(1−s)^{1+α}ℓ(1−s) — de novo uma função geradora, não uma
probabilidade condicional; renovação de cauda pesada e Poisson
fracionário injetam na *distribuição de tempos de espera* (que pode ter
suporte ilimitado). Em nenhum desses objetos há a exigência específica
que q(s) impõe: **ser uma probabilidade (limitada a [0,1]) que se anula
exatamente em s=0 (sem átomo — condição necessária para não colapsar
trivialmente a α=1, DERIVATIONS.md §2) mas cuja razão q(s)/s diverge
quando s→0 (β<1)** — uma forma que nenhum objeto "taxa" ou "função
geradora" natural precisa satisfazer, porque essas vivem naturalmente
num espaço sem teto em 1. Isto não é uma prova de impossibilidade — é
uma explicação precisa, corroborada por 15 buscas independentes em
classes de processos bem separadas, de por que a busca por front (a)
tende a vir vazia: **a parametrização q(s) do M-q é, estruturalmente, o
lugar ERRADO para procurar variação regular natural.** Esta observação
é o que motiva a Seção 2: mover a variação regular para o eixo onde ela
naturalmente vive.

---

## 2. Frente derivação própria — mecanismo M-WEIB(β)

### 2.1 Re-derivação independente da fórmula-mestre (checagem, não nova alegação)

Antes de generalizar, a fórmula-mestre de `DERIVATIONS.md` §1 foi
re-derivada do zero (`verify_algebra.py` parte A), por um argumento
ligeiramente diferente do PGFL original mas equivalente, para poder
generalizá-la com confiança. Considere um evento de reroteamento na
massa s∈[0,t): ele **termina o processo antes da massa t** se, e
somente se, (i) ele mata diretamente (prob. q(s)) OU (ii) ele sobrevive
mas o NOVO arco que cria fecha (por π-closure) antes da massa t (prob.
(1−q(s))·[1 − (1−t)/(1−s)], usando a mesma fórmula de sobrevivência
size-biased do próprio x₀, centrada em s). Chamando essa probabilidade
de `bracket(s,t)`:

**bracket(s,t) = q(s) + (1−q(s))·(t−s)/(1−s) ≡ 1 − (1−q(s))(1−t)/(1−s)**
(identidade algébrica, verificada simbolicamente).

Por independência de Poisson (PGFL, herdado — mesmo passo de
`DERIVATIONS.md`), E[S(t)] = (1−t)·exp(−c·∫₀ᵗ bracket(s,t) ds), e
integrar a identidade acima recupera **exatamente** H_q(t) = t −
(1−t)∫₀ᵗ(1−q(s))/(1−s)ds — confirmando (1.1) de `DERIVATIONS.md` por
uma rota independente. [DERIVADO — mesmo nível de rigor herdado
(PGFL de Poisson no limite contínuo), nada de novo aqui além da
confirmação.]

### 2.2 A identidade-chave: bracket(s,t) = t, exatamente, quando q(s)=s

Substituindo q(s)=s (a regra de destino uniforme de M-U) em bracket:

**bracket(s,t)|_{q=s} = s + (1−s)(t−s)/(1−s) = s + (t−s) = t.**

**Isto é uma identidade exata, independente de s** — verificado
simbolicamente (`verify_algebra.py` parte B). Ou seja: para destinos
uniformes, a probabilidade de que UM evento de reroteamento na massa s
acabe terminando o processo antes da massa t é sempre exatamente t,
não importa QUANDO (s) o evento ocorreu. É uma propriedade de simetria
específica do destino uniforme (que faz M-U ser insensível à ORDEM
temporal dos eventos, não só à sua identidade — reforça, por uma rota
nova, o "lema de intercambiabilidade" já em `DERIVATIONS.md` §3.1, que
tratava intercambiabilidade de DESTINO; aqui é intercambiabilidade de
TEMPO).

### 2.3 A generalização: variar a TAXA em vez de q(s)

A família M-q inteira (`DERIVATIONS.md` §1) fixa a taxa de eventos em
**c constante** e deixa **apenas q(s) variar**. A busca da onda 3 (e a
busca de literatura da Seção 1 acima) tentou encontrar β∈(0,1) DENTRO
desse eixo. **Aqui se propõe o eixo ortogonal: manter q(s)=s (destino
uniforme, o mecanismo mais simples e "menos contrivado" possível — a
MESMA regra de M-U, sem nenhuma curva livre plantada) e deixar a TAXA
de eventos variar no tempo**, λ(s) em vez de c constante, com
Λ(t)=∫₀ᵗλ(s)ds a contagem média acumulada de eventos até a massa t.

Pela identidade da Seção 2.2 (bracket=t, independente de s, válida
para QUALQUER perfil de taxa, homogêneo ou não — verificado
simbolicamente em `verify_algebra.py` parte C):

**c·H(t) := ∫₀ᵗ λ(s)·bracket(s,t) ds = ∫₀ᵗ λ(s)·t ds = t·Λ(t)**

**H(t) = t·Λ(t)/c, exatamente, para q(s)=s e Λ(t) ARBITRÁRIA.**  (2.1)

[DERIVADO, ao mesmo nível de rigor herdado (PGFL de Poisson não-
homogêneo — generalização direta e padrão do PGFL de Poisson homogêneo
já usado na fórmula-mestre; não introduz heurística adicional além da
já herdada "passagem finito-n → contínuo controlada empiricamente".]

Checagem de contorno: Λ(t)=ct (taxa constante) ⟹ H(t)=t·ct/c=t²,
recupera M-U exatamente. ✓ (`verify_algebra.py` parte D, checado
simbolicamente).

### 2.4 M-WEIB(β): perfil de taxa em forma de Weibull

Tome **Λ(t) = c·t^β**, β>0 — a função de contagem média acumulada de um
**processo de Poisson não-homogêneo com intensidade Weibull**
λ(s)=cβs^{β−1}: um objeto padrão de teoria de confiabilidade/análise de
sobrevivência ("curva-banheira"), **verificado por fetch direto**
(`SEARCH_LOG.md` #17): forma de risco DECRESCENTE ("mortalidade
infantil") para β<1, constante (Poisson homogêneo, recupera M-U) para
β=1, CRESCENTE ("desgaste") para β>1. Interpretação natural para o
problema: a propensão a sofrer um evento de reroteamento **diminui**
conforme a exploração de x₀ amadurece (mais massa já foi incorporada à
árvore de exploração ⇒ processo mais "estável", menos sujeito a nova
perturbação) — um perfil qualitativamente análogo ao decaimento de
Omori-Utsu de "atividade pós-choque" (`SEARCH_LOG.md` #4), embora aqui
referenciado à massa TOTAL explorada desde x₀ (não à idade de cada arco
individualmente — ver Seção 4.3 sobre a variante "local" não
perseguida).

Por (2.1): **H_WEIB(t) = t·(c·t^β)/c = t^{1+β}**, logo

**φ_WEIB(c;β) = ∫₀¹ exp(−c·t^{1+β}) dt.**                          (2.2)

Contornos (checados simbolicamente, `verify_algebra.py` parte D):
β→1: H→t², recupera M-U. β→0⁺: Λ(t)→c (constante — um "surto" de
c eventos concentrado em s=0⁺, i.e. um ÁTOMO de massa de evento na
origem), H→t, recupera **exatamente** a forma de M-SELF/M-PREV
((1−e^{−c})/c) — consistente e satisfatório: o mesmo limite α→1 que a
família M-q atinge via átomo de MATAR em q(s) é atingido aqui via átomo
de TAXA em s=0⁺, uma segunda rota independente para o mesmo limite.

### 2.5 Lei do expoente

Watson/Laplace em (2.2) (∫₀¹e^{−ct^γ}dt ~ Γ(1+1/γ)c^{−1/γ}, checado
contra o caso conhecido γ=2 ⟹ Γ(3/2)=√π/2, o coeficiente de M-U ✓):

**φ_WEIB(c;β) ~ Γ(1+α)·c^{−α}, α = 1/(1+β).**                      (2.3)

**A MESMA lei de expoente α=1/(1+β) da família abstrata q~a·s^β**
(`DERIVATIONS.md` §2.2) — mas obtida por um mecanismo estruturalmente
diferente (variar a taxa, não q). Para **β∈(0,1): α∈(1/2,1)** —
exatamente a lacuna buscada. Esta coincidência de lei de expoente entre
os dois eixos (variar q vs. variar a taxa) não é arbitrária: ambas
entram na mesma posição (o termo de ordem t^{1+β} dominando o t²/2 de
crowding) da mesma integral de Laplace — mas SOMENTE o eixo da taxa tem
uma realização "natural" identificada (Seção 2.4); o eixo de q(s)
continua sem uma (Seção 1).

### 2.6 Por que isto está genuinamente FORA de M-q (não uma reparametrização)

A família M-q (`DERIVATIONS.md` §1) fixa "taxa c constante" como parte
da PRÓPRIA DEFINIÇÃO da classe — não é um parâmetro livre dentro dela,
é a estrutura de fundo sobre a qual q(s) varia. M-WEIB(β) modifica
exatamente essa estrutura de fundo (Λ(t)=ct^β em vez de ct), então não
é um caso especial de M-q com algum q̃(s) equivalente — é definido num
eixo ORTOGONAL, exatamente a opção (b) pedida pelo mandato desta
frente ("generalização natural BEYOND the strict M-q family"). Isto
também explica por que **não contradiz** o teorema piso/teto de
`DERIVATIONS.md` §2 (α∈[1/2,1] DENTRO de M-q): esse teorema usa
H_{q≡0} ≤ H_q ≤ H_{q≡1} PARA TAXA CONSTANTE c — a demonstração não se
aplica quando a própria taxa deixa de ser constante. A Seção 2.7 abaixo
confirma isto numericamente: o mesmo eixo, do lado β>1, produz α<1/2,
o que seria impossível dentro de M-q mas é perfeitamente consistente
(e derivado) fora dela.

### 2.7 Corolário: β>1 quebra o piso α≥1/2 (verificado numericamente)

Λ(t)=ct^β com β>1 é IGUALMENTE um perfil de taxa "natural" (Weibull de
risco CRESCENTE — "desgaste", o outro lado padrão da curva-banheira,
`SEARCH_LOG.md` #17), e (2.3) prevê α=1/(1+β)<1/2 para β>1.
**Verificado no simulador contínuo (Seção 3.1):** β=2 dá
α̂=0.3307–0.3352 (alvo 1/3=0.3333); β=3 dá α̂=0.2379–0.2482 (alvo
1/4=0.25) — ambos claramente abaixo de 1/2, em duas execuções
independentes (`continuum_sim.py` inline check e
`supplementary_checks.py` S2, sementes diferentes, resultados
consistentes entre si e com a teoria a <2σ em todas as 4 células). Isto
não estava no escopo original da pergunta (que pede apenas α∈(1/2,1)),
mas é um resultado colateral honesto e relevante: **o piso α≥1/2
"duplamente protegido" de `DERIVATIONS.md` é uma propriedade da
CONSTÂNCIA da taxa, não uma lei universal de todo mecanismo de
redirecionamento pontual de destino único** — a segunda proteção
citada lá ("crowding", termo t²/2 mecanismo-independente) continua
valendo termo-a-termo DENTRO de M-q, mas a comparação entre H_q e H_WEIB
não é uma comparação dentro da mesma classe.

---

## 3. Validação numérica

Dois simuladores próprios, independentes um do outro e da máquina
`ualpha_sim.py` (que não foi importada nem executada — apenas seu
método de detecção de ciclo por elevação-ao-quadrado iterada é
reaproveitado conceitualmente, não seu código). Execução única cada,
sementes pré-fixadas, foreground.

### 3.1 Simulador evento-contínuo (`continuum_sim.py`)

Simula DIRETAMENTE o processo contínuo herdado (`DERIVATIONS.md` §0):
amostragem exata por CDF-inversa da corrida entre (i) fechamento
π-closure em QUALQUER um dos A arcos ativos (sempre terminal — ponto
que corrigiu um bug próprio, ver "Honestidade" abaixo) e (ii) o próximo
evento de reroteamento via Λ^{-1}. **Auto-teste crítico:** em β=1 (que
deve recuperar M-U exatamente), reproduz φ_U(c) — já validado
independentemente pela onda 3 do arquivo — a |z|≤1.04 em 4 valores de c
(0.5, 2, 10, 40), CONFIRMANDO que o simulador está correto antes de
usá-lo para β<1.

**Resultado principal (N=8000/célula, `continuum_sim_results.json`):**

| β | α previsto = 1/(1+β) | α̂ medido (c=10→640) | \|desvio\| em σ | φ_MC vs. φ_teoria (5 células, c∈{2,10,40,160,640}) |
|---|---|---|---|---|
| 0.25 | 0.8000 | 0.7615 ± 0.0349 | 1.1σ | \|z\|≤1.48 em todas |
| 0.50 | 0.6667 | 0.6884 ± 0.0256 | 0.8σ | \|z\|≤1.54 em todas |
| 0.75 | 0.5714 | 0.5770 ± 0.0190 | 0.3σ | \|z\|≤1.60 em todas |

**Todas as 15 células (3β × 5c) dentro de |z|<4** (critério herdado de
`METHODOLOGY_NOTE.md`); os três α̂ caem clara e consistentemente
**dentro de (1/2, 1)**, com a ordenação correta (α̂ decresce com β,
como previsto por 1/(1+β)).

### 3.2 Simulador finito-n em permutação real (`finiten_sim.py`)

Checagem independente e mais forte: construção "preguiçosa"/sob-demanda
sobre uma permutação π REAL de [n] (n=8192), caminhando ponto-a-ponto
com rastreamento genuíno do conjunto visitado (não a abstração de
"corrida" do simulador contínuo). Eventos de reroteamento agendados na
massa via a mesma lei Λ(t)=ct^β (CDF-inversa), mas a decisão de
matar/sobreviver e a detecção de fechamento usam **destinos reais
sorteados em [n]** e **checagem real de pertencimento ao conjunto
visitado**.

**Auto-teste crítico (β=1=M-U, n=8192):** |z|≤2.54 contra a fórmula
φ_U(c) já validada (n=32768 no arquivo original) — viés finito-n
pequeno e esperado (n aqui é 4× menor que o padrão do arquivo).

**Resultado principal (N=5000/célula, `finiten_sim_results.json`):**

| β | α previsto | α̂ medido (n=8192, c=10→640) | \|desvio\| em σ | φ_MC vs. teoria contínua |
|---|---|---|---|---|
| 0.25 | 0.8000 | 0.6588 ± 0.0328 | 4.3σ | z até +4.82 (viés sistemático) |
| 0.50 | 0.6667 | 0.5914 ± 0.0264 | 2.8σ | z até +2.84 |
| 0.75 | 0.5714 | 0.5372 ± 0.0222 | 1.5σ | z até +1.23 |

**Leitura honesta:** há um viés finito-n real e sistemático (φ_MC
sistematicamente ACIMA da previsão contínua), crescente conforme β→0
(onde a taxa Weibull diverge mais fortemente em s→0⁺, exigindo mais
resolução de massa que n=8192 comporta confortavelmente) — o mesmo
padrão qualitativo que `mclust_rigor/` encontrou para M-CLUST(b) em b
grande. **Mas mesmo com esse viés, α̂ nunca se aproxima de 1/2 nem de
1 em nenhuma das 3 células — permanece robustamente intermediário.**

**Verificação de que é um efeito de tamanho finito genuíno, não um bug
ou uma falha estrutural** (`supplementary_checks.py`, S1): repetindo
β=0.25 em n=32768 (a resolução padrão do arquivo, 4× maior),
N=3000/célula: **α̂ = 0.7054 ± 0.0490, desvio cai de 4.3σ (n=8192) para
1.9σ (n=32768)** — o viés ENCOLHE mensuravelmente com n, na direção
certa, consistente com um efeito de tamanho finito genuíno que se
resolve no limite n→∞ (mesma leitura qualitativa que
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` já documentou para M-CLUST(b)
grande — "resíduo sistemático, mesmo sentido, encolhendo", não
promovido a "fechado" por honestidade, mas também não uma refutação).

### 3.3 Honestidade sobre o processo de validação: um bug próprio, encontrado e corrigido

A primeira versão de `continuum_sim.py` continha um erro conceitual: ao
implementar a "corrida" entre A arcos ativos, tratava o fechamento de
um arco QUE NÃO É x₀ como um evento que apenas remove aquele arco e
continua a exploração — em vez de TERMINAL para toda a corrida (a
formulação exata em `DERIVATIONS.md` §0 diz "x₀ é cíclico sse o
**primeiro evento terminal** é π-closure em x₀ mesmo", implicando que
QUALQUER fechamento, não só o de x₀, encerra a corrida). Este bug foi
detectado exatamente pelo auto-teste descrito acima: em β=1, a
primeira versão dava φ_MC sistematicamente muito ACIMA de φ_U(c)
conhecido (z de +33 a +50). Corrigido (fechamento de QUALQUER arco é
terminal), o auto-teste passou a |z|≤1.04, e a execução única declarada
(Seção 3.1) foi feita DEPOIS da correção — o código final em
`continuum_sim.py` já reflete apenas a versão corrigida. Reportado por
disciplina de honestidade do laboratório — o mesmo padrão de "achar,
corrigir, declarar" já praticado em `mclust_rigor/`.

---

## 4. Direções exploradas e descartadas (near-misses, com a obstrução precisa)

Por honestidade e para poupar trabalho futuro, os seguintes caminhos
foram considerados e **especificamente descartados**, com o motivo
técnico exato:

### 4.1 M-CLUST(b) com b/n → ρ fixo (n→∞): NÃO produz expoente intermediário

Ideia natural: já que M-CLUST(b) (`DERIVATIONS.md` §3.5,
`mclust_rigor/`) usa blocos de tamanho b ao longo de π, e mostra
correções finito-n que crescem com bc/n, por que não deixar b crescer
COM n (b=λn, razão fixa) para ver se emerge um novo expoente no limite
duplo? **Resposta, verificada simbolicamente** (`verify_algebra.py`
parte E): usando a fórmula de campo médio já derivada em
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` (§4, q_CLUST(s)=s/(1−ρ),
ρ=1−(1−c/n)^b → ρ constante quando b/n→λ fixo), a expansão em série de
Taylor de H_NEW(t) em t=0 dá coeficiente de t¹ = 0 e coeficiente de
**t² = (2−ρ)/(2(1−ρ))** (=1 em ρ=0, recuperando M-U exatamente) — a
ordem t³ é não-nula mas SUBLIDER. **O termo dominante continua
EXATAMENTE quadrático (β=1) para todo ρ∈(0,1) fixo — o eixo b/n→λ
apenas RE-ESCALA o coeficiente de U_{1/2}, não produz um expoente
novo.** Descartado como fonte de α intermediário; documentado aqui
para não ser refeito.

### 4.2 Taxa dependente de um ranking AUXILIAR independente de π: "lavado" pela troca

Tentativa: marcar pontos com probabilidade dependente de sua posição
numa ordem ω INDEPENDENTE de π (em vez de depender da massa s
literalmente caminhada), esperando obter um perfil de taxa não-trivial
"visto pelo caminhante" sem precisar de bookkeeping sequencial.
**Obstrução identificada (argumento, não simulado — o mesmo princípio
de "lema de intercambiabilidade" de `DERIVATIONS.md` §3.1, generalizado
de destino para TEMPO de evento):** como ω⊥π, a sequência de postos-ω
encontrados AO LONGO do caminho π é, em lei, uma amostragem
essencialmente não-correlacionada com a posição no caminho — qualquer
estrutura de variação em ω é "lavada" pela independência, e o processo
visto pelo caminhante colapsa de volta a uma taxa efetivamente
CONSTANTE (a média de λ sobre ω), recuperando M-U com c'=Λ(1). Esta é a
razão técnica precisa pela qual M-WEIB(β) (Seção 2) teve que ancorar a
taxa na MASSA REALMENTE CAMINHADA s (path-dependente), não numa
estrutura auxiliar independente — e é o mesmo motivo, por analogia, que
um processo de renovação de cauda pesada definido numa coordenada
independente de π (a primeira ideia considerada antes de M-WEIB, nunca
implementada por este argumento) teria falhado do mesmo jeito.

### 4.3 Variante "local" (idade-do-arco) tipo Hawkes: não derivada, deixada em aberto

Uma generalização natural de M-WEIB(β), mais próxima ainda da analogia
Omori-Utsu/Hawkes (`SEARCH_LOG.md` #4): em vez de a intensidade
decrescer com a MASSA TOTAL explorada desde x₀ (M-WEIB, "global"), cada
ARCO individual (incluindo os criados por reroteamentos sobreviventes)
teria seu PRÓPRIO relógio Weibull local, reiniciado na própria idade do
arco. A identidade bracket(s,t)=t (Seção 2.2) ainda vale por evento
(não depende de COMO a taxa é estruturada), mas calcular Λ(t) exigiria
somar as contribuições de TODOS os arcos vivos, nascidos em tempos
aleatórios recursivamente gerados pelo próprio processo — uma
autoconsistência tipo processo de cluster de Poisson/Hawkes que não foi
resolvida em forma fechada dentro do orçamento desta frente. **Deixado
honestamente em aberto**, sem alegação de resultado, como candidato
"ainda mais natural" para trabalho futuro (é estruturalmente mais
próximo do Hawkes/ETAS real do que M-WEIB, que usa um relógio global
único).

---

## 5. Limitações e honestidade final

- **Rigor herdado, não elevado:** a derivação de (2.1)–(2.3) usa
  EXATAMENTE o mesmo nível de rigor que a fórmula-mestre original de
  `DERIVATIONS.md` (PGFL de Poisson, agora não-homogêneo, no limite
  contínuo) — não introduz uma heurística nova além da já herdada
  ressalva "passagem finito-n→contínuo controlada empiricamente, não
  formalizada" (`DERIVATIONS.md` item 1 de loose ends, também citada em
  `mclust_rigor/`).
- **Viés finito-n não fechado por esta frente:** o simulador finito-n
  (Seção 3.2) mostra um viés real, sistemático, que ENCOLHE
  mensuravelmente com n (4.3σ→1.9σ ao quadruplicar n em β=0.25) mas não
  foi levado a n→∞ nem corrigido analiticamente (o mesmo padrão de
  honestidade que `mclust_rigor/DERIVATION_MCLUST_FIXED.md` já registrou
  para M-CLUST — "melhoria consistente, não fechamento completo, dentro
  do orçamento desta frente"). A CONCLUSÃO QUALITATIVA (α
  robustamente intermediário, nunca colapsando a 1/2 ou 1) não depende
  desse fechamento — é visível mesmo no pior caso testado.
- **"Natural" é uma alegação qualitativa, não uma prova de
  unicidade:** M-WEIB(β) é natural no sentido específico enunciado no
  mandato desta frente — não requer plantar uma curva q(s) livre
  arbitrária; reaproveita a MESMA regra de destino de M-U; usa um
  perfil de taxa (Weibull não-homogêneo) que é um objeto padrão,
  nomeado e verificado por fetch (`SEARCH_LOG.md` #17), com
  interpretação física direta (maturação/estabilização da exploração,
  ou por analogia a decaimento pós-choque tipo Omori). Isso não é uma
  alegação de que seja o ÚNICO mecanismo natural possível, nem de
  novidade fora deste arquivo (mandato herdado da frente A,
  DISC-DEC-015 — nenhuma alegação de prioridade é feita aqui).
- **Frente (a) da literatura permanece, estritamente, um "não
  encontrado"**, não um "provado impossível" — 15 buscas cobrindo as
  classes mais plausíveis vieram vazias, com uma explicação estrutural
  precisa (Seção 1) de POR QUE tendem a vir vazias, mas isso não é uma
  demonstração de que NENHUM processo nomeado da literatura, em nenhum
  canto não buscado, poderia ser reinterpretado como um M-q com
  β∈(0,1).

## Arquivos (todos em `intermediate_alpha_search/`)

- `SEARCH_LOG.md` — 15 queries de busca + 9 verificações de fetch,
  todas registradas com resultado (achado ou vazio).
- `MECANISMO_ALPHA_INTERMEDIARIO.md` — este arquivo (papel de
  `FINDINGS.md` pedido pelo mandato: veredito de literatura +
  derivação própria).
- `verify_algebra.py` / `verify_algebra.log` — checagens simbólicas
  (sympy) das identidades algébricas da Seção 2 e do near-miss da
  Seção 4.1. Execução única.
- `continuum_sim.py` / `continuum_sim.log` / `continuum_sim_results.json`
  — simulador evento-contínuo de M-WEIB(β) (Seção 3.1), incluindo o
  auto-teste β=1 contra φ_U(c) conhecido. Execução única (pós-correção
  do bug da Seção 3.3).
- `finiten_sim.py` / `finiten_sim.log` / `finiten_sim_results.json` —
  simulador finito-n em permutação real (Seção 3.2). Execução única.
- `supplementary_checks.py` / `supplementary_checks.log` /
  `supplementary_checks_results.json` — tendência de viés finito-n
  (n=8192→32768, Seção 3.2) e corolário β>1 (Seção 2.7). Execução
  única.

---

## [Correção pós-adversarial, 2026-08-22]

A verificação adversarial obrigatória (`adversarial/ADVERSARIAL_VERDICT.md`,
implementação e derivação independentes, feitas antes de ler este arquivo)
**confirma toda a matemática substantiva** — a identidade `bracket(s,t)=t`
(Seção 2.2), a fórmula fechada `φ_WEIB(c;β)=∫₀¹e^{-c·t^{1+β}}dt` (Seção
2.4-2.5), a lei do expoente `α=1/(1+β)`, e a validação numérica (dois
simuladores próprios adicionais, seeds independentes, todos os pontos
testados dentro de |z|<3, incluindo um valor de β nunca testado aqui) —
**mas REFUTA o enquadramento da Seção 2.6** ("genuinamente fora de M-q")
para exatamente a região que importava, `β∈(0,1)`.

**O achado adversarial:** resolvendo a fórmula-mestre de `DERIVATIONS.md`
§1 para o `q(t)` que reproduziria `H(t)=t^{1+β}`, obtém-se uma forma
fechada explícita

> `q(t) = [(1+β)·t^β − β·t^{1+β} − t] / (1−t)`

verificada numericamente como permanecendo em `[0,1]` para TODO `β∈(0,1)`
testado (incluindo `β=0,99`) — ou seja, **`M-WEIB(β<1)` não está fora da
família M-q: é um membro dela**, com este `q(t)` como sua realização
explícita. Para `β>1` (ex. `β=2`, `q_min=-0,125`), `q(t)` sai de `[0,1]`
— nenhum candidato válido existe — confirmando que **só o lado `β>1` sai
genuinamente de M-q**, o que valida por completo o corolário da Seção
2.7 (quebra do piso `α≥1/2`) exatamente como reportado.

**Isto não enfraquece a resposta à pergunta original — na verdade a
torna mais forte e mais simples.** A pergunta era "existe um mecanismo
natural com `α∈(1/2,1)`?", e a resposta permanece **SIM**, agora
respondida inteiramente DENTRO do arcabouço M-q já classificado e
verificado por `DERIVATIONS.md`: o perfil `q(t)` acima é o membro da
família que faltava (Seção 1 da busca de literatura já explicava,
corretamente, por que ele nunca teria sido adivinhado por tentativa
direta em `q(s)~a·s^β` — o achado de M-WEIB foi o caminho indireto certo
para encontrá-lo, mesmo que a interpretação "taxa variável, fora de M-q"
para `β<1` estivesse equivocada). A identidade `H(t)=t·Λ(t)/c` (2.1)
continua um resultado real e correto — de fato mais geral do que
alegado, válida para qualquer perfil `Λ` determinístico, não só Weibull
(achado extra da verificação adversarial) — só a alegação de novidade
estrutural ("eixo ortogonal a M-q") não se sustenta para `β<1`.

**Veredito final, corrigido:** mecanismo com `α∈(1/2,1)` — ENCONTRADO e
CONFIRMADO, como um membro explícito e antes-desconhecido da família
M-q. Mecanismo com `α<1/2` (quebra do piso) — ENCONTRADO e CONFIRMADO,
genuinamente fora de M-q (β>1). Ver `adversarial/ADVERSARIAL_VERDICT.md`
para a verificação completa.
