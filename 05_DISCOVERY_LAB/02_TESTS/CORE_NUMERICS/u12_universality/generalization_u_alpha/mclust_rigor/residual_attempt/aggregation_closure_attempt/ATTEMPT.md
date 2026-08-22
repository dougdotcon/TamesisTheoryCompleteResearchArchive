# ATTEMPT — fechando a agregação do hazard elevado sobre o conjunto aleatório de alvos vivos

**Onda 8 (continuação de DISC-DEC-033), frente `MCLUST-RESIDUAL-RIGOR`,
subfrente `AGGREGATION-CLOSURE`.**
**Escopo, fixado por mandato:** este documento e os arquivos desta
subpasta (`aggregation_closure_attempt/`) são um anexo NOVO que estende
`residual_attempt/ATTEMPT.md`, sem modificá-lo. Nenhum arquivo em
`residual_attempt/` ou em `mclust_rigor/` foi tocado (apenas lido).
`THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md` e `README.md` não foram tocados — integração
fica a cargo da sessão orquestradora. Nenhum commit git foi criado. A
classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ não é questionada em
lugar nenhum abaixo.

**Alvo específico:** a obstrução nomeada explicitamente em
`residual_attempt/ATTEMPT.md` §5 — o cálculo de janela deslizante ali
produz P(π(x)=y | x∉R, y∉R) ≈ (1/n)/(1−ρ) para um alvo y FIXO, mas "não
fechei a agregação: somar essa probabilidade condicional sobre TODOS os
alvos y∉R possíveis... não reproduz de forma óbvia o valor exato
P(π(x)∉R|x∉R)=1−c/n já provado — a soma ingênua dá 1, não 1−c/n". Esta
frente ataca exatamente essa agregação, do zero.

## 0. Disciplina

Li por inteiro `residual_attempt/ATTEMPT.md` (todas as seções, §0–9),
`DERIVATION_MCLUST_FIXED.md` (mecanismo e a prova de janela deslizante de
onda 4 para a taxa de encontro c), `DERIVATIONS.md` §0–3.5 (fórmula-mestre
M-q e o caso M-CLUST), e os quatro simuladores de `residual_attempt/`
(`mclust_walk_diagnostic.py`, `mclust_residual_v3.py`,
`mclust_residual_v4.py`, `mclust_residual_validate.py`) para entender a
infraestrutura já existente antes de escrever qualquer código novo.

Todo simulador nesta subpasta é implementação própria — nenhum arquivo
desta subpasta importa `mclust_residual_v4.py`, `mclust_residual_validate.py`,
`mclust_walk_diagnostic.py`, `mclust_validate.py`, ou `ualpha_sim.py`.
Sementes usadas nesta subpasta, todas novas e nunca reusadas entre si:

- `SeedSequence(20260822901)` — `lemma_direct_test.py` (§3.2, teste
  isolado em n=8000 escalado).
- `SeedSequence(20260822902)` — `lemma_direct_test_v2.py` (§3.2, tentativa
  de correção por sobreposição de janela, descartada).
- `SeedSequence(20260822903)` — `lemma_direct_test_v3_fullscale.py` (§3.2,
  teste isolado em n=65536, escala de produção — **o resultado que
  importa**).
- `SeedSequence(20260822904)` — `mclust_aggregation_validate.py` (§5,
  validação final da fórmula φ completa).

Nenhuma delas é `SeedSequence(20260822018)` (onda 4), `SeedSequence(918302033)`
ou `SeedSequence(720330339)` (`residual_attempt/`).

`quadratic_coeff_reuse_check.py` (§6) e as duas checagens de reuso em
`mclust_residual_v5.py` (§4.2) são explicitamente **triagem barata**,
reusando dados MC já gravados (`../H_true_extracted.json`,
`../../mclust_validate_results.json`, `../mclust_residual_validate_results.json`)
— não contam como validação nova, exatamente como o precedente já havia
convencionado em suas próprias checagens de reuso.

## 1. Recapitulação exata da obstrução

O predecessor (`residual_attempt/ATTEMPT.md` §5) derivou, para um alvo y
FIXO, via janela deslizante aplicada a DOIS pontos condicionados
simultaneamente:

```
P(π(x)=y | x∉R, y∉R) ≈ (1/n)·(1−c/n)^{-(b-1)} ≈ (1/n)/(1−ρ)
```

e então tentou verificar a agregação somando essa expressão sobre TODOS
os alvos y∉R, esperando recuperar P(π(x)∉R|x∉R)=1−c/n (já provado por
onda 4, exato). A soma "ingênua" (usando a forma simplificada (1/n)/(1−ρ)
vezes |R^c|≈(1−ρ)n) dá exatamente 1 — não 1−c/n — e o predecessor
concluiu (corretamente, na época) que não sabia fechar essa discrepância,
atribuindo-a a "correlações de segunda ordem entre o status-R de
diferentes pontos" não contabilizadas.

**§3 abaixo mostra que essa soma não deveria dar 1 nem 1−c/n — ela dá um
terceiro valor, P := (1−c/n)^{-(b-1)}, e deriva exatamente por quê.** A
"obstrução" era, em parte, uma confusão de normalização entre duas
probabilidades condicionais distintas (uma condicionada apenas em x∉R,
outra condicionada em x∉R E y∉R simultaneamente) — não uma correlação de
segunda ordem irredutível. Isso não invalida o instinto do predecessor de
que havia algo delicado ali (havia, e §7 abaixo localiza precisamente
onde a dificuldade genuína remanescente está) — apenas mostra que a
manifestação específica "a soma dá 1" tinha uma explicação mais simples
do que se temia.

## 2. Setup preciso do problema de agregação

Mecanismo idêntico ao já fixado (`residual_attempt/ATTEMPT.md` §1,
`DERIVATION_MCLUST_FIXED.md` §1): π permutação uniforme de [n]; sementes
i.i.d. Bernoulli(c/n) independentes de π; bloco de semente s =
{s,π(s),...,π^{b-1}(s)}; R = união dos blocos; p∈R ⟺ ∃k∈{0,...,b-1}:
π^{-k}(p) é semente.

O passeio de x₀ constrói um conjunto VISITADO ao longo do tempo,
particionado (pelo argumento de indução do simulador de passeio direto,
`mclust_walk_diagnostic.py`, reconfirmado independentemente em §3.1
abaixo por um argumento diferente) em:

- **início de arco** (arc start): x₀ em si, ou qualquer ponto alcançado
  por um sorteio de rota (f-draw) que SOBREVIVEU (caiu fora de R) — estes
  permanecem alvos válidos de fechamento para SEMPRE após criados, porque
  nunca são "consumidos" como imagem de π por um passo normal (chegar
  neles exige justamente o evento de fechamento).
- **interior de arco**: todo outro ponto visitado, que É a imagem-π já
  estabelecida do seu predecessor imediato no mesmo arco — logo
  estruturalmente inatingível por um NOVO passo-π normal (injetividade).

Y_live(t) := conjunto de inícios de arco vivos (ainda não usados como
alvo de fechamento) no instante em que a massa visitada é t; K(t) :=
|Y_live(t)|. **O objeto que faltava fechar:** dado que o passeio está em
x (x∉R, prestes a dar um passo-π normal), qual é

```
P(π(x) ∈ Y_live(t) | x∉R) = ?
```

em termos de K(t) e ρ (não apenas do valor por-alvo já derivado)?

## 3. Derivação por exposição sequencial (do zero, não é a janela deslizante do predecessor)

### 3.1 O lema

**Fato padrão (exposição sequencial de uma permutação uniforme):** uma
permutação uniforme de [n] pode ser gerada revelando imagens uma de cada
vez — mantendo um conjunto U de valores "ainda não usados como imagem"
(inicializado a [n]); para revelar π(z) de um novo argumento z, sorteia-se
uniformemente de U e remove-se o valor sorteado. Rodar esse processo em
QUALQUER ordem de consultas (inclusive adaptativa) produz exatamente a
lei de uma permutação uniforme — é o mecanismo por trás do embaralhamento
de Fisher–Yates, aplicado aqui como ferramenta de prova, não como
algoritmo do simulador.

**Exposição da janela para trás de x.** Para decidir x∈R, precisamos do
status-semente de {x,π^{-1}(x),...,π^{-(b-1)}(x)} — b pontos. Expomos
essa cadeia via o MESMO processo, para trás: revelar π^{-1}(x) (equivale
a revelar o par π^{-1}(x)→x), depois π^{-2}(x) (par π^{-2}(x)→π^{-1}(x)),
… , b−1 revelações no total. Cada revelação consome UM valor de U como
IMAGEM — os valores consumidos são exatamente {x,π^{-1}(x),...,π^{-(b-2)}(x)}
(b−1 pontos; π^{-(b-1)}(x) é usado apenas como ARGUMENTO nessa cadeia,
nunca como imagem, e permanece em U).

Como as marcas (sementes) são i.i.d. e independentes de π, condicionar em
"x∉R" (todos os b pontos da janela não-semente) não altera em nada essa
estrutura de exposição de π — é uma restrição só sobre marcas.

**Imagem para frente de x.** Consultar π(x) agora — um argumento NOVO
(x só foi usado como imagem de π^{-1}(x), nunca como argumento na direção
para frente). Pelo processo de exposição sequencial, π(x) é sorteado
uniformemente do U atual, que perdeu exatamente b−1 valores. Logo:

```
π(x) | (janela para trás revelada, x∉R) é EXATAMENTE uniforme sobre
N' = n−b+1 pontos = [n] \ {x, π^{-1}(x), ..., π^{-(b-2)}(x)}.
```

Exato em n finito (não apenas assintótico), a menos do evento de medida
O(b²/n) de um ciclo-π curto (período <b) atravessar x — desprezível no
limite n→∞, b fixo já usado em toda esta linha de pesquisa.

**Status-R do alvo, dado π(x)=y.** Para y genérico (fora da janela de x,
automaticamente garantido pois y∈U), y∈R ⟺ ∃k∈{0,...,b-1}:π^{-k}(y)
semente. Mas π^{-1}(y)=x, π^{-2}(y)=π^{-1}(x), …, π^{-(b-1)}(y)=π^{-(b-2)}(x)
— exatamente os b−1 pontos da janela de x, JÁ CONFIRMADOS não-semente
por x∉R! Só resta k=0 (y em si é semente?) — um sorteio fresco,
independente, Bernoulli(c/n). Logo:

```
P(y∉R | π(x)=y, x∉R) = 1−c/n exatamente (mesmas correções desprezíveis).
```

**Combinando:** para cada um dos N' candidatos y (cada um com
probabilidade 1/N'), independentemente P(y∉R)=1−c/n. Logo

```
P(π(x)=y, y∉R | x∉R) = (1−c/n)/N' ≈ (1−c/n)/n     [n≫b]      (3.1)
```

para todo y genérico — **densidade UNIFORME**, mesmo valor para qualquer
y∉R, independente da identidade/história de y. Somando sobre os N'
candidatos recupera exatamente P(π(x)∉R|x∉R) = 1−c/n (onda 4, §2 de
`DERIVATION_MCLUST_FIXED.md`) — checagem de consistência interna, não
uma coincidência.

**A fórmula de agregação.** Para qualquer conjunto aleatório Y de alvos
cuja pertença NÃO depende da janela local de x (formalizado: Y é
mensurável em relação à sigma-álgebra gerada por (π,marcas) fora da
vizinhança de O(b) pontos ao redor de x — válido por construção para um
conjunto de teste EXÓGENO, e válido para o Y_live REAL do passeio pela
razão causal dada em §7.1 abaixo, com a ressalva ali registrada), somando
(3.1) sobre y∈Y:

```
P(π(x)∈Y | x∉R) ≈ |Y|·(1−c/n)/n                                  (3.2)
```

E, condicionando adicionalmente no fato JÁ CONHECIDO de que todo membro
de Y_live satisfaz y∉R (verdade por construção do mecanismo — início de
arco nunca está em R), dividimos pela marginal P(y∉R|x∉R)≈1−ρ (válida
para y genérico, mesma ressalva de disjunção):

```
P(π(x) ∈ Y_live(t) | x∉R) ≈ K(t) · P/n,     P := (1−c/n)^{-(b-1)}     (3.3)
```

**(3.3) é a fórmula de agregação que fecha a lacuna nomeada em
`residual_attempt/ATTEMPT.md` §5.** P é uma quantidade DERIVADA (não
ajustada) — a mesma elevação multiplicativa 1/(1−ρ) que o predecessor
motivou por um caminho diferente (janela deslizante de dois pontos, §5
deles), agora obtida por um argumento de exposição sequencial mais
elementar, E com uma correção adicional exata: P=(1−c/n)^{-(b-1)}, um
fator (1−c/n) menor que 1/(1−ρ)=(1−c/n)^{-b}.

### 3.2 Resolvendo explicitamente o paradoxo "a soma dá 1"

Com (3.3) em mãos, podemos calcular exatamente o que o predecessor tentou
calcular. Três somas DIFERENTES, frequentemente confundidas:

```
(a) Σ_y P(π(x)=y | x∉R)                    [y varre TODO [n]]   = 1          (trivial)
(b) Σ_{y∈R^c} P(π(x)=y | x∉R)               [y varre só R^c]     = 1−c/n      (onda 4, exato)
(c) Σ_{y∈R^c} P(π(x)=y | x∉R, y∉R)          [condicionamento
                                              ADICIONAL em CADA y]  = P        (este documento)
```

(c) é a quantidade que o predecessor calculou (usando a forma
simplificada (1/n)/(1−ρ) por termo) e esperava que desse (b) — mas (c) e
(b) são objetos matematicamente DIFERENTES (um soma uma probabilidade
condicionada-em-y-específico; o outro soma uma probabilidade condicionada
só em x, sobre um subconjunto fixo de índices). Fazendo a conta
corretamente: (c) = Σ_{y∈R^c}P(π(x)=y,y∉R|x∉R)/P(y∉R|x∉R) = (1/(1−ρ))·(b)
= (1−c/n)/(1−ρ) = (1−c/n)^{1-b} = P. **Nem 1, nem 1−c/n — P.** Isso
resolve o paradoxo específico citado, analiticamente, sem invocar
nenhuma correlação de segunda ordem não contabilizada.

## 4. Validação direta do lema (isolada do passeio completo)

### 4.1 Primeira tentativa — n escalado para baixo (n=8000)

`lemma_direct_test.py`: constrói (π,R) para muitas instâncias, sorteia
x∉R, e mede a taxa empírica de π(x) cair num conjunto de teste EXÓGENO
Y_test (K_test=300 pontos, sorteados independentemente de π/marcas a
cada instância), comparando contra três previsões: "exata" (3.3) com
P=(1−c/n)^{-(b-1)}, "leading" (candidato do predecessor, P=1/(1−ρ)), e
"nula" (sem elevação nenhuma, densidade 1/n — a suposição implícita de
φ_NEW). n escalado para 8000 (de 65536) com c escalado proporcionalmente
(preserva ρ exatamente, já que ρ depende só de c/n e b).

Resultado (5 células, χ² sobre 5 pontos):

| forma | χ² |
|---|---|
| nula (sem elevação) | 34958,23 |
| leading, P=1/(1−ρ) | 34,09 |
| exata, P=(1−c/n)^{-(b-1)} | **18,86** |

A forma nula é refutada por até z=110 — a elevação é real e da ordem de
grandeza certa. A forma exata bate melhor que a leading, mas ainda deixa
χ²=18,86 para 5 células (esperado ≈5 sob ruído puro) — um resíduo
pequeno mas visível, crescendo com b (célula b=300 e b=100/c=600 com
z=−3,35 e −2,30).

### 4.2 Diagnóstico do resíduo — tentativa de correção, DESCARTADA

Hipótese: em n=8000 com K_test=300 fixo, um alvo de teste pode
coincidir, por acaso, com um dos b−1 pontos da JANELA de x (excluídos da
candidatura de π(x) por injetividade) — evento de contagem esperada
b·K_test/n, que NÃO é desprezível em n=8000 (chega a ≈15 sobreposições
esperadas por x na célula b=400). `lemma_direct_test_v2.py` tenta
corrigir subtraindo, para cada x, a contagem de sobreposição entre
Y_test e a janela de x (com correção de um bug inicial: só sobreposições
que também satisfazem ∉R contam, já que só essas entravam em K_valid em
primeiro lugar).

**Resultado: a "correção" piora o ajuste, não melhora** (χ² sobe de
12,17 — usando o MESMO conjunto de 6 células, uncorrected — para 293,07
corrected). Isso é reportado por honestidade — foi uma hipótese razoável
que **falhou empiricamente**, não uma correção válida descartada por
capricho. Interpretação (§4.3 confirma): o problema real era n=8000 ser
pequeno demais para as aproximações "n≫b" usadas na derivação, não uma
sobreposição de janela especificamente corrigível dessa forma ingênua
(subtrair candidatos sem redistribuir a massa de probabilidade removida
é ele mesmo um viés, na direção errada).

### 4.3 Escala de produção (n=65536) — o resultado que importa

`lemma_direct_test_v3_fullscale.py`: mesmo teste do §4.1 (forma exata,
sem tentativa de correção), mas em n=65536 (escala real usada em toda a
grade de validação de φ, sem reescalonamento), 4 células de estresse
(b=100/c=400, b=300/c=150, b=100/c=600, b=400/c=100 — ρ até 0,60).

```
n= 65536 b=100 c= 400.0 rho=0.4579 | emp=0.004467+-0.000136 | pred=0.004569 (z=-0.75)
n= 65536 b=300 c= 150.0 rho=0.4971 | emp=0.004738+-0.000140 | pred=0.004616 (z=+0.87)
n= 65536 b=100 c= 600.0 rho=0.6014 | emp=0.004650+-0.000139 | pred=0.004563 (z=+0.63)
n= 65536 b=400 c= 100.0 rho=0.4571 | emp=0.004508+-0.000137 | pred=0.004573 (z=-0.48)

chi2 (4 cells): 1.93
```

**χ²=1,93 para 4 células (esperado ≈4 sob ruído puro, p≈0,75) — nível de
ruído estatístico, sem viés sistemático detectável.** Isto confirma: (a)
o resíduo do §4.1 era um artefato de n=8000 ser pequeno demais para as
aproximações "n≫b, N'≈n" usadas na derivação, não um efeito físico
faltando; e (b) **a fórmula de agregação (3.3) está corretamente
derivada E validada por simulação direta, na escala de produção usada
pelo resto desta linha de pesquisa.**

**Isto fecha, com derivação de primeiros princípios E validação
numérica independente, a obstrução específica nomeada em
`residual_attempt/ATTEMPT.md` §5.**

## 5. Aplicando o lema à fórmula-mestre: φ_V5 / φ_CAND5

Seguindo exatamente o mesmo padrão estrutural que `mclust_residual_v4.py`
usou para φ_V4 (substituir o hazard padrão 1/(1−s) por P/(1−s), mantendo
q_CLUST(s)=s/(1−ρ) inalterado), mas com P DERIVADO em vez do P=1/(1−ρ)
motivado empiricamente:

```
q_CLUST(s) = s/(1−ρ)                                       [onda 4, inalterado]
P := (1−c/n)^{-(b-1)}                                       [esta frente, derivado, §3]
H_v5(t) = t − (1−t)^P · ∫₀ᵗ (1−q_CLUST(s))·(1−s)^{-P} ds
φ_v5(c,n,b) = ∫₀¹ P·(1−t)^{P-1}·exp(−c·H_v5(t)) dt
φ_CAND5(c,n,b) := (1−ρ)·φ_v5(c,n,b)                          [diluição x₀∈R, inalterada]
```

Implementado em `mclust_residual_v5.py`, com checagem de sanidade
ρ→0 ⟹ φ_V5→φ_U (verificado, diff<1e-6) e P→1.

### 5.1 Checagem barata de reuso (triagem, sementes de outras frentes)

Contra a grade de 15 células de onda 4 (`../../mclust_validate_results.json`):
φ_CAND5 mantém desvios pequenos (|dev|≲2,2%, comparável a φ_CAND).
Contra a própria grade fresca de 18 células do predecessor
(`../mclust_residual_validate_results.json`, sementes 720330339):

```
chi2 (CAND, reused 18-cell grid): 81.54
chi2 (CAND5, same 18 cells): 98.23
```

**φ_CAND5 é PIOR que φ_CAND nesta checagem barata** — a correção
(1−c/n) empurra na direção ERRADA quando embutida na fórmula integrada.

### 5.2 Validação fresca (sementes novas, obrigatória antes de confiar)

`mclust_aggregation_validate.py`, implementação própria,
`SeedSequence(20260822904)`, reproduzindo a grade de 18 células do
predecessor (comparação direta antes/depois), 211s de parede:

| | φ_NEW | φ_CAND | φ_CAND5 |
|---|---|---|---|
| χ² (18 células) | 1710,40 | 73,57 | **89,93** |
| dev% máx \|·\| | −15,56% | +3,76% | +4,71% (z) |

Log completo em `mclust_aggregation_validate.log`, dados em
`mclust_aggregation_validate_results.json`. **Confirma, com sementes
totalmente independentes das do §5.1, que φ_CAND5 é sistematicamente
PIOR que φ_CAND — não apenas ruído de uma única realização.** Em toda
célula das 18, φ_CAND5 ≤ φ_CAND (mesmo sentido, nunca inverte), e como
φ_CAND já SUBESTIMA φ verdadeiro (dev% positivo consistente), reduzir
ainda mais piora sistematicamente.

**Achado honesto:** o lema (3.3), embora derivado corretamente E
validado por simulação isolada (§4.3, χ²=1,93 em escala de produção), ao
ser substituído ingenuamente na integral H(t)/φ da fórmula-mestre, NÃO
melhora — de fato piora ligeiramente — o ajuste agregado. Isso não
invalida o lema (que é sobre um objeto diferente e mais simples — uma
única consulta isolada π(x) contra um conjunto de alvos EXÓGENO); mostra
que a PONTE entre o lema validado e a integral da fórmula-mestre não é
tão direta quanto a substituição de P por P assumiu.

## 6. Checagem cruzada barata: coeficiente quadrático de H_true(t)

Reusando `../H_true_extracted.json` (dados já coletados do simulador de
passeio direto do predecessor, sementes 918302033 — triagem, não nova
simulação), `quadratic_coeff_reuse_check.py` compara o coeficiente
quadrático medido H_true(t)/t² (t pequeno) contra as três previsões:

```
   b      c     rho |   H_true/t^2 (small t) | (1-rho/2)/(1-rho) [onda4] | 1/(1-rho) [CAND] | P=(1-c/n)^-(b-1) [CAND5]
 100  400.0  0.4579 | [  1.8461,   2.3444]    |                   1.4223 |            1.8445 |                   1.8333
  50  400.0  0.2637 | [  1.2971,   2.1425]    |                   1.1791 |            1.3581 |                   1.3498
 200  150.0  0.3676 | [  1.5571,   2.7272]    |                   1.2907 |            1.5814 |                   1.5777
   8  160.0  0.0384 | [  1.0616,   1.1589]    |                   1.0200 |            1.0399 |                   1.0349
```

Em toda célula, P (CAND5) < 1/(1−ρ) (CAND) < valor medido — ou seja, a
correção (1−c/n) empurra AINDA MAIS PARA LONGE do valor empírico
verdadeiro, na mesma direção que §5 já encontrou de forma independente
(via ajuste de φ completo, não via este coeficiente local). Duas
checagens totalmente diferentes (uma no espaço de H(t) local, outra no
espaço de φ integrado) concordam: **a refinação (1−c/n) tem o sinal
errado para o resíduo que resta depois de φ_CAND, e sua magnitude
(diferença de ~0,5–1% entre P e 1/(1−ρ)) é pequena demais frente ao gap
de 5–25% entre QUALQUER elevação constante e o H_true(t) medido.**

## 7. Diagnóstico do porquê o lema validado não fecha a fórmula-mestre

### 7.1 Por que Y_live é (razoavelmente) exógeno — mas com uma ressalva

A justificativa de §3.1 para (3.2)/(3.3) exige que a pertença de Y a
Y_live não dependa da janela LOCAL de x. Para o Y_live REAL (não um
Y_test artificial), isso é plausível pela mesma razão causal que
`mclust_walk_diagnostic.py` já usa: nenhum ponto da janela atual de x
pode já ser um início de arco de OUTRO arco, porque se fosse, o arco
ATUAL já teria disparado seu próprio fechamento ao alcançá-lo antes de
chegar em x. **Isso está correto** — mas não implica que a densidade por
alvo (3.1) seja exatamente a densidade relevante para TODO o histórico
acumulado do passeio, como §7.2 explica.

### 7.2 A peça que genuinamente falta: exclusão de imagens já consumidas em TODA a trajetória, não só na janela local de x

A derivação de §3.1 exclui apenas os b−1 pontos da janela LOCAL de x da
candidatura de π(x). Mas, ao longo de TODA a exploração até o instante
t, muitos OUTROS pontos (interior de arcos mais antigos, potencialmente
de OUTRAS trajetórias-arco não relacionadas a x) já foram "consumidos"
como imagem de π por passos normais anteriores — e por injetividade,
π(x) também não pode cair em NENHUM desses pontos, não apenas nos b−1 da
janela local de x. O número desses pontos já consumidos é
aproximadamente tn − K(t) (massa total visitada menos os K(t) inícios de
arco ainda "livres"/não consumidos) — uma exclusão de ORDEM tn, não de
ordem b.

Isso sugere que o "pool de candidatos" real para π(x), no instante em
que a massa visitada é t, tem tamanho efetivo ≈ n·(1−t) (não apenas
n−b+1≈n), e que a densidade POR ALVO relevante para a integral H(t) da
fórmula-mestre deveria escalar como ~1/[(1−t)n] e não simplesmente
~1/n — o que, aliás, é exatamente a origem estrutural do fator (1−t) na
teoria M-U herdada (não questionada aqui, mas agora com uma intuição
mais clara do MECANISMO por trás dele, não apenas aceito como dado).

**Isto é uma HIPÓTESE, não uma derivação nem uma validação nova.** Não
tentei (a) formalizar rigorosamente essa exclusão de escala global, nem
(b) reconciliá-la quantitativamente com a elevação-por-R (3.3) derivada
aqui — as duas exclusões (janela local de x, ordem b; imagens já
consumidas globalmente, ordem tn) interagem de um jeito que eu não
resolvi. É plausível que seja precisamente essa interação — não capturada
pela substituição simples "P constante multiplicando 1/(1−s)" que tanto
φ_V4 quanto φ_V5 usam — que produz o resíduo pequeno mas real (χ²≈74–90
para 18 células, contra ~18 esperado por ruído) que ambas as fórmulas
deixam. Não persegui isso mais a fundo por não ter uma forma fechada
candidata que não fosse, na prática, apenas mais uma tentativa de
ajuste — o que o mandato desta frente explicitamente proíbe apresentar
como derivação.

## 8. Uma explicação derivada (não testada por nova simulação) para a assimetria φ_V4/φ_NEW

`residual_attempt/ATTEMPT.md` §8, item 2, registra como "não explicada"
a assimetria: aplicar o fator de diluição (1−ρ) sobre φ_V4 funciona bem
(φ_CAND), mas aplicá-lo sobre φ_NEW piora drasticamente (até +61%).

**Argumento estrutural (§1 de `DERIVATIONS.md` relido com atenção): a
fórmula-mestre original — base (1−t) EXTERNA à integral de H(t) — já
representa, ela mesma, o relógio de fechamento do PRÓPRIO arco de x₀,
usando o MESMO hazard 1/(1−t) que aparece dentro da integral.** Isso
significa que φ_V4 (que substitui 1/(1−s)→P/(1−s) tanto DENTRO da
integral de H_v4 quanto na base externa (1−t)→(1−t)^P) aplica a elevação
de hazard **consistentemente a TODO passo normal-π do passeio inteiro**
— o que é exatamente correto, porque TODO passo normal-π do mecanismo
(não só o primeiro) ocorre com a origem atual ∉R (reroutes só acontecem
quando a posição atual ∈R; passos normais só quando ∉R). Isso torna
φ_V4 interpretável, de ponta a ponta, como uma aproximação a
P(cíclico | x₀∉R) — sob essa leitura, φ_true = ρ·P(cíclico|x₀∈R) +
(1−ρ)·P(cíclico|x₀∉R) ≈ ρ·0 + (1−ρ)·φ_V4 (usando P(cíclico|x₀∈R)≈0 do
lema de sombreamento) é EXATAMENTE a decomposição de probabilidade total
correta, e (1−ρ)·φ_V4 = φ_CAND funciona por essa razão limpa.

φ_NEW, por outro lado, NÃO aplica nenhuma elevação de hazard em lugar
nenhum — é uma tentativa direta de aproximar φ_true incondicionalmente
(misturando implicitamente os casos x₀∈R e x₀∉R de um jeito que não é
uma decomposição de probabilidade total limpa, já que 1/(1−ρ) diluição
adicional a favor de x0∉R sozinha não é como φ_NEW foi construído).
Multiplicar φ_NEW por (1−ρ) não corresponde a nenhuma decomposição
condicional válida — é uma dupla-aplicação/aplicação incompatível de um
fator de diluição a uma quantidade que já não estava condicionada da
forma que a diluição pressupõe, daí o resultado ruim.

**Classificação:** este é um argumento estrutural plausível e
consistente com todos os fatos conhecidos, mas é DERIVADO
qualitativamente — não o testei com uma nova simulação isolada
(exigiria, por exemplo, medir diretamente P(cíclico | x₀∉R) via um
simulador que force x₀∉R por rejeição e comparar contra φ_V4
separadamente de φ_NEW) e portanto é relatado como explicação plausível,
não como resultado provado ao mesmo padrão do lema de §3.

## 9. Honestidade — o que fechou, o que é heurístico, o que continua aberto

**O que fechou (derivado E validado por simulação independente, nível de
ruído):**

1. A obstrução específica nomeada em `residual_attempt/ATTEMPT.md` §5 —
   "como agregar a probabilidade condicional por-alvo sobre o conjunto
   de alvos vivos" — está resolvida: a fórmula correta é
   P(π(x)∈Y_live|x∉R) ≈ K(t)·(1−c/n)^{-(b-1)}/n (eq. 3.3), derivada por
   exposição sequencial (não por ajuste), e validada diretamente por
   simulação isolada, com sementes novas, na escala de produção
   (n=65536): χ²=1,93 para 4 células de estresse (§4.3).
2. O paradoxo específico "a soma ingênua dá 1, não 1−c/n" (§5 deles) tem
   explicação analítica limpa: a soma correta dá P=(1−c/n)^{-(b-1)} — um
   terceiro valor, nem 1 nem 1−c/n — porque a quantidade somada é uma
   probabilidade condicionada por-y-específico, não a marginal
   condicionada só em x (§3.2).

**O que NÃO fechou:** substituir a fórmula validada (3.3) na integral
H(t)/φ da fórmula-mestre (mesmo padrão estrutural que φ_V4 já usa) não
melhora o ajuste ao φ verdadeiro — piora ligeiramente, de forma
consistente em DUAS checagens independentes (reuso da grade do
predecessor, χ² 81,5→98,2; validação fresca com sementes próprias, χ²
73,6→89,9) e numa terceira checagem qualitativa (coeficiente quadrático
de H_true(t), §6). O resíduo pequeno mas real que já existia em φ_CAND
(χ²≈74–82 para 18 células, contra ~18 esperado) **permanece sem
explicação** depois desta frente.

**O que é heurístico/hipótese, nomeado e não escondido:**

1. §7.2 — a hipótese de que o pool de candidatos relevante para π(x)
   deveria excluir TODAS as imagens já consumidas ao longo de TODA a
   trajetória (ordem tn), não apenas a janela local de x (ordem b) — e
   que a interação dessa exclusão de escala global com a elevação-por-R
   derivada aqui é o que falta para fechar o resíduo de φ_CAND. Não
   formalizada, não testada por nova simulação.
2. §8 — a explicação estrutural da assimetria φ_V4/φ_NEW (por que a
   diluição (1−ρ) funciona emparelhada com φ_V4 mas não com φ_NEW) — um
   argumento de decomposição de probabilidade total, plausível e
   consistente com os dados, mas não testado isoladamente por simulação
   nova.

**O que continua intocado:** a aproximação de Poissonização/independência
da própria fórmula-mestre (item 3 de `residual_attempt/ATTEMPT.md` §8,
já herdado e nunca provado em rigor pleno) permanece fora do escopo
desta frente também. A classificação M-CLUST(b) ∈ U_{1/2} no limite
n→∞ não é afetada por nada acima.

## 10. Veredito

> **PROGRESSO PARCIAL — a obstrução de agregação especificamente nomeada
> foi FECHADA (derivada por primeiros princípios e validada por
> simulação independente a nível de ruído, χ²=1,93/4 em escala de
> produção), mas essa fechamento não se traduz em melhoria da fórmula φ
> integrada completa — pelo contrário, piora ligeiramente o ajuste em
> duas validações independentes com sementes novas.** A lição científica
> honesta: um lema de primeiro princípio, corretamente derivado e
> diretamente confirmado por simulação isolada, não implica
> automaticamente que substituí-lo numa fórmula integrada mais complexa
> melhore essa fórmula — a PONTE entre o lema local (uma única consulta
> π(x) contra um conjunto de alvos exógeno) e a integral global H(t)/φ
> (que soma implicitamente sobre TODA a história de exclusões
> acumuladas da trajetória, não só a vizinhança local de x) é, ela
> mesma, uma peça não trivial que esta frente identifica precisamente
> (§7.2) mas não fecha. φ_CAND (`residual_attempt/ATTEMPT.md`) continua
> sendo a melhor fórmula disponível nesta linha (χ²≈74, contra χ²≈90 do
> candidato desta frente e χ²≈1710 de φ_NEW, nos mesmos 18 pontos com
> sementes frescas) — este documento não a supera, mas caracteriza mais
> precisamente ONDE a dificuldade remanescente mora, e fecha, com prova
> e validação, a pergunta específica que havia sido nomeada como "a
> obstrução matemática concreta" no documento anterior. A classificação
> M-CLUST(b) ∈ U_{1/2} no limite n→∞ (∀ b fixo) permanece completamente
> intocada por tudo acima.

## Arquivos (todos nesta subpasta, `aggregation_closure_attempt/`)

- `ATTEMPT.md` — este documento.
- `lemma_direct_test.py` / `.log` / `_results.json` — §4.1, primeiro
  teste isolado do lema (3.1)–(3.3), n=8000 escalado, sementes 20260822901.
- `lemma_direct_test_v2.py` / `.log` / `_results.json` — §4.2, tentativa
  de correção por sobreposição de janela, DESCARTADA (piora o ajuste),
  sementes 20260822902. Mantido por honestidade sobre o processo.
- `lemma_direct_test_v3_fullscale.py` / `.log` / `_results.json` — §4.3,
  validação em escala de produção (n=65536), sementes 20260822903.
  **Este é o resultado que fecha a obstrução do lema.**
- `mclust_residual_v5.py` / `stage2_v5_reuse_check.json` — §5, fórmulas
  φ_V5/φ_CAND5 e checagem barata de reuso (sementes de outras frentes).
- `mclust_aggregation_validate.py` / `.log` / `_results.json` — §5.2,
  validação final fresca (sementes 20260822904, 18 células, 211s de
  parede). **Este é o resultado que decide se φ_CAND5 supera φ_CAND —
  não supera.**
- `quadratic_coeff_reuse_check.py` / `.json` — §6, checagem cruzada
  barata reusando `../H_true_extracted.json`.
