# Pré-registro: variância do número de zeros de zeta — GUE ingênuo (Modelo A) vs correção de primos de Berry (Modelo B)

**Status:** LOCKED
**Data de lock:** 2026-08-22
**Autor (agente/sessão):** Tamesis Discovery Lab, onda 4, frente
`DISC-RH-NUMBER-VARIANCE-001` (Claude Code)
**Linha:** `DISC-RH-REAL-001`. **Governança:** `DISC-DEC-019`
(última entrada de `00_GOVERNANCE/DECISION_LEDGER.yaml`).
**Evidence level alvo:** teste pré-registrado (não exploratório) — mas ver
Seção 8: NENHUM resultado deste teste constitui alegação sobre RH.

> Escrito e travado DEPOIS de três validações sintéticas (Seção 6) e ANTES
> de qualquer cômputo de `V(L)` sobre os dados reais de `zeros1.txt` ou
> `zeros3.txt`. Os únicos números tocados nos dados reais antes deste lock
> foram METADADOS deterministicos e públicos (T, log T, faixa de `x`
> renormalizado — `design_explore.py` / `design_metadata.json`), usados só
> para dimensionar a grade de `L` e a contagem de blocos, na mesma
> disciplina do `phase0_timing.py` do FHK (`DISC-RH-FHK-SHORT-INTERVAL-MAX-001`,
> lido nesta sessão como modelo de rigor). Nenhum valor de `V(L)` real foi
> computado antes deste lock.

## 0. Por que este teste existe

`DISC-DEC-019` autorizou o pré-registro completo do item 12 do
levantamento original de `DISC-RH-REAL-001` (variância do número / rigidez
GUE), depois que um piloto exploratório não pré-registrado
(`../untried_items_review/REVIEW.md` + `item12_number_variance_pilot.py`,
rotulado `exploratory_only`, ~22s, execução única) mostrou sinal
qualitativo — a variância empírica do número achata/satura em `L` grande
em vez de crescer como o Modelo A ingênuo prevê, em três regimes de altura
independentes (`zeros1`, `zeros3`, `zeros4`). O piloto tinha limitações
honestamente catalogadas: estimador ad hoc (janela deslizante com passo
`L/4`), sem critério de decisão travado a priori, Modelo B truncado
(estimativa heurística de fração capturada) para `zeros3`/`zeros4`. Este
pré-registro substitui o estimador, define os dois modelos com fórmulas
verificadas por fetch direto da fonte primária (não de memória), valida o
pipeline contra ground truth sintético (GUE + processos de referência)
ANTES de tocar dado real, e trava a regra de decisão antes de qualquer
cômputo substantivo.

## 1. Hipóteses exatas — dois modelos concorrentes nomeados

Fonte primária: Lugar, Milinovich & Quesada-Herrera, *"On the number
variance of zeta zeros and a conjecture of Berry"*, arXiv:2211.14918v1
(27 nov 2022) — **verificado por fetch direto do PDF nesta sessão**
(páginas 1–10, não citado de memória). Formula original: M. V. Berry,
*"Semiclassical formula for the number variance of the Riemann zeros"*,
Nonlinearity 1 (1988), 399–407 (existência e título confirmados por
`WebSearch` nesta sessão).

### 1.1 Definições (idênticas às da fonte, §1.4 do paper)

- Termo principal de Riemann–von Mangoldt: `N(E) := E/(2π)·(log(E/2π)−1) + 7/8`
  (eq. 1.1 do paper, via Titchmarsh cap. 9). Zeros renormalizados:
  `x_m := N(γ_m)`, espaçamento médio exatamente 1.
- `n(L;y)` := número de `x_m` renormalizados no intervalo `[y−L/2, y+L/2]`.
- **Variância do número, definição EXATA (não a janela deslizante ad hoc
  do piloto):**
  `V(L;x) := (1/Δx) · ∫_{x−Δx/2}^{x+Δx/2} [n(L;y) − L]² dy`
  (parágrafo imediatamente antes da Conjectura 1.4.1 do paper).

### 1.2 Modelo A — GUE ingênuo (regime universal aplicado fora de seu domínio)

Conjectura 1.4.1(a) de Berry (1988), citada verbatim no paper (eq. 1.19):
para `δ = o(log T)`,

```
V(L;x) ~ (1/π²)·[log(2πL) − Ci(2πL) − 2πL·Si(2πL) + π²L − cos(2πL) + 1 + γ₀]
```

com `Si`, `Ci` as integrais seno/cosseno padrão e `γ₀` a constante de
Euler–Mascheroni. **O próprio paper afirma que esta fórmula coincide
EXATAMENTE com a variância de autovalores GUE** (não apenas a aproxima).
Modelo A = esta fórmula fechada, avaliada em **qualquer** `L`, inclusive
fora do regime universal `L = o(log T)` — a hipótese ingênua "a rigidez
GUE de curto alcance vale em qualquer escala". Assintoticamente, para
`L→∞`, esta expressão cresce como `(1/π²)[log(2πL) + 1 + γ₀]` — log-lento
mas **ilimitado**.

### 1.3 Modelo B — correção de primos de Berry (regime não-universal)

Conjectura 1.4.1(b) de Berry (1988): para `δ ≫ log T`,

```
V(L;x) ~ (1/π²)·[ Σ_{n≤T} (Λ(n)²/(n·log²n))·(1 − cos(2πL·log(n)/log T)) + 1 ]
```

soma sobre potências de primos `n = p^k` (`Λ(n) = log p` se `n=p^k`, 0
caso contrário). **Identidade algébrica usada** (derivada e verificada
nesta sessão): `Λ(p^k)²/(p^k·log²(p^k)) = 1/(k²·p^k)`, simplificando a
soma para `Σ_{p^k≤T} (1/(k²p^k))·(1−cos(2πLk·log p/log T))`.

**Status de prova:** Corolário 1.4.3 do paper (assumindo RH + Conjectura
1.4.2 de Chan 2004 sobre gaps de zeros em alcances longos) prova a
Conjectura 1.4.1 completa (ambos os regimes) para `δ = o(log^{4/3}T)`. Além
desse alcance, a parte (b) permanece a conjectura ORIGINAL de Berry (o
próprio paper nota: *"Berry never conjectures the range of δ for which
part (b) holds... conceivably part (b) continues to hold in a much longer
range"*). **Este teste avalia a conjectura de Berry como formulada (sem
limite superior declarado por Berry para a parte b)** — a Seção 4 marca
explicitamente quais pontos da grade de `L` caem dentro da janela
PROVADA (`L ≤ log^{4/3}T`) vs além dela (testando a extensão ainda
conjectural). Isto é o alinhamento correto com `DISC-DEC-019`, que cita a
prova condicional como APOIO à formulação de Berry, não como o objeto
exato sendo testado.

## 2. Estimador exato (substituindo o ad hoc do piloto)

`n(L;y)` é uma função em escada de `y`, com saltos exatamente em
`y = x_m − L/2` (+1, ponto entra) e `y = x_m + L/2` (−1, ponto sai). A
integral `∫[n(L;y)−L]² dy` sobre qualquer intervalo é computada
**exatamente** (sem discretização) somando `(valor)² × largura` sobre os
trechos entre pontos de quebra consecutivos — implementado em
`estimator.py::_exact_window_integral`.

**Estimador em blocos** (`estimator.py::block_number_variance`,
implementa literalmente a definição de `V(L;x)` da Seção 1.1 com
`Δx` = largura do bloco, `x` = centro do bloco): o range observado de
cada dataset é particionado em `B` blocos de largura uniforme
(`np.linspace(x_min, x_max, B+1)` — determinístico, sem seed). Dentro de
cada bloco `[a,b]`, a janela `y` varia apenas na sub-região INTERIOR
`[a+L/2, b−L/2]` (evita efeito de borda — nunca inventa dado fora do
observado). Blocos com largura `< 3L` são descartados. `V̂(L)` = média
sobre blocos; `SE(L)` = desvio padrão entre blocos / `√B`.

## 3. Datasets e holdout selado

| Dataset | Papel | n zeros | T (altura) | log T |
|---|---|---|---|---|
| `zeros1.txt` | **primário** | 100.000 | 74.920,83 | 11,2242 |
| `zeros3.txt` | **primário** | 10.000 (perto de #10¹²) | 267.653.395.647 | 26,3130 |
| `zeros4.txt` | **HOLDOUT SELADO** | 10.000 (perto de #10²¹) | 1,4418×10²⁰ | 46,4176 |

`zeros4.txt` é o dataset de **maior altura** disponível — reservado como
holdout selado, mesmo precedente de `zeros3` (T=10¹¹) em
`DISC-RH-FHK-SHORT-INTERVAL-MAX-001` (`../fhk_short_interval_max/PREREGISTRATION.md`
Seção 7) e de SPARC-003 em `COSMOLOGY_WIDE_BINARIES`. **Nenhum `V(L)` de
`zeros4.txt` é computado por esta frente.** Reservado para o Gate de
Replicação, caso o veredito primário favoreça algum modelo (Seção 8).

### Renormalização

- `zeros1`: fórmula ABSOLUTA `x = N(γ)` (γ ≤ 75.000, seguro em float64,
  sem cancelamento catastrófico).
- `zeros3` (e `zeros4`, reservado): linearização LOCAL
  `x = offset · N'(base)`, `N'(E) = (1/2π)·log(E/2π)` — evita o problema
  de cancelamento catastrófico documentado em `../data/PROVENANCE.md`
  (base com 12–21 dígitos, não subtraível com segurança em float64). Erro
  de 2ª ordem **derivado e quantificado nesta sessão** (Taylor de `N` em
  torno de `base`, usando `N''(E)=1/(2πE)`):
  `err₂ = offset_max² / (4π·base)`. Para `zeros3`: `err₂ = 1,96×10⁻⁶`
  (desprezível frente à escala de `V(L)`, `O(0,1)–O(1)`) —
  ver `design_metadata.json`.

## 4. Grade de `L` declarada e pontos decisivos primários

Grade mecânica, multiplicativa em `log T` (idêntica em forma para os dois
datasets, para comparabilidade): `L = mult · log T`,
`mult ∈ {1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256}`.
Contagem de blocos: `B(L) = ⌊x_range / (4·L)⌋` (fator 4 — 3 unidades de
largura interior por bloco, mínimo declarado). Um ponto da grade só é
**usável** se `B(L) ≥ 10`. Tudo isto é computado a partir de metadados
determinísticos (`T`, `log T`, `x_range`), NUNCA de `V(L)` — travado em
`DESIGN.json` (gerado por `lock_design.py`, executado uma única vez antes
deste documento).

**Ponto decisivo primário por dataset = maior `L` usável na grade**
(máxima separação Modelo A/Modelo B, escolha mecânica, não ajustada após
ver resultado):

| Dataset | `L` primário | mult | `B` (blocos) | Dentro da janela provada (Cor. 1.4.3, `L≤log^{4/3}T`)? |
|---|---|---|---|---|
| `zeros1` | **2155,044** | 192× log T | 11 | Não (log^{4/3}T=25,13) — testa a conjectura original de Berry além do alcance hoje provado |
| `zeros3` | **210,504** | 8× log T | 11 | Não (log^{4/3}T=78,26) — idem |

**Ponto secundário/descritivo** (não decide, mais blocos, robustez):
`zeros1` `L=1436,70` (mult=128, B=17); `zeros3` `L=157,88` (mult=6, B=15).
A curva completa da grade (todos os `mult` usáveis) é reportada como
**descritiva** (não decisória) — ver Seção 7.

Nota honesta: os DOIS pontos decisivos primários caem **fora** da janela
hoje rigorosamente provada por Corolário 1.4.3 (`L ≤ log^{4/3}T ≈ 25,1` e
`≈78,3` respectivamente) — escolhidos assim porque é exatamente onde a
separação Modelo A/Modelo B é maior (maior poder), consistente com o sinal
visto no piloto exploratório em `L` da mesma ordem (100–3000). Um
veredito `BERRY_FAVORED` aqui é evidência sobre a conjectura de Berry
1988 **tal como formulada por Berry** (sem limite superior declarado para
a parte b), não uma confirmação do teorema condicional da Seção 1.3 —
distinção mantida explicitamente em qualquer leitura do resultado
(Seção 8).

## 5. Modelo B: exato (`zeros1`) vs cota rigorosa (`zeros3`)

- **`zeros1`** (T≈74.920,8): TODAS as potências de primos `p^k ≤ T` são
  enumeráveis (crivo de Eratóstenes, 7.486 potências de primos) — Modelo
  B é **exato**, sem truncagem.
- **`zeros3`** (T≈2,68×10¹¹): enumerar todos os primos até T é inviável.
  Em vez da heurística "fração estimada capturada" do piloto (limitação
  #4 do `REVIEW.md`), usa-se aqui uma **cota bilateral rigorosa**:
  - Termo `p^k ≤ P_cutoff = 2×10⁸` (11.078.937 primos, crivo vetorizado,
    ~6s): computado **exatamente**.
  - Cauda `k=1`, `P_cutoff < p ≤ T`: `0 ≤ Σ 1/p ≤ 2·[cota superior]`, via
    o teorema clássico de Mertens (F. Mertens, *"Ein Beitrag zur
    analytischen Zahlentheorie"*, J. Reine Angew. Math. 78 (1874), 46–62):
    `|Σ_{p≤x} 1/p − loglog(x) − M| ≤ 4/log(x+1) + 2/(x·log x)` para todo
    `x≥2` (`M`=constante de Meissel–Mertens=0,261497...) — **verificado
    por fetch em `en.wikipedia.org/wiki/Mertens'_theorems` nesta sessão**
    (a tentativa de verificar a cota mais justa, porém mais moderna, de
    Rosser–Schoenfeld 1962 falhou por HTTP 503 no fetch direto do PDF —
    por isso NÃO usada, preferindo a cota mais fraca mas confirmada).
  - Cauda `k≥2` além de `P_cutoff`: cota autocontida e derivada nesta
    sessão (série geométrica + majoração por soma telescópica sobre
    inteiros): `≤ 1/P_cutoff` (≈5×10⁻⁹, desprezível).
  - Resultado: **intervalo** `[V_B_lower(L), V_B_upper(L)]`, largura
    numericamente verificada `≈0,1296` em toda a grade de `L` usada
    (constante porque a cota independe de `L` — só depende de `P_cutoff`
    e `T`) — ver `estimator.py::model_B_bounded` e checagem em
    `design_explore.py`/testes desta sessão.
  - **Uso conservador na regra de decisão**: `V̂` é comparado à borda MAIS
    PRÓXIMA do intervalo (distância 0 se `V̂` está dentro) — torna
    estritamente MAIS DIFÍCIL rejeitar o Modelo B por causa da incerteza
    de truncagem, nunca mais fácil.

## 6. Validações pré-lock (todas PASSARAM; logs e falhas preservados)

Duas falhas REAIS de implementação foram encontradas e corrigidas durante
a validação — documentadas aqui sem maquiagem, exatamente a disciplina
que a validação existe para cumprir:

- **Bug 1 (normalização GUE):** a primeira tentativa de gerar matrizes
  GUE sintéticas (`validate_gue.py`) simetrizava uma matriz complexa
  independente (`H=(A+A^†)/2`), que **reduz a variância efetiva por um
  fator 2** frente à convenção padrão — a borda do espectro empírica saiu
  30% menor que o raio teórico do semicírculo (`70,48` vs `100,00`
  esperado). Corrigido gerando as entradas com a variância-alvo
  diretamente (sem simetrizar uma amostra independente) — borda empírica
  passou a `99,74` vs `100,00` teórico (razão 0,9974). Log preservado:
  `validation_gue_run1_FAILED.log` (+ `_run2_FAILED.log`, 2ª tentativa
  com a normalização corrigida mas antes do Bug 2 abaixo).
- **Bug 2 (estimador exato, `_exact_window_integral`):** o valor inicial
  `n₀` da integral em escada era computado com uma convenção de fronteira
  inconsistente (`side="left"` no limite inferior), que **deixava de
  processar um evento de saída exatamente coincidente com `y_lo`**,
  inflando `n(L;y)` em +1 permanentemente a partir daí. Detectado
  comparando o estimador contra três ground truths independentes: rede
  regular (variância deveria ser ~0, saiu 1,0 antes da correção, 0,0
  depois), processo de Poisson (`V(L)=L` exato), e comparação direta por
  força bruta em grade fina contra os autovalores GUE sintéticos (exato
  batia com força bruta a <0,02% em TODA a grade de `L` de 1 a 2155,
  incluindo os `L` primários reais desta análise, depois da correção).
  Corrigido trocando o lado da busca binária no limite inferior de
  `n₀` para manter a mesma convenção de fronteira usada no resto da
  função. Um problema de PERFORMANCE relacionado (o método varria o
  array inteiro por bloco, custando `O(N·B)`) também foi corrigido
  (fatiamento local por bloco) — sem isso a análise primária com `B`
  grande em `L` pequeno não caberia no orçamento de tempo.

Validações finais (pós-correção):

- **(a) Recuperação de GUE** (`validate_gue.py`, seed 20260822·01, N=2500,
  25 réplicas, convenção padrão de Mehta verificada numericamente —
  borda empírica/teórica = 0,9974): `|z| < 3` confirmado em `L` seguro
  (`L∈{5,10,20}`, `L`/bulk ≤1,3%) — z ∈ [−1,00, −0,40]. Em `L` maior
  (40–320, `L`/bulk 2,7–21,3%) há desvio sistemático do Modelo A
  (`z`≈+3,1 a +3,6) — **efeito conhecido de N finito da matriz sintética**
  (não do estimador — confirmado por (b) abaixo), reportado como
  descritivo, não decisivo para o lock. `validation_gue.{json,log}`.
- **(b) Correção da implementação** (`validate_estimator_bruteforce.py`,
  seed 20260822·02): Parte 1 — `block_number_variance` (o MESMO código
  usado na análise primária) recupera `V(L)=L` de um processo de Poisson
  em TODA a grade real (`L`=1 a 2155), `|z|<1,51` em todos os 13 pontos.
  Parte 2 — integral exata vs integração numérica independente em grade
  local com resolução `L/2000` (1ª tentativa com grade fixa global falhou
  por subamostragem em `L` pequeno — `validation_estimator_bruteforce_run1_FAILED.{json,log}`,
  não um bug do método exato): diferença relativa máxima `0,00025` (0,025%)
  em 10 valores de `L` de 1 a 2155. `validation_estimator_bruteforce.{json,log}`.
- **(c) Poder de discriminação** (`validate_power_saturating.py`, seed
  20260822·03): substituto DECLARADO (rede jitterizada,
  `x_m=m+ε_m`, `ε_m~U(−0,45,0,45)`) com a MESMA assinatura qualitativa
  que distingue os modelos (variância saturada/limitada, não log-crescente)
  — não uma simulação literal da fórmula de Berry (ver docstring do
  script para a justificativa completa dessa escolha). No desenho REAL
  (mesmo `M`, mesmo `B(L)`, mesmo `L` primário de cada dataset), 10/10
  réplicas rejeitam o Modelo A a `|z|≥3` em ambos os cenários
  (`zeros1_scale`: `z`∈[−2379,−8,0]; `zeros3_scale`: `z`∈[−401,−5,2]) —
  poder projetado 100% (limiar declarado de aceite: ≥80%). Nota honesta:
  os valores de `z` mostram um padrão bimodal entre réplicas (~−8 vs
  ~−1000+) cuja causa exata não foi diagnosticada — não afeta a conclusão
  qualitativa (ambos os subgrupos rejeitam o Modelo A por enorme margem),
  mas fica registrado como uma peculiaridade não resolvida do substituto
  sintético declarado, não do dado real. `validation_power_saturating.{json,log}`.

## 7. Regra de decisão TERNÁRIA (travada)

Para cada dataset `d ∈ {zeros1, zeros3}`, no `L` primário da Seção 4:
`z_A(d) = (V̂(d) − modelo_A(L_d)) / SE(d)`;
`z_B(d) = (V̂(d) − alvo_B(d)) / SE(d)`, onde `alvo_B` = valor exato
(`zeros1`) ou a borda MAIS PRÓXIMA do intervalo `[lower,upper]`
(`zeros3`; `z_B=0` se `V̂` está dentro do intervalo).

- **BERRY_FAVORED** ⟺ `|z_A(zeros1)|≥3` **E** `|z_A(zeros3)|≥3` **E**
  `|z_B(zeros1)|<2` **E** `|z_B(zeros3)|<2` (GUE claramente rejeitado nos
  DOIS regimes de altura independentes; Berry não rejeitado em nenhum).
- **GUE_FAVORED** ⟺ `|z_B(zeros1)|≥3` **E** `|z_B(zeros3)|≥3` **E**
  `|z_A(zeros1)|<2` **E** `|z_A(zeros3)|<2` (simétrico).
- **INCONCLUSIVE**, caso contrário, com subcaso anotado:
  - `NEITHER_MODEL`: ambos os modelos rejeitados (`|z|≥3`) nos DOIS
    datasets — negativo informativo, catalogado com peso integral.
  - `UNDERPOWERED`: nenhum modelo claramente rejeitado (`|z|<3`) em pelo
    menos um dataset para pelo menos um modelo.
  - `PARTIAL_DISAGREEMENT`: os dois datasets apontam em direções
    diferentes (um favorece o padrão Berry, outro o padrão GUE) — a
    salvaguarda mais importante contra escolher só o dataset que "deu
    certo".

Não há busca sobre `L`, estimador, ou pesos além do que está travado
aqui. A grade COMPLETA (todos os `mult` usáveis por dataset) é reportada
como curva **descritiva** — mostra a forma de `V̂(L)` vs os dois modelos
em toda a faixa acessível, mas **não** entra na regra de decisão (mesmo
papel do χ² "descritor apenas" do FHK).

**Checagens de sanidade mecânicas (não alteram a regra):** S1 — `V̂` no
ponto secundário (mais blocos) deve ter o mesmo SINAL de desvio de
Modelo A que o ponto primário, em cada dataset (consistência interna,
não deveria inverter com poucos blocos a mais). S2 — comparação de
ordem de grandeza com os números do piloto exploratório em `L`
comparável (`REVIEW.md`, tabela da Seção "Resultado") — mero registro de
plausibilidade, o piloto usou um estimador ad hoc e não é ground truth.
Se S1 falhar: veredito retido (`INVALID_RUN`), investigado e documentado
antes de qualquer leitura do resultado.

## 8. Condições de parada e o que NÃO está sendo testado

- **Nenhuma alegação sobre RH** em nenhum desfecho — condição permanente
  da linha `DISC-RH-REAL-001`. O teste discrimina duas hipóteses
  estatísticas sobre a variância local do número de zeros em altura
  finita; os zeros usados (tabelas de Odlyzko) são computados sob a
  suposição de que estão na linha crítica — o teste não avalia essa
  suposição.
- **Distinção proved vs conjectural preservada**: um veredito
  `BERRY_FAVORED` nos `L` primários (Seção 4, ambos fora da janela do
  Corolário 1.4.3) é evidência sobre a conjectura ORIGINAL de Berry 1988,
  não uma "confirmação" do teorema condicional de Lugar–Milinovich–Quesada-Herrera
  2022 — que cobre um `L` menor. Isso será dito explicitamente em
  qualquer relato do resultado.
- **Sem reformulação pós-hoc**: resultado que sugerir estatística/estimador
  melhor vira proposta de um NOVO pré-registro; este arquivo recebe no
  máximo um adendo pré-análise datado, e o preenchimento da Seção 10
  depois da análise primária.
- **Qualquer veredito favorecendo um modelo (achado positivo) NÃO é
  reportado como real** até reprodução adversarial independente
  (implementação do zero a partir SOMENTE deste arquivo) — e o holdout
  `zeros4` permanece selado até esse gate. Flag para o orquestrador, sem
  abrir o holdout nesta sessão.
- Um `INCONCLUSIVE/NEITHER_MODEL` é catalogado com peso integral como
  resultado negativo informativo.
- Computação em primeiro plano (com uma única execução em segundo plano
  monitorada nesta sessão, terminada antes do lock, sem processos
  órfãos); nenhum dado real tocado antes deste lock.

## 9. Limitações declaradas (antes de ver o dado real)

1. **Poucos blocos nos pontos decisivos primários** (`B=11` em ambos os
   datasets) — SE(L) tem incerteza de amostragem substancial nessa
   contagem (grau de liberdade baixo para a variância entre blocos). O
   ponto secundário (mais blocos: 17 e 15) serve de checagem de robustez,
   mas não decide.
2. **`zeros3` tem grade mais rasa** (apenas 7 pontos usáveis vs 16 de
   `zeros1`) — dataset menor (10.000 zeros vs 100.000), regra `B≥10`
   idêntica aplicada a ambos exclui os `mult` maiores mecanicamente, não
   por escolha.
3. **Modelo B em `zeros3` é um intervalo, não um ponto** (largura
   `≈0,13`) — reduz o poder de rejeitar Modelo B especificamente nesse
   dataset (mitigado por usar a borda mais próxima, nunca o centro).
4. **Ambos os pontos decisivos primários estão fora da janela hoje
   provada** (Corolário 1.4.3) — testam a conjectura original de Berry,
   não o teorema condicional. Ver nota da Seção 4/8.
5. **Peculiaridade não resolvida no substituto sintético de poder**
   (Seção 6c, padrão bimodal de `z` entre réplicas) — não afeta a
   conclusão de poder (ambos os subgrupos rejeitam por larga margem), mas
   não foi diagnosticada a fundo, por orçamento de tempo.
6. **O piloto exploratório já viu o padrão qualitativo** (achatamento em
   `L` grande) nos mesmos três datasets — o desenho desta frente
   (escolha do `L` primário = maior `L` usável, onde a separação é maior)
   foi motivado por esse sinal prévio. Mitigação: estimador, grade e
   regra são inteiramente mecânicos/travados aqui, sem reajuste após ver
   `V̂` real; gate adversarial obrigatório para qualquer achado positivo
   (Seção 8).

## 10. Arquivos e seeds (todos travados neste commit)

| Papel | Arquivo | Seed |
|---|---|---|
| Estimador + modelos (biblioteca) | `estimator.py` | — |
| Metadados de desenho (determinístico) | `design_explore.py`, `design_metadata.json` | — |
| Desenho travado (grade, B(L), pontos primários) | `lock_design.py`, `DESIGN.json` | — |
| Validação (a) GUE | `validate_gue.py`, `validation_gue.{json,log}`, `validation_gue_run1_FAILED.log`, `validation_gue_run2_FAILED.{json,log}` | 20260822·01 |
| Validação (b) implementação | `validate_estimator_bruteforce.py`, `validation_estimator_bruteforce.{json,log}`, `_run1_FAILED.{json,log}` | 20260822·02 |
| Validação (c) poder | `validate_power_saturating.py`, `validation_power_saturating.{json,log}` | 20260822·03 |
| Análise primária | `run_primary.py`, `primary_result.json`, `primary_run.log` | — (determinístico, sem seed) |
| Holdout (SELADO) | — (não computado) | reservado, seed a definir pelo Gate |

---

*Adendo pré-análise permitido: no máximo um, datado, acima desta linha de
resultado. Abaixo: preenchido somente após a análise primária.*

## [Preenchido depois da análise] Resultado

**Data da análise:** 2026-08-22 (mesma sessão do lock; nenhuma alteração de
regra, grade, limiares ou modelos entre lock e análise). `run_primary.py`,
wall time 11,6s (crivo de primos + integração exata em todos os pontos
usáveis da grade de ambos os datasets — 16 pontos em `zeros1`, 7 em
`zeros3`).

**Pontos decisivos primários** (Seção 4, traváveis antes de ver `V(L)`):

| Dataset | `L` | `V̂(L)` | `SE` | Modelo A | `z_A` | Modelo B | `z_B` |
|---|---|---|---|---|---|---|---|
| `zeros1` | 2155,04 | 0,3600 | 0,0038 | 1,1237 | **−203,25** | 0,3049 (exato) | **+14,66** |
| `zeros3` | 210,50 | 0,5182 | 0,0895 | 0,8880 | **−4,13** | [0,4797; 0,6092] | **+0,00** |

**VEREDITO (regra ternária travada da Seção 7): `INCONCLUSIVE`, subcaso
`PARTIAL_DISAGREEMENT`** (rótulo mecânico exato produzido pela regra —
ver leitura honesta abaixo para o padrão real, mais sutil que "os
datasets discordam de direção"). Nenhum dos dois requisitos completos
(`BERRY_FAVORED` ou `GUE_FAVORED`) foi satisfeito: em `zeros3` o padrão
"Modelo A rejeitado, Modelo B não rejeitado" se cumpre integralmente
(`|z_A|=4,13≥3`, `|z_B|=0,00<2`); em `zeros1` o Modelo A é rejeitado por
margem enorme (`|z_A|=203,25`), mas o Modelo B TAMBÉM é tecnicamente
rejeitado pelo limiar de 2σ pré-declarado (`|z_B|=14,66≥2`), mesmo a
diferença absoluta `V̂−modelo_B` sendo pequena (`0,360−0,305=0,055`) —
porque `SE(zeros1)=0,0038` é extremamente pequeno (11 blocos com dispersão
interna muito baixa, ver diagnóstico abaixo). Isso impede o requisito
`|z_B(zeros1)|<2` da regra `BERRY_FAVORED`.

**Diagnóstico pós-hoc do `SE` pequeno em `zeros1`** (investigação honesta,
NÃO uma reformulação da regra — a regra e o veredito acima já estão
fixados): os 11 valores por bloco em `zeros1`/`L=2155,04` são
`[0,331; 0,3495; 0,3541; 0,3578; 0,361; 0,3684; 0,3603; 0,3679; 0,3772;
0,3617; 0,3713]` — dispersão interna genuinamente pequena, não um
artefato de implementação (confirmado por inspeção direta, não apenas
inferido). Removendo o bloco 1 (menor altura, γ∈[14,13; 9098,0], onde
`log T` local ≈9,116 vs `log T` global=11,224 usado uniformemente na
grade — heterogeneidade de altura dentro de `zeros1`, que cobre γ de 14 a
74.921, um fator >4700× em altura absoluta) o resultado muda pouco:
`V̂=0,3629`, `SE=0,0026`, `z_A=−288,8`, `z_B=+22,0` — mesmo padrão
qualitativo, GUE ainda mais rejeitado, Modelo B ainda tecnicamente
rejeitado pelo limiar de 2σ. **O ponto decisivo primário de `zeros1` é
robusto a esse efeito de borda especificamente** — a heterogeneidade de
altura é uma limitação de desenho real e documentada (Seção 9, item 4
abaixo), mas não é a causa do `SE` pequeno nem muda o veredito.

**Leitura honesta dentro da estrutura pré-declarada** (não altera o
veredito formal, mas contextualiza-o, mesmo papel da leitura honesta do
FHK): (i) o Modelo A (GUE ingênuo estendido) é excluído por margem
enorme e consistente nos DOIS regimes de altura independentes
(`z_A=−203,25` em `zeros1`; `z_A=−4,13` em `zeros3`) — o dado real está
muito mais achatado/limitado do que a extrapolação GUE ingênua prevê,
replicando o sinal qualitativo do piloto exploratório sob desenho
pré-registrado; (ii) o dado está MUITO mais próximo do Modelo B do que do
Modelo A em distância absoluta nos dois datasets (`zeros1`:
`|V̂−B|=0,055` vs `|V̂−A|=0,764`, 14× mais perto de Berry; `zeros3`: `V̂`
cai DENTRO do intervalo do Modelo B, fora do intervalo bem mais distante
do Modelo A); (iii) o Modelo B não é formalmente "aceito" em `zeros1`
apenas porque o `SE` medido ali é pequeno o bastante para que uma
diferença absoluta pequena cruze o limiar de 2σ pré-declarado — isto é
uma leitura de PODER ALTO (o desenho é sensível o bastante para detectar
desvios finos), não evidência de que o Modelo B esteja errado em
magnitude relevante. Nenhuma dessas leituras vira alegação de achado até
o gate adversarial (Seção 8) — e nenhuma delas é uma alegação sobre RH.

**Checagem de consistência com o piloto exploratório (S2, não decisiva):**
piloto (`../untried_items_review/REVIEW.md`) reportou `V_emp≈0,40–0,51`
para `zeros1` em `L=1000–3000` e `V_emp≈0,30–0,57` para `zeros3` em
`L=500–1500`, com estimador ad hoc. Este pré-registro obtém `V̂=0,360`
(`zeros1`, `L=2155`) e `V̂=0,518` (`zeros3`, `L=210,5`) — mesma ordem de
grandeza e mesmo padrão qualitativo (bem abaixo do Modelo A GUE), sem
contradição grosseira. Plausibilidade confirmada, não é ground truth.

**Sanidade:** S1 PASS nos dois datasets (sinal de `z_A` no ponto primário
bate com o sinal no ponto secundário — `zeros1`: negativo/negativo;
`zeros3`: negativo/negativo). Run `VALID`; veredito mantido.

**Curva completa da grade (descritiva, não decide):** em `zeros1`, `z_A`
é negativo (GUE rejeitado a ≥3σ) em TODOS os 16 pontos usáveis da grade,
incluindo pontos dentro da janela provada do Corolário 1.4.3
(`mult∈{1; 1,5; 2}`, `z_A∈[−341,6; −216,7]`) — o achatamento em relação a
GUE aparece mesmo dentro do regime hoje rigorosamente coberto, não só na
extensão conjectural. Em `zeros3`, mesmo padrão (`z_A` negativo em todos
os 7 pontos, `z_A∈[−130,0; −4,0]`). Quanto ao Modelo B, o padrão é MISTO
e não deve ser lido como "compatível na maior parte da grade": em
`zeros1`, `V̂` fica DENTRO/perto do intervalo aceito (`|z_B|<2`) em 6 dos
16 pontos (`mult∈{1,5; 32; 48; 64; 96; 128}`) e é tecnicamente rejeitado
(`|z_B|≥2`, geralmente por margem grande, `|z_B|` até 66) nos outros 10 —
sem um padrão monotônico óbvio em `L`; em `zeros3`, compatível em 6 dos 7
pontos, rejeitado só em `mult=4` (`z_B=−28,98`). Em distância absoluta, o Modelo B fica mais perto do `V̂` empírico do que
o Modelo A em **23 dos 23 pontos usáveis da grade combinada** (16/16 em
`zeros1`, 7/7 em `zeros3` — verificado ponto a ponto, não só nos dois
pontos primários), inclusive nos pontos onde é tecnicamente rejeitado
pelo limiar de 2σ. Isto é o padrão mais forte e mais uniforme de todo o
resultado — tabela completa em `primary_result.json`.

**Holdout `zeros4`: SELADO** — nenhum `V(L)` de `zeros4.txt` foi
computado por esta frente. Permanece reservado ao Gate de Replicação.

**Flag adversarial: SIM.** O veredito formal é `INCONCLUSIVE`, não abre o
holdout — mas contém um componente de exclusão muito forte e consistente
(GUE rejeitado a `|z|` de 4 a 203 em AMBOS os datasets independentes),
que pela condição de parada da Seção 8 (qualquer achado tipo p<0,05 exige
reprodução adversarial antes de ser reportado como real) fica retido como
CANDIDATO até reprodução adversarial independente (implementação do zero
a partir SOMENTE deste arquivo). Nenhuma alegação sobre RH em nenhuma
hipótese — o teste avalia exclusivamente a compatibilidade de duas
formas fechadas de `V(L)` com zeros reais de zeta em altura finita.

Resultado completo: `primary_result.json`; log: `primary_run.log`.

## [Correção pós-adversarial, 2026-08-22] Resultado corrigido

A reprodução adversarial obrigatória (`adversarial/ADVERSARIAL_VERDICT.md`)
encontrou um **terceiro bug real** em `estimator.py::block_number_variance`
(erro de arredondamento de ponto flutuante no round-trip
`(a+L/2)-L/2` ao recompor a borda inferior do bloco 0, afetando 15 dos 23
pontos usáveis da grade — ver descrição completa no arquivo adversarial).
Nos dois pontos decisivos primários, o arredondamento caiu do lado seguro
em `zeros1` (números batem exatamente, sem alteração) mas do lado ruim em
`zeros3` (`SE` inflado ~31×). O texto do "Resultado" acima é preservado
INTACTO como registro histórico do que foi computado antes desta
correção; os valores abaixo são os corretos e substituem os de `zeros3`
na leitura final:

| Dataset | `L` | `V̂(L)` | `SE` | Modelo A | `z_A` | Modelo B | `z_B` |
|---|---|---|---|---|---|---|---|
| `zeros1` | 2155,04 | 0,3600 | 0,0038 | 1,1237 | −203,25 (inalterado) | 0,3049 | +14,66 (inalterado) |
| `zeros3` | 210,50 | **0,4272** | **0,0029** | 0,8880 | **−160,76** | [0,4797;0,6092] | **−18,29** |

**Veredito corrigido pela mesma regra ternária travada da Seção 7 (regra
em si não mudou, só os números de entrada):** `zeros1`: `|z_A|≥3` e
`|z_B|≥3` → ambos rejeitados. `zeros3`: `|z_A|≥3` e `|z_B|≥3` → ambos
rejeitados. **Subcaso correto = `NEITHER_MODEL`, não `PARTIAL_DISAGREEMENT`.**
O veredito de topo permanece `INCONCLUSIVE` — não muda.

O componente **GUE-EXCLUSION fica CONFIRMADO por reprodução adversarial
independente, e mais forte do que o relatório original sugeria**: GUE é
rejeitado por margem enorme nos dois regimes de altura independentes
(`z_A=-203,25` e `z_A=-160,76`, não `-4,13`), e o dado permanece
consistentemente mais próximo do Modelo B do que do Modelo A em
distância absoluta nos 23/23 pontos da grade (`zeros3` corrigido: ~9×
mais perto de Berry que de GUE). O holdout `zeros4` **não** é aberto —
a condição de parada da Seção 8 é sobre achados que favorecem
formalmente um modelo, e isso continua não sendo o caso.

`estimator.py` requer a correção do round-trip antes de qualquer
reanálise futura que reuse este código (ver `adversarial/bug_report_block0_fp.py`
para a correção mínima e prova de conceito). O código original,
com o bug, é preservado intacto para registro histórico.

