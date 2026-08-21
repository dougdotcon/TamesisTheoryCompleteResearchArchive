# Proveniência dos dados de referência — frente `knot-quark-mass`

Data dos fetches: 2026-08-21. Nenhum valor digitado de memória.

## 1. Ropelength de nós ideais (fonte independente)

- **Fonte primária tentada:** KnotInfo (knotinfo.math.indiana.edu) —
  **INACESSÍVEL** do ambiente (DNS: `getaddrinfo ENOTFOUND
  knotinfo.math.indiana.edu`, 2026-08-21). Registrado como inacessível,
  conforme METHODOLOGY_NOTE.md; fonte alternativa pré-listada usada.
- **Fonte usada:** T. Ashton, J. Cantarella, M. Piatek, E. Rawdon,
  *Knot Tightening By Constrained Gradient Descent*, Experimental
  Mathematics 20(1):57–90, 2011 — PDF baixado de
  **https://arxiv.org/pdf/1002.1723** em 2026-08-21 (2.442.095 bytes,
  `%PDF-1.4`), cópia local `data/acpr_1002.1723.pdf`.
- **O que foi extraído:** Tabelas 3–4 (Apêndice A, páginas 38–39 do PDF,
  índices 37–38 zero-based), coluna **Rop** (limite superior de
  ropelength suave), para todos os NÓS primos (1 componente) de 3 a 9
  cruzamentos — 84 nós. Elos (multicomponente, com sobrescrito) foram
  excluídos pelo parser (`parse_acpr.py`); dedupe de linhas repetidas na
  quebra de coluna/página.
- **Convenção:** Rop = Len/Thi com espessura = raio unitário
  (ropelength padrão, L/r). O arquivo Tamesis usa L/D = Rop/2.
  A conversão é afim em x e **não altera R²** (registrado na nota de
  metodologia).
- **Valores-âncora extraídos (conferidos visualmente na página 38 do PDF):**
  - 3_1: Rop = 32.7436 → L/D = 16.3718
  - 4_1: Rop = 42.0887 → L/D = 21.0444
  - 5_1: Rop = 47.2016 → L/D = 23.6008
  - Tabela completa: `data/knot_ropelength_acpr.json` (gerada por
    `parse_acpr.py`, com verificação de contagem = 84).
- **Confirmação cruzada do valor do trefoil:** busca web 2026-08-21
  (Pieranski, SONO: L∞ = 32.742950 ± 0.000001 para 3_1; arXiv:1402.5760
  "High resolution portrait of the ideal trefoil knot") — consistente com
  32.7436 de ACPR.
- **Nota sobre a citação do arquivo:** `knot_mass_fit.py:17` cita
  "Pieranski, S. (1998). Ideal Knots" sem página/DOI. Os valores do
  arquivo (16.37, 21.17, 23.55) NÃO coincidem exatamente com ACPR/2
  para 4_1 (21.17 vs 21.0444) e 5_1 (23.55 vs 23.6008); coincidem para
  3_1 (16.37 vs 16.3718). Discrepâncias documentadas no RESULTS_SUMMARY.

## 2. Massas de quarks (PDG)

- **Fonte:** Particle Data Group, *Summary Tables — Quarks*, 2025 update
  (S. Navas et al., Phys. Rev. D 110, 030001 (2024) and 2025 update),
  PDF baixado de **https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf**
  em 2026-08-21 (49.062 bytes, criado 2025-05-30 segundo o rodapé),
  cópia local `data/rpp2025-sum-quarks.pdf`.
- **Valores extraídos (texto integral do PDF):**
  - m_u = 2.16 ± 0.07 MeV — MS-bar, µ = 2 GeV
  - m_d = 4.70 ± 0.07 MeV — MS-bar, µ = 2 GeV
  - m_s = 93.5 ± 0.8 MeV — MS-bar, µ = 2 GeV
  - m_c = 1.2730 ± 0.0046 GeV — MS-bar, m_c(m_c)
  - m_b = 4.183 ± 0.007 GeV — MS-bar, m_b(m_b)
  - m_t (direct measurements) = 172.56 ± 0.31 GeV
  - m_t (pole, from cross-section) = 172.4 ± 0.7 GeV [sensibilidade]
  - m_t (MS-bar, from cross-section) = 162.5 +2.1/−1.5 GeV [sensibilidade]
- **Nota honesta de esquema/escala (pré-declarada):** as massas leves
  (u,d,s) são MS-bar a 2 GeV; c e b são MS-bar na própria escala; o top
  "direto" é uma massa tipo-Monte-Carlo. Misturar esses números num único
  "M" — como o arquivo faz — é uma escolha de convenção não declarada na
  fonte primária Tamesis; qualquer "lei" M(L/D) herda essa ambiguidade.
  A combinação primária do teste replica a escolha implícita do arquivo
  (u,d,s @ 2 GeV; m_c(m_c); m_b(m_b); top direto), com sensibilidade ao
  esquema do top reportada.

## 3. Dados do próprio arquivo (fonte primária da alegação)

- `01_TAMESIS_CORE/02_Experimental_Validation/Particle_Physics/quarks/simulation/knot_mass_fit.py`
  linhas 22 (L/D), 32 (up-type), 38 (down-type) — commit corrente do repo.
- Alegação R²>0.99: `.../quarks/index.html:333` (setor up) e
  `01_TAMESIS_CORE/RESEARCH_RESULTS.md:341-344` (ambos os setores,
  "CONFIRMED").
