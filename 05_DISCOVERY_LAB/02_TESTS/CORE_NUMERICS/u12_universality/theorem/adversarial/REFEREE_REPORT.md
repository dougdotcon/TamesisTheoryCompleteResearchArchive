# Relatório do referee — THEOREM.md (frente `u12_universality/theorem`)

**Papel:** referee hostil de periódico de probabilidade/combinatória.
**Alvo:** `../THEOREM.md` (lido integralmente, 1325 linhas, ambas as
Etapas). **Método:** verificação passo a passo de cada prova + tentativa
de contraexemplo em cada uma; checagem numérica independente (scripts
próprios, escritos do zero, não copiados de nenhum arquivo do repositório)
de toda alegação intermediária verificável computacionalmente; refetch
independente do PDF Hansen–Jaworski.

**Scripts desta verificação** (todos nesta pasta): `ref_check1_def3_mc.py`
(simulação literal da Definição 3), `ref_check2_broken_variant.py`
(variante quebrada, testa a narrativa de size-biasing), `ref_check3_k1_density.py`
(simulação crua em n finito, sem nenhuma maquinaria contínua),
`ref_check4_exact_k1_k0.py` (enumeração exata independente K=1 + bound de
cauda + Chernoff), `ref_check5_exact_k2.py` (enumeração exata independente
K=2). Logs de execução reproduzidos abaixo, seção "Evidência numérica".

---

## Sumário executivo do referee

**Nenhum erro real foi encontrado.** Toda alegação rotulada PROVED no
documento resistiu à tentativa de contraexemplo e, onde computacionalmente
verificável, foi confirmada por rota numérica independente (código
próprio, não o do documento). A auto-classificação do documento
(PROVED / CITED / CONJECTURED / PROPOSIÇÃO CONDICIONAL) é **precisa e, se
algo, conservadora** — não encontrei nenhum caso de alegação rotulada mais
forte do que o que a prova de fato sustenta. Concordo com o sumário
executivo do documento quase inteiramente; a única divergência é de
ênfase, não de substância (ver "Veredito global" ao final).

Vereditos por item seguem abaixo, seção a seção.

---

## §2 — Definição 3 (construção explícita) e Proposição 2.4

**Verdito: SOUND, com o risco corretamente localizado.**

Ponto de atenção especial pedido pela tarefa: a Definição 3 processa as
marcas do processo de Poisson em ordem CRESCENTE de posição `S_j`, e não
na ordem em que seriam de fato visitadas por uma exploração de trajetória
única — à primeira leitura isso parece assumir implicitamente que o
"tempo de exploração" e a "posição no intervalo" são a mesma coisa, o que
não é óbvio (a trajetória de `x₀` é um único caminho, não pode ramificar;
por que processar marcas por posição, e não por ordem de visita?).

Reconstruí o argumento: isso só faz sentido porque `[0,1)` não representa
rótulos originais de `[n]`, mas sim **massa já percorrida pela exploração**
(exatamente como declarado em DERIVATION.md §2, "t = fração percorrida").
Sob essa leitura, "posição = massa percorrida no momento em que aquele
ponto é encontrado" é uma tautologia, não uma suposição extra — e as
"cabeças de arco" simultaneamente abertas correspondem a arcos cujo início
já foi revelado mas cujo fechamento-π ainda não, exatamente o dispositivo
de "revelação preguiçosa" de DERIVATION.md §1. A regra de parada («se
`S_j ≥ min_{i∈𝒜} T_i`: parar») está correta sob essa leitura: se algum
arco já fechou antes de `S_j`, a exploração real já terminou e a marca em
`S_j` nunca seria alcançada.

O que a Definição 3 **não** demonstra por si mesma (e o documento é
honesto sobre isso, rotulando-o CITED) é que este mecanismo de "massa
percorrida = intervalo `[0,t)` literal, cabeças de arco = relógios de
fechamento independentes" é de fato a representação padrão de exploração
de uma partição `PD(1)`/`GEM(1)` (Feller coupling). Não re-derivei essa
equivalência a partir de primeiros princípios (nem o documento o faz —
Proposição 2.4 é citação, não derivação, e isso está corretamente
sinalizado). Isto é exatamente o ponto de maior risco do documento
inteiro, e é rotulado como tal — não encontrei nenhum lugar em que essa
citação seja usada como se fosse mais forte do que uma citação.

**Contorno independente do risco.** Como Prop. 2.4 afeta apenas a
*interpretação* de Definição 3 como "o objeto-limite u12" (não a validade
interna de nenhuma prova §3–§5, §7, todas autocontidas a partir da
Definição 3), a pergunta que realmente importa para o valor científico do
resultado é: **Definição 3, tomada literalmente como um objeto
matemático autônomo, de fato produz φ_∞(c)=∫e^{-ct²}dt quando simulada?**
Testei isso diretamente — ver "Evidência numérica", Check 1 — e a resposta
é sim, dentro do erro estatístico esperado, em 4 valores de `c`
espalhados (0.3 a 8.0), com `|z|<0.4` em todos. Isso confirma a
Etapa-3–6 do Teorema 1 (a computação), independentemente de qualquer
questão sobre se Definição 3 é a representação "certa" do limite u12
(essa segunda questão permanece garantida apenas pela citação + pelo
controle empírico externo de `RESULTS_SUMMARY.md`/`ADVERSARIAL_VERDICT.md`
sobre `M_n(c)` finito, não por este documento).

---

## Teorema 1 (§3) — forma fechada `φ_∞(c) = ∫₀¹e^{-ct²}dt`

**Verdito: SOUND.**

Refiz cada passo à mão:

- **Passo 4 (o cálculo nuclear).** `P(Θ≥s)=1-s` ✓. Condicional a `Θ≥s`:
  `T>t ⟺ e^{-E}<(1-t)/(1-s) ⟺ E>ln((1-s)/(1-t))`, e como `s<t` isso é um
  argumento positivo bem definido para o `ln` — confirmei o sinal e a
  direção da desigualdade termo a termo. `P(E>ln((1-s)/(1-t)))=(1-t)/(1-s)`
  ✓ (uso direto de `P(E>a)=e^{-a}`). Produto: `(1-s)·(1-t)/(1-s)=1-t`,
  independente de `s` ✓ — este é o cancelamento anunciado, e a álgebra
  está correta.
- **Passo 5 (thinning de Poisson).** Marcas falham com prob. `t`
  (constante), então o número de marcas falhas em `[0,t)` é
  `Poisson(c·t·t)=Poisson(ct²)` — correto (taxa `c` × comprimento `t` ×
  prob. de falha `t`).
- **Passo 6.** `∫₀¹e^{-ct²}dt`, substituição `u=√c·t` dá a forma erf —
  álgebra trivial, correta.

**Tentativa de contraexemplo:** tentei quebrar o Passo 4 assumindo que a
"cabeça de arco irmã" gerada por uma marca sobrevivente não precisasse
também fechar depois de `t` (i.e., usar só a prob. de não-morte `1-s` em
vez do produto `(1-s)·(1-t)/(1-s)`). Isso é exatamente o erro que
`THEOREM.md` §3.1(a) já antecipa e nomeia — não encontrei um modo
diferente de quebrar o passo.

**Confirmação numérica independente (a mais forte deste relatório):**
implementação própria, do zero, do algoritmo *literal* da Definição 3
(loop com `𝒜`, `T_i`, regra de parada), sem reusar nenhum código do
documento ou de `limit_characterization/`. Simulação de Monte Carlo em
`c ∈ {0.3, 1.0, 3.0, 8.0}`, N=300.000: todos os `|z|<0.4` contra
`∫₀¹e^{-ct²}dt` (ver Check 1 abaixo). Isso testa exatamente a
correção aritmética dos Passos 1–6 sobre o objeto tal como definido —
independentemente de qualquer questão sobre se a Definição 3 é a
representação "certa" do limite `u12` (essa é a Prop. 2.4, tratada acima).

---

## §3.1 — a armadilha de size-biasing, feita explícita

**Verdito: SOUND, e a narrativa do documento é demonstravelmente correta.**

Esta é a seção que a tarefa pediu atenção especial (item i). O documento
afirma que esquecer o fator `(1-t)/(1-s)` (i.e. usar só `1-s`, prob. de
"não é morte", ignorando que a cabeça de arco irmã também precisa
sobreviver até `t`) produzido pela troca de thinning "prob. de falha `t`"
por "prob. de falha `s`" dá `Poisson(c∫₀ᵗs\,ds)=Poisson(ct²/2)`, logo o
integrando errado `e^{-ct²/2}` e a cauda errada `√(π/2)c^{-1/2}` — a
mesma constante já sinalizada pela nota adversarial da onda 2.

Implementei essa variante quebrada como um algoritmo genuinamente
diferente (marca sobrevivente não ganha relógio de fechamento próprio,
só o teste de não-morte `Θ_j≥S_j` importa) e simulei-a independentemente.
Resultado (Check 2 abaixo): a variante quebrada bate com
`∫₀¹e^{-ct²/2}dt` a `<0.2σ` em `c∈{1,3,8}`, e diverge claramente de
`∫₀¹e^{-ct²}dt` (a forma correta) — por exemplo em `c=3`: quebrada
`0.6628±0.0009` vs. predição-quebrada `0.6634` vs. forma correta
`0.5043`. Isso confirma, por simulação direta e independente (não apenas
por álgebra), que o modo de falha específico que o documento diz ter
evitado é real e produz exatamente a constante `√2` errada que a
verificação adversarial original (onda 2) havia sinalizado — e que a
prova do Teorema 1, tal como escrita, não cai nessa armadilha (Check 1
confirma o valor correto).

---

## §4 — Corolários 4.1, 4.2, 4.3

**Verdito: SOUND em todos os três.**

- **Cor. 4.1 (série).** Teste-M de Weierstrass corretamente aplicado
  (`|(-c)^kt^{2k}/k!|≤|c|^k/k!`, soma `e^{|c|}<∞`) — justifica a troca
  `∫↔Σ` de forma explícita, não apenas assumida. Sem falha encontrada.
- **Cor. 4.2 (cauda com erro rigoroso).** Refiz a integração por partes:
  `∫_z^∞e^{-u²}du = e^{-z²}/(2z) - ∫_z^∞ e^{-u²}/(2u²)du`, e como o termo
  subtraído é estritamente positivo, `0<∫_z^∞e^{-u²}du<e^{-z²}/(2z)` —
  correto. Com `z=√c`: `0<R(c)<e^{-c}/(2c)`. **Verificado numericamente**
  (Check 4b) com precisão suficiente (até 150 dígitos em `c=200`, para
  evitar cancelamento catastrófico) em `c∈{1,5,10,30,80,200}`: a
  desigualdade `0<R(c)<bound` vale exatamente como alegado em todos os
  casos — nota: um teste ingênuo com `mpmath` em precisão padrão (30–50
  dígitos) reporta falsamente `R(c)=0` em `c≥80` por cancelamento
  numérico entre dois floats quase iguais; isso é um artefato do MEU
  script de checagem, não um problema na prova (a prova é analítica,
  íntegra pela integração por partes acima, não depende de ponto
  flutuante).
- **Cor. 4.3 (padrão `a₁(n)=(n²-1)/(3n²)`).** Refiz a diferenciação
  termo-a-termo de (7.1) em `c=0`: só os termos `K=0,1` de
  `Binomial(n,c/n)` contribuem em ordem `c¹` (`K≥2` é `O(c²)`), dando
  `∂_cφ(n,c)|₀=-φ_n^{(0)}+φ_n^{(1)}=φ_n^{(1)}-1` (usando `φ_n^{(0)}=1`),
  logo `a₁(n)=1-φ_n^{(1)}=1/3-1/(3n²)=(n²-1)/(3n²)` — álgebra confere.
  **Cross-check independente:** esta fórmula reproduz exatamente os
  quatro valores que a verificação adversarial da onda 2 tinha obtido por
  EXTRAPOLAÇÃO numérica pura (não pela fórmula), gravados em
  `../limit_characterization/adversarial/adv2_extrap.json`:
  `a₁(4)=15/48`, `a₁(5)=24/75`, `a₁(6)=35/108`, `a₁(7)=48/147` — os
  quatro batem com `(n²-1)/(3n²)` exatamente. Isso é uma confirmação
  forte porque as duas rotas (extrapolação numérica cega da onda 2 vs.
  fórmula fechada deste documento) são computacionalmente independentes
  e concordam a mais de 5 dígitos nos quatro pontos onde ambas existem.

---

## Lema 2 (§5) — média por-K e densidade K=1

**Verdito: SOUND em ambas as partes provadas; conjectura K≥2 corretamente
rotulada.**

- **Média (§5.2, integral de Wallis).** A substituição `t=sinθ` e as
  identidades de fatorial duplo são padrão; `φ_K=4^K(K!)²/(2K+1)!` bate
  com os valores tabulados (`1, 2/3, 8/15, 16/35, ...`). Consistência com
  o Teorema 1 via mistura de Poisson verificada algebricamente (mesmo
  teste-M já usado em Cor. 4.1, reaplicado corretamente).
- **Densidade K=1 (§5.3, `f_{M₁}(x)=2x`).** Esta é a alegação
  genuinamente nova do documento (Etapa 1) — não estava provada em
  nenhum lugar anterior do arquivo, só a média. Refiz o cálculo dos dois
  ramos (mudança de variável para `M₁=1-L` no Ramo 1, e integração sobre
  `L` no Ramo 2) e a álgebra confere: `f_{M1}(x)=x+x=2x`.
  **Verificação independente, a partir do zero absoluto** (Check 3
  abaixo): simulei o modelo combinatório CRU (permutação uniforme de
  `n=4000` elementos + 1 índice reroteado para alvo uniforme), sem
  nenhuma maquinaria de PD(1)/GEM/processo de exploração — contagem
  direta de pontos cíclicos no grafo funcional resultante, 4000
  repetições. Resultado: média empírica `0.66802` (alvo `2/3=0.66667`);
  teste KS contra `F(x)=x²` (densidade `2x`): `D=0.0093`, `p=0.874` — sem
  rejeição, e o histograma por decis bate visualmente com `2x` em toda a
  faixa. Esta é a checagem mais forte possível para esta alegação
  específica: nem a construção da Definição 3 nem a citação da
  Proposição 2.4 são usadas, é combinatória crua em `n` finito grande.
- **Densidade geral K≥2 (§5.4).** Corretamente rotulada CONJECTURE, não
  PROVED — o documento é explícito de que a prova em K=1 usa uma
  propriedade especial (um só reroteamento perturba só um ciclo de
  fundo) que não generaliza trivialmente. Concordo com essa avaliação; a
  identidade de consistência de média (§5.4, por partes) está corretamente
  rotulada como necessária mas não suficiente para a densidade completa.

---

## §5.5 — a conexão Hansen–Jaworski

**Verdito: CONFIRMADA por refetch independente do PDF original.**

Busquei o PDF diretamente de `combinatorics.org` (URL do artigo,
independente de qualquer fetch anterior nesta árvore de sessões) e
extraí com `pdftotext -layout` (mesma ferramenta que o documento diz ter
usado, mas execução própria, arquivo próprio). O Teorema 7(ii), como
aparece literalmente no PDF extraído:

> "(ii) Suppose that 0 < x < 1 (and x is fixed). If r = n − a where
> a ∈ Z⁺ is fixed and k = ⌊xn⌋, then
> Pr{X̂ⁿᵣ = k} ∼ (1/n)·2ax(1−x²)^{a−1}."

Isto bate **literalmente, símbolo por símbolo**, com a citação em
`THEOREM.md` §5.5. Também confirmei o resumo (abstract) do artigo
verbatim — incluindo a frase exata "r vertices that are constrained to
have in-degree at most 1 and the remaining vertices have in-degree at
most 2" — que corresponde exatamente à caracterização de `a:=n-r` dada
no documento ("número de vértices permitidos in-degree até 2"). Autores,
afiliações, datas de submissão/aceite também conferem.

O documento é preciso ao afirmar que isso é evidência de suporte via
universalidade, não uma prova para o ensemble `u12` — concordo
integralmente com essa distinção (§5.5, último parágrafo antes da
citação de arquivo): os dois modelos microscópicos são genuinamente
diferentes (restrição de in-degree vs. reroteamento Bernoulli), e o
Teorema 7(ii) é um teorema sobre `T̂ⁿᵣ`, não sobre `M_n(c)`/`L(c)`.

---

## §7 — a ponte `n→∞` (item de maior risco da tarefa)

Esta é a seção que a tarefa pediu atenção especial (item iii). Vereditos
por peça:

### Proposição 3 (§7.2, redução de mistura) — **SOUND**

Verifiquei a decomposição telescópica `φ(n,c)-φ_∞(c)=A_n+B_n` por
substituição direta — soma e subtrai `Σ_KP(Bin=K)φ_K` corretamente,
sem erro.

- **Bound de `B_n`** via lema de Scheffé: a convergência pontual
  `P(Bin=K)→P(Poi=K)` para `K` fixo é o teorema-limite de Poisson
  clássico, re-derivado (não só citado) corretamente no texto; a
  invocação de Scheffé (convergência pontual de densidades em espaço de
  medida contável ⇒ convergência `L¹`/TV) é um uso padrão e de baixo
  risco, citação apropriada.
- **Bound de `A_n`** via Chernoff multiplicativo (7.3). Refiz a
  minimização: `P(X≥M)≤exp(c(e^t-1)-tM)`, minimizado em `t=ln(M/c)` dá
  exatamente `e^{-c}(ec/M)^M` — bate com o texto. **Verificado
  numericamente** (Check 4c): para `(n,c,M)∈{(50,5,15),(500,5,15),
  (5000,5,15),(200,10,25)}`, a probabilidade binomial real
  `P(X≥M)` fica sempre abaixo do bound de Chernoff, com folga de 1–2
  ordens de grandeza (o bound não é apertado, mas é válido, que é tudo
  que a prova precisa). O ponto crucial — que o bound `δ(c,M)` **não
  depende de `n`** porque `μ=np=c` é constante — está correto e é
  exatamente o que torna o argumento de "cauda uniforme em `n`" válido.
- **Combinação `ε`-`δ`:** a divisão `ε/4+ε/4` para `A_n` e o resto para
  `B_n` é análise padrão, sem passo faltando.

Tentativa de contraexemplo: procurei por uma exigência escondida de
convergência UNIFORME em `K≤M` (em vez de pontual) que o argumento
pudesse precisar sem declarar — não encontrei nenhuma: `M` é fixado
*antes* de `n→∞` (depende só de `c,ε` via o bound de Chernoff, que não
depende de `n`), então a soma finita de `M+1` termos convergindo
pontualmente é suficiente. Nenhuma lacuna.

### `K=0` e `K=1` (§7.3) — **SOUND, ambos**

`K=0`: identidade trivial e exata (`f=π` bijeção, todo ponto cíclico) —
correta, sem risco.

`K=1` (Proposição 4, `φ_n^{(1)}=2/3+1/(3n²)`): refiz a contagem de casos
dentro do ciclo `C` (Passo 3) à mão — os três casos (`U∉C`, `U=c₀`,
`U=c_d`) e suas contagens de pontos cíclicos (`0`, `1`, `L-d+1`
respectivamente) conferem por inspeção direta do grafo funcional
resultante em cada caso. A soma `Σ_{d=1}^{ℓ-1}(ℓ-d+1)=(ℓ-1)(ℓ+2)/2` e a
média sobre `L~Unif{1,...,n}` (usando `E[ℓ]`, `E[ℓ²]` padrão) reproduzem
`φ_n^{(1)}=(2n²+1)/(3n²)`.

**Verificação numérica independente** (Check 4a): enumeração exata
própria (implementação de detecção de ciclo diferente da do repositório,
aritmética racional exata) para `n=2,...,6`: concordância EXATA (frações
idênticas) com a fórmula em todos os cinco valores de `n`. Nenhuma
divergência.

### Open Lemma, `K≥2` (§7.4) — **classificação CORRETA como aberto, não
provado**

Esta é a peça que separa "Proposição Condicional 5" de um Teorema 3
completo, e o documento a rotula honestamente como não provada nem
refutada. Concordo com essa classificação. Verifiquei a tabela de
`φ_n^{(2)}` para `n=2,3,4` por enumeração exata própria (Check 5,
implementação independente): concordância EXATA com os três valores
citados (`3/4`, `17/27`, `113/192`). Não tive tempo/orçamento
computacional para reproduzir `n=5,...,8` (cresce como `n!·n²`), mas a
concordância exata nos três primeiros pontos, mais o padrão qualitativo
plausível (`φ_n^{(2)}` decrescendo monotonicamente em direção a
`8/15≈0.5333`), não dá motivo para desconfiar dos pontos restantes da
tabela.

**Ponto que o referee verificou especificamente e endossa:** o documento
recusa-se a extrapolar a taxa `O(1/n²)` de `K=1` para `K=2` porque o
desvio reescalado `n²·(φ_n^{(2)}-φ_2)` não estabiliza no intervalo
`n=2..8` (`0.867→0.992`, ainda subindo). Isto é precisamente a disciplina
correta — uma tentação natural seria extrapolar "K=1 deu O(1/n²), então
K≥2 também dá", e o documento resiste a essa tentação explicitamente,
reportando o padrão como não estabelecido em vez de assumir. Concordo que
isso é a leitura honesta dos dados: não há evidência suficiente para
afirmar OU refutar `O(1/n²)` em `K=2` a partir de `n≤8`.

### Proposição Condicional 5 (§7.5) — **rótulo correto**

A afirmação "`φ(n,c)→φ_∞(c)` condicional ao Open Lemma para todo `K≥2`"
é exatamente o que Proposição 3 + os casos `K=0,1` entregam, nem mais nem
menos. Não é chamada de "Teorema 3" em nenhum lugar do documento — a
autocontenção do rótulo está correta. A frase "PROVADO... unicamente
implicação" no rodapé de §7.2 ("o que esta proposição estabelece e não
estabelece") é uma clarificação útil que evita que um leitor apressado
leia "Proposição 3 provada" como "a ponte inteira está provada" — bom
sinal de disciplina de escrita, não uma lacuna.

---

## §8 (Conjecturas) e §9 (lista de lacunas) — auditoria de completude

**Verdito: rotulagem correta; lista de lacunas parece completa.**

Conjectura 1 (densidade geral-K) e Conjectura 2 (lei incondicional
`M(c)=min(1,√(E/c))`) estão corretamente separadas do que é provado, com
o suporte (consistência de média, testes KS, conexão Hansen–Jaworski)
listado sem ser confundido com prova. A nota "por que o Open Lemma de §7.4
não é chamado de 'Conjectura 3'" (distinção entre "objeto com forma
candidata" vs. "afirmação de convergência") é uma distinção
metodológica correta e útil — não é um jogo de rótulos para evitar
escrutínio, é uma diferença real no tipo de trabalho que falta.

Revisei a lista de 11 lacunas do §9 contra o resto do documento
procurando por lacunas NÃO listadas — não encontrei nenhuma que já não
estivesse coberta. Os itens 8 (bound de Le Cam, citado sem
re-verificação) e 9 (caso-limite `n≤c`) são exemplos de honestidade que
poderiam facilmente ter sido omitidos sem que ninguém notasse — o fato de
estarem listados é evidência a favor do rigor do processo, não uma
lacuna nova.

---

## Observações menores (não bloqueantes)

Nenhuma destas afeta a validade de qualquer prova; são notas de
precisão/estilo que um editor apontaria em revisão de forma.

1. **(7.1), enunciado da Fato 4.1:** o texto diz "Para todo `n` e todo
   `c≥0`" mas a frase seguinte restringe corretamente a `n>c`
   (necessário para `c/n` ser uma probabilidade Bernoulli válida). A
   caixa deveria dizer "para todo `n>c`" diretamente — inconsistência
   cosmética entre o enunciado formal e a prosa que o segue, já
   corrigida pelo contexto imediato, não gera erro em nenhuma prova
   downstream (todas usam `n→∞` a `c` fixo, onde `n>c` é automático).
2. **Proposição 3, qualificador "PROVED, unconditionally":** pode ser
   lido, isoladamente, como "a conclusão `φ(n,c)→φ_∞(c)` está provada
   incondicionalmente" — o que seria falso. O parágrafo seguinte
   ("What this proposition does and does not establish") corrige
   isso explicitamente, então não há erro de fato, só um rótulo que
   convida a uma leitura apressada errada se alguém parar no título da
   caixa.
3. A tabela de `n²·(φ_n^{(2)}-φ_2)` em §7.4 não foi reproduzida além de
   `n=4` por este referee (custo computacional `O(n!·n²)`); os três
   primeiros pontos (`n=2,3,4`) conferem exatamente, e não há motivo
   estrutural para desconfiar dos demais, mas registro que não é uma
   reprodução completa até `n=8`.

---

## Evidência numérica (logs das checagens deste referee)

**Check 1 — simulação literal da Definição 3 vs. forma fechada**
(`ref_check1_def3_mc.py`, N=300.000/célula, seed 20260822):

```
c=  0.30  MC=0.908427 +/- 0.000527   closed_form=0.908393   z=+0.06
c=  1.00  MC=0.747087 +/- 0.000794   closed_form=0.746824   z=+0.33
c=  3.00  MC=0.504157 +/- 0.000913   closed_form=0.504344   z=-0.20
c=  8.00  MC=0.313457 +/- 0.000847   closed_form=0.313309   z=+0.17
```

**Check 2 — variante quebrada (esquece o fechamento da cabeça irmã)**
(`ref_check2_broken_variant.py`, N=300.000/célula, seed 99001):

```
c= 1.00  MC(broken)=0.855553+/-0.000642  predicted(int e^-ct^2/2)=0.855624  true(int e^-ct^2)=0.746824
c= 3.00  MC(broken)=0.662777+/-0.000863  predicted(int e^-ct^2/2)=0.663351  true(int e^-ct^2)=0.504344
c= 8.00  MC(broken)=0.441330+/-0.000907  predicted(int e^-ct^2/2)=0.441041  true(int e^-ct^2)=0.313309
```

**Check 3 — densidade K=1, simulação crua em n finito (sem PD(1)/GEM)**
(`ref_check3_k1_density.py`, n=4000, 4000 repetições, seed 31415926):

```
mean(M1) empirical = 0.66802  target (Lemma2 K=1 mean) = 0.66667
KS vs F(x)=x^2 (density 2x):  D=0.00933  p=0.8742
```

**Check 4a — enumeração exata independente, K=1**
(`ref_check4_exact_k1_k0.py`):

```
n=2: exact=3/4    formula=3/4    match=True
n=3: exact=19/27  formula=19/27  match=True
n=4: exact=11/16  formula=11/16  match=True
n=5: exact=17/25  formula=17/25  match=True
n=6: exact=73/108 formula=73/108 match=True
```

**Check 4b — bound de cauda Cor. 4.2, alta precisão (150 dígitos p/ c=200)**

```
c=  1.0  R(c)=0.139403   bound=0.18394    0<R<bound: True
c=  5.0  R(c)=6.204e-04  bound=6.738e-04  0<R<bound: True
c= 10.0  R(c)=2.170e-06  bound=2.270e-06  0<R<bound: True
c= 30.0  R(c)=1.535e-15  bound=1.560e-15  0<R<bound: True
c= 80.0  R(c)=1.121e-37  bound=1.128e-37  0<R<bound: True
c=200.0  R(c)=3.451e-90  bound=3.460e-90  0<R<bound: True
```

**Check 4c — bound de Chernoff (7.3)**

```
n=   50 c= 5.0 M=15   P(X>=M)=7.384e-05   bound=1.535e-03   holds=True
n=  500 c= 5.0 M=15   P(X>=M)=2.057e-04   bound=1.535e-03   holds=True
n= 5000 c= 5.0 M=15   P(X>=M)=2.241e-04   bound=1.535e-03   holds=True
n=  200 c=10.0 M=25   P(X>=M)=2.607e-05   bound=3.681e-04   holds=True
```

**Check 5 — enumeração exata independente, K=2** (`ref_check5_exact_k2.py`):

```
n=2: my_exact=3/4     claimed=3/4     match=True
n=3: my_exact=17/27   claimed=17/27   match=True
n=4: my_exact=113/192 claimed=113/192 match=True
```

**Hansen–Jaworski, refetch independente:** PDF baixado diretamente de
`combinatorics.org/ojs/index.php/eljc/article/download/v21i1p18/pdf/`
nesta sessão (não reusando nenhum fetch anterior), extraído com
`pdftotext -layout`. Teorema 7(ii) e o resumo do artigo conferem
literalmente com a citação de `THEOREM.md` §5.5.

---

## Veredito global

**Concordo com a auto-classificação do sumário executivo do documento,
quase sem ressalva.** O documento afirma: núcleo analítico da Etapa 1
(Teorema 1, Corolários, Lema 2 média + densidade K=1) **sólido e
completo**; Etapa 2 fecha genuinamente uma fatia da ponte `n→∞`
(Proposição 3 + casos `K=0,1` exatos) mas deixa `K≥2` honestamente em
aberto; duas conjecturas explicitamente separadas de prova; um fato
clássico citado (Prop. 2.4), não re-derivado.

Depois de refazer cada prova à mão e testar cada alegação verificável
computacionalmente com código próprio (5 scripts, cobrindo: a construção
literal do objeto-limite, o modo de falha específico de size-biasing
citado pela própria tarefa, a densidade K=1 a partir de combinatória
crua em n finito sem nenhuma maquinaria analítica, duas enumerações
exatas independentes (K=1 e K=2), o bound de Chernoff, o bound de cauda
de alta precisão, e um refetch independente da fonte Hansen–Jaworski):
**nenhuma dessas checagens contradisse o documento; todas o confirmaram
dentro do erro estatístico esperado ou exatamente (nos casos de
aritmética racional exata)**.

O que "pode honestamente ser chamado de teorema" (na minha avaliação
independente, coincidindo com a do documento):

- **Teorema** (autocontido, sem lacuna): Teorema 1, Corolários 4.1–4.3,
  Lema 2 (média, todo `K`; densidade, `K=1`), Proposição 3, Proposição 4
  (incluindo Corolário 4.3).
- **Proposição condicional** (implicação provada, hipótese em aberto):
  Proposição Condicional 5 — o `n→∞` bridge completo depende do Open
  Lemma `K≥2`, que nem este documento nem esta verificação provam.
- **Conjectura** (suportada, não provada): densidade geral-K (§5.4/
  Conjectura 1), lei incondicional `min(1,√(E/c))` (Conjectura 2).
- **Citação, não re-derivação:** Proposição 2.4 (o elo Definição
  3 ↔ objeto-limite `PD(1)`/`GEM(1)` canônico) e o bound quantitativo
  de Le Cam.

Nenhuma alegação de "novo" foi verificada aqui além do que já constava —
não é escopo deste referee avaliar prioridade, apenas correção; a
questão de novidade permanece com a frente de prioridade, como as regras
desta sessão exigem.

