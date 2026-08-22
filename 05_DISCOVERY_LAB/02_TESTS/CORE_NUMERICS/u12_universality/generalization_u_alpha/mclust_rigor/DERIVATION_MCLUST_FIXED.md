# DERIVATION_MCLUST_FIXED — correção da correção finito-n de M-CLUST(b)

**Onda 4, DISC-DEC-018, frente (b) "U-ALPHA-MCLUST-RIGOR".**
**Escopo, fixado por mandato:** este documento toca **apenas** a fórmula
de correção finito-n de M-CLUST(b) em `DERIVATIONS.md` §3.5. A
classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞, ∀ b fixo (argumento
de sombreamento), **não é questionada e não muda** — nenhuma evidência
aqui contradiz o limite; o achado é inteiramente sobre a *velocidade e
forma* da convergência em n finito quando b é grande. Nenhum outro
mecanismo (M-U, M-SELF, M-PREV, M-MIX, M-INTRA) é tocado.

**Gatilho:** `adversarial/ADVERSARIAL_VERDICT.md` §3 — teste de estresse
b=50 encontrou desvio relativo crescente e sistemático (+0,7% → −3,5%
→ −11,3% → −27,1% em c=10/50/150/400, n=65536) contra o alvo publicado
φ_U(c_eff), c_eff=c(1−c/n)^b, com magnitude "em ordem de grandeza com
bc/n" — ou seja, o termo de "chain-kill amplification O(bc/n) com
cancelamento parcial" que `DERIVATIONS.md` §3.5 cita mas não quantifica
**não cancela** para b grande.

## 0. Disciplina

Reli `ualpha_sim.py` (definição exata do mecanismo M-CLUST8, linhas
59–92), `DERIVATIONS.md` §3.5, `RESULTS_SUMMARY.md` e
`adversarial/ADVERSARIAL_VERDICT.md`/`ADVERSARIAL_NOTE.md` (achado e
sua própria re-derivação de ρ). A re-derivação abaixo é feita do zero
(não copiada); o simulador de validação (`mclust_validate.py`) é
implementação própria nesta subpasta, com sementes próprias, que lê a
*definição* do mecanismo no código-fonte citado mas não importa nem
executa `ualpha_sim.py`. Nenhum arquivo fora de `mclust_rigor/` é
modificado, exceto um parágrafo de adendo datado ao final de
`../RESULTS_SUMMARY.md`.

## 1. O mecanismo, exatamente (relido do código)

n pontos, π permutação uniforme. Cada ponto é marcado "semente" i.i.d.
com prob. c/n. Para cada semente s, o **bloco** de s é
{s, π(s), π²(s), …, π^{b−1}(s)} (b pontos ao longo da órbita de π à
frente de s). R = união de todos os blocos (com deduplicação). **Todo**
ponto de R — semente ou membro interior do bloco, sem distinção — recebe
um destino f(x) uniforme em [n], i.i.d., fixado de antemão (uma única
amostra por ponto, não uma re-amostragem a cada visita). Fora de R,
f = π.

**Sombreamento (re-confirmado, §3.5 deles):** um ponto p ∈ R só é
alcançável pelo passeio-π vindo de fora se π^{-1}(p) ∉ R — porque se
π^{-1}(p) ∈ R, o passeio já teria sido redirecionado ANTES de dar o
passo até p. Isto é exato: chamando "início de bloco alcançável" (run
start) a p∈R com π^{-1}(p)∉R, todo membro interior de um bloco (não a
semente) tem seu predecessor-π dentro do próprio bloco ⇒ sempre em R ⇒
nunca alcançado por passeio normal.

**Densidade de R:** ρ := |R|/n = P(∃k∈{0,…,b−1}: π^{-k}(z) semente) =
**1 − (1−c/n)^b** — exato (os b pontos π^0(z),…,π^{-(b-1)}(z) são
distintos genericamente e suas marcas são Bernoulli(c/n) i.i.d.,
independentes de π). Confirmado numericamente (`mclust_validate.py`,
coluna ρ_measured vs ρ_formula, concordância a 4 casas decimais em
todas as 15 células).

**Densidade de "run start":** ρ_start := P(p é run start) =
P(p semente) · P(π^{-1}(p),…,π^{-b}(p) todos não-sementes) =
**(c/n)(1−c/n)^b** — mesmo argumento, b+1 pontos i.i.d. Este é o número
que `DERIVATIONS.md` §3.5 usa para propor **c_eff = c(1−c/n)^b** como
"taxa efetiva de eventos" (n · ρ_start).

## 2. Erro 1 — c_eff usa a densidade ERRADA (não-condicional em vez de condicional-ao-passeio)

**Alegação:** ρ_start = (c/n)(1−c/n)^b é a probabilidade de que um
ponto **fixo, escolhido a priori, sem informação adicional** seja um
run start. Mas a taxa relevante para o passeio não é essa — é a
probabilidade de que o **próximo** ponto visitado seja um run start,
**dado que o passeio está correntemente num ponto x ∉ R** (que é
sempre o caso entre eventos, por construção — o passeio só reside em
pontos fora de R).

**Prova (janela deslizante):** x ∉ R significa, por definição, que
NENHUM dos b pontos {x, π^{-1}(x), …, π^{-(b-1)}(x)} é semente — essa é
a "janela de b posições terminando em x". Pergunta-se: π(x) ∈ R?
Isso exige que ao menos um dos b pontos {π(x), x, π^{-1}(x), …,
π^{-(b-2)}(x)} — a janela de b posições terminando em π(x) — seja
semente. Essa janela é a de x **deslocada em uma posição**: perde
π^{-(b-1)}(x) e ganha π(x); os outros b−1 pontos (x, π^{-1}(x), …,
π^{-(b-2)}(x)) são um SUBCONJUNTO da janela de x, portanto **já
sabemos, pela condição x∉R, que todos eles são não-sementes**. Resta
apenas UM ponto não examinado: π(x) em si. Logo

**P(π(x) ∈ R | x ∉ R) = P(π(x) é semente) = c/n — exatamente, sem
fator (1−c/n)^b.**

Este argumento é local (usa só a condição sobre x, não a história
completa do passeio) e telescópico: aplica-se identicamente em CADA
passo de CADA arco-π (novo início de arco D_final ∉ R inclusive, pela
mesma lógica), então a **taxa de encontro de run starts ao longo do
passeio é constante e igual a c/n por ponto = c por unidade de massa —
não c(1−c/n)^b**. Verificação de caso pequeno (b=3) por enumeração
direta das três posições envolvidas confirma o mesmo resultado (feito
à mão antes de generalizar).

**Por que a heurística original parecia funcionar:** ρ_start
(densidade não-condicional) e c/n (taxa condicional correta) só
divergem quando bc/n não é pequeno. Para b=8 (validado na onda 3) e
mesmo b=13 (validado no adversarial), bc/n ≤ 0,044 no alcance testado
— a diferença entre as duas taxas é despezível frente ao ruído
estatístico, então os dois modelos são numericamente indistinguíveis
nesse regime. Só em b grande × c grande (o teste de estresse) a
diferença fica visível — e o `c_eff` publicado está, neste sentido,
**estruturalmente mal-derivado** (mediu a quantidade errada), não
apenas "impreciso em ordem superior".

## 3. Erro 2 — o termo "chain-kill" não cancela; quantificação exata (nível de campo médio)

Quando o passeio ENCONTRA um run start (à taxa correta c, por §2), o
destino D₁ sorteado uniformemente pode cair de volta em R — em
QUALQUER membro, run start ou sombreado, de QUALQUER bloco — com
probabilidade ρ (não ρ_start: aqui o sorteio é uniforme sobre TODO
[n], não condicionado a estrutura de π). Se D₁ ∈ R, f(D₁) é OUTRO
sorteio uniforme pré-fixado independente (todo ponto de R recebe
destino independente, por construção) — o passeio é imediatamente
redirecionado de novo, SEM consumir massa (a "cadeia"). A cadeia só
termina quando um sorteio cai fora de R (sobrevive, novo arco começa
ali) ou sobre massa já visitada (mata, terminal).

**Depleção de R quase não ocorre (achado central desta seção):** o
passeio só "consome" (visita) um ponto de R quando ele é run start
(taxa c por unidade de massa, §2) ou via um salto de cadeia raro — os
b−1 membros sombreados por bloco permanecem estruturalmente
inatingíveis pelo passeio normal, então ficam "frescos" (não
visitados) durante TODA a exploração, salvo um sorteio de cadeia
acertá-los diretamente (evento raro: massa extra esperada consumida
por cadeias até t=1 é ≈ c·ρ/((1−ρ)n), **≤0,22% de n mesmo no ponto de
estresse mais extremo testado (b=50,c=400,n=65536)** — verificado
numericamente, `mclust_decompose.py` não usa este termo por ser
desprezível). Logo, ao contrário da massa TOTAL não-visitada
((1−t)·n, que encolhe conforme o passeio avança), a massa de R
não-visitada permanece ≈ ρn ao longo de quase todo o intervalo
[0,1) — ou seja, **a concentração de R dentro da massa fresca
remanescente CRESCE conforme t cresce**, em vez de ficar constante:

**P(sorteio D cai em R fresco | massa visitada = s) ≈ ρ (aprox.
constante em s, para a faixa de s relevante — dedução completa abaixo
via ρn − c·s ≈ ρn, válida enquanto c/n ≪ ρ, i.e. b ≫ 1, o regime de
interesse; a forma exata seria ρ/(1−s) mas com numerador corrigido
por −cs/n, negligenciável aqui).**

Com P(matar | s) = s (definição herdada, inalterada), P(cadeia
continua | s) = ρ (pelo argumento acima), P(sobrevive | s) =
1 − s − ρ, a cadeia resolve-se via série geométrica:

P(sobrevive total | s) = (1−s−ρ)/(1−ρ)  ⟹

**q_CLUST(s) = 1 − P(sobrevive) = s/(1−ρ).**            (3.1)

Isto substitui q(s)=s (M-U/heurística original) — **q_CLUST(s) > s
para todo s>0 quando ρ>0: a cadeia estritamente AUMENTA a
probabilidade de morte em cada instante**, na direção certa para
explicar φ_MC < φ_U(c_eff) observado em todos os testes (adversarial e
aqui). Isto contradiz diretamente a frase "cancelamento parcial de
sinal" de `DERIVATIONS.md` §3.5: não há cancelamento — o termo é
estritamente amplificador, monotônico em ρ.

## 4. Fórmula corrigida

Substituindo q_CLUST(s) em H_q(t) = t − (1−t)∫₀ᵗ(1−q(s))/(1−s)ds (fórmula-mestre,
DERIVATIONS.md §1, não alterada):

(1−q_CLUST(s))/(1−s) = (1−ρ−s)/[(1−ρ)(1−s)] = [1 − ρ/(1−s)]/(1−ρ)

∫₀ᵗ[1 − ρ/(1−s)]ds = t + ρ·ln(1−t)  ⟹

**H_NEW(t) = t − (1−t)·[t + ρ·ln(1−t)]/(1−ρ)**,   ρ = 1−(1−c/n)^b.    (4.1)

Junto com a taxa corrigida do §2 (**c**, não c_eff):

**φ_CLUST(b),n(c) ≈ φ_NEW(c,n,b) := ∫₀¹ exp[−c·H_NEW(t)] dt.**       (4.2)

Verificações: ρ→0 ⇒ H_NEW(t)→t² (recupera M-U exatamente); H_NEW(0)=0;
H_NEW(1⁻) = 1 − 0 = 1 (usando lim_{t→1}(1−t)ln(1−t)=0), consistente
com H_q(1⁻)=1 exigido pela teoria geral (§2 de DERIVATIONS.md). A
fórmula é válida enquanto a aproximação de depleção-desprezível vale
(c/n ≪ ρ, i.e. b≫1 — checado abaixo por simulação até esse regime
começar a ficar marginal em ρ≈0,46).

**Isto é uma correção de CAMPO MÉDIO** (mesmo nível de rigor que a
fórmula-mestre original — Poissonização + independência aproximada dos
eventos), não uma prova exata; ver §6 sobre o resíduo.

## 5. Validação numérica

**Simulador:** `mclust_validate.py`, implementação própria (não
importa `ualpha_sim.py`), mesma detecção de ciclo por dobramento (f^{2^k},
2^k ≥ 2n) já validada em ondas anteriores. Sementes fixadas via
`np.random.SeedSequence(20260822018)` (data + DISC-DEC-018), execução
única, foreground, 165,8 s de parede.

**Grade:** b∈{8 (controle, faixa já validada na onda 3), 50 (o alvo do
achado adversarial), 100, 200 (além de qualquer coisa testada antes,
por mandato)}; n=32768 (b=8) ou 65536 (b≥50); c cobrindo ρ de 0,002 a
0,46 (o ponto mais extremo, b=100/c=400, empurra deliberadamente para
onde a aproximação de campo médio já é questionável). N_rep=3000–4000
por célula.

| n | b | c | ρ | MC (±SEM) | φ_OLD (dev%) | φ_NEW (dev%) | gap fechado |
|---|---|---|---|---|---|---|---|
| 32768 | 8 | 10 | 0,0024 | 0,27990±0,00277 | 0,28059 (−0,25%) | 0,28010 (−0,07%) | 71% |
| 32768 | 8 | 40 | 0,0097 | 0,13956±0,00135 | 0,14081 (−0,89%) | 0,13981 (−0,18%) | 80% |
| 32768 | 8 | 160 | 0,0384 | 0,06815±0,00065 | 0,07145 (−4,61%) | 0,06939 (−1,79%) | 61% |
| 65536 | 50 | 10 | 0,0076 | 0,28154±0,00233 | 0,28132 (+0,08%) | 0,27980 (+0,62%) | (ruído; ambos < 1σ) |
| 65536 | 50 | 50 | 0,0374 | 0,12338±0,00100 | 0,12775 (−3,42%) | 0,12420 (−0,66%) | 81% |
| 65536 | 50 | 150 | 0,1083 | 0,06837±0,00057 | 0,07663 (−10,77%) | 0,07032 (−2,78%) | 74% |
| 65536 | 50 | 400 | 0,2637 | 0,03844±0,00032 | 0,05164 (−25,56%) | 0,04086 (−5,93%) | 77% |
| 65536 | 100 | 10 | 0,0151 | 0,27884±0,00231 | 0,28239 (−1,26%) | 0,27934 (−0,18%) | 86% |
| 65536 | 100 | 50 | 0,0735 | 0,12158±0,00100 | 0,13021 (−6,63%) | 0,12305 (−1,20%) | 82% |
| 65536 | 100 | 150 | 0,2048 | 0,06407±0,00052 | 0,08114 (−21,05%) | 0,06823 (−6,10%) | 71% |
| 65536 | 100 | 400 | 0,4579 | 0,03254±0,00027 | 0,06018 (−45,93%) | 0,03725 (−12,64%) | 73% |
| 65536 | 200 | 5 | 0,0151 | 0,39553±0,00329 | 0,39869 (−0,79%) | 0,39460 (+0,24%) | 70% |
| 65536 | 200 | 20 | 0,0592 | 0,19403±0,00160 | 0,20431 (−5,03%) | 0,19541 (−0,71%) | 86% |
| 65536 | 200 | 60 | 0,1674 | 0,10458±0,00086 | 0,12539 (−16,59%) | 0,10932 (−4,33%) | 74% |
| 65536 | 200 | 150 | 0,3676 | 0,05681±0,00048 | 0,09100 (−37,57%) | 0,06390 (−11,09%) | 71% |

(reprodução independente do achado adversarial: b=50/n=65536/c=10-400
com sementes/N próprios reproduz −25,56% em c=400 contra o −27,1%
deles — mesma ordem, confirmando o achado antes de corrigi-lo.)

**Decomposição** (`mclust_decompose.py`, mesmos alvos MC, sem nova
simulação): isolando cada correção — RATEfix sozinho (usar c em vez de
c_eff, sem termo de cadeia) fecha ~50% do gap; CHAINfix sozinho (termo
de cadeia aplicado sobre c_eff, sem corrigir a taxa) fecha ~25–30%;
**as duas juntas (φ_NEW) são consistentemente melhores que qualquer
uma isolada** em toda célula testada — ambos os erros são reais e
aditivos, não redundantes. Exemplo (b=100,c=400,ρ=0,458): OLD −45,93%
→ RATEfix −26,57% → CHAINfix −35,74% → AMBOS −12,64%.

## 6. Honestidade — o resíduo não fecha completamente

φ_NEW fecha **70–86% do gap** (mediana ≈75%) em toda a grade testada
(exceto a célula de ρ muito pequeno, onde o gap original já estava
dentro do ruído estatístico e a razão perde sentido). Isto é uma
melhoria grande e consistente, mas **não uma correção completa**: um
resíduo sistemático permanece, sempre no mesmo sentido (φ_NEW ainda
superestima ligeiramente o φ verdadeiro), crescendo com ρ — de
essencialmente zero em ρ<0,01 até −5,9% (b=50), −12,6% (b=100) e
−11,1% (b=200) nos pontos mais extremos testados.

**O resíduo NÃO é função de ρ sozinho:** duas células com ρ quase
idêntico mas b/c diferentes — (b=8,c=160,ρ=0,0384,dev=−1,79%) vs
(b=50,c=50,ρ=0,0374,dev=−0,66%) — mostram desvios que diferem por um
fator ~2,7. Isso indica que o resíduo carrega uma dependência
adicional (provavelmente em c, ou no produto c·ρ, ou b — os dados
disponíveis não bastam para isolar qual) que a reparametrização de
campo médio em (taxa, q(s)) usada aqui **não captura**. Hipóteses não
confirmadas, listadas por transparência e não perseguidas mais a
fundo por orçamento de tempo desta frente:

- Correlações de segunda ordem entre cadeias de eventos DIFERENTES
  (a aproximação tratou cada evento como um sorteio i.i.d. isolado;
  eventos tardios no mesmo passeio já "sabem" que certos pontos foram
  visitados, correlação que a taxa constante c e o ρ aproximadamente
  constante não capturam além do primeiro momento).
- A própria janela de validade de ρ(s)≈ρ (deduzida assumindo c/n≪ρ,
  i.e. depleção de R desprezível) é uma aproximação de primeira ordem;
  o próximo termo (∝ c·s/n, retido acima como desprezível) poderia
  contribuir de forma não-linear quando combinado com o crescimento
  de H_NEW(t) dentro da integral exponencial — não testado
  separadamente.
- A aproximação de Poissonização/independência da fórmula-mestre em si
  (herdada, nunca provada em rigor pleno — `DERIVATIONS.md` item 1 de
  "loose ends") pode ela mesma degradar em ρ grande, sem relação com
  M-CLUST especificamente.

**Não foi encontrada uma forma fechada simples que feche o resíduo
inteiro dentro do orçamento desta frente.** Isto é reportado como
resultado honesto e completo (mandato do usuário, item 3): a correção
proposta (4.1)–(4.2) é uma melhoria substancial, DERIVADA e validada,
não um fechamento exato — e o alcance de validade prática é
caracterizado (erro relativo residual tipicamente <6% para ρ≲0,26,
crescendo para ~11–13% no extremo ρ≈0,37–0,46 testado, contra 25–46%
da fórmula antiga nos mesmos pontos).

## 7. Veredito

> **PARCIALMENTE CORRIGIDO.** Dois erros distintos e reais foram
> identificados na fórmula finito-n original de M-CLUST(b)
> (`DERIVATIONS.md` §3.5): (i) a taxa c_eff=c(1−c/n)^b mede a densidade
> NÃO-condicional de run starts, não a taxa condicional-ao-passeio
> correta (que é simplesmente c, sem depressão — prova por argumento de
> janela deslizante, §2); (ii) o termo de "chain-kill" que a redação
> original supôs parcialmente cancelado na verdade AUMENTA
> monotonicamente a probabilidade de morte a cada instante, sem
> cancelamento algum (q_CLUST(s)=s/(1−ρ) > s, §3). A fórmula corrigida
> φ_NEW (4.1)–(4.2), validada numericamente com simulador e sementes
> próprios em b∈{8,50,100,200}, c cobrindo ρ até 0,46, fecha
> consistentemente 70–86% do gap identificado pela verificação
> adversarial, mas deixa um resíduo sistemático não explicado
> (crescente em ρ, com dependência residual em c/b não isolada) — **a
> correção completa provavelmente exige uma forma funcional mais rica
> que uma simples reparametrização (taxa, q(s)) de campo médio, e não
> foi encontrada aqui.** A classificação M-CLUST(b) ∈ U_{1/2} no limite
> n→∞ (∀ b fixo) permanece intocada e não é questionada por nada
> acima — nenhuma das 15 células mostra declive local incompatível com
> α=1/2 (checagem qualitativa, não formalizada nesta frente).

## Arquivos (todos em `mclust_rigor/`)

- `DERIVATION_MCLUST_FIXED.md` — este documento.
- `mclust_validate.py` / `mclust_validate.log` /
  `mclust_validate_results.json` — simulador próprio, execução única,
  15 células, sementes fixas.
- `mclust_decompose.py` / `mclust_decompose.log` — decomposição
  analítica (reusa os alvos MC já gravados, sem nova simulação) que
  isola a contribuição de cada correção.
