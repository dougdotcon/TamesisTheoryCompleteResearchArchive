# Nota de metodologia — frente `knot-quark-mass` (DISC-CORE-NUMERICS-001)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo de
ajuste contra dados de referência. Mesma disciplina de
`05_DISCOVERY_LAB/02_TESTS/TRI_RG/*/METHODOLOGY_NOTE.md`.

**Data:** 2026-08-21.
**Autoridade:** DISC-DEC-013 (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`,
última entrada), item (3) da lista de adjudicações de mesa.

## Alegação sob teste (fonte primária, localizada antes desta nota)

`M ∝ exp(α · L/D)`, onde `L/D` é o comprimento de corda ideal
(*ropelength* em unidades de diâmetro) de um nó primo atribuído a cada
geração de quarks, com `R² > 0,99` alegado para o setor up.

Fontes primárias no arquivo (file:line):

- **Código do ajuste:**
  `01_TAMESIS_CORE/02_Experimental_Validation/Particle_Physics/quarks/simulation/knot_mass_fit.py`
  - linhas 10–13: mapeamento Gen1(u/d)→Trefoil 3_1, Gen2(c/s)→Figure-8 4_1,
    Gen3(t/b)→Cinquefoil 5_1;
  - linha 22: `ideal_lengths = [16.37, 21.17, 23.55]` (fonte citada no
    comentário da linha 17: "Pieranski, S. (1998). Ideal Knots" — citação
    incompleta; o autor de referência é Piotr Pieranski; nenhum DOI/página);
  - linha 32: massas up-type `[2.2, 1275, 173000]` MeV;
  - linha 38: massas down-type `[4.7, 95, 4180]` MeV;
  - linhas 50–59: ajuste por `np.polyfit` de `ln M` vs `L/D` (reta em
    log-espaço, 2 parâmetros livres por setor).
  - **O script NÃO computa R² em lugar nenhum.** O número `R² > 0.99`
    aparece apenas como texto em
    `.../quarks/index.html:333` ("For the Up-type sector (u, c, t), the fit
    is extraordinarily high (R² > 0.99)") e na tabela de
    `01_TAMESIS_CORE/RESEARCH_RESULTS.md:341-344` (R² > 0.99 para AMBOS os
    setores, α=1.53 up, α=0.90 down, status "CONFIRMED").
- **README:** `.../quarks/README.md:19-23` (mesma tabela de mapeamento),
  `README.md:36-41` (α≈1.53 up, α≈0.90 down).
- **Duplicata do modelo:**
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Universe_Equation/05_Particle_Spectrum/generate_visualizations.py:34-36`
  (mesmos L/D; massa do top ali é 172760 MeV, não 173000 — já uma
  inconsistência interna de dado).
- **Inconsistência interna de mapeamento:**
  `01_TAMESIS_CORE/RESEARCH_RESULTS.md:109-113` atribui Charm→5_1 (5
  cruzamentos) e Strange→4_1, contradizendo o mapeamento por geração da
  área quarks/ (Charm e Strange ambos em 4_1). O arquivo portanto NÃO tem
  um mapeamento único documentado; adotamos como "alegação canônica" o da
  área quarks/ (a que contém o ajuste), e registramos a contradição como
  achado.
- **Auditoria interna preexistente:** `.../quarks/AUDITORIA.md` (2026-07-29)
  já classifica o resultado como "ajuste fenomenológico exploratório" e
  exige validação leave-one-out nunca executada.

## Estrutura estatística declarada honestamente, a priori

Cada setor é um ajuste de **3 pontos com 2 parâmetros livres** (1 grau de
liberdade). R² em log-espaço mede apenas a colinearidade de 3 pontos no
plano `(L/D, ln M)`. Além disso há **liberdade de atribuição** (qual nó
para qual geração) não penalizada. Qualquer veredito "sobrevive" precisa
vencer esse handicap explícito — daí o critério (iv).

## Convenções fixadas

- Modelo: `ln M = c + α·(L/D)`, ajustado por OLS (`np.polyfit` grau 1),
  idêntico ao do arquivo. R² computado em log-espaço:
  `R² = 1 − SS_res/SS_tot` sobre `ln M`.
- *Ropelength* na literatura é usualmente `Rop = L/r` (raio unitário);
  o arquivo usa `L/D = Rop/2`. Conversão linear de escala em x **não altera
  R²** (invariância afim); altera só α por fator 2. Registrar em qual
  convenção cada valor de referência foi obtido e converter para L/D.
- Massas: MeV. Logaritmo natural.

## Critérios pré-declarados

### (i) Reprodução com os números do próprio arquivo

Rodar o ajuste com exatamente os vetores das linhas 22/32/38 de
`knot_mass_fit.py`. Computar α e R² por setor.
**Passa se:** α_up ≈ 1.53 e α_down ≈ 0.90 (±0.02) E R² > 0.99 nos setores
em que o arquivo alega (index.html alega para up; RESEARCH_RESULTS.md
alega para ambos — reportar ambos e confrontar as duas versões da
alegação).

### (ii) Reajuste com dados de referência independentes

- **Ropelength:** buscar valores publicados para 3_1, 4_1, 5_1 (e a tabela
  estendida do critério iv) via WebFetch/WebSearch — alvo primário
  KnotInfo (knotinfo.math.indiana.edu); alternativas: tabelas de
  Ashton–Cantarella–Piatek–Rawdon (2011) ou Katritch et al. (1996).
  URL + data + valores em `PROVENANCE.md`. Se inacessível: reportar
  inacessível, NUNCA digitar de memória.
- **Massas PDG** (pdg.lbl.gov): u, d, s em MS-bar a 2 GeV; c como m_c(m_c);
  b como m_b(m_b); top da média de medidas diretas (massa "de Monte
  Carlo"/pole-like) E, como sensibilidade, m_t MS-bar. Declarar
  explicitamente que massas leves são dependentes de esquema/escala — uma
  "lei" física teria que dizer qual massa entra, e o arquivo não diz.
**Passa se:** R² > 0.99 se mantém em AMBOS os setores com os dados
independentes (a alegação de RESEARCH_RESULTS.md é para ambos), sob a
combinação primária de esquemas; sensibilidade a esquema do top reportada.

### (iii) Leave-one-out (exigência da própria AUDITORIA.md)

Por setor: excluir cada quark, ajustar a reta nos 2 restantes (ajuste
exato), prever a massa do excluído. Erro em dex:
`e = |log10(M_pred / M_obs)|`. Total de 6 predições.
**Pré-declarado: uma predição FALHA se e > 0.5 dex (fator ~3.2).**
O critério (iii) **falha se qualquer uma das 6 predições falhar** — o
arquivo usa o modelo para prever uma 4ª geração a ~100 TeV, portanto
reivindica poder preditivo extrapolativo; errar um quark conhecido por
mais de um fator 3 é incompatível com isso. Reportar também os erros com
os números do próprio arquivo (critério iii-a) e com os dados
independentes (iii-b); o veredito usa iii-b.

### (iv) Nulo de permutação (liberdade de atribuição)

Tabela de nós: todos os nós primos com valor de ropelength publicado na
fonte obtida no (ii), até 9 cruzamentos inclusive (se a fonte cobrir
menos, usar o que houver e registrar). Duas distribuições nulas:

- **Nulo A (irrestrito):** todas as triplas ordenadas injetivas
  (Gen1,Gen2,Gen3) de nós distintos da tabela (ou amostra aleatória de
  100.000 se o total exceder isso; seed=12345). Ajustar o mesmo modelo por
  setor com dados independentes do (ii); registrar R².
- **Nulo B (monotônico):** subconjunto do Nulo A com
  L/D(Gen1) < L/D(Gen2) < L/D(Gen3) — respeita a motivação declarada
  "complexidade cresce com a geração", que é a única restrição que o
  arquivo oferece.

**Pré-declarado: a atribuição alegada (3_1, 4_1, 5_1) só conta como
não-trivial se seu R² estiver acima do percentil 95 da distribuição nula
correspondente, em CADA setor, no Nulo B (o nulo mais favorável à
alegação é o A; o B é o justo).** Reportar o rank nos dois nulos.

### Veredito máximo permitido

"sobrevive / não sobrevive à validação como formulado". Sobrevive apenas
se (i) E (ii) E (iii) E (iv) passarem. Se sobreviver, sinalizar
reprodução adversarial em nível de orquestrador antes de qualquer
reporte como real. Negativo tem o mesmo peso que positivo.

## Adendo permitido

No máximo UM adendo datado e delimitado a esta nota (p.ex. se a fonte
primária de ropelength estiver fora do ar e for preciso trocar de fonte),
antes de olhar qualquer resultado de ajuste com dados independentes.

## O que este teste NÃO é

Não é teste da hipótese física "partículas são sólitons topológicos" —
apenas da alegação numérica específica `M ∝ exp(α·L/D)` com R²>0,99 e do
seu status "CONFIRMED" em RESEARCH_RESULTS.md. Nenhuma inferência Tamesis
além do que o número sustentar.
