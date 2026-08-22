# ATTEMPT — a assimetria x₀ vs. os outros membros de Y_live, medida diretamente

**Onda 9, DISC-DEC-041, frente (a) `MCLUST-X0-ASYMMETRY-ATTEMPT`**
(continuação da linha `MCLUST-RESIDUAL-RIGOR`, DISC-DEC-033).

**Escopo, fixado por mandato:** este documento e os arquivos desta
subpasta (`x0_asymmetry_attempt/`) são um anexo NOVO que estende
`global_exclusion_attempt/ATTEMPT.md`, sem modificá-lo. Nenhum arquivo em
`global_exclusion_attempt/`, `aggregation_closure_attempt/`,
`residual_attempt/` ou `mclust_rigor/` foi tocado (apenas lido).
`THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `README.md`/`README_*.md`,
`PROOF_DEPENDENCY_MAP.md` e `tamesis-cycle-survival/` não foram tocados —
integração é da sessão orquestradora, não desta frente. Nenhum commit git
foi criado. Nada sob `u12_universality/theorem/` foi tocado. A
classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ (∀ b fixo) não é
questionada em lugar nenhum abaixo — tudo aqui é sobre a *fórmula de
correção finito-n*, exatamente como os três documentos que este estende.

**Alvo específico, citado literalmente do predecessor**
(`global_exclusion_attempt/ATTEMPT.md` §6, item 1(b), lista "o que
continua aberto"):

> "(b) uma possível assimetria entre x₀ (fixo desde o início, nunca criado
> por um sorteio de reroteamento) e os OUTROS membros de Y_live (todos
> criados dinamicamente por sobrevivência de reroteamento) — o formalismo
> de §2–3 assume ambos se comportam identicamente sob a mesma elevação P,
> mas isso não foi testado separadamente."

---

## 0. Disciplina

**Lido por inteiro antes de escrever qualquer linha de código:**
`DISC-DEC-041` (`00_GOVERNANCE/DECISION_LEDGER.yaml`, linhas 2335–2391);
`global_exclusion_attempt/ATTEMPT.md` (§0–7, integral);
`aggregation_closure_attempt/ATTEMPT.md` (§0–10, integral);
`residual_attempt/ATTEMPT.md` (§0–9, integral);
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` (§0–7, integral);
`generalization_u_alpha/DERIVATIONS.md` §0–3.6 e §6 (fórmula-mestre M-q,
o que o hazard 1/(1−t) representa, M-CLUST(b) original, "loose ends").
Também lidos, para entender a infraestrutura existente antes de escrever a
minha: `global_exclusion_walk_measure.py`, `mclust_global_formula.py`
(`global_exclusion_attempt/`), `mclust_aggregation_validate.py`
(`aggregation_closure_attempt/`), `mclust_residual_v4.py`
(`residual_attempt/`).

**Implementação.** Todo script desta subpasta é implementação própria.
Nenhum arquivo desta subpasta importa qualquer script de
`residual_attempt/`, `aggregation_closure_attempt/`,
`global_exclusion_attempt/`, `mclust_rigor/` ou `ualpha_sim.py`. Os cinco
scripts desta frente importam apenas uns aos outros (`x0_asym_formula.py`
→ `x0_asym_candidate.py` → `x0_asym_validate.py`; `mu_baseline_control.py`
→ `mu_baseline_precision.py`), que é a prática já registrada pelos três
documentos predecessores para scripts de uma mesma frente.

**Sementes** — todas novas, nunca reusadas entre si nem por nenhuma frente
anterior desta linha:

| semente | uso |
|---|---|
| `SeedSequence(20260822941)` | `x0_asymmetry_walk_measure.py`, estágios A/B/U (§3) |
| `SeedSequence(20260822942)` | `x0_asymmetry_walk_measure.py`, estágio R — replicação independente (§4.3) |
| `SeedSequence(20260822943)` | `x0_asym_validate.py` — validação fresca de 18 células (§5.2) |
| `SeedSequence(20260822944)` | `mu_baseline_control.py` — controle M-U (§5.4) |
| `SeedSequence(20260822945)` | `mu_baseline_precision.py` — braço de alta precisão do controle (§5.4) |

Nenhuma delas é `SeedSequence(20260822018)` (onda 4), `(918302033)` ou
`(720330339)` (`residual_attempt/`), `(20260822901)`–`(20260822904)`
(`aggregation_closure_attempt/`), ou `(20260822910)`–`(20260822911)`
(`global_exclusion_attempt/`).

**Reuso explicitamente rotulado** (mesma convenção dos predecessores para
blocos compartilhados — constantes de fórmula, não código):

- ρ = 1 − (1−c/n)^b, exato (onda 4 §1).
- ρ_start = (c/n)(1−c/n)^b, exato (onda 4 §1; usado só em §5.1–5.2).
- q_CLUST(s) = s/(1−ρ), **sem truncamento em 1** (onda 4 §3; a convenção
  não-truncada é a de `mclust_residual_v4.py`, e é mantida para que o caso
  simétrico P₀=P₁ reproduza φ_CAND a precisão de máquina, e não apenas
  aproximadamente — verificado, §2.1).
- P_lead = 1/(1−ρ) (φ_CAND) e P_exact = (1−c/n)^{-(b-1)} (φ_CAND5), como
  valores de referência a comparar.
- Médias de Monte Carlo **já gravadas** pelos predecessores
  (`mclust_global_validate_results.json` sementes 20260822911;
  `mclust_aggregation_validate_results.json` sementes 20260822904;
  `mclust_residual_validate_results.json` sementes 720330339) são usadas
  como *triagem barata*, sempre rotuladas como tal. A decisão sobre a
  única fórmula candidata desta frente (§5.2) é tomada com **simulação
  nova, sementes novas** (`x0_asym_validate.py`, 20260822943).

**Ordem de trabalho (relevante para a disciplina do mandato):**
`x0_asym_formula.py` (o modelo de duas elevações, §2.1) e a tabela da
assimetria NECESSÁRIA (§2.3) foram escritos e executados **antes** de
qualquer simulação nova desta frente. Nenhuma hipótese foi reformulada
depois de olhar os dados novos; §4 relata o teste exatamente como foi
pré-registrado, e o que veio depois (§5) está separado e rotulado como
achado secundário do mesmo levantamento, não como a hipótese testada.

---

## 1. A peça exata do formalismo que está em teste

Estado da linha (relido, não redefinido). A fórmula-mestre
(`DERIVATIONS.md` §0–1) descreve a exploração da f-órbita de x₀ como:
cada **início de arco vivo** ("arc start" ∈ Y_live) — x₀ mais cada
sobrevivente de reroteamento — carrega, individualmente, uma densidade de
hazard de fechamento 1/(1−t) por unidade de massa; x₀ é cíclico sse o
primeiro evento terminal for o fechamento em x₀ **ele mesmo**. A partir de
`residual_attempt/ATTEMPT.md` §6, essa densidade por alvo é multiplicada
por uma **elevação** P que capta o condicionamento em R:

```
hazard de fechamento em UM dado arc start = P / (1−t)   por unidade de massa
P = 1/(1−ρ)              [phi_CAND, residual_attempt §6]
P = (1−c/n)^{-(b-1)}     [phi_CAND5, aggregation_closure §3, derivado]
```

e a média sobre x₀ uniforme é feita pelo fator de diluição

```
phi_true = (1−ρ)·phi(cíclico | x₀ ∉ R) + ρ·eps,      eps := P(cíclico | x₀ ∈ R)
```

com **eps posto igual a 0** por φ_CAND, φ_CAND5 e φ_GLOBAL
(`residual_attempt/ATTEMPT.md` §6: x₀ sombreado "nunca pode ser alcançado
por um passo-π normal", com o canal restante estimado ≤0,6% e
"negligenciável").

**Duas suposições sobre x₀, e só duas, existem no formalismo:** (i) x₀
obedece à MESMA elevação P que os arc starts criados por reroteamento;
(ii) eps = 0. O mandato desta frente é (i). Mediu-se (i) diretamente (§4);
(ii) apareceu como consequência imediata do mesmo desenho experimental e
está relatado separadamente em §5.1–5.2.

**Resíduo a ser explicado.** φ_CAND continua sendo a melhor fórmula da
linha, mas subestima φ sistematicamente nas células de maior ρ/b:
+3,3% (b=300,c=150), +3,9% (b=100,c=600), +3,3% (b=400,c=100) na grade
fresca do predecessor (`mclust_global_validate_results.json`).

---

## 2. Formalização da hipótese — escrita ANTES de qualquer dado novo

### 2.1 A fórmula-mestre com DUAS elevações (derivada do zero)

Sejam

```
P0 := elevação do hazard de fechamento em x₀ ele mesmo
P1 := elevação do hazard de fechamento em CADA arc start criado por reroteamento
```

Refazendo a PGFL de Poisson de `DERIVATIONS.md` §1 do zero, mantendo as
duas elevações distintas (a base é o relógio de fechamento do próprio x₀;
cada evento de reroteamento em s mata com prob. q(s) e, caso contrário,
cria UM arc start que passa a carregar hazard P1/(1−r) para r ∈ [s,t]):

```
base:      exp(−∫₀ᵗ P0 dr/(1−r)) = (1−t)^{P0}
por evento: F(s) = (1−q(s))·((1−t)/(1−s))^{P1}
E[S(t)]  = (1−t)^{P0} · exp(−c·H(t)),
H(t)     = t − (1−t)^{P1} ∫₀ᵗ (1−q(s))(1−s)^{-P1} ds              (A)
phi      = ∫₀¹ [P0/(1−t)]·E[S(t)] dt
         = ∫₀¹ P0 (1−t)^{P0−1} exp(−c·H(t)) dt                     (B)
phi_ASYM = (1−ρ)·(B) + ρ·eps                                       (C)
```

Implementado em `x0_asym_formula.py`. Verificações embutidas (saída do
`__main__` do arquivo):

- ρ→0 ⟹ P0=P1→1 ⟹ φ→φ_U (diff < 1,6e-8);
- P1=1 e q(s)=s ⟹ H(t) = t² exatamente (conferido em t=0,1/0,5/0,9);
- **P0 = P1 = 1/(1−ρ), eps=0 reproduz φ_CAND, e P0 = P1 = (1−c/n)^{-(b-1)},
  eps=0 reproduz φ_CAND5, nas 18 células já gravadas pelo predecessor, com
  desvio relativo máximo 3,9e-5** — ou seja, (A)–(C) é uma generalização
  estrita e o caso simétrico não é uma aproximação do que os predecessores
  fizeram, é o mesmo número.

### 2.2 O estimador (o que é novo em relação ao predecessor)

`global_exclusion_walk_measure.py` (onda 9, frente anterior) mediu a
elevação AGREGADA sobre todo Y_live, separada por *profundidade de arco*.
Aqui a separação é por **identidade do alvo**. Em cada passo-π NORMAL do
passeio (posição atual ∉ R; passos de reroteamento são governados por
q_CLUST(s), fora de escopo e já reconfirmados por
`residual_attempt/ATTEMPT.md` §3.1), com n_vis pontos visitados:

```
w        := 1/(n − n_vis)  [ = 1/((1−s)n): a densidade por alvo NÃO elevada
                             que a fórmula-mestre herdada atribui a CADA
                             arc start vivo ]
peso A   = w                                  (o alvo único x₀)
peso B   = w   se o arc start do arco ATUAL não é x₀, senão 0
peso C   = (K − 1 − [B ativo])·w              (os demais arc starts vivos)
```

e o indicador correspondente de o passo efetivamente fechar naquela
categoria. As razões de Horvitz–Thompson

```
lambda_x0    = Σ hit_A / Σ peso_A
lambda_other = (Σ hit_B + Σ hit_C) / (Σ peso_B + Σ peso_C)
```

estimam consistentemente a elevação por alvo de x₀ e a dos arc starts
criados por reroteamento (cada evento carrega o seu próprio peso, logo a
variação de K e de s dentro da amostra já está contabilizada; o tempo de
parada do passeio é previsível, então vale o teorema de parada opcional
para a martingala Σ(hit − w·λ)). **Sob o formalismo atual, ambas valem a
MESMA constante P.** K é o K(t) REAL do passeio, não uma fórmula assumida.

Duas refinações metodológicas, ambas necessárias para que a separação
signifique algo:

1. **x₀ é sorteado condicionado a x₀ ∉ R** (rejeição). O predecessor
   sorteava x₀ uniforme em [n]; na fração ρ (até 0,60) de passeios com
   x₀ ∈ R, x₀ é estruturalmente quase impossível de fechar (lema do
   sombreamento) mas ainda assim contribui uma fatia inteira 1/((1−s)n)
   ao peso agregado — o que enviesa uma elevação AGREGADA para baixo e
   destruiria por completo uma separação x₀-vs-outros. Condicionar em
   x₀ ∉ R é, além disso, exatamente o condicionamento sob o qual a
   fórmula dos predecessores é definida (φ_CAND = (1−ρ)·φ_V4).
2. **Eventos terminais são classificados por COMO ocorreram:** um passo-π
   normal que fecha em x₀ (o único tipo de evento que o estimador de
   lambda_x0 pode contar) é separado de um sorteio-f que cai em x₀ (também
   torna x₀ cíclico — a órbita percorrida fecha — mas é um evento de
   reroteamento, não um fechamento-π, e não pode entrar no estimador de
   hazard).

### 2.3 A assimetria NECESSÁRIA — calculada antes de medir

Quanta assimetria seria preciso para fechar o resíduo? Fixando P1 =
P_lead = 1/(1−ρ) (o valor de φ_CAND) e resolvendo (C) para o P0 que
reproduz exatamente o φ_mc já gravado (sementes 20260822911 — reuso
rotulado, sem simulação nova), por bissecção
(`x0_asym_formula.solve_P0_needed`):

| b | c | ρ | P_lead | P₀ necessário | **P₀/P₁ necessário** |
|---|---|---|---|---|---|
| 200 | 20 | 0,0592 | 1,0629 | 1,0604 | 0,9976 |
| 100 | 50 | 0,0735 | 1,0793 | 1,0891 | 1,0091 |
| 50 | 150 | 0,1083 | 1,1214 | 1,1349 | 1,0121 |
| 200 | 60 | 0,1674 | 1,2010 | 1,2025 | 1,0012 |
| 100 | 150 | 0,2048 | 1,2575 | 1,2685 | 1,0087 |
| 50 | 400 | 0,2637 | 1,3581 | 1,3738 | 1,0116 |
| 200 | 150 | 0,3676 | 1,5814 | 1,6205 | 1,0247 |
| 400 | 100 | 0,4571 | 1,8419 | 1,9071 | **1,0354** |
| 100 | 400 | 0,4579 | 1,8445 | 1,9046 | **1,0326** |
| 300 | 150 | 0,4971 | 1,9886 | 2,0589 | **1,0354** |
| 100 | 600 | 0,6014 | 2,5086 | 2,6094 | **1,0402** |

**Requisito pré-registrado: uma assimetria POSITIVA, essencialmente nula
em ρ≲0,2 e crescendo até +2,5% a +4,0% nas cinco células de ρ≥0,37
(lambda_x0 > lambda_other).** É nas células de ρ alto que o resíduo vive,
e é lá que o requisito é grande. Isso fixou a precisão
necessária da medição em ≲1% em lambda_x0, o que por sua vez fixou o
número de passeios por célula (§3).

### 2.4 Critério de decisão, fixado antes de medir

- **H₀:** lambda_x0 = lambda_other (o formalismo atual).
- **H₁ (a hipótese do mandato, na direção que ajudaria):**
  lambda_x0 / lambda_other > 1, pelos valores da tabela acima (≈+2,5% a
  +4,0% nas células de ρ≥0,37, ≈0 nas de ρ baixo).
- Medir as duas com estimadores HT em ≥4 células de estresse e testar
  z = (λ̂₀−λ̂₁)/sem(diferença), com sem por **bootstrap de cluster sobre
  instâncias** (passeios que compartilham uma instância (π,R,f) são
  correlacionados; um sem por passeio subestimaria o erro).
- Se |z| < 2 em todas: nenhuma assimetria detectável — hipótese
  descartada como fonte do resíduo.
- Se houver assimetria sistemática **na direção certa e do tamanho certo**:
  construir φ_ASYM e validar em 18 células com sementes novas.
- Se houver assimetria significativa **na direção errada** ou sem lei
  consistente: relatar como refutação, com replicação independente antes
  de afirmar significância.

---

## 3. Desenho da medição

`x0_asymmetry_walk_measure.py`, implementação própria, passeio passo a
passo (não o atalho f^(2^k) de contagem cíclica), n = 65536, quatro
células de estresse já usadas por todos os predecessores desta linha
(b=100/c=400, b=300/c=150, b=100/c=600, b=400/c=100) **mais duas células
de ρ intermediário** (b=50/c=400 ρ=0,264; b=200/c=150 ρ=0,368) para que a
assimetria possa ser acompanhada como função de ρ e não só no extremo.
Instância reconstruída a cada 25 passeios; erros por bootstrap de cluster
(2000 réplicas, reamostragem conjunta sobre instâncias, de modo que
quantidades derivadas como a razão lambda_x0/lambda_other fiquem
corretamente correlacionadas).

Três estágios com fluxos de semente disjuntos:

| estágio | x₀ sorteado de | passeios/célula | mede |
|---|---|---|---|
| **A** | R^c (rejeição) | 200 000 – 320 000 | lambda_x0, lambda_other, φ_A = P(cíclico\|x₀∉R) |
| **B** | R (rejeição) | 300 000 – 500 000 | eps = P(cíclico\|x₀∈R) |
| **U** | [n] uniforme | 120 000 – 150 000 | φ, para checagem cruzada do simulador |

Total: ~40 min de parede (2300 s + 1755 s + 597 s, três processos em
paralelo).

**Checagem cruzada do simulador (estágio U vs. φ_mc já gravado por DOIS
predecessores com sementes independentes):**

| b,c | φ̂ (estágio U) | φ_mc (sementes 911) | z | φ_mc (sementes 904) | z |
|---|---|---|---|---|---|
| 100,400 | 0,033407±0,000523 | 0,033250±0,000275 | +0,26 | 0,032857±0,000272 | +0,93 |
| 300,150 | 0,051347±0,000654 | 0,051846±0,000430 | −0,64 | 0,051225±0,000428 | +0,16 |
| 100,600 | 0,023300±0,000433 | 0,023377±0,000192 | −0,16 | 0,023123±0,000190 | +0,37 |
| 400,100 | 0,066450±0,000892 | 0,065818±0,000556 | +0,60 | 0,065780±0,000550 | +0,64 |
| 50,400 | 0,038133±0,000603 | 0,038223±0,000311 | −0,13 | 0,038390±0,000312 | −0,38 |
| 200,150 | 0,057500±0,000796 | 0,058028±0,000484 | −0,57 | 0,057383±0,000490 | +0,13 |

|z| ≤ 0,93 em 12 comparações — sem evidência de defeito sistemático no
simulador novo.

**Checagem de probabilidade total** (φ_mc =? (1−ρ)φ_A + ρ·eps, usando as
medições independentes dos estágios A e B): contra o φ_mc do predecessor,
z = −2,55, −1,44, +0,54, +0,96, +0,26, +1,43 (χ² = 11,9 em 6 células, p≈0,06
— aceitável, com a célula b=100/c=600 em leve tensão); contra o estágio U
desta mesma frente (checagem inteiramente interna), z = −1,29, −0,45,
+0,10, +0,10, +0,74, +1,14, χ² = 3,7 em 6 células. A decomposição
condicional está internamente consistente.

---

## 4. RESULTADO PRIMÁRIO — a assimetria pré-registrada

### 4.1 A medição

Estágio A, sementes 20260822941. `P_lead` = 1/(1−ρ) é o valor comum que
φ_CAND atribui a ambas as populações.

| b | c | ρ | P_lead | **lambda_x0** | **lambda_other** | **razão** | z(dif.) |
|---|---|---|---|---|---|---|---|
| 100 | 400 | 0,4579 | 1,8445 | 1,8976±0,0166 | 1,8800±0,0168 | 1,0094±0,0119 | +0,79 |
| 300 | 150 | 0,4971 | 1,9886 | 2,0235±0,0162 | 2,1166±0,0207 | 0,9560±0,0115 | **−3,73** |
| 100 | 600 | 0,6014 | 2,5086 | 2,4834±0,0214 | 2,5840±0,0221 | 0,9611±0,0112 | **−3,42** |
| 400 | 100 | 0,4571 | 1,8419 | 1,9269±0,0161 | 1,9289±0,0219 | 0,9990±0,0133 | −0,08 |
| 200 | 150 | 0,3676 | 1,5814 | 1,6359±0,0157 | 1,6549±0,0185 | 0,9885±0,0135 | −0,84 |
| 50 | 400 | 0,2637 | 1,3581 | 1,3832±0,0154 | 1,3696±0,0148 | 1,0099±0,0147 | +0,68 |

(1,04–2,44×10⁴ fechamentos-π normais em x₀ por célula; 0,88–1,48×10⁵ nos
demais arc starts; 1 460 000 passeios no total do estágio A, mais 760 000
na replicação do estágio R.)

**Nenhuma célula mostra a assimetria POSITIVA que seria necessária**
(+2,5% a +4,0% nas quatro células de ρ≥0,37 desta grade; +1,2% em
b=50/c=400). Duas células mostram uma assimetria significativa **de
sinal oposto** (x₀ MENOS elevado que os outros, −4%), e quatro são
compatíveis com simetria exata.

### 4.2 O mesmo teste lido como razão exigida

Substituindo, célula a célula, o P1 medido (lambda_other) e o eps medido
(§5.1) em (C) e resolvendo para o P0 que reproduz φ_mc:

| b | c | **P₀/P₁ EXIGIDO pelos dados** | P₀/P₁ MEDIDO |
|---|---|---|---|
| 100 | 600 | 0,9942 | 0,9611±0,0112 |
| 300 | 150 | 0,9837 | 0,9560±0,0115 |
| 100 | 400 | 1,0068 | 1,0094±0,0119 |
| 400 | 100 | 0,9961 | 0,9990±0,0133 |
| 200 | 150 | 0,9862 | 0,9885±0,0135 |
| 50 | 400 | 0,9966 | 1,0099±0,0147 |

**A razão exigida cai inteiramente no intervalo [0,984 ; 1,007]: uma vez
medidos o nível comum da elevação e o eps, o φ verdadeiro exige que x₀ e
os demais arc starts carreguem essencialmente a MESMA elevação.** A
assimetria de +1% a +4% de §2.3 era um artefato de manter P₁ fixo no valor
teórico 1/(1−ρ); ela desaparece quando P₁ é medido em vez de suposto.

### 4.3 Replicação independente (obrigatória antes de afirmar as duas células significativas)

Duas células deram −3,4σ / −3,7σ e as seis razões falharam num teste de
homogeneidade (χ² = 19,2 em 5 g.l., p≈0,002) — uma realização só não basta.
Estágio R, `SeedSequence(20260822942)`, mesmas três células mais
interessantes (as duas significativas + um controle nulo), mesmos números
de passeios:

| b | c | run 1 (941) | run 2 (942) | z(run1−run2) |
|---|---|---|---|---|
| 100 | 600 | 0,9611±0,0112 | 0,9715±0,0113 | −0,65 |
| 300 | 150 | 0,9560±0,0115 | **1,0032±0,0122** | −2,82 |
| 400 | 100 | 0,9990±0,0133 | 0,9654±0,0130 | +1,81 |

**A célula b=300/c=150 — a de −3,73σ — NÃO replica**: a segunda
realização dá 1,0032±0,0122, compatível com simetria exata. A célula
b=100/c=600 replica (ambas ≈0,96–0,97). A célula-controle b=400/c=100
inverte o quadro (nula na primeira, −2,6σ na segunda).

Agrupando as 9 medições (6 do estágio A + 3 do R):

```
razão agrupada (só erro estatístico) : 0,9828 ± 0,0041
homogeneidade                        : chi2 = 24,87 em 8 g.l.
                                       -> os sems estão sub-dispersos ~1,76x
razão agrupada, erro inflado pela dispersão : 0,9828 ± 0,0073   (z vs 1 = -2,36)
```

**Leitura honesta:** existe, no máximo, uma assimetria de ~−1,7% (x₀
LIGEIRAMENTE MENOS elevado que os demais arc starts), marginalmente
significativa (2,4σ) depois de inflar o erro pela dispersão observada
entre realizações, e sem lei consistente célula a célula. Ela é do sinal
**errado** para ajudar: para fechar o resíduo seria preciso +2,5% a +4,0%
nas células de ρ alto, e o que se mede é −1,7%±0,7% — a diferença entre o
medido e o necessário é de 4 a 6 pontos percentuais, muitas vezes o erro
de medição.

### 4.4 Separação estrutural (mesmo papel no passeio) e perfil em s

Comparação casada por papel — "x₀ enquanto ainda é o início do arco
ATUAL" contra "outro arc start enquanto é o início do arco atual", e
"x₀ já como arc start ANTIGO" contra "outro arc start antigo" (estágio A):

| b,c | x₀ como arco atual | outro, arco atual | x₀ como antigo | outro, antigo |
|---|---|---|---|---|
| 100,600 | 2,4136±0,0687 | 2,6176±0,0751 | 2,4891±0,0223 | 2,5796±0,0232 |
| 300,150 | 1,9505±0,0396 | 2,0451±0,0547 | 2,0348±0,0179 | 2,1347±0,0226 |
| 100,400 | 1,9249±0,0539 | 1,9910±0,0561 | 1,8953±0,0174 | 1,8651±0,0176 |
| 400,100 | 1,8303±0,0360 | 1,8651±0,0516 | 1,9449±0,0182 | 1,9485±0,0245 |
| 200,150 | 1,5952±0,0387 | 1,6388±0,0498 | 1,6414±0,0168 | 1,6584±0,0202 |
| 50,400 | 1,3425±0,0531 | 1,3389±0,0503 | 1,3861±0,0161 | 1,3731±0,0154 |

Nenhuma diferença casada excede ~1,5σ com sinal consistente. **Também não
há assimetria dependente de s:** o estágio R gravou a elevação em 8 faixas
de massa visitada concentradas onde os passeios de fato vivem
(0–0,005–0,01–0,02–0,035–0,06–0,10–0,25–1); lambda_x0 acompanha
lambda_other faixa a faixa nas três células (ex.: b=100/c=600,
lambda_x0 = 2,53/2,49/2,59/2,51/2,56 contra lambda_other =
2,51/2,54/2,57/2,64/2,68). A elevação é aproximadamente constante em s,
com uma leve subida em s alto presente nas DUAS populações igualmente.

### 4.5 Veredito do teste primário

> **A hipótese nomeada em DISC-DEC-039/`global_exclusion_attempt` §6(b)
> está REFUTADA como fonte do resíduo de φ_CAND.** x₀ não carrega uma
> elevação sistematicamente maior que a dos arc starts criados por
> reroteamento; a diferença agrupada é −1,7%±0,7% (sinal oposto ao que
> ajudaria), não é homogênea entre células, e a única célula com −3,7σ
> não replicou com semente independente. Mais decisivamente (§4.2): uma
> vez medido o nível comum da elevação, o φ verdadeiro **exige** que as
> duas populações tenham a mesma elevação a ±1,6%. O formalismo estava
> certo neste ponto específico.

---

## 5. Achados secundários do mesmo levantamento

Tudo abaixo é subproduto do desenho experimental de §3, **não** a hipótese
mandatada. Está separado por isso.

### 5.1 eps = P(cíclico | x₀ ∈ R) NÃO é zero (12,5–21,7σ)

Estágio B, sementes 20260822941, 300 000–500 000 passeios por célula com
x₀ sorteado dentro de R:

| b | c | ρ | **eps medido** | eps derivado (§5.2) | ρ·eps como % de φ_mc |
|---|---|---|---|---|---|
| 100 | 400 | 0,4579 | 7,58e-4 ± 3,9e-5 | 7,85e-4 | **1,04%** |
| 300 | 150 | 0,4971 | 4,15e-4 ± 3,2e-5 | 4,52e-4 | 0,40% |
| 100 | 600 | 0,6014 | 8,50e-4 ± 4,2e-5 | 8,52e-4 | **2,19%** |
| 400 | 100 | 0,4571 | 5,23e-4 ± 4,2e-5 | 3,85e-4 | 0,36% |
| 200 | 150 | 0,3676 | 6,37e-4 ± 4,5e-5 | 5,51e-4 | 0,40% |
| 50 | 400 | 0,2637 | 1,208e-3 ± 5,6e-5 | 1,181e-3 | 0,81% |

Os dois canais previstos aparecem separados na contagem do simulador
(coluna `n_norm_x0` vs `n_rr_x0` do log): fechamento-π normal em x₀
(possível apenas quando x₀ é um *run start*) e sorteio-f caindo
exatamente em x₀. Ambos são da mesma ordem (203/176, 70/96, 154/271,
78/79, 121/70, 357/126 eventos respectivamente).

**Onde a forma derivada de §5.2 erra:** ela bate com a medição dentro de
~1,2σ em quatro das seis células, mas subestima em b=400/c=100
(3,85e-4 derivado contra 5,23e-4±4,2e-5 medido, −3,3σ) e em b=200/c=150
(5,51e-4 contra 6,37e-4±4,5e-5, −1,9σ) — as duas células de maior b com
c pequeno. Isso está registrado como limitação da derivação de ordem
líder, não escondido, e é uma das razões pelas quais φ_EPS é apresentada
como candidata sujeita a verificação adversarial, e não como resultado
fechado.

### 5.2 Uma fórmula candidata DERIVADA, `phi_EPS`, e sua validação fresca

Derivação (ordem líder; mesmo nível de rigor de campo médio do resto da
linha — **não é prova**; `x0_asym_candidate.py` documenta cada passo):

- **canal run-start:** dado x₀ ∈ R, um passo-π normal só pode alcançar x₀
  se π^{-1}(x₀) ∉ R, i.e. se x₀ é run start; P(run start | x₀∈R) =
  ρ_start/ρ com ρ_start = (c/n)(1−ρ). Condicionalmente a isso, x₀ é um
  alvo vivo desde t=0 com a mesma elevação que qualquer arc start (o
  cálculo de janela deslizante para um alvo run-start dá (1−c/n)^{-b} =
  1/(1−ρ) = P, exatamente o P que φ_CAND já usa), logo a probabilidade de
  retorno é, a ordem líder, o MESMO φ_cond = φ_V4. *(Passo heurístico,
  rotulado: o passeio a partir de um x₀ ∈ R começa com um salto-f e não
  com um passo-π, então sua exploração não é literalmente idêntica —
  apenas seu papel como ALVO é.)*
- **canal sorteio-f:** cada sorteio f é uniforme em [n] e independente de
  tudo, contribuindo E[#sorteios]/n; eventos de reroteamento ocorrem à
  taxa c por unidade de massa (onda 4 §2, exato) e cada cadeia faz
  1/(1−ρ) sorteios em média (onda 4 §3), logo E[#sorteios] =
  (c/(1−ρ))·T, com T = ∫₀¹ S(t)dt calculado pela própria fórmula.

```
eps      = (rho_start/rho)·phi_cond + (c/((1−rho)·n))·T
phi_EPS := (1−rho)·phi_cond + rho·eps
         = (1−rho)·phi_cond·(1 + c/n) + rho·c·T/((1−rho)·n)
```

Sem parâmetro ajustado; reduz-se a φ_CAND identicamente quando c/n→0
(verificado, diff < 5e-7 relativo em n=1e8/1e9). Cada canal foi conferido
contra a medição do estágio B **antes** de ser escrito como fórmula: o
canal run-start reproduz a contagem medida com razão 0,75–1,17 e o canal
sorteio-f com razão 0,99–1,53 nas seis células (as duas piores razões do canal
sorteio-f, b=400/c=100 (1,53) e b=200/c=150 (1,18), são as de menor
contagem — 79 e 70 eventos, ou seja 11%–12% de erro estatístico só de
Poisson; as duas piores do canal run-start, b=300/c=150 (0,75) e
b=400/c=100 (1,17), têm 70 e 78 eventos).

**Validação fresca, obrigatória** (`x0_asym_validate.py`,
`SeedSequence(20260822943)`, 18 células — a mesma grade das três últimas
validações da linha; conjunto cíclico calculado por quadratura iterada
F←F[F], com uma implementação independente por *peeling* de grau de
entrada auditando cada 200ª instância, e ambas conferidas contra
seguimento bruto de órbita em 200 mapas aleatórios pequenos):

| b | c | ρ | φ_mc (943) | φ_CAND dev% (z) | **φ_EPS dev% (z)** |
|---|---|---|---|---|---|
| 8 | 10 | 0,0024 | 0,281510±0,002283 | +0,61 (+0,74) | +0,58 (+0,71) |
| 8 | 40 | 0,0097 | 0,140936±0,001170 | +1,13 (+1,35) | +1,01 (+1,20) |
| 8 | 160 | 0,0384 | 0,068648±0,000572 | +0,04 (+0,05) | −0,47 (−0,56) |
| 50 | 10 | 0,0076 | 0,280280±0,002082 | +0,50 (+0,67) | +0,48 (+0,65) |
| 50 | 50 | 0,0374 | 0,123371±0,000899 | +0,55 (+0,75) | +0,47 (+0,64) |
| 50 | 150 | 0,1083 | 0,069077±0,000506 | +1,46 (+1,96) | +1,20 (+1,62) |
| 50 | 400 | 0,2637 | 0,038703±0,000284 | +2,39 (+3,17) | +1,55 (+2,08) |
| 100 | 10 | 0,0151 | 0,280362±0,002076 | +1,01 (+1,36) | +1,00 (+1,34) |
| 100 | 50 | 0,0735 | 0,121317±0,000879 | +0,99 (+1,36) | +0,91 (+1,24) |
| 100 | 150 | 0,2048 | 0,064767±0,000481 | +1,10 (+1,47) | +0,81 (+1,09) |
| 100 | 400 | 0,4579 | 0,032869±0,000246 | +1,95 (+2,55) | +0,82 (+1,09) |
| 200 | 5 | 0,0151 | 0,394471±0,002890 | +0,76 (+1,03) | +0,75 (+1,02) |
| 200 | 20 | 0,0592 | 0,192778±0,001417 | +0,86 (+1,15) | +0,82 (+1,11) |
| 200 | 60 | 0,1674 | 0,105236±0,000778 | +1,75 (+2,32) | +1,64 (+2,18) |
| 200 | 150 | 0,3676 | 0,057362±0,000428 | +1,15 (+1,52) | +0,79 (+1,05) |
| 300 | 150 | 0,4971 | 0,051852±0,000383 | +3,30 (+4,33) | +2,84 (+3,75) |
| 100 | 600 | 0,6014 | 0,023496±0,000172 | +4,39 (+5,74) | +2,07 (+2,76) |
| 400 | 100 | 0,4571 | 0,066467±0,000494 | +4,27 (+5,50) | +3,98 (+5,15) |

```
chi2 (18 células, sementes NOVAS 20260822943): phi_CAND = 121,69   phi_EPS = 71,98
```

E, como triagem barata nas três grades já gravadas por predecessores
(reuso rotulado, sem simulação nova): χ² 73,57→46,59 (sementes 904),
79,99→44,13 (sementes 911), 81,54→49,99 (sementes 720330339). A melhoria
é consistente nas **quatro** grades independentes.

**Status honesto de φ_EPS:** é uma melhoria real, derivada e sem
parâmetro livre, mas **não fecha o resíduo** (χ²=72 contra ~18 esperado
por ruído puro) e piora marginalmente uma célula de ρ baixo
(b=8/c=160: +0,04% → −0,47%, ambos dentro do ruído). Ela também é
*pequena* comparada ao que falta: o grosso do resíduo está no nível da
elevação (§5.3), não aqui. **Esta é uma alegação positiva; pelo padrão
desta linha ela exige verificação adversarial independente antes de
qualquer catalogação, e esta frente NÃO a declara integrada nem substitui
φ_CAND como fórmula de registro.**

### 5.3 Onde o resíduo realmente mora: o NÍVEL da elevação comum

A elevação comum medida (razão HT agregando as duas populações,
`lambda_bar`) é **sistematicamente maior** que 1/(1−ρ):

| b,c | ρ | P_lead | lambda_bar (run A) | lambda_bar/P_lead | (run R) |
|---|---|---|---|---|---|
| 50,400 | 0,2637 | 1,3581 | 1,3709 | 1,0094 | — |
| 100,400 | 0,4579 | 1,8445 | 1,8820 | 1,0203 | — |
| 100,600 | 0,6014 | 2,5086 | 2,5729 | 1,0256 | 1,0375 |
| 200,150 | 0,3676 | 1,5814 | 1,6517 | 1,0445 | — |
| 400,100 | 0,4571 | 1,8419 | 1,9284 | 1,0470 | 1,0434 |
| 300,150 | 0,4971 | 1,9886 | 2,0991 | 1,0555 | 1,0345 |

Substituindo esse valor MEDIDO como a elevação comum (P₀=P₁=lambda_bar) e
o eps MEDIDO em (C) — decomposição de `x0_asym_analysis.py` §5, contra o
φ_mc gravado com sementes 20260822911:

| ingrediente | b=100,600 | b=300,150 | b=100,400 | b=400,100 | b=200,150 | b=50,400 | **χ² (6)** |
|---|---|---|---|---|---|---|---|
| φ_CAND (P=1/(1−ρ), eps=0) | +3,86% | +3,29% | +3,13% | +3,25% | +2,32% | +1,12% | **71,90** |
| + eps medido | +1,56% | +2,87% | +2,03% | +2,86% | +1,90% | +0,27% | 36,54 |
| + **nível medido** (simétrico) | −0,25% | −0,94% | +0,57% | −0,35% | −1,16% | −0,40% | **4,28** |
| + assimetria medida (P₀≠P₁) | +3,24% | +2,68% | −0,24% | −0,27% | −0,23% | −1,27% | 27,30 |

Três leituras, todas relevantes para as próximas frentes:

1. **A estrutura da fórmula-mestre está correta.** Com a elevação COMUM
   medida diretamente do mecanismo (não ajustada a φ) e o eps medido, a
   fórmula reproduz φ_mc nas seis células de estresse com χ² = 4,28 em 6
   graus de liberdade. O resíduo de φ_CAND vive inteiramente no **valor**
   de uma constante, não na forma funcional. Confirmado independentemente
   pelo estágio R (nas suas três células, o mesmo cálculo com o
   `lambda_bar` da SEGUNDA realização dá desvios +0,47%, −0,55%, +0,87%
   contra o φ_mc fresco de sementes 943).
2. **Introduzir a assimetria medida PIORA o ajuste** (χ² 4,28 → 27,30) —
   uma confirmação independente, no espaço de φ, do resultado primário de
   §4.
3. **Não existe forma fechada derivada para lambda_bar aqui.** O excesso
   lambda_bar/P_lead − 1 é +0,9% a +5,6% e parece crescer com b (≈+1% em
   b=50, ≈+2,0–2,6% em b=100, ≈+3,5–5,6% em b=200–400), mas a razão
   excesso/(b/n) não é constante (varia entre 7,7 e 16,8 nas seis
   células, sem padrão monotônico) e seis pontos com dispersão entre
   realizações independentes de ~2% não bastam para
   isolar uma lei. **Ajustar uma é exatamente o que o mandato desta linha
   proíbe apresentar como derivação, e não é feito aqui.** Fica registrado
   como o alvo mais bem localizado que esta linha já teve.

### 5.4 Controle: o resíduo é mesmo um efeito de M-CLUST?

Na validação fresca de 18 células (§5.2), φ_CAND fica ABAIXO da média MC
em **18 de 18 células**, incluindo as quatro com ρ ≤ 0,015, onde φ_CAND é
numericamente indistinguível de φ_U(c). Isso levantou a suspeita de que
parte do que as ondas 7–9 chamam de "resíduo de M-CLUST" seja o erro
finito-n da própria fórmula-mestre herdada — a aproximação que
`DERIVATIONS.md` §6 item 1 sempre listou como "empiricamente controlada,
não plenamente rigorosa".

`mu_baseline_control.py` (`SeedSequence(20260822944)`) testa isso no
membro mais simples da família: M-CLUST(1) ≡ M-U (b=1 ⟹ um bloco é uma
única semente, R é exatamente o conjunto de sementes, sem estrutura de
cluster nem sombreamento; ρ = c/n; φ_CAND = φ_U(c) a menos de 1e-6).
Dez células, c ∈ {10,50,150,400} × n ∈ {16384, 65536} mais duas em
n=262144: **χ²(φ_U vs MC) = 6,77 em 10 células** — perfeitamente
consistente. `mu_baseline_precision.py` (`SeedSequence(20260822945)`)
gasta as réplicas em precisão em vez de largura, em c=50:

| n | n_rep | desvio de φ_U | z |
|---|---|---|---|
| 4 096 | 200 000 | **+0,385% ± 0,117%** | +3,28 |
| 16 384 | 100 000 | +0,071% ± 0,165% | +0,43 |
| 65 536 | 40 000 | −0,120% ± 0,328% | −0,46 |

O viés finito-n da fórmula-mestre em b=1 existe, é positivo, e escala como
O(1/n): +0,39% em n=4096 cai para ≈+0,1% em n=16384 (previsão 1/n:
+0,096%) e para ≈+0,02% em n=65536. **Em n=65536 ele é duas ordens de
grandeza menor que o resíduo de M-CLUST.** A suspeita levantada acima
está, portanto, REFUTADA pelo próprio controle: o resíduo é genuinamente
um efeito de b>1 (estrutura de cluster), e a fórmula-mestre não é a
culpada — o que também estreita, e não alarga, o espaço de busca das
próximas frentes.

*(Precisão sobre o que este controle NÃO estabelece: o próprio deslocamento
de +0,5% a +1,0% nas células de ρ≤0,015 da grade M-CLUST é, por célula,
menor que 1,4σ, e agrupado sobre as quatro chega a ≈1,9σ — o sinal
positivo em 18 de 18 células é o que chama atenção, não a magnitude
individual. O controle mostra que, seja o que for esse deslocamento, ele
não vem da fórmula-mestre em si; não estabelece que ele exista como
efeito separado do resíduo que cresce com ρ.)*

### 5.5 Um canal terminal que o formalismo não modela

O simulador contabiliza separadamente os fechamentos-π normais que caem em
um ponto visitado que **não é arc start** — pontos de R visitados durante
uma cadeia, cujo predecessor-π nunca foi consumido por um passo normal.
Eles são 0,15%–0,70% de todos os eventos terminais (maiores justamente
onde b·c/n é maior: 0,70% em b=100/c=600, 0,57% em b=50/c=400). São
mortes reais que nem q_CLUST(s) nem o hazard de fechamento representam.
Efeito no mesmo sentido de reduzir φ, e portanto **contrário** ao resíduo
observado — registrado por completude, não como explicação.

---

## 6. Honestidade — o que ficou estabelecido, o que é heurístico, o que continua aberto

**Estabelecido (medido diretamente, sementes novas, com replicação):**

1. A hipótese nomeada em DISC-DEC-039 está refutada: x₀ **não** carrega
   elevação sistematicamente diferente da dos arc starts criados por
   reroteamento, nem no agregado (razão agrupada 0,983±0,007 sobre 9
   medições, sinal oposto ao que ajudaria), nem no perfil em s, nem na
   comparação casada por papel no passeio (§4.4). Uma vez medido o nível
   comum da elevação, o φ verdadeiro **exige** simetria a ±1,6% (§4.2).
2. A única célula que dava −3,7σ não replicou com semente independente; a
   dispersão entre realizações é ~1,8× maior que os sems de bootstrap de
   cluster, o que também recalibra para baixo a confiança que se deve dar
   a resultados de célula única deste tipo de medição — inclusive aos das
   frentes anteriores.
3. eps = P(cíclico | x₀ ∈ R) não é zero: 4,2e-4 a 1,2e-3, ou 0,36%–2,19%
   de φ, a 12,5–21,7σ. A suposição eps=0 de φ_CAND/φ_CAND5/φ_GLOBAL está
   errada, embora por pouco.
4. A **estrutura** da fórmula-mestre com elevação multiplicativa está
   correta: com a elevação comum e o eps medidos diretamente do mecanismo,
   ela reproduz φ_mc nas seis células de estresse com χ² = 4,28 em 6 g.l.
   O resíduo de φ_CAND vive no VALOR da elevação, não na forma.
5. O erro finito-n da fórmula-mestre herdada, isolado em M-U (b=1), é
   O(1/n) e vale ≈0,02% em n=65536 — não é a fonte do resíduo.

**Heurístico / derivado a ordem líder, rotulado (não provado):**

1. φ_EPS (§5.2). Os dois canais de eps são derivados a ordem líder, não
   provados; o passo "a probabilidade de retorno para um x₀ ∈ R run-start
   é o mesmo φ_cond" é explicitamente aproximado; o canal sorteio-f usa
   E[#sorteios] calculado pelo próprio modelo. A validação com sementes
   novas é real (χ² 121,7→72,0 em 18 células) e reproduzida em mais três
   grades já gravadas, mas **uma alegação positiva nesta linha exige
   verificação adversarial independente antes de catalogar**, e esta
   frente não a faz nem a declara feita.
2. A comparação casada de §4.4 usa "profundidade zero no arco atual" como
   proxy do papel estrutural; é o casamento mais próximo que consegui
   montar, não uma equivalência provada.

**Aberto (nomeado, não perseguido aqui):**

1. **A forma fechada da elevação.** O nível medido excede 1/(1−ρ) por
   +0,9% a +5,6%, crescendo grosso modo com b, e é *isto* — não a
   assimetria, não a exclusão global (onda 9 frente anterior), não a
   agregação (onda 8) — que carrega praticamente todo o resíduo restante
   de φ_CAND. Nem 1/(1−ρ) (φ_CAND) nem (1−c/n)^{-(b-1)} (φ_CAND5, que é
   ainda MENOR) o alcançam. Note que este achado é compatível com o teste
   decisivo de `global_exclusion_attempt` §4 (que mostrou que a elevação
   medida *com x₀ uniforme* ficava ABAIXO do necessário em 2 de 4
   células): condicionar em x₀ ∉ R — refinação metodológica desta frente,
   §2.2 item 1 — remove um viés para baixo naquela medição.
2. Por que a dispersão entre realizações independentes da mesma célula é
   ~1,8× o sem de bootstrap de cluster. Pode ser correlação residual
   entre passeios da mesma instância (25 por instância aqui) mal captada
   pelo bootstrap, ou uma cauda pesada na distribuição por instância.
   Não investigado.
3. O canal terminal de §5.5 (0,15%–0,70% dos eventos), não representado
   em nenhuma peça da fórmula-mestre.
4. A aproximação de Poissonização/independência da fórmula-mestre
   permanece intocada, como em todas as frentes anteriores desta linha —
   embora §5.4 agora limite sua contribuição, em b=1 e n=65536, a ≈0,02%.

---

## 7. Veredito

> **REFUTAÇÃO HONESTA da hipótese mandatada, com o resíduo relocalizado
> com precisão inédita.** A assimetria x₀-vs-outros-arc-starts nomeada por
> DISC-DEC-039 foi formalizada como um modelo de duas elevações (P₀ na
> base do relógio de x₀, P₁ dentro da integral de H — derivação própria,
> que reproduz φ_CAND e φ_CAND5 a 4e-5 no caso simétrico), o tamanho da
> assimetria NECESSÁRIA foi calculado ANTES de medir (+2,5% a +4,0% nas
> células de ρ≥0,37, onde o resíduo vive), e a assimetria foi então medida diretamente, com um
> estimador de Horvitz–Thompson separado por identidade do alvo, em seis
> células de estresse, 1,46 milhão de passeios (mais 0,76 milhão na
> replicação), com dois refinamentos
> metodológicos sobre a medição do predecessor (x₀ condicionado a ∉R;
> eventos terminais separados por mecanismo). **Nenhuma célula mostra a
> assimetria positiva necessária; a razão agrupada sobre nove medições é
> 0,983±0,007 — do sinal ERRADO, e distante 4 a 6 pontos percentuais do
> que seria preciso — e a única célula que dava −3,7σ não replicou com
> semente independente.
> Mais decisivamente: uma vez medido o NÍVEL comum da elevação, o φ
> verdadeiro exige que x₀ e os demais arc starts carreguem a mesma
> elevação a ±1,6%.** O formalismo estava correto neste ponto.
>
> O mesmo levantamento produziu três resultados secundários, todos
> rotulados como tais: (i) eps = P(cíclico | x₀ ∈ R), que φ_CAND/φ_CAND5/
> φ_GLOBAL põem em zero, é 0,36%–2,19% de φ a 12,5–21,7σ, e admite uma
> derivação de ordem líder que dá a fórmula candidata φ_EPS, sem parâmetro
> livre, reduzindo χ² de 121,7 para 72,0 em 18 células com sementes novas
> (e melhorando nas outras três grades já gravadas) — **alegação positiva,
> que exige verificação adversarial obrigatória antes de qualquer
> catalogação, e que esta frente NÃO declara integrada**; (ii) com a
> elevação comum e o eps MEDIDOS, a fórmula-mestre reproduz φ_mc nas seis
> células de estresse com χ² = 4,28/6 — a estrutura está certa, o resíduo
> inteiro vive no VALOR de uma constante, que excede 1/(1−ρ) por +0,9% a
> +5,6% crescendo com b, e para a qual nenhuma forma fechada derivada foi
> encontrada (nem ajustada, por disciplina); (iii) um controle dedicado em
> M-U (b=1) mostra que o erro finito-n da própria fórmula-mestre é O(1/n)
> e vale ≈0,02% em n=65536, refutando — pelo meu próprio controle — a
> suspeita, levantada nesta frente, de que parte do resíduo não fosse um
> efeito de M-CLUST.
>
> φ_CAND permanece a fórmula de registro de M-CLUST(b); esta frente não a
> substitui. A classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ (∀ b fixo)
> permanece completamente intocada por tudo acima.

---

## 8. Scorecard

| item | status | evidência |
|---|---|---|
| Hipótese mandatada (assimetria x₀ vs. outros) | **REFUTADA** | razão agrupada 0,9828±0,0073 sobre 9 medições, sinal oposto; razão EXIGIDA ∈ [0,984; 1,007] (§4.1–4.3) |
| Assimetria dependente de profundidade/papel | não detectada | §4.4, todas as diferenças casadas <1,5σ |
| Assimetria dependente de s | não detectada | §4.4, 8 faixas de massa, estágio R |
| Simulador novo validado | sim | 12 comparações contra 2 predecessores, \|z\|≤0,93 (§3) |
| Replicação independente do resultado primário | feita | estágio R, sementes 20260822942 (§4.3) |
| eps ≠ 0 | **ESTABELECIDO** | 12,5–21,7σ, 6 células (§5.1) |
| φ_EPS melhora φ_CAND | **SIM, com sementes novas** | χ² 121,7→72,0 (18 células, sementes 943); +3 grades gravadas (§5.2) |
| φ_EPS fecha o resíduo | **não** | χ²=72 contra ~18 esperado; falta o nível da elevação (§5.3) |
| Estrutura da fórmula-mestre | **validada** | χ²=4,28/6 com elevação e eps medidos (§5.3) |
| Forma fechada para o nível da elevação | **NÃO ENCONTRADA** | §5.3 item 3 — deliberadamente não ajustada |
| Erro finito-n da fórmula-mestre é a fonte? | **NÃO** | controle M-U: O(1/n), ≈0,02% em n=65536 (§5.4) |
| Arquivos fora desta subpasta modificados | nenhum | `git status`: apenas `x0_asymmetry_attempt/` (não rastreado) |
| Commit git criado | nenhum | — |

---

## 9. Arquivos (todos nesta subpasta, `x0_asymmetry_attempt/`)

- `ATTEMPT.md` — este documento.
- `PROGRESS.log` — checkpoints de progresso (não é o relatório final).
- `x0_asym_formula.py` — a fórmula-mestre de DUAS elevações (§2.1),
  escrita ANTES de qualquer medição nova; contém as checagens de sanidade
  e a bissecção `solve_P0_needed` usada em §2.3 e §4.2. Verificado:
  reproduz φ_CAND e φ_CAND5 gravados a <4e-5 relativo em 18 células.
- `x0_asymmetry_walk_measure.py` — simulador de passeio próprio com o
  estimador HT separado por identidade do alvo e bootstrap de cluster.
  Estágios A/B/U (sementes 20260822941) e R (replicação, 20260822942).
  - `x0_asymmetry_walk_measure_A.log` / `_A_results.json` — §4.1, §5.1.
  - `x0_asymmetry_walk_measure_B.log` / `_B_results.json` — §5.1 (eps).
  - `x0_asymmetry_walk_measure_U.log` / `_U_results.json` — §3 (checagem
    cruzada do simulador).
  - `x0_asymmetry_walk_measure_R.log` / `_R_results.json` — §4.3, §4.4
    (replicação independente + perfil em s). **É o resultado que impede
    esta frente de reportar como real a assimetria de −3,7σ da primeira
    realização.**
- `x0_asym_analysis.py` / `x0_asym_analysis.log` /
  `x0_asym_analysis_results.json` — análise determinística (sem simulação
  nova) das seções (1)–(8): checagem cruzada, probabilidade total, teste
  pré-registrado, teste decisivo, decomposição, agrupamento e
  homogeneidade, replicação, perfil em s. Reusa φ_mc já gravado pelos
  predecessores, sempre rotulado.
- `x0_asym_candidate.py` — a ÚNICA fórmula candidata desta frente
  (φ_EPS, §5.2), com a derivação de ordem líder de eps no cabeçalho e a
  triagem barata contra a grade já gravada.
- `x0_asym_validate.py` / `x0_asym_validate.log` /
  `x0_asym_validate_results.json` — validação fresca de 18 células,
  `SeedSequence(20260822943)`, com duas implementações independentes do
  conjunto cíclico conferidas entre si a cada 200ª instância e ambas
  contra força bruta (`python3 x0_asym_validate.py selftest`).
  **É o resultado que decide se φ_EPS supera φ_CAND — supera, sem
  fechar.**
- `mu_baseline_control.py` / `.log` / `_results.json` — controle M-U
  (b=1), 10 células, `SeedSequence(20260822944)` (§5.4).
- `mu_baseline_precision.py` / `.log` / `_results.json` — braço de alta
  precisão do controle, escala em n, `SeedSequence(20260822945)` (§5.4).
  **É o resultado que refuta a suspeita levantada por esta própria frente
  de que o resíduo não fosse um efeito de M-CLUST.**
