# Nota de metodologia — `constant_fits` (adjudicação de ajustes de constantes no núcleo Tamesis)

**Linha:** DISC-CORE-NUMERICS-001 · **Frente:** constant-fit-adjudication (autorizada por DISC-DEC-013)
**Status:** critérios de decisão fixados ANTES de qualquer fetch de valor de referência
externo (PDG, CODATA/NIST, Planck) e antes de qualquer cálculo de σ. Mesma disciplina
de METHODOLOGY_NOTE.md de toda a história da linha TRI-RG.

**Natureza:** adjudicação de mesa ("desk check") sobre alegações INTERNAS do arquivo,
comparadas a valores medidos externos. Nenhuma alegação de física nova é feita aqui —
apenas veredito por sub-alegação, no vocabulário máximo permitido:
"consistente/inconsistente como formulado" + "identificável/não-identificável (tuning)".

---

## Sub-alegação (a): sin²θ_W = 3/13 = 0,230769… — "CONFIRMED, 0,19% error"

### Fonte exata no núcleo (localizada ANTES desta nota; citações literais)

- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:321-328`:
  > `| **Hypothesis** | sin²θ_W = 3/13 (Kissing Number) |`
  > `| **Status** | ✅ **CONFIRMED** |`
  > `| Geometric prediction | **0.23077** |`
  > `| CODATA observed | **0.23122 ± 0.00004** |`
  > `| Discrepancy | **0.19%** |`
- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:31`:
  > `| Weak mixing (sin²θ_W) | 0.23077 | 0.23122 | **0.19%** |`
- `01_TAMESIS_CORE/02_Experimental_Validation/Particle_Physics/electroweak/README.md:25`:
  > `We scanned various geometric ratios (simulation/torsion_angle.py) to match the observed CODATA value ($\sin^2 \theta_W = 0.23122$).`
- `.../electroweak/simulation/torsion_angle.py:15-16`: `target_s2w = 0.23122` declarado
  como alvo da busca; linhas 40-45 do mesmo script reconhecem o valor on-shell/tree
  ≈ 0,223 via M_W/M_Z.
- Auditoria interna já existente: `.../electroweak/AUDITORIA.md:3` — "A razao 3/13 e uma
  associacao numerica baseada em uma rede hipotetica. Ela nao deriva o angulo de
  Weinberg sem Lagrangiana, simetria de gauge, escala de renormalizacao e correcoes
  radiativas."

### Requisito de honestidade sobre esquema (fixado a priori)

sin²θ_W é dependente de esquema de renormalização. Serão buscados no PDG, com
proveniência (URL + data + valor citado literalmente):

1. **MS-bar em M_Z** — ŝ²_Z (o esquema do valor 0,23122 citado pelo próprio núcleo);
2. **on-shell** — s²_W = 1 − M_W²/M_Z² (≈ 0,223x);
3. **efetivo leptônico** — sin²θ_eff^lept (≈ 0,2315x).

A adjudicação será feita (i) sob MS-bar (o esquema que o núcleo cita como alvo) e
(ii) sob O ESQUEMA MAIS CARIDOSO — aquele em que |3/13 − valor|/σ_esquema for mínimo.
O veredito final usa a leitura mais caridosa: só é algo diferente de
"inconsistente como formulado" se sobreviver a ela.

### Critérios de decisão (pré-declarados)

- **"consistente como formulado":** exige |3/13 − valor_PDG|/σ_PDG ≤ 2 no esquema mais
  caridoso E rótulo interno "CONFIRMED, 0,19% error" fiel (i.e., 0,19% de fato dentro
  de ~2σ da medida). Caso contrário: "inconsistente como formulado". Nota pré-declarada:
  como as incertezas do PDG em sin²θ_W são O(10⁻⁴)–O(10⁻⁵), um desvio percentual de
  0,19% (~4,5×10⁻⁴ absoluto) só poderia ser "consistente" se σ_PDG ≳ 2×10⁻⁴ — o número
  de σ será computado e reportado, não presumido.
- **"identificável":** exige que 3/13 tenha sido fixado INDEPENDENTEMENTE do valor-alvo.
  A evidência interna já localizada (README:25 "scanned … to match the observed CODATA
  value"; script com `target_s2w` explícito) será adjudicada contra este critério: uma
  razão selecionada por varredura contra o alvo NÃO é identificável, salvo se algum
  documento do núcleo (a ser citado com file:line) fixar 3/13 antes/independentemente
  do alvo. Também será registrado que a escolha do ESQUEMA em que a comparação é feita
  constitui um grau de liberdade adicional pós-hoc, se for o caso.

### Plano de fetch

- PDG (pdg.lbl.gov): Review "Electroweak Model and Physics of Constants" e/ou
  Physical Constants summary table, edição corrente (2024/2025). Se pdg.lbl.gov estiver
  inacessível, reportar INACESSÍVEL — nunca substituir por memória.

---

## Sub-alegação (b): α⁻¹ = Ω^1.03 ≈ 137,04, com Ω = 117,038

### Fonte exata no núcleo

- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:61-62`:
  > `| Fine structure | α⁻¹ = Ω^β | 137.04 | 137.035999 | **0.003%** |`
  > `| Exponent β | — | 1.033 | N/A | — |`
- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:30`:
  > `| Fine structure (α⁻¹) | 137.04 | 137.035999 | **0.003%** |`
- Ω = 117,038 declarado como "TAMESIS compression" em `RESEARCH_RESULTS.md:704`; o
  próprio núcleo lista `paper_origin_omega` como "⏳ In Progress" (`RESEARCH_RESULTS.md:211`)
  — i.e., Ω não tem derivação fechada nem incerteza propagada no arquivo.
- Auditoria interna já existente:
  `01_TAMESIS_CORE/01_Foundation/Core_Papers/paper_fine_structure/AUDITORIA.md:4`:
  > `**Nível global:** E0/H1 — coincidência numérica, não derivação`

### Critérios de decisão (pré-declarados)

- Esta adjudicação é primariamente de **IDENTIFICABILIDADE**, não de σ: um expoente
  contínuo livre β ajustado a um único número pode reproduzir QUALQUER alvo positivo
  exatamente (x = ln α⁻¹ / ln Ω sempre existe). Computar:
  1. o expoente exato x* que resolve Ω^x = α⁻¹_CODATA;
  2. a sensibilidade dα⁻¹/dβ em β≈1,03 (quantos dígitos de β são absorvidos pelo alvo);
  3. contagem de parâmetros: 1 parâmetro contínuo livre (β) + 1 alvo = 0 graus de
     liberdade de teste. Sem predição excedente, o ajuste é não-falsificável.
- **"identificável"** exigiria β fixado por derivação independente do alvo (nenhuma
  encontrada no núcleo; se existir, citar file:line). Caso contrário:
  **"não-identificável (tuning)"** — e o rótulo "0,003% error" é adjudicado como
  artefato de arredondamento do próprio ajuste (β citado com 3-4 dígitos), não como
  acurácia preditiva.
- "consistente como formulado" não se aplica no sentido de σ (o ajuste é exato por
  construção); o veredito de consistência avaliará apenas se a ARITMÉTICA interna
  confere (Ω^1.033 ≈ 137,04?) e será reportado como tal.

### Plano de fetch

- CODATA via NIST: https://physics.nist.gov/cgi-bin/cuu/Value?alphinv (valor corrente
  CODATA de α⁻¹ com incerteza). Inacessível → reportado inacessível.

---

## Sub-alegação (c): bounce, ξ=100 → n_s = 0,967, N = 61,7 ("Planck compatible")

### Fonte exata no núcleo

- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:160-167` (tabela "Inflation Optimization"):
  > `| 1 | 9.4 | 0.893 | Insufficient |`
  > `| 10 | 18.5 | 0.946 | Insufficient |`
  > `| **100** | **61.7** | **0.967** | **TARGET** ✅ |`
  > `| 1000 | 133.3 | 0.985 | Over-inflated |`
  > `**Critical Discovery:** ξ = 100 produces N = 61.7 > 60 (solves horizon problem) with n_s ≈ 0.965 ± 0.004 (Planck compatible).`
- `01_TAMESIS_CORE/01_Foundation/Theoretical_Labs/Bounce_Cosmology/src/scan_xi.py:46`:
  > `xis = [1.0, 10.0, 100.0, 1000.0, 3000.0, 5000.0, 10000.0]`
  (varredura explícita de ξ; seleção do que produz N na janela desejada).
- `.../Bounce_Cosmology/src/optimize_inflation.py:97-99`:
  > `# Target values` / `N_target = 60.0` / `ns_target = 0.965`
  e linhas 92-95: `n_s = 1 - 2/N` (limite Starobinsky/Higgs) com o comentário
  > `Então, se conseguirmos N=60, teremos n_s correto automaticamente para modelos tipo Starobinsky.`
- `.../Bounce_Cosmology/README.md:71,292-293`: mesma tabela; critério "ns 0.965 ± 0.005".

### Critérios de decisão (pré-declarados)

- **σ de concordância:** computar |n_s_claim − n_s_Planck|/σ_Planck com o valor
  Planck 2018 buscado com proveniência (esperado da ordem de 0,96xx ± 0,004x; o número
  exato virá do fetch, não desta nota). Consistência ≤2σ é condição NECESSÁRIA mas não
  suficiente para "consistente como formulado", porque o rótulo interno é de
  DESCOBERTA ("Critical Discovery", "TARGET ✅").
- **Identificabilidade:** n_s é "predição" apenas se ξ (e portanto N) foi fixado
  independentemente do alvo. Evidência interna a adjudicar: (i) ξ foi varrido em grade
  {1,10,100,1000,3000,5000,10000} e 100 selecionado por dar N>60 — rotulado "TARGET"
  na própria tabela; (ii) n_s = 1 − 2/N é consequência algébrica de N no limite
  Starobinsky — logo, tunar N≈60 fixa n_s≈0,967 automaticamente (o próprio código o
  diz). Se ambos confirmados, veredito: **"não-identificável (tuning)"** — n_s é
  consequência da seleção de ξ contra o alvo N>60, não predição. Registrar também que
  n_s=1−2/N para N=60 dá 0,9667 para QUALQUER modelo da classe Starobinsky — o valor
  não discrimina o mecanismo de bounce alegado.

### Plano de fetch

- Planck 2018 results VI (arXiv:1807.06209 / A&A 641 A6): n_s (TT,TE,EE+lowE+lensing).
  Fonte primária: arxiv.org abstract ou página da A&A; alternativa: wiki oficial Planck
  (ESA). Inacessível → reportado inacessível.

---

## Sub-alegação (d, oportunista): ρ_Λ ~ 1/L_H² — "CONFIRMED" com desvio ×1,46 (46%)

### Fonte exata no núcleo

- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:360-371`:
  > `### 2.8 Vacuum Catastrophe Solution (lambda/)`
  > `| **Hypothesis** | ρ_Λ ~ 1/L_H² (not M_p⁴) |`
  > `| **Status** | ✅ **CONFIRMED** |`
  > `| Observed | 5.8×10⁻²⁷ | Reference |`
  > `| **Holographic** | **8.5×10⁻²⁷** | **×1.46** |`
- `RESEARCH_RESULTS.md:32`: mesma linha na tabela-resumo ("**46%**").
- Auditoria interna já existente: `.../Cosmology/lambda/AUDITORIA.md:3` — "A
  coincidencia de ordem de grandeza nao resolve o problema da constante cosmologica."

### Critérios de decisão (pré-declarados)

- Busca no arquivo por QUALQUER tolerância pré-declarada sob a qual 46% contaria como
  confirmação (grep por "tolerân", "tolerance", "threshold", "criteri" nos diretórios
  lambda/ e adjacentes). Se nenhuma for encontrada: veredito
  **"inconsistente como formulado"** — "CONFIRMED" sem tolerância pré-declarada, com
  desvio de 46% e incerteza observacional de ρ_Λ da ordem de ~1-2% (Planck), é rótulo
  indevido; o máximo defensável seria "ordem de grandeza correta", que é o que a
  própria AUDITORIA.md interna já diz. O σ formal (|8,5−5,8|/σ_obs) será computado com
  a incerteza de ρ_Λ derivada de Planck 2018 (Ω_Λ, H₀) se o fetch (c) a fornecer; caso
  contrário, reportado como ordem de grandeza apenas.
- Identificabilidade: registrar se há fator O(1) livre na construção 1/L_H² (cutoff,
  escolha de horizonte) — conforme a própria AUDITORIA.md interna aponta.

---

## Protocolo comum (todas as sub-alegações)

1. Nenhum valor de referência digitado de memória: TODOS via WebFetch/WebSearch com
   URL + data de acesso + valor citado literalmente em `PROVENANCE.md`. Fonte
   inacessível = reportada inacessível (a sub-adjudicação fica "não adjudicável por
   referência inacessível", nunca substituída).
2. Cálculos em script único auditável (`adjudicate_constants.py`), saída em
   `adjudication_results.json` + log. Aritmética exata (fractions/decimal onde couber).
3. Máximo um adendo datado e delimitado a esta nota; nenhuma revisão silenciosa.
4. Qualquer sub-alegação que SOBREVIVER (veredito ≠ refutado nos dois eixos) →
   recomputação independente por segunda rota + flag para reprodução adversarial no
   nível do orquestrador.
5. Sem commit/push; sem edição de governança; computação em foreground.
6. Vocabulário máximo de veredito: "consistente/inconsistente como formulado" +
   "identificável/não-identificável (tuning)". Nenhuma alegação física mais ampla,
   positiva ou negativa.

*Fixado em 2026-08-21, antes de qualquer fetch de referência.*
