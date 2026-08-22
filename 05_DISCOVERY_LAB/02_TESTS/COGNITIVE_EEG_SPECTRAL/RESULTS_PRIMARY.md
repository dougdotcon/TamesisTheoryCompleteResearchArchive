# Resultado primário — Assinatura Espectral em Depressão (Mumtaz MDD vs. HC)

**Test ID:** `DISC-COGNITIVE-EEG-SPECTRAL-001` (braço depressão)
**Pré-registro (LOCKED):** `PREREGISTRATION.md`, travado por `DISC-DEC-028`
(`00_GOVERNANCE/DECISION_LEDGER.yaml`). Este documento reporta o resultado
exatamente como saiu da execução da análise pré-registrada — nenhuma
reformulação de hipótese, estatística, banda, regra de rejeição de
artefato, teste, ou critério de decisão foi feita depois de ver o dado.
**Data de execução:** 2026-08-22.
**Código:** `analysis/run_primary_analysis.py` (reexecutável, determinístico
— nenhuma aleatoriedade real é usada em nenhuma etapa do pipeline).
**Resultados numéricos completos:** `results/result_primary.json`
(sumário + todos os campos de decisão) e `results/per_subject_full.json`
(array completo por sujeito, por canal). Log de execução completo:
`results/run_log.txt`.

> **Este é o resultado da análise primária (não-adversarial), executado por
> um único agente.** Por `00_GOVERNANCE/AGENTS.md` passo 7, ele **não pode**
> ser catalogado como fechado (`01_PORTFOLIO/TEST_QUEUE.yaml`,
> `00_GOVERNANCE/CLAIM_LEDGER.yaml`) até que um segundo agente, instruído a
> tentar refutá-lo, reexecute a análise de forma independente (código
> próprio, mesma proveniência de dado) — essa reexecução **não** foi feita
> por este agente/sessão.

---

## Veredito

```
VEREDITO: REFUTA
```

O teste t de Welch rejeita `H0` (`p = 3.97×10⁻⁶ < α = 0,05`) **na direção
oposta** à prevista por `H_Tamesis`: `Ī(X)_MDD > Ī(X)_HC` (entropia
espectral **maior** em MDD, não menor). Isto corresponde, palavra por
palavra, ao critério **REFUTA** de `PREREGISTRATION.md` §6:

> "REFUTA: o teste t de Welch rejeita H0 na direção oposta (Ī(X)_MDD >
> Ī(X)_HC) — interpretável à luz do modelo concorrente §5.2 (rede mais
> randomizada/menos estruturada em MDD poderia, plausivelmente,
> correlacionar com entropia espectral maior, não menor)."

Isto **não** é lido aqui como "Tamesis refutado" de forma geral, nem como
"Sun et al. 2019 confirmado" — apenas como o resultado deste teste único,
pré-registrado, sobre este dataset, nesta condição (`EC`), com este N. Por
`AGENTS.md` ("Proibições"), nenhuma alegação além disso é feita, e este
resultado só pode ser catalogado como fechado depois da reexecução
adversarial obrigatória (passo 7).

---

## 1. Proveniência e acesso ao dado

Metodologia de download idêntica à já verificada na etapa de
operacionalização (`data/DOWNLOAD_VERIFICATION_MUMTAZ.log`): listagem
completa via `https://api.figshare.com/v2/articles/4244171` (HTTP 200),
filtro por nome de arquivo (`\bEC\b`, sem sobreposição com `EO`/`TASK`,
verificado estruturalmente antes do download — ver `load_ec_file_list()`
em `analysis/run_primary_analysis.py`), download via
`ndownloader.figshare.com/files/<id>` e **verificação de MD5 contra o
checksum fornecido pela própria API antes de qualquer arquivo ser usado**.
Nenhum arquivo com MD5 divergente foi usado (nenhum ocorreu). Nenhum dado
fabricado/embutido substituiu qualquer download real.

O filtro de nome produziu exatamente os 64 arquivos `EC` esperados por
`PREREGISTRATION.md` §3 (34 `MDD *`, 30 `H *`), sem sobreposição com os 65
arquivos `EO` nem os 64 `TASK` (193 no total — verificado programaticamente,
não apenas por contagem).

### 1.1 Desvio de disponibilidade de dado (NÃO um desvio de método) — 6/64 arquivos indisponíveis

**Achado, não decisão de design:** 6 dos 64 arquivos `EC` pré-registrados
retornam **HTTP 404 "Entity not found: file"** no endpoint de download do
Figshare, de forma reprodutível (3 tentativas cada, mais uma reverificação
manual direta no momento da redação deste relatório). Isto **não** é uma
falha de rede transitória desta sessão: os mesmos 6 arquivos, e **somente**
eles entre os 64, têm na própria listagem da API do Figshare
`computed_md5: ""` e `mimetype: "undefined"` (todos os outros 58 têm
`computed_md5` idêntico ao `supplied_md5` e um `mimetype` real) — evidência
independente e corroborante de que o backend de armazenamento do Figshare
está genuinamente sem esses objetos de arquivo, não um problema do lado
desta sessão. Confirmado idêntico também na versão 1 do artigo (não é um
problema introduzido pela v2).

| Arquivo | Figshare file id | MD5 esperado | HTTP (3 tentativas) |
|---|---|---|---|
| `H S12 EC.edf` | 6921113 | `7fb12388787f9480be050f05051e06e9` | 404, 404, 404 |
| `H S18 EC.edf` | 6921167 | `f7a9b9f7ff489dbbaaf02582a4f28394` | 404, 404, 404 |
| `MDD S4 EC.edf` | 6921410 | `5c2c7c05c957f43ebcb15502da69a52e` | 404, 404, 404 |
| `MDD S8 EC.edf` | 6921446 | `efbf6191abf8a845062215726fe50947` | 404, 404, 404 |
| `MDD S12 EC.edf` | 6921485 | `c5fbf6ae50d831f308a4853d23c385f2` | 404, 404, 404 |
| `MDD S16  EC.edf` | 6921521 | `fb08dd5e42d0f7dfaea22a6a7358f5e0` | 404, 404, 404 |

Por `AGENTS.md` ("Proibições": *"falha de download é reportada como falha,
nunca mascarada por um fallback silencioso"*), estes 6 sujeitos estão
**ausentes** da análise — nenhum dado substituto, em cache, ou fabricado foi
usado para eles. Isto reduz o pool analisável, **antes** da regra de
rejeição de artefato, de 64 para **58** arquivos (30 `MDD`, 28 `H`
disponíveis por download). **Nenhum parâmetro de `I(X)`, `R_λ`, do
pré-processamento, do teste, ou do critério de decisão foi alterado por
causa disso** — apenas o conjunto de sujeitos com dado real disponível
mudou, por um fato externo sobre o dataset publicado, não por uma escolha
de design desta análise.

### 1.2 Anomalia descoberta — 2 pares de arquivos com conteúdo idêntico (byte-a-byte)

Durante o processamento dos 58 arquivos baixados, foi descoberto que:

- `H S27 EC.edf` e `H S30 EC.edf` são **byte-idênticos** (MD5
  `723217c6472d66e05cfef4fb122ccafe` para ambos).
- `MDD S33 EC.edf` e `MDD S34 EC.edf` são **byte-idênticos** (MD5
  `4c16e8636fca72ae59711c0ba803349f` para ambos).

Isto foi confirmado de duas formas independentes: (1) MD5 dos bytes
efetivamente baixados nesta sessão; (2) a própria API do Figshare já lista
`supplied_md5 == computed_md5` idêntico para os dois arquivos de cada par —
ou seja, é um artefato de proveniência do dataset publicado em si (dois
IDs de sujeito distintos apontando para a mesma gravação), **não** algo
introduzido por este pipeline. Nenhum outro par duplicado existe entre os
58 arquivos baixados (62 MD5s únicos em 58... na verdade 58 arquivos, 56
únicos + 2 pares — ver `results/result_primary.json`
→ `secondary_deduplication_sensitivity_check.duplicate_content_groups_found`).

**Decisão, seguindo `AGENTS.md` (proibição de reformular critério depois de
ver o dado):** `PREREGISTRATION.md` não declara nenhuma regra de
deduplicação. Introduzir uma agora, depois de ver que ela afetaria o
resultado (ou não), seria exatamente o tipo de reformulação pós-hoc que a
governança proíbe. **O veredito primário acima usa todos os 58 arquivos
baixados e verificados, sem deduplicação** — exatamente como pré-registrado
("todo sujeito com dado EC real disponível e que passa a regra de
artefato"). Uma checagem de robustez **secundária/exploratória** (rótulo
explícito, não decide o veredito) foi computada removendo um membro de cada
par duplicado:

| | N (MDD/HC) | Ī(X) MDD | Ī(X) HC | t | p | Mann-Whitney p | d | Direção |
|---|---|---|---|---|---|---|---|---|
| **Primário (sem dedup)** | 30/26 | 0,7613 | 0,6558 | 5,268 | 3,97×10⁻⁶ | 5,14×10⁻⁶ | 1,447 | MDD>HC |
| Secundário (com dedup) | 29/25 | 0,7583 | 0,6559 | 4,981 | 1,19×10⁻⁵ | 1,23×10⁻⁵ | 1,399 | MDD>HC |

O resultado é robusto a esta anomalia — a duplicação não é responsável pela
significância observada (ambas as versões rejeitam `H0` na mesma direção,
com magnitude e significância comparáveis). Isto é reportado por
transparência e como gatilho de anomalia (`METHODOLOGY_EXTENSIONS.md` §5,
"contaminação de dataset" como um dos mecanismos que um debunker
convencional deveria checar) — recomendado como item de verificação
explícito para a reexecução adversarial (passo 7).

---

## 2. Pipeline exato (recapitulado de `PREREGISTRATION.md` §2, §4)

- **Canais:** 19 EEG nomeados (10-20), montagem `-LE` (orelhas ligadas),
  sem re-referenciação — lidos diretamente do rótulo de canal EDF.
- **Taxa de amostragem:** 256 Hz (verificado por sujeito, todos batem).
- **Regra de rejeição de artefato (§4.5):** janela de 4s (1024 amostras,
  grade de 50% sobreposição) rejeitada se **qualquer** um dos 19 canais
  exceder ±150 μV pico-a-pico nessa janela — **uma máscara de rejeição
  compartilhada por sujeito** (não independente por canal), aplicada
  identicamente aos 19 canais. Sujeito excluído se >50% das janelas dessa
  máscara forem rejeitadas.
- **Welch PSD (§4.4):** janela Hann (convenção periódica/`fftbins=True` do
  próprio `scipy.signal.welch`, verificada bit-a-bit contra
  `scipy.signal.welch` como autoteste do script — ver
  `verify_welch_matches_scipy()`), `nperseg=1024`, `noverlap=512`,
  `nfft=1024`, detrend por remoção de média (`constant`), escala de
  densidade (`density`).
- **`R_λ = [1, 40]` Hz.**
- **`I(X)` (§2):** entropia de Shannon da PSD de Welch normalizada como
  pmf sobre `R_λ`, dividida por `log2(N)` bins. Computada **por janela não
  rejeitada, por canal**, depois média sobre as janelas não rejeitadas,
  depois média sobre os 19 canais → `Ī(X)` por sujeito.
- **Potência bruta de banda (§5.3, controle descritivo):** `Σ P(f)` não
  normalizada sobre `R_λ`, mesma média (janelas não rejeitadas → canais).
  **Não entra no critério de decisão.**
- **Teste primário (§6):** t de Welch (`scipy.stats.ttest_ind(...,
  equal_var=False)`), bicaudal, `α=0,05`, **sem correção de comparações
  múltiplas** (§8, decisão deliberada e travada — não alterada aqui).
- **Teste companheiro:** Mann-Whitney U, reportado, não decide o veredito.

---

## 3. Resultados — grupo

| Grupo | N incluído | Ī(X) média | Ī(X) DP | Potência bruta média (μV²) | Potência bruta DP (μV²) |
|---|---|---|---|---|---|
| MDD | 30 | 0,761322 | 0,059954 | 334,04 | 263,82 |
| HC | 26 | 0,655848 | 0,085486 | 386,49 | 166,91 |

Nota sobre a potência bruta (controle §5.3, não decide o veredito): a
direção é **oposta** à de `Ī(X)` — HC tem potência bruta média **maior**
que MDD, enquanto MDD tem `Ī(X)` **maior** que HC. Isto é consistente com
`Ī(X)` estar capturando algo além de um simples reescalonamento de
amplitude (o nulo "apenas amplitude" de §5.3 não explica trivialmente o
padrão observado em `Ī(X)`, já que as duas estatísticas nem sequer vão na
mesma direção entre os grupos).

### Estatísticas de teste

| Estatística | Valor |
|---|---|
| t de Welch | `t = 5,2678` |
| p (t de Welch, bicaudal) | `p = 3,970×10⁻⁶` |
| Mann-Whitney U | `U = 668,0` |
| p (Mann-Whitney, bicaudal) | `p = 5,136×10⁻⁶` |
| Cohen's d (pooled SD) | `d = 1,447` |
| Direção observada | `Ī(X)_MDD > Ī(X)_HC` (oposta à prevista) |
| Rejeita H0 em α=0,05? | Sim |

O teste companheiro (Mann-Whitney) confirma a mesma direção e ordem de
grandeza de significância do teste primário — consistência qualitativa
esperada por §6, não usada para decidir o veredito por si só.

**Poder a priori (§7, recomputado aqui apenas como referência, não
recalculado com o N reduzido):** o pré-registro já reconhecia que o desenho
(N=34/30 nominal) só tinha 80% de poder para `d≥0,713`. O `d` observado
(1,447) é quase o dobro desse mínimo — um efeito muito maior do que o
desenho foi dimensionado para detectar, na direção **oposta** à prevista.

---

## 4. Sujeitos excluídos pela regra de artefato (§4.5)

2 de 58 sujeitos com dado disponível foram excluídos (ambos do grupo HC):

| Arquivo | Grupo | Janelas rejeitadas | Janelas totais | Fração rejeitada | Motivo |
|---|---|---|---|---|---|
| `H S5 EC.edf` | HC | 150 | 150 | 100,0% | Canal `Fz` com amplitude anormalmente alta (DP≈48μV, p2p≈264μV, vs. DP≈10-14μV nos outros 18 canais do mesmo sujeito) faz **toda** janela de 4s exceder ±150μV em pelo menos um canal — consistente com a regra §4.5 (rejeição compartilhada entre os 19 canais), não um erro de parsing (verificado inspecionando a amplitude de todos os 19 canais individualmente). `PREREGISTRATION.md` não define exclusão por canal isoladamente, então o sujeito inteiro é excluído, como especificado. |
| `H S19 EC.edf` | HC | 113 | 149 | 75,8% | Acima do limiar de 50% (§4.5); não investigado canal-a-canal além disso, pois a regra pré-registrada não distingue causa — apenas aplica o limiar. |

Nenhum sujeito do grupo MDD foi excluído pela regra de artefato.

---

## 5. Tabela completa por sujeito

`Ī(X)` = entropia espectral de Shannon normalizada, média sobre janelas não
rejeitadas e sobre os 19 canais. "--" = sujeito excluído (sem `Ī(X)`
computável). Array completo, incluindo `I(X)` por canal individual, em
`results/per_subject_full.json`.

| Grupo | S# | Arquivo | Excluído | Ī(X) | Potência bruta (μV²) | Janelas totais | Janelas usadas | Fração rejeitada |
|---|---|---|---|---|---|---|---|---|
| HC | 1 | H S1 EC.edf | não | 0,7774 | 280,3 | 149 | 138 | 7,4% |
| HC | 2 | H S2 EC.edf | não | 0,7121 | 421,8 | 150 | 146 | 2,7% |
| HC | 3 | H S3 EC.edf | não | 0,6939 | 457,7 | 149 | 149 | 0,0% |
| HC | 4 | H S4 EC.edf | não | 0,5127 | 640,1 | 149 | 147 | 1,3% |
| HC | 5 | H S5 EC.edf | **SIM** | -- | -- | 150 | 0 | 100,0% |
| HC | 6 | H S6 EC.edf | não | 0,6856 | 369,5 | 149 | 143 | 4,0% |
| HC | 7 | H S7 EC.edf | não | 0,7168 | 268,3 | 177 | 165 | 6,8% |
| HC | 8 | H S8 EC.edf | não | 0,5539 | 291,9 | 150 | 141 | 6,0% |
| HC | 9 | H S9 EC.edf | não | 0,5588 | 475,8 | 149 | 149 | 0,0% |
| HC | 10 | H S10 EC.edf | não | 0,6952 | 617,1 | 187 | 173 | 7,5% |
| HC | 11 | H S11 EC.edf | não | 0,7416 | 176,2 | 149 | 142 | 4,7% |
| HC | 12 | *(indisponível para download — ver §1.1)* | -- | -- | -- | -- | -- | -- |
| HC | 13 | H S13 EC.edf | não | 0,5416 | 205,6 | 149 | 146 | 2,0% |
| HC | 14 | H S14 EC.edf | não | 0,6306 | 369,0 | 150 | 150 | 0,0% |
| HC | 15 | H S15 EC.edf | não | 0,5487 | 491,7 | 149 | 149 | 0,0% |
| HC | 16 | H S16 EC.edf | não | 0,7919 | 157,2 | 145 | 145 | 0,0% |
| HC | 17 | H S17 EC.edf | não | 0,7526 | 221,1 | 153 | 153 | 0,0% |
| HC | 18 | *(indisponível para download — ver §1.1)* | -- | -- | -- | -- | -- | -- |
| HC | 19 | H S19 EC.edf | **SIM** | -- | -- | 149 | 36 | 75,8% |
| HC | 20 | H S20 EC.edf | não | 0,7151 | 767,9 | 152 | 130 | 14,5% |
| HC | 21 | H S21 EC.edf | não | 0,6342 | 530,8 | 149 | 146 | 2,0% |
| HC | 22 | H S22 EC.edf | não | 0,6809 | 493,4 | 149 | 131 | 12,1% |
| HC | 23 | H S23 EC.edf | não | 0,4845 | 353,9 | 150 | 81 | 46,0% |
| HC | 24 | H S24 EC.edf | não | 0,7474 | 184,3 | 148 | 142 | 4,1% |
| HC | 25 | H S25 EC.edf | não | 0,7242 | 137,6 | 149 | 144 | 3,4% |
| HC | 26 | H S26 EC.edf | não | 0,6083 | 608,5 | 150 | 120 | 20,0% |
| HC | 27 | H S27 EC.edf | não | 0,6555 | 298,9 | 149 | 149 | 0,0% *(conteúdo idêntico a S30, §1.2)* |
| HC | 28 | H S28 EC.edf | não | 0,5713 | 425,8 | 149 | 149 | 0,0% |
| HC | 29 | H S29 EC.edf | não | 0,6618 | 505,7 | 150 | 148 | 1,3% |
| HC | 30 | H S30 EC.edf | não | 0,6555 | 298,9 | 149 | 149 | 0,0% *(conteúdo idêntico a S27, §1.2)* |
| MDD | 1 | MDD S1 EC.edf | não | 0,7917 | 152,1 | 150 | 81 | 46,0% |
| MDD | 2 | MDD S2 EC.edf | não | 0,6562 | 695,2 | 147 | 134 | 8,8% |
| MDD | 3 | MDD S3 EC.edf | não | 0,7917 | 237,1 | 89 | 86 | 3,4% |
| MDD | 4 | *(indisponível para download — ver §1.1)* | -- | -- | -- | -- | -- | -- |
| MDD | 5 | MDD S5 EC.edf | não | 0,7755 | 370,4 | 150 | 133 | 11,3% |
| MDD | 6 | MDD S6 EC.edf | não | 0,7464 | 245,3 | 150 | 150 | 0,0% |
| MDD | 7 | MDD S7 EC.edf | não | 0,7880 | 177,9 | 149 | 124 | 16,8% |
| MDD | 8 | *(indisponível para download — ver §1.1)* | -- | -- | -- | -- | -- | -- |
| MDD | 9 | MDD S9 EC.edf | não | 0,8146 | 209,1 | 149 | 149 | 0,0% |
| MDD | 10 | MDD S10 EC.edf | não | 0,8012 | 190,6 | 149 | 139 | 6,7% |
| MDD | 11 | MDD S11 EC.edf | não | 0,7690 | 243,3 | 148 | 146 | 1,4% |
| MDD | 12 | *(indisponível para download — ver §1.1)* | -- | -- | -- | -- | -- | -- |
| MDD | 13 | MDD S13 EC.edf | não | 0,7594 | 166,2 | 149 | 145 | 2,7% |
| MDD | 14 | MDD S14 EC.edf | não | 0,8254 | 327,1 | 149 | 136 | 8,7% |
| MDD | 15 | MDD S15 EC.edf | não | 0,7558 | 194,2 | 149 | 133 | 10,7% |
| MDD | 16 | *(indisponível para download — ver §1.1)* | -- | -- | -- | -- | -- | -- |
| MDD | 17 | MDD S17 EC.edf | não | 0,7649 | 164,9 | 147 | 141 | 4,1% |
| MDD | 18 | MDD S18 EC.edf | não | 0,7210 | 350,0 | 149 | 146 | 2,0% |
| MDD | 19 | MDD S19 EC.edf | não | 0,7682 | 166,6 | 148 | 148 | 0,0% |
| MDD | 20 | MDD S20 EC.edf | não | 0,7494 | 229,0 | 148 | 130 | 12,2% |
| MDD | 21 | MDD S21 EC.edf | não | 0,7679 | 457,8 | 149 | 145 | 2,7% |
| MDD | 22 | MDD S22 EC.edf | não | 0,7953 | 139,4 | 147 | 142 | 3,4% |
| MDD | 23 | MDD S23 EC.edf | não | 0,6403 | 567,6 | 150 | 137 | 8,7% |
| MDD | 24 | MDD S24 EC.edf | não | 0,8218 | 161,2 | 149 | 149 | 0,0% |
| MDD | 25 | MDD S25 EC.edf | não | 0,6697 | 1300,1 | 149 | 84 | 43,6% |
| MDD | 26 | MDD S26 EC.edf | não | 0,7721 | 182,5 | 149 | 133 | 10,7% |
| MDD | 27 | MDD S27 EC.edf | não | 0,5984 | 465,2 | 149 | 139 | 6,7% |
| MDD | 28 | MDD S28 EC.edf | não | 0,6795 | 741,7 | 149 | 102 | 31,5% |
| MDD | 29 | MDD S29 EC.edf | não | 0,8027 | 185,7 | 149 | 144 | 3,4% |
| MDD | 30 | MDD S30 EC.edf | não | 0,7496 | 869,2 | 119 | 112 | 5,9% |
| MDD | 31 | MDD S31 EC.edf | não | 0,8012 | 182,4 | 150 | 148 | 1,3% |
| MDD | 32 | MDD S32 EC.edf | não | 0,7667 | 250,6 | 148 | 140 | 5,4% |
| MDD | 33 | MDD S33 EC.edf | não | 0,8480 | 199,5 | 148 | 125 | 15,5% *(conteúdo idêntico a S34, §1.2)* |
| MDD | 34 | MDD S34 EC.edf | não | 0,8480 | 199,5 | 148 | 125 | 15,5% *(conteúdo idêntico a S33, §1.2)* |

---

## 6. Gatilhos de descoberta adversarial de nulo (`AGENTS.md` passo 7 / `METHODOLOGY_EXTENSIONS.md` §5)

Este resultado é **REFUTA**, não **CONFIRMA** — os gatilhos formais de
"descoberta adversarial de nulos" de `METHODOLOGY_EXTENSIONS.md` §5 são
definidos para candidatos que **sobrevivem** à reexecução adversarial
padrão e entram no Gate de Replicação (ou seja, resultados CONFIRMA
promovidos), o que não é o caso aqui. Ainda assim, seguindo a instrução
explícita desta tarefa (verificar qualquer anomalia), duas anomalias reais
foram encontradas e documentadas integralmente acima, sem serem escondidas
ou usadas para alterar o veredito:

1. **6/64 arquivos indisponíveis para download** (§1.1) — mecanismo
   convencional plausível: problema de armazenamento/curadoria no Figshare,
   não um artefato estatístico desta análise.
2. **2 pares de arquivos com conteúdo idêntico** (§1.2) — mecanismo
   convencional plausível: erro de upload/rotulagem no dataset original
   (dois nomes de sujeito apontando para a mesma gravação). Testado
   explicitamente por uma checagem de robustez secundária (dedup) — o
   veredito **não muda** e a significância permanece muito alta
   (`p=1,19×10⁻⁵`) mesmo removendo a duplicação.

Nenhum outro gatilho de anomalia (efeito implausivelmente grande sem
explicação, inconsistência entre teste primário e companheiro, contagem de
canais/amostras divergente da esperada por sujeito, etc.) foi disparado —
verificado explicitamente: todos os 58 sujeitos com dado disponível tinham
exatamente os 19 canais nomeados presentes, taxa de amostragem 256 Hz
exata, e o teste t e o Mann-Whitney concordam em direção e ordem de
magnitude de significância.

---

## 7. Desvios do pré-registro

**Nenhum desvio de método, estatística, banda, regra de artefato, teste,
ou critério de decisão foi feito** — `I(X)`, `R_λ=[1,40]Hz`, os parâmetros
de Welch, a regra de rejeição ±150μV/50%, o teste t de Welch bicaudal
`α=0,05` sem correção, e o critério CONFIRMA/REFUTA/INCONCLUSIVO de §6
foram aplicados exatamente como travados em `PREREGISTRATION.md`.

Dois fatos sobre a **disponibilidade do dado real** (não sobre o método)
são documentados em detalhe nas §1.1–§1.2 acima e resumidos aqui para o
registro:

1. 6 dos 64 arquivos `EC` pré-registrados estão genuinamente indisponíveis
   no Figshare (HTTP 404 reproduzível, corroborado pelos próprios metadados
   da API) — não substituídos, não fabricados, simplesmente ausentes.
2. 2 pares de arquivos entre os 58 disponíveis têm conteúdo idêntico —
   artefato de proveniência do dataset original, não desta análise;
   reportado com uma checagem de robustez secundária que confirma que o
   veredito não depende dessa duplicação.

Nenhuma decisão de excluir/incluir esses casos foi tomada de forma a mudar
o critério pré-registrado — os 6 arquivos indisponíveis simplesmente não
entram por não existirem como bytes reais para baixar; os 2 pares
duplicados entram no veredito primário como pré-registrado (nenhuma regra
de deduplicação estava pré-declarada), com a análise de sensibilidade
reportada à parte, claramente rotulada como secundária.

---

## 8. O que este resultado NÃO estabelece (escopo, §9-§10 do pré-registro)

- Não é uma alegação diagnóstica ou clínica sobre depressão (§9 item 1) —
  não deve ser lido, citado, ou usado como ferramenta de triagem/diagnóstico
  para nenhum indivíduo.
- Não decide entre `PAPER_B` e Sun et al. 2019 de forma definitiva — apenas
  mostra que, neste dataset e nesta estatística, a direção observada é
  consistente qualitativamente com a direção que a topologia "mais
  randomizada" de Sun et al. 2019 sugeriria para entropia espectral, e
  inconsistente com a direção prevista por `PAPER_B` §3.1.
- Não é uma alegação "Tamesis refutado" em qualquer sentido amplo — é o
  resultado de **um** teste pré-registrado, que ainda precisa de
  reexecução adversarial (passo 7) antes de ser catalogado como fechado.
- Não toca o braço ansiedade/DASPS — não tocado, não baixado, permanece
  inteiramente fora de escopo.

---

## 9. Inventário de arquivos desta etapa

- `analysis/run_primary_analysis.py` — código completo, reexecutável,
  determinístico (leitor EDF próprio, Welch manual verificado bit-a-bit
  contra `scipy.signal.welch`, entropia de Shannon, download+MD5,
  detecção de duplicatas, testes estatísticos).
- `results/result_primary.json` — todos os números de decisão, grupo,
  exclusões, arquivos indisponíveis, checagem de deduplicação.
- `results/per_subject_full.json` — `Ī(X)` e potência bruta por sujeito
  **e por canal individual** (todos os 58 sujeitos com dado disponível,
  incluindo os 2 excluídos com seus campos vazios/nulos).
- `results/run_log.txt` — log completo de execução (download, exclusões,
  anomalias, resultado).
- `RESULTS_PRIMARY.md` — este documento.

**Nenhum arquivo `.edf` bruto foi retido** neste diretório após a análise —
os cabeçalhos EDF deste dataset contêm campos `patient_id` com strings que
se parecem com nomes reais de sujeitos (mesma observação de privacidade já
registrada em `data/DOWNLOAD_VERIFICATION_MUMTAZ.log`); os 58 arquivos
baixados e verificados por MD5 foram removidos depois do cálculo, seguindo
o mesmo precedente já estabelecido na etapa de operacionalização — a
verificação de integridade (checksum, formato, resultado numérico) não
depende de reter o binário.
