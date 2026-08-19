# Resultado do fechamento dos gaps — `evt-hill` (Dinâmica do Índice de Cauda via Estimador de Hill)

**Data:** 2026-08-19. Metodologia fixada em `METHODOLOGY_NOTE.md` (commit
`9c40c41`) e pipeline (`analysis/evt_hill_common.py`, estimador de Hill
com seleção de `k*` via bootstrap simples de MSE + companheiro `xi_MLE`
via GPD/MLE + teste de significância por randomização do ponto de corte,
NÃO IAAFT) validada contra dado sintético (commit `b84c078` — ver
`VALIDATION_NOTE.md`) ANTES de qualquer dado real. Aplicada SEM
MODIFICAÇÃO aos 2 domínios da Fase 0.6 (onda de calor PDX 2021, furacão
Florence/Cape Fear 2018).

## Domínio 1 — PDX (NOAA GHCN-Daily, onda de calor de 2021): NÃO TESTÁVEL, piso de amostra

`n_pre=7.846` dias (2000-2021), `n_post=37` dias (2021-06-25 a
2021-07-31, o limite MAIS GENEROSO permitido pelo Gap (d)). `MIN_N_PER_
SEGMENT=200` (Gap e) **não é atingido** — consequência estrutural
inevitável de combinar a resolução de 1 obs/dia do GHCN-Daily com a
janela de "várias semanas, não dias" que o próprio Gap (d) exige para
evitar circularidade. `run_evt_hill_analysis` retorna
`status=insufficient_samples` honestamente, sem tentativa de contornar
isso ampliando a janela POST além do que Gap (d) já permite. **Domínio
reportado como estruturalmente não testável com esta combinação exata de
resolução temporal e definição de janela — não como resultado
nulo/negativo por ausência de sinal.** Ver
`data/PROVENANCE_PDX.md`/`analysis/result_pdx.json`.

## Domínio 2 — Cape Fear (USGS 02105769, furacão Florence 2018)

`n_pre=6.546` dias (altura de régua diária MÁXIMA, 2000-2018). POST via
regra de recessão mecânica pré-declarada (ver
`data/PROVENANCE_CAPEFEAR.md`): primária (`10%`/3 dias, até
`2018-10-02`, `n=1.695` leituras de 15 min); robustez (`5%`/3 dias, até
`2018-10-10`, `n=2.462`).

| Variante | `xi_Hill` PRE/POST/Δ | `p_xi_Hill` (randomização) | `xi_MLE` PRE/POST/Δ | `p_xi_MLE` (randomização) |
|---|---|---|---|---|
| Primária | 0,0420 / 0,0015 / **−0,0404** | **0,185** | 0,1147 / **−1,0628** / **−1,1775** | 0,09 |
| Robustez | 0,0420 / 0,0017 / **−0,0403** | **0,22** | 0,1147 / −1,0628 / −1,1775 | **0,025** |

(`xi_Hill`/`xi_MLE` de PRE idênticos entre variantes — esperado: PRE é o
MESMO array de dado nas duas variantes, e ambas chamam `run_evt_hill_
analysis` com a MESMA seed, então o PRE — computado primeiro, antes de
qualquer outro sorteio — é bit-idêntico; não é um bug.)

**Canal primário (`xi_Hill`): NÃO significativo em nenhuma variante**
(`p=0,185` e `p=0,22`). Notável: a nula de randomização (Gap f) já vem
DESLOCADA para perto do próprio `Delta` real neste domínio (nula
média≈`−0,038` a `−0,039`, real≈`−0,040`) — o mesmo fenômeno de
deslocamento estrutural da nula já documentado na validação sintética
(`VALIDATION_NOTE.md` seção 3, causado por PRE/POST muito desbalanceado
colocando a transição real perto da borda do intervalo `[0,2;0,8]` do
pool) aparece também em dado real aqui, confirmando que a interpretação
da seção 3 generaliza.

**Canal companheiro (`xi_MLE`): divergente entre variantes** — `p=0,09`
(primária, não sig.) vs. **`p=0,025`** (robustez, sig.). Investigado a
fundo em `analysis/CONFOUND_CHECK_CAPEFEAR.md`: `xi_MLE(POST)=−1,063`
(fortemente negativo, suporte GPD finito em `≈30,68 ft`) reflete um
PLATÔ DE CRISTA DE CHEIA físico real e limitado (observado diretamente
na série bruta, 19-23/09/2018, altura quase constante perto de `30,6-
30,7 ft` antes de recessar) — não uma cauda de lei de potência mais
pesada. `xi_Hill` concorda QUALITATIVAMENTE (cai para `≈0`, também
indicando cauda mais LEVE/limitada, não mais pesada) mesmo discordando
em magnitude — a discordância de magnitude entre os dois estimadores
perto de um suporte efetivamente limitado já era um modo de instabilidade
conhecido de `xi_MLE`, documentado na validação sintética ANTES de
qualquer dado real ser tocado (`VALIDATION_NOTE.md` seção 1).

## Checagem de confundidor de comporta (Lock 1) — ACIONADA, ver `analysis/CONFOUND_CHECK_CAPEFEAR.md`

Acionada porque `p_xi_MLE<0,05` na variante de robustez. Log operacional
completo da comporta NÃO encontrado publicamente (limitação de dado
declarada, não escondida). Evidência circunstancial disponível PESA
CONTRA um confundidor de operação de comporta: a estrutura ficou
COMPLETAMENTE SUBMERSA durante o pico da cheia (documentado
fotograficamente pelo DVIDS/Departamento de Defesa dos EUA), sem
monitoramento ativo durante o período crítico (reportagem local,
dez/2018) — uma vez submersa, a comporta deixa de ser o fator
hidraulicamente dominante. O padrão observado (platô de crista limitada)
é exatamente o que a física de uma cheia fluvial real produziria
independente de qualquer comporta. Nenhuma leitura USGS no pico está
marcada como estimada/com defeito de equipamento.

## Veredito honesto

**`xi_Hill` (canal primário, de decisão): NEGATIVO nos 2 domínios** — PDX
estruturalmente não testável (piso de amostra), Cape Fear sem
significância em nenhuma variante de janela (`p=0,185`/`0,22`), com a
nula de randomização já mostrando o mesmo deslocamento estrutural
identificado na validação sintética. `xi_MLE` (canal companheiro) mostra
um `p<0,05` em UMA de duas variantes em Cape Fear, mas investigado e
explicado por um efeito físico plausível e parcimonioso (plateau de
crista de cheia limitada, refletido como suporte GPD finito) mais um
modo de instabilidade de `xi_MLE` já conhecido e documentado ANTES de
qualquer dado real — não reportado como achado cross-domain genuíno.

`evt-hill`, como formulado e testado aqui (`xi_Hill` via estimador de
Hill com seleção automatizada de `k*`, `xi_MLE` companheiro via GPD/MLE,
teste de significância por randomização do ponto de corte), **não
produz um invariante cross-domain sobrevivente** — consistente com o
padrão dos 9 candidatos anteriores desta linha (`DISC-TRI-RG-001`), e
o único dos 2 domínios desta rodada que pôde de fato ser testado
(Cape Fear; PDX não foi testável por piso de amostra estrutural, não
por ausência de sinal) terminou negativo no canal primário. Isto é o
10º candidato desta linha a terminar sem produzir um achado cross-domain
sobrevivente.

## Arquivos desta etapa

- `analysis/evt_hill_common.py` (pipeline, LOCKED sem modificação desde
  a validação sintética)
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`,
  `VALIDATION_NOTE.md` (validação sintética completa, incl. o achado de
  deslocamento estrutural da nula do Gap (f))
- `analysis/soc_redundancy_check.py`, `analysis/soc_redundancy_check.json`
  (checagem de redundância com SOC, Gap c)
- `analysis/run_pdx.py`, `analysis/result_pdx.json`,
  `data/pdx_tmax_raw.json`, `data/PROVENANCE_PDX.md` (domínio 1)
- `analysis/run_capefear.py`, `analysis/result_capefear.json`,
  `data/capefear_pre_dailymax.json`, `data/capefear_post_instant_wide.json`,
  `data/PROVENANCE_CAPEFEAR.md` (domínio 2)
- `analysis/CONFOUND_CHECK_CAPEFEAR.md` (checagem de confundidor de
  comporta, acionada pelo Gap (d))

## Estado da linha e próximo passo

`TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md` NÃO foram atualizados por
este agente (decisão de governança/registro final da linha fica com a
sessão orquestradora, mesmo padrão já usado para os candidatos
anteriores desta linha). Reexecução adversarial independente (passo 7 de
`AGENTS.md`) fica pendente de decisão da sessão orquestradora — nenhuma
das duas checagens obrigatórias (piso de amostra em PDX, confundidor de
comporta em Cape Fear) encontrou um achado forte o bastante para exigir
escalada adicional por proporcionalidade (mesmo critério já usado nos
candidatos anteriores desta linha), mas ambas ficam documentadas in
extenso para quem quiser reexecutar de forma independente.
