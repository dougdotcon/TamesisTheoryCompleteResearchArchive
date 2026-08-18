# Resultado do fechamento dos gaps — `entropia-de-permutacao` (Entropia de Permutação Multiescala + Plano Complexidade-Entropia)

**Data:** 2026-08-18. Metodologia fixada em `METHODOLOGY_NOTE.md` (commit
`ca3ba7f`) e pipeline (`analysis/pe_common.py`, coarse-graining de blocos
não sobrepostos + embedding ordinal de Bandt-Pompe (`m=4` fixo) +
`I(X)`=`H_S`/`PCI` + `C_JS`/`MCI` + substitutos IAAFT como teste PRIMÁRIO)
validada contra dado sintético ANTES de qualquer cálculo real (commits
`4f89ed4`, `a17ac29` — ver `VALIDATION_NOTE.md`). Aplicada SEM MODIFICAÇÃO
aos 2 domínios da Fase 0.6 (indução de anestesia via EEG, VitalDB;
episódio isquêmico transitório via ECG, PhysioNet European ST-T Database).

## Validação — recapitulação

Ao contrário da hipótese a priori assimétrica de `METHODOLOGY_NOTE.md`
(`C_JS` teria poder, `H_S` talvez não, como `alpha` do DFA), a validação
sintética encontrou que **os DOIS canais têm poder real e completo contra
IAAFT** no controle positivo (mapa logístico `r=4`: `p_PCI=0,0`
`sigma≈-12,4`; `p_MCI=0,0` `sigma≈+10,6`), calibração correta no controle
negativo (mesmo `H`), e — no controle adicional de Hurst diferencial
pedido pela sessão orquestradora (`H=0,3` vs. `H=0,9`, sem conteúdo
não-linear) — **nenhum dos dois canais mostrou significância espúria**
(`p=1,0` em ambos). Ver `VALIDATION_NOTE.md` para a discussão completa.

## Correção de desempenho encontrada e corrigida durante o passo de dado real

Ao aplicar `run_pe_analysis` aos domínios reais (segmentos de até
1.217.103 amostras), um bug de desempenho foi descoberto: os substitutos
IAAFT estavam sendo gerados a partir da série bruta (NÃO subamostrada),
em vez de a subamostragem `MAX_N_PER_SEGMENT=20.000` (Gap (d)) ser
aplicada ANTES da geração de substitutos — tornando o protocolo de 200
substitutos × 50 iterações computacionalmente inviável em escala real
(FFT + argsort sobre >1M amostras, repetido 200×2×2 vezes). **Corrigido em
`pe_common.py`** (subamostragem movida para o topo de `run_pe_analysis`,
aplicada UMA VEZ antes de qualquer geração de substituto), mesma
convenção já estabelecida e auditada em `rqa_common.py::run_rqa_analysis`
nesta mesma linha. **Confirmado, reexecutando `validate_synthetic.py`
após a correção, que os resultados da validação sintética são
BIT-IDÊNTICOS aos já relatados** (todas as séries de validação usaram
`N=3.000 < MAX_N_PER_SEGMENT=20.000`, então a subamostragem nunca era
acionada ali — a correção não afeta nenhuma conclusão já reportada da
validação). Isso NÃO é uma reformulação metodológica: é uma correção de
bug de implementação que faz a regra já declarada em Gap (d) valer de
fato para todo o pipeline, não apenas para a contagem de padrões
ordinais. Um resultado (`edb`/robustez) que havia terminado antes da
correção foi descartado e recalculado do zero sob o código corrigido,
para garantir aplicação idêntica em todas as 4 combinações.

## Domínio 1 — VitalDB (indução de anestesia, EEG, caso `408`, canal `BIS/EEG1_WAV`)

| Variante | `PCI` PRE/POST/Δ | `p_PCI` (IAAFT, bicaudal) | `MCI` PRE/POST/Δ | `p_MCI` (IAAFT, bicaudal) |
|---|---|---|---|---|
| Primária | 13,8798 / 13,8782 / **−0,00164** | **0,97** | 0,15596 / 0,15751 / **+0,00155** | **0,99** |
| Robustez | 13,7970 / 13,7992 / **+0,00226** | **0,995** | 0,25963 / 0,25892 / **−0,00071** | **1,0** |

**Sem sinal em nenhuma variante, nenhum canal.** `Δ` reais são
minúsculos (ordem de `10^-3`) e caem bem dentro da distribuição nula
IAAFT em todos os 4 casos.

## Domínio 2 — PhysioNet European ST-T Database (episódio isquêmico, registro `e0103`, canal `MLIII`)

| Variante | `PCI` PRE/POST/Δ | `p_PCI` (IAAFT, bicaudal) | `MCI` PRE/POST/Δ | `p_MCI` (IAAFT, bicaudal) |
|---|---|---|---|---|
| Primária | 13,5056 / 13,0570 / **−0,4486** | **0,275** | 0,62247 / 1,15684 / **+0,53436** | **0,325** |
| Robustez | 13,4165 / 13,2032 / **−0,2132** | **1,0** | 0,73702 / 0,98847 / **+0,25144** | **0,99** |

**Sem sinal significativo em nenhuma variante** (`p<0,05` em nenhum
caso). Nota honesta: a variante primária de EDB tem os `p` mais baixos
das 8 combinações testadas (`p_PCI=0,275`, `p_MCI=0,325`) — ambos os
canais mudam na mesma direção qualitativa prevista intuitivamente para
isquemia (`H_S`/`PCI` cai, `C_JS`/`MCI` sobe, i.e. o sinal fica menos
aleatório/mais complexo-estruturado durante o episódio) e o `Δ_MCI` real
é a maior magnitude relativa observada em qualquer domínio/variante — mas
nenhum dos dois cruza `p<0,05`, e a variante de robustez do MESMO domínio
(POST mais curto, mais próximo da transição) já não reproduz esse `p`
mais baixo (`p_PCI=1,0`, `p_MCI=0,99`). Isso é reportado honestamente como
tendência sub-limiar, não como achado.

## Checagem complementar DFA/wavelet (contexto interpretativo)

**Não acionada** — condicional a "algum canal cruzar significância em
dado real" (instrução da sessão orquestradora), e nenhuma das 8
combinações canal×domínio×variante cruzou `p<0,05`.

## Sobre a checagem adversarial

Nenhuma das 8 combinações (2 domínios × 2 variantes × 2 canais) produziu
um resultado significativo — não há achado a explicar via reexecução
adversarial completa ou descoberta de nulos; uma reexecução cega completa
não foi acionada por proporcionalidade, mesmo espírito de escalada
condicional ao tamanho do efeito já praticado nesta linha (`mse-
multiscale-entropy`, `visibility_graph`).

## Veredito honesto

`entropia-de-permutacao`, como formulado e testado aqui (pipeline
`I(X)`=`H_S`/`PCI`+`C_JS`/`MCI`, sem reformulação por domínio, aplicada a
2 domínios fisiológicos reais distintos), **não produz um invariante
cross-domain significativo em nenhuma das 8 combinações testadas** —
apesar de ter sido o candidato com a validação sintética de PODER mais
limpa e completa de toda esta linha (7 candidatos anteriores incluídos).
Isso reforça, e não contradiz, a interpretação honesta: a validação
sintética confirma que o discriminador (IAAFT) tem poder real para
detectar determinismo não-linear GENUÍNO quando ele existe (mapa
logístico) — o resultado negativo em dado real não pode ser atribuído a
um teste de significância sem poder (como aconteceu com `alpha` do DFA
antes do bootstrap, ou com o embedding do RQA), é consistente com a
mudança fisiológica real PRE→POST simplesmente não ter a assinatura de
determinismo não-linear que `H_S`/`C_JS` foram desenhados para capturar,
nestes 2 domínios/segmentos específicos.

Isso é o 8º candidato desta linha (`DISC-TRI-RG-001`) a terminar sem
produzir um achado cross-domain sobrevivente: 7 anteriores (6 negativos
em dado real + RQA fechado na validação) e agora `entropia-de-permutacao`
negativo em dado real nos 2 domínios testados.

## Arquivos desta etapa

- `analysis/pe_common.py` (pipeline, corrigido — ver seção de correção acima)
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json` (validação sintética)
- `analysis/run_real_domain.py` (executor por domínio/variante)
- `data/prepare_vitaldb.py`, `data/prepare_edb.py` (download + preparação, re-executáveis)
- `data/PROVENANCE_VITALDB.md`, `data/PROVENANCE_EDB.md` (proveniência completa)
- `data/vitaldb_{pre,post}_{primary,robust}.npy`, `data/edb_{pre,post}_{primary,robust}.npy` (segmentos derivados)
- `analysis/result_vitaldb_primary.json`, `analysis/result_vitaldb_robust.json`,
  `analysis/result_edb_primary.json`, `analysis/result_edb_robust.json` (resultados completos)
- `VALIDATION_NOTE.md` (validação sintética completa, incluindo o adendo de Hurst diferencial)

## Estado da linha e próximo passo

`TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md` NÃO foram atualizados por
este agente (decisão de governança/registro final da linha fica com a
sessão orquestradora, mesmo padrão já usado para `RQA`). Reexecução
adversarial independente (passo 7 de `AGENTS.md`) e decisão sobre
próximos passos da linha `DISC-TRI-RG-001` (nova busca, considerar a
linha suficientemente explorada, etc.) ficam pendentes de decisão da
sessão orquestradora.
