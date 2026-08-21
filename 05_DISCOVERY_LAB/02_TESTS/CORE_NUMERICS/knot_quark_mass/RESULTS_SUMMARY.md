# Resultados — frente `knot-quark-mass` (DISC-CORE-NUMERICS-001)

**Data:** 2026-08-21.
**Alegação testada:** `M ∝ exp(α·L/D)` com nós ideais atribuídos por
geração (3_1, 4_1, 5_1) e `R² > 0,99` alegado
(`.../Particle_Physics/quarks/index.html:333`,
`01_TAMESIS_CORE/RESEARCH_RESULTS.md:341-344`, status "CONFIRMED").
Critérios pré-declarados em `METHODOLOGY_NOTE.md` ANTES de qualquer
ajuste; dados de referência com proveniência em `PROVENANCE.md`;
números completos em `results.json` / `analysis.log`.

## VEREDITO: NÃO SOBREVIVE à validação como formulado

Falha nos **quatro** critérios pré-declarados, inclusive na simples
reprodução do R² alegado com os números do próprio arquivo.

| Critério | Resultado | Passa? |
|---|---|---|
| (i) Reprodução com dados do arquivo | α_up=1.535, α_down=0.900 reproduzem; **R²_up=0.9861, R²_down=0.9348 — nenhum é > 0.99** | **NÃO** |
| (ii) Reajuste com dados independentes (ACPR + PDG 2025) | R²_up=0.9915 > 0.99, mas **R²_down=0.9452 << 0.99** (a alegação de RESEARCH_RESULTS.md é para ambos) | **NÃO** |
| (iii) Leave-one-out (exigido pela própria AUDITORIA.md) | 5 de 6 predições falham o limiar de 0.5 dex; erros de fator 2.5× a 52× | **NÃO** |
| (iv) Nulo de permutação (atribuição de nós) | Percentil 86 (up) e 70 (down) no nulo monotônico — abaixo do limiar pré-declarado de 95 | **NÃO** |

## Achado central sobre a origem do "R² > 0,99"

O script do arquivo (`knot_mass_fit.py`) **nunca computa R²** — o número
só existe como texto no HTML e no RESEARCH_RESULTS.md. Com os próprios
vetores do arquivo, o ajuste log-linear dá R² = 0.9861 (up) e 0.9348
(down). A explicação mais provável do "0.99": o coeficiente de
**correlação de Pearson** do setor up é r = 0.9930 — r foi aparentemente
reportado como R². Mesmo sob essa leitura caridosa, a alegação de
RESEARCH_RESULTS.md de R² > 0.99 para o setor **down** é falsa sob
qualquer definição (r_down = 0.9668, r² = 0.9348).

## Detalhes por critério

### (i) Reprodução (dados do arquivo: L/D = 16.37, 21.17, 23.55; massas de knot_mass_fit.py:32,38)

- α_up = 1.5346, M0 = 2.11e-11 MeV; α_down = 0.8995 — batem com o
  alegado (1.53 / 0.90): o ajuste é reproduzível.
- R² (log-espaço): up 0.9861, down 0.9348 — **a alegação R²>0.99 não se
  reproduz nem com os números do próprio arquivo.**

### (ii) Dados independentes

- Ropelength ACPR (arXiv:1002.1723, Tabelas 3–4): L/D = 16.3718 (3_1),
  21.0444 (4_1), 23.6008 (5_1). Os valores do arquivo divergem da fonte
  para 4_1 (21.17 vs 21.04) e 5_1 (23.55 vs 23.60); a citação do arquivo
  ("Pieranski, S. (1998)") é incompleta e não confere no detalhe.
- Massas PDG 2025: u 2.16, d 4.70, s 93.5, c 1273.0, b 4183, t 172560
  (direta) MeV. Esquemas mistos (MS-bar 2 GeV / m_q(m_q) / massa direta)
  — ambiguidade que a "lei" nunca declara.
- Resultado: R²_up = 0.9915 (por pouco acima de 0.99 — e note que isso é
  3 pontos, 2 parâmetros, 1 grau de liberdade), R²_down = 0.9452.
  Sensibilidade ao esquema do top: R²_up ∈ [0.9915, 0.9921] (direta,
  pole, MS-bar) — o critério down é o decisivo e falha longe.

### (iii) Leave-one-out (dados independentes; limiar pré-declarado 0.5 dex)

| Setor | Excluído | M_obs (MeV) | M_pred (MeV) | Erro (dex) | Fator |
|---|---|---|---|---|---|
| up | u | 2.16 | 0.161 | −1.13 | 13.4× | 
| up | c | 1273 | 3186 | +0.40 | 2.5× |
| up | t | 172560 | 41741 | −0.62 | 4.1× |
| down | d | 4.70 | 0.090 | −1.72 | 52.3× |
| down | s | 93.5 | 379 | +0.61 | 4.1× |
| down | b | 4183 | 480 | −0.94 | 8.7× |

5/6 predições falham (com os números do próprio arquivo: 6/6). O modelo
que o arquivo usa para "prever" uma 4ª geração a ~100 TeV erra o top
conhecido por fator 4 e o quark d por fator 52 quando obrigado a prever
em vez de ajustar. A validação que a AUDITORIA.md exigia, agora feita,
é negativa.

### (iv) Nulo de permutação (84 nós primos de 3–9 cruzamentos, ACPR)

- Nulo A (100.000 triplas injetivas ordenadas, seed 12345): a atribuição
  alegada fica no percentil 95.9 (up) / 89.4 (down).
- Nulo B (triplas monotônicas em L/D — a única restrição que a motivação
  do arquivo impõe): percentil **86.0 (up)** e **70.3 (down)**;
  **14.9%** das triplas monotônicas dão R²_up > 0.99 e 12.2% dão
  R²_down > 0.99. Enumeração completa (95.284 triplas) confirma
  (86.2 / 70.4).
- Ou seja: dentro do espaço de escolhas que o próprio modelo permite, a
  atribuição (3_1, 4_1, 5_1) não é nem excepcional — cerca de 1 em 7
  atribuições monotônicas alternativas ajusta o setor up "melhor que
  0.99". Falha o limiar pré-declarado (percentil 95) nos dois setores.

## Achados colaterais documentados

1. **Mapeamento internamente inconsistente:**
   `01_TAMESIS_CORE/RESEARCH_RESULTS.md:109-113` atribui Charm→5_1 e
   Strange→4_1, contradizendo o mapeamento por geração da área quarks/
   usada no ajuste.
2. **Dados internos inconsistentes:** massa do top 173000 MeV em
   `knot_mass_fit.py:32` vs 172760 MeV em
   `05_Particle_Spectrum/generate_visualizations.py:36`.
3. **Status "CONFIRMED" indevido:** RESEARCH_RESULTS.md:337 marca a
   hipótese como "✅ CONFIRMED" com R²>0.99 em ambos os setores; nenhuma
   das duas coisas resiste ao recálculo. A própria AUDITORIA.md
   (2026-07-29) já rebaixava o resultado a "ajuste fenomenológico
   exploratório" — este teste confirma e quantifica o rebaixamento.
4. **KnotInfo inacessível** do ambiente (DNS); fonte alternativa
   pré-listada (ACPR 2011) usada com verificação cruzada do trefoil
   contra Pieranski/SONO (32.74295).

## Sinalização

Reprodução adversarial de orquestrador: **NÃO requerida** (resultado
negativo; a regra pré-declarada só a exige para achado positivo).

## Arquivos

- `METHODOLOGY_NOTE.md` — critérios pré-declarados (antes de computar).
- `PROVENANCE.md` — fontes, URLs, datas, valores.
- `parse_acpr.py` → `data/knot_ropelength_acpr.json` (84 nós, checks).
- `analysis.py` → `results.json`, `analysis.log`.
- `data/acpr_1002.1723.pdf`, `data/rpp2025-sum-quarks.pdf` — cópias das
  fontes.
