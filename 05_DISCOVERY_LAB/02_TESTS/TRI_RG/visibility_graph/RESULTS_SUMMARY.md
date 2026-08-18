# Resultado do fechamento dos gaps — `grafo-de-visibilidade`

**Data:** 2026-08-18. Metodologia fixada em `METHODOLOGY_NOTE.md` (commit
`9bc22a1`) e pipeline (`analysis/vg_common.py`, grafo de visibilidade natural
+ box-covering CBB + `d_B`+`C` + substitutos IAAFT como teste PRIMÁRIO)
validada contra dado sintético (commit `ad36e03`, `VALIDATION_NOTE.md`) ANTES
de qualquer cálculo real. Aplicada sem modificação aos 2 domínios
(geomagnetismo, hidrologia).

## Validação — achado decisivo sobre os dois canais

A validação sintética obrigatória (Gap (b)) revelou um resultado assimétrico
entre os dois canais de `I(X)`, mais fundamental que o padrão de baixo poder
já visto em `dfa-multiscale-entropy`:

- **`d_B` (box-covering, canal primário original):** ESTRUTURALMENTE NÃO
  COMPUTÁVEL sob a própria grade a priori do Gap (a)
  (`l_B_max=floor(diam(G)/4)`, mínimo 4 escalas, ou seja `diam(G)>=20`).
  Grafos de visibilidade de séries estocásticas típicas são "small-world"
  (diâmetro cresce só como `~log(N)`, medido entre 9 e 19 para `N` de 1.000 a
  15.000), nunca alcançando o piso de 20 dentro do teto
  `MAX_N_PER_SEGMENT=5.000` do Gap (d). Não é bug — um diagnóstico com série
  determinística de diâmetro grande confirma que o código de box-covering/CBB
  /ajuste OLS funciona corretamente quando a grade é atingível
  (`d_B=1,899`). Um substituto de bootstrap por blocos móveis (pré-
  autorizado no Gap (e) para o padrão de baixo poder do DFA-alpha) foi
  testado empiricamente (25 reamostras de cada segmento do controle
  positivo) e **não resolve** o problema, porque não é de poder estatístico
  — é de topologia do grafo (25/25 reamostras continuaram
  `insufficient_scales`).
- **`C` (clustering, canal companheiro):** validado com PODER REAL forte —
  controle positivo (ruído branco vs. mapa logístico caótico, marginal/
  espectro casados por remapeamento de posto) recuperou `Delta_C` fora da
  distribuição nula IAAFT por **~14,55 desvios-padrão** (`p_C=0,0`, `n=200`
  substitutos); controle negativo (dois processos lineares idênticos)
  corretamente não significativo (`p_C=0,25`).

Ver `VALIDATION_NOTE.md` para a discussão completa. Decisão, fixada ANTES de
qualquer dado real: `d_B` retirado do critério de decisão desta rodada
(mantido apenas como diagnóstico reportável); `C` promovido a `I(X)` único.

## Domínio 1 — Geomagnetismo (índice SYM-H, tempestade de 17/03/2015, NASA/SPDF OMNIweb)

Estação/fonte: `data/omni_5min2015.asc` (ano completo 2015, 5 min, 105.120
amostras, sem lacuna). SSC verificado em 04:45 UT (Kamide & Kusano 2015).
Próximo evento documentado: tempestade de 22-25/06/2015. Ver
`data/PROVENANCE.md` para URLs exatas e verificação de sanidade (SYM-H
mínimo do arquivo = −233 nT, bate com o −234 nT documentado na literatura).

| Variante | n usado (PRE/POST, pós-subamostragem) | diam PRE/POST | status `d_B` | `C` PRE | `C` POST | `Δ_C` | `p_C` (IAAFT, bicaudal) |
|---|---|---|---|---|---|---|---|
| Primária | 4.332 / 4.647 | 13 / 10 | insufficient_scales | 0,7094 | 0,7078 | −0,00162 | 0,780 |
| Robustez | 3.610 / 4.647 | 11 / 12 | insufficient_scales | 0,6957 | 0,6910 | −0,00465 | 0,595 |

**Sem sinal em nenhuma variante.** `Δ_C` real cai bem dentro da distribuição
nula dos substitutos IAAFT em ambas — a mudança de clustering observada é
inteiramente consistente com o que um processo linear com o mesmo espectro/
amplitude já produziria.

## Domínio 2 — Hidrologia (altura de régua, furacão Harvey/2017, USGS NWIS)

Estação: USGS 08074500, Whiteoak Bayou at Houston, TX (parâmetro 00065, gage
height em pés). PRE = 2007-10-01 a 2017-08-24 (334.289 leituras de 15 min,
início do registro instantâneo contínuo documentado pelo catálogo de séries
da própria USGS). POST = 2017-08-25 até o final do registro contínuo
disponível no momento desta sessão (2026-08-17, 313.063 leituras). Pico real
recuperado no POST = **44,31 pés exatos** em 2017-08-27, batendo dígito a
dígito com o valor de pico anual oficial da USGS e com o número já citado em
`METHODOLOGY_NOTE.md` — confirma estação/parâmetro/período corretos. Ver
`data/PROVENANCE.md`.

| Variante | n usado (PRE/POST, pós-subamostragem) | diam PRE/POST | status `d_B` | `C` PRE | `C` POST | `Δ_C` | `p_C` (IAAFT, bicaudal) |
|---|---|---|---|---|---|---|---|
| Primária | 5.000 / 5.000 | 9 / 9 | insufficient_scales | 0,8169 | 0,8188 | +0,00188 | 0,995 |
| Robustez | 5.000 / 5.000 | 10 / 9 | insufficient_scales | 0,8064 | 0,8082 | +0,00180 | 0,855 |

**Sem sinal em nenhuma variante** — `p_C` entre 0,855 e 0,995, resultado
inequivocamente negativo. Nota: o sinal de `Δ_C` é POSITIVO na hidrologia e
NEGATIVO no geomagnetismo — nenhuma consistência direcional cross-domain,
reforçando a ausência de um padrão genuíno (mesmo se algum `p` individual
fosse limítrofe, o que não é o caso aqui).

## `d_B` nos 4 casos reais — diagnóstico, não achado

Em nenhum dos 4 casos reais (2 domínios × 2 variantes) a grade `l_B` atingiu
o piso de 4 escalas distintas do Gap (a) (diâmetros observados entre 9 e 13,
grades resultantes de 1-2 valores de `l_B` apenas) — exatamente o padrão já
antecipado pela validação sintética. Isso é reportado como
`status="insufficient_scales"` em todos os 4 `result_*.json`, nunca como "sem
mudança de `d_B`" (uma alegação diferente e mais forte que os dados não
sustentam).

## Sobre a checagem adversarial

Como nenhuma das 8 combinações reais testadas (2 domínios × 2 variantes ×
canal `C`, único canal com protocolo de significância validado) produziu
resultado significativo, e `d_B` não foi sequer computável em nenhuma delas,
não há achado a explicar ou refutar — reexecução adversarial completa e
busca de nulo dedicada não foram acionadas, por proporcionalidade (mesmo
princípio já usado com sucesso em `mse-multiscale-entropy`, onde 8/8
combinações não-significativas também dispensaram essa etapa).

## Veredito honesto

`grafo-de-visibilidade` (redesenhado com `C` como canal único de decisão
após o achado de não-computabilidade estrutural de `d_B`, decisão tomada
ANTES de qualquer dado real), como formulado e testado aqui, **não produz um
invariante cross-domain confiável** — mesmo veredito já obtido para os
outros 5 candidatos desta linha. Diferente de `dfa-multiscale-entropy` e
`soc-avalanches`, aqui não houve achado inicial promissor em nenhum domínio
isolado — o resultado é negativo de forma limpa nos 2 domínios, mesmo padrão
de `mse-multiscale-entropy`. Isso não invalida o clustering de grafo de
visibilidade como ferramenta (validado com poder real forte no controle
sintético), nem a própria dimensão de box-covering como conceito (o código
funciona corretamente quando a grade é atingível) — mostra apenas que, sob a
convenção de grade fixada a priori e o teto de subamostragem `O(N²)` desta
linha, `d_B` não é aplicável a séries temporais reais de comprimento
tratável, e `C` não separa PRE de POST nestes 2 domínios específicos com o
protocolo genuinamente cego ao domínio aplicado aqui.

## Estado da linha — 6 dos 6 candidatos considerados com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| `mse-multiscale-entropy` | Geomagnetismo (1989), rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |
| `grafo-de-visibilidade` | Geomagnetismo (2015), hidrologia/Harvey | NEGATIVO (sem achado em nenhum domínio; `d_B` estruturalmente não testável) |

Todos os 6 candidatos originais da linha `DISC-TRI-RG-001` agora têm
resultado completo — 6/6 negativos (2 com achados isolados de 1 domínio já
explicados por mecanismo convencional/nulo, refutando a hipótese TRI/TDTR
como explicação). Nenhum `PREREGISTRATION.md` foi escrito, seguindo o mesmo
padrão já usado nos 5 candidatos anteriores desta linha de fechamento
exploratório de gaps (ver `METHODOLOGY_NOTE.md`, "O que este passo NÃO é").
