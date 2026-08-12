# Proveniência de dados — DISC-COSMOLOGY-MOND-SPARC-002 (pivotado)

## Dado de curvas de rotação e catálogo

Reaproveitado sem modificação de
`02_TESTS/COSMOLOGY_MOND_SPARC/data/` — mesma proveniência documentada lá
(`SPARC_Lelli2016c.mrt`, sha256
`5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`;
`Rotmod_LTG/*.dat`, 175 arquivos). Nenhum novo download foi necessário.

## Split discovery/holdout (novo nesta pasta)

- **Arquivo:** `discovery_holdout_split.json`
- **sha256:** `1ce2d16090ff717fca57367c3b747d6e29a36572418b4e7666ebd40e233493da`
- **Gerado por:** `random.Random(20260812).shuffle` (seed = data de lock,
  YYYYMMDD) sobre a lista ordenada dos 175 nomes de galáxia do catálogo
  real, primeiros 55 pós-shuffle para holdout, restantes 120 para
  descoberta. Script exato usado para gerar (não versionado
  separadamente, reproduzível a partir do seed declarado):

  ```python
  import random
  names = sorted(...)  # 175 nomes do catalogo real, ordem alfabetica
  r = random.Random(20260812)
  shuffled = names[:]
  r.shuffle(shuffled)
  holdout = sorted(shuffled[:55])
  discovery = sorted(shuffled[55:])
  ```

- **Data de geração:** 2026-08-12, antes de qualquer cálculo de
  `g_bar`/`g_obs`/`g†` sobre os dados.

## Fórmula de aceleração baryônica e escala g† (fonte externa, verificada por fetch)

- McGaugh, S. S., Lelli, F. & Schombert, J. M. (2016). "The Radial
  Acceleration Relation in Rotationally Supported Galaxies." *Physical
  Review Letters*, 117, 201101. arXiv:1609.05917.
- Verificado por `WebFetch` direto em 2026-08-12 (arXiv abstract + versão
  ar5iv.labs.arxiv.org/html/1609.05917) e `WebSearch` cruzada para a
  convenção de quadratura com preservação de sinal
  ($V_{\text{gas}}$ pode ser negativo).
- $\Upsilon_{\text{disk}}=0{,}50$, $\Upsilon_{\text{bul}}=0{,}7$
  $M_\odot/L_\odot$ (3,6 μm); $g^\dagger_{\text{literatura}} =
  1{,}20\pm0{,}02\text{(stat)}\pm0{,}24\text{(sys)} \times10^{-10}$ m/s².
  Usado apenas como checagem de sanidade (Seção 5 do
  `PREREGISTRATION.md`), não como parte do critério de decisão entre H_A
  e H_B.
