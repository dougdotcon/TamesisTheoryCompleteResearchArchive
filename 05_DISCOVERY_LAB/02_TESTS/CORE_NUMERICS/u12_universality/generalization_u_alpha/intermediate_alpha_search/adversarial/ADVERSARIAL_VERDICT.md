# Veredito adversarial — mecanismo M-WEIB(β), `intermediate_alpha_search`

**Frente atacada:** `MECANISMO_ALPHA_INTERMEDIARIO.md` (onda 5,
DISC-DEC-022). **Disciplina cumprida:** re-derivação e simuladores
próprios feitos ANTES de ler a derivação/código do alvo — ver
`ADVERSARIAL_NOTE.md` para o plano, as sementes e os critérios de
veredito registrados previamente. Todos os números abaixo vêm dos
scripts nesta pasta, com logs e JSONs salvos.

## Resumo executivo

**A alegação matemática central sobrevive integralmente ao ataque: a
identidade, a forma fechada e o expoente da cauda estão CONFIRMADOS por
re-derivação independente e por dois simuladores próprios (contínuo e
finito-n), com dois bugs encontrados e corrigidos — em código MEU, não
deles, documentados abaixo por transparência.** O único ponto onde a
verificação diverge do relatório do front é a alegação de novidade
"genuinamente fora de M-q": ela é **CONFIRMADA para β>1** mas
**tecnicamente REFUTADA para β∈(0,1)** — o regime que é o achado
principal da frente — no seguinte sentido preciso: encontrei uma função
`q(t)` válida (0≤q≤1 em todo o domínio) tal que o mecanismo M-q(q(t)),
com TAXA CONSTANTE `c`, reproduz `φ_WEIB(c;β)` EXATAMENTE, para todo
`c`, com erro de ordem `1e-15` numa rota de verificação independente.
Isso não invalida a matemática da frente (a forma fechada e o expoente
estão corretos), mas enfraquece a alegação de que o OBSERVÁVEL φ(c) seja
"novo" — ele já era alcançável dentro da família M-q classificada, só
não tinha sido encontrado por lá. Ver §(c) para o porquê isso não é uma
contradição do teorema piso/teto, e por que β>1 é estruturalmente
diferente.

## (a) Identidade algébrica H(t) = t·Λ(t)/c

**CONFIRMADA**, por duas rotas independentes:

**Rota 1 — re-derivação à mão (`ADVERSARIAL_NOTE.md`, antes de rodar
qualquer código).** Generalizei a prova do Teorema 1 de `THEOREM.md`
§3 (Definição 3), trocando o processo de Poisson homogêneo de taxa `c`
por um processo de Poisson não-homogêneo de intensidade determinística
`λ(s)` qualquer, mantendo a regra de destino de M-U (`q(s)=s`). Os
Passos 1–3 do Teorema 1 não usam a taxa do processo em nenhum ponto
(são puramente sobre ordem de eventos e a propriedade de restrição de
processos de Poisson, válida para intensidade não-constante). O Passo 4
— o cálculo nuclear `P(sucesso em s) = (1-s)·(1-t)/(1-s) = 1-t` — é um
cálculo sobre UMA marca isolada condicionada à posição `s`; a taxa do
processo simplesmente não aparece nele. Logo **a identidade "bracket
independente de s" é mais geral do que o relatório do alvo sugere: ela
vale para QUALQUER perfil de taxa `Λ`, não é uma peculiaridade do
perfil Weibull** — é uma propriedade de qualquer perturbação pura-da-
-taxa sob a regra M-U. Isso dá, pelo teorema de marcação/afinamento de
Poisson (válido para processos não-homogêneos), `H(t)=t·Λ(t)/c`
exatamente, com `Λ(t)=c·t^β` reduzindo a `H(t)=t^{1+β}`.

**Rota 2 — Monte Carlo cirúrgico, `identity_check.py` (semente
20260823, 300 000 réplicas/célula).** Testei `P(zero marcas falhas em
[0,t)) = e^{-t·Λ(t)}` diretamente — sem passar pela integral em `t` —
numa grade `t∈{0.1,0.3,0.5,0.7,0.9}` × `β∈{0.25,0.5,0.75}` ×
`c∈{1,4,16}` (45 células). Resultado: **44/45 células dentro de 3σ
binomial (97.8%)**, sem viés sistemático de sinal (z's espalhados entre
-3.17 e +2.63; a única célula fora de 3σ é consistente com o ~12% de
chance esperada de pelo menos uma excursão de 3σ em 45 testes
independentes). Ver `identity_check_results.json`.

**Veredito: CONFIRMADA.** Não encontrei nenhum termo descartado
incorretamente nem nenhum `(s,t)` onde a identidade falhe.

## (b) Forma fechada φ_WEIB(c;β) e expoente α=1/(1+β)

**CONFIRMADA**, por três rotas independentes:

**Rota 1 — cauda por Laplace/Watson (à mão).** Substituição
`u=c^{1/(1+β)}t` em `∫₀¹e^{-ct^{1+β}}dt` dá
`c^{-1/(1+β)}∫₀^{c^{1/(1+β)}}e^{-u^{1+β}}du → c^{-1/(1+β)}Γ(1+1/(1+β))`
quando `c→∞` (cauda do integrando decai exponencialmente além de
`u~O(1)`). **α=1/(1+β) confirmado analiticamente**, coeficiente
`Γ(1+1/(1+β))` (checagem: β=1 dá `Γ(3/2)=√π/2`, o valor exato de M-U).

**Rota 2 — Simulador A, evento-contínuo próprio (`sim_continuum.py`,
semente 20260822, 300 000 réplicas/célula, grade `β∈{0.25,0.5,0.75,
0.9}` × `c∈{0.5,1,2,4,8,16,32,64}`, 32 células — 0.9 é o valor extra
fora da grade deles, pedido pelo mandato). Construção própria: amostra
`K~Poisson(c)` marcas com posições `Beta(β,1)` (densidade da lei
condicional de um processo Weibull-NHPP, verificada por CDF), Θ~Unif(0,1)
(kill), `T=S+(1-S)(1-e^{-E})` (relógio de fechamento), laço de
"corrida de arc-heads" implementado do zero seguindo a Definição 3 de
`THEOREM.md`. **Todas as 32 células dentro de ~2.6σ, sem viés
sistemático de sinal** (ver `sim_continuum_results.json`,
`sim_continuum.log`). **α̂ ajustado por regressão log-log (metade
superior da grade de c, `tail_fit.py`) bate com 1/(1+β) a menos de
0.005 em TODOS os 4 valores de β**:

| β | α̂ (MC próprio) | α teórico 1/(1+β) | diferença |
|---|---|---|---|
| 0.25 | 0.7951 | 0.8000 | -0.0049 |
| 0.50 | 0.6692 | 0.6667 | +0.0026 |
| 0.75 | 0.5701 | 0.5714 | -0.0013 |
| 0.90 (extra) | 0.5228 | 0.5263 | -0.0035 |

**Rota 3 — Simulador B, finito-n próprio (`sim_finiten.py`, ver §(d)).**

**Nota de transparência (bug próprio nº1):** a primeira versão de
`sim_continuum.py` tinha um bug de lógica — marcava `is_cyclic=True`
sempre que nenhum "kill" ocorria, sem checar SE o vencedor final da
corrida de arc-heads era de fato o arc-head 0 (x₀). Isso produzia
`phi_hat` sistematicamente MAIOR que a teoria por >100σ em TODAS as 32
células (log preservado nos comentários do código-fonte). Corrigido
rastreando explicitamente quem detém o mínimo corrente antes de
declarar ciclicidade; após a correção, bate com a quadratura numérica
em todas as células. Documentado para mostrar que a disciplina
"reproduzir do zero, sem ver o código deles" tem um custo real (bugs
próprios) que teve de ser resolvido por triangulação (comparação com
`identity_check.py`, já validado), e não que a teoria estava errada.

**Veredito: CONFIRMADA**, tanto a forma fechada quanto o expoente.

## (c) A alegação "genuinamente fora de M-q"

**REFUTADA (como alegação de novidade) para β∈(0,1); CONFIRMADA
para β>1.** Este é o achado adversarial mais substantivo desta
verificação — exatamente o tipo de sutileza que o mandato pediu para
caçar.

**Setup.** A fórmula-mestre de M-q (`H_q(t)=t-(1-t)∫₀ᵗ(1-q(s))/(1-s)ds`)
é LINEAR (logo invertível) em `q`. Resolvi à mão, ANTES de rodar
qualquer script (`ADVERSARIAL_NOTE.md`), qual `q(t)` reproduziria
`H_q(t)=t^{1+β}` exatamente:

```
q(t) = [(1+β)·t^β - β·t^{1+β} - t] / (1-t)
```

Checagens de limite feitas à mão: β=1 ⇒ q(t)=t (M-U exato ✓); β=0 ⇒
q≡1 (bate com o caso extremo `q≡1 ⇒ H=t` de `DERIVATIONS.md` §1 ✓).

**`mq_equivalence.py` (determinístico, sem Monte Carlo) testou duas
coisas:**

1. **Plugar `q(t)` de volta na integral ORIGINAL de M-q** (não no atalho
   `t^{1+β}`) via quadratura numérica independente — bate com
   `t^{1+β}` em TODOS os pontos testados (β∈{0.25,0.5,0.75}, t∈
   {0.1,...,0.99}) com erro de `1e-15` a `1e-17` (arredondamento de
   máquina puro — ver `mq_equivalence_results.json`).
2. **Varrer `q(t)` em `t∈(0,1)` para β<1 e β>1:**

| β | q_min | q_max | válido em [0,1]? |
|---|---|---|---|
| 0.25 | +0.0395 | 1.0000 | **sim** |
| 0.50 | +0.0015 | 1.0000 | **sim** |
| 0.75 | +0.00005 | 1.0000 | **sim** |
| 0.99 | +0.0000013 | 1.0000 | **sim** |
| 1.00 | ≈0 (arred.) | 1.0000 | **sim** (= M-U) |
| 1.10 | **-0.000021** | 1.0000 | **não** |
| 2.00 | **-0.1250** | 1.0000 | **não** |
| 3.00 | **-0.3796** | 1.0000 | **não** |

**Interpretação.** Para **todo β∈(0,1) testado** (exatamente o regime
`α∈(1/2,1)` que é o achado central da frente), `q(t)` permanece uma
probabilidade válida em TODO o domínio — ou seja, **M-WEIB(β<1) é
reproduzido, φ(c) para todo c simultaneamente, por um mecanismo M-q
legítimo** (taxa constante `c`, probabilidade de kill `q(t)` dada
acima). O MECANISMO microscópico é de fato diferente (perturbar a taxa
vs. perturbar `q`), mas o OBSERVÁVEL — a própria quantidade que a
árvore inteira usa para classificar mecanismos — não é novo: já estava
dentro do alcance de M-q, só não tinha sido exibido. A frase "fora da
família M-q estrita" no VEREDITO EXECUTIVO do alvo é tecnicamente
verdadeira apenas no sentido "não satisfaz a definição microscópica
literal de M-q" — mas o enquadramento como achado que ocupa "a opção
(b) do mandato" (um mecanismo GENUINAMENTE novo) fica mais fraco do que
apresentado: `DERIVATIONS.md` §6 item 3 já sabia, por análise
assintótica de `q(s)~a·s^β` perto de `s=0`, que expoentes intermediários
eram alcançáveis EM PRINCÍPIO dentro de M-q — meu `q(t)` é exatamente
essa família estendida a uma forma fechada exata em todo o domínio
(pequeno-t: `q(t)~(1+β)t^β`, i.e. "a"=1+β na notação deles; plugando
`a=1+β` na fórmula assintótica geral deles, `φ~Γ(1+1/(β+1))[(β+1)/
(ac)]^{1/(β+1)}`, dá exatamente `Γ(1+1/(1+β))c^{-1/(1+β)}` — bate com a
cauda de M-WEIB, uma checagem de consistência adicional e não-trivial).

**Por que β>1 É genuinamente diferente (e por que isso não contradiz o
teorema piso/teto).** Como `H_q↦q` é injetora (a diferença
`H_q(t)-H_{q'}(t)` é identicamente nula em `t` só se `q≡q'` q.t.p.), o
`q(t)` acima é o ÚNICO candidato. Para β>1 ele sai de `[0,1]`
(negativo perto de `t` pequeno) — **não existe NENHUM `q(t)`∈[0,1]**
que reproduza `H(t)=t^{1+β}` para β>1. Isso significa que M-WEIB(β>1)
está genuína e demonstravelmente FORA do alcance de M-q — exatamente o
regime em que o relatório do alvo alega "quebrar o piso α≥1/2", e essa
alegação é CONSISTENTE (não contraditória) com o teorema piso/teto de
`DERIVATIONS.md` §2, porque esse teorema é uma afirmação SOBRE a classe
M-q inteira (0≤q≤1 ⇒ α∈[1/2,1]) — e M-WEIB(β>1) simplesmente não é um
membro dessa classe. A fronteira exata onde `q(t)` deixa de ser válido
é `β=1`, exatamente onde M-U mora — uma coincidência estrutural elegante
que aumenta minha confiança de que ambas as contas (a minha e a deles)
estão corretas.

**Veredito:** (c1) forma fechada/expoente: correta (já coberto em (b)).
(c2) alegação de novidade "fora de M-q": **REFUTADA para β∈(0,1)** no
sentido preciso acima (observável replicável dentro de M-q por um `q(t)`
explícito e válido) — **recomendo que o relatório do alvo seja
corrigido/qualificado neste ponto** — mas **CONFIRMADA para β>1**, onde
o mecanismo é de fato inacessível a M-q e a quebra do piso é genuína e
não-contraditória.

## (d) Reprodução numérica

**CONFIRMADA**, com uma ressalva honesta de poder estatístico no
componente finito-n.

**Simulador A (contínuo):** ver §(b), Rota 2 — 32/32 células dentro de
~2.6σ, α̂ bate com 1/(1+β) a <0.005 em 4 valores de β incluindo um fora
da grade deles.

**Simulador B (finito-n, `sim_finiten.py`, semente 20260824).**
Construção própria: revelação preguiçosa da órbita de x₀ passo a passo
(não construção global de π), decisão de reroteamento no passo `k`
com probabilidade `1-exp(-(Λ((k+1)/n)-Λ(k/n)))` (correção de casa
decimal necessária e documentada: a probabilidade linear ingênua
`Λ((k+1)/n)-Λ(k/n)` pode exceder 1 perto de `t=0` para β<1 e `c`
grande, já que a intensidade instantânea diverge em `t=0`; a forma
`1-e^{-Δ}` é a construção padrão NHPP→discreto e permanece em [0,1]
sempre), destino de reroteamento uniforme irrestrito em `[n]`,
destino de "seguir π" uniforme entre os alvos ainda não usados como
imagem de π (com x₀ sempre elegível, permitindo o fechamento natural
do ciclo).

**Nota de transparência (bug próprio nº2):** a primeira versão excluía
TODOS os pontos já visitados (inclusive os alcançados por
reroteamento) do pool de "seguir π", em vez de excluir apenas os que
já foram revelados como IMAGEM de π. Isso protegia artificialmente
toda trajetória de colidir com seus próprios pontos visitados por
reroteamento via o canal de π, inflando `φ_hat` em +0.10 a +0.44 —
**um viés que, de forma reveladora, NÃO encolhia com n** (a pista de
que era um bug de construção, não um efeito genuíno de tamanho finito:
um viés O(1/n) real deveria encolher com n crescente, e este não
encolhia). Corrigido separando o pool de exclusão (`pi_used_targets`,
só imagens de π já reveladas) da checagem de parada (`target in
path_set`, que continua usando TODO o caminho, como deve ser).

**Resultado pós-correção** (grade `n∈{2000,8000,32768}` ×
`β∈{0.25,0.5,0.75}` × `c∈{1,4,16}`, 27 células; réplicas reduzidas de
20000/20000/4000 pré-registradas para 4000/1500/400 por razão de
orçamento de tempo — o comprimento médio do passeio acabou sendo
O(n) (ordem do tamanho de ciclo de uma permutação, não O(√n) como eu
tinha estimado ao registrar o plano — corrigido honestamente aqui):

| n | diff médio (φ̂-φ_contínuo) | RMS(diff) | erro-padrão MC típico |
|---|---|---|---|
| 2000 | +0.00555 | 0.01080 | ~0.007 |
| 8000 | +0.00416 | 0.01495 | ~0.012 |
| 32768 | -0.01089 | 0.02380 | ~0.024 |

Todas as 27 diferenças são pequenas (a maior é -0.055, em ~1.9σ) e
consistentes com ruído Monte Carlo — **nenhum viés sistemático grande
sobrevive à correção do bug**. **Ressalva honesta:** como reduzi as
réplicas para caber no orçamento de tempo, o erro-padrão cresce com
`n` na mesma proporção que a redução de réplicas, então **meus dados
não têm poder estatístico suficiente para confirmar OU refutar,
independentemente, a sub-alegação específica "o viés encolhe
mensuravelmente com n"** relatada pelo alvo — o RMS(diff) observado é
consistente com ruído em cada nível de n, não com uma tendência limpa.
O que posso confirmar com confiança é o resultado mais fraco, mas
ainda substantivo: **não há evidência de viés grande ou sistemático em
nenhuma escala de n testada**, qualitativamente reproduzindo o padrão
"finito-n aproxima o contínuo" alegado.

**Veredito: CONFIRMADA** (forma fechada + expoente, alta confiança;
padrão qualitativo finito-n, confiança moderada — poder estatístico
insuficiente para a sub-alegação fina sobre a taxa de encolhimento do
viés).

## Itens de prioridade menor (mandato item 6, verificação leve)

Não teve tempo/orçamento para simuladores dedicados; reportado por
honestidade, com confiança mais baixa que (a)-(d).

**"Taxa dependente de ranking auxiliar independente de π é lavada pela
troca":** **CONFIRMADO por raciocínio independente**, cheguei à MESMA
conclusão sozinho, antes de ler a seção 4.2 do alvo, ao desenhar o
Simulador B: marcar por RÓTULO FIXO (ou qualquer ranking auxiliar
independente de π) não pode produzir uma taxa efetivamente não-
-constante ao longo da massa explorada, porque π é uniforme e a ordem
de visitação é "cega" aos rótulos — qualquer dependência do rótulo se
mistura (average out) para uma taxa efetivamente constante no limite
contínuo, exatamente a razão pela qual o Simulador B teve de amarrar o
reroteamento ao RANK DE VISITAÇÃO (dinâmico), não ao rótulo. Mesma
lógica estrutural do Lema de Exchangeability de `DERIVATIONS.md` §3.1
(para destinos) aplicada ao eixo da taxa.

**"M-CLUST(b) com b/n→λ fixo não produz expoente intermediário":**
**INCONCLUSIVO** por parte desta verificação — não construí um
simulador dedicado nem uma re-derivação completa dentro do orçamento.
Raciocínio parcial (não verificado numericamente): a derivação de
`DERIVATIONS.md` §3.5 para b FIXO depende de "cadeias de sombreamento
têm comprimento 1 q.c." porque `P(cair em R)=bc/n→0`; para `b=λn`
macroscópico, `bc/n→λc`, uma constante POSITIVA — a hipótese central
da derivação de b fixo colapsa, então a conclusão `φ_CLUST=φ_U`
(independente de b) simplesmente não se estende por esse argumento a
b macroscópico; não vi razão para achar que o resultado é INCORRETO,
mas também não posso confirmá-lo com o rigor usado em (a)-(d). Deixado
honestamente em aberto.

## Veredito geral

**CONFIRMADO, com uma correção de enquadramento.** A identidade
`H(t)=t·Λ(t)/c`, a forma fechada `φ_WEIB(c;β)=∫₀¹e^{-ct^{1+β}}dt` e o
expoente `α=1/(1+β)∈(1/2,1)` para `β∈(0,1)` sobrevivem integralmente a
uma re-derivação independente E a dois simuladores próprios (com dois
bugs — ambos MEUS, ambos documentados, ambos corrigidos e verificados
por triangulação antes de aceitar qualquer resultado). Isso NÃO é um
mecanismo numericamente frágil nem um artefato de precisão — é uma
identidade algébrica robusta, generalizável (vale para QUALQUER perfil
de taxa `Λ(t)`, não só Weibull) e numericamente reproduzida com
sementes e algoritmos totalmente independentes dos usados pelo alvo.

A única correção substantiva que este veredito traz é sobre a moldura
("framing") da alegação de novidade: **para β∈(0,1) — o regime que dá
título ao arquivo do alvo — o observável φ(c) já era alcançável dentro
de M-q por um `q(t)` explícito, válido e verificado até erro de máquina;
"fora de M-q" só é estritamente verdadeiro no nível da CONSTRUÇÃO
microscópica, não no nível do observável classificado pela árvore
inteira.** Para β>1, em contraste, a alegação de novidade E a quebra do
piso α≥1/2 são ambas genuínas e não-contraditórias com o teorema
piso/teto, por uma razão estrutural limpa (o mesmo `q(t)` sai de [0,1]
exatamente em β=1). Recomendo que `MECANISMO_ALPHA_INTERMEDIARIO.md`
seja atualizado para refletir essa distinção antes de qualquer entrada
no ledger de governança que dependa da alegação "genuinamente fora de
M-q" no regime β∈(0,1).

## Arquivos desta verificação

- `ADVERSARIAL_NOTE.md` — plano, sementes e critérios pré-registrados
  (gravado antes de qualquer execução).
- `mq_equivalence.py` / `.log` / `_results.json` — checagem determinística
  da equivalência com M-q (item c).
- `identity_check.py` / `.log` / `_results.json` — Monte Carlo cirúrgico
  da identidade H(t)=t·Λ(t)/c (item a).
- `sim_continuum.py` / `.log` / `_results.json` — Simulador A, evento-
  contínuo próprio, phi(c;β) completo (item b/d).
- `tail_fit.py` / `.log` / `_results.json` — ajuste do expoente da cauda
  a partir do Simulador A.
- `sim_finiten.py` / `.log` / `_results.json` — Simulador B, finito-n
  próprio (item d).
- `ADVERSARIAL_VERDICT.md` — este arquivo.

Nenhum resultado acima foi visto antes de ser gerado pelos scripts
listados; os dois bugs relatados são meus (não do alvo) e estão
documentados inline no código-fonte correspondente para rastreabilidade.
