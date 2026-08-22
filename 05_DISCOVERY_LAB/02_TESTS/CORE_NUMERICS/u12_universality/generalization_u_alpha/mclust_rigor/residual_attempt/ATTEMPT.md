# ATTEMPT — closing the b·c/n residual left by DERIVATION_MCLUST_FIXED.md

**Onda 7, DISC-DEC-033, frente `MCLUST-RESIDUAL-RIGOR`.**
**Escopo, fixado por mandato:** este documento e os arquivos desta
subpasta (`residual_attempt/`) são um anexo novo. Nenhum arquivo
existente em `mclust_rigor/` (`DERIVATION_MCLUST_FIXED.md`,
`mclust_validate.py`, `mclust_decompose.py`, seus logs/JSON) foi
modificado. `THEOREM.md`, `DECISION_LEDGER.yaml` e `TEST_QUEUE.yaml`
também não foram tocados. Nenhum commit git foi criado. A classificação
M-CLUST(b) ∈ U_{1/2} no limite n→∞ (∀ b fixo) não é questionada em
lugar nenhum abaixo — este documento é inteiramente sobre a *taxa de
correção finito-n*, exatamente como o documento que ele estende.

**Alvo:** o resíduo sistemático deixado por φ_NEW
(`DERIVATION_MCLUST_FIXED.md` §6) — fecha 70–86% do gap original mas
deixa até −11 a −13% de desvio nos pontos mais extremos testados
(b=100,c=400: −12,6%; b=200,c=150: −11,1%), crescendo com b·c/n, "não
totalmente explicado".

## 0. Disciplina

Reli `DERIVATION_MCLUST_FIXED.md` por inteiro (não apenas o resumo),
`mclust_validate.py`, `mclust_decompose.py`, seus logs/JSON, e
`DERIVATIONS.md` §0–1 (fórmula-mestre) e §3.5 (versão original,
pré-onda-4). A re-derivação abaixo é feita do zero; todo simulador
nesta subpasta é implementação própria (não importa `ualpha_sim.py`,
`mclust_validate.py`, nem `mclust_walk_diagnostic.py` entre si além do
uso interno já documentado). Três sementes independentes e nunca
reusadas entre si nesta frente: `SeedSequence(918302033)` (simulador de
passeio direto, §3), `SeedSequence(720330339)` (validação final,
sementes novas, §6) — nenhuma delas é a `SeedSequence(20260822018)` da
onda 4.

## 1. O mecanismo, relido (confirmação, não redefinição)

Idêntico ao que `DERIVATION_MCLUST_FIXED.md` §1 já fixou: n pontos,
π uniforme; sementes i.i.d. Bernoulli(c/n); bloco de uma semente s é
{s, π(s), …, π^{b−1}(s)}; R = união dos blocos; todo ponto de R recebe
destino f(x) uniforme em [n] i.i.d., fixado de antemão; fora de R,
f = π. ρ = 1−(1−c/n)^b (exato). Sombreamento: p∈R só é alcançável pelo
passeio-π normal se π^{-1}(p)∉R ("run start"); todo membro interior de
bloco é π-inatingível de fora. A taxa de encontro condicional-ao-passeio
é exatamente c (prova por janela deslizante, §2 deles) — **este
resultado é reconfirmado abaixo por medição direta (§3) e não é
questionado**. q_CLUST(s) = s/(1−ρ) (cadeia geométrica, §3 deles) —
**também reconfirmado abaixo por medição direta**.

## 2. Duas hipóteses concretas testadas e descartadas

### 2.1 Depleção de R entre cadeias diferentes (correção O(c·s/n) ao ρ)

`DERIVATION_MCLUST_FIXED.md` §6 lista, sem testar, a hipótese de que a
aproximação "ρ(s) ≈ ρ constante" (justificada por c/n ≪ ρ) tem um
próximo termo ∝ c·s/n que poderia importar. Re-derivei isso do zero:
cada evento de reroteamento que **continua** a cadeia (cai em R fresco)
consome permanentemente um ponto de R — não só o ponto que inicia a
cadeia. O número esperado de pontos de R consumidos por evento é
ρ_eff/(1−ρ_eff) (série geométrica), não 1. Isso dá uma EDO
auto-consistente para a massa extra consumida x(s) = X(s)/n:

```
dx/ds = (c/n) · ρ_eff(s)/(1−ρ_eff(s)),   ρ_eff(s) = ρ − c·s/n − x(s),   x(0)=0
```

Implementada em `mclust_residual_ode.py` (RK4, reusa os alvos MC já
gravados de `../mclust_validate_results.json` — checagem barata antes
de gastar simulação nova). **Resultado: x(s) atinge no máximo ≈0,005
mesmo no ponto de estresse mais extremo (b=100,c=400,ρ=0,458)** — a
correção correspondente em φ (coluna V2 de `stageA_reuse_check.json`)
move o desvio de −12,64% para −12,52%: **melhoria de 0,1 ponto
percentual, três ordens de magnitude pequena demais para explicar o
resíduo de −13%.** Descartada como fonte dominante.

### 2.2 Hazard de fechamento com "pool reduzido" ingênuo (redução multiplicativa)

Hipótese: pontos sombreados (fração ρ de TODO [n]) nunca são alvo de
passo-π normal, então o "pool" competindo por fechamento deveria ser
(1−t−ρ)n em vez de (1−t)n, dando hazard 1/(1−s−ρ) em vez de 1/(1−s).
Re-derivando H_q(t) com essa troca (mantendo q_CLUST(s) de onda 4):

```
(1 − q_CLUST(s)) / (1 − s − ρ) = 1/(1−ρ)   IDENTICAMENTE em s
⟹ H_v3(t) = t²/(1−ρ),  t ∈ [0, 1−ρ)
```

Implementada em `mclust_residual_v3.py`. Substituindo t=(1−ρ)u mostra
**φ_v3(c) ≡ φ_U(c(1−ρ)) = φ_OLD(c) exatamente** (verificado
numericamente a 1e-17, `stageC_v3_reuse_check.json`) — ou seja, essa
correção é algebricamente IDÊNTICA à fórmula c_eff **já refutada** pela
onda 4 (Erro 1), apenas disfarçada por uma mudança de variável. Pior
que φ_NEW em toda a grade. **Descartada**: a subtração ingênua do pool
está estruturalmente errada do mesmo jeito que c_eff estava (mede a
densidade não-condicional em vez da condicional).

## 3. Simulador de passeio direto (medição em vez de dedução manual)

Dada a dificuldade de continuar a dedução manual com confiança (ver
tentativa de janela deslizante para P(π(x)=y | x∉R, y∉R) no rascunho
que motiva §6 abaixo — cálculo delicado, fácil de errar de novo do
mesmo jeito que o c_eff original errou), construí um simulador que
**segue uma única trajetória de x₀ passo a passo** (não o atalho
f^(2^k) de contagem cíclica), verificando a cada passo se é um evento
de reroteamento (kill/continue/survive) ou um passo normal-π
(fechamento em x₀ / fechamento em outro / avanço livre). Implementação
própria, `mclust_walk_diagnostic.py`; sementes `SeedSequence(918302033)`.

**Correção do simulador:** π é uma permutação (bijeção); se o passeio
de x₀ está fadado a colidir com massa já visitada, colide EXATAMENTE
com o início do arco mais próximo (nunca com um ponto interior de um
arco mais antigo, porque esse arco já teria disparado seu próprio
fechamento/kill ao alcançar aquele início primeiro). Logo checar
`visited[destino]` a cada passo é suficiente — não precisa de
contabilidade separada de "quais pontos são início de arco".

**Validação cruzada (contra o φ_mc independente da onda 4):** rodando
nas 4 células mais extremas (b∈{50,100,200,8}, c grande), φ̂ do
simulador de passeio bate com φ_mc da onda 4 dentro de <1,3σ em todas
(ex.: b=100,c=400: φ̂=0,03367±0,00233 vs φ_mc=0,032537±0,00027,
z=0,49) — o simulador está correto.

### 3.1 q(s) por sorteio e por cadeia: CONFIRMADOS, não são a fonte

`analyze_diagnostic.py` fez uma primeira comparação (errada — comparou
o q por-sorteio contra s/(1−ρ), que é o valor agregado-por-cadeia, não
o por-sorteio). `analyze_diagnostic2.py` corrige isso:

- **q por sorteio** (prob. de matar em UM sorteio dentro da cadeia) vs.
  **s** (previsão de onda 4, inalterada): desvios pequenos (tipicamente
  <0,03 em valor absoluto, alguns σ estatisticamente significativos mas
  sem sinal sistemático consistente — às vezes acima, às vezes abaixo).
- **kill agregado por cadeia** (prob. de a cadeia INTEIRA terminar em
  morte) vs. **s/(1−ρ)** (fórmula de onda 4, §3 deles): mesmo padrão —
  pequenos desvios, sem viés sistemático dominante.

**Conclusão: q_CLUST(s) = s/(1−ρ) está confirmado, medido diretamente
do mecanismo, com sementes e implementação próprias.** Não é a fonte do
resíduo de −13%.

### 3.2 Curva de sobrevivência S(t): aqui está o problema

Medi diretamente S(t) = P(massa final visitada ≥ t) (basta olhar a
massa final de cada trajetória — não precisa de contabilidade de
hazard) e comparei contra E[S(t)] = (1−t)·exp(−c·H_NEW(t,ρ)) previsto
por φ_NEW. **Desvio grande, sistemático, e estatisticamente enorme**
(até 20σ) em quase toda a faixa de t, sempre no mesmo sentido
(S_empírico < S_previsto — sobrevivência real cai mais rápido que a
fórmula prevê). Exemplo (b=100,c=400,ρ=0,458): em t=0,032,
S_emp=0,4193 vs S_pred=0,5384 (diff=−0,119, z=−18,7).

**Isto localiza o erro:** já que q(s) está confirmado correto (§3.1),
o problema não está na probabilidade de morte por evento — está na
OUTRA metade da fórmula-mestre, o termo de hazard de fechamento/
"crowding" (1−t)/(1−s), que `DERIVATION_MCLUST_FIXED.md` §4 herdou
"não alterada" de M-U. **Esta é uma localização nova, não listada nas
3 hipóteses de §6 deles** (que eram todas sobre a taxa efetiva do R,
não sobre o hazard de fechamento).

Testei também se a "massa extra" das cadeias (que não avança t, só s —
ver §2.1) poderia estar sendo mal contabilizada ao comparar t vs. s no
eixo da curva de sobrevivência: `mean_excess_mass`/`max_excess_mass`
gravados por célula em `mclust_walk_diagnostic_results.json` mostram
excesso máximo ≈0,0012 — mesma ordem pequena de §2.1, **não explica o
gap de S(t)**.

## 4. Extração de H_true(t) — caracterização quantitativa do resíduo

Invertendo S_emp(t) = (1−t)·exp(−c·H_true(t)) ⟹
H_true(t) = −ln(S_emp(t)/(1−t))/c, comparei H_true(t) contra H_NEW(t,ρ)
ponto a ponto (`extract_H_true.py`, dados em `H_true_extracted.json`).

**Achado 1 (qualitativo):** H_true(t) > H_NEW(t,ρ) em quase toda a
faixa de t testável (exceto na cauda extrema de t, onde a amostra fica
pequena) — consistente com φ_NEW super-estimar φ.

**Achado 2 (quantitativo, mais preciso que "cresce com b·c/n"):**
mesmo o coeficiente QUADRÁTICO (t→0) de H(t) está subestimado por
φ_NEW. Expandindo H_NEW(t,ρ) = t²·(1−ρ/2)/(1−ρ) + O(t³) (conferido por
álgebra) e medindo a razão H_true(t)/t² em t pequeno nas 3 células de
estresse:

| célula (b,c) | ρ | (1−ρ/2)/(1−ρ) [previsto onda 4] | H_true/t² medido (t pequeno) | 1/(1−ρ) [candidato] |
|---|---|---|---|---|
| b=100,c=400 | 0,4579 | 1,42 | ≈1,87–1,90 | 1,845 |
| b=50,c=400  | 0,2637 | 1,18 | ≈1,40–1,53 | 1,358 |
| b=200,c=150 | 0,3676 | 1,29 | ≈1,52–1,55 | 1,581 |

O candidato **1/(1−ρ)** (não (1−ρ/2)/(1−ρ)) descreve o coeficiente
quadrático empírico muito melhor (dentro de ~2–10%) que a fórmula de
onda 4 (subestima por 20–30%). Isso é uma caracterização mais precisa
do resíduo do que "cresce com b·c/n": **o próprio expoente quadrático
de H(t) — não só termos de ordem superior — está errado, e o valor
correto do coeficiente parece ser 1/(1−ρ)** em vez de (1−ρ/2)/(1−ρ).

Uma regressão de H_true−H_NEW contra bases candidatas
(ρt³/(1−ρ), ρt²/(1−ρ), etc., ver script inline na sessão — não
persistido por não ter dado forma fechada limpa, R²≈0,85–0,90, sem
coeficiente universal claramente melhor) não produziu uma forma fechada
única e convincente por si só — foi o gatilho para a derivação de §5,
não um resultado final.

## 5. Derivação parcial de por que 1/(1−ρ) — e a peça que falta

Tentativa de re-derivar rigorosamente P(π(x)=y | x∉R, y∉R) para um
alvo y FIXO (mesmo estilo de janela deslizante que a onda 4 usou para
a taxa de encontro, mas aplicado a DOIS pontos condicionados
simultaneamente em vez de um): condicionando em x∉R (janela de b pontos
atrás de x não-sementes) E y∉R (janela de b pontos atrás de y
não-sementes), e no caso π(x)=y as duas janelas se fundem numa cadeia
de b+1 pontos (não 2b, pela sobreposição x=π^{-1}(y)) — o cálculo de
Bayes dá, a ordem líder em c/n:

```
P(π(x)=y | x∉R, y∉R) ≈ (1/n) · (1−c/n)^{-(b-1)} ≈ (1/n)/(1−ρ)
```

Isto é consistente em DIREÇÃO e ORDEM DE GRANDEZA com o achado
empírico de §4 (elevação multiplicativa 1/(1−ρ), não subtrativa
1/(1−s−ρ) como em §2.2). **Mas não fechei a agregação**: somar essa
probabilidade condicional sobre TODOS os alvos y∉R possíveis (para
obter o hazard agregado "P(π(x)∈ algum alvo vivo)") não reproduz de
forma óbvia o valor exato P(π(x)∉R|x∉R)=1−c/n já provado — a soma
ingênua dá 1, não 1−c/n, porque as probabilidades condicionais
diferentes-y não são independentes (a estrutura de R para y diferentes
está correlacionada) e não posso simplesmente multiplicar
probabilidade-por-alvo × contagem-de-alvos. **Esta é a obstrução
matemática concreta que impediu uma prova completa**: o argumento de
janela deslizante funciona lindamente para UM alvo fixo, mas agregar
sobre o conjunto ALEATÓRIO de "todos os alvos vivos não-R" exige uma
contabilidade de correlações de segunda ordem entre R-status de
diferentes pontos que não consegui fechar no orçamento desta frente.

## 6. Fórmula candidata (motivada, verificada numericamente, não provada por completo)

Dado o resultado de §5 (elevação multiplicativa, não a forma
1/(1−s−ρ) de §2.2 que colapsa em φ_OLD), testei o modelo de hazard

```
hazard(s) = 1/[(1−ρ)(1−s)]     (elevação MULTIPLICATIVA, domínio t∈[0,1) preservado
                                 — NÃO o domínio truncado [0,1−ρ) de §2.2)
```

mantendo q_CLUST(s)=s/(1−ρ) de onda 4 (confirmado em §3.1). Isso dá
(sem forma fechada — integrada numericamente, `mclust_residual_v4.py`):

```
H_v4(t) = t − (1−t)^{1/(1−ρ)} · ∫₀ᵗ (1−q_CLUST(s))·(1−s)^{-1/(1−ρ)} ds
φ_V4(c,n,b) = ∫₀¹ (1−t)^{1/(1−ρ)−1}/(1−ρ) · exp(−c·H_v4(t)) dt
```

Checagens de sanidade: ρ→0 ⟹ φ_V4→φ_U (verificado, diff<1e-6); H_v4
perto de t=1 tende a 1 (verificado numericamente). **Isoladamente,
φ_V4 é PIOR que φ_NEW** (mais killing "local" mas a normalização de
"fechar em x₀ especificamente" fica super-elevada por um fator 1/(1−ρ)
que não é compensado — ver `stageE_v4_reuse_check.json`, coluna V4 dev%
fica entre OLD e NEW, mais perto de OLD).

**A segunda peça, necessária para a combinação funcionar: diluição por
x₀∈R.** φ é uma média sobre um x₀ UNIFORME em [n] — mas a fórmula-mestre
herdada (`DERIVATIONS.md` §1, nunca alterada por onda 4) descreve
implicitamente a exploração assumindo que x₀ começa FORA de R (seu
primeiro passo é π(x₀), não f(x₀)). Isso sempre foi inofensivo antes
de M-CLUST porque ρ = O(c/n) → 0 para M-U/M-MIX/M-PREV/M-SELF — mas
para M-CLUST(b) com b grande, ρ pode ser O(1) (até 0,60 na grade
testada aqui). Com probabilidade ρ, x₀∈R — e pela MESMA lei de
sombreamento já provada por onda 4, se x₀ é um membro interior de bloco
(fração ≈(b−1)/b de R, ou seja quase todo ρ), x₀ **nunca pode ser
alcançado por um passo-π normal** — só por um salto de cadeia raro
caindo exatamente nele (estimado ≤0,6% de probabilidade mesmo no ponto
mais extremo testado, `mclust_decompose.py`-style — negligenciável).
Logo φ(x₀ sombreado) ≈ 0, e

```
φ_true ≈ (1−ρ)·φ(x₀∉R) + ρ·0 + O(c/n negligenciável)
```

**Candidato final:**

```
φ_CAND(c,n,b) := (1−ρ) · φ_V4(c,n,b)
```

## 7. Validação

### 7.1 Checagem barata (reusa MC de onda 4, mesmas sementes deles)

`mclust_residual_v4.py` roda φ_CAND contra as 15 células já gravadas em
`../mclust_validate_results.json`: desvios caem para |dev| < 1,7% em
TODAS as 15 células (vs. até −12,64% de φ_NEW), χ² = 16,8 (15 pontos,
consistente com ruído puro, p≈0,33). Ver `stageE_v4_reuse_check.json`.
Isto é apenas triagem — sementes de onda 4, não novas.

### 7.2 Validação com sementes NOVAS e grade estendida (obrigatória antes de confiar)

`mclust_residual_validate.py`: implementação própria (não importa
nenhum outro simulador desta frente), `SeedSequence(720330339)` — nunca
usada em nenhum outro lugar desta frente ou da onda 4. Reproduz a
grade de 15 células de onda 4 (para comparação direta) **mais 3 células
novas empurrando além de qualquer coisa testada antes**
(b=300/c=150: ρ=0,497, bc/n=0,687; b=100/c=600: ρ=0,601, bc/n=0,916;
b=400/c=100: ρ=0,457, bc/n=0,610) — 18 células, 3000–4000 réplicas
cada, 212s de parede.

**Resultado (grade original de 15 células, sementes novas):**

| | φ_OLD | φ_NEW (onda 4) | φ_CAND (esta frente) |
|---|---|---|---|
| χ² (15 células) | — | 532,0 | **39,1** |
| desvio máx. \|%\| | até −49,6% | até −10,72% | **3,13%** |

**Resultado (3 células novas, além de tudo testado antes):**

| b,c | ρ | b·c/n | dev NEW | dev CAND |
|---|---|---|---|---|
| 300,150 | 0,497 | 0,687 | −13,55% (z=−19,0) | **+2,40%** (z=+2,84) |
| 100,600 | 0,601 | 0,916 | −15,05% (z=−21,4) | **+3,36%** (z=+3,93) |
| 400,100 | 0,457 | 0,610 | −11,48% (z=−15,6) | **+3,76%** (z=+4,35) |

**Total (18 células): χ²(φ_NEW) = 1592,9, χ²(φ_CAND) = 81,5** — redução
de χ² por um fator ≈19,5×. Desvio absoluto mediano cai de 2,49%
(φ_NEW) para 1,06% (φ_CAND); desvio máximo cai de −15,59% para +4,35%.
Log completo: `mclust_residual_validate.log`,
`mclust_residual_validate_results.json`.

## 8. Honestidade — o que fechou, o que não fechou, e o que continua heurístico

**O que fechou (verificado com sementes novas, fora da amostra de
calibração):** φ_CAND reduz o resíduo sistemático de onda 4 em
aproximadamente 90% em termos de desvio relativo mediano, e por um
fator ≈19,5× em χ² agregado, incluindo em 3 células deliberadamente
além de qualquer coisa testada antes (b·c/n até 0,92). Isso é uma
melhoria real, grande, e verificada — não apenas recalibrada nos mesmos
dados.

**O que NÃO fechou completamente:** χ²=81,5 para 18 células ainda é
muito maior que o esperado por ruído puro (~18) — as 3 células mais
extremas (as novas, e a b=100/c=400 original) mostram um viés residual
pequeno mas real e consistente (z entre +2,8 e +4,35, sempre no mesmo
sentido: φ_CAND agora SUBESTIMA φ ligeiramente, ao contrário de φ_NEW
que SUPERESTIMA). Isto sugere um segundo termo de correção, menor,
ainda não identificado, que também escala com b·c/n (ou ρ) mas em
sentido oposto ao termo já corrigido — dados insuficientes nesta grade
para caracterizar sua forma exata.

**O que continua heurístico/não provado por completo (nomeado, não
escondido):**

1. A elevação multiplicativa do hazard 1/[(1−ρ)(1−s)] (§6) é motivada
   por (a) um cálculo condicional de janela-deslizante para um alvo
   FIXO (§5, rigoroso até onde vai) e (b) o ajuste empírico do
   coeficiente quadrático de H_true(t) (§4) — mas a AGREGAÇÃO sobre o
   conjunto aleatório de alvos vivos (§5, último parágrafo) não foi
   fechada analiticamente. A forma final foi escolhida porque bate bem
   numericamente, não porque foi deduzida linha a linha do mecanismo.
2. **Assimetria não explicada:** aplicar o fator (1−ρ) de diluição de
   x₀∈R diretamente sobre φ_NEW (em vez de φ_V4) **piora** drasticamente
   o ajuste (até +61% de desvio na checagem de reuso, coluna
   "(1−ρ)·NEW" impressa durante a exploração desta frente, não
   persistida em arquivo por não ter sido um candidato final — ver
   histórico do terminal desta sessão) — ou seja, o fator de diluição
   só "funciona" em combinação com a versão de hazard elevado, não com
   a fórmula original. Não tenho uma explicação teórica limpa de por
   que essas duas correções precisam ser emparelhadas dessa forma
   específica em vez de, por exemplo, φ_NEW já incorporar parcialmente
   a diluição implicitamente. Isto é reportado como um ponto em aberto,
   não resolvido.
3. A aproximação de Poissonização/independência da própria fórmula-
   mestre (herdada, nunca provada em rigor pleno — item já listado por
   `DERIVATIONS.md` e por onda 4) permanece intocada e pode contribuir
   ao resíduo residual de §8 acima.

**Classificação deste resultado:** nem "fechado" nem apenas
"caracterizado" — **parcialmente fechado, com fechamento substancial
verificado**: o resíduo de onda 4 (até −13%, crescendo com b·c/n) foi
reduzido para um resíduo bem menor (até +4,4%, com sinal invertido) por
uma correção de dois componentes, cada um com justificativa parcial
mas não uma prova completa de cabo a rabo, validada com sementes e
grade novas fora da amostra usada para motivá-la. Um resíduo real,
menor e de sinal oposto permanece, e sua forma exata não foi
caracterizada além de "parece escalar residualmente com b·c/n também,
mas ~4-5× menor que antes."

## 9. Veredito

> **PARCIALMENTE FECHADO — redução substancial e verificada do resíduo,
> não fechamento completo.** Localizei a fonte do resíduo de onda 4 em
> uma peça específica da fórmula-mestre que onda 4 não tocou: o termo
> de hazard de fechamento/crowding (1−t)/(1−s), herdado sem modificação
> de M-U, mais um efeito de amostragem não contabilizado (x₀ uniforme
> tem probabilidade ρ de começar DENTRO de R, onde — pela mesma lei de
> sombreamento que onda 4 já provou — fica estruturalmente quase
> impossível de fechar ciclicamente). q_CLUST(s)=s/(1−ρ) (o resultado
> central de onda 4) foi RECONFIRMADO por medição direta do mecanismo,
> não é a fonte do resíduo. A fórmula candidata φ_CAND=(1−ρ)·φ_V4
> reduz o χ² agregado por um fator ≈19,5× (532→39 na grade original de
> onda 4; 1593→82 incluindo 3 células novas até b·c/n=0,92) usando
> sementes nunca antes usadas nesta linha — mas deixa um resíduo
> pequeno, real, de sinal oposto (~3-4σ nos pontos mais extremos), e a
> derivação tem uma peça (a agregação do hazard elevado sobre o
> conjunto de alvos vivos, §5) que não fechei analiticamente. A
> classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ permanece
> completamente intocada por tudo acima.

## Arquivos (todos nesta subpasta, `residual_attempt/`)

- `ATTEMPT.md` — este documento.
- `mclust_residual_ode.py` / `stageA_reuse_check.json` — §2.1, EDO de
  depleção entre cadeias, descartada (efeito 1000× pequeno demais).
- `mclust_residual_v3.py` / `stageC_v3_reuse_check.json` — §2.2, hazard
  subtrativo 1/(1−s−ρ), descartado (colapsa em φ_OLD, já refutado).
- `mclust_walk_diagnostic.py` / `.log` / `_results.json` — §3, simulador
  de passeio direto, implementação própria, sementes 918302033.
- `analyze_diagnostic.py` — primeira análise (com um erro de comparação
  identificado e corrigido em `analyze_diagnostic2.py`; mantido para
  registro honesto do processo, não usado nas conclusões finais).
- `analyze_diagnostic2.py` — §3.1–3.2, comparação corrigida (q por
  sorteio, q por cadeia, curva de sobrevivência).
- `extract_H_true.py` / `H_true_extracted.json` — §4, inversão de S(t)
  para H_true(t) e comparação de coeficiente quadrático.
- `mclust_residual_v4.py` / `stageE_v4_reuse_check.json` — §6, modelo de
  hazard multiplicativamente elevado (φ_V4), checagem de reuso.
- `mclust_residual_validate.py` / `.log` / `_results.json` — §7.2,
  validação final com sementes NOVAS (SeedSequence 720330339) e grade
  estendida (18 células, até b·c/n=0,92). **Este é o resultado que
  importa para confiar (ou não) na fórmula candidata.**
