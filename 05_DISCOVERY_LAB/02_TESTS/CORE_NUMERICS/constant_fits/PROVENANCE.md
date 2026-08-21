# Proveniência dos valores de referência — `constant_fits`

Todos os valores abaixo foram obtidos por fetch direto em **2026-08-21** (WebFetch),
nunca de memória. Citações literais entre aspas.

## 1. PDG — sin²θ_W (três esquemas)

### 1a. Tabela de constantes físicas, PDG 2025
- **URL:** https://pdg.lbl.gov/2025/reviews/rpp2025-rev-phys-constants.pdf
- **Acesso:** 2026-08-21 (PDF baixado e texto extraído com pymupdf)
- **Identificação do documento:** "Table 1.1: Revised Sept. 2025 by D. Robinson (LBNL)
  and P.A. Zyla (LBNL). Mainly from 'CODATA recommended values of the fundamental
  physical constants: 2022' "
- **Valor citado (MS-bar):** "weak-mixing angle‡‡ sin2 bθ(MZ) (MS) 0.231 22(6)††"
- **Nota do documento:** "††Derived from sin2 θ for the eﬀective angle ¯s2 ℓ = 0.23154(6)."
- **Também citado:** "7.297 352 5643(11)×10−3 = 1/137.035 999 177(21)" e
  "A world average of the latest data yields α−1 = 137.035 999 178(8)."
- **Massas para checagem on-shell tree-level:** "mW 80.3692(133) GeV/c2", "mZ 91.1880(20) GeV/c2".

### 1b. Review "Electroweak model and constraints on new physics", PDG 2025
- **URL:** https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf
  (localizado via índice https://pdg.lbl.gov/2025/reviews/contents_sports.html)
- **Acesso:** 2026-08-21 (PDF baixado, texto extraído com pymupdf; tabela na pág. de
  índice 22/23 do PDF, "known input parameters and unknown higher orders [106]")
- **Valores citados (tabela de esquemas):**
  - "On-shell s2 W 0.22342 ±0.00009"
  - "Eﬀective angle ¯s2 ℓ 0.23154 ±0.00006"
  - "MS bs 2 Z 0.23122 ±0.00006"

## 2. CODATA/NIST — α⁻¹

- **URL:** https://physics.nist.gov/cgi-bin/cuu/Value?alphinv
- **Acesso:** 2026-08-21
- **Valor citado:** "2022 CODATA recommended value": "137.035 999 177",
  incerteza-padrão "0.000 000 021" — forma concisa "137.035 999 177(21)".

## 3. Planck 2018 — n_s, H₀, Ω_m

- **URL:** https://arxiv.org/abs/1807.06209 (Planck 2018 results. VI. Cosmological
  parameters; publicado como A&A 641, A6 (2020))
- **Acesso:** 2026-08-21
- **Valores citados (abstract, combinação "polarization, temperature, and lensing …
  in combination", 68% CL):**
  - "scalar spectral index $n_s = 0.965\pm 0.004$"
  - "Hubble constant $H_0 = (67.4\pm 0.5)$ km/s/Mpc"
  - "matter density parameter $\Omega_m = 0.315\pm 0.007$"
- **Nota:** o abstract publica n_s com 3 casas (0,965±0,004). O valor de tabela com 4
  casas (TT,TE,EE+lowE+lensing, frequentemente citado como 0,9649±0,0042) não foi
  extraído aqui; a adjudicação usa o valor do abstract, com análise de sensibilidade
  no script mostrando que a conclusão não muda entre as duas formas.

## 4. CODATA/NIST — G (para converter H₀, Ω_m em ρ_Λ em kg/m³)

- **URL:** https://physics.nist.gov/cgi-bin/cuu/Value?bg
- **Acesso:** 2026-08-21
- **Valor citado:** "6.674 30 x 10⁻¹¹ m³ kg⁻¹ s⁻²", incerteza-padrão
  "0.000 15 x 10⁻¹¹" — forma concisa "6.674 30(15) × 10⁻¹¹ m³ kg⁻¹ s⁻²" (CODATA 2022).

## 5. Constantes exatas usadas (definições, não medidas)

- 1 au ≡ 149 597 870 700 m (definição IAU 2012); 1 pc ≡ (648000/π) au;
  logo 1 Mpc = 3.0856775814913673×10²² m (conversão exata, calculada no script).
- c ≡ 299 792 458 m/s (definição SI).

## Fontes internas do arquivo (alegações sob teste) — file:line

- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:31,321-328` (sin²θ_W "CONFIRMED", 0,19%)
- `01_TAMESIS_CORE/02_Experimental_Validation/Particle_Physics/electroweak/README.md:25,31-34`
- `01_TAMESIS_CORE/02_Experimental_Validation/Particle_Physics/electroweak/simulation/torsion_angle.py:15-16`
- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:30,61-62` (α⁻¹ = Ω^β, β=1,033), `:704` (Ω=117,038)
- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:160-167` (tabela ξ; "TARGET ✅"; "Critical Discovery")
- `01_TAMESIS_CORE/01_Foundation/Theoretical_Labs/Bounce_Cosmology/src/scan_xi.py:46`
- `01_TAMESIS_CORE/01_Foundation/Theoretical_Labs/Bounce_Cosmology/src/optimize_inflation.py:89-107`
- `01_TAMESIS_CORE/RESEARCH_RESULTS.md:32,360-371` (Λ "CONFIRMED", ×1,46)
- `01_TAMESIS_CORE/02_Experimental_Validation/Cosmology/lambda/simulation/holographic_lambda.py:76-92`
  (construção ρ_holo e critério "within 1 order of magnitude": `if 0.1 < ratio < 10`)
