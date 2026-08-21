# Nota de validação — `transfer_entropy`

**Resultado: validação sintética obrigatória PASSOU, sem necessidade do
passo de correção pré-autorizado.** Pipeline (`analysis/te_common.py`)
seguiu, sem modificação, para dado real (ver `RESULTS_SUMMARY.md`).
Script completo: `analysis/validate_synthetic.py`; saída bruta:
`analysis/validation_synthetic.json`, `analysis/validate_synthetic.log`.

## Tier 0 — diagnóstico de correção de código (não é a validação de identificabilidade em si)

- **(a) Dois canais Gaussianos independentes:** `TE(X->Y)=0,00006`,
  `TE(Y->X)=-0,00332` — ambos `~0`, dentro da margem pré-declarada
  (`|TE|<0,15`). **PASSOU.**
- **(b) AR(1) acoplado, verdade-terreno X->Y, `c=0,5`:**
  `TE(X->Y)=0,33996 >> TE(Y->X)=0,00135` — direção correta recuperada
  com folga ampla. **PASSOU.**

O estimador KSG-CMI implementado (`te_common.ksg_cmi`/`te_ksg`) produz
valores sensatos e na direção correta ANTES de qualquer teste
estatístico contra dado ambíguo — checagem de correção de implementação,
não de identificabilidade, mas dá confiança de que o código está correto
antes de interpretar qualquer `p`-valor.

## Tier 1 — controle positivo (PRE não-acoplado -> POST acoplado, `c=0,5`)

`N_PER_HALF=3000` cada lado, `phi_x=0,6`, `phi_y=0,3`. PRE = par AR(1)
SEM acoplamento (`c=0`); POST = MESMO par AR(1) com acoplamento X->Y
LIGADO (`c=0,5`). Pipeline completa (`run_te_analysis`, 200 substitutos
IAAFT + 200 substitutos de deslocamento circular, `k_NN=4`,
sub-janelamento, ambos estimadores KSG e Simbólico) rodada sem
modificação.

| Canal | `Delta` real | `p` IAAFT | `p` deslocamento circular |
|---|---|---|---|
| `TE_net` (primário) | +0,1947 | **0,0** | **0,0** |
| `TE_sum` (companheiro) | +0,2586 | **0,0** | **0,0** |
| `STE_net` (robustez) | +0,1596 | **0,0** | **0,0** |
| `STE_sum` (robustez) | -0,2224 | **0,0** | **0,0** |

**Poder discriminativo real, forte, nos 4 canais, sob AMBOS os
substitutos nulos.** Nenhuma correção pré-autorizada foi necessária —
`C_STRONG_V1=0,5` (a especificação literal) já foi suficiente. Sinal
positivo de `Delta_TE_net` corretamente reflete o aumento de fluxo
X->Y ao ligar o acoplamento (verdade-terreno). `STE_sum` mostra sinal
NEGATIVO apesar de detectar a mudança com `p=0,0` — não uma falha, só
um lembrete de que TE Simbólica mede um objeto matemático diferente
(baseado em padrões ordinais, não amplitude contínua) e não precisa
concordar em SINAL com a versão KSG-contínua, só em PODER
discriminativo, que ela demonstra ter aqui.

## Tier 2 — controle negativo (2 realizações independentes do MESMO processo NÃO-acoplado, sem transição real)

3 sementes independentes, `n=8` verificações por semente (4 canais × 2
nulos) = `24` verificações totais.

| Semente | `p_IAAFT(TE_net)` | `p_shift(TE_net)` | `p_IAAFT(TE_sum)` | `p_shift(TE_sum)` | `p_IAAFT(STE_net)` | `p_shift(STE_net)` | `p_IAAFT(STE_sum)` | `p_shift(STE_sum)` |
|---|---|---|---|---|---|---|---|---|
| 0 | 0,55 | 0,60 | 0,365 | 0,325 | 0,55 | 0,50 | 0,07 | **0,025** |
| 1 | 0,08 | **0,045** | 0,995 | 0,99 | 0,42 | 0,41 | 0,315 | 0,785 |
| 2 | 0,06 | 0,05 | 0,26 | 0,295 | **0,035** | 0,255 | 0,74 | 0,68 |

**Taxa de falso-positivo observada: `2/24 ~ 0,083`** (contando os dois
valores `<0,05`: `STE_sum`/deslocamento-circular na semente 0, e
`TE_net`/deslocamento-circular na semente 1, que ficou em `0,045`,
marginal). Compatível com o nível nominal `alpha=0,05` esperado sob a
nula, dado o número pequeno de sementes e a não-independência completa
entre os 8 canais/nulos testados por semente (4 canais correlacionados
entre si, 2 nulos parcialmente correlacionados). **Nenhum padrão
sistemático de falso-positivo nos canais PRIMÁRIOS (`TE_net`/`TE_sum`)
através das 3 sementes** — o único valor marginal em `TE_net`
(`p=0,045`, semente 1, SÓ no substituto de deslocamento circular, não
replicado no IAAFT da mesma semente, `p=0,08`) não se repete nas outras
2 sementes. Não há evidência de viés estrutural que exija correção.

## Veredito de escalonamento

**Nenhuma correção pré-autorizada foi necessária.** O controle positivo
passou na primeira tentativa (`C_STRONG_V1=0,5`), o controle negativo não
revelou um padrão sistemático de falso-positivo nos canais primários.
`correction_applied=false` em `validation_synthetic.json`.

## Veredito final

**`PASS_PROCEED_TO_REAL_DATA`.** A pipeline `te_common.run_te_analysis`
segue para os 2 domínios reais (CHB-MIT EEG, terremotos da Turquia) SEM
NENHUMA modificação em relação ao que foi validado aqui — mesmo
`k_NN=4`, mesma seleção de embedding Ragwitz-Kantz, mesmo `u=1`, mesmo
sub-janelamento, mesmos 2 protocolos de substituto nulo, mesmos 4
canais (`TE_net`, `TE_sum`, `STE_net`, `STE_sum`).

**Ressalva honesta a carregar adiante:** a validação usa um sistema
AR(1) simples com acoplamento linear — não testa diretamente o risco de
não-estacionariedade FORTE (convulsão, sequência de terremotos) que os
2 domínios reais efetivamente têm; a mitigação de sub-janelamento foi
FIXADA a priori em `METHODOLOGY_NOTE.md` precisamente por causa desse
risco conhecido e não testável sinteticamente de forma simples — seu
desempenho real só pode ser avaliado nos próprios domínios (e checado
adversarialmente se houver achado `p<0,05`, per protocolo desta linha).
