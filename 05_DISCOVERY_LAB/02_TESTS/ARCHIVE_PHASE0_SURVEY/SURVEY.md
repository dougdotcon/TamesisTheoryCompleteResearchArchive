# ARCHIVE-WIDE-PHASE0-SURVEY — levantamento de candidatos fora da forma TRI-RG

**Autoridade:** `DISC-DEC-023`, frente (b) — "busca de candidatos de pesquisa
genuinamente falsificaveis em todo o arquivo Tamesis (nao restrita a TRI-RG)
... busca e relatorio honesto, sem tocar dado real".

**Data:** 2026-08-22. **Metodo:** releitura dirigida do arquivo inteiro
(`01_TAMESIS_CORE`, `RECURSOS_PARA_PESQUISA`, `90_LEGACY`), checando cada
alegacao quantitativa/matematica contra os criterios do enunciado: (a) nao
coberta por `FAILED_HYPOTHESES.md` nem por nenhuma linha aberta/fechada de
`DISCOVERY_LAB_STATE.md`; (b) admite pergunta falsificavel precisa, com dado
real verificavel OU matematica pura derivavel; (c) tem modelo
concorrente/nulo nomeado ou criterio de sucesso/fracasso pre-declaravel; (d)
nao exige inventar hipotese nova sobre Ω/holografia/metafisica de substrato
informacional (fora de escopo aqui). Nenhum dado real foi baixado ou
processado nesta frente — apenas verificacao de existencia/acesso quando
aplicavel (WebSearch/WebFetch), igual ao padrao "verificar dado real antes de
declarar viavel" das fases 0/0.5/0.6/0.7/0.8 de `DISC-TRI-RG-001`, mas sem o
passo de calculo.

**Disciplina:** toda citacao usa `arquivo:linha`. Nenhuma alegacao fabricada.
Todo candidato marcado `viable:false` recebe justificativa concreta, nao um
descarte vago. Checagem de identificabilidade feita contra a lista COMPLETA
de linhas ja fechadas (`FAILED_HYPOTHESES.md`, `DISCOVERY_LAB_STATE.md`,
`00_GOVERNANCE/DECISION_LEDGER.yaml`), nao apenas contra `DISC-TRI-RG-001`.

**Por que a forma TRI-RG nao se aplica aqui:** as 5 rodadas de busca de
`DISC-TRI-RG-001` (`02_TESTS/TRI_RG/phase0/PHASE0*.md`) buscaram
especificamente um par `(R_lambda, I(X))` — mapa de coarse-graining +
invariante cross-domain. Esta frente busca qualquer alegacao quantitativa OU
objeto matematico derivavel, sem essa restricao de forma — mais perto de
como `DISC-CORE-NUMERICS-001` (M_c, quark-nos, ajustes de constante, U_1/2)
foi originada: releitura do arquivo procurando numeros/formulas nunca
adjudicados.

---

## Sumario executivo (preenchido ao final — ver secao "Ranking honesto")

19 candidatos considerados em 7 areas (particulas, cosmologia,
transicao quantico-classica/limite holografico, classes de universalidade
puras, reinterpretacoes de matematica/fisica ja estabelecida, misticismo/
Millennium fora de escopo, topologia cognitiva). Resultado antecipado: **18
rejeitados com justificativa concreta, 1 candidato marcado `viable: true`
mas imaturo** (precisa de nota de metodologia propria antes de qualquer
pre-registro — nenhuma alegacao de TAMESIS foi tocada em dado real nesta
frente). Ver secao final para o veredito completo e a recomendacao.

---

## Bloco 1 — Física de partículas (`01_TAMESIS_CORE/02_Experimental_Validation/Particle_Physics/`)

Todos os itens deste bloco carregam `AUDITORIA.md` interno já cético
(revisão de 2026-07-29), mas nenhum havia sido formalmente adjudicado pelo
Discovery Lab antes desta frente — `DISC-CORE-NUMERICS-001` onda 1 tocou
apenas `sin²θ_W` (electroweak) e a lei de nós de quarks (`quarks/`), ambos
já fechados `❌` em `FAILED_HYPOTHESES.md` §4.

### 1.1 Neutrino genus-mass ratio

- **Área:** `Particle_Physics/neutrinos/` — massa de neutrinos ~ `exp(α·2g)`
  do gênero topológico da superfície.
- **Alegação exata:** razão `m₃/m₂ ≈ 5,8` (de `Δm²_21=7,5e-5`,
  `Δm²_32=2,5e-3` eV², NuFIT) comparada a `exp(2)≈7,39` (previsão de Euler);
  melhor ajuste `α≈1,76` (`neutrinos/README.md:33-35`).
- **Dado real verificado?** Os valores de `Δm²` citam NuFIT/Super-Kamiokande
  (`neutrinos/AUDITORIA.md:5`) — fonte real e citável, não fabricada.
- **Modelo concorrente/nulo:** hierarquia de massa padrão (normal/invertida)
  sem lei topológica — razão `m₃/m₂` é parâmetro livre, sem valor previsto.
- **Risco de identificabilidade:** `neutrinos/simulation/genus_mass_simulation.py:68-76`
  mostra o problema estrutural na cara: **2 pontos de dado** (`m₂`, `m₃`)
  ajustados por **2 parâmetros livres** (`M₀`, `α`) — 0 graus de liberdade,
  o ajuste bate exatamente por construção, qualquer que seja a "lei"
  verdadeira. É a MESMA falha estrutural que já fechou `constant-fit-adjudication`
  (`α⁻¹=Ω^1.03`: "ajuste de 1 parâmetro a 1 número, 0 g.l." —
  `FAILED_HYPOTHESES.md:88`, `DECISION_LEDGER.yaml` `DISC-DEC-014` rationale).
- **`viable: false`** — não existe uma terceira massa/razão independente
  para dar poder ao ajuste; a "confirmação" do slope 1,76 vs. 2,0 é
  matematicamente garantida pela forma do ajuste, não um teste real.

### 1.2 Higgs VEV como potência de Ω

- **Área:** `Particle_Physics/paper_higgs_topology/`.
- **Alegação exata:** `v = M_Planck · Ω^power_v`, com `power_v` calculado
  por `power_v = log(v/M_planck)/log(Ω)` (`simulate_higgs.py:58`) — ou seja,
  o expoente é **resolvido a partir do valor conhecido de v**, não previsto.
- **Dado real verificado?** `v=246 GeV`, `M_Higgs=125,25 GeV` são valores
  PDG/ATLAS reais (`simulate_higgs.py:11-14`; `AUDITORIA.md:5` cita ATLAS
  Higgs 2012).
- **Modelo concorrente/nulo:** mecanismo de Higgs padrão (VEV como parâmetro
  livre do potencial, sem relação com Ω).
- **Risco de identificabilidade:** estrutura idêntica a `α⁻¹=Ω^1.03` já
  fechado `❌` em `constant-fit-adjudication` — 1 equação, 1 incógnita
  (`power_v`), 0 g.l., nenhuma previsão fora da amostra possível.
  `AUDITORIA.md:3` já nomeia isso: "é um ansatz até que a escala e o
  expoente sejam derivados de ação gauge-invariante".
- **`viable: false`** — mesma falha estrutural de uma linha já fechada.

### 1.3 Strong CP: θ = 0 topologicamente

- **Área:** `Particle_Physics/paper_strong_cp/`.
- **Alegação exata:** consistência de "winding" do braiding de glúons
  restringe `θ ∈ {0, π}`; `θ=π` é excluído por EDM de nêutron ⇒ `θ=0`
  (`analyze_strong_cp.py:82-88`).
- **Dado real verificado?** Limite experimental `d_n < 3×10⁻²⁶ e·cm` é real
  (fonte citada, `AUDITORIA.md:5`, PRL 124, 081803).
- **Modelo concorrente/nulo:** Peccei-Quinn/axion, quark up sem massa,
  antrópico — todos já compatíveis com `θ≈0` observado.
- **Por que falha o critério (c):** `θ=0` é exatamente o valor que TODOS os
  modelos concorrentes também acomodam (é o dado observado, não uma previsão
  discriminante) — não há observável que distinga "θ=0 por topologia" de
  "θ=0 por qualquer outro mecanismo" com o dado disponível. O próprio código
  admite isso implicitamente: não há previsão numérica testável além do
  valor já conhecido.
- **`viable: false`** — não falsificável/discriminante como formulado.

### 1.4 Flavor anomalies: correção topológica ao g-2 do múon

- **Área:** `Particle_Physics/paper_flavor_anomalies/`.
- **Alegação exata:** `δg ≈ (α/π)·ln(Ω)·(crossing_diff)`, com
  `crossing_diff=1` escolhido à mão (`analyze_anomalies.py:70-77`);
  resultado comparado à discrepância real `Δa_μ` (Fermilab 2021-2023,
  valores reais em `analyze_anomalies.py:9-11`) apenas por **ordem de
  grandeza** (`analyze_anomalies.py:84`, "MATCHES!").
- **Dado real verificado?** Sim — `Δa_μ` e R(K)/R(K*) são valores reais
  citados (HFLAV, Fermilab).
- **Modelo concorrente/nulo:** Modelo Padrão + hadronic vacuum polarization
  (a controvérsia lattice-vs-R-ratio já documentada no próprio script).
- **Risco de identificabilidade:** `crossing_diff` é um inteiro escolhido
  livremente, sem derivação; o teste declarado ("ordem de grandeza")
  não é um critério de sucesso/fracasso quantitativo — `AUDITORIA.md:3`
  já nomeia: "uma correção topológica de ordem de grandeza não é ajuste
  global".
- **`viable: false`** — nenhum critério quantitativo pré-declarável sem
  primeiro inventar o valor de `crossing_diff` a partir de uma derivação
  que não existe no arquivo.

### 1.5 Topologia bariônica / massa do próton por nós

- **Área:** `01_Foundation/Core_Papers/paper_baryon_topology/`.
- **Alegação:** massa do próton ~ modos vibracionais de um nó trifólio
  (`REAL_DISCOVERIES.md:136-139`).
- **Risco de identificabilidade — DIRETO:** esta é a mesma classe de
  alegação (massa de hádron por invariante de nó/crossing number) já
  testada e **REFUTADA** em `DISC-CORE-NUMERICS-001/knot-quark-mass`
  (`FAILED_HYPOTHESES.md:87`: "R² alegado nunca foi computado... leave-one-out
  falha em 5/6 quarks"). `paper_baryon_topology/AUDITORIA.md:12-15` nomeia a
  mesma lacuna estrutural (crossing number não é observável gauge-invariante
  estabelecido, sem ação efetiva, sem quantização).
- **`viable: false`** — redundante com linha já fechada; não há dado ou
  método novo aqui, apenas a mesma alegação em outro hádron.

---

## Bloco 2 — Cosmologia (`01_TAMESIS_CORE/02_Experimental_Validation/Cosmology/`)

Distinto de `DISC-COSMOLOGY-MOND-SPARC-00{1..4}` (que testou EFE/a₀ contra
SPARC e Gaia) — este bloco cobre as OUTRAS 6 alegações cosmológicas do
núcleo, nunca tocadas pelo Discovery Lab.

### 2.1 Tensão de Hubble: fator 1+1/12 "Casimir"

- **Área:** `RECURSOS_PARA_PESQUISA/PATH_A_SCIENTIFIC_TRUTH/STAGE_03_H0_HUBBLE_TENSION/hubble_gap_solver.py`,
  citado em `RECURSOS_PARA_PESQUISA/REAL_DISCOVERIES.md:120-122` e
  `01_TAMESIS_CORE/RESEARCH_RESULTS.md:375-387` (η=1,083).
- **Alegação exata:** `H₀^Late = H₀^CMB × (1+1/12)` ⇒ `67,4×1,0833=73,01`
  km/s/Mpc, "match perfeito" com SH0ES.
- **Dado real verificado?** `H₀^Planck=67,4±0,5` e `H₀^SH0ES=73,0±1,0` são
  valores reais (Planck 2020, Riess et al. 2022 — citados em
  `paper_hubble_tension/AUDITORIA.md:5`).
- **Modelo concorrente/nulo:** nenhuma tensão real (erro sistemático de
  calibração) — a própria auditoria interna já assinala isso
  (`paper_hubble_tension/AUDITORIA.md:3`: "não é resolução estabelecida").
- **Risco de identificabilidade — FUMAÇA DA ARMA NO PRÓPRIO CÓDIGO:**
  `hubble_gap_solver.py:27-30` documenta literalmente uma busca por
  numerologia: `# Search for Geometric Candidate ... Factor = 1 + zeta(-1)?
  No, zeta(-1) is -1/12. Factor = 1 + |zeta(-1)| = 1 + 1/12.` — a constante
  foi tentada, o sinal invertido até bater com a razão **já conhecida**
  73,0/67,4≈1,083 entre 2 números que o próprio script já tinha antes de
  "derivar" o fator. Zero graus de liberdade, mesma classe de falha já
  fechada em `constant-fit-adjudication` (varredura de `ξ` do bounce até
  `n_s` bater — `FAILED_HYPOTHESES.md:88`).
- **`viable: false`** — numerologia pós-hoc documentada no próprio
  comentário do código, não uma derivação.

### 2.2 JWST: fator de aceleração de formação de galáxias

- **Área:** `paper_jwst_galaxies/analyze_jwst.py`.
- **Alegação exata:** `enhancement=5` (Myr efetivo = 5× o tempo ΛCDM),
  escolhido de um intervalo verbal "3-10x" (`analyze_jwst.py:64-70`), sem
  derivação a partir de nenhuma fórmula Tamesis.
- **Dado real verificado?** NÃO — a "curva de observações JWST" no gráfico
  é explicitamente `# "JWST observations" (schematic)` (`analyze_jwst.py:97`),
  não dado real de catálogo algum; nenhum z, massa estelar ou contagem de
  galáxias real é citado com número, apenas prosa ("10-100x mais massivas").
- **Modelo concorrente/nulo:** ΛCDM padrão com função de massa calibrada
  (ex. Labbé et al. 2023, Naidu et al. — citado em `AUDITORIA.md:5`, mas
  nunca usado quantitativamente no script).
- **Risco de identificabilidade:** `enhancement` é um parâmetro livre
  escolhido dentro de um range verbal, não uma previsão — qualquer valor
  entre 3 e 10 "funcionaria"; mesmo padrão de 0 g.l. das linhas já fechadas.
- **`viable: false`** — nem fórmula derivada nem dado real usado
  quantitativamente; falha o critério (b) diretamente.

### 2.3 CMB B-modes: r → 0

- **Área:** `paper_cmb_bmodes/`.
- **Já auditado internamente** (`AUDITORIA.md:3`): "`r → 0` não é assinatura
  exclusiva de TAMESIS; várias classes inflacionárias e incertezas de
  foreground produzem limites semelhantes."
- **`viable: false`** — não discriminante (falha critério c) pela própria
  auditoria interna do arquivo, confirmada nesta releitura.

### 2.4 Ondas gravitacionais: assinatura EMRI

- **Área:** `paper_gravitational_waves/analyze_gw.py`.
- **Alegação:** desvio de GR em EMRIs de baixa aceleração; o próprio script
  admite "Current precision: insufficient to detect" para o canal mais
  promissor (ringdown/EMRI).
- **`viable: false`** — não testável com dado atualmente acessível (nenhum
  detector, presente ou anunciado, tem sensibilidade no regime declarado);
  falha critério (b) por ausência de dado real acessível agora.

### 2.5 Vazios cósmicos / superestruturas

- **Área:** `paper_cosmological_voids/`.
- **Já auditado internamente** (`AUDITORIA.md:3`): "modelo entrópico é
  hipótese condicional; requer mocks pareados, covariância e comparação
  ΛCDM" — nenhuma fórmula Tamesis-específica é computada no script, apenas
  a tensão ΛCDM já conhecida na literatura (El Gordo, Sloan Great Wall) é
  reafirmada em prosa.
- **`viable: false`** — nenhuma previsão numérica Tamesis-específica existe
  a testar; falha critério (b).

### 2.6 Constante cosmológica / catástrofe do vácuo (`Cosmology/lambda/`)

- **Alegação:** `ρ_Λ ~ 1/L_H²` (holográfico), `8,5e-27` vs. observado
  `5,8e-27 kg/m³` (`×1,46`) — `RESEARCH_RESULTS.md:360-371`.
- **Risco de identificabilidade — DIRETO:** `1/L_H² ∝ H₀² ∝ ρ_crit`
  por definição (`L_H=c/H₀`) — é a MESMA identidade algébrica já fechada
  `❌` em `constant-fit-adjudication`: "`Λ`: identidade algébrica com
  `ρ_crit`" (`FAILED_HYPOTHESES.md:88`), apenas calculada em outro arquivo
  do arquivo (`02_Experimental_Validation/Cosmology/lambda/` em vez de
  `03_Axiomatic_Closure/Universe_Equation/03_Lambda_Derivation/`).
- **`viable: false`** — redundante com linha já fechada, mesma tautologia
  dimensional.

---

## Bloco 3 — Transição quântico-clássica além de M_c

### 3.1 "A Holographic Bound on Macroscopic Quantum Superpositions"

- **Área:** `01_TAMESIS_CORE/08_AHolographicBoundonMacroscopicQuantumSuperpositions/`
  (paper completo com PDF, versão PRL).
- **Risco de identificabilidade — DIRETO:** `AUDITORIA_paper.md:3` cita
  exatamente `M_c ~ 10⁻¹⁴ kg` como o valor central do paper — é o MESMO
  objeto já adjudicado em `DISC-CORE-NUMERICS-001/mc-internal-consistency`
  (`FAILED_HYPOTHESES.md:86`: "os 4 valores de `M_c` do núcleo divergem em
  até 189,7×"; um dos 4 valores documentados é justamente `2,2×10⁻¹⁴ kg`,
  `RESEARCH_RESULTS.md:479`, a "Killer Prediction"). Este paper é uma
  formalização mais longa do MESMO número já mostrado inconsistente.
- **`viable: false`** — redundante com linha já fechada; a alegação central
  (transição abrupta vs. gradual) também não é testável com dado real hoje
  — `AUDITORIA_paper.md:3` já nomeia "o valor `10⁻¹⁴ kg` não é universal sem
  esses parâmetros", e experimentos reais de interferometria (Fein et al.
  2019, ~10⁻²⁰ kg) estão ~6 ordens de grandeza abaixo de `M_c` — nenhum dado
  real acessível hoje testa a forma funcional (degrau vs. decaimento
  gradual).

---

## Bloco 4 — Classes de universalidade além de U₁/₂ (matemática pura ainda não formulável)

`DISC-CORE-NUMERICS-001` já adjudicou `U_1/2` (φ(c)=(1+c)^(-1/2), REFUTADO
como fórmula fechada mas expoente 1/2 confirmado — ver `FAILED_HYPOTHESES.md`
§5) e sua generalização `U_α`. `06_Universality_Discovery/Universality_Classes/`
lista mais duas classes candidatas (`U₀`, `U₂`) nunca tocadas.

### 4.1 U₀ — limiar de classicalidade via percolação em grafo de Hilbert

- **Área:** `Universality_Classes/U0_Threshold/`.
- **Por que falha o critério (b) agora:** `AUDITORIA.md:19-21` (própria
  auditoria interna) diz sem rodeios: "o grafo, os nós, as arestas e a
  variável `p` não estão definidos a partir de um Hamiltoniano ou processo
  quântico concreto"; "`p_c=1/d` depende da topologia e não é um limiar
  universal"; "a relação `p∼e^(−S/S_BH)` não tem derivação no artigo." —
  não existe hoje um objeto matemático computável, apenas um esboço
  conceitual. Adjudicar isso exigiria primeiro CONSTRUIR a teoria (definir
  o grafo, derivar `p`), o que é trabalho de pesquisa nova, não uma
  adjudicação de alegação existente — foge do escopo desta frente
  (ver critério d, "não inventar hipótese nova").
- **`viable: false`** — objeto matemático não está definido o suficiente
  para admitir pergunta falsificável; não é um "U_1/2 escondido em
  linguagem especulativa" — é uma lacuna de derivação reconhecida
  internamente, não uma fórmula pronta para adjudicar.

### 4.2 U₂ — dinâmica de Lindblad com γ_k geométrico

- **Área:** `Universality_Classes/U2_Lindblad/`.
- **Mesma falha:** `AUDITORIA.md:19` — "não existe derivação apresentada
  para `γ_k` a partir do spectral form factor." A equação de Lindblad em si
  é matemática padrão bem estabelecida (Lindblad 1976); o que seria
  Tamesis-específico (`γ_k` de uma geometria/defeito topológico) nunca foi
  derivado.
- **`viable: false`** — mesma razão de 4.1: nenhuma fórmula concreta a
  adjudicar ainda.

### 4.3 Universality Atlas (taxonomia geral)

- **Área:** `Universality_Atlas/`.
- **Veredito da própria auditoria interna** (`AUDITORIA.md:8`): "os rótulos
  U e expoentes misturam propriedades de modelos diferentes e não
  constituem classes universais no sentido de teoria de escala."
- **`viable: false`** — a própria fonte já se autodescredencia como
  taxonomia não validada, não uma lista de candidatos prontos.

---

## Bloco 5 — Matemática/física já estabelecida, reinterpretada em linguagem Tamesis (sem alegação nova)

Estes três candidatos pareciam promissores pelo título ("prova estrutural
profunda"), mas na leitura completa revelaram-se reinterpretações narrativas
de resultados matemáticos ou experimentais JÁ PROVADOS/CONFIRMADOS há
décadas — não há alegação Tamesis-específica falsificável, apenas metáfora
sobre um resultado que já é verdade independentemente de Tamesis.

### 5.1 Teorema de Bruns / problema dos 3 corpos

- **Área:** `RECURSOS_PARA_PESQUISA/10_LAGRANGE_PROBLEM/readme.md`.
- **Conteúdo:** reafirma o teorema de Heinrich Bruns (1887) — não existem
  integrais algébricas adicionais para o problema de 3 corpos — em
  linguagem de "Teoria de Incompatibilidade de Regimes" (`readme.md:9-15`).
- **`viable: false`** — o teorema de Bruns já é matemática rigorosamente
  provada há 139 anos; não há nenhuma previsão NOVA, falsificável ou não,
  proposta aqui — é reformulação de vocabulário sobre um resultado clássico.

### 5.2 Legado de Tonomura / efeito Aharonov-Bohm

- **Área:** `RECURSOS_PARA_PESQUISA/11_TONOMURA_REALITY_A4/readme.md`.
- **Conteúdo:** reafirma o experimento de Tonomura (1986), já confirmado
  experimentalmente e aceito no consenso da física, como "prova" do
  "paradigma da Informação" de Tamesis (`readme.md:9-16`).
- **`viable: false`** — o resultado físico (realidade do potencial vetor via
  efeito AB) já está estabelecido e confirmado desde 1986; a leitura Tamesis
  é interpretativa, não produz uma previsão adicional testável.

### 5.3 Fita de Möbius (topologia experimental)

- **Área:** `02_Experimental_Validation/Mobius_Topology/readme.md`.
- **Conteúdo:** protocolo de corte de fita de Möbius com as propriedades
  topológicas corretas e já conhecidas (Listing 1847, Möbius 1858) —
  `readme.md:116-146` — seguido de "insights TAMESIS" puramente
  metafóricos (regimes quântico/clássico como as duas fitas resultantes,
  `readme.md:150-211`), sem formalização que gere um número ou previsão
  testável distinto da topologia elementar já sabida.
- **`viable: false`** — matemática elementar já demonstrada há 168 anos;
  nenhuma pergunta nova, falsificável ou não, é formulada.

---

## Bloco 6 — Fora de escopo por desenho (critério d) ou por conteúdo não-físico

### 6.1 P vs NP / "Censura Termodinâmica"

- **Área:** `RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/P_vs_NP_Paper/`.
- **Por que fora de escopo:** é uma alegação de resolução de um Problema do
  Millennium (P vs NP), explicitamente vedada em toda a governança do
  laboratório desde `DISC-DEC-001` ("nenhuma alegação de Problema do
  Millennium resolvido, aproximado, ou alcançável por esta trilha" —
  `DECISION_LEDGER.yaml:63`, salvaguarda repetida em toda decisão
  subsequente). Não avaliado quanto ao mérito — descartado por desenho,
  como o próprio mandato desta frente exige.

### 6.2 Landauer / termodinâmica pós-morte

- **Área:** `RECURSOS_PARA_PESQUISA/14_LANDAUER/readme.md`.
- **Por que fora de escopo:** aplica o princípio de Landauer a "morte/
  reencarnação" e audita teorias gnósticas/"Arcontes" (`readme.md:9-30`) —
  não é uma alegação física ou matemática falsificável, é especulação
  metafísica explícita. Não avaliado quanto ao mérito.

---

## Bloco 7 — Candidato genuinamente novo: assinaturas espectrais de regimes cognitivos

### 7.1 Topologia espectral de EEG em depressão/ansiedade (redshift/blueshift)

- **Área:** `90_LEGACY/08_COGNITIVE_TOPOLOGY/TOPOLOGICAL_THEORY_OF_COGNITIVE_STATES/PAPER_B_SPECTRAL_SIGNATURES.md`.
- **Alegação:** mapeando autovalores do Laplaciano do conectoma para bandas
  de EEG (`PAPER_B_SPECTRAL_SIGNATURES.md:36-42`), o paper prevê uma
  assinatura espectral distinta para 3 regimes patológicos: depressão
  ("Entropic Trap" — colapso de altas frequências, dominância de baixos
  autovalores `λ→0`, baixa complexidade de Lempel-Ziv, linhas 53-63);
  ansiedade ("Oscillatory Chaos" — ruído de alta frequência não travado em
  fase, alta entropia "ruim", linhas 65-73); e uma terceira classe
  metabólica/viscosa (achatamento do PSD `1/f^α` com `α` maior, linhas
  75-83).
- **Dado real acessível?** VERIFICADO PARCIALMENTE nesta sessão, sem
  download/computo (fora de escopo aqui): (1) dataset Mumtaz et al. — 34
  pacientes MDD + 30 controles saudáveis, 19 canais 10-20, olhos
  fechados/abertos, hospedado no Figshare
  (`figshare.com/articles/dataset/EEG_Data_New/4244171`), amplamente citado
  na literatura publicada — confirmado via WebSearch nesta sessão, mas o
  WebFetch direto retornou HTTP 403 (provável bloqueio anti-bot da
  plataforma, não indício de que o dataset não existe ou é fabricado — 
  precisa de verificação por download real numa frente futura); (2) DASPS
  (ansiedade, 23 sujeitos, EEG 14 canais) confirmado acessível via
  WebFetch nesta sessão, IEEE DataPort, login gratuito sem aprovação
  institucional (`ieee-dataport.org/open-access/dasps-database`,
  verificado 2026-08-22); (3) MODMA (depressão, 128 canais) existe mas
  exige aprovação institucional — mencionado apenas como alternativa, não
  necessário dado que Mumtaz/DASPS já cobrem o essencial.
- **Modelo concorrente/nulo nomeável:** literatura de grafo-teoria clínica
  já publicada mostra achados ESPECÍFICOS e por vezes DIRECIONALMENTE
  DIFERENTES do que o paper Tamesis prevê — ex. coeficiente de
  clustering/eficiência local REDUZIDOS em MDD (achado real, ver busca
  desta sessão), enquanto o paper Tamesis associa MDD a alta conectividade
  local rígida ("deep local attractor", `PAPER_B:56-58`) — a literatura
  publicada de conectividade funcional em MDD serve como modelo
  concorrente nomeado e imediatamente disponível para comparação.
- **Por que NÃO está pronto para pré-registro hoje (o que falta):**
  1. **Nenhum limiar numérico é declarado no arquivo** — toda a previsão é
     qualitativa ("colapso", "dominância", linhas 53-83) sem uma estatística
     `I(X)` fechada (ex.: `λ₂` exato, inclinação `1/f` exata, threshold de
     Lempel-Ziv) nem um critério de decisão pré-declarável — falha o
     critério (c) COMO ESTÁ ESCRITO no arquivo, precisaria de nota de
     metodologia própria para operacionalizar antes de qualquer
     pré-registro (mesmo trabalho que `DISC-DEC-004` fez para `a₀`, não uma
     invenção de hipótese nova — a hipótese qualitativa já existe no
     arquivo, falta só sua forma quantitativa).
  2. **Download/inspeção do dataset não foi feito** (fora de escopo desta
     frente) — acesso real ainda não confirmado por bytes, só por busca.
  3. Amostra pequena em ambos os datasets identificados (N=64 MDD/HC,
     N=23 ansiedade) — poder estatístico precisaria ser calculado a priori
     antes de qualquer lock.
- **Risco de identificabilidade vs. linhas já fechadas:** MODERADO, não
  direto. `DISC-TRI-RG-001` já testou entropia de permutação e MSE sobre
  EEG real (`VitalDB` indução de anestesia, `permutation_entropy/
  RESULTS_SUMMARY.md` — NEGATIVO, `FAILED_HYPOTHESES.md:35`) usando
  ferramental estatístico da MESMA família (entropia/complexidade de sinal
  fisiológico) — mas para uma PERGUNTA estruturalmente diferente
  (transição de regime dentro do mesmo sujeito ao longo do tempo, exigida
  pela forma TRI-RG) contra a pergunta aqui (classificação estática
  MDD-vs-saudável entre sujeitos diferentes, explicitamente o tipo de
  comparação que a própria síntese de `PHASE0_SURVEY.md:146-154` rejeitou
  como forma errada PARA TRI-RG, mas que é exatamente a forma CORRETA para
  uma pergunta de classificação clínica). Não é redundância direta, mas o
  histórico de nulos desta lab usando entropia/complexidade em sinal
  fisiológico é um prior de cautela genuíno, não um motivo de descarte.
- **`viable: true`, mas IMATURO** — é o único candidato desta frente com
  (i) domínio genuinamente não tocado por nenhuma linha fechada, (ii) dado
  real existente e parcialmente confirmado acessível, (iii) um modelo
  concorrente nomeável a partir de literatura publicada real, e (iv) uma
  hipótese qualitativa já articulada no próprio arquivo — mas exige uma
  nota de metodologia completa (operacionalizar `I(X)`, decidir `R_lambda`/
  pré-processamento de EEG, calcular poder a priori, verificar acesso real
  por download) ANTES de qualquer pré-registro. Não deve ser tratado como
  pronto para lock — é matéria-prima para uma frente futura dedicada, não
  um resultado desta frente de reconhecimento.

---

## Tabela-resumo (19 candidatos, 7 áreas)

| # | Candidato | Área | Dado real verificado? | Modelo concorrente/nulo | Risco de identificabilidade | `viable` |
|---|---|---|---|---|---|---|
| 1.1 | Neutrino genus-mass ratio | Partículas | Sim (NuFIT/Super-K) | Hierarquia padrão, sem lei topológica | Mesma falha 0 g.l. de `constant-fit-adjudication` | false |
| 1.2 | Higgs VEV = M_P·Ω^power | Partículas | Sim (PDG/ATLAS) | Mecanismo de Higgs padrão | Idêntico a `α⁻¹=Ω^1.03` já fechado | false |
| 1.3 | Strong CP θ=0 topológico | Partículas | Sim (limite EDM nêutron) | PQ/axion, u sem massa, antrópico | Não-discriminante (falha critério c) | false |
| 1.4 | g-2 do múon via crossing topológico | Partículas | Sim (Fermilab/HFLAV) | MP + hadronic VP | `crossing_diff` livre, "ordem de grandeza" não é critério | false |
| 1.5 | Massa bariônica por nó trifólio | Partículas | Parcial (sem dado processado) | Espectroscopia/lattice QCD | Redundante — mesma falha de `knot-quark-mass` já `❌` | false |
| 2.1 | H₀ tardio = H₀ CMB × (1+1/12) | Cosmologia | Sim (Planck/SH0ES) | Sistemático de calibração (sem tensão real) | Numerologia pós-hoc documentada no próprio código | false |
| 2.2 | JWST enhancement=5× | Cosmologia | Não (curva "schematic") | ΛCDM calibrado (Labbé et al.) | Parâmetro livre sem derivação nem dado real usado | false |
| 2.3 | CMB B-modes r→0 | Cosmologia | Sim (BICEP/Keck) | Múltiplas classes inflacionárias | Não-discriminante (auditoria interna já admite) | false |
| 2.4 | GW assinatura EMRI | Cosmologia | Não (precisão insuficiente hoje) | GR padrão | Não testável com instrumentação atual | false |
| 2.5 | Vazios cósmicos entrópicos | Cosmologia | Sim (tensão já conhecida na lit.) | ΛCDM + mocks pareados | Nenhuma fórmula Tamesis computada | false |
| 2.6 | ρ_Λ ~ 1/L_H² | Cosmologia | Sim (Planck) | — | Redundante — idêntico a `Λ=identidade ρ_crit` já `❌` | false |
| 3.1 | Bound holográfico em superposição macroscópica | Quântico-clássico | Parcial | CSL/GRW/decoerência padrão | Redundante — mesmo M_c já `❌` em `mc-internal-consistency` | false |
| 4.1 | U₀ (percolação em grafo de Hilbert) | Universalidade | N/A (objeto não definido) | — | Sem fórmula computável ainda (não é adjudicável) | false |
| 4.2 | U₂ (Lindblad γ_k geométrico) | Universalidade | N/A (objeto não definido) | — | Sem fórmula computável ainda | false |
| 4.3 | Universality Atlas geral | Universalidade | N/A | — | Auto-descredenciado pela própria auditoria | false |
| 5.1 | Teorema de Bruns (3 corpos) | Matemática estabelecida | N/A | — | Matemática já provada (1887), sem alegação nova | false |
| 5.2 | Tonomura/Aharonov-Bohm | Física estabelecida | N/A | — | Experimento já confirmado (1986), sem alegação nova | false |
| 5.3 | Fita de Möbius | Topologia elementar | N/A | — | Matemática já provada (1858), sem alegação nova | false |
| — | P vs NP / Censura Termodinâmica | Millennium | — | — | Fora de escopo por desenho (critério d) | não avaliado |
| — | Landauer / reencarnação | Metafísica | — | — | Fora de escopo (não-físico) | não avaliado |
| **7.1** | **Assinatura espectral EEG (depressão/ansiedade)** | **Cognitivo/clínico** | **Parcial (2 datasets reais localizados, acesso não baixado)** | **Grafo-teoria clínica publicada (clustering/eficiência)** | **Moderado, não direto — mesma família estatística de 3 candidatos já `❌` de TRI-RG, mas pergunta estruturalmente diferente** | **true (imaturo)** |

---

## Ranking honesto

**19 candidatos considerados em 7 áreas distintas** (física de partículas,
cosmologia, transição quântico-clássica, classes de universalidade puras,
matemática/física já estabelecida, temas fora de escopo por desenho, e
topologia cognitiva). **18 rejeitados com justificativa concreta e citação
`arquivo:linha`. 1 candidato marcado `viable: true`, mas explicitamente
imaturo** — não é um resultado, é uma pista honesta para uma frente futura.

Padrões que se repetiram através de quase todas as rejeições, valendo a
pena nomear explicitamente (achado estrutural desta própria frente, no
mesmo espírito do achado estrutural de `DISC-TRI-RG-001` sobre os 4 eixos
latentes — `FAILED_HYPOTHESES.md:45-51`):

1. **Ajuste de 0 graus de liberdade** (1-2 números conhecidos, 1-2
   parâmetros livres resolvidos para bater exatamente) apareceu em 5 dos 19
   candidatos (1.1, 1.2, 2.1, e por extensão a mesma família já fechada em
   `constant-fit-adjudication`) — o núcleo Tamesis parece ter um padrão
   recorrente de "resolver o expoente/fator a partir do alvo conhecido" em
   vez de prevê-lo independentemente. Isso já era conhecido de
   `DISC-CORE-NUMERICS-001`, mas esta frente confirma que o padrão se
   estende a MUITO mais alegações do núcleo do que as 4 originalmente
   adjudicadas.
2. **Redundância com linhas já fechadas** apareceu em 3 candidatos (1.5,
   2.6, 3.1) — a mesma alegação subjacente (massa por nó, `Λ~ρ_crit`, `M_c`)
   reaparece em múltiplos arquivos/pastas do arquivo sob nomes diferentes.
3. **Matemática ou física já estabelecida, sem alegação nova** apareceu em
   3 candidatos (5.1, 5.2, 5.3) — reinterpretação narrativa de resultados
   centenários/1986, não pesquisa nova.
4. **Objeto matemático nunca definido o suficiente para ser adjudicável**
   apareceu em 3 candidatos (4.1, 4.2, 4.3) — diferente do que aconteceu
   com `U_1/2` (que tinha uma fórmula fechada pronta,
   `φ(c)=(1+c)^(-1/2)`, mesmo que errada), `U₀`/`U₂` nunca chegaram a ter
   uma fórmula candidata — não são "U_1/2 escondidos", são esboços
   conceituais sem derivação.
5. **Dado real inexistente ou inacessível hoje** apareceu em 2 candidatos
   (2.2 JWST, 2.4 GW EMRI).

## Recomendação

**Não há candidato pronto para pré-registro nesta frente.** O único
candidato com um caminho honesto adiante é **7.1 (assinatura espectral de
EEG em depressão/ansiedade)** — mas ele exigiria, antes de qualquer
`PREREGISTRATION.md`, o mesmo trabalho de formulação que precedeu
`DISC-TRI-RG-001` e `DISC-COSMOLOGY-MOND-SPARC-002`: (a) operacionalizar
`I(X)` com uma fórmula fechada e um critério de decisão pré-declarável
(não apenas "colapso"/"dominância" qualitativos); (b) baixar e inspecionar
de fato o dataset Mumtaz (Figshare) e/ou DASPS (IEEE DataPort) — o acesso
foi localizado mas não verificado por download nesta sessão; (c) calcular
poder estatístico a priori dado o N pequeno de ambos os datasets (64 e 23
sujeitos); (d) nomear precisamente o modelo concorrente (qual métrica
específica da literatura de grafo-teoria clínica, com qual direção
prevista, servirá de comparação). Isso é trabalho de uma frente nova
dedicada, não desta frente de reconhecimento — nenhum dado real foi
tocado aqui, por desenho.

Se o usuário decidir não perseguir 7.1, o resultado honesto desta frente é
**"nenhum candidato novo viável encontrado nesta rodada"** — um resultado
negativo de valor completo, no mesmo espírito do encerramento formal de
`DISC-TRI-RG-001` (`DISC-DEC-010`, `FAILED_HYPOTHESES.md` §1): a releitura
completa do arquivo, fora da forma TRI-RG, majoritariamente encontrou
alegações já cobertas por linhas fechadas, alegações estruturalmente
não-falsificáveis (0 graus de liberdade ou não-discriminantes), ou
matemática/física já estabelecida vestida de linguagem Tamesis — não um
poço de candidatos genuinamente novos esperando para ser testados. Isso é
consistente com o próprio achado de `DISC-DEC-013` (a releitura que
originou `DISC-CORE-NUMERICS-001` já havia identificado a maior parte das
alegações quantitativas genuinamente novas do núcleo) e com o achado
estrutural de `DISC-TRI-RG-001` (grande parte do espaço de "invariantes
óbvios" já estava coberta antes de qualquer candidato individual ser
testado) — o arquivo parece ter uma quantidade finita e já
substancialmente explorada de alegações numéricas adjudicáveis fora da
tese central.

